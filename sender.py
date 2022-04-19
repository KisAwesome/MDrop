import os
import tqdm
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER_HOST = s.getsockname()[0]
s.close()


SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

filename = sys.argv[1]


s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(1)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()

print(f"[+] {address} is connected.")

filesize = os.path.getsize(filename)

client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(
    filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        client_socket.send(bytes_read)
        progress.update(len(bytes_read))
s.close()
