#!/usr/bin/env python3
"""SMW Game Genie helper: read the original bytes and print the entry lines.

    python3 -I cheats/tools/sgg.py 0585BF:04 05BD36:AD

Each argument is SNESADDR:NEW (hex). The original byte is read from the
US ROM: SMW_U.smc on the Mac, or build/SMW_U.smc in a cloud session
(made by cheats/cloud_build.sh). SMW is LoROM. Both files have a
512-byte copier header (524800 bytes), so
file offset = $200 + (bank & $7F) * $8000 + (addr & $7FFF).
The header is found from the file size.

It also prints the byte at each address in the other versions (J, SS,
E0, E1) when their ROMs are there, for the **Revisions:** line. The
same address can hold different code in another version.

It prints each code, then **Codes:** and **Raw form:** lines in the
format of cheats/smw_game_genie.md. It warns when an address is not in
ROM, when the new byte equals the original, and when the same byte
pattern (the original byte with 4 bytes on each side) also appears
somewhere else in the ROM, which can mean a copied routine you meant to
change too.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import snes_gg_encode as gg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
WORDS = ["", "", "both", "all three", "all four", "all five"]


def rom_path(ver="U"):
    for p in ("SMW_%s.smc" % ver, os.path.join("build", "SMW_%s.smc" % ver)):
        full = os.path.join(ROOT, p)
        if os.path.isfile(full):
            return full
    if ver != "U":
        return None
    sys.exit("No ROM: run cheats/cloud_build.sh first.")


def main(args):
    if not args:
        sys.exit(__doc__)
    path = rom_path()
    rom = open(path, "rb").read()
    hdr = len(rom) % 0x8000
    if hdr not in (0, 0x200):
        sys.exit("Odd ROM size %d: not a plain or copier-header LoROM file." % len(rom))
    others = {}
    for v in ("J", "SS", "E0", "E1"):
        p = rom_path(v)
        if p:
            others[v] = open(p, "rb").read()
    gg.selftest(2000)
    codes, raws = [], []
    for arg in args:
        a, _, v = arg.partition(":")
        addr, new = int(a, 16), int(v, 16)
        if not gg.is_lorom_rom_address(addr):
            sys.exit("$%06X is not in LoROM ROM space." % addr)
        off = hdr + (addr >> 16 & 0x7F) * 0x8000 + (addr & 0x7FFF)
        if off >= len(rom):
            sys.exit("$%06X is past the end of the ROM." % addr)
        orig = rom[off]
        code = gg.encode(addr, new)
        assert gg.decode(code) == (addr, new)
        note = ""
        if orig == new:
            note = "  WARNING: new byte equals the original"
        pat = rom[max(hdr, off - 4):off + 5]
        hits = rom[hdr:].count(pat)
        if hits > 1:
            note += "  NOTE: this 9-byte pattern appears %d times in the ROM" % hits
        print("%s   $%06X:%02X (orig $%02X, file $%05X)%s" % (code, addr, new, orig, off, note))
        if others:
            vs = []
            for v, data in others.items():
                o = len(data) % 0x8000 + (addr >> 16 & 0x7F) * 0x8000 + (addr & 0x7FFF)
                b = data[o] if o < len(data) else None
                same = b == orig and data[o - 4:o + 5] == rom[off - 4:off + 5]
                vs.append("%s $%02X%s" % (v, b, "" if same else " (differs)") if b is not None else v + " -")
            print("              other versions: " + ", ".join(vs))
        codes.append(code)
        raws.append("`%06X:%02X` (orig `$%02X`)" % (addr, new, orig))
    n = len(codes)
    use = "" if n == 1 else " (use %s)" % (WORDS[n] if n < len(WORDS) else "all %d" % n)
    print()
    print("ROM: %s" % os.path.relpath(path, ROOT))
    print("**Codes:** " + " + ".join("`%s`" % c for c in codes) + use)
    print("**Raw form:** " + "; ".join(raws))


if __name__ == "__main__":
    main(sys.argv[1:])
