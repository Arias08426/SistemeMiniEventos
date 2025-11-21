from typing import List, Optional
from src.attendance.attendance_model import Attendance
from src.database.connection import Database
import sqlite3

class AttendanceRepository:
    """Repositorio para operaciones CRUD de inscripciones"""
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
    
    def find_all(self) -> List[Attendance]:
        """Obtiene todas las inscripciones"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM attendance')
        rows = cursor.fetchall()
        return [Attendance.from_row(row) for row in rows]
    
    def find_by_user_and_event(self, user_id: int, event_id: int) -> Optional[Attendance]:
        """Verifica si un usuario ya está inscrito en un evento"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM attendance WHERE user_id = ? AND event_id = ?',
            (user_id, event_id)
        )
        row = cursor.fetchone()
        return Attendance.from_row(row) if row else None
    
    def create(self, attendance: Attendance) -> Attendance:
        """Crea una nueva inscripción"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO attendance (user_id, event_id) VALUES (?, ?)',
                (attendance.user_id, attendance.event_id)
            )
            self.conn.commit()
            attendance.id = cursor.lastrowid
            return attendance
        except sqlite3.IntegrityError:
            raise ValueError("El usuario ya está inscrito en este evento")
