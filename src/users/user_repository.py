from typing import List, Optional
from src.users.user_model import User
from src.database.connection import Database
import sqlite3

class UserRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
    
    def find_all(self) -> List[User]:
        """Obtiene todos los usuarios"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        return [User.from_row(row) for row in rows]
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return User.from_row(row) if row else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        return User.from_row(row) if row else None
    
    def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (nombre, email) VALUES (?, ?)',
                (user.nombre, user.email)
            )
            self.conn.commit()
            user.id = cursor.lastrowid
            return user
        except sqlite3.IntegrityError:
            raise ValueError("El email ya está registrado")
    
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
