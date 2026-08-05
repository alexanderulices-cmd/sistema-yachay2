# ================================================================
# FICHAS DE BIOLOGÍA — CEPRU UNSAAC
# Basado en el material oficial «Biología», Área B.
# ================================================================
"""Mismo formato que Historia: por cada balota, ficha de texto para
completar a dos columnas y banco de 20 preguntas, en versión alumno y
versión docente. Reutiliza el motor de fichas_historia.py.

ESTADO: 2 de 16 temas completos. Los 14 restantes se agregan por
tandas, igual que se hizo con Geografía, Cívica, Comunicativa y
Economía.

Integración: se usa a través de academia_cepru.py, no directamente.
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


BIOLOGIA_TEMAS = [{'num': 1,
  'titulo': 'Concepto de Biología y Niveles de Organización',
  'secciones': [{'titulo': '1.1 DEFINICIÓN DE BIOLOGÍA',
                 'items': ['Etimológicamente, «biología» deriva de las '
                           'raíces griegas «{bios}» (vida) y «{logos}» '
                           '(tratado o estudio).',
                           'La biología es la ciencia que estudia a los '
                           '{seres vivos}, su origen, evolución, '
                           'clasificación, estructura, función y {herencia}.',
                           'La biología también estudia la interacción de '
                           'los organismos entre sí y con el {ambiente}.']},
                {'titulo': '1.2 RELACIÓN CON OTRAS CIENCIAS',
                 'items': ['La unión de la física y la biología da origen a '
                           'la {biofísica}, que estudia la estructura de los '
                           'seres vivos.',
                           'La {astrofísica} ayuda a comprender el origen de '
                           'la vida en el planeta, a través del estudio del '
                           'universo.',
                           'La {bioquímica} aporta las bases del '
                           'conocimiento de la estructura de la materia '
                           '{viva}.',
                           'La {bioestadística} surge de la relación entre '
                           'la biología y las {matemáticas}.']},
                {'titulo': '1.3 NIVEL QUÍMICO DE ORGANIZACIÓN',
                 'items': ['El nivel {subatómico} está formado por protón, '
                           'neutrón y electrón.',
                           'El nivel {atómico} es la unidad más pequeña de '
                           'un elemento químico, como H, C, N, O.',
                           'Las {macromoléculas} tienen un peso de miles de '
                           'daltons y resultan de la unión de unidades '
                           '{monoméricas}.',
                           'El nivel de {complejos supramoleculares}, o '
                           'nivel prebiótico, incluye virus, ribosomas y '
                           'glucoproteínas.',
                           'Los {orgánulos celulares}, u organelos, incluyen '
                           'la membrana plasmática, mitocondrias y '
                           'cloroplastos, y aún no cumplen funciones de ser '
                           'vivo.']},
                {'titulo': '1.4 NIVEL BIOLÓGICO DE ORGANIZACIÓN',
                 'items': ['El nivel {celular} es la unidad mínima de la '
                           'materia viva; los organismos formados por muchas '
                           'células son {pluricelulares}.',
                           'A partir de la {especie} siguen los niveles de '
                           'organización ecológica: población, comunidad, '
                           'ecosistema, bioma y {biosfera}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Etimológicamente, «biología» proviene de las '
                           'raíces griegas «bios» y {Logos}.',
                           'La raíz griega «bios» significa {Vida}.',
                           'La biología es la ciencia que estudia {Los seres '
                           'vivos}.',
                           'El estudio de la biología comprende el origen, '
                           'evolución, clasificación, estructura, función y '
                           '{Herencia}.',
                           'La rama que surge de la unión de la física y la '
                           'biología se llama {Biofísica}.',
                           'La biofísica aplica los principios de la física '
                           'para estudiar {La estructura de los seres '
                           'vivos}.',
                           'La rama que aporta las bases del conocimiento de '
                           'la estructura de la materia viva es la '
                           '{Bioquímica}.',
                           'La rama que surge de la relación entre biología '
                           'y matemáticas se llama {Bioestadística}.',
                           'El nivel formado por protón, neutrón y electrón '
                           'se llama nivel {Subatómico}.',
                           'El átomo se define como la unidad más pequeña de '
                           '{Un elemento químico}.',
                           'Las moléculas con un peso de miles de daltons, '
                           'formadas por unidades monoméricas, se llaman '
                           '{Macromoléculas}.',
                           'El almidón es un polímero de glucosa, mientras '
                           'que las proteínas son polímeros de '
                           '{Aminoácidos}.',
                           'El nivel de complejos supramoleculares también '
                           'se conoce como nivel {Prebiótico}.',
                           'Los virus, ribosomas y glucoproteínas son '
                           'ejemplos del nivel {Supramolecular}.',
                           'Los orgánulos celulares, como las mitocondrias, '
                           'no se consideran seres vivos porque {No cumplen '
                           'las funciones de nutrición, relación y '
                           'reproducción}.',
                           'La unidad mínima de la materia viva es {La '
                           'célula}.',
                           'Los organismos formados por muchas células se '
                           'denominan {Pluricelulares}.',
                           'A partir de la especie, comienzan los niveles de '
                           'organización {Ecológicos}.',
                           'Los niveles de organización ecológica incluyen '
                           'población, comunidad, ecosistema, bioma y '
                           '{Biosfera}.',
                           'Los niveles de organización permiten, entre '
                           'otras cosas {Establecer límites y ordenar '
                           'conceptos}.']}],
  'cuadros': [{'titulo': '1.3 NIVEL QUÍMICO DE ORGANIZACIÓN',
               'encabezados': ['Nivel', 'Ejemplo'],
               'filas': [['{Partícula subatómica}',
                          'Protón, {neutrón}, electrón'],
                         ['{Átomo}', 'H, C, N, O, {P}, S'],
                         ['{Macromolécula}',
                          'Carbohidratos, {lípidos}, proteínas'],
                         ['{Supramolécula}', '{Virus}, ribosomas']]}],
  'preguntas': [{'pregunta': 'Etimológicamente, «biología» proviene de las '
                             'raíces griegas «bios» y:',
                 'alternativas': ['Genos', 'Logos', 'Physis', 'Soma', 'Zoon'],
                 'correcta': 'B'},
                {'pregunta': 'La raíz griega «bios» significa:',
                 'alternativas': ['Estudio',
                                  'Vida',
                                  'Origen',
                                  'Célula',
                                  'Materia'],
                 'correcta': 'B'},
                {'pregunta': 'La biología es la ciencia que estudia:',
                 'alternativas': ['Solo la materia inerte',
                                  'Los seres vivos',
                                  'Solo los minerales',
                                  'Solo el universo',
                                  'Solo las estrellas'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio de la biología comprende el origen, '
                             'evolución, clasificación, estructura, función '
                             'y:',
                 'alternativas': ['Comercio',
                                  'Herencia',
                                  'Economía',
                                  'Política',
                                  'Religión'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la unión de la física y '
                             'la biología se llama:',
                 'alternativas': ['Bioquímica',
                                  'Biofísica',
                                  'Bioestadística',
                                  'Astrobiología',
                                  'Geología'],
                 'correcta': 'B'},
                {'pregunta': 'La biofísica aplica los principios de la '
                             'física para estudiar:',
                 'alternativas': ['Solo el universo',
                                  'La estructura de los seres vivos',
                                  'Solo la economía',
                                  'Solo la historia',
                                  'Solo el clima'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que aporta las bases del conocimiento '
                             'de la estructura de la materia viva es la:',
                 'alternativas': ['Biofísica',
                                  'Bioquímica',
                                  'Bioestadística',
                                  'Astrofísica',
                                  'Geología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la relación entre '
                             'biología y matemáticas se llama:',
                 'alternativas': ['Bioquímica',
                                  'Bioestadística',
                                  'Biofísica',
                                  'Biogeografía',
                                  'Bioética'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel formado por protón, neutrón y '
                             'electrón se llama nivel:',
                 'alternativas': ['Atómico',
                                  'Subatómico',
                                  'Molecular',
                                  'Celular',
                                  'Macromolecular'],
                 'correcta': 'B'},
                {'pregunta': 'El átomo se define como la unidad más pequeña '
                             'de:',
                 'alternativas': ['Una célula',
                                  'Un elemento químico',
                                  'Un organismo',
                                  'Un ecosistema',
                                  'Una molécula orgánica'],
                 'correcta': 'B'},
                {'pregunta': 'Las moléculas con un peso de miles de daltons, '
                             'formadas por unidades monoméricas, se llaman:',
                 'alternativas': ['Átomos',
                                  'Macromoléculas',
                                  'Partículas subatómicas',
                                  'Organelos',
                                  'Ecosistemas'],
                 'correcta': 'B'},
                {'pregunta': 'El almidón es un polímero de glucosa, mientras '
                             'que las proteínas son polímeros de:',
                 'alternativas': ['Nucleótidos',
                                  'Aminoácidos',
                                  'Lípidos',
                                  'Glúcidos',
                                  'Iones'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel de complejos supramoleculares también '
                             'se conoce como nivel:',
                 'alternativas': ['Atómico',
                                  'Prebiótico',
                                  'Celular',
                                  'Ecológico',
                                  'Orgánico'],
                 'correcta': 'B'},
                {'pregunta': 'Los virus, ribosomas y glucoproteínas son '
                             'ejemplos del nivel:',
                 'alternativas': ['Atómico',
                                  'Supramolecular',
                                  'Celular',
                                  'Ecológico',
                                  'Orgánico'],
                 'correcta': 'B'},
                {'pregunta': 'Los orgánulos celulares, como las '
                             'mitocondrias, no se consideran seres vivos '
                             'porque:',
                 'alternativas': ['No tienen forma definida',
                                  'No cumplen las funciones de nutrición, '
                                  'relación y reproducción',
                                  'Son demasiado pequeños',
                                  'No contienen materia orgánica',
                                  'No están formados por moléculas'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad mínima de la materia viva es:',
                 'alternativas': ['El átomo',
                                  'La célula',
                                  'La molécula',
                                  'El tejido',
                                  'El órgano'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos formados por muchas células se '
                             'denominan:',
                 'alternativas': ['Unicelulares',
                                  'Pluricelulares',
                                  'Acelulares',
                                  'Procariontes exclusivamente',
                                  'Virales'],
                 'correcta': 'B'},
                {'pregunta': 'A partir de la especie, comienzan los niveles '
                             'de organización:',
                 'alternativas': ['Químicos',
                                  'Ecológicos',
                                  'Subatómicos',
                                  'Moleculares',
                                  'Celulares exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los niveles de organización ecológica incluyen '
                             'población, comunidad, ecosistema, bioma y:',
                 'alternativas': ['Órgano',
                                  'Biosfera',
                                  'Tejido',
                                  'Célula',
                                  'Molécula'],
                 'correcta': 'B'},
                {'pregunta': 'Los niveles de organización permiten, entre '
                             'otras cosas:',
                 'alternativas': ['Eliminar el estudio sistemático',
                                  'Establecer límites y ordenar conceptos',
                                  'Confundir la clasificación',
                                  'Ignorar la complejidad biológica',
                                  'Evitar el análisis científico'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'Composición Química de la Materia Viviente',
  'secciones': [{'titulo': '2.1 BIOELEMENTOS',
                 'items': ['La materia está formada por {118} elementos '
                           'químicos, de los cuales {92} son naturales.',
                           'Los seres vivos están constituidos por {40} '
                           'elementos en cantidades variables.',
                           'Los {bioelementos} son elementos químicos '
                           'presentes en los organismos vivos; {20} de ellos '
                           'son biogenésicos.',
                           'Los bioelementos se clasifican en '
                           '{macroelementos} (primarios y secundarios) y '
                           '{microelementos} u oligoelementos.']},
                {'titulo': '2.2 BIOELEMENTOS PRIMARIOS',
                 'items': ['Los macroelementos representan el {99,6}% de la '
                           'materia viva, y están conformados por {11} '
                           'bioelementos.',
                           'Los bioelementos {primarios} son seis: carbono, '
                           'hidrógeno, oxígeno, nitrógeno, {fósforo} y '
                           'azufre, llamados organógenos.',
                           'Los primeros cuatro bioelementos primarios '
                           'representan el {96}% de la materia viva.',
                           'El {carbono} es la piedra angular en la '
                           'construcción de moléculas biológicas.',
                           'El {oxígeno} es el elemento más abundante en la '
                           'naturaleza y forma parte de la molécula del '
                           '{agua}.',
                           'El {nitrógeno} forma las proteínas, esenciales '
                           'para el crecimiento de los seres vivos.',
                           'El {fósforo} desempeña un papel esencial en la '
                           'transferencia de energía, como en el {ATP}.',
                           'El {azufre} forma parte de aminoácidos como la '
                           'metionina y la {cisteína}.']},
                {'titulo': '2.3 BIOELEMENTOS SECUNDARIOS',
                 'items': ['Los bioelementos {secundarios} son cinco: sodio, '
                           'potasio, calcio, magnesio y {cloro}.',
                           'El {sodio} es el principal ión positivo del '
                           'líquido intersticial, esencial en la conducción '
                           'de impulsos {nerviosos}.',
                           'El {potasio} es el principal catión del interior '
                           'de las {células}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La materia está formada por un total de '
                           'elementos químicos igual a {118}.',
                           'De los elementos químicos existentes, los que '
                           'son naturales suman {92}.',
                           'Los seres vivos están constituidos por un número '
                           'de elementos igual a {92}.',
                           'Los bioelementos se clasifican en macroelementos '
                           'y {Microelementos u oligoelementos}.',
                           'Los macroelementos representan de la materia '
                           'viva aproximadamente {99,6%}.',
                           'Los bioelementos primarios, también llamados '
                           'organógenos, suman un total de {Seis}.',
                           'Los cuatro bioelementos primarios más abundantes '
                           'representan de la materia viva {96%}.',
                           'El elemento considerado la piedra angular en la '
                           'construcción de moléculas biológicas es {El '
                           'carbono}.',
                           'El elemento más abundante en la naturaleza, que '
                           'forma parte del agua, es {El oxígeno}.',
                           'El elemento que forma las proteínas, esenciales '
                           'para el crecimiento, es {El nitrógeno}.',
                           'El elemento que desempeña un papel esencial en '
                           'la transferencia de energía, como en el ATP, es '
                           '{El fósforo}.',
                           'El elemento que forma parte de aminoácidos como '
                           'la metionina y la cisteína es {El azufre}.',
                           'Los bioelementos secundarios son cinco: sodio, '
                           'potasio, calcio, magnesio y {Cloro}.',
                           'El principal ión positivo del líquido '
                           'intersticial, esencial para impulsos nerviosos, '
                           'es {El sodio}.',
                           'El principal catión del interior de las células '
                           'es {El potasio}.',
                           'El hidrógeno es considerado el elemento {Más '
                           'liviano que existe en la naturaleza}.',
                           'El fósforo forma parte de los fosfolípidos que '
                           'se encuentran en {Las membranas celulares}.',
                           'El azufre se encuentra, entre otros lugares, en '
                           'la bilis, el cartílago y {Las glándulas '
                           'suprarrenales}.',
                           'El nitrógeno también forma parte de compuestos '
                           'como {Los fertilizantes}.',
                           'Los bioelementos secundarios son necesarios para '
                           'las células en cantidades {Más pequeñas que los '
                           'primarios}.']}],
  'cuadros': [{'titulo': '2.2 LOS SEIS BIOELEMENTOS PRIMARIOS (ORGANÓGENOS)',
               'encabezados': ['Elemento', 'Símbolo', 'Función principal'],
               'filas': [['{Carbono}', 'C', 'Base de moléculas {biológicas}'],
                         ['{Hidrógeno}', 'H', 'Componente {estructural}'],
                         ['{Oxígeno}', 'O', 'Forma parte del {agua}'],
                         ['{Nitrógeno}', 'N', 'Forma {proteínas}'],
                         ['{Fósforo}', 'P', 'Transferencia de {energía}'],
                         ['{Azufre}', 'S', 'Forma {aminoácidos}']]}],
  'preguntas': [{'pregunta': 'La materia está formada por un total de '
                             'elementos químicos igual a:',
                 'alternativas': ['92', '118', '40', '20', '11'],
                 'correcta': 'B'},
                {'pregunta': 'De los elementos químicos existentes, los que '
                             'son naturales suman:',
                 'alternativas': ['118', '92', '40', '20', '6'],
                 'correcta': 'B'},
                {'pregunta': 'Los seres vivos están constituidos por un '
                             'número de elementos igual a:',
                 'alternativas': ['118', '92', '40', '20', '6'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos se clasifican en '
                             'macroelementos y:',
                 'alternativas': ['Bioelementos primarios exclusivamente',
                                  'Microelementos u oligoelementos',
                                  'Solo minerales',
                                  'Solo orgánicos',
                                  'Solo inorgánicos'],
                 'correcta': 'B'},
                {'pregunta': 'Los macroelementos representan de la materia '
                             'viva aproximadamente:',
                 'alternativas': ['50%', '99,6%', '10%', '75%', '25%'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos primarios, también llamados '
                             'organógenos, suman un total de:',
                 'alternativas': ['Cuatro',
                                  'Seis',
                                  'Once',
                                  'Cinco',
                                  'Veinte'],
                 'correcta': 'B'},
                {'pregunta': 'Los cuatro bioelementos primarios más '
                             'abundantes representan de la materia viva:',
                 'alternativas': ['50%', '96%', '20%', '75%', '10%'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento considerado la piedra angular en '
                             'la construcción de moléculas biológicas es:',
                 'alternativas': ['El oxígeno',
                                  'El carbono',
                                  'El nitrógeno',
                                  'El azufre',
                                  'El fósforo'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento más abundante en la naturaleza, '
                             'que forma parte del agua, es:',
                 'alternativas': ['El carbono',
                                  'El oxígeno',
                                  'El nitrógeno',
                                  'El hidrógeno',
                                  'El fósforo'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que forma las proteínas, '
                             'esenciales para el crecimiento, es:',
                 'alternativas': ['El carbono',
                                  'El nitrógeno',
                                  'El oxígeno',
                                  'El azufre',
                                  'El fósforo'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que desempeña un papel esencial en '
                             'la transferencia de energía, como en el ATP, '
                             'es:',
                 'alternativas': ['El nitrógeno',
                                  'El fósforo',
                                  'El carbono',
                                  'El hidrógeno',
                                  'El azufre'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que forma parte de aminoácidos '
                             'como la metionina y la cisteína es:',
                 'alternativas': ['El fósforo',
                                  'El azufre',
                                  'El nitrógeno',
                                  'El carbono',
                                  'El oxígeno'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos secundarios son cinco: sodio, '
                             'potasio, calcio, magnesio y:',
                 'alternativas': ['Fósforo',
                                  'Cloro',
                                  'Azufre',
                                  'Carbono',
                                  'Nitrógeno'],
                 'correcta': 'B'},
                {'pregunta': 'El principal ión positivo del líquido '
                             'intersticial, esencial para impulsos '
                             'nerviosos, es:',
                 'alternativas': ['El potasio',
                                  'El sodio',
                                  'El calcio',
                                  'El magnesio',
                                  'El cloro'],
                 'correcta': 'B'},
                {'pregunta': 'El principal catión del interior de las '
                             'células es:',
                 'alternativas': ['El sodio',
                                  'El potasio',
                                  'El calcio',
                                  'El cloro',
                                  'El magnesio'],
                 'correcta': 'B'},
                {'pregunta': 'El hidrógeno es considerado el elemento:',
                 'alternativas': ['Más pesado de la naturaleza',
                                  'Más liviano que existe en la naturaleza',
                                  'Menos abundante',
                                  'Exclusivo de las plantas',
                                  'Sin relación con la vida'],
                 'correcta': 'B'},
                {'pregunta': 'El fósforo forma parte de los fosfolípidos que '
                             'se encuentran en:',
                 'alternativas': ['Las paredes celulares vegetales '
                                  'exclusivamente',
                                  'Las membranas celulares',
                                  'Solo el núcleo celular',
                                  'Solo el citoplasma',
                                  'Solo los ribosomas'],
                 'correcta': 'B'},
                {'pregunta': 'El azufre se encuentra, entre otros lugares, '
                             'en la bilis, el cartílago y:',
                 'alternativas': ['Los huesos exclusivamente',
                                  'Las glándulas suprarrenales',
                                  'Solo los dientes',
                                  'Solo el cabello',
                                  'Solo las uñas'],
                 'correcta': 'B'},
                {'pregunta': 'El nitrógeno también forma parte de compuestos '
                             'como:',
                 'alternativas': ['Solo el agua',
                                  'Los fertilizantes',
                                  'Solo el oxígeno molecular',
                                  'Solo el dióxido de carbono',
                                  'Solo la glucosa'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos secundarios son necesarios '
                             'para las células en cantidades:',
                 'alternativas': ['Mayores que los primarios',
                                  'Más pequeñas que los primarios',
                                  'Idénticas a los primarios',
                                  'Nulas',
                                  'Ilimitadas'],
                 'correcta': 'B'}]},
 {'num': 3,
  'titulo': 'Biomoléculas Inorgánicas',
  'secciones': [{'titulo': '3.1 CARACTERÍSTICAS GENERALES',
                 'items': ['Las biomoléculas inorgánicas se caracterizan por '
                           'la {ausencia} de enlaces carbono-carbono en su '
                           'estructura química.',
                           'Los {minerales sólidos} forman estructuras '
                           'duras, como huesos, dientes y conchas.',
                           'Los {minerales en disolución} son electrolitos '
                           'que participan en la contracción muscular y el '
                           'equilibrio {osmótico}.',
                           'Los {gases disueltos}, principalmente oxígeno y '
                           'dióxido de carbono, se usan en la respiración y '
                           'la {fotosíntesis}.']},
                {'titulo': '3.2 LA MOLÉCULA DE AGUA',
                 'items': ['La molécula de agua está formada por dos átomos '
                           'de {hidrógeno} y uno de {oxígeno}, unidos por '
                           'enlaces {covalentes}.',
                           'La molécula de agua tiene una estructura '
                           '{tetraédrica}, con un ángulo entre los '
                           'hidrógenos de {104,5}°.',
                           'La molécula de agua forma {dipolos}, porque el '
                           'oxígeno tiene carga negativa parcial y el '
                           'hidrógeno, carga {positiva} parcial.',
                           'La atracción entre moléculas de agua polares '
                           'produce el llamado {puente de hidrógeno}.',
                           'Una sola molécula de agua puede formar puentes '
                           'de hidrógeno hasta con otras {cuatro} moléculas '
                           'de agua.']},
                {'titulo': '3.3 EL AGUA EN LA CÉLULA',
                 'items': ['El agua {libre} representa el 95% del agua '
                           'celular, y actúa como solvente estable e '
                           '{ionizante}.',
                           'El agua {ligada} representa el 5% restante, y '
                           'comprende el agua de {imbibición} y el agua de '
                           'constitución.']},
                {'titulo': '3.4 PROPIEDADES DEL AGUA',
                 'items': ['El {poder solvente} del agua es su capacidad de '
                           'disolver gran cantidad de moléculas inorgánicas '
                           'y {orgánicas}.',
                           'La {polaridad} de la molécula de agua favorece '
                           'la disociación de moléculas formadoras de '
                           '{iones}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Las biomoléculas inorgánicas se caracterizan por '
                           'la ausencia de enlaces {Carbono-carbono}.',
                           'Los minerales que forman estructuras duras, como '
                           'huesos y dientes, se llaman {Minerales sólidos}.',
                           'Los minerales en disolución son electrolitos que '
                           'participan, entre otras funciones, en {La '
                           'contracción muscular}.',
                           'Los gases disueltos que usan los seres vivos son '
                           'principalmente oxígeno y {Dióxido de carbono}.',
                           'La molécula de agua está formada por dos átomos '
                           'de hidrógeno y uno de {Oxígeno}.',
                           'Los átomos de la molécula de agua se unen '
                           'mediante enlaces {Covalentes}.',
                           'La estructura de la molécula de agua se describe '
                           'como {Tetraédrica}.',
                           'El ángulo entre los dos átomos de hidrógeno en '
                           'la molécula de agua es de aproximadamente '
                           '{104,5°}.',
                           'La distribución desigual de carga dentro de un '
                           'enlace se denomina {Dipolo}.',
                           'En la molécula de agua, el oxígeno tiene una '
                           'carga parcial {Negativa}.',
                           'La atracción entre moléculas de agua debido a su '
                           'polaridad produce el llamado {Puente de '
                           'hidrógeno}.',
                           'Una sola molécula de agua puede formar puentes '
                           'de hidrógeno con hasta otras {Cuatro moléculas}.',
                           'El agua en estado libre representa del agua '
                           'celular total aproximadamente {95%}.',
                           'El agua en estado libre desempeña un papel como '
                           '{Solvente estable e ionizante}.',
                           'El agua ligada representa del agua celular total '
                           'aproximadamente {5%}.',
                           'El agua ligada comprende el agua de imbibición y '
                           'el agua de {Constitución}.',
                           'La capacidad del agua de disolver gran cantidad '
                           'de moléculas se llama {Poder solvente}.',
                           'La polaridad de la molécula de agua favorece la '
                           'disociación de moléculas formadoras de {Iones}.',
                           'El agua de imbibición está ligada fuertemente a '
                           'la superficie de {Las proteínas}.',
                           'Para liberar el agua ligada de las proteínas se '
                           'requiere {Grandes cantidades de energía}.']}],
  'cuadros': [{'titulo': '3.3 EL AGUA EN LA CÉLULA',
               'encabezados': ['Forma', 'Porcentaje'],
               'filas': [['Agua {libre}', '{95}%'],
                         ['Agua {ligada}', '{5}%']]}],
  'preguntas': [{'pregunta': 'Las biomoléculas inorgánicas se caracterizan '
                             'por la ausencia de enlaces:',
                 'alternativas': ['Hidrógeno-oxígeno',
                                  'Carbono-carbono',
                                  'Nitrógeno-fósforo',
                                  'Azufre-carbono',
                                  'Oxígeno-nitrógeno'],
                 'correcta': 'B'},
                {'pregunta': 'Los minerales que forman estructuras duras, '
                             'como huesos y dientes, se llaman:',
                 'alternativas': ['Minerales en disolución',
                                  'Minerales sólidos',
                                  'Gases disueltos',
                                  'Electrolitos exclusivos',
                                  'Iones libres'],
                 'correcta': 'B'},
                {'pregunta': 'Los minerales en disolución son electrolitos '
                             'que participan, entre otras funciones, en:',
                 'alternativas': ['La respiración exclusivamente',
                                  'La contracción muscular',
                                  'La digestión de proteínas',
                                  'La síntesis de ADN exclusivamente',
                                  'El transporte de oxígeno exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los gases disueltos que usan los seres vivos '
                             'son principalmente oxígeno y:',
                 'alternativas': ['Nitrógeno',
                                  'Dióxido de carbono',
                                  'Hidrógeno gaseoso',
                                  'Metano',
                                  'Ozono'],
                 'correcta': 'B'},
                {'pregunta': 'La molécula de agua está formada por dos '
                             'átomos de hidrógeno y uno de:',
                 'alternativas': ['Carbono',
                                  'Oxígeno',
                                  'Nitrógeno',
                                  'Azufre',
                                  'Fósforo'],
                 'correcta': 'B'},
                {'pregunta': 'Los átomos de la molécula de agua se unen '
                             'mediante enlaces:',
                 'alternativas': ['Iónicos',
                                  'Covalentes',
                                  'Metálicos',
                                  'De hidrógeno exclusivamente',
                                  'Van der Waals exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura de la molécula de agua se '
                             'describe como:',
                 'alternativas': ['Lineal',
                                  'Tetraédrica',
                                  'Cúbica',
                                  'Esférica perfecta',
                                  'Hexagonal'],
                 'correcta': 'B'},
                {'pregunta': 'El ángulo entre los dos átomos de hidrógeno en '
                             'la molécula de agua es de aproximadamente:',
                 'alternativas': ['90°', '104,5°', '180°', '60°', '120°'],
                 'correcta': 'B'},
                {'pregunta': 'La distribución desigual de carga dentro de un '
                             'enlace se denomina:',
                 'alternativas': ['Isómero',
                                  'Dipolo',
                                  'Catión',
                                  'Anión',
                                  'Radical libre'],
                 'correcta': 'B'},
                {'pregunta': 'En la molécula de agua, el oxígeno tiene una '
                             'carga parcial:',
                 'alternativas': ['Positiva',
                                  'Negativa',
                                  'Neutra',
                                  'Nula',
                                  'Variable al azar'],
                 'correcta': 'B'},
                {'pregunta': 'La atracción entre moléculas de agua debido a '
                             'su polaridad produce el llamado:',
                 'alternativas': ['Enlace iónico',
                                  'Puente de hidrógeno',
                                  'Enlace covalente puro',
                                  'Enlace metálico',
                                  'Enlace peptídico'],
                 'correcta': 'B'},
                {'pregunta': 'Una sola molécula de agua puede formar puentes '
                             'de hidrógeno con hasta otras:',
                 'alternativas': ['Dos moléculas',
                                  'Cuatro moléculas',
                                  'Ocho moléculas',
                                  'Una sola molécula',
                                  'Diez moléculas'],
                 'correcta': 'B'},
                {'pregunta': 'El agua en estado libre representa del agua '
                             'celular total aproximadamente:',
                 'alternativas': ['50%', '95%', '5%', '75%', '25%'],
                 'correcta': 'B'},
                {'pregunta': 'El agua en estado libre desempeña un papel '
                             'como:',
                 'alternativas': ['Estructura rígida',
                                  'Solvente estable e ionizante',
                                  'Fuente de energía exclusiva',
                                  'Pigmento celular',
                                  'Material genético'],
                 'correcta': 'B'},
                {'pregunta': 'El agua ligada representa del agua celular '
                             'total aproximadamente:',
                 'alternativas': ['95%', '5%', '50%', '25%', '75%'],
                 'correcta': 'B'},
                {'pregunta': 'El agua ligada comprende el agua de imbibición '
                             'y el agua de:',
                 'alternativas': ['Reserva',
                                  'Constitución',
                                  'Transporte exclusivo',
                                  'Excreción',
                                  'Filtración'],
                 'correcta': 'B'},
                {'pregunta': 'La capacidad del agua de disolver gran '
                             'cantidad de moléculas se llama:',
                 'alternativas': ['Poder calorífico',
                                  'Poder solvente',
                                  'Poder tensioactivo',
                                  'Poder oxidante',
                                  'Poder reductor'],
                 'correcta': 'B'},
                {'pregunta': 'La polaridad de la molécula de agua favorece '
                             'la disociación de moléculas formadoras de:',
                 'alternativas': ['Enlaces covalentes puros',
                                  'Iones',
                                  'Enlaces peptídicos',
                                  'Cadenas de carbono',
                                  'Anillos aromáticos'],
                 'correcta': 'B'},
                {'pregunta': 'El agua de imbibición está ligada fuertemente '
                             'a la superficie de:',
                 'alternativas': ['Los carbohidratos',
                                  'Las proteínas',
                                  'Los lípidos exclusivamente',
                                  'El ADN exclusivamente',
                                  'Los minerales sólidos'],
                 'correcta': 'B'},
                {'pregunta': 'Para liberar el agua ligada de las proteínas '
                             'se requiere:',
                 'alternativas': ['Ninguna energía',
                                  'Grandes cantidades de energía',
                                  'Solo un cambio de temperatura leve',
                                  'Solo presión atmosférica normal',
                                  'Solo luz solar'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'Biomoléculas Orgánicas',
  'secciones': [{'titulo': '4.1 CARACTERÍSTICAS DE LOS CARBOHIDRATOS',
                 'items': ['Los carbohidratos, o {glúcidos}, son moléculas '
                           'orgánicas formadas por carbono, hidrógeno y '
                           '{oxígeno}.',
                           'En los carbohidratos, la relación entre '
                           'hidrógeno y oxígeno es de {2:1}, igual que en el '
                           'agua.',
                           'Los carbohidratos son sintetizados por los '
                           '{autótrofos} mediante la {fotosíntesis}.',
                           'La fórmula empírica de los carbohidratos es '
                           '{(CH2O)n}.']},
                {'titulo': '4.2 FUNCIONES DE LOS CARBOHIDRATOS',
                 'items': ['Los carbohidratos son fuente {inmediata} de '
                           'energía, proporcionando la energía de {arranque} '
                           'para las actividades vitales.',
                           'Los carbohidratos sirven como {reserva '
                           'energética}: el {glucógeno} en animales y el '
                           'almidón en plantas.',
                           'Los carbohidratos participan como materiales '
                           '{estructurales}, como la {celulosa} en las '
                           'fibras vegetales.']},
                {'titulo': '4.3 CLASIFICACIÓN: MONOSACÁRIDOS',
                 'items': ['Los {monosacáridos} son los azúcares más '
                           'simples, dulces, sólidos, cristalizables e '
                           '{hidrolizables}.',
                           'Las {aldosas} poseen grupo aldehído; las '
                           '{cetosas} poseen grupo cetona.',
                           'En la estructura {piranosa}, el anillo está '
                           'formado por 5 átomos de carbono, como en la '
                           '{glucosa}.',
                           'En la estructura {furanosa}, el anillo está '
                           'formado por 4 átomos de carbono, como en la '
                           '{fructosa}.',
                           'Las {pentosas} más importantes son la ribosa y '
                           'la {desoxirribosa}, que forman parte del ARN y '
                           'el ADN.',
                           'La {glucosa} es el monosacárido más abundante en '
                           'la naturaleza y la principal fuente de {energía} '
                           'de los seres vivos.',
                           'La {galactosa} no se encuentra libre, sino '
                           'combinada con la glucosa formando {lactosa}.']},
                {'titulo': '4.4 OLIGOSACÁRIDOS Y DISACÁRIDOS',
                 'items': ['Los {oligosacáridos} son cadenas de 2 a 10 '
                           'monosacáridos unidos por un enlace '
                           '{O-glucosídico}.',
                           'Los {disacáridos} son los oligosacáridos más '
                           'abundantes, formados por la unión de dos '
                           '{monosacáridos}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los carbohidratos también se llaman glúcidos o '
                           '{Hidratos de carbono}.',
                           'Los carbohidratos están formados por carbono, '
                           'hidrógeno y {Oxígeno}.',
                           'En los carbohidratos, la relación entre '
                           'hidrógeno y oxígeno es de {2:1}.',
                           'Los carbohidratos son sintetizados por los '
                           'autótrofos mediante {La fotosíntesis}.',
                           'La fórmula empírica general de los carbohidratos '
                           'es {(CH2O)n}.',
                           'La función de los carbohidratos que proporciona '
                           'energía de arranque se llama {Fuente inmediata '
                           'de energía}.',
                           'El glucógeno almacenado en hígado y músculos '
                           'cumple la función de {Reserva energética}.',
                           'La celulosa, presente en fibras vegetales, '
                           'cumple principalmente una función {Estructural}.',
                           'Los azúcares más simples, dulces y '
                           'cristalizables, se llaman {Monosacáridos}.',
                           'Los monosacáridos que poseen grupo aldehído se '
                           'llaman {Aldosas}.',
                           'Los monosacáridos que poseen grupo cetona se '
                           'llaman {Cetosas}.',
                           'La estructura cíclica con anillo de 5 átomos de '
                           'carbono, como en la glucosa, se llama '
                           '{Piranosa}.',
                           'La estructura cíclica con anillo de 4 átomos de '
                           'carbono, como en la fructosa, se llama '
                           '{Furanosa}.',
                           'Las pentosas más importantes, que forman parte '
                           'de los ácidos nucleicos, son la ribosa y la '
                           '{Desoxirribosa}.',
                           'El monosacárido más abundante en la naturaleza y '
                           'principal fuente de energía es la {Glucosa}.',
                           'La galactosa no se encuentra libre, sino '
                           'combinada con la glucosa para formar {Lactosa}.',
                           'La manosa es constituyente de glicoproteínas de '
                           'origen {Animal}.',
                           'Los oligosacáridos están formados por un número '
                           'de monosacáridos entre {2 y 10}.',
                           'El enlace que une a los monosacáridos en los '
                           'oligosacáridos se llama enlace {O-glucosídico}.',
                           'Los disacáridos, oligosacáridos más abundantes, '
                           'están formados por la unión de {Dos '
                           'monosacáridos}.']}],
  'cuadros': [{'titulo': '4.3 CLASIFICACIÓN DE MONOSACÁRIDOS POR CARBONOS',
               'encabezados': ['Tipo', 'Número de carbonos', 'Ejemplo'],
               'filas': [['{Triosas}', '3', 'Gliceraldehído'],
                         ['{Pentosas}', '5', '{Ribosa}, desoxirribosa'],
                         ['{Hexosas}', '6', '{Glucosa}, fructosa']]}],
  'preguntas': [{'pregunta': 'Los carbohidratos también se llaman glúcidos '
                             'o:',
                 'alternativas': ['Lípidos',
                                  'Hidratos de carbono',
                                  'Ácidos nucleicos',
                                  'Proteínas',
                                  'Aminoácidos'],
                 'correcta': 'B'},
                {'pregunta': 'Los carbohidratos están formados por carbono, '
                             'hidrógeno y:',
                 'alternativas': ['Nitrógeno',
                                  'Oxígeno',
                                  'Azufre',
                                  'Fósforo',
                                  'Sodio'],
                 'correcta': 'B'},
                {'pregunta': 'En los carbohidratos, la relación entre '
                             'hidrógeno y oxígeno es de:',
                 'alternativas': ['1:1', '2:1', '3:1', '1:2', '4:1'],
                 'correcta': 'B'},
                {'pregunta': 'Los carbohidratos son sintetizados por los '
                             'autótrofos mediante:',
                 'alternativas': ['La respiración celular',
                                  'La fotosíntesis',
                                  'La digestión',
                                  'La glucólisis exclusiva',
                                  'La fermentación'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula empírica general de los '
                             'carbohidratos es:',
                 'alternativas': ['CO2',
                                  '(CH2O)n',
                                  'H2O',
                                  'NH3',
                                  'C6H12O6 exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La función de los carbohidratos que '
                             'proporciona energía de arranque se llama:',
                 'alternativas': ['Reserva energética',
                                  'Fuente inmediata de energía',
                                  'Función estructural',
                                  'Función catalítica',
                                  'Función hormonal'],
                 'correcta': 'B'},
                {'pregunta': 'El glucógeno almacenado en hígado y músculos '
                             'cumple la función de:',
                 'alternativas': ['Fuente inmediata de energía',
                                  'Reserva energética',
                                  'Material estructural',
                                  'Transporte de oxígeno',
                                  'Catálisis enzimática'],
                 'correcta': 'B'},
                {'pregunta': 'La celulosa, presente en fibras vegetales, '
                             'cumple principalmente una función:',
                 'alternativas': ['Energética inmediata',
                                  'Estructural',
                                  'Catalítica',
                                  'Hormonal',
                                  'De transporte'],
                 'correcta': 'B'},
                {'pregunta': 'Los azúcares más simples, dulces y '
                             'cristalizables, se llaman:',
                 'alternativas': ['Polisacáridos',
                                  'Monosacáridos',
                                  'Disacáridos exclusivamente',
                                  'Oligosacáridos exclusivamente',
                                  'Lípidos'],
                 'correcta': 'B'},
                {'pregunta': 'Los monosacáridos que poseen grupo aldehído se '
                             'llaman:',
                 'alternativas': ['Cetosas',
                                  'Aldosas',
                                  'Pentosas exclusivamente',
                                  'Hexosas exclusivamente',
                                  'Triosas exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los monosacáridos que poseen grupo cetona se '
                             'llaman:',
                 'alternativas': ['Aldosas',
                                  'Cetosas',
                                  'Pentosas exclusivamente',
                                  'Disacáridos',
                                  'Polisacáridos'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura cíclica con anillo de 5 átomos '
                             'de carbono, como en la glucosa, se llama:',
                 'alternativas': ['Furanosa',
                                  'Piranosa',
                                  'Lineal',
                                  'Aldosa exclusiva',
                                  'Cetosa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura cíclica con anillo de 4 átomos '
                             'de carbono, como en la fructosa, se llama:',
                 'alternativas': ['Piranosa',
                                  'Furanosa',
                                  'Lineal',
                                  'Hexosa exclusiva',
                                  'Pentosa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Las pentosas más importantes, que forman parte '
                             'de los ácidos nucleicos, son la ribosa y la:',
                 'alternativas': ['Glucosa',
                                  'Desoxirribosa',
                                  'Fructosa',
                                  'Galactosa',
                                  'Manosa'],
                 'correcta': 'B'},
                {'pregunta': 'El monosacárido más abundante en la naturaleza '
                             'y principal fuente de energía es la:',
                 'alternativas': ['Fructosa',
                                  'Glucosa',
                                  'Galactosa',
                                  'Manosa',
                                  'Ribosa'],
                 'correcta': 'B'},
                {'pregunta': 'La galactosa no se encuentra libre, sino '
                             'combinada con la glucosa para formar:',
                 'alternativas': ['Sacarosa',
                                  'Lactosa',
                                  'Maltosa',
                                  'Celulosa',
                                  'Almidón'],
                 'correcta': 'B'},
                {'pregunta': 'La manosa es constituyente de glicoproteínas '
                             'de origen:',
                 'alternativas': ['Vegetal exclusivo',
                                  'Animal',
                                  'Bacteriano exclusivo',
                                  'Mineral',
                                  'Viral exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los oligosacáridos están formados por un '
                             'número de monosacáridos entre:',
                 'alternativas': ['1 y 2',
                                  '2 y 10',
                                  '10 y 100',
                                  '100 y 1000',
                                  'Más de 1000'],
                 'correcta': 'B'},
                {'pregunta': 'El enlace que une a los monosacáridos en los '
                             'oligosacáridos se llama enlace:',
                 'alternativas': ['Peptídico',
                                  'O-glucosídico',
                                  'Fosfodiéster',
                                  'De hidrógeno exclusivo',
                                  'Iónico'],
                 'correcta': 'B'},
                {'pregunta': 'Los disacáridos, oligosacáridos más '
                             'abundantes, están formados por la unión de:',
                 'alternativas': ['Un solo monosacárido',
                                  'Dos monosacáridos',
                                  'Diez monosacáridos',
                                  'Cien monosacáridos',
                                  'Ningún monosacárido'],
                 'correcta': 'B'}]},
 {'num': 5,
  'titulo': 'La Célula',
  'secciones': [{'titulo': '5.1 GENERALIDADES Y ORIGEN DEL TÉRMINO',
                 'items': ['La palabra «célula» proviene del latín '
                           '«{cella}», que significa «pequeña habitación o '
                           'celda».',
                           'La célula es la unidad {estructural} y '
                           '{funcional} fundamental de todos los seres '
                           'vivos.',
                           'En {1665}, {Robert Hooke} introdujo el término '
                           '«célula» al observar cavidades en un corte de '
                           'corcho.',
                           'Hooke publicó sus observaciones en el libro '
                           '«{Micrographia}».']},
                {'titulo': '5.2 LA TEORÍA CELULAR',
                 'items': ['Los fundadores de la teoría celular fueron '
                           '{Mathias Schleiden} (1838) y {Theodor Schwann} '
                           '(1839).',
                           'Schleiden concluyó que todas las {plantas} están '
                           'formadas por células; Schwann, lo mismo sobre '
                           'los {animales}.',
                           'En 1855, {Rudolph Virchow} sintetizó la frase '
                           '«omnis cellula ex {cellula}»: toda célula '
                           'proviene de otra célula.',
                           'Según la teoría celular, todos los seres vivos '
                           'están formados por una o más {células}.',
                           'Las {actividades} esenciales de la vida ocurren '
                           'en el interior de las células.',
                           'Las nuevas células se originan de células '
                           '{preexistentes}, por división de estas.',
                           'Las células contienen la {información '
                           'hereditaria} que pasa de células progenitoras a '
                           'células hijas.']},
                {'titulo': '5.3 CÉLULA PROCARIOTA Y EUCARIOTA',
                 'items': ['«Procariota» proviene del griego «protos» '
                           '(primitivo) y «{karyon}» (núcleo).',
                           'Las células procariotas tienen su material '
                           'genético como una molécula {circular} de ADN, en '
                           'una región llamada {nucleoide}.',
                           '«Eucariota» proviene del griego «{eu}» '
                           '(verdadero) y «karyon» (núcleo).',
                           'Las células eucariotas poseen un ADN {lineal} '
                           'dentro de un núcleo verdadero, delimitado por '
                           'una envoltura {nuclear}.',
                           'Solo los organismos {moneras} son procariotas; '
                           'los demás reinos son eucariotas.',
                           'Según el criterio de tres dominios, {Archaea} y '
                           '{Bacteria} son procariotas, y {Eukarya} agrupa a '
                           'los eucariotas.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La palabra «célula» proviene del latín «cella», '
                           'que significa {Pequeña habitación o celda}.',
                           'La célula es considerada la unidad estructural y '
                           '{Funcional fundamental de los seres vivos}.',
                           'El científico que introdujo el término «célula» '
                           'en 1665 fue {Robert Hooke}.',
                           'Robert Hooke publicó sus observaciones celulares '
                           'en el libro {Micrographia}.',
                           'Los fundadores de la teoría celular fueron '
                           'Schleiden y {Schwann}.',
                           'Schleiden concluyó que todas las plantas están '
                           'constituidas por {Células}.',
                           'Schwann concluyó la misma idea que Schleiden, '
                           'pero referida a {Los animales}.',
                           'La célebre frase «omnis cellula ex cellula» fue '
                           'sintetizada por {Schwann}.',
                           'La frase «omnis cellula ex cellula» significa '
                           '{Toda célula se origina de otra célula}.',
                           'Según la teoría celular, las actividades '
                           'esenciales de la vida ocurren {En el interior de '
                           'las células}.',
                           'Según la teoría celular, las nuevas células se '
                           'originan de {Células preexistentes, por '
                           'división}.',
                           'Las células contienen la información '
                           'hereditaria, que pasa de {Células progenitoras a '
                           'células hijas}.',
                           'El término «procariota» proviene del griego '
                           '«protos», que significa {Primitivo}.',
                           'El material genético de la célula procariota es '
                           'una molécula de ADN {Circular}.',
                           'En la célula procariota, el ADN se concentra en '
                           'una región llamada {Nucleoide}.',
                           'El término «eucariota» proviene del griego «eu», '
                           'que significa {Verdadero}.',
                           'En la célula eucariota, el ADN se encuentra '
                           'dentro de {Un núcleo verdadero con envoltura '
                           'nuclear}.',
                           'Solo los organismos del reino monera son de tipo '
                           'celular {Procariota}.',
                           'Según el criterio de tres dominios, Archaea y '
                           'Bacteria agrupan a los organismos {Procariotas}.',
                           'El dominio Eukarya agrupa a todos los organismos '
                           '{Eucariotas}.']}],
  'cuadros': [{'titulo': '5.3 CÉLULA PROCARIOTA FRENTE A EUCARIOTA',
               'encabezados': ['Característica', 'Procariota', 'Eucariota'],
               'filas': [['ADN',
                          '{Circular}, en nucleoide',
                          '{Lineal}, en núcleo verdadero'],
                         ['Envoltura nuclear', '{Ausente}', '{Presente}'],
                         ['Organelos membranosos',
                          '{Ausentes}',
                          '{Presentes}']]}],
  'preguntas': [{'pregunta': 'La palabra «célula» proviene del latín '
                             '«cella», que significa:',
                 'alternativas': ['Núcleo',
                                  'Pequeña habitación o celda',
                                  'Membrana',
                                  'Organelo',
                                  'Tejido'],
                 'correcta': 'B'},
                {'pregunta': 'La célula es considerada la unidad estructural '
                             'y:',
                 'alternativas': ['Química exclusiva',
                                  'Funcional fundamental de los seres vivos',
                                  'Genética exclusiva',
                                  'Ecológica',
                                  'Atómica'],
                 'correcta': 'B'},
                {'pregunta': 'El científico que introdujo el término '
                             '«célula» en 1665 fue:',
                 'alternativas': ['Schleiden',
                                  'Robert Hooke',
                                  'Schwann',
                                  'Virchow',
                                  'Darwin'],
                 'correcta': 'B'},
                {'pregunta': 'Robert Hooke publicó sus observaciones '
                             'celulares en el libro:',
                 'alternativas': ['El origen de las especies',
                                  'Micrographia',
                                  'De Revolutionibus',
                                  'Principia',
                                  'Systema Naturae'],
                 'correcta': 'B'},
                {'pregunta': 'Los fundadores de la teoría celular fueron '
                             'Schleiden y:',
                 'alternativas': ['Hooke',
                                  'Schwann',
                                  'Virchow',
                                  'Darwin',
                                  'Mendel'],
                 'correcta': 'B'},
                {'pregunta': 'Schleiden concluyó que todas las plantas están '
                             'constituidas por:',
                 'alternativas': ['Tejidos exclusivamente',
                                  'Células',
                                  'Órganos exclusivamente',
                                  'Minerales',
                                  'Fibras'],
                 'correcta': 'B'},
                {'pregunta': 'Schwann concluyó la misma idea que Schleiden, '
                             'pero referida a:',
                 'alternativas': ['Los hongos',
                                  'Los animales',
                                  'Las bacterias',
                                  'Los virus',
                                  'Los minerales'],
                 'correcta': 'B'},
                {'pregunta': 'La célebre frase «omnis cellula ex cellula» '
                             'fue sintetizada por:',
                 'alternativas': ['Schleiden',
                                  'Schwann',
                                  'Rudolph Virchow',
                                  'Robert Hooke',
                                  'Charles Darwin'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «omnis cellula ex cellula» significa:',
                 'alternativas': ['Toda célula tiene núcleo',
                                  'Toda célula se origina de otra célula',
                                  'Toda célula es eucariota',
                                  'Toda célula tiene ADN circular',
                                  'Toda célula muere pronto'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría celular, las actividades '
                             'esenciales de la vida ocurren:',
                 'alternativas': ['Fuera de las células',
                                  'En el interior de las células',
                                  'Solo en el núcleo',
                                  'Solo en la membrana',
                                  'Solo en el citoplasma exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría celular, las nuevas células se '
                             'originan de:',
                 'alternativas': ['La nada',
                                  'Células preexistentes, por división',
                                  'Solo del ADN libre',
                                  'Reacciones químicas espontáneas',
                                  'Fusión de tejidos'],
                 'correcta': 'B'},
                {'pregunta': 'Las células contienen la información '
                             'hereditaria, que pasa de:',
                 'alternativas': ['Células hijas a progenitoras',
                                  'Células progenitoras a células hijas',
                                  'Tejidos a órganos',
                                  'Órganos a sistemas',
                                  'Ninguna transmisión ocurre'],
                 'correcta': 'B'},
                {'pregunta': 'El término «procariota» proviene del griego '
                             '«protos», que significa:',
                 'alternativas': ['Verdadero',
                                  'Primitivo',
                                  'Núcleo',
                                  'Hueco',
                                  'Vida'],
                 'correcta': 'B'},
                {'pregunta': 'El material genético de la célula procariota '
                             'es una molécula de ADN:',
                 'alternativas': ['Lineal',
                                  'Circular',
                                  'Ausente',
                                  'Ramificada',
                                  'Doble hélice exclusivamente eucariota'],
                 'correcta': 'B'},
                {'pregunta': 'En la célula procariota, el ADN se concentra '
                             'en una región llamada:',
                 'alternativas': ['Núcleo',
                                  'Nucleoide',
                                  'Nucléolo',
                                  'Cromosoma',
                                  'Retículo'],
                 'correcta': 'B'},
                {'pregunta': 'El término «eucariota» proviene del griego '
                             '«eu», que significa:',
                 'alternativas': ['Primitivo',
                                  'Verdadero',
                                  'Hueco',
                                  'Pequeño',
                                  'Externo'],
                 'correcta': 'B'},
                {'pregunta': 'En la célula eucariota, el ADN se encuentra '
                             'dentro de:',
                 'alternativas': ['El citoplasma sin protección',
                                  'Un núcleo verdadero con envoltura nuclear',
                                  'La pared celular',
                                  'El nucleoide',
                                  'La membrana plasmática'],
                 'correcta': 'B'},
                {'pregunta': 'Solo los organismos del reino monera son de '
                             'tipo celular:',
                 'alternativas': ['Eucariota',
                                  'Procariota',
                                  'Mixto',
                                  'Viral',
                                  'Ninguno de los anteriores'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio de tres dominios, Archaea y '
                             'Bacteria agrupan a los organismos:',
                 'alternativas': ['Eucariotas',
                                  'Procariotas',
                                  'Virales',
                                  'Mixtos',
                                  'Fúngicos exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El dominio Eukarya agrupa a todos los '
                             'organismos:',
                 'alternativas': ['Procariotas',
                                  'Eucariotas',
                                  'Virales exclusivamente',
                                  'Solo bacterias',
                                  'Solo arqueas'],
                 'correcta': 'B'}]},
 {'num': 6,
  'titulo': 'Célula Eucariota',
  'secciones': [{'titulo': '6.1 ESTRUCTURA GENERAL',
                 'items': ['Las células eucariotas tienen su ADN encerrado '
                           'dentro de una {doble membrana} o envoltura '
                           'nuclear.',
                           'En la célula eucariota se diferencian tres '
                           'partes: la {membrana}, el citoplasma y el '
                           '{núcleo}.',
                           'El ADN asociado a histonas se llama {cromatina}, '
                           'localizada en el {núcleo}.',
                           'Las células eucariotas son mucho más {grandes} '
                           'que las procariotas.']},
                {'titulo': '6.2 PARED CELULAR Y GLICOCÁLIX',
                 'items': ['La {pared celular} está presente solo en células '
                           'vegetales y hongos, y está formada por '
                           '{celulosa}.',
                           'Entre células vegetales adyacentes hay puentes '
                           'intercelulares llamados {plasmodesmos}.',
                           'La {quitina} es componente de la pared celular '
                           'de los {hongos}.',
                           'El {glicocálix}, o cubierta externa, caracteriza '
                           'a las células animales y participa en el '
                           '{reconocimiento} celular.']},
                {'titulo': '6.3 LA MEMBRANA CELULAR',
                 'items': ['La membrana plasmática es de naturaleza '
                           '{lipoproteica} y tiene permeabilidad '
                           '{selectiva}.',
                           'El modelo de estructura de membrana se llama '
                           '«{mosaico fluido}», propuesto por {Singer y '
                           'Nicholson} en 1972.',
                           'En la membrana, los lípidos representan '
                           'aproximadamente el {40}%, las proteínas el '
                           '{52}%, y los glúcidos el 8%.',
                           'Los {fosfolípidos} son los componentes lipídicos '
                           'más abundantes, formando la bicapa lipídica.',
                           'El {colesterol} se encuentra en células animales '
                           'y es responsable de la {fluidez} de la '
                           'membrana.']},
                {'titulo': '6.4 PROTEÍNAS DE MEMBRANA',
                 'items': ['Las proteínas {periféricas} o extrínsecas se '
                           'localizan en las superficies de la membrana y '
                           'son {solubles} en agua.',
                           'Las proteínas {integrales} o intrínsecas '
                           'atraviesan todo el espesor de la membrana y no '
                           'son solubles en {agua}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['En la célula eucariota, el ADN se encuentra '
                           'encerrado dentro de {Una doble membrana o '
                           'envoltura nuclear}.',
                           'Las tres partes principales de la célula '
                           'eucariota son membrana, citoplasma y {Núcleo}.',
                           'El ADN asociado a histonas recibe el nombre de '
                           '{Cromatina}.',
                           'Las células eucariotas, en comparación con las '
                           'procariotas, son {Mucho más grandes}.',
                           'La pared celular está presente en {Células '
                           'vegetales y hongos}.',
                           'El principal componente estructural de la pared '
                           'celular vegetal es {La celulosa}.',
                           'Los puentes intercelulares entre células '
                           'vegetales adyacentes se llaman {Plasmodesmos}.',
                           'El componente de la pared celular de los hongos '
                           'es {La quitina}.',
                           'El glicocálix caracteriza a las células '
                           '{Animales}.',
                           'El glicocálix participa principalmente en {El '
                           'reconocimiento celular}.',
                           'La membrana plasmática es de naturaleza '
                           '{Lipoproteica}.',
                           'El modelo de estructura de la membrana celular '
                           'se denomina modelo de {Mosaico fluido}.',
                           'El modelo de mosaico fluido fue propuesto por '
                           '{Singer y Nicholson}.',
                           'En la composición de la membrana, los lípidos '
                           'representan aproximadamente {40%}.',
                           'En la composición de la membrana, las proteínas '
                           'representan aproximadamente {52%}.',
                           'Los componentes lipídicos más abundantes de la '
                           'membrana son los {Fosfolípidos}.',
                           'El colesterol de la membrana celular es '
                           'responsable, entre otras cosas, de {La fluidez '
                           'de la membrana}.',
                           'Las proteínas que se localizan en las '
                           'superficies de la membrana y son solubles en '
                           'agua se llaman {Periféricas o extrínsecas}.',
                           'Las proteínas que atraviesan todo el espesor de '
                           'la membrana se llaman proteínas {Integrales o '
                           'intrínsecas}.',
                           'Los carbohidratos de la membrana se encuentran '
                           'únicamente en {La superficie de la monocapa '
                           'externa}.']}],
  'cuadros': [{'titulo': '6.3 COMPOSICIÓN DE LA MEMBRANA CELULAR',
               'encabezados': ['Componente', 'Proporción aproximada'],
               'filas': [['{Lípidos}', '{40}%'],
                         ['{Proteínas}', '{52}%'],
                         ['{Glúcidos}', '8%']]}],
  'preguntas': [{'pregunta': 'En la célula eucariota, el ADN se encuentra '
                             'encerrado dentro de:',
                 'alternativas': ['Una sola membrana',
                                  'Una doble membrana o envoltura nuclear',
                                  'El citoplasma libre',
                                  'La pared celular',
                                  'El nucleoide'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres partes principales de la célula '
                             'eucariota son membrana, citoplasma y:',
                 'alternativas': ['Pared celular',
                                  'Núcleo',
                                  'Glicocálix',
                                  'Nucleoide',
                                  'Ribosoma'],
                 'correcta': 'B'},
                {'pregunta': 'El ADN asociado a histonas recibe el nombre '
                             'de:',
                 'alternativas': ['Nucleoide',
                                  'Cromatina',
                                  'Glicocálix',
                                  'Citosol',
                                  'Matriz'],
                 'correcta': 'B'},
                {'pregunta': 'Las células eucariotas, en comparación con las '
                             'procariotas, son:',
                 'alternativas': ['Más pequeñas',
                                  'Mucho más grandes',
                                  'Del mismo tamaño',
                                  'Sin núcleo definido',
                                  'Sin membrana'],
                 'correcta': 'B'},
                {'pregunta': 'La pared celular está presente en:',
                 'alternativas': ['Células animales exclusivamente',
                                  'Células vegetales y hongos',
                                  'Solo bacterias',
                                  'Todas las células sin excepción',
                                  'Solo células humanas'],
                 'correcta': 'B'},
                {'pregunta': 'El principal componente estructural de la '
                             'pared celular vegetal es:',
                 'alternativas': ['La quitina',
                                  'La celulosa',
                                  'El colesterol',
                                  'La queratina',
                                  'El glucógeno'],
                 'correcta': 'B'},
                {'pregunta': 'Los puentes intercelulares entre células '
                             'vegetales adyacentes se llaman:',
                 'alternativas': ['Desmosomas',
                                  'Plasmodesmos',
                                  'Uniones estrechas',
                                  'Sinapsis',
                                  'Gap junctions exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'El componente de la pared celular de los '
                             'hongos es:',
                 'alternativas': ['La celulosa',
                                  'La quitina',
                                  'El colesterol',
                                  'La lignina exclusiva',
                                  'La queratina'],
                 'correcta': 'B'},
                {'pregunta': 'El glicocálix caracteriza a las células:',
                 'alternativas': ['Vegetales',
                                  'Animales',
                                  'Fúngicas',
                                  'Bacterianas',
                                  'Procariotas en general'],
                 'correcta': 'B'},
                {'pregunta': 'El glicocálix participa principalmente en:',
                 'alternativas': ['La fotosíntesis',
                                  'El reconocimiento celular',
                                  'La respiración celular',
                                  'La replicación del ADN',
                                  'La síntesis de proteínas'],
                 'correcta': 'B'},
                {'pregunta': 'La membrana plasmática es de naturaleza:',
                 'alternativas': ['Puramente proteica',
                                  'Lipoproteica',
                                  'Puramente lipídica',
                                  'Mineral',
                                  'Celulósica'],
                 'correcta': 'B'},
                {'pregunta': 'El modelo de estructura de la membrana celular '
                             'se denomina modelo de:',
                 'alternativas': ['Doble hélice',
                                  'Mosaico fluido',
                                  'Capa rígida',
                                  'Red cristalina',
                                  'Esfera sólida'],
                 'correcta': 'B'},
                {'pregunta': 'El modelo de mosaico fluido fue propuesto por:',
                 'alternativas': ['Watson y Crick',
                                  'Singer y Nicholson',
                                  'Schleiden y Schwann',
                                  'Hooke y Virchow',
                                  'Mendel y Darwin'],
                 'correcta': 'B'},
                {'pregunta': 'En la composición de la membrana, los lípidos '
                             'representan aproximadamente:',
                 'alternativas': ['8%', '40%', '52%', '90%', '100%'],
                 'correcta': 'B'},
                {'pregunta': 'En la composición de la membrana, las '
                             'proteínas representan aproximadamente:',
                 'alternativas': ['8%', '40%', '52%', '10%', '0%'],
                 'correcta': 'C'},
                {'pregunta': 'Los componentes lipídicos más abundantes de la '
                             'membrana son los:',
                 'alternativas': ['Glicolípidos',
                                  'Fosfolípidos',
                                  'Esteroides',
                                  'Triglicéridos',
                                  'Carotenoides'],
                 'correcta': 'B'},
                {'pregunta': 'El colesterol de la membrana celular es '
                             'responsable, entre otras cosas, de:',
                 'alternativas': ['La rigidez total',
                                  'La fluidez de la membrana',
                                  'El transporte activo exclusivo',
                                  'La síntesis de proteínas',
                                  'La replicación del ADN'],
                 'correcta': 'B'},
                {'pregunta': 'Las proteínas que se localizan en las '
                             'superficies de la membrana y son solubles en '
                             'agua se llaman:',
                 'alternativas': ['Integrales',
                                  'Periféricas o extrínsecas',
                                  'Transmembrana',
                                  'Glicoproteicas exclusivas',
                                  'Enzimáticas exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Las proteínas que atraviesan todo el espesor '
                             'de la membrana se llaman proteínas:',
                 'alternativas': ['Periféricas',
                                  'Integrales o intrínsecas',
                                  'Extrínsecas',
                                  'Solubles en agua',
                                  'Superficiales'],
                 'correcta': 'B'},
                {'pregunta': 'Los carbohidratos de la membrana se encuentran '
                             'únicamente en:',
                 'alternativas': ['La monocapa interna',
                                  'La superficie de la monocapa externa',
                                  'El citoplasma',
                                  'El núcleo',
                                  'La matriz mitocondrial'],
                 'correcta': 'B'}]},
 {'num': 7,
  'titulo': 'Nutrición',
  'secciones': [{'titulo': '7.1 TIPOS DE NUTRICIÓN CELULAR',
                 'items': ['La nutrición celular puede ser de dos tipos: '
                           '{autótrofa} y {heterótrofa}.',
                           'La nutrición {autótrofa} es realizada por '
                           'células capaces de fabricar sus propios '
                           'alimentos a partir de productos {inorgánicos}.',
                           'Existen dos procesos de nutrición autótrofa: la '
                           '{quimioautótrofa} y la {fotoautótrofa}.']},
                {'titulo': '7.2 NUTRICIÓN QUIMIOAUTÓTROFA',
                 'items': ['La nutrición {quimioautótrofa}, o '
                           'quimiosíntesis, es característica de los '
                           'organismos {procariontes}.',
                           'Los quimiótrofos usan energía {química}, '
                           'obtenida por oxidación de productos inorgánicos, '
                           'en vez de energía {luminosa}.',
                           'Los procariontes {sulfurosos} oxidan compuestos '
                           'de azufre y producen ácido {sulfúrico}.',
                           'Los procariontes {hidrogenosos} oxidan el '
                           'hidrógeno del aire mediante una enzima especial.',
                           'Los procariontes {ferrosos} oxidan el hierro, '
                           'desde el estado ferroso al estado {férrico}.',
                           'Los procariontes {nitrificantes} oxidan el '
                           'amoniaco en nitritos y estos en {nitratos}, '
                           'siendo clave en la fertilidad del suelo.']},
                {'titulo': '7.3 NUTRICIÓN FOTOAUTÓTROFA: LA FOTOSÍNTESIS',
                 'items': ['El organelo típicamente vegetal necesario para '
                           'la fotosíntesis es el {cloroplasto}.',
                           'Las pilas de «monedas» dentro del cloroplasto se '
                           'llaman {tilacoides}; su conjunto se llama '
                           '{grana}.',
                           'La sustancia rica en enzimas que rodea a los '
                           'tilacoides se llama {estroma}.',
                           'La fotosíntesis transforma la energía {luminosa} '
                           'en energía {química}.',
                           'Los reactivos de la fotosíntesis son luz solar, '
                           'dióxido de carbono, agua y {clorofila}.',
                           'Los productos finales de la fotosíntesis son '
                           '{glucosa} y {oxígeno}.',
                           'La fotosíntesis tiene dos fases: la fase {I} o '
                           'luminosa, y la fase {II} o independiente de la '
                           'luz.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La nutrición celular puede ser de dos tipos: '
                           'autótrofa y {Heterótrofa}.',
                           'La nutrición realizada por células que fabrican '
                           'su propio alimento a partir de compuestos '
                           'inorgánicos es {Autótrofa}.',
                           'Los dos procesos de nutrición autótrofa son la '
                           'quimioautótrofa y la {Fotoautótrofa}.',
                           'La nutrición quimioautótrofa es característica '
                           'de los organismos {Procariontes}.',
                           'Los organismos quimiótrofos utilizan energía '
                           'química obtenida mediante la oxidación de '
                           'productos {Inorgánicos}.',
                           'Los procariontes que oxidan compuestos de azufre '
                           'se llaman procariontes {Sulfurosos}.',
                           'Los procariontes sulfurosos producen como '
                           'resultado de su oxidación {Ácido sulfúrico}.',
                           'Los procariontes que oxidan el hidrógeno del '
                           'aire se llaman procariontes {Hidrogenosos}.',
                           'Los procariontes que oxidan el hierro desde el '
                           'estado ferroso al férrico se llaman procariontes '
                           '{Ferrosos}.',
                           'Los procariontes que oxidan el amoniaco en '
                           'nitritos y estos en nitratos se llaman '
                           'procariontes {Nitrificantes}.',
                           'Las bacterias nitrificantes desempeñan un papel '
                           'importante en {La fertilidad de los suelos}.',
                           'El organelo típicamente vegetal necesario para '
                           'la fotosíntesis es {El cloroplasto}.',
                           'Las pilas de «monedas» dentro del cloroplasto se '
                           'llaman {Tilacoides}.',
                           'El conjunto de tilacoides recibe el nombre de '
                           '{Grana}.',
                           'La fotosíntesis transforma la energía luminosa '
                           'en energía {Química}.',
                           'Entre los reactivos necesarios para la '
                           'fotosíntesis figura la clorofila y {Dióxido de '
                           'carbono, agua y luz solar}.',
                           'Los productos finales de la fotosíntesis son '
                           'glucosa y {Oxígeno}.',
                           'La fase de la fotosíntesis que depende de la luz '
                           'se llama fase {I o luminosa}.',
                           'La fase de la fotosíntesis independiente de la '
                           'luz puede ocurrir {De día y de noche}.']}],
  'cuadros': [{'titulo': '7.2 TIPOS DE PROCARIONTES QUIMIOAUTÓTROFOS',
               'encabezados': ['Tipo', 'Oxida'],
               'filas': [['{Sulfurosos}', 'Compuestos de {azufre}'],
                         ['{Hidrogenosos}', '{Hidrógeno} del aire'],
                         ['{Ferrosos}', '{Hierro}'],
                         ['{Nitrificantes}', '{Amoniaco} y nitritos']]}],
  'preguntas': [{'pregunta': 'La nutrición celular puede ser de dos tipos: '
                             'autótrofa y:',
                 'alternativas': ['Fotótrofa exclusiva',
                                  'Heterótrofa',
                                  'Quimiótrofa exclusiva',
                                  'Mixótrofa',
                                  'Saprótrofa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La nutrición realizada por células que '
                             'fabrican su propio alimento a partir de '
                             'compuestos inorgánicos es:',
                 'alternativas': ['Heterótrofa',
                                  'Autótrofa',
                                  'Saprofita exclusiva',
                                  'Parasitaria',
                                  'Mixótrofa'],
                 'correcta': 'B'},
                {'pregunta': 'Los dos procesos de nutrición autótrofa son la '
                             'quimioautótrofa y la:',
                 'alternativas': ['Heterótrofa',
                                  'Fotoautótrofa',
                                  'Saprófita',
                                  'Parasitaria',
                                  'Simbiótica'],
                 'correcta': 'B'},
                {'pregunta': 'La nutrición quimioautótrofa es característica '
                             'de los organismos:',
                 'alternativas': ['Eucariotas exclusivamente',
                                  'Procariontes',
                                  'Animales exclusivamente',
                                  'Fúngicos exclusivamente',
                                  'Vegetales exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos quimiótrofos utilizan energía '
                             'química obtenida mediante la oxidación de '
                             'productos:',
                 'alternativas': ['Orgánicos exclusivamente',
                                  'Inorgánicos',
                                  'Solo carbohidratos',
                                  'Solo lípidos',
                                  'Solo proteínas'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan compuestos de '
                             'azufre se llaman procariontes:',
                 'alternativas': ['Hidrogenosos',
                                  'Sulfurosos',
                                  'Ferrosos',
                                  'Nitrificantes',
                                  'Fotótrofos'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes sulfurosos producen como '
                             'resultado de su oxidación:',
                 'alternativas': ['Ácido nítrico',
                                  'Ácido sulfúrico',
                                  'Ácido clorhídrico',
                                  'Ácido carbónico',
                                  'Ácido fosfórico'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan el hidrógeno del '
                             'aire se llaman procariontes:',
                 'alternativas': ['Sulfurosos',
                                  'Hidrogenosos',
                                  'Ferrosos',
                                  'Nitrificantes',
                                  'Fotótrofos'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan el hierro desde el '
                             'estado ferroso al férrico se llaman '
                             'procariontes:',
                 'alternativas': ['Sulfurosos',
                                  'Ferrosos',
                                  'Hidrogenosos',
                                  'Nitrificantes',
                                  'Autótrofos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan el amoniaco en '
                             'nitritos y estos en nitratos se llaman '
                             'procariontes:',
                 'alternativas': ['Ferrosos',
                                  'Nitrificantes',
                                  'Sulfurosos',
                                  'Hidrogenosos',
                                  'Fotótrofos'],
                 'correcta': 'B'},
                {'pregunta': 'Las bacterias nitrificantes desempeñan un '
                             'papel importante en:',
                 'alternativas': ['La fotosíntesis vegetal',
                                  'La fertilidad de los suelos',
                                  'La respiración animal',
                                  'La digestión humana',
                                  'La reproducción celular'],
                 'correcta': 'B'},
                {'pregunta': 'El organelo típicamente vegetal necesario para '
                             'la fotosíntesis es:',
                 'alternativas': ['La mitocondria',
                                  'El cloroplasto',
                                  'El ribosoma',
                                  'El lisosoma',
                                  'El aparato de Golgi'],
                 'correcta': 'B'},
                {'pregunta': 'Las pilas de «monedas» dentro del cloroplasto '
                             'se llaman:',
                 'alternativas': ['Estroma',
                                  'Tilacoides',
                                  'Cristas',
                                  'Matriz',
                                  'Cresta'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de tilacoides recibe el nombre de:',
                 'alternativas': ['Estroma',
                                  'Grana',
                                  'Matriz',
                                  'Cresta',
                                  'Nucleoide'],
                 'correcta': 'B'},
                {'pregunta': 'La sustancia rica en enzimas que rodea a los '
                             'tilacoides se llama:',
                 'alternativas': ['Grana',
                                  'Estroma',
                                  'Cresta',
                                  'Matriz mitocondrial',
                                  'Citosol'],
                 'correcta': 'B'},
                {'pregunta': 'La fotosíntesis transforma la energía luminosa '
                             'en energía:',
                 'alternativas': ['Mecánica',
                                  'Química',
                                  'Térmica exclusiva',
                                  'Eléctrica',
                                  'Nuclear'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los reactivos necesarios para la '
                             'fotosíntesis figura la clorofila y:',
                 'alternativas': ['Solo agua',
                                  'Dióxido de carbono, agua y luz solar',
                                  'Solo oxígeno',
                                  'Solo glucosa',
                                  'Solo nitrógeno'],
                 'correcta': 'B'},
                {'pregunta': 'Los productos finales de la fotosíntesis son '
                             'glucosa y:',
                 'alternativas': ['Dióxido de carbono',
                                  'Oxígeno',
                                  'Nitrógeno',
                                  'Agua exclusivamente',
                                  'Clorofila'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de la fotosíntesis que depende de la '
                             'luz se llama fase:',
                 'alternativas': ['II u oscura',
                                  'I o luminosa',
                                  'Intermedia',
                                  'Neutra',
                                  'Anaeróbica'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de la fotosíntesis independiente de la '
                             'luz puede ocurrir:',
                 'alternativas': ['Solo de día',
                                  'De día y de noche',
                                  'Solo de noche',
                                  'Nunca',
                                  'Solo en invierno'],
                 'correcta': 'B'}]},
 {'num': 8,
  'titulo': 'Nivel Sistémico',
  'secciones': [{'titulo': '8.1 EL SISTEMA RESPIRATORIO HUMANO',
                 'items': ['El hombre es un ser de respiración {aerobia}: '
                           'requiere aporte continuo de {oxígeno} para sus '
                           'células.',
                           'El oxígeno interviene en el paso final de la '
                           'cadena respiratoria, que ocurre en la membrana '
                           '{mitocondrial}.',
                           'El dióxido de carbono eliminado proviene de la '
                           '{glucólisis} y el ciclo de {Krebs}.',
                           'Estructuralmente, las vías respiratorias '
                           '{superiores} comprenden la nariz y la faringe; '
                           'las {inferiores}, laringe, tráquea, bronquios y '
                           'pulmones.']},
                {'titulo': '8.2 DIVISIÓN FISIOLÓGICA DEL APARATO '
                           'RESPIRATORIO',
                 'items': ['La porción {conductora} conduce el aire '
                           'inspirado y espirado; comprende nariz, faringe, '
                           'laringe, tráquea y {bronquios}.',
                           'La porción {respiratoria} se ocupa de oxigenar '
                           'la sangre; comprende bronquiolos respiratorios y '
                           '{alvéolos}.']},
                {'titulo': '8.3 LA NARIZ Y LA FARINGE',
                 'items': ['El interior de la nariz se divide en dos '
                           'cavidades nasales separadas por el {tabique} '
                           'nasal.',
                           'Las proyecciones recubiertas de la mucosa nasal '
                           'se llaman {cornetes}.',
                           'Las fosas nasales se comunican con la faringe a '
                           'través de dos aberturas llamadas {coanas}.',
                           'Las funciones de la nariz son calentar, '
                           'humedecer y {filtrar} el aire, y recibir '
                           'impulsos {olfatorios}.',
                           'La faringe, o garganta, es un órgano compartido '
                           'por los aparatos respiratorio y {digestivo}.',
                           'La faringe presenta tres regiones: '
                           '{nasofaringe}, orofaringe y {laringofaringe}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El hombre es un ser de respiración {Aerobia}.',
                           'El oxígeno interviene en el paso final de la '
                           'cadena respiratoria, que ocurre en {La membrana '
                           'mitocondrial}.',
                           'El dióxido de carbono que se elimina proviene '
                           'del metabolismo celular, específicamente de la '
                           'glucólisis y {El ciclo de Krebs}.',
                           'Las vías respiratorias superiores comprenden la '
                           'nariz y {La faringe}.',
                           'Las vías respiratorias inferiores incluyen la '
                           'laringe, la tráquea, los bronquios y {Los '
                           'pulmones}.',
                           'La porción del aparato respiratorio que conduce '
                           'el aire inspirado y espirado se llama porción '
                           '{Conductora}.',
                           'La porción del aparato respiratorio encargada de '
                           'oxigenar la sangre se llama porción '
                           '{Respiratoria}.',
                           'La porción respiratoria comprende bronquiolos '
                           'respiratorios, conductos alveolares y {Los '
                           'alvéolos}.',
                           'El interior de la nariz está dividido en dos '
                           'cavidades nasales por {El tabique nasal}.',
                           'Las proyecciones recubiertas en las paredes '
                           'laterales de la mucosa nasal se llaman '
                           '{Cornetes}.',
                           'Las aberturas que comunican las fosas nasales '
                           'con la faringe se llaman {Coanas}.',
                           'Entre las funciones de la nariz figura calentar, '
                           'humedecer y {Filtrar el aire}.',
                           'La nariz también cumple la función de recibir '
                           'los impulsos {Olfatorios}.',
                           'La faringe es un órgano compartido por los '
                           'aparatos respiratorio y {Digestivo}.',
                           'La faringe, externamente, mide aproximadamente '
                           '{12 a 13 cm}.',
                           'La faringe se ubica por detrás de la cavidad '
                           'nasal y la boca, y por delante de {Las vértebras '
                           'cervicales}.',
                           'La parte superior de la faringe, ubicada detrás '
                           'de la nariz, se llama {Nasofaringe o '
                           'rinofaringe}.',
                           'Los sistemas que comparten la responsabilidad de '
                           'aportar oxígeno y eliminar dióxido de carbono '
                           'son el respiratorio y el {Cardiovascular}.',
                           'Si el sistema respiratorio o cardiovascular '
                           'fallan, las células empiezan a morir por {Falta '
                           'de oxígeno y acumulación de CO2}.',
                           'La constitución anatómica de la faringe incluye '
                           'un armazón fibroso, músculos y {Un revestimiento '
                           'mucoso}.']}],
  'cuadros': [{'titulo': '8.2 DIVISIÓN FISIOLÓGICA DEL APARATO RESPIRATORIO',
               'encabezados': ['Porción', 'Función'],
               'filas': [['{Conductora}', '{Conducir} el aire'],
                         ['{Respiratoria}', '{Oxigenar} la sangre']]}],
  'preguntas': [{'pregunta': 'El hombre es un ser de respiración:',
                 'alternativas': ['Anaerobia',
                                  'Aerobia',
                                  'Mixta obligatoria',
                                  'Sin oxígeno',
                                  'Fermentativa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El oxígeno interviene en el paso final de la '
                             'cadena respiratoria, que ocurre en:',
                 'alternativas': ['El citoplasma',
                                  'La membrana mitocondrial',
                                  'El núcleo',
                                  'El retículo endoplasmático',
                                  'El aparato de Golgi'],
                 'correcta': 'B'},
                {'pregunta': 'El dióxido de carbono que se elimina proviene '
                             'del metabolismo celular, específicamente de la '
                             'glucólisis y:',
                 'alternativas': ['La fotosíntesis',
                                  'El ciclo de Krebs',
                                  'La replicación del ADN',
                                  'La síntesis de proteínas',
                                  'La mitosis'],
                 'correcta': 'B'},
                {'pregunta': 'Las vías respiratorias superiores comprenden '
                             'la nariz y:',
                 'alternativas': ['Los pulmones',
                                  'La faringe',
                                  'Los bronquios',
                                  'La tráquea',
                                  'Los alvéolos'],
                 'correcta': 'B'},
                {'pregunta': 'Las vías respiratorias inferiores incluyen la '
                             'laringe, la tráquea, los bronquios y:',
                 'alternativas': ['La faringe',
                                  'Los pulmones',
                                  'La nariz',
                                  'Las fosas nasales',
                                  'Los senos paranasales'],
                 'correcta': 'B'},
                {'pregunta': 'La porción del aparato respiratorio que '
                             'conduce el aire inspirado y espirado se llama '
                             'porción:',
                 'alternativas': ['Respiratoria',
                                  'Conductora',
                                  'Alveolar exclusiva',
                                  'Bronquial exclusiva',
                                  'Nasal exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La porción del aparato respiratorio encargada '
                             'de oxigenar la sangre se llama porción:',
                 'alternativas': ['Conductora',
                                  'Respiratoria',
                                  'Nasal',
                                  'Traqueal exclusiva',
                                  'Faríngea exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La porción respiratoria comprende bronquiolos '
                             'respiratorios, conductos alveolares y:',
                 'alternativas': ['La tráquea',
                                  'Los alvéolos',
                                  'La faringe',
                                  'La laringe',
                                  'Los cornetes'],
                 'correcta': 'B'},
                {'pregunta': 'El interior de la nariz está dividido en dos '
                             'cavidades nasales por:',
                 'alternativas': ['Los cornetes',
                                  'El tabique nasal',
                                  'Las coanas',
                                  'Los senos paranasales',
                                  'La faringe'],
                 'correcta': 'B'},
                {'pregunta': 'Las proyecciones recubiertas en las paredes '
                             'laterales de la mucosa nasal se llaman:',
                 'alternativas': ['Coanas',
                                  'Cornetes',
                                  'Vestíbulos',
                                  'Meatos exclusivamente',
                                  'Senos'],
                 'correcta': 'B'},
                {'pregunta': 'Las aberturas que comunican las fosas nasales '
                             'con la faringe se llaman:',
                 'alternativas': ['Cornetes',
                                  'Coanas',
                                  'Vestíbulos',
                                  'Meatos',
                                  'Narinas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las funciones de la nariz figura '
                             'calentar, humedecer y:',
                 'alternativas': ['Oxigenar la sangre directamente',
                                  'Filtrar el aire',
                                  'Producir dióxido de carbono',
                                  'Eliminar bacterias del pulmón',
                                  'Regular la temperatura corporal total'],
                 'correcta': 'B'},
                {'pregunta': 'La nariz también cumple la función de recibir '
                             'los impulsos:',
                 'alternativas': ['Auditivos',
                                  'Olfatorios',
                                  'Visuales',
                                  'Táctiles exclusivos',
                                  'Gustativos'],
                 'correcta': 'B'},
                {'pregunta': 'La faringe es un órgano compartido por los '
                             'aparatos respiratorio y:',
                 'alternativas': ['Circulatorio',
                                  'Digestivo',
                                  'Excretor',
                                  'Nervioso',
                                  'Endocrino'],
                 'correcta': 'B'},
                {'pregunta': 'La faringe, externamente, mide '
                             'aproximadamente:',
                 'alternativas': ['2 a 3 cm',
                                  '12 a 13 cm',
                                  '30 a 40 cm',
                                  '1 metro',
                                  '50 cm'],
                 'correcta': 'B'},
                {'pregunta': 'La faringe se ubica por detrás de la cavidad '
                             'nasal y la boca, y por delante de:',
                 'alternativas': ['Los pulmones',
                                  'Las vértebras cervicales',
                                  'El esófago exclusivamente',
                                  'El corazón',
                                  'El estómago'],
                 'correcta': 'B'},
                {'pregunta': 'La parte superior de la faringe, ubicada '
                             'detrás de la nariz, se llama:',
                 'alternativas': ['Orofaringe',
                                  'Nasofaringe o rinofaringe',
                                  'Laringofaringe',
                                  'Traqueofaringe',
                                  'Bronquiofaringe'],
                 'correcta': 'B'},
                {'pregunta': 'Los sistemas que comparten la responsabilidad '
                             'de aportar oxígeno y eliminar dióxido de '
                             'carbono son el respiratorio y el:',
                 'alternativas': ['Digestivo',
                                  'Cardiovascular',
                                  'Excretor',
                                  'Nervioso',
                                  'Endocrino'],
                 'correcta': 'B'},
                {'pregunta': 'Si el sistema respiratorio o cardiovascular '
                             'fallan, las células empiezan a morir por:',
                 'alternativas': ['Exceso de oxígeno',
                                  'Falta de oxígeno y acumulación de CO2',
                                  'Exceso de glucosa',
                                  'Falta de agua',
                                  'Exceso de proteínas'],
                 'correcta': 'B'},
                {'pregunta': 'La constitución anatómica de la faringe '
                             'incluye un armazón fibroso, músculos y:',
                 'alternativas': ['Cartílago exclusivo',
                                  'Un revestimiento mucoso',
                                  'Hueso exclusivo',
                                  'Tejido adiposo exclusivo',
                                  'Solo piel'],
                 'correcta': 'B'}]},
 {'num': 9,
  'titulo': 'Coordinación',
  'secciones': [{'titulo': '9.1 EL SISTEMA NERVIOSO EN ANIMALES',
                 'items': ['El sistema nervioso lleva información desde los '
                           'órganos {sensoriales} hasta los centros de '
                           'control, generando una {respuesta}.',
                           'La unidad funcional básica del sistema nervioso '
                           'es la {neurona}, especializada en la '
                           'transducción de señales.']},
                {'titulo': '9.2 SISTEMA NERVIOSO EN INVERTEBRADOS',
                 'items': ['Los {cnidarios} son los organismos más sencillos '
                           'con células nerviosas: una red difusa de '
                           '{protoneuronas}.',
                           'Los {platelmintos} son el primer grupo con '
                           'sistema nervioso {hiponeuro}, con ganglios '
                           'cerebroides, dando inicio a la {cefalización}.',
                           'Los {nematodos} tienen un sistema nervioso '
                           'formado por un {anillo nervioso} alrededor del '
                           'esófago.',
                           'Los {anélidos} presentan dos ganglios cerebrales '
                           'desarrollados y un cordón nervioso central '
                           '{metamérico}.',
                           'Los {moluscos} más simples tienen un anillo '
                           'periesofágico con tres ganglios; los '
                           '{cefalópodos} tienen un cerebro complejo similar '
                           'al de vertebrados.',
                           'Los {artrópodos} tienen un sistema nervioso '
                           'metamérico, con cerebro dividido en '
                           'protocerebro, {deutocerebro} y tritocerebro.']},
                {'titulo': '9.3 SISTEMA NERVIOSO EN VERTEBRADOS',
                 'items': ['El sistema nervioso de los vertebrados se forma '
                           'por invaginación dorsal del {ectodermo}, dando '
                           'lugar al {tubo neural}.',
                           'Se diferencian dos regiones funcionales: el '
                           '{encéfalo} y la médula {espinal}.',
                           'El encéfalo está protegido por la caja '
                           '{craneal}; la médula espinal, por el canal '
                           '{vertebral}.']},
                {'titulo': '9.4 TIPOS DE SISTEMA NERVIOSO',
                 'items': ['El sistema nervioso {central} consiste en el '
                           'encéfalo y la médula espinal; el {periférico}, '
                           'en los nervios que recorren el cuerpo.',
                           'El sistema nervioso {somático} regula funciones '
                           'voluntarias; el sistema nervioso {autónomo} o '
                           'vegetativo regula funciones inconscientes.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El sistema nervioso lleva información desde los '
                           'órganos sensoriales hasta {Los centros de '
                           'control}.',
                           'La unidad funcional básica del sistema nervioso '
                           'es {La neurona}.',
                           'Los organismos más sencillos en tener células '
                           'nerviosas son los {Cnidarios}.',
                           'El sistema nervioso de los cnidarios se '
                           'caracteriza por ser {Una red difusa de '
                           'protoneuronas}.',
                           'El primer grupo de animales con sistema nervioso '
                           'hiponeuro son los {Platelmintos}.',
                           'El proceso de concentración de células nerviosas '
                           'en la región anterior del animal se llama '
                           '{Cefalización}.',
                           'El sistema nervioso de los nematodos se '
                           'estructura alrededor de {Un anillo nervioso '
                           'alrededor del esófago}.',
                           'Los anélidos presentan un cordón nervioso '
                           'central que se divide, en cada metámero, en {Dos '
                           'nervios laterales}.',
                           'En los cefalópodos, el sistema nervioso alcanza '
                           'una complejidad similar a la de {Los '
                           'vertebrados}.',
                           'El cerebro de los artrópodos está formado por '
                           'tres pares de ganglios, diferenciados en '
                           'protocerebro, deutocerebro y {Tritocerebro}.',
                           'En los vertebrados, el sistema nervioso se forma '
                           'por invaginación dorsal de {El ectodermo}.',
                           'La invaginación dorsal del ectodermo en '
                           'vertebrados da lugar a un cordón hueco llamado '
                           '{Tubo neural}.',
                           'En los vertebrados se diferencian dos regiones '
                           'funcionales del sistema nervioso: el encéfalo y '
                           '{La médula espinal}.',
                           'El encéfalo de los vertebrados está protegido '
                           'por {La caja craneal}.',
                           'La médula espinal de los vertebrados está '
                           'protegida por {El canal vertebral}.',
                           'El sistema nervioso central está formado por el '
                           'encéfalo y {La médula espinal}.',
                           'El sistema nervioso periférico está formado por '
                           '{Los nervios que recorren el organismo}.',
                           'El sistema nervioso que regula las funciones '
                           'voluntarias, como el movimiento muscular, se '
                           'llama sistema nervioso {Somático}.',
                           'El sistema nervioso que controla las funciones '
                           'inconscientes del organismo se llama sistema '
                           'nervioso {Autónomo o vegetativo}.',
                           'Además de la neurona, otro componente importante '
                           'del sistema nervioso, aunque no todos los '
                           'animales lo poseen, son {Las células '
                           'gliales}.']}],
  'cuadros': [{'titulo': '9.2 SISTEMA NERVIOSO POR GRUPO DE INVERTEBRADOS',
               'encabezados': ['Grupo', 'Sistema nervioso'],
               'filas': [['{Cnidarios}', 'Red difusa de {protoneuronas}'],
                         ['{Platelmintos}',
                          '{Hiponeuro}, primera cefalización'],
                         ['{Artrópodos}',
                          'Metamérico, cerebro con 3 {pares} de ganglios']]}],
  'preguntas': [{'pregunta': 'El sistema nervioso lleva información desde '
                             'los órganos sensoriales hasta:',
                 'alternativas': ['Los órganos efectores directamente',
                                  'Los centros de control',
                                  'El sistema circulatorio',
                                  'El sistema digestivo',
                                  'El sistema excretor'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad funcional básica del sistema '
                             'nervioso es:',
                 'alternativas': ['La célula glial',
                                  'La neurona',
                                  'El axón exclusivamente',
                                  'La dendrita exclusivamente',
                                  'La sinapsis exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos más sencillos en tener células '
                             'nerviosas son los:',
                 'alternativas': ['Platelmintos',
                                  'Cnidarios',
                                  'Nematodos',
                                  'Anélidos',
                                  'Artrópodos'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso de los cnidarios se '
                             'caracteriza por ser:',
                 'alternativas': ['Muy centralizado',
                                  'Una red difusa de protoneuronas',
                                  'Un cerebro complejo',
                                  'Un tubo neural',
                                  'Un sistema hiponeuro avanzado'],
                 'correcta': 'B'},
                {'pregunta': 'El primer grupo de animales con sistema '
                             'nervioso hiponeuro son los:',
                 'alternativas': ['Cnidarios',
                                  'Platelmintos',
                                  'Moluscos',
                                  'Artrópodos',
                                  'Vertebrados'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de concentración de células '
                             'nerviosas en la región anterior del animal se '
                             'llama:',
                 'alternativas': ['Metamerización',
                                  'Cefalización',
                                  'Segmentación',
                                  'Invaginación',
                                  'Neurulación'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso de los nematodos se '
                             'estructura alrededor de:',
                 'alternativas': ['Ganglios dispersos sin conexión',
                                  'Un anillo nervioso alrededor del esófago',
                                  'Un cerebro complejo',
                                  'Un tubo neural',
                                  'La médula espinal'],
                 'correcta': 'B'},
                {'pregunta': 'Los anélidos presentan un cordón nervioso '
                             'central que se divide, en cada metámero, en:',
                 'alternativas': ['Un solo nervio',
                                  'Dos nervios laterales',
                                  'Tres nervios',
                                  'Cuatro nervios',
                                  'Ningún nervio adicional'],
                 'correcta': 'B'},
                {'pregunta': 'En los cefalópodos, el sistema nervioso '
                             'alcanza una complejidad similar a la de:',
                 'alternativas': ['Los cnidarios',
                                  'Los vertebrados',
                                  'Los platelmintos',
                                  'Los nematodos',
                                  'Ningún otro grupo'],
                 'correcta': 'B'},
                {'pregunta': 'El cerebro de los artrópodos está formado por '
                             'tres pares de ganglios, diferenciados en '
                             'protocerebro, deutocerebro y:',
                 'alternativas': ['Mesocerebro',
                                  'Tritocerebro',
                                  'Metacerebro',
                                  'Endocerebro',
                                  'Ectocerebro'],
                 'correcta': 'B'},
                {'pregunta': 'En los vertebrados, el sistema nervioso se '
                             'forma por invaginación dorsal de:',
                 'alternativas': ['El endodermo',
                                  'El ectodermo',
                                  'El mesodermo',
                                  'La notocorda exclusiva',
                                  'El celoma'],
                 'correcta': 'B'},
                {'pregunta': 'La invaginación dorsal del ectodermo en '
                             'vertebrados da lugar a un cordón hueco '
                             'llamado:',
                 'alternativas': ['Notocorda',
                                  'Tubo neural',
                                  'Celoma',
                                  'Blastocele',
                                  'Arquenterón'],
                 'correcta': 'B'},
                {'pregunta': 'En los vertebrados se diferencian dos regiones '
                             'funcionales del sistema nervioso: el encéfalo '
                             'y:',
                 'alternativas': ['El corazón',
                                  'La médula espinal',
                                  'El hígado',
                                  'Los pulmones',
                                  'Los riñones'],
                 'correcta': 'B'},
                {'pregunta': 'El encéfalo de los vertebrados está protegido '
                             'por:',
                 'alternativas': ['El canal vertebral',
                                  'La caja craneal',
                                  'La piel exclusivamente',
                                  'Los músculos exclusivamente',
                                  'El tejido adiposo'],
                 'correcta': 'B'},
                {'pregunta': 'La médula espinal de los vertebrados está '
                             'protegida por:',
                 'alternativas': ['La caja craneal',
                                  'El canal vertebral',
                                  'La piel exclusivamente',
                                  'El diafragma',
                                  'Las costillas exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso central está formado por '
                             'el encéfalo y:',
                 'alternativas': ['Los nervios periféricos',
                                  'La médula espinal',
                                  'Los ganglios simpáticos',
                                  'Las glándulas endocrinas',
                                  'Los órganos sensoriales'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso periférico está formado '
                             'por:',
                 'alternativas': ['Solo el encéfalo',
                                  'Los nervios que recorren el organismo',
                                  'Solo la médula espinal',
                                  'Solo el cerebelo',
                                  'Solo el bulbo raquídeo'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso que regula las funciones '
                             'voluntarias, como el movimiento muscular, se '
                             'llama sistema nervioso:',
                 'alternativas': ['Autónomo',
                                  'Somático',
                                  'Simpático exclusivo',
                                  'Parasimpático exclusivo',
                                  'Entérico'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso que controla las funciones '
                             'inconscientes del organismo se llama sistema '
                             'nervioso:',
                 'alternativas': ['Somático',
                                  'Autónomo o vegetativo',
                                  'Central exclusivo',
                                  'Periférico exclusivo',
                                  'Motor exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Además de la neurona, otro componente '
                             'importante del sistema nervioso, aunque no '
                             'todos los animales lo poseen, son:',
                 'alternativas': ['Los eritrocitos',
                                  'Las células gliales',
                                  'Los plaquetas',
                                  'Los linfocitos',
                                  'Los osteocitos'],
                 'correcta': 'B'}]},
 {'num': 10,
  'titulo': 'Reproducción',
  'secciones': [{'titulo': '10.1 REPRODUCCIÓN ASEXUAL O AGÁMICA',
                 'items': ['En la reproducción {asexual} interviene un solo '
                           'organismo, sin fusión de {gametos}.',
                           'La descendencia asexual es genéticamente '
                           '{idéntica} entre sí y al progenitor.',
                           'En la reproducción asexual participan células '
                           '{somáticas}.']},
                {'titulo': '10.2 TIPOS DE REPRODUCCIÓN ASEXUAL',
                 'items': ['La {escisión binaria}, o bipartición, se da por '
                           'estrangulación en el plano medio, obteniendo dos '
                           'nuevos individuos.',
                           'La escisión binaria {transversal} pasa por el '
                           'eje central en ángulo recto, como en '
                           '{Paramecium}.',
                           'La escisión binaria {longitudinal} escinde al '
                           'organismo a lo largo, como en {Euglena}.',
                           'La {gemación} forma una yema o botón que se '
                           'rodea de citoplasma; ocurre en poríferos y '
                           '{celentéreos}.',
                           'Una forma especial de gemación es la '
                           '{estrobilación}, presente en medusas y '
                           '{céstodos}.',
                           'La {esporulación} consiste en divisiones '
                           'mitóticas que liberan esporas; ejemplo: '
                           '{Plasmodium}, causante de la malaria.',
                           'La {fragmentación} es la escisión del progenitor '
                           'en partes, cada una capaz de originar un nuevo '
                           'animal, como en {planarias}.',
                           'El fenómeno de desprender apéndices o la cola '
                           'ante el peligro se llama {autotomía}.']},
                {'titulo': '10.3 REPRODUCCIÓN CELULAR',
                 'items': ['La capacidad de perpetuar la especie es la '
                           'característica que mejor distingue a los seres '
                           '{vivos}.',
                           'En organismos eucariotas existen dos tipos de '
                           'división: la {mitosis}, que produce células '
                           'genéticamente idénticas, y la {meiosis}, con la '
                           'mitad del contenido genético.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['En la reproducción asexual interviene {Un solo '
                           'organismo}.',
                           'La descendencia producida por reproducción '
                           'asexual es, respecto al progenitor '
                           '{Genéticamente idéntica}.',
                           'En la reproducción asexual participan células de '
                           'tipo {Somáticas}.',
                           'La escisión binaria se da por una estrangulación '
                           'en {El plano medio del organismo}.',
                           'La escisión binaria transversal ocurre, por '
                           'ejemplo, en {Paramecium}.',
                           'La escisión binaria longitudinal ocurre, por '
                           'ejemplo, en {Euglena o Astasia}.',
                           'La formación de una yema o botón que se rodea de '
                           'citoplasma se llama {Gemación}.',
                           'La gemación ocurre, entre otros organismos, en '
                           'poríferos y {Celentéreos}.',
                           'Una forma especial de gemación, presente en '
                           'medusas y céstodos, se llama {Estrobilación}.',
                           'La esporulación consiste en divisiones mitóticas '
                           'del núcleo que finalmente liberan {Esporas}.',
                           'El Plasmodium, agente causante de la malaria, se '
                           'reproduce por {Esporulación}.',
                           'La escisión del progenitor en dos o más partes, '
                           'cada una capaz de originar un nuevo animal, se '
                           'llama {Fragmentación}.',
                           'La fragmentación se observa, por ejemplo, en '
                           'estrellas de mar y {Planarias}.',
                           'El fenómeno por el cual un crustáceo o lagarto '
                           'desprende un apéndice o la cola ante el peligro '
                           'se llama {Autotomía}.',
                           'La reproducción asexual es común en '
                           'microorganismos, plantas y animales de '
                           'organización {Simple}.',
                           'La característica que mejor distingue a los '
                           'seres vivos de la materia no viva es la '
                           'capacidad de {Perpetuar su propia especie}.',
                           'En organismos eucariotas existen dos tipos de '
                           'división celular: mitosis y {Meiosis}.',
                           'La división celular que produce células '
                           'genéticamente idénticas a la célula madre es {La '
                           'mitosis}.',
                           'La división celular que produce células con la '
                           'mitad del contenido genético de la célula madre '
                           'es {La meiosis}.',
                           'Rudolf Virchow resumió el concepto de '
                           'continuidad celular con el axioma en latín '
                           '{Omnis cellula e cellula}.']}],
  'cuadros': [{'titulo': '10.2 TIPOS DE REPRODUCCIÓN ASEXUAL',
               'encabezados': ['Tipo', 'Ejemplo'],
               'filas': [['{Escisión binaria}', '{Paramecium}, Euglena'],
                         ['{Gemación}', '{Hidra}, esponjas'],
                         ['{Esporulación}', '{Plasmodium}'],
                         ['{Fragmentación}',
                          '{Planaria}, estrella de mar']]}],
  'preguntas': [{'pregunta': 'En la reproducción asexual interviene:',
                 'alternativas': ['Dos organismos',
                                  'Un solo organismo',
                                  'Solo gametos masculinos',
                                  'Solo gametos femeninos',
                                  'Ningún organismo'],
                 'correcta': 'B'},
                {'pregunta': 'La descendencia producida por reproducción '
                             'asexual es, respecto al progenitor:',
                 'alternativas': ['Genéticamente diferente',
                                  'Genéticamente idéntica',
                                  'Parcialmente similar solamente',
                                  'Sin ninguna relación genética',
                                  'Siempre mutada'],
                 'correcta': 'B'},
                {'pregunta': 'En la reproducción asexual participan células '
                             'de tipo:',
                 'alternativas': ['Sexuales o gametos',
                                  'Somáticas',
                                  'Solo espermatozoides',
                                  'Solo óvulos',
                                  'Ninguna célula específica'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria se da por una '
                             'estrangulación en:',
                 'alternativas': ['El polo de la célula',
                                  'El plano medio del organismo',
                                  'El núcleo exclusivamente',
                                  'La membrana externa solamente',
                                  'Ningún punto específico'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria transversal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Euglena',
                                  'Paramecium',
                                  'Hidra',
                                  'Plasmodium',
                                  'Planaria'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria longitudinal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Paramecium',
                                  'Euglena o Astasia',
                                  'Hidra',
                                  'Plasmodium',
                                  'Estrella de mar'],
                 'correcta': 'B'},
                {'pregunta': 'La formación de una yema o botón que se rodea '
                             'de citoplasma se llama:',
                 'alternativas': ['Escisión binaria',
                                  'Gemación',
                                  'Esporulación',
                                  'Fragmentación',
                                  'Autotomía'],
                 'correcta': 'B'},
                {'pregunta': 'La gemación ocurre, entre otros organismos, en '
                             'poríferos y:',
                 'alternativas': ['Mamíferos',
                                  'Celentéreos',
                                  'Aves',
                                  'Reptiles',
                                  'Peces'],
                 'correcta': 'B'},
                {'pregunta': 'Una forma especial de gemación, presente en '
                             'medusas y céstodos, se llama:',
                 'alternativas': ['Fragmentación',
                                  'Estrobilación',
                                  'Autotomía',
                                  'Esporulación',
                                  'Bipartición'],
                 'correcta': 'B'},
                {'pregunta': 'La esporulación consiste en divisiones '
                             'mitóticas del núcleo que finalmente liberan:',
                 'alternativas': ['Gametos',
                                  'Esporas',
                                  'Yemas',
                                  'Fragmentos',
                                  'Larvas'],
                 'correcta': 'B'},
                {'pregunta': 'El Plasmodium, agente causante de la malaria, '
                             'se reproduce por:',
                 'alternativas': ['Gemación',
                                  'Esporulación',
                                  'Fragmentación',
                                  'Escisión binaria',
                                  'Autotomía'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión del progenitor en dos o más '
                             'partes, cada una capaz de originar un nuevo '
                             'animal, se llama:',
                 'alternativas': ['Gemación',
                                  'Fragmentación',
                                  'Esporulación',
                                  'Bipartición',
                                  'Estrobilación'],
                 'correcta': 'B'},
                {'pregunta': 'La fragmentación se observa, por ejemplo, en '
                             'estrellas de mar y:',
                 'alternativas': ['Mamíferos',
                                  'Planarias',
                                  'Aves',
                                  'Reptiles',
                                  'Peces óseos'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno por el cual un crustáceo o lagarto '
                             'desprende un apéndice o la cola ante el '
                             'peligro se llama:',
                 'alternativas': ['Fragmentación',
                                  'Autotomía',
                                  'Gemación',
                                  'Esporulación',
                                  'Escisión'],
                 'correcta': 'B'},
                {'pregunta': 'La reproducción asexual es común en '
                             'microorganismos, plantas y animales de '
                             'organización:',
                 'alternativas': ['Muy compleja',
                                  'Simple',
                                  'Exclusivamente vertebrada',
                                  'Exclusivamente mamífera',
                                  'Sin organización'],
                 'correcta': 'B'},
                {'pregunta': 'La característica que mejor distingue a los '
                             'seres vivos de la materia no viva es la '
                             'capacidad de:',
                 'alternativas': ['Moverse',
                                  'Perpetuar su propia especie',
                                  'Cambiar de color',
                                  'Producir sonidos',
                                  'Emitir luz'],
                 'correcta': 'B'},
                {'pregunta': 'En organismos eucariotas existen dos tipos de '
                             'división celular: mitosis y:',
                 'alternativas': ['Gemación',
                                  'Meiosis',
                                  'Esporulación',
                                  'Fragmentación',
                                  'Escisión binaria'],
                 'correcta': 'B'},
                {'pregunta': 'La división celular que produce células '
                             'genéticamente idénticas a la célula madre es:',
                 'alternativas': ['La meiosis',
                                  'La mitosis',
                                  'La gemación',
                                  'La esporulación',
                                  'La fragmentación'],
                 'correcta': 'B'},
                {'pregunta': 'La división celular que produce células con la '
                             'mitad del contenido genético de la célula '
                             'madre es:',
                 'alternativas': ['La mitosis',
                                  'La meiosis',
                                  'La gemación',
                                  'La fragmentación',
                                  'La escisión binaria'],
                 'correcta': 'B'},
                {'pregunta': 'Rudolf Virchow resumió el concepto de '
                             'continuidad celular con el axioma en latín:',
                 'alternativas': ['In vino veritas',
                                  'Omnis cellula e cellula',
                                  'Carpe diem',
                                  'Cogito ergo sum',
                                  'Ad astra per aspera'],
                 'correcta': 'B'}]},
 {'num': 11,
  'titulo': 'Genética',
  'secciones': [{'titulo': '11.1 CONCEPTO Y RAMAS DE LA GENÉTICA',
                 'items': ['«Genética» deriva de la raíz griega «gen», que '
                           'significa «{llegar} a ser».',
                           'La genética estudia todo lo relacionado con la '
                           '{herencia} biológica de los seres vivos.',
                           'La {genética molecular} estudia la organización, '
                           'replicación y expresión del {ADN}.',
                           'La {genética de poblaciones} estudia el conjunto '
                           'de genes de una población, relacionada con la '
                           '{evolución}.',
                           'La {genética clásica} o de transmisión estudia '
                           'cómo cada organismo hereda y transmite sus '
                           '{genes}.',
                           '{Gregor Mendel} descubrió cómo los cromosomas '
                           'transmiten las características hereditarias.']},
                {'titulo': '11.2 TERMINOLOGÍA GENÉTICA',
                 'items': ['El {gen} es la unidad de la herencia que produce '
                           'la expresión característica observable.',
                           'El {locus} es el sitio específico en la cadena '
                           'nucleotídica donde se encuentra el gen.',
                           'El {alelo} es cada una de las variantes génicas '
                           'que determinan un carácter.',
                           'El alelo {dominante} se manifiesta siempre y se '
                           'representa con letra {mayúscula}.',
                           'El alelo {recesivo} se manifiesta solo si no '
                           'está el dominante, y se representa con letra '
                           '{minúscula}.',
                           'El {fenotipo} es la expresión observable '
                           'determinada por el genotipo, «lo que se ve».',
                           'El {genotipo} es la dotación genética del '
                           'individuo para un carácter determinado.',
                           'El {homocigoto} porta dos alelos idénticos; el '
                           '{heterocigoto} porta dos alelos distintos.',
                           'El {genoma} es el conjunto de genes de una '
                           'especie.']},
                {'titulo': '11.3 IMPORTANCIA Y APLICACIONES',
                 'items': ['En la agricultura y ganadería se aplica la '
                           '{selección artificial} para mejorar especies.',
                           'En {biotecnología}, bacterias y hongos '
                           'manipulados genéticamente sintetizan '
                           'medicamentos.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El término «genética» deriva de la raíz griega '
                           '«gen», que significa {Llegar a ser}.',
                           'La genética es la rama de la biología que '
                           'estudia {La herencia biológica de los seres '
                           'vivos}.',
                           'La rama de la genética que estudia la '
                           'organización y replicación del ADN es la '
                           'genética {Molecular}.',
                           'La rama de la genética que estudia el conjunto '
                           'de genes de una población, vinculada a la '
                           'evolución, es la genética {De poblaciones}.',
                           'La rama de la genética que estudia cómo un '
                           'organismo hereda y transmite sus genes es la '
                           'genética {De poblaciones}.',
                           'El científico asociado a la genética clásica, '
                           'descubridor de las leyes de la herencia, es '
                           '{Gregor Mendel}.',
                           'La unidad de la herencia que produce la '
                           'expresión característica observable se llama '
                           '{Gen}.',
                           'El sitio específico en la cadena nucleotídica '
                           'donde se encuentra un gen se llama {Locus}.',
                           'Cada una de las variantes génicas que determinan '
                           'un carácter se llama {Alelo}.',
                           'El alelo que se manifiesta siempre, representado '
                           'con letra mayúscula, se llama alelo {Dominante}.',
                           'El alelo que solo se manifiesta si no está '
                           'presente el dominante se llama alelo {Recesivo}.',
                           'La expresión observable determinada por el '
                           'genotipo, «lo que se ve», se llama {Fenotipo}.',
                           'La dotación genética de un individuo para un '
                           'carácter determinado se llama {Genotipo}.',
                           'El individuo que porta dos alelos idénticos para '
                           'un carácter se llama {Homocigoto}.',
                           'El individuo que porta dos alelos distintos para '
                           'un carácter se llama {Heterocigoto}.',
                           'El conjunto de genes de una especie se llama '
                           '{Genoma}.',
                           'AA se representa como un ejemplo de genotipo '
                           '{Homocigoto dominante}.',
                           'Aa se representa como un ejemplo de genotipo '
                           '{Heterocigoto}.',
                           'En agricultura y ganadería, la elección de '
                           'especies con rasgos deseables se llama '
                           '{Selección artificial}.',
                           'En biotecnología, medicamentos son sintetizados '
                           'por bacterias y hongos que han sido {Manipulados '
                           'genéticamente}.']}],
  'cuadros': [{'titulo': '11.2 TÉRMINOS GENÉTICOS BÁSICOS',
               'encabezados': ['Término', 'Significado'],
               'filas': [['{Gen}', 'Unidad de la {herencia}'],
                         ['{Alelo}', 'Variante {génica}'],
                         ['{Fenotipo}', 'Lo que se {observa}'],
                         ['{Genotipo}', 'Dotación {genética}']]}],
  'preguntas': [{'pregunta': 'El término «genética» deriva de la raíz griega '
                             '«gen», que significa:',
                 'alternativas': ['Herencia',
                                  'Llegar a ser',
                                  'Célula',
                                  'Cromosoma',
                                  'Especie'],
                 'correcta': 'B'},
                {'pregunta': 'La genética es la rama de la biología que '
                             'estudia:',
                 'alternativas': ['Solo la evolución',
                                  'La herencia biológica de los seres vivos',
                                  'Solo la ecología',
                                  'Solo la fotosíntesis',
                                  'Solo la nutrición'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia la '
                             'organización y replicación del ADN es la '
                             'genética:',
                 'alternativas': ['Clásica',
                                  'Molecular',
                                  'De poblaciones',
                                  'Aplicada exclusiva',
                                  'Ambiental'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia el conjunto '
                             'de genes de una población, vinculada a la '
                             'evolución, es la genética:',
                 'alternativas': ['Molecular',
                                  'De poblaciones',
                                  'Clásica',
                                  'Aplicada',
                                  'Celular'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia cómo un '
                             'organismo hereda y transmite sus genes es la '
                             'genética:',
                 'alternativas': ['Molecular',
                                  'De poblaciones',
                                  'Clásica o de transmisión',
                                  'Ambiental',
                                  'Aplicada'],
                 'correcta': 'B'},
                {'pregunta': 'El científico asociado a la genética clásica, '
                             'descubridor de las leyes de la herencia, es:',
                 'alternativas': ['Darwin',
                                  'Gregor Mendel',
                                  'Watson',
                                  'Crick',
                                  'Virchow'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad de la herencia que produce la '
                             'expresión característica observable se llama:',
                 'alternativas': ['Locus',
                                  'Gen',
                                  'Alelo',
                                  'Fenotipo',
                                  'Cromosoma'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio específico en la cadena nucleotídica '
                             'donde se encuentra un gen se llama:',
                 'alternativas': ['Alelo',
                                  'Locus',
                                  'Genotipo',
                                  'Fenotipo',
                                  'Genoma'],
                 'correcta': 'B'},
                {'pregunta': 'Cada una de las variantes génicas que '
                             'determinan un carácter se llama:',
                 'alternativas': ['Locus',
                                  'Alelo',
                                  'Genoma',
                                  'Cromátida',
                                  'Nucleótido'],
                 'correcta': 'B'},
                {'pregunta': 'El alelo que se manifiesta siempre, '
                             'representado con letra mayúscula, se llama '
                             'alelo:',
                 'alternativas': ['Recesivo',
                                  'Dominante',
                                  'Codominante',
                                  'Neutro',
                                  'Mutante'],
                 'correcta': 'B'},
                {'pregunta': 'El alelo que solo se manifiesta si no está '
                             'presente el dominante se llama alelo:',
                 'alternativas': ['Dominante',
                                  'Recesivo',
                                  'Codominante',
                                  'Letal',
                                  'Neutro'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión observable determinada por el '
                             'genotipo, «lo que se ve», se llama:',
                 'alternativas': ['Genotipo',
                                  'Fenotipo',
                                  'Genoma',
                                  'Locus',
                                  'Alelo'],
                 'correcta': 'B'},
                {'pregunta': 'La dotación genética de un individuo para un '
                             'carácter determinado se llama:',
                 'alternativas': ['Fenotipo',
                                  'Genotipo',
                                  'Locus',
                                  'Alelo',
                                  'Cromátida'],
                 'correcta': 'B'},
                {'pregunta': 'El individuo que porta dos alelos idénticos '
                             'para un carácter se llama:',
                 'alternativas': ['Heterocigoto',
                                  'Homocigoto',
                                  'Híbrido exclusivo',
                                  'Mutante',
                                  'Recesivo puro'],
                 'correcta': 'B'},
                {'pregunta': 'El individuo que porta dos alelos distintos '
                             'para un carácter se llama:',
                 'alternativas': ['Homocigoto',
                                  'Heterocigoto',
                                  'Puro',
                                  'Dominante puro',
                                  'Recesivo puro'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de genes de una especie se llama:',
                 'alternativas': ['Fenotipo',
                                  'Genoma',
                                  'Alelo',
                                  'Locus',
                                  'Cromátida'],
                 'correcta': 'B'},
                {'pregunta': 'AA se representa como un ejemplo de genotipo:',
                 'alternativas': ['Heterocigoto',
                                  'Homocigoto dominante',
                                  'Homocigoto recesivo',
                                  'Codominante',
                                  'Ligado al sexo'],
                 'correcta': 'B'},
                {'pregunta': 'Aa se representa como un ejemplo de genotipo:',
                 'alternativas': ['Homocigoto dominante',
                                  'Heterocigoto',
                                  'Homocigoto recesivo',
                                  'Nulo',
                                  'Letal'],
                 'correcta': 'B'},
                {'pregunta': 'En agricultura y ganadería, la elección de '
                             'especies con rasgos deseables se llama:',
                 'alternativas': ['Selección natural',
                                  'Selección artificial',
                                  'Deriva génica',
                                  'Mutación dirigida',
                                  'Migración génica'],
                 'correcta': 'B'},
                {'pregunta': 'En biotecnología, medicamentos son '
                             'sintetizados por bacterias y hongos que han '
                             'sido:',
                 'alternativas': ['Extinguidos',
                                  'Manipulados genéticamente',
                                  'Eliminados del ecosistema',
                                  'Fosilizados',
                                  'Domesticados sin cambios'],
                 'correcta': 'B'}]},
 {'num': 12,
  'titulo': 'Evolución y Origen de la Vida',
  'secciones': [{'titulo': '12.1 CONCEPTO Y ANTECEDENTES',
                 'items': ['La {evolución} es todo cambio en una población '
                           'mediante el cual se forman nuevas especies a lo '
                           'largo del tiempo.',
                           'La palabra «evolución» fue empleada por primera '
                           'vez por el naturalista suizo {Charles Bonnet}, a '
                           'mediados del siglo XVIII.',
                           'La hipótesis de Bonnet, que explicaba los '
                           'fósiles por catástrofes periódicas, se conoce '
                           'como {catastrofismo}.']},
                {'titulo': '12.2 TEORÍA DEL TRANSFORMISMO',
                 'items': ['La primera hipótesis completa de la evolución '
                           'fue de {Jean Baptiste Lamarck}, publicada en '
                           '1809 en «{Filosofía Zoológica}».',
                           'El {principio de uso y desuso} de Lamarck dice '
                           'que las estructuras que más se usan se '
                           'desarrollan.',
                           'El {principio de la herencia de los caracteres '
                           'adquiridos} sostiene que la modificación por uso '
                           'y desuso es heredable.',
                           'Lamarck ilustró su teoría con el ejemplo del '
                           '{cuello de la jirafa}, alargado por el esfuerzo '
                           'de alcanzar ramas altas.']},
                {'titulo': '12.3 TEORÍA DE LA SELECCIÓN NATURAL',
                 'items': ['{Charles Darwin} es el fundador de la teoría de '
                           'la evolución, y publicó en 1859 «{El origen de '
                           'las especies}».',
                           '{Alfred Russel Wallace} llegó a conclusiones '
                           'similares a las de Darwin de forma '
                           'independiente.',
                           'Los cuatro conceptos centrales de la selección '
                           'natural son: {variación}, sobreproducción, '
                           '{lucha por la existencia} y selección natural.',
                           'La {variación} sostiene que todos los miembros '
                           'de una especie difieren entre sí.',
                           'La {sobreproducción} incrementa las '
                           'probabilidades de que algunos vástagos '
                           'sobrevivan.',
                           'En la {selección natural}, los individuos mejor '
                           'adaptados sobreviven y transmiten sus '
                           'características.']},
                {'titulo': '12.4 MUTACIONISMO Y TEORÍA SINTÉTICA',
                 'items': ['{Hugo De Vries} publicó en 1889 «Pangénesis '
                           'intracelular», reemplazando la variación '
                           'continua por la {mutación}.',
                           'Una {mutación} es la aparición repentina de una '
                           'variante en un gen particular.',
                           '{Theodosius Dobzhansky} publicó en 1937 «La '
                           'Genética y el Origen de las Especies», dando '
                           'origen a la {Teoría Sintética}.',
                           'La Teoría Sintética combina la selección natural '
                           'de {Darwin} con las leyes de la herencia de '
                           '{Mendel} y el mutacionismo.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La evolución se define como todo cambio en una '
                           'población mediante el cual se forman {Nuevas '
                           'especies a lo largo del tiempo}.',
                           'La palabra «evolución» fue empleada por primera '
                           'vez por {Charles Bonnet}.',
                           'La hipótesis que explicaba los fósiles por '
                           'catástrofes periódicas se llama {Catastrofismo}.',
                           'La primera hipótesis completa de la evolución '
                           'fue formulada por {Lamarck}.',
                           'Lamarck publicó su hipótesis en 1809 en el libro '
                           '{Filosofía Zoológica}.',
                           'El principio de Lamarck según el cual las '
                           'estructuras más usadas se desarrollan se llama '
                           '{Uso y desuso}.',
                           'El principio de que las modificaciones por uso y '
                           'desuso son heredables se llama {Herencia de los '
                           'caracteres adquiridos}.',
                           'Lamarck ilustró su teoría con el ejemplo clásico '
                           'de {El cuello de la jirafa}.',
                           'El fundador de la teoría de la evolución por '
                           'selección natural es {Charles Darwin}.',
                           'Darwin publicó su obra principal, «El origen de '
                           'las especies», en el año {1859}.',
                           'El biólogo que llegó a conclusiones similares a '
                           'Darwin de forma independiente fue {Alfred Russel '
                           'Wallace}.',
                           'Los cuatro conceptos centrales de la selección '
                           'natural son variación, sobreproducción, lucha '
                           'por la existencia y {Selección natural}.',
                           'El concepto que sostiene que todos los miembros '
                           'de una especie difieren entre sí se llama '
                           '{Variación}.',
                           'El mecanismo que incrementa las probabilidades '
                           'de que algunos vástagos sobrevivan se llama '
                           '{Sobreproducción}.',
                           'Según la selección natural, los individuos mejor '
                           'adaptados {Sobreviven y transmiten sus '
                           'características}.',
                           'El botánico que publicó «Pangénesis '
                           'intracelular» en 1889 fue {Hugo De Vries}.',
                           'De Vries reemplazó la noción de variación '
                           'continua por la de {Variación discontinua o '
                           'mutación}.',
                           'Una mutación se define como la aparición '
                           'repentina de una variante en {Un gen particular '
                           'o grupo de genes}.',
                           'La Teoría Sintética de la evolución fue dada a '
                           'conocer por {Theodosius Dobzhansky}.',
                           'La Teoría Sintética combina la selección natural '
                           'con las leyes de la herencia de Mendel y {El '
                           'mutacionismo}.']}],
  'cuadros': [{'titulo': '12.1-12.4 TEORÍAS DE LA EVOLUCIÓN',
               'encabezados': ['Teoría', 'Autor'],
               'filas': [['{Transformismo}', '{Lamarck}'],
                         ['{Selección natural}', '{Darwin}'],
                         ['{Mutacionismo}', '{De Vries}'],
                         ['{Teoría Sintética}', '{Dobzhansky}']]}],
  'preguntas': [{'pregunta': 'La evolución se define como todo cambio en una '
                             'población mediante el cual se forman:',
                 'alternativas': ['Nuevos individuos idénticos',
                                  'Nuevas especies a lo largo del tiempo',
                                  'Solo mutaciones aisladas',
                                  'Ninguna variación',
                                  'Solo caracteres adquiridos'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «evolución» fue empleada por '
                             'primera vez por:',
                 'alternativas': ['Darwin',
                                  'Charles Bonnet',
                                  'Lamarck',
                                  'Mendel',
                                  'De Vries'],
                 'correcta': 'B'},
                {'pregunta': 'La hipótesis que explicaba los fósiles por '
                             'catástrofes periódicas se llama:',
                 'alternativas': ['Transformismo',
                                  'Catastrofismo',
                                  'Selección natural',
                                  'Mutacionismo',
                                  'Teoría sintética'],
                 'correcta': 'B'},
                {'pregunta': 'La primera hipótesis completa de la evolución '
                             'fue formulada por:',
                 'alternativas': ['Darwin',
                                  'Lamarck',
                                  'De Vries',
                                  'Dobzhansky',
                                  'Wallace'],
                 'correcta': 'B'},
                {'pregunta': 'Lamarck publicó su hipótesis en 1809 en el '
                             'libro:',
                 'alternativas': ['El origen de las especies',
                                  'Filosofía Zoológica',
                                  'Pangénesis intracelular',
                                  'La Genética y el Origen de las Especies',
                                  'Principios de Biología'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de Lamarck según el cual las '
                             'estructuras más usadas se desarrollan se '
                             'llama:',
                 'alternativas': ['Selección natural',
                                  'Uso y desuso',
                                  'Mutación espontánea',
                                  'Variación continua',
                                  'Herencia mendeliana'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de que las modificaciones por uso '
                             'y desuso son heredables se llama:',
                 'alternativas': ['Selección natural',
                                  'Herencia de los caracteres adquiridos',
                                  'Mutacionismo',
                                  'Variación discontinua',
                                  'Teoría sintética'],
                 'correcta': 'B'},
                {'pregunta': 'Lamarck ilustró su teoría con el ejemplo '
                             'clásico de:',
                 'alternativas': ['El pico del pinzón',
                                  'El cuello de la jirafa',
                                  'La resistencia bacteriana',
                                  'El color de la polilla',
                                  'Las alas del murciélago'],
                 'correcta': 'B'},
                {'pregunta': 'El fundador de la teoría de la evolución por '
                             'selección natural es:',
                 'alternativas': ['Lamarck',
                                  'Charles Darwin',
                                  'De Vries',
                                  'Mendel',
                                  'Bonnet'],
                 'correcta': 'B'},
                {'pregunta': 'Darwin publicó su obra principal, «El origen '
                             'de las especies», en el año:',
                 'alternativas': ['1809', '1859', '1889', '1937', '1758'],
                 'correcta': 'B'},
                {'pregunta': 'El biólogo que llegó a conclusiones similares '
                             'a Darwin de forma independiente fue:',
                 'alternativas': ['De Vries',
                                  'Alfred Russel Wallace',
                                  'Dobzhansky',
                                  'Lamarck',
                                  'Mendel'],
                 'correcta': 'B'},
                {'pregunta': 'Los cuatro conceptos centrales de la selección '
                             'natural son variación, sobreproducción, lucha '
                             'por la existencia y:',
                 'alternativas': ['Mutación',
                                  'Selección natural',
                                  'Herencia adquirida',
                                  'Catastrofismo',
                                  'Uso y desuso'],
                 'correcta': 'B'},
                {'pregunta': 'El concepto que sostiene que todos los '
                             'miembros de una especie difieren entre sí se '
                             'llama:',
                 'alternativas': ['Sobreproducción',
                                  'Variación',
                                  'Selección natural',
                                  'Mutación',
                                  'Herencia'],
                 'correcta': 'B'},
                {'pregunta': 'El mecanismo que incrementa las probabilidades '
                             'de que algunos vástagos sobrevivan se llama:',
                 'alternativas': ['Variación',
                                  'Sobreproducción',
                                  'Selección natural',
                                  'Mutación',
                                  'Adaptación exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Según la selección natural, los individuos '
                             'mejor adaptados:',
                 'alternativas': ['Desaparecen primero',
                                  'Sobreviven y transmiten sus '
                                  'características',
                                  'No se reproducen nunca',
                                  'Son eliminados por competencia',
                                  'No tienen ventaja alguna'],
                 'correcta': 'B'},
                {'pregunta': 'El botánico que publicó «Pangénesis '
                             'intracelular» en 1889 fue:',
                 'alternativas': ['Darwin',
                                  'Hugo De Vries',
                                  'Dobzhansky',
                                  'Lamarck',
                                  'Wallace'],
                 'correcta': 'B'},
                {'pregunta': 'De Vries reemplazó la noción de variación '
                             'continua por la de:',
                 'alternativas': ['Selección natural',
                                  'Variación discontinua o mutación',
                                  'Herencia de caracteres adquiridos',
                                  'Catastrofismo',
                                  'Uso y desuso'],
                 'correcta': 'B'},
                {'pregunta': 'Una mutación se define como la aparición '
                             'repentina de una variante en:',
                 'alternativas': ['Un organismo completo',
                                  'Un gen particular o grupo de genes',
                                  'Una especie entera',
                                  'Un ecosistema',
                                  'Una población completa'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría Sintética de la evolución fue dada a '
                             'conocer por:',
                 'alternativas': ['Darwin',
                                  'Theodosius Dobzhansky',
                                  'Lamarck',
                                  'De Vries',
                                  'Wallace'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría Sintética combina la selección '
                             'natural con las leyes de la herencia de Mendel '
                             'y:',
                 'alternativas': ['El catastrofismo',
                                  'El mutacionismo',
                                  'La teoría celular',
                                  'El transformismo puro',
                                  'La teoría del big bang'],
                 'correcta': 'B'}]},
 {'num': 13,
  'titulo': 'Ecología, Factores Ecológicos y Ecosistemas',
  'secciones': [{'titulo': '13.1 CONCEPTO DE ECOLOGÍA',
                 'items': ['«Ecología» proviene de los vocablos griegos '
                           '«{oikos}» (casa) y «{logos}» (ciencia).',
                           'El primer estudioso de las interacciones entre '
                           'seres vivos y ambiente fue {Teofrasto}, '
                           'condiscípulo de Aristóteles.',
                           'El término «Ecología» fue establecido por el '
                           'biólogo alemán {Ernest Haeckel} en {1869}.',
                           'La ecología estudia principalmente la '
                           '{Biosfera}, influenciada por la litósfera y la '
                           'atmósfera.']},
                {'titulo': '13.2 EL ECOLOGISMO Y SUS TIPOS',
                 'items': ['El {ecologismo} es el activismo de la ecología, '
                           'un movimiento cívico para el cuidado del '
                           '{ambiente}.',
                           'El ecologismo {tecnicista} busca reducir la '
                           'contaminación proponiendo energías '
                           '{alternativas}.',
                           'El ecologismo {naturalista} es ecocentrista y '
                           'busca evitar la extinción de {especies}.',
                           'El ecologismo {sociológico-político} estudia '
                           'problemas de superpoblación y {hambruna}.']},
                {'titulo': '13.3 FACTORES AMBIENTALES',
                 'items': ['Los factores ambientales se clasifican en '
                           '{bióticos} y {abióticos}.',
                           'Los factores {bióticos}, o animados, '
                           'corresponden a todos los seres {vivos}.',
                           'La {densidad poblacional} es la concentración de '
                           'individuos en un área geográfica determinada.',
                           'Las relaciones {intraespecíficas} ocurren entre '
                           'individuos de la misma especie; las '
                           '{interespecíficas}, entre especies distintas.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El término «ecología» proviene de los vocablos '
                           'griegos «oikos» y {Logos}.',
                           'El primer estudioso de las interacciones entre '
                           'seres vivos y ambiente fue {Teofrasto}.',
                           'El término «Ecología» fue establecido '
                           'formalmente por {Ernest Haeckel}.',
                           'Ernest Haeckel estableció el término «Ecología» '
                           'en el año {1869}.',
                           'Haeckel definió la ecología como el estudio de '
                           'las relaciones de los organismos con su ambiente '
                           '{Orgánico e inorgánico}.',
                           'La ecología estudia principalmente {La '
                           'biosfera}.',
                           'El activismo de la ecología, como movimiento '
                           'cívico, se llama {Ecologismo}.',
                           'El ecologismo tecnicista tiene como objetivo '
                           '{Reducir la contaminación proponiendo energías '
                           'alternativas}.',
                           'El ecologismo naturalista es una corriente '
                           'filosófica que busca {Evitar la extinción de '
                           'especies animales}.',
                           'El ecologismo sociológico-político estudia, '
                           'entre otros temas, la superpoblación y {La '
                           'hambruna en el mundo}.',
                           'Los factores ambientales se clasifican en '
                           'bióticos y {Abióticos}.',
                           'Los factores bióticos corresponden a {Todos los '
                           'seres vivos}.',
                           'La concentración de individuos de una especie en '
                           'un área geográfica se llama {Densidad '
                           'poblacional}.',
                           'Las relaciones entre individuos de la misma '
                           'especie se llaman relaciones {Intraespecíficas}.',
                           'Las relaciones entre individuos de especies '
                           'distintas se llaman relaciones '
                           '{Interespecíficas}.',
                           'El ambiente también se suele denominar entorno, '
                           'medio ambiente o {Naturaleza}.',
                           'En el ambiente se agrupan seres en dos '
                           'categorías: vivos y {No vivos}.',
                           'Debido a que los humanos forman parte de la red '
                           'de vida de la Tierra, sus actividades económicas '
                           'y políticas tienen {Profundas implicaciones '
                           'ecológicas}.',
                           'El ecologismo surge como una nueva forma de '
                           'hacer política centrada en {El desarrollo '
                           'sostenible}.']}],
  'cuadros': [{'titulo': '13.3 FACTORES AMBIENTALES',
               'encabezados': ['Tipo', 'Corresponde a'],
               'filas': [['{Bióticos}', 'Seres {vivos}'],
                         ['{Abióticos}', 'Ambiente {físico} no viviente']]}],
  'preguntas': [{'pregunta': 'El término «ecología» proviene de los vocablos '
                             'griegos «oikos» y:',
                 'alternativas': ['Bios', 'Logos', 'Physis', 'Genos', 'Zoon'],
                 'correcta': 'B'},
                {'pregunta': '«Oikos» en griego significa:',
                 'alternativas': ['Ciencia',
                                  'Casa',
                                  'Vida',
                                  'Estudio',
                                  'Naturaleza'],
                 'correcta': 'B'},
                {'pregunta': 'El primer estudioso de las interacciones entre '
                             'seres vivos y ambiente fue:',
                 'alternativas': ['Aristóteles',
                                  'Teofrasto',
                                  'Haeckel',
                                  'Darwin',
                                  'Linneo'],
                 'correcta': 'B'},
                {'pregunta': 'El término «Ecología» fue establecido '
                             'formalmente por:',
                 'alternativas': ['Charles Darwin',
                                  'Ernest Haeckel',
                                  'Teofrasto',
                                  'Gregor Mendel',
                                  'Alfred Wallace'],
                 'correcta': 'B'},
                {'pregunta': 'Ernest Haeckel estableció el término '
                             '«Ecología» en el año:',
                 'alternativas': ['1809', '1859', '1869', '1937', '1789'],
                 'correcta': 'C'},
                {'pregunta': 'Haeckel definió la ecología como el estudio de '
                             'las relaciones de los organismos con su '
                             'ambiente:',
                 'alternativas': ['Solo orgánico',
                                  'Orgánico e inorgánico',
                                  'Solo inorgánico',
                                  'Solo social',
                                  'Solo económico'],
                 'correcta': 'B'},
                {'pregunta': 'La ecología estudia principalmente:',
                 'alternativas': ['La atmósfera exclusivamente',
                                  'La biosfera',
                                  'Solo la litósfera',
                                  'Solo el clima',
                                  'Solo los océanos'],
                 'correcta': 'B'},
                {'pregunta': 'El activismo de la ecología, como movimiento '
                             'cívico, se llama:',
                 'alternativas': ['Ambientalismo exclusivo',
                                  'Ecologismo',
                                  'Conservacionismo exclusivo',
                                  'Naturalismo exclusivo',
                                  'Sostenibilismo'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo tecnicista tiene como objetivo:',
                 'alternativas': ['Evitar la extinción de especies',
                                  'Reducir la contaminación proponiendo '
                                  'energías alternativas',
                                  'Estudiar la superpoblación',
                                  'Proteger la vida anímica',
                                  'Viajar a otros planetas'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo naturalista es una corriente '
                             'filosófica que busca:',
                 'alternativas': ['Reducir la contaminación técnica',
                                  'Evitar la extinción de especies animales',
                                  'Estudiar recursos limitados',
                                  'Promover el amor espiritual',
                                  'Analizar la superpoblación'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo sociológico-político estudia, '
                             'entre otros temas, la superpoblación y:',
                 'alternativas': ['La extinción de especies exclusivamente',
                                  'La hambruna en el mundo',
                                  'Solo la energía nuclear',
                                  'Solo el reciclaje',
                                  'Solo la deforestación'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores ambientales se clasifican en '
                             'bióticos y:',
                 'alternativas': ['Ecológicos',
                                  'Abióticos',
                                  'Orgánicos exclusivos',
                                  'Antrópicos exclusivos',
                                  'Naturales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores bióticos corresponden a:',
                 'alternativas': ['El ambiente físico no viviente',
                                  'Todos los seres vivos',
                                  'Solo el clima',
                                  'Solo el suelo',
                                  'Solo el agua'],
                 'correcta': 'B'},
                {'pregunta': 'La concentración de individuos de una especie '
                             'en un área geográfica se llama:',
                 'alternativas': ['Biomasa',
                                  'Densidad poblacional',
                                  'Nicho ecológico',
                                  'Bioma',
                                  'Hábitat exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Las relaciones entre individuos de la misma '
                             'especie se llaman relaciones:',
                 'alternativas': ['Interespecíficas',
                                  'Intraespecíficas',
                                  'Ecológicas generales',
                                  'Tróficas exclusivas',
                                  'Simbióticas exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Las relaciones entre individuos de especies '
                             'distintas se llaman relaciones:',
                 'alternativas': ['Intraespecíficas',
                                  'Interespecíficas',
                                  'Poblacionales exclusivas',
                                  'Bióticas generales',
                                  'Abióticas'],
                 'correcta': 'B'},
                {'pregunta': 'El ambiente también se suele denominar '
                             'entorno, medio ambiente o:',
                 'alternativas': ['Ecosistema exclusivo',
                                  'Naturaleza',
                                  'Bioma exclusivo',
                                  'Hábitat exclusivo',
                                  'Nicho'],
                 'correcta': 'B'},
                {'pregunta': 'En el ambiente se agrupan seres en dos '
                             'categorías: vivos y:',
                 'alternativas': ['Extintos',
                                  'No vivos',
                                  'Domesticados',
                                  'Migratorios',
                                  'Fósiles'],
                 'correcta': 'B'},
                {'pregunta': 'Debido a que los humanos forman parte de la '
                             'red de vida de la Tierra, sus actividades '
                             'económicas y políticas tienen:',
                 'alternativas': ['Ninguna implicación ecológica',
                                  'Profundas implicaciones ecológicas',
                                  'Solo implicaciones económicas',
                                  'Solo implicaciones sociales',
                                  'Efectos neutros'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo surge como una nueva forma de '
                             'hacer política centrada en:',
                 'alternativas': ['El crecimiento económico ilimitado',
                                  'El desarrollo sostenible',
                                  'La industrialización acelerada',
                                  'La explotación de recursos',
                                  'El comercio internacional'],
                 'correcta': 'B'}]},
 {'num': 14,
  'titulo': 'Flujo de Energía y Ciclos Biogeoquímicos',
  'secciones': [{'titulo': '14.1 ENERGÍA CINÉTICA Y POTENCIAL',
                 'items': ['La energía solar llega a la Tierra en partículas '
                           'energéticas llamadas {fotones}.',
                           'La energía {cinética} es la energía en '
                           'movimiento, como la energía mecánica, la luz o '
                           'el calor.',
                           'La energía {potencial} es la energía almacenada, '
                           'disponible para llevar a cabo trabajo, como en '
                           'la leña o el petróleo.']},
                {'titulo': '14.2 LEYES DE LA TERMODINÁMICA',
                 'items': ['Los ecosistemas son sistemas termodinámicamente '
                           '{abiertos}: la energía y materia entran y salen '
                           'de ellos.',
                           'La {primera ley} de la termodinámica, o '
                           'principio de conservación de la energía, fue '
                           'postulada por {R. Mayer} en 1841.',
                           'Según la primera ley, la energía no se {crea} ni '
                           'se destruye, solo se {transforma}.',
                           'La {segunda ley} de la termodinámica, o ley de '
                           'la {entropía}, indica que al transformar '
                           'energía, parte se degrada en forma no '
                           'aprovechable.',
                           'Cuando la energía se transfiere de un organismo '
                           'a otro, gran parte se degrada como {calor}.']},
                {'titulo': '14.3 LA LEY DEL DIEZMO ECOLÓGICO',
                 'items': ['Según la Ley del {Diezmo Ecológico}, al pasar de '
                           'un nivel trófico a otro, solo se transfiere el '
                           '{10}% de la energía.',
                           'Los organismos usan el {90}% de la energía '
                           'capturada en su propio metabolismo y movimiento.',
                           'Un vegetal aprovecha el 90% de la energía solar '
                           'fijada; un {herbívoro} que lo consume solo '
                           'aprovecha el {10}% de esa energía.']},
                {'titulo': '14.4 EL FLUJO DE ENERGÍA',
                 'items': ['Aproximadamente el {99,98}% de la energía '
                           'disponible en la Tierra proviene del {sol}.',
                           'El resto de la energía proviene de las mareas, '
                           'la energía {nuclear}, la termal y la '
                           'gravitacional.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La energía solar llega a la Tierra en forma de '
                           'partículas energéticas llamadas {Fotones}.',
                           'La energía en movimiento, como la energía '
                           'mecánica o el calor, se llama energía '
                           '{Cinética}.',
                           'La energía almacenada, disponible para llevar a '
                           'cabo trabajo, se llama energía {Potencial}.',
                           'Los ecosistemas son sistemas termodinámicamente '
                           '{Abiertos}.',
                           'La primera ley de la termodinámica también se '
                           'conoce como el principio de {La conservación de '
                           'la energía}.',
                           'La primera ley de la termodinámica fue postulada '
                           'en 1841 por {R. Mayer}.',
                           'Según la primera ley de la termodinámica, la '
                           'energía {No se crea ni se destruye, solo se '
                           'transforma}.',
                           'La segunda ley de la termodinámica también se '
                           'conoce como ley de {La entropía o degradación de '
                           'la energía}.',
                           'Según la segunda ley de la termodinámica, al '
                           'transformarse la energía {Parte se degrada en '
                           'una forma no trasladable}.',
                           'Cuando la energía se transfiere de un organismo '
                           'a otro en la cadena alimenticia, gran parte se '
                           'degrada en forma de {Calor}.',
                           'Según la Ley del Diezmo Ecológico, al pasar de '
                           'un nivel trófico a otro se transfiere {El 10% de '
                           'la energía}.',
                           'Según la Ley del Diezmo Ecológico, los '
                           'organismos usan en su propio metabolismo {El 90% '
                           'de la energía capturada}.',
                           'Un vegetal aprovecha para sus funciones de '
                           'supervivencia aproximadamente {90% de la energía '
                           'solar fijada}.',
                           'Un herbívoro que consume un vegetal solo puede '
                           'aprovechar de la energía fijada por este {El '
                           '10%}.',
                           'Un carnívoro que consume a un herbívoro solo '
                           'puede aprovechar de la energía que este recibió '
                           '{El 10%}.',
                           'El porcentaje aproximado de la energía '
                           'disponible en la Tierra que proviene del sol es '
                           '{99,98%}.',
                           'Además del sol, otras fuentes de energía '
                           'terrestre incluyen las mareas, la energía '
                           'nuclear, la termal y la {Gravitacional}.',
                           'La radiación solar que llega a la superficie '
                           'terrestre varía según la latitud, la altura, la '
                           'orografía y {La nubosidad}.',
                           'La historia de la energía en un ecosistema está '
                           'en gran parte relacionada con la historia de {El '
                           'carbono}.',
                           'La energía almacenada en los enlaces químicos de '
                           'los carbohidratos proviene originalmente de {La '
                           'fotosíntesis}.']}],
  'cuadros': [{'titulo': '14.2 LAS DOS LEYES DE LA TERMODINÁMICA',
               'encabezados': ['Ley', 'Enunciado'],
               'filas': [['{Primera}',
                          'La energía no se crea ni se {destruye}, solo se '
                          'transforma'],
                         ['{Segunda}',
                          'Parte de la energía se {degrada} como calor no '
                          'aprovechable']]}],
  'preguntas': [{'pregunta': 'La energía solar llega a la Tierra en forma de '
                             'partículas energéticas llamadas:',
                 'alternativas': ['Electrones',
                                  'Fotones',
                                  'Neutrones',
                                  'Iones',
                                  'Quarks'],
                 'correcta': 'B'},
                {'pregunta': 'La energía en movimiento, como la energía '
                             'mecánica o el calor, se llama energía:',
                 'alternativas': ['Potencial',
                                  'Cinética',
                                  'Química exclusiva',
                                  'Nuclear exclusiva',
                                  'Radiante exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La energía almacenada, disponible para llevar '
                             'a cabo trabajo, se llama energía:',
                 'alternativas': ['Cinética',
                                  'Potencial',
                                  'Térmica exclusiva',
                                  'Mecánica exclusiva',
                                  'Lumínica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Los ecosistemas son sistemas '
                             'termodinámicamente:',
                 'alternativas': ['Cerrados',
                                  'Abiertos',
                                  'Aislados',
                                  'Neutros',
                                  'Estáticos'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ley de la termodinámica también se '
                             'conoce como el principio de:',
                 'alternativas': ['La entropía',
                                  'La conservación de la energía',
                                  'El diezmo ecológico',
                                  'La selección natural',
                                  'La herencia'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ley de la termodinámica fue '
                             'postulada en 1841 por:',
                 'alternativas': ['Darwin',
                                  'R. Mayer',
                                  'Haeckel',
                                  'Mendel',
                                  'Dobzhansky'],
                 'correcta': 'B'},
                {'pregunta': 'Según la primera ley de la termodinámica, la '
                             'energía:',
                 'alternativas': ['Se crea constantemente',
                                  'No se crea ni se destruye, solo se '
                                  'transforma',
                                  'Desaparece con el tiempo',
                                  'Se multiplica en cada transformación',
                                  'Se pierde totalmente en cada ciclo'],
                 'correcta': 'B'},
                {'pregunta': 'La segunda ley de la termodinámica también se '
                             'conoce como ley de:',
                 'alternativas': ['La conservación de la energía',
                                  'La entropía o degradación de la energía',
                                  'El diezmo ecológico',
                                  'La selección natural',
                                  'La herencia'],
                 'correcta': 'B'},
                {'pregunta': 'Según la segunda ley de la termodinámica, al '
                             'transformarse la energía:',
                 'alternativas': ['Se conserva completamente aprovechable',
                                  'Parte se degrada en una forma no '
                                  'trasladable',
                                  'Aumenta su cantidad total',
                                  'Se transforma en materia',
                                  'Desaparece por completo'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando la energía se transfiere de un '
                             'organismo a otro en la cadena alimenticia, '
                             'gran parte se degrada en forma de:',
                 'alternativas': ['Luz',
                                  'Calor',
                                  'Sonido',
                                  'Materia sólida',
                                  'Electricidad'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, al pasar de '
                             'un nivel trófico a otro se transfiere:',
                 'alternativas': ['El 90% de la energía',
                                  'El 10% de la energía',
                                  'El 50% de la energía',
                                  'El 100% de la energía',
                                  'El 1% de la energía'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, los '
                             'organismos usan en su propio metabolismo:',
                 'alternativas': ['El 10% de la energía capturada',
                                  'El 90% de la energía capturada',
                                  'El 50% de la energía capturada',
                                  'Toda la energía capturada',
                                  'Ninguna energía'],
                 'correcta': 'B'},
                {'pregunta': 'Un vegetal aprovecha para sus funciones de '
                             'supervivencia aproximadamente:',
                 'alternativas': ['10% de la energía solar fijada',
                                  '90% de la energía solar fijada',
                                  '50% de la energía solar fijada',
                                  '100% de la energía solar',
                                  '1% de la energía solar'],
                 'correcta': 'B'},
                {'pregunta': 'Un herbívoro que consume un vegetal solo puede '
                             'aprovechar de la energía fijada por este:',
                 'alternativas': ['El 90%',
                                  'El 10%',
                                  'El 50%',
                                  'El 100%',
                                  'El 1%'],
                 'correcta': 'B'},
                {'pregunta': 'Un carnívoro que consume a un herbívoro solo '
                             'puede aprovechar de la energía que este '
                             'recibió:',
                 'alternativas': ['El 90%',
                                  'El 10%',
                                  'El 50%',
                                  'El 100%',
                                  'El 5%'],
                 'correcta': 'B'},
                {'pregunta': 'El porcentaje aproximado de la energía '
                             'disponible en la Tierra que proviene del sol '
                             'es:',
                 'alternativas': ['50%', '99,98%', '10%', '75%', '25%'],
                 'correcta': 'B'},
                {'pregunta': 'Además del sol, otras fuentes de energía '
                             'terrestre incluyen las mareas, la energía '
                             'nuclear, la termal y la:',
                 'alternativas': ['Química exclusiva',
                                  'Gravitacional',
                                  'Cinética exclusiva',
                                  'Potencial exclusiva',
                                  'Radiante exclusiva de origen solar'],
                 'correcta': 'B'},
                {'pregunta': 'La radiación solar que llega a la superficie '
                             'terrestre varía según la latitud, la altura, '
                             'la orografía y:',
                 'alternativas': ['El color del suelo',
                                  'La nubosidad',
                                  'El tipo de roca',
                                  'La profundidad marina',
                                  'La velocidad de rotación'],
                 'correcta': 'B'},
                {'pregunta': 'La historia de la energía en un ecosistema '
                             'está en gran parte relacionada con la historia '
                             'de:',
                 'alternativas': ['El nitrógeno',
                                  'El carbono',
                                  'El oxígeno puro',
                                  'El azufre',
                                  'El fósforo'],
                 'correcta': 'B'},
                {'pregunta': 'La energía almacenada en los enlaces químicos '
                             'de los carbohidratos proviene originalmente '
                             'de:',
                 'alternativas': ['La respiración celular',
                                  'La fotosíntesis',
                                  'La quimiosíntesis exclusiva',
                                  'La descomposición',
                                  'La glucólisis'],
                 'correcta': 'B'}]},
 {'num': 15,
  'titulo': 'Diversidad Biológica y Deterioro de la Flora y la Fauna',
  'secciones': [{'titulo': '15.1 EL CONVENIO SOBRE LA DIVERSIDAD BIOLÓGICA',
                 'items': ['El {Convenio sobre la Diversidad Biológica} '
                           '(CDB) se celebró en la «{Cumbre de la Tierra}», '
                           'en Río de Janeiro, en {1992}.',
                           'El CDB define la diversidad biológica como la '
                           '{variabilidad} de organismos vivos de cualquier '
                           'fuente.',
                           'El CDB reconoce que la conservación de la '
                           'diversidad biológica es interés {común} de toda '
                           'la humanidad.',
                           'En {2010}, en {Nagoya}, Japón, se adoptó el Plan '
                           'Estratégico para la Diversidad Biológica '
                           '2011-2020.',
                           'Como parte del Plan Estratégico se trazaron las '
                           '{Metas de Aichi}.',
                           'La ONU declaró el {22 de mayo} de cada año como '
                           'el Día Internacional de la Diversidad '
                           'Biológica.']},
                {'titulo': '15.2 COMPONENTES DE LA BIODIVERSIDAD',
                 'items': ['La biodiversidad comprende tres componentes: '
                           'diversidad {genética}, diversidad de {especies} '
                           'y diversidad de {ecosistemas}.',
                           'La diversidad {genética} se refiere a las '
                           'diferencias en el material genético entre '
                           'poblaciones e individuos.',
                           'La diversidad de {especies} se refiere al número '
                           'de especies diferentes presentes en un área '
                           'determinada.',
                           'La diversidad de {ecosistemas} se refiere a la '
                           'variedad de sistemas ecológicos que se presentan '
                           'en una región.',
                           'El {Perú} es reconocido como centro mundial de '
                           'origen de recursos genéticos como la {papa}, el '
                           'maíz y el tomate.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El Convenio sobre la Diversidad Biológica se '
                           'celebró en el marco de la conocida como {Cumbre '
                           'de la Tierra}.',
                           'La Cumbre de la Tierra, donde se celebró el CDB, '
                           'se llevó a cabo en {Río de Janeiro, Brasil}.',
                           'El Convenio sobre la Diversidad Biológica se '
                           'celebró en el año {1992}.',
                           'El CDB define la diversidad biológica como la '
                           'variabilidad de {Organismos vivos de cualquier '
                           'fuente}.',
                           'Según el CDB, la conservación de la diversidad '
                           'biológica es interés {Común de toda la '
                           'humanidad}.',
                           'El Plan Estratégico para la Diversidad Biológica '
                           '2011-2020 fue adoptado en {Nagoya, Japón}.',
                           'El Plan Estratégico para la Diversidad Biológica '
                           'fue adoptado en el año {2010}.',
                           'Como parte del Plan Estratégico, se trazaron las '
                           'metas conocidas como {Metas de Aichi}.',
                           'El Día Internacional de la Diversidad Biológica '
                           'se celebra el {22 de mayo}.',
                           'La biodiversidad comprende tres componentes: '
                           'genética, de especies y de {Ecosistemas}.',
                           'La diversidad genética se refiere a las '
                           'diferencias en {El material genético entre '
                           'poblaciones e individuos}.',
                           'La diversidad de especies se refiere al número '
                           'de especies diferentes presentes en {Un área '
                           'determinada}.',
                           'La diversidad de especies tiene dos componentes: '
                           'la riqueza de especies y {Sus abundancias '
                           'relativas}.',
                           'La diversidad de ecosistemas se refiere a la '
                           'variedad de {Sistemas ecológicos en una región}.',
                           'El Perú es reconocido como un centro mundial de '
                           'origen de recursos genéticos de plantas como {La '
                           'papa, el maíz y el tomate}.',
                           'La riqueza genética del Perú está asociada con '
                           'la riqueza cultural desarrollada por {Los '
                           'pueblos indígenas}.',
                           'La distribución global de la diversidad de '
                           'especies depende de gradientes latitudinales, de '
                           'altitud y de {Precipitación}.',
                           'La conservación de la biodiversidad está '
                           'íntimamente asociada con el uso de {Los recursos '
                           'naturales y la tierra}.',
                           'Cuando las actividades humanas se incrementan '
                           'por encima de cierto umbral, los efectos sobre '
                           'los sistemas naturales son {Más significativos y '
                           'prolongados}.',
                           'Además de los tres componentes clásicos, en la '
                           'actualidad se reconoce también como componente '
                           'de la biodiversidad a la diversidad '
                           '{Cultural}.']}],
  'cuadros': [{'titulo': '15.2 LOS TRES COMPONENTES DE LA BIODIVERSIDAD',
               'encabezados': ['Componente', 'Se refiere a'],
               'filas': [['{Genética}',
                          'Diferencias en el material {genético}'],
                         ['De {especies}', 'Número de {especies} en un área'],
                         ['De {ecosistemas}',
                          'Variedad de sistemas {ecológicos}']]}],
  'preguntas': [{'pregunta': 'El Convenio sobre la Diversidad Biológica se '
                             'celebró en el marco de la conocida como:',
                 'alternativas': ['Conferencia de Kioto',
                                  'Cumbre de la Tierra',
                                  'Cumbre de París',
                                  'Protocolo de Montreal',
                                  'Acuerdo de Copenhague'],
                 'correcta': 'B'},
                {'pregunta': 'La Cumbre de la Tierra, donde se celebró el '
                             'CDB, se llevó a cabo en:',
                 'alternativas': ['Nueva York, EE.UU.',
                                  'Río de Janeiro, Brasil',
                                  'Ginebra, Suiza',
                                  'Nagoya, Japón',
                                  'Lima, Perú'],
                 'correcta': 'B'},
                {'pregunta': 'El Convenio sobre la Diversidad Biológica se '
                             'celebró en el año:',
                 'alternativas': ['1972', '1992', '2010', '2000', '1985'],
                 'correcta': 'B'},
                {'pregunta': 'El CDB define la diversidad biológica como la '
                             'variabilidad de:',
                 'alternativas': ['Solo especies vegetales',
                                  'Organismos vivos de cualquier fuente',
                                  'Solo especies animales',
                                  'Solo microorganismos',
                                  'Solo especies marinas'],
                 'correcta': 'B'},
                {'pregunta': 'Según el CDB, la conservación de la diversidad '
                             'biológica es interés:',
                 'alternativas': ['Exclusivo de los países desarrollados',
                                  'Común de toda la humanidad',
                                  'Solo de organismos ambientales',
                                  'Solo económico',
                                  'Solo científico'],
                 'correcta': 'B'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica 2011-2020 fue adoptado en:',
                 'alternativas': ['Río de Janeiro',
                                  'Nagoya, Japón',
                                  'Nueva York',
                                  'Ginebra',
                                  'París'],
                 'correcta': 'B'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica fue adoptado en el año:',
                 'alternativas': ['1992', '2010', '2000', '1985', '2020'],
                 'correcta': 'B'},
                {'pregunta': 'Como parte del Plan Estratégico, se trazaron '
                             'las metas conocidas como:',
                 'alternativas': ['Metas de Kioto',
                                  'Metas de Aichi',
                                  'Metas de París',
                                  'Metas de Montreal',
                                  'Metas de Copenhague'],
                 'correcta': 'B'},
                {'pregunta': 'El Día Internacional de la Diversidad '
                             'Biológica se celebra el:',
                 'alternativas': ['5 de junio',
                                  '22 de mayo',
                                  '22 de abril',
                                  '10 de diciembre',
                                  '1 de enero'],
                 'correcta': 'B'},
                {'pregunta': 'La biodiversidad comprende tres componentes: '
                             'genética, de especies y de:',
                 'alternativas': ['Climas',
                                  'Ecosistemas',
                                  'Suelos',
                                  'Océanos',
                                  'Continentes'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad genética se refiere a las '
                             'diferencias en:',
                 'alternativas': ['El número de especies',
                                  'El material genético entre poblaciones e '
                                  'individuos',
                                  'La cantidad de ecosistemas',
                                  'El tipo de clima',
                                  'La ubicación geográfica'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad de especies se refiere al número '
                             'de especies diferentes presentes en:',
                 'alternativas': ['Todo el planeta exclusivamente',
                                  'Un área determinada',
                                  'Solo un país',
                                  'Solo un continente',
                                  'Solo un océano'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad de especies tiene dos '
                             'componentes: la riqueza de especies y:',
                 'alternativas': ['El clima',
                                  'Sus abundancias relativas',
                                  'La ubicación',
                                  'El tamaño del área',
                                  'El tipo de suelo'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad de ecosistemas se refiere a la '
                             'variedad de:',
                 'alternativas': ['Especies individuales',
                                  'Sistemas ecológicos en una región',
                                  'Genes específicos',
                                  'Climas exclusivamente',
                                  'Recursos minerales'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú es reconocido como un centro mundial '
                             'de origen de recursos genéticos de plantas '
                             'como:',
                 'alternativas': ['El trigo y la cebada',
                                  'La papa, el maíz y el tomate',
                                  'El arroz y la soya',
                                  'El café y el cacao exclusivamente',
                                  'La vid y el olivo'],
                 'correcta': 'B'},
                {'pregunta': 'La riqueza genética del Perú está asociada con '
                             'la riqueza cultural desarrollada por:',
                 'alternativas': ['Colonizadores europeos',
                                  'Los pueblos indígenas',
                                  'Empresas multinacionales',
                                  'Organismos internacionales',
                                  'Científicos extranjeros'],
                 'correcta': 'B'},
                {'pregunta': 'La distribución global de la diversidad de '
                             'especies depende de gradientes latitudinales, '
                             'de altitud y de:',
                 'alternativas': ['Población humana',
                                  'Precipitación',
                                  'Actividad industrial',
                                  'Densidad urbana',
                                  'Comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'La conservación de la biodiversidad está '
                             'íntimamente asociada con el uso de:',
                 'alternativas': ['Solo la tecnología',
                                  'Los recursos naturales y la tierra',
                                  'Solo el capital financiero',
                                  'Solo el comercio internacional',
                                  'Solo la política exterior'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando las actividades humanas se incrementan '
                             'por encima de cierto umbral, los efectos sobre '
                             'los sistemas naturales son:',
                 'alternativas': ['Insignificantes',
                                  'Más significativos y prolongados',
                                  'Siempre positivos',
                                  'Reversibles automáticamente',
                                  'Inexistentes'],
                 'correcta': 'B'},
                {'pregunta': 'Además de los tres componentes clásicos, en la '
                             'actualidad se reconoce también como componente '
                             'de la biodiversidad a la diversidad:',
                 'alternativas': ['Económica',
                                  'Cultural',
                                  'Política',
                                  'Religiosa',
                                  'Militar'],
                 'correcta': 'B'}]},
 {'num': 16,
  'titulo': 'Contaminación, Problemas Ambientales y Conservación',
  'secciones': [{'titulo': '16.1 CONCEPTO DE CONTAMINACIÓN',
                 'items': ['La contaminación surge cuando, por presencia '
                           'cuantitativa o cualitativa de materia o energía, '
                           'se produce un {desequilibrio} ambiental.',
                           'La contaminación es la adición de una sustancia '
                           'al ambiente en cantidades que sobrepasan los '
                           'niveles {regulares} de la naturaleza.',
                           'A mayor {población} en un área geográfica y '
                           'mayor uso de recursos naturales, mayores son los '
                           'problemas de {contaminación}.']},
                {'titulo': '16.2 FUENTES DE CONTAMINACIÓN',
                 'items': ['La contaminación {natural} es causada por '
                           'fuentes como volcanes o efectos {geoclimáticos}.',
                           'La contaminación {antrópica} es producida por el '
                           'ser humano, como basura, esmog y descargas '
                           '{industriales}.',
                           'Una de las principales fuentes de contaminación '
                           'antropogénica es la agricultura '
                           '{industrializada}.']},
                {'titulo': '16.3 TIPOS DE CONTAMINANTES',
                 'items': ['Los contaminantes {biológicos} son '
                           'microorganismos como bacterias, hongos y '
                           '{virus}; ejemplo, el vibrión colérico.',
                           'Los contaminantes {físicos} se relacionan con la '
                           'energía: altas temperaturas, ruido y ondas '
                           '{electromagnéticas}.',
                           'Los contaminantes {químicos} son sustancias '
                           'orgánicas o inorgánicas; su auge se dio durante '
                           'la {Segunda Guerra Mundial}.',
                           'La contaminación química actualmente provoca el '
                           '{calentamiento global}, con gases como los '
                           'CFC.']},
                {'titulo': '16.4 CONTAMINACIÓN DEL AGUA',
                 'items': ['El agua cubre alrededor del {71}% de la '
                           'superficie del planeta, pero está disponible en '
                           'cantidades {limitadas}.',
                           'Entre las sustancias químicas que contaminan el '
                           'agua figuran el petróleo, {detergentes} '
                           'sintéticos y plaguicidas.',
                           'Los contaminantes {físicos} del agua alteran su '
                           '{transparencia}, afectando a los productores del '
                           'ecosistema.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La contaminación surge cuando se produce, por '
                           'presencia de materia o energía, un '
                           '{Desequilibrio ambiental}.',
                           'La contaminación se define como la adición de '
                           'sustancias al ambiente en cantidades que '
                           '{Sobrepasan los niveles regulares de la '
                           'naturaleza}.',
                           'A mayor población e índice de uso de recursos '
                           'naturales en un área, generalmente se presentan '
                           '{Más problemas de contaminación}.',
                           'La contaminación causada por fuentes como '
                           'volcanes o efectos geoclimáticos se llama '
                           'contaminación {Natural}.',
                           'La contaminación producida o distribuida por el '
                           'ser humano se llama contaminación {Antrópica}.',
                           'Una de las principales fuentes de contaminación '
                           'antropogénica es {La agricultura '
                           'industrializada}.',
                           'Los contaminantes causados por microorganismos '
                           'como bacterias y virus se llaman contaminantes '
                           '{Biológicos}.',
                           'El vibrión colérico, presente en aguas de ríos '
                           'latinoamericanos, es un ejemplo de contaminante '
                           '{Biológico}.',
                           'Los contaminantes relacionados con la energía, '
                           'como el ruido o las altas temperaturas, se '
                           'llaman contaminantes {Físicos}.',
                           'Los contaminantes físicos pueden influir en el '
                           'desarrollo de enfermedades humanas de tipo '
                           '{Psico-neurológicas}.',
                           'Los contaminantes provocados por sustancias '
                           'orgánicas o inorgánicas se llaman contaminantes '
                           '{Químicos}.',
                           'El impacto más notorio de la contaminación '
                           'química se dio durante {El auge industrial de la '
                           'Segunda Guerra Mundial}.',
                           'La contaminación química actualmente es la '
                           'principal causante de {El calentamiento global}.',
                           'Entre los gases que provocan el calentamiento '
                           'global se mencionan los {CFC '
                           '(clorofluorocarbonos)}.',
                           'El agua cubre de la superficie del planeta '
                           'aproximadamente {71%}.',
                           'Aunque el agua cubre gran parte del planeta, '
                           'está disponible en cantidades {Limitadas y '
                           'distribuidas de forma no uniforme}.',
                           'Entre las sustancias químicas que contaminan el '
                           'agua figuran el petróleo y los {Detergentes '
                           'sintéticos}.',
                           'Los contaminantes físicos del agua alteran '
                           'principalmente su {Transparencia}.',
                           'Cuando se impide la entrada de luz al agua por '
                           'contaminación física, los productores del '
                           'ecosistema {Deben emigrar o morir}.',
                           'Durante los últimos 200 años, el hombre ha '
                           'agregado al ambiente grandes cantidades de '
                           '{Productos químicos y agentes físicos}.']}],
  'cuadros': [{'titulo': '16.3 TIPOS DE CONTAMINANTES',
               'encabezados': ['Tipo', 'Ejemplo'],
               'filas': [['{Biológico}', 'Bacterias, {virus}, hongos'],
                         ['{Físico}', 'Ruido, {temperatura}, ondas'],
                         ['{Químico}',
                          '{CFC}, plaguicidas, metales pesados']]}],
  'preguntas': [{'pregunta': 'La contaminación surge cuando se produce, por '
                             'presencia de materia o energía, un:',
                 'alternativas': ['Equilibrio ambiental',
                                  'Desequilibrio ambiental',
                                  'Aumento de biodiversidad',
                                  'Ciclo biogeoquímico normal',
                                  'Ninguna alteración'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación se define como la adición de '
                             'sustancias al ambiente en cantidades que:',
                 'alternativas': ['Se mantienen bajo los niveles normales',
                                  'Sobrepasan los niveles regulares de la '
                                  'naturaleza',
                                  'No afectan a ningún organismo',
                                  'Mejoran el ecosistema',
                                  'Son siempre imperceptibles'],
                 'correcta': 'B'},
                {'pregunta': 'A mayor población e índice de uso de recursos '
                             'naturales en un área, generalmente se '
                             'presentan:',
                 'alternativas': ['Menos problemas ambientales',
                                  'Más problemas de contaminación',
                                  'Ningún cambio ambiental',
                                  'Mayor biodiversidad automática',
                                  'Menor consumo energético'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación causada por fuentes como '
                             'volcanes o efectos geoclimáticos se llama '
                             'contaminación:',
                 'alternativas': ['Antrópica',
                                  'Natural',
                                  'Biológica exclusiva',
                                  'Física exclusiva',
                                  'Química exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación producida o distribuida por '
                             'el ser humano se llama contaminación:',
                 'alternativas': ['Natural',
                                  'Antrópica',
                                  'Geológica',
                                  'Cósmica',
                                  'Volcánica'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las principales fuentes de '
                             'contaminación antropogénica es:',
                 'alternativas': ['Los volcanes',
                                  'La agricultura industrializada',
                                  'Las mareas',
                                  'Los terremotos',
                                  'La radiación solar natural'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes causados por microorganismos '
                             'como bacterias y virus se llaman '
                             'contaminantes:',
                 'alternativas': ['Físicos',
                                  'Biológicos',
                                  'Químicos',
                                  'Térmicos exclusivos',
                                  'Sonoros exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'El vibrión colérico, presente en aguas de ríos '
                             'latinoamericanos, es un ejemplo de '
                             'contaminante:',
                 'alternativas': ['Físico',
                                  'Biológico',
                                  'Químico',
                                  'Térmico',
                                  'Sonoro'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes relacionados con la energía, '
                             'como el ruido o las altas temperaturas, se '
                             'llaman contaminantes:',
                 'alternativas': ['Biológicos',
                                  'Físicos',
                                  'Químicos',
                                  'Orgánicos exclusivos',
                                  'Naturales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes físicos pueden influir en el '
                             'desarrollo de enfermedades humanas de tipo:',
                 'alternativas': ['Solo digestivas',
                                  'Psico-neurológicas',
                                  'Solo dermatológicas',
                                  'Solo cardiovasculares exclusivas',
                                  'Solo óseas'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes provocados por sustancias '
                             'orgánicas o inorgánicas se llaman '
                             'contaminantes:',
                 'alternativas': ['Físicos',
                                  'Químicos',
                                  'Biológicos',
                                  'Sonoros',
                                  'Radiactivos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'El impacto más notorio de la contaminación '
                             'química se dio durante:',
                 'alternativas': ['La Edad Media',
                                  'El auge industrial de la Segunda Guerra '
                                  'Mundial',
                                  'La Revolución Francesa',
                                  'La colonización americana',
                                  'La Primera Guerra Mundial exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación química actualmente es la '
                             'principal causante de:',
                 'alternativas': ['La biodiversidad',
                                  'El calentamiento global',
                                  'La fotosíntesis',
                                  'La reproducción celular',
                                  'La mitosis'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los gases que provocan el calentamiento '
                             'global se mencionan los:',
                 'alternativas': ['Gases nobles',
                                  'CFC (clorofluorocarbonos)',
                                  'Gases inertes',
                                  'Vapor de agua exclusivamente',
                                  'Oxígeno puro'],
                 'correcta': 'B'},
                {'pregunta': 'El agua cubre de la superficie del planeta '
                             'aproximadamente:',
                 'alternativas': ['50%', '71%', '30%', '90%', '20%'],
                 'correcta': 'B'},
                {'pregunta': 'Aunque el agua cubre gran parte del planeta, '
                             'está disponible en cantidades:',
                 'alternativas': ['Ilimitadas',
                                  'Limitadas y distribuidas de forma no '
                                  'uniforme',
                                  'Excesivas en todas las regiones',
                                  'Iguales en todo el mundo',
                                  'Infinitas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las sustancias químicas que contaminan '
                             'el agua figuran el petróleo y los:',
                 'alternativas': ['Oxígenos disueltos',
                                  'Detergentes sintéticos',
                                  'Nutrientes naturales',
                                  'Minerales esenciales',
                                  'Gases nobles'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes físicos del agua alteran '
                             'principalmente su:',
                 'alternativas': ['Composición química exclusiva',
                                  'Transparencia',
                                  'Temperatura exclusivamente',
                                  'pH exclusivamente',
                                  'Salinidad exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando se impide la entrada de luz al agua por '
                             'contaminación física, los productores del '
                             'ecosistema:',
                 'alternativas': ['Se multiplican más rápido',
                                  'Deben emigrar o morir',
                                  'No se ven afectados',
                                  'Aumentan su fotosíntesis',
                                  'Cambian de especie'],
                 'correcta': 'B'},
                {'pregunta': 'Durante los últimos 200 años, el hombre ha '
                             'agregado al ambiente grandes cantidades de:',
                 'alternativas': ['Solo agua pura',
                                  'Productos químicos y agentes físicos',
                                  'Solo oxígeno',
                                  'Solo nitrógeno',
                                  'Solo materia orgánica natural'],
                 'correcta': 'B'}]}]
