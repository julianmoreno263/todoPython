# Aquí ejecutamos la aplicación importando una instancia de la función create_app
from todor import create_app

# Creamos la instancia de la app de forma global para que Gunicorn la pueda ver
app = create_app()

# Punto de entrada para ejecución local
if __name__ == "__main__":
    import os
    # Render asigna un puerto dinámico en la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)