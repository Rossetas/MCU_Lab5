import serial
import csv
from time import sleep

# Configuracion
PUERTO_SERIAL = "/dev/ttyACM0"
BAUDIOS = 9600
TIEMPO_ESPERA = 2
NUM_MUESTRAS = 1000

# tipo de movimiento
movimiento = input("Ingrese el tipo de movimiento (circulos, arriba_abajo, golpe): ").strip().lower()
archivo_csv = f"{movimiento}.csv"

try:
    print(f"Conectando al Arduino en {PUERTO_SERIAL}...")
    arduino = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
    sleep(TIEMPO_ESPERA)
    print("Conexion exitosa. Iniciando captura de datos...")

    with open(archivo_csv, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ'])

        contador = 0
        while contador < NUM_MUESTRAS:
            linea = arduino.readline().decode('utf-8').strip()
            if linea.count(',') == 5:
                datos = linea.split(',')
                try:
                    datos_float = [float(valor) for valor in datos]
                    escritor.writerow(datos_float)
                    contador += 1
                    print(f"[{contador}/{NUM_MUESTRAS}] {datos_float}")
                except ValueError:
                    print("Datos corruptos descartados:", datos)
            else:
                print("Linea no valida:", linea)

    print(f"Captura finalizada. Archivo guardado como: {archivo_csv}")

except serial.SerialException as e:
    print(f"Error de conexion con el puerto {PUERTO_SERIAL}: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
