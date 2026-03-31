from typing import cast
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import time

base_path = Path('.').resolve()
archivo_entrada = base_path / "assets" / 'wm_order.xlsx'
archivo_salida = base_path / 'assets' / 'Informe_Tiempos_Actualizados.xlsx'

if archivo_entrada.exists():
    try:
        # Carga
        df_principal = cast(pd.DataFrame, pd.read_excel(
            archivo_entrada, sheet_name='Page 1'))

        # Selección y limpieza
        df_one = df_principal[[
            "Número", "Creado", "Grupo de calificación", "Nombre", "Ubicación", "Actualizado"
        ]].copy()

        # Cálculo
        df_one['Actualizado'] = pd.to_datetime(df_one['Actualizado'])
        df_one['tiempo_transcurrido'] = datetime.now() - df_one['Actualizado']

        # Ordenar (los que llevan más tiempo sin actualizar arriba)
        # df_one = df_one.sort_values(by='tiempo_transcurrido', ascending=False)
        # 1. Aseguramos que la columna sea timedelta (por si acaso)
        df_one['tiempo_transcurrido'] = pd.to_timedelta(
            df_one['tiempo_transcurrido'])

        # 2. Creamos una función para formatear cada celda
        def formatear_tiempo(td: pd.Timedelta) -> str:
            # Si el valor es nulo (NaT)
            if pd.isnull(td):
                return "Sin datos"

            # Extraemos componentes
            dias = td.days
            horas = td.components.hours
            minutos = td.components.minutes

            # Retornamos un string limpio: "X días, HH:MM"
            return f"{dias} días, {horas:02d}:{minutos:02d}"

        # 3. Aplicamos el formato
        df_one['tiempo_transcurrido_legible'] = df_one['tiempo_transcurrido'].apply(
            formatear_tiempo)

        # 4. Guardamos a Excel usando la nueva columna legible
        df_one.to_excel(archivo_salida, index=False)
        # Guardar
        df_one.to_excel(archivo_salida, index=False)
        print(df_one)
        print(f"Proceso completado. Archivo generado: {archivo_salida.name}")

    except Exception as e:
        print(f"Error en el proceso de los excels: {str(e)}")
else:
    print("No se encontró el archivo de origen.")
