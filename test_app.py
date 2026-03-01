"""
Pruebas unitarias para la aplicación Flask usando pytest.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """
    Fixture que proporciona un cliente de prueba para la aplicación Flask.
    
    Yields:
        FlaskClient: Cliente para hacer peticiones a la aplicación
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHelloRoute:
    """Pruebas para la ruta raíz (/) de la aplicación."""
    
    def test_hello_status_code(self, client):
        """
        Verifica que la ruta raíz responde con código 200.
        
        Args:
            client: Cliente de prueba fixture
        """
        response = client.get('/')
        assert response.status_code == 200
    
    def test_hello_message_content(self, client):
        """
        Verifica que el mensaje de respuesta es el esperado.
        
        Args:
            client: Cliente de prueba fixture
        """
        response = client.get('/')
        data = response.get_json()
        
        assert data is not None
        assert 'message' in data
        assert data['message'] == '¡Hola desde Flask en Docker!'
        assert data['status'] == 'success'


class TestInfoRoute:
    """Pruebas para la ruta /api/info."""
    
    def test_info_status_code(self, client):
        """Verifica que la ruta /api/info responde con código 200."""
        response = client.get('/api/info')
        assert response.status_code == 200
    
    def test_info_content(self, client):
        """Verifica que la ruta /api/info devuelve los datos esperados."""
        response = client.get('/api/info')
        data = response.get_json()
        
        assert data is not None
        assert 'app_name' in data
        assert 'version' in data
        assert 'environment' in data
        assert data['environment'] == 'containerized'


class TestHealthRoute:
    """Pruebas para la ruta /health."""
    
    def test_health_check_status_code(self, client):
        """Verifica que la ruta /health responde con código 200."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_check_content(self, client):
        """Verifica que el estado de salud es correctamente reportado."""
        response = client.get('/health')
        data = response.get_json()
        
        assert data is not None
        assert data['status'] == 'healthy'
