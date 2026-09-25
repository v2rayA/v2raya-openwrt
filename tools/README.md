# Current-source packages for OpenWrt 24.10

The legacy SDK recipe at `v2raya/Makefile` targets v2.2.7.4. Current
v2rayA has a separate `core/` Go module and requires its matching
`v2raya_core`, not an independently installed `xray-core` binary.

The legacy recipe's `core/iptables.TproxyNotSkipBr=true` linker flag still
controls LAN bridge interception in its pinned v2.2.7.4 sources. Keep it in
that recipe. The current-source pipeline does not pass that flag: use a
checkout containing [v2rayA #2057](https://github.com/v2rayA/v2rayA/pull/2057),
which includes OpenWrt LAN bridges through runtime defaults and migrates the
exact historical exclusion list. Custom interface exclusions remain intact.

This alternative source-build pipeline packages both binaries and the LuCI
sources from this checkout for `aarch64_cortex-a53`. It does not require
replacing the Go compiler inside the OpenWrt 24.10 SDK.

Requirements: Go 1.26 (or automatic Go toolchain selection), Node.js 24,
Yarn Classic, Python 3, Git and `shasum`.

```sh
./tools/build-current.sh /path/to/v2rayA 2.5.7-custom.1 r1 ./packages
```

The input checkout must include the desired changes. Both binaries receive
exactly the same version. `BUILD.txt` records source commits and dirty files;
release builds should use committed, reviewed sources. The output directory
must not exist, to prevent mixing packages from different builds.

The application depends on the matching `v2raya-core` package, CA certificates,
`kmod-nft-tproxy` and official geodata packages. LuCI depends on the application
and `luci-light`. `/etc/config/v2raya` is an opkg conffile; `/etc/v2raya/` is
preserved by sysupgrade via `/lib/upgrade/keep.d/v2raya`. A directory must not
be placed in the binary package's `conffiles` list: opkg cannot back it up as
a regular file during an upgrade.

The init script uses `/usr/share/v2ray`, where OpenWrt installs geodata,
avoiding an unnecessary download into a second directory on first startup.

For a local installation, copy all three IPKs to the router, update its
configured official feed indices and install the three files together.
Check `/api/version`: `coreVersionValid` must be true. Start the service,
open LuCI's Services / v2rayA page and test actual proxied traffic.

For publication, sign `Packages` using OpenWrt `usign`, distribute only the
public key through a trusted channel and configure an HTTPS opkg source.
Do not disable signature verification. The scripts generate an unsigned
index; they never generate or publish a private signing key.

These packages contain static userspace ARM64 programs, not kernel modules.
Kernel dependencies must come from the exact installed OpenWrt release's
feeds. VM validation on generic ARM64 does not validate a physical router's
wireless drivers, hardware offload or flash upgrade process.

## Application integration checks

For the automatic-group and subscription-timer changes in
[v2rayA #2055](https://github.com/v2rayA/v2rayA/pull/2055), run the application's
`tests/openwrt/automation.py` against a disposable OpenWrt 24.10.4 VM. It uses
synthetic VLESS subscriptions and an independent direct-traffic trap. Check
the entire catalog, all-dead blocking, recovery and actual minute retries;
one working first node is not a sufficient installation test.

After the VM suite passes, publish a signed index and test installation or
upgrade through LuCI Software with signature verification enabled and without
force-overwrite. Confirm the exact service/core pair, preserved accounts and
UCI settings, and the application UI. The application owns group membership
and subscription timers; this LuCI package configures the OpenWrt service.
