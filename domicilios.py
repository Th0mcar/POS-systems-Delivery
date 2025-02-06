import win32print
import win32ui
import tkinter as tk
from tkinter import messagebox, ttk
import locale
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='config/.env')

# Configuración de moneda COP
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

# Diccionario de barrios y precios cargado desde el archivo .env
barrios = {}
for key, value in os.environ.items():
    if key.startswith("BARRIO_"):
        nombre_barrio = key[7:].replace("_", " ")
        precios = tuple(map(int, value.split(",")))
        barrios[nombre_barrio] = precios


def actualizar_valor_domicilio(event=None):
    barrio = combo_barrio.get()

    if barrio in barrios:
        min_valor, max_valor = barrios[barrio]

        # Verificar tarifa seleccionada
        if seleccion_tarifa.get() == "Mínima":
            entry_valor_domicilio.delete(0, tk.END)
            entry_valor_domicilio.insert(0, f"{min_valor:,.0f}")
        elif seleccion_tarifa.get() == "Máxima":
            entry_valor_domicilio.delete(0, tk.END)
            entry_valor_domicilio.insert(0, f"{max_valor:,.0f}")
    else:
        # Si el barrio no está enlistado, ingresar el valor manualmente
        entry_valor_domicilio.delete(0, tk.END)
        entry_valor_domicilio.insert(0, "")


def capturar_datos():
    # Captura de datos desde la interfaz
    barrio = combo_barrio.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    valor_pedido = float(entry_valor_pedido.get().replace(",", ""))

    # Obtiene el valor del domicilio
    valor_domicilio = 0
    if barrio in barrios:
        min_valor, max_valor = barrios[barrio]
        if seleccion_tarifa.get() == "Mínima":
            valor_domicilio = min_valor
        elif seleccion_tarifa.get() == "Máxima":
            valor_domicilio = max_valor
    else:
        # Si el barrio no está enlistado, toma el valor manual
        try:
            valor_domicilio = float(
                entry_valor_domicilio.get().replace(",", ""))
        except ValueError:
            messagebox.showwarning(
                "Error", "Por favor ingrese un valor numérico válido para el domicilio.")
            return

    metodo_pago = combo_metodo_pago.get().lower()

    if metodo_pago == "efectivo":
        try:
            paga_con = float(entry_pago_con.get().replace(",", ""))
            total_a_pagar = valor_pedido + valor_domicilio
            if paga_con < total_a_pagar:
                messagebox.showwarning(
                    "Advertencia", "El pago es insuficiente para cubrir el pedido y domicilio.")
                vuelto = None
            else:
                vuelto = paga_con - total_a_pagar
        except ValueError:
            messagebox.showwarning(
                "Error", "Por favor ingrese un valor numérico válido para el pago.")
            return
    else:
        paga_con = 0.0
        vuelto = None

    total = valor_pedido + valor_domicilio
    extra = entry_extra.get()

    # Resumen del pedido
    resultado = f"""
    ----- Resumen del Pedido -----

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
        resultado += f"\nPago con efectivo: {locale.currency(paga_con, grouping=True)}\nVuelto: {
            locale.currency(vuelto, grouping=True)}\n\n\n\n"

    # Muestra la información en el cuadro de mensaje
    messagebox.showinfo("Resumen del Pedido", resultado)

    # Imprimir si es necesario
    imprimir(resultado)


def imprimir(texto):
    """Imprime el texto en la impresora configurada"""
    try:
        # Configuración ancho de línea (se ajusta según el ancho de la impresora) c:
        ancho_linea = 1000

        def dividir_en_lineas(texto, ancho):
            """Divide texto en líneas por ancho especificado."""
            lineas = []
            while len(texto) > ancho:
                corte = texto[:ancho]
                lineas.append(corte)
                texto = texto[ancho:]
            lineas.append(texto)
            return "\n".join(lineas)

        texto_formateado = dividir_en_lineas(texto, ancho_linea)

        # Enviar a la impresora c:
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
            # Salto entre líneas (se ajusta dependiendo de la impresora) c:
            y += 30
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

    except Exception as e:
        messagebox.showerror("Error de impresión",
                             f"No se pudo imprimir el documento: {e}")


# Crear ventana
root = tk.Tk()
root.title("Captura de Datos del Pedido")
root.geometry("500x400")  # Tamaño de la ventana

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

# Botón de captura de datos e imprimir :o
btn_guardar = ttk.Button(
    root, text="Guardar y Imprimir", command=capturar_datos)
btn_guardar.grid(row=9, column=0, columnspan=2, pady=20)

root.mainloop()
