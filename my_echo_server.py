#!/usr/bin/env python3


import socket
import sys


def reverse_string(s):
    """Reverse a string."""
    return s[::-1]


def main():
    # Default port number
    port = 8888
    
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Error: Port must be a number")
            sys.exit(1)
    
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    try:
        server_socket.bind(('', port))
        print(f"Reverse Echo Server started on port {port}")
        print(f"Waiting for connections...")
    except OSError as e:
        print(f"Error: Could not bind to port {port}: {e}")
        sys.exit(1)
    
    server_socket.listen(5)
    
    try:
        while True:
            
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address[0]}:{client_address[1]}")
            
            try:
                while True:
                    
                    data = client_socket.recv(1024).decode('utf-8')
                    
                    if not data:
                        # Client closed connection
                        break
                    
                    
                    message = data.rstrip('\n\r')
                    
                    
                    reversed_message = reverse_string(message)
                    
                    print(f"Received: {message}")
                    print(f"Sending: {reversed_message}")
                    
                    
                    client_socket.send((reversed_message + '\n').encode('utf-8'))
            
            except ConnectionResetError:
                print(f"Client {client_address[0]}:{client_address[1]} disconnected unexpectedly")
            except Exception as e:
                print(f"Error handling client: {e}")
            finally:
                client_socket.close()
                print(f"Connection with {client_address[0]}:{client_address[1]} closed")
    
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()
        print("Server closed")


if __name__ == "__main__":
    main()

