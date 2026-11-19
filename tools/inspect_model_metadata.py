import struct
import os
import sys

def parse_gguf_metadata(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    file_size = os.path.getsize(filepath)
    print(f"\n=======================================================")
    print(f" INSPECTING GGUF FILE: {os.path.basename(filepath)}")
    print(f" Full Path: {filepath}")
    print(f" File Size: {file_size:,} bytes ({file_size/(1024**3):.4f} GiB / {file_size/1e9:.4f} GB)")
    print(f"=======================================================")

    with open(filepath, "rb") as f:
        magic = f.read(4)
        if magic != b"GGUF":
            print(f"[ERROR] Invalid magic bytes: {magic}")
            return False

        version, = struct.unpack("<I", f.read(4))
        tensor_count, = struct.unpack("<Q", f.read(8))
        metadata_kv_count, = struct.unpack("<Q", f.read(8))

        print(f"GGUF Version:          {version}")
        print(f"Total Tensor Count:    {tensor_count:,}")
        print(f"Metadata Key-Value Pairs: {metadata_kv_count:,}")

        def read_str():
            length, = struct.unpack("<Q", f.read(8))
            if length > 100_000_000:
                raise ValueError(f"String length too large ({length}), likely alignment error")
            raw = f.read(length)
            return raw.decode("utf-8", errors="replace")

        def read_value(vtype):
            if vtype == 0:   # UINT8
                val, = struct.unpack("<B", f.read(1))
                return val
            elif vtype == 1: # INT8
                val, = struct.unpack("<b", f.read(1))
                return val
            elif vtype == 2: # UINT16
                val, = struct.unpack("<H", f.read(2))
                return val
            elif vtype == 3: # INT16
                val, = struct.unpack("<h", f.read(2))
                return val
            elif vtype == 4: # UINT32
                val, = struct.unpack("<I", f.read(4))
                return val
            elif vtype == 5: # INT32
                val, = struct.unpack("<i", f.read(4))
                return val
            elif vtype == 6: # FLOAT32 (4 bytes)
                val, = struct.unpack("<f", f.read(4))
                return val
            elif vtype == 7: # BOOL
                val, = struct.unpack("<B", f.read(1))
                return bool(val)
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
                val, = struct.unpack("<Q", f.read(8))
                return val
            elif vtype == 11: # INT64
                val, = struct.unpack("<q", f.read(8))
                return val
            elif vtype == 12: # FLOAT64 (8 bytes)
                val, = struct.unpack("<d", f.read(8))
                return val
            else:
                raise ValueError(f"Unsupported GGUF value type {vtype}")

        kv_data = {}
        for _ in range(metadata_kv_count):
            k = read_str()
            vtype, = struct.unpack("<I", f.read(4))
            v = read_value(vtype)
            kv_data[k] = v

        print(f"\n--- Parsed Key Architectural Metadata ({len(kv_data)} keys) ---")
        for k in sorted(kv_data.keys()):
            if any(term in k.lower() for term in ["architecture", "context", "embedding", "block", "head", "feed_forward", "vocab", "file_type", "quantization"]):
                val_disp = kv_data[k]
                if isinstance(val_disp, list) and len(val_disp) > 10:
                    val_disp = f"[Array of {len(val_disp)} elements]"
                print(f"  * {k:<45} = {val_disp}")

        print(f"\n--- Reading Tensor Info Table ({tensor_count} tensors) ---")
        tensor_info = []
        for _ in range(tensor_count):
            tname = read_str()
            ndims, = struct.unpack("<I", f.read(4))
            shape = struct.unpack(f"<{ndims}Q", f.read(8 * ndims))
            ttype, = struct.unpack("<I", f.read(4))
            offset, = struct.unpack("<Q", f.read(8))
            tensor_info.append((tname, shape, ttype, offset))
            if any(term in tname.lower() for term in ["txt_in", "img_in", "time_in", "vector_in", "ada_ln", "final_layer", "token_embd", "output"]):
                print(f"  * Tensor {tname:<35} shape={shape} type={ttype}")

        return True

if __name__ == "__main__":
    flux_path = r"T:\ai creation\flux-2-klein-4b-q4_0.gguf"
    qwen_path = r"T:\ai creation\Qwen3-4B-Q4_K_M.gguf"

    print("Executing GGUF Binary Metadata Inspection Tool...")
    success_flux = parse_gguf_metadata(flux_path)
    success_qwen = parse_gguf_metadata(qwen_path)

    if success_flux and success_qwen:
        print("\n=======================================================")
        print(" GGUF METADATA INSPECTION COMPLETED SUCCESSFULLY (EXIT 0)")
        print("=======================================================")
        sys.exit(0)
    else:
        print("\n[FAIL] GGUF metadata inspection failed")
        sys.exit(1)
