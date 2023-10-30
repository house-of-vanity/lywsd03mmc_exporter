# Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) prom exporter 

```sh
docker run -d --name xiaomi_exporter \
  --restart=always --net=host --privileged \
  -t ultradesu/lywsd03mmc_exporter:latest \
  python3 /app/bt_exporter.py \
  --device 'A4:C1:38:54:AE:E0;guest_bedroom' \
  --device 'A4:C1:38:79:9D:20;bedroom' \
  --port 7536
```
