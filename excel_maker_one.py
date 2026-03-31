import pandas as pd
from datetime import datetime

# 1. Preparar los datos (Simulación de carga)
# En un escenario real, usarías: df = pd.read_excel('tu_archivo.xlsx')
data = {
    'ColumnaA': ['ID1', 'ID2', 'ID3'],
    'ColumnaH': ['PROD-001', 'SUR-002', 'CENTRO-003'],
    'Fecha_Ult_Avance': ['2026-03-20 10:00', '2026-03-21 11:00', '2026-03-22 12:00'],
    'Grupo': ['OYM_BOG_CENTRO PROD', 'OYM_BOG_SUR PROD', 'OYM_CAR_PROD']
}

df = pd.DataFrame(data)

# 2. Dividir texto (TextToColumns de VBA)
# Dividimos por el guion '-' y nos quedamos con la primera parte
df['H_Limpia'] = df['ColumnaH'].str.split('-').str[0]

# 3. Cálculo de tiempo transcurrido
df['HOY'] = datetime.now()
df['Fecha_Ult_Avance'] = pd.to_datetime(df['Fecha_Ult_Avance'])
df['Tiempo_Transcurrido'] = df['HOY'] - df['Fecha_Ult_Avance']

# 4. Asignar Contratistas (Sustituye tu ciclo While e IFs)
mapeo = {
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
df['Contratista'] = df['Grupo'].map(mapeo)

# 5. GENERAR EL EXCEL FINAL
nombre_archivo = 'Resultado_Informe_WO.xlsx'
df.to_excel(nombre_archivo, index=False)

print(f"¡Listo! Se ha creado el archivo: {nombre_archivo}")
