from waitress import serve
import sys
import os

# --- Configuración para usar settings de Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legajodedocentes.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# --- Ejecutar servidor ---
if __name__ == "__main__":
    print("Servidor corriendo en http://127.0.0.1:8000")
    serve(application, host="127.0.0.1", port=8000)
