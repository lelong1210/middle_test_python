import socket
import threading

HOST = '127.0.0.1'  # Địa chỉ IP của máy chủ
PORT = 9999         # Cổng mà server socket lắng nghe

def handle_client(client_socket, client_address):
    print(f"Đã kết nối từ {client_address}")

    # Nhận dữ liệu từ client
    data = client_socket.recv(1024).decode()
    received_array = data.split(',')

    print("Mảng nhận được từ client:")
    for i in received_array:
        print(i)

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server đang lắng nghe trên cổng {PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()

        # Tạo một thread mới để xử lý kết nối từ client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()