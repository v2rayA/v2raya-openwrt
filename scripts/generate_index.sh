#!/bin/bash
# Copyright (C) 2021 Tianling Shen <cnsztl@immortalWrt.org>

set -o pipefail

TOPDIR="$PWD"
KEY_BUILD="$PWD/v2raya.sec"
echo -e "$USIGN_KEY" > "$KEY_BUILD"

pushd "$PWD/bin/packages/$BUILD_ARCH/v2raya_ci"

"$TOPDIR"/scripts/ipkg-make-index.sh . 2>&1 > "Packages.manifest"

grep -vE "^(Maintainer|LicenseFiles|Source|SourceName|Require|SourceDateEpoch)" "Packages.manifest" > "Packages"
case "$(((64 + "$(stat -L -c%s "Packages")") % 128))" in
	110|111)
		echo -e "\033[33mWARNING: Applying padding in Packages to workaround usign SHA-512 bug!\033[0m"
		{ echo ""; echo ""; } >> "Packages"
	;;
esac
gzip -9nc "Packages" > "Packages.gz"

signify-openbsd -S -s "$KEY_BUILD" -m "Packages"
rm -f "$KEY_BUILD"

popd
