from dataclasses import dataclass
from typing import Optional

@dataclass
class Event:
    """Modelo de Evento"""
    id: Optional[int]
    nombre: str
    fecha: str
    capacidad: int
    inscritos: int = 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'capacidad': self.capacidad,
            'inscritos': self.inscritos
        }
    
    @staticmethod
    def from_row(row):
        """Crea un Event desde una fila de BD"""
        return Event(
            id=row['id'],
            nombre=row['nombre'],
            fecha=row['fecha'],
            capacidad=row['capacidad'],
            inscritos=row['inscritos']
        )
