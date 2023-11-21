from mitmproxy import http
from mitmproxy import ctx

class ProxyServer:
    def __init__(self):
        self.ssl_bump_enabled = True

    def request(self, flow: http.HTTPFlow) -> None:
        # Xử lý yêu cầu trước khi gửi đến máy chủ
        print(f"[CLIENT TO SERVER] {flow.request}")

    def response(self, flow: http.HTTPFlow) -> None:
        # Xử lý phản hồi từ máy chủ trước khi gửi đến ứng dụng
        print(f"[SERVER TO CLIENT] {flow.response}")

        if flow.request.scheme == 'https':
            if self.ssl_bump_enabled and not flow.server_conn.sni:
                flow.server_conn.sni = flow.request.host

        decoded_content = flow.response.content.decode('utf-8')
        print(f"[RESPONSE CONTENT] {decoded_content}")

addons = [
    ProxyServer()
]

def start_proxy():
    ctx.log.info("Bắt đầu proxy server...")
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__] + ctx.argv[1:])

if __name__ == '__main__':
    start_proxy()