# Bets Analytics - Arquitectura y Reglas del Proyecto

## Visión General
Aplicación de un solo usuario (Solo-Tenant) para análisis y predicción de resultados de fútbol, utilizando IA para procesar estadísticas. 

## Stack Tecnológico y Despliegue
- **Backend / Ingesta de Datos:** Python. Ejecución de scripts modulares para extraer datos de APIs deportivas (ej. API-Football).
- **Procesamiento de IA:** Google Gemini Pro (vía Vertex AI o Gemini API).
- **Base de Datos:** Firebase Firestore. Usada para almacenar tanto el dato crudo (estadísticas) como el dato procesado (predicciones de IA).
- **Frontend / Visualización:** Flutter (Web). Despliegue en Firebase Hosting.

## Arquitectura (Flujo de Datos)
1. **Scraping:** Scripts en Python extraen datos recientes (últimos 5-10 partidos, H2H, lesiones).
2. **Análisis IA:** Los datos crudos se envían a la API de Gemini mediante un System Prompt estricto. La IA devuelve un JSON estructurado con la predicción.
3. **Almacenamiento:** El JSON se guarda en colecciones de Firestore (`predicciones_partidos`).
4. **Consumo:** El frontend en Flutter lee reactivamente de Firestore y muestra el dashboard.

## Reglas de Codificación (Instrucciones para Jules)
- **Modularidad:** Mantén la lógica de la API deportiva separada de la lógica de Gemini y de la conexión a Firestore.
- **Tipado y Errores:** En Python, usa siempre manejo de excepciones (`try/except`) para caídas de red y respuestas inválidas.
- **Formato de Datos:** Todos los datos analíticos deben manejarse y guardarse en formato JSON.
- **Complejidad:** Evita el over-engineering. No uses microservicios ni configuraciones complejas de GCP. Todo debe poder ejecutarse como scripts independientes o Functions simples.
