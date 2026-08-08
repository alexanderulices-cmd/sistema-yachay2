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
                {'titulo': '1.1.1 RAMAS DE LA BIOLOGÍA',
                 'items': ['La {anatomía} estudia los órganos, aparatos y '
                           'sistemas de los seres vivos.',
                           'La {fisiología} estudia las funciones de los '
                           'seres vivos; la {embriología} estudia la '
                           'formación y desarrollo de los embriones.',
                           'La {zoología} estudia a los animales; la '
                           '{botánica} estudia a las plantas; la {micología} '
                           'estudia a los hongos.',
                           'La {bacteriología} estudia a las bacterias; la '
                           '{ficología} estudia a las algas; la '
                           '{protozoología} estudia a los protozoarios.',
                           'La {taxonomía} clasifica a los seres vivos; la '
                           '{histología} estudia los tejidos; la '
                           '{paleontología} estudia los fósiles.',
                           'La {genética} estudia las variaciones y la '
                           'herencia; la {ingeniería genética} estudia '
                           'organismos y productos transgénicos.',
                           'La {ecología} estudia las interrelaciones entre '
                           'seres vivos y el medio ambiente; la {etología} '
                           'estudia el carácter y comportamiento.',
                           'La {patología} estudia las enfermedades; la '
                           '{evolución} estudia el origen y los cambios en '
                           'las especies.']},
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
                           'ecosistema, bioma y {biosfera}.']}],
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
                 'alternativas': ['Logos', 'Physis', 'Zoon', 'Genos', 'Soma'],
                 'correcta': 'A'},
                {'pregunta': 'La raíz griega «bios» significa:',
                 'alternativas': ['Vida',
                                  'Célula',
                                  'Materia',
                                  'Estudio',
                                  'Origen'],
                 'correcta': 'A'},
                {'pregunta': 'La biología es la ciencia que estudia:',
                 'alternativas': ['Solo las estrellas',
                                  'Solo el universo',
                                  'Los seres vivos',
                                  'Solo la materia inerte',
                                  'Solo los minerales'],
                 'correcta': 'C'},
                {'pregunta': 'El estudio de la biología comprende el origen, '
                             'evolución, clasificación, estructura, función '
                             'y:',
                 'alternativas': ['Política',
                                  'Herencia',
                                  'Economía',
                                  'Religión',
                                  'Comercio'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la unión de la física y '
                             'la biología se llama:',
                 'alternativas': ['Geología',
                                  'Biofísica',
                                  'Bioquímica',
                                  'Astrobiología',
                                  'Bioestadística'],
                 'correcta': 'B'},
                {'pregunta': 'La biofísica aplica los principios de la '
                             'física para estudiar:',
                 'alternativas': ['Solo el universo',
                                  'La estructura de los seres vivos',
                                  'Solo la historia',
                                  'Solo el clima',
                                  'Solo la economía'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que aporta las bases del conocimiento '
                             'de la estructura de la materia viva es la:',
                 'alternativas': ['Astrofísica',
                                  'Bioquímica',
                                  'Geología',
                                  'Bioestadística',
                                  'Biofísica'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la relación entre '
                             'biología y matemáticas se llama:',
                 'alternativas': ['Biofísica',
                                  'Bioquímica',
                                  'Bioética',
                                  'Bioestadística',
                                  'Biogeografía'],
                 'correcta': 'D'},
                {'pregunta': 'El nivel formado por protón, neutrón y '
                             'electrón se llama nivel:',
                 'alternativas': ['Macromolecular',
                                  'Atómico',
                                  'Molecular',
                                  'Celular',
                                  'Subatómico'],
                 'correcta': 'E'},
                {'pregunta': 'El átomo se define como la unidad más pequeña '
                             'de:',
                 'alternativas': ['Una célula',
                                  'Un organismo',
                                  'Un ecosistema',
                                  'Una molécula orgánica',
                                  'Un elemento químico'],
                 'correcta': 'E'},
                {'pregunta': 'Las moléculas con un peso de miles de daltons, '
                             'formadas por unidades monoméricas, se llaman:',
                 'alternativas': ['Átomos',
                                  'Organelos',
                                  'Ecosistemas',
                                  'Partículas subatómicas',
                                  'Macromoléculas'],
                 'correcta': 'E'},
                {'pregunta': 'El almidón es un polímero de glucosa, mientras '
                             'que las proteínas son polímeros de:',
                 'alternativas': ['Nucleótidos',
                                  'Glúcidos',
                                  'Lípidos',
                                  'Iones',
                                  'Aminoácidos'],
                 'correcta': 'E'},
                {'pregunta': 'El nivel de complejos supramoleculares también '
                             'se conoce como nivel:',
                 'alternativas': ['Ecológico',
                                  'Orgánico',
                                  'Prebiótico',
                                  'Atómico',
                                  'Celular'],
                 'correcta': 'C'},
                {'pregunta': 'Los virus, ribosomas y glucoproteínas son '
                             'ejemplos del nivel:',
                 'alternativas': ['Celular',
                                  'Orgánico',
                                  'Atómico',
                                  'Ecológico',
                                  'Supramolecular'],
                 'correcta': 'E'},
                {'pregunta': 'Los orgánulos celulares, como las '
                             'mitocondrias, no se consideran seres vivos '
                             'porque:',
                 'alternativas': ['No cumplen las funciones de nutrición, '
                                  'relación y reproducción',
                                  'No tienen forma definida',
                                  'Son demasiado pequeños',
                                  'No están formados por moléculas',
                                  'No contienen materia orgánica'],
                 'correcta': 'A'},
                {'pregunta': 'La unidad mínima de la materia viva es:',
                 'alternativas': ['El órgano',
                                  'La célula',
                                  'La molécula',
                                  'El tejido',
                                  'El átomo'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos formados por muchas células se '
                             'denominan:',
                 'alternativas': ['Pluricelulares',
                                  'Acelulares',
                                  'Procariontes exclusivamente',
                                  'Unicelulares',
                                  'Virales'],
                 'correcta': 'A'},
                {'pregunta': 'A partir de la especie, comienzan los niveles '
                             'de organización:',
                 'alternativas': ['Celulares exclusivamente',
                                  'Subatómicos',
                                  'Moleculares',
                                  'Ecológicos',
                                  'Químicos'],
                 'correcta': 'D'},
                {'pregunta': 'Los niveles de organización ecológica incluyen '
                             'población, comunidad, ecosistema, bioma y:',
                 'alternativas': ['Órgano',
                                  'Biosfera',
                                  'Molécula',
                                  'Célula',
                                  'Tejido'],
                 'correcta': 'B'},
                {'pregunta': 'Los niveles de organización permiten, entre '
                             'otras cosas:',
                 'alternativas': ['Eliminar el estudio sistemático',
                                  'Evitar el análisis científico',
                                  'Establecer límites y ordenar conceptos',
                                  'Ignorar la complejidad biológica',
                                  'Confundir la clasificación'],
                 'correcta': 'C'},
                {'pregunta': 'La rama de la biología que estudia los '
                             'órganos, aparatos y sistemas se llama:',
                 'alternativas': ['Embriología',
                                  'Fisiología',
                                  'Anatomía',
                                  'Citología',
                                  'Histología'],
                 'correcta': 'C'},
                {'pregunta': 'La rama que estudia la formación y desarrollo '
                             'de los embriones se llama:',
                 'alternativas': ['Embriología',
                                  'Genética',
                                  'Histología',
                                  'Anatomía',
                                  'Fisiología'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la biología que estudia a los '
                             'hongos se llama:',
                 'alternativas': ['Protozoología',
                                  'Bacteriología',
                                  'Micología',
                                  'Botánica',
                                  'Ficología'],
                 'correcta': 'C'},
                {'pregunta': 'La rama que estudia a las algas se llama:',
                 'alternativas': ['Micología',
                                  'Botánica',
                                  'Bacteriología',
                                  'Ficología',
                                  'Zoología'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la biología que clasifica a los '
                             'seres vivos se llama:',
                 'alternativas': ['Taxonomía',
                                  'Histología',
                                  'Paleontología',
                                  'Etología',
                                  'Ecología'],
                 'correcta': 'A'},
                {'pregunta': 'La rama que estudia los tejidos de los seres '
                             'vivos se llama:',
                 'alternativas': ['Citología',
                                  'Anatomía',
                                  'Fisiología',
                                  'Histología',
                                  'Taxonomía'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la biología que estudia los fósiles '
                             'se llama:',
                 'alternativas': ['Etología',
                                  'Genética',
                                  'Ecología',
                                  'Paleontología',
                                  'Evolución'],
                 'correcta': 'D'},
                {'pregunta': 'La rama que estudia organismos y productos '
                             'transgénicos se llama:',
                 'alternativas': ['Bioestadística',
                                  'Bioquímica',
                                  'Ingeniería genética',
                                  'Biofísica',
                                  'Genética'],
                 'correcta': 'C'},
                {'pregunta': 'La rama de la biología que estudia el carácter '
                             'y comportamiento de los seres vivos se llama:',
                 'alternativas': ['Patología',
                                  'Taxonomía',
                                  'Fisiología',
                                  'Etología',
                                  'Ecología'],
                 'correcta': 'D'},
                {'pregunta': 'La rama que estudia las enfermedades se llama:',
                 'alternativas': ['Genética',
                                  'Etología',
                                  'Ecología',
                                  'Patología',
                                  'Fisiología'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'DEFINICIÓN DE BIOLOGÍA',
                      'items': ['Etimológicamente, «biología» deriva de las '
                                'raíces griegas «bios» (vida) y «logos» '
                                '(tratado o estudio).']},
                     {'titulo': 'RAMAS DE LA BIOLOGÍA',
                      'items': ['La anatomía estudia los órganos, aparatos y '
                                'sistemas de los seres vivos.']},
                     {'titulo': 'RELACIÓN CON OTRAS CIENCIAS',
                      'items': ['La unión de la física y la biología da '
                                'origen a la biofísica, que estudia la '
                                'estructura de los seres vivos.']},
                     {'titulo': 'NIVEL QUÍMICO DE ORGANIZACIÓN',
                      'items': ['El nivel subatómico está formado por '
                                'protón, neutrón y electrón.']},
                     {'titulo': 'NIVEL BIOLÓGICO DE ORGANIZACIÓN',
                      'items': ['El nivel celular es la unidad mínima de la '
                                'materia viva; los organismos formados por '
                                'muchas células son pluricelulares.']}]},
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
                {'titulo': '2.1.1.A BIOELEMENTOS PRIMARIOS',
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
                {'titulo': '2.1.1.B BIOELEMENTOS SECUNDARIOS',
                 'items': ['Los bioelementos {secundarios} son cinco: sodio, '
                           'potasio, calcio, magnesio y {cloro}.',
                           'El {sodio} es el principal ión positivo del '
                           'líquido intersticial, esencial en la conducción '
                           'de impulsos {nerviosos}.',
                           'El {potasio} es el principal catión del interior '
                           'de las {células}.']},
                {'titulo': '2.1.2.A MICROELEMENTOS NO VARIABLES',
                 'items': ['Los {microelementos}, u oligoelementos, se '
                           'encuentran en los seres vivos en cantidades muy '
                           'pequeñas: apenas {0,4}% de la materia viva.',
                           'Los microelementos {no variables} son: hierro, '
                           'manganeso, cobre, zinc, yodo, flúor, cobalto, '
                           'molibdeno y {boro}.',
                           'El {hierro} forma el grupo prostético hemo de la '
                           'hemoglobina, que transporta {oxígeno} en la '
                           'sangre.',
                           'El {yodo} se concentra en la glándula '
                           '{tiroides}, donde se convierte en tiroxina y '
                           'yodotirosina.',
                           'El {flúor} aumenta la resistencia del esmalte '
                           'dental e inhibe el proceso de {caries}.',
                           'El {zinc} activa numerosas enzimas y es '
                           'constituyente de proteínas como la {insulina}.',
                           'El {cobalto} está asociado con la funcionalidad '
                           'de la vitamina {B12} o cobalamina.']},
                {'titulo': '2.1.2.B MICROELEMENTOS VARIABLES',
                 'items': ['Los microelementos {variables} son: selenio, '
                           'silicio, cromo, aluminio, litio, níquel y '
                           '{bromo}.',
                           'El {cromo} tiene una función preponderante en el '
                           'metabolismo de la insulina como factor de '
                           'tolerancia a la {glucosa}.',
                           'El {selenio} cumple funciones antioxidantes, de '
                           'regulación hormonal, y tiene efectos '
                           '{anticancerígenos}.']}],
  'cuadros': [{'titulo': 'LOS SEIS BIOELEMENTOS PRIMARIOS (ORGANÓGENOS)',
               'encabezados': ['Elemento', 'Símbolo', 'Función principal'],
               'filas': [['{Carbono}', 'C', 'Base de moléculas {biológicas}'],
                         ['{Hidrógeno}', 'H', 'Componente {estructural}'],
                         ['{Oxígeno}', 'O', 'Forma parte del {agua}'],
                         ['{Nitrógeno}', 'N', 'Forma {proteínas}'],
                         ['{Fósforo}', 'P', 'Transferencia de {energía}'],
                         ['{Azufre}', 'S', 'Forma {aminoácidos}']],
               'despues_de': '2.1.1.A BIOELEMENTOS PRIMARIOS'}],
  'preguntas': [{'pregunta': 'La materia está formada por un total de '
                             'elementos químicos igual a:',
                 'alternativas': ['40', '11', '92', '20', '118'],
                 'correcta': 'E'},
                {'pregunta': 'De los elementos químicos existentes, los que '
                             'son naturales suman:',
                 'alternativas': ['92', '40', '6', '118', '20'],
                 'correcta': 'A'},
                {'pregunta': 'Los seres vivos están constituidos por un '
                             'número de elementos igual a:',
                 'alternativas': ['6', '92', '118', '40', '20'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos se clasifican en '
                             'macroelementos y:',
                 'alternativas': ['Solo minerales',
                                  'Solo inorgánicos',
                                  'Solo orgánicos',
                                  'Microelementos u oligoelementos',
                                  'Bioelementos primarios exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Los macroelementos representan de la materia '
                             'viva aproximadamente:',
                 'alternativas': ['50%', '10%', '25%', '99,6%', '75%'],
                 'correcta': 'D'},
                {'pregunta': 'Los bioelementos primarios, también llamados '
                             'organógenos, suman un total de:',
                 'alternativas': ['Once',
                                  'Cinco',
                                  'Seis',
                                  'Veinte',
                                  'Cuatro'],
                 'correcta': 'C'},
                {'pregunta': 'Los cuatro bioelementos primarios más '
                             'abundantes representan de la materia viva:',
                 'alternativas': ['20%', '50%', '96%', '75%', '10%'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento considerado la piedra angular en '
                             'la construcción de moléculas biológicas es:',
                 'alternativas': ['El azufre',
                                  'El oxígeno',
                                  'El carbono',
                                  'El fósforo',
                                  'El nitrógeno'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento más abundante en la naturaleza, '
                             'que forma parte del agua, es:',
                 'alternativas': ['El oxígeno',
                                  'El carbono',
                                  'El hidrógeno',
                                  'El fósforo',
                                  'El nitrógeno'],
                 'correcta': 'A'},
                {'pregunta': 'El elemento que forma las proteínas, '
                             'esenciales para el crecimiento, es:',
                 'alternativas': ['El carbono',
                                  'El nitrógeno',
                                  'El oxígeno',
                                  'El fósforo',
                                  'El azufre'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que desempeña un papel esencial en '
                             'la transferencia de energía, como en el ATP, '
                             'es:',
                 'alternativas': ['El hidrógeno',
                                  'El carbono',
                                  'El fósforo',
                                  'El azufre',
                                  'El nitrógeno'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento que forma parte de aminoácidos '
                             'como la metionina y la cisteína es:',
                 'alternativas': ['El carbono',
                                  'El nitrógeno',
                                  'El azufre',
                                  'El oxígeno',
                                  'El fósforo'],
                 'correcta': 'C'},
                {'pregunta': 'Los bioelementos secundarios son cinco: sodio, '
                             'potasio, calcio, magnesio y:',
                 'alternativas': ['Fósforo',
                                  'Azufre',
                                  'Nitrógeno',
                                  'Carbono',
                                  'Cloro'],
                 'correcta': 'E'},
                {'pregunta': 'El principal ión positivo del líquido '
                             'intersticial, esencial para impulsos '
                             'nerviosos, es:',
                 'alternativas': ['El potasio',
                                  'El cloro',
                                  'El sodio',
                                  'El calcio',
                                  'El magnesio'],
                 'correcta': 'C'},
                {'pregunta': 'El principal catión del interior de las '
                             'células es:',
                 'alternativas': ['El sodio',
                                  'El magnesio',
                                  'El calcio',
                                  'El cloro',
                                  'El potasio'],
                 'correcta': 'E'},
                {'pregunta': 'El hidrógeno es considerado el elemento:',
                 'alternativas': ['Exclusivo de las plantas',
                                  'Más pesado de la naturaleza',
                                  'Más liviano que existe en la naturaleza',
                                  'Sin relación con la vida',
                                  'Menos abundante'],
                 'correcta': 'C'},
                {'pregunta': 'El fósforo forma parte de los fosfolípidos que '
                             'se encuentran en:',
                 'alternativas': ['Las membranas celulares',
                                  'Las paredes celulares vegetales '
                                  'exclusivamente',
                                  'Solo el citoplasma',
                                  'Solo los ribosomas',
                                  'Solo el núcleo celular'],
                 'correcta': 'A'},
                {'pregunta': 'El azufre se encuentra, entre otros lugares, '
                             'en la bilis, el cartílago y:',
                 'alternativas': ['Solo las uñas',
                                  'Solo el cabello',
                                  'Solo los dientes',
                                  'Los huesos exclusivamente',
                                  'Las glándulas suprarrenales'],
                 'correcta': 'E'},
                {'pregunta': 'El nitrógeno también forma parte de compuestos '
                             'como:',
                 'alternativas': ['Solo el oxígeno molecular',
                                  'Solo el agua',
                                  'Los fertilizantes',
                                  'Solo la glucosa',
                                  'Solo el dióxido de carbono'],
                 'correcta': 'C'},
                {'pregunta': 'Los bioelementos secundarios son necesarios '
                             'para las células en cantidades:',
                 'alternativas': ['Idénticas a los primarios',
                                  'Ilimitadas',
                                  'Más pequeñas que los primarios',
                                  'Mayores que los primarios',
                                  'Nulas'],
                 'correcta': 'C'},
                {'pregunta': 'Los microelementos, u oligoelementos, '
                             'representan de la materia viva '
                             'aproximadamente:',
                 'alternativas': ['40%', '1%', '4%', '0,4%', '10%'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los microelementos no variables se '
                             'encuentran hierro, manganeso, cobre, zinc, '
                             'yodo, flúor, cobalto, molibdeno y:',
                 'alternativas': ['Selenio',
                                  'Aluminio',
                                  'Boro',
                                  'Níquel',
                                  'Cromo'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los microelementos variables se '
                             'encuentran selenio, silicio, cromo, aluminio, '
                             'litio, níquel y:',
                 'alternativas': ['Bromo',
                                  'Zinc',
                                  'Cobalto',
                                  'Yodo',
                                  'Hierro'],
                 'correcta': 'A'},
                {'pregunta': 'El microelemento que forma el grupo prostético '
                             'hemo de la hemoglobina es:',
                 'alternativas': ['El cobre',
                                  'El hierro',
                                  'El manganeso',
                                  'El zinc',
                                  'El yodo'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento que se concentra en la '
                             'glándula tiroides es:',
                 'alternativas': ['El yodo',
                                  'El cobalto',
                                  'El flúor',
                                  'El hierro',
                                  'El zinc'],
                 'correcta': 'A'},
                {'pregunta': 'El microelemento que aumenta la resistencia '
                             'del esmalte dental e inhibe las caries es:',
                 'alternativas': ['El flúor',
                                  'El cobre',
                                  'El yodo',
                                  'El zinc',
                                  'El hierro'],
                 'correcta': 'A'},
                {'pregunta': 'El microelemento que es constituyente de '
                             'proteínas como la insulina es:',
                 'alternativas': ['El hierro',
                                  'El flúor',
                                  'El yodo',
                                  'El cobalto',
                                  'El zinc'],
                 'correcta': 'E'},
                {'pregunta': 'El microelemento asociado con la funcionalidad '
                             'de la vitamina B12 es:',
                 'alternativas': ['El yodo',
                                  'El hierro',
                                  'El zinc',
                                  'El cobalto',
                                  'El manganeso'],
                 'correcta': 'D'},
                {'pregunta': 'El microelemento con función preponderante en '
                             'el metabolismo de la insulina como factor de '
                             'tolerancia a la glucosa es:',
                 'alternativas': ['El cromo',
                                  'El hierro',
                                  'El yodo',
                                  'El cobalto',
                                  'El zinc'],
                 'correcta': 'A'},
                {'pregunta': 'El oligoelemento que en los seres vivos cumple '
                             'funciones antioxidantes, de regulación '
                             'hormonal y tiene efectos anticancerígenos, es:',
                 'alternativas': ['Cromo',
                                  'Cobre',
                                  'Zinc',
                                  'Selenio',
                                  'Silicio'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'BIOELEMENTOS',
                      'items': ['La materia está formada por 118 elementos '
                                'químicos, de los cuales 92 son naturales.']},
                     {'titulo': '.A BIOELEMENTOS PRIMARIOS',
                      'items': ['Los macroelementos representan el 99,6% de '
                                'la materia viva, y están conformados por 11 '
                                'bioelementos.']},
                     {'titulo': '.B BIOELEMENTOS SECUNDARIOS',
                      'items': ['Los bioelementos secundarios son cinco: '
                                'sodio, potasio, calcio, magnesio y cloro.']},
                     {'titulo': '.A MICROELEMENTOS NO VARIABLES',
                      'items': ['Los microelementos, u oligoelementos, se '
                                'encuentran en los seres vivos en cantidades '
                                'muy pequeñas: apenas 0,4% de la materia '
                                'viva.']},
                     {'titulo': '.B MICROELEMENTOS VARIABLES',
                      'items': ['Los microelementos variables son: selenio, '
                                'silicio, cromo, aluminio, litio, níquel y '
                                'bromo.']}]},
 {'num': 3,
  'titulo': 'Biomoléculas Inorgánicas',
  'secciones': [{'titulo': 'CARACTERÍSTICAS GENERALES DE LAS BIOMOLÉCULAS '
                           'INORGÁNICAS',
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
                {'titulo': '3.1 EL AGUA',
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
                {'titulo': '3.1.1 AGUA EN LA CÉLULA',
                 'items': ['El agua {libre} representa el 95% del agua '
                           'celular, y actúa como solvente estable e '
                           '{ionizante}.',
                           'El agua {ligada} representa el 5% restante, y '
                           'comprende el agua de {imbibición} y el agua de '
                           'constitución.']},
                {'titulo': '3.1.2 PROPIEDADES DEL AGUA',
                 'items': ['El {poder solvente} del agua es su capacidad de '
                           'disolver gran cantidad de moléculas inorgánicas '
                           'y {orgánicas}.',
                           'La {polaridad} de la molécula de agua favorece '
                           'la disociación de moléculas formadoras de '
                           '{iones}.']},
                {'titulo': '3.1.3 FUNCIONES DEL AGUA',
                 'items': ['La función de {transporte}: el agua transporta '
                           'sustancias del interior al exterior de la célula '
                           'y viceversa.',
                           'La función {estructural}: el agua da forma y '
                           'volumen a las células.',
                           'La función {termorreguladora}: el agua actúa en '
                           'los cambios de temperatura para mantener el '
                           'cuerpo a temperatura constante, como en la '
                           '{sudoración}.',
                           'La función {química}: el agua actúa en '
                           'reacciones químicas como la hidrólisis o la '
                           '{condensación}.',
                           'La función {lubricante}: el agua actúa como '
                           'amortiguador de roces y golpes en las '
                           '{articulaciones}.']},
                {'titulo': '3.2 SALES MINERALES Y ELECTROLITOS',
                 'items': ['Las {sales minerales} son compuestos neutros '
                           'producidos por la reacción de un ácido y una '
                           '{base}.',
                           'En estado sólido, las sales forman estructuras '
                           'duras, como caparazones, huesos y {dientes}.',
                           'Cuando una sal se disuelve en agua, se disocia '
                           'en {iones}: cationes y aniones.',
                           'Los {aniones} son iones con carga negativa, como '
                           'el cloruro (Cl<super>-</super>) y los fosfatos.',
                           'Los {cationes} son iones con carga positiva, '
                           'como el sodio (Na<super>+</super>) y el calcio '
                           '(Ca<super>2+</super>).',
                           'Las sales minerales más abundantes en el cuerpo '
                           'humano contienen {fósforo} y calcio.']},
                {'titulo': '3.2.1 FUNCIONES DE LOS ELECTROLITOS',
                 'items': ['La concentración elevada de {sodio} '
                           '(Na<super>+</super>) en la sangre produce '
                           '{hipertensión} arterial.',
                           'La concentración elevada de {potasio} '
                           '(K<super>+</super>) en la sangre conlleva a la '
                           '{hipotensión}.',
                           'El {calcio} (Ca<super>2+</super>) participa '
                           'también en los procesos de {secreción} de las '
                           'células nerviosas.',
                           'El {magnesio} (Mg<super>2+</super>) estabiliza '
                           'los {ribosomas}, manteniendo unidas sus '
                           'subunidades durante la síntesis de proteínas.',
                           'El {cloruro} (Cl<super>-</super>) abunda en la '
                           'mucosa gástrica, la orina, el sudor y la '
                           '{leche}.',
                           'El {bicarbonato} '
                           '(HCO<sub>3</sub><super>-</super>) actúa como '
                           'tampón {extracelular}, a diferencia del fosfato, '
                           'que es tampón intracelular.']}],
  'cuadros': [{'titulo': 'DISTRIBUCIÓN DEL AGUA EN LA CÉLULA',
               'encabezados': ['Forma', 'Porcentaje'],
               'filas': [['Agua {libre}', '{95}%'],
                         ['Agua {ligada}', '{5}%']],
               'despues_de': '3.1.1 AGUA EN LA CÉLULA'},
              {'titulo': 'PRINCIPALES ELECTROLITOS Y SU FUNCIÓN',
               'despues_de': '3.2.1 FUNCIONES DE LOS ELECTROLITOS',
               'encabezados': ['Ion', 'Funciones'],
               'filas': [['{Sodio} (Na<super>+</super>)',
                          'Regulación osmótica, potencial de membrana, '
                          'transporte y {conducción nerviosa}'],
                         ['{Potasio} (K<super>+</super>)',
                          'Regulación osmótica, potencial de membrana, '
                          'transmisión de la excitación y {contracción '
                          'muscular}'],
                         ['{Calcio} (Ca<super>2+</super>)',
                          'Estructura ósea, estabilización de membrana, '
                          'coagulación y {contracción muscular}'],
                         ['{Magnesio} (Mg<super>2+</super>)',
                          'Cofactor enzimático, estructura de la {clorofila} '
                          'y componente de los huesos'],
                         ['{Cloruro} (Cl<super>-</super>)',
                          'Electroneutralidad, transporte de membrana y '
                          'equilibrio {hídrico}'],
                         ['{Fosfato} (PO<sub>4</sub><super>3-</super>)',
                          'Tampón intracelular, estructura ósea y parte de '
                          'nucleótidos, ADN y {ARN}'],
                         ['{Bicarbonato} (HCO<sub>3</sub><super>-</super>)',
                          'Tampón {extracelular}']]}],
  'preguntas': [{'pregunta': 'Las biomoléculas inorgánicas se caracterizan '
                             'por la ausencia de enlaces:',
                 'alternativas': ['Carbono-carbono',
                                  'Azufre-carbono',
                                  'Oxígeno-nitrógeno',
                                  'Hidrógeno-oxígeno',
                                  'Nitrógeno-fósforo'],
                 'correcta': 'A'},
                {'pregunta': 'Los minerales que forman estructuras duras, '
                             'como huesos y dientes, se llaman:',
                 'alternativas': ['Gases disueltos',
                                  'Minerales en disolución',
                                  'Iones libres',
                                  'Minerales sólidos',
                                  'Electrolitos exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los minerales en disolución son electrolitos '
                             'que participan, entre otras funciones, en:',
                 'alternativas': ['La contracción muscular',
                                  'La digestión de proteínas',
                                  'El transporte de oxígeno exclusivamente',
                                  'La respiración exclusivamente',
                                  'La síntesis de ADN exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los gases disueltos que usan los seres vivos '
                             'son principalmente oxígeno y:',
                 'alternativas': ['Dióxido de carbono',
                                  'Metano',
                                  'Nitrógeno',
                                  'Ozono',
                                  'Hidrógeno gaseoso'],
                 'correcta': 'A'},
                {'pregunta': 'La molécula de agua está formada por dos '
                             'átomos de hidrógeno y uno de:',
                 'alternativas': ['Oxígeno',
                                  'Nitrógeno',
                                  'Azufre',
                                  'Carbono',
                                  'Fósforo'],
                 'correcta': 'A'},
                {'pregunta': 'Los átomos de la molécula de agua se unen '
                             'mediante enlaces:',
                 'alternativas': ['Metálicos',
                                  'De hidrógeno exclusivamente',
                                  'Van der Waals exclusivos',
                                  'Iónicos',
                                  'Covalentes'],
                 'correcta': 'E'},
                {'pregunta': 'La estructura de la molécula de agua se '
                             'describe como:',
                 'alternativas': ['Hexagonal',
                                  'Lineal',
                                  'Tetraédrica',
                                  'Cúbica',
                                  'Esférica perfecta'],
                 'correcta': 'C'},
                {'pregunta': 'El ángulo entre los dos átomos de hidrógeno en '
                             'la molécula de agua es de aproximadamente:',
                 'alternativas': ['104,5°', '90°', '60°', '120°', '180°'],
                 'correcta': 'A'},
                {'pregunta': 'La distribución desigual de carga dentro de un '
                             'enlace se denomina:',
                 'alternativas': ['Radical libre',
                                  'Isómero',
                                  'Catión',
                                  'Anión',
                                  'Dipolo'],
                 'correcta': 'E'},
                {'pregunta': 'En la molécula de agua, el oxígeno tiene una '
                             'carga parcial:',
                 'alternativas': ['Positiva',
                                  'Neutra',
                                  'Variable al azar',
                                  'Nula',
                                  'Negativa'],
                 'correcta': 'E'},
                {'pregunta': 'La atracción entre moléculas de agua debido a '
                             'su polaridad produce el llamado:',
                 'alternativas': ['Enlace covalente puro',
                                  'Enlace iónico',
                                  'Enlace peptídico',
                                  'Enlace metálico',
                                  'Puente de hidrógeno'],
                 'correcta': 'E'},
                {'pregunta': 'Una sola molécula de agua puede formar puentes '
                             'de hidrógeno con hasta otras:',
                 'alternativas': ['Cuatro moléculas',
                                  'Una sola molécula',
                                  'Ocho moléculas',
                                  'Diez moléculas',
                                  'Dos moléculas'],
                 'correcta': 'A'},
                {'pregunta': 'El agua en estado libre representa del agua '
                             'celular total aproximadamente:',
                 'alternativas': ['25%', '5%', '50%', '75%', '95%'],
                 'correcta': 'E'},
                {'pregunta': 'El agua en estado libre desempeña un papel '
                             'como:',
                 'alternativas': ['Solvente estable e ionizante',
                                  'Estructura rígida',
                                  'Fuente de energía exclusiva',
                                  'Pigmento celular',
                                  'Material genético'],
                 'correcta': 'A'},
                {'pregunta': 'El agua ligada representa del agua celular '
                             'total aproximadamente:',
                 'alternativas': ['95%', '75%', '5%', '50%', '25%'],
                 'correcta': 'C'},
                {'pregunta': 'El agua ligada comprende el agua de imbibición '
                             'y el agua de:',
                 'alternativas': ['Reserva',
                                  'Filtración',
                                  'Constitución',
                                  'Excreción',
                                  'Transporte exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'La capacidad del agua de disolver gran '
                             'cantidad de moléculas se llama:',
                 'alternativas': ['Poder solvente',
                                  'Poder calorífico',
                                  'Poder oxidante',
                                  'Poder tensioactivo',
                                  'Poder reductor'],
                 'correcta': 'A'},
                {'pregunta': 'La polaridad de la molécula de agua favorece '
                             'la disociación de moléculas formadoras de:',
                 'alternativas': ['Cadenas de carbono',
                                  'Enlaces peptídicos',
                                  'Anillos aromáticos',
                                  'Iones',
                                  'Enlaces covalentes puros'],
                 'correcta': 'D'},
                {'pregunta': 'El agua de imbibición está ligada fuertemente '
                             'a la superficie de:',
                 'alternativas': ['Los lípidos exclusivamente',
                                  'Las proteínas',
                                  'Los minerales sólidos',
                                  'El ADN exclusivamente',
                                  'Los carbohidratos'],
                 'correcta': 'B'},
                {'pregunta': 'Para liberar el agua ligada de las proteínas '
                             'se requiere:',
                 'alternativas': ['Ninguna energía',
                                  'Solo luz solar',
                                  'Solo un cambio de temperatura leve',
                                  'Grandes cantidades de energía',
                                  'Solo presión atmosférica normal'],
                 'correcta': 'D'},
                {'pregunta': 'Las sales minerales son compuestos neutros '
                             'producidos por la reacción de un ácido y:',
                 'alternativas': ['Una base',
                                  'Un catión',
                                  'Un electrolito neutro',
                                  'Un anión exclusivo',
                                  'Agua pura'],
                 'correcta': 'A'},
                {'pregunta': 'En estado sólido, las sales minerales forman, '
                             'por ejemplo:',
                 'alternativas': ['Solo gases disueltos',
                                  'Solo enzimas',
                                  'Huesos y dientes',
                                  'Solo membranas celulares',
                                  'Solo líquidos corporales'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando una sal se disuelve en agua, se disocia '
                             'en:',
                 'alternativas': ['Compuestos orgánicos',
                                  'Solo electrones libres',
                                  'Moléculas neutras',
                                  'Iones (cationes y aniones)',
                                  'Solo protones'],
                 'correcta': 'D'},
                {'pregunta': 'Los iones con carga negativa se llaman:',
                 'alternativas': ['Cationes',
                                  'Isótopos',
                                  'Electrolitos neutros',
                                  'Aniones',
                                  'Radicales libres'],
                 'correcta': 'D'},
                {'pregunta': 'Los iones con carga positiva se llaman:',
                 'alternativas': ['Fotones',
                                  'Electrones libres',
                                  'Neutrones',
                                  'Aniones',
                                  'Cationes'],
                 'correcta': 'E'},
                {'pregunta': 'Las sales minerales más abundantes en el '
                             'cuerpo humano contienen fósforo y:',
                 'alternativas': ['Magnesio',
                                  'Sodio',
                                  'Calcio',
                                  'Potasio',
                                  'Cloro'],
                 'correcta': 'C'},
                {'pregunta': 'El electrolito cuya concentración elevada '
                             'produce hipertensión arterial es:',
                 'alternativas': ['El magnesio',
                                  'El cloruro',
                                  'El sodio',
                                  'El calcio',
                                  'El potasio'],
                 'correcta': 'C'},
                {'pregunta': 'El electrolito clave en la contracción '
                             'muscular y la coagulación de la sangre es:',
                 'alternativas': ['El cloruro',
                                  'El calcio',
                                  'El bicarbonato',
                                  'El sodio',
                                  'El fosfato'],
                 'correcta': 'B'},
                {'pregunta': 'El electrolito que actúa como cofactor '
                             'enzimático y forma parte de la clorofila es:',
                 'alternativas': ['El magnesio',
                                  'El sodio',
                                  'El calcio',
                                  'El fosfato',
                                  'El potasio'],
                 'correcta': 'A'},
                {'pregunta': 'El fosfato (PO43-) forma parte de nucleótidos, '
                             'ADN y:',
                 'alternativas': ['ARN',
                                  'Carbohidratos exclusivamente',
                                  'Lípidos exclusivamente',
                                  'Proteínas exclusivamente',
                                  'Vitaminas'],
                 'correcta': 'A'},
                {'pregunta': 'La función del agua que consiste en llevar '
                             'sustancias del interior al exterior de la '
                             'célula se llama función:',
                 'alternativas': ['Estructural',
                                  'Lubricante',
                                  'Química',
                                  'De transporte',
                                  'Térmica'],
                 'correcta': 'D'},
                {'pregunta': 'La función del agua que da forma y volumen a '
                             'las células se llama función:',
                 'alternativas': ['De transporte',
                                  'Estructural',
                                  'Química',
                                  'Termorreguladora',
                                  'Lubricante'],
                 'correcta': 'B'},
                {'pregunta': 'La función del agua que mantiene el cuerpo a '
                             'temperatura constante, como en la sudoración, '
                             'se llama función:',
                 'alternativas': ['Estructural',
                                  'De transporte',
                                  'Termorreguladora',
                                  'Química',
                                  'Lubricante'],
                 'correcta': 'C'},
                {'pregunta': 'La función del agua que actúa en reacciones '
                             'como la hidrólisis o la condensación se llama '
                             'función:',
                 'alternativas': ['Lubricante',
                                  'Estructural',
                                  'Termorreguladora',
                                  'De transporte',
                                  'Química'],
                 'correcta': 'E'},
                {'pregunta': 'La función del agua que amortigua roces y '
                             'golpes en las articulaciones se llama función:',
                 'alternativas': ['Termorreguladora',
                                  'Química',
                                  'Lubricante',
                                  'Estructural',
                                  'De transporte'],
                 'correcta': 'C'},
                {'pregunta': 'La concentración elevada de potasio en la '
                             'sangre conlleva a:',
                 'alternativas': ['Hipotensión',
                                  'Diabetes',
                                  'Osteoporosis',
                                  'Anemia',
                                  'Hipertensión'],
                 'correcta': 'A'},
                {'pregunta': 'Además de ser cofactor enzimático, el magnesio '
                             'estabiliza:',
                 'alternativas': ['El aparato de Golgi',
                                  'Los ribosomas',
                                  'El núcleo',
                                  'Los lisosomas',
                                  'Las mitocondrias'],
                 'correcta': 'B'},
                {'pregunta': 'El cloruro abunda en la mucosa gástrica, la '
                             'orina, el sudor y:',
                 'alternativas': ['El plasma exclusivamente',
                                  'La saliva exclusivamente',
                                  'Las lágrimas exclusivamente',
                                  'La bilis exclusivamente',
                                  'La leche'],
                 'correcta': 'E'},
                {'pregunta': 'A diferencia del fosfato, que es tampón '
                             'intracelular, el bicarbonato actúa como '
                             'tampón:',
                 'alternativas': ['Mitocondrial',
                                  'Nuclear',
                                  'Ribosomal',
                                  'Extracelular',
                                  'Lisosomal'],
                 'correcta': 'D'},
                {'pregunta': 'El calcio, además de la estructura ósea y la '
                             'coagulación, participa en los procesos de:',
                 'alternativas': ['Replicación del ADN',
                                  'Traducción del ARN',
                                  'Secreción de las células nerviosas',
                                  'Fotosíntesis',
                                  'Respiración celular exclusiva'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CARACTERÍSTICAS GENERALES DE LAS '
                                'BIOMOLÉCULAS INORGÁNICAS',
                      'items': ['Las biomoléculas inorgánicas se '
                                'caracterizan por la ausencia de enlaces '
                                'carbono-carbono en su estructura química.']},
                     {'titulo': 'EL AGUA',
                      'items': ['La molécula de agua está formada por dos '
                                'átomos de hidrógeno y uno de oxígeno, '
                                'unidos por enlaces covalentes.']},
                     {'titulo': 'AGUA EN LA CÉLULA',
                      'items': ['El agua libre representa el 95% del agua '
                                'celular, y actúa como solvente estable e '
                                'ionizante.']},
                     {'titulo': 'PROPIEDADES DEL AGUA',
                      'items': ['El poder solvente del agua es su capacidad '
                                'de disolver gran cantidad de moléculas '
                                'inorgánicas y orgánicas.']},
                     {'titulo': 'FUNCIONES DEL AGUA',
                      'items': ['La función de transporte: el agua '
                                'transporta sustancias del interior al '
                                'exterior de la célula y viceversa.']},
                     {'titulo': 'SALES MINERALES Y ELECTROLITOS',
                      'items': ['Las sales minerales son compuestos neutros '
                                'producidos por la reacción de un ácido y '
                                'una base.']},
                     {'titulo': 'FUNCIONES DE LOS ELECTROLITOS',
                      'items': ['La concentración elevada de sodio '
                                '(Na<super>+</super>) en la sangre produce '
                                'hipertensión arterial.']}]},
 {'num': 4,
  'titulo': 'Biomoléculas Orgánicas',
  'secciones': [{'titulo': '4.1.1 CARACTERÍSTICAS DE LOS CARBOHIDRATOS',
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
                {'titulo': '4.1.2 FUNCIONES DE LOS CARBOHIDRATOS',
                 'items': ['Los carbohidratos son fuente {inmediata} de '
                           'energía, proporcionando la energía de {arranque} '
                           'para las actividades vitales.',
                           'Los carbohidratos sirven como {reserva '
                           'energética}: el {glucógeno} en animales y el '
                           'almidón en plantas.',
                           'Los carbohidratos participan como materiales '
                           '{estructurales}, como la {celulosa} en las '
                           'fibras vegetales.']},
                {'titulo': '4.1.3.A CLASIFICACIÓN: MONOSACÁRIDOS',
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
                {'titulo': '4.1.3.B OLIGOSACÁRIDOS Y DISACÁRIDOS',
                 'items': ['Los {oligosacáridos} son cadenas de 2 a 10 '
                           'monosacáridos unidos por un enlace '
                           '{O-glucosídico}.',
                           'Los {disacáridos} son los oligosacáridos más '
                           'abundantes, formados por la unión de dos '
                           '{monosacáridos}.']},
                {'titulo': '4.2.1 LÍPIDOS: CARACTERÍSTICAS Y FUNCIONES',
                 'items': ['Los lípidos son insolubles en {agua}, pero '
                           'solubles en solventes orgánicos como el '
                           'cloroformo o el éter.',
                           'Los lípidos son {anfipáticos}: tienen una '
                           'porción polar o hidrofílica y otra no polar o '
                           '{hidrofóbica}.',
                           'Los lípidos sirven como fuente y '
                           '{almacenamiento} de energía, aislantes térmicos, '
                           'protección de órganos y componentes de '
                           '{membranas}.']},
                {'titulo': '4.2.3 COMPOSICIÓN MOLECULAR: ÁCIDOS GRASOS',
                 'items': ['Los ácidos grasos son cadenas hidrocarbonadas '
                           'con un {grupo carboxilo} en un extremo.',
                           'Los ácidos grasos {saturados} tienen solo '
                           'enlaces sencillos, cadenas rectas, y son sólidos '
                           'a temperatura ambiente.',
                           'Los niveles elevados de grasas saturadas pueden '
                           'producir {arterioesclerosis}.',
                           'Los ácidos grasos {insaturados} tienen uno o más '
                           'dobles enlaces, son de origen {vegetal} y de '
                           'consistencia fluida.',
                           'El ácido {palmítico} (16 carbonos) está presente '
                           'en las grasas de carnes rojas y derivados de la '
                           'leche.',
                           'El ácido {oleico} (18 carbonos) es un ácido '
                           'graso insaturado con un solo doble enlace.']},
                {'titulo': '4.2.4.A LÍPIDOS SIMPLES',
                 'items': ['Los {lípidos simples} son ésteres de alcohol y '
                           'ácidos grasos, con solo carbono, {hidrógeno} y '
                           'oxígeno.',
                           'Los {triglicéridos} o triacilgliceroles están '
                           'formados por glicerol y tres ácidos grasos, '
                           'unidos por enlace {éster}.',
                           'Los {homoglicéridos} tienen los tres ácidos '
                           'grasos del mismo tipo; los {heteroglicéridos} de '
                           'tipos diferentes.',
                           'Una grasa en estado líquido se llama {aceite}; '
                           'en estado sólido se llama {sebo}.',
                           'Los {céridos}, o ceras, son lípidos formados por '
                           'un alcohol superior esterificado con un ácido '
                           'graso; cumplen función de {protección}.',
                           'Ejemplos de céridos son la {lanolina} (lana), la '
                           'miricina (cera de abeja) y el {espermaceti} '
                           '(cabeza de ballenas).']},
                {'titulo': '4.2.4.B LÍPIDOS COMPUESTOS',
                 'items': ['Los {lípidos compuestos} son los principales '
                           'componentes de la estructura de las {membranas} '
                           'celulares.',
                           'Además de C, H y O, los lípidos compuestos '
                           'contienen {fósforo}, nitrógeno u otros '
                           'compuestos orgánicos.',
                           'Los {fosfolípidos} tienen dos colas de ácidos '
                           'grasos hidrofóbicas y una cabeza {hidrofílica} '
                           'de fosfato; son moléculas {anfipáticas}.',
                           'Entre los fosfoglicéridos están las {lecitinas} '
                           '(fosfatidil-colina) y las cefalinas, los lípidos '
                           'más importantes de la {membrana} celular.',
                           'Las {esfingomielinas} presentan el alcohol '
                           'esfingosina y son abundantes en el {cerebro} y '
                           'el tejido nervioso.',
                           'Los {glicoesfingolípidos} contienen esfingosina, '
                           'ácido graso y carbohidrato; incluyen a los '
                           '{cerebrósidos} y gangliósidos.',
                           'Los {gangliósidos} forman la sustancia gris del '
                           'cerebro e intervienen en la transmisión de '
                           'impulsos durante la {sinapsis}.']},
                {'titulo': '4.2.4.C ESTEROIDES',
                 'items': ['Los {esteroides} derivan de un hidrocarburo '
                           'tetracíclico de 17 carbonos, llamado '
                           'ciclopentano {perhidrofenantreno}.',
                           'El {colesterol} es un esterol de origen animal, '
                           'componente de la membrana de células {animales}, '
                           'donde influye en su fluidez.',
                           'Niveles elevados de colesterol están '
                           'relacionados con la {arterioesclerosis}.',
                           'Derivados del colesterol incluyen hormonas '
                           'sexuales, la vitamina {D3} o colecalciferol, y '
                           'los ácidos {biliares}.',
                           'El {ergosterol} se encuentra en las levaduras; '
                           'de él se sintetiza la vitamina {D2} o '
                           'calciferol.']},
                {'titulo': '4.3.1 PROTEÍNAS: CARACTERÍSTICAS Y FUNCIONES',
                 'items': ['Las proteínas son los compuestos orgánicos más '
                           '{abundantes} en las células, constituyendo hasta '
                           'el 50% del peso {seco}.',
                           'Las proteínas están formadas por unidades '
                           'estructurales llamadas {aminoácidos}.',
                           'Solo {20} aminoácidos, llamados alfa '
                           'aminoácidos, pueden formar proteínas.',
                           'Función de {transporte}: la hemoglobina '
                           'transporta oxígeno desde los pulmones a los '
                           'tejidos.',
                           'Función {estructural}: la queratina forma la '
                           'piel y el cabello; el {colágeno} forma el '
                           'cartílago.',
                           'Función de {defensa}: las inmunoglobulinas '
                           'forman anticuerpos que reconocen antígenos.',
                           'Función {hormonal}: la insulina y el glucagón '
                           'regulan procesos corporales.',
                           'Función {enzimática}: muchas proteínas catalizan '
                           'reacciones químicas metabólicas.']},
                {'titulo': '4.3.3 COMPOSICIÓN: AMINOÁCIDOS',
                 'items': ['Todo aminoácido tiene un carbono central unido a '
                           'un grupo {amino}, un grupo carboxilo y un grupo '
                           '{R}.',
                           'El cuerpo humano puede sintetizar {10} '
                           'aminoácidos, llamados no esenciales.',
                           'Los otros {10} aminoácidos, llamados esenciales, '
                           'deben obtenerse mediante la {dieta}.',
                           'El huevo, la leche, la carne y el pescado '
                           'contienen todos los aminoácidos {esenciales}.']},
                {'titulo': '4.3.4 ESTRUCTURA DE LAS PROTEÍNAS',
                 'items': ['La estructura {primaria} es la secuencia de '
                           'aminoácidos, representada como cadena lineal con '
                           'grupo amino {NH2} y carboxilo terminal.',
                           'La estructura {secundaria} surge del plegamiento '
                           'de la cadena; sus dos tipos son la {alfa hélice} '
                           'y la beta plegada.',
                           'La {alfa hélice} se produce cuando la cadena se '
                           'enrolla sobre sí misma por puentes de '
                           '{hidrógeno}; ejemplo: la queratina.',
                           'La {beta plegada} da apariencia de lámina '
                           'plegada; ejemplo: la {fibroína} de la seda.',
                           'La estructura {terciaria} es la conformación '
                           'tridimensional globular, formada por puentes '
                           '{disulfuro}; ejemplo: la mioglobina.',
                           'Las enzimas, hormonas y anticuerpos tienen '
                           'estructura {terciaria}.',
                           'La estructura {cuaternaria} implica la '
                           'interacción de dos o más cadenas polipeptídicas; '
                           'ejemplos: la insulina y la {hemoglobina}.',
                           'Un aminoácido incorrecto en la hemoglobina '
                           '(valina en vez de ácido glutámico) causa la '
                           'enfermedad de células {falciformes}.',
                           'La {desnaturalización} es la pérdida de la '
                           'función de una proteína por alteraciones '
                           'causadas por el calor o cambios de {pH}.']},
                {'titulo': '4.3.5 LAS PROTEÍNAS COMO ENZIMAS',
                 'items': ['Con excepción de un pequeño grupo de ARN '
                           'catalítico, todas las {enzimas} son proteínas.',
                           'Las enzimas son {catalizadores} de las '
                           'reacciones químicas en los seres vivos.',
                           'Los reactantes sobre los que actúa la enzima se '
                           'llaman {sustratos}; cada enzima actúa sobre un '
                           'sustrato {específico}.',
                           'Los sustratos se enlazan temporalmente a las '
                           'enzimas en lugares específicos llamados sitios '
                           '{activos}.']},
                {'titulo': '4.3.6.A PROTEÍNAS SIMPLES: GLOBULARES',
                 'items': ['Las {proteínas simples} u holoproteínas están '
                           'constituidas solo por {aminoácidos}.',
                           'Las {albúminas} son solubles en agua; ejemplos: '
                           'la lactoalbúmina de la leche y la ovoalbúmina '
                           'del {huevo}.',
                           'Las {globulinas} son solubles en soluciones '
                           'salinas; incluyen las gammaglobulinas para la '
                           'defensa {inmunitaria}.',
                           'Las {glutelinas} son insolubles en agua pero '
                           'solubles en soluciones ácidas o básicas; '
                           'ejemplo: el gluten del {trigo}.',
                           'Las {prolaminas} son ricas en el aminoácido '
                           'prolina; ejemplo: la zeína en el {maíz}.',
                           'Las {protaminas} son ricas en arginina y se '
                           'asocian a ácidos nucleicos en espermatozoides, '
                           'como la salmina del {salmón}.']},
                {'titulo': '4.3.6.B PROTEÍNAS SIMPLES: FIBROSAS',
                 'items': ['Las {proteínas fibrosas} o escleroproteínas son '
                           'insolubles en agua, con funciones '
                           '{estructurales} y de protección.',
                           'La {queratina}, rica en cisteína, constituye la '
                           'piel, cabellos, uñas y {plumas}.',
                           'El {colágeno} es una proteína de sostén, '
                           'componente del tejido {conjuntivo}, '
                           'cartilaginoso y de los huesos.',
                           'La {elastina} es responsable de la elasticidad '
                           'de la piel, ligamentos y vasos {sanguíneos}.',
                           'La {actina} forma los filamentos delgados y la '
                           '{miosina} los filamentos gruesos de las '
                           'miofibrillas musculares.',
                           'El {fibrinógeno} es la proteína responsable de '
                           'la coagulación {sanguínea}.']},
                {'titulo': '4.3.6.C PROTEÍNAS CONJUGADAS (HETEROPROTEÍNAS)',
                 'items': ['Las {proteínas conjugadas} están formadas por '
                           'una proteína simple más un {grupo prostético} no '
                           'proteico.',
                           'En las {nucleoproteínas} el grupo prostético es '
                           'el ácido nucleico; ejemplo: el ADN asociado a '
                           'histonas forma la {cromatina}.',
                           'En las {lipoproteínas} el grupo prostético es un '
                           'lípido, transportado en el {plasma} sanguíneo.',
                           'En las {glicoproteínas} el grupo prostético es '
                           'un carbohidrato; ejemplo: las '
                           '{inmunoglobulinas}.',
                           'En las {cromoproteínas} el grupo prostético '
                           'puede ser el grupo hemo, con {hierro}, como en '
                           'la hemoglobina.',
                           'La {clorofila} es una cromoproteína cuyo grupo '
                           'prostético, la porfirina, contiene {magnesio}.',
                           'En las {metaloproteínas} el grupo prostético es '
                           'un electrolito metálico; ejemplo: la '
                           'hemocianina, que transporta oxígeno con '
                           '{cobre}.']},
                {'titulo': '4.4.1 COMPOSICIÓN: NUCLEÓTIDOS',
                 'items': ['Los ácidos nucleicos son polímeros lineales de '
                           '{nucleótidos}: ADN y {ARN}.',
                           'Un nucleótido se compone de tres subunidades: '
                           'una {base nitrogenada}, una pentosa y un grupo '
                           '{fosfato}.',
                           'Las bases {púricas}, adenina y guanina, tienen '
                           'dos anillos heterocíclicos fusionados.',
                           'Las bases {pirimídicas} —citosina, timina y '
                           'uracilo— tienen un solo anillo heterocíclico.',
                           'La {timina} solo forma parte del ADN; el '
                           '{uracilo} solo forma parte del ARN.',
                           'El azúcar del ADN es la {desoxirribosa}; el '
                           'azúcar del ARN es la {ribosa}.']},
                {'titulo': '4.4.2.1 GENERALIDADES DEL ADN',
                 'items': ['El ADN contiene toda la {información genética} y '
                           'tiene la capacidad de {replicarse}.',
                           'Un {gen} es un segmento de ADN con la '
                           'información para producir una proteína.',
                           'En células eucariotas, el ADN se localiza en el '
                           'núcleo, mitocondrias y {cloroplastos}.',
                           'El ADN consta de dos cadenas de polinucleótidos '
                           'enrolladas, a modo de {escalera en espiral}.',
                           'La adenina se une con la {timina} mediante dos '
                           'puentes de hidrógeno; la guanina con la '
                           '{citosina}, mediante tres.']},
                {'titulo': '4.4.2.2 MODELO DE LA DOBLE HÉLICE',
                 'items': ['En {1953}, {Watson y Crick} propusieron el '
                           'modelo de la doble hélice del ADN, ganando el '
                           'Premio {Nobel}.',
                           'Las dos cadenas del ADN son {antiparalelas}, '
                           'unidas por puentes de hidrógeno entre bases A-T '
                           'y {C-G}.',
                           'El par de bases más estable es {C-G}, unido por '
                           'tres puentes de hidrógeno.']},
                {'titulo': '4.4.2.3 REPLICACIÓN DEL ADN',
                 'items': ['La replicación del ADN es {semiconservativa}: la '
                           'nueva doble hélice tiene una hebra original y '
                           'una recién {sintetizada}.',
                           'Los nucleótidos se unen según la '
                           'complementariedad de bases: adenina con '
                           '{timina}, guanina con {citosina}.',
                           'La cadena de ADN no puede iniciarse sola; '
                           'requiere un {cebador} o primer de ARN.',
                           'Las enzimas {helicasas} rompen los puentes de '
                           'hidrógeno para iniciar la replicación en puntos '
                           'llamados {replicones}.',
                           'Los fragmentos discontinuos de la hebra hija se '
                           'llaman fragmentos de {Okazaki}.']},
                {'titulo': '4.4.2.4 FUNCIONES DEL ADN',
                 'items': ['El ADN tiene la capacidad de {replicarse}, para '
                           'que las células hijas tengan la misma dotación '
                           '{genética} que la madre.',
                           'Dentro de los cromosomas están los {genes}, que '
                           'contienen la información para fabricar las '
                           '{proteínas} que requiere el ser vivo.',
                           'Esta fabricación de proteínas ocurre mediante la '
                           'mediación del {ARN}, que transcribe y traduce la '
                           'información genética.']},
                {'titulo': '4.4.3.1 EL ARN Y LA TRANSCRIPCIÓN',
                 'items': ['El ARN se diferencia del ADN porque presenta el '
                           'azúcar {ribosa} y la base {uracilo} en lugar de '
                           'la timina.',
                           'Las moléculas de ARN son {monocatenarias}, a '
                           'diferencia del ADN, que es bicatenario.',
                           'El proceso por el cual se sintetiza ARN a partir '
                           'de un molde de ADN se llama {transcripción}.',
                           'La enzima que cataliza la transcripción es la '
                           '{ARN polimerasa}.',
                           'A diferencia de la ADN polimerasa, la ARN '
                           'polimerasa no requiere un {cebador} para iniciar '
                           'la síntesis.',
                           'La ARN polimerasa se une al ADN en una secuencia '
                           'llamada {promotor}.']},
                {'titulo': '4.4.3.3 TIPOS DE ARN',
                 'items': ['El {ARN mensajero} (ARNm) lleva la información '
                           'genética copiada del ADN en tripletes llamados '
                           '{codones}.',
                           'El {ARN de transferencia} (ARNt) sirve de '
                           'adaptador entre el ARNm y los aminoácidos, con '
                           'forma de {trébol}.',
                           'El {ARN ribosómico} (ARNr) forma los '
                           '{ribosomas}, junto con proteínas.']},
                {'titulo': '4.4.3.4 LA TRADUCCIÓN',
                 'items': ['En la traducción participa el {ARN ribosomal}, '
                           'que forma los ribosomas, donde se sintetizan las '
                           '{proteínas}.',
                           'El {ARN de transferencia} lleva un anticodón de '
                           'tres bases, y en otra parte un sitio de unión a '
                           'un {aminoácido}.',
                           'Paso 1: el {ARNm} se coloca sobre un ribosoma y '
                           'se inicia la interpretación del mensaje.',
                           'Paso 2: la información del ARNm se lee por '
                           'tripletes; a cada paquete de tres letras se le '
                           'llama {codón}.',
                           'Paso 3: cada ARNt, con su {anticodón} '
                           'correspondiente, coloca el aminoácido específico '
                           'según el mensaje genético.',
                           'Paso 4: los aminoácidos se unen por enlaces '
                           '{peptídicos}, formando la cadena de proteína.',
                           'Paso 5: cuando termina de interpretarse el '
                           'mensaje, la {proteína} se libera del ribosoma.']},
                {'titulo': '4.4.3.5 FUNCIONES DEL ARN',
                 'items': ['El ARN copia al {ADN} para producir las '
                           'proteínas que necesita la célula.',
                           'El ARN une los {aminoácidos} de una proteína en '
                           'el orden indicado por el código {genético}.',
                           'El ARN forma los {ribosomas}.']}],
  'cuadros': [{'titulo': 'CLASIFICACIÓN DE MONOSACÁRIDOS POR CARBONOS',
               'encabezados': ['Tipo', 'Número de carbonos', 'Ejemplo'],
               'filas': [['{Triosas}', '3', 'Gliceraldehído'],
                         ['{Pentosas}', '5', '{Ribosa}, desoxirribosa'],
                         ['{Hexosas}', '6', '{Glucosa}, fructosa']],
               'despues_de': '4.1.3.A CLASIFICACIÓN: MONOSACÁRIDOS'}],
  'preguntas': [{'pregunta': 'Los carbohidratos también se llaman glúcidos '
                             'o:',
                 'alternativas': ['Ácidos nucleicos',
                                  'Hidratos de carbono',
                                  'Proteínas',
                                  'Aminoácidos',
                                  'Lípidos'],
                 'correcta': 'B'},
                {'pregunta': 'Los carbohidratos están formados por carbono, '
                             'hidrógeno y:',
                 'alternativas': ['Oxígeno',
                                  'Azufre',
                                  'Nitrógeno',
                                  'Fósforo',
                                  'Sodio'],
                 'correcta': 'A'},
                {'pregunta': 'En los carbohidratos, la relación entre '
                             'hidrógeno y oxígeno es de:',
                 'alternativas': ['3:1', '1:1', '2:1', '4:1', '1:2'],
                 'correcta': 'C'},
                {'pregunta': 'Los carbohidratos son sintetizados por los '
                             'autótrofos mediante:',
                 'alternativas': ['La glucólisis exclusiva',
                                  'La fotosíntesis',
                                  'La fermentación',
                                  'La digestión',
                                  'La respiración celular'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula empírica general de los '
                             'carbohidratos es:',
                 'alternativas': ['NH3',
                                  'CO2',
                                  'H2O',
                                  'C6H12O6 exclusivo',
                                  '(CH2O)n'],
                 'correcta': 'E'},
                {'pregunta': 'La función de los carbohidratos que '
                             'proporciona energía de arranque se llama:',
                 'alternativas': ['Función estructural',
                                  'Función hormonal',
                                  'Reserva energética',
                                  'Función catalítica',
                                  'Fuente inmediata de energía'],
                 'correcta': 'E'},
                {'pregunta': 'El glucógeno almacenado en hígado y músculos '
                             'cumple la función de:',
                 'alternativas': ['Transporte de oxígeno',
                                  'Fuente inmediata de energía',
                                  'Material estructural',
                                  'Reserva energética',
                                  'Catálisis enzimática'],
                 'correcta': 'D'},
                {'pregunta': 'La celulosa, presente en fibras vegetales, '
                             'cumple principalmente una función:',
                 'alternativas': ['Catalítica',
                                  'Hormonal',
                                  'Energética inmediata',
                                  'Estructural',
                                  'De transporte'],
                 'correcta': 'D'},
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
                 'alternativas': ['Triosas exclusivamente',
                                  'Hexosas exclusivamente',
                                  'Aldosas',
                                  'Cetosas',
                                  'Pentosas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los monosacáridos que poseen grupo cetona se '
                             'llaman:',
                 'alternativas': ['Polisacáridos',
                                  'Cetosas',
                                  'Disacáridos',
                                  'Pentosas exclusivamente',
                                  'Aldosas'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura cíclica con anillo de 5 átomos '
                             'de carbono, como en la glucosa, se llama:',
                 'alternativas': ['Lineal',
                                  'Cetosa exclusiva',
                                  'Furanosa',
                                  'Piranosa',
                                  'Aldosa exclusiva'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura cíclica con anillo de 4 átomos '
                             'de carbono, como en la fructosa, se llama:',
                 'alternativas': ['Piranosa',
                                  'Pentosa exclusiva',
                                  'Lineal',
                                  'Hexosa exclusiva',
                                  'Furanosa'],
                 'correcta': 'E'},
                {'pregunta': 'Las pentosas más importantes, que forman parte '
                             'de los ácidos nucleicos, son la ribosa y la:',
                 'alternativas': ['Desoxirribosa',
                                  'Manosa',
                                  'Galactosa',
                                  'Glucosa',
                                  'Fructosa'],
                 'correcta': 'A'},
                {'pregunta': 'El monosacárido más abundante en la naturaleza '
                             'y principal fuente de energía es la:',
                 'alternativas': ['Glucosa',
                                  'Ribosa',
                                  'Fructosa',
                                  'Galactosa',
                                  'Manosa'],
                 'correcta': 'A'},
                {'pregunta': 'La galactosa no se encuentra libre, sino '
                             'combinada con la glucosa para formar:',
                 'alternativas': ['Maltosa',
                                  'Sacarosa',
                                  'Lactosa',
                                  'Almidón',
                                  'Celulosa'],
                 'correcta': 'C'},
                {'pregunta': 'La manosa es constituyente de glicoproteínas '
                             'de origen:',
                 'alternativas': ['Animal',
                                  'Vegetal exclusivo',
                                  'Viral exclusivo',
                                  'Mineral',
                                  'Bacteriano exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Los oligosacáridos están formados por un '
                             'número de monosacáridos entre:',
                 'alternativas': ['1 y 2',
                                  'Más de 1000',
                                  '2 y 10',
                                  '100 y 1000',
                                  '10 y 100'],
                 'correcta': 'C'},
                {'pregunta': 'El enlace que une a los monosacáridos en los '
                             'oligosacáridos se llama enlace:',
                 'alternativas': ['Iónico',
                                  'O-glucosídico',
                                  'Fosfodiéster',
                                  'De hidrógeno exclusivo',
                                  'Peptídico'],
                 'correcta': 'B'},
                {'pregunta': 'Los disacáridos, oligosacáridos más '
                             'abundantes, están formados por la unión de:',
                 'alternativas': ['Diez monosacáridos',
                                  'Cien monosacáridos',
                                  'Un solo monosacárido',
                                  'Ningún monosacárido',
                                  'Dos monosacáridos'],
                 'correcta': 'E'},
                {'pregunta': 'Los lípidos son insolubles en agua pero '
                             'solubles en:',
                 'alternativas': ['Ácidos fuertes',
                                  'Solventes orgánicos como el cloroformo',
                                  'Bases débiles',
                                  'Sales minerales',
                                  'Ácidos nucleicos'],
                 'correcta': 'B'},
                {'pregunta': 'Los lípidos son anfipáticos porque tienen una '
                             'porción polar y otra:',
                 'alternativas': ['Ácida',
                                  'Neutra exclusiva',
                                  'Básica',
                                  'Hidrofóbica',
                                  'Radiactiva'],
                 'correcta': 'D'},
                {'pregunta': 'Los ácidos grasos saturados se caracterizan '
                             'por tener:',
                 'alternativas': ['Anillos aromáticos',
                                  'Grupos amino',
                                  'Solo enlaces sencillos',
                                  'Cadenas ramificadas',
                                  'Dobles enlaces múltiples'],
                 'correcta': 'C'},
                {'pregunta': 'Los niveles elevados de ácidos grasos '
                             'saturados pueden producir:',
                 'alternativas': ['Anemia',
                                  'Arterioesclerosis',
                                  'Diabetes exclusivamente',
                                  'Osteoporosis',
                                  'Hipoglucemia'],
                 'correcta': 'B'},
                {'pregunta': 'Los ácidos grasos insaturados tienen uno o '
                             'más:',
                 'alternativas': ['Dobles enlaces',
                                  'Puentes disulfuro',
                                  'Anillos aromáticos',
                                  'Grupos amino',
                                  'Grupos fosfato'],
                 'correcta': 'A'},
                {'pregunta': 'El ácido palmítico, presente en grasas de '
                             'carnes rojas, tiene un número de carbonos '
                             'igual a:',
                 'alternativas': ['20', '24', '16', '8', '12'],
                 'correcta': 'C'},
                {'pregunta': 'Las proteínas son los compuestos orgánicos más '
                             'abundantes en las células, constituyendo '
                             'hasta:',
                 'alternativas': ['50% o más del peso seco',
                                  '10% del peso seco',
                                  '90% del peso seco',
                                  '1% del peso seco',
                                  '5% del peso seco'],
                 'correcta': 'A'},
                {'pregunta': 'Las proteínas están formadas por unidades '
                             'estructurales llamadas:',
                 'alternativas': ['Ácidos grasos',
                                  'Aminoácidos',
                                  'Bases nitrogenadas',
                                  'Monosacáridos',
                                  'Nucleótidos'],
                 'correcta': 'B'},
                {'pregunta': 'Del total de aminoácidos existentes en la '
                             'naturaleza, cuántos pueden formar proteínas:',
                 'alternativas': ['100', '50', '20', '30', '10'],
                 'correcta': 'C'},
                {'pregunta': 'La hemoglobina, que transporta oxígeno, es un '
                             'ejemplo de proteína con función:',
                 'alternativas': ['Enzimática',
                                  'De transporte',
                                  'Hormonal',
                                  'Estructural',
                                  'De reserva'],
                 'correcta': 'B'},
                {'pregunta': 'La queratina y el colágeno son ejemplos de '
                             'proteínas con función:',
                 'alternativas': ['Hormonal',
                                  'De defensa',
                                  'De transporte',
                                  'Estructural',
                                  'Enzimática'],
                 'correcta': 'D'},
                {'pregunta': 'Las inmunoglobulinas, que forman anticuerpos, '
                             'son proteínas con función:',
                 'alternativas': ['De transporte',
                                  'De reserva',
                                  'Estructural',
                                  'Hormonal',
                                  'De defensa inmunitaria'],
                 'correcta': 'E'},
                {'pregunta': 'La insulina y el glucagón son proteínas con '
                             'función:',
                 'alternativas': ['De defensa',
                                  'Hormonal',
                                  'Contráctil',
                                  'Estructural',
                                  'Enzimática exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El cuerpo humano puede sintetizar un número de '
                             'aminoácidos (no esenciales) igual a:',
                 'alternativas': ['20', '15', '5', '0', '10'],
                 'correcta': 'E'},
                {'pregunta': 'Los aminoácidos que deben obtenerse mediante '
                             'la dieta se llaman:',
                 'alternativas': ['Básicos exclusivos',
                                  'Neutros',
                                  'Esenciales',
                                  'No esenciales',
                                  'Ácidos exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'El modelo de la doble hélice del ADN fue '
                             'propuesto en 1953 por:',
                 'alternativas': ['Virchow y Hooke',
                                  'Watson y Crick',
                                  'Schleiden y Schwann',
                                  'De Vries y Dobzhansky',
                                  'Mendel y Darwin'],
                 'correcta': 'B'},
                {'pregunta': 'En el ADN, la adenina se une con la timina '
                             'mediante:',
                 'alternativas': ['Dos puentes de hidrógeno',
                                  'Un enlace iónico',
                                  'Un enlace covalente',
                                  'Ningún enlace',
                                  'Tres puentes de hidrógeno'],
                 'correcta': 'A'},
                {'pregunta': 'En el ADN, la guanina se une con la citosina '
                             'mediante:',
                 'alternativas': ['Un enlace covalente',
                                  'Dos puentes de hidrógeno',
                                  'Ningún enlace',
                                  'Un enlace peptídico',
                                  'Tres puentes de hidrógeno'],
                 'correcta': 'E'},
                {'pregunta': 'La replicación del ADN se llama '
                             'semiconservativa porque:',
                 'alternativas': ['No se conserva ninguna hebra original',
                                  'Solo se replica la mitad del ADN',
                                  'La nueva hélice tiene una hebra original '
                                  'y una nueva',
                                  'Ambas hebras son completamente nuevas',
                                  'Se pierde toda la información'],
                 'correcta': 'C'},
                {'pregunta': 'Los fragmentos discontinuos formados durante '
                             'la replicación del ADN se llaman:',
                 'alternativas': ['Fragmentos de Darwin',
                                  'Fragmentos de Mendel',
                                  'Fragmentos de Crick',
                                  'Fragmentos de Okazaki',
                                  'Fragmentos de Watson'],
                 'correcta': 'D'},
                {'pregunta': 'El ARN se diferencia del ADN porque tiene el '
                             'azúcar ribosa y la base:',
                 'alternativas': ['Citosina',
                                  'Adenina',
                                  'Uracilo',
                                  'Timina',
                                  'Guanina'],
                 'correcta': 'C'},
                {'pregunta': 'Las moléculas de ARN, a diferencia del ADN, '
                             'son:',
                 'alternativas': ['Inexistentes en células',
                                  'Monocatenarias',
                                  'Bicatenarias',
                                  'Circulares exclusivamente',
                                  'Idénticas al ADN'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de sintetizar ARN a partir de un '
                             'molde de ADN se llama:',
                 'alternativas': ['Translocación',
                                  'Transcripción',
                                  'Traducción',
                                  'Duplicación',
                                  'Replicación'],
                 'correcta': 'B'},
                {'pregunta': 'La enzima que cataliza la transcripción es:',
                 'alternativas': ['La helicasa',
                                  'La ARN polimerasa',
                                  'La ADN polimerasa',
                                  'La ligasa',
                                  'La primasa'],
                 'correcta': 'B'},
                {'pregunta': 'El ARN mensajero (ARNm) lleva la información '
                             'genética codificada en tripletes llamados:',
                 'alternativas': ['Anticodones',
                                  'Nucleósidos',
                                  'Ribosomas',
                                  'Codones',
                                  'Promotores'],
                 'correcta': 'D'},
                {'pregunta': 'El ARN de transferencia (ARNt) tiene una forma '
                             'característica que se asemeja a:',
                 'alternativas': ['Una esfera',
                                  'Un trébol de cuatro hojas',
                                  'Una hélice simple',
                                  'Un cubo',
                                  'Una escalera'],
                 'correcta': 'B'},
                {'pregunta': 'El ARN ribosómico (ARNr) forma parte de:',
                 'alternativas': ['Las mitocondrias exclusivamente',
                                  'El núcleo exclusivamente',
                                  'El citoesqueleto',
                                  'La membrana celular',
                                  'Los ribosomas'],
                 'correcta': 'E'},
                {'pregunta': 'Los lípidos simples son ésteres de alcohol y '
                             'ácidos grasos, con solo carbono, hidrógeno y:',
                 'alternativas': ['Oxígeno',
                                  'Fósforo',
                                  'Nitrógeno',
                                  'Calcio',
                                  'Azufre'],
                 'correcta': 'A'},
                {'pregunta': 'Un triglicérido está formado por glicerol y '
                             'tres ácidos grasos unidos mediante enlace:',
                 'alternativas': ['Glucosídico',
                                  'Amida',
                                  'Éster',
                                  'De hidrógeno',
                                  'Peptídico'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando los tres ácidos grasos de un '
                             'triglicérido son del mismo tipo, se llama:',
                 'alternativas': ['Cérido',
                                  'Heteroglicérido',
                                  'Glicoesfingolípido',
                                  'Fosfoglicérido',
                                  'Homoglicérido'],
                 'correcta': 'E'},
                {'pregunta': 'Una grasa en estado sólido, como la que forman '
                             'los triglicéridos, se llama:',
                 'alternativas': ['Colesterol',
                                  'Cera',
                                  'Aceite',
                                  'Fosfolípido',
                                  'Sebo'],
                 'correcta': 'E'},
                {'pregunta': 'Los lípidos formados por un alcohol superior '
                             'esterificado con un ácido graso, con función '
                             'de protección, se llaman:',
                 'alternativas': ['Esteroides',
                                  'Glicolípidos',
                                  'Triglicéridos',
                                  'Fosfolípidos',
                                  'Céridos o ceras'],
                 'correcta': 'E'},
                {'pregunta': 'La cera presente en la cabeza de las ballenas '
                             'se llama:',
                 'alternativas': ['Cerumen',
                                  'Miricina',
                                  'Lanolina',
                                  'Colesterilo',
                                  'Espermaceti'],
                 'correcta': 'E'},
                {'pregunta': 'Los lípidos que son los principales '
                             'componentes de las membranas celulares se '
                             'llaman lípidos:',
                 'alternativas': ['Compuestos',
                                  'Triglicéridos',
                                  'Esteroides',
                                  'Simples',
                                  'Céridos'],
                 'correcta': 'A'},
                {'pregunta': 'Los fosfolípidos tienen dos colas hidrofóbicas '
                             'y una cabeza hidrofílica, por lo que son '
                             'moléculas:',
                 'alternativas': ['Apolares',
                                  'Neutras',
                                  'Covalentes',
                                  'Iónicas',
                                  'Anfipáticas'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los fosfoglicéridos, los lípidos más '
                             'importantes de la membrana celular son las '
                             'lecitinas y:',
                 'alternativas': ['Los sulfátidos',
                                  'El ergosterol',
                                  'Los cerebrósidos',
                                  'Las cefalinas',
                                  'Los gangliósidos'],
                 'correcta': 'D'},
                {'pregunta': 'Las esfingomielinas, que presentan el alcohol '
                             'esfingosina, son abundantes en:',
                 'alternativas': ['El cerebro y el tejido nervioso',
                                  'La piel',
                                  'El hígado',
                                  'Los riñones',
                                  'El tejido adiposo'],
                 'correcta': 'A'},
                {'pregunta': 'Los glicoesfingolípidos que forman la '
                             'sustancia gris del cerebro y participan en la '
                             'sinapsis se llaman:',
                 'alternativas': ['Fosfoglicéridos',
                                  'Cerebrósidos',
                                  'Gangliósidos',
                                  'Sulfátidos',
                                  'Céridos'],
                 'correcta': 'C'},
                {'pregunta': 'Los esteroides derivan de un hidrocarburo '
                             'tetracíclico de 17 carbonos llamado:',
                 'alternativas': ['Ciclopentano perhidrofenantreno',
                                  'Fosfoglicérido',
                                  'Ácido graso',
                                  'Glicerol',
                                  'Esfingosina'],
                 'correcta': 'A'},
                {'pregunta': 'El esterol de origen animal que influye en la '
                             'fluidez de la membrana celular es:',
                 'alternativas': ['El fosfolípido',
                                  'El ergosterol',
                                  'La lecitina',
                                  'El coprosterol',
                                  'El colesterol'],
                 'correcta': 'E'},
                {'pregunta': 'Niveles elevados de colesterol están '
                             'relacionados con la enfermedad llamada:',
                 'alternativas': ['Arterioesclerosis',
                                  'Hipertiroidismo',
                                  'Anemia',
                                  'Osteoporosis',
                                  'Diabetes'],
                 'correcta': 'A'},
                {'pregunta': 'El esterol que se encuentra en las levaduras, '
                             'del cual se sintetiza la vitamina D2, se '
                             'llama:',
                 'alternativas': ['Fosfatidilinositol',
                                  'Cerebrósido',
                                  'Colesterol',
                                  'Ergosterol',
                                  'Coprosterol'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura primaria de una proteína es la '
                             'secuencia de:',
                 'alternativas': ['Fosfolípidos',
                                  'Ácidos grasos',
                                  'Monosacáridos',
                                  'Aminoácidos',
                                  'Nucleótidos'],
                 'correcta': 'D'},
                {'pregunta': 'Los dos tipos de estructura secundaria de las '
                             'proteínas son la alfa hélice y la:',
                 'alternativas': ['Beta plegada',
                                  'Delta hélice',
                                  'Omega hélice',
                                  'Gamma plegada',
                                  'Terciaria plegada'],
                 'correcta': 'A'},
                {'pregunta': 'La estructura secundaria alfa hélice, presente '
                             'en la queratina, se forma por:',
                 'alternativas': ['Puentes disulfuro',
                                  'Puentes de hidrógeno',
                                  'Enlaces peptídicos',
                                  'Enlaces covalentes',
                                  'Enlaces iónicos'],
                 'correcta': 'B'},
                {'pregunta': 'La estructura secundaria en lámina plegada, '
                             'presente en la fibroína de la seda, se llama:',
                 'alternativas': ['Terciaria',
                                  'Alfa hélice',
                                  'Primaria compleja',
                                  'Beta plegada',
                                  'Cuaternaria'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura terciaria de una proteína es su '
                             'conformación tridimensional globular, formada '
                             'por puentes:',
                 'alternativas': ['De hidrógeno exclusivamente',
                                  'Disulfuro',
                                  'Glucosídicos',
                                  'Peptídicos',
                                  'Iónicos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Las enzimas, hormonas y anticuerpos tienen '
                             'estructura:',
                 'alternativas': ['Solo cuaternaria',
                                  'Primaria',
                                  'Solo secundaria',
                                  'Terciaria',
                                  'Ninguna estructura definida'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura cuaternaria implica la '
                             'interacción de dos o más cadenas '
                             'polipeptídicas, como en la insulina y la:',
                 'alternativas': ['Fibroína',
                                  'Actina',
                                  'Elastina',
                                  'Hemoglobina',
                                  'Queratina'],
                 'correcta': 'D'},
                {'pregunta': 'La enfermedad de células falciformes es '
                             'causada por un cambio en un aminoácido de:',
                 'alternativas': ['El colágeno',
                                  'La insulina',
                                  'La miosina',
                                  'La queratina',
                                  'La hemoglobina'],
                 'correcta': 'E'},
                {'pregunta': 'La pérdida de función de una proteína por '
                             'alteraciones causadas por el calor o cambios '
                             'de pH se llama:',
                 'alternativas': ['Fermentación',
                                  'Oxidación',
                                  'Polimerización',
                                  'Hidrólisis',
                                  'Desnaturalización'],
                 'correcta': 'E'},
                {'pregunta': 'Con excepción de un pequeño grupo de ARN '
                             'catalítico, todas las enzimas son:',
                 'alternativas': ['Carbohidratos',
                                  'Proteínas',
                                  'Ácidos nucleicos',
                                  'Minerales',
                                  'Lípidos'],
                 'correcta': 'B'},
                {'pregunta': 'El reactante sobre el que actúa '
                             'específicamente una enzima se llama:',
                 'alternativas': ['Sustrato',
                                  'Cofactor',
                                  'Producto',
                                  'Catalizador',
                                  'Coenzima'],
                 'correcta': 'A'},
                {'pregunta': 'El lugar específico donde se enlaza '
                             'temporalmente el sustrato a la enzima se '
                             'llama:',
                 'alternativas': ['Cadena lateral',
                                  'Grupo carboxilo',
                                  'Sitio activo',
                                  'Grupo prostético',
                                  'Puente disulfuro'],
                 'correcta': 'C'},
                {'pregunta': 'Las proteínas simples, constituidas solo por '
                             'aminoácidos, también se llaman:',
                 'alternativas': ['Cromoproteínas',
                                  'Heteroproteínas',
                                  'Metaloproteínas',
                                  'Holoproteínas',
                                  'Glicoproteínas'],
                 'correcta': 'D'},
                {'pregunta': 'Las albúminas, como la ovoalbúmina del huevo, '
                             'son proteínas globulares solubles en:',
                 'alternativas': ['Bases exclusivamente',
                                  'Ácidos exclusivamente',
                                  'Alcohol',
                                  'Grasas',
                                  'Agua'],
                 'correcta': 'E'},
                {'pregunta': 'Las globulinas, escasamente solubles en agua '
                             'pero solubles en soluciones salinas, incluyen '
                             'a las gammaglobulinas de la defensa:',
                 'alternativas': ['Respiratoria',
                                  'Inmunitaria',
                                  'Nerviosa',
                                  'Digestiva',
                                  'Circulatoria'],
                 'correcta': 'B'},
                {'pregunta': 'Las glutelinas, insolubles en agua pero '
                             'solubles en ácidos o bases, incluyen al gluten '
                             'del:',
                 'alternativas': ['Trigo',
                                  'Cebada exclusiva',
                                  'Maíz',
                                  'Arroz',
                                  'Ajonjolí'],
                 'correcta': 'A'},
                {'pregunta': 'Las prolaminas, ricas en el aminoácido '
                             'prolina, incluyen a la zeína, presente en:',
                 'alternativas': ['El arroz',
                                  'La cebada',
                                  'La soya',
                                  'El maíz',
                                  'El trigo'],
                 'correcta': 'D'},
                {'pregunta': 'Las protaminas, ricas en arginina, se asocian '
                             'a ácidos nucleicos en los espermatozoides, '
                             'como la salmina del:',
                 'alternativas': ['Salmón',
                                  'Esturión',
                                  'Bacalao',
                                  'Arenque',
                                  'Atún'],
                 'correcta': 'A'},
                {'pregunta': 'Las proteínas fibrosas o escleroproteínas son, '
                             'a diferencia de las globulares:',
                 'alternativas': ['Solubles en agua',
                                  'Solubles solo en alcohol',
                                  'Insolubles en agua',
                                  'Gaseosas',
                                  'Líquidas'],
                 'correcta': 'C'},
                {'pregunta': 'La queratina, rica en cisteína, constituye la '
                             'piel, los cabellos, las uñas y:',
                 'alternativas': ['Los huesos exclusivamente',
                                  'Las plumas',
                                  'El cerebro',
                                  'Los músculos',
                                  'La sangre'],
                 'correcta': 'B'},
                {'pregunta': 'El colágeno es una proteína de sostén, '
                             'componente del tejido conjuntivo, '
                             'cartilaginoso y de:',
                 'alternativas': ['Los pulmones',
                                  'La piel exclusivamente',
                                  'La sangre',
                                  'El cerebro',
                                  'Los huesos'],
                 'correcta': 'E'},
                {'pregunta': 'La proteína responsable de la elasticidad de '
                             'la piel, ligamentos y vasos sanguíneos es:',
                 'alternativas': ['El colágeno',
                                  'La actina',
                                  'La queratina',
                                  'La elastina',
                                  'La fibroína'],
                 'correcta': 'D'},
                {'pregunta': 'La actina forma los filamentos delgados y la '
                             'miosina los filamentos gruesos, responsables '
                             'de la contracción:',
                 'alternativas': ['Respiratoria',
                                  'Muscular',
                                  'Cardíaca exclusiva',
                                  'Nerviosa',
                                  'Vascular'],
                 'correcta': 'B'},
                {'pregunta': 'La proteína responsable de la coagulación '
                             'sanguínea se llama:',
                 'alternativas': ['Queratina',
                                  'Elastina',
                                  'Fibrinógeno',
                                  'Miosina',
                                  'Colágeno'],
                 'correcta': 'C'},
                {'pregunta': 'Las proteínas conjugadas, o heteroproteínas, '
                             'están formadas por una proteína simple más:',
                 'alternativas': ['Solo carbohidratos',
                                  'Solo aminoácidos',
                                  'Un grupo prostético no proteico',
                                  'Solo agua',
                                  'Otra proteína simple'],
                 'correcta': 'C'},
                {'pregunta': 'En las nucleoproteínas, el grupo prostético es '
                             'el ácido nucleico; el ADN asociado a histonas '
                             'forma la:',
                 'alternativas': ['Mitocondria',
                                  'Pared celular',
                                  'Cromatina',
                                  'Membrana',
                                  'Vacuola'],
                 'correcta': 'C'},
                {'pregunta': 'En las lipoproteínas, el grupo prostético es '
                             'un lípido transportado en:',
                 'alternativas': ['El núcleo',
                                  'El plasma sanguíneo',
                                  'El citoplasma exclusivo',
                                  'La saliva',
                                  'La linfa exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'En las glicoproteínas, el grupo prostético es '
                             'un carbohidrato; un ejemplo son las:',
                 'alternativas': ['Histonas',
                                  'Queratinas',
                                  'Miosinas',
                                  'Elastinas',
                                  'Inmunoglobulinas'],
                 'correcta': 'E'},
                {'pregunta': 'En las cromoproteínas, el grupo prostético '
                             'hemo contiene el elemento hierro, como en la '
                             'hemoglobina y:',
                 'alternativas': ['La queratina',
                                  'El colágeno',
                                  'La mioglobina',
                                  'La actina',
                                  'La elastina'],
                 'correcta': 'C'},
                {'pregunta': 'La clorofila es una cromoproteína cuyo grupo '
                             'prostético, la porfirina, contiene el '
                             'elemento:',
                 'alternativas': ['Calcio',
                                  'Hierro',
                                  'Cobre',
                                  'Zinc',
                                  'Magnesio'],
                 'correcta': 'E'},
                {'pregunta': 'En las metaloproteínas, el grupo prostético es '
                             'un electrolito metálico; la hemocianina '
                             'transporta oxígeno usando:',
                 'alternativas': ['Cobre',
                                  'Magnesio',
                                  'Calcio',
                                  'Zinc',
                                  'Hierro'],
                 'correcta': 'A'},
                {'pregunta': 'Una de las funciones primordiales del ADN es '
                             'su capacidad de:',
                 'alternativas': ['Traducirse directamente',
                                  'Degradarse',
                                  'Fosforilarse',
                                  'Replicarse',
                                  'Transcribirse solamente'],
                 'correcta': 'D'},
                {'pregunta': 'Dentro de los cromosomas se hallan los genes, '
                             'formados por ADN, que contienen la información '
                             'para fabricar:',
                 'alternativas': ['Lípidos',
                                  'Vitaminas',
                                  'Proteínas',
                                  'Minerales',
                                  'Carbohidratos'],
                 'correcta': 'C'},
                {'pregunta': 'La fabricación de proteínas a partir de la '
                             'información del ADN ocurre mediante la '
                             'mediación de:',
                 'alternativas': ['Los ribosomas exclusivamente',
                                  'Las enzimas exclusivamente',
                                  'El citoplasma',
                                  'Las mitocondrias',
                                  'El ARN'],
                 'correcta': 'E'},
                {'pregunta': 'En la traducción, el ARN que forma los '
                             'ribosomas, donde se sintetizan las proteínas, '
                             'se llama ARN:',
                 'alternativas': ['Polimerasa',
                                  'Mensajero',
                                  'De transferencia',
                                  'Catalítico',
                                  'Ribosomal'],
                 'correcta': 'E'},
                {'pregunta': 'El grupo de tres bases que lleva el ARN de '
                             'transferencia, complementario al codón, se '
                             'llama:',
                 'alternativas': ['Triplete génico',
                                  'Codón',
                                  'Promotor',
                                  'Marco de lectura',
                                  'Anticodón'],
                 'correcta': 'E'},
                {'pregunta': 'En la traducción, la información del ARN '
                             'mensajero se lee por paquetes de tres letras '
                             'llamados:',
                 'alternativas': ['Nucleótidos simples',
                                  'Exones',
                                  'Genes',
                                  'Codones',
                                  'Anticodones'],
                 'correcta': 'D'},
                {'pregunta': 'En la traducción, los aminoácidos colocados en '
                             'el ribosoma se unen mediante enlaces:',
                 'alternativas': ['Peptídicos',
                                  'Glucosídicos',
                                  'Fosfodiéster',
                                  'De hidrógeno exclusivos',
                                  'Disulfuro exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Al terminar de interpretarse el mensaje '
                             'genético en la traducción, la proteína se '
                             'libera de:',
                 'alternativas': ['El núcleo',
                                  'El ribosoma',
                                  'El ADN',
                                  'La membrana',
                                  'El citoplasma exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las funciones del ARN está copiar al ADN '
                             'para producir las proteínas que necesita:',
                 'alternativas': ['La célula',
                                  'La mitocondria',
                                  'El núcleo',
                                  'El ribosoma exclusivo',
                                  'El citoplasma exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'Otra función del ARN es unir los aminoácidos '
                             'de una proteína en el orden indicado por:',
                 'alternativas': ['El código genético',
                                  'El pH celular',
                                  'La presión osmótica',
                                  'La temperatura',
                                  'El azar'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CARACTERÍSTICAS DE LOS CARBOHIDRATOS / '
                                'FUNCIONES DE LOS CARBOHIDRATOS (+2)',
                      'items': ['Los carbohidratos, o glúcidos, son '
                                'moléculas orgánicas formadas por carbono, '
                                'hidrógeno y oxígeno.',
                                'Los carbohidratos son fuente inmediata de '
                                'energía, proporcionando la energía de '
                                'arranque para las actividades vitales.',
                                'Los monosacáridos son los azúcares más '
                                'simples, dulces, sólidos, cristalizables e '
                                'hidrolizables.',
                                'Los oligosacáridos son cadenas de 2 a 10 '
                                'monosacáridos unidos por un enlace '
                                'O-glucosídico.']},
                     {'titulo': 'LÍPIDOS: CARACTERÍSTICAS Y FUNCIONES / '
                                'COMPOSICIÓN MOLECULAR: ÁCIDOS GRASOS',
                      'items': ['Los lípidos son insolubles en agua, pero '
                                'solubles en solventes orgánicos como el '
                                'cloroformo o el éter.',
                                'Los ácidos grasos son cadenas '
                                'hidrocarbonadas con un grupo carboxilo en '
                                'un extremo.',
                                'Los lípidos simples son ésteres de alcohol '
                                'y ácidos grasos, con solo carbono, '
                                'hidrógeno y oxígeno.',
                                'Los lípidos compuestos son los principales '
                                'componentes de la estructura de las '
                                'membranas celulares.']},
                     {'titulo': '.C ESTEROIDES / PROTEÍNAS: CARACTERÍSTICAS '
                                'Y FUNCIONES (+2)',
                      'items': ['Los esteroides derivan de un hidrocarburo '
                                'tetracíclico de 17 carbonos, llamado '
                                'ciclopentano perhidrofenantreno.',
                                'Las proteínas son los compuestos orgánicos '
                                'más abundantes en las células, '
                                'constituyendo hasta el 50% del peso seco.',
                                'Todo aminoácido tiene un carbono central '
                                'unido a un grupo amino, un grupo carboxilo '
                                'y un grupo R.',
                                'La estructura primaria es la secuencia de '
                                'aminoácidos, representada como cadena '
                                'lineal con grupo amino NH2 y carboxilo '
                                'terminal.']},
                     {'titulo': 'LAS PROTEÍNAS COMO ENZIMAS / .A PROTEÍNAS '
                                'SIMPLES: GLOBULARES (+2)',
                      'items': ['Con excepción de un pequeño grupo de ARN '
                                'catalítico, todas las enzimas son '
                                'proteínas.',
                                'Las proteínas simples u holoproteínas están '
                                'constituidas solo por aminoácidos.',
                                'Las proteínas fibrosas o escleroproteínas '
                                'son insolubles en agua, con funciones '
                                'estructurales y de protección.',
                                'Las proteínas conjugadas están formadas por '
                                'una proteína simple más un grupo prostético '
                                'no proteico.']},
                     {'titulo': 'COMPOSICIÓN: NUCLEÓTIDOS / GENERALIDADES '
                                'DEL ADN (+2)',
                      'items': ['Los ácidos nucleicos son polímeros lineales '
                                'de nucleótidos: ADN y ARN.',
                                'El ADN contiene toda la información '
                                'genética y tiene la capacidad de '
                                'replicarse.',
                                'En 1953, Watson y Crick propusieron el '
                                'modelo de la doble hélice del ADN, ganando '
                                'el Premio Nobel.',
                                'La replicación del ADN es semiconservativa: '
                                'la nueva doble hélice tiene una hebra '
                                'original y una recién sintetizada.']},
                     {'titulo': 'FUNCIONES DEL ADN / EL ARN Y LA '
                                'TRANSCRIPCIÓN (+2)',
                      'items': ['El ADN tiene la capacidad de replicarse, '
                                'para que las células hijas tengan la misma '
                                'dotación genética que la madre.',
                                'El ARN se diferencia del ADN porque '
                                'presenta el azúcar ribosa y la base uracilo '
                                'en lugar de la timina.',
                                'El ARN mensajero (ARNm) lleva la '
                                'información genética copiada del ADN en '
                                'tripletes llamados codones.',
                                'En la traducción participa el ARN '
                                'ribosomal, que forma los ribosomas, donde '
                                'se sintetizan las proteínas.']},
                     {'titulo': 'FUNCIONES DEL ARN',
                      'items': ['El ARN copia al ADN para producir las '
                                'proteínas que necesita la célula.']}]},
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
                           'los eucariotas.',
                           'El ADN procariota no está asociado a {histonas}, '
                           'y el único organelo que presentan las células '
                           'procariotas son los {ribosomas}.',
                           'Las bacterias típicas presentan diferentes '
                           'formas mantenidas por la pared celular: cocos, '
                           '{bacilos} y espirilos.']},
                {'titulo': '5.4 ESTRUCTURA BACTERIANA',
                 'items': ['La {cápsula} es una estructura de polisacáridos '
                           'que forma un glucocálix grueso y rígido, con '
                           'función de {adherencia}.',
                           'La pared celular bacteriana está formada '
                           'principalmente por {peptidoglicano} o mureína.',
                           'La tinción de {Gram} clasifica a las bacterias '
                           'en Gram positivas y Gram {negativas}.',
                           'Las bacterias {Gram positivas} tienen una pared '
                           'gruesa con 60-90% de peptidoglicano.',
                           'Las bacterias {Gram negativas} tienen menos '
                           'peptidoglicano y poseen una {membrana externa} '
                           'adicional.',
                           'Los {mesosomas} son invaginaciones de la '
                           'membrana plasmática que intervienen en la '
                           'duplicación del {ADN}.',
                           'El material genético bacteriano es una molécula '
                           'circular de ADN {bicatenario}, ubicada en el '
                           '{nucleoide}.',
                           'Los {plásmidos} son moléculas de ADN '
                           'extracromosómico que pueden conferir resistencia '
                           'a {antibióticos}.',
                           'Los {flagelos} son estructuras filamentosas '
                           'responsables de la {movilidad} bacteriana.']},
                {'titulo': '5.5 MICOPLASMAS',
                 'items': ['Los {micoplasmas}, también llamados Mollicutes o '
                           'PPLO, son las bacterias más {pequeñas} '
                           'conocidas, con diámetro de 0,125 a 0,150 µm.',
                           'Los micoplasmas son {pleomórficos}: varían su '
                           'forma (ovoide, esférica, vesicular) según las '
                           'condiciones del medio.',
                           'Los micoplasmas son los únicos procariotas '
                           'conocidos que carecen de {pared celular}.',
                           'Su membrana plasmática contiene fosfolípidos y '
                           '{colesterol}, esterol que no se encuentra en '
                           'otras células procariotas.',
                           'El protoplasma de los micoplasmas contiene ADN '
                           'de {doble hélice}, ribosomas y algunas enzimas.',
                           '{Mycoplasma pneumoniae} causa la neumonía '
                           'atípica en humanos; {Mycoplasma mycoides} causa '
                           'la pleuroneumonía bovina.']},
                {'titulo': '5.6 CIANOBACTERIAS',
                 'items': ['Las {cianobacterias}, o algas verde-azules, son '
                           'las bacterias {fotosintéticas} más '
                           'evolucionadas.',
                           'Tienen pared celular semejante a la de las '
                           'bacterias Gram {negativas}, y carecen de cilios '
                           'o {flagelos}.',
                           'Además de clorofila, contienen pigmentos '
                           'llamados {ficobilinas}: la ficocianina (azul) y '
                           'la ficoeritrina ({roja}).',
                           'Las cianobacterias pueden fijar {nitrógeno} (N2) '
                           'y convertirlo en amoniaco, sintetizando '
                           'aminoácidos y {nucleótidos}.',
                           'Entre los principales géneros de cianobacterias '
                           'están {Spirulina}, Anabaena y Nostoc.',
                           'El género {Nostoc} es comestible y se conoce '
                           'comúnmente como «{llullucha}» o «murmunta».']}],
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
                 'alternativas': ['Tejido',
                                  'Organelo',
                                  'Núcleo',
                                  'Membrana',
                                  'Pequeña habitación o celda'],
                 'correcta': 'E'},
                {'pregunta': 'La célula es considerada la unidad estructural '
                             'y:',
                 'alternativas': ['Química exclusiva',
                                  'Atómica',
                                  'Funcional fundamental de los seres vivos',
                                  'Ecológica',
                                  'Genética exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'El científico que introdujo el término '
                             '«célula» en 1665 fue:',
                 'alternativas': ['Virchow',
                                  'Robert Hooke',
                                  'Schwann',
                                  'Darwin',
                                  'Schleiden'],
                 'correcta': 'B'},
                {'pregunta': 'Robert Hooke publicó sus observaciones '
                             'celulares en el libro:',
                 'alternativas': ['El origen de las especies',
                                  'Principia',
                                  'Micrographia',
                                  'De Revolutionibus',
                                  'Systema Naturae'],
                 'correcta': 'C'},
                {'pregunta': 'Los fundadores de la teoría celular fueron '
                             'Schleiden y:',
                 'alternativas': ['Hooke',
                                  'Mendel',
                                  'Schwann',
                                  'Darwin',
                                  'Virchow'],
                 'correcta': 'C'},
                {'pregunta': 'Schleiden concluyó que todas las plantas están '
                             'constituidas por:',
                 'alternativas': ['Minerales',
                                  'Células',
                                  'Órganos exclusivamente',
                                  'Fibras',
                                  'Tejidos exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Schwann concluyó la misma idea que Schleiden, '
                             'pero referida a:',
                 'alternativas': ['Los animales',
                                  'Los hongos',
                                  'Las bacterias',
                                  'Los minerales',
                                  'Los virus'],
                 'correcta': 'A'},
                {'pregunta': 'La célebre frase «omnis cellula ex cellula» '
                             'fue sintetizada por:',
                 'alternativas': ['Rudolph Virchow',
                                  'Charles Darwin',
                                  'Robert Hooke',
                                  'Schwann',
                                  'Schleiden'],
                 'correcta': 'D'},
                {'pregunta': 'La frase «omnis cellula ex cellula» significa:',
                 'alternativas': ['Toda célula es eucariota',
                                  'Toda célula tiene núcleo',
                                  'Toda célula tiene ADN circular',
                                  'Toda célula muere pronto',
                                  'Toda célula se origina de otra célula'],
                 'correcta': 'E'},
                {'pregunta': 'Según la teoría celular, las actividades '
                             'esenciales de la vida ocurren:',
                 'alternativas': ['Fuera de las células',
                                  'Solo en el núcleo',
                                  'Solo en el citoplasma exclusivamente',
                                  'En el interior de las células',
                                  'Solo en la membrana'],
                 'correcta': 'D'},
                {'pregunta': 'Según la teoría celular, las nuevas células se '
                             'originan de:',
                 'alternativas': ['Solo del ADN libre',
                                  'Células preexistentes, por división',
                                  'Fusión de tejidos',
                                  'La nada',
                                  'Reacciones químicas espontáneas'],
                 'correcta': 'B'},
                {'pregunta': 'Las células contienen la información '
                             'hereditaria, que pasa de:',
                 'alternativas': ['Órganos a sistemas',
                                  'Células hijas a progenitoras',
                                  'Ninguna transmisión ocurre',
                                  'Células progenitoras a células hijas',
                                  'Tejidos a órganos'],
                 'correcta': 'D'},
                {'pregunta': 'El término «procariota» proviene del griego '
                             '«protos», que significa:',
                 'alternativas': ['Verdadero',
                                  'Hueco',
                                  'Núcleo',
                                  'Primitivo',
                                  'Vida'],
                 'correcta': 'D'},
                {'pregunta': 'El material genético de la célula procariota '
                             'es una molécula de ADN:',
                 'alternativas': ['Ausente',
                                  'Circular',
                                  'Ramificada',
                                  'Doble hélice exclusivamente eucariota',
                                  'Lineal'],
                 'correcta': 'B'},
                {'pregunta': 'En la célula procariota, el ADN se concentra '
                             'en una región llamada:',
                 'alternativas': ['Nucléolo',
                                  'Cromosoma',
                                  'Nucleoide',
                                  'Núcleo',
                                  'Retículo'],
                 'correcta': 'C'},
                {'pregunta': 'El término «eucariota» proviene del griego '
                             '«eu», que significa:',
                 'alternativas': ['Verdadero',
                                  'Externo',
                                  'Primitivo',
                                  'Pequeño',
                                  'Hueco'],
                 'correcta': 'A'},
                {'pregunta': 'En la célula eucariota, el ADN se encuentra '
                             'dentro de:',
                 'alternativas': ['La membrana plasmática',
                                  'El nucleoide',
                                  'El citoplasma sin protección',
                                  'La pared celular',
                                  'Un núcleo verdadero con envoltura '
                                  'nuclear'],
                 'correcta': 'E'},
                {'pregunta': 'Solo los organismos del reino monera son de '
                             'tipo celular:',
                 'alternativas': ['Viral',
                                  'Ninguno de los anteriores',
                                  'Eucariota',
                                  'Mixto',
                                  'Procariota'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio de tres dominios, Archaea y '
                             'Bacteria agrupan a los organismos:',
                 'alternativas': ['Eucariotas',
                                  'Virales',
                                  'Fúngicos exclusivamente',
                                  'Procariotas',
                                  'Mixtos'],
                 'correcta': 'D'},
                {'pregunta': 'El dominio Eukarya agrupa a todos los '
                             'organismos:',
                 'alternativas': ['Solo bacterias',
                                  'Virales exclusivamente',
                                  'Solo arqueas',
                                  'Procariotas',
                                  'Eucariotas'],
                 'correcta': 'E'},
                {'pregunta': 'El glucocálix bacteriano, cuando es grueso y '
                             'rígido, se denomina:',
                 'alternativas': ['Membrana externa',
                                  'Cápsula',
                                  'Pared celular',
                                  'Mucílago',
                                  'Periplasma'],
                 'correcta': 'B'},
                {'pregunta': 'El principal componente de la pared celular '
                             'bacteriana es:',
                 'alternativas': ['El peptidoglicano o mureína',
                                  'La quitina',
                                  'La celulosa',
                                  'La lignina',
                                  'El colesterol'],
                 'correcta': 'A'},
                {'pregunta': 'La tinción que clasifica a las bacterias según '
                             'su pared celular se llama tinción de:',
                 'alternativas': ['Giemsa',
                                  'Gram',
                                  'Ziehl-Neelsen',
                                  'Papanicolaou',
                                  'Wright'],
                 'correcta': 'B'},
                {'pregunta': 'Las bacterias Gram positivas se caracterizan '
                             'por tener una pared con un contenido de '
                             'peptidoglicano de:',
                 'alternativas': ['30 a 40%',
                                  '0%',
                                  '60 a 90%',
                                  '100%',
                                  '10 a 20%'],
                 'correcta': 'C'},
                {'pregunta': 'Las bacterias Gram negativas poseen, además de '
                             'la pared, una estructura adicional llamada:',
                 'alternativas': ['Flagelo',
                                  'Membrana externa',
                                  'Pili',
                                  'Cápsula gruesa',
                                  'Mesosoma'],
                 'correcta': 'B'},
                {'pregunta': 'Las invaginaciones de la membrana plasmática '
                             'bacteriana que intervienen en la duplicación '
                             'del ADN se llaman:',
                 'alternativas': ['Mesosomas',
                                  'Flagelos',
                                  'Plásmidos',
                                  'Pili',
                                  'Ribosomas'],
                 'correcta': 'A'},
                {'pregunta': 'El material genético bacteriano se ubica en '
                             'una región llamada:',
                 'alternativas': ['Nucleoide',
                                  'Núcleo',
                                  'Cromátida',
                                  'Nucléolo',
                                  'Centrómero'],
                 'correcta': 'A'},
                {'pregunta': 'Las moléculas de ADN extracromosómico que '
                             'pueden conferir resistencia a antibióticos se '
                             'llaman:',
                 'alternativas': ['Plásmidos',
                                  'Mesosomas',
                                  'Cápsulas',
                                  'Ribosomas',
                                  'Flagelos'],
                 'correcta': 'A'},
                {'pregunta': 'Las estructuras filamentosas responsables de '
                             'la movilidad bacteriana se llaman:',
                 'alternativas': ['Mesosomas',
                                  'Pili',
                                  'Ribosomas',
                                  'Cilios',
                                  'Flagelos'],
                 'correcta': 'E'},
                {'pregunta': 'Los micoplasmas se caracterizan por ser las '
                             'bacterias más pequeñas y por carecer de:',
                 'alternativas': ['Pared celular',
                                  'Ribosomas',
                                  'Membrana plasmática',
                                  'Citoplasma',
                                  'ADN'],
                 'correcta': 'A'},
                {'pregunta': 'Las cianobacterias son capaces de realizar:',
                 'alternativas': ['Fermentación exclusiva',
                                  'Solo respiración anaerobia',
                                  'Quimiosíntesis exclusivamente',
                                  'Fotosíntesis oxigénica',
                                  'Ninguna función metabólica'],
                 'correcta': 'D'},
                {'pregunta': 'El único organelo presente en las células '
                             'procariotas son:',
                 'alternativas': ['Los cloroplastos',
                                  'Los lisosomas',
                                  'Los ribosomas',
                                  'El aparato de Golgi',
                                  'Las mitocondrias'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia del ADN eucariota, el ADN '
                             'procariota no está asociado a:',
                 'alternativas': ['Fosfolípidos',
                                  'Histonas',
                                  'Proteínas de membrana',
                                  'Enzimas',
                                  'Ribosomas'],
                 'correcta': 'B'},
                {'pregunta': 'Las formas típicas de las bacterias, '
                             'mantenidas por la pared celular, son cocos, '
                             'espirilos y:',
                 'alternativas': ['Filamentos exclusivos',
                                  'Esferas',
                                  'Bacilos',
                                  'Discos',
                                  'Tubos'],
                 'correcta': 'C'},
                {'pregunta': 'Los micoplasmas, también llamados Mollicutes o '
                             'PPLO, se caracterizan por ser:',
                 'alternativas': ['Bacterias exclusivamente marinas',
                                  'Bacterias fotosintéticas',
                                  'Bacterias con pared muy gruesa',
                                  'Las bacterias más pequeñas conocidas',
                                  'Las bacterias más grandes conocidas'],
                 'correcta': 'D'},
                {'pregunta': 'Los micoplasmas varían su forma según las '
                             'condiciones del medio; esta propiedad se '
                             'llama:',
                 'alternativas': ['Isomorfismo',
                                  'Polimorfismo genético',
                                  'Pleomorfismo',
                                  'Heteromorfismo',
                                  'Metamorfismo'],
                 'correcta': 'C'},
                {'pregunta': 'Los micoplasmas son los únicos procariotas '
                             'conocidos que carecen de:',
                 'alternativas': ['Enzimas',
                                  'Ribosomas',
                                  'Pared celular',
                                  'Membrana plasmática',
                                  'ADN'],
                 'correcta': 'C'},
                {'pregunta': 'La membrana plasmática de los micoplasmas '
                             'contiene fosfolípidos y un esterol llamado:',
                 'alternativas': ['Colesterol',
                                  'Testosterona',
                                  'Progesterona',
                                  'Ergosterol',
                                  'Estradiol'],
                 'correcta': 'A'},
                {'pregunta': 'La especie de micoplasma causante de la '
                             'neumonía atípica en humanos es:',
                 'alternativas': ['Mycoplasma hominis',
                                  'Mycoplasma pneumoniae',
                                  'Mycoplasma bovis',
                                  'Mycoplasma mycoides',
                                  'Mycoplasma genitalium'],
                 'correcta': 'B'},
                {'pregunta': 'Las cianobacterias son consideradas las '
                             'bacterias más evolucionadas de tipo:',
                 'alternativas': ['Parasitario',
                                  'Fotosintético',
                                  'Saprófito',
                                  'Heterótrofo',
                                  'Quimiosintético'],
                 'correcta': 'B'},
                {'pregunta': 'La pared celular de las cianobacterias es '
                             'semejante a la de las bacterias:',
                 'alternativas': ['Micoplasmas',
                                  'Sin pared',
                                  'Arqueas',
                                  'Gram negativas',
                                  'Gram positivas'],
                 'correcta': 'D'},
                {'pregunta': 'Además de la clorofila, las cianobacterias '
                             'contienen pigmentos llamados ficobilinas, '
                             'entre ellos la ficocianina, de color:',
                 'alternativas': ['Amarillo',
                                  'Azul',
                                  'Verde',
                                  'Rojo',
                                  'Café'],
                 'correcta': 'B'},
                {'pregunta': 'Las cianobacterias pueden fijar nitrógeno (N2) '
                             'y convertirlo en:',
                 'alternativas': ['Urea',
                                  'Amoniaco',
                                  'Nitratos directamente',
                                  'Nitrógeno líquido',
                                  'Óxido nitroso'],
                 'correcta': 'B'},
                {'pregunta': 'El género de cianobacteria comestible, '
                             'conocido en los Andes como «llullucha» o '
                             '«murmunta», es:',
                 'alternativas': ['Nostoc',
                                  'Anabaena',
                                  'Oscillatoria',
                                  'Spirulina',
                                  'Chlorella'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'GENERALIDADES Y ORIGEN DEL TÉRMINO',
                      'items': ['La palabra «célula» proviene del latín '
                                '«cella», que significa «pequeña habitación '
                                'o celda».']},
                     {'titulo': 'LA TEORÍA CELULAR',
                      'items': ['Los fundadores de la teoría celular fueron '
                                'Mathias Schleiden (1838) y Theodor Schwann '
                                '(1839).']},
                     {'titulo': 'CÉLULA PROCARIOTA Y EUCARIOTA',
                      'items': ['«Procariota» proviene del griego «protos» '
                                '(primitivo) y «karyon» (núcleo).']},
                     {'titulo': 'ESTRUCTURA BACTERIANA',
                      'items': ['La cápsula es una estructura de '
                                'polisacáridos que forma un glucocálix '
                                'grueso y rígido, con función de '
                                'adherencia.']},
                     {'titulo': 'MICOPLASMAS',
                      'items': ['Los micoplasmas, también llamados '
                                'Mollicutes o PPLO, son las bacterias más '
                                'pequeñas conocidas, con diámetro de 0,125 a '
                                '0,150 µm.']},
                     {'titulo': 'CIANOBACTERIAS',
                      'items': ['Las cianobacterias, o algas verde-azules, '
                                'son las bacterias fotosintéticas más '
                                'evolucionadas.']}]},
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
                {'titulo': '6.5 FUNCIONES DE LA MEMBRANA CELULAR',
                 'items': ['La {compartimentalización} separa los medios '
                           'intracelular y {extracelular}.',
                           'La {permeabilidad selectiva} determina la '
                           'diferencia de concentración de electrolitos '
                           'entre ambos medios.',
                           'La membrana presenta {receptores} específicos '
                           'para moléculas llamadas {ligandos}, ubicados en '
                           'su superficie externa.',
                           'La membrana media la {interacción intercelular} '
                           'y permite a las células {reconocerse} entre sí.',
                           'En la {transducción de energía}, los pigmentos '
                           'de membrana absorben luz solar durante la '
                           '{fotosíntesis} y la convierten en energía '
                           'química.']},
                {'titulo': '6.6 TRANSPORTE PASIVO',
                 'items': ['El {transporte pasivo}, o difusión pasiva, '
                           'ocurre en forma espontánea, {sin gasto} de '
                           'energía, a favor del gradiente de concentración.',
                           'La {difusión simple} a través de la bicapa '
                           'permite el paso de moléculas lipídicas, como '
                           'hormonas {esteroideas} y vitaminas A, D, E, K.',
                           'La {ósmosis} es el paso de agua desde una región '
                           'de baja concentración de soluto hacia otra de '
                           '{alta} concentración.',
                           'La {difusión simple} a través de canales permite '
                           'el paso de iones como Na+, K+, Ca2+, mediante '
                           '{proteínas} de canal.',
                           'La {difusión facilitada} permite el transporte '
                           'de moléculas polares, como aminoácidos, mediante '
                           'proteínas transportadoras o {permeasas}.']},
                {'titulo': '6.7 TRANSPORTE ACTIVO',
                 'items': ['El {transporte activo} requiere gasto de energía '
                           'en forma de {ATP}, mediante la enzima {ATPasa}.',
                           'El {transporte por bombas} mueve electrolitos en '
                           'contra de su gradiente; la más conocida es la '
                           'bomba de {Na/K}.',
                           'La bomba de Na+/K+ bombea {3} iones sodio hacia '
                           'el exterior y {2} iones potasio hacia el '
                           'interior, por cada ATP hidrolizado.',
                           'Las células nerviosas gastan más del {70}% del '
                           'ATP que producen para bombear estos iones.',
                           'El {transporte en masa} se realiza mediante '
                           'formación de {vesículas}, para sustancias de '
                           'mayor tamaño.',
                           'La {endocitosis} incorpora partículas del medio '
                           'extracelular; puede ser {fagocitosis} '
                           '(partículas sólidas) o pinocitosis (partículas '
                           'líquidas).',
                           'La {fagocitosis} es realizada por células '
                           'especializadas: leucocitos, amebas y '
                           '{macrófagos}.',
                           'La {exocitosis} es la secreción celular de '
                           'productos elaborados por la célula, mediante '
                           'vesículas que se fusionan con la {membrana}.']},
                {'titulo': '6.8 EL CITOPLASMA',
                 'items': ['El {citoplasma}, o hialoplasma, es el mayor '
                           'compartimento de la célula, entre la membrana '
                           'plasmática y la {nuclear}.',
                           'El {citosol} es el fluido acuoso del citoplasma, '
                           'donde ocurren reacciones como los primeros pasos '
                           'de la {glucólisis}.',
                           'El {citoesqueleto} es la red de soporte formada '
                           'por microfilamentos, microtúbulos y filamentos '
                           '{intermedios}.',
                           'Los {microfilamentos} de actina son las '
                           'estructuras más delgadas del citoesqueleto, con '
                           '7 nm de diámetro.',
                           'Los {microtúbulos} de tubulina son las '
                           'estructuras más rígidas, con 25 nm de diámetro, '
                           'formando cilios y flagelos.',
                           'Los {filamentos intermedios} son los más '
                           'elásticos y resistentes, formados por queratinas '
                           'y vimentinas.',
                           'Los {centriolos} son un par de estructuras '
                           'cilíndricas formadas por 9 tripletes de '
                           'microtúbulos, cerca del núcleo.']},
                {'titulo': '6.9 CILIOS Y FLAGELOS',
                 'items': ['Los {cilios} y flagelos son proyecciones móviles '
                           'formadas por microtúbulos y proteínas accesorias '
                           'como la {dineína} y nexina.',
                           'Los {cilios} son cortos y numerosos, con '
                           'movimiento como un remo; los {flagelos} son '
                           'pocos, largos, con movimiento ondulatorio.',
                           'Ambos tienen una disposición «{9+2}»: nueve '
                           'pares de microtúbulos rodeando a un par central.',
                           'Están formados por tres partes: el {axonema} '
                           '(eje), la zona de transición, y el {corpúsculo '
                           'basal}.',
                           'Los cilios producen el desplazamiento de '
                           'organismos unicelulares y evitan el paso de '
                           'partículas en la cavidad {nasal}.',
                           'Los flagelos producen el desplazamiento de '
                           'células como el {espermatozoide}.']},
                {'titulo': '6.10 RIBOSOMAS Y RETÍCULO ENDOPLASMÁTICO',
                 'items': ['Los {ribosomas} tienen dos subunidades '
                           'compuestas por ARNr, y se elaboran en el '
                           '{nucléolo}.',
                           'Los ribosomas agrupados en el citosol forman '
                           '{polisomas} o polirribosomas.',
                           'El {retículo endoplasmático rugoso} (RER) está '
                           'conectado a la membrana nuclear y cubierto de '
                           '{ribosomas}.',
                           'El {retículo endoplasmático liso} (REL) carece '
                           'de ribosomas y sintetiza {lípidos} y esteroides.',
                           'El RER sintetiza proteínas de la {matriz '
                           'extracelular} y enzimas lisosomales.']},
                {'titulo': '6.11 COMPLEJO DE GOLGI Y LISOSOMAS',
                 'items': ['El {complejo de Golgi} es un grupo de sacos '
                           'aplanados llamados {dictiosomas}.',
                           'El complejo de Golgi tiene tres regiones: {cis} '
                           'o de formación, medial, y {trans} o de '
                           'maduración.',
                           'El complejo de Golgi empaca proteínas, lípidos y '
                           '{carbohidratos}, dirigiéndolos a su destino '
                           'celular.',
                           'Los {lisosomas} son vesículas con enzimas '
                           'digestivas que funcionan a pH {ácido}.',
                           'Los lisosomas {primarios} se separan del Golgi '
                           'por gemación; los {secundarios} se fusionan con '
                           'vesículas fagocíticas.',
                           'Los lisosomas participan en la {apoptosis} o '
                           'muerte celular programada.']},
                {'titulo': '6.12 PEROXISOMAS',
                 'items': ['Los {peroxisomas} son similares a los lisosomas, '
                           'pero contienen enzimas distintas: {peroxidasas} '
                           'y catalasas.',
                           'Las {peroxidasas} producen peróxido de '
                           'hidrógeno; las {catalasas} lo desdoblan en agua '
                           'y oxígeno.',
                           'Los peroxisomas realizan reacciones oxidativas '
                           'de ácidos grasos y aminoácidos, y reacciones de '
                           '{detoxificación}.',
                           'Su actividad es relevante en células del '
                           '{hígado} y riñón; oxidan la mitad del alcohol '
                           'etílico ingerido.',
                           'Los peroxisomas también participan en la '
                           '{biogénesis} de lípidos, como el colesterol y '
                           'los plasmalógenos.']},
                {'titulo': '6.13 GLIOXISOMAS',
                 'items': ['Los {glioxisomas} son un tipo especial de '
                           'peroxisomas exclusivos de {células vegetales}.',
                           'Contienen enzimas del ciclo del {glioxilato}, '
                           'que convierten lípidos en azúcares durante la '
                           'germinación de semillas.',
                           'Se encuentran en los {cotiledones} o endospermo '
                           'de las semillas en germinación.']},
                {'titulo': '6.14 VACUOLAS',
                 'items': ['Las {vacuolas} son sacos membranosos que se '
                           'forman del retículo endoplásmico, el Golgi, o '
                           'invaginaciones de la {membrana}.',
                           'En protistas como euglenas y paramecios, las '
                           'vacuolas eliminan el exceso de {agua}.',
                           'Las vacuolas actúan como almacén de agua, sales, '
                           'azúcares, y {desechos} celulares.']},
                {'titulo': '6.15 MITOCONDRIAS',
                 'items': ['Las {mitocondrias} se encuentran en todas las '
                           'células eucariotas, con doble {membrana} '
                           '(interna y externa).',
                           'La membrana {interna} se pliega formando las '
                           '{crestas} mitocondriales.',
                           'La {matriz mitocondrial} es el espacio central, '
                           'rico en enzimas para la {respiración} celular.',
                           'Las mitocondrias producen {ATP} a partir de la '
                           'oxidación de la glucosa, en el proceso llamado '
                           '{respiración celular}.']},
                {'titulo': '6.16 PLASTOS Y CLOROPLASTOS',
                 'items': ['Los {plastos} son orgánulos elípticos de las '
                           'células vegetales, similares a las mitocondrias.',
                           'Los {leucoplastos} tienen escasa pigmentación y '
                           'almacenan almidón, lípidos o proteínas.',
                           'Los {cromoplastos} tienen pigmentos '
                           'carotenoideos, causantes del color amarillo o '
                           'rojo.',
                           'Los {cloroplastos} tienen pigmento verde y '
                           'realizan la {fotosíntesis}.',
                           'Los cloroplastos presentan tres membranas: '
                           'externa, interna y {tilacoidal}.',
                           'La membrana tilacoidal forma discos llamados '
                           '{tilacoides}, que en conjunto forman la '
                           '{grana}.']},
                {'titulo': '6.17 EL NÚCLEO',
                 'items': ['El núcleo está ausente en los glóbulos rojos '
                           '{maduros} de los mamíferos.',
                           'El núcleo es considerado el «{cerebro}» de la '
                           'célula porque dirige todas las actividades '
                           'celulares.',
                           'La envoltura nuclear tiene doble membrana, con '
                           'aberturas llamadas {poros} nucleares.',
                           'El {nucleoplasma} es la parte interna del '
                           'núcleo, donde se encuentra el {nucléolo}.']},
                {'titulo': '6.18 CROMATINA Y NUCLÉOLO',
                 'items': ['La {cromatina} está constituida por ADN, '
                           'histonas y proteínas no histónicas.',
                           'La {eucromatina} es cromatina poco condensada; '
                           'la {heterocromatina} es cromatina muy '
                           'condensada.',
                           'La heterocromatina {facultativa} a veces está '
                           'condensada; la {constitutiva} siempre está '
                           'condensada.',
                           'El {nucléolo} sintetiza casi todo el ARN de la '
                           'célula, incluido el {ARNr}.']},
                {'titulo': '6.19 CROMOSOMAS',
                 'items': ['Los {cromosomas} resultan del empaquetamiento '
                           'máximo del ADN nuclear con proteínas.',
                           'Las células con dos juegos completos de '
                           'cromosomas se llaman {diploides} o 2n.',
                           'El ser humano tiene {46} cromosomas (2n), en '
                           '{23} pares.',
                           'De los 23 pares humanos, {22} son autosomas y 1 '
                           'par son los cromosomas {sexuales} (X, Y).',
                           'Las mujeres son el sexo {homogamético} (XX); los '
                           'varones, el {heterogamético} (XY).',
                           'El {centrómero} es el centro cinético del '
                           'cromosoma, esencial para la segregación durante '
                           'la {mitosis}.']}],
  'cuadros': [{'titulo': '6.3 COMPOSICIÓN DE LA MEMBRANA CELULAR',
               'encabezados': ['Componente', 'Proporción aproximada'],
               'filas': [['{Lípidos}', '{40}%'],
                         ['{Proteínas}', '{52}%'],
                         ['{Glúcidos}', '8%']]}],
  'preguntas': [{'pregunta': 'En la célula eucariota, el ADN se encuentra '
                             'encerrado dentro de:',
                 'alternativas': ['El citoplasma libre',
                                  'Una sola membrana',
                                  'El nucleoide',
                                  'La pared celular',
                                  'Una doble membrana o envoltura nuclear'],
                 'correcta': 'E'},
                {'pregunta': 'Las tres partes principales de la célula '
                             'eucariota son membrana, citoplasma y:',
                 'alternativas': ['Pared celular',
                                  'Glicocálix',
                                  'Ribosoma',
                                  'Nucleoide',
                                  'Núcleo'],
                 'correcta': 'E'},
                {'pregunta': 'El ADN asociado a histonas recibe el nombre '
                             'de:',
                 'alternativas': ['Citosol',
                                  'Nucleoide',
                                  'Cromatina',
                                  'Glicocálix',
                                  'Matriz'],
                 'correcta': 'C'},
                {'pregunta': 'Las células eucariotas, en comparación con las '
                             'procariotas, son:',
                 'alternativas': ['Más pequeñas',
                                  'Sin núcleo definido',
                                  'Mucho más grandes',
                                  'Sin membrana',
                                  'Del mismo tamaño'],
                 'correcta': 'C'},
                {'pregunta': 'La pared celular está presente en:',
                 'alternativas': ['Células animales exclusivamente',
                                  'Solo células humanas',
                                  'Solo bacterias',
                                  'Células vegetales y hongos',
                                  'Todas las células sin excepción'],
                 'correcta': 'D'},
                {'pregunta': 'El principal componente estructural de la '
                             'pared celular vegetal es:',
                 'alternativas': ['El colesterol',
                                  'La celulosa',
                                  'El glucógeno',
                                  'La quitina',
                                  'La queratina'],
                 'correcta': 'B'},
                {'pregunta': 'Los puentes intercelulares entre células '
                             'vegetales adyacentes se llaman:',
                 'alternativas': ['Uniones estrechas',
                                  'Gap junctions exclusivas',
                                  'Plasmodesmos',
                                  'Desmosomas',
                                  'Sinapsis'],
                 'correcta': 'C'},
                {'pregunta': 'El componente de la pared celular de los '
                             'hongos es:',
                 'alternativas': ['El colesterol',
                                  'La quitina',
                                  'La celulosa',
                                  'La queratina',
                                  'La lignina exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El glicocálix caracteriza a las células:',
                 'alternativas': ['Procariotas en general',
                                  'Bacterianas',
                                  'Fúngicas',
                                  'Animales',
                                  'Vegetales'],
                 'correcta': 'D'},
                {'pregunta': 'El glicocálix participa principalmente en:',
                 'alternativas': ['El reconocimiento celular',
                                  'La síntesis de proteínas',
                                  'La replicación del ADN',
                                  'La fotosíntesis',
                                  'La respiración celular'],
                 'correcta': 'A'},
                {'pregunta': 'La membrana plasmática es de naturaleza:',
                 'alternativas': ['Celulósica',
                                  'Lipoproteica',
                                  'Puramente proteica',
                                  'Puramente lipídica',
                                  'Mineral'],
                 'correcta': 'B'},
                {'pregunta': 'El modelo de estructura de la membrana celular '
                             'se denomina modelo de:',
                 'alternativas': ['Red cristalina',
                                  'Mosaico fluido',
                                  'Esfera sólida',
                                  'Capa rígida',
                                  'Doble hélice'],
                 'correcta': 'B'},
                {'pregunta': 'El modelo de mosaico fluido fue propuesto por:',
                 'alternativas': ['Mendel y Darwin',
                                  'Watson y Crick',
                                  'Singer y Nicholson',
                                  'Hooke y Virchow',
                                  'Schleiden y Schwann'],
                 'correcta': 'C'},
                {'pregunta': 'En la composición de la membrana, los lípidos '
                             'representan aproximadamente:',
                 'alternativas': ['90%', '40%', '100%', '8%', '52%'],
                 'correcta': 'B'},
                {'pregunta': 'En la composición de la membrana, las '
                             'proteínas representan aproximadamente:',
                 'alternativas': ['52%', '0%', '40%', '10%', '8%'],
                 'correcta': 'A'},
                {'pregunta': 'Los componentes lipídicos más abundantes de la '
                             'membrana son los:',
                 'alternativas': ['Carotenoides',
                                  'Fosfolípidos',
                                  'Glicolípidos',
                                  'Esteroides',
                                  'Triglicéridos'],
                 'correcta': 'B'},
                {'pregunta': 'El colesterol de la membrana celular es '
                             'responsable, entre otras cosas, de:',
                 'alternativas': ['La rigidez total',
                                  'El transporte activo exclusivo',
                                  'La fluidez de la membrana',
                                  'La síntesis de proteínas',
                                  'La replicación del ADN'],
                 'correcta': 'C'},
                {'pregunta': 'Las proteínas que se localizan en las '
                             'superficies de la membrana y son solubles en '
                             'agua se llaman:',
                 'alternativas': ['Enzimáticas exclusivas',
                                  'Transmembrana',
                                  'Periféricas o extrínsecas',
                                  'Integrales',
                                  'Glicoproteicas exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'Las proteínas que atraviesan todo el espesor '
                             'de la membrana se llaman proteínas:',
                 'alternativas': ['Extrínsecas',
                                  'Periféricas',
                                  'Solubles en agua',
                                  'Integrales o intrínsecas',
                                  'Superficiales'],
                 'correcta': 'D'},
                {'pregunta': 'Los carbohidratos de la membrana se encuentran '
                             'únicamente en:',
                 'alternativas': ['El núcleo',
                                  'La matriz mitocondrial',
                                  'La superficie de la monocapa externa',
                                  'El citoplasma',
                                  'La monocapa interna'],
                 'correcta': 'C'},
                {'pregunta': 'El citoplasma corresponde a la región entre la '
                             'membrana plasmática y:',
                 'alternativas': ['El citoesqueleto exclusivo',
                                  'El nucléolo',
                                  'La membrana nuclear',
                                  'La pared celular',
                                  'Los ribosomas'],
                 'correcta': 'C'},
                {'pregunta': 'En el citosol se producen los primeros pasos '
                             'de la degradación de nutrientes, como:',
                 'alternativas': ['La transcripción',
                                  'La glucólisis',
                                  'La fotosíntesis',
                                  'La replicación del ADN',
                                  'La traducción'],
                 'correcta': 'B'},
                {'pregunta': 'El citoesqueleto está formado por '
                             'microfilamentos, microtúbulos y:',
                 'alternativas': ['Ribosomas',
                                  'Lisosomas',
                                  'Filamentos intermedios',
                                  'Mitocondrias',
                                  'Cloroplastos'],
                 'correcta': 'C'},
                {'pregunta': 'Los microfilamentos de actina tienen un '
                             'diámetro aproximado de:',
                 'alternativas': ['1 nm', '25 nm', '7 nm', '50 nm', '100 nm'],
                 'correcta': 'C'},
                {'pregunta': 'Los microtúbulos de tubulina forman, entre '
                             'otras estructuras:',
                 'alternativas': ['El citosol',
                                  'El nucléolo',
                                  'Los cilios y flagelos',
                                  'La pared celular',
                                  'La cromatina'],
                 'correcta': 'C'},
                {'pregunta': 'Los centriolos están formados por nueve '
                             'tripletes de:',
                 'alternativas': ['Microtúbulos',
                                  'Filamentos intermedios',
                                  'Ribosomas',
                                  'Actina',
                                  'Queratina'],
                 'correcta': 'A'},
                {'pregunta': 'Los ribosomas se elaboran en:',
                 'alternativas': ['Los lisosomas',
                                  'El nucléolo',
                                  'El citosol exclusivamente',
                                  'La mitocondria',
                                  'El aparato de Golgi'],
                 'correcta': 'B'},
                {'pregunta': 'Los ribosomas agrupados en el citosol forman '
                             'estructuras llamadas:',
                 'alternativas': ['Dictiosomas',
                                  'Polisomas o polirribosomas',
                                  'Tilacoides',
                                  'Crestas',
                                  'Cisternas'],
                 'correcta': 'B'},
                {'pregunta': 'El retículo endoplasmático rugoso se '
                             'caracteriza por estar cubierto de:',
                 'alternativas': ['Centriolos',
                                  'Ribosomas',
                                  'Lisosomas',
                                  'Cloroplastos',
                                  'Mitocondrias'],
                 'correcta': 'B'},
                {'pregunta': 'El retículo endoplasmático liso se especializa '
                             'en la síntesis de:',
                 'alternativas': ['Lípidos',
                                  'Ácidos nucleicos',
                                  'Proteínas',
                                  'Carbohidratos exclusivamente',
                                  'ARN ribosómico'],
                 'correcta': 'A'},
                {'pregunta': 'El complejo de Golgi está formado por sacos '
                             'apilados llamados:',
                 'alternativas': ['Tilacoides',
                                  'Polisomas',
                                  'Crestas',
                                  'Cisternas nucleares',
                                  'Dictiosomas'],
                 'correcta': 'E'},
                {'pregunta': 'La cara del complejo de Golgi más próxima al '
                             'retículo endoplasmático se llama cara:',
                 'alternativas': ['Lateral',
                                  'Trans',
                                  'Externa',
                                  'Cis',
                                  'Medial exclusiva'],
                 'correcta': 'D'},
                {'pregunta': 'Los lisosomas contienen enzimas digestivas que '
                             'funcionan en un ambiente:',
                 'alternativas': ['Ácido',
                                  'Sin pH definido',
                                  'Alcalino',
                                  'Básico',
                                  'Neutro'],
                 'correcta': 'A'},
                {'pregunta': 'Los lisosomas que se separan del Golgi por '
                             'gemación se llaman lisosomas:',
                 'alternativas': ['Primarios',
                                  'Nucleares',
                                  'Autofágicos exclusivos',
                                  'Terciarios',
                                  'Secundarios'],
                 'correcta': 'A'},
                {'pregunta': 'Las mitocondrias se encuentran en todas las '
                             'células eucariotas y tienen:',
                 'alternativas': ['Una sola membrana',
                                  'Ninguna membrana',
                                  'Membrana tilacoidal exclusiva',
                                  'Doble membrana',
                                  'Pared celular'],
                 'correcta': 'D'},
                {'pregunta': 'Los pliegues de la membrana mitocondrial '
                             'interna se llaman:',
                 'alternativas': ['Tilacoides',
                                  'Cisternas',
                                  'Crestas mitocondriales',
                                  'Dictiosomas',
                                  'Granas'],
                 'correcta': 'C'},
                {'pregunta': 'Las mitocondrias producen ATP mediante el '
                             'proceso de:',
                 'alternativas': ['Traducción',
                                  'Replicación',
                                  'Transcripción',
                                  'Respiración celular',
                                  'Fotosíntesis'],
                 'correcta': 'D'},
                {'pregunta': 'Los plastos con pigmento verde que realizan la '
                             'fotosíntesis se llaman:',
                 'alternativas': ['Amiloplastos',
                                  'Etioplastos',
                                  'Cromoplastos',
                                  'Leucoplastos',
                                  'Cloroplastos'],
                 'correcta': 'E'},
                {'pregunta': 'Los plastos que almacenan almidón, lípidos o '
                             'proteínas, con escasa pigmentación, se llaman:',
                 'alternativas': ['Cromoplastos',
                                  'Leucoplastos',
                                  'Cloroplastos',
                                  'Tilacoides',
                                  'Etioplastos'],
                 'correcta': 'B'},
                {'pregunta': 'La membrana del cloroplasto que forma discos '
                             'aplanados llamados tilacoides es la membrana:',
                 'alternativas': ['Interna exclusiva',
                                  'Tilacoidal',
                                  'Plasmática',
                                  'Externa',
                                  'Nuclear'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo está ausente en un tipo de célula '
                             'humana madura, que es:',
                 'alternativas': ['El glóbulo rojo',
                                  'El hepatocito',
                                  'La neurona',
                                  'El linfocito',
                                  'La célula muscular'],
                 'correcta': 'A'},
                {'pregunta': 'El núcleo es considerado el «cerebro» de la '
                             'célula porque:',
                 'alternativas': ['Solo almacena lípidos',
                                  'Solo forma parte del citoesqueleto',
                                  'No tiene función específica',
                                  'Dirige todas las actividades celulares',
                                  'Produce energía'],
                 'correcta': 'D'},
                {'pregunta': 'Las aberturas de la envoltura nuclear se '
                             'llaman:',
                 'alternativas': ['Poros nucleares',
                                  'Cisternas',
                                  'Crestas',
                                  'Tilacoides',
                                  'Dictiosomas'],
                 'correcta': 'A'},
                {'pregunta': 'La cromatina poco condensada se llama:',
                 'alternativas': ['Heterocromatina',
                                  'Nucleoplasma',
                                  'Cariotipo',
                                  'Eucromatina',
                                  'Centrómero'],
                 'correcta': 'D'},
                {'pregunta': 'La cromatina muy condensada se llama:',
                 'alternativas': ['Heterocromatina',
                                  'Nucleoplasma',
                                  'Eucromatina',
                                  'Nucléolo',
                                  'Cariotipo'],
                 'correcta': 'A'},
                {'pregunta': 'El nucléolo sintetiza casi todo el ARN de la '
                             'célula, en especial el:',
                 'alternativas': ['ADN mitocondrial',
                                  'ARN mensajero exclusivo',
                                  'ARN ribosómico (ARNr)',
                                  'ARN de transferencia exclusivo',
                                  'ADN nuclear'],
                 'correcta': 'C'},
                {'pregunta': 'Las células con dos juegos completos de '
                             'cromosomas se llaman células:',
                 'alternativas': ['Haploides',
                                  'Monoploides',
                                  'Poliploides exclusivas',
                                  'Triploides',
                                  'Diploides'],
                 'correcta': 'E'},
                {'pregunta': 'El número de cromosomas del ser humano (2n) '
                             'es:',
                 'alternativas': ['48', '22', '44', '46', '23'],
                 'correcta': 'D'},
                {'pregunta': 'De los 23 pares de cromosomas humanos, el '
                             'número de pares de autosomas es:',
                 'alternativas': ['46', '23', '22', '24', '1'],
                 'correcta': 'C'},
                {'pregunta': 'El centro cinético del cromosoma, esencial '
                             'para la segregación en la mitosis, se llama:',
                 'alternativas': ['Cinetocoro exclusivo',
                                  'Nucléolo',
                                  'Centrómero',
                                  'Satélite',
                                  'Telómero'],
                 'correcta': 'C'},
                {'pregunta': 'La función de la membrana celular que separa '
                             'los medios intracelular y extracelular se '
                             'llama:',
                 'alternativas': ['Permeabilidad selectiva',
                                  'Transporte activo',
                                  'Compartimentalización',
                                  'Interacción intercelular',
                                  'Transducción de energía'],
                 'correcta': 'C'},
                {'pregunta': 'Los receptores de membrana se unen a moléculas '
                             'específicas llamadas:',
                 'alternativas': ['Enzimas',
                                  'Bombas',
                                  'Permeasas',
                                  'Canales',
                                  'Ligandos'],
                 'correcta': 'E'},
                {'pregunta': 'Durante la fotosíntesis, los pigmentos de '
                             'membrana absorben luz solar y la convierten en '
                             'energía química, ejemplificando la función de:',
                 'alternativas': ['Respuesta a señales exclusiva',
                                  'Transducción de energía',
                                  'Interacción intercelular',
                                  'Permeabilidad selectiva',
                                  'Compartimentalización'],
                 'correcta': 'B'},
                {'pregunta': 'El transporte pasivo, o difusión pasiva, '
                             'ocurre en forma espontánea y:',
                 'alternativas': ['Mediante ATP exclusivamente',
                                  'Solo contra el gradiente',
                                  'Sin gasto de energía',
                                  'Con gran gasto de energía',
                                  'Solo en células vivas'],
                 'correcta': 'C'},
                {'pregunta': 'Las hormonas esteroideas y las vitaminas '
                             'liposolubles atraviesan la membrana mediante:',
                 'alternativas': ['Endocitosis',
                                  'Difusión simple a través de la bicapa',
                                  'Transporte activo',
                                  'Fagocitosis',
                                  'Bombas de sodio-potasio'],
                 'correcta': 'B'},
                {'pregunta': 'El paso de agua desde una región de baja '
                             'concentración de soluto hacia otra de alta '
                             'concentración se llama:',
                 'alternativas': ['Difusión facilitada',
                                  'Pinocitosis',
                                  'Exocitosis',
                                  'Ósmosis',
                                  'Fagocitosis'],
                 'correcta': 'D'},
                {'pregunta': 'Los iones como sodio, potasio y calcio '
                             'atraviesan la membrana mediante difusión '
                             'simple a través de:',
                 'alternativas': ['Fagocitosis',
                                  'Canales proteicos',
                                  'La bicapa lipídica directamente',
                                  'Bombas de ATP',
                                  'Vesículas'],
                 'correcta': 'B'},
                {'pregunta': 'Las proteínas que permiten la difusión '
                             'facilitada de moléculas polares como '
                             'aminoácidos se llaman:',
                 'alternativas': ['Permeasas o proteínas transportadoras',
                                  'Bombas de calcio',
                                  'Canales iónicos',
                                  'Enzimas digestivas',
                                  'Receptores'],
                 'correcta': 'A'},
                {'pregunta': 'El transporte activo requiere gasto de energía '
                             'en forma de ATP, catalizado por la enzima:',
                 'alternativas': ['Lipasa',
                                  'Catalasa',
                                  'Proteasa',
                                  'Amilasa',
                                  'ATPasa'],
                 'correcta': 'E'},
                {'pregunta': 'La bomba más conocida del transporte activo '
                             'por medio de bombas es la bomba de:',
                 'alternativas': ['Sodio-potasio',
                                  'Cloro-bicarbonato',
                                  'Hidrógeno-fosfato',
                                  'Calcio-magnesio',
                                  'Hierro-cobre'],
                 'correcta': 'A'},
                {'pregunta': 'Por cada ATP hidrolizado, la bomba de Na+/K+ '
                             'bombea hacia el exterior un número de iones '
                             'sodio igual a:',
                 'alternativas': ['2', '1', '3', '4', '5'],
                 'correcta': 'C'},
                {'pregunta': 'Las células nerviosas gastan más de este '
                             'porcentaje del ATP que producen para bombear '
                             'iones sodio y potasio:',
                 'alternativas': ['90%', '10%', '30%', '70%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'El transporte en masa, mediante formación de '
                             'vesículas, se realiza para sustancias que por '
                             'su tamaño no pueden atravesar:',
                 'alternativas': ['El citoesqueleto',
                                  'El núcleo',
                                  'El citosol',
                                  'La membrana directamente',
                                  'Los ribosomas'],
                 'correcta': 'D'},
                {'pregunta': 'La incorporación de partículas del medio '
                             'extracelular, rodeadas de membrana, se llama:',
                 'alternativas': ['Endocitosis',
                                  'Transporte activo',
                                  'Difusión simple',
                                  'Exocitosis',
                                  'Ósmosis'],
                 'correcta': 'A'},
                {'pregunta': 'La captación de partículas sólidas, como '
                             'bacterias, mediante la formación de un '
                             'fagosoma, se llama:',
                 'alternativas': ['Difusión facilitada',
                                  'Ósmosis',
                                  'Exocitosis',
                                  'Fagocitosis',
                                  'Pinocitosis'],
                 'correcta': 'D'},
                {'pregunta': 'Las células especializadas en realizar '
                             'fagocitosis incluyen a los leucocitos, las '
                             'amebas y:',
                 'alternativas': ['Las plaquetas',
                                  'Los eritrocitos',
                                  'Los adipocitos',
                                  'Los linfocitos exclusivos',
                                  'Los macrófagos'],
                 'correcta': 'E'},
                {'pregunta': 'La incorporación de partículas líquidas '
                             'mediante una vesícula pinocítica se llama:',
                 'alternativas': ['Exocitosis',
                                  'Difusión simple',
                                  'Pinocitosis',
                                  'Fagocitosis',
                                  'Ósmosis'],
                 'correcta': 'C'},
                {'pregunta': 'La secreción celular de productos elaborados '
                             'por la célula, mediante vesículas que se '
                             'fusionan con la membrana, se llama:',
                 'alternativas': ['Pinocitosis',
                                  'Fagocitosis',
                                  'Exocitosis',
                                  'Endocitosis',
                                  'Difusión facilitada'],
                 'correcta': 'C'},
                {'pregunta': 'Los cilios y flagelos están formados por '
                             'microtúbulos y proteínas accesorias como la '
                             'nexina y:',
                 'alternativas': ['La miosina',
                                  'La queratina',
                                  'La actina',
                                  'La dineína',
                                  'La tubulina exclusiva'],
                 'correcta': 'D'},
                {'pregunta': 'A diferencia de los flagelos, los cilios son:',
                 'alternativas': ['Cortos y numerosos',
                                  'Inmóviles',
                                  'Exclusivos de plantas',
                                  'De movimiento ondulatorio',
                                  'Largos y escasos'],
                 'correcta': 'A'},
                {'pregunta': 'La disposición característica de microtúbulos '
                             'en cilios y flagelos se describe como:',
                 'alternativas': ['6+3', '8+4', '7+1', '9+2', '11+0'],
                 'correcta': 'D'},
                {'pregunta': 'Las tres partes que forman un cilio o flagelo '
                             'son el axonema, la zona de transición y:',
                 'alternativas': ['El nucléolo',
                                  'El retículo',
                                  'El corpúsculo basal',
                                  'La membrana externa exclusiva',
                                  'El citosol'],
                 'correcta': 'C'},
                {'pregunta': 'Los flagelos producen el desplazamiento de '
                             'células como:',
                 'alternativas': ['Los glóbulos rojos',
                                  'El espermatozoide',
                                  'Las plaquetas',
                                  'Los linfocitos',
                                  'Los adipocitos'],
                 'correcta': 'B'},
                {'pregunta': 'Los peroxisomas se diferencian de los '
                             'lisosomas principalmente por el tipo de:',
                 'alternativas': ['Tamaño exclusivo',
                                  'Origen celular',
                                  'Forma exclusiva',
                                  'Membrana que poseen',
                                  'Enzimas que contienen'],
                 'correcta': 'E'},
                {'pregunta': 'Las enzimas de los peroxisomas que producen '
                             'peróxido de hidrógeno se llaman:',
                 'alternativas': ['Hidrolasas',
                                  'Lipasas',
                                  'Peroxidasas',
                                  'Catalasas',
                                  'Amilasas'],
                 'correcta': 'C'},
                {'pregunta': 'Las catalasas de los peroxisomas desdoblan el '
                             'peróxido de hidrógeno en agua y:',
                 'alternativas': ['Ozono',
                                  'Oxígeno',
                                  'Hidrógeno',
                                  'Nitrógeno',
                                  'Dióxido de carbono'],
                 'correcta': 'B'},
                {'pregunta': 'Los peroxisomas son especialmente activos en '
                             'las células del riñón y:',
                 'alternativas': ['Los pulmones',
                                  'El hígado',
                                  'La piel',
                                  'El corazón',
                                  'El cerebro'],
                 'correcta': 'B'},
                {'pregunta': 'Los glioxisomas son un tipo especial de '
                             'peroxisomas exclusivos de:',
                 'alternativas': ['Células animales',
                                  'Bacterias',
                                  'Hongos exclusivos',
                                  'Células vegetales',
                                  'Protozoarios'],
                 'correcta': 'D'},
                {'pregunta': 'Los glioxisomas contienen enzimas del ciclo '
                             'del glioxilato, que convierten lípidos en:',
                 'alternativas': ['Minerales',
                                  'Proteínas',
                                  'Ácidos nucleicos',
                                  'Vitaminas',
                                  'Azúcares'],
                 'correcta': 'E'},
                {'pregunta': 'Los glioxisomas se encuentran en los '
                             'cotiledones o endospermo de semillas durante:',
                 'alternativas': ['La fecundación',
                                  'La germinación',
                                  'La polinización',
                                  'La maduración del fruto',
                                  'La floración'],
                 'correcta': 'B'},
                {'pregunta': 'Las vacuolas se forman a partir del retículo '
                             'endoplásmico, el complejo de Golgi o '
                             'invaginaciones de:',
                 'alternativas': ['Las mitocondrias',
                                  'La membrana plasmática',
                                  'Los peroxisomas',
                                  'El núcleo',
                                  'Los ribosomas'],
                 'correcta': 'B'},
                {'pregunta': 'En protistas como euglenas y paramecios, las '
                             'vacuolas eliminan el exceso de:',
                 'alternativas': ['Proteínas',
                                  'Lípidos',
                                  'Sales exclusivas',
                                  'Glucosa',
                                  'Agua'],
                 'correcta': 'E'},
                {'pregunta': 'Las vacuolas actúan como almacén de agua, '
                             'sales, azúcares y:',
                 'alternativas': ['Solo ADN',
                                  'Solo proteínas',
                                  'Solo ARN',
                                  'Desechos celulares',
                                  'Solo lípidos'],
                 'correcta': 'D'},
                {'pregunta': 'El organelo celular que se ocupa de la '
                             'biogénesis de lípidos en la célula eucariota '
                             'es:',
                 'alternativas': ['El glioxisoma',
                                  'El retículo endoplasmático',
                                  'El ribosoma',
                                  'La mitocondria',
                                  'El peroxisoma'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'ESTRUCTURA GENERAL / PARED CELULAR Y '
                                'GLICOCÁLIX (+1)',
                      'items': ['Las células eucariotas tienen su ADN '
                                'encerrado dentro de una doble membrana o '
                                'envoltura nuclear.',
                                'La pared celular está presente solo en '
                                'células vegetales y hongos, y está formada '
                                'por celulosa.',
                                'La membrana plasmática es de naturaleza '
                                'lipoproteica y tiene permeabilidad '
                                'selectiva.']},
                     {'titulo': 'PROTEÍNAS DE MEMBRANA / FUNCIONES DE LA '
                                'MEMBRANA CELULAR (+1)',
                      'items': ['Las proteínas periféricas o extrínsecas se '
                                'localizan en las superficies de la membrana '
                                'y son solubles en agua.',
                                'La compartimentalización separa los medios '
                                'intracelular y extracelular.',
                                'El transporte pasivo, o difusión pasiva, '
                                'ocurre en forma espontánea, sin gasto de '
                                'energía, a favor del gradiente de '
                                'concentración.']},
                     {'titulo': 'TRANSPORTE ACTIVO / EL CITOPLASMA (+1)',
                      'items': ['El transporte activo requiere gasto de '
                                'energía en forma de ATP, mediante la enzima '
                                'ATPasa.',
                                'El citoplasma, o hialoplasma, es el mayor '
                                'compartimento de la célula, entre la '
                                'membrana plasmática y la nuclear.',
                                'Los cilios y flagelos son proyecciones '
                                'móviles formadas por microtúbulos y '
                                'proteínas accesorias como la dineína y '
                                'nexina.']},
                     {'titulo': 'RIBOSOMAS Y RETÍCULO ENDOPLASMÁTICO / '
                                'COMPLEJO DE GOLGI Y LISOSOMAS (+1)',
                      'items': ['Los ribosomas tienen dos subunidades '
                                'compuestas por ARNr, y se elaboran en el '
                                'nucléolo.',
                                'El complejo de Golgi es un grupo de sacos '
                                'aplanados llamados dictiosomas.',
                                'Los peroxisomas son similares a los '
                                'lisosomas, pero contienen enzimas '
                                'distintas: peroxidasas y catalasas.']},
                     {'titulo': 'GLIOXISOMAS / VACUOLAS (+1)',
                      'items': ['Los glioxisomas son un tipo especial de '
                                'peroxisomas exclusivos de células '
                                'vegetales.',
                                'Las vacuolas son sacos membranosos que se '
                                'forman del retículo endoplásmico, el Golgi, '
                                'o invaginaciones de la membrana.',
                                'Las mitocondrias se encuentran en todas las '
                                'células eucariotas, con doble membrana '
                                '(interna y externa).']},
                     {'titulo': 'PLASTOS Y CLOROPLASTOS / EL NÚCLEO (+1)',
                      'items': ['Los plastos son orgánulos elípticos de las '
                                'células vegetales, similares a las '
                                'mitocondrias.',
                                'El núcleo está ausente en los glóbulos '
                                'rojos maduros de los mamíferos.',
                                'La cromatina está constituida por ADN, '
                                'histonas y proteínas no histónicas.']},
                     {'titulo': 'CROMOSOMAS',
                      'items': ['Los cromosomas resultan del empaquetamiento '
                                'máximo del ADN nuclear con proteínas.']}]},
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
                {'titulo': '7.4 FASE LUMINOSA: FOTOSISTEMAS',
                 'items': ['La {fase luminosa} ocurre en las membranas de '
                           'los {tilacoides}, donde la clorofila rompe la '
                           'molécula de agua ({fotólisis}).',
                           'Existen dos {fotosistemas}: el {1}, rico en '
                           'clorofila a, y el {2}, rico en clorofila b.',
                           'Cada fotosistema tiene un {complejo antena}, que '
                           'capta la energía luminosa, y un {centro de '
                           'reacción}.',
                           'En el {fotosistema 2}, los electrones perdidos '
                           'por la clorofila se reponen con los del '
                           'rompimiento del {agua}; se produce {ATP}.',
                           'En el {fotosistema 1}, los electrones llegan '
                           'hasta el NADP+, formando {NADPH}.',
                           'La molécula resultante del fotosistema 2 es '
                           '{ATP}; la del fotosistema 1 es {NADPH}; ambas se '
                           'usan en la fase {oscura}.']},
                {'titulo': '7.5 FASE OSCURA: EL CICLO DE CALVIN',
                 'items': ['La {fase oscura}, o reacciones independientes de '
                           'la luz, ocurre en el {estroma} del cloroplasto.',
                           'En esta fase, el CO2 y el agua se unen para '
                           'producir {glucosa}, usando el ATP y NADPH de la '
                           'fase {luminosa}.',
                           'El ciclo donde el CO2 se fija se llama ciclo de '
                           '{Calvin} o C3.',
                           'En la etapa de {fijación de carbono}, seis '
                           'moléculas de bifosfato de ribulosa (BPRU) se '
                           'combinan con {CO2} para formar ácido '
                           'fosfoglicérico (AFG).',
                           'En la etapa de síntesis de '
                           '{gliceraldehído-3-fosfato} (G3P), el ATP y NADPH '
                           'transforman el AFG.',
                           'En la etapa de {regeneración} del BPRU, se '
                           'vuelve a formar bifosfato de ribulosa y se '
                           'sintetiza {glucosa} u otras moléculas '
                           'complejas.']},
                {'titulo': '7.6 NUTRICIÓN HETERÓTROFA',
                 'items': ['Un {heterótrofo} es un organismo que no puede '
                           'fabricar sus propios alimentos y deriva '
                           'nutrientes de materia orgánica {ajena}.',
                           'Son heterótrofos los animales, hongos, protozoos '
                           'y la mayoría de las {bacterias}.',
                           'Los organismos {predadores} pueden ser '
                           'cazadores, carroñeros, parásitos u {omnívoros}.',
                           'Según su alimento, los predadores pueden ser '
                           '{carnívoros} o {herbívoros}.',
                           'Los organismos {saprobios} se alimentan por '
                           'absorción de materia orgánica en '
                           'descomposición.']},
                {'titulo': '7.7 RESPIRACIÓN AERÓBICA: GLUCÓLISIS',
                 'items': ['La respiración {aeróbica} requiere presencia de '
                           'oxígeno, produciendo dióxido de carbono y '
                           '{agua}.',
                           'La {glucólisis} es el proceso en que una '
                           'molécula de glucosa se rompe en dos moléculas de '
                           '{ácido pirúvico}, en el citosol.']},
                {'titulo': '7.8 FORMACIÓN DE ACETIL CoA',
                 'items': ['La respiración celular comprende cuatro etapas: '
                           '{glucólisis}, formación de acetil CoA, ciclo de '
                           '{Krebs}, y cadena de transporte de electrones.',
                           'En la {formación de acetil CoA}, el ácido '
                           'pirúvico llega a la matriz mitocondrial y se une '
                           'a la {coenzima A}.',
                           'Por cada ácido pirúvico se produce una molécula '
                           'de {NADH} y una de {CO2}; en total, 2 NADH y 2 '
                           'CO2.']},
                {'titulo': '7.9 EL CICLO DE KREBS',
                 'items': ['El {ciclo de Krebs}, o del ácido cítrico, debe '
                           'su nombre a {Hans Adolf Krebs}, quien lo estudió '
                           'hacia 1937.',
                           'El ciclo de Krebs se realiza en la {matriz '
                           'mitocondrial}; cada acetil CoA se oxida hasta '
                           'CO2 y agua.',
                           'Por cada acetil CoA se producen 3 {NADH}, 1 '
                           'FADH2, 1 GTP (que se convierte en ATP) y 2 '
                           'moléculas de {CO2}.',
                           'Por las dos moléculas de acetil CoA del ciclo '
                           'completo, se producen en total {18} moléculas de '
                           'ATP.']},
                {'titulo': '7.10 CADENA RESPIRATORIA (FOSFORILACIÓN '
                           'OXIDATIVA)',
                 'items': ['La {cadena respiratoria}, o fosforilación '
                           'oxidativa, es la etapa final de la respiración '
                           'celular, donde se produce la mayor cantidad de '
                           '{ATP}.',
                           'Ocurre en el espacio {intermembranoso}; los '
                           'electrones fluyen desde el NADH y FADH2 hasta '
                           'formar {agua}.',
                           'El movimiento de iones H+ de regreso a la matriz '
                           'permite la síntesis de ATP mediante la enzima '
                           '{ATP-sintasa}.',
                           'En la fosforilación oxidativa se producen en '
                           'total de {26} a 28 moléculas de ATP.',
                           'Los organismos que solo pueden vivir en '
                           'presencia de oxígeno se llaman {aerobios '
                           'obligados}.',
                           'Organismos como levaduras, anélidos y moluscos, '
                           'que pueden producir ATP sin oxígeno, se llaman '
                           '{anaerobios facultativos}.']},
                {'titulo': '7.11 RESPIRACIÓN ANAERÓBICA O FERMENTACIÓN',
                 'items': ['La respiración {anaeróbica}, o fermentación, se '
                           'lleva a cabo en {ausencia} de oxígeno.',
                           'En ambos tipos de fermentación ocurre primero la '
                           '{glucólisis} normal.',
                           'En esfuerzos musculares prolongados, la '
                           '{fermentación} produce un aporte rápido de '
                           'ATP.']},
                {'titulo': '7.12 TIPOS DE FERMENTACIÓN',
                 'items': ['En la fermentación {alcohólica}, los piruvatos '
                           'se reducen a {etanol}, con liberación de CO2.',
                           'La fermentación alcohólica es causada por '
                           '{levaduras}, como el Saccharomyces {cerevisiae}.',
                           'En la fermentación {láctica}, el ácido pirúvico '
                           'se reduce a {lactato} o ácido láctico.',
                           'La fermentación láctica es causada por bacterias '
                           'como {Lactobacillus} y Streptococcus.',
                           'Productos como el yogur se conservan bien porque '
                           'la fermentación láctica reduce el {pH}.']}],
  'cuadros': [{'titulo': '7.2 TIPOS DE PROCARIONTES QUIMIOAUTÓTROFOS',
               'encabezados': ['Tipo', 'Oxida'],
               'filas': [['{Sulfurosos}', 'Compuestos de {azufre}'],
                         ['{Hidrogenosos}', '{Hidrógeno} del aire'],
                         ['{Ferrosos}', '{Hierro}'],
                         ['{Nitrificantes}', '{Amoniaco} y nitritos']]}],
  'preguntas': [{'pregunta': 'La nutrición celular puede ser de dos tipos: '
                             'autótrofa y:',
                 'alternativas': ['Mixótrofa',
                                  'Quimiótrofa exclusiva',
                                  'Heterótrofa',
                                  'Saprótrofa exclusiva',
                                  'Fotótrofa exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La nutrición realizada por células que '
                             'fabrican su propio alimento a partir de '
                             'compuestos inorgánicos es:',
                 'alternativas': ['Parasitaria',
                                  'Saprofita exclusiva',
                                  'Heterótrofa',
                                  'Autótrofa',
                                  'Mixótrofa'],
                 'correcta': 'D'},
                {'pregunta': 'Los dos procesos de nutrición autótrofa son la '
                             'quimioautótrofa y la:',
                 'alternativas': ['Simbiótica',
                                  'Parasitaria',
                                  'Heterótrofa',
                                  'Fotoautótrofa',
                                  'Saprófita'],
                 'correcta': 'D'},
                {'pregunta': 'La nutrición quimioautótrofa es característica '
                             'de los organismos:',
                 'alternativas': ['Vegetales exclusivamente',
                                  'Animales exclusivamente',
                                  'Procariontes',
                                  'Fúngicos exclusivamente',
                                  'Eucariotas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los organismos quimiótrofos utilizan energía '
                             'química obtenida mediante la oxidación de '
                             'productos:',
                 'alternativas': ['Solo lípidos',
                                  'Solo proteínas',
                                  'Orgánicos exclusivamente',
                                  'Inorgánicos',
                                  'Solo carbohidratos'],
                 'correcta': 'D'},
                {'pregunta': 'Los procariontes que oxidan compuestos de '
                             'azufre se llaman procariontes:',
                 'alternativas': ['Ferrosos',
                                  'Fotótrofos',
                                  'Sulfurosos',
                                  'Nitrificantes',
                                  'Hidrogenosos'],
                 'correcta': 'C'},
                {'pregunta': 'Los procariontes sulfurosos producen como '
                             'resultado de su oxidación:',
                 'alternativas': ['Ácido carbónico',
                                  'Ácido clorhídrico',
                                  'Ácido nítrico',
                                  'Ácido fosfórico',
                                  'Ácido sulfúrico'],
                 'correcta': 'E'},
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
                 'alternativas': ['Autótrofos exclusivos',
                                  'Ferrosos',
                                  'Sulfurosos',
                                  'Hidrogenosos',
                                  'Nitrificantes'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan el amoniaco en '
                             'nitritos y estos en nitratos se llaman '
                             'procariontes:',
                 'alternativas': ['Fotótrofos',
                                  'Nitrificantes',
                                  'Ferrosos',
                                  'Hidrogenosos',
                                  'Sulfurosos'],
                 'correcta': 'B'},
                {'pregunta': 'Las bacterias nitrificantes desempeñan un '
                             'papel importante en:',
                 'alternativas': ['La reproducción celular',
                                  'La respiración animal',
                                  'La fotosíntesis vegetal',
                                  'La digestión humana',
                                  'La fertilidad de los suelos'],
                 'correcta': 'E'},
                {'pregunta': 'El organelo típicamente vegetal necesario para '
                             'la fotosíntesis es:',
                 'alternativas': ['La mitocondria',
                                  'El lisosoma',
                                  'El aparato de Golgi',
                                  'El ribosoma',
                                  'El cloroplasto'],
                 'correcta': 'E'},
                {'pregunta': 'Las pilas de «monedas» dentro del cloroplasto '
                             'se llaman:',
                 'alternativas': ['Estroma',
                                  'Tilacoides',
                                  'Matriz',
                                  'Cresta',
                                  'Cristas'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de tilacoides recibe el nombre de:',
                 'alternativas': ['Estroma',
                                  'Nucleoide',
                                  'Cresta',
                                  'Matriz',
                                  'Grana'],
                 'correcta': 'E'},
                {'pregunta': 'La sustancia rica en enzimas que rodea a los '
                             'tilacoides se llama:',
                 'alternativas': ['Matriz mitocondrial',
                                  'Cresta',
                                  'Estroma',
                                  'Citosol',
                                  'Grana'],
                 'correcta': 'C'},
                {'pregunta': 'La fotosíntesis transforma la energía luminosa '
                             'en energía:',
                 'alternativas': ['Química',
                                  'Mecánica',
                                  'Eléctrica',
                                  'Térmica exclusiva',
                                  'Nuclear'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los reactivos necesarios para la '
                             'fotosíntesis figura la clorofila y:',
                 'alternativas': ['Solo oxígeno',
                                  'Solo agua',
                                  'Dióxido de carbono, agua y luz solar',
                                  'Solo glucosa',
                                  'Solo nitrógeno'],
                 'correcta': 'C'},
                {'pregunta': 'Los productos finales de la fotosíntesis son '
                             'glucosa y:',
                 'alternativas': ['Oxígeno',
                                  'Dióxido de carbono',
                                  'Agua exclusivamente',
                                  'Clorofila',
                                  'Nitrógeno'],
                 'correcta': 'A'},
                {'pregunta': 'La fase de la fotosíntesis que depende de la '
                             'luz se llama fase:',
                 'alternativas': ['II u oscura',
                                  'Anaeróbica',
                                  'Neutra',
                                  'I o luminosa',
                                  'Intermedia'],
                 'correcta': 'D'},
                {'pregunta': 'La fase de la fotosíntesis independiente de la '
                             'luz puede ocurrir:',
                 'alternativas': ['Solo de noche',
                                  'Solo de día',
                                  'De día y de noche',
                                  'Solo en invierno',
                                  'Nunca'],
                 'correcta': 'C'},
                {'pregunta': 'Un organismo heterótrofo es aquel que:',
                 'alternativas': ['Solo se alimenta de minerales',
                                  'No puede fabricar sus propios alimentos',
                                  'Solo realiza fotosíntesis',
                                  'Vive sin necesidad de nutrientes',
                                  'Fabrica sus propios alimentos'],
                 'correcta': 'B'},
                {'pregunta': 'Son organismos heterótrofos los animales, '
                             'hongos, protozoos y la mayoría de:',
                 'alternativas': ['Las bacterias',
                                  'Los líquenes exclusivamente',
                                  'Las algas',
                                  'Las plantas',
                                  'Los virus exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los organismos que se alimentan de materia '
                             'orgánica en descomposición mediante absorción '
                             'se llaman:',
                 'alternativas': ['Quimioautótrofos',
                                  'Fotoheterótrofos',
                                  'Carnívoros',
                                  'Predadores',
                                  'Saprobios'],
                 'correcta': 'E'},
                {'pregunta': 'Los predadores clasificados según su alimento '
                             'pueden ser carnívoros o:',
                 'alternativas': ['Detritívoros',
                                  'Fotótrofos',
                                  'Quimiótrofos',
                                  'Saprobios',
                                  'Herbívoros'],
                 'correcta': 'E'},
                {'pregunta': 'La respiración aeróbica requiere presencia de:',
                 'alternativas': ['Oxígeno',
                                  'Dióxido de carbono exclusivo',
                                  'Hidrógeno libre',
                                  'Nitrógeno',
                                  'Metano'],
                 'correcta': 'A'},
                {'pregunta': 'La respiración aeróbica produce como desechos '
                             'dióxido de carbono y:',
                 'alternativas': ['Etanol',
                                  'Oxígeno puro',
                                  'Ácido láctico',
                                  'Glucosa',
                                  'Agua'],
                 'correcta': 'E'},
                {'pregunta': 'La glucólisis rompe una molécula de glucosa '
                             'para formar dos moléculas de:',
                 'alternativas': ['ATP exclusivamente',
                                  'Ácido láctico',
                                  'Agua',
                                  'Ácido pirúvico',
                                  'Etanol'],
                 'correcta': 'D'},
                {'pregunta': 'La glucólisis ocurre en:',
                 'alternativas': ['El núcleo',
                                  'El citosol',
                                  'El cloroplasto',
                                  'La mitocondria',
                                  'El aparato de Golgi'],
                 'correcta': 'B'},
                {'pregunta': 'La respiración anaeróbica, o fermentación, se '
                             'lleva a cabo en:',
                 'alternativas': ['Presencia de nitrógeno exclusivamente',
                                  'Presencia abundante de oxígeno',
                                  'Ausencia de oxígeno',
                                  'Total oscuridad',
                                  'Altas temperaturas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'En esfuerzos musculares prolongados, el cuerpo '
                             'humano recurre a:',
                 'alternativas': ['La respiración aeróbica exclusivamente',
                                  'La fermentación para un aporte rápido de '
                                  'ATP',
                                  'La quimiosíntesis',
                                  'Solo la fotosíntesis',
                                  'La transcripción'],
                 'correcta': 'B'},
                {'pregunta': 'En la fermentación alcohólica, los piruvatos '
                             'se reducen a:',
                 'alternativas': ['Etanol',
                                  'Agua',
                                  'ATP directamente',
                                  'Ácido láctico',
                                  'Glucosa'],
                 'correcta': 'A'},
                {'pregunta': 'La fermentación alcohólica es causada '
                             'principalmente por:',
                 'alternativas': ['Virus',
                                  'Hongos filamentosos exclusivos',
                                  'Levaduras como Saccharomyces cerevisiae',
                                  'Protozoos',
                                  'Bacterias lácticas'],
                 'correcta': 'C'},
                {'pregunta': 'En la elaboración de pan, el dióxido de '
                             'carbono producido por la fermentación '
                             'alcohólica es responsable de:',
                 'alternativas': ['El crecimiento de la masa',
                                  'El sabor amargo',
                                  'La conservación',
                                  'La textura dura',
                                  'El color oscuro'],
                 'correcta': 'A'},
                {'pregunta': 'En la fermentación láctica, el ácido pirúvico '
                             'se reduce a:',
                 'alternativas': ['Glucosa',
                                  'Agua',
                                  'Etanol',
                                  'Dióxido de carbono',
                                  'Ácido láctico o lactato'],
                 'correcta': 'E'},
                {'pregunta': 'La fermentación láctica es causada, entre '
                             'otras bacterias, por:',
                 'alternativas': ['Escherichia coli exclusivamente',
                                  'Lactobacillus sp.',
                                  'Saccharomyces cerevisiae',
                                  'Salmonella',
                                  'Vibrio cholerae'],
                 'correcta': 'B'},
                {'pregunta': 'El yogur y la leche agria se obtienen '
                             'mediante:',
                 'alternativas': ['Fotosíntesis',
                                  'Respiración aeróbica exclusiva',
                                  'Fermentación alcohólica',
                                  'Fermentación láctica',
                                  'Quimiosíntesis'],
                 'correcta': 'D'},
                {'pregunta': 'Los productos lácteos fermentados se conservan '
                             'bien debido a que la fermentación:',
                 'alternativas': ['Aumenta el pH',
                                  'Aumenta la temperatura',
                                  'No afecta el pH',
                                  'Disminuye el pH, inhibiendo bacterias '
                                  'dañinas',
                                  'Elimina toda el agua'],
                 'correcta': 'D'},
                {'pregunta': 'La fase luminosa de la fotosíntesis ocurre en '
                             'las membranas de:',
                 'alternativas': ['La mitocondria',
                                  'El estroma',
                                  'El núcleo',
                                  'El citosol',
                                  'Los tilacoides'],
                 'correcta': 'E'},
                {'pregunta': 'El rompimiento de la molécula de agua durante '
                             'la fase luminosa se llama:',
                 'alternativas': ['Fotosíntesis exclusiva',
                                  'Hidrólisis',
                                  'Fotólisis',
                                  'Quimiosíntesis',
                                  'Glucólisis'],
                 'correcta': 'C'},
                {'pregunta': 'El fotosistema rico en clorofila a se llama '
                             'fotosistema:',
                 'alternativas': ['3', '4', '1', '2', '0'],
                 'correcta': 'C'},
                {'pregunta': 'El fotosistema rico en clorofila b se llama '
                             'fotosistema:',
                 'alternativas': ['2', '0', '1', '3', '4'],
                 'correcta': 'A'},
                {'pregunta': 'El componente del fotosistema que capta la '
                             'energía luminosa y la dirige al centro de '
                             'reacción se llama:',
                 'alternativas': ['Quinona',
                                  'Centro de reacción',
                                  'Aceptor primario',
                                  'Fotón captador',
                                  'Complejo antena'],
                 'correcta': 'E'},
                {'pregunta': 'En el fotosistema 2, los electrones perdidos '
                             'por la clorofila se reponen con electrones '
                             'provenientes de:',
                 'alternativas': ['El ATP',
                                  'El CO2',
                                  'La ruptura del agua',
                                  'La glucosa',
                                  'El NADP+'],
                 'correcta': 'C'},
                {'pregunta': 'La molécula primordial resultante del '
                             'fotosistema 2 es:',
                 'alternativas': ['CO2',
                                  'Glucosa',
                                  'ATP',
                                  'NADPH',
                                  'Oxígeno exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'En el fotosistema 1, los electrones llegan '
                             'hasta el NADP+ formando:',
                 'alternativas': ['ATP', 'CO2', 'Glucosa', 'Agua', 'NADPH'],
                 'correcta': 'E'},
                {'pregunta': 'La fase oscura de la fotosíntesis, o '
                             'reacciones independientes de la luz, ocurre '
                             'en:',
                 'alternativas': ['El núcleo',
                                  'El citosol',
                                  'Los tilacoides',
                                  'El estroma del cloroplasto',
                                  'La mitocondria'],
                 'correcta': 'D'},
                {'pregunta': 'El ciclo mediante el cual se fija el CO2 '
                             'durante la fase oscura se llama ciclo de:',
                 'alternativas': ['Urea',
                                  'Calvin',
                                  'Ácido cítrico',
                                  'Krebs',
                                  'Cori'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de fijación de carbono, el '
                             'bifosfato de ribulosa (BPRU) se combina con '
                             'CO2 para formar:',
                 'alternativas': ['ATP',
                                  'Oxígeno',
                                  'Glucosa directamente',
                                  'Ácido fosfoglicérico (AFG)',
                                  'Gliceraldehído-3-fosfato directamente'],
                 'correcta': 'D'},
                {'pregunta': 'En la síntesis de gliceraldehído-3-fosfato '
                             '(G3P), la energía necesaria proviene del ATP '
                             'y:',
                 'alternativas': ['La clorofila',
                                  'El oxígeno',
                                  'El CO2',
                                  'El NADPH',
                                  'El agua'],
                 'correcta': 'D'},
                {'pregunta': 'Las cuatro etapas de la respiración celular '
                             'son glucólisis, formación de acetil CoA, ciclo '
                             'de Krebs y:',
                 'alternativas': ['Ciclo de Calvin',
                                  'Fotólisis',
                                  'Cadena de transporte de electrones',
                                  'Glucogenólisis',
                                  'Fermentación'],
                 'correcta': 'C'},
                {'pregunta': 'En la formación de acetil CoA, el ácido '
                             'pirúvico llega a la matriz mitocondrial y se '
                             'une a:',
                 'alternativas': ['El FADH2',
                                  'La coenzima A',
                                  'El NADH',
                                  'El ATP',
                                  'El oxígeno'],
                 'correcta': 'B'},
                {'pregunta': 'Por cada molécula de ácido pirúvico procesada '
                             'en la formación de acetil CoA se produce una '
                             'molécula de NADH y una de:',
                 'alternativas': ['Oxígeno', 'CO2', 'ATP', 'Agua', 'Glucosa'],
                 'correcta': 'B'},
                {'pregunta': 'El ciclo de Krebs, o del ácido cítrico, debe '
                             'su nombre al científico:',
                 'alternativas': ['Louis Pasteur',
                                  'Melvin Calvin',
                                  'Hans Adolf Krebs',
                                  'Peter Mitchell',
                                  'Otto Warburg'],
                 'correcta': 'C'},
                {'pregunta': 'El ciclo de Krebs se realiza en:',
                 'alternativas': ['La matriz mitocondrial',
                                  'Los tilacoides',
                                  'El retículo endoplasmático',
                                  'El núcleo',
                                  'El citosol'],
                 'correcta': 'A'},
                {'pregunta': 'Por cada molécula de acetil CoA que entra al '
                             'ciclo de Krebs se producen 3 NADH, 1 FADH2, 1 '
                             'GTP y:',
                 'alternativas': ['3 moléculas de CO2',
                                  '1 molécula de CO2',
                                  '2 moléculas de CO2',
                                  '4 moléculas de CO2',
                                  'Ninguna molécula de CO2'],
                 'correcta': 'C'},
                {'pregunta': 'Por las dos moléculas de acetil CoA que entran '
                             'al ciclo de Krebs completo, se producen en '
                             'total:',
                 'alternativas': ['10 moléculas de ATP',
                                  '5 moléculas de ATP',
                                  '30 moléculas de ATP',
                                  '24 moléculas de ATP',
                                  '18 moléculas de ATP'],
                 'correcta': 'E'},
                {'pregunta': 'La etapa final de la respiración celular, '
                             'donde se produce la mayor cantidad de ATP, se '
                             'llama:',
                 'alternativas': ['Ciclo de Krebs',
                                  'Cadena respiratoria o fosforilación '
                                  'oxidativa',
                                  'Formación de acetil CoA',
                                  'Fermentación',
                                  'Glucólisis'],
                 'correcta': 'B'},
                {'pregunta': 'La cadena respiratoria ocurre en el espacio '
                             'intermembranoso, donde los electrones fluyen '
                             'desde el NADH y FADH2 hasta formar:',
                 'alternativas': ['ATP directamente',
                                  'Agua',
                                  'Glucosa',
                                  'CO2',
                                  'Ácido pirúvico'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento de iones H+ de regreso a la '
                             'matriz mitocondrial permite la síntesis de ATP '
                             'mediante la enzima:',
                 'alternativas': ['Citrato sintasa',
                                  'ADN polimerasa',
                                  'ATP-sintasa',
                                  'Piruvato deshidrogenasa',
                                  'Hexoquinasa'],
                 'correcta': 'C'},
                {'pregunta': 'En la fosforilación oxidativa se producen en '
                             'total, a partir de las dos moléculas de acetil '
                             'CoA, un número de moléculas de ATP igual a:',
                 'alternativas': ['15 a 18',
                                  '40 a 45',
                                  '5 a 8',
                                  '10 a 12',
                                  '26 a 28'],
                 'correcta': 'E'},
                {'pregunta': 'Los organismos que solo pueden vivir en '
                             'presencia de oxígeno se llaman:',
                 'alternativas': ['Anaerobios facultativos',
                                  'Aerobios obligados',
                                  'Quimioautótrofos',
                                  'Anaerobios obligados',
                                  'Aerobios facultativos'],
                 'correcta': 'B'},
                {'pregunta': 'Organismos como las levaduras, anélidos y '
                             'moluscos, que pueden producir ATP sin oxígeno, '
                             'se llaman:',
                 'alternativas': ['Quimioautótrofos exclusivos',
                                  'Fotoautótrofos',
                                  'Aerobios obligados',
                                  'Anaerobios facultativos',
                                  'Heterótrofos exclusivos'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'TIPOS DE NUTRICIÓN CELULAR / NUTRICIÓN '
                                'QUIMIOAUTÓTROFA',
                      'items': ['La nutrición celular puede ser de dos '
                                'tipos: autótrofa y heterótrofa.',
                                'La nutrición quimioautótrofa, o '
                                'quimiosíntesis, es característica de los '
                                'organismos procariontes.']},
                     {'titulo': 'NUTRICIÓN FOTOAUTÓTROFA: LA FOTOSÍNTESIS / '
                                'FASE LUMINOSA: FOTOSISTEMAS',
                      'items': ['El organelo típicamente vegetal necesario '
                                'para la fotosíntesis es el cloroplasto.',
                                'La fase luminosa ocurre en las membranas de '
                                'los tilacoides, donde la clorofila rompe la '
                                'molécula de agua (fotólisis).']},
                     {'titulo': 'FASE OSCURA: EL CICLO DE CALVIN / NUTRICIÓN '
                                'HETERÓTROFA',
                      'items': ['La fase oscura, o reacciones independientes '
                                'de la luz, ocurre en el estroma del '
                                'cloroplasto.',
                                'Un heterótrofo es un organismo que no puede '
                                'fabricar sus propios alimentos y deriva '
                                'nutrientes de materia orgánica ajena.']},
                     {'titulo': 'RESPIRACIÓN AERÓBICA: GLUCÓLISIS / '
                                'FORMACIÓN DE ACETIL COA',
                      'items': ['La respiración aeróbica requiere presencia '
                                'de oxígeno, produciendo dióxido de carbono '
                                'y agua.',
                                'La respiración celular comprende cuatro '
                                'etapas: glucólisis, formación de acetil '
                                'CoA, ciclo de Krebs, y cadena de transporte '
                                'de electrones.']},
                     {'titulo': 'EL CICLO DE KREBS / CADENA RESPIRATORIA '
                                '(FOSFORILACIÓN OXIDATIVA)',
                      'items': ['El ciclo de Krebs, o del ácido cítrico, '
                                'debe su nombre a Hans Adolf Krebs, quien lo '
                                'estudió hacia 1937.',
                                'La cadena respiratoria, o fosforilación '
                                'oxidativa, es la etapa final de la '
                                'respiración celular, donde se produce la '
                                'mayor cantidad de ATP.']},
                     {'titulo': 'RESPIRACIÓN ANAERÓBICA O FERMENTACIÓN / '
                                'TIPOS DE FERMENTACIÓN',
                      'items': ['La respiración anaeróbica, o fermentación, '
                                'se lleva a cabo en ausencia de oxígeno.',
                                'En la fermentación alcohólica, los '
                                'piruvatos se reducen a etanol, con '
                                'liberación de CO2.']}]},
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
                {'titulo': '8.4 LA DIGESTIÓN: CONCEPTO Y TIPOS',
                 'items': ['El alimento sirve como combustible para energía '
                           'y como fuente de sustancias para {crecimiento} y '
                           'regeneración.',
                           'La {digestión intracelular} ocurre dentro de la '
                           'célula, tras englobar el alimento por '
                           '{fagocitosis} o pinocitosis.',
                           'Las esponjas digieren su alimento completamente '
                           'mediante el mecanismo {intracelular}.',
                           'La {digestión extracelular} descompone el '
                           'alimento fuera de las células, en compartimentos '
                           'continuos con el exterior.',
                           'En cnidarios y planarias ocurre digestión '
                           '{mixta}: extracelular primero, intracelular '
                           'después.',
                           'El tubo digestivo {incompleto} o celenterónico '
                           'tiene un solo orificio para entrada y salida.',
                           'El tubo digestivo {completo} o enterónico tiene '
                           'boca y {ano} separados, presente en la mayoría '
                           'de animales.']},
                {'titulo': '8.5 SISTEMA DIGESTIVO EN INVERTEBRADOS',
                 'items': ['Los {poríferos}, como las esponjas, no tienen '
                           'boca; filtran agua a través de poros para '
                           'obtener {alimento} y oxígeno.',
                           'En las esponjas, las células flageladas en '
                           'collar se llaman {coanocitos}, y todo el proceso '
                           'digestivo es {intracelular}.',
                           'Los {cnidarios} tienen una cavidad '
                           'gastrovascular incompleta, con boca rodeada de '
                           '{tentáculos}.',
                           'Los cnidarios poseen células urticantes llamadas '
                           '{cnidocitos}, con un aparato llamado '
                           '{nematocisto}.',
                           'Los {platelmintos} de vida libre, como las '
                           'planarias, tienen cavidad digestiva '
                           '{incompleta}, sin ano.',
                           'Los {nemátodos} tienen tubo digestivo '
                           '{completo}, con boca y ano en extremos opuestos.',
                           'Los {anélidos} tienen tubo digestivo completo '
                           'con buche, {molleja} e intestino con tiflosol.',
                           'Los {moluscos} tienen un órgano bucal llamado '
                           '{rádula}, con dientes quitinosos para raer '
                           'alimento.']},
                {'titulo': '8.6 SISTEMA DIGESTIVO EN VERTEBRADOS: AVES',
                 'items': ['En las {aves}, el esófago presenta una amplia '
                           'dilatación llamada {buche}, donde se almacena y '
                           'humedece el alimento.',
                           'El esófago desemboca en un ventrículo o estómago '
                           '{glandular}, cuyas paredes segregan jugos '
                           'digestivos.',
                           'Sigue la {molleja}, muy musculosa, que se '
                           'contrae rítmicamente y machaca el alimento con '
                           'ayuda de piedras.',
                           'En aves jóvenes, la cloaca presenta una '
                           'evaginación llamada bolsa de {Fabricio}, que '
                           'desaparece en los adultos.']},
                {'titulo': '8.7 SISTEMA DIGESTIVO HUMANO: ÓRGANOS',
                 'items': ['El tubo digestivo, o tracto {gastrointestinal}, '
                           'incluye boca, faringe, esófago, estómago, '
                           'intestino delgado y {grueso}.',
                           'Las {glándulas anexas} al tubo digestivo son las '
                           'salivales, el {hígado}, las vías biliares y el '
                           'páncreas.',
                           'El {intestino delgado} se encarga de la '
                           'absorción de nutrientes; el {intestino grueso}, '
                           'de agua y ciertas vitaminas.']},
                {'titulo': '8.8 HISTOLOGÍA DEL TUBO DIGESTIVO',
                 'items': ['Las cuatro capas del tubo digestivo, de adentro '
                           'hacia afuera, son: {mucosa}, submucosa, '
                           '{muscular} y serosa.',
                           'La capa {mucosa} comprende el epitelio de '
                           'revestimiento y la lámina propia.',
                           'En la boca, faringe y esófago, la capa muscular '
                           'es de tipo {esquelético}; en el resto, de '
                           'músculo {liso}.']},
                {'titulo': '8.9 LA BOCA',
                 'items': ['La cavidad bucal se divide en {vestíbulo} bucal '
                           'y cavidad oral propiamente dicha.',
                           'Las paredes de la boca son: labios (pared '
                           '{anterior}), mejillas (paredes laterales), '
                           'paladar duro (pared {superior}) y paladar blando '
                           '(pared posterior).',
                           'Los dientes se disponen en dos {arcos} dentales, '
                           'superior e inferior; solo el arco {inferior} es '
                           'móvil.']},
                {'titulo': '8.10 GLÁNDULAS SALIVALES',
                 'items': ['Las {glándulas salivales menores} están '
                           'diseminadas por toda la mucosa bucal: palatinas, '
                           'labiales, bucales y {linguales}.',
                           'Las {glándulas salivales mayores} son tres '
                           'pares: parótida, submandibular y {sublingual}.',
                           'La {parótida} es la más voluminosa de las '
                           'glándulas salivales, situada posterior a la rama '
                           'de la mandíbula.',
                           'La {saliva} secretada diariamente oscila entre '
                           '1000 y {1500} ml; está compuesta por 99,5% de '
                           'agua.',
                           'La saliva contiene la enzima {amilasa}, además '
                           'de mucina, lisozima, urea y ácido úrico.']},
                {'titulo': '8.11 EL HÍGADO',
                 'items': ['El {hígado}, o hepar, es la glándula más '
                           'voluminosa anexa al aparato digestivo; pesa '
                           'alrededor de {1,4} kilos en un adulto.',
                           'El hígado se divide en dos lóbulos, derecho e '
                           'izquierdo, separados por el ligamento '
                           '{falciforme}.',
                           'Entre las funciones del hígado están producir '
                           '{bilis} para la digestión de grasas, y el '
                           'anticoagulante {heparina}.',
                           'El hígado transforma el exceso de monosacáridos '
                           'en {glucógeno} o grasa, y los almacena.',
                           'El hígado almacena glucógeno, cobre, hierro y '
                           'las vitaminas {A}, D, E y K.',
                           'La {vesícula biliar} almacena la bilis; las vías '
                           'biliares se dividen en {intrahepáticas} y '
                           'extrahepáticas.',
                           'El conducto {colédoco}, o conducto biliar '
                           'principal, conduce la bilis hasta el duodeno.']},
                {'titulo': '8.12 EL PÁNCREAS',
                 'items': ['El {páncreas} es una glándula de secreción '
                           'externa e interna, unida al duodeno por sus '
                           'conductos {excretores}.',
                           'Las partes del páncreas son: cabeza, cuerpo, '
                           'cuello y {cola}.',
                           'Como glándula {endocrina}, el páncreas regula el '
                           'metabolismo de glúcidos mediante la insulina y '
                           'el {glucagón}.',
                           'Como glándula {exocrina}, el páncreas libera '
                           'jugo pancreático alcalino con enzimas como '
                           'tripsinógeno, amilasa y {lipasa}.',
                           'La secreción pancreática es regulada por la '
                           'hormona {secretina}.']},
                {'titulo': '8.13 SISTEMA CIRCULATORIO: TIPOS',
                 'items': ['Las partes principales del sistema circulatorio '
                           'son el {corazón}, los vasos sanguíneos y la '
                           '{sangre}.',
                           'El sistema {cerrado} confina la sangre al '
                           'corazón y los vasos; propio de moluscos '
                           'cefalópodos y {vertebrados}.',
                           'El sistema {abierto} permite que la sangre bañe '
                           'directamente tejidos en espacios llamados '
                           '{hemocele}.',
                           'La circulación {simple}, propia de peces, hace '
                           'que la sangre pase una sola vez por el {corazón} '
                           'en cada circuito.',
                           'La circulación {doble}, de anfibios a mamíferos, '
                           'hace que la sangre pase dos veces por el '
                           'corazón.',
                           'La circulación doble {incompleta} mezcla sangre '
                           'arterial y venosa por tener un solo '
                           '{ventrículo}; en anfibios y reptiles.',
                           'La circulación doble {completa} no mezcla la '
                           'sangre; propia de aves y {mamíferos}.']},
                {'titulo': '8.14 CIRCULACIÓN EN INVERTEBRADOS',
                 'items': ['Los {poríferos} y {cnidarios} no tienen sistema '
                           'circulatorio; el transporte es por difusión '
                           '{simple}.',
                           'En los cnidarios, la {cavidad gastrovascular} '
                           'hace las veces de órgano circulatorio.']},
                {'titulo': '8.15 CIRCULACIÓN EN VERTEBRADOS',
                 'items': ['El sistema circulatorio de los vertebrados es '
                           '{cerrado} y no presenta senos o lagunas.',
                           'Los {peces} tienen corazón con una aurícula y un '
                           'ventrículo, con circulación {simple} y completa.',
                           'Los {anfibios} tienen corazón con dos aurículas '
                           'y un ventrículo, donde se mezcla la sangre '
                           'arterial y {venosa}.',
                           'Los {reptiles} tienen dos aurículas y dos '
                           'ventrículos con tabique {incompleto} (excepto '
                           'cocodrilos).',
                           'Las {aves} tienen corazón cónico con circulación '
                           'doble y completa; su corazón late más {rápido} '
                           'que el de los mamíferos.',
                           'Los {mamíferos} tienen dos aurículas y dos '
                           'ventrículos completamente separados, con '
                           'glóbulos rojos {anucleados}.']},
                {'titulo': '8.16 LA SANGRE',
                 'items': ['El sistema circulatorio también se llama '
                           '{cardiovascular}: «cardio» (corazón) y '
                           '«vascular» (vasos sanguíneos).',
                           'La sangre está formada por {plasma} y tres tipos '
                           'de células: eritrocitos, {leucocitos} y '
                           'plaquetas.',
                           'Los {eritrocitos} o glóbulos rojos transportan '
                           'oxígeno gracias al hierro de la {hemoglobina}.',
                           'Los eritrocitos pierden el {núcleo} al madurar y '
                           'tienen forma de disco {bicóncavo}.',
                           'Los {leucocitos} o glóbulos blancos participan '
                           'en la defensa del organismo; su formación se '
                           'llama {hematopoyesis}.',
                           'Las {plaquetas} se forman a partir de los '
                           '{megacariocitos} y participan en la '
                           'coagulación.']},
                {'titulo': '8.17 EL CORAZÓN',
                 'items': ['El corazón bombea sangre entre {60} y 100 veces '
                           'por minuto, ubicado en el {mediastino}.',
                           'El corazón posee cuatro cavidades: dos '
                           '{aurículas} y dos {ventrículos}.',
                           'Las tres capas del corazón, de adentro hacia '
                           'afuera, son {endocardio}, miocardio y '
                           '{epicardio}.',
                           'La válvula {mitral} o bicúspide conecta el '
                           'ventrículo izquierdo con la aurícula izquierda.',
                           'La válvula {tricúspide} conecta el ventrículo '
                           'derecho con la aurícula derecha.',
                           'El movimiento del corazón se da por {sístole} '
                           '(contracción) y {diástole} (relajación).']},
                {'titulo': '8.18 LOS VASOS SANGUÍNEOS',
                 'items': ['Las {venas} son vasos de paredes delgadas y poco '
                           'elásticas; llevan la sangre del cuerpo hacia el '
                           '{corazón}.',
                           'Las venas presentan {válvulas} que impiden que '
                           'la sangre descienda por su propio peso.',
                           'Las {arterias} son vasos de paredes gruesas, '
                           'resistentes y elásticas, formadas por tres '
                           'capas.',
                           'Las arterias llevan la sangre con {oxígeno} a '
                           'presión desde el corazón hacia el resto del '
                           'cuerpo.',
                           'Los {capilares} sanguíneos son vasos '
                           'microscópicos que unen las venas con las '
                           'arterias, formados por una sola capa '
                           '{endotelial}.',
                           'La función de los capilares es favorecer el '
                           '{intercambio} gaseoso entre la sangre y los '
                           'tejidos.']},
                {'titulo': '8.19 CIRCULACIÓN MAYOR Y MENOR',
                 'items': ['La {circulación mayor}, o general, es la '
                           'circulación de la sangre oxigenada por todo el '
                           'cuerpo y el retorno de la sangre venosa hacia el '
                           '{corazón}.',
                           'La {circulación menor}, o pulmonar, envía la '
                           'sangre venosa a los pulmones y recoge el oxígeno '
                           'para introducir la sangre oxigenada al '
                           '{corazón}.',
                           'Las cavidades {derechas} del corazón impulsan la '
                           'sangre con desechos hacia los pulmones para su '
                           'eliminación.']},
                {'titulo': '8.20 SISTEMA LINFÁTICO',
                 'items': ['El {sistema linfático}, o linfoide, es de suma '
                           'importancia en la defensa del organismo; está '
                           'integrado por una red de capilares por donde '
                           'circula la {linfa}.',
                           'La {linfa} transporta glóbulos blancos desde los '
                           'órganos linfoides primarios hasta los '
                           'secundarios: adenoides, amígdalas, bazo, '
                           'ganglios y placas de {Peyer}.',
                           'Los {ganglios linfáticos} actúan como filtro, '
                           'eliminando partículas extrañas y '
                           'microorganismos.',
                           'El sistema linfático tiene dos partes: una red '
                           'de {vasos linfáticos} que devuelve fluidos al '
                           'sistema vascular, y tejidos y órganos que '
                           'albergan linfocitos y {fagocitos}.']},
                {'titulo': '8.21 EXCRECIÓN: CONCEPTO Y EN INVERTEBRADOS',
                 'items': ['La {excreción} es el proceso por el cual los '
                           'seres vivos liberan productos de desecho del '
                           '{metabolismo}.',
                           'La excreción tiene por objeto principalmente '
                           'eliminar las sustancias {nitrogenadas}.',
                           'Los {poríferos} y cnidarios eliminan desechos '
                           'por difusión simple; el {amoniaco} es su '
                           'principal producto de excreción.',
                           'Los {platelmintos} poseen {protonefridios} con '
                           'células flamígeras como órganos excretores.',
                           'Los {anélidos} poseen {metanefridios}, que '
                           'eliminan principalmente {urea}.',
                           'Los insectos, arácnidos y miriápodos excretan '
                           'mediante los {tubos de Malpighi}.']},
                {'titulo': '8.22 EXCRECIÓN EN VERTEBRADOS',
                 'items': ['Los {peces} excretan por los riñones y por '
                           'células {branquiales} especializadas.',
                           'Los {anfibios} excretan por los riñones '
                           '(mesonefros) y la {piel}.',
                           'Los {reptiles} excretan por riñones de tipo '
                           '{metanefros}, planos y lobulados.']},
                {'titulo': '8.23 EL RIÑÓN',
                 'items': ['El aparato excretor humano se compone de dos '
                           '{riñones} y un conjunto de vías {urinarias}.',
                           'El riñón se encarga de producir la orina y de la '
                           '{osmorregulación}.',
                           'Cada riñón pesa aproximadamente {150} gramos y '
                           'mide entre 10 y 12 centímetros de largo.',
                           'Los riñones se dividen en tres zonas: {corteza}, '
                           'médula y {pelvis} renal.',
                           'La zona medular está formada por estructuras '
                           'triangulares llamadas pirámides de {Malpighi}.']},
                {'titulo': '8.24 LA NEFRONA Y FORMACIÓN DE LA ORINA',
                 'items': ['La {nefrona} es la unidad estructural y '
                           'funcional del riñón; cada riñón tiene cerca de '
                           'un {millón}.',
                           'La {cápsula de Bowman} contiene en su interior '
                           'al {glomérulo} de Malpighi.',
                           'El túbulo de la nefrona se divide en túbulo '
                           'contorneado proximal, {asa de Henle} y túbulo '
                           'contorneado distal.',
                           'La orina se forma mediante tres procesos: '
                           '{filtración}, reabsorción y {secreción}.',
                           'En la {filtración}, las proteínas y células '
                           'sanguíneas no atraviesan los capilares '
                           'glomerulares.',
                           'En la {reabsorción}, más del 90% del filtrado '
                           'regresa a la sangre.']}],
  'cuadros': [{'titulo': '8.2 DIVISIÓN FISIOLÓGICA DEL APARATO RESPIRATORIO',
               'encabezados': ['Porción', 'Función'],
               'filas': [['{Conductora}', '{Conducir} el aire'],
                         ['{Respiratoria}', '{Oxigenar} la sangre']]},
              {'titulo': 'COMPARACIÓN DE LA CIRCULACIÓN EN VERTEBRADOS',
               'despues_de': '8.15 CIRCULACIÓN EN VERTEBRADOS',
               'encabezados': ['Clase', 'Térmico y glóbulos rojos'],
               'filas': [['Peces', '{Ectotermos}, glóbulos rojos nucleados'],
                         ['Anfibios',
                          'Ectotermos, glóbulos rojos {elípticos} y '
                          'nucleados'],
                         ['Reptiles',
                          'Ectotermos, glóbulos rojos nucleados y '
                          '{elípticos}'],
                         ['Aves', '{Endotermos}, glóbulos rojos nucleados'],
                         ['Mamíferos',
                          'Endotermos, glóbulos rojos {anucleados}']]}],
  'preguntas': [{'pregunta': 'El hombre es un ser de respiración:',
                 'alternativas': ['Sin oxígeno',
                                  'Fermentativa exclusiva',
                                  'Aerobia',
                                  'Anaerobia',
                                  'Mixta obligatoria'],
                 'correcta': 'C'},
                {'pregunta': 'El oxígeno interviene en el paso final de la '
                             'cadena respiratoria, que ocurre en:',
                 'alternativas': ['El aparato de Golgi',
                                  'La membrana mitocondrial',
                                  'El citoplasma',
                                  'El retículo endoplasmático',
                                  'El núcleo'],
                 'correcta': 'B'},
                {'pregunta': 'El dióxido de carbono que se elimina proviene '
                             'del metabolismo celular, específicamente de la '
                             'glucólisis y:',
                 'alternativas': ['La replicación del ADN',
                                  'La síntesis de proteínas',
                                  'La mitosis',
                                  'La fotosíntesis',
                                  'El ciclo de Krebs'],
                 'correcta': 'E'},
                {'pregunta': 'Las vías respiratorias superiores comprenden '
                             'la nariz y:',
                 'alternativas': ['La tráquea',
                                  'Los alvéolos',
                                  'Los bronquios',
                                  'La faringe',
                                  'Los pulmones'],
                 'correcta': 'D'},
                {'pregunta': 'Las vías respiratorias inferiores incluyen la '
                             'laringe, la tráquea, los bronquios y:',
                 'alternativas': ['Los pulmones',
                                  'Los senos paranasales',
                                  'La nariz',
                                  'Las fosas nasales',
                                  'La faringe'],
                 'correcta': 'A'},
                {'pregunta': 'La porción del aparato respiratorio que '
                             'conduce el aire inspirado y espirado se llama '
                             'porción:',
                 'alternativas': ['Respiratoria',
                                  'Conductora',
                                  'Alveolar exclusiva',
                                  'Nasal exclusiva',
                                  'Bronquial exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La porción del aparato respiratorio encargada '
                             'de oxigenar la sangre se llama porción:',
                 'alternativas': ['Conductora',
                                  'Nasal',
                                  'Respiratoria',
                                  'Traqueal exclusiva',
                                  'Faríngea exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La porción respiratoria comprende bronquiolos '
                             'respiratorios, conductos alveolares y:',
                 'alternativas': ['Los cornetes',
                                  'La laringe',
                                  'La faringe',
                                  'Los alvéolos',
                                  'La tráquea'],
                 'correcta': 'D'},
                {'pregunta': 'El interior de la nariz está dividido en dos '
                             'cavidades nasales por:',
                 'alternativas': ['Los senos paranasales',
                                  'El tabique nasal',
                                  'La faringe',
                                  'Los cornetes',
                                  'Las coanas'],
                 'correcta': 'B'},
                {'pregunta': 'Las proyecciones recubiertas en las paredes '
                             'laterales de la mucosa nasal se llaman:',
                 'alternativas': ['Meatos exclusivamente',
                                  'Coanas',
                                  'Senos',
                                  'Cornetes',
                                  'Vestíbulos'],
                 'correcta': 'D'},
                {'pregunta': 'Las aberturas que comunican las fosas nasales '
                             'con la faringe se llaman:',
                 'alternativas': ['Vestíbulos',
                                  'Coanas',
                                  'Cornetes',
                                  'Meatos',
                                  'Narinas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las funciones de la nariz figura '
                             'calentar, humedecer y:',
                 'alternativas': ['Oxigenar la sangre directamente',
                                  'Regular la temperatura corporal total',
                                  'Eliminar bacterias del pulmón',
                                  'Producir dióxido de carbono',
                                  'Filtrar el aire'],
                 'correcta': 'E'},
                {'pregunta': 'La nariz también cumple la función de recibir '
                             'los impulsos:',
                 'alternativas': ['Visuales',
                                  'Gustativos',
                                  'Táctiles exclusivos',
                                  'Auditivos',
                                  'Olfatorios'],
                 'correcta': 'E'},
                {'pregunta': 'La faringe es un órgano compartido por los '
                             'aparatos respiratorio y:',
                 'alternativas': ['Nervioso',
                                  'Digestivo',
                                  'Circulatorio',
                                  'Endocrino',
                                  'Excretor'],
                 'correcta': 'B'},
                {'pregunta': 'La faringe, externamente, mide '
                             'aproximadamente:',
                 'alternativas': ['2 a 3 cm',
                                  '1 metro',
                                  '12 a 13 cm',
                                  '50 cm',
                                  '30 a 40 cm'],
                 'correcta': 'C'},
                {'pregunta': 'La faringe se ubica por detrás de la cavidad '
                             'nasal y la boca, y por delante de:',
                 'alternativas': ['Las vértebras cervicales',
                                  'El corazón',
                                  'El estómago',
                                  'El esófago exclusivamente',
                                  'Los pulmones'],
                 'correcta': 'A'},
                {'pregunta': 'La parte superior de la faringe, ubicada '
                             'detrás de la nariz, se llama:',
                 'alternativas': ['Orofaringe',
                                  'Traqueofaringe',
                                  'Nasofaringe o rinofaringe',
                                  'Laringofaringe',
                                  'Bronquiofaringe'],
                 'correcta': 'C'},
                {'pregunta': 'Los sistemas que comparten la responsabilidad '
                             'de aportar oxígeno y eliminar dióxido de '
                             'carbono son el respiratorio y el:',
                 'alternativas': ['Nervioso',
                                  'Excretor',
                                  'Cardiovascular',
                                  'Endocrino',
                                  'Digestivo'],
                 'correcta': 'C'},
                {'pregunta': 'Si el sistema respiratorio o cardiovascular '
                             'fallan, las células empiezan a morir por:',
                 'alternativas': ['Exceso de proteínas',
                                  'Exceso de glucosa',
                                  'Exceso de oxígeno',
                                  'Falta de agua',
                                  'Falta de oxígeno y acumulación de CO2'],
                 'correcta': 'E'},
                {'pregunta': 'La constitución anatómica de la faringe '
                             'incluye un armazón fibroso, músculos y:',
                 'alternativas': ['Hueso exclusivo',
                                  'Solo piel',
                                  'Un revestimiento mucoso',
                                  'Tejido adiposo exclusivo',
                                  'Cartílago exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El alimento sirve como combustible para '
                             'energía y como fuente de sustancias para:',
                 'alternativas': ['Solo la reproducción',
                                  'Solo la excreción',
                                  'Solo la respiración',
                                  'Solo el movimiento',
                                  'Crecimiento y regeneración'],
                 'correcta': 'E'},
                {'pregunta': 'La digestión que ocurre dentro de la célula, '
                             'tras englobar el alimento por fagocitosis, se '
                             'llama digestión:',
                 'alternativas': ['Enterónica',
                                  'Celenterónica',
                                  'Intracelular',
                                  'Extracelular',
                                  'Mixta'],
                 'correcta': 'C'},
                {'pregunta': 'Las esponjas digieren su alimento '
                             'completamente mediante el mecanismo:',
                 'alternativas': ['Ninguno de los anteriores',
                                  'Mixto',
                                  'Intracelular',
                                  'Extracelular',
                                  'Enterónico'],
                 'correcta': 'C'},
                {'pregunta': 'La digestión que descompone el alimento fuera '
                             'de las células se llama digestión:',
                 'alternativas': ['Fagocítica exclusiva',
                                  'Ninguna de las anteriores',
                                  'Extracelular',
                                  'Mixta exclusiva',
                                  'Intracelular'],
                 'correcta': 'C'},
                {'pregunta': 'En los cnidarios y planarias ocurre un tipo de '
                             'digestión llamada:',
                 'alternativas': ['Solo intracelular',
                                  'Fotosintética',
                                  'Solo extracelular',
                                  'Ninguna digestión real',
                                  'Mixta (extracelular e intracelular)'],
                 'correcta': 'E'},
                {'pregunta': 'El tubo digestivo con un solo orificio para '
                             'entrada y salida de alimento se llama tubo '
                             'digestivo:',
                 'alternativas': ['Completo o enterónico',
                                  'Circular',
                                  'Incompleto o celenterónico',
                                  'Mixto',
                                  'Doble'],
                 'correcta': 'C'},
                {'pregunta': 'El tubo digestivo con boca y ano separados se '
                             'llama tubo digestivo:',
                 'alternativas': ['Celenterónico',
                                  'Único',
                                  'Incompleto',
                                  'Completo o enterónico',
                                  'Simple'],
                 'correcta': 'D'},
                {'pregunta': 'La cavidad gastrovascular, presente en '
                             'cnidarios, cumple funciones de digestión y:',
                 'alternativas': ['Respiración exclusiva',
                                  'Excreción exclusiva',
                                  'Reproducción exclusiva',
                                  'Distribución de nutrientes',
                                  'Circulación sanguínea'],
                 'correcta': 'D'},
                {'pregunta': 'Los poríferos, como las esponjas, no poseen '
                             'aparato digestivo ni:',
                 'alternativas': ['Coanocitos',
                                  'Amebocitos',
                                  'Poros',
                                  'Boca',
                                  'Agua'],
                 'correcta': 'D'},
                {'pregunta': 'En las esponjas, las células flageladas en '
                             'collar se llaman:',
                 'alternativas': ['Tentáculos',
                                  'Amebocitos',
                                  'Coanocitos',
                                  'Nematocistos',
                                  'Cnidocitos'],
                 'correcta': 'C'},
                {'pregunta': 'Las células urticantes especializadas de los '
                             'cnidarios se llaman:',
                 'alternativas': ['Tiflosoles',
                                  'Coanocitos',
                                  'Amebocitos',
                                  'Rádulas',
                                  'Cnidocitos'],
                 'correcta': 'E'},
                {'pregunta': 'Los platelmintos de vida libre, como las '
                             'planarias, tienen una cavidad digestiva:',
                 'alternativas': ['Incompleta, sin ano',
                                  'Externa',
                                  'Ausente por completo',
                                  'Doble',
                                  'Completa, con ano'],
                 'correcta': 'A'},
                {'pregunta': 'Los nemátodos tienen un tubo digestivo:',
                 'alternativas': ['Incompleto',
                                  'Solo intracelular',
                                  'Completo, con boca y ano separados',
                                  'Sin órganos definidos',
                                  'Ausente'],
                 'correcta': 'C'},
                {'pregunta': 'En los anélidos, el órgano donde el alimento '
                             'es triturado se llama:',
                 'alternativas': ['Recto',
                                  'Esófago',
                                  'Molleja',
                                  'Buche',
                                  'Faringe'],
                 'correcta': 'C'},
                {'pregunta': 'El pliegue interno del intestino de los '
                             'anélidos, que aumenta la superficie de '
                             'absorción, se llama:',
                 'alternativas': ['Cnidocito',
                                  'Molleja',
                                  'Tiflosol',
                                  'Buche',
                                  'Rádula'],
                 'correcta': 'C'},
                {'pregunta': 'El órgano bucal de los moluscos, similar a una '
                             'lengua con dientes quitinosos, se llama:',
                 'alternativas': ['Rádula',
                                  'Faringe',
                                  'Molleja',
                                  'Tiflosol',
                                  'Buche'],
                 'correcta': 'A'},
                {'pregunta': 'El tubo digestivo humano también se llama '
                             'tracto:',
                 'alternativas': ['Circulatorio',
                                  'Respiratorio',
                                  'Gastrointestinal',
                                  'Nervioso',
                                  'Excretor'],
                 'correcta': 'C'},
                {'pregunta': 'Las glándulas anexas al tubo digestivo '
                             'incluyen las salivales, el hígado, las vías '
                             'biliares y:',
                 'alternativas': ['El corazón',
                                  'Los pulmones',
                                  'El bazo',
                                  'El páncreas',
                                  'Los riñones'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano encargado principalmente de la '
                             'absorción de nutrientes es:',
                 'alternativas': ['El estómago',
                                  'El esófago',
                                  'El intestino grueso',
                                  'La faringe',
                                  'El intestino delgado'],
                 'correcta': 'E'},
                {'pregunta': 'El intestino grueso se encarga principalmente '
                             'de la absorción de agua y:',
                 'alternativas': ['Ciertas vitaminas',
                                  'Grasas exclusivamente',
                                  'Proteínas',
                                  'Glucosa exclusivamente',
                                  'Aminoácidos exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Las cuatro capas del tubo digestivo, de '
                             'adentro hacia afuera, son mucosa, submucosa, '
                             'muscular y:',
                 'alternativas': ['Ósea',
                                  'Serosa',
                                  'Epitelial',
                                  'Nerviosa',
                                  'Cartilaginosa'],
                 'correcta': 'B'},
                {'pregunta': 'En la boca, faringe y esófago, la capa '
                             'muscular del tubo digestivo es de tipo:',
                 'alternativas': ['Cardíaco',
                                  'Ausente',
                                  'Mixto exclusivo',
                                  'Liso',
                                  'Esquelético'],
                 'correcta': 'E'},
                {'pregunta': 'En el resto del tracto digestivo, la capa '
                             'muscular es de músculo:',
                 'alternativas': ['Liso',
                                  'Cardíaco',
                                  'Estriado exclusivo',
                                  'Esquelético',
                                  'Ausente'],
                 'correcta': 'A'},
                {'pregunta': 'La cavidad bucal se divide en cavidad oral '
                             'propiamente dicha y:',
                 'alternativas': ['Esófago',
                                  'Vestíbulo bucal',
                                  'Faringe',
                                  'Estómago',
                                  'Laringe'],
                 'correcta': 'B'},
                {'pregunta': 'De los dos arcos dentales, el que es móvil es '
                             'el arco:',
                 'alternativas': ['Inferior',
                                  'Ambos son móviles',
                                  'Ninguno es móvil',
                                  'Superior',
                                  'Central'],
                 'correcta': 'A'},
                {'pregunta': 'Las partes principales del sistema '
                             'circulatorio son el corazón, la sangre y:',
                 'alternativas': ['Los pulmones',
                                  'El bazo',
                                  'El hígado',
                                  'Los vasos sanguíneos',
                                  'Los riñones'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema circulatorio que confina la sangre '
                             'al corazón y una serie de vasos se llama '
                             'sistema:',
                 'alternativas': ['Cerrado',
                                  'Lagunar',
                                  'Simple exclusivo',
                                  'Difuso',
                                  'Abierto'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema circulatorio en el que la sangre '
                             'baña directamente los tejidos se llama '
                             'sistema:',
                 'alternativas': ['Cerrado',
                                  'Doble',
                                  'Vascular puro',
                                  'Completo',
                                  'Abierto'],
                 'correcta': 'E'},
                {'pregunta': 'El espacio lagunar del sistema circulatorio '
                             'abierto se llama:',
                 'alternativas': ['Mediastino',
                                  'Miocardio',
                                  'Pseudoceloma',
                                  'Hemocele',
                                  'Endocardio'],
                 'correcta': 'D'},
                {'pregunta': 'La circulación en la que la sangre pasa una '
                             'sola vez por el corazón en cada circuito se '
                             'llama circulación:',
                 'alternativas': ['Doble',
                                  'Simple',
                                  'Mixta',
                                  'Incompleta',
                                  'Completa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La circulación simple es propia de:',
                 'alternativas': ['La mayoría de los peces',
                                  'Los anfibios',
                                  'Los mamíferos',
                                  'Los reptiles',
                                  'Las aves'],
                 'correcta': 'A'},
                {'pregunta': 'La circulación doble incompleta, con mezcla de '
                             'sangre arterial y venosa, se presenta en:',
                 'alternativas': ['Solo aves',
                                  'Aves y mamíferos',
                                  'Solo mamíferos',
                                  'Solo peces',
                                  'Anfibios y reptiles'],
                 'correcta': 'E'},
                {'pregunta': 'La circulación doble completa, sin mezcla de '
                             'sangre, es propia de:',
                 'alternativas': ['Anfibios y reptiles',
                                  'Solo peces',
                                  'Solo invertebrados',
                                  'Aves y mamíferos',
                                  'Solo anfibios'],
                 'correcta': 'D'},
                {'pregunta': 'Los poríferos y cnidarios realizan el '
                             'transporte de sustancias por:',
                 'alternativas': ['Vasos sanguíneos',
                                  'Difusión simple',
                                  'Un sistema abierto complejo',
                                  'Bombeo cardíaco',
                                  'Un sistema cerrado'],
                 'correcta': 'B'},
                {'pregunta': 'En los cnidarios, la estructura que hace las '
                             'veces de órgano circulatorio es:',
                 'alternativas': ['El pseudoceloma',
                                  'La cavidad gastrovascular',
                                  'Los vasos sanguíneos',
                                  'El hemocele',
                                  'El corazón'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema circulatorio también se conoce como '
                             'sistema:',
                 'alternativas': ['Nervioso',
                                  'Digestivo',
                                  'Cardiovascular',
                                  'Excretor',
                                  'Linfático'],
                 'correcta': 'C'},
                {'pregunta': 'La sangre está formada por plasma y tres tipos '
                             'de células: eritrocitos, leucocitos y:',
                 'alternativas': ['Plaquetas',
                                  'Neuronas',
                                  'Linfocitos exclusivamente',
                                  'Osteocitos',
                                  'Adipocitos'],
                 'correcta': 'A'},
                {'pregunta': 'Los glóbulos rojos transportan oxígeno gracias '
                             'a la presencia de hierro en:',
                 'alternativas': ['Las plaquetas',
                                  'Los leucocitos',
                                  'La hemoglobina',
                                  'El colágeno',
                                  'El plasma'],
                 'correcta': 'C'},
                {'pregunta': 'Los glóbulos rojos, al madurar, pierden:',
                 'alternativas': ['El color',
                                  'Toda su forma',
                                  'La membrana',
                                  'El núcleo',
                                  'El citoplasma completo'],
                 'correcta': 'D'},
                {'pregunta': 'Los glóbulos blancos participan principalmente '
                             'en:',
                 'alternativas': ['La digestión',
                                  'La defensa del organismo',
                                  'El transporte de nutrientes',
                                  'El transporte de oxígeno',
                                  'La coagulación'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de formación de los glóbulos '
                             'blancos se llama:',
                 'alternativas': ['Eritropoyesis exclusiva',
                                  'Hematopoyesis',
                                  'Trombopoyesis exclusiva',
                                  'Mitosis exclusiva',
                                  'Fagocitosis'],
                 'correcta': 'B'},
                {'pregunta': 'Las plaquetas se forman a partir de grandes '
                             'células llamadas:',
                 'alternativas': ['Linfocitos',
                                  'Leucocitos',
                                  'Megacariocitos',
                                  'Fagocitos',
                                  'Eritrocitos'],
                 'correcta': 'C'},
                {'pregunta': 'Las plaquetas intervienen principalmente en:',
                 'alternativas': ['La coagulación de la sangre',
                                  'La defensa inmunitaria',
                                  'La respiración',
                                  'El transporte de oxígeno',
                                  'La digestión'],
                 'correcta': 'A'},
                {'pregunta': 'El corazón se encuentra ubicado en un espacio '
                             'llamado:',
                 'alternativas': ['Mediastino',
                                  'Peritoneo',
                                  'Diafragma exclusivo',
                                  'Retroperitoneo',
                                  'Pleura'],
                 'correcta': 'A'},
                {'pregunta': 'El corazón posee cuatro cavidades: dos '
                             'aurículas y:',
                 'alternativas': ['Dos ventrículos',
                                  'Dos válvulas',
                                  'Dos arterias',
                                  'Dos venas cavas',
                                  'Dos tabiques'],
                 'correcta': 'A'},
                {'pregunta': 'Las tres capas del corazón son endocardio, '
                             'miocardio y:',
                 'alternativas': ['Mesocardio',
                                  'Endotelio exclusivo',
                                  'Pericardio exclusivo',
                                  'Peritoneo',
                                  'Epicardio'],
                 'correcta': 'E'},
                {'pregunta': 'La válvula que conecta el ventrículo izquierdo '
                             'con la aurícula izquierda se llama:',
                 'alternativas': ['Tricúspide',
                                  'Mitral o bicúspide',
                                  'Pulmonar exclusiva',
                                  'Aórtica exclusiva',
                                  'Semilunar exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La válvula que conecta el ventrículo derecho '
                             'con la aurícula derecha se llama:',
                 'alternativas': ['Mitral',
                                  'Bicúspide',
                                  'Semilunar',
                                  'Tricúspide',
                                  'Aórtica'],
                 'correcta': 'D'},
                {'pregunta': 'El movimiento de contracción del corazón se '
                             'llama:',
                 'alternativas': ['Mitosis',
                                  'Sístole',
                                  'Diástole',
                                  'Peristalsis',
                                  'Miosis'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento de relajación del corazón se '
                             'llama:',
                 'alternativas': ['Diástole',
                                  'Mitosis',
                                  'Fibrilación',
                                  'Miosis',
                                  'Sístole'],
                 'correcta': 'A'},
                {'pregunta': 'La excreción se define como el proceso por el '
                             'cual los seres vivos liberan:',
                 'alternativas': ['Nutrientes esenciales',
                                  'Solo agua',
                                  'Productos de desecho del metabolismo',
                                  'Solo oxígeno',
                                  'Hormonas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'La excreción tiene por objeto principalmente '
                             'eliminar sustancias:',
                 'alternativas': ['Vitamínicas',
                                  'Minerales',
                                  'Grasas exclusivamente',
                                  'Nitrogenadas',
                                  'Glucídicas exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Los poríferos y cnidarios eliminan desechos '
                             'principalmente en forma de:',
                 'alternativas': ['Urea',
                                  'Amoniaco',
                                  'Bilirrubina',
                                  'Creatinina',
                                  'Ácido úrico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los platelmintos poseen órganos excretores '
                             'llamados:',
                 'alternativas': ['Tubos de Malpighi',
                                  'Protonefridios',
                                  'Metanefridios',
                                  'Nefronas',
                                  'Glándulas coxales'],
                 'correcta': 'B'},
                {'pregunta': 'Los anélidos poseen órganos excretores '
                             'llamados:',
                 'alternativas': ['Nefronas',
                                  'Protonefridios',
                                  'Metanefridios',
                                  'Tubos de Malpighi',
                                  'Riñones'],
                 'correcta': 'C'},
                {'pregunta': 'Los insectos, arácnidos y miriápodos excretan '
                             'mediante:',
                 'alternativas': ['Metanefridios',
                                  'Riñones',
                                  'Protonefridios',
                                  'Los tubos de Malpighi',
                                  'Branquias exclusivas'],
                 'correcta': 'D'},
                {'pregunta': 'Los peces excretan por los riñones y por:',
                 'alternativas': ['El intestino exclusivamente',
                                  'Células branquiales especializadas',
                                  'Los pulmones',
                                  'La piel',
                                  'El hígado exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los anfibios excretan por los riñones '
                             '(mesonefros) y también por:',
                 'alternativas': ['Los tubos de Malpighi',
                                  'La piel',
                                  'Las branquias',
                                  'El hígado',
                                  'El intestino'],
                 'correcta': 'B'},
                {'pregunta': 'Los riñones de los reptiles son de tipo:',
                 'alternativas': ['Pronefros',
                                  'Tubos de Malpighi',
                                  'Mesonefros',
                                  'Metanefros',
                                  'Protonefridios'],
                 'correcta': 'D'},
                {'pregunta': 'El aparato excretor humano se compone de dos '
                             'riñones y un conjunto de:',
                 'alternativas': ['Glándulas salivales',
                                  'Bronquios',
                                  'Alvéolos',
                                  'Vías urinarias',
                                  'Vasos linfáticos'],
                 'correcta': 'D'},
                {'pregunta': 'El riñón se encarga de producir la orina y del '
                             'proceso de:',
                 'alternativas': ['Digestión',
                                  'Osmorregulación',
                                  'Fotosíntesis',
                                  'Coagulación',
                                  'Respiración celular'],
                 'correcta': 'B'},
                {'pregunta': 'El peso aproximado de cada riñón humano es de:',
                 'alternativas': ['1000 gramos',
                                  '50 gramos',
                                  '500 gramos',
                                  '150 gramos',
                                  '10 gramos'],
                 'correcta': 'D'},
                {'pregunta': 'Los riñones se dividen en tres zonas: corteza, '
                             'médula y:',
                 'alternativas': ['Cápsula',
                                  'Uréter',
                                  'Pelvis renal',
                                  'Vejiga',
                                  'Uretra'],
                 'correcta': 'C'},
                {'pregunta': 'Las estructuras triangulares de la médula '
                             'renal se llaman pirámides de:',
                 'alternativas': ['Bowman',
                                  'Henle',
                                  'Wolff',
                                  'Golgi',
                                  'Malpighi'],
                 'correcta': 'E'},
                {'pregunta': 'La unidad estructural y funcional del riñón es '
                             'la:',
                 'alternativas': ['Médula renal',
                                  'Pelvis renal',
                                  'Nefrona',
                                  'Pirámide renal',
                                  'Cápsula renal'],
                 'correcta': 'C'},
                {'pregunta': 'Cada riñón tiene aproximadamente un número de '
                             'nefronas de:',
                 'alternativas': ['10 000',
                                  '1 000 000',
                                  '100 000 000',
                                  '100',
                                  '1 000'],
                 'correcta': 'B'},
                {'pregunta': 'La cápsula de Bowman contiene en su interior '
                             'al:',
                 'alternativas': ['Túbulo contorneado',
                                  'Asa de Henle exclusiva',
                                  'Cáliz renal',
                                  'Glomérulo de Malpighi',
                                  'Uréter'],
                 'correcta': 'D'},
                {'pregunta': 'El túbulo de la nefrona se divide en túbulo '
                             'contorneado proximal, asa de Henle y:',
                 'alternativas': ['Pelvis renal',
                                  'Cápsula de Bowman',
                                  'Túbulo contorneado distal',
                                  'Uréter',
                                  'Glomérulo'],
                 'correcta': 'C'},
                {'pregunta': 'La orina se forma mediante tres procesos: '
                             'filtración, secreción y:',
                 'alternativas': ['Excreción',
                                  'Digestión',
                                  'Reabsorción',
                                  'Coagulación',
                                  'Fermentación'],
                 'correcta': 'C'},
                {'pregunta': 'En el proceso de filtración, las proteínas y '
                             'células sanguíneas:',
                 'alternativas': ['Se transforman en urea',
                                  'Se destruyen completamente',
                                  'No atraviesan los capilares glomerulares',
                                  'Forman parte de la orina final',
                                  'Atraviesan libremente los capilares'],
                 'correcta': 'C'},
                {'pregunta': 'En el proceso de reabsorción, el porcentaje '
                             'del filtrado que regresa a la sangre es '
                             'aproximadamente:',
                 'alternativas': ['50%', '10%', 'Más del 90%', '100%', '25%'],
                 'correcta': 'C'},
                {'pregunta': 'La glándula salival más voluminosa, situada '
                             'posterior a la rama de la mandíbula, es la:',
                 'alternativas': ['Submandibular',
                                  'Sublingual',
                                  'Parótida',
                                  'Labial',
                                  'Lingual'],
                 'correcta': 'C',
                 'fuente': None},
                {'pregunta': 'La cantidad de saliva secretada diariamente '
                             'oscila entre 1000 y:',
                 'alternativas': ['800 ml',
                                  '1500 ml',
                                  '500 ml',
                                  '2500 ml',
                                  '3000 ml'],
                 'correcta': 'B'},
                {'pregunta': 'La enzima presente en la saliva que inicia la '
                             'digestión de carbohidratos es la:',
                 'alternativas': ['Pepsina',
                                  'Amilasa',
                                  'Maltasa',
                                  'Lipasa',
                                  'Tripsina'],
                 'correcta': 'B'},
                {'pregunta': 'El hígado se divide en dos lóbulos, derecho e '
                             'izquierdo, separados por el ligamento:',
                 'alternativas': ['Hepatoduodenal',
                                  'Coronario',
                                  'Redondo',
                                  'Triangular',
                                  'Falciforme'],
                 'correcta': 'E'},
                {'pregunta': 'Además de producir bilis, el hígado produce el '
                             'anticoagulante:',
                 'alternativas': ['Protrombina',
                                  'Heparina',
                                  'Plasmina',
                                  'Fibrinógeno',
                                  'Trombina'],
                 'correcta': 'B'},
                {'pregunta': 'El hígado transforma el exceso de '
                             'monosacáridos y los almacena en forma de:',
                 'alternativas': ['Ácidos grasos libres',
                                  'Aminoácidos',
                                  'Urea',
                                  'Glucógeno',
                                  'Colesterol'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano que almacena la bilis elaborada en '
                             'el hígado se llama:',
                 'alternativas': ['Conducto cístico',
                                  'Páncreas',
                                  'Colédoco',
                                  'Duodeno',
                                  'Vesícula biliar'],
                 'correcta': 'E'},
                {'pregunta': 'El conducto biliar principal, que conduce la '
                             'bilis hasta el duodeno, se llama conducto:',
                 'alternativas': ['Colédoco',
                                  'Hepático',
                                  'Pancreático',
                                  'Wirsung',
                                  'Cístico'],
                 'correcta': 'A'},
                {'pregunta': 'Las partes del páncreas son cabeza, cuerpo, '
                             'cuello y:',
                 'alternativas': ['Cola',
                                  'Base',
                                  'Ápice',
                                  'Istmo',
                                  'Vértice'],
                 'correcta': 'A'},
                {'pregunta': 'Como glándula endocrina, el páncreas regula el '
                             'metabolismo de glúcidos mediante insulina y:',
                 'alternativas': ['Somatostatina',
                                  'Gastrina',
                                  'Colecistoquinina',
                                  'Secretina',
                                  'Glucagón'],
                 'correcta': 'E'},
                {'pregunta': 'La secreción exocrina del páncreas, el jugo '
                             'pancreático, es regulada por la hormona:',
                 'alternativas': ['Glucagón',
                                  'Insulina',
                                  'Secretina',
                                  'Adrenalina',
                                  'Gastrina'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema circulatorio de los vertebrados se '
                             'caracteriza por ser:',
                 'alternativas': ['Discontinuo',
                                  'Ausente en peces',
                                  'Cerrado',
                                  'Abierto',
                                  'Mixto'],
                 'correcta': 'C'},
                {'pregunta': 'Los peces tienen un corazón compuesto por una '
                             'aurícula y un ventrículo, con circulación:',
                 'alternativas': ['Doble y completa',
                                  'Simple e incompleta',
                                  'Simple y completa',
                                  'Doble e incompleta',
                                  'Triple'],
                 'correcta': 'C'},
                {'pregunta': 'En los anfibios, el corazón tiene dos '
                             'aurículas y un ventrículo, donde se mezcla la '
                             'sangre arterial con la:',
                 'alternativas': ['Linfa',
                                  'Orina',
                                  'Oxigenada exclusiva',
                                  'Bilis',
                                  'Venosa'],
                 'correcta': 'E'},
                {'pregunta': 'Los reptiles presentan dos aurículas y dos '
                             'ventrículos con un tabique interventricular:',
                 'alternativas': ['Triple',
                                  'Incompleto, excepto en cocodrilos',
                                  'Ausente',
                                  'Doble',
                                  'Completo en todos los casos'],
                 'correcta': 'B'},
                {'pregunta': 'Las aves tienen circulación doble y completa, '
                             'y son animales:',
                 'alternativas': ['Anaerobios',
                                  'Poiquilotermos',
                                  'Heterotermos exclusivos',
                                  'Ectotermos',
                                  'Endotermos'],
                 'correcta': 'E'},
                {'pregunta': 'En los mamíferos, las dos aurículas y dos '
                             'ventrículos del corazón están:',
                 'alternativas': ['Parcialmente unidos',
                                  'Conectados por un seno venoso',
                                  'Fusionados',
                                  'Ausentes en el lado derecho',
                                  'Completamente separados'],
                 'correcta': 'E'},
                {'pregunta': 'Los vasos sanguíneos que llevan la sangre del '
                             'cuerpo hacia el corazón se llaman:',
                 'alternativas': ['Arterias',
                                  'Arteriolas',
                                  'Venas',
                                  'Capilares',
                                  'Vénulas exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'Las estructuras que impiden que la sangre '
                             'descienda por su propio peso en las venas se '
                             'llaman:',
                 'alternativas': ['Tabiques',
                                  'Membranas',
                                  'Cuerdas tendinosas',
                                  'Válvulas',
                                  'Esfínteres'],
                 'correcta': 'D'},
                {'pregunta': 'Los vasos que llevan la sangre con oxígeno a '
                             'presión desde el corazón hacia el cuerpo se '
                             'llaman:',
                 'alternativas': ['Venas',
                                  'Capilares',
                                  'Sinusoides',
                                  'Vénulas',
                                  'Arterias'],
                 'correcta': 'E'},
                {'pregunta': 'Los vasos microscópicos que unen las venas con '
                             'las arterias, formados por una sola capa '
                             'endotelial, se llaman:',
                 'alternativas': ['Arteriolas',
                                  'Vénulas',
                                  'Capilares',
                                  'Anastomosis',
                                  'Sinusoides'],
                 'correcta': 'C'},
                {'pregunta': 'La circulación que envía sangre oxigenada por '
                             'todo el cuerpo y retorna la sangre venosa al '
                             'corazón se llama circulación:',
                 'alternativas': ['Coronaria exclusiva',
                                  'Fetal',
                                  'Menor o pulmonar',
                                  'Portal',
                                  'Mayor o general'],
                 'correcta': 'E'},
                {'pregunta': 'La circulación que envía la sangre venosa a '
                             'los pulmones y recoge el oxígeno se llama '
                             'circulación:',
                 'alternativas': ['Portal',
                                  'Mayor o general',
                                  'Menor o pulmonar',
                                  'Sistémica',
                                  'Coronaria'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema encargado de la defensa del '
                             'organismo, integrado por una red de capilares '
                             'por donde circula la linfa, se llama sistema:',
                 'alternativas': ['Endocrino',
                                  'Circulatorio',
                                  'Linfático',
                                  'Excretor',
                                  'Digestivo'],
                 'correcta': 'C'},
                {'pregunta': 'Los órganos que actúan como filtro del sistema '
                             'linfático, eliminando partículas extrañas, se '
                             'llaman:',
                 'alternativas': ['Ganglios linfáticos',
                                  'Alveolos',
                                  'Riñones',
                                  'Hepatocitos',
                                  'Nefronas'],
                 'correcta': 'A'},
                {'pregunta': 'En las aves, la dilatación del esófago donde '
                             'se almacena y humedece el alimento se llama:',
                 'alternativas': ['Buche',
                                  'Ventrículo',
                                  'Molleja',
                                  'Duodeno',
                                  'Cloaca'],
                 'correcta': 'A'},
                {'pregunta': 'En las aves, el órgano muy musculoso que '
                             'machaca el alimento con ayuda de piedras se '
                             'llama:',
                 'alternativas': ['Buche',
                                  'Molleja',
                                  'Esófago',
                                  'Cloaca',
                                  'Estómago glandular'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'EL SISTEMA RESPIRATORIO HUMANO / DIVISIÓN '
                                'FISIOLÓGICA DEL APARATO RESPIRATO',
                      'items': ['El hombre es un ser de respiración aerobia: '
                                'requiere aporte continuo de oxígeno para '
                                'sus células.',
                                'La porción conductora conduce el aire '
                                'inspirado y espirado; comprende nariz, '
                                'faringe, laringe, tráquea y bronquios.',
                                'El interior de la nariz se divide en dos '
                                'cavidades nasales separadas por el tabique '
                                'nasal.']},
                     {'titulo': 'LA DIGESTIÓN: CONCEPTO Y TIPOS / SISTEMA '
                                'DIGESTIVO EN INVERTEBRADOS (+1)',
                      'items': ['El alimento sirve como combustible para '
                                'energía y como fuente de sustancias para '
                                'crecimiento y regeneración.',
                                'Los poríferos, como las esponjas, no tienen '
                                'boca; filtran agua a través de poros para '
                                'obtener alimento y oxígeno.',
                                'En las aves, el esófago presenta una amplia '
                                'dilatación llamada buche, donde se almacena '
                                'y humedece el alimento.']},
                     {'titulo': 'SISTEMA DIGESTIVO HUMANO: ÓRGANOS / '
                                'HISTOLOGÍA DEL TUBO DIGESTIVO (+1)',
                      'items': ['El tubo digestivo, o tracto '
                                'gastrointestinal, incluye boca, faringe, '
                                'esófago, estómago, intestino delgado y '
                                'grueso.',
                                'Las cuatro capas del tubo digestivo, de '
                                'adentro hacia afuera, son: mucosa, '
                                'submucosa, muscular y serosa.',
                                'La cavidad bucal se divide en vestíbulo '
                                'bucal y cavidad oral propiamente dicha.']},
                     {'titulo': 'GLÁNDULAS SALIVALES / EL HÍGADO (+1)',
                      'items': ['Las glándulas salivales menores están '
                                'diseminadas por toda la mucosa bucal: '
                                'palatinas, labiales, bucales y linguales.',
                                'El hígado, o hepar, es la glándula más '
                                'voluminosa anexa al aparato digestivo; pesa '
                                'alrededor de 1,4 kilos en un adulto.',
                                'El páncreas es una glándula de secreción '
                                'externa e interna, unida al duodeno por sus '
                                'conductos excretores.']},
                     {'titulo': 'SISTEMA CIRCULATORIO: TIPOS / CIRCULACIÓN '
                                'EN INVERTEBRADOS (+1)',
                      'items': ['Las partes principales del sistema '
                                'circulatorio son el corazón, los vasos '
                                'sanguíneos y la sangre.',
                                'Los poríferos y cnidarios no tienen sistema '
                                'circulatorio; el transporte es por difusión '
                                'simple.',
                                'El sistema circulatorio de los vertebrados '
                                'es cerrado y no presenta senos o lagunas.']},
                     {'titulo': 'LA SANGRE / EL CORAZÓN (+1)',
                      'items': ['El sistema circulatorio también se llama '
                                'cardiovascular: «cardio» (corazón) y '
                                '«vascular» (vasos sanguíneos).',
                                'El corazón bombea sangre entre 60 y 100 '
                                'veces por minuto, ubicado en el mediastino.',
                                'Las venas son vasos de paredes delgadas y '
                                'poco elásticas; llevan la sangre del cuerpo '
                                'hacia el corazón.']},
                     {'titulo': 'CIRCULACIÓN MAYOR Y MENOR / SISTEMA '
                                'LINFÁTICO (+1)',
                      'items': ['La circulación mayor, o general, es la '
                                'circulación de la sangre oxigenada por todo '
                                'el cuerpo y el retorno de la sangre venosa '
                                'hacia el corazón.',
                                'El sistema linfático, o linfoide, es de '
                                'suma importancia en la defensa del '
                                'organismo; está integrado por una red de '
                                'capilares por donde circula la linfa.',
                                'La excreción es el proceso por el cual los '
                                'seres vivos liberan productos de desecho '
                                'del metabolismo.']},
                     {'titulo': 'EXCRECIÓN EN VERTEBRADOS / EL RIÑÓN (+1)',
                      'items': ['Los peces excretan por los riñones y por '
                                'células branquiales especializadas.',
                                'El aparato excretor humano se compone de '
                                'dos riñones y un conjunto de vías '
                                'urinarias.',
                                'La nefrona es la unidad estructural y '
                                'funcional del riñón; cada riñón tiene cerca '
                                'de un millón.']}]},
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
                {'titulo': '9.5 SISTEMA NERVIOSO HUMANO',
                 'items': ['El sistema nervioso humano se divide en {sistema '
                           'nervioso central} (SNC) y sistema nervioso '
                           '{periférico} (SNP).',
                           'El número de neuronas en el cerebro humano ronda '
                           'los {100 000} millones.',
                           'El {SNC} está conformado por el encéfalo y la '
                           '{médula espinal}.',
                           'El {encéfalo} incluye el bulbo raquídeo, la '
                           'protuberancia, el mesencéfalo, el cerebelo, el '
                           'diencéfalo y el cerebro.',
                           'La {médula espinal} transmite señales entre la '
                           'periferia y el cerebro, e interviene en el '
                           '{tacto}.',
                           'Los {nervios} son cordones de sustancia blanca '
                           'formados por axones y dendritas.',
                           'Los nervios {craneales} controlan la cabeza y el '
                           'cuello; los nervios {espinales} se ramifican en '
                           'la columna vertebral.',
                           'Los {ganglios} son estructuras formadas por '
                           'cuerpos de neuronas ubicados fuera del encéfalo '
                           'y la médula.']}],
  'cuadros': [{'titulo': '9.2 SISTEMA NERVIOSO POR GRUPO DE INVERTEBRADOS',
               'encabezados': ['Grupo', 'Sistema nervioso'],
               'filas': [['{Cnidarios}', 'Red difusa de {protoneuronas}'],
                         ['{Platelmintos}',
                          '{Hiponeuro}, primera cefalización'],
                         ['{Artrópodos}',
                          'Metamérico, cerebro con 3 {pares} de ganglios']]}],
  'preguntas': [{'pregunta': 'El sistema nervioso lleva información desde '
                             'los órganos sensoriales hasta:',
                 'alternativas': ['El sistema digestivo',
                                  'Los órganos efectores directamente',
                                  'El sistema excretor',
                                  'El sistema circulatorio',
                                  'Los centros de control'],
                 'correcta': 'E'},
                {'pregunta': 'La unidad funcional básica del sistema '
                             'nervioso es:',
                 'alternativas': ['La célula glial',
                                  'La dendrita exclusivamente',
                                  'La sinapsis exclusivamente',
                                  'El axón exclusivamente',
                                  'La neurona'],
                 'correcta': 'E'},
                {'pregunta': 'Los organismos más sencillos en tener células '
                             'nerviosas son los:',
                 'alternativas': ['Cnidarios',
                                  'Artrópodos',
                                  'Platelmintos',
                                  'Anélidos',
                                  'Nematodos'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema nervioso de los cnidarios se '
                             'caracteriza por ser:',
                 'alternativas': ['Un tubo neural',
                                  'Una red difusa de protoneuronas',
                                  'Muy centralizado',
                                  'Un cerebro complejo',
                                  'Un sistema hiponeuro avanzado'],
                 'correcta': 'B'},
                {'pregunta': 'El primer grupo de animales con sistema '
                             'nervioso hiponeuro son los:',
                 'alternativas': ['Artrópodos',
                                  'Moluscos',
                                  'Cnidarios',
                                  'Vertebrados',
                                  'Platelmintos'],
                 'correcta': 'E'},
                {'pregunta': 'El proceso de concentración de células '
                             'nerviosas en la región anterior del animal se '
                             'llama:',
                 'alternativas': ['Cefalización',
                                  'Neurulación',
                                  'Metamerización',
                                  'Invaginación',
                                  'Segmentación'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema nervioso de los nematodos se '
                             'estructura alrededor de:',
                 'alternativas': ['La médula espinal',
                                  'Ganglios dispersos sin conexión',
                                  'Un anillo nervioso alrededor del esófago',
                                  'Un cerebro complejo',
                                  'Un tubo neural'],
                 'correcta': 'C'},
                {'pregunta': 'Los anélidos presentan un cordón nervioso '
                             'central que se divide, en cada metámero, en:',
                 'alternativas': ['Dos nervios laterales',
                                  'Cuatro nervios',
                                  'Tres nervios',
                                  'Un solo nervio',
                                  'Ningún nervio adicional'],
                 'correcta': 'A'},
                {'pregunta': 'En los cefalópodos, el sistema nervioso '
                             'alcanza una complejidad similar a la de:',
                 'alternativas': ['Los nematodos',
                                  'Ningún otro grupo',
                                  'Los platelmintos',
                                  'Los cnidarios',
                                  'Los vertebrados'],
                 'correcta': 'E'},
                {'pregunta': 'El cerebro de los artrópodos está formado por '
                             'tres pares de ganglios, diferenciados en '
                             'protocerebro, deutocerebro y:',
                 'alternativas': ['Mesocerebro',
                                  'Metacerebro',
                                  'Tritocerebro',
                                  'Endocerebro',
                                  'Ectocerebro'],
                 'correcta': 'C'},
                {'pregunta': 'En los vertebrados, el sistema nervioso se '
                             'forma por invaginación dorsal de:',
                 'alternativas': ['La notocorda exclusiva',
                                  'El endodermo',
                                  'El ectodermo',
                                  'El celoma',
                                  'El mesodermo'],
                 'correcta': 'C'},
                {'pregunta': 'La invaginación dorsal del ectodermo en '
                             'vertebrados da lugar a un cordón hueco '
                             'llamado:',
                 'alternativas': ['Tubo neural',
                                  'Celoma',
                                  'Blastocele',
                                  'Notocorda',
                                  'Arquenterón'],
                 'correcta': 'A'},
                {'pregunta': 'En los vertebrados se diferencian dos regiones '
                             'funcionales del sistema nervioso: el encéfalo '
                             'y:',
                 'alternativas': ['La médula espinal',
                                  'El corazón',
                                  'Los riñones',
                                  'El hígado',
                                  'Los pulmones'],
                 'correcta': 'A'},
                {'pregunta': 'El encéfalo de los vertebrados está protegido '
                             'por:',
                 'alternativas': ['La piel exclusivamente',
                                  'El tejido adiposo',
                                  'La caja craneal',
                                  'Los músculos exclusivamente',
                                  'El canal vertebral'],
                 'correcta': 'C'},
                {'pregunta': 'La médula espinal de los vertebrados está '
                             'protegida por:',
                 'alternativas': ['El diafragma',
                                  'El canal vertebral',
                                  'La piel exclusivamente',
                                  'Las costillas exclusivamente',
                                  'La caja craneal'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso central está formado por '
                             'el encéfalo y:',
                 'alternativas': ['Los ganglios simpáticos',
                                  'Los nervios periféricos',
                                  'Las glándulas endocrinas',
                                  'Los órganos sensoriales',
                                  'La médula espinal'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema nervioso periférico está formado '
                             'por:',
                 'alternativas': ['Los nervios que recorren el organismo',
                                  'Solo el cerebelo',
                                  'Solo el encéfalo',
                                  'Solo el bulbo raquídeo',
                                  'Solo la médula espinal'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema nervioso que regula las funciones '
                             'voluntarias, como el movimiento muscular, se '
                             'llama sistema nervioso:',
                 'alternativas': ['Entérico',
                                  'Autónomo',
                                  'Somático',
                                  'Parasimpático exclusivo',
                                  'Simpático exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema nervioso que controla las funciones '
                             'inconscientes del organismo se llama sistema '
                             'nervioso:',
                 'alternativas': ['Central exclusivo',
                                  'Periférico exclusivo',
                                  'Somático',
                                  'Autónomo o vegetativo',
                                  'Motor exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'Además de la neurona, otro componente '
                             'importante del sistema nervioso, aunque no '
                             'todos los animales lo poseen, son:',
                 'alternativas': ['Los osteocitos',
                                  'Los plaquetas',
                                  'Los linfocitos',
                                  'Los eritrocitos',
                                  'Las células gliales'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema nervioso humano se divide en '
                             'sistema nervioso central y sistema nervioso:',
                 'alternativas': ['Somático exclusivo',
                                  'Periférico',
                                  'Voluntario',
                                  'Simpático exclusivo',
                                  'Autónomo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El número de neuronas en el cerebro humano '
                             'ronda aproximadamente:',
                 'alternativas': ['1 millón',
                                  '10 000 millones',
                                  '100 millones',
                                  '1000 millones',
                                  '100 000 millones'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema nervioso central está conformado '
                             'por el encéfalo y:',
                 'alternativas': ['Los ganglios',
                                  'La médula espinal',
                                  'Los nervios periféricos',
                                  'Los músculos',
                                  'Las neuronas motoras'],
                 'correcta': 'B'},
                {'pregunta': 'El encéfalo incluye el bulbo raquídeo, la '
                             'protuberancia, el mesencéfalo, el cerebelo, el '
                             'diencéfalo y:',
                 'alternativas': ['Los nervios craneales',
                                  'La médula espinal',
                                  'El cerebro',
                                  'Los nervios espinales',
                                  'Los ganglios'],
                 'correcta': 'C'},
                {'pregunta': 'La médula espinal interviene en la transmisión '
                             'del tacto y de señales:',
                 'alternativas': ['Solo auditivas',
                                  'Solo olfativas',
                                  'Sensitivas de músculos y articulaciones',
                                  'Solo visuales',
                                  'Solo gustativas'],
                 'correcta': 'C'},
                {'pregunta': 'Los nervios son cordones de sustancia blanca '
                             'formados por axones y:',
                 'alternativas': ['Lisosomas exclusivos',
                                  'Núcleos',
                                  'Ribosomas exclusivos',
                                  'Mitocondrias exclusivas',
                                  'Dendritas'],
                 'correcta': 'E'},
                {'pregunta': 'Los nervios que se localizan en la cabeza y '
                             'controlan sus funciones se llaman nervios:',
                 'alternativas': ['Autónomos exclusivos',
                                  'Periféricos exclusivos',
                                  'Craneales',
                                  'Espinales',
                                  'Somáticos exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'Los nervios ramificados en pares en las '
                             'vértebras de la columna se llaman nervios:',
                 'alternativas': ['Espinales',
                                  'Autónomos exclusivos',
                                  'Craneales',
                                  'Cerebrales exclusivos',
                                  'Centrales exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Las estructuras formadas por cuerpos de '
                             'neuronas ubicados fuera del encéfalo y la '
                             'médula se llaman:',
                 'alternativas': ['Dendritas',
                                  'Ganglios',
                                  'Axones',
                                  'Sinapsis',
                                  'Nervios'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso humano funciona, en '
                             'conjunto, como un ente que:',
                 'alternativas': ['Solo digiere alimentos',
                                  'Solo produce hormonas',
                                  'Solo transporta oxígeno',
                                  'Organiza, controla y coordina las '
                                  'funciones corporales',
                                  'Solo filtra la sangre'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'EL SISTEMA NERVIOSO EN ANIMALES',
                      'items': ['El sistema nervioso lleva información desde '
                                'los órganos sensoriales hasta los centros '
                                'de control, generando una respuesta.']},
                     {'titulo': 'SISTEMA NERVIOSO EN INVERTEBRADOS',
                      'items': ['Los cnidarios son los organismos más '
                                'sencillos con células nerviosas: una red '
                                'difusa de protoneuronas.']},
                     {'titulo': 'SISTEMA NERVIOSO EN VERTEBRADOS',
                      'items': ['El sistema nervioso de los vertebrados se '
                                'forma por invaginación dorsal del '
                                'ectodermo, dando lugar al tubo neural.']},
                     {'titulo': 'TIPOS DE SISTEMA NERVIOSO',
                      'items': ['El sistema nervioso central consiste en el '
                                'encéfalo y la médula espinal; el '
                                'periférico, en los nervios que recorren el '
                                'cuerpo.']},
                     {'titulo': 'SISTEMA NERVIOSO HUMANO',
                      'items': ['El sistema nervioso humano se divide en '
                                'sistema nervioso central (SNC) y sistema '
                                'nervioso periférico (SNP).']}]},
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
                {'titulo': '10.4 EL CICLO CELULAR',
                 'items': ['El {ciclo celular} es la sucesión de etapas en '
                           'que una célula alterna entre crecimiento y '
                           '{división} a lo largo de su vida.',
                           'En células somáticas, el ciclo celular comprende '
                           'la {interfase} y la división por {mitosis}, '
                           'dando dos células hijas diploides idénticas.',
                           'Una célula humana típica puede dividirse en {24} '
                           'horas; de este tiempo, la fase M ocupa menos de '
                           'una {hora}.',
                           'La fase {S} ocupa alrededor de 10 a 12 horas, '
                           'aproximadamente la mitad del ciclo celular.',
                           'La mitosis y citocinesis transcurren en menos de '
                           'una hora, aproximadamente el {5}% del ciclo; el '
                           'resto la célula permanece en {interfase}.',
                           'El ciclo celular se divide en dos etapas '
                           'principales: la {interfase} (fases G1, S y G2), '
                           'y la división celular o fase {M}.',
                           'Existen puntos de control del ciclo celular en '
                           'las fases {G1}, S, G2 y M.']},
                {'titulo': '10.5 LA INTERFASE Y SUS ETAPAS',
                 'items': ['La {interfase} es el período entre dos '
                           'divisiones celulares consecutivas, en el que la '
                           'célula permanece hasta el {95}% del tiempo.',
                           'Durante la interfase ocurre la duplicación del '
                           '{ADN}, síntesis de histonas, y producción de '
                           'organelos para las células hijas.',
                           'En interfase, los cromosomas permanecen '
                           'descondensados en el núcleo, constituyendo la '
                           '{cromatina}.',
                           'La fase {G1} es un período de crecimiento '
                           'general y duplicación de organelos '
                           'citoplasmáticos.',
                           'En el punto de control {G1}, la célula decide si '
                           'se divide o no, según encuentre los factores '
                           'necesarios para pasar a la fase {S}.',
                           'Si no recibe la señal de continuación en G1, la '
                           'célula puede entrar en una fase de no división '
                           'llamada {G0}.',
                           'La fase {S}, o de síntesis, es cuando se realiza '
                           'la duplicación o síntesis del {ADN}.',
                           'La fase {G2}, segunda fase de intervalo, prepara '
                           'a la célula para la división {nuclear}.']},
                {'titulo': '10.6 LA MITOSIS: CONCEPTO Y FASES',
                 'items': ['La {mitosis} es un proceso de división nuclear, '
                           'o {cariocinesis}, que reparte el ADN replicado.',
                           'La mitosis asegura que cada célula posea el '
                           '{mismo} número y tipo de cromosomas que las '
                           'demás.',
                           'La mitosis es la base del {crecimiento} corporal '
                           'y la reparación de {tejidos} en eucariontes '
                           'pluricelulares.',
                           'La mitosis dura entre {30} y 60 minutos, y tiene '
                           '4 fases: profase, metafase, anafase y '
                           '{telofase}.',
                           'En la {profase}, se condensan los cromosomas '
                           'duplicados y se forma el {huso} mitótico a '
                           'partir del centrosoma.',
                           'En la profase, una estructura proteica llamada '
                           '{cinetocoro} se ensambla en el centrómero de '
                           'cada cromátide.',
                           'Al final de la profase, la {envoltura nuclear} '
                           'se desintegra y los nucléolos desaparecen.',
                           'En la {metafase}, los cromosomas se alinean en '
                           'el ecuador de la célula, formando la placa '
                           '{metafásica}.',
                           'En la metafase, el ADN alcanza su {máximo} grado '
                           'de condensación.',
                           'En la {anafase}, los centrómeros se separan y '
                           'las cromátidas hermanas son atraídas hacia polos '
                           '{opuestos}.',
                           'En la mayoría de células animales, el primer '
                           'indicio de {citocinesis} aparece durante la '
                           'anafase.',
                           'En la {telofase}, los microtúbulos del huso se '
                           'desintegran y se forma una nueva envoltura '
                           '{nuclear} en cada grupo de cromosomas.']},
                {'titulo': '10.7 LA CITOCINESIS',
                 'items': ['La {citocinesis} es el proceso de división del '
                           'citoplasma, que reparte el contenido '
                           'citoplasmático y los {organelos}.',
                           'La citocinesis ocurre principalmente durante la '
                           '{telofase}, dividiendo la célula en dos partes '
                           'casi {iguales}.',
                           'En células {animales}, la membrana se constriñe '
                           'por un surco de segmentación, formado por un '
                           'anillo contráctil de {actina} y miosina.',
                           'En células {vegetales}, no existe surco de '
                           'segmentación; en su lugar se forma una {placa '
                           'celular} a partir de vesículas del aparato de '
                           'Golgi.',
                           'En células vegetales, la placa celular se '
                           'impregna de {pectinas} y forma la lámina '
                           '{media}, dando origen a la nueva pared '
                           'celular.']},
                {'titulo': '10.8 LA MEIOSIS',
                 'items': ['La {meiosis} consiste en dos divisiones '
                           'celulares sucesivas, que reducen el número de '
                           'cromosomas a la {mitad}.',
                           'Los cromosomas iguales que se emparejan durante '
                           'la meiosis se llaman cromosomas {homólogos}.',
                           'El número {haploide} (n) tiene una serie de cada '
                           'cromosoma; el {diploide} (2n) tiene dos series.',
                           'En el ser humano, el número haploide es {23} y '
                           'el diploide es {46}.',
                           'Los {gametos} (óvulos y espermatozoides) llevan '
                           'el número haploide.',
                           'Solo las dos últimas divisiones que producen '
                           'gametos son {meióticas}; las demás son '
                           '{mitóticas}.',
                           'En el {paquinema}, ocurre el intercambio de '
                           'segmentos entre cromátidas homólogas, llamado '
                           '{recombinación genética} o crossing over.',
                           'Cada par de cromosomas apareados se llama '
                           '{bivalente} o tétrada, por tener cuatro '
                           '{cromátidas}.',
                           'Las conexiones donde ocurrió el intercambio '
                           'genético se llaman {quiasmas}.']},
                {'titulo': '10.9 REPRODUCCIÓN SEXUAL: CONCEPTO Y FECUNDACIÓN',
                 'items': ['La reproducción {sexual} implica la fusión de '
                           'dos {gametos} y la mezcla de sus materiales '
                           'genéticos.',
                           'La reproducción sexual promueve la {variabilidad '
                           'genética}, base de la evolución biológica.',
                           'La unión de dos gametos se llama {fecundación}, '
                           'y forma un {cigoto} diploide.',
                           'La fecundación {externa} ocurre en el agua, en '
                           'invertebrados acuáticos y peces.',
                           'La fecundación {interna} ocurre dentro del '
                           'cuerpo de la hembra, en la mayoría de animales '
                           'terrestres.']},
                {'titulo': '10.10 GAMETOS Y TIPOS DE ORGANISMOS SEGÚN SU '
                           'SEXO',
                 'items': ['Los gametos masculinos, pequeños, se llaman '
                           '{espermatozoides}; los femeninos, más grandes, '
                           'se llaman {óvulos}.',
                           'Los espermatozoides se producen en los '
                           '{testículos}; los óvulos, en los {ovarios}.',
                           'Los organismos {monoicos}, o hermafroditas, '
                           'tienen órganos reproductivos masculinos y '
                           'femeninos a la vez.',
                           'Los hermafroditas {simultáneos} producen óvulos '
                           'y espermatozoides al mismo tiempo, como la '
                           'tenia.',
                           'Los hermafroditas {secuenciales} cambian de sexo '
                           'durante su vida; si nacen macho, se llaman '
                           '{protándricos}.',
                           'Los organismos {dioicos}, o unisexuales, tienen '
                           'sexos separados, como la mayoría de los '
                           'vertebrados.']}],
  'cuadros': [{'titulo': '10.2 TIPOS DE REPRODUCCIÓN ASEXUAL',
               'encabezados': ['Tipo', 'Ejemplo'],
               'filas': [['{Escisión binaria}', '{Paramecium}, Euglena'],
                         ['{Gemación}', '{Hidra}, esponjas'],
                         ['{Esporulación}', '{Plasmodium}'],
                         ['{Fragmentación}', '{Planaria}, estrella de mar']]},
              {'titulo': 'CITOCINESIS: CÉLULA ANIMAL FRENTE A VEGETAL',
               'despues_de': '10.7 LA CITOCINESIS',
               'encabezados': ['Célula animal', 'Célula vegetal'],
               'filas': [['Se forma un surco de {segmentación}',
                          'Se forma una {placa} celular'],
                         ['Interviene un anillo de {actina} y miosina',
                          'Intervienen vesículas del {Golgi}'],
                         ['La célula se {estrangula} hasta separarse',
                          'La placa crece hasta fusionarse con la '
                          '{membrana}'],
                         ['No forma pared celular nueva',
                          'Se forma una nueva {pared} celular de '
                          'celulosa']]}],
  'preguntas': [{'pregunta': 'En la reproducción asexual interviene:',
                 'alternativas': ['Dos organismos',
                                  'Ningún organismo',
                                  'Solo gametos masculinos',
                                  'Solo gametos femeninos',
                                  'Un solo organismo'],
                 'correcta': 'E'},
                {'pregunta': 'La descendencia producida por reproducción '
                             'asexual es, respecto al progenitor:',
                 'alternativas': ['Siempre mutada',
                                  'Parcialmente similar solamente',
                                  'Genéticamente idéntica',
                                  'Genéticamente diferente',
                                  'Sin ninguna relación genética'],
                 'correcta': 'C'},
                {'pregunta': 'En la reproducción asexual participan células '
                             'de tipo:',
                 'alternativas': ['Sexuales o gametos',
                                  'Solo espermatozoides',
                                  'Somáticas',
                                  'Ninguna célula específica',
                                  'Solo óvulos'],
                 'correcta': 'C'},
                {'pregunta': 'La escisión binaria se da por una '
                             'estrangulación en:',
                 'alternativas': ['Ningún punto específico',
                                  'El plano medio del organismo',
                                  'El núcleo exclusivamente',
                                  'La membrana externa solamente',
                                  'El polo de la célula'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria transversal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Hidra',
                                  'Paramecium',
                                  'Plasmodium',
                                  'Planaria',
                                  'Euglena'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria longitudinal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Estrella de mar',
                                  'Hidra',
                                  'Euglena o Astasia',
                                  'Plasmodium',
                                  'Paramecium'],
                 'correcta': 'C'},
                {'pregunta': 'La formación de una yema o botón que se rodea '
                             'de citoplasma se llama:',
                 'alternativas': ['Fragmentación',
                                  'Esporulación',
                                  'Gemación',
                                  'Escisión binaria',
                                  'Autotomía'],
                 'correcta': 'C'},
                {'pregunta': 'La gemación ocurre, entre otros organismos, en '
                             'poríferos y:',
                 'alternativas': ['Reptiles',
                                  'Celentéreos',
                                  'Aves',
                                  'Mamíferos',
                                  'Peces'],
                 'correcta': 'B'},
                {'pregunta': 'Una forma especial de gemación, presente en '
                             'medusas y céstodos, se llama:',
                 'alternativas': ['Autotomía',
                                  'Estrobilación',
                                  'Bipartición',
                                  'Esporulación',
                                  'Fragmentación'],
                 'correcta': 'B'},
                {'pregunta': 'La esporulación consiste en divisiones '
                             'mitóticas del núcleo que finalmente liberan:',
                 'alternativas': ['Yemas',
                                  'Gametos',
                                  'Larvas',
                                  'Esporas',
                                  'Fragmentos'],
                 'correcta': 'D'},
                {'pregunta': 'El Plasmodium, agente causante de la malaria, '
                             'se reproduce por:',
                 'alternativas': ['Esporulación',
                                  'Escisión binaria',
                                  'Autotomía',
                                  'Fragmentación',
                                  'Gemación'],
                 'correcta': 'A'},
                {'pregunta': 'La escisión del progenitor en dos o más '
                             'partes, cada una capaz de originar un nuevo '
                             'animal, se llama:',
                 'alternativas': ['Fragmentación',
                                  'Estrobilación',
                                  'Esporulación',
                                  'Bipartición',
                                  'Gemación'],
                 'correcta': 'A'},
                {'pregunta': 'La fragmentación se observa, por ejemplo, en '
                             'estrellas de mar y:',
                 'alternativas': ['Peces óseos',
                                  'Mamíferos',
                                  'Aves',
                                  'Reptiles',
                                  'Planarias'],
                 'correcta': 'E'},
                {'pregunta': 'El fenómeno por el cual un crustáceo o lagarto '
                             'desprende un apéndice o la cola ante el '
                             'peligro se llama:',
                 'alternativas': ['Escisión',
                                  'Esporulación',
                                  'Gemación',
                                  'Autotomía',
                                  'Fragmentación'],
                 'correcta': 'D'},
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
                 'alternativas': ['Perpetuar su propia especie',
                                  'Emitir luz',
                                  'Cambiar de color',
                                  'Moverse',
                                  'Producir sonidos'],
                 'correcta': 'A'},
                {'pregunta': 'En organismos eucariotas existen dos tipos de '
                             'división celular: mitosis y:',
                 'alternativas': ['Fragmentación',
                                  'Escisión binaria',
                                  'Gemación',
                                  'Meiosis',
                                  'Esporulación'],
                 'correcta': 'D'},
                {'pregunta': 'La división celular que produce células '
                             'genéticamente idénticas a la célula madre es:',
                 'alternativas': ['La mitosis',
                                  'La esporulación',
                                  'La gemación',
                                  'La fragmentación',
                                  'La meiosis'],
                 'correcta': 'A'},
                {'pregunta': 'La división celular que produce células con la '
                             'mitad del contenido genético de la célula '
                             'madre es:',
                 'alternativas': ['La gemación',
                                  'La meiosis',
                                  'La fragmentación',
                                  'La mitosis',
                                  'La escisión binaria'],
                 'correcta': 'B'},
                {'pregunta': 'Rudolf Virchow resumió el concepto de '
                             'continuidad celular con el axioma en latín:',
                 'alternativas': ['Ad astra per aspera',
                                  'Omnis cellula e cellula',
                                  'Carpe diem',
                                  'Cogito ergo sum',
                                  'In vino veritas'],
                 'correcta': 'B'},
                {'pregunta': 'La meiosis consiste en un par de divisiones '
                             'celulares que reducen el número de cromosomas '
                             'a:',
                 'alternativas': ['La mitad',
                                  'El triple',
                                  'Ninguna reducción',
                                  'Un cuarto',
                                  'El doble'],
                 'correcta': 'A'},
                {'pregunta': 'Los cromosomas iguales que se emparejan '
                             'durante la meiosis se llaman cromosomas:',
                 'alternativas': ['Acéntricos',
                                  'Sexuales exclusivos',
                                  'Homólogos',
                                  'Satélite',
                                  'Autosomas exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'El número haploide del ser humano es:',
                 'alternativas': ['22', '44', '46', '48', '23'],
                 'correcta': 'E'},
                {'pregunta': 'El número diploide del ser humano es:',
                 'alternativas': ['24', '44', '23', '46', '22'],
                 'correcta': 'D'},
                {'pregunta': 'Los gametos humanos (óvulos y espermatozoides) '
                             'llevan el número:',
                 'alternativas': ['Ninguno definido',
                                  'Triploide',
                                  'Tetraploide',
                                  'Diploide',
                                  'Haploide'],
                 'correcta': 'E'},
                {'pregunta': 'El intercambio de segmentos entre cromátidas '
                             'homólogas durante la meiosis se llama:',
                 'alternativas': ['Gemación',
                                  'Esporulación',
                                  'Fecundación',
                                  'Recombinación genética o crossing over',
                                  'Mitosis'],
                 'correcta': 'D'},
                {'pregunta': 'Cada par de cromosomas apareados durante la '
                             'meiosis, con cuatro cromátidas, se llama:',
                 'alternativas': ['Cigoto',
                                  'Haploide',
                                  'Diploide',
                                  'Gameto',
                                  'Bivalente o tétrada'],
                 'correcta': 'E'},
                {'pregunta': 'Las conexiones donde ocurrió el intercambio '
                             'genético en la meiosis se llaman:',
                 'alternativas': ['Telómeros',
                                  'Quiasmas',
                                  'Centrómeros',
                                  'Cinetocoros',
                                  'Nucléolos'],
                 'correcta': 'B'},
                {'pregunta': 'La reproducción sexual implica la fusión de '
                             'dos:',
                 'alternativas': ['Órganos',
                                  'Células somáticas',
                                  'Gametos',
                                  'Embriones',
                                  'Cigotos'],
                 'correcta': 'C'},
                {'pregunta': 'La reproducción sexual promueve principalmente '
                             'la:',
                 'alternativas': ['Clonación exacta',
                                  'Eliminación de mutaciones',
                                  'Reducción de la población',
                                  'Variabilidad genética',
                                  'Identidad genética total'],
                 'correcta': 'D'},
                {'pregunta': 'La unión de dos gametos se llama:',
                 'alternativas': ['Mitosis',
                                  'Esporulación',
                                  'Gemación',
                                  'Meiosis',
                                  'Fecundación'],
                 'correcta': 'E'},
                {'pregunta': 'La fecundación que ocurre en el agua, fuera '
                             'del cuerpo, se llama fecundación:',
                 'alternativas': ['Mixta',
                                  'Interna',
                                  'Asexual',
                                  'Artificial',
                                  'Externa'],
                 'correcta': 'E'},
                {'pregunta': 'La fecundación que ocurre dentro del cuerpo de '
                             'la hembra se llama fecundación:',
                 'alternativas': ['Externa',
                                  'Artificial',
                                  'Mixta',
                                  'Ausente',
                                  'Interna'],
                 'correcta': 'E'},
                {'pregunta': 'Los gametos masculinos, de menor tamaño, se '
                             'llaman:',
                 'alternativas': ['Espermatozoides',
                                  'Ovocitos',
                                  'Cigotos',
                                  'Óvulos',
                                  'Gónadas'],
                 'correcta': 'A'},
                {'pregunta': 'Los espermatozoides se producen en:',
                 'alternativas': ['Las trompas',
                                  'La vagina',
                                  'Los testículos',
                                  'El útero',
                                  'Los ovarios'],
                 'correcta': 'C'},
                {'pregunta': 'Los organismos que tienen órganos '
                             'reproductivos masculinos y femeninos a la vez '
                             'se llaman:',
                 'alternativas': ['Dioicos',
                                  'Unisexuales',
                                  'Monoicos o hermafroditas',
                                  'Ovíparos',
                                  'Partenogenéticos'],
                 'correcta': 'C'},
                {'pregunta': 'Los hermafroditas que producen óvulos y '
                             'espermatozoides al mismo tiempo se llaman '
                             'hermafroditas:',
                 'alternativas': ['Simultáneos',
                                  'Secuenciales',
                                  'Protóginos exclusivos',
                                  'Dioicos',
                                  'Protándricos exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Los hermafroditas que cambian de sexo durante '
                             'su vida se llaman hermafroditas:',
                 'alternativas': ['Asexuales',
                                  'Monoicos puros',
                                  'Secuenciales',
                                  'Simultáneos',
                                  'Dioicos'],
                 'correcta': 'C'},
                {'pregunta': 'Un organismo que nace macho y luego se '
                             'transforma en hembra se llama:',
                 'alternativas': ['Dioico',
                                  'Monoico puro',
                                  'Protándrico',
                                  'Protógino',
                                  'Hermafrodita simultáneo'],
                 'correcta': 'C'},
                {'pregunta': 'Los organismos con sexos separados, como la '
                             'mayoría de los vertebrados, se llaman:',
                 'alternativas': ['Andróginos',
                                  'Hermafroditas',
                                  'Dioicos o unisexuales',
                                  'Partenogenéticos',
                                  'Monoicos'],
                 'correcta': 'C'},
                {'pregunta': 'El ciclo celular en células somáticas '
                             'comprende la interfase y la división por:',
                 'alternativas': ['Esporulación',
                                  'Fisión binaria',
                                  'Gemación',
                                  'Mitosis',
                                  'Meiosis'],
                 'correcta': 'D'},
                {'pregunta': 'Una célula humana típica puede completar su '
                             'ciclo celular en aproximadamente:',
                 'alternativas': ['6 horas',
                                  '24 horas',
                                  '12 horas',
                                  '48 horas',
                                  '72 horas'],
                 'correcta': 'B'},
                {'pregunta': 'La fase del ciclo celular que ocupa '
                             'aproximadamente la mitad del tiempo total, '
                             'dedicada a la síntesis de ADN, es la fase:',
                 'alternativas': ['G2', 'M', 'G1', 'G0', 'S'],
                 'correcta': 'E'},
                {'pregunta': 'La mitosis y la citocinesis transcurren en '
                             'menos de una hora, representando '
                             'aproximadamente qué porcentaje del ciclo '
                             'celular:',
                 'alternativas': ['95%', '75%', '50%', '25%', '5%'],
                 'correcta': 'E'},
                {'pregunta': 'La célula permanece en interfase '
                             'aproximadamente qué porcentaje del tiempo del '
                             'ciclo celular:',
                 'alternativas': ['50%', '5%', '95%', '75%', '25%'],
                 'correcta': 'C'},
                {'pregunta': 'La interfase se divide en tres fases, '
                             'denominadas:',
                 'alternativas': ['Alfa, beta y gamma',
                                  'Inicial, media y final',
                                  'Profase, metafase y anafase',
                                  'Mitosis, meiosis y citocinesis',
                                  'G1, S y G2'],
                 'correcta': 'E'},
                {'pregunta': 'Durante la interfase, los cromosomas '
                             'permanecen descondensados en el núcleo, '
                             'constituyendo la:',
                 'alternativas': ['Lámina media',
                                  'Cromatina',
                                  'Cariocinesis',
                                  'Placa metafásica',
                                  'Cinetocoro'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de crecimiento general y duplicación '
                             'de organelos citoplasmáticos, previa a la '
                             'síntesis de ADN, se llama fase:',
                 'alternativas': ['G2', 'G1', 'G0', 'S', 'M'],
                 'correcta': 'B'},
                {'pregunta': 'Si en el punto de control G1 la célula no '
                             'recibe la señal de continuación, puede entrar '
                             'en una fase de no división llamada:',
                 'alternativas': ['Telofase', 'G2', 'S', 'M', 'G0'],
                 'correcta': 'E'},
                {'pregunta': 'La fase en la que se realiza la duplicación o '
                             'síntesis del ADN se llama fase:',
                 'alternativas': ['S', 'G0', 'G2', 'G1', 'M'],
                 'correcta': 'A'},
                {'pregunta': 'La mitosis es básicamente un proceso de '
                             'división nuclear, también llamado:',
                 'alternativas': ['Meiosis I',
                                  'Sinapsis',
                                  'Cariocinesis',
                                  'Citocinesis',
                                  'Interfase'],
                 'correcta': 'C'},
                {'pregunta': 'La mitosis es la base del crecimiento corporal '
                             'y de la:',
                 'alternativas': ['Reparación de tejidos',
                                  'Variabilidad genética',
                                  'Recombinación',
                                  'Fecundación',
                                  'Formación de gametos'],
                 'correcta': 'A'},
                {'pregunta': 'La mitosis, como proceso continuo, dura '
                             'aproximadamente entre 30 y:',
                 'alternativas': ['45 minutos',
                                  '20 minutos',
                                  '120 minutos',
                                  '60 minutos',
                                  '90 minutos'],
                 'correcta': 'D'},
                {'pregunta': 'Las cuatro fases de la mitosis, en orden, son '
                             'profase, metafase, anafase y:',
                 'alternativas': ['Citocinesis',
                                  'Telofase',
                                  'Interfase',
                                  'G2',
                                  'Sinapsis'],
                 'correcta': 'B'},
                {'pregunta': 'En la profase, la estructura proteica que se '
                             'ensambla en el centrómero de cada cromátide se '
                             'llama:',
                 'alternativas': ['Cinetocoro',
                                  'Huso mitótico',
                                  'Centrosoma',
                                  'Nucléolo',
                                  'Placa metafásica'],
                 'correcta': 'A'},
                {'pregunta': 'El huso mitótico se forma en la profase a '
                             'partir de una estructura llamada:',
                 'alternativas': ['Centrosoma',
                                  'Cromatina',
                                  'Cinetocoro',
                                  'Cromátide',
                                  'Nucléolo'],
                 'correcta': 'A'},
                {'pregunta': 'Al final de la profase, la estructura que se '
                             'desintegra liberando los cromosomas duplicados '
                             'es la:',
                 'alternativas': ['Membrana plasmática',
                                  'Placa celular',
                                  'Envoltura nuclear',
                                  'Placa metafásica',
                                  'Pared celular'],
                 'correcta': 'C'},
                {'pregunta': 'En la metafase, los cromosomas se alinean en '
                             'el ecuador de la célula formando la:',
                 'alternativas': ['Placa celular',
                                  'Cromatina',
                                  'Lámina media',
                                  'Placa metafásica',
                                  'Envoltura nuclear'],
                 'correcta': 'D'},
                {'pregunta': 'Durante la metafase, el ADN alcanza su:',
                 'alternativas': ['Duplicación completa',
                                  'Mínimo grado de condensación',
                                  'Máximo grado de condensación',
                                  'Total descondensación',
                                  'Fragmentación total'],
                 'correcta': 'C'},
                {'pregunta': 'En la anafase, las estructuras que se separan '
                             'primero, permitiendo la separación de las '
                             'cromátidas hermanas, son los:',
                 'alternativas': ['Microtúbulos exclusivamente',
                                  'Husos mitóticos',
                                  'Cinetocoros exclusivamente',
                                  'Nucléolos',
                                  'Centrómeros'],
                 'correcta': 'E'},
                {'pregunta': 'En la mayoría de células animales, el primer '
                             'indicio de citocinesis suele aparecer durante '
                             'la:',
                 'alternativas': ['Profase',
                                  'Fase G1',
                                  'Metafase',
                                  'Anafase',
                                  'Interfase'],
                 'correcta': 'D'},
                {'pregunta': 'En la telofase, alrededor de cada grupo de '
                             'cromosomas se forma una nueva:',
                 'alternativas': ['Envoltura nuclear',
                                  'Placa celular',
                                  'Placa metafásica',
                                  'Pared celular',
                                  'Membrana citoplasmática exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La citocinesis es el proceso de división del:',
                 'alternativas': ['Núcleo',
                                  'Citoplasma',
                                  'Nucléolo',
                                  'ADN exclusivamente',
                                  'Centrómero'],
                 'correcta': 'B'},
                {'pregunta': 'La citocinesis ocurre principalmente durante '
                             'la:',
                 'alternativas': ['Metafase',
                                  'Profase',
                                  'Telofase',
                                  'Interfase',
                                  'Anafase temprana exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'En las células animales, la constricción de la '
                             'membrana durante la citocinesis se debe a un '
                             'anillo contráctil de microfilamentos de:',
                 'alternativas': ['Tubulina',
                                  'Miosina exclusiva',
                                  'Actina',
                                  'Colágeno',
                                  'Queratina'],
                 'correcta': 'C'},
                {'pregunta': 'En las células vegetales, en lugar de un surco '
                             'de segmentación, la citocinesis forma una:',
                 'alternativas': ['Membrana nueva exclusiva',
                                  'Vacuola central',
                                  'Pared primaria exclusiva',
                                  'Placa celular',
                                  'Lámina nuclear'],
                 'correcta': 'D'},
                {'pregunta': 'La placa celular de las células vegetales se '
                             'forma a partir de vesículas derivadas del:',
                 'alternativas': ['Peroxisoma',
                                  'Lisosoma',
                                  'Retículo endoplasmático',
                                  'Núcleo',
                                  'Aparato de Golgi'],
                 'correcta': 'E'},
                {'pregunta': 'La placa celular vegetal se impregna de '
                             'pectinas y forma finalmente la:',
                 'alternativas': ['Placa metafásica',
                                  'Lámina media',
                                  'Membrana plasmática nueva',
                                  'Pared primaria exclusiva',
                                  'Cutícula'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'REPRODUCCIÓN ASEXUAL O AGÁMICA / TIPOS DE '
                                'REPRODUCCIÓN ASEXUAL',
                      'items': ['En la reproducción asexual interviene un '
                                'solo organismo, sin fusión de gametos.',
                                'La escisión binaria, o bipartición, se da '
                                'por estrangulación en el plano medio, '
                                'obteniendo dos nuevos individuos.']},
                     {'titulo': 'REPRODUCCIÓN CELULAR / EL CICLO CELULAR',
                      'items': ['La capacidad de perpetuar la especie es la '
                                'característica que mejor distingue a los '
                                'seres vivos.',
                                'El ciclo celular es la sucesión de etapas '
                                'en que una célula alterna entre crecimiento '
                                'y división a lo largo de su vida.']},
                     {'titulo': 'LA INTERFASE Y SUS ETAPAS / LA MITOSIS: '
                                'CONCEPTO Y FASES',
                      'items': ['La interfase es el período entre dos '
                                'divisiones celulares consecutivas, en el '
                                'que la célula permanece hasta el 95% del '
                                'tiempo.',
                                'La mitosis es un proceso de división '
                                'nuclear, o cariocinesis, que reparte el ADN '
                                'replicado.']},
                     {'titulo': 'LA CITOCINESIS / LA MEIOSIS',
                      'items': ['La citocinesis es el proceso de división '
                                'del citoplasma, que reparte el contenido '
                                'citoplasmático y los organelos.',
                                'La meiosis consiste en dos divisiones '
                                'celulares sucesivas, que reducen el número '
                                'de cromosomas a la mitad.']},
                     {'titulo': 'REPRODUCCIÓN SEXUAL: CONCEPTO Y FECUNDACIÓN '
                                '/ GAMETOS Y TIPOS DE ORGANISMOS',
                      'items': ['La reproducción sexual implica la fusión de '
                                'dos gametos y la mezcla de sus materiales '
                                'genéticos.',
                                'Los gametos masculinos, pequeños, se llaman '
                                'espermatozoides; los femeninos, más '
                                'grandes, se llaman óvulos.']}]},
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
                {'titulo': '11.3 INTRODUCCIÓN A LAS LEYES DE MENDEL',
                 'items': ['Los organismos {diploides} tienen los cromosomas '
                           'en pares; un cromosoma de cada par viene del '
                           'óvulo y el otro del {espermatozoide}.',
                           'Las dos copias de un gen para una característica '
                           'se llaman {alelos}; se escriben en forma '
                           'dominante o {recesiva}.',
                           'Mendel utilizó como organismo de estudio el '
                           '{chícharo}, guisante o arveja (Pisum sativum), '
                           'estudiando {siete} características genéticas.']},
                {'titulo': '11.4 PRIMERA LEY DE MENDEL: DOMINANCIA',
                 'items': ['La {Primera Ley de Mendel}, o Ley de la '
                           'Uniformidad o de la Dominancia, se obtiene al '
                           'cruzar dos líneas {puras} de una característica.',
                           'Al cruzar semilla lisa dominante (AA) con rugosa '
                           'recesiva (aa), la descendencia F1 será '
                           'fenotípicamente {dominante} (lisa) y '
                           'genotípicamente {heterocigota} (Aa).',
                           'En la {F1}, todos los descendientes presentan el '
                           'fenotipo {dominante}.']},
                {'titulo': '11.5 SEGUNDA LEY DE MENDEL: SEGREGACIÓN',
                 'items': ['La {Segunda Ley de Mendel}, o Ley de la '
                           'Segregación de los Alelos, se obtiene al cruzar '
                           'dos individuos {heterocigotos} de la F1.',
                           'En la {F2}, se obtiene 25% homocigoto {recesivo} '
                           '(aa), 50% heterocigoto (Aa), y 25% homocigoto '
                           '{dominante} (AA).',
                           'Fenotípicamente en la F2, el {75}% presenta el '
                           'carácter dominante y el 25% el carácter '
                           '{recesivo} (proporción 3:1).',
                           'Esta segregación ocurre porque existe una '
                           'separación de {alelos} en los gametos de los '
                           'individuos.']},
                {'titulo': '11.6 TERCERA LEY DE MENDEL: DISTRIBUCIÓN '
                           'INDEPENDIENTE',
                 'items': ['La {Tercera Ley de Mendel}, o Ley de la '
                           'Distribución Independiente, estudia la herencia '
                           'de {dos} características al mismo tiempo.',
                           'Mendel cruzó semillas lisas y amarillas '
                           '(dominantes) con rugosas y verdes (recesivas); '
                           'en la F1 todas resultaron lisas y amarillas, '
                           '{heterocigotas}.',
                           'En la {F2}, aparecieron todas las combinaciones '
                           'posibles, mostrando que las características se '
                           'heredan de forma {independiente}.',
                           'La distribución independiente resulta de la '
                           'conducta de los {cromosomas} durante la meiosis, '
                           'que se separan al {azar}.']},
                {'titulo': '11.7 EL CUADRO DE PUNNETT',
                 'items': ['Para realizar los cruzamientos genéticos y '
                           'predecir la descendencia, se utiliza el {cuadro '
                           'de Punnett}.',
                           'En la tabla, los gametos de un padre se escriben '
                           'en las {columnas} y los del otro padre en las '
                           '{filas}.',
                           'Cada cuadrado interior muestra un {genotipo} '
                           'posible de la descendencia, combinando los '
                           'alelos de fila y columna.']},
                {'titulo': '11.8 IMPORTANCIA Y APLICACIONES',
                 'items': ['En la agricultura y ganadería se aplica la '
                           '{selección artificial} para mejorar especies.',
                           'En {biotecnología}, bacterias y hongos '
                           'manipulados genéticamente sintetizan '
                           'medicamentos.']}],
  'cuadros': [{'titulo': '11.2 TÉRMINOS GENÉTICOS BÁSICOS',
               'encabezados': ['Término', 'Significado'],
               'filas': [['{Gen}', 'Unidad de la {herencia}'],
                         ['{Alelo}', 'Variante {génica}'],
                         ['{Fenotipo}', 'Lo que se {observa}'],
                         ['{Genotipo}', 'Dotación {genética}']]}],
  'preguntas': [{'pregunta': 'El término «genética» deriva de la raíz griega '
                             '«gen», que significa:',
                 'alternativas': ['Célula',
                                  'Especie',
                                  'Herencia',
                                  'Llegar a ser',
                                  'Cromosoma'],
                 'correcta': 'D'},
                {'pregunta': 'La genética es la rama de la biología que '
                             'estudia:',
                 'alternativas': ['Solo la fotosíntesis',
                                  'La herencia biológica de los seres vivos',
                                  'Solo la nutrición',
                                  'Solo la ecología',
                                  'Solo la evolución'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia la '
                             'organización y replicación del ADN es la '
                             'genética:',
                 'alternativas': ['De poblaciones',
                                  'Aplicada exclusiva',
                                  'Clásica',
                                  'Molecular',
                                  'Ambiental'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la genética que estudia el conjunto '
                             'de genes de una población, vinculada a la '
                             'evolución, es la genética:',
                 'alternativas': ['Celular',
                                  'Aplicada',
                                  'Molecular',
                                  'De poblaciones',
                                  'Clásica'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la genética que estudia cómo un '
                             'organismo hereda y transmite sus genes es la '
                             'genética:',
                 'alternativas': ['Aplicada',
                                  'Ambiental',
                                  'Clásica o de transmisión',
                                  'De poblaciones',
                                  'Molecular'],
                 'correcta': 'D'},
                {'pregunta': 'El científico asociado a la genética clásica, '
                             'descubridor de las leyes de la herencia, es:',
                 'alternativas': ['Virchow',
                                  'Crick',
                                  'Darwin',
                                  'Gregor Mendel',
                                  'Watson'],
                 'correcta': 'D'},
                {'pregunta': 'La unidad de la herencia que produce la '
                             'expresión característica observable se llama:',
                 'alternativas': ['Locus',
                                  'Alelo',
                                  'Gen',
                                  'Cromosoma',
                                  'Fenotipo'],
                 'correcta': 'C'},
                {'pregunta': 'El sitio específico en la cadena nucleotídica '
                             'donde se encuentra un gen se llama:',
                 'alternativas': ['Alelo',
                                  'Fenotipo',
                                  'Genotipo',
                                  'Genoma',
                                  'Locus'],
                 'correcta': 'E'},
                {'pregunta': 'Cada una de las variantes génicas que '
                             'determinan un carácter se llama:',
                 'alternativas': ['Cromátida',
                                  'Locus',
                                  'Nucleótido',
                                  'Alelo',
                                  'Genoma'],
                 'correcta': 'D'},
                {'pregunta': 'El alelo que se manifiesta siempre, '
                             'representado con letra mayúscula, se llama '
                             'alelo:',
                 'alternativas': ['Dominante',
                                  'Recesivo',
                                  'Mutante',
                                  'Codominante',
                                  'Neutro'],
                 'correcta': 'A'},
                {'pregunta': 'El alelo que solo se manifiesta si no está '
                             'presente el dominante se llama alelo:',
                 'alternativas': ['Neutro',
                                  'Recesivo',
                                  'Letal',
                                  'Codominante',
                                  'Dominante'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión observable determinada por el '
                             'genotipo, «lo que se ve», se llama:',
                 'alternativas': ['Genoma',
                                  'Genotipo',
                                  'Fenotipo',
                                  'Alelo',
                                  'Locus'],
                 'correcta': 'C'},
                {'pregunta': 'La dotación genética de un individuo para un '
                             'carácter determinado se llama:',
                 'alternativas': ['Locus',
                                  'Fenotipo',
                                  'Genotipo',
                                  'Cromátida',
                                  'Alelo'],
                 'correcta': 'C'},
                {'pregunta': 'El individuo que porta dos alelos idénticos '
                             'para un carácter se llama:',
                 'alternativas': ['Homocigoto',
                                  'Mutante',
                                  'Recesivo puro',
                                  'Heterocigoto',
                                  'Híbrido exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'El individuo que porta dos alelos distintos '
                             'para un carácter se llama:',
                 'alternativas': ['Puro',
                                  'Homocigoto',
                                  'Recesivo puro',
                                  'Heterocigoto',
                                  'Dominante puro'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de genes de una especie se llama:',
                 'alternativas': ['Locus',
                                  'Fenotipo',
                                  'Cromátida',
                                  'Genoma',
                                  'Alelo'],
                 'correcta': 'D'},
                {'pregunta': 'AA se representa como un ejemplo de genotipo:',
                 'alternativas': ['Homocigoto recesivo',
                                  'Heterocigoto',
                                  'Codominante',
                                  'Ligado al sexo',
                                  'Homocigoto dominante'],
                 'correcta': 'E'},
                {'pregunta': 'Aa se representa como un ejemplo de genotipo:',
                 'alternativas': ['Letal',
                                  'Heterocigoto',
                                  'Nulo',
                                  'Homocigoto dominante',
                                  'Homocigoto recesivo'],
                 'correcta': 'B'},
                {'pregunta': 'En agricultura y ganadería, la elección de '
                             'especies con rasgos deseables se llama:',
                 'alternativas': ['Migración génica',
                                  'Mutación dirigida',
                                  'Deriva génica',
                                  'Selección artificial',
                                  'Selección natural'],
                 'correcta': 'D'},
                {'pregunta': 'En biotecnología, medicamentos son '
                             'sintetizados por bacterias y hongos que han '
                             'sido:',
                 'alternativas': ['Extinguidos',
                                  'Eliminados del ecosistema',
                                  'Manipulados genéticamente',
                                  'Fosilizados',
                                  'Domesticados sin cambios'],
                 'correcta': 'C'},
                {'pregunta': 'En los organismos diploides, un cromosoma de '
                             'cada par viene del óvulo y el otro del:',
                 'alternativas': ['Polen exclusivo',
                                  'Cigoto',
                                  'Espermatozoide',
                                  'Endospermo',
                                  'Embrión'],
                 'correcta': 'C'},
                {'pregunta': 'Las dos copias de un gen para una '
                             'característica dada se llaman:',
                 'alternativas': ['Cinetocoros',
                                  'Cromátidas',
                                  'Alelos',
                                  'Centrómeros',
                                  'Loci exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'El organismo que Mendel utilizó para sus '
                             'experimentos, en el que estudió siete '
                             'características genéticas, fue el:',
                 'alternativas': ['Trigo',
                                  'Ratón',
                                  'Chícharo o guisante',
                                  'Moscardón',
                                  'Maíz'],
                 'correcta': 'C'},
                {'pregunta': 'La Primera Ley de Mendel también se conoce '
                             'como Ley de la Uniformidad o de la:',
                 'alternativas': ['Dominancia',
                                  'Recombinación',
                                  'Distribución independiente',
                                  'Codominancia',
                                  'Segregación'],
                 'correcta': 'A'},
                {'pregunta': 'Al cruzar dos líneas puras (AA x aa), la '
                             'descendencia F1 será fenotípicamente dominante '
                             'y genotípicamente:',
                 'alternativas': ['Homocigota recesiva',
                                  'Heterocigota',
                                  'Homocigota dominante',
                                  'Nula',
                                  'Mixta'],
                 'correcta': 'B'},
                {'pregunta': 'Según la Primera Ley de Mendel, en la F1 todos '
                             'los descendientes presentan el fenotipo:',
                 'alternativas': ['Dominante',
                                  'Variable',
                                  'Mixto',
                                  'Intermedio',
                                  'Recesivo'],
                 'correcta': 'A'},
                {'pregunta': 'La Segunda Ley de Mendel también se conoce '
                             'como Ley de la Segregación de:',
                 'alternativas': ['Los alelos',
                                  'Los cigotos',
                                  'Las especies',
                                  'Las mutaciones',
                                  'Los cromosomas'],
                 'correcta': 'A'},
                {'pregunta': 'La Segunda Ley de Mendel se obtiene al cruzar '
                             'dos individuos de la F1 que son:',
                 'alternativas': ['Híbridos triples',
                                  'Homocigotos recesivos',
                                  'Puros',
                                  'Heterocigotos',
                                  'Homocigotos dominantes'],
                 'correcta': 'D'},
                {'pregunta': 'En la F2, según la Segunda Ley de Mendel, el '
                             'porcentaje de homocigotos recesivos (aa) es:',
                 'alternativas': ['0%', '25%', '50%', '75%', '100%'],
                 'correcta': 'B'},
                {'pregunta': 'En la F2, según la Segunda Ley de Mendel, el '
                             'porcentaje de heterocigotos (Aa) es:',
                 'alternativas': ['25%', '75%', '0%', '100%', '50%'],
                 'correcta': 'E'},
                {'pregunta': 'Fenotípicamente, en la F2 de la Segunda Ley de '
                             'Mendel, la proporción entre carácter dominante '
                             'y recesivo es:',
                 'alternativas': ['1:3', '3:1', '4:1', '2:1', '1:1'],
                 'correcta': 'B'},
                {'pregunta': 'La Tercera Ley de Mendel, o Ley de la '
                             'Distribución Independiente, estudia la '
                             'herencia de:',
                 'alternativas': ['Dos características al mismo tiempo',
                                  'Solo características ligadas al sexo',
                                  'Una sola característica',
                                  'Tres características simultáneas',
                                  'Ninguna característica específica'],
                 'correcta': 'A'},
                {'pregunta': 'Según la Tercera Ley de Mendel, en la F2 '
                             'aparecen todas las combinaciones posibles, '
                             'demostrando que las características se heredan '
                             'de forma:',
                 'alternativas': ['Ligada',
                                  'Independiente',
                                  'Recesiva exclusiva',
                                  'Codominante',
                                  'Dominante exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La distribución independiente de las '
                             'características resulta de la conducta de los '
                             'cromosomas durante la:',
                 'alternativas': ['Interfase',
                                  'Meiosis',
                                  'Fecundación',
                                  'Mitosis',
                                  'Citocinesis'],
                 'correcta': 'B'},
                {'pregunta': 'El instrumento utilizado para realizar '
                             'cruzamientos genéticos y predecir la '
                             'descendencia se llama:',
                 'alternativas': ['Árbol genealógico',
                                  'Cariotipo',
                                  'Cuadro de Punnett',
                                  'Cuadro de Rowe',
                                  'Mapa cromosómico'],
                 'correcta': 'C'},
                {'pregunta': 'En el Cuadro de Punnett, los gametos de un '
                             'padre se escriben en las columnas y los del '
                             'otro padre se escriben en:',
                 'alternativas': ['Los bordes exclusivos',
                                  'Las filas',
                                  'Fuera de la tabla',
                                  'Diagonal',
                                  'El centro'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y RAMAS DE LA GENÉTICA',
                      'items': ['«Genética» deriva de la raíz griega «gen», '
                                'que significa «llegar a ser».']},
                     {'titulo': 'TERMINOLOGÍA GENÉTICA',
                      'items': ['El gen es la unidad de la herencia que '
                                'produce la expresión característica '
                                'observable.']},
                     {'titulo': 'INTRODUCCIÓN A LAS LEYES DE MENDEL',
                      'items': ['Los organismos diploides tienen los '
                                'cromosomas en pares; un cromosoma de cada '
                                'par viene del óvulo y el otro del '
                                'espermatozoide.']},
                     {'titulo': 'PRIMERA LEY DE MENDEL: DOMINANCIA',
                      'items': ['La Primera Ley de Mendel, o Ley de la '
                                'Uniformidad o de la Dominancia, se obtiene '
                                'al cruzar dos líneas puras de una '
                                'característica.']},
                     {'titulo': 'SEGUNDA LEY DE MENDEL: SEGREGACIÓN',
                      'items': ['La Segunda Ley de Mendel, o Ley de la '
                                'Segregación de los Alelos, se obtiene al '
                                'cruzar dos individuos heterocigotos de la '
                                'F1.']},
                     {'titulo': 'TERCERA LEY DE MENDEL: DISTRIBUCIÓN '
                                'INDEPENDIENTE',
                      'items': ['La Tercera Ley de Mendel, o Ley de la '
                                'Distribución Independiente, estudia la '
                                'herencia de dos características al mismo '
                                'tiempo.']},
                     {'titulo': 'EL CUADRO DE PUNNETT',
                      'items': ['Para realizar los cruzamientos genéticos y '
                                'predecir la descendencia, se utiliza el '
                                'cuadro de Punnett.']},
                     {'titulo': 'IMPORTANCIA Y APLICACIONES',
                      'items': ['En la agricultura y ganadería se aplica la '
                                'selección artificial para mejorar '
                                'especies.']}]},
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
                {'titulo': '12.5 TEORÍAS DEL ORIGEN DE LA VIDA',
                 'items': ['Entre las principales teorías del origen de la '
                           'vida están el creacionismo, la {generación '
                           'espontánea}, la biogénesis, la panspermia y la '
                           'teoría {quimiosintética}.',
                           'La teoría de la {generación espontánea}, o '
                           'abiogénesis, sostenía que la vida surgía de '
                           'materia inerte sin reproducción.']},
                {'titulo': '12.6 EXPERIMENTOS CLAVE: REDI, SPALLANZANI Y '
                           'PASTEUR',
                 'items': ['En el siglo XVII, el italiano Francisco {Redi} '
                           'demostró con frascos de carne que la vida no '
                           'surgía de materia inerte.',
                           'En 1745, el inglés {John Needham} defendió la '
                           'generación espontánea con un experimento de '
                           'caldo hervido mal sellado.',
                           'El italiano {Lázaro Spallanzani} repitió el '
                           'experimento sellando bien los frascos, refutando '
                           'a Needham.',
                           'En el siglo XIX, {Louis Pasteur} puso fin '
                           'definitivo a la generación espontánea usando '
                           'matraces de «cuello de {cisne}».']},
                {'titulo': '12.7 TEORÍA COSMOZOICA O PANSPERMIA',
                 'items': ['La teoría de la {panspermia} fue propuesta en '
                           '1879 por {Herman Von Helmholtz}.',
                           'El químico sueco {Svante Arrhenius} popularizó '
                           'la panspermia en {1908}.',
                           'Según la panspermia, la vida se originó en el '
                           '{espacio}, llegando a la Tierra en '
                           '{meteoritos}.']},
                {'titulo': '12.8 TEORÍA DE LA QUIMIOSÍNTESIS',
                 'items': ['La teoría quimiosintética fue planteada en '
                           '{1921} por el bioquímico ruso {Alexander '
                           'Oparin}.',
                           'Oparin propuso que la atmósfera primitiva era '
                           'rica en metano, amoniaco, CO2 y agua, y muy '
                           'pobre en {oxígeno}.',
                           'Oparin propuso también la teoría de la '
                           '{coacervación}: macromoléculas que formaban '
                           'agregados llamados {coacervados}.',
                           'Los coacervados, rodeados de una membrana '
                           'simple, formaron {precélulas} sujetas a la '
                           'selección natural.',
                           'En {1924}, {John Haldane} llegó a conclusiones '
                           'semejantes a las de Oparin, hablando de una '
                           '«sopa primigenia».']},
                {'titulo': '12.9 EL EXPERIMENTO DE MILLER Y UREY',
                 'items': ['En {1953}, {Stanley Miller} y Harold Urey '
                           'simularon en laboratorio las condiciones de la '
                           'atmósfera primitiva.',
                           'El experimento de Miller y Urey usó una mezcla '
                           'de hidrógeno, vapor de agua, amoniaco y '
                           '{metano}, con descargas eléctricas.',
                           'El experimento produjo aminoácidos como ácido '
                           'glutámico, ácido aspártico, {glicina} y alanina.',
                           'Una conclusión clave fue que sin oxígeno libre '
                           'se formaron compuestos {orgánicos}; con oxígeno, '
                           'solo hubo {oxidación}.',
                           'Las etapas del origen de la vida según esta '
                           'teoría son: síntesis de moléculas simples, '
                           'formación de {polímeros}, formación de '
                           'membranas, e inicio de la {herencia}.']}],
  'cuadros': [{'titulo': '12.1-12.4 TEORÍAS DE LA EVOLUCIÓN',
               'encabezados': ['Teoría', 'Autor'],
               'filas': [['{Transformismo}', '{Lamarck}'],
                         ['{Selección natural}', '{Darwin}'],
                         ['{Mutacionismo}', '{De Vries}'],
                         ['{Teoría Sintética}', '{Dobzhansky}']]}],
  'preguntas': [{'pregunta': 'La evolución se define como todo cambio en una '
                             'población mediante el cual se forman:',
                 'alternativas': ['Ninguna variación',
                                  'Solo mutaciones aisladas',
                                  'Solo caracteres adquiridos',
                                  'Nuevas especies a lo largo del tiempo',
                                  'Nuevos individuos idénticos'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «evolución» fue empleada por '
                             'primera vez por:',
                 'alternativas': ['Darwin',
                                  'Lamarck',
                                  'De Vries',
                                  'Mendel',
                                  'Charles Bonnet'],
                 'correcta': 'E'},
                {'pregunta': 'La hipótesis que explicaba los fósiles por '
                             'catástrofes periódicas se llama:',
                 'alternativas': ['Teoría sintética',
                                  'Mutacionismo',
                                  'Transformismo',
                                  'Catastrofismo',
                                  'Selección natural'],
                 'correcta': 'D'},
                {'pregunta': 'La primera hipótesis completa de la evolución '
                             'fue formulada por:',
                 'alternativas': ['Wallace',
                                  'Darwin',
                                  'De Vries',
                                  'Lamarck',
                                  'Dobzhansky'],
                 'correcta': 'D'},
                {'pregunta': 'Lamarck publicó su hipótesis en 1809 en el '
                             'libro:',
                 'alternativas': ['El origen de las especies',
                                  'Pangénesis intracelular',
                                  'Filosofía Zoológica',
                                  'La Genética y el Origen de las Especies',
                                  'Principios de Biología'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de Lamarck según el cual las '
                             'estructuras más usadas se desarrollan se '
                             'llama:',
                 'alternativas': ['Variación continua',
                                  'Mutación espontánea',
                                  'Uso y desuso',
                                  'Selección natural',
                                  'Herencia mendeliana'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de que las modificaciones por uso '
                             'y desuso son heredables se llama:',
                 'alternativas': ['Selección natural',
                                  'Variación discontinua',
                                  'Herencia de los caracteres adquiridos',
                                  'Mutacionismo',
                                  'Teoría sintética'],
                 'correcta': 'C'},
                {'pregunta': 'Lamarck ilustró su teoría con el ejemplo '
                             'clásico de:',
                 'alternativas': ['El color de la polilla',
                                  'El pico del pinzón',
                                  'El cuello de la jirafa',
                                  'La resistencia bacteriana',
                                  'Las alas del murciélago'],
                 'correcta': 'C'},
                {'pregunta': 'El fundador de la teoría de la evolución por '
                             'selección natural es:',
                 'alternativas': ['De Vries',
                                  'Mendel',
                                  'Lamarck',
                                  'Bonnet',
                                  'Charles Darwin'],
                 'correcta': 'E'},
                {'pregunta': 'Darwin publicó su obra principal, «El origen '
                             'de las especies», en el año:',
                 'alternativas': ['1937', '1758', '1859', '1809', '1889'],
                 'correcta': 'C'},
                {'pregunta': 'El biólogo que llegó a conclusiones similares '
                             'a Darwin de forma independiente fue:',
                 'alternativas': ['Mendel',
                                  'Alfred Russel Wallace',
                                  'Lamarck',
                                  'Dobzhansky',
                                  'De Vries'],
                 'correcta': 'B'},
                {'pregunta': 'Los cuatro conceptos centrales de la selección '
                             'natural son variación, sobreproducción, lucha '
                             'por la existencia y:',
                 'alternativas': ['Uso y desuso',
                                  'Mutación',
                                  'Herencia adquirida',
                                  'Catastrofismo',
                                  'Selección natural'],
                 'correcta': 'E'},
                {'pregunta': 'El concepto que sostiene que todos los '
                             'miembros de una especie difieren entre sí se '
                             'llama:',
                 'alternativas': ['Mutación',
                                  'Herencia',
                                  'Variación',
                                  'Sobreproducción',
                                  'Selección natural'],
                 'correcta': 'C'},
                {'pregunta': 'El mecanismo que incrementa las probabilidades '
                             'de que algunos vástagos sobrevivan se llama:',
                 'alternativas': ['Sobreproducción',
                                  'Selección natural',
                                  'Variación',
                                  'Mutación',
                                  'Adaptación exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Según la selección natural, los individuos '
                             'mejor adaptados:',
                 'alternativas': ['Desaparecen primero',
                                  'Sobreviven y transmiten sus '
                                  'características',
                                  'Son eliminados por competencia',
                                  'No se reproducen nunca',
                                  'No tienen ventaja alguna'],
                 'correcta': 'B'},
                {'pregunta': 'El botánico que publicó «Pangénesis '
                             'intracelular» en 1889 fue:',
                 'alternativas': ['Hugo De Vries',
                                  'Lamarck',
                                  'Dobzhansky',
                                  'Wallace',
                                  'Darwin'],
                 'correcta': 'A'},
                {'pregunta': 'De Vries reemplazó la noción de variación '
                             'continua por la de:',
                 'alternativas': ['Uso y desuso',
                                  'Herencia de caracteres adquiridos',
                                  'Catastrofismo',
                                  'Selección natural',
                                  'Variación discontinua o mutación'],
                 'correcta': 'E'},
                {'pregunta': 'Una mutación se define como la aparición '
                             'repentina de una variante en:',
                 'alternativas': ['Un organismo completo',
                                  'Una especie entera',
                                  'Un ecosistema',
                                  'Una población completa',
                                  'Un gen particular o grupo de genes'],
                 'correcta': 'E'},
                {'pregunta': 'La Teoría Sintética de la evolución fue dada a '
                             'conocer por:',
                 'alternativas': ['De Vries',
                                  'Wallace',
                                  'Darwin',
                                  'Theodosius Dobzhansky',
                                  'Lamarck'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría Sintética combina la selección '
                             'natural con las leyes de la herencia de Mendel '
                             'y:',
                 'alternativas': ['La teoría del big bang',
                                  'El catastrofismo',
                                  'El transformismo puro',
                                  'La teoría celular',
                                  'El mutacionismo'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las principales teorías del origen de la '
                             'vida figuran el creacionismo, la generación '
                             'espontánea, la biogénesis y:',
                 'alternativas': ['El transformismo',
                                  'La panspermia',
                                  'La herencia adquirida',
                                  'El mutacionismo',
                                  'La selección natural'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría que sostenía que la vida surgía de '
                             'materia inerte sin reproducción se llama:',
                 'alternativas': ['Biogénesis',
                                  'Selección natural',
                                  'Generación espontánea o abiogénesis',
                                  'Quimiosíntesis',
                                  'Panspermia'],
                 'correcta': 'C'},
                {'pregunta': 'El científico que en el siglo XVII demostró '
                             'con frascos de carne que la vida no surge de '
                             'materia inerte fue:',
                 'alternativas': ['Needham',
                                  'Spallanzani',
                                  'Pasteur',
                                  'Oparin',
                                  'Francisco Redi'],
                 'correcta': 'E'},
                {'pregunta': 'El inglés que en 1745 defendió la generación '
                             'espontánea con un caldo mal sellado fue:',
                 'alternativas': ['Spallanzani',
                                  'John Needham',
                                  'Pasteur',
                                  'Haldane',
                                  'Redi'],
                 'correcta': 'B'},
                {'pregunta': 'El italiano que refutó a Needham sellando bien '
                             'los frascos fue:',
                 'alternativas': ['Oparin',
                                  'Lázaro Spallanzani',
                                  'Redi',
                                  'Miller',
                                  'Pasteur'],
                 'correcta': 'B'},
                {'pregunta': 'El científico que puso fin definitivo a la '
                             'generación espontánea con matraces de cuello '
                             'de cisne fue:',
                 'alternativas': ['Louis Pasteur',
                                  'Haldane',
                                  'Spallanzani',
                                  'Redi',
                                  'Needham'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría de la panspermia fue propuesta en '
                             '1879 por:',
                 'alternativas': ['Haldane',
                                  'Svante Arrhenius',
                                  'Herman Von Helmholtz',
                                  'Oparin',
                                  'Pasteur'],
                 'correcta': 'C'},
                {'pregunta': 'El químico sueco que popularizó la panspermia '
                             'en 1908 fue:',
                 'alternativas': ['Redi',
                                  'Von Helmholtz',
                                  'Svante Arrhenius',
                                  'Miller',
                                  'Oparin'],
                 'correcta': 'C'},
                {'pregunta': 'Según la panspermia, la vida se originó en el '
                             'espacio y llegó a la Tierra mediante:',
                 'alternativas': ['Meteoritos',
                                  'Ondas de radio',
                                  'Rayos cósmicos',
                                  'Explosiones solares',
                                  'Corrientes marinas'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría quimiosintética fue planteada en '
                             '1921 por el bioquímico ruso:',
                 'alternativas': ['John Haldane',
                                  'Charles Darwin',
                                  'Alexander Oparin',
                                  'Stanley Miller',
                                  'Louis Pasteur'],
                 'correcta': 'C'},
                {'pregunta': 'Según Oparin, la atmósfera primitiva era rica '
                             'en metano, amoniaco, CO2 y agua, pero pobre '
                             'en:',
                 'alternativas': ['Nitrógeno',
                                  'Hidrógeno',
                                  'Azufre',
                                  'Oxígeno',
                                  'Carbono'],
                 'correcta': 'D'},
                {'pregunta': 'Oparin propuso que las macromoléculas formaban '
                             'agregados llamados:',
                 'alternativas': ['Ribosomas',
                                  'Coacervados',
                                  'Plásmidos',
                                  'Gametos',
                                  'Cigotos'],
                 'correcta': 'B'},
                {'pregunta': 'John Haldane, en 1924, habló de una:',
                 'alternativas': ['Panspermia dirigida',
                                  'Selección artificial',
                                  'Mutación espontánea masiva',
                                  'Generación espontánea directa',
                                  'Sopa primigenia'],
                 'correcta': 'E'},
                {'pregunta': 'El experimento clave que simuló la atmósfera '
                             'primitiva en laboratorio fue realizado en 1953 '
                             'por:',
                 'alternativas': ['Darwin y Wallace',
                                  'Stanley Miller y Harold Urey',
                                  'Oparin y Haldane',
                                  'Pasteur y Needham',
                                  'Redi y Spallanzani'],
                 'correcta': 'B'},
                {'pregunta': 'El experimento de Miller y Urey usó una mezcla '
                             'de hidrógeno, vapor de agua, amoniaco y:',
                 'alternativas': ['Ozono',
                                  'Metano',
                                  'Nitrógeno puro',
                                  'Oxígeno',
                                  'Dióxido de azufre'],
                 'correcta': 'B'},
                {'pregunta': 'El experimento de Miller y Urey produjo, entre '
                             'otros compuestos, aminoácidos como:',
                 'alternativas': ['Solo ADN completo',
                                  'Solo agua y sal',
                                  'Ácido glutámico y glicina',
                                  'Solo minerales',
                                  'Solo proteínas complejas'],
                 'correcta': 'C'},
                {'pregunta': 'Una conclusión clave del experimento de Miller '
                             'y Urey fue que sin oxígeno libre se formaron:',
                 'alternativas': ['Solo gases inertes',
                                  'Compuestos orgánicos',
                                  'Solo minerales',
                                  'Ninguna sustancia nueva',
                                  'Solo agua'],
                 'correcta': 'B'},
                {'pregunta': 'Con presencia de oxígeno en el experimento de '
                             'Miller y Urey, solo se produjeron reacciones '
                             'de:',
                 'alternativas': ['Oxidación',
                                  'Síntesis orgánica',
                                  'Fotosíntesis',
                                  'Fermentación',
                                  'Reducción exclusiva'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ANTECEDENTES / TEORÍA DEL '
                                'TRANSFORMISMO',
                      'items': ['La evolución es todo cambio en una '
                                'población mediante el cual se forman nuevas '
                                'especies a lo largo del tiempo.',
                                'La primera hipótesis completa de la '
                                'evolución fue de Jean Baptiste Lamarck, '
                                'publicada en 1809 en «Filosofía '
                                'Zoológica».']},
                     {'titulo': 'TEORÍA DE LA SELECCIÓN NATURAL / '
                                'MUTACIONISMO Y TEORÍA SINTÉTICA',
                      'items': ['Charles Darwin es el fundador de la teoría '
                                'de la evolución, y publicó en 1859 «El '
                                'origen de las especies».',
                                'Hugo De Vries publicó en 1889 «Pangénesis '
                                'intracelular», reemplazando la variación '
                                'continua por la mutación.']},
                     {'titulo': 'TEORÍAS DEL ORIGEN DE LA VIDA / '
                                'EXPERIMENTOS CLAVE: REDI, SPALLANZANI Y PAS',
                      'items': ['Entre las principales teorías del origen de '
                                'la vida están el creacionismo, la '
                                'generación espontánea, la biogénesis, la '
                                'panspermia y la teoría quimiosintética.',
                                'En el siglo XVII, el italiano Francisco '
                                'Redi demostró con frascos de carne que la '
                                'vida no surgía de materia inerte.']},
                     {'titulo': 'TEORÍA COSMOZOICA O PANSPERMIA / TEORÍA DE '
                                'LA QUIMIOSÍNTESIS',
                      'items': ['La teoría de la panspermia fue propuesta en '
                                '1879 por Herman Von Helmholtz.',
                                'La teoría quimiosintética fue planteada en '
                                '1921 por el bioquímico ruso Alexander '
                                'Oparin.']},
                     {'titulo': 'EL EXPERIMENTO DE MILLER Y UREY',
                      'items': ['En 1953, Stanley Miller y Harold Urey '
                                'simularon en laboratorio las condiciones de '
                                'la atmósfera primitiva.']}]},
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
                {'titulo': '13.4 EL ECOSISTEMA: CONCEPTO Y TÉRMINOS '
                           'RELACIONADOS',
                 'items': ['El término «ecosistema» fue acuñado por {Arthur '
                           'Tansley} en {1935}, como el complejo de '
                           'organismos y factores físicos del ambiente.',
                           'Un ecosistema es un sistema {abierto}: hay una '
                           'corriente continua de captación y pérdida de '
                           'sustancias y {energía}.',
                           'El ecosistema más grande que se puede concebir '
                           'es la {biosfera}.',
                           'La {biocenosis} es la comunidad biótica formada '
                           'por todos los organismos vivos de un lugar.',
                           'El {biotopo} es el espacio físico donde vive una '
                           'biocenosis, caracterizado por factores '
                           '{abióticos}.',
                           'El {hábitat} es el lugar donde un organismo '
                           'encuentra condiciones favorables para vivir; es '
                           'su «{dirección}» ecológica.',
                           'El {nicho ecológico} son las necesidades '
                           'especiales de una población respecto a alimento, '
                           'luz y humedad.',
                           'Dos organismos en un mismo lugar nunca tienen el '
                           'mismo {nicho ecológico}, o entrarían en '
                           '{competencia}.']},
                {'titulo': '13.5 COMPONENTES ABIÓTICOS DEL ECOSISTEMA',
                 'items': ['La {luz solar} es la fuente de energía de la '
                           'mayoría de los ecosistemas.',
                           'Los {nutrientes} principales del tejido vivo son '
                           'carbono, nitrógeno, oxígeno, hidrógeno, fósforo '
                           'y {azufre}.',
                           'Los factores {climáticos} determinan la '
                           'distribución geográfica de los componentes del '
                           'ecosistema.',
                           'El {suelo} está compuesto de roca y minerales, '
                           'más un componente orgánico de materia animal y '
                           'vegetal muerta.']},
                {'titulo': '13.6 RELACIONES INTRAESPECÍFICAS',
                 'items': ['Las relaciones {intraespecíficas} u homotípicas '
                           'se dan entre individuos de la {misma} especie.',
                           'Las {agrupaciones casuales} o agregaciones no '
                           'generan vínculos, como guacamayos en colpas o '
                           'mariposas en flores.',
                           'La {asociación} o sociedad es la relación '
                           'temporal o permanente con vínculos, como la '
                           'defensa común.',
                           'Las {colmenas} son familias con diferenciación '
                           'morfológica: reinas, zánganos, obreras y '
                           '{soldados}.',
                           'La agrupación de individuos puede producir tres '
                           'efectos: {cooperación}, competencia e '
                           '{interferencia}.']},
                {'titulo': '13.7 RELACIONES INTERESPECÍFICAS',
                 'items': ['Las relaciones {interespecíficas} u '
                           'heterotípicas se dan entre individuos de '
                           'especies {diferentes}.',
                           'La {sinequia} ocurre cuando dos organismos viven '
                           'juntos y se toleran sin hacerse {daño}.',
                           'El {epifitismo} ocurre cuando plantas crecen '
                           'sobre otras, usándolas de soporte sin '
                           'dañarlas.']},
                {'titulo': '13.8 MUTUA TOLERANCIA Y CONVIVENCIA',
                 'items': ['La {foresia} ocurre cuando un individuo se deja '
                           'transportar temporalmente por otra especie, como '
                           'los ácaros que se prenden de {insectos}.',
                           'El {comensalismo} beneficia a una especie sin '
                           'efecto sobre la otra; ejemplo: los zorros que '
                           'consumen restos dejados por el {puma}.',
                           'Las {agallas} son proliferaciones de tejido '
                           'vegetal provocadas por avispas, moscas u '
                           'hormigas que ponen sus {huevos} dentro de la '
                           'planta.']},
                {'titulo': '13.9 MUTUALISMO Y SIMBIOSIS',
                 'items': ['El {mutualismo} beneficia a ambas especies; '
                           'puede ser {facultativo} (no imprescindible) u '
                           'obligado.',
                           'La {simbiosis} es un mutualismo obligado para '
                           'ambos, donde los organismos no pueden vivir '
                           '{separados}.',
                           'La {simbiosis liquénica} es la relación entre un '
                           'hongo y un {alga}: el alga aporta oxígeno y '
                           'materia vegetal por fotosíntesis.',
                           'Las bacterias del género {Rhizobium}, en nódulos '
                           'de las raíces, captan nitrógeno del aire para '
                           'las plantas leguminosas.',
                           'En el intestino humano, la {flora intestinal} '
                           'ayuda a digerir alimentos; los antibióticos '
                           'pueden destruir esta simbiosis.']},
                {'titulo': '13.10 DEPREDACIÓN',
                 'items': ['La {depredación} es el consumo de un organismo '
                           'viviente por otro, en la relación '
                           '{presa}-depredador.',
                           'La depredación dinamiza el ciclo de la {energía} '
                           'y nutrientes, y favorece la {selección natural} '
                           'al eliminar a los menos aptos.',
                           'Ejemplo peruano: el {puma} es depredador natural '
                           'de la vicuña adulta; el zorro o atoq caza '
                           'generalmente sus {crías}.']},
                {'titulo': '13.11 PARASITISMO',
                 'items': ['El {parasitismo} es la relación donde un '
                           'organismo (parásito) usa a otro (hospedero) como '
                           'fuente de {alimento}, debilitándolo.',
                           'El {ectoparasitismo} ocurre cuando el parásito '
                           'vive u obtiene alimento en el {exterior} del '
                           'hospedero, como pulgas y garrapatas.',
                           'El {endoparasitismo} ocurre cuando el parásito '
                           'vive en el {interior} del hospedero.',
                           'El {hemoparásito} Plasmodium vivax causa el '
                           '{paludismo} o malaria, transmitido por el '
                           'mosquito Anopheles.',
                           'El {enteroparásito} se encuentra en el intestino '
                           'del huésped; ejemplos: Taenia solium y Ascaris '
                           '{lumbricoides}.',
                           'El {histioparásito} se localiza en los tejidos; '
                           'el cisticerco de la Taenia solium causa la '
                           '{cisticercosis}.']},
                {'titulo': '13.12 FUNCIONES DE LOS ECOSISTEMAS: SUCESIÓN '
                           'ECOLÓGICA',
                 'items': ['La {sucesión ecológica} es la secuencia de '
                           'cambios que experimenta un ecosistema a través '
                           'del tiempo.',
                           'Las sucesiones llevan a un ecosistema a su '
                           'máxima expresión armónica, llamada {comunidad '
                           'clímax}.',
                           'La {sucesión primaria} comienza cuando especies '
                           'pioneras colonizan un hábitat sin suelo, como '
                           'una isla volcánica.',
                           'Los pioneros típicos de la sucesión primaria son '
                           '{musgos} y líquenes.',
                           'La {sucesión secundaria} comienza donde ya '
                           'existía suelo, tras una perturbación como un '
                           'incendio o tala.']},
                {'titulo': '13.13 ECOSISTEMAS DEL PERÚ',
                 'items': ['Los {biomas} son áreas climáticas definidas con '
                           'condiciones ecológicas similares.',
                           'Las {zonas de vida} de Holdridge se definen por '
                           'biotemperatura, precipitación, humedad y '
                           '{altitud}.',
                           'Una {ecorregión} es un área geográfica con '
                           'condiciones homogéneas de clima, suelo, flora y '
                           'fauna.',
                           'Según {Antonio Brack}, el Perú tiene {11} '
                           'ecorregiones.',
                           'La primera ecorregión es el {mar frío} de la '
                           'Corriente Peruana, o Corriente de {Humboldt}.']}],
  'cuadros': [{'titulo': '13.3 FACTORES AMBIENTALES',
               'encabezados': ['Tipo', 'Corresponde a'],
               'filas': [['{Bióticos}', 'Seres {vivos}'],
                         ['{Abióticos}', 'Ambiente {físico} no viviente']]}],
  'preguntas': [{'pregunta': 'El término «ecología» proviene de los vocablos '
                             'griegos «oikos» y:',
                 'alternativas': ['Logos', 'Bios', 'Genos', 'Physis', 'Zoon'],
                 'correcta': 'A'},
                {'pregunta': '«Oikos» en griego significa:',
                 'alternativas': ['Ciencia',
                                  'Estudio',
                                  'Casa',
                                  'Vida',
                                  'Naturaleza'],
                 'correcta': 'C'},
                {'pregunta': 'El primer estudioso de las interacciones entre '
                             'seres vivos y ambiente fue:',
                 'alternativas': ['Teofrasto',
                                  'Aristóteles',
                                  'Linneo',
                                  'Haeckel',
                                  'Darwin'],
                 'correcta': 'A'},
                {'pregunta': 'El término «Ecología» fue establecido '
                             'formalmente por:',
                 'alternativas': ['Ernest Haeckel',
                                  'Teofrasto',
                                  'Alfred Wallace',
                                  'Gregor Mendel',
                                  'Charles Darwin'],
                 'correcta': 'A'},
                {'pregunta': 'Ernest Haeckel estableció el término '
                             '«Ecología» en el año:',
                 'alternativas': ['1859', '1809', '1869', '1937', '1789'],
                 'correcta': 'C'},
                {'pregunta': 'Haeckel definió la ecología como el estudio de '
                             'las relaciones de los organismos con su '
                             'ambiente:',
                 'alternativas': ['Solo orgánico',
                                  'Solo inorgánico',
                                  'Orgánico e inorgánico',
                                  'Solo económico',
                                  'Solo social'],
                 'correcta': 'C'},
                {'pregunta': 'La ecología estudia principalmente:',
                 'alternativas': ['Solo el clima',
                                  'Solo los océanos',
                                  'Solo la litósfera',
                                  'La biosfera',
                                  'La atmósfera exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'El activismo de la ecología, como movimiento '
                             'cívico, se llama:',
                 'alternativas': ['Sostenibilismo',
                                  'Naturalismo exclusivo',
                                  'Ecologismo',
                                  'Conservacionismo exclusivo',
                                  'Ambientalismo exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El ecologismo tecnicista tiene como objetivo:',
                 'alternativas': ['Viajar a otros planetas',
                                  'Reducir la contaminación proponiendo '
                                  'energías alternativas',
                                  'Estudiar la superpoblación',
                                  'Proteger la vida anímica',
                                  'Evitar la extinción de especies'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo naturalista es una corriente '
                             'filosófica que busca:',
                 'alternativas': ['Analizar la superpoblación',
                                  'Promover el amor espiritual',
                                  'Reducir la contaminación técnica',
                                  'Estudiar recursos limitados',
                                  'Evitar la extinción de especies animales'],
                 'correcta': 'E'},
                {'pregunta': 'El ecologismo sociológico-político estudia, '
                             'entre otros temas, la superpoblación y:',
                 'alternativas': ['Solo la deforestación',
                                  'Solo el reciclaje',
                                  'Solo la energía nuclear',
                                  'La hambruna en el mundo',
                                  'La extinción de especies exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Los factores ambientales se clasifican en '
                             'bióticos y:',
                 'alternativas': ['Naturales exclusivos',
                                  'Orgánicos exclusivos',
                                  'Ecológicos',
                                  'Antrópicos exclusivos',
                                  'Abióticos'],
                 'correcta': 'E'},
                {'pregunta': 'Los factores bióticos corresponden a:',
                 'alternativas': ['Todos los seres vivos',
                                  'Solo el clima',
                                  'El ambiente físico no viviente',
                                  'Solo el agua',
                                  'Solo el suelo'],
                 'correcta': 'A'},
                {'pregunta': 'La concentración de individuos de una especie '
                             'en un área geográfica se llama:',
                 'alternativas': ['Biomasa',
                                  'Hábitat exclusivo',
                                  'Densidad poblacional',
                                  'Nicho ecológico',
                                  'Bioma'],
                 'correcta': 'C'},
                {'pregunta': 'Las relaciones entre individuos de la misma '
                             'especie se llaman relaciones:',
                 'alternativas': ['Simbióticas exclusivas',
                                  'Interespecíficas',
                                  'Intraespecíficas',
                                  'Tróficas exclusivas',
                                  'Ecológicas generales'],
                 'correcta': 'C'},
                {'pregunta': 'Las relaciones entre individuos de especies '
                             'distintas se llaman relaciones:',
                 'alternativas': ['Interespecíficas',
                                  'Intraespecíficas',
                                  'Poblacionales exclusivas',
                                  'Abióticas',
                                  'Bióticas generales'],
                 'correcta': 'A'},
                {'pregunta': 'El ambiente también se suele denominar '
                             'entorno, medio ambiente o:',
                 'alternativas': ['Nicho',
                                  'Ecosistema exclusivo',
                                  'Hábitat exclusivo',
                                  'Bioma exclusivo',
                                  'Naturaleza'],
                 'correcta': 'E'},
                {'pregunta': 'En el ambiente se agrupan seres en dos '
                             'categorías: vivos y:',
                 'alternativas': ['Domesticados',
                                  'Migratorios',
                                  'Extintos',
                                  'No vivos',
                                  'Fósiles'],
                 'correcta': 'D'},
                {'pregunta': 'Debido a que los humanos forman parte de la '
                             'red de vida de la Tierra, sus actividades '
                             'económicas y políticas tienen:',
                 'alternativas': ['Solo implicaciones sociales',
                                  'Ninguna implicación ecológica',
                                  'Solo implicaciones económicas',
                                  'Profundas implicaciones ecológicas',
                                  'Efectos neutros'],
                 'correcta': 'D'},
                {'pregunta': 'El ecologismo surge como una nueva forma de '
                             'hacer política centrada en:',
                 'alternativas': ['El crecimiento económico ilimitado',
                                  'El desarrollo sostenible',
                                  'El comercio internacional',
                                  'La explotación de recursos',
                                  'La industrialización acelerada'],
                 'correcta': 'B'},
                {'pregunta': 'El término «ecosistema» fue acuñado por:',
                 'alternativas': ['Odum',
                                  'Arthur Tansley',
                                  'Antonio Brack',
                                  'Charles Darwin',
                                  'Ernest Haeckel'],
                 'correcta': 'B'},
                {'pregunta': 'Un ecosistema es considerado un sistema:',
                 'alternativas': ['Abierto',
                                  'Cerrado',
                                  'Aislado',
                                  'Sin energía',
                                  'Estático'],
                 'correcta': 'A'},
                {'pregunta': 'El ecosistema más grande que se puede concebir '
                             'es:',
                 'alternativas': ['La biosfera',
                                  'Un bioma',
                                  'Una ecorregión',
                                  'Un biotopo',
                                  'Una biocenosis'],
                 'correcta': 'A'},
                {'pregunta': 'La comunidad biótica formada por todos los '
                             'organismos vivos de un lugar se llama:',
                 'alternativas': ['Hábitat',
                                  'Biotopo',
                                  'Bioma',
                                  'Nicho ecológico',
                                  'Biocenosis'],
                 'correcta': 'E'},
                {'pregunta': 'El espacio físico donde vive una biocenosis, '
                             'caracterizado por factores abióticos, se '
                             'llama:',
                 'alternativas': ['Biotopo',
                                  'Nicho',
                                  'Biocenosis',
                                  'Ecorregión',
                                  'Hábitat'],
                 'correcta': 'A'},
                {'pregunta': 'El lugar donde un organismo encuentra '
                             'condiciones favorables para vivir se llama:',
                 'alternativas': ['Hábitat',
                                  'Biocenosis',
                                  'Bioma',
                                  'Nicho ecológico',
                                  'Biotopo'],
                 'correcta': 'A'},
                {'pregunta': 'Las necesidades especiales de una población '
                             'respecto a alimento, luz y humedad se llaman:',
                 'alternativas': ['Nicho ecológico',
                                  'Hábitat',
                                  'Ecorregión',
                                  'Biotopo',
                                  'Biocenosis'],
                 'correcta': 'A'},
                {'pregunta': 'Dos organismos que viven en el mismo lugar '
                             'nunca comparten el mismo:',
                 'alternativas': ['Biotopo',
                                  'Clima',
                                  'Bioma',
                                  'Nicho ecológico',
                                  'Hábitat'],
                 'correcta': 'D'},
                {'pregunta': 'La fuente de energía de la mayoría de los '
                             'ecosistemas es:',
                 'alternativas': ['El agua',
                                  'El suelo',
                                  'La luz solar',
                                  'Los minerales',
                                  'El aire'],
                 'correcta': 'C'},
                {'pregunta': 'Las relaciones que se dan entre individuos de '
                             'la misma especie se llaman relaciones:',
                 'alternativas': ['Simbióticas exclusivas',
                                  'Predatorias exclusivas',
                                  'Interespecíficas',
                                  'Tróficas exclusivas',
                                  'Intraespecíficas'],
                 'correcta': 'E'},
                {'pregunta': 'Las relaciones que se dan entre individuos de '
                             'especies diferentes se llaman relaciones:',
                 'alternativas': ['Familiares exclusivas',
                                  'Intraespecíficas',
                                  'Interespecíficas',
                                  'De colmena exclusivas',
                                  'Homotípicas'],
                 'correcta': 'C'},
                {'pregunta': 'Las agrupaciones sin vínculos ni trascendencia '
                             'ecológica, como mariposas en flores, se '
                             'llaman:',
                 'alternativas': ['Familias',
                                  'Clanes',
                                  'Sociedades',
                                  'Agrupaciones casuales o agregaciones',
                                  'Colmenas'],
                 'correcta': 'D'},
                {'pregunta': 'Las familias con diferenciación morfológica en '
                             'reinas, zánganos y obreras se llaman:',
                 'alternativas': ['Sociedades simples',
                                  'Agregaciones',
                                  'Manadas',
                                  'Clanes',
                                  'Colmenas'],
                 'correcta': 'E'},
                {'pregunta': 'La agrupación de individuos puede producir '
                             'tres efectos: cooperación, interferencia y:',
                 'alternativas': ['Parasitismo',
                                  'Simbiosis',
                                  'Comensalismo',
                                  'Depredación',
                                  'Competencia'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando dos organismos viven juntos y se '
                             'toleran sin hacerse daño, la relación se '
                             'llama:',
                 'alternativas': ['Competencia',
                                  'Epifitismo',
                                  'Parasitismo',
                                  'Sinequia',
                                  'Depredación'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando una planta crece sobre otra usándola de '
                             'soporte sin dañarla, ocurre:',
                 'alternativas': ['Parasitismo',
                                  'Epifitismo',
                                  'Depredación',
                                  'Sinequia',
                                  'Mutualismo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La secuencia de cambios que experimenta un '
                             'ecosistema a través del tiempo se llama:',
                 'alternativas': ['Biocenosis',
                                  'Sucesión ecológica',
                                  'Bioma',
                                  'Nicho ecológico',
                                  'Comunidad clímax'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima expresión armónica de las '
                             'poblaciones de un ecosistema se llama:',
                 'alternativas': ['Nicho ecológico',
                                  'Ecorregión',
                                  'Comunidad clímax',
                                  'Sucesión primaria',
                                  'Biotopo'],
                 'correcta': 'C'},
                {'pregunta': 'La sucesión que comienza en un hábitat sin '
                             'suelo, como una isla volcánica, se llama '
                             'sucesión:',
                 'alternativas': ['Terciaria',
                                  'Clímax',
                                  'Secundaria',
                                  'Antrópica',
                                  'Primaria'],
                 'correcta': 'E'},
                {'pregunta': 'Los organismos pioneros típicos de la sucesión '
                             'primaria son:',
                 'alternativas': ['Árboles grandes',
                                  'Aves',
                                  'Musgos y líquenes',
                                  'Mamíferos',
                                  'Peces'],
                 'correcta': 'C'},
                {'pregunta': 'La sucesión que comienza donde ya existía '
                             'suelo, tras una perturbación, se llama '
                             'sucesión:',
                 'alternativas': ['Secundaria',
                                  'Ninguna de las anteriores',
                                  'Primaria',
                                  'Clímax exclusiva',
                                  'Terciaria'],
                 'correcta': 'A'},
                {'pregunta': 'Las zonas de vida de Holdridge se definen en '
                             'función de biotemperatura, precipitación, '
                             'humedad y:',
                 'alternativas': ['Longitud',
                                  'Latitud',
                                  'Salinidad',
                                  'Presión atmosférica',
                                  'Altitud'],
                 'correcta': 'E'},
                {'pregunta': 'Según Antonio Brack, el Perú tiene un número '
                             'de ecorregiones igual a:',
                 'alternativas': ['20', '8', '11', '15', '5'],
                 'correcta': 'C'},
                {'pregunta': 'La primera ecorregión del Perú, según Brack, '
                             'es:',
                 'alternativas': ['El mar tropical',
                                  'La puna',
                                  'El mar frío de la Corriente Peruana',
                                  'El desierto costero',
                                  'La selva alta'],
                 'correcta': 'C'},
                {'pregunta': 'La relación en la que un individuo se deja '
                             'transportar temporalmente por otra especie, '
                             'sin dañarla, se llama:',
                 'alternativas': ['Sinequia',
                                  'Agallas',
                                  'Comensalismo',
                                  'Epifitismo',
                                  'Foresia'],
                 'correcta': 'E'},
                {'pregunta': 'La relación en la que una especie se beneficia '
                             'sin tener efecto sobre la otra se llama:',
                 'alternativas': ['Simbiosis',
                                  'Mutualismo',
                                  'Depredación',
                                  'Comensalismo',
                                  'Parasitismo'],
                 'correcta': 'D'},
                {'pregunta': 'Las proliferaciones de tejido vegetal '
                             'provocadas por avispas u hormigas que ponen '
                             'sus huevos en la planta se llaman:',
                 'alternativas': ['Agallas',
                                  'Zarcillos',
                                  'Espinas',
                                  'Micorrizas',
                                  'Nódulos'],
                 'correcta': 'A'},
                {'pregunta': 'El mutualismo en el que cada individuo obtiene '
                             'un beneficio pero no depende del otro se '
                             'llama:',
                 'alternativas': ['Comensal',
                                  'Obligado',
                                  'Facultativo',
                                  'Simbiótico exclusivo',
                                  'Parasitario'],
                 'correcta': 'C'},
                {'pregunta': 'El mutualismo obligado para ambas especies, '
                             'donde no pueden vivir separadas, se llama:',
                 'alternativas': ['Comensalismo',
                                  'Foresia',
                                  'Depredación',
                                  'Simbiosis',
                                  'Amensalismo'],
                 'correcta': 'D'},
                {'pregunta': 'La simbiosis liquénica es la relación entre un '
                             'hongo y:',
                 'alternativas': ['Un virus',
                                  'Una planta superior',
                                  'Un alga',
                                  'Un protozoario',
                                  'Una bacteria'],
                 'correcta': 'C'},
                {'pregunta': 'Las bacterias del género Rhizobium, en nódulos '
                             'de las raíces, captan del aire:',
                 'alternativas': ['Oxígeno',
                                  'Hidrógeno',
                                  'Nitrógeno',
                                  'Dióxido de carbono',
                                  'Metano'],
                 'correcta': 'C'},
                {'pregunta': 'En el intestino humano, la flora intestinal '
                             'ayuda a digerir alimentos; su equilibrio puede '
                             'ser afectado por el uso de:',
                 'alternativas': ['Enzimas digestivas',
                                  'Antibióticos',
                                  'Vitaminas',
                                  'Probióticos exclusivos',
                                  'Fibra'],
                 'correcta': 'B'},
                {'pregunta': 'La relación de consumo de un organismo '
                             'viviente por otro, en el vínculo '
                             'presa-depredador, se llama:',
                 'alternativas': ['Mutualismo',
                                  'Comensalismo',
                                  'Parasitismo',
                                  'Foresia',
                                  'Depredación'],
                 'correcta': 'E'},
                {'pregunta': 'La depredación favorece la selección natural '
                             'al eliminar a los organismos:',
                 'alternativas': ['Más longevos',
                                  'Menos aptos',
                                  'Más numerosos',
                                  'De mayor tamaño',
                                  'Más aptos'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, el depredador natural de la vicuña '
                             'adulta es:',
                 'alternativas': ['El cóndor',
                                  'El oso de anteojos',
                                  'El zorro o atoq',
                                  'El puma',
                                  'El gato andino'],
                 'correcta': 'D'},
                {'pregunta': 'La relación donde un parásito usa a otro '
                             'organismo (hospedero) como fuente de alimento, '
                             'debilitándolo, se llama:',
                 'alternativas': ['Parasitismo',
                                  'Simbiosis',
                                  'Mutualismo',
                                  'Comensalismo',
                                  'Depredación'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando el parásito vive u obtiene alimento en '
                             'el exterior del hospedero, se llama:',
                 'alternativas': ['Histioparasitismo',
                                  'Hemoparasitismo',
                                  'Ectoparasitismo',
                                  'Enteroparasitismo',
                                  'Endoparasitismo'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando el parásito vive en el interior del '
                             'hospedero, se llama:',
                 'alternativas': ['Mutualismo',
                                  'Endoparasitismo',
                                  'Comensalismo',
                                  'Ectoparasitismo',
                                  'Foresia'],
                 'correcta': 'B'},
                {'pregunta': 'El protozoario Plasmodium vivax es un '
                             'hemoparásito que causa la enfermedad de la:',
                 'alternativas': ['Tuberculosis',
                                  'Malaria o paludismo',
                                  'Fiebre amarilla',
                                  'Fiebre tifoidea',
                                  'Leishmaniasis'],
                 'correcta': 'B'},
                {'pregunta': 'La Taenia solium y el Ascaris lumbricoides son '
                             'ejemplos de:',
                 'alternativas': ['Ectoparásitos',
                                  'Enteroparásitos',
                                  'Mutualistas',
                                  'Hemoparásitos exclusivos',
                                  'Depredadores'],
                 'correcta': 'B'},
                {'pregunta': 'El cisticerco de la Taenia solium, localizado '
                             'en tejidos como el músculo o el cerebro, causa '
                             'la enfermedad denominada:',
                 'alternativas': ['Amebiasis',
                                  'Cisticercosis',
                                  'Fascioliasis',
                                  'Paludismo',
                                  'Giardiasis'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE ECOLOGÍA / EL ECOLOGISMO Y SUS '
                                'TIPOS',
                      'items': ['«Ecología» proviene de los vocablos griegos '
                                '«oikos» (casa) y «logos» (ciencia).',
                                'El ecologismo es el activismo de la '
                                'ecología, un movimiento cívico para el '
                                'cuidado del ambiente.']},
                     {'titulo': 'FACTORES AMBIENTALES / EL ECOSISTEMA: '
                                'CONCEPTO Y TÉRMINOS RELACIONADOS',
                      'items': ['Los factores ambientales se clasifican en '
                                'bióticos y abióticos.',
                                'El término «ecosistema» fue acuñado por '
                                'Arthur Tansley en 1935, como el complejo de '
                                'organismos y factores físicos del '
                                'ambiente.']},
                     {'titulo': 'COMPONENTES ABIÓTICOS DEL ECOSISTEMA / '
                                'RELACIONES INTRAESPECÍFICAS',
                      'items': ['La luz solar es la fuente de energía de la '
                                'mayoría de los ecosistemas.',
                                'Las relaciones intraespecíficas u '
                                'homotípicas se dan entre individuos de la '
                                'misma especie.']},
                     {'titulo': 'RELACIONES INTERESPECÍFICAS / MUTUA '
                                'TOLERANCIA Y CONVIVENCIA',
                      'items': ['Las relaciones interespecíficas u '
                                'heterotípicas se dan entre individuos de '
                                'especies diferentes.',
                                'La foresia ocurre cuando un individuo se '
                                'deja transportar temporalmente por otra '
                                'especie, como los ácaros que se prenden de '
                                'insectos.']},
                     {'titulo': 'MUTUALISMO Y SIMBIOSIS / DEPREDACIÓN',
                      'items': ['El mutualismo beneficia a ambas especies; '
                                'puede ser facultativo (no imprescindible) u '
                                'obligado.',
                                'La depredación es el consumo de un '
                                'organismo viviente por otro, en la relación '
                                'presa-depredador.']},
                     {'titulo': 'PARASITISMO / FUNCIONES DE LOS ECOSISTEMAS: '
                                'SUCESIÓN ECOLÓGICA',
                      'items': ['El parasitismo es la relación donde un '
                                'organismo (parásito) usa a otro (hospedero) '
                                'como fuente de alimento, debilitándolo.',
                                'La sucesión ecológica es la secuencia de '
                                'cambios que experimenta un ecosistema a '
                                'través del tiempo.']},
                     {'titulo': 'ECOSISTEMAS DEL PERÚ',
                      'items': ['Los biomas son áreas climáticas definidas '
                                'con condiciones ecológicas similares.']}]},
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
                {'titulo': '14.5 NIVELES TRÓFICOS',
                 'items': ['El {primer} nivel trófico lo forman los '
                           '{productores}, organismos autótrofos que '
                           'fabrican su propio alimento.',
                           'El {segundo} nivel trófico lo forman los '
                           '{consumidores primarios} o herbívoros.',
                           'El {tercer} nivel trófico lo forman los '
                           '{consumidores secundarios} o carnívoros, también '
                           'llamados depredadores.',
                           'El animal del que se alimenta un depredador se '
                           'llama su {presa}.',
                           'El {cuarto} nivel trófico lo forman los '
                           'carroñeros o consumidores {terciarios}, como el '
                           'gallinazo y el cóndor.',
                           'Los organismos {omnívoros}, como el hombre, se '
                           'alimentan de plantas y carne a la vez.',
                           'Los {descomponedores} o desintegradores, como '
                           'hongos y bacterias, desintegran la materia '
                           'orgánica muerta.']},
                {'titulo': '14.6 CADENAS, REDES Y PIRÁMIDES TRÓFICAS',
                 'items': ['Una {cadena alimenticia} muestra cómo la energía '
                           'fluye de un organismo a otro a través de cada '
                           'nivel trófico.',
                           'En ecosistemas marinos, las cadenas tróficas '
                           'llegan hasta {6} eslabones; en ecosistemas '
                           'pequeños, hasta {3}.',
                           'El conjunto de todas las cadenas alimenticias '
                           'interconectadas de una comunidad forma una {red '
                           'trófica}.',
                           'Las {pirámides tróficas} muestran el flujo de '
                           'energía, con los {productores} en la base '
                           'representando la mayor energía.']},
                {'titulo': '14.7 CICLOS BIOGEOQUÍMICOS: CONCEPTO Y '
                           'CLASIFICACIÓN',
                 'items': ['Los {ciclos biogeoquímicos} son el movimiento '
                           'circular de elementos y compuestos entre el '
                           'ambiente y los organismos.',
                           'Se llaman biogeoquímicos porque involucran '
                           'componentes {geológicos}, biológicos y '
                           '{químicos}.',
                           'Los componentes geológicos son la {atmósfera}, '
                           'la litósfera y la {hidrósfera}.',
                           'Los ciclos {gaseosos}, como el carbono, oxígeno '
                           'y nitrógeno, tienen a la atmósfera como '
                           'principal reservorio.',
                           'Los ciclos {sedimentarios}, como el fósforo y el '
                           'azufre, tienen a las rocas sedimentarias como '
                           'reservorio y son más {lentos}.']},
                {'titulo': '14.8 EL CICLO DEL CARBONO',
                 'items': ['Los dos procesos básicos que participan en el '
                           'ciclo del carbono son la {fotosíntesis} y la '
                           'respiración {celular}.',
                           'Cada año se fijan aproximadamente {200} billones '
                           'de toneladas de carbono mediante fotosíntesis; '
                           'el 90% lo fijan las {algas} oceánicas.',
                           'Los {moluscos} combinan CO2 disuelto con calcio '
                           'para formar carbonato de calcio en sus '
                           '{conchas}.',
                           'Los {combustibles fósiles} —carbón, petróleo y '
                           'gas— se forman de restos orgánicos por presión y '
                           'temperatura durante millones de años.']},
                {'titulo': '14.9 EL CICLO DEL NITRÓGENO',
                 'items': ['La atmósfera está formada por aproximadamente '
                           '{78}% de gas nitrógeno libre (N2).',
                           'Las plantas y animales {no} pueden usar el '
                           'nitrógeno atmosférico directamente; debe '
                           'convertirse en {nitratos}.',
                           'El ciclo del nitrógeno incluye fijación, '
                           '{amonificación}, nitrificación y '
                           '{desnitrificación}.',
                           'En la {fijación} de nitrógeno, bacterias '
                           'convierten el N2 atmosférico en {amoníaco} '
                           '(NH3).',
                           'Las bacterias fijadoras de nitrógeno viven en '
                           'nódulos de las raíces de {leguminosas}, como el '
                           'frijol.']},
                {'titulo': '14.10 EL CICLO HIDROLÓGICO',
                 'items': ['El {ciclo hidrológico}, o ciclo del agua, es el '
                           'movimiento repetido de agua entre la superficie '
                           'de la Tierra y la {atmósfera}.',
                           'El mayor reservorio de agua en el mundo es el '
                           '{océano}, que contiene más del {97}% del agua '
                           'disponible.',
                           'El ciclo hidrológico es posible gracias a la '
                           'energía {solar}, que evapora el agua, y la '
                           '{gravedad}, que la regresa a la tierra.',
                           'El agua evaporada entra a la atmósfera como '
                           '{vapor de agua}; al enfriarse, se {condensa} y '
                           'forma nubes.',
                           'Las nubes retornan el agua a la tierra como '
                           '{precipitación}, en forma de lluvia, nieve o '
                           'granizo.',
                           'Parte del agua precipitada es tomada por plantas '
                           'y animales; otra alimenta cuerpos de agua '
                           '{superficiales} y subterráneos (mantos '
                           'freáticos).',
                           'Las plantas eliminan agua a través de las hojas '
                           'mediante la {transpiración}; los animales la '
                           'eliminan por el sudor, la exhalación y la '
                           '{orina}.']}],
  'cuadros': [{'titulo': '14.2 LAS DOS LEYES DE LA TERMODINÁMICA',
               'encabezados': ['Ley', 'Ejemplo'],
               'filas': [['{Primera} ley',
                          'La luz se transforma en materia orgánica por '
                          '{fotosíntesis}, y esta en calor y luz'],
                         ['{Segunda} ley',
                          'Al quemar carbón, parte de la energía crea vapor '
                          'y otra se dispersa como {calor}']]}],
  'preguntas': [{'pregunta': 'La energía solar llega a la Tierra en forma de '
                             'partículas energéticas llamadas:',
                 'alternativas': ['Neutrones',
                                  'Fotones',
                                  'Iones',
                                  'Quarks',
                                  'Electrones'],
                 'correcta': 'B'},
                {'pregunta': 'La energía en movimiento, como la energía '
                             'mecánica o el calor, se llama energía:',
                 'alternativas': ['Cinética',
                                  'Nuclear exclusiva',
                                  'Potencial',
                                  'Química exclusiva',
                                  'Radiante exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La energía almacenada, disponible para llevar '
                             'a cabo trabajo, se llama energía:',
                 'alternativas': ['Mecánica exclusiva',
                                  'Lumínica exclusiva',
                                  'Potencial',
                                  'Térmica exclusiva',
                                  'Cinética'],
                 'correcta': 'C'},
                {'pregunta': 'Los ecosistemas son sistemas '
                             'termodinámicamente:',
                 'alternativas': ['Estáticos',
                                  'Abiertos',
                                  'Cerrados',
                                  'Aislados',
                                  'Neutros'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ley de la termodinámica también se '
                             'conoce como el principio de:',
                 'alternativas': ['La herencia',
                                  'La conservación de la energía',
                                  'La selección natural',
                                  'El diezmo ecológico',
                                  'La entropía'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ley de la termodinámica fue '
                             'postulada en 1841 por:',
                 'alternativas': ['R. Mayer',
                                  'Dobzhansky',
                                  'Darwin',
                                  'Mendel',
                                  'Haeckel'],
                 'correcta': 'A'},
                {'pregunta': 'Según la primera ley de la termodinámica, la '
                             'energía:',
                 'alternativas': ['Desaparece con el tiempo',
                                  'No se crea ni se destruye, solo se '
                                  'transforma',
                                  'Se multiplica en cada transformación',
                                  'Se crea constantemente',
                                  'Se pierde totalmente en cada ciclo'],
                 'correcta': 'B'},
                {'pregunta': 'La segunda ley de la termodinámica también se '
                             'conoce como ley de:',
                 'alternativas': ['La selección natural',
                                  'El diezmo ecológico',
                                  'La entropía o degradación de la energía',
                                  'La conservación de la energía',
                                  'La herencia'],
                 'correcta': 'C'},
                {'pregunta': 'Según la segunda ley de la termodinámica, al '
                             'transformarse la energía:',
                 'alternativas': ['Desaparece por completo',
                                  'Se conserva completamente aprovechable',
                                  'Se transforma en materia',
                                  'Aumenta su cantidad total',
                                  'Parte se degrada en una forma no '
                                  'trasladable'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando la energía se transfiere de un '
                             'organismo a otro en la cadena alimenticia, '
                             'gran parte se degrada en forma de:',
                 'alternativas': ['Electricidad',
                                  'Luz',
                                  'Materia sólida',
                                  'Calor',
                                  'Sonido'],
                 'correcta': 'D'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, al pasar de '
                             'un nivel trófico a otro se transfiere:',
                 'alternativas': ['El 1% de la energía',
                                  'El 100% de la energía',
                                  'El 50% de la energía',
                                  'El 10% de la energía',
                                  'El 90% de la energía'],
                 'correcta': 'D'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, los '
                             'organismos usan en su propio metabolismo:',
                 'alternativas': ['Ninguna energía',
                                  'El 90% de la energía capturada',
                                  'El 50% de la energía capturada',
                                  'El 10% de la energía capturada',
                                  'Toda la energía capturada'],
                 'correcta': 'B'},
                {'pregunta': 'Un vegetal aprovecha para sus funciones de '
                             'supervivencia aproximadamente:',
                 'alternativas': ['100% de la energía solar',
                                  '1% de la energía solar',
                                  '10% de la energía solar fijada',
                                  '90% de la energía solar fijada',
                                  '50% de la energía solar fijada'],
                 'correcta': 'D'},
                {'pregunta': 'Un herbívoro que consume un vegetal solo puede '
                             'aprovechar de la energía fijada por este:',
                 'alternativas': ['El 100%',
                                  'El 90%',
                                  'El 1%',
                                  'El 10%',
                                  'El 50%'],
                 'correcta': 'D'},
                {'pregunta': 'Un carnívoro que consume a un herbívoro solo '
                             'puede aprovechar de la energía que este '
                             'recibió:',
                 'alternativas': ['El 100%',
                                  'El 90%',
                                  'El 50%',
                                  'El 5%',
                                  'El 10%'],
                 'correcta': 'E'},
                {'pregunta': 'El porcentaje aproximado de la energía '
                             'disponible en la Tierra que proviene del sol '
                             'es:',
                 'alternativas': ['50%', '10%', '75%', '99,98%', '25%'],
                 'correcta': 'D'},
                {'pregunta': 'Además del sol, otras fuentes de energía '
                             'terrestre incluyen las mareas, la energía '
                             'nuclear, la termal y la:',
                 'alternativas': ['Potencial exclusiva',
                                  'Cinética exclusiva',
                                  'Radiante exclusiva de origen solar',
                                  'Química exclusiva',
                                  'Gravitacional'],
                 'correcta': 'E'},
                {'pregunta': 'La radiación solar que llega a la superficie '
                             'terrestre varía según la latitud, la altura, '
                             'la orografía y:',
                 'alternativas': ['El color del suelo',
                                  'La nubosidad',
                                  'La profundidad marina',
                                  'El tipo de roca',
                                  'La velocidad de rotación'],
                 'correcta': 'B'},
                {'pregunta': 'La historia de la energía en un ecosistema '
                             'está en gran parte relacionada con la historia '
                             'de:',
                 'alternativas': ['El oxígeno puro',
                                  'El carbono',
                                  'El nitrógeno',
                                  'El fósforo',
                                  'El azufre'],
                 'correcta': 'B'},
                {'pregunta': 'La energía almacenada en los enlaces químicos '
                             'de los carbohidratos proviene originalmente '
                             'de:',
                 'alternativas': ['La fotosíntesis',
                                  'La quimiosíntesis exclusiva',
                                  'La glucólisis',
                                  'La descomposición',
                                  'La respiración celular'],
                 'correcta': 'A'},
                {'pregunta': 'El primer nivel trófico está formado por:',
                 'alternativas': ['Los carroñeros',
                                  'Los descomponedores',
                                  'Los omnívoros',
                                  'Los productores u organismos autótrofos',
                                  'Los carnívoros'],
                 'correcta': 'D'},
                {'pregunta': 'El segundo nivel trófico está formado por:',
                 'alternativas': ['Los productores',
                                  'Los carroñeros',
                                  'Los consumidores primarios o herbívoros',
                                  'Los descomponedores',
                                  'Los carnívoros'],
                 'correcta': 'C'},
                {'pregunta': 'El tercer nivel trófico está formado por los '
                             'consumidores secundarios, también llamados:',
                 'alternativas': ['Herbívoros',
                                  'Productores',
                                  'Omnívoros exclusivos',
                                  'Descomponedores',
                                  'Depredadores o carnívoros'],
                 'correcta': 'E'},
                {'pregunta': 'El animal del que se alimenta un depredador se '
                             'llama su:',
                 'alternativas': ['Presa',
                                  'Hospedero',
                                  'Parásito',
                                  'Simbionte',
                                  'Huésped'],
                 'correcta': 'A'},
                {'pregunta': 'Los organismos que se alimentan tanto de '
                             'plantas como de carne se llaman:',
                 'alternativas': ['Omnívoros',
                                  'Descomponedores',
                                  'Detritívoros exclusivos',
                                  'Herbívoros',
                                  'Carnívoros puros'],
                 'correcta': 'A'},
                {'pregunta': 'Los hongos y bacterias que desintegran materia '
                             'orgánica muerta se llaman:',
                 'alternativas': ['Herbívoros',
                                  'Productores',
                                  'Consumidores secundarios',
                                  'Descomponedores',
                                  'Consumidores primarios'],
                 'correcta': 'D'},
                {'pregunta': 'Una cadena alimenticia muestra cómo fluye la '
                             'energía de un organismo a otro a través de:',
                 'alternativas': ['Un solo nivel trófico',
                                  'Ningún nivel definido',
                                  'Solo los productores',
                                  'Cada nivel trófico',
                                  'Solo los depredadores'],
                 'correcta': 'D'},
                {'pregunta': 'En ecosistemas marinos, las cadenas tróficas '
                             'pueden llegar hasta:',
                 'alternativas': ['20 eslabones',
                                  '6 eslabones',
                                  '1 eslabón',
                                  '10 eslabones',
                                  '2 eslabones'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de todas las cadenas alimenticias '
                             'interconectadas de una comunidad forma:',
                 'alternativas': ['Una red trófica',
                                  'Un nicho ecológico',
                                  'Un bioma',
                                  'Una pirámide trófica',
                                  'Una ecorregión'],
                 'correcta': 'A'},
                {'pregunta': 'En las pirámides tróficas, los productores se '
                             'ubican en:',
                 'alternativas': ['Fuera de la pirámide',
                                  'La cúspide',
                                  'No aparecen',
                                  'El centro',
                                  'La base'],
                 'correcta': 'E'},
                {'pregunta': 'Los ciclos biogeoquímicos se definen como el '
                             'movimiento circular de elementos entre:',
                 'alternativas': ['Solo la atmósfera',
                                  'Solo el suelo',
                                  'Solo el agua',
                                  'Solo los organismos',
                                  'El ambiente y los organismos'],
                 'correcta': 'E'},
                {'pregunta': 'Los ciclos biogeoquímicos involucran '
                             'componentes geológicos, biológicos y:',
                 'alternativas': ['Políticos',
                                  'Culturales',
                                  'Económicos',
                                  'Químicos',
                                  'Sociales'],
                 'correcta': 'D'},
                {'pregunta': 'Los componentes geológicos de los ciclos '
                             'biogeoquímicos son atmósfera, litósfera e:',
                 'alternativas': ['Termósfera',
                                  'Hidrósfera',
                                  'Estratósfera',
                                  'Ionósfera',
                                  'Exósfera'],
                 'correcta': 'B'},
                {'pregunta': 'Los ciclos que tienen a la atmósfera como '
                             'principal reservorio se llaman ciclos:',
                 'alternativas': ['Orgánicos exclusivos',
                                  'Hídricos exclusivos',
                                  'Gaseosos',
                                  'Minerales exclusivos',
                                  'Sedimentarios'],
                 'correcta': 'C'},
                {'pregunta': 'Los ciclos que tienen a las rocas '
                             'sedimentarias como reservorio, y son más '
                             'lentos, se llaman ciclos:',
                 'alternativas': ['Sedimentarios',
                                  'Atmosféricos',
                                  'Gaseosos',
                                  'Rápidos',
                                  'Hídricos'],
                 'correcta': 'A'},
                {'pregunta': 'Los dos procesos básicos que participan en el '
                             'ciclo del carbono son fotosíntesis y:',
                 'alternativas': ['Respiración celular',
                                  'Excreción',
                                  'Fermentación',
                                  'Digestión',
                                  'Transcripción'],
                 'correcta': 'A'},
                {'pregunta': 'La mayor parte del carbono fijado anualmente '
                             'por fotosíntesis, un 90%, es fijado por:',
                 'alternativas': ['Los animales',
                                  'Las algas oceánicas',
                                  'Las bacterias del suelo',
                                  'Los hongos',
                                  'Los bosques'],
                 'correcta': 'B'},
                {'pregunta': 'Los moluscos combinan CO2 disuelto con calcio '
                             'para formar:',
                 'alternativas': ['Dióxido de carbono puro',
                                  'Metano',
                                  'Carbonato de calcio en sus conchas',
                                  'Bicarbonato de sodio',
                                  'Ácido carbónico'],
                 'correcta': 'C'},
                {'pregunta': 'Los combustibles fósiles, como el carbón y el '
                             'petróleo, se forman de restos orgánicos '
                             'transformados por:',
                 'alternativas': ['Radiación solar directa',
                                  'Fotosíntesis directa',
                                  'Alta temperatura y presión durante '
                                  'millones de años',
                                  'Reacciones químicas instantáneas',
                                  'Congelación'],
                 'correcta': 'C'},
                {'pregunta': 'La atmósfera está formada por gas nitrógeno '
                             'libre en una proporción aproximada de:',
                 'alternativas': ['95%', '10%', '50%', '21%', '78%'],
                 'correcta': 'E'},
                {'pregunta': 'Las plantas y animales no pueden usar '
                             'directamente el nitrógeno atmosférico porque '
                             'debe convertirse primero en:',
                 'alternativas': ['Dióxido de carbono',
                                  'Nitratos',
                                  'Oxígeno',
                                  'Metano',
                                  'Ozono'],
                 'correcta': 'B'},
                {'pregunta': 'El ciclo del nitrógeno incluye los procesos de '
                             'fijación, amonificación, nitrificación y:',
                 'alternativas': ['Desnitrificación',
                                  'Respiración',
                                  'Fermentación',
                                  'Fotosíntesis',
                                  'Glucólisis'],
                 'correcta': 'A'},
                {'pregunta': 'En la fijación de nitrógeno, las bacterias '
                             'convierten el N2 atmosférico en:',
                 'alternativas': ['Oxígeno',
                                  'Nitratos directamente',
                                  'Ácido sulfúrico',
                                  'Amoníaco (NH3)',
                                  'Dióxido de carbono'],
                 'correcta': 'D'},
                {'pregunta': 'Las bacterias fijadoras de nitrógeno viven en '
                             'nódulos de las raíces de plantas llamadas:',
                 'alternativas': ['Coníferas',
                                  'Helechos',
                                  'Gramíneas',
                                  'Leguminosas, como el frijol',
                                  'Cactáceas'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando se quema carbón en una caldera, parte '
                             'de la energía crea vapor mientras que la otra '
                             'se dispersa como calor; esto ilustra:',
                 'alternativas': ['La ley de conservación de la masa',
                                  'La Ley del Diezmo Ecológico',
                                  'La fotosíntesis',
                                  'La primera ley de la termodinámica',
                                  'La segunda ley de la termodinámica'],
                 'correcta': 'E'},
                {'pregunta': 'El ciclo hidrológico, o ciclo del agua, es el '
                             'movimiento repetido de agua entre la '
                             'superficie de la Tierra y la:',
                 'alternativas': ['Biosfera exclusiva',
                                  'Hidrosfera exclusiva',
                                  'Litosfera',
                                  'Estratosfera',
                                  'Atmósfera'],
                 'correcta': 'E'},
                {'pregunta': 'Uno de los reservorios para el ciclo del agua '
                             'en nuestro planeta, el mayor de todos, viene a '
                             'ser:',
                 'alternativas': ['Los ríos con 90% del agua del planeta',
                                  'Los lagos, ríos y aguas subterráneas con '
                                  '10%',
                                  'Los océanos con más del 97% del agua '
                                  'disponible',
                                  'El agua de la atmósfera con 5%',
                                  'Los glaciares y capas de hielo polar con '
                                  'cerca de 2%'],
                 'correcta': 'C'},
                {'pregunta': 'El ciclo hidrológico es posible gracias a la '
                             'energía solar, que evapora el agua, y a la:',
                 'alternativas': ['Rotación terrestre',
                                  'Presión atmosférica',
                                  'Radiación ultravioleta',
                                  'Gravedad',
                                  'Fotosíntesis'],
                 'correcta': 'D'},
                {'pregunta': 'El agua evaporada entra a la atmósfera como un '
                             'gas llamado:',
                 'alternativas': ['Nitrógeno',
                                  'Oxígeno',
                                  'Ozono',
                                  'Vapor de agua',
                                  'Dióxido de carbono'],
                 'correcta': 'D'},
                {'pregunta': 'En la atmósfera, el vapor de agua se enfría y '
                             'se condensa para formar:',
                 'alternativas': ['Lluvia directamente',
                                  'Granizo directamente',
                                  'Nubes',
                                  'Rocío exclusivamente',
                                  'Neblina exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Las plantas eliminan agua hacia la atmósfera a '
                             'través de las hojas mediante el proceso de:',
                 'alternativas': ['Transpiración',
                                  'Ósmosis',
                                  'Respiración exclusiva',
                                  'Absorción',
                                  'Fotosíntesis'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'ENERGÍA CINÉTICA Y POTENCIAL / LEYES DE LA '
                                'TERMODINÁMICA',
                      'items': ['La energía solar llega a la Tierra en '
                                'partículas energéticas llamadas fotones.',
                                'Los ecosistemas son sistemas '
                                'termodinámicamente abiertos: la energía y '
                                'materia entran y salen de ellos.']},
                     {'titulo': 'LA LEY DEL DIEZMO ECOLÓGICO / EL FLUJO DE '
                                'ENERGÍA',
                      'items': ['Según la Ley del Diezmo Ecológico, al pasar '
                                'de un nivel trófico a otro, solo se '
                                'transfiere el 10% de la energía.',
                                'Aproximadamente el 99,98% de la energía '
                                'disponible en la Tierra proviene del sol.']},
                     {'titulo': 'NIVELES TRÓFICOS / CADENAS, REDES Y '
                                'PIRÁMIDES TRÓFICAS',
                      'items': ['El primer nivel trófico lo forman los '
                                'productores, organismos autótrofos que '
                                'fabrican su propio alimento.',
                                'Una cadena alimenticia muestra cómo la '
                                'energía fluye de un organismo a otro a '
                                'través de cada nivel trófico.']},
                     {'titulo': 'CICLOS BIOGEOQUÍMICOS: CONCEPTO Y '
                                'CLASIFICACIÓN / EL CICLO DEL CARBONO',
                      'items': ['Los ciclos biogeoquímicos son el movimiento '
                                'circular de elementos y compuestos entre el '
                                'ambiente y los organismos.',
                                'Los dos procesos básicos que participan en '
                                'el ciclo del carbono son la fotosíntesis y '
                                'la respiración celular.']},
                     {'titulo': 'EL CICLO DEL NITRÓGENO / EL CICLO '
                                'HIDROLÓGICO',
                      'items': ['La atmósfera está formada por '
                                'aproximadamente 78% de gas nitrógeno libre '
                                '(N2).',
                                'El ciclo hidrológico, o ciclo del agua, es '
                                'el movimiento repetido de agua entre la '
                                'superficie de la Tierra y la atmósfera.']}]},
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
                {'titulo': '15.3 BENEFICIOS DE LA DIVERSIDAD BIOLÓGICA',
                 'items': ['Los servicios de {aprovisionamiento} suministran '
                           'bienes con valor monetario directo: alimentos, '
                           'agua, madera.',
                           'Los servicios {reguladores} incluyen la '
                           'regulación del clima, el control de erosión y la '
                           '{polinización}.',
                           'Los servicios {culturales} incluyen valor '
                           'espiritual, recreación, ecoturismo y '
                           '{educación}.',
                           'Los servicios de {apoyo} o soporte son '
                           'esenciales para el ecosistema: formación de '
                           'suelos, ciclos de nutrientes.',
                           'En el Perú, la {pesquería} es una de las '
                           'actividades más rentables relacionadas con la '
                           'biodiversidad.']},
                {'titulo': '15.4 PELIGROS PARA LA DIVERSIDAD BIOLÓGICA',
                 'items': ['La causa principal de extinción de especies es '
                           'la {destrucción} del hábitat por expansión de '
                           'poblaciones humanas.',
                           'Entre las causas de pérdida de biodiversidad '
                           'están el cambio de uso de suelo, la '
                           '{sobreexplotación} de recursos, y especies '
                           '{exóticas invasivas}.',
                           'En el Perú, el cambio de uso de suelo por '
                           'monocultivos y {deforestación} afecta gravemente '
                           'la Amazonía.',
                           'Otro peligro es la introducción de {organismos '
                           'vivos modificados} (OVM).']},
                {'titulo': '15.5 EL PERÚ COMO PAÍS MEGADIVERSO',
                 'items': ['El {Perú} es uno de los cinco países con mayor '
                           'diversidad biológica del mundo, y uno de los '
                           '{doce} países megadiversos.',
                           'Los países megadiversos poseen el {70}% de la '
                           'biodiversidad del mundo; entre ellos están '
                           'Brasil, Colombia, México y {Perú}.',
                           'La megadiversidad del Perú se debe a su '
                           'ubicación entre el Ecuador y el trópico, la '
                           'Cordillera de los {Andes}, y las corrientes '
                           'marinas fría y {cálida}.',
                           'El Perú es centro mundial de origen de la '
                           '{agricultura} y la ganadería; los cultivos más '
                           'antiguos se hallan en la cueva {Guitarrero} '
                           '(Ancash) y en Chilca.']},
                {'titulo': '15.6 RECURSOS GENÉTICOS DEL PERÚ',
                 'items': ['El Perú posee al menos {182} especies de plantas '
                           'domesticadas, como la papa, el tomate, el camote '
                           'y el {maíz}.',
                           'El Perú es el primer país en variedades de '
                           '{papa} (unas 3000) y de maíz (36 {ecotipos}).',
                           'De la papa existen {9} especies domesticadas con '
                           'unas 3000 variedades, y unas 85 especies '
                           '{silvestres}.']},
                {'titulo': '15.7 DIVERSIDAD DE FLORA EN EL PERÚ',
                 'items': ['El Perú posee al menos {20 533} especies de '
                           'plantas, de las cuales un {30}% son endémicas.',
                           'El Perú es primero en el mundo en número de '
                           'especies de {orquídeas}, y posee la orquídea más '
                           'grande del planeta, en {Huachucolpa}, '
                           'Huancavelica.',
                           'El Perú posee la planta con el fruto más grande '
                           'de la Tierra, el {zapallo macre}, que puede '
                           'pesar más de {70} kg.']},
                {'titulo': '15.8 DIVERSIDAD DE FAUNA EN EL PERÚ',
                 'items': ['El Perú es {primero} en el mundo en número de '
                           'especies de peces (1200) y de {mariposas}.',
                           'El Perú es {segundo} en el mundo en variedad de '
                           'aves (1857 especies) y en primates ({34} '
                           'especies).',
                           'El Perú es {tercero} en el mundo en anfibios y '
                           'en {mamíferos}.',
                           'El mono choro de cola amarilla es un primate '
                           '{endémico} del Perú.',
                           'El {mar peruano} es una de las siete cuencas '
                           'pesqueras marinas del mundo, conocido como «una '
                           'sopa de {plancton}» por su cantidad de '
                           'nutrientes.',
                           'El Perú posee seis formas de animales '
                           'domésticos, entre ellas la {alpaca} (forma '
                           'doméstica de la vicuña) y la {llama} (forma '
                           'doméstica del guanaco).']},
                {'titulo': '15.9 DETERIORO DE LA FLORA Y FAUNA',
                 'items': ['La flora y fauna son recursos naturales '
                           '{renovables}, que se regeneran por reproducción '
                           'o {propagación}.',
                           'El uso insostenible de flora y fauna genera '
                           'deterioro de {hábitat}, extinción de especies y '
                           'erosión {genética}.',
                           'La {erosión genética} es la pérdida o reducción '
                           'de la {variabilidad genética} de una especie.',
                           'Una causa de erosión genética es la introducción '
                           'de variedades {exóticas} en lugar de las '
                           'nativas.',
                           'La {chinchilla} es un caso emblemático de '
                           'especie extinta en su hábitat natural andino por '
                           'sobreexplotación.']},
                {'titulo': '15.10 TIPOS DE DETERIORO',
                 'items': ['El {uso excesivo de biomasa} es la utilización '
                           'insostenible de materia orgánica de plantas y '
                           'animales.',
                           'La {extracción selectiva} sin control afecta '
                           'especies de alta demanda comercial, como el '
                           '{cedro} y la caoba.',
                           'Entre la fauna afectada por extracción selectiva '
                           'están la {vicuña}, el lobo marino y la tortuga '
                           '{charapa}.',
                           'La {pesca no planificada} es la pesca '
                           'insostenible sin respetar las épocas de '
                           '{veda}.']}],
  'cuadros': [{'titulo': '15.2 LOS TRES COMPONENTES DE LA BIODIVERSIDAD',
               'encabezados': ['Componente', 'Se refiere a'],
               'filas': [['{Genética}',
                          'Diferencias en el material {genético}'],
                         ['De {especies}', 'Número de {especies} en un área'],
                         ['De {ecosistemas}',
                          'Variedad de sistemas {ecológicos}']]}],
  'preguntas': [{'pregunta': 'El Convenio sobre la Diversidad Biológica se '
                             'celebró en el marco de la conocida como:',
                 'alternativas': ['Protocolo de Montreal',
                                  'Cumbre de París',
                                  'Cumbre de la Tierra',
                                  'Conferencia de Kioto',
                                  'Acuerdo de Copenhague'],
                 'correcta': 'C'},
                {'pregunta': 'La Cumbre de la Tierra, donde se celebró el '
                             'CDB, se llevó a cabo en:',
                 'alternativas': ['Ginebra, Suiza',
                                  'Nagoya, Japón',
                                  'Nueva York, EE.UU.',
                                  'Río de Janeiro, Brasil',
                                  'Lima, Perú'],
                 'correcta': 'D'},
                {'pregunta': 'El Convenio sobre la Diversidad Biológica se '
                             'celebró en el año:',
                 'alternativas': ['2000', '1992', '1972', '1985', '2010'],
                 'correcta': 'B'},
                {'pregunta': 'El CDB define la diversidad biológica como la '
                             'variabilidad de:',
                 'alternativas': ['Solo especies animales',
                                  'Solo especies marinas',
                                  'Solo microorganismos',
                                  'Solo especies vegetales',
                                  'Organismos vivos de cualquier fuente'],
                 'correcta': 'E'},
                {'pregunta': 'Según el CDB, la conservación de la diversidad '
                             'biológica es interés:',
                 'alternativas': ['Exclusivo de los países desarrollados',
                                  'Solo científico',
                                  'Solo de organismos ambientales',
                                  'Solo económico',
                                  'Común de toda la humanidad'],
                 'correcta': 'E'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica 2011-2020 fue adoptado en:',
                 'alternativas': ['Río de Janeiro',
                                  'París',
                                  'Nagoya, Japón',
                                  'Ginebra',
                                  'Nueva York'],
                 'correcta': 'C'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica fue adoptado en el año:',
                 'alternativas': ['1992', '2020', '2000', '2010', '1985'],
                 'correcta': 'D'},
                {'pregunta': 'Como parte del Plan Estratégico, se trazaron '
                             'las metas conocidas como:',
                 'alternativas': ['Metas de Copenhague',
                                  'Metas de Kioto',
                                  'Metas de París',
                                  'Metas de Aichi',
                                  'Metas de Montreal'],
                 'correcta': 'D'},
                {'pregunta': 'El Día Internacional de la Diversidad '
                             'Biológica se celebra el:',
                 'alternativas': ['22 de abril',
                                  '1 de enero',
                                  '22 de mayo',
                                  '5 de junio',
                                  '10 de diciembre'],
                 'correcta': 'C'},
                {'pregunta': 'La biodiversidad comprende tres componentes: '
                             'genética, de especies y de:',
                 'alternativas': ['Climas',
                                  'Ecosistemas',
                                  'Océanos',
                                  'Continentes',
                                  'Suelos'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad genética se refiere a las '
                             'diferencias en:',
                 'alternativas': ['La cantidad de ecosistemas',
                                  'El material genético entre poblaciones e '
                                  'individuos',
                                  'El número de especies',
                                  'La ubicación geográfica',
                                  'El tipo de clima'],
                 'correcta': 'B'},
                {'pregunta': 'La diversidad de especies se refiere al número '
                             'de especies diferentes presentes en:',
                 'alternativas': ['Un área determinada',
                                  'Todo el planeta exclusivamente',
                                  'Solo un país',
                                  'Solo un continente',
                                  'Solo un océano'],
                 'correcta': 'A'},
                {'pregunta': 'La diversidad de especies tiene dos '
                             'componentes: la riqueza de especies y:',
                 'alternativas': ['El tipo de suelo',
                                  'El clima',
                                  'El tamaño del área',
                                  'Sus abundancias relativas',
                                  'La ubicación'],
                 'correcta': 'D'},
                {'pregunta': 'La diversidad de ecosistemas se refiere a la '
                             'variedad de:',
                 'alternativas': ['Genes específicos',
                                  'Sistemas ecológicos en una región',
                                  'Climas exclusivamente',
                                  'Especies individuales',
                                  'Recursos minerales'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú es reconocido como un centro mundial '
                             'de origen de recursos genéticos de plantas '
                             'como:',
                 'alternativas': ['La vid y el olivo',
                                  'El trigo y la cebada',
                                  'El café y el cacao exclusivamente',
                                  'El arroz y la soya',
                                  'La papa, el maíz y el tomate'],
                 'correcta': 'E'},
                {'pregunta': 'La riqueza genética del Perú está asociada con '
                             'la riqueza cultural desarrollada por:',
                 'alternativas': ['Empresas multinacionales',
                                  'Organismos internacionales',
                                  'Los pueblos indígenas',
                                  'Colonizadores europeos',
                                  'Científicos extranjeros'],
                 'correcta': 'C'},
                {'pregunta': 'La distribución global de la diversidad de '
                             'especies depende de gradientes latitudinales, '
                             'de altitud y de:',
                 'alternativas': ['Densidad urbana',
                                  'Actividad industrial',
                                  'Comercio internacional',
                                  'Precipitación',
                                  'Población humana'],
                 'correcta': 'D'},
                {'pregunta': 'La conservación de la biodiversidad está '
                             'íntimamente asociada con el uso de:',
                 'alternativas': ['Solo la tecnología',
                                  'Los recursos naturales y la tierra',
                                  'Solo la política exterior',
                                  'Solo el capital financiero',
                                  'Solo el comercio internacional'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando las actividades humanas se incrementan '
                             'por encima de cierto umbral, los efectos sobre '
                             'los sistemas naturales son:',
                 'alternativas': ['Más significativos y prolongados',
                                  'Insignificantes',
                                  'Inexistentes',
                                  'Siempre positivos',
                                  'Reversibles automáticamente'],
                 'correcta': 'A'},
                {'pregunta': 'Además de los tres componentes clásicos, en la '
                             'actualidad se reconoce también como componente '
                             'de la biodiversidad a la diversidad:',
                 'alternativas': ['Cultural',
                                  'Militar',
                                  'Política',
                                  'Religiosa',
                                  'Económica'],
                 'correcta': 'A'},
                {'pregunta': 'Los servicios que suministran bienes con valor '
                             'monetario directo, como alimentos y madera, se '
                             'llaman servicios de:',
                 'alternativas': ['Culturales',
                                  'Ninguno de los anteriores',
                                  'Regulación',
                                  'Apoyo',
                                  'Aprovisionamiento'],
                 'correcta': 'E'},
                {'pregunta': 'Los servicios que incluyen la regulación del '
                             'clima y la polinización se llaman servicios:',
                 'alternativas': ['De aprovisionamiento',
                                  'Reguladores',
                                  'De apoyo',
                                  'Ninguno de los anteriores',
                                  'Culturales'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios que incluyen valor espiritual, '
                             'recreación y ecoturismo se llaman servicios:',
                 'alternativas': ['Culturales',
                                  'De apoyo',
                                  'Reguladores',
                                  'De aprovisionamiento',
                                  'Ninguno de los anteriores'],
                 'correcta': 'A'},
                {'pregunta': 'Los servicios esenciales para el '
                             'funcionamiento del ecosistema, como la '
                             'formación de suelos, se llaman servicios de:',
                 'alternativas': ['Regulación',
                                  'Aprovisionamiento',
                                  'Ninguno de los anteriores',
                                  'Apoyo o soporte',
                                  'Cultura'],
                 'correcta': 'D'},
                {'pregunta': 'En el Perú, una de las actividades más '
                             'rentables relacionadas con la biodiversidad '
                             'es:',
                 'alternativas': ['La pesquería',
                                  'La minería exclusiva',
                                  'La industria textil',
                                  'El comercio internacional',
                                  'La banca'],
                 'correcta': 'A'},
                {'pregunta': 'La causa principal de extinción de especies en '
                             'la actualidad es:',
                 'alternativas': ['Los desastres naturales exclusivos',
                                  'La competencia natural exclusiva',
                                  'La destrucción del hábitat por '
                                  'actividades humanas',
                                  'El cambio de estaciones',
                                  'Las enfermedades exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las causas de pérdida de biodiversidad '
                             'figuran el cambio de uso de suelo y:',
                 'alternativas': ['El crecimiento de bosques',
                                  'El aumento de áreas protegidas',
                                  'La sobreexplotación de recursos bióticos',
                                  'La conservación estricta',
                                  'La reforestación'],
                 'correcta': 'C'},
                {'pregunta': 'En la Amazonía peruana, el cambio de uso de '
                             'suelo se debe principalmente a monocultivos '
                             'extensivos y:',
                 'alternativas': ['El turismo sostenible',
                                  'La protección estatal',
                                  'La investigación científica',
                                  'La reforestación',
                                  'La deforestación por tala y quema'],
                 'correcta': 'E'},
                {'pregunta': 'Un peligro adicional para la biodiversidad es '
                             'la introducción de:',
                 'alternativas': ['Organismos vivos modificados (OVM)',
                                  'Reservas comunales',
                                  'Especies nativas',
                                  'Parques nacionales',
                                  'Áreas protegidas'],
                 'correcta': 'A'},
                {'pregunta': 'La flora y la fauna son recursos naturales:',
                 'alternativas': ['Inexistentes en el Perú',
                                  'No renovables',
                                  'Inagotables sin límite',
                                  'Renovables',
                                  'Artificiales'],
                 'correcta': 'D'},
                {'pregunta': 'La pérdida o reducción de la variabilidad '
                             'genética de una especie se llama:',
                 'alternativas': ['Deriva génica',
                                  'Mutación dirigida',
                                  'Especiación',
                                  'Erosión genética',
                                  'Selección natural'],
                 'correcta': 'D'},
                {'pregunta': 'Una causa de erosión genética es la '
                             'introducción de variedades exóticas en lugar '
                             'de:',
                 'alternativas': ['Ninguna variedad',
                                  'Las variedades nativas o locales',
                                  'Variedades importadas',
                                  'Variedades híbridas',
                                  'Variedades transgénicas'],
                 'correcta': 'B'},
                {'pregunta': 'La chinchilla es un ejemplo emblemático de '
                             'especie extinta en su hábitat andino debido a:',
                 'alternativas': ['La migración voluntaria',
                                  'Una enfermedad viral',
                                  'El cambio climático exclusivo',
                                  'La competencia natural',
                                  'La sobreexplotación'],
                 'correcta': 'E'},
                {'pregunta': 'El uso excesivo de biomasa se refiere a la '
                             'utilización insostenible de materia orgánica '
                             'de:',
                 'alternativas': ['Solo rocas',
                                  'Plantas y animales',
                                  'Solo minerales',
                                  'Solo aire',
                                  'Solo agua'],
                 'correcta': 'B'},
                {'pregunta': 'La extracción selectiva sin control afecta '
                             'especies de alta demanda comercial como el '
                             'cedro y:',
                 'alternativas': ['El eucalipto',
                                  'El ciprés',
                                  'La caoba',
                                  'El sauce',
                                  'El pino'],
                 'correcta': 'C'},
                {'pregunta': 'Entre la fauna peruana afectada por extracción '
                             'selectiva figuran la vicuña y:',
                 'alternativas': ['La paloma común',
                                  'La rana común',
                                  'El ratón',
                                  'La tortuga charapa',
                                  'El gato doméstico'],
                 'correcta': 'D'},
                {'pregunta': 'La pesca insostenible que no respeta las '
                             'épocas de veda se llama:',
                 'alternativas': ['Pesca artesanal',
                                  'Pesca no planificada',
                                  'Pesca sostenible',
                                  'Acuicultura',
                                  'Pesca deportiva'],
                 'correcta': 'B'},
                {'pregunta': 'Especies como la anchoveta, sardina y merluza '
                             'han reducido sus poblaciones debido a:',
                 'alternativas': ['El aumento de depredadores naturales',
                                  'Causas exclusivamente naturales',
                                  'Cambios genéticos espontáneos',
                                  'La migración voluntaria',
                                  'Actividades antrópicas como la pesca no '
                                  'planificada'],
                 'correcta': 'E'},
                {'pregunta': 'El Perú es considerado uno de los países '
                             'megadiversos del mundo, cuyo total suma:',
                 'alternativas': ['Ocho países',
                                  'Quince países',
                                  'Veinte países',
                                  'Doce países',
                                  'Cinco países'],
                 'correcta': 'D'},
                {'pregunta': 'Los países megadiversos del mundo poseen en '
                             'conjunto un porcentaje de la biodiversidad '
                             'mundial igual a:',
                 'alternativas': ['70%', '30%', '90%', '50%', '60%'],
                 'correcta': 'A'},
                {'pregunta': 'La megadiversidad del Perú se debe, entre '
                             'otros factores, a su ubicación entre el '
                             'Ecuador y el trópico, y a la presencia de la '
                             'Cordillera de:',
                 'alternativas': ['Los Urales',
                                  'Los Alpes',
                                  'Los Andes',
                                  'Las Rocosas',
                                  'El Himalaya'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú es centro mundial de origen de la '
                             'agricultura y la ganadería; uno de los centros '
                             'más antiguos de cultivos se halla en la cueva '
                             'de:',
                 'alternativas': ['Guitarrero',
                                  'Chivateros',
                                  'Paccaicasa',
                                  'Toquepala',
                                  'Lauricocha'],
                 'correcta': 'A'},
                {'pregunta': 'El Perú posee al menos un número de especies '
                             'de plantas domesticadas igual a:',
                 'alternativas': ['250', '100', '50', '182', '300'],
                 'correcta': 'D'},
                {'pregunta': 'El Perú es el primer país del mundo en '
                             'variedades de papa, con aproximadamente:',
                 'alternativas': ['3000 variedades',
                                  '5000 variedades',
                                  '500 variedades',
                                  '10000 variedades',
                                  '1000 variedades'],
                 'correcta': 'A'},
                {'pregunta': 'El Perú es primer país en variedades de maíz, '
                             'con un número de ecotipos igual a:',
                 'alternativas': ['60', '50', '36', '15', '20'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú posee al menos un número de especies '
                             'de plantas igual a:',
                 'alternativas': ['50 000',
                                  '20 533',
                                  '10 000',
                                  '5 000',
                                  '15 000'],
                 'correcta': 'B'},
                {'pregunta': 'Del total de especies de plantas del Perú, el '
                             'porcentaje que es endémico es aproximadamente:',
                 'alternativas': ['70%', '90%', '30%', '10%', '50%'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú es el primer país del mundo en número '
                             'de especies de:',
                 'alternativas': ['Cactus',
                                  'Bromelias',
                                  'Helechos',
                                  'Orquídeas',
                                  'Musgos'],
                 'correcta': 'D'},
                {'pregunta': 'La planta con el fruto más grande de la '
                             'Tierra, que puede pesar más de 70 kg y se '
                             'encuentra en el Perú, se llama:',
                 'alternativas': ['Sandía gigante',
                                  'Calabaza andina',
                                  'Tomate silvestre',
                                  'Zapallo macre',
                                  'Zapallo común'],
                 'correcta': 'D'},
                {'pregunta': 'El Perú es el primer país del mundo en número '
                             'de especies de peces y de:',
                 'alternativas': ['Reptiles',
                                  'Mariposas',
                                  'Anfibios',
                                  'Mamíferos',
                                  'Aves'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú es el segundo país del mundo en '
                             'variedad de aves, con un número aproximado de '
                             'especies igual a:',
                 'alternativas': ['1857', '3000', '2500', '1000', '500'],
                 'correcta': 'A'},
                {'pregunta': 'El Perú es el segundo país del mundo en '
                             'variedad de primates, con un número de '
                             'especies igual a:',
                 'alternativas': ['34', '10', '15', '20', '50'],
                 'correcta': 'A'},
                {'pregunta': 'El primate endémico del Perú, uno de los 34 '
                             'especies de primates del país, es el:',
                 'alternativas': ['Mono aullador',
                                  'Tití pigmeo',
                                  'Mono choro de cola amarilla',
                                  'Mono capuchino',
                                  'Mono araña'],
                 'correcta': 'C'},
                {'pregunta': 'El mar peruano es conocido como «una sopa de '
                             'plancton» debido a su gran cantidad de:',
                 'alternativas': ['Nutrientes',
                                  'Corrientes',
                                  'Sal',
                                  'Minerales exclusivos',
                                  'Oxígeno exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'La alpaca es la forma doméstica de:',
                 'alternativas': ['El guanaco',
                                  'La llama silvestre',
                                  'La vicuña',
                                  'El taruca',
                                  'La oveja andina'],
                 'correcta': 'C'},
                {'pregunta': 'La llama es la forma doméstica de:',
                 'alternativas': ['El guanaco',
                                  'La vicuña',
                                  'La taruca',
                                  'El venado',
                                  'La alpaca silvestre'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'EL CONVENIO SOBRE LA DIVERSIDAD BIOLÓGICA / '
                                'COMPONENTES DE LA BIODIVERSIDAD',
                      'items': ['El Convenio sobre la Diversidad Biológica '
                                '(CDB) se celebró en la «Cumbre de la '
                                'Tierra», en Río de Janeiro, en 1992.',
                                'La biodiversidad comprende tres '
                                'componentes: diversidad genética, '
                                'diversidad de especies y diversidad de '
                                'ecosistemas.']},
                     {'titulo': 'BENEFICIOS DE LA DIVERSIDAD BIOLÓGICA / '
                                'PELIGROS PARA LA DIVERSIDAD BIOLÓGI',
                      'items': ['Los servicios de aprovisionamiento '
                                'suministran bienes con valor monetario '
                                'directo: alimentos, agua, madera.',
                                'La causa principal de extinción de especies '
                                'es la destrucción del hábitat por expansión '
                                'de poblaciones humanas.']},
                     {'titulo': 'EL PERÚ COMO PAÍS MEGADIVERSO / RECURSOS '
                                'GENÉTICOS DEL PERÚ',
                      'items': ['El Perú es uno de los cinco países con '
                                'mayor diversidad biológica del mundo, y uno '
                                'de los doce países megadiversos.',
                                'El Perú posee al menos 182 especies de '
                                'plantas domesticadas, como la papa, el '
                                'tomate, el camote y el maíz.']},
                     {'titulo': 'DIVERSIDAD DE FLORA EN EL PERÚ / DIVERSIDAD '
                                'DE FAUNA EN EL PERÚ',
                      'items': ['El Perú posee al menos 20 533 especies de '
                                'plantas, de las cuales un 30% son '
                                'endémicas.',
                                'El Perú es primero en el mundo en número de '
                                'especies de peces (1200) y de mariposas.']},
                     {'titulo': 'DETERIORO DE LA FLORA Y FAUNA / TIPOS DE '
                                'DETERIORO',
                      'items': ['La flora y fauna son recursos naturales '
                                'renovables, que se regeneran por '
                                'reproducción o propagación.',
                                'El uso excesivo de biomasa es la '
                                'utilización insostenible de materia '
                                'orgánica de plantas y animales.']}]},
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
                {'titulo': '16.5 INCREMENTO DEL EFECTO INVERNADERO',
                 'items': ['El {efecto invernadero} es un fenómeno natural '
                           'que permite la vida en la Tierra, por la '
                           'absorción de radiación solar por los {gases} de '
                           'efecto invernadero.',
                           'Los principales gases de efecto invernadero '
                           'naturales son el vapor de agua, el dióxido de '
                           'carbono y el {metano}.',
                           'Sin estos gases, la temperatura de la superficie '
                           'terrestre sería de {-18}°C a -20°C.',
                           'El aumento del dióxido de carbono se debe '
                           'principalmente al uso de {combustibles fósiles} '
                           'y la deforestación.',
                           'El incremento de metano y óxido nitroso se debe '
                           'principalmente a la {agricultura} y ganadería.',
                           'Entre las consecuencias del incremento del '
                           'efecto invernadero están la fusión de los '
                           'casquetes {polares} y el aumento del nivel del '
                           'mar.']},
                {'titulo': '16.6 CALENTAMIENTO GLOBAL Y CAMBIO CLIMÁTICO',
                 'items': ['El {calentamiento global} es el aumento de la '
                           'temperatura media global de la atmósfera y los '
                           'océanos; su principal causa es el {efecto '
                           'invernadero}.',
                           'El {cambio climático} es un cambio del clima '
                           'atribuido directa o indirectamente a la '
                           'actividad {humana}.',
                           'El {albedo} es la cantidad total de radiación '
                           'solar que llega a la Tierra y es reflejada.',
                           'El albedo es {alto} en superficies cubiertas de '
                           'nieve, y {bajo} en superficies con vegetación y '
                           'océanos.',
                           'Entre las causas del cambio climático está la '
                           'alteración del {ciclo hidrológico}, generando '
                           'sequías e inundaciones.',
                           'La zona {andina} del Perú se considera una de '
                           'las zonas con mayor vulnerabilidad al cambio '
                           'climático.']},
                {'titulo': '16.7 DISMINUCIÓN DE LA CAPA DE OZONO',
                 'items': ['El {ozono} se encuentra en una franja entre los '
                           '20 y 40 km de altura, en la {estratosfera}.',
                           'La capa de ozono absorbe los rayos '
                           '{ultravioleta} nocivos del sol, protegiendo al '
                           'fitoplancton y a los organismos marinos.',
                           'En el hombre, el daño a la capa de ozono causa '
                           'debilitamiento inmunológico, cataratas y cáncer '
                           'de {piel}.',
                           'En {1974}, los científicos Rowland y Molina '
                           'descubrieron que los {CFC} (clorofluorocarbonos) '
                           'destruyen la capa de ozono.',
                           'Los CFC se usan comúnmente en aerosoles, '
                           'frigoríficos y aparatos de {acondicionamiento} '
                           'de aire.',
                           'El cloro liberado por los CFC puede descomponer '
                           'hasta {100 000} moléculas de ozono durante su '
                           'permanencia en la estratosfera.']},
                {'titulo': '16.8 CONSERVACIÓN DEL MEDIO AMBIENTE',
                 'items': ['Según la {UICN} (1980), la conservación es la '
                           'gestión de la biosfera para el mayor beneficio '
                           'sostenido de las generaciones {presentes} y '
                           'futuras.',
                           'Los tres objetivos de la conservación son: '
                           'mantener procesos ecológicos, preservar la '
                           'diversidad {genética}, y asegurar el '
                           'aprovechamiento {sostenido}.',
                           'El {proteccionismo} sostiene que los recursos '
                           'deben mantenerse sin tocar, «bajo llave».',
                           'El {conservacionismo} se basa en el desarrollo '
                           'sostenible: uso racional y equilibrado de los '
                           'recursos.',
                           'La conservación {ex situ} protege componentes de '
                           'la biodiversidad fuera de su hábitat natural.',
                           'La conservación {in situ} mantiene poblaciones '
                           'viables de especies en sus entornos naturales, '
                           'como en las áreas naturales protegidas.']},
                {'titulo': '16.9 FORESTACIÓN Y REFORESTACIÓN',
                 'items': ['La {forestación} es poblar con árboles áreas que '
                           'nunca o hace mucho tiempo tuvieron bosque.',
                           'La {reforestación} es repoblar con especies '
                           'arbóreas suelos que sí tuvieron cobertura '
                           'forestal antes.',
                           'En la cuenca de {Patacancha}, Ollantaytambo, se '
                           'ha forestado con Polylepis sp. o {queuña}.',
                           'En la cuenca de {Tambomachay}, Cusco, se ha '
                           'reforestado también con {queuña}.']},
                {'titulo': '16.10 ÁREAS NATURALES PROTEGIDAS DEL PERÚ (ANP)',
                 'items': ['Las ANP están reguladas por la Ley N° {29834}, '
                           'para conservar la diversidad biológica y valores '
                           'culturales asociados.',
                           'El artículo {68} de la Constitución obliga al '
                           'Estado a promover la conservación de la '
                           'diversidad biológica y las ANP.',
                           'El {SERNANP} es el Servicio Nacional de Áreas '
                           'Naturales Protegidas por el Estado, ente rector '
                           'del sistema.',
                           'El {SINANPE} es el Sistema Nacional de Áreas '
                           'Naturales Protegidas, conformado por las áreas '
                           'de administración {nacional}.',
                           'Las ANP con estatus definitivo se clasifican en '
                           '{nueve} categorías: 3 de uso indirecto y {6} de '
                           'uso directo.',
                           'Las áreas de uso {indirecto} permiten '
                           'investigación y turismo, pero no la extracción '
                           'de recursos; incluyen Parques y Santuarios '
                           '{Nacionales}.',
                           'Las áreas de uso {directo} sí permiten el '
                           'aprovechamiento de recursos naturales.']}],
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
                                  'Ciclo biogeoquímico normal',
                                  'Ninguna alteración',
                                  'Aumento de biodiversidad'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación se define como la adición de '
                             'sustancias al ambiente en cantidades que:',
                 'alternativas': ['No afectan a ningún organismo',
                                  'Se mantienen bajo los niveles normales',
                                  'Mejoran el ecosistema',
                                  'Sobrepasan los niveles regulares de la '
                                  'naturaleza',
                                  'Son siempre imperceptibles'],
                 'correcta': 'D'},
                {'pregunta': 'A mayor población e índice de uso de recursos '
                             'naturales en un área, generalmente se '
                             'presentan:',
                 'alternativas': ['Menor consumo energético',
                                  'Mayor biodiversidad automática',
                                  'Más problemas de contaminación',
                                  'Ningún cambio ambiental',
                                  'Menos problemas ambientales'],
                 'correcta': 'C'},
                {'pregunta': 'La contaminación causada por fuentes como '
                             'volcanes o efectos geoclimáticos se llama '
                             'contaminación:',
                 'alternativas': ['Química exclusiva',
                                  'Física exclusiva',
                                  'Natural',
                                  'Biológica exclusiva',
                                  'Antrópica'],
                 'correcta': 'C'},
                {'pregunta': 'La contaminación producida o distribuida por '
                             'el ser humano se llama contaminación:',
                 'alternativas': ['Natural',
                                  'Geológica',
                                  'Antrópica',
                                  'Volcánica',
                                  'Cósmica'],
                 'correcta': 'C'},
                {'pregunta': 'Una de las principales fuentes de '
                             'contaminación antropogénica es:',
                 'alternativas': ['Los volcanes',
                                  'La agricultura industrializada',
                                  'Las mareas',
                                  'La radiación solar natural',
                                  'Los terremotos'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes causados por microorganismos '
                             'como bacterias y virus se llaman '
                             'contaminantes:',
                 'alternativas': ['Sonoros exclusivos',
                                  'Biológicos',
                                  'Térmicos exclusivos',
                                  'Químicos',
                                  'Físicos'],
                 'correcta': 'B'},
                {'pregunta': 'El vibrión colérico, presente en aguas de ríos '
                             'latinoamericanos, es un ejemplo de '
                             'contaminante:',
                 'alternativas': ['Biológico',
                                  'Térmico',
                                  'Físico',
                                  'Sonoro',
                                  'Químico'],
                 'correcta': 'A'},
                {'pregunta': 'Los contaminantes relacionados con la energía, '
                             'como el ruido o las altas temperaturas, se '
                             'llaman contaminantes:',
                 'alternativas': ['Biológicos',
                                  'Químicos',
                                  'Naturales exclusivos',
                                  'Orgánicos exclusivos',
                                  'Físicos'],
                 'correcta': 'E'},
                {'pregunta': 'Los contaminantes físicos pueden influir en el '
                             'desarrollo de enfermedades humanas de tipo:',
                 'alternativas': ['Psico-neurológicas',
                                  'Solo digestivas',
                                  'Solo cardiovasculares exclusivas',
                                  'Solo dermatológicas',
                                  'Solo óseas'],
                 'correcta': 'A'},
                {'pregunta': 'Los contaminantes provocados por sustancias '
                             'orgánicas o inorgánicas se llaman '
                             'contaminantes:',
                 'alternativas': ['Radiactivos exclusivos',
                                  'Biológicos',
                                  'Sonoros',
                                  'Químicos',
                                  'Físicos'],
                 'correcta': 'D'},
                {'pregunta': 'El impacto más notorio de la contaminación '
                             'química se dio durante:',
                 'alternativas': ['La Revolución Francesa',
                                  'La Edad Media',
                                  'La Primera Guerra Mundial exclusivamente',
                                  'El auge industrial de la Segunda Guerra '
                                  'Mundial',
                                  'La colonización americana'],
                 'correcta': 'D'},
                {'pregunta': 'La contaminación química actualmente es la '
                             'principal causante de:',
                 'alternativas': ['El calentamiento global',
                                  'La biodiversidad',
                                  'La reproducción celular',
                                  'La fotosíntesis',
                                  'La mitosis'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los gases que provocan el calentamiento '
                             'global se mencionan los:',
                 'alternativas': ['CFC (clorofluorocarbonos)',
                                  'Oxígeno puro',
                                  'Gases inertes',
                                  'Gases nobles',
                                  'Vapor de agua exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El agua cubre de la superficie del planeta '
                             'aproximadamente:',
                 'alternativas': ['20%', '90%', '30%', '50%', '71%'],
                 'correcta': 'E'},
                {'pregunta': 'Aunque el agua cubre gran parte del planeta, '
                             'está disponible en cantidades:',
                 'alternativas': ['Iguales en todo el mundo',
                                  'Limitadas y distribuidas de forma no '
                                  'uniforme',
                                  'Excesivas en todas las regiones',
                                  'Ilimitadas',
                                  'Infinitas'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las sustancias químicas que contaminan '
                             'el agua figuran el petróleo y los:',
                 'alternativas': ['Oxígenos disueltos',
                                  'Minerales esenciales',
                                  'Gases nobles',
                                  'Detergentes sintéticos',
                                  'Nutrientes naturales'],
                 'correcta': 'D'},
                {'pregunta': 'Los contaminantes físicos del agua alteran '
                             'principalmente su:',
                 'alternativas': ['Salinidad exclusiva',
                                  'Temperatura exclusivamente',
                                  'pH exclusivamente',
                                  'Composición química exclusiva',
                                  'Transparencia'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando se impide la entrada de luz al agua por '
                             'contaminación física, los productores del '
                             'ecosistema:',
                 'alternativas': ['Se multiplican más rápido',
                                  'Deben emigrar o morir',
                                  'Aumentan su fotosíntesis',
                                  'No se ven afectados',
                                  'Cambian de especie'],
                 'correcta': 'B'},
                {'pregunta': 'Durante los últimos 200 años, el hombre ha '
                             'agregado al ambiente grandes cantidades de:',
                 'alternativas': ['Solo materia orgánica natural',
                                  'Solo nitrógeno',
                                  'Productos químicos y agentes físicos',
                                  'Solo agua pura',
                                  'Solo oxígeno'],
                 'correcta': 'C'},
                {'pregunta': 'Según la UICN (1980), la conservación es la '
                             'gestión de la biosfera para beneficio de las '
                             'generaciones presentes y:',
                 'alternativas': ['Solo las próximas dos décadas',
                                  'Solo la actual',
                                  'Futuras',
                                  'Ninguna otra generación',
                                  'Pasadas exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los tres objetivos de la conservación '
                             'es preservar la diversidad:',
                 'alternativas': ['Económica',
                                  'Política',
                                  'Cultural exclusiva',
                                  'Genética',
                                  'Religiosa'],
                 'correcta': 'D'},
                {'pregunta': 'La corriente que sostiene que los recursos '
                             'naturales deben mantenerse sin tocar, «bajo '
                             'llave», se llama:',
                 'alternativas': ['Extractivismo',
                                  'Mito de la inagotabilidad',
                                  'Conservacionismo',
                                  'Desarrollismo',
                                  'Proteccionismo'],
                 'correcta': 'E'},
                {'pregunta': 'La corriente basada en el desarrollo '
                             'sostenible y el uso racional de los recursos '
                             'se llama:',
                 'alternativas': ['Explotacionismo',
                                  'Extractivismo',
                                  'Conservacionismo',
                                  'Mito de la inagotabilidad',
                                  'Proteccionismo'],
                 'correcta': 'C'},
                {'pregunta': 'La conservación de componentes de la '
                             'biodiversidad fuera de su hábitat natural se '
                             'llama conservación:',
                 'alternativas': ['Mixta',
                                  'Directa',
                                  'Indirecta',
                                  'Ex situ',
                                  'In situ'],
                 'correcta': 'D'},
                {'pregunta': 'La conservación de especies dentro de sus '
                             'entornos naturales, como en áreas protegidas, '
                             'se llama conservación:',
                 'alternativas': ['Externa',
                                  'Indirecta',
                                  'In situ',
                                  'Ex situ',
                                  'Artificial'],
                 'correcta': 'C'},
                {'pregunta': 'Poblar con árboles áreas que nunca tuvieron '
                             'bosque se llama:',
                 'alternativas': ['Forestación',
                                  'Silvicultura exclusiva',
                                  'Deforestación',
                                  'Agroforestería',
                                  'Reforestación'],
                 'correcta': 'A'},
                {'pregunta': 'Repoblar con árboles suelos que sí tuvieron '
                             'cobertura forestal antes se llama:',
                 'alternativas': ['Extracción forestal',
                                  'Reforestación',
                                  'Forestación',
                                  'Deforestación',
                                  'Tala selectiva'],
                 'correcta': 'B'},
                {'pregunta': 'En la cuenca de Patacancha, Ollantaytambo, se '
                             'ha forestado principalmente con:',
                 'alternativas': ['Eucalipto',
                                  'Pino',
                                  'Queuña (Polylepis sp.)',
                                  'Ciprés',
                                  'Molle'],
                 'correcta': 'C'},
                {'pregunta': 'Las Áreas Naturales Protegidas del Perú están '
                             'reguladas por la Ley N°:',
                 'alternativas': ['28611',
                                  '26300',
                                  '30220',
                                  '29834',
                                  '27444'],
                 'correcta': 'D'},
                {'pregunta': 'El artículo de la Constitución que obliga al '
                             'Estado a promover la conservación de las ANP '
                             'es el:',
                 'alternativas': ['Artículo 68',
                                  'Artículo 189',
                                  'Artículo 2',
                                  'Artículo 24',
                                  'Artículo 200'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo que asegura la conservación de '
                             'las Áreas Naturales Protegidas del Perú es:',
                 'alternativas': ['El SERNANP',
                                  'El MINAM exclusivamente',
                                  'El MINAGRI',
                                  'La SUNAT',
                                  'El INEI'],
                 'correcta': 'A'},
                {'pregunta': 'El Sistema Nacional de Áreas Naturales '
                             'Protegidas por el Estado se conoce por las '
                             'siglas:',
                 'alternativas': ['INRENA',
                                  'SINANPE',
                                  'MINAM',
                                  'SERNANP',
                                  'SUNARP'],
                 'correcta': 'B'},
                {'pregunta': 'Las Áreas Naturales Protegidas con estatus '
                             'definitivo se clasifican en un número de '
                             'categorías igual a:',
                 'alternativas': ['Tres', 'Nueve', 'Doce', 'Seis', 'Cinco'],
                 'correcta': 'B'},
                {'pregunta': 'De las nueve categorías de ANP, el número de '
                             'categorías de uso indirecto es:',
                 'alternativas': ['Cinco', 'Seis', 'Uno', 'Tres', 'Nueve'],
                 'correcta': 'D'},
                {'pregunta': 'Las áreas de uso indirecto permiten '
                             'investigación científica y turismo, pero no '
                             'permiten:',
                 'alternativas': ['La investigación académica',
                                  'La extracción de recursos naturales',
                                  'El acceso de científicos',
                                  'La visita de turistas',
                                  'La educación ambiental'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las áreas de uso indirecto se cuentan '
                             'los Parques Nacionales y los:',
                 'alternativas': ['Cotos de caza',
                                  'Santuarios Nacionales',
                                  'Bosques de protección',
                                  'Reservas comunales',
                                  'Refugios de vida silvestre'],
                 'correcta': 'B'},
                {'pregunta': 'Las áreas de uso directo, a diferencia de las '
                             'de uso indirecto, sí permiten:',
                 'alternativas': ['Solo investigación',
                                  'Ninguna actividad',
                                  'Solo turismo',
                                  'El aprovechamiento de recursos naturales',
                                  'Solo educación'],
                 'correcta': 'D'},
                {'pregunta': 'El efecto invernadero es un fenómeno natural '
                             'que permite la vida en la Tierra, mediante la '
                             'absorción de radiación solar por los:',
                 'alternativas': ['Gases de efecto invernadero',
                                  'Rayos infrarrojos exclusivos',
                                  'Rayos ultravioleta',
                                  'Vientos estratosféricos',
                                  'Aerosoles'],
                 'correcta': 'A'},
                {'pregunta': 'Los principales gases de efecto invernadero '
                             'naturales son el vapor de agua, el dióxido de '
                             'carbono y el:',
                 'alternativas': ['Hidrógeno',
                                  'Helio',
                                  'Oxígeno',
                                  'Metano',
                                  'Nitrógeno'],
                 'correcta': 'D'},
                {'pregunta': 'Sin los gases de efecto invernadero, la '
                             'temperatura de la superficie terrestre sería '
                             'de aproximadamente:',
                 'alternativas': ['0°C a 10°C',
                                  '-50°C a -60°C',
                                  '30°C a 40°C',
                                  '10°C a 20°C',
                                  '-18°C a -20°C'],
                 'correcta': 'E'},
                {'pregunta': 'El aumento del dióxido de carbono atmosférico '
                             'se debe principalmente al uso de combustibles '
                             'fósiles y a la:',
                 'alternativas': ['Ganadería exclusiva',
                                  'Agricultura exclusiva',
                                  'Deforestación',
                                  'Minería exclusiva',
                                  'Pesca'],
                 'correcta': 'C'},
                {'pregunta': 'El incremento de metano y óxido nitroso en la '
                             'atmósfera se debe principalmente a la '
                             'agricultura y la:',
                 'alternativas': ['Construcción',
                                  'Pesca',
                                  'Ganadería',
                                  'Industria textil',
                                  'Minería'],
                 'correcta': 'C'},
                {'pregunta': 'El calentamiento global es el aumento de la '
                             'temperatura media global de la atmósfera y los '
                             'océanos, cuya principal causa es:',
                 'alternativas': ['La actividad volcánica',
                                  'La disminución del ozono',
                                  'El efecto invernadero',
                                  'La rotación terrestre',
                                  'Las corrientes marinas'],
                 'correcta': 'C'},
                {'pregunta': 'El cambio climático es un cambio del clima '
                             'atribuido directa o indirectamente a la '
                             'actividad:',
                 'alternativas': ['Volcánica',
                                  'Sísmica',
                                  'Humana',
                                  'Cósmica',
                                  'Solar exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La cantidad total de radiación solar que llega '
                             'a la Tierra y es reflejada se llama:',
                 'alternativas': ['Insolación',
                                  'Albedo',
                                  'Efecto invernadero',
                                  'Fotosíntesis',
                                  'Irradiancia'],
                 'correcta': 'B'},
                {'pregunta': 'El albedo es alto en superficies cubiertas de '
                             'nieve, y bajo en superficies cubiertas de:',
                 'alternativas': ['Nubes',
                                  'Roca desnuda',
                                  'Vegetación y océanos',
                                  'Arena',
                                  'Hielo'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las causas del cambio climático está la '
                             'alteración del ciclo hidrológico, generando '
                             'sequías e:',
                 'alternativas': ['Terremotos',
                                  'Erupciones',
                                  'Inundaciones',
                                  'Tsunamis',
                                  'Huracanes exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'La zona del Perú considerada con mayor '
                             'vulnerabilidad al cambio climático es la zona:',
                 'alternativas': ['Andina',
                                  'Desértica',
                                  'Amazónica exclusiva',
                                  'Insular',
                                  'Costera'],
                 'correcta': 'A'},
                {'pregunta': 'El ozono se encuentra en una estrecha franja '
                             'de altura ubicada en la:',
                 'alternativas': ['Termosfera',
                                  'Troposfera',
                                  'Exosfera',
                                  'Estratosfera',
                                  'Mesosfera'],
                 'correcta': 'D'},
                {'pregunta': 'La capa de ozono absorbe los rayos nocivos del '
                             'sol de tipo:',
                 'alternativas': ['Microondas',
                                  'X',
                                  'Gamma',
                                  'Infrarrojos',
                                  'Ultravioleta'],
                 'correcta': 'E'},
                {'pregunta': 'El daño a la capa de ozono, en el hombre, '
                             'puede causar cataratas, debilitamiento '
                             'inmunológico y cáncer de:',
                 'alternativas': ['Riñón',
                                  'Pulmón',
                                  'Piel',
                                  'Estómago',
                                  'Hígado'],
                 'correcta': 'C'},
                {'pregunta': 'En 1974, los científicos que descubrieron que '
                             'los CFC destruyen la capa de ozono fueron:',
                 'alternativas': ['Rowland y Molina',
                                  'Oparin y Haldane',
                                  'Miller y Urey',
                                  'Watson y Crick',
                                  'Darwin y Wallace'],
                 'correcta': 'A'},
                {'pregunta': 'Los CFC (clorofluorocarbonos), responsables de '
                             'la destrucción del ozono, se usan comúnmente '
                             'en aerosoles y en:',
                 'alternativas': ['Frigoríficos y aire acondicionado',
                                  'Fertilizantes',
                                  'Pinturas exclusivas',
                                  'Combustibles exclusivos',
                                  'Plásticos exclusivos'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE CONTAMINACIÓN / FUENTES DE '
                                'CONTAMINACIÓN',
                      'items': ['La contaminación surge cuando, por '
                                'presencia cuantitativa o cualitativa de '
                                'materia o energía, se produce un '
                                'desequilibrio ambiental.',
                                'La contaminación natural es causada por '
                                'fuentes como volcanes o efectos '
                                'geoclimáticos.']},
                     {'titulo': 'TIPOS DE CONTAMINANTES / CONTAMINACIÓN DEL '
                                'AGUA',
                      'items': ['Los contaminantes biológicos son '
                                'microorganismos como bacterias, hongos y '
                                'virus; ejemplo, el vibrión colérico.',
                                'El agua cubre alrededor del 71% de la '
                                'superficie del planeta, pero está '
                                'disponible en cantidades limitadas.']},
                     {'titulo': 'INCREMENTO DEL EFECTO INVERNADERO / '
                                'CALENTAMIENTO GLOBAL Y CAMBIO CLIMÁTICO',
                      'items': ['El efecto invernadero es un fenómeno '
                                'natural que permite la vida en la Tierra, '
                                'por la absorción de radiación solar por los '
                                'gases de efecto invernadero.',
                                'El calentamiento global es el aumento de la '
                                'temperatura media global de la atmósfera y '
                                'los océanos; su principal causa es el '
                                'efecto invernadero.']},
                     {'titulo': 'DISMINUCIÓN DE LA CAPA DE OZONO / '
                                'CONSERVACIÓN DEL MEDIO AMBIENTE',
                      'items': ['El ozono se encuentra en una franja entre '
                                'los 20 y 40 km de altura, en la '
                                'estratosfera.',
                                'Según la UICN (1980), la conservación es la '
                                'gestión de la biosfera para el mayor '
                                'beneficio sostenido de las generaciones '
                                'presentes y futuras.']},
                     {'titulo': 'FORESTACIÓN Y REFORESTACIÓN / ÁREAS '
                                'NATURALES PROTEGIDAS DEL PERÚ (ANP)',
                      'items': ['La forestación es poblar con árboles áreas '
                                'que nunca o hace mucho tiempo tuvieron '
                                'bosque.',
                                'Las ANP están reguladas por la Ley N° '
                                '29834, para conservar la diversidad '
                                'biológica y valores culturales '
                                'asociados.']}]}]
