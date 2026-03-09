import socket
import threading

def web_gateway(comp):
    # Puerto que abrirás en tu navegador (Ryzen)
    WEB_PROXY_PORT = 9000 
    # Puerto interno de Speedbee confirmado
    SPEEDBEE_INTERNAL_PORT = 8080 
    
    def start_proxy():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', WEB_PROXY_PORT))
            s.listen(10)
            comp.col_res.insert(f"🌐 WEB ACCESIBLE: http://100.117.214.15:{WEB_PROXY_PORT}")
            
            while True:
                client_conn, addr = s.accept()
                def handle_tunnel(c):
                    try:
                        # Conexión interna al servicio Speedbee
                        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote.connect(('127.0.0.1', SPEEDBEE_INTERNAL_PORT))
                        
                        def forward(src, dst):
                            try:
                                while True:
                                    data = src.recv(4096)
                                    if not data: break
                                    dst.sendall(data)
                            except: pass
                            finally:
                                src.close()
                                dst.close()
                        
                        # Flujo bidireccional
                        threading.Thread(target=forward, args=(c, remote), daemon=True).start()
                        threading.Thread(target=forward, args=(remote, c), daemon=True).start()
                    except:
                        c.close()
                
                threading.Thread(target=handle_tunnel, args=(client_conn,), daemon=True).start()
        except Exception as e:
            comp.col_res.insert(f"❌ Error en Bridge: {e}")

    # Ejecución en hilo para no bloquear el componente
    t_web = threading.Thread(target=start_proxy, daemon=True)
    t_web.start()

web_gateway(self)