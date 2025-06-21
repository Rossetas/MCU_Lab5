import serial
import csv
from time import sleep

# Configuracion
PUERTO_SERIAL = "/dev/ttyACM0"
BAUDIOS = 9600
TIEMPO_ESPERA = 2
NUM_MUESTRAS = 1000
ARCHIVO_CSV = "movimientos.csv"

# tipo de movimiento actual
movimiento = input("Ingrese el tipo de movimiento actual (circulos, arriba_abajo, golpe): ").strip().lower()

try:
    print(f"Conectando al Arduino en {PUERTO_SERIAL}...")
    arduino = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
    sleep(TIEMPO_ESPERA)
    print("Conexion exitosa. Iniciando captura de datos...")

    # Verificar si el archivo ya existe y tiene encabezado
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            encabezado_ya_escrito = True
    except FileNotFoundError:
        encabezado_ya_escrito = False

    with open(ARCHIVO_CSV, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        if not encabezado_ya_escrito:
            escritor.writerow(['Etiqueta', 'aX', 'aY', 'aZ', 'gX', 'gY', 'gZ'])

        contador = 0
        while contador < NUM_MUESTRAS:
            linea = arduino.readline().decode('utf-8').strip()
            if linea.count(',') == 5:
                datos = linea.split(',')
                try:
                    datos_float = [float(valor) for valor in datos]
                    escritor.writerow([movimiento] + datos_float)
                    contador += 1
                    print(f"[{contador}/{NUM_MUESTRAS}] {movimiento}, {datos_float}")
                except ValueError:
                    print("Datos corruptos descartados:", datos)
            else:
                print("Linea no valida:", linea)

    print(f"Captura finalizada. Datos agregados a: {ARCHIVO_CSV}")

except serial.SerialException as e:
    print(f"Error de conexion con el puerto {PUERTO_SERIAL}: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
