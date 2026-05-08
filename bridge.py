import serial
import requests
import time

# Beddel l-COM port 3la hsab chnou t-la3 lik f Arduino IDE
ser = serial.Serial('COM6', 9600, timeout=1) 
API_URL = "http://127.0.0.1:8000/attendance/log"

print("🌉 Bridge Connected. Waiting for Keypad...")

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("SCAN:"):
            apogee = line.split(":")[1]
            print(f"🔍 Processing Apogee: {apogee}")
            
            try:
                response = requests.post(API_URL, json={"apogee_code": apogee})
                
                if response.status_code == 200:
                    data = response.json()
                    ser.write(f"OK|{data['student']}|{data['logs_today']}\n".encode())
                elif response.status_code == 409:
                    detail = response.json()['detail']
                    if detail['status'] == "limit_reached":
                        ser.write(b"LIMIT\n")
                    else:
                        ser.write(f"SOON|{detail['minutes_remaining']}\n".encode())
                else:
                    ser.write(b"ERROR\n")
            except Exception as e:
                print(f"❌ API Error: {e}")
                ser.write(b"SERVER_DOWN\n")
    time.sleep(0.1)