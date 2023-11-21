import socketserver
from http.server import SimpleHTTPRequestHandler
import requests

class ProxyServer:
    def Get_Request(self,url,data):
        send = requests.get(url=url,data=data)
        print(send.text)

class Gui:
    def __init__(self) -> None:
        pass

ProxyServer = ProxyServer()
ProxyServer.Get_Request("https://www.google.com/","")