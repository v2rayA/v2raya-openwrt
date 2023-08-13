# v2raya-openwrt

opkg feed of v2rayA for OpenWrt users.

[简体中文](README.zh-cn.md)

## How to install

1. Add v2rayA usign key

   > Make sure package `wget-ssl` or `libustream` is installed on your device

   ```sh
   wget https://downloads.sourceforge.net/v2raya/openwrt/v2raya.pub -O /etc/opkg/keys/94cc2a834fb0aa03
   ```

2. Import v2rayA feed

   ```sh
   echo "src/gz v2raya https://downloads.sourceforge.net/v2raya/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"
   ```

3. Update feeds

   ```sh
   opkg update
   ```

4. Install v2rayA and its dependencies

   ```sh
   opkg install v2raya

   # Check your firewall implementation
   # Install the following packages for the nftables-based firewall4 (command -v fw4)
   # Generally speaking, install them on OpenWrt 22.03 and later
   opkg install kmod-nft-tproxy
   # Install the following packages for the iptables-based firewall3 (command -v fw3)
   # Generally speaking, install them on OpenWrt 21.02 and earlier
   opkg install iptables-mod-conntrack-extra \
     iptables-mod-extra \
     iptables-mod-filter \
     iptables-mod-tproxy \
     kmod-ipt-nat6

   # Choose a core you'd like to use, v2ray or Xray
   # If you have both installed, the latter is preferred by default
   #
   # Note from maintainer: due to broken tproxy support in v2ray, recommend using Xray instead
   opkg install xray-core
   # opkg install v2ray-core

   # Optional
   # opkg install v2fly-geoip v2fly-geosite
   ```

## How to use

- Method 1 - Configure via LuCI interface (for __OpenWrt 21.02 and higher__ version only)

   1. Install LuCI app

      ```sh
      opkg install luci-app-v2raya
      ```

   2. Visit `http://<your_router_ip>/cgi-bin/luci/admin/services/v2raya` and complete setup.

- Method 2 - Configure via cli

   1. Setup v2rayA

      ```sh
      # For advanced usage, please see /etc/config/v2raya
      uci set v2raya.config.enabled='1'
      uci commit v2raya
      ```

   2. Start v2rayA

      ```sh
      /etc/init.d/v2raya start
      ```

   3. Visit v2rayA webUI and enjoy

      `http://<your_router_ip>:2017`
