#!/usr/bin/env python3
# helper.py - compute offset and ret (lab formula) from buffer and ebp addresses
# Usage:
#   python3 helper.py 0xffffc458 0xffffc4d8
#   python3 helper.py 0xffffc458 0xffffc4d8 --payload-len 517 --no-plus128

import argparse

def parse_hex(s):
    s = s.strip().lower()
    if s.startswith("0x"):
        return int(s, 16)
    return int(s, 16)

def main():
    p = argparse.ArgumentParser(description="Compute offset index and lab-formula ret")
    p.add_argument("--buffer", help="buffer start address (hex), e.g. 0xffffc458")
    p.add_argument("--ebp", help="frame pointer ebp (hex), e.g. 0xffffc4d8")
    p.add_argument("--payload-len", type=int, default=517, help="payload length (default 517)")
    p.add_argument("--no-plus128", action="store_true",
                   help="omit the +128 slack in the lab formula (use ebp+12+32 only)")
    args = p.parse_args()

    try:
        buffer = parse_hex(args.buffer)
        ebp    = parse_hex(args.ebp)
    except Exception as e:
        print("Error parsing hex addresses:", e)
        sys.exit(1)

    if ebp < buffer:
        print("Warning: ebp < buffer (this is unusual). Did you swap the arguments?")
        # continue, but print both orders
    offset_to_ebp = ebp - buffer
    saved_eip_addr = ebp + 4
    offset_index = saved_eip_addr - buffer

    # lab formula: ret = buffer + offset_to_ebp + 12 + 32 + 128
    base_extra = 12 + 32
    extra_128 = 128 if not args.no_plus128 else 0
    ret = buffer + offset_to_ebp + base_extra + extra_128

    # safety checks
    in_bounds = (0 <= offset_index <= args.payload_len - 4)

    print("buffer =", hex(buffer))
    print("ebp    =", hex(ebp))
    print(f"offset_to_ebp = ebp - buffer \noffset_to_ebp = hex: {hex(offset_to_ebp)}, decimal:{offset_to_ebp}\n\n")
    

    print(f"ret = buffer + offset_to_ebp + 12 + 32 + {extra_128}\nret = hex: {hex(ret)}, decimal:{ret}")

    payload_offset_value = ret.to_bytes(4, byteorder='little')

    print(f"\n\nRET_ADDR little-endian bytes (will be written into payload[offset:offset+4]):\n payload_offset_value= hex:{(payload_offset_value.hex())}, decimal: {payload_offset_value}, list(payload_offset_value): {list(payload_offset_value)}\n\n")

    print("saved_eip_addr (ebp+4) =", hex(saved_eip_addr))
    print("offset_index (where saved EIP lives relative to buffer) =", offset_index, hex(offset_index))
    print("payload length =", args.payload_len)
    print("offset_index in payload bounds? ->", in_bounds)

    # check for zero bytes in LE representation
    if b'\x00' in payload_offset_value:
        print("Warning: RET_ADDR contains 0x00 bytes; if the victim uses strcpy/scanf(\"%s\") this could terminate the copy early.")

    # also print example offset check: (ebp+4) - buffer should equal the offset you computed earlier manually
    print()
    print("Example: saved EIP absolute address - buffer start = offset_index")
    abs_check = saved_eip_addr - buffer
    print("  ", hex(saved_eip_addr), "-", hex(buffer), "=", hex(abs_check), abs_check)

if __name__ == "__main__":
    main()