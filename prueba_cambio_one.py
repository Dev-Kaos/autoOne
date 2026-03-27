import pandas as pd
from datetime import datetime

def cargar_excels(archivo_orders, archivo_tasks):
    # 1. Cargar archivos
    df = pd.read_excel(archivo_orders)
    df_ref = pd.read_excel(archivo_tasks)
    
    # ---------------------------------------------------------
    # SIMULACIÓN DE BORRADOS DE COLUMNAS (Igual a tu Macro)
    # ---------------------------------------------------------
    
    # VBA: Columns("H:H").Delete e I:I.Delete
    # Eliminamos las columnas originales en esas posiciones (índices 7 y 8)
    cols_to_drop = [df.columns[7], df.columns[8]]
    df.drop(columns=cols_to_drop, inplace=True)
    
    # VBA: Columns("C:E").Delete
    # Al borrar C, D y E, todo lo demás se desplaza a la izquierda
    cols_cde = [df.columns[2], df.columns[3], df.columns[4]]
    df.drop(columns=cols_cde, inplace=True)

    # ---------------------------------------------------------
    # PROCESAMIENTO DE FECHAS (Columna "Fecha Ultimo Avance")
    # ---------------------------------------------------------
    
    # Tras los borrados, la columna con la fecha "27/03/2026... - Francisco" 
    # queda en una nueva posición. La limpiamos:
    col_fecha_idx = 4 # Ajustado según el desplazamiento de columnas de tu macro
    raw_fecha = df.iloc[:, col_fecha_idx].astype(str).str[:19]
    
    fecha_dt = pd.to_datetime(raw_fecha, format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Crear "Tiempo Transcurrido" (Ahora - Fecha Avance)
    df['Tiempo Transcurrido'] = datetime.now() - fecha_dt

    # ---------------------------------------------------------
    # RENOMBRAR ENCABEZADOS (Igual a los Range("C1").Value de VBA)
    # ---------------------------------------------------------
    
    # Asignamos los nombres exactos que pedía tu macro
    df.rename(columns={
        df.columns[2]: "Grupo",
        df.columns[3]: "Departamento",
        df.columns[4]: "Fecha Ultimo Avance"
    }, inplace=True)

    # ---------------------------------------------------------
    # CONTRATISTAS Y CRUCE (VLOOKUP -> PR)
    # ---------------------------------------------------------
    
    mapa_contratistas = {
        "OYM_BOG_CENTRO PROD": "INCOPSA",
        "OYM_BOG_SUR PROD": "OPEGIN - SUR",
        "OYM_CAR_PROD": "EIA - CARIBE NORTE",
        "OYM_CAR_SUR_PROD": "EIA - CARIBE SUR",
        "OYM_NOC_PROD": "EIA",
        "OYM_ORI_PROD": "OPEGIN - NORTE",
        "OYM_SOC_PROD": "IMEL - SUR",
        "OYM_BOG_PROD": "IMEL - NORTE",
        "OYM_EJE_CAF_PROD": "EIA - EJE CAFETERO"
    }
    df['Contratista'] = df['Grupo'].map(mapa_contratistas)

    # El VLOOKUP de la macro genera la columna "PR"
    df = pd.merge(df, df_ref[[df_ref.columns[0]]], 
                  left_on=df.columns[0], right_on=df_ref.columns[0], 
                  how='left', suffixes=('', '_REF'))
    
    df.rename(columns={df_ref.columns[0] + '_REF': 'PR'}, inplace=True)

    # ---------------------------------------------------------
    # VERIFICACIÓN FINAL
    # ---------------------------------------------------------
    
    # Ordenar por tiempo ascendente
    df.sort_values(by='Tiempo Transcurrido', ascending=True, inplace=True)

    # MOSTRAR CAMPOS RESULTANTES
    print("\n--- CAMPOS GENERADOS EN EL EXCEL ---")
    print(df.columns.tolist())
    print("-" * 36)

    # Guardar
    df.to_excel('Informe_Final_WO.xlsx', index=False)
    print(">>> Proceso finalizado. Archivo guardado como 'Informe_Final_WO.xlsx'")

# Ejecutar
if __name__ == "__main__":
    orders = 'assets/wm_order.xlsx'
    task = 'assets/wm_task.xlsx'
    cargar_excels(orders, task)