# SPDX-License-Identifier: GPL-3.0-only
#
# Copyright (C) 2022 ImmortalWrt.org

include $(TOPDIR)/rules.mk

LUCI_TITLE:=LuCI support for v2rayA
LUCI_DEPENDS:=+v2raya
LUCI_PKGARCH:=all

PKG_VERSION:=10
PKG_PO_VERSION:=$(PKG_VERSION)

include $(TOPDIR)/feeds/luci/luci.mk

# call BuildPackage - OpenWrt buildroot signature
