from flask import Flask, request
import csv
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from fpdf import FPDF

app = Flask(__name__)

# --------------------
# Configuración Twilio
# --------------------
ACCOUNT_SID = "TU_ACCOUNT_SID"       # <- Aquí tu Account SID
AUTH_TOKEN = "TU_AUTH_TOKEN"         # <- Aquí tu Auth Token
TWILIO_WHATSAPP = "whatsapp:+TU_NUMERO_TWILIO"  # <- Número Twilio WhatsApp
client = Client(ACCOUNT_SID, AUTH_TOKEN)

CSV_FILE = "registros.csv"  # Archivo CSV

# --------------------
# Flask para WhatsApp
# --------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_incoming():
    request.form.get("From")
    mensaje = request.form.get("Body")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    resp = MessagingResponse()

    try:
        # Formato esperado: Tipo;Monto;Categoria
        tipo, monto, categoria = mensaje.split(";")
        tipo = tipo.strip()
        categoria = categoria.strip()
        
        if tipo not in ["Ingreso", "Egreso"]:
            resp.message("❌ Tipo inválido. Usar solo 'Ingreso' o 'Egreso'.")
            return str(resp), 200
        
        try:
            monto = float(monto.strip())
        except ValueError:
            resp.message("❌ Monto inválido. Debe ser un número.")
            return str(resp), 200
        
        # Guardar en CSV
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([fecha, tipo, monto, categoria])
        
        resp.message(f"✅ Registro guardado:\nTipo: {tipo}\nMonto: {monto}\nCategoría: {categoria}")

    except ValueError:
        resp.message("❌ Formato incorrecto. Usar: Tipo;Monto;Categoría")

    return str(resp), 200

# --------------------
# Función para PDF
# --------------------
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

# --------------------
# Ejecución Flask
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
csv_a_pdf("registros.csv", "registros.pdf")
