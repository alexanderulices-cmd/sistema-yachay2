# ================================================================
# SIMULADOR DE NOMBRAMIENTO DOCENTE
# Estructura oficial de la Prueba Nacional (MINEDU, vigente desde 2024)
# ================================================================
"""Simulacros cronometrados con la estructura real de la Prueba Nacional.

Estructura oficial vigente:
  · Habilidades Generales ......... 25 preguntas × 2 pts = 50 pts (sin mínimo)
      - Comprensión lectora: 12 preguntas sobre 2 textos
      - Razonamiento lógico: 13 preguntas
  · Conocimientos Pedagógicos,
    Curriculares y Disciplinares ... 50 preguntas × 3 pts = 150 pts
      - Mínimo eliminatorio: 84 puntos
  · Total: 75 preguntas · 3 h 45 min · mínimo global 110 puntos

Las preguntas son ORIGINALES, redactadas sobre los desempeños de la
matriz de evaluación. No reproducen los cuadernillos del MINEDU, que
están protegidos: para practicar con los oficiales, descárgalos de
evaluaciondocente.perueduca.pe, sección «Evaluaciones anteriores».

Integración en sistema_web.py:
    from simulador_nombramiento import tab_simulador_nombramiento
"""

import io
import json
import random
from datetime import datetime, timedelta

import streamlit as st

# ---------------------------------------------------------------
# PARÁMETROS OFICIALES
# ---------------------------------------------------------------
HG_PREGUNTAS = 25
HG_VALOR = 2
HG_MAXIMO = 50

CPD_PREGUNTAS = 50
CPD_VALOR = 3
CPD_MAXIMO = 150
CPD_MINIMO = 84

TOTAL_PREGUNTAS = 75
MINIMO_GLOBAL = 110
MINUTOS_TOTAL = 225          # 3 h 45 min

LETRAS = ["A", "B", "C", "D", "E"]


def balancear(preguntas, semilla=7):
    """Reparte la clave correcta entre las cinco letras.

    Sin esto, al redactar en serie la correcta cae casi siempre en la
    misma posición y el simulacro deja de medir: se aprueba marcando
    una sola letra.
    """
    salida = []
    for i, p in enumerate(preguntas):
        alts = list(p["alternativas"])
        correcta_txt = alts[LETRAS.index(p["correcta"])]
        destino = (i + semilla) % 5
        cuerpo = [a for a in alts if a != correcta_txt]
        destino = min(destino, len(cuerpo))
        cuerpo.insert(destino, correcta_txt)
        salida.append({**p, "alternativas": cuerpo,
                       "correcta": LETRAS[cuerpo.index(correcta_txt)]})
    return salida


def armar_simulacro(banco_hg, banco_cpd, semilla=0):
    """Construye un simulacro con la estructura oficial.

    Cada semilla distinta produce una combinación distinta, de modo que
    el docente puede rendir varios simulacros sin repetir preguntas
    hasta agotar el banco.
    """
    rnd = random.Random(semilla)

    # Habilidades Generales: 12 de comprensión lectora + 13 de razonamiento
    lectura = [p for p in banco_hg if p.get("tipo") == "lectura"]
    logico = [p for p in banco_hg if p.get("tipo") == "logico"]
    rnd.shuffle(lectura)
    rnd.shuffle(logico)
    hg = lectura[:12] + logico[:13]
    if len(hg) < HG_PREGUNTAS:               # banco corto: completar
        resto = [p for p in banco_hg if p not in hg]
        rnd.shuffle(resto)
        hg += resto[:HG_PREGUNTAS - len(hg)]
    hg = hg[:HG_PREGUNTAS]

    cpd = list(banco_cpd)
    rnd.shuffle(cpd)
    cpd = cpd[:CPD_PREGUNTAS]

    return {
        "hg": balancear(hg, semilla + 3),
        "cpd": balancear(cpd, semilla + 11),
    }


def calificar(simulacro, respuestas):
    """Aplica el criterio oficial de calificación y clasificación."""
    ok_hg = sum(1 for i, p in enumerate(simulacro["hg"])
                if respuestas.get(f"hg{i}") == p["correcta"])
    ok_cpd = sum(1 for i, p in enumerate(simulacro["cpd"])
                 if respuestas.get(f"cpd{i}") == p["correcta"])
    pt_hg = ok_hg * HG_VALOR
    pt_cpd = ok_cpd * CPD_VALOR
    total = pt_hg + pt_cpd

    pasa_cpd = pt_cpd >= CPD_MINIMO
    pasa_total = total >= MINIMO_GLOBAL
    if not pasa_cpd:
        veredicto = ("NO CLASIFICA", "#B3161C",
                     f"No alcanzó el mínimo de {CPD_MINIMO} puntos en "
                     f"Conocimientos. Este filtro es eliminatorio.")
    elif not pasa_total:
        veredicto = ("NO CLASIFICA", "#B3161C",
                     f"Superó Conocimientos, pero no llegó a los "
                     f"{MINIMO_GLOBAL} puntos totales exigidos.")
    else:
        veredicto = ("CLASIFICA", "#0F7A34",
                     "Superó ambos filtros: el mínimo de Conocimientos "
                     "y el puntaje total.")

    return {
        "ok_hg": ok_hg, "ok_cpd": ok_cpd,
        "pt_hg": pt_hg, "pt_cpd": pt_cpd, "total": total,
        "pasa_cpd": pasa_cpd, "pasa_total": pasa_total,
        "veredicto": veredicto,
        "max_total": HG_MAXIMO + CPD_MAXIMO,
    }


def resumen_por_competencia(simulacro, respuestas):
    """Agrupa los aciertos por competencia para saber qué reforzar."""
    conteo = {}
    for i, p in enumerate(simulacro["cpd"]):
        comp = p.get("competencia", "General")
        d = conteo.setdefault(comp, {"total": 0, "ok": 0})
        d["total"] += 1
        if respuestas.get(f"cpd{i}") == p["correcta"]:
            d["ok"] += 1
    for i, p in enumerate(simulacro["hg"]):
        comp = "Comprensión lectora" if p.get("tipo") == "lectura" \
            else "Razonamiento lógico"
        d = conteo.setdefault(comp, {"total": 0, "ok": 0})
        d["total"] += 1
        if respuestas.get(f"hg{i}") == p["correcta"]:
            d["ok"] += 1
    for c, d in conteo.items():
        d["pct"] = round(100 * d["ok"] / d["total"], 1) if d["total"] else 0
    return conteo


# ================================================================
# BANCOS DE PREGUNTAS
# ================================================================


TEXTO_1 = """La evaluación formativa se distingue de la evaluación tradicional no por el momento en que se aplica, sino por el uso que se da a la información que produce. Una prueba aplicada al final de una unidad puede ser formativa si sus resultados sirven para reorientar la enseñanza; y una lista de cotejo aplicada a mitad de proceso puede ser meramente sumativa si solo se archiva para asignar una nota.

El malentendido más extendido consiste en creer que evaluar formativamente significa evaluar con más frecuencia. Un docente puede aplicar diez instrumentos en un bimestre y no haber ofrecido jamás una retroalimentación que permita al estudiante identificar dónde está su error y cómo corregirlo. En ese caso ha multiplicado el registro, no la formación.

La retroalimentación efectiva, según la investigación disponible, cumple tres condiciones: es descriptiva antes que valorativa, señala la distancia entre el desempeño actual y el esperado, y ofrece una ruta concreta de mejora. Decirle a un estudiante «te faltó argumentar mejor» no cumple ninguna de las tres. Decirle «tu conclusión afirma algo que tus dos ejemplos no sostienen; agrega un dato que la respalde» cumple las tres.

Existe, sin embargo, una tensión que los sistemas educativos rara vez reconocen. La retroalimentación descrita exige tiempo por estudiante, y ese tiempo compite con la cobertura curricular. Los docentes que la practican con rigor suelen avanzar menos contenidos. Mientras la evaluación del propio sistema siga premiando la cobertura, la evaluación formativa seguirá siendo una recomendación que se cumple a medias."""

