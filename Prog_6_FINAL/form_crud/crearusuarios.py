import flet as ft
import sqlite3
import re
def enable_wal_mode():
    try:
        with sqlite3.connect("form_crud/datos.db") as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
    except sqlite3.Error as e:
        print("Error al habilitar WAL mode:", e)

# Llama esta función al iniciar la aplicación
enable_wal_mode()


# Función para crear un nuevo usuario en la base de datos
def create_user(email, password):
    connection = None  # Define la conexión fuera del bloque try
    try:
        connection = sqlite3.connect("form_crud/datos.db")
        cursor = connection.cursor()

        query = "INSERT INTO usuarios (email, password) VALUES (?, ?)"
        cursor.execute(query, (email, password))

        connection.commit()
        return True
    except sqlite3.Error as e:
        print("Error al conectar con la base de datos:", e)
        return False
    finally:
        if connection:
            connection.close()  # Asegúrate de cerrar la conexión


# Función para validar el correo electrónico
def validate_email(email):
    # Expresión regular simple para verificar el formato del correo electrónico
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def main(page: ft.Page):
    # Configuración inicial de la ventana
    page.window_min_height = 500
    page.window_min_width = 100
    page.window.center()
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.email_value = ""
    page.password_value = ""
    page.confirm_password_value = ""

    def register_user(e):
        email = page.email_value
        password = page.password_value
        confirm_password = page.confirm_password_value

        # Validaciones
        if not email or not password or not confirm_password:
            show_error_dialog("Todos los campos son obligatorios.")
            return
        
        if not validate_email(email):
            show_error_dialog("El correo electrónico no es válido.")
            return

        if password != confirm_password:
            show_error_dialog("Las contraseñas no coinciden.")
            return

        if create_user(email, password):
            # Mostrar mensaje de éxito
            show_success_dialog("Usuario creado exitosamente.")
            
            # Vaciar los campos después de crear el usuario
            page.email_value = ""
            page.password_value = ""
            page.confirm_password_value = ""

            # Actualizar los campos visualmente
            for control in register_form.content.controls[0].content.controls:
                if isinstance(control, ft.Container) and isinstance(control.content, ft.TextField):
                    control.content.value = ""
            
            page.update()  # Refrescar la página para reflejar los cambios
        else:
            show_error_dialog("Error al crear el usuario. Intente nuevamente.")



    def show_error_dialog(message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())]
        )
        page.dialog = error_dialog
        page.dialog.open = True
        page.update()

    def show_success_dialog(message):
        success_dialog = ft.AlertDialog(
            title=ft.Text("Éxito"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())]
        )
        page.dialog = success_dialog
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def go_back_to_login(e):
        from login import loginMenu
        page.clean()  # Limpiar la página antes de agregar la nueva vista
        login_menu = loginMenu()  # Crear una instancia de loginMenu
        login_menu.main(page)  # Llamar al método principal del loginMenu
        page.update()

    # Diseño del formulario de registro de usuario
    register_form = ft.Container(
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
                        'Crear Cuenta',
                        width=360,
                        size=30,
                        weight='w900',
                        text_align='center',
                        color="White"
                    ),
                    ft.Container(
                        ft.TextField(
                            width=280,
                            height=40,
                            hint_text='Correo electrónico',
                            border='underline',
                            color='White',
                            prefix_icon=ft.icons.EMAIL,
                            on_change=lambda e: setattr(page, "email_value", e.control.value),
                            text_style=ft.TextStyle(color="White")  # Cambiar color del hint text
                        ),
                        padding=ft.padding.only(20, 10)
                    ),
                    ft.Container(
                        ft.TextField(
                            width=280,
                            height=40,
                            hint_text='Contraseña',
                            border='underline',
                            color='White',
                            prefix_icon=ft.icons.LOCK,
                            password=True,
                            on_change=lambda e: setattr(page, "password_value", e.control.value),
                            text_style=ft.TextStyle(color="White")  # Cambiar color del hint text
                        ),
                        padding=ft.padding.only(20, 10)
                    ),
                    ft.Container(
                        ft.TextField(
                            width=280,
                            height=40,
                            hint_text='Confirmar contraseña',
                            border='underline',
                            color='White',
                            prefix_icon=ft.icons.LOCK,
                            password=True,
                            on_change=lambda e: setattr(page, "confirm_password_value", e.control.value),
                            text_style=ft.TextStyle(color="White")  # Cambiar color del hint text
                        ),
                        padding=ft.padding.only(20, 10)
                    ),
                    ft.Container(
                        ft.ElevatedButton(
                            content=ft.Text('Registrarse', color='black'),
                            width=280,
                            bgcolor='White',
                            on_click=register_user
                        ),
                        padding=ft.padding.only(25, 10)
                    ),
                    # Nuevo botón para redirigir al login
                    ft.Row(
                        controls=[
                            ft.Text("¿Ya tienes una cuenta?"),
                            ft.TextButton('Iniciar Sesión', style=ft.ButtonStyle(color="white"), on_click=go_back_to_login),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER         
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                bgcolor="cyan",
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
        content=register_form,
        image_src="form_crud/fondoCeleste.jpg",  # Ruta de la imagen de fondo
        image_fit=ft.ImageFit.COVER,  # Ajusta la imagen al tamaño del contenedor
        expand=True  # Expande el contenedor para cubrir toda la página
    )

    # Agregar el contenedor principal a la página
    page.add(background)
