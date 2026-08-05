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
                 'alternativas': ['Lex', 'Ius', 'Directum', 'Mores', 'Ethos'],
                 'correcta': 'B'},
                {'pregunta': 'El vocablo latino «Directum», aplicado tras el '
                             'Corpus Iuris Civilis, significa:',
                 'alternativas': ['Costumbre',
                                  'Justicia',
                                  'Recto, conforme a la norma',
                                  'Autoridad',
                                  'Sanción'],
                 'correcta': 'C'},
                {'pregunta': 'Para Mario Alzamora Valdez, el Derecho es la '
                             'regulación de la vida social del hombre para '
                             'alcanzar:',
                 'alternativas': ['El orden',
                                  'La justicia',
                                  'La libertad',
                                  'La paz social',
                                  'La igualdad'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de normas jurídicas que forman el '
                             'ordenamiento vigente (Constitución, leyes, '
                             'códigos) corresponde al Derecho:',
                 'alternativas': ['Subjetivo',
                                  'Natural',
                                  'Objetivo',
                                  'Consuetudinario',
                                  'Positivo'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho a la vida, a la libertad o a la '
                             'propiedad son ejemplos del Derecho:',
                 'alternativas': ['Objetivo',
                                  'Subjetivo',
                                  'Consuetudinario',
                                  'Público',
                                  'Comparado'],
                 'correcta': 'B'},
                {'pregunta': 'En el derecho subjetivo, la persona sobre la '
                             'cual recae un deber correlativo es el:',
                 'alternativas': ['Sujeto activo',
                                  'Objeto del derecho',
                                  'Sujeto pasivo',
                                  'Titular del derecho',
                                  'Legislador'],
                 'correcta': 'C'},
                {'pregunta': 'Las fuentes que hacen referencia a los '
                             'orígenes mediatos de la norma jurídica '
                             '(factores sociales, económicos y culturales) '
                             'se denominan:',
                 'alternativas': ['Formales',
                                  'Materiales o reales',
                                  'Jurisprudenciales',
                                  'Doctrinarias',
                                  'Consuetudinarias'],
                 'correcta': 'B'},
                {'pregunta': 'La forma de conducta implantada por una '
                             'colectividad, repetida de manera uniforme y '
                             'permanente, cuya observancia se hace '
                             'obligatoria, es:',
                 'alternativas': ['La ley',
                                  'La doctrina',
                                  'La costumbre',
                                  'La jurisprudencia',
                                  'La equidad'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de resoluciones emitidas por la '
                             'Corte Suprema y el Tribunal Constitucional '
                             'sobre una cuestión determinada constituye:',
                 'alternativas': ['La doctrina',
                                  'La jurisprudencia',
                                  'La costumbre',
                                  'Los principios generales',
                                  'La ley'],
                 'correcta': 'B'},
                {'pregunta': 'Los estudios especializados del derecho, que '
                             'dan lugar a escuelas y teorías jurídicas pero '
                             'carecen de fuerza legal obligatoria, '
                             'constituyen:',
                 'alternativas': ['La jurisprudencia',
                                  'La costumbre',
                                  'La doctrina',
                                  'La ley',
                                  'La casuística'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 139 de la Constitución '
                             'vigente, los principios generales del derecho '
                             'tienen:',
                 'alternativas': ['Solo valor referencial',
                                  'Fuerza de ley',
                                  'Valor supletorio únicamente',
                                  'Aplicación exclusiva penal',
                                  'Carácter consuetudinario'],
                 'correcta': 'B'},
                {'pregunta': 'Que una ley deba ser cumplida por todos los '
                             'que están en el territorio donde rige, incluso '
                             'en contra de su voluntad, corresponde a su '
                             'carácter:',
                 'alternativas': ['Impersonal',
                                  'Abstracto',
                                  'Obligatorio',
                                  'Permanente',
                                  'Coercitivo'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ley se aplique a un grupo indeterminado '
                             'de sujetos y no a una sola persona corresponde '
                             'a su carácter:',
                 'alternativas': ['Coercitivo',
                                  'Impersonal',
                                  'Irretroactivo',
                                  'General',
                                  'Permanente'],
                 'correcta': 'B'},
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
                 'alternativas': ['Abstracto',
                                  'Coercitivo',
                                  'Permanente',
                                  'Impersonal',
                                  'General'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, la palabra «Moral» proviene '
                             'del latín «mores», que significa:',
                 'alternativas': ['Justicia',
                                  'Costumbre',
                                  'Deber',
                                  'Virtud',
                                  'Ley'],
                 'correcta': 'B'},
                {'pregunta': 'Respecto de su ámbito, la Moral es interior y '
                             'el Derecho es:',
                 'alternativas': ['Bilateral',
                                  'Coercible',
                                  'Exterior',
                                  'Heterónomo',
                                  'Autónomo'],
                 'correcta': 'C'},
                {'pregunta': 'Que la Moral solo imponga deberes cuyo '
                             'cumplimiento no genera ningún derecho, a '
                             'diferencia del Derecho que concede facultades '
                             'y señala deberes, corresponde a la diferencia '
                             'por su(s):',
                 'alternativas': ['Origen',
                                  'Fuerza',
                                  'Efectos',
                                  'Campo de acción',
                                  'Ámbito'],
                 'correcta': 'C'},
                {'pregunta': 'Que la Moral surja espontáneamente por '
                             'decisión personal y sea renunciable, mientras '
                             'que el Derecho emane de un poder extraño de '
                             'cumplimiento ineludible, corresponde a la '
                             'diferencia por su:',
                 'alternativas': ['Ámbito',
                                  'Origen',
                                  'Fuerza',
                                  'Campo de acción',
                                  'Efecto'],
                 'correcta': 'B'},
                {'pregunta': 'Que la Moral sea incoercible (sin fuerza que '
                             'obligue su cumplimiento) y el Derecho sea '
                             'coercible (con poder coercitivo que exige su '
                             'cumplimiento) corresponde a la diferencia por '
                             'su:',
                 'alternativas': ['Campo de acción',
                                  'Ámbito',
                                  'Origen',
                                  'Fuerza',
                                  'Efecto'],
                 'correcta': 'D'}]},
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
                                  'Gnoseología',
                                  'Lógica',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «justicia» proviene de la '
                             'voz latina:',
                 'alternativas': ['Iustitia',
                                  'Solidus',
                                  'Honestitad',
                                  'Dignitas',
                                  'Veritas'],
                 'correcta': 'A'},
                {'pregunta': 'La justicia que busca el bien de la sociedad '
                             'entera se llama:',
                 'alternativas': ['Particular',
                                  'General',
                                  'Judicial',
                                  'Distributiva',
                                  'Conmutativa'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia aplicada por un juez al emitir '
                             'sentencia se denomina:',
                 'alternativas': ['General',
                                  'Particular',
                                  'Judicial',
                                  'Social',
                                  'Conmutativa'],
                 'correcta': 'C'},
                {'pregunta': 'La forma clásica de justicia, entre individuos '
                             'como pares independientes, es la:',
                 'alternativas': ['Distributiva',
                                  'Social',
                                  'Conmutativa',
                                  'General',
                                  'Particular'],
                 'correcta': 'C'},
                {'pregunta': 'La justicia que considera al individuo frente '
                             'al todo social es la:',
                 'alternativas': ['Conmutativa',
                                  'Distributiva',
                                  'Judicial',
                                  'Particular',
                                  'General'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «solidaridad» proviene del latín '
                             '«solidus», que significa:',
                 'alternativas': ['Ayuda',
                                  'Sólido, firme, compacto',
                                  'Unión',
                                  'Colaboración',
                                  'Fraternidad'],
                 'correcta': 'B'},
                {'pregunta': 'La honestidad se define principalmente como el '
                             'respeto a:',
                 'alternativas': ['La ley',
                                  'La verdad',
                                  'La autoridad',
                                  'La costumbre',
                                  'La religión'],
                 'correcta': 'B'},
                {'pregunta': 'La dignidad humana depende de:',
                 'alternativas': ['La raza y el sexo',
                                  'Ningún condicionamiento externo, es '
                                  'inherente al ser humano',
                                  'La condición social',
                                  'El nivel educativo',
                                  'La nacionalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad se define como la capacidad de la '
                             'persona de:',
                 'alternativas': ['Obedecer las normas',
                                  'Autodeterminarse y actuar según su '
                                  'voluntad',
                                  'Depender de otros',
                                  'Seguir la mayoría',
                                  'Evitar responsabilidades'],
                 'correcta': 'B'},
                {'pregunta': 'La solidaridad se practica sin distinción de:',
                 'alternativas': ['Solo edad',
                                  'Credo, sexo, raza o afiliación política',
                                  'Solo nacionalidad',
                                  'Solo género',
                                  'Solo religión'],
                 'correcta': 'B'},
                {'pregunta': 'Los valores representan, en síntesis:',
                 'alternativas': ['Normas legales obligatorias',
                                  'Lo mejor que la vida humana puede ofrecer',
                                  'Costumbres regionales',
                                  'Reglas religiosas',
                                  'Tradiciones familiares'],
                 'correcta': 'B'},
                {'pregunta': 'Adicionalmente a la Filosofía, estudian los '
                             'valores de forma aplicada:',
                 'alternativas': ['Solo la Biología',
                                  'La Sociología, la Economía y la Política',
                                  'Solo la Medicina',
                                  'La Astronomía',
                                  'La Física'],
                 'correcta': 'B'},
                {'pregunta': 'La igualdad implica que todas las personas '
                             'tienen ante la ley:',
                 'alternativas': ['Distintos derechos según su riqueza',
                                  'Los mismos derechos y oportunidades',
                                  'Derechos según su edad',
                                  'Privilegios especiales',
                                  'Ninguna garantía'],
                 'correcta': 'B'},
                {'pregunta': 'El respeto se define como el reconocimiento '
                             'de:',
                 'alternativas': ['Solo la autoridad estatal',
                                  'El valor propio y los derechos de los '
                                  'demás',
                                  'Las tradiciones religiosas',
                                  'Las normas de tránsito',
                                  'Los símbolos patrios'],
                 'correcta': 'B'},
                {'pregunta': 'En la antigua Grecia, el concepto de valores '
                             'se trataba:',
                 'alternativas': ['De forma muy especializada por '
                                  'disciplinas',
                                  'Como algo general y sin divisiones',
                                  'Solo en el ámbito religioso',
                                  'Exclusivamente en la política',
                                  'Solo entre filósofos estoicos'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia social comprende:',
                 'alternativas': ['Solo decisiones judiciales',
                                  'El conjunto de decisiones, normas y '
                                  'principios razonables de una organización '
                                  'social',
                                  'Solo normas religiosas',
                                  'Únicamente leyes penales',
                                  'Solo acuerdos económicos'],
                 'correcta': 'B'},
                {'pregunta': 'Tener valores se relaciona directamente con:',
                 'alternativas': ['Acumular riqueza',
                                  'Respetar a los demás',
                                  'Ganar poder político',
                                  'Evitar el trabajo',
                                  'Buscar fama'],
                 'correcta': 'B'},
                {'pregunta': 'La honestidad, en su sentido más evidente, '
                             'implica coherencia entre:',
                 'alternativas': ['El pensamiento y la apariencia',
                                  'El comportamiento, la expresión y la '
                                  'verdad',
                                  'La riqueza y el estatus',
                                  'La edad y la experiencia',
                                  'El poder y la autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'La dignidad, según la distinción de '
                             'Millán-Puelles, puede ser ontológica o:',
                 'alternativas': ['Social',
                                  'Adquirida',
                                  'Legal',
                                  'Política',
                                  'Religiosa'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['El Libro I',
                                  'El Libro II',
                                  'El Libro III',
                                  'El Libro IV',
                                  'La Constitución'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, la palabra «persona» '
                             'originalmente designaba:',
                 'alternativas': ['Un cargo político',
                                  'La máscara usada por los actores de '
                                  'teatro',
                                  'Un título nobiliario',
                                  'Un documento legal',
                                  'Una ceremonia religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'Según Aníbal Torres Vásquez, la existencia de '
                             'la persona natural comienza con:',
                 'alternativas': ['El nacimiento',
                                  'La concepción',
                                  'El registro civil',
                                  'Los 18 años',
                                  'El bautizo'],
                 'correcta': 'B'},
                {'pregunta': 'La existencia de la persona natural termina '
                             'con:',
                 'alternativas': ['La jubilación',
                                  'La muerte',
                                  'Los 100 años',
                                  'La incapacidad',
                                  'El matrimonio'],
                 'correcta': 'B'},
                {'pregunta': 'Según Fernández Sessarego, la persona humana '
                             'es una unidad:',
                 'alternativas': ['Solo física',
                                  'Psicosomática',
                                  'Solo espiritual',
                                  'Únicamente legal',
                                  'Solo social'],
                 'correcta': 'B'},
                {'pregunta': 'El Libro I del Código Civil se divide en '
                             'cuántas secciones:',
                 'alternativas': ['Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis'],
                 'correcta': 'C'},
                {'pregunta': 'Las comunidades campesinas y nativas se '
                             'regulan dentro de:',
                 'alternativas': ['El derecho penal',
                                  'El Libro I del Código Civil',
                                  'El derecho laboral',
                                  'El derecho tributario',
                                  'La ley de municipalidades'],
                 'correcta': 'B'},
                {'pregunta': 'La persona puede definirse también como un '
                             'sujeto:',
                 'alternativas': ['Sin obligaciones',
                                  'Consciente y racional, titular de '
                                  'derechos y obligaciones',
                                  'Solo con derechos',
                                  'Sin capacidad legal',
                                  'Exclusivamente económico'],
                 'correcta': 'B'},
                {'pregunta': 'El ser humano es considerado un ser social '
                             'porque:',
                 'alternativas': ['Vive completamente aislado',
                                  'Se realiza plenamente en convivencia con '
                                  'otros',
                                  'No necesita normas',
                                  'Prefiere la soledad',
                                  'Depende solo de sí mismo'],
                 'correcta': 'B'},
                {'pregunta': 'Las personas jurídicas se diferencian de las '
                             'personas naturales en que:',
                 'alternativas': ['No tienen personería legal',
                                  'Son entidades con personería legal '
                                  'distinta a un individuo',
                                  'Son siempre empresas',
                                  'No tienen derechos',
                                  'Solo existen en el derecho penal'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad se define como el conjunto de '
                             'personas que comparten:',
                 'alternativas': ['Solo un territorio',
                                  'Cultura, normas e instituciones comunes',
                                  'Solo un idioma',
                                  'Solo una religión',
                                  'Solo una economía'],
                 'correcta': 'B'},
                {'pregunta': 'El «Derecho de las personas» regula el '
                             'reconocimiento de:',
                 'alternativas': ['Solo derechos patrimoniales',
                                  'Los derechos fundamentales de la persona',
                                  'Solo obligaciones tributarias',
                                  'Solo derechos políticos',
                                  'Solo derechos laborales'],
                 'correcta': 'B'},
                {'pregunta': 'En la Edad Media, el término «persona» se usó '
                             'como sinónimo de:',
                 'alternativas': ['Esclavo',
                                  'Portador de dignidades',
                                  'Comerciante',
                                  'Soldado',
                                  'Campesino'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra persona es considerada, según el '
                             'texto, equívoca y:',
                 'alternativas': ['Unívoca',
                                  'Polisémica',
                                  'Simple',
                                  'Restringida',
                                  'Exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Las asociaciones, fundaciones y comités NO '
                             'inscritos se regulan en:',
                 'alternativas': ['El derecho penal',
                                  'El Libro I del Código Civil, tercera '
                                  'sección',
                                  'La Constitución exclusivamente',
                                  'El derecho internacional',
                                  'Ninguna norma'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio antropológico revela que el hombre '
                             'es un ser:',
                 'alternativas': ['Cerrado y limitado',
                                  'Abierto al infinito',
                                  'Puramente material',
                                  'Sin capacidad de trascender',
                                  'Determinado biológicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad psicosomática de la persona implica '
                             'que lo que afecta al cuerpo:',
                 'alternativas': ['No afecta a la psique',
                                  'Repercute también en la psique, y '
                                  'viceversa',
                                  'Es independiente de la mente',
                                  'Solo afecta la salud física',
                                  'No tiene relación con las emociones'],
                 'correcta': 'B'},
                {'pregunta': 'La persona jurídica se distingue por tener:',
                 'alternativas': ['Existencia biológica',
                                  'Personería legal reconocida',
                                  'Solo obligaciones morales',
                                  'Capacidad física',
                                  'Solo derechos naturales'],
                 'correcta': 'B'},
                {'pregunta': 'El concepto de persona se amplió con el tiempo '
                             'para comprender a:',
                 'alternativas': ['Solo a los nobles',
                                  'Todo ser humano',
                                  'Solo a los ciudadanos',
                                  'Solo a los adultos',
                                  'Solo a los varones'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad y la persona se relacionan porque '
                             'el individuo:',
                 'alternativas': ['Existe independientemente de la sociedad',
                                  'Se desarrolla y realiza en el marco de la '
                                  'vida social',
                                  'No requiere de otros',
                                  'Es anterior a toda organización social',
                                  'Rechaza las normas colectivas'],
                 'correcta': 'B'}]},
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
                           'de los hijos y su patrimonio.']}],
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
                                  'Natural',
                                  'Contractual',
                                  'Religioso',
                                  'Administrativo'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo de la Constitución peruana que '
                             'reconoce a la familia como instituto natural y '
                             'fundamental es el:',
                 'alternativas': ['Artículo 2',
                                  'Artículo 4',
                                  'Artículo 10',
                                  'Artículo 16',
                                  'Artículo 20'],
                 'correcta': 'B'},
                {'pregunta': 'Según Aguilar Llanos, las familias peruanas se '
                             'originan:',
                 'alternativas': ['Solo en el matrimonio civil',
                                  'También en las uniones de hecho, además '
                                  'del matrimonio',
                                  'Únicamente por adopción',
                                  'Solo por vínculo religioso',
                                  'Exclusivamente por vínculo consanguíneo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Tribunal Constitucional, la familia '
                             'se encarga también de transmitir:',
                 'alternativas': ['Solo bienes materiales',
                                  'Valores éticos, cívicos y culturales',
                                  'Solo el apellido',
                                  'Únicamente el idioma',
                                  'Solo tradiciones religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'La persona a quien reconocen como ascendiente '
                             'común varios parientes se llama:',
                 'alternativas': ['Grado',
                                  'Línea',
                                  'Tronco',
                                  'Vínculo',
                                  'Parentesco'],
                 'correcta': 'C'},
                {'pregunta': 'La distancia entre dos parientes se denomina:',
                 'alternativas': ['Tronco', 'Línea', 'Grado', 'Rama', 'Nexo'],
                 'correcta': 'C'},
                {'pregunta': 'La línea que se forma con personas que '
                             'descienden unas de otras es la línea:',
                 'alternativas': ['Colateral',
                                  'Recta',
                                  'Espiritual',
                                  'Transversal',
                                  'Horizontal'],
                 'correcta': 'B'},
                {'pregunta': 'La línea colateral también se conoce como:',
                 'alternativas': ['Ascendente',
                                  'Horizontal o transversal',
                                  'Descendente',
                                  'Directa',
                                  'Consanguínea pura'],
                 'correcta': 'B'},
                {'pregunta': 'Para efectos civiles, en la línea colateral se '
                             'considera hasta el:',
                 'alternativas': ['Segundo grado',
                                  'Tercer grado',
                                  'Cuarto grado',
                                  'Quinto grado',
                                  'Sexto grado'],
                 'correcta': 'C'},
                {'pregunta': 'El parentesco espiritual se establece, por '
                             'ejemplo, con motivo de:',
                 'alternativas': ['Un contrato comercial',
                                  'Un sacramento como el bautismo',
                                  'Una compraventa',
                                  'Un préstamo',
                                  'Un testamento'],
                 'correcta': 'B'},
                {'pregunta': 'La adopción está regulada en el artículo del '
                             'Código Civil número:',
                 'alternativas': ['118', '238', '418', '618', '818'],
                 'correcta': 'B'},
                {'pregunta': 'Mediante la adopción, el adoptado asume los '
                             'derechos y obligaciones de un:',
                 'alternativas': ['Tutor',
                                  'Hijo matrimonial',
                                  'Curador',
                                  'Padrino',
                                  'Apoderado'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «patria potestad» alude al '
                             '«pater familia» y a la:',
                 'alternativas': ['Herencia',
                                  'Potestad o dominio',
                                  'Adopción',
                                  'Tutela',
                                  'Curatela'],
                 'correcta': 'B'},
                {'pregunta': 'La patria potestad está regulada en el '
                             'artículo del Código Civil número:',
                 'alternativas': ['118', '238', '418', '518', '618'],
                 'correcta': 'C'},
                {'pregunta': 'Durante el matrimonio, la patria potestad se '
                             'ejerce:',
                 'alternativas': ['Solo por el padre',
                                  'Solo por la madre',
                                  'Conjuntamente por el padre y la madre',
                                  'Por los abuelos',
                                  'Por el Estado'],
                 'correcta': 'C'},
                {'pregunta': 'En caso de divorcio, la patria potestad la '
                             'ejerce:',
                 'alternativas': ['Siempre el padre',
                                  'Siempre la madre',
                                  'El cónyuge a quien se confían los hijos',
                                  'Los abuelos paternos',
                                  'El Poder Judicial directamente'],
                 'correcta': 'C'},
                {'pregunta': 'Quien cuida a un menor sin ser su progenitor '
                             'actúa a título de:',
                 'alternativas': ['Padre biológico',
                                  'Tutor',
                                  'Adoptante',
                                  'Curador exclusivo',
                                  'Padrino'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad de la patria potestad es de '
                             'carácter:',
                 'alternativas': ['Punitivo',
                                  'Tuitivo, de protección y defensa',
                                  'Económico exclusivamente',
                                  'Simbólico',
                                  'Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'Según Cussiánovich, la familia debe garantizar '
                             'al ser humano recién nacido:',
                 'alternativas': ['Solo alimentación',
                                  'Sobrevivencia física, emocional y '
                                  'afectiva',
                                  'Solo educación formal',
                                  'Solo protección legal',
                                  'Solo un nombre'],
                 'correcta': 'B'},
                {'pregunta': 'La patria potestad NO alcanza a:',
                 'alternativas': ['Los padres',
                                  'Los ascendientes ni parientes colaterales',
                                  'Los hijos menores',
                                  'Los hijos adoptivos',
                                  'Los cónyuges'],
                 'correcta': 'B'}]},
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
                {'titulo': '5.4 PATRIMONIO CULTURAL Y NATURAL',
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
                 'alternativas': ['Territorio',
                                  'Nacimiento o raza',
                                  'Gobierno',
                                  'Idioma',
                                  'Cultura'],
                 'correcta': 'B'},
                {'pregunta': 'Para Herder y Fichte, compartir elementos como '
                             'etnia y folclore expresa:',
                 'alternativas': ['Un contrato social',
                                  'Un alma colectiva',
                                  'Una obligación legal',
                                  'Un acuerdo político',
                                  'Una decisión estatal'],
                 'correcta': 'B'},
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
                 'alternativas': ['El idioma',
                                  'La conciencia nacional',
                                  'La religión',
                                  'El territorio',
                                  'La raza'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio, la raza, la religión y el '
                             'idioma son elementos de la nación '
                             'considerados:',
                 'alternativas': ['Esenciales',
                                  'Secundarios',
                                  'Únicos',
                                  'Legales',
                                  'Constitucionales'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'define quiénes son peruanos por nacimiento es '
                             'el:',
                 'alternativas': ['Artículo 2',
                                  'Artículo 52',
                                  'Artículo 4',
                                  'Artículo 100',
                                  'Artículo 200'],
                 'correcta': 'B'},
                {'pregunta': 'Son peruanos por nacimiento los nacidos en el '
                             'exterior de padre o madre peruanos si:',
                 'alternativas': ['Nunca pueden ser peruanos',
                                  'Son inscritos en el registro '
                                  'correspondiente durante su minoría de '
                                  'edad',
                                  'Solo si nacen en un país de habla hispana',
                                  'Solo si regresan al Perú antes de los 5 '
                                  'años',
                                  'Automáticamente sin ningún trámite'],
                 'correcta': 'B'},
                {'pregunta': 'La Ley de Nacionalidad del Perú lleva el '
                             'número:',
                 'alternativas': ['Ley N° 26300',
                                  'Ley N° 26574',
                                  'Ley N° 27444',
                                  'Ley N° 30220',
                                  'Ley N° 28044'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Ley de Nacionalidad, un peruano que '
                             'adopta otra nacionalidad:',
                 'alternativas': ['Pierde automáticamente la peruana',
                                  'No pierde la peruana, salvo renuncia '
                                  'expresa',
                                  'Debe elegir una sola desde el nacimiento',
                                  'Pierde sus derechos civiles',
                                  'Debe pagar una multa'],
                 'correcta': 'B'},
                {'pregunta': 'Para renunciar a la nacionalidad peruana es '
                             'necesario:',
                 'alternativas': ['Ser menor de edad',
                                  'Ser mayor de edad y suscribir escritura '
                                  'pública',
                                  'Solo presentar el DNI',
                                  'Pedir autorización de los padres',
                                  'Ninguna formalidad especial'],
                 'correcta': 'B'},
                {'pregunta': 'Los padres pueden renunciar a la nacionalidad '
                             'peruana en nombre de sus hijos menores:',
                 'alternativas': ['Sí, siempre',
                                  'No, solo los mayores de edad pueden '
                                  'renunciar',
                                  'Solo con autorización judicial',
                                  'Solo si el hijo lo solicita',
                                  'Solo en casos excepcionales'],
                 'correcta': 'B'},
                {'pregunta': 'La identidad nacional se define como:',
                 'alternativas': ['Una obligación legal',
                                  'El sentimiento subjetivo de pertenecer a '
                                  'una nación concreta',
                                  'Un documento oficial',
                                  'Una condición económica',
                                  'Un requisito para votar'],
                 'correcta': 'B'},
                {'pregunta': 'El término «peruanidad» fue acuñado por:',
                 'alternativas': ['José Carlos Mariátegui',
                                  'Víctor Andrés Belaunde García',
                                  'Jorge Basadre',
                                  'Raúl Porras Barrenechea',
                                  'Manuel González Prada'],
                 'correcta': 'B'},
                {'pregunta': 'La peruanidad se define como el sentimiento '
                             'que vincula a los pueblos del Perú con:',
                 'alternativas': ['Solo su gobierno actual',
                                  'Sus tradiciones y la fe en su futuro',
                                  'Solo su territorio físico',
                                  'Solo su economía',
                                  'Solo su idioma oficial'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los aspectos que fundamentan la '
                             'peruanidad figura la etapa de cultura:',
                 'alternativas': ['Colonial únicamente',
                                  'Prehispánica',
                                  'Solo republicana',
                                  'Solo contemporánea',
                                  'Exclusivamente virreinal'],
                 'correcta': 'B'},
                {'pregunta': 'La nacionalidad se adquiere, además del '
                             'nacimiento, por naturalización o:',
                 'alternativas': ['Matrimonio exclusivamente',
                                  'Opción, con residencia en el Perú',
                                  'Solo por herencia',
                                  'Solo por decisión judicial',
                                  'Solo por concurso público'],
                 'correcta': 'B'},
                {'pregunta': 'Las personas con doble nacionalidad ejercen '
                             'los derechos y obligaciones:',
                 'alternativas': ['De ambos países simultáneamente sin '
                                  'distinción',
                                  'Del país donde domicilian y cuya '
                                  'nacionalidad poseen',
                                  'Solo del Perú',
                                  'Solo del país extranjero',
                                  'Ninguno de los dos'],
                 'correcta': 'B'},
                {'pregunta': 'La doble nacionalidad confiere a los '
                             'extranjeros naturalizados:',
                 'alternativas': ['Los mismos derechos privativos de los '
                                  'peruanos por nacimiento',
                                  'Ningún derecho privativo de los peruanos '
                                  'por nacimiento',
                                  'Derechos superiores a los nacionales',
                                  'Automática ciudadanía plena',
                                  'Exoneración total de impuestos'],
                 'correcta': 'B'},
                {'pregunta': 'La nación, para Herder y Fichte, se sustenta '
                             'principalmente en:',
                 'alternativas': ['Un tratado internacional',
                                  'Elementos compartidos como etnia, '
                                  'folclore y cultura',
                                  'Solo la Constitución vigente',
                                  'Solo las fronteras políticas',
                                  'Solo el sistema económico'],
                 'correcta': 'B'},
                {'pregunta': 'El renunciante a la nacionalidad peruana que '
                             'vive en el exterior lo hace ante:',
                 'alternativas': ['Un notario extranjero únicamente',
                                  'El funcionario consular',
                                  'La embajada de otro país',
                                  'Las Naciones Unidas',
                                  'Un juez peruano en el extranjero'],
                 'correcta': 'B'}]}]


# ================================================================
# INTERFAZ
# ================================================================

def _tema_completo_civica(preguntas=False):
    """Fusiona todas las balotas cargadas en un solo documento imprimible."""
    secs, cuadros, pregs = [], [], []
    for t in BALOTAS_CIVICA:
        for s in t.get("secciones", []):
            secs.append({"titulo": f"B{t['num']}. {s['titulo']}",
                         "items": s["items"]})
        for c in t.get("cuadros", []):
            cuadros.append({"titulo": f"B{t['num']}. {c['titulo']}",
                            "encabezados": c["encabezados"],
                            "filas": c["filas"]})
        if preguntas:
            for p in balancear(t["preguntas"]):
                pregs.append({**p,
                              "pregunta": f"(B{t['num']}) {p['pregunta']}"})
    return {"num": f"1–{len(BALOTAS_CIVICA)}",
            "titulo": "TEMARIO DE EDUCACIÓN CÍVICA",
            "secciones": secs, "cuadros": cuadros, "preguntas": pregs}


def tab_fichas_civica(config=None):
    st.subheader("⚖️ Educación Cívica — Fichas y banco de preguntas (CEPRU)")
    st.caption("Temario oficial de Educación Cívica, Área D "
               f"— {len(BALOTAS_CIVICA)} de 18 balotas cargadas por ahora. "
               "Cada una genera cuatro documentos.")

    opciones = {f"Balota {t['num']} — {t['titulo']}": t for t in BALOTAS_CIVICA}
    sel = st.selectbox("Balota:", list(opciones.keys()), key="fc_sel")
    tema = opciones[sel]

    c1, c2, c3 = st.columns(3)
    c1.metric("Espacios para completar", contar_espacios(tema))
    c2.metric("Preguntas", len(tema["preguntas"]))
    c3.metric("Cuadros", len(tema.get("cuadros", [])))

    grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                              placeholder="GRUPO CD", key="fc_grado")

    st.markdown("##### Descargar")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt, area="Educación Cívica"),
                file_name=f"civica_balota{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fc_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt, area="Educación Cívica"),
                file_name=f"civica_balota{tema['num']}_docente.pdf",
                mime="application/pdf", use_container_width=True, key="fc_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de 20 preguntas**")
        try:
            tema_b = {**tema, "preguntas": balancear(tema["preguntas"])}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt, area="Educación Cívica"),
                file_name=f"civica_preguntas{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fc_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt, area="Educación Cívica"),
                file_name=f"civica_preguntas{tema['num']}_claves.pdf",
                mime="application/pdf", use_container_width=True, key="fc_pd")
        except Exception as e:
            st.error(f"No se pudo generar el banco: {e}")

    st.markdown("---")
    st.markdown("##### Descargar el temario completo (balotas cargadas)")
    g1, g2 = st.columns(2)
    with g1:
        if st.button("📚 Todas las fichas cargadas",
                     use_container_width=True, key="fc_todas_f"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["fc_pdf"] = generar_ficha_texto(
                        _tema_completo_civica(), False, grado_txt,
                        area="Educación Cívica")
                    st.session_state["fc_nom"] = "civica_fichas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")
    with g2:
        if st.button("📚 Todos los bancos cargados",
                     use_container_width=True, key="fc_todas_p"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["fc_pdf"] = generar_banco_preguntas(
                        _tema_completo_civica(preguntas=True), False, grado_txt,
                        area="Educación Cívica")
                    st.session_state["fc_nom"] = "civica_preguntas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.get("fc_pdf"):
        st.download_button(
            "⬇️ Descargar documento completo",
            data=st.session_state["fc_pdf"],
            file_name=st.session_state.get("fc_nom", "civica.pdf"),
            mime="application/pdf", use_container_width=True, key="fc_dl")

    with st.expander("Ver el contenido de esta balota"):
        for sec in tema["secciones"]:
            st.markdown(f"**{sec['titulo']}**")
            for it in sec["items"]:
                st.markdown("- " + _PATRON.sub(r"**\1**", it))
        for cu in tema.get("cuadros", []):
            st.markdown(f"**{cu['titulo']}**")
            for fila in cu["filas"]:
                st.markdown(" | ".join(_PATRON.sub(r"**\1**", c) for c in fila))
        st.markdown("**Primeras cinco preguntas:**")
        for i, p in enumerate(tema["preguntas"][:5], start=1):
            st.markdown(f"{i}. {p['pregunta']}")
            for k, a in enumerate(p["alternativas"]):
                marca = " ✅" if LETRAS[k] == p["correcta"] else ""
                st.markdown(f"   {LETRAS[k]}) {a}{marca}")
