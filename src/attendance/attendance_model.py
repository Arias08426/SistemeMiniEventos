from dataclasses import dataclass
from typing import Optional

@dataclass
class Attendance:
    """Modelo de Inscripción"""
    id: Optional[int]
    user_id: int
    event_id: int
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id
        }
    
    @staticmethod
    def from_row(row):
        """Crea un Attendance desde una fila de BD"""
        return Attendance(
            id=row['id'],
            user_id=row['user_id'],
            event_id=row['event_id']
        )
