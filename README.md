# Xiaomi Mi Temperature and Humidity Monitor 2 prom exporter
### Also known as LYWSD03MMC

Bluetooth LE compatible adapter on Docker Host Machine should be configured and available.

```sh
# Check Bluetooth device
ab@home $ hciconfig
hci0:   Type: Primary  Bus: USB
        BD Address: F4:16:79:31:50:35  ACL MTU: 1021:4  SCO MTU: 96:6
        UP RUNNING 
        RX bytes:64175 acl:452 sco:0 events:5086 errors:0
        TX bytes:82225 acl:244 sco:0 commands:3200 errors:0

# Find your Xiaomi Mi devices
ab@home $ sudo hcitool lescan
LE Scan ...
A4:C1:38:54:AE:A0 LYWSD03MMC
A4:C1:38:3B:6C:A5 LYWSD03MMC
```



```sh
docker run -d --name xiaomi_exporter \
  --restart=always --net=host --privileged \
  -t ultradesu/lywsd03mmc_exporter:latest \
  python3 /app/bt_exporter.py \
  --device 'A4:C1:38:54:AE:A0;guest_bedroom' \
  --device 'A4:C1:38:3B:6C:A5;bedroom' \
  --port 7536
```
