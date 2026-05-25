import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

def init_db():
    """Inicializa la conexión con Firestore."""
    if not firebase_admin._apps:
        try:
            # Usa las credenciales por defecto (ADC)
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Aviso: No se pudieron encontrar las credenciales por defecto de Google Cloud: {e}")
            print("El guardado en Firestore fallará si no se configuran las credenciales.")
            return None

    try:
        return firestore.client()
    except Exception as e:
        print(f"Error al obtener el cliente de Firestore: {e}")
        return None

def save_prediction(prediction_data):
    """
    Guarda la predicción en la colección 'predicciones_partidos'.
    El ID del documento sigue el formato: HomeTeam_vs_AwayTeam_YYYY-MM-DD
    """
    db = init_db()
    if db is None:
        print("Saltando guardado en Firestore por falta de conexión/credenciales.")
        return False

    try:
        # Extraer información para el ID
        match_name = prediction_data.get("partido", "unknown_match")
        # Si no viene la fecha en la predicción, intentamos obtenerla o usamos una por defecto
        # En una integración real, estos datos vendrían del scraper

        # Intentamos normalizar el nombre para el ID del documento
        doc_id = match_name.replace(" ", "_")

        # Si tenemos los datos del scraper a mano, podríamos ser más precisos.
        # Por ahora usamos el nombre del partido que viene en el JSON de la IA.

        print(f"Guardando predicción en Firestore con ID: {doc_id}...")

        db.collection('predicciones_partidos').document(doc_id).set(prediction_data)
        print("Predicción guardada exitosamente en Firestore.")
        return True
    except Exception as e:
        print(f"Error al guardar en Firestore: {e}")
        return False

if __name__ == "__main__":
    # Test simple
    test_data = {
        "partido": "Real Madrid vs Barcelona 2024-05-20",
        "prediccion": {
            "ganador": "Real Madrid",
            "probabilidad_local": 0.45,
            "probabilidad_empate": 0.25,
            "probabilidad_visitante": 0.30,
            "marcador_exacto": "2-1",
            "analisis_breve": "Test de guardado."
        }
    }
    save_prediction(test_data)
