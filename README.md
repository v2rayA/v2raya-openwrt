# v2raya-openwrt

opkg feed of v2rayA for OpenWrt users.

[简体中文](README.zh-cn.md)

## How to install

1. Add v2rayA usign key

   > Make sure package `wget-ssl` is installed on your device

   ```sh
   wget https://osdn.net/projects/v2raya/storage/openwrt/v2raya.pub -O /etc/opkg/keys/94cc2a834fb0aa03
   ```

2. Import v2rayA feed

   ```sh
   echo "src/gz v2raya https://osdn.net/projects/v2raya/storage/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"

   # Japan mirror
   # echo "src/gz v2raya https://ftp.jaist.ac.jp/pub/sourceforge.jp/storage/g/v/v2/v2raya/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"
   # US mirror
   # echo "src/gz v2raya https://mirrors.gigenet.com/OSDN/storage/g/v/v2/v2raya/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"
   ```

3. Update feeds

   ```sh
   opkg update
   ```

4. Install v2rayA and its dependencies

   ```sh
   # To use v2rayA with Xray-core, please run:
   opkg install v2raya

   # To use v2rayA with v2ray-core, please run:
   opkg install v2raya2

   # Note: You cannot have both of them installed at the same time.
   #       Due to broken tproxy support in v2ray-core, recommend using Xray-core for now.

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
