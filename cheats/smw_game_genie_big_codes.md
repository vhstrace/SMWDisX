# Super Mario World — big Game Genie codes

Cheats here need far more codes than a real Game Genie can hold (it takes 5
at most). They write a small new routine into unused ROM, one byte per code.
Use them in an emulator that takes any number of codes, such as Mesen.

All codes are for the U release. SNES Game Genie codes have no compare byte.
All of the effects below are derived from the disassembly and **have not been
observed in play**.

## R swaps Mario with a sprite

**Recorded:** 2026-09-19 00:20:29

Three versions: swap X and Y, swap X only, or swap Y only. Use one version at
a time, because they write the same addresses. Each list is complete by
itself and includes the two hook codes.

### How it works

**Hook (2 codes, in all three lists).** The normal level loop calls
`JSL ProcessAllSprites` (`22 8C 80 01`) at `$00A2E2`, once per frame, just
before the sprites run. The first two codes point it at `$01FFBF`:
`00A2E3:BF` (orig `$8C`) and `00A2E4:FF` (orig `$80`). `$01FFBF`–`$01FFFF` is
the 65-byte `%insert_empty` pad at the end of bank 01, all `$FF` in the ROM
and never read. The new routine ends with `JMP $808C`, so the sprites still
run as normal, and `ProcessAllSprites` returns with its own `RTL`.

**Routine.** A and X are 8-bit here (`ProcessAllSprites` starts with
`LDX #$0B`), and A, X and Y are free.

```
    LDA $18          ; axlr0000Frame: buttons newly pressed this frame
    AND #$10         ; R
    BEQ done
    LDX #$0B         ; find the highest slot with a normal sprite
loop:
    LDA $14C8,X      ; SpriteStatus
    CMP #$08
    BEQ found
    DEX
    BPL loop
    BRA done         ; no normal sprite: do nothing
found:
; --- X swap (X-only and X+Y versions) ---
    LDA $94          ; PlayerXPosNext low
    LDY $E4,X        ; SpriteXPosLow
    STA $E4,X
    STY $94
    LDA $95          ; PlayerXPosNext high
    LDY $14E0,X      ; SpriteXPosHigh
    STA $14E0,X
    STY $95
; --- Y swap (Y-only and X+Y versions) ---
    LDY $96          ; old Mario Y low
    LDA $D8,X        ; SpriteYPosLow
    SEC
    SBC #$10         ; Mario Y = sprite Y - $10
    STA $96
    STY $D8,X        ; sprite Y = old Mario Y
    LDY $97          ; old Mario Y high
    LDA $14D4,X      ; SpriteYPosHigh
    SBC #$00
    STA $97
    TYA
    STA $14D4,X
done:
    JMP $808C        ; ProcessAllSprites
```

Why the `$10`: Mario's feet are `$20` below his Y position, and a normal
sprite's feet are `$10` below its Y position. Mario is moved `$10` higher than
the sprite's Y, so his feet land where the sprite's feet were. The sprite is
put at Mario's raw Y, which is `$10` above his feet, so it falls a short way.
The X swap needs no offset.

Bytes (the X+Y version, 65 bytes at `$01FFBF`), checked with asar and by
hand:

`A5 18 29 10 F0 38 A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 2A A5 94 B4 E4 95 E4 84 94 A5 95 BC E0 14 9D E0 14 84 95 A4 96 B5 D8 38 E9 10 85 96 94 D8 A4 97 BD D4 14 E9 00 85 97 98 9D D4 14 4C 8C 80`

X only (41 bytes): `A5 18 29 10 F0 20 A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 12 A5 94 B4 E4 95 E4 84 94 A5 95 BC E0 14 9D E0 14 84 95 4C 8C 80`

Y only (47 bytes): `A5 18 29 10 F0 26 A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 18 A4 96 B5 D8 38 E9 10 85 96 94 D8 A4 97 BD D4 14 E9 00 85 97 98 9D D4 14 4C 8C 80`

### Codes: swap X and Y (67 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 76EA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 4CE2-AD65 C9E2-ADA5 B0E2-AFD5
80E2-AF05 30E2-AF65 B9E2-AFA5 30E2-A4D5 60E2-A405 B0E2-A465 C9E2-A4A5 B9E2-A7D5
8AE2-A705 3DE2-A765 F0E2-A7A5 B2E3-ADD5 3DE3-AD05 F0E3-AD65 60E3-ADA5 B9E3-AFD5
C0E3-AF05 B1E3-AF65 89E3-AFA5 26E3-A4D5 76E3-A405 3BE3-A465 FDE3-A4A5 69E3-A7D5
B1E3-A705 B0E3-A765 26E3-A7A5 C0EE-ADD5 B5EE-AD05 82EE-AD65 20EE-ADA5 F0EE-AFD5
3BEE-AF05 DDEE-AF65 69EE-AFA5 B5EE-A4D5 B6EE-A405 B2EE-A465 20EE-A4A5 F0EE-A7D5
0AEE-A705 6AEE-A765 6DEE-A7A5
```

### Codes: swap X only (43 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 4DEA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 F4E2-AD65 C9E2-ADA5 B0E2-AFD5
80E2-AF05 30E2-AF65 B9E2-AFA5 30E2-A4D5 60E2-A405 B0E2-A465 C9E2-A4A5 B9E2-A7D5
8AE2-A705 3DE2-A765 F0E2-A7A5 B2E3-ADD5 3DE3-AD05 F0E3-AD65 60E3-ADA5 B9E3-AFD5
0AE3-AF05 6AE3-AF65 6DE3-AFA5
```

