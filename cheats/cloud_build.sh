#!/usr/bin/env bash
# cheats/cloud_build.sh: build the five ROMs in a cloud session.
#
# All of SMWDisX's code and data (graphics, levels, music) is in git, so
# this builds the real J, U, SS, E0 and E1 ROMs byte for byte, with no ROM
# dump. It checks each against the sha1 of the Mac's dumps (2026-11-10)
# and stops if one doesn't match.
#
# asar 1.91 is not in git (the Mac's ./asar is a macOS binary). If it is
# missing, this builds it from source into ./asar (ignored by git).
#
# Output: build/SMW_<ver>.smc (ignored by git), each with a 512-byte
# copier header like the dumps. cheats/tools/sgg.py reads them.
# It refuses to run where the real ROM (SMW_U.smc) is present.

set -eu -o pipefail
cd "$(dirname "$0")/.."

sha1_of() {
	case "$1" in
	J)  echo 75f8297e519a2f6b1fa4d61a99e411e6484cc5c9 ;;
	U)  echo 15b51da40ed5d1f868edfcb9a2b73784cfa0a326 ;;
	SS) echo 1e590d90cab0025028f6c6aadeba10c441301c80 ;;
	E0) echo de140424fc9b9ea93a4742bce3d277be05596015 ;;
	E1) echo adce808dd3b293ac537dc796b822a2812fcacd5d ;;
	esac
}

if [ -f SMW_U.smc ]
then
	echo "SMW_U.smc is here; this is the Mac. Use ./asar directly." >&2
	exit 1
fi

if ! { [ -x ./asar ] && ./asar --version 2>/dev/null | grep -q 'Asar 1.91'; }
then
	echo "Building asar 1.91 from source"
	if ! command -v cmake > /dev/null || ! command -v c++ > /dev/null
	then
		SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
		$SUDO apt-get update -qq > /dev/null
		$SUDO apt-get install -y -qq cmake g++ make > /dev/null
	fi
	rm -rf /tmp/asar-src /tmp/asar-build
	git clone -q --depth 1 --branch v1.91 https://github.com/RPGHacker/asar /tmp/asar-src
	cmake -S /tmp/asar-src/src -B /tmp/asar-build -DCMAKE_BUILD_TYPE=Release \
		-DASAR_GEN_LIB=OFF -DASAR_GEN_DLL=OFF \
		-DASAR_GEN_EXE_TEST=OFF -DASAR_GEN_DLL_TEST=OFF > /tmp/asar-cmake.log 2>&1 \
		|| { tail -20 /tmp/asar-cmake.log >&2; exit 1; }
	cmake --build /tmp/asar-build -j "$(nproc 2>/dev/null || echo 4)" > /tmp/asar-make.log 2>&1 \
		|| { tail -20 /tmp/asar-make.log >&2; exit 1; }
	bin=$(find /tmp/asar-build -type f -name asar -perm -u+x | head -1)
	[ -n "$bin" ] || { echo "asar binary not found after build" >&2; exit 1; }
	cp "$bin" ./asar
fi

mkdir -p build
for ver in J U SS E0 E1
do
	rm -f "build/SMW_$ver.smc"
	./asar -wno1009 -wno1018 --fix-checksum=off --define _VER="!__VER_$ver" \
		smw.asm "build/SMW_$ver.smc" > "build/asar_$ver.log" 2>&1 \
		|| { tail -20 "build/asar_$ver.log" >&2; exit 1; }
	got=$(sha1sum "build/SMW_$ver.smc" | cut -d' ' -f1)
	if [ "$got" != "$(sha1_of $ver)" ]
	then
		echo "build/SMW_$ver.smc sha1 is $got, not $(sha1_of $ver). Don't make codes from it." >&2
		exit 1
	fi
done
echo "Built build/SMW_{J,U,SS,E0,E1}.smc; each matches its dump's sha1."
