from flask import Blueprint, request, jsonify
from src.events.event_service import EventService

event_bp = Blueprint('events', __name__)

# Variable global para el servicio (se inyectará desde app.py)
event_service: EventService = None

def init_event_controller(service: EventService):
    """Inicializa el controlador con el servicio"""
    global event_service
    event_service = service

@event_bp.route('/events', methods=['GET'])
def get_events():
    """GET /events - Lista todos los eventos"""
    events = event_service.get_all_events()
    return jsonify(events), 200

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """GET /events/{id} - Obtiene un evento por ID"""
    event = event_service.get_event_by_id(event_id)
    if event:
        return jsonify(event), 200
    return jsonify({'error': 'Evento no encontrado'}), 404

@event_bp.route('/events', methods=['POST'])
def create_event():
    """POST /events - Crea un nuevo evento"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not all(k in data for k in ['nombre', 'fecha', 'capacidad']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        event = event_service.create_event(data)
        return jsonify(event), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear evento'}), 500

@event_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """PUT /events/{id} - Actualiza un evento"""
    try:
        data = request.get_json()
        event = event_service.update_event(event_id, data)
        
        if event:
            return jsonify(event), 200
        return jsonify({'error': 'Evento no encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al actualizar evento'}), 500

@event_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """DELETE /events/{id} - Elimina un evento"""
    try:
        if event_service.delete_event(event_id):
            return jsonify({'message': 'Evento eliminado'}), 200
        return jsonify({'error': 'Evento no encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al eliminar evento'}), 500
