"""Interfaz web del agente Smart Grid educativo."""
import streamlit as st
from agente import DatosRed, evaluar_red

st.set_page_config(page_title='Agente Smart Grid', page_icon='⚡', layout='wide')
st.title('⚡ Agente de IA para Redes Eléctricas — Smart Grid')
st.caption('Prototipo educativo • decisiones con reglas • datos simulados • no conectado a una red real')

escenarios = {
    'Red equilibrada': dict(consumo=120, solar=35, eolica=25, tradicional=60, capacidad_extra=40, bateria=50, precio=220, transformador=95, linea=90),
    'Alta demanda': dict(consumo=200, solar=20, eolica=15, tradicional=80, capacidad_extra=40, bateria=30, precio=300, transformador=88, linea=90),
    'Mucha energía renovable': dict(consumo=85, solar=90, eolica=40, tradicional=20, capacidad_extra=30, bateria=30, precio=180, transformador=97, linea=94),
    'Falla en transformador': dict(consumo=160, solar=35, eolica=20, tradicional=75, capacidad_extra=30, bateria=25, precio=280, transformador=25, linea=90),
}
seleccion = st.selectbox('Selecciona un caso de prueba', list(escenarios))
e = escenarios[seleccion]
st.markdown('### 1. Percepción: datos de entrada')
a, b, c = st.columns(3)
with a:
    consumo = st.slider('Consumo (MW)', 0, 300, e['consumo'])
    solar = st.slider('Generación solar (MW)', 0, 150, e['solar'])
    eolica = st.slider('Generación eólica (MW)', 0, 150, e['eolica'])
with b:
    tradicional = st.slider('Generación tradicional (MW)', 0, 200, e['tradicional'])
    capacidad_extra = st.slider('Capacidad tradicional extra (MW)', 0, 100, e['capacidad_extra'])
    bateria = st.slider('Energía virtual disponible en batería (MWh)', 0, 100, e['bateria'])
with c:
    precio = st.slider('Precio ilustrativo por MWh (unidades)', 50, 500, e['precio'])
    transformador = st.slider('Estado transformador (%)', 0, 100, e['transformador'])
    linea = st.slider('Estado línea (%)', 0, 100, e['linea'])

resultado = evaluar_red(DatosRed(consumo, solar, eolica, tradicional, capacidad_extra, bateria, precio, transformador, linea))
st.divider()
st.markdown('### 2. Razonamiento: comparación de oferta y demanda')
m1, m2, m3 = st.columns(3)
m1.metric('Demanda inicial', f'{consumo} MW')
m2.metric('Generación inicial', f"{resultado['generacion_inicial']:.1f} MW")
m3.metric('Balance inicial', f"{resultado['diferencia_inicial']:+.1f} MW")
if resultado['riesgo_corte']:
    st.error('Riesgo de déficit: las medidas simuladas no cubren toda la demanda.')
elif resultado['riesgo_equipo']:
    st.warning('Alerta de infraestructura: hay que revisar equipos aunque el balance energético sea suficiente.')
else:
    st.success('Balance atendido en la simulación (no representa una garantía de estabilidad real).')

st.markdown('### 3. Acción: decisiones del agente')
for i, accion in enumerate(resultado['acciones'], start=1):
    st.write(f'{i}. {accion}')

st.markdown('### 4. Retroalimentación: resultado de las decisiones')
r1, r2, r3 = st.columns(3)
r1.metric('Oferta después de acciones', f"{resultado['oferta_final']:.1f} MW")
r2.metric('Demanda después de ahorro', f"{resultado['demanda_final']:.1f} MW")
r3.metric('Balance final (descontando carga)', f"{resultado['balance_final']:+.1f} MW")
st.bar_chart({'Demanda inicial': consumo, 'Generación inicial': resultado['generacion_inicial'], 'Oferta tras ajustes': resultado['oferta_final']})
st.info(f"Indicador de costo de generación ilustrativo: {resultado['costo_indicativo']:,.0f} unidades. No es una factura ni una optimización real del mercado.")
st.markdown('### 5. Iteración')
st.write('Cambia uno de los controles o el escenario: el agente vuelve a percibir, razonar, actuar y mostrar el resultado automáticamente.')
with st.expander('¿Por qué se considera un agente inteligente?'):
    st.write('Porque recibe información del entorno, aplica reglas de decisión, propone acciones, evalúa el resultado y repite el proceso. Es IA simbólica básica, sin entrenamiento de un modelo de aprendizaje automático.')
with st.expander('Limitaciones importantes'):
    st.write('Los datos son inventados para clase. No modela frecuencia, tensión, flujos eléctricos, seguridad N-1, costos reales, límites de rampa ni regulación. No debe controlar infraestructura física.')
