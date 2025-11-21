# Script de prueba rápida de la API FastEvents
# Ejecutar con: python test_api_manual.py

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Imprime una respuesta formateada"""
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def main():
    print("\n🚀 Iniciando pruebas manuales de FastEvents API")
    print("="*60)
    
    # 1. Verificar que la API está funcionando
    print("\n1️⃣ Verificando estado de la API...")
    response = requests.get(f"{BASE_URL}/")
    print_response("Estado de la API", response)
    
    # 2. Crear un evento
    print("\n2️⃣ Creando un nuevo evento...")
    event_data = {
        "nombre": "Conferencia Python 2025",
        "fecha": "2025-12-25",
        "capacidad": 100
    }
    response = requests.post(f"{BASE_URL}/events", json=event_data)
    print_response("Evento creado", response)
    event_id = response.json()['id'] if response.status_code == 201 else None
    
    # 3. Crear un usuario
    print("\n3️⃣ Creando un nuevo usuario...")
    user_data = {
        "nombre": "Ana García",
        "email": "ana.garcia@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print_response("Usuario creado", response)
    user_id = response.json()['id'] if response.status_code == 201 else None
    
    # 4. Listar todos los eventos
    print("\n4️⃣ Listando todos los eventos...")
    response = requests.get(f"{BASE_URL}/events")
    print_response("Lista de eventos", response)
    
    # 5. Obtener evento específico (prueba de caché)
    if event_id:
        print(f"\n5️⃣ Obteniendo evento {event_id} (primera vez - se guarda en caché)...")
        response = requests.get(f"{BASE_URL}/events/{event_id}")
        print_response("Evento obtenido", response)
        
        print(f"\n6️⃣ Obteniendo evento {event_id} de nuevo (desde caché)...")
        response = requests.get(f"{BASE_URL}/events/{event_id}")
        print_response("Evento desde caché", response)
    
    # 7. Inscribir usuario al evento
    if user_id and event_id:
        print(f"\n7️⃣ Inscribiendo usuario {user_id} al evento {event_id}...")
        attendance_data = {
            "userId": user_id,
            "eventId": event_id
        }
        response = requests.post(f"{BASE_URL}/attendance", json=attendance_data)
        print_response("Inscripción registrada", response)
        
        # 8. Verificar que se incrementó el contador de inscritos
        print(f"\n8️⃣ Verificando incremento de inscritos...")
        response = requests.get(f"{BASE_URL}/events/{event_id}")
        print_response("Evento actualizado con inscritos", response)
    
    # 9. Actualizar evento
    if event_id:
        print(f"\n9️⃣ Actualizando evento {event_id}...")
        update_data = {
            "nombre": "Conferencia Python 2025 - ACTUALIZADA",
            "capacidad": 150
        }
        response = requests.put(f"{BASE_URL}/events/{event_id}", json=update_data)
        print_response("Evento actualizado", response)
    
    # 10. Intentar crear usuario con email duplicado
    print("\n🔟 Intentando crear usuario con email duplicado...")
    duplicate_user = {
        "nombre": "Otro Usuario",
        "email": "ana.garcia@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=duplicate_user)
    print_response("Error esperado - Email duplicado", response)
    
    # 11. Intentar inscribir usuario dos veces
    if user_id and event_id:
        print(f"\n1️⃣1️⃣ Intentando inscribir usuario dos veces...")
        attendance_data = {
            "userId": user_id,
            "eventId": event_id
        }
        response = requests.post(f"{BASE_URL}/attendance", json=attendance_data)
        print_response("Error esperado - Doble inscripción", response)
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
        print("   Ejecuta: python app.py")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
