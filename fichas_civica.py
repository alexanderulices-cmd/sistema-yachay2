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
                {'titulo': '1.4 LA MORAL: CONCEPTO Y ETIMOLOGÍA',
                 'items': ['La {moral} es la forma de conducta que la mutua '
                           'convivencia fija entre los hombres, cuyo fin es '
                           'hacer el {bien}.',
                           'La moral concierne al {fuero interno}, con '
                           'efectos en el ascenso espiritual y la perfección '
                           'humana.',
                           'Etimológicamente, {moral} proviene del latín '
                           '«mores», que significa {costumbre}.',
                           'Etimológicamente, {ética} proviene del griego '
                           '«ethos», que también significa costumbre; la '
                           'ética es la disciplina que trata la {moral}.']},
                {'titulo': '1.5 DIFERENCIAS ENTRE DERECHO Y MORAL',
                 'items': ['Por su ámbito: la {moral} es interior (gobierna '
                           'la conciencia) y el {derecho} es exterior '
                           '(regula la conducta externa).',
                           'Por sus efectos: la moral es {unilateral} (solo '
                           'impone deberes, sin generar derechos), y el '
                           'derecho es {bilateral} (concede facultades y a '
                           'la vez deberes).',
                           'Por su origen: la moral es {autónoma} (surge por '
                           'decisión personal), y el derecho es {heterónomo} '
                           '(emana de un poder extraño, la Ley).',
                           'Por su fuerza: la moral es {incoercible} (no '
                           'existe fuerza que obligue su cumplimiento), y el '
                           'derecho es {coercible} (existe poder '
                           'coercitivo).',
                           'Por su campo de acción: la moral es {amplia} '
                           '(impone deberes incluso con uno mismo y con '
                           'Dios), y el derecho es {preciso} (reglas '
                           'detalladas).']}],
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
                 'alternativas': ['Ethos', 'Ius', 'Lex', 'Directum', 'Mores'],
                 'correcta': 'B'},
                {'pregunta': 'El vocablo latino «Directum», aplicado tras el '
                             'Corpus Iuris Civilis, significa:',
                 'alternativas': ['Costumbre',
                                  'Justicia',
                                  'Autoridad',
                                  'Sanción',
                                  'Recto, conforme a la norma'],
                 'correcta': 'E'},
                {'pregunta': 'Para Mario Alzamora Valdez, el Derecho es la '
                             'regulación de la vida social del hombre para '
                             'alcanzar:',
                 'alternativas': ['La justicia',
                                  'La paz social',
                                  'El orden',
                                  'La igualdad',
                                  'La libertad'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de normas jurídicas que forman el '
                             'ordenamiento vigente (Constitución, leyes, '
                             'códigos) corresponde al Derecho:',
                 'alternativas': ['Objetivo',
                                  'Natural',
                                  'Consuetudinario',
                                  'Subjetivo',
                                  'Positivo'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho a la vida, a la libertad o a la '
                             'propiedad son ejemplos del Derecho:',
                 'alternativas': ['Objetivo',
                                  'Subjetivo',
                                  'Público',
                                  'Comparado',
                                  'Consuetudinario'],
                 'correcta': 'B'},
                {'pregunta': 'En el derecho subjetivo, la persona sobre la '
                             'cual recae un deber correlativo es el:',
                 'alternativas': ['Objeto del derecho',
                                  'Legislador',
                                  'Sujeto activo',
                                  'Titular del derecho',
                                  'Sujeto pasivo'],
                 'correcta': 'E'},
                {'pregunta': 'Las fuentes que hacen referencia a los '
                             'orígenes mediatos de la norma jurídica '
                             '(factores sociales, económicos y culturales) '
                             'se denominan:',
                 'alternativas': ['Consuetudinarias',
                                  'Materiales o reales',
                                  'Formales',
                                  'Doctrinarias',
                                  'Jurisprudenciales'],
                 'correcta': 'B'},
                {'pregunta': 'La forma de conducta implantada por una '
                             'colectividad, repetida de manera uniforme y '
                             'permanente, cuya observancia se hace '
                             'obligatoria, es:',
                 'alternativas': ['La costumbre',
                                  'La doctrina',
                                  'La jurisprudencia',
                                  'La ley',
                                  'La equidad'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de resoluciones emitidas por la '
                             'Corte Suprema y el Tribunal Constitucional '
                             'sobre una cuestión determinada constituye:',
                 'alternativas': ['La jurisprudencia',
                                  'La costumbre',
                                  'La ley',
                                  'Los principios generales',
                                  'La doctrina'],
                 'correcta': 'A'},
                {'pregunta': 'Los estudios especializados del derecho, que '
                             'dan lugar a escuelas y teorías jurídicas pero '
                             'carecen de fuerza legal obligatoria, '
                             'constituyen:',
                 'alternativas': ['La costumbre',
                                  'La ley',
                                  'La casuística',
                                  'La doctrina',
                                  'La jurisprudencia'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 139 de la Constitución '
                             'vigente, los principios generales del derecho '
                             'tienen:',
                 'alternativas': ['Valor supletorio únicamente',
                                  'Solo valor referencial',
                                  'Carácter consuetudinario',
                                  'Fuerza de ley',
                                  'Aplicación exclusiva penal'],
                 'correcta': 'D'},
                {'pregunta': 'Que una ley deba ser cumplida por todos los '
                             'que están en el territorio donde rige, incluso '
                             'en contra de su voluntad, corresponde a su '
                             'carácter:',
                 'alternativas': ['Abstracto',
                                  'Impersonal',
                                  'Obligatorio',
                                  'Coercitivo',
                                  'Permanente'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ley se aplique a un grupo indeterminado '
                             'de sujetos y no a una sola persona corresponde '
                             'a su carácter:',
                 'alternativas': ['Impersonal',
                                  'Coercitivo',
                                  'Irretroactivo',
                                  'Permanente',
                                  'General'],
                 'correcta': 'A'},
                {'pregunta': 'Que una ley regule hechos posteriores a su '
                             'sanción y no rija sobre conductas anteriores '
                             'corresponde a su carácter:',
                 'alternativas': ['Permanente',
                                  'Abstracto',
                                  'Irretroactivo',
                                  'Coercitivo',
                                  'Impersonal'],
                 'correcta': 'C'},
                {'pregunta': 'Que el incumplimiento de la ley implique la '
                             'imposición de una pena o castigo corresponde a '
                             'su carácter:',
                 'alternativas': ['Coercitivo',
                                  'Permanente',
                                  'General',
                                  'Impersonal',
                                  'Abstracto'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, la palabra «Moral» proviene '
                             'del latín «mores», que significa:',
                 'alternativas': ['Virtud',
                                  'Deber',
                                  'Justicia',
                                  'Costumbre',
                                  'Ley'],
                 'correcta': 'D'},
                {'pregunta': 'Respecto de su ámbito, la Moral es interior y '
                             'el Derecho es:',
                 'alternativas': ['Heterónomo',
                                  'Exterior',
                                  'Bilateral',
                                  'Autónomo',
                                  'Coercible'],
                 'correcta': 'B'},
                {'pregunta': 'Que la Moral solo imponga deberes cuyo '
                             'cumplimiento no genera ningún derecho, a '
                             'diferencia del Derecho que concede facultades '
                             'y señala deberes, corresponde a la diferencia '
                             'por su(s):',
                 'alternativas': ['Fuerza',
                                  'Origen',
                                  'Ámbito',
                                  'Campo de acción',
                                  'Efectos'],
                 'correcta': 'E'},
                {'pregunta': 'Que la Moral surja espontáneamente por '
                             'decisión personal y sea renunciable, mientras '
                             'que el Derecho emane de un poder extraño de '
                             'cumplimiento ineludible, corresponde a la '
                             'diferencia por su:',
                 'alternativas': ['Ámbito',
                                  'Fuerza',
                                  'Efecto',
                                  'Origen',
                                  'Campo de acción'],
                 'correcta': 'D'},
                {'pregunta': 'Que la Moral sea incoercible (sin fuerza que '
                             'obligue su cumplimiento) y el Derecho sea '
                             'coercible (con poder coercitivo que exige su '
                             'cumplimiento) corresponde a la diferencia por '
                             'su:',
                 'alternativas': ['Fuerza',
                                  'Efecto',
                                  'Ámbito',
                                  'Campo de acción',
                                  'Origen'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de normas de conducta humana para '
                             'organizar y regularizar la vida social del '
                             'hombre se llama: (I CEPRU 2025-I)',
                 'alternativas': ['El derecho',
                                  'La ley',
                                  'La moral',
                                  'Los valores',
                                  'Las virtudes'],
                 'correcta': 'A'},
                {'pregunta': 'La ley que es de carácter indefinido y '
                             'permanente, y solo deja de tener vigencia '
                             'cuando es reemplazada por otra ley del mismo '
                             'rango, se caracteriza por ser: (I CEPRU '
                             '2024-II)',
                 'alternativas': ['Obligatoria',
                                  'Coercible',
                                  'Irretroactiva',
                                  'Permanente',
                                  'General'],
                 'correcta': 'D'},
                {'pregunta': 'El no conocimiento de la ley no es excusa para '
                             'su no cumplimiento; es una característica de '
                             'la ley: (I CEPRU 2023-II)',
                 'alternativas': ['De polaridad',
                                  'Obligatoria',
                                  'Jerárquica',
                                  'Universal',
                                  'Flexible'],
                 'correcta': 'B'},
                {'pregunta': 'Una característica de la ley es que es: (I '
                             'CEPRU 2023-I)',
                 'alternativas': ['Voluntaria',
                                  'Efímera',
                                  'Impersonal',
                                  'Incoercible',
                                  'Retroactiva'],
                 'correcta': 'C'},
                {'pregunta': 'Una característica de la ley es que es: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Voluntaria',
                                  'Concreta',
                                  'Coercitiva',
                                  'Individual',
                                  'Retroactiva'],
                 'correcta': 'C'},
                {'pregunta': 'La Ley es toda norma jurídica emanada del '
                             'poder público, destinada a regular la '
                             'conducta: (II CEPRU 2016-II)',
                 'alternativas': ['Externa de las personas fuera de la '
                                  'familia',
                                  'Externa de las personas dentro de la '
                                  'familia',
                                  'Externa de las personas dentro de la '
                                  'sociedad',
                                  'Interna de las personas fuera de la '
                                  'sociedad',
                                  'Interna de las personas dentro de la '
                                  'ciudad'],
                 'correcta': 'C'},
                {'pregunta': 'A la práctica general, uniforme y '
                             'constantemente repetida de una determinada '
                             'conducta por los miembros de una comunidad se '
                             'le denomina: (II CEPRU 2016-II)',
                 'alternativas': ['Costumbre',
                                  'Hábito',
                                  'Arte',
                                  'Historia',
                                  'Idiosincrasia'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, el término «moral» proviene '
                             'del latín «mores», que significa:',
                 'alternativas': ['Ley',
                                  'Costumbre',
                                  'Justicia',
                                  'Bien',
                                  'Virtud'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, el término «ética» proviene '
                             'del griego «ethos», que también significa:',
                 'alternativas': ['Virtud',
                                  'Ley',
                                  'Justicia',
                                  'Costumbre',
                                  'Bien'],
                 'correcta': 'D'},
                {'pregunta': 'Por su ámbito, la moral es interior porque '
                             'gobierna la conciencia, mientras que el '
                             'derecho es:',
                 'alternativas': ['Divino',
                                  'Espiritual',
                                  'Interior también',
                                  'Neutro',
                                  'Exterior, pues regula la conducta '
                                  'externa'],
                 'correcta': 'E'},
                {'pregunta': 'Por sus efectos, la moral es unilateral (solo '
                             'impone deberes) mientras que el derecho es:',
                 'alternativas': ['Unilateral también',
                                  'Trilateral',
                                  'Multilateral',
                                  'Neutro',
                                  'Bilateral (concede facultades y deberes)'],
                 'correcta': 'E'},
                {'pregunta': 'Por su origen, la moral es autónoma (surge por '
                             'decisión personal) mientras que el derecho es:',
                 'alternativas': ['Heterónomo (emana de un poder extraño)',
                                  'Espontáneo',
                                  'Autónomo también',
                                  'Neutro',
                                  'Voluntario'],
                 'correcta': 'A'},
                {'pregunta': 'Por su fuerza, la moral es incoercible (sin '
                             'fuerza que obligue su cumplimiento) mientras '
                             'que el derecho es:',
                 'alternativas': ['Flexible',
                                  'Voluntario',
                                  'Neutro',
                                  'Coercible (existe poder coercitivo)',
                                  'Incoercible también'],
                 'correcta': 'D'},
                {'pregunta': 'Por su campo de acción, la moral es amplia '
                             '(impone deberes incluso con uno mismo) '
                             'mientras que el derecho es:',
                 'alternativas': ['Genérico',
                                  'Amplio también',
                                  'Flexible',
                                  'Preciso (reglas detalladas)',
                                  'Ambiguo'],
                 'correcta': 'D'}],
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
                     {'titulo': 'LA MORAL: CONCEPTO Y ETIMOLOGÍA',
                      'items': ['La moral es la forma de conducta que la '
                                'mutua convivencia fija entre los hombres, '
                                'cuyo fin es hacer el bien.',
                                'La moral concierne al fuero interno, con '
                                'efectos en el ascenso espiritual y la '
                                'perfección humana.',
                                'Etimológicamente, moral proviene del latín '
                                '«mores», que significa costumbre.',
                                'Etimológicamente, ética proviene del griego '
                                '«ethos», que también significa costumbre; '
                                'la ética es la disciplina que trata la '
                                'moral.']},
                     {'titulo': 'DIFERENCIAS ENTRE DERECHO Y MORAL',
                      'items': ['Por su ámbito: la moral es interior '
                                '(gobierna la conciencia) y el derecho es '
                                'exterior (regula la conducta externa).',
                                'Por sus efectos: la moral es unilateral '
                                '(solo impone deberes, sin generar '
                                'derechos), y el derecho es bilateral '
                                '(concede facultades y a la vez deberes).',
                                'Por su origen: la moral es autónoma (surge '
                                'por decisión personal), y el derecho es '
                                'heterónomo (emana de un poder extraño, la '
                                'Ley).',
                                'Por su fuerza: la moral es incoercible (no '
                                'existe fuerza que obligue su cumplimiento), '
                                'y el derecho es coercible (existe poder '
                                'coercitivo).',
                                'Por su campo de acción: la moral es amplia '
                                '(impone deberes incluso con uno mismo y con '
                                'Dios), y el derecho es preciso (reglas '
                                'detalladas).']}],
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
                 'alternativas': ['Lógica',
                                  'Axiología',
                                  'Ontología',
                                  'Gnoseología',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «justicia» proviene de la '
                             'voz latina:',
                 'alternativas': ['Solidus',
                                  'Veritas',
                                  'Dignitas',
                                  'Iustitia',
                                  'Honestitad'],
                 'correcta': 'D'},
                {'pregunta': 'La justicia que busca el bien de la sociedad '
                             'entera se llama:',
                 'alternativas': ['Particular',
                                  'General',
                                  'Conmutativa',
                                  'Distributiva',
                                  'Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia aplicada por un juez al emitir '
                             'sentencia se denomina:',
                 'alternativas': ['General',
                                  'Conmutativa',
                                  'Particular',
                                  'Judicial',
                                  'Social'],
                 'correcta': 'D'},
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
                 'alternativas': ['Judicial',
                                  'Particular',
                                  'General',
                                  'Conmutativa',
                                  'Distributiva'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra «solidaridad» proviene del latín '
                             '«solidus», que significa:',
                 'alternativas': ['Ayuda',
                                  'Colaboración',
                                  'Sólido, firme, compacto',
                                  'Unión',
                                  'Fraternidad'],
                 'correcta': 'C'},
                {'pregunta': 'La honestidad se define principalmente como el '
                             'respeto a:',
                 'alternativas': ['La ley',
                                  'La costumbre',
                                  'La autoridad',
                                  'La religión',
                                  'La verdad'],
                 'correcta': 'E'},
                {'pregunta': 'La dignidad humana depende de:',
                 'alternativas': ['La raza y el sexo',
                                  'El nivel educativo',
                                  'La nacionalidad',
                                  'La condición social',
                                  'Ningún condicionamiento externo, es '
                                  'inherente al ser humano'],
                 'correcta': 'E'},
                {'pregunta': 'La libertad se define como la capacidad de la '
                             'persona de:',
                 'alternativas': ['Seguir la mayoría',
                                  'Obedecer las normas',
                                  'Evitar responsabilidades',
                                  'Depender de otros',
                                  'Autodeterminarse y actuar según su '
                                  'voluntad'],
                 'correcta': 'E'},
                {'pregunta': 'La solidaridad se practica sin distinción de:',
                 'alternativas': ['Solo edad',
                                  'Credo, sexo, raza o afiliación política',
                                  'Solo nacionalidad',
                                  'Solo religión',
                                  'Solo género'],
                 'correcta': 'B'},
                {'pregunta': 'Los valores representan, en síntesis:',
                 'alternativas': ['Tradiciones familiares',
                                  'Normas legales obligatorias',
                                  'Reglas religiosas',
                                  'Lo mejor que la vida humana puede ofrecer',
                                  'Costumbres regionales'],
                 'correcta': 'D'},
                {'pregunta': 'Adicionalmente a la Filosofía, estudian los '
                             'valores de forma aplicada:',
                 'alternativas': ['La Astronomía',
                                  'Solo la Medicina',
                                  'La Sociología, la Economía y la Política',
                                  'La Física',
                                  'Solo la Biología'],
                 'correcta': 'C'},
                {'pregunta': 'La igualdad implica que todas las personas '
                             'tienen ante la ley:',
                 'alternativas': ['Distintos derechos según su riqueza',
                                  'Privilegios especiales',
                                  'Derechos según su edad',
                                  'Ninguna garantía',
                                  'Los mismos derechos y oportunidades'],
                 'correcta': 'E'},
                {'pregunta': 'El respeto se define como el reconocimiento '
                             'de:',
                 'alternativas': ['El valor propio y los derechos de los '
                                  'demás',
                                  'Las normas de tránsito',
                                  'Las tradiciones religiosas',
                                  'Los símbolos patrios',
                                  'Solo la autoridad estatal'],
                 'correcta': 'A'},
                {'pregunta': 'En la antigua Grecia, el concepto de valores '
                             'se trataba:',
                 'alternativas': ['Como algo general y sin divisiones',
                                  'Solo en el ámbito religioso',
                                  'Solo entre filósofos estoicos',
                                  'Exclusivamente en la política',
                                  'De forma muy especializada por '
                                  'disciplinas'],
                 'correcta': 'A'},
                {'pregunta': 'La justicia social comprende:',
                 'alternativas': ['Solo acuerdos económicos',
                                  'El conjunto de decisiones, normas y '
                                  'principios razonables de una organización '
                                  'social',
                                  'Solo decisiones judiciales',
                                  'Únicamente leyes penales',
                                  'Solo normas religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'Tener valores se relaciona directamente con:',
                 'alternativas': ['Acumular riqueza',
                                  'Evitar el trabajo',
                                  'Respetar a los demás',
                                  'Buscar fama',
                                  'Ganar poder político'],
                 'correcta': 'C'},
                {'pregunta': 'La honestidad, en su sentido más evidente, '
                             'implica coherencia entre:',
                 'alternativas': ['El poder y la autoridad',
                                  'El comportamiento, la expresión y la '
                                  'verdad',
                                  'El pensamiento y la apariencia',
                                  'La riqueza y el estatus',
                                  'La edad y la experiencia'],
                 'correcta': 'B'},
                {'pregunta': 'La dignidad, según la distinción de '
                             'Millán-Puelles, puede ser ontológica o:',
                 'alternativas': ['Adquirida',
                                  'Social',
                                  'Religiosa',
                                  'Política',
                                  'Legal'],
                 'correcta': 'A'},
                {'pregunta': 'Es la colaboración mutua entre dos personas: '
                             '(I CEPRU 2025-I)',
                 'alternativas': ['La dignidad',
                                  'El respeto',
                                  'La solidaridad',
                                  'La igualdad',
                                  'La tolerancia'],
                 'correcta': 'C'},
                {'pregunta': 'Las vivencias e ideales que orientan nuestros '
                             'actos en beneficio propio y de la '
                             'colectividad, llevándonos a la superación '
                             'personal, se refieren a: (III CEPRU 2025-I)',
                 'alternativas': ['Moral',
                                  'Ética',
                                  'Valores',
                                  'Virtud',
                                  'Derecho'],
                 'correcta': 'C'},
                {'pregunta': 'Que el hombre pueda determinarse sin sujeción '
                             'a ninguna fuerza o coacción psicológica '
                             'interior o exterior pertenece al valor de: (I '
                             'CEPRU 2023-II)',
                 'alternativas': ['Derecho',
                                  'Respeto',
                                  'Libertad',
                                  'Moral',
                                  'Solidaridad'],
                 'correcta': 'C'},
                {'pregunta': 'El valor que permite apreciar, reconocer y '
                             'valorar a la sociedad es: (I CEPRU 2023-I)',
                 'alternativas': ['Solidaridad',
                                  'Justicia',
                                  'Respeto',
                                  'Libertad',
                                  'Igualdad'],
                 'correcta': 'C'}],
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
                {'titulo': '3.2 LA SOCIEDAD: ETIMOLOGÍA Y ELEMENTOS '
                           'MATERIALES',
                 'items': ['El término {sociedad} deriva del latín '
                           '«societas» y del griego «koinonia», que '
                           'significa {comunidad}.',
                           'El iusfilósofo {Thomasius} señala que fuera de '
                           'la sociedad no hay derecho.',
                           'Los elementos {materiales} de la sociedad son el '
                           'territorio (espacio físico) y la {población} '
                           '(personas que la conforman).',
                           'El {territorio} es el espacio físico en que '
                           'radica la sociedad, generalmente un país.']},
                {'titulo': '3.3 LA SOCIEDAD: ELEMENTOS ESPIRITUALES',
                 'items': ['El {instinto} es la inclinación natural del '
                           'hombre a ser, por naturaleza, un animal '
                           '{social}.',
                           'La {inteligencia} es la facultad que permite al '
                           'hombre conocer los fines de la vida social, '
                           'desearlos y aceptarlos.',
                           'El {sentimiento} es la base de la cooperación, '
                           'especialmente la {simpatía}.',
                           'La {voluntad} lleva a la cooperación y al '
                           'cumplimiento de los deberes respecto a las '
                           'normas del grupo.']},
                {'titulo': '3.4 CLASES DE PERSONAS Y TEORÍAS DE '
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
                {'titulo': '3.5 EXISTENCIA Y CAPACIDAD DE LA PERSONA',
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
                 'alternativas': ['El Libro I',
                                  'El Libro III',
                                  'El Libro II',
                                  'El Libro IV',
                                  'La Constitución'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, la palabra «persona» '
                             'originalmente designaba:',
                 'alternativas': ['Un documento legal',
                                  'Un título nobiliario',
                                  'La máscara usada por los actores de '
                                  'teatro',
                                  'Una ceremonia religiosa',
                                  'Un cargo político'],
                 'correcta': 'C'},
                {'pregunta': 'Según Aníbal Torres Vásquez, la existencia de '
                             'la persona natural comienza con:',
                 'alternativas': ['El nacimiento',
                                  'La concepción',
                                  'El bautizo',
                                  'Los 18 años',
                                  'El registro civil'],
                 'correcta': 'B'},
                {'pregunta': 'La existencia de la persona natural termina '
                             'con:',
                 'alternativas': ['El matrimonio',
                                  'La muerte',
                                  'La incapacidad',
                                  'Los 100 años',
                                  'La jubilación'],
                 'correcta': 'B'},
                {'pregunta': 'Según Fernández Sessarego, la persona humana '
                             'es una unidad:',
                 'alternativas': ['Solo espiritual',
                                  'Solo social',
                                  'Psicosomática',
                                  'Únicamente legal',
                                  'Solo física'],
                 'correcta': 'C'},
                {'pregunta': 'El Libro I del Código Civil se divide en '
                             'cuántas secciones:',
                 'alternativas': ['Cinco', 'Seis', 'Tres', 'Cuatro', 'Dos'],
                 'correcta': 'D'},
                {'pregunta': 'Las comunidades campesinas y nativas se '
                             'regulan dentro de:',
                 'alternativas': ['El derecho tributario',
                                  'El derecho laboral',
                                  'El Libro I del Código Civil',
                                  'El derecho penal',
                                  'La ley de municipalidades'],
                 'correcta': 'C'},
                {'pregunta': 'La persona puede definirse también como un '
                             'sujeto:',
                 'alternativas': ['Sin obligaciones',
                                  'Solo con derechos',
                                  'Consciente y racional, titular de '
                                  'derechos y obligaciones',
                                  'Sin capacidad legal',
                                  'Exclusivamente económico'],
                 'correcta': 'C'},
                {'pregunta': 'El ser humano es considerado un ser social '
                             'porque:',
                 'alternativas': ['Se realiza plenamente en convivencia con '
                                  'otros',
                                  'Prefiere la soledad',
                                  'Depende solo de sí mismo',
                                  'No necesita normas',
                                  'Vive completamente aislado'],
                 'correcta': 'A'},
                {'pregunta': 'Las personas jurídicas se diferencian de las '
                             'personas naturales en que:',
                 'alternativas': ['Son entidades con personería legal '
                                  'distinta a un individuo',
                                  'No tienen derechos',
                                  'Solo existen en el derecho penal',
                                  'Son siempre empresas',
                                  'No tienen personería legal'],
                 'correcta': 'A'},
                {'pregunta': 'La sociedad se define como el conjunto de '
                             'personas que comparten:',
                 'alternativas': ['Solo un idioma',
                                  'Solo una economía',
                                  'Cultura, normas e instituciones comunes',
                                  'Solo un territorio',
                                  'Solo una religión'],
                 'correcta': 'C'},
                {'pregunta': 'El «Derecho de las personas» regula el '
                             'reconocimiento de:',
                 'alternativas': ['Solo derechos laborales',
                                  'Solo derechos políticos',
                                  'Los derechos fundamentales de la persona',
                                  'Solo derechos patrimoniales',
                                  'Solo obligaciones tributarias'],
                 'correcta': 'C'},
                {'pregunta': 'En la Edad Media, el término «persona» se usó '
                             'como sinónimo de:',
                 'alternativas': ['Esclavo',
                                  'Comerciante',
                                  'Soldado',
                                  'Campesino',
                                  'Portador de dignidades'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra persona es considerada, según el '
                             'texto, equívoca y:',
                 'alternativas': ['Exclusiva',
                                  'Restringida',
                                  'Polisémica',
                                  'Simple',
                                  'Unívoca'],
                 'correcta': 'C'},
                {'pregunta': 'Las asociaciones, fundaciones y comités NO '
                             'inscritos se regulan en:',
                 'alternativas': ['El derecho internacional',
                                  'La Constitución exclusivamente',
                                  'El derecho penal',
                                  'El Libro I del Código Civil, tercera '
                                  'sección',
                                  'Ninguna norma'],
                 'correcta': 'D'},
                {'pregunta': 'El estudio antropológico revela que el hombre '
                             'es un ser:',
                 'alternativas': ['Puramente material',
                                  'Abierto al infinito',
                                  'Cerrado y limitado',
                                  'Determinado biológicamente',
                                  'Sin capacidad de trascender'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad psicosomática de la persona implica '
                             'que lo que afecta al cuerpo:',
                 'alternativas': ['No afecta a la psique',
                                  'No tiene relación con las emociones',
                                  'Solo afecta la salud física',
                                  'Repercute también en la psique, y '
                                  'viceversa',
                                  'Es independiente de la mente'],
                 'correcta': 'D'},
                {'pregunta': 'La persona jurídica se distingue por tener:',
                 'alternativas': ['Existencia biológica',
                                  'Personería legal reconocida',
                                  'Capacidad física',
                                  'Solo obligaciones morales',
                                  'Solo derechos naturales'],
                 'correcta': 'B'},
                {'pregunta': 'El concepto de persona se amplió con el tiempo '
                             'para comprender a:',
                 'alternativas': ['Todo ser humano',
                                  'Solo a los varones',
                                  'Solo a los ciudadanos',
                                  'Solo a los adultos',
                                  'Solo a los nobles'],
                 'correcta': 'A'},
                {'pregunta': 'La sociedad y la persona se relacionan porque '
                             'el individuo:',
                 'alternativas': ['Es anterior a toda organización social',
                                  'Se desarrolla y realiza en el marco de la '
                                  'vida social',
                                  'No requiere de otros',
                                  'Existe independientemente de la sociedad',
                                  'Rechaza las normas colectivas'],
                 'correcta': 'B'},
                {'pregunta': 'Las personas creadas por ley y con un fin '
                             'social, dentro de la clasificación de persona, '
                             'se refieren a la: (III CEPRU 2025-I)',
                 'alternativas': ['Persona jurídica',
                                  'Persona física',
                                  'Persona jurídica de derecho público',
                                  'Persona natural',
                                  'Persona jurídica de derecho privado'],
                 'correcta': 'C'},
                {'pregunta': 'Según el Código Civil, el inicio de la vida '
                             'humana es desde: (I CEPRU 2023-II)',
                 'alternativas': ['5 días de nacido',
                                  'El nacimiento',
                                  '2 horas de nacido',
                                  'La concepción',
                                  '30 días de nacido'],
                 'correcta': 'D'},
                {'pregunta': 'Desde un enfoque legal, la persona humana es '
                             'sujeto de derecho desde su: (II CEPRU 2022-II)',
                 'alternativas': ['Nacimiento',
                                  'Anidación',
                                  'Evolución',
                                  'Concepción',
                                  'Involución'],
                 'correcta': 'D'},
                {'pregunta': 'El término «sociedad» deriva del latín '
                             '«societas» y del griego «koinonia», que '
                             'significa:',
                 'alternativas': ['Reunión',
                                  'Nación',
                                  'Comunidad',
                                  'Estado',
                                  'Grupo'],
                 'correcta': 'C'},
                {'pregunta': 'El iusfilósofo que señala que «fuera de la '
                             'sociedad no hay derecho» es:',
                 'alternativas': ['Kelsen',
                                  'Thomasius',
                                  'Rousseau',
                                  'Kant',
                                  'Hegel'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos materiales de la sociedad son el '
                             'territorio y la:',
                 'alternativas': ['Población',
                                  'Cultura',
                                  'Economía',
                                  'Religión',
                                  'Historia'],
                 'correcta': 'A'},
                {'pregunta': 'El elemento espiritual de la sociedad que '
                             'representa la inclinación natural del hombre a '
                             'ser un animal social se llama:',
                 'alternativas': ['Voluntad',
                                  'Sentimiento',
                                  'Inteligencia',
                                  'Razón',
                                  'Instinto'],
                 'correcta': 'E'},
                {'pregunta': 'El elemento espiritual de la sociedad que '
                             'permite al hombre conocer los fines de la vida '
                             'social, desearlos y aceptarlos, se llama:',
                 'alternativas': ['Emoción',
                                  'Inteligencia',
                                  'Instinto',
                                  'Sentimiento',
                                  'Voluntad'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento espiritual de la sociedad '
                             'considerado la base de la cooperación, '
                             'especialmente la simpatía, se llama:',
                 'alternativas': ['Consciencia',
                                  'Instinto',
                                  'Inteligencia',
                                  'Voluntad',
                                  'Sentimiento'],
                 'correcta': 'E'},
                {'pregunta': 'El elemento espiritual de la sociedad que '
                             'lleva a la cooperación y al cumplimiento de '
                             'los deberes respecto a las normas del grupo se '
                             'llama:',
                 'alternativas': ['Sentimiento',
                                  'Inteligencia',
                                  'Razón',
                                  'Voluntad',
                                  'Instinto'],
                 'correcta': 'D'}],
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
                     {'titulo': 'LA SOCIEDAD: ETIMOLOGÍA Y ELEMENTOS '
                                'MATERIALES',
                      'items': ['El término sociedad deriva del latín '
                                '«societas» y del griego «koinonia», que '
                                'significa comunidad.',
                                'El iusfilósofo Thomasius señala que fuera '
                                'de la sociedad no hay derecho.',
                                'Los elementos materiales de la sociedad son '
                                'el territorio (espacio físico) y la '
                                'población (personas que la conforman).',
                                'El territorio es el espacio físico en que '
                                'radica la sociedad, generalmente un país.']},
                     {'titulo': 'LA SOCIEDAD: ELEMENTOS ESPIRITUALES',
                      'items': ['El instinto es la inclinación natural del '
                                'hombre a ser, por naturaleza, un animal '
                                'social.',
                                'La inteligencia es la facultad que permite '
                                'al hombre conocer los fines de la vida '
                                'social, desearlos y aceptarlos.',
                                'El sentimiento es la base de la '
                                'cooperación, especialmente la simpatía.',
                                'La voluntad lleva a la cooperación y al '
                                'cumplimiento de los deberes respecto a las '
                                'normas del grupo.']},
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
                           'facilitar el ejercicio de sus {derechos}.']},
                {'titulo': '4.5 EL MATRIMONIO: CONCEPTO Y ENFOQUES',
                 'items': ['El {matrimonio} es una institución social '
                           'reconocida como legítima, consistente en la '
                           'unión de dos personas para establecer una '
                           'comunidad de {vida}.',
                           'El artículo {4} de la Constitución Política '
                           'establece que la comunidad y el Estado otorgan '
                           'protección a la familia y promocionan el '
                           '{matrimonio}.',
                           'El artículo {234} del Código Civil define al '
                           'matrimonio como la unión voluntariamente '
                           'concertada por un varón y una mujer legalmente '
                           'aptos, formalizada con sujeción al {Código}, a '
                           'fin de hacer vida común.',
                           'El {matrimonio civil} otorga al marido y la '
                           'mujer autoridad, consideraciones, derechos, '
                           'deberes y responsabilidades {iguales} en el '
                           'hogar.',
                           'El {matrimonio religioso} es el sacramento '
                           'establecido por la iglesia; es {indisoluble}, '
                           'por ser sacramental.']},
                {'titulo': '4.6 REQUISITOS DE FONDO PARA EL MATRIMONIO',
                 'items': ['El requisito de fondo está relacionado con las '
                           'condiciones naturales de {aptitud física}, '
                           'morales y sociales, y la manifestación libre de '
                           'la voluntad.',
                           'Se requiere el {consentimiento}: el matrimonio '
                           'es un acto voluntario.',
                           'Los contrayentes deben ser mayores de {18} años '
                           'de edad.',
                           'No deben adolecer de enfermedades {crónicas} ni '
                           'contagiosas transmisibles por herencia.',
                           'Se requiere gozar del pleno uso de las '
                           '{facultades mentales}, y no ser casados.']},
                {'titulo': '4.7 REQUISITOS DE FORMA PARA EL MATRIMONIO',
                 'items': ['El requisito de {forma} está relacionado con el '
                           'trámite ante el Alcalde provincial o distrital '
                           'del domicilio de cualquiera de los contrayentes.',
                           'Se debe presentar la {partida de nacimiento} y '
                           'certificado de domicilio.',
                           'Se requiere {certificado médico}, expedido no '
                           'antes de 30 días, acreditando aptitud física y '
                           'psicológica.',
                           'Para menores de edad, se requiere el '
                           '{consentimiento} de los padres.',
                           'Se deben publicar los {Edictos matrimoniales} o '
                           'proclamas, anuncio público del matrimonio '
                           'próximo, para que se denuncien posibles '
                           '{impedimentos}.']},
                {'titulo': '4.8 IMPEDIMENTOS PARA CONTRAER MATRIMONIO',
                 'items': ['Los {impedimentos absolutos} (art. 241 C.C.) '
                           'incluyen a los adolescentes (salvo dispensa '
                           'judicial desde los 16 años), personas con '
                           'capacidad restringida, y los {casados}.',
                           'Los {impedimentos relativos} (art. 242 C.C.) '
                           'incluyen a los consanguíneos en línea recta y '
                           'colateral hasta el {tercer} grado, y a los '
                           'afines.',
                           'Entre los impedimentos relativos está también el '
                           '{raptor} con la raptada, mientras subsista el '
                           'rapto o retención violenta.',
                           'Los {impedimentos especiales} (art. 243 C.C.) '
                           'incluyen al tutor o curador con la persona bajo '
                           'su cargo, mientras no estén aprobadas '
                           'judicialmente las {cuentas}.',
                           'Otro impedimento especial afecta a la {viuda}, '
                           'que no puede volver a casarse hasta que '
                           'transcurran 300 días desde la muerte de su '
                           'marido, salvo certificado médico de no estar '
                           '{embarazada}.']},
                {'titulo': '4.9 EL CONCUBINATO O UNIÓN DE HECHO',
                 'items': ['El término {concubinato} deriva de la voz latina '
                           '«concubinatum», del verbo «concubero», que '
                           'significa {dormir} juntos.',
                           'El artículo {5} de la Constitución establece que '
                           'la unión estable de un varón y una mujer, libres '
                           'de impedimento matrimonial, da lugar a una '
                           'comunidad de {bienes} sujeta al régimen de '
                           'sociedad de gananciales.',
                           'El artículo {326} del Código Civil denomina al '
                           'concubinato «{unión de hecho}»; requiere una '
                           'duración mínima de dos años {continuos}.',
                           'El {concubinato propio} (strictu sensu) es '
                           'cuando la pareja vive como casados sin tener '
                           '{impedimentos} para serlo.',
                           'El {concubinato impropio} (lato sensu) es la '
                           'unión de una pareja que hace vida de casados sin '
                           'serlo, por tener {impedimentos}.']},
                {'titulo': '4.10 EL DIVORCIO: CONCEPTO Y CONSECUENCIAS',
                 'items': ['El {divorcio} es la disolución absoluta del '
                           'vínculo matrimonial, poniendo fin a los deberes '
                           '{conyugales} y a la sociedad de gananciales.',
                           'Por el divorcio {cesa} la obligación alimenticia '
                           'entre marido y mujer.',
                           'Si el divorcio es por culpa de un cónyuge y el '
                           'otro carece de bienes suficientes, el juez le '
                           'asigna una {pensión} alimenticia no mayor a un '
                           'tercio de la renta.',
                           'El cónyuge {culpable} del divorcio pierde los '
                           'gananciales que proceden de los bienes del otro.',
                           'Los cónyuges divorciados no tienen derecho a '
                           '{heredar} entre sí.']},
                {'titulo': '4.11 CAUSALES DEL DIVORCIO (ARTÍCULO 333 C.C.)',
                 'items': ['Entre las causales de divorcio, según el '
                           'artículo {333} del Código Civil, están el '
                           'adulterio y la {violencia} física o psicológica.',
                           'También son causales el {atentado} contra la '
                           'vida del cónyuge, y la injuria grave que haga '
                           'insoportable la vida en {común}.',
                           'El artículo {349} del Código Civil remite a las '
                           'mismas 12 causales del artículo 333 (causales de '
                           'separación de {cuerpos}).']}],
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
                 'alternativas': ['Legal',
                                  'Contractual',
                                  'Natural',
                                  'Religioso',
                                  'Administrativo'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo de la Constitución peruana que '
                             'reconoce a la familia como instituto natural y '
                             'fundamental es el:',
                 'alternativas': ['Artículo 20',
                                  'Artículo 4',
                                  'Artículo 2',
                                  'Artículo 10',
                                  'Artículo 16'],
                 'correcta': 'B'},
                {'pregunta': 'Según Aguilar Llanos, las familias peruanas se '
                             'originan:',
                 'alternativas': ['Solo por vínculo religioso',
                                  'Solo en el matrimonio civil',
                                  'Únicamente por adopción',
                                  'Exclusivamente por vínculo consanguíneo',
                                  'También en las uniones de hecho, además '
                                  'del matrimonio'],
                 'correcta': 'E'},
                {'pregunta': 'Según el Tribunal Constitucional, la familia '
                             'se encarga también de transmitir:',
                 'alternativas': ['Solo tradiciones religiosas',
                                  'Únicamente el idioma',
                                  'Solo bienes materiales',
                                  'Solo el apellido',
                                  'Valores éticos, cívicos y culturales'],
                 'correcta': 'E'},
                {'pregunta': 'La persona a quien reconocen como ascendiente '
                             'común varios parientes se llama:',
                 'alternativas': ['Vínculo',
                                  'Parentesco',
                                  'Tronco',
                                  'Grado',
                                  'Línea'],
                 'correcta': 'C'},
                {'pregunta': 'La distancia entre dos parientes se denomina:',
                 'alternativas': ['Línea', 'Nexo', 'Tronco', 'Rama', 'Grado'],
                 'correcta': 'E'},
                {'pregunta': 'La línea que se forma con personas que '
                             'descienden unas de otras es la línea:',
                 'alternativas': ['Recta',
                                  'Colateral',
                                  'Horizontal',
                                  'Espiritual',
                                  'Transversal'],
                 'correcta': 'A'},
                {'pregunta': 'La línea colateral también se conoce como:',
                 'alternativas': ['Ascendente',
                                  'Descendente',
                                  'Consanguínea pura',
                                  'Directa',
                                  'Horizontal o transversal'],
                 'correcta': 'E'},
                {'pregunta': 'Para efectos civiles, en la línea colateral se '
                             'considera hasta el:',
                 'alternativas': ['Quinto grado',
                                  'Cuarto grado',
                                  'Sexto grado',
                                  'Segundo grado',
                                  'Tercer grado'],
                 'correcta': 'B'},
                {'pregunta': 'El parentesco espiritual se establece, por '
                             'ejemplo, con motivo de:',
                 'alternativas': ['Un contrato comercial',
                                  'Un sacramento como el bautismo',
                                  'Una compraventa',
                                  'Un testamento',
                                  'Un préstamo'],
                 'correcta': 'B'},
                {'pregunta': 'La adopción está regulada en el artículo del '
                             'Código Civil número:',
                 'alternativas': ['238', '118', '418', '618', '818'],
                 'correcta': 'A'},
                {'pregunta': 'Mediante la adopción, el adoptado asume los '
                             'derechos y obligaciones de un:',
                 'alternativas': ['Apoderado',
                                  'Padrino',
                                  'Hijo matrimonial',
                                  'Curador',
                                  'Tutor'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, «patria potestad» alude al '
                             '«pater familia» y a la:',
                 'alternativas': ['Herencia',
                                  'Adopción',
                                  'Tutela',
                                  'Potestad o dominio',
                                  'Curatela'],
                 'correcta': 'D'},
                {'pregunta': 'La patria potestad está regulada en el '
                             'artículo del Código Civil número:',
                 'alternativas': ['618', '518', '418', '238', '118'],
                 'correcta': 'C'},
                {'pregunta': 'Durante el matrimonio, la patria potestad se '
                             'ejerce:',
                 'alternativas': ['Solo por la madre',
                                  'Por el Estado',
                                  'Solo por el padre',
                                  'Por los abuelos',
                                  'Conjuntamente por el padre y la madre'],
                 'correcta': 'E'},
                {'pregunta': 'En caso de divorcio, la patria potestad la '
                             'ejerce:',
                 'alternativas': ['Siempre el padre',
                                  'Los abuelos paternos',
                                  'El Poder Judicial directamente',
                                  'Siempre la madre',
                                  'El cónyuge a quien se confían los hijos'],
                 'correcta': 'E'},
                {'pregunta': 'Quien cuida a un menor sin ser su progenitor '
                             'actúa a título de:',
                 'alternativas': ['Tutor',
                                  'Adoptante',
                                  'Padre biológico',
                                  'Curador exclusivo',
                                  'Padrino'],
                 'correcta': 'A'},
                {'pregunta': 'La finalidad de la patria potestad es de '
                             'carácter:',
                 'alternativas': ['Económico exclusivamente',
                                  'Simbólico',
                                  'Tuitivo, de protección y defensa',
                                  'Religioso',
                                  'Punitivo'],
                 'correcta': 'C'},
                {'pregunta': 'Según Cussiánovich, la familia debe garantizar '
                             'al ser humano recién nacido:',
                 'alternativas': ['Solo un nombre',
                                  'Solo educación formal',
                                  'Solo protección legal',
                                  'Sobrevivencia física, emocional y '
                                  'afectiva',
                                  'Solo alimentación'],
                 'correcta': 'D'},
                {'pregunta': 'La patria potestad NO alcanza a:',
                 'alternativas': ['Los cónyuges',
                                  'Los ascendientes ni parientes colaterales',
                                  'Los hijos menores',
                                  'Los hijos adoptivos',
                                  'Los padres'],
                 'correcta': 'B'},
                {'pregunta': 'La institución que protege a los menores de '
                             'edad que no tienen quién ejerza la patria '
                             'potestad sobre ellos se llama:',
                 'alternativas': ['Tutela',
                                  'Adopción',
                                  'Salvaguardia',
                                  'Apoyo',
                                  'Curatela'],
                 'correcta': 'A'},
                {'pregunta': 'La tutela que los padres establecen antes de '
                             'morir, designando al tutor en su testamento, '
                             'se llama tutela:',
                 'alternativas': ['Judicial',
                                  'Estatal',
                                  'Testamentaria',
                                  'Legítima',
                                  'Dativa'],
                 'correcta': 'C'},
                {'pregunta': 'La tutela que, a falta de la testamentaria, '
                             'recae en los abuelos u otros descendientes se '
                             'llama tutela:',
                 'alternativas': ['Notarial',
                                  'Testamentaria',
                                  'Legítima',
                                  'Estatal',
                                  'Dativa'],
                 'correcta': 'C'},
                {'pregunta': 'La tutela que establece el consejo de familia '
                             'cuando no hay tutela testamentaria ni legítima '
                             'se llama tutela:',
                 'alternativas': ['Testamentaria',
                                  'Judicial',
                                  'Legítima',
                                  'Estatal',
                                  'Dativa'],
                 'correcta': 'E'},
                {'pregunta': 'La tutela ejercida por el Estado para niños '
                             'huérfanos o abandonados se llama tutela:',
                 'alternativas': ['Testamentaria',
                                  'Legítima',
                                  'Notarial',
                                  'Estatal',
                                  'Dativa'],
                 'correcta': 'D'},
                {'pregunta': 'La institución jurídica creada para proteger a '
                             'la persona y bienes del mayor de edad '
                             'incapacitado se llama:',
                 'alternativas': ['Tutela',
                                  'Patria potestad',
                                  'Apoyo exclusivo',
                                  'Curatela',
                                  'Adopción'],
                 'correcta': 'D'},
                {'pregunta': 'La persona que ejerce la curatela se llama:',
                 'alternativas': ['Curador',
                                  'Albacea',
                                  'Tutor',
                                  'Curado',
                                  'Apoderado'],
                 'correcta': 'A'},
                {'pregunta': 'El adulto que recibe la curatela se llama:',
                 'alternativas': ['Curador',
                                  'Tutelado exclusivo',
                                  'Apoderado',
                                  'Curado',
                                  'Menor'],
                 'correcta': 'D'},
                {'pregunta': 'Los apoyos, según el Código Civil, son formas '
                             'de asistencia libremente elegidas por una '
                             'persona mayor de edad para facilitar el '
                             'ejercicio de:',
                 'alternativas': ['Sus bienes exclusivamente',
                                  'Sus contratos exclusivamente',
                                  'Sus deudas',
                                  'Sus derechos',
                                  'Sus obligaciones'],
                 'correcta': 'D'},
                {'pregunta': 'Es la unión entre una mujer y un varón '
                             'reconocida por el Código Civil: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['El matrimonio civil',
                                  'La unión de hecho',
                                  'El matrimonio religioso',
                                  'La comunidad',
                                  'La convivencia'],
                 'correcta': 'A'},
                {'pregunta': 'Respecto a la muerte presunta, es correcto '
                             'afirmar que: (I CEPRU 2025-I)',
                 'alternativas': ['Pone fin a la persona humana',
                                  'Si la persona es mayor de 80 años debe '
                                  'transcurrir 10 años',
                                  'Se declara al transcurrir 7 años de la '
                                  'desaparición',
                                  'No disuelve el matrimonio del '
                                  'desaparecido',
                                  'No apertura la sucesión'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de los requisitos de fondo para '
                             'contraer matrimonio está: (III CEPRU 2025-I)',
                 'alternativas': ['Certificado médico de no padecer '
                                  'enfermedad crónica',
                                  'Edicto matrimonial',
                                  'Certificado médico',
                                  'Certificado domiciliario con residencia '
                                  'actual',
                                  'Ser mayor de 18 años'],
                 'correcta': 'E'},
                {'pregunta': 'Los parientes del cónyuge constituyen una '
                             'clase de parentesco denominada: (I CEPRU '
                             '2023-I)',
                 'alternativas': ['Adopción',
                                  'Territorio',
                                  'Afinidad',
                                  'Espiritual',
                                  'Consanguinidad'],
                 'correcta': 'C'},
                {'pregunta': 'La persona es sujeto de derecho desde: (I '
                             'CEPRU 2023-I)',
                 'alternativas': ['El bautizo',
                                  'El nacimiento',
                                  'La muerte',
                                  'La fecundación',
                                  'La concepción'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución que establece '
                             'que el Estado otorga protección a la familia y '
                             'promueve el matrimonio es el artículo:',
                 'alternativas': ['Artículo 6',
                                  'Artículo 2',
                                  'Artículo 7',
                                  'Artículo 4',
                                  'Artículo 5'],
                 'correcta': 'D'},
                {'pregunta': 'El matrimonio, como unión voluntaria de un '
                             'varón y una mujer formalizada con sujeción al '
                             'Código Civil, está definido en el artículo:',
                 'alternativas': ['Artículo 333',
                                  'Artículo 234',
                                  'Artículo 326',
                                  'Artículo 241',
                                  'Artículo 349'],
                 'correcta': 'B'},
                {'pregunta': 'El matrimonio religioso, sacramento '
                             'establecido por la iglesia, se caracteriza por '
                             'ser:',
                 'alternativas': ['Indisoluble',
                                  'Temporal',
                                  'De prueba',
                                  'Disoluble libremente',
                                  'Renovable anualmente'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los requisitos de fondo para contraer '
                             'matrimonio, los contrayentes deben ser mayores '
                             'de:',
                 'alternativas': ['14 años',
                                  '21 años',
                                  '18 años',
                                  '25 años',
                                  '16 años'],
                 'correcta': 'C'},
                {'pregunta': 'El anuncio público del matrimonio próximo, '
                             'para que se denuncien posibles impedimentos, '
                             'se llama:',
                 'alternativas': ['Partida matrimonial',
                                  'Edictos matrimoniales o proclamas',
                                  'Fe de vida',
                                  'Acta de compromiso',
                                  'Certificado de soltería'],
                 'correcta': 'B'},
                {'pregunta': 'Los impedimentos matrimoniales que incluyen a '
                             'los adolescentes y a los ya casados, según el '
                             'artículo 241 del Código Civil, se llaman '
                             'impedimentos:',
                 'alternativas': ['Relativos',
                                  'Temporales',
                                  'Especiales',
                                  'Absolutos',
                                  'Condicionales'],
                 'correcta': 'D'},
                {'pregunta': 'Los impedimentos matrimoniales que incluyen a '
                             'los consanguíneos en línea recta y colateral, '
                             'según el artículo 242 del Código Civil, se '
                             'llaman impedimentos:',
                 'alternativas': ['Especiales',
                                  'Relativos',
                                  'Permanentes',
                                  'Genéricos',
                                  'Absolutos'],
                 'correcta': 'B'},
                {'pregunta': 'El impedimento matrimonial que impide a la '
                             'viuda casarse hasta transcurridos 300 días '
                             'desde la muerte de su marido, salvo '
                             'certificado médico, es un impedimento:',
                 'alternativas': ['Especial',
                                  'General',
                                  'Absoluto',
                                  'Temporal',
                                  'Relativo'],
                 'correcta': 'A'},
                {'pregunta': 'El término «concubinato» deriva de la voz '
                             'latina «concubinatum», relacionada con el '
                             'verbo que significa:',
                 'alternativas': ['Compartir bienes',
                                  'Dormir juntos',
                                  'Unirse legalmente',
                                  'Convivir',
                                  'Formar hogar'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo de la Constitución que regula la '
                             'unión de hecho o concubinato es el artículo:',
                 'alternativas': ['Artículo 5',
                                  'Artículo 7',
                                  'Artículo 4',
                                  'Artículo 8',
                                  'Artículo 6'],
                 'correcta': 'A'},
                {'pregunta': 'El Código Civil, en su artículo 326, denomina '
                             'al concubinato como:',
                 'alternativas': ['Sociedad conyugal',
                                  'Matrimonio civil',
                                  'Comunidad familiar',
                                  'Unión de hecho',
                                  'Vínculo matrimonial'],
                 'correcta': 'D'},
                {'pregunta': 'Para que el concubinato origine una sociedad '
                             'de bienes bajo el régimen de gananciales, la '
                             'unión debe haber durado como mínimo:',
                 'alternativas': ['Dos años continuos',
                                  'Cinco años',
                                  'Seis meses',
                                  'Un año',
                                  'Tres años'],
                 'correcta': 'A'},
                {'pregunta': 'El concubinato en el que la pareja vive como '
                             'casados sin tener impedimentos para serlo se '
                             'llama concubinato:',
                 'alternativas': ['Legal',
                                  'Formal',
                                  'Impropio o lato sensu',
                                  'Propio o strictu sensu',
                                  'Absoluto'],
                 'correcta': 'D'},
                {'pregunta': 'La disolución absoluta del vínculo '
                             'matrimonial, que pone fin a los deberes '
                             'conyugales, se llama:',
                 'alternativas': ['Separación de cuerpos',
                                  'Nulidad matrimonial',
                                  'Anulación',
                                  'Divorcio',
                                  'Concubinato'],
                 'correcta': 'D'},
                {'pregunta': 'Como consecuencia del divorcio, el cónyuge '
                             'declarado culpable pierde:',
                 'alternativas': ['La patria potestad automáticamente',
                                  'El derecho a alimentos exclusivamente',
                                  'Los gananciales que proceden de los '
                                  'bienes del otro',
                                  'El derecho a trabajar',
                                  'La nacionalidad'],
                 'correcta': 'C'},
                {'pregunta': 'Tras el divorcio, los excónyuges, en relación '
                             'al derecho sucesorio, se caracterizan por:',
                 'alternativas': ['Mantener el derecho pleno de herencia',
                                  'No tener derecho a heredar entre sí',
                                  'Heredar solo bienes muebles',
                                  'Heredar solo si hay hijos',
                                  'Heredar en partes iguales'],
                 'correcta': 'B'},
                {'pregunta': 'Las causales de divorcio en el Perú están '
                             'señaladas en el artículo 333 del Código Civil, '
                             'que incluye entre ellas al:',
                 'alternativas': ['Cambio de domicilio',
                                  'Viaje prolongado',
                                  'Desempleo del cónyuge',
                                  'Cambio de trabajo',
                                  'Adulterio'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y NATURALEZA / PARENTESCO: GRADOS '
                                'Y LÍNEAS',
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
                                'El tronco es la persona a quien reconocen '
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
                                'un ascendiente común.']},
                     {'titulo': 'INSTITUCIONES DE AMPARO FAMILIAR: LA PATRIA '
                                'POTESTAD / INSTITUCIONES SUPLET',
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
                                'La tutela protege a los menores de edad '
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
                                'testamentaria ni legítima.']},
                     {'titulo': 'EL MATRIMONIO: CONCEPTO Y ENFOQUES / '
                                'REQUISITOS DE FONDO PARA EL MATRIMONIO',
                      'items': ['El matrimonio es una institución social '
                                'reconocida como legítima, consistente en la '
                                'unión de dos personas para establecer una '
                                'comunidad de vida.',
                                'El artículo 4 de la Constitución Política '
                                'establece que la comunidad y el Estado '
                                'otorgan protección a la familia y '
                                'promocionan el matrimonio.',
                                'El artículo 234 del Código Civil define al '
                                'matrimonio como la unión voluntariamente '
                                'concertada por un varón y una mujer '
                                'legalmente aptos, formalizada con sujeción '
                                'al Código, a fin de hacer vida común.',
                                'El matrimonio civil otorga al marido y la '
                                'mujer autoridad, consideraciones, derechos, '
                                'deberes y responsabilidades iguales en el '
                                'hogar.',
                                'El requisito de fondo está relacionado con '
                                'las condiciones naturales de aptitud '
                                'física, morales y sociales, y la '
                                'manifestación libre de la voluntad.',
                                'Se requiere el consentimiento: el '
                                'matrimonio es un acto voluntario.',
                                'Los contrayentes deben ser mayores de 18 '
                                'años de edad.',
                                'No deben adolecer de enfermedades crónicas '
                                'ni contagiosas transmisibles por '
                                'herencia.']},
                     {'titulo': 'REQUISITOS DE FORMA PARA EL MATRIMONIO / '
                                'IMPEDIMENTOS PARA CONTRAER MATRIMO',
                      'items': ['El requisito de forma está relacionado con '
                                'el trámite ante el Alcalde provincial o '
                                'distrital del domicilio de cualquiera de '
                                'los contrayentes.',
                                'Se debe presentar la partida de nacimiento '
                                'y certificado de domicilio.',
                                'Se requiere certificado médico, expedido no '
                                'antes de 30 días, acreditando aptitud '
                                'física y psicológica.',
                                'Para menores de edad, se requiere el '
                                'consentimiento de los padres.',
                                'Los impedimentos absolutos (art. 241 C.C.) '
                                'incluyen a los adolescentes (salvo dispensa '
                                'judicial desde los 16 años), personas con '
                                'capacidad restringida, y los casados.',
                                'Los impedimentos relativos (art. 242 C.C.) '
                                'incluyen a los consanguíneos en línea recta '
                                'y colateral hasta el tercer grado, y a los '
                                'afines.',
                                'Entre los impedimentos relativos está '
                                'también el raptor con la raptada, mientras '
                                'subsista el rapto o retención violenta.',
                                'Los impedimentos especiales (art. 243 C.C.) '
                                'incluyen al tutor o curador con la persona '
                                'bajo su cargo, mientras no estén aprobadas '
                                'judicialmente las cuentas.']},
                     {'titulo': 'EL CONCUBINATO O UNIÓN DE HECHO / EL '
                                'DIVORCIO: CONCEPTO Y CONSECUENCIAS',
                      'items': ['El término concubinato deriva de la voz '
                                'latina «concubinatum», del verbo '
                                '«concubero», que significa dormir juntos.',
                                'El artículo 5 de la Constitución establece '
                                'que la unión estable de un varón y una '
                                'mujer, libres de impedimento matrimonial, '
                                'da lugar a una comunidad de bienes sujeta '
                                'al régimen de sociedad de gananciales.',
                                'El artículo 326 del Código Civil denomina '
                                'al concubinato «unión de hecho»; requiere '
                                'una duración mínima de dos años continuos.',
                                'El concubinato propio (strictu sensu) es '
                                'cuando la pareja vive como casados sin '
                                'tener impedimentos para serlo.',
                                'El divorcio es la disolución absoluta del '
                                'vínculo matrimonial, poniendo fin a los '
                                'deberes conyugales y a la sociedad de '
                                'gananciales.',
                                'Por el divorcio cesa la obligación '
                                'alimenticia entre marido y mujer.',
                                'Si el divorcio es por culpa de un cónyuge y '
                                'el otro carece de bienes suficientes, el '
                                'juez le asigna una pensión alimenticia no '
                                'mayor a un tercio de la renta.',
                                'El cónyuge culpable del divorcio pierde los '
                                'gananciales que proceden de los bienes del '
                                'otro.']},
                     {'titulo': 'CAUSALES DEL DIVORCIO (ARTÍCULO 333 C.C.)',
                      'items': ['Entre las causales de divorcio, según el '
                                'artículo 333 del Código Civil, están el '
                                'adulterio y la violencia física o '
                                'psicológica.',
                                'También son causales el atentado contra la '
                                'vida del cónyuge, y la injuria grave que '
                                'haga insoportable la vida en común.',
                                'El artículo 349 del Código Civil remite a '
                                'las mismas 12 causales del artículo 333 '
                                '(causales de separación de cuerpos).']}],
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
                 'alternativas': ['Cultura',
                                  'Nacimiento o raza',
                                  'Territorio',
                                  'Gobierno',
                                  'Idioma'],
                 'correcta': 'B'},
                {'pregunta': 'Para Herder y Fichte, compartir elementos como '
                             'etnia y folclore expresa:',
                 'alternativas': ['Un alma colectiva',
                                  'Una obligación legal',
                                  'Un acuerdo político',
                                  'Una decisión estatal',
                                  'Un contrato social'],
                 'correcta': 'A'},
                {'pregunta': 'Anthony D. Smith asocia a la nación '
                             'principalmente con:',
                 'alternativas': ['Un gobierno central',
                                  'Un territorio nacional y mitos comunes de '
                                  'antepasados',
                                  'Solo la lengua oficial',
                                  'Solo la religión mayoritaria',
                                  'Solo la moneda nacional'],
                 'correcta': 'B'},
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
                 'alternativas': ['Únicos',
                                  'Constitucionales',
                                  'Esenciales',
                                  'Legales',
                                  'Secundarios'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'define quiénes son peruanos por nacimiento es '
                             'el:',
                 'alternativas': ['Artículo 100',
                                  'Artículo 2',
                                  'Artículo 52',
                                  'Artículo 4',
                                  'Artículo 200'],
                 'correcta': 'C'},
                {'pregunta': 'Son peruanos por nacimiento los nacidos en el '
                             'exterior de padre o madre peruanos si:',
                 'alternativas': ['Nunca pueden ser peruanos',
                                  'Automáticamente sin ningún trámite',
                                  'Solo si nacen en un país de habla hispana',
                                  'Solo si regresan al Perú antes de los 5 '
                                  'años',
                                  'Son inscritos en el registro '
                                  'correspondiente durante su minoría de '
                                  'edad'],
                 'correcta': 'E'},
                {'pregunta': 'La Ley de Nacionalidad del Perú lleva el '
                             'número:',
                 'alternativas': ['Ley N° 27444',
                                  'Ley N° 28044',
                                  'Ley N° 26574',
                                  'Ley N° 30220',
                                  'Ley N° 26300'],
                 'correcta': 'C'},
                {'pregunta': 'Según la Ley de Nacionalidad, un peruano que '
                             'adopta otra nacionalidad:',
                 'alternativas': ['Debe elegir una sola desde el nacimiento',
                                  'Debe pagar una multa',
                                  'No pierde la peruana, salvo renuncia '
                                  'expresa',
                                  'Pierde automáticamente la peruana',
                                  'Pierde sus derechos civiles'],
                 'correcta': 'C'},
                {'pregunta': 'Para renunciar a la nacionalidad peruana es '
                             'necesario:',
                 'alternativas': ['Ser mayor de edad y suscribir escritura '
                                  'pública',
                                  'Pedir autorización de los padres',
                                  'Ser menor de edad',
                                  'Solo presentar el DNI',
                                  'Ninguna formalidad especial'],
                 'correcta': 'A'},
                {'pregunta': 'Los padres pueden renunciar a la nacionalidad '
                             'peruana en nombre de sus hijos menores:',
                 'alternativas': ['No, solo los mayores de edad pueden '
                                  'renunciar',
                                  'Solo en casos excepcionales',
                                  'Solo si el hijo lo solicita',
                                  'Solo con autorización judicial',
                                  'Sí, siempre'],
                 'correcta': 'A'},
                {'pregunta': 'La identidad nacional se define como:',
                 'alternativas': ['Un documento oficial',
                                  'Una condición económica',
                                  'Un requisito para votar',
                                  'Una obligación legal',
                                  'El sentimiento subjetivo de pertenecer a '
                                  'una nación concreta'],
                 'correcta': 'E'},
                {'pregunta': 'El término «peruanidad» fue acuñado por:',
                 'alternativas': ['Raúl Porras Barrenechea',
                                  'José Carlos Mariátegui',
                                  'Víctor Andrés Belaunde García',
                                  'Manuel González Prada',
                                  'Jorge Basadre'],
                 'correcta': 'C'},
                {'pregunta': 'La peruanidad se define como el sentimiento '
                             'que vincula a los pueblos del Perú con:',
                 'alternativas': ['Sus tradiciones y la fe en su futuro',
                                  'Solo su territorio físico',
                                  'Solo su idioma oficial',
                                  'Solo su economía',
                                  'Solo su gobierno actual'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los aspectos que fundamentan la '
                             'peruanidad figura la etapa de cultura:',
                 'alternativas': ['Solo contemporánea',
                                  'Solo republicana',
                                  'Exclusivamente virreinal',
                                  'Prehispánica',
                                  'Colonial únicamente'],
                 'correcta': 'D'},
                {'pregunta': 'La nacionalidad se adquiere, además del '
                             'nacimiento, por naturalización o:',
                 'alternativas': ['Matrimonio exclusivamente',
                                  'Solo por herencia',
                                  'Opción, con residencia en el Perú',
                                  'Solo por concurso público',
                                  'Solo por decisión judicial'],
                 'correcta': 'C'},
                {'pregunta': 'Las personas con doble nacionalidad ejercen '
                             'los derechos y obligaciones:',
                 'alternativas': ['Solo del país extranjero',
                                  'De ambos países simultáneamente sin '
                                  'distinción',
                                  'Solo del Perú',
                                  'Del país donde domicilian y cuya '
                                  'nacionalidad poseen',
                                  'Ninguno de los dos'],
                 'correcta': 'D'},
                {'pregunta': 'La doble nacionalidad confiere a los '
                             'extranjeros naturalizados:',
                 'alternativas': ['Derechos superiores a los nacionales',
                                  'Ningún derecho privativo de los peruanos '
                                  'por nacimiento',
                                  'Exoneración total de impuestos',
                                  'Automática ciudadanía plena',
                                  'Los mismos derechos privativos de los '
                                  'peruanos por nacimiento'],
                 'correcta': 'B'},
                {'pregunta': 'La nación, para Herder y Fichte, se sustenta '
                             'principalmente en:',
                 'alternativas': ['Elementos compartidos como etnia, '
                                  'folclore y cultura',
                                  'Solo las fronteras políticas',
                                  'Solo el sistema económico',
                                  'Solo la Constitución vigente',
                                  'Un tratado internacional'],
                 'correcta': 'A'},
                {'pregunta': 'El renunciante a la nacionalidad peruana que '
                             'vive en el exterior lo hace ante:',
                 'alternativas': ['Un juez peruano en el extranjero',
                                  'Las Naciones Unidas',
                                  'Un notario extranjero únicamente',
                                  'La embajada de otro país',
                                  'El funcionario consular'],
                 'correcta': 'E'},
                {'pregunta': 'El Sistema de Defensa Nacional es presidido y '
                             'dirigido por:',
                 'alternativas': ['El Poder Judicial',
                                  'El Jefe del Ejército',
                                  'El Congreso',
                                  'El Ministro de Defensa',
                                  'El Presidente de la República'],
                 'correcta': 'E'},
                {'pregunta': 'El Sistema de Defensa Nacional está integrado '
                             'por el Consejo de Ministros, el Ministerio de '
                             'Defensa, el Sistema de Inteligencia Nacional y '
                             'el Sistema de:',
                 'alternativas': ['Salud Pública',
                                  'Aduanas',
                                  'Defensa Civil',
                                  'Educación Nacional',
                                  'Justicia Militar'],
                 'correcta': 'C'},
                {'pregunta': 'Las Fuerzas Armadas peruanas están compuestas '
                             'por el Ejército, la Marina de Guerra y:',
                 'alternativas': ['El Serenazgo',
                                  'La Policía Nacional',
                                  'La Guardia Civil',
                                  'La Marina Mercante',
                                  'La Fuerza Aérea'],
                 'correcta': 'E'},
                {'pregunta': 'La finalidad de la Policía Nacional del Perú '
                             'es garantizar y restablecer:',
                 'alternativas': ['La soberanía territorial',
                                  'El orden interno',
                                  'El comercio internacional',
                                  'La independencia nacional',
                                  'La defensa exterior'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente de la República es el Jefe '
                             'Supremo de las Fuerzas Armadas y de:',
                 'alternativas': ['El Poder Judicial',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'La Policía Nacional',
                                  'La Contraloría'],
                 'correcta': 'D'},
                {'pregunta': 'El estudio de las banderas se llama:',
                 'alternativas': ['Numismática',
                                  'Vexilología',
                                  'Genealogía',
                                  'Filatelia',
                                  'Heráldica'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 49 de la Constitución, los '
                             'símbolos de la Patria son la bandera, el '
                             'escudo y:',
                 'alternativas': ['La escarapela',
                                  'La flor de la cantuta',
                                  'El himno nacional',
                                  'El sol de Mayo',
                                  'El águila'],
                 'correcta': 'C'},
                {'pregunta': 'La primera bandera republicana peruana fue '
                             'creada por:',
                 'alternativas': ['José de San Martín',
                                  'José de la Torre Ugarte',
                                  'Simón Bolívar',
                                  'Torre Tagle',
                                  'Túpac Amaru II'],
                 'correcta': 'A'},
                {'pregunta': 'La bandera definitiva del Perú fue establecida '
                             'el 25 de febrero de 1825 bajo el gobierno de:',
                 'alternativas': ['José de San Martín',
                                  'Torre Tagle',
                                  'Ramón Castilla',
                                  'Simón Bolívar',
                                  'Andrés A. Cáceres'],
                 'correcta': 'D'},
                {'pregunta': 'Según Abraham Valdelomar, San Martín se '
                             'inspiró para los colores de la bandera en:',
                 'alternativas': ['El sol de los Incas',
                                  'La bandera argentina exclusivamente',
                                  'Las pariguanas (flamencos)',
                                  'La bandera chilena',
                                  'El escudo incaico'],
                 'correcta': 'C'},
                {'pregunta': 'El color rojo de la bandera peruana simboliza:',
                 'alternativas': ['La pureza y la paz',
                                  'La riqueza mineral',
                                  'La selva amazónica',
                                  'La sangre de los héroes y mártires',
                                  'El cielo peruano'],
                 'correcta': 'D'},
                {'pregunta': 'El Escudo Nacional se estableció el 25 de '
                             'febrero de 1825 mediante ley promulgada por:',
                 'alternativas': ['Torre Tagle',
                                  'Ramón Castilla',
                                  'José de San Martín',
                                  'Simón Bolívar',
                                  'El Congreso actual'],
                 'correcta': 'D'},
                {'pregunta': 'En el Escudo Nacional, la vicuña representa el '
                             'reino:',
                 'alternativas': ['Vegetal',
                                  'Aéreo',
                                  'Acuático',
                                  'Animal',
                                  'Mineral'],
                 'correcta': 'D'},
                {'pregunta': 'En el Escudo Nacional, el árbol de la quina '
                             'representa el reino:',
                 'alternativas': ['Aéreo',
                                  'Animal',
                                  'Mineral',
                                  'Marino',
                                  'Vegetal'],
                 'correcta': 'E'},
                {'pregunta': 'En el Escudo Nacional, la cornucopia con '
                             'monedas representa el reino:',
                 'alternativas': ['Vegetal',
                                  'Animal',
                                  'Marino',
                                  'Celestial',
                                  'Mineral'],
                 'correcta': 'A'},
                {'pregunta': 'La letra del Himno Nacional del Perú fue '
                             'escrita por:',
                 'alternativas': ['José Bernardo Alcedo',
                                  'Abraham Valdelomar',
                                  'Ricardo Palma',
                                  'César Vallejo',
                                  'José de la Torre Ugarte'],
                 'correcta': 'E'},
                {'pregunta': 'La música del Himno Nacional del Perú fue '
                             'compuesta por:',
                 'alternativas': ['José de la Torre Ugarte',
                                  'José Bernardo Alcedo',
                                  'Torre Tagle',
                                  'Simón Bolívar',
                                  'San Martín'],
                 'correcta': 'B'},
                {'pregunta': 'El Himno Nacional del Perú fue reconocido por '
                             'ley el 15 de abril de:',
                 'alternativas': ['1825', '1821', '1822', '1824', '1820'],
                 'correcta': 'C'},
                {'pregunta': 'El Himno Nacional consta originalmente de seis '
                             'estrofas, pero actualmente solo se cantan la '
                             'primera y:',
                 'alternativas': ['La quinta',
                                  'La cuarta',
                                  'La sexta',
                                  'La segunda',
                                  'La tercera'],
                 'correcta': 'C'},
                {'pregunta': 'La escarapela, de color blanco y encarnado, es '
                             'un símbolo patrio:',
                 'alternativas': ['No oficial pero de uso arraigado',
                                  'Oficial exclusivo',
                                  'Prohibido por ley',
                                  'Militar exclusivo',
                                  'Extranjero'],
                 'correcta': 'A'},
                {'pregunta': 'Respecto a los elementos esenciales de la '
                             'Nación, es correcto señalar: (III CEPRU '
                             '2025-I)',
                 'alternativas': ['Lengua',
                                  'Tradiciones',
                                  'Ideales al futuro',
                                  'Conciencia nacional',
                                  'Costumbre'],
                 'correcta': 'D'},
                {'pregunta': '¿Quién escribió el libro «7 Ensayos de '
                             'Interpretación de la Realidad Peruana»? (IV '
                             'CEPRU 2023-II)',
                 'alternativas': ['Luis Guillermo Lumbreras',
                                  'José Carlos Mariátegui',
                                  'Julio César Tello',
                                  'Víctor Andrés Belaunde',
                                  'John Rowe'],
                 'correcta': 'B'},
                {'pregunta': 'El término «Peruanidad» fue acuñado por: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Víctor Andrés Belaúnde García',
                                  'Fernando Belaúnde Terry',
                                  'Hipólito Unanue',
                                  'Blasco Núñez de Vela',
                                  'José de la Serna'],
                 'correcta': 'A'},
                {'pregunta': 'El elemento integrante de nuestra peruanidad '
                             'de larga tradición y posesión histórica es el: '
                             '(II CEPRU 2022-I)',
                 'alternativas': ['Sentido de organización',
                                  'Sistema político',
                                  'Territorio ancestral',
                                  'Folclore',
                                  'Sistema jurídico'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema mercantilista, en los aspectos que '
                             'fundamentan la peruanidad, se implantó en la '
                             'etapa de: (I CEPRU 2016-I)',
                 'alternativas': ['El desarrollo industrial',
                                  'La influencia hispánica',
                                  'La cultura prehispánica',
                                  'El desarrollo de la República',
                                  'El desarrollo económico'],
                 'correcta': 'B'}],
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
                {'titulo': '6.3 SUBTIPOS DEL ESTADO UNITARIO',
                 'items': ['El {Estado unitario en estricto sensu} se '
                           'caracteriza porque la autoridad central '
                           'monopoliza el poder, organizado '
                           '{piramidalmente}, con un solo sistema judicial.',
                           'El {Estado unitario desconcentrado} atenúa la '
                           'vocación aglutinadora del centro, mediante la '
                           'delegación de funciones hacia autoridades '
                           '{subordinadas}.',
                           'El {Estado unitario descentralizado} establece '
                           'organismos en espacios local, departamental y '
                           'regional, con {autonomía} para administrarse en '
                           'ciertas materias.']},
                {'titulo': '6.4 ESTADO FEDERAL Y ESTADO CONFEDERADO',
                 'items': ['El {Estado federal} se compone de varios Estados '
                           'con gobierno propio, legislación privada y gran '
                           'autonomía administrativa, con representación '
                           'internacional confiada al ejecutivo {federal}.',
                           'Ejemplo de Estado federal: la Constitución de '
                           'los {Estados Unidos} de América de 1787, formada '
                           'por la unión de 13 soberanías autónomas.',
                           'El {Estado confederado} es una organización '
                           'política donde territorios autónomos y soberanos '
                           'se unen, naciendo de un {tratado} internacional.',
                           'En el Estado confederado, los delegados no '
                           'rinden cuentas al Estado central, sino a los '
                           'respectivos {gobiernos} de sus Estados '
                           'miembros.']},
                {'titulo': '6.5 EL ESTADO PERUANO (ARTÍCULO 43)',
                 'items': ['El artículo {43} de la Constitución establece '
                           'que la República del Perú es democrática, '
                           'social, {independiente} y soberana.',
                           'Según el artículo 43, el gobierno del Estado '
                           'peruano es {unitario}, representativo y '
                           'descentralizado.',
                           'El Estado peruano se organiza según el principio '
                           'de {separación de poderes}: Poder Ejecutivo, '
                           'Poder Legislativo y Poder Judicial.']},
                {'titulo': '6.6 EL GOBIERNO: CONCEPTO Y FORMAS CLÁSICAS',
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
                {'titulo': '6.7 OTRAS FORMAS DE GOBIERNO',
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
                 'alternativas': ['Un gobierno de turno',
                                  'La nación jurídicamente organizada',
                                  'Un territorio delimitado',
                                  'Una constitución escrita',
                                  'Un conjunto de ciudadanos'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos del Estado son población, '
                             'territorio, organización jurídica y:',
                 'alternativas': ['Economía',
                                  'Cultura',
                                  'Religión',
                                  'Idioma',
                                  'Soberanía'],
                 'correcta': 'E'},
                {'pregunta': 'El territorio del Estado se caracteriza por '
                             'ser inalienable e:',
                 'alternativas': ['Divisible',
                                  'Inviolable',
                                  'Transferible',
                                  'Ilimitado',
                                  'Negociable'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 54 de la Constitución, el '
                             'territorio comprende el suelo, el subsuelo, el '
                             'espacio aéreo y:',
                 'alternativas': ['El aire internacional',
                                  'Las fronteras vecinas',
                                  'El mar territorial',
                                  'Solo el litoral',
                                  'El espacio exterior'],
                 'correcta': 'C'},
                {'pregunta': 'La organización jurídica de un Estado está '
                             'integrada por:',
                 'alternativas': ['Los tratados internacionales únicamente',
                                  'Solo el Poder Judicial',
                                  'Las costumbres sociales',
                                  'La Constitución, leyes y decretos',
                                  'Solo la Constitución'],
                 'correcta': 'D'},
                {'pregunta': 'La soberanía interna del Estado implica:',
                 'alternativas': ['Depender de organismos internacionales',
                                  'Relacionarse con otros Estados',
                                  'No tener autoridad propia',
                                  'Ceder autoridad a otros países',
                                  'Supremacía sobre los demás poderes del '
                                  'territorio'],
                 'correcta': 'E'},
                {'pregunta': 'La soberanía externa permite al Estado:',
                 'alternativas': ['Actuar sin reconocer a otros Estados',
                                  'Relacionarse con otros Estados soberanos '
                                  'como igual',
                                  'Anexar territorios vecinos',
                                  'Imponerse sobre otros Estados',
                                  'Ignorar el derecho internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado Constitucional surgió en:',
                 'alternativas': ['Francia',
                                  'Alemania',
                                  'Inglaterra',
                                  'Estados Unidos',
                                  'España'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado Constitucional surgió con el '
                             'objetivo de:',
                 'alternativas': ['Eliminar toda forma de gobierno',
                                  'Fortalecer al monarca absoluto',
                                  'Crear un imperio',
                                  'Unificar territorios',
                                  'Limitar las decisiones de los monarcas '
                                  'absolutos'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado Liberal se desarrolló principalmente '
                             'durante el siglo:',
                 'alternativas': ['XVIII', 'XX', 'XIX', 'XV', 'XVII'],
                 'correcta': 'C'},
                {'pregunta': 'Un pilar del Estado Liberal es:',
                 'alternativas': ['La propiedad privada y la economía de '
                                  'mercado',
                                  'La censura estatal',
                                  'La propiedad colectiva obligatoria',
                                  'La monarquía absoluta',
                                  'El partido único'],
                 'correcta': 'A'},
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
                 'alternativas': ['Los sindicatos',
                                  'Un único partido',
                                  'Las ONG',
                                  'Cualquier partido político',
                                  'Las asambleas populares'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado unitario se caracteriza por '
                             'reconocer como fuente de soberanía:',
                 'alternativas': ['Organismos internacionales',
                                  'Solo las regiones',
                                  'Una sola nación',
                                  'Ninguna nación específica',
                                  'Varias naciones'],
                 'correcta': 'C'},
                {'pregunta': 'En un Estado unitario existe:',
                 'alternativas': ['Ningún poder judicial central',
                                  'Varios gobiernos regionales autónomos',
                                  'Un solo gobierno, un parlamento y un '
                                  'poder judicial',
                                  'Solo gobiernos locales',
                                  'Múltiples constituciones'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú, según su estructura política, es un '
                             'Estado:',
                 'alternativas': ['Monárquico',
                                  'Unitario',
                                  'Confederado',
                                  'Sin forma definida',
                                  'Federal'],
                 'correcta': 'B'},
                {'pregunta': 'La población del Estado está constituida por:',
                 'alternativas': ['Únicamente los nacidos en el país',
                                  'Solo los ciudadanos con derecho a voto',
                                  'Solo los funcionarios públicos',
                                  'Solo los mayores de edad',
                                  'Los habitantes organizados políticamente'],
                 'correcta': 'E'},
                {'pregunta': 'El pueblo, dentro de los elementos del Estado, '
                             'se caracteriza por ser:',
                 'alternativas': ['Dependiente de otro Estado',
                                  'Soberano e independiente',
                                  'Subordinado al gobierno extranjero',
                                  'Sin organización',
                                  'Neutral políticamente'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la organización jurídica, el Estado:',
                 'alternativas': ['Carecería de forma',
                                  'Funcionaría igual',
                                  'Sería más eficiente',
                                  'Se fortalecería',
                                  'Tendría más soberanía'],
                 'correcta': 'A'},
                {'pregunta': 'El Estado, en sentido restringido, se refiere '
                             'a:',
                 'alternativas': ['Solo la población',
                                  'El idioma oficial',
                                  'La cultura nacional',
                                  'El conjunto de organismos que ejercen el '
                                  'poder',
                                  'Todo el territorio nacional'],
                 'correcta': 'D'},
                {'pregunta': 'El Gobierno es la autoridad que dirige, '
                             'controla y administra las instituciones de:',
                 'alternativas': ['Los partidos políticos',
                                  'Las empresas privadas',
                                  'La familia',
                                  'La sociedad civil',
                                  'El Estado'],
                 'correcta': 'E'},
                {'pregunta': 'El Gobierno consiste en la conducción política '
                             'general o ejercicio del poder:',
                 'alternativas': ['Electoral',
                                  'Municipal',
                                  'Judicial',
                                  'Legislativo',
                                  'Ejecutivo'],
                 'correcta': 'E'},
                {'pregunta': 'Según Aristóteles, las formas de gobierno se '
                             'dividen en formas puras e:',
                 'alternativas': ['Antiguas',
                                  'Modernas',
                                  'Impuras',
                                  'Democráticas exclusivas',
                                  'Ideales'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las formas puras de gobierno según '
                             'Aristóteles está la monarquía, la aristocracia '
                             'y:',
                 'alternativas': ['La demagogia',
                                  'La democracia',
                                  'La plutocracia',
                                  'La oligarquía',
                                  'La tiranía'],
                 'correcta': 'B'},
                {'pregunta': 'La forma pura de gobierno de uno solo se '
                             'llama:',
                 'alternativas': ['Monarquía',
                                  'Democracia',
                                  'Oligarquía',
                                  'Tiranía',
                                  'Aristocracia'],
                 'correcta': 'A'},
                {'pregunta': 'La deformación de la monarquía, donde el único '
                             'gobernante abusa del poder, se llama:',
                 'alternativas': ['Demagogia',
                                  'Plutocracia',
                                  'Aristocracia',
                                  'Tiranía',
                                  'Oligarquía'],
                 'correcta': 'D'},
                {'pregunta': 'La deformación de la aristocracia, donde el '
                             'grupo gobernante atiende sus propios '
                             'intereses, se llama:',
                 'alternativas': ['Tiranía',
                                  'Demagogia',
                                  'Democracia',
                                  'Monarquía',
                                  'Oligarquía'],
                 'correcta': 'E'},
                {'pregunta': 'La deformación de la democracia, donde el '
                             'gobernante halaga al pueblo con regalos, se '
                             'llama:',
                 'alternativas': ['Plutocracia',
                                  'Tiranía',
                                  'Demagogia',
                                  'Aristocracia',
                                  'Oligarquía'],
                 'correcta': 'C'},
                {'pregunta': 'El gobierno que está de acuerdo con la '
                             'Constitución se llama gobierno:',
                 'alternativas': ['Usurpador',
                                  'De jure o de derecho',
                                  'Revolucionario',
                                  'Provisional',
                                  'De facto'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno que no ha sido elegido según la '
                             'Constitución, pero no necesariamente usa la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['De jure',
                                  'Usurpador',
                                  'Constitucional',
                                  'Legítimo',
                                  'De facto'],
                 'correcta': 'E'},
                {'pregunta': 'El gobierno que carece de título por no haber '
                             'sido elegido, y se mantiene mediante la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['De facto',
                                  'De jure',
                                  'Usurpador',
                                  'Parlamentario',
                                  'Presidencialista'],
                 'correcta': 'A'},
                {'pregunta': 'El gobierno con un jefe de Estado sin '
                             'responsabilidad y un consejo de ministros '
                             'responsable ante el parlamento se llama '
                             'gobierno:',
                 'alternativas': ['Presidencialista',
                                  'Revolucionario',
                                  'De facto',
                                  'Usurpador',
                                  'Parlamentario o de gabinete'],
                 'correcta': 'E'},
                {'pregunta': '¿Quién preside el Sistema de Defensa Nacional? '
                             '(I CEPRU 2023-I)',
                 'alternativas': ['La Primera Dama',
                                  'El Congreso',
                                  'El Presidente del Tribunal Constitucional',
                                  'El Premier',
                                  'El Presidente de la República'],
                 'correcta': 'E'},
                {'pregunta': 'Las lenguas oficiales adoptadas por la ONU '
                             'son: (IV CEPRU 2022-I)',
                 'alternativas': ['Chino - árabe - inglés - italiano - ruso '
                                  '- español',
                                  'Árabe - chino - inglés - portugués - ruso '
                                  '- español',
                                  'Árabe - chino - inglés - holandés - ruso '
                                  '- francés',
                                  'Árabe - chino - inglés - francés - ruso - '
                                  'español',
                                  'Árabe - inglés - chino - alemán - ruso - '
                                  'español'],
                 'correcta': 'D'},
                {'pregunta': 'La Organización de los Estados Americanos es '
                             'un organismo de carácter: (IV CEPRU 2022-I)',
                 'alternativas': ['Mundial',
                                  'Local',
                                  'Regional',
                                  'Universal',
                                  'Nacional'],
                 'correcta': 'C'},
                {'pregunta': 'El que dirige el Sistema de Defensa Nacional '
                             'es el presidente: (II CEPRU 2022-I)',
                 'alternativas': ['De la República',
                                  'De la Corte Suprema',
                                  'Del Consejo de Ministros',
                                  'De la Corte Superior de Justicia',
                                  'Del Pleno del Jurado Nacional de '
                                  'Elecciones'],
                 'correcta': 'A'},
                {'pregunta': 'El Estado unitario en el que la autoridad '
                             'central monopoliza el poder, organizado '
                             'piramidalmente, con un solo sistema judicial, '
                             'se llama Estado unitario:',
                 'alternativas': ['En estricto sensu',
                                  'Descentralizado',
                                  'Confederado',
                                  'Federal',
                                  'Desconcentrado'],
                 'correcta': 'A'},
                {'pregunta': 'El Estado unitario que delega funciones y '
                             'decisiones desde el nivel superior hacia '
                             'autoridades subordinadas se llama Estado '
                             'unitario:',
                 'alternativas': ['Descentralizado',
                                  'En estricto sensu',
                                  'Desconcentrado',
                                  'Federal',
                                  'Confederado'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado unitario que establece organismos en '
                             'espacios local, departamental y regional con '
                             'autonomía administrativa se llama Estado '
                             'unitario:',
                 'alternativas': ['Federal',
                                  'Descentralizado',
                                  'Confederado',
                                  'En estricto sensu',
                                  'Desconcentrado'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado compuesto de varios Estados con '
                             'gobierno propio y legislación privada, pero '
                             'con representación internacional confiada a un '
                             'ejecutivo común, se llama Estado:',
                 'alternativas': ['Autonómico',
                                  'Regional',
                                  'Confederado',
                                  'Federal',
                                  'Unitario'],
                 'correcta': 'D'},
                {'pregunta': 'La Constitución de los Estados Unidos de '
                             'América de 1787 es ejemplo clásico de Estado:',
                 'alternativas': ['Autonómico',
                                  'Unitario',
                                  'Confederado',
                                  'Regional',
                                  'Federal'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado que nace de un tratado '
                             'internacional, donde los delegados no rinden '
                             'cuentas al Estado central sino a sus propios '
                             'gobiernos, se llama Estado:',
                 'alternativas': ['Confederado',
                                  'Unitario',
                                  'Federal',
                                  'Centralizado',
                                  'Descentralizado'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 43 de la Constitución establece '
                             'que la República del Perú es democrática, '
                             'social, independiente y:',
                 'alternativas': ['Confederada',
                                  'Autónoma',
                                  'Federal',
                                  'Soberana',
                                  'Descentralizada'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 43 de la Constitución, el '
                             'gobierno del Estado peruano es unitario, '
                             'representativo y:',
                 'alternativas': ['Confederado',
                                  'Federal',
                                  'Regional',
                                  'Descentralizado',
                                  'Autonómico'],
                 'correcta': 'D'}],
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
                                'Constitución, leyes y decretos.']},
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
                     {'titulo': 'SUBTIPOS DEL ESTADO UNITARIO',
                      'items': ['El Estado unitario en estricto sensu se '
                                'caracteriza porque la autoridad central '
                                'monopoliza el poder, organizado '
                                'piramidalmente, con un solo sistema '
                                'judicial.',
                                'El Estado unitario desconcentrado atenúa la '
                                'vocación aglutinadora del centro, mediante '
                                'la delegación de funciones hacia '
                                'autoridades subordinadas.',
                                'El Estado unitario descentralizado '
                                'establece organismos en espacios local, '
                                'departamental y regional, con autonomía '
                                'para administrarse en ciertas materias.']},
                     {'titulo': 'ESTADO FEDERAL Y ESTADO CONFEDERADO',
                      'items': ['El Estado federal se compone de varios '
                                'Estados con gobierno propio, legislación '
                                'privada y gran autonomía administrativa, '
                                'con representación internacional confiada '
                                'al ejecutivo federal.',
                                'Ejemplo de Estado federal: la Constitución '
                                'de los Estados Unidos de América de 1787, '
                                'formada por la unión de 13 soberanías '
                                'autónomas.',
                                'El Estado confederado es una organización '
                                'política donde territorios autónomos y '
                                'soberanos se unen, naciendo de un tratado '
                                'internacional.',
                                'En el Estado confederado, los delegados no '
                                'rinden cuentas al Estado central, sino a '
                                'los respectivos gobiernos de sus Estados '
                                'miembros.']},
                     {'titulo': 'EL ESTADO PERUANO (ARTÍCULO 43)',
                      'items': ['El artículo 43 de la Constitución establece '
                                'que la República del Perú es democrática, '
                                'social, independiente y soberana.',
                                'Según el artículo 43, el gobierno del '
                                'Estado peruano es unitario, representativo '
                                'y descentralizado.',
                                'El Estado peruano se organiza según el '
                                'principio de separación de poderes: Poder '
                                'Ejecutivo, Poder Legislativo y Poder '
                                'Judicial.']},
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
                                'gobernante abusa del poder.']},
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
                {'titulo': '7.2 LAS CINCO PARTES DE LA CONSTITUCIÓN PERUANA',
                 'items': ['El {preámbulo} es un enunciado previo a las '
                           'normas, que expresa los valores, principios y '
                           'necesidades de un pueblo.',
                           'La {parte dogmática} contiene los principios '
                           'pilares de la constitución: los derechos '
                           'fundamentales y garantías individuales.',
                           'La {parte orgánica} determina la estructura del '
                           'Estado, organizando los {poderes} públicos.',
                           'La {cláusula de reforma} es una garantía de la '
                           'rigidez constitucional, condicionando su reforma '
                           'parcial o total.',
                           'La {declaración} final del texto constitucional '
                           'declara al Perú país vinculado a la {Antártida}, '
                           'propiciando su conservación como Zona de Paz.']},
                {'titulo': '7.3 PODER CONSTITUYENTE Y PODER CONSTITUIDO',
                 'items': ['El {poder constituyente} es «el poder creador '
                           'del Estado» (Burdeau); a él corresponde '
                           'establecer la {Constitución}.',
                           'El poder constituyente es {originario}: su '
                           'fuente radica en sí mismo, sin derivar del poder '
                           'vigente ni del orden jurídico establecido.',
                           'El poder constituyente es {extraordinario}: solo '
                           'aparece en circunstancias excepcionales, como el '
                           'nacimiento del Estado.',
                           'El poder constituyente es {absoluto}: no está '
                           'limitado ni regulado por el derecho vigente, '
                           'gozando de libertad total.',
                           'El {poder constituido}, a diferencia del '
                           'constituyente, es {derivado} (nace de la '
                           'Constitución), ordinario (actúa permanentemente) '
                           'y limitado (sometido al derecho vigente).',
                           'En una sociedad democrática, existe consenso en '
                           'que la titularidad del poder constituyente '
                           'corresponde al {pueblo}.']},
                {'titulo': '7.4 ETIMOLOGÍA Y ANTECEDENTES',
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
                {'titulo': '7.5 CONSTITUCIÓN FORMAL Y MATERIAL',
                 'items': ['Edmund Burke y Ferdinand Lassalle, al igual que '
                           '{Kelsen}, establecieron la división entre '
                           'Constitución formal y {material}.',
                           'La Constitución peruana de {1993} es la norma '
                           'vigente que rige actualmente el ordenamiento '
                           'jurídico del país.']},
                {'titulo': '7.6 CLASES DE CONSTITUCIONES',
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
                {'titulo': '7.7 LA JERARQUÍA NORMATIVA (PIRÁMIDE DE KELSEN)',
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
                 'alternativas': ['Internacional únicamente',
                                  'Positivo',
                                  'Comparado',
                                  'Consuetudinario',
                                  'Privado'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución no está sujeta a evaluación de '
                             'validez formal porque:',
                 'alternativas': ['Depende de tratados internacionales',
                                  'Es revisada cada año',
                                  'No existe un precepto superior a ella',
                                  'Es una ley ordinaria',
                                  'La aprueba el Poder Ejecutivo'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución es resultado del ejercicio del '
                             'Poder:',
                 'alternativas': ['Ejecutivo',
                                  'Legislativo ordinario',
                                  'Constituyente',
                                  'Municipal',
                                  'Judicial'],
                 'correcta': 'C'},
                {'pregunta': 'El titular del Poder Constituyente es:',
                 'alternativas': ['Los partidos políticos',
                                  'El Tribunal Constitucional',
                                  'El pueblo',
                                  'El Congreso',
                                  'El presidente'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 51 de la Constitución, esta '
                             'prevalece sobre:',
                 'alternativas': ['Solo los decretos',
                                  'Solo los tratados internacionales',
                                  'Nada en particular',
                                  'Solo las leyes penales',
                                  'Toda otra norma legal'],
                 'correcta': 'E'},
                {'pregunta': 'El fin último de la Constitución, según el '
                             'texto, debe ser afianzar:',
                 'alternativas': ['La religión oficial',
                                  'El comercio internacional',
                                  'El poder del Estado',
                                  'La economía',
                                  'La Justicia'],
                 'correcta': 'E'},
                {'pregunta': 'El término latino «constitutio» fue '
                             'introducido por:',
                 'alternativas': ['Cicerón',
                                  'Rousseau',
                                  'Aristóteles',
                                  'Platón',
                                  'Montesquieu'],
                 'correcta': 'A'},
                {'pregunta': 'Rousseau llamó «contrato social» a:',
                 'alternativas': ['Un tratado comercial',
                                  'La decisión originaria del pueblo de '
                                  'fundar la comunidad política',
                                  'Un acuerdo entre monarcas',
                                  'Un pacto religioso',
                                  'Una ley penal'],
                 'correcta': 'B'},
                {'pregunta': 'Vattel definió la Constitución como el '
                             'reglamento fundamental que determina:',
                 'alternativas': ['El territorio del Estado',
                                  'El idioma nacional',
                                  'La moneda oficial',
                                  'Cómo debe ejercerse la autoridad pública',
                                  'Los impuestos del Estado'],
                 'correcta': 'D'},
                {'pregunta': 'En 1776, el Congreso de Estados Unidos '
                             'resolvió que los Estados de la Confederación:',
                 'alternativas': ['Adoptaran la Constitución inglesa',
                                  'Eliminaran sus leyes',
                                  'Formaran una monarquía',
                                  'Se dieran sus propias Constituciones',
                                  'Se unificaran en un solo territorio'],
                 'correcta': 'D'},
                {'pregunta': 'El paso de la doctrina del derecho natural a '
                             'la teoría del Estado como contrato social se '
                             'atribuye a:',
                 'alternativas': ['Montesquieu',
                                  'Kelsen',
                                  'Locke exclusivamente',
                                  'Rousseau',
                                  'Thomas Hobbes'],
                 'correcta': 'E'},
                {'pregunta': 'John Locke explicaba que los individuos forman '
                             'una sociedad para:',
                 'alternativas': ['Eliminar toda autoridad',
                                  'Depender de otro Estado',
                                  'Beneficiarse mutuamente bajo la '
                                  'protección del Estado y la ley',
                                  'Someterse a un monarca absoluto',
                                  'Vivir sin normas'],
                 'correcta': 'C'},
                {'pregunta': 'La división entre Constitución formal y '
                             'material fue establecida, entre otros, por:',
                 'alternativas': ['Kelsen',
                                  'Vattel',
                                  'Cicerón',
                                  'Rousseau',
                                  'Bossuet'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución peruana actualmente vigente '
                             'data del año:',
                 'alternativas': ['1933', '1920', '1993', '1856', '1979'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución es descrita como la «norma de '
                             'normas» porque:',
                 'alternativas': ['Es opcional para el Estado',
                                  'Es la primera de las normas de producción',
                                  'Solo rige el comercio',
                                  'No tiene jerarquía superior a las leyes',
                                  'Solo aplica al Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'Según Blancas Bustamante, la Constitución '
                             'define la posición de las personas frente al '
                             'Estado mediante:',
                 'alternativas': ['Tratados internacionales exclusivamente',
                                  'Solo sanciones penales',
                                  'Solo obligaciones tributarias',
                                  'Acuerdos comerciales',
                                  'El reconocimiento de libertades y '
                                  'derechos'],
                 'correcta': 'E'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano tuvo como fuente formal:',
                 'alternativas': ['La Carta Magna inglesa',
                                  'El Código de Hammurabi',
                                  'La Constitución española',
                                  'La Constitución rusa',
                                  'Las Constituciones de los Estados de la '
                                  'Confederación norteamericana'],
                 'correcta': 'E'},
                {'pregunta': 'En el siglo XVIII, se consideraba «todo el '
                             'pueblo» al llamado:',
                 'alternativas': ['Segundo Estado',
                                  'Tercer Estado, compuesto por la burguesía',
                                  'Cuarto Estado',
                                  'Primer Estado',
                                  'Estado eclesiástico'],
                 'correcta': 'B'},
                {'pregunta': 'Rousseau llamó «leyes fundamentales» a:',
                 'alternativas': ['La estructura jurídica correspondiente al '
                                  'régimen político',
                                  'Los tratados internacionales',
                                  'Las costumbres sociales',
                                  'El derecho penal',
                                  'La estructura de poder'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución constituye, define y crea los '
                             'poderes:',
                 'alternativas': ['Ninguno en particular',
                                  'Legislativo, ejecutivo y judicial',
                                  'Solo el legislativo',
                                  'Solo el judicial',
                                  'Solo el ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'Una Constitución contenida en un documento '
                             'formal se llama Constitución:',
                 'alternativas': ['Semántica',
                                  'Consuetudinaria',
                                  'Escrita',
                                  'Nominal',
                                  'Flexible'],
                 'correcta': 'C'},
                {'pregunta': 'Las Constituciones que nacen de un acto '
                             'voluntario del Rey, cediendo poderes al '
                             'Parlamento, se llaman:',
                 'alternativas': ['Populares',
                                  'Otorgadas',
                                  'Rígidas',
                                  'Derivadas',
                                  'Pactadas'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que surgen de un '
                             'convenio-pacto entre el Rey y el Parlamento se '
                             'llaman:',
                 'alternativas': ['Pactadas',
                                  'Flexibles',
                                  'Populares',
                                  'Otorgadas',
                                  'Originarias'],
                 'correcta': 'A'},
                {'pregunta': 'Las Constituciones que pueden modificarse por '
                             'el procedimiento legislativo ordinario se '
                             'llaman:',
                 'alternativas': ['Rígidas',
                                  'Otorgadas',
                                  'Derivadas',
                                  'Flexibles',
                                  'Semánticas'],
                 'correcta': 'D'},
                {'pregunta': 'Las Constituciones que requieren un '
                             'procedimiento complejo para su reforma se '
                             'llaman:',
                 'alternativas': ['Nominales',
                                  'Originarias',
                                  'Flexibles',
                                  'Rígidas',
                                  'Pactadas'],
                 'correcta': 'D'},
                {'pregunta': 'Las Constituciones cargadas de un programa '
                             'ideológico se llaman:',
                 'alternativas': ['Nominales',
                                  'Derivadas',
                                  'Utilitarias',
                                  'Semánticas',
                                  'Ideológicas'],
                 'correcta': 'E'},
                {'pregunta': 'Según la clasificación de Loewenstein, la '
                             'Constitución efectivamente vivida por '
                             'gobernantes y gobernados se llama:',
                 'alternativas': ['Rígida',
                                  'Semántica',
                                  'Utilitaria',
                                  'Normativa',
                                  'Nominal'],
                 'correcta': 'D'},
                {'pregunta': 'Según Loewenstein, la Constitución que sirve '
                             'para estabilizar y eternizar el poder de los '
                             'dominadores se llama:',
                 'alternativas': ['Nominal',
                                  'Flexible',
                                  'Normativa',
                                  'Semántica',
                                  'Ideológica'],
                 'correcta': 'D'},
                {'pregunta': 'El creador de la jerarquía normativa '
                             'piramidal, conocida como «pirámide de Kelsen», '
                             'fue:',
                 'alternativas': ['Montesquieu',
                                  'Locke',
                                  'Rousseau',
                                  'Hans Kelsen',
                                  'Aristóteles'],
                 'correcta': 'D'},
                {'pregunta': 'Kelsen esquematizó la jerarquía normativa en '
                             'su obra «La Teoría Pura del Derecho», '
                             'publicada en:',
                 'alternativas': ['1900', '1934', '1960', '1945', '1919'],
                 'correcta': 'B'},
                {'pregunta': 'El primer nivel de la jerarquía normativa '
                             'peruana es:',
                 'alternativas': ['Los decretos supremos',
                                  'Los tratados',
                                  'Las leyes ordinarias',
                                  'Las resoluciones',
                                  'La Constitución'],
                 'correcta': 'E'},
                {'pregunta': 'El segundo nivel de la jerarquía normativa '
                             'incluye tratados, leyes y:',
                 'alternativas': ['Resoluciones legislativas',
                                  'Directivas internas',
                                  'Memorandos',
                                  'Circulares',
                                  'Ordenanzas municipales'],
                 'correcta': 'A'},
                {'pregunta': 'El funcionario facultado para celebrar '
                             'tratados internacionales del Perú es:',
                 'alternativas': ['El Congreso',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'El Presidente de la República',
                                  'La Contraloría'],
                 'correcta': 'D'},
                {'pregunta': 'Las leyes que instauran el marco normativo de '
                             'instituciones del Estado y requieren mayoría '
                             'calificada se llaman leyes:',
                 'alternativas': ['Ordinarias',
                                  'Resolutivas',
                                  'Reglamentarias',
                                  'Orgánicas',
                                  'Supletorias'],
                 'correcta': 'D'},
                {'pregunta': 'El Decreto de Urgencia lo dicta el Presidente '
                             'y lo aprueba:',
                 'alternativas': ['El Poder Judicial',
                                  'La Contraloría',
                                  'El Consejo de Ministros',
                                  'El Congreso',
                                  'El Tribunal Constitucional'],
                 'correcta': 'C'},
                {'pregunta': 'El Congreso de la República del Perú es de '
                             'tipo:',
                 'alternativas': ['Regional',
                                  'Mixto',
                                  'Unicameral',
                                  'Bicameral',
                                  'Tricameral'],
                 'correcta': 'C'},
                {'pregunta': 'El número de congresistas que integran el '
                             'Congreso de la República es:',
                 'alternativas': ['110', '120', '100', '130', '150'],
                 'correcta': 'D'},
                {'pregunta': 'El titular del poder constituyente viene a '
                             'ser: (II CEPRU 2025-I)',
                 'alternativas': ['El pueblo',
                                  'La ONU',
                                  'El presidente',
                                  'El congreso',
                                  'El Estado'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 43 de la Constitución, son '
                             'características del gobierno del Perú: (III '
                             'CEPRU 2025-I)',
                 'alternativas': ['Democrático - social - unitario',
                                  'Independiente - democrático - soberano',
                                  'Uno e indivisible',
                                  'Unitario - representativo - '
                                  'descentralizado',
                                  'Inviolable - inalienable'],
                 'correcta': 'D'},
                {'pregunta': 'La norma fundamental del Estado que establece '
                             'la organización de sus poderes, la competencia '
                             'de estos y la posición de la persona en '
                             'relación con el Estado, es: (II CEPRU 2023-II)',
                 'alternativas': ['La resolución',
                                  'La Constitución',
                                  'El reglamento',
                                  'La ley',
                                  'El decreto'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho de todo ciudadano de presentar uno '
                             'o más proyectos de ley se denomina: (II CEPRU '
                             '2023-II)',
                 'alternativas': ['Iniciativa Legislativa',
                                  'Referéndum',
                                  'Revocatoria',
                                  'Remoción',
                                  'Iniciativa de reforma Constitucional'],
                 'correcta': 'A'},
                {'pregunta': '¿Con qué Constitución se aprobó el voto a los '
                             'analfabetos? (II CEPRU 2022-II)',
                 'alternativas': ['Constitución de 1979',
                                  'Constitución de 1920',
                                  'Constitución de 1993',
                                  'Constitución de 1933',
                                  'Constitución de 1956'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución Política del Estado de 1993, '
                             'durante el gobierno del ex presidente Alberto '
                             'Fujimori, fue redactada por el: (II CEPRU '
                             '2022-II)',
                 'alternativas': ['Congreso Ejecutivo democrático',
                                  'Poder Legislativo democrático',
                                  'Poder constituyente democrático',
                                  'Poder constituido democrático',
                                  'Congreso constituyente democrático'],
                 'correcta': 'E'},
                {'pregunta': 'La parte de la Constitución que expresa los '
                             'valores, principios y necesidades de un '
                             'pueblo, previa a las normas numeradas, se '
                             'llama:',
                 'alternativas': ['Declaración',
                                  'Cláusula de reforma',
                                  'Preámbulo',
                                  'Parte dogmática',
                                  'Parte orgánica'],
                 'correcta': 'C'},
                {'pregunta': 'La parte de la Constitución que contiene los '
                             'principios pilares y los derechos '
                             'fundamentales de los ciudadanos se llama '
                             'parte:',
                 'alternativas': ['Preambular',
                                  'Dogmática',
                                  'Declarativa',
                                  'Orgánica',
                                  'Transitoria'],
                 'correcta': 'B'},
                {'pregunta': 'La parte de la Constitución que determina la '
                             'estructura del Estado y organiza los poderes '
                             'públicos se llama parte:',
                 'alternativas': ['Complementaria',
                                  'Declarativa',
                                  'Orgánica',
                                  'Dogmática',
                                  'Preambular'],
                 'correcta': 'C'},
                {'pregunta': 'La garantía de la rigidez constitucional que '
                             'condiciona la reforma parcial o total de la '
                             'Constitución se llama:',
                 'alternativas': ['Preámbulo',
                                  'Parte orgánica',
                                  'Parte dogmática',
                                  'Cláusula de reforma',
                                  'Declaración'],
                 'correcta': 'D'},
                {'pregunta': 'El poder «creador del Estado», al que '
                             'corresponde establecer la Constitución, se '
                             'llama poder:',
                 'alternativas': ['Constituyente',
                                  'Ejecutivo',
                                  'Judicial',
                                  'Constituido',
                                  'Legislativo'],
                 'correcta': 'A'},
                {'pregunta': 'El poder constituyente se caracteriza por ser '
                             'originario, extraordinario y:',
                 'alternativas': ['Limitado',
                                  'Absoluto',
                                  'Ordinario',
                                  'Condicionado',
                                  'Derivado'],
                 'correcta': 'B'},
                {'pregunta': 'A diferencia del poder constituyente, el poder '
                             'constituido es derivado, ordinario y:',
                 'alternativas': ['Absoluto',
                                  'Extraordinario',
                                  'Soberano',
                                  'Limitado',
                                  'Originario'],
                 'correcta': 'D'},
                {'pregunta': 'En una sociedad democrática, existe consenso '
                             'en que la titularidad del poder constituyente '
                             'corresponde a:',
                 'alternativas': ['El pueblo',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'El presidente',
                                  'Los partidos políticos'],
                 'correcta': 'A'}],
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
                     {'titulo': 'LAS CINCO PARTES DE LA CONSTITUCIÓN PERUANA',
                      'items': ['El preámbulo es un enunciado previo a las '
                                'normas, que expresa los valores, principios '
                                'y necesidades de un pueblo.',
                                'La parte dogmática contiene los principios '
                                'pilares de la constitución: los derechos '
                                'fundamentales y garantías individuales.',
                                'La parte orgánica determina la estructura '
                                'del Estado, organizando los poderes '
                                'públicos.',
                                'La cláusula de reforma es una garantía de '
                                'la rigidez constitucional, condicionando su '
                                'reforma parcial o total.',
                                'La declaración final del texto '
                                'constitucional declara al Perú país '
                                'vinculado a la Antártida, propiciando su '
                                'conservación como Zona de Paz.']},
                     {'titulo': 'PODER CONSTITUYENTE Y PODER CONSTITUIDO',
                      'items': ['El poder constituyente es «el poder creador '
                                'del Estado» (Burdeau); a él corresponde '
                                'establecer la Constitución.',
                                'El poder constituyente es originario: su '
                                'fuente radica en sí mismo, sin derivar del '
                                'poder vigente ni del orden jurídico '
                                'establecido.',
                                'El poder constituyente es extraordinario: '
                                'solo aparece en circunstancias '
                                'excepcionales, como el nacimiento del '
                                'Estado.',
                                'El poder constituyente es absoluto: no está '
                                'limitado ni regulado por el derecho '
                                'vigente, gozando de libertad total.',
                                'El poder constituido, a diferencia del '
                                'constituyente, es derivado (nace de la '
                                'Constitución), ordinario (actúa '
                                'permanentemente) y limitado (sometido al '
                                'derecho vigente).',
                                'En una sociedad democrática, existe '
                                'consenso en que la titularidad del poder '
                                'constituyente corresponde al pueblo.']},
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
                                'carácter neutral.']},
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
                                'celebrarlos.']}],
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
                {'titulo': '8.3 CIUDADANÍA Y CARACTERÍSTICAS DEL SUFRAGIO',
                 'items': ['El artículo {30} de la Constitución establece '
                           'que son ciudadanos los peruanos mayores de {18} '
                           'años, requiriéndose la inscripción electoral.',
                           'Las características del derecho al voto son: '
                           'personal, {irrenunciable}, universal, igual, '
                           'libre, {secreto} y obligatorio hasta los 70 '
                           'años.',
                           'A la mujer se le reconoció el derecho al voto '
                           'municipal en la Constitución de {1933}, '
                           'efectivizándose en las elecciones municipales de '
                           '{1956}.',
                           'La mujer participó por primera vez en elecciones '
                           'presidenciales y congresales en {1962}.']},
                {'titulo': '8.4 EVOLUCIÓN HISTÓRICA DEL DERECHO AL VOTO EN '
                           'EL PERÚ',
                 'items': ['La Constitución de {1823} exigía ser peruano de '
                           'nacimiento, casado o mayor de 25 años, y saber '
                           'leer y escribir.',
                           'La Constitución de {1933} otorgó el voto a '
                           'peruanos varones mayores de edad y casados '
                           'mayores de 18, con obligatoriedad hasta los 70 '
                           'años.',
                           'En las elecciones de {1956}, por la ley de 1955, '
                           'se dio el voto a las mujeres.',
                           'En las elecciones de {1980}, por la Constitución '
                           'de 1979, se dio el voto a los analfabetos.',
                           'En las elecciones de {2006}, por ley del año '
                           '2005, se dio el voto a policías y militares.']},
                {'titulo': '8.5 EL SISTEMA ELECTORAL PERUANO',
                 'items': ['El {Jurado Nacional de Elecciones} (JNE) es un '
                           'organismo constitucionalmente autónomo, cuyo '
                           'pleno está integrado por {cinco} miembros de '
                           'distintas instancias.',
                           'El pleno del JNE es presidido por el '
                           'representante elegido por la {Sala Plena} de la '
                           'Corte Suprema de Justicia.',
                           'La {Oficina Nacional de Procesos Electorales} '
                           '(ONPE) organiza y ejecuta los procesos '
                           'electorales, de referéndum y otras consultas '
                           'populares.',
                           'El {RENIEC} (Registro Nacional de Identificación '
                           'y Estado Civil) se creó mediante Ley N.º '
                           '{26497}, como organismo autónomo con personería '
                           'jurídica.',
                           'El artículo {35} de la Constitución establece '
                           'que los ciudadanos pueden ejercer sus derechos '
                           'individualmente o a través de {organizaciones '
                           'políticas}.']},
                {'titulo': '8.6 LEY DE PARTICIPACIÓN Y CONTROL CIUDADANO '
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
                {'titulo': '8.7 DERECHOS DE PARTICIPACIÓN CIUDADANA',
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
                {'titulo': '8.8 DERECHOS DE CONTROL DE LOS CIUDADANOS',
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
                 'alternativas': ['1976', '2000', '1948', '1966', '1993'],
                 'correcta': 'D'},
                {'pregunta': 'El PIDCP entró en vigor el:',
                 'alternativas': ['10 de diciembre de 1948',
                                  '1 de enero de 1980',
                                  '23 de marzo de 1976',
                                  '30 de abril de 1990',
                                  '16 de diciembre de 1966'],
                 'correcta': 'C'},
                {'pregunta': 'El PIDCP ha sido ratificado por un total de '
                             'Estados de:',
                 'alternativas': ['100', '75', '50', '167', '200'],
                 'correcta': 'D'},
                {'pregunta': 'El PIDCP consta de un número de partes igual '
                             'a:',
                 'alternativas': ['3', '6', '10', '4', '8'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP consta de un número de artículos '
                             'igual a:',
                 'alternativas': ['25', '30', '75', '100', '53'],
                 'correcta': 'E'},
                {'pregunta': 'El Primer Protocolo Facultativo del PIDCP '
                             'regula:',
                 'alternativas': ['Los derechos económicos',
                                  'El comercio internacional',
                                  'Los mecanismos de denuncia contra los '
                                  'Estados',
                                  'La migración',
                                  'La abolición de la pena de muerte'],
                 'correcta': 'C'},
                {'pregunta': 'El Segundo Protocolo Facultativo del PIDCP '
                             'está destinado a:',
                 'alternativas': ['La abolición de la pena de muerte',
                                  'La protección ambiental',
                                  'Los derechos laborales',
                                  'El comercio exterior',
                                  'El mecanismo de denuncias'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos civiles se distinguen de los '
                             'derechos naturales porque son:',
                 'alternativas': ['Reconocidos dentro de un Estado '
                                  'determinado',
                                  'Universales sin excepción',
                                  'Otorgados por organismos internacionales',
                                  'Internacionales por naturaleza',
                                  'Innatos al nacer'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos naturales o humanos se poseen:',
                 'alternativas': ['Solo a partir de la mayoría de edad',
                                  'Solo si el Estado los otorga',
                                  'Por el mero hecho de nacer',
                                  'Solo en democracias',
                                  'Únicamente si se solicitan'],
                 'correcta': 'C'},
                {'pregunta': 'John Locke sostuvo que debían convertirse en '
                             'derechos civiles protegidos por el Estado:',
                 'alternativas': ['Solo el derecho a la propiedad',
                                  'Los derechos económicos',
                                  'Solo el derecho a la vida',
                                  'La vida, la libertad y la propiedad',
                                  'Los derechos culturales'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho considerado el primero de todos, '
                             'generador de cualquier otro derecho, es el '
                             'derecho a:',
                 'alternativas': ['La libertad de expresión',
                                  'La vida',
                                  'La propiedad',
                                  'El trabajo',
                                  'La educación'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho a la integridad física y '
                             'psicológica protege contra:',
                 'alternativas': ['La libre expresión',
                                  'El comercio informal',
                                  'Los impuestos elevados',
                                  'La migración',
                                  'Las torturas y tratos crueles e '
                                  'inhumanos'],
                 'correcta': 'E'},
                {'pregunta': 'El derecho a la identidad comprende, entre '
                             'otros aspectos:',
                 'alternativas': ['El derecho a tener un nombre y documento '
                                  'de identidad',
                                  'El derecho al voto',
                                  'El derecho a la propiedad',
                                  'El derecho al trabajo',
                                  'El derecho a la educación superior'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos políticos permiten participar en:',
                 'alternativas': ['La vida privada únicamente',
                                  'El comercio internacional',
                                  'Solo actividades económicas',
                                  'El gobierno del Estado y la toma de '
                                  'decisiones',
                                  'Solo actividades religiosas'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos políticos están reconocidos por:',
                 'alternativas': ['Solo tratados internacionales',
                                  'La Constitución y las leyes',
                                  'Solo la costumbre',
                                  'Organismos privados',
                                  'Ninguna norma específica'],
                 'correcta': 'B'},
                {'pregunta': 'La Parte III del PIDCP, artículos 6 a 27, '
                             'protege contra:',
                 'alternativas': ['La contaminación ambiental',
                                  'El desempleo',
                                  'La evasión tributaria',
                                  'El comercio desleal',
                                  'La discriminación por sexo, religión, '
                                  'raza u otras formas'],
                 'correcta': 'E'},
                {'pregunta': 'La Parte I del PIDCP, artículo 1, trata sobre:',
                 'alternativas': ['La pena de muerte',
                                  'El comercio internacional',
                                  'Los tratados bilaterales',
                                  'La migración',
                                  'La libre determinación de los pueblos'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDCP es catalogado como un tratado '
                             'internacional de tipo:',
                 'alternativas': ['Multilateral general',
                                  'Regional exclusivo',
                                  'Bilateral',
                                  'Privado',
                                  'Comercial'],
                 'correcta': 'A'},
                {'pregunta': 'La contraposición al derecho a la vida es:',
                 'alternativas': ['La discapacidad',
                                  'El envejecimiento',
                                  'La pobreza',
                                  'La enfermedad',
                                  'La muerte'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los derechos civiles y políticos '
                             'mencionados figura el derecho a elegir y:',
                 'alternativas': ['Ser elegido representante',
                                  'No participar',
                                  'No votar',
                                  'Rechazar la ciudadanía',
                                  'Evadir impuestos'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de los Derechos de Participación y '
                             'Control Ciudadano se conoce como Ley:',
                 'alternativas': ['28237',
                                  '26859',
                                  '26301',
                                  '26300',
                                  '27444'],
                 'correcta': 'D'},
                {'pregunta': 'Según la Ley 26300, los ciudadanos pueden '
                             'participar mediante referéndum, iniciativa '
                             'legislativa, remoción o:',
                 'alternativas': ['Censura',
                                  'Amnistía',
                                  'Revocación de autoridades',
                                  'Vacancia exclusiva',
                                  'Indulto'],
                 'correcta': 'C'},
                {'pregunta': 'Todo acto que prohíba o limite al ciudadano el '
                             'ejercicio de sus derechos de participación es '
                             'considerado:',
                 'alternativas': ['Nulo y punible',
                                  'Legal si está motivado',
                                  'Aceptable temporalmente',
                                  'Válido con restricciones',
                                  'Sujeto a apelación únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'La iniciativa de reforma constitucional '
                             'requiere la adhesión de un porcentaje de la '
                             'población electoral nacional igual a:',
                 'alternativas': ['1%', '0,3%', '25%', '10%', '3%'],
                 'correcta': 'B'},
                {'pregunta': 'Es improcedente toda iniciativa de reforma '
                             'constitucional que recorte los derechos '
                             'ciudadanos consagrados en el artículo:',
                 'alternativas': ['Artículo 1',
                                  'Artículo 10',
                                  'Artículo 5',
                                  'Artículo 2',
                                  'Artículo 20'],
                 'correcta': 'D'},
                {'pregunta': 'La iniciativa en la formación de leyes '
                             'requiere firmas de no menos del 0,3% del '
                             'electorado, y el Congreso tiene un plazo de:',
                 'alternativas': ['180 días',
                                  '30 días',
                                  '120 días',
                                  '60 días',
                                  '90 días'],
                 'correcta': 'C'},
                {'pregunta': 'El referéndum es el derecho de los ciudadanos '
                             'para pronunciarse sobre, entre otros temas, la '
                             'reforma de:',
                 'alternativas': ['Solo tratados internacionales',
                                  'La Constitución',
                                  'Solo decretos supremos',
                                  'Solo el presupuesto',
                                  'Solo ordenanzas municipales'],
                 'correcta': 'B'},
                {'pregunta': 'El referéndum puede ser solicitado por un '
                             'número de ciudadanos no menor a:',
                 'alternativas': ['50% del electorado',
                                  '10% del electorado',
                                  '5% del electorado',
                                  '25% del electorado',
                                  '0,3% del electorado'],
                 'correcta': 'B'},
                {'pregunta': 'Para que el referéndum sea válido, debe ser '
                             'aprobado por no menos del:',
                 'alternativas': ['50% de los votantes',
                                  '30% del total de votantes',
                                  '10% de los votantes',
                                  '90% de los votantes',
                                  '70% de los votantes'],
                 'correcta': 'B'},
                {'pregunta': 'Una norma aprobada mediante referéndum no '
                             'puede modificarse dentro de los siguientes:',
                 'alternativas': ['Cinco años',
                                  'Diez años',
                                  'Dos años',
                                  'Un año',
                                  'Seis meses'],
                 'correcta': 'C'},
                {'pregunta': 'La revocatoria es el derecho de la ciudadanía '
                             'para destituir de sus cargos a autoridades de '
                             'elección:',
                 'alternativas': ['Judicial exclusiva',
                                  'Eclesiástica',
                                  'Militar',
                                  'Popular',
                                  'Designada'],
                 'correcta': 'D'},
                {'pregunta': 'La revocatoria no procede durante el primer y '
                             'último año de mandato, salvo en el caso de:',
                 'alternativas': ['Alcaldes',
                                  'Regidores',
                                  'Magistrados',
                                  'Congresistas',
                                  'Ministros'],
                 'correcta': 'C'},
                {'pregunta': 'Para solicitar la revocatoria, la solicitud:',
                 'alternativas': ['Requiere sentencia previa',
                                  'Requiere referéndum previo',
                                  'Solo requiere ser fundamentada',
                                  'Debe ser probada judicialmente',
                                  'Necesita aprobación del Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'Para solicitar la revocatoria se requiere la '
                             'firma de al menos un porcentaje de electores '
                             'de la autoridad igual a:',
                 'alternativas': ['50%', '25%', '40%', '10%', '5%'],
                 'correcta': 'B'},
                {'pregunta': 'El número máximo de firmas requeridas para '
                             'solicitar una revocatoria es:',
                 'alternativas': ['250 000',
                                  '50 000',
                                  '100 000',
                                  '400 000',
                                  '1 000 000'],
                 'correcta': 'D'},
                {'pregunta': 'Para revocar a una autoridad se requiere la '
                             'mitad más uno de los votos, y que haya '
                             'asistido al menos:',
                 'alternativas': ['El 25% de electores hábiles',
                                  'El 10% de electores hábiles',
                                  'El 75% de electores hábiles',
                                  'El 50% de electores hábiles',
                                  'Todos los electores hábiles'],
                 'correcta': 'D'},
                {'pregunta': 'Si la revocatoria no procede, no se admite una '
                             'nueva petición hasta después de:',
                 'alternativas': ['Un año',
                                  'Nunca más',
                                  'Dos años',
                                  'Seis meses',
                                  'Cinco años'],
                 'correcta': 'C'},
                {'pregunta': 'Tras una revocatoria exitosa, asume el cargo:',
                 'alternativas': ['Ninguno, el cargo queda vacante',
                                  'El regidor de mayor edad',
                                  'El ganador de nuevas elecciones '
                                  'inmediatas',
                                  'Un candidato designado por el JNE',
                                  'Quien alcanzó el siguiente lugar en votos '
                                  'de la misma lista'],
                 'correcta': 'E'},
                {'pregunta': 'Un derecho constitucional conexo con la '
                             'libertad individual es: (II CEPRU 2018-I)',
                 'alternativas': ['El debido proceso',
                                  'La remuneración',
                                  'La petición de pensión',
                                  'La inviolabilidad científica',
                                  'La rectificación'],
                 'correcta': 'A'},
                {'pregunta': 'Una característica del derecho al voto es que '
                             'es: (II CEPRU 2022-I)',
                 'alternativas': ['Desigual',
                                  'Limitado',
                                  'Irrenunciable',
                                  'Impersonal',
                                  'Renunciable'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 30 de la Constitución, son '
                             'ciudadanos los peruanos mayores de:',
                 'alternativas': ['14 años',
                                  '21 años',
                                  '18 años',
                                  '16 años',
                                  '25 años'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las características del derecho al voto '
                             'en el Perú no se encuentra:',
                 'alternativas': ['Obligatorio hasta los 70 años',
                                  'Personal',
                                  'Secreto',
                                  'Universal',
                                  'Transferible'],
                 'correcta': 'E'},
                {'pregunta': 'A la mujer peruana se le reconoció el derecho '
                             'al voto en elecciones municipales en la '
                             'Constitución de:',
                 'alternativas': ['1993', '1956', '1933', '1979', '1920'],
                 'correcta': 'C'},
                {'pregunta': 'La mujer peruana participó por primera vez en '
                             'elecciones presidenciales y congresales en:',
                 'alternativas': ['1979', '1933', '1956', '1980', '1962'],
                 'correcta': 'E'},
                {'pregunta': 'En las elecciones de 1980, por mandato de la '
                             'Constitución de 1979, se otorgó el derecho al '
                             'voto a:',
                 'alternativas': ['Los menores de edad',
                                  'Los analfabetos',
                                  'Los militares y policías',
                                  'Las mujeres',
                                  'Los extranjeros'],
                 'correcta': 'B'},
                {'pregunta': 'En las elecciones de 2006, por ley del año '
                             '2005, se otorgó el derecho al voto a:',
                 'alternativas': ['Los extranjeros residentes',
                                  'Las mujeres',
                                  'Los policías y militares',
                                  'Los adolescentes',
                                  'Los analfabetos'],
                 'correcta': 'C'},
                {'pregunta': 'El pleno del Jurado Nacional de Elecciones '
                             'está integrado por un número de miembros igual '
                             'a:',
                 'alternativas': ['Cinco', 'Once', 'Nueve', 'Siete', 'Tres'],
                 'correcta': 'A'},
                {'pregunta': 'El pleno del Jurado Nacional de Elecciones es '
                             'presidido por el representante elegido por:',
                 'alternativas': ['El Poder Ejecutivo',
                                  'El Colegio de Abogados de Lima',
                                  'El Congreso',
                                  'La Sala Plena de la Corte Suprema de '
                                  'Justicia',
                                  'La Junta de Fiscales Supremos'],
                 'correcta': 'D'},
                {'pregunta': 'El organismo electoral encargado de organizar '
                             'y ejecutar los procesos electorales, de '
                             'referéndum y otras consultas populares es:',
                 'alternativas': ['El JEE',
                                  'El Congreso',
                                  'La ONPE',
                                  'El RENIEC',
                                  'El JNE'],
                 'correcta': 'C'},
                {'pregunta': 'El RENIEC se creó mediante la Ley N.º:',
                 'alternativas': ['26300',
                                  '26864',
                                  '27972',
                                  '28803',
                                  '26497'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución que establece '
                             'que los ciudadanos pueden ejercer sus derechos '
                             'a través de organizaciones políticas es el '
                             'artículo:',
                 'alternativas': ['Artículo 35',
                                  'Artículo 31',
                                  'Artículo 176',
                                  'Artículo 30',
                                  'Artículo 183'],
                 'correcta': 'A'}],
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
                     {'titulo': 'CIUDADANÍA Y CARACTERÍSTICAS DEL SUFRAGIO',
                      'items': ['El artículo 30 de la Constitución establece '
                                'que son ciudadanos los peruanos mayores de '
                                '18 años, requiriéndose la inscripción '
                                'electoral.',
                                'Las características del derecho al voto '
                                'son: personal, irrenunciable, universal, '
                                'igual, libre, secreto y obligatorio hasta '
                                'los 70 años.',
                                'A la mujer se le reconoció el derecho al '
                                'voto municipal en la Constitución de 1933, '
                                'efectivizándose en las elecciones '
                                'municipales de 1956.',
                                'La mujer participó por primera vez en '
                                'elecciones presidenciales y congresales en '
                                '1962.']},
                     {'titulo': 'EVOLUCIÓN HISTÓRICA DEL DERECHO AL VOTO EN '
                                'EL PERÚ',
                      'items': ['La Constitución de 1823 exigía ser peruano '
                                'de nacimiento, casado o mayor de 25 años, y '
                                'saber leer y escribir.',
                                'La Constitución de 1933 otorgó el voto a '
                                'peruanos varones mayores de edad y casados '
                                'mayores de 18, con obligatoriedad hasta los '
                                '70 años.',
                                'En las elecciones de 1956, por la ley de '
                                '1955, se dio el voto a las mujeres.',
                                'En las elecciones de 1980, por la '
                                'Constitución de 1979, se dio el voto a los '
                                'analfabetos.',
                                'En las elecciones de 2006, por ley del año '
                                '2005, se dio el voto a policías y '
                                'militares.']},
                     {'titulo': 'EL SISTEMA ELECTORAL PERUANO',
                      'items': ['El Jurado Nacional de Elecciones (JNE) es '
                                'un organismo constitucionalmente autónomo, '
                                'cuyo pleno está integrado por cinco '
                                'miembros de distintas instancias.',
                                'El pleno del JNE es presidido por el '
                                'representante elegido por la Sala Plena de '
                                'la Corte Suprema de Justicia.',
                                'La Oficina Nacional de Procesos Electorales '
                                '(ONPE) organiza y ejecuta los procesos '
                                'electorales, de referéndum y otras '
                                'consultas populares.',
                                'El RENIEC (Registro Nacional de '
                                'Identificación y Estado Civil) se creó '
                                'mediante Ley N.º 26497, como organismo '
                                'autónomo con personería jurídica.',
                                'El artículo 35 de la Constitución establece '
                                'que los ciudadanos pueden ejercer sus '
                                'derechos individualmente o a través de '
                                'organizaciones políticas.']},
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
                                'votantes.']},
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
                                'años.']}],
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
                 'alternativas': ['Solo el sufragio',
                                  'Solo la libertad de tránsito',
                                  'Un nivel de vida adecuado, alimentación y '
                                  'vivienda digna',
                                  'Solo la nacionalidad',
                                  'Solo la propiedad privada'],
                 'correcta': 'C'},
                {'pregunta': 'El Protocolo Adicional a la Convención '
                             'Americana en materia de derechos económicos, '
                             'sociales y culturales se conoce como:',
                 'alternativas': ['Protocolo de Nueva York',
                                  'Protocolo de San Salvador',
                                  'Protocolo de Lima',
                                  'Protocolo de Ginebra',
                                  'Protocolo de Roma'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hakansson, estos derechos representan la '
                             'función del Estado de:',
                 'alternativas': ['Limitar la educación',
                                  'Aumentar impuestos',
                                  'Equilibrar las desigualdades sociales',
                                  'Reducir el gasto público',
                                  'Privatizar servicios'],
                 'correcta': 'C'},
                {'pregunta': 'El valor básico que fundamenta todos los '
                             'derechos humanos es:',
                 'alternativas': ['La nacionalidad',
                                  'El poder político',
                                  'La religión',
                                  'La dignidad de la persona humana',
                                  'La riqueza'],
                 'correcta': 'D'},
                {'pregunta': 'Según Nogueira, la dignidad humana fundamenta:',
                 'alternativas': ['Solo los derechos civiles',
                                  'Tanto los derechos civiles y políticos '
                                  'como los económicos, sociales y '
                                  'culturales',
                                  'Ningún derecho en particular',
                                  'Solo los derechos culturales',
                                  'Solo los derechos económicos'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 22 de la Constitución establece '
                             'que el trabajo es:',
                 'alternativas': ['Un privilegio',
                                  'Un deber y un derecho',
                                  'Solo un derecho opcional',
                                  'Una actividad comercial',
                                  'Solo una obligación'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 22, el trabajo es la base '
                             'de:',
                 'alternativas': ['El comercio exterior',
                                  'El bienestar social',
                                  'El sistema bancario',
                                  'La recaudación fiscal',
                                  'La política monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 23 de la Constitución protege '
                             'especialmente a:',
                 'alternativas': ['Solo a los sindicatos',
                                  'Solo a los empresarios',
                                  'Solo al Estado',
                                  'A los extranjeros exclusivamente',
                                  'A la madre, al menor de edad y al '
                                  'impedido que trabajan'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 23, ninguna relación laboral '
                             'puede:',
                 'alternativas': ['Fijar un sueldo',
                                  'Exigir puntualidad',
                                  'Solicitar experiencia',
                                  'Limitar los derechos constitucionales ni '
                                  'rebajar la dignidad del trabajador',
                                  'Establecer horarios'],
                 'correcta': 'D'},
                {'pregunta': 'Según la Constitución, nadie está obligado a '
                             'prestar trabajo:',
                 'alternativas': ['Los fines de semana',
                                  'Fuera de su ciudad',
                                  'Sin retribución o sin su libre '
                                  'consentimiento',
                                  'Para el Estado',
                                  'En el sector privado'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 24 de la Constitución establece el '
                             'derecho del trabajador a:',
                 'alternativas': ['Trabajo garantizado de por vida',
                                  'Doble sueldo',
                                  'Una remuneración equitativa y suficiente',
                                  'Vacaciones ilimitadas',
                                  'Ascenso automático'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado promueve condiciones para el '
                             'progreso social y económico mediante:',
                 'alternativas': ['La reducción del gasto en educación',
                                  'Políticas de fomento del empleo '
                                  'productivo y educación para el trabajo',
                                  'La eliminación de sindicatos',
                                  'El cierre de empresas',
                                  'El aumento de impuestos únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos, '
                             'en su preámbulo, señala que todo individuo y '
                             'órgano de la sociedad debe:',
                 'alternativas': ['Promover el respeto a los derechos '
                                  'humanos',
                                  'Rechazar tratados internacionales',
                                  'Depender del Estado',
                                  'Limitar la participación ciudadana',
                                  'Ignorar los derechos humanos'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos sociales y económicos buscan que '
                             'los ciudadanos gocen de:',
                 'alternativas': ['Solo prestigio social',
                                  'Solo poder político',
                                  'Un estado de bienestar',
                                  'Solo riqueza material',
                                  'Ninguna prestación estatal'],
                 'correcta': 'C'},
                {'pregunta': 'Según el texto, la persona, en virtud de su '
                             'dignidad, se convierte en:',
                 'alternativas': ['Un medio para el Estado',
                                  'Un sujeto pasivo sin derechos',
                                  'El fin del Estado',
                                  'Un elemento secundario',
                                  'Un obstáculo para el desarrollo'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado, según Nogueira, está al servicio '
                             'de:',
                 'alternativas': ['La persona humana',
                                  'El mercado',
                                  'Solo el gobierno de turno',
                                  'Las empresas privadas',
                                  'Los organismos internacionales'],
                 'correcta': 'A'},
                {'pregunta': 'La finalidad del Estado, según el texto, es '
                             'promover:',
                 'alternativas': ['La expansión territorial',
                                  'El crecimiento demográfico',
                                  'El comercio exterior únicamente',
                                  'El bien común',
                                  'Solo la recaudación fiscal'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los instrumentos con jerarquía '
                             'constitucional que contemplan estos derechos '
                             'figura:',
                 'alternativas': ['Solo la Constitución peruana',
                                  'Ninguno en particular',
                                  'Solo el Código Civil',
                                  'La Declaración Universal de Derechos '
                                  'Humanos',
                                  'Solo el Código Penal'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de dignidad humana implica que '
                             'los derechos se reconozcan:',
                 'alternativas': ['Solo a ciertos grupos',
                                  'Solo a los trabajadores formales',
                                  'Solo a los adultos',
                                  'Sin distingo de tipo cultural, económico '
                                  'o social',
                                  'Solo a los ciudadanos con recursos'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos sociales y económicos '
                             'representan, según el texto:',
                 'alternativas': ['Los fines sociales del Estado',
                                  'Obligaciones exclusivas del ciudadano',
                                  'Normas sin aplicación práctica',
                                  'Una carga innecesaria',
                                  'Privilegios de unos pocos'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 7° de la Constitución establece '
                             'que todos tienen derecho a la protección de:',
                 'alternativas': ['Su libertad exclusiva',
                                  'Su honor exclusivo',
                                  'Su salud',
                                  'Su patrimonio',
                                  'Su intimidad exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 9° de la Constitución señala que '
                             'el Estado determina la política nacional de:',
                 'alternativas': ['Educación',
                                  'Salud',
                                  'Vivienda',
                                  'Seguridad',
                                  'Trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 11° de la Constitución garantiza '
                             'el libre acceso a prestaciones de salud y:',
                 'alternativas': ['Educación gratuita',
                                  'Vivienda',
                                  'Vacaciones pagadas',
                                  'Empleo garantizado',
                                  'Pensiones'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los cuatro aspectos que garantizan la '
                             'salud según la Constitución están '
                             'disponibilidad, accesibilidad, aceptabilidad '
                             'y:',
                 'alternativas': ['Gratuidad total',
                                  'Rapidez',
                                  'Calidad',
                                  'Anonimato',
                                  'Exclusividad'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 13° de la Constitución establece '
                             'que la educación tiene como finalidad el '
                             'desarrollo:',
                 'alternativas': ['Solo intelectual',
                                  'Exclusivamente profesional',
                                  'Integral de la persona humana',
                                  'Militar de la nación',
                                  'Económico del país'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 14° establece que la enseñanza de '
                             'la Constitución y los derechos humanos es:',
                 'alternativas': ['Solo para educación militar',
                                  'Solo para universidades',
                                  'Prohibida en colegios religiosos',
                                  'Obligatoria en todo el proceso educativo',
                                  'Opcional'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 15° de la Constitución establece '
                             'que el profesorado en la enseñanza oficial es:',
                 'alternativas': ['Cargo de confianza',
                                  'Servicio voluntario',
                                  'Trabajo temporal',
                                  'Función privada',
                                  'Carrera pública'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 17° establece que la educación '
                             'inicial, primaria y secundaria son:',
                 'alternativas': ['Solo para quienes puedan pagarlas',
                                  'Obligatorias',
                                  'Solo secundarias',
                                  'Opcionales',
                                  'Exclusivas del sector privado'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 18° establece que la educación '
                             'universitaria tiene como fines la formación '
                             'profesional, la difusión cultural, la creación '
                             'intelectual y:',
                 'alternativas': ['La religión oficial',
                                  'El comercio exterior',
                                  'La investigación científica y tecnológica',
                                  'El deporte exclusivo',
                                  'La política partidaria'],
                 'correcta': 'C'},
                {'pregunta': 'Cada universidad, según la Constitución, es '
                             'autónoma en su régimen normativo, de gobierno, '
                             'académico, administrativo y:',
                 'alternativas': ['Militar',
                                  'Diplomático',
                                  'Judicial',
                                  'Religioso',
                                  'Económico'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDESC (Pacto Internacional de Derechos '
                             'Económicos, Sociales y Culturales) fue '
                             'adoptado por la Asamblea General de la ONU en:',
                 'alternativas': ['1966', '1976', '1993', '1989', '1948'],
                 'correcta': 'A'},
                {'pregunta': 'El PIDESC entró en vigor el 3 de enero de:',
                 'alternativas': ['1993', '1976', '1989', '1948', '1966'],
                 'correcta': 'B'},
                {'pregunta': 'El Protocolo de San Salvador entiende el '
                             'derecho a la salud como el disfrute del más '
                             'alto nivel de bienestar físico, mental y:',
                 'alternativas': ['Social',
                                  'Religioso',
                                  'Espiritual',
                                  'Político',
                                  'Económico'],
                 'correcta': 'A'},
                {'pregunta': 'El Pacto Internacional de los Derechos '
                             'Económicos, Sociales y Culturales se aprobó en '
                             'la asamblea general de: (II CEPRU 2025-I)',
                 'alternativas': ['El CEPAL',
                                  'La ONU',
                                  'La OEA',
                                  'La OTAN',
                                  'La CAN'],
                 'correcta': 'B'},
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
                 'alternativas': ['Trabajo',
                                  'Paz',
                                  'Salud',
                                  'Medio Ambiente',
                                  'Educación'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho que constituye la base del '
                             'bienestar social y un medio de realización de '
                             'la persona es: (II CEPRU 2022-II)',
                 'alternativas': ['El trabajo',
                                  'La cultura',
                                  'El conocimiento',
                                  'La educación',
                                  'La salud'],
                 'correcta': 'A'}],
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
                {'titulo': '10.4 FUNCIÓN DE CONTROL O FISCALIZACIÓN',
                 'items': ['El Parlamento tiene, además de la legislativa, '
                           'una {función de control o fiscalización} del '
                           'gobierno.',
                           'Esta función presenta dos modalidades: el '
                           'control {político} y el control jurídico o de '
                           'legalidad.',
                           'En la responsabilidad {política}, el Parlamento '
                           'ejerce la potestad de juzgar la actividad de '
                           'quienes ejercen el gobierno.',
                           'Los mecanismos del control político incluyen las '
                           '{preguntas}, la interpelación, las comisiones '
                           'investigadoras y la invitación a informar.',
                           'El {control jurídico} o de legalidad busca '
                           'determinar si un funcionario público ha '
                           'infringido la ley o la Constitución.']},
                {'titulo': '10.5 LA FUNCIÓN REPRESENTATIVA Y COMPOSICIÓN DEL '
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
                {'titulo': '10.6 ÓRGANOS DEL PODER LEGISLATIVO',
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
                {'titulo': '10.7 ATRIBUCIONES DEL CONGRESO Y FUNCIÓN DEL '
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
                 'alternativas': ['Ejecutar el presupuesto',
                                  'Administrar justicia',
                                  'Dictar, modificar, interpretar y derogar '
                                  'leyes',
                                  'Nombrar ministros',
                                  'Firmar tratados exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano que ejerce la potestad legislativa '
                             'se denomina:',
                 'alternativas': ['Tribunal Constitucional',
                                  'Parlamento',
                                  'Poder Judicial',
                                  'Jurado Electoral',
                                  'Poder Ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 91 de la Constitución, el '
                             'Poder Legislativo reside en:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'Los gobiernos regionales',
                                  'El Presidente',
                                  'El Congreso',
                                  'El Poder Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'Poder Legislativo y Congreso de la República '
                             'son, conceptualmente:',
                 'alternativas': ['Idénticos en toda circunstancia',
                                  'Exactamente lo mismo',
                                  'Términos intercambiables sin matices',
                                  'Categorías conceptuales distintas',
                                  'Sinónimos absolutos'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente de la República puede expedir '
                             'normas con rango de ley llamadas:',
                 'alternativas': ['Decretos de Urgencia y Decretos '
                                  'Legislativos',
                                  'Directivas internas',
                                  'Resoluciones administrativas',
                                  'Circulares',
                                  'Ordenanzas municipales'],
                 'correcta': 'A'},
                {'pregunta': 'En regímenes de facto, se gobierna mediante:',
                 'alternativas': ['Directivas',
                                  'Decretos Ley',
                                  'Decretos Supremos',
                                  'Ordenanzas',
                                  'Resoluciones Ministeriales'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Locales expiden normas con rango '
                             'de ley llamadas:',
                 'alternativas': ['Resoluciones Legislativas',
                                  'Decretos de Urgencia',
                                  'Normas generales',
                                  'Decretos Legislativos',
                                  'Ordenanzas Municipales'],
                 'correcta': 'E'},
                {'pregunta': 'Los Gobiernos Regionales expiden normas con '
                             'rango de ley denominadas:',
                 'alternativas': ['Resoluciones Ministeriales',
                                  'Decretos Supremos',
                                  'Ordenanzas Municipales',
                                  'Normas generales',
                                  'Decretos Ley'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 102 de la Constitución establece '
                             'que dar leyes es atribución de:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'El Congreso',
                                  'El Poder Ejecutivo',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'C'},
                {'pregunta': 'La fase introductoria del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La iniciativa para proponer un proyecto '
                                  'de ley',
                                  'La publicación en el diario oficial',
                                  'La promulgación de la ley',
                                  'El veto presidencial',
                                  'La votación final'],
                 'correcta': 'A'},
                {'pregunta': 'La iniciativa popular en el Perú requiere '
                             'representar de la población electoral:',
                 'alternativas': ['3%', '30%', '10%', '0,3%', '1%'],
                 'correcta': 'D'},
                {'pregunta': 'La fase constitutiva del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La publicación oficial',
                                  'La promulgación',
                                  'La iniciativa del proyecto',
                                  'El archivo del proyecto',
                                  'La deliberación y aprobación de la ley '
                                  'por el Congreso'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 105, todo proyecto de ley '
                             'debe ser previamente:',
                 'alternativas': ['Consultado con el pueblo',
                                  'Aprobado por el Poder Judicial',
                                  'Dictaminado por una comisión',
                                  'Publicado en un diario',
                                  'Traducido a lenguas originarias'],
                 'correcta': 'C'},
                {'pregunta': 'Las leyes ordinarias en el Congreso se '
                             'aprueban por:',
                 'alternativas': ['Consenso obligatorio',
                                  'Mayoría simple',
                                  'Unanimidad',
                                  'Dos tercios',
                                  'Mayoría calificada'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes orgánicas requieren el voto de:',
                 'alternativas': ['Todos los congresistas',
                                  'Un tercio de los congresistas',
                                  'Solo la mesa directiva',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'La mayoría relativa'],
                 'correcta': 'D'},
                {'pregunta': 'La promulgación de la ley es realizada por:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El Presidente de la República',
                                  'El presidente del Congreso',
                                  'El Poder Judicial',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'La promulgación consiste en que el Jefe de '
                             'Estado:',
                 'alternativas': ['Rubrique la ley y ordene su publicación',
                                  'Elabore el proyecto',
                                  'Redacte la ley',
                                  'Modifique el texto legal',
                                  'Vote la ley'],
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
                 'alternativas': ['102', '105', '108', '91', '206'],
                 'correcta': 'E'},
                {'pregunta': 'El derecho de iniciativa legislativa, además '
                             'del Legislativo y Ejecutivo, se otorga también '
                             'a:',
                 'alternativas': ['Solo al sector privado',
                                  'El Poder Judicial, gobiernos regionales, '
                                  'locales y colegios profesionales',
                                  'Solo a organismos internacionales',
                                  'Solo a las universidades',
                                  'Solo a los partidos políticos'],
                 'correcta': 'B'},
                {'pregunta': 'Mediante la función representativa, los '
                             'congresistas actúan como voceros de:',
                 'alternativas': ['Los ciudadanos',
                                  'El Poder Ejecutivo',
                                  'El Poder Judicial',
                                  'Los organismos internacionales',
                                  'Las Fuerzas Armadas'],
                 'correcta': 'A'},
                {'pregunta': 'El Congreso de la República está integrado por '
                             'un número de parlamentarios igual a:',
                 'alternativas': ['150', '130', '120', '110', '100'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo del mandato congresal en el Perú es '
                             'de:',
                 'alternativas': ['7 años',
                                  '3 años',
                                  '4 años',
                                  '5 años',
                                  '6 años'],
                 'correcta': 'D'},
                {'pregunta': 'Los congresistas no pueden ser reelegidos de '
                             'manera inmediata para:',
                 'alternativas': ['Un nuevo periodo en el mismo cargo',
                                  'Cargos regionales',
                                  'Cargos municipales',
                                  'Ningún cargo público',
                                  'Ministerios'],
                 'correcta': 'A'},
                {'pregunta': 'El Congreso peruano actual tiene cámara única, '
                             'es decir, es de tipo:',
                 'alternativas': ['Mixto',
                                  'Regional',
                                  'Tricameral',
                                  'Bicameral',
                                  'Unicameral'],
                 'correcta': 'E'},
                {'pregunta': 'La única Constitución peruana que reconoció un '
                             'parlamento tricameral fue la de:',
                 'alternativas': ['1826', '1860', '1979', '1839', '1920'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las ventajas del sistema unicameral está '
                             'la celeridad en la aprobación de:',
                 'alternativas': ['Nombramientos',
                                  'Tratados exclusivamente',
                                  'Normas legales',
                                  'Presupuestos exclusivamente',
                                  'Impuestos exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las desventajas del sistema unicameral '
                             'está la fácil sumisión del Congreso al:',
                 'alternativas': ['Tribunal Constitucional',
                                  'Poder Judicial',
                                  'Ministerio Público',
                                  'Poder Ejecutivo',
                                  'Jurado Nacional de Elecciones'],
                 'correcta': 'D'},
                {'pregunta': 'La máxima asamblea deliberativa del Congreso, '
                             'integrada por todos los congresistas, se '
                             'llama:',
                 'alternativas': ['El Pleno',
                                  'Junta de Portavoces',
                                  'Comisión Permanente',
                                  'Consejo Directivo',
                                  'Mesa Directiva'],
                 'correcta': 'A'},
                {'pregunta': 'El órgano que tiene a cargo la dirección '
                             'administrativa del Congreso se llama:',
                 'alternativas': ['La Comisión Permanente',
                                  'El Pleno',
                                  'La Mesa Directiva',
                                  'Los Grupos Parlamentarios',
                                  'La Junta de Portavoces'],
                 'correcta': 'C'},
                {'pregunta': 'La Mesa Directiva está compuesta por el '
                             'Presidente y un número de Vicepresidentes '
                             'igual a:',
                 'alternativas': ['Cinco', 'Dos', 'Tres', 'Cuatro', 'Uno'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano encargado del estudio y dictamen de '
                             'asuntos ordinarios se llama:',
                 'alternativas': ['Junta de Portavoces',
                                  'Comisiones Ordinarias',
                                  'Consejo Directivo',
                                  'Comisión Permanente',
                                  'Ligas Parlamentarias'],
                 'correcta': 'B'},
                {'pregunta': 'La Comisión Permanente no puede exceder de un '
                             'porcentaje del total de congresistas igual a:',
                 'alternativas': ['10%', '25%', '30%', '15%', '50%'],
                 'correcta': 'B'},
                {'pregunta': 'Los conjuntos de congresistas que comparten '
                             'ideas o intereses afines se llaman:',
                 'alternativas': ['Comisiones Ordinarias',
                                  'Mesa Directiva',
                                  'Ligas Parlamentarias',
                                  'Grupos Parlamentarios',
                                  'Consejo Directivo'],
                 'correcta': 'D'},
                {'pregunta': 'Además de la función legislativa, el Congreso '
                             'tiene función fiscalizadora y:',
                 'alternativas': ['Notarial',
                                  'Ejecutiva',
                                  'Judicial',
                                  'Representativa',
                                  'Electoral'],
                 'correcta': 'D'},
                {'pregunta': 'Mediante la función fiscalizadora, el Congreso '
                             'puede iniciar investigaciones sobre asuntos de '
                             'interés:',
                 'alternativas': ['Privado exclusivo',
                                  'Militar exclusivo',
                                  'Religioso',
                                  'Comercial exclusivo',
                                  'Público'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las atribuciones del Congreso en la '
                             'formación de la orientación política general '
                             'está aprobar tratados internacionales y '
                             'declarar:',
                 'alternativas': ['Impuestos',
                                  'Elecciones',
                                  'La guerra y la paz',
                                  'El presupuesto exclusivo',
                                  'Feriados nacionales'],
                 'correcta': 'C'},
                {'pregunta': 'En la gestión financiera, el Congreso aprueba '
                             'el Presupuesto de la República y:',
                 'alternativas': ['Solo las tarifas públicas',
                                  'Solo el tipo de cambio',
                                  'Solo los impuestos municipales',
                                  'Solo el gasto militar',
                                  'La Cuenta General'],
                 'correcta': 'E'},
                {'pregunta': 'El Congreso designa, entre otros altos '
                             'funcionarios, a los magistrados del Tribunal '
                             'Constitucional y al:',
                 'alternativas': ['Presidente de la República',
                                  'Alcalde de Lima',
                                  'Defensor del Pueblo',
                                  'Fiscal de la Nación exclusivo',
                                  'Presidente del Poder Judicial exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'La función de congresista es de tiempo '
                             'completo; le está prohibido ejercer otra '
                             'profesión durante:',
                 'alternativas': ['Los fines de semana',
                                  'Las horas de funcionamiento del Congreso',
                                  'Los feriados',
                                  'Ningún momento, puede ejercer libremente',
                                  'Las vacaciones'],
                 'correcta': 'B'},
                {'pregunta': 'El mandato del congresista es incompatible con '
                             'el ejercicio de cualquier otra función '
                             'pública, excepto la de:',
                 'alternativas': ['Ministro de Estado',
                                  'Gobernador Regional',
                                  'Juez',
                                  'Fiscal',
                                  'Alcalde'],
                 'correcta': 'A'},
                {'pregunta': 'La Cuenta General de la República, como '
                             'documento oficial, es aprobada por: (II CEPRU '
                             '2025-I)',
                 'alternativas': ['La Comisión de Presupuesto',
                                  'La Contraloría General de la República',
                                  'El Congreso de la República',
                                  'El Consejo de Ministros',
                                  'El Ministerio de Economía y Finanzas'],
                 'correcta': 'C'},
                {'pregunta': 'Es una atribución del Congreso: (III CEPRU '
                             '2025-I)',
                 'alternativas': ['Autorizar los empréstitos',
                                  'Administrar la hacienda pública',
                                  'Cumplir y hacer cumplir la Constitución, '
                                  'los tratados, leyes y demás disposiciones '
                                  'legales',
                                  'Emitir los Decretos Legislativos y de '
                                  'Urgencia',
                                  'Dirigir la política general del Gobierno'],
                 'correcta': 'A'},
                {'pregunta': 'Es un requisito para ser congresista: (II '
                             'CEPRU 2022-II)',
                 'alternativas': ['Tener estudios universitarios',
                                  'Tener primaria completa',
                                  'Ser varón',
                                  'Terminar el 5to de secundaria',
                                  'Ser peruano de nacimiento'],
                 'correcta': 'E'},
                {'pregunta': 'Además de la función legislativa, el '
                             'Parlamento tiene una función de control del '
                             'gobierno, también llamada función de:',
                 'alternativas': ['Ejecución',
                                  'Fiscalización',
                                  'Conciliación',
                                  'Administración',
                                  'Representación exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La función de control o fiscalización del '
                             'Congreso presenta dos modalidades: el control '
                             'político y el control:',
                 'alternativas': ['Territorial',
                                  'Electoral',
                                  'Social',
                                  'Jurídico o de legalidad',
                                  'Económico'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los mecanismos del control político del '
                             'Congreso están las preguntas, las comisiones '
                             'investigadoras y:',
                 'alternativas': ['La interpelación',
                                  'La consulta previa',
                                  'El referéndum',
                                  'El plebiscito',
                                  'La revocatoria'],
                 'correcta': 'A'},
                {'pregunta': 'El control jurídico o de legalidad del '
                             'Congreso busca determinar si un funcionario '
                             'público ha incurrido en:',
                 'alternativas': ['Infracción de la ley o de la Constitución',
                                  'Ausencias injustificadas',
                                  'Retrasos en sus funciones',
                                  'Errores de redacción',
                                  'Faltas administrativas menores'],
                 'correcta': 'A'}],
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
                                'número legal de congresistas.']},
                     {'titulo': 'FUNCIÓN DE CONTROL O FISCALIZACIÓN',
                      'items': ['El Parlamento tiene, además de la '
                                'legislativa, una función de control o '
                                'fiscalización del gobierno.',
                                'Esta función presenta dos modalidades: el '
                                'control político y el control jurídico o de '
                                'legalidad.',
                                'En la responsabilidad política, el '
                                'Parlamento ejerce la potestad de juzgar la '
                                'actividad de quienes ejercen el gobierno.',
                                'Los mecanismos del control político '
                                'incluyen las preguntas, la interpelación, '
                                'las comisiones investigadoras y la '
                                'invitación a informar.',
                                'El control jurídico o de legalidad busca '
                                'determinar si un funcionario público ha '
                                'infringido la ley o la Constitución.']},
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
                                'funcionamiento.']}],
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
                 'alternativas': ['Jefe militar exclusivamente',
                                  'Jefe del Poder Judicial',
                                  'Jefe del Congreso',
                                  'Jefe de Gobierno',
                                  'Jefe religioso'],
                 'correcta': 'D'},
                {'pregunta': 'El Poder Ejecutivo es el órgano encargado de:',
                 'alternativas': ['Organizar elecciones',
                                  'Fiscalizar al Congreso',
                                  'La administración del Estado y ejecución '
                                  'de las leyes',
                                  'Administrar justicia',
                                  'Dictar leyes exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Integran el Poder Ejecutivo el Presidente y:',
                 'alternativas': ['El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'El Consejo de Ministros',
                                  'La Defensoría del Pueblo',
                                  'El Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'En el sistema presidencial, los tres poderes '
                             'del Estado son:',
                 'alternativas': ['Subordinados al Ejecutivo',
                                  'Elegidos por el Congreso',
                                  'Dependientes entre sí',
                                  'Fusionados en uno solo',
                                  'Autónomos e independientes'],
                 'correcta': 'E'},
                {'pregunta': 'Para ser presidente del Perú se requiere ser '
                             'peruano:',
                 'alternativas': ['Residente',
                                  'Mayor de 50 años exclusivamente',
                                  'De nacimiento',
                                  'Naturalizado',
                                  'Con doble nacionalidad'],
                 'correcta': 'C'},
                {'pregunta': 'La edad mínima para postular a la presidencia '
                             'es de:',
                 'alternativas': ['25 años',
                                  '30 años',
                                  '40 años',
                                  '45 años',
                                  '35 años'],
                 'correcta': 'E'},
                {'pregunta': 'El presidente de la República se elige por un '
                             'mandato de:',
                 'alternativas': ['5 años',
                                  '6 años',
                                  '3 años',
                                  '4 años',
                                  '7 años'],
                 'correcta': 'A'},
                {'pregunta': 'La reelección presidencial inmediata en el '
                             'Perú está:',
                 'alternativas': ['Permitida sin restricciones',
                                  'Obligatoria',
                                  'No permitida',
                                  'Permitida solo una vez',
                                  'Sujeta a referéndum'],
                 'correcta': 'C'},
                {'pregunta': 'Para ganar la presidencia en primera vuelta se '
                             'requiere:',
                 'alternativas': ['La mitad exacta de votos válidos',
                                  'Un tercio de los votos',
                                  'Mayoría absoluta',
                                  'Mayoría relativa',
                                  'Solo más votos que el segundo'],
                 'correcta': 'C'},
                {'pregunta': 'Si ningún candidato obtiene mayoría absoluta, '
                             'se realiza:',
                 'alternativas': ['Un sorteo',
                                  'Una nueva convocatoria general',
                                  'Una segunda elección entre los dos más '
                                  'votados',
                                  'Una decisión del Congreso',
                                  'Una tercera vuelta'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 116, el Presidente jura y '
                             'asume el cargo ante:',
                 'alternativas': ['El Jurado Nacional de Elecciones',
                                  'El pueblo directamente',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'El Poder Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente asume el cargo el:',
                 'alternativas': ['28 de julio',
                                  '9 de diciembre',
                                  '15 de agosto',
                                  '1 de enero',
                                  '1 de mayo'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las atribuciones del Presidente figura '
                             'representar al Estado:',
                 'alternativas': ['Dentro y fuera de la República',
                                  'Solo ante el Congreso',
                                  'Solo en tratados comerciales',
                                  'Solo dentro del país',
                                  'Solo en organismos internacionales'],
                 'correcta': 'A'},
                {'pregunta': 'El Presidente puede convocar al Congreso a '
                             'legislatura:',
                 'alternativas': ['Extraordinaria',
                                  'Permanente sin descanso',
                                  'Solo virtual',
                                  'Ninguna, esa función es del Congreso',
                                  'Solo ordinaria'],
                 'correcta': 'A'},
                {'pregunta': 'El Presidente dirige mensajes obligatorios al '
                             'Congreso al instalarse la legislatura:',
                 'alternativas': ['Solo el último año de gobierno',
                                  'Cada seis meses',
                                  'Nunca, esa función no le corresponde',
                                  'Extraordinaria únicamente',
                                  'Ordinaria anual'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente reglamenta las leyes mediante:',
                 'alternativas': ['Leyes orgánicas',
                                  'Resoluciones legislativas',
                                  'Sentencias judiciales',
                                  'Decretos y resoluciones',
                                  'Ordenanzas municipales'],
                 'correcta': 'D'},
                {'pregunta': 'Al reglamentar las leyes, el Presidente no '
                             'puede:',
                 'alternativas': ['Publicarlas',
                                  'Ejecutarlas',
                                  'Emitir decretos',
                                  'Cumplirlas',
                                  'Transgredirlas ni desnaturalizarlas'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente dirige la política exterior y '
                             'puede:',
                 'alternativas': ['Modificar la Constitución solo',
                                  'Celebrar y ratificar tratados',
                                  'Elegir a los congresistas',
                                  'Disolver el Poder Judicial',
                                  'Declarar la guerra sin el Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'Junto con el Presidente se eligen, con los '
                             'mismos requisitos:',
                 'alternativas': ['Los gobernadores regionales',
                                  'Los alcaldes',
                                  'Los congresistas',
                                  'Los ministros',
                                  'Dos vicepresidentes'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente debe velar por el orden interno '
                             'y:',
                 'alternativas': ['El sistema educativo',
                                  'La política monetaria',
                                  'La reforma agraria',
                                  'La seguridad exterior de la República',
                                  'El comercio exterior'],
                 'correcta': 'D'},
                {'pregunta': 'La Presidencia de la República vaca por '
                             'muerte, incapacidad moral o física, aceptación '
                             'de renuncia o:',
                 'alternativas': ['Destitución',
                                  'Vacaciones prolongadas',
                                  'Viaje autorizado',
                                  'Enfermedad leve',
                                  'Ausencia de un día'],
                 'correcta': 'A'},
                {'pregunta': 'La Presidencia también vaca si el Presidente '
                             'sale del territorio nacional sin permiso de:',
                 'alternativas': ['La Contraloría',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'El Consejo de Ministros exclusivo',
                                  'El Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'El ejercicio de la Presidencia se suspende por '
                             'incapacidad temporal o por estar sometido a '
                             'proceso:',
                 'alternativas': ['Administrativo',
                                  'Fiscal exclusivo',
                                  'Electoral exclusivo',
                                  'Judicial',
                                  'Disciplinario menor'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 117, el Presidente solo '
                             'puede ser acusado durante su periodo por '
                             'traición a la patria o por impedir:',
                 'alternativas': ['El comercio exterior',
                                  'El turismo',
                                  'Reformas económicas',
                                  'Las elecciones',
                                  'La educación pública'],
                 'correcta': 'D'},
                {'pregunta': 'Por impedimento del Presidente, asume sus '
                             'funciones en primer lugar:',
                 'alternativas': ['El Presidente del Poder Judicial',
                                  'El Segundo Vicepresidente',
                                  'El Presidente del Congreso',
                                  'El Premier',
                                  'El Primer Vicepresidente'],
                 'correcta': 'E'},
                {'pregunta': 'El Consejo de Ministros es el organismo del '
                             'Poder Ejecutivo constituido por la reunión de:',
                 'alternativas': ['Los gobernadores regionales',
                                  'Los congresistas',
                                  'Los jueces supremos',
                                  'Los ministros',
                                  'Los alcaldes'],
                 'correcta': 'D'},
                {'pregunta': 'Son nulos los actos del Presidente que carecen '
                             'de:',
                 'alternativas': ['Firma notarial',
                                  'Publicación inmediata',
                                  'Aprobación popular',
                                  'Refrendación ministerial',
                                  'Sello presidencial'],
                 'correcta': 'D'},
                {'pregunta': 'El jefe del Consejo de Ministros, quien puede '
                             'tener cartera o no, se llama:',
                 'alternativas': ['Vicepresidente',
                                  'Portavoz',
                                  'Canciller',
                                  'Premier o Presidente del Consejo de '
                                  'Ministros',
                                  'Secretario General'],
                 'correcta': 'D'},
                {'pregunta': 'Para ser ministro se requiere ser peruano de '
                             'nacimiento, ciudadano en ejercicio, y tener '
                             'como mínimo:',
                 'alternativas': ['21 años',
                                  '35 años',
                                  '30 años',
                                  '18 años',
                                  '25 años'],
                 'correcta': 'E'},
                {'pregunta': 'Actualmente el Perú cuenta con un número de '
                             'ministerios igual a:',
                 'alternativas': ['18', '15', '16', '12', '20'],
                 'correcta': 'A'},
                {'pregunta': 'Los ministros son individualmente responsables '
                             'por sus propios actos, y solidariamente '
                             'responsables por actos que:',
                 'alternativas': ['Delegan a terceros',
                                  'Refrendan en conjunto',
                                  'Nunca comparten',
                                  'Ocultan al Congreso',
                                  'Publican en el diario oficial'],
                 'correcta': 'B'},
                {'pregunta': 'La interpelación es la facultad de los '
                             'congresistas de requerir a los ministros que:',
                 'alternativas': ['Paguen una multa',
                                  'Sean destituidos',
                                  'Informen, aclaren o expliquen un asunto',
                                  'Renuncien inmediatamente',
                                  'Se retiren del país'],
                 'correcta': 'C'},
                {'pregunta': 'La interpelación debe presentarse por escrito '
                             'por no menos de un porcentaje de congresistas '
                             'igual a:',
                 'alternativas': ['5%', '15%', '25%', '30%', '10%'],
                 'correcta': 'B'},
                {'pregunta': 'El resultado de una interpelación puede ser un '
                             'voto de confianza o un voto de:',
                 'alternativas': ['Reconocimiento',
                                  'Aplauso',
                                  'Felicitación',
                                  'Abstención exclusiva',
                                  'Censura'],
                 'correcta': 'E'},
                {'pregunta': 'Toda moción de censura contra el Consejo de '
                             'Ministros debe presentarse por no menos de un '
                             'porcentaje igual a:',
                 'alternativas': ['10%', '5%', '50%', '25%', '15%'],
                 'correcta': 'D'},
                {'pregunta': 'La aprobación de una moción de censura '
                             'requiere el voto de:',
                 'alternativas': ['Un tercio del Congreso',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'Unanimidad',
                                  'Dos tercios del Congreso',
                                  'La cuarta parte'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente puede disolver el Congreso si '
                             'este ha censurado o negado su confianza a un '
                             'número de Consejos de Ministros igual a:',
                 'alternativas': ['Cuatro', 'Tres', 'Uno', 'Dos', 'Cinco'],
                 'correcta': 'D'},
                {'pregunta': 'Tras la disolución del Congreso, las nuevas '
                             'elecciones deben realizarse dentro de:',
                 'alternativas': ['Un año',
                                  'Dos meses',
                                  'Cuatro meses',
                                  'Seis meses',
                                  'Tres meses'],
                 'correcta': 'C'},
                {'pregunta': 'El Congreso no puede ser disuelto en el último '
                             'año de su mandato ni cuando se está en:',
                 'alternativas': ['Receso ordinario',
                                  'Elecciones municipales',
                                  'Estado de sitio',
                                  'Estado de emergencia',
                                  'Vacaciones parlamentarias'],
                 'correcta': 'C'},
                {'pregunta': 'Al disolverse el Congreso, se mantiene en '
                             'funciones:',
                 'alternativas': ['El Pleno completo',
                                  'La Mesa Directiva exclusiva',
                                  'Ningún órgano',
                                  'El Consejo de Ministros exclusivo',
                                  'La Comisión Permanente'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 137 de la Constitución establece '
                             'dos regímenes de excepción: estado de sitio y '
                             'estado de:',
                 'alternativas': ['Conmoción',
                                  'Guerra',
                                  'Alerta máxima',
                                  'Emergencia',
                                  'Alarma'],
                 'correcta': 'D'},
                {'pregunta': 'Los regímenes de excepción son declarados por '
                             'el Presidente con acuerdo de:',
                 'alternativas': ['El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'La Contraloría',
                                  'El Congreso exclusivo',
                                  'El Consejo de Ministros'],
                 'correcta': 'E'},
                {'pregunta': 'Durante los regímenes de excepción, no se '
                             'suspenden el hábeas corpus y:',
                 'alternativas': ['El amparo',
                                  'El hábeas data',
                                  'La acción de inconstitucionalidad',
                                  'La acción popular',
                                  'El proceso de cumplimiento'],
                 'correcta': 'A'},
                {'pregunta': 'El estado de emergencia se declara por '
                             'perturbación de la paz, catástrofe o graves '
                             'circunstancias, y dura hasta:',
                 'alternativas': ['30 días',
                                  '45 días',
                                  '15 días',
                                  '90 días',
                                  '60 días'],
                 'correcta': 'E'},
                {'pregunta': 'Durante el estado de emergencia, asumen el '
                             'control interno del país:',
                 'alternativas': ['El Poder Judicial',
                                  'La Policía Nacional exclusivamente',
                                  'Los municipios',
                                  'Las Fuerzas Armadas',
                                  'Los gobiernos regionales'],
                 'correcta': 'D'},
                {'pregunta': 'El estado de sitio se declara en caso de '
                             'invasión, guerra exterior o:',
                 'alternativas': ['Crisis económica',
                                  'Escasez de alimentos',
                                  'Elecciones fraudulentas',
                                  'Guerra civil',
                                  'Corrupción generalizada'],
                 'correcta': 'D'},
                {'pregunta': 'El plazo del estado de sitio no debe exceder '
                             'de:',
                 'alternativas': ['45 días',
                                  '90 días',
                                  '15 días',
                                  '30 días',
                                  '60 días'],
                 'correcta': 'A'},
                {'pregunta': 'El encargado de elegir al presidente del '
                             'Consejo de Ministros, así como de removerlo, '
                             'es el presidente de: (IV CEPRU 2025-I)',
                 'alternativas': ['La República',
                                  'El Tribunal Constitucional',
                                  'El Consejo de Ministros',
                                  'La Corte Suprema de Justicia',
                                  'El Congreso de la República'],
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
                 'alternativas': ['Dictar leyes',
                                  'Administrar justicia',
                                  'Ejecutar el presupuesto',
                                  'Organizar elecciones',
                                  'Representar al Estado en el exterior'],
                 'correcta': 'B'},
                {'pregunta': 'El Poder Judicial es autónomo en lo político, '
                             'administrativo, económico y:',
                 'alternativas': ['Disciplinario',
                                  'Militar',
                                  'Educativo',
                                  'Religioso',
                                  'Comercial'],
                 'correcta': 'A'},
                {'pregunta': 'En el ejercicio jurisdiccional, el Poder '
                             'Judicial es:',
                 'alternativas': ['Independiente',
                                  'Controlado por el Tribunal Constitucional',
                                  'Dirigido por el Presidente',
                                  'Subordinado al Congreso',
                                  'Dependiente del Ejecutivo'],
                 'correcta': 'A'},
                {'pregunta': 'La potestad de administrar justicia emana de:',
                 'alternativas': ['Los jueces exclusivamente',
                                  'Organismos internacionales',
                                  'El pueblo',
                                  'El Presidente',
                                  'El Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'El máximo órgano jurisdiccional del Poder '
                             'Judicial es:',
                 'alternativas': ['Las Cortes Superiores',
                                  'Los Juzgados Mixtos',
                                  'Los Juzgados de Paz',
                                  'El Consejo Ejecutivo',
                                  'La Corte Suprema de Justicia'],
                 'correcta': 'E'},
                {'pregunta': 'Los Juzgados de Paz Letrados corresponden al '
                             'nivel:',
                 'alternativas': ['Internacional',
                                  'Constitucional',
                                  'Básico',
                                  'Superior',
                                  'Supremo'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano de gestión encargado de la '
                             'administración del Poder Judicial es:',
                 'alternativas': ['La Defensoría del Pueblo',
                                  'El Ministerio Público',
                                  'El Jurado Nacional de Elecciones',
                                  'El Consejo Ejecutivo del Poder Judicial',
                                  'La Sala Penal'],
                 'correcta': 'D'},
                {'pregunta': 'No existe ni puede establecerse jurisdicción '
                             'independiente, salvo:',
                 'alternativas': ['La militar y la arbitral',
                                  'La municipal',
                                  'La internacional',
                                  'La religiosa',
                                  'La comercial'],
                 'correcta': 'A'},
                {'pregunta': 'El principio de unidad y exclusividad de la '
                             'función jurisdiccional implica que:',
                 'alternativas': ['Existen múltiples jurisdicciones '
                                  'paralelas',
                                  'Cualquier autoridad puede juzgar',
                                  'Los alcaldes pueden juzgar delitos',
                                  'No hay proceso judicial por comisión o '
                                  'delegación',
                                  'El Congreso puede sentenciar'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de independencia jurisdiccional '
                             'impide que una autoridad:',
                 'alternativas': ['Realice investigaciones periodísticas',
                                  'Solicite información pública',
                                  'Participe en audiencias públicas',
                                  'Se avoque a causas pendientes ante el '
                                  'órgano jurisdiccional',
                                  'Presente denuncias'],
                 'correcta': 'D'},
                {'pregunta': 'El debido proceso impide que una persona sea '
                             'juzgada por:',
                 'alternativas': ['La Corte Suprema',
                                  'Comisiones especiales creadas al efecto',
                                  'Un tribunal constitucional',
                                  'Un juzgado de paz',
                                  'Un juez competente'],
                 'correcta': 'B'},
                {'pregunta': 'La regla general en los procesos judiciales es '
                             'la:',
                 'alternativas': ['Publicidad, salvo disposición contraria '
                                  'de la ley',
                                  'Reserva absoluta',
                                  'Exclusividad militar',
                                  'Confidencialidad total',
                                  'Prohibición de prensa'],
                 'correcta': 'A'},
                {'pregunta': 'Los procesos por responsabilidad de '
                             'funcionarios públicos son:',
                 'alternativas': ['Siempre públicos',
                                  'Resueltos por decreto',
                                  'Siempre reservados',
                                  'Confidenciales por defecto',
                                  'Decididos por el Congreso'],
                 'correcta': 'A'},
                {'pregunta': 'La motivación escrita de las resoluciones '
                             'judiciales es obligatoria en:',
                 'alternativas': ['Solo casos penales',
                                  'Solo la Corte Suprema',
                                  'Todas las instancias',
                                  'Solo la primera instancia',
                                  'Ningún nivel en particular'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo de la Constitución que precisa la '
                             'extensión jurisdiccional en comunidades es el:',
                 'alternativas': ['Artículo 51',
                                  'Artículo 149',
                                  'Artículo 24',
                                  'Artículo 22',
                                  'Artículo 91'],
                 'correcta': 'B'},
                {'pregunta': 'Ninguna autoridad puede dejar sin efecto '
                             'resoluciones que han pasado en autoridad de:',
                 'alternativas': ['Consulta previa',
                                  'Resolución administrativa',
                                  'Reglamento interno',
                                  'Norma transitoria',
                                  'Cosa juzgada'],
                 'correcta': 'E'},
                {'pregunta': 'El derecho de gracia y la facultad de '
                             'investigación del Congreso no deben:',
                 'alternativas': ['Ser públicas',
                                  'Ser reguladas por ley',
                                  'Ejercerse nunca',
                                  'Interferir en el procedimiento '
                                  'jurisdiccional',
                                  'Aplicarse a funcionarios'],
                 'correcta': 'D'},
                {'pregunta': 'La Sala Plena de la Corte Suprema es un órgano '
                             'de:',
                 'alternativas': ['Jurisdicción exclusiva',
                                  'Relaciones internacionales',
                                  'Control tributario',
                                  'Fiscalización externa',
                                  'Gestión'],
                 'correcta': 'E'},
                {'pregunta': 'Los Juzgados de Paz, en la estructura del '
                             'Poder Judicial, están en el nivel:',
                 'alternativas': ['Más básico',
                                  'Internacional',
                                  'Militar',
                                  'Constitucional',
                                  'Supremo'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley Orgánica del Poder Judicial regula, '
                             'junto con la Constitución, el ejercicio de:',
                 'alternativas': ['Solo la función administrativa',
                                  'Solo el presupuesto',
                                  'Solo las relaciones exteriores',
                                  'Las funciones jurisdiccionales y de '
                                  'gobierno',
                                  'Solo la disciplina interna'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que permite que una resolución '
                             'sea revisada por un órgano superior se llama:',
                 'alternativas': ['Pluralidad de instancia',
                                  'Cosa juzgada',
                                  'Publicidad',
                                  'Unidad jurisdiccional',
                                  'Debido proceso'],
                 'correcta': 'A'},
                {'pregunta': 'El Estado debe indemnizar por los errores '
                             'judiciales en procesos penales y por:',
                 'alternativas': ['Demoras administrativas',
                                  'Multas excesivas',
                                  'Costas procesales',
                                  'Apelaciones rechazadas',
                                  'Detenciones arbitrarias'],
                 'correcta': 'E'},
                {'pregunta': 'En caso de vacío o deficiencia de la ley, el '
                             'juez debe aplicar los principios generales del '
                             'derecho y:',
                 'alternativas': ['Solo jurisprudencia extranjera',
                                  'Solo la doctrina',
                                  'Su criterio personal exclusivo',
                                  'El derecho consuetudinario',
                                  'Ninguna norma adicional'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que impide aplicar por semejanza '
                             'la ley penal se llama principio de:',
                 'alternativas': ['Retroactividad',
                                  'Legalidad exclusiva',
                                  'Tipicidad',
                                  'Proporcionalidad',
                                  'Inaplicabilidad por analogía'],
                 'correcta': 'E'},
                {'pregunta': 'Un principio fundamental de la administración '
                             'de justicia es que nadie puede ser penado sin:',
                 'alternativas': ['Pago de fianza',
                                  'Confesión previa',
                                  'Testigos presenciales',
                                  'Proceso judicial previo',
                                  'Denuncia pública'],
                 'correcta': 'D'},
                {'pregunta': 'En caso de duda o conflicto entre leyes '
                             'penales, se debe aplicar la ley:',
                 'alternativas': ['Más antigua',
                                  'Más severa',
                                  'Más reciente exclusivamente',
                                  'Extranjera',
                                  'Más favorable al procesado'],
                 'correcta': 'E'},
                {'pregunta': 'Un principio de la administración de justicia '
                             'establece que nadie puede ser condenado:',
                 'alternativas': ['Sin apelación',
                                  'Sin fianza',
                                  'Sin testigos',
                                  'Sin abogado',
                                  'En ausencia'],
                 'correcta': 'E'},
                {'pregunta': 'Está prohibido revivir procesos fenecidos con '
                             'resolución ejecutoriada; la amnistía y el '
                             'indulto producen efectos de:',
                 'alternativas': ['Suspensión temporal',
                                  'Prescripción inmediata',
                                  'Nulidad absoluta',
                                  'Revisión automática',
                                  'Cosa juzgada'],
                 'correcta': 'E'},
                {'pregunta': 'El derecho de defensa no puede ser negado en '
                             'ningún:',
                 'alternativas': ['Tribunal superior exclusivo',
                                  'Recurso de apelación exclusivo',
                                  'Estado del proceso',
                                  'Juicio oral exclusivo',
                                  'Proceso civil exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano jurisdiccional jerárquico que ejerce '
                             'sus funciones en un distrito judicial es: (IV '
                             'CEPRU 2025-I)',
                 'alternativas': ['Los Juzgados de Paz Letrados',
                                  'La Corte Suprema',
                                  'Los Juzgados Mixtos Provinciales',
                                  'Los Juzgados de Paz',
                                  'Las Cortes Superiores'],
                 'correcta': 'E'}],
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
                           'dejado el cargo con {un año} de anticipación.',
                           'Según el artículo {201} de la Constitución, el '
                           'Tribunal Constitucional se compone de {siete} '
                           'miembros elegidos por cinco años.',
                           'No hay {reelección} inmediata de los miembros '
                           'del Tribunal Constitucional.']},
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
                 'alternativas': ['Empresarial',
                                  'Eclesiástico',
                                  'Internacional',
                                  'Militar',
                                  'Local'],
                 'correcta': 'E'},
                {'pregunta': 'El número de organismos constitucionales '
                             'autónomos en el Perú es:',
                 'alternativas': ['Quince',
                                  'Veinte',
                                  'Tres',
                                  'Diez',
                                  'Cinco'],
                 'correcta': 'D'},
                {'pregunta': 'La autonomía de los OCA implica que sus '
                             'directivos:',
                 'alternativas': ['Dependen del Presidente',
                                  'Son elegidos por sorteo',
                                  'Toman decisiones sin someterse a órdenes '
                                  'superiores',
                                  'Actúan solo por consulta popular',
                                  'Dependen del Congreso exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'El Tribunal Constitucional es el órgano de '
                             'control de:',
                 'alternativas': ['El comercio exterior',
                                  'La banca',
                                  'El presupuesto',
                                  'Las elecciones únicamente',
                                  'La Constitución'],
                 'correcta': 'E'},
                {'pregunta': 'El Tribunal Constitucional está regulado en el '
                             'artículo:',
                 'alternativas': ['91', '201', '24', '102', '158'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional se compone de:',
                 'alternativas': ['Doce miembros',
                                  'Cinco miembros',
                                  'Nueve miembros',
                                  'Siete miembros',
                                  'Tres miembros'],
                 'correcta': 'D'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Cuatro años',
                                  'Vitalicio',
                                  'Tres años',
                                  'Diez años',
                                  'Cinco años'],
                 'correcta': 'E'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por el Congreso con:',
                 'alternativas': ['Mayoría absoluta',
                                  'Mayoría simple',
                                  'El voto de los dos tercios del número '
                                  'legal de miembros',
                                  'Unanimidad',
                                  'Consulta popular directa'],
                 'correcta': 'C'},
                {'pregunta': 'No pueden ser magistrados del Tribunal '
                             'Constitucional los jueces o fiscales que no '
                             'dejaron el cargo con anticipación de:',
                 'alternativas': ['Un año',
                                  'Tres meses',
                                  'Dos años',
                                  'Seis meses',
                                  'Cinco años'],
                 'correcta': 'A'},
                {'pregunta': 'El Ministerio Público es el órgano encargado '
                             'de:',
                 'alternativas': ['Emitir moneda',
                                  'Legislar',
                                  'Dirigir el gobierno',
                                  'Perseguir el delito',
                                  'Administrar justicia directamente'],
                 'correcta': 'D'},
                {'pregunta': 'El Ministerio Público es presidido por:',
                 'alternativas': ['El presidente del Poder Judicial',
                                  'El presidente del Congreso',
                                  'El Defensor del Pueblo',
                                  'El Presidente de la República',
                                  'El Fiscal de la Nación'],
                 'correcta': 'E'},
                {'pregunta': 'El Fiscal de la Nación es elegido por:',
                 'alternativas': ['El Congreso',
                                  'La Junta de Fiscales Supremos',
                                  'El Poder Judicial',
                                  'El Presidente de la República',
                                  'Voto popular directo'],
                 'correcta': 'B'},
                {'pregunta': 'El cargo de Fiscal de la Nación dura:',
                 'alternativas': ['Vitalicio',
                                  'Dos años',
                                  'Cinco años',
                                  'Tres años',
                                  'Un año'],
                 'correcta': 'D'},
                {'pregunta': 'El cargo de Fiscal de la Nación puede '
                             'prorrogarse por reelección hasta por:',
                 'alternativas': ['Dos años más',
                                  'Un año más',
                                  'No es prorrogable',
                                  'Diez años más',
                                  'Cinco años más'],
                 'correcta': 'A'},
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
                 'alternativas': ['Los gobiernos regionales',
                                  'Los gobiernos locales',
                                  'El Ministerio Público',
                                  'Solo el Congreso',
                                  'Solo el Poder Judicial'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los organismos constitucionales '
                             'autónomos figura el organismo encargado de '
                             'emitir moneda, que es:',
                 'alternativas': ['La SBS',
                                  'El BID',
                                  'El MEF',
                                  'El Banco Central de Reserva',
                                  'La SUNAT'],
                 'correcta': 'D'},
                {'pregunta': 'El organismo encargado de la defensa de los '
                             'derechos constitucionales de la persona es:',
                 'alternativas': ['La Defensoría del Pueblo',
                                  'El JNE',
                                  'La ONPE',
                                  'La Contraloría',
                                  'El Tribunal Constitucional'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo encargado de organizar los '
                             'procesos electorales es:',
                 'alternativas': ['La ONPE',
                                  'La Defensoría del Pueblo',
                                  'El RENIEC',
                                  'El Ministerio Público',
                                  'El JNE'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo encargado del registro de '
                             'identificación y estado civil es:',
                 'alternativas': ['El RENIEC',
                                  'La SUNARP',
                                  'El JNE',
                                  'El INEI',
                                  'La ONPE'],
                 'correcta': 'A'},
                {'pregunta': 'La Junta Nacional de Justicia sustituyó al:',
                 'alternativas': ['Ministerio Público',
                                  'Tribunal Constitucional',
                                  'Consejo Nacional de la Magistratura',
                                  'Poder Judicial',
                                  'Jurado Nacional de Elecciones'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 150 de la Constitución, la '
                             'Junta Nacional de Justicia selecciona y nombra '
                             'a:',
                 'alternativas': ['Jueces y fiscales',
                                  'Solo gobernadores regionales',
                                  'Solo congresistas',
                                  'Solo ministros',
                                  'Solo alcaldes'],
                 'correcta': 'A'},
                {'pregunta': 'Para ser miembro de la Junta Nacional de '
                             'Justicia se requiere tener una edad entre:',
                 'alternativas': ['40 y 70 años',
                                  '35 y 80 años',
                                  '30 y 65 años',
                                  '25 y 60 años',
                                  '45 y 75 años'],
                 'correcta': 'E'},
                {'pregunta': 'La Junta Nacional de Justicia está conformada '
                             'por un número de miembros titulares igual a:',
                 'alternativas': ['Cinco', 'Tres', 'Nueve', 'Siete', 'Once'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de los miembros de la Junta '
                             'Nacional de Justicia es de:',
                 'alternativas': ['Tres años',
                                  'Seis años',
                                  'Siete años',
                                  'Cinco años',
                                  'Cuatro años'],
                 'correcta': 'D'},
                {'pregunta': 'La Defensoría del Pueblo tiene su origen '
                             'histórico en:',
                 'alternativas': ['Francia',
                                  'Suecia',
                                  'España',
                                  'Inglaterra',
                                  'Estados Unidos'],
                 'correcta': 'B'},
                {'pregunta': 'El Defensor del Pueblo es elegido y removido '
                             'por el Congreso con el voto de:',
                 'alternativas': ['Un tercio',
                                  'Los dos tercios de su número legal',
                                  'Unanimidad',
                                  'Mayoría simple',
                                  'La mitad más uno'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser elegido Defensor del Pueblo se '
                             'requiere tener una edad mínima de:',
                 'alternativas': ['30 años',
                                  '40 años',
                                  '35 años',
                                  '25 años',
                                  '45 años'],
                 'correcta': 'C'},
                {'pregunta': 'El cargo de Defensor del Pueblo dura:',
                 'alternativas': ['Cinco años',
                                  'Cuatro años',
                                  'Seis años',
                                  'Siete años',
                                  'Tres años'],
                 'correcta': 'A'},
                {'pregunta': 'La finalidad principal del Banco Central de '
                             'Reserva es:',
                 'alternativas': ['Recaudar impuestos',
                                  'Supervisar el Poder Judicial',
                                  'Administrar el presupuesto público',
                                  'Fiscalizar elecciones',
                                  'Preservar la estabilidad monetaria'],
                 'correcta': 'E'},
                {'pregunta': 'El BCR está prohibido de conceder '
                             'financiamiento al erario, salvo la compra en '
                             'el mercado secundario de valores emitidos por:',
                 'alternativas': ['Municipalidades',
                                  'Bancos privados',
                                  'El Tesoro Público',
                                  'Gobiernos regionales',
                                  'Empresas mineras'],
                 'correcta': 'C'},
                {'pregunta': 'La SBS (Superintendencia de Banca, Seguros y '
                             'AFP) supervisa a las empresas vinculadas al '
                             'ámbito:',
                 'alternativas': ['Educativo',
                                  'Turístico',
                                  'Financiero y de seguros',
                                  'Minero',
                                  'Agrícola'],
                 'correcta': 'C'},
                {'pregunta': 'El Superintendente de la SBS es designado por '
                             'el Poder Ejecutivo y ratificado por:',
                 'alternativas': ['El BCR',
                                  'La Contraloría',
                                  'El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'El Congreso'],
                 'correcta': 'E'},
                {'pregunta': 'La Contraloría General de la República es el '
                             'órgano superior del Sistema Nacional de:',
                 'alternativas': ['Salud',
                                  'Educación',
                                  'Seguridad',
                                  'Control',
                                  'Justicia'],
                 'correcta': 'D'},
                {'pregunta': 'El Contralor General es designado por el '
                             'Congreso, a propuesta del Poder Ejecutivo, por '
                             'un periodo de:',
                 'alternativas': ['Seis años',
                                  'Cinco años',
                                  'Tres años',
                                  'Siete años',
                                  'Cuatro años'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema electoral peruano es de naturaleza:',
                 'alternativas': ['Tetracéfalo',
                                  'Bicéfalo',
                                  'Tricéfalo',
                                  'Unicéfalo',
                                  'Pentacéfalo'],
                 'correcta': 'C'},
                {'pregunta': 'Los integrantes del Pleno del Jurado Nacional '
                             'de Elecciones son elegidos por un periodo de:',
                 'alternativas': ['Dos años',
                                  'Cuatro años',
                                  'Seis años',
                                  'Cinco años',
                                  'Tres años'],
                 'correcta': 'B'},
                {'pregunta': 'El JNE fiscaliza la legalidad del ejercicio '
                             'del sufragio y de la realización de:',
                 'alternativas': ['Solo la seguridad ciudadana',
                                  'Solo el presupuesto',
                                  'Solo la educación cívica',
                                  'Los procesos electorales',
                                  'Solo el registro civil'],
                 'correcta': 'D'},
                {'pregunta': 'El Pleno del Jurado Nacional de Elecciones '
                             'está compuesto por un número de miembros igual '
                             'a:',
                 'alternativas': ['Siete',
                                  'Cinco',
                                  'Nueve',
                                  'Tres',
                                  'Cuatro'],
                 'correcta': 'B'},
                {'pregunta': 'El Jefe de la Oficina Nacional de Procesos '
                             'Electorales (ONPE) es nombrado por:',
                 'alternativas': ['La Contraloría',
                                  'La Junta Nacional de Justicia',
                                  'El JNE',
                                  'El Presidente de la República',
                                  'El Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'A la ONPE le corresponde organizar los '
                             'procesos electorales, incluyendo el diseño de:',
                 'alternativas': ['Las cortes electorales',
                                  'El padrón judicial',
                                  'Las leyes electorales',
                                  'Los partidos políticos',
                                  'La cédula de sufragio'],
                 'correcta': 'E'},
                {'pregunta': 'El RENIEC tiene a su cargo la inscripción de '
                             'nacimientos, matrimonios, divorcios y:',
                 'alternativas': ['Contratos comerciales',
                                  'Defunciones',
                                  'Propiedades',
                                  'Vehículos',
                                  'Empresas'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo encargado de inscribir los actos '
                             'relativos a la capacidad y estado civil de las '
                             'personas naturales es: (II CEPRU 2023-II)',
                 'alternativas': ['RENIEC',
                                  'SUNAT',
                                  'JNE',
                                  'Registros Públicos',
                                  'ONPE'],
                 'correcta': 'A'},
                {'pregunta': 'El Organismo Constitucional Autónomo que '
                             'protege los derechos constitucionales de la '
                             'persona y la comunidad se denomina: (II CEPRU '
                             '2017-I)',
                 'alternativas': ['Comisión Andina de Juristas',
                                  'Ministerio de Justicia y Derechos Humanos',
                                  'Defensoría del Pueblo',
                                  'Asociación Pro Derechos Humanos',
                                  'Comisión de la Verdad y la '
                                  'Reconciliación'],
                 'correcta': 'C'},
                {'pregunta': 'Una atribución del Jurado Nacional de '
                             'Elecciones es: (II CEPRU 2017-I)',
                 'alternativas': ['Organizar y ejecutar los procesos '
                                  'electorales, referéndum y consultas '
                                  'populares',
                                  'Asignar un código único de identificación',
                                  'Confeccionar un registro único de '
                                  'identificación',
                                  'Proclamar a los candidatos elegidos y '
                                  'expedir las credenciales correspondientes',
                                  'Velar por la obtención de la fiel y libre '
                                  'expresión de la voluntad popular'],
                 'correcta': 'D'},
                {'pregunta': 'Es atribución de la Oficina Nacional de '
                             'Procesos Electorales (ONPE): (II CEPRU 2018-I)',
                 'alternativas': ['Expedir las credenciales a las '
                                  'autoridades elegidas',
                                  'Disponer la protección de la libertad '
                                  'personal en los comicios',
                                  'Fiscalizar la realización de los procesos '
                                  'electorales',
                                  'Organizar los procesos electorales',
                                  'Preparar el padrón electoral'],
                 'correcta': 'D'},
                {'pregunta': 'La atribución del JNE de mantener y custodiar '
                             'el registro de: (II CEPRU 2018-I)',
                 'alternativas': ['Personas Jurídicas',
                                  'Organizaciones Políticas',
                                  'Defunciones',
                                  'Personas Naturales',
                                  'Nacimientos'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo que prepara, mantiene y actualiza '
                             'el padrón electoral es: (II CEPRU 2018-I)',
                 'alternativas': ['El Jurado Nacional de Elecciones',
                                  'La Oficina Nacional de Procesos '
                                  'Electorales',
                                  'El Consejo Nacional de la Magistratura',
                                  'La Corte Superior de Justicia',
                                  'El Registro Nacional de Identificación y '
                                  'Estado Civil'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 201 de la Constitución, el '
                             'Tribunal Constitucional se compone de un '
                             'número de miembros igual a:',
                 'alternativas': ['Cinco', 'Nueve', 'Once', 'Tres', 'Siete'],
                 'correcta': 'E'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Cinco años',
                                  'Siete años',
                                  'Cuatro años',
                                  'Seis años',
                                  'Diez años'],
                 'correcta': 'A'}],
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
                                'año de anticipación.',
                                'Según el artículo 201 de la Constitución, '
                                'el Tribunal Constitucional se compone de '
                                'siete miembros elegidos por cinco años.',
                                'No hay reelección inmediata de los miembros '
                                'del Tribunal Constitucional.']},
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
                {'titulo': '14.5 LA LIBERTAD CONTRACTUAL',
                 'items': ['El artículo {62} de la Constitución declara que '
                           'la libertad de contratar garantiza que las '
                           'partes pueden pactar válidamente según las '
                           'normas {vigentes} al tiempo del contrato.',
                           'La libertad de contratar incluye el derecho a '
                           'decidir la {celebración} o no de un contrato.',
                           'También incluye el derecho a {elegir} con quién '
                           'contratar.',
                           'También incluye el derecho de {regular} el '
                           'contenido de los contratos, lo que constituye '
                           'propiamente la libertad contractual.',
                           'La libertad contractual constituye un derecho '
                           '{relacional}, pues a través de su ejercicio se '
                           'ejecutan otros derechos como la libertad de '
                           'comercio y de trabajo.']},
                {'titulo': '14.6 EL TRIBUTO Y SUS CLASES',
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
                {'titulo': '14.7 PRINCIPIOS DE LA POTESTAD TRIBUTARIA',
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
                 'alternativas': ['Las empresas privadas',
                                  'El sector informal',
                                  'Los sindicatos',
                                  'Los organismos internacionales',
                                  'El Estado en materia económica'],
                 'correcta': 'E'},
                {'pregunta': 'Según García Belaúnde, la Constitución '
                             'Económica surgió en:',
                 'alternativas': ['La Antigüedad clásica',
                                  'El siglo XXI',
                                  'La época colonial',
                                  'El siglo XIX',
                                  'El periodo de entreguerras del siglo XX'],
                 'correcta': 'E'},
                {'pregunta': 'La constitución considerada pionera del '
                             'constitucionalismo económico es la de:',
                 'alternativas': ['Cádiz',
                                  'Weimar',
                                  'Bayona',
                                  'Roma',
                                  'Filadelfia'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución de Weimar garantiza el derecho '
                             'de:',
                 'alternativas': ['Nacionalización total',
                                  'Propiedad, con límites por el bien '
                                  'general',
                                  'Voto universal',
                                  'Libre comercio sin restricciones',
                                  'Monopolio estatal'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen económico peruano se basa, entre '
                             'otros principios, en la economía social de:',
                 'alternativas': ['Planificación central',
                                  'Estado',
                                  'Autarquía',
                                  'Mercado',
                                  'Trueque'],
                 'correcta': 'D'},
                {'pregunta': 'La economía social de mercado es '
                             'representativa de los valores de:',
                 'alternativas': ['Aislamiento económico',
                                  'Libertad y justicia',
                                  'Autoridad y jerarquía',
                                  'Uniformidad y control',
                                  'Propiedad colectiva obligatoria'],
                 'correcta': 'B'},
                {'pregunta': 'Según Herhärd y Müller Armack, la economía '
                             'social de mercado transforma la productividad '
                             'individual en:',
                 'alternativas': ['Estancamiento económico',
                                  'Progreso social',
                                  'Monopolio privado',
                                  'Control estatal total',
                                  'Ganancia exclusiva de empresarios'],
                 'correcta': 'B'},
                {'pregunta': 'La economía social de mercado combate la '
                             'formación de:',
                 'alternativas': ['Carteles y concentración de poder '
                                  'económico',
                                  'Cooperativas',
                                  'Mercados locales',
                                  'Sindicatos',
                                  'Pequeñas empresas'],
                 'correcta': 'A'},
                {'pregunta': 'Para que funcione de manera óptima el mercado, '
                             'el Estado debe:',
                 'alternativas': ['Establecer normas claras sin intervenir '
                                  'de manera permanente',
                                  'Intervenir permanentemente',
                                  'Controlar todos los precios',
                                  'Nacionalizar las empresas',
                                  'Eliminar la competencia'],
                 'correcta': 'A'},
                {'pregunta': 'La economía social de mercado requiere un '
                             'Estado:',
                 'alternativas': ['Ausente en la economía',
                                  'Fuerte e independiente de los grupos de '
                                  'poder económico',
                                  'Débil y dependiente de grupos de poder',
                                  'Sin aparato judicial',
                                  'Controlado por monopolios'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de solidaridad en la economía '
                             'social de mercado exige:',
                 'alternativas': ['Individualismo extremo',
                                  'Aislamiento económico',
                                  'Competencia sin límites',
                                  'Equilibrio social y promoción del bien '
                                  'común',
                                  'Monopolio estatal'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de subsidiaridad establece que el '
                             'Estado no debe hacer:',
                 'alternativas': ['Ninguna función pública',
                                  'Lo que el individuo puede hacer por '
                                  'propia iniciativa',
                                  'Regulación económica',
                                  'Control tributario',
                                  'Políticas sociales'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado y la competencia, según el texto, '
                             'deben garantizar la libertad de:',
                 'alternativas': ['Solo los bancos',
                                  'Solo los inversionistas extranjeros',
                                  'Solo el Estado',
                                  'Consumidores, empleadores y trabajadores',
                                  'Solo los empresarios'],
                 'correcta': 'D'},
                {'pregunta': 'Combatir los monopolios requiere, según el '
                             'texto, una legislación:',
                 'alternativas': ['De control de precios',
                                  'De nacionalización',
                                  'De protección arancelaria total',
                                  'Antimonopolio',
                                  'De libre mercado absoluto'],
                 'correcta': 'D'},
                {'pregunta': 'El régimen económico también se define como el '
                             'conjunto de reglas de juego con rango:',
                 'alternativas': ['Municipal',
                                  'Constitucional',
                                  'Internacional exclusivo',
                                  'Reglamentario',
                                  'Consuetudinario'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los principios que rigen el régimen '
                             'económico peruano figura la libre:',
                 'alternativas': ['Migración',
                                  'Censura',
                                  'Expropiación',
                                  'Competencia',
                                  'Nacionalización'],
                 'correcta': 'D'},
                {'pregunta': 'El régimen económico busca contribuir '
                             'positivamente al:',
                 'alternativas': ['Cierre de fronteras',
                                  'Desempeño económico del país',
                                  'Aislamiento comercial',
                                  'Control absoluto del mercado',
                                  'Monopolio estatal'],
                 'correcta': 'B'},
                {'pregunta': 'El aparato administrativo y judicial en la '
                             'economía social de mercado debe ser:',
                 'alternativas': ['Eliminado del sistema',
                                  'Independiente y libre de corrupción',
                                  'Controlado por empresas privadas',
                                  'Subordinado al Congreso',
                                  'Dependiente del poder económico'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, en una economía social de mercado, '
                             'actúa por medio de:',
                 'alternativas': ['El control absoluto de empresas',
                                  'La intervención directa en precios',
                                  'La eliminación del mercado',
                                  'La propiedad estatal de todo',
                                  'El sistema monetario y el ordenamiento '
                                  'jurídico'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los principios del régimen económico '
                             'constitucional peruano figura la igualdad de '
                             'tratamiento al:',
                 'alternativas': ['Estado',
                                  'Poder Judicial',
                                  'Congreso',
                                  'Capital',
                                  'Poder Ejecutivo'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo 58 de la Constitución establece '
                             'que la iniciativa privada es libre, ejercida '
                             'en una economía:',
                 'alternativas': ['Social de mercado',
                                  'Centralmente planificada',
                                  'Cerrada exclusiva',
                                  'Colectivizada',
                                  'De subsistencia'],
                 'correcta': 'A'},
                {'pregunta': 'El reconocimiento constitucional de las '
                             'libertades económicas en el Perú se inicia con '
                             'el texto de:',
                 'alternativas': ['1979', '1856', '1993', '1920', '1823'],
                 'correcta': 'E'},
                {'pregunta': 'La libertad de empresa comprende, entre otras '
                             'facultades, emprender, crear, organizar, '
                             'gestionar y:',
                 'alternativas': ['Contaminar libremente',
                                  'Monopolizar el mercado',
                                  'Evitar la competencia',
                                  'Cerrar la empresa',
                                  'Evadir impuestos'],
                 'correcta': 'D'},
                {'pregunta': 'La libertad de comercio se define como la '
                             'capacidad de mediar entre la oferta y:',
                 'alternativas': ['Los tratados internacionales',
                                  'El Estado',
                                  'La banca central',
                                  'El sistema tributario',
                                  'La demanda'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 59, el ejercicio de la '
                             'libertad de comercio no debe ser lesivo a la '
                             'moral, la salud o:',
                 'alternativas': ['Las ganancias',
                                  'El comercio exterior',
                                  'Las utilidades',
                                  'Los impuestos',
                                  'La seguridad pública'],
                 'correcta': 'E'},
                {'pregunta': 'La libertad de industria consiste en la '
                             'facultad de realizar operaciones para la '
                             'obtención o transformación de:',
                 'alternativas': ['Divisas exclusivas',
                                  'Servicios exclusivamente',
                                  'Capital financiero exclusivo',
                                  'Mano de obra exclusiva',
                                  'Productos naturales'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 65 de la Constitución establece un '
                             'deber especial de protección a:',
                 'alternativas': ['Los bancos',
                                  'Los inversionistas exclusivos',
                                  'Los empresarios',
                                  'El Estado exclusivamente',
                                  'Los consumidores y usuarios'],
                 'correcta': 'E'},
                {'pregunta': 'El tributo es el género, y sus especies son el '
                             'impuesto, la tasa y:',
                 'alternativas': ['El arancel exclusivo',
                                  'El interés',
                                  'La contribución',
                                  'La multa',
                                  'La comisión'],
                 'correcta': 'C'},
                {'pregunta': 'El fundamento del impuesto es la capacidad:',
                 'alternativas': ['Legal',
                                  'Contributiva',
                                  'Comercial exclusiva',
                                  'Administrativa',
                                  'Patrimonial exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La recaudación de impuestos es controlada '
                             'mediante el principio de caja:',
                 'alternativas': ['Regional',
                                  'Múltiple',
                                  'Compartida',
                                  'Única',
                                  'Descentralizada'],
                 'correcta': 'D'},
                {'pregunta': 'La tasa tiene como hecho gravado un servicio '
                             'público:',
                 'alternativas': ['Colectivo exclusivo',
                                  'Voluntario',
                                  'Individualizado',
                                  'Gratuito exclusivo',
                                  'Optativo'],
                 'correcta': 'C'},
                {'pregunta': 'La contribución es el tributo cuya obligación '
                             'tiene como hecho generador beneficios '
                             'derivados de obras públicas o:',
                 'alternativas': ['Herencias',
                                  'Préstamos bancarios',
                                  'Actividades estatales',
                                  'Donaciones',
                                  'Ventas privadas'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 74, los tributos se crean, '
                             'modifican o derogan exclusivamente por ley o:',
                 'alternativas': ['Ordenanza municipal exclusiva',
                                  'Reglamento interno',
                                  'Decreto supremo exclusivo',
                                  'Resolución ministerial',
                                  'Decreto legislativo en caso de '
                                  'delegación'],
                 'correcta': 'E'},
                {'pregunta': 'Los gobiernos locales pueden crear, modificar '
                             'y suprimir contribuciones y tasas dentro de '
                             'su:',
                 'alternativas': ['Cartera ministerial',
                                  'Jurisdicción',
                                  'Circunscripción electoral',
                                  'Presupuesto exclusivo',
                                  'Consejo Regional'],
                 'correcta': 'B'},
                {'pregunta': 'Ningún tributo puede tener efecto:',
                 'alternativas': ['Proporcional',
                                  'Confiscatorio',
                                  'Progresivo',
                                  'Regresivo',
                                  'Retroactivo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 74, los decretos de urgencia '
                             'no pueden contener materia:',
                 'alternativas': ['Ambiental',
                                  'Educativa',
                                  'Tributaria',
                                  'Laboral exclusiva',
                                  'Presupuestaria exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de reserva de la ley establece '
                             'que solo por ley se puede determinar al '
                             'contribuyente y fijar:',
                 'alternativas': ['El banco receptor',
                                  'La fecha de pago exclusivamente',
                                  'El nombre del tributo',
                                  'El monto del tributo',
                                  'El lugar de pago'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que complementa la reserva de '
                             'ley, referido al uso del instrumento legal '
                             'permitido por su titular, se llama principio '
                             'de:',
                 'alternativas': ['Proporcionalidad',
                                  'Igualdad',
                                  'No confiscatoriedad',
                                  'Legalidad',
                                  'Capacidad contributiva'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de igualdad tributaria establece '
                             'que situaciones iguales deben ser tratadas '
                             'igualmente y las situaciones desiguales:',
                 'alternativas': ['De forma arbitraria',
                                  'También igualmente',
                                  'Con exención total',
                                  'Desigualmente',
                                  'Sin ningún criterio'],
                 'correcta': 'D'},
                {'pregunta': 'En el régimen tributario, conforma un impuesto '
                             'indirecto: (IV CEPRU 2025-I)',
                 'alternativas': ['Impuesto a los Activos Netos',
                                  'Impuesto al Patrimonio Vehicular',
                                  'Impuesto a la Venta de Arroz Pilado',
                                  'Impuesto a la Renta',
                                  'Impuesto General a las Ventas'],
                 'correcta': 'E'},
                {'pregunta': '¿Cómo se llama el título de la Constitución '
                             'que regula la economía del país? (II CEPRU '
                             '2022-II)',
                 'alternativas': ['De las Garantías Constitucionales',
                                  'Los Tributos',
                                  'Estructura del Estado',
                                  'Del Estado y la Nación',
                                  'Régimen Económico'],
                 'correcta': 'E'},
                {'pregunta': 'La tercera vía entre el capitalismo y el '
                             'socialismo es la: (I CEPRU 2016-I)',
                 'alternativas': ['Economía Liberal',
                                  'Economía Subordinada',
                                  'Economía Transversal',
                                  'Economía Mixta Radical',
                                  'Economía Social de Mercado'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución que declara que '
                             'la libertad de contratar garantiza que las '
                             'partes pueden pactar válidamente es el '
                             'artículo:',
                 'alternativas': ['Artículo 70',
                                  'Artículo 62',
                                  'Artículo 65',
                                  'Artículo 58',
                                  'Artículo 59'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las manifestaciones de la libertad de '
                             'contratar está el derecho a decidir la '
                             'celebración o no de un contrato, y el derecho '
                             'a:',
                 'alternativas': ['Suspender contratos ajenos',
                                  'Evadir impuestos',
                                  'Anular cualquier contrato',
                                  'Elegir con quién contratar',
                                  'Modificar leyes tributarias'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho de regular el contenido de los '
                             'contratos, es decir los derechos y '
                             'obligaciones de las partes, constituye '
                             'propiamente la:',
                 'alternativas': ['Libertad de empresa',
                                  'Libertad de industria',
                                  'Libertad de trabajo',
                                  'Libertad de comercio',
                                  'Libertad contractual'],
                 'correcta': 'E'},
                {'pregunta': 'La libertad contractual es considerada un '
                             'derecho relacional porque, a través de su '
                             'ejercicio, se ejecutan otros derechos como:',
                 'alternativas': ['La libertad de expresión',
                                  'El derecho al voto',
                                  'La libertad de comercio y de trabajo',
                                  'El derecho a la vida',
                                  'El derecho a la salud'],
                 'correcta': 'C'}],
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
                                'naturales.']},
                     {'titulo': 'LA LIBERTAD CONTRACTUAL',
                      'items': ['El artículo 62 de la Constitución declara '
                                'que la libertad de contratar garantiza que '
                                'las partes pueden pactar válidamente según '
                                'las normas vigentes al tiempo del contrato.',
                                'La libertad de contratar incluye el derecho '
                                'a decidir la celebración o no de un '
                                'contrato.',
                                'También incluye el derecho a elegir con '
                                'quién contratar.',
                                'También incluye el derecho de regular el '
                                'contenido de los contratos, lo que '
                                'constituye propiamente la libertad '
                                'contractual.',
                                'La libertad contractual constituye un '
                                'derecho relacional, pues a través de su '
                                'ejercicio se ejecutan otros derechos como '
                                'la libertad de comercio y de trabajo.']},
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
                                'legal permitido por su respectivo '
                                'titular.']}],
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
                {'titulo': '15.5 INSTRUMENTOS LEGALES DE LOS GOBIERNOS '
                           'REGIONALES',
                 'items': ['Las {ordenanzas regionales} norman asuntos de '
                           'carácter general, organización y administración; '
                           'son dictadas por el {Consejo Regional} y '
                           'promulgadas por la presidencia.',
                           'Los {acuerdos regionales} expresan la decisión '
                           'del Consejo Regional sobre asuntos {internos} o '
                           'de interés público, ciudadano o institucional.',
                           'Los {decretos regionales} establecen normas '
                           'reglamentarias para la ejecución de las '
                           'ordenanzas regionales; son aprobados por la '
                           '{presidencia} regional.',
                           'Las {resoluciones regionales} norman asuntos de '
                           'carácter {administrativo}; tienen tres niveles: '
                           'ejecutiva regional, gerencial general regional y '
                           'gerencial regional.',
                           'La elección de autoridades municipales está '
                           'regulada por la Ley N.º {26864}.',
                           'Los {alcaldes} y regidores son elegidos por '
                           'sufragio directo para un periodo de {cuatro} '
                           'años, en forma conjunta.']},
                {'titulo': '15.6 LOS GOBIERNOS LOCALES',
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
                 'alternativas': ['Del sector financiero exclusivamente',
                                  'Del sector privado',
                                  'Solo del sistema educativo',
                                  'Solo del sistema judicial',
                                  'Del Estado peruano'],
                 'correcta': 'E'},
                {'pregunta': 'La descentralización busca alcanzar un '
                             'gobierno:',
                 'alternativas': ['Sin participación ciudadana',
                                  'Exclusivamente militar',
                                  'Efectivo, eficiente y al servicio de la '
                                  'ciudadanía',
                                  'Autoritario',
                                  'Centralizado y jerárquico'],
                 'correcta': 'C'},
                {'pregunta': 'Según Finot, la descentralización es un '
                             'proceso de transferencia desde el gobierno '
                             'nacional hacia:',
                 'alternativas': ['Organismos internacionales',
                                  'Una autoridad subnacional o local',
                                  'Ningún otro nivel de gobierno',
                                  'Las Fuerzas Armadas',
                                  'El sector privado'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización, según el texto, busca '
                             'reducir:',
                 'alternativas': ['Los servicios públicos',
                                  'La participación ciudadana',
                                  'El desarrollo regional',
                                  'La pobreza y la corrupción',
                                  'La inversión privada'],
                 'correcta': 'D'},
                {'pregunta': 'Un objetivo general de la descentralización es '
                             'que cada gobierno regional y local:',
                 'alternativas': ['Dependa del gobierno central para todo',
                                  'No participe en la gestión pública',
                                  'Se subordine a Lima',
                                  'Elimine su autonomía',
                                  'Decida sobre sus propios recursos'],
                 'correcta': 'E'},
                {'pregunta': 'Un objetivo político de la descentralización '
                             'es:',
                 'alternativas': ['El aislamiento regional',
                                  'El debilitamiento del Estado',
                                  'La unidad y eficiencia del Estado',
                                  'La centralización total',
                                  'La eliminación de gobiernos locales'],
                 'correcta': 'C'},
                {'pregunta': 'Un objetivo económico de la descentralización '
                             'es:',
                 'alternativas': ['Eliminar la inversión regional',
                                  'Reducir los servicios sociales',
                                  'El desarrollo económico autosostenido de '
                                  'las regiones',
                                  'Aumentar la dependencia central',
                                  'Concentrar recursos en Lima'],
                 'correcta': 'C'},
                {'pregunta': 'Otro objetivo económico de la '
                             'descentralización es la redistribución:',
                 'alternativas': ['Desigual de recursos',
                                  'Solo para zonas urbanas',
                                  'Equitativa de los recursos del Estado',
                                  'Exclusiva para Lima',
                                  'Centralizada de los recursos'],
                 'correcta': 'C'},
                {'pregunta': 'Históricamente, el Perú ha sido caracterizado '
                             'por los analistas como un país:',
                 'alternativas': ['Sin estructura política definida',
                                  'Federal',
                                  'Descentralizado desde su origen',
                                  'Confederado',
                                  'Centralista'],
                 'correcta': 'E'},
                {'pregunta': 'El «descentralismo centralista» se extiende '
                             'desde el inicio de la República hasta:',
                 'alternativas': ['2002', '1979', '1920', '1821', '1993'],
                 'correcta': 'C'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'provinieron principalmente de:',
                 'alternativas': ['Los movimientos indígenas',
                                  'Organismos internacionales',
                                  'Las provincias',
                                  'Los gobiernos regionales actuales',
                                  'El pensamiento capitalino, de la élite de '
                                  'Lima'],
                 'correcta': 'E'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'carecieron de:',
                 'alternativas': ['Presupuesto estatal',
                                  'Apoyo internacional',
                                  'Interés político',
                                  'Marco legal',
                                  'Respaldo social provinciano'],
                 'correcta': 'A'},
                {'pregunta': 'El periodo del federalismo fallido en el Perú '
                             'se ubica entre:',
                 'alternativas': ['1532 y 1821',
                                  '1900 y 1950',
                                  '1979 y 1993',
                                  '1993 y 2020',
                                  '1821 y 1873'],
                 'correcta': 'E'},
                {'pregunta': 'La descentralización es descrita como un '
                             'proceso:',
                 'alternativas': ['Exclusivamente fiscal',
                                  'Unidimensional',
                                  'Solo político',
                                  'Solo administrativo',
                                  'Multidimensional, con dinámicas '
                                  'políticas, fiscales y administrativas'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los objetivos generales de la '
                             'descentralización figura la participación de:',
                 'alternativas': ['Solo el gobierno central',
                                  'Solo las empresas privadas',
                                  'La sociedad civil',
                                  'Solo el sector militar',
                                  'Solo organismos internacionales'],
                 'correcta': 'C'},
                {'pregunta': 'La descentralización busca la integración '
                             'entre el Estado y:',
                 'alternativas': ['Solo el sector privado',
                                  'La sociedad civil',
                                  'Solo organismos extranjeros',
                                  'Solo las Fuerzas Armadas',
                                  'Ningún actor social'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los objetivos políticos figura la '
                             'institucionalización de:',
                 'alternativas': ['Un solo partido político',
                                  'Gobiernos temporales',
                                  'Gobiernos centralizados',
                                  'Regímenes militares',
                                  'Sólidos gobiernos regionales y locales'],
                 'correcta': 'E'},
                {'pregunta': 'Un objetivo económico es la cobertura de '
                             'servicios sociales básicos en:',
                 'alternativas': ['Solo la capital',
                                  'Solo zonas costeras',
                                  'Todo el territorio nacional',
                                  'Solo zonas fronterizas',
                                  'Solo zonas urbanas'],
                 'correcta': 'C'},
                {'pregunta': 'El descentralismo formó parte de casi todos '
                             'los proyectos políticos, pero por razones '
                             'estructurales:',
                 'alternativas': ['Se aplicaron de inmediato',
                                  'Se cumplieron totalmente',
                                  'Fueron rechazados por la población',
                                  'No generaron ningún debate',
                                  'No llegaron a concretarse'],
                 'correcta': 'E'},
                {'pregunta': 'La descentralización tiene como finalidad el '
                             'desarrollo integral, armónico y:',
                 'alternativas': ['Exclusivo de Lima',
                                  'Sostenible del país',
                                  'Temporal',
                                  'Limitado a la costa',
                                  'Solo económico'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano normativo y fiscalizador del '
                             'Gobierno Regional se llama:',
                 'alternativas': ['Presidencia Regional',
                                  'Gerencia Regional',
                                  'Consejo de Coordinación Regional',
                                  'Alcaldía Regional',
                                  'Consejo Regional'],
                 'correcta': 'E'},
                {'pregunta': 'Los consejeros regionales son elegidos por '
                             'sufragio directo por un periodo de:',
                 'alternativas': ['Seis años',
                                  'Dos años',
                                  'Cinco años',
                                  'Tres años',
                                  'Cuatro años'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano ejecutivo del Gobierno Regional se '
                             'llama Presidencia Regional; desde 2015 al '
                             'presidente se le llama:',
                 'alternativas': ['Alcalde Regional',
                                  'Delegado Regional',
                                  'Prefecto',
                                  'Gobernador Regional',
                                  'Ministro Regional'],
                 'correcta': 'D'},
                {'pregunta': 'El Consejo de Coordinación Regional está '
                             'integrado por alcaldes provinciales y '
                             'representantes de:',
                 'alternativas': ['La sociedad civil',
                                  'El Ejecutivo exclusivamente',
                                  'Otros gobiernos regionales exclusivamente',
                                  'El Poder Judicial',
                                  'El Congreso'],
                 'correcta': 'A'},
                {'pregunta': 'Las normas que regulan asuntos de carácter '
                             'general del gobierno regional se llaman:',
                 'alternativas': ['Directivas regionales',
                                  'Ordenanzas regionales',
                                  'Resoluciones regionales',
                                  'Decretos regionales',
                                  'Acuerdos regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas que expresan la decisión del '
                             'Consejo Regional sobre asuntos internos se '
                             'llaman:',
                 'alternativas': ['Resoluciones regionales',
                                  'Acuerdos regionales',
                                  'Circulares regionales',
                                  'Ordenanzas regionales',
                                  'Decretos regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas reglamentarias para ejecutar las '
                             'ordenanzas regionales, aprobadas por la '
                             'presidencia regional, se llaman:',
                 'alternativas': ['Directivas',
                                  'Decretos regionales',
                                  'Acuerdos regionales',
                                  'Resoluciones regionales',
                                  'Ordenanzas regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Locales conforman el nivel de '
                             'gobierno del Estado número:',
                 'alternativas': ['Quinto',
                                  'Segundo',
                                  'Primero',
                                  'Cuarto',
                                  'Tercero'],
                 'correcta': 'E'},
                {'pregunta': 'Los Gobiernos Locales también se denominan '
                             'municipalidades, y pueden ser provinciales o:',
                 'alternativas': ['Regionales',
                                  'Nacionales',
                                  'Distritales',
                                  'Departamentales',
                                  'Metropolitanas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los alcaldes son elegidos por sufragio directo '
                             'por un periodo de:',
                 'alternativas': ['Seis años',
                                  'Cuatro años',
                                  'Cinco años',
                                  'Dos años',
                                  'Tres años'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura orgánica básica de las '
                             'municipalidades está compuesta por el Concejo '
                             'Municipal y:',
                 'alternativas': ['El Consejo de Coordinación exclusivo',
                                  'El Consejo Regional',
                                  'La Alcaldía',
                                  'La Gerencia General',
                                  'La Junta Vecinal exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'El Concejo Municipal está conformado por el '
                             'alcalde y:',
                 'alternativas': ['Los regidores',
                                  'Los gerentes municipales',
                                  'Los vecinos elegidos',
                                  'Los jueces de paz',
                                  'El gobernador regional'],
                 'correcta': 'A'},
                {'pregunta': 'La Alcaldía es el órgano ejecutivo del '
                             'gobierno local; el alcalde es el representante '
                             'legal y su:',
                 'alternativas': ['Fiscalizador',
                                  'Consultor externo',
                                  'Vocero exclusivo',
                                  'Asesor jurídico',
                                  'Máxima autoridad administrativa'],
                 'correcta': 'E'},
                {'pregunta': 'Los mecanismos de participación ciudadana '
                             'municipal incluyen el Consejo de Coordinación '
                             'Local y:',
                 'alternativas': ['El Tribunal Municipal',
                                  'La Fiscalía Municipal',
                                  'Las Juntas de Delegados Vecinales',
                                  'El Poder Judicial Local',
                                  'El Congreso Local'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano normativo y fiscalizador dentro de '
                             'la organización de los gobiernos regionales '
                             'es: (IV CEPRU 2025-I)',
                 'alternativas': ['El Consejo Regional',
                                  'La Secretaría Regional',
                                  'El Gobernador Regional',
                                  'El Consejo de Coordinación',
                                  'La Gerencia Regional'],
                 'correcta': 'A'},
                {'pregunta': 'La autoridad que puede ser revocada es: (II '
                             'CEPRU 2025-I)',
                 'alternativas': ['Los jueces',
                                  'Los diputados',
                                  'Los congresistas',
                                  'Los senadores',
                                  'Los alcaldes'],
                 'correcta': 'E'},
                {'pregunta': 'Como antecedente de la descentralización en el '
                             'Perú existieron grupos antagónicos en la '
                             'organización de un Estado eficiente, '
                             'denominados: (IV CEPRU 2022-II)',
                 'alternativas': ['Caudillistas y centralistas',
                                  'Caciquistas y federalistas',
                                  'Federalistas y centralistas',
                                  'Regionalistas y centralistas',
                                  'Centralistas y caudillistas'],
                 'correcta': 'C'},
                {'pregunta': 'El instrumento legal regional que norma '
                             'asuntos de carácter general, dictado por el '
                             'Consejo Regional y promulgado por la '
                             'presidencia, es:',
                 'alternativas': ['El decreto regional',
                                  'La ordenanza regional',
                                  'El acuerdo regional',
                                  'La resolución regional',
                                  'El reglamento regional'],
                 'correcta': 'B'},
                {'pregunta': 'El instrumento legal que expresa la decisión '
                             'del Consejo Regional sobre sus asuntos '
                             'internos o de interés público se llama:',
                 'alternativas': ['Acuerdo regional',
                                  'Resolución regional',
                                  'Ley regional',
                                  'Decreto regional',
                                  'Ordenanza regional'],
                 'correcta': 'A'},
                {'pregunta': 'El instrumento legal que establece normas '
                             'reglamentarias para la ejecución de las '
                             'ordenanzas regionales, aprobado por la '
                             'presidencia regional, es:',
                 'alternativas': ['El edicto regional',
                                  'La resolución regional',
                                  'El acuerdo regional',
                                  'La ordenanza regional',
                                  'El decreto regional'],
                 'correcta': 'E'},
                {'pregunta': 'El instrumento legal regional que norma '
                             'asuntos de carácter administrativo, con tres '
                             'niveles (ejecutiva, gerencial general y '
                             'gerencial), es:',
                 'alternativas': ['El decreto regional',
                                  'La ordenanza regional',
                                  'La resolución regional',
                                  'El bando regional',
                                  'El acuerdo regional'],
                 'correcta': 'C'},
                {'pregunta': 'La elección de autoridades municipales en el '
                             'Perú está regulada por la Ley N.º:',
                 'alternativas': ['27783',
                                  '26300',
                                  '27972',
                                  '26864',
                                  '28056'],
                 'correcta': 'D'},
                {'pregunta': 'Los alcaldes y regidores son elegidos por '
                             'sufragio directo para un periodo de:',
                 'alternativas': ['Tres años',
                                  'Dos años',
                                  'Cinco años',
                                  'Cuatro años',
                                  'Seis años'],
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
                     {'titulo': 'INSTRUMENTOS LEGALES DE LOS GOBIERNOS '
                                'REGIONALES',
                      'items': ['Las ordenanzas regionales norman asuntos de '
                                'carácter general, organización y '
                                'administración; son dictadas por el Consejo '
                                'Regional y promulgadas por la presidencia.',
                                'Los acuerdos regionales expresan la '
                                'decisión del Consejo Regional sobre asuntos '
                                'internos o de interés público, ciudadano o '
                                'institucional.',
                                'Los decretos regionales establecen normas '
                                'reglamentarias para la ejecución de las '
                                'ordenanzas regionales; son aprobados por la '
                                'presidencia regional.',
                                'Las resoluciones regionales norman asuntos '
                                'de carácter administrativo; tienen tres '
                                'niveles: ejecutiva regional, gerencial '
                                'general regional y gerencial regional.',
                                'La elección de autoridades municipales está '
                                'regulada por la Ley N.º 26864.',
                                'Los alcaldes y regidores son elegidos por '
                                'sufragio directo para un periodo de cuatro '
                                'años, en forma conjunta.']},
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
                {'titulo': '16.4 ORIGEN DE LA CLASIFICACIÓN POR GENERACIONES',
                 'items': ['La división de los derechos humanos en tres '
                           'generaciones fue propuesta en {1979} por el '
                           'jurista checo {Karel Vasak}.',
                           'El Perú es firmante del Pacto Internacional de '
                           'Derechos Civiles y Políticos, ratificado por '
                           'Decreto Ley N.º {22128}, del 23 de marzo de '
                           '1976.',
                           'El Perú es firmante de la Convención Americana '
                           'de Derechos Humanos, conocida como el {Pacto de '
                           'San José} de Costa Rica, ratificada en {1978}.']},
                {'titulo': '16.5 EVOLUCIÓN: EL PRIMER MOMENTO O '
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
                {'titulo': '16.6 SEGUNDO MOMENTO: LA UNIVERSALIZACIÓN',
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
                {'titulo': '16.7 CLASIFICACIÓN POR GENERACIONES',
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
                {'titulo': '16.8 INSTRUMENTOS JURÍDICOS SUPRANACIONALES',
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
                 'alternativas': ['Su nivel económico',
                                  'Su edad',
                                  'Su religión',
                                  'Su nacionalidad',
                                  'Su condición humana'],
                 'correcta': 'E'},
                {'pregunta': 'Según Hernández Gómez, los derechos humanos '
                             'son condiciones que permiten a la persona:',
                 'alternativas': ['Su aislamiento',
                                  'Su dependencia del Estado',
                                  'Su realización',
                                  'Su sometimiento',
                                  'Su exclusión social'],
                 'correcta': 'C'},
                {'pregunta': 'Que los derechos humanos se apliquen a todos '
                             'sin distinción corresponde a la característica '
                             'de:',
                 'alternativas': ['Imprescriptibilidad',
                                  'Indivisibilidad',
                                  'Progresividad',
                                  'Universalidad',
                                  'Obligatoriedad'],
                 'correcta': 'D'},
                {'pregunta': 'Que los derechos humanos no se pierdan con el '
                             'paso del tiempo corresponde a que son:',
                 'alternativas': ['Inviolables',
                                  'Universales',
                                  'Imprescriptibles',
                                  'Progresivos',
                                  'Indisolubles'],
                 'correcta': 'C'},
                {'pregunta': 'Que no se pueda hablar de una división de los '
                             'derechos humanos corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Obligatorios',
                                  'Irreversibles',
                                  'Progresivos',
                                  'Indivisibles'],
                 'correcta': 'E'},
                {'pregunta': 'Que nadie pueda atentar contra los derechos '
                             'humanos corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Imprescriptibles',
                                  'Inviolables',
                                  'Universales',
                                  'Indisolubles'],
                 'correcta': 'C'},
                {'pregunta': 'Que un derecho reconocido quede integrado de '
                             'forma irrevocable corresponde a que son:',
                 'alternativas': ['Indivisibles',
                                  'Irreversibles',
                                  'Progresivos',
                                  'Obligatorios',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos formen un conjunto '
                             'inseparable corresponde a que son:',
                 'alternativas': ['Inviolables',
                                  'Imprescriptibles',
                                  'Progresivos',
                                  'Indisolubles',
                                  'Universales'],
                 'correcta': 'D'},
                {'pregunta': 'Que el Estado deba respetar los derechos '
                             'humanos aunque no exista ley expresa '
                             'corresponde a que son:',
                 'alternativas': ['Obligatorios',
                                  'Indivisibles',
                                  'Universales',
                                  'Progresivos',
                                  'Irreversibles'],
                 'correcta': 'A'},
                {'pregunta': 'Que puedan reconocerse nuevos derechos humanos '
                             'en el futuro corresponde a que son:',
                 'alternativas': ['Imprescriptibles',
                                  'Inviolables',
                                  'Universales',
                                  'Indisolubles',
                                  'Progresivos'],
                 'correcta': 'E'},
                {'pregunta': 'La evolución de los derechos humanos comprende '
                             'dos grandes momentos: la juridificación y:',
                 'alternativas': ['La internacionalización',
                                  'La secularización',
                                  'La regionalización',
                                  'La privatización',
                                  'La militarización'],
                 'correcta': 'A'},
                {'pregunta': 'La Carta Magna, o Petición de los Derechos, se '
                             'dio en Inglaterra en el año:',
                 'alternativas': ['1215', '1948', '1789', '1776', '1679'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de Habeas Corpus fue dictada en '
                             'Inglaterra en:',
                 'alternativas': ['1776', '1948', '1789', '1679', '1215'],
                 'correcta': 'D'},
                {'pregunta': 'El Acta de Independencia de Estados Unidos '
                             'data de:',
                 'alternativas': ['1948', '1789', '1776', '1215', '1679'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano corresponde a:',
                 'alternativas': ['Alemania, 1919',
                                  'Estados Unidos, 1776',
                                  'Francia, 1789',
                                  'España, 1812',
                                  'Inglaterra, 1215'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo de juridificación se caracteriza '
                             'porque los nuevos Estados modernos:',
                 'alternativas': ['Centralizaron el poder absoluto',
                                  'Prohibieron su difusión',
                                  'Introdujeron el reconocimiento y '
                                  'protección de estos derechos en sus '
                                  'legislaciones',
                                  'Rechazaron los derechos humanos',
                                  'Eliminaron toda garantía legal'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo de juridificación estuvo imbuido de '
                             'la ideología:',
                 'alternativas': ['Socialista',
                                  'Conservadora',
                                  'Absolutista',
                                  'Liberal',
                                  'Monárquica'],
                 'correcta': 'D'},
                {'pregunta': 'El ejercicio de rebeliones históricas para '
                             'lograr el reconocimiento de derechos demuestra '
                             'que estos son, en parte:',
                 'alternativas': ['Ajenos a la evolución humana',
                                  'Exclusivos de una nación',
                                  'Producto de un proceso histórico y social',
                                  'Impuestos por organismos internacionales',
                                  'Otorgados sin lucha por el Estado'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho a la vida, como derecho inviolable, '
                             'no puede ser violentado:',
                 'alternativas': ['Solo temporalmente',
                                  'En ninguna circunstancia',
                                  'Solo en situaciones de guerra',
                                  'Bajo excepciones económicas',
                                  'Solo por decisión judicial'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos humanos, según su carácter '
                             'obligatorio, deben respetarse:',
                 'alternativas': ['Solo si están en la ley nacional',
                                  'Solo por decisión del gobierno de turno',
                                  'Aunque no exista una ley que lo diga '
                                  'expresamente',
                                  'Solo si lo exige un tratado',
                                  'Solo en situaciones normales'],
                 'correcta': 'C'},
                {'pregunta': 'La división de los derechos humanos en tres '
                             'generaciones fue propuesta en 1979 por:',
                 'alternativas': ['John Rawls',
                                  'Rousseau',
                                  'Norberto Bobbio',
                                  'Hans Kelsen',
                                  'Karel Vasak'],
                 'correcta': 'E'},
                {'pregunta': 'Los derechos de primera generación consideran '
                             'a la persona como:',
                 'alternativas': ['Una nación',
                                  'Un grupo social',
                                  'Un sujeto colectivo',
                                  'Un individuo con libertad y autonomía',
                                  'Un pueblo indígena'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos de primera generación también se '
                             'conocen como derechos:',
                 'alternativas': ['Colectivos',
                                  'Civiles y políticos',
                                  'Económicos y sociales',
                                  'De solidaridad',
                                  'Difusos'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho más importante entre los de primera '
                             'generación es el derecho a:',
                 'alternativas': ['La paz',
                                  'El trabajo',
                                  'La sindicación',
                                  'La vida',
                                  'La propiedad'],
                 'correcta': 'D'},
                {'pregunta': 'El Perú ratificó el Pacto Internacional de '
                             'Derechos Civiles y Políticos mediante Decreto '
                             'Ley N°:',
                 'alternativas': ['27444',
                                  '22128',
                                  '25278',
                                  '26300',
                                  '28237'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos de segunda generación son '
                             'derechos económicos, sociales y:',
                 'alternativas': ['Culturales',
                                  'De solidaridad exclusiva',
                                  'Colectivos exclusivos',
                                  'Ambientales exclusivos',
                                  'Difusos'],
                 'correcta': 'A'},
                {'pregunta': 'La instauración de los derechos de segunda '
                             'generación provocó la sustitución del Estado '
                             'Liberal por el Estado:',
                 'alternativas': ['Absolutista',
                                  'Militar',
                                  'Social de Derecho',
                                  'Totalitario',
                                  'Confesional'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los derechos de segunda generación está '
                             'el derecho al trabajo y a la libre:',
                 'alternativas': ['Propiedad',
                                  'Emigración',
                                  'Sindicación',
                                  'Herencia',
                                  'Religión'],
                 'correcta': 'C'},
                {'pregunta': 'Los derechos de tercera generación también se '
                             'llaman derechos de:',
                 'alternativas': ['Libertad',
                                  'Solidaridad',
                                  'Igualdad',
                                  'Autonomía individual',
                                  'Propiedad'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de tercera generación se '
                             'reconocen a partir de la década de:',
                 'alternativas': ['1970', '1945', '1990', '1960', '1980'],
                 'correcta': 'E'},
                {'pregunta': 'Los titulares de los derechos de tercera '
                             'generación son sujetos:',
                 'alternativas': ['Colectivos',
                                  'Empresariales',
                                  'Individuales exclusivamente',
                                  'Estatales exclusivamente',
                                  'Religiosos exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los derechos de tercera generación está '
                             'la autodeterminación de los pueblos y la '
                             'protección de:',
                 'alternativas': ['El medio ambiente',
                                  'La banca',
                                  'Las telecomunicaciones',
                                  'El comercio',
                                  'La propiedad privada'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos humanos pueden conceptualizarse '
                             'desde cuatro dimensiones: histórica, ética, '
                             'política y:',
                 'alternativas': ['Económica',
                                  'Religiosa',
                                  'Jurídica',
                                  'Cultural exclusiva',
                                  'Social exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La dimensión de los derechos humanos que se '
                             'fundamenta en valores como la dignidad y la '
                             'libertad se llama dimensión:',
                 'alternativas': ['Histórica',
                                  'Ética',
                                  'Social',
                                  'Política',
                                  'Jurídica'],
                 'correcta': 'B'},
                {'pregunta': 'La dimensión de los derechos humanos que '
                             'refiere a su proclamación por la ONU se llama '
                             'dimensión:',
                 'alternativas': ['Jurídica',
                                  'Ética',
                                  'Política',
                                  'Económica',
                                  'Histórica'],
                 'correcta': 'C'},
                {'pregunta': 'El segundo momento en la evolución de los '
                             'derechos humanos, tras la juridificación, se '
                             'llama:',
                 'alternativas': ['Universalización',
                                  'Regionalización',
                                  'Descentralización',
                                  'Privatización',
                                  'Constitucionalización'],
                 'correcta': 'A'},
                {'pregunta': 'La universalización de los derechos humanos se '
                             'consolida con la Carta de San Francisco de '
                             '1945 y:',
                 'alternativas': ['La Carta Magna',
                                  'El Tratado de Versalles',
                                  'El Pacto de Varsovia',
                                  'La Convención de Ginebra exclusiva',
                                  'La Declaración Universal de los Derechos '
                                  'Humanos'],
                 'correcta': 'E'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos fue aprobada en la Asamblea General de '
                             'la ONU el 10 de diciembre de:',
                 'alternativas': ['1948', '1989', '1945', '1979', '1966'],
                 'correcta': 'A'},
                {'pregunta': 'La Carta Internacional de los Derechos Humanos '
                             'incluye la Carta de la ONU, la Declaración '
                             'Universal y:',
                 'alternativas': ['Los dos Pactos Internacionales de 1966',
                                  'Solo la Carta Magna',
                                  'Solo el Habeas Corpus',
                                  'La Convención de Viena exclusiva',
                                  'Solo tratados regionales'],
                 'correcta': 'A'},
                {'pregunta': 'La Convención Internacional para la prevención '
                             'y sanción del crimen de genocidio data de:',
                 'alternativas': ['1984', '1966', '1979', '1945', '1948'],
                 'correcta': 'E'},
                {'pregunta': 'La Convención contra la Tortura y otros tratos '
                             'crueles data de:',
                 'alternativas': ['1952', '1948', '1960', '1984', '1966'],
                 'correcta': 'D'},
                {'pregunta': 'La elaboración de la Declaración Universal de '
                             'los Derechos Humanos fue encargada a un comité '
                             'de redacción integrado por un número de '
                             'expertos igual a:',
                 'alternativas': ['Cinco', 'Quince', 'Ocho', 'Tres', 'Diez'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos consta de un preámbulo y un número de '
                             'artículos igual a:',
                 'alternativas': ['40', '30', '20', '50', '25'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración Universal de los Derechos '
                             'Humanos se aprobó el: (IV CEPRU 2025-I)',
                 'alternativas': ['10 de diciembre de 1948',
                                  '24 de octubre de 1945',
                                  '22 de noviembre de 1969',
                                  '26 de junio de 1945',
                                  '02 de mayo de 1948'],
                 'correcta': 'A'},
                {'pregunta': 'Los idiomas oficiales de la Corte '
                             'Internacional de Justicia son: (IV CEPRU '
                             '2025-I)',
                 'alternativas': ['Inglés y chino',
                                  'Inglés y francés',
                                  'Ruso y español',
                                  'Portugués e inglés',
                                  'Inglés y español'],
                 'correcta': 'B'},
                {'pregunta': 'Dentro de los instrumentos supranacionales de '
                             'protección de derechos humanos tenemos: (IV '
                             'CEPRU 2025-I)',
                 'alternativas': ['La Carta Magna de Juan Sin Tierra',
                                  'La Declaración Interamericana de los '
                                  'Derechos Humanos',
                                  'El Pacto Americano de los Derechos '
                                  'Económicos, Sociales y Culturales',
                                  'La Declaración Africana de los Derechos '
                                  'del Hombre y Ciudadano',
                                  'El Pacto Internacional de los Derechos '
                                  'Civiles y Políticos'],
                 'correcta': 'E'},
                {'pregunta': 'Son un conjunto de bienes materiales heredados '
                             'como legado, transmitidos a futuras '
                             'generaciones a lo largo de la historia: (I '
                             'CEPRU 2023-II)',
                 'alternativas': ['Patrimonio inmaterial',
                                  'Fuentes culturales',
                                  'Patrimonio natural',
                                  'Patrimonio material',
                                  'Patrimonio cultural'],
                 'correcta': 'D'},
                {'pregunta': 'En la clasificación de los Derechos Humanos, '
                             'el derecho a la protección de la salud '
                             'pertenece a la generación: (IV CEPRU 2022-I)',
                 'alternativas': ['Cuarta',
                                  'Segunda',
                                  'Tercera',
                                  'Quinta',
                                  'Primera'],
                 'correcta': 'B'},
                {'pregunta': 'Los Derechos Humanos de tercera generación '
                             'reconocen el derecho a la: (II CEPRU 2022-I)',
                 'alternativas': ['Libertad y seguridad personal',
                                  'Libre sindicación y protección de la '
                                  'salud',
                                  'Paz y protección del medio ambiente',
                                  'Igualdad ante la ley y libertad de '
                                  'conciencia',
                                  'Propiedad y herencia'],
                 'correcta': 'C'},
                {'pregunta': 'La división de los derechos humanos en tres '
                             'generaciones fue propuesta en 1979 por el '
                             'jurista checo:',
                 'alternativas': ['Luigi Ferrajoli',
                                  'Karel Vasak',
                                  'Hans Kelsen',
                                  'Norberto Bobbio',
                                  'Robert Alexy'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú ratificó el Pacto Internacional de '
                             'Derechos Civiles y Políticos mediante el '
                             'Decreto Ley N.º:',
                 'alternativas': ['27972',
                                  '26300',
                                  '26497',
                                  '22128',
                                  '26864'],
                 'correcta': 'D'},
                {'pregunta': 'La Convención Americana de Derechos Humanos es '
                             'conocida también como el Pacto de:',
                 'alternativas': ['Ciudad de México',
                                  'Lima',
                                  'Panamá',
                                  'San José de Costa Rica',
                                  'Bogotá'],
                 'correcta': 'D'}],
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
                     {'titulo': 'ORIGEN DE LA CLASIFICACIÓN POR GENERACIONES',
                      'items': ['La división de los derechos humanos en tres '
                                'generaciones fue propuesta en 1979 por el '
                                'jurista checo Karel Vasak.',
                                'El Perú es firmante del Pacto Internacional '
                                'de Derechos Civiles y Políticos, ratificado '
                                'por Decreto Ley N.º 22128, del 23 de marzo '
                                'de 1976.',
                                'El Perú es firmante de la Convención '
                                'Americana de Derechos Humanos, conocida '
                                'como el Pacto de San José de Costa Rica, '
                                'ratificada en 1978.']},
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
                 'alternativas': ['Una sanción administrativa',
                                  'Un beneficio',
                                  'Un contrato civil',
                                  'Una obligación tributaria',
                                  'Un peligro en el disfrute de los '
                                  'derechos'],
                 'correcta': 'E'},
                {'pregunta': 'Las Garantías Constitucionales tienen su '
                             'origen en la tradición:',
                 'alternativas': ['Romana',
                                  'Alemana',
                                  'Francesa',
                                  'Española',
                                  'Inglesa'],
                 'correcta': 'C'},
                {'pregunta': 'En el Perú, la institucionalidad de las '
                             'garantías se inicia con la Constitución de:',
                 'alternativas': ['1993', '1856', '1920', '1979', '1933'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución de 1920 distinguió tres tipos '
                             'de garantías: nacionales, individuales y:',
                 'alternativas': ['Sociales',
                                  'Económicas',
                                  'Religiosas',
                                  'Culturales',
                                  'Militares'],
                 'correcta': 'A'},
                {'pregunta': 'Según García Toma, las Garantías '
                             'Constitucionales aseguran el disfrute de los '
                             'derechos:',
                 'alternativas': ['Solo privados',
                                  'Solo políticos',
                                  'Solo económicos',
                                  'Públicos y privados',
                                  'Solo públicos'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'establece las Garantías Constitucionales es '
                             'el:',
                 'alternativas': ['Artículo 149',
                                  'Artículo 200',
                                  'Artículo 51',
                                  'Artículo 24',
                                  'Artículo 91'],
                 'correcta': 'B'},
                {'pregunta': 'El número de Garantías Constitucionales '
                             'establecidas en el artículo 200 es:',
                 'alternativas': ['Ocho', 'Seis', 'Cuatro', 'Tres', 'Diez'],
                 'correcta': 'B'},
                {'pregunta': 'La primera garantía constitucional reconocida '
                             'en el Perú, en 1920, fue:',
                 'alternativas': ['La Acción de Cumplimiento',
                                  'La Acción de Amparo',
                                  'La Acción Popular',
                                  'El Habeas Data',
                                  'El Habeas Corpus'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción Popular fue incorporada en la '
                             'Constitución de:',
                 'alternativas': ['1933', '1993', '1920', '1856', '1979'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción de Amparo y la Acción de '
                             'Inconstitucionalidad se incorporaron en la '
                             'Constitución de:',
                 'alternativas': ['1856', '1979', '1993', '1933', '1920'],
                 'correcta': 'B'},
                {'pregunta': 'El Habeas Data y la Acción de Cumplimiento se '
                             'incorporaron en la Constitución de:',
                 'alternativas': ['1993', '1856', '1979', '1920', '1933'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión «habeas corpus» significa '
                             'literalmente:',
                 'alternativas': ['Que traigas el cuerpo',
                                  'Justicia inmediata',
                                  'Protege al pueblo',
                                  'Derecho supremo',
                                  'Libertad total'],
                 'correcta': 'A'},
                {'pregunta': 'El antecedente histórico del habeas corpus es '
                             'la ley inglesa de:',
                 'alternativas': ['1215', '1679', '1993', '1948', '1789'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus protege principalmente:',
                 'alternativas': ['La propiedad privada',
                                  'La libertad individual y la seguridad '
                                  'personal',
                                  'La libertad de prensa únicamente',
                                  'El comercio exterior',
                                  'Los derechos laborales exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus se presenta, en primera '
                             'instancia, ante:',
                 'alternativas': ['El Juez especializado en lo Penal',
                                  'El Tribunal Constitucional',
                                  'El Ministerio Público',
                                  'El Congreso',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'A'},
                {'pregunta': 'Si no hay Juez Penal disponible, el habeas '
                             'corpus se presenta ante:',
                 'alternativas': ['El Fiscal de la Nación',
                                  'El Defensor del Pueblo',
                                  'El Juez de Paz Letrado',
                                  'El Presidente de la Corte Suprema',
                                  'El Alcalde'],
                 'correcta': 'C'},
                {'pregunta': 'La última y definitiva instancia para resolver '
                             'denegatorias de habeas corpus es:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'La Defensoría del Pueblo',
                                  'El Ministerio Público',
                                  'La Corte Suprema',
                                  'El Congreso'],
                 'correcta': 'A'},
                {'pregunta': 'La acción de habeas corpus se caracteriza por '
                             'estar exenta de:',
                 'alternativas': ['Formalidades',
                                  'Sustento fáctico',
                                  'Revisión judicial',
                                  'Plazos procesales',
                                  'Competencia territorial'],
                 'correcta': 'A'},
                {'pregunta': 'Para presentar un habeas corpus NO se '
                             'requiere:',
                 'alternativas': ['Presentar el escrito ante juez competente',
                                  'Un hecho vulnerador',
                                  'Poder, tasas judiciales ni firma de '
                                  'letrado',
                                  'Identificar a la autoridad responsable',
                                  'Señalar el derecho vulnerado'],
                 'correcta': 'C'},
                {'pregunta': 'El habeas corpus puede formularse:',
                 'alternativas': ['Solo mediante representante legal',
                                  'Únicamente en audiencia pública',
                                  'Solo por escrito con abogado',
                                  'Exclusivamente por vía electrónica',
                                  'Por escrito o verbalmente, en forma '
                                  'directa o por correo'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción de Amparo fue introducida por '
                             'primera vez, como garantía distinta al hábeas '
                             'corpus, en la Constitución de:',
                 'alternativas': ['1933', '1993', '1856', '1979', '1920'],
                 'correcta': 'D'},
                {'pregunta': 'La Acción de Amparo protege todos los derechos '
                             'constitucionales, excepto los protegidos por '
                             'hábeas corpus y:',
                 'alternativas': ['Acción popular',
                                  'Hábeas data',
                                  'Cumplimiento',
                                  'Inconstitucionalidad',
                                  'Proceso competencial'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para presentar la Acción de Amparo es '
                             'de 60 días desde la vulneración del derecho, '
                             'salvo en sentencias judiciales, donde el plazo '
                             'es de:',
                 'alternativas': ['10 días',
                                  '45 días',
                                  '30 días',
                                  '15 días',
                                  '90 días'],
                 'correcta': 'C'},
                {'pregunta': 'El Hábeas Data fue introducido por la '
                             'Constitución de:',
                 'alternativas': ['1933', '1856', '1979', '1920', '1993'],
                 'correcta': 'E'},
                {'pregunta': 'El Hábeas Data protege el derecho a solicitar '
                             'y recibir información, y la protección de la '
                             'intimidad:',
                 'alternativas': ['Política',
                                  'Empresarial',
                                  'Personal y familiar',
                                  'Comercial',
                                  'Religiosa'],
                 'correcta': 'C'},
                {'pregunta': 'El plazo para presentar el Hábeas Data es de '
                             '60 días hábiles después de:',
                 'alternativas': ['El acto administrativo',
                                  'La publicación de la norma',
                                  'La notificación fiscal',
                                  'La sentencia judicial',
                                  'La respuesta denegatoria'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción de Inconstitucionalidad se crea con '
                             'la Constitución de:',
                 'alternativas': ['1979', '1920', '1993', '1933', '1856'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción de Inconstitucionalidad es la única '
                             'garantía que se presenta en:',
                 'alternativas': ['Instancia única y definitiva',
                                  'Instancia administrativa',
                                  'Doble instancia',
                                  'Tres instancias',
                                  'Primera instancia'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los facultados para interponer Acción de '
                             'Inconstitucionalidad está un grupo de '
                             'ciudadanos con firmas comprobadas por el JNE, '
                             'en número no menor a:',
                 'alternativas': ['5000', '1000', '500', '2000', '10000'],
                 'correcta': 'A'},
                {'pregunta': 'El plazo para interponer una Acción de '
                             'Inconstitucionalidad es de 6 años desde su '
                             'publicación, y en tratados internacionales el '
                             'plazo es de:',
                 'alternativas': ['2 años',
                                  '3 meses',
                                  '6 meses',
                                  '6 años también',
                                  '1 año'],
                 'correcta': 'C'},
                {'pregunta': 'Para resolver la Acción de '
                             'Inconstitucionalidad se requiere el voto a '
                             'favor de un número de magistrados del Tribunal '
                             'Constitucional igual a:',
                 'alternativas': ['6', '7', '3', '5', '4'],
                 'correcta': 'D'},
                {'pregunta': 'La Acción Popular se originó en la justicia '
                             'romana y se introdujo por primera vez en la '
                             'Constitución de:',
                 'alternativas': ['1933', '1856', '1979', '1993', '1920'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción Popular procede contra normas de '
                             'rango de decretos y resoluciones, y es '
                             'competencia exclusiva de:',
                 'alternativas': ['La Contraloría',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'El Ejecutivo',
                                  'El Poder Judicial'],
                 'correcta': 'E'},
                {'pregunta': 'El plazo para interponer una Acción Popular es '
                             'de:',
                 'alternativas': ['10 años',
                                  '3 años',
                                  '5 años',
                                  '6 años',
                                  '1 año'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Cumplimiento fue creada por la '
                             'Constitución de:',
                 'alternativas': ['1920', '1933', '1979', '1993', '1856'],
                 'correcta': 'D'},
                {'pregunta': 'La Acción de Cumplimiento sirve para hacer '
                             'cumplir normas legales o:',
                 'alternativas': ['Reglamentos internos',
                                  'Decisiones empresariales',
                                  'Actos administrativos',
                                  'Sentencias privadas',
                                  'Contratos comerciales'],
                 'correcta': 'C'},
                {'pregunta': 'El plazo para presentar la Acción de '
                             'Cumplimiento es de 60 días después de:',
                 'alternativas': ['La notificación fiscal',
                                  'La publicación de la norma',
                                  'La demanda inicial',
                                  'No haberse cumplido el mandato',
                                  'La sentencia'],
                 'correcta': 'D'},
                {'pregunta': 'La vulneración o amenaza, por cualquier '
                             'autoridad, del derecho de solicitar '
                             'información de cualquier entidad pública, es '
                             'protegida por la acción: (IV CEPRU 2025-I)',
                 'alternativas': ['Popular',
                                  'De Habeas Corpus',
                                  'De Inconstitucionalidad',
                                  'De Habeas Data',
                                  'De Amparo'],
                 'correcta': 'D'},
                {'pregunta': 'La garantía constitucional que protege la '
                             'libertad individual y la seguridad personal '
                             'corresponde a la acción de: (IV CEPRU 2022-II)',
                 'alternativas': ['Inconstitucionalidad',
                                  'Habeas Corpus',
                                  'Habeas Data',
                                  'Amparo',
                                  'Constitucionalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Habeas Data, introducida por '
                             'primera vez en la Constitución de 1993, tiene '
                             'por objeto la protección del ciudadano frente '
                             'al abuso de: (IV CEPRU 2022-I)',
                 'alternativas': ['La información nacional e internacional',
                                  'Las autoridades civiles y políticas',
                                  'La informática vinculada con el derecho a '
                                  'la privacidad',
                                  'La comunicación familiar y social',
                                  'La información social y cultural'],
                 'correcta': 'C'},
                {'pregunta': 'La Acción de Cumplimiento, que procede contra '
                             'cualquier autoridad o funcionario renuente a '
                             'acatar una norma legal, se interpone ante el '
                             'juez: (IV CEPRU 2022-I)',
                 'alternativas': ['Laboral',
                                  'De Familia',
                                  'Civil',
                                  'Penal',
                                  'Agrario'],
                 'correcta': 'C'}],
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
                {'titulo': '18.3 SISTEMA UNIVERSAL: LA ONU Y LA DUDH',
                 'items': ['La {ONU} fue creada el {24 de octubre} de 1945, '
                           'con la adopción de la Carta de las Naciones '
                           'Unidas, ratificada por 50 Estados en la '
                           'Conferencia de {San Francisco}.',
                           'La {Declaración Universal de Derechos Humanos} '
                           '(DUDH) fue adoptada el 10 de diciembre de '
                           '{1948}, mediante Resolución de la Asamblea '
                           'General N.º {217 (III)}.',
                           'La DUDH reconoce un total de {30} derechos, '
                           'tanto civiles y políticos como económicos, '
                           'sociales y culturales.',
                           'La DUDH fue una afirmación de buenas '
                           'intenciones, sin carácter {vinculante}, y no '
                           'establece mecanismo específico de {reclamo}.',
                           'Dentro de la ONU, los órganos encargados de la '
                           'promoción y protección de derechos humanos son '
                           'la Asamblea General, la Secretaría General y el '
                           '{ECOSOC} (Consejo Económico y Social).',
                           'La ONU está actualmente integrada por {193} '
                           'Estados miembros.']},
                {'titulo': '18.4 ORGANIZACIÓN Y FINES DE LA ONU',
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
                {'titulo': '18.5 EL SISTEMA INTERAMERICANO (SIDH)',
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
                {'titulo': '18.6 LA COMISIÓN INTERAMERICANA DE DERECHOS '
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
                           'informe anual ante la Asamblea General.',
                           'La Comisión Interamericana de Derechos Humanos '
                           'está compuesta por {siete} miembros, elegidos '
                           'por un periodo de {cuatro} años, reelegibles una '
                           'sola vez.']},
                {'titulo': '18.7 LA CORTE INTERAMERICANA Y LA CORTE DE LA '
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
                 'alternativas': ['La Cruz Roja',
                                  'La Sociedad de Naciones',
                                  'La OEA',
                                  'El Pacto Andino',
                                  'La OTAN'],
                 'correcta': 'B'},
                {'pregunta': 'La Sociedad de Naciones se estableció en el '
                             'año:',
                 'alternativas': ['1939', '1918', '1945', '1914', '1919'],
                 'correcta': 'E'},
                {'pregunta': 'La Sociedad de Naciones se estableció en '
                             'virtud del Tratado de:',
                 'alternativas': ['Westfalia',
                                  'Ancón',
                                  'Versalles',
                                  'Roma',
                                  'Ginebra'],
                 'correcta': 'C'},
                {'pregunta': 'El fracaso de la Sociedad de Naciones '
                             'desembocó en:',
                 'alternativas': ['La Revolución Rusa',
                                  'La Primera Guerra Mundial',
                                  'La Segunda Guerra Mundial',
                                  'La Guerra Fría',
                                  'La Guerra de Corea'],
                 'correcta': 'C'},
                {'pregunta': 'El nombre «Naciones Unidas» fue acuñado por:',
                 'alternativas': ['Harry Truman',
                                  'Joseph Stalin',
                                  'Woodrow Wilson',
                                  'Franklin D. Roosevelt',
                                  'Winston Churchill'],
                 'correcta': 'D'},
                {'pregunta': 'El nombre «Naciones Unidas» se usó por primera '
                             'vez en:',
                 'alternativas': ['1919', '1945', '1939', '1942', '1950'],
                 'correcta': 'D'},
                {'pregunta': 'La Carta de las Naciones Unidas fue firmada el '
                             '26 de junio de:',
                 'alternativas': ['1945', '1950', '1942', '1939', '1919'],
                 'correcta': 'A'},
                {'pregunta': 'La Carta de la ONU fue firmada inicialmente '
                             'por:',
                 'alternativas': ['26 países',
                                  '100 países',
                                  '50 países',
                                  '10 países',
                                  '193 países'],
                 'correcta': 'C'},
                {'pregunta': 'Las Naciones Unidas empezaron a existir '
                             'oficialmente el:',
                 'alternativas': ['1 de enero de 1942',
                                  '10 de diciembre de 1948',
                                  '26 de junio de 1945',
                                  '1 de enero de 1945',
                                  '24 de octubre de 1945'],
                 'correcta': 'E'},
                {'pregunta': 'El 24 de octubre se celebra como:',
                 'alternativas': ['El Día de los Derechos Humanos',
                                  'El Día de la Democracia',
                                  'El Día del Multilateralismo',
                                  'El Día de la Paz Mundial',
                                  'El Día de las Naciones Unidas'],
                 'correcta': 'E'},
                {'pregunta': 'La ONU tiene actualmente un número de Estados '
                             'Miembros de:',
                 'alternativas': ['250', '150', '193', '51', '100'],
                 'correcta': 'C'},
                {'pregunta': 'La sede principal de la ONU se ubica en:',
                 'alternativas': ['Ginebra',
                                  'París',
                                  'Nueva York',
                                  'Viena',
                                  'Nairobi'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las sedes secundarias de la ONU figura:',
                 'alternativas': ['Roma',
                                  'Londres',
                                  'Berlín',
                                  'Ginebra',
                                  'Madrid'],
                 'correcta': 'D'},
                {'pregunta': 'Los idiomas oficiales de la ONU son seis, '
                             'entre ellos figura:',
                 'alternativas': ['El árabe',
                                  'El portugués',
                                  'El italiano',
                                  'El japonés',
                                  'El alemán'],
                 'correcta': 'A'},
                {'pregunta': 'La ONU está compuesta por un número de órganos '
                             'principales igual a:',
                 'alternativas': ['Diez', 'Cuatro', 'Ocho', 'Tres', 'Seis'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano de la ONU encargado de la paz y '
                             'seguridad internacional es:',
                 'alternativas': ['El Consejo Económico y Social',
                                  'La Corte Internacional de Justicia',
                                  'La Asamblea General',
                                  'El Secretario General',
                                  'El Consejo de Seguridad'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano judicial principal de la ONU es:',
                 'alternativas': ['El Consejo Económico y Social',
                                  'La Corte Internacional de Justicia',
                                  'El Consejo de Administración Fiduciaria',
                                  'La Asamblea General',
                                  'El Consejo de Seguridad'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los fines de la ONU figura defender y '
                             'garantizar:',
                 'alternativas': ['Los Derechos Humanos',
                                  'Solo el turismo',
                                  'Solo el comercio internacional',
                                  'Solo la seguridad militar',
                                  'Solo la moneda internacional'],
                 'correcta': 'A'},
                {'pregunta': 'Un Estado que infringe los principios de la '
                             'Carta de la ONU puede ser:',
                 'alternativas': ['Anexado a otro país',
                                  'Excluido temporalmente o expulsado',
                                  'Ignorado sin consecuencias',
                                  'Premiado',
                                  'Automáticamente disuelto'],
                 'correcta': 'B'},
                {'pregunta': 'Estados no miembros de la ONU, como el '
                             'Vaticano, pueden tener estatuto de:',
                 'alternativas': ['Sancionado permanente',
                                  'Fundador',
                                  'Excluido total',
                                  'Miembro pleno',
                                  'Observador, sin derecho a voto'],
                 'correcta': 'E'},
                {'pregunta': 'El Sistema Interamericano de Protección de los '
                             'Derechos Humanos (SIDH) opera en el marco de:',
                 'alternativas': ['El FMI',
                                  'La UNASUR',
                                  'La UNESCO',
                                  'La ONU',
                                  'La OEA'],
                 'correcta': 'E'},
                {'pregunta': 'La Declaración Americana de los Deberes y '
                             'Derechos del Hombre se aprobó en:',
                 'alternativas': ['1945', '1978', '1948', '1959', '1969'],
                 'correcta': 'C'},
                {'pregunta': 'La Convención Americana de Derechos Humanos se '
                             'aprobó el 22 de noviembre de:',
                 'alternativas': ['1959', '1990', '1948', '1978', '1969'],
                 'correcta': 'E'},
                {'pregunta': 'El SIDH está constituido por dos organismos: '
                             'la Corte Interamericana y la:',
                 'alternativas': ['Fiscalía Interamericana',
                                  'Comisión Interamericana',
                                  'Asamblea de la OEA',
                                  'Corte de La Haya',
                                  'Corte Suprema Regional'],
                 'correcta': 'B'},
                {'pregunta': 'La CIDH se originó de la Declaración de '
                             'Santiago, redactada en:',
                 'alternativas': ['1959', '1970', '1948', '1978', '1965'],
                 'correcta': 'A'},
                {'pregunta': 'El Protocolo que estableció a la CIDH como '
                             'órgano principal de la OEA se llama Protocolo '
                             'de:',
                 'alternativas': ['Buenos Aires',
                                  'San José',
                                  'Washington',
                                  'Lima',
                                  'Santiago'],
                 'correcta': 'A'},
                {'pregunta': 'La sede de la Comisión Interamericana de '
                             'Derechos Humanos está en:',
                 'alternativas': ['Ginebra',
                                  'Nueva York',
                                  'La Haya',
                                  'San José de Costa Rica',
                                  'Washington DC'],
                 'correcta': 'E'},
                {'pregunta': 'La Comisión Interamericana está compuesta por '
                             'un número de miembros igual a:',
                 'alternativas': ['Siete',
                                  'Once',
                                  'Cinco',
                                  'Nueve',
                                  'Quince'],
                 'correcta': 'A'},
                {'pregunta': 'La Corte Interamericana de Derechos Humanos se '
                             'instaló en el año:',
                 'alternativas': ['1969', '1959', '1948', '1990', '1978'],
                 'correcta': 'E'},
                {'pregunta': 'La sede de la Corte Interamericana de Derechos '
                             'Humanos está en:',
                 'alternativas': ['Washington DC',
                                  'La Haya',
                                  'San José de Costa Rica',
                                  'Bogotá',
                                  'Ginebra'],
                 'correcta': 'C'},
                {'pregunta': 'Los jueces de la Corte Interamericana son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Cuatro años',
                                  'Ocho años',
                                  'Diez años',
                                  'Cinco años',
                                  'Seis años'],
                 'correcta': 'E'},
                {'pregunta': 'La Corte Interamericana cumple una función '
                             'jurisdiccional y otra función llamada:',
                 'alternativas': ['Consultiva',
                                  'Fiscalizadora',
                                  'Ejecutiva',
                                  'Legislativa',
                                  'Administrativa'],
                 'correcta': 'A'},
                {'pregunta': 'La Corte Internacional de Justicia, o Corte de '
                             'La Haya, es el principal órgano judicial de:',
                 'alternativas': ['La OEA',
                                  'La UNESCO',
                                  'La ONU',
                                  'El FMI',
                                  'La Unión Europea'],
                 'correcta': 'C'},
                {'pregunta': 'La Corte de La Haya tiene su sede en el '
                             'Palacio de la Paz, ubicado en:',
                 'alternativas': ['Bruselas, Bélgica',
                                  'Nueva York, Estados Unidos',
                                  'Ginebra, Suiza',
                                  'La Haya, Países Bajos',
                                  'Viena, Austria'],
                 'correcta': 'D'},
                {'pregunta': 'La Corte de La Haya está encargada de decidir '
                             'controversias jurídicas entre:',
                 'alternativas': ['Organizaciones no gubernamentales',
                                  'Personas naturales',
                                  'Municipios',
                                  'Estados',
                                  'Empresas privadas'],
                 'correcta': 'D'},
                {'pregunta': 'El número de magistrados de la Corte '
                             'Internacional de Justicia es:',
                 'alternativas': ['Once',
                                  'Nueve',
                                  'Siete',
                                  'Quince',
                                  'Veintiuno'],
                 'correcta': 'D'},
                {'pregunta': '¿Cuál es la sede de la Corte Interamericana de '
                             'los Derechos Humanos? (IV CEPRU 2023-II)',
                 'alternativas': ['Barcelona',
                                  'Lima',
                                  'Nueva York',
                                  'San José',
                                  'Washington D.C.'],
                 'correcta': 'D'},
                {'pregunta': 'Es uno de los instrumentos supranacionales de '
                             'protección de los Derechos Humanos: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['Convenio de Miami',
                                  'Petición de Derechos',
                                  'Constitución Política del Perú',
                                  'Convención de los Derechos Políticos de '
                                  'la Mujer',
                                  'Declaración de los Derechos Civiles y '
                                  'Políticos'],
                 'correcta': 'D'},
                {'pregunta': 'La institución constituida por 7 jueces '
                             'elegidos a título personal con reconocida '
                             'competencia en derechos humanos es la: (II '
                             'CEPRU 2023-II)',
                 'alternativas': ['Corte Interamericana de Derechos Humanos',
                                  'Corte de la Haya',
                                  'Comisión Interamericana de Derechos '
                                  'Humanos',
                                  'Corte Internacional de Justicia',
                                  'Corte Americana de Justicia'],
                 'correcta': 'A'},
                {'pregunta': 'El principal órgano judicial de las Naciones '
                             'Unidas, con sede en el Palacio de la Paz, es '
                             'la Corte: (IV CEPRU 2022-II)',
                 'alternativas': ['Marcial de Justicia',
                                  'Subalterna de Justicia',
                                  'Internacional de Justicia',
                                  'Superior de Justicia',
                                  'Suprema de Justicia'],
                 'correcta': 'C'},
                {'pregunta': 'La ONU fue creada el 24 de octubre de 1945, '
                             'con la adopción de la Carta de las Naciones '
                             'Unidas, ratificada en la Conferencia de:',
                 'alternativas': ['La Haya',
                                  'San Francisco',
                                  'Nueva York',
                                  'Washington',
                                  'Ginebra'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos '
                             'fue adoptada el 10 de diciembre de 1948 '
                             'mediante Resolución de la Asamblea General '
                             'N.º:',
                 'alternativas': ['194 (II)',
                                  '96 (I)',
                                  '377 (V)',
                                  '217 (III)',
                                  '260 (III)'],
                 'correcta': 'D'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos '
                             'reconoce un total de derechos igual a:',
                 'alternativas': ['20', '10', '50', '30', '40'],
                 'correcta': 'D'},
                {'pregunta': 'Dentro de la ONU, además de la Asamblea '
                             'General y la Secretaría General, el órgano '
                             'encargado de la promoción y protección de '
                             'derechos humanos es el:',
                 'alternativas': ['Secretariado Técnico',
                                  'ECOSOC',
                                  'Consejo de Seguridad',
                                  'Consejo de Administración Fiduciaria',
                                  'Tribunal Internacional'],
                 'correcta': 'B'},
                {'pregunta': 'Actualmente, la ONU está integrada por un '
                             'número de Estados miembros igual a:',
                 'alternativas': ['193', '200', '150', '220', '175'],
                 'correcta': 'A'},
                {'pregunta': 'La Comisión Interamericana de Derechos Humanos '
                             'está compuesta por un número de miembros igual '
                             'a:',
                 'alternativas': ['Siete',
                                  'Nueve',
                                  'Quince',
                                  'Cinco',
                                  'Once'],
                 'correcta': 'A'}],
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
                     {'titulo': 'SISTEMA UNIVERSAL: LA ONU Y LA DUDH',
                      'items': ['La ONU fue creada el 24 de octubre de 1945, '
                                'con la adopción de la Carta de las Naciones '
                                'Unidas, ratificada por 50 Estados en la '
                                'Conferencia de San Francisco.',
                                'La Declaración Universal de Derechos '
                                'Humanos (DUDH) fue adoptada el 10 de '
                                'diciembre de 1948, mediante Resolución de '
                                'la Asamblea General N.º 217 (III).',
                                'La DUDH reconoce un total de 30 derechos, '
                                'tanto civiles y políticos como económicos, '
                                'sociales y culturales.',
                                'La DUDH fue una afirmación de buenas '
                                'intenciones, sin carácter vinculante, y no '
                                'establece mecanismo específico de reclamo.',
                                'Dentro de la ONU, los órganos encargados de '
                                'la promoción y protección de derechos '
                                'humanos son la Asamblea General, la '
                                'Secretaría General y el ECOSOC (Consejo '
                                'Económico y Social).',
                                'La ONU está actualmente integrada por 193 '
                                'Estados miembros.']},
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
                                'un informe anual ante la Asamblea General.',
                                'La Comisión Interamericana de Derechos '
                                'Humanos está compuesta por siete miembros, '
                                'elegidos por un periodo de cuatro años, '
                                'reelegibles una sola vez.']},
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
