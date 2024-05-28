import socket
import curses

def create_client_name(name, my_socket, scr):
    my_socket.send(f"{name}\n".encode())
    confirmation = my_socket.recv(1024).decode()  # Receive confirmation from server
    scr.addstr(confirmation + "\n")  # Display confirmation
    scr.refresh()

def create_client_get_names(request, my_socket, scr): 
    my_socket.send(f"{request}\n".encode())
    while True:
        try:
            names = my_socket.recv(1024).decode()
            scr.addstr(names + "\n")
            scr.refresh()
            break
        except BlockingIOError:
            continue

def create_client_message(message, my_socket, scr):
    my_socket.send(f"{message}\n".encode())

def create_exit_message(my_socket, scr):
    my_socket.send("EXIT\n".encode())
    my_socket.close()
    curses.endwin()  # End the curses window
    exit()

def main(scr):
    try:
        curses.echo()
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = "127.0.0.1"
        server_port = 7777
        my_socket.connect((server_ip, server_port))

        message = my_socket.recv(1024).decode()
        scr.addstr(message + "\n")
        scr.refresh()

        while True:
            # Input loop
            scr.addstr(" > ")
            scr.refresh()
            client_str = scr.getstr().decode()

            if client_str.startswith("NAME"):
                create_client_name(client_str, my_socket, scr)
            elif client_str.startswith("GET_NAMES"):
                create_client_get_names(client_str, my_socket, scr)
            elif client_str.startswith("MSG"):
                create_client_message(client_str, my_socket, scr)
            elif client_str.startswith("EXIT"):
                create_exit_message(my_socket, scr)
            else:  # invalid message
                scr.addstr("Invalid command\n")
                scr.refresh()

            # Check for server response and display it
            my_socket.setblocking(0)  # Set socket to non-blocking
            try:
                while True:
                    data = my_socket.recv(1024).decode()
                    if data:
                        scr.addstr(data + "\n")
                        scr.refresh()
                    else:
                        break
            except BlockingIOError:
                pass

    except KeyboardInterrupt:
        create_exit_message(my_socket, scr)  # Pass scr to create_exit_message

if __name__ == '__main__':
    curses.wrapper(main)
