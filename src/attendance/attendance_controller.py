from flask import Blueprint, request, jsonify
from src.attendance.attendance_service import AttendanceService

attendance_bp = Blueprint('attendance', __name__)

# Variable global para el servicio (se inyectará desde app.py)
attendance_service: AttendanceService = None

def init_attendance_controller(service: AttendanceService):
    """Inicializa el controlador con el servicio"""
    global attendance_service
    attendance_service = service

@attendance_bp.route('/attendance', methods=['POST'])
def register_attendance():
    """POST /attendance - Inscribe un usuario a un evento"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not all(k in data for k in ['userId', 'eventId']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        attendance = attendance_service.register_user_to_event(
            data['userId'],
            data['eventId']
        )
        return jsonify(attendance), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al registrar inscripción'}), 500
