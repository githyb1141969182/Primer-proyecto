from fpdf import FPDF 
import csv
import os
pdf=FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
archivo = 'datos.csv'

# Crear archivo con encabezado si no existe
if not os.path.exists(archivo):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['TIPO', 'CATEGORIA', 'MONTO'])

while True:
    try:
        tipo = int(input("Ingrese qué es (Gasto(0) - Ingreso(1) - Salir(2)): "))
        if tipo == 2:
            break
        if tipo not in [0, 1]:
            print("⚠️ Valor inválido.")
            continue

        categoria = input("Categoría: ")
        monto = float(input("Monto: "))
        fila = ['Gasto' if tipo == 0 else 'Ingreso', categoria, -abs(monto) if tipo == 0 else abs(monto)]

        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(fila)

    except ValueError:
        print("⚠️ Ingrese un número válido.")

# --- Resumen ---
ingresos = gastos = 0
with open(archivo, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        monto = float(row['MONTO'])
        ingresos += monto if row['TIPO'] == 'Ingreso' else 0
        gastos += monto if row['TIPO'] == 'Gasto' else 0


balance = ingresos + gastos
pdf.cell(200, 10, txt="Resumen de Ingresos y Gastos", ln=True, align='C')
pdf.cell(200, 10, txt=f"Ingresos: {ingresos:.2f}", ln=True, align='C')
pdf.cell(200, 10, txt=f"Gastos: {abs(gastos):.2f}", ln=True, align='C')
pdf.cell(200, 10, txt=f"Balance: {balance:.2f}", ln=True, align='C')
pdf_file = 'Resumen.pdf'
pdf.output(pdf_file)
print("\n📊 RESUMEN")
print(f"Ingresos: {ingresos:.2f}")
print(f"Gastos:   {abs(gastos):.2f}")
print(f"Balance:  {balance:.2f}")