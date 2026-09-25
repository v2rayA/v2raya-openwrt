#!/usr/bin/env bash
# Build service, matching core and LuCI packages for OpenWrt 24.10 ARM64.
set -euo pipefail
if [[ $# != 4 ]]; then
  echo "Usage: $0 V2RAYA_CHECKOUT VERSION PACKAGE_RELEASE OUTPUT_DIRECTORY" >&2
  exit 2
fi
source_dir=$(cd "$1" && pwd)
version=$2
release=$3
output=$4
script_dir=$(cd "$(dirname "$0")" && pwd)
[[ "$version" =~ ^[A-Za-z0-9.+_-]+$ ]] || exit 2
[[ "$release" =~ ^[A-Za-z0-9.+_-]+$ ]] || exit 2
[[ ! -e "$output" ]] || { echo "Output already exists: $output" >&2; exit 2; }
node -e 'if (Number(process.versions.node.split(".")[0]) < 24) process.exit(1)'
# build.sh embeds the GUI and stamps both binaries with the same version.
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 bash "$source_dir/build.sh" "$version"
python3 "$script_dir/package-current.py" \
  --service "$source_dir/v2raya" --core "$source_dir/v2raya_core" \
  --version "$version-$release" --luci-version "26.268.0-$release" --output "$output"
{
  printf 'v2rayA source: %s\n' "$(git -C "$source_dir" rev-parse HEAD)"
  printf 'OpenWrt integration source: %s\n' "$(git -C "$script_dir" rev-parse HEAD)"
  printf 'Version: %s\n' "$version"
  printf 'Go: %s\n' "$(cd "$source_dir/service" && go version)"
  printf 'Node: %s\n' "$(node --version)"
  git -C "$source_dir" status --short
} > "$output/BUILD.txt"
(cd "$output" && shasum -a 256 ./*.ipk Packages Packages.gz > SHA256SUMS)
