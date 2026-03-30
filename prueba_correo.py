import flet as ft
# Asegúrate de que config.py tenga: LISTA_CORREOS = ["ejemplo@mail.com"]
import correos


def main(page: ft.Page):
    page.title = "kcode"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- Lógica de Gestión de Correos ---
    def guardar_en_correos():
        """Escribe la lista actual en el archivo config.py"""
        with open("correos.py", "w", encoding="utf-8") as f:
            f.write(f"LISTA_CORREOS = {correos.LISTA_CORREOS}")
        snack = ft.SnackBar(ft.Text("Lista actualizada en correos.py"))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def abrir_ajustes_correo(e):
        lista_items = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
        txt_nuevo_correo = ft.TextField(label="Nuevo correo", expand=True)

        def eliminar_correo(correo_texto: str):
            correos.LISTA_CORREOS.remove(correo_texto)
            guardar_en_correos()
            actualizar_lista_visual()

        def agregar_correo(e):
            if txt_nuevo_correo.value:
                correos.LISTA_CORREOS.append(txt_nuevo_correo.value)
                txt_nuevo_correo.value = ""
                guardar_en_correos()
                actualizar_lista_visual()

        def actualizar_lista_visual():
            lista_items.controls.clear()
            for correo in correos.LISTA_CORREOS:
                lista_items.controls.append(
                    ft.Row([
                        ft.Text(correo, expand=True),
                        ft.IconButton(ft.Icons.DELETE, icon_color="red",
                                      on_click=lambda e, c=correo: eliminar_correo(c))
                    ])
                )
            page.update()

        actualizar_lista_visual()

        # Diálogo emergente
        def cerrar_dialogo():
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Destinatarios"),
            content=ft.Column(controls=[
                lista_items,
                ft.Row(controls=[txt_nuevo_correo, ft.IconButton(
                    ft.Icons.ADD, on_click=agregar_correo)]),
            ], tight=True, width=400),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: cerrar_dialogo())
            ],
        )

        # MÉTODO COMPATIBLE PARA ABRIR:
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- Elementos de tu Interfaz Original ---
    txt_usuario = ft.TextField(
        label="Usuario", hint_text="pedro@onnetfibra.co", prefix_icon=ft.Icons.PERSON, width=400)
    txt_password = ft.TextField(label="Contraseña", password=True,
                                can_reveal_password=True, prefix_icon=ft.Icons.LOCK, width=400)

    # NUEVO: Sección de verificación de lista de correo
    seccion_verificacion = ft.Row(
        controls=[
            ft.Text("Ver los Destinatarios:", weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Ver / Editar", icon=ft.Icons.VISIBILITY, on_click=abrir_ajustes_correo)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    fila_botones = ft.Row(
        controls=[
            ft.OutlinedButton("Opción A", icon=ft.Icons.SETTINGS),
            ft.OutlinedButton("Opción B", icon=ft.Icons.HELP),
            ft.OutlinedButton("Opción C", icon=ft.Icons.INFO),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    txt_mensaje = ft.TextField(label="Escribe tu mensaje aquí",
                               multiline=True, min_lines=5, max_lines=10, width=500)
    btn_realizar = ft.FilledButton(
        "Enviar Reporte", icon=ft.Icons.DONE_ALL, width=200, height=50, bgcolor=ft.Colors.BLUE_700)

    # Agregar todo a la página
    page.add(
        ft.Text("Informe de ...", size=30, weight=ft.FontWeight.W_700),
        ft.Divider(height=20, color="transparent"),
        txt_usuario,
        txt_password,
        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE,
                          on_click=lambda _: print("Datos enviados")),
        ft.Divider(height=40),

        seccion_verificacion,  # <--- La nueva sección aquí

        ft.Divider(height=20, color="transparent"),
        ft.Text("Acciones Rápidas", size=16, weight=ft.FontWeight.W_500),
        fila_botones,
        ft.Divider(height=20, color="transparent"),
        txt_mensaje,
        btn_realizar
    )


if __name__ == "__main__":
    ft.app(target=main)
