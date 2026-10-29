# Agente de IA para Gestión de Redes Eléctricas (Smart Grid)

Aplicación web educativa construida en **Python y Streamlit**. Simula un agente **basado en reglas** (IA simbólica básica); no utiliza datos reales ni modelos entrenados.

## ¿Qué hace?
1. **Percepción:** recibe consumo, producción solar/eólica/tradicional, batería, precio y salud de equipos.
2. **Razonamiento:** compara generación y consumo; detecta riesgo de déficit y alerta de equipo.
3. **Acción:** sugiere aumentar la generación, usar batería, reducir demanda flexible o inspeccionar equipo.
4. **Retroalimentación:** calcula el balance tras los ajustes.
5. **Iteración:** al cambiar parámetros, repite las decisiones.

## Ejecutar en VS Code
Requisitos: Python 3.10 o superior.

Abre esta carpeta en VS Code. En una terminal:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

En Windows si `python` no funciona, prueba `py` en su lugar. Se abrirá una dirección local como `http://localhost:8501`.

## Cómo crear un link público gratuito
1. Crea un repositorio público nuevo en GitHub.
2. Sube `app.py`, `agente.py` y `requirements.txt` (junto al README).
3. Entra a https://share.streamlit.io/ y conecta tu cuenta de GitHub.
4. Elige **Create app**, repositorio, rama `main` y archivo principal `app.py`.
5. Pulsa **Deploy**. Streamlit mostrará un enlace `https://...streamlit.app` que puedes compartir.

Consulta la guía oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Ejemplo de la exposición
Escenario **Alta demanda**: el consumo es 200 MW y la generación inicial 115 MW; hay un déficit inicial de 85 MW. El agente usa 40 MW de generación adicional, 30 MW de batería y sugiere ahorrar 15 MW. El balance final queda en 0 MW en este ejemplo simplificado.

## Notas técnicas
- El indicador de costo es **ilustrativo** y no representa los precios reales de mercado.
- La batería se simplifica como energía disponible por intervalo y descarga máxima virtual de 30 MW; la aplicación no modela intervalos temporales físicamente detallados.
- El sistema no decide sobre protecciones ni opera una red real. Los comandos son propuestas simuladas.
- La estabilidad real requiere cálculos eléctricos y control por personal autorizado.

## Referencias
- https://www.energy.gov/oe/grid-modernization-and-smart-grid
- https://www.ferc.gov/smart-grid-1
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
