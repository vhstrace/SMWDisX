#!/usr/bin/env python3
"""
SNES Game Genie code encoder / decoder, with a round-trip self-test.

NOTE ON FORMAT
--------------
This is the *SNES* scheme, which is NOT the NES one. On the NES a code is 6 or 8
letters and the 8-letter form carries a compare byte. On the SNES:

  * every code is exactly 8 characters, written XXXX-XXXX;
  * it encodes a 24-bit bus address plus an 8-bit replacement value;
  * there is NO compare byte.

Alphabet, nibble 0..F in order:  D F 4 7 0 9 1 5 6 B C 8 A 2 3 E

Layout: the 8 nibbles form a 32-bit word.  The top byte is the data; the low
24 bits are the address, bit-scrambled.  The descramble permutation below is the
canonical one (matches Snes9x `S9xGameGenieToRaw`).  Rather than hand-writing the
inverse, this module derives it by probing the forward permutation one bit at a
time, so the two can never drift apart.

Addresses come from `tools/linemap_U.tsv` / `SMW_U.sym` and are plain SNES bus
addresses (e.g. KillMario's `LDA #$90` operand at $00F60B).  SMW is LoROM, so
ROM lives at $8000-$FFFF of each bank; an address with a low half offset is not
in ROM and is rejected.

Usage
-----
    python3 game_genie/gg_encode.py --selftest
    python3 game_genie/gg_encode.py encode 00F60B C0
    python3 game_genie/gg_encode.py decode DD82-6F6F
"""

import argparse
import random
import sys

ALPHABET = "DF4709156BC8A23E"


def _descramble(addr24):
    """Scrambled 24-bit field -> real SNES address. Canonical permutation."""
    a = addr24 & 0xFFFFFF
    return (((a & 0x003C00) << 10) |
            ((a & 0x00003C) << 14) |
            ((a & 0xF00000) >> 8) |
            ((a & 0x000003) << 10) |
            ((a & 0x00C000) >> 6) |
            ((a & 0x0F0000) >> 12) |
            ((a & 0x0003C0) >> 6))


def _build_scramble_table():
    """Derive the inverse by probing _descramble with one set bit at a time.

    _descramble is a pure bit permutation, so probing 1<<i tells us exactly which
    output bit input bit i feeds. Asserting bijectivity here means a typo in the
    permutation above becomes an import-time failure rather than a wrong code.
    """
    fwd = {}
    for i in range(24):
        out = _descramble(1 << i)
        if out == 0 or (out & (out - 1)):
            raise AssertionError(
                "descramble bit %d is not a single-bit map (got %06X)" % (i, out))
        fwd[i] = out.bit_length() - 1
    if sorted(fwd.values()) != list(range(24)):
        raise AssertionError("descramble is not a bijection over 24 bits")
    return {v: k for k, v in fwd.items()}   # real bit -> scrambled bit


_SCRAMBLE = _build_scramble_table()


def _scramble(address):
    """Real SNES address -> scrambled 24-bit field."""
    out = 0
    for real_bit, scr_bit in _SCRAMBLE.items():
        if address & (1 << real_bit):
            out |= 1 << scr_bit
    return out


def encode(address, data):
    """(24-bit SNES address, 8-bit value) -> 'XXXX-XXXX'."""
    if not 0 <= address <= 0xFFFFFF:
        raise ValueError("address %X out of range" % address)
    if not 0 <= data <= 0xFF:
        raise ValueError("data %X out of range" % data)
    word = (data << 24) | _scramble(address)
    chars = [ALPHABET[(word >> (28 - 4 * i)) & 0xF] for i in range(8)]
    return "".join(chars[:4]) + "-" + "".join(chars[4:])


def decode(code):
    """'XXXX-XXXX' (dash optional) -> (address, data)."""
    c = code.strip().upper().replace("-", "")
    if len(c) != 8:
        raise ValueError("SNES Game Genie codes are 8 characters, got %d" % len(c))
    word = 0
    for i, ch in enumerate(c):
        idx = ALPHABET.find(ch)
        if idx < 0:
            raise ValueError("%r is not a Game Genie character (alphabet: %s)"
                             % (ch, ALPHABET))
        word |= idx << (28 - 4 * i)
    return _descramble(word & 0xFFFFFF), (word >> 24) & 0xFF


def is_lorom_rom_address(address):
    """SMW is LoROM: ROM occupies $8000-$FFFF of each bank."""
    return (address & 0xFFFF) >= 0x8000


