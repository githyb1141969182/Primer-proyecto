# Registro de Ingresos/Egresos vía WhatsApp

Este proyecto permite registrar ingresos y egresos directamente desde WhatsApp, guardándolos automáticamente en un archivo CSV y confirmando el registro al usuario. Está construido con **Python**, **Flask** y **Twilio WhatsApp API**.

---

## Tecnologías usadas

- **Python 3**: Lenguaje de programación principal.
- **Flask**: Framework web ligero para exponer rutas HTTP.
- **Twilio WhatsApp API**: Para enviar y recibir mensajes de WhatsApp.
- **CSV**: Archivo de texto para almacenar los registros.
- **ngrok** (opcional): Para exponer tu servidor Flask local a Internet y recibir mensajes desde Twilio Sandbox.

Instalación

Ejecutar el comando de clonación:

git clone https://github.com/githyb1141969182/Primer-proyecto.git


Este comando descargará todo el contenido del repositorio en una carpeta llamada Primer-proyecto.

Acceder al directorio del proyecto:

cd Primer-proyecto


Verificar las ramas disponibles:

git branch -a

Esto mostrará todas las ramas disponibles.

Cambiar a la rama específica:

git checkout d8d804963755406eb8a001cdc412a7b1271873c7

- Crear un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Instalar dependencias:

pip install flask twilio

Configuración de Twilio

Crear una cuenta en Twilio
.

Acceder al WhatsApp Sandbox en el panel de Twilio.

Configurar las credenciales en tu código:

ACCOUNT_SID = "TU_ACCOUNT_SID"       # <- Aquí va tu Account SID de Twilio
AUTH_TOKEN = "TU_AUTH_TOKEN"         # <- Aquí va tu Auth Token de Twilio
TWILIO_WHATSAPP = "whatsapp:+TU_NUMERO_TWILIO"  # <- Número oficial de Twilio WhatsApp


Copiar la URL pública de ngrok (opcional) en el campo de mensajes entrantes de Twilio Sandbox.

Ejecución

Ejecutar el servidor Flask:

python app.py


Si estás en local y quieres exponerlo a Twilio, ejecutar ngrok:

ngrok http 5000


Configurar la URL pública de ngrok en Twilio Sandbox para recibir mensajes.

Uso

Enviar un mensaje de WhatsApp al número del Twilio Sandbox con el siguiente formato:

Tipo;Monto;Descripción


Tipo: Ingreso o Egreso

Monto: Número decimal (ej: 1500.50)

Descripción: Texto explicativo del registro

Ejemplo:

Ingreso;5000;Venta de producto
Egreso;1200;Compra de insumos


El sistema responderá automáticamente confirmando el registro y lo guardará en registros.csv con fecha y número de remitente.


