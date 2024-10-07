import socket
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Socket Server")
    parser.add_argument('-p', '--port', required=True, type=int, help='Server port')
    args = parser.parse_args()
    return args

def create_server_socket(server_port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', server_port))
        server_socket.listen(5)
        print(f"Server listening on port {server_port}")
        return server_socket
    except Exception as e:
        print(f"Error: Unable to create server socket: {e}")
        sys.exit(1)

def accept_connection(server_socket):
    try:
        connection, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        return connection
    except Exception as e:
        print(f"Error: Unable to accept connection: {e}")
        return None

def handle_request(connection):
    try:
        # Receive file data from the client
        file_data = b""
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                break
            file_data += chunk

        if not file_data:
            return "Error: No file data received."

        file_content = file_data.decode('utf-8')
        char_count = sum(char.isalpha() for char in file_content)
        return str(char_count)
    except Exception as e:
        return f"Error: Unable to process file data: {e}"

def send_response(connection, response):
    try:
        connection.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error: Unable to send response: {e}")

def close_socket(socket):
    socket.close()

def main():
    args = parse_arguments()
    server_socket = create_server_socket(args.port)

    try:
        while True:
            connection = accept_connection(server_socket)
            if connection is None:
                continue

            try:
                print("Processing client request...")
                response = handle_request(connection)
                send_response(connection, response)
                print(f"Response sent: {response}")
                
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                connection.close()
                print("Connection closed.")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        close_socket(server_socket)
        print("Server socket closed")

if __name__ == "__main__":
    main()