from flask import Blueprint, request, jsonify
from src.users.user_service import UserService

user_bp = Blueprint('users', __name__)

# Variable global para el servicio (se inyectará desde app.py)
user_service: UserService = None

def init_user_controller(service: UserService):
    """Inicializa el controlador con el servicio"""
    global user_service
    user_service = service

@user_bp.route('/users', methods=['GET'])
def get_users():
    """GET /users - Lista todos los usuarios"""
    users = user_service.get_all_users()
    return jsonify(users), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /users/{id} - Obtiene un usuario por ID"""
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    """POST /users - Crea un nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not all(k in data for k in ['nombre', 'email']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        user = user_service.create_user(data)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear usuario'}), 500
