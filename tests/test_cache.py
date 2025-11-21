import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.cache.cache_service import CacheService

@pytest.fixture
def cache():
    """Crea un servicio de caché para pruebas (sin Redis, usa memoria)"""
    # Forzar uso de memoria para tests (Redis no disponible en CI/CD)
    cache_service = CacheService(redis_url='redis://localhost:9999')  # Puerto inválido
    cache_service.clear()  # Limpiar antes de cada test
    yield cache_service
    cache_service.clear()  # Limpiar después de cada test

def test_cache_set_and_get(cache):
    """Prueba: almacenar y recuperar del caché"""
    key = 'event_1'
    value = {'id': 1, 'nombre': 'Evento Test', 'capacidad': 100}
    
    cache.set(key, value)
    result = cache.get(key)
    
    assert result is not None
    assert result['id'] == 1
    assert result['nombre'] == 'Evento Test'

def test_cache_get_nonexistent_key(cache):
    """Prueba: obtener clave inexistente retorna None"""
    result = cache.get('nonexistent_key')
    assert result is None

def test_cache_invalidate(cache):
    """Prueba: invalidar caché elimina la entrada"""
    key = 'event_2'
    value = {'id': 2, 'nombre': 'Evento 2', 'capacidad': 50}
    
    cache.set(key, value)
    assert cache.has(key) is True
    
    cache.invalidate(key)
    assert cache.has(key) is False
    assert cache.get(key) is None

def test_cache_clear(cache):
    """Prueba: limpiar caché elimina todas las entradas"""
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    assert cache.has('key1') is True
    assert cache.has('key2') is True
    
    cache.clear()
    
    assert cache.has('key1') is False
    assert cache.has('key2') is False
    assert cache.has('key3') is False

def test_cache_has_method(cache):
    """Prueba: verificar existencia de clave"""
    key = 'test_key'
    
    assert cache.has(key) is False
    
    cache.set(key, 'test_value')
    assert cache.has(key) is True

def test_cache_overwrite_value(cache):
    """Prueba: sobrescribir valor en caché"""
    key = 'event_3'
    value1 = {'id': 3, 'nombre': 'Evento Original', 'capacidad': 30}
    value2 = {'id': 3, 'nombre': 'Evento Actualizado', 'capacidad': 50}
    
    cache.set(key, value1)
    assert cache.get(key)['nombre'] == 'Evento Original'
    
    cache.set(key, value2)
    assert cache.get(key)['nombre'] == 'Evento Actualizado'
    assert cache.get(key)['capacidad'] == 50
