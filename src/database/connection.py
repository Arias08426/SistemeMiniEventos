import sqlite3
from typing import Optional

class Database:
    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self, db_path: str = 'fastevents.db'):
        """Establece conexión con la base de datos"""
        if self._connection is None:
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._create_tables()
        return self._connection
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna la conexión activa"""
        if self._connection is None:
            self.connect()
        return self._connection
    
    def _create_tables(self):
        """Crea las tablas si no existen"""
        cursor = self._connection.cursor()
        
        # Tabla events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                capacidad INTEGER NOT NULL,
                inscritos INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Tabla attendance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                event_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (event_id) REFERENCES events(id),
                UNIQUE(user_id, event_id)
            )
        ''')
        
        self._connection.commit()
    
    def close(self):
        """Cierra la conexión"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def reset(self):
        """Resetea la base de datos (útil para pruebas)"""
        cursor = self._connection.cursor()
        cursor.execute('DELETE FROM attendance')
        cursor.execute('DELETE FROM events')
        cursor.execute('DELETE FROM users')
        self._connection.commit()
