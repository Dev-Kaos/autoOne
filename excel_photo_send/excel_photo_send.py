import pandas as pd
import dataframe_image as dfi
import pywhatkit as kit
from datetime import datetime
from pathlib import Path
import time

# --- (Tu lógica anterior de carga y procesamiento) ---
# Supongamos que ya tienes tu df_one ordenado y formateado


def automatizar_reporte(df: pd.DataFrame, ruta_imagen: Path, numero_tel: str):
    try:
        # 1. Tomar captura de los primeros 10 registros (para que quepa en la imagen)
        df_snapshot = df.head(10)

        # Estilizar un poco para que se vea bien en la captura
        df_styled = df_snapshot.style.set_table_styles(
            [{'selector': 'th', 'props': [
                ('background-color', '#4CAF50'), ('color', 'white')]}]
        ).background_gradient(cmap='Greens', subset=['Actualizado'])

        # Guardar como PNG
        dfi.export(df_styled, str(ruta_imagen))
        print("Captura de pantalla generada.")

        # 2. Enviar por WhatsApp
        # El número debe incluir el código de país (ej: +57 para Colombia)
        # mensaje = f"Hola, adjunto reporte de pedidos actualizado al {datetime.now().strftime('%d/%m %H:%M')}"

        # # Esto abrirá WhatsApp Web y enviará la imagen
        # # Espera 15 segundos para que cargue la página antes de enviar
        # kit.sendwhats_image(numero_tel, str(ruta_imagen), mensaje, wait_time=15)

        # print("Mensaje enviado con éxito.")

    except Exception as e:
        print(f"Error en la automatización: {e}")


# --- EJECUCIÓN ---
ruta_captura = base_path / "assets" / "reporte_captura.png"
# Reemplaza con el número real de Melissa o el tuyo para probar
numero_destino = "+573001234567"

automatizar_reporte(df_one, ruta_captura, numero_destino)
