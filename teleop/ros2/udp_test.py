
import socket
import json
import time

PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.settimeout(2.0)

print("Waiting for Xbox controller data...")

last_print = 0

try:
    while True:
        try:
            data, address = sock.recvfrom(4096)
        except socket.timeout:
            print("No controller packets received")
            continue

        message = json.loads(data.decode("utf-8"))

        if time.monotonic() - last_print >= 0.2:
            print("Axes:", [
                round(x, 2) for x in message["axes"]
            ])
            print("Buttons:", message["buttons"])
            print("------------------------")
            last_print = time.monotonic()

except KeyboardInterrupt:
    print("Receiver stopped")

finally:
    sock.close()
