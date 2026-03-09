# --- TEST DE EJECUCIÓN ---
import time

def hola_mundo_dx1(comp):
    # 1. Log visual en la columna de resultados
    comp.col_res.insert("--------------------------------")
    comp.col_res.insert(f"👋 ¡HOLA! El script se está ejecutando")
    comp.col_res.insert(f"🕒 Hora local DX1: {time.strftime('%H:%M:%S')}")
    comp.col_res.insert("--------------------------------")
    
    # 2. Forzar un valor en el componente para ver movimiento en el panel
    # Si este componente tiene un puerto de salida, esto debería cambiarlo
    try:
        if hasattr(comp, 'outports') and len(comp.outports) > 0:
            comp.outports[0].send(f"TEST_OK_{time.time()}")
            comp.col_res.insert("✅ Salida enviada al puerto")
    except:
        pass

# Ejecución inmediata
hola_mundo_dx1(self)