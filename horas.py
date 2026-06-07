"""
Alumno: Roberto Dos Ramos

Módulo para la normalización de expresiones horarias en texto.
Convierte expresiones horarias en lenguaje natural al formato HH:MM.
"""

import re


import doctest
 
 
def normalizaHoras(ficText, ficNorm):
    """
    Lee un fichero de texto con expresiones horarias y escribe el resultado
    normalizado en otro fichero. Cada línea se procesa de forma independiente.
 
    >>> normalizaHoras('horas.txt', 'horas_norm.txt')
    >>> for linea in open('horas_norm.txt', encoding='utf-8'):
    ...     print(linea, end='')
    La llegada del tren está prevista a las 18:30
    Tenía su clase entre las 08:00 y las 10:30
    Se acaba a las 16:30
    Empieza a trabajar a las 07:00
    Es lo mismo 04:45 que 04:45
    Tenemos descanso hasta las 17:05
    Las campanadas son a las 00:00
    <BLANKLINE>
    Son exactamente las 17:5
    Cuando llegó, ya eran las 11 de la tarde
    El examen es a las 17 de la tarde
    Cenamos en las 7 puertas
    No llegará antes de las 1h78m
    Corrió la maratón en 32h31m, pero no ganó
    Quedamos a las 23 en punto
    """
    with open(ficText, 'r', encoding='utf-8') as f:
        contenido = f.read()
 
    resultado = normaliza_texto(contenido)
 
    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write(resultado)



# una y otra
reg_full = r'\b(?P<hora>1[0-2]|0?[1-9])h?\s+(?P<fraccion>en punto|y cuarto|y media|menos cuarto)\s+(?P<periodo>de la (?:mañana|tarde|noche|madrugada)|del mediodía)'

# solo fraccion
reg_fracc = r'\b(?P<hora>1[0-2]|0?[1-9])h?\s+(?P<fraccion>en punto|y cuarto|y media|menos cuarto)'

# solo periodo
reg_period = r'\b(?P<hora>1[0-2]|0?[1-9])h?\s+(?P<periodo>de la (?:mañana|tarde|noche|madrugada)|del mediodía)'


def normaliza_texto(texto):
    

    # 1.  fraccion Y periodo 
    texto = re.sub(
        reg_full,
        reemplaza_completo,
        texto
    )

    # 2. solo periodo
    texto = re.sub(
        reg_period,
        reemplaza_completo,
        texto
    )

    # 3. solo fraccion
    texto = re.sub(
        reg_fracc,
        reemplaza_completo,
        texto
    )

    # 4. Formato estándar HH:MM (ej: 18:30, 08:05, 8:27)
   
    texto = re.sub(
        r'\b(\d{1,2}):(\d{2})\b',
        reemplaza_estandar,
        texto
    )

    # 5. Formato Xh o XhYm (ej: 8h, 10h30m, 17h5m)
    
    texto = re.sub(
        r'\b(\d{1,2})h(?:(\d{1,2})m)?\b',
        reemplaza_h,
        texto
    )

    return texto


def reemplaza_estandar(m):
    """Formato HH:MM — válido si horas 0-23 y minutos con exactamente 2 dígitos."""
    hora_str = m.group(1)
    min_str  = m.group(2)
    hora     = int(hora_str)
    minuto   = int(min_str)

    # Los minutos deben estar escritos con exactamente 2 dígitos
    if len(min_str) != 2:
        return m.group(0)

    if hora > 23 or minuto > 59:
        return m.group(0)

    return f"{hora:02d}:{minuto:02d}"


def reemplaza_h(m):
    """Formato Xh o XhYm."""
    hora   = int(m.group(1))
    minuto = int(m.group(2)) if m.group(2) else 0

    if hora > 23 or minuto > 59:
        return m.group(0)

    return f"{hora:02d}:{minuto:02d}"


def reemplaza_completo(m):
    hora           = int(m.group('hora'))
    # FIX 1: usar groupdict().get() para grupos opcionales según el patrón usado
    fraccion       = m.groupdict().get('fraccion')
    periodo        = m.groupdict().get('periodo')
    texto_original = m.group(0)

    # hora fuera de rango 1-12 con fraccion (23 en punto)
    if fraccion and (hora < 1 or hora > 12):
        return texto_original

    # hora fuera de rango 1-12 con periodo (17 de la tarde)
    if periodo and (hora < 1 or hora > 12):
        return texto_original

    # Determinamos hora_24 según el periodo
    if periodo:
        if periodo == 'de la mañana':
            
            if hora > 12:
                return texto_original
            hora_24 = 0 if hora == 12 else hora

        elif periodo == 'del mediodía':
            
            if hora not in [12, 1, 2, 3]:
                return texto_original
            hora_24 = hora  # 12 del mediodía = 12:00

        elif periodo == 'de la tarde':
            # rango válido: 3-8
            if hora < 3 or hora > 8:
                return texto_original
            hora_24 = hora + 12  # nunca es 12 dentro de este rango

        elif periodo == 'de la noche':
            # rango válido: 8-12
            if hora < 8 or hora > 12:
                return texto_original
            hora_24 = 0 if hora == 12 else hora + 12

        elif periodo == 'de la madrugada':
            # rango válido: 1-6
            if hora < 1 or hora > 6:
                return texto_original
            hora_24 = hora  # 1-6 AM

    else:
        hora_24 = hora

    # Determinamos los minutos según la fraccion
    if fraccion:
        if fraccion == 'en punto':
            minuto = 0
        elif fraccion == 'y cuarto':
            minuto = 15
        elif fraccion == 'y media':
            minuto = 30
        elif fraccion == 'menos cuarto':
            # FIX 3: módulo 24 para evitar hora negativa (ej: 00:00 → 23:45)
            hora_24 = (hora_24 - 1) % 24
            minuto  = 45
    else:
        minuto = 0

    return f"{hora_24:02d}:{minuto:02d}"


if __name__ == '__main__':
    doctest.testmod(verbose=True)
