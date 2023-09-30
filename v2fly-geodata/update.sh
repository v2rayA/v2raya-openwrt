#!/bin/bash

set -x

export CURDIR="$(cd "$(dirname $0)"; pwd)"

function update_geodata() {
	local type="$1"
	local repo="$2"
	local res="$3"
	local tag ver sha line

	tag="$(curl -H "Authorization: $GITHUB_TOKEN" -sL "https://api.github.com/repos/$repo/releases/latest" | jq -r ".tag_name")"
	[ -n "$tag" ] || return 1

	ver="$(awk -F "${type}_VER:=" '{print $2}' "$CURDIR/Makefile" | xargs)"
	[ "$tag" != "$ver" ] || return 2

	sha="$(curl -fsSL "https://github.com/$repo/releases/download/$tag/$res.dat.sha256sum" | awk '{print $1}')"
	[ -n "$sha" ] || return 1

	line="$(awk "/FILE:=\\$\(${type}_FILE\)/ {print NR}" "$CURDIR/Makefile")"
	sed -i -e "s/${type}_VER:=.*/${type}_VER:=$tag/" \
	       -e "$((line + 1))s/HASH:=.*/HASH:=$sha/" \
		"$CURDIR/Makefile"
}

update_geodata "GEOIP" "v2fly/geoip" "geoip"
update_geodata "GEOSITE" "v2fly/domain-list-community" "dlc"
