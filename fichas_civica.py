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
                 'alternativas': ['Ethos', 'Lex', 'Mores', 'Directum', 'Ius'],
                 'correcta': 'E'},
                {'pregunta': 'El vocablo latino «Directum», aplicado tras el '
                             'Corpus Iuris Civilis, significa:',
                 'alternativas': ['Recto, conforme a la norma',
                                  'Autoridad',
                                  'Sanción',
                                  'Costumbre',
                                  'Justicia'],
                 'correcta': 'A'},
                {'pregunta': 'Para Mario Alzamora Valdez, el Derecho es la '
                             'regulación de la vida social del hombre para '
                             'alcanzar:',
                 'alternativas': ['La libertad',
                                  'El orden',
                                  'La igualdad',
                                  'La justicia',
                                  'La paz social'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de normas jurídicas que forman el '
                             'ordenamiento vigente (Constitución, leyes, '
                             'códigos) corresponde al Derecho:',
                 'alternativas': ['Consuetudinario',
                                  'Subjetivo',
                                  'Natural',
                                  'Positivo',
                                  'Objetivo'],
                 'correcta': 'E'},
                {'pregunta': 'El derecho a la vida, a la libertad o a la '
                             'propiedad son ejemplos del Derecho:',
                 'alternativas': ['Comparado',
                                  'Objetivo',
                                  'Público',
                                  'Consuetudinario',
                                  'Subjetivo'],
                 'correcta': 'E'},
                {'pregunta': 'En el derecho subjetivo, la persona sobre la '
                             'cual recae un deber correlativo es el:',
                 'alternativas': ['Titular del derecho',
                                  'Objeto del derecho',
                                  'Sujeto pasivo',
                                  'Sujeto activo',
                                  'Legislador'],
                 'correcta': 'C'},
                {'pregunta': 'Las fuentes que hacen referencia a los '
                             'orígenes mediatos de la norma jurídica '
                             '(factores sociales, económicos y culturales) '
                             'se denominan:',
                 'alternativas': ['Formales',
                                  'Jurisprudenciales',
                                  'Materiales o reales',
                                  'Consuetudinarias',
                                  'Doctrinarias'],
                 'correcta': 'C'},
                {'pregunta': 'La forma de conducta implantada por una '
                             'colectividad, repetida de manera uniforme y '
                             'permanente, cuya observancia se hace '
                             'obligatoria, es:',
                 'alternativas': ['La equidad',
                                  'La jurisprudencia',
                                  'La costumbre',
                                  'La ley',
                                  'La doctrina'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de resoluciones emitidas por la '
                             'Corte Suprema y el Tribunal Constitucional '
                             'sobre una cuestión determinada constituye:',
                 'alternativas': ['La jurisprudencia',
                                  'La doctrina',
                                  'Los principios generales',
                                  'La ley',
                                  'La costumbre'],
                 'correcta': 'A'},
                {'pregunta': 'Los estudios especializados del derecho, que '
                             'dan lugar a escuelas y teorías jurídicas pero '
                             'carecen de fuerza legal obligatoria, '
                             'constituyen:',
                 'alternativas': ['La casuística',
                                  'La costumbre',
                                  'La jurisprudencia',
                                  'La doctrina',
                                  'La ley'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 139 de la Constitución '
                             'vigente, los principios generales del derecho '
                             'tienen:',
                 'alternativas': ['Aplicación exclusiva penal',
                                  'Carácter consuetudinario',
                                  'Fuerza de ley',
                                  'Solo valor referencial',
                                  'Valor supletorio únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'Que una ley deba ser cumplida por todos los '
                             'que están en el territorio donde rige, incluso '
                             'en contra de su voluntad, corresponde a su '
                             'carácter:',
                 'alternativas': ['Impersonal',
                                  'Permanente',
                                  'Coercitivo',
                                  'Obligatorio',
                                  'Abstracto'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ley se aplique a un grupo indeterminado '
                             'de sujetos y no a una sola persona corresponde '
                             'a su carácter:',
                 'alternativas': ['Irretroactivo',
                                  'Impersonal',
                                  'General',
                                  'Permanente',
                                  'Coercitivo'],
                 'correcta': 'B'},
                {'pregunta': 'Que una ley regule hechos posteriores a su '
                             'sanción y no rija sobre conductas anteriores '
                             'corresponde a su carácter:',
                 'alternativas': ['Coercitivo',
                                  'Abstracto',
                                  'Impersonal',
                                  'Permanente',
                                  'Irretroactivo'],
                 'correcta': 'E'},
                {'pregunta': 'Que el incumplimiento de la ley implique la '
                             'imposición de una pena o castigo corresponde a '
                             'su carácter:',
                 'alternativas': ['Abstracto',
                                  'Coercitivo',
                                  'Permanente',
                                  'General',
                                  'Impersonal'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, la palabra «Moral» proviene '
                             'del latín «mores», que significa:',
                 'alternativas': ['Ley',
                                  'Justicia',
                                  'Costumbre',
                                  'Deber',
                                  'Virtud'],
                 'correcta': 'C'},
                {'pregunta': 'Respecto de su ámbito, la Moral es interior y '
                             'el Derecho es:',
                 'alternativas': ['Heterónomo',
                                  'Autónomo',
                                  'Exterior',
                                  'Bilateral',
                                  'Coercible'],
                 'correcta': 'C'},
                {'pregunta': 'Que la Moral solo imponga deberes cuyo '
                             'cumplimiento no genera ningún derecho, a '
                             'diferencia del Derecho que concede facultades '
                             'y señala deberes, corresponde a la diferencia '
                             'por su(s):',
                 'alternativas': ['Ámbito',
                                  'Fuerza',
                                  'Origen',
                                  'Efectos',
                                  'Campo de acción'],
                 'correcta': 'D'},
                {'pregunta': 'Que la Moral surja espontáneamente por '
                             'decisión personal y sea renunciable, mientras '
                             'que el Derecho emane de un poder extraño de '
                             'cumplimiento ineludible, corresponde a la '
                             'diferencia por su:',
                 'alternativas': ['Ámbito',
                                  'Efecto',
                                  'Campo de acción',
                                  'Fuerza',
                                  'Origen'],
                 'correcta': 'E'},
                {'pregunta': 'Que la Moral sea incoercible (sin fuerza que '
                             'obligue su cumplimiento) y el Derecho sea '
                             'coercible (con poder coercitivo que exige su '
                             'cumplimiento) corresponde a la diferencia por '
                             'su:',
                 'alternativas': ['Efecto',
                                  'Fuerza',
                                  'Ámbito',
                                  'Origen',
                                  'Campo de acción'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Axiología',
                                  'Estética',
                                  'Gnoseología',
                                  'Ontología',
                                  'Lógica'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, «justicia» proviene de la '
                             'voz latina:',
                 'alternativas': ['Solidus',
                                  'Iustitia',
                                  'Honestitad',
                                  'Dignitas',
                                  'Veritas'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia que busca el bien de la sociedad '
                             'entera se llama:',
                 'alternativas': ['Conmutativa',
                                  'Judicial',
                                  'Distributiva',
                                  'General',
                                  'Particular'],
                 'correcta': 'D'},
                {'pregunta': 'La justicia aplicada por un juez al emitir '
                             'sentencia se denomina:',
                 'alternativas': ['General',
                                  'Particular',
                                  'Social',
                                  'Judicial',
                                  'Conmutativa'],
                 'correcta': 'D'},
                {'pregunta': 'La forma clásica de justicia, entre individuos '
                             'como pares independientes, es la:',
                 'alternativas': ['Particular',
                                  'Conmutativa',
                                  'Distributiva',
                                  'Social',
                                  'General'],
                 'correcta': 'B'},
                {'pregunta': 'La justicia que considera al individuo frente '
                             'al todo social es la:',
                 'alternativas': ['Judicial',
                                  'Conmutativa',
                                  'Particular',
                                  'Distributiva',
                                  'General'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «solidaridad» proviene del latín '
                             '«solidus», que significa:',
                 'alternativas': ['Fraternidad',
                                  'Ayuda',
                                  'Unión',
                                  'Colaboración',
                                  'Sólido, firme, compacto'],
                 'correcta': 'E'},
                {'pregunta': 'La honestidad se define principalmente como el '
                             'respeto a:',
                 'alternativas': ['La autoridad',
                                  'La ley',
                                  'La costumbre',
                                  'La verdad',
                                  'La religión'],
                 'correcta': 'D'},
                {'pregunta': 'La dignidad humana depende de:',
                 'alternativas': ['La raza y el sexo',
                                  'La nacionalidad',
                                  'La condición social',
                                  'Ningún condicionamiento externo, es '
                                  'inherente al ser humano',
                                  'El nivel educativo'],
                 'correcta': 'D'},
                {'pregunta': 'La libertad se define como la capacidad de la '
                             'persona de:',
                 'alternativas': ['Seguir la mayoría',
                                  'Obedecer las normas',
                                  'Depender de otros',
                                  'Evitar responsabilidades',
                                  'Autodeterminarse y actuar según su '
                                  'voluntad'],
                 'correcta': 'E'},
                {'pregunta': 'La solidaridad se practica sin distinción de:',
                 'alternativas': ['Solo religión',
                                  'Solo nacionalidad',
                                  'Credo, sexo, raza o afiliación política',
                                  'Solo edad',
                                  'Solo género'],
                 'correcta': 'C'},
                {'pregunta': 'Los valores representan, en síntesis:',
                 'alternativas': ['Tradiciones familiares',
                                  'Normas legales obligatorias',
                                  'Reglas religiosas',
                                  'Lo mejor que la vida humana puede ofrecer',
                                  'Costumbres regionales'],
                 'correcta': 'D'},
                {'pregunta': 'Adicionalmente a la Filosofía, estudian los '
                             'valores de forma aplicada:',
                 'alternativas': ['Solo la Medicina',
                                  'Solo la Biología',
                                  'La Astronomía',
                                  'La Sociología, la Economía y la Política',
                                  'La Física'],
                 'correcta': 'D'},
                {'pregunta': 'La igualdad implica que todas las personas '
                             'tienen ante la ley:',
                 'alternativas': ['Privilegios especiales',
                                  'Ninguna garantía',
                                  'Derechos según su edad',
                                  'Los mismos derechos y oportunidades',
                                  'Distintos derechos según su riqueza'],
                 'correcta': 'D'},
                {'pregunta': 'El respeto se define como el reconocimiento '
                             'de:',
                 'alternativas': ['Las normas de tránsito',
                                  'El valor propio y los derechos de los '
                                  'demás',
                                  'Los símbolos patrios',
                                  'Solo la autoridad estatal',
                                  'Las tradiciones religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'En la antigua Grecia, el concepto de valores '
                             'se trataba:',
                 'alternativas': ['Como algo general y sin divisiones',
                                  'Exclusivamente en la política',
                                  'Solo entre filósofos estoicos',
                                  'Solo en el ámbito religioso',
                                  'De forma muy especializada por '
                                  'disciplinas'],
                 'correcta': 'A'},
                {'pregunta': 'La justicia social comprende:',
                 'alternativas': ['Solo acuerdos económicos',
                                  'El conjunto de decisiones, normas y '
                                  'principios razonables de una organización '
                                  'social',
                                  'Solo normas religiosas',
                                  'Únicamente leyes penales',
                                  'Solo decisiones judiciales'],
                 'correcta': 'B'},
                {'pregunta': 'Tener valores se relaciona directamente con:',
                 'alternativas': ['Evitar el trabajo',
                                  'Ganar poder político',
                                  'Respetar a los demás',
                                  'Acumular riqueza',
                                  'Buscar fama'],
                 'correcta': 'C'},
                {'pregunta': 'La honestidad, en su sentido más evidente, '
                             'implica coherencia entre:',
                 'alternativas': ['La riqueza y el estatus',
                                  'El poder y la autoridad',
                                  'La edad y la experiencia',
                                  'El pensamiento y la apariencia',
                                  'El comportamiento, la expresión y la '
                                  'verdad'],
                 'correcta': 'E'},
                {'pregunta': 'La dignidad, según la distinción de '
                             'Millán-Puelles, puede ser ontológica o:',
                 'alternativas': ['Política',
                                  'Adquirida',
                                  'Legal',
                                  'Social',
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
                                  'El Libro IV',
                                  'El Libro III',
                                  'La Constitución'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, la palabra «persona» '
                             'originalmente designaba:',
                 'alternativas': ['Un cargo político',
                                  'Una ceremonia religiosa',
                                  'Un documento legal',
                                  'La máscara usada por los actores de '
                                  'teatro',
                                  'Un título nobiliario'],
                 'correcta': 'D'},
                {'pregunta': 'Según Aníbal Torres Vásquez, la existencia de '
                             'la persona natural comienza con:',
                 'alternativas': ['El bautizo',
                                  'El nacimiento',
                                  'La concepción',
                                  'Los 18 años',
                                  'El registro civil'],
                 'correcta': 'C'},
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
                 'alternativas': ['Solo social',
                                  'Solo física',
                                  'Solo espiritual',
                                  'Psicosomática',
                                  'Únicamente legal'],
                 'correcta': 'D'},
                {'pregunta': 'El Libro I del Código Civil se divide en '
                             'cuántas secciones:',
                 'alternativas': ['Cinco', 'Seis', 'Tres', 'Dos', 'Cuatro'],
                 'correcta': 'E'},
                {'pregunta': 'Las comunidades campesinas y nativas se '
                             'regulan dentro de:',
                 'alternativas': ['La ley de municipalidades',
                                  'El derecho laboral',
                                  'El derecho tributario',
                                  'El derecho penal',
                                  'El Libro I del Código Civil'],
                 'correcta': 'E'},
                {'pregunta': 'La persona puede definirse también como un '
                             'sujeto:',
                 'alternativas': ['Solo con derechos',
                                  'Sin capacidad legal',
                                  'Exclusivamente económico',
                                  'Sin obligaciones',
                                  'Consciente y racional, titular de '
                                  'derechos y obligaciones'],
                 'correcta': 'E'},
                {'pregunta': 'El ser humano es considerado un ser social '
                             'porque:',
                 'alternativas': ['Prefiere la soledad',
                                  'No necesita normas',
                                  'Se realiza plenamente en convivencia con '
                                  'otros',
                                  'Vive completamente aislado',
                                  'Depende solo de sí mismo'],
                 'correcta': 'C'},
                {'pregunta': 'Las personas jurídicas se diferencian de las '
                             'personas naturales en que:',
                 'alternativas': ['Solo existen en el derecho penal',
                                  'Son siempre empresas',
                                  'Son entidades con personería legal '
                                  'distinta a un individuo',
                                  'No tienen derechos',
                                  'No tienen personería legal'],
                 'correcta': 'C'},
                {'pregunta': 'La sociedad se define como el conjunto de '
                             'personas que comparten:',
                 'alternativas': ['Solo una religión',
                                  'Solo un idioma',
                                  'Solo un territorio',
                                  'Solo una economía',
                                  'Cultura, normas e instituciones comunes'],
                 'correcta': 'E'},
                {'pregunta': 'El «Derecho de las personas» regula el '
                             'reconocimiento de:',
                 'alternativas': ['Los derechos fundamentales de la persona',
                                  'Solo derechos políticos',
                                  'Solo derechos patrimoniales',
                                  'Solo obligaciones tributarias',
                                  'Solo derechos laborales'],
                 'correcta': 'A'},
                {'pregunta': 'En la Edad Media, el término «persona» se usó '
                             'como sinónimo de:',
                 'alternativas': ['Campesino',
                                  'Esclavo',
                                  'Comerciante',
                                  'Portador de dignidades',
                                  'Soldado'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra persona es considerada, según el '
                             'texto, equívoca y:',
                 'alternativas': ['Polisémica',
                                  'Unívoca',
                                  'Simple',
                                  'Restringida',
                                  'Exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Las asociaciones, fundaciones y comités NO '
                             'inscritos se regulan en:',
                 'alternativas': ['El Libro I del Código Civil, tercera '
                                  'sección',
                                  'La Constitución exclusivamente',
                                  'Ninguna norma',
                                  'El derecho internacional',
                                  'El derecho penal'],
                 'correcta': 'A'},
                {'pregunta': 'El estudio antropológico revela que el hombre '
                             'es un ser:',
                 'alternativas': ['Cerrado y limitado',
                                  'Determinado biológicamente',
                                  'Puramente material',
                                  'Sin capacidad de trascender',
                                  'Abierto al infinito'],
                 'correcta': 'E'},
                {'pregunta': 'La unidad psicosomática de la persona implica '
                             'que lo que afecta al cuerpo:',
                 'alternativas': ['Repercute también en la psique, y '
                                  'viceversa',
                                  'Es independiente de la mente',
                                  'No tiene relación con las emociones',
                                  'No afecta a la psique',
                                  'Solo afecta la salud física'],
                 'correcta': 'A'},
                {'pregunta': 'La persona jurídica se distingue por tener:',
                 'alternativas': ['Capacidad física',
                                  'Solo derechos naturales',
                                  'Solo obligaciones morales',
                                  'Existencia biológica',
                                  'Personería legal reconocida'],
                 'correcta': 'E'},
                {'pregunta': 'El concepto de persona se amplió con el tiempo '
                             'para comprender a:',
                 'alternativas': ['Solo a los varones',
                                  'Solo a los nobles',
                                  'Solo a los adultos',
                                  'Todo ser humano',
                                  'Solo a los ciudadanos'],
                 'correcta': 'D'},
                {'pregunta': 'La sociedad y la persona se relacionan porque '
                             'el individuo:',
                 'alternativas': ['Es anterior a toda organización social',
                                  'Se desarrolla y realiza en el marco de la '
                                  'vida social',
                                  'Existe independientemente de la sociedad',
                                  'Rechaza las normas colectivas',
                                  'No requiere de otros'],
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
                                  'Religioso',
                                  'Administrativo',
                                  'Legal',
                                  'Natural'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución peruana que '
                             'reconoce a la familia como instituto natural y '
                             'fundamental es el:',
                 'alternativas': ['Artículo 10',
                                  'Artículo 20',
                                  'Artículo 16',
                                  'Artículo 2',
                                  'Artículo 4'],
                 'correcta': 'E'},
                {'pregunta': 'Según Aguilar Llanos, las familias peruanas se '
                             'originan:',
                 'alternativas': ['Exclusivamente por vínculo consanguíneo',
                                  'También en las uniones de hecho, además '
                                  'del matrimonio',
                                  'Solo en el matrimonio civil',
                                  'Únicamente por adopción',
                                  'Solo por vínculo religioso'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Tribunal Constitucional, la familia '
                             'se encarga también de transmitir:',
                 'alternativas': ['Únicamente el idioma',
                                  'Solo tradiciones religiosas',
                                  'Solo bienes materiales',
                                  'Solo el apellido',
                                  'Valores éticos, cívicos y culturales'],
                 'correcta': 'E'},
                {'pregunta': 'La persona a quien reconocen como ascendiente '
                             'común varios parientes se llama:',
                 'alternativas': ['Parentesco',
                                  'Línea',
                                  'Tronco',
                                  'Vínculo',
                                  'Grado'],
                 'correcta': 'C'},
                {'pregunta': 'La distancia entre dos parientes se denomina:',
                 'alternativas': ['Rama', 'Grado', 'Nexo', 'Línea', 'Tronco'],
                 'correcta': 'B'},
                {'pregunta': 'La línea que se forma con personas que '
                             'descienden unas de otras es la línea:',
                 'alternativas': ['Transversal',
                                  'Horizontal',
                                  'Espiritual',
                                  'Recta',
                                  'Colateral'],
                 'correcta': 'D'},
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
                                  'Segundo grado',
                                  'Sexto grado',
                                  'Cuarto grado',
                                  'Tercer grado'],
                 'correcta': 'D'},
                {'pregunta': 'El parentesco espiritual se establece, por '
                             'ejemplo, con motivo de:',
                 'alternativas': ['Un préstamo',
                                  'Un testamento',
                                  'Una compraventa',
                                  'Un contrato comercial',
                                  'Un sacramento como el bautismo'],
                 'correcta': 'E'},
                {'pregunta': 'La adopción está regulada en el artículo del '
                             'Código Civil número:',
                 'alternativas': ['238', '618', '118', '418', '818'],
                 'correcta': 'A'},
                {'pregunta': 'Mediante la adopción, el adoptado asume los '
                             'derechos y obligaciones de un:',
                 'alternativas': ['Apoderado',
                                  'Tutor',
                                  'Padrino',
                                  'Curador',
                                  'Hijo matrimonial'],
                 'correcta': 'E'},
                {'pregunta': 'Etimológicamente, «patria potestad» alude al '
                             '«pater familia» y a la:',
                 'alternativas': ['Tutela',
                                  'Herencia',
                                  'Curatela',
                                  'Potestad o dominio',
                                  'Adopción'],
                 'correcta': 'D'},
                {'pregunta': 'La patria potestad está regulada en el '
                             'artículo del Código Civil número:',
                 'alternativas': ['118', '518', '238', '418', '618'],
                 'correcta': 'D'},
                {'pregunta': 'Durante el matrimonio, la patria potestad se '
                             'ejerce:',
                 'alternativas': ['Solo por la madre',
                                  'Conjuntamente por el padre y la madre',
                                  'Solo por el padre',
                                  'Por el Estado',
                                  'Por los abuelos'],
                 'correcta': 'B'},
                {'pregunta': 'En caso de divorcio, la patria potestad la '
                             'ejerce:',
                 'alternativas': ['El cónyuge a quien se confían los hijos',
                                  'Siempre el padre',
                                  'Los abuelos paternos',
                                  'Siempre la madre',
                                  'El Poder Judicial directamente'],
                 'correcta': 'A'},
                {'pregunta': 'Quien cuida a un menor sin ser su progenitor '
                             'actúa a título de:',
                 'alternativas': ['Padre biológico',
                                  'Curador exclusivo',
                                  'Padrino',
                                  'Tutor',
                                  'Adoptante'],
                 'correcta': 'D'},
                {'pregunta': 'La finalidad de la patria potestad es de '
                             'carácter:',
                 'alternativas': ['Punitivo',
                                  'Simbólico',
                                  'Económico exclusivamente',
                                  'Religioso',
                                  'Tuitivo, de protección y defensa'],
                 'correcta': 'E'},
                {'pregunta': 'Según Cussiánovich, la familia debe garantizar '
                             'al ser humano recién nacido:',
                 'alternativas': ['Sobrevivencia física, emocional y '
                                  'afectiva',
                                  'Solo educación formal',
                                  'Solo alimentación',
                                  'Solo un nombre',
                                  'Solo protección legal'],
                 'correcta': 'A'},
                {'pregunta': 'La patria potestad NO alcanza a:',
                 'alternativas': ['Los padres',
                                  'Los cónyuges',
                                  'Los hijos menores',
                                  'Los hijos adoptivos',
                                  'Los ascendientes ni parientes '
                                  'colaterales'],
                 'correcta': 'E'},
                {'pregunta': 'La institución que protege a los menores de '
                             'edad que no tienen quién ejerza la patria '
                             'potestad sobre ellos se llama:',
                 'alternativas': ['Curatela',
                                  'Tutela',
                                  'Apoyo',
                                  'Salvaguardia',
                                  'Adopción'],
                 'correcta': 'B'},
                {'pregunta': 'La tutela que los padres establecen antes de '
                             'morir, designando al tutor en su testamento, '
                             'se llama tutela:',
                 'alternativas': ['Legítima',
                                  'Testamentaria',
                                  'Dativa',
                                  'Estatal',
                                  'Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'La tutela que, a falta de la testamentaria, '
                             'recae en los abuelos u otros descendientes se '
                             'llama tutela:',
                 'alternativas': ['Testamentaria',
                                  'Legítima',
                                  'Dativa',
                                  'Estatal',
                                  'Notarial'],
                 'correcta': 'B'},
                {'pregunta': 'La tutela que establece el consejo de familia '
                             'cuando no hay tutela testamentaria ni legítima '
                             'se llama tutela:',
                 'alternativas': ['Legítima',
                                  'Dativa',
                                  'Estatal',
                                  'Testamentaria',
                                  'Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'La tutela ejercida por el Estado para niños '
                             'huérfanos o abandonados se llama tutela:',
                 'alternativas': ['Dativa',
                                  'Estatal',
                                  'Legítima',
                                  'Testamentaria',
                                  'Notarial'],
                 'correcta': 'B'},
                {'pregunta': 'La institución jurídica creada para proteger a '
                             'la persona y bienes del mayor de edad '
                             'incapacitado se llama:',
                 'alternativas': ['Tutela',
                                  'Curatela',
                                  'Patria potestad',
                                  'Adopción',
                                  'Apoyo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La persona que ejerce la curatela se llama:',
                 'alternativas': ['Curado',
                                  'Curador',
                                  'Tutor',
                                  'Apoderado',
                                  'Albacea'],
                 'correcta': 'B'},
                {'pregunta': 'El adulto que recibe la curatela se llama:',
                 'alternativas': ['Curador',
                                  'Curado',
                                  'Tutelado exclusivo',
                                  'Apoderado',
                                  'Menor'],
                 'correcta': 'B'},
                {'pregunta': 'Los apoyos, según el Código Civil, son formas '
                             'de asistencia libremente elegidas por una '
                             'persona mayor de edad para facilitar el '
                             'ejercicio de:',
                 'alternativas': ['Sus obligaciones',
                                  'Sus derechos',
                                  'Sus deudas',
                                  'Sus contratos exclusivamente',
                                  'Sus bienes exclusivamente'],
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
                 'alternativas': ['Una obligación legal',
                                  'Una decisión estatal',
                                  'Un contrato social',
                                  'Un acuerdo político',
                                  'Un alma colectiva'],
                 'correcta': 'E'},
                {'pregunta': 'Anthony D. Smith asocia a la nación '
                             'principalmente con:',
                 'alternativas': ['Solo la lengua oficial',
                                  'Un territorio nacional y mitos comunes de '
                                  'antepasados',
                                  'Un gobierno central',
                                  'Solo la religión mayoritaria',
                                  'Solo la moneda nacional'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos esenciales de la nación son la '
                             'tradición histórica y:',
                 'alternativas': ['La conciencia nacional',
                                  'El idioma',
                                  'La religión',
                                  'El territorio',
                                  'La raza'],
                 'correcta': 'A'},
                {'pregunta': 'El territorio, la raza, la religión y el '
                             'idioma son elementos de la nación '
                             'considerados:',
                 'alternativas': ['Legales',
                                  'Únicos',
                                  'Esenciales',
                                  'Secundarios',
                                  'Constitucionales'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'define quiénes son peruanos por nacimiento es '
                             'el:',
                 'alternativas': ['Artículo 100',
                                  'Artículo 2',
                                  'Artículo 200',
                                  'Artículo 52',
                                  'Artículo 4'],
                 'correcta': 'D'},
                {'pregunta': 'Son peruanos por nacimiento los nacidos en el '
                             'exterior de padre o madre peruanos si:',
                 'alternativas': ['Nunca pueden ser peruanos',
                                  'Solo si regresan al Perú antes de los 5 '
                                  'años',
                                  'Automáticamente sin ningún trámite',
                                  'Solo si nacen en un país de habla hispana',
                                  'Son inscritos en el registro '
                                  'correspondiente durante su minoría de '
                                  'edad'],
                 'correcta': 'E'},
                {'pregunta': 'La Ley de Nacionalidad del Perú lleva el '
                             'número:',
                 'alternativas': ['Ley N° 26300',
                                  'Ley N° 28044',
                                  'Ley N° 30220',
                                  'Ley N° 27444',
                                  'Ley N° 26574'],
                 'correcta': 'E'},
                {'pregunta': 'Según la Ley de Nacionalidad, un peruano que '
                             'adopta otra nacionalidad:',
                 'alternativas': ['No pierde la peruana, salvo renuncia '
                                  'expresa',
                                  'Debe elegir una sola desde el nacimiento',
                                  'Pierde sus derechos civiles',
                                  'Pierde automáticamente la peruana',
                                  'Debe pagar una multa'],
                 'correcta': 'A'},
                {'pregunta': 'Para renunciar a la nacionalidad peruana es '
                             'necesario:',
                 'alternativas': ['Ser menor de edad',
                                  'Solo presentar el DNI',
                                  'Pedir autorización de los padres',
                                  'Ser mayor de edad y suscribir escritura '
                                  'pública',
                                  'Ninguna formalidad especial'],
                 'correcta': 'D'},
                {'pregunta': 'Los padres pueden renunciar a la nacionalidad '
                             'peruana en nombre de sus hijos menores:',
                 'alternativas': ['Solo con autorización judicial',
                                  'Solo en casos excepcionales',
                                  'Sí, siempre',
                                  'Solo si el hijo lo solicita',
                                  'No, solo los mayores de edad pueden '
                                  'renunciar'],
                 'correcta': 'E'},
                {'pregunta': 'La identidad nacional se define como:',
                 'alternativas': ['Una obligación legal',
                                  'Un requisito para votar',
                                  'El sentimiento subjetivo de pertenecer a '
                                  'una nación concreta',
                                  'Una condición económica',
                                  'Un documento oficial'],
                 'correcta': 'C'},
                {'pregunta': 'El término «peruanidad» fue acuñado por:',
                 'alternativas': ['José Carlos Mariátegui',
                                  'Víctor Andrés Belaunde García',
                                  'Jorge Basadre',
                                  'Manuel González Prada',
                                  'Raúl Porras Barrenechea'],
                 'correcta': 'B'},
                {'pregunta': 'La peruanidad se define como el sentimiento '
                             'que vincula a los pueblos del Perú con:',
                 'alternativas': ['Sus tradiciones y la fe en su futuro',
                                  'Solo su economía',
                                  'Solo su gobierno actual',
                                  'Solo su territorio físico',
                                  'Solo su idioma oficial'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los aspectos que fundamentan la '
                             'peruanidad figura la etapa de cultura:',
                 'alternativas': ['Solo republicana',
                                  'Exclusivamente virreinal',
                                  'Colonial únicamente',
                                  'Prehispánica',
                                  'Solo contemporánea'],
                 'correcta': 'D'},
                {'pregunta': 'La nacionalidad se adquiere, además del '
                             'nacimiento, por naturalización o:',
                 'alternativas': ['Solo por concurso público',
                                  'Solo por decisión judicial',
                                  'Opción, con residencia en el Perú',
                                  'Matrimonio exclusivamente',
                                  'Solo por herencia'],
                 'correcta': 'C'},
                {'pregunta': 'Las personas con doble nacionalidad ejercen '
                             'los derechos y obligaciones:',
                 'alternativas': ['Solo del país extranjero',
                                  'Solo del Perú',
                                  'Ninguno de los dos',
                                  'Del país donde domicilian y cuya '
                                  'nacionalidad poseen',
                                  'De ambos países simultáneamente sin '
                                  'distinción'],
                 'correcta': 'D'},
                {'pregunta': 'La doble nacionalidad confiere a los '
                             'extranjeros naturalizados:',
                 'alternativas': ['Derechos superiores a los nacionales',
                                  'Automática ciudadanía plena',
                                  'Los mismos derechos privativos de los '
                                  'peruanos por nacimiento',
                                  'Ningún derecho privativo de los peruanos '
                                  'por nacimiento',
                                  'Exoneración total de impuestos'],
                 'correcta': 'D'},
                {'pregunta': 'La nación, para Herder y Fichte, se sustenta '
                             'principalmente en:',
                 'alternativas': ['Un tratado internacional',
                                  'Solo el sistema económico',
                                  'Solo la Constitución vigente',
                                  'Solo las fronteras políticas',
                                  'Elementos compartidos como etnia, '
                                  'folclore y cultura'],
                 'correcta': 'E'},
                {'pregunta': 'El renunciante a la nacionalidad peruana que '
                             'vive en el exterior lo hace ante:',
                 'alternativas': ['Un notario extranjero únicamente',
                                  'Las Naciones Unidas',
                                  'El funcionario consular',
                                  'Un juez peruano en el extranjero',
                                  'La embajada de otro país'],
                 'correcta': 'C'},
                {'pregunta': 'El Sistema de Defensa Nacional es presidido y '
                             'dirigido por:',
                 'alternativas': ['El Ministro de Defensa',
                                  'El Presidente de la República',
                                  'El Congreso',
                                  'El Poder Judicial',
                                  'El Jefe del Ejército'],
                 'correcta': 'B'},
                {'pregunta': 'El Sistema de Defensa Nacional está integrado '
                             'por el Consejo de Ministros, el Ministerio de '
                             'Defensa, el Sistema de Inteligencia Nacional y '
                             'el Sistema de:',
                 'alternativas': ['Salud Pública',
                                  'Defensa Civil',
                                  'Educación Nacional',
                                  'Justicia Militar',
                                  'Aduanas'],
                 'correcta': 'B'},
                {'pregunta': 'Las Fuerzas Armadas peruanas están compuestas '
                             'por el Ejército, la Marina de Guerra y:',
                 'alternativas': ['La Policía Nacional',
                                  'La Fuerza Aérea',
                                  'La Guardia Civil',
                                  'El Serenazgo',
                                  'La Marina Mercante'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad de la Policía Nacional del Perú '
                             'es garantizar y restablecer:',
                 'alternativas': ['La soberanía territorial',
                                  'El orden interno',
                                  'La independencia nacional',
                                  'La defensa exterior',
                                  'El comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente de la República es el Jefe '
                             'Supremo de las Fuerzas Armadas y de:',
                 'alternativas': ['El Poder Judicial',
                                  'La Policía Nacional',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio de las banderas se llama:',
                 'alternativas': ['Heráldica',
                                  'Vexilología',
                                  'Filatelia',
                                  'Numismática',
                                  'Genealogía'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 49 de la Constitución, los '
                             'símbolos de la Patria son la bandera, el '
                             'escudo y:',
                 'alternativas': ['La escarapela',
                                  'El himno nacional',
                                  'El águila',
                                  'El sol de Mayo',
                                  'La flor de la cantuta'],
                 'correcta': 'B'},
                {'pregunta': 'La primera bandera republicana peruana fue '
                             'creada por:',
                 'alternativas': ['Simón Bolívar',
                                  'José de San Martín',
                                  'Torre Tagle',
                                  'José de la Torre Ugarte',
                                  'Túpac Amaru II'],
                 'correcta': 'B'},
                {'pregunta': 'La bandera definitiva del Perú fue establecida '
                             'el 25 de febrero de 1825 bajo el gobierno de:',
                 'alternativas': ['José de San Martín',
                                  'Simón Bolívar',
                                  'Torre Tagle',
                                  'Ramón Castilla',
                                  'Andrés A. Cáceres'],
                 'correcta': 'B'},
                {'pregunta': 'Según Abraham Valdelomar, San Martín se '
                             'inspiró para los colores de la bandera en:',
                 'alternativas': ['La bandera chilena',
                                  'Las pariguanas (flamencos)',
                                  'El escudo incaico',
                                  'La bandera argentina exclusivamente',
                                  'El sol de los Incas'],
                 'correcta': 'B'},
                {'pregunta': 'El color rojo de la bandera peruana simboliza:',
                 'alternativas': ['La pureza y la paz',
                                  'La sangre de los héroes y mártires',
                                  'La riqueza mineral',
                                  'El cielo peruano',
                                  'La selva amazónica'],
                 'correcta': 'B'},
                {'pregunta': 'El Escudo Nacional se estableció el 25 de '
                             'febrero de 1825 mediante ley promulgada por:',
                 'alternativas': ['José de San Martín',
                                  'Simón Bolívar',
                                  'Torre Tagle',
                                  'Ramón Castilla',
                                  'El Congreso actual'],
                 'correcta': 'B'},
                {'pregunta': 'En el Escudo Nacional, la vicuña representa el '
                             'reino:',
                 'alternativas': ['Vegetal',
                                  'Animal',
                                  'Mineral',
                                  'Acuático',
                                  'Aéreo'],
                 'correcta': 'B'},
                {'pregunta': 'En el Escudo Nacional, el árbol de la quina '
                             'representa el reino:',
                 'alternativas': ['Animal',
                                  'Vegetal',
                                  'Mineral',
                                  'Marino',
                                  'Aéreo'],
                 'correcta': 'B'},
                {'pregunta': 'En el Escudo Nacional, la cornucopia con '
                             'monedas representa el reino:',
                 'alternativas': ['Animal',
                                  'Vegetal',
                                  'Mineral',
                                  'Marino',
                                  'Celestial'],
                 'correcta': 'B'},
                {'pregunta': 'La letra del Himno Nacional del Perú fue '
                             'escrita por:',
                 'alternativas': ['José Bernardo Alcedo',
                                  'José de la Torre Ugarte',
                                  'Abraham Valdelomar',
                                  'Ricardo Palma',
                                  'César Vallejo'],
                 'correcta': 'B'},
                {'pregunta': 'La música del Himno Nacional del Perú fue '
                             'compuesta por:',
                 'alternativas': ['José de la Torre Ugarte',
                                  'José Bernardo Alcedo',
                                  'Simón Bolívar',
                                  'San Martín',
                                  'Torre Tagle'],
                 'correcta': 'B'},
                {'pregunta': 'El Himno Nacional del Perú fue reconocido por '
                             'ley el 15 de abril de:',
                 'alternativas': ['1820', '1822', '1825', '1821', '1824'],
                 'correcta': 'B'},
                {'pregunta': 'El Himno Nacional consta originalmente de seis '
                             'estrofas, pero actualmente solo se cantan la '
                             'primera y:',
                 'alternativas': ['La segunda',
                                  'La sexta',
                                  'La tercera',
                                  'La cuarta',
                                  'La quinta'],
                 'correcta': 'B'},
                {'pregunta': 'La escarapela, de color blanco y encarnado, es '
                             'un símbolo patrio:',
                 'alternativas': ['Oficial exclusivo',
                                  'No oficial pero de uso arraigado',
                                  'Prohibido por ley',
                                  'Extranjero',
                                  'Militar exclusivo'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Un gobierno de turno',
                                  'Una constitución escrita',
                                  'Un territorio delimitado',
                                  'Un conjunto de ciudadanos',
                                  'La nación jurídicamente organizada'],
                 'correcta': 'E'},
                {'pregunta': 'Los elementos del Estado son población, '
                             'territorio, organización jurídica y:',
                 'alternativas': ['Idioma',
                                  'Soberanía',
                                  'Economía',
                                  'Religión',
                                  'Cultura'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio del Estado se caracteriza por '
                             'ser inalienable e:',
                 'alternativas': ['Divisible',
                                  'Inviolable',
                                  'Transferible',
                                  'Negociable',
                                  'Ilimitado'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 54 de la Constitución, el '
                             'territorio comprende el suelo, el subsuelo, el '
                             'espacio aéreo y:',
                 'alternativas': ['Las fronteras vecinas',
                                  'Solo el litoral',
                                  'El espacio exterior',
                                  'El mar territorial',
                                  'El aire internacional'],
                 'correcta': 'D'},
                {'pregunta': 'La organización jurídica de un Estado está '
                             'integrada por:',
                 'alternativas': ['Las costumbres sociales',
                                  'Los tratados internacionales únicamente',
                                  'Solo la Constitución',
                                  'Solo el Poder Judicial',
                                  'La Constitución, leyes y decretos'],
                 'correcta': 'E'},
                {'pregunta': 'La soberanía interna del Estado implica:',
                 'alternativas': ['Ceder autoridad a otros países',
                                  'Relacionarse con otros Estados',
                                  'Depender de organismos internacionales',
                                  'Supremacía sobre los demás poderes del '
                                  'territorio',
                                  'No tener autoridad propia'],
                 'correcta': 'D'},
                {'pregunta': 'La soberanía externa permite al Estado:',
                 'alternativas': ['Anexar territorios vecinos',
                                  'Imponerse sobre otros Estados',
                                  'Relacionarse con otros Estados soberanos '
                                  'como igual',
                                  'Ignorar el derecho internacional',
                                  'Actuar sin reconocer a otros Estados'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado Constitucional surgió en:',
                 'alternativas': ['Alemania',
                                  'Francia',
                                  'España',
                                  'Estados Unidos',
                                  'Inglaterra'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado Constitucional surgió con el '
                             'objetivo de:',
                 'alternativas': ['Unificar territorios',
                                  'Crear un imperio',
                                  'Fortalecer al monarca absoluto',
                                  'Eliminar toda forma de gobierno',
                                  'Limitar las decisiones de los monarcas '
                                  'absolutos'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado Liberal se desarrolló principalmente '
                             'durante el siglo:',
                 'alternativas': ['XV', 'XVIII', 'XVII', 'XIX', 'XX'],
                 'correcta': 'D'},
                {'pregunta': 'Un pilar del Estado Liberal es:',
                 'alternativas': ['La propiedad privada y la economía de '
                                  'mercado',
                                  'El partido único',
                                  'La censura estatal',
                                  'La monarquía absoluta',
                                  'La propiedad colectiva obligatoria'],
                 'correcta': 'A'},
                {'pregunta': 'En la democracia liberal o representativa, las '
                             'decisiones las toman:',
                 'alternativas': ['Los militares',
                                  'Solo el presidente',
                                  'Todos los ciudadanos directamente',
                                  'Representantes elegidos',
                                  'Un consejo religioso'],
                 'correcta': 'D'},
                {'pregunta': 'En los Estados de partido único, se considera '
                             'legítima expresión de la voluntad general:',
                 'alternativas': ['Las ONG',
                                  'Cualquier partido político',
                                  'Los sindicatos',
                                  'Un único partido',
                                  'Las asambleas populares'],
                 'correcta': 'D'},
                {'pregunta': 'El Estado unitario se caracteriza por '
                             'reconocer como fuente de soberanía:',
                 'alternativas': ['Varias naciones',
                                  'Ninguna nación específica',
                                  'Solo las regiones',
                                  'Organismos internacionales',
                                  'Una sola nación'],
                 'correcta': 'E'},
                {'pregunta': 'En un Estado unitario existe:',
                 'alternativas': ['Un solo gobierno, un parlamento y un '
                                  'poder judicial',
                                  'Múltiples constituciones',
                                  'Solo gobiernos locales',
                                  'Varios gobiernos regionales autónomos',
                                  'Ningún poder judicial central'],
                 'correcta': 'A'},
                {'pregunta': 'El Perú, según su estructura política, es un '
                             'Estado:',
                 'alternativas': ['Confederado',
                                  'Unitario',
                                  'Sin forma definida',
                                  'Monárquico',
                                  'Federal'],
                 'correcta': 'B'},
                {'pregunta': 'La población del Estado está constituida por:',
                 'alternativas': ['Solo los funcionarios públicos',
                                  'Solo los mayores de edad',
                                  'Únicamente los nacidos en el país',
                                  'Solo los ciudadanos con derecho a voto',
                                  'Los habitantes organizados políticamente'],
                 'correcta': 'E'},
                {'pregunta': 'El pueblo, dentro de los elementos del Estado, '
                             'se caracteriza por ser:',
                 'alternativas': ['Subordinado al gobierno extranjero',
                                  'Soberano e independiente',
                                  'Dependiente de otro Estado',
                                  'Neutral políticamente',
                                  'Sin organización'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la organización jurídica, el Estado:',
                 'alternativas': ['Se fortalecería',
                                  'Carecería de forma',
                                  'Tendría más soberanía',
                                  'Sería más eficiente',
                                  'Funcionaría igual'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, en sentido restringido, se refiere '
                             'a:',
                 'alternativas': ['La cultura nacional',
                                  'El idioma oficial',
                                  'El conjunto de organismos que ejercen el '
                                  'poder',
                                  'Todo el territorio nacional',
                                  'Solo la población'],
                 'correcta': 'C'},
                {'pregunta': 'El Gobierno es la autoridad que dirige, '
                             'controla y administra las instituciones de:',
                 'alternativas': ['La sociedad civil',
                                  'El Estado',
                                  'Las empresas privadas',
                                  'Los partidos políticos',
                                  'La familia'],
                 'correcta': 'B'},
                {'pregunta': 'El Gobierno consiste en la conducción política '
                             'general o ejercicio del poder:',
                 'alternativas': ['Legislativo',
                                  'Ejecutivo',
                                  'Judicial',
                                  'Electoral',
                                  'Municipal'],
                 'correcta': 'B'},
                {'pregunta': 'Según Aristóteles, las formas de gobierno se '
                             'dividen en formas puras e:',
                 'alternativas': ['Ideales',
                                  'Impuras',
                                  'Modernas',
                                  'Democráticas exclusivas',
                                  'Antiguas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las formas puras de gobierno según '
                             'Aristóteles está la monarquía, la aristocracia '
                             'y:',
                 'alternativas': ['La tiranía',
                                  'La democracia',
                                  'La oligarquía',
                                  'La demagogia',
                                  'La plutocracia'],
                 'correcta': 'B'},
                {'pregunta': 'La forma pura de gobierno de uno solo se '
                             'llama:',
                 'alternativas': ['Aristocracia',
                                  'Monarquía',
                                  'Democracia',
                                  'Oligarquía',
                                  'Tiranía'],
                 'correcta': 'B'},
                {'pregunta': 'La deformación de la monarquía, donde el único '
                             'gobernante abusa del poder, se llama:',
                 'alternativas': ['Oligarquía',
                                  'Tiranía',
                                  'Demagogia',
                                  'Aristocracia',
                                  'Plutocracia'],
                 'correcta': 'B'},
                {'pregunta': 'La deformación de la aristocracia, donde el '
                             'grupo gobernante atiende sus propios '
                             'intereses, se llama:',
                 'alternativas': ['Tiranía',
                                  'Oligarquía',
                                  'Demagogia',
                                  'Monarquía',
                                  'Democracia'],
                 'correcta': 'B'},
                {'pregunta': 'La deformación de la democracia, donde el '
                             'gobernante halaga al pueblo con regalos, se '
                             'llama:',
                 'alternativas': ['Tiranía',
                                  'Demagogia',
                                  'Oligarquía',
                                  'Aristocracia',
                                  'Plutocracia'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno que está de acuerdo con la '
                             'Constitución se llama gobierno:',
                 'alternativas': ['De facto',
                                  'De jure o de derecho',
                                  'Usurpador',
                                  'Revolucionario',
                                  'Provisional'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno que no ha sido elegido según la '
                             'Constitución, pero no necesariamente usa la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['De jure',
                                  'De facto',
                                  'Usurpador',
                                  'Legítimo',
                                  'Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno que carece de título por no haber '
                             'sido elegido, y se mantiene mediante la '
                             'fuerza, se llama gobierno:',
                 'alternativas': ['De jure',
                                  'De facto',
                                  'Usurpador',
                                  'Parlamentario',
                                  'Presidencialista'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno con un jefe de Estado sin '
                             'responsabilidad y un consejo de ministros '
                             'responsable ante el parlamento se llama '
                             'gobierno:',
                 'alternativas': ['Presidencialista',
                                  'Parlamentario o de gabinete',
                                  'Usurpador',
                                  'De facto',
                                  'Revolucionario'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Internacional únicamente',
                                  'Comparado',
                                  'Privado',
                                  'Consuetudinario',
                                  'Positivo'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución no está sujeta a evaluación de '
                             'validez formal porque:',
                 'alternativas': ['Es revisada cada año',
                                  'La aprueba el Poder Ejecutivo',
                                  'Es una ley ordinaria',
                                  'Depende de tratados internacionales',
                                  'No existe un precepto superior a ella'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución es resultado del ejercicio del '
                             'Poder:',
                 'alternativas': ['Municipal',
                                  'Judicial',
                                  'Legislativo ordinario',
                                  'Constituyente',
                                  'Ejecutivo'],
                 'correcta': 'D'},
                {'pregunta': 'El titular del Poder Constituyente es:',
                 'alternativas': ['El presidente',
                                  'El pueblo',
                                  'El Congreso',
                                  'Los partidos políticos',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 51 de la Constitución, esta '
                             'prevalece sobre:',
                 'alternativas': ['Solo los decretos',
                                  'Toda otra norma legal',
                                  'Solo las leyes penales',
                                  'Solo los tratados internacionales',
                                  'Nada en particular'],
                 'correcta': 'B'},
                {'pregunta': 'El fin último de la Constitución, según el '
                             'texto, debe ser afianzar:',
                 'alternativas': ['La Justicia',
                                  'La economía',
                                  'El comercio internacional',
                                  'El poder del Estado',
                                  'La religión oficial'],
                 'correcta': 'A'},
                {'pregunta': 'El término latino «constitutio» fue '
                             'introducido por:',
                 'alternativas': ['Montesquieu',
                                  'Platón',
                                  'Cicerón',
                                  'Aristóteles',
                                  'Rousseau'],
                 'correcta': 'C'},
                {'pregunta': 'Rousseau llamó «contrato social» a:',
                 'alternativas': ['Un tratado comercial',
                                  'Un acuerdo entre monarcas',
                                  'Una ley penal',
                                  'La decisión originaria del pueblo de '
                                  'fundar la comunidad política',
                                  'Un pacto religioso'],
                 'correcta': 'D'},
                {'pregunta': 'Vattel definió la Constitución como el '
                             'reglamento fundamental que determina:',
                 'alternativas': ['Los impuestos del Estado',
                                  'El idioma nacional',
                                  'Cómo debe ejercerse la autoridad pública',
                                  'La moneda oficial',
                                  'El territorio del Estado'],
                 'correcta': 'C'},
                {'pregunta': 'En 1776, el Congreso de Estados Unidos '
                             'resolvió que los Estados de la Confederación:',
                 'alternativas': ['Adoptaran la Constitución inglesa',
                                  'Formaran una monarquía',
                                  'Se unificaran en un solo territorio',
                                  'Se dieran sus propias Constituciones',
                                  'Eliminaran sus leyes'],
                 'correcta': 'D'},
                {'pregunta': 'El paso de la doctrina del derecho natural a '
                             'la teoría del Estado como contrato social se '
                             'atribuye a:',
                 'alternativas': ['Montesquieu',
                                  'Rousseau',
                                  'Locke exclusivamente',
                                  'Thomas Hobbes',
                                  'Kelsen'],
                 'correcta': 'D'},
                {'pregunta': 'John Locke explicaba que los individuos forman '
                             'una sociedad para:',
                 'alternativas': ['Depender de otro Estado',
                                  'Eliminar toda autoridad',
                                  'Vivir sin normas',
                                  'Beneficiarse mutuamente bajo la '
                                  'protección del Estado y la ley',
                                  'Someterse a un monarca absoluto'],
                 'correcta': 'D'},
                {'pregunta': 'La división entre Constitución formal y '
                             'material fue establecida, entre otros, por:',
                 'alternativas': ['Kelsen',
                                  'Cicerón',
                                  'Vattel',
                                  'Bossuet',
                                  'Rousseau'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución peruana actualmente vigente '
                             'data del año:',
                 'alternativas': ['1856', '1993', '1933', '1920', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución es descrita como la «norma de '
                             'normas» porque:',
                 'alternativas': ['No tiene jerarquía superior a las leyes',
                                  'Es opcional para el Estado',
                                  'Es la primera de las normas de producción',
                                  'Solo aplica al Poder Judicial',
                                  'Solo rige el comercio'],
                 'correcta': 'C'},
                {'pregunta': 'Según Blancas Bustamante, la Constitución '
                             'define la posición de las personas frente al '
                             'Estado mediante:',
                 'alternativas': ['Tratados internacionales exclusivamente',
                                  'Acuerdos comerciales',
                                  'Solo obligaciones tributarias',
                                  'Solo sanciones penales',
                                  'El reconocimiento de libertades y '
                                  'derechos'],
                 'correcta': 'E'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano tuvo como fuente formal:',
                 'alternativas': ['La Constitución española',
                                  'El Código de Hammurabi',
                                  'La Carta Magna inglesa',
                                  'La Constitución rusa',
                                  'Las Constituciones de los Estados de la '
                                  'Confederación norteamericana'],
                 'correcta': 'E'},
                {'pregunta': 'En el siglo XVIII, se consideraba «todo el '
                             'pueblo» al llamado:',
                 'alternativas': ['Primer Estado',
                                  'Cuarto Estado',
                                  'Estado eclesiástico',
                                  'Tercer Estado, compuesto por la burguesía',
                                  'Segundo Estado'],
                 'correcta': 'D'},
                {'pregunta': 'Rousseau llamó «leyes fundamentales» a:',
                 'alternativas': ['La estructura de poder',
                                  'El derecho penal',
                                  'Los tratados internacionales',
                                  'Las costumbres sociales',
                                  'La estructura jurídica correspondiente al '
                                  'régimen político'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución constituye, define y crea los '
                             'poderes:',
                 'alternativas': ['Ninguno en particular',
                                  'Solo el ejecutivo',
                                  'Solo el judicial',
                                  'Legislativo, ejecutivo y judicial',
                                  'Solo el legislativo'],
                 'correcta': 'D'},
                {'pregunta': 'Una Constitución contenida en un documento '
                             'formal se llama Constitución:',
                 'alternativas': ['Consuetudinaria',
                                  'Escrita',
                                  'Flexible',
                                  'Nominal',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que nacen de un acto '
                             'voluntario del Rey, cediendo poderes al '
                             'Parlamento, se llaman:',
                 'alternativas': ['Pactadas',
                                  'Otorgadas',
                                  'Populares',
                                  'Derivadas',
                                  'Rígidas'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que surgen de un '
                             'convenio-pacto entre el Rey y el Parlamento se '
                             'llaman:',
                 'alternativas': ['Otorgadas',
                                  'Pactadas',
                                  'Populares',
                                  'Originarias',
                                  'Flexibles'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que pueden modificarse por '
                             'el procedimiento legislativo ordinario se '
                             'llaman:',
                 'alternativas': ['Rígidas',
                                  'Flexibles',
                                  'Otorgadas',
                                  'Derivadas',
                                  'Semánticas'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones que requieren un '
                             'procedimiento complejo para su reforma se '
                             'llaman:',
                 'alternativas': ['Flexibles',
                                  'Rígidas',
                                  'Pactadas',
                                  'Originarias',
                                  'Nominales'],
                 'correcta': 'B'},
                {'pregunta': 'Las Constituciones cargadas de un programa '
                             'ideológico se llaman:',
                 'alternativas': ['Utilitarias',
                                  'Ideológicas',
                                  'Derivadas',
                                  'Semánticas',
                                  'Nominales'],
                 'correcta': 'B'},
                {'pregunta': 'Según la clasificación de Loewenstein, la '
                             'Constitución efectivamente vivida por '
                             'gobernantes y gobernados se llama:',
                 'alternativas': ['Nominal',
                                  'Normativa',
                                  'Semántica',
                                  'Utilitaria',
                                  'Rígida'],
                 'correcta': 'B'},
                {'pregunta': 'Según Loewenstein, la Constitución que sirve '
                             'para estabilizar y eternizar el poder de los '
                             'dominadores se llama:',
                 'alternativas': ['Normativa',
                                  'Semántica',
                                  'Nominal',
                                  'Ideológica',
                                  'Flexible'],
                 'correcta': 'B'},
                {'pregunta': 'El creador de la jerarquía normativa '
                             'piramidal, conocida como «pirámide de Kelsen», '
                             'fue:',
                 'alternativas': ['Montesquieu',
                                  'Hans Kelsen',
                                  'Rousseau',
                                  'Aristóteles',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'Kelsen esquematizó la jerarquía normativa en '
                             'su obra «La Teoría Pura del Derecho», '
                             'publicada en:',
                 'alternativas': ['1919', '1934', '1945', '1900', '1960'],
                 'correcta': 'B'},
                {'pregunta': 'El primer nivel de la jerarquía normativa '
                             'peruana es:',
                 'alternativas': ['Los tratados',
                                  'La Constitución',
                                  'Las leyes ordinarias',
                                  'Los decretos supremos',
                                  'Las resoluciones'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo nivel de la jerarquía normativa '
                             'incluye tratados, leyes y:',
                 'alternativas': ['Ordenanzas municipales',
                                  'Resoluciones legislativas',
                                  'Directivas internas',
                                  'Circulares',
                                  'Memorandos'],
                 'correcta': 'B'},
                {'pregunta': 'El funcionario facultado para celebrar '
                             'tratados internacionales del Perú es:',
                 'alternativas': ['El Congreso',
                                  'El Presidente de la República',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes que instauran el marco normativo de '
                             'instituciones del Estado y requieren mayoría '
                             'calificada se llaman leyes:',
                 'alternativas': ['Ordinarias',
                                  'Orgánicas',
                                  'Resolutivas',
                                  'Supletorias',
                                  'Reglamentarias'],
                 'correcta': 'B'},
                {'pregunta': 'El Decreto de Urgencia lo dicta el Presidente '
                             'y lo aprueba:',
                 'alternativas': ['El Congreso',
                                  'El Consejo de Ministros',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso de la República del Perú es de '
                             'tipo:',
                 'alternativas': ['Bicameral',
                                  'Unicameral',
                                  'Tricameral',
                                  'Mixto',
                                  'Regional'],
                 'correcta': 'B'},
                {'pregunta': 'El número de congresistas que integran el '
                             'Congreso de la República es:',
                 'alternativas': ['100', '130', '120', '150', '110'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['1976', '1966', '1993', '2000', '1948'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP entró en vigor el:',
                 'alternativas': ['10 de diciembre de 1948',
                                  '1 de enero de 1980',
                                  '16 de diciembre de 1966',
                                  '30 de abril de 1990',
                                  '23 de marzo de 1976'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDCP ha sido ratificado por un total de '
                             'Estados de:',
                 'alternativas': ['50', '75', '100', '200', '167'],
                 'correcta': 'E'},
                {'pregunta': 'El PIDCP consta de un número de partes igual '
                             'a:',
                 'alternativas': ['3', '8', '4', '6', '10'],
                 'correcta': 'D'},
                {'pregunta': 'El PIDCP consta de un número de artículos '
                             'igual a:',
                 'alternativas': ['75', '30', '100', '25', '53'],
                 'correcta': 'E'},
                {'pregunta': 'El Primer Protocolo Facultativo del PIDCP '
                             'regula:',
                 'alternativas': ['Los derechos económicos',
                                  'Los mecanismos de denuncia contra los '
                                  'Estados',
                                  'El comercio internacional',
                                  'La abolición de la pena de muerte',
                                  'La migración'],
                 'correcta': 'B'},
                {'pregunta': 'El Segundo Protocolo Facultativo del PIDCP '
                             'está destinado a:',
                 'alternativas': ['El mecanismo de denuncias',
                                  'Los derechos laborales',
                                  'El comercio exterior',
                                  'La protección ambiental',
                                  'La abolición de la pena de muerte'],
                 'correcta': 'E'},
                {'pregunta': 'Los derechos civiles se distinguen de los '
                             'derechos naturales porque son:',
                 'alternativas': ['Innatos al nacer',
                                  'Universales sin excepción',
                                  'Internacionales por naturaleza',
                                  'Reconocidos dentro de un Estado '
                                  'determinado',
                                  'Otorgados por organismos internacionales'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos naturales o humanos se poseen:',
                 'alternativas': ['Por el mero hecho de nacer',
                                  'Solo en democracias',
                                  'Únicamente si se solicitan',
                                  'Solo si el Estado los otorga',
                                  'Solo a partir de la mayoría de edad'],
                 'correcta': 'A'},
                {'pregunta': 'John Locke sostuvo que debían convertirse en '
                             'derechos civiles protegidos por el Estado:',
                 'alternativas': ['Los derechos económicos',
                                  'Solo el derecho a la vida',
                                  'Los derechos culturales',
                                  'La vida, la libertad y la propiedad',
                                  'Solo el derecho a la propiedad'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho considerado el primero de todos, '
                             'generador de cualquier otro derecho, es el '
                             'derecho a:',
                 'alternativas': ['La propiedad',
                                  'La libertad de expresión',
                                  'La educación',
                                  'La vida',
                                  'El trabajo'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho a la integridad física y '
                             'psicológica protege contra:',
                 'alternativas': ['Los impuestos elevados',
                                  'La libre expresión',
                                  'El comercio informal',
                                  'Las torturas y tratos crueles e inhumanos',
                                  'La migración'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho a la identidad comprende, entre '
                             'otros aspectos:',
                 'alternativas': ['El derecho al voto',
                                  'El derecho a tener un nombre y documento '
                                  'de identidad',
                                  'El derecho al trabajo',
                                  'El derecho a la propiedad',
                                  'El derecho a la educación superior'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos políticos permiten participar en:',
                 'alternativas': ['Solo actividades religiosas',
                                  'La vida privada únicamente',
                                  'El gobierno del Estado y la toma de '
                                  'decisiones',
                                  'El comercio internacional',
                                  'Solo actividades económicas'],
                 'correcta': 'C'},
                {'pregunta': 'Los derechos políticos están reconocidos por:',
                 'alternativas': ['Ninguna norma específica',
                                  'La Constitución y las leyes',
                                  'Solo la costumbre',
                                  'Organismos privados',
                                  'Solo tratados internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'La Parte III del PIDCP, artículos 6 a 27, '
                             'protege contra:',
                 'alternativas': ['La contaminación ambiental',
                                  'El comercio desleal',
                                  'La evasión tributaria',
                                  'El desempleo',
                                  'La discriminación por sexo, religión, '
                                  'raza u otras formas'],
                 'correcta': 'E'},
                {'pregunta': 'La Parte I del PIDCP, artículo 1, trata sobre:',
                 'alternativas': ['La migración',
                                  'La libre determinación de los pueblos',
                                  'Los tratados bilaterales',
                                  'La pena de muerte',
                                  'El comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP es catalogado como un tratado '
                             'internacional de tipo:',
                 'alternativas': ['Bilateral',
                                  'Multilateral general',
                                  'Privado',
                                  'Comercial',
                                  'Regional exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La contraposición al derecho a la vida es:',
                 'alternativas': ['La enfermedad',
                                  'La discapacidad',
                                  'La pobreza',
                                  'La muerte',
                                  'El envejecimiento'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los derechos civiles y políticos '
                             'mencionados figura el derecho a elegir y:',
                 'alternativas': ['No participar',
                                  'Rechazar la ciudadanía',
                                  'Evadir impuestos',
                                  'Ser elegido representante',
                                  'No votar'],
                 'correcta': 'D'},
                {'pregunta': 'La Ley de los Derechos de Participación y '
                             'Control Ciudadano se conoce como Ley:',
                 'alternativas': ['26301',
                                  '26300',
                                  '28237',
                                  '27444',
                                  '26859'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Ley 26300, los ciudadanos pueden '
                             'participar mediante referéndum, iniciativa '
                             'legislativa, remoción o:',
                 'alternativas': ['Amnistía',
                                  'Revocación de autoridades',
                                  'Indulto',
                                  'Censura',
                                  'Vacancia exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Todo acto que prohíba o limite al ciudadano el '
                             'ejercicio de sus derechos de participación es '
                             'considerado:',
                 'alternativas': ['Válido con restricciones',
                                  'Nulo y punible',
                                  'Legal si está motivado',
                                  'Aceptable temporalmente',
                                  'Sujeto a apelación únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa de reforma constitucional '
                             'requiere la adhesión de un porcentaje de la '
                             'población electoral nacional igual a:',
                 'alternativas': ['3%', '0,3%', '10%', '25%', '1%'],
                 'correcta': 'B'},
                {'pregunta': 'Es improcedente toda iniciativa de reforma '
                             'constitucional que recorte los derechos '
                             'ciudadanos consagrados en el artículo:',
                 'alternativas': ['Artículo 1',
                                  'Artículo 2',
                                  'Artículo 5',
                                  'Artículo 10',
                                  'Artículo 20'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa en la formación de leyes '
                             'requiere firmas de no menos del 0,3% del '
                             'electorado, y el Congreso tiene un plazo de:',
                 'alternativas': ['60 días',
                                  '120 días',
                                  '30 días',
                                  '180 días',
                                  '90 días'],
                 'correcta': 'B'},
                {'pregunta': 'El referéndum es el derecho de los ciudadanos '
                             'para pronunciarse sobre, entre otros temas, la '
                             'reforma de:',
                 'alternativas': ['Solo ordenanzas municipales',
                                  'La Constitución',
                                  'Solo decretos supremos',
                                  'Solo tratados internacionales',
                                  'Solo el presupuesto'],
                 'correcta': 'B'},
                {'pregunta': 'El referéndum puede ser solicitado por un '
                             'número de ciudadanos no menor a:',
                 'alternativas': ['5% del electorado',
                                  '10% del electorado',
                                  '25% del electorado',
                                  '0,3% del electorado',
                                  '50% del electorado'],
                 'correcta': 'B'},
                {'pregunta': 'Para que el referéndum sea válido, debe ser '
                             'aprobado por no menos del:',
                 'alternativas': ['10% de los votantes',
                                  '30% del total de votantes',
                                  '50% de los votantes',
                                  '70% de los votantes',
                                  '90% de los votantes'],
                 'correcta': 'B'},
                {'pregunta': 'Una norma aprobada mediante referéndum no '
                             'puede modificarse dentro de los siguientes:',
                 'alternativas': ['Seis meses',
                                  'Dos años',
                                  'Cinco años',
                                  'Un año',
                                  'Diez años'],
                 'correcta': 'B'},
                {'pregunta': 'La revocatoria es el derecho de la ciudadanía '
                             'para destituir de sus cargos a autoridades de '
                             'elección:',
                 'alternativas': ['Designada',
                                  'Popular',
                                  'Judicial exclusiva',
                                  'Militar',
                                  'Eclesiástica'],
                 'correcta': 'B'},
                {'pregunta': 'La revocatoria no procede durante el primer y '
                             'último año de mandato, salvo en el caso de:',
                 'alternativas': ['Alcaldes',
                                  'Magistrados',
                                  'Regidores',
                                  'Congresistas',
                                  'Ministros'],
                 'correcta': 'B'},
                {'pregunta': 'Para solicitar la revocatoria, la solicitud:',
                 'alternativas': ['Debe ser probada judicialmente',
                                  'Solo requiere ser fundamentada',
                                  'Requiere sentencia previa',
                                  'Necesita aprobación del Congreso',
                                  'Requiere referéndum previo'],
                 'correcta': 'B'},
                {'pregunta': 'Para solicitar la revocatoria se requiere la '
                             'firma de al menos un porcentaje de electores '
                             'de la autoridad igual a:',
                 'alternativas': ['10%', '25%', '50%', '5%', '40%'],
                 'correcta': 'B'},
                {'pregunta': 'El número máximo de firmas requeridas para '
                             'solicitar una revocatoria es:',
                 'alternativas': ['100 000',
                                  '400 000',
                                  '1 000 000',
                                  '50 000',
                                  '250 000'],
                 'correcta': 'B'},
                {'pregunta': 'Para revocar a una autoridad se requiere la '
                             'mitad más uno de los votos, y que haya '
                             'asistido al menos:',
                 'alternativas': ['El 25% de electores hábiles',
                                  'El 50% de electores hábiles',
                                  'El 75% de electores hábiles',
                                  'El 10% de electores hábiles',
                                  'Todos los electores hábiles'],
                 'correcta': 'B'},
                {'pregunta': 'Si la revocatoria no procede, no se admite una '
                             'nueva petición hasta después de:',
                 'alternativas': ['Seis meses',
                                  'Dos años',
                                  'Un año',
                                  'Cinco años',
                                  'Nunca más'],
                 'correcta': 'B'},
                {'pregunta': 'Tras una revocatoria exitosa, asume el cargo:',
                 'alternativas': ['Un candidato designado por el JNE',
                                  'Quien alcanzó el siguiente lugar en votos '
                                  'de la misma lista',
                                  'El ganador de nuevas elecciones '
                                  'inmediatas',
                                  'El regidor de mayor edad',
                                  'Ninguno, el cargo queda vacante'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Solo la nacionalidad',
                                  'Solo el sufragio',
                                  'Un nivel de vida adecuado, alimentación y '
                                  'vivienda digna',
                                  'Solo la libertad de tránsito',
                                  'Solo la propiedad privada'],
                 'correcta': 'C'},
                {'pregunta': 'El Protocolo Adicional a la Convención '
                             'Americana en materia de derechos económicos, '
                             'sociales y culturales se conoce como:',
                 'alternativas': ['Protocolo de Nueva York',
                                  'Protocolo de San Salvador',
                                  'Protocolo de Roma',
                                  'Protocolo de Lima',
                                  'Protocolo de Ginebra'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hakansson, estos derechos representan la '
                             'función del Estado de:',
                 'alternativas': ['Equilibrar las desigualdades sociales',
                                  'Reducir el gasto público',
                                  'Aumentar impuestos',
                                  'Privatizar servicios',
                                  'Limitar la educación'],
                 'correcta': 'A'},
                {'pregunta': 'El valor básico que fundamenta todos los '
                             'derechos humanos es:',
                 'alternativas': ['La dignidad de la persona humana',
                                  'El poder político',
                                  'La religión',
                                  'La nacionalidad',
                                  'La riqueza'],
                 'correcta': 'A'},
                {'pregunta': 'Según Nogueira, la dignidad humana fundamenta:',
                 'alternativas': ['Tanto los derechos civiles y políticos '
                                  'como los económicos, sociales y '
                                  'culturales',
                                  'Ningún derecho en particular',
                                  'Solo los derechos económicos',
                                  'Solo los derechos civiles',
                                  'Solo los derechos culturales'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 22 de la Constitución establece '
                             'que el trabajo es:',
                 'alternativas': ['Un deber y un derecho',
                                  'Un privilegio',
                                  'Una actividad comercial',
                                  'Solo un derecho opcional',
                                  'Solo una obligación'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 22, el trabajo es la base '
                             'de:',
                 'alternativas': ['El comercio exterior',
                                  'La recaudación fiscal',
                                  'El sistema bancario',
                                  'La política monetaria',
                                  'El bienestar social'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo 23 de la Constitución protege '
                             'especialmente a:',
                 'alternativas': ['Solo al Estado',
                                  'Solo a los empresarios',
                                  'Solo a los sindicatos',
                                  'A la madre, al menor de edad y al '
                                  'impedido que trabajan',
                                  'A los extranjeros exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 23, ninguna relación laboral '
                             'puede:',
                 'alternativas': ['Solicitar experiencia',
                                  'Limitar los derechos constitucionales ni '
                                  'rebajar la dignidad del trabajador',
                                  'Exigir puntualidad',
                                  'Fijar un sueldo',
                                  'Establecer horarios'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Constitución, nadie está obligado a '
                             'prestar trabajo:',
                 'alternativas': ['En el sector privado',
                                  'Fuera de su ciudad',
                                  'Sin retribución o sin su libre '
                                  'consentimiento',
                                  'Para el Estado',
                                  'Los fines de semana'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 24 de la Constitución establece el '
                             'derecho del trabajador a:',
                 'alternativas': ['Trabajo garantizado de por vida',
                                  'Una remuneración equitativa y suficiente',
                                  'Vacaciones ilimitadas',
                                  'Ascenso automático',
                                  'Doble sueldo'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado promueve condiciones para el '
                             'progreso social y económico mediante:',
                 'alternativas': ['Políticas de fomento del empleo '
                                  'productivo y educación para el trabajo',
                                  'El cierre de empresas',
                                  'La reducción del gasto en educación',
                                  'El aumento de impuestos únicamente',
                                  'La eliminación de sindicatos'],
                 'correcta': 'A'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos, '
                             'en su preámbulo, señala que todo individuo y '
                             'órgano de la sociedad debe:',
                 'alternativas': ['Depender del Estado',
                                  'Promover el respeto a los derechos '
                                  'humanos',
                                  'Rechazar tratados internacionales',
                                  'Limitar la participación ciudadana',
                                  'Ignorar los derechos humanos'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos sociales y económicos buscan que '
                             'los ciudadanos gocen de:',
                 'alternativas': ['Solo prestigio social',
                                  'Un estado de bienestar',
                                  'Ninguna prestación estatal',
                                  'Solo poder político',
                                  'Solo riqueza material'],
                 'correcta': 'B'},
                {'pregunta': 'Según el texto, la persona, en virtud de su '
                             'dignidad, se convierte en:',
                 'alternativas': ['Un sujeto pasivo sin derechos',
                                  'El fin del Estado',
                                  'Un elemento secundario',
                                  'Un obstáculo para el desarrollo',
                                  'Un medio para el Estado'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, según Nogueira, está al servicio '
                             'de:',
                 'alternativas': ['Las empresas privadas',
                                  'La persona humana',
                                  'El mercado',
                                  'Los organismos internacionales',
                                  'Solo el gobierno de turno'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad del Estado, según el texto, es '
                             'promover:',
                 'alternativas': ['El crecimiento demográfico',
                                  'La expansión territorial',
                                  'El comercio exterior únicamente',
                                  'El bien común',
                                  'Solo la recaudación fiscal'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los instrumentos con jerarquía '
                             'constitucional que contemplan estos derechos '
                             'figura:',
                 'alternativas': ['La Declaración Universal de Derechos '
                                  'Humanos',
                                  'Solo el Código Civil',
                                  'Ninguno en particular',
                                  'Solo el Código Penal',
                                  'Solo la Constitución peruana'],
                 'correcta': 'A'},
                {'pregunta': 'El principio de dignidad humana implica que '
                             'los derechos se reconozcan:',
                 'alternativas': ['Solo a ciertos grupos',
                                  'Solo a los ciudadanos con recursos',
                                  'Solo a los adultos',
                                  'Sin distingo de tipo cultural, económico '
                                  'o social',
                                  'Solo a los trabajadores formales'],
                 'correcta': 'D'},
                {'pregunta': 'Los derechos sociales y económicos '
                             'representan, según el texto:',
                 'alternativas': ['Normas sin aplicación práctica',
                                  'Privilegios de unos pocos',
                                  'Los fines sociales del Estado',
                                  'Una carga innecesaria',
                                  'Obligaciones exclusivas del ciudadano'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo 7° de la Constitución establece '
                             'que todos tienen derecho a la protección de:',
                 'alternativas': ['Su patrimonio',
                                  'Su salud',
                                  'Su libertad exclusiva',
                                  'Su intimidad exclusiva',
                                  'Su honor exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 9° de la Constitución señala que '
                             'el Estado determina la política nacional de:',
                 'alternativas': ['Educación',
                                  'Salud',
                                  'Vivienda',
                                  'Trabajo',
                                  'Seguridad'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 11° de la Constitución garantiza '
                             'el libre acceso a prestaciones de salud y:',
                 'alternativas': ['Vivienda',
                                  'Pensiones',
                                  'Educación gratuita',
                                  'Empleo garantizado',
                                  'Vacaciones pagadas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los cuatro aspectos que garantizan la '
                             'salud según la Constitución están '
                             'disponibilidad, accesibilidad, aceptabilidad '
                             'y:',
                 'alternativas': ['Rapidez',
                                  'Calidad',
                                  'Gratuidad total',
                                  'Exclusividad',
                                  'Anonimato'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 13° de la Constitución establece '
                             'que la educación tiene como finalidad el '
                             'desarrollo:',
                 'alternativas': ['Económico del país',
                                  'Integral de la persona humana',
                                  'Militar de la nación',
                                  'Exclusivamente profesional',
                                  'Solo intelectual'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 14° establece que la enseñanza de '
                             'la Constitución y los derechos humanos es:',
                 'alternativas': ['Opcional',
                                  'Obligatoria en todo el proceso educativo',
                                  'Solo para universidades',
                                  'Solo para educación militar',
                                  'Prohibida en colegios religiosos'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 15° de la Constitución establece '
                             'que el profesorado en la enseñanza oficial es:',
                 'alternativas': ['Trabajo temporal',
                                  'Carrera pública',
                                  'Servicio voluntario',
                                  'Cargo de confianza',
                                  'Función privada'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 17° establece que la educación '
                             'inicial, primaria y secundaria son:',
                 'alternativas': ['Opcionales',
                                  'Obligatorias',
                                  'Solo para quienes puedan pagarlas',
                                  'Exclusivas del sector privado',
                                  'Solo secundarias'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 18° establece que la educación '
                             'universitaria tiene como fines la formación '
                             'profesional, la difusión cultural, la creación '
                             'intelectual y:',
                 'alternativas': ['El deporte exclusivo',
                                  'La investigación científica y tecnológica',
                                  'El comercio exterior',
                                  'La política partidaria',
                                  'La religión oficial'],
                 'correcta': 'B'},
                {'pregunta': 'Cada universidad, según la Constitución, es '
                             'autónoma en su régimen normativo, de gobierno, '
                             'académico, administrativo y:',
                 'alternativas': ['Religioso',
                                  'Económico',
                                  'Militar',
                                  'Diplomático',
                                  'Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDESC (Pacto Internacional de Derechos '
                             'Económicos, Sociales y Culturales) fue '
                             'adoptado por la Asamblea General de la ONU en:',
                 'alternativas': ['1948', '1966', '1976', '1993', '1989'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDESC entró en vigor el 3 de enero de:',
                 'alternativas': ['1966', '1976', '1948', '1993', '1989'],
                 'correcta': 'B'},
                {'pregunta': 'El Protocolo de San Salvador entiende el '
                             'derecho a la salud como el disfrute del más '
                             'alto nivel de bienestar físico, mental y:',
                 'alternativas': ['Espiritual',
                                  'Social',
                                  'Económico',
                                  'Político',
                                  'Religioso'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Ejecutar el presupuesto',
                                  'Administrar justicia',
                                  'Dictar, modificar, interpretar y derogar '
                                  'leyes',
                                  'Firmar tratados exclusivamente',
                                  'Nombrar ministros'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano que ejerce la potestad legislativa '
                             'se denomina:',
                 'alternativas': ['Poder Judicial',
                                  'Parlamento',
                                  'Tribunal Constitucional',
                                  'Poder Ejecutivo',
                                  'Jurado Electoral'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 91 de la Constitución, el '
                             'Poder Legislativo reside en:',
                 'alternativas': ['El Congreso',
                                  'El Presidente',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'Los gobiernos regionales'],
                 'correcta': 'A'},
                {'pregunta': 'Poder Legislativo y Congreso de la República '
                             'son, conceptualmente:',
                 'alternativas': ['Términos intercambiables sin matices',
                                  'Categorías conceptuales distintas',
                                  'Exactamente lo mismo',
                                  'Sinónimos absolutos',
                                  'Idénticos en toda circunstancia'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente de la República puede expedir '
                             'normas con rango de ley llamadas:',
                 'alternativas': ['Decretos de Urgencia y Decretos '
                                  'Legislativos',
                                  'Ordenanzas municipales',
                                  'Resoluciones administrativas',
                                  'Directivas internas',
                                  'Circulares'],
                 'correcta': 'A'},
                {'pregunta': 'En regímenes de facto, se gobierna mediante:',
                 'alternativas': ['Decretos Ley',
                                  'Decretos Supremos',
                                  'Directivas',
                                  'Resoluciones Ministeriales',
                                  'Ordenanzas'],
                 'correcta': 'A'},
                {'pregunta': 'Los Gobiernos Locales expiden normas con rango '
                             'de ley llamadas:',
                 'alternativas': ['Resoluciones Legislativas',
                                  'Normas generales',
                                  'Decretos de Urgencia',
                                  'Decretos Legislativos',
                                  'Ordenanzas Municipales'],
                 'correcta': 'E'},
                {'pregunta': 'Los Gobiernos Regionales expiden normas con '
                             'rango de ley denominadas:',
                 'alternativas': ['Normas generales',
                                  'Decretos Ley',
                                  'Ordenanzas Municipales',
                                  'Resoluciones Ministeriales',
                                  'Decretos Supremos'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 102 de la Constitución establece '
                             'que dar leyes es atribución de:',
                 'alternativas': ['El Poder Ejecutivo',
                                  'El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'La Defensoría del Pueblo',
                                  'El Congreso'],
                 'correcta': 'E'},
                {'pregunta': 'La fase introductoria del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La promulgación de la ley',
                                  'La iniciativa para proponer un proyecto '
                                  'de ley',
                                  'La publicación en el diario oficial',
                                  'La votación final',
                                  'El veto presidencial'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa popular en el Perú requiere '
                             'representar de la población electoral:',
                 'alternativas': ['30%', '1%', '0,3%', '3%', '10%'],
                 'correcta': 'C'},
                {'pregunta': 'La fase constitutiva del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['El archivo del proyecto',
                                  'La promulgación',
                                  'La publicación oficial',
                                  'La iniciativa del proyecto',
                                  'La deliberación y aprobación de la ley '
                                  'por el Congreso'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 105, todo proyecto de ley '
                             'debe ser previamente:',
                 'alternativas': ['Consultado con el pueblo',
                                  'Dictaminado por una comisión',
                                  'Publicado en un diario',
                                  'Traducido a lenguas originarias',
                                  'Aprobado por el Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes ordinarias en el Congreso se '
                             'aprueban por:',
                 'alternativas': ['Mayoría simple',
                                  'Unanimidad',
                                  'Consenso obligatorio',
                                  'Mayoría calificada',
                                  'Dos tercios'],
                 'correcta': 'A'},
                {'pregunta': 'Las leyes orgánicas requieren el voto de:',
                 'alternativas': ['Solo la mesa directiva',
                                  'La mayoría relativa',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'Todos los congresistas',
                                  'Un tercio de los congresistas'],
                 'correcta': 'C'},
                {'pregunta': 'La promulgación de la ley es realizada por:',
                 'alternativas': ['El Jurado Nacional de Elecciones',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'El presidente del Congreso',
                                  'El Presidente de la República'],
                 'correcta': 'E'},
                {'pregunta': 'La promulgación consiste en que el Jefe de '
                             'Estado:',
                 'alternativas': ['Vote la ley',
                                  'Elabore el proyecto',
                                  'Modifique el texto legal',
                                  'Rubrique la ley y ordene su publicación',
                                  'Redacte la ley'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 108, la ley aprobada se '
                             'envía al Presidente para:',
                 'alternativas': ['Su revisión judicial',
                                  'Su archivo',
                                  'Su anulación',
                                  'Su traducción',
                                  'Su promulgación'],
                 'correcta': 'E'},
                {'pregunta': 'Las leyes de reforma constitucional se sujetan '
                             'al procedimiento del artículo:',
                 'alternativas': ['108', '206', '91', '102', '105'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho de iniciativa legislativa, además '
                             'del Legislativo y Ejecutivo, se otorga también '
                             'a:',
                 'alternativas': ['El Poder Judicial, gobiernos regionales, '
                                  'locales y colegios profesionales',
                                  'Solo a organismos internacionales',
                                  'Solo a los partidos políticos',
                                  'Solo al sector privado',
                                  'Solo a las universidades'],
                 'correcta': 'A'},
                {'pregunta': 'Mediante la función representativa, los '
                             'congresistas actúan como voceros de:',
                 'alternativas': ['El Poder Ejecutivo',
                                  'Los ciudadanos',
                                  'El Poder Judicial',
                                  'Las Fuerzas Armadas',
                                  'Los organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso de la República está integrado por '
                             'un número de parlamentarios igual a:',
                 'alternativas': ['120', '130', '100', '150', '110'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo del mandato congresal en el Perú es '
                             'de:',
                 'alternativas': ['4 años',
                                  '5 años',
                                  '6 años',
                                  '3 años',
                                  '7 años'],
                 'correcta': 'B'},
                {'pregunta': 'Los congresistas no pueden ser reelegidos de '
                             'manera inmediata para:',
                 'alternativas': ['Ningún cargo público',
                                  'Un nuevo periodo en el mismo cargo',
                                  'Cargos municipales',
                                  'Cargos regionales',
                                  'Ministerios'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso peruano actual tiene cámara única, '
                             'es decir, es de tipo:',
                 'alternativas': ['Bicameral',
                                  'Unicameral',
                                  'Tricameral',
                                  'Mixto',
                                  'Regional'],
                 'correcta': 'B'},
                {'pregunta': 'La única Constitución peruana que reconoció un '
                             'parlamento tricameral fue la de:',
                 'alternativas': ['1839', '1826', '1860', '1920', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las ventajas del sistema unicameral está '
                             'la celeridad en la aprobación de:',
                 'alternativas': ['Presupuestos exclusivamente',
                                  'Normas legales',
                                  'Tratados exclusivamente',
                                  'Impuestos exclusivamente',
                                  'Nombramientos'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las desventajas del sistema unicameral '
                             'está la fácil sumisión del Congreso al:',
                 'alternativas': ['Poder Judicial',
                                  'Poder Ejecutivo',
                                  'Tribunal Constitucional',
                                  'Jurado Nacional de Elecciones',
                                  'Ministerio Público'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima asamblea deliberativa del Congreso, '
                             'integrada por todos los congresistas, se '
                             'llama:',
                 'alternativas': ['Consejo Directivo',
                                  'El Pleno',
                                  'Mesa Directiva',
                                  'Comisión Permanente',
                                  'Junta de Portavoces'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano que tiene a cargo la dirección '
                             'administrativa del Congreso se llama:',
                 'alternativas': ['El Pleno',
                                  'La Mesa Directiva',
                                  'La Comisión Permanente',
                                  'Los Grupos Parlamentarios',
                                  'La Junta de Portavoces'],
                 'correcta': 'B'},
                {'pregunta': 'La Mesa Directiva está compuesta por el '
                             'Presidente y un número de Vicepresidentes '
                             'igual a:',
                 'alternativas': ['Dos', 'Tres', 'Cuatro', 'Uno', 'Cinco'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano encargado del estudio y dictamen de '
                             'asuntos ordinarios se llama:',
                 'alternativas': ['Comisión Permanente',
                                  'Comisiones Ordinarias',
                                  'Consejo Directivo',
                                  'Junta de Portavoces',
                                  'Ligas Parlamentarias'],
                 'correcta': 'B'},
                {'pregunta': 'La Comisión Permanente no puede exceder de un '
                             'porcentaje del total de congresistas igual a:',
                 'alternativas': ['10%', '25%', '50%', '15%', '30%'],
                 'correcta': 'B'},
                {'pregunta': 'Los conjuntos de congresistas que comparten '
                             'ideas o intereses afines se llaman:',
                 'alternativas': ['Ligas Parlamentarias',
                                  'Grupos Parlamentarios',
                                  'Comisiones Ordinarias',
                                  'Consejo Directivo',
                                  'Mesa Directiva'],
                 'correcta': 'B'},
                {'pregunta': 'Además de la función legislativa, el Congreso '
                             'tiene función fiscalizadora y:',
                 'alternativas': ['Ejecutiva',
                                  'Representativa',
                                  'Judicial',
                                  'Notarial',
                                  'Electoral'],
                 'correcta': 'B'},
                {'pregunta': 'Mediante la función fiscalizadora, el Congreso '
                             'puede iniciar investigaciones sobre asuntos de '
                             'interés:',
                 'alternativas': ['Privado exclusivo',
                                  'Público',
                                  'Militar exclusivo',
                                  'Religioso',
                                  'Comercial exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las atribuciones del Congreso en la '
                             'formación de la orientación política general '
                             'está aprobar tratados internacionales y '
                             'declarar:',
                 'alternativas': ['Impuestos',
                                  'La guerra y la paz',
                                  'Feriados nacionales',
                                  'El presupuesto exclusivo',
                                  'Elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'En la gestión financiera, el Congreso aprueba '
                             'el Presupuesto de la República y:',
                 'alternativas': ['Solo los impuestos municipales',
                                  'La Cuenta General',
                                  'Solo el gasto militar',
                                  'Solo las tarifas públicas',
                                  'Solo el tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso designa, entre otros altos '
                             'funcionarios, a los magistrados del Tribunal '
                             'Constitucional y al:',
                 'alternativas': ['Presidente de la República',
                                  'Defensor del Pueblo',
                                  'Fiscal de la Nación exclusivo',
                                  'Presidente del Poder Judicial exclusivo',
                                  'Alcalde de Lima'],
                 'correcta': 'B'},
                {'pregunta': 'La función de congresista es de tiempo '
                             'completo; le está prohibido ejercer otra '
                             'profesión durante:',
                 'alternativas': ['Los fines de semana',
                                  'Las horas de funcionamiento del Congreso',
                                  'Las vacaciones',
                                  'Los feriados',
                                  'Ningún momento, puede ejercer libremente'],
                 'correcta': 'B'},
                {'pregunta': 'El mandato del congresista es incompatible con '
                             'el ejercicio de cualquier otra función '
                             'pública, excepto la de:',
                 'alternativas': ['Alcalde',
                                  'Ministro de Estado',
                                  'Gobernador Regional',
                                  'Juez',
                                  'Fiscal'],
                 'correcta': 'B'}]},
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
                                  'Jefe de Gobierno',
                                  'Jefe religioso',
                                  'Jefe del Congreso',
                                  'Jefe del Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'El Poder Ejecutivo es el órgano encargado de:',
                 'alternativas': ['Administrar justicia',
                                  'La administración del Estado y ejecución '
                                  'de las leyes',
                                  'Organizar elecciones',
                                  'Fiscalizar al Congreso',
                                  'Dictar leyes exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Integran el Poder Ejecutivo el Presidente y:',
                 'alternativas': ['El Poder Judicial',
                                  'La Defensoría del Pueblo',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'El Consejo de Ministros'],
                 'correcta': 'E'},
                {'pregunta': 'En el sistema presidencial, los tres poderes '
                             'del Estado son:',
                 'alternativas': ['Elegidos por el Congreso',
                                  'Autónomos e independientes',
                                  'Fusionados en uno solo',
                                  'Dependientes entre sí',
                                  'Subordinados al Ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser presidente del Perú se requiere ser '
                             'peruano:',
                 'alternativas': ['Naturalizado',
                                  'De nacimiento',
                                  'Con doble nacionalidad',
                                  'Mayor de 50 años exclusivamente',
                                  'Residente'],
                 'correcta': 'B'},
                {'pregunta': 'La edad mínima para postular a la presidencia '
                             'es de:',
                 'alternativas': ['30 años',
                                  '25 años',
                                  '40 años',
                                  '45 años',
                                  '35 años'],
                 'correcta': 'E'},
                {'pregunta': 'El presidente de la República se elige por un '
                             'mandato de:',
                 'alternativas': ['4 años',
                                  '5 años',
                                  '6 años',
                                  '3 años',
                                  '7 años'],
                 'correcta': 'B'},
                {'pregunta': 'La reelección presidencial inmediata en el '
                             'Perú está:',
                 'alternativas': ['Sujeta a referéndum',
                                  'No permitida',
                                  'Permitida sin restricciones',
                                  'Obligatoria',
                                  'Permitida solo una vez'],
                 'correcta': 'B'},
                {'pregunta': 'Para ganar la presidencia en primera vuelta se '
                             'requiere:',
                 'alternativas': ['La mitad exacta de votos válidos',
                                  'Solo más votos que el segundo',
                                  'Un tercio de los votos',
                                  'Mayoría relativa',
                                  'Mayoría absoluta'],
                 'correcta': 'E'},
                {'pregunta': 'Si ningún candidato obtiene mayoría absoluta, '
                             'se realiza:',
                 'alternativas': ['Un sorteo',
                                  'Una decisión del Congreso',
                                  'Una segunda elección entre los dos más '
                                  'votados',
                                  'Una nueva convocatoria general',
                                  'Una tercera vuelta'],
                 'correcta': 'C'},
                {'pregunta': 'Según el artículo 116, el Presidente jura y '
                             'asume el cargo ante:',
                 'alternativas': ['El pueblo directamente',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente asume el cargo el:',
                 'alternativas': ['28 de julio',
                                  '1 de mayo',
                                  '9 de diciembre',
                                  '1 de enero',
                                  '15 de agosto'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las atribuciones del Presidente figura '
                             'representar al Estado:',
                 'alternativas': ['Solo dentro del país',
                                  'Solo ante el Congreso',
                                  'Solo en organismos internacionales',
                                  'Dentro y fuera de la República',
                                  'Solo en tratados comerciales'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente puede convocar al Congreso a '
                             'legislatura:',
                 'alternativas': ['Solo ordinaria',
                                  'Permanente sin descanso',
                                  'Extraordinaria',
                                  'Solo virtual',
                                  'Ninguna, esa función es del Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'El Presidente dirige mensajes obligatorios al '
                             'Congreso al instalarse la legislatura:',
                 'alternativas': ['Ordinaria anual',
                                  'Extraordinaria únicamente',
                                  'Cada seis meses',
                                  'Solo el último año de gobierno',
                                  'Nunca, esa función no le corresponde'],
                 'correcta': 'A'},
                {'pregunta': 'El Presidente reglamenta las leyes mediante:',
                 'alternativas': ['Ordenanzas municipales',
                                  'Decretos y resoluciones',
                                  'Resoluciones legislativas',
                                  'Sentencias judiciales',
                                  'Leyes orgánicas'],
                 'correcta': 'B'},
                {'pregunta': 'Al reglamentar las leyes, el Presidente no '
                             'puede:',
                 'alternativas': ['Ejecutarlas',
                                  'Emitir decretos',
                                  'Cumplirlas',
                                  'Transgredirlas ni desnaturalizarlas',
                                  'Publicarlas'],
                 'correcta': 'D'},
                {'pregunta': 'El Presidente dirige la política exterior y '
                             'puede:',
                 'alternativas': ['Modificar la Constitución solo',
                                  'Declarar la guerra sin el Congreso',
                                  'Elegir a los congresistas',
                                  'Celebrar y ratificar tratados',
                                  'Disolver el Poder Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'Junto con el Presidente se eligen, con los '
                             'mismos requisitos:',
                 'alternativas': ['Los ministros',
                                  'Los gobernadores regionales',
                                  'Los alcaldes',
                                  'Los congresistas',
                                  'Dos vicepresidentes'],
                 'correcta': 'E'},
                {'pregunta': 'El Presidente debe velar por el orden interno '
                             'y:',
                 'alternativas': ['El sistema educativo',
                                  'El comercio exterior',
                                  'La seguridad exterior de la República',
                                  'La política monetaria',
                                  'La reforma agraria'],
                 'correcta': 'C'},
                {'pregunta': 'La Presidencia de la República vaca por '
                             'muerte, incapacidad moral o física, aceptación '
                             'de renuncia o:',
                 'alternativas': ['Vacaciones prolongadas',
                                  'Destitución',
                                  'Enfermedad leve',
                                  'Viaje autorizado',
                                  'Ausencia de un día'],
                 'correcta': 'B'},
                {'pregunta': 'La Presidencia también vaca si el Presidente '
                             'sale del territorio nacional sin permiso de:',
                 'alternativas': ['El Poder Judicial',
                                  'El Congreso',
                                  'El Consejo de Ministros exclusivo',
                                  'La Contraloría',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'El ejercicio de la Presidencia se suspende por '
                             'incapacidad temporal o por estar sometido a '
                             'proceso:',
                 'alternativas': ['Administrativo',
                                  'Judicial',
                                  'Electoral exclusivo',
                                  'Disciplinario menor',
                                  'Fiscal exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 117, el Presidente solo '
                             'puede ser acusado durante su periodo por '
                             'traición a la patria o por impedir:',
                 'alternativas': ['Reformas económicas',
                                  'Las elecciones',
                                  'El comercio exterior',
                                  'La educación pública',
                                  'El turismo'],
                 'correcta': 'B'},
                {'pregunta': 'Por impedimento del Presidente, asume sus '
                             'funciones en primer lugar:',
                 'alternativas': ['El Presidente del Congreso',
                                  'El Primer Vicepresidente',
                                  'El Presidente del Poder Judicial',
                                  'El Premier',
                                  'El Segundo Vicepresidente'],
                 'correcta': 'B'},
                {'pregunta': 'El Consejo de Ministros es el organismo del '
                             'Poder Ejecutivo constituido por la reunión de:',
                 'alternativas': ['Los congresistas',
                                  'Los ministros',
                                  'Los jueces supremos',
                                  'Los gobernadores regionales',
                                  'Los alcaldes'],
                 'correcta': 'B'},
                {'pregunta': 'Son nulos los actos del Presidente que carecen '
                             'de:',
                 'alternativas': ['Aprobación popular',
                                  'Refrendación ministerial',
                                  'Publicación inmediata',
                                  'Firma notarial',
                                  'Sello presidencial'],
                 'correcta': 'B'},
                {'pregunta': 'El jefe del Consejo de Ministros, quien puede '
                             'tener cartera o no, se llama:',
                 'alternativas': ['Vicepresidente',
                                  'Premier o Presidente del Consejo de '
                                  'Ministros',
                                  'Canciller',
                                  'Secretario General',
                                  'Portavoz'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser ministro se requiere ser peruano de '
                             'nacimiento, ciudadano en ejercicio, y tener '
                             'como mínimo:',
                 'alternativas': ['18 años',
                                  '25 años',
                                  '30 años',
                                  '35 años',
                                  '21 años'],
                 'correcta': 'B'},
                {'pregunta': 'Actualmente el Perú cuenta con un número de '
                             'ministerios igual a:',
                 'alternativas': ['15', '18', '20', '12', '16'],
                 'correcta': 'B'},
                {'pregunta': 'Los ministros son individualmente responsables '
                             'por sus propios actos, y solidariamente '
                             'responsables por actos que:',
                 'alternativas': ['Nunca comparten',
                                  'Refrendan en conjunto',
                                  'Delegan a terceros',
                                  'Ocultan al Congreso',
                                  'Publican en el diario oficial'],
                 'correcta': 'B'},
                {'pregunta': 'La interpelación es la facultad de los '
                             'congresistas de requerir a los ministros que:',
                 'alternativas': ['Renuncien inmediatamente',
                                  'Informen, aclaren o expliquen un asunto',
                                  'Sean destituidos',
                                  'Paguen una multa',
                                  'Se retiren del país'],
                 'correcta': 'B'},
                {'pregunta': 'La interpelación debe presentarse por escrito '
                             'por no menos de un porcentaje de congresistas '
                             'igual a:',
                 'alternativas': ['10%', '15%', '25%', '30%', '5%'],
                 'correcta': 'B'},
                {'pregunta': 'El resultado de una interpelación puede ser un '
                             'voto de confianza o un voto de:',
                 'alternativas': ['Aplauso',
                                  'Censura',
                                  'Abstención exclusiva',
                                  'Reconocimiento',
                                  'Felicitación'],
                 'correcta': 'B'},
                {'pregunta': 'Toda moción de censura contra el Consejo de '
                             'Ministros debe presentarse por no menos de un '
                             'porcentaje igual a:',
                 'alternativas': ['15%', '25%', '10%', '50%', '5%'],
                 'correcta': 'B'},
                {'pregunta': 'La aprobación de una moción de censura '
                             'requiere el voto de:',
                 'alternativas': ['Un tercio del Congreso',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'Dos tercios del Congreso',
                                  'Unanimidad',
                                  'La cuarta parte'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente puede disolver el Congreso si '
                             'este ha censurado o negado su confianza a un '
                             'número de Consejos de Ministros igual a:',
                 'alternativas': ['Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco'],
                 'correcta': 'B'},
                {'pregunta': 'Tras la disolución del Congreso, las nuevas '
                             'elecciones deben realizarse dentro de:',
                 'alternativas': ['Dos meses',
                                  'Cuatro meses',
                                  'Seis meses',
                                  'Un año',
                                  'Tres meses'],
                 'correcta': 'B'},
                {'pregunta': 'El Congreso no puede ser disuelto en el último '
                             'año de su mandato ni cuando se está en:',
                 'alternativas': ['Estado de emergencia',
                                  'Estado de sitio',
                                  'Vacaciones parlamentarias',
                                  'Receso ordinario',
                                  'Elecciones municipales'],
                 'correcta': 'B'},
                {'pregunta': 'Al disolverse el Congreso, se mantiene en '
                             'funciones:',
                 'alternativas': ['Ningún órgano',
                                  'La Comisión Permanente',
                                  'El Consejo de Ministros exclusivo',
                                  'La Mesa Directiva exclusiva',
                                  'El Pleno completo'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 137 de la Constitución establece '
                             'dos regímenes de excepción: estado de sitio y '
                             'estado de:',
                 'alternativas': ['Guerra',
                                  'Emergencia',
                                  'Alarma',
                                  'Alerta máxima',
                                  'Conmoción'],
                 'correcta': 'B'},
                {'pregunta': 'Los regímenes de excepción son declarados por '
                             'el Presidente con acuerdo de:',
                 'alternativas': ['El Congreso exclusivo',
                                  'El Consejo de Ministros',
                                  'El Tribunal Constitucional',
                                  'La Contraloría',
                                  'El Poder Judicial'],
                 'correcta': 'B'},
                {'pregunta': 'Durante los regímenes de excepción, no se '
                             'suspenden el hábeas corpus y:',
                 'alternativas': ['El hábeas data',
                                  'El amparo',
                                  'La acción popular',
                                  'El proceso de cumplimiento',
                                  'La acción de inconstitucionalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El estado de emergencia se declara por '
                             'perturbación de la paz, catástrofe o graves '
                             'circunstancias, y dura hasta:',
                 'alternativas': ['30 días',
                                  '60 días',
                                  '90 días',
                                  '45 días',
                                  '15 días'],
                 'correcta': 'B'},
                {'pregunta': 'Durante el estado de emergencia, asumen el '
                             'control interno del país:',
                 'alternativas': ['Los gobiernos regionales',
                                  'Las Fuerzas Armadas',
                                  'El Poder Judicial',
                                  'Los municipios',
                                  'La Policía Nacional exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El estado de sitio se declara en caso de '
                             'invasión, guerra exterior o:',
                 'alternativas': ['Crisis económica',
                                  'Guerra civil',
                                  'Elecciones fraudulentas',
                                  'Escasez de alimentos',
                                  'Corrupción generalizada'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo del estado de sitio no debe exceder '
                             'de:',
                 'alternativas': ['30 días',
                                  '45 días',
                                  '60 días',
                                  '90 días',
                                  '15 días'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Organizar elecciones',
                                  'Dictar leyes',
                                  'Administrar justicia',
                                  'Ejecutar el presupuesto',
                                  'Representar al Estado en el exterior'],
                 'correcta': 'C'},
                {'pregunta': 'El Poder Judicial es autónomo en lo político, '
                             'administrativo, económico y:',
                 'alternativas': ['Educativo',
                                  'Disciplinario',
                                  'Comercial',
                                  'Militar',
                                  'Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'En el ejercicio jurisdiccional, el Poder '
                             'Judicial es:',
                 'alternativas': ['Dirigido por el Presidente',
                                  'Subordinado al Congreso',
                                  'Independiente',
                                  'Dependiente del Ejecutivo',
                                  'Controlado por el Tribunal '
                                  'Constitucional'],
                 'correcta': 'C'},
                {'pregunta': 'La potestad de administrar justicia emana de:',
                 'alternativas': ['Organismos internacionales',
                                  'El Congreso',
                                  'Los jueces exclusivamente',
                                  'El Presidente',
                                  'El pueblo'],
                 'correcta': 'E'},
                {'pregunta': 'El máximo órgano jurisdiccional del Poder '
                             'Judicial es:',
                 'alternativas': ['Los Juzgados Mixtos',
                                  'Las Cortes Superiores',
                                  'El Consejo Ejecutivo',
                                  'La Corte Suprema de Justicia',
                                  'Los Juzgados de Paz'],
                 'correcta': 'D'},
                {'pregunta': 'Los Juzgados de Paz Letrados corresponden al '
                             'nivel:',
                 'alternativas': ['Constitucional',
                                  'Internacional',
                                  'Básico',
                                  'Superior',
                                  'Supremo'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano de gestión encargado de la '
                             'administración del Poder Judicial es:',
                 'alternativas': ['El Consejo Ejecutivo del Poder Judicial',
                                  'La Sala Penal',
                                  'El Ministerio Público',
                                  'El Jurado Nacional de Elecciones',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'A'},
                {'pregunta': 'No existe ni puede establecerse jurisdicción '
                             'independiente, salvo:',
                 'alternativas': ['La militar y la arbitral',
                                  'La internacional',
                                  'La comercial',
                                  'La municipal',
                                  'La religiosa'],
                 'correcta': 'A'},
                {'pregunta': 'El principio de unidad y exclusividad de la '
                             'función jurisdiccional implica que:',
                 'alternativas': ['El Congreso puede sentenciar',
                                  'Existen múltiples jurisdicciones '
                                  'paralelas',
                                  'Los alcaldes pueden juzgar delitos',
                                  'Cualquier autoridad puede juzgar',
                                  'No hay proceso judicial por comisión o '
                                  'delegación'],
                 'correcta': 'E'},
                {'pregunta': 'El principio de independencia jurisdiccional '
                             'impide que una autoridad:',
                 'alternativas': ['Solicite información pública',
                                  'Presente denuncias',
                                  'Participe en audiencias públicas',
                                  'Realice investigaciones periodísticas',
                                  'Se avoque a causas pendientes ante el '
                                  'órgano jurisdiccional'],
                 'correcta': 'E'},
                {'pregunta': 'El debido proceso impide que una persona sea '
                             'juzgada por:',
                 'alternativas': ['Comisiones especiales creadas al efecto',
                                  'La Corte Suprema',
                                  'Un juzgado de paz',
                                  'Un juez competente',
                                  'Un tribunal constitucional'],
                 'correcta': 'A'},
                {'pregunta': 'La regla general en los procesos judiciales es '
                             'la:',
                 'alternativas': ['Publicidad, salvo disposición contraria '
                                  'de la ley',
                                  'Confidencialidad total',
                                  'Prohibición de prensa',
                                  'Reserva absoluta',
                                  'Exclusividad militar'],
                 'correcta': 'A'},
                {'pregunta': 'Los procesos por responsabilidad de '
                             'funcionarios públicos son:',
                 'alternativas': ['Siempre públicos',
                                  'Decididos por el Congreso',
                                  'Siempre reservados',
                                  'Confidenciales por defecto',
                                  'Resueltos por decreto'],
                 'correcta': 'A'},
                {'pregunta': 'La motivación escrita de las resoluciones '
                             'judiciales es obligatoria en:',
                 'alternativas': ['Ningún nivel en particular',
                                  'Solo la primera instancia',
                                  'Solo la Corte Suprema',
                                  'Todas las instancias',
                                  'Solo casos penales'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución que precisa la '
                             'extensión jurisdiccional en comunidades es el:',
                 'alternativas': ['Artículo 149',
                                  'Artículo 51',
                                  'Artículo 91',
                                  'Artículo 24',
                                  'Artículo 22'],
                 'correcta': 'A'},
                {'pregunta': 'Ninguna autoridad puede dejar sin efecto '
                             'resoluciones que han pasado en autoridad de:',
                 'alternativas': ['Consulta previa',
                                  'Reglamento interno',
                                  'Norma transitoria',
                                  'Cosa juzgada',
                                  'Resolución administrativa'],
                 'correcta': 'D'},
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
                                  'Relaciones internacionales',
                                  'Gestión',
                                  'Jurisdicción exclusiva',
                                  'Fiscalización externa'],
                 'correcta': 'C'},
                {'pregunta': 'Los Juzgados de Paz, en la estructura del '
                             'Poder Judicial, están en el nivel:',
                 'alternativas': ['Más básico',
                                  'Internacional',
                                  'Constitucional',
                                  'Militar',
                                  'Supremo'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley Orgánica del Poder Judicial regula, '
                             'junto con la Constitución, el ejercicio de:',
                 'alternativas': ['Solo la disciplina interna',
                                  'Solo la función administrativa',
                                  'Solo las relaciones exteriores',
                                  'Solo el presupuesto',
                                  'Las funciones jurisdiccionales y de '
                                  'gobierno'],
                 'correcta': 'E'},
                {'pregunta': 'El principio que permite que una resolución '
                             'sea revisada por un órgano superior se llama:',
                 'alternativas': ['Unidad jurisdiccional',
                                  'Pluralidad de instancia',
                                  'Cosa juzgada',
                                  'Debido proceso',
                                  'Publicidad'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado debe indemnizar por los errores '
                             'judiciales en procesos penales y por:',
                 'alternativas': ['Multas excesivas',
                                  'Detenciones arbitrarias',
                                  'Demoras administrativas',
                                  'Costas procesales',
                                  'Apelaciones rechazadas'],
                 'correcta': 'B'},
                {'pregunta': 'En caso de vacío o deficiencia de la ley, el '
                             'juez debe aplicar los principios generales del '
                             'derecho y:',
                 'alternativas': ['Su criterio personal exclusivo',
                                  'El derecho consuetudinario',
                                  'Solo jurisprudencia extranjera',
                                  'Ninguna norma adicional',
                                  'Solo la doctrina'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que impide aplicar por semejanza '
                             'la ley penal se llama principio de:',
                 'alternativas': ['Retroactividad',
                                  'Inaplicabilidad por analogía',
                                  'Legalidad exclusiva',
                                  'Tipicidad',
                                  'Proporcionalidad'],
                 'correcta': 'B'},
                {'pregunta': 'Un principio fundamental de la administración '
                             'de justicia es que nadie puede ser penado sin:',
                 'alternativas': ['Confesión previa',
                                  'Proceso judicial previo',
                                  'Denuncia pública',
                                  'Testigos presenciales',
                                  'Pago de fianza'],
                 'correcta': 'B'},
                {'pregunta': 'En caso de duda o conflicto entre leyes '
                             'penales, se debe aplicar la ley:',
                 'alternativas': ['Más antigua',
                                  'Más favorable al procesado',
                                  'Más reciente exclusivamente',
                                  'Extranjera',
                                  'Más severa'],
                 'correcta': 'B'},
                {'pregunta': 'Un principio de la administración de justicia '
                             'establece que nadie puede ser condenado:',
                 'alternativas': ['Sin abogado',
                                  'En ausencia',
                                  'Sin fianza',
                                  'Sin apelación',
                                  'Sin testigos'],
                 'correcta': 'B'},
                {'pregunta': 'Está prohibido revivir procesos fenecidos con '
                             'resolución ejecutoriada; la amnistía y el '
                             'indulto producen efectos de:',
                 'alternativas': ['Nulidad absoluta',
                                  'Cosa juzgada',
                                  'Suspensión temporal',
                                  'Revisión automática',
                                  'Prescripción inmediata'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho de defensa no puede ser negado en '
                             'ningún:',
                 'alternativas': ['Recurso de apelación exclusivo',
                                  'Estado del proceso',
                                  'Tribunal superior exclusivo',
                                  'Proceso civil exclusivo',
                                  'Juicio oral exclusivo'],
                 'correcta': 'B'}]},
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
                                  'Internacional',
                                  'Empresarial',
                                  'Eclesiástico',
                                  'Militar'],
                 'correcta': 'A'},
                {'pregunta': 'El número de organismos constitucionales '
                             'autónomos en el Perú es:',
                 'alternativas': ['Diez',
                                  'Tres',
                                  'Veinte',
                                  'Cinco',
                                  'Quince'],
                 'correcta': 'A'},
                {'pregunta': 'La autonomía de los OCA implica que sus '
                             'directivos:',
                 'alternativas': ['Son elegidos por sorteo',
                                  'Dependen del Presidente',
                                  'Dependen del Congreso exclusivamente',
                                  'Toman decisiones sin someterse a órdenes '
                                  'superiores',
                                  'Actúan solo por consulta popular'],
                 'correcta': 'D'},
                {'pregunta': 'El Tribunal Constitucional es el órgano de '
                             'control de:',
                 'alternativas': ['El presupuesto',
                                  'La Constitución',
                                  'Las elecciones únicamente',
                                  'La banca',
                                  'El comercio exterior'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional está regulado en el '
                             'artículo:',
                 'alternativas': ['158', '201', '102', '91', '24'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional se compone de:',
                 'alternativas': ['Tres miembros',
                                  'Nueve miembros',
                                  'Siete miembros',
                                  'Doce miembros',
                                  'Cinco miembros'],
                 'correcta': 'C'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Vitalicio',
                                  'Tres años',
                                  'Cinco años',
                                  'Cuatro años',
                                  'Diez años'],
                 'correcta': 'C'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por el Congreso con:',
                 'alternativas': ['Unanimidad',
                                  'Consulta popular directa',
                                  'Mayoría absoluta',
                                  'Mayoría simple',
                                  'El voto de los dos tercios del número '
                                  'legal de miembros'],
                 'correcta': 'E'},
                {'pregunta': 'No pueden ser magistrados del Tribunal '
                             'Constitucional los jueces o fiscales que no '
                             'dejaron el cargo con anticipación de:',
                 'alternativas': ['Seis meses',
                                  'Un año',
                                  'Cinco años',
                                  'Dos años',
                                  'Tres meses'],
                 'correcta': 'B'},
                {'pregunta': 'El Ministerio Público es el órgano encargado '
                             'de:',
                 'alternativas': ['Dirigir el gobierno',
                                  'Administrar justicia directamente',
                                  'Perseguir el delito',
                                  'Legislar',
                                  'Emitir moneda'],
                 'correcta': 'C'},
                {'pregunta': 'El Ministerio Público es presidido por:',
                 'alternativas': ['El presidente del Congreso',
                                  'El presidente del Poder Judicial',
                                  'El Defensor del Pueblo',
                                  'El Presidente de la República',
                                  'El Fiscal de la Nación'],
                 'correcta': 'E'},
                {'pregunta': 'El Fiscal de la Nación es elegido por:',
                 'alternativas': ['El Poder Judicial',
                                  'El Presidente de la República',
                                  'El Congreso',
                                  'La Junta de Fiscales Supremos',
                                  'Voto popular directo'],
                 'correcta': 'D'},
                {'pregunta': 'El cargo de Fiscal de la Nación dura:',
                 'alternativas': ['Vitalicio',
                                  'Cinco años',
                                  'Tres años',
                                  'Un año',
                                  'Dos años'],
                 'correcta': 'C'},
                {'pregunta': 'El cargo de Fiscal de la Nación puede '
                             'prorrogarse por reelección hasta por:',
                 'alternativas': ['Cinco años más',
                                  'Un año más',
                                  'No es prorrogable',
                                  'Dos años más',
                                  'Diez años más'],
                 'correcta': 'D'},
                {'pregunta': 'Según el artículo 159, el Ministerio Público '
                             'conduce desde su inicio:',
                 'alternativas': ['La investigación del delito',
                                  'El presupuesto público',
                                  'La política exterior',
                                  'El proceso legislativo',
                                  'Las elecciones'],
                 'correcta': 'A'},
                {'pregunta': 'La Policía Nacional está obligada a cumplir '
                             'los mandatos de:',
                 'alternativas': ['Los gobiernos regionales',
                                  'Los gobiernos locales',
                                  'El Ministerio Público',
                                  'Solo el Poder Judicial',
                                  'Solo el Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los organismos constitucionales '
                             'autónomos figura el organismo encargado de '
                             'emitir moneda, que es:',
                 'alternativas': ['El MEF',
                                  'La SBS',
                                  'La SUNAT',
                                  'El BID',
                                  'El Banco Central de Reserva'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo encargado de la defensa de los '
                             'derechos constitucionales de la persona es:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El JNE',
                                  'La ONPE',
                                  'La Contraloría',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo encargado de organizar los '
                             'procesos electorales es:',
                 'alternativas': ['El RENIEC',
                                  'El Ministerio Público',
                                  'La Defensoría del Pueblo',
                                  'La ONPE',
                                  'El JNE'],
                 'correcta': 'D'},
                {'pregunta': 'El organismo encargado del registro de '
                             'identificación y estado civil es:',
                 'alternativas': ['La ONPE',
                                  'El RENIEC',
                                  'La SUNARP',
                                  'El INEI',
                                  'El JNE'],
                 'correcta': 'B'},
                {'pregunta': 'La Junta Nacional de Justicia sustituyó al:',
                 'alternativas': ['Tribunal Constitucional',
                                  'Consejo Nacional de la Magistratura',
                                  'Ministerio Público',
                                  'Poder Judicial',
                                  'Jurado Nacional de Elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 150 de la Constitución, la '
                             'Junta Nacional de Justicia selecciona y nombra '
                             'a:',
                 'alternativas': ['Solo congresistas',
                                  'Jueces y fiscales',
                                  'Solo alcaldes',
                                  'Solo ministros',
                                  'Solo gobernadores regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser miembro de la Junta Nacional de '
                             'Justicia se requiere tener una edad entre:',
                 'alternativas': ['30 y 65 años',
                                  '45 y 75 años',
                                  '25 y 60 años',
                                  '40 y 70 años',
                                  '35 y 80 años'],
                 'correcta': 'B'},
                {'pregunta': 'La Junta Nacional de Justicia está conformada '
                             'por un número de miembros titulares igual a:',
                 'alternativas': ['Cinco', 'Siete', 'Nueve', 'Tres', 'Once'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de los miembros de la Junta '
                             'Nacional de Justicia es de:',
                 'alternativas': ['Cuatro años',
                                  'Cinco años',
                                  'Seis años',
                                  'Tres años',
                                  'Siete años'],
                 'correcta': 'B'},
                {'pregunta': 'La Defensoría del Pueblo tiene su origen '
                             'histórico en:',
                 'alternativas': ['Inglaterra',
                                  'Suecia',
                                  'Francia',
                                  'España',
                                  'Estados Unidos'],
                 'correcta': 'B'},
                {'pregunta': 'El Defensor del Pueblo es elegido y removido '
                             'por el Congreso con el voto de:',
                 'alternativas': ['La mitad más uno',
                                  'Los dos tercios de su número legal',
                                  'Un tercio',
                                  'Mayoría simple',
                                  'Unanimidad'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser elegido Defensor del Pueblo se '
                             'requiere tener una edad mínima de:',
                 'alternativas': ['25 años',
                                  '35 años',
                                  '40 años',
                                  '30 años',
                                  '45 años'],
                 'correcta': 'B'},
                {'pregunta': 'El cargo de Defensor del Pueblo dura:',
                 'alternativas': ['Cuatro años',
                                  'Cinco años',
                                  'Seis años',
                                  'Tres años',
                                  'Siete años'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad principal del Banco Central de '
                             'Reserva es:',
                 'alternativas': ['Recaudar impuestos',
                                  'Preservar la estabilidad monetaria',
                                  'Administrar el presupuesto público',
                                  'Supervisar el Poder Judicial',
                                  'Fiscalizar elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'El BCR está prohibido de conceder '
                             'financiamiento al erario, salvo la compra en '
                             'el mercado secundario de valores emitidos por:',
                 'alternativas': ['Bancos privados',
                                  'El Tesoro Público',
                                  'Empresas mineras',
                                  'Gobiernos regionales',
                                  'Municipalidades'],
                 'correcta': 'B'},
                {'pregunta': 'La SBS (Superintendencia de Banca, Seguros y '
                             'AFP) supervisa a las empresas vinculadas al '
                             'ámbito:',
                 'alternativas': ['Educativo',
                                  'Financiero y de seguros',
                                  'Agrícola',
                                  'Minero',
                                  'Turístico'],
                 'correcta': 'B'},
                {'pregunta': 'El Superintendente de la SBS es designado por '
                             'el Poder Ejecutivo y ratificado por:',
                 'alternativas': ['El Poder Judicial',
                                  'El Congreso',
                                  'La Contraloría',
                                  'El Tribunal Constitucional',
                                  'El BCR'],
                 'correcta': 'B'},
                {'pregunta': 'La Contraloría General de la República es el '
                             'órgano superior del Sistema Nacional de:',
                 'alternativas': ['Justicia',
                                  'Control',
                                  'Educación',
                                  'Salud',
                                  'Seguridad'],
                 'correcta': 'B'},
                {'pregunta': 'El Contralor General es designado por el '
                             'Congreso, a propuesta del Poder Ejecutivo, por '
                             'un periodo de:',
                 'alternativas': ['Cinco años',
                                  'Siete años',
                                  'Cuatro años',
                                  'Seis años',
                                  'Tres años'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema electoral peruano es de naturaleza:',
                 'alternativas': ['Unicéfalo',
                                  'Tricéfalo',
                                  'Bicéfalo',
                                  'Tetracéfalo',
                                  'Pentacéfalo'],
                 'correcta': 'B'},
                {'pregunta': 'Los integrantes del Pleno del Jurado Nacional '
                             'de Elecciones son elegidos por un periodo de:',
                 'alternativas': ['Tres años',
                                  'Cuatro años',
                                  'Cinco años',
                                  'Seis años',
                                  'Dos años'],
                 'correcta': 'B'},
                {'pregunta': 'El JNE fiscaliza la legalidad del ejercicio '
                             'del sufragio y de la realización de:',
                 'alternativas': ['Solo el presupuesto',
                                  'Los procesos electorales',
                                  'Solo la educación cívica',
                                  'Solo el registro civil',
                                  'Solo la seguridad ciudadana'],
                 'correcta': 'B'},
                {'pregunta': 'El Pleno del Jurado Nacional de Elecciones '
                             'está compuesto por un número de miembros igual '
                             'a:',
                 'alternativas': ['Tres',
                                  'Cinco',
                                  'Siete',
                                  'Nueve',
                                  'Cuatro'],
                 'correcta': 'B'},
                {'pregunta': 'El Jefe de la Oficina Nacional de Procesos '
                             'Electorales (ONPE) es nombrado por:',
                 'alternativas': ['El Congreso',
                                  'La Junta Nacional de Justicia',
                                  'El Presidente de la República',
                                  'El JNE',
                                  'La Contraloría'],
                 'correcta': 'B'},
                {'pregunta': 'A la ONPE le corresponde organizar los '
                             'procesos electorales, incluyendo el diseño de:',
                 'alternativas': ['Las leyes electorales',
                                  'La cédula de sufragio',
                                  'Los partidos políticos',
                                  'El padrón judicial',
                                  'Las cortes electorales'],
                 'correcta': 'B'},
                {'pregunta': 'El RENIEC tiene a su cargo la inscripción de '
                             'nacimientos, matrimonios, divorcios y:',
                 'alternativas': ['Contratos comerciales',
                                  'Defunciones',
                                  'Propiedades',
                                  'Empresas',
                                  'Vehículos'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['El Estado en materia económica',
                                  'Los sindicatos',
                                  'El sector informal',
                                  'Los organismos internacionales',
                                  'Las empresas privadas'],
                 'correcta': 'A'},
                {'pregunta': 'Según García Belaúnde, la Constitución '
                             'Económica surgió en:',
                 'alternativas': ['La Antigüedad clásica',
                                  'El siglo XIX',
                                  'El periodo de entreguerras del siglo XX',
                                  'El siglo XXI',
                                  'La época colonial'],
                 'correcta': 'C'},
                {'pregunta': 'La constitución considerada pionera del '
                             'constitucionalismo económico es la de:',
                 'alternativas': ['Roma',
                                  'Filadelfia',
                                  'Weimar',
                                  'Bayona',
                                  'Cádiz'],
                 'correcta': 'C'},
                {'pregunta': 'La Constitución de Weimar garantiza el derecho '
                             'de:',
                 'alternativas': ['Propiedad, con límites por el bien '
                                  'general',
                                  'Voto universal',
                                  'Libre comercio sin restricciones',
                                  'Monopolio estatal',
                                  'Nacionalización total'],
                 'correcta': 'A'},
                {'pregunta': 'El régimen económico peruano se basa, entre '
                             'otros principios, en la economía social de:',
                 'alternativas': ['Planificación central',
                                  'Autarquía',
                                  'Mercado',
                                  'Estado',
                                  'Trueque'],
                 'correcta': 'C'},
                {'pregunta': 'La economía social de mercado es '
                             'representativa de los valores de:',
                 'alternativas': ['Autoridad y jerarquía',
                                  'Libertad y justicia',
                                  'Propiedad colectiva obligatoria',
                                  'Uniformidad y control',
                                  'Aislamiento económico'],
                 'correcta': 'B'},
                {'pregunta': 'Según Herhärd y Müller Armack, la economía '
                             'social de mercado transforma la productividad '
                             'individual en:',
                 'alternativas': ['Control estatal total',
                                  'Progreso social',
                                  'Monopolio privado',
                                  'Estancamiento económico',
                                  'Ganancia exclusiva de empresarios'],
                 'correcta': 'B'},
                {'pregunta': 'La economía social de mercado combate la '
                             'formación de:',
                 'alternativas': ['Mercados locales',
                                  'Carteles y concentración de poder '
                                  'económico',
                                  'Cooperativas',
                                  'Pequeñas empresas',
                                  'Sindicatos'],
                 'correcta': 'B'},
                {'pregunta': 'Para que funcione de manera óptima el mercado, '
                             'el Estado debe:',
                 'alternativas': ['Eliminar la competencia',
                                  'Nacionalizar las empresas',
                                  'Establecer normas claras sin intervenir '
                                  'de manera permanente',
                                  'Intervenir permanentemente',
                                  'Controlar todos los precios'],
                 'correcta': 'C'},
                {'pregunta': 'La economía social de mercado requiere un '
                             'Estado:',
                 'alternativas': ['Sin aparato judicial',
                                  'Fuerte e independiente de los grupos de '
                                  'poder económico',
                                  'Débil y dependiente de grupos de poder',
                                  'Controlado por monopolios',
                                  'Ausente en la economía'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de solidaridad en la economía '
                             'social de mercado exige:',
                 'alternativas': ['Aislamiento económico',
                                  'Individualismo extremo',
                                  'Monopolio estatal',
                                  'Equilibrio social y promoción del bien '
                                  'común',
                                  'Competencia sin límites'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de subsidiaridad establece que el '
                             'Estado no debe hacer:',
                 'alternativas': ['Políticas sociales',
                                  'Lo que el individuo puede hacer por '
                                  'propia iniciativa',
                                  'Control tributario',
                                  'Regulación económica',
                                  'Ninguna función pública'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado y la competencia, según el texto, '
                             'deben garantizar la libertad de:',
                 'alternativas': ['Solo los inversionistas extranjeros',
                                  'Solo los empresarios',
                                  'Solo el Estado',
                                  'Solo los bancos',
                                  'Consumidores, empleadores y trabajadores'],
                 'correcta': 'E'},
                {'pregunta': 'Combatir los monopolios requiere, según el '
                             'texto, una legislación:',
                 'alternativas': ['De libre mercado absoluto',
                                  'De protección arancelaria total',
                                  'De control de precios',
                                  'De nacionalización',
                                  'Antimonopolio'],
                 'correcta': 'E'},
                {'pregunta': 'El régimen económico también se define como el '
                             'conjunto de reglas de juego con rango:',
                 'alternativas': ['Internacional exclusivo',
                                  'Consuetudinario',
                                  'Reglamentario',
                                  'Municipal',
                                  'Constitucional'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los principios que rigen el régimen '
                             'económico peruano figura la libre:',
                 'alternativas': ['Expropiación',
                                  'Nacionalización',
                                  'Migración',
                                  'Competencia',
                                  'Censura'],
                 'correcta': 'D'},
                {'pregunta': 'El régimen económico busca contribuir '
                             'positivamente al:',
                 'alternativas': ['Desempeño económico del país',
                                  'Aislamiento comercial',
                                  'Cierre de fronteras',
                                  'Control absoluto del mercado',
                                  'Monopolio estatal'],
                 'correcta': 'A'},
                {'pregunta': 'El aparato administrativo y judicial en la '
                             'economía social de mercado debe ser:',
                 'alternativas': ['Dependiente del poder económico',
                                  'Controlado por empresas privadas',
                                  'Independiente y libre de corrupción',
                                  'Subordinado al Congreso',
                                  'Eliminado del sistema'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado, en una economía social de mercado, '
                             'actúa por medio de:',
                 'alternativas': ['La propiedad estatal de todo',
                                  'El sistema monetario y el ordenamiento '
                                  'jurídico',
                                  'El control absoluto de empresas',
                                  'La eliminación del mercado',
                                  'La intervención directa en precios'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los principios del régimen económico '
                             'constitucional peruano figura la igualdad de '
                             'tratamiento al:',
                 'alternativas': ['Capital',
                                  'Poder Ejecutivo',
                                  'Poder Judicial',
                                  'Congreso',
                                  'Estado'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo 58 de la Constitución establece '
                             'que la iniciativa privada es libre, ejercida '
                             'en una economía:',
                 'alternativas': ['Centralmente planificada',
                                  'Social de mercado',
                                  'De subsistencia',
                                  'Cerrada exclusiva',
                                  'Colectivizada'],
                 'correcta': 'B'},
                {'pregunta': 'El reconocimiento constitucional de las '
                             'libertades económicas en el Perú se inicia con '
                             'el texto de:',
                 'alternativas': ['1856', '1823', '1920', '1979', '1993'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad de empresa comprende, entre otras '
                             'facultades, emprender, crear, organizar, '
                             'gestionar y:',
                 'alternativas': ['Evadir impuestos',
                                  'Cerrar la empresa',
                                  'Monopolizar el mercado',
                                  'Evitar la competencia',
                                  'Contaminar libremente'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad de comercio se define como la '
                             'capacidad de mediar entre la oferta y:',
                 'alternativas': ['El Estado',
                                  'La demanda',
                                  'El sistema tributario',
                                  'Los tratados internacionales',
                                  'La banca central'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 59, el ejercicio de la '
                             'libertad de comercio no debe ser lesivo a la '
                             'moral, la salud o:',
                 'alternativas': ['Las ganancias',
                                  'La seguridad pública',
                                  'Los impuestos',
                                  'El comercio exterior',
                                  'Las utilidades'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad de industria consiste en la '
                             'facultad de realizar operaciones para la '
                             'obtención o transformación de:',
                 'alternativas': ['Servicios exclusivamente',
                                  'Productos naturales',
                                  'Capital financiero exclusivo',
                                  'Mano de obra exclusiva',
                                  'Divisas exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 65 de la Constitución establece un '
                             'deber especial de protección a:',
                 'alternativas': ['Los empresarios',
                                  'Los consumidores y usuarios',
                                  'El Estado exclusivamente',
                                  'Los bancos',
                                  'Los inversionistas exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'El tributo es el género, y sus especies son el '
                             'impuesto, la tasa y:',
                 'alternativas': ['El arancel exclusivo',
                                  'La contribución',
                                  'La multa',
                                  'El interés',
                                  'La comisión'],
                 'correcta': 'B'},
                {'pregunta': 'El fundamento del impuesto es la capacidad:',
                 'alternativas': ['Legal',
                                  'Contributiva',
                                  'Patrimonial exclusiva',
                                  'Comercial exclusiva',
                                  'Administrativa'],
                 'correcta': 'B'},
                {'pregunta': 'La recaudación de impuestos es controlada '
                             'mediante el principio de caja:',
                 'alternativas': ['Múltiple',
                                  'Única',
                                  'Compartida',
                                  'Regional',
                                  'Descentralizada'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa tiene como hecho gravado un servicio '
                             'público:',
                 'alternativas': ['Colectivo exclusivo',
                                  'Individualizado',
                                  'Gratuito exclusivo',
                                  'Voluntario',
                                  'Optativo'],
                 'correcta': 'B'},
                {'pregunta': 'La contribución es el tributo cuya obligación '
                             'tiene como hecho generador beneficios '
                             'derivados de obras públicas o:',
                 'alternativas': ['Ventas privadas',
                                  'Actividades estatales',
                                  'Herencias',
                                  'Donaciones',
                                  'Préstamos bancarios'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 74, los tributos se crean, '
                             'modifican o derogan exclusivamente por ley o:',
                 'alternativas': ['Decreto supremo exclusivo',
                                  'Decreto legislativo en caso de delegación',
                                  'Ordenanza municipal exclusiva',
                                  'Resolución ministerial',
                                  'Reglamento interno'],
                 'correcta': 'B'},
                {'pregunta': 'Los gobiernos locales pueden crear, modificar '
                             'y suprimir contribuciones y tasas dentro de '
                             'su:',
                 'alternativas': ['Presupuesto exclusivo',
                                  'Jurisdicción',
                                  'Consejo Regional',
                                  'Cartera ministerial',
                                  'Circunscripción electoral'],
                 'correcta': 'B'},
                {'pregunta': 'Ningún tributo puede tener efecto:',
                 'alternativas': ['Retroactivo exclusivamente',
                                  'Confiscatorio',
                                  'Progresivo',
                                  'Proporcional',
                                  'Regresivo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 74, los decretos de urgencia '
                             'no pueden contener materia:',
                 'alternativas': ['Presupuestaria exclusiva',
                                  'Tributaria',
                                  'Educativa',
                                  'Ambiental',
                                  'Laboral exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de reserva de la ley establece '
                             'que solo por ley se puede determinar al '
                             'contribuyente y fijar:',
                 'alternativas': ['El nombre del tributo',
                                  'El monto del tributo',
                                  'La fecha de pago exclusivamente',
                                  'El lugar de pago',
                                  'El banco receptor'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que complementa la reserva de '
                             'ley, referido al uso del instrumento legal '
                             'permitido por su titular, se llama principio '
                             'de:',
                 'alternativas': ['Igualdad',
                                  'Legalidad',
                                  'Proporcionalidad',
                                  'Capacidad contributiva',
                                  'No confiscatoriedad'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de igualdad tributaria establece '
                             'que situaciones iguales deben ser tratadas '
                             'igualmente y las situaciones desiguales:',
                 'alternativas': ['También igualmente',
                                  'Desigualmente',
                                  'De forma arbitraria',
                                  'Sin ningún criterio',
                                  'Con exención total'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Del Estado peruano',
                                  'Del sector financiero exclusivamente',
                                  'Del sector privado',
                                  'Solo del sistema judicial',
                                  'Solo del sistema educativo'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización busca alcanzar un '
                             'gobierno:',
                 'alternativas': ['Exclusivamente militar',
                                  'Centralizado y jerárquico',
                                  'Sin participación ciudadana',
                                  'Autoritario',
                                  'Efectivo, eficiente y al servicio de la '
                                  'ciudadanía'],
                 'correcta': 'E'},
                {'pregunta': 'Según Finot, la descentralización es un '
                             'proceso de transferencia desde el gobierno '
                             'nacional hacia:',
                 'alternativas': ['Ningún otro nivel de gobierno',
                                  'El sector privado',
                                  'Una autoridad subnacional o local',
                                  'Las Fuerzas Armadas',
                                  'Organismos internacionales'],
                 'correcta': 'C'},
                {'pregunta': 'La descentralización, según el texto, busca '
                             'reducir:',
                 'alternativas': ['Los servicios públicos',
                                  'El desarrollo regional',
                                  'La pobreza y la corrupción',
                                  'La participación ciudadana',
                                  'La inversión privada'],
                 'correcta': 'C'},
                {'pregunta': 'Un objetivo general de la descentralización es '
                             'que cada gobierno regional y local:',
                 'alternativas': ['Decida sobre sus propios recursos',
                                  'Dependa del gobierno central para todo',
                                  'Se subordine a Lima',
                                  'Elimine su autonomía',
                                  'No participe en la gestión pública'],
                 'correcta': 'A'},
                {'pregunta': 'Un objetivo político de la descentralización '
                             'es:',
                 'alternativas': ['La eliminación de gobiernos locales',
                                  'La unidad y eficiencia del Estado',
                                  'La centralización total',
                                  'El aislamiento regional',
                                  'El debilitamiento del Estado'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo económico de la descentralización '
                             'es:',
                 'alternativas': ['Reducir los servicios sociales',
                                  'Eliminar la inversión regional',
                                  'Concentrar recursos en Lima',
                                  'Aumentar la dependencia central',
                                  'El desarrollo económico autosostenido de '
                                  'las regiones'],
                 'correcta': 'E'},
                {'pregunta': 'Otro objetivo económico de la '
                             'descentralización es la redistribución:',
                 'alternativas': ['Exclusiva para Lima',
                                  'Desigual de recursos',
                                  'Equitativa de los recursos del Estado',
                                  'Centralizada de los recursos',
                                  'Solo para zonas urbanas'],
                 'correcta': 'C'},
                {'pregunta': 'Históricamente, el Perú ha sido caracterizado '
                             'por los analistas como un país:',
                 'alternativas': ['Confederado',
                                  'Centralista',
                                  'Descentralizado desde su origen',
                                  'Federal',
                                  'Sin estructura política definida'],
                 'correcta': 'B'},
                {'pregunta': 'El «descentralismo centralista» se extiende '
                             'desde el inicio de la República hasta:',
                 'alternativas': ['2002', '1920', '1993', '1821', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'provinieron principalmente de:',
                 'alternativas': ['Los gobiernos regionales actuales',
                                  'El pensamiento capitalino, de la élite de '
                                  'Lima',
                                  'Los movimientos indígenas',
                                  'Las provincias',
                                  'Organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'carecieron de:',
                 'alternativas': ['Marco legal',
                                  'Apoyo internacional',
                                  'Interés político',
                                  'Presupuesto estatal',
                                  'Respaldo social provinciano'],
                 'correcta': 'D'},
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
                 'alternativas': ['Solo político',
                                  'Exclusivamente fiscal',
                                  'Unidimensional',
                                  'Multidimensional, con dinámicas '
                                  'políticas, fiscales y administrativas',
                                  'Solo administrativo'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los objetivos generales de la '
                             'descentralización figura la participación de:',
                 'alternativas': ['Solo el gobierno central',
                                  'La sociedad civil',
                                  'Solo organismos internacionales',
                                  'Solo el sector militar',
                                  'Solo las empresas privadas'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización busca la integración '
                             'entre el Estado y:',
                 'alternativas': ['Solo las Fuerzas Armadas',
                                  'Ningún actor social',
                                  'Solo el sector privado',
                                  'Solo organismos extranjeros',
                                  'La sociedad civil'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los objetivos políticos figura la '
                             'institucionalización de:',
                 'alternativas': ['Un solo partido político',
                                  'Regímenes militares',
                                  'Sólidos gobiernos regionales y locales',
                                  'Gobiernos centralizados',
                                  'Gobiernos temporales'],
                 'correcta': 'C'},
                {'pregunta': 'Un objetivo económico es la cobertura de '
                             'servicios sociales básicos en:',
                 'alternativas': ['Solo zonas urbanas',
                                  'Todo el territorio nacional',
                                  'Solo zonas fronterizas',
                                  'Solo la capital',
                                  'Solo zonas costeras'],
                 'correcta': 'B'},
                {'pregunta': 'El descentralismo formó parte de casi todos '
                             'los proyectos políticos, pero por razones '
                             'estructurales:',
                 'alternativas': ['Se aplicaron de inmediato',
                                  'No llegaron a concretarse',
                                  'No generaron ningún debate',
                                  'Fueron rechazados por la población',
                                  'Se cumplieron totalmente'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización tiene como finalidad el '
                             'desarrollo integral, armónico y:',
                 'alternativas': ['Temporal',
                                  'Sostenible del país',
                                  'Exclusivo de Lima',
                                  'Solo económico',
                                  'Limitado a la costa'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano normativo y fiscalizador del '
                             'Gobierno Regional se llama:',
                 'alternativas': ['Presidencia Regional',
                                  'Consejo Regional',
                                  'Consejo de Coordinación Regional',
                                  'Gerencia Regional',
                                  'Alcaldía Regional'],
                 'correcta': 'B'},
                {'pregunta': 'Los consejeros regionales son elegidos por '
                             'sufragio directo por un periodo de:',
                 'alternativas': ['Cinco años',
                                  'Cuatro años',
                                  'Tres años',
                                  'Seis años',
                                  'Dos años'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano ejecutivo del Gobierno Regional se '
                             'llama Presidencia Regional; desde 2015 al '
                             'presidente se le llama:',
                 'alternativas': ['Alcalde Regional',
                                  'Gobernador Regional',
                                  'Prefecto',
                                  'Ministro Regional',
                                  'Delegado Regional'],
                 'correcta': 'B'},
                {'pregunta': 'El Consejo de Coordinación Regional está '
                             'integrado por alcaldes provinciales y '
                             'representantes de:',
                 'alternativas': ['El Congreso',
                                  'La sociedad civil',
                                  'El Poder Judicial',
                                  'Otros gobiernos regionales exclusivamente',
                                  'El Ejecutivo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas que regulan asuntos de carácter '
                             'general del gobierno regional se llaman:',
                 'alternativas': ['Acuerdos regionales',
                                  'Ordenanzas regionales',
                                  'Decretos regionales',
                                  'Resoluciones regionales',
                                  'Directivas regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas que expresan la decisión del '
                             'Consejo Regional sobre asuntos internos se '
                             'llaman:',
                 'alternativas': ['Ordenanzas regionales',
                                  'Acuerdos regionales',
                                  'Decretos regionales',
                                  'Resoluciones regionales',
                                  'Circulares regionales'],
                 'correcta': 'B'},
                {'pregunta': 'Las normas reglamentarias para ejecutar las '
                             'ordenanzas regionales, aprobadas por la '
                             'presidencia regional, se llaman:',
                 'alternativas': ['Acuerdos regionales',
                                  'Decretos regionales',
                                  'Resoluciones regionales',
                                  'Ordenanzas regionales',
                                  'Directivas'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Locales conforman el nivel de '
                             'gobierno del Estado número:',
                 'alternativas': ['Primero',
                                  'Tercero',
                                  'Segundo',
                                  'Cuarto',
                                  'Quinto'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Locales también se denominan '
                             'municipalidades, y pueden ser provinciales o:',
                 'alternativas': ['Regionales',
                                  'Distritales',
                                  'Nacionales',
                                  'Departamentales',
                                  'Metropolitanas exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los alcaldes son elegidos por sufragio directo '
                             'por un periodo de:',
                 'alternativas': ['Tres años',
                                  'Cuatro años',
                                  'Cinco años',
                                  'Seis años',
                                  'Dos años'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura orgánica básica de las '
                             'municipalidades está compuesta por el Concejo '
                             'Municipal y:',
                 'alternativas': ['El Consejo Regional',
                                  'La Alcaldía',
                                  'La Gerencia General',
                                  'El Consejo de Coordinación exclusivo',
                                  'La Junta Vecinal exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El Concejo Municipal está conformado por el '
                             'alcalde y:',
                 'alternativas': ['Los gerentes municipales',
                                  'Los regidores',
                                  'Los vecinos elegidos',
                                  'El gobernador regional',
                                  'Los jueces de paz'],
                 'correcta': 'B'},
                {'pregunta': 'La Alcaldía es el órgano ejecutivo del '
                             'gobierno local; el alcalde es el representante '
                             'legal y su:',
                 'alternativas': ['Consultor externo',
                                  'Máxima autoridad administrativa',
                                  'Asesor jurídico',
                                  'Vocero exclusivo',
                                  'Fiscalizador'],
                 'correcta': 'B'},
                {'pregunta': 'Los mecanismos de participación ciudadana '
                             'municipal incluyen el Consejo de Coordinación '
                             'Local y:',
                 'alternativas': ['El Congreso Local',
                                  'Las Juntas de Delegados Vecinales',
                                  'El Poder Judicial Local',
                                  'La Fiscalía Municipal',
                                  'El Tribunal Municipal'],
                 'correcta': 'B'}]},
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
                {'titulo': '16.5 CLASIFICACIÓN POR GENERACIONES',
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
                           'la {paz}.']}],
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
                 'alternativas': ['Su edad',
                                  'Su nivel económico',
                                  'Su nacionalidad',
                                  'Su condición humana',
                                  'Su religión'],
                 'correcta': 'D'},
                {'pregunta': 'Según Hernández Gómez, los derechos humanos '
                             'son condiciones que permiten a la persona:',
                 'alternativas': ['Su realización',
                                  'Su exclusión social',
                                  'Su dependencia del Estado',
                                  'Su aislamiento',
                                  'Su sometimiento'],
                 'correcta': 'A'},
                {'pregunta': 'Que los derechos humanos se apliquen a todos '
                             'sin distinción corresponde a la característica '
                             'de:',
                 'alternativas': ['Universalidad',
                                  'Progresividad',
                                  'Imprescriptibilidad',
                                  'Obligatoriedad',
                                  'Indivisibilidad'],
                 'correcta': 'A'},
                {'pregunta': 'Que los derechos humanos no se pierdan con el '
                             'paso del tiempo corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Inviolables',
                                  'Universales',
                                  'Indisolubles',
                                  'Imprescriptibles'],
                 'correcta': 'E'},
                {'pregunta': 'Que no se pueda hablar de una división de los '
                             'derechos humanos corresponde a que son:',
                 'alternativas': ['Obligatorios',
                                  'Indivisibles',
                                  'Progresivos',
                                  'Irreversibles',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Que nadie pueda atentar contra los derechos '
                             'humanos corresponde a que son:',
                 'alternativas': ['Inviolables',
                                  'Indisolubles',
                                  'Progresivos',
                                  'Universales',
                                  'Imprescriptibles'],
                 'correcta': 'A'},
                {'pregunta': 'Que un derecho reconocido quede integrado de '
                             'forma irrevocable corresponde a que son:',
                 'alternativas': ['Obligatorios',
                                  'Irreversibles',
                                  'Progresivos',
                                  'Indivisibles',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos formen un conjunto '
                             'inseparable corresponde a que son:',
                 'alternativas': ['Indisolubles',
                                  'Inviolables',
                                  'Imprescriptibles',
                                  'Universales',
                                  'Progresivos'],
                 'correcta': 'A'},
                {'pregunta': 'Que el Estado deba respetar los derechos '
                             'humanos aunque no exista ley expresa '
                             'corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Irreversibles',
                                  'Universales',
                                  'Indivisibles',
                                  'Obligatorios'],
                 'correcta': 'E'},
                {'pregunta': 'Que puedan reconocerse nuevos derechos humanos '
                             'en el futuro corresponde a que son:',
                 'alternativas': ['Indisolubles',
                                  'Imprescriptibles',
                                  'Inviolables',
                                  'Progresivos',
                                  'Universales'],
                 'correcta': 'D'},
                {'pregunta': 'La evolución de los derechos humanos comprende '
                             'dos grandes momentos: la juridificación y:',
                 'alternativas': ['La privatización',
                                  'La internacionalización',
                                  'La militarización',
                                  'La regionalización',
                                  'La secularización'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta Magna, o Petición de los Derechos, se '
                             'dio en Inglaterra en el año:',
                 'alternativas': ['1948', '1789', '1776', '1215', '1679'],
                 'correcta': 'D'},
                {'pregunta': 'La Ley de Habeas Corpus fue dictada en '
                             'Inglaterra en:',
                 'alternativas': ['1679', '1948', '1789', '1215', '1776'],
                 'correcta': 'A'},
                {'pregunta': 'El Acta de Independencia de Estados Unidos '
                             'data de:',
                 'alternativas': ['1789', '1776', '1215', '1679', '1948'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano corresponde a:',
                 'alternativas': ['Alemania, 1919',
                                  'España, 1812',
                                  'Inglaterra, 1215',
                                  'Francia, 1789',
                                  'Estados Unidos, 1776'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de juridificación se caracteriza '
                             'porque los nuevos Estados modernos:',
                 'alternativas': ['Prohibieron su difusión',
                                  'Centralizaron el poder absoluto',
                                  'Rechazaron los derechos humanos',
                                  'Introdujeron el reconocimiento y '
                                  'protección de estos derechos en sus '
                                  'legislaciones',
                                  'Eliminaron toda garantía legal'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de juridificación estuvo imbuido de '
                             'la ideología:',
                 'alternativas': ['Monárquica',
                                  'Absolutista',
                                  'Liberal',
                                  'Conservadora',
                                  'Socialista'],
                 'correcta': 'C'},
                {'pregunta': 'El ejercicio de rebeliones históricas para '
                             'lograr el reconocimiento de derechos demuestra '
                             'que estos son, en parte:',
                 'alternativas': ['Producto de un proceso histórico y social',
                                  'Exclusivos de una nación',
                                  'Impuestos por organismos internacionales',
                                  'Otorgados sin lucha por el Estado',
                                  'Ajenos a la evolución humana'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho a la vida, como derecho inviolable, '
                             'no puede ser violentado:',
                 'alternativas': ['En ninguna circunstancia',
                                  'Solo por decisión judicial',
                                  'Solo temporalmente',
                                  'Solo en situaciones de guerra',
                                  'Bajo excepciones económicas'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos humanos, según su carácter '
                             'obligatorio, deben respetarse:',
                 'alternativas': ['Aunque no exista una ley que lo diga '
                                  'expresamente',
                                  'Solo en situaciones normales',
                                  'Solo si están en la ley nacional',
                                  'Solo si lo exige un tratado',
                                  'Solo por decisión del gobierno de turno'],
                 'correcta': 'A'},
                {'pregunta': 'La división de los derechos humanos en tres '
                             'generaciones fue propuesta en 1979 por:',
                 'alternativas': ['Norberto Bobbio',
                                  'Karel Vasak',
                                  'Hans Kelsen',
                                  'John Rawls',
                                  'Rousseau'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de primera generación consideran '
                             'a la persona como:',
                 'alternativas': ['Un grupo social',
                                  'Un individuo con libertad y autonomía',
                                  'Un sujeto colectivo',
                                  'Una nación',
                                  'Un pueblo indígena'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de primera generación también se '
                             'conocen como derechos:',
                 'alternativas': ['Económicos y sociales',
                                  'Civiles y políticos',
                                  'De solidaridad',
                                  'Colectivos',
                                  'Difusos'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho más importante entre los de primera '
                             'generación es el derecho a:',
                 'alternativas': ['La propiedad',
                                  'La vida',
                                  'El trabajo',
                                  'La paz',
                                  'La sindicación'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú ratificó el Pacto Internacional de '
                             'Derechos Civiles y Políticos mediante Decreto '
                             'Ley N°:',
                 'alternativas': ['22128',
                                  '26300',
                                  '28237',
                                  '27444',
                                  '25278'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de segunda generación son '
                             'derechos económicos, sociales y:',
                 'alternativas': ['Difusos',
                                  'Culturales',
                                  'Colectivos exclusivos',
                                  'De solidaridad exclusiva',
                                  'Ambientales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'La instauración de los derechos de segunda '
                             'generación provocó la sustitución del Estado '
                             'Liberal por el Estado:',
                 'alternativas': ['Absolutista',
                                  'Social de Derecho',
                                  'Totalitario',
                                  'Confesional',
                                  'Militar'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los derechos de segunda generación está '
                             'el derecho al trabajo y a la libre:',
                 'alternativas': ['Emigración',
                                  'Sindicación',
                                  'Herencia',
                                  'Propiedad',
                                  'Religión'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de tercera generación también se '
                             'llaman derechos de:',
                 'alternativas': ['Libertad',
                                  'Solidaridad',
                                  'Propiedad',
                                  'Autonomía individual',
                                  'Igualdad'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos de tercera generación se '
                             'reconocen a partir de la década de:',
                 'alternativas': ['1960', '1980', '1945', '1990', '1970'],
                 'correcta': 'B'},
                {'pregunta': 'Los titulares de los derechos de tercera '
                             'generación son sujetos:',
                 'alternativas': ['Individuales exclusivamente',
                                  'Colectivos',
                                  'Estatales exclusivamente',
                                  'Empresariales',
                                  'Religiosos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los derechos de tercera generación está '
                             'la autodeterminación de los pueblos y la '
                             'protección de:',
                 'alternativas': ['La propiedad privada',
                                  'El medio ambiente',
                                  'El comercio',
                                  'La banca',
                                  'Las telecomunicaciones'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos humanos pueden conceptualizarse '
                             'desde cuatro dimensiones: histórica, ética, '
                             'política y:',
                 'alternativas': ['Económica',
                                  'Jurídica',
                                  'Social exclusiva',
                                  'Cultural exclusiva',
                                  'Religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'La dimensión de los derechos humanos que se '
                             'fundamenta en valores como la dignidad y la '
                             'libertad se llama dimensión:',
                 'alternativas': ['Histórica',
                                  'Ética',
                                  'Jurídica',
                                  'Política',
                                  'Social'],
                 'correcta': 'B'},
                {'pregunta': 'La dimensión de los derechos humanos que '
                             'refiere a su proclamación por la ONU se llama '
                             'dimensión:',
                 'alternativas': ['Ética',
                                  'Política',
                                  'Jurídica',
                                  'Histórica',
                                  'Económica'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Una obligación tributaria',
                                  'Un peligro en el disfrute de los derechos',
                                  'Un beneficio',
                                  'Una sanción administrativa',
                                  'Un contrato civil'],
                 'correcta': 'B'},
                {'pregunta': 'Las Garantías Constitucionales tienen su '
                             'origen en la tradición:',
                 'alternativas': ['Romana',
                                  'Española',
                                  'Inglesa',
                                  'Francesa',
                                  'Alemana'],
                 'correcta': 'D'},
                {'pregunta': 'En el Perú, la institucionalidad de las '
                             'garantías se inicia con la Constitución de:',
                 'alternativas': ['1993', '1920', '1856', '1933', '1979'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución de 1920 distinguió tres tipos '
                             'de garantías: nacionales, individuales y:',
                 'alternativas': ['Sociales',
                                  'Religiosas',
                                  'Militares',
                                  'Culturales',
                                  'Económicas'],
                 'correcta': 'A'},
                {'pregunta': 'Según García Toma, las Garantías '
                             'Constitucionales aseguran el disfrute de los '
                             'derechos:',
                 'alternativas': ['Solo económicos',
                                  'Solo privados',
                                  'Públicos y privados',
                                  'Solo políticos',
                                  'Solo públicos'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'establece las Garantías Constitucionales es '
                             'el:',
                 'alternativas': ['Artículo 149',
                                  'Artículo 200',
                                  'Artículo 24',
                                  'Artículo 91',
                                  'Artículo 51'],
                 'correcta': 'B'},
                {'pregunta': 'El número de Garantías Constitucionales '
                             'establecidas en el artículo 200 es:',
                 'alternativas': ['Seis', 'Tres', 'Cuatro', 'Ocho', 'Diez'],
                 'correcta': 'A'},
                {'pregunta': 'La primera garantía constitucional reconocida '
                             'en el Perú, en 1920, fue:',
                 'alternativas': ['El Habeas Corpus',
                                  'La Acción de Amparo',
                                  'La Acción Popular',
                                  'La Acción de Cumplimiento',
                                  'El Habeas Data'],
                 'correcta': 'A'},
                {'pregunta': 'La Acción Popular fue incorporada en la '
                             'Constitución de:',
                 'alternativas': ['1979', '1920', '1993', '1856', '1933'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción de Amparo y la Acción de '
                             'Inconstitucionalidad se incorporaron en la '
                             'Constitución de:',
                 'alternativas': ['1856', '1993', '1979', '1920', '1933'],
                 'correcta': 'C'},
                {'pregunta': 'El Habeas Data y la Acción de Cumplimiento se '
                             'incorporaron en la Constitución de:',
                 'alternativas': ['1979', '1920', '1856', '1933', '1993'],
                 'correcta': 'E'},
                {'pregunta': 'La expresión «habeas corpus» significa '
                             'literalmente:',
                 'alternativas': ['Libertad total',
                                  'Protege al pueblo',
                                  'Que traigas el cuerpo',
                                  'Derecho supremo',
                                  'Justicia inmediata'],
                 'correcta': 'C'},
                {'pregunta': 'El antecedente histórico del habeas corpus es '
                             'la ley inglesa de:',
                 'alternativas': ['1215', '1679', '1948', '1993', '1789'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus protege principalmente:',
                 'alternativas': ['Los derechos laborales exclusivamente',
                                  'El comercio exterior',
                                  'La libertad individual y la seguridad '
                                  'personal',
                                  'La propiedad privada',
                                  'La libertad de prensa únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'El habeas corpus se presenta, en primera '
                             'instancia, ante:',
                 'alternativas': ['El Juez especializado en lo Penal',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'El Ministerio Público',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'A'},
                {'pregunta': 'Si no hay Juez Penal disponible, el habeas '
                             'corpus se presenta ante:',
                 'alternativas': ['El Alcalde',
                                  'El Presidente de la Corte Suprema',
                                  'El Fiscal de la Nación',
                                  'El Defensor del Pueblo',
                                  'El Juez de Paz Letrado'],
                 'correcta': 'E'},
                {'pregunta': 'La última y definitiva instancia para resolver '
                             'denegatorias de habeas corpus es:',
                 'alternativas': ['La Defensoría del Pueblo',
                                  'El Ministerio Público',
                                  'El Tribunal Constitucional',
                                  'La Corte Suprema',
                                  'El Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'La acción de habeas corpus se caracteriza por '
                             'estar exenta de:',
                 'alternativas': ['Competencia territorial',
                                  'Revisión judicial',
                                  'Sustento fáctico',
                                  'Formalidades',
                                  'Plazos procesales'],
                 'correcta': 'D'},
                {'pregunta': 'Para presentar un habeas corpus NO se '
                             'requiere:',
                 'alternativas': ['Un hecho vulnerador',
                                  'Poder, tasas judiciales ni firma de '
                                  'letrado',
                                  'Identificar a la autoridad responsable',
                                  'Señalar el derecho vulnerado',
                                  'Presentar el escrito ante juez '
                                  'competente'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus puede formularse:',
                 'alternativas': ['Solo por escrito con abogado',
                                  'Únicamente en audiencia pública',
                                  'Solo mediante representante legal',
                                  'Exclusivamente por vía electrónica',
                                  'Por escrito o verbalmente, en forma '
                                  'directa o por correo'],
                 'correcta': 'E'},
                {'pregunta': 'La Acción de Amparo fue introducida por '
                             'primera vez, como garantía distinta al hábeas '
                             'corpus, en la Constitución de:',
                 'alternativas': ['1933', '1979', '1993', '1920', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Amparo protege todos los derechos '
                             'constitucionales, excepto los protegidos por '
                             'hábeas corpus y:',
                 'alternativas': ['Acción popular',
                                  'Hábeas data',
                                  'Inconstitucionalidad',
                                  'Cumplimiento',
                                  'Proceso competencial'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para presentar la Acción de Amparo es '
                             'de 60 días desde la vulneración del derecho, '
                             'salvo en sentencias judiciales, donde el plazo '
                             'es de:',
                 'alternativas': ['15 días',
                                  '30 días',
                                  '45 días',
                                  '90 días',
                                  '10 días'],
                 'correcta': 'B'},
                {'pregunta': 'El Hábeas Data fue introducido por la '
                             'Constitución de:',
                 'alternativas': ['1979', '1993', '1933', '1920', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'El Hábeas Data protege el derecho a solicitar '
                             'y recibir información, y la protección de la '
                             'intimidad:',
                 'alternativas': ['Comercial',
                                  'Personal y familiar',
                                  'Empresarial',
                                  'Política',
                                  'Religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para presentar el Hábeas Data es de '
                             '60 días hábiles después de:',
                 'alternativas': ['La sentencia judicial',
                                  'La respuesta denegatoria',
                                  'La publicación de la norma',
                                  'El acto administrativo',
                                  'La notificación fiscal'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Inconstitucionalidad se crea con '
                             'la Constitución de:',
                 'alternativas': ['1933', '1979', '1993', '1856', '1920'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Inconstitucionalidad es la única '
                             'garantía que se presenta en:',
                 'alternativas': ['Primera instancia',
                                  'Instancia única y definitiva',
                                  'Tres instancias',
                                  'Doble instancia',
                                  'Instancia administrativa'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los facultados para interponer Acción de '
                             'Inconstitucionalidad está un grupo de '
                             'ciudadanos con firmas comprobadas por el JNE, '
                             'en número no menor a:',
                 'alternativas': ['1000', '5000', '500', '10000', '2000'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para interponer una Acción de '
                             'Inconstitucionalidad es de 6 años desde su '
                             'publicación, y en tratados internacionales el '
                             'plazo es de:',
                 'alternativas': ['3 meses',
                                  '6 meses',
                                  '1 año',
                                  '2 años',
                                  '6 años también'],
                 'correcta': 'B'},
                {'pregunta': 'Para resolver la Acción de '
                             'Inconstitucionalidad se requiere el voto a '
                             'favor de un número de magistrados del Tribunal '
                             'Constitucional igual a:',
                 'alternativas': ['3', '5', '7', '4', '6'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción Popular se originó en la justicia '
                             'romana y se introdujo por primera vez en la '
                             'Constitución de:',
                 'alternativas': ['1920', '1933', '1979', '1993', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción Popular procede contra normas de '
                             'rango de decretos y resoluciones, y es '
                             'competencia exclusiva de:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'El Congreso',
                                  'La Contraloría',
                                  'El Ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para interponer una Acción Popular es '
                             'de:',
                 'alternativas': ['3 años',
                                  '5 años',
                                  '6 años',
                                  '10 años',
                                  '1 año'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Cumplimiento fue creada por la '
                             'Constitución de:',
                 'alternativas': ['1979', '1993', '1933', '1920', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Cumplimiento sirve para hacer '
                             'cumplir normas legales o:',
                 'alternativas': ['Sentencias privadas',
                                  'Actos administrativos',
                                  'Contratos comerciales',
                                  'Decisiones empresariales',
                                  'Reglamentos internos'],
                 'correcta': 'B'},
                {'pregunta': 'El plazo para presentar la Acción de '
                             'Cumplimiento es de 60 días después de:',
                 'alternativas': ['La publicación de la norma',
                                  'No haberse cumplido el mandato',
                                  'La demanda inicial',
                                  'La sentencia',
                                  'La notificación fiscal'],
                 'correcta': 'B'}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La organización precursora de las Naciones '
                           'Unidas fue {La Sociedad de Naciones}.',
                           'La Sociedad de Naciones se estableció en el año '
                           '{1919}.',
                           'La Sociedad de Naciones se estableció en virtud '
                           'del Tratado de {Versalles}.',
                           'El fracaso de la Sociedad de Naciones desembocó '
                           'en {La Segunda Guerra Mundial}.',
                           'El nombre «Naciones Unidas» fue acuñado por '
                           '{Franklin D. Roosevelt}.',
                           'El nombre «Naciones Unidas» se usó por primera '
                           'vez en {1942}.',
                           'La Carta de las Naciones Unidas fue firmada el '
                           '26 de junio de {1945}.',
                           'La Carta de la ONU fue firmada inicialmente por '
                           '{50 países}.',
                           'Las Naciones Unidas empezaron a existir '
                           'oficialmente el {24 de octubre de 1945}.',
                           'El 24 de octubre se celebra como {El Día de las '
                           'Naciones Unidas}.',
                           'La ONU tiene actualmente un número de Estados '
                           'Miembros de {193}.',
                           'La sede principal de la ONU se ubica en {Nueva '
                           'York}.',
                           'Entre las sedes secundarias de la ONU figura '
                           '{Ginebra}.',
                           'Los idiomas oficiales de la ONU son seis, entre '
                           'ellos figura {El árabe}.',
                           'La ONU está compuesta por un número de órganos '
                           'principales igual a {Seis}.',
                           'El órgano de la ONU encargado de la paz y '
                           'seguridad internacional es {El Consejo de '
                           'Seguridad}.',
                           'El órgano judicial principal de la ONU es {La '
                           'Corte Internacional de Justicia}.',
                           'Entre los fines de la ONU figura defender y '
                           'garantizar {Los Derechos Humanos}.',
                           'Un Estado que infringe los principios de la '
                           'Carta de la ONU puede ser {Excluido '
                           'temporalmente o expulsado}.',
                           'Estados no miembros de la ONU, como el Vaticano, '
                           'pueden tener estatuto de {Observador, sin '
                           'derecho a voto}.']}],
  'cuadros': [{'titulo': '18.3 ÓRGANOS PRINCIPALES DE LA ONU',
               'encabezados': ['N°', 'Órgano'],
               'filas': [['1', '{Asamblea} General'],
                         ['2', '{Secretario} General'],
                         ['3', '{Consejo} de Seguridad'],
                         ['4', 'Consejo {Económico} y Social'],
                         ['5', '{Corte Internacional} de Justicia']]}],
  'preguntas': [{'pregunta': 'La organización precursora de las Naciones '
                             'Unidas fue:',
                 'alternativas': ['La OTAN',
                                  'La OEA',
                                  'El Pacto Andino',
                                  'La Sociedad de Naciones',
                                  'La Cruz Roja'],
                 'correcta': 'D'},
                {'pregunta': 'La Sociedad de Naciones se estableció en el '
                             'año:',
                 'alternativas': ['1939', '1945', '1914', '1918', '1919'],
                 'correcta': 'E'},
                {'pregunta': 'La Sociedad de Naciones se estableció en '
                             'virtud del Tratado de:',
                 'alternativas': ['Ginebra',
                                  'Versalles',
                                  'Ancón',
                                  'Roma',
                                  'Westfalia'],
                 'correcta': 'B'},
                {'pregunta': 'El fracaso de la Sociedad de Naciones '
                             'desembocó en:',
                 'alternativas': ['La Segunda Guerra Mundial',
                                  'La Revolución Rusa',
                                  'La Guerra de Corea',
                                  'La Primera Guerra Mundial',
                                  'La Guerra Fría'],
                 'correcta': 'A'},
                {'pregunta': 'El nombre «Naciones Unidas» fue acuñado por:',
                 'alternativas': ['Woodrow Wilson',
                                  'Franklin D. Roosevelt',
                                  'Winston Churchill',
                                  'Joseph Stalin',
                                  'Harry Truman'],
                 'correcta': 'B'},
                {'pregunta': 'El nombre «Naciones Unidas» se usó por primera '
                             'vez en:',
                 'alternativas': ['1919', '1942', '1950', '1939', '1945'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta de las Naciones Unidas fue firmada el '
                             '26 de junio de:',
                 'alternativas': ['1919', '1950', '1939', '1945', '1942'],
                 'correcta': 'D'},
                {'pregunta': 'La Carta de la ONU fue firmada inicialmente '
                             'por:',
                 'alternativas': ['50 países',
                                  '193 países',
                                  '10 países',
                                  '26 países',
                                  '100 países'],
                 'correcta': 'A'},
                {'pregunta': 'Las Naciones Unidas empezaron a existir '
                             'oficialmente el:',
                 'alternativas': ['1 de enero de 1945',
                                  '24 de octubre de 1945',
                                  '1 de enero de 1942',
                                  '26 de junio de 1945',
                                  '10 de diciembre de 1948'],
                 'correcta': 'B'},
                {'pregunta': 'El 24 de octubre se celebra como:',
                 'alternativas': ['El Día de la Democracia',
                                  'El Día de la Paz Mundial',
                                  'El Día de las Naciones Unidas',
                                  'El Día del Multilateralismo',
                                  'El Día de los Derechos Humanos'],
                 'correcta': 'C'},
                {'pregunta': 'La ONU tiene actualmente un número de Estados '
                             'Miembros de:',
                 'alternativas': ['150', '100', '250', '51', '193'],
                 'correcta': 'E'},
                {'pregunta': 'La sede principal de la ONU se ubica en:',
                 'alternativas': ['París',
                                  'Viena',
                                  'Ginebra',
                                  'Nairobi',
                                  'Nueva York'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las sedes secundarias de la ONU figura:',
                 'alternativas': ['Berlín',
                                  'Ginebra',
                                  'Londres',
                                  'Roma',
                                  'Madrid'],
                 'correcta': 'B'},
                {'pregunta': 'Los idiomas oficiales de la ONU son seis, '
                             'entre ellos figura:',
                 'alternativas': ['El italiano',
                                  'El japonés',
                                  'El portugués',
                                  'El alemán',
                                  'El árabe'],
                 'correcta': 'E'},
                {'pregunta': 'La ONU está compuesta por un número de órganos '
                             'principales igual a:',
                 'alternativas': ['Tres', 'Ocho', 'Cuatro', 'Seis', 'Diez'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano de la ONU encargado de la paz y '
                             'seguridad internacional es:',
                 'alternativas': ['El Secretario General',
                                  'El Consejo Económico y Social',
                                  'La Corte Internacional de Justicia',
                                  'El Consejo de Seguridad',
                                  'La Asamblea General'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano judicial principal de la ONU es:',
                 'alternativas': ['La Corte Internacional de Justicia',
                                  'El Consejo Económico y Social',
                                  'El Consejo de Seguridad',
                                  'La Asamblea General',
                                  'El Consejo de Administración Fiduciaria'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los fines de la ONU figura defender y '
                             'garantizar:',
                 'alternativas': ['Los Derechos Humanos',
                                  'Solo el comercio internacional',
                                  'Solo el turismo',
                                  'Solo la seguridad militar',
                                  'Solo la moneda internacional'],
                 'correcta': 'A'},
                {'pregunta': 'Un Estado que infringe los principios de la '
                             'Carta de la ONU puede ser:',
                 'alternativas': ['Ignorado sin consecuencias',
                                  'Premiado',
                                  'Anexado a otro país',
                                  'Excluido temporalmente o expulsado',
                                  'Automáticamente disuelto'],
                 'correcta': 'D'},
                {'pregunta': 'Estados no miembros de la ONU, como el '
                             'Vaticano, pueden tener estatuto de:',
                 'alternativas': ['Fundador',
                                  'Excluido total',
                                  'Miembro pleno',
                                  'Observador, sin derecho a voto',
                                  'Sancionado permanente'],
                 'correcta': 'D'}]}]
