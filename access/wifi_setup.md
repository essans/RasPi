```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```


```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
        ssid="<ssid_name1>"
        psk="<password1>"
}

network={
        ssid="<ssid_name2>"
        psk="<password2>"
        key_mgmt=WPA-PSK
}

```
