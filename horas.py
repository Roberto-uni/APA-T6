"""
Alumno: Roberto Dos Ramos
 
Módulo para la normalización de expresiones horarias en texto.
Convierte expresiones horarias en lenguaje natural al formato HH:MM.
"""
 
import re

def normalizaHoras(ficText, ficNorm):
    with open(ficText, 'r', encoding='utf-8') as f:
        contenido = f.read()

    resultado = normaliza_texto(contenido)

    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write(resultado)


def normaliza_texto(texto):
    # Orden importante: de más específico a menos específico

    # 1. Formato estándar HH:MM (ej: 18:30, 08:05, 8:27)
    texto = re.sub(
        r'\b(\d{1,2}):(\d{2})\b',
        reemplaza_estandar,
        texto
    )

    # 2. Formato Xh o XhYm (ej: 8h, 10h30m, 17h5m)
    texto = re.sub(
        r'\b(\d{1,2})h(?:(\d{1,2})m)?\b',
        reemplaza_h,
        texto
    )

    return texto


def reemplaza_estandar(m):
    """Formato HH:MM — válido si horas 0-23 y minutos con 2 dígitos."""
    hora_str = m.group(1)
    min_str  = m.group(2)
    hora = int(hora_str)
    minuto = int(min_str)

    # Los minutos deben estar escritos con exactamente 2 dígitos
    if len(min_str) != 2:
        return m.group(0)  # incorrecto: dejar tal cual

    if hora > 23 or minuto > 59:
        return m.group(0)  # fuera de rango: dejar tal cual

    return f"{hora:02d}:{minuto:02d}"


def reemplaza_h(m):
    """Formato Xh o XhYm."""
    hora = int(m.group(1))
    minuto = int(m.group(2)) if m.group(2) else 0

    if hora > 23 or minuto > 59:
        return m.group(0)  # incorrecto: dejar tal cual

    return f"{hora:02d}:{minuto:02d}"


#r'(\d{1,2})h?\s+(en punto|y cuarto|y media|menos cuarto)\s+(de la (?:mañana|tarde|noche|madrugada)|del mediodía)'

# --- Prueba rápida ---(cortesia de claude)
if __name__ == '__main__':
    import tempfile, os

    ejemplos = [
        # Correctos
        ("18:30",    "18:30"),
        ("8h",       "08:00"),
        ("10h30m",   "10:30"),
        ("17h5m",    "17:05"),
        ("4:45",     "04:45"),
        # Incorrectos (deben quedar igual)
        ("17:5",     "17:5"),    # minutos con 1 dígito
        ("1h78m",    "1h78m"),   # minutos > 59
        ("32h31m",   "32h31m"),  # horas > 23
    ]

    print("=== Tests unitarios ===")
    for entrada, esperado in ejemplos:
        resultado = normaliza_texto(entrada)
        ok = "✓" if resultado == esperado else "✗"
        print(f"  {ok}  '{entrada}' → '{resultado}'  (esperado: '{esperado}')")

    # Prueba con fichero
    texto_prueba = """La llegada del tren está prevista a las 18:30
Tenía su clase entre las 8h y las 10h30m
Tenemos descanso hasta las 17h5m
Son exactamente las 17:5
No llegará antes de las 1h78m
Corrió la maratón en 32h31m, pero no ganó
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as fin:
        fin.write(texto_prueba)
        ruta_in = fin.name

    ruta_out = ruta_in.replace('.txt', '_norm.txt')
    normalizaHoras(ruta_in, ruta_out)

    print("\n=== Resultado del fichero ===")
    with open(ruta_out, encoding='utf-8') as f:
        print(f.read())

    os.unlink(ruta_in)
    os.unlink(ruta_out)