import tkinter as tk
from tkinter import messagebox, ttk
import locale

#moneda COP
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

# Diccionario domicilios -------------------------------
barrios = {
    "17 DE DICIEMBRE": (7500, 8000),
    "20 DE JULIO": (7000, 8000),
    "ALCACERES": (7000, 7500),
    "ALFONSO LOPEZ": (6500, 7500),
    "ALMENDROS": (6500, 7000),
    "ALTOS DELICIA": (6500, 7000),
    "AV DEL RIO (DEPENDE)": (5500, 7500),
    "BAHIA CONCHA": (10000, 10000),
    "BALCONES": (3500, 3500),
    "BASTIDAS": (6500, 7500),
    "BAVARIA CONTRY": (7000, 8000),
    "CARIBE IN": (4000, 4500),
    "CENTRO (DEPENDE)": (8000, 10000),
    "CHIMILA": (6500, 7500),
    "CIUDADELA": (7500, 8500),
    "CEHOCA": (7500, 8500),
    "COCOS": (9000, 9000),
    "CUNDI": (7000, 7500),
    "DIVINO NIÑO 1": (7000, 7000),
    "DIVINO NIÑO 2": (8000, 8000),
    "ENSENADA JUAN 23": (6500, 7500),
    "GALICIA": (4500, 5500),
    "JARDIN": (6000, 6500),
    "LA 19": (7000, 8000),
    "LA SAMARIA": (4000, 5000),
    "LA TENERIA": (8500, 9000),
    "LIBERTADOR": (5000, 5500),
    "LUIS R CALVO": (6500, 7000),
    "MANZANARES": (8500, 9000),
    "MARIA CRISTINA": (7500, 8000),
    "MERCADO": (7500, 8000),
    "NACHO VIVES": (7500, 8500),
    "NOGALES": (5000, 6000),
    "NUEVA GALICIA": (5500, 6500),
    "OCEAN MALL": (7000, 8000),
    "OLIVOS": (6500, 7000),
    "ONDAS DEL CARIBE": (6500, 7500),
    "PANDO": (8000, 8000),
    "PANTANO": (6500, 7500),
    "PESCAITO": (7500, 8500),
    "PETROMIL": (3000, 4000),
    "PORVENIR": (6500, 7000),
    "QSP": (4000, 4500),
    "REPOSO": (5000, 6000),
    "SAN CARLOS": (4000, 4500),
    "SAN FERNANDO": (7000, 8000),
    "SAN PEDRO ALEJANDRINO": (5000, 6000),
    "SANTA FE": (5000, 6000),
    "SANTA LUCIA": (5000, 6000),
    "SANTA CATALINA": (7500, 8000),
    "SANTA RITA": (7500, 8000),
    "TAYRONA": (5500, 6500),
    "TERRITORAL": (7500, 8000),
    "TERRALOF": (5500, 6000),
    "VILLA DEL CARMEN": (7000, 8000),
    "VILLA LIBERTADOR": (4000, 4500),
    "VILLA OLIMPICA": (6500, 7500),
    "VILLA SARA": (4500, 5500),
    "ZONA 30": (8000, 8000),
    "ZONA CARCEL": (7000, 7500)
}
 #-----------------------------------------------------
 
def actualizar_valor_domicilio(event=None):
    barrio = combo_barrio.get()

    if barrio in barrios:
        min_valor, max_valor = barrios[barrio]

        # Verificarar tarifa está seleccionada
        if seleccion_tarifa.get() == "Mínima":
            entry_valor_domicilio.delete(0, tk.END)
            entry_valor_domicilio.insert(0, f"{min_valor:,.0f}")
        elif seleccion_tarifa.get() == "Máxima":
            entry_valor_domicilio.delete(0, tk.END)
            entry_valor_domicilio.insert(0, f"{max_valor:,.0f}")
    else:
        # Si el barrio no enlistado, ingresar el valor manualmente C:
        entry_valor_domicilio.delete(0, tk.END)
        entry_valor_domicilio.insert(0, "")

