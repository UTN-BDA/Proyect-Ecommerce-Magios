from app import create_app, db
from app.models import stock  # Asegurate de importar tus modelos
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = create_app()

with app.app_context():
    db.create_all()  # ✅ Esto crea las tablas si no existen

if __name__ == '__main__':
    """
    Server Startup
    """
    app.run(host="0.0.0.0", debug=False, port=5000)
