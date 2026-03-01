"""
Aplicación Flask simple para demostración de contenerización con Docker.
"""

from flask import Flask, jsonify

# Crear instancia de la aplicación Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """
    Ruta raíz que responde con un mensaje de saludo.
    
    Returns:
        dict: Mensaje de saludo en formato JSON
    """
    return jsonify({
        'message': '¡Hola desde Flask en Docker!',
        'status': 'success'
    }), 200


@app.route('/api/info')
def info():
    """
    Ruta adicional que proporciona información de la aplicación.
    
    Returns:
        dict: Información de la aplicación en formato JSON
    """
    return jsonify({
        'app_name': 'Flask Docker Application',
        'version': '1.0.0',
        'environment': 'containerized'
    }), 200


@app.route('/health')
def health_check():
    """
    Ruta de verificación de salud para comprobar que la app está funcionando.
    
    Returns:
        dict: Estado de salud de la aplicación
    """
    return jsonify({
        'status': 'healthy',
        'message': 'La aplicación está funcionando correctamente'
    }), 200


if __name__ == '__main__':
    # Ejecutar la app en modo debug en desarrollo
    # En producción en Docker, se usará en modo no-debug
    app.run(host='0.0.0.0', port=5000, debug=False)