### Codes: swap Y only (49 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 41EA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 F6E2-AD65 C0E2-ADA5 B1E2-AFD5
89E2-AF05 26E2-AF65 76E2-AFA5 3BE2-A4D5 FDE2-A405 69E2-A465 B1E2-A4A5 B0E2-A7D5
26E2-A705 C0E2-A765 B5E2-A7A5 82E3-ADD5 20E3-AD05 F0E3-AD65 3BE3-ADA5 DDE3-AFD5
69E3-AF05 B5E3-AF65 B6E3-AFA5 B2E3-A4D5 20E3-A405 F0E3-A465 0AE3-A4A5 6AE3-A7D5
6DE3-A705
```

### Caveats

- The sprite is the one in the **highest slot** with status 8 (normal), not
  the nearest one. It may be off screen. Press R again to swap back with the
  same sprite, as long as the slots do not change.
- Carried, kicked and stunned items (status 9–B) are skipped. If there is no
  normal sprite, R does nothing.
- The hook is only in the normal level loop. Mode 7 boss rooms and the other
  `ProcessAllSprites` callers (`$00986C`, `$009947`, `$02A75F`) are not
  hooked, so R does nothing there.
- It runs once per press of R, not while R is held. R also keeps its normal
  job of scrolling the screen.
- Speeds are not swapped. Mario keeps his speed at the new place, and he can
  land inside a wall or the ground if the sprite was in a tight space.
- A sprite moved far off screen may be erased by the off-screen check the
  next time it runs.
- Not checked: Yoshi, while Mario rides him, and sprites that set their own
  position from something else every frame (platforms on lines, carried
  items). Those may snap back.
- Whether the level loop reaches this call while the game is paused has not
  been checked.
- All three versions are for the U release only.

## R destroys a sprite and teleports Mario to it

**Recorded:** 2026-09-19 22:26:11

The same idea as the R swap above, but one way: the sprite dies in a puff of
smoke and Mario takes its place. Three versions: move on both axes, on X only,
or on Y only.

These share the `$01FFBF` pad with the R swap, so use only one R-button cheat
at a time.

### How it works

**Hook (2 codes, in all three lists).** The same hook as the R swap:
`00A2E3:BF` and `00A2E4:FF` point the level loop's
`JSL ProcessAllSprites` at `$00A2E2` to the free pad at `$01FFBF`, and the new
routine ends with `JMP $808C` so the sprites still run.

**Routine.** The sprite search is the same. Mario's position is then copied
from the sprite, and the sprite is killed with the game's own spin-jump kill,
`CODE_019ACB` at `$019ACB`: it sets the sprite's status to `$04` (killed by
spin jump) and its `$1540` timer to `$1F`, which is the puff of smoke. `$08` in
`$1DF9` queues the spin-kill sound with it.

```
    LDA $18          ; axlr0000Frame: buttons newly pressed this frame
    AND #$10         ; R
    BEQ done
    LDX #$0B         ; find the highest slot with a normal sprite
loop:
    LDA $14C8,X      ; SpriteStatus
    CMP #$08
    BEQ found
    DEX
    BPL loop
    BRA done         ; no normal sprite: do nothing
found:
; --- X move (X-only and X+Y versions) ---
    LDA $E4,X        ; SpriteXPosLow
    STA $94          ; PlayerXPosNext low
    LDA $14E0,X      ; SpriteXPosHigh
    STA $95          ; PlayerXPosNext high
; --- Y move (Y-only and X+Y versions) ---
    LDA $D8,X        ; SpriteYPosLow
    SEC
    SBC #$10         ; Mario Y = sprite Y - $10
    STA $96          ; PlayerYPosNext low
    LDA $14D4,X      ; SpriteYPosHigh
    SBC #$00
    STA $97          ; PlayerYPosNext high
; --- kill (all three versions) ---
    LDA #$08         ; SFX_SPINKILL
    STA $1DF9        ; SPCIO0
    JSR $9ACB        ; status = 4, smoke timer = $1F
done:
    JMP $808C        ; ProcessAllSprites
```

The `$10` is the same foot-height correction as in the R swap: Mario is put
`$10` higher than the sprite's Y, so his feet land where its feet were.

Bytes (the X+Y version, 54 bytes at `$01FFBF`), checked with asar:

`A5 18 29 10 F0 2D A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 1F B5 E4 85 94 BD E0 14 85 95 B5 D8 38 E9 10 85 96 BD D4 14 E9 00 85 97 A9 08 8D F9 1D 20 CB 9A 4C 8C 80`

X only (40 bytes): `A5 18 29 10 F0 1F A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 11 B5 E4 85 94 BD E0 14 85 95 A9 08 8D F9 1D 20 CB 9A 4C 8C 80`

Y only (45 bytes): `A5 18 29 10 F0 24 A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 16 B5 D8 38 E9 10 85 96 BD D4 14 E9 00 85 97 A9 08 8D F9 1D 20 CB 9A 4C 8C 80`

### Codes: kill and move X and Y (56 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 42EA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 FEE2-AD65 89E2-ADA5 30E2-AFD5
69E2-AF05 B0E2-AF65 82E2-AFA5 3DE2-A4D5 F0E2-A405 69E2-A465 B9E2-A4A5 89E2-A7D5
26E2-A705 76E2-A765 3BE2-A7A5 FDE3-ADD5 69E3-AD05 B1E3-AD65 82E3-ADA5 20E3-AFD5
F0E3-AF05 3BE3-AF65 DDE3-AFA5 69E3-A4D5 B5E3-A405 CBE3-A465 D6E3-A4A5 62E3-A7D5
EBE3-A705 F2E3-A765 4DE3-A7A5 A8EE-ADD5 BCEE-AD05 0AEE-AD65 6AEE-ADA5 6DEE-AFD5
```