TEXTO_2 = """Durante décadas se asumió que la lengua materna de los estudiantes indígenas era un obstáculo para el aprendizaje escolar y que el camino consistía en reemplazarla cuanto antes por el castellano. Los resultados de esa política fueron pobres y, con frecuencia, contraproducentes: los niños no consolidaban la lectura en ninguna de las dos lenguas.

La evidencia acumulada apunta en dirección contraria. Un estudiante que aprende a leer primero en la lengua que domina construye con mayor solidez las habilidades de decodificación y comprensión, y luego las transfiere a la segunda lengua. Lo que se transfiere no es el vocabulario, sino la competencia lectora subyacente: la conciencia de que los signos representan sonidos y de que los textos tienen una estructura.

Esto explica una paradoja aparente. Los programas que dedican más tiempo a la lengua originaria en los primeros grados suelen obtener, hacia el cuarto o quinto grado, mejores resultados en castellano que los programas que la excluyeron desde el inicio. El tiempo invertido en la lengua materna no se resta al castellano: lo prepara.

Conviene precisar un límite. La transferencia ocurre cuando existe enseñanza sistemática en ambas lenguas y materiales adecuados en la lengua originaria. Cuando el programa se limita a usar la lengua materna como puente oral, sin desarrollar la lectura en ella, la ventaja descrita no aparece."""

