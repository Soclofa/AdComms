import socket

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            first_letters = []
            
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                if data == "EXIT":
                    response = ''.join(first_letters)
                    conn.sendall(response.encode())
                    break
                else:
                    first_letters.append(data[0])
            
if __name__ == "__main__":
    start_server()