### Codes: kill and move X only (42 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 FEEA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 FFE2-AD65 89E2-ADA5 30E2-AFD5
69E2-AF05 B0E2-AF65 82E2-AFA5 3DE2-A4D5 F0E2-A405 69E2-A465 B9E2-A4A5 CBE2-A7D5
D6E2-A705 62E2-A765 EBE2-A7A5 F2E3-ADD5 4DE3-AD05 A8E3-AD65 BCE3-ADA5 0AE3-AFD5
6AE3-AF05 6DE3-AF65
```

### Codes: kill and move Y only (47 codes)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 40EA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 F1E2-AD65 89E2-ADA5 26E2-AFD5
76E2-AF05 3BE2-AF65 FDE2-AFA5 69E2-A4D5 B1E2-A405 82E2-A465 20E2-A4A5 F0E2-A7D5
3BE2-A705 DDE2-A765 69E2-A7A5 B5E3-ADD5 CBE3-AD05 D6E3-AD65 62E3-ADA5 EBE3-AFD5
F2E3-AF05 4DE3-AF65 A8E3-AFA5 BCE3-A4D5 0AE3-A405 6AE3-A465 6DE3-A4A5
```

### Caveats

The R swap's caveats about which sprite is picked, the hook, the once-per-press
timing and Mario's speed all apply here too. On top of those:

- The dead sprite's status is 4, not 8, so the next press of R finds the next
  one down. Press R over and over to clear the level's normal sprites one at
  a time, hopping to each in turn.
- The kill writes the status straight into the slot, so the sprite's own death
  code never runs. Nothing is dropped, no shell is left, and no points are
  scored. A Koopa vanishes whole instead of leaving its shell.
- Not checked: bosses and other sprites that run their own death code. Killing
  those with the plain smoke death may look wrong or leave the level stuck.
- All three versions are for the U release only.

## R moves Mario to a sprite's X position

**Recorded:** 2026-09-19 22:29:56

Press R and Mario is moved sideways to the highest-numbered normal sprite in
the level. His height does not change, and the sprite stays where it is.

This uses the `$01FFBF` pad, so use only one R-button cheat at a time.

### How it works

**Hook (2 codes).** The same hook as the other R-button cheats:
`00A2E3:BF` and `00A2E4:FF` point the level loop's `JSL ProcessAllSprites` at
`$00A2E2` to the free pad at `$01FFBF`, and the new routine ends with
`JMP $808C` so the sprites still run.

**Routine.** The sprite search is the same as the other R-button cheats. The
sprite's X position is then copied into Mario's.

```
    LDA $18          ; axlr0000Frame: buttons newly pressed this frame
    AND #$10         ; R
    BEQ done
    LDX #$0B         ; find the highest slot with a normal sprite
loop:
    LDA $14C8,X      ; SpriteStatus
    CMP #$08
    BEQ found
    DEX
    BPL loop
    BRA done         ; no normal sprite: do nothing
found:
    LDA $E4,X        ; SpriteXPosLow
    STA $94          ; PlayerXPosNext low
    LDA $14E0,X      ; SpriteXPosHigh
    STA $95          ; PlayerXPosNext high
done:
    JMP $808C        ; ProcessAllSprites
```

No height correction is needed, because only the X position is written.

Bytes (32 bytes at `$01FFBF`), checked with asar:

`A5 18 29 10 F0 17 A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 09 B5 E4 85 94 BD E0 14 85 95 4C 8C 80`

### Codes (34)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 F5EA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 DBE2-AD65 89E2-ADA5 30E2-AFD5
69E2-AF05 B0E2-AF65 82E2-AFA5 3DE2-A4D5 F0E2-A405 69E2-A465 B9E2-A4A5 0AE2-A7D5
6AE2-A705 6DE2-A765
```

### Caveats

The R swap's caveats about which sprite is picked, the hook, the once-per-press
timing and Mario's speed all apply here too. On top of those:

- The sprite keeps its slot and its status, so the same sprite is found again on
  the next press. R moves Mario to it once and then does nothing more, until the
  slots change or a higher slot fills.
- Mario lands at the sprite's left-right position but at his own height, so he
  can end up inside a wall or the ground.
- For the U release only.

## R moves Mario to a sprite's Y position

**Recorded:** 2026-09-19 22:30:02

Press R and Mario is moved up or down to the height of the highest-numbered
normal sprite in the level. His left-right position does not change, and the
sprite stays where it is.

This uses the `$01FFBF` pad, so use only one R-button cheat at a time.

### How it works

**Hook (2 codes).** The same hook as the other R-button cheats:
`00A2E3:BF` and `00A2E4:FF` point the level loop's `JSL ProcessAllSprites` at
`$00A2E2` to the free pad at `$01FFBF`, and the new routine ends with
`JMP $808C` so the sprites still run.

**Routine.** The sprite search is the same as the other R-button cheats. The
sprite's Y position is then copied into Mario's, less `$10`.

```
    LDA $18          ; axlr0000Frame: buttons newly pressed this frame
    AND #$10         ; R
    BEQ done
    LDX #$0B         ; find the highest slot with a normal sprite
