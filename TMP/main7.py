import socket
import sys
import _thread
import traceback
import ssl

def main():
    global listen_port, buffer_size, max_conn
    try:
        listen_port = int(input("Enter a listening port: "))
    except KeyboardInterrupt:
        sys.exit(0)

    max_conn = 10000
    buffer_size = 10000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", listen_port))
        s.listen(max_conn)
        print("[*] Initializing socket. Done.")
        print("[*] Socket binded successfully...")
        print("[*] Server started successfully [{}]".format(listen_port))
    except Exception as e:
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            _thread.start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Shutting down...")
            sys.exit(1)
    s.close()


def conn_string(conn, data, addr):
    try:
        print(addr)
        first_line = data.decode('latin-1').split("\n")[0]
        print(first_line)
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        print(webserver)
        proxy_server(webserver, port, conn, data, addr)
    except Exception as e:
        print(e)
        traceback.print_exc()


def proxy_server(webserver, port, conn, data, addr):
    print("{} {} {} {}".format(webserver, port, conn, addr))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))

        if port == 443:  # HTTPS connection
            print("[DEBUG] PORT IS 443")
            context = ssl.create_default_context()
            ssl_conn = context.wrap_socket(s, server_hostname=webserver)
            ssl_conn.send(data)

            # Print data received from the client
            print("[Client -> Proxy HTTPS] Data is:", data.decode('latin-1'))

            while True:
                reply = ssl_conn.recv(buffer_size)

                if len(reply) > 0:
                    conn.sendall(reply)
                    print("[Proxy -> Client HTTPS] Data is:", reply.decode('latin-1'))
                    print("[*] Request sent HTTPS: {} > {}".format(addr[0], webserver))
                else:
                    break

            ssl_conn.close()
        else:  # HTTP connection
            s.send(data)

            # Print data received from the client
            print("[Client -> Proxy] Data is:", data.decode('latin-1'))

            while True:
                reply = s.recv(buffer_size)

                if len(reply) > 0:
                    conn.sendall(reply)
                    print("[Proxy -> Client] Data is:", reply.decode('latin-1'))
                    print("[*] Request sent: {} > {}".format(addr[0], webserver))
                else:
                    break

        s.close()
        conn.close()

    except Exception as e:
        print(e)
        traceback.print_exc()
        s.close()
        conn.close()
        sys.exit(1)


if __name__ == "__main__":
    main()