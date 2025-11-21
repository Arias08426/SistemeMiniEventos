from typing import Dict
from src.attendance.attendance_model import Attendance
from src.attendance.attendance_repository import AttendanceRepository
from src.events.event_repository import EventRepository
from src.users.user_repository import UserRepository

class AttendanceService:
    """Servicio con lógica de negocio para inscripciones"""
    
    def __init__(
        self, 
        repository: AttendanceRepository,
        event_repository: EventRepository,
        user_repository: UserRepository,
        cache_service=None
    ):
        self.repository = repository
        self.event_repository = event_repository
        self.user_repository = user_repository
        self.cache_service = cache_service
    
    def register_user_to_event(self, user_id: int, event_id: int) -> Dict:
        """Inscribe un usuario a un evento"""
        
        # Verificar que el usuario existe
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Verificar que el evento existe
        event = self.event_repository.find_by_id(event_id)
        if not event:
            raise ValueError("Evento no encontrado")
        
        # Verificar que el evento no está lleno
        if event.inscritos >= event.capacidad:
            raise ValueError("El evento ya está lleno")
        
        # Verificar que el usuario no está ya inscrito
        existing = self.repository.find_by_user_and_event(user_id, event_id)
        if existing:
            raise ValueError("El usuario ya está inscrito en este evento")
        
        # Crear la inscripción
        attendance = Attendance(
            id=None,
            user_id=user_id,
            event_id=event_id
        )
        
        created = self.repository.create(attendance)
        
        # Incrementar el contador de inscritos del evento
        self.event_repository.increment_inscritos(event_id)
        
        # Invalidar caché del evento
        if self.cache_service:
            self.cache_service.invalidate(f'event_{event_id}')
        
        return created.to_dict()