loop:
    LDA $14C8,X      ; SpriteStatus
    CMP #$08
    BEQ found
    DEX
    BPL loop
    BRA done         ; no normal sprite: do nothing
found:
    LDA $D8,X        ; SpriteYPosLow
    SEC
    SBC #$10         ; Mario Y = sprite Y - $10
    STA $96          ; PlayerYPosNext low
    LDA $14D4,X      ; SpriteYPosHigh
    SBC #$00
    STA $97          ; PlayerYPosNext high
done:
    JMP $808C        ; ProcessAllSprites
```

The `$10` is the same foot-height correction as in the R swap: Mario's feet are
`$20` below his Y position and a normal sprite's feet are `$10` below its Y
position, so Mario is put `$10` higher than the sprite's Y and his feet land at
the height of its feet.

Bytes (37 bytes at `$01FFBF`), checked with asar:

`A5 18 29 10 F0 1C A2 0B BD C8 14 C9 08 F0 05 CA 10 F6 80 0E B5 D8 38 E9 10 85 96 BD D4 14 E9 00 85 97 4C 8C 80`

### Codes (39)

```
8EC3-6DAD EEC3-6FDD C9E8-A7A5 F6EA-ADD5 4BEA-AD05 FDEA-AD65 EDEA-ADA5 FAEA-AFD5
C4EA-AF05 D8EA-AF65 82EA-AFA5 A6EA-A4D5 F0EA-A405 ABEA-A465 D6EA-A4A5 EDEA-A7D5
D9EA-A705 ACEA-A765 FDEA-A7A5 E1E2-ADD5 6DE2-AD05 D3E2-AD65 89E2-ADA5 26E2-AFD5
76E2-AF05 3BE2-AF65 FDE2-AFA5 69E2-A4D5 B1E2-A405 82E2-A465 20E2-A4A5 F0E2-A7D5
3BE2-A705 DDE2-A765 69E2-A7A5 B5E3-ADD5 0AE3-AD05 6AE3-AD65 6DE3-ADA5
```

### Caveats

The R swap's caveats about which sprite is picked, the hook, the once-per-press
timing and Mario's speed all apply here too. On top of those:

- The sprite keeps its slot and its status, so the same sprite is found again on
  the next press. R moves Mario to it once and then does nothing more, until the
  slots change or a higher slot fills.
- Mario lands at the sprite's height but at his own left-right position, so he
  can end up inside a wall or the ground.
- For the U release only.

## Kicked shells touch every sprite

**Recorded:** 2026-09-19 00:41:51

**Codes (24):**

```
08C1-DD09 DDCC-D7D9 8DCC-D769 34CC-D7A9 BD38-6DD0 D338-6D00 8B38-6D60 A638-6DA0
F038-6FD0 AB38-6F00 DC38-6F60 ED38-6FA0 D538-64D0 8238-6400 A638-6460 F038-64A0
AB38-67D0 DC38-6700 2D38-6760 D738-67A0 0A3A-6DD0 8C3A-6D00 C03A-6D60 1D3A-6DA0
```

It does not overlap the R-button cheats above (those use
`$01FFBF`–`$01FFFF`), so it can be used together with any of them.

### How it works

`SubSprSprInteract` scans each lower slot X against the current sprite Y. A
pair only reaches `SprSprContact` (`$01A4BA`) if two range tests pass:
- X: the difference must be within `-$10..+$0F` (`BCS CODE_01A4B0` at
  `$01A460`),
- Y: the difference must be within `-$0C..+$0B` (`BCS CODE_01A4B0` at
  `$01A4AB`).

Both tests end with carry set when the pair is out of range. The first two
codes point both branches at the `JSR SprSprContact` at `$01A4AD`, not past it:
- `01A461:4B` (orig `$4E`),
- `01A4AC:00` (orig `$03`).

So every pair now reaches the `JSR`, and carry says whether they really touch.
The next two codes point that `JSR` at a stub in the 24-byte `%insert_empty`
pad at `$01E2B0`:
- `01A4AE:B0` (orig `$BA`),
- `01A4AF:E2` (orig `$A4`).

The remaining 20 codes write the stub:

```
    BCC j            ; in range: the normal contact code
    LDA $14C8,Y      ; SpriteStatus of the current sprite
    CMP #$0A         ; kicked?
    BEQ j
    LDA $14C8,X      ; SpriteStatus of the other sprite
    CMP #$0A         ; kicked?
    BNE r
