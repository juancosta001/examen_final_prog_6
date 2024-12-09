import sqlite3

class Productos:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("form_crud/datos.db", check_same_thread= False)

    def add_products(self,name,stock, costo, iva):
        query = ''' INSERT INTO productos(nombre, stock, costo, iva)
                    VALUES(?,?,?,?)    
'''
        self.connection.execute(query, (name, stock, costo, iva))
        self.connection.commit()

    def get_products(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM productos"
        cursor.execute(query)
        clientes = cursor.fetchall()
        return clientes

    def delete_products(self, product_id):
        query = "DELETE FROM productos WHERE idproductos = ?"
        self.connection.execute(query, (product_id,))
        self.connection.commit()


    def update_products(self,prod_id,name,stock, costo, iva):
        query = '''UPDATE productos SET nombre = ? , stock = ? , costo = ? , iva = ? WHERE idproductos = ?'''
        self.connection.execute(query, (name, stock, costo, iva, prod_id))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
    
