
import socket
import serial
import json
import time
import math

COM_PORT = "COM5"
BAUD = 115200
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
sock.settimeout(0.05)

teensy = serial.Serial(
    COM_PORT,
    BAUD,
    timeout=0,
    write_timeout=0.1
)

time.sleep(1)

teensy.reset_input_buffer()

def send(enabled, vx, vy, wz):

    command = (
        f"V,{int(enabled)},"
        f"{vx:.4f},{vy:.4f},{wz:.4f}\n"
    )

    teensy.write(command.encode("ascii"))


# Always start disabled
send(False, 0.0, 0.0, 0.0)

print("MINI TESLA - ROS TO TEENSY")
print("Listening on UDP 5006")
print("Connected to Teensy:", COM_PORT)
print("Drive starts DISABLED")

last_packet = time.monotonic()
last_print = 0.0
last_enabled = None
connected = False

try:

    while True:

        try:
            packet, address = sock.recvfrom(4096)

            data = json.loads(
                packet.decode("utf-8")
            )

            enabled = data.get("enabled", True)

            if type(enabled) is not bool:
                raise ValueError("Invalid enable state")

            vx = float(data["vx"])
            vy = float(data["vy"])
            wz = float(data["wz"])

            if not all(math.isfinite(v) for v in [vx, vy, wz]):
                raise ValueError("Invalid velocity")

            if (
                abs(vx) > 0.151
                or abs(vy) > 0.151
                or abs(wz) > 0.501
            ):
                raise ValueError("Velocity out of range")

            if not enabled:
                vx = 0.0
                vy = 0.0
                wz = 0.0

            send(enabled, vx, vy, wz)

            now = time.monotonic()
            last_packet = now
            connected = True

            if (
                enabled != last_enabled
                or now - last_print >= 0.5
            ):
                print(
                    f"Enabled={enabled} "
                    f"VX={vx:.3f} "
                    f"VY={vy:.3f} "
                    f"WZ={wz:.3f}"
                )

                last_print = now
                last_enabled = enabled

        except socket.timeout:

            if (
                connected
                and time.monotonic() - last_packet > 0.2
            ):
                send(False, 0.0, 0.0, 0.0)
                connected = False
                last_enabled = False
                print("ROS CONNECTION LOST - STOPPED")

        except (ValueError, KeyError, TypeError,
                UnicodeError, json.JSONDecodeError):

            send(False, 0.0, 0.0, 0.0)
            connected = False
            print("INVALID PACKET - STOPPED")

        # Read available Teensy responses
        response = teensy.read_all()

        if response:
            print(
                response.decode(
                    errors="replace"
                ).strip()
            )

except KeyboardInterrupt:
    print("\nStopping robot...")

finally:

    try:
        send(False, 0.0, 0.0, 0.0)
        teensy.flush()
    finally:
        teensy.close()
        sock.close()
