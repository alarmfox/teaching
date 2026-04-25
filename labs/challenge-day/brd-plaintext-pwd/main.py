"""
DTLab: Interactive Security Challenge - Network Traffic Analysis

GOAL: Capture this traffic with Wireshark and decode the password.

WARNING: This script demonstrates an insecure practice. Sending credentials 
without real encryption (Base64 is just encoding) is highly dangerous.

Usage with `uv`:
1. Ensure `uv` is installed: https://docs.astral.sh/uv/
2. Run the script:
   uv run main.py --password "supersecret" -p 8080 --ip 127.0.0.1
"""

import argparse
import json
import base64
import time
import socket as sk


# Setup command line arguments
parser = argparse.ArgumentParser(prog="Client", description="DTLab educational network challenge")

parser.add_argument("--password", required=True, type=str, help="The password to broadcast")
parser.add_argument("-p", "--port", required=True, type=int, help="Target UDP port")
parser.add_argument("--ip", required=True, action="append", help="Target IP addresses")

packet = {"protocol": "DTLab-Challenge", "encoding": "base64"}


def send_packet(address: str, port: int, password: str) -> None:
    # Create a UDP socket for broadcasting the challenge data
    cs = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    cs.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    cs.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)

    # CHALLENGE: We encode the password in Base64.
    # Students must capture this traffic in Wireshark and decode the 'secret'.
    packet["secret"] = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    data = json.dumps(packet)
    cs.sendto(data.encode("utf-8"), (address, port))

    cs.close()


def run(ips: list, port: int, password: str) -> None:
    print("Broadcasting packet. Open Wireshark now to capture.")
    print("Press Ctrl+C to stop.")
    while True:
        for ip in ips:
            print(f"Sending packet on {ip}:{port}")
            send_packet(ip, port, password)
        # Wait 5 seconds between broadcasts for easier capture
        time.sleep(5)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        run(args.ip, args.port, args.password)
    except KeyboardInterrupt:
        print("\nChallenge stopped.")
