#!/bin/bash
echo Assembling...
for ver in J U SS E0 E1; do
	./asar -wno1009 -wno1018 --fix-checksum=off --symbols=nocash --define _VER="!__VER_$ver" smw.asm SMW_$ver.smc || exit
done
echo Assembly complete!

for ver in J U SS E0 E1; do
	[ -f comparison_$ver.smc ] || continue
	if cmp --silent comparison_$ver.smc SMW_$ver.smc; then
		echo "$ver version match!"
	else
		echo "$ver version MISMATCH!"
	fi
done
