import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.attendance.attendance_repository import AttendanceRepository
from src.attendance.attendance_service import AttendanceService
from src.events.event_repository import EventRepository
from src.events.event_model import Event
from src.users.user_repository import UserRepository
from src.users.user_model import User
from src.cache.cache_service import CacheService
from src.database.connection import Database

@pytest.fixture
def setup_db():
    """Configura la base de datos para pruebas"""
    db = Database()
    db.connect('test_attendance.db')
    db.reset()
    yield db
    db.close()
    if os.path.exists('test_attendance.db'):
        os.remove('test_attendance.db')

@pytest.fixture
def attendance_service(setup_db):
    """Crea un servicio de inscripciones para pruebas"""
    attendance_repo = AttendanceRepository()
    event_repo = EventRepository()
    user_repo = UserRepository()
    cache = CacheService()
    return AttendanceService(attendance_repo, event_repo, user_repo, cache)

@pytest.fixture
def sample_user_and_event(setup_db):
    """Crea un usuario y evento de prueba"""
    user_repo = UserRepository()
    event_repo = EventRepository()
    
    user = User(id=None, nombre='Juan Pérez', email='juan@test.com')
    created_user = user_repo.create(user)
    
    event = Event(id=None, nombre='Evento Test', fecha='2025-12-01', capacidad=10, inscritos=0)
    created_event = event_repo.create(event)
    
    return created_user.id, created_event.id

def test_register_user_to_event_success(attendance_service, sample_user_and_event):
    """Prueba: inscribir usuario exitosamente"""
    user_id, event_id = sample_user_and_event
    
    attendance = attendance_service.register_user_to_event(user_id, event_id)
    
    assert attendance is not None
    assert attendance['user_id'] == user_id
    assert attendance['event_id'] == event_id

def test_cannot_register_user_twice(attendance_service, sample_user_and_event):
    """Prueba: no permitir doble inscripción"""
    user_id, event_id = sample_user_and_event
    
    # Primera inscripción
    attendance_service.register_user_to_event(user_id, event_id)
    
    # Intentar segunda inscripción
    with pytest.raises(ValueError, match="El usuario ya está inscrito en este evento"):
        attendance_service.register_user_to_event(user_id, event_id)

def test_cannot_register_to_full_event(attendance_service, setup_db):
    """Prueba: no permitir inscripción en evento lleno"""
    user_repo = UserRepository()
    event_repo = EventRepository()
    
    # Crear usuario
    user = User(id=None, nombre='María López', email='maria@test.com')
    created_user = user_repo.create(user)
    
    # Crear evento con capacidad 0
    event = Event(id=None, nombre='Evento Lleno', fecha='2025-12-05', capacidad=0, inscritos=0)
    created_event = event_repo.create(event)
    
    # Intentar inscribir
    with pytest.raises(ValueError, match="El evento ya está lleno"):
        attendance_service.register_user_to_event(created_user.id, created_event.id)

def test_cannot_register_nonexistent_user(attendance_service, setup_db):
    """Prueba: no permitir inscribir usuario inexistente"""
    event_repo = EventRepository()
    
    event = Event(id=None, nombre='Evento', fecha='2025-12-10', capacidad=10, inscritos=0)
    created_event = event_repo.create(event)
    
    # Intentar inscribir usuario inexistente
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        attendance_service.register_user_to_event(9999, created_event.id)

def test_cannot_register_to_nonexistent_event(attendance_service, setup_db):
    """Prueba: no permitir inscribir a evento inexistente"""
    user_repo = UserRepository()
    
    user = User(id=None, nombre='Pedro Gómez', email='pedro@test.com')
    created_user = user_repo.create(user)
    
    # Intentar inscribir a evento inexistente
    with pytest.raises(ValueError, match="Evento no encontrado"):
        attendance_service.register_user_to_event(created_user.id, 9999)

def test_increment_inscritos_after_registration(attendance_service, sample_user_and_event):
    """Prueba: verificar que se incrementa el contador de inscritos"""
    user_id, event_id = sample_user_and_event
    
    event_repo = EventRepository()
    event_before = event_repo.find_by_id(event_id)
    inscritos_before = event_before.inscritos
    
    # Inscribir usuario
    attendance_service.register_user_to_event(user_id, event_id)
    
    # Verificar incremento
    event_after = event_repo.find_by_id(event_id)
    assert event_after.inscritos == inscritos_before + 1
