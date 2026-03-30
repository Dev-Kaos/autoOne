# main.py
import flet as ft
import config
from core_mail import enviar_correo_masivo

def main(page: ft.Page):
    page.title = "Asistente Manuel Vela"
    page.window_width = 450
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Campos de Entrada
    txt_correo = ft.TextField(label="Tu Correo", value=config.EMAIL_REMITENTE, border_radius=10)
    txt_pass = ft.TextField(label="Contraseña de Aplicación", password=True, can_reveal_password=True, border_radius=10)
    
    # Cuerpo del mensaje
    txt_cuerpo = ft.TextField(
        label="Cuerpo del correo", 
        multiline=True, 
        min_lines=3, 
        value="Adjunto el informe semanal del área para su revisión."
    )

    # Botones de mensajes rápidos
    def set_mensaje(e):
        if e.control.text == "Finalizado":
            txt_cuerpo.value = "El informe ha sido completado exitosamente."
        elif e.control.text == "Pendientes":
            txt_cuerpo.value = "Se envía informe con algunos pendientes por validar."
        page.update()

    btn_row = ft.Row([
        ft.ElevatedButton("Finalizado", on_click=set_mensaje),
        ft.ElevatedButton("Pendientes", on_click=set_mensaje),
    ], alignment="center")

    # Función de Activación
    def ejecutar_envio(e):
        try:
            btn_activar.disabled = True
            btn_activar.text = "Enviando..."
            page.update()
            
            # Llamamos a la lógica del otro archivo
            enviar_correo_masivo(txt_correo.value, txt_pass.value, txt_cuerpo.value)
            
            page.snack_bar = ft.SnackBar(ft.Text("✅ ¡Informe enviado a los 5 jefes!"), bgcolor="green")
            page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {err}"), bgcolor="red")
            page.snack_bar.open = True
        finally:
            btn_activar.disabled = False
            btn_activar.text = "ACTIVAR ENVÍO AUTOMÁTICO"
            page.update()

    btn_activar = ft.FilledButton(
        "ACTIVAR ENVÍO AUTOMÁTICO", 
        icon=ft.icons.SEND, 
        on_click=ejecutar_envio,
        width=350
    )

    page.add(
        ft.Text("Automatización de Informes", size=24, weight="bold"),
        ft.Divider(),
        txt_correo,
        txt_pass,
        ft.Text("Mensajes Rápidos:"),
        btn_row,
        txt_cuerpo,
        ft.Divider(),
        btn_activar
    )

if __name__ == "_main_":
    ft.app(target=main)