import pandas as pd
from datetime import datetime, timedelta

# TODO:

orders = 'assets/wm_order.xlsx'
task = 'assets/wm_task.xlsx'

# Los campos requeridos son : work order  fecha ultimo avance, creado, grupo Calificación, comuna y tiempo transcurrido
def cargar_excels(orders, task):
    df_orders = pd.read_excel(orders)
    df_task = pd.read_excel(task)

    # print(f"Estas son las ordenes \n{df_orders}")
    # print(f"Estas son las tasks \n{df_task}")

    df_orders['Actualizado'] = df_orders['Número'].map(
        df_task.set_index('Número')['Actualizado']
    )

    # print(f"Estas son las ordenes \n{df_orders}")
    
    df_orders_actu = df_orders[['work order']]
    print(f"Estas son las ordenes \n{df_orders_actu}")

# Ejecutar
if __name__ == "__main__":
    cargar_excels(orders, task)