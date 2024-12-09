import flet as ft
from login import loginMenu  # Importa el UserControl de login
from crearusuarios import main   # Importa el UserControl de crear usuarios

def main(page: ft.Page):
    # Configuración inicial de la ventana
    page.window_min_height = 500
    page.window_min_width = 100
    page.window.center()
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    # Llama al formulario de login como pantalla inicial
    loginMenu.show_login(page)  # Muestra la interfaz de login en el primer inicio

# Llamar a la función main() solo una vez, iniciando la aplicación
ft.app(target=main)
