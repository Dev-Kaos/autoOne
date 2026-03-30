import flet as ft
import correos
import config_mensajes


def main(page: ft.Page):
    page.title = "kcode"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- Lógica del FilePicker Corregida ---
    lbl_ruta = ft.Text("No se ha seleccionado archivo",
                       italic=True, color="grey")

    # def al_elegir_archivo(e):
    #     # La forma correcta y simple de acceder en versiones modernas
    #     if e.files:
    #         lbl_ruta.value = f"Seleccionado: {e.files[0].name}"
    #         lbl_ruta.color = "blue"
    #         lbl_ruta.weight = "bold"
    #     else:
    #         lbl_ruta.value = "Selección cancelada"
    #     page.update()

    # file_picker = ft.FilePicker(on_result=al_elegir_archivo)
    # page.overlay.append(file_picker)

    # --- Gestión de Archivos y Mensajes ---
    def guardar_en_correos():
        with open("correos.py", "w", encoding="utf-8") as f:
            f.write(f"LISTA_CORREOS = {correos.LISTA_CORREOS}")
        mostrar_notificacion("Lista de correos actualizada")

    def guardar_mensaje_en_archivo():
        with open("config_mensajes.py", "w", encoding="utf-8") as f:
            f.write(f"TEXTOS_GUARDADOS = {config_mensajes.TEXTOS_GUARDADOS}")
        mostrar_notificacion("Plantilla guardada")

    def cargar_plantilla(e):
        opcion = e.control.data
        txt_mensaje.value = config_mensajes.TEXTOS_GUARDADOS.get(opcion, "")
        page.update()

    def grabar_actual(e):
        opcion = e.control.data
        if txt_mensaje.value.strip():
            config_mensajes.TEXTOS_GUARDADOS[opcion] = txt_mensaje.value
            guardar_mensaje_en_archivo()
        else:
            mostrar_notificacion("Escribe algo para grabar")

    def mostrar_notificacion(texto):
        snack = ft.SnackBar(ft.Text(texto))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- Ventana de Correos ---
    def abrir_ajustes_correo(e):
        lista_items = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
        txt_nuevo_correo = ft.TextField(label="Nuevo correo", expand=True)

        def eliminar_correo(correo_texto):
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

        dlg = ft.AlertDialog(
            title=ft.Text("Destinatarios"),
            content=ft.Column(controls=[
                lista_items,
                ft.Row(controls=[txt_nuevo_correo, ft.IconButton(
                    ft.Icons.ADD, on_click=agregar_correo)]),
            ], tight=True, width=400),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: (
                setattr(dlg, "open", False), page.update()))],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- Interfaz Gráfica ---
    txt_usuario = ft.TextField(
        label="Usuario", prefix_icon=ft.Icons.PERSON, width=400)
    txt_password = ft.TextField(label="Contraseña", password=True,
                                can_reveal_password=True, prefix_icon=ft.Icons.LOCK, width=400)
    txt_mensaje = ft.TextField(
        label="Mensaje", multiline=True, min_lines=5, width=500)

    def btn_plantilla(letra):
        return ft.Column([
            ft.OutlinedButton(
                f"Opción {letra}", icon=ft.Icons.DOWNLOAD, on_click=cargar_plantilla, data=letra),
            ft.TextButton("Grabar", icon=ft.Icons.SAVE,
                          on_click=grabar_actual, data=letra, icon_color="blue")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    seccion_archivo = ft.Container(
        content=ft.Column([
            ft.Text("ADJUNTAR MATRIZ DE DATOS", size=12, weight="bold"),
            ft.Row([
                ft.ElevatedButton("Cargar Archivo", icon=ft.Icons.UPLOAD_FILE,
                                  on_click=lambda _: file_picker.pick_files()),
                lbl_ruta
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment="center"),
        padding=20, bgcolor=ft.Colors.GREY_100, border_radius=10
    )

    page.add(
        ft.Text("Informe de Gestión", size=30, weight="bold"),
        txt_usuario, txt_password,
        ft.ElevatedButton(
            "Guardar Login", on_click=lambda _: print("Login guardado")),
        ft.Divider(height=30),
        ft.Row([ft.Text("Destinatarios:"), ft.ElevatedButton(
            "Editar", on_click=abrir_ajustes_correo)], alignment="center"),
        ft.Row([btn_plantilla("A"), btn_plantilla("B"),
               btn_plantilla("C")], alignment="center"),
        txt_mensaje,
        seccion_archivo,
        ft.FilledButton("Enviar Reporte", icon=ft.Icons.SEND,
                        width=250, bgcolor=ft.Colors.BLUE_700)
    )


if __name__ == "__main__":
    ft.app(target=main)
