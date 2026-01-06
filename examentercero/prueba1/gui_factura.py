# gui_factura.py
import tkinter as tk
from tkinter import ttk, messagebox

from dao_product import ProductDAO
from dao_client import ClientDAO
from dao_bill import BillDAO

def round2(x: float) -> float:
    return round(x + 1e-12, 2)

class FacturaWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Factura")
        self.geometry("980x620")

        self.product_dao = ProductDAO()
        self.current_product = None

        # ====== Cliente ======
        frm_client = ttk.LabelFrame(self, text="Datos del cliente")
        frm_client.pack(fill="x", padx=10, pady=8)

        self.txtnombre = ttk.Entry(frm_client, width=30)
        self.txttelefono = ttk.Entry(frm_client, width=30)
        self.txtdireccion = ttk.Entry(frm_client, width=30)
        self.txtemail = ttk.Entry(frm_client, width=30)

        ttk.Label(frm_client, text="Nombre:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.txtnombre.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(frm_client, text="Teléfono:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.txttelefono.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(frm_client, text="Dirección:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.txtdireccion.grid(row=1, column=1, padx=6, pady=4)
        ttk.Label(frm_client, text="Email:").grid(row=1, column=2, sticky="w", padx=6, pady=4)
        self.txtemail.grid(row=1, column=3, padx=6, pady=4)

        # ====== Filtro producto ======
        frm_filter = ttk.LabelFrame(self, text="Buscar producto (MongoDB -> PRODUCT)")
        frm_filter.pack(fill="x", padx=10, pady=8)

        self.txtfiltroid = ttk.Entry(frm_filter, width=20)
        self.txtfiltronombre = ttk.Entry(frm_filter, width=25)

        ttk.Label(frm_filter, text="ID producto:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        self.txtfiltroid.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(frm_filter, text="Nombre producto:").grid(row=0, column=2, padx=6, pady=4, sticky="w")
        self.txtfiltronombre.grid(row=0, column=3, padx=6, pady=4)

        btn_mostrar = ttk.Button(frm_filter, text="Mostrar", command=self.on_mostrar_producto)
        btn_mostrar.grid(row=0, column=4, padx=10, pady=4)

        # ====== Detalle linea ======
        frm_line = ttk.LabelFrame(self, text="Detalle del ítem")
        frm_line.pack(fill="x", padx=10, pady=8)

        self.txtnumero = ttk.Entry(frm_line, width=10, state="readonly")
        self.txtproducto = ttk.Entry(frm_line, width=25, state="readonly")
        self.txtdescripcion = ttk.Entry(frm_line, width=30, state="readonly")

        self.txtcantidad_var = tk.StringVar()
        self.txtcantidad = ttk.Entry(frm_line, width=10, textvariable=self.txtcantidad_var)

        self.txtprecio = ttk.Entry(frm_line, width=12, state="readonly")

        self.txttotal_var = tk.StringVar()
        self.txttotal = ttk.Entry(frm_line, width=12, textvariable=self.txttotal_var, state="readonly")

        ttk.Label(frm_line, text="N°:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        self.txtnumero.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(frm_line, text="Producto:").grid(row=0, column=2, padx=6, pady=4, sticky="w")
        self.txtproducto.grid(row=0, column=3, padx=6, pady=4)
        ttk.Label(frm_line, text="Descripción:").grid(row=0, column=4, padx=6, pady=4, sticky="w")
        self.txtdescripcion.grid(row=0, column=5, padx=6, pady=4)

        ttk.Label(frm_line, text="Cantidad:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
        self.txtcantidad.grid(row=1, column=1, padx=6, pady=4)
        ttk.Label(frm_line, text="Precio Unit:").grid(row=1, column=2, padx=6, pady=4, sticky="w")
        self.txtprecio.grid(row=1, column=3, padx=6, pady=4)
        ttk.Label(frm_line, text="Total:").grid(row=1, column=4, padx=6, pady=4, sticky="w")
        self.txttotal.grid(row=1, column=5, padx=6, pady=4)

        self.txtcantidad_var.trace_add("write", lambda *_: self.update_line_total())

        btn_agregar = ttk.Button(frm_line, text="Agregar", command=self.on_agregar)
        btn_agregar.grid(row=1, column=6, padx=10, pady=4)

        # ====== Tabla ======
        frm_table = ttk.Frame(self)
        frm_table.pack(fill="both", expand=True, padx=10, pady=8)

        cols = ("numero", "producto", "descripcion", "cantidad", "precio", "total")
        self.tree = ttk.Treeview(frm_table, columns=cols, show="headings", height=10)
        for c, t in zip(cols, ["N°", "Producto", "Descripción", "Cantidad", "Precio Unit", "Total"]):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=120 if c in ("producto","descripcion") else 90, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # ====== Totales + Facturar ======
        frm_tot = ttk.LabelFrame(self, text="Totales")
        frm_tot.pack(fill="x", padx=10, pady=8)

        self.txtsubtotal_var = tk.StringVar()
        self.txtiva_var = tk.StringVar()
        self.txttotalneto_var = tk.StringVar()

        ttk.Label(frm_tot, text="SubTotal:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
        ttk.Entry(frm_tot, textvariable=self.txtsubtotal_var, state="readonly", width=15).grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(frm_tot, text="IVA (15%):").grid(row=0, column=2, padx=6, pady=4, sticky="w")
        ttk.Entry(frm_tot, textvariable=self.txtiva_var, state="readonly", width=15).grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(frm_tot, text="Total Neto:").grid(row=0, column=4, padx=6, pady=4, sticky="w")
        ttk.Entry(frm_tot, textvariable=self.txttotalneto_var, state="readonly", width=15).grid(row=0, column=5, padx=6, pady=4)

        btn_facturar = ttk.Button(frm_tot, text="Facturar", command=self.on_facturar)
        btn_facturar.grid(row=0, column=6, padx=10, pady=4)

        btn_salir = ttk.Button(frm_tot, text="Salir", command=self.on_salir)
        btn_salir.grid(row=0, column=7, padx=10, pady=4)

    # ---------- Helpers ----------
    def get_next_row_number(self) -> int:
        return len(self.tree.get_children()) + 1

    def set_entry(self, entry: ttk.Entry, value: str):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def update_line_total(self):
        try:
            qty = int(self.txtcantidad_var.get().strip() or "0")
            price = float(self.txtprecio.get().strip() or "0")
            total = round2(qty * price)
            self.txttotal_var.set(str(total) if qty > 0 else "")
        except Exception:
            self.txttotal_var.set("")

    def compute_subtotal(self) -> float:
        subtotal = 0.0
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, "values")
            if values and len(values) == 6:
                subtotal += float(values[5])
        subtotal = round2(subtotal)
        self.txtsubtotal_var.set(str(subtotal))
        return subtotal

    # ---------- Actions ----------
    def on_mostrar_producto(self):
        pid = self.txtfiltroid.get().strip()
        name = self.txtfiltronombre.get().strip()

        if not pid and not name:
            messagebox.showwarning("Validación", "Ingresa el ID o el Nombre del producto para buscar.")
            return

        try:
            if pid:
                doc = self.product_dao.find_by_product_id(pid)
            else:
                doc = self.product_dao.find_by_name(name)

            if not doc:
                messagebox.showinfo("Sin resultados", "No se encontró el producto en la base de datos.")
                self.current_product = None
                return

            self.current_product = doc

            self.set_entry(self.txtnumero, str(self.get_next_row_number()))
            self.set_entry(self.txtproducto, doc.get("name", ""))
            self.set_entry(self.txtdescripcion, doc.get("detail", ""))

            price = float(doc.get("price", 0))
            self.set_entry(self.txtprecio, str(price))

            self.txtcantidad_var.set("")
            self.txttotal_var.set("")

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar producto:\n{e}")
            self.current_product = None

    def on_agregar(self):
        if not self.current_product:
            messagebox.showwarning("Validación", "Primero debes buscar un producto con 'Mostrar'.")
            return

        try:
            numero = int(self.txtnumero.get().strip())
            producto = self.txtproducto.get().strip()
            descripcion = self.txtdescripcion.get().strip()
            cantidad = int(self.txtcantidad_var.get().strip())
            precio = float(self.txtprecio.get().strip())

            if cantidad <= 0:
                messagebox.showwarning("Validación", "La cantidad debe ser un entero mayor que 0.")
                return

            total = round2(cantidad * precio)
            self.txttotal_var.set(str(total))

            self.tree.insert("", "end", values=(numero, producto, descripcion, cantidad, precio, total))

            # recalcular subtotal (opcional)
            self.compute_subtotal()

            # limpiar área de línea
            self.current_product = None
            self.txtfiltroid.delete(0, tk.END)
            self.txtfiltronombre.delete(0, tk.END)
            self.set_entry(self.txtnumero, "")
            self.set_entry(self.txtproducto, "")
            self.set_entry(self.txtdescripcion, "")
            self.txtcantidad_var.set("")
            self.set_entry(self.txtprecio, "")
            self.txttotal_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser entero y Precio numérico.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar:\n{e}")

    def on_facturar(self):
        try:
            if len(self.tree.get_children()) == 0:
                messagebox.showwarning("Validación", "No hay productos agregados a la factura.")
                return

            cname = self.txtnombre.get().strip()
            cphone = self.txttelefono.get().strip()
            caddr = self.txtdireccion.get().strip()
            cemail = self.txtemail.get().strip()

            if not cname or not cphone or not caddr or not cemail:
                messagebox.showwarning("Validación", "Completa los datos del cliente antes de facturar.")
                return

            subtotal = self.compute_subtotal()
            iva = round2(subtotal * 0.15)
            total_neto = round2(subtotal + iva)

            self.txtiva_var.set(str(iva))
            self.txttotalneto_var.set(str(total_neto))

            # guardar cliente
            client_dao = ClientDAO()
            client_doc = client_dao.insert_client(cname, cphone, caddr, cemail)

            # items desde tabla
            items = []
            for item_id in self.tree.get_children():
                n, p, d, c, pr, t = self.tree.item(item_id, "values")
                items.append({
                    "numero": int(n),
                    "producto": p,
                    "descripcion": d,
                    "cantidad": int(c),
                    "precio": float(pr),
                    "total": float(t)
                })

            # guardar bill
            bill_dao = BillDAO()
            bill_id = bill_dao.insert_bill(client_doc, items, subtotal, iva, total_neto)

            messagebox.showinfo("Éxito", f"Factura guardada correctamente.\nBillID: {bill_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al facturar/guardar:\n{e}")

    def on_salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir del programa?"):
            self.destroy()
