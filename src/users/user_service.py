from typing import List, Optional, Dict
from src.users.user_model import User
from src.users.user_repository import UserRepository

class UserService:
    """Servicio con lógica de negocio para usuarios"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def get_all_users(self) -> List[Dict]:
        """Obtiene todos los usuarios"""
        users = self.repository.find_all()
        return [user.to_dict() for user in users]
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        user = self.repository.find_by_id(user_id)
        return user.to_dict() if user else None
    
    def create_user(self, data: Dict) -> Dict:
        """Crea un nuevo usuario"""
        # Validar que el email no esté repetido
        existing = self.repository.find_by_email(data['email'])
        if existing:
            raise ValueError("El email ya está registrado")
        
        user = User(
            id=None,
            nombre=data['nombre'],
            email=data['email']
        )
        
        created = self.repository.create(user)
        return created.to_dict()