def capturar_datos():
    # Captura de datos desde la interfaz aca c:
    barrio = combo_barrio.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    valor_pedido = float(entry_valor_pedido.get().replace(",", ""))

    # Obtiene el valor del domicilio aca c:
    valor_domicilio = 0
    if barrio in barrios:
        min_valor, max_valor = barrios[barrio]
        if seleccion_tarifa.get() == "Mínima":
            valor_domicilio = min_valor
        elif seleccion_tarifa.get() == "Máxima":
            valor_domicilio = max_valor
    else:
        # barrio enlistado, toma valor manual! C:
        try:
            valor_domicilio = float(entry_valor_domicilio.get().replace(",", ""))
        except ValueError:
            messagebox.showwarning("Error", "Por favor ingrese un valor numérico válido para el domicilio.")
            return

    metodo_pago = combo_metodo_pago.get().lower()

    if metodo_pago == "efectivo":
        try:
            paga_con = float(entry_pago_con.get().replace(",", ""))
            total_a_pagar = valor_pedido + valor_domicilio
            if paga_con < total_a_pagar:
                messagebox.showwarning("Advertencia", "El pago es insuficiente para cubrir el pedido y domicilio.")
                vuelto = None
            else:
                vuelto = paga_con - total_a_pagar
        except ValueError:
            messagebox.showwarning("Error", "Por favor ingrese un valor numérico válido para el pago.")
            return
    else:
        paga_con = 0.0
        vuelto = None  

    total = valor_pedido + valor_domicilio
    extra = entry_extra.get()

    # resumen del pedido c:
    resultado = f"""
    ----- Resumen del Pedido ----- \n
    Barrio: {barrio}
    Dirección: {direccion}
    Teléfono: {telefono}
    Valor Domicilio: {locale.currency(valor_domicilio, grouping=True)}
    Método de Pago: {metodo_pago.capitalize()}
    Valor Pedido: {locale.currency(valor_pedido, grouping=True)}
    Total: {locale.currency(total, grouping=True)}
    Extra: {extra}
    """

    if metodo_pago == "efectivo" and vuelto is not None:
        resultado += f"\nPago con efectivo: {locale.currency(paga_con, grouping=True)}\nVuelto: {locale.currency(vuelto, grouping=True)}\n\n\n\n"

    # Muestra la información en el cuadro de mensaje
    messagebox.showinfo("Resumen del Pedido", resultado)

    # aca Imprimir si caundo sea necesario c:
    imprimir(resultado)

def imprimir(texto):
    """Imprime el texto en la impresora configurada, con saltos de línea adecuados."""
    try:
        import win32print
        import win32ui

        # Configuración del ancho de línea (hay que ajústarlo según el ancho de la impresora) c:
        ancho_linea = 1000

        def dividir_en_lineas(texto, ancho):
            """Divide un texto en líneas según el ancho especificado."""
            lineas = []
            while len(texto) > ancho:
                corte = texto[:ancho]
                lineas.append(corte)
                texto = texto[ancho:]
            lineas.append(texto)  
            return "\n".join(lineas)

        texto_formateado = dividir_en_lineas(texto, ancho_linea)

        # Enviar a la impresora
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)
        pdc.StartDoc("Pedido de Domicilio")
        pdc.StartPage()

        # Coordenadas iniciales
        x, y = 10, 10  # Ajusta las coordenadas según la impresora c:
        for linea in texto_formateado.split("\n"):
            pdc.TextOut(x, y, linea.strip())
            y += 30  # Salto entre líneas (aca lo ajustare dependiendo la impresora c: )
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

    except Exception as e:
        messagebox.showerror("Error de impresión", f"No se pudo imprimir el documento: {e}")


# Crear ventana 
root = tk.Tk()
root.title("Captura de Datos del Pedido")
root.geometry("500x400")  # tamaño para la ventana

# Estilos 
style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 12),
                padding=6)
style.configure("TLabel",
                font=("Helvetica", 10))

# Etiquetas y campos de entrada
tk.Label(root, text="Barrio:").grid(row=0, column=0, padx=10, pady=5)
combo_barrio = ttk.Combobox(root, values=list(barrios.keys()))
combo_barrio.grid(row=0, column=1, padx=10, pady=5)
combo_barrio.set("Seleccionar")
combo_barrio.bind("<<ComboboxSelected>>", actualizar_valor_domicilio)

tk.Label(root, text="Dirección:").grid(row=1, column=0, padx=10, pady=5)
entry_direccion = tk.Entry(root)
entry_direccion.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5)
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Valor del Pedido:").grid(row=3, column=0, padx=10, pady=5)
entry_valor_pedido = tk.Entry(root)
entry_valor_pedido.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Valor Domicilio:").grid(row=4, column=0, padx=10, pady=5)
entry_valor_domicilio = tk.Entry(root)
entry_valor_domicilio.grid(row=4, column=1, padx=10, pady=5)

seleccion_tarifa = ttk.Combobox(root, values=["Mínima", "Máxima"])
seleccion_tarifa.set("Mínima")
seleccion_tarifa.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Método de Pago:").grid(row=6, column=0, padx=10, pady=5)
combo_metodo_pago = ttk.Combobox(root, values=["Efectivo", "Tarjeta"])
combo_metodo_pago.set("Efectivo")
combo_metodo_pago.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Pago con:").grid(row=7, column=0, padx=10, pady=5)
entry_pago_con = tk.Entry(root)
entry_pago_con.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Extra:").grid(row=8, column=0, padx=10, pady=5)
entry_extra = tk.Entry(root)
entry_extra.grid(row=8, column=1, padx=10, pady=5)

# Botón para capturar datos e imprimir
btn_guardar = ttk.Button(root, text="Guardar y Imprimir", command=capturar_datos)
btn_guardar.grid(row=9, column=0, columnspan=2, pady=20)

root.mainloop()