j:  JMP $A4BA        ; SprSprContact
r:  RTS              ; out of range and neither is kicked: no contact
```

Bytes, checked with asar: `90 0E B9 C8 14 C9 0A F0 07 BD C8 14 C9 0A D0 03
4C BA A4 60`

`SprSprContact` then does what it does for a real touch. A kicked sprite
kills a normal one. It kills a carryable one on the ground, and if the
carryable one is in the air, both die. A kicked sprite and a kicked or
carried one both die. (See the table above `SprSprContact` in `bank_01.asm`.)

Registers are safe. At the X test, Y still holds the current slot and X the
other slot. At the Y test, X was just reloaded from `SpriteInterIndex`.
`SprSprContact` already has to keep X and Y for the scan to go on, and the
stub changes only A and flags.

### What it should look like

- Kick a shell, and every enemy loaded in the level dies within a frame or
  two, wherever it is, even off screen. Each kill adds to the shell's combo,
  so the points climb fast and reach 1-Ups.
- Any carried item or other kicked sprite dies with the shell.
- A thrown Goomba, Bob-omb or other kicked item (status `$0A`) does the same.

### Caveats

- The scan's other skip rules still apply: sprites that ignore other sprites
  (`SpriteTweakerE` bit 3), no-contact timers (`SpriteMisc1564`), sprites on
  Yoshi's tongue, and the fence-side test. Each slot still scans only every
  other frame.
- Only sprites with status 8 to B take part. Sprites being spawned or already
  dying are skipped.
- The exceptions in `SprSprContact` still apply. A flying `?` block is hit, not
  killed, and the shell bounces back from it. A blue shell-less Koopa facing
  the shell may catch it.
- If you ride Yoshi, he is a normal sprite (status 8). Whether his tweaker
  bits keep him out of the scan was not checked.
- Out-of-range pairs with no kicked sprite are skipped by the stub's `RTS`, as
  before. Pairs that really touch act as normal.

## Every extended sprite hits enemies like a fireball

**Recorded:** 2026-10-04 21:17:09

Tags: `video-ready`

**Codes (19):**

```
3ABF-ADDC 89BF-AD0C 8283-07DB D883-070B F583-076B AB83-07AB D48E-0DDB BD8E-0D0B
D58E-0D6B C98E-0DAB B28E-0FDB 2D8E-0F0B D78E-0F6B 4D8E-0FAB CA8E-04DB CD8E-040B
0A8E-046B F18E-04AB B88E-07DB
```

It uses the bank 02 pad at `$02B5EC`, so it does not overlap any cheat above.

### How it works

`ProcessExtSprites` (`$029B0A`) runs once a frame and calls
`JSR HandleExtSprite` for each of the 10 extended sprite slots, with the slot
in X. `HandleExtSprite` jumps through a table by `ExtSpriteNumber`: hammers,
bones, baseballs, Reznor and Piranha fireballs, Volcano Lotus fire, lava
splashes, spin-jump stars and so on.

Only two of those handlers, `MarioFireball` and `YoshiFireball`, call
`ProcessFireball`. That routine checks the slot against all 10 normal sprites
and, on contact, kills the sprite, turns it into a coin, or counts a hit on a
Chuck.

The first two codes point the `JSR HandleExtSprite` at `$029B0F` to a new
routine in the 68-byte `%insert_empty` pad at `$02B5EC`:
- `029B10:EC` (orig `$16`),
- `029B11:B5` (orig `$9B`).

The other 17 codes write the routine:

```
    LDA $170B,X      ; ExtSpriteNumber
    CMP #$02         ; skip empty slots (0) and smoke puffs (1)
    BCC j
    LDA $9D          ; SpriteLock
    BNE j
    JSR $A0AC        ; ProcessFireball
