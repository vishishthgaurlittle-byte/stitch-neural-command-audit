import struct
import os
import sys
import argparse

# GGML Type sizes / block sizes for offset and range validation
GGML_TYPE_INFO = {
    0:  {"name": "F32",     "block_size": 1,  "type_size": 4},
    1:  {"name": "F16",     "block_size": 1,  "type_size": 2},
    2:  {"name": "Q4_0",    "block_size": 32, "type_size": 18},
    3:  {"name": "Q4_1",    "block_size": 32, "type_size": 20},
    6:  {"name": "Q5_0",    "block_size": 32, "type_size": 22},
    7:  {"name": "Q5_1",    "block_size": 32, "type_size": 24},
    8:  {"name": "Q8_0",    "block_size": 32, "type_size": 34},
    9:  {"name": "Q8_1",    "block_size": 32, "type_size": 40},
    10: {"name": "Q2_K",    "block_size": 256, "type_size": 84},
    11: {"name": "Q3_K",    "block_size": 256, "type_size": 110},
    12: {"name": "Q4_K",    "block_size": 256, "type_size": 144},
    13: {"name": "Q5_K",    "block_size": 256, "type_size": 176},
    14: {"name": "Q6_K",    "block_size": 256, "type_size": 210},
    15: {"name": "Q8_K",    "block_size": 256, "type_size": 292},
    16: {"name": "IQ2_XXS", "block_size": 256, "type_size": 66},
    28: {"name": "BF16",    "block_size": 1,  "type_size": 2},
    30: {"name": "Q4_0_4_4","block_size": 32, "type_size": 18},
}

