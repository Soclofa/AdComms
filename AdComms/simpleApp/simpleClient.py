import socket

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            user_input = input("Enter input (type 'EXIT' to stop): ")
            s.sendall(user_input.encode())
            if user_input == "EXIT":
                data = s.recv(1024).decode()
                print(f"Server reply: {data}")
                break

if __name__ == "__main__":
    start_client()

