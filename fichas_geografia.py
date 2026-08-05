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
                           'Santos}, Fred Kurt Schaefer y William Bunge.']},
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
                 'alternativas': ['Tierra y ciencia',
                                  'Tierra y descripción',
                                  'Mundo y espacio',
                                  'Espacio y estudio',
                                  'Suelo y medición'],
                 'correcta': 'B'},
                {'pregunta': 'Los geógrafos que iniciaron, en la Época '
                             'Moderna, una nueva era de la Geografía fueron:',
                 'alternativas': ['Eratóstenes y Ptolomeo',
                                  'Milton Santos y Bunge',
                                  'Von Humboldt y Carlos Ritter',
                                  'Ratzel y Brunhes',
                                  'Vidal de la Blache y Schaefer'],
                 'correcta': 'C'},
                {'pregunta': 'El geógrafo que calculó la circunferencia '
                             'terrestre con notable aproximación y elaboró '
                             'un mapamundi fue:',
                 'alternativas': ['Claudio Ptolomeo',
                                  'Eratóstenes',
                                  'Jean Brunhes',
                                  'Federico Ratzel',
                                  'Carlos Ritter'],
                 'correcta': 'B'},
                {'pregunta': 'El primero en elaborar un Atlas Universal fue:',
                 'alternativas': ['Eratóstenes',
                                  'Von Humboldt',
                                  'Claudio Ptolomeo',
                                  'Milton Santos',
                                  'Vidal de la Blache'],
                 'correcta': 'C'},
                {'pregunta': 'La etapa del pensamiento geográfico que va '
                             'desde los tiempos primitivos hasta mediados '
                             'del siglo XIX, de carácter empírico y '
                             'rutinario, es la Geografía:',
                 'alternativas': ['Nueva',
                                  'Cuantitativa',
                                  'Antigua',
                                  'Científica',
                                  'Teorética'],
                 'correcta': 'C'},
                {'pregunta': 'La Geografía Moderna o Científica se '
                             'fundamenta en la filosofía del:',
                 'alternativas': ['Neopositivismo',
                                  'Positivismo',
                                  'Empirismo',
                                  'Racionalismo',
                                  'Estructuralismo'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que se fundamenta en el '
                             'Neopositivismo o Positivismo Lógico y utiliza '
                             'el método deductivo es la Geografía:',
                 'alternativas': ['Antigua',
                                  'Moderna',
                                  'Descriptiva',
                                  'Nueva, Cuantitativa o Teorética',
                                  'Regional clásica'],
                 'correcta': 'D'},
                {'pregunta': 'Según Milton Santos da Almeida, el espacio '
                             'geográfico es:',
                 'alternativas': ['La epidermis del planeta Tierra',
                                  'La naturaleza modificada por el hombre a '
                                  'través del trabajo',
                                  'El marco físico de toda acción humana',
                                  'La suma de climas y relieves',
                                  'El territorio de un Estado'],
                 'correcta': 'B'},
                {'pregunta': 'La flora, la fauna y la diversidad de relieves '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Culturales',
                                  'Políticos',
                                  'Naturales',
                                  'Económicos',
                                  'Sociales'],
                 'correcta': 'C'},
                {'pregunta': 'Las viviendas, ciudades y vías de comunicación '
                             'son elementos del espacio geográfico de tipo:',
                 'alternativas': ['Naturales',
                                  'Culturales',
                                  'Bióticos',
                                  'Abióticos',
                                  'Climáticos'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la Geografía Física que estudia el '
                             'origen, evolución y formas del relieve es la:',
                 'alternativas': ['Climatología',
                                  'Edafología',
                                  'Geomorfología',
                                  'Hidrogeografía',
                                  'Biogeografía'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de la Hidrogeografía, el estudio de los '
                             'ríos corresponde a la:',
                 'alternativas': ['Oceanografía',
                                  'Limnología',
                                  'Fluviología',
                                  'Edafología',
                                  'Fitogeografía'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de la Biogeografía, el estudio de la '
                             'distribución de los animales corresponde a la:',
                 'alternativas': ['Fitogeografía',
                                  'Zoogeografía',
                                  'Limnología',
                                  'Oceanografía',
                                  'Demogeografía'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la Geografía Humana que estudia la '
                             'distribución de la población en la superficie '
                             'terrestre es la:',
                 'alternativas': ['Geografía Política',
                                  'Geografía Urbana',
                                  'Demogeografía',
                                  'Geografía Rural',
                                  'Geografía Histórica'],
                 'correcta': 'C'},
                {'pregunta': 'El principio metodológico según el cual todo '
                             'elemento del espacio geográfico debe ser '
                             'ubicado en mapas y cartas geográficas, '
                             'formulado por Federico Ratzel, es el de:',
                 'alternativas': ['Causalidad',
                                  'Comparación',
                                  'Localización, Distribución o Extensión',
                                  'Actividad o Dinamismo',
                                  'Relación o Conexión'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de Causalidad o Explicación, que '
                             'establece que todo elemento debe analizarse '
                             'por sus causas y consecuencias, fue formulado '
                             'por:',
                 'alternativas': ['Federico Ratzel',
                                  'Alejandro Von Humboldt',
                                  'Jean Brunhes',
                                  'Carlos Ritter',
                                  'Vidal de la Blache'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que establece que los elementos '
                             'del espacio geográfico están en íntima '
                             'interdependencia, formulado por Jean Brunhes, '
                             'es el de:',
                 'alternativas': ['Comparación',
                                  'Causalidad',
                                  'Relación o Conexión',
                                  'Localización',
                                  'Actividad'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de Comparación, también llamado '
                             'de Coordinación, Universalización o Analogía, '
                             'fue formulado por:',
                 'alternativas': ['Federico Ratzel y Jean Brunhes',
                                  'Carlos Ritter y Vidal de la Blache',
                                  'Von Humboldt y Ptolomeo',
                                  'Eratóstenes y Milton Santos',
                                  'Schaefer y Bunge'],
                 'correcta': 'B'},
                {'pregunta': 'Que los elementos del espacio geográfico deban '
                             'estudiarse en su constante y perpetua '
                             'transformación corresponde al principio de:',
                 'alternativas': ['Localización',
                                  'Causalidad',
                                  'Comparación',
                                  'Actividad, Dinamismo o Evolución',
                                  'Relación'],
                 'correcta': 'D'},
                {'pregunta': 'Herramientas propias de la Geografía Aplicada '
                             'para la gestión del territorio son:',
                 'alternativas': ['Solo mapas físicos en papel',
                                  'La cartografía digital, los SIG y la '
                                  'teledetección',
                                  'Únicamente encuestas de campo',
                                  'Los censos poblacionales',
                                  'Los tratados internacionales'],
                 'correcta': 'B'}]},
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
                           'mayor tamaño y más lejanos al Sol.']},
                {'titulo': '2.5 DIMENSIONES Y MOVIMIENTOS DE LA TIERRA',
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
                 'alternativas': ['Cósmicas',
                                  'Antrópicas',
                                  'Estelares',
                                  'Galácticas',
                                  'Solares'],
                 'correcta': 'B'},
                {'pregunta': 'La litósfera, la atmósfera y la hidrósfera son '
                             'entidades:',
                 'alternativas': ['Bióticas',
                                  'Abióticas',
                                  'Antrópicas',
                                  'Cósmicas',
                                  'Estelares'],
                 'correcta': 'B'},
                {'pregunta': 'La biósfera es una entidad del geosistema de '
                             'tipo:',
                 'alternativas': ['Abiótica',
                                  'Biótica',
                                  'Antrópica',
                                  'Cósmica',
                                  'Solar'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría del Big-Bang fue planteada '
                             'originalmente por:',
                 'alternativas': ['George Gamow',
                                  'George Lemaître',
                                  'Isaac Newton',
                                  'Edwin Hubble',
                                  'Albert Einstein'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Big-Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['5 000 millones de años',
                                  '15 000 millones de años',
                                  '1 000 millones de años',
                                  '500 millones de años',
                                  '100 000 millones de años'],
                 'correcta': 'B'},
                {'pregunta': 'Las aglomeraciones de millones de estrellas se '
                             'denominan:',
                 'alternativas': ['Nebulosas',
                                  'Galaxias',
                                  'Cúmulos',
                                  'Cometas',
                                  'Meteoritos'],
                 'correcta': 'B'},
                {'pregunta': 'El diámetro medio de la Vía Láctea es de '
                             'aproximadamente:',
                 'alternativas': ['10 000 años luz',
                                  '100 000 años luz',
                                  '1 000 000 años luz',
                                  '1 000 años luz',
                                  '500 000 años luz'],
                 'correcta': 'B'},
                {'pregunta': 'Las estrellas producen su propia luz mediante:',
                 'alternativas': ['Combustión química',
                                  'Fusión nuclear',
                                  'Reflexión solar',
                                  'Radiación cósmica',
                                  'Fisión atómica'],
                 'correcta': 'B'},
                {'pregunta': 'Las regiones interestelares donde nacen las '
                             'estrellas se llaman:',
                 'alternativas': ['Cúmulos',
                                  'Nebulosas',
                                  'Galaxias',
                                  'Cometas',
                                  'Asteroides'],
                 'correcta': 'B'},
                {'pregunta': 'El año luz es una unidad de:',
                 'alternativas': ['Tiempo',
                                  'Distancia',
                                  'Masa',
                                  'Velocidad',
                                  'Temperatura'],
                 'correcta': 'B'},
                {'pregunta': 'La luz del Sol tarda en llegar a la Tierra '
                             'aproximadamente:',
                 'alternativas': ['8,3 segundos',
                                  '8,3 minutos',
                                  '8,3 horas',
                                  '1 minuto',
                                  '1 hora'],
                 'correcta': 'B'},
                {'pregunta': 'El Sol contiene de la masa total del Sistema '
                             'Solar aproximadamente:',
                 'alternativas': ['50%', '98,85%', '75%', '25%', '10%'],
                 'correcta': 'B'},
                {'pregunta': 'La Unión Astronómica Internacional definió las '
                             'tres categorías de cuerpos del Sistema Solar '
                             'en el año:',
                 'alternativas': ['1990', '2006', '2015', '1980', '2020'],
                 'correcta': 'B'},
                {'pregunta': 'Los planetas interiores o terrestres son:',
                 'alternativas': ['Júpiter, Saturno, Urano y Neptuno',
                                  'Mercurio, Venus, Tierra y Marte',
                                  'Solo la Tierra y Marte',
                                  'Solo Mercurio y Venus',
                                  'Ceres y Plutón'],
                 'correcta': 'B'},
                {'pregunta': 'Los planetas exteriores o jovianos se '
                             'caracterizan por ser:',
                 'alternativas': ['Sólidos y pequeños',
                                  'Gaseosos y de mayor tamaño',
                                  'Cercanos al Sol',
                                  'De alta densidad',
                                  'Sin satélites'],
                 'correcta': 'B'},
                {'pregunta': 'El planeta con mayor número de satélites entre '
                             'los mostrados es:',
                 'alternativas': ['Saturno',
                                  'Júpiter',
                                  'Urano',
                                  'Neptuno',
                                  'Marte'],
                 'correcta': 'B'},
                {'pregunta': 'El planeta de mayor diámetro del Sistema Solar '
                             'es:',
                 'alternativas': ['Saturno',
                                  'Júpiter',
                                  'Neptuno',
                                  'Urano',
                                  'Tierra'],
                 'correcta': 'B'},
                {'pregunta': 'Plutón es clasificado actualmente como:',
                 'alternativas': ['Planeta interior',
                                  'Planeta enano',
                                  'Planeta exterior',
                                  'Satélite',
                                  'Cometa'],
                 'correcta': 'B'},
                {'pregunta': 'El geosistema se caracteriza por estar en:',
                 'alternativas': ['Equilibrio estático total',
                                  'Equilibrio dinámico relativo',
                                  'Colapso permanente',
                                  'Expansión sin cambios',
                                  'Estado sólido fijo'],
                 'correcta': 'B'},
                {'pregunta': 'La entidad antrópica del geosistema '
                             'corresponde a:',
                 'alternativas': ['Los océanos',
                                  'La sociedad humana',
                                  'Las rocas',
                                  'El aire',
                                  'Los seres vivos no humanos'],
                 'correcta': 'B'}]},
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
                {'titulo': '3.4 TELEDETECCIÓN, GPS Y HUSOS HORARIOS',
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
                                  'Expresar gráficamente mediante mapas',
                                  'Estudiar el clima',
                                  'Clasificar rocas',
                                  'Calcular distancias astronómicas'],
                 'correcta': 'B'},
                {'pregunta': 'El padre de la cartografía moderna fue:',
                 'alternativas': ['Gerardus Mercator',
                                  'Abraham Ortelius',
                                  'Claudio Ptolomeo',
                                  'Alexander von Humboldt',
                                  'Eratóstenes'],
                 'correcta': 'B'},
                {'pregunta': 'Las proyecciones cartográficas sirven para '
                             'transferir información desde la superficie '
                             'esférica hacia:',
                 'alternativas': ['Un globo terráqueo',
                                  'Un plano o mapa',
                                  'Una fotografía satelital',
                                  'Un modelo digital',
                                  'Un cilindro únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La proyección cilíndrica más utilizada en '
                             'cartografía es la de:',
                 'alternativas': ['Ortelius',
                                  'Mercator',
                                  'Ptolomeo',
                                  'Humboldt',
                                  'Gauss'],
                 'correcta': 'B'},
                {'pregunta': 'El principal inconveniente de la proyección '
                             'cilíndrica es que deforma:',
                 'alternativas': ['El centro del mapa',
                                  'Las áreas próximas a los polos',
                                  'El Ecuador',
                                  'Los continentes pequeños',
                                  'Las líneas rectas'],
                 'correcta': 'B'},
                {'pregunta': 'La proyección adecuada para representar un '
                             'solo país o región es la:',
                 'alternativas': ['Cilíndrica',
                                  'Cónica',
                                  'Cenital pura',
                                  'Mercator',
                                  'Universal'],
                 'correcta': 'B'},
                {'pregunta': 'La proyección que da lugar a un mapa circular '
                             'es la:',
                 'alternativas': ['Cilíndrica',
                                  'Cenital o azimutal',
                                  'Cónica',
                                  'De Mercator',
                                  'Poliédrica'],
                 'correcta': 'B'},
                {'pregunta': 'Los círculos máximos dividen a la Tierra en:',
                 'alternativas': ['Cuatro partes desiguales',
                                  'Dos partes iguales',
                                  'Tres partes iguales',
                                  'Ocho sectores',
                                  'Ninguna división real'],
                 'correcta': 'B'},
                {'pregunta': 'Los meridianos son semicírculos que van de:',
                 'alternativas': ['Este a oeste',
                                  'Polo a polo',
                                  'Ecuador a ecuador',
                                  'Trópico a trópico',
                                  'Centro a superficie'],
                 'correcta': 'B'},
                {'pregunta': 'El meridiano base internacional pasa por el '
                             'observatorio de:',
                 'alternativas': ['París',
                                  'Greenwich',
                                  'Madrid',
                                  'Washington',
                                  'Roma'],
                 'correcta': 'B'},
                {'pregunta': 'El meridiano de Greenwich y su opuesto dividen '
                             'la Tierra en los hemisferios:',
                 'alternativas': ['Norte y Sur',
                                  'Occidental y Oriental',
                                  'Superior e inferior',
                                  'Interno y externo',
                                  'Tropical y polar'],
                 'correcta': 'B'},
                {'pregunta': 'Los paralelos son líneas imaginarias con '
                             'orientación:',
                 'alternativas': ['Norte-Sur',
                                  'Este-Oeste',
                                  'Diagonal',
                                  'Vertical',
                                  'Radial'],
                 'correcta': 'B'},
                {'pregunta': 'La línea del Ecuador corresponde al paralelo:',
                 'alternativas': ['90°', '0°', '45°', '180°', "23°27'"],
                 'correcta': 'B'},
                {'pregunta': 'El Ecuador divide a la Tierra en los '
                             'hemisferios:',
                 'alternativas': ['Occidental y Oriental',
                                  'Norte y Sur',
                                  'Anterior y posterior',
                                  'Este y polar',
                                  'Tropical y templado'],
                 'correcta': 'B'},
                {'pregunta': 'El Trópico de Cáncer se ubica en el hemisferio '
                             'norte, a una latitud de:',
                 'alternativas': ['0°', "23°27'", '45°', "66°33'", '90°'],
                 'correcta': 'B'},
                {'pregunta': 'El Trópico de Capricornio se ubica en el '
                             'hemisferio:',
                 'alternativas': ['Norte',
                                  'Sur',
                                  'Occidental',
                                  'Oriental',
                                  'Ecuatorial'],
                 'correcta': 'B'},
                {'pregunta': 'Los Círculos Polares se ubican a una latitud '
                             'de:',
                 'alternativas': ["23°27'",
                                  "45°00'",
                                  "66°33'",
                                  "90°00'",
                                  "0°00'"],
                 'correcta': 'C'},
                {'pregunta': 'Los meridianos alcanzan su mayor separación '
                             'al:',
                 'alternativas': ['Cruzar los polos',
                                  'Atravesar el Ecuador',
                                  'Cruzar los trópicos',
                                  'Unirse en el centro',
                                  'Separarse en los círculos polares'],
                 'correcta': 'B'},
                {'pregunta': 'Los meridianos convergen (se unen) en:',
                 'alternativas': ['El Ecuador',
                                  'Los polos',
                                  'Los trópicos',
                                  'Los círculos polares',
                                  'El centro de la Tierra'],
                 'correcta': 'B'},
                {'pregunta': 'Las formas que se usan para transferir la '
                             'esfera terrestre a un mapa se llaman '
                             'superficies:',
                 'alternativas': ['Curvas irregulares',
                                  'Desarrollables, como conos y cilindros',
                                  'Esféricas puras',
                                  'Planas únicamente',
                                  'Triangulares'],
                 'correcta': 'B'}]},
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
                {'titulo': '4.3 CLASES DE ESCALA Y CÁLCULO DE DISTANCIAS',
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
                {'titulo': '4.4 EJEMPLO: HALLANDO LA ESCALA DE UN MAPA',
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
                                  'Plana',
                                  'Cónica',
                                  'Cilíndrica',
                                  'Irregular'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas se clasifican, según su función, en '
                             'generales y:',
                 'alternativas': ['Físicos',
                                  'Temáticos',
                                  'Políticos',
                                  'Digitales',
                                  'Satelitales'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas que representan el territorio por '
                             'medio de símbolos de un aspecto concreto son '
                             'los:',
                 'alternativas': ['Generales',
                                  'Temáticos',
                                  'Topográficos',
                                  'Catastrales',
                                  'Náuticos'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa con escala 1:50 000 corresponde a una '
                             'escala:',
                 'alternativas': ['Muy pequeña',
                                  'Grande',
                                  'Muy grande',
                                  'Pequeña',
                                  'Intermedia'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas de continentes y del mundo '
                             'corresponden a una escala:',
                 'alternativas': ['Grande',
                                  'Intermedia',
                                  'Muy pequeña',
                                  'Muy grande',
                                  'Pequeña'],
                 'correcta': 'C'},
                {'pregunta': 'Un plano de una vivienda corresponde a una '
                             'escala:',
                 'alternativas': ['Pequeña',
                                  'Muy grande',
                                  'Muy pequeña',
                                  'Intermedia',
                                  'Grande estándar'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento del mapa que se ubica en la parte '
                             'superior e indica el contenido es:',
                 'alternativas': ['La leyenda',
                                  'El título',
                                  'La escala',
                                  'La orientación',
                                  'La red geográfica'],
                 'correcta': 'B'},
                {'pregunta': 'En un mapa correctamente orientado, el Norte '
                             'corresponde a la parte:',
                 'alternativas': ['Inferior',
                                  'Superior',
                                  'Izquierda',
                                  'Derecha',
                                  'Central'],
                 'correcta': 'B'},
                {'pregunta': 'La ubicación de un mapa se determina mediante:',
                 'alternativas': ['El título',
                                  'La red de meridianos y paralelos',
                                  'Los colores usados',
                                  'El tamaño del papel',
                                  'La leyenda únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los signos convencionales de un mapa '
                             'constituyen:',
                 'alternativas': ['El título',
                                  'La leyenda',
                                  'La escala',
                                  'La orientación',
                                  'El marco'],
                 'correcta': 'B'},
                {'pregunta': 'Una escala de 1:100 000 significa que el '
                             'terreno real fue reducido:',
                 'alternativas': ['100 veces',
                                  '100 000 veces',
                                  '1000 veces',
                                  '10 veces',
                                  '1 000 000 veces'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa climático indica la distribución de:',
                 'alternativas': ['Ríos y lagos',
                                  'Los diversos tipos de clima',
                                  'Fronteras políticas',
                                  'Actividades económicas',
                                  'Especies vegetales'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa hidrográfico indica principalmente:',
                 'alternativas': ['Tipos de clima',
                                  'La distribución de ríos y lagos',
                                  'Fronteras administrativas',
                                  'Densidad poblacional',
                                  'Actividades agrícolas'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa político indica:',
                 'alternativas': ['Tipos de suelo',
                                  'Fronteras políticas y límites '
                                  'administrativos',
                                  'Distribución de lenguas',
                                  'Tipos de vegetación',
                                  'Recursos minerales'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa económico indica la distribución '
                             'territorial de:',
                 'alternativas': ['Las lenguas habladas',
                                  'Las actividades económicas',
                                  'Los acontecimientos históricos',
                                  'Los climas',
                                  'Las fronteras'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa lingüístico corresponde a un mapa '
                             'temático de tipo:',
                 'alternativas': ['Físico',
                                  'Humano',
                                  'Geológico',
                                  'Hidrográfico',
                                  'Climático'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa geológico indica:',
                 'alternativas': ['La distribución de lenguas',
                                  'La composición de las rocas de la corteza '
                                  'terrestre',
                                  'Las fronteras políticas',
                                  'Las actividades económicas',
                                  'La densidad de población'],
                 'correcta': 'B'},
                {'pregunta': 'Los mapas generales suelen aparecer en:',
                 'alternativas': ['Solo revistas científicas',
                                  'Los atlas',
                                  'Solo periódicos',
                                  'Solo internet',
                                  'Solo documentos legales'],
                 'correcta': 'B'},
                {'pregunta': 'Un mapa de provincias y departamentos '
                             'corresponde a una escala:',
                 'alternativas': ['Muy grande',
                                  'Intermedia',
                                  'Muy pequeña',
                                  'Pequeña extrema',
                                  'Nula'],
                 'correcta': 'B'},
                {'pregunta': 'La ventaja principal del mapa frente a la '
                             'esfera terrestre es:',
                 'alternativas': ['Mayor exactitud absoluta',
                                  'Facilidad de manejo y representación '
                                  'ampliada de áreas pequeñas',
                                  'Eliminar toda deformación',
                                  'No requerir escala',
                                  'Representar en tres dimensiones'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Silicio y aluminio',
                                  'Níquel y hierro',
                                  'Magnesio y oxígeno',
                                  'Carbono e hidrógeno',
                                  'Potasio y sodio'],
                 'correcta': 'B'},
                {'pregunta': 'La discontinuidad que limita el núcleo externo '
                             'del núcleo interno es la de:',
                 'alternativas': ['Mohorovicic',
                                  'Lehman',
                                  'Conrad',
                                  'Repetti',
                                  'Gutemberg'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo está limitado con el manto por la '
                             'discontinuidad de:',
                 'alternativas': ['Conrad',
                                  'Mohorovicic',
                                  'Wiechert Gutemberg',
                                  'Repetti',
                                  'Lehman'],
                 'correcta': 'C'},
                {'pregunta': 'El manto externo y el manto interno están '
                             'separados por la discontinuidad de:',
                 'alternativas': ['Mohorovicic',
                                  'Repetti',
                                  'Gutemberg',
                                  'Conrad',
                                  'Lehman'],
                 'correcta': 'B'},
                {'pregunta': 'El manto está limitado con la corteza '
                             'terrestre por la discontinuidad de:',
                 'alternativas': ['Lehman',
                                  'Repetti',
                                  'Mohorovicic',
                                  'Gutemberg',
                                  'Conrad'],
                 'correcta': 'C'},
                {'pregunta': 'La astenósfera es una capa ubicada en:',
                 'alternativas': ['El núcleo interno',
                                  'La parte superior del manto',
                                  'La corteza oceánica',
                                  'El núcleo externo',
                                  'La corteza continental'],
                 'correcta': 'B'},
                {'pregunta': 'La astenósfera es clave para explicar la '
                             'teoría de:',
                 'alternativas': ['El Big Bang',
                                  'La Tectónica de Placas',
                                  'La formación del universo',
                                  'El ciclo del agua',
                                  'La formación de galaxias'],
                 'correcta': 'B'},
                {'pregunta': 'La corteza continental o granítica se compone '
                             'principalmente de:',
                 'alternativas': ['Silicio y magnesio',
                                  'Silicio y aluminio',
                                  'Hierro y níquel',
                                  'Carbono y oxígeno',
                                  'Potasio y calcio'],
                 'correcta': 'B'},
                {'pregunta': 'La corteza oceánica o basáltica se compone '
                             'principalmente de:',
                 'alternativas': ['Silicio y aluminio',
                                  'Silicio y magnesio',
                                  'Hierro y níquel',
                                  'Oxígeno y carbono',
                                  'Calcio y sodio'],
                 'correcta': 'B'},
                {'pregunta': 'La corteza externa y la corteza interna están '
                             'separadas por la discontinuidad de:',
                 'alternativas': ['Mohorovicic',
                                  'Conrad',
                                  'Gutemberg',
                                  'Lehman',
                                  'Repetti'],
                 'correcta': 'B'},
                {'pregunta': 'El relieve terrestre se define como el '
                             'conjunto de:',
                 'alternativas': ['Climas del planeta',
                                  'Irregularidades o geoformas de la '
                                  'superficie',
                                  'Corrientes marinas',
                                  'Capas de la atmósfera',
                                  'Zonas sísmicas únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los procesos que actúan del interior hacia la '
                             'superficie terrestre se llaman:',
                 'alternativas': ['Geodinámica externa',
                                  'Geodinámica interna',
                                  'Erosión eólica',
                                  'Meteorización',
                                  'Sedimentación'],
                 'correcta': 'B'},
                {'pregunta': 'La geodinámica interna es considerada una '
                             'fuerza:',
                 'alternativas': ['Destructora del relieve',
                                  'Constructora del relieve',
                                  'Sin efecto en el relieve',
                                  'Solo erosiva',
                                  'Exclusivamente marina'],
                 'correcta': 'B'},
                {'pregunta': 'Los movimientos orogénicos originan '
                             'principalmente:',
                 'alternativas': ['Erosión costera',
                                  'Plegamientos y fallas',
                                  'Sedimentación fluvial',
                                  'Formación de dunas',
                                  'Glaciación'],
                 'correcta': 'B'},
                {'pregunta': 'Los movimientos orogénicos se caracterizan por '
                             'ser:',
                 'alternativas': ['Verticales y rápidos',
                                  'Laterales, compresivos y lentos',
                                  'Solo horizontales rápidos',
                                  'Explosivos',
                                  'Aleatorios'],
                 'correcta': 'B'},
                {'pregunta': 'Los movimientos epirogénicos también se '
                             'conocen como:',
                 'alternativas': ['Tectónica horizontal',
                                  'Tectónica vertical',
                                  'Vulcanismo puro',
                                  'Sismicidad superficial',
                                  'Erosión interna'],
                 'correcta': 'B'},
                {'pregunta': 'El origen de los movimientos epirogénicos se '
                             'encuentra en:',
                 'alternativas': ['El vulcanismo',
                                  'La isostasia',
                                  'La erosión eólica',
                                  'Las corrientes marinas',
                                  'La meteorización química'],
                 'correcta': 'B'},
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
                 'alternativas': ['Erosión fluvial',
                                  'Vulcanismo',
                                  'Sedimentación eólica',
                                  'Meteorización física',
                                  'Glaciarismo'],
                 'correcta': 'B'},
                {'pregunta': 'El manto representa aproximadamente qué '
                             'porcentaje del volumen terrestre:',
                 'alternativas': ['16%', '83%', '1%', '50%', '25%'],
                 'correcta': 'B'}]},
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
                                  'Tórrida',
                                  'Glacial',
                                  'Subtropical',
                                  'Polar'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú es considerado el país de América del '
                             'Sur con extensión:',
                 'alternativas': ['La mayor',
                                  'La tercera mayor',
                                  'La menor',
                                  'La cuarta mayor',
                                  'La segunda menor'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más alto del Perú es el nevado:',
                 'alternativas': ['Salkantay',
                                  'Huascarán',
                                  'Ausangate',
                                  'Coropuna',
                                  'Alpamayo'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más bajo del territorio peruano es:',
                 'alternativas': ['El lago Titicaca',
                                  'La Depresión de Bayovar',
                                  'El valle del Colca',
                                  'La fosa de Tacna',
                                  'El desierto de Sechura'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más lluvioso del Perú es:',
                 'alternativas': ['Iquitos',
                                  'Quince Mil',
                                  'Chachapoyas',
                                  'Tarapoto',
                                  'Moyobamba'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más caluroso del Perú es:',
                 'alternativas': ['Piura',
                                  'Neshuya',
                                  'Tumbes',
                                  'Sechura',
                                  'Jaén'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar más frío del Perú es:',
                 'alternativas': ['Puno',
                                  'Imata',
                                  'Cusco',
                                  'Juliaca',
                                  'El Misti'],
                 'correcta': 'B'},
                {'pregunta': 'La frontera más extensa del Perú es con:',
                 'alternativas': ['Ecuador',
                                  'Brasil',
                                  'Chile',
                                  'Bolivia',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'La frontera más corta del Perú es con:',
                 'alternativas': ['Bolivia',
                                  'Colombia',
                                  'Chile',
                                  'Ecuador',
                                  'Brasil'],
                 'correcta': 'C'},
                {'pregunta': 'El perímetro total del Perú, incluido el '
                             'litoral, es aproximadamente de:',
                 'alternativas': ['5 000 km',
                                  '10 156,8 km',
                                  '20 000 km',
                                  '1 000 km',
                                  '15 000 km'],
                 'correcta': 'B'},
                {'pregunta': 'Por el sur, el Perú limita con:',
                 'alternativas': ['Ecuador',
                                  'Chile',
                                  'Colombia',
                                  'Brasil',
                                  'Bolivia'],
                 'correcta': 'B'},
                {'pregunta': 'Por el este, el Perú limita con:',
                 'alternativas': ['Solo Brasil',
                                  'Bolivia y Brasil',
                                  'Solo Bolivia',
                                  'Chile y Bolivia',
                                  'Ecuador y Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'El punto extremo norte del Perú se relaciona '
                             'con el río:',
                 'alternativas': ['Amazonas',
                                  'Putumayo',
                                  'Madre de Dios',
                                  'Marañón',
                                  'Ucayali'],
                 'correcta': 'B'},
                {'pregunta': 'El punto extremo sur del Perú se ubica en:',
                 'alternativas': ['Arequipa',
                                  'Tacna',
                                  'Puno',
                                  'Moquegua',
                                  'Ica'],
                 'correcta': 'B'},
                {'pregunta': 'El punto extremo este del Perú limita con:',
                 'alternativas': ['Ecuador',
                                  'Bolivia',
                                  'Chile',
                                  'Colombia',
                                  'Brasil únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La región Costa representa del área '
                             'continental peruana:',
                 'alternativas': ['12,5%', '30,2%', '50%', '5%', '20%'],
                 'correcta': 'A'},
                {'pregunta': 'La región Andina representa del área '
                             'continental peruana:',
                 'alternativas': ['12,5%', '30,2%', '60%', '10%', '45%'],
                 'correcta': 'B'},
                {'pregunta': 'El litoral peruano se extiende desde Boca de '
                             'Capones hasta:',
                 'alternativas': ['Tumbes',
                                  'El hito La Concordia',
                                  'Ilo',
                                  'Tacna',
                                  'Paracas'],
                 'correcta': 'B'},
                {'pregunta': 'La longitud del litoral peruano es '
                             'aproximadamente de:',
                 'alternativas': ['1 000 km',
                                  '3 080 km',
                                  '5 000 km',
                                  '500 km',
                                  '10 000 km'],
                 'correcta': 'B'},
                {'pregunta': 'El ancho del territorio peruano, de este a '
                             'oeste, es de aproximadamente:',
                 'alternativas': ['1 640 km',
                                  '2 135 km',
                                  '500 km',
                                  '3 000 km',
                                  '800 km'],
                 'correcta': 'A'}]},
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
                 'alternativas': ['La Costa',
                                  'La Amazónica o Selva',
                                  'La Andina',
                                  'El litoral',
                                  'Ninguna en particular'],
                 'correcta': 'B'},
                {'pregunta': 'La región amazónica representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['12,5%', '30,2%', '57,3%', '10%', '90%'],
                 'correcta': 'C'},
                {'pregunta': 'La selva alta también se conoce como:',
                 'alternativas': ['Omagua',
                                  'Rupa Rupa o Ceja de Selva',
                                  'Llanura Amazónica',
                                  'Cratón Brasileño',
                                  'Selva Baja'],
                 'correcta': 'B'},
                {'pregunta': 'El relieve de la selva alta está afectado por:',
                 'alternativas': ['El Cratón Brasileño',
                                  'La Tectónica Andina',
                                  'Solo la erosión eólica',
                                  'El clima ecuatorial',
                                  'La sedimentación marina'],
                 'correcta': 'B'},
                {'pregunta': 'Los cortes fluviales donde un río corta una '
                             'cadena de montañas se llaman:',
                 'alternativas': ['Restingas',
                                  'Pongos',
                                  'Qochas',
                                  'Tahuampas',
                                  'Altos'],
                 'correcta': 'B'},
                {'pregunta': 'El Pongo de Mainique fue formado por el río:',
                 'alternativas': ['Marañón',
                                  'Urubamba',
                                  'Huallaga',
                                  'Tambo',
                                  'Inambari'],
                 'correcta': 'B'},
                {'pregunta': 'La selva baja también se llama:',
                 'alternativas': ['Rupa Rupa',
                                  'Omagua o Llanura Amazónica',
                                  'Ceja de Selva',
                                  'Faja Sub Andina',
                                  'Cordillera Oriental'],
                 'correcta': 'B'},
                {'pregunta': 'La selva baja no es afectada por la tectónica '
                             'andina porque se asienta sobre:',
                 'alternativas': ['La Cordillera Oriental',
                                  'El antiguo Cratón Brasileño',
                                  'La plataforma costanera',
                                  'La cadena costanera',
                                  'Los Andes centrales'],
                 'correcta': 'B'},
                {'pregunta': 'Los lagos abandonados por los ríos que '
                             'cambiaron de cauce se llaman:',
                 'alternativas': ['Tahuampas',
                                  'Qochas',
                                  'Restingas',
                                  'Altos',
                                  'Filos'],
                 'correcta': 'B'},
                {'pregunta': 'Las áreas bajas cubiertas de agua todo el año, '
                             'con palmeras de aguaje, se llaman:',
                 'alternativas': ['Restingas',
                                  'Tahuampas o aguajales',
                                  'Altos',
                                  'Filos',
                                  'Qochas'],
                 'correcta': 'B'},
                {'pregunta': 'Las áreas que solo se inundan en las crecidas '
                             'de los ríos se llaman:',
                 'alternativas': ['Altos',
                                  'Restingas',
                                  'Filos',
                                  'Tahuampas',
                                  'Qochas'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades de la selva baja se han edificado '
                             'principalmente en:',
                 'alternativas': ['Las restingas',
                                  'Los altos',
                                  'Las tahuampas',
                                  'Las qochas',
                                  'Los filos'],
                 'correcta': 'B'},
                {'pregunta': 'La región Costa representa del territorio '
                             'nacional aproximadamente:',
                 'alternativas': ['57,3%', '30,2%', '12,5%', '5%', '70%'],
                 'correcta': 'C'},
                {'pregunta': 'La región Costa se extiende desde el nivel del '
                             'mar hasta una altitud de:',
                 'alternativas': ['500 m',
                                  '1000 m',
                                  '2000 m',
                                  '300 m',
                                  '1500 m'],
                 'correcta': 'B'},
                {'pregunta': 'La Costa Sur o Meridional se extiende entre la '
                             'frontera con Chile y:',
                 'alternativas': ['Tumbes',
                                  'La península de Paracas',
                                  'Trujillo',
                                  'Chiclayo',
                                  'Lima'],
                 'correcta': 'B'},
                {'pregunta': 'La Cadena Costanera alcanza su mayor altitud '
                             'en:',
                 'alternativas': ['Lima',
                                  'El cerro Criterión, Ica',
                                  'Tacna',
                                  'Arequipa',
                                  'Piura'],
                 'correcta': 'B'},
                {'pregunta': 'Las planicies de origen aluvial en la costa '
                             'sur se llaman:',
                 'alternativas': ['Tablazos',
                                  'Pampas',
                                  'Tahuampas',
                                  'Restingas',
                                  'Aguajales'],
                 'correcta': 'B'},
                {'pregunta': 'Los valles de Jaén y Bagua se ubican en la '
                             'subregión de:',
                 'alternativas': ['Selva baja',
                                  'Selva alta',
                                  'Costa sur',
                                  'Costa norte',
                                  'Sierra central'],
                 'correcta': 'B'},
                {'pregunta': 'El valle de Chanchamayo pertenece al '
                             'departamento de:',
                 'alternativas': ['Cusco',
                                  'Junín',
                                  'Puno',
                                  'San Martín',
                                  'Huánuco'],
                 'correcta': 'B'},
                {'pregunta': 'El Boquerón del Padre Abad fue formado por el '
                             'río:',
                 'alternativas': ['Marañón',
                                  'Yuracyacu',
                                  'Huallaga',
                                  'Tambo',
                                  'Urubamba'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Cauce',
                                  'Caudal',
                                  'Curso',
                                  'Talweg',
                                  'Régimen'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando un río arrastra la mínima cantidad de '
                             'agua, se le llama:',
                 'alternativas': ['Crecida',
                                  'Estiaje',
                                  'Torrente',
                                  'Afluente',
                                  'Cauce'],
                 'correcta': 'B'},
                {'pregunta': 'El canal o lecho por donde se desplazan las '
                             'aguas del río se llama:',
                 'alternativas': ['Talweg',
                                  'Cauce',
                                  'Curso',
                                  'Régimen',
                                  'Vertiente'],
                 'correcta': 'B'},
                {'pregunta': 'La línea que une los puntos más profundos del '
                             'canal fluvial es:',
                 'alternativas': ['El cauce',
                                  'El talweg o vaguada',
                                  'La cuenca',
                                  'El curso',
                                  'El régimen'],
                 'correcta': 'B'},
                {'pregunta': 'Los ríos que salen de otro río o de un lago se '
                             'denominan:',
                 'alternativas': ['Afluentes',
                                  'Efluentes',
                                  'Confluentes',
                                  'Principales',
                                  'Torrentosos'],
                 'correcta': 'B'},
                {'pregunta': 'La ANA ha identificado en el Perú un total de '
                             'unidades hidrográficas de:',
                 'alternativas': ['59', '159', '259', '99', '359'],
                 'correcta': 'B'},
                {'pregunta': 'La cuenca del Amazonas representa del '
                             'territorio nacional:',
                 'alternativas': ['30,2%', '74,5%', '3,8%', '12,5%', '57,3%'],
                 'correcta': 'B'},
                {'pregunta': 'La cuenca hidrográfica más extensa del Perú, '
                             'de América y del mundo es la del:',
                 'alternativas': ['Titicaca',
                                  'Amazonas',
                                  'Pacífico',
                                  'Marañón',
                                  'Ucayali'],
                 'correcta': 'B'},
                {'pregunta': 'La cuenca del Titicaca representa del '
                             'territorio nacional:',
                 'alternativas': ['3,8%', '30,2%', '57,3%', '12,5%', '74,5%'],
                 'correcta': 'A'},
                {'pregunta': 'El lago Titicaca es reconocido mundialmente '
                             'por ser el lago:',
                 'alternativas': ['Más profundo del mundo',
                                  'Navegable más alto del mundo',
                                  'Más extenso de Sudamérica',
                                  'Con más islas del mundo',
                                  'Más frío del planeta'],
                 'correcta': 'B'},
                {'pregunta': 'El lago Titicaca se ubica a una altitud '
                             'aproximada de:',
                 'alternativas': ['2 500 m',
                                  '3 810 m',
                                  '4 500 m',
                                  '5 000 m',
                                  '1 800 m'],
                 'correcta': 'B'},
                {'pregunta': 'El origen geológico del lago Titicaca es:',
                 'alternativas': ['Volcánico',
                                  'Tectónico',
                                  'Glaciar exclusivamente',
                                  'Kárstico',
                                  'Eólico'],
                 'correcta': 'B'},
                {'pregunta': 'El lago Titicaca se divide en dos sectores '
                             'separados por el Estrecho de:',
                 'alternativas': ['Magallanes',
                                  'Tiquina',
                                  'Bering',
                                  'Gibraltar',
                                  'Panamá'],
                 'correcta': 'B'},
                {'pregunta': 'El sector del Titicaca correspondiente al Perú '
                             'se llama lago Mayor o:',
                 'alternativas': ['Huiñaymarca',
                                  'Chucuito',
                                  'Poopó',
                                  'Uros',
                                  'Taraco'],
                 'correcta': 'B'},
                {'pregunta': 'El único río efluente del lago Titicaca es el '
                             'río:',
                 'alternativas': ['Ramis',
                                  'Desaguadero',
                                  'Coata',
                                  'Ilave',
                                  'Suchez'],
                 'correcta': 'B'},
                {'pregunta': 'El río Desaguadero desemboca finalmente en el '
                             'lago:',
                 'alternativas': ['Titicaca',
                                  'Poopó',
                                  'Junín',
                                  'Chinchaycocha',
                                  'Parinacochas'],
                 'correcta': 'B'},
                {'pregunta': 'El río más extenso del Perú es el:',
                 'alternativas': ['Marañón',
                                  'Ucayali',
                                  'Amazonas',
                                  'Huallaga',
                                  'Mantaro'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo río más extenso del Perú es el:',
                 'alternativas': ['Ucayali',
                                  'Marañón',
                                  'Putumayo',
                                  'Yavarí',
                                  'Vilcanota'],
                 'correcta': 'B'},
                {'pregunta': 'El río Ramis, principal afluente del Titicaca, '
                             'tiene una longitud de:',
                 'alternativas': ['180 km',
                                  '304 km',
                                  '163 km',
                                  '500 km',
                                  '250 km'],
                 'correcta': 'B'},
                {'pregunta': 'El río Rímac nace en el nevado de:',
                 'alternativas': ['Huascarán',
                                  'Tíclio',
                                  'Coropuna',
                                  'Ausangate',
                                  'Salkantay'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['100 millas',
                                  '200 millas',
                                  '300 millas',
                                  '50 millas',
                                  '150 millas'],
                 'correcta': 'B'},
                {'pregunta': 'La extensión del mar peruano representa del '
                             'territorio peruano aproximadamente:',
                 'alternativas': ['50%', '90%', '30%', '70%', '20%'],
                 'correcta': 'B'},
                {'pregunta': 'Tras el fallo de la Corte de La Haya, el Perú '
                             'obtuvo adicionalmente:',
                 'alternativas': ['100 000 km²',
                                  '50 284 km²',
                                  '10 000 km²',
                                  '200 000 km²',
                                  '500 km²'],
                 'correcta': 'B'},
                {'pregunta': 'El mar peruano se distingue de otros por la '
                             'presencia de:',
                 'alternativas': ['Aguas cálidas todo el año',
                                  'La Corriente Peruana y la frialdad de sus '
                                  'aguas',
                                  'Ausencia de peces',
                                  'Escasa vida marina',
                                  'Aguas dulces'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina de las 200 millas fue proclamada '
                             'por Perú junto con Ecuador y:',
                 'alternativas': ['Bolivia',
                                  'Chile',
                                  'Colombia',
                                  'Brasil',
                                  'Argentina'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis de las 200 millas se declaró mediante '
                             'el D.S. N° 781 en el gobierno de:',
                 'alternativas': ['Manuel A. Odría',
                                  'José Bustamante y Rivero',
                                  'Fernando Belaunde',
                                  'Alan García',
                                  'Alberto Fujimori'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis de las 200 millas se proclamó en el '
                             'año:',
                 'alternativas': ['1930', '1947', '1960', '1980', '1993'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los fundamentos de la Tesis de las 200 '
                             'millas NO figura el fundamento:',
                 'alternativas': ['Geológico',
                                  'Biológico',
                                  'Estratégico',
                                  'Religioso',
                                  'Económico'],
                 'correcta': 'D'},
                {'pregunta': 'La región norte del mar peruano se extiende '
                             'desde la Península de Illescas hasta:',
                 'alternativas': ['Paracas',
                                  'Boca de Capones',
                                  'Tacna',
                                  'Ica',
                                  'Trujillo'],
                 'correcta': 'B'},
                {'pregunta': 'El color del mar en la región norte se debe '
                             'principalmente a:',
                 'alternativas': ['El plancton',
                                  'La descarga de los ríos',
                                  'Las algas',
                                  'La sal',
                                  'El afloramiento'],
                 'correcta': 'B'},
                {'pregunta': 'La temperatura promedio del mar en la región '
                             'central y sur es de:',
                 'alternativas': ['10°C', '18°C', '25°C', '5°C', '30°C'],
                 'correcta': 'B'},
                {'pregunta': 'El color verdoso del mar en la región central '
                             'y sur se debe a:',
                 'alternativas': ['La arena',
                                  'El plancton y las algas',
                                  'Los sedimentos fluviales',
                                  'La temperatura',
                                  'Las corrientes cálidas'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno del afloramiento consiste en:',
                 'alternativas': ['El hundimiento de aguas cálidas',
                                  'El ascenso de aguas frías hacia la '
                                  'superficie',
                                  'La formación de olas',
                                  'El derretimiento de glaciares',
                                  'La evaporación del mar'],
                 'correcta': 'B'},
                {'pregunta': 'La plataforma o zócalo continental llega hasta '
                             'la isóbata de:',
                 'alternativas': ['100 m',
                                  '200 m',
                                  '500 m',
                                  '1000 m',
                                  '50 m'],
                 'correcta': 'B'},
                {'pregunta': 'El talud continental se extiende entre las '
                             'isóbatas de:',
                 'alternativas': ['0 a 100 m',
                                  '200 a 5000 m',
                                  '500 a 1000 m',
                                  '5000 a 10000 m',
                                  '0 a 50 m'],
                 'correcta': 'B'},
                {'pregunta': 'Las fosas marinas se producen por:',
                 'alternativas': ['La erosión eólica',
                                  'La subducción de la Placa de Nasca',
                                  'El afloramiento',
                                  'Las corrientes marinas',
                                  'La sedimentación fluvial'],
                 'correcta': 'B'},
                {'pregunta': 'La Dorsal de Nasca es:',
                 'alternativas': ['Una fosa marina',
                                  'Una cordillera submarina volcánica',
                                  'Un golfo',
                                  'Una bahía',
                                  'Una península'],
                 'correcta': 'B'},
                {'pregunta': 'La Dorsal de Nasca se ubica aproximadamente a '
                             'qué distancia de la costa de Ica:',
                 'alternativas': ['50 km',
                                  '150 km',
                                  '500 km',
                                  '10 km',
                                  '300 km'],
                 'correcta': 'B'},
                {'pregunta': 'El fundamento geológico de la Tesis de las 200 '
                             'millas se refiere a:',
                 'alternativas': ['La riqueza pesquera',
                                  'La continuidad del zócalo continental',
                                  'La seguridad nacional',
                                  'El comercio marítimo',
                                  'El turismo'],
                 'correcta': 'B'},
                {'pregunta': 'La salinidad del mar en la región norte es de '
                             'aproximadamente:',
                 'alternativas': ['30 gr/l',
                                  '34 gr/l',
                                  '40 gr/l',
                                  '20 gr/l',
                                  '45 gr/l'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['La lluvia ácida',
                                  'Los rayos ultravioleta y meteoritos',
                                  'Los sismos',
                                  'Las mareas',
                                  'La erosión'],
                 'correcta': 'B'},
                {'pregunta': 'El gas más abundante de la atmósfera es:',
                 'alternativas': ['Oxígeno',
                                  'Nitrógeno',
                                  'Argón',
                                  'Dióxido de carbono',
                                  'Ozono'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo gas más abundante de la atmósfera '
                             'es:',
                 'alternativas': ['Nitrógeno',
                                  'Oxígeno',
                                  'Argón',
                                  'Neón',
                                  'Helio'],
                 'correcta': 'B'},
                {'pregunta': 'La capa inferior de la atmósfera, donde '
                             'ocurren los fenómenos meteorológicos, es:',
                 'alternativas': ['La estratósfera',
                                  'La tropósfera',
                                  'La mesósfera',
                                  'La termósfera',
                                  'La ionósfera'],
                 'correcta': 'B'},
                {'pregunta': 'La altitud promedio de la tropósfera es de:',
                 'alternativas': ['5 km',
                                  '12,5 km',
                                  '50 km',
                                  '90 km',
                                  '100 km'],
                 'correcta': 'B'},
                {'pregunta': 'En la tropósfera, la temperatura disminuye '
                             '0,6°C cada:',
                 'alternativas': ['10 m', '100 m', '1000 m', '50 m', '500 m'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno de disminución de temperatura con '
                             'la altitud en la tropósfera se llama:',
                 'alternativas': ['Inversión térmica',
                                  'Gradiente Térmico Vertical',
                                  'Efecto invernadero',
                                  'Capa de ozono',
                                  'Corriente de chorro'],
                 'correcta': 'B'},
                {'pregunta': 'La capa de ozono se ubica dentro de la:',
                 'alternativas': ['Tropósfera',
                                  'Estratósfera',
                                  'Mesósfera',
                                  'Termósfera',
                                  'Exósfera'],
                 'correcta': 'B'},
                {'pregunta': 'La capa de ozono se ubica entre los:',
                 'alternativas': ['0 y 10 km',
                                  '24 y 30 km',
                                  '50 y 90 km',
                                  '90 y 500 km',
                                  '10 y 20 km'],
                 'correcta': 'B'},
                {'pregunta': 'La función principal de la capa de ozono es:',
                 'alternativas': ['Producir lluvia',
                                  'Impedir el paso de los rayos ultravioleta',
                                  'Generar viento',
                                  'Formar nubes',
                                  'Regular la humedad'],
                 'correcta': 'B'},
                {'pregunta': 'En la estratósfera, la temperatura:',
                 'alternativas': ['Disminuye constantemente',
                                  'Aumenta progresivamente',
                                  'Se mantiene igual',
                                  'Baja a cero',
                                  'Fluctúa sin patrón'],
                 'correcta': 'B'},
                {'pregunta': 'La mesósfera se extiende entre:',
                 'alternativas': ['0 y 12,5 km',
                                  '50 y 90 km',
                                  '90 y 500 km',
                                  '12,5 y 50 km',
                                  '500 y 1000 km'],
                 'correcta': 'B'},
                {'pregunta': 'En la mesósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['0°C', '-110°C', '50°C', '100°C', '-50°C'],
                 'correcta': 'B'},
                {'pregunta': 'La termósfera o ionósfera se localiza entre:',
                 'alternativas': ['0 y 12,5 km',
                                  '50 y 90 km',
                                  '90 y 500 km',
                                  '12,5 y 50 km',
                                  '500 y 1000 km'],
                 'correcta': 'C'},
                {'pregunta': 'En la termósfera, la temperatura puede llegar '
                             'hasta:',
                 'alternativas': ['100°C',
                                  '800°C a 1500°C',
                                  '0°C',
                                  '-100°C',
                                  '300°C'],
                 'correcta': 'B'},
                {'pregunta': 'Las auroras polares se producen en:',
                 'alternativas': ['La tropósfera',
                                  'La termósfera',
                                  'La estratósfera',
                                  'La mesósfera',
                                  'La capa de ozono'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos de la termósfera se encuentran:',
                 'alternativas': ['Congelados',
                                  'Ionizados o electrizados',
                                  'Líquidos',
                                  'Sólidos',
                                  'Inertes'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los gases de efecto invernadero figura '
                             'principalmente:',
                 'alternativas': ['El nitrógeno',
                                  'El CO2',
                                  'El argón',
                                  'El neón',
                                  'El helio'],
                 'correcta': 'B'},
                {'pregunta': 'Sin la atmósfera, el paisaje terrestre sería '
                             'similar al de:',
                 'alternativas': ['Marte',
                                  'La Luna',
                                  'Venus',
                                  'Júpiter',
                                  'Saturno'],
                 'correcta': 'B'},
                {'pregunta': 'El límite final de la tropósfera se llama:',
                 'alternativas': ['Estratopausa',
                                  'Tropopausa',
                                  'Mesopausa',
                                  'Termopausa',
                                  'Ionopausa'],
                 'correcta': 'B'}]},
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
                                  'Ofrece la naturaleza espontáneamente',
                                  'Solo existen en la costa',
                                  'Son producidos por la industria',
                                  'Provienen únicamente del mar'],
                 'correcta': 'B'},
                {'pregunta': 'Los recursos que se agotan con el '
                             'aprovechamiento del hombre son los:',
                 'alternativas': ['Renovables',
                                  'No renovables',
                                  'Hídricos',
                                  'Marinos',
                                  'Forestales'],
                 'correcta': 'B'},
                {'pregunta': 'El petróleo y el gas son recursos naturales:',
                 'alternativas': ['Renovables',
                                  'No renovables',
                                  'Inagotables',
                                  'Ilimitados',
                                  'Reciclables'],
                 'correcta': 'B'},
                {'pregunta': 'El agua, el aire y el suelo son recursos '
                             'naturales:',
                 'alternativas': ['No renovables',
                                  'Renovables',
                                  'Escasos',
                                  'Artificiales',
                                  'Prohibidos'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el hombre aprovecha un recurso natural, '
                             'este se convierte en:',
                 'alternativas': ['Patrimonio intangible',
                                  'Recurso económico',
                                  'Bien público exclusivo',
                                  'Elemento sin valor',
                                  'Recurso prohibido'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las aves guaneras del mar peruano '
                             'figuran el guanay, piquero y:',
                 'alternativas': ['Cóndor',
                                  'Alcatraz',
                                  'Águila',
                                  'Gaviota andina',
                                  'Zorzal'],
                 'correcta': 'B'},
                {'pregunta': 'El hierro se explota principalmente en la '
                             'localidad de:',
                 'alternativas': ['Bayóvar',
                                  'Marcona',
                                  'Cerro de Pasco',
                                  'Toquepala',
                                  'Cajamarca'],
                 'correcta': 'B'},
                {'pregunta': 'Los fosfatos como fertilizante se explotan en:',
                 'alternativas': ['Marcona',
                                  'Bayóvar, Piura',
                                  'Cusco',
                                  'Puno',
                                  'Arequipa'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los minerales de la región andina '
                             'figuran el cobre, plomo, zinc, oro y:',
                 'alternativas': ['Petróleo',
                                  'Plata',
                                  'Gas natural',
                                  'Carbón vegetal',
                                  'Sal'],
                 'correcta': 'B'},
                {'pregunta': 'La vicuña, el cóndor y la chinchilla son fauna '
                             'representativa de:',
                 'alternativas': ['La costa',
                                  'La región andina',
                                  'El mar peruano',
                                  'La selva baja',
                                  'La selva alta'],
                 'correcta': 'B'},
                {'pregunta': 'De la selva se obtiene, entre otros recursos, '
                             'oro:',
                 'alternativas': ['En vetas superficiales',
                                  'Aluvial',
                                  'Solo en laboratorio',
                                  'Importado',
                                  'Sintético'],
                 'correcta': 'B'},
                {'pregunta': 'El SERNANP está adscrito al Ministerio de:',
                 'alternativas': ['Agricultura',
                                  'Ambiente',
                                  'Energía y Minas',
                                  'Cultura',
                                  'Educación'],
                 'correcta': 'B'},
                {'pregunta': 'El SERNANP fue creado mediante el Decreto '
                             'Legislativo:',
                 'alternativas': ['1013', '997', '1090', '713', '850'],
                 'correcta': 'A'},
                {'pregunta': 'El SERNANP fue creado en el año:',
                 'alternativas': ['1990', '2008', '2015', '1998', '2020'],
                 'correcta': 'B'},
                {'pregunta': 'Las Áreas Naturales Protegidas representan del '
                             'territorio nacional:',
                 'alternativas': ['5%', '15,41%', '30%', '50%', '2%'],
                 'correcta': 'B'},
                {'pregunta': 'En los Parques Nacionales solo se permite:',
                 'alternativas': ['La minería y agricultura',
                                  'El turismo e investigación científica',
                                  'La caza deportiva',
                                  'La tala de árboles',
                                  'La ganadería extensiva'],
                 'correcta': 'B'},
                {'pregunta': 'El parque nacional más pequeño y antiguo del '
                             'Perú es:',
                 'alternativas': ['Manu',
                                  'Cutervo',
                                  'Huascarán',
                                  'Bahuaja Sonene',
                                  'Tingo María'],
                 'correcta': 'B'},
                {'pregunta': 'El parque nacional más extenso del Perú es:',
                 'alternativas': ['Cutervo',
                                  'Huascarán',
                                  'Manu',
                                  'Río Abiseo',
                                  'Cerros de Amotape'],
                 'correcta': 'C'},
                {'pregunta': 'El parque nacional Manu se ubica entre Cusco '
                             'y:',
                 'alternativas': ['Puno',
                                  'Madre de Dios',
                                  'Apurímac',
                                  'Arequipa',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'El Parque Nacional Huascarán se ubica en el '
                             'departamento de:',
                 'alternativas': ['Cusco',
                                  'Áncash',
                                  'Cajamarca',
                                  'Puno',
                                  'Lima'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['29338',
                                  '29664',
                                  '27444',
                                  '30220',
                                  '28044'],
                 'correcta': 'B'},
                {'pregunta': 'El SINAGERD se caracteriza por ser un sistema:',
                 'alternativas': ['Centralizado y vertical',
                                  'Interinstitucional, descentralizado y '
                                  'participativo',
                                  'Exclusivamente militar',
                                  'Solo consultivo',
                                  'Sin participación ciudadana'],
                 'correcta': 'B'},
                {'pregunta': 'La Política Nacional de Gestión del Riesgo de '
                             'Desastres fue aprobada mediante:',
                 'alternativas': ['Una ley del Congreso',
                                  'El Decreto Supremo N° 111-2012-PCM',
                                  'Una ordenanza municipal',
                                  'Un decreto legislativo',
                                  'Una resolución ministerial'],
                 'correcta': 'B'},
                {'pregunta': 'Un fenómeno natural que ocurre en una zona '
                             'despoblada:',
                 'alternativas': ['Siempre es un desastre',
                                  'No representa necesariamente una amenaza',
                                  'Es automáticamente un riesgo alto',
                                  'Requiere evacuación inmediata',
                                  'Se clasifica como vulnerabilidad'],
                 'correcta': 'B'},
                {'pregunta': 'Un desastre se produce cuando:',
                 'alternativas': ['Ocurre un fenómeno en zona despoblada',
                                  'Se altera intensamente la vida cotidiana '
                                  'de una comunidad',
                                  'Solo hay pérdidas económicas menores',
                                  'No hay ningún efecto adverso',
                                  'El fenómeno es predecible'],
                 'correcta': 'B'},
                {'pregunta': 'El riesgo se calcula mediante la fórmula:',
                 'alternativas': ['Amenaza + Vulnerabilidad',
                                  'Amenaza × Vulnerabilidad',
                                  'Amenaza − Vulnerabilidad',
                                  'Amenaza ÷ Vulnerabilidad',
                                  'Vulnerabilidad ÷ Amenaza'],
                 'correcta': 'B'},
                {'pregunta': 'Para que exista riesgo se requiere la '
                             'presencia de:',
                 'alternativas': ['Solo la amenaza',
                                  'Amenaza y vulnerabilidad juntas',
                                  'Solo la vulnerabilidad',
                                  'Ningún factor en particular',
                                  'Solo fenómenos naturales extremos'],
                 'correcta': 'B'},
                {'pregunta': 'La amenaza se define como la probabilidad de '
                             'que ocurra:',
                 'alternativas': ['Una vulnerabilidad social',
                                  'Un fenómeno que pueda poner en peligro a '
                                  'las personas',
                                  'Un desastre ya consumado',
                                  'Una política pública',
                                  'Un cambio climático'],
                 'correcta': 'B'},
                {'pregunta': 'Las amenazas naturales se originan por:',
                 'alternativas': ['Acción humana exclusivamente',
                                  'La naturaleza misma',
                                  'Fallas de infraestructura',
                                  'Decisiones políticas',
                                  'El comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'La vulnerabilidad depende, entre otros '
                             'factores, de:',
                 'alternativas': ['Solo el clima',
                                  'La ubicación y tipo de vivienda',
                                  'Solo la economía nacional',
                                  'Solo la edad de la población',
                                  'Solo el idioma'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los objetivos de la política nacional de '
                             'gestión del riesgo figura:',
                 'alternativas': ['Eliminar los fenómenos naturales',
                                  'Fortalecer la cultura de prevención',
                                  'Evitar toda construcción',
                                  'Prohibir la habitación en zonas de riesgo',
                                  'Aumentar la vulnerabilidad'],
                 'correcta': 'B'},
                {'pregunta': 'Un terremoto en un área no poblada es un '
                             'ejemplo de:',
                 'alternativas': ['Desastre',
                                  'Fenómeno natural sin amenaza directa',
                                  'Riesgo alto',
                                  'Vulnerabilidad extrema',
                                  'Catástrofe social'],
                 'correcta': 'B'},
                {'pregunta': 'El riesgo representa la proximidad de:',
                 'alternativas': ['Un evento positivo',
                                  'Un daño potencial',
                                  'Una mejora económica',
                                  'Un fenómeno inexistente',
                                  'Una política pública exitosa'],
                 'correcta': 'B'},
                {'pregunta': 'Sin vulnerabilidad, una amenaza:',
                 'alternativas': ['Genera un desastre igual',
                                  'No representa un riesgo por sí sola',
                                  'Se convierte en catástrofe automática',
                                  'Aumenta exponencialmente',
                                  'Es imposible de medir'],
                 'correcta': 'B'},
                {'pregunta': 'El SINAGERD busca capacitar a los componentes '
                             'del sistema para:',
                 'alternativas': ['Evitar toda capacitación',
                                  'La toma de decisiones',
                                  'Reducir el presupuesto público',
                                  'Centralizar el poder',
                                  'Eliminar la participación privada'],
                 'correcta': 'B'},
                {'pregunta': 'Los fenómenos naturales pueden ser de orden '
                             'climatológico, hidrológico o:',
                 'alternativas': ['Económico',
                                  'Geológico',
                                  'Comercial',
                                  'Educativo',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'El SINAGERD tiene un carácter, entre otros, '
                             'transversal y:',
                 'alternativas': ['Exclusivo',
                                  'Participativo',
                                  'Cerrado',
                                  'Unipersonal',
                                  'Temporal'],
                 'correcta': 'B'},
                {'pregunta': 'El cálculo del riesgo puede incluir el número '
                             'de:',
                 'alternativas': ['Solo empresas afectadas',
                                  'Posibles vidas expuestas y viviendas que '
                                  'pueden perderse',
                                  'Solo turistas en la zona',
                                  'Solo funcionarios públicos',
                                  'Solo vehículos en circulación'],
                 'correcta': 'B'},
                {'pregunta': 'Una inundación en un lugar deshabitado se '
                             'considera:',
                 'alternativas': ['Un desastre mayor',
                                  'Un fenómeno natural, no una amenaza '
                                  'directa',
                                  'Un riesgo alto para la población',
                                  'Una catástrofe económica',
                                  'Una vulnerabilidad social'],
                 'correcta': 'B'},
                {'pregunta': 'La gestión del riesgo de desastres busca '
                             'minimizar los efectos adversos sobre:',
                 'alternativas': ['Solo la economía',
                                  'La población, la economía y el ambiente',
                                  'Solo el ambiente',
                                  'Solo el turismo',
                                  'Solo la infraestructura vial'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['La demografía',
                                  'La demogeografía',
                                  'La estadística',
                                  'La cartografía',
                                  'La geopolítica'],
                 'correcta': 'B'},
                {'pregunta': 'La demografía estudia estadísticamente la '
                             'estructura y dinámica de:',
                 'alternativas': ['Los ecosistemas',
                                  'Las poblaciones humanas',
                                  'El relieve terrestre',
                                  'Los climas',
                                  'Las corrientes marinas'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de natalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['6,2‰', '23,3‰', '50‰', '10‰', '1‰'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de mortalidad en el Perú es '
                             'aproximadamente de:',
                 'alternativas': ['23,3‰', '6,2‰', '15‰', '30‰', '2‰'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de crecimiento poblacional considera '
                             'nacimientos, muertes y:',
                 'alternativas': ['El clima',
                                  'La migración',
                                  'La religión',
                                  'El idioma',
                                  'La economía'],
                 'correcta': 'B'},
                {'pregunta': 'Según el INEI, la población del Perú al 2017 '
                             'superaba:',
                 'alternativas': ['20 millones',
                                  '31 237 385 habitantes',
                                  '50 millones',
                                  '10 millones',
                                  '40 millones'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo central y rector del Sistema '
                             'Estadístico Nacional del Perú es:',
                 'alternativas': ['El MEF',
                                  'El INEI',
                                  'El BCRP',
                                  'La SUNAT',
                                  'El MINEDU'],
                 'correcta': 'B'},
                {'pregunta': 'El INEI depende directamente de:',
                 'alternativas': ['El Congreso',
                                  'El Presidente del Consejo de Ministros',
                                  'El Poder Judicial',
                                  'El Ministerio de Economía',
                                  'La Presidencia de la República '
                                  'directamente'],
                 'correcta': 'B'},
                {'pregunta': 'El antecesor del INEI, creado en 1969, se '
                             'llamó:',
                 'alternativas': ['INE', 'ONEC', 'SUNAT', 'MEF', 'BCRP'],
                 'correcta': 'B'},
                {'pregunta': 'La población peruana se caracteriza por ser:',
                 'alternativas': ['Homogénea y monocultural',
                                  'Heterogénea, multirracial y multicultural',
                                  'Exclusivamente andina',
                                  'Solo urbana',
                                  'Sin diversidad lingüística'],
                 'correcta': 'B'},
                {'pregunta': 'La población peruana se concentra mayormente '
                             'en:',
                 'alternativas': ['La sierra',
                                  'La costa y zonas urbanas',
                                  'La selva',
                                  'Zonas fronterizas',
                                  'Zonas rurales exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La población nominal es:',
                 'alternativas': ['La estimada por proyección',
                                  'El número total de habitantes censados',
                                  'Solo la población rural',
                                  'Solo la población urbana',
                                  'La población futura'],
                 'correcta': 'B'},
                {'pregunta': 'La población que no se halla físicamente '
                             'durante el censo se llama:',
                 'alternativas': ['Población absoluta',
                                  'Población omitida',
                                  'Población relativa',
                                  'Población nominal',
                                  'Población flotante'],
                 'correcta': 'B'},
                {'pregunta': 'La población absoluta es:',
                 'alternativas': ['Solo un porcentaje',
                                  'La cantidad total de habitantes de una '
                                  'unidad geográfica',
                                  'Solo la densidad',
                                  'Solo la tasa de crecimiento',
                                  'Un promedio estimado'],
                 'correcta': 'B'},
                {'pregunta': 'La densidad de población también se llama:',
                 'alternativas': ['Población nominal',
                                  'Población relativa',
                                  'Población omitida',
                                  'Población flotante',
                                  'Población censada'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula de la población relativa es:',
                 'alternativas': ['Población absoluta × extensión '
                                  'territorial',
                                  'Población absoluta entre extensión '
                                  'territorial',
                                  'Extensión territorial entre población '
                                  'absoluta',
                                  'Población nominal más omitida',
                                  'Tasa de natalidad menos mortalidad'],
                 'correcta': 'B'},
                {'pregunta': 'Según el censo de 1940, la población del Perú '
                             'era de:',
                 'alternativas': ['10 420 357',
                                  '7 023 111',
                                  '14 121 564',
                                  '22 639 443',
                                  '28 220 764'],
                 'correcta': 'B'},
                {'pregunta': 'Según el censo de 2007, la población del Perú '
                             'era de:',
                 'alternativas': ['22 639 443',
                                  '28 220 764',
                                  '31 237 385',
                                  '17 762 231',
                                  '14 121 564'],
                 'correcta': 'B'},
                {'pregunta': 'La densidad poblacional del Perú en 2017 era '
                             'aproximadamente de:',
                 'alternativas': ['10 hab/km²',
                                  '24,3 hab/km²',
                                  '50 hab/km²',
                                  '5 hab/km²',
                                  '100 hab/km²'],
                 'correcta': 'B'},
                {'pregunta': 'La esperanza de vida en el Perú, según el '
                             'censo de 2007, fue de:',
                 'alternativas': ['55 años',
                                  '71,2 años',
                                  '35,6 años',
                                  '65 años',
                                  '80 años'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Reproductiva',
                                  'Extractiva',
                                  'Financiera',
                                  'Industrial exclusiva',
                                  'Comercial únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los factores de la riqueza ictiológica '
                             'del mar peruano figura:',
                 'alternativas': ['El agua cálida',
                                  'La frialdad de las aguas por la Corriente '
                                  'Peruana',
                                  'La escasez de plancton',
                                  'La ausencia de zócalo continental',
                                  'El agua dulce'],
                 'correcta': 'B'},
                {'pregunta': 'La especie más importante de la pesca marina '
                             'peruana es:',
                 'alternativas': ['El atún',
                                  'La anchoveta',
                                  'El bonito',
                                  'La caballa',
                                  'El jurel'],
                 'correcta': 'B'},
                {'pregunta': 'De la anchoveta se extrae principalmente:',
                 'alternativas': ['Aceite de oliva',
                                  'Harina y aceite de pescado',
                                  'Sal marina',
                                  'Perlas',
                                  'Conservas de lujo'],
                 'correcta': 'B'},
                {'pregunta': 'La anchoveta sirve de alimento principal para:',
                 'alternativas': ['Solo el ser humano',
                                  'Peces mayores y aves guaneras',
                                  'Solo mamíferos marinos',
                                  'Solo aves terrestres',
                                  'Ningún otro organismo'],
                 'correcta': 'B'},
                {'pregunta': 'El principal puerto pesquero del Perú, según '
                             'datos de 2018, fue:',
                 'alternativas': ['Callao',
                                  'Chimbote',
                                  'Paita',
                                  'Pisco',
                                  'Chancay'],
                 'correcta': 'B'},
                {'pregunta': 'En la selva, una técnica tradicional de pesca '
                             'es el uso de:',
                 'alternativas': ['Redes industriales',
                                  'Flecha y arpón',
                                  'Barcos factoría',
                                  'Sonar',
                                  'Trampas eléctricas'],
                 'correcta': 'B'},
                {'pregunta': 'El paiche se pesca principalmente en:',
                 'alternativas': ['El mar peruano',
                                  'Las cochas amazónicas',
                                  'El lago Titicaca',
                                  'Ríos de la costa',
                                  'Lagunas andinas'],
                 'correcta': 'B'},
                {'pregunta': 'El paiche se captura tradicionalmente con:',
                 'alternativas': ['Redes de arrastre',
                                  'Arpón',
                                  'Anzuelo eléctrico',
                                  'Trampas de metal',
                                  'Explosivos'],
                 'correcta': 'B'},
                {'pregunta': 'La pesca de camarón en la costa se realiza en '
                             'ríos de Arequipa, Lima e:',
                 'alternativas': ['Ica',
                                  'Tacna',
                                  'Piura',
                                  'Moquegua',
                                  'Tumbes'],
                 'correcta': 'A'},
                {'pregunta': 'En la región andina, la pesca se practica '
                             'principalmente en el lago:',
                 'alternativas': ['Junín',
                                  'Titicaca',
                                  'Parinacochas',
                                  'Chinchaycocha',
                                  'Sausacocha'],
                 'correcta': 'B'},
                {'pregunta': 'La principal especie de pesca en la región '
                             'andina es:',
                 'alternativas': ['El paiche',
                                  'La trucha',
                                  'La anchoveta',
                                  'El atún',
                                  'El camarón'],
                 'correcta': 'B'},
                {'pregunta': 'Los departamentos productores de trucha son '
                             'Puno, Huancavelica y:',
                 'alternativas': ['Cusco',
                                  'Junín',
                                  'Arequipa',
                                  'Tacna',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'Los impactos en la biodiversidad pesquera '
                             'provienen de la sobrepesca, la captura '
                             'incidental y:',
                 'alternativas': ['El turismo',
                                  'La degradación del hábitat',
                                  'El comercio justo',
                                  'La pesca artesanal exclusivamente',
                                  'La acuicultura'],
                 'correcta': 'B'},
                {'pregunta': 'El exceso de pesca causa principalmente:',
                 'alternativas': ['Aumento de especies',
                                  'Reducción de la existencia de especies',
                                  'Mejora del ecosistema',
                                  'Ningún efecto negativo',
                                  'Incremento de la biodiversidad'],
                 'correcta': 'B'},
                {'pregunta': 'La amplitud del zócalo continental favorece la '
                             'riqueza ictiológica porque facilita:',
                 'alternativas': ['El enfriamiento del agua',
                                  'La penetración de rayos solares',
                                  'La formación de olas',
                                  'La salinidad extrema',
                                  'El afloramiento volcánico'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno del afloramiento influye en la '
                             'pesca porque:',
                 'alternativas': ['Calienta el agua superficial',
                                  'Produce la frialdad característica del '
                                  'mar peruano',
                                  'Elimina el plancton',
                                  'Genera tsunamis',
                                  'Reduce el oxígeno del agua'],
                 'correcta': 'B'},
                {'pregunta': 'El zúngaro es una especie de pesca '
                             'característica de:',
                 'alternativas': ['El mar peruano',
                                  'La selva',
                                  'El lago Titicaca',
                                  'La costa sur',
                                  'Los Andes centrales'],
                 'correcta': 'B'},
                {'pregunta': 'El plancton constituye alimento fundamental '
                             'para:',
                 'alternativas': ['Solo el hombre',
                                  'Los peces del mar peruano',
                                  'Solo las aves',
                                  'Solo los mamíferos marinos',
                                  'Ningún organismo marino'],
                 'correcta': 'B'},
                {'pregunta': 'La pesca deportiva en la región andina se '
                             'realiza principalmente con:',
                 'alternativas': ['Redes industriales',
                                  'Anzuelos, redes y balsas',
                                  'Explosivos',
                                  'Barcos factoría',
                                  'Trampas eléctricas'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Extractiva',
                                  'Reproductiva',
                                  'Financiera',
                                  'Terciaria exclusiva',
                                  'Informal'],
                 'correcta': 'B'},
                {'pregunta': 'Los españoles introdujeron al Perú cultivos '
                             'como el arroz, cebada y:',
                 'alternativas': ['La papa',
                                  'La caña de azúcar',
                                  'La quinua',
                                  'El olluco',
                                  'El tarwi'],
                 'correcta': 'B'},
                {'pregunta': 'Según la FAO, el Perú tiene en cultivo '
                             'aproximadamente:',
                 'alternativas': ['1 millón de hectáreas',
                                  '4,4 millones de hectáreas',
                                  '10 millones de hectáreas',
                                  '500 mil hectáreas',
                                  '20 millones de hectáreas'],
                 'correcta': 'B'},
                {'pregunta': 'El área cultivada representa del territorio '
                             'nacional peruano aproximadamente:',
                 'alternativas': ['10%', '3,5%', '20%', '50%', '1%'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la costa se caracteriza por '
                             'ser:',
                 'alternativas': ['Extensiva y tradicional',
                                  'Intensiva, tecnificada y mecanizada',
                                  'Migratoria',
                                  'De subsistencia exclusiva',
                                  'Sin uso de maquinaria'],
                 'correcta': 'B'},
                {'pregunta': 'En la costa se pueden obtener anualmente:',
                 'alternativas': ['Una cosecha',
                                  'Hasta dos cosechas',
                                  'Tres cosechas mínimo',
                                  'Ninguna cosecha regular',
                                  'Cosechas cada dos años'],
                 'correcta': 'B'},
                {'pregunta': 'En la costa predominan los cultivos '
                             'industriales como la caña de azúcar y:',
                 'alternativas': ['La papa',
                                  'El algodón',
                                  'El olluco',
                                  'La cañihua',
                                  'La quinua'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la costa goza de asistencia:',
                 'alternativas': ['Militar',
                                  'Crediticia por bancos y entidades '
                                  'financieras',
                                  'Religiosa',
                                  'Solo comunal',
                                  'Internacional exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la región andina se '
                             'caracteriza por ser:',
                 'alternativas': ['Intensiva y mecanizada',
                                  'Extensiva y tradicional',
                                  'Industrial',
                                  'De exportación masiva',
                                  'Altamente tecnificada'],
                 'correcta': 'B'},
                {'pregunta': 'En la región andina, el cultivo se realiza '
                             'principalmente en época de:',
                 'alternativas': ['Sequía',
                                  'Lluvias',
                                  'Helada',
                                  'Granizo',
                                  'Neblina'],
                 'correcta': 'B'},
                {'pregunta': 'Una herramienta tradicional de la agricultura '
                             'andina es:',
                 'alternativas': ['El tractor',
                                  'La chaquitaclla',
                                  'La fumigadora',
                                  'La avioneta agrícola',
                                  'La bomba hidráulica'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura andina está orientada '
                             'principalmente al cultivo de productos de:',
                 'alternativas': ['Alta rentabilidad para exportación',
                                  'Baja rentabilidad, como papa, maíz y '
                                  'cebada',
                                  'Solo flores ornamentales',
                                  'Solo productos industriales',
                                  'Solo productos tropicales'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la selva se caracteriza por '
                             'ser:',
                 'alternativas': ['Intensiva y mecanizada',
                                  'Migratoria',
                                  'Exportadora exclusiva',
                                  'Altamente tecnificada',
                                  'Sin degradación de suelos'],
                 'correcta': 'B'},
                {'pregunta': 'La técnica de roce, tumba y quema se practica '
                             'en la agricultura de:',
                 'alternativas': ['La costa',
                                  'La selva',
                                  'La región andina alta',
                                  'El litoral',
                                  'Las lomas costeras'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los cultivos industriales de la selva '
                             'figuran la coca, el café y:',
                 'alternativas': ['El trigo',
                                  'El tabaco',
                                  'La cebada',
                                  'La papa',
                                  'El olluco'],
                 'correcta': 'B'},
                {'pregunta': 'En la selva alta existen valles permanentes de '
                             'cultivo como Jaén, Bagua y:',
                 'alternativas': ['Ica',
                                  'Chanchamayo',
                                  'Tacna',
                                  'Arequipa',
                                  'Piura'],
                 'correcta': 'B'},
                {'pregunta': 'La agricultura de la selva está relacionada '
                             'con la depredación de:',
                 'alternativas': ['El agua',
                                  'El suelo',
                                  'El aire',
                                  'Los minerales',
                                  'El mar'],
                 'correcta': 'B'},
                {'pregunta': 'En el antiguo Perú se cultivaba, entre otros '
                             'productos:',
                 'alternativas': ['Trigo y cebada',
                                  'Papa, quinua y oca',
                                  'Arroz y caña de azúcar',
                                  'Café y tabaco',
                                  'Algodón egipcio'],
                 'correcta': 'B'},
                {'pregunta': 'Las tierras aptas para cultivo en el Perú '
                             'alcanzan aproximadamente:',
                 'alternativas': ['1 millón de hectáreas',
                                  '7,6 millones de hectáreas',
                                  '20 millones de hectáreas',
                                  '500 mil hectáreas',
                                  '15 millones de hectáreas'],
                 'correcta': 'B'},
                {'pregunta': 'Un factor limitante de la agricultura en la '
                             'selva es:',
                 'alternativas': ['El exceso de tecnología',
                                  'La limitación en transporte y '
                                  'comercialización',
                                  'El exceso de crédito bancario',
                                  'La sobreproducción',
                                  'El exceso de maquinaria'],
                 'correcta': 'B'}]},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La geografía política estudia la organización '
                           'política y administrativa de {Los Estados de la '
                           'Tierra}.',
                           'El territorio de la República peruana está '
                           'integrado, según el artículo 189, por regiones, '
                           'departamentos, provincias y {Distritos}.',
                           'El Perú está dividido en un número de '
                           'departamentos igual a {24}.',
                           'Además de los departamentos, el Perú tiene una '
                           'provincia constitucional, que es {El Callao}.',
                           'El número total de distritos del Perú es '
                           'aproximadamente {1874}.',
                           'El departamento más extenso del Perú es '
                           '{Loreto}.',
                           'La capital del departamento de Loreto es '
                           '{Iquitos}.',
                           'El departamento de Cusco tiene una extensión '
                           'aproximada de {71 891 km²}.',
                           'El sistema donde el poder emana del gobierno '
                           'central se denomina {Centralismo}.',
                           'La descentralización está regulada en el '
                           'artículo de la Constitución número {188}.',
                           'Según el artículo 188, la descentralización es '
                           'una forma de organización {Democrática}.',
                           'La descentralización es considerada una política '
                           'permanente de carácter {Obligatorio}.',
                           'El proceso de descentralización se realiza {Por '
                           'etapas, en forma progresiva y ordenada}.',
                           'La descentralización implica la transferencia de '
                           'recursos del gobierno nacional hacia {Los '
                           'gobiernos regionales y locales}.',
                           'La regionalización busca la conformación de '
                           'regiones con autonomía {Administrativa, '
                           'económica y política}.',
                           'El objetivo fundamental de la descentralización '
                           'es {El desarrollo integral del país}.',
                           'La capital del departamento de Arequipa es '
                           '{Arequipa}.',
                           'La capital del departamento de Áncash es '
                           '{Huaraz}.',
                           'El departamento de Tumbes tiene una extensión '
                           'aproximada de {4 669 km²}.',
                           'En la provincia de La Convención, Cusco, se '
                           'crearon recientemente los distritos de Villa '
                           'Virgen, Villa Kintiarina, Incahuasi y '
                           '{Megantoni}.']}],
  'cuadros': [{'titulo': '17.2 DEPARTAMENTOS DESTACADOS DEL PERÚ',
               'encabezados': ['Departamento', 'Capital', 'Área km²'],
               'filas': [['{Loreto}', 'Iquitos', '368 851'],
                         ['{Cusco}', 'Cusco', '71 891'],
                         ['{Arequipa}', 'Arequipa', '63 345'],
                         ['{Lima}', 'Lima', '34 801'],
                         ['{Tumbes}', 'Tumbes', '4 669']]}],
  'preguntas': [{'pregunta': 'La geografía política estudia la organización '
                             'política y administrativa de:',
                 'alternativas': ['Solo el relieve',
                                  'Los Estados de la Tierra',
                                  'Solo el clima',
                                  'Solo los ríos',
                                  'Solo las ciudades'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio de la República peruana está '
                             'integrado, según el artículo 189, por '
                             'regiones, departamentos, provincias y:',
                 'alternativas': ['Comunidades',
                                  'Distritos',
                                  'Caseríos exclusivamente',
                                  'Centros poblados solamente',
                                  'Anexos'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú está dividido en un número de '
                             'departamentos igual a:',
                 'alternativas': ['25', '24', '30', '20', '28'],
                 'correcta': 'B'},
                {'pregunta': 'Además de los departamentos, el Perú tiene una '
                             'provincia constitucional, que es:',
                 'alternativas': ['Lima',
                                  'El Callao',
                                  'Arequipa',
                                  'Trujillo',
                                  'Cusco'],
                 'correcta': 'B'},
                {'pregunta': 'El número total de distritos del Perú es '
                             'aproximadamente:',
                 'alternativas': ['1000', '1874', '500', '2500', '800'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento más extenso del Perú es:',
                 'alternativas': ['Cusco',
                                  'Loreto',
                                  'Arequipa',
                                  'Puno',
                                  'Ucayali'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del departamento de Loreto es:',
                 'alternativas': ['Pucallpa',
                                  'Iquitos',
                                  'Moyobamba',
                                  'Tarapoto',
                                  'Yurimaguas'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento de Cusco tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['35 000 km²',
                                  '71 891 km²',
                                  '100 000 km²',
                                  '20 000 km²',
                                  '50 000 km²'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema donde el poder emana del gobierno '
                             'central se denomina:',
                 'alternativas': ['Descentralización',
                                  'Centralismo',
                                  'Regionalización',
                                  'Federalismo',
                                  'Municipalismo'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización está regulada en el '
                             'artículo de la Constitución número:',
                 'alternativas': ['189', '188', '201', '91', '24'],
                 'correcta': 'B'},
                {'pregunta': 'Según el artículo 188, la descentralización es '
                             'una forma de organización:',
                 'alternativas': ['Autoritaria',
                                  'Democrática',
                                  'Militar',
                                  'Monárquica',
                                  'Religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización es considerada una '
                             'política permanente de carácter:',
                 'alternativas': ['Opcional',
                                  'Obligatorio',
                                  'Temporal',
                                  'Regional exclusivo',
                                  'Provincial'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de descentralización se realiza:',
                 'alternativas': ['De forma inmediata y única',
                                  'Por etapas, en forma progresiva y '
                                  'ordenada',
                                  'Sin ningún criterio técnico',
                                  'Solo en Lima',
                                  'De manera aleatoria'],
                 'correcta': 'B'},
                {'pregunta': 'La descentralización implica la transferencia '
                             'de recursos del gobierno nacional hacia:',
                 'alternativas': ['Solo el sector privado',
                                  'Los gobiernos regionales y locales',
                                  'Organismos internacionales',
                                  'Solo las universidades',
                                  'Solo las Fuerzas Armadas'],
                 'correcta': 'B'},
                {'pregunta': 'La regionalización busca la conformación de '
                             'regiones con autonomía:',
                 'alternativas': ['Solo administrativa',
                                  'Administrativa, económica y política',
                                  'Solo económica',
                                  'Solo política',
                                  'Ninguna autonomía real'],
                 'correcta': 'B'},
                {'pregunta': 'El objetivo fundamental de la '
                             'descentralización es:',
                 'alternativas': ['Concentrar el poder en Lima',
                                  'El desarrollo integral del país',
                                  'Eliminar los gobiernos regionales',
                                  'Reducir la participación ciudadana',
                                  'Aumentar la burocracia central'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del departamento de Arequipa es:',
                 'alternativas': ['Mollendo',
                                  'Arequipa',
                                  'Camaná',
                                  'Chivay',
                                  'Islay'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del departamento de Áncash es:',
                 'alternativas': ['Chimbote',
                                  'Huaraz',
                                  'Casma',
                                  'Huarmey',
                                  'Recuay'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento de Tumbes tiene una extensión '
                             'aproximada de:',
                 'alternativas': ['4 669 km²',
                                  '15 000 km²',
                                  '50 000 km²',
                                  '1 000 km²',
                                  '100 000 km²'],
                 'correcta': 'A'},
                {'pregunta': 'En la provincia de La Convención, Cusco, se '
                             'crearon recientemente los distritos de Villa '
                             'Virgen, Villa Kintiarina, Incahuasi y:',
                 'alternativas': ['Ollantaytambo',
                                  'Megantoni',
                                  'Urubamba',
                                  'Calca',
                                  'Anta'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Nor-occidental del Perú',
                                  'Sur-oriental del Perú',
                                  'Centro-occidental del Perú',
                                  'Extremo norte del país',
                                  'Litoral del Perú'],
                 'correcta': 'B'},
                {'pregunta': 'La superficie del departamento del Cusco '
                             'representa del territorio nacional:',
                 'alternativas': ['1%', '5,6%', '15%', '20%', '10%'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más alto del departamento del Cusco '
                             'es el nevado:',
                 'alternativas': ['Salkantay',
                                  'Ausangate',
                                  'Veronica',
                                  'Chicón',
                                  'Huanacaure'],
                 'correcta': 'B'},
                {'pregunta': 'La altitud del nevado Ausangate es '
                             'aproximadamente de:',
                 'alternativas': ['5 000 m',
                                  '6 364 m',
                                  '4 500 m',
                                  '7 000 m',
                                  '5 800 m'],
                 'correcta': 'B'},
                {'pregunta': 'El punto más bajo del departamento del Cusco '
                             'se ubica en la provincia de:',
                 'alternativas': ['Urubamba',
                                  'La Convención',
                                  'Calca',
                                  'Quispicanchi',
                                  'Paucartambo'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco limita por el norte '
                             'con:',
                 'alternativas': ['Puno',
                                  'Ucayali',
                                  'Apurímac',
                                  'Arequipa',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco limita por el sur '
                             'con:',
                 'alternativas': ['Madre de Dios',
                                  'Arequipa',
                                  'Junín',
                                  'Ucayali',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco limita por el este y '
                             'sureste con:',
                 'alternativas': ['Apurímac',
                                  'Puno',
                                  'Junín',
                                  'Ayacucho',
                                  'Madre de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'La región andina o sierra representa del '
                             'territorio cusqueño:',
                 'alternativas': ['28%', '53%', '19%', '70%', '40%'],
                 'correcta': 'B'},
                {'pregunta': 'La selva alta o faja sub andina representa del '
                             'territorio del Cusco:',
                 'alternativas': ['53%', '28%', '19%', '10%', '5%'],
                 'correcta': 'B'},
                {'pregunta': 'La selva baja o llanura representa del '
                             'territorio cusqueño:',
                 'alternativas': ['53%', '28%', '19%', '40%', '70%'],
                 'correcta': 'C'},
                {'pregunta': 'El departamento del Cusco está dividido en un '
                             'número de provincias igual a:',
                 'alternativas': ['8', '13', '20', '10', '15'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco tiene un número de '
                             'distritos igual a:',
                 'alternativas': ['84', '112', '166', '65', '100'],
                 'correcta': 'B'},
                {'pregunta': 'La provincia más extensa del departamento del '
                             'Cusco es:',
                 'alternativas': ['Urubamba',
                                  'La Convención',
                                  'Calca',
                                  'Cusco',
                                  'Quispicanchi'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de la provincia de La Convención '
                             'es:',
                 'alternativas': ['Quillabamba',
                                  'Urubamba',
                                  'Calca',
                                  'Sicuani',
                                  'Yanaoca'],
                 'correcta': 'A'},
                {'pregunta': 'La provincia de La Convención representa del '
                             'área departamental del Cusco:',
                 'alternativas': ['10%', '41,52%', '5%', '20%', '70%'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de la provincia de Canchis es:',
                 'alternativas': ['Sicuani',
                                  'Yanaoca',
                                  'Espinar',
                                  'Acomayo',
                                  'Anta'],
                 'correcta': 'A'},
                {'pregunta': 'El distrito más poblado de la provincia del '
                             'Cusco, según el censo 2017, es:',
                 'alternativas': ['Wanchaq',
                                  'San Sebastián',
                                  'Santiago',
                                  'Poroy',
                                  'Saylla'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco se caracteriza por '
                             'ser un espacio geográfico:',
                 'alternativas': ['Homogéneo y uniforme',
                                  'Diverso en geomorfología, clima, suelo, '
                                  'flora y fauna',
                                  'Solo desértico',
                                  'Exclusivamente amazónico',
                                  'Sin variedad de pisos altitudinales'],
                 'correcta': 'B'},
                {'pregunta': 'El departamento del Cusco limita por el oeste '
                             'con:',
                 'alternativas': ['Apurímac',
                                  'Ayacucho',
                                  'Puno',
                                  'Arequipa',
                                  'Madre de Dios'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['África',
                                  'Asia',
                                  'Europa',
                                  'Oceanía',
                                  'Antártida'],
                 'correcta': 'B'},
                {'pregunta': 'América comprende tres fracciones unidas por:',
                 'alternativas': ['El Canal de Suez',
                                  'El Istmo de Panamá',
                                  'El Estrecho de Bering',
                                  'El Canal de Magallanes',
                                  'El Golfo de México'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema orográfico más importante de '
                             'América del Sur es:',
                 'alternativas': ['Las Rocosas',
                                  'La Cordillera de los Andes',
                                  'El Macizo Brasileño',
                                  'Los Apalaches',
                                  'La Sierra Madre'],
                 'correcta': 'B'},
                {'pregunta': 'El pico más elevado de América es el '
                             'Aconcagua, ubicado en:',
                 'alternativas': ['Chile',
                                  'Argentina',
                                  'Perú',
                                  'Bolivia',
                                  'Ecuador'],
                 'correcta': 'B'},
                {'pregunta': 'La altitud aproximada del Aconcagua es de:',
                 'alternativas': ['5 000 m',
                                  '6 960 m',
                                  '4 500 m',
                                  '7 500 m',
                                  '6 000 m'],
                 'correcta': 'B'},
                {'pregunta': 'América está dividida políticamente en un '
                             'número de países igual a:',
                 'alternativas': ['25', '35', '45', '20', '50'],
                 'correcta': 'B'},
                {'pregunta': 'América del Sur se extiende, por el sur, '
                             'hasta:',
                 'alternativas': ['Punta Gallinas',
                                  'La isla Diego Ramírez, Cabo de Hornos',
                                  'El Istmo de Panamá',
                                  'El río Amazonas',
                                  'El Macizo Brasileño'],
                 'correcta': 'B'},
                {'pregunta': 'El Macizo Brasileño se caracteriza por '
                             'presentar un relieve de:',
                 'alternativas': ['Alta montaña',
                                  'Meseta, de escasa elevación',
                                  'Fosas profundas',
                                  'Cordillera nevada',
                                  'Volcanes activos'],
                 'correcta': 'B'},
                {'pregunta': 'América del Sur posee del agua dulce del '
                             'planeta aproximadamente:',
                 'alternativas': ['10%', '26%', '50%', '5%', '70%'],
                 'correcta': 'B'},
                {'pregunta': 'El río más grande del planeta se ubica en:',
                 'alternativas': ['África',
                                  'Sudamérica',
                                  'Asia',
                                  'Norteamérica',
                                  'Europa'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de Brasil es:',
                 'alternativas': ['Río de Janeiro',
                                  'Brasilia',
                                  'São Paulo',
                                  'Salvador',
                                  'Belo Horizonte'],
                 'correcta': 'B'},
                {'pregunta': 'La moneda de Brasil es el:',
                 'alternativas': ['Peso',
                                  'Real',
                                  'Dólar',
                                  'Bolívar',
                                  'Guaraní'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de Argentina es:',
                 'alternativas': ['Córdoba',
                                  'Buenos Aires',
                                  'Rosario',
                                  'Mendoza',
                                  'La Plata'],
                 'correcta': 'B'},
                {'pregunta': 'La moneda del Perú es:',
                 'alternativas': ['El Peso',
                                  'El Nuevo Sol',
                                  'El Dólar',
                                  'El Bolívar',
                                  'El Real'],
                 'correcta': 'B'},
                {'pregunta': 'Bolivia tiene como capital constitucional a:',
                 'alternativas': ['La Paz',
                                  'Sucre',
                                  'Santa Cruz',
                                  'Cochabamba',
                                  'Potosí'],
                 'correcta': 'B'},
                {'pregunta': 'La sede de gobierno de Bolivia es:',
                 'alternativas': ['Sucre',
                                  'La Paz',
                                  'Santa Cruz',
                                  'Cochabamba',
                                  'Oruro'],
                 'correcta': 'B'},
                {'pregunta': 'La actividad económica principal de Chile, '
                             'según la tabla, es:',
                 'alternativas': ['Agricultura',
                                  'Minería',
                                  'Ganadería',
                                  'Pesca exclusiva',
                                  'Turismo'],
                 'correcta': 'B'},
                {'pregunta': 'La actividad económica principal de Venezuela '
                             'es:',
                 'alternativas': ['Agricultura',
                                  'Minería (petróleo)',
                                  'Ganadería',
                                  'Turismo',
                                  'Pesca'],
                 'correcta': 'B'},
                {'pregunta': 'La moneda de Colombia es el:',
                 'alternativas': ['Peso',
                                  'Bolívar',
                                  'Sol',
                                  'Guaraní',
                                  'Real'],
                 'correcta': 'A'},
                {'pregunta': 'El río Orinoco y el río Paraná, junto con el '
                             'Amazonas, se caracterizan por ser:',
                 'alternativas': ['Ríos cortos y de bajo caudal',
                                  'Ríos extensos y caudalosos',
                                  'Ríos estacionales secos',
                                  'Ríos artificiales',
                                  'Ríos de agua salada'],
                 'correcta': 'B'}]}]


# ================================================================
# INTERFAZ
# ================================================================

def _tema_completo_geografia(preguntas=False):
    """Fusiona todos los temas cargados en un solo documento imprimible."""
    secs, cuadros, pregs = [], [], []
    for t in GEOGRAFIA_TEMAS:
        for s in t.get("secciones", []):
            secs.append({"titulo": f"T{t['num']}. {s['titulo']}",
                         "items": s["items"]})
        for c in t.get("cuadros", []):
            cuadros.append({"titulo": f"T{t['num']}. {c['titulo']}",
                            "encabezados": c["encabezados"],
                            "filas": c["filas"]})
        if preguntas:
            for p in balancear(t["preguntas"]):
                pregs.append({**p,
                              "pregunta": f"(T{t['num']}) {p['pregunta']}"})
    return {"num": f"1–{len(GEOGRAFIA_TEMAS)}",
            "titulo": "TEMARIO DE GEOGRAFÍA",
            "secciones": secs, "cuadros": cuadros, "preguntas": pregs}


def tab_fichas_geografia(config=None):
    st.subheader("🌎 Geografía — Fichas y banco de preguntas (CEPRU)")
    st.caption("Temario oficial de Geografía del Perú y del Mundo, Área D "
               f"— {len(GEOGRAFIA_TEMAS)} de 18 temas cargados por ahora. "
               "Cada uno genera cuatro documentos.")

    opciones = {f"Tema {t['num']} — {t['titulo']}": t for t in GEOGRAFIA_TEMAS}
    sel = st.selectbox("Tema:", list(opciones.keys()), key="fg_sel")
    tema = opciones[sel]

    c1, c2, c3 = st.columns(3)
    c1.metric("Espacios para completar", contar_espacios(tema))
    c2.metric("Preguntas", len(tema["preguntas"]))
    c3.metric("Cuadros", len(tema.get("cuadros", [])))

    grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                              placeholder="GRUPO CD", key="fg_grado")

    st.markdown("##### Descargar")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt, area="Geografía"),
                file_name=f"geografia_tema{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fg_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt, area="Geografía"),
                file_name=f"geografia_tema{tema['num']}_docente.pdf",
                mime="application/pdf", use_container_width=True, key="fg_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de 20 preguntas**")
        try:
            tema_b = {**tema, "preguntas": balancear(tema["preguntas"])}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt, area="Geografía"),
                file_name=f"geografia_preguntas{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fg_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt, area="Geografía"),
                file_name=f"geografia_preguntas{tema['num']}_claves.pdf",
                mime="application/pdf", use_container_width=True, key="fg_pd")
        except Exception as e:
            st.error(f"No se pudo generar el banco: {e}")

    st.markdown("---")
    st.markdown("##### Descargar el temario completo (temas cargados)")
    g1, g2 = st.columns(2)
    with g1:
        if st.button("📚 Todas las fichas cargadas",
                     use_container_width=True, key="fg_todas_f"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["fg_pdf"] = generar_ficha_texto(
                        _tema_completo_geografia(), False, grado_txt,
                        area="Geografía")
                    st.session_state["fg_nom"] = "geografia_fichas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")
    with g2:
        if st.button("📚 Todos los bancos cargados",
                     use_container_width=True, key="fg_todas_p"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["fg_pdf"] = generar_banco_preguntas(
                        _tema_completo_geografia(preguntas=True), False, grado_txt,
                        area="Geografía")
                    st.session_state["fg_nom"] = "geografia_preguntas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.get("fg_pdf"):
        st.download_button(
            "⬇️ Descargar documento completo",
            data=st.session_state["fg_pdf"],
            file_name=st.session_state.get("fg_nom", "geografia.pdf"),
            mime="application/pdf", use_container_width=True, key="fg_dl")

    with st.expander("Ver el contenido de este tema"):
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
