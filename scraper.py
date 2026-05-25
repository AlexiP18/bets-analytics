import json
import os

def fetch_match_data():
    """
    Simula la obtención de datos de una API de fútbol.
    En una implementación real, aquí se usaría 'requests' para llamar a API-Football.
    """
    print("Obteniendo datos de partidos...")

    # Datos simulados (Mock)
    mock_data = {
        "match": "Real Madrid vs Barcelona",
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "match_date": "2024-05-20",
        "recent_stats": {
            "Real Madrid": {
                "last_5_matches": ["W", "W", "D", "W", "L"],
                "avg_goals_scored": 2.4,
                "avg_goals_conceded": 0.8
            },
            "Barcelona": {
                "last_5_matches": ["W", "D", "W", "W", "W"],
                "avg_goals_scored": 2.1,
                "avg_goals_conceded": 1.1
            }
        },
        "h2h": {
            "last_5": "3W Real Madrid, 2W Barcelona"
        }
    }

    return mock_data

def save_to_json(data, filepath="datos_temporales.json"):
    """Guarda los datos en un archivo JSON."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Datos guardados exitosamente en {filepath}")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def main():
    data = fetch_match_data()
    save_to_json(data)

if __name__ == "__main__":
    main()
