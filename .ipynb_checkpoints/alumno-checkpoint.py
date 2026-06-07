"""
Alumno: Roberto Dos Ramos
 
Módulo para el tratamiento de las notas de los alumnos.
Incluye la clase Alumno y la función leeAlumnos() para leer ficheros de notas.
"""
 
import re
import doctest


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve un
    diccionario en el que la clave es el nombre de cada alumno y su contenido
    el objeto Alumno correspondiente.
 
    Cada línea del fichero tiene el formato:
        <numIden> <nombre completo> <nota1> <nota2> ...
 
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcell de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    #en el test unitario tuve que cambiar uno de los apellidos
    #Balcells lo pase a Balcell ya que en alumnos.txt no tiene esa s del final
    reNumero = r'(?P<numero>\d+)'
    reNombre = r'(?P<nombre>\w*( [a-zA-Z\D]*))'#en la segunda hay que especificar que NO queremos numeros, si no se piensa que es 'Blanca Agirrebarrenetse 10'
    reNotas  = r'(?P<notas>[\d.\s]+)'
    reAlumno = re.compile(reNumero + r'\s+' + reNombre + r'\s+' + reNotas)
    
    alumnos = {}
    with open(ficAlum, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            m = reAlumno.match(linea)
            if m:
                num_iden = int(m.group('numero'))
                nombre   = m.group('nombre')
                notas    = [float(n) for n in re.findall(r'\d+\.?\d*', m.group('notas'))]
                alumnos[nombre] = Alumno(nombre, num_iden, notas)
    return alumnos
 
 

doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
