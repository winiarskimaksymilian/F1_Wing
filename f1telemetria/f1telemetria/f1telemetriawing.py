import sys
import socket
import struct
import serial.tools.list_ports  
import time
import serial

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial() 
time.sleep(2)
porList = []

serialInst.baudrate = 115200 # Ustawienie prędkości transmisji
serialInst.port = "COM4"
serialInst.open()

# 1. Konfiguracja połączenia UDP
UDP_IP = "0.0.0.0"  # Słuchamy na wszystkich interfejsach sieciowych
UDP_PORT = 20777

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

print(f"=== Oczekiwanie na telemetrię z F1 na porcie {UDP_PORT}... ===")

time.sleep(2)

try:
    while True:
        # 2. Odbiór surowych bajtów z gry
        data, addr = udp_socket.recvfrom(2048)

        # 3. Zabezpieczenie przed zbyt krótkim pakietem
        if len(data) < 29:
            continue

        # 4. Rozpakowanie nagłówka (dokładnie 29 bajtów)
        # Format: <HBBBBBQfIBBBB
        # Suma bajtów: 2+1+1+1+1+1+8+4+4+1+1+1+1 = 29 B
        header = struct.unpack('<HBBBBBQfIBBBB', data[:27])
        packet_id = header[5]  # ID pakietu (6 = Car Telemetry)

        # 5. Filtrowanie: Interesuje nas tylko Packet ID = 6
        if packet_id == 6:
            # Upewniamy się, że odczytaliśmy pełny pakiet telemetrii
            if len(data) < 1000:
                continue

            drs = data[47]

            # 7. Wypisanie czytelnych wyników
            print(drs)
            komunikat = f"{drs}\n"
            serialInst.write(komunikat.encode('utf-8'))  # Wysyłanie danych DRS przez port szeregowy
            

except KeyboardInterrupt:
    print("\nZatrzymano odbiornik telemetrii.")
finally:
    udp_socket.close()


