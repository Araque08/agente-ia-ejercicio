"""Agente didáctico basado en reglas. No controla equipos eléctricos reales."""
from dataclasses import dataclass, asdict

@dataclass
class DatosRed:
    consumo: float
    solar: float
    eolica: float
    tradicional: float
    capacidad_extra: float
    bateria: float
    precio: float
    transformador: int
    linea: int


def evaluar_red(d: DatosRed) -> dict:
    """Percibe, decide, actúa virtualmente y registra la retroalimentación."""
    valores = [d.consumo, d.solar, d.eolica, d.tradicional, d.capacidad_extra, d.bateria, d.precio]
    if any(v < 0 for v in valores) or not (0 <= d.transformador <= 100 and 0 <= d.linea <= 100):
        raise ValueError('Los valores no pueden ser negativos y los estados deben estar entre 0 y 100.')

    generacion_inicial = d.solar + d.eolica + d.tradicional
    diferencia_inicial = generacion_inicial - d.consumo
    riesgo_equipo = d.transformador < 40 or d.linea < 40
    acciones = []
    adicional = 0.0
    descarga = 0.0
    reduccion = 0.0
    carga_bateria = 0.0

    if riesgo_equipo:
        acciones.append('Alertar al operador: revisar transformador o línea en mal estado.')

    faltante = max(0.0, -diferencia_inicial)
    if faltante > 0:
        # Primero aumenta generación disponible; costo variable estimado simplificado.
        adicional = min(faltante, d.capacidad_extra)
        faltante -= adicional
        if adicional > 0:
            acciones.append(f'Aumentar generación convencional en {adicional:.1f} MW (simulación).')
        descarga = min(faltante, d.bateria, 30.0)  # límite virtual por ciclo
        faltante -= descarga
        if descarga > 0:
            acciones.append(f'Usar {descarga:.1f} MW de batería (simulación).')
        reduccion = min(faltante, d.consumo * .15)
        faltante -= reduccion
        if reduccion > 0:
            acciones.append(f'Sugerir ahorro voluntario de {reduccion:.1f} MW (demanda flexible).')
    else:
        carga_bateria = min(diferencia_inicial, max(0, 100 - d.bateria), 30.0)
        if carga_bateria > 0:
            acciones.append(f'Almacenar {carga_bateria:.1f} MWh equivalentes en batería virtual.')
        sobrante = diferencia_inicial - carga_bateria
        if sobrante > 0:
            acciones.append(f'Registrar excedente de {sobrante:.1f} MW para posible reducción de generación.')

    oferta_final = generacion_inicial + adicional + descarga
    demanda_final = d.consumo - reduccion
    balance_final = oferta_final - demanda_final - carga_bateria
    riesgo_corte = balance_final < -0.01
    estado = 'RIESGO DE DÉFICIT' if riesgo_corte else ('ALERTA DE EQUIPO' if riesgo_equipo else 'ESTABLE EN LA SIMULACIÓN')
    if riesgo_corte:
        acciones.append(f'Déficit pendiente de {-balance_final:.1f} MW: notificar para intervención humana.')
    if not acciones:
        acciones.append('Mantener operación simulada y continuar supervisando.')
    # Costos ilustrativos, no precios reales de despacho o mercado.
    costo = (d.tradicional + adicional) * d.precio + descarga * (d.precio * .3)
    return {
        'entradas': asdict(d), 'generacion_inicial': round(generacion_inicial, 2),
        'diferencia_inicial': round(diferencia_inicial, 2), 'adicional': round(adicional, 2),
        'descarga': round(descarga, 2), 'reduccion': round(reduccion, 2),
        'carga_bateria': round(carga_bateria, 2), 'oferta_final': round(oferta_final, 2),
        'demanda_final': round(demanda_final, 2), 'balance_final': round(balance_final, 2),
        'estado': estado, 'riesgo_corte': riesgo_corte, 'riesgo_equipo': riesgo_equipo,
        'acciones': acciones, 'costo_indicativo': round(costo, 2)
    }
