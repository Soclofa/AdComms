import socket
import select
import chat_protocol

SERVER_PORT = 7777
SERVER_IP = "0.0.0.0"

def handle_client_request(current_socket, clients_names, data):
    if data.startswith("GET_NAMES"):
        names_list = "Connected clients:\n" + "\n".join(clients_names.values())
        return names_list, current_socket
    elif data.startswith("MSG"):
        try:
            parts = data.split(" ", 2)  # Split into 3 parts: "MSG", "client_name", and "msg_content"
            if len(parts) < 3:
                raise ValueError("Invalid format")
            _, recipient_name, message = parts
        except ValueError:
            return "Invalid message format. Use: MSG client_name msg_content", current_socket

        recipient_socket = None
        for socket, name in clients_names.items():
            if name == recipient_name:
                recipient_socket = socket
                break

        if recipient_socket is not None:
            return f"{clients_names[current_socket]}: {message}", recipient_socket  # Return sender's name and message
        else:
            return f"No client named {recipient_name}", current_socket  # Return error message if recipient not found
    else:
        # Simple echo server: just return the data back to the sender
        reply = f"{clients_names[current_socket]}: {data}"
        return reply, current_socket

def handle_client_message(): 
    pass

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def create_initial_response(): 
    return "Welcome to the server!\nPlease enter your name:\n".encode()

def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")

    client_sockets = []
    clients_names = {}
    messages_to_send = []

    while True:
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])

        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print("Client connected from", client_address)
                client_sockets.append(client_socket)
                client_socket.send(create_initial_response())
            else:
                data = current_socket.recv(1024).decode()
                if not data:
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    if current_socket in clients_names:
                        del clients_names[current_socket]
                    current_socket.close()
                else:
                    if current_socket not in clients_names: 
                        print(data)
                        if data.startswith("NAME"):
                            clients_names[current_socket] = data.split(" ")[1].strip()  # Extract name from NAME protocol message
                            print(f"Client's name is: {clients_names[current_socket]}")
                            current_socket.send("Name received successfully\n".encode())  # Send response to client
                        else: 
                            print("Client did not provide a name. Ignoring message.")
                    else:
                        response, dest_socket = handle_client_request(current_socket, clients_names, data)
                        messages_to_send.append((dest_socket, response))

        for message in messages_to_send:
            dest_socket, data = message
            if dest_socket in ready_to_write:
                dest_socket.send(data.encode())
                messages_to_send.remove(message)

if __name__ == '__main__':
    main()