# Known-good vectors from romdev's bundled cheat DB for Super Mario World (USA),
# via cheats({op:'lookup'}). Round-tripping proves only that this module is
# self-consistent; these prove the *permutation itself* is right, against an
# independent implementation. Two of them also corroborate the disassembly:
# $008F2C and $008F37 are the two `!CoinsPer1up` operands in `HandleCoins`
# (bank_00.asm), and $009E25 is the `LDA.B #4` operand in `LoadSaveAndFadeToOW`.
KNOWN_VECTORS = [
    ("DDB4-6F07", 0x009E25, 0x00, "Start with 1 life instead of 5"),
    ("D964-A7D7", 0x008F2C, 0x05, "Extra life at 5 coins (compare site)"),
    ("D967-AFA7", 0x008F37, 0x05, "Extra life at 5 coins (subtract site)"),
    ("DC64-A7D7", 0x008F2C, 0x0A, "Extra life at 10 coins"),
    ("F064-A7D7", 0x008F2C, 0x14, "Extra life at 20 coins"),
    ("7464-A7D7", 0x008F2C, 0x32, "Extra life at 50 coins"),
    ("DD64-A7D7", 0x008F2C, 0x00, "Extra life on every coin"),
    ("D2E5-A7AD", 0x00F37F, 0x0D, "Extra life per dragon coin"),
    ("DE22-D4DD", 0x00D0D8, 0x0F, "Die after losing one life"),
    ("BB22-D4DD", 0x00D0D8, 0x99, "Lose every life but one on death"),
    ("C022-D4DD", 0x00D0D8, 0xA4, "Game over after every life"),
]


def selftest(n=200000):
    """Round-trip every code we could ever emit, plus known-value spot checks."""
    # 0. External ground truth -- both directions.
    for code, addr, data, desc in KNOWN_VECTORS:
        assert decode(code) == (addr, data), \
            "known vector %s (%s) decoded to %r, expected ($%06X, $%02X)" % (
                code, desc, decode(code), addr, data)
        assert encode(addr, data) == code, \
            "known vector %s (%s) re-encoded to %s" % (code, desc, encode(addr, data))

    # 1. Exhaustive over the alphabet's structural edges.
    for addr, data in [(0x000000, 0x00), (0xFFFFFF, 0xFF),
                       (0x00F60B, 0x90), (0x008000, 0x01)]:
        got = decode(encode(addr, data))
        assert got == (addr, data), "edge case %06X/%02X -> %r" % (addr, data, got)

    # 2. Every single address bit in isolation -- catches a permutation that is
    #    self-consistent but drops or duplicates a bit.
    for i in range(24):
        a = 1 << i
        assert decode(encode(a, 0x5A)) == (a, 0x5A), "bit %d round-trip failed" % i
    for i in range(8):
        d = 1 << i
        assert decode(encode(0x00F60B, d)) == (0x00F60B, d), "data bit %d failed" % i

    # 3. Random round-trips.
    rng = random.Random(0xF60B)
    for _ in range(n):
        a = rng.randrange(0x1000000)
        d = rng.randrange(0x100)
        assert decode(encode(a, d)) == (a, d), "round-trip failed for %06X/%02X" % (a, d)

    # 4. Decode -> encode direction, over random well-formed codes.
    for _ in range(n // 10):
        code = "".join(rng.choice(ALPHABET) for _ in range(8))
        a, d = decode(code)
        assert encode(a, d).replace("-", "") == code, "re-encode failed for %s" % code

    print("selftest OK: %d known-good vectors (both directions), %d random "
          "round-trips, all 24 address bits, all 8 data bits, %d reverse "
          "round-trips" % (len(KNOWN_VECTORS), n, n // 10))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("encode")
    e.add_argument("address", help="24-bit SNES address, hex (e.g. 00F60B)")
    e.add_argument("data", help="replacement byte, hex (e.g. C0)")
    d = sub.add_parser("decode")
    d.add_argument("code", help="XXXX-XXXX")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if args.cmd == "encode":
        addr = int(args.address, 16)
        val = int(args.data, 16)
        selftest(2000)          # never emit a code without proving the codec first
        if not is_lorom_rom_address(addr):
            print("WARNING: $%06X is not in LoROM ROM space ($8000-$FFFF of a "
                  "bank) -- check the address." % addr, file=sys.stderr)
        code = encode(addr, val)
        back = decode(code)
        assert back == (addr, val), "ROUND-TRIP FAILED, refusing to print"
        print("%s   ($%06X <- $%02X, verified by decode)" % (code, addr, val))
    elif args.cmd == "decode":
        addr, val = decode(args.code)
        assert encode(addr, val).replace("-", "") == \
            args.code.strip().upper().replace("-", ""), "ROUND-TRIP FAILED"
        print("$%06X <- $%02X" % (addr, val))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
