import csv
from fpdf import FPDF

class PDFConEncabezado(FPDF):
    def __init__(self, encabezados):
        super().__init__()
        self.encabezados = encabezados
        self.ancho_col = 190 / len(encabezados)

    def header(self):
        self.set_font("Arial", 'B', 12)
        for col in self.encabezados:
            self.cell(self.ancho_col, 10, col, border=1, align='C')
        self.ln()

def csv_a_pdf(nombre_csv, nombre_pdf):
    with open(nombre_csv, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv)
        filas = list(lector)

    if not filas:
        print("CSV vacío")
        return

    encabezados = ["Día y Hora", "Tipo", "Monto", "Categoría"]
    pdf = PDFConEncabezado(encabezados)
    pdf.add_page()
    pdf.set_font("Arial", '', 12)

    for fila in filas:
        for i, celda in enumerate(fila[:4]):  # Aseguramos solo 4 columnas
            pdf.cell(pdf.ancho_col, 10, str(celda), border=1, align='C')
        pdf.ln()

    pdf.output(nombre_pdf)
    print(f"PDF generado: {nombre_pdf}")
csv_a_pdf("registros.csv", "registros.pdf")