j:  JMP $9B16        ; HandleExtSprite, as before
```

Bytes, checked with asar: `BD 0B 17 C9 02 90 07 A5 9D D0 03 20 AC A0 4C 16
9B`

`ProcessFireball` uses X as the extended sprite slot, as `HandleExtSprite`
does, and puts X back before it returns. The routine changes only A, Y and
flags, and `HandleExtSprite` loads its own Y.

Smoke puffs are skipped because a fireball that hits an enemy becomes a puff
(`CODE_02A4E0`). Without the skip, that puff would go on killing for 15 more
frames, which a real fireball does not do.

### What it should look like

- A hammer, bone, baseball or enemy fireball that touches an enemy kills it
  (or turns it into a coin, as a fireball does) and becomes a puff of smoke.
- Spin-jump stars, lava splashes and the other small effects do the same.
- Mario's and Yoshi's fireballs work as before.

### Caveats

- **Enemies that throw things may kill themselves.** A projectile usually
  starts on top of the sprite that threw it. If that sprite can be killed by
  fire, it can die on its first throw (Hammer Brothers, Piranha Plants, Volcano
  Lotus and others).
- The fireball rules still apply: sprites immune to fire (`SpriteTweakerD`
  bit 1, `SpriteTweakerC` bit 4) are not hurt, and Chucks need 5 hits.
- Like a fireball, each slot is checked on 1 frame out of 4.
- A Yoshi fireball is checked twice on that frame, because `YoshiFireball`
  still calls `ProcessFireball` itself. A Yoshi fireball does not become a
  puff, so it adds 2 hits to a Chuck, not 1. A Mario fireball becomes a puff
  on the first check, so the second check does nothing.
- An extended sprite that runs into an enemy plays the bonk sound.
- Not tested in play. The effect comes from the disassembly.

## Mario throws Yoshi's fireballs

**Recorded:** 2026-10-04 21:35:06

**Codes (6):**

```
FFEA-6DD7 DDEA-6F07 26EB-6FD7 46EB-6F07 D5EC-6407 D9E8-6D07
```

This is one more code than a real Game Genie can hold. It writes no new
routine, so it uses no free ROM. It cannot be used together with these cheats
in `smw_game_genie.md`, because they patch the same bytes:
- "Fireball launch Y speed" (`00FEC5`),
- "Mario throws hammers instead of fireballs" (`00FEC0`),
- "Mario gets four fireballs at once" (`00FEB1`).

### How it works

`ShootFireball` (`$00FEA8`) finds a free extended sprite slot and fills it in.
`YoshiFireball` does not need Yoshi: it only moves the sprite, calls
`ProcessFireball` and draws it. So it is enough to make `ShootFireball` spawn
extended sprite `$11` with values that suit it.

| Code | Raw | Orig | Effect |
|---|---|---|---|
| `FFEA-6DD7` | `00FEC0:11` | `$05` | Spawn a Yoshi fireball (`$11`), not a Mario fireball (`$05`). |
| `DDEA-6F07` | `00FEC5:00` | `$30` | No Y speed. A Yoshi fireball has no gravity, so `$30` would send it down through the floor. |
| `26EB-6FD7` | `00FE94:D8` | `$FD` | X speed facing left (`DATA_00FE94`). |
| `46EB-6F07` | `00FE95:28` | `$03` | X speed facing right. |
| `D5EC-6407` | `00FEA9:07` | `$09` | The slot search starts at slot 7, not 9. |
| `D9E8-6D07` | `00FEB1:05` | `$07` | The slot search stops after slot 6, not 8. |

The X speeds are Yoshi's own (`CODE_01F295` uses `$28`). `YoshiFireball`
moves in 1/16 pixel units, while `MarioFireball` moves in whole pixels, so
the original `$FD`/`$03` would barely move.

The slot change is needed because `YoshiFireball` gets its OAM index from
`DATA_02A153`, which has 8 entries, one for each of slots 0-7. Mario's
fireballs use slots 8 and 9, which would read past the table into
`FireballTiles` and use those bytes as OAM indexes. Slots 7 and 6 have entries,
so `YoshiFireball` needs no change.

### What it should look like

- Mario's fireballs are Yoshi's big fireballs. They fly straight ahead, about
  2.5 pixels a frame, and do not bounce.
- They go through walls and the floor, and through enemies: one fireball can
  kill every enemy in its path. It is deleted when it leaves the screen.
- Mario can still have only 2 on the screen at once.

### Caveats

- Slots 6 and 7 are shared with other extended sprites (smoke, enemy
  projectiles and so on), so a fireball may be refused when the screen is
  busy, and Yoshi's own fireballs may find fewer free slots.
- Chucks still need 5 hits. A Yoshi fireball stays alive after a hit, so it
  can hit the same Chuck more than once as it passes through.
- Not tested in play. The effect comes from the disassembly.

## Mario spits Yoshi's fire spread

**Recorded:** 2026-10-04 21:59:49

**Codes (99):**

```
44EC-64D7 F3EC-6407 29EC-6467 D4EC-64A7 1DEC-67D7 C42F-076B D42F-07AB CD24-0DDB
D524-0D0B 8B24-0D6B D824-0DAB F524-0FDB ED24-0F0B D024-0F6B 6624-0FAB FD24-04DB
E624-040B 1824-046B CB24-04AB D124-07DB 6224-070B EA24-076B F224-07AB CB27-0DDB
DC27-0D0B 6227-0D6B BA27-0DAB F027-0FDB CB27-0F0B FF27-0F6B BB27-0FAB D827-04DB
F527-040B 8E27-046B 2A27-04AB E427-07DB DF27-070B BB27-076B 7227-07AB F520-0DDB
8E20-0D0B 2B20-0D6B E420-0DAB DF20-0FDB 2C20-0F0B C120-0F6B 5120-0FAB 2D20-04DB
D720-040B 0B20-046B FC20-07DB BB20-070B 0520-076B F520-07AB C929-0DDB B029-0D0B
F629-0D6B 5E29-0DAB B129-0FDB E329-0F0B DD29-0F6B BB29-0FAB FE29-04DB F529-040B
C929-046B B929-04AB 5E29-07DB BA29-070B E329-076B DD29-07AB BB21-0DDB 7721-0D0B
F521-0D6B EC21-0DAB C921-0FDB B121-0F0B F621-0F6B 1B21-0FAB D621-04DB BB21-040B
F921-046B F521-04AB C921-07DB B521-070B 1B21-076B DD21-07AB BB25-0DDB 4B25-0D0B
F525-0D6B C225-0DAB EB25-0FDB F725-0F0B BB25-0F6B 5B25-0FAB F525-04DB AC25-040B
FD25-046B C025-04AB 1825-07DB
```

It uses the bank 02 pad at `$02D51E`, so it does not overlap any cheat above.
It cannot be used with "Mario throws Yoshi's fireballs" or with any code in
`smw_game_genie.md` that patches `ShootFireball` (`$00FEA8`-`$00FEC5`),
because this one replaces that routine.

### How it works

This is a second version of "Mario throws Yoshi's fireballs". That one makes
`ShootFireball` spawn one Yoshi fireball (`$11`). This one spawns Yoshi's full
spread of 3, as `CODE_01F27C` does when Yoshi spits a red shell. It cannot
call `CODE_01F295`, the routine that spawns each of Yoshi's fireballs, because
that routine takes the position and facing from Yoshi's sprite slot in X.
So it is written again for Mario.

The first 5 codes replace the start of `ShootFireball` (`$00FEA8`) with
`JSL $02D51E` / `RTS` (orig `A2 09 BD 0B 17`). The other 94 codes write the
new routine into the 98-byte `%insert_empty` pad at `$02D51E`:

```
    LDX #$02                  ; speed index 2..0, as in CODE_01F295