BANCO_HG = [
 # ---------- COMPRENSIÓN LECTORA — TEXTO 1 ----------
 {"tipo":"lectura","texto":1,
  "pregunta":"Según el texto 1, ¿qué distingue a la evaluación formativa de la tradicional?",
  "alternativas":["El momento en que se aplica","El uso que se da a la información que produce","La cantidad de instrumentos empleados","El tipo de instrumento utilizado","La nota que se asigna"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"¿Cuál es el malentendido más extendido que señala el autor?",
  "alternativas":["Que la evaluación formativa no requiere instrumentos","Que evaluar formativamente significa evaluar con más frecuencia","Que la retroalimentación debe ser oral","Que solo el docente puede evaluar","Que la evaluación formativa no lleva nota"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"De acuerdo con el texto, «te faltó argumentar mejor» es un ejemplo de retroalimentación:",
  "alternativas":["Descriptiva y útil","Que no cumple ninguna de las tres condiciones señaladas","Valorativa pero suficiente","Formativa aunque incompleta","Ejemplar"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"¿Cuál de las siguientes NO es una condición de la retroalimentación efectiva según el texto?",
  "alternativas":["Ser descriptiva antes que valorativa","Señalar la distancia entre el desempeño actual y el esperado","Ofrecer una ruta concreta de mejora","Ser inmediata y pública","Todas son condiciones señaladas"],"correcta":"D"},
 {"tipo":"lectura","texto":1,
  "pregunta":"La tensión que el autor considera poco reconocida por los sistemas educativos es:",
  "alternativas":["Entre docentes y directivos","Entre el tiempo que exige la retroalimentación y la cobertura curricular","Entre evaluación escrita y oral","Entre padres y escuela","Entre teoría y práctica pedagógica"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"Se infiere del último párrafo que, para que la evaluación formativa se generalice, sería necesario:",
  "alternativas":["Aumentar el número de evaluaciones","Cambiar aquello que el propio sistema premia","Reducir el número de estudiantes por aula únicamente","Eliminar las notas","Capacitar solo a los directivos"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"«Ha multiplicado el registro, no la formación» significa que el docente:",
  "alternativas":["Enseñó más contenidos","Acumuló datos sin producir aprendizaje","Formó mejor a sus estudiantes","Evaluó de manera formativa","Redujo su carga administrativa"],"correcta":"B"},
 {"tipo":"lectura","texto":1,
  "pregunta":"Según el texto, una prueba aplicada al final de una unidad:",
  "alternativas":["Nunca puede ser formativa","Puede ser formativa si sus resultados reorientan la enseñanza","Siempre es formativa","Solo sirve para asignar notas","Debe evitarse"],"correcta":"B"},
 # ---------- COMPRENSIÓN LECTORA — TEXTO 2 ----------
 {"tipo":"lectura","texto":2,
  "pregunta":"¿Cuál era el supuesto de la política educativa cuestionada en el texto 2?",
  "alternativas":["Que la lengua materna facilitaba el aprendizaje","Que la lengua materna era un obstáculo que debía reemplazarse pronto","Que ambas lenguas debían enseñarse por igual","Que el castellano debía posponerse","Que la lectura no era prioritaria"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"Según el texto, lo que se transfiere de una lengua a otra es:",
  "alternativas":["El vocabulario","La competencia lectora subyacente","La pronunciación","La gramática","La escritura ortográfica"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"La «paradoja aparente» que menciona el texto consiste en que:",
  "alternativas":["Los niños bilingües leen menos","Dedicar más tiempo a la lengua originaria mejora luego los resultados en castellano","El castellano se aprende sin enseñanza","La lectura no se transfiere","Los materiales no importan"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"El límite que precisa el autor es que la transferencia ocurre solo si:",
  "alternativas":["El docente es bilingüe","Hay enseñanza sistemática en ambas lenguas y materiales en la originaria","Los padres hablan castellano","Se empieza en secundaria","Se excluye la lengua originaria"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"«El tiempo invertido en la lengua materna no se resta al castellano: lo prepara» expresa una relación de:",
  "alternativas":["Oposición","Fundamentación de la tesis del autor","Ejemplificación","Concesión","Digresión"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"Usar la lengua materna solo como puente oral, según el texto:",
  "alternativas":["Produce la ventaja descrita","No produce la ventaja descrita","Es la mejor estrategia","Equivale a la enseñanza sistemática","Mejora la ortografía"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"El propósito principal del texto 2 es:",
  "alternativas":["Narrar la historia de la educación rural","Sustentar por qué conviene alfabetizar primero en la lengua materna","Criticar a los docentes bilingües","Describir el currículo nacional","Proponer eliminar el castellano"],"correcta":"B"},
 {"tipo":"lectura","texto":2,
  "pregunta":"Se deduce que los resultados de la política antigua fueron pobres porque los niños:",
  "alternativas":["Aprendían dos lenguas a la vez","No consolidaban la lectura en ninguna de las dos lenguas","Rechazaban el castellano","Tenían pocos docentes","Abandonaban la escuela"],"correcta":"B"},
 # ---------- RAZONAMIENTO LÓGICO ----------
 {"tipo":"logico","pregunta":"En una IE hay 480 estudiantes. El 35% son de primaria y el resto de secundaria. ¿Cuántos son de secundaria?",
  "alternativas":["168","312","288","192","360"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Un docente corrige 12 pruebas en 30 minutos. Al mismo ritmo, ¿cuántas corrige en 2 horas?",
  "alternativas":["36","48","24","60","40"],"correcta":"B"},
 {"tipo":"logico","pregunta":"El precio de un libro subió de S/ 40 a S/ 50. ¿Cuál fue el porcentaje de aumento?",
  "alternativas":["20%","25%","10%","30%","15%"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Si todos los profesores de la IE son colegiados y algunos colegiados tienen maestría, se concluye necesariamente que:",
  "alternativas":["Todos los profesores tienen maestría","Algunos colegiados son profesores","Ningún profesor tiene maestría","Todos los colegiados son profesores","Algunos profesores no son colegiados"],"correcta":"B"},
 {"tipo":"logico","pregunta":"¿Qué número continúa? 3, 6, 12, 24, ...",
  "alternativas":["36","48","30","54","42"],"correcta":"B"},
 {"tipo":"logico","pregunta":"¿Qué número continúa? 2, 5, 10, 17, 26, ...",
  "alternativas":["35","37","36","38","40"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Cinco docentes se saludan dándose la mano una sola vez cada par. ¿Cuántos saludos hay?",
  "alternativas":["20","10","15","25","5"],"correcta":"B"},
 {"tipo":"logico","pregunta":"En un aula, la razón de varones a mujeres es 3 a 5. Si hay 40 estudiantes, ¿cuántas mujeres hay?",
  "alternativas":["15","25","20","24","30"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Un aula se pinta en 6 días con 4 pintores. ¿Cuántos días tardarán 3 pintores al mismo ritmo?",
  "alternativas":["4,5 días","8 días","6 días","9 días","12 días"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Ana es mayor que Beto. Carla es menor que Beto. Diana es mayor que Ana. ¿Quién es la mayor?",
  "alternativas":["Ana","Diana","Beto","Carla","No se puede saber"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Si la premisa «si estudia, aprueba» es verdadera y sabemos que NO aprobó, se concluye que:",
  "alternativas":["Estudió","No estudió","Estudió poco","Aprobó igual","No se puede concluir nada"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Un descuento del 20% sobre S/ 250, seguido de otro 10% sobre el nuevo precio, deja un precio final de:",
  "alternativas":["S/ 175","S/ 180","S/ 200","S/ 190","S/ 170"],"correcta":"B"},
 {"tipo":"logico","pregunta":"El promedio de 4 notas es 14. Si se agrega una quinta nota de 19, el nuevo promedio es:",
  "alternativas":["14,5","15","16","15,5","14"],"correcta":"B"},
 {"tipo":"logico","pregunta":"De 60 docentes, 35 enseñan primaria, 30 secundaria y 8 ambos niveles. ¿Cuántos no enseñan en ninguno de esos niveles?",
  "alternativas":["5","3","7","2","0"],"correcta":"B"},
 {"tipo":"logico","pregunta":"«Ningún estudiante irresponsable aprueba. Luis aprobó». Se concluye que Luis:",
  "alternativas":["Es irresponsable","No es irresponsable","Estudió mucho","Es el mejor del aula","Copió"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Una sesión dura 45 minutos. Si inicia a las 8:20 a.m., ¿a qué hora termina?",
  "alternativas":["9:00 a.m.","9:05 a.m.","8:55 a.m.","9:15 a.m.","9:10 a.m."],"correcta":"B"},
 {"tipo":"logico","pregunta":"Si 3 cuadernos cuestan S/ 13,50, ¿cuánto cuestan 7 cuadernos?",
  "alternativas":["S/ 30,00","S/ 31,50","S/ 28,00","S/ 33,00","S/ 27,50"],"correcta":"B"},
 {"tipo":"logico","pregunta":"En una encuesta, 3 de cada 5 padres asistieron a la reunión. Si hay 200 padres, ¿cuántos NO asistieron?",
  "alternativas":["120","80","60","100","140"],"correcta":"B"},
 {"tipo":"logico","pregunta":"¿Qué figura sigue en la serie: 1 punto, 3 puntos, 6 puntos, 10 puntos, ...?",
  "alternativas":["13","15","14","16","12"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Un estudiante responde 40 de 50 preguntas correctamente. ¿Qué porcentaje acertó?",
  "alternativas":["75%","80%","85%","70%","90%"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Si p → q es verdadera y p es verdadera, entonces q es:",
  "alternativas":["Falsa","Verdadera","Indeterminada","Contradictoria","Irrelevante"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Cuatro docentes deben ubicarse en fila. ¿De cuántas maneras distintas pueden hacerlo?",
  "alternativas":["12","24","16","20","8"],"correcta":"B"},
 {"tipo":"logico","pregunta":"El 15% de los estudiantes de un aula de 40 faltó. ¿Cuántos asistieron?",
  "alternativas":["6","34","30","36","32"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Si un mapa tiene escala 1:50 000, 4 cm en el mapa equivalen en la realidad a:",
  "alternativas":["1 km","2 km","4 km","5 km","20 km"],"correcta":"B"},
 {"tipo":"logico","pregunta":"«Algunos docentes son tutores. Todos los tutores reciben capacitación». Se concluye que:",
  "alternativas":["Todos los docentes reciben capacitación","Algunos docentes reciben capacitación","Ningún docente recibe capacitación","Solo los tutores son docentes","No se concluye nada"],"correcta":"B"},
 {"tipo":"logico","pregunta":"Una biblioteca tiene 1200 libros. Si el 25% son de literatura y el 40% del resto son de ciencias, ¿cuántos son de ciencias?",
  "alternativas":["480","360","300","400","240"],"correcta":"B"},
]



BANCO_CCSS = [
 # ===== PEDAGÓGICO GENERAL =====
 {"competencia":"Enfoque por competencias","pregunta":"Una docente plantea a sus estudiantes analizar por qué su distrito sufre inundaciones y proponer medidas. Esta situación es pertinente al enfoque por competencias PRINCIPALMENTE porque:",
  "alternativas":["Cubre varios contenidos del área","Moviliza saberes diversos frente a un problema real del contexto","Permite aplicar una prueba escrita","Facilita el trabajo en grupo","Reduce el tiempo de exposición docente"],"correcta":"B"},
 {"competencia":"Enfoque por competencias","pregunta":"En el CNEB, una competencia se define como la facultad de:",
  "alternativas":["Memorizar información relevante","Combinar un conjunto de capacidades para lograr un propósito en una situación determinada","Repetir procedimientos aprendidos","Aprobar una evaluación estandarizada","Seguir instrucciones con precisión"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"Un docente devuelve las pruebas con la nota y la palabra «mejorar». Desde la evaluación formativa, la principal deficiencia es que:",
  "alternativas":["No usó una rúbrica","No señala la distancia con el desempeño esperado ni una ruta de mejora","Corrigió con demora","No socializó las notas","No aplicó coevaluación"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"El propósito central de la retroalimentación por descubrimiento o reflexión es:",
  "alternativas":["Dar la respuesta correcta de inmediato","Que el estudiante identifique por sí mismo su error mediante repreguntas","Asignar una calificación justa","Comparar entre estudiantes","Registrar evidencias para el portafolio"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"Los criterios de evaluación en el CNEB se derivan directamente de:",
  "alternativas":["Los contenidos de la unidad","Los estándares y desempeños de la competencia","El libro de texto","La cantidad de sesiones","El acuerdo con los padres"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"Un estudiante alcanza el nivel «En proceso» en una competencia. La decisión pedagógica más pertinente es:",
  "alternativas":["Repetir la misma actividad","Diseñar actividades que atiendan específicamente la dificultad identificada","Asignar tareas adicionales de refuerzo memorístico","Bajar el nivel de exigencia del criterio","Esperar al siguiente periodo"],"correcta":"B"},
 {"competencia":"Mediación y andamiaje","pregunta":"Un estudiante no logra elaborar una línea de tiempo solo, pero sí con apoyo del docente. Según Vygotsky, esa distancia corresponde a:",
  "alternativas":["El nivel de desarrollo real","La zona de desarrollo próximo","El nivel de desarrollo potencial alcanzado","La asimilación","La acomodación"],"correcta":"B"},
 {"competencia":"Mediación y andamiaje","pregunta":"El andamiaje docente es adecuado cuando:",
  "alternativas":["Se mantiene constante todo el año","Se retira progresivamente conforme el estudiante gana autonomía","Sustituye el trabajo del estudiante","Se aplica solo a quienes van atrasados","Consiste en dar la respuesta"],"correcta":"B"},
 {"competencia":"Gestión del aula","pregunta":"Ante un conflicto entre dos estudiantes en plena sesión, la actuación más coherente con el enfoque de derechos es:",
  "alternativas":["Sancionar de inmediato a ambos","Detener la agresión y luego abrir un espacio de diálogo para restaurar el vínculo","Enviarlos a dirección sin intervenir","Ignorarlo para no perder la clase","Pedir que se disculpen frente al aula"],"correcta":"B"},
 {"competencia":"Atención a la diversidad","pregunta":"Una estudiante con discapacidad visual está incluida en el aula. La medida más pertinente para el área es:",
  "alternativas":["Exonerarla de las actividades cartográficas","Adaptar los materiales, por ejemplo con mapas en relieve, manteniendo el mismo propósito de aprendizaje","Asignarle trabajos más simples","Ubicarla con una compañera que le dicte todo","Evaluarla solo oralmente en todo el año"],"correcta":"B"},

 # ===== DIDÁCTICA DEL ÁREA =====
 {"competencia":"Didáctica de CCSS","pregunta":"El uso de fuentes históricas primarias en el aula tiene como propósito principal:",
  "alternativas":["Ilustrar la exposición del docente","Que el estudiante construya interpretaciones a partir de evidencia","Aumentar la cantidad de información","Facilitar la memorización de fechas","Reemplazar el libro de texto"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"Al trabajar con dos crónicas que narran de modo distinto un mismo hecho, el docente busca desarrollar sobre todo:",
  "alternativas":["La memoria de datos","La comprensión de que las fuentes tienen perspectiva e intencionalidad","La ortografía","La velocidad lectora","La expresión oral"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"La competencia «Construye interpretaciones históricas» supone que el estudiante:",
  "alternativas":["Memorice la secuencia de gobernantes","Explique procesos usando fuentes y comprendiendo el tiempo histórico","Ubique lugares en un mapa","Debata sobre política actual","Resuma capítulos del texto"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"La competencia «Gestiona responsablemente el espacio y el ambiente» se evidencia cuando el estudiante:",
  "alternativas":["Dibuja mapas con exactitud","Toma decisiones y actúa frente a una problemática ambiental de su territorio","Nombra las regiones naturales","Describe el clima","Ubica coordenadas"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"La competencia «Gestiona responsablemente los recursos económicos» busca que el estudiante:",
  "alternativas":["Aprenda contabilidad básica","Comprenda el sistema económico y tome decisiones responsables como consumidor y agente","Memorice indicadores macroeconómicos","Calcule intereses","Elabore presupuestos familiares únicamente"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"El uso de la historia local en el aula se justifica principalmente porque:",
  "alternativas":["Es más fácil de enseñar","Permite al estudiante vincular los procesos generales con su propia realidad y fuentes accesibles","Reduce la carga curricular","Evita el uso de textos","Es exigido por la norma"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"Al analizar un proceso histórico, distinguir entre causas estructurales y coyunturales permite al estudiante:",
  "alternativas":["Memorizar más causas","Comprender que los procesos tienen factores de distinta duración y peso","Simplificar el análisis","Evitar el uso de fuentes","Ordenar cronológicamente"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"El anacronismo en el análisis histórico consiste en:",
  "alternativas":["Confundir fechas","Juzgar el pasado exclusivamente con los valores y categorías del presente","Usar fuentes secundarias","Omitir la cronología","Analizar causas múltiples"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"Una salida de campo al centro histórico del distrito aporta principalmente porque:",
  "alternativas":["Motiva y distrae del aula","Convierte el entorno en fuente directa para la construcción de interpretaciones","Permite tomar fotografías","Sustituye la evaluación","Reduce el trabajo del docente"],"correcta":"B"},
 {"competencia":"Didáctica de CCSS","pregunta":"La lectura de un gráfico estadístico en CCSS desarrolla principalmente la capacidad de:",
  "alternativas":["Cálculo aritmético","Interpretar información cuantitativa para sustentar explicaciones sociales","Dibujar con precisión","Memorizar cifras","Redactar informes"],"correcta":"B"},

 # ===== DISCIPLINAR — HISTORIA =====
 {"competencia":"Historia","pregunta":"La reciprocidad y la redistribución fueron principios que organizaron fundamentalmente:",
  "alternativas":["El comercio colonial","La economía del Tahuantinsuyo","La república aristocrática","El sistema de haciendas","La era del guano"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"Las reformas borbónicas del siglo XVIII tuvieron como propósito central:",
  "alternativas":["Otorgar autonomía a los criollos","Recuperar el control económico y político de las colonias","Abolir la mita","Promover la independencia","Fundar universidades"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"Un factor estructural que explica la rebelión de Túpac Amaru II fue:",
  "alternativas":["La llegada de Napoleón","Los repartos mercantiles y los abusos de los corregidores","La independencia de Estados Unidos","La Guerra del Pacífico","El contrato Dreyfus"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"La era del guano se caracterizó económicamente por:",
  "alternativas":["La industrialización del país","La dependencia de la exportación de un solo recurso","El desarrollo del mercado interno","La reforma agraria","La diversificación productiva"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"La Reforma Agraria de 1969 tuvo como consecuencia principal:",
  "alternativas":["El fortalecimiento del sistema de haciendas","El desmontaje del régimen de hacienda y la transformación de la estructura de tenencia de tierras","El aumento de la exportación de guano","La creación del sistema universitario","La firma del Tratado de Ancón"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"El periodo de violencia iniciado en 1980 tuvo como escenario inicial:",
  "alternativas":["Lima metropolitana","Chuschi, Ayacucho","Cusco","La selva central","Trujillo"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"La Comisión de la Verdad y Reconciliación tuvo como mandato principal:",
  "alternativas":["Juzgar a los responsables","Esclarecer el proceso de violencia y proponer reparaciones y reformas","Redactar una nueva constitución","Organizar elecciones","Administrar justicia penal"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"El concepto de «memoria histórica» en la enseñanza escolar apunta a:",
  "alternativas":["Repetir la versión oficial","Reconocer las distintas experiencias del pasado y sus efectos en el presente","Evitar temas conflictivos","Memorizar fechas de conflictos","Neutralizar el juicio ético"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"El proceso de descentralización iniciado en 2002 en el Perú implicó:",
  "alternativas":["La supresión de los municipios","La creación de gobiernos regionales con competencias transferidas","La centralización del presupuesto","La eliminación de las UGEL","La reforma del Poder Judicial"],"correcta":"B"},
 {"competencia":"Historia","pregunta":"El concepto de «tiempo de larga duración» es útil en el aula para que el estudiante comprenda:",
  "alternativas":["Las fechas exactas de los hechos","Que hay procesos que cambian lentamente a lo largo de siglos","La biografía de los personajes","Los conflictos actuales","La cronología absoluta"],"correcta":"B"},

 # ===== DISCIPLINAR — GEOGRAFÍA Y AMBIENTE =====
 {"competencia":"Geografía","pregunta":"El concepto de «territorio» se diferencia del de «espacio geográfico» porque incorpora:",
  "alternativas":["Solo elementos físicos","Las relaciones de poder y apropiación social del espacio","Únicamente coordenadas","La altitud","El clima"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"La vulnerabilidad frente a un desastre depende principalmente de:",
  "alternativas":["La magnitud del fenómeno natural","Las condiciones sociales, económicas y físicas de la población expuesta","La ubicación geográfica solamente","La estación del año","La densidad poblacional únicamente"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"El riesgo de desastre se entiende como la relación entre:",
  "alternativas":["Peligro y lluvia","Peligro y vulnerabilidad","Población y territorio","Altitud y clima","Economía y ambiente"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"El Fenómeno El Niño se explica fundamentalmente por:",
  "alternativas":["El deshielo de glaciares","El calentamiento anómalo de las aguas superficiales del Pacífico ecuatorial","La deforestación amazónica","La actividad sísmica","La contaminación del aire"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"Las ocho regiones naturales fueron propuestas por:",
  "alternativas":["Antonio Raimondi","Javier Pulgar Vidal","María Rostworowski","Carlos Monge","Emilio Romero"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"El desarrollo sostenible se define como aquel que:",
  "alternativas":["Prioriza el crecimiento económico","Satisface las necesidades presentes sin comprometer las de las generaciones futuras","Detiene toda actividad extractiva","Depende de la ayuda internacional","Se limita a la conservación"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"Un conflicto socioambiental por actividad minera se analiza mejor en el aula:",
  "alternativas":["Tomando partido desde el inicio","Identificando los actores, sus intereses y las evidencias que sustentan cada posición","Evitando el tema por polémico","Solo desde el aspecto legal","Solo desde el aspecto económico"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"La cuenca hidrográfica es una unidad de gestión pertinente porque:",
  "alternativas":["Coincide con los límites políticos","Integra el ciclo del agua y las actividades humanas de un mismo sistema","Es más fácil de delimitar","Corresponde a una región natural","Facilita el turismo"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"El uso de un Sistema de Información Geográfica en el aula permite principalmente:",
  "alternativas":["Dibujar mapas más bonitos","Superponer capas de información para analizar relaciones territoriales","Ubicar países","Medir distancias","Reemplazar la salida de campo"],"correcta":"B"},
 {"competencia":"Geografía","pregunta":"La migración interna en el Perú del siglo XX se explica principalmente por:",
  "alternativas":["Razones climáticas","La búsqueda de oportunidades económicas y educativas en las ciudades","Políticas de reubicación","Conflictos limítrofes","Programas de vivienda"],"correcta":"B"},

 # ===== DISCIPLINAR — ECONOMÍA Y CIUDADANÍA =====
 {"competencia":"Economía","pregunta":"La inflación se define como:",
  "alternativas":["El alza de un producto específico","El aumento sostenido y generalizado del nivel de precios","La caída del empleo","El aumento del PBI","La devaluación de la moneda"],"correcta":"B"},
 {"competencia":"Economía","pregunta":"El Banco Central de Reserva del Perú tiene como finalidad principal:",
  "alternativas":["Recaudar impuestos","Preservar la estabilidad monetaria","Otorgar créditos a empresas","Administrar el presupuesto público","Fiscalizar a los bancos"],"correcta":"B"},
 {"competencia":"Economía","pregunta":"El costo de oportunidad se refiere a:",
  "alternativas":["El precio de un bien","El valor de la mejor alternativa a la que se renuncia al elegir","El costo de producción","El impuesto pagado","La utilidad obtenida"],"correcta":"B"},
 {"competencia":"Economía","pregunta":"La informalidad laboral afecta principalmente a los trabajadores porque:",
  "alternativas":["Reduce sus ingresos nominales","Los deja sin protección social ni derechos laborales reconocidos","Aumenta sus impuestos","Limita su movilidad geográfica","Reduce la competencia"],"correcta":"B"},
 {"competencia":"Economía","pregunta":"Enseñar educación financiera en secundaria busca principalmente que el estudiante:",
  "alternativas":["Aprenda a invertir en bolsa","Tome decisiones informadas y responsables sobre ahorro, gasto y endeudamiento","Memorice productos bancarios","Calcule intereses compuestos","Elija una carrera rentable"],"correcta":"B"},
 {"competencia":"Ciudadanía","pregunta":"El enfoque de derechos en la escuela implica que el estudiante sea considerado:",
  "alternativas":["Receptor de contenidos","Sujeto de derechos con capacidad de participación","Beneficiario de servicios","Responsable de sus resultados","Usuario del sistema"],"correcta":"B"},
 {"competencia":"Ciudadanía","pregunta":"Un municipio escolar cumple su función formativa cuando:",
  "alternativas":["Organiza actividades recreativas","Constituye un espacio real de deliberación y toma de decisiones estudiantiles","Es elegido anualmente","Apoya a la dirección","Recauda fondos"],"correcta":"B"},
 {"competencia":"Ciudadanía","pregunta":"La interculturalidad crítica se diferencia de la interculturalidad funcional porque:",
  "alternativas":["Celebra las diferencias culturales","Cuestiona las relaciones de poder y desigualdad entre culturas","Promueve el folclore","Enseña lenguas originarias","Evita el conflicto"],"correcta":"B"},
 {"competencia":"Ciudadanía","pregunta":"El Estado peruano se define constitucionalmente como:",
  "alternativas":["Federal y presidencialista","Unitario, representativo y descentralizado","Confederado","Parlamentario","Monárquico constitucional"],"correcta":"B"},
 {"competencia":"Ciudadanía","pregunta":"El control ciudadano sobre las autoridades se ejerce, entre otros mecanismos, mediante:",
  "alternativas":["El voto obligatorio","La revocatoria y la rendición de cuentas","El referéndum exclusivamente","La huelga","La consulta previa"],"correcta":"B"},
]



BANCO_DPCC = [
 # ===== PEDAGÓGICO Y CURRICULAR =====
 {"competencia":"Enfoque del área","pregunta":"El área de DPCC se sustenta principalmente en los enfoques:",
  "alternativas":["Comunicativo y por indagación","De derechos, intercultural, de igualdad de género y de búsqueda del bien común","Conductista y por objetivos","Tecnológico y ambiental","Histórico y crítico"],"correcta":"B"},
 {"competencia":"Enfoque del área","pregunta":"Las dos competencias del área de DPCC en el CNEB son:",
  "alternativas":["Lee y escribe diversos textos","Construye su identidad y Convive y participa democráticamente","Indaga y explica el mundo físico","Gestiona proyectos y resuelve problemas","Se comunica y aprecia manifestaciones artísticas"],"correcta":"B"},
 {"competencia":"Enfoque del área","pregunta":"La competencia «Construye su identidad» supone que el estudiante:",
  "alternativas":["Memorice los derechos humanos","Reconozca sus características, gestione sus emociones y actúe según principios éticos","Participe en elecciones escolares","Elabore proyectos productivos","Analice normas legales"],"correcta":"B"},
 {"competencia":"Enfoque del área","pregunta":"La competencia «Convive y participa democráticamente» se evidencia cuando el estudiante:",
  "alternativas":["Obedece las normas del aula","Delibera sobre asuntos públicos y participa en acciones que promueven el bien común","Conoce la Constitución","Respeta a sus mayores","Cumple sus tareas"],"correcta":"B"},
 {"competencia":"Enfoque del área","pregunta":"El enfoque de búsqueda del bien común implica que la escuela promueva:",
  "alternativas":["El éxito individual","Relaciones solidarias orientadas al bienestar de todos","La competencia entre estudiantes","El cumplimiento de normas","La eficiencia administrativa"],"correcta":"B"},
 {"competencia":"Didáctica del área","pregunta":"La deliberación sobre asuntos públicos en el aula requiere fundamentalmente que:",
  "alternativas":["Todos opinen libremente sin restricción","Los estudiantes sustenten sus posiciones con información y consideren distintas perspectivas","El docente fije la conclusión correcta","Se vote al final","Se evite el desacuerdo"],"correcta":"B"},
 {"competencia":"Didáctica del área","pregunta":"Un asunto público se distingue de un asunto privado porque:",
  "alternativas":["Es más polémico","Afecta o interesa al conjunto de la comunidad y admite deliberación colectiva","Aparece en los medios","Involucra al Estado únicamente","Es de interés del docente"],"correcta":"B"},
 {"competencia":"Didáctica del área","pregunta":"Al abordar un tema controversial, el rol del docente de DPCC es principalmente:",
  "alternativas":["Imponer la posición correcta","Garantizar que se examinen argumentos y evidencias de distintas posiciones","Evitar el tema","Dejar que decidan sin orientación","Encuestar a los estudiantes"],"correcta":"B"},
 {"competencia":"Didáctica del área","pregunta":"El estudio de casos es pertinente en DPCC porque permite:",
  "alternativas":["Cubrir más contenidos","Analizar dilemas reales y tomar posición fundamentada","Simplificar la evaluación","Evitar la lectura","Trabajar individualmente"],"correcta":"B"},
 {"competencia":"Didáctica del área","pregunta":"Un proyecto participativo estudiantil cumple su propósito formativo cuando:",
  "alternativas":["Se presenta en la feria escolar","Los estudiantes identifican un problema real y ejecutan acciones que buscan incidir en él","Lo dirige el docente","Obtiene financiamiento","Se documenta en un informe"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"Para evaluar «Convive y participa democráticamente» el instrumento más pertinente es:",
  "alternativas":["Una prueba de opción múltiple","Una rúbrica aplicada durante la observación del desempeño en situaciones reales","Un cuestionario de conocimientos","Un examen oral","Una lista de asistencia"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"En una rúbrica, los descriptores deben estar redactados en términos de:",
  "alternativas":["Actitudes generales","Desempeños observables","Contenidos temáticos","Calificaciones numéricas","Rasgos de personalidad"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"La autoevaluación en DPCC aporta principalmente porque:",
  "alternativas":["Ahorra tiempo al docente","Desarrolla la metacognición y la responsabilidad del estudiante sobre su aprendizaje","Genera notas más altas","Evita conflictos","Reemplaza la heteroevaluación"],"correcta":"B"},
 {"competencia":"Evaluación formativa","pregunta":"Al evaluar la competencia «Construye su identidad», NO corresponde:",
  "alternativas":["Observar desempeños en situaciones cotidianas","Calificar los rasgos de personalidad del estudiante","Usar rúbricas con criterios claros","Registrar evidencias en el portafolio","Dar retroalimentación descriptiva"],"correcta":"B"},
 {"competencia":"Tutoría y convivencia","pregunta":"La convivencia escolar democrática se construye principalmente mediante:",
  "alternativas":["Un reglamento estricto","Normas construidas participativamente y aplicadas con criterios restaurativos","Sanciones ejemplares","Vigilancia permanente","Premios al buen comportamiento"],"correcta":"B"},
 {"competencia":"Tutoría y convivencia","pregunta":"Ante un caso de acoso escolar, el primer paso conforme a la normativa vigente es:",
  "alternativas":["Citar a los padres del agresor","Reportar el caso en el portal SíseVe y activar el protocolo correspondiente","Sancionar al agresor","Cambiar de aula a la víctima","Investigar en privado"],"correcta":"B"},
 {"competencia":"Tutoría y convivencia","pregunta":"El enfoque restaurativo frente a una falta busca principalmente:",
  "alternativas":["Aplicar la sanción proporcional","Reparar el daño y restablecer el vínculo entre las partes","Documentar el incidente","Prevenir la reincidencia mediante castigo","Informar a la UGEL"],"correcta":"B"},
 {"competencia":"Tutoría y convivencia","pregunta":"Ante la sospecha de violencia familiar contra un estudiante, el docente debe:",
  "alternativas":["Confrontar a la familia","Reportar al directivo y activar el protocolo, sin investigar por cuenta propia","Guardar reserva absoluta","Aconsejar al estudiante que hable con sus padres","Esperar más evidencias"],"correcta":"B"},
 {"competencia":"Atención a la diversidad","pregunta":"El enfoque de igualdad de género en DPCC implica:",
  "alternativas":["Tratar a todos exactamente igual","Reconocer y remover las desigualdades que limitan a mujeres y varones por su género","Separar actividades por sexo","Evitar el tema por controversial","Priorizar a las mujeres"],"correcta":"B"},
 {"competencia":"Atención a la diversidad","pregunta":"Ante un estudiante que expresa un prejuicio discriminatorio en clase, lo más pertinente es:",
  "alternativas":["Sancionarlo de inmediato","Abrir el análisis del prejuicio con evidencia y confrontarlo pedagógicamente","Ignorar el comentario","Cambiar de tema","Pedirle que se disculpe"],"correcta":"B"},

 # ===== DISCIPLINAR — ÉTICA E IDENTIDAD =====
 {"competencia":"Ética","pregunta":"La diferencia entre ética y moral radica en que la ética es:",
  "alternativas":["Un conjunto de costumbres","La reflexión teórica y crítica sobre la moral","Un código legal","Una norma religiosa","Un hábito social"],"correcta":"B"},
 {"competencia":"Ética","pregunta":"Un dilema moral se caracteriza porque:",
  "alternativas":["Tiene una solución evidente","Enfrenta valores igualmente legítimos entre los que hay que optar","Se resuelve con la norma","No admite argumentación","Solo tiene una respuesta correcta"],"correcta":"B"},
 {"competencia":"Ética","pregunta":"Según Kohlberg, actuar correctamente por temor al castigo corresponde al nivel:",
  "alternativas":["Convencional","Preconvencional","Posconvencional","Autónomo","Universal"],"correcta":"B"},
 {"competencia":"Ética","pregunta":"El nivel posconvencional del desarrollo moral se caracteriza porque la persona:",
  "alternativas":["Cumple la norma para evitar sanciones","Actúa según principios éticos universales que puede sustentar racionalmente","Busca aprobación social","Obedece a la autoridad","Sigue la costumbre del grupo"],"correcta":"B"},
 {"competencia":"Ética","pregunta":"La autonomía moral supone que la persona:",
  "alternativas":["Actúa sin considerar a los demás","Se da a sí misma principios que puede justificar y asume las consecuencias","Rechaza toda norma","Obedece su conciencia sin reflexión","Depende del criterio del grupo"],"correcta":"B"},
 {"competencia":"Identidad","pregunta":"La identidad personal, según el enfoque del área, se construye:",
  "alternativas":["Al nacer y permanece fija","De manera dinámica en la interacción con otros y con la cultura","Solo en la adolescencia","Por herencia familiar","Por decisión individual aislada"],"correcta":"B"},
 {"competencia":"Identidad","pregunta":"La autorregulación emocional implica que el estudiante:",
  "alternativas":["Reprima lo que siente","Reconozca sus emociones y module su expresión de modo adecuado al contexto","Evite situaciones difíciles","Exprese todo lo que siente","Controle las emociones de otros"],"correcta":"B"},
 {"competencia":"Identidad","pregunta":"El proyecto de vida en el marco de DPCC se entiende como:",
  "alternativas":["La elección de una carrera","La construcción reflexiva de metas coherentes con los propios valores y el contexto","Un plan económico","Un documento escolar","Una lista de aspiraciones"],"correcta":"B"},
 {"competencia":"Identidad","pregunta":"La educación sexual integral, según el CNEB, aborda la sexualidad como:",
  "alternativas":["Un tema exclusivamente biológico","Una dimensión que integra lo biológico, afectivo, ético y social","Un asunto de la familia","Un contenido de secundaria superior","Un tema de riesgo"],"correcta":"B"},
 {"competencia":"Identidad","pregunta":"Trabajar la empatía en el aula supone desarrollar la capacidad de:",
  "alternativas":["Sentir lástima por otros","Comprender la perspectiva y el estado emocional del otro","Estar de acuerdo con todos","Evitar los conflictos","Ayudar materialmente"],"correcta":"B"},

 # ===== DISCIPLINAR — CIUDADANÍA, ESTADO Y DERECHOS =====
 {"competencia":"Derechos humanos","pregunta":"Los derechos humanos se caracterizan por ser:",
  "alternativas":["Otorgados por el Estado","Universales, inalienables e indivisibles","Condicionados al cumplimiento de deberes","Exclusivos de los ciudadanos","Renunciables"],"correcta":"B"},
 {"competencia":"Derechos humanos","pregunta":"Los derechos de segunda generación corresponden a los derechos:",
  "alternativas":["Civiles y políticos","Económicos, sociales y culturales","De los pueblos","Ambientales","Digitales"],"correcta":"B"},
 {"competencia":"Derechos humanos","pregunta":"El Estado tiene frente a los derechos humanos las obligaciones de:",
  "alternativas":["Solo no violarlos","Respetar, proteger y garantizar","Difundirlos","Legislarlos","Financiarlos"],"correcta":"B"},
 {"competencia":"Derechos humanos","pregunta":"El interés superior del niño implica que, ante decisiones que lo afecten:",
  "alternativas":["Decide la familia","Se prioriza aquello que mejor garantice sus derechos","Decide la autoridad educativa","Se consulta al niño solamente","Prevalece el criterio económico"],"correcta":"B"},
 {"competencia":"Derechos humanos","pregunta":"El Convenio 169 de la OIT reconoce a los pueblos indígenas el derecho a:",
  "alternativas":["La autonomía territorial plena","La consulta previa sobre medidas que los afecten","La exoneración tributaria","La representación parlamentaria reservada","La educación gratuita"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La democracia, más allá del voto, supone:",
  "alternativas":["Elecciones periódicas únicamente","Participación, deliberación pública y respeto a los derechos de las minorías","Gobierno de la mayoría sin límites","Alternancia en el poder","Existencia de partidos"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"El Estado de derecho implica fundamentalmente que:",
  "alternativas":["El gobierno es elegido","El poder está sometido a la ley y a la Constitución","Existe separación de poderes solamente","Hay elecciones libres","Se respeta la propiedad privada"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"El poder encargado de controlar la constitucionalidad de las leyes en el Perú es:",
  "alternativas":["El Congreso","El Tribunal Constitucional","La Corte Suprema","La Defensoría del Pueblo","El Ministerio Público"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La Defensoría del Pueblo tiene como función principal:",
  "alternativas":["Juzgar a funcionarios","Defender los derechos de las personas frente a la administración estatal","Investigar delitos","Administrar justicia","Fiscalizar el presupuesto"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La acción de amparo procede para:",
  "alternativas":["Proteger la libertad personal","Proteger derechos constitucionales distintos a la libertad individual y al acceso a la información","Acceder a información pública","Impugnar normas","Exigir el cumplimiento de una ley"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La acción de hábeas corpus protege específicamente:",
  "alternativas":["El derecho a la información","La libertad individual y derechos conexos","El derecho a la salud","La propiedad","La identidad"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"El presupuesto participativo constituye un mecanismo de:",
  "alternativas":["Control judicial","Participación ciudadana en la asignación de recursos públicos","Recaudación tributaria","Fiscalización parlamentaria","Auditoría privada"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La corrupción afecta a la democracia principalmente porque:",
  "alternativas":["Encarece los servicios","Desvía recursos públicos y erosiona la confianza en las instituciones","Genera desempleo","Reduce la inversión extranjera","Aumenta la burocracia"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La cultura de la legalidad supone que los ciudadanos:",
  "alternativas":["Temen la sanción","Reconocen la norma como legítima y la cumplen por convicción","Conocen todas las leyes","Denuncian a los infractores","Participan en elecciones"],"correcta":"B"},
 {"competencia":"Estado y democracia","pregunta":"La consulta previa en el Perú debe realizarse:",
  "alternativas":["Después de aprobada la medida","Antes de adoptar medidas que afecten directamente a los pueblos indígenas","Solo si lo solicita la comunidad","Cada cinco años","Durante la ejecución del proyecto"],"correcta":"B"},
 {"competencia":"Ciudadanía global","pregunta":"La ciudadanía ambiental implica reconocer que:",
  "alternativas":["El ambiente es responsabilidad del Estado","Las decisiones individuales y colectivas tienen efectos ambientales que involucran derechos","La conservación limita el desarrollo","El cambio climático es lejano","La tecnología resolverá el problema"],"correcta":"B"},
 {"competencia":"Ciudadanía global","pregunta":"La migración venezolana en el Perú, abordada desde DPCC, debe analizarse principalmente:",
  "alternativas":["Desde el impacto económico","Desde el enfoque de derechos y la deconstrucción de prejuicios","Desde la seguridad ciudadana","Desde la normativa migratoria","Evitando el tema"],"correcta":"B"},
 {"competencia":"Ciudadanía global","pregunta":"La desinformación en redes sociales se combate en el aula desarrollando:",
  "alternativas":["Prohibición del uso de redes","El pensamiento crítico y la verificación de fuentes","Control parental","Uso exclusivo de textos impresos","Denuncia de cuentas falsas"],"correcta":"B"},
 {"competencia":"Ciudadanía global","pregunta":"Los Objetivos de Desarrollo Sostenible constituyen:",
  "alternativas":["Normas obligatorias para los Estados","Una agenda global acordada para el año 2030","Un tratado comercial","Una política peruana","Un programa de la OEA"],"correcta":"B"},
 {"competencia":"Ciudadanía global","pregunta":"El voluntariado juvenil aporta a la formación ciudadana cuando:",
  "alternativas":["Suma horas de servicio","Se articula con la reflexión crítica sobre las causas del problema atendido","Es obligatorio","Recibe reconocimiento público","Lo organiza la institución"],"correcta":"B"},
]


ESPECIALIDADES = {
    "Ciencias Sociales (Secundaria)": BANCO_CCSS,
    "DPCC (Secundaria)": BANCO_DPCC,
}

TEXTOS = {1: TEXTO_1, 2: TEXTO_2}


# ================================================================
# INTERFAZ
# ================================================================

def tab_simulador_nombramiento(config=None):
    st.subheader("🎯 Simulador de Nombramiento Docente")
    st.caption("Estructura oficial de la Prueba Nacional: 75 preguntas, "
               "3 h 45 min. Preguntas originales sobre la matriz de "
               "evaluación; los cuadernillos oficiales se descargan de "
               "evaluaciondocente.perueduca.pe")

    ss = st.session_state
    ss.setdefault("sim_estado", "inicio")
    ss.setdefault("sim_resp", {})

    # ---------- PANTALLA DE INICIO ----------
    if ss["sim_estado"] == "inicio":
        c1, c2 = st.columns(2)
        with c1:
            esp = st.selectbox("Especialidad:", list(ESPECIALIDADES.keys()),
                               key="sim_esp")
        with c2:
            num = st.number_input("N° de simulacro:", 1, 30, 1, key="sim_num",
                                  help="Cada número genera una combinación "
                                       "distinta de preguntas.")
        modo = st.radio(
            "Modo:",
            ["Examen completo cronometrado (3 h 45 min)",
             "Solo Habilidades Generales (25 preg.)",
             "Solo Conocimientos de la especialidad (50 preg.)",
             "Práctica sin cronómetro"],
            key="sim_modo")

        st.info(f"**Puntajes oficiales** · Habilidades Generales: "
                f"{HG_PREGUNTAS} preg. × {HG_VALOR} = {HG_MAXIMO} pts (sin "
                f"mínimo) · Conocimientos: {CPD_PREGUNTAS} preg. × "
                f"{CPD_VALOR} = {CPD_MAXIMO} pts (**mínimo {CPD_MINIMO}**) · "
                f"Total mínimo para clasificar: **{MINIMO_GLOBAL} pts**")

        if st.button("▶️ INICIAR SIMULACRO", type="primary",
                     use_container_width=True, key="sim_go"):
            ss["sim_data"] = armar_simulacro(BANCO_HG, ESPECIALIDADES[esp],
                                             semilla=int(num) * 17)
            ss["sim_modo_activo"] = modo
            ss["sim_esp_activa"] = esp
            ss["sim_num_activo"] = int(num)
            ss["sim_resp"] = {}
            ss["sim_inicio"] = datetime.now()
            ss["sim_estado"] = "rindiendo"
            st.rerun()
        return

    # ---------- RINDIENDO ----------
    if ss["sim_estado"] == "rindiendo":
        sim = ss["sim_data"]
        modo = ss["sim_modo_activo"]
        con_tiempo = "cronometrado" in modo
        ver_hg = "Conocimientos" not in modo
        ver_cpd = "Habilidades" not in modo

        if con_tiempo:
            transcurrido = datetime.now() - ss["sim_inicio"]
            restante = timedelta(minutes=MINUTOS_TOTAL) - transcurrido
            if restante.total_seconds() <= 0:
                st.error("⏰ Se agotó el tiempo. El simulacro se cerró "
                         "automáticamente, igual que en la prueba real.")
                ss["sim_estado"] = "resultado"
                st.rerun()
            h = int(restante.total_seconds() // 3600)
            m = int((restante.total_seconds() % 3600) // 60)
            color = "#B3161C" if restante.total_seconds() < 1800 else "#12307F"
            st.markdown(
                f"<div style='position:sticky;top:0;z-index:99;background:{color};"
                f"color:#fff;padding:10px;border-radius:8px;text-align:center;"
                f"font-weight:900;font-size:1.1rem;'>⏱️ Tiempo restante: "
                f"{h} h {m:02d} min</div>", unsafe_allow_html=True)
            st.caption("El cronómetro avanza al recargar la página. "
                       "Responde y pulsa «Terminar» antes de que llegue a cero.")

        total_v = (len(sim["hg"]) if ver_hg else 0) + \
                  (len(sim["cpd"]) if ver_cpd else 0)
        st.progress(len(ss["sim_resp"]) / max(total_v, 1),
                    text=f"Respondidas: {len(ss['sim_resp'])} de {total_v}")

        if ver_hg:
            st.markdown("### Subprueba 1 · Habilidades Generales")
            textos_usados = sorted({p["texto"] for p in sim["hg"]
                                    if p.get("tipo") == "lectura"})
            for t in textos_usados:
                with st.expander(f"📖 Texto {t} — léelo antes de responder",
                                 expanded=True):
                    st.write(TEXTOS[t])
            for i, p in enumerate(sim["hg"]):
                _pregunta(f"hg{i}", i + 1, p)

        if ver_cpd:
            st.markdown(f"### Subprueba 2 · Conocimientos — "
                        f"{ss['sim_esp_activa']}")
            for i, p in enumerate(sim["cpd"]):
                _pregunta(f"cpd{i}", i + 1, p)

        st.markdown("---")
        if st.button("✅ TERMINAR Y VER RESULTADO", type="primary",
                     use_container_width=True, key="sim_fin"):
            ss["sim_estado"] = "resultado"
            st.rerun()
        if st.button("❌ Abandonar simulacro", use_container_width=True,
                     key="sim_salir"):
            ss["sim_estado"] = "inicio"
            st.rerun()
        return

    # ---------- RESULTADO ----------
    sim = ss["sim_data"]
    r = calificar(sim, ss["sim_resp"])
    etq, color, msg = r["veredicto"]

    st.markdown(
        f"<div style='background:{color};color:#fff;padding:18px;"
        f"border-radius:12px;text-align:center;'>"
        f"<div style='font-size:1.6rem;font-weight:900;'>{etq}</div>"
        f"<div style='font-size:2.6rem;font-weight:900;'>{r['total']} / "
        f"{r['max_total']}</div><div>{msg}</div></div>",
        unsafe_allow_html=True)

    st.markdown("### Detalle por subprueba")
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Habilidades Generales",
                  f"{r['pt_hg']} / {HG_MAXIMO}",
                  f"{r['ok_hg']} de {len(sim['hg'])} correctas")
        st.caption("Sin puntaje mínimo, pero suma al total.")
    with m2:
        st.metric("Conocimientos de la especialidad",
                  f"{r['pt_cpd']} / {CPD_MAXIMO}",
                  f"{r['ok_cpd']} de {len(sim['cpd'])} correctas")
        if r["pasa_cpd"]:
            st.success(f"Superó el mínimo de {CPD_MINIMO} puntos.")
        else:
            st.error(f"Faltaron {CPD_MINIMO - r['pt_cpd']} puntos para el "
                     f"mínimo de {CPD_MINIMO}. Este filtro elimina.")

    st.markdown("### Dónde reforzar")
    res = resumen_por_competencia(sim, ss["sim_resp"])
    for comp, d in sorted(res.items(), key=lambda x: x[1]["pct"]):
        col = "#0F7A34" if d["pct"] >= 70 else (
            "#E08900" if d["pct"] >= 50 else "#B3161C")
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;"
            f"padding:7px 12px;margin-bottom:5px;border-radius:8px;"
            f"background:#F5F7FB;border-left:5px solid {col};'>"
            f"<div style='flex:3;'><b>{comp}</b></div>"
            f"<div style='flex:4;background:#DDE2E8;border-radius:20px;"
            f"height:12px;'><div style='width:{d['pct']}%;background:{col};"
            f"height:12px;border-radius:20px;'></div></div>"
            f"<div style='flex:1;text-align:right;'>{d['ok']}/{d['total']}"
            f"</div></div>", unsafe_allow_html=True)

    with st.expander("Ver las preguntas falladas con su explicación"):
        for etiqueta, clave, lista in [("Habilidades Generales", "hg", sim["hg"]),
                                       ("Conocimientos", "cpd", sim["cpd"])]:
            fallas = [(i, p) for i, p in enumerate(lista)
                      if ss["sim_resp"].get(f"{clave}{i}") != p["correcta"]]
            if not fallas:
                continue
            st.markdown(f"**{etiqueta} — {len(fallas)} falladas**")
            for i, p in fallas:
                dada = ss["sim_resp"].get(f"{clave}{i}", "—")
                st.markdown(f"- {p['pregunta']}")
                st.markdown(
                    f"  <span style='color:#B3161C;'>Marcaste: {dada}</span> · "
                    f"<span style='color:#0F7A34;'>Correcta: {p['correcta']}) "
                    f"{p['alternativas'][LETRAS.index(p['correcta'])]}</span>",
                    unsafe_allow_html=True)

    if st.button("🔄 Rendir otro simulacro", type="primary",
                 use_container_width=True, key="sim_otro"):
        ss["sim_estado"] = "inicio"
        st.rerun()


def _pregunta(clave, num, p):
    """Dibuja una pregunta con sus cinco alternativas."""
    st.markdown(f"**{num}.** {p['pregunta']}")
    opciones = ["(sin responder)"] + [
        f"{LETRAS[k]}) {a}" for k, a in enumerate(p["alternativas"])]
    actual = st.session_state["sim_resp"].get(clave)
    idx = 0 if actual is None else LETRAS.index(actual) + 1
    sel = st.radio("", opciones, index=idx, key=f"w_{clave}",
                   label_visibility="collapsed")
    if sel == "(sin responder)":
        st.session_state["sim_resp"].pop(clave, None)
    else:
        st.session_state["sim_resp"][clave] = sel[0]
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
