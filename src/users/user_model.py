from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Modelo de Usuario"""
    id: Optional[int]
    nombre: str
    email: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email
        }
    
    @staticmethod
    def from_row(row):
        """Crea un User desde una fila de BD"""
        return User(
            id=row['id'],
            nombre=row['nombre'],
            email=row['email']
        )
