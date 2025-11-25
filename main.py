import network
import time
import machine
from machine import Pin
import ubinascii
from umqtt.simple import MQTTClient

# Config WiFi
SSID = "Wokwi-GUEST"
PASSWORD = ""

# Config MQTT
MQTT_BROKER = "broker.emqx.io"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"sala/status"

# Pinos
pir = Pin(14, Pin.IN)
led_luz = Pin(12, Pin.OUT)
led_ar = Pin(13, Pin.OUT)

# Conecta ao Wi-Fi
def conecta_wifi():
    print("Conectando ao Wi-Fi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        time.sleep(0.5)
    print("Conectado:", sta_if.ifconfig())

# Envia mensagem MQTT
def envia_mensagem(mensagem):
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883)
        client.connect()
        client.publish(TOPIC, mensagem)
        client.disconnect()
        print("Mensagem enviada:", mensagem)
    except Exception as e:
        print("Erro ao enviar MQTT:", e)

# Programa principal
conecta_wifi()

tempo_sem_movimento_luz = 0
tempo_limite_luz = 10
tempo_sem_movimento_ar = 0
tempo_limite_ar = 20

led_luz.value(1)
led_ar.value(1)
print("Luzes e ar ligados.")

while True:
    if pir.value() == 1:
        tempo_sem_movimento_luz = 0
        tempo_sem_movimento_ar = 0
        if led_luz.value() == 0:
            led_luz.value(1)
        if led_ar.value() == 0:
            led_ar.value(1)
        print("Movimento detectado.")
    else:
        tempo_sem_movimento_luz += 1
        tempo_sem_movimento_ar += 1
        print("Sem movimento:", tempo_sem_movimento_luz, tempo_sem_movimento_ar)

        if tempo_sem_movimento_luz >= tempo_limite_luz and led_luz.value() == 1:
            led_luz.value(0)
            print("Luz desligada.")
            envia_mensagem("Luz desligada.")

        if tempo_sem_movimento_ar >= tempo_limite_ar and led_ar.value() == 1:
            led_ar.value(0)
            print("Ar desligado.")
            envia_mensagem("Ar desligado.")

    time.sleep(1)
