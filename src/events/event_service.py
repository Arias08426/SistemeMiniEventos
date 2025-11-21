from typing import List, Optional, Dict
from src.events.event_model import Event
from src.events.event_repository import EventRepository

class EventService:
    """Servicio con lógica de negocio para eventos"""
    
    def __init__(self, repository: EventRepository, cache_service=None):
        self.repository = repository
        self.cache_service = cache_service
    
    def get_all_events(self) -> List[Dict]:
        """Obtiene todos los eventos"""
        events = self.repository.find_all()
        return [event.to_dict() for event in events]
    
    def get_event_by_id(self, event_id: int) -> Optional[Dict]:
        """Obtiene un evento por ID (usa caché si está disponible)"""
        # Intentar obtener desde caché
        if self.cache_service:
            cached = self.cache_service.get(f'event_{event_id}')
            if cached:
                return cached
        
        # Si no está en caché, buscar en BD
        event = self.repository.find_by_id(event_id)
        if event:
            event_dict = event.to_dict()
            # Guardar en caché
            if self.cache_service:
                self.cache_service.set(f'event_{event_id}', event_dict)
            return event_dict
        return None
    
    def create_event(self, data: Dict) -> Dict:
        """Crea un nuevo evento"""
        # Validar capacidad
        if data.get('capacidad', 0) < 0:
            raise ValueError("La capacidad no puede ser negativa")
        
        event = Event(
            id=None,
            nombre=data['nombre'],
            fecha=data['fecha'],
            capacidad=data['capacidad'],
            inscritos=0
        )
        
        created = self.repository.create(event)
        return created.to_dict()
    
    def update_event(self, event_id: int, data: Dict) -> Optional[Dict]:
        """Actualiza un evento"""
        # Validar capacidad
        if data.get('capacidad', 0) < 0:
            raise ValueError("La capacidad no puede ser negativa")
        
        existing = self.repository.find_by_id(event_id)
        if not existing:
            return None
        
        # Actualizar campos
        existing.nombre = data.get('nombre', existing.nombre)
        existing.fecha = data.get('fecha', existing.fecha)
        existing.capacidad = data.get('capacidad', existing.capacidad)
        
        updated = self.repository.update(existing)
        
        # Invalidar caché
        if self.cache_service and updated:
            self.cache_service.invalidate(f'event_{event_id}')
        
        return updated.to_dict() if updated else None
    
    def delete_event(self, event_id: int) -> bool:
        """Elimina un evento si no tiene inscritos"""
        event = self.repository.find_by_id(event_id)
        
        if not event:
            return False
        
        # No permitir eliminar si tiene inscritos
        if event.inscritos > 0:
            raise ValueError("No se puede eliminar un evento con inscritos")
        
        deleted = self.repository.delete(event_id)
        
        # Invalidar caché
        if self.cache_service and deleted:
            self.cache_service.invalidate(f'event_{event_id}')
        
        return deleted
