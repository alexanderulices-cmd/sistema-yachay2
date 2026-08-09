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
                 'alternativas': ['Mundo y espacio',
                                  'Tierra y ciencia',
                                  'Espacio y estudio',
                                  'Suelo y medición',
                                  'Tierra y descripción'],
                 'correcta': 'E'},
                {'pregunta': 'Los geógrafos que iniciaron, en la Época '
                             'Moderna, una nueva era de la Geografía fueron:',
                 'alternativas': ['Von Humboldt y Carlos Ritter',
                                  'Ratzel y Brunhes',
                                  'Eratóstenes y Ptolomeo',
                                  'Milton Santos y Bunge',
                                  'Vidal de la Blache y Schaefer'],
                 'correcta': 'A'},
                {'pregunta': 'El geógrafo que calculó la circunferencia '
                             'terrestre con notable aproximación y elaboró '
                             'un mapamundi fue:',
                 'alternativas': ['Claudio Ptolomeo',
                                  'Eratóstenes',
                                  'Jean Brunhes',
                                  'Carlos Ritter',
                                  'Federico Ratzel'],
                 'correcta': 'B'},
                {'pregunta': 'El primero en elaborar un Atlas Universal fue:',
                 'alternativas': ['Vidal de la Blache',
                                  'Von Humboldt',
                                  'Milton Santos',
                                  'Eratóstenes',
                                  'Claudio Ptolomeo'],
                 'correcta': 'E'},
                {'pregunta': 'La etapa del pensamiento geográfico que va '
                             'desde los tiempos primitivos hasta mediados '
                             'del siglo XIX, de carácter empírico y '
                             'rutinario, es la Geografía:',
                 'alternativas': ['Cuantitativa',
                                  'Científica',
                                  'Antigua',
                                  'Teorética',
                                  'Nueva'],
                 'correcta': 'C'},
                {'pregunta': 'La Geografía Moderna o Científica se '
                             'fundamenta en la filosofía del:',
                 'alternativas': ['Estructuralismo',
                                  'Positivismo',
                                  'Neopositivismo',
                                  'Empirismo',
                                  'Racionalismo'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que se fundamenta en el '
                             'Neopositivismo o Positivismo Lógico y utiliza '
                             'el método deductivo es la Geografía:',
                 'alternativas': ['Descriptiva',
                                  'Nueva, Cuantitativa o Teorética',
                                  'Antigua',
                                  'Moderna',
                                  'Regional clásica'],
                 'correcta': 'B'},
                {'pregunta': 'Según Milton Santos da Almeida, el espacio '
                             'geográfico es:',
                 'alternativas': ['El marco físico de toda acción humana',
                                  'La naturaleza modificada por el hombre a '
                                  'través del trabajo',
                                  'La epidermis del planeta Tierra',
                                  'El territorio de un Estado',
                                  'La suma de climas y relieves'],
                 'correcta': 'B'},
                {'pregunta': 'La flora, la fauna y la diversidad de relieves '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Económicos',
                                  'Políticos',
                                  'Naturales',
                                  'Culturales',
                                  'Sociales'],
                 'correcta': 'C'},
                {'pregunta': 'Las viviendas, ciudades y vías de comunicación '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Culturales',
                                  'Naturales',
                                  'Abióticos',
                                  'Climáticos',
                                  'Bióticos'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la Geografía Física que estudia el '
                             'origen, evolución y formas del relieve es la:',
                 'alternativas': ['Climatología',
                                  'Hidrogeografía',
                                  'Geomorfología',
                                  'Edafología',
                                  'Biogeografía'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de la Hidrogeografía, el estudio de los '
                             'ríos corresponde a la:',
                 'alternativas': ['Oceanografía',
                                  'Edafología',
                                  'Fluviología',
                                  'Fitogeografía',
                                  'Limnología'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de la Biogeografía, el estudio de la '
                             'distribución de los animales corresponde a la:',
                 'alternativas': ['Zoogeografía',
                                  'Fitogeografía',
                                  'Demogeografía',
                                  'Limnología',
                                  'Oceanografía'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la Geografía Humana que estudia la '
                             'distribución de la población en la superficie '
                             'terrestre es la:',
                 'alternativas': ['Geografía Urbana',
                                  'Demogeografía',
                                  'Geografía Histórica',
                                  'Geografía Política',
                                  'Geografía Rural'],
                 'correcta': 'B'},
                {'pregunta': 'El principio metodológico según el cual todo '
                             'elemento del espacio geográfico debe ser '
                             'ubicado en mapas y cartas geográficas, '
                             'formulado por Federico Ratzel, es el de:',
                 'alternativas': ['Comparación',
                                  'Localización, Distribución o Extensión',
                                  'Actividad o Dinamismo',
                                  'Relación o Conexión',
                                  'Causalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de Causalidad o Explicación, que '
                             'establece que todo elemento debe analizarse '
                             'por sus causas y consecuencias, fue formulado '
                             'por:',
                 'alternativas': ['Vidal de la Blache',
                                  'Carlos Ritter',
                                  'Federico Ratzel',
                                  'Jean Brunhes',
                                  'Alejandro Von Humboldt'],
                 'correcta': 'E'},
                {'pregunta': 'El principio que establece que los elementos '
                             'del espacio geográfico están en íntima '
                             'interdependencia, formulado por Jean Brunhes, '
                             'es el de:',
                 'alternativas': ['Causalidad',
                                  'Relación o Conexión',
                                  'Localización',
                                  'Actividad',
                                  'Comparación'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de Comparación, también llamado '
                             'de Coordinación, Universalización o Analogía, '
                             'fue formulado por:',
                 'alternativas': ['Federico Ratzel y Jean Brunhes',
                                  'Carlos Ritter y Vidal de la Blache',
                                  'Schaefer y Bunge',
                                  'Von Humboldt y Ptolomeo',
                                  'Eratóstenes y Milton Santos'],
                 'correcta': 'B'},
                {'pregunta': 'Que los elementos del espacio geográfico deban '
                             'estudiarse en su constante y perpetua '
                             'transformación corresponde al principio de:',
                 'alternativas': ['Localización',
                                  'Relación',
                                  'Causalidad',
                                  'Comparación',
                                  'Actividad, Dinamismo o Evolución'],
                 'correcta': 'E'},
                {'pregunta': 'Herramientas propias de la Geografía Aplicada '
                             'para la gestión del territorio son:',
                 'alternativas': ['La cartografía digital, los SIG y la '
                                  'teledetección',
                                  'Los censos poblacionales',
                                  'Únicamente encuestas de campo',
                                  'Solo mapas físicos en papel',
                                  'Los tratados internacionales'],
                 'correcta': 'A'},
                {'pregunta': 'Junto con Alexander von Humboldt, el geógrafo '
                             'considerado fundador de la Geografía Moderna '
                             'es:',
                 'alternativas': ['Milton Santos',
                                  'Karl Ritter',
                                  'Fred Schaefer',
                                  'William Bunge',
                                  'Eratóstenes'],
                 'correcta': 'B'},
                {'pregunta': 'En la Geografía Antigua, el geógrafo que '
                             'calculó la circunferencia terrestre con '
                             'notable aproximación fue:',
                 'alternativas': ['Claudio Ptolomeo',
                                  'Eratóstenes',
                                  'Alexander von Humboldt',
                                  'Karl Ritter',
                                  'Estrabón'],
                 'correcta': 'B'},
                {'pregunta': 'La ciencia que se encarga de estudiar la '
                             'distribución de plantas y animales en el '
                             'espacio geográfico es la: (I CEPRU 2024)',
                 'alternativas': ['Edafología',
                                  'Biogeografía',
                                  'Hidrogeografía',
                                  'Demogeografía',
                                  'Biología'],
                 'correcta': 'B'},
                {'pregunta': 'El origen, estructura y clases de suelos es '
                             'estudiado por la: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['Geomorfología',
                                  'Edafología',
                                  'Geología',
                                  'Limnología',
                                  'Fisiografía'],
                 'correcta': 'B'},
                {'pregunta': 'El objeto de estudio de la Ciencia geográfica '
                             'es el: (Primera Oportunidad UNSAAC 2023)',
                 'alternativas': ['Geosistema del universo',
                                  'Fenómeno global de la Tierra',
                                  'Espacio geográfico',
                                  'Espacio terrestre',
                                  'Ecosistema del hombre'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de Dinamismo se le atribuye a: '
                             '(Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Federico Ratzel',
                                  'A. Von Humboldt',
                                  'Jean Brunhes',
                                  'P. Vidal de la Blache',
                                  'Karl Ritter'],
                 'correcta': 'C'}],
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
  'qr_reto': [{'pregunta': '¿Qué significa etimológicamente Geografía?',
               'respuesta': 'Descripción de la Tierra (Geo=Tierra, '
                            'Graphía=Descripción)'},
              {'pregunta': '¿Quién calculó la circunferencia terrestre en la '
                           'Antigüedad?',
               'respuesta': 'Eratóstenes'},
              {'pregunta': '¿Qué principio metodológico propuso Federico '
                           'Ratzel?',
               'respuesta': 'Principio de Localización, Distribución o '
                            'Extensión'}],
  'qr_dato': 'El territorio peruano tiene 1 285 216 km² y se ubica '
             'íntegramente en el hemisferio sur y occidental. ¡Es el 19º '
             'país más extenso del mundo! 🌎'},
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
                 'alternativas': ['Estelares',
                                  'Galácticas',
                                  'Cósmicas',
                                  'Antrópicas',
                                  'Solares'],
                 'correcta': 'D'},
                {'pregunta': 'La litósfera, la atmósfera y la hidrósfera son '
                             'entidades:',
                 'alternativas': ['Estelares',
                                  'Abióticas',
                                  'Cósmicas',
                                  'Antrópicas',
                                  'Bióticas'],
                 'correcta': 'B'},
                {'pregunta': 'La biósfera es una entidad del geosistema de '
                             'tipo:',
                 'alternativas': ['Abiótica',
                                  'Cósmica',
                                  'Antrópica',
                                  'Solar',
                                  'Biótica'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría del Big-Bang fue planteada '
                             'originalmente por:',
                 'alternativas': ['Edwin Hubble',
                                  'George Gamow',
                                  'Albert Einstein',
                                  'George Lemaître',
                                  'Isaac Newton'],
                 'correcta': 'D'},
                {'pregunta': 'Según el Big-Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['500 millones de años',
                                  '15 000 millones de años',
                                  '5 000 millones de años',
                                  '1 000 millones de años',
                                  '100 000 millones de años'],
                 'correcta': 'B'},
                {'pregunta': 'Las aglomeraciones de millones de estrellas se '
                             'denominan:',
                 'alternativas': ['Galaxias',
                                  'Cúmulos',
                                  'Cometas',
                                  'Nebulosas',
                                  'Meteoritos'],
                 'correcta': 'A'},
                {'pregunta': 'El diámetro medio de la Vía Láctea es de '
                             'aproximadamente:',
                 'alternativas': ['1 000 000 años luz',
                                  '100 000 años luz',
                                  '1 000 años luz',
                                  '10 000 años luz',
                                  '500 000 años luz'],
                 'correcta': 'B'},
                {'pregunta': 'Las estrellas producen su propia luz mediante:',
                 'alternativas': ['Radiación cósmica',
                                  'Combustión química',
                                  'Fisión atómica',
                                  'Fusión nuclear',
                                  'Reflexión solar'],
                 'correcta': 'D'},
                {'pregunta': 'Las regiones interestelares donde nacen las '
                             'estrellas se llaman:',
                 'alternativas': ['Nebulosas',
                                  'Cometas',
                                  'Asteroides',
                                  'Cúmulos',
                                  'Galaxias'],
                 'correcta': 'A'},
                {'pregunta': 'El año luz es una unidad de:',
                 'alternativas': ['Temperatura',
                                  'Tiempo',
                                  'Distancia',
                                  'Masa',
                                  'Velocidad'],
                 'correcta': 'C'},
                {'pregunta': 'La luz del Sol tarda en llegar a la Tierra '
                             'aproximadamente:',
                 'alternativas': ['1 minuto',
                                  '1 hora',
                                  '8,3 minutos',
                                  '8,3 segundos',
                                  '8,3 horas'],
                 'correcta': 'C'},
                {'pregunta': 'El Sol contiene de la masa total del Sistema '
                             'Solar aproximadamente:',
                 'alternativas': ['50%', '10%', '25%', '98,85%', '75%'],
                 'correcta': 'D'},
                {'pregunta': 'La Unión Astronómica Internacional definió las '
                             'tres categorías de cuerpos del Sistema Solar '
                             'en el año:',
                 'alternativas': ['2006', '2020', '1980', '2015', '1990'],
                 'correcta': 'A'},
                {'pregunta': 'Los planetas interiores o terrestres son:',
                 'alternativas': ['Júpiter, Saturno, Urano y Neptuno',
                                  'Ceres y Plutón',
                                  'Solo Mercurio y Venus',
                                  'Mercurio, Venus, Tierra y Marte',
                                  'Solo la Tierra y Marte'],
                 'correcta': 'D'},
                {'pregunta': 'Los planetas exteriores o jovianos se '
                             'caracterizan por ser:',
                 'alternativas': ['Cercanos al Sol',
                                  'Sin satélites',
                                  'Sólidos y pequeños',
                                  'Gaseosos y de mayor tamaño',
                                  'De alta densidad'],
                 'correcta': 'D'},
                {'pregunta': 'El planeta con mayor número de satélites entre '
                             'los mostrados es:',
                 'alternativas': ['Urano',
                                  'Marte',
                                  'Júpiter',
                                  'Saturno',
                                  'Neptuno'],
                 'correcta': 'C'},
                {'pregunta': 'El planeta de mayor diámetro del Sistema Solar '
                             'es:',
                 'alternativas': ['Urano',
                                  'Tierra',
                                  'Saturno',
                                  'Júpiter',
                                  'Neptuno'],
                 'correcta': 'D'},
                {'pregunta': 'Plutón es clasificado actualmente como:',
                 'alternativas': ['Cometa',
                                  'Planeta enano',
                                  'Satélite',
                                  'Planeta interior',
                                  'Planeta exterior'],
                 'correcta': 'B'},
                {'pregunta': 'El geosistema se caracteriza por estar en:',
                 'alternativas': ['Estado sólido fijo',
                                  'Colapso permanente',
                                  'Equilibrio dinámico relativo',
                                  'Expansión sin cambios',
                                  'Equilibrio estático total'],
                 'correcta': 'C'},
                {'pregunta': 'La entidad antrópica del geosistema '
                             'corresponde a:',
                 'alternativas': ['Los seres vivos no humanos',
                                  'La sociedad humana',
                                  'Las rocas',
                                  'Los océanos',
                                  'El aire'],
                 'correcta': 'B'},
                {'pregunta': 'Las zonas de radiación que rodean la Tierra, '
                             'formadas por partículas cargadas atrapadas por '
                             'el campo magnético, se llaman:',
                 'alternativas': ['Ionosfera',
                                  'Cinturones de Van Allen',
                                  'Magnetosfera exclusiva',
                                  'Exosfera',
                                  'Termosfera'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia del movimiento de rotación '
                             'terrestre es: (II CEPRU 2024)',
                 'alternativas': ['Desviación de los vientos y las '
                                  'corrientes marinas',
                                  'Puntos cardinales y las zonas térmicas',
                                  'Día artificial y achatamiento polar',
                                  'Zonas climáticas y día artificial',
                                  'Presencia de mareas y las estaciones del '
                                  'año'],
                 'correcta': 'C'},
                {'pregunta': 'Marque una consecuencia del movimiento de '
                             'rotación de la Tierra: (II CEPRU 2022)',
                 'alternativas': ['Día artificial',
                                  'Estaciones del año',
                                  'Achatamiento polar',
                                  'Zonas climáticas',
                                  'Desigual distribución de los rayos del '
                                  'sol'],
                 'correcta': 'A'},
                {'pregunta': 'La ciudad «X» está ubicada a 75° de longitud. '
                             '¿Cuántas horas de diferencia existe con el '
                             'meridiano de Greenwich? (II CEPRU 2022)',
                 'alternativas': ['10 horas',
                                  '5 horas',
                                  '4 horas',
                                  '6 horas',
                                  '7 horas'],
                 'correcta': 'B'},
                {'pregunta': 'Las entidades del Geosistema a escala Global '
                             'son: (Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Antrópicas, fitogeográficas y bióticas',
                                  'Abióticas, bióticas y antrópicas',
                                  'Hidrosfera, sociósfera y zoogeografía',
                                  'Bióticas, litosfera y heliomasa',
                                  'Abióticas, naturales y culturales'],
                 'correcta': 'B'},
                {'pregunta': 'La Longitud es: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Distancia angular de un punto de la '
                                  'superficie terrestre a la línea '
                                  'ecuatorial',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre hacia el círculo '
                                  'polar ártico',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre al meridiano base de '
                                  'Greenwich',
                                  'Distancia angular de un punto de la '
                                  'superficie terrestre al meridiano de '
                                  'referencia del Perú',
                                  'Sistema de referencia basado en paralelos '
                                  'y meridianos'],
                 'correcta': 'C'},
                {'pregunta': 'El cuarto y séptimo planeta en la órbita solar '
                             'corresponden a: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['Venus y Neptuno',
                                  'Tierra y Saturno',
                                  'Marte y Urano',
                                  'Ceres y Eris',
                                  'Júpiter y Neptuno'],
                 'correcta': 'C'},
                {'pregunta': 'Si en la ciudad «X» (28°30\'40" N, 75°29\'10" '
                             'W) son las 14:29 horas del 11 de diciembre, la '
                             'hora y fecha en la ciudad «Y» (71°40\'50" S, '
                             '135°10\'50" E) es: (Primera Oportunidad UNSAAC '
                             '2021)',
                 'alternativas': ['04:29 horas del 12 de diciembre',
                                  '16:29 horas del 12 de diciembre',
                                  '03:29 horas del 11 de diciembre',
                                  '05:29 horas del 11 de diciembre',
                                  '05:29 horas del 12 de diciembre'],
                 'correcta': 'A'},
                {'pregunta': 'El paralelo del trópico de Cáncer, ubicado en '
                             'el hemisferio norte, se encuentra situado a '
                             'una latitud de: (Primera Oportunidad UNSAAC '
                             '2023)',
                 'alternativas': ["25° 30'",
                                  "28° 25'",
                                  "63° 27'",
                                  "66° 33'",
                                  "23° 27'"],
                 'correcta': 'E'},
                {'pregunta': 'Una característica que corresponde a un '
                             'planeta interior o terrestre del Sistema '
                             'Planetario Solar es: (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ['Son más fríos y lejanos al Sol',
                                  'Poseen menor masa y volumen',
                                  'Se les denomina planetas jovianos',
                                  'Tienen mayor cantidad de satélites',
                                  'Son más gaseosos'],
                 'correcta': 'B'},
                {'pregunta': "Cuando en el Cusco son las 9 h 37', ¿qué hora "
                             'será en Roma (10° E)? (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ["13 h 25'",
                                  "14 h 27'",
                                  "15 h 37'",
                                  "03 h 27'",
                                  "03 h 39'"],
                 'correcta': 'C'},
                {'pregunta': 'La ciencia que estudia y determina la forma y '
                             'dimensiones de la Tierra y su campo de '
                             'gravedad se llama:',
                 'alternativas': ['Cartografía',
                                  'Geodesia',
                                  'Topografía',
                                  'Geomorfología',
                                  'Astronomía'],
                 'correcta': 'B'},
                {'pregunta': 'La edad de la Tierra, calculada mediante '
                             'isótopos radiactivos, se estima en:',
                 'alternativas': ['4600 millones de años',
                                  '2300 millones de años',
                                  '6000 millones de años',
                                  '1000 millones de años',
                                  '10000 millones de años'],
                 'correcta': 'A'},
                {'pregunta': 'La forma real de la Tierra, considerando sus '
                             'partes salientes y entrantes tal como es, se '
                             'llama forma:',
                 'alternativas': ['Geoide',
                                  'Física o topográfica',
                                  'Elipsoide de revolución',
                                  'Esférica',
                                  'Achatada'],
                 'correcta': 'B'},
                {'pregunta': 'La forma de la Tierra que resulta de nivelar '
                             'la superficie continental con el nivel medio '
                             'del mar se llama forma:',
                 'alternativas': ['Física',
                                  'Elipsoide de revolución',
                                  'Geoide',
                                  'Topográfica',
                                  'Esférica'],
                 'correcta': 'C'},
                {'pregunta': 'La forma matemática o geométrica de la Tierra, '
                             'achatada en los polos y ensanchada en el '
                             'ecuador, se llama:',
                 'alternativas': ['Geoide',
                                  'Elipsoide de revolución',
                                  'Forma física',
                                  'Forma topográfica',
                                  'Esfera perfecta'],
                 'correcta': 'B'},
                {'pregunta': 'La superficie total de la Tierra es '
                             'aproximadamente de:',
                 'alternativas': ['361 000 000 km²',
                                  '510 000 000 km²',
                                  '149 000 000 km²',
                                  '200 000 000 km²',
                                  '700 000 000 km²'],
                 'correcta': 'B'},
                {'pregunta': 'La densidad media de la Tierra es de:',
                 'alternativas': ['1 gr/cm³',
                                  '5,518 gr/cm³',
                                  '10 gr/cm³',
                                  '3,2 gr/cm³',
                                  '8,9 gr/cm³'],
                 'correcta': 'B'}],
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
                                'presencia de las mareas.']}]},
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
                                  'Expresar gráficamente mediante mapas',
                                  'Clasificar rocas'],
                 'correcta': 'D'},
                {'pregunta': 'El padre de la cartografía moderna fue:',
                 'alternativas': ['Claudio Ptolomeo',
                                  'Eratóstenes',
                                  'Alexander von Humboldt',
                                  'Abraham Ortelius',
                                  'Gerardus Mercator'],
                 'correcta': 'D'},
                {'pregunta': 'Las proyecciones cartográficas sirven para '
                             'transferir información desde la superficie '
                             'esférica hacia:',
                 'alternativas': ['Un plano o mapa',
                                  'Un globo terráqueo',
                                  'Un cilindro únicamente',
                                  'Un modelo digital',
                                  'Una fotografía satelital'],
                 'correcta': 'A'},
                {'pregunta': 'La proyección cilíndrica más utilizada en '
                             'cartografía es la de:',
                 'alternativas': ['Ptolomeo',
                                  'Gauss',
                                  'Humboldt',
                                  'Mercator',
                                  'Ortelius'],
                 'correcta': 'D'},
                {'pregunta': 'El principal inconveniente de la proyección '
                             'cilíndrica es que deforma:',
                 'alternativas': ['El centro del mapa',
                                  'Las áreas próximas a los polos',
                                  'Las líneas rectas',
                                  'El Ecuador',
                                  'Los continentes pequeños'],
                 'correcta': 'B'},
                {'pregunta': 'La proyección adecuada para representar un '
                             'solo país o región es la:',
                 'alternativas': ['Universal',
                                  'Mercator',
                                  'Cónica',
                                  'Cilíndrica',
                                  'Cenital pura'],
                 'correcta': 'C'},
                {'pregunta': 'La proyección que da lugar a un mapa circular '
                             'es la:',
                 'alternativas': ['Cilíndrica',
                                  'Cónica',
                                  'Poliédrica',
                                  'De Mercator',
                                  'Cenital o azimutal'],
                 'correcta': 'E'},
                {'pregunta': 'Los círculos máximos dividen a la Tierra en:',
                 'alternativas': ['Dos partes iguales',
                                  'Cuatro partes desiguales',
                                  'Tres partes iguales',
                                  'Ninguna división real',
                                  'Ocho sectores'],
                 'correcta': 'A'},
                {'pregunta': 'Los meridianos son semicírculos que van de:',
                 'alternativas': ['Ecuador a ecuador',
                                  'Centro a superficie',
                                  'Este a oeste',
                                  'Polo a polo',
                                  'Trópico a trópico'],
                 'correcta': 'D'},
                {'pregunta': 'El meridiano base internacional pasa por el '
                             'observatorio de:',
                 'alternativas': ['Madrid',
                                  'Greenwich',
                                  'Washington',
                                  'Roma',
                                  'París'],
                 'correcta': 'B'},
                {'pregunta': 'El meridiano de Greenwich y su opuesto dividen '
                             'la Tierra en los hemisferios:',
                 'alternativas': ['Superior e inferior',
                                  'Interno y externo',
                                  'Norte y Sur',
                                  'Tropical y polar',
                                  'Occidental y Oriental'],
                 'correcta': 'E'},
                {'pregunta': 'Los paralelos son líneas imaginarias con '
                             'orientación:',
                 'alternativas': ['Norte-Sur',
                                  'Radial',
                                  'Este-Oeste',
                                  'Vertical',
                                  'Diagonal'],
                 'correcta': 'C'},
                {'pregunta': 'La línea del Ecuador corresponde al paralelo:',
                 'alternativas': ['90°', '0°', '180°', "23°27'", '45°'],
                 'correcta': 'B'},
                {'pregunta': 'El Ecuador divide a la Tierra en los '
                             'hemisferios:',
                 'alternativas': ['Tropical y templado',
                                  'Anterior y posterior',
                                  'Occidental y Oriental',
                                  'Norte y Sur',
                                  'Este y polar'],
                 'correcta': 'D'},
                {'pregunta': 'El Trópico de Cáncer se ubica en el hemisferio '
                             'norte, a una latitud de:',
                 'alternativas': ['0°', "66°33'", '45°', '90°', "23°27'"],
                 'correcta': 'E'},
                {'pregunta': 'El Trópico de Capricornio se ubica en el '
                             'hemisferio:',
                 'alternativas': ['Occidental',
                                  'Sur',
                                  'Oriental',
                                  'Ecuatorial',
                                  'Norte'],
                 'correcta': 'B'},
                {'pregunta': 'Los Círculos Polares se ubican a una latitud '
                             'de:',
                 'alternativas': ["23°27'",
                                  "0°00'",
                                  "90°00'",
                                  "45°00'",
                                  "66°33'"],
                 'correcta': 'E'},
                {'pregunta': 'Los meridianos alcanzan su mayor separación '
                             'al:',
                 'alternativas': ['Unirse en el centro',
                                  'Separarse en los círculos polares',
                                  'Atravesar el Ecuador',
                                  'Cruzar los trópicos',
                                  'Cruzar los polos'],
                 'correcta': 'C'},
                {'pregunta': 'Los meridianos convergen (se unen) en:',
                 'alternativas': ['El Ecuador',
                                  'Los trópicos',
                                  'Los polos',
                                  'Los círculos polares',
                                  'El centro de la Tierra'],
                 'correcta': 'C'},
                {'pregunta': 'Las formas que se usan para transferir la '
                             'esfera terrestre a un mapa se llaman '
                             'superficies:',
                 'alternativas': ['Planas únicamente',
                                  'Triangulares',
                                  'Esféricas puras',
                                  'Desarrollables, como conos y cilindros',
                                  'Curvas irregulares'],
                 'correcta': 'D'},
                {'pregunta': 'En la hoja de la Carta Geográfica Nacional, la '
                             'planimetría y altimetría forman parte de: (II '
                             'CEPRU 2025)',
                 'alternativas': ['El sistema de coordenadas',
                                  'La escala de la hoja',
                                  'El cuerpo de la hoja',
                                  'La información marginal',
                                  'Los signos convencionales'],
                 'correcta': 'C'},
                {'pregunta': 'Según las Coordenadas Universal Transversal de '
                             'Mercator (UTM), la Tierra está dividida en: '
                             '(II CEPRU 2024)',
                 'alternativas': ['60 zonas y 20 bandas',
                                  '24 zonas y 20 bandas',
                                  '60 bandas y 20 zonas',
                                  '60 zonas y 19 bandas',
                                  '60 husos y 20 bandas'],
                 'correcta': 'A'},
                {'pregunta': 'La carta geográfica nacional del territorio '
                             'peruano se encuentra dividida en: (II CEPRU '
                             '2024)',
                 'alternativas': ['305 hojas',
                                  '501 hojas',
                                  '505 hojas',
                                  '201 hojas',
                                  '101 hojas'],
                 'correcta': 'C'},
                {'pregunta': 'La escala de la carta nacional del Perú es: (I '
                             'CEPRU 2023)',
                 'alternativas': ['1:50 000',
                                  '1:1 000 000',
                                  '1:100 000',
                                  '1:10 000 000',
                                  '1:200 000'],
                 'correcta': 'C'},
                {'pregunta': 'La Carta Geográfica Nacional es un gran mapa '
                             'de nuestro país dividido en 501 mapas: (I '
                             'CEPRU 2024)',
                 'alternativas': ['Hidrográficos',
                                  'Geográficos',
                                  'Geológicos',
                                  'Topográficos',
                                  'Económicos'],
                 'correcta': 'D'},
                {'pregunta': 'Respecto al sistema de coordenadas UTM, el '
                             'territorio peruano se encuentra entre las '
                             'zonas: (Primera Oportunidad UNSAAC 2024)',
                 'alternativas': ['54, 56 y 57',
                                  '14, 15 y 17',
                                  '17, 18 y 19',
                                  '20, 21 y 22',
                                  '45, 46 y 47'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema de coordenadas UTM se basa en la '
                             'proyección cartográfica transversa de:',
                 'alternativas': ['Robinson',
                                  'Mercator',
                                  'Peters',
                                  'Azimutal',
                                  'Cónica'],
                 'correcta': 'B'},
                {'pregunta': 'A diferencia de las coordenadas geográficas '
                             '(longitud/latitud), las magnitudes del sistema '
                             'UTM se expresan en:',
                 'alternativas': ['Grados sexagesimales',
                                  'Metros',
                                  'Millas náuticas',
                                  'Radianes',
                                  'Kilómetros cuadrados'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema UTM fue desarrollado por el Cuerpo '
                             'de Ingenieros del Ejército de Estados Unidos '
                             'en la década de:',
                 'alternativas': ['1920', '1940', '1960', '1980', '1900'],
                 'correcta': 'B'},
                {'pregunta': 'La Tierra está dividida, según el sistema UTM, '
                             'en un número de zonas o husos igual a:',
                 'alternativas': ['24', '60', '20', '180', '360'],
                 'correcta': 'B'},
                {'pregunta': 'La Tierra está dividida, según el sistema UTM, '
                             'en un número de bandas igual a:',
                 'alternativas': ['60', '20', '24', '12', '30'],
                 'correcta': 'B'},
                {'pregunta': 'Por encima de los 80° de latitud sur y 84° de '
                             'latitud norte, en vez de la Red UTM, se '
                             'utiliza la Red Universal:',
                 'alternativas': ['Geográfica Polar',
                                  'Estereográfica Polar (UPS)',
                                  'Cónica Polar',
                                  'Cilíndrica Polar',
                                  'Azimutal Ecuatorial'],
                 'correcta': 'B'}],
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
                                'el año 1884.']}]},
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
                 'alternativas': ['Esférica',
                                  'Cónica',
                                  'Irregular',
                                  'Cilíndrica',
                                  'Plana'],
                 'correcta': 'E'},
                {'pregunta': 'Los mapas se clasifican, según su función, en '
                             'generales y:',
                 'alternativas': ['Temáticos',
                                  'Digitales',
                                  'Físicos',
                                  'Políticos',
                                  'Satelitales'],
                 'correcta': 'A'},
                {'pregunta': 'Los mapas que representan el territorio por '
                             'medio de símbolos de un aspecto concreto son '
                             'los:',
                 'alternativas': ['Temáticos',
                                  'Catastrales',
                                  'Náuticos',
                                  'Generales',
                                  'Topográficos'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa con escala 1:50 000 corresponde a una '
                             'escala:',
                 'alternativas': ['Intermedia',
                                  'Grande',
                                  'Muy grande',
                                  'Muy pequeña',
                                  'Pequeña'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas de continentes y del mundo '
                             'corresponden a una escala:',
                 'alternativas': ['Grande',
                                  'Muy pequeña',
                                  'Pequeña',
                                  'Intermedia',
                                  'Muy grande'],
                 'correcta': 'B'},
                {'pregunta': 'Un plano de una vivienda corresponde a una '
                             'escala:',
                 'alternativas': ['Muy pequeña',
                                  'Pequeña',
                                  'Muy grande',
                                  'Grande estándar',
                                  'Intermedia'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento del mapa que se ubica en la parte '
                             'superior e indica el contenido es:',
                 'alternativas': ['El título',
                                  'La escala',
                                  'La red geográfica',
                                  'La leyenda',
                                  'La orientación'],
                 'correcta': 'A'},
                {'pregunta': 'En un mapa correctamente orientado, el Norte '
                             'corresponde a la parte:',
                 'alternativas': ['Inferior',
                                  'Derecha',
                                  'Superior',
                                  'Central',
                                  'Izquierda'],
                 'correcta': 'C'},
                {'pregunta': 'La ubicación de un mapa se determina mediante:',
                 'alternativas': ['Los colores usados',
                                  'El título',
                                  'La red de meridianos y paralelos',
                                  'El tamaño del papel',
                                  'La leyenda únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los signos convencionales de un mapa '
                             'constituyen:',
                 'alternativas': ['La leyenda',
                                  'El marco',
                                  'La escala',
                                  'La orientación',
                                  'El título'],
                 'correcta': 'A'},
                {'pregunta': 'Una escala de 1:100 000 significa que el '
                             'terreno real fue reducido:',
                 'alternativas': ['10 veces',
                                  '100 000 veces',
                                  '1000 veces',
                                  '1 000 000 veces',
                                  '100 veces'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa climático indica la distribución de:',
                 'alternativas': ['Los diversos tipos de clima',
                                  'Fronteras políticas',
                                  'Especies vegetales',
                                  'Ríos y lagos',
                                  'Actividades económicas'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa hidrográfico indica principalmente:',
                 'alternativas': ['Fronteras administrativas',
                                  'Densidad poblacional',
                                  'Tipos de clima',
                                  'La distribución de ríos y lagos',
                                  'Actividades agrícolas'],
                 'correcta': 'D'},
                {'pregunta': 'Un mapa político indica:',
                 'alternativas': ['Fronteras políticas y límites '
                                  'administrativos',
                                  'Recursos minerales',
                                  'Tipos de suelo',
                                  'Tipos de vegetación',
                                  'Distribución de lenguas'],
                 'correcta': 'A'},
                {'pregunta': 'Un mapa económico indica la distribución '
                             'territorial de:',
                 'alternativas': ['Los climas',
                                  'Las actividades económicas',
                                  'Las fronteras',
                                  'Las lenguas habladas',
                                  'Los acontecimientos históricos'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa lingüístico corresponde a un mapa '
                             'temático de tipo:',
                 'alternativas': ['Físico',
                                  'Hidrográfico',
                                  'Climático',
                                  'Geológico',
                                  'Humano'],
                 'correcta': 'E'},
                {'pregunta': 'Un mapa geológico indica:',
                 'alternativas': ['La densidad de población',
                                  'La composición de las rocas de la corteza '
                                  'terrestre',
                                  'La distribución de lenguas',
                                  'Las actividades económicas',
                                  'Las fronteras políticas'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas generales suelen aparecer en:',
                 'alternativas': ['Solo periódicos',
                                  'Solo documentos legales',
                                  'Los atlas',
                                  'Solo internet',
                                  'Solo revistas científicas'],
                 'correcta': 'C'},
                {'pregunta': 'Un mapa de provincias y departamentos '
                             'corresponde a una escala:',
                 'alternativas': ['Muy grande',
                                  'Pequeña extrema',
                                  'Intermedia',
                                  'Nula',
                                  'Muy pequeña'],
                 'correcta': 'C'},
                {'pregunta': 'La ventaja principal del mapa frente a la '
                             'esfera terrestre es:',
                 'alternativas': ['Eliminar toda deformación',
                                  'Facilidad de manejo y representación '
                                  'ampliada de áreas pequeñas',
                                  'Mayor exactitud absoluta',
                                  'Representar en tres dimensiones',
                                  'No requerir escala'],
                 'correcta': 'B'},
                {'pregunta': 'La escala que emplea segmentos gráficos para '
                             'indicar la proporción entre la distancia y su '
                             'medida en el mapa es la: (II CEPRU 2022)',
                 'alternativas': ['Escala numérica',
                                  'Escala natural',
                                  'Escala gráfica',
                                  'Escala de reducción',
                                  'Escala de ampliación'],
                 'correcta': 'C'},
                {'pregunta': 'La proyección cartográfica que se emplea para '
                             'graficar zonas de alta latitud es: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Mercator',
                                  'Cónica',
                                  'Escalar',
                                  'Rectangular',
                                  'Azimutal'],
                 'correcta': 'E'},
                {'pregunta': 'La Carta Geográfica Nacional del Perú es un '
                             'gran mapa dividido en un número de hojas igual '
                             'a:',
                 'alternativas': ['305', '501', '201', '101', '601'],
                 'correcta': 'B'},
                {'pregunta': 'La Carta Geográfica Nacional del Perú se ha '
                             'levantado a una escala de:',
                 'alternativas': ['1:50 000',
                                  '1:100 000',
                                  '1:200 000',
                                  '1:1 000 000',
                                  '1:10 000'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo de la Carta Geográfica Nacional fue '
                             'iniciado por el:',
                 'alternativas': ['Instituto Nacional de Estadística',
                                  'Instituto Geográfico Militar',
                                  'Ministerio de Defensa',
                                  'Instituto Geofísico del Perú',
                                  'Servicio Nacional de Meteorología'],
                 'correcta': 'B'},
                {'pregunta': 'Cada hoja de la Carta Geográfica Nacional '
                             'representa un área de longitud y latitud de:',
                 'alternativas': ['15 minutos',
                                  '30 minutos',
                                  '60 minutos',
                                  '45 minutos',
                                  '20 minutos'],
                 'correcta': 'B'},
                {'pregunta': 'Una hoja o mapa topográfico está compuesta de '
                             'tres partes: cuerpo, signos convencionales y:',
                 'alternativas': ['Escala numérica',
                                  'Información marginal',
                                  'Coordenadas UTM',
                                  'Curvas de nivel',
                                  'Red geográfica'],
                 'correcta': 'B'},
                {'pregunta': 'En la hoja de la Carta Geográfica Nacional, la '
                             'planimetría y la altimetría forman parte de:',
                 'alternativas': ['El sistema de coordenadas',
                                  'La escala de la hoja',
                                  'El cuerpo de la hoja',
                                  'La información marginal',
                                  'Los signos convencionales'],
                 'correcta': 'C'},
                {'pregunta': 'La ubicación del espacio en un plano mediante '
                             'simbología convencional, representando '
                             'elementos naturales o culturales, se llama:',
                 'alternativas': ['Altimetría',
                                  'Planimetría',
                                  'Isoyeta',
                                  'Curva de nivel',
                                  'Leyenda'],
                 'correcta': 'B'},
                {'pregunta': 'Las curvas de nivel, que indican la altitud '
                             'sobre el nivel del mar, forman parte de la:',
                 'alternativas': ['Planimetría',
                                  'Altimetría',
                                  'Leyenda',
                                  'Información marginal',
                                  'Escala'],
                 'correcta': 'B'}],
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
                                'convertir a escala numérica.']}]},
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
                           'formando las {fosas} marinas.']}],
  'cuadros': [{'titulo': '5.1 ESTRUCTURA INTERNA DE LA TIERRA',
               'encabezados': ['Capa', '% del volumen', 'Espesor'],
               'filas': [['{Corteza}', '1%', '5 a 70 km'],
                         ['{Manto}', '83%', '2800 km'],
                         ['{Núcleo}', '16%', '3450 km']]}],
  'preguntas': [{'pregunta': 'El núcleo terrestre está formado '
                             'principalmente por:',
                 'alternativas': ['Carbono e hidrógeno',
                                  'Potasio y sodio',
                                  'Silicio y aluminio',
                                  'Níquel y hierro',
                                  'Magnesio y oxígeno'],
                 'correcta': 'D'},
                {'pregunta': 'La discontinuidad que limita el núcleo externo '
                             'del núcleo interno es la de:',
                 'alternativas': ['Mohorovicic',
                                  'Repetti',
                                  'Gutemberg',
                                  'Lehman',
                                  'Conrad'],
                 'correcta': 'D'},
                {'pregunta': 'El núcleo está limitado con el manto por la '
                             'discontinuidad de:',
                 'alternativas': ['Conrad',
                                  'Mohorovicic',
                                  'Lehman',
                                  'Wiechert Gutemberg',
                                  'Repetti'],
                 'correcta': 'D'},
                {'pregunta': 'El manto externo y el manto interno están '
                             'separados por la discontinuidad de:',
                 'alternativas': ['Mohorovicic',
                                  'Gutemberg',
                                  'Lehman',
                                  'Conrad',
                                  'Repetti'],
                 'correcta': 'E'},
                {'pregunta': 'El manto está limitado con la corteza '
                             'terrestre por la discontinuidad de:',
                 'alternativas': ['Lehman',
                                  'Conrad',
                                  'Repetti',
                                  'Gutemberg',
                                  'Mohorovicic'],
                 'correcta': 'E'},
                {'pregunta': 'La astenósfera es una capa ubicada en:',
                 'alternativas': ['La parte superior del manto',
                                  'El núcleo externo',
                                  'El núcleo interno',
                                  'La corteza oceánica',
                                  'La corteza continental'],
                 'correcta': 'A'},
                {'pregunta': 'La astenósfera es clave para explicar la '
                             'teoría de:',
                 'alternativas': ['La formación de galaxias',
                                  'La formación del universo',
                                  'El Big Bang',
                                  'El ciclo del agua',
                                  'La Tectónica de Placas'],
                 'correcta': 'E'},
                {'pregunta': 'La corteza continental o granítica se compone '
                             'principalmente de:',
                 'alternativas': ['Carbono y oxígeno',
                                  'Silicio y magnesio',
                                  'Silicio y aluminio',
                                  'Potasio y calcio',
                                  'Hierro y níquel'],
                 'correcta': 'C'},
                {'pregunta': 'La corteza oceánica o basáltica se compone '
                             'principalmente de:',
                 'alternativas': ['Oxígeno y carbono',
                                  'Hierro y níquel',
                                  'Calcio y sodio',
                                  'Silicio y magnesio',
                                  'Silicio y aluminio'],
                 'correcta': 'D'},
                {'pregunta': 'La corteza externa y la corteza interna están '
                             'separadas por la discontinuidad de:',
                 'alternativas': ['Lehman',
                                  'Repetti',
                                  'Conrad',
                                  'Mohorovicic',
                                  'Gutemberg'],
                 'correcta': 'C'},
                {'pregunta': 'El relieve terrestre se define como el '
                             'conjunto de:',
                 'alternativas': ['Irregularidades o geoformas de la '
                                  'superficie',
                                  'Climas del planeta',
                                  'Corrientes marinas',
                                  'Zonas sísmicas únicamente',
                                  'Capas de la atmósfera'],
                 'correcta': 'A'},
                {'pregunta': 'Los procesos que actúan del interior hacia la '
                             'superficie terrestre se llaman:',
                 'alternativas': ['Meteorización',
                                  'Erosión eólica',
                                  'Geodinámica interna',
                                  'Geodinámica externa',
                                  'Sedimentación'],
                 'correcta': 'C'},
                {'pregunta': 'La geodinámica interna es considerada una '
                             'fuerza:',
                 'alternativas': ['Sin efecto en el relieve',
                                  'Destructora del relieve',
                                  'Solo erosiva',
                                  'Constructora del relieve',
                                  'Exclusivamente marina'],
                 'correcta': 'D'},
                {'pregunta': 'Los movimientos orogénicos originan '
                             'principalmente:',
                 'alternativas': ['Plegamientos y fallas',
                                  'Erosión costera',
                                  'Formación de dunas',
                                  'Glaciación',
                                  'Sedimentación fluvial'],
                 'correcta': 'A'},
                {'pregunta': 'Los movimientos orogénicos se caracterizan por '
                             'ser:',
                 'alternativas': ['Laterales, compresivos y lentos',
                                  'Verticales y rápidos',
                                  'Explosivos',
                                  'Aleatorios',
                                  'Solo horizontales rápidos'],
                 'correcta': 'A'},
                {'pregunta': 'Los movimientos epirogénicos también se '
                             'conocen como:',
                 'alternativas': ['Erosión interna',
                                  'Tectónica horizontal',
                                  'Tectónica vertical',
                                  'Vulcanismo puro',
                                  'Sismicidad superficial'],
                 'correcta': 'C'},
                {'pregunta': 'El origen de los movimientos epirogénicos se '
                             'encuentra en:',
                 'alternativas': ['Las corrientes marinas',
                                  'La erosión eólica',
                                  'El vulcanismo',
                                  'La meteorización química',
                                  'La isostasia'],
                 'correcta': 'E'},
                {'pregunta': 'Los movimientos epirogénicos afectan grandes '
                             'extensiones sin:',
                 'alternativas': ['Elevar el terreno',
                                  'Deformar la estructura geológica de las '
                                  'rocas',
                                  'Hundir el terreno',
                                  'Generar continentes',
                                  'Modificar la altitud'],
                 'correcta': 'B'},
                {'pregunta': 'La geodinámica interna comprende movimientos '
                             'orogénicos, epirogénicos y:',
                 'alternativas': ['Meteorización física',
                                  'Vulcanismo',
                                  'Glaciarismo',
                                  'Sedimentación eólica',
                                  'Erosión fluvial'],
                 'correcta': 'B'},
                {'pregunta': 'El manto representa aproximadamente qué '
                             'porcentaje del volumen terrestre:',
                 'alternativas': ['16%', '83%', '1%', '25%', '50%'],
                 'correcta': 'B'},
                {'pregunta': 'La segunda cordillera con mayor superficie '
                             'glaciar en el Perú es: (II CEPRU 2025)',
                 'alternativas': ['Huatapallana',
                                  'Vilcanota',
                                  'Ampato',
                                  'Huayhuash',
                                  'Vilcabamba'],
                 'correcta': 'B'},
                {'pregunta': 'Las placas tectónicas en sentido convergente '
                             'originan bordes: (II CEPRU 2024)',
                 'alternativas': ['Constructivos',
                                  'Conservativos',
                                  'Destructivos',
                                  'Moderados',
                                  'Convencionales'],
                 'correcta': 'C'},
                {'pregunta': 'En un glaciar, la parte donde se produce la '
                             'pérdida de masa de hielo se llama: (II CEPRU '
                             '2024)',
                 'alternativas': ['Zona de acumulación',
                                  'Morrenas glaciares',
                                  'Línea de equilibrio',
                                  'Zona de ablación',
                                  'Área de compactación'],
                 'correcta': 'D'},
                {'pregunta': 'Es la discontinuidad entre el núcleo interno y '
                             'el núcleo externo: (II CEPRU 2022)',
                 'alternativas': ['Conrad',
                                  'W. Gutenberg',
                                  'Mohorovicic',
                                  'Lehman',
                                  'Repetti'],
                 'correcta': 'D'},
                {'pregunta': 'Ciencia que estudia el origen, evolución y '
                             'formas de relieve: (I CEPRU 2023)',
                 'alternativas': ['Geodesia',
                                  'Geomorfología',
                                  'Geosistema',
                                  'Edafología',
                                  'Fitogeografía'],
                 'correcta': 'B'},
                {'pregunta': 'Las placas tectónicas se mueven en tres '
                             'direcciones: (I CEPRU 2024)',
                 'alternativas': ['Lateral - convergente - divergente',
                                  'Lateral - horizontal - convergente',
                                  'Divergente - colateral - convergente',
                                  'Convergente - lineal - paralelo',
                                  'Divergente - vertical - lineal'],
                 'correcta': 'A'},
                {'pregunta': 'Las partes de un volcán son: (I CEPRU 2024)',
                 'alternativas': ['Cono, cráter y magma',
                                  'Chimenea, cono y cráter',
                                  'Cámara magmática, cono y lava',
                                  'Cráter, chimenea y cámara magmática',
                                  'Lava, cráter y chimenea'],
                 'correcta': 'B'},
                {'pregunta': 'El intemperismo y la erosión son procesos que '
                             'forman el relieve terrestre, originados por la '
                             'energía: (Primera Oportunidad UNSAAC 2021)',
                 'alternativas': ['De meteoritos',
                                  'Volcánica',
                                  'De la luna',
                                  'Interna de la Tierra',
                                  'Solar'],
                 'correcta': 'E'},
                {'pregunta': 'Las placas tectónicas en su sentido divergente '
                             'se caracterizan por ser: (Primera Oportunidad '
                             'UNSAAC 2023)',
                 'alternativas': ['Constructivas',
                                  'Destructivas',
                                  'Laterales',
                                  'Conservativas',
                                  'Compresivas'],
                 'correcta': 'A'},
                {'pregunta': 'La discontinuidad más próxima al centro de la '
                             'Tierra es: (Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Repetti',
                                  'Gutenberg',
                                  'Conrad',
                                  'Mohorovicic',
                                  'Lehman'],
                 'correcta': 'E'},
                {'pregunta': 'Es considerado el nevado más alto de la zona '
                             'tropical del mundo: (Primera Oportunidad '
                             'UNSAAC 2020)',
                 'alternativas': ['Misti',
                                  'Barroso',
                                  'Salkantay',
                                  'Huascarán',
                                  'Alpamayo'],
                 'correcta': 'D'}],
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
                                'óxidos de magnesio, hierro y silicio.',
                                'El manto está limitado con la corteza por '
                                'la Discontinuidad de Mohorovicic.',
                                'La astenósfera es una capa débil, blanda y '
                                'plástica del manto, ubicada entre 100 y 300 '
                                'km de profundidad, clave para la Tectónica '
                                'de Placas.']},
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
                                'Sudamericana.',
                                'En el sentido convergente, cuando una placa '
                                'oceánica choca con una continental, se '
                                'produce la subducción, originando bordes '
                                'destructivos.',
                                'En el sentido divergente, las placas se '
                                'separan formando dorsales mesoceánicas y '
                                'bordes constructivos.',
                                'En el sentido lateral, las placas se '
                                'desplazan una junto a otra originando '
                                'fallas transformantes y bordes '
                                'conservativos.',
                                'La subducción consiste en el hundimiento de '
                                'una placa oceánica bajo una placa '
                                'continental, formando las fosas '
                                'marinas.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El territorio peruano se ubica en la zona '
                           '{Tórrida}.',
                           'El Perú es considerado el país de América del '
                           'Sur con extensión {La tercera mayor}.',
                           'El punto más alto del Perú es el nevado '
                           '{Huascarán}.',
                           'El punto más bajo del territorio peruano es {La '
                           'Depresión de Bayovar}.',
                           'El lugar más lluvioso del Perú es {Quince Mil}.',
                           'El lugar más caluroso del Perú es {Neshuya}.',
                           'El lugar más frío del Perú es {Imata}.',
                           'La frontera más extensa del Perú es con '
                           '{Brasil}.',
                           'La frontera más corta del Perú es con {Chile}.',
                           'El perímetro total del Perú, incluido el '
                           'litoral, es aproximadamente de {10 156,8 km}.',
                           'Por el sur, el Perú limita con {Chile}.',
                           'Por el este, el Perú limita con {Bolivia y '
                           'Brasil}.',
                           'El punto extremo norte del Perú se relaciona con '
                           'el río {Putumayo}.',
                           'El punto extremo sur del Perú se ubica en '
                           '{Tacna}.',
                           'El punto extremo este del Perú limita con '
                           '{Bolivia}.',
                           'La región Costa representa del área continental '
                           'peruana {12,5%}.',
                           'La región Andina representa del área continental '
                           'peruana {30,2%}.',
                           'El litoral peruano se extiende desde Boca de '
                           'Capones hasta {El hito La Concordia}.',
                           'La longitud del litoral peruano es '
                           'aproximadamente de {3 080 km}.',
                           'El ancho del territorio peruano, de este a '
                           'oeste, es de aproximadamente {1 640 km}.']}],
  'cuadros': [{'titulo': '6.3 FRONTERAS DEL PERÚ',
               'encabezados': ['País', 'Longitud'],
               'filas': [['{Ecuador}', '1528,5 km'],
                         ['Colombia', '1506,0 km'],
                         ['{Brasil}', '2822,5 km'],
                         ['Bolivia', '1047,1 km'],
                         ['{Chile}', '169,1 km']]}],
  'preguntas': [{'pregunta': 'El territorio peruano se ubica en la zona:',
                 'alternativas': ['Templada',
                                  'Subtropical',
                                  'Tórrida',
                                  'Glacial',
                                  'Polar'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú es considerado el país de América del '
                             'Sur con extensión:',
                 'alternativas': ['La mayor',
                                  'La tercera mayor',
                                  'La segunda menor',
                                  'La cuarta mayor',
                                  'La menor'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más alto del Perú es el nevado:',
                 'alternativas': ['Huascarán',
                                  'Alpamayo',
                                  'Ausangate',
                                  'Salkantay',
                                  'Coropuna'],
                 'correcta': 'A'},
                {'pregunta': 'El punto más bajo del territorio peruano es:',
                 'alternativas': ['El valle del Colca',
                                  'La Depresión de Bayovar',
                                  'El desierto de Sechura',
                                  'La fosa de Tacna',
                                  'El lago Titicaca'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más lluvioso del Perú es:',
                 'alternativas': ['Moyobamba',
                                  'Quince Mil',
                                  'Chachapoyas',
                                  'Tarapoto',
                                  'Iquitos'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más caluroso del Perú es:',
                 'alternativas': ['Piura',
                                  'Sechura',
                                  'Neshuya',
                                  'Tumbes',
                                  'Jaén'],
                 'correcta': 'C'},
                {'pregunta': 'El lugar más frío del Perú es:',
                 'alternativas': ['Cusco',
                                  'Puno',
                                  'El Misti',
                                  'Juliaca',
                                  'Imata'],
                 'correcta': 'E'},
                {'pregunta': 'La frontera más extensa del Perú es con:',
                 'alternativas': ['Brasil',
                                  'Ecuador',
                                  'Colombia',
                                  'Chile',
                                  'Bolivia'],
                 'correcta': 'A'},
                {'pregunta': 'La frontera más corta del Perú es con:',
                 'alternativas': ['Colombia',
                                  'Ecuador',
                                  'Bolivia',
                                  'Brasil',
                                  'Chile'],
                 'correcta': 'E'},
                {'pregunta': 'El perímetro total del Perú, incluido el '
                             'litoral, es aproximadamente de:',
                 'alternativas': ['15 000 km',
                                  '20 000 km',
                                  '10 156,8 km',
                                  '1 000 km',
                                  '5 000 km'],
                 'correcta': 'C'},
                {'pregunta': 'Por el sur, el Perú limita con:',
                 'alternativas': ['Ecuador',
                                  'Brasil',
                                  'Bolivia',
                                  'Chile',
                                  'Colombia'],
                 'correcta': 'D'},
                {'pregunta': 'Por el este, el Perú limita con:',
                 'alternativas': ['Chile y Bolivia',
                                  'Ecuador y Colombia',
                                  'Bolivia y Brasil',
                                  'Solo Bolivia',
                                  'Solo Brasil'],
                 'correcta': 'C'},
                {'pregunta': 'El punto extremo norte del Perú se relaciona '
                             'con el río:',
                 'alternativas': ['Madre de Dios',
                                  'Marañón',
                                  'Ucayali',
                                  'Amazonas',
                                  'Putumayo'],
                 'correcta': 'E'},
                {'pregunta': 'El punto extremo sur del Perú se ubica en:',
                 'alternativas': ['Puno',
                                  'Tacna',
                                  'Arequipa',
                                  'Ica',
                                  'Moquegua'],
                 'correcta': 'B'},
                {'pregunta': 'El punto extremo este del Perú limita con:',
                 'alternativas': ['Colombia',
                                  'Bolivia',
                                  'Ecuador',
                                  'Chile',
                                  'Brasil únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La región Costa representa del área '
                             'continental peruana:',
                 'alternativas': ['30,2%', '20%', '50%', '12,5%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'La región Andina representa del área '
                             'continental peruana:',
                 'alternativas': ['60%', '10%', '30,2%', '12,5%', '45%'],
                 'correcta': 'C'},
                {'pregunta': 'El litoral peruano se extiende desde Boca de '
                             'Capones hasta:',
                 'alternativas': ['Paracas',
                                  'Ilo',
                                  'Tumbes',
                                  'Tacna',
                                  'El hito La Concordia'],
                 'correcta': 'E'},
                {'pregunta': 'La longitud del litoral peruano es '
                             'aproximadamente de:',
                 'alternativas': ['10 000 km',
                                  '5 000 km',
                                  '1 000 km',
                                  '500 km',
                                  '3 080 km'],
                 'correcta': 'E'},
                {'pregunta': 'El ancho del territorio peruano, de este a '
                             'oeste, es de aproximadamente:',
                 'alternativas': ['3 000 km',
                                  '500 km',
                                  '800 km',
                                  '1 640 km',
                                  '2 135 km'],
                 'correcta': 'D'},
                {'pregunta': 'Son características morfológicas de la región '
                             'andina: (I CEPRU 2024)',
                 'alternativas': ['Pampas, manantes y valles transversales',
                                  'Altiplanos, desiertos y acantilados',
                                  'Valles interandinos, mesetas y altiplanos',
                                  'Andenes, quebradas y lagos',
                                  'Mesetas, ríos y picos'],
                 'correcta': 'C'},
                {'pregunta': 'El piso altitudinal que se desarrolla por '
                             'encima de los 4600 m.s.n.m., con temperatura '
                             'media anual menor a 3°C, es: (II CEPRU 2022)',
                 'alternativas': ["Rit'i",
                                  'Puna baja',
                                  'Puna alta',
                                  'Qheswa',
                                  'Yunka'],
                 'correcta': 'A'},
                {'pregunta': 'Es una característica de la vertiente o '
                             'llamada oriental de la Región Andina: (Primera '
                             'Oportunidad UNSAAC 2024)',
                 'alternativas': ['Escasa precipitación',
                                  'Ríos de corto recorrido',
                                  'Árido',
                                  'Escasa vegetación',
                                  'Abundante vegetación'],
                 'correcta': 'E'},
                {'pregunta': 'La ciudad de Yauri, ubicada a 3915 m.s.n.m., '
                             'pertenece al piso climático: (Primera '
                             'Oportunidad UNSAAC 2021)',
                 'alternativas': ['Qheswa baja',
                                  'Qheswa alta',
                                  'Puna baja',
                                  'Transición',
                                  'Puna alta'],
                 'correcta': 'C'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['El territorio peruano se ubica en la zona '
                                'Tórrida.',
                                'El Perú es considerado el país de América '
                                'del Sur con extensión La tercera mayor.',
                                'El punto más alto del Perú es el nevado '
                                'Huascarán.',
                                'El punto más bajo del territorio peruano es '
                                'La Depresión de Bayovar.',
                                'El lugar más lluvioso del Perú es Quince '
                                'Mil.',
                                'El lugar más caluroso del Perú es Neshuya.',
                                'El lugar más frío del Perú es Imata.',
                                'La frontera más extensa del Perú es con '
                                'Brasil.',
                                'La frontera más corta del Perú es con '
                                'Chile.',
                                'El perímetro total del Perú, incluido el '
                                'litoral, es aproximadamente de 10 156,8 '
                                'km.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La región geográfica más extensa del Perú es {La '
                           'Amazónica o Selva}.',
                           'La región amazónica representa del territorio '
                           'nacional aproximadamente {57,3%}.',
                           'La selva alta también se conoce como {Rupa Rupa '
                           'o Ceja de Selva}.',
                           'El relieve de la selva alta está afectado por '
                           '{La Tectónica Andina}.',
                           'Los cortes fluviales donde un río corta una '
                           'cadena de montañas se llaman {Pongos}.',
                           'El Pongo de Mainique fue formado por el río '
                           '{Urubamba}.',
                           'La selva baja también se llama {Omagua o Llanura '
                           'Amazónica}.',
                           'La selva baja no es afectada por la tectónica '
                           'andina porque se asienta sobre {El antiguo '
                           'Cratón Brasileño}.',
                           'Los lagos abandonados por los ríos que cambiaron '
                           'de cauce se llaman {Qochas}.',
                           'Las áreas bajas cubiertas de agua todo el año, '
                           'con palmeras de aguaje, se llaman {Tahuampas o '
                           'aguajales}.',
                           'Las áreas que solo se inundan en las crecidas de '
                           'los ríos se llaman {Restingas}.',
                           'Las ciudades de la selva baja se han edificado '
                           'principalmente en {Los altos}.',
                           'La región Costa representa del territorio '
                           'nacional aproximadamente {12,5%}.',
                           'La región Costa se extiende desde el nivel del '
                           'mar hasta una altitud de {1000 m}.',
                           'La Costa Sur o Meridional se extiende entre la '
                           'frontera con Chile y {La península de Paracas}.',
                           'La Cadena Costanera alcanza su mayor altitud en '
                           '{El cerro Criterión, Ica}.',
                           'Las planicies de origen aluvial en la costa sur '
                           'se llaman {Pampas}.',
                           'Los valles de Jaén y Bagua se ubican en la '
                           'subregión de {Selva alta}.',
                           'El valle de Chanchamayo pertenece al '
                           'departamento de {Junín}.',
                           'El Boquerón del Padre Abad fue formado por el '
                           'río {Yuracyacu}.']}],
  'cuadros': [{'titulo': '7.2 PONGOS DE LA SELVA ALTA',
               'encabezados': ['Pongo', 'Río', 'Departamento'],
               'filas': [['{Manseriche}', 'Marañón', '{Amazonas}'],
                         ['{Mainique}', 'Urubamba', '{Cusco}'],
                         ['{Aguirre}', 'Huallaga', 'San Martín'],
                         ['Del {Tambo}', 'Tambo', 'Junín']]}],
  'preguntas': [{'pregunta': 'La región geográfica más extensa del Perú es:',
                 'alternativas': ['La Andina',
                                  'La Costa',
                                  'Ninguna en particular',
                                  'El litoral',
                                  'La Amazónica o Selva'],
                 'correcta': 'E'},
                {'pregunta': 'La región amazónica representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['30,2%', '12,5%', '90%', '57,3%', '10%'],
                 'correcta': 'D'},
                {'pregunta': 'La selva alta también se conoce como:',
                 'alternativas': ['Omagua',
                                  'Rupa Rupa o Ceja de Selva',
                                  'Llanura Amazónica',
                                  'Cratón Brasileño',
                                  'Selva Baja'],
                 'correcta': 'B'},
                {'pregunta': 'El relieve de la selva alta está afectado por:',
                 'alternativas': ['La sedimentación marina',
                                  'El Cratón Brasileño',
                                  'La Tectónica Andina',
                                  'Solo la erosión eólica',
                                  'El clima ecuatorial'],
                 'correcta': 'C'},
                {'pregunta': 'Los cortes fluviales donde un río corta una '
                             'cadena de montañas se llaman:',
                 'alternativas': ['Pongos',
                                  'Altos',
                                  'Restingas',
                                  'Qochas',
                                  'Tahuampas'],
                 'correcta': 'A'},
                {'pregunta': 'El Pongo de Mainique fue formado por el río:',
                 'alternativas': ['Inambari',
                                  'Tambo',
                                  'Huallaga',
                                  'Urubamba',
                                  'Marañón'],
                 'correcta': 'D'},
                {'pregunta': 'La selva baja también se llama:',
                 'alternativas': ['Ceja de Selva',
                                  'Cordillera Oriental',
                                  'Faja Sub Andina',
                                  'Rupa Rupa',
                                  'Omagua o Llanura Amazónica'],
                 'correcta': 'E'},
                {'pregunta': 'La selva baja no es afectada por la tectónica '
                             'andina porque se asienta sobre:',
                 'alternativas': ['La cadena costanera',
                                  'Los Andes centrales',
                                  'El antiguo Cratón Brasileño',
                                  'La plataforma costanera',
                                  'La Cordillera Oriental'],
                 'correcta': 'C'},
                {'pregunta': 'Los lagos abandonados por los ríos que '
                             'cambiaron de cauce se llaman:',
                 'alternativas': ['Altos',
                                  'Restingas',
                                  'Tahuampas',
                                  'Qochas',
                                  'Filos'],
                 'correcta': 'D'},
                {'pregunta': 'Las áreas bajas cubiertas de agua todo el año, '
                             'con palmeras de aguaje, se llaman:',
                 'alternativas': ['Qochas',
                                  'Tahuampas o aguajales',
                                  'Altos',
                                  'Restingas',
                                  'Filos'],
                 'correcta': 'B'},
                {'pregunta': 'Las áreas que solo se inundan en las crecidas '
                             'de los ríos se llaman:',
                 'alternativas': ['Qochas',
                                  'Filos',
                                  'Tahuampas',
                                  'Restingas',
                                  'Altos'],
                 'correcta': 'D'},
                {'pregunta': 'Las ciudades de la selva baja se han edificado '
                             'principalmente en:',
                 'alternativas': ['Las restingas',
                                  'Los filos',
                                  'Los altos',
                                  'Las qochas',
                                  'Las tahuampas'],
                 'correcta': 'C'},
                {'pregunta': 'La región Costa representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['70%', '30,2%', '57,3%', '12,5%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'La región Costa se extiende desde el nivel del '
                             'mar hasta una altitud de:',
                 'alternativas': ['1500 m',
                                  '300 m',
                                  '500 m',
                                  '1000 m',
                                  '2000 m'],
                 'correcta': 'D'},
                {'pregunta': 'La Costa Sur o Meridional se extiende entre la '
                             'frontera con Chile y:',
                 'alternativas': ['Trujillo',
                                  'La península de Paracas',
                                  'Chiclayo',
                                  'Tumbes',
                                  'Lima'],
                 'correcta': 'B'},
                {'pregunta': 'La Cadena Costanera alcanza su mayor altitud '
                             'en:',
                 'alternativas': ['Arequipa',
                                  'Tacna',
                                  'Lima',
                                  'El cerro Criterión, Ica',
                                  'Piura'],
                 'correcta': 'D'},
                {'pregunta': 'Las planicies de origen aluvial en la costa '
                             'sur se llaman:',
                 'alternativas': ['Pampas',
                                  'Tablazos',
                                  'Tahuampas',
                                  'Aguajales',
                                  'Restingas'],
                 'correcta': 'A'},
                {'pregunta': 'Los valles de Jaén y Bagua se ubican en la '
                             'subregión de:',
                 'alternativas': ['Sierra central',
                                  'Selva alta',
                                  'Selva baja',
                                  'Costa sur',
                                  'Costa norte'],
                 'correcta': 'B'},
                {'pregunta': 'El valle de Chanchamayo pertenece al '
                             'departamento de:',
                 'alternativas': ['Puno',
                                  'Cusco',
                                  'Junín',
                                  'Huánuco',
                                  'San Martín'],
                 'correcta': 'C'},
                {'pregunta': 'El Boquerón del Padre Abad fue formado por el '
                             'río:',
                 'alternativas': ['Marañón',
                                  'Yuracyacu',
                                  'Huallaga',
                                  'Urubamba',
                                  'Tambo'],
                 'correcta': 'B'},
                {'pregunta': 'El desierto de Sechura se localiza en el '
                             'departamento de: (II CEPRU 2025)',
                 'alternativas': ['Lambayeque',
                                  'Moquegua',
                                  'Áncash',
                                  'Piura',
                                  'Ica'],
                 'correcta': 'D'},
                {'pregunta': 'Los bosques de algarrobos y vegetación de '
                             'monte ribereño pertenecen a la: (II CEPRU '
                             '2024)',
                 'alternativas': ['Costa sur',
                                  'Sierra sur',
                                  'Costa central',
                                  'Costa norte',
                                  'Selva norte'],
                 'correcta': 'D'},
                {'pregunta': 'En la costa peruana, los espacios o áreas '
                             'interfluviales emplazadas entre los valles se '
                             'llaman: (II CEPRU 2022)',
                 'alternativas': ['Tablazos',
                                  'Desiertos',
                                  'Depresiones',
                                  'Lomas',
                                  'Pampas'],
                 'correcta': 'E'},
                {'pregunta': 'Los valles de Tocache y Chanchamayo se '
                             'encuentran, respectivamente, en los '
                             'departamentos de: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Loreto - Pasco',
                                  'San Martín - Junín',
                                  'Amazonas - La Libertad',
                                  'Junín - Cajamarca',
                                  'Puno - Ucayali'],
                 'correcta': 'B'},
                {'pregunta': 'La depresión más importante de la costa '
                             'peruana es: (Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Bayóvar',
                                  'Chilca',
                                  'Chivay',
                                  'Otuma',
                                  'Pariñas'],
                 'correcta': 'A'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['La región geográfica más extensa del Perú '
                                'es La Amazónica o Selva.',
                                'La región amazónica representa del '
                                'territorio nacional aproximadamente 57,3%.',
                                'La selva alta también se conoce como Rupa '
                                'Rupa o Ceja de Selva.',
                                'El relieve de la selva alta está afectado '
                                'por La Tectónica Andina.',
                                'Los cortes fluviales donde un río corta una '
                                'cadena de montañas se llaman Pongos.',
                                'El Pongo de Mainique fue formado por el río '
                                'Urubamba.',
                                'La selva baja también se llama Omagua o '
                                'Llanura Amazónica.',
                                'La selva baja no es afectada por la '
                                'tectónica andina porque se asienta sobre El '
                                'antiguo Cratón Brasileño.',
                                'Los lagos abandonados por los ríos que '
                                'cambiaron de cauce se llaman Qochas.',
                                'Las áreas bajas cubiertas de agua todo el '
                                'año, con palmeras de aguaje, se llaman '
                                'Tahuampas o aguajales.']}]},
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
                           '{Marañón}, con 1414 km.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El volumen de agua que transporta un río se '
                           'denomina {Caudal}.',
                           'Cuando un río arrastra la mínima cantidad de '
                           'agua, se le llama {Estiaje}.',
                           'El canal o lecho por donde se desplazan las '
                           'aguas del río se llama {Cauce}.',
                           'La línea que une los puntos más profundos del '
                           'canal fluvial es {El talweg o vaguada}.',
                           'Los ríos que salen de otro río o de un lago se '
                           'denominan {Efluentes}.',
                           'La ANA ha identificado en el Perú un total de '
                           'unidades hidrográficas de {159}.',
                           'La cuenca del Amazonas representa del territorio '
                           'nacional {74,5%}.',
                           'La cuenca hidrográfica más extensa del Perú, de '
                           'América y del mundo es la del {Amazonas}.',
                           'La cuenca del Titicaca representa del territorio '
                           'nacional {3,8%}.',
                           'El lago Titicaca es reconocido mundialmente por '
                           'ser el lago {Navegable más alto del mundo}.',
                           'El lago Titicaca se ubica a una altitud '
                           'aproximada de {3 810 m}.',
                           'El origen geológico del lago Titicaca es '
                           '{Tectónico}.',
                           'El lago Titicaca se divide en dos sectores '
                           'separados por el Estrecho de {Tiquina}.',
                           'El sector del Titicaca correspondiente al Perú '
                           'se llama lago Mayor o {Chucuito}.',
                           'El único río efluente del lago Titicaca es el '
                           'río {Desaguadero}.',
                           'El río Desaguadero desemboca finalmente en el '
                           'lago {Poopó}.',
                           'El río más extenso del Perú es el {Ucayali}.',
                           'El segundo río más extenso del Perú es el '
                           '{Marañón}.',
                           'El río Ramis, principal afluente del Titicaca, '
                           'tiene una longitud de {304 km}.',
                           'El río Rímac nace en el nevado de {Tíclio}.']}],
  'cuadros': [{'titulo': '8.4 LOS RÍOS MÁS EXTENSOS DEL PERÚ',
               'encabezados': ['Río', 'Longitud'],
               'filas': [['{Ucayali}', '1771 km'],
                         ['{Marañón}', '1414 km'],
                         ['Putumayo', '1380 km'],
                         ['{Yavarí}', '1184 km'],
                         ['Huallaga', '1138 km']]}],
  'preguntas': [{'pregunta': 'El volumen de agua que transporta un río se '
                             'denomina:',
                 'alternativas': ['Curso',
                                  'Talweg',
                                  'Cauce',
                                  'Régimen',
                                  'Caudal'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando un río arrastra la mínima cantidad de '
                             'agua, se le llama:',
                 'alternativas': ['Crecida',
                                  'Torrente',
                                  'Cauce',
                                  'Estiaje',
                                  'Afluente'],
                 'correcta': 'D'},
                {'pregunta': 'El canal o lecho por donde se desplazan las '
                             'aguas del río se llama:',
                 'alternativas': ['Talweg',
                                  'Régimen',
                                  'Vertiente',
                                  'Curso',
                                  'Cauce'],
                 'correcta': 'E'},
                {'pregunta': 'La línea que une los puntos más profundos del '
                             'canal fluvial es:',
                 'alternativas': ['El talweg o vaguada',
                                  'El cauce',
                                  'El curso',
                                  'La cuenca',
                                  'El régimen'],
                 'correcta': 'A'},
                {'pregunta': 'Los ríos que salen de otro río o de un lago se '
                             'denominan:',
                 'alternativas': ['Torrentosos',
                                  'Efluentes',
                                  'Confluentes',
                                  'Principales',
                                  'Afluentes'],
                 'correcta': 'B'},
                {'pregunta': 'La ANA ha identificado en el Perú un total de '
                             'unidades hidrográficas de:',
                 'alternativas': ['99', '159', '59', '359', '259'],
                 'correcta': 'B'},
                {'pregunta': 'La cuenca del Amazonas representa del '
                             'territorio nacional:',
                 'alternativas': ['3,8%', '12,5%', '74,5%', '57,3%', '30,2%'],
                 'correcta': 'C'},
                {'pregunta': 'La cuenca hidrográfica más extensa del Perú, '
                             'de América y del mundo es la del:',
                 'alternativas': ['Marañón',
                                  'Ucayali',
                                  'Amazonas',
                                  'Titicaca',
                                  'Pacífico'],
                 'correcta': 'C'},
                {'pregunta': 'La cuenca del Titicaca representa del '
                             'territorio nacional:',
                 'alternativas': ['12,5%', '57,3%', '30,2%', '3,8%', '74,5%'],
                 'correcta': 'D'},
                {'pregunta': 'El lago Titicaca es reconocido mundialmente '
                             'por ser el lago:',
                 'alternativas': ['Más extenso de Sudamérica',
                                  'Con más islas del mundo',
                                  'Navegable más alto del mundo',
                                  'Más profundo del mundo',
                                  'Más frío del planeta'],
                 'correcta': 'C'},
                {'pregunta': 'El lago Titicaca se ubica a una altitud '
                             'aproximada de:',
                 'alternativas': ['1 800 m',
                                  '2 500 m',
                                  '5 000 m',
                                  '3 810 m',
                                  '4 500 m'],
                 'correcta': 'D'},
                {'pregunta': 'El origen geológico del lago Titicaca es:',
                 'alternativas': ['Kárstico',
                                  'Eólico',
                                  'Volcánico',
                                  'Glaciar exclusivamente',
                                  'Tectónico'],
                 'correcta': 'E'},
                {'pregunta': 'El lago Titicaca se divide en dos sectores '
                             'separados por el Estrecho de:',
                 'alternativas': ['Panamá',
                                  'Bering',
                                  'Tiquina',
                                  'Magallanes',
                                  'Gibraltar'],
                 'correcta': 'C'},
                {'pregunta': 'El sector del Titicaca correspondiente al Perú '
                             'se llama lago Mayor o:',
                 'alternativas': ['Huiñaymarca',
                                  'Taraco',
                                  'Poopó',
                                  'Chucuito',
                                  'Uros'],
                 'correcta': 'D'},
                {'pregunta': 'El único río efluente del lago Titicaca es el '
                             'río:',
                 'alternativas': ['Ilave',
                                  'Suchez',
                                  'Ramis',
                                  'Coata',
                                  'Desaguadero'],
                 'correcta': 'E'},
                {'pregunta': 'El río Desaguadero desemboca finalmente en el '
                             'lago:',
                 'alternativas': ['Titicaca',
                                  'Parinacochas',
                                  'Junín',
                                  'Poopó',
                                  'Chinchaycocha'],
                 'correcta': 'D'},
                {'pregunta': 'El río más extenso del Perú es el:',
                 'alternativas': ['Amazonas',
                                  'Huallaga',
                                  'Mantaro',
                                  'Marañón',
                                  'Ucayali'],
                 'correcta': 'E'},
                {'pregunta': 'El segundo río más extenso del Perú es el:',
                 'alternativas': ['Vilcanota',
                                  'Ucayali',
                                  'Putumayo',
                                  'Marañón',
                                  'Yavarí'],
                 'correcta': 'D'},
                {'pregunta': 'El río Ramis, principal afluente del Titicaca, '
                             'tiene una longitud de:',
                 'alternativas': ['180 km',
                                  '304 km',
                                  '500 km',
                                  '163 km',
                                  '250 km'],
                 'correcta': 'B'},
                {'pregunta': 'El río Rímac nace en el nevado de:',
                 'alternativas': ['Huascarán',
                                  'Tíclio',
                                  'Coropuna',
                                  'Salkantay',
                                  'Ausangate'],
                 'correcta': 'B'},
                {'pregunta': 'La confluencia de los ríos Apurímac y Mantaro '
                             'forman el río: (II CEPRU 2025)',
                 'alternativas': ['Tambo',
                                  'Ucayali',
                                  'Huallaga',
                                  'Ene',
                                  'Perené'],
                 'correcta': 'D'},
                {'pregunta': 'En la llanura amazónica, las Qochas o lagos de '
                             'media luna son originados por la dinámica: '
                             '(Primera Oportunidad UNSAAC 2021)',
                 'alternativas': ['Forestal',
                                  'Fluvial',
                                  'Faunística',
                                  'Eólica',
                                  'Mareomotriz'],
                 'correcta': 'B'},
                {'pregunta': 'Los ríos cuyas nacientes y recorrido se '
                             'encuentran en la vertiente occidental de los '
                             'Andes peruanos, de régimen irregular y con '
                             'dirección de este a oeste, corresponden a la '
                             'región hidrográfica del: (Primera Oportunidad '
                             'UNSAAC 2021)',
                 'alternativas': ['Ucayali',
                                  'Alto Madre de Dios',
                                  'Titicaca',
                                  'Pacífico',
                                  'Amazonas'],
                 'correcta': 'D'},
                {'pregunta': 'El río de la cuenca del Pacífico que erosiona '
                             'el Cañón del Pato es el río: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Rímac',
                                  'Virú',
                                  'Tumbes',
                                  'Santa',
                                  'Chira'],
                 'correcta': 'D'},
                {'pregunta': 'El río Amazonas se forma en la localidad de '
                             'Nauta a partir de la confluencia de los ríos: '
                             '(Primera Oportunidad UNSAAC 2020)',
                 'alternativas': ['Tambo y Urubamba',
                                  'Palcazu y Piches',
                                  'Mantaro y Apurímac',
                                  'Marañón y Ucayali',
                                  'Ene y Perené'],
                 'correcta': 'D'}],
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
                                'Marañón, con 1414 km.']},
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['El volumen de agua que transporta un río se '
                                'denomina Caudal.',
                                'Cuando un río arrastra la mínima cantidad '
                                'de agua, se le llama Estiaje.',
                                'El canal o lecho por donde se desplazan las '
                                'aguas del río se llama Cauce.',
                                'La línea que une los puntos más profundos '
                                'del canal fluvial es El talweg o vaguada.',
                                'Los ríos que salen de otro río o de un lago '
                                'se denominan Efluentes.',
                                'La ANA ha identificado en el Perú un total '
                                'de unidades hidrográficas de 159.',
                                'La cuenca del Amazonas representa del '
                                'territorio nacional 74,5%.',
                                'La cuenca hidrográfica más extensa del '
                                'Perú, de América y del mundo es la del '
                                'Amazonas.',
                                'La cuenca del Titicaca representa del '
                                'territorio nacional 3,8%.',
                                'El lago Titicaca es reconocido mundialmente '
                                'por ser el lago Navegable más alto del '
                                'mundo.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El mar peruano se extiende, en distancia, hasta '
                           '{200 millas}.',
                           'La extensión del mar peruano representa del '
                           'territorio peruano aproximadamente {90%}.',
                           'Tras el fallo de la Corte de La Haya, el Perú '
                           'obtuvo adicionalmente {50 284 km²}.',
                           'El mar peruano se distingue de otros por la '
                           'presencia de {La Corriente Peruana y la frialdad '
                           'de sus aguas}.',
                           'La doctrina de las 200 millas fue proclamada por '
                           'Perú junto con Ecuador y {Chile}.',
                           'La tesis de las 200 millas se declaró mediante '
                           'el D.S. N° 781 en el gobierno de {José '
                           'Bustamante y Rivero}.',
                           'La tesis de las 200 millas se proclamó en el año '
                           '{1947}.',
                           'La región norte del mar peruano se extiende '
                           'desde la Península de Illescas hasta {Boca de '
                           'Capones}.',
                           'El color del mar en la región norte se debe '
                           'principalmente a {La descarga de los ríos}.',
                           'La temperatura promedio del mar en la región '
                           'central y sur es de {18°C}.',
                           'El color verdoso del mar en la región central y '
                           'sur se debe a {El plancton y las algas}.',
                           'El fenómeno del afloramiento consiste en {El '
                           'ascenso de aguas frías hacia la superficie}.',
                           'La plataforma o zócalo continental llega hasta '
                           'la isóbata de {200 m}.',
                           'El talud continental se extiende entre las '
                           'isóbatas de {200 a 5000 m}.',
                           'Las fosas marinas se producen por {La subducción '
                           'de la Placa de Nasca}.',
                           'La Dorsal de Nasca es {Una cordillera submarina '
                           'volcánica}.',
                           'La Dorsal de Nasca se ubica aproximadamente a '
                           'qué distancia de la costa de Ica {150 km}.',
                           'El fundamento geológico de la Tesis de las 200 '
                           'millas se refiere a {La continuidad del zócalo '
                           'continental}.',
                           'La salinidad del mar en la región norte es de '
                           'aproximadamente {34 gr/l}.']}],
  'cuadros': [{'titulo': '9.4 RELIEVE SUBMARINO DEL MAR PERUANO',
               'encabezados': ['Elemento', 'Profundidad'],
               'filas': [['{Zócalo} continental', 'Hasta 200 m'],
                         ['{Talud} continental', '200 a 5000 m'],
                         ['{Fosas} marinas', 'Mayores profundidades']]}],
  'preguntas': [{'pregunta': 'El mar peruano se extiende, en distancia, '
                             'hasta:',
                 'alternativas': ['150 millas',
                                  '300 millas',
                                  '200 millas',
                                  '100 millas',
                                  '50 millas'],
                 'correcta': 'C'},
                {'pregunta': 'La extensión del mar peruano representa del '
                             'territorio peruano aproximadamente:',
                 'alternativas': ['70%', '50%', '30%', '20%', '90%'],
                 'correcta': 'E'},
                {'pregunta': 'Tras el fallo de la Corte de La Haya, el Perú '
                             'obtuvo adicionalmente:',
                 'alternativas': ['500 km²',
                                  '200 000 km²',
                                  '100 000 km²',
                                  '50 284 km²',
                                  '10 000 km²'],
                 'correcta': 'D'},
                {'pregunta': 'El mar peruano se distingue de otros por la '
                             'presencia de:',
                 'alternativas': ['Aguas cálidas todo el año',
                                  'Ausencia de peces',
                                  'Aguas dulces',
                                  'La Corriente Peruana y la frialdad de sus '
                                  'aguas',
                                  'Escasa vida marina'],
                 'correcta': 'D'},
                {'pregunta': 'La doctrina de las 200 millas fue proclamada '
                             'por Perú junto con Ecuador y:',
                 'alternativas': ['Bolivia',
                                  'Chile',
                                  'Argentina',
                                  'Brasil',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis de las 200 millas se declaró mediante '
                             'el D.S. N° 781 en el gobierno de:',
                 'alternativas': ['José Bustamante y Rivero',
                                  'Alberto Fujimori',
                                  'Alan García',
                                  'Fernando Belaunde',
                                  'Manuel A. Odría'],
                 'correcta': 'A'},
                {'pregunta': 'La tesis de las 200 millas se proclamó en el '
                             'año:',
                 'alternativas': ['1947', '1993', '1980', '1960', '1930'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los fundamentos de la Tesis de las 200 '
                             'millas NO figura el fundamento:',
                 'alternativas': ['Geológico',
                                  'Económico',
                                  'Estratégico',
                                  'Religioso',
                                  'Biológico'],
                 'correcta': 'D'},
                {'pregunta': 'La región norte del mar peruano se extiende '
                             'desde la Península de Illescas hasta:',
                 'alternativas': ['Paracas',
                                  'Ica',
                                  'Trujillo',
                                  'Boca de Capones',
                                  'Tacna'],
                 'correcta': 'D'},
                {'pregunta': 'El color del mar en la región norte se debe '
                             'principalmente a:',
                 'alternativas': ['El afloramiento',
                                  'La sal',
                                  'La descarga de los ríos',
                                  'Las algas',
                                  'El plancton'],
                 'correcta': 'C'},
                {'pregunta': 'La temperatura promedio del mar en la región '
                             'central y sur es de:',
                 'alternativas': ['5°C', '10°C', '25°C', '30°C', '18°C'],
                 'correcta': 'E'},
                {'pregunta': 'El color verdoso del mar en la región central '
                             'y sur se debe a:',
                 'alternativas': ['El plancton y las algas',
                                  'La temperatura',
                                  'Los sedimentos fluviales',
                                  'La arena',
                                  'Las corrientes cálidas'],
                 'correcta': 'A'},
                {'pregunta': 'El fenómeno del afloramiento consiste en:',
                 'alternativas': ['El derretimiento de glaciares',
                                  'La formación de olas',
                                  'El ascenso de aguas frías hacia la '
                                  'superficie',
                                  'El hundimiento de aguas cálidas',
                                  'La evaporación del mar'],
                 'correcta': 'C'},
                {'pregunta': 'La plataforma o zócalo continental llega hasta '
                             'la isóbata de:',
                 'alternativas': ['500 m',
                                  '1000 m',
                                  '50 m',
                                  '200 m',
                                  '100 m'],
                 'correcta': 'D'},
                {'pregunta': 'El talud continental se extiende entre las '
                             'isóbatas de:',
                 'alternativas': ['0 a 100 m',
                                  '5000 a 10000 m',
                                  '500 a 1000 m',
                                  '200 a 5000 m',
                                  '0 a 50 m'],
                 'correcta': 'D'},
                {'pregunta': 'Las fosas marinas se producen por:',
                 'alternativas': ['La erosión eólica',
                                  'Las corrientes marinas',
                                  'La subducción de la Placa de Nasca',
                                  'La sedimentación fluvial',
                                  'El afloramiento'],
                 'correcta': 'C'},
                {'pregunta': 'La Dorsal de Nasca es:',
                 'alternativas': ['Un golfo',
                                  'Una bahía',
                                  'Una fosa marina',
                                  'Una cordillera submarina volcánica',
                                  'Una península'],
                 'correcta': 'D'},
                {'pregunta': 'La Dorsal de Nasca se ubica aproximadamente a '
                             'qué distancia de la costa de Ica:',
                 'alternativas': ['500 km',
                                  '50 km',
                                  '10 km',
                                  '300 km',
                                  '150 km'],
                 'correcta': 'E'},
                {'pregunta': 'El fundamento geológico de la Tesis de las 200 '
                             'millas se refiere a:',
                 'alternativas': ['La seguridad nacional',
                                  'El turismo',
                                  'El comercio marítimo',
                                  'La riqueza pesquera',
                                  'La continuidad del zócalo continental'],
                 'correcta': 'E'},
                {'pregunta': 'La salinidad del mar en la región norte es de '
                             'aproximadamente:',
                 'alternativas': ['20 gr/l',
                                  '34 gr/l',
                                  '40 gr/l',
                                  '45 gr/l',
                                  '30 gr/l'],
                 'correcta': 'B'},
                {'pregunta': 'La alteración del fenómeno de afloramiento y '
                             'la desaparición de la capa de inversión '
                             'térmica son consecuencias de: (II CEPRU 2025)',
                 'alternativas': ['Las olas y mareas',
                                  'El fenómeno de El Niño',
                                  'La corriente de Humboldt',
                                  'La circumpolar Antártica',
                                  'El fenómeno de La Niña'],
                 'correcta': 'B'},
                {'pregunta': 'Un impacto negativo de la actividad pesquera '
                             'es: (II CEPRU 2024)',
                 'alternativas': ['Incremento de la economía',
                                  'Desarrollo sostenible',
                                  'La pesca selectiva',
                                  'La pesca controlada',
                                  'La pesca de arrastre'],
                 'correcta': 'E'},
                {'pregunta': 'El fundamento de la tesis de las 200 millas '
                             'marinas, que consiste en la continuidad del '
                             'zócalo continental, es de carácter: (II CEPRU '
                             '2022)',
                 'alternativas': ['Geográfico',
                                  'Jurídico',
                                  'Geológico',
                                  'Biológico',
                                  'Económico'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente peruana circula con una '
                             'dirección: (I CEPRU 2024)',
                 'alternativas': ['NW a SE',
                                  'SW a NE',
                                  'NW a SW',
                                  'SE a NW',
                                  'NE a SE'],
                 'correcta': 'D'},
                {'pregunta': 'La ausencia de la inversión térmica y la '
                             'alteración del fenómeno de afloramiento '
                             'costero son consecuencias del fenómeno de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['La corriente ecuatorial del sur',
                                  'El aguaje o pintor',
                                  'El Niño',
                                  'La Niña',
                                  'La corriente circumpolar antártica'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los fundamentos de la Tesis de las 200 '
                             'Millas Marítimas es: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['La presencia de riqueza ictiológica',
                                  'La presencia de fauna tropical',
                                  'El dominio marítimo y terrestre',
                                  'La seguridad territorial',
                                  'El enfriamiento del mar'],
                 'correcta': 'A'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['El mar peruano se extiende, en distancia, '
                                'hasta 200 millas.',
                                'La extensión del mar peruano representa del '
                                'territorio peruano aproximadamente 90%.',
                                'Tras el fallo de la Corte de La Haya, el '
                                'Perú obtuvo adicionalmente 50 284 km².',
                                'El mar peruano se distingue de otros por la '
                                'presencia de La Corriente Peruana y la '
                                'frialdad de sus aguas.',
                                'La doctrina de las 200 millas fue '
                                'proclamada por Perú junto con Ecuador y '
                                'Chile.',
                                'La tesis de las 200 millas se declaró '
                                'mediante el D.S. N° 781 en el gobierno de '
                                'José Bustamante y Rivero.',
                                'La tesis de las 200 millas se proclamó en '
                                'el año 1947.',
                                'La región norte del mar peruano se extiende '
                                'desde la Península de Illescas hasta Boca '
                                'de Capones.',
                                'El color del mar en la región norte se debe '
                                'principalmente a La descarga de los ríos.',
                                'La temperatura promedio del mar en la '
                                'región central y sur es de 18°C.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La atmósfera nos protege principalmente de {Los '
                           'rayos ultravioleta y meteoritos}.',
                           'El gas más abundante de la atmósfera es '
                           '{Nitrógeno}.',
                           'El segundo gas más abundante de la atmósfera es '
                           '{Oxígeno}.',
                           'La capa inferior de la atmósfera, donde ocurren '
                           'los fenómenos meteorológicos, es {La '
                           'tropósfera}.',
                           'La altitud promedio de la tropósfera es de {12,5 '
                           'km}.',
                           'En la tropósfera, la temperatura disminuye 0,6°C '
                           'cada {100 m}.',
                           'El fenómeno de disminución de temperatura con la '
                           'altitud en la tropósfera se llama {Gradiente '
                           'Térmico Vertical}.',
                           'La capa de ozono se ubica dentro de la '
                           '{Estratósfera}.',
                           'La capa de ozono se ubica entre los {24 y 30 '
                           'km}.',
                           'La función principal de la capa de ozono es '
                           '{Impedir el paso de los rayos ultravioleta}.',
                           'En la estratósfera, la temperatura {Aumenta '
                           'progresivamente}.',
                           'La mesósfera se extiende entre {50 y 90 km}.',
                           'En la mesósfera, la temperatura puede llegar '
                           'hasta {-110°C}.',
                           'La termósfera o ionósfera se localiza entre {90 '
                           'y 500 km}.',
                           'En la termósfera, la temperatura puede llegar '
                           'hasta {800°C a 1500°C}.',
                           'Las auroras polares se producen en {La '
                           'termósfera}.',
                           'Los elementos de la termósfera se encuentran '
                           '{Ionizados o electrizados}.',
                           'Entre los gases de efecto invernadero figura '
                           'principalmente {El CO2}.',
                           'Sin la atmósfera, el paisaje terrestre sería '
                           'similar al de {La Luna}.',
                           'El límite final de la tropósfera se llama '
                           '{Tropopausa}.']}],
  'cuadros': [{'titulo': '10.2-10.4 CAPAS DE LA ATMÓSFERA',
               'encabezados': ['Capa', 'Altitud'],
               'filas': [['{Tropósfera}', 'Hasta 12,5 km'],
                         ['{Estratósfera}', '12,5 a 50 km'],
                         ['{Mesósfera}', '50 a 90 km'],
                         ['{Termósfera}', '90 a 500 km']]}],
  'preguntas': [{'pregunta': 'La atmósfera nos protege principalmente de:',
                 'alternativas': ['La erosión',
                                  'La lluvia ácida',
                                  'Los rayos ultravioleta y meteoritos',
                                  'Las mareas',
                                  'Los sismos'],
                 'correcta': 'C'},
                {'pregunta': 'El gas más abundante de la atmósfera es:',
                 'alternativas': ['Ozono',
                                  'Oxígeno',
                                  'Argón',
                                  'Dióxido de carbono',
                                  'Nitrógeno'],
                 'correcta': 'E'},
                {'pregunta': 'El segundo gas más abundante de la atmósfera '
                             'es:',
                 'alternativas': ['Neón',
                                  'Oxígeno',
                                  'Helio',
                                  'Nitrógeno',
                                  'Argón'],
                 'correcta': 'B'},
                {'pregunta': 'La capa inferior de la atmósfera, donde '
                             'ocurren los fenómenos meteorológicos, es:',
                 'alternativas': ['La tropósfera',
                                  'La mesósfera',
                                  'La ionósfera',
                                  'La estratósfera',
                                  'La termósfera'],
                 'correcta': 'A'},
                {'pregunta': 'La altitud promedio de la tropósfera es de:',
                 'alternativas': ['12,5 km',
                                  '100 km',
                                  '50 km',
                                  '90 km',
                                  '5 km'],
                 'correcta': 'A'},
                {'pregunta': 'En la tropósfera, la temperatura disminuye '
                             '0,6°C cada:',
                 'alternativas': ['100 m', '500 m', '10 m', '1000 m', '50 m'],
                 'correcta': 'A'},
                {'pregunta': 'El fenómeno de disminución de temperatura con '
                             'la altitud en la tropósfera se llama:',
                 'alternativas': ['Efecto invernadero',
                                  'Corriente de chorro',
                                  'Inversión térmica',
                                  'Gradiente Térmico Vertical',
                                  'Capa de ozono'],
                 'correcta': 'D'},
                {'pregunta': 'La capa de ozono se ubica dentro de la:',
                 'alternativas': ['Estratósfera',
                                  'Exósfera',
                                  'Termósfera',
                                  'Tropósfera',
                                  'Mesósfera'],
                 'correcta': 'A'},
                {'pregunta': 'La capa de ozono se ubica entre los:',
                 'alternativas': ['90 y 500 km',
                                  '50 y 90 km',
                                  '0 y 10 km',
                                  '10 y 20 km',
                                  '24 y 30 km'],
                 'correcta': 'E'},
                {'pregunta': 'La función principal de la capa de ozono es:',
                 'alternativas': ['Formar nubes',
                                  'Impedir el paso de los rayos ultravioleta',
                                  'Producir lluvia',
                                  'Regular la humedad',
                                  'Generar viento'],
                 'correcta': 'B'},
                {'pregunta': 'En la estratósfera, la temperatura:',
                 'alternativas': ['Se mantiene igual',
                                  'Fluctúa sin patrón',
                                  'Disminuye constantemente',
                                  'Aumenta progresivamente',
                                  'Baja a cero'],
                 'correcta': 'D'},
                {'pregunta': 'La mesósfera se extiende entre:',
                 'alternativas': ['0 y 12,5 km',
                                  '500 y 1000 km',
                                  '90 y 500 km',
                                  '50 y 90 km',
                                  '12,5 y 50 km'],
                 'correcta': 'D'},
                {'pregunta': 'En la mesósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['-110°C', '-50°C', '50°C', '0°C', '100°C'],
                 'correcta': 'A'},
                {'pregunta': 'La termósfera o ionósfera se localiza entre:',
                 'alternativas': ['90 y 500 km',
                                  '12,5 y 50 km',
                                  '50 y 90 km',
                                  '500 y 1000 km',
                                  '0 y 12,5 km'],
                 'correcta': 'A'},
                {'pregunta': 'En la termósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['300°C',
                                  '0°C',
                                  '800°C a 1500°C',
                                  '-100°C',
                                  '100°C'],
                 'correcta': 'C'},
                {'pregunta': 'Las auroras polares se producen en:',
                 'alternativas': ['La capa de ozono',
                                  'La tropósfera',
                                  'La termósfera',
                                  'La mesósfera',
                                  'La estratósfera'],
                 'correcta': 'C'},
                {'pregunta': 'Los elementos de la termósfera se encuentran:',
                 'alternativas': ['Sólidos',
                                  'Inertes',
                                  'Congelados',
                                  'Líquidos',
                                  'Ionizados o electrizados'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los gases de efecto invernadero figura '
                             'principalmente:',
                 'alternativas': ['El nitrógeno',
                                  'El CO2',
                                  'El neón',
                                  'El helio',
                                  'El argón'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la atmósfera, el paisaje terrestre sería '
                             'similar al de:',
                 'alternativas': ['Saturno',
                                  'Júpiter',
                                  'La Luna',
                                  'Marte',
                                  'Venus'],
                 'correcta': 'C'},
                {'pregunta': 'El límite final de la tropósfera se llama:',
                 'alternativas': ['Mesopausa',
                                  'Ionopausa',
                                  'Tropopausa',
                                  'Termopausa',
                                  'Estratopausa'],
                 'correcta': 'C'},
                {'pregunta': 'La mayor cantidad de climas en el Perú está '
                             'determinada por el factor: (II CEPRU 2025)',
                 'alternativas': ['Corrientes marinas',
                                  'Vegetación',
                                  'Altitud',
                                  'Anticiclón del Pacífico Sur',
                                  'Latitud'],
                 'correcta': 'C'},
                {'pregunta': 'Los registros de los fenómenos meteorológicos '
                             'sirven para pronosticar: (I CEPRU 2025)',
                 'alternativas': ['Cambio climático',
                                  'Variabilidad climática',
                                  'Tiempo meteorológico',
                                  'Tiempo cronológico',
                                  'Calentamiento global'],
                 'correcta': 'C'},
                {'pregunta': 'Las auroras polares se producen en la capa '
                             'atmosférica de la: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Estratosfera',
                                  'Ionosfera',
                                  'Mesosfera',
                                  'Troposfera',
                                  'Termosfera exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Corresponde a la Tropósfera: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Se producen los fenómenos meteorológicos',
                                  'Tiene una subcapa llamada Ozonósfera',
                                  'Es una zona de radiación cósmica',
                                  'Alcanza hasta la termopausa',
                                  'Existen los cinturones de radiación de '
                                  'Van Allen'],
                 'correcta': 'A'},
                {'pregunta': 'El instrumento que mide la intensidad de los '
                             'vientos es el: (Primera Oportunidad UNSAAC '
                             '2020)',
                 'alternativas': ['Veleta',
                                  'Termómetro',
                                  'Barómetro',
                                  'Pluviómetro',
                                  'Anemómetro'],
                 'correcta': 'E'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['La atmósfera nos protege principalmente de '
                                'Los rayos ultravioleta y meteoritos.',
                                'El gas más abundante de la atmósfera es '
                                'Nitrógeno.',
                                'El segundo gas más abundante de la '
                                'atmósfera es Oxígeno.',
                                'La capa inferior de la atmósfera, donde '
                                'ocurren los fenómenos meteorológicos, es La '
                                'tropósfera.',
                                'La altitud promedio de la tropósfera es de '
                                '12,5 km.',
                                'En la tropósfera, la temperatura disminuye '
                                '0,6°C cada 100 m.',
                                'El fenómeno de disminución de temperatura '
                                'con la altitud en la tropósfera se llama '
                                'Gradiente Térmico Vertical.',
                                'La capa de ozono se ubica dentro de la '
                                'Estratósfera.',
                                'La capa de ozono se ubica entre los 24 y 30 '
                                'km.',
                                'La función principal de la capa de ozono es '
                                'Impedir el paso de los rayos '
                                'ultravioleta.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los recursos naturales son elementos que {Ofrece '
                           'la naturaleza espontáneamente}.',
                           'Los recursos que se agotan con el '
                           'aprovechamiento del hombre son los {No '
                           'renovables}.',
                           'El petróleo y el gas son recursos naturales {No '
                           'renovables}.',
                           'El agua, el aire y el suelo son recursos '
                           'naturales {Renovables}.',
                           'Cuando el hombre aprovecha un recurso natural, '
                           'este se convierte en {Recurso económico}.',
                           'Entre las aves guaneras del mar peruano figuran '
                           'el guanay, piquero y {Alcatraz}.',
                           'El hierro se explota principalmente en la '
                           'localidad de {Marcona}.',
                           'Los fosfatos como fertilizante se explotan en '
                           '{Bayóvar, Piura}.',
                           'Entre los minerales de la región andina figuran '
                           'el cobre, plomo, zinc, oro y {Plata}.',
                           'La vicuña, el cóndor y la chinchilla son fauna '
                           'representativa de {La región andina}.',
                           'De la selva se obtiene, entre otros recursos, '
                           'oro {Aluvial}.',
                           'El SERNANP está adscrito al Ministerio de '
                           '{Ambiente}.',
                           'El SERNANP fue creado mediante el Decreto '
                           'Legislativo {1013}.',
                           'El SERNANP fue creado en el año {2008}.',
                           'Las Áreas Naturales Protegidas representan del '
                           'territorio nacional {15,41%}.',
                           'En los Parques Nacionales solo se permite {El '
                           'turismo e investigación científica}.',
                           'El parque nacional más pequeño y antiguo del '
                           'Perú es {Cutervo}.',
                           'El parque nacional más extenso del Perú es '
                           '{Manu}.',
                           'El parque nacional Manu se ubica entre Cusco y '
                           '{Madre de Dios}.',
                           'El Parque Nacional Huascarán se ubica en el '
                           'departamento de {Áncash}.']}],
  'cuadros': [{'titulo': '11.1 TIPOS DE RECURSOS NATURALES',
               'encabezados': ['Tipo', 'Se agotan', 'Ejemplos'],
               'filas': [['{No renovables}',
                          '{Sí}',
                          'Minerales, petróleo, gas'],
                         ['{Renovables}',
                          '{No}',
                          'Agua, aire, suelo, flora, fauna']]}],
  'preguntas': [{'pregunta': 'Los recursos naturales son elementos que:',
                 'alternativas': ['Crea el hombre artificialmente',
                                  'Son producidos por la industria',
                                  'Ofrece la naturaleza espontáneamente',
                                  'Solo existen en la costa',
                                  'Provienen únicamente del mar'],
                 'correcta': 'C'},
                {'pregunta': 'Los recursos que se agotan con el '
                             'aprovechamiento del hombre son los:',
                 'alternativas': ['Renovables',
                                  'Marinos',
                                  'No renovables',
                                  'Forestales',
                                  'Hídricos'],
                 'correcta': 'C'},
                {'pregunta': 'El petróleo y el gas son recursos naturales:',
                 'alternativas': ['No renovables',
                                  'Ilimitados',
                                  'Inagotables',
                                  'Renovables',
                                  'Reciclables'],
                 'correcta': 'A'},
                {'pregunta': 'El agua, el aire y el suelo son recursos '
                             'naturales:',
                 'alternativas': ['Artificiales',
                                  'Escasos',
                                  'No renovables',
                                  'Renovables',
                                  'Prohibidos'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando el hombre aprovecha un recurso natural, '
                             'este se convierte en:',
                 'alternativas': ['Bien público exclusivo',
                                  'Elemento sin valor',
                                  'Patrimonio intangible',
                                  'Recurso prohibido',
                                  'Recurso económico'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las aves guaneras del mar peruano '
                             'figuran el guanay, piquero y:',
                 'alternativas': ['Cóndor',
                                  'Gaviota andina',
                                  'Águila',
                                  'Zorzal',
                                  'Alcatraz'],
                 'correcta': 'E'},
                {'pregunta': 'El hierro se explota principalmente en la '
                             'localidad de:',
                 'alternativas': ['Toquepala',
                                  'Bayóvar',
                                  'Marcona',
                                  'Cerro de Pasco',
                                  'Cajamarca'],
                 'correcta': 'C'},
                {'pregunta': 'Los fosfatos como fertilizante se explotan en:',
                 'alternativas': ['Marcona',
                                  'Arequipa',
                                  'Puno',
                                  'Cusco',
                                  'Bayóvar, Piura'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los minerales de la región andina '
                             'figuran el cobre, plomo, zinc, oro y:',
                 'alternativas': ['Sal',
                                  'Petróleo',
                                  'Gas natural',
                                  'Carbón vegetal',
                                  'Plata'],
                 'correcta': 'E'},
                {'pregunta': 'La vicuña, el cóndor y la chinchilla son fauna '
                             'representativa de:',
                 'alternativas': ['La región andina',
                                  'La selva alta',
                                  'La selva baja',
                                  'El mar peruano',
                                  'La costa'],
                 'correcta': 'A'},
                {'pregunta': 'De la selva se obtiene, entre otros recursos, '
                             'oro:',
                 'alternativas': ['Importado',
                                  'Sintético',
                                  'Aluvial',
                                  'Solo en laboratorio',
                                  'En vetas superficiales'],
                 'correcta': 'C'},
                {'pregunta': 'El SERNANP está adscrito al Ministerio de:',
                 'alternativas': ['Ambiente',
                                  'Energía y Minas',
                                  'Educación',
                                  'Agricultura',
                                  'Cultura'],
                 'correcta': 'A'},
                {'pregunta': 'El SERNANP fue creado mediante el Decreto '
                             'Legislativo:',
                 'alternativas': ['997', '1090', '1013', '850', '713'],
                 'correcta': 'C'},
                {'pregunta': 'El SERNANP fue creado en el año:',
                 'alternativas': ['1998', '2008', '1990', '2020', '2015'],
                 'correcta': 'B'},
                {'pregunta': 'Las Áreas Naturales Protegidas representan del '
                             'territorio nacional:',
                 'alternativas': ['2%', '50%', '30%', '15,41%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'En los Parques Nacionales solo se permite:',
                 'alternativas': ['El turismo e investigación científica',
                                  'La caza deportiva',
                                  'La ganadería extensiva',
                                  'La minería y agricultura',
                                  'La tala de árboles'],
                 'correcta': 'A'},
                {'pregunta': 'El parque nacional más pequeño y antiguo del '
                             'Perú es:',
                 'alternativas': ['Huascarán',
                                  'Bahuaja Sonene',
                                  'Manu',
                                  'Cutervo',
                                  'Tingo María'],
                 'correcta': 'D'},
                {'pregunta': 'El parque nacional más extenso del Perú es:',
                 'alternativas': ['Cutervo',
                                  'Huascarán',
                                  'Cerros de Amotape',
                                  'Río Abiseo',
                                  'Manu'],
                 'correcta': 'E'},
                {'pregunta': 'El parque nacional Manu se ubica entre Cusco '
                             'y:',
                 'alternativas': ['Apurímac',
                                  'Madre de Dios',
                                  'Arequipa',
                                  'Ayacucho',
                                  'Puno'],
                 'correcta': 'B'},
                {'pregunta': 'El Parque Nacional Huascarán se ubica en el '
                             'departamento de:',
                 'alternativas': ['Puno',
                                  'Cusco',
                                  'Cajamarca',
                                  'Áncash',
                                  'Lima'],
                 'correcta': 'D'},
                {'pregunta': 'Satisfacer las necesidades del presente sin '
                             'comprometer los recursos de las futuras '
                             'generaciones corresponde al concepto de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['Contaminación ambiental',
                                  'Desastre ecológico',
                                  'Riesgo de desastre',
                                  'Desarrollo sostenible',
                                  'Impacto ambiental'],
                 'correcta': 'D'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['Los recursos naturales son elementos que '
                                'Ofrece la naturaleza espontáneamente.',
                                'Los recursos que se agotan con el '
                                'aprovechamiento del hombre son los No '
                                'renovables.',
                                'El petróleo y el gas son recursos naturales '
                                'No renovables.',
                                'El agua, el aire y el suelo son recursos '
                                'naturales Renovables.',
                                'Cuando el hombre aprovecha un recurso '
                                'natural, este se convierte en Recurso '
                                'económico.',
                                'Entre las aves guaneras del mar peruano '
                                'figuran el guanay, piquero y Alcatraz.',
                                'El hierro se explota principalmente en la '
                                'localidad de Marcona.',
                                'Los fosfatos como fertilizante se explotan '
                                'en Bayóvar, Piura.',
                                'Entre los minerales de la región andina '
                                'figuran el cobre, plomo, zinc, oro y Plata.',
                                'La vicuña, el cóndor y la chinchilla son '
                                'fauna representativa de La región '
                                'andina.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El SINAGERD fue creado mediante la Ley N° '
                           '{29664}.',
                           'El SINAGERD se caracteriza por ser un sistema '
                           '{Interinstitucional, descentralizado y '
                           'participativo}.',
                           'La Política Nacional de Gestión del Riesgo de '
                           'Desastres fue aprobada mediante {El Decreto '
                           'Supremo N° 111-2012-PCM}.',
                           'Un fenómeno natural que ocurre en una zona '
                           'despoblada {No representa necesariamente una '
                           'amenaza}.',
                           'Un desastre se produce cuando {Se altera '
                           'intensamente la vida cotidiana de una '
                           'comunidad}.',
                           'El riesgo se calcula mediante la fórmula '
                           '{Amenaza × Vulnerabilidad}.',
                           'Para que exista riesgo se requiere la presencia '
                           'de {Amenaza y vulnerabilidad juntas}.',
                           'La amenaza se define como la probabilidad de que '
                           'ocurra {Un fenómeno que pueda poner en peligro a '
                           'las personas}.',
                           'Las amenazas naturales se originan por {La '
                           'naturaleza misma}.',
                           'La vulnerabilidad depende, entre otros factores, '
                           'de {La ubicación y tipo de vivienda}.',
                           'Entre los objetivos de la política nacional de '
                           'gestión del riesgo figura {Fortalecer la cultura '
                           'de prevención}.',
                           'Un terremoto en un área no poblada es un ejemplo '
                           'de {Fenómeno natural sin amenaza directa}.',
                           'El riesgo representa la proximidad de {Un daño '
                           'potencial}.',
                           'Sin vulnerabilidad, una amenaza {No representa '
                           'un riesgo por sí sola}.',
                           'El SINAGERD busca capacitar a los componentes '
                           'del sistema para {La toma de decisiones}.',
                           'Los fenómenos naturales pueden ser de orden '
                           'climatológico, hidrológico o {Geológico}.',
                           'El SINAGERD tiene un carácter, entre otros, '
                           'transversal y {Participativo}.',
                           'El cálculo del riesgo puede incluir el número de '
                           '{Posibles vidas expuestas y viviendas que pueden '
                           'perderse}.',
                           'Una inundación en un lugar deshabitado se '
                           'considera {Un fenómeno natural, no una amenaza '
                           'directa}.',
                           'La gestión del riesgo de desastres busca '
                           'minimizar los efectos adversos sobre {La '
                           'población, la economía y el ambiente}.']}],
  'cuadros': [{'titulo': '12.2 FÓRMULA DEL RIESGO',
               'encabezados': ['Elemento', 'Definición'],
               'filas': [['{Riesgo}', '{Amenaza} × Vulnerabilidad'],
                         ['{Amenaza}',
                          'Probabilidad de un fenómeno {dañino}'],
                         ['{Vulnerabilidad}',
                          'Susceptibilidad de sufrir {daño}']]}],
  'preguntas': [{'pregunta': 'El SINAGERD fue creado mediante la Ley N°:',
                 'alternativas': ['27444',
                                  '29338',
                                  '29664',
                                  '28044',
                                  '30220'],
                 'correcta': 'C'},
                {'pregunta': 'El SINAGERD se caracteriza por ser un sistema:',
                 'alternativas': ['Solo consultivo',
                                  'Interinstitucional, descentralizado y '
                                  'participativo',
                                  'Exclusivamente militar',
                                  'Centralizado y vertical',
                                  'Sin participación ciudadana'],
                 'correcta': 'B'},
                {'pregunta': 'La Política Nacional de Gestión del Riesgo de '
                             'Desastres fue aprobada mediante:',
                 'alternativas': ['Un decreto legislativo',
                                  'Una resolución ministerial',
                                  'Una ley del Congreso',
                                  'El Decreto Supremo N° 111-2012-PCM',
                                  'Una ordenanza municipal'],
                 'correcta': 'D'},
                {'pregunta': 'Un fenómeno natural que ocurre en una zona '
                             'despoblada:',
                 'alternativas': ['Se clasifica como vulnerabilidad',
                                  'Siempre es un desastre',
                                  'No representa necesariamente una amenaza',
                                  'Requiere evacuación inmediata',
                                  'Es automáticamente un riesgo alto'],
                 'correcta': 'C'},
                {'pregunta': 'Un desastre se produce cuando:',
                 'alternativas': ['Ocurre un fenómeno en zona despoblada',
                                  'No hay ningún efecto adverso',
                                  'Solo hay pérdidas económicas menores',
                                  'El fenómeno es predecible',
                                  'Se altera intensamente la vida cotidiana '
                                  'de una comunidad'],
                 'correcta': 'E'},
                {'pregunta': 'El riesgo se calcula mediante la fórmula:',
                 'alternativas': ['Amenaza − Vulnerabilidad',
                                  'Amenaza + Vulnerabilidad',
                                  'Vulnerabilidad ÷ Amenaza',
                                  'Amenaza ÷ Vulnerabilidad',
                                  'Amenaza × Vulnerabilidad'],
                 'correcta': 'E'},
                {'pregunta': 'Para que exista riesgo se requiere la '
                             'presencia de:',
                 'alternativas': ['Solo fenómenos naturales extremos',
                                  'Solo la amenaza',
                                  'Solo la vulnerabilidad',
                                  'Ningún factor en particular',
                                  'Amenaza y vulnerabilidad juntas'],
                 'correcta': 'E'},
                {'pregunta': 'La amenaza se define como la probabilidad de '
                             'que ocurra:',
                 'alternativas': ['Un desastre ya consumado',
                                  'Una vulnerabilidad social',
                                  'Un fenómeno que pueda poner en peligro a '
                                  'las personas',
                                  'Una política pública',
                                  'Un cambio climático'],
                 'correcta': 'C'},
                {'pregunta': 'Las amenazas naturales se originan por:',
                 'alternativas': ['El comercio internacional',
                                  'La naturaleza misma',
                                  'Decisiones políticas',
                                  'Fallas de infraestructura',
                                  'Acción humana exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La vulnerabilidad depende, entre otros '
                             'factores, de:',
                 'alternativas': ['La ubicación y tipo de vivienda',
                                  'Solo la economía nacional',
                                  'Solo el idioma',
                                  'Solo la edad de la población',
                                  'Solo el clima'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los objetivos de la política nacional de '
                             'gestión del riesgo figura:',
                 'alternativas': ['Eliminar los fenómenos naturales',
                                  'Aumentar la vulnerabilidad',
                                  'Fortalecer la cultura de prevención',
                                  'Evitar toda construcción',
                                  'Prohibir la habitación en zonas de '
                                  'riesgo'],
                 'correcta': 'C'},
                {'pregunta': 'Un terremoto en un área no poblada es un '
                             'ejemplo de:',
                 'alternativas': ['Riesgo alto',
                                  'Catástrofe social',
                                  'Desastre',
                                  'Fenómeno natural sin amenaza directa',
                                  'Vulnerabilidad extrema'],
                 'correcta': 'D'},
                {'pregunta': 'El riesgo representa la proximidad de:',
                 'alternativas': ['Una política pública exitosa',
                                  'Una mejora económica',
                                  'Un daño potencial',
                                  'Un fenómeno inexistente',
                                  'Un evento positivo'],
                 'correcta': 'C'},
                {'pregunta': 'Sin vulnerabilidad, una amenaza:',
                 'alternativas': ['Es imposible de medir',
                                  'Aumenta exponencialmente',
                                  'Se convierte en catástrofe automática',
                                  'No representa un riesgo por sí sola',
                                  'Genera un desastre igual'],
                 'correcta': 'D'},
                {'pregunta': 'El SINAGERD busca capacitar a los componentes '
                             'del sistema para:',
                 'alternativas': ['Evitar toda capacitación',
                                  'Eliminar la participación privada',
                                  'La toma de decisiones',
                                  'Centralizar el poder',
                                  'Reducir el presupuesto público'],
                 'correcta': 'C'},
                {'pregunta': 'Los fenómenos naturales pueden ser de orden '
                             'climatológico, hidrológico o:',
                 'alternativas': ['Educativo',
                                  'Comercial',
                                  'Cultural',
                                  'Económico',
                                  'Geológico'],
                 'correcta': 'E'},
                {'pregunta': 'El SINAGERD tiene un carácter, entre otros, '
                             'transversal y:',
                 'alternativas': ['Exclusivo',
                                  'Unipersonal',
                                  'Temporal',
                                  'Participativo',
                                  'Cerrado'],
                 'correcta': 'D'},
                {'pregunta': 'El cálculo del riesgo puede incluir el número '
                             'de:',
                 'alternativas': ['Solo turistas en la zona',
                                  'Solo empresas afectadas',
                                  'Posibles vidas expuestas y viviendas que '
                                  'pueden perderse',
                                  'Solo vehículos en circulación',
                                  'Solo funcionarios públicos'],
                 'correcta': 'C'},
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
                 'alternativas': ['Calamidad',
                                  'Plaga',
                                  'Epidemia',
                                  'Endemia',
                                  'Pandemia'],
                 'correcta': 'C'},
                {'pregunta': 'La autoridad que preside el Comité de Defensa '
                             'Civil Regional es: (II CEPRU 2024)',
                 'alternativas': ['Consejo Regional',
                                  'Alcalde Provincial',
                                  'Gobernador Regional',
                                  'Teniente Alcalde',
                                  'Concejo Municipal'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'EL SINAGERD',
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
                                'figura fortalecer la cultura de '
                                'prevención.']},
                     {'titulo': 'CONCEPTOS BÁSICOS: FENÓMENO, DESASTRE Y '
                                'RIESGO',
                      'items': ['Un fenómeno natural es una manifestación '
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
                     {'titulo': 'AMENAZA Y VULNERABILIDAD',
                      'items': ['La amenaza es la probabilidad de que ocurra '
                                'un fenómeno natural o causado por el hombre '
                                'que puede poner en peligro a un grupo de '
                                'personas.',
                                'Las amenazas naturales son las originadas '
                                'por la naturaleza misma, como los '
                                'movimientos sísmicos.',
                                'La vulnerabilidad depende, entre otros '
                                'factores, de la ubicación de la vivienda y '
                                'la organización de la población.']},
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['El SINAGERD fue creado mediante la Ley N° '
                                '29664.',
                                'El SINAGERD se caracteriza por ser un '
                                'sistema Interinstitucional, descentralizado '
                                'y participativo.',
                                'La Política Nacional de Gestión del Riesgo '
                                'de Desastres fue aprobada mediante El '
                                'Decreto Supremo N° 111-2012-PCM.',
                                'Un fenómeno natural que ocurre en una zona '
                                'despoblada No representa necesariamente una '
                                'amenaza.',
                                'Un desastre se produce cuando Se altera '
                                'intensamente la vida cotidiana de una '
                                'comunidad.',
                                'El riesgo se calcula mediante la fórmula '
                                'Amenaza × Vulnerabilidad.',
                                'Para que exista riesgo se requiere la '
                                'presencia de Amenaza y vulnerabilidad '
                                'juntas.',
                                'La amenaza se define como la probabilidad '
                                'de que ocurra Un fenómeno que pueda poner '
                                'en peligro a las personas.',
                                'Las amenazas naturales se originan por La '
                                'naturaleza misma.',
                                'La vulnerabilidad depende, entre otros '
                                'factores, de La ubicación y tipo de '
                                'vivienda.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La disciplina que estudia la distribución de la '
                           'población en un área geográfica es {La '
                           'demogeografía}.',
                           'La demografía estudia estadísticamente la '
                           'estructura y dinámica de {Las poblaciones '
                           'humanas}.',
                           'La tasa de natalidad en el Perú es '
                           'aproximadamente de {23,3‰}.',
                           'La tasa de mortalidad en el Perú es '
                           'aproximadamente de {6,2‰}.',
                           'La tasa de crecimiento poblacional considera '
                           'nacimientos, muertes y {La migración}.',
                           'Según el INEI, la población del Perú al 2017 '
                           'superaba {31 237 385 habitantes}.',
                           'El organismo central y rector del Sistema '
                           'Estadístico Nacional del Perú es {El INEI}.',
                           'El INEI depende directamente de {El Presidente '
                           'del Consejo de Ministros}.',
                           'El antecesor del INEI, creado en 1969, se llamó '
                           '{ONEC}.',
                           'La población peruana se caracteriza por ser '
                           '{Heterogénea, multirracial y multicultural}.',
                           'La población peruana se concentra mayormente en '
                           '{La costa y zonas urbanas}.',
                           'La población nominal es {El número total de '
                           'habitantes censados}.',
                           'La población que no se halla físicamente durante '
                           'el censo se llama {Población omitida}.',
                           'La población absoluta es {La cantidad total de '
                           'habitantes de una unidad geográfica}.',
                           'La densidad de población también se llama '
                           '{Población relativa}.',
                           'La fórmula de la población relativa es '
                           '{Población absoluta entre extensión '
                           'territorial}.',
                           'Según el censo de 1940, la población del Perú '
                           'era de {7 023 111}.',
                           'Según el censo de 2007, la población del Perú '
                           'era de {28 220 764}.',
                           'La densidad poblacional del Perú en 2017 era '
                           'aproximadamente de {24,3 hab/km²}.',
                           'La esperanza de vida en el Perú, según el censo '
                           'de 2007, fue de {71,2 años}.']}],
  'cuadros': [{'titulo': '13.2 POBLACIÓN DEL PERÚ POR CENSOS',
               'encabezados': ['Año', 'Población', 'Densidad hab/km²'],
               'filas': [['{1940}', '7 023 111', '5,5'],
                         ['1961', '10 420 357', '{8,1}'],
                         ['1993', '{22 639 443}', '17,6'],
                         ['2007', '28 220 764', '{22,0}'],
                         ['{2017}', '31 237 385', '24,3']]}],
  'preguntas': [{'pregunta': 'La disciplina que estudia la distribución de '
                             'la población en un área geográfica es:',
                 'alternativas': ['La cartografía',
                                  'La demogeografía',
                                  'La demografía',
                                  'La geopolítica',
                                  'La estadística'],
                 'correcta': 'B'},
                {'pregunta': 'La demografía estudia estadísticamente la '
                             'estructura y dinámica de:',
                 'alternativas': ['Las poblaciones humanas',
                                  'El relieve terrestre',
                                  'Las corrientes marinas',
                                  'Los climas',
                                  'Los ecosistemas'],
                 'correcta': 'A'},
                {'pregunta': 'La tasa de natalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['6,2‰', '10‰', '1‰', '50‰', '23,3‰'],
                 'correcta': 'E'},
                {'pregunta': 'La tasa de mortalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['23,3‰', '6,2‰', '30‰', '15‰', '2‰'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de crecimiento poblacional considera '
                             'nacimientos, muertes y:',
                 'alternativas': ['La economía',
                                  'El idioma',
                                  'La religión',
                                  'La migración',
                                  'El clima'],
                 'correcta': 'D'},
                {'pregunta': 'Según el INEI, la población del Perú al 2017 '
                             'superaba:',
                 'alternativas': ['40 millones',
                                  '31 237 385 habitantes',
                                  '20 millones',
                                  '50 millones',
                                  '10 millones'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo central y rector del Sistema '
                             'Estadístico Nacional del Perú es:',
                 'alternativas': ['El INEI',
                                  'El MINEDU',
                                  'El MEF',
                                  'La SUNAT',
                                  'El BCRP'],
                 'correcta': 'A'},
                {'pregunta': 'El INEI depende directamente de:',
                 'alternativas': ['La Presidencia de la República '
                                  'directamente',
                                  'El Poder Judicial',
                                  'El Ministerio de Economía',
                                  'El Congreso',
                                  'El Presidente del Consejo de Ministros'],
                 'correcta': 'E'},
                {'pregunta': 'El antecesor del INEI, creado en 1969, se '
                             'llamó:',
                 'alternativas': ['INE', 'ONEC', 'SUNAT', 'MEF', 'BCRP'],
                 'correcta': 'B'},
                {'pregunta': 'La población peruana se caracteriza por ser:',
                 'alternativas': ['Exclusivamente andina',
                                  'Sin diversidad lingüística',
                                  'Heterogénea, multirracial y multicultural',
                                  'Solo urbana',
                                  'Homogénea y monocultural'],
                 'correcta': 'C'},
                {'pregunta': 'La población peruana se concentra mayormente '
                             'en:',
                 'alternativas': ['Zonas fronterizas',
                                  'La costa y zonas urbanas',
                                  'La sierra',
                                  'Zonas rurales exclusivamente',
                                  'La selva'],
                 'correcta': 'B'},
                {'pregunta': 'La población nominal es:',
                 'alternativas': ['La estimada por proyección',
                                  'La población futura',
                                  'Solo la población urbana',
                                  'El número total de habitantes censados',
                                  'Solo la población rural'],
                 'correcta': 'D'},
                {'pregunta': 'La población que no se halla físicamente '
                             'durante el censo se llama:',
                 'alternativas': ['Población nominal',
                                  'Población omitida',
                                  'Población absoluta',
                                  'Población relativa',
                                  'Población flotante'],
                 'correcta': 'B'},
                {'pregunta': 'La población absoluta es:',
                 'alternativas': ['Un promedio estimado',
                                  'Solo la tasa de crecimiento',
                                  'La cantidad total de habitantes de una '
                                  'unidad geográfica',
                                  'Solo la densidad',
                                  'Solo un porcentaje'],
                 'correcta': 'C'},
                {'pregunta': 'La densidad de población también se llama:',
                 'alternativas': ['Población relativa',
                                  'Población flotante',
                                  'Población omitida',
                                  'Población nominal',
                                  'Población censada'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula de la población relativa es:',
                 'alternativas': ['Tasa de natalidad menos mortalidad',
                                  'Población absoluta entre extensión '
                                  'territorial',
                                  'Población nominal más omitida',
                                  'Extensión territorial entre población '
                                  'absoluta',
                                  'Población absoluta × extensión '
                                  'territorial'],
                 'correcta': 'B'},
                {'pregunta': 'Según el censo de 1940, la población del Perú '
                             'era de:',
                 'alternativas': ['7 023 111',
                                  '28 220 764',
                                  '22 639 443',
                                  '14 121 564',
                                  '10 420 357'],
                 'correcta': 'A'},
                {'pregunta': 'Según el censo de 2007, la población del Perú '
                             'era de:',
                 'alternativas': ['14 121 564',
                                  '28 220 764',
                                  '17 762 231',
                                  '31 237 385',
                                  '22 639 443'],
                 'correcta': 'B'},
                {'pregunta': 'La densidad poblacional del Perú en 2017 era '
                             'aproximadamente de:',
                 'alternativas': ['50 hab/km²',
                                  '5 hab/km²',
                                  '100 hab/km²',
                                  '24,3 hab/km²',
                                  '10 hab/km²'],
                 'correcta': 'D'},
                {'pregunta': 'La esperanza de vida en el Perú, según el '
                             'censo de 2007, fue de:',
                 'alternativas': ['80 años',
                                  '55 años',
                                  '65 años',
                                  '35,6 años',
                                  '71,2 años'],
                 'correcta': 'E'},
                {'pregunta': 'La ciencia que estudia estadísticamente la '
                             'estructura y la dinámica de las poblaciones '
                             'humanas es: (I CEPRU 2024)',
                 'alternativas': ['Edafología',
                                  'Demogeografía',
                                  'Geomorfología',
                                  'Geodesia',
                                  'Demografía'],
                 'correcta': 'E'},
                {'pregunta': 'Considerando los periodos censales entre 1940 '
                             'y 2017, la región natural que presenta '
                             'tendencia negativa en su crecimiento '
                             'poblacional es la: (II CEPRU 2022)',
                 'alternativas': ['Faja subandina',
                                  'Vertiente occidental',
                                  'Sierra',
                                  'Costa',
                                  'Selva'],
                 'correcta': 'C'},
                {'pregunta': 'Según el censo del 2017, la región natural con '
                             'mayor tendencia al crecimiento poblacional es: '
                             '(Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['El Norte',
                                  'La Sierra',
                                  'La Costa',
                                  'El Sur',
                                  'La Selva'],
                 'correcta': 'C'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['La disciplina que estudia la distribución '
                                'de la población en un área geográfica es La '
                                'demogeografía.',
                                'La demografía estudia estadísticamente la '
                                'estructura y dinámica de Las poblaciones '
                                'humanas.',
                                'La tasa de natalidad en el Perú es '
                                'aproximadamente de 23,3‰.',
                                'La tasa de mortalidad en el Perú es '
                                'aproximadamente de 6,2‰.',
                                'La tasa de crecimiento poblacional '
                                'considera nacimientos, muertes y La '
                                'migración.',
                                'Según el INEI, la población del Perú al '
                                '2017 superaba 31 237 385 habitantes.',
                                'El organismo central y rector del Sistema '
                                'Estadístico Nacional del Perú es El INEI.',
                                'El INEI depende directamente de El '
                                'Presidente del Consejo de Ministros.',
                                'El antecesor del INEI, creado en 1969, se '
                                'llamó ONEC.',
                                'La población peruana se caracteriza por ser '
                                'Heterogénea, multirracial y '
                                'multicultural.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La pesca es una actividad económica de tipo '
                           '{Extractiva}.',
                           'Entre los factores de la riqueza ictiológica del '
                           'mar peruano figura {La frialdad de las aguas por '
                           'la Corriente Peruana}.',
                           'La especie más importante de la pesca marina '
                           'peruana es {La anchoveta}.',
                           'De la anchoveta se extrae principalmente {Harina '
                           'y aceite de pescado}.',
                           'La anchoveta sirve de alimento principal para '
                           '{Peces mayores y aves guaneras}.',
                           'El principal puerto pesquero del Perú, según '
                           'datos de 2018, fue {Chimbote}.',
                           'En la selva, una técnica tradicional de pesca es '
                           'el uso de {Flecha y arpón}.',
                           'El paiche se pesca principalmente en {Las cochas '
                           'amazónicas}.',
                           'El paiche se captura tradicionalmente con '
                           '{Arpón}.',
                           'La pesca de camarón en la costa se realiza en '
                           'ríos de Arequipa, Lima e {Ica}.',
                           'En la región andina, la pesca se practica '
                           'principalmente en el lago {Titicaca}.',
                           'La principal especie de pesca en la región '
                           'andina es {La trucha}.',
                           'Los departamentos productores de trucha son '
                           'Puno, Huancavelica y {Junín}.',
                           'Los impactos en la biodiversidad pesquera '
                           'provienen de la sobrepesca, la captura '
                           'incidental y {La degradación del hábitat}.',
                           'El exceso de pesca causa principalmente '
                           '{Reducción de la existencia de especies}.',
                           'La amplitud del zócalo continental favorece la '
                           'riqueza ictiológica porque facilita {La '
                           'penetración de rayos solares}.',
                           'El fenómeno del afloramiento influye en la pesca '
                           'porque {Produce la frialdad característica del '
                           'mar peruano}.',
                           'El zúngaro es una especie de pesca '
                           'característica de {La selva}.',
                           'El plancton constituye alimento fundamental para '
                           '{Los peces del mar peruano}.',
                           'La pesca deportiva en la región andina se '
                           'realiza principalmente con {Anzuelos, redes y '
                           'balsas}.']}],
  'cuadros': [{'titulo': '14.1 PRINCIPALES PUERTOS PESQUEROS (2018)',
               'encabezados': ['Orden', 'Puerto'],
               'filas': [['1°', '{Chimbote}'],
                         ['2°', '{Chicama}'],
                         ['3°', 'Coishco'],
                         ['4°', '{Paita}'],
                         ['5°', 'Callao']]}],
  'preguntas': [{'pregunta': 'La pesca es una actividad económica de tipo:',
                 'alternativas': ['Comercial únicamente',
                                  'Extractiva',
                                  'Reproductiva',
                                  'Industrial exclusiva',
                                  'Financiera'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los factores de la riqueza ictiológica '
                             'del mar peruano figura:',
                 'alternativas': ['La ausencia de zócalo continental',
                                  'La frialdad de las aguas por la Corriente '
                                  'Peruana',
                                  'El agua dulce',
                                  'El agua cálida',
                                  'La escasez de plancton'],
                 'correcta': 'B'},
                {'pregunta': 'La especie más importante de la pesca marina '
                             'peruana es:',
                 'alternativas': ['El jurel',
                                  'La anchoveta',
                                  'El bonito',
                                  'La caballa',
                                  'El atún'],
                 'correcta': 'B'},
                {'pregunta': 'De la anchoveta se extrae principalmente:',
                 'alternativas': ['Conservas de lujo',
                                  'Perlas',
                                  'Harina y aceite de pescado',
                                  'Sal marina',
                                  'Aceite de oliva'],
                 'correcta': 'C'},
                {'pregunta': 'La anchoveta sirve de alimento principal para:',
                 'alternativas': ['Solo el ser humano',
                                  'Solo aves terrestres',
                                  'Peces mayores y aves guaneras',
                                  'Solo mamíferos marinos',
                                  'Ningún otro organismo'],
                 'correcta': 'C'},
                {'pregunta': 'El principal puerto pesquero del Perú, según '
                             'datos de 2018, fue:',
                 'alternativas': ['Callao',
                                  'Paita',
                                  'Chancay',
                                  'Pisco',
                                  'Chimbote'],
                 'correcta': 'E'},
                {'pregunta': 'En la selva, una técnica tradicional de pesca '
                             'es el uso de:',
                 'alternativas': ['Flecha y arpón',
                                  'Trampas eléctricas',
                                  'Redes industriales',
                                  'Barcos factoría',
                                  'Sonar'],
                 'correcta': 'A'},
                {'pregunta': 'El paiche se pesca principalmente en:',
                 'alternativas': ['Lagunas andinas',
                                  'El mar peruano',
                                  'El lago Titicaca',
                                  'Las cochas amazónicas',
                                  'Ríos de la costa'],
                 'correcta': 'D'},
                {'pregunta': 'El paiche se captura tradicionalmente con:',
                 'alternativas': ['Arpón',
                                  'Redes de arrastre',
                                  'Trampas de metal',
                                  'Explosivos',
                                  'Anzuelo eléctrico'],
                 'correcta': 'A'},
                {'pregunta': 'La pesca de camarón en la costa se realiza en '
                             'ríos de Arequipa, Lima e:',
                 'alternativas': ['Tacna',
                                  'Tumbes',
                                  'Moquegua',
                                  'Ica',
                                  'Piura'],
                 'correcta': 'D'},
                {'pregunta': 'En la región andina, la pesca se practica '
                             'principalmente en el lago:',
                 'alternativas': ['Sausacocha',
                                  'Junín',
                                  'Chinchaycocha',
                                  'Titicaca',
                                  'Parinacochas'],
                 'correcta': 'D'},
                {'pregunta': 'La principal especie de pesca en la región '
                             'andina es:',
                 'alternativas': ['La trucha',
                                  'El camarón',
                                  'El atún',
                                  'La anchoveta',
                                  'El paiche'],
                 'correcta': 'A'},
                {'pregunta': 'Los departamentos productores de trucha son '
                             'Puno, Huancavelica y:',
                 'alternativas': ['Cusco',
                                  'Junín',
                                  'Tacna',
                                  'Arequipa',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'Los impactos en la biodiversidad pesquera '
                             'provienen de la sobrepesca, la captura '
                             'incidental y:',
                 'alternativas': ['El turismo',
                                  'El comercio justo',
                                  'La acuicultura',
                                  'La degradación del hábitat',
                                  'La pesca artesanal exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'El exceso de pesca causa principalmente:',
                 'alternativas': ['Ningún efecto negativo',
                                  'Reducción de la existencia de especies',
                                  'Mejora del ecosistema',
                                  'Incremento de la biodiversidad',
                                  'Aumento de especies'],
                 'correcta': 'B'},
                {'pregunta': 'La amplitud del zócalo continental favorece la '
                             'riqueza ictiológica porque facilita:',
                 'alternativas': ['La formación de olas',
                                  'El afloramiento volcánico',
                                  'La salinidad extrema',
                                  'El enfriamiento del agua',
                                  'La penetración de rayos solares'],
                 'correcta': 'E'},
                {'pregunta': 'El fenómeno del afloramiento influye en la '
                             'pesca porque:',
                 'alternativas': ['Genera tsunamis',
                                  'Reduce el oxígeno del agua',
                                  'Elimina el plancton',
                                  'Produce la frialdad característica del '
                                  'mar peruano',
                                  'Calienta el agua superficial'],
                 'correcta': 'D'},
                {'pregunta': 'El zúngaro es una especie de pesca '
                             'característica de:',
                 'alternativas': ['El lago Titicaca',
                                  'La costa sur',
                                  'La selva',
                                  'El mar peruano',
                                  'Los Andes centrales'],
                 'correcta': 'C'},
                {'pregunta': 'El plancton constituye alimento fundamental '
                             'para:',
                 'alternativas': ['Solo el hombre',
                                  'Solo los mamíferos marinos',
                                  'Ningún organismo marino',
                                  'Los peces del mar peruano',
                                  'Solo las aves'],
                 'correcta': 'D'},
                {'pregunta': 'La pesca deportiva en la región andina se '
                             'realiza principalmente con:',
                 'alternativas': ['Barcos factoría',
                                  'Trampas eléctricas',
                                  'Anzuelos, redes y balsas',
                                  'Redes industriales',
                                  'Explosivos'],
                 'correcta': 'C'},
                {'pregunta': 'El segundo departamento productor de gas en el '
                             'Perú es: (II CEPRU 2025)',
                 'alternativas': ['Junín',
                                  'Loreto',
                                  'Madre de Dios',
                                  'Piura',
                                  'Ucayali'],
                 'correcta': 'E'},
                {'pregunta': 'La refinería de La Oroya se ubica en el '
                             'departamento de: (II CEPRU 2022)',
                 'alternativas': ['Ayacucho',
                                  'Cajamarca',
                                  'Junín',
                                  'Moquegua',
                                  'Lima'],
                 'correcta': 'C'},
                {'pregunta': 'El principal productor de maíz amiláceo en el '
                             'territorio peruano es el departamento de: (II '
                             'CEPRU 2022)',
                 'alternativas': ['Arequipa',
                                  'Puno',
                                  'Pasco',
                                  'Cajamarca',
                                  'Lima'],
                 'correcta': 'D'},
                {'pregunta': 'El uso continuo del suelo y el predominio de '
                             'herramientas mecanizadas es una característica '
                             'de la agricultura denominada: (Primera '
                             'Oportunidad UNSAAC 2025)',
                 'alternativas': ['Tradicional',
                                  'Intensiva',
                                  'Extensiva',
                                  'Experimental',
                                  'Migratoria'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'LA PESCA EN EL MAR PERUANO',
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
                                'pesquero del Perú es Chimbote.']},
                     {'titulo': 'PESCA EN LA SELVA Y EN LA COSTA',
                      'items': ['En la selva se pesca con técnicas '
                                'tradicionales como redes de cortina, flecha '
                                'y arpón.',
                                'El paiche es la principal especie de pesca '
                                'en las cochas amazónicas, capturado con '
                                'arpón.',
                                'En la costa, la pesca de camarón se realiza '
                                'en ríos de Arequipa, Lima e Ica.']},
                     {'titulo': 'PESCA EN LA REGIÓN ANDINA',
                      'items': ['En la región andina se pesca principalmente '
                                'en el lago Titicaca, con fines deportivos y '
                                'alimenticios.',
                                'La principal especie de pesca andina es la '
                                'trucha, producida sobre todo en Puno, '
                                'Huancavelica y Junín.']},
                     {'titulo': 'IMPACTO AMBIENTAL DE LA PESCA',
                      'items': ['Los impactos en la biodiversidad pesquera '
                                'provienen de la sobrepesca, la captura '
                                'incidental y la degradación del hábitat.',
                                'El exceso de pesca reduce la existencia de '
                                'especies y afecta la estructura de los '
                                'ecosistemas marinos.']},
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['La pesca es una actividad económica de tipo '
                                'Extractiva.',
                                'Entre los factores de la riqueza '
                                'ictiológica del mar peruano figura La '
                                'frialdad de las aguas por la Corriente '
                                'Peruana.',
                                'La especie más importante de la pesca '
                                'marina peruana es La anchoveta.',
                                'De la anchoveta se extrae principalmente '
                                'Harina y aceite de pescado.',
                                'La anchoveta sirve de alimento principal '
                                'para Peces mayores y aves guaneras.',
                                'El principal puerto pesquero del Perú, '
                                'según datos de 2018, fue Chimbote.',
                                'En la selva, una técnica tradicional de '
                                'pesca es el uso de Flecha y arpón.',
                                'El paiche se pesca principalmente en Las '
                                'cochas amazónicas.',
                                'El paiche se captura tradicionalmente con '
                                'Arpón.',
                                'La pesca de camarón en la costa se realiza '
                                'en ríos de Arequipa, Lima e Ica.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La agricultura es una actividad económica de '
                           'tipo {Reproductiva}.',
                           'Los españoles introdujeron al Perú cultivos como '
                           'el arroz, cebada y {La caña de azúcar}.',
                           'Según la FAO, el Perú tiene en cultivo '
                           'aproximadamente {4,4 millones de hectáreas}.',
                           'El área cultivada representa del territorio '
                           'nacional peruano aproximadamente {3,5%}.',
                           'La agricultura de la costa se caracteriza por '
                           'ser {Intensiva, tecnificada y mecanizada}.',
                           'En la costa se pueden obtener anualmente {Hasta '
                           'dos cosechas}.',
                           'En la costa predominan los cultivos industriales '
                           'como la caña de azúcar y {El algodón}.',
                           'La agricultura de la costa goza de asistencia '
                           '{Crediticia por bancos y entidades financieras}.',
                           'La agricultura de la región andina se '
                           'caracteriza por ser {Extensiva y tradicional}.',
                           'En la región andina, el cultivo se realiza '
                           'principalmente en época de {Lluvias}.',
                           'Una herramienta tradicional de la agricultura '
                           'andina es {La chaquitaclla}.',
                           'La agricultura andina está orientada '
                           'principalmente al cultivo de productos de {Baja '
                           'rentabilidad, como papa, maíz y cebada}.',
                           'La agricultura de la selva se caracteriza por '
                           'ser {Migratoria}.',
                           'La técnica de roce, tumba y quema se practica en '
                           'la agricultura de {La selva}.',
                           'Entre los cultivos industriales de la selva '
                           'figuran la coca, el café y {El tabaco}.',
                           'La agricultura de la selva está relacionada con '
                           'la depredación de {El suelo}.',
                           'En el antiguo Perú se cultivaba, entre otros '
                           'productos {Papa, quinua y oca}.',
                           'Las tierras aptas para cultivo en el Perú '
                           'alcanzan aproximadamente {7,6 millones de '
                           'hectáreas}.',
                           'Un factor limitante de la agricultura en la '
                           'selva es {La limitación en transporte y '
                           'comercialización}.']}],
  'cuadros': [{'titulo': '15. LA AGRICULTURA POR REGIÓN',
               'encabezados': ['Región', 'Tipo', 'Rendimiento'],
               'filas': [['{Costa}', 'Intensiva y {mecanizada}', 'Alto'],
                         ['{Andina}', 'Extensiva y {tradicional}', 'Bajo'],
                         ['{Selva}', '{Migratoria}', 'Decreciente']]}],
  'preguntas': [{'pregunta': 'La agricultura es una actividad económica de '
                             'tipo:',
                 'alternativas': ['Financiera',
                                  'Informal',
                                  'Terciaria exclusiva',
                                  'Reproductiva',
                                  'Extractiva'],
                 'correcta': 'D'},
                {'pregunta': 'Los españoles introdujeron al Perú cultivos '
                             'como el arroz, cebada y:',
                 'alternativas': ['El tarwi',
                                  'La papa',
                                  'El olluco',
                                  'La quinua',
                                  'La caña de azúcar'],
                 'correcta': 'E'},
                {'pregunta': 'Según la FAO, el Perú tiene en cultivo '
                             'aproximadamente:',
                 'alternativas': ['20 millones de hectáreas',
                                  '500 mil hectáreas',
                                  '4,4 millones de hectáreas',
                                  '10 millones de hectáreas',
                                  '1 millón de hectáreas'],
                 'correcta': 'C'},
                {'pregunta': 'El área cultivada representa del territorio '
                             'nacional peruano aproximadamente:',
                 'alternativas': ['50%', '20%', '1%', '3,5%', '10%'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la costa se caracteriza por '
                             'ser:',
                 'alternativas': ['Intensiva, tecnificada y mecanizada',
                                  'Sin uso de maquinaria',
                                  'Migratoria',
                                  'Extensiva y tradicional',
                                  'De subsistencia exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'En la costa se pueden obtener anualmente:',
                 'alternativas': ['Hasta dos cosechas',
                                  'Una cosecha',
                                  'Cosechas cada dos años',
                                  'Tres cosechas mínimo',
                                  'Ninguna cosecha regular'],
                 'correcta': 'A'},
                {'pregunta': 'En la costa predominan los cultivos '
                             'industriales como la caña de azúcar y:',
                 'alternativas': ['La papa',
                                  'El algodón',
                                  'El olluco',
                                  'La quinua',
                                  'La cañihua'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la costa goza de asistencia:',
                 'alternativas': ['Solo comunal',
                                  'Internacional exclusiva',
                                  'Religiosa',
                                  'Militar',
                                  'Crediticia por bancos y entidades '
                                  'financieras'],
                 'correcta': 'E'},
                {'pregunta': 'La agricultura de la región andina se '
                             'caracteriza por ser:',
                 'alternativas': ['Extensiva y tradicional',
                                  'De exportación masiva',
                                  'Industrial',
                                  'Altamente tecnificada',
                                  'Intensiva y mecanizada'],
                 'correcta': 'A'},
                {'pregunta': 'En la región andina, el cultivo se realiza '
                             'principalmente en época de:',
                 'alternativas': ['Sequía',
                                  'Helada',
                                  'Granizo',
                                  'Lluvias',
                                  'Neblina'],
                 'correcta': 'D'},
                {'pregunta': 'Una herramienta tradicional de la agricultura '
                             'andina es:',
                 'alternativas': ['La bomba hidráulica',
                                  'La chaquitaclla',
                                  'El tractor',
                                  'La fumigadora',
                                  'La avioneta agrícola'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura andina está orientada '
                             'principalmente al cultivo de productos de:',
                 'alternativas': ['Solo productos tropicales',
                                  'Baja rentabilidad, como papa, maíz y '
                                  'cebada',
                                  'Solo productos industriales',
                                  'Solo flores ornamentales',
                                  'Alta rentabilidad para exportación'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la selva se caracteriza por '
                             'ser:',
                 'alternativas': ['Sin degradación de suelos',
                                  'Intensiva y mecanizada',
                                  'Exportadora exclusiva',
                                  'Migratoria',
                                  'Altamente tecnificada'],
                 'correcta': 'D'},
                {'pregunta': 'La técnica de roce, tumba y quema se practica '
                             'en la agricultura de:',
                 'alternativas': ['La región andina alta',
                                  'El litoral',
                                  'La selva',
                                  'Las lomas costeras',
                                  'La costa'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los cultivos industriales de la selva '
                             'figuran la coca, el café y:',
                 'alternativas': ['La cebada',
                                  'El tabaco',
                                  'El olluco',
                                  'La papa',
                                  'El trigo'],
                 'correcta': 'B'},
                {'pregunta': 'En la selva alta existen valles permanentes de '
                             'cultivo como Jaén, Bagua y:',
                 'alternativas': ['Tacna',
                                  'Ica',
                                  'Piura',
                                  'Chanchamayo',
                                  'Arequipa'],
                 'correcta': 'D'},
                {'pregunta': 'La agricultura de la selva está relacionada '
                             'con la depredación de:',
                 'alternativas': ['El suelo',
                                  'El agua',
                                  'El aire',
                                  'Los minerales',
                                  'El mar'],
                 'correcta': 'A'},
                {'pregunta': 'En el antiguo Perú se cultivaba, entre otros '
                             'productos:',
                 'alternativas': ['Trigo y cebada',
                                  'Papa, quinua y oca',
                                  'Algodón egipcio',
                                  'Café y tabaco',
                                  'Arroz y caña de azúcar'],
                 'correcta': 'B'},
                {'pregunta': 'Las tierras aptas para cultivo en el Perú '
                             'alcanzan aproximadamente:',
                 'alternativas': ['7,6 millones de hectáreas',
                                  '15 millones de hectáreas',
                                  '20 millones de hectáreas',
                                  '500 mil hectáreas',
                                  '1 millón de hectáreas'],
                 'correcta': 'A'},
                {'pregunta': 'Un factor limitante de la agricultura en la '
                             'selva es:',
                 'alternativas': ['La sobreproducción',
                                  'El exceso de crédito bancario',
                                  'El exceso de tecnología',
                                  'El exceso de maquinaria',
                                  'La limitación en transporte y '
                                  'comercialización'],
                 'correcta': 'E'},
                {'pregunta': 'Una característica de la ganadería de la selva '
                             'es: (I CEPRU 2024)',
                 'alternativas': ['Extensiva y migratoria',
                                  'Intensiva y migratoria',
                                  'Intensiva y experimental',
                                  'Extensiva y experimental',
                                  'Intensiva y extensiva'],
                 'correcta': 'A'},
                {'pregunta': 'La especie exótica de mayor reproducción '
                             'acuícola en la región andina corresponde a la: '
                             '(Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Palometa',
                                  'Ractacara',
                                  'Llambina',
                                  'Trucha',
                                  'Gamitana'],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['La agricultura es una actividad económica '
                                'de tipo Reproductiva.',
                                'Los españoles introdujeron al Perú cultivos '
                                'como el arroz, cebada y La caña de azúcar.',
                                'Según la FAO, el Perú tiene en cultivo '
                                'aproximadamente 4,4 millones de hectáreas.',
                                'El área cultivada representa del territorio '
                                'nacional peruano aproximadamente 3,5%.',
                                'La agricultura de la costa se caracteriza '
                                'por ser Intensiva, tecnificada y '
                                'mecanizada.',
                                'En la costa se pueden obtener anualmente '
                                'Hasta dos cosechas.',
                                'En la costa predominan los cultivos '
                                'industriales como la caña de azúcar y El '
                                'algodón.',
                                'La agricultura de la costa goza de '
                                'asistencia Crediticia por bancos y '
                                'entidades financieras.',
                                'La agricultura de la región andina se '
                                'caracteriza por ser Extensiva y '
                                'tradicional.',
                                'En la región andina, el cultivo se realiza '
                                'principalmente en época de Lluvias.']}]},
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
                 'alternativas': ['Tres', 'Seis', 'Cuatro', 'Ocho', 'Diez'],
                 'correcta': 'B'},
                {'pregunta': 'La Carretera Longitudinal de la Costa Sur va '
                             'desde Lima hasta la ciudad de Tacna, en la '
                             'frontera con:',
                 'alternativas': ['Bolivia',
                                  'Chile',
                                  'Ecuador',
                                  'Brasil',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'La Carretera Longitudinal de la Sierra Sur '
                             'llega hasta Desaguadero, en la frontera con:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Ecuador',
                                  'Brasil',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'La Carretera Longitudinal de la Selva Norte '
                             'llega hasta el Puente Internacional La Balsa, '
                             'en la frontera con:',
                 'alternativas': ['Bolivia',
                                  'Ecuador',
                                  'Colombia',
                                  'Brasil',
                                  'Chile'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto internacional Inca Manco Cápac '
                             'está ubicado en la ciudad de:',
                 'alternativas': ['Cusco',
                                  'Juliaca',
                                  'Puno capital',
                                  'Arequipa',
                                  'Tacna'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto internacional Francisco Secada '
                             'Vignetta está ubicado en la ciudad de:',
                 'alternativas': ['Pucallpa',
                                  'Iquitos',
                                  'Tarapoto',
                                  'Yurimaguas',
                                  'Tingo María'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto María Reiche Neuman, llamado así '
                             'en honor a la investigadora de las líneas de '
                             'Nasca, está ubicado en:',
                 'alternativas': ['Ica capital',
                                  'Nasca',
                                  'Pisco',
                                  'Chincha',
                                  'Palpa'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto internacional Padre Aldamiz está '
                             'ubicado en la ciudad de:',
                 'alternativas': ['Iquitos',
                                  'Puerto Maldonado',
                                  'Pucallpa',
                                  'Tarapoto',
                                  'Atalaya'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto internacional más importante del '
                             'Perú después de Jorge Chávez es: (II CEPRU '
                             '2025)',
                 'alternativas': ['Inca Manco Cápac',
                                  'Alejandro Velasco Astete',
                                  'Carlos Martínez de Pinillos',
                                  'Alfredo Rodríguez Ballón',
                                  'José Abelardo Quiñones'],
                 'correcta': 'B'},
                {'pregunta': 'La carretera más importante del Perú es la: (I '
                             'CEPRU 2024)',
                 'alternativas': ['De enlace',
                                  'De penetración',
                                  'Marginal de la selva',
                                  'Panamericana',
                                  'Interoceánica'],
                 'correcta': 'D'}],
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
                                'Aldamiz, en Puerto Maldonado.']}]},
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
                {'titulo': '17.4 PRINCIPALES AEROPUERTOS DEL PERÚ',
                 'items': ['El aeropuerto internacional {Jorge Chávez}, en '
                           'Lima, es el principal aeropuerto del Perú.',
                           'El aeropuerto {Alejandro Velasco Astete} está '
                           'ubicado en la ciudad del {Cusco}.',
                           'El aeropuerto {Alfredo Rodríguez Ballón} está '
                           'ubicado en la ciudad de {Arequipa}.',
                           'El aeropuerto {José Abelardo Quiñones} está '
                           'ubicado en la ciudad de {Chiclayo}.']}],
  'cuadros': [{'titulo': '17.2 DEPARTAMENTOS DESTACADOS DEL PERÚ',
               'encabezados': ['Departamento', 'Capital', 'Área km²'],
               'filas': [['{Loreto}', 'Iquitos', '368 851'],
                         ['{Cusco}', 'Cusco', '71 891'],
                         ['{Arequipa}', 'Arequipa', '63 345'],
                         ['{Lima}', 'Lima', '34 801'],
                         ['{Tumbes}', 'Tumbes', '4 669']]}],
  'preguntas': [{'pregunta': 'La geografía política estudia la organización '
                             'política y administrativa de:',
                 'alternativas': ['Solo los ríos',
                                  'Solo las ciudades',
                                  'Los Estados de la Tierra',
                                  'Solo el relieve',
                                  'Solo el clima'],
                 'correcta': 'C'},
                {'pregunta': 'El territorio de la República peruana está '
                             'integrado, según el artículo 189, por '
                             'regiones, departamentos, provincias y:',
                 'alternativas': ['Comunidades',
                                  'Distritos',
                                  'Centros poblados solamente',
                                  'Caseríos exclusivamente',
                                  'Anexos'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú está dividido en un número de '
                             'departamentos igual a:',
                 'alternativas': ['30', '20', '24', '28', '25'],
                 'correcta': 'C'},
                {'pregunta': 'Además de los departamentos, el Perú tiene una '
                             'provincia constitucional, que es:',
                 'alternativas': ['Trujillo',
                                  'Cusco',
                                  'Arequipa',
                                  'Lima',
                                  'El Callao'],
                 'correcta': 'E'},
                {'pregunta': 'El número total de distritos del Perú es '
                             'aproximadamente:',
                 'alternativas': ['1000', '1874', '500', '800', '2500'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento más extenso del Perú es:',
                 'alternativas': ['Arequipa',
                                  'Puno',
                                  'Ucayali',
                                  'Cusco',
                                  'Loreto'],
                 'correcta': 'E'},
                {'pregunta': 'La capital del departamento de Loreto es:',
                 'alternativas': ['Tarapoto',
                                  'Moyobamba',
                                  'Iquitos',
                                  'Pucallpa',
                                  'Yurimaguas'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento de Cusco tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['50 000 km²',
                                  '20 000 km²',
                                  '35 000 km²',
                                  '71 891 km²',
                                  '100 000 km²'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema donde el poder emana del gobierno '
                             'central se denomina:',
                 'alternativas': ['Centralismo',
                                  'Descentralización',
                                  'Regionalización',
                                  'Federalismo',
                                  'Municipalismo'],
                 'correcta': 'A'},
                {'pregunta': 'La descentralización está regulada en el '
                             'artículo de la Constitución número:',
                 'alternativas': ['24', '189', '91', '201', '188'],
                 'correcta': 'E'},
                {'pregunta': 'Según el artículo 188, la descentralización es '
                             'una forma de organización:',
                 'alternativas': ['Militar',
                                  'Religiosa',
                                  'Autoritaria',
                                  'Democrática',
                                  'Monárquica'],
                 'correcta': 'D'},
                {'pregunta': 'La descentralización es considerada una '
                             'política permanente de carácter:',
                 'alternativas': ['Temporal',
                                  'Obligatorio',
                                  'Opcional',
                                  'Regional exclusivo',
                                  'Provincial'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de descentralización se realiza:',
                 'alternativas': ['Sin ningún criterio técnico',
                                  'De forma inmediata y única',
                                  'Solo en Lima',
                                  'De manera aleatoria',
                                  'Por etapas, en forma progresiva y '
                                  'ordenada'],
                 'correcta': 'E'},
                {'pregunta': 'La descentralización implica la transferencia '
                             'de recursos del gobierno nacional hacia:',
                 'alternativas': ['Los gobiernos regionales y locales',
                                  'Organismos internacionales',
                                  'Solo el sector privado',
                                  'Solo las universidades',
                                  'Solo las Fuerzas Armadas'],
                 'correcta': 'A'},
                {'pregunta': 'La regionalización busca la conformación de '
                             'regiones con autonomía:',
                 'alternativas': ['Ninguna autonomía real',
                                  'Administrativa, económica y política',
                                  'Solo administrativa',
                                  'Solo política',
                                  'Solo económica'],
                 'correcta': 'B'},
                {'pregunta': 'El objetivo fundamental de la '
                             'descentralización es:',
                 'alternativas': ['Reducir la participación ciudadana',
                                  'Aumentar la burocracia central',
                                  'Concentrar el poder en Lima',
                                  'El desarrollo integral del país',
                                  'Eliminar los gobiernos regionales'],
                 'correcta': 'D'},
                {'pregunta': 'La capital del departamento de Arequipa es:',
                 'alternativas': ['Chivay',
                                  'Mollendo',
                                  'Islay',
                                  'Camaná',
                                  'Arequipa'],
                 'correcta': 'E'},
                {'pregunta': 'La capital del departamento de Áncash es:',
                 'alternativas': ['Huaraz',
                                  'Chimbote',
                                  'Huarmey',
                                  'Recuay',
                                  'Casma'],
                 'correcta': 'A'},
                {'pregunta': 'El departamento de Tumbes tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['100 000 km²',
                                  '1 000 km²',
                                  '4 669 km²',
                                  '15 000 km²',
                                  '50 000 km²'],
                 'correcta': 'C'},
                {'pregunta': 'En la provincia de La Convención, Cusco, se '
                             'crearon recientemente los distritos de Villa '
                             'Virgen, Villa Kintiarina, Incahuasi y:',
                 'alternativas': ['Calca',
                                  'Urubamba',
                                  'Anta',
                                  'Ollantaytambo',
                                  'Megantoni'],
                 'correcta': 'E'},
                {'pregunta': 'El principal aeropuerto internacional del '
                             'Perú, ubicado en Lima, es el:',
                 'alternativas': ['Alejandro Velasco Astete',
                                  'Jorge Chávez',
                                  'Alfredo Rodríguez Ballón',
                                  'José Abelardo Quiñones',
                                  'Rodríguez Ballón'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto Alejandro Velasco Astete está '
                             'ubicado en la ciudad de:',
                 'alternativas': ['Arequipa',
                                  'Cusco',
                                  'Chiclayo',
                                  'Piura',
                                  'Trujillo'],
                 'correcta': 'B'},
                {'pregunta': 'El aeropuerto Alfredo Rodríguez Ballón está '
                             'ubicado en la ciudad de:',
                 'alternativas': ['Cusco',
                                  'Arequipa',
                                  'Tacna',
                                  'Puno',
                                  'Chiclayo'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso técnico-geográfico para delimitar '
                             'los distritos, provincias y demás áreas '
                             'geográficas se llama: (II CEPRU 2024)',
                 'alternativas': ['Ordenamiento territorial',
                                  'Demarcación territorial',
                                  'Zonificación ecológica y económica',
                                  'Gestión territorial',
                                  'Regionalización'],
                 'correcta': 'B'},
                {'pregunta': 'Los niveles de estudio de la Zonificación '
                             'Ecológica y Económica (ZEE) son ejecutados en '
                             'tres niveles, estos son: (I CEPRU 2024)',
                 'alternativas': ['Microzonificación, mesozonificación y '
                                  'macrozonificación',
                                  'Departamental, provincial y distrital',
                                  'Macrozonificación, descentralización y '
                                  'regionalización',
                                  'Microzonificación, centralismo y '
                                  'descentralización',
                                  'Centralismo, descentralización y '
                                  'regionalización'],
                 'correcta': 'A'},
                {'pregunta': 'El nivel de estudio de la ZEE que contribuye a '
                             'la elaboración de políticas y planes de '
                             'desarrollo en el ámbito local o distrital, con '
                             'escala 1:25 000, es el nivel de: (II CEPRU '
                             '2022)',
                 'alternativas': ['Zonificación extra',
                                  'Microzonificación',
                                  'Mesozonificación',
                                  'Macrozonificación',
                                  'Demarcación territorial'],
                 'correcta': 'B'}],
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
                     {'titulo': 'PRINCIPALES AEROPUERTOS DEL PERÚ',
                      'items': ['El aeropuerto internacional Jorge Chávez, '
                                'en Lima, es el principal aeropuerto del '
                                'Perú.',
                                'El aeropuerto Alejandro Velasco Astete está '
                                'ubicado en la ciudad del Cusco.',
                                'El aeropuerto Alfredo Rodríguez Ballón está '
                                'ubicado en la ciudad de Arequipa.',
                                'El aeropuerto José Abelardo Quiñones está '
                                'ubicado en la ciudad de Chiclayo.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El departamento del Cusco se ubica en la parte '
                           '{Sur-oriental del Perú}.',
                           'La superficie del departamento del Cusco '
                           'representa del territorio nacional {5,6%}.',
                           'El punto más alto del departamento del Cusco es '
                           'el nevado {Ausangate}.',
                           'La altitud del nevado Ausangate es '
                           'aproximadamente de {6 364 m}.',
                           'El punto más bajo del departamento del Cusco se '
                           'ubica en la provincia de {La Convención}.',
                           'El departamento del Cusco limita por el norte '
                           'con {Ucayali}.',
                           'El departamento del Cusco limita por el sur con '
                           '{Arequipa}.',
                           'El departamento del Cusco limita por el este y '
                           'sureste con {Puno}.',
                           'La región andina o sierra representa del '
                           'territorio cusqueño {53%}.',
                           'La selva alta o faja sub andina representa del '
                           'territorio del Cusco {28%}.',
                           'La selva baja o llanura representa del '
                           'territorio cusqueño {19%}.',
                           'El departamento del Cusco está dividido en un '
                           'número de provincias igual a {13}.',
                           'El departamento del Cusco tiene un número de '
                           'distritos igual a {112}.',
                           'La provincia más extensa del departamento del '
                           'Cusco es {La Convención}.',
                           'La capital de la provincia de La Convención es '
                           '{Quillabamba}.',
                           'La provincia de La Convención representa del '
                           'área departamental del Cusco {41,52%}.',
                           'La capital de la provincia de Canchis es '
                           '{Sicuani}.',
                           'El distrito más poblado de la provincia del '
                           'Cusco, según el censo 2017, es {San Sebastián}.',
                           'El departamento del Cusco se caracteriza por ser '
                           'un espacio geográfico {Diverso en geomorfología, '
                           'clima, suelo, flora y fauna}.',
                           'El departamento del Cusco limita por el oeste '
                           'con {Ayacucho}.']}],
  'cuadros': [{'titulo': '18.3 REGIONES NATURALES DEL CUSCO',
               'encabezados': ['Región', 'Porcentaje'],
               'filas': [['{Andina} o Sierra', '{53}%'],
                         ['{Selva Alta}', '28%'],
                         ['{Selva Baja}', '{19}%']]}],
  'preguntas': [{'pregunta': 'El departamento del Cusco se ubica en la '
                             'parte:',
                 'alternativas': ['Sur-oriental del Perú',
                                  'Centro-occidental del Perú',
                                  'Litoral del Perú',
                                  'Extremo norte del país',
                                  'Nor-occidental del Perú'],
                 'correcta': 'A'},
                {'pregunta': 'La superficie del departamento del Cusco '
                             'representa del territorio nacional:',
                 'alternativas': ['20%', '1%', '5,6%', '15%', '10%'],
                 'correcta': 'C'},
                {'pregunta': 'El punto más alto del departamento del Cusco '
                             'es el nevado:',
                 'alternativas': ['Veronica',
                                  'Huanacaure',
                                  'Salkantay',
                                  'Chicón',
                                  'Ausangate'],
                 'correcta': 'E'},
                {'pregunta': 'La altitud del nevado Ausangate es '
                             'aproximadamente de:',
                 'alternativas': ['5 000 m',
                                  '6 364 m',
                                  '4 500 m',
                                  '5 800 m',
                                  '7 000 m'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más bajo del departamento del Cusco '
                             'se ubica en la provincia de:',
                 'alternativas': ['Quispicanchi',
                                  'Urubamba',
                                  'La Convención',
                                  'Paucartambo',
                                  'Calca'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento del Cusco limita por el norte '
                             'con:',
                 'alternativas': ['Ayacucho',
                                  'Arequipa',
                                  'Apurímac',
                                  'Puno',
                                  'Ucayali'],
                 'correcta': 'E'},
                {'pregunta': 'El departamento del Cusco limita por el sur '
                             'con:',
                 'alternativas': ['Junín',
                                  'Arequipa',
                                  'Ayacucho',
                                  'Ucayali',
                                  'Madre de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco limita por el este y '
                             'sureste con:',
                 'alternativas': ['Puno',
                                  'Ayacucho',
                                  'Madre de Dios',
                                  'Apurímac',
                                  'Junín'],
                 'correcta': 'A'},
                {'pregunta': 'La región andina o sierra representa del '
                             'territorio cusqueño:',
                 'alternativas': ['19%', '40%', '70%', '28%', '53%'],
                 'correcta': 'E'},
                {'pregunta': 'La selva alta o faja sub andina representa del '
                             'territorio del Cusco:',
                 'alternativas': ['28%', '10%', '19%', '53%', '5%'],
                 'correcta': 'A'},
                {'pregunta': 'La selva baja o llanura representa del '
                             'territorio cusqueño:',
                 'alternativas': ['28%', '70%', '19%', '40%', '53%'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento del Cusco está dividido en un '
                             'número de provincias igual a:',
                 'alternativas': ['10', '13', '15', '8', '20'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco tiene un número de '
                             'distritos igual a:',
                 'alternativas': ['166', '112', '84', '65', '100'],
                 'correcta': 'B'},
                {'pregunta': 'La provincia más extensa del departamento del '
                             'Cusco es:',
                 'alternativas': ['Calca',
                                  'Quispicanchi',
                                  'Urubamba',
                                  'Cusco',
                                  'La Convención'],
                 'correcta': 'E'},
                {'pregunta': 'La capital de la provincia de La Convención '
                             'es:',
                 'alternativas': ['Calca',
                                  'Sicuani',
                                  'Yanaoca',
                                  'Urubamba',
                                  'Quillabamba'],
                 'correcta': 'E'},
                {'pregunta': 'La provincia de La Convención representa del '
                             'área departamental del Cusco:',
                 'alternativas': ['10%', '70%', '20%', '41,52%', '5%'],
                 'correcta': 'D'},
                {'pregunta': 'La capital de la provincia de Canchis es:',
                 'alternativas': ['Sicuani',
                                  'Anta',
                                  'Espinar',
                                  'Yanaoca',
                                  'Acomayo'],
                 'correcta': 'A'},
                {'pregunta': 'El distrito más poblado de la provincia del '
                             'Cusco, según el censo 2017, es:',
                 'alternativas': ['Wanchaq',
                                  'Poroy',
                                  'San Sebastián',
                                  'Santiago',
                                  'Saylla'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento del Cusco se caracteriza por '
                             'ser un espacio geográfico:',
                 'alternativas': ['Diverso en geomorfología, clima, suelo, '
                                  'flora y fauna',
                                  'Homogéneo y uniforme',
                                  'Exclusivamente amazónico',
                                  'Solo desértico',
                                  'Sin variedad de pisos altitudinales'],
                 'correcta': 'A'},
                {'pregunta': 'El departamento del Cusco limita por el oeste '
                             'con:',
                 'alternativas': ['Puno',
                                  'Apurímac',
                                  'Ayacucho',
                                  'Madre de Dios',
                                  'Arequipa'],
                 'correcta': 'C'},
                {'pregunta': 'La montaña de origen volcánico que domina la '
                             'ciudad del Cusco es: (II CEPRU 2025)',
                 'alternativas': ['Araway',
                                  'Viva el Perú',
                                  'Pachatusan',
                                  'Wanaqauri',
                                  'Fortaleza'],
                 'correcta': 'C'},
                {'pregunta': 'Las capitales de las provincias de '
                             'Quispicanchi, Canchis y Paruro son, '
                             'respectivamente: (II CEPRU 2024)',
                 'alternativas': ['Urcos, Sicuani y Paruro',
                                  'Yanaoca, Canchis y Paruro',
                                  'Yanaoca, Sicuani y Paruro',
                                  'Yauri, Sicuani y Paruro',
                                  'Urcos, Yanaoca y Paruro'],
                 'correcta': 'A'},
                {'pregunta': 'Constituyen parte de los distritos de la '
                             'Provincia del Cusco: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Poroy, Huasao y Ccorca',
                                  'Ccorca, Saylla y Poroy',
                                  'Saylla, Huasao y Tipón',
                                  'Oropesa, Saylla y Poroy',
                                  'Wanchaq, Oropesa y Lucre'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades de Yanaoca y Quillabamba son las '
                             'capitales de las provincias de: (Primera '
                             'Oportunidad UNSAAC 2020)',
                 'alternativas': ['Paruro y La Convención',
                                  'Canas y Urubamba',
                                  'Canas y La Convención',
                                  'Calca y La Convención',
                                  'Acomayo y Anta'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LOCALIZACIÓN Y EXTENSIÓN',
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
                                'límite con Ucayali.']},
                     {'titulo': 'LÍMITES DEL DEPARTAMENTO',
                      'items': ['El Cusco limita por el norte con Ucayali, '
                                'por el noroeste con Junín, y por el noreste '
                                'con Madre de Dios.',
                                'El Cusco limita por el sur con Arequipa, '
                                'por el este y sureste con Puno, por el '
                                'oeste con Ayacucho y por el suroeste con '
                                'Apurímac.']},
                     {'titulo': 'REGIONES NATURALES DEL CUSCO',
                      'items': ['La región Andina o Sierra representa el 53% '
                                'del territorio del departamento del Cusco.',
                                'La Selva Alta o Faja Sub Andina representa '
                                'el 28% del territorio cusqueño.',
                                'La Selva Baja o llanura representa el 19% '
                                'del territorio del departamento.']},
                     {'titulo': 'DIVISIÓN POLÍTICA DEL CUSCO',
                      'items': ['El departamento del Cusco tiene 13 '
                                'provincias y 112 distritos.',
                                'La provincia con mayor extensión '
                                'territorial del Cusco es La Convención, con '
                                'capital Quillabamba, representando el '
                                '41,52% del área departamental.',
                                'La provincia del Cusco tiene como capital '
                                'la ciudad del Cusco, y su distrito más '
                                'poblado es San Sebastián.']},
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['El departamento del Cusco se ubica en la '
                                'parte Sur-oriental del Perú.',
                                'La superficie del departamento del Cusco '
                                'representa del territorio nacional 5,6%.',
                                'El punto más alto del departamento del '
                                'Cusco es el nevado Ausangate.',
                                'La altitud del nevado Ausangate es '
                                'aproximadamente de 6 364 m.',
                                'El punto más bajo del departamento del '
                                'Cusco se ubica en la provincia de La '
                                'Convención.',
                                'El departamento del Cusco limita por el '
                                'norte con Ucayali.',
                                'El departamento del Cusco limita por el sur '
                                'con Arequipa.',
                                'El departamento del Cusco limita por el '
                                'este y sureste con Puno.',
                                'La región andina o sierra representa del '
                                'territorio cusqueño 53%.',
                                'La selva alta o faja sub andina representa '
                                'del territorio del Cusco 28%.']}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['América es el segundo continente por su '
                           'extensión, después de {Asia}.',
                           'América comprende tres fracciones unidas por {El '
                           'Istmo de Panamá}.',
                           'El sistema orográfico más importante de América '
                           'del Sur es {La Cordillera de los Andes}.',
                           'El pico más elevado de América es el Aconcagua, '
                           'ubicado en {Argentina}.',
                           'La altitud aproximada del Aconcagua es de {6 960 '
                           'm}.',
                           'América está dividida políticamente en un número '
                           'de países igual a {35}.',
                           'América del Sur se extiende, por el sur, hasta '
                           '{La isla Diego Ramírez, Cabo de Hornos}.',
                           'El Macizo Brasileño se caracteriza por presentar '
                           'un relieve de {Meseta, de escasa elevación}.',
                           'América del Sur posee del agua dulce del planeta '
                           'aproximadamente {26%}.',
                           'El río más grande del planeta se ubica en '
                           '{Sudamérica}.',
                           'La capital de Brasil es {Brasilia}.',
                           'La moneda de Brasil es el {Real}.',
                           'La capital de Argentina es {Buenos Aires}.',
                           'La moneda del Perú es {El Nuevo Sol}.',
                           'Bolivia tiene como capital constitucional a '
                           '{Sucre}.',
                           'La sede de gobierno de Bolivia es {La Paz}.',
                           'La actividad económica principal de Chile, según '
                           'la tabla, es {Minería}.',
                           'La actividad económica principal de Venezuela es '
                           '{Minería (petróleo)}.',
                           'La moneda de Colombia es el {Peso}.',
                           'El río Orinoco y el río Paraná, junto con el '
                           'Amazonas, se caracterizan por ser {Ríos extensos '
                           'y caudalosos}.']}],
  'cuadros': [{'titulo': '19.3 PAÍSES DE AMÉRICA DEL SUR: CAPITAL Y MONEDA',
               'encabezados': ['País', 'Capital', 'Moneda'],
               'filas': [['{Argentina}', 'Buenos Aires', '{Peso}'],
                         ['{Brasil}', 'Brasilia', '{Real}'],
                         ['{Chile}', 'Santiago', 'Peso'],
                         ['{Perú}', 'Lima', '{Nuevo Sol}'],
                         ['{Venezuela}', 'Caracas', 'Bolívar']]}],
  'preguntas': [{'pregunta': 'América es el segundo continente por su '
                             'extensión, después de:',
                 'alternativas': ['Europa',
                                  'Antártida',
                                  'África',
                                  'Oceanía',
                                  'Asia'],
                 'correcta': 'E'},
                {'pregunta': 'América comprende tres fracciones unidas por:',
                 'alternativas': ['El Istmo de Panamá',
                                  'El Golfo de México',
                                  'El Canal de Suez',
                                  'El Canal de Magallanes',
                                  'El Estrecho de Bering'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema orográfico más importante de '
                             'América del Sur es:',
                 'alternativas': ['La Sierra Madre',
                                  'La Cordillera de los Andes',
                                  'Los Apalaches',
                                  'El Macizo Brasileño',
                                  'Las Rocosas'],
                 'correcta': 'B'},
                {'pregunta': 'El pico más elevado de América es el '
                             'Aconcagua, ubicado en:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Argentina',
                                  'Ecuador',
                                  'Perú'],
                 'correcta': 'C'},
                {'pregunta': 'La altitud aproximada del Aconcagua es de:',
                 'alternativas': ['7 500 m',
                                  '6 000 m',
                                  '5 000 m',
                                  '6 960 m',
                                  '4 500 m'],
                 'correcta': 'D'},
                {'pregunta': 'América está dividida políticamente en un '
                             'número de países igual a:',
                 'alternativas': ['20', '35', '50', '25', '45'],
                 'correcta': 'B'},
                {'pregunta': 'América del Sur se extiende, por el sur, '
                             'hasta:',
                 'alternativas': ['El Macizo Brasileño',
                                  'La isla Diego Ramírez, Cabo de Hornos',
                                  'Punta Gallinas',
                                  'El río Amazonas',
                                  'El Istmo de Panamá'],
                 'correcta': 'B'},
                {'pregunta': 'El Macizo Brasileño se caracteriza por '
                             'presentar un relieve de:',
                 'alternativas': ['Meseta, de escasa elevación',
                                  'Alta montaña',
                                  'Volcanes activos',
                                  'Cordillera nevada',
                                  'Fosas profundas'],
                 'correcta': 'A'},
                {'pregunta': 'América del Sur posee del agua dulce del '
                             'planeta aproximadamente:',
                 'alternativas': ['70%', '5%', '26%', '10%', '50%'],
                 'correcta': 'C'},
                {'pregunta': 'El río más grande del planeta se ubica en:',
                 'alternativas': ['Sudamérica',
                                  'Asia',
                                  'Norteamérica',
                                  'África',
                                  'Europa'],
                 'correcta': 'A'},
                {'pregunta': 'La capital de Brasil es:',
                 'alternativas': ['São Paulo',
                                  'Salvador',
                                  'Brasilia',
                                  'Belo Horizonte',
                                  'Río de Janeiro'],
                 'correcta': 'C'},
                {'pregunta': 'La moneda de Brasil es el:',
                 'alternativas': ['Peso',
                                  'Real',
                                  'Guaraní',
                                  'Dólar',
                                  'Bolívar'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de Argentina es:',
                 'alternativas': ['Mendoza',
                                  'La Plata',
                                  'Rosario',
                                  'Córdoba',
                                  'Buenos Aires'],
                 'correcta': 'E'},
                {'pregunta': 'La moneda del Perú es:',
                 'alternativas': ['El Bolívar',
                                  'El Dólar',
                                  'El Nuevo Sol',
                                  'El Real',
                                  'El Peso'],
                 'correcta': 'C'},
                {'pregunta': 'Bolivia tiene como capital constitucional a:',
                 'alternativas': ['Cochabamba',
                                  'Potosí',
                                  'La Paz',
                                  'Sucre',
                                  'Santa Cruz'],
                 'correcta': 'D'},
                {'pregunta': 'La sede de gobierno de Bolivia es:',
                 'alternativas': ['Santa Cruz',
                                  'Sucre',
                                  'Cochabamba',
                                  'Oruro',
                                  'La Paz'],
                 'correcta': 'E'},
                {'pregunta': 'La actividad económica principal de Chile, '
                             'según la tabla, es:',
                 'alternativas': ['Minería',
                                  'Pesca exclusiva',
                                  'Ganadería',
                                  'Agricultura',
                                  'Turismo'],
                 'correcta': 'A'},
                {'pregunta': 'La actividad económica principal de Venezuela '
                             'es:',
                 'alternativas': ['Turismo',
                                  'Ganadería',
                                  'Pesca',
                                  'Minería (petróleo)',
                                  'Agricultura'],
                 'correcta': 'D'},
                {'pregunta': 'La moneda de Colombia es el:',
                 'alternativas': ['Peso',
                                  'Real',
                                  'Guaraní',
                                  'Sol',
                                  'Bolívar'],
                 'correcta': 'A'},
                {'pregunta': 'El río Orinoco y el río Paraná, junto con el '
                             'Amazonas, se caracterizan por ser:',
                 'alternativas': ['Ríos artificiales',
                                  'Ríos de agua salada',
                                  'Ríos cortos y de bajo caudal',
                                  'Ríos estacionales secos',
                                  'Ríos extensos y caudalosos'],
                 'correcta': 'E'},
                {'pregunta': 'El país con menor extensión territorial de '
                             'América del Norte es: (II CEPRU 2022)',
                 'alternativas': ['Canadá',
                                  'Belice',
                                  'México',
                                  'El Salvador',
                                  'Estados Unidos'],
                 'correcta': 'B'},
                {'pregunta': 'Las montañas localizadas al oriente de '
                             'Norteamérica son los: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Montes Atlas',
                                  'Apalaches',
                                  'Alpes',
                                  'Escandinavos',
                                  'Urales'],
                 'correcta': 'B'}],
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
                     {'titulo': 'DATOS COMPLEMENTARIOS',
                      'items': ['América es el segundo continente por su '
                                'extensión, después de Asia.',
                                'América comprende tres fracciones unidas '
                                'por El Istmo de Panamá.',
                                'El sistema orográfico más importante de '
                                'América del Sur es La Cordillera de los '
                                'Andes.',
                                'El pico más elevado de América es el '
                                'Aconcagua, ubicado en Argentina.',
                                'La altitud aproximada del Aconcagua es de 6 '
                                '960 m.',
                                'América está dividida políticamente en un '
                                'número de países igual a 35.',
                                'América del Sur se extiende, por el sur, '
                                'hasta La isla Diego Ramírez, Cabo de '
                                'Hornos.',
                                'El Macizo Brasileño se caracteriza por '
                                'presentar un relieve de Meseta, de escasa '
                                'elevación.',
                                'América del Sur posee del agua dulce del '
                                'planeta aproximadamente 26%.',
                                'El río más grande del planeta se ubica en '
                                'Sudamérica.']}]},
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
                                  'Asiático',
                                  'Americano',
                                  'Antártico',
                                  'Oceánico'],
                 'correcta': 'B'},
                {'pregunta': 'Europa está dividida políticamente en un '
                             'número de países igual a:',
                 'alternativas': ['27', '43', '48', '53', '14'],
                 'correcta': 'B'},
                {'pregunta': 'El río más largo de Europa, que desemboca en '
                             'el mar Caspio, es el río:',
                 'alternativas': ['Danubio', 'Volga', 'Rin', 'Sena', 'Ebro'],
                 'correcta': 'B'},
                {'pregunta': 'El continente más extenso del planeta es:',
                 'alternativas': ['África',
                                  'Asia',
                                  'América',
                                  'Europa',
                                  'Oceanía'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema orográfico más importante del '
                             'mundo, ubicado en Asia, cuyo pico más elevado '
                             'es el Everest, se llama:',
                 'alternativas': ['Los Andes',
                                  'El Himalaya',
                                  'El Cáucaso',
                                  'Los Alpes',
                                  'El Atlas'],
                 'correcta': 'B'},
                {'pregunta': 'Asia se conecta con África a través del:',
                 'alternativas': ['Estrecho de Gibraltar',
                                  'Canal de Suez',
                                  'Estrecho de Bering',
                                  'Canal de Panamá',
                                  'Mar Rojo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El porcentaje de la superficie de la Antártida '
                             'cubierta de hielo es aproximadamente:',
                 'alternativas': ['80%', '98%', '50%', '70%', '90%'],
                 'correcta': 'B'},
                {'pregunta': 'El tratado que rige a la Antártida, firmado en '
                             '1959, prohibiendo actividades militares y '
                             'extracción de minerales, se llama:',
                 'alternativas': ['Tratado de Kioto',
                                  'Tratado Antártico',
                                  'Tratado de Montreal',
                                  'Protocolo de Madrid',
                                  'Convenio de Basilea'],
                 'correcta': 'B'},
                {'pregunta': 'África es considerada la cuna de la:',
                 'alternativas': ['Agricultura',
                                  'Raza humana',
                                  'Civilización occidental',
                                  'Escritura',
                                  'Ganadería'],
                 'correcta': 'B'},
                {'pregunta': 'El desierto más grande de la Tierra, ubicado '
                             'en África, es el desierto:',
                 'alternativas': ['Atacama',
                                  'Sahara',
                                  'Gobi',
                                  'Kalahari',
                                  'Namib'],
                 'correcta': 'B'},
                {'pregunta': 'El río más largo de África es el río:',
                 'alternativas': ['Congo',
                                  'Nilo',
                                  'Níger',
                                  'Senegal',
                                  'Zambeze'],
                 'correcta': 'B'},
                {'pregunta': 'Oceanía es el continente más pequeño de la '
                             'Tierra y se caracteriza por ser eminentemente:',
                 'alternativas': ['Continental',
                                  'Insular',
                                  'Desértico',
                                  'Glaciar',
                                  'Montañoso'],
                 'correcta': 'B'},
                {'pregunta': 'Las cuatro áreas geográficas en que se agrupa '
                             'Oceanía son Australasia, Micronesia, Polinesia '
                             'y:',
                 'alternativas': ['Indonesia',
                                  'Melanesia',
                                  'Malasia',
                                  'Filipinas',
                                  'Antillas'],
                 'correcta': 'B'},
                {'pregunta': 'El país más extenso de Oceanía, con relieve '
                             'llano y numerosos desiertos, es:',
                 'alternativas': ['Nueva Zelanda',
                                  'Australia',
                                  'Papúa Nueva Guinea',
                                  'Fiji',
                                  'Samoa'],
                 'correcta': 'B'},
                {'pregunta': 'El continente con la ubicación más austral es: '
                             '(II CEPRU 2025)',
                 'alternativas': ['América',
                                  'Asia',
                                  'Oceanía',
                                  'África',
                                  'Antártida'],
                 'correcta': 'E'}],
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
                                'desiertos.']}]}]
