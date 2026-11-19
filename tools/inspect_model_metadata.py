import struct, os, sys

def inspect_flux():
    path = r'T:\ai creation\flux-2-klein-4b-q4_0.gguf'
    if not os.path.exists(path):
        print('File not found:', path)
        return

    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic != b'GGUF':
            print('Not GGUF:', magic)
            return
        version, = struct.unpack('<I', f.read(4))
        ti_count, = struct.unpack('<Q', f.read(8))
        kv_count, = struct.unpack('<Q', f.read(8))
        print(f'=== FLUX.2 Klein GGUF ===')
        print(f'Magic: {magic}, Version: {version}, Tensors: {ti_count}, KV metadata count: {kv_count}')

        def read_str():
            slen, = struct.unpack('<Q', f.read(8))
            return f.read(slen).decode('utf-8', errors='replace')

        def skip_val(vtype):
            if vtype in (0, 1, 7): # u8, i8, bool
                f.seek(1, 1)
            elif vtype in (2, 3): # u16, i16
                f.seek(2, 1)
            elif vtype in (4, 5, 12): # u32, i32, f32
                f.seek(4, 1)
            elif vtype in (6, 10, 11, 13): # u64, i64, f64
                f.seek(8, 1)
            elif vtype == 8: # str
                slen, = struct.unpack('<Q', f.read(8))
                f.seek(slen, 1)
            elif vtype == 9: # arr
                atype, = struct.unpack('<I', f.read(4))
                alen, = struct.unpack('<Q', f.read(8))
                for _ in range(alen):
                    skip_val(atype)

        for i in range(kv_count):
            k = read_str()
            vtype, = struct.unpack('<I', f.read(4))
            if vtype == 8:
                slen, = struct.unpack('<Q', f.read(8))
                val = f.read(slen).decode('utf-8', errors='replace')
                print(f'KV: {k} = "{val}"')
            elif vtype in (4, 5, 12):
                val, = struct.unpack('<I', f.read(4))
                print(f'KV: {k} = {val}')
            elif vtype in (6, 10):
                val, = struct.unpack('<Q', f.read(8))
                print(f'KV: {k} = {val}')
            else:
                skip_val(vtype)

        print('\n=== Relevant Input Tensors ===')
        for i in range(ti_count):
            tname = read_str()
            ndims, = struct.unpack('<I', f.read(4))
            shape = struct.unpack(f'<{ndims}Q', f.read(8 * ndims))
            ttype, = struct.unpack('<I', f.read(4))
            offset, = struct.unpack('<Q', f.read(8))
            if any(term in tname for term in ['txt_in', 'img_in', 'vector_in', 'time_in', 'guidance_in', 'final_layer']):
                print(f'Tensor: {tname:35} shape={shape} type={ttype}')

def inspect_qwen_main():
    path = r'T:\ai creation\Qwen3-4B-Q4_K_M.gguf'
    if not os.path.exists(path):
        print('File not found:', path)
        return
    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic != b'GGUF':
            return
        version, = struct.unpack('<I', f.read(4))
        ti_count, = struct.unpack('<Q', f.read(8))
        kv_count, = struct.unpack('<Q', f.read(8))
        print(f'\n=== Qwen3-4B-Q4_K_M GGUF ===')
        print(f'Tensors: {ti_count}, KV metadata count: {kv_count}')

        def read_str():
            slen, = struct.unpack('<Q', f.read(8))
            return f.read(slen).decode('utf-8', errors='replace')

        def skip_val(vtype):
            if vtype in (0, 1, 7): f.seek(1, 1)
            elif vtype in (2, 3): f.seek(2, 1)
            elif vtype in (4, 5, 12): f.seek(4, 1)
            elif vtype in (6, 10, 11, 13): f.seek(8, 1)
            elif vtype == 8:
                slen, = struct.unpack('<Q', f.read(8))
                f.seek(slen, 1)
            elif vtype == 9:
                atype, = struct.unpack('<I', f.read(4))
                alen, = struct.unpack('<Q', f.read(8))
                for _ in range(alen):
                    skip_val(atype)

        for i in range(kv_count):
            k = read_str()
            vtype, = struct.unpack('<I', f.read(4))
            if any(x in k for x in ['context_length', 'embedding_length', 'block_count', 'head_count', 'feed_forward_length', 'rope']):
                if vtype in (4, 5, 12):
                    val, = struct.unpack('<I', f.read(4))
                    print(f'KV: {k} = {val}')
                elif vtype in (6, 10):
                    val, = struct.unpack('<Q', f.read(8))
                    print(f'KV: {k} = {val}')
                elif vtype == 8:
                    slen, = struct.unpack('<Q', f.read(8))
                    val = f.read(slen).decode('utf-8', errors='replace')
                    print(f'KV: {k} = "{val}"')
                else:
                    skip_val(vtype)
            else:
                skip_val(vtype)

if __name__ == '__main__':
    inspect_flux()
    inspect_qwen_main()
