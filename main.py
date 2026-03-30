import flet as ft

def main(page: ft.Page):
    # Configuración de la página
    page.title = "kcode"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE # Permite scroll si el contenido es largo
    page.padding = 30

    # Autentificacíon
    txt_usuario = ft.TextField(
        label="Usuario",
        hint_text="pedro@onnetfibra.co", 
        prefix_icon=ft.Icons.PERSON,
        width=400
    )
    txt_password = ft.TextField(
        label="Contraseña", 
        hint_text="la clave de 16 dígitos que generes",
        password=True, 
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        width=400
    )
    btn_enviar = ft.ElevatedButton(
        "Guardar",
        icon=ft.Icons.SAVE,
        on_click=lambda _: print("Datos enviados"),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    # Verificacion de lista de correo
    

    # 3. Fila de tres botones debajo
    fila_botones = ft.Row(
        controls=[
            ft.OutlinedButton("Opción A", icon=ft.Icons.SETTINGS),
            ft.OutlinedButton("Opción B", icon=ft.Icons.HELP),
            ft.OutlinedButton("Opción C", icon=ft.Icons.INFO),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # 4. Campo de texto grande para mensaje
    txt_mensaje = ft.TextField(
        label="Escribe tu mensaje aquí",
        multiline=True,
        min_lines=5,
        max_lines=10,
        hint_text="Ingresa el contenido detallado...",
        width=500
    )

    # 5. Botón de Realizar
    btn_realizar = ft.FilledButton(
        "Enviar Reporte",
        icon=ft.Icons.DONE_ALL,
        width=200,
        height=50,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700
    )

    # Agregar todos los elementos a la página en orden vertical
    page.add(
        ft.Text("Informe de ...", size=30, weight=ft.FontWeight.W_700),
        ft.Divider(height=20, color="transparent"), # Espaciador
        txt_usuario,
        txt_password,
        btn_enviar,
        ft.Divider(height=40), # Línea divisoria
        ft.Text("Acciones Rápidas", size=16, weight=ft.FontWeight.W_500),
        fila_botones,
        ft.Divider(height=20, color="transparent"),
        txt_mensaje,
        btn_realizar
    )

if __name__ == "__main__":
    ft.app(target=main) # type: ignore