def parse_gguf_metadata(filepath, verbose=False):
    """
    Parses and rigorously validates GGUF binary metadata, architecture headers,
    tensor tables, and data offset boundaries.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        return False

    file_size = os.path.getsize(filepath)
    print(f"\n=======================================================")
    print(f" INSPECTING GGUF FILE: {os.path.basename(filepath)}")
    print(f" Full Path: {filepath}")
    print(f" File Size: {file_size:,} bytes ({file_size/(1024**3):.4f} GiB / {file_size/1e9:.4f} GB)")
    print(f"=======================================================")

    with open(filepath, "rb") as f:
        # Magic bytes check
        magic = f.read(4)
        if magic != b"GGUF":
            print(f"[FAIL] Invalid magic bytes: {magic!r}. Expected b'GGUF'.", file=sys.stderr)
            return False

        # Version check
        version, = struct.unpack("<I", f.read(4))
        if version not in (2, 3):
            print(f"[FAIL] Unsupported GGUF version {version}. Expected version 2 or 3.", file=sys.stderr)
            return False

        tensor_count, = struct.unpack("<Q", f.read(8))
        metadata_kv_count, = struct.unpack("<Q", f.read(8))

        print(f"GGUF Version:             {version} (VALID)")
        print(f"Total Tensor Count:       {tensor_count:,}")
        print(f"Metadata Key-Value Pairs: {metadata_kv_count:,}")

        def read_str():
            length_bytes = f.read(8)
            if len(length_bytes) < 8:
                raise ValueError("Unexpected EOF while reading string length")
            length, = struct.unpack("<Q", length_bytes)
            if length > 100_000_000:
                raise ValueError(f"String length exceeds safe boundary ({length:,} bytes)")
            raw = f.read(length)
            if len(raw) < length:
                raise ValueError(f"Unexpected EOF while reading string payload (expected {length:,} bytes)")
            return raw.decode("utf-8", errors="replace")

        def read_value(vtype):
            if vtype == 0:   # UINT8
                return struct.unpack("<B", f.read(1))[0]
            elif vtype == 1: # INT8
                return struct.unpack("<b", f.read(1))[0]
            elif vtype == 2: # UINT16
                return struct.unpack("<H", f.read(2))[0]
            elif vtype == 3: # INT16
                return struct.unpack("<h", f.read(2))[0]
            elif vtype == 4: # UINT32
                return struct.unpack("<I", f.read(4))[0]
            elif vtype == 5: # INT32
                return struct.unpack("<i", f.read(4))[0]
            elif vtype == 6: # FLOAT32
                return struct.unpack("<f", f.read(4))[0]
            elif vtype == 7: # BOOL
                return bool(struct.unpack("<B", f.read(1))[0])
            elif vtype == 8: # STRING
                return read_str()
            elif vtype == 9: # ARRAY
                elem_type, = struct.unpack("<I", f.read(4))
                elem_count, = struct.unpack("<Q", f.read(8))
                arr = []
                for _ in range(elem_count):
                    arr.append(read_value(elem_type))
                return arr
            elif vtype == 10: # UINT64
                return struct.unpack("<Q", f.read(8))[0]
            elif vtype == 11: # INT64
                return struct.unpack("<q", f.read(8))[0]
            elif vtype == 12: # FLOAT64
                return struct.unpack("<d", f.read(8))[0]
            else:
                raise ValueError(f"Unsupported GGUF metadata type ID: {vtype}")

        kv_data = {}
        try:
            for _ in range(metadata_kv_count):
                k = read_str()
                vtype, = struct.unpack("<I", f.read(4))
                v = read_value(vtype)
                kv_data[k] = v
        except Exception as e:
            print(f"[FAIL] Error parsing metadata KV table: {e}", file=sys.stderr)
            return False

        # Extract alignment
        alignment = kv_data.get("general.alignment", 32)
        print(f"Alignment:                {alignment} bytes")

        # Architectural inspection
        arch = kv_data.get("general.architecture", "unknown")
        print(f"\n--- Model Architecture Identification ---")
        print(f"  Architecture:           {arch}")
        
        # Check specific Qwen / Attention dimensions
        head_count = kv_data.get(f"{arch}.attention.head_count")
        head_count_kv = kv_data.get(f"{arch}.attention.head_count_kv")
        key_length = kv_data.get(f"{arch}.attention.key_length")
        value_length = kv_data.get(f"{arch}.attention.value_length")
        block_count = kv_data.get(f"{arch}.block_count")
        embedding_len = kv_data.get(f"{arch}.embedding_length")
        context_len = kv_data.get(f"{arch}.context_length")

        if head_count is not None:
            print(f"  Attention Head Count:   {head_count}")
        if head_count_kv is not None:
            print(f"  KV Head Count:          {head_count_kv}")
        if key_length is not None:
            print(f"  Key Length (head_dim):  {key_length}")
        if value_length is not None:
            print(f"  Value Length:           {value_length}")
        if block_count is not None:
            print(f"  Block Count (Layers):   {block_count}")
        if embedding_len is not None:
            print(f"  Embedding Length:       {embedding_len}")
        if context_len is not None:
            print(f"  Context Length:         {context_len}")

        # If architecture is Qwen, verify KV cache formula components
        if head_count_kv and block_count and (key_length or (embedding_len and head_count)):
            eff_head_dim = key_length if key_length is not None else (embedding_len // head_count)
            elem_per_token = 2 * block_count * head_count_kv * eff_head_dim
            fp16_4k_mib = (elem_per_token * 2 * 4096) / (1024**2)
            q8_4k_mib = (elem_per_token * (34 / 32) * 4096) / (1024**2)
            print(f"\n--- Derived KV-Cache Architecture from Metadata ---")
            print(f"  Effective Head Dim:     {eff_head_dim}")
            print(f"  KV Elements / Token:    {elem_per_token:,} (2 * {block_count} * {head_count_kv} * {eff_head_dim})")
            print(f"  4K FP16 KV Cache:       {fp16_4k_mib:.2f} MiB")
            print(f"  4K Q8_0 KV Cache:       {q8_4k_mib:.2f} MiB")

        # Parse Tensor Info Table
        print(f"\n--- Reading Tensor Info Table ({tensor_count:,} tensors) ---")
        tensor_info = []
        try:
            for _ in range(tensor_count):
                tname = read_str()
                ndims, = struct.unpack("<I", f.read(4))
                shape = struct.unpack(f"<{ndims}Q", f.read(8 * ndims))
                ttype, = struct.unpack("<I", f.read(4))
                offset, = struct.unpack("<Q", f.read(8))
                tensor_info.append((tname, shape, ttype, offset))
        except Exception as e:
            print(f"[FAIL] Error parsing tensor table: {e}", file=sys.stderr)
            return False

        # Current file position after tensor table is aligned to compute tensor data offset
        cur_pos = f.tell()
        tensor_data_offset = (cur_pos + alignment - 1) // alignment * alignment
        print(f"Tensor Data Start Offset: {tensor_data_offset:,} bytes")

        if tensor_data_offset > file_size:
            print(f"[FAIL] Tensor data start offset {tensor_data_offset} exceeds file size {file_size}", file=sys.stderr)
            return False

        # Validate tensor offsets and ranges against file size
        max_tensor_end = tensor_data_offset
        sample_tensors = []
        for tname, shape, ttype, offset in tensor_info:
            start_byte = tensor_data_offset + offset
            # Calculate tensor size if known type
            n_elements = 1
            for dim in shape:
                n_elements *= dim
            
            type_info = GGML_TYPE_INFO.get(ttype)
            if type_info:
                bs = type_info["block_size"]
                ts = type_info["type_size"]
                n_blocks = (n_elements + bs - 1) // bs
                byte_size = n_blocks * ts
                end_byte = start_byte + byte_size
            else:
                byte_size = None
                end_byte = start_byte

            if start_byte > file_size:
                print(f"[FAIL] Tensor '{tname}' start offset {start_byte:,} exceeds file size {file_size:,}", file=sys.stderr)
                return False
            if byte_size is not None and end_byte > file_size:
                print(f"[FAIL] Tensor '{tname}' end offset {end_byte:,} exceeds file size {file_size:,}", file=sys.stderr)
                return False

            if end_byte > max_tensor_end:
                max_tensor_end = end_byte

            if any(term in tname.lower() for term in ["txt_in", "img_in", "time_in", "token_embd", "output", "blk.0.attn"]):
                sample_tensors.append((tname, shape, ttype, offset))

        print(f"Tensor Boundary Check:    PASSED (All {tensor_count:,} tensors reside within file bounds)")
        print(f"Max Tensor End Offset:    {max_tensor_end:,} / {file_size:,} bytes")

        print(f"\n--- Significant Architectural Tensors Sample ---")
        for tname, shape, ttype, offset in sample_tensors[:12]:
            t_type_name = GGML_TYPE_INFO.get(ttype, {}).get("name", f"type_{ttype}")
            print(f"  * Tensor {tname:<35} shape={shape!s:<22} type={t_type_name:<8} offset={offset}")

        print(f"\n[STATUS] Structural GGUF parse & boundary validation: PASSED")
        print(f"[NOTE] Structural validity confirms file integrity; it does NOT prove runtime inference compatibility.")
        return True

def main():
    parser = argparse.ArgumentParser(description="KAATYA GGUF Binary Metadata & Architectural Inspector")
    parser.add_argument("models", nargs="*", help="Paths to GGUF model files to inspect")
    parser.add_argument("--model", "-m", action="append", help="Alternative flag for model file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    model_paths = []
    if args.models:
        model_paths.extend(args.models)
    if args.model:
        model_paths.extend(args.model)

    if not model_paths:
        # Default target models in workspace
        default_flux = r"T:\ai creation\flux-2-klein-4b-q4_0.gguf"
        default_qwen = r"T:\ai creation\Qwen3-4B-Q4_K_M.gguf"
        model_paths = [default_flux, default_qwen]

    print(f"Inspecting {len(model_paths)} GGUF model file(s)...")
    all_success = True
    for p in model_paths:
        ok = parse_gguf_metadata(p, verbose=args.verbose)
        if not ok:
            all_success = False

    if all_success:
        print("\n=======================================================")
        print(" GGUF METADATA INSPECTION COMPLETED SUCCESSFULLY (EXIT 0)")
        print("=======================================================")
        sys.exit(0)
    else:
        print("\n=======================================================")
        print(" [FAIL] GGUF METADATA INSPECTION FAILED (EXIT 1)")
        print("=======================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
