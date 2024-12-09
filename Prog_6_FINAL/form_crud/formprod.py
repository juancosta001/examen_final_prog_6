import flet as ft
from productos import Productos
import pandas as pd
from fpdf import FPDF
import datetime

class ProdForm(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.data = Productos()  # Base de datos de producto
        self.selected__row = None  # Almacena la fila seleccionada para editar o borrar
        # Campos de entrada para los datos del producto
        self.name = ft.TextField(label="Nombre", border_color="blue")
        self.stock = ft.TextField(
            label="stock",
            border_color="blue",
            input_filter=ft.NumbersOnlyInputFilter(),  # Solo permite números
            max_length=3  # Limita la longitud a 2 caracteres
        )
        self.costo = ft.TextField(label="Costo", border_color="blue")
        self.iva = ft.RadioGroup(content=ft.Row([
                    ft.Radio(value="10", label="10%"),ft.Radio(value="5", label="5%"), ]))
        self.alert_dialog = ft.AlertDialog() # Diálogo de alerta para mostrar mensajes de error
        self.search_filed = ft.TextField(  # Campo de búsqueda para filtrar productos por nombre
            label="Buscar por nombre",
            suffix_icon=ft.icons.SEARCH,
            border=ft.InputBorder.UNDERLINE,
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            on_change=self.search_data,  # Llama a `search_data` en cada cambio
        )
        self.data_table = ft.DataTable(    # Configuración de la tabla de productos con columnas personalizadas
            expand=True,
            border=ft.border.all(2, "blue"),
            data_row_color={ft.MaterialState.SELECTED: "blue", ft.MaterialState.PRESSED: "black"},
            border_radius=10,
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("Nombre", color="blue", weight="bold")),
                ft.DataColumn(ft.Text("Stock", color="blue", weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Costo", color="blue", weight="bold")),
                ft.DataColumn(ft.Text("Iva", color="blue", weight="bold")),
            ]
        )
       
        self.show_data()  # Muestra los datos actuales en la tabla     
        self.form = ft.Container(    # Contenedor del formulario de entrada
            bgcolor="#222222",border_radius=10,col=4,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Ingrese el producto", size=40, text_align="center", font_family="roboto"), self.name, self.stock, self.costo, self.iva,
                    ft.Container( # Botones de acción: Guardar, Actualizar y Borrar
                        content=ft.Row(
                            controls=[
                                ft.TextButton(text="Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.add_data),
                                ft.TextButton(text="Actualizar", icon=ft.icons.UPDATE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.update_data),
                                ft.TextButton(text="Borrar", icon=ft.icons.DELETE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.delete_data)
                            ]
                        )
                    )
                ]
            )
        )
        self.table = ft.Container(  # Contenedor de la tabla y los botones de búsqueda/exportación
            bgcolor="#222222",border_radius=10,col=8,padding=10,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[ self.search_filed,
                                ft.IconButton(tooltip="Editar", icon=ft.icons.EDIT, icon_color="white", on_click=self.edit_filed_text),
                                ft.IconButton(tooltip="Descargar en PDF", icon=ft.icons.PICTURE_AS_PDF, icon_color="white", on_click=self.save_pdf),
                                ft.IconButton(tooltip="Descargar en EXCEL", icon=ft.icons.SAVE_ALT, icon_color="white", on_click=self.save_excel),
                                ft.IconButton(
                                    tooltip="Volver",
                                    icon=ft.icons.ARROW_BACK,  # Icono de flecha hacia atrás
                                    icon_color="white",
                                    on_click=self.go_back_to_menu  # Define el evento del botón
                                )
                            ]
                        )
                    ), ft.Column(expand=True, scroll="auto", controls=[ft.ResponsiveRow([self.data_table])])
                ]
            )
        )

        
        self.conent = ft.ResponsiveRow(controls=[self.form, self.table]) # Distribución general de la interfaz en una fila responsiva
    def show_alert(self, message):
        self.alert_dialog.content = ft.Text(message)
        self.page.dialog = self.alert_dialog
        self.alert_dialog.open = True
        self.page.update()

    def show_data(self):
        self.data_table.rows = []
        for x in self.data.get_products():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(x[1])),  ft.DataCell(ft.Text(str(x[2]))),  # Nombre y  stock
                        ft.DataCell(ft.Text(x[3])), ft.DataCell(ft.Text(str(x[4])))   # costo y iva
                    ]
                )
            )
        self.page.update()
    def add_data(self, e):
        name = self.name.value
        stock = str(self.stock.value)
        costo = self.costo.value
        iva = self.iva.value
        # Validación: Verificar si todos los campos están rellenados y si el IVA fue seleccionado
        if not name or not stock or not costo or not iva:
            self.show_alert("Todos los campos son obligatorios. Por favor, complete todos los campos.")
            return  
        if iva not in ["10", "5", "0"]:  # Validación: Verificar si el IVA fue seleccionado
            self.show_alert("Debe seleccionar una opción de IVA.")
            return
        prod_exist = False   # Validar que el producto no exista
        for row in self.data.get_products():
            if row[1] == name:
                prod_exist = True
                break
        if not prod_exist:
            self.limpiador()
            self.data.add_products(name, stock, costo, iva)
            self.show_data()
        else:
            self.show_alert("El producto ya existe.")

    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True
        name = e.control.cells[0].content.value
        for row in self.data.get_products():
            if row[1] == name:
                self.selected__row = row
                break
        self.page.update()

    def edit_filed_text(self, e):
        try:
            self.name.value = self.selected__row[1]
            self.stock.value = self.selected__row[2]
            self.costo.value = self.selected__row[3]
            # Establecer el valor del IVA en el RadioGroup basado en el IVA del producto
            self.iva.value = self.selected__row[4]
            self.page.update()
        except TypeError:
            self.show_alert("Seleccione un producto para editar.")

    def update_data(self, e):
        if self.selected__row:
            name = self.name.value
            stock = str(self.stock.value)
            costo = self.costo.value
            iva = self.iva.value

            # Validación: Verificar si todos los campos están rellenados y si el IVA fue seleccionado
            if not name or not stock or not costo or not iva:
                self.show_alert("Todos los campos son obligatorios. Por favor, complete todos los campos.")
                return

            # Realizar la actualización
            self.limpiador()
            self.data.update_products(self.selected__row[0], name, stock, costo, iva)
            self.show_data()
        else:
            self.show_alert("Seleccione un producto para actualizar.")

    def search_data(self, e):
        search = self.search_filed.value.lower()
        name = list(filter(lambda x: search in x[1].lower(), self.data.get_products()))
        self.data_table.rows = []
        if self.search_filed.value:
            if len(name) > 0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,
                            cells=[
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(str(x[2]))),
                                ft.DataCell(ft.Text(x[3])),
                                ft.DataCell(ft.Text(str(x[4]))),
                            ]
                        )
                    )
                self.page.update()
            else:
                self.show_alert("No se encontraron resultados.")
        else:
            self.show_data()
    def delete_data(self, e):
        if self.selected__row:
            product_id = self.selected__row[0]
            self.data.delete_products(product_id)
            self.limpiador()
            self.show_data()
            self.selected__row = None
        else:
            self.show_alert("Seleccione un cliente para borrar.")
    def limpiador(self):
        self.name.value = ""
        self.stock.value = ""
        self.costo.value = ""
        self.iva.value = "10"  # Resetea el IVA al valor predeterminado 10



    def save_pdf(self, e):
        pdf = FPDF()
        pdf.add_page()
        column_widths = [10, 40, 20, 80, 40]
        data = self.data.get_products()
        header = ("ID", "NOMBRE", "STOCK", "COSTO", "IVA")
        data.insert(0, header)
        for row in data:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

    def go_back_to_menu(self, e):
        from menu import formMenu
        print("Volviendo al menú principal...")
        self.page.clean()
        formMenu(self.page)
        self.page.update

    def save_excel(self, e):
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        contacts = self.data.get_products()
        df = pd.DataFrame(contacts, columns=["ID", "Nombre", "Edad", "Correo", "Teléfono"])
        df.to_excel(file_name, index=False)

    def build(self):
        return self.conent
