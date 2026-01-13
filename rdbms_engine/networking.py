import socket
import threading

class TCPServer:
    def __init__(self, host='0.0.0.0', port=9999, executor=None):
        self.host = host
        self.port = port
        self.executor = executor  # Logic engine (to be added later)
        self.running = False

    def start(self):
        """Starts the main listener loop."""
        self.running = True
        # Create an IPv4 (AF_INET), TCP (SOCK_STREAM) socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow reusing the address immediately if the server restarts
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[*] DB listening on {self.host}:{self.port}")

            while self.running:
                try:
                    client, addr = server_socket.accept()
                    # Hand off client to a new thread so the main loop isn't blocked
                    client_handler = threading.Thread(target=self.handle_client, args=(client,))
                    client_handler.start()
                except Exception as e:
                    print(f"[!] Accept Error: {e}")
        
        except Exception as e:
            print(f"[!] Bind Error: {e}")
        finally:
            server_socket.close()

    def handle_client(self, client_socket):
        """Handles the communication with a specific client."""
        with client_socket:
            print(f"[+] New connection established.")
            while True:
                try:
                    # Receive data (max 1KB buffer for now)
                    request = client_socket.recv(1024).decode('utf-8')
                    
                    if not request:
                        break # Client disconnected
                    
                    # Placeholder: Echo the data back to prove connectivity
                    print(f"[>] Received: {request}")
                    response = f"SERVER_ACK: {request}"
                    
                    client_socket.send(response.encode('utf-8'))
                    
                except ConnectionResetError:
                    break
        print("[-] Connection closed.")