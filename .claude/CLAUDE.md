# Cloud sessions (Claude Code on the web and mobile)

This part applies only when `SMW_U.smc` is missing, which is the case in
a cloud session. On the Mac, ignore it and follow `AGENTS.md`.

Cloud sessions make **Game Genie codes**. Don't change the disassembly
(code, comments, labels). Its style rules are in the Mac's `AGENTS.md`,
which is not in git, so leave comment work to the Mac.

Work on the `cheat-hunt` branch. The Game Genie entries are in `cheats/`:

- `cheats/smw_game_genie.md`: most cheats.
- `cheats/smw_game_genie_big_codes.md`: cheats that write a new routine
  into unused ROM, with far more codes than a Game Genie holds.

The Mac copies them back into its own `game_genie/` folder later, and
builds ROMs, syncs Mesen2, Batocera and MinUI there. None of those exist
here, so don't try them, and don't write to `~/Downloads`.

## The ROMs

The dumps are not in git, but the whole game is: a SessionStart hook runs
`cheats/cloud_build.sh`, which builds `build/SMW_J.smc`, `SMW_U.smc`,
`SMW_SS.smc`, `SMW_E0.smc` and `SMW_E1.smc` and checks each against the
sha1 of the real dump. These are the real bytes, not placeholders. If
`build/SMW_U.smc` is missing, run `cheats/cloud_build.sh` yourself. If
it fails, stop and tell the user. Never commit a ROM.

Addresses are in `SMW_U.sym` (in git) and in the labels of the `.asm`
files. The target is the U version.

## Making a code

1. Find the code to change in the `bank_*.asm` files. Don't change them.
   Version-specific code is in `if ver_is_english(!_VER)` (and
   `ver_is_japanese`, `ver_is_lores` and so on) blocks; the banner on the
   `if` line lists the versions. Read the parts U builds.
2. Encode it with the wrapper. It reads the original byte from the U ROM
   and shows the byte in the other versions:

       python3 -I cheats/tools/sgg.py 0585BF:04 05BD36:AD

   Each argument is `SNESADDR:NEW` in hex (SMW is LoROM, so the address
   is a `$xx8000`-`$xxFFFF` bus address). It prints the codes and the
   **Codes:** and **Raw form:** lines. Check each original byte against
   the instruction you meant to change.
3. SNES codes have no compare byte, so there is no other-bank check. But
   if the wrapper says the byte pattern appears more than once, a copy of
   the same routine may exist elsewhere; say in the entry whether it
   needs a code too.
4. Write the entry at the bottom of the right file in `cheats/`.

## Entry format

Copy the newest entries in `cheats/smw_game_genie.md`. The shape is:

```
## Short title that says what the player sees

**Codes:** `AAAA-AAAA` + `BBBB-BBBB` (use both)
**Raw form:** `0585BF:04` (orig `$03`); `05BD36:AD` (orig `$9C`)
(address:new-byte — the original byte is documentation, not part of the code;
SNES Game Genie has no compare byte)
**Recorded:** YYYY-MM-DD HH:MM:SS

**Mechanism:** what the original code does (quote it, with labels and
the source file), and what the patched code does.

**Where you see it:** (optional) levels or places where the effect shows.

**Evidence:** bytes read from `build/SMW_U.smc` (made by
`cheats/cloud_build.sh`, the same sha1 as the real dump), and labels.

**Revisions:** which versions have the same bytes, from the wrapper's
"other versions" line.

**Caveats:**

- Not tested.
- Side effects, limits, and things that still work as before.
```

- Newest entry last, in **Recorded:** order. Use simple technical
  English in entries.
- No `Tags:` line unless the user asks for tags. Add or remove tags only
  when asked.
- A real SNES Game Genie holds 5 codes. Cheats that need far more,
  usually because they write a new routine into unused ROM (see
  `freespace.txt`), go in `cheats/smw_game_genie_big_codes.md`. Read its
  header first.
- Optional extra codes go on their own line, such as
  `**Optional, for Donut Plains 2:** ...`. List every code the option
  needs on that line, and no other codes.
- When porting a cheat from another game, say which one in the Mechanism.
  Other games' cheat files are not in this repo; the user can paste one.

## Commits

Commit each change on `cheat-hunt` and push it. Commit only files in
`cheats/`. A git pre-commit hook (`cheats/githooks/pre-commit`, turned on
by the SessionStart hook) refuses any other file and any ROM. Messages:
`Add: <title>` for a new entry, `Remove: <title>` for a deleted one,
otherwise a short plain sentence. No attribution lines.
