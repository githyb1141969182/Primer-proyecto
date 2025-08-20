from flask import Flask, request
import csv
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configuración de Twilio
ACCOUNT_SID = "AC036510f7b8420c728002424ceebc8a0f"
AUTH_TOKEN = "d0a9db7276d73ae2d24146456f206284"
TWILIO_WHATSAPP = "whatsapp:+14155238886"  # Número oficial de Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

CSV_FILE = "registros.csv"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_incoming():
    remitente = request.form.get("From")    # Número de quien envía
    mensaje = request.form.get("Body")      # Contenido del mensaje
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Inicializar respuesta
    resp = MessagingResponse()

    try:
        # Esperamos el formato: Tipo;Monto;Descripcion
        tipo, monto, descripcion = mensaje.split(";")
        tipo = tipo.strip()
        descripcion = descripcion.strip()
        
        # Validar tipo
        if tipo not in ["Ingreso", "Egreso"]:
            resp.message("❌ Tipo inválido. Usar solo 'Ingreso' o 'Egreso'.")
            return str(resp), 200
        
        # Validar monto
        try:
            monto = float(monto.strip())
        except ValueError:
            resp.message("❌ Monto inválido. Debe ser un número.")
            return str(resp), 200
        
        # Guardar en CSV
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([fecha, remitente, tipo, monto, descripcion])
        
        # Confirmación al usuario
        resp.message(f"✅ Registro guardado:\nTipo: {tipo}\nMonto: {monto}\nDescripción: {descripcion}")

    except ValueError:
        resp.message("❌ Formato incorrecto. Usar: Tipo;Monto;Descripción")

    return str(resp), 200

if __name__ == "__main__":
    app.run(debug=True)
