# boot.py -- run on boot-up
import network, utime

# Replace the following with your WIFI Credentials
SSID = "TP-Link_70B0"
SSI_PASSWORD = "31460439"

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()