next:
    LDY #$07                  ; free slot 7..0, as in CODE_018EEF
find:
    LDA ExtSpriteNumber,Y
    BEQ found
    DEY
    BPL find
    RTL                       ; no free slot: stop
found:
    LDA #!SFX_FIREBALL        ; same sound and throw pose as ShootFireball
    STA SPCIO3
    LDA #$0A
    STA ShootFireTimer
    LDA #$11                  ; Yoshi fireball
    STA ExtSpriteNumber,Y
    LDA.L DATA_01F2DC,X       ; Yoshi's Y speeds: 00, F8, 08
    STA ExtSpriteYSpeed,Y
    LDA.L DATA_01F2D9,X       ; Yoshi's X speeds: 28, 24, 24
    PHX
    LDX PlayerDirection
    BNE +
    EOR #$FF                  ; facing left: negate
    INC A
  + STA ExtSpriteXSpeed,Y
    LDA PlayerXPosNext        ; X position: ShootFireball's own offsets
    CLC
    ADC.L DATA_00FE96,X
    STA ExtSpriteXPosLow,Y
    LDA PlayerXPosNext+1
    ADC.L DATA_00FE9C,X
    STA ExtSpriteXPosHigh,Y
    PLX
    LDA PlayerYPosNext        ; Y position: Mario + 8, as on foot
    CLC
    ADC #$08
    STA ExtSpriteYPosLow,Y
    LDA PlayerYPosNext+1
    ADC #$00
    STA ExtSpriteYPosHigh,Y
    LDA PlayerBehindNet
    STA ExtSpritePriority,Y
    DEX
    BPL next
    RTL
```

It was assembled by asar against the disassembly's own labels. The pad was
all `$FF`, so the `$FF` operand of `EOR #$FF` at `$02D54B` needs no code. The
65816 has no long,Y addressing mode, so X holds the table index and Y the
slot, the opposite of `ShootFireball`. Both callers of `ShootFireball` return
right after the `JSR`, so the new X and Y values do not matter.

### What it should look like

- Each throw sends 3 big Yoshi fireballs ahead of Mario: one straight, one
  angled up, one angled down. They pass through enemies and walls and kill
  what they touch.
- The spin-jump fireballs that fire Mario throws come out as spreads too.

### Caveats

- There is no limit of 2 fireballs any more. A throw only needs one free slot
  in 7..0. If fewer than 3 slots are free, it throws fewer fireballs.
- Slots 0-7 are shared with other extended sprites, so a few fast throws can
  leave no slots for enemy projectiles or Yoshi's own fire.
- `ExtSpriteMisc176F` is not set (Yoshi sets it to `$A0`). Neither
  `YoshiFireball` nor `ProcessFireball` reads it.
- Not tested in play. The effect comes from the disassembly.

## Every level is populated with the next level's enemies, with their graphics

**Recorded:** 2026-11-01 00:26:48

**Codes (32):**

```
C260-0FB9 6964-6DF5 1C64-6D95 A464-6DB5 4D64-6D25 8B64-6FF5 D064-6F95 3D64-6FB5
6964-6F25 D964-64F5 8B64-6495 D764-64B5 3D64-6425 FC64-67F5 FC64-6795 6964-67B5
D064-6725 C567-6DF5 D067-6D95 4B67-6DB5 DE67-6D25 DD67-6FF5 6267-6F95 4867-6FB5
FB67-6F25 1D67-64F5 4D22-D7B1 4D22-D721 6323-DDF1 3C23-DD91 D423-D7F1 D72E-DD91
```

The list includes the two codes of "Every level is populated with the next
level's enemies" in `smw_game_genie.md` (the last two, `D423-D7F1` and
`D72E-DD91`), so don't add those again.

It uses the bank 05 pad at `$058E19`. No other cheat here or in
`smw_game_genie.md` writes `$058546`, `$058E20`-`$058E38` or
`$05D8DE`-`$05D8E1`. "Every level gets the next level's background" in
`smw_game_genie.md` patches the operands just before (`$05D8D2`-`$05D8DC`), so
the two can be used together.

The first version (57 codes) is in this file's git history. It hooked
`LDA.W #$0000` at `$05D8E6` instead, where Y holds the level number × 2, so it
had to compute × 3 itself.

### How it works

The two-code cheat moves each level's sprite list to the next level's list
(level *n* gets the sprites of level *n+1*). But the sprite graphics are not
part of the sprite list. They come from the low nibble of byte 3 of the
Layer 1 level header, which `CODE_0584E3` stores in `SpriteTileset`:

