from typing import cast
from pathlib import Path
import pandas as pd
import dataframe_image as dfi
import pywhatkit as kit
from datetime import datetime

# 1. CONFIGURACIÓN DE RUTAS
base_path = Path('.').resolve()
archivo_entrada = base_path / "assets" / 'wm_order.xlsx'
archivo_salida = base_path / 'assets' / 'Informe_Tiempos_Actualizados.xlsx'
# Usamos .absolute() para evitar errores de copia en el portapapeles
ruta_captura = (base_path / "assets" / "reporte_captura.png").absolute()

# Configuración de contacto
NUMERO_WHATSAPP = "+573017846018"


def formatear_tiempo(td: pd.Timedelta) -> str:
    """Convierte un Timedelta en un formato legible de días y horas."""
    if pd.isnull(td):
        return "Sin datos"
    dias = td.days
    horas = td.components.hours
    minutos = td.components.minutes
    return f"{dias} días, {horas:02d}:{minutos:02d}"


def enviar_reporte_whatsapp(df: pd.DataFrame, ruta_img: Path, numero: str):
    """Genera una captura del DataFrame y la envía por WhatsApp."""
    try:
        # Seleccionamos solo las columnas más importantes para la foto
        # (Así la imagen no queda demasiado ancha y se lee bien en el celular)
        columnas_foto = ["Número", "Nombre",
                         "Ubicación", "tiempo_transcurrido_legible"]
        df_snapshot = df[columnas_foto].head(10)

        # Estilizar para la captura
        df_styled = df_snapshot.style.set_table_styles(
            [{'selector': 'th', 'props': [
                ('background-color', '#4CAF50'),
                ('color', 'white'),
                ('font-family', 'Arial')]}]
            # Ocultamos el índice (0, 1, 2...) para que se vea más limpio
        ).hide(axis="index")

        # Exportar imagen
        dfi.export(df_styled, str(ruta_img))
        print(f"--- Captura generada en: {ruta_img} ---")

        # Mensaje de texto
        ahora = datetime.now().strftime('%d/%m %H:%M')
        mensaje = f"Hola Melissa, adjunto el reporte de pedidos con mayor tiempo sin actualizar ({ahora})."

        print("Abriendo WhatsApp Web... NO MUEVAS EL MOUSE NI CAMBIES DE VENTANA.")

        # Ajuste de tiempos:
        # wait_time=35 (espera a que cargue la página antes de pegar la imagen)
        kit.sendwhats_image(
            receiver=numero,
            img_path=str(ruta_img),
            caption=mensaje,
            wait_time=35
        )
        print("--- Proceso de WhatsApp completado ---")

    except Exception as e:
        print(f"Error al enviar WhatsApp: {str(e)}")


# 2. EJECUCIÓN PRINCIPAL
if archivo_entrada.exists():
    try:
        print("Iniciando procesamiento de datos...")
        df_principal = cast(pd.DataFrame, pd.read_excel(
            archivo_entrada, sheet_name='Page 1'))

        # Selección de columnas originales
        df_one = df_principal[[
            "Número", "Creado", "Grupo de calificación", "Nombre", "Ubicación", "Actualizado"
        ]].copy()

        # Cálculos de tiempo
        df_one['Actualizado'] = pd.to_datetime(df_one['Actualizado'])
        df_one['tiempo_transcurrido'] = datetime.now() - df_one['Actualizado']

        # IMPORTANTE: Ordenar antes de formatear a texto
        df_one = df_one.sort_values(by='tiempo_transcurrido', ascending=False)

        # Crear columna legible (String) para el reporte
        df_one['tiempo_transcurrido_legible'] = df_one['tiempo_transcurrido'].apply(
            formatear_tiempo)

        # Guardar el Excel completo
        df_one.to_excel(archivo_salida, index=False)
        print(f"Archivo Excel generado: {archivo_salida.name}")

        # 3. LLAMADA A LA AUTOMATIZACIÓN
        enviar_reporte_whatsapp(df_one, ruta_captura, NUMERO_WHATSAPP)

    except Exception as e:
        print(f"Error en el proceso: {str(e)}")
else:
    print(f"No se encontró el archivo en: {archivo_entrada}")
