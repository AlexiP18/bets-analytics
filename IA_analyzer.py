import json
import os
import sys
import google.generativeai as genai
from typing import Dict, Any

def load_data(filepath: str) -> Dict[str, Any]:
    """Carga los datos desde un archivo JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Archivo {filepath} no encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: El archivo {filepath} no contiene un JSON válido.")
        sys.exit(1)

def analyze_with_gemini(data: Dict[str, Any]) -> str:
    """Envía los datos a Gemini y retorna la predicción en formato JSON."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
        # Para propósitos de demostración en este entorno, retornamos un mensaje informativo
        # en lugar de salir, para que Jules pueda ver el flujo.
        return json.dumps({"error": "Missing API Key", "status": "failed"})

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Eres un analista experto en apuestas de fútbol. Analiza los siguientes datos y proporciona una predicción detallada.

    Datos del partido:
    {json.dumps(data, indent=2)}

    Debes responder EXCLUSIVAMENTE con un JSON válido que tenga la siguiente estructura:
    {{
        "partido": "Nombre del partido",
        "prediccion": {{
            "ganador": "Local/Empate/Visitante",
            "probabilidad_local": float,
            "probabilidad_empate": float,
            "probabilidad_visitante": float,
            "marcador_exacto": "X-Y",
            "analisis_breve": "Breve explicación de 2-3 líneas"
        }}
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Intentar extraer el JSON de la respuesta
        text = response.text.strip()
        # A veces Gemini envuelve el JSON en bloques de código markdown
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0].strip()

        return text
    except Exception as e:
        print(f"Error durante la llamada a la API de Gemini: {e}")
        return json.dumps({"error": str(e), "status": "failed"})

def main():
    input_file = "datos_temporales.json"

    # 1. Cargar datos
    print(f"Cargando datos de {input_file}...")
    data = load_data(input_file)

    # 2. Analizar con Gemini
    print("Enviando datos a Gemini API...")
    prediction_json = analyze_with_gemini(data)

    # 3. Mostrar/Guardar resultado
    try:
        # Validar que sea un JSON válido
        json_result = json.loads(prediction_json)
        print("\nPredicción generada exitosamente:")
        print(json.dumps(json_result, indent=2, ensure_ascii=False))

        # Opcionalmente guardar en un archivo
        with open("prediccion_resultado.json", "w", encoding="utf-8") as f:
            json.dump(json_result, f, indent=2, ensure_ascii=False)
            print("\nResultado guardado en prediccion_resultado.json")

    except json.JSONDecodeError:
        print("\nError: La IA no devolvió un JSON válido.")
        print("Respuesta cruda de la IA:")
        print(prediction_json)

if __name__ == "__main__":
    main()
