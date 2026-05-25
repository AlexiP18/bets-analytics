import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_db():
    """Inicializa la aplicación Firebase Admin con Application Default Credentials."""
    try:
        # Si ya está inicializada, obtenemos la app existente
        return firestore.client()
    except ValueError:
        # Si no, la inicializamos
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        return firestore.client()

def guardar_prediccion(prediction_data):
    """
    Guarda el objeto JSON de predicción en Firestore.

    Args:
        prediction_data (dict): Datos de la predicción generados por IA_analyzer.py
    """
    db = initialize_db()

    partido = prediction_data.get('partido', 'Partido_Desconocido')
    fecha = datetime.now().strftime('%Y-%m-%d')

    # Sanitizar el ID del documento: reemplazar espacios por guiones bajos y limpiar caracteres especiales si fuera necesario
    doc_id = f"{partido.replace(' ', '_')}_{fecha}"

    try:
        doc_ref = db.collection('predicciones_partidos').document(doc_id)
        doc_ref.set(prediction_data)
        logger.info(f"Predicción guardada exitosamente con ID: {doc_id}")
        return doc_id
    except Exception as e:
        logger.error(f"Error al guardar la predicción en Firestore: {e}")
        raise

if __name__ == "__main__":
    # Ejemplo de uso/prueba rápida
    sample_data = {
        "partido": "Test Team vs Demo FC",
        "prediccion": {
            "ganador": "Empate",
            "probabilidad_local": 33.3,
            "probabilidad_empate": 33.4,
            "probabilidad_visitante": 33.3,
            "marcador_exacto": "1-1",
            "analisis_breve": "Partido de prueba"
        }
    }
    try:
        # Nota: Esto fallará localmente si no hay Application Default Credentials configuradas
        guardar_prediccion(sample_data)
    except Exception:
        print("La ejecución falló (probablemente por falta de credenciales de GCP), lo cual es esperado en este paso.")
