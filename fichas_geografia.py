# ================================================================
# FICHAS DE GEOGRAFÍA — CEPRU UNSAAC
# Basado en el material oficial «Geografía del Perú y del Mundo»,
# Área D, Ciclo Primera Oportunidad.
# ================================================================
"""Mismo formato que el módulo de Historia: por cada tema genera la
ficha de texto para completar a dos columnas y el banco de 20
preguntas con cinco alternativas, en versión alumno y versión docente.

Reutiliza el motor de fichas_historia.py en lugar de duplicarlo.

Integración en sistema_web.py:
    from fichas_geografia import tab_fichas_geografia

ESTADO: el temario oficial tiene 18 temas. Esta primera entrega
incluye el Tema 1 (Geografía y espacio geográfico), completo y listo
para imprimir, como muestra del formato. Los temas 2 a 18 se agregan a
GEOGRAFIA_TEMAS de la misma manera.

NOTA sobre mapas y gráficos: el libro trae mapas, fotos y diagramas
(sobre todo en el Tema 4 «Mapas: lectura e interpretación» y el Tema 17
«Espacio geográfico del Cusco»). El motor actual de fichas es de texto
para completar, así que esos temas se trabajan como listas de
elementos/leyenda para completar y cuadros comparativos en vez de un
mapa dibujado; si se necesita un mapa mudo real para imprimir, se puede
armar aparte (por ejemplo en Word con una imagen del mapa y espacios en
blanco al lado) cuando lleguemos a ese tema.
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


GEOGRAFIA_TEMAS = [{'num': 1,
  'titulo': 'Geografía y Espacio Geográfico',
  'secciones': [{'titulo': '1.1 LA GEOGRAFÍA: ETIMOLOGÍA Y EVOLUCIÓN',
                 'items': ['El término Geografía proviene de dos voces '
                           'griegas: {Geo} = Tierra y {Graphía} = '
                           'Descripción.',
                           '{Alejandro Von Humboldt} y {Carlos Ritter} '
                           'iniciaron en la Época Moderna una nueva era de '
                           'la Geografía.',
                           '{Eratóstenes} (276-196 a.C.) calculó la '
                           'circunferencia terrestre con notable '
                           'aproximación y elaboró un mapamundi.',
                           '{Claudio Ptolomeo} (90-168 d.C.) fue el primero '
                           'en hacer un Atlas Universal.',
                           'Durante la {Edad Media}, la Geografía sufrió un '
                           'retroceso u oscurantismo debido a la concepción '
                           'teocéntrica.']},
                {'titulo': '1.2 ETAPAS DEL PENSAMIENTO GEOGRÁFICO',
                 'items': ['La {Geografía Antigua} comprende desde los '
                           'tiempos primitivos hasta mediados del siglo '
                           '{XIX}; era empírica y rutinaria, y formaba parte '
                           'de la {filosofía}.',
                           'La {Geografía Moderna o Científica} va de '
                           'mediados del siglo XIX a mediados del siglo XX; '
                           'se fundamenta en el {positivismo} y usa el '
                           'método {inductivo}.',
                           'En la Geografía Moderna, el hombre aparece como '
                           'un elemento más del {paisaje}, y la disciplina '
                           'es considerada una ciencia de {síntesis}.',
                           'La {Geografía Nueva, Cuantitativa o Teorética} '
                           'se desarrolla desde mediados del siglo XX hasta '
                           'la actualidad; se fundamenta en el '
                           '{Neopositivismo} o Positivismo Lógico.',
                           'La Geografía Nueva utiliza el método '
                           '{deductivo}, el concepto de espacio {relativo} y '
                           'herramientas como GPS y sensores remotos.',
                           'Representantes de la Geografía Nueva: {Milton '
                           'Santos}, Fred Kurt Schaefer y William Bunge.',
                           '{Karl Ritter}, junto con Alexander von Humboldt, '
                           'es considerado fundador de la Geografía '
                           '{Moderna} o Científica.',
                           'En la Geografía Antigua destacaron '
                           '{Eratóstenes}, quien calculó la circunferencia '
                           'terrestre, y {Claudio Ptolomeo}, el primero en '
                           'elaborar un Atlas Universal.']},
                {'titulo': '1.3 EL ESPACIO GEOGRÁFICO: OBJETO DE ESTUDIO',
                 'items': ['Para {Milton Santos da Almeida}, el Espacio '
                           'Geográfico es el objeto de estudio de la ciencia '
                           'geográfica.',
                           'Según {Jean Tricart}, el espacio geográfico «es '
                           'la epidermis del planeta Tierra».',
                           'Según Milton Santos, el espacio geográfico es '
                           '«la {naturaleza} modificada por el hombre a '
                           'través del {trabajo}».',
                           'Elementos {naturales} del espacio geográfico: '
                           'flora, fauna, relieve, rocas, minerales, mares, '
                           'ríos, entre otros no intervenidos por el hombre.',
                           'Elementos {culturales} del espacio geográfico: '
                           'viviendas, ciudades, vías de comunicación, '
                           'agricultura, minería, industria: creaciones del '
                           'hombre.']},
                {'titulo': '1.4 DIVISIÓN DE LA GEOGRAFÍA',
                 'items': ['La {Geografía Física} estudia los objetos '
                           'naturales, abióticos y bióticos: Geomorfología, '
                           'Climatología, Edafología, Hidrogeografía y '
                           'Biogeografía.',
                           'La {Geomorfología} estudia el origen, evolución '
                           'y formas del relieve; la {Climatología} estudia '
                           'los climas del mundo.',
                           'La {Hidrogeografía} estudia la distribución de '
                           'las aguas, y se subdivide en {Oceanografía} '
                           '(océanos y mares), {Fluviología} (ríos) y '
                           '{Limnología} (lagos).',
                           'La {Biogeografía} se subdivide en '
                           '{Fitogeografía} (distribución de las plantas) y '
                           '{Zoogeografía} (distribución de los animales).',
                           'La {Geografía Humana} estudia las agrupaciones '
                           'humanas en relación con el medio geográfico, '
                           'desde el punto de vista social, económico y '
                           'político.',
                           'La Geografía Humana comprende: Geografía '
                           '{Política}, Geografía {Económica}, '
                           '{Demogeografía}, Geografía {Histórica}, '
                           'Geografía {Urbana} y Geografía {Rural}.']},
                {'titulo': '1.5 PRINCIPIOS METODOLÓGICOS DE LA INVESTIGACIÓN '
                           'GEOGRÁFICA',
                 'items': ['Principio de {Localización, Distribución o '
                           'Extensión} ({Federico Ratzel}): todo elemento '
                           'debe ser ubicado en mapas y cartas geográficas.',
                           'Principio de {Causalidad o Explicación} '
                           '({Alejandro Von Humboldt}): el estudio debe '
                           'analizar causas y consecuencias.',
                           'Principio de {Relación o Conexión} ({Jean '
                           'Brunhes}): los elementos del espacio geográfico '
                           'están en íntima interdependencia.',
                           'Principio de {Comparación} ({Carlos Ritter} y '
                           '{Vidal de la Blache}): consiste en comparar los '
                           'elementos por su semejanza u oposición.',
                           'Principio de {Actividad, Dinamismo o Evolución} '
                           '({Jean Brunhes}): los elementos geográficos '
                           'están en constante transformación.']},
                {'titulo': '1.6 GEOGRAFÍA APLICADA E IMPORTANCIA',
                 'items': ['La {Geografía Aplicada} orienta los estudios e '
                           'investigaciones hacia soluciones prácticas de '
                           'problemas territoriales.',
                           'Herramientas de la Geografía Aplicada: '
                           'cartografía digital, {Sistemas de Información '
                           'Geográfica (SIG)} y {teledetección}.',
                           'El planeta Tierra tiene un hábitat de 510 '
                           'millones de km², dividido políticamente en {193} '
                           'países, con una población de {7 450} millones de '
                           'habitantes (Censo EE.UU. 2018).']}],
  'cuadros': [{'titulo': '1.4.1 RAMAS DE LA GEOGRAFÍA FÍSICA',
               'encabezados': ['Rama', 'Objeto de estudio'],
               'filas': [['Geomorfología',
                          '{Origen, evolución y formas del relieve}'],
                         ['Climatología', '{Climas del mundo}'],
                         ['Edafología o Pedología',
                          '{Suelos, su origen y sus clases}'],
                         ['Hidrogeografía',
                          '{Distribución de las aguas en la superficie '
                          'terrestre}'],
                         ['Biogeografía',
                          '{Elementos vivientes: plantas y animales}']]}],
  'preguntas': [{'pregunta': 'Etimológicamente, la palabra Geografía '
                             'proviene del griego «Geo» y «Graphía», que '
                             'significan:',
                 'alternativas': ['Suelo y medición',
                                  'Tierra y ciencia',
                                  'Espacio y estudio',
                                  'Mundo y espacio',
                                  'Tierra y descripción'],
                 'correcta': 'E'},
                {'pregunta': 'Los geógrafos que iniciaron, en la Época '
                             'Moderna, una nueva era de la Geografía fueron:',
                 'alternativas': ['Eratóstenes y Ptolomeo',
                                  'Vidal de la Blache y Schaefer',
                                  'Ratzel y Brunhes',
                                  'Von Humboldt y Carlos Ritter',
                                  'Milton Santos y Bunge'],
                 'correcta': 'D'},
                {'pregunta': 'El geógrafo que calculó la circunferencia '
                             'terrestre con notable aproximación y elaboró '
                             'un mapamundi fue:',
                 'alternativas': ['Carlos Ritter',
                                  'Claudio Ptolomeo',
                                  'Jean Brunhes',
                                  'Federico Ratzel',
                                  'Eratóstenes'],
                 'correcta': 'E'},
                {'pregunta': 'El primero en elaborar un Atlas Universal fue:',
                 'alternativas': ['Vidal de la Blache',
                                  'Von Humboldt',
                                  'Eratóstenes',
                                  'Claudio Ptolomeo',
                                  'Milton Santos'],
                 'correcta': 'D'},
                {'pregunta': 'La etapa del pensamiento geográfico que va '
                             'desde los tiempos primitivos hasta mediados '
                             'del siglo XIX, de carácter empírico y '
                             'rutinario, es la Geografía:',
                 'alternativas': ['Antigua',
                                  'Nueva',
                                  'Cuantitativa',
                                  'Teorética',
                                  'Científica'],
                 'correcta': 'A'},
                {'pregunta': 'La Geografía Moderna o Científica se '
                             'fundamenta en la filosofía del:',
                 'alternativas': ['Neopositivismo',
                                  'Positivismo',
                                  'Empirismo',
                                  'Estructuralismo',
                                  'Racionalismo'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que se fundamenta en el '
                             'Neopositivismo o Positivismo Lógico y utiliza '
                             'el método deductivo es la Geografía:',
                 'alternativas': ['Descriptiva',
                                  'Nueva, Cuantitativa o Teorética',
                                  'Moderna',
                                  'Antigua',
                                  'Regional clásica'],
                 'correcta': 'B'},
                {'pregunta': 'Según Milton Santos da Almeida, el espacio '
                             'geográfico es:',
                 'alternativas': ['La naturaleza modificada por el hombre a '
                                  'través del trabajo',
                                  'La suma de climas y relieves',
                                  'El marco físico de toda acción humana',
                                  'El territorio de un Estado',
                                  'La epidermis del planeta Tierra'],
                 'correcta': 'A'},
                {'pregunta': 'La flora, la fauna y la diversidad de relieves '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Sociales',
                                  'Económicos',
                                  'Culturales',
                                  'Naturales',
                                  'Políticos'],
                 'correcta': 'D'},
                {'pregunta': 'Las viviendas, ciudades y vías de comunicación '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Naturales',
                                  'Culturales',
                                  'Climáticos',
                                  'Bióticos',
                                  'Abióticos'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la Geografía Física que estudia el '
                             'origen, evolución y formas del relieve es la:',
                 'alternativas': ['Climatología',
                                  'Geomorfología',
                                  'Hidrogeografía',
                                  'Edafología',
                                  'Biogeografía'],
                 'correcta': 'B'},
                {'pregunta': 'Dentro de la Hidrogeografía, el estudio de los '
                             'ríos corresponde a la:',
                 'alternativas': ['Edafología',
                                  'Limnología',
                                  'Fitogeografía',
                                  'Fluviología',
                                  'Oceanografía'],
                 'correcta': 'D'},
                {'pregunta': 'Dentro de la Biogeografía, el estudio de la '
                             'distribución de los animales corresponde a la:',
                 'alternativas': ['Demogeografía',
                                  'Zoogeografía',
                                  'Limnología',
                                  'Oceanografía',
                                  'Fitogeografía'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la Geografía Humana que estudia la '
                             'distribución de la población en la superficie '
                             'terrestre es la:',
                 'alternativas': ['Geografía Histórica',
                                  'Geografía Rural',
                                  'Demogeografía',
                                  'Geografía Urbana',
                                  'Geografía Política'],
                 'correcta': 'C'},
                {'pregunta': 'El principio metodológico según el cual todo '
                             'elemento del espacio geográfico debe ser '
                             'ubicado en mapas y cartas geográficas, '
                             'formulado por Federico Ratzel, es el de:',
                 'alternativas': ['Relación o Conexión',
                                  'Localización, Distribución o Extensión',
                                  'Comparación',
                                  'Actividad o Dinamismo',
                                  'Causalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de Causalidad o Explicación, que '
                             'establece que todo elemento debe analizarse '
                             'por sus causas y consecuencias, fue formulado '
                             'por:',
                 'alternativas': ['Vidal de la Blache',
                                  'Alejandro Von Humboldt',
                                  'Federico Ratzel',
                                  'Jean Brunhes',
                                  'Carlos Ritter'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que establece que los elementos '
                             'del espacio geográfico están en íntima '
                             'interdependencia, formulado por Jean Brunhes, '
                             'es el de:',
                 'alternativas': ['Comparación',
                                  'Localización',
                                  'Actividad',
                                  'Causalidad',
                                  'Relación o Conexión'],
                 'correcta': 'E'},
                {'pregunta': 'El principio de Comparación, también llamado '
                             'de Coordinación, Universalización o Analogía, '
                             'fue formulado por:',
                 'alternativas': ['Von Humboldt y Ptolomeo',
                                  'Schaefer y Bunge',
                                  'Eratóstenes y Milton Santos',
                                  'Federico Ratzel y Jean Brunhes',
                                  'Carlos Ritter y Vidal de la Blache'],
                 'correcta': 'E'},
                {'pregunta': 'Que los elementos del espacio geográfico deban '
                             'estudiarse en su constante y perpetua '
                             'transformación corresponde al principio de:',
                 'alternativas': ['Relación',
                                  'Actividad, Dinamismo o Evolución',
                                  'Comparación',
                                  'Causalidad',
                                  'Localización'],
                 'correcta': 'B'},
                {'pregunta': 'Herramientas propias de la Geografía Aplicada '
                             'para la gestión del territorio son:',
                 'alternativas': ['La cartografía digital, los SIG y la '
                                  'teledetección',
                                  'Únicamente encuestas de campo',
                                  'Los censos poblacionales',
                                  'Los tratados internacionales',
                                  'Solo mapas físicos en papel'],
                 'correcta': 'A'},
                {'pregunta': 'Junto con Alexander von Humboldt, el geógrafo '
                             'considerado fundador de la Geografía Moderna '
                             'es:',
                 'alternativas': ['Fred Schaefer',
                                  'Karl Ritter',
                                  'Eratóstenes',
                                  'William Bunge',
                                  'Milton Santos'],
                 'correcta': 'B'},
                {'pregunta': 'En la Geografía Antigua, el geógrafo que '
                             'calculó la circunferencia terrestre con '
                             'notable aproximación fue:',
                 'alternativas': ['Estrabón',
                                  'Alexander von Humboldt',
                                  'Claudio Ptolomeo',
                                  'Eratóstenes',
                                  'Karl Ritter'],
                 'correcta': 'D'},
                {'pregunta': 'La ciencia que se encarga de estudiar la '
                             'distribución de plantas y animales en el '
                             'espacio geográfico es la: (I CEPRU 2024)',
                 'alternativas': ['Demogeografía',
                                  'Biología',
                                  'Hidrogeografía',
                                  'Edafología',
                                  'Biogeografía'],
                 'correcta': 'E'},
                {'pregunta': 'El origen, estructura y clases de suelos es '
                             'estudiado por la: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['Geomorfología',
                                  'Edafología',
                                  'Fisiografía',
                                  'Geología',
                                  'Limnología'],
                 'correcta': 'B'},
                {'pregunta': 'El objeto de estudio de la Ciencia geográfica '
                             'es el: (Primera Oportunidad UNSAAC 2023)',
                 'alternativas': ['Ecosistema del hombre',
                                  'Geosistema del universo',
                                  'Fenómeno global de la Tierra',
                                  'Espacio terrestre',
                                  'Espacio geográfico'],
                 'correcta': 'E'},
                {'pregunta': 'El principio de Dinamismo se le atribuye a: '
                             '(Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Jean Brunhes',
                                  'Karl Ritter',
                                  'P. Vidal de la Blache',
                                  'Federico Ratzel',
                                  'A. Von Humboldt'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'LA GEOGRAFÍA: ETIMOLOGÍA Y EVOLUCIÓN',
                      'items': ['El término Geografía proviene de dos voces '
                                'griegas: Geo = Tierra y Graphía = '
                                'Descripción.',
                                'Alejandro Von Humboldt y Carlos Ritter '
                                'iniciaron en la Época Moderna una nueva era '
                                'de la Geografía.',
                                'Eratóstenes (276-196 a.C.) calculó la '
                                'circunferencia terrestre con notable '
                                'aproximación y elaboró un mapamundi.',
                                'Claudio Ptolomeo (90-168 d.C.) fue el '
                                'primero en hacer un Atlas Universal.',
                                'Durante la Edad Media, la Geografía sufrió '
                                'un retroceso u oscurantismo debido a la '
                                'concepción teocéntrica.']},
                     {'titulo': 'ETAPAS DEL PENSAMIENTO GEOGRÁFICO',
                      'items': ['La Geografía Antigua comprende desde los '
                                'tiempos primitivos hasta mediados del siglo '
                                'XIX; era empírica y rutinaria, y formaba '
                                'parte de la filosofía.',
                                'La Geografía Moderna o Científica va de '
                                'mediados del siglo XIX a mediados del siglo '
                                'XX; se fundamenta en el positivismo y usa '
                                'el método inductivo.',
                                'En la Geografía Moderna, el hombre aparece '
                                'como un elemento más del paisaje, y la '
                                'disciplina es considerada una ciencia de '
                                'síntesis.',
                                'La Geografía Nueva, Cuantitativa o '
                                'Teorética se desarrolla desde mediados del '
                                'siglo XX hasta la actualidad; se fundamenta '
                                'en el Neopositivismo o Positivismo Lógico.',
                                'La Geografía Nueva utiliza el método '
                                'deductivo, el concepto de espacio relativo '
                                'y herramientas como GPS y sensores remotos.',
                                'Representantes de la Geografía Nueva: '
                                'Milton Santos, Fred Kurt Schaefer y William '
                                'Bunge.',
                                'Karl Ritter, junto con Alexander von '
                                'Humboldt, es considerado fundador de la '
                                'Geografía Moderna o Científica.',
                                'En la Geografía Antigua destacaron '
                                'Eratóstenes, quien calculó la '
                                'circunferencia terrestre, y Claudio '
                                'Ptolomeo, el primero en elaborar un Atlas '
                                'Universal.']},
                     {'titulo': 'EL ESPACIO GEOGRÁFICO: OBJETO DE ESTUDIO',
                      'items': ['Para Milton Santos da Almeida, el Espacio '
                                'Geográfico es el objeto de estudio de la '
                                'ciencia geográfica.',
                                'Según Jean Tricart, el espacio geográfico '
                                '«es la epidermis del planeta Tierra».',
                                'Según Milton Santos, el espacio geográfico '
                                'es «la naturaleza modificada por el hombre '
                                'a través del trabajo».',
                                'Elementos naturales del espacio geográfico: '
                                'flora, fauna, relieve, rocas, minerales, '
                                'mares, ríos, entre otros no intervenidos '
                                'por el hombre.',
                                'Elementos culturales del espacio '
                                'geográfico: viviendas, ciudades, vías de '
                                'comunicación, agricultura, minería, '
                                'industria: creaciones del hombre.']},
                     {'titulo': 'DIVISIÓN DE LA GEOGRAFÍA',
                      'items': ['La Geografía Física estudia los objetos '
                                'naturales, abióticos y bióticos: '
                                'Geomorfología, Climatología, Edafología, '
                                'Hidrogeografía y Biogeografía.',
                                'La Geomorfología estudia el origen, '
                                'evolución y formas del relieve; la '
                                'Climatología estudia los climas del mundo.',
                                'La Hidrogeografía estudia la distribución '
                                'de las aguas, y se subdivide en '
                                'Oceanografía (océanos y mares), Fluviología '
                                '(ríos) y Limnología (lagos).',
                                'La Biogeografía se subdivide en '
                                'Fitogeografía (distribución de las plantas) '
                                'y Zoogeografía (distribución de los '
                                'animales).',
                                'La Geografía Humana estudia las '
                                'agrupaciones humanas en relación con el '
                                'medio geográfico, desde el punto de vista '
                                'social, económico y político.',
                                'La Geografía Humana comprende: Geografía '
                                'Política, Geografía Económica, '
                                'Demogeografía, Geografía Histórica, '
                                'Geografía Urbana y Geografía Rural.']},
                     {'titulo': 'PRINCIPIOS METODOLÓGICOS DE LA '
                                'INVESTIGACIÓN GEOGRÁFICA',
                      'items': ['Principio de Localización, Distribución o '
                                'Extensión (Federico Ratzel): todo elemento '
                                'debe ser ubicado en mapas y cartas '
                                'geográficas.',
                                'Principio de Causalidad o Explicación '
                                '(Alejandro Von Humboldt): el estudio debe '
                                'analizar causas y consecuencias.',
                                'Principio de Relación o Conexión (Jean '
                                'Brunhes): los elementos del espacio '
                                'geográfico están en íntima '
                                'interdependencia.',
                                'Principio de Comparación (Carlos Ritter y '
                                'Vidal de la Blache): consiste en comparar '
                                'los elementos por su semejanza u oposición.',
                                'Principio de Actividad, Dinamismo o '
                                'Evolución (Jean Brunhes): los elementos '
                                'geográficos están en constante '
                                'transformación.']},
                     {'titulo': 'GEOGRAFÍA APLICADA E IMPORTANCIA',
                      'items': ['La Geografía Aplicada orienta los estudios '
                                'e investigaciones hacia soluciones '
                                'prácticas de problemas territoriales.',
                                'Herramientas de la Geografía Aplicada: '
                                'cartografía digital, Sistemas de '
                                'Información Geográfica (SIG) y '
                                'teledetección.',
                                'El planeta Tierra tiene un hábitat de 510 '
                                'millones de km², dividido políticamente en '
                                '193 países, con una población de 7 450 '
                                'millones de habitantes (Censo EE.UU. '
                                '2018).']}],
  'qr_reto': [{'pregunta': 'El objeto de estudio de la Ciencia geográfica es '
                           'el:',
               'respuesta': 'Espacio geográfico'},
              {'pregunta': 'Dentro de la Biogeografía, el estudio de la '
                           'distribución de los animales corresponde a la:',
               'respuesta': 'Zoogeografía'},
              {'pregunta': 'El origen, estructura y clases de suelos es '
                           'estudiado por la:',
               'respuesta': 'Edafología'}],
  'qr_dato': 'Herramientas de la Geografía Aplicada: cartografía digital, '
             'Sistemas de Información Geográfica (SIG) y teledetección.'},
 {'num': 2,
  'titulo': 'Geosistema y Espacio Exterior',
  'secciones': [{'titulo': '2.1 EL GEOSISTEMA',
                 'items': ['El geosistema, o planeta Tierra considerado como '
                           'unidad, es el conjunto de entidades bióticas, '
                           '{abióticas} y antrópicas que se interrelacionan '
                           'permanentemente.',
                           'Las entidades abióticas del geosistema son la '
                           'hidrósfera, la atmósfera y la {litósfera}.',
                           'La entidad biótica del geosistema es la '
                           '{biósfera}; la entidad antrópica es la '
                           'sociósfera o {antropósfera}.',
                           'El geosistema se autodesarrolla y se encuentra '
                           'en {equilibrio} dinámico relativo.']},
                {'titulo': '2.2 EL UNIVERSO Y SU ORIGEN',
                 'items': ['El universo es la totalidad de la materia, la '
                           'radiación y el espacio-tiempo, que se encuentra '
                           'en proceso de {expansión}.',
                           'La teoría de la Gran Explosión o {Big-Bang} fue '
                           'planteada por George Lemaître en 1927 y '
                           'complementada después por George Gamow.',
                           'Según el Big-Bang, el universo se originó de un '
                           '«súper átomo» o {huevo cósmico} que explotó hace '
                           'unos 15 000 millones de años.']},
                {'titulo': '2.3 ESTRUCTURA DEL UNIVERSO',
                 'items': ['Las {galaxias}, llamadas también universos isla, '
                           'son aglomeraciones de millones de estrellas.',
                           'La Vía Láctea, nuestra galaxia, tiene un '
                           'diámetro medio de {100 000} años luz y contiene '
                           'unas 200 000 millones de estrellas.',
                           'Las {estrellas} son esferas de gases calientes '
                           'que producen su propia luz mediante fusión '
                           'nuclear.',
                           'Las {nebulosas} son regiones del medio '
                           'interestelar donde nacen las estrellas, '
                           'constituidas principalmente por hidrógeno y '
                           'helio.',
                           'El {año luz} es la distancia que recorre la luz '
                           'en un año, a 300 000 km por segundo.',
                           'La luz del Sol tarda {8,3} minutos en llegar a '
                           'la Tierra.']},
                {'titulo': '2.4 EL SISTEMA PLANETARIO SOLAR',
                 'items': ['El Sol contiene el {98,85}% de la masa total del '
                           'Sistema Solar y domina su campo gravitacional.',
                           'La Unión Astronómica Internacional, en {2006}, '
                           'definió tres categorías: planeta, planeta enano '
                           'y cuerpos menores.',
                           'Los planetas interiores o {terrestres} son '
                           'Mercurio, Venus, Tierra y Marte: sólidos, densos '
                           'y cercanos al Sol.',
                           'Los planetas exteriores o {jovianos} son '
                           'Júpiter, Saturno, Urano y Neptuno: gaseosos, de '
                           'mayor tamaño y más lejanos al Sol.',
                           'Los {cinturones de Van Allen} son zonas de '
                           'radiación que rodean la Tierra, formadas por '
                           'partículas cargadas atrapadas por el campo '
                           '{magnético}.']},
                {'titulo': '2.5 LA GEODESIA Y LAS FORMAS DE LA TIERRA',
                 'items': ['La {geodesia} es una de las ciencias más '
                           'antiguas cultivadas por el hombre; estudia y '
                           'determina la forma y dimensiones de la Tierra y '
                           'su campo de {gravedad}.',
                           'La edad de la Tierra se ha calculado mediante '
                           'isótopos radiactivos en unos {4600} millones de '
                           'años.',
                           'La forma {física} o topográfica es la forma real '
                           'de la Tierra, considerando sus partes salientes '
                           'y entrantes; es una forma {irregular}.',
                           'La forma {geoide} resulta de nivelar la '
                           'superficie continental con el nivel medio del '
                           'mar; es una superficie {equipotencial} de '
                           'gravedad terrestre.',
                           'La forma {elipsoide de revolución} es la forma '
                           'matemática o geométrica de la Tierra, achatada '
                           'en los {polos} y ensanchada en el ecuador.',
                           'La superficie total de la Tierra es de {510 000 '
                           '000} km²; la superficie continental es de 149 '
                           '000 000 km² y la marítima de {361 000 000} km².',
                           'La densidad media de la Tierra es de {5,518} '
                           'gr/cm³.']},
                {'titulo': '2.6 DIMENSIONES Y MOVIMIENTOS DE LA TIERRA',
                 'items': ['La circunferencia ecuatorial de la Tierra mide '
                           '{40 076} km, y la circunferencia polar {40 009} '
                           'km.',
                           'El diámetro ecuatorial de la Tierra es de {12 '
                           '757} km; el diámetro polar es de {12 714} km.',
                           'Los dos principales movimientos de la Tierra son '
                           'el de {rotación} y el de {traslación}.',
                           'El movimiento de rotación se realiza alrededor '
                           'de un eje imaginario, cuyos extremos son los '
                           '{polos}, en un día.',
                           'La rotación terrestre tiene una dirección de {W} '
                           'a E, con una velocidad de 1674 km/h en la zona '
                           'ecuatorial.',
                           'El tiempo que emplea la Tierra en dar una vuelta '
                           'completa sobre su eje es de {23} horas, 56 '
                           'minutos y 4,09 segundos.',
                           'Entre las consecuencias de la rotación están la '
                           'sucesión del {día} y la noche, y la forma '
                           '{achatada} de la Tierra.',
                           'La rotación también genera la desviación de '
                           'vientos y {corrientes marinas}, y la presencia '
                           'de las {mareas}.']}],
  'cuadros': [{'titulo': '2.4 PLANETAS DEL SISTEMA SOLAR',
               'encabezados': ['Planeta', 'N° satélites', 'Orden de tamaño'],
               'filas': [['Mercurio', '0', '{8}°'],
                         ['Tierra', '{1}', '5°'],
                         ['{Júpiter}', '63', '1°'],
                         ['Saturno', '61', '{2}°'],
                         ['{Neptuno}', '13', '4°']]}],
  'preguntas': [{'pregunta': 'El geosistema está compuesto por entidades '
                             'bióticas, abióticas y:',
                 'alternativas': ['Solares',
                                  'Estelares',
                                  'Cósmicas',
                                  'Galácticas',
                                  'Antrópicas'],
                 'correcta': 'E'},
                {'pregunta': 'La litósfera, la atmósfera y la hidrósfera son '
                             'entidades:',
                 'alternativas': ['Estelares',
                                  'Cósmicas',
                                  'Antrópicas',
                                  'Abióticas',
                                  'Bióticas'],
                 'correcta': 'D'},
                {'pregunta': 'La biósfera es una entidad del geosistema de '
                             'tipo:',
                 'alternativas': ['Biótica',
                                  'Solar',
                                  'Antrópica',
                                  'Abiótica',
                                  'Cósmica'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría del Big-Bang fue planteada '
                             'originalmente por:',
                 'alternativas': ['George Lemaître',
                                  'Albert Einstein',
                                  'Isaac Newton',
                                  'Edwin Hubble',
                                  'George Gamow'],
                 'correcta': 'A'},
                {'pregunta': 'Según el Big-Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['500 millones de años',
                                  '15 000 millones de años',
                                  '1 000 millones de años',
                                  '5 000 millones de años',
                                  '100 000 millones de años'],
                 'correcta': 'B'},
                {'pregunta': 'Las aglomeraciones de millones de estrellas se '
                             'denominan:',
                 'alternativas': ['Meteoritos',
                                  'Galaxias',
                                  'Cometas',
                                  'Nebulosas',
                                  'Cúmulos'],
                 'correcta': 'B'},
                {'pregunta': 'El diámetro medio de la Vía Láctea es de '
                             'aproximadamente:',
                 'alternativas': ['10 000 años luz',
                                  '1 000 000 años luz',
                                  '1 000 años luz',
                                  '100 000 años luz',
                                  '500 000 años luz'],
                 'correcta': 'D'},
                {'pregunta': 'Las estrellas producen su propia luz mediante:',
                 'alternativas': ['Reflexión solar',
                                  'Fisión atómica',
                                  'Combustión química',
                                  'Fusión nuclear',
                                  'Radiación cósmica'],
                 'correcta': 'D'},
                {'pregunta': 'Las regiones interestelares donde nacen las '
                             'estrellas se llaman:',
                 'alternativas': ['Asteroides',
                                  'Cometas',
                                  'Cúmulos',
                                  'Nebulosas',
                                  'Galaxias'],
                 'correcta': 'D'},
                {'pregunta': 'El año luz es una unidad de:',
                 'alternativas': ['Masa',
                                  'Velocidad',
                                  'Distancia',
                                  'Tiempo',
                                  'Temperatura'],
                 'correcta': 'C'},
                {'pregunta': 'La luz del Sol tarda en llegar a la Tierra '
                             'aproximadamente:',
                 'alternativas': ['1 minuto',
                                  '8,3 segundos',
                                  '1 hora',
                                  '8,3 minutos',
                                  '8,3 horas'],
                 'correcta': 'D'},
                {'pregunta': 'El Sol contiene de la masa total del Sistema '
                             'Solar aproximadamente:',
                 'alternativas': ['75%', '98,85%', '10%', '50%', '25%'],
                 'correcta': 'B'},
                {'pregunta': 'La Unión Astronómica Internacional definió las '
                             'tres categorías de cuerpos del Sistema Solar '
                             'en el año:',
                 'alternativas': ['2015', '2006', '2020', '1980', '1990'],
                 'correcta': 'B'},
                {'pregunta': 'Los planetas interiores o terrestres son:',
                 'alternativas': ['Solo la Tierra y Marte',
                                  'Ceres y Plutón',
                                  'Solo Mercurio y Venus',
                                  'Mercurio, Venus, Tierra y Marte',
                                  'Júpiter, Saturno, Urano y Neptuno'],
                 'correcta': 'D'},
                {'pregunta': 'Los planetas exteriores o jovianos se '
                             'caracterizan por ser:',
                 'alternativas': ['Sin satélites',
                                  'De alta densidad',
                                  'Cercanos al Sol',
                                  'Sólidos y pequeños',
                                  'Gaseosos y de mayor tamaño'],
                 'correcta': 'E'},
                {'pregunta': 'El planeta con mayor número de satélites entre '
                             'los mostrados es:',
                 'alternativas': ['Júpiter',
                                  'Marte',
                                  'Saturno',
                                  'Neptuno',
                                  'Urano'],
                 'correcta': 'A'},
                {'pregunta': 'El planeta de mayor diámetro del Sistema Solar '
                             'es:',
                 'alternativas': ['Tierra',
                                  'Urano',
                                  'Júpiter',
                                  'Saturno',
                                  'Neptuno'],
                 'correcta': 'C'},
                {'pregunta': 'Plutón es clasificado actualmente como:',
                 'alternativas': ['Planeta exterior',
                                  'Planeta interior',
                                  'Planeta enano',
                                  'Cometa',
                                  'Satélite'],
                 'correcta': 'C'},
                {'pregunta': 'El geosistema se caracteriza por estar en:',
                 'alternativas': ['Estado sólido fijo',
                                  'Colapso permanente',
                                  'Equilibrio estático total',
                                  'Equilibrio dinámico relativo',
                                  'Expansión sin cambios'],
                 'correcta': 'D'},
                {'pregunta': 'La entidad antrópica del geosistema '
                             'corresponde a:',
                 'alternativas': ['Las rocas',
                                  'El aire',
                                  'Los seres vivos no humanos',
                                  'La sociedad humana',
                                  'Los océanos'],
                 'correcta': 'D'},
                {'pregunta': 'Las zonas de radiación que rodean la Tierra, '
                             'formadas por partículas cargadas atrapadas por '
                             'el campo magnético, se llaman:',
                 'alternativas': ['Cinturones de Van Allen',
                                  'Termosfera',
                                  'Magnetosfera exclusiva',
                                  'Ionosfera',
                                  'Exosfera'],
                 'correcta': 'A'},
                {'pregunta': 'Una consecuencia del movimiento de rotación '
                             'terrestre es: (II CEPRU 2024)',
                 'alternativas': ['Zonas climáticas y día artificial',
                                  'Puntos cardinales y las zonas térmicas',
                                  'Día artificial y achatamiento polar',
                                  'Presencia de mareas y las estaciones del '
                                  'año',
                                  'Desviación de los vientos y las '
                                  'corrientes marinas'],
                 'correcta': 'C'},
                {'pregunta': 'Marque una consecuencia del movimiento de '
                             'rotación de la Tierra: (II CEPRU 2022)',
                 'alternativas': ['Estaciones del año',
                                  'Zonas climáticas',
                                  'Desigual distribución de los rayos del '
                                  'sol',
                                  'Día artificial',
                                  'Achatamiento polar'],
                 'correcta': 'D'},
                {'pregunta': 'La ciudad «X» está ubicada a 75° de longitud. '
                             '¿Cuántas horas de diferencia existe con el '
                             'meridiano de Greenwich? (II CEPRU 2022)',
                 'alternativas': ['4 horas',
                                  '6 horas',
                                  '5 horas',
                                  '7 horas',
                                  '10 horas'],
                 'correcta': 'C'},
                {'pregunta': 'Las entidades del Geosistema a escala Global '
                             'son: (Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Hidrosfera, sociósfera y zoogeografía',
                                  'Antrópicas, fitogeográficas y bióticas',
                                  'Bióticas, litosfera y heliomasa',
                                  'Abióticas, naturales y culturales',
                                  'Abióticas, bióticas y antrópicas'],
                 'correcta': 'E'},
                {'pregunta': 'La Longitud es: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Distancia angular de un punto de la '
                                  'superficie terrestre hacia el círculo '
                                  'polar ártico',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre al meridiano base de '
                                  'Greenwich',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre a la línea '
                                  'ecuatorial',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre al meridiano de '
                                  'referencia del Perú',
                                  'Sistema de referencia basado en paralelos '
                                  'y meridianos'],
                 'correcta': 'B'},
                {'pregunta': 'El cuarto y séptimo planeta en la órbita solar '
                             'corresponden a: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['Ceres y Eris',
                                  'Tierra y Saturno',
                                  'Marte y Urano',
                                  'Júpiter y Neptuno',
                                  'Venus y Neptuno'],
                 'correcta': 'C'},
                {'pregunta': 'Si en la ciudad «X» (28°30\'40" N, 75°29\'10" '
                             'W) son las 14:29 horas del 11 de diciembre, la '
                             'hora y fecha en la ciudad «Y» (71°40\'50" S, '
                             '135°10\'50" E) es: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['04:29 horas del 12 de diciembre',
                                  '03:29 horas del 11 de diciembre',
                                  '05:29 horas del 12 de diciembre',
                                  '05:29 horas del 11 de diciembre',
                                  '16:29 horas del 12 de diciembre'],
                 'correcta': 'A'},
                {'pregunta': 'El paralelo del trópico de Cáncer, ubicado en '
                             'el hemisferio norte, se encuentra situado a '
                             'una latitud de: (Primera Oportunidad UNSAAC '
                             '2023)',
                 'alternativas': ["66° 33'",
                                  "63° 27'",
                                  "25° 30'",
                                  "23° 27'",
                                  "28° 25'"],
                 'correcta': 'D'},
                {'pregunta': 'Una característica que corresponde a un '
                             'planeta interior o terrestre del Sistema '
                             'Planetario Solar es: (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ['Se les denomina planetas jovianos',
                                  'Poseen menor masa y volumen',
                                  'Tienen mayor cantidad de satélites',
                                  'Son más gaseosos',
                                  'Son más fríos y lejanos al Sol'],
                 'correcta': 'B'},
                {'pregunta': "Cuando en el Cusco son las 9 h 37', ¿qué hora "
                             'será en Roma (10° E)? (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ["15 h 37'",
                                  "13 h 25'",
                                  "03 h 39'",
                                  "03 h 27'",
                                  "14 h 27'"],
                 'correcta': 'A'},
                {'pregunta': 'La ciencia que estudia y determina la forma y '
                             'dimensiones de la Tierra y su campo de '
                             'gravedad se llama:',
                 'alternativas': ['Astronomía',
                                  'Topografía',
                                  'Geomorfología',
                                  'Geodesia',
                                  'Cartografía'],
                 'correcta': 'D'},
                {'pregunta': 'La edad de la Tierra, calculada mediante '
                             'isótopos radiactivos, se estima en:',
                 'alternativas': ['2300 millones de años',
                                  '6000 millones de años',
                                  '4600 millones de años',
                                  '10000 millones de años',
                                  '1000 millones de años'],
                 'correcta': 'C'},
                {'pregunta': 'La forma real de la Tierra, considerando sus '
                             'partes salientes y entrantes tal como es, se '
                             'llama forma:',
                 'alternativas': ['Esférica',
                                  'Geoide',
                                  'Física o topográfica',
                                  'Elipsoide de revolución',
                                  'Achatada'],
                 'correcta': 'C'},
                {'pregunta': 'La forma de la Tierra que resulta de nivelar '
                             'la superficie continental con el nivel medio '
                             'del mar se llama forma:',
                 'alternativas': ['Física',
                                  'Elipsoide de revolución',
                                  'Esférica',
                                  'Topográfica',
                                  'Geoide'],
                 'correcta': 'E'},
                {'pregunta': 'La forma matemática o geométrica de la Tierra, '
                             'achatada en los polos y ensanchada en el '
                             'ecuador, se llama:',
                 'alternativas': ['Forma topográfica',
                                  'Geoide',
                                  'Elipsoide de revolución',
                                  'Forma física',
                                  'Esfera perfecta'],
                 'correcta': 'C'},
                {'pregunta': 'La superficie total de la Tierra es '
                             'aproximadamente de:',
                 'alternativas': ['149 000 000 km²',
                                  '200 000 000 km²',
                                  '361 000 000 km²',
                                  '700 000 000 km²',
                                  '510 000 000 km²'],
                 'correcta': 'E'},
                {'pregunta': 'La densidad media de la Tierra es de:',
                 'alternativas': ['5,518 gr/cm³',
                                  '1 gr/cm³',
                                  '3,2 gr/cm³',
                                  '8,9 gr/cm³',
                                  '10 gr/cm³'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'EL GEOSISTEMA',
                      'items': ['El geosistema, o planeta Tierra considerado '
                                'como unidad, es el conjunto de entidades '
                                'bióticas, abióticas y antrópicas que se '
                                'interrelacionan permanentemente.',
                                'Las entidades abióticas del geosistema son '
                                'la hidrósfera, la atmósfera y la litósfera.',
                                'La entidad biótica del geosistema es la '
                                'biósfera; la entidad antrópica es la '
                                'sociósfera o antropósfera.',
                                'El geosistema se autodesarrolla y se '
                                'encuentra en equilibrio dinámico '
                                'relativo.']},
                     {'titulo': 'EL UNIVERSO Y SU ORIGEN',
                      'items': ['El universo es la totalidad de la materia, '
                                'la radiación y el espacio-tiempo, que se '
                                'encuentra en proceso de expansión.',
                                'La teoría de la Gran Explosión o Big-Bang '
                                'fue planteada por George Lemaître en 1927 y '
                                'complementada después por George Gamow.',
                                'Según el Big-Bang, el universo se originó '
                                'de un «súper átomo» o huevo cósmico que '
                                'explotó hace unos 15 000 millones de '
                                'años.']},
                     {'titulo': 'ESTRUCTURA DEL UNIVERSO',
                      'items': ['Las galaxias, llamadas también universos '
                                'isla, son aglomeraciones de millones de '
                                'estrellas.',
                                'La Vía Láctea, nuestra galaxia, tiene un '
                                'diámetro medio de 100 000 años luz y '
                                'contiene unas 200 000 millones de '
                                'estrellas.',
                                'Las estrellas son esferas de gases '
                                'calientes que producen su propia luz '
                                'mediante fusión nuclear.',
                                'Las nebulosas son regiones del medio '
                                'interestelar donde nacen las estrellas, '
                                'constituidas principalmente por hidrógeno y '
                                'helio.',
                                'El año luz es la distancia que recorre la '
                                'luz en un año, a 300 000 km por segundo.',
                                'La luz del Sol tarda 8,3 minutos en llegar '
                                'a la Tierra.']},
                     {'titulo': 'EL SISTEMA PLANETARIO SOLAR',
                      'items': ['El Sol contiene el 98,85% de la masa total '
                                'del Sistema Solar y domina su campo '
                                'gravitacional.',
                                'La Unión Astronómica Internacional, en '
                                '2006, definió tres categorías: planeta, '
                                'planeta enano y cuerpos menores.',
                                'Los planetas interiores o terrestres son '
                                'Mercurio, Venus, Tierra y Marte: sólidos, '
                                'densos y cercanos al Sol.',
                                'Los planetas exteriores o jovianos son '
                                'Júpiter, Saturno, Urano y Neptuno: '
                                'gaseosos, de mayor tamaño y más lejanos al '
                                'Sol.',
                                'Los cinturones de Van Allen son zonas de '
                                'radiación que rodean la Tierra, formadas '
                                'por partículas cargadas atrapadas por el '
                                'campo magnético.']},
                     {'titulo': 'LA GEODESIA Y LAS FORMAS DE LA TIERRA',
                      'items': ['La geodesia es una de las ciencias más '
                                'antiguas cultivadas por el hombre; estudia '
                                'y determina la forma y dimensiones de la '
                                'Tierra y su campo de gravedad.',
                                'La edad de la Tierra se ha calculado '
                                'mediante isótopos radiactivos en unos 4600 '
                                'millones de años.',
                                'La forma física o topográfica es la forma '
                                'real de la Tierra, considerando sus partes '
                                'salientes y entrantes; es una forma '
                                'irregular.',
                                'La forma geoide resulta de nivelar la '
                                'superficie continental con el nivel medio '
                                'del mar; es una superficie equipotencial de '
                                'gravedad terrestre.',
                                'La forma elipsoide de revolución es la '
                                'forma matemática o geométrica de la Tierra, '
                                'achatada en los polos y ensanchada en el '
                                'ecuador.',
                                'La superficie total de la Tierra es de 510 '
                                '000 000 km²; la superficie continental es '
                                'de 149 000 000 km² y la marítima de 361 000 '
                                '000 km².',
                                'La densidad media de la Tierra es de 5,518 '
                                'gr/cm³.']},
                     {'titulo': 'DIMENSIONES Y MOVIMIENTOS DE LA TIERRA',
                      'items': ['La circunferencia ecuatorial de la Tierra '
                                'mide 40 076 km, y la circunferencia polar '
                                '40 009 km.',
                                'El diámetro ecuatorial de la Tierra es de '
                                '12 757 km; el diámetro polar es de 12 714 '
                                'km.',
                                'Los dos principales movimientos de la '
                                'Tierra son el de rotación y el de '
                                'traslación.',
                                'El movimiento de rotación se realiza '
                                'alrededor de un eje imaginario, cuyos '
                                'extremos son los polos, en un día.',
                                'La rotación terrestre tiene una dirección '
                                'de W a E, con una velocidad de 1674 km/h en '
                                'la zona ecuatorial.',
                                'El tiempo que emplea la Tierra en dar una '
                                'vuelta completa sobre su eje es de 23 '
                                'horas, 56 minutos y 4,09 segundos.',
                                'Entre las consecuencias de la rotación '
                                'están la sucesión del día y la noche, y la '
                                'forma achatada de la Tierra.',
                                'La rotación también genera la desviación de '
                                'vientos y corrientes marinas, y la '
                                'presencia de las mareas.']}],
  'qr_reto': [{'pregunta': 'El Sol contiene de la masa total del Sistema '
                           'Solar aproximadamente:',
               'respuesta': '98,85%'},
              {'pregunta': 'La ciencia que estudia y determina la forma y '
                           'dimensiones de la Tierra y su campo de gravedad '
                           'se llama:',
               'respuesta': 'Geodesia'},
              {'pregunta': 'Según el Big-Bang, el universo se originó hace '
                           'aproximadamente:',
               'respuesta': '15 000 millones de años'}],
  'qr_dato': 'La entidad biótica del geosistema es la biósfera; la entidad '
             'antrópica es la sociósfera o antropósfera.'},
 {'num': 3,
  'titulo': 'Cartografía y Sistemas de Información Geográfica',
  'secciones': [{'titulo': '3.1 LA CARTOGRAFÍA',
                 'items': ['La cartografía es la ciencia y arte de expresar '
                           'gráficamente, por medio de {mapas}, las '
                           'características del geosistema.',
                           'El padre de la cartografía es {Abraham Ortelius} '
                           '(1527-1598), cartógrafo y geógrafo flamenco que '
                           'realizó el primer atlas moderno.',
                           'Las proyecciones cartográficas son el sistema '
                           'para transferir la información de la superficie '
                           'esférica de la Tierra a un {plano} o mapa.',
                           'El mapa no es exacto porque la {esfera} '
                           'terrestre no puede representarse sin deformación '
                           'en un plano.']},
                {'titulo': '3.2 TIPOS DE PROYECCIONES',
                 'items': ['La proyección {cilíndrica} usa un cilindro '
                           'tangente al Ecuador; su mayor inconveniente es '
                           'que deforma las áreas cercanas a los polos.',
                           'La proyección cilíndrica más utilizada es la de '
                           '{Mercator}.',
                           'La proyección {cónica} se obtiene proyectando la '
                           'superficie terrestre sobre un cono, y resulta '
                           'adecuada para representar países o regiones.',
                           'La proyección {cenital} o azimutal proyecta '
                           'paralelos y meridianos sobre un plano tangente, '
                           'dando lugar a un mapa {circular}.']},
                {'titulo': '3.3 LÍNEAS IMAGINARIAS TERRESTRES',
                 'items': ['Los {círculos máximos} dividen a la Tierra en '
                           'dos partes iguales, como el Ecuador; los '
                           'círculos {menores} son paralelos al Ecuador.',
                           'Los {meridianos} son semicírculos imaginarios '
                           'que van de polo a polo, cortando '
                           'perpendicularmente al Ecuador.',
                           'El meridiano base internacional es el que pasa '
                           'por el Observatorio de {Greenwich}, en '
                           'Inglaterra.',
                           'El meridiano de Greenwich divide al planeta en '
                           'el hemisferio {Occidental} y el hemisferio '
                           'Oriental.',
                           'Los {paralelos} son líneas imaginarias '
                           'horizontales, perpendiculares al eje terrestre, '
                           'que disminuyen de tamaño al acercarse a los '
                           'polos.',
                           'La línea del Ecuador es el paralelo {0}°, y '
                           'divide al planeta en hemisferio Norte y '
                           'hemisferio Sur.',
                           'El Trópico de Cáncer se ubica en el hemisferio '
                           "norte, a una latitud de {23}° 27'.",
                           'El Trópico de Capricornio se ubica en el '
                           "hemisferio sur, también a {23}° 27' de latitud.",
                           'Los Círculos Polares, Ártico y Antártico, se '
                           "ubican a {66}° 33' de latitud."]},
                {'titulo': '3.4 SISTEMA DE COORDENADAS UTM',
                 'items': ['El sistema de coordenadas {UTM} (Universal '
                           'Transversal de Mercator) se basa en la '
                           'proyección cartográfica transversa de '
                           '{Mercator}, tangente a un meridiano.',
                           'A diferencia de las coordenadas geográficas '
                           '(longitud/latitud), las magnitudes UTM se '
                           'expresan en {metros}.',
                           'El sistema UTM fue desarrollado por el Cuerpo de '
                           'Ingenieros del Ejército de EE.UU. en la década '
                           'de {1940}; actualmente usa el elipsoide {WGS84}.',
                           'La Tierra está dividida en {60} zonas o husos '
                           'UTM de 6° de longitud cada uno.',
                           'La Tierra está dividida en {20} bandas UTM: 19 '
                           'de 8° de latitud y una última de 12°, '
                           'identificadas con letras de la {C} a la X (sin I '
                           'ni O).',
                           'El territorio peruano se ubica en las zonas o '
                           'husos {17}, 18 y 19, y en las bandas K, L y {M}.',
                           'La Red UTM se utiliza entre los 80° de latitud '
                           'sur y los 84° de latitud norte; por encima se '
                           'usa la Red Universal Estereográfica {Polar} '
                           '(UPS).']},
                {'titulo': '3.5 TELEDETECCIÓN, GPS Y HUSOS HORARIOS',
                 'items': ['La {teledetección} es la técnica que permite '
                           'obtener información de un objeto o área mediante '
                           'el análisis de imágenes, sin contacto físico.',
                           'La teledetección espacial adquiere imágenes de '
                           'la superficie terrestre mediante sensores '
                           'instalados en {satélites} artificiales.',
                           'El GPS ({Sistema de Posicionamiento Global}) fue '
                           'desarrollado por el Departamento de Defensa de '
                           'los {Estados Unidos}.',
                           'El sistema GPS utiliza {24} satélites en órbita, '
                           'a 200 km de altura, con trayectorias '
                           'sincronizadas.',
                           'Un {huso horario} es una franja comprendida '
                           'entre dos meridianos, con un ángulo de '
                           'separación de {15} grados.',
                           'La Tierra está dividida en {24} husos horarios, '
                           'ya que su circunferencia tiene 360 grados.',
                           'La convención universal que estableció los husos '
                           'horarios se realizó en {Washington} en el año '
                           '{1884}.']}],
  'cuadros': [{'titulo': '3.3 PARALELOS PRINCIPALES',
               'encabezados': ['Paralelo', 'Latitud'],
               'filas': [['Línea {Ecuatorial}', "00°00'"],
                         ['Trópico de {Cáncer}', "23°27' N"],
                         ['Trópico de {Capricornio}', "23°27' S"],
                         ['Círculo Polar {Ártico}', "66°33' N"],
                         ['Círculo Polar {Antártico}', "66°33' S"]]}],
  'preguntas': [{'pregunta': 'La cartografía es definida como la ciencia y '
                             'arte de:',
                 'alternativas': ['Medir el tiempo',
                                  'Calcular distancias astronómicas',
                                  'Estudiar el clima',
                                  'Clasificar rocas',
                                  'Expresar gráficamente mediante mapas'],
                 'correcta': 'E'},
                {'pregunta': 'El padre de la cartografía moderna fue:',
                 'alternativas': ['Gerardus Mercator',
                                  'Eratóstenes',
                                  'Claudio Ptolomeo',
                                  'Abraham Ortelius',
                                  'Alexander von Humboldt'],
                 'correcta': 'D'},
                {'pregunta': 'Las proyecciones cartográficas sirven para '
                             'transferir información desde la superficie '
                             'esférica hacia:',
                 'alternativas': ['Un globo terráqueo',
                                  'Una fotografía satelital',
                                  'Un modelo digital',
                                  'Un cilindro únicamente',
                                  'Un plano o mapa'],
                 'correcta': 'E'},
                {'pregunta': 'La proyección cilíndrica más utilizada en '
                             'cartografía es la de:',
                 'alternativas': ['Gauss',
                                  'Ptolomeo',
                                  'Ortelius',
                                  'Humboldt',
                                  'Mercator'],
                 'correcta': 'E'},
                {'pregunta': 'El principal inconveniente de la proyección '
                             'cilíndrica es que deforma:',
                 'alternativas': ['El centro del mapa',
                                  'Las áreas próximas a los polos',
                                  'El Ecuador',
                                  'Las líneas rectas',
                                  'Los continentes pequeños'],
                 'correcta': 'B'},
                {'pregunta': 'La proyección adecuada para representar un '
                             'solo país o región es la:',
                 'alternativas': ['Mercator',
                                  'Cenital pura',
                                  'Cónica',
                                  'Universal',
                                  'Cilíndrica'],
                 'correcta': 'C'},
                {'pregunta': 'La proyección que da lugar a un mapa circular '
                             'es la:',
                 'alternativas': ['Cónica',
                                  'Poliédrica',
                                  'De Mercator',
                                  'Cilíndrica',
                                  'Cenital o azimutal'],
                 'correcta': 'E'},
                {'pregunta': 'Los círculos máximos dividen a la Tierra en:',
                 'alternativas': ['Ocho sectores',
                                  'Dos partes iguales',
                                  'Tres partes iguales',
                                  'Ninguna división real',
                                  'Cuatro partes desiguales'],
                 'correcta': 'B'},
                {'pregunta': 'Los meridianos son semicírculos que van de:',
                 'alternativas': ['Polo a polo',
                                  'Este a oeste',
                                  'Centro a superficie',
                                  'Trópico a trópico',
                                  'Ecuador a ecuador'],
                 'correcta': 'A'},
                {'pregunta': 'El meridiano base internacional pasa por el '
                             'observatorio de:',
                 'alternativas': ['Roma',
                                  'Greenwich',
                                  'París',
                                  'Washington',
                                  'Madrid'],
                 'correcta': 'B'},
                {'pregunta': 'El meridiano de Greenwich y su opuesto dividen '
                             'la Tierra en los hemisferios:',
                 'alternativas': ['Occidental y Oriental',
                                  'Interno y externo',
                                  'Superior e inferior',
                                  'Tropical y polar',
                                  'Norte y Sur'],
                 'correcta': 'A'},
                {'pregunta': 'Los paralelos son líneas imaginarias con '
                             'orientación:',
                 'alternativas': ['Vertical',
                                  'Este-Oeste',
                                  'Norte-Sur',
                                  'Radial',
                                  'Diagonal'],
                 'correcta': 'B'},
                {'pregunta': 'La línea del Ecuador corresponde al paralelo:',
                 'alternativas': ['45°', "23°27'", '90°', '180°', '0°'],
                 'correcta': 'E'},
                {'pregunta': 'El Ecuador divide a la Tierra en los '
                             'hemisferios:',
                 'alternativas': ['Este y polar',
                                  'Norte y Sur',
                                  'Anterior y posterior',
                                  'Occidental y Oriental',
                                  'Tropical y templado'],
                 'correcta': 'B'},
                {'pregunta': 'El Trópico de Cáncer se ubica en el hemisferio '
                             'norte, a una latitud de:',
                 'alternativas': ["23°27'", '90°', "66°33'", '45°', '0°'],
                 'correcta': 'A'},
                {'pregunta': 'El Trópico de Capricornio se ubica en el '
                             'hemisferio:',
                 'alternativas': ['Norte',
                                  'Sur',
                                  'Ecuatorial',
                                  'Oriental',
                                  'Occidental'],
                 'correcta': 'B'},
                {'pregunta': 'Los Círculos Polares se ubican a una latitud '
                             'de:',
                 'alternativas': ["45°00'",
                                  "66°33'",
                                  "90°00'",
                                  "23°27'",
                                  "0°00'"],
                 'correcta': 'B'},
                {'pregunta': 'Los meridianos alcanzan su mayor separación '
                             'al:',
                 'alternativas': ['Cruzar los trópicos',
                                  'Separarse en los círculos polares',
                                  'Cruzar los polos',
                                  'Unirse en el centro',
                                  'Atravesar el Ecuador'],
                 'correcta': 'E'},
                {'pregunta': 'Los meridianos convergen (se unen) en:',
                 'alternativas': ['El Ecuador',
                                  'Los polos',
                                  'Los círculos polares',
                                  'El centro de la Tierra',
                                  'Los trópicos'],
                 'correcta': 'B'},
                {'pregunta': 'Las formas que se usan para transferir la '
                             'esfera terrestre a un mapa se llaman '
                             'superficies:',
                 'alternativas': ['Desarrollables, como conos y cilindros',
                                  'Planas únicamente',
                                  'Triangulares',
                                  'Curvas irregulares',
                                  'Esféricas puras'],
                 'correcta': 'A'},
                {'pregunta': 'En la hoja de la Carta Geográfica Nacional, la '
                             'planimetría y altimetría forman parte de: (II '
                             'CEPRU 2025)',
                 'alternativas': ['La escala de la hoja',
                                  'El sistema de coordenadas',
                                  'El cuerpo de la hoja',
                                  'La información marginal',
                                  'Los signos convencionales'],
                 'correcta': 'C'},
                {'pregunta': 'Según las Coordenadas Universal Transversal de '
                             'Mercator (UTM), la Tierra está dividida en: '
                             '(II CEPRU 2024)',
                 'alternativas': ['60 husos y 20 bandas',
                                  '60 zonas y 20 bandas',
                                  '60 zonas y 19 bandas',
                                  '60 bandas y 20 zonas',
                                  '24 zonas y 20 bandas'],
                 'correcta': 'B'},
                {'pregunta': 'La carta geográfica nacional del territorio '
                             'peruano se encuentra dividida en: (II CEPRU '
                             '2024)',
                 'alternativas': ['505 hojas',
                                  '201 hojas',
                                  '305 hojas',
                                  '501 hojas',
                                  '101 hojas'],
                 'correcta': 'A'},
                {'pregunta': 'La escala de la carta nacional del Perú es: (I '
                             'CEPRU 2023)',
                 'alternativas': ['1:200 000',
                                  '1:10 000 000',
                                  '1:50 000',
                                  '1:1 000 000',
                                  '1:100 000'],
                 'correcta': 'E'},
                {'pregunta': 'La Carta Geográfica Nacional es un gran mapa '
                             'de nuestro país dividido en 501 mapas: (I '
                             'CEPRU 2024)',
                 'alternativas': ['Topográficos',
                                  'Hidrográficos',
                                  'Económicos',
                                  'Geográficos',
                                  'Geológicos'],
                 'correcta': 'A'},
                {'pregunta': 'Respecto al sistema de coordenadas UTM, el '
                             'territorio peruano se encuentra entre las '
                             'zonas: (Primera Oportunidad UNSAAC 2024)',
                 'alternativas': ['54, 56 y 57',
                                  '20, 21 y 22',
                                  '17, 18 y 19',
                                  '45, 46 y 47',
                                  '14, 15 y 17'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema de coordenadas UTM se basa en la '
                             'proyección cartográfica transversa de:',
                 'alternativas': ['Cónica',
                                  'Robinson',
                                  'Mercator',
                                  'Peters',
                                  'Azimutal'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia de las coordenadas geográficas '
                             '(longitud/latitud), las magnitudes del sistema '
                             'UTM se expresan en:',
                 'alternativas': ['Kilómetros cuadrados',
                                  'Grados sexagesimales',
                                  'Millas náuticas',
                                  'Metros',
                                  'Radianes'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema UTM fue desarrollado por el Cuerpo '
                             'de Ingenieros del Ejército de Estados Unidos '
                             'en la década de:',
                 'alternativas': ['1920', '1980', '1960', '1900', '1940'],
                 'correcta': 'E'},
                {'pregunta': 'La Tierra está dividida, según el sistema UTM, '
                             'en un número de zonas o husos igual a:',
                 'alternativas': ['60', '360', '20', '180', '24'],
                 'correcta': 'A'},
                {'pregunta': 'La Tierra está dividida, según el sistema UTM, '
                             'en un número de bandas igual a:',
                 'alternativas': ['20', '12', '60', '24', '30'],
                 'correcta': 'A'},
                {'pregunta': 'Por encima de los 80° de latitud sur y 84° de '
                             'latitud norte, en vez de la Red UTM, se '
                             'utiliza la Red Universal:',
                 'alternativas': ['Azimutal Ecuatorial',
                                  'Cilíndrica Polar',
                                  'Cónica Polar',
                                  'Geográfica Polar',
                                  'Estereográfica Polar (UPS)'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'LA CARTOGRAFÍA',
                      'items': ['La cartografía es la ciencia y arte de '
                                'expresar gráficamente, por medio de mapas, '
                                'las características del geosistema.',
                                'El padre de la cartografía es Abraham '
                                'Ortelius (1527-1598), cartógrafo y geógrafo '
                                'flamenco que realizó el primer atlas '
                                'moderno.',
                                'Las proyecciones cartográficas son el '
                                'sistema para transferir la información de '
                                'la superficie esférica de la Tierra a un '
                                'plano o mapa.',
                                'El mapa no es exacto porque la esfera '
                                'terrestre no puede representarse sin '
                                'deformación en un plano.']},
                     {'titulo': 'TIPOS DE PROYECCIONES',
                      'items': ['La proyección cilíndrica usa un cilindro '
                                'tangente al Ecuador; su mayor inconveniente '
                                'es que deforma las áreas cercanas a los '
                                'polos.',
                                'La proyección cilíndrica más utilizada es '
                                'la de Mercator.',
                                'La proyección cónica se obtiene proyectando '
                                'la superficie terrestre sobre un cono, y '
                                'resulta adecuada para representar países o '
                                'regiones.',
                                'La proyección cenital o azimutal proyecta '
                                'paralelos y meridianos sobre un plano '
                                'tangente, dando lugar a un mapa circular.']},
                     {'titulo': 'LÍNEAS IMAGINARIAS TERRESTRES',
                      'items': ['Los círculos máximos dividen a la Tierra en '
                                'dos partes iguales, como el Ecuador; los '
                                'círculos menores son paralelos al Ecuador.',
                                'Los meridianos son semicírculos imaginarios '
                                'que van de polo a polo, cortando '
                                'perpendicularmente al Ecuador.',
                                'El meridiano base internacional es el que '
                                'pasa por el Observatorio de Greenwich, en '
                                'Inglaterra.',
                                'El meridiano de Greenwich divide al planeta '
                                'en el hemisferio Occidental y el hemisferio '
                                'Oriental.',
                                'Los paralelos son líneas imaginarias '
                                'horizontales, perpendiculares al eje '
                                'terrestre, que disminuyen de tamaño al '
                                'acercarse a los polos.',
                                'La línea del Ecuador es el paralelo 0°, y '
                                'divide al planeta en hemisferio Norte y '
                                'hemisferio Sur.',
                                'El Trópico de Cáncer se ubica en el '
                                "hemisferio norte, a una latitud de 23° 27'.",
                                'El Trópico de Capricornio se ubica en el '
                                "hemisferio sur, también a 23° 27' de "
                                'latitud.',
                                'Los Círculos Polares, Ártico y Antártico, '
                                "se ubican a 66° 33' de latitud."]},
                     {'titulo': 'SISTEMA DE COORDENADAS UTM',
                      'items': ['El sistema de coordenadas UTM (Universal '
                                'Transversal de Mercator) se basa en la '
                                'proyección cartográfica transversa de '
                                'Mercator, tangente a un meridiano.',
                                'A diferencia de las coordenadas geográficas '
                                '(longitud/latitud), las magnitudes UTM se '
                                'expresan en metros.',
                                'El sistema UTM fue desarrollado por el '
                                'Cuerpo de Ingenieros del Ejército de EE.UU. '
                                'en la década de 1940; actualmente usa el '
                                'elipsoide WGS84.',
                                'La Tierra está dividida en 60 zonas o husos '
                                'UTM de 6° de longitud cada uno.',
                                'La Tierra está dividida en 20 bandas UTM: '
                                '19 de 8° de latitud y una última de 12°, '
                                'identificadas con letras de la C a la X '
                                '(sin I ni O).',
                                'El territorio peruano se ubica en las zonas '
                                'o husos 17, 18 y 19, y en las bandas K, L y '
                                'M.',
                                'La Red UTM se utiliza entre los 80° de '
                                'latitud sur y los 84° de latitud norte; por '
                                'encima se usa la Red Universal '
                                'Estereográfica Polar (UPS).']},
                     {'titulo': 'TELEDETECCIÓN, GPS Y HUSOS HORARIOS',
                      'items': ['La teledetección es la técnica que permite '
                                'obtener información de un objeto o área '
                                'mediante el análisis de imágenes, sin '
                                'contacto físico.',
                                'La teledetección espacial adquiere imágenes '
                                'de la superficie terrestre mediante '
                                'sensores instalados en satélites '
                                'artificiales.',
                                'El GPS (Sistema de Posicionamiento Global) '
                                'fue desarrollado por el Departamento de '
                                'Defensa de los Estados Unidos.',
                                'El sistema GPS utiliza 24 satélites en '
                                'órbita, a 200 km de altura, con '
                                'trayectorias sincronizadas.',
                                'Un huso horario es una franja comprendida '
                                'entre dos meridianos, con un ángulo de '
                                'separación de 15 grados.',
                                'La Tierra está dividida en 24 husos '
                                'horarios, ya que su circunferencia tiene '
                                '360 grados.',
                                'La convención universal que estableció los '
                                'husos horarios se realizó en Washington en '
                                'el año 1884.']}],
  'qr_reto': [{'pregunta': 'Los meridianos convergen (se unen) en:',
               'respuesta': 'Los polos'},
              {'pregunta': 'El Trópico de Capricornio se ubica en el '
                           'hemisferio:',
               'respuesta': 'Sur'},
              {'pregunta': 'El meridiano de Greenwich y su opuesto dividen '
                           'la Tierra en los hemisferios:',
               'respuesta': 'Occidental y Oriental'}],
  'qr_dato': 'La proyección cilíndrica más utilizada es la de Mercator.'},
 {'num': 4,
  'titulo': 'Mapas: Lectura e Interpretación',
  'secciones': [{'titulo': '4.1 CONCEPTO Y CLASIFICACIÓN',
                 'items': ['Un mapa es una representación, total o parcial, '
                           'de la superficie curva de la Tierra sobre una '
                           'superficie {plana}.',
                           'Los mapas se clasifican según el tamaño de la '
                           '{escala} y según su {función}.',
                           'Según su función, los mapas pueden ser '
                           '{temáticos} o generales.',
                           'Los mapas {temáticos} representan el territorio '
                           'mediante símbolos de un aspecto concreto de la '
                           'realidad, físico o humano.',
                           'Los mapas {generales} representan de manera '
                           'completa pero genérica los elementos de un '
                           'territorio, como los que aparecen en los '
                           'atlas.']},
                {'titulo': '4.2 ELEMENTOS DEL MAPA',
                 'items': ['El {título} del mapa se ubica en la parte '
                           'superior y representa el contenido del mapa.',
                           'La {orientación} del mapa se indica con una Rosa '
                           'Náutica o una flecha que señala el Norte; el '
                           'Norte corresponde a la parte {superior}.',
                           'La {ubicación} de un mapa se realiza mediante la '
                           'red geográfica de meridianos y paralelos.',
                           'La {leyenda}, llamada también signos '
                           'convencionales, es el lenguaje visual que '
                           'representa elementos del terreno como carreteras '
                           'o líneas férreas.',
                           'La {escala} indica cuántas veces se ha reducido '
                           'el terreno real para representarlo en el mapa; '
                           'por ejemplo, 1:100 000 significa una reducción '
                           'de {100 000} veces.']},
                {'titulo': '4.3 LA CARTA GEOGRÁFICA NACIONAL DEL PERÚ',
                 'items': ['La {Carta Geográfica Nacional} es un gran mapa '
                           'de nuestro país dividido en {501} hojas o mapas '
                           'topográficos.',
                           'La Carta Nacional se ha levantado a una escala '
                           'de {1:100 000}; el trabajo fue iniciado por el '
                           '{Instituto Geográfico Militar}.',
                           'Originalmente se usó el sistema de la plancheta '
                           'con escala de {1:200 000}; hoy se emplean '
                           'procedimientos modernos.',
                           'Cada hoja representa un área de {30} minutos de '
                           'longitud por 30 minutos de latitud.',
                           'Una hoja mide 55,4 cm x 54,1 cm, equivalente en '
                           'el terreno a {55,4} km de largo por 54,1 km de '
                           'ancho, con un área de 2997,1 km².']},
                {'titulo': '4.4 PARTES DE LA HOJA O MAPA TOPOGRÁFICO',
                 'items': ['Una hoja o mapa topográfico está compuesta de '
                           'tres partes: {cuerpo}, información marginal, y '
                           'signos convencionales o {leyenda}.',
                           'El {cuerpo} de la hoja constituye la '
                           'representación del espacio geográfico; presenta '
                           'la {planimetría} y la altimetría.',
                           'La {planimetría} es la ubicación del espacio en '
                           'un plano mediante simbología convencional, '
                           'representando elementos naturales o '
                           '{culturales}.',
                           'La {altimetría} está representada por las curvas '
                           'de nivel, que indican la {altitud} sobre el '
                           'nivel del mar.',
                           'Las {curvas de nivel} son líneas a intervalos '
                           'iguales, con un valor determinado de altitud.',
                           'La {información marginal} constituye el borde de '
                           'la carta; incluye nombre y número de la hoja, '
                           'cuadro de hojas vecinas, {coordenadas} y escala.',
                           'Los {signos convencionales} o leyenda permiten '
                           'interpretar la simbología de la carta.']},
                {'titulo': '4.5 CLASES DE ESCALA Y CÁLCULO DE DISTANCIAS',
                 'items': ['Existen dos clases de escala: la escala '
                           '{numérica}, expresada como una fracción, y la '
                           'escala {gráfica}, un segmento graduado.',
                           'En un mapa de escala 1:50 000, cada centímetro '
                           'del mapa equivale a {0,5} km en el terreno real.',
                           'En un mapa de escala 1:250 000, cada centímetro '
                           'del mapa equivale a {2,5} km en el terreno real.',
                           'Para hallar la distancia real a partir del mapa, '
                           'se aplica una regla de {tres} simple entre la '
                           'escala y la medida tomada.',
                           'Los tres casos típicos de ejercicios con escalas '
                           'son: hallar la distancia en el terreno real, '
                           'hallar la distancia en el {mapa}, y hallar la '
                           '{escala} del mapa.']},
                {'titulo': '4.6 EJEMPLO: HALLANDO LA ESCALA DE UN MAPA',
                 'items': ['Para hallar la escala de un mapa, el número {1} '
                           'siempre se coloca al inicio de la proporción (1: '
                           '?).',
                           'Si 65 cm en el mapa representan 2080 km reales, '
                           'la escala numérica resultante es {1:3 200 000}.',
                           'Para hallar la distancia en el mapa a partir de '
                           'la real, también se aplica una regla de tres, '
                           'invirtiendo el {procedimiento}.',
                           'Las escalas gráficas, expresadas como un '
                           'segmento graduado, también se pueden convertir a '
                           'escala {numérica}.']}],
  'cuadros': [{'titulo': '4.1 MAPAS SEGÚN EL TAMAÑO DE LA ESCALA',
               'encabezados': ['Escala', 'Representa'],
               'filas': [['Muy {grande}',
                          'Planos de viviendas y {edificios}'],
                         ['{Grande}',
                          'Centros poblados, ciudades y {distritos}'],
                         ['{Intermedia}',
                          'Provincias, departamentos y {regiones}'],
                         ['{Pequeña}', 'Países'],
                         ['Muy {pequeña}', 'Continentes y el {mundo}']]},
              {'titulo': '4.1 MAPAS TEMÁTICOS FÍSICOS Y HUMANOS',
               'encabezados': ['Tipo', 'Mapa', 'Indica'],
               'filas': [['{Físico}',
                          'Climático',
                          'Distribución de {climas}'],
                         ['Físico',
                          '{Hidrográfico}',
                          'Distribución de ríos y lagos'],
                         ['{Humano}',
                          'Político',
                          'Fronteras y límites {administrativos}'],
                         ['Humano',
                          '{Económico}',
                          'Distribución de actividades económicas']]}],
  'preguntas': [{'pregunta': 'Un mapa es una representación de la superficie '
                             'curva de la Tierra sobre una superficie:',
                 'alternativas': ['Cilíndrica',
                                  'Plana',
                                  'Irregular',
                                  'Esférica',
                                  'Cónica'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas se clasifican, según su función, en '
                             'generales y:',
                 'alternativas': ['Políticos',
                                  'Satelitales',
                                  'Digitales',
                                  'Físicos',
                                  'Temáticos'],
                 'correcta': 'E'},
                {'pregunta': 'Los mapas que representan el territorio por '
                             'medio de símbolos de un aspecto concreto son '
                             'los:',
                 'alternativas': ['Temáticos',
                                  'Topográficos',
                                  'Náuticos',
                                  'Generales',
                                  'Catastrales'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa con escala 1:50 000 corresponde a una '
                             'escala:',
                 'alternativas': ['Intermedia',
                                  'Muy grande',
                                  'Grande',
                                  'Muy pequeña',
                                  'Pequeña'],
                 'correcta': 'C'},
                {'pregunta': 'Los mapas de continentes y del mundo '
                             'corresponden a una escala:',
                 'alternativas': ['Muy grande',
                                  'Muy pequeña',
                                  'Grande',
                                  'Intermedia',
                                  'Pequeña'],
                 'correcta': 'B'},
                {'pregunta': 'Un plano de una vivienda corresponde a una '
                             'escala:',
                 'alternativas': ['Muy pequeña',
                                  'Pequeña',
                                  'Intermedia',
                                  'Muy grande',
                                  'Grande estándar'],
                 'correcta': 'D'},
                {'pregunta': 'El elemento del mapa que se ubica en la parte '
                             'superior e indica el contenido es:',
                 'alternativas': ['La red geográfica',
                                  'El título',
                                  'La escala',
                                  'La orientación',
                                  'La leyenda'],
                 'correcta': 'B'},
                {'pregunta': 'En un mapa correctamente orientado, el Norte '
                             'corresponde a la parte:',
                 'alternativas': ['Derecha',
                                  'Inferior',
                                  'Superior',
                                  'Central',
                                  'Izquierda'],
                 'correcta': 'C'},
                {'pregunta': 'La ubicación de un mapa se determina mediante:',
                 'alternativas': ['La red de meridianos y paralelos',
                                  'Los colores usados',
                                  'El tamaño del papel',
                                  'El título',
                                  'La leyenda únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los signos convencionales de un mapa '
                             'constituyen:',
                 'alternativas': ['El marco',
                                  'El título',
                                  'La leyenda',
                                  'La escala',
                                  'La orientación'],
                 'correcta': 'C'},
                {'pregunta': 'Una escala de 1:100 000 significa que el '
                             'terreno real fue reducido:',
                 'alternativas': ['100 000 veces',
                                  '1 000 000 veces',
                                  '10 veces',
                                  '100 veces',
                                  '1000 veces'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa climático indica la distribución de:',
                 'alternativas': ['Los diversos tipos de clima',
                                  'Ríos y lagos',
                                  'Especies vegetales',
                                  'Fronteras políticas',
                                  'Actividades económicas'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa hidrográfico indica principalmente:',
                 'alternativas': ['Tipos de clima',
                                  'Actividades agrícolas',
                                  'Densidad poblacional',
                                  'Fronteras administrativas',
                                  'La distribución de ríos y lagos'],
                 'correcta': 'E'},
                {'pregunta': 'Un mapa político indica:',
                 'alternativas': ['Fronteras políticas y límites '
                                  'administrativos',
                                  'Recursos minerales',
                                  'Distribución de lenguas',
                                  'Tipos de suelo',
                                  'Tipos de vegetación'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa económico indica la distribución '
                             'territorial de:',
                 'alternativas': ['Los acontecimientos históricos',
                                  'Los climas',
                                  'Las actividades económicas',
                                  'Las fronteras',
                                  'Las lenguas habladas'],
                 'correcta': 'C'},
                {'pregunta': 'Un mapa lingüístico corresponde a un mapa '
                             'temático de tipo:',
                 'alternativas': ['Geológico',
                                  'Hidrográfico',
                                  'Climático',
                                  'Físico',
                                  'Humano'],
                 'correcta': 'E'},
                {'pregunta': 'Un mapa geológico indica:',
                 'alternativas': ['Las fronteras políticas',
                                  'La composición de las rocas de la corteza '
                                  'terrestre',
                                  'La distribución de lenguas',
                                  'Las actividades económicas',
                                  'La densidad de población'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas generales suelen aparecer en:',
                 'alternativas': ['Solo periódicos',
                                  'Solo revistas científicas',
                                  'Los atlas',
                                  'Solo internet',
                                  'Solo documentos legales'],
                 'correcta': 'C'},
                {'pregunta': 'Un mapa de provincias y departamentos '
                             'corresponde a una escala:',
                 'alternativas': ['Nula',
                                  'Muy grande',
                                  'Pequeña extrema',
                                  'Intermedia',
                                  'Muy pequeña'],
                 'correcta': 'D'},
                {'pregunta': 'La ventaja principal del mapa frente a la '
                             'esfera terrestre es:',
                 'alternativas': ['Representar en tres dimensiones',
                                  'Facilidad de manejo y representación '
                                  'ampliada de áreas pequeñas',
                                  'Mayor exactitud absoluta',
                                  'No requerir escala',
                                  'Eliminar toda deformación'],
                 'correcta': 'B'},
                {'pregunta': 'La escala que emplea segmentos gráficos para '
                             'indicar la proporción entre la distancia y su '
                             'medida en el mapa es la: (II CEPRU 2022)',
                 'alternativas': ['Escala numérica',
                                  'Escala natural',
                                  'Escala de ampliación',
                                  'Escala gráfica',
                                  'Escala de reducción'],
                 'correcta': 'D'},
                {'pregunta': 'La proyección cartográfica que se emplea para '
                             'graficar zonas de alta latitud es: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Rectangular',
                                  'Cónica',
                                  'Mercator',
                                  'Azimutal',
                                  'Escalar'],
                 'correcta': 'D'},
                {'pregunta': 'La Carta Geográfica Nacional del Perú es un '
                             'gran mapa dividido en un número de hojas igual '
                             'a:',
                 'alternativas': ['305', '501', '601', '201', '101'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta Geográfica Nacional del Perú se ha '
                             'levantado a una escala de:',
                 'alternativas': ['1:100 000',
                                  '1:1 000 000',
                                  '1:10 000',
                                  '1:50 000',
                                  '1:200 000'],
                 'correcta': 'A'},
                {'pregunta': 'El trabajo de la Carta Geográfica Nacional fue '
                             'iniciado por el:',
                 'alternativas': ['Instituto Nacional de Estadística',
                                  'Servicio Nacional de Meteorología',
                                  'Instituto Geofísico del Perú',
                                  'Ministerio de Defensa',
                                  'Instituto Geográfico Militar'],
                 'correcta': 'E'},
                {'pregunta': 'Cada hoja de la Carta Geográfica Nacional '
                             'representa un área de longitud y latitud de:',
                 'alternativas': ['45 minutos',
                                  '20 minutos',
                                  '15 minutos',
                                  '60 minutos',
                                  '30 minutos'],
                 'correcta': 'E'},
                {'pregunta': 'Una hoja o mapa topográfico está compuesta de '
                             'tres partes: cuerpo, signos convencionales y:',
                 'alternativas': ['Curvas de nivel',
                                  'Coordenadas UTM',
                                  'Red geográfica',
                                  'Escala numérica',
                                  'Información marginal'],
                 'correcta': 'E'},
                {'pregunta': 'En la hoja de la Carta Geográfica Nacional, la '
                             'planimetría y la altimetría forman parte de:',
                 'alternativas': ['La escala de la hoja',
                                  'El cuerpo de la hoja',
                                  'Los signos convencionales',
                                  'La información marginal',
                                  'El sistema de coordenadas'],
                 'correcta': 'B'},
                {'pregunta': 'La ubicación del espacio en un plano mediante '
                             'simbología convencional, representando '
                             'elementos naturales o culturales, se llama:',
                 'alternativas': ['Planimetría',
                                  'Curva de nivel',
                                  'Leyenda',
                                  'Altimetría',
                                  'Isoyeta'],
                 'correcta': 'A'},
                {'pregunta': 'Las curvas de nivel, que indican la altitud '
                             'sobre el nivel del mar, forman parte de la:',
                 'alternativas': ['Escala',
                                  'Información marginal',
                                  'Planimetría',
                                  'Altimetría',
                                  'Leyenda'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y CLASIFICACIÓN',
                      'items': ['Un mapa es una representación, total o '
                                'parcial, de la superficie curva de la '
                                'Tierra sobre una superficie plana.',
                                'Los mapas se clasifican según el tamaño de '
                                'la escala y según su función.',
                                'Según su función, los mapas pueden ser '
                                'temáticos o generales.',
                                'Los mapas temáticos representan el '
                                'territorio mediante símbolos de un aspecto '
                                'concreto de la realidad, físico o humano.',
                                'Los mapas generales representan de manera '
                                'completa pero genérica los elementos de un '
                                'territorio, como los que aparecen en los '
                                'atlas.']},
                     {'titulo': 'ELEMENTOS DEL MAPA',
                      'items': ['El título del mapa se ubica en la parte '
                                'superior y representa el contenido del '
                                'mapa.',
                                'La orientación del mapa se indica con una '
                                'Rosa Náutica o una flecha que señala el '
                                'Norte; el Norte corresponde a la parte '
                                'superior.',
                                'La ubicación de un mapa se realiza mediante '
                                'la red geográfica de meridianos y '
                                'paralelos.',
                                'La leyenda, llamada también signos '
                                'convencionales, es el lenguaje visual que '
                                'representa elementos del terreno como '
                                'carreteras o líneas férreas.',
                                'La escala indica cuántas veces se ha '
                                'reducido el terreno real para representarlo '
                                'en el mapa; por ejemplo, 1:100 000 '
                                'significa una reducción de 100 000 veces.']},
                     {'titulo': 'LA CARTA GEOGRÁFICA NACIONAL DEL PERÚ',
                      'items': ['La Carta Geográfica Nacional es un gran '
                                'mapa de nuestro país dividido en 501 hojas '
                                'o mapas topográficos.',
                                'La Carta Nacional se ha levantado a una '
                                'escala de 1:100 000; el trabajo fue '
                                'iniciado por el Instituto Geográfico '
                                'Militar.',
                                'Originalmente se usó el sistema de la '
                                'plancheta con escala de 1:200 000; hoy se '
                                'emplean procedimientos modernos.',
                                'Cada hoja representa un área de 30 minutos '
                                'de longitud por 30 minutos de latitud.',
                                'Una hoja mide 55,4 cm x 54,1 cm, '
                                'equivalente en el terreno a 55,4 km de '
                                'largo por 54,1 km de ancho, con un área de '
                                '2997,1 km².']},
                     {'titulo': 'PARTES DE LA HOJA O MAPA TOPOGRÁFICO',
                      'items': ['Una hoja o mapa topográfico está compuesta '
                                'de tres partes: cuerpo, información '
                                'marginal, y signos convencionales o '
                                'leyenda.',
                                'El cuerpo de la hoja constituye la '
                                'representación del espacio geográfico; '
                                'presenta la planimetría y la altimetría.',
                                'La planimetría es la ubicación del espacio '
                                'en un plano mediante simbología '
                                'convencional, representando elementos '
                                'naturales o culturales.',
                                'La altimetría está representada por las '
                                'curvas de nivel, que indican la altitud '
                                'sobre el nivel del mar.',
                                'Las curvas de nivel son líneas a intervalos '
                                'iguales, con un valor determinado de '
                                'altitud.',
                                'La información marginal constituye el borde '
                                'de la carta; incluye nombre y número de la '
                                'hoja, cuadro de hojas vecinas, coordenadas '
                                'y escala.',
                                'Los signos convencionales o leyenda '
                                'permiten interpretar la simbología de la '
                                'carta.']},
                     {'titulo': 'CLASES DE ESCALA Y CÁLCULO DE DISTANCIAS',
                      'items': ['Existen dos clases de escala: la escala '
                                'numérica, expresada como una fracción, y la '
                                'escala gráfica, un segmento graduado.',
                                'En un mapa de escala 1:50 000, cada '
                                'centímetro del mapa equivale a 0,5 km en el '
                                'terreno real.',
                                'En un mapa de escala 1:250 000, cada '
                                'centímetro del mapa equivale a 2,5 km en el '
                                'terreno real.',
                                'Para hallar la distancia real a partir del '
                                'mapa, se aplica una regla de tres simple '
                                'entre la escala y la medida tomada.',
                                'Los tres casos típicos de ejercicios con '
                                'escalas son: hallar la distancia en el '
                                'terreno real, hallar la distancia en el '
                                'mapa, y hallar la escala del mapa.']},
                     {'titulo': 'EJEMPLO: HALLANDO LA ESCALA DE UN MAPA',
                      'items': ['Para hallar la escala de un mapa, el número '
                                '1 siempre se coloca al inicio de la '
                                'proporción (1: ?).',
                                'Si 65 cm en el mapa representan 2080 km '
                                'reales, la escala numérica resultante es '
                                '1:3 200 000.',
                                'Para hallar la distancia en el mapa a '
                                'partir de la real, también se aplica una '
                                'regla de tres, invirtiendo el '
                                'procedimiento.',
                                'Las escalas gráficas, expresadas como un '
                                'segmento graduado, también se pueden '
                                'convertir a escala numérica.']}],
  'qr_reto': [{'pregunta': 'Los mapas de continentes y del mundo '
                           'corresponden a una escala:',
               'respuesta': 'Muy pequeña'},
              {'pregunta': 'Un mapa hidrográfico indica principalmente:',
               'respuesta': 'La distribución de ríos y lagos'},
              {'pregunta': 'La ventaja principal del mapa frente a la esfera '
                           'terrestre es:',
               'respuesta': 'Facilidad de manejo y representación ampliada '
                            'de áreas pequeñas'}],
  'qr_dato': 'La Carta Geográfica Nacional es un gran mapa de nuestro país '
             'dividido en 501 hojas o mapas topográficos.'},
 {'num': 5,
  'titulo': 'Relieve Terrestre: Origen y Procesos Dinámicos',
  'secciones': [{'titulo': '5.1 ESTRUCTURA INTERNA DE LA TIERRA: EL NÚCLEO Y '
                           'EL MANTO',
                 'items': ['El núcleo alcanza temperaturas entre 4000° y '
                           '{5000}° C, y está formado por níquel y {hierro}.',
                           'El núcleo externo y el núcleo interno están '
                           'limitados por la Discontinuidad de {Lehman}.',
                           'El núcleo está limitado con el manto por la '
                           'Discontinuidad de {Wiechert Gutemberg}.',
                           'El manto se divide en manto externo e interno, '
                           'separados por la Discontinuidad de {Repetti}.',
                           'El manto superior se compone de hierro y '
                           'silicatos de {magnesio}, con temperaturas entre '
                           '1700° y 1800° C.',
                           'El manto inferior o {pirosfera} está conformado '
                           'por olivinos, peridotita y óxidos de magnesio, '
                           'hierro y silicio.',
                           'El manto está limitado con la corteza por la '
                           'Discontinuidad de {Mohorovicic}.',
                           'La {astenósfera} es una capa débil, blanda y '
                           'plástica del manto, ubicada entre 100 y 300 km '
                           'de profundidad, clave para la Tectónica de '
                           'Placas.']},
                {'titulo': '5.2 LA CORTEZA TERRESTRE',
                 'items': ['La corteza externa, llamada {granítica} o Si Al, '
                           'es la corteza continental, formada por silicio y '
                           'aluminio.',
                           'La corteza interna, llamada {basáltica} o Si Mg, '
                           'es la corteza oceánica, formada por silicio y '
                           'magnesio.',
                           'La corteza externa y la corteza interna están '
                           'separadas por la Discontinuidad de {Conrad}.']},
                {'titulo': '5.3 EL RELIEVE TERRESTRE Y LA GEODINÁMICA '
                           'INTERNA',
                 'items': ['El relieve terrestre es el conjunto de '
                           '{irregularidades} o geoformas que presenta la '
                           'superficie de la Tierra.',
                           'El relieve se origina por procesos internos o '
                           'geodinámica {interna}, y procesos externos o '
                           'geodinámica {externa}.',
                           'La geodinámica interna, o procesos endógenos, '
                           'son fuerzas {constructoras} del relieve, que '
                           'generan montañas, mesetas y altiplanos.',
                           'La geodinámica interna comprende los movimientos '
                           '{orogénicos}, epirogénicos y el vulcanismo.',
                           'Los movimientos {orogénicos} son compresivos, '
                           'laterales y lentos, y originan plegamientos y '
                           '{fallas}.',
                           'Los movimientos {epirogénicos}, también llamados '
                           'tectónica vertical, son de levantamiento y '
                           'hundimiento, y se originan en la {isostasia}.']},
                {'titulo': '5.4 LA ISOSTASIA, EL VULCANISMO Y LA TECTÓNICA '
                           'DE PLACAS',
                 'items': ['La {isostasia} es el principio geofísico que '
                           'explica el equilibrio entre los continentes '
                           'elevados y las cuencas oceánicas deprimidas.',
                           'El {vulcanismo} es el proceso de desplazamiento '
                           'de magma o lava desde el manto hacia la '
                           'superficie, a través de una fisura llamada '
                           '{volcán}.',
                           'La Teoría de la Tectónica de Placas fue '
                           'formulada en {1960} por {Harry Hammond Hess}.',
                           'Según la Tectónica de Placas, la corteza '
                           'terrestre está fraccionada en {28} placas '
                           'rígidas que se mueven por los movimientos '
                           'convectivos del {manto}.',
                           'La placa más grande del planeta es la '
                           '{Pacífica}, que abarca la mayor parte del Océano '
                           'Pacífico.',
                           'El Perú se ubica sobre la placa {Sudamericana}.',
                           'En el sentido {convergente}, cuando una placa '
                           'oceánica choca con una continental, se produce '
                           'la {subducción}, originando bordes destructivos.',
                           'En el sentido {divergente}, las placas se '
                           'separan formando dorsales mesoceánicas y bordes '
                           '{constructivos}.',
                           'En el sentido {lateral}, las placas se desplazan '
                           'una junto a otra originando fallas '
                           '{transformantes} y bordes conservativos.',
                           'La subducción consiste en el hundimiento de una '
                           'placa {oceánica} bajo una placa continental, '
                           'formando las {fosas} marinas.']},
                {'titulo': '5.5 METEORIZACIÓN Y EROSIÓN',
                 'items': ['La {meteorización}, o intemperismo, es el '
                           'proceso de destrucción de las rocas y minerales '
                           'que forman la {corteza}.',
                           'La meteorización {mecánica} o física rompe las '
                           'rocas progresivamente en fragmentos, sin cambios '
                           'en su composición {química}; intervienen cambios '
                           'de temperatura, heladas y sales.',
                           'La meteorización {química} origina cambios en la '
                           'forma y estructura química de las rocas; el agua '
                           'es el principal {agente}.',
                           'La {erosión} es el desgaste de suelos y rocas de '
                           'la superficie terrestre, cuyos materiales son '
                           'arrancados y transportados por agentes erosivos.',
                           'Los principales agentes erosivos son los {ríos}, '
                           'glaciares, vientos, mares y el hombre.']},
                {'titulo': '5.6 RELIEVES SALIENTES Y ENTRANTES',
                 'items': ['Las {cordilleras} son montañas alineadas de '
                           'altitud variable entre 5000 y 6000 msnm; pueden '
                           'tener glaciares si superan los {5500} msnm.',
                           'Las {abras} o pasos son las partes más bajas '
                           'entre dos montañas; tienen importancia para las '
                           '{vías} de comunicación.',
                           'Las {serranías residuales} son alineamientos de '
                           'montañas erosionadas entre 4000 y 4500 m de '
                           'altitud.',
                           'Los {valles} son depresiones entre dos '
                           'elevaciones, con base amplia, aprovechados para '
                           'la agricultura; son centros {demográficos}.',
                           'Los {cañones} son depresiones estrechas y '
                           'profundas, con paredes verticales, que no '
                           'favorecen la actividad {agrícola}: Cañón del '
                           'Colca, Cañón del Apurímac.',
                           'Las {quebradas} son pequeñas depresiones '
                           'alargadas y angostas, recorridas por arroyos y '
                           'ríos {tributarios}.',
                           'Los {pongos} son cortes fluviales profundos en '
                           'las cordilleras: Pongo de {Mainique}, Retama, '
                           'Manseriche.']},
                {'titulo': '5.7 RELIEVES PLANOS Y DEPOSICIONALES',
                 'items': ['Las {llanuras} son extensas superficies planas '
                           'poco accidentadas a poca altitud: llanura del '
                           '{Amazonas}.',
                           'Las {mesetas} son superficies planas a grandes '
                           'altitudes, entre 3000 y 4000 m, limitadas por '
                           'una {depresión}: Meseta de Junín.',
                           'Los {altiplanos} son extensas superficies '
                           'rodeadas por cadenas de montañas: Altiplano del '
                           '{Titicaca}.',
                           'El {cono aluvial} o cono de deyección son '
                           'materiales depositados por corrientes fluviales '
                           'tras las precipitaciones; también incluyen '
                           'derrames {volcánicos} y morrenas.']}],
  'cuadros': [{'titulo': '5.1 ESTRUCTURA INTERNA DE LA TIERRA',
               'encabezados': ['Capa', '% del volumen', 'Espesor'],
               'filas': [['{Corteza}', '1%', '5 a 70 km'],
                         ['{Manto}', '83%', '2800 km'],
                         ['{Núcleo}', '16%', '3450 km']]}],
  'preguntas': [{'pregunta': 'El núcleo terrestre está formado '
                             'principalmente por:',
                 'alternativas': ['Magnesio y oxígeno',
                                  'Potasio y sodio',
                                  'Carbono e hidrógeno',
                                  'Silicio y aluminio',
                                  'Níquel y hierro'],
                 'correcta': 'E'},
                {'pregunta': 'La discontinuidad que limita el núcleo externo '
                             'del núcleo interno es la de:',
                 'alternativas': ['Conrad',
                                  'Lehman',
                                  'Repetti',
                                  'Gutemberg',
                                  'Mohorovicic'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo está limitado con el manto por la '
                             'discontinuidad de:',
                 'alternativas': ['Lehman',
                                  'Repetti',
                                  'Conrad',
                                  'Wiechert Gutemberg',
                                  'Mohorovicic'],
                 'correcta': 'D'},
                {'pregunta': 'El manto externo y el manto interno están '
                             'separados por la discontinuidad de:',
                 'alternativas': ['Lehman',
                                  'Gutemberg',
                                  'Mohorovicic',
                                  'Conrad',
                                  'Repetti'],
                 'correcta': 'E'},
                {'pregunta': 'El manto está limitado con la corteza '
                             'terrestre por la discontinuidad de:',
                 'alternativas': ['Gutemberg',
                                  'Lehman',
                                  'Repetti',
                                  'Mohorovicic',
                                  'Conrad'],
                 'correcta': 'D'},
                {'pregunta': 'La astenósfera es una capa ubicada en:',
                 'alternativas': ['El núcleo interno',
                                  'La corteza oceánica',
                                  'El núcleo externo',
                                  'La corteza continental',
                                  'La parte superior del manto'],
                 'correcta': 'E'},
                {'pregunta': 'La astenósfera es clave para explicar la '
                             'teoría de:',
                 'alternativas': ['El ciclo del agua',
                                  'La formación del universo',
                                  'La formación de galaxias',
                                  'El Big Bang',
                                  'La Tectónica de Placas'],
                 'correcta': 'E'},
                {'pregunta': 'La corteza continental o granítica se compone '
                             'principalmente de:',
                 'alternativas': ['Silicio y aluminio',
                                  'Hierro y níquel',
                                  'Potasio y calcio',
                                  'Silicio y magnesio',
                                  'Carbono y oxígeno'],
                 'correcta': 'A'},
                {'pregunta': 'La corteza oceánica o basáltica se compone '
                             'principalmente de:',
                 'alternativas': ['Oxígeno y carbono',
                                  'Silicio y magnesio',
                                  'Calcio y sodio',
                                  'Silicio y aluminio',
                                  'Hierro y níquel'],
                 'correcta': 'B'},
                {'pregunta': 'La corteza externa y la corteza interna están '
                             'separadas por la discontinuidad de:',
                 'alternativas': ['Gutemberg',
                                  'Mohorovicic',
                                  'Repetti',
                                  'Conrad',
                                  'Lehman'],
                 'correcta': 'D'},
                {'pregunta': 'El relieve terrestre se define como el '
                             'conjunto de:',
                 'alternativas': ['Climas del planeta',
                                  'Irregularidades o geoformas de la '
                                  'superficie',
                                  'Capas de la atmósfera',
                                  'Corrientes marinas',
                                  'Zonas sísmicas únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los procesos que actúan del interior hacia la '
                             'superficie terrestre se llaman:',
                 'alternativas': ['Meteorización',
                                  'Geodinámica externa',
                                  'Sedimentación',
                                  'Geodinámica interna',
                                  'Erosión eólica'],
                 'correcta': 'D'},
                {'pregunta': 'La geodinámica interna es considerada una '
                             'fuerza:',
                 'alternativas': ['Solo erosiva',
                                  'Exclusivamente marina',
                                  'Sin efecto en el relieve',
                                  'Constructora del relieve',
                                  'Destructora del relieve'],
                 'correcta': 'D'},
                {'pregunta': 'Los movimientos orogénicos originan '
                             'principalmente:',
                 'alternativas': ['Glaciación',
                                  'Erosión costera',
                                  'Formación de dunas',
                                  'Plegamientos y fallas',
                                  'Sedimentación fluvial'],
                 'correcta': 'D'},
                {'pregunta': 'Los movimientos orogénicos se caracterizan por '
                             'ser:',
                 'alternativas': ['Aleatorios',
                                  'Verticales y rápidos',
                                  'Explosivos',
                                  'Laterales, compresivos y lentos',
                                  'Solo horizontales rápidos'],
                 'correcta': 'D'},
                {'pregunta': 'Los movimientos epirogénicos también se '
                             'conocen como:',
                 'alternativas': ['Vulcanismo puro',
                                  'Sismicidad superficial',
                                  'Erosión interna',
                                  'Tectónica horizontal',
                                  'Tectónica vertical'],
                 'correcta': 'E'},
                {'pregunta': 'El origen de los movimientos epirogénicos se '
                             'encuentra en:',
                 'alternativas': ['Las corrientes marinas',
                                  'La isostasia',
                                  'El vulcanismo',
                                  'La erosión eólica',
                                  'La meteorización química'],
                 'correcta': 'B'},
                {'pregunta': 'Los movimientos epirogénicos afectan grandes '
                             'extensiones sin:',
                 'alternativas': ['Elevar el terreno',
                                  'Deformar la estructura geológica de las '
                                  'rocas',
                                  'Modificar la altitud',
                                  'Generar continentes',
                                  'Hundir el terreno'],
                 'correcta': 'B'},
                {'pregunta': 'La geodinámica interna comprende movimientos '
                             'orogénicos, epirogénicos y:',
                 'alternativas': ['Vulcanismo',
                                  'Sedimentación eólica',
                                  'Glaciarismo',
                                  'Meteorización física',
                                  'Erosión fluvial'],
                 'correcta': 'A'},
                {'pregunta': 'El manto representa aproximadamente qué '
                             'porcentaje del volumen terrestre:',
                 'alternativas': ['50%', '83%', '25%', '1%', '16%'],
                 'correcta': 'B'},
                {'pregunta': 'La segunda cordillera con mayor superficie '
                             'glaciar en el Perú es: (II CEPRU 2025)',
                 'alternativas': ['Vilcanota',
                                  'Vilcabamba',
                                  'Huayhuash',
                                  'Ampato',
                                  'Huatapallana'],
                 'correcta': 'A'},
                {'pregunta': 'Las placas tectónicas en sentido convergente '
                             'originan bordes: (II CEPRU 2024)',
                 'alternativas': ['Moderados',
                                  'Convencionales',
                                  'Constructivos',
                                  'Destructivos',
                                  'Conservativos'],
                 'correcta': 'D'},
                {'pregunta': 'En un glaciar, la parte donde se produce la '
                             'pérdida de masa de hielo se llama: (II CEPRU '
                             '2024)',
                 'alternativas': ['Morrenas glaciares',
                                  'Zona de acumulación',
                                  'Área de compactación',
                                  'Línea de equilibrio',
                                  'Zona de ablación'],
                 'correcta': 'E'},
                {'pregunta': 'Es la discontinuidad entre el núcleo interno y '
                             'el núcleo externo: (II CEPRU 2022)',
                 'alternativas': ['W. Gutenberg',
                                  'Repetti',
                                  'Lehman',
                                  'Conrad',
                                  'Mohorovicic'],
                 'correcta': 'C'},
                {'pregunta': 'Ciencia que estudia el origen, evolución y '
                             'formas de relieve: (I CEPRU 2023)',
                 'alternativas': ['Geodesia',
                                  'Geosistema',
                                  'Edafología',
                                  'Geomorfología',
                                  'Fitogeografía'],
                 'correcta': 'D'},
                {'pregunta': 'Las placas tectónicas se mueven en tres '
                             'direcciones: (I CEPRU 2024)',
                 'alternativas': ['Divergente - vertical - lineal',
                                  'Divergente - colateral - convergente',
                                  'Lateral - convergente - divergente',
                                  'Lateral - horizontal - convergente',
                                  'Convergente - lineal - paralelo'],
                 'correcta': 'C'},
                {'pregunta': 'Las partes de un volcán son: (I CEPRU 2024)',
                 'alternativas': ['Lava, cráter y chimenea',
                                  'Cráter, chimenea y cámara magmática',
                                  'Cámara magmática, cono y lava',
                                  'Cono, cráter y magma',
                                  'Chimenea, cono y cráter'],
                 'correcta': 'E'},
                {'pregunta': 'El intemperismo y la erosión son procesos que '
                             'forman el relieve terrestre, originados por la '
                             'energía: (Primera Oportunidad UNSAAC 2021)',
                 'alternativas': ['De meteoritos',
                                  'Interna de la Tierra',
                                  'Solar',
                                  'De la luna',
                                  'Volcánica'],
                 'correcta': 'C'},
                {'pregunta': 'Las placas tectónicas en su sentido divergente '
                             'se caracterizan por ser: (Primera Oportunidad '
                             'UNSAAC 2023)',
                 'alternativas': ['Destructivas',
                                  'Laterales',
                                  'Constructivas',
                                  'Compresivas',
                                  'Conservativas'],
                 'correcta': 'C'},
                {'pregunta': 'La discontinuidad más próxima al centro de la '
                             'Tierra es: (Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Mohorovicic',
                                  'Lehman',
                                  'Gutenberg',
                                  'Repetti',
                                  'Conrad'],
                 'correcta': 'B'},
                {'pregunta': 'Es considerado el nevado más alto de la zona '
                             'tropical del mundo: (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ['Misti',
                                  'Salkantay',
                                  'Barroso',
                                  'Alpamayo',
                                  'Huascarán'],
                 'correcta': 'E'},
                {'pregunta': 'El proceso de destrucción de las rocas y '
                             'minerales que forman la corteza terrestre se '
                             'llama:',
                 'alternativas': ['Diastrofismo',
                                  'Sedimentación',
                                  'Erosión',
                                  'Orogénesis',
                                  'Meteorización o intemperismo'],
                 'correcta': 'E'},
                {'pregunta': 'La meteorización que rompe las rocas '
                             'progresivamente en fragmentos, sin cambios en '
                             'su composición química, se llama '
                             'meteorización:',
                 'alternativas': ['Biológica',
                                  'Mecánica o física',
                                  'Orgánica',
                                  'Cristalina',
                                  'Química'],
                 'correcta': 'B'},
                {'pregunta': 'La meteorización que origina cambios en la '
                             'forma y estructura química de las rocas se '
                             'llama meteorización:',
                 'alternativas': ['Térmica',
                                  'Física',
                                  'Mecánica',
                                  'Química',
                                  'Eólica'],
                 'correcta': 'D'},
                {'pregunta': 'El desgaste de suelos y rocas de la superficie '
                             'terrestre, cuyos materiales son arrancados y '
                             'transportados por agentes erosivos, se llama:',
                 'alternativas': ['Orogénesis',
                                  'Sedimentación',
                                  'Diastrofismo',
                                  'Meteorización',
                                  'Erosión'],
                 'correcta': 'E'},
                {'pregunta': 'Las montañas alineadas de altitud variable '
                             'entre 5000 y 6000 msnm se llaman:',
                 'alternativas': ['Llanuras',
                                  'Altiplanos',
                                  'Serranías residuales',
                                  'Cordilleras',
                                  'Mesetas'],
                 'correcta': 'D'},
                {'pregunta': 'Las partes más bajas entre dos montañas, '
                             'importantes para las vías de comunicación, se '
                             'llaman:',
                 'alternativas': ['Pongos',
                                  'Abras o pasos',
                                  'Cañones',
                                  'Quebradas',
                                  'Valles'],
                 'correcta': 'B'},
                {'pregunta': 'Los alineamientos de montañas erosionadas '
                             'entre 4000 y 4500 m de altitud se llaman:',
                 'alternativas': ['Altiplanos',
                                  'Serranías residuales',
                                  'Mesetas',
                                  'Abras',
                                  'Cordilleras'],
                 'correcta': 'B'},
                {'pregunta': 'Las depresiones entre dos elevaciones, de base '
                             'amplia, aprovechadas para la agricultura y '
                             'consideradas centros demográficos, se llaman:',
                 'alternativas': ['Valles',
                                  'Mesetas',
                                  'Quebradas',
                                  'Cañones',
                                  'Pongos'],
                 'correcta': 'A'},
                {'pregunta': 'Las depresiones estrechas y profundas, con '
                             'paredes verticales, que no favorecen la '
                             'actividad agrícola, se llaman:',
                 'alternativas': ['Mesetas',
                                  'Altiplanos',
                                  'Llanuras',
                                  'Cañones',
                                  'Valles'],
                 'correcta': 'D'},
                {'pregunta': 'Los cortes fluviales profundos en las '
                             'cordilleras, como el de Mainique, se llaman:',
                 'alternativas': ['Pongos',
                                  'Cañones',
                                  'Valles',
                                  'Abras',
                                  'Quebradas'],
                 'correcta': 'A'},
                {'pregunta': 'Las superficies planas a grandes altitudes, '
                             'entre 3000 y 4000 m, limitadas por una '
                             'depresión, se llaman:',
                 'alternativas': ['Mesetas',
                                  'Altiplanos',
                                  'Cordilleras',
                                  'Llanuras',
                                  'Valles'],
                 'correcta': 'A'},
                {'pregunta': 'Las extensas superficies rodeadas por cadenas '
                             'de montañas, como el del Titicaca, se llaman:',
                 'alternativas': ['Altiplanos',
                                  'Serranías',
                                  'Llanuras',
                                  'Mesetas',
                                  'Valles'],
                 'correcta': 'A'},
                {'pregunta': 'Los materiales depositados por corrientes '
                             'fluviales tras las precipitaciones se llaman:',
                 'alternativas': ['Deltas exclusivos',
                                  'Cono aluvial o de deyección',
                                  'Derrames volcánicos exclusivos',
                                  'Meandros',
                                  'Morrenas exclusivas'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'ESTRUCTURA INTERNA DE LA TIERRA: EL NÚCLEO '
                                'Y EL MANTO',
                      'items': ['El núcleo alcanza temperaturas entre 4000° '
                                'y 5000° C, y está formado por níquel y '
                                'hierro.',
                                'El núcleo externo y el núcleo interno están '
                                'limitados por la Discontinuidad de Lehman.',
                                'El núcleo está limitado con el manto por la '
                                'Discontinuidad de Wiechert Gutemberg.',
                                'El manto se divide en manto externo e '
                                'interno, separados por la Discontinuidad de '
                                'Repetti.',
                                'El manto superior se compone de hierro y '
                                'silicatos de magnesio, con temperaturas '
                                'entre 1700° y 1800° C.',
                                'El manto inferior o pirosfera está '
                                'conformado por olivinos, peridotita y '
                                'óxidos de magnesio, hierro y silicio.']},
                     {'titulo': 'LA CORTEZA TERRESTRE',
                      'items': ['La corteza externa, llamada granítica o Si '
                                'Al, es la corteza continental, formada por '
                                'silicio y aluminio.',
                                'La corteza interna, llamada basáltica o Si '
                                'Mg, es la corteza oceánica, formada por '
                                'silicio y magnesio.',
                                'La corteza externa y la corteza interna '
                                'están separadas por la Discontinuidad de '
                                'Conrad.']},
                     {'titulo': 'EL RELIEVE TERRESTRE Y LA GEODINÁMICA '
                                'INTERNA',
                      'items': ['El relieve terrestre es el conjunto de '
                                'irregularidades o geoformas que presenta la '
                                'superficie de la Tierra.',
                                'El relieve se origina por procesos internos '
                                'o geodinámica interna, y procesos externos '
                                'o geodinámica externa.',
                                'La geodinámica interna, o procesos '
                                'endógenos, son fuerzas constructoras del '
                                'relieve, que generan montañas, mesetas y '
                                'altiplanos.',
                                'La geodinámica interna comprende los '
                                'movimientos orogénicos, epirogénicos y el '
                                'vulcanismo.',
                                'Los movimientos orogénicos son compresivos, '
                                'laterales y lentos, y originan plegamientos '
                                'y fallas.',
                                'Los movimientos epirogénicos, también '
                                'llamados tectónica vertical, son de '
                                'levantamiento y hundimiento, y se originan '
                                'en la isostasia.']},
                     {'titulo': 'LA ISOSTASIA, EL VULCANISMO Y LA TECTÓNICA '
                                'DE PLACAS',
                      'items': ['La isostasia es el principio geofísico que '
                                'explica el equilibrio entre los continentes '
                                'elevados y las cuencas oceánicas '
                                'deprimidas.',
                                'El vulcanismo es el proceso de '
                                'desplazamiento de magma o lava desde el '
                                'manto hacia la superficie, a través de una '
                                'fisura llamada volcán.',
                                'La Teoría de la Tectónica de Placas fue '
                                'formulada en 1960 por Harry Hammond Hess.',
                                'Según la Tectónica de Placas, la corteza '
                                'terrestre está fraccionada en 28 placas '
                                'rígidas que se mueven por los movimientos '
                                'convectivos del manto.',
                                'La placa más grande del planeta es la '
                                'Pacífica, que abarca la mayor parte del '
                                'Océano Pacífico.',
                                'El Perú se ubica sobre la placa '
                                'Sudamericana.']},
                     {'titulo': 'METEORIZACIÓN Y EROSIÓN',
                      'items': ['La meteorización, o intemperismo, es el '
                                'proceso de destrucción de las rocas y '
                                'minerales que forman la corteza.',
                                'La meteorización mecánica o física rompe '
                                'las rocas progresivamente en fragmentos, '
                                'sin cambios en su composición química; '
                                'intervienen cambios de temperatura, heladas '
                                'y sales.',
                                'La meteorización química origina cambios en '
                                'la forma y estructura química de las rocas; '
                                'el agua es el principal agente.',
                                'La erosión es el desgaste de suelos y rocas '
                                'de la superficie terrestre, cuyos '
                                'materiales son arrancados y transportados '
                                'por agentes erosivos.',
                                'Los principales agentes erosivos son los '
                                'ríos, glaciares, vientos, mares y el '
                                'hombre.']},
                     {'titulo': 'RELIEVES SALIENTES Y ENTRANTES',
                      'items': ['Las cordilleras son montañas alineadas de '
                                'altitud variable entre 5000 y 6000 msnm; '
                                'pueden tener glaciares si superan los 5500 '
                                'msnm.',
                                'Las abras o pasos son las partes más bajas '
                                'entre dos montañas; tienen importancia para '
                                'las vías de comunicación.',
                                'Las serranías residuales son alineamientos '
                                'de montañas erosionadas entre 4000 y 4500 m '
                                'de altitud.',
                                'Los valles son depresiones entre dos '
                                'elevaciones, con base amplia, aprovechados '
                                'para la agricultura; son centros '
                                'demográficos.',
                                'Los cañones son depresiones estrechas y '
                                'profundas, con paredes verticales, que no '
                                'favorecen la actividad agrícola: Cañón del '
                                'Colca, Cañón del Apurímac.',
                                'Las quebradas son pequeñas depresiones '
                                'alargadas y angostas, recorridas por '
                                'arroyos y ríos tributarios.']},
                     {'titulo': 'RELIEVES PLANOS Y DEPOSICIONALES',
                      'items': ['Las llanuras son extensas superficies '
                                'planas poco accidentadas a poca altitud: '
                                'llanura del Amazonas.',
                                'Las mesetas son superficies planas a '
                                'grandes altitudes, entre 3000 y 4000 m, '
                                'limitadas por una depresión: Meseta de '
                                'Junín.',
                                'Los altiplanos son extensas superficies '
                                'rodeadas por cadenas de montañas: Altiplano '
                                'del Titicaca.',
                                'El cono aluvial o cono de deyección son '
                                'materiales depositados por corrientes '
                                'fluviales tras las precipitaciones; también '
                                'incluyen derrames volcánicos y morrenas.']}],
  'qr_reto': [{'pregunta': 'Las placas tectónicas en sentido convergente '
                           'originan bordes:',
               'respuesta': 'Destructivos'},
              {'pregunta': 'La geodinámica interna comprende movimientos '
                           'orogénicos, epirogénicos y:',
               'respuesta': 'Vulcanismo'},
              {'pregunta': 'El relieve terrestre se define como el conjunto '
                           'de:',
               'respuesta': 'Irregularidades o geoformas de la superficie'}],
  'qr_dato': 'El cono aluvial o cono de deyección son materiales depositados '
             'por corrientes fluviales tras las precipitaciones; también '
             'incluyen derrames volcánicos y morrenas.'},
 {'num': 6,
  'titulo': 'Espacio Geográfico Peruano: Región Andina',
  'secciones': [{'titulo': '6.1 LOCALIZACIÓN Y DIMENSIONES DEL PERÚ',
                 'items': ['El territorio peruano se ubica en la parte '
                           'occidental y central de Sudamérica, en la zona '
                           '{tórrida}, Hemisferio Austral.',
                           'La superficie del territorio peruano asciende a '
                           '{1 285 215,60} km², siendo el {tercer} país más '
                           'extenso de América del Sur.',
                           'El punto más alto del Perú es el nevado '
                           '{Huascarán}, a 6746 m de altitud.',
                           'El punto más bajo del Perú es la Depresión de '
                           '{Bayovar}, a -37 m, ubicada en Piura.',
                           'El largo del territorio peruano, de norte a sur, '
                           'es de {2 135} km.',
                           'La longitud del litoral peruano es de {3 080} '
                           'km, desde Boca de Capones hasta el hito La '
                           'Concordia.']},
                {'titulo': '6.2 DATOS EXTREMOS DEL PERÚ',
                 'items': ['El lugar más lluvioso del Perú es {Quince Mil}, '
                           'en la provincia de Quispicanchi, Cusco, con 8000 '
                           'mm.',
                           'El lugar más caluroso del Perú es {Neshuya}, en '
                           'Ucayali, con 41 °C.',
                           'El lugar más frío del Perú es {Imata}, en '
                           'Arequipa, con -25 °C.',
                           'La mayor fosa marina del Perú se ubica entre '
                           'Tacna y {Arica}, superando los 7000 metros bajo '
                           'el nivel del mar.']},
                {'titulo': '6.3 FRONTERAS Y LÍMITES',
                 'items': ['La frontera más extensa del Perú es con '
                           '{Brasil}, con 2822,5 km.',
                           'El perímetro total del Perú, incluyendo el '
                           'litoral, es de {10 156,8} km.',
                           'El Perú limita por el norte con {Ecuador} y '
                           'Colombia, por el sur con {Chile}, por el este '
                           'con Bolivia y Brasil, y por el oeste con el '
                           'océano {Pacífico}.',
                           'El punto extremo norte del Perú se ubica en el '
                           'talweg del río {Putumayo}, cerca de Güeppí, '
                           'Loreto.',
                           'El punto extremo sur del Perú se ubica en el '
                           'Hito N° 1 de la Concordia, en {Tacna}.']},
                {'titulo': '6.4 REGIONES NATURALES DEL ÁREA CONTINENTAL',
                 'items': ['La región {Costa} representa el 12,5% del área '
                           'continental del Perú.',
                           'La región {Andina} representa el 30,2% del área '
                           'continental del Perú.']},
                {'titulo': '6.5 SECTORES DE LOS ANDES PERUANOS',
                 'items': ['Los Andes Peruanos se dividen tradicionalmente '
                           'en {tres} sectores, separados por los nudos o '
                           'divisorias fluviales de {Pasco} y Vilcanota.',
                           'Los {Andes del Norte} presentan Cordillera '
                           'Occidental, Central y {Oriental}.',
                           'Los {Andes del Centro} presentan Cordillera '
                           'Occidental, Central y {Oriental}.',
                           'Los {Andes del Sur} presentan Cordillera '
                           'Occidental y {Oriental} (sin Central).',
                           'El {nudo de Pasco} separa los Andes del Norte de '
                           'los Andes del Centro; el {nudo de Vilcanota} '
                           'separa los Andes del Centro de los del Sur.']},
                {'titulo': '6.6 DATOS SUPERLATIVOS DE LA REGIÓN ANDINA',
                 'items': ['Los Andes constituyen la cordillera más {larga} '
                           'del mundo, con {7240} km.',
                           'La {Cordillera Blanca} es la cordillera más alta '
                           'de la zona tropical.',
                           'El nevado más alto de la zona tropical es el '
                           '{Huascarán}, con 6746 m.',
                           'El volcán más alto del Perú es el {Coropuna}, en '
                           'Arequipa, con 6426 m; el volcán más hermoso es '
                           'el {Misti}.',
                           'El cañón más profundo del mundo es el '
                           '{Cotahuasi}, en Arequipa, con 3535 m de '
                           'profundidad.',
                           'El pongo más largo es el de {Manseriche}; el '
                           'paso o abra más bajo es {Porculla}, en Piura.',
                           'El paso o abra más alto es {Anticona}; los '
                           'volcanes activos del Perú son el {Sabancaya} y '
                           'el Ubinas.']},
                {'titulo': '6.7 LOS GLACIARES: CONCEPTO Y PARTES',
                 'items': ['Los {glaciares} son masas de hielo que se forman '
                           'en las partes altas de las montañas y casquetes '
                           'polares, por acumulación, compactación y '
                           '{recristalización} de la nieve.',
                           'La {zona de acumulación} se ubica en la parte '
                           'alta del glaciar, donde la nieve se transforma '
                           'en {neviza} y luego en hielo.',
                           'La {zona de ablación} se ubica en la parte baja '
                           'del glaciar; es la zona donde el hielo se '
                           '{derrite}.',
                           'La {línea de equilibrio} separa la zona de '
                           'acumulación de la zona de ablación.',
                           'Los materiales transportados y depositados por '
                           'el glaciar (rocas, lodo) se llaman {morrenas}.']},
                {'titulo': '6.8 EL GLACIAR QELCCAYA Y RANKING DE GLACIARES',
                 'items': ['El glaciar {Qelccaya} se ubica en la cordillera '
                           'de Vilcanota, entre Canchis (Cusco) y Melgar '
                           '(Puno); es el glaciar más extenso de la zona '
                           '{tropical} del mundo.',
                           'El glaciar Qelccaya tiene 18 km de largo, 2,5 km '
                           'de ancho, una superficie de {44} km² y una capa '
                           'de hielo de más de 200 m de espesor.',
                           'Las cordilleras con mayor superficie glaciar del '
                           'Perú son: {Blanca} (448 km²), Vilcanota (255 '
                           'km²), Vilcabamba (101 km²), Huayhuash (53 km²) y '
                           '{Ampato} (50 km²).',
                           'Entre las importancias de los glaciares están '
                           'constituir reservas de {agua dulce} y mantener '
                           'el balance hídrico de las cuencas.']}],
  'cuadros': [{'titulo': '6.3 FRONTERAS DEL PERÚ',
               'encabezados': ['País', 'Longitud'],
               'filas': [['{Ecuador}', '1528,5 km'],
                         ['Colombia', '1506,0 km'],
                         ['{Brasil}', '2822,5 km'],
                         ['Bolivia', '1047,1 km'],
                         ['{Chile}', '169,1 km']]}],
  'preguntas': [{'pregunta': 'El territorio peruano se ubica en la zona:',
                 'alternativas': ['Glacial',
                                  'Subtropical',
                                  'Tórrida',
                                  'Templada',
                                  'Polar'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú es considerado el país de América del '
                             'Sur con extensión:',
                 'alternativas': ['La mayor',
                                  'La segunda menor',
                                  'La menor',
                                  'La tercera mayor',
                                  'La cuarta mayor'],
                 'correcta': 'D'},
                {'pregunta': 'El punto más alto del Perú es el nevado:',
                 'alternativas': ['Ausangate',
                                  'Huascarán',
                                  'Coropuna',
                                  'Salkantay',
                                  'Alpamayo'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más bajo del territorio peruano es:',
                 'alternativas': ['La fosa de Tacna',
                                  'El desierto de Sechura',
                                  'La Depresión de Bayovar',
                                  'El valle del Colca',
                                  'El lago Titicaca'],
                 'correcta': 'C'},
                {'pregunta': 'El lugar más lluvioso del Perú es:',
                 'alternativas': ['Tarapoto',
                                  'Quince Mil',
                                  'Iquitos',
                                  'Moyobamba',
                                  'Chachapoyas'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más caluroso del Perú es:',
                 'alternativas': ['Jaén',
                                  'Neshuya',
                                  'Sechura',
                                  'Tumbes',
                                  'Piura'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más frío del Perú es:',
                 'alternativas': ['Imata',
                                  'Juliaca',
                                  'El Misti',
                                  'Puno',
                                  'Cusco'],
                 'correcta': 'A'},
                {'pregunta': 'La frontera más extensa del Perú es con:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Colombia',
                                  'Ecuador',
                                  'Brasil'],
                 'correcta': 'E'},
                {'pregunta': 'La frontera más corta del Perú es con:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Brasil',
                                  'Ecuador',
                                  'Colombia'],
                 'correcta': 'A'},
                {'pregunta': 'El perímetro total del Perú, incluido el '
                             'litoral, es aproximadamente de:',
                 'alternativas': ['15 000 km',
                                  '1 000 km',
                                  '5 000 km',
                                  '20 000 km',
                                  '10 156,8 km'],
                 'correcta': 'E'},
                {'pregunta': 'Por el sur, el Perú limita con:',
                 'alternativas': ['Chile',
                                  'Ecuador',
                                  'Brasil',
                                  'Colombia',
                                  'Bolivia'],
                 'correcta': 'A'},
                {'pregunta': 'Por el este, el Perú limita con:',
                 'alternativas': ['Bolivia y Brasil',
                                  'Solo Brasil',
                                  'Chile y Bolivia',
                                  'Solo Bolivia',
                                  'Ecuador y Colombia'],
                 'correcta': 'A'},
                {'pregunta': 'El punto extremo norte del Perú se relaciona '
                             'con el río:',
                 'alternativas': ['Marañón',
                                  'Amazonas',
                                  'Madre de Dios',
                                  'Putumayo',
                                  'Ucayali'],
                 'correcta': 'D'},
                {'pregunta': 'El punto extremo sur del Perú se ubica en:',
                 'alternativas': ['Arequipa',
                                  'Tacna',
                                  'Moquegua',
                                  'Ica',
                                  'Puno'],
                 'correcta': 'B'},
                {'pregunta': 'El punto extremo este del Perú limita con:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Brasil únicamente',
                                  'Ecuador',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'La región Costa representa del área '
                             'continental peruana:',
                 'alternativas': ['12,5%', '50%', '5%', '30,2%', '20%'],
                 'correcta': 'A'},
                {'pregunta': 'La región Andina representa del área '
                             'continental peruana:',
                 'alternativas': ['12,5%', '30,2%', '45%', '10%', '60%'],
                 'correcta': 'B'},
                {'pregunta': 'El litoral peruano se extiende desde Boca de '
                             'Capones hasta:',
                 'alternativas': ['Ilo',
                                  'El hito La Concordia',
                                  'Paracas',
                                  'Tumbes',
                                  'Tacna'],
                 'correcta': 'B'},
                {'pregunta': 'La longitud del litoral peruano es '
                             'aproximadamente de:',
                 'alternativas': ['10 000 km',
                                  '1 000 km',
                                  '500 km',
                                  '3 080 km',
                                  '5 000 km'],
                 'correcta': 'D'},
                {'pregunta': 'El ancho del territorio peruano, de este a '
                             'oeste, es de aproximadamente:',
                 'alternativas': ['3 000 km',
                                  '2 135 km',
                                  '800 km',
                                  '500 km',
                                  '1 640 km'],
                 'correcta': 'E'},
                {'pregunta': 'Son características morfológicas de la región '
                             'andina: (I CEPRU 2024)',
                 'alternativas': ['Pampas, manantes y valles transversales',
                                  'Mesetas, ríos y picos',
                                  'Andenes, quebradas y lagos',
                                  'Valles interandinos, mesetas y altiplanos',
                                  'Altiplanos, desiertos y acantilados'],
                 'correcta': 'D'},
                {'pregunta': 'El piso altitudinal que se desarrolla por '
                             'encima de los 4600 m.s.n.m., con temperatura '
                             'media anual menor a 3°C, es: (II CEPRU 2022)',
                 'alternativas': ['Qheswa',
                                  'Puna alta',
                                  'Yunka',
                                  "Rit'i",
                                  'Puna baja'],
                 'correcta': 'D'},
                {'pregunta': 'Es una característica de la vertiente o '
                             'llamada oriental de la Región Andina: (Primera '
                             'Oportunidad UNSAAC 2024)',
                 'alternativas': ['Árido',
                                  'Abundante vegetación',
                                  'Ríos de corto recorrido',
                                  'Escasa precipitación',
                                  'Escasa vegetación'],
                 'correcta': 'B'},
                {'pregunta': 'La ciudad de Yauri, ubicada a 3915 m.s.n.m., '
                             'pertenece al piso climático: (Primera '
                             'Oportunidad UNSAAC 2021)',
                 'alternativas': ['Puna alta',
                                  'Qheswa baja',
                                  'Puna baja',
                                  'Qheswa alta',
                                  'Transición'],
                 'correcta': 'C'},
                {'pregunta': 'Los Andes Peruanos se dividen tradicionalmente '
                             'en un número de sectores igual a:',
                 'alternativas': ['Dos', 'Seis', 'Cinco', 'Tres', 'Cuatro'],
                 'correcta': 'D'},
                {'pregunta': 'Los sectores de los Andes Peruanos están '
                             'separados por los nudos o divisorias fluviales '
                             'de Vilcanota y:',
                 'alternativas': ['Anticona',
                                  'Porculla',
                                  'Pasco',
                                  'Huaytapallana',
                                  'Apurímac'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia de los Andes del Norte y del '
                             'Centro, los Andes del Sur presentan únicamente '
                             'Cordillera Occidental y:',
                 'alternativas': ['Central',
                                  'Marginal',
                                  'Interior',
                                  'Costera',
                                  'Oriental'],
                 'correcta': 'E'},
                {'pregunta': 'Los Andes constituyen la cordillera más larga '
                             'del mundo, con una longitud aproximada de:',
                 'alternativas': ['6500 km',
                                  '5000 km',
                                  '3000 km',
                                  '9000 km',
                                  '7240 km'],
                 'correcta': 'E'},
                {'pregunta': 'La cordillera más alta de la zona tropical es '
                             'la:',
                 'alternativas': ['Vilcanota',
                                  'Huayhuash',
                                  'Vilcabamba',
                                  'Carabaya',
                                  'Blanca'],
                 'correcta': 'E'},
                {'pregunta': 'El nevado más alto de la zona tropical del '
                             'mundo es el:',
                 'alternativas': ['Salkantay',
                                  'Ampato',
                                  'Huascarán',
                                  'Misti',
                                  'Coropuna'],
                 'correcta': 'C'},
                {'pregunta': 'El volcán más alto del Perú, ubicado en '
                             'Arequipa, es el:',
                 'alternativas': ['Misti',
                                  'Ubinas',
                                  'Coropuna',
                                  'Sabancaya',
                                  'Ampato'],
                 'correcta': 'C'},
                {'pregunta': 'El cañón más profundo del mundo, ubicado en '
                             'Arequipa, es el:',
                 'alternativas': ['Pato',
                                  'Machupicchu',
                                  'Colca',
                                  'Apurímac',
                                  'Cotahuasi'],
                 'correcta': 'E'},
                {'pregunta': 'El pongo más largo del Perú es el de:',
                 'alternativas': ['Manseriche',
                                  'Aguirre',
                                  'Mainique',
                                  'Boquerón del Padre Abad',
                                  'Retama'],
                 'correcta': 'A'},
                {'pregunta': 'El paso o abra más bajo del Perú, ubicado en '
                             'Piura, es:',
                 'alternativas': ['Crucero Alto',
                                  'Ticlio',
                                  'Porculla',
                                  'Anticona',
                                  'La Raya'],
                 'correcta': 'C'},
                {'pregunta': 'Las masas de hielo que se forman en las partes '
                             'altas de las montañas por acumulación y '
                             'recristalización de la nieve se llaman:',
                 'alternativas': ['Casquetes',
                                  'Glaciares',
                                  'Nevados',
                                  'Neviza',
                                  'Morrenas'],
                 'correcta': 'B'},
                {'pregunta': 'La parte de un glaciar ubicada en la zona '
                             'alta, donde la nieve se transforma en neviza y '
                             'luego en hielo, se llama zona de:',
                 'alternativas': ['Acumulación',
                                  'Ablación',
                                  'Fusión',
                                  'Compactación',
                                  'Equilibrio'],
                 'correcta': 'A'},
                {'pregunta': 'La parte de un glaciar ubicada en la zona '
                             'baja, donde el hielo se derrite, se llama zona '
                             'de:',
                 'alternativas': ['Neviza',
                                  'Equilibrio',
                                  'Acumulación',
                                  'Ablación',
                                  'Compactación'],
                 'correcta': 'D'},
                {'pregunta': 'La línea que separa la zona de acumulación de '
                             'la zona de ablación de un glaciar se llama '
                             'línea de:',
                 'alternativas': ['Nieve',
                                  'Compactación',
                                  'Equilibrio',
                                  'Deshielo',
                                  'Fusión'],
                 'correcta': 'C'},
                {'pregunta': 'Los materiales transportados y depositados por '
                             'un glaciar (rocas, lodo) se llaman:',
                 'alternativas': ['Aluviones',
                                  'Neviza',
                                  'Conos',
                                  'Morrenas',
                                  'Sedimentos fluviales'],
                 'correcta': 'D'},
                {'pregunta': 'El glaciar más extenso de toda la zona '
                             'tropical del mundo, ubicado entre Cusco y '
                             'Puno, es el:',
                 'alternativas': ['Coropuna',
                                  'Salkantay',
                                  'Ausangate',
                                  'Ampay',
                                  'Qelccaya'],
                 'correcta': 'E'},
                {'pregunta': 'La cordillera con mayor superficie glaciar del '
                             'Perú es la:',
                 'alternativas': ['Vilcabamba',
                                  'Blanca',
                                  'Ampato',
                                  'Vilcanota',
                                  'Huayhuash'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'LOCALIZACIÓN Y DIMENSIONES DEL PERÚ',
                      'items': ['El territorio peruano se ubica en la parte '
                                'occidental y central de Sudamérica, en la '
                                'zona tórrida, Hemisferio Austral.',
                                'La superficie del territorio peruano '
                                'asciende a 1 285 215,60 km², siendo el '
                                'tercer país más extenso de América del Sur.',
                                'El punto más alto del Perú es el nevado '
                                'Huascarán, a 6746 m de altitud.',
                                'El punto más bajo del Perú es la Depresión '
                                'de Bayovar, a -37 m, ubicada en Piura.',
                                'El largo del territorio peruano, de norte a '
                                'sur, es de 2 135 km.',
                                'La longitud del litoral peruano es de 3 080 '
                                'km, desde Boca de Capones hasta el hito La '
                                'Concordia.']},
                     {'titulo': 'DATOS EXTREMOS DEL PERÚ',
                      'items': ['El lugar más lluvioso del Perú es Quince '
                                'Mil, en la provincia de Quispicanchi, '
                                'Cusco, con 8000 mm.',
                                'El lugar más caluroso del Perú es Neshuya, '
                                'en Ucayali, con 41 °C.',
                                'El lugar más frío del Perú es Imata, en '
                                'Arequipa, con -25 °C.',
                                'La mayor fosa marina del Perú se ubica '
                                'entre Tacna y Arica, superando los 7000 '
                                'metros bajo el nivel del mar.']},
                     {'titulo': 'FRONTERAS Y LÍMITES',
                      'items': ['La frontera más extensa del Perú es con '
                                'Brasil, con 2822,5 km.',
                                'El perímetro total del Perú, incluyendo el '
                                'litoral, es de 10 156,8 km.',
                                'El Perú limita por el norte con Ecuador y '
                                'Colombia, por el sur con Chile, por el este '
                                'con Bolivia y Brasil, y por el oeste con el '
                                'océano Pacífico.',
                                'El punto extremo norte del Perú se ubica en '
                                'el talweg del río Putumayo, cerca de '
                                'Güeppí, Loreto.',
                                'El punto extremo sur del Perú se ubica en '
                                'el Hito N° 1 de la Concordia, en Tacna.']},
                     {'titulo': 'REGIONES NATURALES DEL ÁREA CONTINENTAL',
                      'items': ['La región Costa representa el 12,5% del '
                                'área continental del Perú.',
                                'La región Andina representa el 30,2% del '
                                'área continental del Perú.']},
                     {'titulo': 'SECTORES DE LOS ANDES PERUANOS',
                      'items': ['Los Andes Peruanos se dividen '
                                'tradicionalmente en tres sectores, '
                                'separados por los nudos o divisorias '
                                'fluviales de Pasco y Vilcanota.',
                                'Los Andes del Norte presentan Cordillera '
                                'Occidental, Central y Oriental.',
                                'Los Andes del Centro presentan Cordillera '
                                'Occidental, Central y Oriental.',
                                'Los Andes del Sur presentan Cordillera '
                                'Occidental y Oriental (sin Central).',
                                'El nudo de Pasco separa los Andes del Norte '
                                'de los Andes del Centro; el nudo de '
                                'Vilcanota separa los Andes del Centro de '
                                'los del Sur.']},
                     {'titulo': 'DATOS SUPERLATIVOS DE LA REGIÓN ANDINA',
                      'items': ['Los Andes constituyen la cordillera más '
                                'larga del mundo, con 7240 km.',
                                'La Cordillera Blanca es la cordillera más '
                                'alta de la zona tropical.',
                                'El nevado más alto de la zona tropical es '
                                'el Huascarán, con 6746 m.',
                                'El volcán más alto del Perú es el Coropuna, '
                                'en Arequipa, con 6426 m; el volcán más '
                                'hermoso es el Misti.',
                                'El cañón más profundo del mundo es el '
                                'Cotahuasi, en Arequipa, con 3535 m de '
                                'profundidad.',
                                'El pongo más largo es el de Manseriche; el '
                                'paso o abra más bajo es Porculla, en '
                                'Piura.']},
                     {'titulo': 'LOS GLACIARES: CONCEPTO Y PARTES',
                      'items': ['Los glaciares son masas de hielo que se '
                                'forman en las partes altas de las montañas '
                                'y casquetes polares, por acumulación, '
                                'compactación y recristalización de la '
                                'nieve.',
                                'La zona de acumulación se ubica en la parte '
                                'alta del glaciar, donde la nieve se '
                                'transforma en neviza y luego en hielo.',
                                'La zona de ablación se ubica en la parte '
                                'baja del glaciar; es la zona donde el hielo '
                                'se derrite.',
                                'La línea de equilibrio separa la zona de '
                                'acumulación de la zona de ablación.',
                                'Los materiales transportados y depositados '
                                'por el glaciar (rocas, lodo) se llaman '
                                'morrenas.']},
                     {'titulo': 'EL GLACIAR QELCCAYA Y RANKING DE GLACIARES',
                      'items': ['El glaciar Qelccaya se ubica en la '
                                'cordillera de Vilcanota, entre Canchis '
                                '(Cusco) y Melgar (Puno); es el glaciar más '
                                'extenso de la zona tropical del mundo.',
                                'El glaciar Qelccaya tiene 18 km de largo, '
                                '2,5 km de ancho, una superficie de 44 km² y '
                                'una capa de hielo de más de 200 m de '
                                'espesor.',
                                'Las cordilleras con mayor superficie '
                                'glaciar del Perú son: Blanca (448 km²), '
                                'Vilcanota (255 km²), Vilcabamba (101 km²), '
                                'Huayhuash (53 km²) y Ampato (50 km²).',
                                'Entre las importancias de los glaciares '
                                'están constituir reservas de agua dulce y '
                                'mantener el balance hídrico de las '
                                'cuencas.']}],
  'qr_reto': [{'pregunta': 'El punto extremo este del Perú limita con:',
               'respuesta': 'Bolivia'},
              {'pregunta': 'La longitud del litoral peruano es '
                           'aproximadamente de:',
               'respuesta': '3 080 km'},
              {'pregunta': 'El territorio peruano se ubica en la zona:',
               'respuesta': 'Tórrida'}],
  'qr_dato': 'La longitud del litoral peruano es de 3 080 km, desde Boca de '
             'Capones hasta el hito La Concordia.'},
 {'num': 7,
  'titulo': 'Espacio Geográfico Peruano: Región Amazónica y Costa',
  'secciones': [{'titulo': '7.1 LA REGIÓN AMAZÓNICA',
                 'items': ['La región amazónica o selva es la región '
                           'geográfica más {extensa} del Perú, representando '
                           'el {57,3}% del territorio nacional.',
                           'La selva se caracteriza por un relieve plano, '
                           'clima cálido y húmedo, ubicada por debajo de los '
                           '{1000} m de altitud.',
                           'La región amazónica comprende dos subregiones: '
                           'la selva {alta} y la selva {baja}.']},
                {'titulo': '7.2 LA SELVA ALTA O RUPA RUPA',
                 'items': ['La selva alta, llamada también {Rupa Rupa} o '
                           'Ceja de Selva, es una faja angosta entre la '
                           'región andina y la llanura amazónica.',
                           'El relieve de la selva alta está afectado por la '
                           '{Tectónica} Andina, con pongos, valles y '
                           'cañones.',
                           'Los {pongos} son cortes fluviales donde los ríos '
                           'han erosionado profundamente una cadena de '
                           'montañas.',
                           'El Pongo de {Mainique} fue formado por el río '
                           'Urubamba, en el Cusco.',
                           'El Pongo de {Manseriche} fue formado por el río '
                           'Marañón, en Amazonas.']},
                {'titulo': '7.3 LA SELVA BAJA U OMAGUA',
                 'items': ['La selva baja, llamada también {Omagua} o '
                           'Llanura Amazónica, ocupa parte del antiguo '
                           'Cratón {Brasileño} y no es afectada por la '
                           'tectónica andina.',
                           "Las {qochas}, llamadas también t'ipisqas, son "
                           'lagos abandonados por ríos que cambiaron de '
                           'cauce.',
                           'Las {tahuampas} o aguajales son áreas bajas '
                           'cubiertas de agua todo el año, formadas por '
                           'palmeras de aguaje.',
                           'Las {restingas} son áreas altas que solo se '
                           'inundan en las crecidas de los ríos.',
                           'Los {altos} son áreas de colinas o terrazas no '
                           'inundables, donde se han edificado las ciudades '
                           'y se practica la ganadería.']},
                {'titulo': '7.4 LA REGIÓN COSTA',
                 'items': ['La región Costa es un espacio desértico y '
                           'estrecho, ubicado desde el nivel del mar hasta '
                           '{1000} m de altitud, y representa el {12,5}% del '
                           'territorio nacional.',
                           'La Costa Sur o {Meridional} se extiende entre la '
                           'frontera con Chile y la península de Paracas.',
                           'En la costa sur destaca la «Cadena {Costanera}», '
                           'con hasta 1200 m de altitud en el cerro '
                           'Criterión, Ica.',
                           'Entre la cadena costanera y las vertientes '
                           'andinas se desarrolla la plataforma costanera '
                           'desértica, con planicies llamadas {pampas}.']},
                {'titulo': '7.5 FORMAS DE RELIEVE DE LA COSTA',
                 'items': ['Las {estribaciones andinas} son pequeñas cadenas '
                           'de montañas desprendidas de la Cordillera '
                           'Occidental; algunas forman {acantilados} al '
                           'llegar al mar.',
                           'La {Cordillera Costanera} es una cadena '
                           'montañosa de hasta 1000 m de altitud que se '
                           'extiende de forma discontinua a lo largo de la '
                           '{costa}; sus testimonios actuales son las islas.',
                           'Los {valles} de la costa son transversales y '
                           'jóvenes, formados por ríos que descienden de la '
                           'Cordillera Occidental: Piura y Chira (Piura), '
                           'Rímac y Chillón (Lima).',
                           'Las {pampas} son áreas interfluviales entre los '
                           'valles, formadas por depósitos aluviales; tienen '
                           'suelos excelentes para la {agricultura}: Pampa '
                           'de Olmos, Cañete.',
                           'Los {desiertos} son áreas de gran extensión '
                           'cubiertas de arena, con ausencia de vegetación y '
                           'precipitaciones: {Sechura} en Piura, Ica en '
                           'Ica.']},
                {'titulo': '7.6 EL LITORAL PERUANO',
                 'items': ['El {litoral} es la faja longitudinal o zona de '
                           'contacto entre el mar y la costa, entre el nivel '
                           'de {pleamar} y bajamar.',
                           'Las {penínsulas} son porciones de tierra que '
                           'ingresan al mar, unidas al continente por un '
                           '{istmo}: Paracas (Ica), Illescas (Piura).',
                           'Las {puntas} son porciones de tierra estrechas '
                           'que ingresan al mar: La Punta en el {Callao}, '
                           'Lobos en Arequipa.',
                           'Los {cabos} son porciones de tierra abultadas o '
                           'redondeadas que avanzan hacia el mar: Cabo '
                           '{Blanco} en Piura.',
                           'Las {bahías} son entrantes de mar en el '
                           'continente: Paita (Piura), Chimbote (Áncash), '
                           '{Paracas} (Ica).',
                           'Las {islas} son porciones de tierra en medio del '
                           'mar; albergan aves guaneras: San Lorenzo, '
                           'Ballestas, {Pachacámac}.']}],
  'cuadros': [{'titulo': '7.2 PONGOS DE LA SELVA ALTA',
               'encabezados': ['Pongo', 'Río', 'Departamento'],
               'filas': [['{Manseriche}', 'Marañón', '{Amazonas}'],
                         ['{Mainique}', 'Urubamba', '{Cusco}'],
                         ['{Aguirre}', 'Huallaga', 'San Martín'],
                         ['Del {Tambo}', 'Tambo', 'Junín']]}],
  'preguntas': [{'pregunta': 'La región geográfica más extensa del Perú es:',
                 'alternativas': ['La Amazónica o Selva',
                                  'El litoral',
                                  'La Andina',
                                  'Ninguna en particular',
                                  'La Costa'],
                 'correcta': 'A'},
                {'pregunta': 'La región amazónica representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['10%', '12,5%', '57,3%', '90%', '30,2%'],
                 'correcta': 'C'},
                {'pregunta': 'La selva alta también se conoce como:',
                 'alternativas': ['Omagua',
                                  'Rupa Rupa o Ceja de Selva',
                                  'Llanura Amazónica',
                                  'Cratón Brasileño',
                                  'Selva Baja'],
                 'correcta': 'B'},
                {'pregunta': 'El relieve de la selva alta está afectado por:',
                 'alternativas': ['El clima ecuatorial',
                                  'Solo la erosión eólica',
                                  'El Cratón Brasileño',
                                  'La Tectónica Andina',
                                  'La sedimentación marina'],
                 'correcta': 'D'},
                {'pregunta': 'Los cortes fluviales donde un río corta una '
                             'cadena de montañas se llaman:',
                 'alternativas': ['Restingas',
                                  'Tahuampas',
                                  'Altos',
                                  'Qochas',
                                  'Pongos'],
                 'correcta': 'E'},
                {'pregunta': 'El Pongo de Mainique fue formado por el río:',
                 'alternativas': ['Inambari',
                                  'Tambo',
                                  'Urubamba',
                                  'Huallaga',
                                  'Marañón'],
                 'correcta': 'C'},
                {'pregunta': 'La selva baja también se llama:',
                 'alternativas': ['Cordillera Oriental',
                                  'Omagua o Llanura Amazónica',
                                  'Faja Sub Andina',
                                  'Ceja de Selva',
                                  'Rupa Rupa'],
                 'correcta': 'B'},
                {'pregunta': 'La selva baja no es afectada por la tectónica '
                             'andina porque se asienta sobre:',
                 'alternativas': ['Los Andes centrales',
                                  'La Cordillera Oriental',
                                  'El antiguo Cratón Brasileño',
                                  'La cadena costanera',
                                  'La plataforma costanera'],
                 'correcta': 'C'},
                {'pregunta': 'Los lagos abandonados por los ríos que '
                             'cambiaron de cauce se llaman:',
                 'alternativas': ['Filos',
                                  'Restingas',
                                  'Altos',
                                  'Tahuampas',
                                  'Qochas'],
                 'correcta': 'E'},
                {'pregunta': 'Las áreas bajas cubiertas de agua todo el año, '
                             'con palmeras de aguaje, se llaman:',
                 'alternativas': ['Filos',
                                  'Restingas',
                                  'Qochas',
                                  'Altos',
                                  'Tahuampas o aguajales'],
                 'correcta': 'E'},
                {'pregunta': 'Las áreas que solo se inundan en las crecidas '
                             'de los ríos se llaman:',
                 'alternativas': ['Altos',
                                  'Qochas',
                                  'Filos',
                                  'Restingas',
                                  'Tahuampas'],
                 'correcta': 'D'},
                {'pregunta': 'Las ciudades de la selva baja se han edificado '
                             'principalmente en:',
                 'alternativas': ['Las qochas',
                                  'Las tahuampas',
                                  'Las restingas',
                                  'Los filos',
                                  'Los altos'],
                 'correcta': 'E'},
                {'pregunta': 'La región Costa representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['57,3%', '30,2%', '12,5%', '5%', '70%'],
                 'correcta': 'C'},
                {'pregunta': 'La región Costa se extiende desde el nivel del '
                             'mar hasta una altitud de:',
                 'alternativas': ['2000 m',
                                  '1000 m',
                                  '300 m',
                                  '1500 m',
                                  '500 m'],
                 'correcta': 'B'},
                {'pregunta': 'La Costa Sur o Meridional se extiende entre la '
                             'frontera con Chile y:',
                 'alternativas': ['Tumbes',
                                  'Trujillo',
                                  'Lima',
                                  'La península de Paracas',
                                  'Chiclayo'],
                 'correcta': 'D'},
                {'pregunta': 'La Cadena Costanera alcanza su mayor altitud '
                             'en:',
                 'alternativas': ['El cerro Criterión, Ica',
                                  'Piura',
                                  'Lima',
                                  'Arequipa',
                                  'Tacna'],
                 'correcta': 'A'},
                {'pregunta': 'Las planicies de origen aluvial en la costa '
                             'sur se llaman:',
                 'alternativas': ['Tahuampas',
                                  'Restingas',
                                  'Tablazos',
                                  'Pampas',
                                  'Aguajales'],
                 'correcta': 'D'},
                {'pregunta': 'Los valles de Jaén y Bagua se ubican en la '
                             'subregión de:',
                 'alternativas': ['Selva baja',
                                  'Selva alta',
                                  'Costa norte',
                                  'Costa sur',
                                  'Sierra central'],
                 'correcta': 'B'},
                {'pregunta': 'El valle de Chanchamayo pertenece al '
                             'departamento de:',
                 'alternativas': ['San Martín',
                                  'Cusco',
                                  'Puno',
                                  'Junín',
                                  'Huánuco'],
                 'correcta': 'D'},
                {'pregunta': 'El Boquerón del Padre Abad fue formado por el '
                             'río:',
                 'alternativas': ['Tambo',
                                  'Marañón',
                                  'Urubamba',
                                  'Huallaga',
                                  'Yuracyacu'],
                 'correcta': 'E'},
                {'pregunta': 'El desierto de Sechura se localiza en el '
                             'departamento de: (II CEPRU 2025)',
                 'alternativas': ['Lambayeque',
                                  'Moquegua',
                                  'Piura',
                                  'Ica',
                                  'Áncash'],
                 'correcta': 'C'},
                {'pregunta': 'Los bosques de algarrobos y vegetación de '
                             'monte ribereño pertenecen a la: (II CEPRU '
                             '2024)',
                 'alternativas': ['Sierra sur',
                                  'Selva norte',
                                  'Costa sur',
                                  'Costa central',
                                  'Costa norte'],
                 'correcta': 'E'},
                {'pregunta': 'En la costa peruana, los espacios o áreas '
                             'interfluviales emplazadas entre los valles se '
                             'llaman: (II CEPRU 2022)',
                 'alternativas': ['Pampas',
                                  'Tablazos',
                                  'Lomas',
                                  'Desiertos',
                                  'Depresiones'],
                 'correcta': 'A'},
                {'pregunta': 'Los valles de Tocache y Chanchamayo se '
                             'encuentran, respectivamente, en los '
                             'departamentos de: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['San Martín - Junín',
                                  'Puno - Ucayali',
                                  'Amazonas - La Libertad',
                                  'Loreto - Pasco',
                                  'Junín - Cajamarca'],
                 'correcta': 'A'},
                {'pregunta': 'La depresión más importante de la costa '
                             'peruana es: (Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Otuma',
                                  'Pariñas',
                                  'Chilca',
                                  'Bayóvar',
                                  'Chivay'],
                 'correcta': 'D'},
                {'pregunta': 'Las pequeñas cadenas de montañas desprendidas '
                             'de la Cordillera Occidental, que algunas veces '
                             'forman acantilados al llegar al mar, se '
                             'llaman:',
                 'alternativas': ['Cabos',
                                  'Pampas costeras',
                                  'Estribaciones andinas',
                                  'Cordillera Costanera',
                                  'Valles transversales'],
                 'correcta': 'C'},
                {'pregunta': 'La cadena montañosa de hasta 1000 m de altitud '
                             'que se extiende de forma discontinua a lo '
                             'largo de la costa peruana se llama:',
                 'alternativas': ['Cordillera Occidental',
                                  'Meseta costera',
                                  'Cordillera Costanera',
                                  'Estribaciones andinas',
                                  'Cadena litoral'],
                 'correcta': 'C'},
                {'pregunta': 'Los valles de la costa peruana se caracterizan '
                             'por ser transversales y:',
                 'alternativas': ['Endorreicos',
                                  'Antiguos',
                                  'Jóvenes',
                                  'Glaciares',
                                  'Longitudinales'],
                 'correcta': 'C'},
                {'pregunta': 'Las áreas interfluviales entre los valles de '
                             'la costa, con suelos excelentes para la '
                             'agricultura, se llaman:',
                 'alternativas': ['Pampas',
                                  'Tablazos',
                                  'Desiertos',
                                  'Cabos',
                                  'Estribaciones'],
                 'correcta': 'A'},
                {'pregunta': 'El desierto de Sechura se localiza en el '
                             'departamento de:',
                 'alternativas': ['Lambayeque',
                                  'Moquegua',
                                  'Áncash',
                                  'Piura',
                                  'Ica'],
                 'correcta': 'D'},
                {'pregunta': 'La faja longitudinal o zona de contacto entre '
                             'el mar y la costa, entre el nivel de pleamar y '
                             'bajamar, se llama:',
                 'alternativas': ['Litoral',
                                  'Plataforma continental',
                                  'Estuario',
                                  'Zócalo continental',
                                  'Delta'],
                 'correcta': 'A'},
                {'pregunta': 'Las porciones de tierra que ingresan al mar y '
                             'se unen al continente por un istmo se llaman:',
                 'alternativas': ['Penínsulas',
                                  'Puntas',
                                  'Cabos',
                                  'Islas',
                                  'Bahías'],
                 'correcta': 'A'},
                {'pregunta': 'Las porciones de tierra estrechas que ingresan '
                             'al mar, como La Punta en el Callao, se llaman:',
                 'alternativas': ['Cabos',
                                  'Golfos',
                                  'Puntas',
                                  'Bahías',
                                  'Penínsulas'],
                 'correcta': 'C'},
                {'pregunta': 'Las porciones de tierra abultadas o '
                             'redondeadas que avanzan hacia el mar, como el '
                             'Cabo Blanco en Piura, se llaman:',
                 'alternativas': ['Islas',
                                  'Puntas',
                                  'Penínsulas',
                                  'Bahías',
                                  'Cabos'],
                 'correcta': 'E'},
                {'pregunta': 'Los entrantes de mar en el continente, como '
                             'Paracas en Ica, se llaman:',
                 'alternativas': ['Puntas',
                                  'Cabos',
                                  'Estrechos',
                                  'Bahías',
                                  'Penínsulas'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'LA REGIÓN AMAZÓNICA',
                      'items': ['La región amazónica o selva es la región '
                                'geográfica más extensa del Perú, '
                                'representando el 57,3% del territorio '
                                'nacional.',
                                'La selva se caracteriza por un relieve '
                                'plano, clima cálido y húmedo, ubicada por '
                                'debajo de los 1000 m de altitud.',
                                'La región amazónica comprende dos '
                                'subregiones: la selva alta y la selva '
                                'baja.']},
                     {'titulo': 'LA SELVA ALTA O RUPA RUPA',
                      'items': ['La selva alta, llamada también Rupa Rupa o '
                                'Ceja de Selva, es una faja angosta entre la '
                                'región andina y la llanura amazónica.',
                                'El relieve de la selva alta está afectado '
                                'por la Tectónica Andina, con pongos, valles '
                                'y cañones.',
                                'Los pongos son cortes fluviales donde los '
                                'ríos han erosionado profundamente una '
                                'cadena de montañas.',
                                'El Pongo de Mainique fue formado por el río '
                                'Urubamba, en el Cusco.',
                                'El Pongo de Manseriche fue formado por el '
                                'río Marañón, en Amazonas.']},
                     {'titulo': 'LA SELVA BAJA U OMAGUA',
                      'items': ['La selva baja, llamada también Omagua o '
                                'Llanura Amazónica, ocupa parte del antiguo '
                                'Cratón Brasileño y no es afectada por la '
                                'tectónica andina.',
                                "Las qochas, llamadas también t'ipisqas, son "
                                'lagos abandonados por ríos que cambiaron de '
                                'cauce.',
                                'Las tahuampas o aguajales son áreas bajas '
                                'cubiertas de agua todo el año, formadas por '
                                'palmeras de aguaje.',
                                'Las restingas son áreas altas que solo se '
                                'inundan en las crecidas de los ríos.',
                                'Los altos son áreas de colinas o terrazas '
                                'no inundables, donde se han edificado las '
                                'ciudades y se practica la ganadería.']},
                     {'titulo': 'LA REGIÓN COSTA',
                      'items': ['La región Costa es un espacio desértico y '
                                'estrecho, ubicado desde el nivel del mar '
                                'hasta 1000 m de altitud, y representa el '
                                '12,5% del territorio nacional.',
                                'La Costa Sur o Meridional se extiende entre '
                                'la frontera con Chile y la península de '
                                'Paracas.',
                                'En la costa sur destaca la «Cadena '
                                'Costanera», con hasta 1200 m de altitud en '
                                'el cerro Criterión, Ica.',
                                'Entre la cadena costanera y las vertientes '
                                'andinas se desarrolla la plataforma '
                                'costanera desértica, con planicies llamadas '
                                'pampas.']},
                     {'titulo': 'FORMAS DE RELIEVE DE LA COSTA',
                      'items': ['Las estribaciones andinas son pequeñas '
                                'cadenas de montañas desprendidas de la '
                                'Cordillera Occidental; algunas forman '
                                'acantilados al llegar al mar.',
                                'La Cordillera Costanera es una cadena '
                                'montañosa de hasta 1000 m de altitud que se '
                                'extiende de forma discontinua a lo largo de '
                                'la costa; sus testimonios actuales son las '
                                'islas.',
                                'Los valles de la costa son transversales y '
                                'jóvenes, formados por ríos que descienden '
                                'de la Cordillera Occidental: Piura y Chira '
                                '(Piura), Rímac y Chillón (Lima).',
                                'Las pampas son áreas interfluviales entre '
                                'los valles, formadas por depósitos '
                                'aluviales; tienen suelos excelentes para la '
                                'agricultura: Pampa de Olmos, Cañete.',
                                'Los desiertos son áreas de gran extensión '
                                'cubiertas de arena, con ausencia de '
                                'vegetación y precipitaciones: Sechura en '
                                'Piura, Ica en Ica.']},
                     {'titulo': 'EL LITORAL PERUANO',
                      'items': ['El litoral es la faja longitudinal o zona '
                                'de contacto entre el mar y la costa, entre '
                                'el nivel de pleamar y bajamar.',
                                'Las penínsulas son porciones de tierra que '
                                'ingresan al mar, unidas al continente por '
                                'un istmo: Paracas (Ica), Illescas (Piura).',
                                'Las puntas son porciones de tierra '
                                'estrechas que ingresan al mar: La Punta en '
                                'el Callao, Lobos en Arequipa.',
                                'Los cabos son porciones de tierra abultadas '
                                'o redondeadas que avanzan hacia el mar: '
                                'Cabo Blanco en Piura.',
                                'Las bahías son entrantes de mar en el '
                                'continente: Paita (Piura), Chimbote '
                                '(Áncash), Paracas (Ica).',
                                'Las islas son porciones de tierra en medio '
                                'del mar; albergan aves guaneras: San '
                                'Lorenzo, Ballestas, Pachacámac.']}],
  'qr_reto': [{'pregunta': 'Los entrantes de mar en el continente, como '
                           'Paracas en Ica, se llaman:',
               'respuesta': 'Bahías'},
              {'pregunta': 'La selva alta también se conoce como:',
               'respuesta': 'Rupa Rupa o Ceja de Selva'},
              {'pregunta': 'Los valles de Tocache y Chanchamayo se '
                           'encuentran, respectivamente, en los '
                           'departamentos de:',
               'respuesta': 'San Martín - Junín'}],
  'qr_dato': 'La región amazónica comprende dos subregiones: la selva alta y '
             'la selva baja.'},
 {'num': 8,
  'titulo': 'Hidrografía del Perú: Ríos y Lagos',
  'secciones': [{'titulo': '8.1 CARACTERÍSTICAS DE LOS RÍOS',
                 'items': ['El {curso} de un río es la distancia entre su '
                           'origen y desembocadura, y comprende tres tramos: '
                           'alto, medio y {bajo}.',
                           'El {caudal} es el volumen de agua que transporta '
                           'el río; cuando es máximo se llama crecida y '
                           'cuando es mínimo se llama {estiaje}.',
                           'El {régimen} de un río puede ser regular, si el '
                           'caudal se mantiene, o irregular, si varía mucho '
                           'durante el año.',
                           'El {cauce} o lecho fluvial es el canal por donde '
                           'se desplazan las aguas.',
                           'El {talweg} o vaguada es la línea que une los '
                           'puntos más profundos del canal fluvial.',
                           'Los ríos {afluentes} son de menor jerarquía y '
                           'desembocan en el río principal.',
                           'Los ríos {efluentes} son los que salen de otro '
                           'río o de un lago.']},
                {'titulo': '8.2 LAS TRES VERTIENTES DEL PERÚ',
                 'items': ['La Autoridad Nacional del Agua (ANA) identificó '
                           '{159} unidades hidrográficas en el Perú.',
                           'La cuenca del {Amazonas} representa el 74,5% del '
                           'territorio nacional, y es la cuenca más extensa '
                           'del Perú, de América y del mundo.',
                           'La Cuenca del {Titicaca} representa el 3,8% del '
                           'territorio nacional y es la mayor cuenca '
                           'endorreica sudamericana.']},
                {'titulo': '8.3 EL LAGO TITICACA',
                 'items': ['El lago Titicaca es el lago {navegable} más alto '
                           'del mundo, ubicado a 3810 m de altitud.',
                           'El Titicaca tiene un área de {8380} km², de los '
                           'cuales 4996,28 km² pertenecen al {Perú}.',
                           'El origen del lago Titicaca es {tectónico}, '
                           'formado por el hundimiento de la zona por el '
                           'levantamiento andino.',
                           'El Titicaca se divide en dos sectores separados '
                           'por el Estrecho de {Tiquina}: el lago Mayor o '
                           'Chucuito hacia el Perú, y el Huiñaymarca hacia '
                           'Bolivia.',
                           'El único río efluente del Titicaca es el río '
                           '{Desaguadero}, que lleva sus aguas al lago Poopó '
                           'y señala el límite con Bolivia.']},
                {'titulo': '8.4 RÍOS MÁS EXTENSOS DEL PERÚ',
                 'items': ['El río más extenso del Perú es el {Ucayali}, con '
                           '1771 km.',
                           'El segundo río más extenso del Perú es el '
                           '{Marañón}, con 1414 km.']}],
  'cuadros': [{'titulo': '8.4 LOS RÍOS MÁS EXTENSOS DEL PERÚ',
               'encabezados': ['Río', 'Longitud'],
               'filas': [['{Ucayali}', '1771 km'],
                         ['{Marañón}', '1414 km'],
                         ['Putumayo', '1380 km'],
                         ['{Yavarí}', '1184 km'],
                         ['Huallaga', '1138 km']]}],
  'preguntas': [{'pregunta': 'El volumen de agua que transporta un río se '
                             'denomina:',
                 'alternativas': ['Caudal',
                                  'Curso',
                                  'Cauce',
                                  'Talweg',
                                  'Régimen'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando un río arrastra la mínima cantidad de '
                             'agua, se le llama:',
                 'alternativas': ['Estiaje',
                                  'Crecida',
                                  'Afluente',
                                  'Cauce',
                                  'Torrente'],
                 'correcta': 'A'},
                {'pregunta': 'El canal o lecho por donde se desplazan las '
                             'aguas del río se llama:',
                 'alternativas': ['Régimen',
                                  'Talweg',
                                  'Cauce',
                                  'Curso',
                                  'Vertiente'],
                 'correcta': 'C'},
                {'pregunta': 'La línea que une los puntos más profundos del '
                             'canal fluvial es:',
                 'alternativas': ['El talweg o vaguada',
                                  'La cuenca',
                                  'El régimen',
                                  'El curso',
                                  'El cauce'],
                 'correcta': 'A'},
                {'pregunta': 'Los ríos que salen de otro río o de un lago se '
                             'denominan:',
                 'alternativas': ['Torrentosos',
                                  'Afluentes',
                                  'Principales',
                                  'Efluentes',
                                  'Confluentes'],
                 'correcta': 'D'},
                {'pregunta': 'La ANA ha identificado en el Perú un total de '
                             'unidades hidrográficas de:',
                 'alternativas': ['99', '59', '259', '359', '159'],
                 'correcta': 'E'},
                {'pregunta': 'La cuenca del Amazonas representa del '
                             'territorio nacional:',
                 'alternativas': ['12,5%', '74,5%', '3,8%', '57,3%', '30,2%'],
                 'correcta': 'B'},
                {'pregunta': 'La cuenca hidrográfica más extensa del Perú, '
                             'de América y del mundo es la del:',
                 'alternativas': ['Amazonas',
                                  'Titicaca',
                                  'Marañón',
                                  'Ucayali',
                                  'Pacífico'],
                 'correcta': 'A'},
                {'pregunta': 'La cuenca del Titicaca representa del '
                             'territorio nacional:',
                 'alternativas': ['57,3%', '3,8%', '30,2%', '12,5%', '74,5%'],
                 'correcta': 'B'},
                {'pregunta': 'El lago Titicaca es reconocido mundialmente '
                             'por ser el lago:',
                 'alternativas': ['Más extenso de Sudamérica',
                                  'Más frío del planeta',
                                  'Con más islas del mundo',
                                  'Más profundo del mundo',
                                  'Navegable más alto del mundo'],
                 'correcta': 'E'},
                {'pregunta': 'El lago Titicaca se ubica a una altitud '
                             'aproximada de:',
                 'alternativas': ['3 810 m',
                                  '5 000 m',
                                  '4 500 m',
                                  '1 800 m',
                                  '2 500 m'],
                 'correcta': 'A'},
                {'pregunta': 'El origen geológico del lago Titicaca es:',
                 'alternativas': ['Kárstico',
                                  'Tectónico',
                                  'Eólico',
                                  'Volcánico',
                                  'Glaciar exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El lago Titicaca se divide en dos sectores '
                             'separados por el Estrecho de:',
                 'alternativas': ['Bering',
                                  'Panamá',
                                  'Tiquina',
                                  'Gibraltar',
                                  'Magallanes'],
                 'correcta': 'C'},
                {'pregunta': 'El sector del Titicaca correspondiente al Perú '
                             'se llama lago Mayor o:',
                 'alternativas': ['Uros',
                                  'Chucuito',
                                  'Huiñaymarca',
                                  'Taraco',
                                  'Poopó'],
                 'correcta': 'B'},
                {'pregunta': 'El único río efluente del lago Titicaca es el '
                             'río:',
                 'alternativas': ['Ilave',
                                  'Suchez',
                                  'Coata',
                                  'Desaguadero',
                                  'Ramis'],
                 'correcta': 'D'},
                {'pregunta': 'El río Desaguadero desemboca finalmente en el '
                             'lago:',
                 'alternativas': ['Titicaca',
                                  'Junín',
                                  'Poopó',
                                  'Parinacochas',
                                  'Chinchaycocha'],
                 'correcta': 'C'},
                {'pregunta': 'El río más extenso del Perú es el:',
                 'alternativas': ['Ucayali',
                                  'Mantaro',
                                  'Marañón',
                                  'Amazonas',
                                  'Huallaga'],
                 'correcta': 'A'},
                {'pregunta': 'El segundo río más extenso del Perú es el:',
                 'alternativas': ['Ucayali',
                                  'Yavarí',
                                  'Vilcanota',
                                  'Putumayo',
                                  'Marañón'],
                 'correcta': 'E'},
                {'pregunta': 'El río Ramis, principal afluente del Titicaca, '
                             'tiene una longitud de:',
                 'alternativas': ['180 km',
                                  '163 km',
                                  '500 km',
                                  '304 km',
                                  '250 km'],
                 'correcta': 'D'},
                {'pregunta': 'El río Rímac nace en el nevado de:',
                 'alternativas': ['Coropuna',
                                  'Salkantay',
                                  'Huascarán',
                                  'Ausangate',
                                  'Tíclio'],
                 'correcta': 'E'},
                {'pregunta': 'La confluencia de los ríos Apurímac y Mantaro '
                             'forman el río: (II CEPRU 2025)',
                 'alternativas': ['Perené',
                                  'Ene',
                                  'Huallaga',
                                  'Tambo',
                                  'Ucayali'],
                 'correcta': 'B'},
                {'pregunta': 'En la llanura amazónica, las Qochas o lagos de '
                             'media luna son originados por la dinámica: '
                             '(Primera Oportunidad UNSAAC 2021)',
                 'alternativas': ['Faunística',
                                  'Mareomotriz',
                                  'Eólica',
                                  'Fluvial',
                                  'Forestal'],
                 'correcta': 'D'},
                {'pregunta': 'Los ríos cuyas nacientes y recorrido se '
                             'encuentran en la vertiente occidental de los '
                             'Andes peruanos, de régimen irregular y con '
                             'dirección de este a oeste, corresponden a la '
                             'región hidrográfica del: (Primera Oportunidad '
                             'UNSAAC 2021)',
                 'alternativas': ['Pacífico',
                                  'Ucayali',
                                  'Alto Madre de Dios',
                                  'Titicaca',
                                  'Amazonas'],
                 'correcta': 'A'},
                {'pregunta': 'El río de la cuenca del Pacífico que erosiona '
                             'el Cañón del Pato es el río: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Tumbes',
                                  'Rímac',
                                  'Virú',
                                  'Chira',
                                  'Santa'],
                 'correcta': 'E'},
                {'pregunta': 'El río Amazonas se forma en la localidad de '
                             'Nauta a partir de la confluencia de los ríos: '
                             '(Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Ene y Perené',
                                  'Marañón y Ucayali',
                                  'Palcazu y Piches',
                                  'Tambo y Urubamba',
                                  'Mantaro y Apurímac'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CARACTERÍSTICAS DE LOS RÍOS',
                      'items': ['El curso de un río es la distancia entre su '
                                'origen y desembocadura, y comprende tres '
                                'tramos: alto, medio y bajo.',
                                'El caudal es el volumen de agua que '
                                'transporta el río; cuando es máximo se '
                                'llama crecida y cuando es mínimo se llama '
                                'estiaje.',
                                'El régimen de un río puede ser regular, si '
                                'el caudal se mantiene, o irregular, si '
                                'varía mucho durante el año.',
                                'El cauce o lecho fluvial es el canal por '
                                'donde se desplazan las aguas.',
                                'El talweg o vaguada es la línea que une los '
                                'puntos más profundos del canal fluvial.',
                                'Los ríos afluentes son de menor jerarquía y '
                                'desembocan en el río principal.',
                                'Los ríos efluentes son los que salen de '
                                'otro río o de un lago.']},
                     {'titulo': 'LAS TRES VERTIENTES DEL PERÚ',
                      'items': ['La Autoridad Nacional del Agua (ANA) '
                                'identificó 159 unidades hidrográficas en el '
                                'Perú.',
                                'La cuenca del Amazonas representa el 74,5% '
                                'del territorio nacional, y es la cuenca más '
                                'extensa del Perú, de América y del mundo.',
                                'La Cuenca del Titicaca representa el 3,8% '
                                'del territorio nacional y es la mayor '
                                'cuenca endorreica sudamericana.']},
                     {'titulo': 'EL LAGO TITICACA',
                      'items': ['El lago Titicaca es el lago navegable más '
                                'alto del mundo, ubicado a 3810 m de '
                                'altitud.',
                                'El Titicaca tiene un área de 8380 km², de '
                                'los cuales 4996,28 km² pertenecen al Perú.',
                                'El origen del lago Titicaca es tectónico, '
                                'formado por el hundimiento de la zona por '
                                'el levantamiento andino.',
                                'El Titicaca se divide en dos sectores '
                                'separados por el Estrecho de Tiquina: el '
                                'lago Mayor o Chucuito hacia el Perú, y el '
                                'Huiñaymarca hacia Bolivia.',
                                'El único río efluente del Titicaca es el '
                                'río Desaguadero, que lleva sus aguas al '
                                'lago Poopó y señala el límite con '
                                'Bolivia.']},
                     {'titulo': 'RÍOS MÁS EXTENSOS DEL PERÚ',
                      'items': ['El río más extenso del Perú es el Ucayali, '
                                'con 1771 km.',
                                'El segundo río más extenso del Perú es el '
                                'Marañón, con 1414 km.']}],
  'qr_reto': [{'pregunta': 'El río Ramis, principal afluente del Titicaca, '
                           'tiene una longitud de:',
               'respuesta': '304 km'},
              {'pregunta': 'La ANA ha identificado en el Perú un total de '
                           'unidades hidrográficas de:',
               'respuesta': '159'},
              {'pregunta': 'El sector del Titicaca correspondiente al Perú '
                           'se llama lago Mayor o:',
               'respuesta': 'Chucuito'}],
  'qr_dato': 'La cuenca del Amazonas representa el 74,5% del territorio '
             'nacional, y es la cuenca más extensa del Perú, de América y '
             'del mundo.'},
 {'num': 9,
  'titulo': 'Hidrografía del Perú: Mar Peruano',
  'secciones': [{'titulo': '9.1 EL MAR PERUANO',
                 'items': ['El mar peruano se extiende desde la línea de '
                           'Concordia hasta la Boca de {Capones}, y hasta '
                           '{200} millas mar adentro.',
                           'El mar peruano tiene una extensión de {1 140 '
                           '646} km², equivalente al 90% del territorio '
                           'peruano.',
                           'Tras el fallo de la Corte Internacional de {La '
                           'Haya}, el Perú obtuvo 50 284 km² adicionales.',
                           'El mar peruano se distingue por la presencia de '
                           'la Corriente Peruana, la {frialdad} de sus aguas '
                           'y su riqueza {ictiológica}.']},
                {'titulo': '9.2 SOBERANÍA MARÍTIMA: LA TESIS DE LAS 200 '
                           'MILLAS',
                 'items': ['La doctrina de las 200 millas fue proclamada por '
                           'Perú, junto con {Chile} y Ecuador.',
                           'La tesis de las 200 millas se declaró mediante '
                           'el D.S. N° {781}, del 1 de agosto de {1947}, en '
                           'el gobierno de José {Bustamante y Rivero}.',
                           'Los fundamentos de la Tesis de las 200 millas '
                           'fueron de orden geológico, geográfico, '
                           '{biológico}, económico, jurídico y '
                           '{estratégico}.']},
                {'titulo': '9.3 CARACTERÍSTICAS POR REGIONES',
                 'items': ['La región norte del mar peruano se extiende '
                           'desde la península de {Illescas} hasta Boca de '
                           'Capones, con temperatura elevada y color azul '
                           '{plomizo}.',
                           'La región central y sur del mar peruano tiene '
                           'una temperatura promedio de {18}°C, por la '
                           'influencia de la Corriente Peruana.',
                           'El fenómeno del {afloramiento} consiste en el '
                           'ascenso de aguas frías hacia la superficie, en '
                           'las zonas del zócalo continental.']},
                {'titulo': '9.4 RELIEVE SUBMARINO',
                 'items': ['La plataforma o {zócalo} continental es el '
                           'relieve submarino que continúa a la costa hasta '
                           'la isóbata de 200 m.',
                           'El {talud} continental se extiende entre las '
                           'isóbatas de 200 a 5000 m, con grandes cañones y '
                           'escarpas.',
                           'Las {fosas marinas} son las mayores '
                           'profundidades del mar peruano, producidas por la '
                           'subducción de la Placa de {Nasca}.',
                           'La Dorsal de {Nasca} es una cordillera submarina '
                           'volcánica ubicada a 150 km de la costa de Ica.']},
                {'titulo': '9.5 AGUAS SUBTERRÁNEAS',
                 'items': ['Las {aguas subterráneas} se encuentran debajo de '
                           'la superficie, infiltradas a través de rocas '
                           '{permeables}.',
                           'El agua que se acumula en el subsuelo, al '
                           'encontrar una roca {impermeable}, se conoce como '
                           '{acuífero}.',
                           'La profundidad a la que se encuentra el agua '
                           'subterránea al hacer un agujero en el suelo se '
                           'llama {nivel freático}.',
                           'El agua subterránea representa unas {veinte} '
                           'veces más que el total de las aguas '
                           'superficiales de la Tierra.',
                           'Del total del agua dulce terrestre, el {21}% es '
                           'agua subterránea.',
                           'Las aguas subterráneas son importantes para el '
                           'sostenimiento de {ríos}, lagos, humedales y '
                           'otros ecosistemas.']}],
  'cuadros': [{'titulo': '9.4 RELIEVE SUBMARINO DEL MAR PERUANO',
               'encabezados': ['Elemento', 'Profundidad'],
               'filas': [['{Zócalo} continental', 'Hasta 200 m'],
                         ['{Talud} continental', '200 a 5000 m'],
                         ['{Fosas} marinas', 'Mayores profundidades']]}],
  'preguntas': [{'pregunta': 'El mar peruano se extiende, en distancia, '
                             'hasta:',
                 'alternativas': ['150 millas',
                                  '200 millas',
                                  '100 millas',
                                  '300 millas',
                                  '50 millas'],
                 'correcta': 'B'},
                {'pregunta': 'La extensión del mar peruano representa del '
                             'territorio peruano aproximadamente:',
                 'alternativas': ['20%', '30%', '50%', '70%', '90%'],
                 'correcta': 'E'},
                {'pregunta': 'Tras el fallo de la Corte de La Haya, el Perú '
                             'obtuvo adicionalmente:',
                 'alternativas': ['50 284 km²',
                                  '200 000 km²',
                                  '100 000 km²',
                                  '500 km²',
                                  '10 000 km²'],
                 'correcta': 'A'},
                {'pregunta': 'El mar peruano se distingue de otros por la '
                             'presencia de:',
                 'alternativas': ['Ausencia de peces',
                                  'La Corriente Peruana y la frialdad de sus '
                                  'aguas',
                                  'Escasa vida marina',
                                  'Aguas dulces',
                                  'Aguas cálidas todo el año'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina de las 200 millas fue proclamada '
                             'por Perú junto con Ecuador y:',
                 'alternativas': ['Colombia',
                                  'Chile',
                                  'Brasil',
                                  'Argentina',
                                  'Bolivia'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis de las 200 millas se declaró mediante '
                             'el D.S. N° 781 en el gobierno de:',
                 'alternativas': ['Manuel A. Odría',
                                  'Fernando Belaunde',
                                  'José Bustamante y Rivero',
                                  'Alan García',
                                  'Alberto Fujimori'],
                 'correcta': 'C'},
                {'pregunta': 'La tesis de las 200 millas se proclamó en el '
                             'año:',
                 'alternativas': ['1980', '1993', '1960', '1930', '1947'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los fundamentos de la Tesis de las 200 '
                             'millas NO figura el fundamento:',
                 'alternativas': ['Biológico',
                                  'Religioso',
                                  'Económico',
                                  'Geológico',
                                  'Estratégico'],
                 'correcta': 'B'},
                {'pregunta': 'La región norte del mar peruano se extiende '
                             'desde la Península de Illescas hasta:',
                 'alternativas': ['Tacna',
                                  'Boca de Capones',
                                  'Paracas',
                                  'Trujillo',
                                  'Ica'],
                 'correcta': 'B'},
                {'pregunta': 'El color del mar en la región norte se debe '
                             'principalmente a:',
                 'alternativas': ['El afloramiento',
                                  'El plancton',
                                  'La sal',
                                  'Las algas',
                                  'La descarga de los ríos'],
                 'correcta': 'E'},
                {'pregunta': 'La temperatura promedio del mar en la región '
                             'central y sur es de:',
                 'alternativas': ['25°C', '10°C', '30°C', '18°C', '5°C'],
                 'correcta': 'D'},
                {'pregunta': 'El color verdoso del mar en la región central '
                             'y sur se debe a:',
                 'alternativas': ['La arena',
                                  'Los sedimentos fluviales',
                                  'La temperatura',
                                  'Las corrientes cálidas',
                                  'El plancton y las algas'],
                 'correcta': 'E'},
                {'pregunta': 'El fenómeno del afloramiento consiste en:',
                 'alternativas': ['La formación de olas',
                                  'El derretimiento de glaciares',
                                  'La evaporación del mar',
                                  'El hundimiento de aguas cálidas',
                                  'El ascenso de aguas frías hacia la '
                                  'superficie'],
                 'correcta': 'E'},
                {'pregunta': 'La plataforma o zócalo continental llega hasta '
                             'la isóbata de:',
                 'alternativas': ['200 m',
                                  '50 m',
                                  '1000 m',
                                  '100 m',
                                  '500 m'],
                 'correcta': 'A'},
                {'pregunta': 'El talud continental se extiende entre las '
                             'isóbatas de:',
                 'alternativas': ['0 a 50 m',
                                  '200 a 5000 m',
                                  '0 a 100 m',
                                  '5000 a 10000 m',
                                  '500 a 1000 m'],
                 'correcta': 'B'},
                {'pregunta': 'Las fosas marinas se producen por:',
                 'alternativas': ['El afloramiento',
                                  'La subducción de la Placa de Nasca',
                                  'La erosión eólica',
                                  'La sedimentación fluvial',
                                  'Las corrientes marinas'],
                 'correcta': 'B'},
                {'pregunta': 'La Dorsal de Nasca es:',
                 'alternativas': ['Una península',
                                  'Una fosa marina',
                                  'Un golfo',
                                  'Una cordillera submarina volcánica',
                                  'Una bahía'],
                 'correcta': 'D'},
                {'pregunta': 'La Dorsal de Nasca se ubica aproximadamente a '
                             'qué distancia de la costa de Ica:',
                 'alternativas': ['500 km',
                                  '10 km',
                                  '300 km',
                                  '150 km',
                                  '50 km'],
                 'correcta': 'D'},
                {'pregunta': 'El fundamento geológico de la Tesis de las 200 '
                             'millas se refiere a:',
                 'alternativas': ['La continuidad del zócalo continental',
                                  'La riqueza pesquera',
                                  'La seguridad nacional',
                                  'El turismo',
                                  'El comercio marítimo'],
                 'correcta': 'A'},
                {'pregunta': 'La salinidad del mar en la región norte es de '
                             'aproximadamente:',
                 'alternativas': ['45 gr/l',
                                  '40 gr/l',
                                  '30 gr/l',
                                  '20 gr/l',
                                  '34 gr/l'],
                 'correcta': 'E'},
                {'pregunta': 'La alteración del fenómeno de afloramiento y '
                             'la desaparición de la capa de inversión '
                             'térmica son consecuencias de: (II CEPRU 2025)',
                 'alternativas': ['La corriente de Humboldt',
                                  'Las olas y mareas',
                                  'La circumpolar Antártica',
                                  'El fenómeno de La Niña',
                                  'El fenómeno de El Niño'],
                 'correcta': 'E'},
                {'pregunta': 'Un impacto negativo de la actividad pesquera '
                             'es: (II CEPRU 2024)',
                 'alternativas': ['La pesca de arrastre',
                                  'La pesca controlada',
                                  'La pesca selectiva',
                                  'Incremento de la economía',
                                  'Desarrollo sostenible'],
                 'correcta': 'A'},
                {'pregunta': 'El fundamento de la tesis de las 200 millas '
                             'marinas, que consiste en la continuidad del '
                             'zócalo continental, es de carácter: (II CEPRU '
                             '2022)',
                 'alternativas': ['Geográfico',
                                  'Biológico',
                                  'Económico',
                                  'Jurídico',
                                  'Geológico'],
                 'correcta': 'E'},
                {'pregunta': 'La corriente peruana circula con una '
                             'dirección: (I CEPRU 2024)',
                 'alternativas': ['NE a SE',
                                  'NW a SE',
                                  'SE a NW',
                                  'SW a NE',
                                  'NW a SW'],
                 'correcta': 'C'},
                {'pregunta': 'La ausencia de la inversión térmica y la '
                             'alteración del fenómeno de afloramiento '
                             'costero son consecuencias del fenómeno de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['La Niña',
                                  'La corriente circumpolar antártica',
                                  'El Niño',
                                  'El aguaje o pintor',
                                  'La corriente ecuatorial del sur'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los fundamentos de la Tesis de las 200 '
                             'Millas Marítimas es: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['El enfriamiento del mar',
                                  'El dominio marítimo y terrestre',
                                  'La seguridad territorial',
                                  'La presencia de riqueza ictiológica',
                                  'La presencia de fauna tropical'],
                 'correcta': 'D'},
                {'pregunta': 'Las aguas que se encuentran debajo de la '
                             'superficie, infiltradas a través de rocas '
                             'permeables, se llaman aguas:',
                 'alternativas': ['Marinas',
                                  'Superficiales',
                                  'Glaciares',
                                  'Pluviales exclusivas',
                                  'Subterráneas'],
                 'correcta': 'E'},
                {'pregunta': 'El agua que se acumula en el subsuelo, al '
                             'encontrar una roca impermeable, se conoce '
                             'como:',
                 'alternativas': ['Manantial',
                                  'Nivel freático',
                                  'Napa superficial',
                                  'Acuífero',
                                  'Vertiente'],
                 'correcta': 'D'},
                {'pregunta': 'La profundidad a la que se encuentra el agua '
                             'subterránea al hacer un agujero en el suelo se '
                             'llama:',
                 'alternativas': ['Nivel freático',
                                  'Napa profunda',
                                  'Estrato acuoso',
                                  'Acuífero',
                                  'Vertiente hídrica'],
                 'correcta': 'A'},
                {'pregunta': 'El agua subterránea representa, respecto al '
                             'total de las aguas superficiales de la Tierra, '
                             'aproximadamente:',
                 'alternativas': ['La mitad',
                                  'Veinte veces más',
                                  'Diez veces menos',
                                  'Una cantidad similar',
                                  'El doble'],
                 'correcta': 'B'},
                {'pregunta': 'Del total del agua dulce terrestre, el '
                             'porcentaje que corresponde a agua subterránea '
                             'es aproximadamente:',
                 'alternativas': ['50%', '5%', '90%', '75%', '21%'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'EL MAR PERUANO',
                      'items': ['El mar peruano se extiende desde la línea '
                                'de Concordia hasta la Boca de Capones, y '
                                'hasta 200 millas mar adentro.',
                                'El mar peruano tiene una extensión de 1 140 '
                                '646 km², equivalente al 90% del territorio '
                                'peruano.',
                                'Tras el fallo de la Corte Internacional de '
                                'La Haya, el Perú obtuvo 50 284 km² '
                                'adicionales.',
                                'El mar peruano se distingue por la '
                                'presencia de la Corriente Peruana, la '
                                'frialdad de sus aguas y su riqueza '
                                'ictiológica.']},
                     {'titulo': 'SOBERANÍA MARÍTIMA: LA TESIS DE LAS 200 '
                                'MILLAS',
                      'items': ['La doctrina de las 200 millas fue '
                                'proclamada por Perú, junto con Chile y '
                                'Ecuador.',
                                'La tesis de las 200 millas se declaró '
                                'mediante el D.S. N° 781, del 1 de agosto de '
                                '1947, en el gobierno de José Bustamante y '
                                'Rivero.',
                                'Los fundamentos de la Tesis de las 200 '
                                'millas fueron de orden geológico, '
                                'geográfico, biológico, económico, jurídico '
                                'y estratégico.']},
                     {'titulo': 'CARACTERÍSTICAS POR REGIONES',
                      'items': ['La región norte del mar peruano se extiende '
                                'desde la península de Illescas hasta Boca '
                                'de Capones, con temperatura elevada y color '
                                'azul plomizo.',
                                'La región central y sur del mar peruano '
                                'tiene una temperatura promedio de 18°C, por '
                                'la influencia de la Corriente Peruana.',
                                'El fenómeno del afloramiento consiste en el '
                                'ascenso de aguas frías hacia la superficie, '
                                'en las zonas del zócalo continental.']},
                     {'titulo': 'RELIEVE SUBMARINO',
                      'items': ['La plataforma o zócalo continental es el '
                                'relieve submarino que continúa a la costa '
                                'hasta la isóbata de 200 m.',
                                'El talud continental se extiende entre las '
                                'isóbatas de 200 a 5000 m, con grandes '
                                'cañones y escarpas.',
                                'Las fosas marinas son las mayores '
                                'profundidades del mar peruano, producidas '
                                'por la subducción de la Placa de Nasca.',
                                'La Dorsal de Nasca es una cordillera '
                                'submarina volcánica ubicada a 150 km de la '
                                'costa de Ica.']},
                     {'titulo': 'AGUAS SUBTERRÁNEAS',
                      'items': ['Las aguas subterráneas se encuentran debajo '
                                'de la superficie, infiltradas a través de '
                                'rocas permeables.',
                                'El agua que se acumula en el subsuelo, al '
                                'encontrar una roca impermeable, se conoce '
                                'como acuífero.',
                                'La profundidad a la que se encuentra el '
                                'agua subterránea al hacer un agujero en el '
                                'suelo se llama nivel freático.',
                                'El agua subterránea representa unas veinte '
                                'veces más que el total de las aguas '
                                'superficiales de la Tierra.',
                                'Del total del agua dulce terrestre, el 21% '
                                'es agua subterránea.',
                                'Las aguas subterráneas son importantes para '
                                'el sostenimiento de ríos, lagos, humedales '
                                'y otros ecosistemas.']}],
  'qr_reto': [{'pregunta': 'Las fosas marinas se producen por:',
               'respuesta': 'La subducción de la Placa de Nasca'},
              {'pregunta': 'El mar peruano se extiende, en distancia, hasta:',
               'respuesta': '200 millas'},
              {'pregunta': 'El fenómeno del afloramiento consiste en:',
               'respuesta': 'El ascenso de aguas frías hacia la superficie'}],
  'qr_dato': 'Del total del agua dulce terrestre, el 21% es agua '
             'subterránea.'},
 {'num': 10,
  'titulo': 'Atmósfera y Cambio Climático',
  'secciones': [{'titulo': '10.1 LA ATMÓSFERA Y SU COMPOSICIÓN',
                 'items': ['La atmósfera regula las temperaturas extremas y '
                           'nos protege de los rayos {ultravioleta} y de '
                           'cuerpos como los meteoritos.',
                           'El gas más abundante de la atmósfera es el '
                           '{nitrógeno}, con 78,08%; le sigue el {oxígeno}, '
                           'con 20,94%.',
                           'Entre los gases de efecto invernadero figuran el '
                           '{CO2} y el vapor de agua.']},
                {'titulo': '10.2 LA TROPÓSFERA',
                 'items': ['La {tropósfera} es la capa inferior de la '
                           'atmósfera, con un promedio de {12,5} km de '
                           'altitud.',
                           'En la tropósfera, la temperatura disminuye 0,6°C '
                           'por cada 100 m de altitud, fenómeno llamado '
                           '{Gradiente Térmico Vertical}.',
                           'La tropósfera es la capa más {densa} y donde se '
                           'producen los meteoros como nubes, viento y '
                           'humedad.']},
                {'titulo': '10.3 LA ESTRATÓSFERA Y LA CAPA DE OZONO',
                 'items': ['La {estratósfera} cubre la tropósfera hasta los '
                           '50 km de altitud, y es la zona de {calma}.',
                           'Entre los 24 y 30 km se encuentra la capa de '
                           'ozono, llamada {ozonósfera}, que impide el paso '
                           'de los rayos ultravioleta.',
                           'En la estratósfera, la temperatura {aumenta} '
                           'progresivamente, invirtiendo el gradiente '
                           'térmico vertical.']},
                {'titulo': '10.4 MESÓSFERA Y TERMÓSFERA',
                 'items': ['La {mesósfera} se extiende de 50 a 90 km, con '
                           'temperaturas que llegan hasta -110°C.',
                           'La {termósfera} o ionósfera se localiza entre '
                           'los 90 y 500 km, con temperaturas de hasta '
                           '1500°C.',
                           'En la termósfera, los elementos se encuentran '
                           '{ionizados}, y allí se producen las auroras '
                           'polares.']},
                {'titulo': '10.5 EL TIEMPO Y EL CLIMA',
                 'items': ['El {tiempo meteorológico} es el estado de la '
                           'atmósfera en un momento y lugar determinados; es '
                           '{instantáneo}, cambiante e irrepetible.',
                           'El {clima} es el estado medio de las condiciones '
                           'atmosféricas de un lugar a lo largo de un {año}; '
                           'es la sucesión frecuente de tipos de tiempo.',
                           'La {radiación solar} es la fuente principal de '
                           'energía que dinamiza la atmósfera; se propaga a '
                           '{300 000} km/seg.',
                           'La radiación solar se mide con el {actinómetro} '
                           'y se registra con el actinógrafo; el '
                           '{heliógrafo} registra las horas de brillo '
                           'solar.']},
                {'titulo': '10.6 ELEMENTOS DEL CLIMA',
                 'items': ['La {temperatura} es el grado de calor o frío '
                           'sensible en la atmósfera; se mide con el '
                           '{termómetro} y se registra con el termógrafo.',
                           'La {presión atmosférica} es el peso que ejerce '
                           'el aire sobre la superficie terrestre; a nivel '
                           'del mar es de {1013,25} mb.',
                           'Los {vientos} son corrientes de aire originadas '
                           'por diferencia de presiones; su velocidad se '
                           'mide con el {anemómetro} y su dirección con la '
                           'veleta.',
                           'La {humedad relativa} es la cantidad de vapor de '
                           'agua que podría retener la atmósfera a una '
                           'temperatura dada; se mide con el {higrómetro} o '
                           'psicrómetro.',
                           'La {precipitación} es la caída de aguas '
                           'meteóricas por efecto de la gravedad; se mide '
                           'con el {pluviómetro} y se registra con el '
                           'pluviógrafo, en milímetros.']},
                {'titulo': '10.7 FACTORES DEL CLIMA',
                 'items': ['Los {factores del clima} son las características '
                           'propias y fijas de un lugar que alteran el '
                           'comportamiento de los elementos climáticos.',
                           'La {latitud} determina que a bajas latitudes '
                           'correspondan climas cálidos y húmedos, y a altas '
                           'latitudes climas {fríos} y secos.',
                           'La {altitud} determina que a menor altitud '
                           'correspondan climas cálidos, y a grandes '
                           'altitudes climas {fríos} y secos.',
                           'La {oceanidad y continentalidad} determina que '
                           'las zonas cercanas a masas de agua tengan climas '
                           'más {frescos} y suaves.',
                           'Las {corrientes marinas} cálidas determinan '
                           'climas cálidos y lluviosos; las corrientes '
                           '{frías} determinan climas fríos y secos.']},
                {'titulo': '10.8 FACTORES CONDICIONANTES DEL CLIMA PERUANO',
                 'items': ['El Perú es considerado la {síntesis climática} '
                           'del mundo, por tener la mayor parte de los '
                           'climas existentes.',
                           'La {Corriente Peruana} o de Humboldt es fría y '
                           'determina la sequedad del clima {subtropical '
                           'árido} de la costa central y sur.',
                           'La {Corriente de El Niño} determina el clima '
                           'semitropical, cálido y húmedo, de la {costa '
                           'norte} del Perú.',
                           'El {Anticiclón del Pacífico Sur} es una masa de '
                           'aire de alta presión que gira en sentido '
                           '{antihorario}, provocando tiempo estable y '
                           'ausencia de precipitaciones.',
                           'El Anticiclón del Pacífico Sur, junto con la '
                           'Corriente Peruana, determina el clima {árido} de '
                           'la costa.']}],
  'cuadros': [{'titulo': '10.2-10.4 CAPAS DE LA ATMÓSFERA',
               'encabezados': ['Capa', 'Altitud'],
               'filas': [['{Tropósfera}', 'Hasta 12,5 km'],
                         ['{Estratósfera}', '12,5 a 50 km'],
                         ['{Mesósfera}', '50 a 90 km'],
                         ['{Termósfera}', '90 a 500 km']]},
              {'titulo': 'INSTRUMENTOS DE MEDICIÓN DE LOS ELEMENTOS DEL '
                         'CLIMA',
               'despues_de': '10.6 ELEMENTOS DEL CLIMA',
               'encabezados': ['Elemento', 'Instrumento', 'Unidad de medida'],
               'filas': [['Temperatura', '{Termómetro}', '°C / °F'],
                         ['Presión atmosférica', '{Barómetro}', 'mm Hg / mb'],
                         ['Viento (velocidad)', '{Anemómetro}', 'm/s, km/h'],
                         ['Viento (dirección)', '{Veleta}', 'Rumbos'],
                         ['Humedad',
                          '{Higrómetro} / Psicrómetro',
                          'Porcentaje (%)'],
                         ['Precipitación',
                          '{Pluviómetro}',
                          'Milímetros (mm)']]}],
  'preguntas': [{'pregunta': 'La atmósfera nos protege principalmente de:',
                 'alternativas': ['Los sismos',
                                  'Los rayos ultravioleta y meteoritos',
                                  'Las mareas',
                                  'La lluvia ácida',
                                  'La erosión'],
                 'correcta': 'B'},
                {'pregunta': 'El gas más abundante de la atmósfera es:',
                 'alternativas': ['Dióxido de carbono',
                                  'Nitrógeno',
                                  'Oxígeno',
                                  'Ozono',
                                  'Argón'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo gas más abundante de la atmósfera '
                             'es:',
                 'alternativas': ['Helio',
                                  'Argón',
                                  'Oxígeno',
                                  'Nitrógeno',
                                  'Neón'],
                 'correcta': 'C'},
                {'pregunta': 'La capa inferior de la atmósfera, donde '
                             'ocurren los fenómenos meteorológicos, es:',
                 'alternativas': ['La estratósfera',
                                  'La mesósfera',
                                  'La tropósfera',
                                  'La ionósfera',
                                  'La termósfera'],
                 'correcta': 'C'},
                {'pregunta': 'La altitud promedio de la tropósfera es de:',
                 'alternativas': ['12,5 km',
                                  '100 km',
                                  '50 km',
                                  '90 km',
                                  '5 km'],
                 'correcta': 'A'},
                {'pregunta': 'En la tropósfera, la temperatura disminuye '
                             '0,6°C cada:',
                 'alternativas': ['500 m', '1000 m', '10 m', '100 m', '50 m'],
                 'correcta': 'D'},
                {'pregunta': 'El fenómeno de disminución de temperatura con '
                             'la altitud en la tropósfera se llama:',
                 'alternativas': ['Capa de ozono',
                                  'Inversión térmica',
                                  'Efecto invernadero',
                                  'Corriente de chorro',
                                  'Gradiente Térmico Vertical'],
                 'correcta': 'E'},
                {'pregunta': 'La capa de ozono se ubica dentro de la:',
                 'alternativas': ['Tropósfera',
                                  'Exósfera',
                                  'Termósfera',
                                  'Mesósfera',
                                  'Estratósfera'],
                 'correcta': 'E'},
                {'pregunta': 'La capa de ozono se ubica entre los:',
                 'alternativas': ['0 y 10 km',
                                  '90 y 500 km',
                                  '50 y 90 km',
                                  '24 y 30 km',
                                  '10 y 20 km'],
                 'correcta': 'D'},
                {'pregunta': 'La función principal de la capa de ozono es:',
                 'alternativas': ['Regular la humedad',
                                  'Formar nubes',
                                  'Producir lluvia',
                                  'Generar viento',
                                  'Impedir el paso de los rayos '
                                  'ultravioleta'],
                 'correcta': 'E'},
                {'pregunta': 'En la estratósfera, la temperatura:',
                 'alternativas': ['Baja a cero',
                                  'Fluctúa sin patrón',
                                  'Disminuye constantemente',
                                  'Aumenta progresivamente',
                                  'Se mantiene igual'],
                 'correcta': 'D'},
                {'pregunta': 'La mesósfera se extiende entre:',
                 'alternativas': ['0 y 12,5 km',
                                  '500 y 1000 km',
                                  '50 y 90 km',
                                  '90 y 500 km',
                                  '12,5 y 50 km'],
                 'correcta': 'C'},
                {'pregunta': 'En la mesósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['-50°C', '50°C', '100°C', '0°C', '-110°C'],
                 'correcta': 'E'},
                {'pregunta': 'La termósfera o ionósfera se localiza entre:',
                 'alternativas': ['90 y 500 km',
                                  '12,5 y 50 km',
                                  '500 y 1000 km',
                                  '0 y 12,5 km',
                                  '50 y 90 km'],
                 'correcta': 'A'},
                {'pregunta': 'En la termósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['0°C',
                                  '-100°C',
                                  '100°C',
                                  '300°C',
                                  '800°C a 1500°C'],
                 'correcta': 'E'},
                {'pregunta': 'Las auroras polares se producen en:',
                 'alternativas': ['La tropósfera',
                                  'La termósfera',
                                  'La estratósfera',
                                  'La mesósfera',
                                  'La capa de ozono'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos de la termósfera se encuentran:',
                 'alternativas': ['Ionizados o electrizados',
                                  'Sólidos',
                                  'Congelados',
                                  'Líquidos',
                                  'Inertes'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los gases de efecto invernadero figura '
                             'principalmente:',
                 'alternativas': ['El helio',
                                  'El CO2',
                                  'El argón',
                                  'El neón',
                                  'El nitrógeno'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la atmósfera, el paisaje terrestre sería '
                             'similar al de:',
                 'alternativas': ['La Luna',
                                  'Júpiter',
                                  'Saturno',
                                  'Venus',
                                  'Marte'],
                 'correcta': 'A'},
                {'pregunta': 'El límite final de la tropósfera se llama:',
                 'alternativas': ['Tropopausa',
                                  'Termopausa',
                                  'Mesopausa',
                                  'Ionopausa',
                                  'Estratopausa'],
                 'correcta': 'A'},
                {'pregunta': 'La mayor cantidad de climas en el Perú está '
                             'determinada por el factor: (II CEPRU 2025)',
                 'alternativas': ['Latitud',
                                  'Altitud',
                                  'Anticiclón del Pacífico Sur',
                                  'Corrientes marinas',
                                  'Vegetación'],
                 'correcta': 'B'},
                {'pregunta': 'Los registros de los fenómenos meteorológicos '
                             'sirven para pronosticar: (I CEPRU 2025)',
                 'alternativas': ['Calentamiento global',
                                  'Tiempo meteorológico',
                                  'Cambio climático',
                                  'Tiempo cronológico',
                                  'Variabilidad climática'],
                 'correcta': 'B'},
                {'pregunta': 'Las auroras polares se producen en la capa '
                             'atmosférica de la: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Ionosfera',
                                  'Troposfera',
                                  'Mesosfera',
                                  'Estratosfera',
                                  'Termosfera exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Corresponde a la Tropósfera: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Tiene una subcapa llamada Ozonósfera',
                                  'Es una zona de radiación cósmica',
                                  'Alcanza hasta la termopausa',
                                  'Se producen los fenómenos meteorológicos',
                                  'Existen los cinturones de radiación de '
                                  'Van Allen'],
                 'correcta': 'D'},
                {'pregunta': 'El instrumento que mide la intensidad de los '
                             'vientos es el: (Primera Oportunidad UNSAAC '
                             '2020)',
                 'alternativas': ['Termómetro',
                                  'Pluviómetro',
                                  'Barómetro',
                                  'Anemómetro',
                                  'Veleta'],
                 'correcta': 'D'},
                {'pregunta': 'El estado de la atmósfera en un momento y '
                             'lugar determinados, instantáneo y cambiante, '
                             'se llama:',
                 'alternativas': ['Estación',
                                  'Microclima',
                                  'Clima',
                                  'Bioclima',
                                  'Tiempo meteorológico'],
                 'correcta': 'E'},
                {'pregunta': 'El estado medio de las condiciones '
                             'atmosféricas de un lugar a lo largo de un año '
                             'se llama:',
                 'alternativas': ['Régimen',
                                  'Estación',
                                  'Tiempo meteorológico',
                                  'Clima',
                                  'Meteoro'],
                 'correcta': 'D'},
                {'pregunta': 'La radiación solar, fuente principal de '
                             'energía que dinamiza la atmósfera, se mide con '
                             'el:',
                 'alternativas': ['Termómetro',
                                  'Barómetro',
                                  'Actinómetro',
                                  'Pluviómetro',
                                  'Anemómetro'],
                 'correcta': 'C'},
                {'pregunta': 'El grado de calor o frío sensible en la '
                             'atmósfera se llama:',
                 'alternativas': ['Presión atmosférica',
                                  'Temperatura',
                                  'Precipitación',
                                  'Insolación',
                                  'Humedad'],
                 'correcta': 'B'},
                {'pregunta': 'El peso o fuerza que ejerce el aire sobre la '
                             'superficie terrestre se llama:',
                 'alternativas': ['Temperatura',
                                  'Presión atmosférica',
                                  'Humedad',
                                  'Viento',
                                  'Precipitación'],
                 'correcta': 'B'},
                {'pregunta': 'El instrumento que mide la velocidad de los '
                             'vientos es el:',
                 'alternativas': ['Higrómetro',
                                  'Anemómetro',
                                  'Veleta',
                                  'Barómetro',
                                  'Pluviómetro'],
                 'correcta': 'B'},
                {'pregunta': 'El instrumento que mide la dirección de los '
                             'vientos es la:',
                 'alternativas': ['Termómetro',
                                  'Veleta',
                                  'Anemómetro',
                                  'Higrómetro',
                                  'Barómetro'],
                 'correcta': 'B'},
                {'pregunta': 'El instrumento que mide la humedad relativa de '
                             'la atmósfera es el:',
                 'alternativas': ['Anemómetro',
                                  'Termómetro',
                                  'Higrómetro o psicrómetro',
                                  'Barómetro',
                                  'Pluviómetro'],
                 'correcta': 'C'},
                {'pregunta': 'El instrumento que mide la precipitación, en '
                             'milímetros, es el:',
                 'alternativas': ['Anemómetro',
                                  'Barómetro',
                                  'Termómetro',
                                  'Higrómetro',
                                  'Pluviómetro'],
                 'correcta': 'E'},
                {'pregunta': 'Las características propias y fijas de un '
                             'lugar que alteran el comportamiento de los '
                             'elementos climáticos se llaman:',
                 'alternativas': ['Fenómenos climáticos',
                                  'Meteoros',
                                  'Elementos del clima',
                                  'Variables atmosféricas',
                                  'Factores del clima'],
                 'correcta': 'E'},
                {'pregunta': 'Según climatólogos, el Perú es considerado la '
                             'síntesis climática del mundo porque:',
                 'alternativas': ['Tiene solo dos tipos de clima',
                                  'Tiene un clima uniforme en todo el '
                                  'territorio',
                                  'Tiene la mayor parte de los climas '
                                  'existentes en el mundo',
                                  'No tiene variación climática',
                                  'Solo tiene climas tropicales'],
                 'correcta': 'C'},
                {'pregunta': 'La Corriente Peruana o de Humboldt, de aguas '
                             'frías, determina el clima subtropical árido de '
                             'la costa:',
                 'alternativas': ['Insular',
                                  'Central y sur',
                                  'Andina',
                                  'Amazónica',
                                  'Norte'],
                 'correcta': 'B'},
                {'pregunta': 'La Corriente de El Niño determina el clima '
                             'semitropical, cálido y húmedo, de la costa:',
                 'alternativas': ['Norte',
                                  'Amazónica',
                                  'Insular',
                                  'Andina',
                                  'Central y sur'],
                 'correcta': 'A'},
                {'pregunta': 'El Anticiclón del Pacífico Sur es una masa de '
                             'aire de:',
                 'alternativas': ['Baja presión',
                                  'Presión neutra',
                                  'Alta presión',
                                  'Presión mínima',
                                  'Presión variable'],
                 'correcta': 'C'},
                {'pregunta': 'El Anticiclón del Pacífico Sur, junto con la '
                             'Corriente Peruana, determina el clima de la '
                             'costa de tipo:',
                 'alternativas': ['Húmedo y lluvioso',
                                  'Tropical',
                                  'Polar',
                                  'Árido',
                                  'Templado húmedo'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'LA ATMÓSFERA Y SU COMPOSICIÓN',
                      'items': ['La atmósfera regula las temperaturas '
                                'extremas y nos protege de los rayos '
                                'ultravioleta y de cuerpos como los '
                                'meteoritos.',
                                'El gas más abundante de la atmósfera es el '
                                'nitrógeno, con 78,08%; le sigue el oxígeno, '
                                'con 20,94%.',
                                'Entre los gases de efecto invernadero '
                                'figuran el CO2 y el vapor de agua.']},
                     {'titulo': 'LA TROPÓSFERA',
                      'items': ['La tropósfera es la capa inferior de la '
                                'atmósfera, con un promedio de 12,5 km de '
                                'altitud.',
                                'En la tropósfera, la temperatura disminuye '
                                '0,6°C por cada 100 m de altitud, fenómeno '
                                'llamado Gradiente Térmico Vertical.',
                                'La tropósfera es la capa más densa y donde '
                                'se producen los meteoros como nubes, viento '
                                'y humedad.']},
                     {'titulo': 'LA ESTRATÓSFERA Y LA CAPA DE OZONO',
                      'items': ['La estratósfera cubre la tropósfera hasta '
                                'los 50 km de altitud, y es la zona de '
                                'calma.',
                                'Entre los 24 y 30 km se encuentra la capa '
                                'de ozono, llamada ozonósfera, que impide el '
                                'paso de los rayos ultravioleta.',
                                'En la estratósfera, la temperatura aumenta '
                                'progresivamente, invirtiendo el gradiente '
                                'térmico vertical.']},
                     {'titulo': 'MESÓSFERA Y TERMÓSFERA',
                      'items': ['La mesósfera se extiende de 50 a 90 km, con '
                                'temperaturas que llegan hasta -110°C.',
                                'La termósfera o ionósfera se localiza entre '
                                'los 90 y 500 km, con temperaturas de hasta '
                                '1500°C.',
                                'En la termósfera, los elementos se '
                                'encuentran ionizados, y allí se producen '
                                'las auroras polares.']},
                     {'titulo': 'EL TIEMPO Y EL CLIMA',
                      'items': ['El tiempo meteorológico es el estado de la '
                                'atmósfera en un momento y lugar '
                                'determinados; es instantáneo, cambiante e '
                                'irrepetible.',
                                'El clima es el estado medio de las '
                                'condiciones atmosféricas de un lugar a lo '
                                'largo de un año; es la sucesión frecuente '
                                'de tipos de tiempo.',
                                'La radiación solar es la fuente principal '
                                'de energía que dinamiza la atmósfera; se '
                                'propaga a 300 000 km/seg.',
                                'La radiación solar se mide con el '
                                'actinómetro y se registra con el '
                                'actinógrafo; el heliógrafo registra las '
                                'horas de brillo solar.']},
                     {'titulo': 'ELEMENTOS DEL CLIMA',
                      'items': ['La temperatura es el grado de calor o frío '
                                'sensible en la atmósfera; se mide con el '
                                'termómetro y se registra con el termógrafo.',
                                'La presión atmosférica es el peso que '
                                'ejerce el aire sobre la superficie '
                                'terrestre; a nivel del mar es de 1013,25 '
                                'mb.',
                                'Los vientos son corrientes de aire '
                                'originadas por diferencia de presiones; su '
                                'velocidad se mide con el anemómetro y su '
                                'dirección con la veleta.',
                                'La humedad relativa es la cantidad de vapor '
                                'de agua que podría retener la atmósfera a '
                                'una temperatura dada; se mide con el '
                                'higrómetro o psicrómetro.',
                                'La precipitación es la caída de aguas '
                                'meteóricas por efecto de la gravedad; se '
                                'mide con el pluviómetro y se registra con '
                                'el pluviógrafo, en milímetros.']},
                     {'titulo': 'FACTORES DEL CLIMA',
                      'items': ['Los factores del clima son las '
                                'características propias y fijas de un lugar '
                                'que alteran el comportamiento de los '
                                'elementos climáticos.',
                                'La latitud determina que a bajas latitudes '
                                'correspondan climas cálidos y húmedos, y a '
                                'altas latitudes climas fríos y secos.',
                                'La altitud determina que a menor altitud '
                                'correspondan climas cálidos, y a grandes '
                                'altitudes climas fríos y secos.',
                                'La oceanidad y continentalidad determina '
                                'que las zonas cercanas a masas de agua '
                                'tengan climas más frescos y suaves.',
                                'Las corrientes marinas cálidas determinan '
                                'climas cálidos y lluviosos; las corrientes '
                                'frías determinan climas fríos y secos.']},
                     {'titulo': 'FACTORES CONDICIONANTES DEL CLIMA PERUANO',
                      'items': ['El Perú es considerado la síntesis '
                                'climática del mundo, por tener la mayor '
                                'parte de los climas existentes.',
                                'La Corriente Peruana o de Humboldt es fría '
                                'y determina la sequedad del clima '
                                'subtropical árido de la costa central y '
                                'sur.',
                                'La Corriente de El Niño determina el clima '
                                'semitropical, cálido y húmedo, de la costa '
                                'norte del Perú.',
                                'El Anticiclón del Pacífico Sur es una masa '
                                'de aire de alta presión que gira en sentido '
                                'antihorario, provocando tiempo estable y '
                                'ausencia de precipitaciones.',
                                'El Anticiclón del Pacífico Sur, junto con '
                                'la Corriente Peruana, determina el clima '
                                'árido de la costa.']}],
  'qr_reto': [{'pregunta': 'Sin la atmósfera, el paisaje terrestre sería '
                           'similar al de:',
               'respuesta': 'La Luna'},
              {'pregunta': 'El estado medio de las condiciones atmosféricas '
                           'de un lugar a lo largo de un año se llama:',
               'respuesta': 'Clima'},
              {'pregunta': 'El peso o fuerza que ejerce el aire sobre la '
                           'superficie terrestre se llama:',
               'respuesta': 'Presión atmosférica'}],
  'qr_dato': 'El gas más abundante de la atmósfera es el nitrógeno, con '
             '78,08%; le sigue el oxígeno, con 20,94%.'},
 {'num': 11,
  'titulo': 'Recursos Naturales, Conservación e Impacto Ambiental',
  'secciones': [{'titulo': '11.1 CONCEPTO Y CLASIFICACIÓN',
                 'items': ['Los recursos naturales son elementos que la '
                           'naturaleza ofrece espontáneamente para '
                           'satisfacer las necesidades del {hombre}.',
                           'Los recursos naturales no renovables se agotan '
                           'con el aprovechamiento, por existir en '
                           'cantidades {limitadas} y carecer de capacidad de '
                           'reproducción; ejemplo: minerales, {petróleo}, '
                           'gas.',
                           'Los recursos naturales renovables no se acaban '
                           'con el aprovechamiento, aunque existan en '
                           'cantidades limitadas; ejemplo: el agua, el aire, '
                           'el {suelo}, la flora y la fauna.',
                           'Cuando el hombre aprovecha un recurso natural, '
                           'este se convierte en recurso {económico}, con '
                           'propietario individual.']},
                {'titulo': '11.2 RECURSOS POR REGIÓN',
                 'items': ['Del mar peruano se obtienen microorganismos, '
                           'peces como la {anchoveta}, cetáceos, moluscos y '
                           'aves guaneras como el guanay, piquero y '
                           '{alcatraz}.',
                           'En la costa se explota hierro en {Marcona}, y '
                           'fosfatos en Bayóvar, {Piura}.',
                           'En la región andina destacan minerales como el '
                           '{cobre}, plomo, zinc, oro y plata, además de '
                           'fauna como la {vicuña} y el cóndor.',
                           'En la selva se obtienen especies madereras, '
                           'petróleo, gas y {oro} aluvial.']},
                {'titulo': '11.3 ÁREAS NATURALES PROTEGIDAS',
                 'items': ['El {SERNANP} es el organismo adscrito al '
                           'Ministerio del Ambiente encargado de la '
                           'conservación de las Áreas Naturales Protegidas, '
                           'creado por el Decreto Legislativo {1013} del '
                           '2008.',
                           'Las Áreas Naturales Protegidas representan el '
                           '{15,41}% del territorio nacional.',
                           'Los {Parques Nacionales} son áreas de carácter '
                           'intangible donde solo se permite el turismo y la '
                           'investigación científica.',
                           'El parque nacional más pequeño y antiguo del '
                           'Perú es {Cutervo}, en Cajamarca.',
                           'El parque nacional más extenso del Perú es el '
                           '{Manu}, entre Cusco y Madre de Dios.']},
                {'titulo': '11.4 EXPLOSIÓN DEMOGRÁFICA',
                 'items': ['La {explosión demográfica} es un aumento súbito '
                           'de la cantidad de habitantes en una determinada '
                           'región, que satura los {servicios públicos}.',
                           'La explosión demográfica genera crecimiento de '
                           'los {cinturones de pobreza}, en las periferias '
                           'de las ciudades.',
                           'El mundo cuenta actualmente con unos {7450} '
                           'millones de habitantes; alcanzará los 9700 '
                           'millones en el {2050}.',
                           'Según la ONU, en pocos años la {India} superará '
                           'a China como el país más poblado del mundo.']},
                {'titulo': '11.5 DETERIORO DE LA CAPA DE OZONO: AGENTES',
                 'items': ['El {ozono} (O₃) es una molécula de tres átomos '
                           'de oxígeno, que absorbe los rayos {ultravioleta} '
                           'del Sol.',
                           'Los {clorofluorocarburos} (CFC) son compuestos '
                           'de cloro, flúor y carbono, usados como '
                           'refrigerantes y disolventes.',
                           'Los {halones}, compuestos de bromo, flúor y '
                           'carbono, se usan en extintores; su Br es más '
                           'efectivo destruyendo el ozono que el {cloro}.',
                           'El {bromuro de metilo} es un pesticida que, por '
                           'su contenido de bromo, daña la capa de ozono.']},
                {'titulo': '11.6 EFECTO INVERNADERO Y CALENTAMIENTO GLOBAL',
                 'items': ['Sin la presencia del CO₂ ni del vapor de agua, '
                           'la temperatura media de la Tierra sería del '
                           'orden de {18} °C bajo cero.',
                           'El {calentamiento global} es el aumento de la '
                           'temperatura media de los océanos y la atmósfera, '
                           'causado por emisiones que realzan el efecto '
                           'invernadero.',
                           'De 1880 al 2012, la temperatura media global ha '
                           'aumentado en {0,85} °C; el nivel del mar ha '
                           'subido 19 cm entre 1901 y 2010.']},
                {'titulo': '11.7 CAMBIO CLIMÁTICO Y VARIABILIDAD CLIMÁTICA',
                 'items': ['El {cambio climático} es la variación global del '
                           'clima, resultado de cambios en periodos de '
                           'cientos, miles o millones de {años}; sus causas '
                           'pueden ser naturales o {antropogénicas}.',
                           'La {variabilidad climática} es la variación de '
                           'los parámetros climáticos en cortos lapsos de '
                           'tiempo: días, semanas o algunos {meses}.',
                           'La {adaptación al cambio climático} son las '
                           'iniciativas para reducir la vulnerabilidad de la '
                           'sociedad ante los efectos del cambio climático, '
                           'según el {IPCC}.',
                           'La {pobreza}, más que cualquier otro factor, '
                           'determina la vulnerabilidad frente al cambio '
                           'climático.']}],
  'cuadros': [{'titulo': '11.1 TIPOS DE RECURSOS NATURALES',
               'encabezados': ['Tipo', 'Se agotan', 'Ejemplos'],
               'filas': [['{No renovables}',
                          '{Sí}',
                          'Minerales, petróleo, gas'],
                         ['{Renovables}',
                          '{No}',
                          'Agua, aire, suelo, flora, fauna']]}],
  'preguntas': [{'pregunta': 'Los recursos naturales son elementos que:',
                 'alternativas': ['Ofrece la naturaleza espontáneamente',
                                  'Crea el hombre artificialmente',
                                  'Provienen únicamente del mar',
                                  'Son producidos por la industria',
                                  'Solo existen en la costa'],
                 'correcta': 'A'},
                {'pregunta': 'Los recursos que se agotan con el '
                             'aprovechamiento del hombre son los:',
                 'alternativas': ['Marinos',
                                  'No renovables',
                                  'Forestales',
                                  'Hídricos',
                                  'Renovables'],
                 'correcta': 'B'},
                {'pregunta': 'El petróleo y el gas son recursos naturales:',
                 'alternativas': ['No renovables',
                                  'Renovables',
                                  'Ilimitados',
                                  'Inagotables',
                                  'Reciclables'],
                 'correcta': 'A'},
                {'pregunta': 'El agua, el aire y el suelo son recursos '
                             'naturales:',
                 'alternativas': ['Renovables',
                                  'Artificiales',
                                  'Prohibidos',
                                  'Escasos',
                                  'No renovables'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando el hombre aprovecha un recurso natural, '
                             'este se convierte en:',
                 'alternativas': ['Recurso económico',
                                  'Recurso prohibido',
                                  'Elemento sin valor',
                                  'Patrimonio intangible',
                                  'Bien público exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las aves guaneras del mar peruano '
                             'figuran el guanay, piquero y:',
                 'alternativas': ['Alcatraz',
                                  'Cóndor',
                                  'Zorzal',
                                  'Águila',
                                  'Gaviota andina'],
                 'correcta': 'A'},
                {'pregunta': 'El hierro se explota principalmente en la '
                             'localidad de:',
                 'alternativas': ['Marcona',
                                  'Bayóvar',
                                  'Cerro de Pasco',
                                  'Cajamarca',
                                  'Toquepala'],
                 'correcta': 'A'},
                {'pregunta': 'Los fosfatos como fertilizante se explotan en:',
                 'alternativas': ['Bayóvar, Piura',
                                  'Puno',
                                  'Cusco',
                                  'Marcona',
                                  'Arequipa'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los minerales de la región andina '
                             'figuran el cobre, plomo, zinc, oro y:',
                 'alternativas': ['Plata',
                                  'Petróleo',
                                  'Gas natural',
                                  'Carbón vegetal',
                                  'Sal'],
                 'correcta': 'A'},
                {'pregunta': 'La vicuña, el cóndor y la chinchilla son fauna '
                             'representativa de:',
                 'alternativas': ['La selva alta',
                                  'La selva baja',
                                  'La región andina',
                                  'La costa',
                                  'El mar peruano'],
                 'correcta': 'C'},
                {'pregunta': 'De la selva se obtiene, entre otros recursos, '
                             'oro:',
                 'alternativas': ['En vetas superficiales',
                                  'Aluvial',
                                  'Importado',
                                  'Solo en laboratorio',
                                  'Sintético'],
                 'correcta': 'B'},
                {'pregunta': 'El SERNANP está adscrito al Ministerio de:',
                 'alternativas': ['Cultura',
                                  'Agricultura',
                                  'Educación',
                                  'Energía y Minas',
                                  'Ambiente'],
                 'correcta': 'E'},
                {'pregunta': 'El SERNANP fue creado mediante el Decreto '
                             'Legislativo:',
                 'alternativas': ['997', '850', '1013', '713', '1090'],
                 'correcta': 'C'},
                {'pregunta': 'El SERNANP fue creado en el año:',
                 'alternativas': ['2008', '2015', '2020', '1990', '1998'],
                 'correcta': 'A'},
                {'pregunta': 'Las Áreas Naturales Protegidas representan del '
                             'territorio nacional:',
                 'alternativas': ['30%', '5%', '50%', '15,41%', '2%'],
                 'correcta': 'D'},
                {'pregunta': 'En los Parques Nacionales solo se permite:',
                 'alternativas': ['La tala de árboles',
                                  'La caza deportiva',
                                  'La minería y agricultura',
                                  'El turismo e investigación científica',
                                  'La ganadería extensiva'],
                 'correcta': 'D'},
                {'pregunta': 'El parque nacional más pequeño y antiguo del '
                             'Perú es:',
                 'alternativas': ['Cutervo',
                                  'Huascarán',
                                  'Bahuaja Sonene',
                                  'Manu',
                                  'Tingo María'],
                 'correcta': 'A'},
                {'pregunta': 'El parque nacional más extenso del Perú es:',
                 'alternativas': ['Cerros de Amotape',
                                  'Río Abiseo',
                                  'Cutervo',
                                  'Huascarán',
                                  'Manu'],
                 'correcta': 'E'},
                {'pregunta': 'El parque nacional Manu se ubica entre Cusco '
                             'y:',
                 'alternativas': ['Arequipa',
                                  'Apurímac',
                                  'Madre de Dios',
                                  'Puno',
                                  'Ayacucho'],
                 'correcta': 'C'},
                {'pregunta': 'El Parque Nacional Huascarán se ubica en el '
                             'departamento de:',
                 'alternativas': ['Cusco',
                                  'Áncash',
                                  'Puno',
                                  'Cajamarca',
                                  'Lima'],
                 'correcta': 'B'},
                {'pregunta': 'Satisfacer las necesidades del presente sin '
                             'comprometer los recursos de las futuras '
                             'generaciones corresponde al concepto de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['Riesgo de desastre',
                                  'Impacto ambiental',
                                  'Desarrollo sostenible',
                                  'Contaminación ambiental',
                                  'Desastre ecológico'],
                 'correcta': 'C'},
                {'pregunta': 'El aumento súbito de la cantidad de habitantes '
                             'en una determinada región, que satura los '
                             'servicios públicos, se llama:',
                 'alternativas': ['Urbanización',
                                  'Colonización',
                                  'Densificación',
                                  'Migración masiva',
                                  'Explosión demográfica'],
                 'correcta': 'E'},
                {'pregunta': 'La explosión demográfica genera crecimiento de '
                             'los cinturones de:',
                 'alternativas': ['Riqueza',
                                  'Comercio',
                                  'Educación',
                                  'Industria',
                                  'Pobreza'],
                 'correcta': 'E'},
                {'pregunta': 'Según proyecciones de la ONU, la población '
                             'mundial alcanzará los 9700 millones de '
                             'habitantes en el año:',
                 'alternativas': ['2200', '2030', '2100', '2025', '2050'],
                 'correcta': 'E'},
                {'pregunta': 'Según la ONU, en las próximas décadas, el país '
                             'que superará a China como el más poblado del '
                             'mundo será:',
                 'alternativas': ['Nigeria',
                                  'Estados Unidos',
                                  'Pakistán',
                                  'La India',
                                  'Indonesia'],
                 'correcta': 'D'},
                {'pregunta': 'El ozono, molécula formada de tres átomos de '
                             'oxígeno, tiene la función principal de '
                             'absorber los rayos:',
                 'alternativas': ['Ultravioleta',
                                  'X',
                                  'Cósmicos',
                                  'Gamma',
                                  'Infrarrojos'],
                 'correcta': 'A'},
                {'pregunta': 'Los compuestos formados por cloro, flúor y '
                             'carbono, usados como refrigerantes y '
                             'disolventes, que deterioran la capa de ozono, '
                             'se llaman:',
                 'alternativas': ['Óxidos de nitrógeno',
                                  'Halones',
                                  'Bromuro de metilo',
                                  'Clorofluorocarburos (CFC)',
                                  'Tetracloruro de carbono'],
                 'correcta': 'D'},
                {'pregunta': 'Los compuestos de bromo, flúor y carbono '
                             'usados en extintores, cuyo bromo es muy '
                             'efectivo destruyendo el ozono, se llaman:',
                 'alternativas': ['HCFC',
                                  'Bromuro de metilo',
                                  'Halones',
                                  'CFC',
                                  'Tetracloruro de carbono'],
                 'correcta': 'C'},
                {'pregunta': 'Sin la presencia del CO₂ ni del vapor de agua '
                             'en la atmósfera, la temperatura media de la '
                             'Tierra sería del orden de:',
                 'alternativas': ['18°C bajo cero',
                                  '0°C',
                                  '10°C',
                                  '5°C',
                                  '50°C bajo cero'],
                 'correcta': 'A'},
                {'pregunta': 'El aumento de la temperatura media de los '
                             'océanos y la atmósfera de la Tierra, causado '
                             'por emisiones que realzan el efecto '
                             'invernadero, se llama:',
                 'alternativas': ['Cambio climático exclusivamente',
                                  'Calentamiento global',
                                  'Adaptación climática',
                                  'Efecto invernadero natural',
                                  'Variabilidad climática'],
                 'correcta': 'B'},
                {'pregunta': 'De 1880 al 2012, la temperatura media global '
                             'de la Tierra ha aumentado aproximadamente en:',
                 'alternativas': ['2°C', '5°C', '1,5°C', '3°C', '0,85°C'],
                 'correcta': 'E'},
                {'pregunta': 'La variación global del clima de la Tierra, '
                             'resultado de cambios en periodos de cientos, '
                             'miles o millones de años, se llama:',
                 'alternativas': ['Variabilidad climática',
                                  'Efecto invernadero',
                                  'Calentamiento local',
                                  'Microclima',
                                  'Cambio climático'],
                 'correcta': 'E'},
                {'pregunta': 'La variación de los parámetros climáticos en '
                             'cortos lapsos de tiempo, como días, semanas o '
                             'meses, se llama:',
                 'alternativas': ['Adaptación climática',
                                  'Efecto invernadero',
                                  'Cambio climático',
                                  'Calentamiento global',
                                  'Variabilidad climática'],
                 'correcta': 'E'},
                {'pregunta': 'Las iniciativas y medidas encaminadas a '
                             'reducir la vulnerabilidad de la sociedad ante '
                             'los efectos del cambio climático se llaman:',
                 'alternativas': ['Reforestación exclusiva',
                                  'Prevención exclusiva',
                                  'Mitigación exclusiva',
                                  'Resiliencia exclusiva',
                                  'Adaptación al cambio climático'],
                 'correcta': 'E'},
                {'pregunta': 'Según el texto, el factor que más que '
                             'cualquier otro determina la vulnerabilidad '
                             'frente al cambio climático es:',
                 'alternativas': ['La pobreza',
                                  'La ubicación geográfica exclusiva',
                                  'La edad',
                                  'El género exclusivo',
                                  'La educación'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y CLASIFICACIÓN',
                      'items': ['Los recursos naturales son elementos que la '
                                'naturaleza ofrece espontáneamente para '
                                'satisfacer las necesidades del hombre.',
                                'Los recursos naturales no renovables se '
                                'agotan con el aprovechamiento, por existir '
                                'en cantidades limitadas y carecer de '
                                'capacidad de reproducción; ejemplo: '
                                'minerales, petróleo, gas.',
                                'Los recursos naturales renovables no se '
                                'acaban con el aprovechamiento, aunque '
                                'existan en cantidades limitadas; ejemplo: '
                                'el agua, el aire, el suelo, la flora y la '
                                'fauna.',
                                'Cuando el hombre aprovecha un recurso '
                                'natural, este se convierte en recurso '
                                'económico, con propietario individual.']},
                     {'titulo': 'RECURSOS POR REGIÓN',
                      'items': ['Del mar peruano se obtienen '
                                'microorganismos, peces como la anchoveta, '
                                'cetáceos, moluscos y aves guaneras como el '
                                'guanay, piquero y alcatraz.',
                                'En la costa se explota hierro en Marcona, y '
                                'fosfatos en Bayóvar, Piura.',
                                'En la región andina destacan minerales como '
                                'el cobre, plomo, zinc, oro y plata, además '
                                'de fauna como la vicuña y el cóndor.',
                                'En la selva se obtienen especies madereras, '
                                'petróleo, gas y oro aluvial.']},
                     {'titulo': 'ÁREAS NATURALES PROTEGIDAS',
                      'items': ['El SERNANP es el organismo adscrito al '
                                'Ministerio del Ambiente encargado de la '
                                'conservación de las Áreas Naturales '
                                'Protegidas, creado por el Decreto '
                                'Legislativo 1013 del 2008.',
                                'Las Áreas Naturales Protegidas representan '
                                'el 15,41% del territorio nacional.',
                                'Los Parques Nacionales son áreas de '
                                'carácter intangible donde solo se permite '
                                'el turismo y la investigación científica.',
                                'El parque nacional más pequeño y antiguo '
                                'del Perú es Cutervo, en Cajamarca.',
                                'El parque nacional más extenso del Perú es '
                                'el Manu, entre Cusco y Madre de Dios.']},
                     {'titulo': 'EXPLOSIÓN DEMOGRÁFICA',
                      'items': ['La explosión demográfica es un aumento '
                                'súbito de la cantidad de habitantes en una '
                                'determinada región, que satura los '
                                'servicios públicos.',
                                'La explosión demográfica genera crecimiento '
                                'de los cinturones de pobreza, en las '
                                'periferias de las ciudades.',
                                'El mundo cuenta actualmente con unos 7450 '
                                'millones de habitantes; alcanzará los 9700 '
                                'millones en el 2050.',
                                'Según la ONU, en pocos años la India '
                                'superará a China como el país más poblado '
                                'del mundo.']},
                     {'titulo': 'DETERIORO DE LA CAPA DE OZONO: AGENTES',
                      'items': ['El ozono (O₃) es una molécula de tres '
                                'átomos de oxígeno, que absorbe los rayos '
                                'ultravioleta del Sol.',
                                'Los clorofluorocarburos (CFC) son '
                                'compuestos de cloro, flúor y carbono, '
                                'usados como refrigerantes y disolventes.',
                                'Los halones, compuestos de bromo, flúor y '
                                'carbono, se usan en extintores; su Br es '
                                'más efectivo destruyendo el ozono que el '
                                'cloro.',
                                'El bromuro de metilo es un pesticida que, '
                                'por su contenido de bromo, daña la capa de '
                                'ozono.']},
                     {'titulo': 'EFECTO INVERNADERO Y CALENTAMIENTO GLOBAL',
                      'items': ['Sin la presencia del CO₂ ni del vapor de '
                                'agua, la temperatura media de la Tierra '
                                'sería del orden de 18 °C bajo cero.',
                                'El calentamiento global es el aumento de la '
                                'temperatura media de los océanos y la '
                                'atmósfera, causado por emisiones que '
                                'realzan el efecto invernadero.',
                                'De 1880 al 2012, la temperatura media '
                                'global ha aumentado en 0,85 °C; el nivel '
                                'del mar ha subido 19 cm entre 1901 y '
                                '2010.']},
                     {'titulo': 'CAMBIO CLIMÁTICO Y VARIABILIDAD CLIMÁTICA',
                      'items': ['El cambio climático es la variación global '
                                'del clima, resultado de cambios en periodos '
                                'de cientos, miles o millones de años; sus '
                                'causas pueden ser naturales o '
                                'antropogénicas.',
                                'La variabilidad climática es la variación '
                                'de los parámetros climáticos en cortos '
                                'lapsos de tiempo: días, semanas o algunos '
                                'meses.',
                                'La adaptación al cambio climático son las '
                                'iniciativas para reducir la vulnerabilidad '
                                'de la sociedad ante los efectos del cambio '
                                'climático, según el IPCC.',
                                'La pobreza, más que cualquier otro factor, '
                                'determina la vulnerabilidad frente al '
                                'cambio climático.']}],
  'qr_reto': [{'pregunta': 'Los compuestos formados por cloro, flúor y '
                           'carbono, usados como refrigerantes y '
                           'disolventes, que deterioran la capa de ozono, se '
                           'llaman:',
               'respuesta': 'Clorofluorocarburos (CFC)'},
              {'pregunta': 'Cuando el hombre aprovecha un recurso natural, '
                           'este se convierte en:',
               'respuesta': 'Recurso económico'},
              {'pregunta': 'Los fosfatos como fertilizante se explotan en:',
               'respuesta': 'Bayóvar, Piura'}],
  'qr_dato': 'El calentamiento global es el aumento de la temperatura media '
             'de los océanos y la atmósfera, causado por emisiones que '
             'realzan el efecto invernadero.'},
 {'num': 12,
  'titulo': 'Riesgo de Desastres en el Perú',
  'secciones': [{'titulo': '12.1 EL SINAGERD',
                 'items': ['El Sistema Nacional de Gestión del Riesgo de '
                           'Desastres, {SINAGERD}, fue creado por la Ley N° '
                           '{29664}.',
                           'El SINAGERD es un sistema interinstitucional, '
                           'sinérgico, {descentralizado}, transversal y '
                           'participativo.',
                           'La Política Nacional de Gestión del Riesgo de '
                           'Desastres fue aprobada como de obligatorio '
                           'cumplimiento por el Decreto Supremo N° '
                           '{111-2012-PCM}.',
                           'Entre los objetivos de la política nacional '
                           'figura fortalecer la cultura de {prevención}.']},
                {'titulo': '12.2 CONCEPTOS BÁSICOS: FENÓMENO, DESASTRE Y '
                           'RIESGO',
                 'items': ['Un {fenómeno natural} es una manifestación '
                           'espontánea de la naturaleza que no '
                           'necesariamente representa una amenaza para el '
                           'hombre.',
                           'Un {desastre} ocurre cuando se altera o '
                           'interrumpe intensamente la vida cotidiana de una '
                           'comunidad.',
                           'El {riesgo} es la probabilidad de que ocurra un '
                           'desastre, y se calcula como amenaza multiplicada '
                           'por {vulnerabilidad}.',
                           'No puede haber riesgo sin {amenaza} y tampoco '
                           'sin {vulnerabilidad}.']},
                {'titulo': '12.3 AMENAZA Y VULNERABILIDAD',
                 'items': ['La {amenaza} es la probabilidad de que ocurra un '
                           'fenómeno natural o causado por el hombre que '
                           'puede poner en peligro a un grupo de personas.',
                           'Las amenazas {naturales} son las originadas por '
                           'la naturaleza misma, como los movimientos '
                           'sísmicos.',
                           'La {vulnerabilidad} depende, entre otros '
                           'factores, de la ubicación de la vivienda y la '
                           'organización de la población.']},
                {'titulo': '12.4 MOVIMIENTOS SÍSMICOS: CONCEPTOS BÁSICOS',
                 'items': ['Los {movimientos sísmicos} son vibraciones de la '
                           'corteza terrestre; la {sismología} es la rama de '
                           'la geofísica que los estudia.',
                           'El {sismógrafo} es el aparato capaz de detectar '
                           'las vibraciones más leves de la Tierra.',
                           'El {hipocentro} o foco es el punto en la '
                           'profundidad de la Tierra desde donde se libera '
                           'la energía sísmica.',
                           'El {epicentro} es el punto en la superficie '
                           'terrestre directamente sobre el hipocentro, '
                           'donde el movimiento es {mayor}.',
                           'Una {falla} es una fractura en la corteza '
                           'terrestre donde las rocas se han desplazado; '
                           'puede ser {activa} (con desplazamientos en el '
                           'Cuaternario) o inactiva.']},
                {'titulo': '12.5 ESCALAS DE MEDICIÓN: RICHTER Y MERCALLI',
                 'items': ['La escala de {Richter} fue desarrollada por '
                           'Charles Richter y Beno Gutenberg en {1935}; mide '
                           'la magnitud o energía sísmica liberada, según el '
                           'registro sismográfico.',
                           'El mayor sismo registrado, en {Valdivia}, Chile '
                           '(1960), alcanzó una magnitud de {9,5}.',
                           'La escala de {Mercalli}, creada en 1902 por '
                           'Giuseppe Mercalli, mide la {intensidad}: el '
                           'efecto o daño producido en un lugar determinado.',
                           'La escala de Mercalli no se basa en registros '
                           'sismográficos sino en {entrevistas}, registros '
                           'históricos y noticias; se expresa en números '
                           '{romanos}.']},
                {'titulo': '12.6 VULCANISMO Y TSUNAMIS',
                 'items': ['Las {erupciones volcánicas} son el '
                           'desplazamiento violento de lava o magma desde el '
                           'manto hacia el exterior.',
                           'Un {tsunami} o maremoto son olas enormes '
                           'originadas generalmente por un movimiento '
                           'sísmico submarino; pueden desplazarse a '
                           '{500}-1000 km/h.',
                           'Los tsunamis ocurren sobre todo en el {océano '
                           'Pacífico}, propiciados por fallas de subducción '
                           'como la de las placas de Nazca y Sudamericana.',
                           'El tsunami de {1960} viajó desde Chile hasta '
                           'Hawái en 15 horas y a Japón en 22 horas.']},
                {'titulo': '12.7 PELIGROS DE GEODINÁMICA EXTERNA',
                 'items': ['El {deslizamiento} de tierras es el '
                           'desplazamiento de masa de tierra en una '
                           'pendiente, súbito o lento, por inestabilidad de '
                           'un {talud}.',
                           'El {derrumbe} es la caída o desmoronamiento de '
                           'una estructura natural o artificial que se ha '
                           'desprendido de su lugar de origen.',
                           'El {aluvión} es un flujo de gran volumen de '
                           'hielo, nieve, agua y lodo a gran velocidad, '
                           'generalmente tras intensas {lluvias} o deshielo.',
                           'El {alud} o avalancha es una gran masa de nieve '
                           'que se desplaza ladera abajo, con velocidad '
                           'entre {50} y 300 km/h.',
                           'El {golpe de agua} o Loclla (en quechua), mal '
                           'llamado «huayco», es el desprendimiento de lodo '
                           'y rocas por saturación de agua en el suelo.']},
                {'titulo': '12.8 PELIGROS HIDROMETEOROLÓGICOS',
                 'items': ['La {sequía} es la deficiencia de humedad en la '
                           'atmósfera por precipitaciones irregulares o '
                           'insuficientes.',
                           'La {helada} es el excesivo descenso de la '
                           'temperatura, causando daño a plantas y animales.',
                           'Las {tormentas} son fenómenos atmosféricos '
                           'producidos por descargas {eléctricas} en la '
                           'atmósfera.',
                           'Los {huracanes} son vientos que sobrepasan los '
                           '24 km/h por la interacción de aire caliente y '
                           'húmedo del océano con aire {frío}.',
                           'La {inundación} es la invasión lenta o violenta '
                           'de aguas de río, lagunas o lagos, por fuertes '
                           'precipitaciones o ruptura de embalses.']},
                {'titulo': '12.9 PELIGROS DE ORIGEN BIOLÓGICO Y TECNOLÓGICO',
                 'items': ['Una {plaga} es una situación en la que un animal '
                           'produce daños económicos a intereses de las '
                           'personas.',
                           'Una {epidemia} es el aumento extraordinario del '
                           'número de casos de una enfermedad infecciosa ya '
                           'existente en una región.',
                           'Un {incendio} es una ocurrencia de fuego no '
                           'controlada que puede afectar estructuras y seres '
                           'vivos.']},
                {'titulo': '12.10 INDECI Y DEFENSA CIVIL',
                 'items': ['El {INDECI} (Instituto Nacional de Defensa '
                           'Civil) es un organismo público ejecutor que '
                           'conforma el {SINAGERD}.',
                           'El INDECI es responsable de coordinar la '
                           'Política y el Plan Nacional de Gestión del '
                           'Riesgo de Desastres, en preparación, {respuesta} '
                           'y rehabilitación.',
                           'La {Defensa Civil} es el conjunto de medidas '
                           'permanentes destinadas a prevenir, reducir '
                           'riesgos y reparar daños causados por desastres.',
                           'El {Comité de Defensa Civil Regional} es '
                           'presidido por el Presidente del Gobierno '
                           'Regional.',
                           'El {Comité de Defensa Civil Provincial} es '
                           'presidido por el Alcalde Provincial; el '
                           'Distrital, por el Alcalde {Distrital}.',
                           'El {brigadista} es la persona entre 16 y 40 años '
                           'que, de forma voluntaria, conforma la Brigada de '
                           'Defensa Civil.']}],
  'cuadros': [{'titulo': '12.2 FÓRMULA DEL RIESGO',
               'encabezados': ['Elemento', 'Definición'],
               'filas': [['{Riesgo}', '{Amenaza} × Vulnerabilidad'],
                         ['{Amenaza}',
                          'Probabilidad de un fenómeno {dañino}'],
                         ['{Vulnerabilidad}',
                          'Susceptibilidad de sufrir {daño}']]}],
  'preguntas': [{'pregunta': 'El SINAGERD fue creado mediante la Ley N°:',
                 'alternativas': ['28044',
                                  '29664',
                                  '30220',
                                  '29338',
                                  '27444'],
                 'correcta': 'B'},
                {'pregunta': 'El SINAGERD se caracteriza por ser un sistema:',
                 'alternativas': ['Solo consultivo',
                                  'Exclusivamente militar',
                                  'Interinstitucional, descentralizado y '
                                  'participativo',
                                  'Centralizado y vertical',
                                  'Sin participación ciudadana'],
                 'correcta': 'C'},
                {'pregunta': 'La Política Nacional de Gestión del Riesgo de '
                             'Desastres fue aprobada mediante:',
                 'alternativas': ['Una ordenanza municipal',
                                  'Una resolución ministerial',
                                  'Una ley del Congreso',
                                  'El Decreto Supremo N° 111-2012-PCM',
                                  'Un decreto legislativo'],
                 'correcta': 'D'},
                {'pregunta': 'Un fenómeno natural que ocurre en una zona '
                             'despoblada:',
                 'alternativas': ['Se clasifica como vulnerabilidad',
                                  'No representa necesariamente una amenaza',
                                  'Siempre es un desastre',
                                  'Requiere evacuación inmediata',
                                  'Es automáticamente un riesgo alto'],
                 'correcta': 'B'},
                {'pregunta': 'Un desastre se produce cuando:',
                 'alternativas': ['El fenómeno es predecible',
                                  'Ocurre un fenómeno en zona despoblada',
                                  'Se altera intensamente la vida cotidiana '
                                  'de una comunidad',
                                  'Solo hay pérdidas económicas menores',
                                  'No hay ningún efecto adverso'],
                 'correcta': 'C'},
                {'pregunta': 'El riesgo se calcula mediante la fórmula:',
                 'alternativas': ['Amenaza × Vulnerabilidad',
                                  'Vulnerabilidad ÷ Amenaza',
                                  'Amenaza ÷ Vulnerabilidad',
                                  'Amenaza + Vulnerabilidad',
                                  'Amenaza − Vulnerabilidad'],
                 'correcta': 'A'},
                {'pregunta': 'Para que exista riesgo se requiere la '
                             'presencia de:',
                 'alternativas': ['Amenaza y vulnerabilidad juntas',
                                  'Ningún factor en particular',
                                  'Solo fenómenos naturales extremos',
                                  'Solo la vulnerabilidad',
                                  'Solo la amenaza'],
                 'correcta': 'A'},
                {'pregunta': 'La amenaza se define como la probabilidad de '
                             'que ocurra:',
                 'alternativas': ['Una política pública',
                                  'Una vulnerabilidad social',
                                  'Un desastre ya consumado',
                                  'Un cambio climático',
                                  'Un fenómeno que pueda poner en peligro a '
                                  'las personas'],
                 'correcta': 'E'},
                {'pregunta': 'Las amenazas naturales se originan por:',
                 'alternativas': ['Decisiones políticas',
                                  'Fallas de infraestructura',
                                  'La naturaleza misma',
                                  'Acción humana exclusivamente',
                                  'El comercio internacional'],
                 'correcta': 'C'},
                {'pregunta': 'La vulnerabilidad depende, entre otros '
                             'factores, de:',
                 'alternativas': ['Solo el clima',
                                  'Solo la economía nacional',
                                  'Solo la edad de la población',
                                  'Solo el idioma',
                                  'La ubicación y tipo de vivienda'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los objetivos de la política nacional de '
                             'gestión del riesgo figura:',
                 'alternativas': ['Aumentar la vulnerabilidad',
                                  'Evitar toda construcción',
                                  'Eliminar los fenómenos naturales',
                                  'Prohibir la habitación en zonas de riesgo',
                                  'Fortalecer la cultura de prevención'],
                 'correcta': 'E'},
                {'pregunta': 'Un terremoto en un área no poblada es un '
                             'ejemplo de:',
                 'alternativas': ['Catástrofe social',
                                  'Desastre',
                                  'Vulnerabilidad extrema',
                                  'Fenómeno natural sin amenaza directa',
                                  'Riesgo alto'],
                 'correcta': 'D'},
                {'pregunta': 'El riesgo representa la proximidad de:',
                 'alternativas': ['Un daño potencial',
                                  'Una política pública exitosa',
                                  'Un fenómeno inexistente',
                                  'Una mejora económica',
                                  'Un evento positivo'],
                 'correcta': 'A'},
                {'pregunta': 'Sin vulnerabilidad, una amenaza:',
                 'alternativas': ['No representa un riesgo por sí sola',
                                  'Aumenta exponencialmente',
                                  'Genera un desastre igual',
                                  'Se convierte en catástrofe automática',
                                  'Es imposible de medir'],
                 'correcta': 'A'},
                {'pregunta': 'El SINAGERD busca capacitar a los componentes '
                             'del sistema para:',
                 'alternativas': ['Eliminar la participación privada',
                                  'La toma de decisiones',
                                  'Centralizar el poder',
                                  'Reducir el presupuesto público',
                                  'Evitar toda capacitación'],
                 'correcta': 'B'},
                {'pregunta': 'Los fenómenos naturales pueden ser de orden '
                             'climatológico, hidrológico o:',
                 'alternativas': ['Educativo',
                                  'Geológico',
                                  'Económico',
                                  'Cultural',
                                  'Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'El SINAGERD tiene un carácter, entre otros, '
                             'transversal y:',
                 'alternativas': ['Temporal',
                                  'Unipersonal',
                                  'Participativo',
                                  'Exclusivo',
                                  'Cerrado'],
                 'correcta': 'C'},
                {'pregunta': 'El cálculo del riesgo puede incluir el número '
                             'de:',
                 'alternativas': ['Solo vehículos en circulación',
                                  'Posibles vidas expuestas y viviendas que '
                                  'pueden perderse',
                                  'Solo empresas afectadas',
                                  'Solo funcionarios públicos',
                                  'Solo turistas en la zona'],
                 'correcta': 'B'},
                {'pregunta': 'Una inundación en un lugar deshabitado se '
                             'considera:',
                 'alternativas': ['Un fenómeno natural, no una amenaza '
                                  'directa',
                                  'Un desastre mayor',
                                  'Una vulnerabilidad social',
                                  'Un riesgo alto para la población',
                                  'Una catástrofe económica'],
                 'correcta': 'A'},
                {'pregunta': 'La gestión del riesgo de desastres busca '
                             'minimizar los efectos adversos sobre:',
                 'alternativas': ['Solo la economía',
                                  'Solo la infraestructura vial',
                                  'Solo el turismo',
                                  'La población, la economía y el ambiente',
                                  'Solo el ambiente'],
                 'correcta': 'D'},
                {'pregunta': 'El brote de una enfermedad infectocontagiosa '
                             'que aparece en forma masiva en una región se '
                             'denomina: (II CEPRU 2025)',
                 'alternativas': ['Pandemia',
                                  'Endemia',
                                  'Epidemia',
                                  'Calamidad',
                                  'Plaga'],
                 'correcta': 'C'},
                {'pregunta': 'La autoridad que preside el Comité de Defensa '
                             'Civil Regional es: (II CEPRU 2024)',
                 'alternativas': ['Alcalde Provincial',
                                  'Teniente Alcalde',
                                  'Concejo Municipal',
                                  'Gobernador Regional',
                                  'Consejo Regional'],
                 'correcta': 'D'},
                {'pregunta': 'El punto en la profundidad de la Tierra desde '
                             'donde se libera la energía en un movimiento '
                             'sísmico se llama:',
                 'alternativas': ['Talweg',
                                  'Hipocentro o foco',
                                  'Epicentro',
                                  'Sismógrafo',
                                  'Falla'],
                 'correcta': 'B'},
                {'pregunta': 'El punto en la superficie terrestre '
                             'directamente sobre el hipocentro, donde el '
                             'movimiento sísmico es mayor, se llama:',
                 'alternativas': ['Epicentro',
                                  'Terremoto',
                                  'Falla activa',
                                  'Talweg',
                                  'Hipocentro'],
                 'correcta': 'A'},
                {'pregunta': 'Una fractura en la corteza terrestre donde las '
                             'rocas se han desplazado, con actividad durante '
                             'el Cuaternario, se llama falla:',
                 'alternativas': ['Tectónica exclusiva',
                                  'Sísmica exclusiva',
                                  'Activa',
                                  'Geológica exclusiva',
                                  'Inactiva'],
                 'correcta': 'C'},
                {'pregunta': 'La escala que mide la magnitud o energía '
                             'sísmica liberada, desarrollada por Charles '
                             'Richter en 1935, se llama escala de:',
                 'alternativas': ['Richter',
                                  'Mercalli',
                                  'Beaufort',
                                  'Saffir-Simpson',
                                  'Fujita'],
                 'correcta': 'A'},
                {'pregunta': 'La escala que mide la intensidad de un sismo, '
                             'es decir el efecto o daño producido en un '
                             'lugar, creada por Giuseppe Mercalli en 1902, '
                             'se llama escala de:',
                 'alternativas': ['Richter',
                                  'Beaufort',
                                  'Mercalli',
                                  'Fujita',
                                  'Saffir-Simpson'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia de la escala de Richter, la '
                             'escala de Mercalli se expresa en:',
                 'alternativas': ['Números decimales',
                                  'Porcentajes',
                                  'Letras',
                                  'Números romanos',
                                  'Fracciones'],
                 'correcta': 'D'},
                {'pregunta': 'Un maremoto u ola enorme originada '
                             'generalmente por un movimiento sísmico '
                             'submarino se llama:',
                 'alternativas': ['Corriente marina',
                                  'Oleaje',
                                  'Resaca',
                                  'Tsunami',
                                  'Marejada'],
                 'correcta': 'D'},
                {'pregunta': 'El desprendimiento de lodo, rocas y todo lo '
                             'que encuentra a su paso, mal llamado «huayco», '
                             'se denomina correctamente, en quechua:',
                 'alternativas': ['Aluvión',
                                  'Deslizamiento',
                                  'Derrumbe',
                                  'Golpe de agua o Loclla',
                                  'Alud'],
                 'correcta': 'D'},
                {'pregunta': 'El flujo de gran volumen de hielo, nieve, agua '
                             'y lodo que se desplaza a gran velocidad tras '
                             'intensas lluvias o deshielo se llama:',
                 'alternativas': ['Sequía',
                                  'Derrumbe',
                                  'Deslizamiento',
                                  'Alud',
                                  'Aluvión'],
                 'correcta': 'E'},
                {'pregunta': 'La gran masa de nieve que se desplaza ladera '
                             'abajo, también llamada avalancha, se llama:',
                 'alternativas': ['Deslizamiento',
                                  'Aluvión',
                                  'Golpe de agua',
                                  'Alud',
                                  'Derrumbe'],
                 'correcta': 'D'},
                {'pregunta': 'La deficiencia de humedad en la atmósfera por '
                             'precipitaciones irregulares o insuficientes se '
                             'llama:',
                 'alternativas': ['Tormenta',
                                  'Inundación',
                                  'Helada',
                                  'Granizada',
                                  'Sequía'],
                 'correcta': 'E'},
                {'pregunta': 'El excesivo descenso de la temperatura que '
                             'causa daño a plantas y animales se llama:',
                 'alternativas': ['Huracán',
                                  'Sequía',
                                  'Helada',
                                  'Tornado',
                                  'Granizada'],
                 'correcta': 'C'},
                {'pregunta': 'Una situación en la que un animal produce '
                             'daños económicos a intereses de las personas '
                             'se llama:',
                 'alternativas': ['Plaga',
                                  'Endemia',
                                  'Pandemia',
                                  'Epidemia',
                                  'Incendio'],
                 'correcta': 'A'},
                {'pregunta': 'El aumento extraordinario del número de casos '
                             'de una enfermedad infecciosa ya existente en '
                             'una región se llama:',
                 'alternativas': ['Brote controlado',
                                  'Pandemia exclusiva',
                                  'Plaga',
                                  'Endemia exclusiva',
                                  'Epidemia'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo público ejecutor que conforma el '
                             'SINAGERD, responsable de la Política Nacional '
                             'de Gestión del Riesgo de Desastres, se llama:',
                 'alternativas': ['Cruz Roja',
                                  'SINADECI exclusivamente',
                                  'Bomberos',
                                  'Defensa Civil exclusivamente',
                                  'INDECI'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto de medidas permanentes destinadas '
                             'a prevenir, reducir riesgos y reparar daños '
                             'causados por desastres se llama:',
                 'alternativas': ['Gestión de Riesgos exclusiva',
                                  'SINAGERD exclusivamente',
                                  'COEN',
                                  'Defensa Civil',
                                  'INDECI exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'El Comité de Defensa Civil Regional es '
                             'presidido por el:',
                 'alternativas': ['Presidente del Gobierno Regional',
                                  'Prefecto',
                                  'Alcalde Distrital',
                                  'Alcalde Provincial',
                                  'Congresista Regional'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'EL SINAGERD / CONCEPTOS BÁSICOS: FENÓMENO, '
                                'DESASTRE Y RIESGO',
                      'items': ['El Sistema Nacional de Gestión del Riesgo '
                                'de Desastres, SINAGERD, fue creado por la '
                                'Ley N° 29664.',
                                'El SINAGERD es un sistema '
                                'interinstitucional, sinérgico, '
                                'descentralizado, transversal y '
                                'participativo.',
                                'La Política Nacional de Gestión del Riesgo '
                                'de Desastres fue aprobada como de '
                                'obligatorio cumplimiento por el Decreto '
                                'Supremo N° 111-2012-PCM.',
                                'Entre los objetivos de la política nacional '
                                'figura fortalecer la cultura de prevención.',
                                'Un fenómeno natural es una manifestación '
                                'espontánea de la naturaleza que no '
                                'necesariamente representa una amenaza para '
                                'el hombre.',
                                'Un desastre ocurre cuando se altera o '
                                'interrumpe intensamente la vida cotidiana '
                                'de una comunidad.',
                                'El riesgo es la probabilidad de que ocurra '
                                'un desastre, y se calcula como amenaza '
                                'multiplicada por vulnerabilidad.',
                                'No puede haber riesgo sin amenaza y tampoco '
                                'sin vulnerabilidad.']},
                     {'titulo': 'AMENAZA Y VULNERABILIDAD / MOVIMIENTOS '
                                'SÍSMICOS: CONCEPTOS BÁSICOS',
                      'items': ['La amenaza es la probabilidad de que ocurra '
                                'un fenómeno natural o causado por el hombre '
                                'que puede poner en peligro a un grupo de '
                                'personas.',
                                'Las amenazas naturales son las originadas '
                                'por la naturaleza misma, como los '
                                'movimientos sísmicos.',
                                'La vulnerabilidad depende, entre otros '
                                'factores, de la ubicación de la vivienda y '
                                'la organización de la población.',
                                'Los movimientos sísmicos son vibraciones de '
                                'la corteza terrestre; la sismología es la '
                                'rama de la geofísica que los estudia.',
                                'El sismógrafo es el aparato capaz de '
                                'detectar las vibraciones más leves de la '
                                'Tierra.',
                                'El hipocentro o foco es el punto en la '
                                'profundidad de la Tierra desde donde se '
                                'libera la energía sísmica.',
                                'El epicentro es el punto en la superficie '
                                'terrestre directamente sobre el hipocentro, '
                                'donde el movimiento es mayor.',
                                'Una falla es una fractura en la corteza '
                                'terrestre donde las rocas se han '
                                'desplazado; puede ser activa (con '
                                'desplazamientos en el Cuaternario) o '
                                'inactiva.']},
                     {'titulo': 'ESCALAS DE MEDICIÓN: RICHTER Y MERCALLI / '
                                'VULCANISMO Y TSUNAMIS',
                      'items': ['La escala de Richter fue desarrollada por '
                                'Charles Richter y Beno Gutenberg en 1935; '
                                'mide la magnitud o energía sísmica '
                                'liberada, según el registro sismográfico.',
                                'El mayor sismo registrado, en Valdivia, '
                                'Chile (1960), alcanzó una magnitud de 9,5.',
                                'La escala de Mercalli, creada en 1902 por '
                                'Giuseppe Mercalli, mide la intensidad: el '
                                'efecto o daño producido en un lugar '
                                'determinado.',
                                'La escala de Mercalli no se basa en '
                                'registros sismográficos sino en '
                                'entrevistas, registros históricos y '
                                'noticias; se expresa en números romanos.',
                                'Las erupciones volcánicas son el '
                                'desplazamiento violento de lava o magma '
                                'desde el manto hacia el exterior.',
                                'Un tsunami o maremoto son olas enormes '
                                'originadas generalmente por un movimiento '
                                'sísmico submarino; pueden desplazarse a '
                                '500-1000 km/h.',
                                'Los tsunamis ocurren sobre todo en el '
                                'océano Pacífico, propiciados por fallas de '
                                'subducción como la de las placas de Nazca y '
                                'Sudamericana.',
                                'El tsunami de 1960 viajó desde Chile hasta '
                                'Hawái en 15 horas y a Japón en 22 horas.']},
                     {'titulo': 'PELIGROS DE GEODINÁMICA EXTERNA / PELIGROS '
                                'HIDROMETEOROLÓGICOS',
                      'items': ['El deslizamiento de tierras es el '
                                'desplazamiento de masa de tierra en una '
                                'pendiente, súbito o lento, por '
                                'inestabilidad de un talud.',
                                'El derrumbe es la caída o desmoronamiento '
                                'de una estructura natural o artificial que '
                                'se ha desprendido de su lugar de origen.',
                                'El aluvión es un flujo de gran volumen de '
                                'hielo, nieve, agua y lodo a gran velocidad, '
                                'generalmente tras intensas lluvias o '
                                'deshielo.',
                                'El alud o avalancha es una gran masa de '
                                'nieve que se desplaza ladera abajo, con '
                                'velocidad entre 50 y 300 km/h.',
                                'El golpe de agua o Loclla (en quechua), mal '
                                'llamado «huayco», es el desprendimiento de '
                                'lodo y rocas por saturación de agua en el '
                                'suelo.',
                                'La sequía es la deficiencia de humedad en '
                                'la atmósfera por precipitaciones '
                                'irregulares o insuficientes.',
                                'La helada es el excesivo descenso de la '
                                'temperatura, causando daño a plantas y '
                                'animales.',
                                'Las tormentas son fenómenos atmosféricos '
                                'producidos por descargas eléctricas en la '
                                'atmósfera.',
                                'Los huracanes son vientos que sobrepasan '
                                'los 24 km/h por la interacción de aire '
                                'caliente y húmedo del océano con aire frío.',
                                'La inundación es la invasión lenta o '
                                'violenta de aguas de río, lagunas o lagos, '
                                'por fuertes precipitaciones o ruptura de '
                                'embalses.']},
                     {'titulo': 'PELIGROS DE ORIGEN BIOLÓGICO Y TECNOLÓGICO '
                                '/ INDECI Y DEFENSA CIVIL',
                      'items': ['Una plaga es una situación en la que un '
                                'animal produce daños económicos a intereses '
                                'de las personas.',
                                'Una epidemia es el aumento extraordinario '
                                'del número de casos de una enfermedad '
                                'infecciosa ya existente en una región.',
                                'Un incendio es una ocurrencia de fuego no '
                                'controlada que puede afectar estructuras y '
                                'seres vivos.',
                                'El INDECI (Instituto Nacional de Defensa '
                                'Civil) es un organismo público ejecutor que '
                                'conforma el SINAGERD.',
                                'El INDECI es responsable de coordinar la '
                                'Política y el Plan Nacional de Gestión del '
                                'Riesgo de Desastres, en preparación, '
                                'respuesta y rehabilitación.',
                                'La Defensa Civil es el conjunto de medidas '
                                'permanentes destinadas a prevenir, reducir '
                                'riesgos y reparar daños causados por '
                                'desastres.',
                                'El Comité de Defensa Civil Regional es '
                                'presidido por el Presidente del Gobierno '
                                'Regional.',
                                'El Comité de Defensa Civil Provincial es '
                                'presidido por el Alcalde Provincial; el '
                                'Distrital, por el Alcalde Distrital.',
                                'El brigadista es la persona entre 16 y 40 '
                                'años que, de forma voluntaria, conforma la '
                                'Brigada de Defensa Civil.']}],
  'qr_reto': [{'pregunta': 'Una situación en la que un animal produce daños '
                           'económicos a intereses de las personas se llama:',
               'respuesta': 'Plaga'},
              {'pregunta': 'El SINAGERD busca capacitar a los componentes '
                           'del sistema para:',
               'respuesta': 'La toma de decisiones'},
              {'pregunta': 'El punto en la profundidad de la Tierra desde '
                           'donde se libera la energía en un movimiento '
                           'sísmico se llama:',
               'respuesta': 'Hipocentro o foco'}],
  'qr_dato': 'No puede haber riesgo sin amenaza y tampoco sin '
             'vulnerabilidad.'},
 {'num': 13,
  'titulo': 'Dinámica Poblacional en el Perú',
  'secciones': [{'titulo': '13.1 DEMOGRAFÍA Y DEMOGEOGRAFÍA',
                 'items': ['La {demogeografía} pertenece a la geografía '
                           'humana y estudia la distribución de la población '
                           'en un área geográfica.',
                           'La {demografía} es la ciencia que estudia '
                           'estadísticamente la estructura y dinámica de las '
                           'poblaciones humanas.']},
                {'titulo': '13.2 ÍNDICES DEMOGRÁFICOS',
                 'items': ['La {tasa de natalidad} es el número de '
                           'nacimientos por cada mil habitantes en un año; '
                           'en el Perú es de {23,3}‰ anual.',
                           'La {tasa de mortalidad} es el número de '
                           'defunciones por cada mil habitantes; en el Perú '
                           'es de {6,2}‰ anual.',
                           'La {tasa de crecimiento} considera nacimientos, '
                           'muertes y migración, y nunca debe confundirse '
                           'con la tasa de {natalidad}.',
                           'Según el INEI, la población del Perú al año 2017 '
                           'superaba los {31 237 385} habitantes, con una '
                           'tasa de crecimiento anual de {1,0}%.']},
                {'titulo': '13.3 EL INEI Y LA POBLACIÓN PERUANA',
                 'items': ['El {INEI} es el organismo central y rector del '
                           'Sistema Estadístico Nacional, dependiente del '
                           'Presidente del Consejo de Ministros.',
                           'En {1969}, mediante Decreto Ley 17532, se creó '
                           'la Oficina Nacional de Estadística y Censos, '
                           'conocida como {ONEC}.',
                           'La población peruana es {heterogénea}: '
                           'multirracial, multilingüe y multicultural, y se '
                           'concentra mayormente en la {costa}.']},
                {'titulo': '13.4 CLASES DE POBLACIÓN',
                 'items': ['La {población nominal} es el número total de '
                           'habitantes que han sido censados.',
                           'La {población omitida} es la que no se halla '
                           'físicamente durante el censo.',
                           'La {población absoluta} es la cantidad total de '
                           'habitantes de una unidad geográfica.',
                           'La {población relativa} o densidad de población '
                           'es el número de habitantes por km² de área '
                           'territorial.']},
                {'titulo': '13.5 ESTRUCTURA DE LA POBLACIÓN',
                 'items': ['La {estructura demográfica} de una población es '
                           'su distribución por {edad} y sexo.',
                           'Esta distribución se representa en un gráfico de '
                           'barras horizontales llamado {pirámide '
                           'poblacional}.',
                           'La pirámide poblacional peruana actual muestra '
                           'una base más {reducida} que en 1940, reflejando '
                           'menor natalidad y mayor población en edad '
                           '{activa}.',
                           'Según el Censo {2017}, en el Perú se censaron '
                           '3145 personas centenarias (100 años o más): 994 '
                           'hombres y {2151} mujeres.']},
                {'titulo': '13.6 LA MIGRACIÓN: CAUSAS',
                 'items': ['La {migración} es el desplazamiento de la '
                           'población de un lugar de origen a un lugar de '
                           '{residencia}; incluye migración interna y '
                           'externa.',
                           'Entre las causas de la migración peruana están '
                           'las {catástrofes naturales}, el {centralismo}, y '
                           'la violencia social del terrorismo.',
                           'Otras causas son los bajos ingresos de los '
                           'agricultores de la {sierra}, y el poder de '
                           'atracción de las ciudades por su {desarrollo}.']},
                {'titulo': '13.7 CONSECUENCIAS NEGATIVAS DE LA MIGRACIÓN',
                 'items': ['Entre las consecuencias negativas de la '
                           'migración peruana están el {despoblamiento} del '
                           'campo y el abandono de la agricultura.',
                           'También genera el {crecimiento desordenado} de '
                           'las ciudades y la desocupación de la población '
                           'urbana.',
                           'Provoca problemas sociales en las ciudades como '
                           '{delincuencia}, drogadicción y alcoholismo.']}],
  'cuadros': [{'titulo': '13.2 POBLACIÓN DEL PERÚ POR CENSOS',
               'encabezados': ['Año', 'Población', 'Densidad hab/km²'],
               'filas': [['{1940}', '7 023 111', '5,5'],
                         ['1961', '10 420 357', '{8,1}'],
                         ['1993', '{22 639 443}', '17,6'],
                         ['2007', '28 220 764', '{22,0}'],
                         ['{2017}', '31 237 385', '24,3']]}],
  'preguntas': [{'pregunta': 'La disciplina que estudia la distribución de '
                             'la población en un área geográfica es:',
                 'alternativas': ['La demogeografía',
                                  'La demografía',
                                  'La cartografía',
                                  'La estadística',
                                  'La geopolítica'],
                 'correcta': 'A'},
                {'pregunta': 'La demografía estudia estadísticamente la '
                             'estructura y dinámica de:',
                 'alternativas': ['Las poblaciones humanas',
                                  'Los climas',
                                  'Los ecosistemas',
                                  'Las corrientes marinas',
                                  'El relieve terrestre'],
                 'correcta': 'A'},
                {'pregunta': 'La tasa de natalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['6,2‰', '23,3‰', '10‰', '50‰', '1‰'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de mortalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['30‰', '15‰', '23,3‰', '6,2‰', '2‰'],
                 'correcta': 'D'},
                {'pregunta': 'La tasa de crecimiento poblacional considera '
                             'nacimientos, muertes y:',
                 'alternativas': ['La migración',
                                  'La religión',
                                  'La economía',
                                  'El clima',
                                  'El idioma'],
                 'correcta': 'A'},
                {'pregunta': 'Según el INEI, la población del Perú al 2017 '
                             'superaba:',
                 'alternativas': ['20 millones',
                                  '10 millones',
                                  '50 millones',
                                  '40 millones',
                                  '31 237 385 habitantes'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo central y rector del Sistema '
                             'Estadístico Nacional del Perú es:',
                 'alternativas': ['El MINEDU',
                                  'El MEF',
                                  'El INEI',
                                  'La SUNAT',
                                  'El BCRP'],
                 'correcta': 'C'},
                {'pregunta': 'El INEI depende directamente de:',
                 'alternativas': ['El Congreso',
                                  'La Presidencia de la República '
                                  'directamente',
                                  'El Poder Judicial',
                                  'El Presidente del Consejo de Ministros',
                                  'El Ministerio de Economía'],
                 'correcta': 'D'},
                {'pregunta': 'El antecesor del INEI, creado en 1969, se '
                             'llamó:',
                 'alternativas': ['ONEC', 'INE', 'BCRP', 'MEF', 'SUNAT'],
                 'correcta': 'A'},
                {'pregunta': 'La población peruana se caracteriza por ser:',
                 'alternativas': ['Sin diversidad lingüística',
                                  'Heterogénea, multirracial y multicultural',
                                  'Homogénea y monocultural',
                                  'Solo urbana',
                                  'Exclusivamente andina'],
                 'correcta': 'B'},
                {'pregunta': 'La población peruana se concentra mayormente '
                             'en:',
                 'alternativas': ['La sierra',
                                  'Zonas rurales exclusivamente',
                                  'La selva',
                                  'La costa y zonas urbanas',
                                  'Zonas fronterizas'],
                 'correcta': 'D'},
                {'pregunta': 'La población nominal es:',
                 'alternativas': ['La población futura',
                                  'Solo la población urbana',
                                  'La estimada por proyección',
                                  'Solo la población rural',
                                  'El número total de habitantes censados'],
                 'correcta': 'E'},
                {'pregunta': 'La población que no se halla físicamente '
                             'durante el censo se llama:',
                 'alternativas': ['Población relativa',
                                  'Población absoluta',
                                  'Población omitida',
                                  'Población flotante',
                                  'Población nominal'],
                 'correcta': 'C'},
                {'pregunta': 'La población absoluta es:',
                 'alternativas': ['Solo la tasa de crecimiento',
                                  'Solo un porcentaje',
                                  'Solo la densidad',
                                  'La cantidad total de habitantes de una '
                                  'unidad geográfica',
                                  'Un promedio estimado'],
                 'correcta': 'D'},
                {'pregunta': 'La densidad de población también se llama:',
                 'alternativas': ['Población relativa',
                                  'Población nominal',
                                  'Población omitida',
                                  'Población censada',
                                  'Población flotante'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula de la población relativa es:',
                 'alternativas': ['Tasa de natalidad menos mortalidad',
                                  'Población nominal más omitida',
                                  'Población absoluta entre extensión '
                                  'territorial',
                                  'Población absoluta × extensión '
                                  'territorial',
                                  'Extensión territorial entre población '
                                  'absoluta'],
                 'correcta': 'C'},
                {'pregunta': 'Según el censo de 1940, la población del Perú '
                             'era de:',
                 'alternativas': ['22 639 443',
                                  '7 023 111',
                                  '14 121 564',
                                  '10 420 357',
                                  '28 220 764'],
                 'correcta': 'B'},
                {'pregunta': 'Según el censo de 2007, la población del Perú '
                             'era de:',
                 'alternativas': ['17 762 231',
                                  '22 639 443',
                                  '31 237 385',
                                  '14 121 564',
                                  '28 220 764'],
                 'correcta': 'E'},
                {'pregunta': 'La densidad poblacional del Perú en 2017 era '
                             'aproximadamente de:',
                 'alternativas': ['5 hab/km²',
                                  '100 hab/km²',
                                  '50 hab/km²',
                                  '24,3 hab/km²',
                                  '10 hab/km²'],
                 'correcta': 'D'},
                {'pregunta': 'La esperanza de vida en el Perú, según el '
                             'censo de 2007, fue de:',
                 'alternativas': ['35,6 años',
                                  '80 años',
                                  '55 años',
                                  '65 años',
                                  '71,2 años'],
                 'correcta': 'E'},
                {'pregunta': 'La ciencia que estudia estadísticamente la '
                             'estructura y la dinámica de las poblaciones '
                             'humanas es: (I CEPRU 2024)',
                 'alternativas': ['Geomorfología',
                                  'Demogeografía',
                                  'Geodesia',
                                  'Edafología',
                                  'Demografía'],
                 'correcta': 'E'},
                {'pregunta': 'Considerando los periodos censales entre 1940 '
                             'y 2017, la región natural que presenta '
                             'tendencia negativa en su crecimiento '
                             'poblacional es la: (II CEPRU 2022)',
                 'alternativas': ['Selva',
                                  'Costa',
                                  'Vertiente occidental',
                                  'Sierra',
                                  'Faja subandina'],
                 'correcta': 'D'},
                {'pregunta': 'Según el censo del 2017, la región natural con '
                             'mayor tendencia al crecimiento poblacional es: '
                             '(Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['El Sur',
                                  'La Sierra',
                                  'El Norte',
                                  'La Selva',
                                  'La Costa'],
                 'correcta': 'E'},
                {'pregunta': 'La distribución de una población por edad y '
                             'sexo se llama:',
                 'alternativas': ['Estructura demográfica',
                                  'Tasa de natalidad',
                                  'Densidad poblacional',
                                  'Migración',
                                  'Esperanza de vida'],
                 'correcta': 'A'},
                {'pregunta': 'La estructura demográfica de una población se '
                             'representa en un gráfico de barras '
                             'horizontales llamado:',
                 'alternativas': ['Curva de Lorenz',
                                  'Histograma de natalidad',
                                  'Gráfico de dispersión',
                                  'Mapa de calor',
                                  'Pirámide poblacional'],
                 'correcta': 'E'},
                {'pregunta': 'Según el Censo 2017, el número de personas '
                             'centenarias (100 años o más) censadas en el '
                             'Perú fue de:',
                 'alternativas': ['2000', '1000', '3145', '10000', '5000'],
                 'correcta': 'C'},
                {'pregunta': 'El desplazamiento de la población de un lugar '
                             'de origen a un lugar de residencia se llama:',
                 'alternativas': ['Natalidad',
                                  'Mortalidad',
                                  'Densidad poblacional',
                                  'Fecundidad',
                                  'Migración'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las causas de la migración peruana está '
                             'el centralismo, que favorece el desarrollo de:',
                 'alternativas': ['Algunas ciudades',
                                  'Solo las zonas rurales',
                                  'Todas las regiones por igual',
                                  'Solo la selva',
                                  'Solo la sierra'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las consecuencias negativas de la '
                             'migración peruana está el despoblamiento del '
                             'campo y el abandono de la:',
                 'alternativas': ['Agricultura',
                                  'Minería',
                                  'Pesca',
                                  'Ganadería exclusiva',
                                  'Industria'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'DEMOGRAFÍA Y DEMOGEOGRAFÍA',
                      'items': ['La demogeografía pertenece a la geografía '
                                'humana y estudia la distribución de la '
                                'población en un área geográfica.',
                                'La demografía es la ciencia que estudia '
                                'estadísticamente la estructura y dinámica '
                                'de las poblaciones humanas.']},
                     {'titulo': 'ÍNDICES DEMOGRÁFICOS',
                      'items': ['La tasa de natalidad es el número de '
                                'nacimientos por cada mil habitantes en un '
                                'año; en el Perú es de 23,3‰ anual.',
                                'La tasa de mortalidad es el número de '
                                'defunciones por cada mil habitantes; en el '
                                'Perú es de 6,2‰ anual.',
                                'La tasa de crecimiento considera '
                                'nacimientos, muertes y migración, y nunca '
                                'debe confundirse con la tasa de natalidad.',
                                'Según el INEI, la población del Perú al año '
                                '2017 superaba los 31 237 385 habitantes, '
                                'con una tasa de crecimiento anual de '
                                '1,0%.']},
                     {'titulo': 'EL INEI Y LA POBLACIÓN PERUANA',
                      'items': ['El INEI es el organismo central y rector '
                                'del Sistema Estadístico Nacional, '
                                'dependiente del Presidente del Consejo de '
                                'Ministros.',
                                'En 1969, mediante Decreto Ley 17532, se '
                                'creó la Oficina Nacional de Estadística y '
                                'Censos, conocida como ONEC.',
                                'La población peruana es heterogénea: '
                                'multirracial, multilingüe y multicultural, '
                                'y se concentra mayormente en la costa.']},
                     {'titulo': 'CLASES DE POBLACIÓN',
                      'items': ['La población nominal es el número total de '
                                'habitantes que han sido censados.',
                                'La población omitida es la que no se halla '
                                'físicamente durante el censo.',
                                'La población absoluta es la cantidad total '
                                'de habitantes de una unidad geográfica.',
                                'La población relativa o densidad de '
                                'población es el número de habitantes por '
                                'km² de área territorial.']},
                     {'titulo': 'ESTRUCTURA DE LA POBLACIÓN',
                      'items': ['La estructura demográfica de una población '
                                'es su distribución por edad y sexo.',
                                'Esta distribución se representa en un '
                                'gráfico de barras horizontales llamado '
                                'pirámide poblacional.',
                                'La pirámide poblacional peruana actual '
                                'muestra una base más reducida que en 1940, '
                                'reflejando menor natalidad y mayor '
                                'población en edad activa.',
                                'Según el Censo 2017, en el Perú se censaron '
                                '3145 personas centenarias (100 años o más): '
                                '994 hombres y 2151 mujeres.']},
                     {'titulo': 'LA MIGRACIÓN: CAUSAS',
                      'items': ['La migración es el desplazamiento de la '
                                'población de un lugar de origen a un lugar '
                                'de residencia; incluye migración interna y '
                                'externa.',
                                'Entre las causas de la migración peruana '
                                'están las catástrofes naturales, el '
                                'centralismo, y la violencia social del '
                                'terrorismo.',
                                'Otras causas son los bajos ingresos de los '
                                'agricultores de la sierra, y el poder de '
                                'atracción de las ciudades por su '
                                'desarrollo.']},
                     {'titulo': 'CONSECUENCIAS NEGATIVAS DE LA MIGRACIÓN',
                      'items': ['Entre las consecuencias negativas de la '
                                'migración peruana están el despoblamiento '
                                'del campo y el abandono de la agricultura.',
                                'También genera el crecimiento desordenado '
                                'de las ciudades y la desocupación de la '
                                'población urbana.',
                                'Provoca problemas sociales en las ciudades '
                                'como delincuencia, drogadicción y '
                                'alcoholismo.']}],
  'qr_reto': [{'pregunta': 'Según el INEI, la población del Perú al 2017 '
                           'superaba:',
               'respuesta': '31 237 385 habitantes'},
              {'pregunta': 'La población nominal es:',
               'respuesta': 'El número total de habitantes censados'},
              {'pregunta': 'El desplazamiento de la población de un lugar de '
                           'origen a un lugar de residencia se llama:',
               'respuesta': 'Migración'}],
  'qr_dato': 'La población relativa o densidad de población es el número de '
             'habitantes por km² de área territorial.'},
 {'num': 14,
  'titulo': 'Actividades Económicas Extractivas en el Perú',
  'secciones': [{'titulo': '14.1 LA PESCA EN EL MAR PERUANO',
                 'items': ['La pesca es una actividad económica {extractiva} '
                           'que consiste en el aprovechamiento de los '
                           'recursos {hidrobiológicos}.',
                           'Entre los factores de la riqueza ictiológica '
                           'figuran la {frialdad} de las aguas y la '
                           'abundancia del {plancton}.',
                           'La especie más importante de la pesca marina es '
                           'la {anchoveta}, de la cual se extrae harina y '
                           '{aceite} de pescado.',
                           'La anchoveta es el alimento principal de peces '
                           'mayores y de las aves {guaneras}.',
                           'Según datos al 2018, el principal puerto '
                           'pesquero del Perú es {Chimbote}.']},
                {'titulo': '14.2 PESCA EN LA SELVA Y EN LA COSTA',
                 'items': ['En la selva se pesca con técnicas tradicionales '
                           'como redes de cortina, {flecha} y arpón.',
                           'El {paiche} es la principal especie de pesca en '
                           'las cochas amazónicas, capturado con arpón.',
                           'En la costa, la pesca de {camarón} se realiza en '
                           'ríos de Arequipa, Lima e Ica.']},
                {'titulo': '14.3 PESCA EN LA REGIÓN ANDINA',
                 'items': ['En la región andina se pesca principalmente en '
                           'el lago {Titicaca}, con fines deportivos y '
                           'alimenticios.',
                           'La principal especie de pesca andina es la '
                           '{trucha}, producida sobre todo en Puno, '
                           'Huancavelica y {Junín}.']},
                {'titulo': '14.4 IMPACTO AMBIENTAL DE LA PESCA',
                 'items': ['Los impactos en la biodiversidad pesquera '
                           'provienen de la {sobrepesca}, la captura '
                           'incidental y la degradación del {hábitat}.',
                           'El exceso de pesca reduce la existencia de '
                           'especies y afecta la estructura de los '
                           '{ecosistemas} marinos.']},
                {'titulo': '14.5 LA MINERÍA EN EL PERÚ: CLASIFICACIÓN',
                 'items': ['La {gran minería} opera en más de 2000 '
                           'hectáreas, con más de {5000} TM/día de volumen.',
                           'La {mediana minería} opera en más de 2000 '
                           'hectáreas, con hasta 5000 TM/día; la {pequeña '
                           'minería}, hasta 2000 hectáreas y 300 TM/día.',
                           'La {minería artesanal} opera hasta 1000 '
                           'hectáreas, con hasta {25} TM/día.',
                           'Al 2023, Arequipa es el principal productor de '
                           '{cobre}; La Libertad, de {oro}; y Pasco, de '
                           'plata y plomo.']},
                {'titulo': '14.6 GRANDES CENTROS MINEROS DEL PERÚ',
                 'items': ['{Toquepala}, en Tacna, fue el centro minero más '
                           'grande del Perú hasta 1977; se extrae {cobre} a '
                           'tajo abierto.',
                           '{Yanacocha}, en Cajamarca, produce {oro}.',
                           '{Antamina}, en Áncash, constituye la mayor '
                           'reserva minera; transporta cobre y zinc por un '
                           'mineroducto de {320} km.',
                           '{Marcona}, en Ica, es el único centro minero que '
                           'produce {hierro}.',
                           '{Las Bambas}, en Apurímac (desde 2016), explota '
                           'cobre a tajo abierto.',
                           'La {refinería de La Oroya}, en Junín, procesa '
                           '{11} minerales distintos.']},
                {'titulo': '14.7 EL PETRÓLEO: ZONAS DE PRODUCCIÓN',
                 'items': ['El {petróleo}, llamado «oro negro», es un '
                           'mineral energético formado a partir de '
                           'microorganismos marinos enterrados hace millones '
                           'de años.',
                           'Los principales yacimientos petrolíferos se '
                           'localizan en la {costa norte} (Piura) y en la '
                           '{selva} peruana.',
                           'En la costa norte (Piura), los principales '
                           'yacimientos son La Brea, Pariñas y {Talara}; '
                           'trabaja la empresa {Petrobras}.',
                           'La {Refinería de Talara} es la más antigua, con '
                           'capacidad de 67 000 barriles diarios; procesa '
                           'petróleo {nacional}.',
                           'La {Refinería de La Pampilla}, en Ventanilla, es '
                           'la más moderna y amplia, con 110 000 barriles '
                           'diarios; procesa petróleo {importado}.']},
                {'titulo': '14.8 EL GAS NATURAL',
                 'items': ['El {gas natural} es un hidrocarburo gaseoso cuyo '
                           'origen está relacionado con el del {petróleo}.',
                           'Al 2023, el principal departamento productor de '
                           'gas natural es {Cusco}, con 94,8%; el segundo es '
                           '{Piura}, con 3,7%; el tercero es Ucayali, con '
                           '1,5%.']},
                {'titulo': '14.9 IMPACTO AMBIENTAL DE LA MINERÍA',
                 'items': ['Por cada gramo de oro producido, queda una '
                           '{tonelada} de tierra con cianuro, arsénico y '
                           'otros metales pesados.',
                           'La contaminación del aire por la minería se '
                           'manifiesta a través de polvos y gases, siendo el '
                           'más significativo el {dióxido de azufre}.',
                           'En la salud, la contaminación minera afecta el '
                           'aparato respiratorio, causando neumoconiosis y '
                           '{cáncer} de pulmón.',
                           'La minería ilegal en {Madre de Dios} ha '
                           'destruido una extensión de bosques equivalente a '
                           '41 mil canchas de fútbol.']}],
  'cuadros': [{'titulo': '14.1 PRINCIPALES PUERTOS PESQUEROS (2018)',
               'encabezados': ['Orden', 'Puerto'],
               'filas': [['1°', '{Chimbote}'],
                         ['2°', '{Chicama}'],
                         ['3°', 'Coishco'],
                         ['4°', '{Paita}'],
                         ['5°', 'Callao']]}],
  'preguntas': [{'pregunta': 'La pesca es una actividad económica de tipo:',
                 'alternativas': ['Financiera',
                                  'Industrial exclusiva',
                                  'Reproductiva',
                                  'Comercial únicamente',
                                  'Extractiva'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los factores de la riqueza ictiológica '
                             'del mar peruano figura:',
                 'alternativas': ['El agua cálida',
                                  'La ausencia de zócalo continental',
                                  'La frialdad de las aguas por la Corriente '
                                  'Peruana',
                                  'El agua dulce',
                                  'La escasez de plancton'],
                 'correcta': 'C'},
                {'pregunta': 'La especie más importante de la pesca marina '
                             'peruana es:',
                 'alternativas': ['El atún',
                                  'El jurel',
                                  'La caballa',
                                  'La anchoveta',
                                  'El bonito'],
                 'correcta': 'D'},
                {'pregunta': 'De la anchoveta se extrae principalmente:',
                 'alternativas': ['Conservas de lujo',
                                  'Harina y aceite de pescado',
                                  'Aceite de oliva',
                                  'Sal marina',
                                  'Perlas'],
                 'correcta': 'B'},
                {'pregunta': 'La anchoveta sirve de alimento principal para:',
                 'alternativas': ['Solo aves terrestres',
                                  'Solo mamíferos marinos',
                                  'Ningún otro organismo',
                                  'Solo el ser humano',
                                  'Peces mayores y aves guaneras'],
                 'correcta': 'E'},
                {'pregunta': 'El principal puerto pesquero del Perú, según '
                             'datos de 2018, fue:',
                 'alternativas': ['Paita',
                                  'Chancay',
                                  'Chimbote',
                                  'Callao',
                                  'Pisco'],
                 'correcta': 'C'},
                {'pregunta': 'En la selva, una técnica tradicional de pesca '
                             'es el uso de:',
                 'alternativas': ['Redes industriales',
                                  'Flecha y arpón',
                                  'Trampas eléctricas',
                                  'Barcos factoría',
                                  'Sonar'],
                 'correcta': 'B'},
                {'pregunta': 'El paiche se pesca principalmente en:',
                 'alternativas': ['Las cochas amazónicas',
                                  'Ríos de la costa',
                                  'Lagunas andinas',
                                  'El mar peruano',
                                  'El lago Titicaca'],
                 'correcta': 'A'},
                {'pregunta': 'El paiche se captura tradicionalmente con:',
                 'alternativas': ['Explosivos',
                                  'Redes de arrastre',
                                  'Arpón',
                                  'Anzuelo eléctrico',
                                  'Trampas de metal'],
                 'correcta': 'C'},
                {'pregunta': 'La pesca de camarón en la costa se realiza en '
                             'ríos de Arequipa, Lima e:',
                 'alternativas': ['Ica',
                                  'Tacna',
                                  'Piura',
                                  'Tumbes',
                                  'Moquegua'],
                 'correcta': 'A'},
                {'pregunta': 'En la región andina, la pesca se practica '
                             'principalmente en el lago:',
                 'alternativas': ['Junín',
                                  'Chinchaycocha',
                                  'Parinacochas',
                                  'Sausacocha',
                                  'Titicaca'],
                 'correcta': 'E'},
                {'pregunta': 'La principal especie de pesca en la región '
                             'andina es:',
                 'alternativas': ['El atún',
                                  'El paiche',
                                  'La anchoveta',
                                  'La trucha',
                                  'El camarón'],
                 'correcta': 'D'},
                {'pregunta': 'Los departamentos productores de trucha son '
                             'Puno, Huancavelica y:',
                 'alternativas': ['Arequipa',
                                  'Cusco',
                                  'Tacna',
                                  'Junín',
                                  'Ayacucho'],
                 'correcta': 'D'},
                {'pregunta': 'Los impactos en la biodiversidad pesquera '
                             'provienen de la sobrepesca, la captura '
                             'incidental y:',
                 'alternativas': ['La degradación del hábitat',
                                  'El comercio justo',
                                  'El turismo',
                                  'La acuicultura',
                                  'La pesca artesanal exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El exceso de pesca causa principalmente:',
                 'alternativas': ['Reducción de la existencia de especies',
                                  'Ningún efecto negativo',
                                  'Aumento de especies',
                                  'Incremento de la biodiversidad',
                                  'Mejora del ecosistema'],
                 'correcta': 'A'},
                {'pregunta': 'La amplitud del zócalo continental favorece la '
                             'riqueza ictiológica porque facilita:',
                 'alternativas': ['La salinidad extrema',
                                  'El afloramiento volcánico',
                                  'La penetración de rayos solares',
                                  'La formación de olas',
                                  'El enfriamiento del agua'],
                 'correcta': 'C'},
                {'pregunta': 'El fenómeno del afloramiento influye en la '
                             'pesca porque:',
                 'alternativas': ['Genera tsunamis',
                                  'Reduce el oxígeno del agua',
                                  'Produce la frialdad característica del '
                                  'mar peruano',
                                  'Calienta el agua superficial',
                                  'Elimina el plancton'],
                 'correcta': 'C'},
                {'pregunta': 'El zúngaro es una especie de pesca '
                             'característica de:',
                 'alternativas': ['El mar peruano',
                                  'Los Andes centrales',
                                  'La costa sur',
                                  'El lago Titicaca',
                                  'La selva'],
                 'correcta': 'E'},
                {'pregunta': 'El plancton constituye alimento fundamental '
                             'para:',
                 'alternativas': ['Los peces del mar peruano',
                                  'Solo las aves',
                                  'Solo el hombre',
                                  'Solo los mamíferos marinos',
                                  'Ningún organismo marino'],
                 'correcta': 'A'},
                {'pregunta': 'La pesca deportiva en la región andina se '
                             'realiza principalmente con:',
                 'alternativas': ['Trampas eléctricas',
                                  'Anzuelos, redes y balsas',
                                  'Explosivos',
                                  'Redes industriales',
                                  'Barcos factoría'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo departamento productor de gas en el '
                             'Perú es: (II CEPRU 2025)',
                 'alternativas': ['Ucayali',
                                  'Junín',
                                  'Piura',
                                  'Loreto',
                                  'Madre de Dios'],
                 'correcta': 'C'},
                {'pregunta': 'La refinería de La Oroya se ubica en el '
                             'departamento de: (II CEPRU 2022)',
                 'alternativas': ['Junín',
                                  'Moquegua',
                                  'Cajamarca',
                                  'Ayacucho',
                                  'Lima'],
                 'correcta': 'A'},
                {'pregunta': 'El principal productor de maíz amiláceo en el '
                             'territorio peruano es el departamento de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['Pasco',
                                  'Lima',
                                  'Cajamarca',
                                  'Arequipa',
                                  'Puno'],
                 'correcta': 'C'},
                {'pregunta': 'El uso continuo del suelo y el predominio de '
                             'herramientas mecanizadas es una característica '
                             'de la agricultura denominada: (Primera '
                             'Oportunidad UNSAAC 2025)',
                 'alternativas': ['Tradicional',
                                  'Experimental',
                                  'Intensiva',
                                  'Migratoria',
                                  'Extensiva'],
                 'correcta': 'C'},
                {'pregunta': 'La clasificación minera que opera en más de '
                             '2000 hectáreas, con más de 5000 TM/día, se '
                             'llama:',
                 'alternativas': ['Minería artesanal',
                                  'Minería informal',
                                  'Gran minería',
                                  'Pequeña minería',
                                  'Mediana minería'],
                 'correcta': 'C'},
                {'pregunta': 'La minería que opera hasta 1000 hectáreas, con '
                             'hasta 25 TM/día, se llama minería:',
                 'alternativas': ['Gran minería',
                                  'Pequeña',
                                  'Mediana',
                                  'Industrial',
                                  'Artesanal'],
                 'correcta': 'E'},
                {'pregunta': 'El centro minero que fue el más grande del '
                             'Perú hasta 1977, ubicado en Tacna, donde se '
                             'extrae cobre a tajo abierto, es:',
                 'alternativas': ['Cerro Verde',
                                  'Toquepala',
                                  'Cuajone',
                                  'Las Bambas',
                                  'Antamina'],
                 'correcta': 'B'},
                {'pregunta': 'El centro minero de Yanacocha, en Cajamarca, '
                             'produce principalmente:',
                 'alternativas': ['Hierro', 'Oro', 'Plata', 'Zinc', 'Cobre'],
                 'correcta': 'B'},
                {'pregunta': 'El centro minero que constituye la mayor '
                             'reserva minera del Perú, ubicado en Áncash, '
                             'que transporta cobre y zinc por un '
                             'mineroducto, es:',
                 'alternativas': ['Antamina',
                                  'Marcona',
                                  'Toquepala',
                                  'Cerro de Pasco',
                                  'Cobriza'],
                 'correcta': 'A'},
                {'pregunta': 'El único centro minero del Perú que produce '
                             'hierro, ubicado en Ica, es:',
                 'alternativas': ['Yanacocha',
                                  'Cerro Verde',
                                  'Marcona',
                                  'Antamina',
                                  'Cobriza'],
                 'correcta': 'C'},
                {'pregunta': 'La refinería de La Oroya, en el departamento '
                             'de Junín, procesa un número de minerales igual '
                             'a:',
                 'alternativas': ['3', '20', '11', '1', '5'],
                 'correcta': 'C'},
                {'pregunta': 'El petróleo, llamado «oro negro», se formó a '
                             'partir de:',
                 'alternativas': ['Rocas volcánicas',
                                  'Minerales metálicos',
                                  'Sedimentos glaciares',
                                  'Cenizas volcánicas',
                                  'Microorganismos marinos enterrados hace '
                                  'millones de años'],
                 'correcta': 'E'},
                {'pregunta': 'Los principales yacimientos petrolíferos del '
                             'Perú se localizan en la costa norte y en la:',
                 'alternativas': ['Selva peruana',
                                  'Zona insular',
                                  'Región del Titicaca',
                                  'Costa sur',
                                  'Región andina'],
                 'correcta': 'A'},
                {'pregunta': 'La refinería de petróleo más antigua del Perú, '
                             'con capacidad de 67 000 barriles diarios, es '
                             'la de:',
                 'alternativas': ['Pucallpa',
                                  'Talara',
                                  'La Pampilla',
                                  'Iquitos',
                                  'Conchán'],
                 'correcta': 'B'},
                {'pregunta': 'La refinería de petróleo más moderna y amplia '
                             'del Perú, ubicada en Ventanilla, es la de:',
                 'alternativas': ['Shiviyacu',
                                  'Talara',
                                  'La Pampilla',
                                  'El Milagro',
                                  'Conchán'],
                 'correcta': 'C'},
                {'pregunta': 'Al 2023, el principal departamento productor '
                             'de gas natural del Perú es:',
                 'alternativas': ['Loreto',
                                  'Piura',
                                  'Ucayali',
                                  'Puno',
                                  'Cusco'],
                 'correcta': 'E'},
                {'pregunta': 'Al 2023, el segundo departamento productor de '
                             'gas natural del Perú, con 3,7%, es:',
                 'alternativas': ['Ucayali',
                                  'Madre de Dios',
                                  'Piura',
                                  'Loreto',
                                  'Cusco'],
                 'correcta': 'C'},
                {'pregunta': 'El contaminante gaseoso más significativo '
                             'producido por la actividad minera se llama:',
                 'alternativas': ['Dióxido de carbono',
                                  'Monóxido de carbono',
                                  'Metano',
                                  'Dióxido de azufre',
                                  'Ozono'],
                 'correcta': 'D'},
                {'pregunta': 'Por cada gramo de oro producido en la minería, '
                             'queda una tonelada de tierra contaminada con:',
                 'alternativas': ['Solo polvo',
                                  'Solo residuos orgánicos',
                                  'Cianuro, arsénico y metales pesados',
                                  'Solo agua',
                                  'Solo tierra estéril'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LA PESCA EN EL MAR PERUANO / PESCA EN LA '
                                'SELVA Y EN LA COSTA',
                      'items': ['La pesca es una actividad económica '
                                'extractiva que consiste en el '
                                'aprovechamiento de los recursos '
                                'hidrobiológicos.',
                                'Entre los factores de la riqueza '
                                'ictiológica figuran la frialdad de las '
                                'aguas y la abundancia del plancton.',
                                'La especie más importante de la pesca '
                                'marina es la anchoveta, de la cual se '
                                'extrae harina y aceite de pescado.',
                                'La anchoveta es el alimento principal de '
                                'peces mayores y de las aves guaneras.',
                                'Según datos al 2018, el principal puerto '
                                'pesquero del Perú es Chimbote.',
                                'En la selva se pesca con técnicas '
                                'tradicionales como redes de cortina, flecha '
                                'y arpón.',
                                'El paiche es la principal especie de pesca '
                                'en las cochas amazónicas, capturado con '
                                'arpón.',
                                'En la costa, la pesca de camarón se realiza '
                                'en ríos de Arequipa, Lima e Ica.']},
                     {'titulo': 'PESCA EN LA REGIÓN ANDINA / IMPACTO '
                                'AMBIENTAL DE LA PESCA',
                      'items': ['En la región andina se pesca principalmente '
                                'en el lago Titicaca, con fines deportivos y '
                                'alimenticios.',
                                'La principal especie de pesca andina es la '
                                'trucha, producida sobre todo en Puno, '
                                'Huancavelica y Junín.',
                                'Los impactos en la biodiversidad pesquera '
                                'provienen de la sobrepesca, la captura '
                                'incidental y la degradación del hábitat.',
                                'El exceso de pesca reduce la existencia de '
                                'especies y afecta la estructura de los '
                                'ecosistemas marinos.']},
                     {'titulo': 'LA MINERÍA EN EL PERÚ: CLASIFICACIÓN / '
                                'GRANDES CENTROS MINEROS DEL PERÚ',
                      'items': ['La gran minería opera en más de 2000 '
                                'hectáreas, con más de 5000 TM/día de '
                                'volumen.',
                                'La mediana minería opera en más de 2000 '
                                'hectáreas, con hasta 5000 TM/día; la '
                                'pequeña minería, hasta 2000 hectáreas y 300 '
                                'TM/día.',
                                'La minería artesanal opera hasta 1000 '
                                'hectáreas, con hasta 25 TM/día.',
                                'Al 2023, Arequipa es el principal productor '
                                'de cobre; La Libertad, de oro; y Pasco, de '
                                'plata y plomo.',
                                'Toquepala, en Tacna, fue el centro minero '
                                'más grande del Perú hasta 1977; se extrae '
                                'cobre a tajo abierto.',
                                'Yanacocha, en Cajamarca, produce oro.',
                                'Antamina, en Áncash, constituye la mayor '
                                'reserva minera; transporta cobre y zinc por '
                                'un mineroducto de 320 km.',
                                'Marcona, en Ica, es el único centro minero '
                                'que produce hierro.',
                                'Las Bambas, en Apurímac (desde 2016), '
                                'explota cobre a tajo abierto.',
                                'La refinería de La Oroya, en Junín, procesa '
                                '11 minerales distintos.']},
                     {'titulo': 'EL PETRÓLEO: ZONAS DE PRODUCCIÓN / EL GAS '
                                'NATURAL',
                      'items': ['El petróleo, llamado «oro negro», es un '
                                'mineral energético formado a partir de '
                                'microorganismos marinos enterrados hace '
                                'millones de años.',
                                'Los principales yacimientos petrolíferos se '
                                'localizan en la costa norte (Piura) y en la '
                                'selva peruana.',
                                'En la costa norte (Piura), los principales '
                                'yacimientos son La Brea, Pariñas y Talara; '
                                'trabaja la empresa Petrobras.',
                                'La Refinería de Talara es la más antigua, '
                                'con capacidad de 67 000 barriles diarios; '
                                'procesa petróleo nacional.',
                                'La Refinería de La Pampilla, en Ventanilla, '
                                'es la más moderna y amplia, con 110 000 '
                                'barriles diarios; procesa petróleo '
                                'importado.',
                                'El gas natural es un hidrocarburo gaseoso '
                                'cuyo origen está relacionado con el del '
                                'petróleo.',
                                'Al 2023, el principal departamento '
                                'productor de gas natural es Cusco, con '
                                '94,8%; el segundo es Piura, con 3,7%; el '
                                'tercero es Ucayali, con 1,5%.']},
                     {'titulo': 'IMPACTO AMBIENTAL DE LA MINERÍA',
                      'items': ['Por cada gramo de oro producido, queda una '
                                'tonelada de tierra con cianuro, arsénico y '
                                'otros metales pesados.',
                                'La contaminación del aire por la minería se '
                                'manifiesta a través de polvos y gases, '
                                'siendo el más significativo el dióxido de '
                                'azufre.',
                                'En la salud, la contaminación minera afecta '
                                'el aparato respiratorio, causando '
                                'neumoconiosis y cáncer de pulmón.',
                                'La minería ilegal en Madre de Dios ha '
                                'destruido una extensión de bosques '
                                'equivalente a 41 mil canchas de fútbol.']}],
  'qr_reto': [{'pregunta': 'El principal productor de maíz amiláceo en el '
                           'territorio peruano es el departamento de:',
               'respuesta': 'Cajamarca'},
              {'pregunta': 'El principal puerto pesquero del Perú, según '
                           'datos de 2018, fue:',
               'respuesta': 'Chimbote'},
              {'pregunta': 'El centro minero que constituye la mayor reserva '
                           'minera del Perú, ubicado en Áncash, que '
                           'transporta cobre y zinc por un mineroducto, es:',
               'respuesta': 'Antamina'}],
  'qr_dato': 'El petróleo, llamado «oro negro», es un mineral energético '
             'formado a partir de microorganismos marinos enterrados hace '
             'millones de años.'},
 {'num': 15,
  'titulo': 'Actividades Económicas Reproductivas en el Perú',
  'secciones': [{'titulo': '15.1 LA AGRICULTURA EN EL PERÚ',
                 'items': ['La agricultura es la actividad económica '
                           '{reproductiva} que consiste en el cultivo del '
                           'suelo para obtener plantas alimenticias e '
                           'industriales.',
                           'Los españoles trajeron el arado de tracción '
                           'animal y nuevas especies como el {arroz}, '
                           'cebada, caña de azúcar y trigo.',
                           'Según la FAO, el Perú tiene en cultivo '
                           'aproximadamente {4,4} millones de hectáreas, el '
                           '{3,5}% del área total del territorio.']},
                {'titulo': '15.2 LA AGRICULTURA EN LA COSTA',
                 'items': ['La agricultura de la costa es {intensiva}, ya '
                           'que el suelo no descansa, obteniéndose hasta dos '
                           'cosechas {anuales}.',
                           'La agricultura costeña es {tecnificada} y '
                           '{mecanizada}, con uso de tractores y '
                           'fumigadoras.',
                           'En la costa predominan los cultivos '
                           '{industriales} y para la exportación, como la '
                           'caña de azúcar y el algodón.',
                           'La agricultura costeña goza de asistencia '
                           '{crediticia} por parte de bancos y entidades '
                           'financieras.']},
                {'titulo': '15.3 LA AGRICULTURA EN LA REGIÓN ANDINA',
                 'items': ['La agricultura andina es {extensiva}, porque el '
                           'suelo descansa y solo se cultiva en época de '
                           '{lluvias}.',
                           'La agricultura andina es {tradicional}, no '
                           'tecnificada, guiada por la experiencia de los '
                           'campesinos.',
                           'La agricultura andina no es {mecanizada}; se '
                           'usan herramientas tradicionales como la '
                           '{chaquitaclla}.',
                           'La agricultura andina está orientada al cultivo '
                           'de plantas de baja {rentabilidad}, como la papa, '
                           'el maíz y la cebada.']},
                {'titulo': '15.4 LA AGRICULTURA EN LA SELVA',
                 'items': ['La agricultura en la selva es {migratoria}: los '
                           'suelos se degradan rápidamente y se practica el '
                           'roce, tumba y {quema}.',
                           'La agricultura selvática está orientada al '
                           'cultivo de arroz, yuca y plátano, además de '
                           'cultivos industriales como {coca}, café y '
                           'tabaco.',
                           'En la selva alta existen valles permanentes de '
                           'cultivo como Jaén, Bagua y {Chanchamayo}.']},
                {'titulo': '15.5 LA GANADERÍA EN EL PERÚ: CONCEPTO Y '
                           'REGIONES',
                 'items': ['La {ganadería} es la actividad económica '
                           'reproductiva que consiste en la crianza, '
                           'selección y reproducción de animales domésticos, '
                           'llamados {ganado}.',
                           'La ganadería de la {costa} es predominantemente '
                           'intensiva, tecnificada y científica; predomina '
                           'el ganado vacuno {fino}, aves de corral y '
                           'porcinos.',
                           'La ganadería de la {región andina} es '
                           'predominantemente extensiva y tradicional; se '
                           'cría ganado {chusco} o criollo de baja '
                           'productividad.',
                           'En la región andina predomina la crianza de '
                           'ganado {ovino}, camélidos y vacuno; se '
                           'desarrolla en mesetas, punas y valles '
                           'interandinos.',
                           'La ganadería de la {selva} es extensiva y de '
                           'experimentación; predomina el ganado vacuno de '
                           'raza {Amazonas} (cruce de Cebú con Brown '
                           'Swiss).']},
                {'titulo': '15.6 PRINCIPALES DEPARTAMENTOS PRODUCTORES DE '
                           'GANADO',
                 'items': ['Al 2022, {Huánuco} es el principal productor de '
                           'ganado vacuno; {Puno} lidera en ovino, alpaca y '
                           'llama.',
                           '{Lima} es el principal productor de ganado '
                           'porcino y de aves; {Piura} lidera en producción '
                           'caprina.']},
                {'titulo': '15.7 IMPACTO AMBIENTAL DE LA GANADERÍA',
                 'items': ['La ganadería contamina el agua subterránea por '
                           'los {purines} o residuos fecales de las granjas, '
                           'aumentando la concentración de {nitratos}.',
                           'Según la FAO, el sector ganadero genera el {18}% '
                           'de los gases de efecto invernadero, más que el '
                           'sector transporte.',
                           'Los animales, al digerir alimentos, producen '
                           'grandes cantidades de {metano}, un potente gas '
                           'de efecto invernadero.',
                           'La ganadería utiliza el {30}% de la superficie '
                           'terrestre del planeta; en el Amazonas, el {70}% '
                           'de los bosques desaparecidos se dedicaron a '
                           'pastizales.']}],
  'cuadros': [{'titulo': '15. LA AGRICULTURA POR REGIÓN',
               'encabezados': ['Región', 'Tipo', 'Rendimiento'],
               'filas': [['{Costa}', 'Intensiva y {mecanizada}', 'Alto'],
                         ['{Andina}', 'Extensiva y {tradicional}', 'Bajo'],
                         ['{Selva}', '{Migratoria}', 'Decreciente']]}],
  'preguntas': [{'pregunta': 'La agricultura es una actividad económica de '
                             'tipo:',
                 'alternativas': ['Informal',
                                  'Terciaria exclusiva',
                                  'Reproductiva',
                                  'Extractiva',
                                  'Financiera'],
                 'correcta': 'C'},
                {'pregunta': 'Los españoles introdujeron al Perú cultivos '
                             'como el arroz, cebada y:',
                 'alternativas': ['El tarwi',
                                  'El olluco',
                                  'La papa',
                                  'La quinua',
                                  'La caña de azúcar'],
                 'correcta': 'E'},
                {'pregunta': 'Según la FAO, el Perú tiene en cultivo '
                             'aproximadamente:',
                 'alternativas': ['10 millones de hectáreas',
                                  '500 mil hectáreas',
                                  '1 millón de hectáreas',
                                  '4,4 millones de hectáreas',
                                  '20 millones de hectáreas'],
                 'correcta': 'D'},
                {'pregunta': 'El área cultivada representa del territorio '
                             'nacional peruano aproximadamente:',
                 'alternativas': ['50%', '20%', '10%', '3,5%', '1%'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la costa se caracteriza por '
                             'ser:',
                 'alternativas': ['Migratoria',
                                  'Intensiva, tecnificada y mecanizada',
                                  'De subsistencia exclusiva',
                                  'Sin uso de maquinaria',
                                  'Extensiva y tradicional'],
                 'correcta': 'B'},
                {'pregunta': 'En la costa se pueden obtener anualmente:',
                 'alternativas': ['Cosechas cada dos años',
                                  'Una cosecha',
                                  'Ninguna cosecha regular',
                                  'Hasta dos cosechas',
                                  'Tres cosechas mínimo'],
                 'correcta': 'D'},
                {'pregunta': 'En la costa predominan los cultivos '
                             'industriales como la caña de azúcar y:',
                 'alternativas': ['La cañihua',
                                  'La papa',
                                  'El olluco',
                                  'El algodón',
                                  'La quinua'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la costa goza de asistencia:',
                 'alternativas': ['Solo comunal',
                                  'Internacional exclusiva',
                                  'Religiosa',
                                  'Crediticia por bancos y entidades '
                                  'financieras',
                                  'Militar'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la región andina se '
                             'caracteriza por ser:',
                 'alternativas': ['Industrial',
                                  'Intensiva y mecanizada',
                                  'Extensiva y tradicional',
                                  'De exportación masiva',
                                  'Altamente tecnificada'],
                 'correcta': 'C'},
                {'pregunta': 'En la región andina, el cultivo se realiza '
                             'principalmente en época de:',
                 'alternativas': ['Granizo',
                                  'Lluvias',
                                  'Neblina',
                                  'Helada',
                                  'Sequía'],
                 'correcta': 'B'},
                {'pregunta': 'Una herramienta tradicional de la agricultura '
                             'andina es:',
                 'alternativas': ['La fumigadora',
                                  'La bomba hidráulica',
                                  'La chaquitaclla',
                                  'La avioneta agrícola',
                                  'El tractor'],
                 'correcta': 'C'},
                {'pregunta': 'La agricultura andina está orientada '
                             'principalmente al cultivo de productos de:',
                 'alternativas': ['Alta rentabilidad para exportación',
                                  'Solo productos industriales',
                                  'Solo flores ornamentales',
                                  'Baja rentabilidad, como papa, maíz y '
                                  'cebada',
                                  'Solo productos tropicales'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la selva se caracteriza por '
                             'ser:',
                 'alternativas': ['Intensiva y mecanizada',
                                  'Altamente tecnificada',
                                  'Migratoria',
                                  'Sin degradación de suelos',
                                  'Exportadora exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La técnica de roce, tumba y quema se practica '
                             'en la agricultura de:',
                 'alternativas': ['Las lomas costeras',
                                  'El litoral',
                                  'La costa',
                                  'La región andina alta',
                                  'La selva'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los cultivos industriales de la selva '
                             'figuran la coca, el café y:',
                 'alternativas': ['La cebada',
                                  'El trigo',
                                  'La papa',
                                  'El olluco',
                                  'El tabaco'],
                 'correcta': 'E'},
                {'pregunta': 'En la selva alta existen valles permanentes de '
                             'cultivo como Jaén, Bagua y:',
                 'alternativas': ['Arequipa',
                                  'Ica',
                                  'Tacna',
                                  'Piura',
                                  'Chanchamayo'],
                 'correcta': 'E'},
                {'pregunta': 'La agricultura de la selva está relacionada '
                             'con la depredación de:',
                 'alternativas': ['El aire',
                                  'El suelo',
                                  'El mar',
                                  'Los minerales',
                                  'El agua'],
                 'correcta': 'B'},
                {'pregunta': 'En el antiguo Perú se cultivaba, entre otros '
                             'productos:',
                 'alternativas': ['Trigo y cebada',
                                  'Algodón egipcio',
                                  'Café y tabaco',
                                  'Arroz y caña de azúcar',
                                  'Papa, quinua y oca'],
                 'correcta': 'E'},
                {'pregunta': 'Las tierras aptas para cultivo en el Perú '
                             'alcanzan aproximadamente:',
                 'alternativas': ['1 millón de hectáreas',
                                  '20 millones de hectáreas',
                                  '7,6 millones de hectáreas',
                                  '15 millones de hectáreas',
                                  '500 mil hectáreas'],
                 'correcta': 'C'},
                {'pregunta': 'Un factor limitante de la agricultura en la '
                             'selva es:',
                 'alternativas': ['El exceso de crédito bancario',
                                  'La limitación en transporte y '
                                  'comercialización',
                                  'El exceso de tecnología',
                                  'La sobreproducción',
                                  'El exceso de maquinaria'],
                 'correcta': 'B'},
                {'pregunta': 'Una característica de la ganadería de la selva '
                             'es: (I CEPRU 2024)',
                 'alternativas': ['Extensiva y experimental',
                                  'Intensiva y experimental',
                                  'Extensiva y migratoria',
                                  'Intensiva y migratoria',
                                  'Intensiva y extensiva'],
                 'correcta': 'C'},
                {'pregunta': 'La especie exótica de mayor reproducción '
                             'acuícola en la región andina corresponde a la: '
                             '(Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Gamitana',
                                  'Palometa',
                                  'Llambina',
                                  'Ractacara',
                                  'Trucha'],
                 'correcta': 'E'},
                {'pregunta': 'La actividad económica reproductiva que '
                             'consiste en la crianza, selección y '
                             'reproducción de animales domésticos se llama:',
                 'alternativas': ['Pesca',
                                  'Agricultura',
                                  'Silvicultura',
                                  'Ganadería',
                                  'Apicultura'],
                 'correcta': 'D'},
                {'pregunta': 'La ganadería de la costa peruana se '
                             'caracteriza por ser predominantemente:',
                 'alternativas': ['Nómada',
                                  'De subsistencia',
                                  'Intensiva y tecnificada',
                                  'Migratoria',
                                  'Extensiva y tradicional'],
                 'correcta': 'C'},
                {'pregunta': 'El ganado de baja productividad, criado de '
                             'forma extensiva y tradicional en la región '
                             'andina, se llama ganado:',
                 'alternativas': ['Amazonas',
                                  'Fino',
                                  'Brown Swiss',
                                  'Cebú',
                                  'Chusco o criollo'],
                 'correcta': 'E'},
                {'pregunta': 'En la región andina predomina la crianza de '
                             'ganado ovino, vacuno y:',
                 'alternativas': ['Porcino',
                                  'Equino exclusivo',
                                  'Camélidos',
                                  'Aves de corral',
                                  'Caprino exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'La raza de ganado vacuno desarrollada en la '
                             'selva peruana, cruce de Cebú hembra con Brown '
                             'Swiss, se llama raza:',
                 'alternativas': ['Holstein',
                                  'Angus',
                                  'Chusca',
                                  'Amazonas',
                                  'Criolla'],
                 'correcta': 'D'},
                {'pregunta': 'Al 2022, el principal departamento productor '
                             'de ganado vacuno del Perú es:',
                 'alternativas': ['Lima',
                                  'Huánuco',
                                  'Cusco',
                                  'Puno',
                                  'Cajamarca'],
                 'correcta': 'B'},
                {'pregunta': 'Al 2022, el principal departamento productor '
                             'de ganado ovino, alpaca y llama del Perú es:',
                 'alternativas': ['Apurímac',
                                  'Arequipa',
                                  'Puno',
                                  'Huancavelica',
                                  'Cusco'],
                 'correcta': 'C'},
                {'pregunta': 'La ganadería contamina el agua subterránea '
                             'principalmente por los purines o residuos '
                             'fecales, que aumentan la concentración de:',
                 'alternativas': ['Carbonatos',
                                  'Fosfatos',
                                  'Nitratos',
                                  'Sulfatos',
                                  'Cloruros'],
                 'correcta': 'C'},
                {'pregunta': 'Según la FAO, el porcentaje de gases de efecto '
                             'invernadero generado por el sector ganadero, '
                             'mayor que el del transporte, es:',
                 'alternativas': ['30%', '10%', '25%', '18%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'Al digerir alimentos, los animales de '
                             'ganadería producen grandes cantidades de un '
                             'potente gas de efecto invernadero llamado:',
                 'alternativas': ['Monóxido de carbono',
                                  'Óxido nitroso',
                                  'Ozono',
                                  'Dióxido de carbono',
                                  'Metano'],
                 'correcta': 'E'},
                {'pregunta': 'La ganadería utiliza aproximadamente qué '
                             'porcentaje de la superficie terrestre del '
                             'planeta:',
                 'alternativas': ['10%', '70%', '50%', '30%', '90%'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'LA AGRICULTURA EN EL PERÚ',
                      'items': ['La agricultura es la actividad económica '
                                'reproductiva que consiste en el cultivo del '
                                'suelo para obtener plantas alimenticias e '
                                'industriales.',
                                'Los españoles trajeron el arado de tracción '
                                'animal y nuevas especies como el arroz, '
                                'cebada, caña de azúcar y trigo.',
                                'Según la FAO, el Perú tiene en cultivo '
                                'aproximadamente 4,4 millones de hectáreas, '
                                'el 3,5% del área total del territorio.']},
                     {'titulo': 'LA AGRICULTURA EN LA COSTA',
                      'items': ['La agricultura de la costa es intensiva, ya '
                                'que el suelo no descansa, obteniéndose '
                                'hasta dos cosechas anuales.',
                                'La agricultura costeña es tecnificada y '
                                'mecanizada, con uso de tractores y '
                                'fumigadoras.',
                                'En la costa predominan los cultivos '
                                'industriales y para la exportación, como la '
                                'caña de azúcar y el algodón.',
                                'La agricultura costeña goza de asistencia '
                                'crediticia por parte de bancos y entidades '
                                'financieras.']},
                     {'titulo': 'LA AGRICULTURA EN LA REGIÓN ANDINA',
                      'items': ['La agricultura andina es extensiva, porque '
                                'el suelo descansa y solo se cultiva en '
                                'época de lluvias.',
                                'La agricultura andina es tradicional, no '
                                'tecnificada, guiada por la experiencia de '
                                'los campesinos.',
                                'La agricultura andina no es mecanizada; se '
                                'usan herramientas tradicionales como la '
                                'chaquitaclla.',
                                'La agricultura andina está orientada al '
                                'cultivo de plantas de baja rentabilidad, '
                                'como la papa, el maíz y la cebada.']},
                     {'titulo': 'LA AGRICULTURA EN LA SELVA',
                      'items': ['La agricultura en la selva es migratoria: '
                                'los suelos se degradan rápidamente y se '
                                'practica el roce, tumba y quema.',
                                'La agricultura selvática está orientada al '
                                'cultivo de arroz, yuca y plátano, además de '
                                'cultivos industriales como coca, café y '
                                'tabaco.',
                                'En la selva alta existen valles permanentes '
                                'de cultivo como Jaén, Bagua y '
                                'Chanchamayo.']},
                     {'titulo': 'LA GANADERÍA EN EL PERÚ: CONCEPTO Y '
                                'REGIONES',
                      'items': ['La ganadería es la actividad económica '
                                'reproductiva que consiste en la crianza, '
                                'selección y reproducción de animales '
                                'domésticos, llamados ganado.',
                                'La ganadería de la costa es '
                                'predominantemente intensiva, tecnificada y '
                                'científica; predomina el ganado vacuno '
                                'fino, aves de corral y porcinos.',
                                'La ganadería de la región andina es '
                                'predominantemente extensiva y tradicional; '
                                'se cría ganado chusco o criollo de baja '
                                'productividad.',
                                'En la región andina predomina la crianza de '
                                'ganado ovino, camélidos y vacuno; se '
                                'desarrolla en mesetas, punas y valles '
                                'interandinos.',
                                'La ganadería de la selva es extensiva y de '
                                'experimentación; predomina el ganado vacuno '
                                'de raza Amazonas (cruce de Cebú con Brown '
                                'Swiss).']},
                     {'titulo': 'PRINCIPALES DEPARTAMENTOS PRODUCTORES DE '
                                'GANADO',
                      'items': ['Al 2022, Huánuco es el principal productor '
                                'de ganado vacuno; Puno lidera en ovino, '
                                'alpaca y llama.',
                                'Lima es el principal productor de ganado '
                                'porcino y de aves; Piura lidera en '
                                'producción caprina.']},
                     {'titulo': 'IMPACTO AMBIENTAL DE LA GANADERÍA',
                      'items': ['La ganadería contamina el agua subterránea '
                                'por los purines o residuos fecales de las '
                                'granjas, aumentando la concentración de '
                                'nitratos.',
                                'Según la FAO, el sector ganadero genera el '
                                '18% de los gases de efecto invernadero, más '
                                'que el sector transporte.',
                                'Los animales, al digerir alimentos, '
                                'producen grandes cantidades de metano, un '
                                'potente gas de efecto invernadero.',
                                'La ganadería utiliza el 30% de la '
                                'superficie terrestre del planeta; en el '
                                'Amazonas, el 70% de los bosques '
                                'desaparecidos se dedicaron a pastizales.']}],
  'qr_reto': [{'pregunta': 'Según la FAO, el Perú tiene en cultivo '
                           'aproximadamente:',
               'respuesta': '4,4 millones de hectáreas'},
              {'pregunta': 'La agricultura de la región andina se '
                           'caracteriza por ser:',
               'respuesta': 'Extensiva y tradicional'},
              {'pregunta': 'En el antiguo Perú se cultivaba, entre otros '
                           'productos:',
               'respuesta': 'Papa, quinua y oca'}],
  'qr_dato': 'La agricultura costeña goza de asistencia crediticia por parte '
             'de bancos y entidades financieras.'},
 {'num': 16,
  'titulo': 'Actividades del Transporte en el Perú',
  'secciones': [{'titulo': '16.1 CARRETERAS LONGITUDINALES DEL PERÚ',
                 'items': ['El Perú cuenta con {seis} carreteras '
                           'longitudinales principales, que recorren de '
                           'norte a sur las tres regiones naturales.',
                           'La {Carretera Longitudinal de la Costa} se '
                           'divide en tramo norte (Tumbes-Lima) y tramo '
                           '{sur} (Lima-Tacna, frontera con Chile).',
                           'La {Carretera Longitudinal de la Sierra} se '
                           'divide en tramo norte (La Oroya-Ayabaca, '
                           'frontera con Ecuador) y tramo {sur} (La '
                           'Oroya-Desaguadero, frontera con Bolivia).',
                           'La {Carretera Longitudinal de la Selva} se '
                           'divide en tramo norte (Chanchamayo-La Balsa, '
                           'frontera con Ecuador) y tramo {sur} '
                           '(Chanchamayo-Río Heath, frontera con Bolivia).']},
                {'titulo': '16.2 PRINCIPALES AEROPUERTOS DEL PERÚ',
                 'items': ['El aeropuerto internacional {Jorge Chávez}, en '
                           'el Callao, es el principal aeropuerto del Perú.',
                           'El aeropuerto {Rodríguez Ballón} está en '
                           'Arequipa; el {Alejandro Velasco Astete}, en '
                           'Cusco.',
                           'El aeropuerto {José Abelardo Quiñones} está en '
                           'Chiclayo; el {Inca Manco Cápac}, en Juliaca, '
                           'Puno.',
                           'El aeropuerto {Francisco Secada Vignetta} está '
                           'en Iquitos, Loreto; el {María Reiche Neuman}, en '
                           'Nasca, Ica.',
                           'El aeropuerto {Carlos Martínez de Pinillos} está '
                           'en Trujillo, La Libertad; el {Padre Aldamiz}, en '
                           'Puerto Maldonado.']}],
  'cuadros': [],
  'preguntas': [{'pregunta': 'El Perú cuenta con un número de carreteras '
                             'longitudinales principales igual a:',
                 'alternativas': ['Cuatro', 'Ocho', 'Tres', 'Diez', 'Seis'],
                 'correcta': 'E'},
                {'pregunta': 'La Carretera Longitudinal de la Costa Sur va '
                             'desde Lima hasta la ciudad de Tacna, en la '
                             'frontera con:',
                 'alternativas': ['Ecuador',
                                  'Bolivia',
                                  'Colombia',
                                  'Chile',
                                  'Brasil'],
                 'correcta': 'D'},
                {'pregunta': 'La Carretera Longitudinal de la Sierra Sur '
                             'llega hasta Desaguadero, en la frontera con:',
                 'alternativas': ['Ecuador',
                                  'Bolivia',
                                  'Colombia',
                                  'Brasil',
                                  'Chile'],
                 'correcta': 'B'},
                {'pregunta': 'La Carretera Longitudinal de la Selva Norte '
                             'llega hasta el Puente Internacional La Balsa, '
                             'en la frontera con:',
                 'alternativas': ['Chile',
                                  'Brasil',
                                  'Bolivia',
                                  'Ecuador',
                                  'Colombia'],
                 'correcta': 'D'},
                {'pregunta': 'El aeropuerto internacional Inca Manco Cápac '
                             'está ubicado en la ciudad de:',
                 'alternativas': ['Tacna',
                                  'Arequipa',
                                  'Cusco',
                                  'Juliaca',
                                  'Puno capital'],
                 'correcta': 'D'},
                {'pregunta': 'El aeropuerto internacional Francisco Secada '
                             'Vignetta está ubicado en la ciudad de:',
                 'alternativas': ['Tarapoto',
                                  'Tingo María',
                                  'Iquitos',
                                  'Yurimaguas',
                                  'Pucallpa'],
                 'correcta': 'C'},
                {'pregunta': 'El aeropuerto María Reiche Neuman, llamado así '
                             'en honor a la investigadora de las líneas de '
                             'Nasca, está ubicado en:',
                 'alternativas': ['Nasca',
                                  'Chincha',
                                  'Ica capital',
                                  'Palpa',
                                  'Pisco'],
                 'correcta': 'A'},
                {'pregunta': 'El aeropuerto internacional Padre Aldamiz está '
                             'ubicado en la ciudad de:',
                 'alternativas': ['Tarapoto',
                                  'Puerto Maldonado',
                                  'Atalaya',
                                  'Pucallpa',
                                  'Iquitos'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto internacional más importante del '
                             'Perú después de Jorge Chávez es: (II CEPRU '
                             '2025)',
                 'alternativas': ['Alfredo Rodríguez Ballón',
                                  'Carlos Martínez de Pinillos',
                                  'Alejandro Velasco Astete',
                                  'José Abelardo Quiñones',
                                  'Inca Manco Cápac'],
                 'correcta': 'C'},
                {'pregunta': 'La carretera más importante del Perú es la: (I '
                             'CEPRU 2024)',
                 'alternativas': ['Panamericana',
                                  'Marginal de la selva',
                                  'De enlace',
                                  'De penetración',
                                  'Interoceánica'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CARRETERAS LONGITUDINALES DEL PERÚ',
                      'items': ['El Perú cuenta con seis carreteras '
                                'longitudinales principales, que recorren de '
                                'norte a sur las tres regiones naturales.',
                                'La Carretera Longitudinal de la Costa se '
                                'divide en tramo norte (Tumbes-Lima) y tramo '
                                'sur (Lima-Tacna, frontera con Chile).',
                                'La Carretera Longitudinal de la Sierra se '
                                'divide en tramo norte (La Oroya-Ayabaca, '
                                'frontera con Ecuador) y tramo sur (La '
                                'Oroya-Desaguadero, frontera con Bolivia).',
                                'La Carretera Longitudinal de la Selva se '
                                'divide en tramo norte (Chanchamayo-La '
                                'Balsa, frontera con Ecuador) y tramo sur '
                                '(Chanchamayo-Río Heath, frontera con '
                                'Bolivia).']},
                     {'titulo': 'PRINCIPALES AEROPUERTOS DEL PERÚ',
                      'items': ['El aeropuerto internacional Jorge Chávez, '
                                'en el Callao, es el principal aeropuerto '
                                'del Perú.',
                                'El aeropuerto Rodríguez Ballón está en '
                                'Arequipa; el Alejandro Velasco Astete, en '
                                'Cusco.',
                                'El aeropuerto José Abelardo Quiñones está '
                                'en Chiclayo; el Inca Manco Cápac, en '
                                'Juliaca, Puno.',
                                'El aeropuerto Francisco Secada Vignetta '
                                'está en Iquitos, Loreto; el María Reiche '
                                'Neuman, en Nasca, Ica.',
                                'El aeropuerto Carlos Martínez de Pinillos '
                                'está en Trujillo, La Libertad; el Padre '
                                'Aldamiz, en Puerto Maldonado.']}],
  'qr_reto': [{'pregunta': 'El aeropuerto internacional Padre Aldamiz está '
                           'ubicado en la ciudad de:',
               'respuesta': 'Puerto Maldonado'},
              {'pregunta': 'El aeropuerto internacional Francisco Secada '
                           'Vignetta está ubicado en la ciudad de:',
               'respuesta': 'Iquitos'},
              {'pregunta': 'La Carretera Longitudinal de la Sierra Sur llega '
                           'hasta Desaguadero, en la frontera con:',
               'respuesta': 'Bolivia'}],
  'qr_dato': 'La Carretera Longitudinal de la Costa se divide en tramo norte '
             '(Tumbes-Lima) y tramo sur (Lima-Tacna, frontera con Chile).'},
 {'num': 17,
  'titulo': 'Geografía Política del Perú y Gestión Territorial',
  'secciones': [{'titulo': '17.1 GEOGRAFÍA POLÍTICA',
                 'items': ['La geografía política estudia la organización '
                           'política y administrativa de los Estados, sus '
                           'formas de {gobierno}, fronteras y relaciones con '
                           'otros Estados.',
                           'Según el artículo {189} de la Constitución, el '
                           'territorio de la República está integrado por '
                           'regiones, departamentos, {provincias} y '
                           'distritos.']},
                {'titulo': '17.2 DIVISIÓN POLÍTICA DEL PERÚ',
                 'items': ['El territorio peruano está dividido en 25 '
                           'regiones, {24} departamentos, 195 provincias más '
                           'la provincia constitucional del {Callao}, y '
                           '{1874} distritos.',
                           'El departamento más extenso del Perú es '
                           '{Loreto}, con 368 851 km².',
                           'La capital del departamento de {Cusco} es la '
                           'ciudad del Cusco, con 71 891 km² de área y 3399 '
                           'm de altitud.']},
                {'titulo': '17.3 CENTRALISMO, DESCENTRALIZACIÓN Y '
                           'REGIONALIZACIÓN',
                 'items': ['El {centralismo} es el sistema donde el poder '
                           'político, administrativo y económico emana del '
                           'gobierno central.',
                           'Según el artículo {188} de la Constitución, la '
                           'descentralización es una forma de organización '
                           'democrática y una política permanente de '
                           'carácter {obligatorio}.',
                           'La descentralización se refiere a la '
                           'transferencia de facultades y {competencias} del '
                           'gobierno central hacia las instancias '
                           'descentralizadas.',
                           'La {regionalización} busca la conformación de '
                           'regiones con autonomía administrativa, económica '
                           'y {política}.']},
                {'titulo': '17.4 CATEGORÍAS DE LOS CENTROS POBLADOS',
                 'items': ['El {caserío} concentra una población de 151 a '
                           '{1000} habitantes, con viviendas continuas o '
                           'dispersas.',
                           'El {pueblo} concentra una población de 1001 a '
                           '{2500} habitantes, con calles y plaza céntrica; '
                           'tiene institución educativa primaria completa.',
                           'La {villa} concentra una población de 2501 a '
                           '{5000} habitantes, con Plan de Ordenamiento '
                           'Urbano; tiene primaria completa y 3 grados de '
                           'secundaria.',
                           'La {ciudad} concentra una población de 5001 a '
                           '{500 000} habitantes; se clasifica en menores, '
                           'intermedias y mayores.',
                           'La {metrópoli} concentra una población de {500 '
                           '001} habitantes a más; presenta Plan de '
                           'Desarrollo Metropolitano.',
                           'La {comunidad campesina}, según la Ley {24656}, '
                           'es una organización de interés público integrada '
                           'por familias ligadas por vínculos ancestrales.',
                           'Según estudios de la UNMSM, a nivel distrital el '
                           '{80}% de las capitales tienen la categoría de '
                           'pueblo.']}],
  'cuadros': [{'titulo': '17.2 DEPARTAMENTOS DESTACADOS DEL PERÚ',
               'encabezados': ['Departamento', 'Capital', 'Área km²'],
               'filas': [['{Loreto}', 'Iquitos', '368 851'],
                         ['{Cusco}', 'Cusco', '71 891'],
                         ['{Arequipa}', 'Arequipa', '63 345'],
                         ['{Lima}', 'Lima', '34 801'],
                         ['{Tumbes}', 'Tumbes', '4 669']]}],
  'preguntas': [{'pregunta': 'La geografía política estudia la organización '
                             'política y administrativa de:',
                 'alternativas': ['Solo las ciudades',
                                  'Solo los ríos',
                                  'Los Estados de la Tierra',
                                  'Solo el clima',
                                  'Solo el relieve'],
                 'correcta': 'C'},
                {'pregunta': 'El territorio de la República peruana está '
                             'integrado, según el artículo 189, por '
                             'regiones, departamentos, provincias y:',
                 'alternativas': ['Centros poblados solamente',
                                  'Comunidades',
                                  'Anexos',
                                  'Distritos',
                                  'Caseríos exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'El Perú está dividido en un número de '
                             'departamentos igual a:',
                 'alternativas': ['20', '28', '25', '24', '30'],
                 'correcta': 'D'},
                {'pregunta': 'Además de los departamentos, el Perú tiene una '
                             'provincia constitucional, que es:',
                 'alternativas': ['Cusco',
                                  'El Callao',
                                  'Lima',
                                  'Arequipa',
                                  'Trujillo'],
                 'correcta': 'B'},
                {'pregunta': 'El número total de distritos del Perú es '
                             'aproximadamente:',
                 'alternativas': ['1000', '1874', '800', '2500', '500'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento más extenso del Perú es:',
                 'alternativas': ['Puno',
                                  'Loreto',
                                  'Ucayali',
                                  'Cusco',
                                  'Arequipa'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del departamento de Loreto es:',
                 'alternativas': ['Iquitos',
                                  'Yurimaguas',
                                  'Tarapoto',
                                  'Moyobamba',
                                  'Pucallpa'],
                 'correcta': 'A'},
                {'pregunta': 'El departamento de Cusco tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['20 000 km²',
                                  '100 000 km²',
                                  '71 891 km²',
                                  '35 000 km²',
                                  '50 000 km²'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema donde el poder emana del gobierno '
                             'central se denomina:',
                 'alternativas': ['Regionalización',
                                  'Descentralización',
                                  'Federalismo',
                                  'Centralismo',
                                  'Municipalismo'],
                 'correcta': 'D'},
                {'pregunta': 'La descentralización está regulada en el '
                             'artículo de la Constitución número:',
                 'alternativas': ['188', '91', '189', '201', '24'],
                 'correcta': 'A'},
                {'pregunta': 'Según el artículo 188, la descentralización es '
                             'una forma de organización:',
                 'alternativas': ['Democrática',
                                  'Militar',
                                  'Monárquica',
                                  'Religiosa',
                                  'Autoritaria'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización es considerada una '
                             'política permanente de carácter:',
                 'alternativas': ['Provincial',
                                  'Opcional',
                                  'Regional exclusivo',
                                  'Obligatorio',
                                  'Temporal'],
                 'correcta': 'D'},
                {'pregunta': 'El proceso de descentralización se realiza:',
                 'alternativas': ['Por etapas, en forma progresiva y '
                                  'ordenada',
                                  'De forma inmediata y única',
                                  'De manera aleatoria',
                                  'Sin ningún criterio técnico',
                                  'Solo en Lima'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización implica la transferencia '
                             'de recursos del gobierno nacional hacia:',
                 'alternativas': ['Solo las universidades',
                                  'Solo el sector privado',
                                  'Organismos internacionales',
                                  'Los gobiernos regionales y locales',
                                  'Solo las Fuerzas Armadas'],
                 'correcta': 'D'},
                {'pregunta': 'La regionalización busca la conformación de '
                             'regiones con autonomía:',
                 'alternativas': ['Solo económica',
                                  'Ninguna autonomía real',
                                  'Solo política',
                                  'Administrativa, económica y política',
                                  'Solo administrativa'],
                 'correcta': 'D'},
                {'pregunta': 'El objetivo fundamental de la '
                             'descentralización es:',
                 'alternativas': ['Aumentar la burocracia central',
                                  'Eliminar los gobiernos regionales',
                                  'El desarrollo integral del país',
                                  'Reducir la participación ciudadana',
                                  'Concentrar el poder en Lima'],
                 'correcta': 'C'},
                {'pregunta': 'La capital del departamento de Arequipa es:',
                 'alternativas': ['Camaná',
                                  'Chivay',
                                  'Arequipa',
                                  'Mollendo',
                                  'Islay'],
                 'correcta': 'C'},
                {'pregunta': 'La capital del departamento de Áncash es:',
                 'alternativas': ['Chimbote',
                                  'Huaraz',
                                  'Casma',
                                  'Huarmey',
                                  'Recuay'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento de Tumbes tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['100 000 km²',
                                  '4 669 km²',
                                  '1 000 km²',
                                  '50 000 km²',
                                  '15 000 km²'],
                 'correcta': 'B'},
                {'pregunta': 'En la provincia de La Convención, Cusco, se '
                             'crearon recientemente los distritos de Villa '
                             'Virgen, Villa Kintiarina, Incahuasi y:',
                 'alternativas': ['Megantoni',
                                  'Calca',
                                  'Ollantaytambo',
                                  'Anta',
                                  'Urubamba'],
                 'correcta': 'A'},
                {'pregunta': 'El proceso técnico-geográfico para delimitar '
                             'los distritos, provincias y demás áreas '
                             'geográficas se llama: (II CEPRU 2024)',
                 'alternativas': ['Regionalización',
                                  'Gestión territorial',
                                  'Ordenamiento territorial',
                                  'Zonificación ecológica y económica',
                                  'Demarcación territorial'],
                 'correcta': 'E'},
                {'pregunta': 'Los niveles de estudio de la Zonificación '
                             'Ecológica y Económica (ZEE) son ejecutados en '
                             'tres niveles, estos son: (I CEPRU 2024)',
                 'alternativas': ['Microzonificación, mesozonificación y '
                                  'macrozonificación',
                                  'Macrozonificación, descentralización y '
                                  'regionalización',
                                  'Departamental, provincial y distrital',
                                  'Centralismo, descentralización y '
                                  'regionalización',
                                  'Microzonificación, centralismo y '
                                  'descentralización'],
                 'correcta': 'A'},
                {'pregunta': 'El nivel de estudio de la ZEE que contribuye a '
                             'la elaboración de políticas y planes de '
                             'desarrollo en el ámbito local o distrital, con '
                             'escala 1:25 000, es el nivel de: (II CEPRU '
                             '2022)',
                 'alternativas': ['Demarcación territorial',
                                  'Mesozonificación',
                                  'Microzonificación',
                                  'Macrozonificación',
                                  'Zonificación extra'],
                 'correcta': 'C'},
                {'pregunta': 'El centro poblado que concentra una población '
                             'de 151 a 1000 habitantes se llama:',
                 'alternativas': ['Ciudad',
                                  'Pueblo',
                                  'Caserío',
                                  'Metrópoli',
                                  'Villa'],
                 'correcta': 'C'},
                {'pregunta': 'El centro poblado que concentra una población '
                             'de 1001 a 2500 habitantes, con calles y plaza '
                             'céntrica, se llama:',
                 'alternativas': ['Metrópoli',
                                  'Pueblo',
                                  'Caserío',
                                  'Villa',
                                  'Ciudad'],
                 'correcta': 'B'},
                {'pregunta': 'El centro poblado que concentra una población '
                             'de 2501 a 5000 habitantes, con Plan de '
                             'Ordenamiento Urbano, se llama:',
                 'alternativas': ['Villa',
                                  'Ciudad',
                                  'Metrópoli',
                                  'Caserío',
                                  'Pueblo'],
                 'correcta': 'A'},
                {'pregunta': 'El centro poblado con viviendas dispersas y '
                             'población menor a mil habitantes se denomina:',
                 'alternativas': ['Ciudadela',
                                  'Ciudad',
                                  'Villa',
                                  'Metrópoli',
                                  'Caserío'],
                 'correcta': 'E'},
                {'pregunta': 'El centro poblado que concentra una población '
                             'de 500 001 habitantes a más, con Plan de '
                             'Desarrollo Metropolitano, se llama:',
                 'alternativas': ['Pueblo',
                                  'Ciudad intermedia',
                                  'Metrópoli',
                                  'Ciudad mayor',
                                  'Villa'],
                 'correcta': 'C'},
                {'pregunta': 'Según la Ley 24656, la organización de interés '
                             'público integrada por familias ligadas por '
                             'vínculos ancestrales que controlan un '
                             'territorio se llama:',
                 'alternativas': ['Comunidad campesina',
                                  'Anexo',
                                  'Junta vecinal',
                                  'Municipalidad',
                                  'Cooperativa'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'GEOGRAFÍA POLÍTICA',
                      'items': ['La geografía política estudia la '
                                'organización política y administrativa de '
                                'los Estados, sus formas de gobierno, '
                                'fronteras y relaciones con otros Estados.',
                                'Según el artículo 189 de la Constitución, '
                                'el territorio de la República está '
                                'integrado por regiones, departamentos, '
                                'provincias y distritos.']},
                     {'titulo': 'DIVISIÓN POLÍTICA DEL PERÚ',
                      'items': ['El territorio peruano está dividido en 25 '
                                'regiones, 24 departamentos, 195 provincias '
                                'más la provincia constitucional del Callao, '
                                'y 1874 distritos.',
                                'El departamento más extenso del Perú es '
                                'Loreto, con 368 851 km².',
                                'La capital del departamento de Cusco es la '
                                'ciudad del Cusco, con 71 891 km² de área y '
                                '3399 m de altitud.']},
                     {'titulo': 'CENTRALISMO, DESCENTRALIZACIÓN Y '
                                'REGIONALIZACIÓN',
                      'items': ['El centralismo es el sistema donde el poder '
                                'político, administrativo y económico emana '
                                'del gobierno central.',
                                'Según el artículo 188 de la Constitución, '
                                'la descentralización es una forma de '
                                'organización democrática y una política '
                                'permanente de carácter obligatorio.',
                                'La descentralización se refiere a la '
                                'transferencia de facultades y competencias '
                                'del gobierno central hacia las instancias '
                                'descentralizadas.',
                                'La regionalización busca la conformación de '
                                'regiones con autonomía administrativa, '
                                'económica y política.']},
                     {'titulo': 'CATEGORÍAS DE LOS CENTROS POBLADOS',
                      'items': ['El caserío concentra una población de 151 a '
                                '1000 habitantes, con viviendas continuas o '
                                'dispersas.',
                                'El pueblo concentra una población de 1001 a '
                                '2500 habitantes, con calles y plaza '
                                'céntrica; tiene institución educativa '
                                'primaria completa.',
                                'La villa concentra una población de 2501 a '
                                '5000 habitantes, con Plan de Ordenamiento '
                                'Urbano; tiene primaria completa y 3 grados '
                                'de secundaria.',
                                'La ciudad concentra una población de 5001 a '
                                '500 000 habitantes; se clasifica en '
                                'menores, intermedias y mayores.',
                                'La metrópoli concentra una población de 500 '
                                '001 habitantes a más; presenta Plan de '
                                'Desarrollo Metropolitano.',
                                'La comunidad campesina, según la Ley 24656, '
                                'es una organización de interés público '
                                'integrada por familias ligadas por vínculos '
                                'ancestrales.',
                                'Según estudios de la UNMSM, a nivel '
                                'distrital el 80% de las capitales tienen la '
                                'categoría de pueblo.']}],
  'qr_reto': [{'pregunta': 'El nivel de estudio de la ZEE que contribuye a '
                           'la elaboración de políticas y planes de '
                           'desarrollo en el ámbito local o distrital, con '
                           'escala 1:25 000, es el nivel de:',
               'respuesta': 'Microzonificación'},
              {'pregunta': 'La descentralización implica la transferencia de '
                           'recursos del gobierno nacional hacia:',
               'respuesta': 'Los gobiernos regionales y locales'},
              {'pregunta': 'El departamento de Tumbes tiene una extensión '
                           'aproximada de:',
               'respuesta': '4 669 km²'}],
  'qr_dato': 'La geografía política estudia la organización política y '
             'administrativa de los Estados, sus formas de gobierno, '
             'fronteras y relaciones con otros Estados.'},
 {'num': 18,
  'titulo': 'Espacio Geográfico Físico del Cusco',
  'secciones': [{'titulo': '18.1 LOCALIZACIÓN Y EXTENSIÓN',
                 'items': ['El departamento del Cusco se ubica en la parte '
                           '{sur-oriental} del Perú, entre la Cordillera de '
                           'los Andes, la Selva Alta y la Selva Baja.',
                           'La superficie total del departamento del Cusco '
                           'es de {72 364} km², representando el {5,6}% del '
                           'territorio nacional.',
                           'El punto más alto del departamento es el nevado '
                           '{Ausangate}, a 6364 m de altitud.',
                           'El punto más bajo del Cusco se ubica en la '
                           'provincia de {La Convención}, a 180 m, en el '
                           'límite con Ucayali.']},
                {'titulo': '18.2 LÍMITES DEL DEPARTAMENTO',
                 'items': ['El Cusco limita por el norte con {Ucayali}, por '
                           'el noroeste con Junín, y por el noreste con '
                           '{Madre de Dios}.',
                           'El Cusco limita por el sur con {Arequipa}, por '
                           'el este y sureste con Puno, por el oeste con '
                           'Ayacucho y por el suroeste con {Apurímac}.']},
                {'titulo': '18.3 REGIONES NATURALES DEL CUSCO',
                 'items': ['La región {Andina} o Sierra representa el {53}% '
                           'del territorio del departamento del Cusco.',
                           'La {Selva Alta} o Faja Sub Andina representa el '
                           '{28}% del territorio cusqueño.',
                           'La {Selva Baja} o llanura representa el {19}% '
                           'del territorio del departamento.']},
                {'titulo': '18.4 DIVISIÓN POLÍTICA DEL CUSCO',
                 'items': ['El departamento del Cusco tiene {13} provincias '
                           'y {112} distritos.',
                           'La provincia con mayor extensión territorial del '
                           'Cusco es {La Convención}, con capital '
                           '{Quillabamba}, representando el 41,52% del área '
                           'departamental.',
                           'La provincia del Cusco tiene como capital la '
                           'ciudad del {Cusco}, y su distrito más poblado es '
                           '{San Sebastián}.']},
                {'titulo': '18.5 CORDILLERAS DEL DEPARTAMENTO DEL CUSCO',
                 'items': ['La cordillera {Vilcabamba} está alineada de SE a '
                           'NW; su mayor elevación es el nevado {Salkantay} '
                           '(6271 m).',
                           'La cordillera {Vilcanota-Urubamba} presenta la '
                           'mayor cantidad de glaciares de la región; su '
                           'pico más elevado es el {Ausangate} (6384 m).',
                           'En la cordillera Vilcanota se ubica el abra '
                           '{Málaga}, por donde pasa la carretera '
                           'Cusco-Quillabamba.',
                           'La cordillera {Paucartambo} está constituida por '
                           'serranías residuales, entre 3800 y 4500 m; ahí '
                           'se ubica el abra {Acjanaco}, por la carretera '
                           'Cusco-Pilcopata.']},
                {'titulo': '18.6 VALLES DEL DEPARTAMENTO DEL CUSCO',
                 'items': ['El {valle del Vilcanota-Urubamba} se extiende '
                           '480 km, desde el abra La Raya (4100 m) hasta el '
                           'pongo de {Mainique} (450 m).',
                           'El valle del Vilcanota-Urubamba concentra '
                           'aproximadamente el {79}% de la población del '
                           'departamento del Cusco, y el {75}% de sus suelos '
                           'de cultivo.',
                           'En el valle del Vilcanota se ubican los restos '
                           'arqueológicos de {Pisaq}, Ollantaytambo y '
                           'Machupicchu.',
                           'El río {Apurímac}, considerado el brazo más '
                           'extenso del río Amazonas, forma el Cañón del '
                           'Apurímac en su curso alto y medio.',
                           'El {valle del Mapacho}, o Yavero, es otra '
                           'depresión longitudinal importante, de menor '
                           'amplitud que el valle del Vilcanota.']},
                {'titulo': '18.7 RIESGO DE DESASTRES EN EL DEPARTAMENTO DEL '
                           'CUSCO',
                 'items': ['El riesgo sísmico en el Cusco se debe '
                           'principalmente a la presencia de {fallas '
                           'activas} de la edad Cuaternaria.',
                           'El {sistema de fallas del Cusco} comprende más '
                           'de 100 km, entre Abancay y Urcos, pasando cerca '
                           'de la ciudad; incluye las fallas Zurite, '
                           'Chinchero y {Tambomachay}.',
                           'El {sistema de fallas del Vilcanota} abarca '
                           'alrededor de 100 km, conformado por las fallas '
                           'Pomacanchi, Sangarará y {Langui-Layo}.',
                           'La {falla Tambomachay} tiene una longitud de 18 '
                           'km y se ubica a 7 km al norte de la ciudad del '
                           'Cusco.',
                           'El riesgo de {deslizamientos} en el Cusco se '
                           'encuentra principalmente en las quebradas y '
                           'vertientes del valle del {Watanay}.',
                           'La quebrada {Saphy} es una de las de mayor '
                           'peligro por deslizamientos, poniendo en riesgo '
                           'monumentos como la iglesia de la {Compañía} de '
                           'Jesús.']},
                {'titulo': '18.8 CONTAMINACIÓN ATMOSFÉRICA Y ACÚSTICA EN '
                           'CUSCO',
                 'items': ['La contaminación atmosférica en Cusco se vincula '
                           'a la quema de {pastizales}, el parque automotor, '
                           'y las fábricas de {ladrillos} y tejas.',
                           'A nivel del departamento del Cusco se han '
                           'identificado {473} empresas de fábricas de '
                           'ladrillos y tejas, la mayoría en el valle del '
                           'río {Watanay}.',
                           'La {contaminación acústica} en Cusco se debe al '
                           'tráfico vehicular y a la llegada y salida de '
                           'aviones del aeropuerto {Alejandro Velasco '
                           'Astete}.']},
                {'titulo': '18.9 CONTAMINACIÓN DE LOS RÍOS WATANAY Y '
                           'VILCANOTA',
                 'items': ['El río {Watanay} recibe vertidos de aguas '
                           'servidas de más de {400 000} habitantes de la '
                           'ciudad del Cusco.',
                           'La contaminación del río {Vilcanota} proviene '
                           'principalmente de vertidos urbano-domésticos y '
                           'residuos {sólidos}; el valle alberga cerca de un '
                           'millón de habitantes.',
                           'Entre los efectos de esta contaminación están la '
                           'disminución de la {fauna acuática} y '
                           'enfermedades a la piel por contacto directo.']},
                {'titulo': '18.10 DESECHOS SÓLIDOS EN LA CIUDAD DEL CUSCO',
                 'items': ['El botadero de {Jaquira}, en Santiago, forma una '
                           'montaña con más de {1,5} millones de toneladas '
                           'de desechos.',
                           'El botadero de Jaquira recibe a diario un '
                           'promedio de {380} toneladas de desechos.']}],
  'cuadros': [{'titulo': '18.3 REGIONES NATURALES DEL CUSCO',
               'encabezados': ['Región', 'Porcentaje'],
               'filas': [['{Andina} o Sierra', '{53}%'],
                         ['{Selva Alta}', '28%'],
                         ['{Selva Baja}', '{19}%']]}],
  'preguntas': [{'pregunta': 'El departamento del Cusco se ubica en la '
                             'parte:',
                 'alternativas': ['Nor-occidental del Perú',
                                  'Litoral del Perú',
                                  'Extremo norte del país',
                                  'Sur-oriental del Perú',
                                  'Centro-occidental del Perú'],
                 'correcta': 'D'},
                {'pregunta': 'La superficie del departamento del Cusco '
                             'representa del territorio nacional:',
                 'alternativas': ['1%', '20%', '10%', '15%', '5,6%'],
                 'correcta': 'E'},
                {'pregunta': 'El punto más alto del departamento del Cusco '
                             'es el nevado:',
                 'alternativas': ['Huanacaure',
                                  'Salkantay',
                                  'Veronica',
                                  'Ausangate',
                                  'Chicón'],
                 'correcta': 'D'},
                {'pregunta': 'La altitud del nevado Ausangate es '
                             'aproximadamente de:',
                 'alternativas': ['7 000 m',
                                  '5 800 m',
                                  '4 500 m',
                                  '6 364 m',
                                  '5 000 m'],
                 'correcta': 'D'},
                {'pregunta': 'El punto más bajo del departamento del Cusco '
                             'se ubica en la provincia de:',
                 'alternativas': ['Quispicanchi',
                                  'Paucartambo',
                                  'Calca',
                                  'Urubamba',
                                  'La Convención'],
                 'correcta': 'E'},
                {'pregunta': 'El departamento del Cusco limita por el norte '
                             'con:',
                 'alternativas': ['Ucayali',
                                  'Ayacucho',
                                  'Apurímac',
                                  'Arequipa',
                                  'Puno'],
                 'correcta': 'A'},
                {'pregunta': 'El departamento del Cusco limita por el sur '
                             'con:',
                 'alternativas': ['Ucayali',
                                  'Madre de Dios',
                                  'Arequipa',
                                  'Ayacucho',
                                  'Junín'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento del Cusco limita por el este y '
                             'sureste con:',
                 'alternativas': ['Junín',
                                  'Puno',
                                  'Apurímac',
                                  'Ayacucho',
                                  'Madre de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'La región andina o sierra representa del '
                             'territorio cusqueño:',
                 'alternativas': ['40%', '70%', '28%', '53%', '19%'],
                 'correcta': 'D'},
                {'pregunta': 'La selva alta o faja sub andina representa del '
                             'territorio del Cusco:',
                 'alternativas': ['10%', '19%', '5%', '28%', '53%'],
                 'correcta': 'D'},
                {'pregunta': 'La selva baja o llanura representa del '
                             'territorio cusqueño:',
                 'alternativas': ['53%', '28%', '40%', '70%', '19%'],
                 'correcta': 'E'},
                {'pregunta': 'El departamento del Cusco está dividido en un '
                             'número de provincias igual a:',
                 'alternativas': ['20', '15', '8', '10', '13'],
                 'correcta': 'E'},
                {'pregunta': 'El departamento del Cusco tiene un número de '
                             'distritos igual a:',
                 'alternativas': ['84', '100', '166', '65', '112'],
                 'correcta': 'E'},
                {'pregunta': 'La provincia más extensa del departamento del '
                             'Cusco es:',
                 'alternativas': ['Quispicanchi',
                                  'La Convención',
                                  'Cusco',
                                  'Urubamba',
                                  'Calca'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de la provincia de La Convención '
                             'es:',
                 'alternativas': ['Urubamba',
                                  'Calca',
                                  'Quillabamba',
                                  'Yanaoca',
                                  'Sicuani'],
                 'correcta': 'C'},
                {'pregunta': 'La provincia de La Convención representa del '
                             'área departamental del Cusco:',
                 'alternativas': ['20%', '10%', '41,52%', '70%', '5%'],
                 'correcta': 'C'},
                {'pregunta': 'La capital de la provincia de Canchis es:',
                 'alternativas': ['Yanaoca',
                                  'Sicuani',
                                  'Acomayo',
                                  'Anta',
                                  'Espinar'],
                 'correcta': 'B'},
                {'pregunta': 'El distrito más poblado de la provincia del '
                             'Cusco, según el censo 2017, es:',
                 'alternativas': ['San Sebastián',
                                  'Poroy',
                                  'Santiago',
                                  'Wanchaq',
                                  'Saylla'],
                 'correcta': 'A'},
                {'pregunta': 'El departamento del Cusco se caracteriza por '
                             'ser un espacio geográfico:',
                 'alternativas': ['Exclusivamente amazónico',
                                  'Homogéneo y uniforme',
                                  'Sin variedad de pisos altitudinales',
                                  'Diverso en geomorfología, clima, suelo, '
                                  'flora y fauna',
                                  'Solo desértico'],
                 'correcta': 'D'},
                {'pregunta': 'El departamento del Cusco limita por el oeste '
                             'con:',
                 'alternativas': ['Ayacucho',
                                  'Madre de Dios',
                                  'Apurímac',
                                  'Puno',
                                  'Arequipa'],
                 'correcta': 'A'},
                {'pregunta': 'La montaña de origen volcánico que domina la '
                             'ciudad del Cusco es: (II CEPRU 2025)',
                 'alternativas': ['Viva el Perú',
                                  'Wanaqauri',
                                  'Pachatusan',
                                  'Fortaleza',
                                  'Araway'],
                 'correcta': 'C'},
                {'pregunta': 'Las capitales de las provincias de '
                             'Quispicanchi, Canchis y Paruro son, '
                             'respectivamente: (II CEPRU 2024)',
                 'alternativas': ['Yauri, Sicuani y Paruro',
                                  'Urcos, Yanaoca y Paruro',
                                  'Urcos, Sicuani y Paruro',
                                  'Yanaoca, Canchis y Paruro',
                                  'Yanaoca, Sicuani y Paruro'],
                 'correcta': 'C'},
                {'pregunta': 'Constituyen parte de los distritos de la '
                             'Provincia del Cusco: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Wanchaq, Oropesa y Lucre',
                                  'Oropesa, Saylla y Poroy',
                                  'Saylla, Huasao y Tipón',
                                  'Ccorca, Saylla y Poroy',
                                  'Poroy, Huasao y Ccorca'],
                 'correcta': 'D'},
                {'pregunta': 'Las ciudades de Yanaoca y Quillabamba son las '
                             'capitales de las provincias de: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Canas y La Convención',
                                  'Canas y Urubamba',
                                  'Acomayo y Anta',
                                  'Paruro y La Convención',
                                  'Calca y La Convención'],
                 'correcta': 'A'},
                {'pregunta': 'La cordillera del Cusco cuya mayor elevación '
                             'es el nevado Salkantay (6271 m) es la:',
                 'alternativas': ['Ausangate',
                                  'Paucartambo',
                                  'Vilcabamba',
                                  'Vilcanota-Urubamba',
                                  'Carabaya'],
                 'correcta': 'C'},
                {'pregunta': 'La cordillera que presenta la mayor cantidad '
                             'de glaciares del Cusco, con el Ausangate como '
                             'pico más elevado, es la:',
                 'alternativas': ['Paucartambo',
                                  'Vilcabamba',
                                  'Vilcanota-Urubamba',
                                  'Vilcanota exclusiva',
                                  'Salkantay'],
                 'correcta': 'C'},
                {'pregunta': 'El abra por donde pasa la carretera '
                             'Cusco-Quillabamba, en la cordillera Vilcanota, '
                             'se llama:',
                 'alternativas': ['La Raya',
                                  'Málaga',
                                  'Porculla',
                                  'Acjanaco',
                                  'Anticona'],
                 'correcta': 'B'},
                {'pregunta': 'El valle del Vilcanota-Urubamba se extiende '
                             'desde el abra La Raya hasta el:',
                 'alternativas': ['Pongo de Mainique',
                                  'Valle del Mapacho',
                                  'Abra Málaga',
                                  'Cañón del Apurímac',
                                  'Cañón del Colca'],
                 'correcta': 'A'},
                {'pregunta': 'El valle del Vilcanota-Urubamba concentra '
                             'aproximadamente qué porcentaje de la población '
                             'del departamento del Cusco:',
                 'alternativas': ['95%', '30%', '60%', '79%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'El río considerado el brazo más extenso del '
                             'río Amazonas, que forma un cañón profundo en '
                             'su curso alto, es el río:',
                 'alternativas': ['Urubamba',
                                  'Mapacho',
                                  'Vilcanota',
                                  'Apurímac',
                                  'Yavero'],
                 'correcta': 'D'},
                {'pregunta': 'El riesgo sísmico en el departamento del Cusco '
                             'se debe principalmente a la presencia de:',
                 'alternativas': ['Volcanes activos',
                                  'Fallas activas de la edad Cuaternaria',
                                  'Erosión marina',
                                  'Actividad glaciar',
                                  'Fallas inactivas'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de fallas del Cusco, que comprende '
                             'más de 100 km entre Abancay y Urcos, incluye '
                             'la falla:',
                 'alternativas': ['Sangarará',
                                  'Zurite exclusiva',
                                  'Pomacanchi',
                                  'Tambomachay',
                                  'Langui-Layo'],
                 'correcta': 'D'},
                {'pregunta': 'El riesgo de deslizamientos en la ciudad del '
                             'Cusco se encuentra principalmente en las '
                             'quebradas y vertientes del valle del:',
                 'alternativas': ['Vilcanota',
                                  'Mapacho',
                                  'Urubamba',
                                  'Watanay',
                                  'Apurímac'],
                 'correcta': 'D'},
                {'pregunta': 'La contaminación atmosférica en Cusco se '
                             'vincula, entre otros factores, a la quema de '
                             'pastizales y a las fábricas de:',
                 'alternativas': ['Cerámica exclusiva',
                                  'Ladrillos y tejas',
                                  'Papel',
                                  'Textiles',
                                  'Muebles'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación acústica en la ciudad del '
                             'Cusco se debe al tráfico vehicular y a la '
                             'llegada y salida de aviones del aeropuerto:',
                 'alternativas': ['Alejandro Velasco Astete',
                                  'Jorge Chávez',
                                  'Rodríguez Ballón',
                                  'Inca Manco Cápac',
                                  'Velazco Astete Internacional'],
                 'correcta': 'A'},
                {'pregunta': 'El río que recibe vertidos de aguas servidas '
                             'de más de 400 000 habitantes de la ciudad del '
                             'Cusco es el río:',
                 'alternativas': ['Apurímac',
                                  'Mapacho',
                                  'Watanay',
                                  'Yavero',
                                  'Vilcanota'],
                 'correcta': 'C'},
                {'pregunta': 'El botadero de basura de la ciudad del Cusco, '
                             'ubicado en Santiago, que forma una montaña de '
                             'desechos, se llama:',
                 'alternativas': ['Ttio',
                                  'Jaquira',
                                  'Sacsayhuamán',
                                  'Molle',
                                  'Huancaro'],
                 'correcta': 'B'},
                {'pregunta': 'El botadero de Jaquira recibe a diario un '
                             'promedio de desechos de aproximadamente:',
                 'alternativas': ['50 toneladas',
                                  '700 toneladas',
                                  '100 toneladas',
                                  '380 toneladas',
                                  '1000 toneladas'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'LOCALIZACIÓN Y EXTENSIÓN / LÍMITES DEL '
                                'DEPARTAMENTO',
                      'items': ['El departamento del Cusco se ubica en la '
                                'parte sur-oriental del Perú, entre la '
                                'Cordillera de los Andes, la Selva Alta y la '
                                'Selva Baja.',
                                'La superficie total del departamento del '
                                'Cusco es de 72 364 km², representando el '
                                '5,6% del territorio nacional.',
                                'El punto más alto del departamento es el '
                                'nevado Ausangate, a 6364 m de altitud.',
                                'El punto más bajo del Cusco se ubica en la '
                                'provincia de La Convención, a 180 m, en el '
                                'límite con Ucayali.',
                                'El Cusco limita por el norte con Ucayali, '
                                'por el noroeste con Junín, y por el noreste '
                                'con Madre de Dios.',
                                'El Cusco limita por el sur con Arequipa, '
                                'por el este y sureste con Puno, por el '
                                'oeste con Ayacucho y por el suroeste con '
                                'Apurímac.']},
                     {'titulo': 'REGIONES NATURALES DEL CUSCO / DIVISIÓN '
                                'POLÍTICA DEL CUSCO',
                      'items': ['La región Andina o Sierra representa el 53% '
                                'del territorio del departamento del Cusco.',
                                'La Selva Alta o Faja Sub Andina representa '
                                'el 28% del territorio cusqueño.',
                                'La Selva Baja o llanura representa el 19% '
                                'del territorio del departamento.',
                                'El departamento del Cusco tiene 13 '
                                'provincias y 112 distritos.',
                                'La provincia con mayor extensión '
                                'territorial del Cusco es La Convención, con '
                                'capital Quillabamba, representando el '
                                '41,52% del área departamental.',
                                'La provincia del Cusco tiene como capital '
                                'la ciudad del Cusco, y su distrito más '
                                'poblado es San Sebastián.']},
                     {'titulo': 'CORDILLERAS DEL DEPARTAMENTO DEL CUSCO / '
                                'VALLES DEL DEPARTAMENTO DEL CUSCO',
                      'items': ['La cordillera Vilcabamba está alineada de '
                                'SE a NW; su mayor elevación es el nevado '
                                'Salkantay (6271 m).',
                                'La cordillera Vilcanota-Urubamba presenta '
                                'la mayor cantidad de glaciares de la '
                                'región; su pico más elevado es el Ausangate '
                                '(6384 m).',
                                'En la cordillera Vilcanota se ubica el abra '
                                'Málaga, por donde pasa la carretera '
                                'Cusco-Quillabamba.',
                                'La cordillera Paucartambo está constituida '
                                'por serranías residuales, entre 3800 y 4500 '
                                'm; ahí se ubica el abra Acjanaco, por la '
                                'carretera Cusco-Pilcopata.',
                                'El valle del Vilcanota-Urubamba se extiende '
                                '480 km, desde el abra La Raya (4100 m) '
                                'hasta el pongo de Mainique (450 m).',
                                'El valle del Vilcanota-Urubamba concentra '
                                'aproximadamente el 79% de la población del '
                                'departamento del Cusco, y el 75% de sus '
                                'suelos de cultivo.',
                                'En el valle del Vilcanota se ubican los '
                                'restos arqueológicos de Pisaq, '
                                'Ollantaytambo y Machupicchu.',
                                'El río Apurímac, considerado el brazo más '
                                'extenso del río Amazonas, forma el Cañón '
                                'del Apurímac en su curso alto y medio.',
                                'El valle del Mapacho, o Yavero, es otra '
                                'depresión longitudinal importante, de menor '
                                'amplitud que el valle del Vilcanota.']},
                     {'titulo': 'RIESGO DE DESASTRES EN EL DEPARTAMENTO DEL '
                                'CUSCO / CONTAMINACIÓN ATMOSFÉRIC',
                      'items': ['El riesgo sísmico en el Cusco se debe '
                                'principalmente a la presencia de fallas '
                                'activas de la edad Cuaternaria.',
                                'El sistema de fallas del Cusco comprende '
                                'más de 100 km, entre Abancay y Urcos, '
                                'pasando cerca de la ciudad; incluye las '
                                'fallas Zurite, Chinchero y Tambomachay.',
                                'El sistema de fallas del Vilcanota abarca '
                                'alrededor de 100 km, conformado por las '
                                'fallas Pomacanchi, Sangarará y Langui-Layo.',
                                'La falla Tambomachay tiene una longitud de '
                                '18 km y se ubica a 7 km al norte de la '
                                'ciudad del Cusco.',
                                'El riesgo de deslizamientos en el Cusco se '
                                'encuentra principalmente en las quebradas y '
                                'vertientes del valle del Watanay.',
                                'La quebrada Saphy es una de las de mayor '
                                'peligro por deslizamientos, poniendo en '
                                'riesgo monumentos como la iglesia de la '
                                'Compañía de Jesús.',
                                'La contaminación atmosférica en Cusco se '
                                'vincula a la quema de pastizales, el parque '
                                'automotor, y las fábricas de ladrillos y '
                                'tejas.',
                                'A nivel del departamento del Cusco se han '
                                'identificado 473 empresas de fábricas de '
                                'ladrillos y tejas, la mayoría en el valle '
                                'del río Watanay.',
                                'La contaminación acústica en Cusco se debe '
                                'al tráfico vehicular y a la llegada y '
                                'salida de aviones del aeropuerto Alejandro '
                                'Velasco Astete.']},
                     {'titulo': 'CONTAMINACIÓN DE LOS RÍOS WATANAY Y '
                                'VILCANOTA / DESECHOS SÓLIDOS EN LA CIUD',
                      'items': ['El río Watanay recibe vertidos de aguas '
                                'servidas de más de 400 000 habitantes de la '
                                'ciudad del Cusco.',
                                'La contaminación del río Vilcanota proviene '
                                'principalmente de vertidos '
                                'urbano-domésticos y residuos sólidos; el '
                                'valle alberga cerca de un millón de '
                                'habitantes.',
                                'Entre los efectos de esta contaminación '
                                'están la disminución de la fauna acuática y '
                                'enfermedades a la piel por contacto '
                                'directo.',
                                'El botadero de Jaquira, en Santiago, forma '
                                'una montaña con más de 1,5 millones de '
                                'toneladas de desechos.',
                                'El botadero de Jaquira recibe a diario un '
                                'promedio de 380 toneladas de desechos.']}],
  'qr_reto': [{'pregunta': 'El departamento del Cusco tiene un número de '
                           'distritos igual a:',
               'respuesta': '112'},
              {'pregunta': 'El sistema de fallas del Cusco, que comprende '
                           'más de 100 km entre Abancay y Urcos, incluye la '
                           'falla:',
               'respuesta': 'Tambomachay'},
              {'pregunta': 'El valle del Vilcanota-Urubamba concentra '
                           'aproximadamente qué porcentaje de la población '
                           'del departamento del Cusco:',
               'respuesta': '79%'}],
  'qr_dato': 'El sistema de fallas del Cusco comprende más de 100 km, entre '
             'Abancay y Urcos, pasando cerca de la ciudad; incluye las '
             'fallas Zurite, Chinchero y Tambomachay.'},
 {'num': 19,
  'titulo': 'Geografía de América',
  'secciones': [{'titulo': '19.1 GENERALIDADES DEL CONTINENTE',
                 'items': ['América es el {segundo} continente por su '
                           'extensión, después de {Asia}, con cerca de 42 '
                           '974 372 km².',
                           'América comprende tres fracciones: América del '
                           '{Sur}, América Central y América del {Norte}, '
                           'unidas por el Istmo de Panamá.',
                           'Los sistemas orográficos más importantes de '
                           'América son Los {Andes} y las Rocosas o '
                           'Rocallosas.',
                           'El pico más elevado de América es el '
                           '{Aconcagua}, con 6960 m, en Argentina.',
                           'América está dividida políticamente en {35} '
                           'países.']},
                {'titulo': '19.2 AMÉRICA DEL SUR: RELIEVE E HIDROGRAFÍA',
                 'items': ['América del Sur se extiende desde Punta '
                           'Gallinas, en {Colombia}, hasta la isla Diego '
                           'Ramírez, en {Cabo de Hornos}, Chile.',
                           'El sistema orográfico más importante de '
                           'Sudamérica es la Cordillera de los {Andes}, la '
                           'segunda más alta del mundo.',
                           'El {Macizo Brasileño} es un territorio '
                           'erosionado del antiguo escudo brasileño, con '
                           'relieve de meseta.',
                           'América del Sur posee aproximadamente el {26}% '
                           'del agua dulce del planeta.',
                           'El río más grande del planeta, que discurre por '
                           'Sudamérica, es el {Amazonas}.']},
                {'titulo': '19.3 PAÍSES DE AMÉRICA DEL SUR',
                 'items': ['La capital de Brasil es {Brasilia}, y su moneda '
                           'es el {Real}.',
                           'La capital de Argentina es {Buenos Aires}, y su '
                           'moneda es el {Peso}.',
                           'La moneda oficial del Perú es el {Nuevo Sol}.',
                           'Bolivia tiene dos capitales: {Sucre}, la capital '
                           'constitucional, y {La Paz}, sede de gobierno.']},
                {'titulo': '19.4 AMÉRICA CENTRAL',
                 'items': ['{América Central} es una estrecha franja de '
                           'terreno que conecta Norteamérica y América del '
                           'Sur, rodeada por el mar {Caribe} al este y el '
                           'océano Pacífico al oeste.',
                           'El relieve centroamericano es mayormente '
                           'montañoso y escarpado, con una cadena '
                           '{volcánica}; en su territorio se construyó el '
                           'Canal de {Panamá}.',
                           'Los ríos de América Central son de corto '
                           'recorrido, desembocando en las vertientes '
                           '{Pacífico} y Atlántico; el río {Usumacinta} '
                           'sirve de límite entre México y Guatemala.',
                           'En el área continental de América Central están '
                           'Guatemala, El Salvador, Honduras, Nicaragua, '
                           'Costa Rica, {Belice} y Panamá.',
                           'En el área insular de América Central están las '
                           '{Antillas Mayores} (Cuba, República Dominicana, '
                           'Haití, Jamaica) y las Antillas Menores.']},
                {'titulo': '19.5 AMÉRICA DEL NORTE',
                 'items': ['{América del Norte} es la región más extensa de '
                           'América; se extiende desde el círculo polar '
                           'Ártico hasta el extremo sur de {México}.',
                           'Al occidente de América del Norte se ubican las '
                           'Montañas {Rocosas} o Rocallosas, desde Alaska '
                           'hasta México.',
                           'Al oriente de América del Norte se ubican los '
                           'montes {Apalaches}.',
                           'La {Gran Llanura Central} de Norteamérica es '
                           'drenada por los ríos Mississippi, Missouri y sus '
                           'tributarios como el {Ohio}.',
                           'La capital de {Canadá} es Ottawa, y su moneda es '
                           'el dólar canadiense; su principal actividad '
                           'económica es la industria y la {tala}.',
                           'La capital de {México} es Ciudad de México, y su '
                           'moneda es el peso; su principal actividad '
                           'económica es la minería de petróleo y {plata}.',
                           'La capital de {Estados Unidos} es Washington, y '
                           'su moneda es el dólar; su principal actividad '
                           'económica es la {industria}.']}],
  'cuadros': [{'titulo': '19.3 PAÍSES DE AMÉRICA DEL SUR: CAPITAL Y MONEDA',
               'encabezados': ['País', 'Capital', 'Moneda'],
               'filas': [['{Argentina}', 'Buenos Aires', '{Peso}'],
                         ['{Brasil}', 'Brasilia', '{Real}'],
                         ['{Chile}', 'Santiago', 'Peso'],
                         ['{Perú}', 'Lima', '{Nuevo Sol}'],
                         ['{Venezuela}', 'Caracas', 'Bolívar']]}],
  'preguntas': [{'pregunta': 'América es el segundo continente por su '
                             'extensión, después de:',
                 'alternativas': ['África',
                                  'Antártida',
                                  'Europa',
                                  'Oceanía',
                                  'Asia'],
                 'correcta': 'E'},
                {'pregunta': 'América comprende tres fracciones unidas por:',
                 'alternativas': ['El Estrecho de Bering',
                                  'El Golfo de México',
                                  'El Istmo de Panamá',
                                  'El Canal de Magallanes',
                                  'El Canal de Suez'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema orográfico más importante de '
                             'América del Sur es:',
                 'alternativas': ['La Sierra Madre',
                                  'Los Apalaches',
                                  'El Macizo Brasileño',
                                  'La Cordillera de los Andes',
                                  'Las Rocosas'],
                 'correcta': 'D'},
                {'pregunta': 'El pico más elevado de América es el '
                             'Aconcagua, ubicado en:',
                 'alternativas': ['Perú',
                                  'Chile',
                                  'Argentina',
                                  'Bolivia',
                                  'Ecuador'],
                 'correcta': 'C'},
                {'pregunta': 'La altitud aproximada del Aconcagua es de:',
                 'alternativas': ['4 500 m',
                                  '6 000 m',
                                  '7 500 m',
                                  '6 960 m',
                                  '5 000 m'],
                 'correcta': 'D'},
                {'pregunta': 'América está dividida políticamente en un '
                             'número de países igual a:',
                 'alternativas': ['20', '45', '25', '50', '35'],
                 'correcta': 'E'},
                {'pregunta': 'América del Sur se extiende, por el sur, '
                             'hasta:',
                 'alternativas': ['El Macizo Brasileño',
                                  'El Istmo de Panamá',
                                  'Punta Gallinas',
                                  'El río Amazonas',
                                  'La isla Diego Ramírez, Cabo de Hornos'],
                 'correcta': 'E'},
                {'pregunta': 'El Macizo Brasileño se caracteriza por '
                             'presentar un relieve de:',
                 'alternativas': ['Cordillera nevada',
                                  'Volcanes activos',
                                  'Fosas profundas',
                                  'Alta montaña',
                                  'Meseta, de escasa elevación'],
                 'correcta': 'E'},
                {'pregunta': 'América del Sur posee del agua dulce del '
                             'planeta aproximadamente:',
                 'alternativas': ['26%', '5%', '10%', '50%', '70%'],
                 'correcta': 'A'},
                {'pregunta': 'El río más grande del planeta se ubica en:',
                 'alternativas': ['África',
                                  'Europa',
                                  'Norteamérica',
                                  'Asia',
                                  'Sudamérica'],
                 'correcta': 'E'},
                {'pregunta': 'La capital de Brasil es:',
                 'alternativas': ['Belo Horizonte',
                                  'Salvador',
                                  'Río de Janeiro',
                                  'São Paulo',
                                  'Brasilia'],
                 'correcta': 'E'},
                {'pregunta': 'La moneda de Brasil es el:',
                 'alternativas': ['Bolívar',
                                  'Real',
                                  'Peso',
                                  'Dólar',
                                  'Guaraní'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de Argentina es:',
                 'alternativas': ['La Plata',
                                  'Córdoba',
                                  'Rosario',
                                  'Buenos Aires',
                                  'Mendoza'],
                 'correcta': 'D'},
                {'pregunta': 'La moneda del Perú es:',
                 'alternativas': ['El Dólar',
                                  'El Bolívar',
                                  'El Real',
                                  'El Peso',
                                  'El Nuevo Sol'],
                 'correcta': 'E'},
                {'pregunta': 'Bolivia tiene como capital constitucional a:',
                 'alternativas': ['La Paz',
                                  'Potosí',
                                  'Santa Cruz',
                                  'Sucre',
                                  'Cochabamba'],
                 'correcta': 'D'},
                {'pregunta': 'La sede de gobierno de Bolivia es:',
                 'alternativas': ['Oruro',
                                  'Santa Cruz',
                                  'Sucre',
                                  'La Paz',
                                  'Cochabamba'],
                 'correcta': 'D'},
                {'pregunta': 'La actividad económica principal de Chile, '
                             'según la tabla, es:',
                 'alternativas': ['Turismo',
                                  'Agricultura',
                                  'Ganadería',
                                  'Pesca exclusiva',
                                  'Minería'],
                 'correcta': 'E'},
                {'pregunta': 'La actividad económica principal de Venezuela '
                             'es:',
                 'alternativas': ['Turismo',
                                  'Ganadería',
                                  'Agricultura',
                                  'Pesca',
                                  'Minería (petróleo)'],
                 'correcta': 'E'},
                {'pregunta': 'La moneda de Colombia es el:',
                 'alternativas': ['Bolívar',
                                  'Guaraní',
                                  'Sol',
                                  'Real',
                                  'Peso'],
                 'correcta': 'E'},
                {'pregunta': 'El río Orinoco y el río Paraná, junto con el '
                             'Amazonas, se caracterizan por ser:',
                 'alternativas': ['Ríos extensos y caudalosos',
                                  'Ríos estacionales secos',
                                  'Ríos cortos y de bajo caudal',
                                  'Ríos artificiales',
                                  'Ríos de agua salada'],
                 'correcta': 'A'},
                {'pregunta': 'El país con menor extensión territorial de '
                             'América del Norte es: (II CEPRU 2022)',
                 'alternativas': ['México',
                                  'El Salvador',
                                  'Canadá',
                                  'Estados Unidos',
                                  'Belice'],
                 'correcta': 'E'},
                {'pregunta': 'Las montañas localizadas al oriente de '
                             'Norteamérica son los: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Alpes',
                                  'Escandinavos',
                                  'Apalaches',
                                  'Urales',
                                  'Montes Atlas'],
                 'correcta': 'C'},
                {'pregunta': 'La estrecha franja de terreno que conecta '
                             'Norteamérica y América del Sur, rodeada por el '
                             'mar Caribe y el océano Pacífico, se llama:',
                 'alternativas': ['América del Norte',
                                  'América Insular',
                                  'Mesoamérica',
                                  'América Central',
                                  'Las Antillas'],
                 'correcta': 'D'},
                {'pregunta': 'En el territorio de América Central se '
                             'construyó una importante obra de ingeniería '
                             'llamada:',
                 'alternativas': ['Estrecho de Magallanes',
                                  'Túnel del Darién',
                                  'Canal de Suez',
                                  'Puente de las Américas',
                                  'Canal de Panamá'],
                 'correcta': 'E'},
                {'pregunta': 'El río que sirve de límite fronterizo entre '
                             'México y Guatemala se llama río:',
                 'alternativas': ['Yukón',
                                  'Mackenzie',
                                  'Usumacinta',
                                  'Colorado',
                                  'Grande'],
                 'correcta': 'C'},
                {'pregunta': 'Las Antillas Mayores, que forman parte del '
                             'área insular de América Central, incluyen a '
                             'Cuba, Jamaica, Haití y:',
                 'alternativas': ['República Dominicana',
                                  'Trinidad y Tobago',
                                  'Granada',
                                  'Bahamas',
                                  'Barbados'],
                 'correcta': 'A'},
                {'pregunta': 'América del Norte se extiende desde el círculo '
                             'polar Ártico hasta el extremo sur de:',
                 'alternativas': ['Estados Unidos',
                                  'Guatemala',
                                  'Panamá',
                                  'Canadá',
                                  'México'],
                 'correcta': 'E'},
                {'pregunta': 'Las montañas ubicadas al occidente de América '
                             'del Norte, desde Alaska hasta México, se '
                             'llaman montañas:',
                 'alternativas': ['Apalaches',
                                  'Urales',
                                  'Andes',
                                  'Alpes',
                                  'Rocosas o Rocallosas'],
                 'correcta': 'E'},
                {'pregunta': 'Las montañas ubicadas al oriente de América '
                             'del Norte se llaman montes:',
                 'alternativas': ['Apalaches',
                                  'Rocosos',
                                  'Andinos',
                                  'Cascada',
                                  'Sierra Madre'],
                 'correcta': 'A'},
                {'pregunta': 'La Gran Llanura Central de Norteamérica es '
                             'drenada principalmente por el río Mississippi '
                             'y el río:',
                 'alternativas': ['Yukón',
                                  'Grande',
                                  'Mackenzie',
                                  'Colorado',
                                  'Missouri'],
                 'correcta': 'E'},
                {'pregunta': 'La capital de Canadá es:',
                 'alternativas': ['Vancouver',
                                  'Quebec',
                                  'Montreal',
                                  'Toronto',
                                  'Ottawa'],
                 'correcta': 'E'},
                {'pregunta': 'La principal actividad económica de México, '
                             'según su producción minera, es:',
                 'alternativas': ['Minería de petróleo y plata',
                                  'Pesca exclusiva',
                                  'Agricultura exclusiva',
                                  'Turismo exclusivo',
                                  'Industria textil'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'GENERALIDADES DEL CONTINENTE',
                      'items': ['América es el segundo continente por su '
                                'extensión, después de Asia, con cerca de 42 '
                                '974 372 km².',
                                'América comprende tres fracciones: América '
                                'del Sur, América Central y América del '
                                'Norte, unidas por el Istmo de Panamá.',
                                'Los sistemas orográficos más importantes de '
                                'América son Los Andes y las Rocosas o '
                                'Rocallosas.',
                                'El pico más elevado de América es el '
                                'Aconcagua, con 6960 m, en Argentina.',
                                'América está dividida políticamente en 35 '
                                'países.']},
                     {'titulo': 'AMÉRICA DEL SUR: RELIEVE E HIDROGRAFÍA',
                      'items': ['América del Sur se extiende desde Punta '
                                'Gallinas, en Colombia, hasta la isla Diego '
                                'Ramírez, en Cabo de Hornos, Chile.',
                                'El sistema orográfico más importante de '
                                'Sudamérica es la Cordillera de los Andes, '
                                'la segunda más alta del mundo.',
                                'El Macizo Brasileño es un territorio '
                                'erosionado del antiguo escudo brasileño, '
                                'con relieve de meseta.',
                                'América del Sur posee aproximadamente el '
                                '26% del agua dulce del planeta.',
                                'El río más grande del planeta, que discurre '
                                'por Sudamérica, es el Amazonas.']},
                     {'titulo': 'PAÍSES DE AMÉRICA DEL SUR',
                      'items': ['La capital de Brasil es Brasilia, y su '
                                'moneda es el Real.',
                                'La capital de Argentina es Buenos Aires, y '
                                'su moneda es el Peso.',
                                'La moneda oficial del Perú es el Nuevo Sol.',
                                'Bolivia tiene dos capitales: Sucre, la '
                                'capital constitucional, y La Paz, sede de '
                                'gobierno.']},
                     {'titulo': 'AMÉRICA CENTRAL',
                      'items': ['América Central es una estrecha franja de '
                                'terreno que conecta Norteamérica y América '
                                'del Sur, rodeada por el mar Caribe al este '
                                'y el océano Pacífico al oeste.',
                                'El relieve centroamericano es mayormente '
                                'montañoso y escarpado, con una cadena '
                                'volcánica; en su territorio se construyó el '
                                'Canal de Panamá.',
                                'Los ríos de América Central son de corto '
                                'recorrido, desembocando en las vertientes '
                                'Pacífico y Atlántico; el río Usumacinta '
                                'sirve de límite entre México y Guatemala.',
                                'En el área continental de América Central '
                                'están Guatemala, El Salvador, Honduras, '
                                'Nicaragua, Costa Rica, Belice y Panamá.',
                                'En el área insular de América Central están '
                                'las Antillas Mayores (Cuba, República '
                                'Dominicana, Haití, Jamaica) y las Antillas '
                                'Menores.']},
                     {'titulo': 'AMÉRICA DEL NORTE',
                      'items': ['América del Norte es la región más extensa '
                                'de América; se extiende desde el círculo '
                                'polar Ártico hasta el extremo sur de '
                                'México.',
                                'Al occidente de América del Norte se ubican '
                                'las Montañas Rocosas o Rocallosas, desde '
                                'Alaska hasta México.',
                                'Al oriente de América del Norte se ubican '
                                'los montes Apalaches.',
                                'La Gran Llanura Central de Norteamérica es '
                                'drenada por los ríos Mississippi, Missouri '
                                'y sus tributarios como el Ohio.',
                                'La capital de Canadá es Ottawa, y su moneda '
                                'es el dólar canadiense; su principal '
                                'actividad económica es la industria y la '
                                'tala.',
                                'La capital de México es Ciudad de México, y '
                                'su moneda es el peso; su principal '
                                'actividad económica es la minería de '
                                'petróleo y plata.',
                                'La capital de Estados Unidos es Washington, '
                                'y su moneda es el dólar; su principal '
                                'actividad económica es la industria.']}],
  'qr_reto': [{'pregunta': 'La estrecha franja de terreno que conecta '
                           'Norteamérica y América del Sur, rodeada por el '
                           'mar Caribe y el océano Pacífico, se llama:',
               'respuesta': 'América Central'},
              {'pregunta': 'La Gran Llanura Central de Norteamérica es '
                           'drenada principalmente por el río Mississippi y '
                           'el río:',
               'respuesta': 'Missouri'},
              {'pregunta': 'El país con menor extensión territorial de '
                           'América del Norte es:',
               'respuesta': 'Belice'}],
  'qr_dato': 'El relieve centroamericano es mayormente montañoso y '
             'escarpado, con una cadena volcánica; en su territorio se '
             'construyó el Canal de Panamá.'},
 {'num': 20,
  'titulo': 'Geografía de Europa, Asia, África, Antártida y Oceanía',
  'secciones': [{'titulo': '20.1 EUROPA',
                 'items': ['{Europa} se ubica en el hemisferio norte y '
                           'morfológicamente es una península del continente '
                           '{asiático}.',
                           'Europa tiene 10 400 000 km² y está dividida '
                           'políticamente en {43} países.',
                           'Europa limita al sur con el {mar Mediterráneo}, '
                           'al este con los Montes Urales y el mar Caspio, y '
                           'al oeste con el océano {Atlántico}.',
                           'El sistema montañoso más importante del sur de '
                           'Europa incluye el Cáucaso, {Alpes}, Balcanes, '
                           'Pirineos y Apeninos.',
                           'El río {Volga}, que desemboca en el mar Caspio, '
                           'es el más largo de Europa; el {Danubio} es el '
                           'más internacional.']},
                {'titulo': '20.2 ASIA',
                 'items': ['{Asia} es el continente más extenso del planeta, '
                           'con 44 614 000 km², dividido políticamente en '
                           '{48} países.',
                           'Asia limita al norte con el océano Glacial '
                           'Ártico, al este con el {Pacífico}, al sur con el '
                           'océano Índico y al oeste con {Europa}.',
                           'El sistema orográfico más importante del mundo '
                           'es el {Himalaya}; su pico más elevado es el '
                           '{Everest}, con 8848 m.',
                           'Asia se conecta con Europa mediante los Montes '
                           '{Urales}, y con África mediante el Canal de '
                           '{Suez}.']},
                {'titulo': '20.3 LA ANTÁRTIDA',
                 'items': ['La {Antártida} es el continente más austral de '
                           'la Tierra, con 14 000 000 km², el cuarto más '
                           'grande después de Asia, América y {África}.',
                           'Alrededor del {98}% de la Antártida está '
                           'cubierta de hielo, con un espesor promedio de '
                           '1,9 km.',
                           'La Antártida es el continente más frío, seco y '
                           '{ventoso}; se rige por el {Tratado Antártico}, '
                           'firmado en 1959.']},
                {'titulo': '20.4 ÁFRICA',
                 'items': ['{África} es el tercer continente más extenso, '
                           'con 30 365 000 km², considerada cuna de la raza '
                           '{humana}.',
                           'África está dividida políticamente en {53} '
                           'países.',
                           'El {Kilimanjaro} es el punto más alto de África; '
                           'el {Sahara} es el desierto más grande de la '
                           'Tierra.',
                           'El río {Nilo}, con 6671 km, es el río más largo '
                           'de África.']},
                {'titulo': '20.5 OCEANÍA',
                 'items': ['{Oceanía} es el continente más pequeño de la '
                           'Tierra y eminentemente {insular}, con cerca de '
                           '30 000 islas.',
                           'Oceanía se agrupa en cuatro áreas geográficas: '
                           'Australasia, {Melanesia}, Micronesia y '
                           'Polinesia.',
                           'Oceanía tiene 8 505 070 km² y está dividida '
                           'políticamente en {14} países.',
                           '{Australia} es el país más extenso de Oceanía, '
                           'con relieve llano y numerosos desiertos.']}],
  'cuadros': [{'titulo': '20.1 LOS CINCO CONTINENTES: ÁREA Y PAÍSES',
               'despues_de': '20.5 OCEANÍA',
               'encabezados': ['Continente', 'Número de países'],
               'filas': [['Europa', '{43} países'],
                         ['Asia', '{48} países'],
                         ['África', '{53} países'],
                         ['Oceanía', '{14} países']]}],
  'preguntas': [{'pregunta': 'Morfológicamente, el continente europeo se '
                             'presenta como una península del continente:',
                 'alternativas': ['Africano',
                                  'Antártico',
                                  'Americano',
                                  'Asiático',
                                  'Oceánico'],
                 'correcta': 'D'},
                {'pregunta': 'Europa está dividida políticamente en un '
                             'número de países igual a:',
                 'alternativas': ['53', '43', '14', '27', '48'],
                 'correcta': 'B'},
                {'pregunta': 'El río más largo de Europa, que desemboca en '
                             'el mar Caspio, es el río:',
                 'alternativas': ['Danubio', 'Rin', 'Ebro', 'Sena', 'Volga'],
                 'correcta': 'E'},
                {'pregunta': 'El continente más extenso del planeta es:',
                 'alternativas': ['América',
                                  'África',
                                  'Asia',
                                  'Oceanía',
                                  'Europa'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema orográfico más importante del '
                             'mundo, ubicado en Asia, cuyo pico más elevado '
                             'es el Everest, se llama:',
                 'alternativas': ['El Himalaya',
                                  'Los Andes',
                                  'Los Alpes',
                                  'El Atlas',
                                  'El Cáucaso'],
                 'correcta': 'A'},
                {'pregunta': 'Asia se conecta con África a través del:',
                 'alternativas': ['Canal de Panamá',
                                  'Canal de Suez',
                                  'Estrecho de Bering',
                                  'Estrecho de Gibraltar',
                                  'Mar Rojo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El porcentaje de la superficie de la Antártida '
                             'cubierta de hielo es aproximadamente:',
                 'alternativas': ['80%', '50%', '70%', '98%', '90%'],
                 'correcta': 'D'},
                {'pregunta': 'El tratado que rige a la Antártida, firmado en '
                             '1959, prohibiendo actividades militares y '
                             'extracción de minerales, se llama:',
                 'alternativas': ['Protocolo de Madrid',
                                  'Convenio de Basilea',
                                  'Tratado de Kioto',
                                  'Tratado Antártico',
                                  'Tratado de Montreal'],
                 'correcta': 'D'},
                {'pregunta': 'África es considerada la cuna de la:',
                 'alternativas': ['Ganadería',
                                  'Raza humana',
                                  'Civilización occidental',
                                  'Escritura',
                                  'Agricultura'],
                 'correcta': 'B'},
                {'pregunta': 'El desierto más grande de la Tierra, ubicado '
                             'en África, es el desierto:',
                 'alternativas': ['Namib',
                                  'Sahara',
                                  'Atacama',
                                  'Kalahari',
                                  'Gobi'],
                 'correcta': 'B'},
                {'pregunta': 'El río más largo de África es el río:',
                 'alternativas': ['Senegal',
                                  'Níger',
                                  'Nilo',
                                  'Congo',
                                  'Zambeze'],
                 'correcta': 'C'},
                {'pregunta': 'Oceanía es el continente más pequeño de la '
                             'Tierra y se caracteriza por ser eminentemente:',
                 'alternativas': ['Montañoso',
                                  'Insular',
                                  'Glaciar',
                                  'Continental',
                                  'Desértico'],
                 'correcta': 'B'},
                {'pregunta': 'Las cuatro áreas geográficas en que se agrupa '
                             'Oceanía son Australasia, Micronesia, Polinesia '
                             'y:',
                 'alternativas': ['Malasia',
                                  'Melanesia',
                                  'Indonesia',
                                  'Antillas',
                                  'Filipinas'],
                 'correcta': 'B'},
                {'pregunta': 'El país más extenso de Oceanía, con relieve '
                             'llano y numerosos desiertos, es:',
                 'alternativas': ['Papúa Nueva Guinea',
                                  'Nueva Zelanda',
                                  'Fiji',
                                  'Samoa',
                                  'Australia'],
                 'correcta': 'E'},
                {'pregunta': 'El continente con la ubicación más austral es: '
                             '(II CEPRU 2025)',
                 'alternativas': ['Asia',
                                  'América',
                                  'África',
                                  'Antártida',
                                  'Oceanía'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'EUROPA',
                      'items': ['Europa se ubica en el hemisferio norte y '
                                'morfológicamente es una península del '
                                'continente asiático.',
                                'Europa tiene 10 400 000 km² y está dividida '
                                'políticamente en 43 países.',
                                'Europa limita al sur con el mar '
                                'Mediterráneo, al este con los Montes Urales '
                                'y el mar Caspio, y al oeste con el océano '
                                'Atlántico.',
                                'El sistema montañoso más importante del sur '
                                'de Europa incluye el Cáucaso, Alpes, '
                                'Balcanes, Pirineos y Apeninos.',
                                'El río Volga, que desemboca en el mar '
                                'Caspio, es el más largo de Europa; el '
                                'Danubio es el más internacional.']},
                     {'titulo': 'ASIA',
                      'items': ['Asia es el continente más extenso del '
                                'planeta, con 44 614 000 km², dividido '
                                'políticamente en 48 países.',
                                'Asia limita al norte con el océano Glacial '
                                'Ártico, al este con el Pacífico, al sur con '
                                'el océano Índico y al oeste con Europa.',
                                'El sistema orográfico más importante del '
                                'mundo es el Himalaya; su pico más elevado '
                                'es el Everest, con 8848 m.',
                                'Asia se conecta con Europa mediante los '
                                'Montes Urales, y con África mediante el '
                                'Canal de Suez.']},
                     {'titulo': 'LA ANTÁRTIDA',
                      'items': ['La Antártida es el continente más austral '
                                'de la Tierra, con 14 000 000 km², el cuarto '
                                'más grande después de Asia, América y '
                                'África.',
                                'Alrededor del 98% de la Antártida está '
                                'cubierta de hielo, con un espesor promedio '
                                'de 1,9 km.',
                                'La Antártida es el continente más frío, '
                                'seco y ventoso; se rige por el Tratado '
                                'Antártico, firmado en 1959.']},
                     {'titulo': 'ÁFRICA',
                      'items': ['África es el tercer continente más extenso, '
                                'con 30 365 000 km², considerada cuna de la '
                                'raza humana.',
                                'África está dividida políticamente en 53 '
                                'países.',
                                'El Kilimanjaro es el punto más alto de '
                                'África; el Sahara es el desierto más grande '
                                'de la Tierra.',
                                'El río Nilo, con 6671 km, es el río más '
                                'largo de África.']},
                     {'titulo': 'OCEANÍA',
                      'items': ['Oceanía es el continente más pequeño de la '
                                'Tierra y eminentemente insular, con cerca '
                                'de 30 000 islas.',
                                'Oceanía se agrupa en cuatro áreas '
                                'geográficas: Australasia, Melanesia, '
                                'Micronesia y Polinesia.',
                                'Oceanía tiene 8 505 070 km² y está dividida '
                                'políticamente en 14 países.',
                                'Australia es el país más extenso de '
                                'Oceanía, con relieve llano y numerosos '
                                'desiertos.']}],
  'qr_reto': [{'pregunta': 'El desierto más grande de la Tierra, ubicado en '
                           'África, es el desierto:',
               'respuesta': 'Sahara'},
              {'pregunta': 'Las cuatro áreas geográficas en que se agrupa '
                           'Oceanía son Australasia, Micronesia, Polinesia '
                           'y:',
               'respuesta': 'Melanesia'},
              {'pregunta': 'Oceanía es el continente más pequeño de la '
                           'Tierra y se caracteriza por ser eminentemente:',
               'respuesta': 'Insular'}],
  'qr_dato': 'Europa tiene 10 400 000 km² y está dividida políticamente en '
             '43 países.'}]
