# SPDX-License-Identifier: GPL-3.0-only
#
# Copyright (C) 2021 ImmortalWrt.org

include $(TOPDIR)/rules.mk

PKG_NAME:=v2ray-core
PKG_VERSION:=4.45.0
PKG_RELEASE:=$(AUTORELEASE)

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/v2fly/v2ray-core/tar.gz/v$(PKG_VERSION)?
PKG_HASH:=fb8731295d8bbad9ef9157dbd3bc62655752d36544e0cc4077d4fa8a8a4ea295

PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Tianling Shen <cnsztl@immortalwrt.org>

PKG_BUILD_DEPENDS:=golang/host
PKG_BUILD_PARALLEL:=1
PKG_USE_MIPS16:=0

GO_PKG:=github.com/v2fly/v2ray-core/v4
GO_PKG_BUILD_PKG:=github.com/v2fly/v2ray-core/v4/main
GO_PKG_LDFLAGS_X:= \
	$(GO_PKG).build=OpenWrt \
	$(GO_PKG).version=$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk
include $(TOPDIR)/feeds/packages/lang/golang/golang-package.mk

GO_PKG_TARGET_VARS:=$(filter-out CGO_ENABLED=%,$(GO_PKG_TARGET_VARS)) CGO_ENABLED=0

define Package/v2ray/template
  TITLE:=A platform for building proxies to bypass network restrictions
  SECTION:=net
  CATEGORY:=Network
  URL:=https://www.v2fly.org
endef

define Package/v2ray-core
  $(call Package/v2ray/template)
  DEPENDS:=$(GO_ARCH_DEPENDS) +ca-bundle
endef

define Package/v2ray-ctl
  $(call Package/v2ray/template)
  DEPENDS:=v2ray-core
endef

define Package/v2ray-extra
  $(call Package/v2ray/template)
  TITLE+= (extra resources)
  DEPENDS:=v2ray-core
  PKGARCH:=all
endef

define Package/v2ray/description
  Project V is a set of network tools that help you to build your own computer network.
  It secures your network connections and thus protects your privacy.
endef

define Package/v2ray-core/description
  $(call Package/v2ray/description)
endef

define Package/v2ray-ctl/description
  $(call Package/v2ray/description)

  This includes configuration tool for v2ray-core.
endef

define Package/v2ray-extra/description
  $(call Package/v2ray/description)

  This includes extra resources for v2ray-core.
endef

define Build/Compile
	$(call GoPackage/Build/Compile)
	mv $(GO_PKG_BUILD_BIN_DIR)/main $(GO_PKG_BUILD_BIN_DIR)/v2ray

ifneq ($(CONFIG_PACKAGE_v2ray-ctl),)
	$(eval GO_PKG_BUILD_PKG:=$(GO_PKG)/infra/control/main)
	$(call GoPackage/Build/Compile)
	mv $(GO_PKG_BUILD_BIN_DIR)/main $(GO_PKG_BUILD_BIN_DIR)/v2ctl
endif
endef

define Package/v2ray-core/install
	$(call GoPackage/Package/Install/Bin,$(PKG_INSTALL_DIR))
	$(INSTALL_DIR) $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/v2ray $(1)/usr/bin/
endef

define Package/v2ray-ctl/install
	$(call GoPackage/Package/Install/Bin,$(PKG_INSTALL_DIR))

	$(INSTALL_DIR) $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/v2ctl $(1)/usr/bin/
endef

define Package/v2ray-extra/install
	$(INSTALL_DIR) $(1)/usr/share/v2ray/
	$(CP) $(PKG_BUILD_DIR)/release/extra/* $(1)/usr/share/v2ray/
endef

$(eval $(call BuildPackage,v2ray-core))
$(eval $(call BuildPackage,v2ray-ctl))
$(eval $(call BuildPackage,v2ray-extra))
