# gui_producto.py
import tkinter as tk
from tkinter import ttk, messagebox

from dao_product import ProductDAO
from gui_factura import FacturaWindow

class ProductoWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agregar Producto")
        self.geometry("520x300")

        self.dao = ProductDAO()

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frm, text="Nombre del producto:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Label(frm, text="Detalle del producto:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Label(frm, text="Stock ingresado:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Label(frm, text="Precio del producto:").grid(row=3, column=0, sticky="w", pady=6)

        self.txtnombre = ttk.Entry(frm, width=35)
        self.txtdetalle = ttk.Entry(frm, width=35)
        self.txtstock = ttk.Entry(frm, width=35)
        self.txtprecio = ttk.Entry(frm, width=35)

        self.txtnombre.grid(row=0, column=1, pady=6, padx=8)
        self.txtdetalle.grid(row=1, column=1, pady=6, padx=8)
        self.txtstock.grid(row=2, column=1, pady=6, padx=8)
        self.txtprecio.grid(row=3, column=1, pady=6, padx=8)

        btn = ttk.Button(frm, text="Guardar", command=self.on_guardar)
        btn.grid(row=4, column=0, columnspan=2, pady=18)

    def on_guardar(self):
        try:
            name = self.txtnombre.get().strip()
            detail = self.txtdetalle.get().strip()
            stock_txt = self.txtstock.get().strip()
            price_txt = self.txtprecio.get().strip()

            if not name or not detail or not stock_txt or not price_txt:
                messagebox.showwarning("Validación", "Completa todos los campos.")
                return

            stock = int(stock_txt)
            price = float(price_txt)

            if stock < 0 or price < 0:
                messagebox.showwarning("Validación", "Stock y precio no pueden ser negativos.")
                return

            new_id = self.dao.generate_next_product_id()

            ok = messagebox.askyesno(
                "Confirmación",
                f"El producto se guardará con el ID autogenerado:\n\n{new_id}\n\n¿Deseas continuar?"
            )
            if not ok:
                return

            self.dao.insert_product(new_id, name, detail, stock, price)

            messagebox.showinfo("Éxito", f"Producto guardado correctamente con ID: {new_id}")

            # Abrir Factura y cerrar Producto
            self.destroy()
            factura = FacturaWindow()
            factura.mainloop()

        except ValueError:
            messagebox.showerror("Error", "Stock debe ser entero y Precio numérico.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{e}")
