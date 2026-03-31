import pandas as pd
from datetime import datetime
import os

# CONFIGURACIÓN DE ARCHIVOS
archivo_entrada = 'wm_order.xlsx'
archivo_maestro = 'wm_task.xlsx'  # El archivo que tiene la "Hoja1"


def ejecutar_macro_completa():
    # Verificación de existencia de ambos archivos
    if not os.path.exists(archivo_entrada) or not os.path.exists(archivo_maestro):
        print("Error: Uno de los archivos de Excel no se encuentra en la carpeta.")
        return

    try:
        # 1. Cargar datos de ambos archivos
        df_principal = pd.read_excel(archivo_entrada, sheet_name='Page 1')
        # Asumimos que la info está en la primera hoja
        df_maestro = pd.read_excel(archivo_maestro)

        # 2. Limpieza de columna H (Text to Columns en VBA)
        # Separamos por '-' y nos quedamos con la primera parte [cite: 1]
        df_principal.iloc[:, 7] = df_principal.iloc[:,
                                                    7].astype(str).str.split('-').str[0]

        # 3. EL "VLOOKUP" (Merge en Pandas)
        # Buscamos los IDs de la columna A del principal en la columna A del maestro
        # 'how=left' asegura que mantengamos todas las filas del archivo original
        df_principal = pd.merge(
            df_principal,
            # Solo tomamos la primera columna del maestro para comparar
            df_maestro.iloc[:, [0]],
            left_on=df_principal.columns[0],
            right_on=df_maestro.columns[0],
            how='left',
            suffixes=('', '_check')
        )

        # Renombramos la columna resultante a "PR" como en tu macro
        df_principal.rename(
            columns={df_maestro.columns[0] + '_check': 'PR'}, inplace=True)

        # 4. Cálculo de Tiempos [cite: 2]
        ahora = datetime.now()
        df_principal['HOY'] = ahora
        df_principal['Fecha_Ref'] = pd.to_datetime(
            df_principal.iloc[:, 7], errors='coerce')
        df_principal['Tiempo_Transcurrido'] = ahora - df_principal['Fecha_Ref']

        # 5. Diccionario de Contratistas (Reemplaza el While/If) [cite: 13, 14]
        mapeo_contratistas = {
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
        # Columna 3 (índice 2) es "Grupo" en tu macro [cite: 4, 13]
        df_principal['Contratista'] = df_principal.iloc[:, 2].map(
            mapeo_contratistas)

        # 6. Ordenar por Tiempo Transcurrido y PR [cite: 3, 11]
        df_principal.sort_values(by=['Tiempo_Transcurrido', 'PR'], ascending=[
                                 True, True], inplace=True)

        # 7. Exportar el resultado final
        df_principal.to_excel('Informe_Final_Completo.xlsx', index=False)
        print("¡Proceso finalizado! Se usaron ambos archivos para generar el reporte.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")


ejecutar_macro_completa()
