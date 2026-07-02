import board
import digitalio
import adafruit_matrixkeypad
import time

# Zumbador en GP20
buzzer = digitalio.DigitalInOut(board.GP15)
buzzer.direction = digitalio.Direction.OUTPUT
buzzer.value = True   # Reposo = apagado

def beep(duration=0.1):
    buzzer.value = False   # Enciende el buzzer
    time.sleep(duration)
    buzzer.value = True    # Lo apaga nuevamente

def beep_success():
    for _ in range(3):
        beep(0.1)
        time.sleep(0.05)

def beep_error():
    for _ in range(2):
        beep(0.3)
        time.sleep(0.1)

# LEDs
led_pins = [board.GP0, board.GP1, board.GP16, board.GP17,
            board.GP18, board.GP19, board.GP20, board.GP21]
leds = []
for p in led_pins:
    led = digitalio.DigitalInOut(p)
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    leds.append(led)

def leds_off():
    for led in leds:
        led.value = True

def leds_ingreso(n):
    leds_off()
    for i in range(min(n * 2, 8)):
        leds[i].value = False

def leds_success():
    for _ in range(3):
        for led in leds:
            led.value = False
        time.sleep(0.2)
        leds_off()
        time.sleep(0.1)

def leds_error():
    for _ in range(3):
        for i in range(0, 8, 2):
            leds[i].value = False
        time.sleep(0.2)
        leds_off()
        time.sleep(0.1)

# Teclado
keys = (
    ('K1',  'K5',  'K9',  'K13'),
    ('K2',  'K6',  'K10', 'K14'),
    ('K3',  'K7',  'K11', 'K15'),
    ('K4',  'K8',  'K12', 'K16'),
)
cols = [digitalio.DigitalInOut(p) for p in (board.GP2, board.GP3, board.GP4, board.GP5)]
rows = [digitalio.DigitalInOut(p) for p in (board.GP6, board.GP7, board.GP8, board.GP9)]

s1 = digitalio.DigitalInOut(board.GP10)
s2 = digitalio.DigitalInOut(board.GP11)
s3 = digitalio.DigitalInOut(board.GP12)
s4 = digitalio.DigitalInOut(board.GP13)
for s in [s1, s2, s3, s4]:
    s.direction = digitalio.Direction.INPUT
    s.pull = digitalio.Pull.UP

teclado = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

MAPA = {
    'K1':'1','K2':'2','K3':'3','K4':'A',
    'K5':'4','K6':'5','K7':'6','K8':'B',
    'K9':'7','K10':'8','K11':'9','K12':'C',
    'K13':'#','K14':'0','K15':'*','K16':'D'
}

SECRET = ['K2', 'K14', 'K14', 'K7']
entrada = []
ultima = None
ultima_s = None

print("Cerrojo listo.")

while True:
    pressed = teclado.pressed_keys

    if pressed:
        tecla = pressed[0]
        if tecla != ultima:
            ultima = tecla
            entrada.append(tecla)
            print(MAPA.get(tecla, tecla))
            beep(0.05)
            leds_ingreso(len(entrada))
    else:
        ultima = None

    if not s1.value:
        if ultima_s != 's1':
            ultima_s = 's1'
            if entrada == SECRET:
                print("ACCESO CONCEDIDO")
                beep_success()
            else:
                print("ACCESO DENEGADO")
                beep_error()
            entrada = []
            leds_off()

    elif not s2.value:
        if ultima_s != 's2':
            ultima_s = 's2'
            if entrada:
                entrada.pop()
            leds_ingreso(len(entrada))
            print("Borrado")
            beep(0.1)

    else:
        ultima_s = None

    time.sleep(0.05)
