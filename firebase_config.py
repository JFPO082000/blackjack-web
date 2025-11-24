# firebase_config.py
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Inicializar Firebase Admin SDK
def initialize_firebase():
    """Inicializa la conexión con Firebase Realtime Database."""
    if not firebase_admin._apps:
        try:
            # Obtener credenciales desde variable de entorno
            cred_json = os.environ.get('FIREBASE_CREDENTIALS')
            
            if cred_json:
                # Parsear JSON de credenciales
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
            else:
                # Fallback: buscar archivo local (solo para desarrollo)
                cred = credentials.Certificate('firebase-credentials.json')
            
            # Inicializar con la URL de tu base de datos
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://basedatoscasino-default-rtdb.firebaseio.com/'
            })
            print("✓ Firebase inicializado correctamente")
        except Exception as e:
            print(f"⚠ Error al inicializar Firebase: {e}")
            print("  Continuando sin Firebase (modo local)")

def get_user_balance(user_id):
    """
    Obtiene el saldo actual del usuario desde Firebase.
    
    Args:
        user_id: El localId del usuario de Firebase Auth
        
    Returns:
        int: El saldo actual, o 500 si no existe o hay error
    """
    try:
        ref = db.reference(f'users/{user_id}/saldo_actual')
        balance = ref.get()
        
        if balance is not None:
            return int(balance)
        else:
            # Usuario nuevo, crear con saldo inicial
            ref.set(500)
            return 500
    except Exception as e:
        print(f"⚠ Error al leer saldo de Firebase: {e}")
        return 500

def update_user_balance(user_id, new_balance):
    """
    Actualiza el saldo del usuario en Firebase.
    
    Args:
        user_id: El localId del usuario de Firebase Auth
        new_balance: El nuevo saldo a guardar
        
    Returns:
        bool: True si se actualizó correctamente, False si hubo error
    """
    try:
        ref = db.reference(f'users/{user_id}/saldo_actual')
        ref.set(int(new_balance))
        return True
    except Exception as e:
        print(f"⚠ Error al actualizar saldo en Firebase: {e}")
        return False

# Inicializar Firebase al importar el módulo
initialize_firebase()
