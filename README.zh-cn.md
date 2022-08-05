# v2raya-openwrt

适用于 OpenWrt 用户的 opkg 软件源。

[English](README.md)

## 安装方法

1. 导入 v2rayA 签名文件

   > 请确认软件包 `wget-ssl` 已经安装在您的设备上

   ```sh
   wget https://osdn.net/projects/v2raya/storage/openwrt/v2raya.pub -O /etc/opkg/keys/94cc2a834fb0aa03
   ```

2. 添加 v2rayA 软件源

   ```sh
   echo "src/gz v2raya https://osdn.net/projects/v2raya/storage/openwrt/$(. /etc/openwrt_release && echo "$DISTRIB_ARCH")" | tee -a "/etc/opkg/customfeeds.conf"
   ```

3. 更新软件源

   ```sh
   opkg update
   ```

4. 安装 v2rayA 及其依赖

   ```sh
   opkg install v2raya

   # 选择一个你喜欢的内核，v2ray 或 Xray
   # 如果两个内核被同时安装，默认使用前者
   opkg install v2ray-core
   # opkg install xray-core

   # 可选
   # opkg install v2fly-geoip v2fly-geosite
   ```

## 使用方法

1. 配置 v2rayA

   ```sh
   # 详细配置请参见 /etc/config/v2raya
   uci set v2raya.config.enabled='1'
   uci commit v2raya
   ```

2. 启动 v2rayA

   ```sh
   /etc/init.d/v2raya start
   ```

3. 访问 v2rayA webUI 面板并完成设置

   http://openwrt.lan:2017
