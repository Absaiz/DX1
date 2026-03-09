import socket, threading

# Configuramos el puente
WEB_PORT = 9000
INTERNAL_PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', WEB_PORT))
s.listen(10)
print(f"PUENTE ACTIVO: Escuchando en {WEB_PORT}")

def tunnel(c):
    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect(('127.0.0.1', INTERNAL_PORT))
        def pipe(src, dst):
            try:
                while True:
                    d = src.recv(8192)
                    if not d: break
                    dst.sendall(d)
            except: pass
        threading.Thread(target=pipe, args=(c, remote), daemon=True).start()
        threading.Thread(target=pipe, args=(remote, c), daemon=True).start()
    except Exception as e:
        print(f"Fallo conexión interna: {e}")
        c.close()

# Bucle de escucha
while True:
    conn, addr = s.accept()
    print(f"Conexión desde {addr}")
    threading.Thread(target=tunnel, args=(conn,), daemon=True).start()