```
    INY                                       ; \Get third byte
    LDA.B [Layer1DataPtr],Y                   ; /
    STA.B _0                                  ; "Push" third byte
    TAX                                       ; "Push" third byte
    AND.B #$0F                                ; \Load sprite set
    STA.W SpriteTileset                       ; /
```

So the enemies of level *n+1* are drawn with the graphics files of level *n*.
This cheat also gives level *n* the sprite graphics list of level *n+1*.
It does not change the Layer 1 pointer, so the terrain stays level *n*'s.

`CODE_05D796` (the primary header loader, `JSL`'d from `GM11LoadLevel`) runs
first. `CODE_0584E3` runs later, from `CODE_05801E` → `LoadLevel`, and by then
the level number in `_E` can be gone (for a background level, `CODE_05801E`
writes `_D`/`_E`). So the new value is written in `CODE_05D796`, and
`CODE_0584E3` must not write over it.

**Hook 1 (4 codes).** In `CODE_05D8B7`, just after the Layer 1 and Layer 2
pointers are read, `STA.B Layer2DataPtr+2` / `REP #$20` (`85 6A C2 20`) at
`$05D8DE` becomes `JSR $8E20` / `NOP`. Y still holds the level number × 3
there (the index into `Layer1Ptrs`), so `Layer1Ptrs+3,Y` is the pointer of
level *n+1*. X and Y are 16-bit, and the data bank is `$05` (`CODE_05D796`
does `PHK`/`PLB`). The routine reads header byte 3 of level *n+1* and stores
its low nibble in `SpriteTileset`:

```
NextTileset:                  ; $058E20
    STA.b Layer2DataPtr+2     ; the two replaced instructions
    REP #$20
    LDA.w Layer1Ptrs+4,Y      ; level n+1: pointer bytes 1-2 to _5/_6
    STA.b _5
    LDA.w Layer1Ptrs+3,Y      ; pointer bytes 0-1, plus 2, to _4/_5
    INC A
    INC A
    STA.b _4
    LDA [_4]                  ; header bytes 3 and 4 of level n+1
    AND.w #$000F              ; sprite graphics list
    STA.w SpriteTileset
    RTS
```

Adding 2 to the pointer instead of using `[_4],Y` keeps Y as the caller left
it. It would read the wrong bank if a pointer's low 16 bits were `$FFFE` or
`$FFFF`, but none of the 512 `Layer1Ptrs` entries is (they are all in banks
`$06` and `$07`). The mask is needed, because the high bits of header byte 3
hold the music and the Layer 3 priority. Because A is 16-bit, the store also
writes 0 to `$192C`, the byte after `SpriteTileset`. It is unused
(`rammap.asm`), and nothing in the disassembly reads it. The routine returns
with A 16-bit. That is what the replaced `REP #$20` left, and the next
instruction (`LDA.B _E`) reloads A. `_4`-`_6` are not used anywhere in
`CODE_05D796`.

**Hook 2 (1 code).** `STA.W SpriteTileset` at `$058546` in `CODE_0584E3`
becomes `LDA.W SpriteTileset` (`$8D` → `$AD`), so `CODE_0584E3` no longer
writes `SpriteTileset` at all. The next instruction (`TXA`) reloads A.

This breaks the one other caller of `CODE_05801E`: the enemy credits
(`GM23PrepEnemyList`). They load each scene with their own Layer 1 pointers
and don't run `CODE_05D796`, so they need `CODE_0584E3` to set the graphics.
`Clear_1A_13D3` leaves `SpriteTileset` at 0 (the forest list), and only
scenes 10 and 12 set their own.

The pad was all `$FF`, and the routine has no `$FF` bytes, so every byte
needs a code. The list was assembled by asar, and ggpatch with the list gives
the same bytes as asar.

### What it should look like

- The enemies of the next level should look right, not like garbage tiles,
  as long as the next level's sprites use the normal per-level graphics
  files (SP3/SP4).
- Terrain, background, music, timer and palettes stay this level's.

### Caveats

- The user tested the 57-code first version and the 32-code list, and they
  worked.
- Shorter versions (29, 19, 18 and 8 codes) are in this file's git history.
  The 19-, 18- and 8-code versions saved the next level's header pointer in
  `$60`-`$63` and redirected the byte 3 read in `CODE_0584E3` through it. The
  user tested all three, and none of them fixed the graphics. The cause wasn't
  found. The 29-code version was never tested.
- Most scenes of the enemy credits at the end of the game show the wrong
  tiles (see above).
- The sprite *palette* is still this level's own. It is in header byte 4
  bits 3-5 (`SpritePalette`), which this cheat does not move. So enemies can
  have the wrong colors even when their tiles are right.
- Boss rooms and other special rooms that set `SpriteTileset` themselves
  after the load (Mode 7 boss rooms, the castle cutscenes) keep their own
  graphics.
- Level entrances that show the "Mario enters the castle" intro
  (`CODE_05DA38`) use a fixed sprite list at `$07C3EE` instead of the moved
  one. They also get the next level's graphics list, which doesn't matter,
  because that list is empty (`00 FF` in the ROM).
- As in the two-code cheat, the highest level index reads past the end of
  `Layer1Ptrs` and `Ptrs05EC00`, so its sprites and graphics come from
  garbage. The value is masked to `$0F`, so it is still a valid graphics
  list.
- Revisions: U only. Others not checked.
