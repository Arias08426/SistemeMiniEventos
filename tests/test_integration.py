import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from app import create_app
from src.database.connection import Database

@pytest.fixture(scope='function')
def client():
    """Crea un cliente de prueba para la aplicación"""
    app = create_app()
    app.config['TESTING'] = True
    
    # Obtener la instancia de BD y limpiar datos
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance')
    cursor.execute('DELETE FROM events')
    cursor.execute('DELETE FROM users')
    conn.commit()
    
    # Limpiar caché si existe
    from src.cache.cache_service import CacheService
    cache = CacheService()
    cache.clear()
    
    with app.test_client() as test_client:
        yield test_client
    
    # Limpiar después de la prueba
    cursor.execute('DELETE FROM attendance')
    cursor.execute('DELETE FROM events')
    cursor.execute('DELETE FROM users')
    conn.commit()

def test_full_flow_create_event_user_and_register(client):
    """Prueba de integración: flujo completo de creación y registro"""
    
    # 1. Crear un evento
    event_data = {
        'nombre': 'Conferencia de Python',
        'fecha': '2025-12-25',
        'capacidad': 100
    }
    response = client.post('/events', 
                          data=json.dumps(event_data),
                          content_type='application/json')
    assert response.status_code == 201
    event = json.loads(response.data)
    event_id = event['id']
    assert event['nombre'] == 'Conferencia de Python'
    assert event['inscritos'] == 0
    
    # 2. Crear un usuario
    user_data = {
        'nombre': 'Ana García',
        'email': 'ana@example.com'
    }
    response = client.post('/users',
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201
    user = json.loads(response.data)
    user_id = user['id']
    assert user['nombre'] == 'Ana García'
    
    # 3. Inscribir usuario al evento
    attendance_data = {
        'userId': user_id,
        'eventId': event_id
    }
    response = client.post('/attendance',
                          data=json.dumps(attendance_data),
                          content_type='application/json')
    assert response.status_code == 201
    attendance = json.loads(response.data)
    assert attendance['user_id'] == user_id
    assert attendance['event_id'] == event_id
    
    # 4. Verificar que el contador de inscritos aumentó
    response = client.get(f'/events/{event_id}')
    assert response.status_code == 200
    updated_event = json.loads(response.data)
    assert updated_event['inscritos'] == 1

def test_get_all_events(client):
    """Prueba: obtener lista de eventos"""
    # Crear algunos eventos
    event1 = {'nombre': 'Evento 1', 'fecha': '2025-12-01', 'capacidad': 50}
    event2 = {'nombre': 'Evento 2', 'fecha': '2025-12-05', 'capacidad': 30}
    
    client.post('/events', data=json.dumps(event1), content_type='application/json')
    client.post('/events', data=json.dumps(event2), content_type='application/json')
    
    # Obtener lista
    response = client.get('/events')
    assert response.status_code == 200
    events = json.loads(response.data)
    assert len(events) >= 2

def test_event_not_found(client):
    """Prueba: obtener evento inexistente retorna 404"""
    response = client.get('/events/9999')
    assert response.status_code == 404
    error = json.loads(response.data)
    assert 'error' in error

def test_update_event(client):
    """Prueba: actualizar evento"""
    # Crear evento
    event_data = {'nombre': 'Evento Original', 'fecha': '2025-12-10', 'capacidad': 40}
    response = client.post('/events', data=json.dumps(event_data), content_type='application/json')
    event = json.loads(response.data)
    event_id = event['id']
    
    # Actualizar
    update_data = {'nombre': 'Evento Modificado', 'capacidad': 60}
    response = client.put(f'/events/{event_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    updated = json.loads(response.data)
    assert updated['nombre'] == 'Evento Modificado'
    assert updated['capacidad'] == 60

def test_cannot_delete_event_with_attendees(client):
    """Prueba: no se puede eliminar evento con inscritos"""
    # Crear evento
    event_data = {'nombre': 'Evento', 'fecha': '2025-12-15', 'capacidad': 20}
    response = client.post('/events', data=json.dumps(event_data), content_type='application/json')
    event = json.loads(response.data)
    event_id = event['id']
    
    # Crear usuario
    user_data = {'nombre': 'Usuario', 'email': 'usuario@test.com'}
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    user = json.loads(response.data)
    
    # Inscribir
    attendance_data = {'userId': user['id'], 'eventId': event_id}
    client.post('/attendance', data=json.dumps(attendance_data), content_type='application/json')
    
    # Intentar eliminar
    response = client.delete(f'/events/{event_id}')
    assert response.status_code == 400
    error = json.loads(response.data)
    assert 'no se puede eliminar' in error['error'].lower()

def test_cache_working(client):
    """Prueba: verificar que el caché funciona"""
    # Crear evento
    event_data = {'nombre': 'Evento para Cache', 'fecha': '2025-12-20', 'capacidad': 15}
    response = client.post('/events', data=json.dumps(event_data), content_type='application/json')
    event = json.loads(response.data)
    event_id = event['id']
    
    # Primera consulta (se guarda en caché)
    response1 = client.get(f'/events/{event_id}')
    assert response1.status_code == 200
    
    # Segunda consulta (debería venir del caché)
    response2 = client.get(f'/events/{event_id}')
    assert response2.status_code == 200
    
    # Ambas respuestas deben ser idénticas
    assert response1.data == response2.data
