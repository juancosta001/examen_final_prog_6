import flet as ft
from usuarios import check_user  # Asumiendo que tienes esta función para verificar el usuario
from menu import formMenu  # Importa el menú principal
from crearusuarios import main as create_user  # Importa la función principal de crear usuarios

class loginMenu(ft.UserControl):
    def main(self, page: ft.Page):
        # Configuración inicial de la ventana
        page.window_min_height = 500
        page.window_min_width = 100
        page.window.center()
        page.padding = 0
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.email_value = ""
        page.password_value = ""

        def login(e):
            email = page.email_value.strip()  # Elimina espacios en blanco antes y después
            password = page.password_value.strip()

            if not email or not password:  # Verifica si algún campo está vacío
                show_error_dialog("Por favor, complete todos los campos.")
                return
            if check_user(email, password):  # Verificar usuario
                page.clean()  # Limpiar la página actual
                formMenu(page)  # Llamar al menú principal
                page.update()  # Actualizar la página
            else:
                show_error_dialog("Correo electrónico o contraseña incorrectos.")

        def show_error_dialog(message):
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(message),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())]
            )
            page.dialog = error_dialog
            page.dialog.open = True
            page.update()
        def close_dialog():
            page.dialog.open = False
            page.update()
        def redirect_to_create_account(e):
            page.clean()  # Limpiar la página antes de cargar el formulario de crear cuenta
            create_user(page)  # Llamar a la función principal del formulario de crear cuenta
            page.update()
        # Diseño del formulario de inicio de sesión centrado
        login_form = ft.Container(
            content=ft.Row([ 
                ft.Container(
                    content=ft.Column(controls=[ 
                        ft.Container(
                            content=ft.Image(
                                src='logo.png',
                                width=70,
                            ),
                            padding=ft.padding.only(150, 20)
                        ),
                        ft.Text(
                            'Iniciar Sesión',
                            width=360,
                            size=30,
                            weight='w900',
                            text_align='center',
                            color="white"
                        ),
                        ft.Container(
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text='Correo electrónico',
                                border='underline',
                                color='white',
                                prefix_icon=ft.icons.EMAIL,
                                on_change=lambda e: setattr(page, "email_value", e.control.value)
                            ),
                            padding=ft.padding.only(20, 10)
                        ),
                        ft.Container(
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text='Contraseña',
                                border='underline',
                                color='white',
                                prefix_icon=ft.icons.LOCK,
                                password=True,
                                on_change=lambda e: setattr(page, "password_value", e.control.value)
                            ),
                            padding=ft.padding.only(20, 10)
                        ),
                        ft.Container(
                            ft.Checkbox(
                                label='Recordar contraseña',
                                check_color='white',
                                label_style=ft.TextStyle(color="white")
                            ),
                            padding=ft.padding.only(40),
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                content=ft.Text(
                                    'INICIAR',
                                    color='black',
                                    weight='w500',
                                ),
                                width=280,
                                bgcolor='white',
                                on_click=login  # Llama a la función de inicio de sesión
                            ),
                            padding=ft.padding.only(25, 10)
                        ),
                        ft.Container(
                            ft.Row([ 
                                ft.Text('¿No tiene una cuenta?', color="white"),
                                ft.TextButton('Crear una cuenta', style=ft.ButtonStyle(color="white"), on_click=redirect_to_create_account),
                            ], spacing=8),
                            padding=ft.padding.only(40)
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    bgcolor="blue",
                    width=380,
                    height=460,
                    border_radius=20,
                    padding=20
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            padding=10,
        )

        # Contenedor principal con la imagen de fondo
        background = ft.Container(
            content=login_form,
            image_src="form_crud/fondoAzul.jpg",  # Ruta de la imagen de fondo
            image_fit=ft.ImageFit.COVER,  # Ajusta la imagen al tamaño del contenedor
            expand=True  # Expande el contenedor para cubrir toda la página
        )

        # Agregar el contenedor principal a la página
        page.add(background)

    @staticmethod
    def show_login(page):
        # Limpiar solo los controles del formulario de login, pero no el fondo
        for control in page.controls:
            if isinstance(control, ft.Container) and control.content:  # Eliminar solo los formularios
                page.controls.remove(control)
        
        login_menu = loginMenu()  # Crear una instancia de loginMenu
        login_menu.main(page)  # Llamar al método principal del loginMenu
        page.update()  # Actualizar la página
