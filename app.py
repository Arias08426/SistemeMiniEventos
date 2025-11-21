from flask import Flask, jsonify
from src.database.connection import Database
from src.cache.cache_service import CacheService

# Importar repositorios
from src.events.event_repository import EventRepository
from src.users.user_repository import UserRepository
from src.attendance.attendance_repository import AttendanceRepository

# Importar servicios
from src.events.event_service import EventService
from src.users.user_service import UserService
from src.attendance.attendance_service import AttendanceService

# Importar controladores
from src.events.event_controller import event_bp, init_event_controller
from src.users.user_controller import user_bp, init_user_controller
from src.attendance.attendance_controller import attendance_bp, init_attendance_controller

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['JSON_AS_ASCII'] = False
    
    # Inicializar base de datos
    db = Database()
    db.connect()
    
    # Inicializar caché
    cache_service = CacheService()
    
    # Inicializar repositorios
    event_repository = EventRepository()
    user_repository = UserRepository()
    attendance_repository = AttendanceRepository()
    
    # Inicializar servicios
    event_service = EventService(event_repository, cache_service)
    user_service = UserService(user_repository)
    attendance_service = AttendanceService(
        attendance_repository,
        event_repository,
        user_repository,
        cache_service
    )
    
    # Inicializar controladores
    init_event_controller(event_service)
    init_user_controller(user_service)
    init_attendance_controller(attendance_service)
    
    # Registrar blueprints
    app.register_blueprint(event_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(attendance_bp)
    
    # Ruta de bienvenida
    @app.route('/')
    def index():
        return jsonify({
            'message': 'FastEvents API',
            'version': '1.0',
            'endpoints': {
                'events': '/events',
                'users': '/users',
                'attendance': '/attendance'
            }
        })
    
    # Manejador de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 FastEvents API iniciada en http://localhost:5000")
    app.run(debug=True, port=5000)
