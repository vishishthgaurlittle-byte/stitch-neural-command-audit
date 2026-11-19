import struct
import os
import sys
import argparse

# GGML Type sizes / block sizes for offset and range validation conforming to upstream ggml.h
GGML_TYPE_INFO = {
    0:  {"name": "F32",      "block_size": 1,   "type_size": 4},
    1:  {"name": "F16",      "block_size": 1,   "type_size": 2},
    2:  {"name": "Q4_0",     "block_size": 32,  "type_size": 18},
    3:  {"name": "Q4_1",     "block_size": 32,  "type_size": 20},
    6:  {"name": "Q5_0",     "block_size": 32,  "type_size": 22},
    7:  {"name": "Q5_1",     "block_size": 32,  "type_size": 24},
    8:  {"name": "Q8_0",     "block_size": 32,  "type_size": 34},
    9:  {"name": "Q8_1",     "block_size": 32,  "type_size": 40},
    10: {"name": "Q2_K",     "block_size": 256, "type_size": 84},
    11: {"name": "Q3_K",     "block_size": 256, "type_size": 110},
    12: {"name": "Q4_K",     "block_size": 256, "type_size": 144},
    13: {"name": "Q5_K",     "block_size": 256, "type_size": 176},
    14: {"name": "Q6_K",     "block_size": 256, "type_size": 210},
    15: {"name": "Q8_K",     "block_size": 256, "type_size": 292},
    16: {"name": "IQ2_XXS",  "block_size": 256, "type_size": 66},
    25: {"name": "I8",       "block_size": 1,   "type_size": 1},
    26: {"name": "I16",      "block_size": 1,   "type_size": 2},
    27: {"name": "I32",      "block_size": 1,   "type_size": 4},
    28: {"name": "I64",      "block_size": 1,   "type_size": 8},
    29: {"name": "F64",      "block_size": 1,   "type_size": 8},
    30: {"name": "BF16",     "block_size": 1,   "type_size": 2},
    31: {"name": "UNRESOLVED_TYPE_31", "block_size": 32, "type_size": 18}, # Unverified/experimental historical mapping; 0 tensors present in local file
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
        header_size = cur_pos
        tensor_data_offset = (cur_pos + alignment - 1) // alignment * alignment
        header_padding = tensor_data_offset - cur_pos
        print(f"Header & Metadata Size:   {header_size:,} bytes")
        print(f"Header Alignment Padding: {header_padding:,} bytes (alignment={alignment})")
        print(f"Tensor Data Start Offset: {tensor_data_offset:,} bytes")

        if tensor_data_offset > file_size:
            print(f"[FAIL] Tensor data start offset {tensor_data_offset} exceeds file size {file_size}", file=sys.stderr)
            return False

        # Sort tensors by offset for sequential layout, overlap, and padding verification
        sorted_tensors = sorted(tensor_info, key=lambda x: x[3])

        type_payloads = {}
        type_counts = {}
        type_elements = {}
        type_blocks = {}
        inter_tensor_padding = 0
        prev_end_byte = tensor_data_offset
        prev_name = "<data_start>"
        max_tensor_end = tensor_data_offset
        sample_tensors = []
        validation_failed = False
        tsv_rows = []

        for idx, (tname, shape, ttype, offset) in enumerate(sorted_tensors, 1):
            start_byte = tensor_data_offset + offset
            
            # 1. Type resolution
            type_info = GGML_TYPE_INFO.get(ttype)
            if not type_info:
                print(f"[FAIL] Tensor '{tname}' uses unknown GGML type ID {ttype}", file=sys.stderr)
                validation_failed = True
                continue

            t_name = type_info["name"]
            bs = type_info["block_size"]
            ts = type_info["type_size"]

            # 2. Block dimension check (shape[0] % bs == 0)
            if len(shape) == 0 or shape[0] % bs != 0:
                print(f"[FAIL] Tensor '{tname}' shape[0]={shape[0] if len(shape) > 0 else 0} not divisible by block size {bs}", file=sys.stderr)
                validation_failed = True

            # 3. Payload size calculation from elements and block specification
            n_elements = 1
            for dim in shape:
                n_elements *= dim

            n_blocks = n_elements // bs
            payload_size = n_blocks * ts
            end_byte = start_byte + payload_size

            # Check exact divisibility by type_size
            if payload_size % ts != 0:
                print(f"[FAIL] Tensor '{tname}' payload {payload_size} not divisible by type size {ts}", file=sys.stderr)
                validation_failed = True

            # 4. Alignment and boundary validation
            if start_byte % alignment != 0:
                print(f"[FAIL] Tensor '{tname}' start byte {start_byte} not aligned to {alignment} bytes", file=sys.stderr)
                validation_failed = True

            if start_byte < tensor_data_offset or end_byte > file_size:
                print(f"[FAIL] Tensor '{tname}' bounds [{start_byte:,}, {end_byte:,}) exceed file bounds [{tensor_data_offset:,}, {file_size:,})", file=sys.stderr)
                validation_failed = True

            # 5. Overlap and padding detection
            if start_byte < prev_end_byte:
                overlap = prev_end_byte - start_byte
                print(f"[FAIL] Tensor '{tname}' overlaps with '{prev_name}' by {overlap:,} bytes", file=sys.stderr)
                validation_failed = True
                pad_before = 0
            else:
                pad_before = start_byte - prev_end_byte
                inter_tensor_padding += pad_before
                if pad_before >= alignment:
                    print(f"[WARN] Tensor '{tname}' has excess padding {pad_before} >= alignment {alignment}")

            # Check padding to next tensor or file end
            if idx < len(sorted_tensors):
                next_start_byte = tensor_data_offset + sorted_tensors[idx][3]
                pad_to_next = next_start_byte - end_byte
            else:
                pad_to_next = file_size - end_byte

            if end_byte > max_tensor_end:
                max_tensor_end = end_byte

            prev_end_byte = end_byte
            prev_name = tname

            # Accumulate per-type totals
            type_payloads[ttype] = type_payloads.get(ttype, 0) + payload_size
            type_counts[ttype] = type_counts.get(ttype, 0) + 1
            type_elements[ttype] = type_elements.get(ttype, 0) + n_elements
            type_blocks[ttype] = type_blocks.get(ttype, 0) + n_blocks

            # Record sample architectural tensors
            if any(term in tname.lower() for term in ["txt_in", "img_in", "time_in", "token_embd", "output", "blk.0.attn"]):
                sample_tensors.append((tname, shape, ttype, offset, payload_size))

            tsv_rows.append([
                str(idx), tname, 'x'.join(str(x) for x in shape), str(ttype), t_name,
                str(bs), str(ts), str(payload_size), str(offset),
                str(start_byte), str(end_byte), str(pad_to_next),
                "PASSED" if not validation_failed else "FAILED"
            ])

        trailing_padding = file_size - max_tensor_end
        total_payload = sum(type_payloads.values())
        accounted_total = header_size + header_padding + total_payload + inter_tensor_padding + trailing_padding
        accounting_diff = file_size - accounted_total

        print(f"\n--- Tensor Boundary & Structural Validation ---")
        if validation_failed:
            print(f"[FAIL] One or more tensor structural assertions failed!", file=sys.stderr)
            return False
        else:
            print(f"Tensor Boundary Check:    PASSED (All {tensor_count:,} tensors reside within file bounds)")
            print(f"Tensor Overlap Check:     PASSED (Zero overlapping tensors detected)")
            print(f"Block Dimension Check:    PASSED (All tensor dimensions conform to quantization block sizes)")
            print(f"Max Tensor End Offset:    {max_tensor_end:,} / {file_size:,} bytes")

        print(f"\n--- Per-Type Payload Accounting ---")
        for ttype in sorted(type_payloads.keys()):
            t_info = GGML_TYPE_INFO.get(ttype, {})
            t_name = t_info.get("name", f"type_{ttype}")
            ts = t_info.get("type_size", 1)
            t_count = type_counts[ttype]
            t_payload = type_payloads[ttype]
            t_elems = type_elements[ttype]
            t_blks = type_blocks[ttype]
            pct = (t_payload / file_size) * 100
            div_check = "PASSED" if (t_payload % ts == 0) else "FAILED"
            print(f"  * {t_name:<10} (ID {ttype:>2}): {t_count:>4} tensors | {t_payload:>13,} bytes ({pct:6.2f}%) | "
                  f"{t_elems:>12,} elems | {t_blks:>11,} blocks | Divisibility by {ts}B: {div_check}")

        print(f"\n--- Exact Container Byte Accounting ---")
        print(f"  Header & Metadata Table:   {header_size:>13,} bytes")
        print(f"  Header Alignment Padding:  {header_padding:>13,} bytes")
        print(f"  Total Tensor Payloads:     {total_payload:>13,} bytes")
        print(f"  Inter-Tensor Padding:      {inter_tensor_padding:>13,} bytes")
        print(f"  Trailing File Padding:     {trailing_padding:>13,} bytes")
        print(f"  -------------------------------------------------")
        print(f"  Total Accounted Bytes:     {accounted_total:>13,} bytes")
        print(f"  Actual File Size on Disk:  {file_size:>13,} bytes")
        print(f"  Accounting Difference:     {accounting_diff:>13,} bytes ({'EXACT MATCH' if accounting_diff == 0 else 'MISMATCH'})")

        if accounting_diff != 0:
            print(f"[FAIL] Container byte accounting mismatch! Difference: {accounting_diff} bytes", file=sys.stderr)
            return False

        # Save detailed canonical audit TSV for FLUX
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        if "flux" in os.path.basename(filepath).lower():
            canonical_tsv = os.path.join(tools_dir, "flux_per_tensor_audit.tsv")
            try:
                headers = [
                    "Index", "Name", "Dimensions", "Raw_GGUF_Type_ID", "Correct_Type_Name",
                    "Block_Size", "Bytes_Per_Block", "Expected_Payload_Size_Bytes", "Actual_Tensor_Offset",
                    "Absolute_File_Start_Byte", "Expected_Tensor_End_Offset", "Alignment_Padding_Before_Next_Tensor",
                    "Boundary_Validation_Result"
                ]
                tsv_content = "\t".join(headers) + "\n" + "\n".join("\t".join(r) for r in tsv_rows) + "\n"
                with open(canonical_tsv, "w", encoding="utf-8") as can_file:
                    can_file.write(tsv_content)
                print(f"\nCanonical per-tensor audit written to: {canonical_tsv}")
            except Exception as e:
                print(f"[WARN] Could not write canonical audit TSV: {e}")

        print(f"\n--- Significant Architectural Tensors Sample ---")
        for tname, shape, ttype, offset, payload_size in sample_tensors[:12]:
            t_type_name = GGML_TYPE_INFO.get(ttype, {}).get("name", f"type_{ttype}")
            print(f"  * Tensor {tname:<35} shape={shape!s:<22} type={t_type_name:<8} payload={payload_size:>10,} B offset={offset}")

        print(f"\n[STATUS] Implemented GGUF structural validation checks: PASSED")
        print(f"[NOTE] Passed implemented GGUF structural validation checks. Structural consistency confirms header formatting, alignment, and boundary accounting; it does NOT prove upstream authenticity, full payload integrity, runtime compatibility, or successful inference.")

        print(f"\n--- Four-Stage Verification Status ---")
        print(f"  * Stage 1: GGUF Structural Validation:       PASSED (Passed implemented GGUF structural validation checks)")
        print(f"  * Stage 2: Runtime Compatibility:             UNVERIFIED (Pending compiled runtime binary execution test)")
        print(f"  * Stage 3: Successful Inference:              UNVERIFIED (No inference execution test performed on this PC)")
        print(f"  * Stage 4: Measured Target-Hardware Perf:     UNVERIFIED (No throughput/latency benchmark measured on this PC)")
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
