from typing import List, Optional
from src.events.event_model import Event
from src.database.connection import Database

class EventRepository:
    """Repositorio para operaciones CRUD de eventos"""
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
    
    def find_all(self) -> List[Event]:
        """Obtiene todos los eventos"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM events')
        rows = cursor.fetchall()
        return [Event.from_row(row) for row in rows]
    
    def find_by_id(self, event_id: int) -> Optional[Event]:
        """Obtiene un evento por ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        return Event.from_row(row) if row else None
    
    def create(self, event: Event) -> Event:
        """Crea un nuevo evento"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO events (nombre, fecha, capacidad, inscritos) VALUES (?, ?, ?, ?)',
            (event.nombre, event.fecha, event.capacidad, event.inscritos)
        )
        self.conn.commit()
        event.id = cursor.lastrowid
        return event
    
    def update(self, event: Event) -> Optional[Event]:
        """Actualiza un evento existente"""
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE events SET nombre = ?, fecha = ?, capacidad = ?, inscritos = ? WHERE id = ?',
            (event.nombre, event.fecha, event.capacidad, event.inscritos, event.id)
        )
        self.conn.commit()
        return event if cursor.rowcount > 0 else None
    
    def delete(self, event_id: int) -> bool:
        """Elimina un evento"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def increment_inscritos(self, event_id: int) -> bool:
        """Incrementa el contador de inscritos"""
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE events SET inscritos = inscritos + 1 WHERE id = ?',
            (event_id,)
        )
        self.conn.commit()
        return cursor.rowcount > 0
