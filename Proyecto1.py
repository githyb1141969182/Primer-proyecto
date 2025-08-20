import csv
import os
from datetime import datetime
from fpdf import FPDF

archivo = 'datos.csv'

# Crear CSV con encabezado si no existe
if not os.path.exists(archivo):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['FECHA_HORA', 'TIPO', 'CATEGORIA', 'MONTO'])

while True:
    try:
        tipo = int(input("Ingrese qué es (Gasto(0) - Ingreso(1) - Salir(2)): "))
        if tipo == 2:
            print("Saliendo del programa...")
            break
        if tipo not in [0, 1]:
            print("⚠️ Valor inválido.")
            continue

        categoria = input("Categoría: ")
        monto = float(input("Monto: "))

        # Fecha y hora actual
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        fila = ['Gasto' if tipo==0 else 'Ingreso',
                categoria,
                -abs(monto) if tipo==0 else abs(monto)]

        # Guardar fila con fecha y hora
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([fecha_hora] + fila)

    except ValueError:
        print("⚠️ Ingrese un valor numérico válido.")


pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Título
pdf.cell(0, 10, "RESUMEN DE GASTOS", ln=1, align="C")
pdf.ln(5)

# Encabezado de tabla
pdf.cell(50, 10, "FECHA_HORA", border=1)
pdf.cell(50, 10, "TIPO", border=1)
pdf.cell(50, 10, "CATEGORIA", border=1)
pdf.cell(40, 10, "MONTO", border=1, ln=1)

# Leer CSV y llenar tabla
ingresos = 0
gastos = 0
with open('datos.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pdf.cell(50, 10, row['FECHA_HORA'], border=1)
        pdf.cell(50, 10, row['TIPO'], border=1)
        pdf.cell(50, 10, row['CATEGORIA'], border=1)
        pdf.cell(40, 10, f"${float(row['MONTO']):.2f}", border=1, ln=1)

        # Acumular totales
        if row['TIPO'] == 'Ingreso':
            ingresos += float(row['MONTO'])
        else:
            gastos += float(row['MONTO'])

balance = ingresos + gastos

# Totales al final
pdf.ln(5)
pdf.cell(50, 10, "", border=1)
pdf.cell(50, 10, "TOTAL INGRESOS", border=1)
pdf.cell(50, 10, "", border=1)
pdf.cell(40, 10, f"${ingresos:.2f}", border=1, ln=1)

pdf.cell(50, 10, "", border=1)
pdf.cell(50, 10, "TOTAL GASTOS", border=1)
pdf.cell(50, 10, "", border=1)
pdf.cell(40, 10, f"${abs(gastos):.2f}", border=1, ln=1)

pdf.cell(50, 10, "", border=1)
pdf.cell(50, 10, "BALANCE", border=1)
pdf.cell(50, 10, "", border=1)
pdf.cell(40, 10, f"${balance:.2f}", border=1, ln=1)

pdf.output("resumen.pdf")
print("PDF generado: resumen.pdf")
