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
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {filepath} no contiene un JSON válido.")
        return {}

def analyze_with_gemini(data: Dict[str, Any]) -> Dict[str, Any]:
    """Envía los datos a Gemini y retorna la predicción como un diccionario."""
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("Aviso: GOOGLE_API_KEY no configurada. Usando respuesta simulada.")
        return {
            "partido": f"{data.get('home_team', 'Local')} vs {data.get('away_team', 'Visitante')} {data.get('match_date', '')}",
            "prediccion": {
                "ganador": data.get('home_team', 'Local'),
                "probabilidad_local": 0.50,
                "probabilidad_empate": 0.25,
                "probabilidad_visitante": 0.25,
                "marcador_exacto": "2-1",
                "analisis_breve": "Simulación: El equipo local tiene mejores estadísticas recientes."
            }
        }

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Eres un analista experto en apuestas de fútbol. Analiza los siguientes datos y proporciona una predicción detallada.

    Datos del partido:
    {json.dumps(data, indent=2)}

    Debes responder EXCLUSIVAMENTE con un JSON válido, sin bloques de código markdown, sin texto adicional.
    Estructura requerida:
    {{
        "partido": "NombreEquipo1 vs NombreEquipo2 YYYY-MM-DD",
        "prediccion": {{
            "ganador": "Local/Empate/Visitante",
            "probabilidad_local": float,
            "probabilidad_empate": float,
            "probabilidad_visitante": float,
            "marcador_exacto": "X-Y",
            "analisis_breve": "Explicación de 2-3 líneas"
        }}
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Limpieza de markdown por si acaso
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)
    except Exception as e:
        print(f"Error durante la llamada a la API de Gemini o parsing: {e}")
        return {"error": str(e), "status": "failed"}

def main():
    input_file = "datos_temporales.json"
    data = load_data(input_file)
    if not data:
        print("No hay datos para analizar.")
        return

    prediction = analyze_with_gemini(data)
    print(json.dumps(prediction, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
