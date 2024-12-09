import flet as ft
from formclientes import ClientForm  # Asegúrate de que esta importación sea correcta
from formprod import ProdForm  # Asegúrate de que esta importación sea correcta
class formMenu(ft.UserControl):
    def __init__(self, page: ft.Page):
        # Configuración inicial de la ventana
        self.page = page
        self.page.title = "Menú Principal"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.scroll = "adaptive"
        self.page.window.min_height = 500
        self.page.window.min_width = 100
        self.page.window.center()
        self.page.window.resizable = True
        client_form = ClientForm(self.page)
        product_form = ProdForm(self.page)
        def show_clients(e):
            print("Redirigiendo a Clientes")
            self.page.clean()
            self.page.add(client_form.build())
        def show_products(e):
            print("Redirigiendo a Productos")
            self.page.clean()
            self.page.add(product_form.build())
        menu_form = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        'Menu Principal',
                        width=360,
                        size=30,
                        weight='w900',
                        text_align='center',
                        color="white"
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Clientes",
                                icon=ft.icons.PERSON,
                                on_click=show_clients,
                                expand=True,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),bgcolor=ft.colors.BLUE_100,
                                    color=ft.colors.BLACK,
                                ),
                            ),
                            ft.ElevatedButton(
                                text="Productos",
                                icon=ft.icons.SHOPPING_CART,
                                on_click=show_products,
                                expand=True,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),bgcolor=ft.colors.BLUE_100,
                                    color=ft.colors.BLACK,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,  
            ),
            bgcolor="blue", width=400, height=300,border_radius=20,padding=20,
        )

        # Fondo que ocupa toda la pantalla
        background = ft.Container(
            content=ft.Image(
                src="form_crud/fondoAzul.jpg",  # Ruta de la imagen de fondo
                fit=ft.ImageFit.COVER,  # Ajuste de la imagen
            ),
            expand=True,  # Expande el fondo para cubrir toda la página
        )

        # Contenedor para el fondo y el menú
        container_menu = ft.Container(
            content=menu_form,
            alignment=ft.Alignment(0.0, 0.0),  # Alineación centrada en ambos ejes
            expand=True,  # Permite que el contenedor se expanda para ocupar todo el espacio disponible
        )

        # Usamos un contenedor de tipo Stack para apilar el fondo y el menú con el gradiente debajo
        stack = ft.Stack(
            controls=[
                background,  # Fondo
                container_menu,  # Menú centrado 
            ],
            alignment=ft.Alignment(0.0, -0.5)  # Centrar el contenido en el Stack
        )

        # Añadimos el stack a la página
        self.page.add(stack)
