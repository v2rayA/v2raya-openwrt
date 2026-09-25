#!/usr/bin/env python3
"""Package static Linux ARM64 service/core binaries with this checkout's LuCI."""
import argparse
import gzip
import hashlib
import io
from pathlib import Path
import re
import tarfile


def archive(files):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        directories = set()
        for name in files:
            directories.update(str(p) for p in Path(name).parents if str(p) != ".")
        for name in sorted(directories, key=lambda s: (s.count("/"), s)):
            item = tarfile.TarInfo("./" + name)
            item.type, item.mode = tarfile.DIRTYPE, 0o755
            tar.addfile(item)
        for name, (data, mode) in sorted(files.items()):
            item = tarfile.TarInfo("./" + name)
            item.mode, item.size = mode, len(data)
            tar.addfile(item, io.BytesIO(data))
    return gzip.compress(buf.getvalue(), mtime=0)


def package(out, name, version, depends, files, conffiles=""):
    license_name = {
        "v2raya": "AGPL-3.0-only",
        "v2raya-core": "MPL-2.0",
        "luci-app-v2raya": "Apache-2.0",
    }[name]
    source = "v2raya-openwrt" if name == "luci-app-v2raya" else "v2rayA"
    control = (
        f"Package: {name}\nVersion: {version}\nArchitecture: aarch64_cortex-a53\n"
        f"License: {license_name}\nSource: https://github.com/v2rayA/{source}\n"
        "Maintainer: v2rayA contributors\nSection: net\nPriority: optional\n"
        f"Depends: {depends}\nInstalled-Size: {sum(len(v[0]) for v in files.values())}\n"
        "Description: Current v2rayA OpenWrt integration\n"
    )
    controls = {"control": (control.encode(), 0o644)}
    if conffiles:
        controls["conffiles"] = (conffiles.encode(), 0o644)
    blob = archive({
        "debian-binary": (b"2.0\n", 0o644),
        "control.tar.gz": (archive(controls), 0o644),
        "data.tar.gz": (archive(files), 0o644),
    })
    path = out / f"{name}_{version}_aarch64_cortex-a53.ipk"
    path.write_bytes(blob)
    return control + (
        f"Filename: {path.name}\nSize: {len(blob)}\n"
        f"SHA256sum: {hashlib.sha256(blob).hexdigest()}\n"
    )


def binary(path):
    data = path.read_bytes()
    if data[:6] != b"\x7fELF\x02\x01" or int.from_bytes(data[18:20], "little") != 183:
        raise ValueError("Expected little-endian Linux ARM64 ELF binary")
    return data, 0o755


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--luci-version", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for version in (args.version, args.luci_version):
        if not re.fullmatch(r"[A-Za-z0-9.+_-]+", version):
            parser.error("Invalid package version")
    root = Path(__file__).resolve().parents[1]
    core = {"usr/bin/v2raya_core": binary(args.core)}
    init = (root / "v2raya/files/v2raya.init").read_bytes()
    marker = b'append_env "config" "/etc/v2raya"'
    if init.count(marker) != 1:
        raise ValueError("Cannot locate the init script's configuration declaration")
    # Official geo packages use this directory; avoid another first-start download.
    init = init.replace(marker, marker + b'\n\tappend_env "v2ray_assetsdir" "/usr/share/v2ray"')
    app = {
        "usr/bin/v2raya": binary(args.service),
        "etc/init.d/v2raya": (init, 0o755),
        "etc/config/v2raya": ((root / "v2raya/files/v2raya.config").read_bytes(), 0o600),
        "lib/upgrade/keep.d/v2raya": (b"/etc/v2raya/\n", 0o644),
    }
    luci = {}
    for source, target in [("root", ""), ("htdocs", "www")]:
        base = root / "luci-app-v2raya" / source
        for file in base.rglob("*"):
            if file.is_file():
                luci[str(Path(target) / file.relative_to(base))] = (file.read_bytes(), 0o644)
    if not luci:
        raise ValueError("LuCI source files are missing")
    args.output.mkdir(parents=True, exist_ok=False)
    index = package(args.output, "v2raya-core", args.version, "libc", core)
    index += "\n" + package(
        args.output, "v2raya", args.version,
        f"libc, ca-bundle, kmod-nft-tproxy, v2raya-core (= {args.version}), v2ray-geoip, v2ray-geosite",
        app, "/etc/config/v2raya\n",
    )
    index += "\n" + package(
        args.output, "luci-app-v2raya", args.luci_version,
        f"luci-light, v2raya (= {args.version})", luci,
    )
    # LuCI commits an index entry at the blank paragraph separator.
    index += "\n"
    (args.output / "Packages").write_text(index)
    (args.output / "Packages.gz").write_bytes(gzip.compress(index.encode(), mtime=0))


if __name__ == "__main__":
    main()
