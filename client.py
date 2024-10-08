import socket
import sys
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Socket Client")
    parser.add_argument('-a', '--addr', required=True, help='Server IP address')
    parser.add_argument('-p', '--port', required=True, type=int, help='Server port')
    parser.add_argument('-f', '--files', required=True, nargs='+', help='Paths to files to send')

    args = parser.parse_args()

    # Validate file paths
    for file_path in args.files:
        if not file_path.strip():
            print("Error: One of the file paths is empty.")
            sys.exit(1)
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)
    
    return args

def connect_client_socket(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        return client_socket
    except Exception as e:
        print(f"Error: Unable to connect to server socket: {e}")
        sys.exit(1)

def send_request(client_socket, file_data):
    try:
        client_socket.sendall(file_data.encode('utf-8'))

        client_socket.shutdown(socket.SHUT_WR)
    except Exception as e:
        print(f"Error: Unable to send request: {e}")
        client_socket.close()
        sys.exit(1)

def receive_response(client_socket):
    try:
        response = ""
        while True:
            chunk = client_socket.recv(4096).decode('utf-8')
            if not chunk:
                break
            response += chunk
        
        return response
    except Exception as e:
        print(f"Error: Unable to receive response: {e}")
        return None

def close_socket(client_socket):
    try:
        client_socket.close()
    except Exception as e:
        print(f"Error: Unable to close socket: {e}")

def main():
    args = parse_arguments()
    server_ip = args.addr
    server_port = args.port
    file_paths = args.files

    # Process each file and send to server
    for file_path in file_paths:
        try:
            client_socket = connect_client_socket(server_ip, server_port)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = f.read()
            
            if not file_data:
                print(f"Warning: File '{file_path}' is empty. Sending empty content.")
            
            # Connect to the server
            send_request(client_socket, file_data)
            print(f"Sent file data from '{file_path}' to server {server_ip}:{server_port}")
            
            # Receive and print the server response
            response = receive_response(client_socket)
            if response:
                print(f"Response for '{file_path}', the alphabet count is : {response}")
            else:
                print(f"Error: No response received for file '{file_path}'.")

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")
        finally:
            close_socket(client_socket)

if __name__ == "__main__":
    main()
