# v2raya-openwrt

opkg feed of v2rayA for OpenWrt users.

## How to install

1. Add v2rayA usign key

   ```sh
   wget-ssl https://mirrors.tuna.tsinghua.edu.cn/osdn/storage/g/v/v2/v2raya/openwrt/v2raya.pub -O /etc/opkg/keys/94cc2a834fb0aa03
   ```

2. Import v2rayA feed

   ```sh
   echo "src/gz v2raya https://mirrors.tuna.tsinghua.edu.cn/osdn/storage/g/v/v2/v2raya/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"
   ```

3. Update feeds

   ```sh
   opkg update
   ```

4. Install v2rayA and its dependencies

   ```sh
   opkg install v2raya

   # Choose a core you'd like to use, v2ray or Xray
   # If you have both installed, the former is preferred by default
   opkg install v2ray-core
   # opkg install xray-core

   # Optional
   # opkg install v2fly-geoip v2fly-geosite
   ```

## How to use

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

   http://openwrt.lan:2017
