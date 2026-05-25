import scraper
import IA_analyzer
import db_manager
import json
import os

def run_pipeline():
    print("--- INICIANDO PIPELINE DE PREDICCIONES ---")

    # 1. Scraping
    print("\n1. Ejecutando Scraper...")
    match_data = scraper.fetch_match_data()
    scraper.save_to_json(match_data)

    # 2. Análisis con IA
    print("\n2. Ejecutando Análisis de IA...")
    prediction = IA_analyzer.analyze_with_gemini(match_data)

    if "error" in prediction:
        print(f"Error en el análisis: {prediction['error']}")
        return

    print("Predicción generada:")
    print(json.dumps(prediction, indent=2, ensure_ascii=False))

    # 3. Guardar en Base de Datos
    print("\n3. Guardando en Firestore...")
    success = db_manager.save_prediction(prediction)

    if success:
        print("\n--- PIPELINE FINALIZADO CON ÉXITO ---")
    else:
        print("\n--- PIPELINE FINALIZADO CON ERRORES EN EL GUARDADO ---")

if __name__ == "__main__":
    run_pipeline()
