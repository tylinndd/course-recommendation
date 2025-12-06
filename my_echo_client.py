#!/usr/bin/env python3


import socket
import sys


def main():
    # Check command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python my_echo_client.py [IP or hostname] [port-number]")
        print("Example: python my_echo_client.py localhost 8888")
        sys.exit(1)
    
    
    server_host = sys.argv[1]
    
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connecting to {server_host}:{server_port}...")
        client_socket.connect((server_host, server_port))
        print(f"Connected to Reverse Echo Server at {server_host}:{server_port}")
        print("Type messages to send (or 'end' to exit):\n")
        
        while True:
            message = input("Enter message: ")
            
            if not message:
                continue
            
            client_socket.send((message + '\n').encode('utf-8'))
            
            # Wait for response from server
            response = client_socket.recv(1024).decode('utf-8')
            
            if not response:
                print("Server closed the connection")
                break
            
            # Get the reversed message
            reversed_message = response.strip()
            
            # If we sent 'end', check if we received 'dne' and terminate
            if message.lower() == 'end':
                if reversed_message.lower() == 'dne':
                    # Display the 'dne' message and terminate
                    print(f"{reversed_message}")
                    break
                else:
                    # Display reversed message even if unexpected
                    print(f"Reversed: {reversed_message}\n")
                    break
            else:
                # Display the reversed message for normal messages
                print(f"Reversed: {reversed_message}\n")
    
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {server_host}:{server_port}")
        print("Make sure the server is running and the address/port are correct.")
        sys.exit(1)
    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{server_host}'")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDisconnecting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")


if __name__ == "__main__":
    main()

