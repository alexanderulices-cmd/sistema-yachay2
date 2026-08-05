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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['En sentido amplio, el Estado se define como {La '
                           'nación jurídicamente organizada}.',
                           'Los elementos del Estado son población, '
                           'territorio, organización jurídica y {Soberanía}.',
                           'El territorio del Estado se caracteriza por ser '
                           'inalienable e {Inviolable}.',
                           'Según el artículo 54 de la Constitución, el '
                           'territorio comprende el suelo, el subsuelo, el '
                           'espacio aéreo y {El mar territorial}.',
                           'La organización jurídica de un Estado está '
                           'integrada por {La Constitución, leyes y '
                           'decretos}.',
                           'La soberanía interna del Estado implica '
                           '{Supremacía sobre los demás poderes del '
                           'territorio}.',
                           'La soberanía externa permite al Estado '
                           '{Relacionarse con otros Estados soberanos como '
                           'igual}.',
                           'El Estado Constitucional surgió en {Inglaterra}.',
                           'El Estado Constitucional surgió con el objetivo '
                           'de {Limitar las decisiones de los monarcas '
                           'absolutos}.',
                           'El Estado Liberal se desarrolló principalmente '
                           'durante el siglo {XIX}.',
                           'Un pilar del Estado Liberal es {La propiedad '
                           'privada y la economía de mercado}.',
                           'En la democracia liberal o representativa, las '
                           'decisiones las toman {Representantes elegidos}.',
                           'En los Estados de partido único, se considera '
                           'legítima expresión de la voluntad general {Un '
                           'único partido}.',
                           'El Estado unitario se caracteriza por reconocer '
                           'como fuente de soberanía {Una sola nación}.',
                           'En un Estado unitario existe {Un solo gobierno, '
                           'un parlamento y un poder judicial}.',
                           'El Perú, según su estructura política, es un '
                           'Estado {Unitario}.',
                           'La población del Estado está constituida por '
                           '{Los habitantes organizados políticamente}.',
                           'El pueblo, dentro de los elementos del Estado, '
                           'se caracteriza por ser {Soberano e '
                           'independiente}.',
                           'Sin la organización jurídica, el Estado '
                           '{Carecería de forma}.',
                           'El Estado, en sentido restringido, se refiere a '
                           '{El conjunto de organismos que ejercen el '
                           'poder}.']}],
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
                 'alternativas': ['Un territorio delimitado',
                                  'La nación jurídicamente organizada',
                                  'Un conjunto de ciudadanos',
                                  'Un gobierno de turno',
                                  'Una constitución escrita'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos del Estado son población, '
                             'territorio, organización jurídica y:',
                 'alternativas': ['Economía',
                                  'Soberanía',
                                  'Cultura',
                                  'Idioma',
                                  'Religión'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio del Estado se caracteriza por '
                             'ser inalienable e:',
                 'alternativas': ['Ilimitado',
                                  'Inviolable',
                                  'Divisible',
                                  'Negociable',
                                  'Transferible'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 54 de la Constitución, el '
                             'territorio comprende el suelo, el subsuelo, el '
                             'espacio aéreo y:',
                 'alternativas': ['El espacio exterior',
                                  'El mar territorial',
                                  'Las fronteras vecinas',
                                  'El aire internacional',
                                  'Solo el litoral'],
                 'correcta': 'B'},
                {'pregunta': 'La organización jurídica de un Estado está '
                             'integrada por:',
                 'alternativas': ['Solo la Constitución',
                                  'La Constitución, leyes y decretos',
                                  'Solo el Poder Judicial',
                                  'Los tratados internacionales únicamente',
                                  'Las costumbres sociales'],
                 'correcta': 'B'},
                {'pregunta': 'La soberanía interna del Estado implica:',
                 'alternativas': ['Relacionarse con otros Estados',
                                  'Supremacía sobre los demás poderes del '
                                  'territorio',
                                  'Ceder autoridad a otros países',
                                  'Depender de organismos internacionales',
                                  'No tener autoridad propia'],
                 'correcta': 'B'},
                {'pregunta': 'La soberanía externa permite al Estado:',
                 'alternativas': ['Imponerse sobre otros Estados',
                                  'Relacionarse con otros Estados soberanos '
                                  'como igual',
                                  'Anexar territorios vecinos',
                                  'Ignorar el derecho internacional',
                                  'Actuar sin reconocer a otros Estados'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado Constitucional surgió en:',
                 'alternativas': ['Francia',
                                  'Inglaterra',
                                  'España',
                                  'Alemania',
                                  'Estados Unidos'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado Constitucional surgió con el '
                             'objetivo de:',
                 'alternativas': ['Fortalecer al monarca absoluto',
                                  'Limitar las decisiones de los monarcas '
                                  'absolutos',
                                  'Eliminar toda forma de gobierno',
                                  'Crear un imperio',
                                  'Unificar territorios'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado Liberal se desarrolló principalmente '
                             'durante el siglo:',
                 'alternativas': ['XVII', 'XIX', 'XV', 'XX', 'XVIII'],
                 'correcta': 'B'},
                {'pregunta': 'Un pilar del Estado Liberal es:',
                 'alternativas': ['La propiedad colectiva obligatoria',
                                  'La propiedad privada y la economía de '
                                  'mercado',
                                  'La censura estatal',
                                  'El partido único',
                                  'La monarquía absoluta'],
                 'correcta': 'B'},
                {'pregunta': 'En la democracia liberal o representativa, las '
                             'decisiones las toman:',
                 'alternativas': ['Todos los ciudadanos directamente',
                                  'Representantes elegidos',
                                  'Solo el presidente',
                                  'Un consejo religioso',
                                  'Los militares'],
                 'correcta': 'B'},
                {'pregunta': 'En los Estados de partido único, se considera '
                             'legítima expresión de la voluntad general:',
                 'alternativas': ['Cualquier partido político',
                                  'Un único partido',
                                  'Los sindicatos',
                                  'Las asambleas populares',
                                  'Las ONG'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado unitario se caracteriza por '
                             'reconocer como fuente de soberanía:',
                 'alternativas': ['Varias naciones',
                                  'Una sola nación',
                                  'Ninguna nación específica',
                                  'Organismos internacionales',
                                  'Solo las regiones'],
                 'correcta': 'B'},
                {'pregunta': 'En un Estado unitario existe:',
                 'alternativas': ['Varios gobiernos regionales autónomos',
                                  'Un solo gobierno, un parlamento y un '
                                  'poder judicial',
                                  'Solo gobiernos locales',
                                  'Ningún poder judicial central',
                                  'Múltiples constituciones'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú, según su estructura política, es un '
                             'Estado:',
                 'alternativas': ['Federal',
                                  'Unitario',
                                  'Confederado',
                                  'Sin forma definida',
                                  'Monárquico'],
                 'correcta': 'B'},
                {'pregunta': 'La población del Estado está constituida por:',
                 'alternativas': ['Solo los ciudadanos con derecho a voto',
                                  'Los habitantes organizados políticamente',
                                  'Solo los funcionarios públicos',
                                  'Solo los mayores de edad',
                                  'Únicamente los nacidos en el país'],
                 'correcta': 'B'},
                {'pregunta': 'El pueblo, dentro de los elementos del Estado, '
                             'se caracteriza por ser:',
                 'alternativas': ['Dependiente de otro Estado',
                                  'Soberano e independiente',
                                  'Subordinado al gobierno extranjero',
                                  'Sin organización',
                                  'Neutral políticamente'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la organización jurídica, el Estado:',
                 'alternativas': ['Funcionaría igual',
                                  'Carecería de forma',
                                  'Sería más eficiente',
                                  'Tendría más soberanía',
                                  'Se fortalecería'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, en sentido restringido, se refiere '
                             'a:',
                 'alternativas': ['Todo el territorio nacional',
                                  'El conjunto de organismos que ejercen el '
                                  'poder',
                                  'Solo la población',
                                  'La cultura nacional',
                                  'El idioma oficial'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La Constitución es considerada la fuente de '
                           'fuentes del Derecho {Positivo}.',
                           'La Constitución no está sujeta a evaluación de '
                           'validez formal porque {No existe un precepto '
                           'superior a ella}.',
                           'La Constitución es resultado del ejercicio del '
                           'Poder {Constituyente}.',
                           'El titular del Poder Constituyente es {El '
                           'pueblo}.',
                           'Según el artículo 51 de la Constitución, esta '
                           'prevalece sobre {Toda otra norma legal}.',
                           'El fin último de la Constitución, según el '
                           'texto, debe ser afianzar {La Justicia}.',
                           'El término latino «constitutio» fue introducido '
                           'por {Cicerón}.',
                           'Rousseau llamó «contrato social» a {La decisión '
                           'originaria del pueblo de fundar la comunidad '
                           'política}.',
                           'Vattel definió la Constitución como el '
                           'reglamento fundamental que determina {Cómo debe '
                           'ejercerse la autoridad pública}.',
                           'En 1776, el Congreso de Estados Unidos resolvió '
                           'que los Estados de la Confederación {Se dieran '
                           'sus propias Constituciones}.',
                           'El paso de la doctrina del derecho natural a la '
                           'teoría del Estado como contrato social se '
                           'atribuye a {Thomas Hobbes}.',
                           'John Locke explicaba que los individuos forman '
                           'una sociedad para {Beneficiarse mutuamente bajo '
                           'la protección del Estado y la ley}.',
                           'La división entre Constitución formal y material '
                           'fue establecida, entre otros, por {Kelsen}.',
                           'La Constitución peruana actualmente vigente data '
                           'del año {1993}.',
                           'La Constitución es descrita como la «norma de '
                           'normas» porque {Es la primera de las normas de '
                           'producción}.',
                           'Según Blancas Bustamante, la Constitución define '
                           'la posición de las personas frente al Estado '
                           'mediante {El reconocimiento de libertades y '
                           'derechos}.',
                           'La Declaración de los Derechos del Hombre y del '
                           'Ciudadano tuvo como fuente formal {Las '
                           'Constituciones de los Estados de la '
                           'Confederación norteamericana}.',
                           'En el siglo XVIII, se consideraba «todo el '
                           'pueblo» al llamado {Tercer Estado, compuesto por '
                           'la burguesía}.',
                           'Rousseau llamó «leyes fundamentales» a {La '
                           'estructura jurídica correspondiente al régimen '
                           'político}.',
                           'La Constitución constituye, define y crea los '
                           'poderes {Legislativo, ejecutivo y judicial}.']}],
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
                 'alternativas': ['Privado',
                                  'Positivo',
                                  'Consuetudinario',
                                  'Comparado',
                                  'Internacional únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución no está sujeta a evaluación de '
                             'validez formal porque:',
                 'alternativas': ['Es una ley ordinaria',
                                  'No existe un precepto superior a ella',
                                  'La aprueba el Poder Ejecutivo',
                                  'Es revisada cada año',
                                  'Depende de tratados internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución es resultado del ejercicio del '
                             'Poder:',
                 'alternativas': ['Legislativo ordinario',
                                  'Constituyente',
                                  'Ejecutivo',
                                  'Judicial',
                                  'Municipal'],
                 'correcta': 'B'},
                {'pregunta': 'El titular del Poder Constituyente es:',
                 'alternativas': ['El presidente',
                                  'El pueblo',
                                  'El Congreso',
                                  'El Tribunal Constitucional',
                                  'Los partidos políticos'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 51 de la Constitución, esta '
                             'prevalece sobre:',
                 'alternativas': ['Solo los decretos',
                                  'Toda otra norma legal',
                                  'Solo los tratados internacionales',
                                  'Nada en particular',
                                  'Solo las leyes penales'],
                 'correcta': 'B'},
                {'pregunta': 'El fin último de la Constitución, según el '
                             'texto, debe ser afianzar:',
                 'alternativas': ['El poder del Estado',
                                  'La Justicia',
                                  'La economía',
                                  'La religión oficial',
                                  'El comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El término latino «constitutio» fue '
                             'introducido por:',
                 'alternativas': ['Aristóteles',
                                  'Cicerón',
                                  'Platón',
                                  'Rousseau',
                                  'Montesquieu'],
                 'correcta': 'B'},
                {'pregunta': 'Rousseau llamó «contrato social» a:',
                 'alternativas': ['Un tratado comercial',
                                  'La decisión originaria del pueblo de '
                                  'fundar la comunidad política',
                                  'Una ley penal',
                                  'Un acuerdo entre monarcas',
                                  'Un pacto religioso'],
                 'correcta': 'B'},
                {'pregunta': 'Vattel definió la Constitución como el '
                             'reglamento fundamental que determina:',
                 'alternativas': ['Los impuestos del Estado',
                                  'Cómo debe ejercerse la autoridad pública',
                                  'El territorio del Estado',
                                  'La moneda oficial',
                                  'El idioma nacional'],
                 'correcta': 'B'},
                {'pregunta': 'En 1776, el Congreso de Estados Unidos '
                             'resolvió que los Estados de la Confederación:',
                 'alternativas': ['Se unificaran en un solo territorio',
                                  'Se dieran sus propias Constituciones',
                                  'Adoptaran la Constitución inglesa',
                                  'Eliminaran sus leyes',
                                  'Formaran una monarquía'],
                 'correcta': 'B'},
                {'pregunta': 'El paso de la doctrina del derecho natural a '
                             'la teoría del Estado como contrato social se '
                             'atribuye a:',
                 'alternativas': ['Rousseau',
                                  'Thomas Hobbes',
                                  'Montesquieu',
                                  'Locke exclusivamente',
                                  'Kelsen'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke explicaba que los individuos forman '
                             'una sociedad para:',
                 'alternativas': ['Someterse a un monarca absoluto',
                                  'Beneficiarse mutuamente bajo la '
                                  'protección del Estado y la ley',
                                  'Eliminar toda autoridad',
                                  'Vivir sin normas',
                                  'Depender de otro Estado'],
                 'correcta': 'B'},
                {'pregunta': 'La división entre Constitución formal y '
                             'material fue establecida, entre otros, por:',
                 'alternativas': ['Rousseau',
                                  'Kelsen',
                                  'Cicerón',
                                  'Vattel',
                                  'Bossuet'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución peruana actualmente vigente '
                             'data del año:',
                 'alternativas': ['1979', '1993', '1933', '1920', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución es descrita como la «norma de '
                             'normas» porque:',
                 'alternativas': ['Solo aplica al Poder Judicial',
                                  'Es la primera de las normas de producción',
                                  'Solo rige el comercio',
                                  'No tiene jerarquía superior a las leyes',
                                  'Es opcional para el Estado'],
                 'correcta': 'B'},
                {'pregunta': 'Según Blancas Bustamante, la Constitución '
                             'define la posición de las personas frente al '
                             'Estado mediante:',
                 'alternativas': ['Solo obligaciones tributarias',
                                  'El reconocimiento de libertades y '
                                  'derechos',
                                  'Solo sanciones penales',
                                  'Acuerdos comerciales',
                                  'Tratados internacionales exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano tuvo como fuente formal:',
                 'alternativas': ['La Constitución española',
                                  'Las Constituciones de los Estados de la '
                                  'Confederación norteamericana',
                                  'La Carta Magna inglesa',
                                  'El Código de Hammurabi',
                                  'La Constitución rusa'],
                 'correcta': 'B'},
                {'pregunta': 'En el siglo XVIII, se consideraba «todo el '
                             'pueblo» al llamado:',
                 'alternativas': ['Primer Estado',
                                  'Tercer Estado, compuesto por la burguesía',
                                  'Segundo Estado',
                                  'Cuarto Estado',
                                  'Estado eclesiástico'],
                 'correcta': 'B'},
                {'pregunta': 'Rousseau llamó «leyes fundamentales» a:',
                 'alternativas': ['La estructura de poder',
                                  'La estructura jurídica correspondiente al '
                                  'régimen político',
                                  'Los tratados internacionales',
                                  'Las costumbres sociales',
                                  'El derecho penal'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución constituye, define y crea los '
                             'poderes:',
                 'alternativas': ['Solo el legislativo',
                                  'Legislativo, ejecutivo y judicial',
                                  'Solo el ejecutivo',
                                  'Solo el judicial',
                                  'Ninguno en particular'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El PIDCP fue adoptado por la Asamblea General de '
                           'la ONU en el año {1966}.',
                           'El PIDCP entró en vigor el {23 de marzo de '
                           '1976}.',
                           'El PIDCP ha sido ratificado por un total de '
                           'Estados de {167}.',
                           'El PIDCP consta de un número de partes igual a '
                           '{6}.',
                           'El PIDCP consta de un número de artículos igual '
                           'a {53}.',
                           'El Primer Protocolo Facultativo del PIDCP regula '
                           '{Los mecanismos de denuncia contra los Estados}.',
                           'El Segundo Protocolo Facultativo del PIDCP está '
                           'destinado a {La abolición de la pena de muerte}.',
                           'Los derechos civiles se distinguen de los '
                           'derechos naturales porque son {Reconocidos '
                           'dentro de un Estado determinado}.',
                           'Los derechos naturales o humanos se poseen {Por '
                           'el mero hecho de nacer}.',
                           'John Locke sostuvo que debían convertirse en '
                           'derechos civiles protegidos por el Estado {La '
                           'vida, la libertad y la propiedad}.',
                           'El derecho considerado el primero de todos, '
                           'generador de cualquier otro derecho, es el '
                           'derecho a {La vida}.',
                           'El derecho a la integridad física y psicológica '
                           'protege contra {Las torturas y tratos crueles e '
                           'inhumanos}.',
                           'El derecho a la identidad comprende, entre otros '
                           'aspectos {El derecho a tener un nombre y '
                           'documento de identidad}.',
                           'Los derechos políticos permiten participar en '
                           '{El gobierno del Estado y la toma de '
                           'decisiones}.',
                           'Los derechos políticos están reconocidos por {La '
                           'Constitución y las leyes}.',
                           'La Parte III del PIDCP, artículos 6 a 27, '
                           'protege contra {La discriminación por sexo, '
                           'religión, raza u otras formas}.',
                           'La Parte I del PIDCP, artículo 1, trata sobre '
                           '{La libre determinación de los pueblos}.',
                           'El PIDCP es catalogado como un tratado '
                           'internacional de tipo {Multilateral general}.',
                           'La contraposición al derecho a la vida es {La '
                           'muerte}.',
                           'Entre los derechos civiles y políticos '
                           'mencionados figura el derecho a elegir y {Ser '
                           'elegido representante}.']}],
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
                 'alternativas': ['1948', '1966', '1976', '1993', '2000'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP entró en vigor el:',
                 'alternativas': ['16 de diciembre de 1966',
                                  '23 de marzo de 1976',
                                  '10 de diciembre de 1948',
                                  '1 de enero de 1980',
                                  '30 de abril de 1990'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP ha sido ratificado por un total de '
                             'Estados de:',
                 'alternativas': ['100', '167', '50', '200', '75'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP consta de un número de partes igual '
                             'a:',
                 'alternativas': ['4', '6', '8', '3', '10'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP consta de un número de artículos '
                             'igual a:',
                 'alternativas': ['30', '53', '100', '25', '75'],
                 'correcta': 'B'},
                {'pregunta': 'El Primer Protocolo Facultativo del PIDCP '
                             'regula:',
                 'alternativas': ['La abolición de la pena de muerte',
                                  'Los mecanismos de denuncia contra los '
                                  'Estados',
                                  'El comercio internacional',
                                  'Los derechos económicos',
                                  'La migración'],
                 'correcta': 'B'},
                {'pregunta': 'El Segundo Protocolo Facultativo del PIDCP '
                             'está destinado a:',
                 'alternativas': ['El mecanismo de denuncias',
                                  'La abolición de la pena de muerte',
                                  'La protección ambiental',
                                  'Los derechos laborales',
                                  'El comercio exterior'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos civiles se distinguen de los '
                             'derechos naturales porque son:',
                 'alternativas': ['Internacionales por naturaleza',
                                  'Reconocidos dentro de un Estado '
                                  'determinado',
                                  'Innatos al nacer',
                                  'Universales sin excepción',
                                  'Otorgados por organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos naturales o humanos se poseen:',
                 'alternativas': ['Solo si el Estado los otorga',
                                  'Por el mero hecho de nacer',
                                  'Solo a partir de la mayoría de edad',
                                  'Únicamente si se solicitan',
                                  'Solo en democracias'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke sostuvo que debían convertirse en '
                             'derechos civiles protegidos por el Estado:',
                 'alternativas': ['Solo el derecho a la propiedad',
                                  'La vida, la libertad y la propiedad',
                                  'Solo el derecho a la vida',
                                  'Los derechos económicos',
                                  'Los derechos culturales'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho considerado el primero de todos, '
                             'generador de cualquier otro derecho, es el '
                             'derecho a:',
                 'alternativas': ['La propiedad',
                                  'La vida',
                                  'La libertad de expresión',
                                  'La educación',
                                  'El trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho a la integridad física y '
                             'psicológica protege contra:',
                 'alternativas': ['Los impuestos elevados',
                                  'Las torturas y tratos crueles e inhumanos',
                                  'La libre expresión',
                                  'El comercio informal',
                                  'La migración'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho a la identidad comprende, entre '
                             'otros aspectos:',
                 'alternativas': ['El derecho al voto',
                                  'El derecho a tener un nombre y documento '
                                  'de identidad',
                                  'El derecho a la propiedad',
                                  'El derecho al trabajo',
                                  'El derecho a la educación superior'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos políticos permiten participar en:',
                 'alternativas': ['Solo actividades económicas',
                                  'El gobierno del Estado y la toma de '
                                  'decisiones',
                                  'Solo actividades religiosas',
                                  'El comercio internacional',
                                  'La vida privada únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos políticos están reconocidos por:',
                 'alternativas': ['Solo tratados internacionales',
                                  'La Constitución y las leyes',
                                  'Solo la costumbre',
                                  'Organismos privados',
                                  'Ninguna norma específica'],
                 'correcta': 'B'},
                {'pregunta': 'La Parte III del PIDCP, artículos 6 a 27, '
                             'protege contra:',
                 'alternativas': ['El comercio desleal',
                                  'La discriminación por sexo, religión, '
                                  'raza u otras formas',
                                  'La contaminación ambiental',
                                  'La evasión tributaria',
                                  'El desempleo'],
                 'correcta': 'B'},
                {'pregunta': 'La Parte I del PIDCP, artículo 1, trata sobre:',
                 'alternativas': ['La pena de muerte',
                                  'La libre determinación de los pueblos',
                                  'El comercio internacional',
                                  'Los tratados bilaterales',
                                  'La migración'],
                 'correcta': 'B'},
                {'pregunta': 'El PIDCP es catalogado como un tratado '
                             'internacional de tipo:',
                 'alternativas': ['Bilateral',
                                  'Multilateral general',
                                  'Regional exclusivo',
                                  'Comercial',
                                  'Privado'],
                 'correcta': 'B'},
                {'pregunta': 'La contraposición al derecho a la vida es:',
                 'alternativas': ['La enfermedad',
                                  'La muerte',
                                  'La pobreza',
                                  'La discapacidad',
                                  'El envejecimiento'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los derechos civiles y políticos '
                             'mencionados figura el derecho a elegir y:',
                 'alternativas': ['No votar',
                                  'Ser elegido representante',
                                  'Evadir impuestos',
                                  'No participar',
                                  'Rechazar la ciudadanía'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los derechos económicos, sociales y culturales '
                           'incluyen, entre otros, el derecho a {Un nivel de '
                           'vida adecuado, alimentación y vivienda digna}.',
                           'El Protocolo Adicional a la Convención Americana '
                           'en materia de derechos económicos, sociales y '
                           'culturales se conoce como {Protocolo de San '
                           'Salvador}.',
                           'Según Hakansson, estos derechos representan la '
                           'función del Estado de {Equilibrar las '
                           'desigualdades sociales}.',
                           'El valor básico que fundamenta todos los '
                           'derechos humanos es {La dignidad de la persona '
                           'humana}.',
                           'Según Nogueira, la dignidad humana fundamenta '
                           '{Tanto los derechos civiles y políticos como los '
                           'económicos, sociales y culturales}.',
                           'El artículo 22 de la Constitución establece que '
                           'el trabajo es {Un deber y un derecho}.',
                           'Según el artículo 22, el trabajo es la base de '
                           '{El bienestar social}.',
                           'El artículo 23 de la Constitución protege '
                           'especialmente a {A la madre, al menor de edad y '
                           'al impedido que trabajan}.',
                           'Según el artículo 23, ninguna relación laboral '
                           'puede {Limitar los derechos constitucionales ni '
                           'rebajar la dignidad del trabajador}.',
                           'Según la Constitución, nadie está obligado a '
                           'prestar trabajo {Sin retribución o sin su libre '
                           'consentimiento}.',
                           'El artículo 24 de la Constitución establece el '
                           'derecho del trabajador a {Una remuneración '
                           'equitativa y suficiente}.',
                           'El Estado promueve condiciones para el progreso '
                           'social y económico mediante {Políticas de '
                           'fomento del empleo productivo y educación para '
                           'el trabajo}.',
                           'La Declaración Universal de Derechos Humanos, en '
                           'su preámbulo, señala que todo individuo y órgano '
                           'de la sociedad debe {Promover el respeto a los '
                           'derechos humanos}.',
                           'Los derechos sociales y económicos buscan que '
                           'los ciudadanos gocen de {Un estado de '
                           'bienestar}.',
                           'Según el texto, la persona, en virtud de su '
                           'dignidad, se convierte en {El fin del Estado}.',
                           'El Estado, según Nogueira, está al servicio de '
                           '{La persona humana}.',
                           'La finalidad del Estado, según el texto, es '
                           'promover {El bien común}.',
                           'Entre los instrumentos con jerarquía '
                           'constitucional que contemplan estos derechos '
                           'figura {La Declaración Universal de Derechos '
                           'Humanos}.',
                           'El principio de dignidad humana implica que los '
                           'derechos se reconozcan {Sin distingo de tipo '
                           'cultural, económico o social}.',
                           'Los derechos sociales y económicos representan, '
                           'según el texto {Los fines sociales del '
                           'Estado}.']}],
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
                 'alternativas': ['Solo la propiedad privada',
                                  'Un nivel de vida adecuado, alimentación y '
                                  'vivienda digna',
                                  'Solo la libertad de tránsito',
                                  'Solo el sufragio',
                                  'Solo la nacionalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El Protocolo Adicional a la Convención '
                             'Americana en materia de derechos económicos, '
                             'sociales y culturales se conoce como:',
                 'alternativas': ['Protocolo de Ginebra',
                                  'Protocolo de San Salvador',
                                  'Protocolo de Lima',
                                  'Protocolo de Nueva York',
                                  'Protocolo de Roma'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hakansson, estos derechos representan la '
                             'función del Estado de:',
                 'alternativas': ['Aumentar impuestos',
                                  'Equilibrar las desigualdades sociales',
                                  'Reducir el gasto público',
                                  'Privatizar servicios',
                                  'Limitar la educación'],
                 'correcta': 'B'},
                {'pregunta': 'El valor básico que fundamenta todos los '
                             'derechos humanos es:',
                 'alternativas': ['La riqueza',
                                  'La dignidad de la persona humana',
                                  'El poder político',
                                  'La nacionalidad',
                                  'La religión'],
                 'correcta': 'B'},
                {'pregunta': 'Según Nogueira, la dignidad humana fundamenta:',
                 'alternativas': ['Solo los derechos civiles',
                                  'Tanto los derechos civiles y políticos '
                                  'como los económicos, sociales y '
                                  'culturales',
                                  'Solo los derechos económicos',
                                  'Solo los derechos culturales',
                                  'Ningún derecho en particular'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 22 de la Constitución establece '
                             'que el trabajo es:',
                 'alternativas': ['Solo una obligación',
                                  'Un deber y un derecho',
                                  'Solo un derecho opcional',
                                  'Una actividad comercial',
                                  'Un privilegio'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 22, el trabajo es la base '
                             'de:',
                 'alternativas': ['El comercio exterior',
                                  'El bienestar social',
                                  'La recaudación fiscal',
                                  'La política monetaria',
                                  'El sistema bancario'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 23 de la Constitución protege '
                             'especialmente a:',
                 'alternativas': ['Solo a los empresarios',
                                  'A la madre, al menor de edad y al '
                                  'impedido que trabajan',
                                  'Solo a los sindicatos',
                                  'Solo al Estado',
                                  'A los extranjeros exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 23, ninguna relación laboral '
                             'puede:',
                 'alternativas': ['Exigir puntualidad',
                                  'Limitar los derechos constitucionales ni '
                                  'rebajar la dignidad del trabajador',
                                  'Establecer horarios',
                                  'Fijar un sueldo',
                                  'Solicitar experiencia'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Constitución, nadie está obligado a '
                             'prestar trabajo:',
                 'alternativas': ['Los fines de semana',
                                  'Sin retribución o sin su libre '
                                  'consentimiento',
                                  'Fuera de su ciudad',
                                  'En el sector privado',
                                  'Para el Estado'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 24 de la Constitución establece el '
                             'derecho del trabajador a:',
                 'alternativas': ['Vacaciones ilimitadas',
                                  'Una remuneración equitativa y suficiente',
                                  'Trabajo garantizado de por vida',
                                  'Doble sueldo',
                                  'Ascenso automático'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado promueve condiciones para el '
                             'progreso social y económico mediante:',
                 'alternativas': ['El aumento de impuestos únicamente',
                                  'Políticas de fomento del empleo '
                                  'productivo y educación para el trabajo',
                                  'La reducción del gasto en educación',
                                  'El cierre de empresas',
                                  'La eliminación de sindicatos'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración Universal de Derechos Humanos, '
                             'en su preámbulo, señala que todo individuo y '
                             'órgano de la sociedad debe:',
                 'alternativas': ['Ignorar los derechos humanos',
                                  'Promover el respeto a los derechos '
                                  'humanos',
                                  'Depender del Estado',
                                  'Rechazar tratados internacionales',
                                  'Limitar la participación ciudadana'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos sociales y económicos buscan que '
                             'los ciudadanos gocen de:',
                 'alternativas': ['Solo riqueza material',
                                  'Un estado de bienestar',
                                  'Solo poder político',
                                  'Solo prestigio social',
                                  'Ninguna prestación estatal'],
                 'correcta': 'B'},
                {'pregunta': 'Según el texto, la persona, en virtud de su '
                             'dignidad, se convierte en:',
                 'alternativas': ['Un medio para el Estado',
                                  'El fin del Estado',
                                  'Un obstáculo para el desarrollo',
                                  'Un sujeto pasivo sin derechos',
                                  'Un elemento secundario'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, según Nogueira, está al servicio '
                             'de:',
                 'alternativas': ['El mercado',
                                  'La persona humana',
                                  'Solo el gobierno de turno',
                                  'Las empresas privadas',
                                  'Los organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad del Estado, según el texto, es '
                             'promover:',
                 'alternativas': ['El comercio exterior únicamente',
                                  'El bien común',
                                  'Solo la recaudación fiscal',
                                  'El crecimiento demográfico',
                                  'La expansión territorial'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los instrumentos con jerarquía '
                             'constitucional que contemplan estos derechos '
                             'figura:',
                 'alternativas': ['Solo la Constitución peruana',
                                  'La Declaración Universal de Derechos '
                                  'Humanos',
                                  'Solo el Código Civil',
                                  'Solo el Código Penal',
                                  'Ninguno en particular'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de dignidad humana implica que '
                             'los derechos se reconozcan:',
                 'alternativas': ['Solo a ciertos grupos',
                                  'Sin distingo de tipo cultural, económico '
                                  'o social',
                                  'Solo a los ciudadanos con recursos',
                                  'Solo a los adultos',
                                  'Solo a los trabajadores formales'],
                 'correcta': 'B'},
                {'pregunta': 'Los derechos sociales y económicos '
                             'representan, según el texto:',
                 'alternativas': ['Obligaciones exclusivas del ciudadano',
                                  'Los fines sociales del Estado',
                                  'Una carga innecesaria',
                                  'Privilegios de unos pocos',
                                  'Normas sin aplicación práctica'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El Poder Legislativo se define como la facultad '
                           'del Estado para {Dictar, modificar, interpretar '
                           'y derogar leyes}.',
                           'El órgano que ejerce la potestad legislativa se '
                           'denomina {Parlamento}.',
                           'Según el artículo 91 de la Constitución, el '
                           'Poder Legislativo reside en {El Congreso}.',
                           'Poder Legislativo y Congreso de la República '
                           'son, conceptualmente {Categorías conceptuales '
                           'distintas}.',
                           'El Presidente de la República puede expedir '
                           'normas con rango de ley llamadas {Decretos de '
                           'Urgencia y Decretos Legislativos}.',
                           'En regímenes de facto, se gobierna mediante '
                           '{Decretos Ley}.',
                           'Los Gobiernos Locales expiden normas con rango '
                           'de ley llamadas {Ordenanzas Municipales}.',
                           'Los Gobiernos Regionales expiden normas con '
                           'rango de ley denominadas {Normas generales}.',
                           'El artículo 102 de la Constitución establece que '
                           'dar leyes es atribución de {El Congreso}.',
                           'La fase introductoria del proceso legislativo '
                           'corresponde a {La iniciativa para proponer un '
                           'proyecto de ley}.',
                           'La iniciativa popular en el Perú requiere '
                           'representar de la población electoral {0,3%}.',
                           'La fase constitutiva del proceso legislativo '
                           'corresponde a {La deliberación y aprobación de '
                           'la ley por el Congreso}.',
                           'Según el artículo 105, todo proyecto de ley debe '
                           'ser previamente {Dictaminado por una comisión}.',
                           'Las leyes ordinarias en el Congreso se aprueban '
                           'por {Mayoría simple}.',
                           'Las leyes orgánicas requieren el voto de {Más de '
                           'la mitad del número legal de congresistas}.',
                           'La promulgación de la ley es realizada por {El '
                           'Presidente de la República}.',
                           'La promulgación consiste en que el Jefe de '
                           'Estado {Rubrique la ley y ordene su '
                           'publicación}.',
                           'Según el artículo 108, la ley aprobada se envía '
                           'al Presidente para {Su promulgación}.',
                           'Las leyes de reforma constitucional se sujetan '
                           'al procedimiento del artículo {206}.',
                           'El derecho de iniciativa legislativa, además del '
                           'Legislativo y Ejecutivo, se otorga también a {El '
                           'Poder Judicial, gobiernos regionales, locales y '
                           'colegios profesionales}.']}],
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
                 'alternativas': ['Administrar justicia',
                                  'Dictar, modificar, interpretar y derogar '
                                  'leyes',
                                  'Ejecutar el presupuesto',
                                  'Firmar tratados exclusivamente',
                                  'Nombrar ministros'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano que ejerce la potestad legislativa '
                             'se denomina:',
                 'alternativas': ['Poder Ejecutivo',
                                  'Parlamento',
                                  'Poder Judicial',
                                  'Tribunal Constitucional',
                                  'Jurado Electoral'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 91 de la Constitución, el '
                             'Poder Legislativo reside en:',
                 'alternativas': ['El Presidente',
                                  'El Congreso',
                                  'El Poder Judicial',
                                  'Los gobiernos regionales',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'Poder Legislativo y Congreso de la República '
                             'son, conceptualmente:',
                 'alternativas': ['Exactamente lo mismo',
                                  'Categorías conceptuales distintas',
                                  'Términos intercambiables sin matices',
                                  'Sinónimos absolutos',
                                  'Idénticos en toda circunstancia'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente de la República puede expedir '
                             'normas con rango de ley llamadas:',
                 'alternativas': ['Ordenanzas municipales',
                                  'Decretos de Urgencia y Decretos '
                                  'Legislativos',
                                  'Resoluciones administrativas',
                                  'Directivas internas',
                                  'Circulares'],
                 'correcta': 'B'},
                {'pregunta': 'En regímenes de facto, se gobierna mediante:',
                 'alternativas': ['Decretos Supremos',
                                  'Decretos Ley',
                                  'Ordenanzas',
                                  'Resoluciones Ministeriales',
                                  'Directivas'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Locales expiden normas con rango '
                             'de ley llamadas:',
                 'alternativas': ['Decretos Legislativos',
                                  'Ordenanzas Municipales',
                                  'Normas generales',
                                  'Decretos de Urgencia',
                                  'Resoluciones Legislativas'],
                 'correcta': 'B'},
                {'pregunta': 'Los Gobiernos Regionales expiden normas con '
                             'rango de ley denominadas:',
                 'alternativas': ['Ordenanzas Municipales',
                                  'Normas generales',
                                  'Decretos Ley',
                                  'Decretos Supremos',
                                  'Resoluciones Ministeriales'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo 102 de la Constitución establece '
                             'que dar leyes es atribución de:',
                 'alternativas': ['El Poder Ejecutivo',
                                  'El Congreso',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'La fase introductoria del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La promulgación de la ley',
                                  'La iniciativa para proponer un proyecto '
                                  'de ley',
                                  'La votación final',
                                  'La publicación en el diario oficial',
                                  'El veto presidencial'],
                 'correcta': 'B'},
                {'pregunta': 'La iniciativa popular en el Perú requiere '
                             'representar de la población electoral:',
                 'alternativas': ['3%', '0,3%', '10%', '1%', '30%'],
                 'correcta': 'B'},
                {'pregunta': 'La fase constitutiva del proceso legislativo '
                             'corresponde a:',
                 'alternativas': ['La iniciativa del proyecto',
                                  'La deliberación y aprobación de la ley '
                                  'por el Congreso',
                                  'La promulgación',
                                  'La publicación oficial',
                                  'El archivo del proyecto'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 105, todo proyecto de ley '
                             'debe ser previamente:',
                 'alternativas': ['Publicado en un diario',
                                  'Dictaminado por una comisión',
                                  'Aprobado por el Poder Judicial',
                                  'Consultado con el pueblo',
                                  'Traducido a lenguas originarias'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes ordinarias en el Congreso se '
                             'aprueban por:',
                 'alternativas': ['Mayoría calificada',
                                  'Mayoría simple',
                                  'Unanimidad',
                                  'Dos tercios',
                                  'Consenso obligatorio'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes orgánicas requieren el voto de:',
                 'alternativas': ['Un tercio de los congresistas',
                                  'Más de la mitad del número legal de '
                                  'congresistas',
                                  'Todos los congresistas',
                                  'Solo la mesa directiva',
                                  'La mayoría relativa'],
                 'correcta': 'B'},
                {'pregunta': 'La promulgación de la ley es realizada por:',
                 'alternativas': ['El presidente del Congreso',
                                  'El Presidente de la República',
                                  'El Tribunal Constitucional',
                                  'El Poder Judicial',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'La promulgación consiste en que el Jefe de '
                             'Estado:',
                 'alternativas': ['Redacte la ley',
                                  'Rubrique la ley y ordene su publicación',
                                  'Modifique el texto legal',
                                  'Vote la ley',
                                  'Elabore el proyecto'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 108, la ley aprobada se '
                             'envía al Presidente para:',
                 'alternativas': ['Su archivo',
                                  'Su promulgación',
                                  'Su anulación',
                                  'Su revisión judicial',
                                  'Su traducción'],
                 'correcta': 'B'},
                {'pregunta': 'Las leyes de reforma constitucional se sujetan '
                             'al procedimiento del artículo:',
                 'alternativas': ['105', '108', '206', '91', '102'],
                 'correcta': 'C'},
                {'pregunta': 'El derecho de iniciativa legislativa, además '
                             'del Legislativo y Ejecutivo, se otorga también '
                             'a:',
                 'alternativas': ['Solo a los partidos políticos',
                                  'El Poder Judicial, gobiernos regionales, '
                                  'locales y colegios profesionales',
                                  'Solo a las universidades',
                                  'Solo al sector privado',
                                  'Solo a organismos internacionales'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El Poder Ejecutivo está constituido por el '
                           'Presidente, quien es Jefe de Estado y {Jefe de '
                           'Gobierno}.',
                           'El Poder Ejecutivo es el órgano encargado de {La '
                           'administración del Estado y ejecución de las '
                           'leyes}.',
                           'Integran el Poder Ejecutivo el Presidente y {El '
                           'Consejo de Ministros}.',
                           'En el sistema presidencial, los tres poderes del '
                           'Estado son {Autónomos e independientes}.',
                           'Para ser presidente del Perú se requiere ser '
                           'peruano {De nacimiento}.',
                           'La edad mínima para postular a la presidencia es '
                           'de {35 años}.',
                           'El presidente de la República se elige por un '
                           'mandato de {5 años}.',
                           'La reelección presidencial inmediata en el Perú '
                           'está {No permitida}.',
                           'Para ganar la presidencia en primera vuelta se '
                           'requiere {Mayoría absoluta}.',
                           'Si ningún candidato obtiene mayoría absoluta, se '
                           'realiza {Una segunda elección entre los dos más '
                           'votados}.',
                           'Según el artículo 116, el Presidente jura y '
                           'asume el cargo ante {El Congreso}.',
                           'El Presidente asume el cargo el {28 de julio}.',
                           'Entre las atribuciones del Presidente figura '
                           'representar al Estado {Dentro y fuera de la '
                           'República}.',
                           'El Presidente puede convocar al Congreso a '
                           'legislatura {Extraordinaria}.',
                           'El Presidente dirige mensajes obligatorios al '
                           'Congreso al instalarse la legislatura {Ordinaria '
                           'anual}.',
                           'El Presidente reglamenta las leyes mediante '
                           '{Decretos y resoluciones}.',
                           'Al reglamentar las leyes, el Presidente no puede '
                           '{Transgredirlas ni desnaturalizarlas}.',
                           'El Presidente dirige la política exterior y '
                           'puede {Celebrar y ratificar tratados}.',
                           'Junto con el Presidente se eligen, con los '
                           'mismos requisitos {Dos vicepresidentes}.',
                           'El Presidente debe velar por el orden interno y '
                           '{La seguridad exterior de la República}.']}],
  'cuadros': [{'titulo': '11.2 REQUISITOS PARA SER PRESIDENTE',
               'encabezados': ['Requisito', 'Detalle'],
               'filas': [['{Nacionalidad}', 'Peruano de {nacimiento}'],
                         ['{Edad}', '35 años como {mínimo}'],
                         ['{Sufragio}', 'Gozar del derecho de voto']]}],
  'preguntas': [{'pregunta': 'El Poder Ejecutivo está constituido por el '
                             'Presidente, quien es Jefe de Estado y:',
                 'alternativas': ['Jefe del Poder Judicial',
                                  'Jefe de Gobierno',
                                  'Jefe del Congreso',
                                  'Jefe militar exclusivamente',
                                  'Jefe religioso'],
                 'correcta': 'B'},
                {'pregunta': 'El Poder Ejecutivo es el órgano encargado de:',
                 'alternativas': ['Dictar leyes exclusivamente',
                                  'La administración del Estado y ejecución '
                                  'de las leyes',
                                  'Administrar justicia',
                                  'Fiscalizar al Congreso',
                                  'Organizar elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'Integran el Poder Ejecutivo el Presidente y:',
                 'alternativas': ['El Congreso',
                                  'El Consejo de Ministros',
                                  'El Poder Judicial',
                                  'El Tribunal Constitucional',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'En el sistema presidencial, los tres poderes '
                             'del Estado son:',
                 'alternativas': ['Dependientes entre sí',
                                  'Autónomos e independientes',
                                  'Subordinados al Ejecutivo',
                                  'Fusionados en uno solo',
                                  'Elegidos por el Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser presidente del Perú se requiere ser '
                             'peruano:',
                 'alternativas': ['Naturalizado',
                                  'De nacimiento',
                                  'Residente',
                                  'Con doble nacionalidad',
                                  'Mayor de 50 años exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La edad mínima para postular a la presidencia '
                             'es de:',
                 'alternativas': ['25 años',
                                  '35 años',
                                  '40 años',
                                  '30 años',
                                  '45 años'],
                 'correcta': 'B'},
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
                 'alternativas': ['Permitida sin restricciones',
                                  'No permitida',
                                  'Permitida solo una vez',
                                  'Obligatoria',
                                  'Sujeta a referéndum'],
                 'correcta': 'B'},
                {'pregunta': 'Para ganar la presidencia en primera vuelta se '
                             'requiere:',
                 'alternativas': ['Mayoría relativa',
                                  'Mayoría absoluta',
                                  'Un tercio de los votos',
                                  'Solo más votos que el segundo',
                                  'La mitad exacta de votos válidos'],
                 'correcta': 'B'},
                {'pregunta': 'Si ningún candidato obtiene mayoría absoluta, '
                             'se realiza:',
                 'alternativas': ['Una tercera vuelta',
                                  'Una segunda elección entre los dos más '
                                  'votados',
                                  'Un sorteo',
                                  'Una decisión del Congreso',
                                  'Una nueva convocatoria general'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 116, el Presidente jura y '
                             'asume el cargo ante:',
                 'alternativas': ['El Poder Judicial',
                                  'El Congreso',
                                  'El Jurado Nacional de Elecciones',
                                  'El pueblo directamente',
                                  'El Tribunal Constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente asume el cargo el:',
                 'alternativas': ['1 de enero',
                                  '28 de julio',
                                  '1 de mayo',
                                  '9 de diciembre',
                                  '15 de agosto'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las atribuciones del Presidente figura '
                             'representar al Estado:',
                 'alternativas': ['Solo dentro del país',
                                  'Dentro y fuera de la República',
                                  'Solo en organismos internacionales',
                                  'Solo ante el Congreso',
                                  'Solo en tratados comerciales'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente puede convocar al Congreso a '
                             'legislatura:',
                 'alternativas': ['Solo ordinaria',
                                  'Extraordinaria',
                                  'Solo virtual',
                                  'Permanente sin descanso',
                                  'Ninguna, esa función es del Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente dirige mensajes obligatorios al '
                             'Congreso al instalarse la legislatura:',
                 'alternativas': ['Extraordinaria únicamente',
                                  'Ordinaria anual',
                                  'Cada seis meses',
                                  'Solo el último año de gobierno',
                                  'Nunca, esa función no le corresponde'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente reglamenta las leyes mediante:',
                 'alternativas': ['Ordenanzas municipales',
                                  'Decretos y resoluciones',
                                  'Sentencias judiciales',
                                  'Leyes orgánicas',
                                  'Resoluciones legislativas'],
                 'correcta': 'B'},
                {'pregunta': 'Al reglamentar las leyes, el Presidente no '
                             'puede:',
                 'alternativas': ['Emitir decretos',
                                  'Transgredirlas ni desnaturalizarlas',
                                  'Publicarlas',
                                  'Ejecutarlas',
                                  'Cumplirlas'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente dirige la política exterior y '
                             'puede:',
                 'alternativas': ['Declarar la guerra sin el Congreso',
                                  'Celebrar y ratificar tratados',
                                  'Modificar la Constitución solo',
                                  'Disolver el Poder Judicial',
                                  'Elegir a los congresistas'],
                 'correcta': 'B'},
                {'pregunta': 'Junto con el Presidente se eligen, con los '
                             'mismos requisitos:',
                 'alternativas': ['Los ministros',
                                  'Dos vicepresidentes',
                                  'Los congresistas',
                                  'Los alcaldes',
                                  'Los gobernadores regionales'],
                 'correcta': 'B'},
                {'pregunta': 'El Presidente debe velar por el orden interno '
                             'y:',
                 'alternativas': ['El comercio exterior',
                                  'La seguridad exterior de la República',
                                  'La política monetaria',
                                  'El sistema educativo',
                                  'La reforma agraria'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El Poder Judicial es el organismo encargado de '
                           '{Administrar justicia}.',
                           'El Poder Judicial es autónomo en lo político, '
                           'administrativo, económico y {Disciplinario}.',
                           'En el ejercicio jurisdiccional, el Poder '
                           'Judicial es {Independiente}.',
                           'La potestad de administrar justicia emana de {El '
                           'pueblo}.',
                           'El máximo órgano jurisdiccional del Poder '
                           'Judicial es {La Corte Suprema de Justicia}.',
                           'Los Juzgados de Paz Letrados corresponden al '
                           'nivel {Básico}.',
                           'El órgano de gestión encargado de la '
                           'administración del Poder Judicial es {El Consejo '
                           'Ejecutivo del Poder Judicial}.',
                           'No existe ni puede establecerse jurisdicción '
                           'independiente, salvo {La militar y la arbitral}.',
                           'El principio de unidad y exclusividad de la '
                           'función jurisdiccional implica que {No hay '
                           'proceso judicial por comisión o delegación}.',
                           'El principio de independencia jurisdiccional '
                           'impide que una autoridad {Se avoque a causas '
                           'pendientes ante el órgano jurisdiccional}.',
                           'El debido proceso impide que una persona sea '
                           'juzgada por {Comisiones especiales creadas al '
                           'efecto}.',
                           'La regla general en los procesos judiciales es '
                           'la {Publicidad, salvo disposición contraria de '
                           'la ley}.',
                           'Los procesos por responsabilidad de funcionarios '
                           'públicos son {Siempre públicos}.',
                           'La motivación escrita de las resoluciones '
                           'judiciales es obligatoria en {Todas las '
                           'instancias}.',
                           'El artículo de la Constitución que precisa la '
                           'extensión jurisdiccional en comunidades es el '
                           '{Artículo 149}.',
                           'Ninguna autoridad puede dejar sin efecto '
                           'resoluciones que han pasado en autoridad de '
                           '{Cosa juzgada}.',
                           'El derecho de gracia y la facultad de '
                           'investigación del Congreso no deben {Interferir '
                           'en el procedimiento jurisdiccional}.',
                           'La Sala Plena de la Corte Suprema es un órgano '
                           'de {Gestión}.',
                           'Los Juzgados de Paz, en la estructura del Poder '
                           'Judicial, están en el nivel {Más básico}.',
                           'La Ley Orgánica del Poder Judicial regula, junto '
                           'con la Constitución, el ejercicio de {Las '
                           'funciones jurisdiccionales y de gobierno}.']}],
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
                                  'Representar al Estado en el exterior',
                                  'Organizar elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'El Poder Judicial es autónomo en lo político, '
                             'administrativo, económico y:',
                 'alternativas': ['Militar',
                                  'Disciplinario',
                                  'Comercial',
                                  'Religioso',
                                  'Educativo'],
                 'correcta': 'B'},
                {'pregunta': 'En el ejercicio jurisdiccional, el Poder '
                             'Judicial es:',
                 'alternativas': ['Dependiente del Ejecutivo',
                                  'Independiente',
                                  'Subordinado al Congreso',
                                  'Controlado por el Tribunal Constitucional',
                                  'Dirigido por el Presidente'],
                 'correcta': 'B'},
                {'pregunta': 'La potestad de administrar justicia emana de:',
                 'alternativas': ['El Presidente',
                                  'El pueblo',
                                  'El Congreso',
                                  'Los jueces exclusivamente',
                                  'Organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'El máximo órgano jurisdiccional del Poder '
                             'Judicial es:',
                 'alternativas': ['Los Juzgados de Paz',
                                  'La Corte Suprema de Justicia',
                                  'Las Cortes Superiores',
                                  'El Consejo Ejecutivo',
                                  'Los Juzgados Mixtos'],
                 'correcta': 'B'},
                {'pregunta': 'Los Juzgados de Paz Letrados corresponden al '
                             'nivel:',
                 'alternativas': ['Superior',
                                  'Básico',
                                  'Supremo',
                                  'Constitucional',
                                  'Internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano de gestión encargado de la '
                             'administración del Poder Judicial es:',
                 'alternativas': ['La Sala Penal',
                                  'El Consejo Ejecutivo del Poder Judicial',
                                  'El Ministerio Público',
                                  'La Defensoría del Pueblo',
                                  'El Jurado Nacional de Elecciones'],
                 'correcta': 'B'},
                {'pregunta': 'No existe ni puede establecerse jurisdicción '
                             'independiente, salvo:',
                 'alternativas': ['La religiosa',
                                  'La militar y la arbitral',
                                  'La comercial',
                                  'La internacional',
                                  'La municipal'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de unidad y exclusividad de la '
                             'función jurisdiccional implica que:',
                 'alternativas': ['Existen múltiples jurisdicciones '
                                  'paralelas',
                                  'No hay proceso judicial por comisión o '
                                  'delegación',
                                  'Cualquier autoridad puede juzgar',
                                  'El Congreso puede sentenciar',
                                  'Los alcaldes pueden juzgar delitos'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de independencia jurisdiccional '
                             'impide que una autoridad:',
                 'alternativas': ['Presente denuncias',
                                  'Se avoque a causas pendientes ante el '
                                  'órgano jurisdiccional',
                                  'Solicite información pública',
                                  'Participe en audiencias públicas',
                                  'Realice investigaciones periodísticas'],
                 'correcta': 'B'},
                {'pregunta': 'El debido proceso impide que una persona sea '
                             'juzgada por:',
                 'alternativas': ['Un juez competente',
                                  'Comisiones especiales creadas al efecto',
                                  'La Corte Suprema',
                                  'Un juzgado de paz',
                                  'Un tribunal constitucional'],
                 'correcta': 'B'},
                {'pregunta': 'La regla general en los procesos judiciales es '
                             'la:',
                 'alternativas': ['Reserva absoluta',
                                  'Publicidad, salvo disposición contraria '
                                  'de la ley',
                                  'Confidencialidad total',
                                  'Exclusividad militar',
                                  'Prohibición de prensa'],
                 'correcta': 'B'},
                {'pregunta': 'Los procesos por responsabilidad de '
                             'funcionarios públicos son:',
                 'alternativas': ['Siempre reservados',
                                  'Siempre públicos',
                                  'Decididos por el Congreso',
                                  'Resueltos por decreto',
                                  'Confidenciales por defecto'],
                 'correcta': 'B'},
                {'pregunta': 'La motivación escrita de las resoluciones '
                             'judiciales es obligatoria en:',
                 'alternativas': ['Solo la primera instancia',
                                  'Todas las instancias',
                                  'Solo la Corte Suprema',
                                  'Solo casos penales',
                                  'Ningún nivel en particular'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo de la Constitución que precisa la '
                             'extensión jurisdiccional en comunidades es el:',
                 'alternativas': ['Artículo 51',
                                  'Artículo 149',
                                  'Artículo 91',
                                  'Artículo 22',
                                  'Artículo 24'],
                 'correcta': 'B'},
                {'pregunta': 'Ninguna autoridad puede dejar sin efecto '
                             'resoluciones que han pasado en autoridad de:',
                 'alternativas': ['Consulta previa',
                                  'Cosa juzgada',
                                  'Resolución administrativa',
                                  'Reglamento interno',
                                  'Norma transitoria'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho de gracia y la facultad de '
                             'investigación del Congreso no deben:',
                 'alternativas': ['Ejercerse nunca',
                                  'Interferir en el procedimiento '
                                  'jurisdiccional',
                                  'Ser reguladas por ley',
                                  'Aplicarse a funcionarios',
                                  'Ser públicas'],
                 'correcta': 'B'},
                {'pregunta': 'La Sala Plena de la Corte Suprema es un órgano '
                             'de:',
                 'alternativas': ['Jurisdicción exclusiva',
                                  'Gestión',
                                  'Fiscalización externa',
                                  'Control tributario',
                                  'Relaciones internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'Los Juzgados de Paz, en la estructura del '
                             'Poder Judicial, están en el nivel:',
                 'alternativas': ['Supremo',
                                  'Más básico',
                                  'Constitucional',
                                  'Internacional',
                                  'Militar'],
                 'correcta': 'B'},
                {'pregunta': 'La Ley Orgánica del Poder Judicial regula, '
                             'junto con la Constitución, el ejercicio de:',
                 'alternativas': ['Solo la función administrativa',
                                  'Las funciones jurisdiccionales y de '
                                  'gobierno',
                                  'Solo el presupuesto',
                                  'Solo la disciplina interna',
                                  'Solo las relaciones exteriores'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El Estado peruano se organiza a nivel nacional, '
                           'regional y {Local}.',
                           'El número de organismos constitucionales '
                           'autónomos en el Perú es {Diez}.',
                           'La autonomía de los OCA implica que sus '
                           'directivos {Toman decisiones sin someterse a '
                           'órdenes superiores}.',
                           'El Tribunal Constitucional es el órgano de '
                           'control de {La Constitución}.',
                           'El Tribunal Constitucional está regulado en el '
                           'artículo {201}.',
                           'El Tribunal Constitucional se compone de {Siete '
                           'miembros}.',
                           'Los miembros del Tribunal Constitucional son '
                           'elegidos por un periodo de {Cinco años}.',
                           'Los miembros del Tribunal Constitucional son '
                           'elegidos por el Congreso con {El voto de los dos '
                           'tercios del número legal de miembros}.',
                           'No pueden ser magistrados del Tribunal '
                           'Constitucional los jueces o fiscales que no '
                           'dejaron el cargo con anticipación de {Un año}.',
                           'El Ministerio Público es el órgano encargado de '
                           '{Perseguir el delito}.',
                           'El Ministerio Público es presidido por {El '
                           'Fiscal de la Nación}.',
                           'El Fiscal de la Nación es elegido por {La Junta '
                           'de Fiscales Supremos}.',
                           'El cargo de Fiscal de la Nación dura {Tres '
                           'años}.',
                           'El cargo de Fiscal de la Nación puede '
                           'prorrogarse por reelección hasta por {Dos años '
                           'más}.',
                           'Según el artículo 159, el Ministerio Público '
                           'conduce desde su inicio {La investigación del '
                           'delito}.',
                           'La Policía Nacional está obligada a cumplir los '
                           'mandatos de {El Ministerio Público}.',
                           'Entre los organismos constitucionales autónomos '
                           'figura el organismo encargado de emitir moneda, '
                           'que es {El Banco Central de Reserva}.',
                           'El organismo encargado de la defensa de los '
                           'derechos constitucionales de la persona es {La '
                           'Defensoría del Pueblo}.',
                           'El organismo encargado de organizar los procesos '
                           'electorales es {La ONPE}.',
                           'El organismo encargado del registro de '
                           'identificación y estado civil es {El RENIEC}.']}],
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
                 'alternativas': ['Internacional',
                                  'Local',
                                  'Militar',
                                  'Eclesiástico',
                                  'Empresarial'],
                 'correcta': 'B'},
                {'pregunta': 'El número de organismos constitucionales '
                             'autónomos en el Perú es:',
                 'alternativas': ['Cinco',
                                  'Diez',
                                  'Quince',
                                  'Tres',
                                  'Veinte'],
                 'correcta': 'B'},
                {'pregunta': 'La autonomía de los OCA implica que sus '
                             'directivos:',
                 'alternativas': ['Dependen del Presidente',
                                  'Toman decisiones sin someterse a órdenes '
                                  'superiores',
                                  'Son elegidos por sorteo',
                                  'Actúan solo por consulta popular',
                                  'Dependen del Congreso exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional es el órgano de '
                             'control de:',
                 'alternativas': ['El presupuesto',
                                  'La Constitución',
                                  'El comercio exterior',
                                  'Las elecciones únicamente',
                                  'La banca'],
                 'correcta': 'B'},
                {'pregunta': 'El Tribunal Constitucional está regulado en el '
                             'artículo:',
                 'alternativas': ['91', '158', '201', '102', '24'],
                 'correcta': 'C'},
                {'pregunta': 'El Tribunal Constitucional se compone de:',
                 'alternativas': ['Cinco miembros',
                                  'Siete miembros',
                                  'Nueve miembros',
                                  'Tres miembros',
                                  'Doce miembros'],
                 'correcta': 'B'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por un periodo de:',
                 'alternativas': ['Tres años',
                                  'Cinco años',
                                  'Diez años',
                                  'Cuatro años',
                                  'Vitalicio'],
                 'correcta': 'B'},
                {'pregunta': 'Los miembros del Tribunal Constitucional son '
                             'elegidos por el Congreso con:',
                 'alternativas': ['Mayoría simple',
                                  'El voto de los dos tercios del número '
                                  'legal de miembros',
                                  'Unanimidad',
                                  'Mayoría absoluta',
                                  'Consulta popular directa'],
                 'correcta': 'B'},
                {'pregunta': 'No pueden ser magistrados del Tribunal '
                             'Constitucional los jueces o fiscales que no '
                             'dejaron el cargo con anticipación de:',
                 'alternativas': ['Seis meses',
                                  'Un año',
                                  'Dos años',
                                  'Tres meses',
                                  'Cinco años'],
                 'correcta': 'B'},
                {'pregunta': 'El Ministerio Público es el órgano encargado '
                             'de:',
                 'alternativas': ['Administrar justicia directamente',
                                  'Perseguir el delito',
                                  'Legislar',
                                  'Dirigir el gobierno',
                                  'Emitir moneda'],
                 'correcta': 'B'},
                {'pregunta': 'El Ministerio Público es presidido por:',
                 'alternativas': ['El Presidente de la República',
                                  'El Fiscal de la Nación',
                                  'El presidente del Poder Judicial',
                                  'El presidente del Congreso',
                                  'El Defensor del Pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'El Fiscal de la Nación es elegido por:',
                 'alternativas': ['El Congreso',
                                  'La Junta de Fiscales Supremos',
                                  'El Presidente de la República',
                                  'El Poder Judicial',
                                  'Voto popular directo'],
                 'correcta': 'B'},
                {'pregunta': 'El cargo de Fiscal de la Nación dura:',
                 'alternativas': ['Dos años',
                                  'Tres años',
                                  'Cinco años',
                                  'Un año',
                                  'Vitalicio'],
                 'correcta': 'B'},
                {'pregunta': 'El cargo de Fiscal de la Nación puede '
                             'prorrogarse por reelección hasta por:',
                 'alternativas': ['Cinco años más',
                                  'Dos años más',
                                  'Un año más',
                                  'Diez años más',
                                  'No es prorrogable'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 159, el Ministerio Público '
                             'conduce desde su inicio:',
                 'alternativas': ['El proceso legislativo',
                                  'La investigación del delito',
                                  'Las elecciones',
                                  'El presupuesto público',
                                  'La política exterior'],
                 'correcta': 'B'},
                {'pregunta': 'La Policía Nacional está obligada a cumplir '
                             'los mandatos de:',
                 'alternativas': ['Solo el Poder Judicial',
                                  'El Ministerio Público',
                                  'Solo el Congreso',
                                  'Los gobiernos regionales',
                                  'Los gobiernos locales'],
                 'correcta': 'B'},
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
                 'alternativas': ['El Tribunal Constitucional',
                                  'La Defensoría del Pueblo',
                                  'La Contraloría',
                                  'El JNE',
                                  'La ONPE'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo encargado de organizar los '
                             'procesos electorales es:',
                 'alternativas': ['El JNE',
                                  'La ONPE',
                                  'El RENIEC',
                                  'La Defensoría del Pueblo',
                                  'El Ministerio Público'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo encargado del registro de '
                             'identificación y estado civil es:',
                 'alternativas': ['La ONPE',
                                  'El RENIEC',
                                  'El JNE',
                                  'La SUNARP',
                                  'El INEI'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según Sumar Albujar, el régimen económico define '
                           'el rol de {El Estado en materia económica}.',
                           'Según García Belaúnde, la Constitución Económica '
                           'surgió en {El periodo de entreguerras del siglo '
                           'XX}.',
                           'La constitución considerada pionera del '
                           'constitucionalismo económico es la de {Weimar}.',
                           'La Constitución de Weimar garantiza el derecho '
                           'de {Propiedad, con límites por el bien general}.',
                           'El régimen económico peruano se basa, entre '
                           'otros principios, en la economía social de '
                           '{Mercado}.',
                           'La economía social de mercado es representativa '
                           'de los valores de {Libertad y justicia}.',
                           'Según Herhärd y Müller Armack, la economía '
                           'social de mercado transforma la productividad '
                           'individual en {Progreso social}.',
                           'La economía social de mercado combate la '
                           'formación de {Carteles y concentración de poder '
                           'económico}.',
                           'Para que funcione de manera óptima el mercado, '
                           'el Estado debe {Establecer normas claras sin '
                           'intervenir de manera permanente}.',
                           'La economía social de mercado requiere un Estado '
                           '{Fuerte e independiente de los grupos de poder '
                           'económico}.',
                           'El principio de solidaridad en la economía '
                           'social de mercado exige {Equilibrio social y '
                           'promoción del bien común}.',
                           'El principio de subsidiaridad establece que el '
                           'Estado no debe hacer {Lo que el individuo puede '
                           'hacer por propia iniciativa}.',
                           'El mercado y la competencia, según el texto, '
                           'deben garantizar la libertad de {Consumidores, '
                           'empleadores y trabajadores}.',
                           'Combatir los monopolios requiere, según el '
                           'texto, una legislación {Antimonopolio}.',
                           'El régimen económico también se define como el '
                           'conjunto de reglas de juego con rango '
                           '{Constitucional}.',
                           'Entre los principios que rigen el régimen '
                           'económico peruano figura la libre {Competencia}.',
                           'El régimen económico busca contribuir '
                           'positivamente al {Desempeño económico del país}.',
                           'El aparato administrativo y judicial en la '
                           'economía social de mercado debe ser '
                           '{Independiente y libre de corrupción}.',
                           'El Estado, en una economía social de mercado, '
                           'actúa por medio de {El sistema monetario y el '
                           'ordenamiento jurídico}.',
                           'Entre los principios del régimen económico '
                           'constitucional peruano figura la igualdad de '
                           'tratamiento al {Capital}.']}],
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
                                  'El Estado en materia económica',
                                  'Los organismos internacionales',
                                  'Los sindicatos',
                                  'El sector informal'],
                 'correcta': 'B'},
                {'pregunta': 'Según García Belaúnde, la Constitución '
                             'Económica surgió en:',
                 'alternativas': ['El siglo XIX',
                                  'El periodo de entreguerras del siglo XX',
                                  'La época colonial',
                                  'El siglo XXI',
                                  'La Antigüedad clásica'],
                 'correcta': 'B'},
                {'pregunta': 'La constitución considerada pionera del '
                             'constitucionalismo económico es la de:',
                 'alternativas': ['Cádiz',
                                  'Weimar',
                                  'Filadelfia',
                                  'Bayona',
                                  'Roma'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución de Weimar garantiza el derecho '
                             'de:',
                 'alternativas': ['Voto universal',
                                  'Propiedad, con límites por el bien '
                                  'general',
                                  'Libre comercio sin restricciones',
                                  'Nacionalización total',
                                  'Monopolio estatal'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen económico peruano se basa, entre '
                             'otros principios, en la economía social de:',
                 'alternativas': ['Estado',
                                  'Mercado',
                                  'Planificación central',
                                  'Trueque',
                                  'Autarquía'],
                 'correcta': 'B'},
                {'pregunta': 'La economía social de mercado es '
                             'representativa de los valores de:',
                 'alternativas': ['Autoridad y jerarquía',
                                  'Libertad y justicia',
                                  'Uniformidad y control',
                                  'Propiedad colectiva obligatoria',
                                  'Aislamiento económico'],
                 'correcta': 'B'},
                {'pregunta': 'Según Herhärd y Müller Armack, la economía '
                             'social de mercado transforma la productividad '
                             'individual en:',
                 'alternativas': ['Ganancia exclusiva de empresarios',
                                  'Progreso social',
                                  'Control estatal total',
                                  'Estancamiento económico',
                                  'Monopolio privado'],
                 'correcta': 'B'},
                {'pregunta': 'La economía social de mercado combate la '
                             'formación de:',
                 'alternativas': ['Pequeñas empresas',
                                  'Carteles y concentración de poder '
                                  'económico',
                                  'Cooperativas',
                                  'Sindicatos',
                                  'Mercados locales'],
                 'correcta': 'B'},
                {'pregunta': 'Para que funcione de manera óptima el mercado, '
                             'el Estado debe:',
                 'alternativas': ['Intervenir permanentemente',
                                  'Establecer normas claras sin intervenir '
                                  'de manera permanente',
                                  'Controlar todos los precios',
                                  'Eliminar la competencia',
                                  'Nacionalizar las empresas'],
                 'correcta': 'B'},
                {'pregunta': 'La economía social de mercado requiere un '
                             'Estado:',
                 'alternativas': ['Débil y dependiente de grupos de poder',
                                  'Fuerte e independiente de los grupos de '
                                  'poder económico',
                                  'Ausente en la economía',
                                  'Controlado por monopolios',
                                  'Sin aparato judicial'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de solidaridad en la economía '
                             'social de mercado exige:',
                 'alternativas': ['Competencia sin límites',
                                  'Equilibrio social y promoción del bien '
                                  'común',
                                  'Individualismo extremo',
                                  'Aislamiento económico',
                                  'Monopolio estatal'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de subsidiaridad establece que el '
                             'Estado no debe hacer:',
                 'alternativas': ['Ninguna función pública',
                                  'Lo que el individuo puede hacer por '
                                  'propia iniciativa',
                                  'Políticas sociales',
                                  'Control tributario',
                                  'Regulación económica'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado y la competencia, según el texto, '
                             'deben garantizar la libertad de:',
                 'alternativas': ['Solo los empresarios',
                                  'Consumidores, empleadores y trabajadores',
                                  'Solo el Estado',
                                  'Solo los inversionistas extranjeros',
                                  'Solo los bancos'],
                 'correcta': 'B'},
                {'pregunta': 'Combatir los monopolios requiere, según el '
                             'texto, una legislación:',
                 'alternativas': ['De libre mercado absoluto',
                                  'Antimonopolio',
                                  'De protección arancelaria total',
                                  'De nacionalización',
                                  'De control de precios'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen económico también se define como el '
                             'conjunto de reglas de juego con rango:',
                 'alternativas': ['Municipal',
                                  'Constitucional',
                                  'Reglamentario',
                                  'Internacional exclusivo',
                                  'Consuetudinario'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los principios que rigen el régimen '
                             'económico peruano figura la libre:',
                 'alternativas': ['Migración',
                                  'Competencia',
                                  'Censura',
                                  'Expropiación',
                                  'Nacionalización'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen económico busca contribuir '
                             'positivamente al:',
                 'alternativas': ['Aislamiento comercial',
                                  'Desempeño económico del país',
                                  'Control absoluto del mercado',
                                  'Monopolio estatal',
                                  'Cierre de fronteras'],
                 'correcta': 'B'},
                {'pregunta': 'El aparato administrativo y judicial en la '
                             'economía social de mercado debe ser:',
                 'alternativas': ['Dependiente del poder económico',
                                  'Independiente y libre de corrupción',
                                  'Controlado por empresas privadas',
                                  'Subordinado al Congreso',
                                  'Eliminado del sistema'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, en una economía social de mercado, '
                             'actúa por medio de:',
                 'alternativas': ['La intervención directa en precios',
                                  'El sistema monetario y el ordenamiento '
                                  'jurídico',
                                  'La propiedad estatal de todo',
                                  'El control absoluto de empresas',
                                  'La eliminación del mercado'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los principios del régimen económico '
                             'constitucional peruano figura la igualdad de '
                             'tratamiento al:',
                 'alternativas': ['Estado',
                                  'Capital',
                                  'Poder Judicial',
                                  'Congreso',
                                  'Poder Ejecutivo'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La descentralización forma parte de la reforma '
                           '{Del Estado peruano}.',
                           'La descentralización busca alcanzar un gobierno '
                           '{Efectivo, eficiente y al servicio de la '
                           'ciudadanía}.',
                           'Según Finot, la descentralización es un proceso '
                           'de transferencia desde el gobierno nacional '
                           'hacia {Una autoridad subnacional o local}.',
                           'La descentralización, según el texto, busca '
                           'reducir {La pobreza y la corrupción}.',
                           'Un objetivo general de la descentralización es '
                           'que cada gobierno regional y local {Decida sobre '
                           'sus propios recursos}.',
                           'Un objetivo político de la descentralización es '
                           '{La unidad y eficiencia del Estado}.',
                           'Un objetivo económico de la descentralización es '
                           '{El desarrollo económico autosostenido de las '
                           'regiones}.',
                           'Otro objetivo económico de la descentralización '
                           'es la redistribución {Equitativa de los recursos '
                           'del Estado}.',
                           'Históricamente, el Perú ha sido caracterizado '
                           'por los analistas como un país {Centralista}.',
                           'El «descentralismo centralista» se extiende '
                           'desde el inicio de la República hasta {1920}.',
                           'Los primeros proyectos de descentralización '
                           'provinieron principalmente de {El pensamiento '
                           'capitalino, de la élite de Lima}.',
                           'Los primeros proyectos de descentralización '
                           'carecieron de {Presupuesto estatal}.',
                           'El periodo del federalismo fallido en el Perú se '
                           'ubica entre {1821 y 1873}.',
                           'La descentralización es descrita como un proceso '
                           '{Multidimensional, con dinámicas políticas, '
                           'fiscales y administrativas}.',
                           'Entre los objetivos generales de la '
                           'descentralización figura la participación de {La '
                           'sociedad civil}.',
                           'La descentralización busca la integración entre '
                           'el Estado y {La sociedad civil}.',
                           'Entre los objetivos políticos figura la '
                           'institucionalización de {Sólidos gobiernos '
                           'regionales y locales}.',
                           'Un objetivo económico es la cobertura de '
                           'servicios sociales básicos en {Todo el '
                           'territorio nacional}.',
                           'El descentralismo formó parte de casi todos los '
                           'proyectos políticos, pero por razones '
                           'estructurales {No llegaron a concretarse}.',
                           'La descentralización tiene como finalidad el '
                           'desarrollo integral, armónico y {Sostenible del '
                           'país}.']}],
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
                                  'Del Estado peruano',
                                  'Solo del sistema judicial',
                                  'Solo del sistema educativo',
                                  'Del sector financiero exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización busca alcanzar un '
                             'gobierno:',
                 'alternativas': ['Centralizado y jerárquico',
                                  'Efectivo, eficiente y al servicio de la '
                                  'ciudadanía',
                                  'Autoritario',
                                  'Sin participación ciudadana',
                                  'Exclusivamente militar'],
                 'correcta': 'B'},
                {'pregunta': 'Según Finot, la descentralización es un '
                             'proceso de transferencia desde el gobierno '
                             'nacional hacia:',
                 'alternativas': ['Organismos internacionales',
                                  'Una autoridad subnacional o local',
                                  'El sector privado',
                                  'Las Fuerzas Armadas',
                                  'Ningún otro nivel de gobierno'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización, según el texto, busca '
                             'reducir:',
                 'alternativas': ['La participación ciudadana',
                                  'La pobreza y la corrupción',
                                  'El desarrollo regional',
                                  'Los servicios públicos',
                                  'La inversión privada'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo general de la descentralización es '
                             'que cada gobierno regional y local:',
                 'alternativas': ['Dependa del gobierno central para todo',
                                  'Decida sobre sus propios recursos',
                                  'Elimine su autonomía',
                                  'Se subordine a Lima',
                                  'No participe en la gestión pública'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo político de la descentralización '
                             'es:',
                 'alternativas': ['El aislamiento regional',
                                  'La unidad y eficiencia del Estado',
                                  'La eliminación de gobiernos locales',
                                  'La centralización total',
                                  'El debilitamiento del Estado'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo económico de la descentralización '
                             'es:',
                 'alternativas': ['Concentrar recursos en Lima',
                                  'El desarrollo económico autosostenido de '
                                  'las regiones',
                                  'Eliminar la inversión regional',
                                  'Reducir los servicios sociales',
                                  'Aumentar la dependencia central'],
                 'correcta': 'B'},
                {'pregunta': 'Otro objetivo económico de la '
                             'descentralización es la redistribución:',
                 'alternativas': ['Desigual de recursos',
                                  'Equitativa de los recursos del Estado',
                                  'Exclusiva para Lima',
                                  'Solo para zonas urbanas',
                                  'Centralizada de los recursos'],
                 'correcta': 'B'},
                {'pregunta': 'Históricamente, el Perú ha sido caracterizado '
                             'por los analistas como un país:',
                 'alternativas': ['Descentralizado desde su origen',
                                  'Centralista',
                                  'Federal',
                                  'Confederado',
                                  'Sin estructura política definida'],
                 'correcta': 'B'},
                {'pregunta': 'El «descentralismo centralista» se extiende '
                             'desde el inicio de la República hasta:',
                 'alternativas': ['1821', '1920', '1979', '1993', '2002'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'provinieron principalmente de:',
                 'alternativas': ['Las provincias',
                                  'El pensamiento capitalino, de la élite de '
                                  'Lima',
                                  'Los gobiernos regionales actuales',
                                  'Organismos internacionales',
                                  'Los movimientos indígenas'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros proyectos de descentralización '
                             'carecieron de:',
                 'alternativas': ['Respaldo social provinciano',
                                  'Presupuesto estatal',
                                  'Marco legal',
                                  'Apoyo internacional',
                                  'Interés político'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo del federalismo fallido en el Perú '
                             'se ubica entre:',
                 'alternativas': ['1821 y 1873',
                                  '1900 y 1950',
                                  '1979 y 1993',
                                  '1532 y 1821',
                                  '1993 y 2020'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización es descrita como un '
                             'proceso:',
                 'alternativas': ['Unidimensional',
                                  'Multidimensional, con dinámicas '
                                  'políticas, fiscales y administrativas',
                                  'Exclusivamente fiscal',
                                  'Solo administrativo',
                                  'Solo político'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los objetivos generales de la '
                             'descentralización figura la participación de:',
                 'alternativas': ['Solo el gobierno central',
                                  'La sociedad civil',
                                  'Solo las empresas privadas',
                                  'Solo organismos internacionales',
                                  'Solo el sector militar'],
                 'correcta': 'B'},
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
                 'alternativas': ['Gobiernos centralizados',
                                  'Sólidos gobiernos regionales y locales',
                                  'Un solo partido político',
                                  'Regímenes militares',
                                  'Gobiernos temporales'],
                 'correcta': 'B'},
                {'pregunta': 'Un objetivo económico es la cobertura de '
                             'servicios sociales básicos en:',
                 'alternativas': ['Solo la capital',
                                  'Todo el territorio nacional',
                                  'Solo zonas costeras',
                                  'Solo zonas urbanas',
                                  'Solo zonas fronterizas'],
                 'correcta': 'B'},
                {'pregunta': 'El descentralismo formó parte de casi todos '
                             'los proyectos políticos, pero por razones '
                             'estructurales:',
                 'alternativas': ['Se cumplieron totalmente',
                                  'No llegaron a concretarse',
                                  'Fueron rechazados por la población',
                                  'Se aplicaron de inmediato',
                                  'No generaron ningún debate'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización tiene como finalidad el '
                             'desarrollo integral, armónico y:',
                 'alternativas': ['Temporal',
                                  'Sostenible del país',
                                  'Exclusivo de Lima',
                                  'Limitado a la costa',
                                  'Solo económico'],
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
                {'titulo': '16.3 EVOLUCIÓN: EL PRIMER MOMENTO O '
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los derechos humanos incluyen a toda persona por '
                           'el simple hecho de {Su condición humana}.',
                           'Según Hernández Gómez, los derechos humanos son '
                           'condiciones que permiten a la persona {Su '
                           'realización}.',
                           'Que los derechos humanos se apliquen a todos sin '
                           'distinción corresponde a la característica de '
                           '{Universalidad}.',
                           'Que los derechos humanos no se pierdan con el '
                           'paso del tiempo corresponde a que son '
                           '{Imprescriptibles}.',
                           'Que no se pueda hablar de una división de los '
                           'derechos humanos corresponde a que son '
                           '{Indivisibles}.',
                           'Que nadie pueda atentar contra los derechos '
                           'humanos corresponde a que son {Inviolables}.',
                           'Que un derecho reconocido quede integrado de '
                           'forma irrevocable corresponde a que son '
                           '{Irreversibles}.',
                           'Que los derechos humanos formen un conjunto '
                           'inseparable corresponde a que son '
                           '{Indisolubles}.',
                           'Que el Estado deba respetar los derechos humanos '
                           'aunque no exista ley expresa corresponde a que '
                           'son {Obligatorios}.',
                           'Que puedan reconocerse nuevos derechos humanos '
                           'en el futuro corresponde a que son '
                           '{Progresivos}.',
                           'La evolución de los derechos humanos comprende '
                           'dos grandes momentos: la juridificación y {La '
                           'internacionalización}.',
                           'La Carta Magna, o Petición de los Derechos, se '
                           'dio en Inglaterra en el año {1215}.',
                           'El Acta de Independencia de Estados Unidos data '
                           'de {1776}.',
                           'La Declaración de los Derechos del Hombre y del '
                           'Ciudadano corresponde a {Francia, 1789}.',
                           'El periodo de juridificación se caracteriza '
                           'porque los nuevos Estados modernos {Introdujeron '
                           'el reconocimiento y protección de estos derechos '
                           'en sus legislaciones}.',
                           'El periodo de juridificación estuvo imbuido de '
                           'la ideología {Liberal}.',
                           'El ejercicio de rebeliones históricas para '
                           'lograr el reconocimiento de derechos demuestra '
                           'que estos son, en parte {Producto de un proceso '
                           'histórico y social}.',
                           'El derecho a la vida, como derecho inviolable, '
                           'no puede ser violentado {En ninguna '
                           'circunstancia}.',
                           'Los derechos humanos, según su carácter '
                           'obligatorio, deben respetarse {Aunque no exista '
                           'una ley que lo diga expresamente}.']}],
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
                 'alternativas': ['Su nacionalidad',
                                  'Su condición humana',
                                  'Su nivel económico',
                                  'Su religión',
                                  'Su edad'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hernández Gómez, los derechos humanos '
                             'son condiciones que permiten a la persona:',
                 'alternativas': ['Su dependencia del Estado',
                                  'Su realización',
                                  'Su aislamiento',
                                  'Su sometimiento',
                                  'Su exclusión social'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos se apliquen a todos '
                             'sin distinción corresponde a la característica '
                             'de:',
                 'alternativas': ['Imprescriptibilidad',
                                  'Universalidad',
                                  'Indivisibilidad',
                                  'Progresividad',
                                  'Obligatoriedad'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos no se pierdan con el '
                             'paso del tiempo corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Imprescriptibles',
                                  'Indisolubles',
                                  'Inviolables',
                                  'Progresivos'],
                 'correcta': 'B'},
                {'pregunta': 'Que no se pueda hablar de una división de los '
                             'derechos humanos corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Indivisibles',
                                  'Progresivos',
                                  'Obligatorios',
                                  'Irreversibles'],
                 'correcta': 'B'},
                {'pregunta': 'Que nadie pueda atentar contra los derechos '
                             'humanos corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Inviolables',
                                  'Imprescriptibles',
                                  'Indisolubles',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Que un derecho reconocido quede integrado de '
                             'forma irrevocable corresponde a que son:',
                 'alternativas': ['Indivisibles',
                                  'Irreversibles',
                                  'Obligatorios',
                                  'Universales',
                                  'Progresivos'],
                 'correcta': 'B'},
                {'pregunta': 'Que los derechos humanos formen un conjunto '
                             'inseparable corresponde a que son:',
                 'alternativas': ['Universales',
                                  'Indisolubles',
                                  'Imprescriptibles',
                                  'Inviolables',
                                  'Progresivos'],
                 'correcta': 'B'},
                {'pregunta': 'Que el Estado deba respetar los derechos '
                             'humanos aunque no exista ley expresa '
                             'corresponde a que son:',
                 'alternativas': ['Progresivos',
                                  'Obligatorios',
                                  'Indivisibles',
                                  'Irreversibles',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Que puedan reconocerse nuevos derechos humanos '
                             'en el futuro corresponde a que son:',
                 'alternativas': ['Imprescriptibles',
                                  'Progresivos',
                                  'Inviolables',
                                  'Indisolubles',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'La evolución de los derechos humanos comprende '
                             'dos grandes momentos: la juridificación y:',
                 'alternativas': ['La militarización',
                                  'La internacionalización',
                                  'La privatización',
                                  'La regionalización',
                                  'La secularización'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta Magna, o Petición de los Derechos, se '
                             'dio en Inglaterra en el año:',
                 'alternativas': ['1679', '1215', '1789', '1776', '1948'],
                 'correcta': 'B'},
                {'pregunta': 'La Ley de Habeas Corpus fue dictada en '
                             'Inglaterra en:',
                 'alternativas': ['1215', '1679', '1776', '1789', '1948'],
                 'correcta': 'B'},
                {'pregunta': 'El Acta de Independencia de Estados Unidos '
                             'data de:',
                 'alternativas': ['1215', '1679', '1776', '1789', '1948'],
                 'correcta': 'C'},
                {'pregunta': 'La Declaración de los Derechos del Hombre y '
                             'del Ciudadano corresponde a:',
                 'alternativas': ['Inglaterra, 1215',
                                  'Francia, 1789',
                                  'Estados Unidos, 1776',
                                  'España, 1812',
                                  'Alemania, 1919'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de juridificación se caracteriza '
                             'porque los nuevos Estados modernos:',
                 'alternativas': ['Rechazaron los derechos humanos',
                                  'Introdujeron el reconocimiento y '
                                  'protección de estos derechos en sus '
                                  'legislaciones',
                                  'Eliminaron toda garantía legal',
                                  'Centralizaron el poder absoluto',
                                  'Prohibieron su difusión'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de juridificación estuvo imbuido de '
                             'la ideología:',
                 'alternativas': ['Conservadora',
                                  'Liberal',
                                  'Socialista',
                                  'Absolutista',
                                  'Monárquica'],
                 'correcta': 'B'},
                {'pregunta': 'El ejercicio de rebeliones históricas para '
                             'lograr el reconocimiento de derechos demuestra '
                             'que estos son, en parte:',
                 'alternativas': ['Otorgados sin lucha por el Estado',
                                  'Producto de un proceso histórico y social',
                                  'Ajenos a la evolución humana',
                                  'Impuestos por organismos internacionales',
                                  'Exclusivos de una nación'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho a la vida, como derecho inviolable, '
                             'no puede ser violentado:',
                 'alternativas': ['En ninguna circunstancia',
                                  'Solo en situaciones de guerra',
                                  'Solo por decisión judicial',
                                  'Solo temporalmente',
                                  'Bajo excepciones económicas'],
                 'correcta': 'A'},
                {'pregunta': 'Los derechos humanos, según su carácter '
                             'obligatorio, deben respetarse:',
                 'alternativas': ['Solo si están en la ley nacional',
                                  'Aunque no exista una ley que lo diga '
                                  'expresamente',
                                  'Solo por decisión del gobierno de turno',
                                  'Solo en situaciones normales',
                                  'Solo si lo exige un tratado'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El término «garantía» se define como la '
                           'seguridad o protección frente a {Un peligro en '
                           'el disfrute de los derechos}.',
                           'En el Perú, la institucionalidad de las '
                           'garantías se inicia con la Constitución de '
                           '{1920}.',
                           'La Constitución de 1920 distinguió tres tipos de '
                           'garantías: nacionales, individuales y '
                           '{Sociales}.',
                           'Según García Toma, las Garantías '
                           'Constitucionales aseguran el disfrute de los '
                           'derechos {Públicos y privados}.',
                           'El artículo de la Constitución de 1993 que '
                           'establece las Garantías Constitucionales es el '
                           '{Artículo 200}.',
                           'El número de Garantías Constitucionales '
                           'establecidas en el artículo 200 es {Seis}.',
                           'La primera garantía constitucional reconocida en '
                           'el Perú, en 1920, fue {El Habeas Corpus}.',
                           'La Acción Popular fue incorporada en la '
                           'Constitución de {1933}.',
                           'La Acción de Amparo y la Acción de '
                           'Inconstitucionalidad se incorporaron en la '
                           'Constitución de {1979}.',
                           'El Habeas Data y la Acción de Cumplimiento se '
                           'incorporaron en la Constitución de {1993}.',
                           'La expresión «habeas corpus» significa '
                           'literalmente {Que traigas el cuerpo}.',
                           'El antecedente histórico del habeas corpus es la '
                           'ley inglesa de {1679}.',
                           'El habeas corpus protege principalmente {La '
                           'libertad individual y la seguridad personal}.',
                           'El habeas corpus se presenta, en primera '
                           'instancia, ante {El Juez especializado en lo '
                           'Penal}.',
                           'Si no hay Juez Penal disponible, el habeas '
                           'corpus se presenta ante {El Juez de Paz '
                           'Letrado}.',
                           'La última y definitiva instancia para resolver '
                           'denegatorias de habeas corpus es {El Tribunal '
                           'Constitucional}.',
                           'La acción de habeas corpus se caracteriza por '
                           'estar exenta de {Formalidades}.',
                           'El habeas corpus puede formularse {Por escrito o '
                           'verbalmente, en forma directa o por correo}.']}],
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
                                  'Una obligación tributaria',
                                  'Un contrato civil',
                                  'Una sanción administrativa'],
                 'correcta': 'B'},
                {'pregunta': 'Las Garantías Constitucionales tienen su '
                             'origen en la tradición:',
                 'alternativas': ['Inglesa',
                                  'Francesa',
                                  'Alemana',
                                  'Española',
                                  'Romana'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, la institucionalidad de las '
                             'garantías se inicia con la Constitución de:',
                 'alternativas': ['1979', '1920', '1993', '1933', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución de 1920 distinguió tres tipos '
                             'de garantías: nacionales, individuales y:',
                 'alternativas': ['Económicas',
                                  'Sociales',
                                  'Militares',
                                  'Religiosas',
                                  'Culturales'],
                 'correcta': 'B'},
                {'pregunta': 'Según García Toma, las Garantías '
                             'Constitucionales aseguran el disfrute de los '
                             'derechos:',
                 'alternativas': ['Solo públicos',
                                  'Públicos y privados',
                                  'Solo privados',
                                  'Solo económicos',
                                  'Solo políticos'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo de la Constitución de 1993 que '
                             'establece las Garantías Constitucionales es '
                             'el:',
                 'alternativas': ['Artículo 91',
                                  'Artículo 200',
                                  'Artículo 51',
                                  'Artículo 149',
                                  'Artículo 24'],
                 'correcta': 'B'},
                {'pregunta': 'El número de Garantías Constitucionales '
                             'establecidas en el artículo 200 es:',
                 'alternativas': ['Cuatro', 'Seis', 'Ocho', 'Tres', 'Diez'],
                 'correcta': 'B'},
                {'pregunta': 'La primera garantía constitucional reconocida '
                             'en el Perú, en 1920, fue:',
                 'alternativas': ['La Acción Popular',
                                  'El Habeas Corpus',
                                  'El Habeas Data',
                                  'La Acción de Amparo',
                                  'La Acción de Cumplimiento'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción Popular fue incorporada en la '
                             'Constitución de:',
                 'alternativas': ['1920', '1933', '1979', '1993', '1856'],
                 'correcta': 'B'},
                {'pregunta': 'La Acción de Amparo y la Acción de '
                             'Inconstitucionalidad se incorporaron en la '
                             'Constitución de:',
                 'alternativas': ['1920', '1933', '1979', '1993', '1856'],
                 'correcta': 'C'},
                {'pregunta': 'El Habeas Data y la Acción de Cumplimiento se '
                             'incorporaron en la Constitución de:',
                 'alternativas': ['1920', '1933', '1979', '1993', '1856'],
                 'correcta': 'D'},
                {'pregunta': 'La expresión «habeas corpus» significa '
                             'literalmente:',
                 'alternativas': ['Protege al pueblo',
                                  'Que traigas el cuerpo',
                                  'Libertad total',
                                  'Justicia inmediata',
                                  'Derecho supremo'],
                 'correcta': 'B'},
                {'pregunta': 'El antecedente histórico del habeas corpus es '
                             'la ley inglesa de:',
                 'alternativas': ['1215', '1679', '1789', '1948', '1993'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus protege principalmente:',
                 'alternativas': ['La propiedad privada',
                                  'La libertad individual y la seguridad '
                                  'personal',
                                  'El comercio exterior',
                                  'Los derechos laborales exclusivamente',
                                  'La libertad de prensa únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'El habeas corpus se presenta, en primera '
                             'instancia, ante:',
                 'alternativas': ['El Tribunal Constitucional',
                                  'El Juez especializado en lo Penal',
                                  'El Congreso',
                                  'El Ministerio Público',
                                  'La Defensoría del Pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'Si no hay Juez Penal disponible, el habeas '
                             'corpus se presenta ante:',
                 'alternativas': ['El Juez de Paz Letrado',
                                  'El Alcalde',
                                  'El Fiscal de la Nación',
                                  'El Presidente de la Corte Suprema',
                                  'El Defensor del Pueblo'],
                 'correcta': 'A'},
                {'pregunta': 'La última y definitiva instancia para resolver '
                             'denegatorias de habeas corpus es:',
                 'alternativas': ['La Corte Suprema',
                                  'El Tribunal Constitucional',
                                  'El Congreso',
                                  'La Defensoría del Pueblo',
                                  'El Ministerio Público'],
                 'correcta': 'B'},
                {'pregunta': 'La acción de habeas corpus se caracteriza por '
                             'estar exenta de:',
                 'alternativas': ['Plazos procesales',
                                  'Formalidades',
                                  'Revisión judicial',
                                  'Competencia territorial',
                                  'Sustento fáctico'],
                 'correcta': 'B'},
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
                                  'Por escrito o verbalmente, en forma '
                                  'directa o por correo',
                                  'Únicamente en audiencia pública',
                                  'Solo mediante representante legal',
                                  'Exclusivamente por vía electrónica'],
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
                 'alternativas': ['La OEA',
                                  'La Sociedad de Naciones',
                                  'La OTAN',
                                  'La Cruz Roja',
                                  'El Pacto Andino'],
                 'correcta': 'B'},
                {'pregunta': 'La Sociedad de Naciones se estableció en el '
                             'año:',
                 'alternativas': ['1914', '1919', '1939', '1945', '1918'],
                 'correcta': 'B'},
                {'pregunta': 'La Sociedad de Naciones se estableció en '
                             'virtud del Tratado de:',
                 'alternativas': ['Versalles',
                                  'Ancón',
                                  'Ginebra',
                                  'Roma',
                                  'Westfalia'],
                 'correcta': 'A'},
                {'pregunta': 'El fracaso de la Sociedad de Naciones '
                             'desembocó en:',
                 'alternativas': ['La Primera Guerra Mundial',
                                  'La Segunda Guerra Mundial',
                                  'La Guerra Fría',
                                  'La Guerra de Corea',
                                  'La Revolución Rusa'],
                 'correcta': 'B'},
                {'pregunta': 'El nombre «Naciones Unidas» fue acuñado por:',
                 'alternativas': ['Winston Churchill',
                                  'Franklin D. Roosevelt',
                                  'Joseph Stalin',
                                  'Harry Truman',
                                  'Woodrow Wilson'],
                 'correcta': 'B'},
                {'pregunta': 'El nombre «Naciones Unidas» se usó por primera '
                             'vez en:',
                 'alternativas': ['1919', '1942', '1945', '1939', '1950'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta de las Naciones Unidas fue firmada el '
                             '26 de junio de:',
                 'alternativas': ['1942', '1945', '1919', '1939', '1950'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta de la ONU fue firmada inicialmente '
                             'por:',
                 'alternativas': ['26 países',
                                  '50 países',
                                  '100 países',
                                  '193 países',
                                  '10 países'],
                 'correcta': 'B'},
                {'pregunta': 'Las Naciones Unidas empezaron a existir '
                             'oficialmente el:',
                 'alternativas': ['1 de enero de 1942',
                                  '24 de octubre de 1945',
                                  '26 de junio de 1945',
                                  '10 de diciembre de 1948',
                                  '1 de enero de 1945'],
                 'correcta': 'B'},
                {'pregunta': 'El 24 de octubre se celebra como:',
                 'alternativas': ['El Día de los Derechos Humanos',
                                  'El Día de las Naciones Unidas',
                                  'El Día de la Paz Mundial',
                                  'El Día de la Democracia',
                                  'El Día del Multilateralismo'],
                 'correcta': 'B'},
                {'pregunta': 'La ONU tiene actualmente un número de Estados '
                             'Miembros de:',
                 'alternativas': ['100', '193', '51', '150', '250'],
                 'correcta': 'B'},
                {'pregunta': 'La sede principal de la ONU se ubica en:',
                 'alternativas': ['Ginebra',
                                  'Nueva York',
                                  'Viena',
                                  'Nairobi',
                                  'París'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las sedes secundarias de la ONU figura:',
                 'alternativas': ['Madrid',
                                  'Ginebra',
                                  'Londres',
                                  'Roma',
                                  'Berlín'],
                 'correcta': 'B'},
                {'pregunta': 'Los idiomas oficiales de la ONU son seis, '
                             'entre ellos figura:',
                 'alternativas': ['El portugués',
                                  'El árabe',
                                  'El alemán',
                                  'El italiano',
                                  'El japonés'],
                 'correcta': 'B'},
                {'pregunta': 'La ONU está compuesta por un número de órganos '
                             'principales igual a:',
                 'alternativas': ['Cuatro', 'Seis', 'Ocho', 'Diez', 'Tres'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano de la ONU encargado de la paz y '
                             'seguridad internacional es:',
                 'alternativas': ['La Asamblea General',
                                  'El Consejo de Seguridad',
                                  'El Consejo Económico y Social',
                                  'La Corte Internacional de Justicia',
                                  'El Secretario General'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano judicial principal de la ONU es:',
                 'alternativas': ['El Consejo de Seguridad',
                                  'La Corte Internacional de Justicia',
                                  'La Asamblea General',
                                  'El Consejo Económico y Social',
                                  'El Consejo de Administración Fiduciaria'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los fines de la ONU figura defender y '
                             'garantizar:',
                 'alternativas': ['Solo el comercio internacional',
                                  'Los Derechos Humanos',
                                  'Solo la moneda internacional',
                                  'Solo la seguridad militar',
                                  'Solo el turismo'],
                 'correcta': 'B'},
                {'pregunta': 'Un Estado que infringe los principios de la '
                             'Carta de la ONU puede ser:',
                 'alternativas': ['Premiado',
                                  'Excluido temporalmente o expulsado',
                                  'Ignorado sin consecuencias',
                                  'Automáticamente disuelto',
                                  'Anexado a otro país'],
                 'correcta': 'B'},
                {'pregunta': 'Estados no miembros de la ONU, como el '
                             'Vaticano, pueden tener estatuto de:',
                 'alternativas': ['Miembro pleno',
                                  'Observador, sin derecho a voto',
                                  'Fundador',
                                  'Excluido total',
                                  'Sancionado permanente'],
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
