# SPDX-License-Identifier: GPL-3.0-only
#
# Copyright (C) 2021 ImmortalWrt.org

include $(TOPDIR)/rules.mk

PKG_NAME:=v2fly-geodata
PKG_RELEASE:=$(AUTORELEASE)

PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Tianling Shen <cnsztl@immortalwrt.org>

include $(INCLUDE_DIR)/package.mk

GEOIP_VER:=202207140057
GEOIP_FILE:=geoip.dat.$(GEOIP_VER)
define Download/geoip
  URL:=https://github.com/v2fly/geoip/releases/download/$(GEOIP_VER)/
  URL_FILE:=geoip.dat
  FILE:=$(GEOIP_FILE)
  HASH:=1c786d10e3a1f84b6088b6d2692cefa7bd34c1b4508de07708f8ecb81ff3cc7c
endef

GEOSITE_VER:=20220717025946
GEOSITE_FILE:=dlc.dat.$(GEOSITE_VER)
define Download/geosite
  URL:=https://github.com/v2fly/domain-list-community/releases/download/$(GEOSITE_VER)/
  URL_FILE:=dlc.dat
  FILE:=$(GEOSITE_FILE)
  HASH:=f719c27f6fa0f4995702ec03a5642d6ee31a59e3d9a4fe825b6a77479a707f3e
endef

define Package/v2fly-geodata/template
  TITLE:=A list to be used for routing purpose in Project V
  SECTION:=net
  CATEGORY:=Network
  URL:=https://www.v2fly.org
  PKGARCH:=all
endef

define Package/v2fly-geoip
  $(call Package/v2fly-geodata/template)
  TITLE+= (geoip)
  VERSION:=$(GEOIP_VER)-$(PKG_RELEASE)
  LICENSE:=CC-BY-SA-4.0
endef

define Package/v2fly-geosite
  $(call Package/v2fly-geodata/template)
  TITLE+= (geosite)
  VERSION:=$(GEOSITE_VER)-$(PKG_RELEASE)
  LICENSE:=MIT
endef

define Build/Prepare
	$(call Build/Prepare/Default)
ifneq ($(CONFIG_PACKAGE_v2fly-geoip),)
	$(call Download,geoip)
endif
ifneq ($(CONFIG_PACKAGE_v2fly-geosite),)
	$(call Download,geosite)
endif
endef

define Build/Compile
endef

define Package/v2fly-geoip/install
	$(INSTALL_DIR) $(1)/usr/share/v2ray $(1)/usr/share/xray
	$(INSTALL_DATA) $(DL_DIR)/$(GEOIP_FILE) $(1)/usr/share/v2ray/geoip.dat
	$(LN) ../v2ray/geoip.dat $(1)/usr/share/xray/geoip.dat
endef

define Package/v2fly-geosite/install
	$(INSTALL_DIR) $(1)/usr/share/v2ray $(1)/usr/share/xray
	$(INSTALL_DATA) $(DL_DIR)/$(GEOSITE_FILE) $(1)/usr/share/v2ray/geosite.dat
	$(LN) ../v2ray/geosite.dat $(1)/usr/share/xray/geosite.dat
endef

$(eval $(call BuildPackage,v2fly-geoip))
$(eval $(call BuildPackage,v2fly-geosite))
