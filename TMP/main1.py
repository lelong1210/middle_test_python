import requests
import socketserver

r = requests.get(url="http://192.168.56.101/phpmyadmin/")
print(r.text)