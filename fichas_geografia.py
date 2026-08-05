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
