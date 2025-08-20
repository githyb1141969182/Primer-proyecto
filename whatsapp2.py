from flask import Flask, request
import csv
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

# --------------------
# Configuración Twilio
# --------------------
ACCOUNT_SID = ""       # <- Aquí tu Account SID
AUTH_TOKEN = ""         # <- Aquí tu Auth Token
TWILIO_WHATSAPP = "whatsapp:+"  # <- Número Twilio WhatsApp
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
# Ejecución Flask
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
