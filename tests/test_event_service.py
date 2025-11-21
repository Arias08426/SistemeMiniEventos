import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.events.event_model import Event
from src.events.event_repository import EventRepository
from src.events.event_service import EventService
from src.cache.cache_service import CacheService
from src.database.connection import Database

@pytest.fixture
def setup_db():
    """Configura la base de datos para pruebas"""
    db = Database()
    db.connect('test_fastevents.db')
    db.reset()
    yield db
    db.close()
    # Limpiar archivo de prueba
    if os.path.exists('test_fastevents.db'):
        os.remove('test_fastevents.db')

@pytest.fixture
def event_service(setup_db):
    """Crea un servicio de eventos para pruebas"""
    repository = EventRepository()
    cache = CacheService()
    return EventService(repository, cache)

def test_create_event_success(event_service):
    """Prueba: crear evento exitosamente"""
    data = {
        'nombre': 'Conferencia Tech',
        'fecha': '2025-12-01',
        'capacidad': 100
    }
    
    event = event_service.create_event(data)
    
    assert event is not None
    assert event['nombre'] == 'Conferencia Tech'
    assert event['capacidad'] == 100
    assert event['inscritos'] == 0
    assert event['id'] is not None

def test_create_event_negative_capacity(event_service):
    """Prueba: no permitir capacidad negativa"""
    data = {
        'nombre': 'Evento Inválido',
        'fecha': '2025-12-01',
        'capacidad': -10
    }
    
    with pytest.raises(ValueError, match="La capacidad no puede ser negativa"):
        event_service.create_event(data)

def test_get_event_by_id(event_service):
    """Prueba: obtener evento por ID"""
    # Crear evento
    data = {
        'nombre': 'Workshop Python',
        'fecha': '2025-12-05',
        'capacidad': 50
    }
    created = event_service.create_event(data)
    
    # Obtener evento
    event = event_service.get_event_by_id(created['id'])
    
    assert event is not None
    assert event['nombre'] == 'Workshop Python'

def test_update_event(event_service):
    """Prueba: actualizar evento"""
    # Crear evento
    data = {
        'nombre': 'Seminario',
        'fecha': '2025-12-10',
        'capacidad': 30
    }
    created = event_service.create_event(data)
    
    # Actualizar
    update_data = {
        'nombre': 'Seminario Actualizado',
        'capacidad': 50
    }
    updated = event_service.update_event(created['id'], update_data)
    
    assert updated is not None
    assert updated['nombre'] == 'Seminario Actualizado'
    assert updated['capacidad'] == 50

def test_delete_event_without_attendees(event_service):
    """Prueba: eliminar evento sin inscritos"""
    # Crear evento
    data = {
        'nombre': 'Evento a Eliminar',
        'fecha': '2025-12-15',
        'capacidad': 20
    }
    created = event_service.create_event(data)
    
    # Eliminar
    result = event_service.delete_event(created['id'])
    
    assert result is True

def test_cannot_delete_event_with_attendees(event_service):
    """Prueba: no permitir eliminar evento con inscritos"""
    # Crear evento
    data = {
        'nombre': 'Evento con Inscritos',
        'fecha': '2025-12-20',
        'capacidad': 10
    }
    created = event_service.create_event(data)
    
    # Simular inscripción modificando directamente
    repository = EventRepository()
    repository.increment_inscritos(created['id'])
    
    # Intentar eliminar
    with pytest.raises(ValueError, match="No se puede eliminar un evento con inscritos"):
        event_service.delete_event(created['id'])
