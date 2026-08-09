# ================================================================
# FICHAS DE EDUCACIÓN CÍVICA — CEPRU UNSAAC
# Basado en el material oficial «Educación Cívica», Área D,
# Ciclo Primera Oportunidad 2024.
# ================================================================
"""Mismo formato que el módulo de Historia: por cada balota genera la
ficha de texto para completar a dos columnas y el banco de 20 preguntas
con cinco alternativas, en versión alumno y versión docente.

Reutiliza el motor de fichas_historia.py en lugar de duplicarlo: si un
día se corrige el diseño del PDF, se corrige en un solo sitio y todos
los cursos quedan iguales.

Integración en sistema_web.py:
    from fichas_civica import tab_fichas_civica

ESTADO: el temario oficial tiene 18 balotas. Esta primera entrega
incluye la Balota 1 (Derecho, Ley y Moral), completa y lista para
imprimir, como muestra del formato. Las balotas 2 a 18 se agregan a
la lista BALOTAS_CIVICA de la misma manera — mismo día se pueden ir
sumando sin tocar el resto del archivo.
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


BALOTAS_CIVICA = [{'num': 1,
  'titulo': 'Derecho, Ley y Moral',
  'secciones': [{'titulo': '1.1 EL DERECHO: CONCEPTO Y CLASES',
                 'items': ['La palabra Derecho viene del latín «{IUS}», '
                           'término con el que los romanos lo designaban.',
                           'Con el Corpus Iuris Civilis se aplicó la palabra '
                           '«{Directum}», que significa «recto», «lo que '
                           'está conforme a la regla».',
                           'Para Mario Alzamora Valdez, el Derecho es la '
                           'regulación de la {vida social} del hombre para '
                           'alcanzar la {justicia}.',
                           'Para Claude Du Pasquier, el Derecho es la '
                           'ordenación {social e imperativa} de la vida '
                           'humana orientada a la realización de {justicia}.',
                           'El {Derecho Objetivo} es el conjunto de normas '
                           'jurídicas que regulan la conducta de una persona '
                           'en relación a otra (Constitución, leyes, '
                           'códigos).',
                           'El {Derecho Subjetivo} es el conjunto de '
                           'prerrogativas, facultades y potestades que tiene '
                           'una persona, como el derecho a la {vida}, a la '
                           '{libertad} o a la propiedad.',
                           'Elementos del derecho subjetivo: el {sujeto '
                           'activo} (titular del derecho), el {sujeto '
                           'pasivo} (sobre quien recae el deber) y el '
                           '{objeto} del derecho.']},
                {'titulo': '1.2 FUENTES DEL DERECHO',
                 'items': ['Las fuentes del Derecho son los procedimientos '
                           'por los que se produce válidamente {normas '
                           'jurídicas} con carácter obligatorio.',
                           'Las fuentes {materiales o reales} hacen '
                           'referencia a los orígenes mediatos de la norma '
                           '(factores sociales, económicos, culturales).',
                           'Las fuentes {formales} son el origen inmediato '
                           'de las normas jurídicas: la ley, la costumbre, '
                           'la jurisprudencia, la doctrina y los principios '
                           'generales del derecho.',
                           'La {costumbre} es una forma de conducta '
                           'implantada por una colectividad, repetida de '
                           'forma uniforme y permanente, cuya observancia se '
                           'hace obligatoria.',
                           'La {jurisprudencia} es el conjunto de '
                           'resoluciones judiciales de la Corte Suprema y '
                           'del Tribunal Constitucional sobre una cuestión '
                           'determinada.',
                           'La {doctrina} son los estudios especializados '
                           'del derecho; carece de {fuerza legal '
                           'obligatoria}.',
                           'Según el artículo {139} de la Constitución '
                           'vigente, los principios generales del derecho '
                           'tienen fuerza de ley.']},
                {'titulo': '1.3 LA LEY: CONCEPTO Y CARACTERÍSTICAS',
                 'items': ['La Ley es toda norma jurídica emanada del {poder '
                           'público}, destinada a regular la conducta '
                           'externa de los miembros de la comunidad.',
                           'Es {obligatoria}: debe ser cumplida por todos, '
                           'incluso en contra de la voluntad del individuo; '
                           'su desconocimiento no excusa su incumplimiento.',
                           'Es {impersonal}: se aplica a un grupo '
                           'indeterminado de sujetos, no a una sola persona.',
                           'Es {abstracta}: se aplica a un número de casos '
                           'no particularizados.',
                           'Es {permanente}: tiene carácter indefinido hasta '
                           'que sea subrogada, abrogada o derogada.',
                           'Es {irretroactiva}: regula hechos posteriores a '
                           'su sanción, no rige sobre conductas anteriores.',
                           'Es {coercitiva}: su incumplimiento implica la '
                           'imposición de una pena o castigo.']},
                {'titulo': '1.4 LA MORAL Y SUS RELACIONES CON EL DERECHO',
                 'items': ['La Moral es la forma de conducta que la '
                           'convivencia fija entre los hombres; concierne al '
                           '{fuero interno} y busca el {bien}.',
                           'Etimológicamente, Moral proviene del latín '
                           '«{mores}» (costumbre); Ética proviene del griego '
                           '«{ethos}» (costumbre).',
                           'La Ética es la disciplina que trata la moral, y '
                           'la Moral es la {práctica} de la ética.']}],
  'cuadros': [{'titulo': '1.4.1 DIFERENCIAS ENTRE DERECHO Y MORAL',
               'encabezados': ['Criterio', 'Moral', 'Derecho'],
               'filas': [['Por su ámbito',
                          '{Interior} (fuero de la conciencia)',
                          '{Exterior} (conducta externa del individuo)'],
                         ['Por sus efectos',
                          '{Unilateral} (solo deberes, sin derecho '
                          'correlativo)',
                          '{Bilateral} (concede facultades y señala '
                          'deberes)'],
                         ['Por su origen',
                          '{Autónoma} (surge por decisión personal, es '
                          'renunciable)',
                          '{Heterónoma} (emana de un poder extraño, de '
                          'cumplimiento ineludible)'],
                         ['Por su fuerza',
                          '{Incoercible} (no existe fuerza que obligue su '
                          'cumplimiento)',
                          '{Coercible} (existe un poder coercitivo que exige '
                          'su cumplimiento)'],
                         ['Por su campo de acción',
                          '{Amplia} (deberes con los demás, consigo mismo y '
                          'con Dios)',
                          '{Precisa} (reglas extremadamente detalladas)']]}],
  'preguntas': [{'pregunta': 'La palabra «Derecho» proviene de la voz '
                             'latina:',
                 'alternativas': ['Lex', 'Ius', 'Directum', 'Ethos', 'Mores'],
                 'correcta': 'B'},
                {'pregunta': 'El vocablo latino «Directum», aplicado tras el '
                             'Corpus Iuris Civilis, significa:',
                 'alternativas': ['Recto, conforme a la norma',
                                  'Autoridad',
                                  'Justicia',
                                  'Sanción',
                                  'Costumbre'],
                 'correcta': 'A'},
                {'pregunta': 'Para Mario Alzamora Valdez, el Derecho es la '
                             'regulación de la vida social del hombre para '
                             'alcanzar:',
                 'alternativas': ['El orden',
                                  'La igualdad',
                                  'La libertad',
                                  'La justicia',
                                  'La paz social'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de normas jurídicas que forman el '
                             'ordenamiento vigente (Constitución, leyes, '
                             'códigos) corresponde al Derecho:',
                 'alternativas': ['Positivo',
                                  'Consuetudinario',
                                  'Objetivo',
                                  'Subjetivo',
                                  'Natural'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho a la vida, a la libertad o a la '
                             'propiedad son ejemplos del Derecho:',
                 'alternativas': ['Objetivo',
                                  'Subjetivo',
                                  'Público',
                                  'Consuetudinario',
                                  'Comparado'],
                 'correcta': 'B'},
                {'pregunta': 'En el derecho subjetivo, la persona sobre la '
                             'cual recae un deber correlativo es el:',
                 'alternativas': ['Objeto del derecho',
                                  'Sujeto activo',
                                  'Legislador',
                                  'Sujeto pasivo',
                                  'Titular del derecho'],
                 'correcta': 'D'},
                {'pregunta': 'Las fuentes que hacen referencia a los '
                             'orígenes mediatos de la norma jurídica '
                             '(factores sociales, económicos y culturales) '
                             'se denominan:',
                 'alternativas': ['Doctrinarias',
                                  'Jurisprudenciales',
                                  'Formales',
                                  'Materiales o reales',
                                  'Consuetudinarias'],
                 'correcta': 'D'},
                {'pregunta': 'La forma de conducta implantada por una '
                             'colectividad, repetida de manera uniforme y '
                             'permanente, cuya observancia se hace '
                             'obligatoria, es:',
                 'alternativas': ['La ley',
                                  'La costumbre',
                                  'La equidad',
                                  'La doctrina',
                                  'La jurisprudencia'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de resoluciones emitidas por la '
                             'Corte Suprema y el Tribunal Constitucional '
                             'sobre una cuestión determinada constituye:',
                 'alternativas': ['La doctrina',
                                  'Los principios generales',
                                  'La costumbre',
                                  'La ley',
                                  'La jurisprudencia'],
                 'correcta': 'E'},
                {'pregunta': 'Los estudios especializados del derecho, que '
                             'dan lugar a escuelas y teorías jurídicas pero '
                             'carecen de fuerza legal obligatoria, '
                             'constituyen:',
                 'alternativas': ['La ley',
                                  'La costumbre',
                                  'La doctrina',
                                  'La casuística',
                                  'La jurisprudencia'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 139 de la Constitución '
                             'vigente, los principios generales del derecho '
                             'tienen:',
                 'alternativas': ['Carácter consuetudinario',
                                  'Valor supletorio únicamente',
                                  'Aplicación exclusiva penal',
                                  'Fuerza de ley',
                                  'Solo valor referencial'],
                 'correcta': 'D'},
                {'pregunta': 'Que una ley deba ser cumplida por todos los '
                             'que están en el territorio donde rige, incluso '
                             'en contra de su voluntad, corresponde a su '
                             'carácter:',
                 'alternativas': ['Obligatorio',
                                  'Coercitivo',
                                  'Impersonal',
                                  'Permanente',
                                  'Abstracto'],
                 'correcta': 'A'},
                {'pregunta': 'Que la ley se aplique a un grupo indeterminado '
                             'de sujetos y no a una sola persona corresponde '
                             'a su carácter:',
                 'alternativas': ['Impersonal',
                                  'Permanente',
                                  'General',
                                  'Irretroactivo',
                                  'Coercitivo'],
                 'correcta': 'A'},
                {'pregunta': 'Que una ley regule hechos posteriores a su '
                             'sanción y no rija sobre conductas anteriores '
                             'corresponde a su carácter:',
                 'alternativas': ['Impersonal',
                                  'Abstracto',
                                  'Coercitivo',
                                  'Permanente',
                                  'Irretroactivo'],
                 'correcta': 'E'},
                {'pregunta': 'Que el incumplimiento de la ley implique la '
                             'imposición de una pena o castigo corresponde a '
                             'su carácter:',
                 'alternativas': ['Coercitivo',
                                  'Abstracto',
                                  'Permanente',
                                  'General',
                                  'Impersonal'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, la palabra «Moral» proviene '
                             'del latín «mores», que significa:',
                 'alternativas': ['Ley',
                                  'Costumbre',
                                  'Virtud',
                                  'Deber',
                                  'Justicia'],
                 'correcta': 'B'},
                {'pregunta': 'Respecto de su ámbito, la Moral es interior y '
                             'el Derecho es:',
                 'alternativas': ['Autónomo',
                                  'Bilateral',
                                  'Exterior',
                                  'Heterónomo',
                                  'Coercible'],
                 'correcta': 'C'},
                {'pregunta': 'Que la Moral solo imponga deberes cuyo '
                             'cumplimiento no genera ningún derecho, a '
                             'diferencia del Derecho que concede facultades '
                             'y señala deberes, corresponde a la diferencia '
                             'por su(s):',
                 'alternativas': ['Efectos',
                                  'Campo de acción',
                                  'Origen',
                                  'Ámbito',
                                  'Fuerza'],
                 'correcta': 'A'},
                {'pregunta': 'Que la Moral surja espontáneamente por '
                             'decisión personal y sea renunciable, mientras '
                             'que el Derecho emane de un poder extraño de '
                             'cumplimiento ineludible, corresponde a la '
                             'diferencia por su:',
                 'alternativas': ['Origen',
                                  'Fuerza',
                                  'Efecto',
                                  'Campo de acción',
                                  'Ámbito'],
                 'correcta': 'A'},
                {'pregunta': 'Que la Moral sea incoercible (sin fuerza que '
                             'obligue su cumplimiento) y el Derecho sea '
                             'coercible (con poder coercitivo que exige su '
                             'cumplimiento) corresponde a la diferencia por '
                             'su:',
                 'alternativas': ['Origen',
                                  'Efecto',
                                  'Ámbito',
                                  'Campo de acción',
                                  'Fuerza'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto de normas de conducta humana para '
                             'organizar y regularizar la vida social del '
                             'hombre se llama: (I CEPRU 2025-I)',
                 'alternativas': ['La ley',
                                  'El derecho',
                                  'La moral',
                                  'Los valores',
                                  'Las virtudes'],
                 'correcta': 'B'},
                {'pregunta': 'La ley que es de carácter indefinido y '
                             'permanente, y solo deja de tener vigencia '
                             'cuando es reemplazada por otra ley del mismo '
                             'rango, se caracteriza por ser: (I CEPRU '
                             '2024-II)',
                 'alternativas': ['Permanente',
                                  'Irretroactiva',
                                  'General',
                                  'Obligatoria',
                                  'Coercible'],
                 'correcta': 'A'},
                {'pregunta': 'El no conocimiento de la ley no es excusa para '
                             'su no cumplimiento; es una característica de '
                             'la ley: (I CEPRU 2023-II)',
                 'alternativas': ['Universal',
                                  'Jerárquica',
                                  'Flexible',
                                  'De polaridad',
                                  'Obligatoria'],
                 'correcta': 'E'},
                {'pregunta': 'Una característica de la ley es que es: (I '
                             'CEPRU 2023-I)',
                 'alternativas': ['Voluntaria',
                                  'Incoercible',
                                  'Retroactiva',
                                  'Impersonal',
                                  'Efímera'],
                 'correcta': 'D'},
                {'pregunta': 'Una característica de la ley es que es: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Individual',
                                  'Concreta',
                                  'Coercitiva',
                                  'Retroactiva',
                                  'Voluntaria'],
                 'correcta': 'C'},
                {'pregunta': 'La Ley es toda norma jurídica emanada del '
                             'poder público, destinada a regular la '
                             'conducta: (II CEPRU 2016-II)',
                 'alternativas': ['Interna de las personas fuera de la '
                                  'sociedad',
                                  'Externa de las personas dentro de la '
                                  'familia',
                                  'Interna de las personas dentro de la '
                                  'ciudad',
                                  'Externa de las personas dentro de la '
                                  'sociedad',
                                  'Externa de las personas fuera de la '
                                  'familia'],
                 'correcta': 'D'},
                {'pregunta': 'A la práctica general, uniforme y '
                             'constantemente repetida de una determinada '
                             'conducta por los miembros de una comunidad se '
                             'le denomina: (II CEPRU 2016-II)',
                 'alternativas': ['Historia',
                                  'Hábito',
                                  'Costumbre',
                                  'Idiosincrasia',
                                  'Arte'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'EL DERECHO: CONCEPTO Y CLASES',
                      'items': ['La palabra Derecho viene del latín «IUS», '
                                'término con el que los romanos lo '
                                'designaban.',
                                'Con el Corpus Iuris Civilis se aplicó la '
                                'palabra «Directum», que significa «recto», '
                                '«lo que está conforme a la regla».',
                                'Para Mario Alzamora Valdez, el Derecho es '
                                'la regulación de la vida social del hombre '
                                'para alcanzar la justicia.',
                                'Para Claude Du Pasquier, el Derecho es la '
                                'ordenación social e imperativa de la vida '
                                'humana orientada a la realización de '
                                'justicia.',
                                'El Derecho Objetivo es el conjunto de '
                                'normas jurídicas que regulan la conducta de '
                                'una persona en relación a otra '
                                '(Constitución, leyes, códigos).',
                                'El Derecho Subjetivo es el conjunto de '
                                'prerrogativas, facultades y potestades que '
                                'tiene una persona, como el derecho a la '
                                'vida, a la libertad o a la propiedad.',
                                'Elementos del derecho subjetivo: el sujeto '
                                'activo (titular del derecho), el sujeto '
                                'pasivo (sobre quien recae el deber) y el '
                                'objeto del derecho.']},
                     {'titulo': 'FUENTES DEL DERECHO',
                      'items': ['Las fuentes del Derecho son los '
                                'procedimientos por los que se produce '
                                'válidamente normas jurídicas con carácter '
                                'obligatorio.',
                                'Las fuentes materiales o reales hacen '
                                'referencia a los orígenes mediatos de la '
                                'norma (factores sociales, económicos, '
                                'culturales).',
                                'Las fuentes formales son el origen '
                                'inmediato de las normas jurídicas: la ley, '
                                'la costumbre, la jurisprudencia, la '
                                'doctrina y los principios generales del '
                                'derecho.',
                                'La costumbre es una forma de conducta '
                                'implantada por una colectividad, repetida '
                                'de forma uniforme y permanente, cuya '
                                'observancia se hace obligatoria.',
                                'La jurisprudencia es el conjunto de '
                                'resoluciones judiciales de la Corte Suprema '
                                'y del Tribunal Constitucional sobre una '
                                'cuestión determinada.',
                                'La doctrina son los estudios especializados '
                                'del derecho; carece de fuerza legal '
                                'obligatoria.',
                                'Según el artículo 139 de la Constitución '
                                'vigente, los principios generales del '
                                'derecho tienen fuerza de ley.']},
                     {'titulo': 'LA LEY: CONCEPTO Y CARACTERÍSTICAS',
                      'items': ['La Ley es toda norma jurídica emanada del '
                                'poder público, destinada a regular la '
                                'conducta externa de los miembros de la '
                                'comunidad.',
                                'Es obligatoria: debe ser cumplida por '
                                'todos, incluso en contra de la voluntad del '
                                'individuo; su desconocimiento no excusa su '
                                'incumplimiento.',
                                'Es impersonal: se aplica a un grupo '
                                'indeterminado de sujetos, no a una sola '
                                'persona.',
                                'Es abstracta: se aplica a un número de '
                                'casos no particularizados.',
                                'Es permanente: tiene carácter indefinido '
                                'hasta que sea subrogada, abrogada o '
                                'derogada.',
                                'Es irretroactiva: regula hechos posteriores '
                                'a su sanción, no rige sobre conductas '
                                'anteriores.',
                                'Es coercitiva: su incumplimiento implica la '
                                'imposición de una pena o castigo.']},
                     {'titulo': 'LA MORAL Y SUS RELACIONES CON EL DERECHO',
                      'items': ['La Moral es la forma de conducta que la '
                                'convivencia fija entre los hombres; '
                                'concierne al fuero interno y busca el bien.',
                                'Etimológicamente, Moral proviene del latín '
                                '«mores» (costumbre); Ética proviene del '
                                'griego «ethos» (costumbre).',
                                'La Ética es la disciplina que trata la '
                                'moral, y la Moral es la práctica de la '
                                'ética.']}],
  'qr_reto': [{'pregunta': 'A la práctica general, uniforme y constantemente '
                           'repetida de una determinada conducta por los '
                           'miembros de una comunidad se le denomina:',
               'respuesta': 'Costumbre'},
              {'pregunta': 'La Ley es toda norma jurídica emanada del poder '
                           'público, destinada a regular la conducta:',
               'respuesta': 'Externa de las personas dentro de la sociedad'},
              {'pregunta': 'Los estudios especializados del derecho, que dan '
                           'lugar a escuelas y teorías jurídicas pero '
                           'carecen de fuerza legal obligatoria, '
                           'constituyen:',
               'respuesta': 'La doctrina'}],
  'qr_dato': 'Según el artículo 139 de la Constitución vigente, los '
             'principios generales del derecho tienen fuerza de ley.'},
 {'num': 2,
  'titulo': 'Valores Cívicos Sociales',
  'secciones': [{'titulo': '2.1 CONCEPTO DE VALOR',
                 'items': ['Los valores son las {vivencias} e ideales que '
                           'orientan nuestros actos en beneficio propio y de '
                           'la {colectividad}, llevándonos a la superación '
                           'personal.',
                           'El estudio de los valores corresponde a la '
                           '{Axiología}, una rama de la {Filosofía}.',
                           'Aplicadamente, otras ciencias también se ocupan '
                           'de los valores, como la Sociología, la Economía '
                           'y la {Política}.']},
                {'titulo': '2.2 LA DIGNIDAD Y LA JUSTICIA',
                 'items': ['La dignidad hace referencia al valor {inherente} '
                           'del ser humano por el simple hecho de serlo, en '
                           'cuanto ser racional dotado de {libertad}.',
                           'La dignidad no depende de ningún '
                           'condicionamiento de raza, sexo o condición '
                           '{social}.',
                           'Etimológicamente, justicia proviene de la voz '
                           'latina {iustitia}, que significa dar a cada cual '
                           'lo que le corresponde.',
                           'La justicia {general} busca el bien de la '
                           'sociedad entera; la justicia {particular} '
                           'armoniza los intereses individuales.',
                           'La justicia {distributiva} considera que el '
                           'individuo se enfrenta no a otros individuos, '
                           'sino al todo social.',
                           'La justicia {conmutativa} es la forma clásica de '
                           'justicia, aplicada en la relación mutua entre '
                           'individuos como pares independientes.']},
                {'titulo': '2.3 LA SOLIDARIDAD Y LA HONESTIDAD',
                 'items': ['Solidaridad proviene del latín {solidus}, que '
                           'significa sólido, firme, compacto.',
                           'La solidaridad se practica sin distinción de '
                           'credo, sexo, raza, nacionalidad o afiliación '
                           '{política}.',
                           'Honestidad proviene del latín {honestitad} y '
                           'significa cualidad de decente, decoroso y '
                           '{razonable}.',
                           'La honestidad es el respeto a la {verdad} en '
                           'relación con el mundo, los hechos y las '
                           'personas.']},
                {'titulo': '2.4 EL RESPETO, LA LIBERTAD Y LA IGUALDAD',
                 'items': ['El respeto es el reconocimiento del {valor} '
                           'propio y de los derechos de los individuos y de '
                           'la sociedad.',
                           'La libertad es la capacidad de la persona de '
                           '{autodeterminarse} y actuar según su propia '
                           'voluntad.',
                           'La igualdad implica que todas las personas '
                           'tienen los mismos {derechos} y oportunidades '
                           'ante la ley.']},
                {'titulo': '2.5 PROFUNDIZANDO LIBERTAD E IGUALDAD',
                 'items': ['Etimológicamente, «respeto» proviene del latín '
                           '{respectus} y significa atención o '
                           'consideración.',
                           'Etimológicamente, «libertad» deriva del latín '
                           '{libertas}, libertatis.',
                           'La libertad implica actuar de acuerdo a la '
                           '{conciencia} propia, sin sujeción a coacción '
                           'interior o exterior.',
                           'La libertad está limitada por la {ley}, la moral '
                           'y las buenas costumbres.',
                           'El filósofo francés Jean Jacques {Rousseau} '
                           'afirmó: «El hombre nace libre, pero en todas '
                           'partes está encadenado».',
                           'Cuando la libertad se ejerce sin responsabilidad '
                           'por los propios actos, se habla de '
                           '{libertinaje}.',
                           'La igualdad es una equivalencia o conformidad en '
                           'la calidad, cantidad o {forma} de dos o más '
                           'elementos.',
                           'La igualdad se asocia con otras palabras como la '
                           '{justicia} y la solidaridad.']}],
  'cuadros': [{'titulo': '2.2 CLASES DE JUSTICIA',
               'encabezados': ['Clase', 'Definición'],
               'filas': [['{General}',
                          'Busca el bien de la {sociedad} entera'],
                         ['{Particular}',
                          'Armoniza los intereses {individuales}'],
                         ['{Judicial}',
                          'El juez emite {sentencia} sobre un caso'],
                         ['{Distributiva}',
                          'Considera al individuo frente al {todo} social'],
                         ['{Conmutativa}',
                          'Relación mutua entre individuos '
                          '{independientes}']]}],
  'preguntas': [{'pregunta': 'El estudio de los valores corresponde a la '
                             'rama filosófica llamada:',
                 'alternativas': ['Ontología',
                                  'Axiología',
                                  'Lógica',
                                  'Estética',
                                  'Gnoseología'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «justicia» proviene de la '
                             'voz latina:',
                 'alternativas': ['Honestitad',
                                  'Dignitas',
                                  'Iustitia',
                                  'Solidus',
                                  'Veritas'],
                 'correcta': 'C'},
                {'pregunta': 'La justicia que busca el bien de la sociedad '
                             'entera se llama:',
                 'alternativas': ['Judicial',
                                  'General',
                                  'Distributiva',
                                  'Particular',
                                  'Conmutativa'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia aplicada por un juez al emitir '
                             'sentencia se denomina:',
                 'alternativas': ['Judicial',
                                  'General',
                                  'Particular',
                                  'Conmutativa',
                                  'Social'],
                 'correcta': 'A'},
                {'pregunta': 'La forma clásica de justicia, entre individuos '
                             'como pares independientes, es la:',
                 'alternativas': ['Conmutativa',
                                  'Distributiva',
                                  'General',
                                  'Particular',
                                  'Social'],
                 'correcta': 'A'},
                {'pregunta': 'La justicia que considera al individuo frente '
                             'al todo social es la:',
                 'alternativas': ['Particular',
                                  'Conmutativa',
                                  'General',
                                  'Judicial',
                                  'Distributiva'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra «solidaridad» proviene del latín '
                             '«solidus», que significa:',
                 'alternativas': ['Sólido, firme, compacto',
                                  'Colaboración',
                                  'Unión',
                                  'Ayuda',
                                  'Fraternidad'],
                 'correcta': 'A'},
                {'pregunta': 'La honestidad se define principalmente como el '
                             'respeto a:',
                 'alternativas': ['La ley',
                                  'La religión',
                                  'La verdad',
                                  'La costumbre',
                                  'La autoridad'],
                 'correcta': 'C'},
                {'pregunta': 'La dignidad humana depende de:',
                 'alternativas': ['Ningún condicionamiento externo, es '
                                  'inherente al ser humano',
                                  'La nacionalidad',
                                  'El nivel educativo',
                                  'La condición social',
                                  'La raza y el sexo'],
                 'correcta': 'A'},
                {'pregunta': 'La libertad se define como la capacidad de la '
                             'persona de:',
                 'alternativas': ['Depender de otros',
                                  'Autodeterminarse y actuar según su '
                                  'voluntad',
                                  'Obedecer las normas',
                                  'Evitar responsabilidades',
                                  'Seguir la mayoría'],
                 'correcta': 'B'},
                {'pregunta': 'La solidaridad se practica sin distinción de:',
                 'alternativas': ['Solo religión',
                                  'Credo, sexo, raza o afiliación política',
                                  'Solo nacionalidad',
                                  'Solo género',
                                  'Solo edad'],
                 'correcta': 'B'},
                {'pregunta': 'Los valores representan, en síntesis:',
                 'alternativas': ['Normas legales obligatorias',
                                  'Reglas religiosas',
                                  'Tradiciones familiares',
                                  'Costumbres regionales',
                                  'Lo mejor que la vida humana puede '
                                  'ofrecer'],
                 'correcta': 'E'},
                {'pregunta': 'Adicionalmente a la Filosofía, estudian los '
                             'valores de forma aplicada:',
                 'alternativas': ['La Sociología, la Economía y la Política',
                                  'Solo la Medicina',
                                  'Solo la Biología',
                                  'La Astronomía',
                                  'La Física'],
                 'correcta': 'A'},
                {'pregunta': 'La igualdad implica que todas las personas '
                             'tienen ante la ley:',
                 'alternativas': ['Privilegios especiales',
                                  'Ninguna garantía',
                                  'Los mismos derechos y oportunidades',
                                  'Derechos según su edad',
                                  'Distintos derechos según su riqueza'],
                 'correcta': 'C'},
                {'pregunta': 'El respeto se define como el reconocimiento '
                             'de:',
                 'alternativas': ['Los símbolos patrios',
                                  'Solo la autoridad estatal',
                                  'El valor propio y los derechos de los '
                                  'demás',
                                  'Las tradiciones religiosas',
                                  'Las normas de tránsito'],
                 'correcta': 'C'},
                {'pregunta': 'En la antigua Grecia, el concepto de valores '
                             'se trataba:',
                 'alternativas': ['Exclusivamente en la política',
                                  'De forma muy especializada por '
                                  'disciplinas',
                                  'Solo en el ámbito religioso',
                                  'Solo entre filósofos estoicos',
                                  'Como algo general y sin divisiones'],
                 'correcta': 'E'},
                {'pregunta': 'La justicia social comprende:',
                 'alternativas': ['Solo acuerdos económicos',
                                  'Solo normas religiosas',
                                  'El conjunto de decisiones, normas y '
                                  'principios razonables de una organización '
                                  'social',
                                  'Solo decisiones judiciales',
                                  'Únicamente leyes penales'],
                 'correcta': 'C'},
                {'pregunta': 'Tener valores se relaciona directamente con:',
                 'alternativas': ['Respetar a los demás',
                                  'Ganar poder político',
                                  'Buscar fama',
                                  'Acumular riqueza',
                                  'Evitar el trabajo'],
                 'correcta': 'A'},
                {'pregunta': 'La honestidad, en su sentido más evidente, '
                             'implica coherencia entre:',
                 'alternativas': ['El comportamiento, la expresión y la '
                                  'verdad',
                                  'La riqueza y el estatus',
                                  'El poder y la autoridad',
                                  'La edad y la experiencia',
                                  'El pensamiento y la apariencia'],
                 'correcta': 'A'},
                {'pregunta': 'La dignidad, según la distinción de '
                             'Millán-Puelles, puede ser ontológica o:',
                 'alternativas': ['Legal',
                                  'Social',
                                  'Adquirida',
                                  'Religiosa',
                                  'Política'],
                 'correcta': 'C'},
                {'pregunta': 'Es la colaboración mutua entre dos personas: '
                             '(I CEPRU 2025-I)',
                 'alternativas': ['La solidaridad',
                                  'El respeto',
                                  'La dignidad',
                                  'La igualdad',
                                  'La tolerancia'],
                 'correcta': 'A'},
                {'pregunta': 'Las vivencias e ideales que orientan nuestros '
                             'actos en beneficio propio y de la '
                             'colectividad, llevándonos a la superación '
                             'personal, se refieren a: (III CEPRU 2025-I)',
                 'alternativas': ['Moral',
                                  'Derecho',
                                  'Valores',
                                  'Ética',
                                  'Virtud'],
                 'correcta': 'C'},
                {'pregunta': 'Que el hombre pueda determinarse sin sujeción '
                             'a ninguna fuerza o coacción psicológica '
                             'interior o exterior pertenece al valor de: (I '
                             'CEPRU 2023-II)',
                 'alternativas': ['Derecho',
                                  'Moral',
                                  'Solidaridad',
                                  'Respeto',
                                  'Libertad'],
                 'correcta': 'E'},
                {'pregunta': 'El valor que permite apreciar, reconocer y '
                             'valorar a la sociedad es: (I CEPRU 2023-I)',
                 'alternativas': ['Libertad',
                                  'Respeto',
                                  'Solidaridad',
                                  'Justicia',
                                  'Igualdad'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE VALOR',
                      'items': ['Los valores son las vivencias e ideales que '
                                'orientan nuestros actos en beneficio propio '
                                'y de la colectividad, llevándonos a la '
                                'superación personal.',
                                'El estudio de los valores corresponde a la '
                                'Axiología, una rama de la Filosofía.',
                                'Aplicadamente, otras ciencias también se '
                                'ocupan de los valores, como la Sociología, '
                                'la Economía y la Política.']},
                     {'titulo': 'LA DIGNIDAD Y LA JUSTICIA',
                      'items': ['La dignidad hace referencia al valor '
                                'inherente del ser humano por el simple '
                                'hecho de serlo, en cuanto ser racional '
                                'dotado de libertad.',
                                'La dignidad no depende de ningún '
                                'condicionamiento de raza, sexo o condición '
                                'social.',
                                'Etimológicamente, justicia proviene de la '
                                'voz latina iustitia, que significa dar a '
                                'cada cual lo que le corresponde.',
                                'La justicia general busca el bien de la '
                                'sociedad entera; la justicia particular '
                                'armoniza los intereses individuales.',
                                'La justicia distributiva considera que el '
                                'individuo se enfrenta no a otros '
                                'individuos, sino al todo social.',
                                'La justicia conmutativa es la forma clásica '
                                'de justicia, aplicada en la relación mutua '
                                'entre individuos como pares '
                                'independientes.']},
                     {'titulo': 'LA SOLIDARIDAD Y LA HONESTIDAD',
                      'items': ['Solidaridad proviene del latín solidus, que '
                                'significa sólido, firme, compacto.',
                                'La solidaridad se practica sin distinción '
                                'de credo, sexo, raza, nacionalidad o '
                                'afiliación política.',
                                'Honestidad proviene del latín honestitad y '
                                'significa cualidad de decente, decoroso y '
                                'razonable.',
                                'La honestidad es el respeto a la verdad en '
                                'relación con el mundo, los hechos y las '
                                'personas.']},
                     {'titulo': 'EL RESPETO, LA LIBERTAD Y LA IGUALDAD',
                      'items': ['El respeto es el reconocimiento del valor '
                                'propio y de los derechos de los individuos '
                                'y de la sociedad.',
                                'La libertad es la capacidad de la persona '
                                'de autodeterminarse y actuar según su '
                                'propia voluntad.',
                                'La igualdad implica que todas las personas '
                                'tienen los mismos derechos y oportunidades '
                                'ante la ley.']},
                     {'titulo': 'PROFUNDIZANDO LIBERTAD E IGUALDAD',
                      'items': ['Etimológicamente, «respeto» proviene del '
                                'latín respectus y significa atención o '
                                'consideración.',
                                'Etimológicamente, «libertad» deriva del '
                                'latín libertas, libertatis.',
                                'La libertad implica actuar de acuerdo a la '
                                'conciencia propia, sin sujeción a coacción '
                                'interior o exterior.',
                                'La libertad está limitada por la ley, la '
                                'moral y las buenas costumbres.',
                                'El filósofo francés Jean Jacques Rousseau '
                                'afirmó: «El hombre nace libre, pero en '
                                'todas partes está encadenado».',
                                'Cuando la libertad se ejerce sin '
                                'responsabilidad por los propios actos, se '
                                'habla de libertinaje.',
                                'La igualdad es una equivalencia o '
                                'conformidad en la calidad, cantidad o forma '
                                'de dos o más elementos.',
                                'La igualdad se asocia con otras palabras '
                                'como la justicia y la solidaridad.']}],
  'qr_reto': [{'pregunta': 'Tener valores se relaciona directamente con:',
               'respuesta': 'Respetar a los demás'},
              {'pregunta': 'La justicia social comprende:',
               'respuesta': 'El conjunto de decisiones, normas y principios '
                            'razonables de una organización social'},
              {'pregunta': 'La justicia que busca el bien de la sociedad '
                           'entera se llama:',
               'respuesta': 'General'}],
  'qr_dato': 'Los valores son las vivencias e ideales que orientan nuestros '
             'actos en beneficio propio y de la colectividad, llevándonos a '
             'la superación personal.'},
 {'num': 3,
  'titulo': 'Persona y Sociedad',
  'secciones': [{'titulo': '3.1 LA PERSONA: ENFOQUE CONSTITUCIONAL Y LEGAL',
                 'items': ['El «Derecho de las personas» es el conjunto de '
                           'normas jurídicas que regulan el reconocimiento '
                           'de los {derechos fundamentales} de la persona.',
                           'En el Perú, el Derecho de las personas se '
                           'desarrolla en el Libro {I} del Código Civil.',
                           'El Libro I del Código Civil se divide en cuatro '
                           'secciones: personas naturales, personas '
                           '{jurídicas}, asociación/fundación/comité no '
                           'inscritos, y comunidades campesinas y {nativas}.',
                           'Etimológicamente, «persona» proviene del latín, '
                           'y originalmente designaba la {máscara} que '
                           'usaban los actores en el teatro antiguo.',
                           'Según Aníbal Torres Vásquez, la persona natural '
                           'es todo ser humano cuya existencia comienza con '
                           'la {concepción} y termina con la {muerte}.',
                           'Según Carlos Fernández Sessarego, la persona '
                           'humana es una unidad {psicosomática} constituida '
                           'y sustentada en su libertad.']},
                {'titulo': '3.2 LA SOCIEDAD',
                 'items': ['La sociedad es el conjunto de personas que se '
                           'relacionan entre sí y comparten una cultura, '
                           'normas e {instituciones} comunes.',
                           'El ser humano es un ser {social} por naturaleza, '
                           'que se realiza plenamente en convivencia con '
                           'otros.']},
                {'titulo': '3.3 CLASES DE PERSONAS Y TEORÍAS DE '
                           'FALLECIMIENTO CONJUNTO',
                 'items': ['La persona {natural} o física es todo ser humano '
                           'cuya existencia comienza con la concepción y '
                           'termina con la muerte.',
                           'Según Aníbal Torres Vásquez, la persona '
                           '{jurídica} es la agrupación de sujetos '
                           'individuales para el logro de ciertos fines que '
                           'el ordenamiento jurídico reconoce.',
                           'La persona jurídica existe por una {ficción} de '
                           'la ley; es distinta de sus miembros y tiene '
                           'existencia {independiente} de quienes la '
                           'integran.',
                           'La {premoriencia} es una ficción jurídica que '
                           'establece criterios sobre quién murió antes, '
                           'cuando no se puede acreditar con certeza.',
                           'El Perú adopta la teoría de la {conmoriencia}, '
                           'regulada en el artículo {62} del Código Civil.',
                           'Según la conmoriencia, si no se puede probar '
                           'cuál de dos personas murió primero, se las '
                           'reputa muertas al mismo {tiempo}, sin '
                           'transmisión de derechos hereditarios entre '
                           'ellas.',
                           'Si dos personas perecen en un peligro común, se '
                           'presume que la muerte fue {simultánea}, salvo '
                           'prueba de que fue sucesiva.',
                           'La declaración de {muerte presunta} procede '
                           'cuando hay certeza de muerte sin que el cadáver '
                           'se encuentre o se pueda reconocer.',
                           'Entre los efectos de la declaración de muerte '
                           'presunta están: poner fin a la persona humana, '
                           'disolver el {matrimonio} del desaparecido y '
                           'abrir la {sucesión}.']},
                {'titulo': '3.4 EXISTENCIA Y CAPACIDAD DE LA PERSONA',
                 'items': ['La existencia de la persona natural comienza con '
                           'la {concepción} y culmina con la muerte.',
                           'El reconocimiento de existencia se obtiene '
                           'mediante resolución del {Poder Judicial}, a '
                           'instancia del Ministerio Público o partes '
                           'interesadas.',
                           'El reconocimiento de existencia faculta a la '
                           'persona a {reivindicar} sus bienes.',
                           'Las personas jurídicas pueden ser de derecho '
                           '{público} o de derecho privado, según la '
                           'doctrina.']}],
  'cuadros': [{'titulo': '3.1 SECCIONES DEL LIBRO I DEL CÓDIGO CIVIL',
               'encabezados': ['Sección', 'Contenido'],
               'filas': [['Personas {naturales}',
                          'Seres humanos individuales'],
                         ['Personas {jurídicas}',
                          'Entidades con personería legal'],
                         ['Asociación, fundación y {comité} no inscritos',
                          'Organizaciones sin registro formal'],
                         ['Comunidades {campesinas} y nativas',
                          'Colectivos con régimen especial']]}],
  'preguntas': [{'pregunta': 'El Derecho de las personas se encuentra '
                             'desarrollado en el Código Civil peruano en:',
                 'alternativas': ['El Libro III',
                                  'El Libro IV',
                                  'El Libro II',
                                  'El Libro I',
                                  'La Constitución'],
                 'correcta': 'D'},
                {'pregunta': 'Etimológicamente, la palabra «persona» '
                             'originalmente designaba:',
                 'alternativas': ['Un documento legal',
                                  'Un título nobiliario',
                                  'La máscara usada por los actores de '
                                  'teatro',
                                  'Un cargo político',
                                  'Una ceremonia religiosa'],
                 'correcta': 'C'},
                {'pregunta': 'Según Aníbal Torres Vásquez, la existencia de '
                             'la persona natural comienza con:',
                 'alternativas': ['El registro civil',
                                  'El bautizo',
                                  'Los 18 años',
                                  'El nacimiento',
                                  'La concepción'],
                 'correcta': 'E'},
                {'pregunta': 'La existencia de la persona natural termina '
                             'con:',
                 'alternativas': ['El matrimonio',
                                  'La incapacidad',
                                  'Los 100 años',
                                  'La jubilación',
                                  'La muerte'],
                 'correcta': 'E'},
                {'pregunta': 'Según Fernández Sessarego, la persona humana '
                             'es una unidad:',
                 'alternativas': ['Solo social',
                                  'Psicosomática',
                                  'Únicamente legal',
                                  'Solo espiritual',
                                  'Solo física'],
                 'correcta': 'B'},
                {'pregunta': 'El Libro I del Código Civil se divide en '
                             'cuántas secciones:',
                 'alternativas': ['Cinco', 'Tres', 'Cuatro', 'Dos', 'Seis'],
                 'correcta': 'C'},
                {'pregunta': 'Las comunidades campesinas y nativas se '
                             'regulan dentro de:',
                 'alternativas': ['El derecho laboral',
                                  'El derecho penal',
                                  'El Libro I del Código Civil',
                                  'La ley de municipalidades',
                                  'El derecho tributario'],
                 'correcta': 'C'},
                {'pregunta': 'La persona puede definirse también como un '
                             'sujeto:',
                 'alternativas': ['Solo con derechos',
                                  'Consciente y racional, titular de '
                                  'derechos y obligaciones',
                                  'Sin obligaciones',
                                  'Sin capacidad legal',
                                  'Exclusivamente económico'],
                 'correcta': 'B'},
                {'pregunta': 'El ser humano es considerado un ser social '
                             'porque:',
                 'alternativas': ['Vive completamente aislado',
                                  'Prefiere la soledad',
                                  'No necesita normas',
                                  'Se realiza plenamente en convivencia con '
                                  'otros',
                                  'Depende solo de sí mismo'],
                 'correcta': 'D'},
                {'pregunta': 'Las personas jurídicas se diferencian de las '
                             'personas naturales en que:',
                 'alternativas': ['No tienen derechos',
                                  'Son siempre empresas',
                                  'No tienen personería legal',
                                  'Son entidades con personería legal '
                                  'distinta a un individuo',
                                  'Solo existen en el derecho penal'],
                 'correcta': 'D'},
                {'pregunta': 'La sociedad se define como el conjunto de '
                             'personas que comparten:',
                 'alternativas': ['Solo una religión',
                                  'Solo un idioma',
                                  'Solo un territorio',
                                  'Cultura, normas e instituciones comunes',
                                  'Solo una economía'],
                 'correcta': 'D'},
                {'pregunta': 'El «Derecho de las personas» regula el '
                             'reconocimiento de:',
                 'alternativas': ['Solo derechos laborales',
                                  'Solo derechos políticos',
                                  'Los derechos fundamentales de la persona',
                                  'Solo obligaciones tributarias',
                                  'Solo derechos patrimoniales'],
                 'correcta': 'C'},
                {'pregunta': 'En la Edad Media, el término «persona» se usó '
                             'como sinónimo de:',
                 'alternativas': ['Portador de dignidades',
                                  'Esclavo',
                                  'Soldado',
                                  'Campesino',
                                  'Comerciante'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra persona es considerada, según el '
                             'texto, equívoca y:',
                 'alternativas': ['Polisémica',
                                  'Simple',
                                  'Unívoca',
                                  'Restringida',
                                  'Exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Las asociaciones, fundaciones y comités NO '
                             'inscritos se regulan en:',
                 'alternativas': ['La Constitución exclusivamente',
                                  'Ninguna norma',
                                  'El Libro I del Código Civil, tercera '
                                  'sección',
                                  'El derecho penal',
                                  'El derecho internacional'],
                 'correcta': 'C'},
                {'pregunta': 'El estudio antropológico revela que el hombre '
                             'es un ser:',
                 'alternativas': ['Puramente material',
                                  'Abierto al infinito',
                                  'Determinado biológicamente',
                                  'Cerrado y limitado',
                                  'Sin capacidad de trascender'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad psicosomática de la persona implica '
                             'que lo que afecta al cuerpo:',
                 'alternativas': ['Es independiente de la mente',
                                  'No tiene relación con las emociones',
                                  'No afecta a la psique',
                                  'Solo afecta la salud física',
                                  'Repercute también en la psique, y '
                                  'viceversa'],
                 'correcta': 'E'},
                {'pregunta': 'La persona jurídica se distingue por tener:',
                 'alternativas': ['Solo derechos naturales',
                                  'Solo obligaciones morales',
                                  'Personería legal reconocida',
                                  'Capacidad física',
                                  'Existencia biológica'],
                 'correcta': 'C'},
                {'pregunta': 'El concepto de persona se amplió con el tiempo '
                             'para comprender a:',
                 'alternativas': ['Solo a los varones',
                                  'Todo ser humano',
                                  'Solo a los adultos',
                                  'Solo a los ciudadanos',
                                  'Solo a los nobles'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad y la persona se relacionan porque '
                             'el individuo:',
                 'alternativas': ['Existe independientemente de la sociedad',
                                  'No requiere de otros',
                                  'Rechaza las normas colectivas',
                                  'Se desarrolla y realiza en el marco de la '
                                  'vida social',
                                  'Es anterior a toda organización social'],
                 'correcta': 'D'},
                {'pregunta': 'Las personas creadas por ley y con un fin '
                             'social, dentro de la clasificación de persona, '
                             'se refieren a la: (III CEPRU 2025-I)',
                 'alternativas': ['Persona jurídica',
                                  'Persona jurídica de derecho público',
                                  'Persona natural',
                                  'Persona física',
                                  'Persona jurídica de derecho privado'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Código Civil, el inicio de la vida '
                             'humana es desde: (I CEPRU 2023-II)',
                 'alternativas': ['El nacimiento',
                                  '30 días de nacido',
                                  '5 días de nacido',
                                  '2 horas de nacido',
                                  'La concepción'],
                 'correcta': 'E'},
                {'pregunta': 'Desde un enfoque legal, la persona humana es '
                             'sujeto de derecho desde su: (II CEPRU 2022-II)',
                 'alternativas': ['Involución',
                                  'Concepción',
                                  'Anidación',
                                  'Evolución',
                                  'Nacimiento'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'LA PERSONA: ENFOQUE CONSTITUCIONAL Y LEGAL',
                      'items': ['El «Derecho de las personas» es el conjunto '
                                'de normas jurídicas que regulan el '
                                'reconocimiento de los derechos '
                                'fundamentales de la persona.',
                                'En el Perú, el Derecho de las personas se '
                                'desarrolla en el Libro I del Código Civil.',
                                'El Libro I del Código Civil se divide en '
                                'cuatro secciones: personas naturales, '
                                'personas jurídicas, '
                                'asociación/fundación/comité no inscritos, y '
                                'comunidades campesinas y nativas.',
                                'Etimológicamente, «persona» proviene del '
                                'latín, y originalmente designaba la máscara '
                                'que usaban los actores en el teatro '
                                'antiguo.',
                                'Según Aníbal Torres Vásquez, la persona '
                                'natural es todo ser humano cuya existencia '
                                'comienza con la concepción y termina con la '
                                'muerte.',
                                'Según Carlos Fernández Sessarego, la '
                                'persona humana es una unidad psicosomática '
                                'constituida y sustentada en su libertad.']},
                     {'titulo': 'LA SOCIEDAD',
                      'items': ['La sociedad es el conjunto de personas que '
                                'se relacionan entre sí y comparten una '
                                'cultura, normas e instituciones comunes.',
                                'El ser humano es un ser social por '
                                'naturaleza, que se realiza plenamente en '
                                'convivencia con otros.']},
                     {'titulo': 'CLASES DE PERSONAS Y TEORÍAS DE '
                                'FALLECIMIENTO CONJUNTO',
                      'items': ['La persona natural o física es todo ser '
                                'humano cuya existencia comienza con la '
                                'concepción y termina con la muerte.',
                                'Según Aníbal Torres Vásquez, la persona '
                                'jurídica es la agrupación de sujetos '
                                'individuales para el logro de ciertos fines '
                                'que el ordenamiento jurídico reconoce.',
                                'La persona jurídica existe por una ficción '
                                'de la ley; es distinta de sus miembros y '
                                'tiene existencia independiente de quienes '
                                'la integran.',
                                'La premoriencia es una ficción jurídica que '
                                'establece criterios sobre quién murió '
                                'antes, cuando no se puede acreditar con '
                                'certeza.',
                                'El Perú adopta la teoría de la '
                                'conmoriencia, regulada en el artículo 62 '
                                'del Código Civil.',
                                'Según la conmoriencia, si no se puede '
                                'probar cuál de dos personas murió primero, '
                                'se las reputa muertas al mismo tiempo, sin '
                                'transmisión de derechos hereditarios entre '
                                'ellas.',
                                'Si dos personas perecen en un peligro '
                                'común, se presume que la muerte fue '
                                'simultánea, salvo prueba de que fue '
                                'sucesiva.',
                                'La declaración de muerte presunta procede '
                                'cuando hay certeza de muerte sin que el '
                                'cadáver se encuentre o se pueda reconocer.',
                                'Entre los efectos de la declaración de '
                                'muerte presunta están: poner fin a la '
                                'persona humana, disolver el matrimonio del '
                                'desaparecido y abrir la sucesión.']},
                     {'titulo': 'EXISTENCIA Y CAPACIDAD DE LA PERSONA',
                      'items': ['La existencia de la persona natural '
                                'comienza con la concepción y culmina con la '
                                'muerte.',
                                'El reconocimiento de existencia se obtiene '
                                'mediante resolución del Poder Judicial, a '
                                'instancia del Ministerio Público o partes '
                                'interesadas.',
                                'El reconocimiento de existencia faculta a '
                                'la persona a reivindicar sus bienes.',
                                'Las personas jurídicas pueden ser de '
                                'derecho público o de derecho privado, según '
                                'la doctrina.']}],
  'qr_reto': [{'pregunta': 'La unidad psicosomática de la persona implica '
                           'que lo que afecta al cuerpo:',
               'respuesta': 'Repercute también en la psique, y viceversa'},
              {'pregunta': 'Etimológicamente, la palabra «persona» '
                           'originalmente designaba:',
               'respuesta': 'La máscara usada por los actores de teatro'},
              {'pregunta': 'La palabra persona es considerada, según el '
                           'texto, equívoca y:',
               'respuesta': 'Polisémica'}],
  'qr_dato': 'Si dos personas perecen en un peligro común, se presume que la '
             'muerte fue simultánea, salvo prueba de que fue sucesiva.'},
 {'num': 4,
  'titulo': 'Familia',
  'secciones': [{'titulo': '4.1 CONCEPTO Y NATURALEZA',
                 'items': ['Para Rodríguez Iturri, la familia humana es un '
                           'núcleo de origen {natural}; no ha sido creada '
                           'por la ley, sino que es obra de la naturaleza.',
                           'La familia es una institución natural, jurídica '
                           'y {social} que constituye la célula de la '
                           'sociedad.',
                           'Según Aguilar Llanos, las familias peruanas no '
                           'se originan únicamente en el {matrimonio}, sino '
                           'también en las uniones de hecho.',
                           'Según Cussiánovich, la familia es el lugar '
                           'natural de {acogimiento} de un ser humano, '
                           'encargado de garantizar su sobrevivencia física, '
                           'emocional y afectiva.',
                           'El Tribunal Constitucional (Exp. N° '
                           '06572-2006-PA/TC) señala que la familia no solo '
                           'tiene dimensión de procreación, sino que también '
                           'transmite valores {éticos}, cívicos y '
                           'culturales.',
                           'El artículo {4} de la Constitución peruana '
                           'reconoce a la familia como un instituto natural '
                           'y fundamental de la sociedad.',
                           'El artículo {16} de la Declaración Universal de '
                           'los Derechos Humanos reconoce el derecho de '
                           'hombres y mujeres a casarse y fundar una '
                           'familia.']},
                {'titulo': '4.2 PARENTESCO: GRADOS Y LÍNEAS',
                 'items': ['El {tronco} es la persona a quien reconocen como '
                           'ascendiente común las personas de un mismo '
                           'parentesco.',
                           'El {grado} es la distancia que existe entre dos '
                           'parientes.',
                           'La línea {recta} se forma con personas que '
                           'descienden unas de otras (artículo 236 del '
                           'Código Civil).',
                           'La línea {colateral}, también llamada horizontal '
                           'o transversal, une a personas que sin descender '
                           'unas de otras comparten un ascendiente común.',
                           'Para efectos civiles, en la línea colateral solo '
                           'se considera hasta el {cuarto} grado.',
                           'El parentesco {espiritual} se establece con '
                           'motivo de un sacramento como el bautismo, la '
                           'confirmación o el matrimonio, entre padrinos y '
                           'ahijados.',
                           'La adopción, regulada en el artículo {238} del '
                           'Código Civil, otorga al adoptado los mismos '
                           'derechos y obligaciones que un hijo '
                           'matrimonial.']},
                {'titulo': '4.3 INSTITUCIONES DE AMPARO FAMILIAR: LA PATRIA '
                           'POTESTAD',
                 'items': ['Etimológicamente, «patria potestad» proviene de '
                           'raíces romanas: «patria» alude al {pater '
                           'familia} y «potestad» denota dominio o poder.',
                           'La patria potestad es el conjunto de derechos y '
                           'deberes que tienen los {progenitores} para '
                           'cuidar de la persona y bienes de sus hijos '
                           '(artículo 418 del Código Civil).',
                           'La patria potestad se ejerce conjuntamente por '
                           'el {padre} y la madre durante el matrimonio.',
                           'En caso de divorcio, separación de cuerpos o '
                           'invalidación del matrimonio, la patria potestad '
                           'la ejerce el cónyuge a quien se confían los '
                           '{hijos}.',
                           'La patria potestad no alcanza a los ascendientes '
                           'ni parientes colaterales; quien cuida a un menor '
                           'sin ser su progenitor lo hace a título de '
                           '{tutor}.',
                           'La patria potestad tiene finalidad {tuitiva}, es '
                           'decir, está dirigida a la protección y defensa '
                           'de los hijos y su patrimonio.']},
                {'titulo': '4.4 INSTITUCIONES SUPLETORIAS DE AMPARO FAMILIAR',
                 'items': ['La {tutela} protege a los menores de edad que, '
                           'por desaparición o incapacidad de los '
                           'progenitores, no tienen quién ejerza la {patria '
                           'potestad}.',
                           'La {tutela testamentaria} es la que establecen '
                           'los padres antes de morir, designando en su '
                           '{testamento} al tutor.',
                           'La {tutela legítima} dispone, a falta de la '
                           'testamentaria, que sean tutores los {abuelos} u '
                           'otros descendientes.',
                           'La {tutela dativa} es la que establece el '
                           '{consejo de familia} cuando no hay tutela '
                           'testamentaria ni legítima.',
                           'La {tutela estatal} es ejercida por el Estado a '
                           'falta de las demás, para niños huérfanos o '
                           '{abandonados}.',
                           'La {curatela} protege a la persona y bienes del '
                           'mayor de edad {incapacitado}.',
                           'Quien ejerce la curatela se llama {curador}; el '
                           'adulto que la recibe se llama {curado}.',
                           'Los {apoyos} son formas de asistencia libremente '
                           'elegidas por una persona mayor de edad para '
                           'facilitar el ejercicio de sus {derechos}.']}],
  'cuadros': [{'titulo': '4.2 LÍNEAS DE PARENTESCO',
               'encabezados': ['Línea', 'Definición'],
               'filas': [['{Recta}',
                          'Personas que descienden unas de {otras}'],
                         ['{Colateral}',
                          'Comparten un {ascendiente} común, sin descender '
                          'entre sí'],
                         ['{Espiritual}',
                          'Vínculo por sacramento, entre {padrinos} y '
                          'ahijados']]}],
  'preguntas': [{'pregunta': 'Para Rodríguez Iturri, la familia humana es un '
                             'núcleo de origen:',
                 'alternativas': ['Contractual',
                                  'Legal',
                                  'Administrativo',
                                  'Natural',
                                  'Religioso'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución peruana que '
                             'reconoce a la familia como instituto natural y '
                             'fundamental es el:',
                 'alternativas': ['Artículo 16',
                                  'Artículo 4',
                                  'Artículo 2',
                                  'Artículo 20',
                                  'Artículo 10'],
                 'correcta': 'B'},
                {'pregunta': 'Según Aguilar Llanos, las familias peruanas se '
                             'originan:',
                 'alternativas': ['Solo por vínculo religioso',
                                  'Solo en el matrimonio civil',
                                  'Exclusivamente por vínculo consanguíneo',
                                  'También en las uniones de hecho, además '
                                  'del matrimonio',
                                  'Únicamente por adopción'],
                 'correcta': 'D'},
                {'pregunta': 'Según el Tribunal Constitucional, la familia '
                             'se encarga también de transmitir:',
                 'alternativas': ['Solo bienes materiales',
                                  'Solo el apellido',
                                  'Valores éticos, cívicos y culturales',
                                  'Únicamente el idioma',
                                  'Solo tradiciones religiosas'],
                 'correcta': 'C'},
                {'pregunta': 'La persona a quien reconocen como ascendiente '
                             'común varios parientes se llama:',
                 'alternativas': ['Línea',
                                  'Parentesco',
                                  'Tronco',
                                  'Vínculo',
                                  'Grado'],
                 'correcta': 'C'},
                {'pregunta': 'La distancia entre dos parientes se denomina:',
                 'alternativas': ['Grado', 'Línea', 'Rama', 'Tronco', 'Nexo'],
                 'correcta': 'A'},
                {'pregunta': 'La línea que se forma con personas que '
                             'descienden unas de otras es la línea:',
                 'alternativas': ['Recta',
                                  'Transversal',
                                  'Espiritual',
                                  'Colateral',
                                  'Horizontal'],
                 'correcta': 'A'},
                {'pregunta': 'La línea colateral también se conoce como:',
                 'alternativas': ['Descendente',
                                  'Horizontal o transversal',
                                  'Directa',
                                  'Consanguínea pura',
                                  'Ascendente'],
                 'correcta': 'B'},
                {'pregunta': 'Para efectos civiles, en la línea colateral se '
                             'considera hasta el:',
                 'alternativas': ['Segundo grado',
                                  'Quinto grado',
                                  'Tercer grado',
                                  'Sexto grado',
                                  'Cuarto grado'],
                 'correcta': 'E'},
                {'pregunta': 'El parentesco espiritual se establece, por '
                             'ejemplo, con motivo de:',
                 'alternativas': ['Un contrato comercial',
                                  'Un préstamo',
                                  'Un sacramento como el bautismo',
                                  'Una compraventa',
                                  'Un testamento'],
                 'correcta': 'C'},
                {'pregunta': 'La adopción está regulada en el artículo del '
                             'Código Civil número:',
                 'alternativas': ['238', '418', '618', '818', '118'],
                 'correcta': 'A'},
                {'pregunta': 'Mediante la adopción, el adoptado asume los '
                             'derechos y obligaciones de un:',
                 'alternativas': ['Apoderado',
                                  'Hijo matrimonial',
                                  'Padrino',
                                  'Tutor',
                                  'Curador'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «patria potestad» alude al '
                             '«pater familia» y a la:',
                 'alternativas': ['Adopción',
                                  'Curatela',
                                  'Potestad o dominio',
                                  'Herencia',
                                  'Tutela'],
                 'correcta': 'C'},
                {'pregunta': 'La patria potestad está regulada en el '
                             'artículo del Código Civil número:',
                 'alternativas': ['618', '238', '518', '418', '118'],
                 'correcta': 'D'},
                {'pregunta': 'Durante el matrimonio, la patria potestad se '
                             'ejerce:',
                 'alternativas': ['Por los abuelos',
                                  'Solo por el padre',
                                  'Por el Estado',
                                  'Solo por la madre',
                                  'Conjuntamente por el padre y la madre'],
                 'correcta': 'E'},
                {'pregunta': 'En caso de divorcio, la patria potestad la '
                             'ejerce:',
                 'alternativas': ['El Poder Judicial directamente',
                                  'El cónyuge a quien se confían los hijos',
                                  'Siempre el padre',
                                  'Siempre la madre',
                                  'Los abuelos paternos'],
                 'correcta': 'B'},
                {'pregunta': 'Quien cuida a un menor sin ser su progenitor '
                             'actúa a título de:',
                 'alternativas': ['Padre biológico',
                                  'Padrino',
                                  'Tutor',
                                  'Adoptante',
                                  'Curador exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'La finalidad de la patria potestad es de '
                             'carácter:',
                 'alternativas': ['Económico exclusivamente',
                                  'Punitivo',
                                  'Religioso',
                                  'Tuitivo, de protección y defensa',
                                  'Simbólico'],
                 'correcta': 'D'},
                {'pregunta': 'Según Cussiánovich, la familia debe garantizar '
                             'al ser humano recién nacido:',
                 'alternativas': ['Sobrevivencia física, emocional y '
                                  'afectiva',
                                  'Solo un nombre',
                                  'Solo alimentación',
                                  'Solo educación formal',
                                  'Solo protección legal'],
                 'correcta': 'A'},
                {'pregunta': 'La patria potestad NO alcanza a:',
                 'alternativas': ['Los hijos menores',
                                  'Los padres',
                                  'Los cónyuges',
                                  'Los ascendientes ni parientes colaterales',
                                  'Los hijos adoptivos'],
                 'correcta': 'D'},
                {'pregunta': 'La institución que protege a los menores de '
                             'edad que no tienen quién ejerza la patria '
                             'potestad sobre ellos se llama:',
                 'alternativas': ['Tutela',
                                  'Apoyo',
                                  'Curatela',
                                  'Adopción',
                                  'Salvaguardia'],
                 'correcta': 'A'},
                {'pregunta': 'La tutela que los padres establecen antes de '
                             'morir, designando al tutor en su testamento, '
                             'se llama tutela:',
                 'alternativas': ['Testamentaria',
                                  'Dativa',
                                  'Estatal',
                                  'Judicial',
                                  'Legítima'],
                 'correcta': 'A'},
                {'pregunta': 'La tutela que, a falta de la testamentaria, '
                             'recae en los abuelos u otros descendientes se '
                             'llama tutela:',
                 'alternativas': ['Legítima',
                                  'Estatal',
                                  'Testamentaria',
                                  'Dativa',
                                  'Notarial'],
                 'correcta': 'A'},
                {'pregunta': 'La tutela que establece el consejo de familia '
                             'cuando no hay tutela testamentaria ni legítima '
                             'se llama tutela:',
                 'alternativas': ['Legítima',
                                  'Testamentaria',
                                  'Estatal',
                                  'Dativa',
                                  'Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'La tutela ejercida por el Estado para niños '
                             'huérfanos o abandonados se llama tutela:',
                 'alternativas': ['Testamentaria',
                                  'Estatal',
                                  'Legítima',
                                  'Notarial',
                                  'Dativa'],
                 'correcta': 'B'},
                {'pregunta': 'La institución jurídica creada para proteger a '
                             'la persona y bienes del mayor de edad '
                             'incapacitado se llama:',
                 'alternativas': ['Apoyo exclusivo',
                                  'Tutela',
                                  'Adopción',
                                  'Curatela',
                                  'Patria potestad'],
                 'correcta': 'D'},
                {'pregunta': 'La persona que ejerce la curatela se llama:',
                 'alternativas': ['Curado',
                                  'Albacea',
                                  'Curador',
                                  'Tutor',
                                  'Apoderado'],
                 'correcta': 'C'},
                {'pregunta': 'El adulto que recibe la curatela se llama:',
                 'alternativas': ['Apoderado',
                                  'Tutelado exclusivo',
                                  'Curador',
                                  'Curado',
                                  'Menor'],
                 'correcta': 'D'},
                {'pregunta': 'Los apoyos, según el Código Civil, son formas '
                             'de asistencia libremente elegidas por una '
                             'persona mayor de edad para facilitar el '
                             'ejercicio de:',
                 'alternativas': ['Sus derechos',
                                  'Sus obligaciones',
                                  'Sus bienes exclusivamente',
                                  'Sus contratos exclusivamente',
                                  'Sus deudas'],
                 'correcta': 'A'},
                {'pregunta': 'Es la unión entre una mujer y un varón '
                             'reconocida por el Código Civil: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['La convivencia',
                                  'La unión de hecho',
                                  'El matrimonio civil',
                                  'El matrimonio religioso',
                                  'La comunidad'],
                 'correcta': 'C'},
                {'pregunta': 'Respecto a la muerte presunta, es correcto '
                             'afirmar que: (I CEPRU 2025-I)',
                 'alternativas': ['No apertura la sucesión',
                                  'No disuelve el matrimonio del '
                                  'desaparecido',
                                  'Si la persona es mayor de 80 años debe '
                                  'transcurrir 10 años',
                                  'Se declara al transcurrir 7 años de la '
                                  'desaparición',
                                  'Pone fin a la persona humana'],
                 'correcta': 'D'},
                {'pregunta': 'Dentro de los requisitos de fondo para '
                             'contraer matrimonio está: (III CEPRU 2025-I)',
                 'alternativas': ['Certificado médico de no padecer '
                                  'enfermedad crónica',
                                  'Certificado médico',
                                  'Ser mayor de 18 años',
                                  'Edicto matrimonial',
                                  'Certificado domiciliario con residencia '
                                  'actual'],
                 'correcta': 'C'},
                {'pregunta': 'Los parientes del cónyuge constituyen una '
                             'clase de parentesco denominada: (I CEPRU '
                             '2023-I)',
                 'alternativas': ['Afinidad',
                                  'Consanguinidad',
                                  'Adopción',
                                  'Territorio',
                                  'Espiritual'],
                 'correcta': 'A'},
                {'pregunta': 'La persona es sujeto de derecho desde: (I '
                             'CEPRU 2023-I)',
                 'alternativas': ['La concepción',
                                  'La fecundación',
                                  'El nacimiento',
                                  'La muerte',
                                  'El bautizo'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y NATURALEZA',
                      'items': ['Para Rodríguez Iturri, la familia humana es '
                                'un núcleo de origen natural; no ha sido '
                                'creada por la ley, sino que es obra de la '
                                'naturaleza.',
                                'La familia es una institución natural, '
                                'jurídica y social que constituye la célula '
                                'de la sociedad.',
                                'Según Aguilar Llanos, las familias peruanas '
                                'no se originan únicamente en el matrimonio, '
                                'sino también en las uniones de hecho.',
                                'Según Cussiánovich, la familia es el lugar '
                                'natural de acogimiento de un ser humano, '
                                'encargado de garantizar su sobrevivencia '
                                'física, emocional y afectiva.',
                                'El Tribunal Constitucional (Exp. N° '
                                '06572-2006-PA/TC) señala que la familia no '
                                'solo tiene dimensión de procreación, sino '
                                'que también transmite valores éticos, '
                                'cívicos y culturales.',
                                'El artículo 4 de la Constitución peruana '
                                'reconoce a la familia como un instituto '
                                'natural y fundamental de la sociedad.',
                                'El artículo 16 de la Declaración Universal '
                                'de los Derechos Humanos reconoce el derecho '
                                'de hombres y mujeres a casarse y fundar una '
                                'familia.']},
                     {'titulo': 'PARENTESCO: GRADOS Y LÍNEAS',
                      'items': ['El tronco es la persona a quien reconocen '
                                'como ascendiente común las personas de un '
                                'mismo parentesco.',
                                'El grado es la distancia que existe entre '
                                'dos parientes.',
                                'La línea recta se forma con personas que '
                                'descienden unas de otras (artículo 236 del '
                                'Código Civil).',
                                'La línea colateral, también llamada '
                                'horizontal o transversal, une a personas '
                                'que sin descender unas de otras comparten '
                                'un ascendiente común.',
                                'Para efectos civiles, en la línea colateral '
                                'solo se considera hasta el cuarto grado.',
                                'El parentesco espiritual se establece con '
                                'motivo de un sacramento como el bautismo, '
                                'la confirmación o el matrimonio, entre '
                                'padrinos y ahijados.',
                                'La adopción, regulada en el artículo 238 '
                                'del Código Civil, otorga al adoptado los '
                                'mismos derechos y obligaciones que un hijo '
                                'matrimonial.']},
                     {'titulo': 'INSTITUCIONES DE AMPARO FAMILIAR: LA PATRIA '
                                'POTESTAD',
                      'items': ['Etimológicamente, «patria potestad» '
                                'proviene de raíces romanas: «patria» alude '
                                'al pater familia y «potestad» denota '
                                'dominio o poder.',
                                'La patria potestad es el conjunto de '
                                'derechos y deberes que tienen los '
                                'progenitores para cuidar de la persona y '
                                'bienes de sus hijos (artículo 418 del '
                                'Código Civil).',
                                'La patria potestad se ejerce conjuntamente '
                                'por el padre y la madre durante el '
                                'matrimonio.',
                                'En caso de divorcio, separación de cuerpos '
                                'o invalidación del matrimonio, la patria '
                                'potestad la ejerce el cónyuge a quien se '
                                'confían los hijos.',
                                'La patria potestad no alcanza a los '
                                'ascendientes ni parientes colaterales; '
                                'quien cuida a un menor sin ser su '
                                'progenitor lo hace a título de tutor.',
                                'La patria potestad tiene finalidad tuitiva, '
                                'es decir, está dirigida a la protección y '
                                'defensa de los hijos y su patrimonio.']},
                     {'titulo': 'INSTITUCIONES SUPLETORIAS DE AMPARO '
                                'FAMILIAR',
                      'items': ['La tutela protege a los menores de edad '
                                'que, por desaparición o incapacidad de los '
                                'progenitores, no tienen quién ejerza la '
                                'patria potestad.',
                                'La tutela testamentaria es la que '
                                'establecen los padres antes de morir, '
                                'designando en su testamento al tutor.',
                                'La tutela legítima dispone, a falta de la '
                                'testamentaria, que sean tutores los abuelos '
                                'u otros descendientes.',
                                'La tutela dativa es la que establece el '
                                'consejo de familia cuando no hay tutela '
                                'testamentaria ni legítima.',
                                'La tutela estatal es ejercida por el Estado '
                                'a falta de las demás, para niños huérfanos '
                                'o abandonados.',
                                'La curatela protege a la persona y bienes '
                                'del mayor de edad incapacitado.',
                                'Quien ejerce la curatela se llama curador; '
                                'el adulto que la recibe se llama curado.',
                                'Los apoyos son formas de asistencia '
                                'libremente elegidas por una persona mayor '
                                'de edad para facilitar el ejercicio de sus '
                                'derechos.']}],
  'qr_reto': [{'pregunta': 'La persona es sujeto de derecho desde:',
               'respuesta': 'La concepción'},
              {'pregunta': 'Para efectos civiles, en la línea colateral se '
                           'considera hasta el:',
               'respuesta': 'Cuarto grado'},
              {'pregunta': 'El artículo de la Constitución peruana que '
                           'reconoce a la familia como instituto natural y '
                           'fundamental es el:',
               'respuesta': 'Artículo 4'}],
  'qr_dato': 'El parentesco espiritual se establece con motivo de un '
             'sacramento como el bautismo, la confirmación o el matrimonio, '
             'entre padrinos y ahijados.'},
 {'num': 5,
  'titulo': 'Nación',
  'secciones': [{'titulo': '5.1 CONCEPTO Y ELEMENTOS',
                 'items': ['Etimológicamente, «nación» proviene del latín '
                           '{natio}, nationis, que significa nacimiento o '
                           'raza.',
                           'Para Herder y Fichte, la nación son quienes '
                           'comparten elementos como la etnia, el folclore, '
                           'la mitología y la {cultura}, expresión de un '
                           'alma colectiva.',
                           'Anthony D. Smith define la nación como una '
                           'comunidad humana con nombre propio, asociada a '
                           'un {territorio} nacional, con mitos comunes de '
                           'antepasados.',
                           'Los elementos esenciales de la nación son la '
                           '{tradición histórica} y la conciencia nacional.',
                           'Los elementos secundarios de la nación son el '
                           'territorio, la raza, la religión, el {idioma} y '
                           'la unidad política.']},
                {'titulo': '5.2 NACIONALIDAD: ADQUISICIÓN Y RENUNCIA',
                 'items': ['La nacionalidad es una capacidad especial que '
                           'define derechos y obligaciones específicos para '
                           'quienes el orden jurídico considera integrantes '
                           '{permanentes} del Estado.',
                           'El artículo {52} de la Constitución de 1993 '
                           'establece que son peruanos por nacimiento los '
                           'nacidos en el territorio de la República.',
                           'También son peruanos por nacimiento los nacidos '
                           'en el exterior de padre o madre peruanos, '
                           'inscritos en el {registro} correspondiente '
                           'durante su minoría de edad.',
                           'Se adquiere la nacionalidad peruana también por '
                           '{naturalización} o por opción, siempre que se '
                           'tenga residencia en el Perú.',
                           'La Ley N° {26574}, Ley de Nacionalidad, regula '
                           'en su Capítulo IV la doble nacionalidad.',
                           'Según el artículo 9 de la Ley de Nacionalidad, '
                           'los peruanos de nacimiento que adoptan otra '
                           'nacionalidad no pierden la suya, salvo '
                           '{renuncia} expresa.',
                           'Solo los {mayores} de edad pueden renunciar a la '
                           'nacionalidad peruana; los padres no pueden '
                           'hacerlo en nombre de sus hijos menores.',
                           'Para renunciar a la nacionalidad peruana se debe '
                           'suscribir una {escritura pública} de renuncia.']},
                {'titulo': '5.3 IDENTIDAD NACIONAL Y LA PERUANIDAD',
                 'items': ['La identidad nacional es el sentimiento '
                           'subjetivo del individuo de {pertenecer} a una '
                           'nación concreta.',
                           'El término «peruanidad» fue acuñado por el '
                           'historiador {Víctor Andrés Belaunde} García.',
                           'La peruanidad es el sentimiento de identidad y '
                           'unidad profunda que vincula a los pueblos del '
                           'Perú con sus {tradiciones} y la fe en su futuro.',
                           'Entre los aspectos que fundamentan la peruanidad '
                           'figura la etapa de cultura {prehispánica}, que '
                           'incluye Caral y las culturas Chavín, Paracas y '
                           'Nazca.']},
                {'titulo': '5.4 SISTEMA DE DEFENSA NACIONAL',
                 'items': ['El {Sistema de Defensa Nacional} garantiza la '
                           'seguridad integral del Estado; lo preside y '
                           'dirige el {Presidente} de la República.',
                           'Está integrado por el Consejo de Ministros, el '
                           'Ministerio de Defensa, el Sistema de '
                           'Inteligencia Nacional y el Sistema de Defensa '
                           '{Civil}.',
                           'Las {Fuerzas Armadas} (Ejército, Marina de '
                           'Guerra y Fuerza Aérea) garantizan la '
                           'independencia, soberanía e integridad '
                           '{territorial}.',
                           'La {Policía Nacional} tiene como finalidad '
                           'garantizar y restablecer el orden {interno}.',
                           'El Presidente de la República es el {Jefe '
                           'Supremo} de las Fuerzas Armadas y de la Policía '
                           'Nacional.']},
                {'titulo': '5.5 LOS SÍMBOLOS PATRIOS: LA BANDERA',
                 'items': ['La {vexilología} es el estudio de las banderas; '
                           'quien se dedica a ella es el {vexilólogo}.',
                           'El artículo {49} de la Constitución señala que '
                           'los símbolos de la Patria son la bandera, el '
                           'escudo y el himno {nacional}.',
                           'La primera bandera republicana fue creada por '
                           '{José de San Martín} el {21} de octubre de 1820.',
                           'La bandera definitiva fue establecida por el '
                           'Congreso Constituyente, bajo {Simón Bolívar}, el '
                           '{25} de febrero de 1825.',
                           'Según Abraham {Valdelomar}, San Martín se '
                           'inspiró en los colores de las {pariguanas}, '
                           'flamencos de alas rojas y pecho blanco.',
                           'El color {rojo} de la bandera simboliza la '
                           'sangre de los héroes; el color {blanco} '
                           'representa la pureza y la paz.']},
                {'titulo': '5.6 EL ESCUDO Y EL HIMNO NACIONAL',
                 'items': ['El {Escudo Nacional} se estableció el 25 de '
                           'febrero de 1825, mediante ley promulgada por '
                           '{Simón Bolívar}.',
                           'El escudo tiene tres partes: la {vicuña} (reino '
                           'animal), el árbol de la {quina} (reino vegetal), '
                           'y la cornucopia (reino {mineral}).',
                           'La letra del {Himno Nacional} es de José de la '
                           'Torre {Ugarte}, y la música de José Bernardo '
                           '{Alcedo}.',
                           'La Ley del {15} de abril de {1822} reconoció el '
                           'Himno Nacional del Perú, compuesto de seis '
                           '{estrofas}.',
                           'Actualmente solo se cantan la primera y {sexta} '
                           'estrofa del himno, según Resolución Ministerial '
                           'de {2010}.',
                           'La {escarapela}, de color blanco y encarnado, es '
                           'un símbolo patrio {no oficial} pero de uso '
                           'arraigado.']},
                {'titulo': '5.7 PATRIMONIO CULTURAL Y NATURAL',
                 'items': ['Según la Convención de la UNESCO de {1972}, el '
                           'patrimonio cultural se compone de aquello que a '
                           'lo largo de la historia han creado los hombres '
                           'de una nación.',
                           'El patrimonio cultural se clasifica en '
                           'arqueológico, histórico, artístico, '
                           '{bibliográfico} y documental.',
                           'El {Ministerio de Cultura} es el principal '
                           'organismo encargado de la defensa, preservación '
                           'y restauración de los bienes culturales del '
                           'país.',
                           'La {Biblioteca Nacional} del Perú conduce las '
                           'acciones de defensa y conservación del '
                           'patrimonio documental-bibliográfico de la '
                           'Nación.',
                           'El {Archivo General de la Nación} se encarga del '
                           'acopio y protección del patrimonio documental, y '
                           'fue creado en {1861}.',
                           'El patrimonio natural está constituido por los '
                           'animales, plantas y territorios con valor '
                           '{excepcional} desde el punto de vista estético, '
                           'científico o ambiental.',
                           'El artículo {66} de la Constitución establece '
                           'que los recursos naturales, renovables y no '
                           'renovables, son patrimonio de la {nación}.',
                           'El {Ministerio del Ambiente} (MINAM) diseña, '
                           'establece y supervisa la política nacional y '
                           'sectorial ambiental.']}],
  'cuadros': [{'titulo': '5.1 ELEMENTOS DE LA NACIÓN',
               'encabezados': ['Tipo', 'Elementos'],
               'filas': [['{Esenciales}',
                          'Tradición histórica y {conciencia} nacional'],
                         ['{Secundarios}',
                          'Territorio, raza, religión, {idioma}, unidad '
                          'política']]}],
  'preguntas': [{'pregunta': 'Etimológicamente, «nación» proviene del latín '
                             '«natio», que significa:',
                 'alternativas': ['Nacimiento o raza',
                                  'Gobierno',
                                  'Territorio',
                                  'Idioma',
                                  'Cultura'],
                 'correcta': 'A'},
                {'pregunta': 'Para Herder y Fichte, compartir elementos como '
                             'etnia y folclore expresa:',
                 'alternativas': ['Una obligación legal',
                                  'Un alma colectiva',
                                  'Un acuerdo político',
                                  'Una decisión estatal',
                                  'Un contrato social'],
                 'correcta': 'B'},
                {'pregunta': 'Anthony D. Smith asocia a la nación '
                             'principalmente con:',
                 'alternativas': ['Un gobierno central',
                                  'Solo la religión mayoritaria',
                                  'Solo la lengua oficial',
                                  'Solo la moneda nacional',
                                  'Un territorio nacional y mitos comunes de '
                                  'antepasados'],
                 'correcta': 'E'},
                {'pregunta': 'Los elementos esenciales de la nación son la '
                             'tradición histórica y:',
                 'alternativas': ['La religión',
                                  'La raza',
                                  'El territorio',
                                  'La conciencia nacional',
                                  'El idioma'],
                 'correcta': 'D'},
                {'pregunta': 'El territorio, la raza, la religión y el '
                             'idioma son elementos de la nación '
                             'considerados:',
                 'alternativas': ['Legales',
                                  'Esenciales',
                                  'Constitucionales',
                                  'Secundarios',
                                  'Únicos'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'define quiénes son peruanos por nacimiento es '
                             'el:',
                 'alternativas': ['Artículo 52',
                                  'Artículo 200',
                                  'Artículo 4',
                                  'Artículo 100',
                                  'Artículo 2'],
                 'correcta': 'A'},
                {'pregunta': 'Son peruanos por nacimiento los nacidos en el '
                             'exterior de padre o madre peruanos si:',
                 'alternativas': ['Solo si nacen en un país de habla hispana',
                                  'Automáticamente sin ningún trámite',
                                  'Nunca pueden ser peruanos',
                                  'Solo si regresan al Perú antes de los 5 '
                                  'años',
                                  'Son inscritos en el registro '
                                  'correspondiente durante su minoría de '
                                  'edad'],
                 'correcta': 'E'},
                {'pregunta': 'La Ley de Nacionalidad del Perú lleva el '
                             'número:',
                 'alternativas': ['Ley N° 27444',
                                  'Ley N° 26574',
                                  'Ley N° 26300',
                                  'Ley N° 28044',
                                  'Ley N° 30220'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Ley de Nacionalidad, un peruano que '
                             'adopta otra nacionalidad:',
                 'alternativas': ['Debe pagar una multa',
                                  'Pierde sus derechos civiles',
                                  'Debe elegir una sola desde el nacimiento',
                                  'Pierde automáticamente la peruana',
                                  'No pierde la peruana, salvo renuncia '
                                  'expresa'],
                 'correcta': 'E'},
                {'pregunta': 'Para renunciar a la nacionalidad peruana es '
                             'necesario:',
                 'alternativas': ['Ser menor de edad',
                                  'Solo presentar el DNI',
                                  'Ser mayor de edad y suscribir escritura '
                                  'pública',
                                  'Ninguna formalidad especial',
                                  'Pedir autorización de los padres'],
                 'correcta': 'C'},
                {'pregunta': 'Los padres pueden renunciar a la nacionalidad '
                             'peruana en nombre de sus hijos menores:',
                 'alternativas': ['Solo en casos excepcionales',
                                  'Solo con autorización judicial',
                                  'Solo si el hijo lo solicita',
                                  'Sí, siempre',
                                  'No, solo los mayores de edad pueden '
                                  'renunciar'],
                 'correcta': 'E'},
                {'pregunta': 'La identidad nacional se define como:',
                 'alternativas': ['Una condición económica',
                                  'Una obligación legal',
                                  'Un requisito para votar',
                                  'El sentimiento subjetivo de pertenecer a '
                                  'una nación concreta',
                                  'Un documento oficial'],
                 'correcta': 'D'},
                {'pregunta': 'El término «peruanidad» fue acuñado por:',
                 'alternativas': ['Víctor Andrés Belaunde García',
                                  'Manuel González Prada',
                                  'José Carlos Mariátegui',
                                  'Jorge Basadre',
                                  'Raúl Porras Barrenechea'],
                 'correcta': 'A'},
                {'pregunta': 'La peruanidad se define como el sentimiento '
                             'que vincula a los pueblos del Perú con:',
                 'alternativas': ['Solo su territorio físico',
                                  'Solo su gobierno actual',
                                  'Sus tradiciones y la fe en su futuro',
                                  'Solo su idioma oficial',
                                  'Solo su economía'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los aspectos que fundamentan la '
                             'peruanidad figura la etapa de cultura:',
                 'alternativas': ['Solo contemporánea',
                                  'Colonial únicamente',
                                  'Prehispánica',
                                  'Solo republicana',
                                  'Exclusivamente virreinal'],
                 'correcta': 'C'},
                {'pregunta': 'La nacionalidad se adquiere, además del '
                             'nacimiento, por naturalización o:',
                 'alternativas': ['Matrimonio exclusivamente',
                                  'Solo por decisión judicial',
                                  'Solo por herencia',
                                  'Solo por concurso público',
                                  'Opción, con residencia en el Perú'],
                 'correcta': 'E'},
                {'pregunta': 'Las personas con doble nacionalidad ejercen '
                             'los derechos y obligaciones:',
                 'alternativas': ['Ninguno de los dos',
                                  'Solo del Perú',
                                  'Solo del país extranjero',
                                  'De ambos países simultáneamente sin '
                                  'distinción',
                                  'Del país donde domicilian y cuya '
                                  'nacionalidad poseen'],
                 'correcta': 'E'},
                {'pregunta': 'La doble nacionalidad confiere a los '
                             'extranjeros naturalizados:',
                 'alternativas': ['Automática ciudadanía plena',
                                  'Ningún derecho privativo de los peruanos '
                                  'por nacimiento',
                                  'Derechos superiores a los nacionales',
                                  'Los mismos derechos privativos de los '
                                  'peruanos por nacimiento',
                                  'Exoneración total de impuestos'],
                 'correcta': 'B'},
                {'pregunta': 'La nación, para Herder y Fichte, se sustenta '
                             'principalmente en:',
                 'alternativas': ['Solo la Constitución vigente',
                                  'Solo las fronteras políticas',
                                  'Elementos compartidos como etnia, '
                                  'folclore y cultura',
                                  'Solo el sistema económico',
                                  'Un tratado internacional'],
                 'correcta': 'C'},
                {'pregunta': 'El renunciante a la nacionalidad peruana que '
                             'vive en el exterior lo hace ante:',
                 'alternativas': ['Las Naciones Unidas',
                                  'Un notario extranjero únicamente',
                                  'El funcionario consular',
                                  'Un juez peruano en el extranjero',
                                  'La embajada de otro país'],
                 'correcta': 'C'},
                {'pregunta': 'El Sistema de Defensa Nacional es presidido y '
                             'dirigido por:',
                 'alternativas': ['El Ministro de Defensa',
                                  'El Presidente de la República',
                                  'El Congreso',
                                  'El Jefe del Ejército',
                                  'El Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'El Sistema de Defensa Nacional está integrado '
                             'por el Consejo de Ministros, el Ministerio de '
                             'Defensa, el Sistema de Inteligencia Nacional y '
                             'el Sistema de:',
                 'alternativas': ['Salud Pública',
                                  'Aduanas',
                                  'Educación Nacional',
                                  'Justicia Militar',
                                  'Defensa Civil'],
                 'correcta': 'E'},
                {'pregunta': 'Las Fuerzas Armadas peruanas están compuestas '
                             'por el Ejército, la Marina de Guerra y:',
                 'alternativas': ['La Policía Nacional',
                                  'La Marina Mercante',
                                  'El Serenazgo',
                                  'La Fuerza Aérea',
                                  'La Guardia Civil'],
                 'correcta': 'D'},
                {'pregunta': 'La finalidad de la Policía Nacional del Perú '
                             'es garantizar y restablecer:',
                 'alternativas': ['El comercio internacional',
                                  'La soberanía territorial',
                                  'La defensa exterior',
                                  'La independencia nacional',
                                  'El orden interno'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente de la República es el Jefe '
                             'Supremo de las Fuerzas Armadas y de:',
                 'alternativas': ['El Poder Judicial',
                                  'La Policía Nacional',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio de las banderas se llama:',
                 'alternativas': ['Genealogía',
                                  'Vexilología',
                                  'Filatelia',
                                  'Heráldica',
                                  'Numismática'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 49 de la Constitución, los '
                             'símbolos de la Patria son la bandera, el '
                             'escudo y:',
                 'alternativas': ['El águila',
                                  'El himno nacional',
                                  'La escarapela',
                                  'El sol de Mayo',
                                  'La flor de la cantuta'],
                 'correcta': 'B'},
                {'pregunta': 'La primera bandera republicana peruana fue '
                             'creada por:',
                 'alternativas': ['Simón Bolívar',
                                  'Túpac Amaru II',
                                  'Torre Tagle',
                                  'José de la Torre Ugarte',
                                  'José de San Martín'],
                 'correcta': 'E'},
                {'pregunta': 'La bandera definitiva del Perú fue establecida '
                             'el 25 de febrero de 1825 bajo el gobierno de:',
                 'alternativas': ['Torre Tagle',
                                  'Simón Bolívar',
                                  'Andrés A. Cáceres',
                                  'Ramón Castilla',
                                  'José de San Martín'],
                 'correcta': 'B'},
                {'pregunta': 'Según Abraham Valdelomar, San Martín se '
                             'inspiró para los colores de la bandera en:',
                 'alternativas': ['El escudo incaico',
                                  'La bandera chilena',
                                  'La bandera argentina exclusivamente',
                                  'El sol de los Incas',
                                  'Las pariguanas (flamencos)'],
                 'correcta': 'E'},
                {'pregunta': 'El color rojo de la bandera peruana simboliza:',
                 'alternativas': ['El cielo peruano',
                                  'La selva amazónica',
                                  'La sangre de los héroes y mártires',
                                  'La riqueza mineral',
                                  'La pureza y la paz'],
                 'correcta': 'C'},
                {'pregunta': 'El Escudo Nacional se estableció el 25 de '
                             'febrero de 1825 mediante ley promulgada por:',
                 'alternativas': ['Torre Tagle',
                                  'Ramón Castilla',
                                  'El Congreso actual',
                                  'Simón Bolívar',
                                  'José de San Martín'],
                 'correcta': 'D'},
                {'pregunta': 'En el Escudo Nacional, la vicuña representa el '
                             'reino:',
                 'alternativas': ['Acuático',
                                  'Vegetal',
                                  'Aéreo',
                                  'Mineral',
                                  'Animal'],
                 'correcta': 'E'},
                {'pregunta': 'En el Escudo Nacional, el árbol de la quina '
                             'representa el reino:',
                 'alternativas': ['Aéreo',
                                  'Mineral',
                                  'Marino',
                                  'Vegetal',
                                  'Animal'],
                 'correcta': 'D'},
                {'pregunta': 'En el Escudo Nacional, la cornucopia con '
                             'monedas representa el reino:',
                 'alternativas': ['Vegetal',
                                  'Marino',
                                  'Celestial',
                                  'Mineral',
                                  'Animal'],
                 'correcta': 'A'},
                {'pregunta': 'La letra del Himno Nacional del Perú fue '
                             'escrita por:',
                 'alternativas': ['Abraham Valdelomar',
                                  'César Vallejo',
                                  'Ricardo Palma',
                                  'José Bernardo Alcedo',
                                  'José de la Torre Ugarte'],
                 'correcta': 'E'},
                {'pregunta': 'La música del Himno Nacional del Perú fue '
                             'compuesta por:',
                 'alternativas': ['San Martín',
                                  'Torre Tagle',
                                  'Simón Bolívar',
                                  'José de la Torre Ugarte',
                                  'José Bernardo Alcedo'],
                 'correcta': 'E'},
                {'pregunta': 'El Himno Nacional del Perú fue reconocido por '
                             'ley el 15 de abril de:',
                 'alternativas': ['1824', '1820', '1821', '1822', '1825'],
                 'correcta': 'D'},
                {'pregunta': 'El Himno Nacional consta originalmente de seis '
                             'estrofas, pero actualmente solo se cantan la '
                             'primera y:',
                 'alternativas': ['La segunda',
                                  'La sexta',
                                  'La quinta',
                                  'La cuarta',
                                  'La tercera'],
                 'correcta': 'B'},
                {'pregunta': 'La escarapela, de color blanco y encarnado, es '
                             'un símbolo patrio:',
                 'alternativas': ['No oficial pero de uso arraigado',
                                  'Extranjero',
                                  'Oficial exclusivo',
                                  'Prohibido por ley',
                                  'Militar exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Respecto a los elementos esenciales de la '
                             'Nación, es correcto señalar: (III CEPRU '
                             '2025-I)',
                 'alternativas': ['Costumbre',
                                  'Lengua',
                                  'Conciencia nacional',
                                  'Ideales al futuro',
                                  'Tradiciones'],
                 'correcta': 'C'},
                {'pregunta': '¿Quién escribió el libro «7 Ensayos de '
                             'Interpretación de la Realidad Peruana»? (IV '
                             'CEPRU 2023-II)',
                 'alternativas': ['Víctor Andrés Belaunde',
                                  'Julio César Tello',
                                  'Luis Guillermo Lumbreras',
                                  'John Rowe',
                                  'José Carlos Mariátegui'],
                 'correcta': 'E'},
                {'pregunta': 'El término «Peruanidad» fue acuñado por: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Blasco Núñez de Vela',
                                  'Hipólito Unanue',
                                  'Víctor Andrés Belaúnde García',
                                  'Fernando Belaúnde Terry',
                                  'José de la Serna'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento integrante de nuestra peruanidad '
                             'de larga tradición y posesión histórica es el: '
                             '(II CEPRU 2022-I)',
                 'alternativas': ['Sistema jurídico',
                                  'Sistema político',
                                  'Territorio ancestral',
                                  'Sentido de organización',
                                  'Folclore'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema mercantilista, en los aspectos que '
                             'fundamentan la peruanidad, se implantó en la '
                             'etapa de: (I CEPRU 2016-I)',
                 'alternativas': ['La influencia hispánica',
                                  'La cultura prehispánica',
                                  'El desarrollo de la República',
                                  'El desarrollo económico',
                                  'El desarrollo industrial'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ELEMENTOS',
                      'items': ['Etimológicamente, «nación» proviene del '
                                'latín natio, nationis, que significa '
                                'nacimiento o raza.',
                                'Para Herder y Fichte, la nación son quienes '
                                'comparten elementos como la etnia, el '
                                'folclore, la mitología y la cultura, '
                                'expresión de un alma colectiva.',
                                'Anthony D. Smith define la nación como una '
                                'comunidad humana con nombre propio, '
                                'asociada a un territorio nacional, con '
                                'mitos comunes de antepasados.',
                                'Los elementos esenciales de la nación son '
                                'la tradición histórica y la conciencia '
                                'nacional.',
                                'Los elementos secundarios de la nación son '
                                'el territorio, la raza, la religión, el '
                                'idioma y la unidad política.']},
                     {'titulo': 'NACIONALIDAD: ADQUISICIÓN Y RENUNCIA',
                      'items': ['La nacionalidad es una capacidad especial '
                                'que define derechos y obligaciones '
                                'específicos para quienes el orden jurídico '
                                'considera integrantes permanentes del '
                                'Estado.',
                                'El artículo 52 de la Constitución de 1993 '
                                'establece que son peruanos por nacimiento '
                                'los nacidos en el territorio de la '
                                'República.',
                                'También son peruanos por nacimiento los '
                                'nacidos en el exterior de padre o madre '
                                'peruanos, inscritos en el registro '
                                'correspondiente durante su minoría de edad.',
                                'Se adquiere la nacionalidad peruana también '
                                'por naturalización o por opción, siempre '
                                'que se tenga residencia en el Perú.',
                                'La Ley N° 26574, Ley de Nacionalidad, '
                                'regula en su Capítulo IV la doble '
                                'nacionalidad.',
                                'Según el artículo 9 de la Ley de '
                                'Nacionalidad, los peruanos de nacimiento '
                                'que adoptan otra nacionalidad no pierden la '
                                'suya, salvo renuncia expresa.']},
                     {'titulo': 'IDENTIDAD NACIONAL Y LA PERUANIDAD',
                      'items': ['La identidad nacional es el sentimiento '
                                'subjetivo del individuo de pertenecer a una '
                                'nación concreta.',
                                'El término «peruanidad» fue acuñado por el '
                                'historiador Víctor Andrés Belaunde García.',
                                'La peruanidad es el sentimiento de '
                                'identidad y unidad profunda que vincula a '
                                'los pueblos del Perú con sus tradiciones y '
                                'la fe en su futuro.',
                                'Entre los aspectos que fundamentan la '
                                'peruanidad figura la etapa de cultura '
                                'prehispánica, que incluye Caral y las '
                                'culturas Chavín, Paracas y Nazca.']},
                     {'titulo': 'SISTEMA DE DEFENSA NACIONAL',
                      'items': ['El Sistema de Defensa Nacional garantiza la '
                                'seguridad integral del Estado; lo preside y '
                                'dirige el Presidente de la República.',
                                'Está integrado por el Consejo de Ministros, '
                                'el Ministerio de Defensa, el Sistema de '
                                'Inteligencia Nacional y el Sistema de '
                                'Defensa Civil.',
                                'Las Fuerzas Armadas (Ejército, Marina de '
                                'Guerra y Fuerza Aérea) garantizan la '
                                'independencia, soberanía e integridad '
                                'territorial.',
                                'La Policía Nacional tiene como finalidad '
                                'garantizar y restablecer el orden interno.',
                                'El Presidente de la República es el Jefe '
                                'Supremo de las Fuerzas Armadas y de la '
                                'Policía Nacional.']},
                     {'titulo': 'LOS SÍMBOLOS PATRIOS: LA BANDERA',
                      'items': ['La vexilología es el estudio de las '
                                'banderas; quien se dedica a ella es el '
                                'vexilólogo.',
                                'El artículo 49 de la Constitución señala '
                                'que los símbolos de la Patria son la '
                                'bandera, el escudo y el himno nacional.',
                                'La primera bandera republicana fue creada '
                                'por José de San Martín el 21 de octubre de '
                                '1820.',
                                'La bandera definitiva fue establecida por '
                                'el Congreso Constituyente, bajo Simón '
                                'Bolívar, el 25 de febrero de 1825.',
                                'Según Abraham Valdelomar, San Martín se '
                                'inspiró en los colores de las pariguanas, '
                                'flamencos de alas rojas y pecho blanco.',
                                'El color rojo de la bandera simboliza la '
                                'sangre de los héroes; el color blanco '
                                'representa la pureza y la paz.']},
                     {'titulo': 'EL ESCUDO Y EL HIMNO NACIONAL',
                      'items': ['El Escudo Nacional se estableció el 25 de '
                                'febrero de 1825, mediante ley promulgada '
                                'por Simón Bolívar.',
                                'El escudo tiene tres partes: la vicuña '
                                '(reino animal), el árbol de la quina (reino '
                                'vegetal), y la cornucopia (reino mineral).',
                                'La letra del Himno Nacional es de José de '
                                'la Torre Ugarte, y la música de José '
                                'Bernardo Alcedo.',
                                'La Ley del 15 de abril de 1822 reconoció el '
                                'Himno Nacional del Perú, compuesto de seis '
                                'estrofas.',
                                'Actualmente solo se cantan la primera y '
                                'sexta estrofa del himno, según Resolución '
                                'Ministerial de 2010.',
                                'La escarapela, de color blanco y encarnado, '
                                'es un símbolo patrio no oficial pero de uso '
                                'arraigado.']},
                     {'titulo': 'PATRIMONIO CULTURAL Y NATURAL',
                      'items': ['Según la Convención de la UNESCO de 1972, '
                                'el patrimonio cultural se compone de '
                                'aquello que a lo largo de la historia han '
                                'creado los hombres de una nación.',
                                'El patrimonio cultural se clasifica en '
                                'arqueológico, histórico, artístico, '
                                'bibliográfico y documental.',
                                'El Ministerio de Cultura es el principal '
                                'organismo encargado de la defensa, '
                                'preservación y restauración de los bienes '
                                'culturales del país.',
                                'La Biblioteca Nacional del Perú conduce las '
                                'acciones de defensa y conservación del '
                                'patrimonio documental-bibliográfico de la '
                                'Nación.',
                                'El Archivo General de la Nación se encarga '
                                'del acopio y protección del patrimonio '
                                'documental, y fue creado en 1861.',
                                'El patrimonio natural está constituido por '
                                'los animales, plantas y territorios con '
                                'valor excepcional desde el punto de vista '
                                'estético, científico o ambiental.']}],
  'qr_reto': [{'pregunta': 'El territorio, la raza, la religión y el idioma '
                           'son elementos de la nación considerados:',
               'respuesta': 'Secundarios'},
              {'pregunta': 'El término «peruanidad» fue acuñado por:',
               'respuesta': 'Víctor Andrés Belaunde García'},
              {'pregunta': 'La doble nacionalidad confiere a los extranjeros '
                           'naturalizados:',
               'respuesta': 'Ningún derecho privativo de los peruanos por '
                            'nacimiento'}],
  'qr_dato': 'Los elementos esenciales de la nación son la tradición '
             'histórica y la conciencia nacional.'},
 {'num': 6,
  'titulo': 'El Estado',
  'secciones': [{'titulo': '6.1 CONCEPTO Y ELEMENTOS',
                 'items': ['En sentido amplio, el Estado es la {nación} '
                           'jurídicamente organizada.',
                           'En sentido restringido, el Estado es el conjunto '
                           'de organismos que ejercen el {poder} de una '
                           'nación.',
                           'Los elementos del Estado son: {población}, '
                           'territorio, organización jurídica y {soberanía}.',
                           'El territorio se caracteriza por ser '
                           '{inalienable} e inviolable, según el artículo 54 '
                           'de la Constitución.',
                           'El territorio comprende el suelo, el subsuelo, '
                           'el espacio {aéreo} y el mar territorial.',
                           'La {organización jurídica} es el esquema legal '
                           'del Estado, integrado por la Constitución, leyes '
                           'y decretos.',
                           'La soberanía {interna} es la supremacía sobre '
                           'los demás poderes sociales del territorio; la '
                           'soberanía {externa} permite relacionarse con '
                           'otros Estados como iguales.']},
                {'titulo': '6.2 FORMAS DE ESTADO SEGÚN EL PROCESO HISTÓRICO',
                 'items': ['El Estado {Constitucional} surgió en Inglaterra '
                           'a mediados del siglo {XVII}, para limitar las '
                           'decisiones de los monarcas absolutos.',
                           'El Estado {Liberal} surgió a lo largo del siglo '
                           'XIX, con pilares como el constitucionalismo y la '
                           'propiedad {privada}.',
                           'En la {democracia} liberal o representativa, las '
                           'decisiones no las toma toda la comunidad, sino '
                           'representantes {elegidos}.',
                           'En los Estados de partido {único}, solo una '
                           'organización puede ser la legítima expresión de '
                           'la voluntad general, como en los sistemas '
                           'comunistas.']},
                {'titulo': '6.3 FORMAS DE ESTADO SEGÚN SU ESTRUCTURA',
                 'items': ['El Estado {unitario} reconoce como fuente de '
                           'soberanía una sola nación, con un gobierno, un '
                           'parlamento y un poder judicial {únicos}.',
                           'En el Estado unitario existe un solo {centro} de '
                           'poder para todo el territorio nacional.']},
                {'titulo': '6.4 EL GOBIERNO: CONCEPTO Y FORMAS CLÁSICAS',
                 'items': ['El {Gobierno} es el principal pilar del Estado; '
                           'la autoridad que dirige, controla y administra '
                           'sus {instituciones}.',
                           'El Gobierno consiste en la conducción política '
                           'general o ejercicio del poder {ejecutivo} del '
                           'Estado.',
                           'Según {Aristóteles}, las formas de gobierno se '
                           'dividen en puras e {impuras}.',
                           'Las formas {puras} son monarquía (gobierno de '
                           '{uno}), aristocracia (gobierno de pocos) y '
                           'democracia (gobierno de {muchos}).',
                           'Las formas {impuras} son tiranía (deformación de '
                           'la monarquía), oligarquía (deformación de la '
                           'aristocracia) y {demagogia} (deformación de la '
                           'democracia).',
                           'La {tiranía} ocurre cuando el único gobernante '
                           'abusa del {poder}.',
                           'La {oligarquía} ocurre cuando el grupo '
                           'gobernante atiende sus propios intereses en vez '
                           'del bien {común}.',
                           'La {demagogia} ocurre cuando el gobernante '
                           'halaga al pueblo con regalos para convertirlo en '
                           'una masa {servil}.']},
                {'titulo': '6.5 OTRAS FORMAS DE GOBIERNO',
                 'items': ['El gobierno {de jure}, o de derecho, es el que '
                           'está de acuerdo con la {Constitución}.',
                           'El gobierno {de facto}, o de hecho, no ha sido '
                           'elegido según la Constitución, pero no '
                           'necesariamente usa la {fuerza}.',
                           'El gobierno {usurpador} carece de título por no '
                           'haber sido elegido, y se mantiene en el poder '
                           'mediante la {fuerza}.',
                           'El gobierno {parlamentario} o de gabinete tiene '
                           'un jefe de Estado sin responsabilidad y un '
                           'consejo de ministros responsable ante el '
                           '{parlamento}.',
                           'El gobierno {presidencialista} también tiene '
                           'división de poderes, con el Presidente como jefe '
                           'de {Estado} y de gobierno.']}],
  'cuadros': [{'titulo': '6.1 ELEMENTOS DEL ESTADO',
               'encabezados': ['Elemento', 'Descripción'],
               'filas': [['{Población}',
                          'Habitantes organizados {políticamente}'],
                         ['{Territorio}',
                          'Base geográfica, inalienable e {inviolable}'],
                         ['Organización {jurídica}',
                          'Constitución, leyes y decretos'],
                         ['{Soberanía}', 'Autoridad interna y {externa}']]}],
  'preguntas': [{'pregunta': 'En sentido amplio, el Estado se define como:',
                 'alternativas': ['La nación jurídicamente organizada',
                                  'Una constitución escrita',
                                  'Un gobierno de turno',
                                  'Un territorio delimitado',
                                  'Un conjunto de ciudadanos'],
                 'correcta': 'A'},
                {'pregunta': 'Los elementos del Estado son población, '
                             'territorio, organización jurídica y:',
                 'alternativas': ['Idioma',
                                  'Economía',
                                  'Soberanía',
                                  'Religión',
                                  'Cultura'],
                 'correcta': 'C'},
                {'pregunta': 'El territorio del Estado se caracteriza por '
                             'ser inalienable e:',
                 'alternativas': ['Transferible',
                                  'Ilimitado',
                                  'Inviolable',
                                  'Negociable',
                                  'Divisible'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 54 de la Constitución, el '
                             'territorio comprende el suelo, el subsuelo, el '
                             'espacio aéreo y:',
                 'alternativas': ['Solo el litoral',
                                  'El aire internacional',
                                  'El espacio exterior',
                                  'Las fronteras vecinas',
                                  'El mar territorial'],
                 'correcta': 'E'},
                {'pregunta': 'La organización jurídica de un Estado está '
                             'integrada por:',
                 'alternativas': ['Los tratados internacionales únicamente',
                                  'Solo la Constitución',
                                  'Solo el Poder Judicial',
                                  'La Constitución, leyes y decretos',
                                  'Las costumbres sociales'],
                 'correcta': 'D'},
                {'pregunta': 'La soberanía interna del Estado implica:',
                 'alternativas': ['Relacionarse con otros Estados',
                                  'Ceder autoridad a otros países',
                                  'Supremacía sobre los demás poderes del '
                                  'territorio',
                                  'Depender de organismos internacionales',
                                  'No tener autoridad propia'],
                 'correcta': 'C'},
                {'pregunta': 'La soberanía externa permite al Estado:',
                 'alternativas': ['Actuar sin reconocer a otros Estados',
                                  'Imponerse sobre otros Estados',
                                  'Anexar territorios vecinos',
                                  'Ignorar el derecho internacional',
                                  'Relacionarse con otros Estados soberanos '
                                  'como igual'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado Constitucional surgió en:',
                 'alternativas': ['Estados Unidos',
                                  'España',
                                  'Inglaterra',
                                  'Francia',
                                  'Alemania'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado Constitucional surgió con el '
                             'objetivo de:',
                 'alternativas': ['Crear un imperio',
                                  'Limitar las decisiones de los monarcas '
                                  'absolutos',
                                  'Eliminar toda forma de gobierno',
                                  'Fortalecer al monarca absoluto',
                                  'Unificar territorios'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado Liberal se desarrolló principalmente '
                             'durante el siglo:',
                 'alternativas': ['XV', 'XX', 'XVII', 'XVIII', 'XIX'],
                 'correcta': 'E'},
                {'pregunta': 'Un pilar del Estado Liberal es:',
                 'alternativas': ['La propiedad colectiva obligatoria',
                                  'La monarquía absoluta',
                                  'La propiedad privada y la economía de '
                                  'mercado',
                                  'La censura estatal',
                                  'El partido único'],
                 'correcta': 'C'},
                {'pregunta': 'En la democracia liberal o representativa, las '
                             'decisiones las toman:',
                 'alternativas': ['Un consejo religioso',
                                  'Representantes elegidos',
                                  'Solo el presidente',
                                  'Los militares',
                                  'Todos los ciudadanos directamente'],
                 'correcta': 'B'},
                {'pregunta': 'En los Estados de partido único, se considera '
                             'legítima expresión de la voluntad general:',
                 'alternativas': ['Las ONG',
                                  'Las asambleas populares',
                                  'Los sindicatos',
                                  'Un único partido',
                                  'Cualquier partido político'],
                 'correcta': 'D'},
                {'pregunta': 'El Estado unitario se caracteriza por '
                             'reconocer como fuente de soberanía:',
                 'alternativas': ['Varias naciones',
                                  'Solo las regiones',
                                  'Ninguna nación específica',
                                  'Una sola nación',
                                  'Organismos internacionales'],
                 'correcta': 'D'},
                {'pregunta': 'En un Estado unitario existe:',
                 'alternativas': ['Ningún poder judicial central',
                                  'Un solo gobierno, un parlamento y un '
                                  'poder judicial',
                                  'Múltiples constituciones',
                                  'Solo gobiernos locales',
                                  'Varios gobiernos regionales autónomos'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú, según su estructura política, es un '
                             'Estado:',
                 'alternativas': ['Monárquico',
                                  'Sin forma definida',
                                  'Unitario',
                                  'Federal',
                                  'Confederado'],
                 'correcta': 'C'},
                {'pregunta': 'La población del Estado está constituida por:',
                 'alternativas': ['Los habitantes organizados políticamente',
                                  'Únicamente los nacidos en el país',
                                  'Solo los funcionarios públicos',
                                  'Solo los mayores de edad',
                                  'Solo los ciudadanos con derecho a voto'],
                 'correcta': 'A'},
                {'pregunta': 'El pueblo, dentro de los elementos del Estado, '
                             'se caracteriza por ser:',
                 'alternativas': ['Sin organización',
                                  'Dependiente de otro Estado',
                                  'Subordinado al gobierno extranjero',
                                  'Neutral políticamente',
                                  'Soberano e independiente'],
                 'correcta': 'E'},
                {'pregunta': 'Sin la organización jurídica, el Estado:',
                 'alternativas': ['Sería más eficiente',
                                  'Tendría más soberanía',
                                  'Carecería de forma',
                                  'Se fortalecería',
                                  'Funcionaría igual'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado, en sentido restringido, se refiere '
                             'a:',
                 'alternativas': ['La cultura nacional',
                                  'Solo la población',
                                  'El conjunto de organismos que ejercen el '
                                  'poder',
                                  'El idioma oficial',
                                  'Todo el territorio nacional'],
                 'correcta': 'C'},
                {'pregunta': 'El Gobierno es la autoridad que dirige, '
                             'controla y administra las instituciones de:',
                 'alternativas': ['Las empresas privadas',
                                  'Los partidos políticos',
                                  'La sociedad civil',
                                  'El Estado',
                                  'La familia'],
                 'correcta': 'D'},
                {'pregunta': 'El Gobierno consiste en la conducción política '
                             'general o ejercicio del poder:',
                 'alternativas': ['Judicial',
                                  'Municipal',
                                  'Legislativo',
                                  'Electoral',
                                  'Ejecutivo'],
                 'correcta': 'E'},
                {'pregunta': 'Según Aristóteles, las formas de gobierno se '
                             'dividen en formas puras e:',
                 'alternativas': ['Democráticas exclusivas',
                                  'Ideales',
                                  'Modernas',
                                  'Impuras',
                                  'Antiguas'],
                 'correcta': 'D'},
                {'pregunta': 'Entre las formas puras de gobierno según '
                             'Aristóteles está la monarquía, la aristocracia '
                             'y:',
                 'alternativas': ['La oligarquía',
                                  'La democracia',
                                  'La tiranía',
                                  'La plutocracia',
                                  'La demagogia'],
                 'correcta': 'B'},
                {'pregunta': 'La forma pura de gobierno de uno solo se '
                             'llama:',
                 'alternativas': ['Democracia',
                                  'Oligarquía',
                                  'Aristocracia',
                                  'Monarquía',
                                  'Tiranía'],
                 'correcta': 'D'},
                {'pregunta': 'La deformación de la monarquía, donde el único '
                             'gobernante abusa del poder, se llama:',
                 'alternativas': ['Demagogia',
                                  'Tiranía',
                                  'Oligarquía',
                                  'Plutocracia',
                                  'Aristocracia'],
                 'correcta': 'B'},
                {'pregunta': 'La deformación de la aristocracia, donde el '
                             'grupo gobernante atiende sus propios '
                             'intereses, se llama:',
                 'alternativas': ['Oligarquía',
                                  'Demagogia',
                                  'Democracia',
                                  'Monarquía',
                                  'Tiranía'],
                 'correcta': 'A'},
                {'pregunta': 'La deformación de la democracia, donde el '
                             'gobernante halaga al pueblo con regalos, se '
                             'llama:',
                 'alternativas': ['Plutocracia',
                                  'Tiranía',
                                  'Demagogia',
                                  'Oligarquía',
                                  'Aristocracia'],
                 'correcta': 'C'},
                {'pregunta': 'El gobierno que está de acuerdo con la '
                             'Constitución se llama gobierno:',
                 'alternativas': ['De facto',
                                  'Provisional',
                                  'Usurpador',
                                  'De jure o de derecho',
                                  'Revolucionario'],
                 'correcta': 'D'},
                {'pregunta': 'El gobierno que no ha sido elegido según la '
                             'Constitución, pero no necesariamente usa la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['Constitucional',
                                  'Usurpador',
                                  'De facto',
                                  'Legítimo',
                                  'De jure'],
                 'correcta': 'C'},
                {'pregunta': 'El gobierno que carece de título por no haber '
                             'sido elegido, y se mantiene mediante la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['Parlamentario',
                                  'Usurpador',
                                  'De facto',
                                  'Presidencialista',
                                  'De jure'],
                 'correcta': 'C'},
                {'pregunta': 'El gobierno con un jefe de Estado sin '
                             'responsabilidad y un consejo de ministros '
                             'responsable ante el parlamento se llama '
                             'gobierno:',
                 'alternativas': ['Parlamentario o de gabinete',
                                  'Usurpador',
                                  'De facto',
                                  'Revolucionario',
                                  'Presidencialista'],
                 'correcta': 'A'},
                {'pregunta': '¿Quién preside el Sistema de Defensa Nacional? '
                             '(I CEPRU 2023-I)',
                 'alternativas': ['El Congreso',
                                  'El Premier',
                                  'La Primera Dama',
                                  'El Presidente del Tribunal Constitucional',
                                  'El Presidente de la República'],
                 'correcta': 'E'},
                {'pregunta': 'Las lenguas oficiales adoptadas por la ONU '
                             'son: (IV CEPRU 2022-I)',
                 'alternativas': ['Árabe - chino - inglés - holandés - ruso '
                                  '- francés',
                                  'Árabe - chino - inglés - portugués - ruso '
                                  '- español',
                                  'Chino - árabe - inglés - italiano - ruso '
                                  '- español',
                                  'Árabe - chino - inglés - francés - ruso - '
                                  'español',
                                  'Árabe - inglés - chino - alemán - ruso - '
                                  'español'],
                 'correcta': 'D'},
                {'pregunta': 'La Organización de los Estados Americanos es '
                             'un organismo de carácter: (IV CEPRU 2022-I)',
                 'alternativas': ['Regional',
                                  'Nacional',
                                  'Local',
                                  'Mundial',
                                  'Universal'],
                 'correcta': 'A'},
                {'pregunta': 'El que dirige el Sistema de Defensa Nacional '
                             'es el presidente: (II CEPRU 2022-I)',
                 'alternativas': ['Del Consejo de Ministros',
                                  'De la Corte Suprema',
                                  'Del Pleno del Jurado Nacional de '
                                  'Elecciones',
                                  'De la Corte Superior de Justicia',
                                  'De la República'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ELEMENTOS',
                      'items': ['En sentido amplio, el Estado es la nación '
                                'jurídicamente organizada.',
                                'En sentido restringido, el Estado es el '
                                'conjunto de organismos que ejercen el poder '
                                'de una nación.',
                                'Los elementos del Estado son: población, '
                                'territorio, organización jurídica y '
                                'soberanía.',
                                'El territorio se caracteriza por ser '
                                'inalienable e inviolable, según el artículo '
                                '54 de la Constitución.',
                                'El territorio comprende el suelo, el '
                                'subsuelo, el espacio aéreo y el mar '
                                'territorial.',
                                'La organización jurídica es el esquema '
                                'legal del Estado, integrado por la '
                                'Constitución, leyes y decretos.',
                                'La soberanía interna es la supremacía sobre '
                                'los demás poderes sociales del territorio; '
                                'la soberanía externa permite relacionarse '
                                'con otros Estados como iguales.']},
                     {'titulo': 'FORMAS DE ESTADO SEGÚN EL PROCESO HISTÓRICO',
                      'items': ['El Estado Constitucional surgió en '
                                'Inglaterra a mediados del siglo XVII, para '
                                'limitar las decisiones de los monarcas '
                                'absolutos.',
                                'El Estado Liberal surgió a lo largo del '
                                'siglo XIX, con pilares como el '
                                'constitucionalismo y la propiedad privada.',
                                'En la democracia liberal o representativa, '
                                'las decisiones no las toma toda la '
                                'comunidad, sino representantes elegidos.',
                                'En los Estados de partido único, solo una '
                                'organización puede ser la legítima '
                                'expresión de la voluntad general, como en '
                                'los sistemas comunistas.']},
                     {'titulo': 'FORMAS DE ESTADO SEGÚN SU ESTRUCTURA',
                      'items': ['El Estado unitario reconoce como fuente de '
                                'soberanía una sola nación, con un gobierno, '
                                'un parlamento y un poder judicial únicos.',
                                'En el Estado unitario existe un solo centro '
                                'de poder para todo el territorio '
                                'nacional.']},
                     {'titulo': 'EL GOBIERNO: CONCEPTO Y FORMAS CLÁSICAS',
                      'items': ['El Gobierno es el principal pilar del '
                                'Estado; la autoridad que dirige, controla y '
                                'administra sus instituciones.',
                                'El Gobierno consiste en la conducción '
                                'política general o ejercicio del poder '
                                'ejecutivo del Estado.',
                                'Según Aristóteles, las formas de gobierno '
                                'se dividen en puras e impuras.',
                                'Las formas puras son monarquía (gobierno de '
                                'uno), aristocracia (gobierno de pocos) y '
                                'democracia (gobierno de muchos).',
                                'Las formas impuras son tiranía (deformación '
                                'de la monarquía), oligarquía (deformación '
                                'de la aristocracia) y demagogia '
                                '(deformación de la democracia).',
                                'La tiranía ocurre cuando el único '
                                'gobernante abusa del poder.',
                                'La oligarquía ocurre cuando el grupo '
                                'gobernante atiende sus propios intereses en '
                                'vez del bien común.',
                                'La demagogia ocurre cuando el gobernante '
                                'halaga al pueblo con regalos para '
                                'convertirlo en una masa servil.']},
                     {'titulo': 'OTRAS FORMAS DE GOBIERNO',
                      'items': ['El gobierno de jure, o de derecho, es el '
                                'que está de acuerdo con la Constitución.',
                                'El gobierno de facto, o de hecho, no ha '
                                'sido elegido según la Constitución, pero no '
                                'necesariamente usa la fuerza.',
                                'El gobierno usurpador carece de título por '
                                'no haber sido elegido, y se mantiene en el '
                                'poder mediante la fuerza.',
                                'El gobierno parlamentario o de gabinete '
                                'tiene un jefe de Estado sin responsabilidad '
                                'y un consejo de ministros responsable ante '
                                'el parlamento.',
                                'El gobierno presidencialista también tiene '
                                'división de poderes, con el Presidente como '
                                'jefe de Estado y de gobierno.']}],
  'qr_reto': [{'pregunta': 'Las lenguas oficiales adoptadas por la ONU son:',
               'respuesta': 'Árabe - chino - inglés - francés - ruso - '
                            'español'},
              {'pregunta': 'La Organización de los Estados Americanos es un '
                           'organismo de carácter:',
               'respuesta': 'Regional'},
              {'pregunta': 'Sin la organización jurídica, el Estado:',
               'respuesta': 'Carecería de forma'}],
  'qr_dato': 'El Estado Constitucional surgió en Inglaterra a mediados del '
             'siglo XVII, para limitar las decisiones de los monarcas '
             'absolutos.'},
 {'num': 7,
  'titulo': 'Constitución Política',
  'secciones': [{'titulo': '7.1 CONCEPTO Y NATURALEZA',
                 'items': ['La Constitución es la fuente de {fuentes} del '
                           'Derecho positivo, la Ley Suprema, que no está '
                           'sujeta a evaluación de validez formal porque no '
                           'existe precepto {superior} a ella.',
                           'La Constitución es el resultado del ejercicio '
                           'del Poder {Constituyente}, cuyo titular es el '
                           '{pueblo}.',
                           'El artículo {51} de la Constitución establece '
                           'que esta prevalece sobre toda otra norma legal.',
                           'Según Blancas Bustamante, la Constitución '
                           'establece la organización de los poderes del '
                           'Estado y reconoce las libertades y {derechos} de '
                           'las personas.',
                           'El fin de la Constitución debe ser afianzar la '
                           '{Justicia}.']},
                {'titulo': '7.2 ETIMOLOGÍA Y ANTECEDENTES',
                 'items': ['La palabra griega «politeía» fue traducida al '
                           'latín por {Cicerón} con el término '
                           '«constitutio».',
                           'Rousseau llamó «{contrato social}» a la decisión '
                           'originaria del pueblo de fundar la comunidad '
                           'política.',
                           'Vattel definió la Constitución del Estado como '
                           'el {reglamento} fundamental que determina cómo '
                           'debe ejercerse la autoridad pública.',
                           'En julio de {1776}, el Congreso de Estados '
                           'Unidos resolvió que los Estados de la '
                           'Confederación se dieran sus propias '
                           'Constituciones.',
                           'A partir de {Thomas Hobbes} se dio el paso de la '
                           'doctrina del derecho natural a la teoría del '
                           'Estado como contrato social.',
                           '{John Locke} explicaba que los individuos '
                           'acuerdan formar una sociedad contractual para '
                           'beneficiarse mutuamente bajo la protección del '
                           'Estado y la ley.']},
                {'titulo': '7.3 CONSTITUCIÓN FORMAL Y MATERIAL',
                 'items': ['Edmund Burke y Ferdinand Lassalle, al igual que '
                           '{Kelsen}, establecieron la división entre '
                           'Constitución formal y {material}.',
                           'La Constitución peruana de {1993} es la norma '
                           'vigente que rige actualmente el ordenamiento '
                           'jurídico del país.']},
                {'titulo': '7.4 CLASES DE CONSTITUCIONES',
                 'items': ['Las constituciones {escritas} están contenidas '
                           'en un documento formal; las {consuetudinarias} '
                           'no están en un único texto.',
                           'Según su origen: las {otorgadas} nacen de un '
                           'acto voluntario del Rey; las {pactadas} surgen '
                           'de un convenio entre el Rey y el Parlamento.',
                           'Las constituciones {populares} expresan la '
                           'voluntad de la Nación como Poder Constituyente, '
                           'aceptadas por el Rey.',
                           'Las {flexibles} pueden modificarse por el '
                           'procedimiento legislativo ordinario; las '
                           '{rígidas} requieren un procedimiento complejo de '
                           'reforma.',
                           'Las {originarias} tienen un principio '
                           'fundamental nuevo; las {derivadas} siguen '
                           'modelos constitucionales ya existentes, '
                           'adaptándolos.',
                           'Las {ideológicas} están cargadas de un programa '
                           'ideológico; las {utilitarias} tienen carácter '
                           'neutral.',
                           'Según la clasificación ontológica de '
                           '{Loewenstein}, la Constitución {normativa} es '
                           'efectivamente vivida por gobernantes y '
                           'gobernados.',
                           'La Constitución {nominal}, según Loewenstein, no '
                           'logra concordancia entre las normas y la '
                           'realidad social y económica.',
                           'La Constitución {semántica}, según Loewenstein, '
                           'sirve para estabilizar y eternizar la '
                           'intervención de quienes dominan el poder.']},
                {'titulo': '7.5 LA JERARQUÍA NORMATIVA (PIRÁMIDE DE KELSEN)',
                 'items': ['El conjunto de normas legales vigentes se '
                           'organiza jerárquicamente en forma de {pirámide}.',
                           'El creador de esta jerarquía piramidal fue el '
                           'filósofo austriaco Hans {Kelsen}, por lo que se '
                           'llama «pirámide de Kelsen».',
                           'Kelsen esquematizó esta jerarquía en su obra «La '
                           'Teoría Pura del Derecho», en el año {1934}.',
                           'El {primer nivel} de la jerarquía normativa es '
                           'la {Constitución}, ley fundamental de la '
                           'organización del Estado.',
                           'El {segundo nivel} incluye los tratados, las '
                           'leyes y las resoluciones legislativas.',
                           'Los {tratados} son acuerdos que el Perú celebra '
                           'con otros Estados; el {Presidente} de la '
                           'República está facultado para celebrarlos.',
                           'Las {leyes orgánicas} instauran el marco '
                           'normativo de instituciones del Estado; requieren '
                           'mayoría {calificada} del Congreso.',
                           'Las {leyes ordinarias} regulan aspectos '
                           'generales o específicos, dictadas por el '
                           '{Congreso}.',
                           'El {Decreto de Urgencia} lo dicta el Presidente '
                           'y lo aprueba el Consejo de Ministros; tiene '
                           'fuerza de ley solo en materia económica y '
                           '{financiera}.',
                           'El Congreso de la República es {unicameral} y '
                           'está integrado por {130} congresistas elegidos '
                           'directamente.']}],
  'cuadros': [{'titulo': '7.1 DENOMINACIONES DE LA CONSTITUCIÓN',
               'encabezados': ['Denominación', 'Significado'],
               'filas': [['Ley {Suprema}',
                          'No sujeta a evaluación de validez formal'],
                         ['Norma de {normas}',
                          'Primera de las normas de producción'],
                         ['{Carta} Fundamental',
                          'Fuente de fuentes del Derecho']]}],
  'preguntas': [{'pregunta': 'La Constitución es considerada la fuente de '
                             'fuentes del Derecho:',
                 'alternativas': ['Consuetudinario',
                                  'Internacional únicamente',
                                  'Comparado',
                                  'Privado',
                                  'Positivo'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución no está sujeta a evaluación de '
                             'validez formal porque:',
                 'alternativas': ['Depende de tratados internacionales',
                                  'Es una ley ordinaria',
                                  'La aprueba el Poder Ejecutivo',
                                  'No existe un precepto superior a ella',
                                  'Es revisada cada año'],
                 'correcta': 'D'},
                {'pregunta': 'La Constitución es resultado del ejercicio del '
                             'Poder:',
                 'alternativas': ['Legislativo ordinario',
                                  'Municipal',
                                  'Ejecutivo',
                                  'Constituyente',
                                  'Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'El titular del Poder Constituyente es:',
                 'alternativas': ['El Congreso',
                                  'El pueblo',
                                  'Los partidos políticos',
                                  'El presidente',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 51 de la Constitución, esta '
                             'prevalece sobre:',
                 'alternativas': ['Solo los decretos',
                                  'Toda otra norma legal',
                                  'Solo los tratados internacionales',
                                  'Solo las leyes penales',
                                  'Nada en particular'],
                 'correcta': 'B'},
                {'pregunta': 'El fin último de la Constitución, según el '
                             'texto, debe ser afianzar:',
                 'alternativas': ['La religión oficial',
                                  'El poder del Estado',
                                  'La Justicia',
                                  'La economía',
                                  'El comercio internacional'],
                 'correcta': 'C'},
                {'pregunta': 'El término latino «constitutio» fue '
                             'introducido por:',
                 'alternativas': ['Rousseau',
                                  'Montesquieu',
                                  'Cicerón',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'C'},
                {'pregunta': 'Rousseau llamó «contrato social» a:',
                 'alternativas': ['Un acuerdo entre monarcas',
                                  'La decisión originaria del pueblo de '
                                  'fundar la comunidad política',
                                  'Un tratado comercial',
                                  'Una ley penal',
                                  'Un pacto religioso'],
                 'correcta': 'B'},
                {'pregunta': 'Vattel definió la Constitución como el '
                             'reglamento fundamental que determina:',
                 'alternativas': ['El idioma nacional',
                                  'Cómo debe ejercerse la autoridad pública',
                                  'La moneda oficial',
                                  'El territorio del Estado',
                                  'Los impuestos del Estado'],
                 'correcta': 'B'},
                {'pregunta': 'En 1776, el Congreso de Estados Unidos '
                             'resolvió que los Estados de la Confederación:',
                 'alternativas': ['Se unificaran en un solo territorio',
                                  'Adoptaran la Constitución inglesa',
                                  'Eliminaran sus leyes',
                                  'Se dieran sus propias Constituciones',
                                  'Formaran una monarquía'],
                 'correcta': 'D'},
                {'pregunta': 'El paso de la doctrina del derecho natural a '
                             'la teoría del Estado como contrato social se '
                             'atribuye a:',
                 'alternativas': ['Thomas Hobbes',
                                  'Montesquieu',
                                  'Rousseau',
                                  'Kelsen',
                                  'Locke exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'John Locke explicaba que los individuos forman '
                             'una sociedad para:',
                 'alternativas': ['Vivir sin normas',
                                  'Someterse a un monarca absoluto',
                                  'Depender de otro Estado',
                                  'Beneficiarse mutuamente bajo la '
                                  'protección del Estado y la ley',
                                  'Eliminar toda autoridad'],
                 'correcta': 'D'},
                {'pregunta': 'La división entre Constitución formal y '
                             'material fue establecida, entre otros, por:',
                 'alternativas': ['Cicerón',
                                  'Rousseau',
                                  'Vattel',
                                  'Bossuet',
                                  'Kelsen'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución peruana actualmente vigente '
                             'data del año:',
                 'alternativas': ['1920', '1979', '1993', '1933', '1856'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución es descrita como la «norma de '
                             'normas» porque:',
                 'alternativas': ['No tiene jerarquía superior a las leyes',
                                  'Solo aplica al Poder Judicial',
                                  'Solo rige el comercio',
                                  'Es opcional para el Estado',
                                  'Es la primera de las normas de '
                                  'producción'],
                 'correcta': 'E'},
                {'pregunta': 'Según Blancas Bustamante, la Constitución '
                             'define la posición de las personas frente al '
                             'Estado mediante:',
                 'alternativas': ['Tratados internacionales exclusivamente',
                                  'Solo sanciones penales',
                                  'Solo obligaciones tributarias',
                                  'El reconocimiento de libertades y '
                                  'derechos',
                                  'Acuerdos comerciales'],
                 'correcta': 'D'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano tuvo como fuente formal:',
                 'alternativas': ['La Constitución española',
                                  'La Constitución rusa',
                                  'El Código de Hammurabi',
                                  'Las Constituciones de los Estados de la '
                                  'Confederación norteamericana',
                                  'La Carta Magna inglesa'],
                 'correcta': 'D'},
                {'pregunta': 'En el siglo XVIII, se consideraba «todo el '
                             'pueblo» al llamado:',
                 'alternativas': ['Primer Estado',
                                  'Tercer Estado, compuesto por la burguesía',
                                  'Cuarto Estado',
                                  'Estado eclesiástico',
                                  'Segundo Estado'],
                 'correcta': 'B'},
                {'pregunta': 'Rousseau llamó «leyes fundamentales» a:',
                 'alternativas': ['La estructura jurídica correspondiente al '
                                  'régimen político',
                                  'El derecho penal',
                                  'La estructura de poder',
                                  'Los tratados internacionales',
                                  'Las costumbres sociales'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución constituye, define y crea los '
                             'poderes:',
                 'alternativas': ['Solo el legislativo',
                                  'Solo el ejecutivo',
                                  'Legislativo, ejecutivo y judicial',
                                  'Ninguno en particular',
                                  'Solo el judicial'],
                 'correcta': 'C'},
                {'pregunta': 'Una Constitución contenida en un documento '
                             'formal se llama Constitución:',
                 'alternativas': ['Semántica',
                                  'Escrita',
                                  'Flexible',
                                  'Nominal',
                                  'Consuetudinaria'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que nacen de un acto '
                             'voluntario del Rey, cediendo poderes al '
                             'Parlamento, se llaman:',
                 'alternativas': ['Populares',
                                  'Pactadas',
                                  'Otorgadas',
                                  'Rígidas',
                                  'Derivadas'],
                 'correcta': 'C'},
                {'pregunta': 'Las Constituciones que surgen de un '
                             'convenio-pacto entre el Rey y el Parlamento se '
                             'llaman:',
                 'alternativas': ['Originarias',
                                  'Pactadas',
                                  'Otorgadas',
                                  'Populares',
                                  'Flexibles'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que pueden modificarse por '
                             'el procedimiento legislativo ordinario se '
                             'llaman:',
                 'alternativas': ['Derivadas',
                                  'Otorgadas',
                                  'Semánticas',
                                  'Rígidas',
                                  'Flexibles'],
                 'correcta': 'E'},
                {'pregunta': 'Las Constituciones que requieren un '
                             'procedimiento complejo para su reforma se '
                             'llaman:',
                 'alternativas': ['Pactadas',
                                  'Originarias',
                                  'Rígidas',
                                  'Nominales',
                                  'Flexibles'],
                 'correcta': 'C'},
                {'pregunta': 'Las Constituciones cargadas de un programa '
                             'ideológico se llaman:',
                 'alternativas': ['Semánticas',
                                  'Derivadas',
                                  'Ideológicas',
                                  'Nominales',
                                  'Utilitarias'],
                 'correcta': 'C'},
                {'pregunta': 'Según la clasificación de Loewenstein, la '
                             'Constitución efectivamente vivida por '
                             'gobernantes y gobernados se llama:',
                 'alternativas': ['Rígida',
                                  'Semántica',
                                  'Nominal',
                                  'Normativa',
                                  'Utilitaria'],
                 'correcta': 'D'},
                {'pregunta': 'Según Loewenstein, la Constitución que sirve '
                             'para estabilizar y eternizar el poder de los '
                             'dominadores se llama:',
                 'alternativas': ['Normativa',
                                  'Flexible',
                                  'Semántica',
                                  'Ideológica',
                                  'Nominal'],
                 'correcta': 'C'},
                {'pregunta': 'El creador de la jerarquía normativa '
                             'piramidal, conocida como «pirámide de Kelsen», '
                             'fue:',
                 'alternativas': ['Hans Kelsen',
                                  'Aristóteles',
                                  'Locke',
                                  'Montesquieu',
                                  'Rousseau'],
                 'correcta': 'A'},
                {'pregunta': 'Kelsen esquematizó la jerarquía normativa en '
                             'su obra «La Teoría Pura del Derecho», '
                             'publicada en:',
                 'alternativas': ['1934', '1960', '1919', '1945', '1900'],
                 'correcta': 'A'},
                {'pregunta': 'El primer nivel de la jerarquía normativa '
                             'peruana es:',
                 'alternativas': ['La Constitución',
                                  'Los tratados',
                                  'Los decretos supremos',
                                  'Las resoluciones',
                                  'Las leyes ordinarias'],
                 'correcta': 'A'},
                {'pregunta': 'El segundo nivel de la jerarquía normativa '
                             'incluye tratados, leyes y:',
                 'alternativas': ['Circulares',
                                  'Resoluciones legislativas',
                                  'Directivas internas',
                                  'Ordenanzas municipales',
                                  'Memorandos'],
                 'correcta': 'B'},
                {'pregunta': 'El funcionario facultado para celebrar '
                             'tratados internacionales del Perú es:',
                 'alternativas': ['El Congreso',
                                  'El Poder Judicial',
                                  'La Contraloría',
                                  'El Presidente de la República',
                                  'El Tribunal Constitucional'],
                 'correcta': 'D'},
                {'pregunta': 'Las leyes que instauran el marco normativo de '
                             'instituciones del Estado y requieren mayoría '
                             'calificada se llaman leyes:',
                 'alternativas': ['Resolutivas',
                                  'Supletorias',
                                  'Ordinarias',
                                  'Orgánicas',
                                  'Reglamentarias'],
                 'correcta': 'D'},
                {'pregunta': 'El Decreto de Urgencia lo dicta el Presidente '
                             'y lo aprueba:',
                 'alternativas': ['La Contraloría',
                                  'El Consejo de Ministros',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'El Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso de la República del Perú es de '
                             'tipo:',
                 'alternativas': ['Unicameral',
                                  'Tricameral',
                                  'Mixto',
                                  'Regional',
                                  'Bicameral'],
                 'correcta': 'A'},
                {'pregunta': 'El número de congresistas que integran el '
                             'Congreso de la República es:',
                 'alternativas': ['150', '110', '120', '130', '100'],
                 'correcta': 'D'},
                {'pregunta': 'El titular del poder constituyente viene a '
                             'ser: (II CEPRU 2025-I)',
                 'alternativas': ['El congreso',
                                  'El presidente',
                                  'El pueblo',
                                  'La ONU',
                                  'El Estado'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 43 de la Constitución, son '
                             'características del gobierno del Perú: (III '
                             'CEPRU 2025-I)',
                 'alternativas': ['Democrático - social - unitario',
                                  'Independiente - democrático - soberano',
                                  'Inviolable - inalienable',
                                  'Uno e indivisible',
                                  'Unitario - representativo - '
                                  'descentralizado'],
                 'correcta': 'E'},
                {'pregunta': 'La norma fundamental del Estado que establece '
                             'la organización de sus poderes, la competencia '
                             'de estos y la posición de la persona en '
                             'relación con el Estado, es: (II CEPRU 2023-II)',
                 'alternativas': ['La ley',
                                  'El decreto',
                                  'La Constitución',
                                  'La resolución',
                                  'El reglamento'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho de todo ciudadano de presentar uno '
                             'o más proyectos de ley se denomina: (II CEPRU '
                             '2023-II)',
                 'alternativas': ['Iniciativa Legislativa',
                                  'Iniciativa de reforma Constitucional',
                                  'Referéndum',
                                  'Remoción',
                                  'Revocatoria'],
                 'correcta': 'A'},
                {'pregunta': '¿Con qué Constitución se aprobó el voto a los '
                             'analfabetos? (II CEPRU 2022-II)',
                 'alternativas': ['Constitución de 1979',
                                  'Constitución de 1933',
                                  'Constitución de 1993',
                                  'Constitución de 1920',
                                  'Constitución de 1956'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución Política del Estado de 1993, '
                             'durante el gobierno del ex presidente Alberto '
                             'Fujimori, fue redactada por el: (II CEPRU '
                             '2022-II)',
                 'alternativas': ['Poder constituido democrático',
                                  'Poder constituyente democrático',
                                  'Poder Legislativo democrático',
                                  'Congreso Ejecutivo democrático',
                                  'Congreso constituyente democrático'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y NATURALEZA',
                      'items': ['La Constitución es la fuente de fuentes del '
                                'Derecho positivo, la Ley Suprema, que no '
                                'está sujeta a evaluación de validez formal '
                                'porque no existe precepto superior a ella.',
                                'La Constitución es el resultado del '
                                'ejercicio del Poder Constituyente, cuyo '
                                'titular es el pueblo.',
                                'El artículo 51 de la Constitución establece '
                                'que esta prevalece sobre toda otra norma '
                                'legal.',
                                'Según Blancas Bustamante, la Constitución '
                                'establece la organización de los poderes '
                                'del Estado y reconoce las libertades y '
                                'derechos de las personas.',
                                'El fin de la Constitución debe ser afianzar '
                                'la Justicia.']},
                     {'titulo': 'ETIMOLOGÍA Y ANTECEDENTES',
                      'items': ['La palabra griega «politeía» fue traducida '
                                'al latín por Cicerón con el término '
                                '«constitutio».',
                                'Rousseau llamó «contrato social» a la '
                                'decisión originaria del pueblo de fundar la '
                                'comunidad política.',
                                'Vattel definió la Constitución del Estado '
                                'como el reglamento fundamental que '
                                'determina cómo debe ejercerse la autoridad '
                                'pública.',
                                'En julio de 1776, el Congreso de Estados '
                                'Unidos resolvió que los Estados de la '
                                'Confederación se dieran sus propias '
                                'Constituciones.',
                                'A partir de Thomas Hobbes se dio el paso de '
                                'la doctrina del derecho natural a la teoría '
                                'del Estado como contrato social.',
                                'John Locke explicaba que los individuos '
                                'acuerdan formar una sociedad contractual '
                                'para beneficiarse mutuamente bajo la '
                                'protección del Estado y la ley.']},
                     {'titulo': 'CONSTITUCIÓN FORMAL Y MATERIAL',
                      'items': ['Edmund Burke y Ferdinand Lassalle, al igual '
                                'que Kelsen, establecieron la división entre '
                                'Constitución formal y material.',
                                'La Constitución peruana de 1993 es la norma '
                                'vigente que rige actualmente el '
                                'ordenamiento jurídico del país.']},
                     {'titulo': 'CLASES DE CONSTITUCIONES',
                      'items': ['Las constituciones escritas están '
                                'contenidas en un documento formal; las '
                                'consuetudinarias no están en un único '
                                'texto.',
                                'Según su origen: las otorgadas nacen de un '
                                'acto voluntario del Rey; las pactadas '
                                'surgen de un convenio entre el Rey y el '
                                'Parlamento.',
                                'Las constituciones populares expresan la '
                                'voluntad de la Nación como Poder '
                                'Constituyente, aceptadas por el Rey.',
                                'Las flexibles pueden modificarse por el '
                                'procedimiento legislativo ordinario; las '
                                'rígidas requieren un procedimiento complejo '
                                'de reforma.',
                                'Las originarias tienen un principio '
                                'fundamental nuevo; las derivadas siguen '
                                'modelos constitucionales ya existentes, '
                                'adaptándolos.',
                                'Las ideológicas están cargadas de un '
                                'programa ideológico; las utilitarias tienen '
                                'carácter neutral.',
                                'Según la clasificación ontológica de '
                                'Loewenstein, la Constitución normativa es '
                                'efectivamente vivida por gobernantes y '
                                'gobernados.',
                                'La Constitución nominal, según Loewenstein, '
                                'no logra concordancia entre las normas y la '
                                'realidad social y económica.',
                                'La Constitución semántica, según '
                                'Loewenstein, sirve para estabilizar y '
                                'eternizar la intervención de quienes '
                                'dominan el poder.']},
                     {'titulo': 'LA JERARQUÍA NORMATIVA (PIRÁMIDE DE KELSEN)',
                      'items': ['El conjunto de normas legales vigentes se '
                                'organiza jerárquicamente en forma de '
                                'pirámide.',
                                'El creador de esta jerarquía piramidal fue '
                                'el filósofo austriaco Hans Kelsen, por lo '
                                'que se llama «pirámide de Kelsen».',
                                'Kelsen esquematizó esta jerarquía en su '
                                'obra «La Teoría Pura del Derecho», en el '
                                'año 1934.',
                                'El primer nivel de la jerarquía normativa '
                                'es la Constitución, ley fundamental de la '
                                'organización del Estado.',
                                'El segundo nivel incluye los tratados, las '
                                'leyes y las resoluciones legislativas.',
                                'Los tratados son acuerdos que el Perú '
                                'celebra con otros Estados; el Presidente de '
                                'la República está facultado para '
                                'celebrarlos.',
                                'Las leyes orgánicas instauran el marco '
                                'normativo de instituciones del Estado; '
                                'requieren mayoría calificada del Congreso.',
                                'Las leyes ordinarias regulan aspectos '
                                'generales o específicos, dictadas por el '
                                'Congreso.',
                                'El Decreto de Urgencia lo dicta el '
                                'Presidente y lo aprueba el Consejo de '
                                'Ministros; tiene fuerza de ley solo en '
                                'materia económica y financiera.',
                                'El Congreso de la República es unicameral y '
                                'está integrado por 130 congresistas '
                                'elegidos directamente.']}],
  'qr_reto': [{'pregunta': 'El Congreso de la República del Perú es de tipo:',
               'respuesta': 'Unicameral'},
              {'pregunta': 'Las Constituciones que surgen de un '
                           'convenio-pacto entre el Rey y el Parlamento se '
                           'llaman:',
               'respuesta': 'Pactadas'},
              {'pregunta': 'La Constitución es descrita como la «norma de '
                           'normas» porque:',
               'respuesta': 'Es la primera de las normas de producción'}],
  'qr_dato': 'La Constitución peruana de 1993 es la norma vigente que rige '
             'actualmente el ordenamiento jurídico del país.'},
 {'num': 8,
  'titulo': 'Derechos Civiles y Políticos',
  'secciones': [{'titulo': '8.1 EL PACTO INTERNACIONAL DE DERECHOS CIVILES Y '
                           'POLÍTICOS',
                 'items': ['El PIDCP fue adoptado por la Asamblea General de '
                           'la ONU mediante la Resolución 2200 A (XXI), el '
                           '{16} de diciembre de {1966}.',
                           'El PIDCP entró en vigor el {23} de marzo de '
                           '{1976}, y ha sido ratificado por {167} Estados.',
                           'El PIDCP consta de {6} partes, {53} artículos y '
                           'dos protocolos {facultativos}.',
                           'El Primer Protocolo Facultativo regula los '
                           'mecanismos por los que las personas pueden '
                           'iniciar {denuncias} contra los Estados.',
                           'El Segundo Protocolo Facultativo está destinado '
                           'a la abolición de la pena de {muerte}.']},
                {'titulo': '8.2 CONCEPTO DE DERECHOS CIVILES',
                 'items': ['Los derechos civiles son reconocidos por todos '
                           'los ciudadanos y por la {ley}, dentro de un '
                           '{Estado} determinado.',
                           'A diferencia de los derechos civiles, los '
                           'derechos {naturales} o humanos son '
                           'internacionales y se tienen por el mero hecho de '
                           '{nacer}.',
                           '{John Locke} sostuvo que los derechos naturales '
                           'a la vida, la libertad y la propiedad debían '
                           'convertirse en derechos civiles protegidos por '
                           'el Estado.',
                           'El derecho a la {vida} es considerado el primero '
                           'de todos los derechos, pues es generador de '
                           'cualquier otro derecho posible.',
                           'El derecho a la integridad {física} y '
                           'psicológica protege a la persona de '
                           'mutilaciones, torturas y tratos crueles e '
                           'inhumanos.',
                           'El derecho a la {identidad} comprende el derecho '
                           'a tener un nombre y a un documento que permita '
                           'la identificación de la persona.']},
                {'titulo': '8.3 CONCEPTO DE DERECHOS POLÍTICOS',
                 'items': ['Los derechos {políticos} son los reconocidos por '
                           'la Constitución y las leyes, que permiten '
                           'participar directa o indirectamente en el '
                           '{gobierno} del Estado.',
                           'Los derechos políticos posibilitan la toma de '
                           '{decisiones} respecto del gobierno del Estado.']},
                {'titulo': '8.4 LEY DE PARTICIPACIÓN Y CONTROL CIUDADANO '
                           '(LEY 26300)',
                 'items': ['La {Ley 26300}, Ley de los Derechos de '
                           'Participación y Control Ciudadano, regula el '
                           'ejercicio de estos derechos junto con la '
                           'Constitución de {1993}.',
                           'Los ciudadanos pueden participar mediante '
                           '{referéndum}, iniciativa legislativa, remoción o '
                           '{revocación} de autoridades y rendición de '
                           'cuentas.',
                           'Es {nulo} y punible todo acto que prohíba o '
                           'limite al ciudadano el ejercicio de estos '
                           'derechos de {participación}.']},
                {'titulo': '8.5 DERECHOS DE PARTICIPACIÓN CIUDADANA',
                 'items': ['La {iniciativa de reforma constitucional} '
                           'requiere la adhesión del {0,3}% de la población '
                           'electoral nacional.',
                           'Es improcedente toda iniciativa de reforma que '
                           'recorte los derechos ciudadanos del artículo '
                           '{2}° de la Constitución.',
                           'La {iniciativa en la formación de leyes} '
                           'requiere firmas de no menos del 0,3% del '
                           'electorado; el Congreso tiene {120} días para '
                           'dictaminarla.',
                           'El {referéndum} permite pronunciarse sobre la '
                           'reforma de la Constitución, la aprobación o '
                           'desaprobación de leyes.',
                           'El referéndum puede ser solicitado por no menos '
                           'del {10}% del electorado nacional.',
                           'El resultado del referéndum requiere la mitad '
                           'más uno de votos favorables, y ser aprobado por '
                           'no menos del {30}% del total de votantes.',
                           'Una norma aprobada por referéndum no puede '
                           'modificarse dentro de los {dos} años siguientes, '
                           'salvo nuevo referéndum.']},
                {'titulo': '8.6 DERECHOS DE CONTROL DE LOS CIUDADANOS',
                 'items': ['La {revocatoria} es el derecho de la ciudadanía '
                           'para destituir de sus cargos a alcaldes, '
                           'regidores y autoridades de elección {popular}.',
                           'La revocatoria no procede durante el {primer} y '
                           'último año de mandato, salvo el caso de '
                           '{magistrados}.',
                           'Para solicitar la revocatoria, la solicitud no '
                           'requiere ser probada, solo {fundamentada}.',
                           'Se requiere la firma de al menos el {25}% de los '
                           'electores de una autoridad, con un máximo de '
                           '{400 000} firmas.',
                           'Para revocar a una autoridad se requiere la '
                           'mitad más uno de votos, y que haya asistido al '
                           'menos el {50}% de los electores hábiles.',
                           'Si la revocatoria no procede, no se admite una '
                           'nueva petición hasta después de {dos} años.',
                           'Tras la revocatoria, asume el cargo quien '
                           'alcanzó el siguiente lugar en {votos} de la '
                           'misma lista.']}],
  'cuadros': [{'titulo': '8.1 ESTRUCTURA DEL PIDCP',
               'encabezados': ['Parte', 'Artículos', 'Contenido'],
               'filas': [['I', '1', 'Libre {determinación} de los pueblos'],
                         ['II',
                          '2-5',
                          '{Garantía} de no exclusión y protección de '
                          'derechos'],
                         ['III',
                          '6-27',
                          'Protección contra la {discriminación}'],
                         ['IV',
                          '28-45',
                          '{Comité}, elección y funcionamiento'],
                         ['VI',
                          '48-53',
                          'Ratificación y {entrada} en vigor']]}],
  'preguntas': [{'pregunta': 'El PIDCP fue adoptado por la Asamblea General '
                             'de la ONU en el año:',
                 'alternativas': ['1993', '2000', '1966', '1976', '1948'],
                 'correcta': 'C'},
                {'pregunta': 'El PIDCP entró en vigor el:',
                 'alternativas': ['10 de diciembre de 1948',
                                  '23 de marzo de 1976',
                                  '30 de abril de 1990',
                                  '1 de enero de 1980',
                                  '16 de diciembre de 1966'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP ha sido ratificado por un total de '
                             'Estados de:',
                 'alternativas': ['200', '167', '75', '100', '50'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP consta de un número de partes igual '
                             'a:',
                 'alternativas': ['3', '6', '8', '10', '4'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP consta de un número de artículos '
                             'igual a:',
                 'alternativas': ['53', '25', '75', '100', '30'],
                 'correcta': 'A'},
                {'pregunta': 'El Primer Protocolo Facultativo del PIDCP '
                             'regula:',
                 'alternativas': ['La migración',
                                  'Los derechos económicos',
                                  'Los mecanismos de denuncia contra los '
                                  'Estados',
                                  'La abolición de la pena de muerte',
                                  'El comercio internacional'],
                 'correcta': 'C'},
                {'pregunta': 'El Segundo Protocolo Facultativo del PIDCP '
                             'está destinado a:',
                 'alternativas': ['La abolición de la pena de muerte',
                                  'La protección ambiental',
                                  'Los derechos laborales',
                                  'El mecanismo de denuncias',
                                  'El comercio exterior'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos civiles se distinguen de los '
                             'derechos naturales porque son:',
                 'alternativas': ['Universales sin excepción',
                                  'Internacionales por naturaleza',
                                  'Otorgados por organismos internacionales',
                                  'Innatos al nacer',
                                  'Reconocidos dentro de un Estado '
                                  'determinado'],
                 'correcta': 'E'},
                {'pregunta': 'Los derechos naturales o humanos se poseen:',
                 'alternativas': ['Solo si el Estado los otorga',
                                  'Solo a partir de la mayoría de edad',
                                  'Solo en democracias',
                                  'Únicamente si se solicitan',
                                  'Por el mero hecho de nacer'],
                 'correcta': 'E'},
                {'pregunta': 'John Locke sostuvo que debían convertirse en '
                             'derechos civiles protegidos por el Estado:',
                 'alternativas': ['La vida, la libertad y la propiedad',
                                  'Solo el derecho a la vida',
                                  'Solo el derecho a la propiedad',
                                  'Los derechos económicos',
                                  'Los derechos culturales'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho considerado el primero de todos, '
                             'generador de cualquier otro derecho, es el '
                             'derecho a:',
                 'alternativas': ['La propiedad',
                                  'El trabajo',
                                  'La libertad de expresión',
                                  'La vida',
                                  'La educación'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho a la integridad física y '
                             'psicológica protege contra:',
                 'alternativas': ['La migración',
                                  'Los impuestos elevados',
                                  'El comercio informal',
                                  'Las torturas y tratos crueles e inhumanos',
                                  'La libre expresión'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho a la identidad comprende, entre '
                             'otros aspectos:',
                 'alternativas': ['El derecho a tener un nombre y documento '
                                  'de identidad',
                                  'El derecho al trabajo',
                                  'El derecho a la educación superior',
                                  'El derecho al voto',
                                  'El derecho a la propiedad'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos políticos permiten participar en:',
                 'alternativas': ['La vida privada únicamente',
                                  'El gobierno del Estado y la toma de '
                                  'decisiones',
                                  'Solo actividades económicas',
                                  'El comercio internacional',
                                  'Solo actividades religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos políticos están reconocidos por:',
                 'alternativas': ['Solo la costumbre',
                                  'Ninguna norma específica',
                                  'Organismos privados',
                                  'Solo tratados internacionales',
                                  'La Constitución y las leyes'],
                 'correcta': 'E'},
                {'pregunta': 'La Parte III del PIDCP, artículos 6 a 27, '
                             'protege contra:',
                 'alternativas': ['El desempleo',
                                  'El comercio desleal',
                                  'La contaminación ambiental',
                                  'La evasión tributaria',
                                  'La discriminación por sexo, religión, '
                                  'raza u otras formas'],
                 'correcta': 'E'},
                {'pregunta': 'La Parte I del PIDCP, artículo 1, trata sobre:',
                 'alternativas': ['Los tratados bilaterales',
                                  'La migración',
                                  'El comercio internacional',
                                  'La pena de muerte',
                                  'La libre determinación de los pueblos'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDCP es catalogado como un tratado '
                             'internacional de tipo:',
                 'alternativas': ['Comercial',
                                  'Bilateral',
                                  'Privado',
                                  'Multilateral general',
                                  'Regional exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'La contraposición al derecho a la vida es:',
                 'alternativas': ['La enfermedad',
                                  'El envejecimiento',
                                  'La discapacidad',
                                  'La muerte',
                                  'La pobreza'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los derechos civiles y políticos '
                             'mencionados figura el derecho a elegir y:',
                 'alternativas': ['Ser elegido representante',
                                  'Rechazar la ciudadanía',
                                  'No participar',
                                  'No votar',
                                  'Evadir impuestos'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de los Derechos de Participación y '
                             'Control Ciudadano se conoce como Ley:',
                 'alternativas': ['27444',
                                  '26859',
                                  '26300',
                                  '26301',
                                  '28237'],
                 'correcta': 'C'},
                {'pregunta': 'Según la Ley 26300, los ciudadanos pueden '
                             'participar mediante referéndum, iniciativa '
                             'legislativa, remoción o:',
                 'alternativas': ['Amnistía',
                                  'Censura',
                                  'Revocación de autoridades',
                                  'Indulto',
                                  'Vacancia exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'Todo acto que prohíba o limite al ciudadano el '
                             'ejercicio de sus derechos de participación es '
                             'considerado:',
                 'alternativas': ['Aceptable temporalmente',
                                  'Nulo y punible',
                                  'Legal si está motivado',
                                  'Sujeto a apelación únicamente',
                                  'Válido con restricciones'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa de reforma constitucional '
                             'requiere la adhesión de un porcentaje de la '
                             'población electoral nacional igual a:',
                 'alternativas': ['25%', '3%', '0,3%', '1%', '10%'],
                 'correcta': 'C'},
                {'pregunta': 'Es improcedente toda iniciativa de reforma '
                             'constitucional que recorte los derechos '
                             'ciudadanos consagrados en el artículo:',
                 'alternativas': ['Artículo 1',
                                  'Artículo 5',
                                  'Artículo 20',
                                  'Artículo 10',
                                  'Artículo 2'],
                 'correcta': 'E'},
                {'pregunta': 'La iniciativa en la formación de leyes '
                             'requiere firmas de no menos del 0,3% del '
                             'electorado, y el Congreso tiene un plazo de:',
                 'alternativas': ['90 días',
                                  '60 días',
                                  '30 días',
                                  '120 días',
                                  '180 días'],
                 'correcta': 'D'},
                {'pregunta': 'El referéndum es el derecho de los ciudadanos '
                             'para pronunciarse sobre, entre otros temas, la '
                             'reforma de:',
                 'alternativas': ['Solo tratados internacionales',
                                  'Solo ordenanzas municipales',
                                  'La Constitución',
                                  'Solo el presupuesto',
                                  'Solo decretos supremos'],
                 'correcta': 'C'},
                {'pregunta': 'El referéndum puede ser solicitado por un '
                             'número de ciudadanos no menor a:',
                 'alternativas': ['5% del electorado',
                                  '25% del electorado',
                                  '50% del electorado',
                                  '10% del electorado',
                                  '0,3% del electorado'],
                 'correcta': 'D'},
                {'pregunta': 'Para que el referéndum sea válido, debe ser '
                             'aprobado por no menos del:',
                 'alternativas': ['30% del total de votantes',
                                  '90% de los votantes',
                                  '10% de los votantes',
                                  '70% de los votantes',
                                  '50% de los votantes'],
                 'correcta': 'A'},
                {'pregunta': 'Una norma aprobada mediante referéndum no '
                             'puede modificarse dentro de los siguientes:',
                 'alternativas': ['Diez años',
                                  'Un año',
                                  'Seis meses',
                                  'Dos años',
                                  'Cinco años'],
                 'correcta': 'D'},
                {'pregunta': 'La revocatoria es el derecho de la ciudadanía '
                             'para destituir de sus cargos a autoridades de '
                             'elección:',
                 'alternativas': ['Judicial exclusiva',
                                  'Eclesiástica',
                                  'Popular',
                                  'Militar',
                                  'Designada'],
                 'correcta': 'C'},
                {'pregunta': 'La revocatoria no procede durante el primer y '
                             'último año de mandato, salvo en el caso de:',
                 'alternativas': ['Alcaldes',
                                  'Regidores',
                                  'Ministros',
                                  'Congresistas',
                                  'Magistrados'],
                 'correcta': 'E'},
                {'pregunta': 'Para solicitar la revocatoria, la solicitud:',
                 'alternativas': ['Requiere sentencia previa',
                                  'Necesita aprobación del Congreso',
                                  'Debe ser probada judicialmente',
                                  'Requiere referéndum previo',
                                  'Solo requiere ser fundamentada'],
                 'correcta': 'E'},
                {'pregunta': 'Para solicitar la revocatoria se requiere la '
                             'firma de al menos un porcentaje de electores '
                             'de la autoridad igual a:',
                 'alternativas': ['5%', '40%', '10%', '25%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'El número máximo de firmas requeridas para '
                             'solicitar una revocatoria es:',
                 'alternativas': ['50 000',
                                  '250 000',
                                  '400 000',
                                  '1 000 000',
                                  '100 000'],
                 'correcta': 'C'},
                {'pregunta': 'Para revocar a una autoridad se requiere la '
                             'mitad más uno de los votos, y que haya '
                             'asistido al menos:',
                 'alternativas': ['El 10% de electores hábiles',
                                  'Todos los electores hábiles',
                                  'El 75% de electores hábiles',
                                  'El 50% de electores hábiles',
                                  'El 25% de electores hábiles'],
                 'correcta': 'D'},
                {'pregunta': 'Si la revocatoria no procede, no se admite una '
                             'nueva petición hasta después de:',
                 'alternativas': ['Dos años',
                                  'Seis meses',
                                  'Nunca más',
                                  'Un año',
                                  'Cinco años'],
                 'correcta': 'A'},
                {'pregunta': 'Tras una revocatoria exitosa, asume el cargo:',
                 'alternativas': ['El ganador de nuevas elecciones '
                                  'inmediatas',
                                  'Un candidato designado por el JNE',
                                  'Ninguno, el cargo queda vacante',
                                  'El regidor de mayor edad',
                                  'Quien alcanzó el siguiente lugar en votos '
                                  'de la misma lista'],
                 'correcta': 'E'},
                {'pregunta': 'Un derecho constitucional conexo con la '
                             'libertad individual es: (II CEPRU 2018-I)',
                 'alternativas': ['La rectificación',
                                  'La remuneración',
                                  'El debido proceso',
                                  'La inviolabilidad científica',
                                  'La petición de pensión'],
                 'correcta': 'C'},
                {'pregunta': 'Una característica del derecho al voto es que '
                             'es: (II CEPRU 2022-I)',
                 'alternativas': ['Limitado',
                                  'Desigual',
                                  'Irrenunciable',
                                  'Renunciable',
                                  'Impersonal'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'EL PACTO INTERNACIONAL DE DERECHOS CIVILES '
                                'Y POLÍTICOS',
                      'items': ['El PIDCP fue adoptado por la Asamblea '
                                'General de la ONU mediante la Resolución '
                                '2200 A (XXI), el 16 de diciembre de 1966.',
                                'El PIDCP entró en vigor el 23 de marzo de '
                                '1976, y ha sido ratificado por 167 Estados.',
                                'El PIDCP consta de 6 partes, 53 artículos y '
                                'dos protocolos facultativos.',
                                'El Primer Protocolo Facultativo regula los '
                                'mecanismos por los que las personas pueden '
                                'iniciar denuncias contra los Estados.',
                                'El Segundo Protocolo Facultativo está '
                                'destinado a la abolición de la pena de '
                                'muerte.']},
                     {'titulo': 'CONCEPTO DE DERECHOS CIVILES',
                      'items': ['Los derechos civiles son reconocidos por '
                                'todos los ciudadanos y por la ley, dentro '
                                'de un Estado determinado.',
                                'A diferencia de los derechos civiles, los '
                                'derechos naturales o humanos son '
                                'internacionales y se tienen por el mero '
                                'hecho de nacer.',
                                'John Locke sostuvo que los derechos '
                                'naturales a la vida, la libertad y la '
                                'propiedad debían convertirse en derechos '
                                'civiles protegidos por el Estado.',
                                'El derecho a la vida es considerado el '
                                'primero de todos los derechos, pues es '
                                'generador de cualquier otro derecho '
                                'posible.',
                                'El derecho a la integridad física y '
                                'psicológica protege a la persona de '
                                'mutilaciones, torturas y tratos crueles e '
                                'inhumanos.',
                                'El derecho a la identidad comprende el '
                                'derecho a tener un nombre y a un documento '
                                'que permita la identificación de la '
                                'persona.']},
                     {'titulo': 'CONCEPTO DE DERECHOS POLÍTICOS',
                      'items': ['Los derechos políticos son los reconocidos '
                                'por la Constitución y las leyes, que '
                                'permiten participar directa o '
                                'indirectamente en el gobierno del Estado.',
                                'Los derechos políticos posibilitan la toma '
                                'de decisiones respecto del gobierno del '
                                'Estado.']},
                     {'titulo': 'LEY DE PARTICIPACIÓN Y CONTROL CIUDADANO '
                                '(LEY 26300)',
                      'items': ['La Ley 26300, Ley de los Derechos de '
                                'Participación y Control Ciudadano, regula '
                                'el ejercicio de estos derechos junto con la '
                                'Constitución de 1993.',
                                'Los ciudadanos pueden participar mediante '
                                'referéndum, iniciativa legislativa, '
                                'remoción o revocación de autoridades y '
                                'rendición de cuentas.',
                                'Es nulo y punible todo acto que prohíba o '
                                'limite al ciudadano el ejercicio de estos '
                                'derechos de participación.']},
                     {'titulo': 'DERECHOS DE PARTICIPACIÓN CIUDADANA',
                      'items': ['La iniciativa de reforma constitucional '
                                'requiere la adhesión del 0,3% de la '
                                'población electoral nacional.',
                                'Es improcedente toda iniciativa de reforma '
                                'que recorte los derechos ciudadanos del '
                                'artículo 2° de la Constitución.',
                                'La iniciativa en la formación de leyes '
                                'requiere firmas de no menos del 0,3% del '
                                'electorado; el Congreso tiene 120 días para '
                                'dictaminarla.',
                                'El referéndum permite pronunciarse sobre la '
                                'reforma de la Constitución, la aprobación o '
                                'desaprobación de leyes.',
                                'El referéndum puede ser solicitado por no '
                                'menos del 10% del electorado nacional.',
                                'El resultado del referéndum requiere la '
                                'mitad más uno de votos favorables, y ser '
                                'aprobado por no menos del 30% del total de '
                                'votantes.',
                                'Una norma aprobada por referéndum no puede '
                                'modificarse dentro de los dos años '
                                'siguientes, salvo nuevo referéndum.']},
                     {'titulo': 'DERECHOS DE CONTROL DE LOS CIUDADANOS',
                      'items': ['La revocatoria es el derecho de la '
                                'ciudadanía para destituir de sus cargos a '
                                'alcaldes, regidores y autoridades de '
                                'elección popular.',
                                'La revocatoria no procede durante el primer '
                                'y último año de mandato, salvo el caso de '
                                'magistrados.',
                                'Para solicitar la revocatoria, la solicitud '
                                'no requiere ser probada, solo fundamentada.',
                                'Se requiere la firma de al menos el 25% de '
                                'los electores de una autoridad, con un '
                                'máximo de 400 000 firmas.',
                                'Para revocar a una autoridad se requiere la '
                                'mitad más uno de votos, y que haya asistido '
                                'al menos el 50% de los electores hábiles.',
                                'Si la revocatoria no procede, no se admite '
                                'una nueva petición hasta después de dos '
                                'años.',
                                'Tras la revocatoria, asume el cargo quien '
                                'alcanzó el siguiente lugar en votos de la '
                                'misma lista.']}],
  'qr_reto': [{'pregunta': 'Según la Ley 26300, los ciudadanos pueden '
                           'participar mediante referéndum, iniciativa '
                           'legislativa, remoción o:',
               'respuesta': 'Revocación de autoridades'},
              {'pregunta': 'John Locke sostuvo que debían convertirse en '
                           'derechos civiles protegidos por el Estado:',
               'respuesta': 'La vida, la libertad y la propiedad'},
              {'pregunta': 'Para que el referéndum sea válido, debe ser '
                           'aprobado por no menos del:',
               'respuesta': '30% del total de votantes'}],
  'qr_dato': 'Los derechos políticos posibilitan la toma de decisiones '
             'respecto del gobierno del Estado.'},
 {'num': 9,
  'titulo': 'Derechos Económicos, Sociales y Culturales',
  'secciones': [{'titulo': '9.1 CONCEPTO Y FUNDAMENTO',
                 'items': ['Los derechos económicos, sociales y culturales '
                           'incluyen el derecho a un nivel de vida adecuado, '
                           'a la alimentación, a la {vivienda} digna, a la '
                           'educación y a la {salud}.',
                           'El Protocolo Adicional a la Convención Americana '
                           'en esta materia se conoce como el Protocolo de '
                           '{San Salvador}.',
                           'Según Hakansson, estos derechos son el conjunto '
                           'de normas de rango constitucional con las que el '
                           'Estado ejerce su función {equilibradora} de las '
                           'desigualdades sociales.',
                           'La {dignidad} de la persona humana es el valor '
                           'básico que fundamenta todos los derechos '
                           'humanos.',
                           'Según Nogueira, la dignidad humana fundamenta '
                           'tanto los derechos civiles y políticos como los '
                           'derechos económicos, sociales y {culturales}.']},
                {'titulo': '9.2 EL DERECHO AL TRABAJO EN LA CONSTITUCIÓN',
                 'items': ['El artículo {22} de la Constitución establece '
                           'que el trabajo es un deber y un derecho, base '
                           'del bienestar {social}.',
                           'El artículo {23} de la Constitución señala que '
                           'el Estado protege especialmente a la madre, al '
                           'menor de edad y al {impedido} que trabajan.',
                           'Según el artículo 23, ninguna relación laboral '
                           'puede limitar el ejercicio de los derechos '
                           '{constitucionales} ni rebajar la dignidad del '
                           'trabajador.',
                           'El artículo {24} de la Constitución establece '
                           'que el trabajador tiene derecho a una '
                           'remuneración {equitativa} y suficiente.']},
                {'titulo': '9.3 EL DERECHO A LA SALUD EN LA CONSTITUCIÓN',
                 'items': ['El artículo {7}° de la Constitución establece '
                           'que todos tienen derecho a la protección de su '
                           '{salud}, la de su familia y la comunidad.',
                           'El artículo {9}° señala que el Estado determina '
                           'la política nacional de salud, en forma plural y '
                           '{descentralizadora}.',
                           'El artículo {11}° garantiza el libre acceso a '
                           'prestaciones de salud y {pensiones}, mediante '
                           'entidades públicas, privadas o mixtas.',
                           'Los cuatro aspectos que garantizan la salud son: '
                           '{disponibilidad}, accesibilidad, aceptabilidad y '
                           '{calidad}.']},
                {'titulo': '9.4 EL DERECHO A LA EDUCACIÓN EN LA CONSTITUCIÓN',
                 'items': ['El artículo {13}° establece que la educación '
                           'tiene como finalidad el desarrollo {integral} de '
                           'la persona humana.',
                           'El artículo {14}° señala que la formación ética '
                           'y cívica y la enseñanza de la Constitución son '
                           '{obligatorias} en todo el proceso educativo.',
                           'El artículo {15}° establece que el profesorado '
                           'en la enseñanza oficial es carrera {pública}.',
                           'El artículo {17}° establece que la educación '
                           'inicial, primaria y secundaria son '
                           '{obligatorias}, y gratuita en instituciones del '
                           'Estado.',
                           'El artículo {18}° establece que la educación '
                           'universitaria tiene como fines la formación '
                           'profesional, la difusión {cultural} y la '
                           'investigación.',
                           'Cada universidad es {autónoma} en su régimen '
                           'normativo, de gobierno, académico, '
                           'administrativo y {económico}.']},
                {'titulo': '9.5 EL PIDESC Y EL PROTOCOLO DE SAN SALVADOR',
                 'items': ['El {PIDESC} (Pacto Internacional de Derechos '
                           'Económicos, Sociales y Culturales) es un tratado '
                           'multilateral que reconoce estos {derechos} y sus '
                           'mecanismos de protección.',
                           'El PIDESC fue adoptado por la Asamblea General '
                           'de la ONU mediante la Resolución 2200A (XXI), el '
                           '{16} de diciembre de {1966}.',
                           'El PIDESC entró en vigor el {3} de enero de '
                           '{1976}.',
                           'El {Protocolo de San Salvador} entiende el '
                           'derecho a la salud como el disfrute del más alto '
                           'nivel de bienestar {físico}, mental y social.']}],
  'cuadros': [{'titulo': '9.2 ARTÍCULOS CONSTITUCIONALES SOBRE EL TRABAJO',
               'encabezados': ['Artículo', 'Contenido'],
               'filas': [['{22}', 'El trabajo es un deber y un {derecho}'],
                         ['{23}',
                          'Atención prioritaria del Estado; protección a la '
                          '{madre}, menor e impedido'],
                         ['{24}',
                          'Derecho a una remuneración {equitativa} y '
                          'suficiente']]}],
  'preguntas': [{'pregunta': 'Los derechos económicos, sociales y culturales '
                             'incluyen, entre otros, el derecho a:',
                 'alternativas': ['Solo la libertad de tránsito',
                                  'Solo la nacionalidad',
                                  'Solo la propiedad privada',
                                  'Solo el sufragio',
                                  'Un nivel de vida adecuado, alimentación y '
                                  'vivienda digna'],
                 'correcta': 'E'},
                {'pregunta': 'El Protocolo Adicional a la Convención '
                             'Americana en materia de derechos económicos, '
                             'sociales y culturales se conoce como:',
                 'alternativas': ['Protocolo de Roma',
                                  'Protocolo de Ginebra',
                                  'Protocolo de San Salvador',
                                  'Protocolo de Nueva York',
                                  'Protocolo de Lima'],
                 'correcta': 'C'},
                {'pregunta': 'Según Hakansson, estos derechos representan la '
                             'función del Estado de:',
                 'alternativas': ['Privatizar servicios',
                                  'Aumentar impuestos',
                                  'Limitar la educación',
                                  'Equilibrar las desigualdades sociales',
                                  'Reducir el gasto público'],
                 'correcta': 'D'},
                {'pregunta': 'El valor básico que fundamenta todos los '
                             'derechos humanos es:',
                 'alternativas': ['El poder político',
                                  'La dignidad de la persona humana',
                                  'La nacionalidad',
                                  'La riqueza',
                                  'La religión'],
                 'correcta': 'B'},
                {'pregunta': 'Según Nogueira, la dignidad humana fundamenta:',
                 'alternativas': ['Solo los derechos económicos',
                                  'Tanto los derechos civiles y políticos '
                                  'como los económicos, sociales y '
                                  'culturales',
                                  'Ningún derecho en particular',
                                  'Solo los derechos culturales',
                                  'Solo los derechos civiles'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 22 de la Constitución establece '
                             'que el trabajo es:',
                 'alternativas': ['Un deber y un derecho',
                                  'Solo un derecho opcional',
                                  'Solo una obligación',
                                  'Una actividad comercial',
                                  'Un privilegio'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 22, el trabajo es la base '
                             'de:',
                 'alternativas': ['La política monetaria',
                                  'El sistema bancario',
                                  'El comercio exterior',
                                  'El bienestar social',
                                  'La recaudación fiscal'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 23 de la Constitución protege '
                             'especialmente a:',
                 'alternativas': ['Solo a los empresarios',
                                  'Solo al Estado',
                                  'Solo a los sindicatos',
                                  'A los extranjeros exclusivamente',
                                  'A la madre, al menor de edad y al '
                                  'impedido que trabajan'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 23, ninguna relación laboral '
                             'puede:',
                 'alternativas': ['Limitar los derechos constitucionales ni '
                                  'rebajar la dignidad del trabajador',
                                  'Solicitar experiencia',
                                  'Fijar un sueldo',
                                  'Exigir puntualidad',
                                  'Establecer horarios'],
                 'correcta': 'A'},
                {'pregunta': 'Según la Constitución, nadie está obligado a '
                             'prestar trabajo:',
                 'alternativas': ['Sin retribución o sin su libre '
                                  'consentimiento',
                                  'En el sector privado',
                                  'Para el Estado',
                                  'Los fines de semana',
                                  'Fuera de su ciudad'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 24 de la Constitución establece el '
                             'derecho del trabajador a:',
                 'alternativas': ['Vacaciones ilimitadas',
                                  'Ascenso automático',
                                  'Una remuneración equitativa y suficiente',
                                  'Doble sueldo',
                                  'Trabajo garantizado de por vida'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado promueve condiciones para el '
                             'progreso social y económico mediante:',
                 'alternativas': ['La eliminación de sindicatos',
                                  'La reducción del gasto en educación',
                                  'El cierre de empresas',
                                  'Políticas de fomento del empleo '
                                  'productivo y educación para el trabajo',
                                  'El aumento de impuestos únicamente'],
                 'correcta': 'D'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos, '
                             'en su preámbulo, señala que todo individuo y '
                             'órgano de la sociedad debe:',
                 'alternativas': ['Ignorar los derechos humanos',
                                  'Promover el respeto a los derechos '
                                  'humanos',
                                  'Limitar la participación ciudadana',
                                  'Depender del Estado',
                                  'Rechazar tratados internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos sociales y económicos buscan que '
                             'los ciudadanos gocen de:',
                 'alternativas': ['Solo riqueza material',
                                  'Ninguna prestación estatal',
                                  'Solo prestigio social',
                                  'Solo poder político',
                                  'Un estado de bienestar'],
                 'correcta': 'E'},
                {'pregunta': 'Según el texto, la persona, en virtud de su '
                             'dignidad, se convierte en:',
                 'alternativas': ['Un medio para el Estado',
                                  'Un obstáculo para el desarrollo',
                                  'Un sujeto pasivo sin derechos',
                                  'Un elemento secundario',
                                  'El fin del Estado'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado, según Nogueira, está al servicio '
                             'de:',
                 'alternativas': ['Las empresas privadas',
                                  'Los organismos internacionales',
                                  'La persona humana',
                                  'Solo el gobierno de turno',
                                  'El mercado'],
                 'correcta': 'C'},
                {'pregunta': 'La finalidad del Estado, según el texto, es '
                             'promover:',
                 'alternativas': ['El crecimiento demográfico',
                                  'Solo la recaudación fiscal',
                                  'El comercio exterior únicamente',
                                  'El bien común',
                                  'La expansión territorial'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los instrumentos con jerarquía '
                             'constitucional que contemplan estos derechos '
                             'figura:',
                 'alternativas': ['Solo el Código Civil',
                                  'Solo el Código Penal',
                                  'Ninguno en particular',
                                  'La Declaración Universal de Derechos '
                                  'Humanos',
                                  'Solo la Constitución peruana'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de dignidad humana implica que '
                             'los derechos se reconozcan:',
                 'alternativas': ['Solo a los trabajadores formales',
                                  'Solo a ciertos grupos',
                                  'Solo a los adultos',
                                  'Solo a los ciudadanos con recursos',
                                  'Sin distingo de tipo cultural, económico '
                                  'o social'],
                 'correcta': 'E'},
                {'pregunta': 'Los derechos sociales y económicos '
                             'representan, según el texto:',
                 'alternativas': ['Privilegios de unos pocos',
                                  'Una carga innecesaria',
                                  'Los fines sociales del Estado',
                                  'Normas sin aplicación práctica',
                                  'Obligaciones exclusivas del ciudadano'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 7° de la Constitución establece '
                             'que todos tienen derecho a la protección de:',
                 'alternativas': ['Su honor exclusivo',
                                  'Su intimidad exclusiva',
                                  'Su patrimonio',
                                  'Su libertad exclusiva',
                                  'Su salud'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 9° de la Constitución señala que '
                             'el Estado determina la política nacional de:',
                 'alternativas': ['Seguridad',
                                  'Salud',
                                  'Vivienda',
                                  'Trabajo',
                                  'Educación'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 11° de la Constitución garantiza '
                             'el libre acceso a prestaciones de salud y:',
                 'alternativas': ['Vacaciones pagadas',
                                  'Vivienda',
                                  'Educación gratuita',
                                  'Empleo garantizado',
                                  'Pensiones'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los cuatro aspectos que garantizan la '
                             'salud según la Constitución están '
                             'disponibilidad, accesibilidad, aceptabilidad '
                             'y:',
                 'alternativas': ['Anonimato',
                                  'Rapidez',
                                  'Exclusividad',
                                  'Calidad',
                                  'Gratuidad total'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 13° de la Constitución establece '
                             'que la educación tiene como finalidad el '
                             'desarrollo:',
                 'alternativas': ['Exclusivamente profesional',
                                  'Económico del país',
                                  'Solo intelectual',
                                  'Militar de la nación',
                                  'Integral de la persona humana'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 14° establece que la enseñanza de '
                             'la Constitución y los derechos humanos es:',
                 'alternativas': ['Opcional',
                                  'Solo para universidades',
                                  'Prohibida en colegios religiosos',
                                  'Obligatoria en todo el proceso educativo',
                                  'Solo para educación militar'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 15° de la Constitución establece '
                             'que el profesorado en la enseñanza oficial es:',
                 'alternativas': ['Trabajo temporal',
                                  'Cargo de confianza',
                                  'Función privada',
                                  'Carrera pública',
                                  'Servicio voluntario'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 17° establece que la educación '
                             'inicial, primaria y secundaria son:',
                 'alternativas': ['Solo para quienes puedan pagarlas',
                                  'Exclusivas del sector privado',
                                  'Opcionales',
                                  'Obligatorias',
                                  'Solo secundarias'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 18° establece que la educación '
                             'universitaria tiene como fines la formación '
                             'profesional, la difusión cultural, la creación '
                             'intelectual y:',
                 'alternativas': ['La investigación científica y tecnológica',
                                  'La política partidaria',
                                  'El comercio exterior',
                                  'La religión oficial',
                                  'El deporte exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Cada universidad, según la Constitución, es '
                             'autónoma en su régimen normativo, de gobierno, '
                             'académico, administrativo y:',
                 'alternativas': ['Diplomático',
                                  'Militar',
                                  'Judicial',
                                  'Religioso',
                                  'Económico'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDESC (Pacto Internacional de Derechos '
                             'Económicos, Sociales y Culturales) fue '
                             'adoptado por la Asamblea General de la ONU en:',
                 'alternativas': ['1966', '1993', '1976', '1948', '1989'],
                 'correcta': 'A'},
                {'pregunta': 'El PIDESC entró en vigor el 3 de enero de:',
                 'alternativas': ['1966', '1989', '1948', '1993', '1976'],
                 'correcta': 'E'},
                {'pregunta': 'El Protocolo de San Salvador entiende el '
                             'derecho a la salud como el disfrute del más '
                             'alto nivel de bienestar físico, mental y:',
                 'alternativas': ['Social',
                                  'Espiritual',
                                  'Económico',
                                  'Político',
                                  'Religioso'],
                 'correcta': 'A'},
                {'pregunta': 'El Pacto Internacional de los Derechos '
                             'Económicos, Sociales y Culturales se aprobó en '
                             'la asamblea general de: (II CEPRU 2025-I)',
                 'alternativas': ['La OEA',
                                  'La CAN',
                                  'La ONU',
                                  'La OTAN',
                                  'El CEPAL'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho que viene a ser la base del '
                             'bienestar social y un medio de realización de '
                             'la persona es el derecho al: (II CEPRU '
                             '2023-II)',
                 'alternativas': ['Educación',
                                  'Trabajo',
                                  'Salud',
                                  'Bienestar',
                                  'Patrimonio'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho mediante el cual se combate y '
                             'sanciona el tráfico ilícito de drogas es el '
                             'derecho a la: (II CEPRU 2023-II)',
                 'alternativas': ['Salud',
                                  'Trabajo',
                                  'Educación',
                                  'Medio Ambiente',
                                  'Paz'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho que constituye la base del '
                             'bienestar social y un medio de realización de '
                             'la persona es: (II CEPRU 2022-II)',
                 'alternativas': ['La educación',
                                  'La salud',
                                  'El trabajo',
                                  'La cultura',
                                  'El conocimiento'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y FUNDAMENTO',
                      'items': ['Los derechos económicos, sociales y '
                                'culturales incluyen el derecho a un nivel '
                                'de vida adecuado, a la alimentación, a la '
                                'vivienda digna, a la educación y a la '
                                'salud.',
                                'El Protocolo Adicional a la Convención '
                                'Americana en esta materia se conoce como el '
                                'Protocolo de San Salvador.',
                                'Según Hakansson, estos derechos son el '
                                'conjunto de normas de rango constitucional '
                                'con las que el Estado ejerce su función '
                                'equilibradora de las desigualdades '
                                'sociales.',
                                'La dignidad de la persona humana es el '
                                'valor básico que fundamenta todos los '
                                'derechos humanos.',
                                'Según Nogueira, la dignidad humana '
                                'fundamenta tanto los derechos civiles y '
                                'políticos como los derechos económicos, '
                                'sociales y culturales.']},
                     {'titulo': 'EL DERECHO AL TRABAJO EN LA CONSTITUCIÓN',
                      'items': ['El artículo 22 de la Constitución establece '
                                'que el trabajo es un deber y un derecho, '
                                'base del bienestar social.',
                                'El artículo 23 de la Constitución señala '
                                'que el Estado protege especialmente a la '
                                'madre, al menor de edad y al impedido que '
                                'trabajan.',
                                'Según el artículo 23, ninguna relación '
                                'laboral puede limitar el ejercicio de los '
                                'derechos constitucionales ni rebajar la '
                                'dignidad del trabajador.',
                                'El artículo 24 de la Constitución establece '
                                'que el trabajador tiene derecho a una '
                                'remuneración equitativa y suficiente.']},
                     {'titulo': 'EL DERECHO A LA SALUD EN LA CONSTITUCIÓN',
                      'items': ['El artículo 7° de la Constitución establece '
                                'que todos tienen derecho a la protección de '
                                'su salud, la de su familia y la comunidad.',
                                'El artículo 9° señala que el Estado '
                                'determina la política nacional de salud, en '
                                'forma plural y descentralizadora.',
                                'El artículo 11° garantiza el libre acceso a '
                                'prestaciones de salud y pensiones, mediante '
                                'entidades públicas, privadas o mixtas.',
                                'Los cuatro aspectos que garantizan la salud '
                                'son: disponibilidad, accesibilidad, '
                                'aceptabilidad y calidad.']},
                     {'titulo': 'EL DERECHO A LA EDUCACIÓN EN LA '
                                'CONSTITUCIÓN',
                      'items': ['El artículo 13° establece que la educación '
                                'tiene como finalidad el desarrollo integral '
                                'de la persona humana.',
                                'El artículo 14° señala que la formación '
                                'ética y cívica y la enseñanza de la '
                                'Constitución son obligatorias en todo el '
                                'proceso educativo.',
                                'El artículo 15° establece que el '
                                'profesorado en la enseñanza oficial es '
                                'carrera pública.',
                                'El artículo 17° establece que la educación '
                                'inicial, primaria y secundaria son '
                                'obligatorias, y gratuita en instituciones '
                                'del Estado.',
                                'El artículo 18° establece que la educación '
                                'universitaria tiene como fines la formación '
                                'profesional, la difusión cultural y la '
                                'investigación.',
                                'Cada universidad es autónoma en su régimen '
                                'normativo, de gobierno, académico, '
                                'administrativo y económico.']},
                     {'titulo': 'EL PIDESC Y EL PROTOCOLO DE SAN SALVADOR',
                      'items': ['El PIDESC (Pacto Internacional de Derechos '
                                'Económicos, Sociales y Culturales) es un '
                                'tratado multilateral que reconoce estos '
                                'derechos y sus mecanismos de protección.',
                                'El PIDESC fue adoptado por la Asamblea '
                                'General de la ONU mediante la Resolución '
                                '2200A (XXI), el 16 de diciembre de 1966.',
                                'El PIDESC entró en vigor el 3 de enero de '
                                '1976.',
                                'El Protocolo de San Salvador entiende el '
                                'derecho a la salud como el disfrute del más '
                                'alto nivel de bienestar físico, mental y '
                                'social.']}],
  'qr_reto': [{'pregunta': 'El artículo 17° establece que la educación '
                           'inicial, primaria y secundaria son:',
               'respuesta': 'Obligatorias'},
              {'pregunta': 'El derecho que constituye la base del bienestar '
                           'social y un medio de realización de la persona '
                           'es:',
               'respuesta': 'El trabajo'},
              {'pregunta': 'El Estado, según Nogueira, está al servicio de:',
               'respuesta': 'La persona humana'}],
  'qr_dato': 'El PIDESC entró en vigor el 3 de enero de 1976.'},
 {'num': 10,
  'titulo': 'Poder Legislativo',
  'secciones': [{'titulo': '10.1 CONCEPTO Y ÓRGANO',
                 'items': ['El Poder Legislativo es la facultad del Estado '
                           'para {dictar}, modificar, interpretar y derogar '
                           'leyes.',
                           'El {Parlamento} es el órgano que ejerce la '
                           'potestad legislativa, órgano de control del '
                           'gobierno y entidad representativa de la '
                           '{Nación}.',
                           'Según el artículo {91} de la Constitución, el '
                           'Poder Legislativo reside en el {Congreso}.',
                           'El Poder Legislativo y el Congreso son '
                           'categorías conceptuales {distintas}: existen '
                           'otras instituciones autónomas que también '
                           'ejercen función legislativa.']},
                {'titulo': '10.2 OTRAS INSTITUCIONES CON FACULTAD '
                           'LEGISLATIVA',
                 'items': ['El Presidente de la República puede expedir '
                           'Decretos de {Urgencia} y Decretos '
                           '{Legislativos}.',
                           'En regímenes de facto, se gobierna mediante '
                           'Decretos {Ley}.',
                           'Los Gobiernos Regionales expiden normas con '
                           'rango de ley llamadas normas {generales}.',
                           'Los Gobiernos Locales expiden normas con rango '
                           'de ley llamadas {Ordenanzas} Municipales.']},
                {'titulo': '10.3 LA FUNCIÓN LEGISLATIVA Y SUS FASES',
                 'items': ['El artículo {102} de la Constitución establece '
                           'que dar leyes es atribución del {Congreso}.',
                           'La fase {introductoria} corresponde a la '
                           'iniciativa para proponer un proyecto de ley.',
                           'La «iniciativa {popular}» en el Perú requiere '
                           'representar el {0,3}% de la población electoral.',
                           'La fase {constitutiva} corresponde a la '
                           'deliberación y aprobación de la ley por el '
                           'Congreso.',
                           'Según el artículo {105}, todo proyecto de ley '
                           'debe ser previamente dictaminado por una '
                           'comisión.',
                           'Las leyes ordinarias se aprueban por mayoría '
                           '{simple}; las leyes orgánicas requieren el voto '
                           'de más de la mitad del número legal de '
                           '{congresistas}.',
                           'La {promulgación} es el acto por el cual el '
                           'Presidente de la República rubrica la ley y '
                           'ordena su publicación.']},
                {'titulo': '10.4 LA FUNCIÓN REPRESENTATIVA Y COMPOSICIÓN DEL '
                           'CONGRESO',
                 'items': ['Mediante la {función representativa}, los '
                           'congresistas son los voceros de los ciudadanos, '
                           'canalizando sus {demandas}.',
                           'El Congreso está integrado por {130} '
                           'parlamentarios, elegidos por sufragio directo, '
                           'por un periodo de {5} años.',
                           'Los congresistas no pueden ser reelegidos de '
                           'manera {inmediata} para un nuevo periodo en el '
                           'mismo cargo.',
                           'El Congreso peruano consta de cámara única, es '
                           'decir, es {unicameral}.',
                           'Solo la Constitución de {1826} reconoció un '
                           'parlamento tricameral, con tribunos, censores y '
                           '{senadores}.',
                           'Una ventaja del sistema unicameral es la '
                           '{celeridad} en la aprobación de normas; una '
                           'desventaja es la fácil {sumisión} al Poder '
                           'Ejecutivo.']},
                {'titulo': '10.5 ÓRGANOS DEL PODER LEGISLATIVO',
                 'items': ['El {Pleno} del Congreso es la máxima asamblea '
                           'deliberativa, integrada por todos los '
                           '{congresistas}.',
                           'La {Mesa Directiva} tiene a cargo la dirección '
                           'administrativa del Congreso; está compuesta por '
                           'el Presidente y tres {Vicepresidentes}.',
                           'Las {Comisiones Ordinarias} se encargan del '
                           'estudio y dictamen de asuntos {ordinarios}.',
                           'La {Comisión Permanente} se instala dentro de '
                           'los 15 días útiles posteriores a la instalación '
                           'del periodo de sesiones, y no excede el {25}% de '
                           'congresistas.',
                           'Los {Grupos Parlamentarios} son conjuntos de '
                           'congresistas que comparten ideas o intereses '
                           '{afines}.']},
                {'titulo': '10.6 ATRIBUCIONES DEL CONGRESO Y FUNCIÓN DEL '
                           'CARGO',
                 'items': ['El Congreso tiene, además de la legislativa, '
                           'función {fiscalizadora} y función '
                           '{representativa}.',
                           'Mediante la función {fiscalizadora}, el Congreso '
                           'puede iniciar investigaciones sobre cualquier '
                           'asunto de interés {público}.',
                           'En la formación de la orientación política '
                           'general, el Congreso aprueba tratados '
                           'internacionales y declara la {guerra} y la paz.',
                           'En la gestión financiera, el Congreso aprueba el '
                           '{Presupuesto} de la República y la Cuenta '
                           '{General}.',
                           'El Congreso designa a los magistrados del '
                           'Tribunal Constitucional, al {Defensor del '
                           'Pueblo}, y a directores del BCR.',
                           'La función de {congresista} es de tiempo '
                           'completo; le está prohibido ejercer otra '
                           'profesión durante las horas de {funcionamiento}.',
                           'El mandato del congresista es {incompatible} con '
                           'otra función pública, excepto la de Ministro de '
                           '{Estado}.']}],
  'cuadros': [{'titulo': '10.3 FASES DE LA FUNCIÓN LEGISLATIVA',
               'encabezados': ['Fase', 'Contenido'],
               'filas': [['{Introductoria}',
                          'Iniciativa para proponer el proyecto de {ley}'],
                         ['{Constitutiva}',
                          '{Deliberación} y aprobación por el Congreso'],
                         ['{Integradora}',
                          '{Promulgación} por el Presidente']]}],
  'preguntas': [{'pregunta': 'El Poder Legislativo se define como la '
                             'facultad del Estado para:',
                 'alternativas': ['Dictar, modificar, interpretar y derogar '
                                  'leyes',
                                  'Ejecutar el presupuesto',
                                  'Nombrar ministros',
                                  'Administrar justicia',
                                  'Firmar tratados exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El órgano que ejerce la potestad legislativa '
                             'se denomina:',
                 'alternativas': ['Jurado Electoral',
                                  'Tribunal Constitucional',
                                  'Poder Judicial',
                                  'Parlamento',
                                  'Poder Ejecutivo'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 91 de la Constitución, el '
                             'Poder Legislativo reside en:',
                 'alternativas': ['El Congreso',
                                  'El Poder Judicial',
                                  'El Presidente',
                                  'Los gobiernos regionales',
                                  'El Tribunal Constitucional'],
                 'correcta': 'A'},
                {'pregunta': 'Poder Legislativo y Congreso de la República '
                             'son, conceptualmente:',
                 'alternativas': ['Sinónimos absolutos',
                                  'Idénticos en toda circunstancia',
                                  'Términos intercambiables sin matices',
                                  'Exactamente lo mismo',
                                  'Categorías conceptuales distintas'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente de la República puede expedir '
                             'normas con rango de ley llamadas:',
                 'alternativas': ['Ordenanzas municipales',
                                  'Circulares',
                                  'Directivas internas',
                                  'Resoluciones administrativas',
                                  'Decretos de Urgencia y Decretos '
                                  'Legislativos'],
                 'correcta': 'E'},
                {'pregunta': 'En regímenes de facto, se gobierna mediante:',
                 'alternativas': ['Directivas',
                                  'Decretos Supremos',
                                  'Resoluciones Ministeriales',
                                  'Decretos Ley',
                                  'Ordenanzas'],
                 'correcta': 'D'},
                {'pregunta': 'Los Gobiernos Locales expiden normas con rango '
                             'de ley llamadas:',
                 'alternativas': ['Resoluciones Legislativas',
                                  'Decretos de Urgencia',
                                  'Ordenanzas Municipales',
                                  'Normas generales',
                                  'Decretos Legislativos'],
                 'correcta': 'C'},
                {'pregunta': 'Los Gobiernos Regionales expiden normas con '
                             'rango de ley denominadas:',
                 'alternativas': ['Resoluciones Ministeriales',
                                  'Decretos Ley',
                                  'Normas generales',
                                  'Ordenanzas Municipales',
                                  'Decretos Supremos'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 102 de la Constitución establece '
                             'que dar leyes es atribución de:',
                 'alternativas': ['El Congreso',
                                  'La Defensoría del Pueblo',
                                  'El Poder Ejecutivo',
                                  'El Tribunal Constitucional',
                                  'El Poder Judicial'],
                 'correcta': 'A'},
                {'pregunta': 'La fase introductoria del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['El veto presidencial',
                                  'La iniciativa para proponer un proyecto '
                                  'de ley',
                                  'La publicación en el diario oficial',
                                  'La votación final',
                                  'La promulgación de la ley'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa popular en el Perú requiere '
                             'representar de la población electoral:',
                 'alternativas': ['10%', '3%', '30%', '1%', '0,3%'],
                 'correcta': 'E'},
                {'pregunta': 'La fase constitutiva del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La publicación oficial',
                                  'La iniciativa del proyecto',
                                  'La deliberación y aprobación de la ley '
                                  'por el Congreso',
                                  'La promulgación',
                                  'El archivo del proyecto'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 105, todo proyecto de ley '
                             'debe ser previamente:',
                 'alternativas': ['Aprobado por el Poder Judicial',
                                  'Consultado con el pueblo',
                                  'Publicado en un diario',
                                  'Traducido a lenguas originarias',
                                  'Dictaminado por una comisión'],
                 'correcta': 'E'},
                {'pregunta': 'Las leyes ordinarias en el Congreso se '
                             'aprueban por:',
                 'alternativas': ['Mayoría calificada',
                                  'Unanimidad',
                                  'Dos tercios',
                                  'Mayoría simple',
                                  'Consenso obligatorio'],
                 'correcta': 'D'},
                {'pregunta': 'Las leyes orgánicas requieren el voto de:',
                 'alternativas': ['Solo la mesa directiva',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'La mayoría relativa',
                                  'Todos los congresistas',
                                  'Un tercio de los congresistas'],
                 'correcta': 'B'},
                {'pregunta': 'La promulgación de la ley es realizada por:',
                 'alternativas': ['El Poder Judicial',
                                  'El presidente del Congreso',
                                  'El Tribunal Constitucional',
                                  'El Presidente de la República',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'D'},
                {'pregunta': 'La promulgación consiste en que el Jefe de '
                             'Estado:',
                 'alternativas': ['Rubrique la ley y ordene su publicación',
                                  'Vote la ley',
                                  'Elabore el proyecto',
                                  'Redacte la ley',
                                  'Modifique el texto legal'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 108, la ley aprobada se '
                             'envía al Presidente para:',
                 'alternativas': ['Su traducción',
                                  'Su anulación',
                                  'Su archivo',
                                  'Su revisión judicial',
                                  'Su promulgación'],
                 'correcta': 'E'},
                {'pregunta': 'Las leyes de reforma constitucional se sujetan '
                             'al procedimiento del artículo:',
                 'alternativas': ['206', '91', '102', '105', '108'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho de iniciativa legislativa, además '
                             'del Legislativo y Ejecutivo, se otorga también '
                             'a:',
                 'alternativas': ['Solo a los partidos políticos',
                                  'Solo al sector privado',
                                  'Solo a las universidades',
                                  'Solo a organismos internacionales',
                                  'El Poder Judicial, gobiernos regionales, '
                                  'locales y colegios profesionales'],
                 'correcta': 'E'},
                {'pregunta': 'Mediante la función representativa, los '
                             'congresistas actúan como voceros de:',
                 'alternativas': ['El Poder Judicial',
                                  'El Poder Ejecutivo',
                                  'Las Fuerzas Armadas',
                                  'Los ciudadanos',
                                  'Los organismos internacionales'],
                 'correcta': 'D'},
                {'pregunta': 'El Congreso de la República está integrado por '
                             'un número de parlamentarios igual a:',
                 'alternativas': ['100', '130', '150', '110', '120'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo del mandato congresal en el Perú es '
                             'de:',
                 'alternativas': ['4 años',
                                  '6 años',
                                  '7 años',
                                  '5 años',
                                  '3 años'],
                 'correcta': 'D'},
                {'pregunta': 'Los congresistas no pueden ser reelegidos de '
                             'manera inmediata para:',
                 'alternativas': ['Ningún cargo público',
                                  'Cargos municipales',
                                  'Ministerios',
                                  'Cargos regionales',
                                  'Un nuevo periodo en el mismo cargo'],
                 'correcta': 'E'},
                {'pregunta': 'El Congreso peruano actual tiene cámara única, '
                             'es decir, es de tipo:',
                 'alternativas': ['Regional',
                                  'Bicameral',
                                  'Tricameral',
                                  'Unicameral',
                                  'Mixto'],
                 'correcta': 'D'},
                {'pregunta': 'La única Constitución peruana que reconoció un '
                             'parlamento tricameral fue la de:',
                 'alternativas': ['1860', '1826', '1920', '1839', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las ventajas del sistema unicameral está '
                             'la celeridad en la aprobación de:',
                 'alternativas': ['Normas legales',
                                  'Tratados exclusivamente',
                                  'Presupuestos exclusivamente',
                                  'Nombramientos',
                                  'Impuestos exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las desventajas del sistema unicameral '
                             'está la fácil sumisión del Congreso al:',
                 'alternativas': ['Poder Judicial',
                                  'Poder Ejecutivo',
                                  'Jurado Nacional de Elecciones',
                                  'Ministerio Público',
                                  'Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima asamblea deliberativa del Congreso, '
                             'integrada por todos los congresistas, se '
                             'llama:',
                 'alternativas': ['Comisión Permanente',
                                  'Consejo Directivo',
                                  'Junta de Portavoces',
                                  'El Pleno',
                                  'Mesa Directiva'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano que tiene a cargo la dirección '
                             'administrativa del Congreso se llama:',
                 'alternativas': ['El Pleno',
                                  'La Comisión Permanente',
                                  'La Junta de Portavoces',
                                  'Los Grupos Parlamentarios',
                                  'La Mesa Directiva'],
                 'correcta': 'E'},
                {'pregunta': 'La Mesa Directiva está compuesta por el '
                             'Presidente y un número de Vicepresidentes '
                             'igual a:',
                 'alternativas': ['Tres', 'Dos', 'Uno', 'Cinco', 'Cuatro'],
                 'correcta': 'A'},
                {'pregunta': 'El órgano encargado del estudio y dictamen de '
                             'asuntos ordinarios se llama:',
                 'alternativas': ['Consejo Directivo',
                                  'Ligas Parlamentarias',
                                  'Comisión Permanente',
                                  'Comisiones Ordinarias',
                                  'Junta de Portavoces'],
                 'correcta': 'D'},
                {'pregunta': 'La Comisión Permanente no puede exceder de un '
                             'porcentaje del total de congresistas igual a:',
                 'alternativas': ['30%', '15%', '50%', '25%', '10%'],
                 'correcta': 'D'},
                {'pregunta': 'Los conjuntos de congresistas que comparten '
                             'ideas o intereses afines se llaman:',
                 'alternativas': ['Consejo Directivo',
                                  'Mesa Directiva',
                                  'Ligas Parlamentarias',
                                  'Grupos Parlamentarios',
                                  'Comisiones Ordinarias'],
                 'correcta': 'D'},
                {'pregunta': 'Además de la función legislativa, el Congreso '
                             'tiene función fiscalizadora y:',
                 'alternativas': ['Notarial',
                                  'Representativa',
                                  'Ejecutiva',
                                  'Judicial',
                                  'Electoral'],
                 'correcta': 'B'},
                {'pregunta': 'Mediante la función fiscalizadora, el Congreso '
                             'puede iniciar investigaciones sobre asuntos de '
                             'interés:',
                 'alternativas': ['Militar exclusivo',
                                  'Público',
                                  'Religioso',
                                  'Comercial exclusivo',
                                  'Privado exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las atribuciones del Congreso en la '
                             'formación de la orientación política general '
                             'está aprobar tratados internacionales y '
                             'declarar:',
                 'alternativas': ['Elecciones',
                                  'Impuestos',
                                  'Feriados nacionales',
                                  'La guerra y la paz',
                                  'El presupuesto exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'En la gestión financiera, el Congreso aprueba '
                             'el Presupuesto de la República y:',
                 'alternativas': ['La Cuenta General',
                                  'Solo el tipo de cambio',
                                  'Solo las tarifas públicas',
                                  'Solo el gasto militar',
                                  'Solo los impuestos municipales'],
                 'correcta': 'A'},
                {'pregunta': 'El Congreso designa, entre otros altos '
                             'funcionarios, a los magistrados del Tribunal '
                             'Constitucional y al:',
                 'alternativas': ['Presidente de la República',
                                  'Fiscal de la Nación exclusivo',
                                  'Alcalde de Lima',
                                  'Presidente del Poder Judicial exclusivo',
                                  'Defensor del Pueblo'],
                 'correcta': 'E'},
                {'pregunta': 'La función de congresista es de tiempo '
                             'completo; le está prohibido ejercer otra '
                             'profesión durante:',
                 'alternativas': ['Las horas de funcionamiento del Congreso',
                                  'Los feriados',
                                  'Ningún momento, puede ejercer libremente',
                                  'Las vacaciones',
                                  'Los fines de semana'],
                 'correcta': 'A'},
                {'pregunta': 'El mandato del congresista es incompatible con '
                             'el ejercicio de cualquier otra función '
                             'pública, excepto la de:',
                 'alternativas': ['Fiscal',
                                  'Ministro de Estado',
                                  'Gobernador Regional',
                                  'Juez',
                                  'Alcalde'],
                 'correcta': 'B'},
                {'pregunta': 'La Cuenta General de la República, como '
                             'documento oficial, es aprobada por: (II CEPRU '
                             '2025-I)',
                 'alternativas': ['El Consejo de Ministros',
                                  'El Congreso de la República',
                                  'El Ministerio de Economía y Finanzas',
                                  'La Contraloría General de la República',
                                  'La Comisión de Presupuesto'],
                 'correcta': 'B'},
                {'pregunta': 'Es una atribución del Congreso: (III CEPRU '
                             '2025-I)',
                 'alternativas': ['Cumplir y hacer cumplir la Constitución, '
                                  'los tratados, leyes y demás disposiciones '
                                  'legales',
                                  'Dirigir la política general del Gobierno',
                                  'Administrar la hacienda pública',
                                  'Autorizar los empréstitos',
                                  'Emitir los Decretos Legislativos y de '
                                  'Urgencia'],
                 'correcta': 'D'},
                {'pregunta': 'Es un requisito para ser congresista: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Terminar el 5to de secundaria',
                                  'Tener estudios universitarios',
                                  'Tener primaria completa',
                                  'Ser varón',
                                  'Ser peruano de nacimiento'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ÓRGANO',
                      'items': ['El Poder Legislativo es la facultad del '
                                'Estado para dictar, modificar, interpretar '
                                'y derogar leyes.',
                                'El Parlamento es el órgano que ejerce la '
                                'potestad legislativa, órgano de control del '
                                'gobierno y entidad representativa de la '
                                'Nación.',
                                'Según el artículo 91 de la Constitución, el '
                                'Poder Legislativo reside en el Congreso.',
                                'El Poder Legislativo y el Congreso son '
                                'categorías conceptuales distintas: existen '
                                'otras instituciones autónomas que también '
                                'ejercen función legislativa.']},
                     {'titulo': 'OTRAS INSTITUCIONES CON FACULTAD '
                                'LEGISLATIVA',
                      'items': ['El Presidente de la República puede expedir '
                                'Decretos de Urgencia y Decretos '
                                'Legislativos.',
                                'En regímenes de facto, se gobierna mediante '
                                'Decretos Ley.',
                                'Los Gobiernos Regionales expiden normas con '
                                'rango de ley llamadas normas generales.',
                                'Los Gobiernos Locales expiden normas con '
                                'rango de ley llamadas Ordenanzas '
                                'Municipales.']},
                     {'titulo': 'LA FUNCIÓN LEGISLATIVA Y SUS FASES',
                      'items': ['El artículo 102 de la Constitución '
                                'establece que dar leyes es atribución del '
                                'Congreso.',
                                'La fase introductoria corresponde a la '
                                'iniciativa para proponer un proyecto de '
                                'ley.',
                                'La «iniciativa popular» en el Perú requiere '
                                'representar el 0,3% de la población '
                                'electoral.',
                                'La fase constitutiva corresponde a la '
                                'deliberación y aprobación de la ley por el '
                                'Congreso.',
                                'Según el artículo 105, todo proyecto de ley '
                                'debe ser previamente dictaminado por una '
                                'comisión.',
                                'Las leyes ordinarias se aprueban por '
                                'mayoría simple; las leyes orgánicas '
                                'requieren el voto de más de la mitad del '
                                'número legal de congresistas.',
                                'La promulgación es el acto por el cual el '
                                'Presidente de la República rubrica la ley y '
                                'ordena su publicación.']},
                     {'titulo': 'LA FUNCIÓN REPRESENTATIVA Y COMPOSICIÓN DEL '
                                'CONGRESO',
                      'items': ['Mediante la función representativa, los '
                                'congresistas son los voceros de los '
                                'ciudadanos, canalizando sus demandas.',
                                'El Congreso está integrado por 130 '
                                'parlamentarios, elegidos por sufragio '
                                'directo, por un periodo de 5 años.',
                                'Los congresistas no pueden ser reelegidos '
                                'de manera inmediata para un nuevo periodo '
                                'en el mismo cargo.',
                                'El Congreso peruano consta de cámara única, '
                                'es decir, es unicameral.',
                                'Solo la Constitución de 1826 reconoció un '
                                'parlamento tricameral, con tribunos, '
                                'censores y senadores.',
                                'Una ventaja del sistema unicameral es la '
                                'celeridad en la aprobación de normas; una '
                                'desventaja es la fácil sumisión al Poder '
                                'Ejecutivo.']},
                     {'titulo': 'ÓRGANOS DEL PODER LEGISLATIVO',
                      'items': ['El Pleno del Congreso es la máxima asamblea '
                                'deliberativa, integrada por todos los '
                                'congresistas.',
                                'La Mesa Directiva tiene a cargo la '
                                'dirección administrativa del Congreso; está '
                                'compuesta por el Presidente y tres '
                                'Vicepresidentes.',
                                'Las Comisiones Ordinarias se encargan del '
                                'estudio y dictamen de asuntos ordinarios.',
                                'La Comisión Permanente se instala dentro de '
                                'los 15 días útiles posteriores a la '
                                'instalación del periodo de sesiones, y no '
                                'excede el 25% de congresistas.',
                                'Los Grupos Parlamentarios son conjuntos de '
                                'congresistas que comparten ideas o '
                                'intereses afines.']},
                     {'titulo': 'ATRIBUCIONES DEL CONGRESO Y FUNCIÓN DEL '
                                'CARGO',
                      'items': ['El Congreso tiene, además de la '
                                'legislativa, función fiscalizadora y '
                                'función representativa.',
                                'Mediante la función fiscalizadora, el '
                                'Congreso puede iniciar investigaciones '
                                'sobre cualquier asunto de interés público.',
                                'En la formación de la orientación política '
                                'general, el Congreso aprueba tratados '
                                'internacionales y declara la guerra y la '
                                'paz.',
                                'En la gestión financiera, el Congreso '
                                'aprueba el Presupuesto de la República y la '
                                'Cuenta General.',
                                'El Congreso designa a los magistrados del '
                                'Tribunal Constitucional, al Defensor del '
                                'Pueblo, y a directores del BCR.',
                                'La función de congresista es de tiempo '
                                'completo; le está prohibido ejercer otra '
                                'profesión durante las horas de '
                                'funcionamiento.',
                                'El mandato del congresista es incompatible '
                                'con otra función pública, excepto la de '
                                'Ministro de Estado.']}],
  'qr_reto': [{'pregunta': 'Mediante la función fiscalizadora, el Congreso '
                           'puede iniciar investigaciones sobre asuntos de '
                           'interés:',
               'respuesta': 'Público'},
              {'pregunta': 'El órgano que tiene a cargo la dirección '
                           'administrativa del Congreso se llama:',
               'respuesta': 'La Mesa Directiva'},
              {'pregunta': 'La función de congresista es de tiempo completo; '
                           'le está prohibido ejercer otra profesión '
                           'durante:',
               'respuesta': 'Las horas de funcionamiento del Congreso'}],
  'qr_dato': 'La función de congresista es de tiempo completo; le está '
             'prohibido ejercer otra profesión durante las horas de '
             'funcionamiento.'},
 {'num': 11,
  'titulo': 'El Poder Ejecutivo',
  'secciones': [{'titulo': '11.1 CONCEPTO Y ORGANIZACIÓN',
                 'items': ['El Poder Ejecutivo está constituido por el '
                           '{Presidente}, quien desarrolla las funciones de '
                           'Jefe de {Estado} y Jefe de Gobierno.',
                           'El Poder Ejecutivo es el órgano encargado de la '
                           '{administración} del Estado y de la ejecución de '
                           'las {leyes}.',
                           'Integran el Poder Ejecutivo el Presidente de la '
                           'República y el {Consejo de Ministros}.',
                           'En el sistema {presidencial}, los poderes '
                           'Ejecutivo, Legislativo y Judicial son autónomos '
                           'e independientes entre sí.']},
                {'titulo': '11.2 ELECCIÓN DEL PRESIDENTE',
                 'items': ['Para ser presidente se requiere ser peruano de '
                           '{nacimiento}, tener 35 años de edad como mínimo '
                           'y gozar del derecho de {sufragio}.',
                           'El presidente se elige por sufragio directo, '
                           'secreto y {universal}, para un mandato de {5} '
                           'años, sin reelección {inmediata}.',
                           'Para ganar en primera vuelta se requiere obtener '
                           'la {mayoría absoluta}, sin computar votos nulos '
                           'ni en blanco.',
                           'Si ningún candidato logra la mayoría absoluta, '
                           'se realiza una {segunda} elección entre los dos '
                           'candidatos con mayor votación.',
                           'Según el artículo {116} de la Constitución, el '
                           'Presidente jura y asume el cargo ante el '
                           'Congreso el {28} de julio del año de la '
                           'elección.']},
                {'titulo': '11.3 ATRIBUCIONES DEL PRESIDENTE',
                 'items': ['Entre las atribuciones del Presidente están '
                           'cumplir y hacer cumplir la {Constitución}, '
                           'representar al Estado y dirigir la política '
                           '{general} del Gobierno.',
                           'El Presidente puede convocar al Congreso a '
                           'legislatura {extraordinaria}, firmando el '
                           'decreto de convocatoria.',
                           'El Presidente dirige mensajes al Congreso, '
                           'obligatoriamente en forma personal y por '
                           'escrito, al instalarse la primera legislatura '
                           '{ordinaria} anual.',
                           'El Presidente tiene la potestad de {reglamentar} '
                           'las leyes sin transgredirlas, dictando decretos '
                           'y resoluciones.',
                           'El Presidente dirige la política {exterior} y '
                           'las relaciones internacionales, y celebra y '
                           'ratifica {tratados}.']},
                {'titulo': '11.4 VACANCIA Y SUSPENSIÓN DEL PRESIDENTE',
                 'items': ['La Presidencia vaca por muerte, {incapacidad} '
                           'moral o física declarada por el Congreso, '
                           'aceptación de renuncia, o {destitución}.',
                           'La Presidencia también vaca si el Presidente '
                           'sale del territorio nacional sin permiso del '
                           '{Congreso} o no regresa a tiempo.',
                           'El ejercicio de la Presidencia se {suspende} por '
                           'incapacidad temporal o por estar sometido a '
                           'proceso {judicial}.',
                           'Según el artículo {117}, el Presidente solo '
                           'puede ser acusado durante su periodo por '
                           'traición a la patria o por impedir {elecciones}.',
                           'Por impedimento del Presidente, asume el {Primer '
                           'Vicepresidente}; en su defecto, el Segundo; en '
                           'defecto de ambos, el Presidente del '
                           '{Congreso}.']},
                {'titulo': '11.5 EL CONSEJO DE MINISTROS',
                 'items': ['El {Consejo de Ministros} es el organismo del '
                           'Poder Ejecutivo constituido por la reunión de '
                           'los {ministros}.',
                           'Son {nulos} los actos del Presidente que carecen '
                           'de refrendación {ministerial}.',
                           'El Consejo está conformado por los ministros y '
                           'el {Presidente del Consejo de Ministros}, o '
                           'premier, quien puede tener cartera o no.',
                           'Para ser ministro se requiere ser peruano de '
                           'nacimiento, ciudadano en ejercicio, y tener {25} '
                           'años como mínimo.',
                           'Actualmente existen {18} ministerios en el Perú.',
                           'Entre las atribuciones del Consejo de Ministros '
                           'está aprobar los proyectos de ley que el '
                           'Presidente somete al {Congreso}.',
                           'Los ministros son {individualmente} responsables '
                           'por sus propios actos, y {solidariamente} '
                           'responsables por actos que refrendan en '
                           'conjunto.']},
                {'titulo': '11.6 INTERPELACIÓN Y DISOLUCIÓN DEL CONGRESO',
                 'items': ['La {interpelación} es la facultad de los '
                           'congresistas de requerir a los ministros que '
                           'informen sobre determinado asunto; se presenta '
                           'por escrito por no menos del {15}% de '
                           'congresistas.',
                           'El resultado de la interpelación puede ser un '
                           '{voto de confianza} o un voto de {censura}.',
                           'Toda moción de censura debe ser presentada por '
                           'no menos del {25}% del número legal de '
                           'congresistas.',
                           'La censura requiere el voto de más de la {mitad} '
                           'del número legal de miembros del Congreso.',
                           'El Presidente puede {disolver} el Congreso si '
                           'este ha censurado o negado su confianza a {dos} '
                           'Consejos de Ministros.',
                           'Las nuevas elecciones tras la disolución se '
                           'realizan dentro de los {cuatro} meses; no puede '
                           'disolverse en el último {año} de mandato ni en '
                           'estado de sitio.',
                           'Disuelto el Congreso, se mantiene en funciones '
                           'la {Comisión Permanente}, que no puede ser '
                           'disuelta.']},
                {'titulo': '11.7 REGÍMENES DE EXCEPCIÓN',
                 'items': ['El artículo {137} de la Constitución establece '
                           'dos regímenes de excepción: estado de '
                           '{emergencia} y estado de {sitio}.',
                           'Ambos son declarados por el Presidente mediante '
                           'decreto supremo, con acuerdo del Consejo de '
                           '{Ministros}.',
                           'El {hábeas corpus} y el {amparo} no se suspenden '
                           'durante los regímenes de excepción.',
                           'El {estado de emergencia} se declara por '
                           'perturbación de la paz, catástrofe, o graves '
                           'circunstancias; dura hasta {60} días.',
                           'Durante el estado de emergencia asumen el '
                           'control las {Fuerzas Armadas}, según disponga el '
                           'Presidente.',
                           'El {estado de sitio} se declara por invasión, '
                           'guerra exterior o guerra civil; dura hasta {45} '
                           'días.']}],
  'cuadros': [{'titulo': '11.2 REQUISITOS PARA SER PRESIDENTE',
               'encabezados': ['Requisito', 'Detalle'],
               'filas': [['{Nacionalidad}', 'Peruano de {nacimiento}'],
                         ['{Edad}', '35 años como {mínimo}'],
                         ['{Sufragio}', 'Gozar del derecho de voto']]}],
  'preguntas': [{'pregunta': 'El Poder Ejecutivo está constituido por el '
                             'Presidente, quien es Jefe de Estado y:',
                 'alternativas': ['Jefe del Poder Judicial',
                                  'Jefe militar exclusivamente',
                                  'Jefe de Gobierno',
                                  'Jefe del Congreso',
                                  'Jefe religioso'],
                 'correcta': 'C'},
                {'pregunta': 'El Poder Ejecutivo es el órgano encargado de:',
                 'alternativas': ['Fiscalizar al Congreso',
                                  'Organizar elecciones',
                                  'La administración del Estado y ejecución '
                                  'de las leyes',
                                  'Administrar justicia',
                                  'Dictar leyes exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Integran el Poder Ejecutivo el Presidente y:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'La Defensoría del Pueblo',
                                  'El Consejo de Ministros',
                                  'El Congreso',
                                  'El Poder Judicial'],
                 'correcta': 'C'},
                {'pregunta': 'En el sistema presidencial, los tres poderes '
                             'del Estado son:',
                 'alternativas': ['Dependientes entre sí',
                                  'Autónomos e independientes',
                                  'Fusionados en uno solo',
                                  'Elegidos por el Congreso',
                                  'Subordinados al Ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser presidente del Perú se requiere ser '
                             'peruano:',
                 'alternativas': ['Mayor de 50 años exclusivamente',
                                  'Residente',
                                  'Naturalizado',
                                  'Con doble nacionalidad',
                                  'De nacimiento'],
                 'correcta': 'E'},
                {'pregunta': 'La edad mínima para postular a la presidencia '
                             'es de:',
                 'alternativas': ['40 años',
                                  '30 años',
                                  '45 años',
                                  '25 años',
                                  '35 años'],
                 'correcta': 'E'},
                {'pregunta': 'El presidente de la República se elige por un '
                             'mandato de:',
                 'alternativas': ['6 años',
                                  '3 años',
                                  '4 años',
                                  '5 años',
                                  '7 años'],
                 'correcta': 'D'},
                {'pregunta': 'La reelección presidencial inmediata en el '
                             'Perú está:',
                 'alternativas': ['Sujeta a referéndum',
                                  'Permitida solo una vez',
                                  'Permitida sin restricciones',
                                  'Obligatoria',
                                  'No permitida'],
                 'correcta': 'E'},
                {'pregunta': 'Para ganar la presidencia en primera vuelta se '
                             'requiere:',
                 'alternativas': ['Un tercio de los votos',
                                  'Mayoría relativa',
                                  'Solo más votos que el segundo',
                                  'La mitad exacta de votos válidos',
                                  'Mayoría absoluta'],
                 'correcta': 'E'},
                {'pregunta': 'Si ningún candidato obtiene mayoría absoluta, '
                             'se realiza:',
                 'alternativas': ['Un sorteo',
                                  'Una tercera vuelta',
                                  'Una nueva convocatoria general',
                                  'Una decisión del Congreso',
                                  'Una segunda elección entre los dos más '
                                  'votados'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 116, el Presidente jura y '
                             'asume el cargo ante:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El pueblo directamente',
                                  'El Congreso',
                                  'El Poder Judicial',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'C'},
                {'pregunta': 'El Presidente asume el cargo el:',
                 'alternativas': ['28 de julio',
                                  '9 de diciembre',
                                  '1 de enero',
                                  '1 de mayo',
                                  '15 de agosto'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las atribuciones del Presidente figura '
                             'representar al Estado:',
                 'alternativas': ['Solo dentro del país',
                                  'Dentro y fuera de la República',
                                  'Solo en tratados comerciales',
                                  'Solo en organismos internacionales',
                                  'Solo ante el Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente puede convocar al Congreso a '
                             'legislatura:',
                 'alternativas': ['Extraordinaria',
                                  'Solo virtual',
                                  'Ninguna, esa función es del Congreso',
                                  'Permanente sin descanso',
                                  'Solo ordinaria'],
                 'correcta': 'A'},
                {'pregunta': 'El Presidente dirige mensajes obligatorios al '
                             'Congreso al instalarse la legislatura:',
                 'alternativas': ['Cada seis meses',
                                  'Extraordinaria únicamente',
                                  'Solo el último año de gobierno',
                                  'Ordinaria anual',
                                  'Nunca, esa función no le corresponde'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente reglamenta las leyes mediante:',
                 'alternativas': ['Sentencias judiciales',
                                  'Leyes orgánicas',
                                  'Resoluciones legislativas',
                                  'Decretos y resoluciones',
                                  'Ordenanzas municipales'],
                 'correcta': 'D'},
                {'pregunta': 'Al reglamentar las leyes, el Presidente no '
                             'puede:',
                 'alternativas': ['Emitir decretos',
                                  'Transgredirlas ni desnaturalizarlas',
                                  'Cumplirlas',
                                  'Publicarlas',
                                  'Ejecutarlas'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente dirige la política exterior y '
                             'puede:',
                 'alternativas': ['Elegir a los congresistas',
                                  'Declarar la guerra sin el Congreso',
                                  'Modificar la Constitución solo',
                                  'Celebrar y ratificar tratados',
                                  'Disolver el Poder Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'Junto con el Presidente se eligen, con los '
                             'mismos requisitos:',
                 'alternativas': ['Los ministros',
                                  'Los alcaldes',
                                  'Los gobernadores regionales',
                                  'Los congresistas',
                                  'Dos vicepresidentes'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente debe velar por el orden interno '
                             'y:',
                 'alternativas': ['La reforma agraria',
                                  'El sistema educativo',
                                  'La política monetaria',
                                  'La seguridad exterior de la República',
                                  'El comercio exterior'],
                 'correcta': 'D'},
                {'pregunta': 'La Presidencia de la República vaca por '
                             'muerte, incapacidad moral o física, aceptación '
                             'de renuncia o:',
                 'alternativas': ['Viaje autorizado',
                                  'Enfermedad leve',
                                  'Destitución',
                                  'Vacaciones prolongadas',
                                  'Ausencia de un día'],
                 'correcta': 'C'},
                {'pregunta': 'La Presidencia también vaca si el Presidente '
                             'sale del territorio nacional sin permiso de:',
                 'alternativas': ['El Poder Judicial',
                                  'El Consejo de Ministros exclusivo',
                                  'El Congreso',
                                  'La Contraloría',
                                  'El Tribunal Constitucional'],
                 'correcta': 'C'},
                {'pregunta': 'El ejercicio de la Presidencia se suspende por '
                             'incapacidad temporal o por estar sometido a '
                             'proceso:',
                 'alternativas': ['Judicial',
                                  'Administrativo',
                                  'Disciplinario menor',
                                  'Fiscal exclusivo',
                                  'Electoral exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 117, el Presidente solo '
                             'puede ser acusado durante su periodo por '
                             'traición a la patria o por impedir:',
                 'alternativas': ['La educación pública',
                                  'El turismo',
                                  'Las elecciones',
                                  'El comercio exterior',
                                  'Reformas económicas'],
                 'correcta': 'C'},
                {'pregunta': 'Por impedimento del Presidente, asume sus '
                             'funciones en primer lugar:',
                 'alternativas': ['El Premier',
                                  'El Presidente del Congreso',
                                  'El Presidente del Poder Judicial',
                                  'El Segundo Vicepresidente',
                                  'El Primer Vicepresidente'],
                 'correcta': 'E'},
                {'pregunta': 'El Consejo de Ministros es el organismo del '
                             'Poder Ejecutivo constituido por la reunión de:',
                 'alternativas': ['Los jueces supremos',
                                  'Los alcaldes',
                                  'Los congresistas',
                                  'Los ministros',
                                  'Los gobernadores regionales'],
                 'correcta': 'D'},
                {'pregunta': 'Son nulos los actos del Presidente que carecen '
                             'de:',
                 'alternativas': ['Refrendación ministerial',
                                  'Publicación inmediata',
                                  'Sello presidencial',
                                  'Aprobación popular',
                                  'Firma notarial'],
                 'correcta': 'A'},
                {'pregunta': 'El jefe del Consejo de Ministros, quien puede '
                             'tener cartera o no, se llama:',
                 'alternativas': ['Canciller',
                                  'Portavoz',
                                  'Premier o Presidente del Consejo de '
                                  'Ministros',
                                  'Secretario General',
                                  'Vicepresidente'],
                 'correcta': 'C'},
                {'pregunta': 'Para ser ministro se requiere ser peruano de '
                             'nacimiento, ciudadano en ejercicio, y tener '
                             'como mínimo:',
                 'alternativas': ['35 años',
                                  '25 años',
                                  '21 años',
                                  '30 años',
                                  '18 años'],
                 'correcta': 'B'},
                {'pregunta': 'Actualmente el Perú cuenta con un número de '
                             'ministerios igual a:',
                 'alternativas': ['20', '12', '16', '15', '18'],
                 'correcta': 'E'},
                {'pregunta': 'Los ministros son individualmente responsables '
                             'por sus propios actos, y solidariamente '
                             'responsables por actos que:',
                 'alternativas': ['Nunca comparten',
                                  'Refrendan en conjunto',
                                  'Publican en el diario oficial',
                                  'Delegan a terceros',
                                  'Ocultan al Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'La interpelación es la facultad de los '
                             'congresistas de requerir a los ministros que:',
                 'alternativas': ['Sean destituidos',
                                  'Renuncien inmediatamente',
                                  'Informen, aclaren o expliquen un asunto',
                                  'Paguen una multa',
                                  'Se retiren del país'],
                 'correcta': 'C'},
                {'pregunta': 'La interpelación debe presentarse por escrito '
                             'por no menos de un porcentaje de congresistas '
                             'igual a:',
                 'alternativas': ['15%', '30%', '25%', '5%', '10%'],
                 'correcta': 'A'},
                {'pregunta': 'El resultado de una interpelación puede ser un '
                             'voto de confianza o un voto de:',
                 'alternativas': ['Censura',
                                  'Reconocimiento',
                                  'Aplauso',
                                  'Abstención exclusiva',
                                  'Felicitación'],
                 'correcta': 'A'},
                {'pregunta': 'Toda moción de censura contra el Consejo de '
                             'Ministros debe presentarse por no menos de un '
                             'porcentaje igual a:',
                 'alternativas': ['15%', '10%', '50%', '25%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'La aprobación de una moción de censura '
                             'requiere el voto de:',
                 'alternativas': ['La cuarta parte',
                                  'Unanimidad',
                                  'Dos tercios del Congreso',
                                  'Un tercio del Congreso',
                                  'Más de la mitad del número legal de '
                                  'congresistas'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente puede disolver el Congreso si '
                             'este ha censurado o negado su confianza a un '
                             'número de Consejos de Ministros igual a:',
                 'alternativas': ['Dos', 'Cuatro', 'Uno', 'Tres', 'Cinco'],
                 'correcta': 'A'},
                {'pregunta': 'Tras la disolución del Congreso, las nuevas '
                             'elecciones deben realizarse dentro de:',
                 'alternativas': ['Dos meses',
                                  'Cuatro meses',
                                  'Un año',
                                  'Seis meses',
                                  'Tres meses'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso no puede ser disuelto en el último '
                             'año de su mandato ni cuando se está en:',
                 'alternativas': ['Estado de emergencia',
                                  'Elecciones municipales',
                                  'Receso ordinario',
                                  'Vacaciones parlamentarias',
                                  'Estado de sitio'],
                 'correcta': 'E'},
                {'pregunta': 'Al disolverse el Congreso, se mantiene en '
                             'funciones:',
                 'alternativas': ['La Mesa Directiva exclusiva',
                                  'El Consejo de Ministros exclusivo',
                                  'La Comisión Permanente',
                                  'Ningún órgano',
                                  'El Pleno completo'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 137 de la Constitución establece '
                             'dos regímenes de excepción: estado de sitio y '
                             'estado de:',
                 'alternativas': ['Emergencia',
                                  'Alerta máxima',
                                  'Conmoción',
                                  'Guerra',
                                  'Alarma'],
                 'correcta': 'A'},
                {'pregunta': 'Los regímenes de excepción son declarados por '
                             'el Presidente con acuerdo de:',
                 'alternativas': ['El Consejo de Ministros',
                                  'El Congreso exclusivo',
                                  'El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'La Contraloría'],
                 'correcta': 'A'},
                {'pregunta': 'Durante los regímenes de excepción, no se '
                             'suspenden el hábeas corpus y:',
                 'alternativas': ['La acción popular',
                                  'El hábeas data',
                                  'La acción de inconstitucionalidad',
                                  'El amparo',
                                  'El proceso de cumplimiento'],
                 'correcta': 'D'},
                {'pregunta': 'El estado de emergencia se declara por '
                             'perturbación de la paz, catástrofe o graves '
                             'circunstancias, y dura hasta:',
                 'alternativas': ['60 días',
                                  '45 días',
                                  '90 días',
                                  '30 días',
                                  '15 días'],
                 'correcta': 'A'},
                {'pregunta': 'Durante el estado de emergencia, asumen el '
                             'control interno del país:',
                 'alternativas': ['Las Fuerzas Armadas',
                                  'La Policía Nacional exclusivamente',
                                  'Los gobiernos regionales',
                                  'El Poder Judicial',
                                  'Los municipios'],
                 'correcta': 'A'},
                {'pregunta': 'El estado de sitio se declara en caso de '
                             'invasión, guerra exterior o:',
                 'alternativas': ['Escasez de alimentos',
                                  'Corrupción generalizada',
                                  'Guerra civil',
                                  'Elecciones fraudulentas',
                                  'Crisis económica'],
                 'correcta': 'C'},
                {'pregunta': 'El plazo del estado de sitio no debe exceder '
                             'de:',
                 'alternativas': ['30 días',
                                  '60 días',
                                  '15 días',
                                  '45 días',
                                  '90 días'],
                 'correcta': 'D'},
                {'pregunta': 'El encargado de elegir al presidente del '
                             'Consejo de Ministros, así como de removerlo, '
                             'es el presidente de: (IV CEPRU 2025-I)',
                 'alternativas': ['La República',
                                  'El Tribunal Constitucional',
                                  'El Congreso de la República',
                                  'El Consejo de Ministros',
                                  'La Corte Suprema de Justicia'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ORGANIZACIÓN',
                      'items': ['El Poder Ejecutivo está constituido por el '
                                'Presidente, quien desarrolla las funciones '
                                'de Jefe de Estado y Jefe de Gobierno.',
                                'El Poder Ejecutivo es el órgano encargado '
                                'de la administración del Estado y de la '
                                'ejecución de las leyes.',
                                'Integran el Poder Ejecutivo el Presidente '
                                'de la República y el Consejo de Ministros.',
                                'En el sistema presidencial, los poderes '
                                'Ejecutivo, Legislativo y Judicial son '
                                'autónomos e independientes entre sí.']},
                     {'titulo': 'ELECCIÓN DEL PRESIDENTE',
                      'items': ['Para ser presidente se requiere ser peruano '
                                'de nacimiento, tener 35 años de edad como '
                                'mínimo y gozar del derecho de sufragio.',
                                'El presidente se elige por sufragio '
                                'directo, secreto y universal, para un '
                                'mandato de 5 años, sin reelección '
                                'inmediata.',
                                'Para ganar en primera vuelta se requiere '
                                'obtener la mayoría absoluta, sin computar '
                                'votos nulos ni en blanco.',
                                'Si ningún candidato logra la mayoría '
                                'absoluta, se realiza una segunda elección '
                                'entre los dos candidatos con mayor '
                                'votación.',
                                'Según el artículo 116 de la Constitución, '
                                'el Presidente jura y asume el cargo ante el '
                                'Congreso el 28 de julio del año de la '
                                'elección.']},
                     {'titulo': 'ATRIBUCIONES DEL PRESIDENTE',
                      'items': ['Entre las atribuciones del Presidente están '
                                'cumplir y hacer cumplir la Constitución, '
                                'representar al Estado y dirigir la política '
                                'general del Gobierno.',
                                'El Presidente puede convocar al Congreso a '
                                'legislatura extraordinaria, firmando el '
                                'decreto de convocatoria.',
                                'El Presidente dirige mensajes al Congreso, '
                                'obligatoriamente en forma personal y por '
                                'escrito, al instalarse la primera '
                                'legislatura ordinaria anual.',
                                'El Presidente tiene la potestad de '
                                'reglamentar las leyes sin transgredirlas, '
                                'dictando decretos y resoluciones.',
                                'El Presidente dirige la política exterior y '
                                'las relaciones internacionales, y celebra y '
                                'ratifica tratados.']},
                     {'titulo': 'VACANCIA Y SUSPENSIÓN DEL PRESIDENTE',
                      'items': ['La Presidencia vaca por muerte, incapacidad '
                                'moral o física declarada por el Congreso, '
                                'aceptación de renuncia, o destitución.',
                                'La Presidencia también vaca si el '
                                'Presidente sale del territorio nacional sin '
                                'permiso del Congreso o no regresa a tiempo.',
                                'El ejercicio de la Presidencia se suspende '
                                'por incapacidad temporal o por estar '
                                'sometido a proceso judicial.',
                                'Según el artículo 117, el Presidente solo '
                                'puede ser acusado durante su periodo por '
                                'traición a la patria o por impedir '
                                'elecciones.',
                                'Por impedimento del Presidente, asume el '
                                'Primer Vicepresidente; en su defecto, el '
                                'Segundo; en defecto de ambos, el Presidente '
                                'del Congreso.']},
                     {'titulo': 'EL CONSEJO DE MINISTROS',
                      'items': ['El Consejo de Ministros es el organismo del '
                                'Poder Ejecutivo constituido por la reunión '
                                'de los ministros.',
                                'Son nulos los actos del Presidente que '
                                'carecen de refrendación ministerial.',
                                'El Consejo está conformado por los '
                                'ministros y el Presidente del Consejo de '
                                'Ministros, o premier, quien puede tener '
                                'cartera o no.',
                                'Para ser ministro se requiere ser peruano '
                                'de nacimiento, ciudadano en ejercicio, y '
                                'tener 25 años como mínimo.',
                                'Actualmente existen 18 ministerios en el '
                                'Perú.',
                                'Entre las atribuciones del Consejo de '
                                'Ministros está aprobar los proyectos de ley '
                                'que el Presidente somete al Congreso.']},
                     {'titulo': 'INTERPELACIÓN Y DISOLUCIÓN DEL CONGRESO',
                      'items': ['La interpelación es la facultad de los '
                                'congresistas de requerir a los ministros '
                                'que informen sobre determinado asunto; se '
                                'presenta por escrito por no menos del 15% '
                                'de congresistas.',
                                'El resultado de la interpelación puede ser '
                                'un voto de confianza o un voto de censura.',
                                'Toda moción de censura debe ser presentada '
                                'por no menos del 25% del número legal de '
                                'congresistas.',
                                'La censura requiere el voto de más de la '
                                'mitad del número legal de miembros del '
                                'Congreso.',
                                'El Presidente puede disolver el Congreso si '
                                'este ha censurado o negado su confianza a '
                                'dos Consejos de Ministros.',
                                'Las nuevas elecciones tras la disolución se '
                                'realizan dentro de los cuatro meses; no '
                                'puede disolverse en el último año de '
                                'mandato ni en estado de sitio.']},
                     {'titulo': 'REGÍMENES DE EXCEPCIÓN',
                      'items': ['El artículo 137 de la Constitución '
                                'establece dos regímenes de excepción: '
                                'estado de emergencia y estado de sitio.',
                                'Ambos son declarados por el Presidente '
                                'mediante decreto supremo, con acuerdo del '
                                'Consejo de Ministros.',
                                'El hábeas corpus y el amparo no se '
                                'suspenden durante los regímenes de '
                                'excepción.',
                                'El estado de emergencia se declara por '
                                'perturbación de la paz, catástrofe, o '
                                'graves circunstancias; dura hasta 60 días.',
                                'Durante el estado de emergencia asumen el '
                                'control las Fuerzas Armadas, según disponga '
                                'el Presidente.',
                                'El estado de sitio se declara por invasión, '
                                'guerra exterior o guerra civil; dura hasta '
                                '45 días.']}],
  'qr_reto': [{'pregunta': 'El Poder Ejecutivo está constituido por el '
                           'Presidente, quien es Jefe de Estado y:',
               'respuesta': 'Jefe de Gobierno'},
              {'pregunta': 'Si ningún candidato obtiene mayoría absoluta, se '
                           'realiza:',
               'respuesta': 'Una segunda elección entre los dos más votados'},
              {'pregunta': 'Según el artículo 116, el Presidente jura y '
                           'asume el cargo ante:',
               'respuesta': 'El Congreso'}],
  'qr_dato': 'El Poder Ejecutivo es el órgano encargado de la administración '
             'del Estado y de la ejecución de las leyes.'},
 {'num': 12,
  'titulo': 'Poder Judicial',
  'secciones': [{'titulo': '12.1 CONCEPTO Y AUTONOMÍA',
                 'items': ['El Poder Judicial es el organismo encargado de '
                           '{administrar} justicia a través de sus órganos '
                           'jerárquicos, con arreglo a la Constitución y las '
                           'leyes.',
                           'El Poder Judicial es autónomo en lo {político}, '
                           'administrativo, económico y disciplinario, e '
                           'independiente en lo {jurisdiccional}.',
                           'La potestad de administrar justicia {emana} del '
                           'pueblo y se ejerce a través de los órganos '
                           'jerárquicos del Poder Judicial.',
                           'La competencia del Poder Judicial se extiende a '
                           'todo el territorio de la {República}.']},
                {'titulo': '12.2 ESTRUCTURA ORGÁNICA',
                 'items': ['Los órganos {jurisdiccionales} del Poder '
                           'Judicial son: Corte Suprema, Cortes Superiores, '
                           'Juzgados Especializados y Mixtos, Juzgados de '
                           'Paz Letrados y Juzgados de {Paz}.',
                           'Los órganos de {gestión} incluyen la Presidencia '
                           'de la Corte Suprema, la Sala Plena y el {Consejo '
                           'Ejecutivo} del Poder Judicial.',
                           'No existe ni puede establecerse jurisdicción '
                           'independiente, salvo la {militar} y la '
                           'arbitral.']},
                {'titulo': '12.3 PRINCIPIOS DE LA FUNCIÓN JURISDICCIONAL',
                 'items': ['El primer principio es la {unidad} y '
                           'exclusividad de la función jurisdiccional.',
                           'El principio de {independencia} establece que '
                           'ninguna autoridad puede avocarse a causas '
                           'pendientes ni interferir en las funciones '
                           'jurisdiccionales.',
                           'El {debido proceso} y la tutela jurisdiccional '
                           'impiden que una persona sea juzgada por '
                           'comisiones especiales o desviada de la '
                           'jurisdicción predeterminada.',
                           'La {publicidad} en los procesos es la regla '
                           'general, salvo disposición contraria de la ley.',
                           'Los procesos por responsabilidad de funcionarios '
                           'públicos y por delitos de prensa son siempre '
                           '{públicos}.',
                           'La {motivación} escrita de las resoluciones '
                           'judiciales es obligatoria en todas las '
                           'instancias.']},
                {'titulo': '12.4 MÁS PRINCIPIOS DE LA ADMINISTRACIÓN DE '
                           'JUSTICIA',
                 'items': ['El principio de {pluralidad de instancia} '
                           'permite que una resolución pueda ser revisada '
                           'por un órgano {superior}.',
                           'El Estado debe {indemnizar}, por los errores '
                           'judiciales en procesos penales y por detenciones '
                           'arbitrarias.',
                           'El principio de no dejar de administrar justicia '
                           'por vacío legal obliga a aplicar los {principios '
                           'generales} del derecho y el derecho '
                           'consuetudinario.',
                           'El principio de {inaplicabilidad por analogía} '
                           'impide aplicar por semejanza la ley penal o '
                           'normas que restrinjan derechos.',
                           'El principio de no ser {penado} sin proceso '
                           'judicial previo.',
                           'En caso de duda o conflicto entre leyes penales, '
                           'se aplica la ley más {favorable} al procesado.',
                           'El principio de no ser {condenado} en ausencia.',
                           'Está prohibido revivir procesos fenecidos con '
                           'resolución {ejecutoriada}; la amnistía y el '
                           'indulto producen efectos de cosa {juzgada}.',
                           'El derecho de {defensa} no puede ser negado en '
                           'ningún estado del proceso.']}],
  'cuadros': [{'titulo': '12.2 ÓRGANOS JURISDICCIONALES',
               'encabezados': ['Nivel', 'Órgano'],
               'filas': [['Máximo', 'Corte {Suprema} de Justicia'],
                         ['Superior', '{Cortes} Superiores de Justicia'],
                         ['Especializado',
                          'Juzgados {Especializados} y Mixtos'],
                         ['Básico', 'Juzgados de {Paz} Letrados y de Paz']]}],
  'preguntas': [{'pregunta': 'El Poder Judicial es el organismo encargado '
                             'de:',
                 'alternativas': ['Representar al Estado en el exterior',
                                  'Dictar leyes',
                                  'Administrar justicia',
                                  'Ejecutar el presupuesto',
                                  'Organizar elecciones'],
                 'correcta': 'C'},
                {'pregunta': 'El Poder Judicial es autónomo en lo político, '
                             'administrativo, económico y:',
                 'alternativas': ['Educativo',
                                  'Militar',
                                  'Religioso',
                                  'Disciplinario',
                                  'Comercial'],
                 'correcta': 'D'},
                {'pregunta': 'En el ejercicio jurisdiccional, el Poder '
                             'Judicial es:',
                 'alternativas': ['Subordinado al Congreso',
                                  'Independiente',
                                  'Dependiente del Ejecutivo',
                                  'Controlado por el Tribunal Constitucional',
                                  'Dirigido por el Presidente'],
                 'correcta': 'B'},
                {'pregunta': 'La potestad de administrar justicia emana de:',
                 'alternativas': ['El Presidente',
                                  'Los jueces exclusivamente',
                                  'Organismos internacionales',
                                  'El pueblo',
                                  'El Congreso'],
                 'correcta': 'D'},
                {'pregunta': 'El máximo órgano jurisdiccional del Poder '
                             'Judicial es:',
                 'alternativas': ['El Consejo Ejecutivo',
                                  'Los Juzgados Mixtos',
                                  'Las Cortes Superiores',
                                  'La Corte Suprema de Justicia',
                                  'Los Juzgados de Paz'],
                 'correcta': 'D'},
                {'pregunta': 'Los Juzgados de Paz Letrados corresponden al '
                             'nivel:',
                 'alternativas': ['Internacional',
                                  'Constitucional',
                                  'Superior',
                                  'Supremo',
                                  'Básico'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano de gestión encargado de la '
                             'administración del Poder Judicial es:',
                 'alternativas': ['La Defensoría del Pueblo',
                                  'El Ministerio Público',
                                  'La Sala Penal',
                                  'El Consejo Ejecutivo del Poder Judicial',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'D'},
                {'pregunta': 'No existe ni puede establecerse jurisdicción '
                             'independiente, salvo:',
                 'alternativas': ['La religiosa',
                                  'La comercial',
                                  'La militar y la arbitral',
                                  'La internacional',
                                  'La municipal'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de unidad y exclusividad de la '
                             'función jurisdiccional implica que:',
                 'alternativas': ['Existen múltiples jurisdicciones '
                                  'paralelas',
                                  'Cualquier autoridad puede juzgar',
                                  'Los alcaldes pueden juzgar delitos',
                                  'El Congreso puede sentenciar',
                                  'No hay proceso judicial por comisión o '
                                  'delegación'],
                 'correcta': 'E'},
                {'pregunta': 'El principio de independencia jurisdiccional '
                             'impide que una autoridad:',
                 'alternativas': ['Participe en audiencias públicas',
                                  'Presente denuncias',
                                  'Se avoque a causas pendientes ante el '
                                  'órgano jurisdiccional',
                                  'Solicite información pública',
                                  'Realice investigaciones periodísticas'],
                 'correcta': 'C'},
                {'pregunta': 'El debido proceso impide que una persona sea '
                             'juzgada por:',
                 'alternativas': ['Comisiones especiales creadas al efecto',
                                  'La Corte Suprema',
                                  'Un juzgado de paz',
                                  'Un tribunal constitucional',
                                  'Un juez competente'],
                 'correcta': 'A'},
                {'pregunta': 'La regla general en los procesos judiciales es '
                             'la:',
                 'alternativas': ['Exclusividad militar',
                                  'Prohibición de prensa',
                                  'Reserva absoluta',
                                  'Publicidad, salvo disposición contraria '
                                  'de la ley',
                                  'Confidencialidad total'],
                 'correcta': 'D'},
                {'pregunta': 'Los procesos por responsabilidad de '
                             'funcionarios públicos son:',
                 'alternativas': ['Decididos por el Congreso',
                                  'Confidenciales por defecto',
                                  'Resueltos por decreto',
                                  'Siempre públicos',
                                  'Siempre reservados'],
                 'correcta': 'D'},
                {'pregunta': 'La motivación escrita de las resoluciones '
                             'judiciales es obligatoria en:',
                 'alternativas': ['Solo casos penales',
                                  'Solo la primera instancia',
                                  'Solo la Corte Suprema',
                                  'Todas las instancias',
                                  'Ningún nivel en particular'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución que precisa la '
                             'extensión jurisdiccional en comunidades es el:',
                 'alternativas': ['Artículo 91',
                                  'Artículo 22',
                                  'Artículo 51',
                                  'Artículo 149',
                                  'Artículo 24'],
                 'correcta': 'D'},
                {'pregunta': 'Ninguna autoridad puede dejar sin efecto '
                             'resoluciones que han pasado en autoridad de:',
                 'alternativas': ['Norma transitoria',
                                  'Consulta previa',
                                  'Cosa juzgada',
                                  'Reglamento interno',
                                  'Resolución administrativa'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho de gracia y la facultad de '
                             'investigación del Congreso no deben:',
                 'alternativas': ['Ser públicas',
                                  'Ejercerse nunca',
                                  'Interferir en el procedimiento '
                                  'jurisdiccional',
                                  'Aplicarse a funcionarios',
                                  'Ser reguladas por ley'],
                 'correcta': 'C'},
                {'pregunta': 'La Sala Plena de la Corte Suprema es un órgano '
                             'de:',
                 'alternativas': ['Control tributario',
                                  'Fiscalización externa',
                                  'Jurisdicción exclusiva',
                                  'Relaciones internacionales',
                                  'Gestión'],
                 'correcta': 'E'},
                {'pregunta': 'Los Juzgados de Paz, en la estructura del '
                             'Poder Judicial, están en el nivel:',
                 'alternativas': ['Más básico',
                                  'Militar',
                                  'Supremo',
                                  'Internacional',
                                  'Constitucional'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley Orgánica del Poder Judicial regula, '
                             'junto con la Constitución, el ejercicio de:',
                 'alternativas': ['Solo la función administrativa',
                                  'Solo la disciplina interna',
                                  'Las funciones jurisdiccionales y de '
                                  'gobierno',
                                  'Solo el presupuesto',
                                  'Solo las relaciones exteriores'],
                 'correcta': 'C'},
                {'pregunta': 'El principio que permite que una resolución '
                             'sea revisada por un órgano superior se llama:',
                 'alternativas': ['Publicidad',
                                  'Debido proceso',
                                  'Pluralidad de instancia',
                                  'Unidad jurisdiccional',
                                  'Cosa juzgada'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado debe indemnizar por los errores '
                             'judiciales en procesos penales y por:',
                 'alternativas': ['Detenciones arbitrarias',
                                  'Demoras administrativas',
                                  'Multas excesivas',
                                  'Costas procesales',
                                  'Apelaciones rechazadas'],
                 'correcta': 'A'},
                {'pregunta': 'En caso de vacío o deficiencia de la ley, el '
                             'juez debe aplicar los principios generales del '
                             'derecho y:',
                 'alternativas': ['Su criterio personal exclusivo',
                                  'El derecho consuetudinario',
                                  'Ninguna norma adicional',
                                  'Solo jurisprudencia extranjera',
                                  'Solo la doctrina'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que impide aplicar por semejanza '
                             'la ley penal se llama principio de:',
                 'alternativas': ['Inaplicabilidad por analogía',
                                  'Legalidad exclusiva',
                                  'Retroactividad',
                                  'Tipicidad',
                                  'Proporcionalidad'],
                 'correcta': 'A'},
                {'pregunta': 'Un principio fundamental de la administración '
                             'de justicia es que nadie puede ser penado sin:',
                 'alternativas': ['Proceso judicial previo',
                                  'Pago de fianza',
                                  'Denuncia pública',
                                  'Testigos presenciales',
                                  'Confesión previa'],
                 'correcta': 'A'},
                {'pregunta': 'En caso de duda o conflicto entre leyes '
                             'penales, se debe aplicar la ley:',
                 'alternativas': ['Más severa',
                                  'Más favorable al procesado',
                                  'Extranjera',
                                  'Más reciente exclusivamente',
                                  'Más antigua'],
                 'correcta': 'B'},
                {'pregunta': 'Un principio de la administración de justicia '
                             'establece que nadie puede ser condenado:',
                 'alternativas': ['Sin apelación',
                                  'Sin fianza',
                                  'Sin abogado',
                                  'Sin testigos',
                                  'En ausencia'],
                 'correcta': 'E'},
                {'pregunta': 'Está prohibido revivir procesos fenecidos con '
                             'resolución ejecutoriada; la amnistía y el '
                             'indulto producen efectos de:',
                 'alternativas': ['Cosa juzgada',
                                  'Revisión automática',
                                  'Prescripción inmediata',
                                  'Nulidad absoluta',
                                  'Suspensión temporal'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho de defensa no puede ser negado en '
                             'ningún:',
                 'alternativas': ['Tribunal superior exclusivo',
                                  'Recurso de apelación exclusivo',
                                  'Proceso civil exclusivo',
                                  'Estado del proceso',
                                  'Juicio oral exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano jurisdiccional jerárquico que ejerce '
                             'sus funciones en un distrito judicial es: (IV '
                             'CEPRU 2025-I)',
                 'alternativas': ['La Corte Suprema',
                                  'Los Juzgados de Paz',
                                  'Las Cortes Superiores',
                                  'Los Juzgados de Paz Letrados',
                                  'Los Juzgados Mixtos Provinciales'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y AUTONOMÍA',
                      'items': ['El Poder Judicial es el organismo encargado '
                                'de administrar justicia a través de sus '
                                'órganos jerárquicos, con arreglo a la '
                                'Constitución y las leyes.',
                                'El Poder Judicial es autónomo en lo '
                                'político, administrativo, económico y '
                                'disciplinario, e independiente en lo '
                                'jurisdiccional.',
                                'La potestad de administrar justicia emana '
                                'del pueblo y se ejerce a través de los '
                                'órganos jerárquicos del Poder Judicial.',
                                'La competencia del Poder Judicial se '
                                'extiende a todo el territorio de la '
                                'República.']},
                     {'titulo': 'ESTRUCTURA ORGÁNICA',
                      'items': ['Los órganos jurisdiccionales del Poder '
                                'Judicial son: Corte Suprema, Cortes '
                                'Superiores, Juzgados Especializados y '
                                'Mixtos, Juzgados de Paz Letrados y Juzgados '
                                'de Paz.',
                                'Los órganos de gestión incluyen la '
                                'Presidencia de la Corte Suprema, la Sala '
                                'Plena y el Consejo Ejecutivo del Poder '
                                'Judicial.',
                                'No existe ni puede establecerse '
                                'jurisdicción independiente, salvo la '
                                'militar y la arbitral.']},
                     {'titulo': 'PRINCIPIOS DE LA FUNCIÓN JURISDICCIONAL',
                      'items': ['El primer principio es la unidad y '
                                'exclusividad de la función jurisdiccional.',
                                'El principio de independencia establece que '
                                'ninguna autoridad puede avocarse a causas '
                                'pendientes ni interferir en las funciones '
                                'jurisdiccionales.',
                                'El debido proceso y la tutela '
                                'jurisdiccional impiden que una persona sea '
                                'juzgada por comisiones especiales o '
                                'desviada de la jurisdicción predeterminada.',
                                'La publicidad en los procesos es la regla '
                                'general, salvo disposición contraria de la '
                                'ley.',
                                'Los procesos por responsabilidad de '
                                'funcionarios públicos y por delitos de '
                                'prensa son siempre públicos.',
                                'La motivación escrita de las resoluciones '
                                'judiciales es obligatoria en todas las '
                                'instancias.']},
                     {'titulo': 'MÁS PRINCIPIOS DE LA ADMINISTRACIÓN DE '
                                'JUSTICIA',
                      'items': ['El principio de pluralidad de instancia '
                                'permite que una resolución pueda ser '
                                'revisada por un órgano superior.',
                                'El Estado debe indemnizar, por los errores '
                                'judiciales en procesos penales y por '
                                'detenciones arbitrarias.',
                                'El principio de no dejar de administrar '
                                'justicia por vacío legal obliga a aplicar '
                                'los principios generales del derecho y el '
                                'derecho consuetudinario.',
                                'El principio de inaplicabilidad por '
                                'analogía impide aplicar por semejanza la '
                                'ley penal o normas que restrinjan derechos.',
                                'El principio de no ser penado sin proceso '
                                'judicial previo.',
                                'En caso de duda o conflicto entre leyes '
                                'penales, se aplica la ley más favorable al '
                                'procesado.',
                                'El principio de no ser condenado en '
                                'ausencia.',
                                'Está prohibido revivir procesos fenecidos '
                                'con resolución ejecutoriada; la amnistía y '
                                'el indulto producen efectos de cosa '
                                'juzgada.',
                                'El derecho de defensa no puede ser negado '
                                'en ningún estado del proceso.']}],
  'qr_reto': [{'pregunta': 'En caso de vacío o deficiencia de la ley, el '
                           'juez debe aplicar los principios generales del '
                           'derecho y:',
               'respuesta': 'El derecho consuetudinario'},
              {'pregunta': 'El principio que impide aplicar por semejanza la '
                           'ley penal se llama principio de:',
               'respuesta': 'Inaplicabilidad por analogía'},
              {'pregunta': 'La motivación escrita de las resoluciones '
                           'judiciales es obligatoria en:',
               'respuesta': 'Todas las instancias'}],
  'qr_dato': 'La publicidad en los procesos es la regla general, salvo '
             'disposición contraria de la ley.'},
 {'num': 13,
  'titulo': 'Organismos Constitucionales Autónomos',
  'secciones': [{'titulo': '13.1 CONCEPTO Y RELACIÓN',
                 'items': ['El Estado peruano se organiza a nivel nacional, '
                           'regional y {local}, según el artículo {189} de '
                           'la Constitución.',
                           'Existen {diez} organismos constitucionales '
                           'autónomos (OCA) en el Perú.',
                           'Según Rubio, la autonomía de estos organismos '
                           'implica que sus directivos toman decisiones sin '
                           'someterse a órdenes {superiores}.']},
                {'titulo': '13.2 EL TRIBUNAL CONSTITUCIONAL',
                 'items': ['El Tribunal Constitucional es el órgano de '
                           'control de la {Constitución}, autónomo e '
                           'independiente, según el artículo {201}.',
                           'El Tribunal Constitucional se compone de {siete} '
                           'miembros, elegidos por un periodo de {cinco} '
                           'años.',
                           'Los miembros del Tribunal Constitucional son '
                           'elegidos por el Congreso con el voto favorable '
                           'de los {dos tercios} del número legal de sus '
                           'miembros.',
                           'No pueden ser elegidos magistrados del Tribunal '
                           'Constitucional los jueces o fiscales que no han '
                           'dejado el cargo con {un año} de anticipación.']},
                {'titulo': '13.3 EL MINISTERIO PÚBLICO',
                 'items': ['El Ministerio Público es el órgano {persecutor} '
                           'del delito, y es presidido por el Fiscal de la '
                           '{Nación}.',
                           'El Fiscal de la Nación es elegido por la {Junta '
                           'de Fiscales Supremos}, y su cargo dura {tres} '
                           'años, prorrogable por reelección solo dos años '
                           'más.',
                           'Según el artículo {159}, el Ministerio Público '
                           'conduce desde su inicio la {investigación} del '
                           'delito.',
                           'La {Policía Nacional} está obligada a cumplir '
                           'los mandatos del Ministerio Público en el ámbito '
                           'de su función.']},
                {'titulo': '13.4 LA JUNTA NACIONAL DE JUSTICIA',
                 'items': ['La {Junta Nacional de Justicia} sustituyó al '
                           'Consejo Nacional de la Magistratura, entrando en '
                           'funciones a inicios de {2020}.',
                           'Según el artículo {150} de la Constitución, la '
                           'Junta selecciona y nombra a jueces y {fiscales}, '
                           'salvo los de elección popular.',
                           'Para ser miembro se requiere ser peruano de '
                           'nacimiento, abogado, y tener entre {45} y 75 '
                           'años de edad.',
                           'La Junta está conformada por {siete} miembros '
                           'titulares, seleccionados por concurso público, '
                           'por un periodo de {cinco} años, sin reelección.',
                           'Entre sus funciones está nombrar jueces y '
                           'fiscales, y {ratificar} a jueces y fiscales cada '
                           'siete años.']},
                {'titulo': '13.5 LA DEFENSORÍA DEL PUEBLO',
                 'items': ['La {Defensoría del Pueblo} tiene su origen en '
                           '{Suecia}; en el Perú se incorporó con la '
                           'Constitución de 1993.',
                           'El {Defensor del Pueblo} es elegido y removido '
                           'por el Congreso con el voto de los {dos tercios} '
                           'de su número legal.',
                           'Para ser Defensor del Pueblo se requiere tener '
                           '{35} años de edad y ser {abogado}.',
                           'El cargo de Defensor del Pueblo dura {cinco} '
                           'años.',
                           'Corresponde a la Defensoría defender los '
                           'derechos {constitucionales} y supervisar el '
                           'cumplimiento de deberes de la administración '
                           'estatal.']},
                {'titulo': '13.6 BCR, SBS Y CONTRALORÍA',
                 'items': ['La finalidad del {Banco Central de Reserva} es '
                           'preservar la {estabilidad} monetaria.',
                           'El BCR regula la {moneda} y el crédito del '
                           'sistema financiero, y administra las {reservas} '
                           'internacionales.',
                           'El BCR está prohibido de conceder '
                           '{financiamiento} al erario, salvo compra en el '
                           'mercado secundario de valores del Tesoro.',
                           'La {Superintendencia de Banca, Seguros y AFP} '
                           '(SBS) supervisa a las empresas del ámbito '
                           'financiero y de {seguros}.',
                           'El Superintendente de la SBS es designado por el '
                           '{Poder Ejecutivo} y ratificado por el '
                           '{Congreso}.',
                           'La {Contraloría General} de la República es el '
                           'órgano superior del Sistema Nacional de '
                           '{Control}.',
                           'La Contraloría supervisa la legalidad de la '
                           'ejecución del {Presupuesto} del Estado y la '
                           'deuda pública.',
                           'El {Contralor General} es designado por el '
                           'Congreso, a propuesta del Poder Ejecutivo, por '
                           '{siete} años.']},
                {'titulo': '13.7 EL SISTEMA ELECTORAL: JNE, ONPE, RENIEC',
                 'items': ['El sistema electoral es {tricéfalo}: JNE, ONPE y '
                           'RENIEC, que actúan con {autonomía} y '
                           'coordinación entre sí.',
                           'Los integrantes del Pleno del {Jurado Nacional '
                           'de Elecciones} (JNE) tienen entre 45 y 70 años, '
                           'elegidos por {cuatro} años.',
                           'El JNE fiscaliza la legalidad del {sufragio} y '
                           'de los procesos electorales, y proclama a los '
                           'candidatos {elegidos}.',
                           'El Pleno del JNE está compuesto por {cinco} '
                           'miembros, elegidos por la Corte Suprema, la '
                           'Junta de Fiscales, y los colegios de abogados.',
                           'El Jefe de la {ONPE} (Oficina Nacional de '
                           'Procesos Electorales) es nombrado por la Junta '
                           'Nacional de Justicia por {cuatro} años.',
                           'A la ONPE le corresponde {organizar} todos los '
                           'procesos electorales y el diseño de la cédula de '
                           '{sufragio}.',
                           'El Jefe del {RENIEC} también es nombrado por la '
                           'Junta Nacional de Justicia por {cuatro} años.',
                           'El RENIEC tiene a su cargo la inscripción de '
                           '{nacimientos}, matrimonios, divorcios y '
                           'defunciones.']}],
  'cuadros': [{'titulo': '13.1 LOS DIEZ ORGANISMOS CONSTITUCIONALES '
                         'AUTÓNOMOS',
               'encabezados': ['N°', 'Organismo'],
               'filas': [['1', '{Tribunal} Constitucional'],
                         ['2', '{Ministerio} Público'],
                         ['3', '{Junta} Nacional de Justicia'],
                         ['4', '{Defensoría} del Pueblo'],
                         ['5', '{Banco Central} de Reserva'],
                         ['6', '{Contraloría} General de la República'],
                         ['7', '{Jurado Nacional} de Elecciones']]}],
  'preguntas': [{'pregunta': 'El Estado peruano se organiza a nivel '
                             'nacional, regional y:',
                 'alternativas': ['Local',
                                  'Eclesiástico',
                                  'Internacional',
                                  'Empresarial',
                                  'Militar'],
                 'correcta': 'A'},
                {'pregunta': 'El número de organismos constitucionales '
                             'autónomos en el Perú es:',
                 'alternativas': ['Quince',
                                  'Diez',
                                  'Cinco',
                                  'Tres',
                                  'Veinte'],
                 'correcta': 'B'},
                {'pregunta': 'La autonomía de los OCA implica que sus '
                             'directivos:',
                 'alternativas': ['Actúan solo por consulta popular',
                                  'Toman decisiones sin someterse a órdenes '
                                  'superiores',
                                  'Dependen del Presidente',
                                  'Son elegidos por sorteo',
                                  'Dependen del Congreso exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional es el órgano de '
                             'control de:',
                 'alternativas': ['La Constitución',
                                  'El presupuesto',
                                  'El comercio exterior',
                                  'La banca',
                                  'Las elecciones únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'El Tribunal Constitucional está regulado en el '
                             'artículo:',
                 'alternativas': ['158', '102', '24', '201', '91'],
                 'correcta': 'D'},
                {'pregunta': 'El Tribunal Constitucional se compone de:',
                 'alternativas': ['Doce miembros',
                                  'Nueve miembros',
                                  'Siete miembros',
                                  'Tres miembros',
                                  'Cinco miembros'],
                 'correcta': 'C'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Tres años',
                                  'Vitalicio',
                                  'Diez años',
                                  'Cinco años',
                                  'Cuatro años'],
                 'correcta': 'D'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por el Congreso con:',
                 'alternativas': ['Consulta popular directa',
                                  'Mayoría simple',
                                  'Unanimidad',
                                  'El voto de los dos tercios del número '
                                  'legal de miembros',
                                  'Mayoría absoluta'],
                 'correcta': 'D'},
                {'pregunta': 'No pueden ser magistrados del Tribunal '
                             'Constitucional los jueces o fiscales que no '
                             'dejaron el cargo con anticipación de:',
                 'alternativas': ['Cinco años',
                                  'Un año',
                                  'Seis meses',
                                  'Dos años',
                                  'Tres meses'],
                 'correcta': 'B'},
                {'pregunta': 'El Ministerio Público es el órgano encargado '
                             'de:',
                 'alternativas': ['Perseguir el delito',
                                  'Emitir moneda',
                                  'Legislar',
                                  'Administrar justicia directamente',
                                  'Dirigir el gobierno'],
                 'correcta': 'A'},
                {'pregunta': 'El Ministerio Público es presidido por:',
                 'alternativas': ['El Defensor del Pueblo',
                                  'El presidente del Congreso',
                                  'El Fiscal de la Nación',
                                  'El presidente del Poder Judicial',
                                  'El Presidente de la República'],
                 'correcta': 'C'},
                {'pregunta': 'El Fiscal de la Nación es elegido por:',
                 'alternativas': ['El Presidente de la República',
                                  'El Poder Judicial',
                                  'Voto popular directo',
                                  'El Congreso',
                                  'La Junta de Fiscales Supremos'],
                 'correcta': 'E'},
                {'pregunta': 'El cargo de Fiscal de la Nación dura:',
                 'alternativas': ['Vitalicio',
                                  'Un año',
                                  'Tres años',
                                  'Cinco años',
                                  'Dos años'],
                 'correcta': 'C'},
                {'pregunta': 'El cargo de Fiscal de la Nación puede '
                             'prorrogarse por reelección hasta por:',
                 'alternativas': ['Un año más',
                                  'Cinco años más',
                                  'Diez años más',
                                  'No es prorrogable',
                                  'Dos años más'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 159, el Ministerio Público '
                             'conduce desde su inicio:',
                 'alternativas': ['La política exterior',
                                  'La investigación del delito',
                                  'Las elecciones',
                                  'El presupuesto público',
                                  'El proceso legislativo'],
                 'correcta': 'B'},
                {'pregunta': 'La Policía Nacional está obligada a cumplir '
                             'los mandatos de:',
                 'alternativas': ['Solo el Poder Judicial',
                                  'Los gobiernos locales',
                                  'El Ministerio Público',
                                  'Los gobiernos regionales',
                                  'Solo el Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los organismos constitucionales '
                             'autónomos figura el organismo encargado de '
                             'emitir moneda, que es:',
                 'alternativas': ['La SBS',
                                  'El Banco Central de Reserva',
                                  'La SUNAT',
                                  'El MEF',
                                  'El BID'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo encargado de la defensa de los '
                             'derechos constitucionales de la persona es:',
                 'alternativas': ['El JNE',
                                  'La Defensoría del Pueblo',
                                  'El Tribunal Constitucional',
                                  'La ONPE',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo encargado de organizar los '
                             'procesos electorales es:',
                 'alternativas': ['La ONPE',
                                  'El Ministerio Público',
                                  'El RENIEC',
                                  'La Defensoría del Pueblo',
                                  'El JNE'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo encargado del registro de '
                             'identificación y estado civil es:',
                 'alternativas': ['El RENIEC',
                                  'El JNE',
                                  'La ONPE',
                                  'El INEI',
                                  'La SUNARP'],
                 'correcta': 'A'},
                {'pregunta': 'La Junta Nacional de Justicia sustituyó al:',
                 'alternativas': ['Jurado Nacional de Elecciones',
                                  'Tribunal Constitucional',
                                  'Poder Judicial',
                                  'Consejo Nacional de la Magistratura',
                                  'Ministerio Público'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 150 de la Constitución, la '
                             'Junta Nacional de Justicia selecciona y nombra '
                             'a:',
                 'alternativas': ['Solo alcaldes',
                                  'Solo gobernadores regionales',
                                  'Jueces y fiscales',
                                  'Solo congresistas',
                                  'Solo ministros'],
                 'correcta': 'C'},
                {'pregunta': 'Para ser miembro de la Junta Nacional de '
                             'Justicia se requiere tener una edad entre:',
                 'alternativas': ['45 y 75 años',
                                  '30 y 65 años',
                                  '40 y 70 años',
                                  '35 y 80 años',
                                  '25 y 60 años'],
                 'correcta': 'A'},
                {'pregunta': 'La Junta Nacional de Justicia está conformada '
                             'por un número de miembros titulares igual a:',
                 'alternativas': ['Nueve', 'Siete', 'Cinco', 'Tres', 'Once'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de los miembros de la Junta '
                             'Nacional de Justicia es de:',
                 'alternativas': ['Seis años',
                                  'Tres años',
                                  'Cinco años',
                                  'Cuatro años',
                                  'Siete años'],
                 'correcta': 'C'},
                {'pregunta': 'La Defensoría del Pueblo tiene su origen '
                             'histórico en:',
                 'alternativas': ['Francia',
                                  'España',
                                  'Estados Unidos',
                                  'Suecia',
                                  'Inglaterra'],
                 'correcta': 'D'},
                {'pregunta': 'El Defensor del Pueblo es elegido y removido '
                             'por el Congreso con el voto de:',
                 'alternativas': ['Un tercio',
                                  'Unanimidad',
                                  'Los dos tercios de su número legal',
                                  'Mayoría simple',
                                  'La mitad más uno'],
                 'correcta': 'C'},
                {'pregunta': 'Para ser elegido Defensor del Pueblo se '
                             'requiere tener una edad mínima de:',
                 'alternativas': ['25 años',
                                  '35 años',
                                  '45 años',
                                  '40 años',
                                  '30 años'],
                 'correcta': 'B'},
                {'pregunta': 'El cargo de Defensor del Pueblo dura:',
                 'alternativas': ['Seis años',
                                  'Siete años',
                                  'Cinco años',
                                  'Cuatro años',
                                  'Tres años'],
                 'correcta': 'C'},
                {'pregunta': 'La finalidad principal del Banco Central de '
                             'Reserva es:',
                 'alternativas': ['Supervisar el Poder Judicial',
                                  'Recaudar impuestos',
                                  'Preservar la estabilidad monetaria',
                                  'Fiscalizar elecciones',
                                  'Administrar el presupuesto público'],
                 'correcta': 'C'},
                {'pregunta': 'El BCR está prohibido de conceder '
                             'financiamiento al erario, salvo la compra en '
                             'el mercado secundario de valores emitidos por:',
                 'alternativas': ['Gobiernos regionales',
                                  'El Tesoro Público',
                                  'Municipalidades',
                                  'Bancos privados',
                                  'Empresas mineras'],
                 'correcta': 'B'},
                {'pregunta': 'La SBS (Superintendencia de Banca, Seguros y '
                             'AFP) supervisa a las empresas vinculadas al '
                             'ámbito:',
                 'alternativas': ['Minero',
                                  'Financiero y de seguros',
                                  'Turístico',
                                  'Educativo',
                                  'Agrícola'],
                 'correcta': 'B'},
                {'pregunta': 'El Superintendente de la SBS es designado por '
                             'el Poder Ejecutivo y ratificado por:',
                 'alternativas': ['El BCR',
                                  'El Congreso',
                                  'La Contraloría',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'La Contraloría General de la República es el '
                             'órgano superior del Sistema Nacional de:',
                 'alternativas': ['Control',
                                  'Seguridad',
                                  'Salud',
                                  'Educación',
                                  'Justicia'],
                 'correcta': 'A'},
                {'pregunta': 'El Contralor General es designado por el '
                             'Congreso, a propuesta del Poder Ejecutivo, por '
                             'un periodo de:',
                 'alternativas': ['Tres años',
                                  'Siete años',
                                  'Cinco años',
                                  'Seis años',
                                  'Cuatro años'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema electoral peruano es de naturaleza:',
                 'alternativas': ['Unicéfalo',
                                  'Tetracéfalo',
                                  'Bicéfalo',
                                  'Tricéfalo',
                                  'Pentacéfalo'],
                 'correcta': 'D'},
                {'pregunta': 'Los integrantes del Pleno del Jurado Nacional '
                             'de Elecciones son elegidos por un periodo de:',
                 'alternativas': ['Seis años',
                                  'Dos años',
                                  'Cuatro años',
                                  'Cinco años',
                                  'Tres años'],
                 'correcta': 'C'},
                {'pregunta': 'El JNE fiscaliza la legalidad del ejercicio '
                             'del sufragio y de la realización de:',
                 'alternativas': ['Solo el registro civil',
                                  'Solo la educación cívica',
                                  'Los procesos electorales',
                                  'Solo la seguridad ciudadana',
                                  'Solo el presupuesto'],
                 'correcta': 'C'},
                {'pregunta': 'El Pleno del Jurado Nacional de Elecciones '
                             'está compuesto por un número de miembros igual '
                             'a:',
                 'alternativas': ['Siete',
                                  'Cuatro',
                                  'Cinco',
                                  'Tres',
                                  'Nueve'],
                 'correcta': 'C'},
                {'pregunta': 'El Jefe de la Oficina Nacional de Procesos '
                             'Electorales (ONPE) es nombrado por:',
                 'alternativas': ['La Contraloría',
                                  'El Congreso',
                                  'El JNE',
                                  'El Presidente de la República',
                                  'La Junta Nacional de Justicia'],
                 'correcta': 'E'},
                {'pregunta': 'A la ONPE le corresponde organizar los '
                             'procesos electorales, incluyendo el diseño de:',
                 'alternativas': ['Los partidos políticos',
                                  'Las cortes electorales',
                                  'Las leyes electorales',
                                  'La cédula de sufragio',
                                  'El padrón judicial'],
                 'correcta': 'D'},
                {'pregunta': 'El RENIEC tiene a su cargo la inscripción de '
                             'nacimientos, matrimonios, divorcios y:',
                 'alternativas': ['Contratos comerciales',
                                  'Propiedades',
                                  'Vehículos',
                                  'Empresas',
                                  'Defunciones'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo encargado de inscribir los actos '
                             'relativos a la capacidad y estado civil de las '
                             'personas naturales es: (II CEPRU 2023-II)',
                 'alternativas': ['SUNAT',
                                  'Registros Públicos',
                                  'JNE',
                                  'ONPE',
                                  'RENIEC'],
                 'correcta': 'E'},
                {'pregunta': 'El Organismo Constitucional Autónomo que '
                             'protege los derechos constitucionales de la '
                             'persona y la comunidad se denomina: (II CEPRU '
                             '2017-I)',
                 'alternativas': ['Ministerio de Justicia y Derechos Humanos',
                                  'Comisión Andina de Juristas',
                                  'Asociación Pro Derechos Humanos',
                                  'Defensoría del Pueblo',
                                  'Comisión de la Verdad y la '
                                  'Reconciliación'],
                 'correcta': 'D'},
                {'pregunta': 'Una atribución del Jurado Nacional de '
                             'Elecciones es: (II CEPRU 2017-I)',
                 'alternativas': ['Organizar y ejecutar los procesos '
                                  'electorales, referéndum y consultas '
                                  'populares',
                                  'Velar por la obtención de la fiel y libre '
                                  'expresión de la voluntad popular',
                                  'Proclamar a los candidatos elegidos y '
                                  'expedir las credenciales correspondientes',
                                  'Confeccionar un registro único de '
                                  'identificación',
                                  'Asignar un código único de '
                                  'identificación'],
                 'correcta': 'C'},
                {'pregunta': 'Es atribución de la Oficina Nacional de '
                             'Procesos Electorales (ONPE): (II CEPRU 2018-I)',
                 'alternativas': ['Disponer la protección de la libertad '
                                  'personal en los comicios',
                                  'Fiscalizar la realización de los procesos '
                                  'electorales',
                                  'Preparar el padrón electoral',
                                  'Expedir las credenciales a las '
                                  'autoridades elegidas',
                                  'Organizar los procesos electorales'],
                 'correcta': 'E'},
                {'pregunta': 'La atribución del JNE de mantener y custodiar '
                             'el registro de: (II CEPRU 2018-I)',
                 'alternativas': ['Organizaciones Políticas',
                                  'Personas Jurídicas',
                                  'Personas Naturales',
                                  'Defunciones',
                                  'Nacimientos'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo que prepara, mantiene y actualiza '
                             'el padrón electoral es: (II CEPRU 2018-I)',
                 'alternativas': ['La Corte Superior de Justicia',
                                  'El Registro Nacional de Identificación y '
                                  'Estado Civil',
                                  'El Jurado Nacional de Elecciones',
                                  'El Consejo Nacional de la Magistratura',
                                  'La Oficina Nacional de Procesos '
                                  'Electorales'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y RELACIÓN',
                      'items': ['El Estado peruano se organiza a nivel '
                                'nacional, regional y local, según el '
                                'artículo 189 de la Constitución.',
                                'Existen diez organismos constitucionales '
                                'autónomos (OCA) en el Perú.',
                                'Según Rubio, la autonomía de estos '
                                'organismos implica que sus directivos toman '
                                'decisiones sin someterse a órdenes '
                                'superiores.']},
                     {'titulo': 'EL TRIBUNAL CONSTITUCIONAL',
                      'items': ['El Tribunal Constitucional es el órgano de '
                                'control de la Constitución, autónomo e '
                                'independiente, según el artículo 201.',
                                'El Tribunal Constitucional se compone de '
                                'siete miembros, elegidos por un periodo de '
                                'cinco años.',
                                'Los miembros del Tribunal Constitucional '
                                'son elegidos por el Congreso con el voto '
                                'favorable de los dos tercios del número '
                                'legal de sus miembros.',
                                'No pueden ser elegidos magistrados del '
                                'Tribunal Constitucional los jueces o '
                                'fiscales que no han dejado el cargo con un '
                                'año de anticipación.']},
                     {'titulo': 'EL MINISTERIO PÚBLICO',
                      'items': ['El Ministerio Público es el órgano '
                                'persecutor del delito, y es presidido por '
                                'el Fiscal de la Nación.',
                                'El Fiscal de la Nación es elegido por la '
                                'Junta de Fiscales Supremos, y su cargo dura '
                                'tres años, prorrogable por reelección solo '
                                'dos años más.',
                                'Según el artículo 159, el Ministerio '
                                'Público conduce desde su inicio la '
                                'investigación del delito.',
                                'La Policía Nacional está obligada a cumplir '
                                'los mandatos del Ministerio Público en el '
                                'ámbito de su función.']},
                     {'titulo': 'LA JUNTA NACIONAL DE JUSTICIA',
                      'items': ['La Junta Nacional de Justicia sustituyó al '
                                'Consejo Nacional de la Magistratura, '
                                'entrando en funciones a inicios de 2020.',
                                'Según el artículo 150 de la Constitución, '
                                'la Junta selecciona y nombra a jueces y '
                                'fiscales, salvo los de elección popular.',
                                'Para ser miembro se requiere ser peruano de '
                                'nacimiento, abogado, y tener entre 45 y 75 '
                                'años de edad.',
                                'La Junta está conformada por siete miembros '
                                'titulares, seleccionados por concurso '
                                'público, por un periodo de cinco años, sin '
                                'reelección.',
                                'Entre sus funciones está nombrar jueces y '
                                'fiscales, y ratificar a jueces y fiscales '
                                'cada siete años.']},
                     {'titulo': 'LA DEFENSORÍA DEL PUEBLO',
                      'items': ['La Defensoría del Pueblo tiene su origen en '
                                'Suecia; en el Perú se incorporó con la '
                                'Constitución de 1993.',
                                'El Defensor del Pueblo es elegido y '
                                'removido por el Congreso con el voto de los '
                                'dos tercios de su número legal.',
                                'Para ser Defensor del Pueblo se requiere '
                                'tener 35 años de edad y ser abogado.',
                                'El cargo de Defensor del Pueblo dura cinco '
                                'años.',
                                'Corresponde a la Defensoría defender los '
                                'derechos constitucionales y supervisar el '
                                'cumplimiento de deberes de la '
                                'administración estatal.']},
                     {'titulo': 'BCR, SBS Y CONTRALORÍA',
                      'items': ['La finalidad del Banco Central de Reserva '
                                'es preservar la estabilidad monetaria.',
                                'El BCR regula la moneda y el crédito del '
                                'sistema financiero, y administra las '
                                'reservas internacionales.',
                                'El BCR está prohibido de conceder '
                                'financiamiento al erario, salvo compra en '
                                'el mercado secundario de valores del '
                                'Tesoro.',
                                'La Superintendencia de Banca, Seguros y AFP '
                                '(SBS) supervisa a las empresas del ámbito '
                                'financiero y de seguros.',
                                'El Superintendente de la SBS es designado '
                                'por el Poder Ejecutivo y ratificado por el '
                                'Congreso.',
                                'La Contraloría General de la República es '
                                'el órgano superior del Sistema Nacional de '
                                'Control.']},
                     {'titulo': 'EL SISTEMA ELECTORAL: JNE, ONPE, RENIEC',
                      'items': ['El sistema electoral es tricéfalo: JNE, '
                                'ONPE y RENIEC, que actúan con autonomía y '
                                'coordinación entre sí.',
                                'Los integrantes del Pleno del Jurado '
                                'Nacional de Elecciones (JNE) tienen entre '
                                '45 y 70 años, elegidos por cuatro años.',
                                'El JNE fiscaliza la legalidad del sufragio '
                                'y de los procesos electorales, y proclama a '
                                'los candidatos elegidos.',
                                'El Pleno del JNE está compuesto por cinco '
                                'miembros, elegidos por la Corte Suprema, la '
                                'Junta de Fiscales, y los colegios de '
                                'abogados.',
                                'El Jefe de la ONPE (Oficina Nacional de '
                                'Procesos Electorales) es nombrado por la '
                                'Junta Nacional de Justicia por cuatro años.',
                                'A la ONPE le corresponde organizar todos '
                                'los procesos electorales y el diseño de la '
                                'cédula de sufragio.']}],
  'qr_reto': [{'pregunta': 'El organismo encargado de inscribir los actos '
                           'relativos a la capacidad y estado civil de las '
                           'personas naturales es:',
               'respuesta': 'RENIEC'},
              {'pregunta': 'Los miembros del Tribunal Constitucional son '
                           'elegidos por un periodo de:',
               'respuesta': 'Cinco años'},
              {'pregunta': 'El Estado peruano se organiza a nivel nacional, '
                           'regional y:',
               'respuesta': 'Local'}],
  'qr_dato': 'El Ministerio Público es el órgano persecutor del delito, y es '
             'presidido por el Fiscal de la Nación.'},
 {'num': 14,
  'titulo': 'Régimen Económico',
  'secciones': [{'titulo': '14.1 CONCEPTO',
                 'items': ['Según Sumar Albujar, el régimen económico '
                           'consiste en las normas o principios que definen '
                           'el {rol} del Estado en materia económica.',
                           'Según Rodríguez Cairo, el régimen económico se '
                           'orienta a garantizar la {gobernabilidad} de un '
                           'país y contribuir al desempeño económico.']},
                {'titulo': '14.2 LA CONSTITUCIÓN ECONÓMICA',
                 'items': ['Según García Belaúnde, la Constitución Económica '
                           'surgió en el periodo de {entreguerras}, en la '
                           'primera mitad del siglo {XX}.',
                           'La Constitución de {Weimar} es considerada '
                           'pionera del constitucionalismo económico.',
                           'La Constitución de Weimar garantiza el derecho '
                           'de {propiedad}, aunque admite límites por el '
                           'bien general o función {social}.']},
                {'titulo': '14.3 LA ECONOMÍA SOCIAL DE MERCADO',
                 'items': ['La {economía social de mercado} es '
                           'representativa de los valores constitucionales '
                           'de libertad y {justicia}.',
                           'Según Herhärd y Müller Armack, este orden '
                           'asegura la {competencia} y transforma la '
                           'productividad individual en progreso {social}.',
                           'La economía social de mercado combate la '
                           'formación de {carteles} y la concentración de '
                           'poder económico.',
                           'El mercado funciona de manera óptima cuando el '
                           'Estado establece normas claras sin {intervenir} '
                           'de manera permanente.',
                           'La práctica de la economía social de mercado se '
                           'refuerza por los principios de {solidaridad} y '
                           'subsidiaridad.',
                           'El principio de {subsidiaridad} establece que lo '
                           'que el individuo puede hacer por propia '
                           'iniciativa no debe hacerlo el {Estado}.']},
                {'titulo': '14.4 LIBERTADES ECONÓMICAS',
                 'items': ['El artículo {58} de la Constitución establece '
                           'que la iniciativa privada es {libre}, ejercida '
                           'en una economía social de mercado.',
                           'El reconocimiento constitucional de las '
                           'libertades económicas en el Perú se inicia con '
                           'el texto de {1823}.',
                           'La {libertad de empresa} comprende la facultad '
                           'de emprender, crear, organizar, gestionar, '
                           'competir y {cerrar} una empresa.',
                           'La {libertad de comercio} es la capacidad de '
                           'mediar entre oferta y demanda para obtener un '
                           'beneficio económico.',
                           'Según el artículo {59}, el ejercicio de la '
                           'libertad de comercio no debe ser lesivo a la '
                           'moral, la salud o la seguridad {pública}.',
                           'La {libertad de industria} es la facultad de '
                           'realizar operaciones destinadas a la obtención o '
                           '{transformación} de productos naturales.',
                           'El artículo {65} de la Constitución establece un '
                           'deber especial de protección a los '
                           '{consumidores} y usuarios.']},
                {'titulo': '14.5 EL TRIBUTO Y SUS CLASES',
                 'items': ['El {tributo} es el concepto fundamental del '
                           'Derecho Tributario; el {impuesto}, la tasa y la '
                           'contribución son sus especies.',
                           'El {impuesto} es la categoría jurídica más '
                           'importante del tributo; su fundamento es la '
                           'capacidad {contributiva}.',
                           'La recaudación de impuestos es controlada por el '
                           '{Tesoro Público} del Ministerio de Economía y '
                           'Finanzas, mediante caja {única}.',
                           'La {tasa} tiene como hecho gravado un servicio '
                           'público {individualizado}; su cuantía no debe '
                           'exceder el gasto del servicio.',
                           'La {contribución} es el tributo cuya obligación '
                           'tiene como hecho generador beneficios derivados '
                           'de {obras} públicas o actividades estatales.']},
                {'titulo': '14.6 PRINCIPIOS DE LA POTESTAD TRIBUTARIA',
                 'items': ['El artículo {74} de la Constitución establece '
                           'que los tributos se crean, modifican o derogan '
                           'exclusivamente por {ley} o decreto legislativo.',
                           'Los {gobiernos locales} pueden crear, modificar '
                           'y suprimir contribuciones y tasas dentro de su '
                           '{jurisdicción}.',
                           'Ningún tributo puede tener efecto '
                           '{confiscatorio}.',
                           'Los {decretos de urgencia} no pueden contener '
                           'materia tributaria.',
                           'El principio de {reserva de la ley} establece '
                           'que solo por ley se puede determinar al '
                           'contribuyente y fijar el monto del {tributo}.',
                           'El principio de {legalidad} complementa la '
                           'reserva de ley: el uso del instrumento legal '
                           'permitido por su respectivo {titular}.',
                           'El principio de {igualdad tributaria} establece '
                           'que situaciones iguales deben ser tratadas '
                           '{igualmente} y las desiguales, desigualmente.']}],
  'cuadros': [{'titulo': '14.3 PRINCIPIOS DE LA ECONOMÍA SOCIAL DE MERCADO',
               'encabezados': ['Principio', 'Contenido'],
               'filas': [['{Solidaridad}',
                          'Equilibrio social y bien {común}'],
                         ['{Subsidiaridad}',
                          'El {Estado} no hace lo que el individuo puede '
                          'hacer']]}],
  'preguntas': [{'pregunta': 'Según Sumar Albujar, el régimen económico '
                             'define el rol de:',
                 'alternativas': ['Los organismos internacionales',
                                  'Las empresas privadas',
                                  'El Estado en materia económica',
                                  'Los sindicatos',
                                  'El sector informal'],
                 'correcta': 'C'},
                {'pregunta': 'Según García Belaúnde, la Constitución '
                             'Económica surgió en:',
                 'alternativas': ['La Antigüedad clásica',
                                  'El siglo XXI',
                                  'La época colonial',
                                  'El periodo de entreguerras del siglo XX',
                                  'El siglo XIX'],
                 'correcta': 'D'},
                {'pregunta': 'La constitución considerada pionera del '
                             'constitucionalismo económico es la de:',
                 'alternativas': ['Bayona',
                                  'Roma',
                                  'Filadelfia',
                                  'Cádiz',
                                  'Weimar'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución de Weimar garantiza el derecho '
                             'de:',
                 'alternativas': ['Propiedad, con límites por el bien '
                                  'general',
                                  'Monopolio estatal',
                                  'Nacionalización total',
                                  'Voto universal',
                                  'Libre comercio sin restricciones'],
                 'correcta': 'A'},
                {'pregunta': 'El régimen económico peruano se basa, entre '
                             'otros principios, en la economía social de:',
                 'alternativas': ['Autarquía',
                                  'Planificación central',
                                  'Trueque',
                                  'Mercado',
                                  'Estado'],
                 'correcta': 'D'},
                {'pregunta': 'La economía social de mercado es '
                             'representativa de los valores de:',
                 'alternativas': ['Uniformidad y control',
                                  'Propiedad colectiva obligatoria',
                                  'Autoridad y jerarquía',
                                  'Aislamiento económico',
                                  'Libertad y justicia'],
                 'correcta': 'E'},
                {'pregunta': 'Según Herhärd y Müller Armack, la economía '
                             'social de mercado transforma la productividad '
                             'individual en:',
                 'alternativas': ['Progreso social',
                                  'Ganancia exclusiva de empresarios',
                                  'Control estatal total',
                                  'Monopolio privado',
                                  'Estancamiento económico'],
                 'correcta': 'A'},
                {'pregunta': 'La economía social de mercado combate la '
                             'formación de:',
                 'alternativas': ['Pequeñas empresas',
                                  'Carteles y concentración de poder '
                                  'económico',
                                  'Sindicatos',
                                  'Mercados locales',
                                  'Cooperativas'],
                 'correcta': 'B'},
                {'pregunta': 'Para que funcione de manera óptima el mercado, '
                             'el Estado debe:',
                 'alternativas': ['Nacionalizar las empresas',
                                  'Controlar todos los precios',
                                  'Eliminar la competencia',
                                  'Intervenir permanentemente',
                                  'Establecer normas claras sin intervenir '
                                  'de manera permanente'],
                 'correcta': 'E'},
                {'pregunta': 'La economía social de mercado requiere un '
                             'Estado:',
                 'alternativas': ['Débil y dependiente de grupos de poder',
                                  'Fuerte e independiente de los grupos de '
                                  'poder económico',
                                  'Controlado por monopolios',
                                  'Sin aparato judicial',
                                  'Ausente en la economía'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de solidaridad en la economía '
                             'social de mercado exige:',
                 'alternativas': ['Individualismo extremo',
                                  'Monopolio estatal',
                                  'Competencia sin límites',
                                  'Equilibrio social y promoción del bien '
                                  'común',
                                  'Aislamiento económico'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de subsidiaridad establece que el '
                             'Estado no debe hacer:',
                 'alternativas': ['Políticas sociales',
                                  'Ninguna función pública',
                                  'Regulación económica',
                                  'Lo que el individuo puede hacer por '
                                  'propia iniciativa',
                                  'Control tributario'],
                 'correcta': 'D'},
                {'pregunta': 'El mercado y la competencia, según el texto, '
                             'deben garantizar la libertad de:',
                 'alternativas': ['Solo los bancos',
                                  'Solo los empresarios',
                                  'Solo los inversionistas extranjeros',
                                  'Consumidores, empleadores y trabajadores',
                                  'Solo el Estado'],
                 'correcta': 'D'},
                {'pregunta': 'Combatir los monopolios requiere, según el '
                             'texto, una legislación:',
                 'alternativas': ['De nacionalización',
                                  'De libre mercado absoluto',
                                  'De protección arancelaria total',
                                  'De control de precios',
                                  'Antimonopolio'],
                 'correcta': 'E'},
                {'pregunta': 'El régimen económico también se define como el '
                             'conjunto de reglas de juego con rango:',
                 'alternativas': ['Consuetudinario',
                                  'Reglamentario',
                                  'Municipal',
                                  'Internacional exclusivo',
                                  'Constitucional'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los principios que rigen el régimen '
                             'económico peruano figura la libre:',
                 'alternativas': ['Censura',
                                  'Competencia',
                                  'Nacionalización',
                                  'Migración',
                                  'Expropiación'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen económico busca contribuir '
                             'positivamente al:',
                 'alternativas': ['Desempeño económico del país',
                                  'Cierre de fronteras',
                                  'Aislamiento comercial',
                                  'Monopolio estatal',
                                  'Control absoluto del mercado'],
                 'correcta': 'A'},
                {'pregunta': 'El aparato administrativo y judicial en la '
                             'economía social de mercado debe ser:',
                 'alternativas': ['Controlado por empresas privadas',
                                  'Eliminado del sistema',
                                  'Independiente y libre de corrupción',
                                  'Dependiente del poder económico',
                                  'Subordinado al Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado, en una economía social de mercado, '
                             'actúa por medio de:',
                 'alternativas': ['El control absoluto de empresas',
                                  'El sistema monetario y el ordenamiento '
                                  'jurídico',
                                  'La propiedad estatal de todo',
                                  'La eliminación del mercado',
                                  'La intervención directa en precios'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los principios del régimen económico '
                             'constitucional peruano figura la igualdad de '
                             'tratamiento al:',
                 'alternativas': ['Poder Ejecutivo',
                                  'Congreso',
                                  'Poder Judicial',
                                  'Estado',
                                  'Capital'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 58 de la Constitución establece '
                             'que la iniciativa privada es libre, ejercida '
                             'en una economía:',
                 'alternativas': ['Centralmente planificada',
                                  'De subsistencia',
                                  'Colectivizada',
                                  'Cerrada exclusiva',
                                  'Social de mercado'],
                 'correcta': 'E'},
                {'pregunta': 'El reconocimiento constitucional de las '
                             'libertades económicas en el Perú se inicia con '
                             'el texto de:',
                 'alternativas': ['1993', '1856', '1920', '1979', '1823'],
                 'correcta': 'E'},
                {'pregunta': 'La libertad de empresa comprende, entre otras '
                             'facultades, emprender, crear, organizar, '
                             'gestionar y:',
                 'alternativas': ['Cerrar la empresa',
                                  'Monopolizar el mercado',
                                  'Evitar la competencia',
                                  'Contaminar libremente',
                                  'Evadir impuestos'],
                 'correcta': 'A'},
                {'pregunta': 'La libertad de comercio se define como la '
                             'capacidad de mediar entre la oferta y:',
                 'alternativas': ['El Estado',
                                  'Los tratados internacionales',
                                  'El sistema tributario',
                                  'La banca central',
                                  'La demanda'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 59, el ejercicio de la '
                             'libertad de comercio no debe ser lesivo a la '
                             'moral, la salud o:',
                 'alternativas': ['Las utilidades',
                                  'El comercio exterior',
                                  'Los impuestos',
                                  'La seguridad pública',
                                  'Las ganancias'],
                 'correcta': 'D'},
                {'pregunta': 'La libertad de industria consiste en la '
                             'facultad de realizar operaciones para la '
                             'obtención o transformación de:',
                 'alternativas': ['Divisas exclusivas',
                                  'Capital financiero exclusivo',
                                  'Productos naturales',
                                  'Mano de obra exclusiva',
                                  'Servicios exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 65 de la Constitución establece un '
                             'deber especial de protección a:',
                 'alternativas': ['Los empresarios',
                                  'Los bancos',
                                  'Los inversionistas exclusivos',
                                  'El Estado exclusivamente',
                                  'Los consumidores y usuarios'],
                 'correcta': 'E'},
                {'pregunta': 'El tributo es el género, y sus especies son el '
                             'impuesto, la tasa y:',
                 'alternativas': ['La multa',
                                  'La contribución',
                                  'El interés',
                                  'La comisión',
                                  'El arancel exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El fundamento del impuesto es la capacidad:',
                 'alternativas': ['Legal',
                                  'Patrimonial exclusiva',
                                  'Contributiva',
                                  'Administrativa',
                                  'Comercial exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La recaudación de impuestos es controlada '
                             'mediante el principio de caja:',
                 'alternativas': ['Única',
                                  'Múltiple',
                                  'Regional',
                                  'Compartida',
                                  'Descentralizada'],
                 'correcta': 'A'},
                {'pregunta': 'La tasa tiene como hecho gravado un servicio '
                             'público:',
                 'alternativas': ['Colectivo exclusivo',
                                  'Gratuito exclusivo',
                                  'Voluntario',
                                  'Optativo',
                                  'Individualizado'],
                 'correcta': 'E'},
                {'pregunta': 'La contribución es el tributo cuya obligación '
                             'tiene como hecho generador beneficios '
                             'derivados de obras públicas o:',
                 'alternativas': ['Herencias',
                                  'Ventas privadas',
                                  'Donaciones',
                                  'Préstamos bancarios',
                                  'Actividades estatales'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 74, los tributos se crean, '
                             'modifican o derogan exclusivamente por ley o:',
                 'alternativas': ['Resolución ministerial',
                                  'Reglamento interno',
                                  'Decreto legislativo en caso de delegación',
                                  'Decreto supremo exclusivo',
                                  'Ordenanza municipal exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'Los gobiernos locales pueden crear, modificar '
                             'y suprimir contribuciones y tasas dentro de '
                             'su:',
                 'alternativas': ['Circunscripción electoral',
                                  'Jurisdicción',
                                  'Cartera ministerial',
                                  'Consejo Regional',
                                  'Presupuesto exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Ningún tributo puede tener efecto:',
                 'alternativas': ['Progresivo',
                                  'Regresivo',
                                  'Proporcional',
                                  'Confiscatorio',
                                  'Retroactivo exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 74, los decretos de urgencia '
                             'no pueden contener materia:',
                 'alternativas': ['Tributaria',
                                  'Ambiental',
                                  'Educativa',
                                  'Laboral exclusiva',
                                  'Presupuestaria exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'El principio de reserva de la ley establece '
                             'que solo por ley se puede determinar al '
                             'contribuyente y fijar:',
                 'alternativas': ['El lugar de pago',
                                  'El monto del tributo',
                                  'El banco receptor',
                                  'La fecha de pago exclusivamente',
                                  'El nombre del tributo'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que complementa la reserva de '
                             'ley, referido al uso del instrumento legal '
                             'permitido por su titular, se llama principio '
                             'de:',
                 'alternativas': ['Igualdad',
                                  'No confiscatoriedad',
                                  'Capacidad contributiva',
                                  'Proporcionalidad',
                                  'Legalidad'],
                 'correcta': 'E'},
                {'pregunta': 'El principio de igualdad tributaria establece '
                             'que situaciones iguales deben ser tratadas '
                             'igualmente y las situaciones desiguales:',
                 'alternativas': ['También igualmente',
                                  'De forma arbitraria',
                                  'Sin ningún criterio',
                                  'Desigualmente',
                                  'Con exención total'],
                 'correcta': 'D'},
                {'pregunta': 'En el régimen tributario, conforma un impuesto '
                             'indirecto: (IV CEPRU 2025-I)',
                 'alternativas': ['Impuesto General a las Ventas',
                                  'Impuesto a la Renta',
                                  'Impuesto al Patrimonio Vehicular',
                                  'Impuesto a la Venta de Arroz Pilado',
                                  'Impuesto a los Activos Netos'],
                 'correcta': 'A'},
                {'pregunta': '¿Cómo se llama el título de la Constitución '
                             'que regula la economía del país? (II CEPRU '
                             '2022-II)',
                 'alternativas': ['Régimen Económico',
                                  'Los Tributos',
                                  'Estructura del Estado',
                                  'Del Estado y la Nación',
                                  'De las Garantías Constitucionales'],
                 'correcta': 'A'},
                {'pregunta': 'La tercera vía entre el capitalismo y el '
                             'socialismo es la: (I CEPRU 2016-I)',
                 'alternativas': ['Economía Social de Mercado',
                                  'Economía Liberal',
                                  'Economía Subordinada',
                                  'Economía Transversal',
                                  'Economía Mixta Radical'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Según Sumar Albujar, el régimen económico '
                                'consiste en las normas o principios que '
                                'definen el rol del Estado en materia '
                                'económica.',
                                'Según Rodríguez Cairo, el régimen económico '
                                'se orienta a garantizar la gobernabilidad '
                                'de un país y contribuir al desempeño '
                                'económico.']},
                     {'titulo': 'LA CONSTITUCIÓN ECONÓMICA',
                      'items': ['Según García Belaúnde, la Constitución '
                                'Económica surgió en el periodo de '
                                'entreguerras, en la primera mitad del siglo '
                                'XX.',
                                'La Constitución de Weimar es considerada '
                                'pionera del constitucionalismo económico.',
                                'La Constitución de Weimar garantiza el '
                                'derecho de propiedad, aunque admite límites '
                                'por el bien general o función social.']},
                     {'titulo': 'LA ECONOMÍA SOCIAL DE MERCADO',
                      'items': ['La economía social de mercado es '
                                'representativa de los valores '
                                'constitucionales de libertad y justicia.',
                                'Según Herhärd y Müller Armack, este orden '
                                'asegura la competencia y transforma la '
                                'productividad individual en progreso '
                                'social.',
                                'La economía social de mercado combate la '
                                'formación de carteles y la concentración de '
                                'poder económico.',
                                'El mercado funciona de manera óptima cuando '
                                'el Estado establece normas claras sin '
                                'intervenir de manera permanente.',
                                'La práctica de la economía social de '
                                'mercado se refuerza por los principios de '
                                'solidaridad y subsidiaridad.',
                                'El principio de subsidiaridad establece que '
                                'lo que el individuo puede hacer por propia '
                                'iniciativa no debe hacerlo el Estado.']},
                     {'titulo': 'LIBERTADES ECONÓMICAS',
                      'items': ['El artículo 58 de la Constitución establece '
                                'que la iniciativa privada es libre, '
                                'ejercida en una economía social de mercado.',
                                'El reconocimiento constitucional de las '
                                'libertades económicas en el Perú se inicia '
                                'con el texto de 1823.',
                                'La libertad de empresa comprende la '
                                'facultad de emprender, crear, organizar, '
                                'gestionar, competir y cerrar una empresa.',
                                'La libertad de comercio es la capacidad de '
                                'mediar entre oferta y demanda para obtener '
                                'un beneficio económico.',
                                'Según el artículo 59, el ejercicio de la '
                                'libertad de comercio no debe ser lesivo a '
                                'la moral, la salud o la seguridad pública.',
                                'La libertad de industria es la facultad de '
                                'realizar operaciones destinadas a la '
                                'obtención o transformación de productos '
                                'naturales.',
                                'El artículo 65 de la Constitución establece '
                                'un deber especial de protección a los '
                                'consumidores y usuarios.']},
                     {'titulo': 'EL TRIBUTO Y SUS CLASES',
                      'items': ['El tributo es el concepto fundamental del '
                                'Derecho Tributario; el impuesto, la tasa y '
                                'la contribución son sus especies.',
                                'El impuesto es la categoría jurídica más '
                                'importante del tributo; su fundamento es la '
                                'capacidad contributiva.',
                                'La recaudación de impuestos es controlada '
                                'por el Tesoro Público del Ministerio de '
                                'Economía y Finanzas, mediante caja única.',
                                'La tasa tiene como hecho gravado un '
                                'servicio público individualizado; su '
                                'cuantía no debe exceder el gasto del '
                                'servicio.',
                                'La contribución es el tributo cuya '
                                'obligación tiene como hecho generador '
                                'beneficios derivados de obras públicas o '
                                'actividades estatales.']},
                     {'titulo': 'PRINCIPIOS DE LA POTESTAD TRIBUTARIA',
                      'items': ['El artículo 74 de la Constitución establece '
                                'que los tributos se crean, modifican o '
                                'derogan exclusivamente por ley o decreto '
                                'legislativo.',
                                'Los gobiernos locales pueden crear, '
                                'modificar y suprimir contribuciones y tasas '
                                'dentro de su jurisdicción.',
                                'Ningún tributo puede tener efecto '
                                'confiscatorio.',
                                'Los decretos de urgencia no pueden contener '
                                'materia tributaria.',
                                'El principio de reserva de la ley establece '
                                'que solo por ley se puede determinar al '
                                'contribuyente y fijar el monto del tributo.',
                                'El principio de legalidad complementa la '
                                'reserva de ley: el uso del instrumento '
                                'legal permitido por su respectivo titular.',
                                'El principio de igualdad tributaria '
                                'establece que situaciones iguales deben ser '
                                'tratadas igualmente y las desiguales, '
                                'desigualmente.']}],
  'qr_reto': [{'pregunta': 'El mercado y la competencia, según el texto, '
                           'deben garantizar la libertad de:',
               'respuesta': 'Consumidores, empleadores y trabajadores'},
              {'pregunta': 'La libertad de comercio se define como la '
                           'capacidad de mediar entre la oferta y:',
               'respuesta': 'La demanda'},
              {'pregunta': 'Entre los principios que rigen el régimen '
                           'económico peruano figura la libre:',
               'respuesta': 'Competencia'}],
  'qr_dato': 'La libertad de empresa comprende la facultad de emprender, '
             'crear, organizar, gestionar, competir y cerrar una empresa.'},
 {'num': 15,
  'titulo': 'Descentralización, Gobiernos Regionales y Gobiernos Locales',
  'secciones': [{'titulo': '15.1 CONCEPTO DE DESCENTRALIZACIÓN',
                 'items': ['La descentralización es un proceso '
                           '{político-técnico} que forma parte de la reforma '
                           'del Estado peruano, orientado a lograr un buen '
                           '{gobierno}.',
                           'Según Finot, la descentralización es un proceso '
                           'de transferencia organizada del gobierno '
                           '{nacional} a una autoridad subnacional o '
                           '{local}.',
                           'La descentralización busca mejorar la eficiencia '
                           'del Estado en la redistribución social, con '
                           'programas contra la {pobreza} y la corrupción.']},
                {'titulo': '15.2 OBJETIVOS DE LA DESCENTRALIZACIÓN',
                 'items': ['Entre los objetivos generales figura que cada '
                           'gobierno {regional} y local decida sobre sus '
                           'propios {recursos}.',
                           'Entre los objetivos políticos está la {unidad} y '
                           'eficiencia del Estado mediante la distribución '
                           'ordenada de competencias públicas.',
                           'Entre los objetivos económicos figura el '
                           'desarrollo económico {autosostenido} y de la '
                           'competitividad regional.',
                           'Otro objetivo económico es la redistribución '
                           '{equitativa} de los recursos del Estado.']},
                {'titulo': '15.3 ANTECEDENTES HISTÓRICOS',
                 'items': ['Los analistas coinciden en caracterizar al Perú '
                           'como un país históricamente {centralista}.',
                           'El primer periodo de descentralismo, llamado '
                           '«descentralismo {centralista}», se extiende '
                           'desde el inicio de la República hasta {1920}.',
                           'Los primeros proyectos de descentralización '
                           'provinieron del pensamiento {capitalino}, '
                           'elaborados por la élite política de Lima, por lo '
                           'que carecieron de respaldo social provinciano.',
                           'El periodo del {federalismo} fallido se ubica '
                           'entre 1821 y 1873.']},
                {'titulo': '15.4 ORGANIZACIÓN DE LOS GOBIERNOS REGIONALES',
                 'items': ['El {Consejo Regional} es el órgano normativo y '
                           '{fiscalizador} del Gobierno Regional, elegido '
                           'por sufragio directo por {4} años.',
                           'La {Presidencia Regional} es el órgano '
                           'ejecutivo; desde 2015 se le llama {Gobernador} '
                           'Regional.',
                           'El {Consejo de Coordinación Regional} es un '
                           'órgano consultivo integrado por alcaldes '
                           'provinciales y representantes de la sociedad '
                           '{civil}.',
                           'Las {ordenanzas regionales} norman asuntos de '
                           'carácter general; son dictadas por el Consejo '
                           'Regional.',
                           'Los {acuerdos regionales} expresan la decisión '
                           'del Consejo Regional sobre asuntos internos o de '
                           'interés {público}.',
                           'Los {decretos regionales} establecen normas '
                           'reglamentarias; son aprobados por la '
                           '{presidencia} regional.',
                           'Las {resoluciones regionales} norman asuntos de '
                           'carácter {administrativo}.']},
                {'titulo': '15.5 LOS GOBIERNOS LOCALES',
                 'items': ['Los {Gobiernos Locales} conforman el {tercer} '
                           'nivel de gobierno del Estado, elegidos por voto '
                           'popular.',
                           'Los Gobiernos Locales también se denominan '
                           '{municipalidades}, y pueden ser provinciales o '
                           '{distritales}.',
                           'Los {alcaldes} son elegidos por sufragio directo '
                           'por {4} años, en forma conjunta con los '
                           'regidores.',
                           'La estructura orgánica básica de las '
                           'municipalidades está compuesta por el {Concejo '
                           'Municipal} y la {Alcaldía}.',
                           'El {Concejo Municipal} está conformado por el '
                           'alcalde y los regidores, con funciones '
                           '{normativas} y fiscalizadoras.',
                           'La {Alcaldía} es el órgano ejecutivo; el alcalde '
                           'es el representante {legal} de la municipalidad.',
                           'El {Consejo de Coordinación Local} y las {Juntas '
                           'de Delegados Vecinales} son mecanismos de '
                           'participación ciudadana municipal.']}],
  'cuadros': [{'titulo': '15.2 TIPOS DE OBJETIVOS DE LA DESCENTRALIZACIÓN',
               'encabezados': ['Tipo', 'Ejemplo'],
               'filas': [['{Generales}',
                          'Que cada gobierno decida sobre sus {recursos}'],
                         ['{Políticos}', 'Unidad y eficiencia del {Estado}'],
                         ['{Económicos}',
                          'Redistribución {equitativa} de recursos']]}],
  'preguntas': [{'pregunta': 'La descentralización forma parte de la '
                             'reforma:',
                 'alternativas': ['Del sector privado',
                                  'Solo del sistema judicial',
                                  'Del sector financiero exclusivamente',
                                  'Solo del sistema educativo',
                                  'Del Estado peruano'],
                 'correcta': 'E'},
                {'pregunta': 'La descentralización busca alcanzar un '
                             'gobierno:',
                 'alternativas': ['Efectivo, eficiente y al servicio de la '
                                  'ciudadanía',
                                  'Centralizado y jerárquico',
                                  'Sin participación ciudadana',
                                  'Autoritario',
                                  'Exclusivamente militar'],
                 'correcta': 'A'},
                {'pregunta': 'Según Finot, la descentralización es un '
                             'proceso de transferencia desde el gobierno '
                             'nacional hacia:',
                 'alternativas': ['El sector privado',
                                  'Una autoridad subnacional o local',
                                  'Organismos internacionales',
                                  'Ningún otro nivel de gobierno',
                                  'Las Fuerzas Armadas'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización, según el texto, busca '
                             'reducir:',
                 'alternativas': ['La inversión privada',
                                  'La pobreza y la corrupción',
                                  'La participación ciudadana',
                                  'El desarrollo regional',
                                  'Los servicios públicos'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo general de la descentralización es '
                             'que cada gobierno regional y local:',
                 'alternativas': ['No participe en la gestión pública',
                                  'Se subordine a Lima',
                                  'Elimine su autonomía',
                                  'Decida sobre sus propios recursos',
                                  'Dependa del gobierno central para todo'],
                 'correcta': 'D'},
                {'pregunta': 'Un objetivo político de la descentralización '
                             'es:',
                 'alternativas': ['La unidad y eficiencia del Estado',
                                  'La centralización total',
                                  'El aislamiento regional',
                                  'La eliminación de gobiernos locales',
                                  'El debilitamiento del Estado'],
                 'correcta': 'A'},
                {'pregunta': 'Un objetivo económico de la descentralización '
                             'es:',
                 'alternativas': ['El desarrollo económico autosostenido de '
                                  'las regiones',
                                  'Reducir los servicios sociales',
                                  'Eliminar la inversión regional',
                                  'Concentrar recursos en Lima',
                                  'Aumentar la dependencia central'],
                 'correcta': 'A'},
                {'pregunta': 'Otro objetivo económico de la '
                             'descentralización es la redistribución:',
                 'alternativas': ['Solo para zonas urbanas',
                                  'Centralizada de los recursos',
                                  'Exclusiva para Lima',
                                  'Equitativa de los recursos del Estado',
                                  'Desigual de recursos'],
                 'correcta': 'D'},
                {'pregunta': 'Históricamente, el Perú ha sido caracterizado '
                             'por los analistas como un país:',
                 'alternativas': ['Centralista',
                                  'Federal',
                                  'Descentralizado desde su origen',
                                  'Sin estructura política definida',
                                  'Confederado'],
                 'correcta': 'A'},
                {'pregunta': 'El «descentralismo centralista» se extiende '
                             'desde el inicio de la República hasta:',
                 'alternativas': ['2002', '1920', '1821', '1993', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'provinieron principalmente de:',
                 'alternativas': ['Los movimientos indígenas',
                                  'Organismos internacionales',
                                  'El pensamiento capitalino, de la élite de '
                                  'Lima',
                                  'Los gobiernos regionales actuales',
                                  'Las provincias'],
                 'correcta': 'C'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'carecieron de:',
                 'alternativas': ['Apoyo internacional',
                                  'Presupuesto estatal',
                                  'Marco legal',
                                  'Respaldo social provinciano',
                                  'Interés político'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo del federalismo fallido en el Perú '
                             'se ubica entre:',
                 'alternativas': ['1900 y 1950',
                                  '1532 y 1821',
                                  '1993 y 2020',
                                  '1821 y 1873',
                                  '1979 y 1993'],
                 'correcta': 'D'},
                {'pregunta': 'La descentralización es descrita como un '
                             'proceso:',
                 'alternativas': ['Multidimensional, con dinámicas '
                                  'políticas, fiscales y administrativas',
                                  'Solo político',
                                  'Exclusivamente fiscal',
                                  'Solo administrativo',
                                  'Unidimensional'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los objetivos generales de la '
                             'descentralización figura la participación de:',
                 'alternativas': ['La sociedad civil',
                                  'Solo organismos internacionales',
                                  'Solo el gobierno central',
                                  'Solo las empresas privadas',
                                  'Solo el sector militar'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización busca la integración '
                             'entre el Estado y:',
                 'alternativas': ['Solo el sector privado',
                                  'Ningún actor social',
                                  'Solo organismos extranjeros',
                                  'La sociedad civil',
                                  'Solo las Fuerzas Armadas'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los objetivos políticos figura la '
                             'institucionalización de:',
                 'alternativas': ['Gobiernos centralizados',
                                  'Regímenes militares',
                                  'Gobiernos temporales',
                                  'Un solo partido político',
                                  'Sólidos gobiernos regionales y locales'],
                 'correcta': 'E'},
                {'pregunta': 'Un objetivo económico es la cobertura de '
                             'servicios sociales básicos en:',
                 'alternativas': ['Solo zonas fronterizas',
                                  'Solo la capital',
                                  'Todo el territorio nacional',
                                  'Solo zonas costeras',
                                  'Solo zonas urbanas'],
                 'correcta': 'C'},
                {'pregunta': 'El descentralismo formó parte de casi todos '
                             'los proyectos políticos, pero por razones '
                             'estructurales:',
                 'alternativas': ['Fueron rechazados por la población',
                                  'Se cumplieron totalmente',
                                  'No llegaron a concretarse',
                                  'Se aplicaron de inmediato',
                                  'No generaron ningún debate'],
                 'correcta': 'C'},
                {'pregunta': 'La descentralización tiene como finalidad el '
                             'desarrollo integral, armónico y:',
                 'alternativas': ['Temporal',
                                  'Exclusivo de Lima',
                                  'Limitado a la costa',
                                  'Solo económico',
                                  'Sostenible del país'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano normativo y fiscalizador del '
                             'Gobierno Regional se llama:',
                 'alternativas': ['Consejo de Coordinación Regional',
                                  'Consejo Regional',
                                  'Presidencia Regional',
                                  'Gerencia Regional',
                                  'Alcaldía Regional'],
                 'correcta': 'B'},
                {'pregunta': 'Los consejeros regionales son elegidos por '
                             'sufragio directo por un periodo de:',
                 'alternativas': ['Seis años',
                                  'Tres años',
                                  'Cuatro años',
                                  'Dos años',
                                  'Cinco años'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano ejecutivo del Gobierno Regional se '
                             'llama Presidencia Regional; desde 2015 al '
                             'presidente se le llama:',
                 'alternativas': ['Delegado Regional',
                                  'Prefecto',
                                  'Gobernador Regional',
                                  'Ministro Regional',
                                  'Alcalde Regional'],
                 'correcta': 'C'},
                {'pregunta': 'El Consejo de Coordinación Regional está '
                             'integrado por alcaldes provinciales y '
                             'representantes de:',
                 'alternativas': ['La sociedad civil',
                                  'El Congreso',
                                  'El Poder Judicial',
                                  'El Ejecutivo exclusivamente',
                                  'Otros gobiernos regionales '
                                  'exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Las normas que regulan asuntos de carácter '
                             'general del gobierno regional se llaman:',
                 'alternativas': ['Decretos regionales',
                                  'Ordenanzas regionales',
                                  'Directivas regionales',
                                  'Resoluciones regionales',
                                  'Acuerdos regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas que expresan la decisión del '
                             'Consejo Regional sobre asuntos internos se '
                             'llaman:',
                 'alternativas': ['Decretos regionales',
                                  'Acuerdos regionales',
                                  'Circulares regionales',
                                  'Ordenanzas regionales',
                                  'Resoluciones regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas reglamentarias para ejecutar las '
                             'ordenanzas regionales, aprobadas por la '
                             'presidencia regional, se llaman:',
                 'alternativas': ['Directivas',
                                  'Acuerdos regionales',
                                  'Resoluciones regionales',
                                  'Ordenanzas regionales',
                                  'Decretos regionales'],
                 'correcta': 'E'},
                {'pregunta': 'Los Gobiernos Locales conforman el nivel de '
                             'gobierno del Estado número:',
                 'alternativas': ['Tercero',
                                  'Cuarto',
                                  'Quinto',
                                  'Primero',
                                  'Segundo'],
                 'correcta': 'A'},
                {'pregunta': 'Los Gobiernos Locales también se denominan '
                             'municipalidades, y pueden ser provinciales o:',
                 'alternativas': ['Nacionales',
                                  'Regionales',
                                  'Departamentales',
                                  'Metropolitanas exclusivamente',
                                  'Distritales'],
                 'correcta': 'E'},
                {'pregunta': 'Los alcaldes son elegidos por sufragio directo '
                             'por un periodo de:',
                 'alternativas': ['Cuatro años',
                                  'Seis años',
                                  'Dos años',
                                  'Tres años',
                                  'Cinco años'],
                 'correcta': 'A'},
                {'pregunta': 'La estructura orgánica básica de las '
                             'municipalidades está compuesta por el Concejo '
                             'Municipal y:',
                 'alternativas': ['El Consejo Regional',
                                  'La Alcaldía',
                                  'La Junta Vecinal exclusiva',
                                  'El Consejo de Coordinación exclusivo',
                                  'La Gerencia General'],
                 'correcta': 'B'},
                {'pregunta': 'El Concejo Municipal está conformado por el '
                             'alcalde y:',
                 'alternativas': ['El gobernador regional',
                                  'Los regidores',
                                  'Los jueces de paz',
                                  'Los vecinos elegidos',
                                  'Los gerentes municipales'],
                 'correcta': 'B'},
                {'pregunta': 'La Alcaldía es el órgano ejecutivo del '
                             'gobierno local; el alcalde es el representante '
                             'legal y su:',
                 'alternativas': ['Consultor externo',
                                  'Fiscalizador',
                                  'Asesor jurídico',
                                  'Máxima autoridad administrativa',
                                  'Vocero exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'Los mecanismos de participación ciudadana '
                             'municipal incluyen el Consejo de Coordinación '
                             'Local y:',
                 'alternativas': ['La Fiscalía Municipal',
                                  'El Tribunal Municipal',
                                  'El Poder Judicial Local',
                                  'Las Juntas de Delegados Vecinales',
                                  'El Congreso Local'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano normativo y fiscalizador dentro de '
                             'la organización de los gobiernos regionales '
                             'es: (IV CEPRU 2025-I)',
                 'alternativas': ['El Consejo Regional',
                                  'La Gerencia Regional',
                                  'El Consejo de Coordinación',
                                  'La Secretaría Regional',
                                  'El Gobernador Regional'],
                 'correcta': 'A'},
                {'pregunta': 'La autoridad que puede ser revocada es: (II '
                             'CEPRU 2025-I)',
                 'alternativas': ['Los alcaldes',
                                  'Los senadores',
                                  'Los diputados',
                                  'Los jueces',
                                  'Los congresistas'],
                 'correcta': 'A'},
                {'pregunta': 'Como antecedente de la descentralización en el '
                             'Perú existieron grupos antagónicos en la '
                             'organización de un Estado eficiente, '
                             'denominados: (IV CEPRU 2022-II)',
                 'alternativas': ['Centralistas y caudillistas',
                                  'Regionalistas y centralistas',
                                  'Caudillistas y centralistas',
                                  'Federalistas y centralistas',
                                  'Caciquistas y federalistas'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE DESCENTRALIZACIÓN',
                      'items': ['La descentralización es un proceso '
                                'político-técnico que forma parte de la '
                                'reforma del Estado peruano, orientado a '
                                'lograr un buen gobierno.',
                                'Según Finot, la descentralización es un '
                                'proceso de transferencia organizada del '
                                'gobierno nacional a una autoridad '
                                'subnacional o local.',
                                'La descentralización busca mejorar la '
                                'eficiencia del Estado en la redistribución '
                                'social, con programas contra la pobreza y '
                                'la corrupción.']},
                     {'titulo': 'OBJETIVOS DE LA DESCENTRALIZACIÓN',
                      'items': ['Entre los objetivos generales figura que '
                                'cada gobierno regional y local decida sobre '
                                'sus propios recursos.',
                                'Entre los objetivos políticos está la '
                                'unidad y eficiencia del Estado mediante la '
                                'distribución ordenada de competencias '
                                'públicas.',
                                'Entre los objetivos económicos figura el '
                                'desarrollo económico autosostenido y de la '
                                'competitividad regional.',
                                'Otro objetivo económico es la '
                                'redistribución equitativa de los recursos '
                                'del Estado.']},
                     {'titulo': 'ANTECEDENTES HISTÓRICOS',
                      'items': ['Los analistas coinciden en caracterizar al '
                                'Perú como un país históricamente '
                                'centralista.',
                                'El primer periodo de descentralismo, '
                                'llamado «descentralismo centralista», se '
                                'extiende desde el inicio de la República '
                                'hasta 1920.',
                                'Los primeros proyectos de descentralización '
                                'provinieron del pensamiento capitalino, '
                                'elaborados por la élite política de Lima, '
                                'por lo que carecieron de respaldo social '
                                'provinciano.',
                                'El periodo del federalismo fallido se ubica '
                                'entre 1821 y 1873.']},
                     {'titulo': 'ORGANIZACIÓN DE LOS GOBIERNOS REGIONALES',
                      'items': ['El Consejo Regional es el órgano normativo '
                                'y fiscalizador del Gobierno Regional, '
                                'elegido por sufragio directo por 4 años.',
                                'La Presidencia Regional es el órgano '
                                'ejecutivo; desde 2015 se le llama '
                                'Gobernador Regional.',
                                'El Consejo de Coordinación Regional es un '
                                'órgano consultivo integrado por alcaldes '
                                'provinciales y representantes de la '
                                'sociedad civil.',
                                'Las ordenanzas regionales norman asuntos de '
                                'carácter general; son dictadas por el '
                                'Consejo Regional.',
                                'Los acuerdos regionales expresan la '
                                'decisión del Consejo Regional sobre asuntos '
                                'internos o de interés público.',
                                'Los decretos regionales establecen normas '
                                'reglamentarias; son aprobados por la '
                                'presidencia regional.',
                                'Las resoluciones regionales norman asuntos '
                                'de carácter administrativo.']},
                     {'titulo': 'LOS GOBIERNOS LOCALES',
                      'items': ['Los Gobiernos Locales conforman el tercer '
                                'nivel de gobierno del Estado, elegidos por '
                                'voto popular.',
                                'Los Gobiernos Locales también se denominan '
                                'municipalidades, y pueden ser provinciales '
                                'o distritales.',
                                'Los alcaldes son elegidos por sufragio '
                                'directo por 4 años, en forma conjunta con '
                                'los regidores.',
                                'La estructura orgánica básica de las '
                                'municipalidades está compuesta por el '
                                'Concejo Municipal y la Alcaldía.',
                                'El Concejo Municipal está conformado por el '
                                'alcalde y los regidores, con funciones '
                                'normativas y fiscalizadoras.',
                                'La Alcaldía es el órgano ejecutivo; el '
                                'alcalde es el representante legal de la '
                                'municipalidad.',
                                'El Consejo de Coordinación Local y las '
                                'Juntas de Delegados Vecinales son '
                                'mecanismos de participación ciudadana '
                                'municipal.']}],
  'qr_reto': [{'pregunta': 'El periodo del federalismo fallido en el Perú se '
                           'ubica entre:',
               'respuesta': '1821 y 1873'},
              {'pregunta': 'Históricamente, el Perú ha sido caracterizado '
                           'por los analistas como un país:',
               'respuesta': 'Centralista'},
              {'pregunta': 'Un objetivo general de la descentralización es '
                           'que cada gobierno regional y local:',
               'respuesta': 'Decida sobre sus propios recursos'}],
  'qr_dato': 'Los analistas coinciden en caracterizar al Perú como un país '
             'históricamente centralista.'},
 {'num': 16,
  'titulo': 'Derechos Humanos',
  'secciones': [{'titulo': '16.1 CONCEPTO',
                 'items': ['Los derechos humanos son libertades, facultades '
                           'e instituciones que incluyen a toda persona por '
                           'el simple hecho de su condición {humana}.',
                           'Según Hernández Gómez, los derechos humanos son '
                           'condiciones {instrumentales} que permiten a la '
                           'persona su realización.']},
                {'titulo': '16.2 CARACTERÍSTICAS DE LOS DERECHOS HUMANOS',
                 'items': ['Los derechos humanos son {universales}: se '
                           'aplican a todos los seres humanos sin '
                           'distinción.',
                           'Son {imprescriptibles}: no se pierden por el '
                           'transcurso del {tiempo}.',
                           'Son {indivisibles}: no puede hablarse de '
                           'división, todos deben ser {respetados}.',
                           'Son {inviolables}: nadie puede atentar contra '
                           'ellos; ni las leyes ni las políticas pueden ser '
                           '{contrarias} a estos derechos.',
                           'Son {irreversibles}: todo derecho reconocido '
                           'queda integrado de forma irrevocable a esta '
                           'categoría.',
                           'Son {indisolubles}: forman un conjunto '
                           'inseparable, con igual grado de {importancia}.',
                           'Son {obligatorios}: imponen al Estado el deber '
                           'de respetarlos aunque no exista una ley expresa.',
                           'Son {progresivos}: dado su carácter evolutivo, '
                           'en el futuro pueden reconocerse nuevos derechos '
                           'humanos.']},
                {'titulo': '16.3 DIMENSIONES DE LOS DERECHOS HUMANOS',
                 'items': ['Los derechos humanos pueden conceptualizarse '
                           'desde {cuatro} dimensiones: histórica, ética, '
                           'política y {jurídica}.',
                           'La dimensión {histórica} reconoce que los '
                           'derechos humanos tienen un pasado, presente y '
                           '{futuro}.',
                           'La dimensión {ética} se fundamenta en valores '
                           'como la dignidad humana y la {libertad}.',
                           'La dimensión {política} refiere a que los '
                           'derechos fueron proclamados por la {ONU} para '
                           'proteger a los seres humanos.',
                           'La dimensión {jurídica} refiere a que los '
                           'derechos aparecen en la Constitución como normas '
                           'de obligatorio {cumplimiento}.']},
                {'titulo': '16.4 EVOLUCIÓN: EL PRIMER MOMENTO O '
                           'JURIDIFICACIÓN',
                 'items': ['La evolución de los derechos humanos comprende '
                           'dos grandes momentos: la {juridificación} y la '
                           'internacionalización.',
                           'La Carta Magna, conocida como la Petición de los '
                           'Derechos, se dio en Inglaterra en el año {1215}.',
                           'La Ley de Habeas Corpus fue dictada en '
                           'Inglaterra en {1679}.',
                           'El Acta de Independencia de Estados Unidos data '
                           'de {1776}, y la Declaración de los Derechos del '
                           'Hombre y del Ciudadano, de Francia, de {1789}.']},
                {'titulo': '16.5 SEGUNDO MOMENTO: LA UNIVERSALIZACIÓN',
                 'items': ['El {segundo momento} en la evolución de los '
                           'derechos humanos es la {universalización}.',
                           'La universalización se plasma cuando la '
                           'comunidad internacional reconoce que la libertad '
                           'debe ser de {todos} los hombres, sin '
                           'discriminación.',
                           'Este momento se consolida con la Carta de San '
                           'Francisco de {1945} y la Declaración Universal '
                           'de los Derechos Humanos.',
                           'La Declaración Universal fue aprobada en la '
                           '{III} Asamblea General de las Naciones Unidas, '
                           'el {10} de diciembre de {1948}.']},
                {'titulo': '16.6 CLASIFICACIÓN POR GENERACIONES',
                 'items': ['La división de los derechos humanos en tres '
                           'generaciones fue propuesta en {1979} por el '
                           'jurista checo Karel {Vasak}.',
                           'Los {derechos de primera generación} se '
                           'establecieron desde el siglo XVIII a inicios del '
                           'XX; consideran a la persona como {individuo} con '
                           'libertad y autonomía.',
                           'Los derechos de primera generación también se '
                           'llaman derechos {civiles} y políticos; el más '
                           'importante es el derecho a la {vida}.',
                           'El Perú ratificó el Pacto Internacional de '
                           'Derechos Civiles y Políticos por Decreto Ley N° '
                           '22128, el {23} de marzo de {1976}.',
                           'Los {derechos de segunda generación} se '
                           'establecieron desde fines del siglo XIX hasta '
                           'mediados del XX; son derechos {económicos}, '
                           'sociales y culturales.',
                           'Los derechos de segunda generación situaron al '
                           'Estado Liberal en un {Estado Social} de Derecho.',
                           'Entre los derechos de segunda generación están '
                           'el derecho al trabajo, la libre {sindicación}, y '
                           'la protección de la {salud}.',
                           'Los {derechos de tercera generación}, o de '
                           '{solidaridad}, se reconocen a partir de la '
                           'década de {1980}.',
                           'Los titulares de los derechos de tercera '
                           'generación son sujetos {colectivos}: un pueblo, '
                           'una nación, una etnia.',
                           'Entre los derechos de tercera generación están '
                           'la autodeterminación de los pueblos, la '
                           'protección del {medio ambiente}, y el derecho a '
                           'la {paz}.']},
                {'titulo': '16.7 INSTRUMENTOS JURÍDICOS SUPRANACIONALES',
                 'items': ['La {Carta Internacional de los Derechos Humanos} '
                           'agrupa la Carta de la ONU (1945), la Declaración '
                           'Universal (1948), y los dos {Pactos} de 1966.',
                           'Otros documentos internacionales incluyen la '
                           'Convención contra el {Genocidio} (1948) y la '
                           'Convención contra la {Tortura} (1984).',
                           'La {Declaración Universal de los Derechos '
                           'Humanos} fue encargada a un comité de redacción '
                           'integrado por {ocho} expertos.',
                           'La Declaración Universal fue aprobada por la '
                           'Asamblea General de la ONU el {10} de diciembre '
                           'de {1948}.',
                           'La Declaración Universal consta de un preámbulo '
                           'y {30} artículos.']}],
  'cuadros': [{'titulo': '16.3 HITOS DEL PERIODO DE JURIDIFICACIÓN',
               'encabezados': ['Hito', 'País', 'Año'],
               'filas': [['{Carta Magna}', 'Inglaterra', '{1215}'],
                         ['Ley de {Habeas Corpus}', 'Inglaterra', '1679'],
                         ['Acta de {Independencia}', 'EE.UU.', '1776'],
                         ['Declaración de los Derechos del {Hombre}',
                          'Francia',
                          '1789']]}],
  'preguntas': [{'pregunta': 'Los derechos humanos incluyen a toda persona '
                             'por el simple hecho de:',
                 'alternativas': ['Su religión',
                                  'Su nivel económico',
                                  'Su nacionalidad',
                                  'Su condición humana',
                                  'Su edad'],
                 'correcta': 'D'},
                {'pregunta': 'Según Hernández Gómez, los derechos humanos '
                             'son condiciones que permiten a la persona:',
                 'alternativas': ['Su dependencia del Estado',
                                  'Su exclusión social',
                                  'Su aislamiento',
                                  'Su realización',
                                  'Su sometimiento'],
                 'correcta': 'D'},
                {'pregunta': 'Que los derechos humanos se apliquen a todos '
                             'sin distinción corresponde a la característica '
                             'de:',
                 'alternativas': ['Obligatoriedad',
                                  'Imprescriptibilidad',
                                  'Progresividad',
                                  'Universalidad',
                                  'Indivisibilidad'],
                 'correcta': 'D'},
                {'pregunta': 'Que los derechos humanos no se pierdan con el '
                             'paso del tiempo corresponde a que son:',
                 'alternativas': ['Imprescriptibles',
                                  'Inviolables',
                                  'Universales',
                                  'Progresivos',
                                  'Indisolubles'],
                 'correcta': 'A'},
                {'pregunta': 'Que no se pueda hablar de una división de los '
                             'derechos humanos corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Indivisibles',
                                  'Obligatorios',
                                  'Irreversibles',
                                  'Progresivos'],
                 'correcta': 'B'},
                {'pregunta': 'Que nadie pueda atentar contra los derechos '
                             'humanos corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Inviolables',
                                  'Progresivos',
                                  'Indisolubles',
                                  'Imprescriptibles'],
                 'correcta': 'B'},
                {'pregunta': 'Que un derecho reconocido quede integrado de '
                             'forma irrevocable corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Irreversibles',
                                  'Progresivos',
                                  'Obligatorios',
                                  'Indivisibles'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos formen un conjunto '
                             'inseparable corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Imprescriptibles',
                                  'Universales',
                                  'Inviolables',
                                  'Indisolubles'],
                 'correcta': 'E'},
                {'pregunta': 'Que el Estado deba respetar los derechos '
                             'humanos aunque no exista ley expresa '
                             'corresponde a que son:',
                 'alternativas': ['Irreversibles',
                                  'Universales',
                                  'Obligatorios',
                                  'Indivisibles',
                                  'Progresivos'],
                 'correcta': 'C'},
                {'pregunta': 'Que puedan reconocerse nuevos derechos humanos '
                             'en el futuro corresponde a que son:',
                 'alternativas': ['Inviolables',
                                  'Universales',
                                  'Imprescriptibles',
                                  'Progresivos',
                                  'Indisolubles'],
                 'correcta': 'D'},
                {'pregunta': 'La evolución de los derechos humanos comprende '
                             'dos grandes momentos: la juridificación y:',
                 'alternativas': ['La secularización',
                                  'La regionalización',
                                  'La militarización',
                                  'La privatización',
                                  'La internacionalización'],
                 'correcta': 'E'},
                {'pregunta': 'La Carta Magna, o Petición de los Derechos, se '
                             'dio en Inglaterra en el año:',
                 'alternativas': ['1215', '1789', '1948', '1776', '1679'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de Habeas Corpus fue dictada en '
                             'Inglaterra en:',
                 'alternativas': ['1215', '1789', '1948', '1679', '1776'],
                 'correcta': 'D'},
                {'pregunta': 'El Acta de Independencia de Estados Unidos '
                             'data de:',
                 'alternativas': ['1776', '1789', '1948', '1679', '1215'],
                 'correcta': 'A'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano corresponde a:',
                 'alternativas': ['España, 1812',
                                  'Francia, 1789',
                                  'Estados Unidos, 1776',
                                  'Inglaterra, 1215',
                                  'Alemania, 1919'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de juridificación se caracteriza '
                             'porque los nuevos Estados modernos:',
                 'alternativas': ['Eliminaron toda garantía legal',
                                  'Rechazaron los derechos humanos',
                                  'Prohibieron su difusión',
                                  'Introdujeron el reconocimiento y '
                                  'protección de estos derechos en sus '
                                  'legislaciones',
                                  'Centralizaron el poder absoluto'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de juridificación estuvo imbuido de '
                             'la ideología:',
                 'alternativas': ['Absolutista',
                                  'Monárquica',
                                  'Liberal',
                                  'Socialista',
                                  'Conservadora'],
                 'correcta': 'C'},
                {'pregunta': 'El ejercicio de rebeliones históricas para '
                             'lograr el reconocimiento de derechos demuestra '
                             'que estos son, en parte:',
                 'alternativas': ['Producto de un proceso histórico y social',
                                  'Ajenos a la evolución humana',
                                  'Otorgados sin lucha por el Estado',
                                  'Impuestos por organismos internacionales',
                                  'Exclusivos de una nación'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho a la vida, como derecho inviolable, '
                             'no puede ser violentado:',
                 'alternativas': ['En ninguna circunstancia',
                                  'Solo en situaciones de guerra',
                                  'Bajo excepciones económicas',
                                  'Solo por decisión judicial',
                                  'Solo temporalmente'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos humanos, según su carácter '
                             'obligatorio, deben respetarse:',
                 'alternativas': ['Aunque no exista una ley que lo diga '
                                  'expresamente',
                                  'Solo si están en la ley nacional',
                                  'Solo en situaciones normales',
                                  'Solo si lo exige un tratado',
                                  'Solo por decisión del gobierno de turno'],
                 'correcta': 'A'},
                {'pregunta': 'La división de los derechos humanos en tres '
                             'generaciones fue propuesta en 1979 por:',
                 'alternativas': ['John Rawls',
                                  'Hans Kelsen',
                                  'Karel Vasak',
                                  'Rousseau',
                                  'Norberto Bobbio'],
                 'correcta': 'C'},
                {'pregunta': 'Los derechos de primera generación consideran '
                             'a la persona como:',
                 'alternativas': ['Un pueblo indígena',
                                  'Un individuo con libertad y autonomía',
                                  'Un sujeto colectivo',
                                  'Una nación',
                                  'Un grupo social'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de primera generación también se '
                             'conocen como derechos:',
                 'alternativas': ['De solidaridad',
                                  'Económicos y sociales',
                                  'Colectivos',
                                  'Civiles y políticos',
                                  'Difusos'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho más importante entre los de primera '
                             'generación es el derecho a:',
                 'alternativas': ['El trabajo',
                                  'La vida',
                                  'La paz',
                                  'La propiedad',
                                  'La sindicación'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú ratificó el Pacto Internacional de '
                             'Derechos Civiles y Políticos mediante Decreto '
                             'Ley N°:',
                 'alternativas': ['27444',
                                  '22128',
                                  '26300',
                                  '28237',
                                  '25278'],
                 'correcta': 'C'},
                {'pregunta': 'Los derechos de segunda generación son '
                             'derechos económicos, sociales y:',
                 'alternativas': ['Culturales',
                                  'De solidaridad exclusiva',
                                  'Ambientales exclusivos',
                                  'Colectivos exclusivos',
                                  'Difusos'],
                 'correcta': 'A'},
                {'pregunta': 'La instauración de los derechos de segunda '
                             'generación provocó la sustitución del Estado '
                             'Liberal por el Estado:',
                 'alternativas': ['Totalitario',
                                  'Militar',
                                  'Absolutista',
                                  'Social de Derecho',
                                  'Confesional'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los derechos de segunda generación está '
                             'el derecho al trabajo y a la libre:',
                 'alternativas': ['Religión',
                                  'Sindicación',
                                  'Herencia',
                                  'Emigración',
                                  'Propiedad'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de tercera generación también se '
                             'llaman derechos de:',
                 'alternativas': ['Autonomía individual',
                                  'Solidaridad',
                                  'Propiedad',
                                  'Igualdad',
                                  'Libertad'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de tercera generación se '
                             'reconocen a partir de la década de:',
                 'alternativas': ['1970', '1960', '1980', '1990', '1945'],
                 'correcta': 'C'},
                {'pregunta': 'Los titulares de los derechos de tercera '
                             'generación son sujetos:',
                 'alternativas': ['Religiosos exclusivos',
                                  'Individuales exclusivamente',
                                  'Colectivos',
                                  'Empresariales',
                                  'Estatales exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los derechos de tercera generación está '
                             'la autodeterminación de los pueblos y la '
                             'protección de:',
                 'alternativas': ['La banca',
                                  'El medio ambiente',
                                  'Las telecomunicaciones',
                                  'La propiedad privada',
                                  'El comercio'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos humanos pueden conceptualizarse '
                             'desde cuatro dimensiones: histórica, ética, '
                             'política y:',
                 'alternativas': ['Social exclusiva',
                                  'Jurídica',
                                  'Cultural exclusiva',
                                  'Económica',
                                  'Religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'La dimensión de los derechos humanos que se '
                             'fundamenta en valores como la dignidad y la '
                             'libertad se llama dimensión:',
                 'alternativas': ['Política',
                                  'Histórica',
                                  'Social',
                                  'Jurídica',
                                  'Ética'],
                 'correcta': 'E'},
                {'pregunta': 'La dimensión de los derechos humanos que '
                             'refiere a su proclamación por la ONU se llama '
                             'dimensión:',
                 'alternativas': ['Política',
                                  'Ética',
                                  'Económica',
                                  'Jurídica',
                                  'Histórica'],
                 'correcta': 'A'},
                {'pregunta': 'El segundo momento en la evolución de los '
                             'derechos humanos, tras la juridificación, se '
                             'llama:',
                 'alternativas': ['Regionalización',
                                  'Privatización',
                                  'Universalización',
                                  'Descentralización',
                                  'Constitucionalización'],
                 'correcta': 'C'},
                {'pregunta': 'La universalización de los derechos humanos se '
                             'consolida con la Carta de San Francisco de '
                             '1945 y:',
                 'alternativas': ['La Carta Magna',
                                  'La Convención de Ginebra exclusiva',
                                  'La Declaración Universal de los Derechos '
                                  'Humanos',
                                  'El Tratado de Versalles',
                                  'El Pacto de Varsovia'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos fue aprobada en la Asamblea General de '
                             'la ONU el 10 de diciembre de:',
                 'alternativas': ['1989', '1966', '1979', '1948', '1945'],
                 'correcta': 'D'},
                {'pregunta': 'La Carta Internacional de los Derechos Humanos '
                             'incluye la Carta de la ONU, la Declaración '
                             'Universal y:',
                 'alternativas': ['Solo la Carta Magna',
                                  'Solo tratados regionales',
                                  'La Convención de Viena exclusiva',
                                  'Los dos Pactos Internacionales de 1966',
                                  'Solo el Habeas Corpus'],
                 'correcta': 'D'},
                {'pregunta': 'La Convención Internacional para la prevención '
                             'y sanción del crimen de genocidio data de:',
                 'alternativas': ['1966', '1984', '1979', '1948', '1945'],
                 'correcta': 'D'},
                {'pregunta': 'La Convención contra la Tortura y otros tratos '
                             'crueles data de:',
                 'alternativas': ['1984', '1966', '1948', '1952', '1960'],
                 'correcta': 'A'},
                {'pregunta': 'La elaboración de la Declaración Universal de '
                             'los Derechos Humanos fue encargada a un comité '
                             'de redacción integrado por un número de '
                             'expertos igual a:',
                 'alternativas': ['Quince', 'Diez', 'Ocho', 'Cinco', 'Tres'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos consta de un preámbulo y un número de '
                             'artículos igual a:',
                 'alternativas': ['20', '40', '30', '50', '25'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos se aprobó el: (IV CEPRU 2025-I)',
                 'alternativas': ['10 de diciembre de 1948',
                                  '02 de mayo de 1948',
                                  '26 de junio de 1945',
                                  '24 de octubre de 1945',
                                  '22 de noviembre de 1969'],
                 'correcta': 'A'},
                {'pregunta': 'Los idiomas oficiales de la Corte '
                             'Internacional de Justicia son: (IV CEPRU '
                             '2025-I)',
                 'alternativas': ['Inglés y francés',
                                  'Portugués e inglés',
                                  'Ruso y español',
                                  'Inglés y español',
                                  'Inglés y chino'],
                 'correcta': 'A'},
                {'pregunta': 'Dentro de los instrumentos supranacionales de '
                             'protección de derechos humanos tenemos: (IV '
                             'CEPRU 2025-I)',
                 'alternativas': ['La Declaración Africana de los Derechos '
                                  'del Hombre y Ciudadano',
                                  'La Declaración Interamericana de los '
                                  'Derechos Humanos',
                                  'El Pacto Internacional de los Derechos '
                                  'Civiles y Políticos',
                                  'La Carta Magna de Juan Sin Tierra',
                                  'El Pacto Americano de los Derechos '
                                  'Económicos, Sociales y Culturales'],
                 'correcta': 'C'},
                {'pregunta': 'Son un conjunto de bienes materiales heredados '
                             'como legado, transmitidos a futuras '
                             'generaciones a lo largo de la historia: (I '
                             'CEPRU 2023-II)',
                 'alternativas': ['Patrimonio material',
                                  'Patrimonio inmaterial',
                                  'Fuentes culturales',
                                  'Patrimonio natural',
                                  'Patrimonio cultural'],
                 'correcta': 'A'},
                {'pregunta': 'En la clasificación de los Derechos Humanos, '
                             'el derecho a la protección de la salud '
                             'pertenece a la generación: (IV CEPRU 2022-I)',
                 'alternativas': ['Segunda',
                                  'Primera',
                                  'Tercera',
                                  'Cuarta',
                                  'Quinta'],
                 'correcta': 'A'},
                {'pregunta': 'Los Derechos Humanos de tercera generación '
                             'reconocen el derecho a la: (II CEPRU 2022-I)',
                 'alternativas': ['Paz y protección del medio ambiente',
                                  'Libre sindicación y protección de la '
                                  'salud',
                                  'Propiedad y herencia',
                                  'Igualdad ante la ley y libertad de '
                                  'conciencia',
                                  'Libertad y seguridad personal'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Los derechos humanos son libertades, '
                                'facultades e instituciones que incluyen a '
                                'toda persona por el simple hecho de su '
                                'condición humana.',
                                'Según Hernández Gómez, los derechos humanos '
                                'son condiciones instrumentales que permiten '
                                'a la persona su realización.']},
                     {'titulo': 'CARACTERÍSTICAS DE LOS DERECHOS HUMANOS',
                      'items': ['Los derechos humanos son universales: se '
                                'aplican a todos los seres humanos sin '
                                'distinción.',
                                'Son imprescriptibles: no se pierden por el '
                                'transcurso del tiempo.',
                                'Son indivisibles: no puede hablarse de '
                                'división, todos deben ser respetados.',
                                'Son inviolables: nadie puede atentar contra '
                                'ellos; ni las leyes ni las políticas pueden '
                                'ser contrarias a estos derechos.',
                                'Son irreversibles: todo derecho reconocido '
                                'queda integrado de forma irrevocable a esta '
                                'categoría.',
                                'Son indisolubles: forman un conjunto '
                                'inseparable, con igual grado de '
                                'importancia.']},
                     {'titulo': 'DIMENSIONES DE LOS DERECHOS HUMANOS',
                      'items': ['Los derechos humanos pueden '
                                'conceptualizarse desde cuatro dimensiones: '
                                'histórica, ética, política y jurídica.',
                                'La dimensión histórica reconoce que los '
                                'derechos humanos tienen un pasado, presente '
                                'y futuro.',
                                'La dimensión ética se fundamenta en valores '
                                'como la dignidad humana y la libertad.',
                                'La dimensión política refiere a que los '
                                'derechos fueron proclamados por la ONU para '
                                'proteger a los seres humanos.',
                                'La dimensión jurídica refiere a que los '
                                'derechos aparecen en la Constitución como '
                                'normas de obligatorio cumplimiento.']},
                     {'titulo': 'EVOLUCIÓN: EL PRIMER MOMENTO O '
                                'JURIDIFICACIÓN',
                      'items': ['La evolución de los derechos humanos '
                                'comprende dos grandes momentos: la '
                                'juridificación y la internacionalización.',
                                'La Carta Magna, conocida como la Petición '
                                'de los Derechos, se dio en Inglaterra en el '
                                'año 1215.',
                                'La Ley de Habeas Corpus fue dictada en '
                                'Inglaterra en 1679.',
                                'El Acta de Independencia de Estados Unidos '
                                'data de 1776, y la Declaración de los '
                                'Derechos del Hombre y del Ciudadano, de '
                                'Francia, de 1789.']},
                     {'titulo': 'SEGUNDO MOMENTO: LA UNIVERSALIZACIÓN',
                      'items': ['El segundo momento en la evolución de los '
                                'derechos humanos es la universalización.',
                                'La universalización se plasma cuando la '
                                'comunidad internacional reconoce que la '
                                'libertad debe ser de todos los hombres, sin '
                                'discriminación.',
                                'Este momento se consolida con la Carta de '
                                'San Francisco de 1945 y la Declaración '
                                'Universal de los Derechos Humanos.',
                                'La Declaración Universal fue aprobada en la '
                                'III Asamblea General de las Naciones '
                                'Unidas, el 10 de diciembre de 1948.']},
                     {'titulo': 'CLASIFICACIÓN POR GENERACIONES',
                      'items': ['La división de los derechos humanos en tres '
                                'generaciones fue propuesta en 1979 por el '
                                'jurista checo Karel Vasak.',
                                'Los derechos de primera generación se '
                                'establecieron desde el siglo XVIII a '
                                'inicios del XX; consideran a la persona '
                                'como individuo con libertad y autonomía.',
                                'Los derechos de primera generación también '
                                'se llaman derechos civiles y políticos; el '
                                'más importante es el derecho a la vida.',
                                'El Perú ratificó el Pacto Internacional de '
                                'Derechos Civiles y Políticos por Decreto '
                                'Ley N° 22128, el 23 de marzo de 1976.',
                                'Los derechos de segunda generación se '
                                'establecieron desde fines del siglo XIX '
                                'hasta mediados del XX; son derechos '
                                'económicos, sociales y culturales.',
                                'Los derechos de segunda generación situaron '
                                'al Estado Liberal en un Estado Social de '
                                'Derecho.']},
                     {'titulo': 'INSTRUMENTOS JURÍDICOS SUPRANACIONALES',
                      'items': ['La Carta Internacional de los Derechos '
                                'Humanos agrupa la Carta de la ONU (1945), '
                                'la Declaración Universal (1948), y los dos '
                                'Pactos de 1966.',
                                'Otros documentos internacionales incluyen '
                                'la Convención contra el Genocidio (1948) y '
                                'la Convención contra la Tortura (1984).',
                                'La Declaración Universal de los Derechos '
                                'Humanos fue encargada a un comité de '
                                'redacción integrado por ocho expertos.',
                                'La Declaración Universal fue aprobada por '
                                'la Asamblea General de la ONU el 10 de '
                                'diciembre de 1948.',
                                'La Declaración Universal consta de un '
                                'preámbulo y 30 artículos.']}],
  'qr_reto': [{'pregunta': 'La Carta Internacional de los Derechos Humanos '
                           'incluye la Carta de la ONU, la Declaración '
                           'Universal y:',
               'respuesta': 'Los dos Pactos Internacionales de 1966'},
              {'pregunta': 'La Convención Internacional para la prevención y '
                           'sanción del crimen de genocidio data de:',
               'respuesta': '1948'},
              {'pregunta': 'El derecho a la vida, como derecho inviolable, '
                           'no puede ser violentado:',
               'respuesta': 'En ninguna circunstancia'}],
  'qr_dato': 'La división de los derechos humanos en tres generaciones fue '
             'propuesta en 1979 por el jurista checo Karel Vasak.'},
 {'num': 17,
  'titulo': 'Garantías Constitucionales',
  'secciones': [{'titulo': '17.1 CONCEPTO Y ANTECEDENTES',
                 'items': ['El término {garantía} se define como la '
                           'seguridad o protección frente a un peligro en el '
                           'disfrute de los derechos.',
                           'Las Garantías Constitucionales tienen su origen '
                           'en la tradición {francesa}.',
                           'En el Perú, la institucionalidad de las '
                           'garantías se inicia con la Constitución de '
                           '{1920}, que distinguió garantías nacionales, '
                           'individuales y {sociales}.',
                           'Según García Toma, las Garantías '
                           'Constitucionales son el conjunto de '
                           'declaraciones, medios y recursos que aseguran el '
                           'disfrute de los derechos {públicos} y '
                           'privados.']},
                {'titulo': '17.2 LAS SEIS GARANTÍAS EN LA CONSTITUCIÓN DE '
                           '1993',
                 'items': ['El artículo {200} de la Constitución de 1993 '
                           'establece {seis} Garantías Constitucionales.',
                           'La Constitución de 1920 reconoció el {Habeas '
                           'Corpus}; la de 1933 sumó la {Acción Popular}.',
                           'La Constitución de 1979 sumó la Acción de '
                           '{Amparo} y la Acción de Inconstitucionalidad.',
                           'La Constitución de 1993 sumó el {Habeas Data} y '
                           'la Acción de {Cumplimiento}.']},
                {'titulo': '17.3 LA ACCIÓN DE HABEAS CORPUS',
                 'items': ['La expresión «habeas corpus», de origen latino, '
                           'significa literalmente «que traigas el '
                           '{cuerpo}».',
                           'El antecedente del habeas corpus es la ley '
                           'inglesa de {1679}.',
                           'En el Perú, el habeas corpus fue regulado por '
                           'primera vez en la Constitución de {1920}.',
                           'El habeas corpus protege la {libertad} '
                           'individual y la seguridad personal, y derechos '
                           'constitucionales {conexos}.',
                           'El habeas corpus se presenta ante el Juez '
                           'especializado en lo {Penal}, o ante el Juez de '
                           'Paz Letrado si no lo hay.',
                           'El {Tribunal Constitucional} es, de forma '
                           'extraordinaria, la última y definitiva instancia '
                           'para resolver las resoluciones denegatorias del '
                           'habeas corpus.',
                           'La acción de habeas corpus está exenta de '
                           '{formalidades}: no requiere poder, tasas '
                           'judiciales ni firma de letrado.']},
                {'titulo': '17.4 LA ACCIÓN DE AMPARO',
                 'items': ['La {Acción de Amparo} fue introducida por '
                           'primera vez en la Constitución de {1979}, como '
                           'garantía distinta al hábeas corpus.',
                           'El Amparo protege todos los derechos '
                           'constitucionales, excepto los protegidos por '
                           'hábeas corpus y hábeas {data}.',
                           'El Amparo tiene por objeto reponer las cosas al '
                           'estado {anterior} a la violación de un derecho.',
                           'La demanda de Amparo se presenta ante el Juez '
                           'especializado en lo {civil}.',
                           'El plazo para presentar el Amparo es de {60} '
                           'días desde la vulneración, y {30} días en '
                           'sentencias judiciales.',
                           'El Amparo requiere formalismo: se presenta por '
                           'escrito con autorización de {abogado}.',
                           'El Amparo no procede contra normas legales ni '
                           'contra resoluciones judiciales de procedimiento '
                           '{regular}.']},
                {'titulo': '17.5 LA ACCIÓN DE HÁBEAS DATA',
                 'items': ['El {Hábeas Data} fue introducido por la '
                           'Constitución de {1993}, para proteger frente al '
                           'abuso de la informática.',
                           'El Hábeas Data protege el derecho a solicitar y '
                           'recibir {información}, y la protección de la '
                           'intimidad personal y {familiar}.',
                           'El plazo para presentar el Hábeas Data es de '
                           '{60} días hábiles después de la respuesta '
                           '{denegatoria}.',
                           'El Hábeas Data no procede sobre información de '
                           '{Defensa Nacional}, secreto bancario, y '
                           '{telecomunicaciones}.']},
                {'titulo': '17.6 LA ACCIÓN DE INCONSTITUCIONALIDAD',
                 'items': ['La {Acción de Inconstitucionalidad} se crea con '
                           'la Constitución de {1979}; procede contra normas '
                           'de rango de ley.',
                           'Es la única garantía que se presenta en '
                           '{instancia única} y definitiva ante el {Tribunal '
                           'Constitucional}.',
                           'Están facultados para interponerla, entre otros, '
                           'el Presidente, el Fiscal de la Nación, y el '
                           '{25}% de congresistas.',
                           'También puede interponerla un grupo de {5000} '
                           'ciudadanos con firmas comprobadas por el JNE.',
                           'El plazo para interponerla es de {6} años desde '
                           'su publicación, y 6 meses para tratados '
                           'internacionales.',
                           'Se requiere el voto a favor de {5} magistrados '
                           'del Tribunal Constitucional.']},
                {'titulo': '17.7 LA ACCIÓN POPULAR Y DE CUMPLIMIENTO',
                 'items': ['La {Acción Popular} se originó en la justicia '
                           'romana; se introdujo por primera vez en la '
                           'Constitución de {1933}.',
                           'La Acción Popular procede contra normas de rango '
                           'de decretos y {resoluciones}, y es competencia '
                           'exclusiva del Poder {Judicial}.',
                           'El plazo para la Acción Popular es de {5} años '
                           'desde su publicación.',
                           'La {Acción de Cumplimiento} fue creada por la '
                           'Constitución de {1993}, para hacer cumplir '
                           'normas legales o actos administrativos.',
                           'El plazo para la Acción de Cumplimiento es de '
                           '{60} días después de no cumplirse el mandato.']}],
  'cuadros': [{'titulo': '17.2 EVOLUCIÓN DE LAS GARANTÍAS POR CONSTITUCIÓN',
               'encabezados': ['Constitución', 'Garantía incorporada'],
               'filas': [['{1920}', '{Habeas Corpus}'],
                         ['{1933}', '{Acción Popular}'],
                         ['{1979}', 'Amparo e {Inconstitucionalidad}'],
                         ['{1993}', 'Habeas Data y {Cumplimiento}']]}],
  'preguntas': [{'pregunta': 'El término «garantía» se define como la '
                             'seguridad o protección frente a:',
                 'alternativas': ['Un beneficio',
                                  'Un peligro en el disfrute de los derechos',
                                  'Una sanción administrativa',
                                  'Una obligación tributaria',
                                  'Un contrato civil'],
                 'correcta': 'B'},
                {'pregunta': 'Las Garantías Constitucionales tienen su '
                             'origen en la tradición:',
                 'alternativas': ['Española',
                                  'Alemana',
                                  'Francesa',
                                  'Romana',
                                  'Inglesa'],
                 'correcta': 'C'},
                {'pregunta': 'En el Perú, la institucionalidad de las '
                             'garantías se inicia con la Constitución de:',
                 'alternativas': ['1993', '1979', '1920', '1933', '1856'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución de 1920 distinguió tres tipos '
                             'de garantías: nacionales, individuales y:',
                 'alternativas': ['Militares',
                                  'Económicas',
                                  'Sociales',
                                  'Religiosas',
                                  'Culturales'],
                 'correcta': 'C'},
                {'pregunta': 'Según García Toma, las Garantías '
                             'Constitucionales aseguran el disfrute de los '
                             'derechos:',
                 'alternativas': ['Públicos y privados',
                                  'Solo privados',
                                  'Solo económicos',
                                  'Solo públicos',
                                  'Solo políticos'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'establece las Garantías Constitucionales es '
                             'el:',
                 'alternativas': ['Artículo 200',
                                  'Artículo 51',
                                  'Artículo 91',
                                  'Artículo 149',
                                  'Artículo 24'],
                 'correcta': 'A'},
                {'pregunta': 'El número de Garantías Constitucionales '
                             'establecidas en el artículo 200 es:',
                 'alternativas': ['Ocho', 'Diez', 'Seis', 'Cuatro', 'Tres'],
                 'correcta': 'C'},
                {'pregunta': 'La primera garantía constitucional reconocida '
                             'en el Perú, en 1920, fue:',
                 'alternativas': ['El Habeas Corpus',
                                  'El Habeas Data',
                                  'La Acción de Cumplimiento',
                                  'La Acción Popular',
                                  'La Acción de Amparo'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción Popular fue incorporada en la '
                             'Constitución de:',
                 'alternativas': ['1979', '1993', '1933', '1920', '1856'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Amparo y la Acción de '
                             'Inconstitucionalidad se incorporaron en la '
                             'Constitución de:',
                 'alternativas': ['1979', '1933', '1993', '1856', '1920'],
                 'correcta': 'A'},
                {'pregunta': 'El Habeas Data y la Acción de Cumplimiento se '
                             'incorporaron en la Constitución de:',
                 'alternativas': ['1993', '1979', '1933', '1920', '1856'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión «habeas corpus» significa '
                             'literalmente:',
                 'alternativas': ['Justicia inmediata',
                                  'Que traigas el cuerpo',
                                  'Libertad total',
                                  'Derecho supremo',
                                  'Protege al pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'El antecedente histórico del habeas corpus es '
                             'la ley inglesa de:',
                 'alternativas': ['1215', '1948', '1993', '1789', '1679'],
                 'correcta': 'E'},
                {'pregunta': 'El habeas corpus protege principalmente:',
                 'alternativas': ['La libertad de prensa únicamente',
                                  'La propiedad privada',
                                  'La libertad individual y la seguridad '
                                  'personal',
                                  'Los derechos laborales exclusivamente',
                                  'El comercio exterior'],
                 'correcta': 'C'},
                {'pregunta': 'El habeas corpus se presenta, en primera '
                             'instancia, ante:',
                 'alternativas': ['El Ministerio Público',
                                  'El Congreso',
                                  'El Juez especializado en lo Penal',
                                  'La Defensoría del Pueblo',
                                  'El Tribunal Constitucional'],
                 'correcta': 'C'},
                {'pregunta': 'Si no hay Juez Penal disponible, el habeas '
                             'corpus se presenta ante:',
                 'alternativas': ['El Defensor del Pueblo',
                                  'El Alcalde',
                                  'El Juez de Paz Letrado',
                                  'El Presidente de la Corte Suprema',
                                  'El Fiscal de la Nación'],
                 'correcta': 'C'},
                {'pregunta': 'La última y definitiva instancia para resolver '
                             'denegatorias de habeas corpus es:',
                 'alternativas': ['El Ministerio Público',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'La Corte Suprema',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'La acción de habeas corpus se caracteriza por '
                             'estar exenta de:',
                 'alternativas': ['Formalidades',
                                  'Competencia territorial',
                                  'Revisión judicial',
                                  'Plazos procesales',
                                  'Sustento fáctico'],
                 'correcta': 'A'},
                {'pregunta': 'Para presentar un habeas corpus NO se '
                             'requiere:',
                 'alternativas': ['Presentar el escrito ante juez competente',
                                  'Un hecho vulnerador',
                                  'Poder, tasas judiciales ni firma de '
                                  'letrado',
                                  'Señalar el derecho vulnerado',
                                  'Identificar a la autoridad responsable'],
                 'correcta': 'C'},
                {'pregunta': 'El habeas corpus puede formularse:',
                 'alternativas': ['Exclusivamente por vía electrónica',
                                  'Solo por escrito con abogado',
                                  'Por escrito o verbalmente, en forma '
                                  'directa o por correo',
                                  'Solo mediante representante legal',
                                  'Únicamente en audiencia pública'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Amparo fue introducida por '
                             'primera vez, como garantía distinta al hábeas '
                             'corpus, en la Constitución de:',
                 'alternativas': ['1993', '1933', '1856', '1920', '1979'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción de Amparo protege todos los derechos '
                             'constitucionales, excepto los protegidos por '
                             'hábeas corpus y:',
                 'alternativas': ['Hábeas data',
                                  'Acción popular',
                                  'Cumplimiento',
                                  'Proceso competencial',
                                  'Inconstitucionalidad'],
                 'correcta': 'A'},
                {'pregunta': 'El plazo para presentar la Acción de Amparo es '
                             'de 60 días desde la vulneración del derecho, '
                             'salvo en sentencias judiciales, donde el plazo '
                             'es de:',
                 'alternativas': ['90 días',
                                  '45 días',
                                  '15 días',
                                  '30 días',
                                  '10 días'],
                 'correcta': 'D'},
                {'pregunta': 'El Hábeas Data fue introducido por la '
                             'Constitución de:',
                 'alternativas': ['1933', '1993', '1856', '1920', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'El Hábeas Data protege el derecho a solicitar '
                             'y recibir información, y la protección de la '
                             'intimidad:',
                 'alternativas': ['Política',
                                  'Comercial',
                                  'Religiosa',
                                  'Empresarial',
                                  'Personal y familiar'],
                 'correcta': 'E'},
                {'pregunta': 'El plazo para presentar el Hábeas Data es de '
                             '60 días hábiles después de:',
                 'alternativas': ['La respuesta denegatoria',
                                  'La sentencia judicial',
                                  'La notificación fiscal',
                                  'El acto administrativo',
                                  'La publicación de la norma'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción de Inconstitucionalidad se crea con '
                             'la Constitución de:',
                 'alternativas': ['1856', '1979', '1920', '1933', '1993'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Inconstitucionalidad es la única '
                             'garantía que se presenta en:',
                 'alternativas': ['Instancia única y definitiva',
                                  'Doble instancia',
                                  'Primera instancia',
                                  'Tres instancias',
                                  'Instancia administrativa'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los facultados para interponer Acción de '
                             'Inconstitucionalidad está un grupo de '
                             'ciudadanos con firmas comprobadas por el JNE, '
                             'en número no menor a:',
                 'alternativas': ['5000', '10000', '1000', '500', '2000'],
                 'correcta': 'A'},
                {'pregunta': 'El plazo para interponer una Acción de '
                             'Inconstitucionalidad es de 6 años desde su '
                             'publicación, y en tratados internacionales el '
                             'plazo es de:',
                 'alternativas': ['6 años también',
                                  '2 años',
                                  '1 año',
                                  '6 meses',
                                  '3 meses'],
                 'correcta': 'D'},
                {'pregunta': 'Para resolver la Acción de '
                             'Inconstitucionalidad se requiere el voto a '
                             'favor de un número de magistrados del Tribunal '
                             'Constitucional igual a:',
                 'alternativas': ['4', '5', '3', '7', '6'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción Popular se originó en la justicia '
                             'romana y se introdujo por primera vez en la '
                             'Constitución de:',
                 'alternativas': ['1856', '1979', '1993', '1920', '1933'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción Popular procede contra normas de '
                             'rango de decretos y resoluciones, y es '
                             'competencia exclusiva de:',
                 'alternativas': ['La Contraloría',
                                  'El Tribunal Constitucional',
                                  'El Ejecutivo',
                                  'El Poder Judicial',
                                  'El Congreso'],
                 'correcta': 'D'},
                {'pregunta': 'El plazo para interponer una Acción Popular es '
                             'de:',
                 'alternativas': ['3 años',
                                  '10 años',
                                  '5 años',
                                  '1 año',
                                  '6 años'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Cumplimiento fue creada por la '
                             'Constitución de:',
                 'alternativas': ['1856', '1979', '1993', '1920', '1933'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Cumplimiento sirve para hacer '
                             'cumplir normas legales o:',
                 'alternativas': ['Sentencias privadas',
                                  'Actos administrativos',
                                  'Reglamentos internos',
                                  'Decisiones empresariales',
                                  'Contratos comerciales'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para presentar la Acción de '
                             'Cumplimiento es de 60 días después de:',
                 'alternativas': ['La publicación de la norma',
                                  'La sentencia',
                                  'La demanda inicial',
                                  'No haberse cumplido el mandato',
                                  'La notificación fiscal'],
                 'correcta': 'D'},
                {'pregunta': 'La vulneración o amenaza, por cualquier '
                             'autoridad, del derecho de solicitar '
                             'información de cualquier entidad pública, es '
                             'protegida por la acción: (IV CEPRU 2025-I)',
                 'alternativas': ['De Habeas Corpus',
                                  'De Amparo',
                                  'De Habeas Data',
                                  'Popular',
                                  'De Inconstitucionalidad'],
                 'correcta': 'C'},
                {'pregunta': 'La garantía constitucional que protege la '
                             'libertad individual y la seguridad personal '
                             'corresponde a la acción de: (IV CEPRU 2022-II)',
                 'alternativas': ['Habeas Corpus',
                                  'Inconstitucionalidad',
                                  'Constitucionalidad',
                                  'Amparo',
                                  'Habeas Data'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción de Habeas Data, introducida por '
                             'primera vez en la Constitución de 1993, tiene '
                             'por objeto la protección del ciudadano frente '
                             'al abuso de: (IV CEPRU 2022-I)',
                 'alternativas': ['La comunicación familiar y social',
                                  'Las autoridades civiles y políticas',
                                  'La información nacional e internacional',
                                  'La informática vinculada con el derecho a '
                                  'la privacidad',
                                  'La información social y cultural'],
                 'correcta': 'D'},
                {'pregunta': 'La Acción de Cumplimiento, que procede contra '
                             'cualquier autoridad o funcionario renuente a '
                             'acatar una norma legal, se interpone ante el '
                             'juez: (IV CEPRU 2022-I)',
                 'alternativas': ['De Familia',
                                  'Civil',
                                  'Penal',
                                  'Laboral',
                                  'Agrario'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ANTECEDENTES',
                      'items': ['El término garantía se define como la '
                                'seguridad o protección frente a un peligro '
                                'en el disfrute de los derechos.',
                                'Las Garantías Constitucionales tienen su '
                                'origen en la tradición francesa.',
                                'En el Perú, la institucionalidad de las '
                                'garantías se inicia con la Constitución de '
                                '1920, que distinguió garantías nacionales, '
                                'individuales y sociales.',
                                'Según García Toma, las Garantías '
                                'Constitucionales son el conjunto de '
                                'declaraciones, medios y recursos que '
                                'aseguran el disfrute de los derechos '
                                'públicos y privados.']},
                     {'titulo': 'LAS SEIS GARANTÍAS EN LA CONSTITUCIÓN DE '
                                '1993',
                      'items': ['El artículo 200 de la Constitución de 1993 '
                                'establece seis Garantías Constitucionales.',
                                'La Constitución de 1920 reconoció el Habeas '
                                'Corpus; la de 1933 sumó la Acción Popular.',
                                'La Constitución de 1979 sumó la Acción de '
                                'Amparo y la Acción de Inconstitucionalidad.',
                                'La Constitución de 1993 sumó el Habeas Data '
                                'y la Acción de Cumplimiento.']},
                     {'titulo': 'LA ACCIÓN DE HABEAS CORPUS',
                      'items': ['La expresión «habeas corpus», de origen '
                                'latino, significa literalmente «que traigas '
                                'el cuerpo».',
                                'El antecedente del habeas corpus es la ley '
                                'inglesa de 1679.',
                                'En el Perú, el habeas corpus fue regulado '
                                'por primera vez en la Constitución de 1920.',
                                'El habeas corpus protege la libertad '
                                'individual y la seguridad personal, y '
                                'derechos constitucionales conexos.',
                                'El habeas corpus se presenta ante el Juez '
                                'especializado en lo Penal, o ante el Juez '
                                'de Paz Letrado si no lo hay.',
                                'El Tribunal Constitucional es, de forma '
                                'extraordinaria, la última y definitiva '
                                'instancia para resolver las resoluciones '
                                'denegatorias del habeas corpus.']},
                     {'titulo': 'LA ACCIÓN DE AMPARO',
                      'items': ['La Acción de Amparo fue introducida por '
                                'primera vez en la Constitución de 1979, '
                                'como garantía distinta al hábeas corpus.',
                                'El Amparo protege todos los derechos '
                                'constitucionales, excepto los protegidos '
                                'por hábeas corpus y hábeas data.',
                                'El Amparo tiene por objeto reponer las '
                                'cosas al estado anterior a la violación de '
                                'un derecho.',
                                'La demanda de Amparo se presenta ante el '
                                'Juez especializado en lo civil.',
                                'El plazo para presentar el Amparo es de 60 '
                                'días desde la vulneración, y 30 días en '
                                'sentencias judiciales.',
                                'El Amparo requiere formalismo: se presenta '
                                'por escrito con autorización de abogado.']},
                     {'titulo': 'LA ACCIÓN DE HÁBEAS DATA',
                      'items': ['El Hábeas Data fue introducido por la '
                                'Constitución de 1993, para proteger frente '
                                'al abuso de la informática.',
                                'El Hábeas Data protege el derecho a '
                                'solicitar y recibir información, y la '
                                'protección de la intimidad personal y '
                                'familiar.',
                                'El plazo para presentar el Hábeas Data es '
                                'de 60 días hábiles después de la respuesta '
                                'denegatoria.',
                                'El Hábeas Data no procede sobre información '
                                'de Defensa Nacional, secreto bancario, y '
                                'telecomunicaciones.']},
                     {'titulo': 'LA ACCIÓN DE INCONSTITUCIONALIDAD',
                      'items': ['La Acción de Inconstitucionalidad se crea '
                                'con la Constitución de 1979; procede contra '
                                'normas de rango de ley.',
                                'Es la única garantía que se presenta en '
                                'instancia única y definitiva ante el '
                                'Tribunal Constitucional.',
                                'Están facultados para interponerla, entre '
                                'otros, el Presidente, el Fiscal de la '
                                'Nación, y el 25% de congresistas.',
                                'También puede interponerla un grupo de 5000 '
                                'ciudadanos con firmas comprobadas por el '
                                'JNE.',
                                'El plazo para interponerla es de 6 años '
                                'desde su publicación, y 6 meses para '
                                'tratados internacionales.',
                                'Se requiere el voto a favor de 5 '
                                'magistrados del Tribunal Constitucional.']},
                     {'titulo': 'LA ACCIÓN POPULAR Y DE CUMPLIMIENTO',
                      'items': ['La Acción Popular se originó en la justicia '
                                'romana; se introdujo por primera vez en la '
                                'Constitución de 1933.',
                                'La Acción Popular procede contra normas de '
                                'rango de decretos y resoluciones, y es '
                                'competencia exclusiva del Poder Judicial.',
                                'El plazo para la Acción Popular es de 5 '
                                'años desde su publicación.',
                                'La Acción de Cumplimiento fue creada por la '
                                'Constitución de 1993, para hacer cumplir '
                                'normas legales o actos administrativos.',
                                'El plazo para la Acción de Cumplimiento es '
                                'de 60 días después de no cumplirse el '
                                'mandato.']}],
  'qr_reto': [{'pregunta': 'El plazo para interponer una Acción de '
                           'Inconstitucionalidad es de 6 años desde su '
                           'publicación, y en tratados internacionales el '
                           'plazo es de:',
               'respuesta': '6 meses'},
              {'pregunta': 'El habeas corpus protege principalmente:',
               'respuesta': 'La libertad individual y la seguridad personal'},
              {'pregunta': 'El habeas corpus se presenta, en primera '
                           'instancia, ante:',
               'respuesta': 'El Juez especializado en lo Penal'}],
  'qr_dato': 'La Constitución de 1979 sumó la Acción de Amparo y la Acción '
             'de Inconstitucionalidad.'},
 {'num': 18,
  'titulo': 'Sistemas de Protección de los Derechos Humanos',
  'secciones': [{'titulo': '18.1 ANTECEDENTES: LA SOCIEDAD DE NACIONES',
                 'items': ['La precursora de las Naciones Unidas fue la '
                           '{Sociedad de Naciones}, concebida durante la '
                           'Primera Guerra Mundial.',
                           'La Sociedad de Naciones se estableció en {1919} '
                           'en virtud del Tratado de {Versalles}.',
                           'La Sociedad de Naciones fracasó en su propósito, '
                           'lo que llevó a la Segunda Guerra {Mundial}.']},
                {'titulo': '18.2 CREACIÓN DE LA ONU',
                 'items': ['El nombre «Naciones Unidas» fue acuñado por el '
                           'presidente estadounidense {Franklin D. '
                           'Roosevelt}.',
                           'El nombre se usó por primera vez el {1} de enero '
                           'de {1942}, cuando 26 naciones aprobaron la '
                           'Declaración de las Naciones Unidas.',
                           'La Carta de creación de las Naciones Unidas fue '
                           'firmada el {26} de junio de {1945} por 50 '
                           'países.',
                           'Las Naciones Unidas empezaron a existir '
                           'oficialmente el {24} de octubre de {1945}, día '
                           'que se celebra como el Día de las Naciones '
                           'Unidas.']},
                {'titulo': '18.3 ORGANIZACIÓN Y FINES DE LA ONU',
                 'items': ['La ONU tiene actualmente {193} Estados Miembros.',
                           'La sede principal de la ONU se ubica en {Nueva '
                           'York}, y tiene sedes secundarias en Ginebra, '
                           'Viena y {Nairobi}.',
                           'Los idiomas oficiales de la ONU son inglés, '
                           'chino, francés, ruso, español y {árabe}.',
                           'La ONU está compuesta por seis órganos '
                           'principales: Asamblea General, Secretario '
                           'General, Consejo de {Seguridad}, Consejo '
                           'Económico y Social, Consejo de Administración '
                           'Fiduciaria y la {Corte Internacional} de '
                           'Justicia.',
                           'Entre los fines de la ONU están preservar la '
                           '{paz} mundial, defender los derechos humanos y '
                           'promover el desarrollo {sostenible}.']},
                {'titulo': '18.4 EL SISTEMA INTERAMERICANO (SIDH)',
                 'items': ['El {Sistema Interamericano de Protección de los '
                           'Derechos Humanos} (SIDH) opera en el marco de la '
                           'Organización de Estados Americanos ({OEA}).',
                           'En 1948 se aprobó la {Declaración Americana} de '
                           'los Deberes y Derechos del Hombre, meses antes '
                           'que la Declaración Universal.',
                           'La {Convención Americana} de Derechos Humanos se '
                           'aprobó el 22 de noviembre de {1969}, entrando en '
                           'vigencia en {1978}.',
                           'El SIDH está constituido por dos organismos: la '
                           '{Comisión Interamericana} y la {Corte '
                           'Interamericana} de Derechos Humanos.']},
                {'titulo': '18.5 LA COMISIÓN INTERAMERICANA DE DERECHOS '
                           'HUMANOS (CIDH)',
                 'items': ['La CIDH se originó de la {Declaración de '
                           'Santiago} de 1959; el Consejo aprobó su Estatuto '
                           'en {1960}.',
                           'En 1965 se adoptó el {Protocolo de Buenos '
                           'Aires}, estableciendo a la CIDH como órgano '
                           'principal de la OEA.',
                           'La sede de la CIDH está en {Washington DC}.',
                           'La Comisión está compuesta por {siete} miembros, '
                           'elegidos por un periodo de {cuatro} años, '
                           'reelegibles una sola vez.',
                           'Entre sus funciones está formular '
                           '{recomendaciones} a los gobiernos y presentar un '
                           'informe anual ante la Asamblea General.']},
                {'titulo': '18.6 LA CORTE INTERAMERICANA Y LA CORTE DE LA '
                           'HAYA',
                 'items': ['La {Corte Interamericana} de Derechos Humanos '
                           '(CORTEIDH) se instala en {1978}, cuando entra en '
                           'vigor la CADH; su sede está en San José de '
                           '{Costa Rica}.',
                           'La Corte Interamericana está constituida por '
                           '{siete} jueces, electos por un periodo de {seis} '
                           'años, reelegibles una vez.',
                           'La Corte Interamericana cumple una función '
                           '{jurisdiccional} (sobre casos sometidos) y una '
                           'función {consultiva} (interpretación de normas).',
                           'La {Corte Internacional de Justicia} (Corte de '
                           'La Haya) es el principal órgano judicial de la '
                           '{ONU}.',
                           'La Corte de La Haya tiene su sede en el Palacio '
                           'de la Paz, en {La Haya} (Países Bajos).',
                           'La Corte de La Haya decide {controversias} '
                           'jurídicas entre Estados, y tiene {quince} '
                           'magistrados.']}],
  'cuadros': [{'titulo': '18.3 ÓRGANOS PRINCIPALES DE LA ONU',
               'encabezados': ['N°', 'Órgano'],
               'filas': [['1', '{Asamblea} General'],
                         ['2', '{Secretario} General'],
                         ['3', '{Consejo} de Seguridad'],
                         ['4', 'Consejo {Económico} y Social'],
                         ['5', '{Corte Internacional} de Justicia']]}],
  'preguntas': [{'pregunta': 'La organización precursora de las Naciones '
                             'Unidas fue:',
                 'alternativas': ['La OEA',
                                  'La OTAN',
                                  'La Sociedad de Naciones',
                                  'El Pacto Andino',
                                  'La Cruz Roja'],
                 'correcta': 'C'},
                {'pregunta': 'La Sociedad de Naciones se estableció en el '
                             'año:',
                 'alternativas': ['1919', '1914', '1918', '1939', '1945'],
                 'correcta': 'A'},
                {'pregunta': 'La Sociedad de Naciones se estableció en '
                             'virtud del Tratado de:',
                 'alternativas': ['Westfalia',
                                  'Ancón',
                                  'Ginebra',
                                  'Roma',
                                  'Versalles'],
                 'correcta': 'E'},
                {'pregunta': 'El fracaso de la Sociedad de Naciones '
                             'desembocó en:',
                 'alternativas': ['La Revolución Rusa',
                                  'La Primera Guerra Mundial',
                                  'La Segunda Guerra Mundial',
                                  'La Guerra Fría',
                                  'La Guerra de Corea'],
                 'correcta': 'C'},
                {'pregunta': 'El nombre «Naciones Unidas» fue acuñado por:',
                 'alternativas': ['Joseph Stalin',
                                  'Harry Truman',
                                  'Woodrow Wilson',
                                  'Franklin D. Roosevelt',
                                  'Winston Churchill'],
                 'correcta': 'D'},
                {'pregunta': 'El nombre «Naciones Unidas» se usó por primera '
                             'vez en:',
                 'alternativas': ['1945', '1942', '1919', '1939', '1950'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta de las Naciones Unidas fue firmada el '
                             '26 de junio de:',
                 'alternativas': ['1942', '1919', '1950', '1945', '1939'],
                 'correcta': 'D'},
                {'pregunta': 'La Carta de la ONU fue firmada inicialmente '
                             'por:',
                 'alternativas': ['193 países',
                                  '10 países',
                                  '26 países',
                                  '100 países',
                                  '50 países'],
                 'correcta': 'E'},
                {'pregunta': 'Las Naciones Unidas empezaron a existir '
                             'oficialmente el:',
                 'alternativas': ['1 de enero de 1945',
                                  '26 de junio de 1945',
                                  '10 de diciembre de 1948',
                                  '1 de enero de 1942',
                                  '24 de octubre de 1945'],
                 'correcta': 'E'},
                {'pregunta': 'El 24 de octubre se celebra como:',
                 'alternativas': ['El Día del Multilateralismo',
                                  'El Día de las Naciones Unidas',
                                  'El Día de la Democracia',
                                  'El Día de la Paz Mundial',
                                  'El Día de los Derechos Humanos'],
                 'correcta': 'B'},
                {'pregunta': 'La ONU tiene actualmente un número de Estados '
                             'Miembros de:',
                 'alternativas': ['100', '150', '193', '250', '51'],
                 'correcta': 'C'},
                {'pregunta': 'La sede principal de la ONU se ubica en:',
                 'alternativas': ['Viena',
                                  'Ginebra',
                                  'Nairobi',
                                  'Nueva York',
                                  'París'],
                 'correcta': 'D'},
                {'pregunta': 'Entre las sedes secundarias de la ONU figura:',
                 'alternativas': ['Berlín',
                                  'Madrid',
                                  'Roma',
                                  'Londres',
                                  'Ginebra'],
                 'correcta': 'E'},
                {'pregunta': 'Los idiomas oficiales de la ONU son seis, '
                             'entre ellos figura:',
                 'alternativas': ['El árabe',
                                  'El portugués',
                                  'El alemán',
                                  'El italiano',
                                  'El japonés'],
                 'correcta': 'A'},
                {'pregunta': 'La ONU está compuesta por un número de órganos '
                             'principales igual a:',
                 'alternativas': ['Cuatro', 'Diez', 'Tres', 'Seis', 'Ocho'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano de la ONU encargado de la paz y '
                             'seguridad internacional es:',
                 'alternativas': ['El Secretario General',
                                  'La Asamblea General',
                                  'El Consejo de Seguridad',
                                  'La Corte Internacional de Justicia',
                                  'El Consejo Económico y Social'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano judicial principal de la ONU es:',
                 'alternativas': ['El Consejo de Administración Fiduciaria',
                                  'La Corte Internacional de Justicia',
                                  'La Asamblea General',
                                  'El Consejo Económico y Social',
                                  'El Consejo de Seguridad'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los fines de la ONU figura defender y '
                             'garantizar:',
                 'alternativas': ['Solo la moneda internacional',
                                  'Solo la seguridad militar',
                                  'Los Derechos Humanos',
                                  'Solo el turismo',
                                  'Solo el comercio internacional'],
                 'correcta': 'C'},
                {'pregunta': 'Un Estado que infringe los principios de la '
                             'Carta de la ONU puede ser:',
                 'alternativas': ['Anexado a otro país',
                                  'Ignorado sin consecuencias',
                                  'Automáticamente disuelto',
                                  'Excluido temporalmente o expulsado',
                                  'Premiado'],
                 'correcta': 'D'},
                {'pregunta': 'Estados no miembros de la ONU, como el '
                             'Vaticano, pueden tener estatuto de:',
                 'alternativas': ['Miembro pleno',
                                  'Observador, sin derecho a voto',
                                  'Sancionado permanente',
                                  'Fundador',
                                  'Excluido total'],
                 'correcta': 'B'},
                {'pregunta': 'El Sistema Interamericano de Protección de los '
                             'Derechos Humanos (SIDH) opera en el marco de:',
                 'alternativas': ['La UNASUR',
                                  'La ONU',
                                  'La OEA',
                                  'La UNESCO',
                                  'El FMI'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración Americana de los Deberes y '
                             'Derechos del Hombre se aprobó en:',
                 'alternativas': ['1969', '1959', '1978', '1945', '1948'],
                 'correcta': 'E'},
                {'pregunta': 'La Convención Americana de Derechos Humanos se '
                             'aprobó el 22 de noviembre de:',
                 'alternativas': ['1978', '1959', '1948', '1990', '1969'],
                 'correcta': 'E'},
                {'pregunta': 'El SIDH está constituido por dos organismos: '
                             'la Corte Interamericana y la:',
                 'alternativas': ['Corte de La Haya',
                                  'Corte Suprema Regional',
                                  'Fiscalía Interamericana',
                                  'Asamblea de la OEA',
                                  'Comisión Interamericana'],
                 'correcta': 'E'},
                {'pregunta': 'La CIDH se originó de la Declaración de '
                             'Santiago, redactada en:',
                 'alternativas': ['1948', '1978', '1959', '1965', '1970'],
                 'correcta': 'C'},
                {'pregunta': 'El Protocolo que estableció a la CIDH como '
                             'órgano principal de la OEA se llama Protocolo '
                             'de:',
                 'alternativas': ['Lima',
                                  'Santiago',
                                  'Buenos Aires',
                                  'Washington',
                                  'San José'],
                 'correcta': 'C'},
                {'pregunta': 'La sede de la Comisión Interamericana de '
                             'Derechos Humanos está en:',
                 'alternativas': ['Nueva York',
                                  'Ginebra',
                                  'La Haya',
                                  'Washington DC',
                                  'San José de Costa Rica'],
                 'correcta': 'D'},
                {'pregunta': 'La Comisión Interamericana está compuesta por '
                             'un número de miembros igual a:',
                 'alternativas': ['Quince',
                                  'Cinco',
                                  'Nueve',
                                  'Once',
                                  'Siete'],
                 'correcta': 'E'},
                {'pregunta': 'La Corte Interamericana de Derechos Humanos se '
                             'instaló en el año:',
                 'alternativas': ['1969', '1948', '1990', '1978', '1959'],
                 'correcta': 'D'},
                {'pregunta': 'La sede de la Corte Interamericana de Derechos '
                             'Humanos está en:',
                 'alternativas': ['San José de Costa Rica',
                                  'La Haya',
                                  'Washington DC',
                                  'Ginebra',
                                  'Bogotá'],
                 'correcta': 'A'},
                {'pregunta': 'Los jueces de la Corte Interamericana son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Seis años',
                                  'Ocho años',
                                  'Cuatro años',
                                  'Diez años',
                                  'Cinco años'],
                 'correcta': 'A'},
                {'pregunta': 'La Corte Interamericana cumple una función '
                             'jurisdiccional y otra función llamada:',
                 'alternativas': ['Fiscalizadora',
                                  'Consultiva',
                                  'Ejecutiva',
                                  'Administrativa',
                                  'Legislativa'],
                 'correcta': 'B'},
                {'pregunta': 'La Corte Internacional de Justicia, o Corte de '
                             'La Haya, es el principal órgano judicial de:',
                 'alternativas': ['El FMI',
                                  'La ONU',
                                  'La Unión Europea',
                                  'La OEA',
                                  'La UNESCO'],
                 'correcta': 'B'},
                {'pregunta': 'La Corte de La Haya tiene su sede en el '
                             'Palacio de la Paz, ubicado en:',
                 'alternativas': ['Nueva York, Estados Unidos',
                                  'Viena, Austria',
                                  'Ginebra, Suiza',
                                  'Bruselas, Bélgica',
                                  'La Haya, Países Bajos'],
                 'correcta': 'E'},
                {'pregunta': 'La Corte de La Haya está encargada de decidir '
                             'controversias jurídicas entre:',
                 'alternativas': ['Organizaciones no gubernamentales',
                                  'Empresas privadas',
                                  'Municipios',
                                  'Estados',
                                  'Personas naturales'],
                 'correcta': 'D'},
                {'pregunta': 'El número de magistrados de la Corte '
                             'Internacional de Justicia es:',
                 'alternativas': ['Siete',
                                  'Nueve',
                                  'Quince',
                                  'Veintiuno',
                                  'Once'],
                 'correcta': 'C'},
                {'pregunta': '¿Cuál es la sede de la Corte Interamericana de '
                             'los Derechos Humanos? (IV CEPRU 2023-II)',
                 'alternativas': ['Washington D.C.',
                                  'Nueva York',
                                  'Lima',
                                  'San José',
                                  'Barcelona'],
                 'correcta': 'D'},
                {'pregunta': 'Es uno de los instrumentos supranacionales de '
                             'protección de los Derechos Humanos: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['Convención de los Derechos Políticos de '
                                  'la Mujer',
                                  'Constitución Política del Perú',
                                  'Declaración de los Derechos Civiles y '
                                  'Políticos',
                                  'Petición de Derechos',
                                  'Convenio de Miami'],
                 'correcta': 'A'},
                {'pregunta': 'La institución constituida por 7 jueces '
                             'elegidos a título personal con reconocida '
                             'competencia en derechos humanos es la: (II '
                             'CEPRU 2023-II)',
                 'alternativas': ['Comisión Interamericana de Derechos '
                                  'Humanos',
                                  'Corte Americana de Justicia',
                                  'Corte de la Haya',
                                  'Corte Internacional de Justicia',
                                  'Corte Interamericana de Derechos Humanos'],
                 'correcta': 'E'},
                {'pregunta': 'El principal órgano judicial de las Naciones '
                             'Unidas, con sede en el Palacio de la Paz, es '
                             'la Corte: (IV CEPRU 2022-II)',
                 'alternativas': ['Superior de Justicia',
                                  'Marcial de Justicia',
                                  'Suprema de Justicia',
                                  'Subalterna de Justicia',
                                  'Internacional de Justicia'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'ANTECEDENTES: LA SOCIEDAD DE NACIONES',
                      'items': ['La precursora de las Naciones Unidas fue la '
                                'Sociedad de Naciones, concebida durante la '
                                'Primera Guerra Mundial.',
                                'La Sociedad de Naciones se estableció en '
                                '1919 en virtud del Tratado de Versalles.',
                                'La Sociedad de Naciones fracasó en su '
                                'propósito, lo que llevó a la Segunda Guerra '
                                'Mundial.']},
                     {'titulo': 'CREACIÓN DE LA ONU',
                      'items': ['El nombre «Naciones Unidas» fue acuñado por '
                                'el presidente estadounidense Franklin D. '
                                'Roosevelt.',
                                'El nombre se usó por primera vez el 1 de '
                                'enero de 1942, cuando 26 naciones aprobaron '
                                'la Declaración de las Naciones Unidas.',
                                'La Carta de creación de las Naciones Unidas '
                                'fue firmada el 26 de junio de 1945 por 50 '
                                'países.',
                                'Las Naciones Unidas empezaron a existir '
                                'oficialmente el 24 de octubre de 1945, día '
                                'que se celebra como el Día de las Naciones '
                                'Unidas.']},
                     {'titulo': 'ORGANIZACIÓN Y FINES DE LA ONU',
                      'items': ['La ONU tiene actualmente 193 Estados '
                                'Miembros.',
                                'La sede principal de la ONU se ubica en '
                                'Nueva York, y tiene sedes secundarias en '
                                'Ginebra, Viena y Nairobi.',
                                'Los idiomas oficiales de la ONU son inglés, '
                                'chino, francés, ruso, español y árabe.',
                                'La ONU está compuesta por seis órganos '
                                'principales: Asamblea General, Secretario '
                                'General, Consejo de Seguridad, Consejo '
                                'Económico y Social, Consejo de '
                                'Administración Fiduciaria y la Corte '
                                'Internacional de Justicia.',
                                'Entre los fines de la ONU están preservar '
                                'la paz mundial, defender los derechos '
                                'humanos y promover el desarrollo '
                                'sostenible.']},
                     {'titulo': 'EL SISTEMA INTERAMERICANO (SIDH)',
                      'items': ['El Sistema Interamericano de Protección de '
                                'los Derechos Humanos (SIDH) opera en el '
                                'marco de la Organización de Estados '
                                'Americanos (OEA).',
                                'En 1948 se aprobó la Declaración Americana '
                                'de los Deberes y Derechos del Hombre, meses '
                                'antes que la Declaración Universal.',
                                'La Convención Americana de Derechos Humanos '
                                'se aprobó el 22 de noviembre de 1969, '
                                'entrando en vigencia en 1978.',
                                'El SIDH está constituido por dos '
                                'organismos: la Comisión Interamericana y la '
                                'Corte Interamericana de Derechos Humanos.']},
                     {'titulo': 'LA COMISIÓN INTERAMERICANA DE DERECHOS '
                                'HUMANOS (CIDH)',
                      'items': ['La CIDH se originó de la Declaración de '
                                'Santiago de 1959; el Consejo aprobó su '
                                'Estatuto en 1960.',
                                'En 1965 se adoptó el Protocolo de Buenos '
                                'Aires, estableciendo a la CIDH como órgano '
                                'principal de la OEA.',
                                'La sede de la CIDH está en Washington DC.',
                                'La Comisión está compuesta por siete '
                                'miembros, elegidos por un periodo de cuatro '
                                'años, reelegibles una sola vez.',
                                'Entre sus funciones está formular '
                                'recomendaciones a los gobiernos y presentar '
                                'un informe anual ante la Asamblea '
                                'General.']},
                     {'titulo': 'LA CORTE INTERAMERICANA Y LA CORTE DE LA '
                                'HAYA',
                      'items': ['La Corte Interamericana de Derechos Humanos '
                                '(CORTEIDH) se instala en 1978, cuando entra '
                                'en vigor la CADH; su sede está en San José '
                                'de Costa Rica.',
                                'La Corte Interamericana está constituida '
                                'por siete jueces, electos por un periodo de '
                                'seis años, reelegibles una vez.',
                                'La Corte Interamericana cumple una función '
                                'jurisdiccional (sobre casos sometidos) y '
                                'una función consultiva (interpretación de '
                                'normas).',
                                'La Corte Internacional de Justicia (Corte '
                                'de La Haya) es el principal órgano judicial '
                                'de la ONU.',
                                'La Corte de La Haya tiene su sede en el '
                                'Palacio de la Paz, en La Haya (Países '
                                'Bajos).',
                                'La Corte de La Haya decide controversias '
                                'jurídicas entre Estados, y tiene quince '
                                'magistrados.']}],
  'qr_reto': [{'pregunta': 'La Carta de la ONU fue firmada inicialmente por:',
               'respuesta': '50 países'},
              {'pregunta': 'Entre las sedes secundarias de la ONU figura:',
               'respuesta': 'Ginebra'},
              {'pregunta': 'Los jueces de la Corte Interamericana son '
                           'elegidos por un periodo de:',
               'respuesta': 'Seis años'}],
  'qr_dato': 'La sede de la CIDH está en Washington DC.'}]
