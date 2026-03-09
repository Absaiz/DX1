import socket
import threading
import time

def web_gateway(comp):
    # Puerto externo (Tailscale) y puerto interno (Speedbee)
    WEB_PROXY_PORT = 9000 
    SPEEDBEE_INTERNAL_PORT = 8080 
    
    def start_proxy():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', WEB_PROXY_PORT))
            s.listen(20)
            
            # Log de inicio en la columna de resultados de Synapse
            comp.col_res.insert(f"🚀 BRIDGE WEB ON: http://100.117.214.15:{WEB_PROXY_PORT}")
            
            while True:
                client_conn, addr = s.accept()
                # Log cada vez que tu Ryzen intenta entrar
                comp.col_res.insert(f"🔗 Conexión entrante desde: {addr[0]}")
                
                def handle_tunnel(c, client_addr):
                    try:
                        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote.settimeout(5)
                        remote.connect(('127.0.0.1', SPEEDBEE_INTERNAL_PORT))
                        
                        def forward(src, dst, label):
                            try:
                                while True:
                                    data = src.recv(8192) # Aumentamos buffer para fluidez web
                                    if not data: break
                                    dst.sendall(data)
                            except:
                                pass
                            finally:
                                src.close()
                                dst.close()

                        # Iniciamos el tráfico bidireccional
                        threading.Thread(target=forward, args=(c, remote, "IN"), daemon=True).start()
                        threading.Thread(target=forward, args=(remote, c, "OUT"), daemon=True).start()
                        
                    except Exception as e:
                        comp.col_res.insert(f"⚠️ Error conectando al puerto 8080: {e}")
                        c.close()
                
                threading.Thread(target=handle_tunnel, args=(client_conn, addr), daemon=True).start()
                
        except Exception as e:
            comp.col_res.insert(f"❌ Fallo crítico en Bridge: {e}")

    # Lanzamos el servicio
    t_web = threading.Thread(target=start_proxy, daemon=True)
    t_web.start()

# Ejecución
web_gateway(self)