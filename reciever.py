import os
import tqdm
import socket
import sys


ip = sys.argv[1]


SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

client_socket = socket.socket()

client_socket.connect((ip, SERVER_PORT))


received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)

filesize = int(filesize)

progress = tqdm.tqdm(range(
    filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)


with open(filename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
