import socket
import threading
import time

def puente_con_logs_a_terminal(comp):
    WEB_PORT = 9000
    INTERNAL_PORT = 8080
    MI_PC_IP = "192.168.171.156" # La IP donde tienes el Hércules/Terminal

    def log_remoto(mensaje):
        try:
            # Enviamos el log a tu terminal abierta
            s_log = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_log.connect((MI_PC_IP, 23)) 
            s_log.sendall(f"[LOG DX1]: {mensaje}\n".encode())
            s_log.close()
        except: pass

    def start_bridge():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                s.bind(('0.0.0.0', WEB_PORT))
                log_remoto(f"🚀 PUENTE EN MARCHA: http://100.117.214.15:{WEB_PORT}")
            except Exception as e:
                log_remoto(f"❌ ERROR BIND: {e}")
                return

            s.listen(10)
            while True:
                conn, addr = s.accept()
                log_remoto(f"🔗 Conexión desde Ryzen: {addr[0]}")
                
                def tunnel(c):
                    try:
                        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote.settimeout(5)
                        remote.connect(('127.0.0.1', INTERNAL_PORT))
                        
                        def pipe(src, dst):
                            try:
                                while True:
                                    d = src.recv(8192)
                                    if not d: break
                                    dst.sendall(d)
                            except: pass
                        
                        threading.Thread(target=pipe, args=(c, remote), daemon=True).start()
                        pipe(remote, c)
                    except Exception as e:
                        log_remoto(f"⚠️ Fallo interno al 8080: {e}")
                        c.close()

                threading.Thread(target=tunnel, args=(conn,), daemon=True).start()
        except Exception as e:
            log_remoto(f"❌ Error Crítico: {e}")

    threading.Thread(target=start_bridge, daemon=True).start()

# Ejecución
puente_con_logs_a_terminal(self)