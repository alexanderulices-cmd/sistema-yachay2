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
                 'alternativas': ['Zoon', 'Logos', 'Genos', 'Soma', 'Physis'],
                 'correcta': 'B'},
                {'pregunta': 'La raíz griega «bios» significa:',
                 'alternativas': ['Estudio',
                                  'Materia',
                                  'Célula',
                                  'Origen',
                                  'Vida'],
                 'correcta': 'E'},
                {'pregunta': 'La biología es la ciencia que estudia:',
                 'alternativas': ['Solo el universo',
                                  'Solo las estrellas',
                                  'Solo los minerales',
                                  'Solo la materia inerte',
                                  'Los seres vivos'],
                 'correcta': 'E'},
                {'pregunta': 'El estudio de la biología comprende el origen, '
                             'evolución, clasificación, estructura, función '
                             'y:',
                 'alternativas': ['Comercio',
                                  'Herencia',
                                  'Política',
                                  'Religión',
                                  'Economía'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la unión de la física y '
                             'la biología se llama:',
                 'alternativas': ['Bioquímica',
                                  'Bioestadística',
                                  'Biofísica',
                                  'Astrobiología',
                                  'Geología'],
                 'correcta': 'C'},
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
                 'alternativas': ['Astrofísica',
                                  'Bioquímica',
                                  'Geología',
                                  'Biofísica',
                                  'Bioestadística'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que surge de la relación entre '
                             'biología y matemáticas se llama:',
                 'alternativas': ['Bioética',
                                  'Biogeografía',
                                  'Biofísica',
                                  'Bioestadística',
                                  'Bioquímica'],
                 'correcta': 'D'},
                {'pregunta': 'El nivel formado por protón, neutrón y '
                             'electrón se llama nivel:',
                 'alternativas': ['Subatómico',
                                  'Molecular',
                                  'Atómico',
                                  'Macromolecular',
                                  'Celular'],
                 'correcta': 'A'},
                {'pregunta': 'El átomo se define como la unidad más pequeña '
                             'de:',
                 'alternativas': ['Un organismo',
                                  'Una célula',
                                  'Un elemento químico',
                                  'Un ecosistema',
                                  'Una molécula orgánica'],
                 'correcta': 'C'},
                {'pregunta': 'Las moléculas con un peso de miles de daltons, '
                             'formadas por unidades monoméricas, se llaman:',
                 'alternativas': ['Átomos',
                                  'Partículas subatómicas',
                                  'Organelos',
                                  'Ecosistemas',
                                  'Macromoléculas'],
                 'correcta': 'E'},
                {'pregunta': 'El almidón es un polímero de glucosa, mientras '
                             'que las proteínas son polímeros de:',
                 'alternativas': ['Aminoácidos',
                                  'Iones',
                                  'Glúcidos',
                                  'Nucleótidos',
                                  'Lípidos'],
                 'correcta': 'A'},
                {'pregunta': 'El nivel de complejos supramoleculares también '
                             'se conoce como nivel:',
                 'alternativas': ['Orgánico',
                                  'Celular',
                                  'Prebiótico',
                                  'Atómico',
                                  'Ecológico'],
                 'correcta': 'C'},
                {'pregunta': 'Los virus, ribosomas y glucoproteínas son '
                             'ejemplos del nivel:',
                 'alternativas': ['Celular',
                                  'Atómico',
                                  'Supramolecular',
                                  'Ecológico',
                                  'Orgánico'],
                 'correcta': 'C'},
                {'pregunta': 'Los orgánulos celulares, como las '
                             'mitocondrias, no se consideran seres vivos '
                             'porque:',
                 'alternativas': ['No tienen forma definida',
                                  'No cumplen las funciones de nutrición, '
                                  'relación y reproducción',
                                  'No están formados por moléculas',
                                  'Son demasiado pequeños',
                                  'No contienen materia orgánica'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad mínima de la materia viva es:',
                 'alternativas': ['La molécula',
                                  'El tejido',
                                  'El átomo',
                                  'El órgano',
                                  'La célula'],
                 'correcta': 'E'},
                {'pregunta': 'Los organismos formados por muchas células se '
                             'denominan:',
                 'alternativas': ['Virales',
                                  'Acelulares',
                                  'Procariontes exclusivamente',
                                  'Pluricelulares',
                                  'Unicelulares'],
                 'correcta': 'D'},
                {'pregunta': 'A partir de la especie, comienzan los niveles '
                             'de organización:',
                 'alternativas': ['Moleculares',
                                  'Celulares exclusivamente',
                                  'Ecológicos',
                                  'Subatómicos',
                                  'Químicos'],
                 'correcta': 'C'},
                {'pregunta': 'Los niveles de organización ecológica incluyen '
                             'población, comunidad, ecosistema, bioma y:',
                 'alternativas': ['Molécula',
                                  'Órgano',
                                  'Biosfera',
                                  'Célula',
                                  'Tejido'],
                 'correcta': 'C'},
                {'pregunta': 'Los niveles de organización permiten, entre '
                             'otras cosas:',
                 'alternativas': ['Establecer límites y ordenar conceptos',
                                  'Confundir la clasificación',
                                  'Eliminar el estudio sistemático',
                                  'Evitar el análisis científico',
                                  'Ignorar la complejidad biológica'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la biología que estudia los '
                             'órganos, aparatos y sistemas se llama:',
                 'alternativas': ['Fisiología',
                                  'Anatomía',
                                  'Histología',
                                  'Embriología',
                                  'Citología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que estudia la formación y desarrollo '
                             'de los embriones se llama:',
                 'alternativas': ['Fisiología',
                                  'Embriología',
                                  'Anatomía',
                                  'Genética',
                                  'Histología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la biología que estudia a los '
                             'hongos se llama:',
                 'alternativas': ['Ficología',
                                  'Micología',
                                  'Bacteriología',
                                  'Protozoología',
                                  'Botánica'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que estudia a las algas se llama:',
                 'alternativas': ['Micología',
                                  'Ficología',
                                  'Bacteriología',
                                  'Botánica',
                                  'Zoología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la biología que clasifica a los '
                             'seres vivos se llama:',
                 'alternativas': ['Histología',
                                  'Taxonomía',
                                  'Paleontología',
                                  'Ecología',
                                  'Etología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que estudia los tejidos de los seres '
                             'vivos se llama:',
                 'alternativas': ['Taxonomía',
                                  'Histología',
                                  'Anatomía',
                                  'Fisiología',
                                  'Citología'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la biología que estudia los fósiles '
                             'se llama:',
                 'alternativas': ['Ecología',
                                  'Paleontología',
                                  'Etología',
                                  'Genética',
                                  'Evolución'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que estudia organismos y productos '
                             'transgénicos se llama:',
                 'alternativas': ['Genética',
                                  'Ingeniería genética',
                                  'Bioquímica',
                                  'Bioestadística',
                                  'Biofísica'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la biología que estudia el carácter '
                             'y comportamiento de los seres vivos se llama:',
                 'alternativas': ['Ecología',
                                  'Etología',
                                  'Fisiología',
                                  'Patología',
                                  'Taxonomía'],
                 'correcta': 'B'},
                {'pregunta': 'La rama que estudia las enfermedades se llama:',
                 'alternativas': ['Etología',
                                  'Patología',
                                  'Ecología',
                                  'Genética',
                                  'Fisiología'],
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
                           'tolerancia a la {glucosa}.']}],
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
                 'alternativas': ['118', '92', '20', '40', '11'],
                 'correcta': 'A'},
                {'pregunta': 'De los elementos químicos existentes, los que '
                             'son naturales suman:',
                 'alternativas': ['118', '40', '20', '6', '92'],
                 'correcta': 'E'},
                {'pregunta': 'Los seres vivos están constituidos por un '
                             'número de elementos igual a:',
                 'alternativas': ['20', '6', '118', '40', '92'],
                 'correcta': 'E'},
                {'pregunta': 'Los bioelementos se clasifican en '
                             'macroelementos y:',
                 'alternativas': ['Solo minerales',
                                  'Bioelementos primarios exclusivamente',
                                  'Microelementos u oligoelementos',
                                  'Solo inorgánicos',
                                  'Solo orgánicos'],
                 'correcta': 'C'},
                {'pregunta': 'Los macroelementos representan de la materia '
                             'viva aproximadamente:',
                 'alternativas': ['10%', '75%', '25%', '99,6%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'Los bioelementos primarios, también llamados '
                             'organógenos, suman un total de:',
                 'alternativas': ['Once',
                                  'Seis',
                                  'Cinco',
                                  'Cuatro',
                                  'Veinte'],
                 'correcta': 'B'},
                {'pregunta': 'Los cuatro bioelementos primarios más '
                             'abundantes representan de la materia viva:',
                 'alternativas': ['20%', '96%', '10%', '75%', '50%'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento considerado la piedra angular en '
                             'la construcción de moléculas biológicas es:',
                 'alternativas': ['El nitrógeno',
                                  'El carbono',
                                  'El oxígeno',
                                  'El fósforo',
                                  'El azufre'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento más abundante en la naturaleza, '
                             'que forma parte del agua, es:',
                 'alternativas': ['El hidrógeno',
                                  'El fósforo',
                                  'El oxígeno',
                                  'El carbono',
                                  'El nitrógeno'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento que forma las proteínas, '
                             'esenciales para el crecimiento, es:',
                 'alternativas': ['El carbono',
                                  'El oxígeno',
                                  'El fósforo',
                                  'El azufre',
                                  'El nitrógeno'],
                 'correcta': 'E'},
                {'pregunta': 'El elemento que desempeña un papel esencial en '
                             'la transferencia de energía, como en el ATP, '
                             'es:',
                 'alternativas': ['El hidrógeno',
                                  'El fósforo',
                                  'El nitrógeno',
                                  'El carbono',
                                  'El azufre'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que forma parte de aminoácidos '
                             'como la metionina y la cisteína es:',
                 'alternativas': ['El carbono',
                                  'El fósforo',
                                  'El oxígeno',
                                  'El nitrógeno',
                                  'El azufre'],
                 'correcta': 'E'},
                {'pregunta': 'Los bioelementos secundarios son cinco: sodio, '
                             'potasio, calcio, magnesio y:',
                 'alternativas': ['Nitrógeno',
                                  'Cloro',
                                  'Azufre',
                                  'Fósforo',
                                  'Carbono'],
                 'correcta': 'B'},
                {'pregunta': 'El principal ión positivo del líquido '
                             'intersticial, esencial para impulsos '
                             'nerviosos, es:',
                 'alternativas': ['El calcio',
                                  'El potasio',
                                  'El cloro',
                                  'El magnesio',
                                  'El sodio'],
                 'correcta': 'E'},
                {'pregunta': 'El principal catión del interior de las '
                             'células es:',
                 'alternativas': ['El magnesio',
                                  'El calcio',
                                  'El sodio',
                                  'El potasio',
                                  'El cloro'],
                 'correcta': 'D'},
                {'pregunta': 'El hidrógeno es considerado el elemento:',
                 'alternativas': ['Sin relación con la vida',
                                  'Exclusivo de las plantas',
                                  'Más liviano que existe en la naturaleza',
                                  'Más pesado de la naturaleza',
                                  'Menos abundante'],
                 'correcta': 'C'},
                {'pregunta': 'El fósforo forma parte de los fosfolípidos que '
                             'se encuentran en:',
                 'alternativas': ['Las paredes celulares vegetales '
                                  'exclusivamente',
                                  'Solo el citoplasma',
                                  'Solo los ribosomas',
                                  'Las membranas celulares',
                                  'Solo el núcleo celular'],
                 'correcta': 'D'},
                {'pregunta': 'El azufre se encuentra, entre otros lugares, '
                             'en la bilis, el cartílago y:',
                 'alternativas': ['Solo las uñas',
                                  'Las glándulas suprarrenales',
                                  'Los huesos exclusivamente',
                                  'Solo el cabello',
                                  'Solo los dientes'],
                 'correcta': 'B'},
                {'pregunta': 'El nitrógeno también forma parte de compuestos '
                             'como:',
                 'alternativas': ['Solo el agua',
                                  'Los fertilizantes',
                                  'Solo el dióxido de carbono',
                                  'Solo la glucosa',
                                  'Solo el oxígeno molecular'],
                 'correcta': 'B'},
                {'pregunta': 'Los bioelementos secundarios son necesarios '
                             'para las células en cantidades:',
                 'alternativas': ['Nulas',
                                  'Ilimitadas',
                                  'Idénticas a los primarios',
                                  'Mayores que los primarios',
                                  'Más pequeñas que los primarios'],
                 'correcta': 'E'},
                {'pregunta': 'Los microelementos, u oligoelementos, '
                             'representan de la materia viva '
                             'aproximadamente:',
                 'alternativas': ['4%', '0,4%', '40%', '10%', '1%'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los microelementos no variables se '
                             'encuentran hierro, manganeso, cobre, zinc, '
                             'yodo, flúor, cobalto, molibdeno y:',
                 'alternativas': ['Selenio',
                                  'Boro',
                                  'Cromo',
                                  'Aluminio',
                                  'Níquel'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los microelementos variables se '
                             'encuentran selenio, silicio, cromo, aluminio, '
                             'litio, níquel y:',
                 'alternativas': ['Hierro',
                                  'Bromo',
                                  'Zinc',
                                  'Yodo',
                                  'Cobalto'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento que forma el grupo prostético '
                             'hemo de la hemoglobina es:',
                 'alternativas': ['El zinc',
                                  'El hierro',
                                  'El cobre',
                                  'El yodo',
                                  'El manganeso'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento que se concentra en la '
                             'glándula tiroides es:',
                 'alternativas': ['El hierro',
                                  'El yodo',
                                  'El zinc',
                                  'El flúor',
                                  'El cobalto'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento que aumenta la resistencia '
                             'del esmalte dental e inhibe las caries es:',
                 'alternativas': ['El yodo',
                                  'El flúor',
                                  'El zinc',
                                  'El hierro',
                                  'El cobre'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento que es constituyente de '
                             'proteínas como la insulina es:',
                 'alternativas': ['El hierro',
                                  'El zinc',
                                  'El yodo',
                                  'El cobalto',
                                  'El flúor'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento asociado con la funcionalidad '
                             'de la vitamina B12 es:',
                 'alternativas': ['El hierro',
                                  'El cobalto',
                                  'El zinc',
                                  'El yodo',
                                  'El manganeso'],
                 'correcta': 'B'},
                {'pregunta': 'El microelemento con función preponderante en '
                             'el metabolismo de la insulina como factor de '
                             'tolerancia a la glucosa es:',
                 'alternativas': ['El hierro',
                                  'El cromo',
                                  'El zinc',
                                  'El yodo',
                                  'El cobalto'],
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
                {'titulo': '3.5 SALES MINERALES Y ELECTROLITOS',
                 'items': ['Las {sales minerales} son compuestos neutros '
                           'producidos por la reacción de un ácido y una '
                           '{base}.',
                           'En estado sólido, las sales forman estructuras '
                           'duras, como caparazones, huesos y {dientes}.',
                           'Cuando una sal se disuelve en agua, se disocia '
                           'en {iones}: cationes y aniones.',
                           'Los {aniones} son iones con carga negativa, como '
                           'el cloruro (Cl⁻) y los fosfatos.',
                           'Los {cationes} son iones con carga positiva, '
                           'como el sodio (Na⁺) y el calcio (Ca²⁺).',
                           'Las sales minerales más abundantes en el cuerpo '
                           'humano contienen {fósforo} y calcio.']},
                {'titulo': '3.6 FUNCIONES DE LOS PRINCIPALES ELECTROLITOS',
                 'items': ['El {sodio} (Na⁺) participa en la regulación '
                           'osmótica y la conducción {nerviosa}; su exceso '
                           'produce {hipertensión}.',
                           'El {potasio} (K⁺) participa en la conducción '
                           'nerviosa y la {contracción} muscular.',
                           'El {calcio} (Ca²⁺) participa en la estructura '
                           'ósea, la coagulación de la sangre y la '
                           'contracción {muscular}.',
                           'El {magnesio} (Mg²⁺) actúa como cofactor '
                           'enzimático y forma parte de la estructura de la '
                           '{clorofila}.',
                           'El {cloruro} (Cl⁻) mantiene la '
                           'electroneutralidad y el equilibrio hídrico '
                           'celular.',
                           'El {fosfato} (PO₄³⁻) es tampón intracelular y '
                           'forma parte de nucleótidos, ADN y {ARN}.']},
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
                 'alternativas': ['Carbono-carbono',
                                  'Azufre-carbono',
                                  'Hidrógeno-oxígeno',
                                  'Oxígeno-nitrógeno',
                                  'Nitrógeno-fósforo'],
                 'correcta': 'A'},
                {'pregunta': 'Los minerales que forman estructuras duras, '
                             'como huesos y dientes, se llaman:',
                 'alternativas': ['Gases disueltos',
                                  'Electrolitos exclusivos',
                                  'Iones libres',
                                  'Minerales sólidos',
                                  'Minerales en disolución'],
                 'correcta': 'D'},
                {'pregunta': 'Los minerales en disolución son electrolitos '
                             'que participan, entre otras funciones, en:',
                 'alternativas': ['La contracción muscular',
                                  'El transporte de oxígeno exclusivamente',
                                  'La respiración exclusivamente',
                                  'La síntesis de ADN exclusivamente',
                                  'La digestión de proteínas'],
                 'correcta': 'A'},
                {'pregunta': 'Los gases disueltos que usan los seres vivos '
                             'son principalmente oxígeno y:',
                 'alternativas': ['Ozono',
                                  'Dióxido de carbono',
                                  'Hidrógeno gaseoso',
                                  'Nitrógeno',
                                  'Metano'],
                 'correcta': 'B'},
                {'pregunta': 'La molécula de agua está formada por dos '
                             'átomos de hidrógeno y uno de:',
                 'alternativas': ['Azufre',
                                  'Fósforo',
                                  'Carbono',
                                  'Nitrógeno',
                                  'Oxígeno'],
                 'correcta': 'E'},
                {'pregunta': 'Los átomos de la molécula de agua se unen '
                             'mediante enlaces:',
                 'alternativas': ['De hidrógeno exclusivamente',
                                  'Van der Waals exclusivos',
                                  'Iónicos',
                                  'Covalentes',
                                  'Metálicos'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura de la molécula de agua se '
                             'describe como:',
                 'alternativas': ['Hexagonal',
                                  'Tetraédrica',
                                  'Esférica perfecta',
                                  'Lineal',
                                  'Cúbica'],
                 'correcta': 'B'},
                {'pregunta': 'El ángulo entre los dos átomos de hidrógeno en '
                             'la molécula de agua es de aproximadamente:',
                 'alternativas': ['60°', '104,5°', '120°', '90°', '180°'],
                 'correcta': 'B'},
                {'pregunta': 'La distribución desigual de carga dentro de un '
                             'enlace se denomina:',
                 'alternativas': ['Anión',
                                  'Isómero',
                                  'Catión',
                                  'Radical libre',
                                  'Dipolo'],
                 'correcta': 'E'},
                {'pregunta': 'En la molécula de agua, el oxígeno tiene una '
                             'carga parcial:',
                 'alternativas': ['Neutra',
                                  'Negativa',
                                  'Positiva',
                                  'Nula',
                                  'Variable al azar'],
                 'correcta': 'B'},
                {'pregunta': 'La atracción entre moléculas de agua debido a '
                             'su polaridad produce el llamado:',
                 'alternativas': ['Enlace iónico',
                                  'Enlace covalente puro',
                                  'Enlace metálico',
                                  'Enlace peptídico',
                                  'Puente de hidrógeno'],
                 'correcta': 'E'},
                {'pregunta': 'Una sola molécula de agua puede formar puentes '
                             'de hidrógeno con hasta otras:',
                 'alternativas': ['Cuatro moléculas',
                                  'Una sola molécula',
                                  'Ocho moléculas',
                                  'Dos moléculas',
                                  'Diez moléculas'],
                 'correcta': 'A'},
                {'pregunta': 'El agua en estado libre representa del agua '
                             'celular total aproximadamente:',
                 'alternativas': ['25%', '5%', '75%', '95%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'El agua en estado libre desempeña un papel '
                             'como:',
                 'alternativas': ['Solvente estable e ionizante',
                                  'Fuente de energía exclusiva',
                                  'Material genético',
                                  'Pigmento celular',
                                  'Estructura rígida'],
                 'correcta': 'A'},
                {'pregunta': 'El agua ligada representa del agua celular '
                             'total aproximadamente:',
                 'alternativas': ['75%', '50%', '5%', '95%', '25%'],
                 'correcta': 'C'},
                {'pregunta': 'El agua ligada comprende el agua de imbibición '
                             'y el agua de:',
                 'alternativas': ['Excreción',
                                  'Transporte exclusivo',
                                  'Reserva',
                                  'Filtración',
                                  'Constitución'],
                 'correcta': 'E'},
                {'pregunta': 'La capacidad del agua de disolver gran '
                             'cantidad de moléculas se llama:',
                 'alternativas': ['Poder solvente',
                                  'Poder oxidante',
                                  'Poder reductor',
                                  'Poder tensioactivo',
                                  'Poder calorífico'],
                 'correcta': 'A'},
                {'pregunta': 'La polaridad de la molécula de agua favorece '
                             'la disociación de moléculas formadoras de:',
                 'alternativas': ['Anillos aromáticos',
                                  'Enlaces peptídicos',
                                  'Enlaces covalentes puros',
                                  'Iones',
                                  'Cadenas de carbono'],
                 'correcta': 'D'},
                {'pregunta': 'El agua de imbibición está ligada fuertemente '
                             'a la superficie de:',
                 'alternativas': ['El ADN exclusivamente',
                                  'Las proteínas',
                                  'Los lípidos exclusivamente',
                                  'Los carbohidratos',
                                  'Los minerales sólidos'],
                 'correcta': 'B'},
                {'pregunta': 'Para liberar el agua ligada de las proteínas '
                             'se requiere:',
                 'alternativas': ['Grandes cantidades de energía',
                                  'Solo un cambio de temperatura leve',
                                  'Solo luz solar',
                                  'Solo presión atmosférica normal',
                                  'Ninguna energía'],
                 'correcta': 'A'},
                {'pregunta': 'Las sales minerales son compuestos neutros '
                             'producidos por la reacción de un ácido y:',
                 'alternativas': ['Agua pura',
                                  'Un electrolito neutro',
                                  'Un catión',
                                  'Un anión exclusivo',
                                  'Una base'],
                 'correcta': 'E'},
                {'pregunta': 'En estado sólido, las sales minerales forman, '
                             'por ejemplo:',
                 'alternativas': ['Solo líquidos corporales',
                                  'Solo enzimas',
                                  'Huesos y dientes',
                                  'Solo gases disueltos',
                                  'Solo membranas celulares'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando una sal se disuelve en agua, se disocia '
                             'en:',
                 'alternativas': ['Solo protones',
                                  'Moléculas neutras',
                                  'Iones (cationes y aniones)',
                                  'Compuestos orgánicos',
                                  'Solo electrones libres'],
                 'correcta': 'C'},
                {'pregunta': 'Los iones con carga negativa se llaman:',
                 'alternativas': ['Isótopos',
                                  'Cationes',
                                  'Radicales libres',
                                  'Electrolitos neutros',
                                  'Aniones'],
                 'correcta': 'E'},
                {'pregunta': 'Los iones con carga positiva se llaman:',
                 'alternativas': ['Neutrones',
                                  'Fotones',
                                  'Cationes',
                                  'Aniones',
                                  'Electrones libres'],
                 'correcta': 'C'},
                {'pregunta': 'Las sales minerales más abundantes en el '
                             'cuerpo humano contienen fósforo y:',
                 'alternativas': ['Magnesio',
                                  'Cloro',
                                  'Potasio',
                                  'Calcio',
                                  'Sodio'],
                 'correcta': 'D'},
                {'pregunta': 'El electrolito cuya concentración elevada '
                             'produce hipertensión arterial es:',
                 'alternativas': ['El calcio',
                                  'El cloruro',
                                  'El magnesio',
                                  'El sodio',
                                  'El potasio'],
                 'correcta': 'D'},
                {'pregunta': 'El electrolito clave en la contracción '
                             'muscular y la coagulación de la sangre es:',
                 'alternativas': ['El calcio',
                                  'El fosfato',
                                  'El bicarbonato',
                                  'El cloruro',
                                  'El sodio'],
                 'correcta': 'A'},
                {'pregunta': 'El electrolito que actúa como cofactor '
                             'enzimático y forma parte de la clorofila es:',
                 'alternativas': ['El sodio',
                                  'El magnesio',
                                  'El calcio',
                                  'El fosfato',
                                  'El potasio'],
                 'correcta': 'B'},
                {'pregunta': 'El fosfato (PO₄³⁻) forma parte de nucleótidos, '
                             'ADN y:',
                 'alternativas': ['Lípidos exclusivamente',
                                  'Proteínas exclusivamente',
                                  'Carbohidratos exclusivamente',
                                  'ARN',
                                  'Vitaminas'],
                 'correcta': 'D'}]},
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
                {'titulo': '4.5 LÍPIDOS: CARACTERÍSTICAS Y FUNCIONES',
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
                {'titulo': '4.6 ÁCIDOS GRASOS',
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
                {'titulo': '4.7 PROTEÍNAS: CARACTERÍSTICAS Y FUNCIONES',
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
                {'titulo': '4.8 AMINOÁCIDOS ESENCIALES Y NO ESENCIALES',
                 'items': ['Todo aminoácido tiene un carbono central unido a '
                           'un grupo {amino}, un grupo carboxilo y un grupo '
                           '{R}.',
                           'El cuerpo humano puede sintetizar {10} '
                           'aminoácidos, llamados no esenciales.',
                           'Los otros {10} aminoácidos, llamados esenciales, '
                           'deben obtenerse mediante la {dieta}.',
                           'El huevo, la leche, la carne y el pescado '
                           'contienen todos los aminoácidos {esenciales}.']},
                {'titulo': '4.9 ÁCIDOS NUCLEICOS: COMPOSICIÓN',
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
                {'titulo': '4.10 EL ADN',
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
                {'titulo': '4.11 EL MODELO DE LA DOBLE HÉLICE',
                 'items': ['En {1953}, {Watson y Crick} propusieron el '
                           'modelo de la doble hélice del ADN, ganando el '
                           'Premio {Nobel}.',
                           'Las dos cadenas del ADN son {antiparalelas}, '
                           'unidas por puentes de hidrógeno entre bases A-T '
                           'y {C-G}.',
                           'El par de bases más estable es {C-G}, unido por '
                           'tres puentes de hidrógeno.']},
                {'titulo': '4.12 REPLICACIÓN DEL ADN',
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
                {'titulo': '4.13 EL ARN Y LA TRANSCRIPCIÓN',
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
                {'titulo': '4.14 TIPOS DE ARN',
                 'items': ['El {ARN mensajero} (ARNm) lleva la información '
                           'genética copiada del ADN en tripletes llamados '
                           '{codones}.',
                           'El {ARN de transferencia} (ARNt) sirve de '
                           'adaptador entre el ARNm y los aminoácidos, con '
                           'forma de {trébol}.',
                           'El {ARN ribosómico} (ARNr) forma los '
                           '{ribosomas}, junto con proteínas.']},
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
                 'alternativas': ['Ácidos nucleicos',
                                  'Lípidos',
                                  'Proteínas',
                                  'Aminoácidos',
                                  'Hidratos de carbono'],
                 'correcta': 'E'},
                {'pregunta': 'Los carbohidratos están formados por carbono, '
                             'hidrógeno y:',
                 'alternativas': ['Sodio',
                                  'Fósforo',
                                  'Azufre',
                                  'Oxígeno',
                                  'Nitrógeno'],
                 'correcta': 'D'},
                {'pregunta': 'En los carbohidratos, la relación entre '
                             'hidrógeno y oxígeno es de:',
                 'alternativas': ['4:1', '1:1', '1:2', '2:1', '3:1'],
                 'correcta': 'D'},
                {'pregunta': 'Los carbohidratos son sintetizados por los '
                             'autótrofos mediante:',
                 'alternativas': ['La fermentación',
                                  'La fotosíntesis',
                                  'La respiración celular',
                                  'La digestión',
                                  'La glucólisis exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula empírica general de los '
                             'carbohidratos es:',
                 'alternativas': ['C6H12O6 exclusivo',
                                  'NH3',
                                  '(CH2O)n',
                                  'H2O',
                                  'CO2'],
                 'correcta': 'C'},
                {'pregunta': 'La función de los carbohidratos que '
                             'proporciona energía de arranque se llama:',
                 'alternativas': ['Función catalítica',
                                  'Reserva energética',
                                  'Función estructural',
                                  'Fuente inmediata de energía',
                                  'Función hormonal'],
                 'correcta': 'D'},
                {'pregunta': 'El glucógeno almacenado en hígado y músculos '
                             'cumple la función de:',
                 'alternativas': ['Catálisis enzimática',
                                  'Material estructural',
                                  'Reserva energética',
                                  'Transporte de oxígeno',
                                  'Fuente inmediata de energía'],
                 'correcta': 'C'},
                {'pregunta': 'La celulosa, presente en fibras vegetales, '
                             'cumple principalmente una función:',
                 'alternativas': ['Energética inmediata',
                                  'Estructural',
                                  'Hormonal',
                                  'Catalítica',
                                  'De transporte'],
                 'correcta': 'B'},
                {'pregunta': 'Los azúcares más simples, dulces y '
                             'cristalizables, se llaman:',
                 'alternativas': ['Polisacáridos',
                                  'Monosacáridos',
                                  'Oligosacáridos exclusivamente',
                                  'Lípidos',
                                  'Disacáridos exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los monosacáridos que poseen grupo aldehído se '
                             'llaman:',
                 'alternativas': ['Hexosas exclusivamente',
                                  'Cetosas',
                                  'Pentosas exclusivamente',
                                  'Aldosas',
                                  'Triosas exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Los monosacáridos que poseen grupo cetona se '
                             'llaman:',
                 'alternativas': ['Cetosas',
                                  'Polisacáridos',
                                  'Disacáridos',
                                  'Aldosas',
                                  'Pentosas exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'La estructura cíclica con anillo de 5 átomos '
                             'de carbono, como en la glucosa, se llama:',
                 'alternativas': ['Lineal',
                                  'Cetosa exclusiva',
                                  'Aldosa exclusiva',
                                  'Furanosa',
                                  'Piranosa'],
                 'correcta': 'E'},
                {'pregunta': 'La estructura cíclica con anillo de 4 átomos '
                             'de carbono, como en la fructosa, se llama:',
                 'alternativas': ['Lineal',
                                  'Furanosa',
                                  'Hexosa exclusiva',
                                  'Pentosa exclusiva',
                                  'Piranosa'],
                 'correcta': 'B'},
                {'pregunta': 'Las pentosas más importantes, que forman parte '
                             'de los ácidos nucleicos, son la ribosa y la:',
                 'alternativas': ['Fructosa',
                                  'Desoxirribosa',
                                  'Galactosa',
                                  'Glucosa',
                                  'Manosa'],
                 'correcta': 'B'},
                {'pregunta': 'El monosacárido más abundante en la naturaleza '
                             'y principal fuente de energía es la:',
                 'alternativas': ['Fructosa',
                                  'Ribosa',
                                  'Glucosa',
                                  'Manosa',
                                  'Galactosa'],
                 'correcta': 'C'},
                {'pregunta': 'La galactosa no se encuentra libre, sino '
                             'combinada con la glucosa para formar:',
                 'alternativas': ['Celulosa',
                                  'Maltosa',
                                  'Almidón',
                                  'Sacarosa',
                                  'Lactosa'],
                 'correcta': 'E'},
                {'pregunta': 'La manosa es constituyente de glicoproteínas '
                             'de origen:',
                 'alternativas': ['Vegetal exclusivo',
                                  'Animal',
                                  'Mineral',
                                  'Bacteriano exclusivo',
                                  'Viral exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los oligosacáridos están formados por un '
                             'número de monosacáridos entre:',
                 'alternativas': ['10 y 100',
                                  '2 y 10',
                                  'Más de 1000',
                                  '100 y 1000',
                                  '1 y 2'],
                 'correcta': 'B'},
                {'pregunta': 'El enlace que une a los monosacáridos en los '
                             'oligosacáridos se llama enlace:',
                 'alternativas': ['Fosfodiéster',
                                  'O-glucosídico',
                                  'Iónico',
                                  'Peptídico',
                                  'De hidrógeno exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los disacáridos, oligosacáridos más '
                             'abundantes, están formados por la unión de:',
                 'alternativas': ['Dos monosacáridos',
                                  'Ningún monosacárido',
                                  'Diez monosacáridos',
                                  'Cien monosacáridos',
                                  'Un solo monosacárido'],
                 'correcta': 'A'},
                {'pregunta': 'Los lípidos son insolubles en agua pero '
                             'solubles en:',
                 'alternativas': ['Ácidos fuertes',
                                  'Solventes orgánicos como el cloroformo',
                                  'Bases débiles',
                                  'Ácidos nucleicos',
                                  'Sales minerales'],
                 'correcta': 'B'},
                {'pregunta': 'Los lípidos son anfipáticos porque tienen una '
                             'porción polar y otra:',
                 'alternativas': ['Hidrofóbica',
                                  'Básica',
                                  'Ácida',
                                  'Radiactiva',
                                  'Neutra exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Los ácidos grasos saturados se caracterizan '
                             'por tener:',
                 'alternativas': ['Dobles enlaces múltiples',
                                  'Anillos aromáticos',
                                  'Cadenas ramificadas',
                                  'Grupos amino',
                                  'Solo enlaces sencillos'],
                 'correcta': 'E'},
                {'pregunta': 'Los niveles elevados de ácidos grasos '
                             'saturados pueden producir:',
                 'alternativas': ['Anemia',
                                  'Osteoporosis',
                                  'Arterioesclerosis',
                                  'Diabetes exclusivamente',
                                  'Hipoglucemia'],
                 'correcta': 'C'},
                {'pregunta': 'Los ácidos grasos insaturados tienen uno o '
                             'más:',
                 'alternativas': ['Anillos aromáticos',
                                  'Dobles enlaces',
                                  'Grupos fosfato',
                                  'Grupos amino',
                                  'Puentes disulfuro'],
                 'correcta': 'B'},
                {'pregunta': 'El ácido palmítico, presente en grasas de '
                             'carnes rojas, tiene un número de carbonos '
                             'igual a:',
                 'alternativas': ['8', '24', '12', '16', '20'],
                 'correcta': 'D'},
                {'pregunta': 'Las proteínas son los compuestos orgánicos más '
                             'abundantes en las células, constituyendo '
                             'hasta:',
                 'alternativas': ['1% del peso seco',
                                  '90% del peso seco',
                                  '5% del peso seco',
                                  '10% del peso seco',
                                  '50% o más del peso seco'],
                 'correcta': 'E'},
                {'pregunta': 'Las proteínas están formadas por unidades '
                             'estructurales llamadas:',
                 'alternativas': ['Nucleótidos',
                                  'Bases nitrogenadas',
                                  'Aminoácidos',
                                  'Monosacáridos',
                                  'Ácidos grasos'],
                 'correcta': 'C'},
                {'pregunta': 'Del total de aminoácidos existentes en la '
                             'naturaleza, cuántos pueden formar proteínas:',
                 'alternativas': ['20', '100', '50', '10', '30'],
                 'correcta': 'A'},
                {'pregunta': 'La hemoglobina, que transporta oxígeno, es un '
                             'ejemplo de proteína con función:',
                 'alternativas': ['Enzimática',
                                  'De transporte',
                                  'Estructural',
                                  'Hormonal',
                                  'De reserva'],
                 'correcta': 'B'},
                {'pregunta': 'La queratina y el colágeno son ejemplos de '
                             'proteínas con función:',
                 'alternativas': ['Hormonal',
                                  'De transporte',
                                  'De defensa',
                                  'Enzimática',
                                  'Estructural'],
                 'correcta': 'E'},
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
                                  'Estructural',
                                  'Contráctil',
                                  'Enzimática exclusiva',
                                  'Hormonal'],
                 'correcta': 'E'},
                {'pregunta': 'El cuerpo humano puede sintetizar un número de '
                             'aminoácidos (no esenciales) igual a:',
                 'alternativas': ['20', '0', '5', '10', '15'],
                 'correcta': 'D'},
                {'pregunta': 'Los aminoácidos que deben obtenerse mediante '
                             'la dieta se llaman:',
                 'alternativas': ['Neutros',
                                  'Básicos exclusivos',
                                  'Esenciales',
                                  'Ácidos exclusivos',
                                  'No esenciales'],
                 'correcta': 'C'},
                {'pregunta': 'El modelo de la doble hélice del ADN fue '
                             'propuesto en 1953 por:',
                 'alternativas': ['Mendel y Darwin',
                                  'Schleiden y Schwann',
                                  'Watson y Crick',
                                  'Virchow y Hooke',
                                  'De Vries y Dobzhansky'],
                 'correcta': 'C'},
                {'pregunta': 'En el ADN, la adenina se une con la timina '
                             'mediante:',
                 'alternativas': ['Ningún enlace',
                                  'Dos puentes de hidrógeno',
                                  'Tres puentes de hidrógeno',
                                  'Un enlace covalente',
                                  'Un enlace iónico'],
                 'correcta': 'B'},
                {'pregunta': 'En el ADN, la guanina se une con la citosina '
                             'mediante:',
                 'alternativas': ['Tres puentes de hidrógeno',
                                  'Un enlace peptídico',
                                  'Dos puentes de hidrógeno',
                                  'Ningún enlace',
                                  'Un enlace covalente'],
                 'correcta': 'A'},
                {'pregunta': 'La replicación del ADN se llama '
                             'semiconservativa porque:',
                 'alternativas': ['Se pierde toda la información',
                                  'No se conserva ninguna hebra original',
                                  'Solo se replica la mitad del ADN',
                                  'Ambas hebras son completamente nuevas',
                                  'La nueva hélice tiene una hebra original '
                                  'y una nueva'],
                 'correcta': 'E'},
                {'pregunta': 'Los fragmentos discontinuos formados durante '
                             'la replicación del ADN se llaman:',
                 'alternativas': ['Fragmentos de Darwin',
                                  'Fragmentos de Watson',
                                  'Fragmentos de Okazaki',
                                  'Fragmentos de Mendel',
                                  'Fragmentos de Crick'],
                 'correcta': 'C'},
                {'pregunta': 'El ARN se diferencia del ADN porque tiene el '
                             'azúcar ribosa y la base:',
                 'alternativas': ['Adenina',
                                  'Citosina',
                                  'Guanina',
                                  'Timina',
                                  'Uracilo'],
                 'correcta': 'E'},
                {'pregunta': 'Las moléculas de ARN, a diferencia del ADN, '
                             'son:',
                 'alternativas': ['Monocatenarias',
                                  'Idénticas al ADN',
                                  'Bicatenarias',
                                  'Inexistentes en células',
                                  'Circulares exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El proceso de sintetizar ARN a partir de un '
                             'molde de ADN se llama:',
                 'alternativas': ['Translocación',
                                  'Transcripción',
                                  'Duplicación',
                                  'Replicación',
                                  'Traducción'],
                 'correcta': 'B'},
                {'pregunta': 'La enzima que cataliza la transcripción es:',
                 'alternativas': ['La primasa',
                                  'La ARN polimerasa',
                                  'La helicasa',
                                  'La ligasa',
                                  'La ADN polimerasa'],
                 'correcta': 'B'},
                {'pregunta': 'El ARN mensajero (ARNm) lleva la información '
                             'genética codificada en tripletes llamados:',
                 'alternativas': ['Codones',
                                  'Ribosomas',
                                  'Anticodones',
                                  'Nucleósidos',
                                  'Promotores'],
                 'correcta': 'A'},
                {'pregunta': 'El ARN de transferencia (ARNt) tiene una forma '
                             'característica que se asemeja a:',
                 'alternativas': ['Un trébol de cuatro hojas',
                                  'Una escalera',
                                  'Un cubo',
                                  'Una esfera',
                                  'Una hélice simple'],
                 'correcta': 'A'},
                {'pregunta': 'El ARN ribosómico (ARNr) forma parte de:',
                 'alternativas': ['Las mitocondrias exclusivamente',
                                  'El citoesqueleto',
                                  'La membrana celular',
                                  'Los ribosomas',
                                  'El núcleo exclusivamente'],
                 'correcta': 'D'}]},
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
                {'titulo': '5.5 MICOPLASMAS Y CIANOBACTERIAS',
                 'items': ['Los {micoplasmas} son las bacterias más pequeñas '
                           'conocidas, y carecen de {pared} celular.',
                           'Las {cianobacterias}, o algas verde-azules, son '
                           'procariotas capaces de realizar {fotosíntesis} '
                           'oxigénica.']},
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
                 'alternativas': ['Organelo',
                                  'Tejido',
                                  'Núcleo',
                                  'Membrana',
                                  'Pequeña habitación o celda'],
                 'correcta': 'E'},
                {'pregunta': 'La célula es considerada la unidad estructural '
                             'y:',
                 'alternativas': ['Atómica',
                                  'Ecológica',
                                  'Genética exclusiva',
                                  'Química exclusiva',
                                  'Funcional fundamental de los seres vivos'],
                 'correcta': 'E'},
                {'pregunta': 'El científico que introdujo el término '
                             '«célula» en 1665 fue:',
                 'alternativas': ['Schwann',
                                  'Virchow',
                                  'Robert Hooke',
                                  'Darwin',
                                  'Schleiden'],
                 'correcta': 'C'},
                {'pregunta': 'Robert Hooke publicó sus observaciones '
                             'celulares en el libro:',
                 'alternativas': ['El origen de las especies',
                                  'De Revolutionibus',
                                  'Micrographia',
                                  'Systema Naturae',
                                  'Principia'],
                 'correcta': 'C'},
                {'pregunta': 'Los fundadores de la teoría celular fueron '
                             'Schleiden y:',
                 'alternativas': ['Hooke',
                                  'Mendel',
                                  'Virchow',
                                  'Darwin',
                                  'Schwann'],
                 'correcta': 'E'},
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
                 'alternativas': ['Los hongos',
                                  'Los virus',
                                  'Los animales',
                                  'Los minerales',
                                  'Las bacterias'],
                 'correcta': 'C'},
                {'pregunta': 'La célebre frase «omnis cellula ex cellula» '
                             'fue sintetizada por:',
                 'alternativas': ['Robert Hooke',
                                  'Rudolph Virchow',
                                  'Schwann',
                                  'Schleiden',
                                  'Charles Darwin'],
                 'correcta': 'C'},
                {'pregunta': 'La frase «omnis cellula ex cellula» significa:',
                 'alternativas': ['Toda célula se origina de otra célula',
                                  'Toda célula es eucariota',
                                  'Toda célula tiene ADN circular',
                                  'Toda célula muere pronto',
                                  'Toda célula tiene núcleo'],
                 'correcta': 'A'},
                {'pregunta': 'Según la teoría celular, las actividades '
                             'esenciales de la vida ocurren:',
                 'alternativas': ['Solo en el citoplasma exclusivamente',
                                  'Solo en el núcleo',
                                  'En el interior de las células',
                                  'Fuera de las células',
                                  'Solo en la membrana'],
                 'correcta': 'C'},
                {'pregunta': 'Según la teoría celular, las nuevas células se '
                             'originan de:',
                 'alternativas': ['Fusión de tejidos',
                                  'Solo del ADN libre',
                                  'Células preexistentes, por división',
                                  'La nada',
                                  'Reacciones químicas espontáneas'],
                 'correcta': 'C'},
                {'pregunta': 'Las células contienen la información '
                             'hereditaria, que pasa de:',
                 'alternativas': ['Ninguna transmisión ocurre',
                                  'Tejidos a órganos',
                                  'Células hijas a progenitoras',
                                  'Células progenitoras a células hijas',
                                  'Órganos a sistemas'],
                 'correcta': 'D'},
                {'pregunta': 'El término «procariota» proviene del griego '
                             '«protos», que significa:',
                 'alternativas': ['Primitivo',
                                  'Núcleo',
                                  'Vida',
                                  'Verdadero',
                                  'Hueco'],
                 'correcta': 'A'},
                {'pregunta': 'El material genético de la célula procariota '
                             'es una molécula de ADN:',
                 'alternativas': ['Doble hélice exclusivamente eucariota',
                                  'Ramificada',
                                  'Circular',
                                  'Lineal',
                                  'Ausente'],
                 'correcta': 'C'},
                {'pregunta': 'En la célula procariota, el ADN se concentra '
                             'en una región llamada:',
                 'alternativas': ['Cromosoma',
                                  'Retículo',
                                  'Nucléolo',
                                  'Nucleoide',
                                  'Núcleo'],
                 'correcta': 'D'},
                {'pregunta': 'El término «eucariota» proviene del griego '
                             '«eu», que significa:',
                 'alternativas': ['Externo',
                                  'Hueco',
                                  'Primitivo',
                                  'Verdadero',
                                  'Pequeño'],
                 'correcta': 'D'},
                {'pregunta': 'En la célula eucariota, el ADN se encuentra '
                             'dentro de:',
                 'alternativas': ['El citoplasma sin protección',
                                  'Un núcleo verdadero con envoltura nuclear',
                                  'El nucleoide',
                                  'La membrana plasmática',
                                  'La pared celular'],
                 'correcta': 'B'},
                {'pregunta': 'Solo los organismos del reino monera son de '
                             'tipo celular:',
                 'alternativas': ['Viral',
                                  'Eucariota',
                                  'Procariota',
                                  'Mixto',
                                  'Ninguno de los anteriores'],
                 'correcta': 'C'},
                {'pregunta': 'Según el criterio de tres dominios, Archaea y '
                             'Bacteria agrupan a los organismos:',
                 'alternativas': ['Fúngicos exclusivamente',
                                  'Virales',
                                  'Procariotas',
                                  'Eucariotas',
                                  'Mixtos'],
                 'correcta': 'C'},
                {'pregunta': 'El dominio Eukarya agrupa a todos los '
                             'organismos:',
                 'alternativas': ['Eucariotas',
                                  'Procariotas',
                                  'Solo arqueas',
                                  'Solo bacterias',
                                  'Virales exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El glucocálix bacteriano, cuando es grueso y '
                             'rígido, se denomina:',
                 'alternativas': ['Periplasma',
                                  'Cápsula',
                                  'Membrana externa',
                                  'Mucílago',
                                  'Pared celular'],
                 'correcta': 'B'},
                {'pregunta': 'El principal componente de la pared celular '
                             'bacteriana es:',
                 'alternativas': ['La quitina',
                                  'El colesterol',
                                  'El peptidoglicano o mureína',
                                  'La celulosa',
                                  'La lignina'],
                 'correcta': 'C'},
                {'pregunta': 'La tinción que clasifica a las bacterias según '
                             'su pared celular se llama tinción de:',
                 'alternativas': ['Wright',
                                  'Gram',
                                  'Ziehl-Neelsen',
                                  'Giemsa',
                                  'Papanicolaou'],
                 'correcta': 'B'},
                {'pregunta': 'Las bacterias Gram positivas se caracterizan '
                             'por tener una pared con un contenido de '
                             'peptidoglicano de:',
                 'alternativas': ['0%',
                                  '100%',
                                  '10 a 20%',
                                  '30 a 40%',
                                  '60 a 90%'],
                 'correcta': 'E'},
                {'pregunta': 'Las bacterias Gram negativas poseen, además de '
                             'la pared, una estructura adicional llamada:',
                 'alternativas': ['Cápsula gruesa',
                                  'Membrana externa',
                                  'Mesosoma',
                                  'Flagelo',
                                  'Pili'],
                 'correcta': 'B'},
                {'pregunta': 'Las invaginaciones de la membrana plasmática '
                             'bacteriana que intervienen en la duplicación '
                             'del ADN se llaman:',
                 'alternativas': ['Pili',
                                  'Mesosomas',
                                  'Ribosomas',
                                  'Flagelos',
                                  'Plásmidos'],
                 'correcta': 'B'},
                {'pregunta': 'El material genético bacteriano se ubica en '
                             'una región llamada:',
                 'alternativas': ['Nucléolo',
                                  'Nucleoide',
                                  'Núcleo',
                                  'Cromátida',
                                  'Centrómero'],
                 'correcta': 'B'},
                {'pregunta': 'Las moléculas de ADN extracromosómico que '
                             'pueden conferir resistencia a antibióticos se '
                             'llaman:',
                 'alternativas': ['Ribosomas',
                                  'Mesosomas',
                                  'Plásmidos',
                                  'Flagelos',
                                  'Cápsulas'],
                 'correcta': 'C'},
                {'pregunta': 'Las estructuras filamentosas responsables de '
                             'la movilidad bacteriana se llaman:',
                 'alternativas': ['Mesosomas',
                                  'Ribosomas',
                                  'Cilios',
                                  'Flagelos',
                                  'Pili'],
                 'correcta': 'D'},
                {'pregunta': 'Los micoplasmas se caracterizan por ser las '
                             'bacterias más pequeñas y por carecer de:',
                 'alternativas': ['Ribosomas',
                                  'Pared celular',
                                  'Citoplasma',
                                  'Membrana plasmática',
                                  'ADN'],
                 'correcta': 'B'},
                {'pregunta': 'Las cianobacterias son capaces de realizar:',
                 'alternativas': ['Fotosíntesis oxigénica',
                                  'Ninguna función metabólica',
                                  'Quimiosíntesis exclusivamente',
                                  'Fermentación exclusiva',
                                  'Solo respiración anaerobia'],
                 'correcta': 'A'}]},
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
                {'titulo': '6.5 EL CITOPLASMA',
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
                {'titulo': '6.6 RIBOSOMAS Y RETÍCULO ENDOPLASMÁTICO',
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
                {'titulo': '6.7 COMPLEJO DE GOLGI Y LISOSOMAS',
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
                {'titulo': '6.8 MITOCONDRIAS',
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
                {'titulo': '6.9 PLASTOS Y CLOROPLASTOS',
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
                {'titulo': '6.10 EL NÚCLEO',
                 'items': ['El núcleo está ausente en los glóbulos rojos '
                           '{maduros} de los mamíferos.',
                           'El núcleo es considerado el «{cerebro}» de la '
                           'célula porque dirige todas las actividades '
                           'celulares.',
                           'La envoltura nuclear tiene doble membrana, con '
                           'aberturas llamadas {poros} nucleares.',
                           'El {nucleoplasma} es la parte interna del '
                           'núcleo, donde se encuentra el {nucléolo}.']},
                {'titulo': '6.11 CROMATINA Y NUCLÉOLO',
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
                {'titulo': '6.12 CROMOSOMAS',
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
                           'la {mitosis}.']},
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
                 'alternativas': ['El citoplasma libre',
                                  'La pared celular',
                                  'Una doble membrana o envoltura nuclear',
                                  'El nucleoide',
                                  'Una sola membrana'],
                 'correcta': 'C'},
                {'pregunta': 'Las tres partes principales de la célula '
                             'eucariota son membrana, citoplasma y:',
                 'alternativas': ['Glicocálix',
                                  'Pared celular',
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
                 'alternativas': ['Mucho más grandes',
                                  'Del mismo tamaño',
                                  'Sin núcleo definido',
                                  'Sin membrana',
                                  'Más pequeñas'],
                 'correcta': 'A'},
                {'pregunta': 'La pared celular está presente en:',
                 'alternativas': ['Células vegetales y hongos',
                                  'Solo bacterias',
                                  'Todas las células sin excepción',
                                  'Células animales exclusivamente',
                                  'Solo células humanas'],
                 'correcta': 'A'},
                {'pregunta': 'El principal componente estructural de la '
                             'pared celular vegetal es:',
                 'alternativas': ['La queratina',
                                  'La celulosa',
                                  'El glucógeno',
                                  'El colesterol',
                                  'La quitina'],
                 'correcta': 'B'},
                {'pregunta': 'Los puentes intercelulares entre células '
                             'vegetales adyacentes se llaman:',
                 'alternativas': ['Plasmodesmos',
                                  'Uniones estrechas',
                                  'Gap junctions exclusivas',
                                  'Desmosomas',
                                  'Sinapsis'],
                 'correcta': 'A'},
                {'pregunta': 'El componente de la pared celular de los '
                             'hongos es:',
                 'alternativas': ['La quitina',
                                  'El colesterol',
                                  'La celulosa',
                                  'La lignina exclusiva',
                                  'La queratina'],
                 'correcta': 'A'},
                {'pregunta': 'El glicocálix caracteriza a las células:',
                 'alternativas': ['Fúngicas',
                                  'Vegetales',
                                  'Bacterianas',
                                  'Animales',
                                  'Procariotas en general'],
                 'correcta': 'D'},
                {'pregunta': 'El glicocálix participa principalmente en:',
                 'alternativas': ['El reconocimiento celular',
                                  'La replicación del ADN',
                                  'La fotosíntesis',
                                  'La síntesis de proteínas',
                                  'La respiración celular'],
                 'correcta': 'A'},
                {'pregunta': 'La membrana plasmática es de naturaleza:',
                 'alternativas': ['Puramente lipídica',
                                  'Puramente proteica',
                                  'Mineral',
                                  'Lipoproteica',
                                  'Celulósica'],
                 'correcta': 'D'},
                {'pregunta': 'El modelo de estructura de la membrana celular '
                             'se denomina modelo de:',
                 'alternativas': ['Doble hélice',
                                  'Capa rígida',
                                  'Esfera sólida',
                                  'Red cristalina',
                                  'Mosaico fluido'],
                 'correcta': 'E'},
                {'pregunta': 'El modelo de mosaico fluido fue propuesto por:',
                 'alternativas': ['Mendel y Darwin',
                                  'Schleiden y Schwann',
                                  'Singer y Nicholson',
                                  'Watson y Crick',
                                  'Hooke y Virchow'],
                 'correcta': 'C'},
                {'pregunta': 'En la composición de la membrana, los lípidos '
                             'representan aproximadamente:',
                 'alternativas': ['40%', '90%', '52%', '8%', '100%'],
                 'correcta': 'A'},
                {'pregunta': 'En la composición de la membrana, las '
                             'proteínas representan aproximadamente:',
                 'alternativas': ['8%', '10%', '0%', '52%', '40%'],
                 'correcta': 'D'},
                {'pregunta': 'Los componentes lipídicos más abundantes de la '
                             'membrana son los:',
                 'alternativas': ['Carotenoides',
                                  'Triglicéridos',
                                  'Fosfolípidos',
                                  'Glicolípidos',
                                  'Esteroides'],
                 'correcta': 'C'},
                {'pregunta': 'El colesterol de la membrana celular es '
                             'responsable, entre otras cosas, de:',
                 'alternativas': ['La replicación del ADN',
                                  'La fluidez de la membrana',
                                  'El transporte activo exclusivo',
                                  'La síntesis de proteínas',
                                  'La rigidez total'],
                 'correcta': 'B'},
                {'pregunta': 'Las proteínas que se localizan en las '
                             'superficies de la membrana y son solubles en '
                             'agua se llaman:',
                 'alternativas': ['Periféricas o extrínsecas',
                                  'Enzimáticas exclusivas',
                                  'Integrales',
                                  'Glicoproteicas exclusivas',
                                  'Transmembrana'],
                 'correcta': 'A'},
                {'pregunta': 'Las proteínas que atraviesan todo el espesor '
                             'de la membrana se llaman proteínas:',
                 'alternativas': ['Extrínsecas',
                                  'Integrales o intrínsecas',
                                  'Superficiales',
                                  'Solubles en agua',
                                  'Periféricas'],
                 'correcta': 'B'},
                {'pregunta': 'Los carbohidratos de la membrana se encuentran '
                             'únicamente en:',
                 'alternativas': ['El citoplasma',
                                  'El núcleo',
                                  'La matriz mitocondrial',
                                  'La monocapa interna',
                                  'La superficie de la monocapa externa'],
                 'correcta': 'E'},
                {'pregunta': 'El citoplasma corresponde a la región entre la '
                             'membrana plasmática y:',
                 'alternativas': ['El citoesqueleto exclusivo',
                                  'La pared celular',
                                  'El nucléolo',
                                  'La membrana nuclear',
                                  'Los ribosomas'],
                 'correcta': 'D'},
                {'pregunta': 'En el citosol se producen los primeros pasos '
                             'de la degradación de nutrientes, como:',
                 'alternativas': ['La traducción',
                                  'La replicación del ADN',
                                  'La fotosíntesis',
                                  'La glucólisis',
                                  'La transcripción'],
                 'correcta': 'D'},
                {'pregunta': 'El citoesqueleto está formado por '
                             'microfilamentos, microtúbulos y:',
                 'alternativas': ['Filamentos intermedios',
                                  'Mitocondrias',
                                  'Cloroplastos',
                                  'Ribosomas',
                                  'Lisosomas'],
                 'correcta': 'A'},
                {'pregunta': 'Los microfilamentos de actina tienen un '
                             'diámetro aproximado de:',
                 'alternativas': ['25 nm', '7 nm', '50 nm', '1 nm', '100 nm'],
                 'correcta': 'B'},
                {'pregunta': 'Los microtúbulos de tubulina forman, entre '
                             'otras estructuras:',
                 'alternativas': ['La cromatina',
                                  'El citosol',
                                  'Los cilios y flagelos',
                                  'El nucléolo',
                                  'La pared celular'],
                 'correcta': 'C'},
                {'pregunta': 'Los centriolos están formados por nueve '
                             'tripletes de:',
                 'alternativas': ['Actina',
                                  'Microtúbulos',
                                  'Ribosomas',
                                  'Filamentos intermedios',
                                  'Queratina'],
                 'correcta': 'B'},
                {'pregunta': 'Los ribosomas se elaboran en:',
                 'alternativas': ['La mitocondria',
                                  'El aparato de Golgi',
                                  'El nucléolo',
                                  'Los lisosomas',
                                  'El citosol exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los ribosomas agrupados en el citosol forman '
                             'estructuras llamadas:',
                 'alternativas': ['Crestas',
                                  'Dictiosomas',
                                  'Polisomas o polirribosomas',
                                  'Cisternas',
                                  'Tilacoides'],
                 'correcta': 'C'},
                {'pregunta': 'El retículo endoplasmático rugoso se '
                             'caracteriza por estar cubierto de:',
                 'alternativas': ['Lisosomas',
                                  'Centriolos',
                                  'Cloroplastos',
                                  'Mitocondrias',
                                  'Ribosomas'],
                 'correcta': 'E'},
                {'pregunta': 'El retículo endoplasmático liso se especializa '
                             'en la síntesis de:',
                 'alternativas': ['Carbohidratos exclusivamente',
                                  'Lípidos',
                                  'ARN ribosómico',
                                  'Proteínas',
                                  'Ácidos nucleicos'],
                 'correcta': 'B'},
                {'pregunta': 'El complejo de Golgi está formado por sacos '
                             'apilados llamados:',
                 'alternativas': ['Polisomas',
                                  'Cisternas nucleares',
                                  'Dictiosomas',
                                  'Tilacoides',
                                  'Crestas'],
                 'correcta': 'C'},
                {'pregunta': 'La cara del complejo de Golgi más próxima al '
                             'retículo endoplasmático se llama cara:',
                 'alternativas': ['Lateral',
                                  'Externa',
                                  'Medial exclusiva',
                                  'Trans',
                                  'Cis'],
                 'correcta': 'E'},
                {'pregunta': 'Los lisosomas contienen enzimas digestivas que '
                             'funcionan en un ambiente:',
                 'alternativas': ['Básico',
                                  'Sin pH definido',
                                  'Alcalino',
                                  'Ácido',
                                  'Neutro'],
                 'correcta': 'D'},
                {'pregunta': 'Los lisosomas que se separan del Golgi por '
                             'gemación se llaman lisosomas:',
                 'alternativas': ['Autofágicos exclusivos',
                                  'Terciarios',
                                  'Nucleares',
                                  'Secundarios',
                                  'Primarios'],
                 'correcta': 'E'},
                {'pregunta': 'Las mitocondrias se encuentran en todas las '
                             'células eucariotas y tienen:',
                 'alternativas': ['Pared celular',
                                  'Doble membrana',
                                  'Ninguna membrana',
                                  'Membrana tilacoidal exclusiva',
                                  'Una sola membrana'],
                 'correcta': 'B'},
                {'pregunta': 'Los pliegues de la membrana mitocondrial '
                             'interna se llaman:',
                 'alternativas': ['Tilacoides',
                                  'Cisternas',
                                  'Dictiosomas',
                                  'Crestas mitocondriales',
                                  'Granas'],
                 'correcta': 'D'},
                {'pregunta': 'Las mitocondrias producen ATP mediante el '
                             'proceso de:',
                 'alternativas': ['Traducción',
                                  'Fotosíntesis',
                                  'Replicación',
                                  'Respiración celular',
                                  'Transcripción'],
                 'correcta': 'D'},
                {'pregunta': 'Los plastos con pigmento verde que realizan la '
                             'fotosíntesis se llaman:',
                 'alternativas': ['Cromoplastos',
                                  'Amiloplastos',
                                  'Cloroplastos',
                                  'Leucoplastos',
                                  'Etioplastos'],
                 'correcta': 'C'},
                {'pregunta': 'Los plastos que almacenan almidón, lípidos o '
                             'proteínas, con escasa pigmentación, se llaman:',
                 'alternativas': ['Cloroplastos',
                                  'Tilacoides',
                                  'Etioplastos',
                                  'Leucoplastos',
                                  'Cromoplastos'],
                 'correcta': 'D'},
                {'pregunta': 'La membrana del cloroplasto que forma discos '
                             'aplanados llamados tilacoides es la membrana:',
                 'alternativas': ['Externa',
                                  'Plasmática',
                                  'Tilacoidal',
                                  'Nuclear',
                                  'Interna exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'El núcleo está ausente en un tipo de célula '
                             'humana madura, que es:',
                 'alternativas': ['El glóbulo rojo',
                                  'La neurona',
                                  'El hepatocito',
                                  'La célula muscular',
                                  'El linfocito'],
                 'correcta': 'A'},
                {'pregunta': 'El núcleo es considerado el «cerebro» de la '
                             'célula porque:',
                 'alternativas': ['Solo forma parte del citoesqueleto',
                                  'Dirige todas las actividades celulares',
                                  'Produce energía',
                                  'No tiene función específica',
                                  'Solo almacena lípidos'],
                 'correcta': 'B'},
                {'pregunta': 'Las aberturas de la envoltura nuclear se '
                             'llaman:',
                 'alternativas': ['Poros nucleares',
                                  'Crestas',
                                  'Cisternas',
                                  'Dictiosomas',
                                  'Tilacoides'],
                 'correcta': 'A'},
                {'pregunta': 'La cromatina poco condensada se llama:',
                 'alternativas': ['Centrómero',
                                  'Cariotipo',
                                  'Heterocromatina',
                                  'Nucleoplasma',
                                  'Eucromatina'],
                 'correcta': 'E'},
                {'pregunta': 'La cromatina muy condensada se llama:',
                 'alternativas': ['Eucromatina',
                                  'Cariotipo',
                                  'Heterocromatina',
                                  'Nucléolo',
                                  'Nucleoplasma'],
                 'correcta': 'C'},
                {'pregunta': 'El nucléolo sintetiza casi todo el ARN de la '
                             'célula, en especial el:',
                 'alternativas': ['ARN de transferencia exclusivo',
                                  'ADN nuclear',
                                  'ARN ribosómico (ARNr)',
                                  'ADN mitocondrial',
                                  'ARN mensajero exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'Las células con dos juegos completos de '
                             'cromosomas se llaman células:',
                 'alternativas': ['Haploides',
                                  'Monoploides',
                                  'Diploides',
                                  'Poliploides exclusivas',
                                  'Triploides'],
                 'correcta': 'C'},
                {'pregunta': 'El número de cromosomas del ser humano (2n) '
                             'es:',
                 'alternativas': ['44', '46', '48', '23', '22'],
                 'correcta': 'B'},
                {'pregunta': 'De los 23 pares de cromosomas humanos, el '
                             'número de pares de autosomas es:',
                 'alternativas': ['22', '1', '24', '23', '46'],
                 'correcta': 'A'},
                {'pregunta': 'El centro cinético del cromosoma, esencial '
                             'para la segregación en la mitosis, se llama:',
                 'alternativas': ['Cinetocoro exclusivo',
                                  'Satélite',
                                  'Nucléolo',
                                  'Centrómero',
                                  'Telómero'],
                 'correcta': 'D'}]},
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
                {'titulo': '7.4 NUTRICIÓN HETERÓTROFA',
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
                {'titulo': '7.5 RESPIRACIÓN AERÓBICA',
                 'items': ['La respiración {aeróbica} requiere presencia de '
                           'oxígeno, produciendo dióxido de carbono y '
                           '{agua}.',
                           'La {glucólisis} es el proceso en que una '
                           'molécula de glucosa se rompe en dos moléculas de '
                           '{ácido pirúvico}, en el citosol.']},
                {'titulo': '7.6 RESPIRACIÓN ANAERÓBICA O FERMENTACIÓN',
                 'items': ['La respiración {anaeróbica}, o fermentación, se '
                           'lleva a cabo en {ausencia} de oxígeno.',
                           'En ambos tipos de fermentación ocurre primero la '
                           '{glucólisis} normal.',
                           'En esfuerzos musculares prolongados, la '
                           '{fermentación} produce un aporte rápido de '
                           'ATP.']},
                {'titulo': '7.7 TIPOS DE FERMENTACIÓN',
                 'items': ['En la fermentación {alcohólica}, los piruvatos '
                           'se reducen a {etanol}, con liberación de CO2.',
                           'La fermentación alcohólica es causada por '
                           '{levaduras}, como el Saccharomyces {cerevisiae}.',
                           'En la fermentación {láctica}, el ácido pirúvico '
                           'se reduce a {lactato} o ácido láctico.',
                           'La fermentación láctica es causada por bacterias '
                           'como {Lactobacillus} y Streptococcus.',
                           'Productos como el yogur se conservan bien porque '
                           'la fermentación láctica reduce el {pH}.']},
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
                 'alternativas': ['Heterótrofa',
                                  'Fotótrofa exclusiva',
                                  'Mixótrofa',
                                  'Saprótrofa exclusiva',
                                  'Quimiótrofa exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La nutrición realizada por células que '
                             'fabrican su propio alimento a partir de '
                             'compuestos inorgánicos es:',
                 'alternativas': ['Autótrofa',
                                  'Parasitaria',
                                  'Saprofita exclusiva',
                                  'Mixótrofa',
                                  'Heterótrofa'],
                 'correcta': 'A'},
                {'pregunta': 'Los dos procesos de nutrición autótrofa son la '
                             'quimioautótrofa y la:',
                 'alternativas': ['Simbiótica',
                                  'Fotoautótrofa',
                                  'Heterótrofa',
                                  'Saprófita',
                                  'Parasitaria'],
                 'correcta': 'B'},
                {'pregunta': 'La nutrición quimioautótrofa es característica '
                             'de los organismos:',
                 'alternativas': ['Animales exclusivamente',
                                  'Procariontes',
                                  'Fúngicos exclusivamente',
                                  'Eucariotas exclusivamente',
                                  'Vegetales exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos quimiótrofos utilizan energía '
                             'química obtenida mediante la oxidación de '
                             'productos:',
                 'alternativas': ['Solo proteínas',
                                  'Solo carbohidratos',
                                  'Inorgánicos',
                                  'Orgánicos exclusivamente',
                                  'Solo lípidos'],
                 'correcta': 'C'},
                {'pregunta': 'Los procariontes que oxidan compuestos de '
                             'azufre se llaman procariontes:',
                 'alternativas': ['Sulfurosos',
                                  'Ferrosos',
                                  'Fotótrofos',
                                  'Hidrogenosos',
                                  'Nitrificantes'],
                 'correcta': 'A'},
                {'pregunta': 'Los procariontes sulfurosos producen como '
                             'resultado de su oxidación:',
                 'alternativas': ['Ácido nítrico',
                                  'Ácido sulfúrico',
                                  'Ácido fosfórico',
                                  'Ácido clorhídrico',
                                  'Ácido carbónico'],
                 'correcta': 'B'},
                {'pregunta': 'Los procariontes que oxidan el hidrógeno del '
                             'aire se llaman procariontes:',
                 'alternativas': ['Sulfurosos',
                                  'Fotótrofos',
                                  'Ferrosos',
                                  'Nitrificantes',
                                  'Hidrogenosos'],
                 'correcta': 'E'},
                {'pregunta': 'Los procariontes que oxidan el hierro desde el '
                             'estado ferroso al férrico se llaman '
                             'procariontes:',
                 'alternativas': ['Sulfurosos',
                                  'Hidrogenosos',
                                  'Autótrofos exclusivos',
                                  'Ferrosos',
                                  'Nitrificantes'],
                 'correcta': 'D'},
                {'pregunta': 'Los procariontes que oxidan el amoniaco en '
                             'nitritos y estos en nitratos se llaman '
                             'procariontes:',
                 'alternativas': ['Hidrogenosos',
                                  'Fotótrofos',
                                  'Sulfurosos',
                                  'Nitrificantes',
                                  'Ferrosos'],
                 'correcta': 'D'},
                {'pregunta': 'Las bacterias nitrificantes desempeñan un '
                             'papel importante en:',
                 'alternativas': ['La reproducción celular',
                                  'La respiración animal',
                                  'La digestión humana',
                                  'La fertilidad de los suelos',
                                  'La fotosíntesis vegetal'],
                 'correcta': 'D'},
                {'pregunta': 'El organelo típicamente vegetal necesario para '
                             'la fotosíntesis es:',
                 'alternativas': ['El ribosoma',
                                  'La mitocondria',
                                  'El lisosoma',
                                  'El aparato de Golgi',
                                  'El cloroplasto'],
                 'correcta': 'E'},
                {'pregunta': 'Las pilas de «monedas» dentro del cloroplasto '
                             'se llaman:',
                 'alternativas': ['Cristas',
                                  'Estroma',
                                  'Tilacoides',
                                  'Matriz',
                                  'Cresta'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de tilacoides recibe el nombre de:',
                 'alternativas': ['Grana',
                                  'Matriz',
                                  'Nucleoide',
                                  'Cresta',
                                  'Estroma'],
                 'correcta': 'A'},
                {'pregunta': 'La sustancia rica en enzimas que rodea a los '
                             'tilacoides se llama:',
                 'alternativas': ['Estroma',
                                  'Cresta',
                                  'Citosol',
                                  'Grana',
                                  'Matriz mitocondrial'],
                 'correcta': 'A'},
                {'pregunta': 'La fotosíntesis transforma la energía luminosa '
                             'en energía:',
                 'alternativas': ['Química',
                                  'Nuclear',
                                  'Eléctrica',
                                  'Mecánica',
                                  'Térmica exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'Entre los reactivos necesarios para la '
                             'fotosíntesis figura la clorofila y:',
                 'alternativas': ['Dióxido de carbono, agua y luz solar',
                                  'Solo glucosa',
                                  'Solo agua',
                                  'Solo nitrógeno',
                                  'Solo oxígeno'],
                 'correcta': 'A'},
                {'pregunta': 'Los productos finales de la fotosíntesis son '
                             'glucosa y:',
                 'alternativas': ['Nitrógeno',
                                  'Agua exclusivamente',
                                  'Oxígeno',
                                  'Clorofila',
                                  'Dióxido de carbono'],
                 'correcta': 'C'},
                {'pregunta': 'La fase de la fotosíntesis que depende de la '
                             'luz se llama fase:',
                 'alternativas': ['I o luminosa',
                                  'II u oscura',
                                  'Anaeróbica',
                                  'Neutra',
                                  'Intermedia'],
                 'correcta': 'A'},
                {'pregunta': 'La fase de la fotosíntesis independiente de la '
                             'luz puede ocurrir:',
                 'alternativas': ['Solo en invierno',
                                  'Solo de noche',
                                  'Nunca',
                                  'De día y de noche',
                                  'Solo de día'],
                 'correcta': 'D'},
                {'pregunta': 'Un organismo heterótrofo es aquel que:',
                 'alternativas': ['Vive sin necesidad de nutrientes',
                                  'Solo realiza fotosíntesis',
                                  'No puede fabricar sus propios alimentos',
                                  'Solo se alimenta de minerales',
                                  'Fabrica sus propios alimentos'],
                 'correcta': 'C'},
                {'pregunta': 'Son organismos heterótrofos los animales, '
                             'hongos, protozoos y la mayoría de:',
                 'alternativas': ['Los virus exclusivamente',
                                  'Las bacterias',
                                  'Las algas',
                                  'Las plantas',
                                  'Los líquenes exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos que se alimentan de materia '
                             'orgánica en descomposición mediante absorción '
                             'se llaman:',
                 'alternativas': ['Fotoheterótrofos',
                                  'Carnívoros',
                                  'Quimioautótrofos',
                                  'Saprobios',
                                  'Predadores'],
                 'correcta': 'D'},
                {'pregunta': 'Los predadores clasificados según su alimento '
                             'pueden ser carnívoros o:',
                 'alternativas': ['Herbívoros',
                                  'Fotótrofos',
                                  'Quimiótrofos',
                                  'Detritívoros',
                                  'Saprobios'],
                 'correcta': 'A'},
                {'pregunta': 'La respiración aeróbica requiere presencia de:',
                 'alternativas': ['Metano',
                                  'Nitrógeno',
                                  'Dióxido de carbono exclusivo',
                                  'Hidrógeno libre',
                                  'Oxígeno'],
                 'correcta': 'E'},
                {'pregunta': 'La respiración aeróbica produce como desechos '
                             'dióxido de carbono y:',
                 'alternativas': ['Oxígeno puro',
                                  'Agua',
                                  'Glucosa',
                                  'Etanol',
                                  'Ácido láctico'],
                 'correcta': 'B'},
                {'pregunta': 'La glucólisis rompe una molécula de glucosa '
                             'para formar dos moléculas de:',
                 'alternativas': ['Etanol',
                                  'Ácido láctico',
                                  'ATP exclusivamente',
                                  'Agua',
                                  'Ácido pirúvico'],
                 'correcta': 'E'},
                {'pregunta': 'La glucólisis ocurre en:',
                 'alternativas': ['El núcleo',
                                  'La mitocondria',
                                  'El citosol',
                                  'El aparato de Golgi',
                                  'El cloroplasto'],
                 'correcta': 'C'},
                {'pregunta': 'La respiración anaeróbica, o fermentación, se '
                             'lleva a cabo en:',
                 'alternativas': ['Presencia abundante de oxígeno',
                                  'Total oscuridad',
                                  'Presencia de nitrógeno exclusivamente',
                                  'Altas temperaturas exclusivamente',
                                  'Ausencia de oxígeno'],
                 'correcta': 'E'},
                {'pregunta': 'En esfuerzos musculares prolongados, el cuerpo '
                             'humano recurre a:',
                 'alternativas': ['La fermentación para un aporte rápido de '
                                  'ATP',
                                  'La transcripción',
                                  'La quimiosíntesis',
                                  'Solo la fotosíntesis',
                                  'La respiración aeróbica exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'En la fermentación alcohólica, los piruvatos '
                             'se reducen a:',
                 'alternativas': ['Etanol',
                                  'ATP directamente',
                                  'Glucosa',
                                  'Ácido láctico',
                                  'Agua'],
                 'correcta': 'A'},
                {'pregunta': 'La fermentación alcohólica es causada '
                             'principalmente por:',
                 'alternativas': ['Protozoos',
                                  'Levaduras como Saccharomyces cerevisiae',
                                  'Bacterias lácticas',
                                  'Hongos filamentosos exclusivos',
                                  'Virus'],
                 'correcta': 'B'},
                {'pregunta': 'En la elaboración de pan, el dióxido de '
                             'carbono producido por la fermentación '
                             'alcohólica es responsable de:',
                 'alternativas': ['La textura dura',
                                  'El crecimiento de la masa',
                                  'El color oscuro',
                                  'La conservación',
                                  'El sabor amargo'],
                 'correcta': 'B'},
                {'pregunta': 'En la fermentación láctica, el ácido pirúvico '
                             'se reduce a:',
                 'alternativas': ['Etanol',
                                  'Dióxido de carbono',
                                  'Glucosa',
                                  'Agua',
                                  'Ácido láctico o lactato'],
                 'correcta': 'E'},
                {'pregunta': 'La fermentación láctica es causada, entre '
                             'otras bacterias, por:',
                 'alternativas': ['Lactobacillus sp.',
                                  'Salmonella',
                                  'Vibrio cholerae',
                                  'Saccharomyces cerevisiae',
                                  'Escherichia coli exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'El yogur y la leche agria se obtienen '
                             'mediante:',
                 'alternativas': ['Fotosíntesis',
                                  'Fermentación láctica',
                                  'Fermentación alcohólica',
                                  'Quimiosíntesis',
                                  'Respiración aeróbica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Los productos lácteos fermentados se conservan '
                             'bien debido a que la fermentación:',
                 'alternativas': ['Elimina toda el agua',
                                  'Aumenta la temperatura',
                                  'Aumenta el pH',
                                  'No afecta el pH',
                                  'Disminuye el pH, inhibiendo bacterias '
                                  'dañinas'],
                 'correcta': 'E'}]},
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
                {'titulo': '8.6 SISTEMA DIGESTIVO HUMANO: ÓRGANOS',
                 'items': ['El tubo digestivo, o tracto {gastrointestinal}, '
                           'incluye boca, faringe, esófago, estómago, '
                           'intestino delgado y {grueso}.',
                           'Las {glándulas anexas} al tubo digestivo son las '
                           'salivales, el {hígado}, las vías biliares y el '
                           'páncreas.',
                           'El {intestino delgado} se encarga de la '
                           'absorción de nutrientes; el {intestino grueso}, '
                           'de agua y ciertas vitaminas.']},
                {'titulo': '8.7 HISTOLOGÍA DEL TUBO DIGESTIVO',
                 'items': ['Las cuatro capas del tubo digestivo, de adentro '
                           'hacia afuera, son: {mucosa}, submucosa, '
                           '{muscular} y serosa.',
                           'La capa {mucosa} comprende el epitelio de '
                           'revestimiento y la lámina propia.',
                           'En la boca, faringe y esófago, la capa muscular '
                           'es de tipo {esquelético}; en el resto, de '
                           'músculo {liso}.']},
                {'titulo': '8.8 LA BOCA',
                 'items': ['La cavidad bucal se divide en {vestíbulo} bucal '
                           'y cavidad oral propiamente dicha.',
                           'Las paredes de la boca son: labios (pared '
                           '{anterior}), mejillas (paredes laterales), '
                           'paladar duro (pared {superior}) y paladar blando '
                           '(pared posterior).',
                           'Los dientes se disponen en dos {arcos} dentales, '
                           'superior e inferior; solo el arco {inferior} es '
                           'móvil.']},
                {'titulo': '8.9 SISTEMA CIRCULATORIO: TIPOS',
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
                {'titulo': '8.10 CIRCULACIÓN EN INVERTEBRADOS',
                 'items': ['Los {poríferos} y {cnidarios} no tienen sistema '
                           'circulatorio; el transporte es por difusión '
                           '{simple}.',
                           'En los cnidarios, la {cavidad gastrovascular} '
                           'hace las veces de órgano circulatorio.']},
                {'titulo': '8.11 LA SANGRE',
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
                {'titulo': '8.12 EL CORAZÓN',
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
                {'titulo': '8.13 EXCRECIÓN: CONCEPTO Y EN INVERTEBRADOS',
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
                {'titulo': '8.14 EXCRECIÓN EN VERTEBRADOS',
                 'items': ['Los {peces} excretan por los riñones y por '
                           'células {branquiales} especializadas.',
                           'Los {anfibios} excretan por los riñones '
                           '(mesonefros) y la {piel}.',
                           'Los {reptiles} excretan por riñones de tipo '
                           '{metanefros}, planos y lobulados.']},
                {'titulo': '8.15 EL RIÑÓN',
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
                {'titulo': '8.16 LA NEFRONA Y FORMACIÓN DE LA ORINA',
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
                           'regresa a la sangre.']},
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
                 'alternativas': ['Mixta obligatoria',
                                  'Fermentativa exclusiva',
                                  'Sin oxígeno',
                                  'Anaerobia',
                                  'Aerobia'],
                 'correcta': 'E'},
                {'pregunta': 'El oxígeno interviene en el paso final de la '
                             'cadena respiratoria, que ocurre en:',
                 'alternativas': ['La membrana mitocondrial',
                                  'El citoplasma',
                                  'El núcleo',
                                  'El aparato de Golgi',
                                  'El retículo endoplasmático'],
                 'correcta': 'A'},
                {'pregunta': 'El dióxido de carbono que se elimina proviene '
                             'del metabolismo celular, específicamente de la '
                             'glucólisis y:',
                 'alternativas': ['La replicación del ADN',
                                  'El ciclo de Krebs',
                                  'La fotosíntesis',
                                  'La mitosis',
                                  'La síntesis de proteínas'],
                 'correcta': 'B'},
                {'pregunta': 'Las vías respiratorias superiores comprenden '
                             'la nariz y:',
                 'alternativas': ['La tráquea',
                                  'Los alvéolos',
                                  'Los bronquios',
                                  'Los pulmones',
                                  'La faringe'],
                 'correcta': 'E'},
                {'pregunta': 'Las vías respiratorias inferiores incluyen la '
                             'laringe, la tráquea, los bronquios y:',
                 'alternativas': ['La faringe',
                                  'Las fosas nasales',
                                  'La nariz',
                                  'Los senos paranasales',
                                  'Los pulmones'],
                 'correcta': 'E'},
                {'pregunta': 'La porción del aparato respiratorio que '
                             'conduce el aire inspirado y espirado se llama '
                             'porción:',
                 'alternativas': ['Nasal exclusiva',
                                  'Conductora',
                                  'Bronquial exclusiva',
                                  'Alveolar exclusiva',
                                  'Respiratoria'],
                 'correcta': 'B'},
                {'pregunta': 'La porción del aparato respiratorio encargada '
                             'de oxigenar la sangre se llama porción:',
                 'alternativas': ['Nasal',
                                  'Respiratoria',
                                  'Faríngea exclusiva',
                                  'Traqueal exclusiva',
                                  'Conductora'],
                 'correcta': 'B'},
                {'pregunta': 'La porción respiratoria comprende bronquiolos '
                             'respiratorios, conductos alveolares y:',
                 'alternativas': ['Los alvéolos',
                                  'La laringe',
                                  'La tráquea',
                                  'La faringe',
                                  'Los cornetes'],
                 'correcta': 'A'},
                {'pregunta': 'El interior de la nariz está dividido en dos '
                             'cavidades nasales por:',
                 'alternativas': ['Los cornetes',
                                  'El tabique nasal',
                                  'Las coanas',
                                  'La faringe',
                                  'Los senos paranasales'],
                 'correcta': 'B'},
                {'pregunta': 'Las proyecciones recubiertas en las paredes '
                             'laterales de la mucosa nasal se llaman:',
                 'alternativas': ['Coanas',
                                  'Senos',
                                  'Meatos exclusivamente',
                                  'Vestíbulos',
                                  'Cornetes'],
                 'correcta': 'E'},
                {'pregunta': 'Las aberturas que comunican las fosas nasales '
                             'con la faringe se llaman:',
                 'alternativas': ['Coanas',
                                  'Narinas',
                                  'Cornetes',
                                  'Meatos',
                                  'Vestíbulos'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las funciones de la nariz figura '
                             'calentar, humedecer y:',
                 'alternativas': ['Filtrar el aire',
                                  'Eliminar bacterias del pulmón',
                                  'Regular la temperatura corporal total',
                                  'Oxigenar la sangre directamente',
                                  'Producir dióxido de carbono'],
                 'correcta': 'A'},
                {'pregunta': 'La nariz también cumple la función de recibir '
                             'los impulsos:',
                 'alternativas': ['Gustativos',
                                  'Visuales',
                                  'Olfatorios',
                                  'Táctiles exclusivos',
                                  'Auditivos'],
                 'correcta': 'C'},
                {'pregunta': 'La faringe es un órgano compartido por los '
                             'aparatos respiratorio y:',
                 'alternativas': ['Endocrino',
                                  'Circulatorio',
                                  'Nervioso',
                                  'Digestivo',
                                  'Excretor'],
                 'correcta': 'D'},
                {'pregunta': 'La faringe, externamente, mide '
                             'aproximadamente:',
                 'alternativas': ['12 a 13 cm',
                                  '1 metro',
                                  '30 a 40 cm',
                                  '2 a 3 cm',
                                  '50 cm'],
                 'correcta': 'A'},
                {'pregunta': 'La faringe se ubica por detrás de la cavidad '
                             'nasal y la boca, y por delante de:',
                 'alternativas': ['El esófago exclusivamente',
                                  'Los pulmones',
                                  'Las vértebras cervicales',
                                  'El corazón',
                                  'El estómago'],
                 'correcta': 'C'},
                {'pregunta': 'La parte superior de la faringe, ubicada '
                             'detrás de la nariz, se llama:',
                 'alternativas': ['Nasofaringe o rinofaringe',
                                  'Laringofaringe',
                                  'Orofaringe',
                                  'Bronquiofaringe',
                                  'Traqueofaringe'],
                 'correcta': 'A'},
                {'pregunta': 'Los sistemas que comparten la responsabilidad '
                             'de aportar oxígeno y eliminar dióxido de '
                             'carbono son el respiratorio y el:',
                 'alternativas': ['Endocrino',
                                  'Excretor',
                                  'Nervioso',
                                  'Digestivo',
                                  'Cardiovascular'],
                 'correcta': 'E'},
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
                 'alternativas': ['Un revestimiento mucoso',
                                  'Hueso exclusivo',
                                  'Solo piel',
                                  'Tejido adiposo exclusivo',
                                  'Cartílago exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'El alimento sirve como combustible para '
                             'energía y como fuente de sustancias para:',
                 'alternativas': ['Solo el movimiento',
                                  'Solo la reproducción',
                                  'Crecimiento y regeneración',
                                  'Solo la respiración',
                                  'Solo la excreción'],
                 'correcta': 'C'},
                {'pregunta': 'La digestión que ocurre dentro de la célula, '
                             'tras englobar el alimento por fagocitosis, se '
                             'llama digestión:',
                 'alternativas': ['Intracelular',
                                  'Extracelular',
                                  'Celenterónica',
                                  'Mixta',
                                  'Enterónica'],
                 'correcta': 'A'},
                {'pregunta': 'Las esponjas digieren su alimento '
                             'completamente mediante el mecanismo:',
                 'alternativas': ['Extracelular',
                                  'Enterónico',
                                  'Intracelular',
                                  'Ninguno de los anteriores',
                                  'Mixto'],
                 'correcta': 'C'},
                {'pregunta': 'La digestión que descompone el alimento fuera '
                             'de las células se llama digestión:',
                 'alternativas': ['Intracelular',
                                  'Extracelular',
                                  'Ninguna de las anteriores',
                                  'Mixta exclusiva',
                                  'Fagocítica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'En los cnidarios y planarias ocurre un tipo de '
                             'digestión llamada:',
                 'alternativas': ['Ninguna digestión real',
                                  'Fotosintética',
                                  'Solo extracelular',
                                  'Solo intracelular',
                                  'Mixta (extracelular e intracelular)'],
                 'correcta': 'E'},
                {'pregunta': 'El tubo digestivo con un solo orificio para '
                             'entrada y salida de alimento se llama tubo '
                             'digestivo:',
                 'alternativas': ['Incompleto o celenterónico',
                                  'Circular',
                                  'Completo o enterónico',
                                  'Doble',
                                  'Mixto'],
                 'correcta': 'A'},
                {'pregunta': 'El tubo digestivo con boca y ano separados se '
                             'llama tubo digestivo:',
                 'alternativas': ['Celenterónico',
                                  'Único',
                                  'Completo o enterónico',
                                  'Simple',
                                  'Incompleto'],
                 'correcta': 'C'},
                {'pregunta': 'La cavidad gastrovascular, presente en '
                             'cnidarios, cumple funciones de digestión y:',
                 'alternativas': ['Respiración exclusiva',
                                  'Distribución de nutrientes',
                                  'Circulación sanguínea',
                                  'Excreción exclusiva',
                                  'Reproducción exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Los poríferos, como las esponjas, no poseen '
                             'aparato digestivo ni:',
                 'alternativas': ['Amebocitos',
                                  'Poros',
                                  'Coanocitos',
                                  'Boca',
                                  'Agua'],
                 'correcta': 'D'},
                {'pregunta': 'En las esponjas, las células flageladas en '
                             'collar se llaman:',
                 'alternativas': ['Tentáculos',
                                  'Cnidocitos',
                                  'Coanocitos',
                                  'Nematocistos',
                                  'Amebocitos'],
                 'correcta': 'C'},
                {'pregunta': 'Las células urticantes especializadas de los '
                             'cnidarios se llaman:',
                 'alternativas': ['Rádulas',
                                  'Cnidocitos',
                                  'Amebocitos',
                                  'Tiflosoles',
                                  'Coanocitos'],
                 'correcta': 'B'},
                {'pregunta': 'Los platelmintos de vida libre, como las '
                             'planarias, tienen una cavidad digestiva:',
                 'alternativas': ['Doble',
                                  'Completa, con ano',
                                  'Incompleta, sin ano',
                                  'Ausente por completo',
                                  'Externa'],
                 'correcta': 'C'},
                {'pregunta': 'Los nemátodos tienen un tubo digestivo:',
                 'alternativas': ['Ausente',
                                  'Incompleto',
                                  'Solo intracelular',
                                  'Sin órganos definidos',
                                  'Completo, con boca y ano separados'],
                 'correcta': 'E'},
                {'pregunta': 'En los anélidos, el órgano donde el alimento '
                             'es triturado se llama:',
                 'alternativas': ['Recto',
                                  'Molleja',
                                  'Faringe',
                                  'Esófago',
                                  'Buche'],
                 'correcta': 'B'},
                {'pregunta': 'El pliegue interno del intestino de los '
                             'anélidos, que aumenta la superficie de '
                             'absorción, se llama:',
                 'alternativas': ['Cnidocito',
                                  'Tiflosol',
                                  'Molleja',
                                  'Buche',
                                  'Rádula'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano bucal de los moluscos, similar a una '
                             'lengua con dientes quitinosos, se llama:',
                 'alternativas': ['Molleja',
                                  'Rádula',
                                  'Buche',
                                  'Tiflosol',
                                  'Faringe'],
                 'correcta': 'B'},
                {'pregunta': 'El tubo digestivo humano también se llama '
                             'tracto:',
                 'alternativas': ['Respiratorio',
                                  'Gastrointestinal',
                                  'Nervioso',
                                  'Excretor',
                                  'Circulatorio'],
                 'correcta': 'B'},
                {'pregunta': 'Las glándulas anexas al tubo digestivo '
                             'incluyen las salivales, el hígado, las vías '
                             'biliares y:',
                 'alternativas': ['El corazón',
                                  'Los pulmones',
                                  'Los riñones',
                                  'El bazo',
                                  'El páncreas'],
                 'correcta': 'E'},
                {'pregunta': 'El órgano encargado principalmente de la '
                             'absorción de nutrientes es:',
                 'alternativas': ['El intestino grueso',
                                  'El esófago',
                                  'La faringe',
                                  'El intestino delgado',
                                  'El estómago'],
                 'correcta': 'D'},
                {'pregunta': 'El intestino grueso se encarga principalmente '
                             'de la absorción de agua y:',
                 'alternativas': ['Aminoácidos exclusivamente',
                                  'Proteínas',
                                  'Glucosa exclusivamente',
                                  'Grasas exclusivamente',
                                  'Ciertas vitaminas'],
                 'correcta': 'E'},
                {'pregunta': 'Las cuatro capas del tubo digestivo, de '
                             'adentro hacia afuera, son mucosa, submucosa, '
                             'muscular y:',
                 'alternativas': ['Ósea',
                                  'Cartilaginosa',
                                  'Nerviosa',
                                  'Epitelial',
                                  'Serosa'],
                 'correcta': 'E'},
                {'pregunta': 'En la boca, faringe y esófago, la capa '
                             'muscular del tubo digestivo es de tipo:',
                 'alternativas': ['Liso',
                                  'Esquelético',
                                  'Cardíaco',
                                  'Ausente',
                                  'Mixto exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'En el resto del tracto digestivo, la capa '
                             'muscular es de músculo:',
                 'alternativas': ['Esquelético',
                                  'Ausente',
                                  'Estriado exclusivo',
                                  'Liso',
                                  'Cardíaco'],
                 'correcta': 'D'},
                {'pregunta': 'La cavidad bucal se divide en cavidad oral '
                             'propiamente dicha y:',
                 'alternativas': ['Faringe',
                                  'Estómago',
                                  'Esófago',
                                  'Laringe',
                                  'Vestíbulo bucal'],
                 'correcta': 'E'},
                {'pregunta': 'De los dos arcos dentales, el que es móvil es '
                             'el arco:',
                 'alternativas': ['Inferior',
                                  'Superior',
                                  'Central',
                                  'Ninguno es móvil',
                                  'Ambos son móviles'],
                 'correcta': 'A'},
                {'pregunta': 'Las partes principales del sistema '
                             'circulatorio son el corazón, la sangre y:',
                 'alternativas': ['Los riñones',
                                  'Los vasos sanguíneos',
                                  'El bazo',
                                  'Los pulmones',
                                  'El hígado'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema circulatorio que confina la sangre '
                             'al corazón y una serie de vasos se llama '
                             'sistema:',
                 'alternativas': ['Difuso',
                                  'Abierto',
                                  'Cerrado',
                                  'Simple exclusivo',
                                  'Lagunar'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema circulatorio en el que la sangre '
                             'baña directamente los tejidos se llama '
                             'sistema:',
                 'alternativas': ['Cerrado',
                                  'Abierto',
                                  'Doble',
                                  'Completo',
                                  'Vascular puro'],
                 'correcta': 'B'},
                {'pregunta': 'El espacio lagunar del sistema circulatorio '
                             'abierto se llama:',
                 'alternativas': ['Endocardio',
                                  'Pseudoceloma',
                                  'Miocardio',
                                  'Mediastino',
                                  'Hemocele'],
                 'correcta': 'E'},
                {'pregunta': 'La circulación en la que la sangre pasa una '
                             'sola vez por el corazón en cada circuito se '
                             'llama circulación:',
                 'alternativas': ['Mixta',
                                  'Doble',
                                  'Simple',
                                  'Completa exclusiva',
                                  'Incompleta'],
                 'correcta': 'C'},
                {'pregunta': 'La circulación simple es propia de:',
                 'alternativas': ['Los reptiles',
                                  'Las aves',
                                  'Los anfibios',
                                  'Los mamíferos',
                                  'La mayoría de los peces'],
                 'correcta': 'E'},
                {'pregunta': 'La circulación doble incompleta, con mezcla de '
                             'sangre arterial y venosa, se presenta en:',
                 'alternativas': ['Anfibios y reptiles',
                                  'Solo peces',
                                  'Solo mamíferos',
                                  'Solo aves',
                                  'Aves y mamíferos'],
                 'correcta': 'A'},
                {'pregunta': 'La circulación doble completa, sin mezcla de '
                             'sangre, es propia de:',
                 'alternativas': ['Anfibios y reptiles',
                                  'Aves y mamíferos',
                                  'Solo peces',
                                  'Solo anfibios',
                                  'Solo invertebrados'],
                 'correcta': 'B'},
                {'pregunta': 'Los poríferos y cnidarios realizan el '
                             'transporte de sustancias por:',
                 'alternativas': ['Un sistema cerrado',
                                  'Vasos sanguíneos',
                                  'Bombeo cardíaco',
                                  'Difusión simple',
                                  'Un sistema abierto complejo'],
                 'correcta': 'D'},
                {'pregunta': 'En los cnidarios, la estructura que hace las '
                             'veces de órgano circulatorio es:',
                 'alternativas': ['Los vasos sanguíneos',
                                  'El corazón',
                                  'El hemocele',
                                  'El pseudoceloma',
                                  'La cavidad gastrovascular'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema circulatorio también se conoce como '
                             'sistema:',
                 'alternativas': ['Linfático',
                                  'Cardiovascular',
                                  'Excretor',
                                  'Nervioso',
                                  'Digestivo'],
                 'correcta': 'B'},
                {'pregunta': 'La sangre está formada por plasma y tres tipos '
                             'de células: eritrocitos, leucocitos y:',
                 'alternativas': ['Adipocitos',
                                  'Plaquetas',
                                  'Osteocitos',
                                  'Neuronas',
                                  'Linfocitos exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los glóbulos rojos transportan oxígeno gracias '
                             'a la presencia de hierro en:',
                 'alternativas': ['Las plaquetas',
                                  'Los leucocitos',
                                  'La hemoglobina',
                                  'El colágeno',
                                  'El plasma'],
                 'correcta': 'C'},
                {'pregunta': 'Los glóbulos rojos, al madurar, pierden:',
                 'alternativas': ['La membrana',
                                  'El color',
                                  'El núcleo',
                                  'El citoplasma completo',
                                  'Toda su forma'],
                 'correcta': 'C'},
                {'pregunta': 'Los glóbulos blancos participan principalmente '
                             'en:',
                 'alternativas': ['La digestión',
                                  'La coagulación',
                                  'La defensa del organismo',
                                  'El transporte de nutrientes',
                                  'El transporte de oxígeno'],
                 'correcta': 'C'},
                {'pregunta': 'El proceso de formación de los glóbulos '
                             'blancos se llama:',
                 'alternativas': ['Trombopoyesis exclusiva',
                                  'Mitosis exclusiva',
                                  'Eritropoyesis exclusiva',
                                  'Fagocitosis',
                                  'Hematopoyesis'],
                 'correcta': 'E'},
                {'pregunta': 'Las plaquetas se forman a partir de grandes '
                             'células llamadas:',
                 'alternativas': ['Fagocitos',
                                  'Eritrocitos',
                                  'Linfocitos',
                                  'Megacariocitos',
                                  'Leucocitos'],
                 'correcta': 'D'},
                {'pregunta': 'Las plaquetas intervienen principalmente en:',
                 'alternativas': ['El transporte de oxígeno',
                                  'La digestión',
                                  'La defensa inmunitaria',
                                  'La respiración',
                                  'La coagulación de la sangre'],
                 'correcta': 'E'},
                {'pregunta': 'El corazón se encuentra ubicado en un espacio '
                             'llamado:',
                 'alternativas': ['Pleura',
                                  'Diafragma exclusivo',
                                  'Retroperitoneo',
                                  'Mediastino',
                                  'Peritoneo'],
                 'correcta': 'D'},
                {'pregunta': 'El corazón posee cuatro cavidades: dos '
                             'aurículas y:',
                 'alternativas': ['Dos válvulas',
                                  'Dos tabiques',
                                  'Dos ventrículos',
                                  'Dos arterias',
                                  'Dos venas cavas'],
                 'correcta': 'C'},
                {'pregunta': 'Las tres capas del corazón son endocardio, '
                             'miocardio y:',
                 'alternativas': ['Peritoneo',
                                  'Mesocardio',
                                  'Endotelio exclusivo',
                                  'Pericardio exclusivo',
                                  'Epicardio'],
                 'correcta': 'E'},
                {'pregunta': 'La válvula que conecta el ventrículo izquierdo '
                             'con la aurícula izquierda se llama:',
                 'alternativas': ['Aórtica exclusiva',
                                  'Semilunar exclusiva',
                                  'Mitral o bicúspide',
                                  'Tricúspide',
                                  'Pulmonar exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La válvula que conecta el ventrículo derecho '
                             'con la aurícula derecha se llama:',
                 'alternativas': ['Mitral',
                                  'Aórtica',
                                  'Semilunar',
                                  'Tricúspide',
                                  'Bicúspide'],
                 'correcta': 'D'},
                {'pregunta': 'El movimiento de contracción del corazón se '
                             'llama:',
                 'alternativas': ['Sístole',
                                  'Mitosis',
                                  'Diástole',
                                  'Peristalsis',
                                  'Miosis'],
                 'correcta': 'A'},
                {'pregunta': 'El movimiento de relajación del corazón se '
                             'llama:',
                 'alternativas': ['Fibrilación',
                                  'Sístole',
                                  'Mitosis',
                                  'Miosis',
                                  'Diástole'],
                 'correcta': 'E'},
                {'pregunta': 'La excreción se define como el proceso por el '
                             'cual los seres vivos liberan:',
                 'alternativas': ['Solo oxígeno',
                                  'Nutrientes esenciales',
                                  'Solo agua',
                                  'Productos de desecho del metabolismo',
                                  'Hormonas exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'La excreción tiene por objeto principalmente '
                             'eliminar sustancias:',
                 'alternativas': ['Nitrogenadas',
                                  'Glucídicas exclusivamente',
                                  'Vitamínicas',
                                  'Minerales',
                                  'Grasas exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los poríferos y cnidarios eliminan desechos '
                             'principalmente en forma de:',
                 'alternativas': ['Amoniaco',
                                  'Creatinina',
                                  'Ácido úrico exclusivo',
                                  'Bilirrubina',
                                  'Urea'],
                 'correcta': 'A'},
                {'pregunta': 'Los platelmintos poseen órganos excretores '
                             'llamados:',
                 'alternativas': ['Protonefridios',
                                  'Glándulas coxales',
                                  'Nefronas',
                                  'Metanefridios',
                                  'Tubos de Malpighi'],
                 'correcta': 'A'},
                {'pregunta': 'Los anélidos poseen órganos excretores '
                             'llamados:',
                 'alternativas': ['Protonefridios',
                                  'Tubos de Malpighi',
                                  'Metanefridios',
                                  'Riñones',
                                  'Nefronas'],
                 'correcta': 'C'},
                {'pregunta': 'Los insectos, arácnidos y miriápodos excretan '
                             'mediante:',
                 'alternativas': ['Los tubos de Malpighi',
                                  'Riñones',
                                  'Metanefridios',
                                  'Protonefridios',
                                  'Branquias exclusivas'],
                 'correcta': 'A'},
                {'pregunta': 'Los peces excretan por los riñones y por:',
                 'alternativas': ['La piel',
                                  'Los pulmones',
                                  'Células branquiales especializadas',
                                  'El intestino exclusivamente',
                                  'El hígado exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Los anfibios excretan por los riñones '
                             '(mesonefros) y también por:',
                 'alternativas': ['La piel',
                                  'Los tubos de Malpighi',
                                  'El intestino',
                                  'Las branquias',
                                  'El hígado'],
                 'correcta': 'A'},
                {'pregunta': 'Los riñones de los reptiles son de tipo:',
                 'alternativas': ['Pronefros',
                                  'Metanefros',
                                  'Tubos de Malpighi',
                                  'Mesonefros',
                                  'Protonefridios'],
                 'correcta': 'B'},
                {'pregunta': 'El aparato excretor humano se compone de dos '
                             'riñones y un conjunto de:',
                 'alternativas': ['Bronquios',
                                  'Vías urinarias',
                                  'Alvéolos',
                                  'Vasos linfáticos',
                                  'Glándulas salivales'],
                 'correcta': 'B'},
                {'pregunta': 'El riñón se encarga de producir la orina y del '
                             'proceso de:',
                 'alternativas': ['Coagulación',
                                  'Fotosíntesis',
                                  'Respiración celular',
                                  'Osmorregulación',
                                  'Digestión'],
                 'correcta': 'D'},
                {'pregunta': 'El peso aproximado de cada riñón humano es de:',
                 'alternativas': ['1000 gramos',
                                  '50 gramos',
                                  '150 gramos',
                                  '500 gramos',
                                  '10 gramos'],
                 'correcta': 'C'},
                {'pregunta': 'Los riñones se dividen en tres zonas: corteza, '
                             'médula y:',
                 'alternativas': ['Pelvis renal',
                                  'Uréter',
                                  'Vejiga',
                                  'Uretra',
                                  'Cápsula'],
                 'correcta': 'A'},
                {'pregunta': 'Las estructuras triangulares de la médula '
                             'renal se llaman pirámides de:',
                 'alternativas': ['Henle',
                                  'Wolff',
                                  'Golgi',
                                  'Bowman',
                                  'Malpighi'],
                 'correcta': 'E'},
                {'pregunta': 'La unidad estructural y funcional del riñón es '
                             'la:',
                 'alternativas': ['Cápsula renal',
                                  'Pirámide renal',
                                  'Pelvis renal',
                                  'Médula renal',
                                  'Nefrona'],
                 'correcta': 'E'},
                {'pregunta': 'Cada riñón tiene aproximadamente un número de '
                             'nefronas de:',
                 'alternativas': ['100',
                                  '100 000 000',
                                  '10 000',
                                  '1 000',
                                  '1 000 000'],
                 'correcta': 'E'},
                {'pregunta': 'La cápsula de Bowman contiene en su interior '
                             'al:',
                 'alternativas': ['Uréter',
                                  'Glomérulo de Malpighi',
                                  'Túbulo contorneado',
                                  'Asa de Henle exclusiva',
                                  'Cáliz renal'],
                 'correcta': 'B'},
                {'pregunta': 'El túbulo de la nefrona se divide en túbulo '
                             'contorneado proximal, asa de Henle y:',
                 'alternativas': ['Uréter',
                                  'Túbulo contorneado distal',
                                  'Glomérulo',
                                  'Pelvis renal',
                                  'Cápsula de Bowman'],
                 'correcta': 'B'},
                {'pregunta': 'La orina se forma mediante tres procesos: '
                             'filtración, secreción y:',
                 'alternativas': ['Reabsorción',
                                  'Fermentación',
                                  'Excreción',
                                  'Coagulación',
                                  'Digestión'],
                 'correcta': 'A'},
                {'pregunta': 'En el proceso de filtración, las proteínas y '
                             'células sanguíneas:',
                 'alternativas': ['Atraviesan libremente los capilares',
                                  'Se transforman en urea',
                                  'Se destruyen completamente',
                                  'Forman parte de la orina final',
                                  'No atraviesan los capilares glomerulares'],
                 'correcta': 'E'},
                {'pregunta': 'En el proceso de reabsorción, el porcentaje '
                             'del filtrado que regresa a la sangre es '
                             'aproximadamente:',
                 'alternativas': ['10%', '25%', '100%', '50%', 'Más del 90%'],
                 'correcta': 'E'}]},
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
                           'y la médula.']},
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
                 'alternativas': ['Los centros de control',
                                  'El sistema excretor',
                                  'El sistema circulatorio',
                                  'El sistema digestivo',
                                  'Los órganos efectores directamente'],
                 'correcta': 'A'},
                {'pregunta': 'La unidad funcional básica del sistema '
                             'nervioso es:',
                 'alternativas': ['La dendrita exclusivamente',
                                  'La neurona',
                                  'La célula glial',
                                  'La sinapsis exclusivamente',
                                  'El axón exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos más sencillos en tener células '
                             'nerviosas son los:',
                 'alternativas': ['Cnidarios',
                                  'Nematodos',
                                  'Platelmintos',
                                  'Anélidos',
                                  'Artrópodos'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema nervioso de los cnidarios se '
                             'caracteriza por ser:',
                 'alternativas': ['Una red difusa de protoneuronas',
                                  'Un sistema hiponeuro avanzado',
                                  'Un tubo neural',
                                  'Muy centralizado',
                                  'Un cerebro complejo'],
                 'correcta': 'A'},
                {'pregunta': 'El primer grupo de animales con sistema '
                             'nervioso hiponeuro son los:',
                 'alternativas': ['Cnidarios',
                                  'Platelmintos',
                                  'Vertebrados',
                                  'Artrópodos',
                                  'Moluscos'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de concentración de células '
                             'nerviosas en la región anterior del animal se '
                             'llama:',
                 'alternativas': ['Invaginación',
                                  'Neurulación',
                                  'Cefalización',
                                  'Metamerización',
                                  'Segmentación'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema nervioso de los nematodos se '
                             'estructura alrededor de:',
                 'alternativas': ['Un anillo nervioso alrededor del esófago',
                                  'Un tubo neural',
                                  'Ganglios dispersos sin conexión',
                                  'Un cerebro complejo',
                                  'La médula espinal'],
                 'correcta': 'A'},
                {'pregunta': 'Los anélidos presentan un cordón nervioso '
                             'central que se divide, en cada metámero, en:',
                 'alternativas': ['Tres nervios',
                                  'Cuatro nervios',
                                  'Dos nervios laterales',
                                  'Ningún nervio adicional',
                                  'Un solo nervio'],
                 'correcta': 'C'},
                {'pregunta': 'En los cefalópodos, el sistema nervioso '
                             'alcanza una complejidad similar a la de:',
                 'alternativas': ['Los cnidarios',
                                  'Los nematodos',
                                  'Ningún otro grupo',
                                  'Los platelmintos',
                                  'Los vertebrados'],
                 'correcta': 'E'},
                {'pregunta': 'El cerebro de los artrópodos está formado por '
                             'tres pares de ganglios, diferenciados en '
                             'protocerebro, deutocerebro y:',
                 'alternativas': ['Tritocerebro',
                                  'Mesocerebro',
                                  'Ectocerebro',
                                  'Endocerebro',
                                  'Metacerebro'],
                 'correcta': 'A'},
                {'pregunta': 'En los vertebrados, el sistema nervioso se '
                             'forma por invaginación dorsal de:',
                 'alternativas': ['El mesodermo',
                                  'El endodermo',
                                  'El celoma',
                                  'La notocorda exclusiva',
                                  'El ectodermo'],
                 'correcta': 'E'},
                {'pregunta': 'La invaginación dorsal del ectodermo en '
                             'vertebrados da lugar a un cordón hueco '
                             'llamado:',
                 'alternativas': ['Blastocele',
                                  'Celoma',
                                  'Tubo neural',
                                  'Notocorda',
                                  'Arquenterón'],
                 'correcta': 'C'},
                {'pregunta': 'En los vertebrados se diferencian dos regiones '
                             'funcionales del sistema nervioso: el encéfalo '
                             'y:',
                 'alternativas': ['Los riñones',
                                  'La médula espinal',
                                  'El hígado',
                                  'El corazón',
                                  'Los pulmones'],
                 'correcta': 'B'},
                {'pregunta': 'El encéfalo de los vertebrados está protegido '
                             'por:',
                 'alternativas': ['La caja craneal',
                                  'El tejido adiposo',
                                  'El canal vertebral',
                                  'La piel exclusivamente',
                                  'Los músculos exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'La médula espinal de los vertebrados está '
                             'protegida por:',
                 'alternativas': ['La caja craneal',
                                  'Las costillas exclusivamente',
                                  'El canal vertebral',
                                  'La piel exclusivamente',
                                  'El diafragma'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema nervioso central está formado por '
                             'el encéfalo y:',
                 'alternativas': ['Los órganos sensoriales',
                                  'Las glándulas endocrinas',
                                  'Los nervios periféricos',
                                  'Los ganglios simpáticos',
                                  'La médula espinal'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema nervioso periférico está formado '
                             'por:',
                 'alternativas': ['Solo el encéfalo',
                                  'Solo el cerebelo',
                                  'Solo el bulbo raquídeo',
                                  'Solo la médula espinal',
                                  'Los nervios que recorren el organismo'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema nervioso que regula las funciones '
                             'voluntarias, como el movimiento muscular, se '
                             'llama sistema nervioso:',
                 'alternativas': ['Autónomo',
                                  'Somático',
                                  'Simpático exclusivo',
                                  'Entérico',
                                  'Parasimpático exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso que controla las funciones '
                             'inconscientes del organismo se llama sistema '
                             'nervioso:',
                 'alternativas': ['Somático',
                                  'Periférico exclusivo',
                                  'Central exclusivo',
                                  'Autónomo o vegetativo',
                                  'Motor exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'Además de la neurona, otro componente '
                             'importante del sistema nervioso, aunque no '
                             'todos los animales lo poseen, son:',
                 'alternativas': ['Los linfocitos',
                                  'Los plaquetas',
                                  'Los osteocitos',
                                  'Las células gliales',
                                  'Los eritrocitos'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema nervioso humano se divide en '
                             'sistema nervioso central y sistema nervioso:',
                 'alternativas': ['Periférico',
                                  'Simpático exclusivo',
                                  'Voluntario',
                                  'Somático exclusivo',
                                  'Autónomo exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'El número de neuronas en el cerebro humano '
                             'ronda aproximadamente:',
                 'alternativas': ['100 millones',
                                  '100 000 millones',
                                  '1 millón',
                                  '10 000 millones',
                                  '1000 millones'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema nervioso central está conformado '
                             'por el encéfalo y:',
                 'alternativas': ['Los músculos',
                                  'Las neuronas motoras',
                                  'Los nervios periféricos',
                                  'Los ganglios',
                                  'La médula espinal'],
                 'correcta': 'E'},
                {'pregunta': 'El encéfalo incluye el bulbo raquídeo, la '
                             'protuberancia, el mesencéfalo, el cerebelo, el '
                             'diencéfalo y:',
                 'alternativas': ['La médula espinal',
                                  'Los nervios craneales',
                                  'El cerebro',
                                  'Los ganglios',
                                  'Los nervios espinales'],
                 'correcta': 'C'},
                {'pregunta': 'La médula espinal interviene en la transmisión '
                             'del tacto y de señales:',
                 'alternativas': ['Solo gustativas',
                                  'Solo olfativas',
                                  'Solo visuales',
                                  'Sensitivas de músculos y articulaciones',
                                  'Solo auditivas'],
                 'correcta': 'D'},
                {'pregunta': 'Los nervios son cordones de sustancia blanca '
                             'formados por axones y:',
                 'alternativas': ['Ribosomas exclusivos',
                                  'Dendritas',
                                  'Lisosomas exclusivos',
                                  'Mitocondrias exclusivas',
                                  'Núcleos'],
                 'correcta': 'B'},
                {'pregunta': 'Los nervios que se localizan en la cabeza y '
                             'controlan sus funciones se llaman nervios:',
                 'alternativas': ['Somáticos exclusivos',
                                  'Autónomos exclusivos',
                                  'Periféricos exclusivos',
                                  'Craneales',
                                  'Espinales'],
                 'correcta': 'D'},
                {'pregunta': 'Los nervios ramificados en pares en las '
                             'vértebras de la columna se llaman nervios:',
                 'alternativas': ['Cerebrales exclusivos',
                                  'Craneales',
                                  'Espinales',
                                  'Centrales exclusivos',
                                  'Autónomos exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'Las estructuras formadas por cuerpos de '
                             'neuronas ubicados fuera del encéfalo y la '
                             'médula se llaman:',
                 'alternativas': ['Sinapsis',
                                  'Axones',
                                  'Ganglios',
                                  'Dendritas',
                                  'Nervios'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema nervioso humano funciona, en '
                             'conjunto, como un ente que:',
                 'alternativas': ['Organiza, controla y coordina las '
                                  'funciones corporales',
                                  'Solo transporta oxígeno',
                                  'Solo produce hormonas',
                                  'Solo filtra la sangre',
                                  'Solo digiere alimentos'],
                 'correcta': 'A'}]},
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
                {'titulo': '10.5 LA MEIOSIS',
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
                {'titulo': '10.6 REPRODUCCIÓN SEXUAL: CONCEPTO Y FECUNDACIÓN',
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
                {'titulo': '10.7 GAMETOS Y TIPOS DE ORGANISMOS SEGÚN SU SEXO',
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
                           'vertebrados.']},
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
                 'alternativas': ['Solo gametos masculinos',
                                  'Dos organismos',
                                  'Solo gametos femeninos',
                                  'Ningún organismo',
                                  'Un solo organismo'],
                 'correcta': 'E'},
                {'pregunta': 'La descendencia producida por reproducción '
                             'asexual es, respecto al progenitor:',
                 'alternativas': ['Genéticamente idéntica',
                                  'Sin ninguna relación genética',
                                  'Siempre mutada',
                                  'Genéticamente diferente',
                                  'Parcialmente similar solamente'],
                 'correcta': 'A'},
                {'pregunta': 'En la reproducción asexual participan células '
                             'de tipo:',
                 'alternativas': ['Somáticas',
                                  'Solo espermatozoides',
                                  'Sexuales o gametos',
                                  'Ninguna célula específica',
                                  'Solo óvulos'],
                 'correcta': 'A'},
                {'pregunta': 'La escisión binaria se da por una '
                             'estrangulación en:',
                 'alternativas': ['Ningún punto específico',
                                  'El plano medio del organismo',
                                  'La membrana externa solamente',
                                  'El polo de la célula',
                                  'El núcleo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria transversal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Hidra',
                                  'Paramecium',
                                  'Plasmodium',
                                  'Euglena',
                                  'Planaria'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión binaria longitudinal ocurre, por '
                             'ejemplo, en:',
                 'alternativas': ['Paramecium',
                                  'Plasmodium',
                                  'Euglena o Astasia',
                                  'Estrella de mar',
                                  'Hidra'],
                 'correcta': 'C'},
                {'pregunta': 'La formación de una yema o botón que se rodea '
                             'de citoplasma se llama:',
                 'alternativas': ['Escisión binaria',
                                  'Fragmentación',
                                  'Gemación',
                                  'Autotomía',
                                  'Esporulación'],
                 'correcta': 'C'},
                {'pregunta': 'La gemación ocurre, entre otros organismos, en '
                             'poríferos y:',
                 'alternativas': ['Mamíferos',
                                  'Peces',
                                  'Aves',
                                  'Celentéreos',
                                  'Reptiles'],
                 'correcta': 'D'},
                {'pregunta': 'Una forma especial de gemación, presente en '
                             'medusas y céstodos, se llama:',
                 'alternativas': ['Autotomía',
                                  'Esporulación',
                                  'Estrobilación',
                                  'Fragmentación',
                                  'Bipartición'],
                 'correcta': 'C'},
                {'pregunta': 'La esporulación consiste en divisiones '
                             'mitóticas del núcleo que finalmente liberan:',
                 'alternativas': ['Esporas',
                                  'Fragmentos',
                                  'Gametos',
                                  'Larvas',
                                  'Yemas'],
                 'correcta': 'A'},
                {'pregunta': 'El Plasmodium, agente causante de la malaria, '
                             'se reproduce por:',
                 'alternativas': ['Escisión binaria',
                                  'Esporulación',
                                  'Gemación',
                                  'Fragmentación',
                                  'Autotomía'],
                 'correcta': 'B'},
                {'pregunta': 'La escisión del progenitor en dos o más '
                             'partes, cada una capaz de originar un nuevo '
                             'animal, se llama:',
                 'alternativas': ['Bipartición',
                                  'Esporulación',
                                  'Estrobilación',
                                  'Fragmentación',
                                  'Gemación'],
                 'correcta': 'D'},
                {'pregunta': 'La fragmentación se observa, por ejemplo, en '
                             'estrellas de mar y:',
                 'alternativas': ['Mamíferos',
                                  'Reptiles',
                                  'Peces óseos',
                                  'Aves',
                                  'Planarias'],
                 'correcta': 'E'},
                {'pregunta': 'El fenómeno por el cual un crustáceo o lagarto '
                             'desprende un apéndice o la cola ante el '
                             'peligro se llama:',
                 'alternativas': ['Escisión',
                                  'Fragmentación',
                                  'Gemación',
                                  'Autotomía',
                                  'Esporulación'],
                 'correcta': 'D'},
                {'pregunta': 'La reproducción asexual es común en '
                             'microorganismos, plantas y animales de '
                             'organización:',
                 'alternativas': ['Muy compleja',
                                  'Simple',
                                  'Sin organización',
                                  'Exclusivamente mamífera',
                                  'Exclusivamente vertebrada'],
                 'correcta': 'B'},
                {'pregunta': 'La característica que mejor distingue a los '
                             'seres vivos de la materia no viva es la '
                             'capacidad de:',
                 'alternativas': ['Perpetuar su propia especie',
                                  'Producir sonidos',
                                  'Moverse',
                                  'Emitir luz',
                                  'Cambiar de color'],
                 'correcta': 'A'},
                {'pregunta': 'En organismos eucariotas existen dos tipos de '
                             'división celular: mitosis y:',
                 'alternativas': ['Meiosis',
                                  'Esporulación',
                                  'Fragmentación',
                                  'Gemación',
                                  'Escisión binaria'],
                 'correcta': 'A'},
                {'pregunta': 'La división celular que produce células '
                             'genéticamente idénticas a la célula madre es:',
                 'alternativas': ['La meiosis',
                                  'La mitosis',
                                  'La gemación',
                                  'La fragmentación',
                                  'La esporulación'],
                 'correcta': 'B'},
                {'pregunta': 'La división celular que produce células con la '
                             'mitad del contenido genético de la célula '
                             'madre es:',
                 'alternativas': ['La meiosis',
                                  'La gemación',
                                  'La mitosis',
                                  'La fragmentación',
                                  'La escisión binaria'],
                 'correcta': 'A'},
                {'pregunta': 'Rudolf Virchow resumió el concepto de '
                             'continuidad celular con el axioma en latín:',
                 'alternativas': ['In vino veritas',
                                  'Cogito ergo sum',
                                  'Carpe diem',
                                  'Ad astra per aspera',
                                  'Omnis cellula e cellula'],
                 'correcta': 'E'},
                {'pregunta': 'La meiosis consiste en un par de divisiones '
                             'celulares que reducen el número de cromosomas '
                             'a:',
                 'alternativas': ['La mitad',
                                  'Un cuarto',
                                  'Ninguna reducción',
                                  'El triple',
                                  'El doble'],
                 'correcta': 'A'},
                {'pregunta': 'Los cromosomas iguales que se emparejan '
                             'durante la meiosis se llaman cromosomas:',
                 'alternativas': ['Homólogos',
                                  'Satélite',
                                  'Autosomas exclusivos',
                                  'Sexuales exclusivos',
                                  'Acéntricos'],
                 'correcta': 'A'},
                {'pregunta': 'El número haploide del ser humano es:',
                 'alternativas': ['22', '46', '23', '48', '44'],
                 'correcta': 'C'},
                {'pregunta': 'El número diploide del ser humano es:',
                 'alternativas': ['46', '23', '22', '24', '44'],
                 'correcta': 'A'},
                {'pregunta': 'Los gametos humanos (óvulos y espermatozoides) '
                             'llevan el número:',
                 'alternativas': ['Haploide',
                                  'Tetraploide',
                                  'Diploide',
                                  'Triploide',
                                  'Ninguno definido'],
                 'correcta': 'A'},
                {'pregunta': 'El intercambio de segmentos entre cromátidas '
                             'homólogas durante la meiosis se llama:',
                 'alternativas': ['Fecundación',
                                  'Gemación',
                                  'Recombinación genética o crossing over',
                                  'Mitosis',
                                  'Esporulación'],
                 'correcta': 'C'},
                {'pregunta': 'Cada par de cromosomas apareados durante la '
                             'meiosis, con cuatro cromátidas, se llama:',
                 'alternativas': ['Cigoto',
                                  'Bivalente o tétrada',
                                  'Gameto',
                                  'Diploide',
                                  'Haploide'],
                 'correcta': 'B'},
                {'pregunta': 'Las conexiones donde ocurrió el intercambio '
                             'genético en la meiosis se llaman:',
                 'alternativas': ['Quiasmas',
                                  'Centrómeros',
                                  'Nucléolos',
                                  'Cinetocoros',
                                  'Telómeros'],
                 'correcta': 'A'},
                {'pregunta': 'La reproducción sexual implica la fusión de '
                             'dos:',
                 'alternativas': ['Órganos',
                                  'Embriones',
                                  'Gametos',
                                  'Células somáticas',
                                  'Cigotos'],
                 'correcta': 'C'},
                {'pregunta': 'La reproducción sexual promueve principalmente '
                             'la:',
                 'alternativas': ['Clonación exacta',
                                  'Variabilidad genética',
                                  'Reducción de la población',
                                  'Identidad genética total',
                                  'Eliminación de mutaciones'],
                 'correcta': 'B'},
                {'pregunta': 'La unión de dos gametos se llama:',
                 'alternativas': ['Gemación',
                                  'Fecundación',
                                  'Meiosis',
                                  'Esporulación',
                                  'Mitosis'],
                 'correcta': 'B'},
                {'pregunta': 'La fecundación que ocurre en el agua, fuera '
                             'del cuerpo, se llama fecundación:',
                 'alternativas': ['Interna',
                                  'Artificial',
                                  'Asexual',
                                  'Mixta',
                                  'Externa'],
                 'correcta': 'E'},
                {'pregunta': 'La fecundación que ocurre dentro del cuerpo de '
                             'la hembra se llama fecundación:',
                 'alternativas': ['Ausente',
                                  'Artificial',
                                  'Externa',
                                  'Interna',
                                  'Mixta'],
                 'correcta': 'D'},
                {'pregunta': 'Los gametos masculinos, de menor tamaño, se '
                             'llaman:',
                 'alternativas': ['Espermatozoides',
                                  'Ovocitos',
                                  'Cigotos',
                                  'Óvulos',
                                  'Gónadas'],
                 'correcta': 'A'},
                {'pregunta': 'Los espermatozoides se producen en:',
                 'alternativas': ['La vagina',
                                  'El útero',
                                  'Los ovarios',
                                  'Los testículos',
                                  'Las trompas'],
                 'correcta': 'D'},
                {'pregunta': 'Los organismos que tienen órganos '
                             'reproductivos masculinos y femeninos a la vez '
                             'se llaman:',
                 'alternativas': ['Monoicos o hermafroditas',
                                  'Partenogenéticos',
                                  'Unisexuales',
                                  'Dioicos',
                                  'Ovíparos'],
                 'correcta': 'A'},
                {'pregunta': 'Los hermafroditas que producen óvulos y '
                             'espermatozoides al mismo tiempo se llaman '
                             'hermafroditas:',
                 'alternativas': ['Protóginos exclusivos',
                                  'Simultáneos',
                                  'Protándricos exclusivos',
                                  'Dioicos',
                                  'Secuenciales'],
                 'correcta': 'B'},
                {'pregunta': 'Los hermafroditas que cambian de sexo durante '
                             'su vida se llaman hermafroditas:',
                 'alternativas': ['Simultáneos',
                                  'Monoicos puros',
                                  'Secuenciales',
                                  'Asexuales',
                                  'Dioicos'],
                 'correcta': 'C'},
                {'pregunta': 'Un organismo que nace macho y luego se '
                             'transforma en hembra se llama:',
                 'alternativas': ['Monoico puro',
                                  'Protándrico',
                                  'Dioico',
                                  'Protógino',
                                  'Hermafrodita simultáneo'],
                 'correcta': 'B'},
                {'pregunta': 'Los organismos con sexos separados, como la '
                             'mayoría de los vertebrados, se llaman:',
                 'alternativas': ['Partenogenéticos',
                                  'Andróginos',
                                  'Hermafroditas',
                                  'Monoicos',
                                  'Dioicos o unisexuales'],
                 'correcta': 'E'}]},
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
                 'alternativas': ['Cromosoma',
                                  'Especie',
                                  'Herencia',
                                  'Llegar a ser',
                                  'Célula'],
                 'correcta': 'D'},
                {'pregunta': 'La genética es la rama de la biología que '
                             'estudia:',
                 'alternativas': ['Solo la nutrición',
                                  'La herencia biológica de los seres vivos',
                                  'Solo la ecología',
                                  'Solo la evolución',
                                  'Solo la fotosíntesis'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia la '
                             'organización y replicación del ADN es la '
                             'genética:',
                 'alternativas': ['Clásica',
                                  'Molecular',
                                  'De poblaciones',
                                  'Ambiental',
                                  'Aplicada exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la genética que estudia el conjunto '
                             'de genes de una población, vinculada a la '
                             'evolución, es la genética:',
                 'alternativas': ['Clásica',
                                  'Molecular',
                                  'Celular',
                                  'De poblaciones',
                                  'Aplicada'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la genética que estudia cómo un '
                             'organismo hereda y transmite sus genes es la '
                             'genética:',
                 'alternativas': ['De poblaciones',
                                  'Molecular',
                                  'Aplicada',
                                  'Ambiental',
                                  'Clásica o de transmisión'],
                 'correcta': 'A'},
                {'pregunta': 'El científico asociado a la genética clásica, '
                             'descubridor de las leyes de la herencia, es:',
                 'alternativas': ['Crick',
                                  'Gregor Mendel',
                                  'Watson',
                                  'Darwin',
                                  'Virchow'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad de la herencia que produce la '
                             'expresión característica observable se llama:',
                 'alternativas': ['Alelo',
                                  'Gen',
                                  'Cromosoma',
                                  'Locus',
                                  'Fenotipo'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio específico en la cadena nucleotídica '
                             'donde se encuentra un gen se llama:',
                 'alternativas': ['Genoma',
                                  'Fenotipo',
                                  'Alelo',
                                  'Genotipo',
                                  'Locus'],
                 'correcta': 'E'},
                {'pregunta': 'Cada una de las variantes génicas que '
                             'determinan un carácter se llama:',
                 'alternativas': ['Genoma',
                                  'Locus',
                                  'Nucleótido',
                                  'Cromátida',
                                  'Alelo'],
                 'correcta': 'E'},
                {'pregunta': 'El alelo que se manifiesta siempre, '
                             'representado con letra mayúscula, se llama '
                             'alelo:',
                 'alternativas': ['Neutro',
                                  'Dominante',
                                  'Recesivo',
                                  'Mutante',
                                  'Codominante'],
                 'correcta': 'B'},
                {'pregunta': 'El alelo que solo se manifiesta si no está '
                             'presente el dominante se llama alelo:',
                 'alternativas': ['Neutro',
                                  'Codominante',
                                  'Dominante',
                                  'Letal',
                                  'Recesivo'],
                 'correcta': 'E'},
                {'pregunta': 'La expresión observable determinada por el '
                             'genotipo, «lo que se ve», se llama:',
                 'alternativas': ['Locus',
                                  'Genoma',
                                  'Genotipo',
                                  'Alelo',
                                  'Fenotipo'],
                 'correcta': 'E'},
                {'pregunta': 'La dotación genética de un individuo para un '
                             'carácter determinado se llama:',
                 'alternativas': ['Locus',
                                  'Genotipo',
                                  'Fenotipo',
                                  'Alelo',
                                  'Cromátida'],
                 'correcta': 'B'},
                {'pregunta': 'El individuo que porta dos alelos idénticos '
                             'para un carácter se llama:',
                 'alternativas': ['Híbrido exclusivo',
                                  'Mutante',
                                  'Recesivo puro',
                                  'Heterocigoto',
                                  'Homocigoto'],
                 'correcta': 'E'},
                {'pregunta': 'El individuo que porta dos alelos distintos '
                             'para un carácter se llama:',
                 'alternativas': ['Recesivo puro',
                                  'Puro',
                                  'Heterocigoto',
                                  'Dominante puro',
                                  'Homocigoto'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de genes de una especie se llama:',
                 'alternativas': ['Fenotipo',
                                  'Locus',
                                  'Genoma',
                                  'Cromátida',
                                  'Alelo'],
                 'correcta': 'C'},
                {'pregunta': 'AA se representa como un ejemplo de genotipo:',
                 'alternativas': ['Codominante',
                                  'Ligado al sexo',
                                  'Homocigoto recesivo',
                                  'Homocigoto dominante',
                                  'Heterocigoto'],
                 'correcta': 'D'},
                {'pregunta': 'Aa se representa como un ejemplo de genotipo:',
                 'alternativas': ['Heterocigoto',
                                  'Nulo',
                                  'Homocigoto dominante',
                                  'Letal',
                                  'Homocigoto recesivo'],
                 'correcta': 'A'},
                {'pregunta': 'En agricultura y ganadería, la elección de '
                             'especies con rasgos deseables se llama:',
                 'alternativas': ['Selección natural',
                                  'Mutación dirigida',
                                  'Deriva génica',
                                  'Selección artificial',
                                  'Migración génica'],
                 'correcta': 'D'},
                {'pregunta': 'En biotecnología, medicamentos son '
                             'sintetizados por bacterias y hongos que han '
                             'sido:',
                 'alternativas': ['Extinguidos',
                                  'Fosilizados',
                                  'Manipulados genéticamente',
                                  'Domesticados sin cambios',
                                  'Eliminados del ecosistema'],
                 'correcta': 'C'}]},
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
                           'membranas, e inicio de la {herencia}.']},
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
                 'alternativas': ['Nuevas especies a lo largo del tiempo',
                                  'Solo caracteres adquiridos',
                                  'Solo mutaciones aisladas',
                                  'Nuevos individuos idénticos',
                                  'Ninguna variación'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «evolución» fue empleada por '
                             'primera vez por:',
                 'alternativas': ['Mendel',
                                  'Lamarck',
                                  'Darwin',
                                  'Charles Bonnet',
                                  'De Vries'],
                 'correcta': 'D'},
                {'pregunta': 'La hipótesis que explicaba los fósiles por '
                             'catástrofes periódicas se llama:',
                 'alternativas': ['Mutacionismo',
                                  'Catastrofismo',
                                  'Transformismo',
                                  'Selección natural',
                                  'Teoría sintética'],
                 'correcta': 'B'},
                {'pregunta': 'La primera hipótesis completa de la evolución '
                             'fue formulada por:',
                 'alternativas': ['Wallace',
                                  'Lamarck',
                                  'Darwin',
                                  'Dobzhansky',
                                  'De Vries'],
                 'correcta': 'B'},
                {'pregunta': 'Lamarck publicó su hipótesis en 1809 en el '
                             'libro:',
                 'alternativas': ['Pangénesis intracelular',
                                  'Filosofía Zoológica',
                                  'La Genética y el Origen de las Especies',
                                  'Principios de Biología',
                                  'El origen de las especies'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de Lamarck según el cual las '
                             'estructuras más usadas se desarrollan se '
                             'llama:',
                 'alternativas': ['Herencia mendeliana',
                                  'Selección natural',
                                  'Uso y desuso',
                                  'Variación continua',
                                  'Mutación espontánea'],
                 'correcta': 'C'},
                {'pregunta': 'El principio de que las modificaciones por uso '
                             'y desuso son heredables se llama:',
                 'alternativas': ['Teoría sintética',
                                  'Selección natural',
                                  'Variación discontinua',
                                  'Mutacionismo',
                                  'Herencia de los caracteres adquiridos'],
                 'correcta': 'E'},
                {'pregunta': 'Lamarck ilustró su teoría con el ejemplo '
                             'clásico de:',
                 'alternativas': ['El color de la polilla',
                                  'La resistencia bacteriana',
                                  'Las alas del murciélago',
                                  'El cuello de la jirafa',
                                  'El pico del pinzón'],
                 'correcta': 'D'},
                {'pregunta': 'El fundador de la teoría de la evolución por '
                             'selección natural es:',
                 'alternativas': ['Lamarck',
                                  'Charles Darwin',
                                  'De Vries',
                                  'Bonnet',
                                  'Mendel'],
                 'correcta': 'B'},
                {'pregunta': 'Darwin publicó su obra principal, «El origen '
                             'de las especies», en el año:',
                 'alternativas': ['1809', '1937', '1859', '1889', '1758'],
                 'correcta': 'C'},
                {'pregunta': 'El biólogo que llegó a conclusiones similares '
                             'a Darwin de forma independiente fue:',
                 'alternativas': ['Lamarck',
                                  'Dobzhansky',
                                  'De Vries',
                                  'Mendel',
                                  'Alfred Russel Wallace'],
                 'correcta': 'E'},
                {'pregunta': 'Los cuatro conceptos centrales de la selección '
                             'natural son variación, sobreproducción, lucha '
                             'por la existencia y:',
                 'alternativas': ['Herencia adquirida',
                                  'Mutación',
                                  'Selección natural',
                                  'Uso y desuso',
                                  'Catastrofismo'],
                 'correcta': 'C'},
                {'pregunta': 'El concepto que sostiene que todos los '
                             'miembros de una especie difieren entre sí se '
                             'llama:',
                 'alternativas': ['Selección natural',
                                  'Sobreproducción',
                                  'Herencia',
                                  'Mutación',
                                  'Variación'],
                 'correcta': 'E'},
                {'pregunta': 'El mecanismo que incrementa las probabilidades '
                             'de que algunos vástagos sobrevivan se llama:',
                 'alternativas': ['Mutación',
                                  'Variación',
                                  'Adaptación exclusiva',
                                  'Sobreproducción',
                                  'Selección natural'],
                 'correcta': 'D'},
                {'pregunta': 'Según la selección natural, los individuos '
                             'mejor adaptados:',
                 'alternativas': ['Sobreviven y transmiten sus '
                                  'características',
                                  'Son eliminados por competencia',
                                  'Desaparecen primero',
                                  'No se reproducen nunca',
                                  'No tienen ventaja alguna'],
                 'correcta': 'A'},
                {'pregunta': 'El botánico que publicó «Pangénesis '
                             'intracelular» en 1889 fue:',
                 'alternativas': ['Darwin',
                                  'Wallace',
                                  'Lamarck',
                                  'Hugo De Vries',
                                  'Dobzhansky'],
                 'correcta': 'D'},
                {'pregunta': 'De Vries reemplazó la noción de variación '
                             'continua por la de:',
                 'alternativas': ['Variación discontinua o mutación',
                                  'Uso y desuso',
                                  'Selección natural',
                                  'Catastrofismo',
                                  'Herencia de caracteres adquiridos'],
                 'correcta': 'A'},
                {'pregunta': 'Una mutación se define como la aparición '
                             'repentina de una variante en:',
                 'alternativas': ['Un ecosistema',
                                  'Una especie entera',
                                  'Un organismo completo',
                                  'Una población completa',
                                  'Un gen particular o grupo de genes'],
                 'correcta': 'E'},
                {'pregunta': 'La Teoría Sintética de la evolución fue dada a '
                             'conocer por:',
                 'alternativas': ['Wallace',
                                  'De Vries',
                                  'Darwin',
                                  'Theodosius Dobzhansky',
                                  'Lamarck'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría Sintética combina la selección '
                             'natural con las leyes de la herencia de Mendel '
                             'y:',
                 'alternativas': ['El catastrofismo',
                                  'La teoría del big bang',
                                  'El mutacionismo',
                                  'El transformismo puro',
                                  'La teoría celular'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las principales teorías del origen de la '
                             'vida figuran el creacionismo, la generación '
                             'espontánea, la biogénesis y:',
                 'alternativas': ['La selección natural',
                                  'El transformismo',
                                  'La herencia adquirida',
                                  'El mutacionismo',
                                  'La panspermia'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría que sostenía que la vida surgía de '
                             'materia inerte sin reproducción se llama:',
                 'alternativas': ['Quimiosíntesis',
                                  'Generación espontánea o abiogénesis',
                                  'Biogénesis',
                                  'Panspermia',
                                  'Selección natural'],
                 'correcta': 'B'},
                {'pregunta': 'El científico que en el siglo XVII demostró '
                             'con frascos de carne que la vida no surge de '
                             'materia inerte fue:',
                 'alternativas': ['Spallanzani',
                                  'Francisco Redi',
                                  'Needham',
                                  'Oparin',
                                  'Pasteur'],
                 'correcta': 'B'},
                {'pregunta': 'El inglés que en 1745 defendió la generación '
                             'espontánea con un caldo mal sellado fue:',
                 'alternativas': ['Spallanzani',
                                  'John Needham',
                                  'Haldane',
                                  'Pasteur',
                                  'Redi'],
                 'correcta': 'B'},
                {'pregunta': 'El italiano que refutó a Needham sellando bien '
                             'los frascos fue:',
                 'alternativas': ['Redi',
                                  'Miller',
                                  'Oparin',
                                  'Lázaro Spallanzani',
                                  'Pasteur'],
                 'correcta': 'D'},
                {'pregunta': 'El científico que puso fin definitivo a la '
                             'generación espontánea con matraces de cuello '
                             'de cisne fue:',
                 'alternativas': ['Needham',
                                  'Spallanzani',
                                  'Haldane',
                                  'Louis Pasteur',
                                  'Redi'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la panspermia fue propuesta en '
                             '1879 por:',
                 'alternativas': ['Herman Von Helmholtz',
                                  'Svante Arrhenius',
                                  'Haldane',
                                  'Pasteur',
                                  'Oparin'],
                 'correcta': 'A'},
                {'pregunta': 'El químico sueco que popularizó la panspermia '
                             'en 1908 fue:',
                 'alternativas': ['Von Helmholtz',
                                  'Redi',
                                  'Miller',
                                  'Oparin',
                                  'Svante Arrhenius'],
                 'correcta': 'E'},
                {'pregunta': 'Según la panspermia, la vida se originó en el '
                             'espacio y llegó a la Tierra mediante:',
                 'alternativas': ['Rayos cósmicos',
                                  'Corrientes marinas',
                                  'Meteoritos',
                                  'Ondas de radio',
                                  'Explosiones solares'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría quimiosintética fue planteada en '
                             '1921 por el bioquímico ruso:',
                 'alternativas': ['Stanley Miller',
                                  'John Haldane',
                                  'Alexander Oparin',
                                  'Charles Darwin',
                                  'Louis Pasteur'],
                 'correcta': 'C'},
                {'pregunta': 'Según Oparin, la atmósfera primitiva era rica '
                             'en metano, amoniaco, CO2 y agua, pero pobre '
                             'en:',
                 'alternativas': ['Oxígeno',
                                  'Nitrógeno',
                                  'Carbono',
                                  'Azufre',
                                  'Hidrógeno'],
                 'correcta': 'A'},
                {'pregunta': 'Oparin propuso que las macromoléculas formaban '
                             'agregados llamados:',
                 'alternativas': ['Coacervados',
                                  'Ribosomas',
                                  'Plásmidos',
                                  'Cigotos',
                                  'Gametos'],
                 'correcta': 'A'},
                {'pregunta': 'John Haldane, en 1924, habló de una:',
                 'alternativas': ['Selección artificial',
                                  'Sopa primigenia',
                                  'Mutación espontánea masiva',
                                  'Generación espontánea directa',
                                  'Panspermia dirigida'],
                 'correcta': 'B'},
                {'pregunta': 'El experimento clave que simuló la atmósfera '
                             'primitiva en laboratorio fue realizado en 1953 '
                             'por:',
                 'alternativas': ['Redi y Spallanzani',
                                  'Darwin y Wallace',
                                  'Stanley Miller y Harold Urey',
                                  'Pasteur y Needham',
                                  'Oparin y Haldane'],
                 'correcta': 'C'},
                {'pregunta': 'El experimento de Miller y Urey usó una mezcla '
                             'de hidrógeno, vapor de agua, amoniaco y:',
                 'alternativas': ['Oxígeno',
                                  'Nitrógeno puro',
                                  'Metano',
                                  'Ozono',
                                  'Dióxido de azufre'],
                 'correcta': 'C'},
                {'pregunta': 'El experimento de Miller y Urey produjo, entre '
                             'otros compuestos, aminoácidos como:',
                 'alternativas': ['Solo proteínas complejas',
                                  'Solo ADN completo',
                                  'Solo agua y sal',
                                  'Ácido glutámico y glicina',
                                  'Solo minerales'],
                 'correcta': 'D'},
                {'pregunta': 'Una conclusión clave del experimento de Miller '
                             'y Urey fue que sin oxígeno libre se formaron:',
                 'alternativas': ['Compuestos orgánicos',
                                  'Solo minerales',
                                  'Solo gases inertes',
                                  'Ninguna sustancia nueva',
                                  'Solo agua'],
                 'correcta': 'A'},
                {'pregunta': 'Con presencia de oxígeno en el experimento de '
                             'Miller y Urey, solo se produjeron reacciones '
                             'de:',
                 'alternativas': ['Fotosíntesis',
                                  'Reducción exclusiva',
                                  'Oxidación',
                                  'Síntesis orgánica',
                                  'Fermentación'],
                 'correcta': 'C'}]},
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
                {'titulo': '13.8 FUNCIONES DE LOS ECOSISTEMAS: SUCESIÓN '
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
                {'titulo': '13.9 ECOSISTEMAS DEL PERÚ',
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
                           'Corriente Peruana, o Corriente de {Humboldt}.']},
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
                 'alternativas': ['Genos', 'Zoon', 'Physis', 'Logos', 'Bios'],
                 'correcta': 'D'},
                {'pregunta': '«Oikos» en griego significa:',
                 'alternativas': ['Vida',
                                  'Ciencia',
                                  'Naturaleza',
                                  'Estudio',
                                  'Casa'],
                 'correcta': 'E'},
                {'pregunta': 'El primer estudioso de las interacciones entre '
                             'seres vivos y ambiente fue:',
                 'alternativas': ['Aristóteles',
                                  'Darwin',
                                  'Linneo',
                                  'Haeckel',
                                  'Teofrasto'],
                 'correcta': 'E'},
                {'pregunta': 'El término «Ecología» fue establecido '
                             'formalmente por:',
                 'alternativas': ['Alfred Wallace',
                                  'Ernest Haeckel',
                                  'Charles Darwin',
                                  'Gregor Mendel',
                                  'Teofrasto'],
                 'correcta': 'B'},
                {'pregunta': 'Ernest Haeckel estableció el término '
                             '«Ecología» en el año:',
                 'alternativas': ['1859', '1869', '1937', '1789', '1809'],
                 'correcta': 'B'},
                {'pregunta': 'Haeckel definió la ecología como el estudio de '
                             'las relaciones de los organismos con su '
                             'ambiente:',
                 'alternativas': ['Orgánico e inorgánico',
                                  'Solo inorgánico',
                                  'Solo orgánico',
                                  'Solo social',
                                  'Solo económico'],
                 'correcta': 'A'},
                {'pregunta': 'La ecología estudia principalmente:',
                 'alternativas': ['Solo el clima',
                                  'La biosfera',
                                  'Solo los océanos',
                                  'La atmósfera exclusivamente',
                                  'Solo la litósfera'],
                 'correcta': 'B'},
                {'pregunta': 'El activismo de la ecología, como movimiento '
                             'cívico, se llama:',
                 'alternativas': ['Conservacionismo exclusivo',
                                  'Sostenibilismo',
                                  'Ecologismo',
                                  'Ambientalismo exclusivo',
                                  'Naturalismo exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El ecologismo tecnicista tiene como objetivo:',
                 'alternativas': ['Proteger la vida anímica',
                                  'Reducir la contaminación proponiendo '
                                  'energías alternativas',
                                  'Evitar la extinción de especies',
                                  'Estudiar la superpoblación',
                                  'Viajar a otros planetas'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo naturalista es una corriente '
                             'filosófica que busca:',
                 'alternativas': ['Estudiar recursos limitados',
                                  'Promover el amor espiritual',
                                  'Reducir la contaminación técnica',
                                  'Analizar la superpoblación',
                                  'Evitar la extinción de especies animales'],
                 'correcta': 'E'},
                {'pregunta': 'El ecologismo sociológico-político estudia, '
                             'entre otros temas, la superpoblación y:',
                 'alternativas': ['Solo la deforestación',
                                  'Solo la energía nuclear',
                                  'La extinción de especies exclusivamente',
                                  'Solo el reciclaje',
                                  'La hambruna en el mundo'],
                 'correcta': 'E'},
                {'pregunta': 'Los factores ambientales se clasifican en '
                             'bióticos y:',
                 'alternativas': ['Antrópicos exclusivos',
                                  'Abióticos',
                                  'Naturales exclusivos',
                                  'Ecológicos',
                                  'Orgánicos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores bióticos corresponden a:',
                 'alternativas': ['Solo el clima',
                                  'Solo el agua',
                                  'El ambiente físico no viviente',
                                  'Todos los seres vivos',
                                  'Solo el suelo'],
                 'correcta': 'D'},
                {'pregunta': 'La concentración de individuos de una especie '
                             'en un área geográfica se llama:',
                 'alternativas': ['Nicho ecológico',
                                  'Densidad poblacional',
                                  'Bioma',
                                  'Hábitat exclusivo',
                                  'Biomasa'],
                 'correcta': 'B'},
                {'pregunta': 'Las relaciones entre individuos de la misma '
                             'especie se llaman relaciones:',
                 'alternativas': ['Intraespecíficas',
                                  'Tróficas exclusivas',
                                  'Simbióticas exclusivas',
                                  'Interespecíficas',
                                  'Ecológicas generales'],
                 'correcta': 'A'},
                {'pregunta': 'Las relaciones entre individuos de especies '
                             'distintas se llaman relaciones:',
                 'alternativas': ['Poblacionales exclusivas',
                                  'Interespecíficas',
                                  'Bióticas generales',
                                  'Abióticas',
                                  'Intraespecíficas'],
                 'correcta': 'B'},
                {'pregunta': 'El ambiente también se suele denominar '
                             'entorno, medio ambiente o:',
                 'alternativas': ['Bioma exclusivo',
                                  'Ecosistema exclusivo',
                                  'Naturaleza',
                                  'Nicho',
                                  'Hábitat exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'En el ambiente se agrupan seres en dos '
                             'categorías: vivos y:',
                 'alternativas': ['Domesticados',
                                  'Extintos',
                                  'Fósiles',
                                  'Migratorios',
                                  'No vivos'],
                 'correcta': 'E'},
                {'pregunta': 'Debido a que los humanos forman parte de la '
                             'red de vida de la Tierra, sus actividades '
                             'económicas y políticas tienen:',
                 'alternativas': ['Solo implicaciones sociales',
                                  'Profundas implicaciones ecológicas',
                                  'Solo implicaciones económicas',
                                  'Ninguna implicación ecológica',
                                  'Efectos neutros'],
                 'correcta': 'B'},
                {'pregunta': 'El ecologismo surge como una nueva forma de '
                             'hacer política centrada en:',
                 'alternativas': ['El desarrollo sostenible',
                                  'El comercio internacional',
                                  'El crecimiento económico ilimitado',
                                  'La industrialización acelerada',
                                  'La explotación de recursos'],
                 'correcta': 'A'},
                {'pregunta': 'El término «ecosistema» fue acuñado por:',
                 'alternativas': ['Charles Darwin',
                                  'Arthur Tansley',
                                  'Antonio Brack',
                                  'Ernest Haeckel',
                                  'Odum'],
                 'correcta': 'B'},
                {'pregunta': 'Un ecosistema es considerado un sistema:',
                 'alternativas': ['Cerrado',
                                  'Sin energía',
                                  'Estático',
                                  'Abierto',
                                  'Aislado'],
                 'correcta': 'D'},
                {'pregunta': 'El ecosistema más grande que se puede concebir '
                             'es:',
                 'alternativas': ['Un bioma',
                                  'Un biotopo',
                                  'La biosfera',
                                  'Una ecorregión',
                                  'Una biocenosis'],
                 'correcta': 'C'},
                {'pregunta': 'La comunidad biótica formada por todos los '
                             'organismos vivos de un lugar se llama:',
                 'alternativas': ['Biotopo',
                                  'Biocenosis',
                                  'Bioma',
                                  'Nicho ecológico',
                                  'Hábitat'],
                 'correcta': 'B'},
                {'pregunta': 'El espacio físico donde vive una biocenosis, '
                             'caracterizado por factores abióticos, se '
                             'llama:',
                 'alternativas': ['Hábitat',
                                  'Nicho',
                                  'Biotopo',
                                  'Ecorregión',
                                  'Biocenosis'],
                 'correcta': 'C'},
                {'pregunta': 'El lugar donde un organismo encuentra '
                             'condiciones favorables para vivir se llama:',
                 'alternativas': ['Hábitat',
                                  'Nicho ecológico',
                                  'Bioma',
                                  'Biotopo',
                                  'Biocenosis'],
                 'correcta': 'A'},
                {'pregunta': 'Las necesidades especiales de una población '
                             'respecto a alimento, luz y humedad se llaman:',
                 'alternativas': ['Ecorregión',
                                  'Biotopo',
                                  'Nicho ecológico',
                                  'Biocenosis',
                                  'Hábitat'],
                 'correcta': 'C'},
                {'pregunta': 'Dos organismos que viven en el mismo lugar '
                             'nunca comparten el mismo:',
                 'alternativas': ['Bioma',
                                  'Nicho ecológico',
                                  'Biotopo',
                                  'Clima',
                                  'Hábitat'],
                 'correcta': 'B'},
                {'pregunta': 'La fuente de energía de la mayoría de los '
                             'ecosistemas es:',
                 'alternativas': ['El aire',
                                  'El agua',
                                  'La luz solar',
                                  'Los minerales',
                                  'El suelo'],
                 'correcta': 'C'},
                {'pregunta': 'Las relaciones que se dan entre individuos de '
                             'la misma especie se llaman relaciones:',
                 'alternativas': ['Predatorias exclusivas',
                                  'Interespecíficas',
                                  'Simbióticas exclusivas',
                                  'Intraespecíficas',
                                  'Tróficas exclusivas'],
                 'correcta': 'D'},
                {'pregunta': 'Las relaciones que se dan entre individuos de '
                             'especies diferentes se llaman relaciones:',
                 'alternativas': ['De colmena exclusivas',
                                  'Intraespecíficas',
                                  'Interespecíficas',
                                  'Homotípicas',
                                  'Familiares exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'Las agrupaciones sin vínculos ni trascendencia '
                             'ecológica, como mariposas en flores, se '
                             'llaman:',
                 'alternativas': ['Familias',
                                  'Agrupaciones casuales o agregaciones',
                                  'Sociedades',
                                  'Colmenas',
                                  'Clanes'],
                 'correcta': 'B'},
                {'pregunta': 'Las familias con diferenciación morfológica en '
                             'reinas, zánganos y obreras se llaman:',
                 'alternativas': ['Colmenas',
                                  'Agregaciones',
                                  'Clanes',
                                  'Sociedades simples',
                                  'Manadas'],
                 'correcta': 'A'},
                {'pregunta': 'La agrupación de individuos puede producir '
                             'tres efectos: cooperación, interferencia y:',
                 'alternativas': ['Simbiosis',
                                  'Comensalismo',
                                  'Competencia',
                                  'Parasitismo',
                                  'Depredación'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando dos organismos viven juntos y se '
                             'toleran sin hacerse daño, la relación se '
                             'llama:',
                 'alternativas': ['Parasitismo',
                                  'Epifitismo',
                                  'Depredación',
                                  'Sinequia',
                                  'Competencia'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando una planta crece sobre otra usándola de '
                             'soporte sin dañarla, ocurre:',
                 'alternativas': ['Epifitismo',
                                  'Depredación',
                                  'Parasitismo',
                                  'Sinequia',
                                  'Mutualismo exclusivo'],
                 'correcta': 'A'},
                {'pregunta': 'La secuencia de cambios que experimenta un '
                             'ecosistema a través del tiempo se llama:',
                 'alternativas': ['Nicho ecológico',
                                  'Comunidad clímax',
                                  'Biocenosis',
                                  'Bioma',
                                  'Sucesión ecológica'],
                 'correcta': 'E'},
                {'pregunta': 'La máxima expresión armónica de las '
                             'poblaciones de un ecosistema se llama:',
                 'alternativas': ['Biotopo',
                                  'Ecorregión',
                                  'Sucesión primaria',
                                  'Nicho ecológico',
                                  'Comunidad clímax'],
                 'correcta': 'E'},
                {'pregunta': 'La sucesión que comienza en un hábitat sin '
                             'suelo, como una isla volcánica, se llama '
                             'sucesión:',
                 'alternativas': ['Terciaria',
                                  'Clímax',
                                  'Secundaria',
                                  'Primaria',
                                  'Antrópica'],
                 'correcta': 'D'},
                {'pregunta': 'Los organismos pioneros típicos de la sucesión '
                             'primaria son:',
                 'alternativas': ['Mamíferos',
                                  'Árboles grandes',
                                  'Musgos y líquenes',
                                  'Peces',
                                  'Aves'],
                 'correcta': 'C'},
                {'pregunta': 'La sucesión que comienza donde ya existía '
                             'suelo, tras una perturbación, se llama '
                             'sucesión:',
                 'alternativas': ['Secundaria',
                                  'Terciaria',
                                  'Clímax exclusiva',
                                  'Primaria',
                                  'Ninguna de las anteriores'],
                 'correcta': 'A'},
                {'pregunta': 'Las zonas de vida de Holdridge se definen en '
                             'función de biotemperatura, precipitación, '
                             'humedad y:',
                 'alternativas': ['Presión atmosférica',
                                  'Longitud',
                                  'Latitud',
                                  'Salinidad',
                                  'Altitud'],
                 'correcta': 'E'},
                {'pregunta': 'Según Antonio Brack, el Perú tiene un número '
                             'de ecorregiones igual a:',
                 'alternativas': ['15', '8', '5', '11', '20'],
                 'correcta': 'D'},
                {'pregunta': 'La primera ecorregión del Perú, según Brack, '
                             'es:',
                 'alternativas': ['La selva alta',
                                  'La puna',
                                  'El mar tropical',
                                  'El mar frío de la Corriente Peruana',
                                  'El desierto costero'],
                 'correcta': 'D'}]},
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
                {'titulo': '14.4 NIVELES TRÓFICOS',
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
                {'titulo': '14.5 CADENAS, REDES Y PIRÁMIDES TRÓFICAS',
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
                {'titulo': '14.6 CICLOS BIOGEOQUÍMICOS: CONCEPTO Y '
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
                {'titulo': '14.7 EL CICLO DEL CARBONO',
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
                {'titulo': '14.8 EL CICLO DEL NITRÓGENO',
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
                 'alternativas': ['Quarks',
                                  'Fotones',
                                  'Neutrones',
                                  'Electrones',
                                  'Iones'],
                 'correcta': 'B'},
                {'pregunta': 'La energía en movimiento, como la energía '
                             'mecánica o el calor, se llama energía:',
                 'alternativas': ['Potencial',
                                  'Cinética',
                                  'Radiante exclusiva',
                                  'Nuclear exclusiva',
                                  'Química exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La energía almacenada, disponible para llevar '
                             'a cabo trabajo, se llama energía:',
                 'alternativas': ['Potencial',
                                  'Lumínica exclusiva',
                                  'Mecánica exclusiva',
                                  'Térmica exclusiva',
                                  'Cinética'],
                 'correcta': 'A'},
                {'pregunta': 'Los ecosistemas son sistemas '
                             'termodinámicamente:',
                 'alternativas': ['Neutros',
                                  'Abiertos',
                                  'Estáticos',
                                  'Cerrados',
                                  'Aislados'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ley de la termodinámica también se '
                             'conoce como el principio de:',
                 'alternativas': ['El diezmo ecológico',
                                  'La herencia',
                                  'La conservación de la energía',
                                  'La selección natural',
                                  'La entropía'],
                 'correcta': 'C'},
                {'pregunta': 'La primera ley de la termodinámica fue '
                             'postulada en 1841 por:',
                 'alternativas': ['Haeckel',
                                  'R. Mayer',
                                  'Darwin',
                                  'Dobzhansky',
                                  'Mendel'],
                 'correcta': 'B'},
                {'pregunta': 'Según la primera ley de la termodinámica, la '
                             'energía:',
                 'alternativas': ['Se crea constantemente',
                                  'Desaparece con el tiempo',
                                  'No se crea ni se destruye, solo se '
                                  'transforma',
                                  'Se multiplica en cada transformación',
                                  'Se pierde totalmente en cada ciclo'],
                 'correcta': 'C'},
                {'pregunta': 'La segunda ley de la termodinámica también se '
                             'conoce como ley de:',
                 'alternativas': ['La herencia',
                                  'La entropía o degradación de la energía',
                                  'El diezmo ecológico',
                                  'La selección natural',
                                  'La conservación de la energía'],
                 'correcta': 'B'},
                {'pregunta': 'Según la segunda ley de la termodinámica, al '
                             'transformarse la energía:',
                 'alternativas': ['Parte se degrada en una forma no '
                                  'trasladable',
                                  'Aumenta su cantidad total',
                                  'Se transforma en materia',
                                  'Desaparece por completo',
                                  'Se conserva completamente aprovechable'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando la energía se transfiere de un '
                             'organismo a otro en la cadena alimenticia, '
                             'gran parte se degrada en forma de:',
                 'alternativas': ['Calor',
                                  'Sonido',
                                  'Electricidad',
                                  'Luz',
                                  'Materia sólida'],
                 'correcta': 'A'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, al pasar de '
                             'un nivel trófico a otro se transfiere:',
                 'alternativas': ['El 100% de la energía',
                                  'El 50% de la energía',
                                  'El 1% de la energía',
                                  'El 10% de la energía',
                                  'El 90% de la energía'],
                 'correcta': 'D'},
                {'pregunta': 'Según la Ley del Diezmo Ecológico, los '
                             'organismos usan en su propio metabolismo:',
                 'alternativas': ['El 90% de la energía capturada',
                                  'Ninguna energía',
                                  'El 50% de la energía capturada',
                                  'Toda la energía capturada',
                                  'El 10% de la energía capturada'],
                 'correcta': 'A'},
                {'pregunta': 'Un vegetal aprovecha para sus funciones de '
                             'supervivencia aproximadamente:',
                 'alternativas': ['100% de la energía solar',
                                  '90% de la energía solar fijada',
                                  '1% de la energía solar',
                                  '10% de la energía solar fijada',
                                  '50% de la energía solar fijada'],
                 'correcta': 'B'},
                {'pregunta': 'Un herbívoro que consume un vegetal solo puede '
                             'aprovechar de la energía fijada por este:',
                 'alternativas': ['El 50%',
                                  'El 100%',
                                  'El 90%',
                                  'El 10%',
                                  'El 1%'],
                 'correcta': 'D'},
                {'pregunta': 'Un carnívoro que consume a un herbívoro solo '
                             'puede aprovechar de la energía que este '
                             'recibió:',
                 'alternativas': ['El 90%',
                                  'El 50%',
                                  'El 100%',
                                  'El 10%',
                                  'El 5%'],
                 'correcta': 'D'},
                {'pregunta': 'El porcentaje aproximado de la energía '
                             'disponible en la Tierra que proviene del sol '
                             'es:',
                 'alternativas': ['75%', '10%', '99,98%', '50%', '25%'],
                 'correcta': 'C'},
                {'pregunta': 'Además del sol, otras fuentes de energía '
                             'terrestre incluyen las mareas, la energía '
                             'nuclear, la termal y la:',
                 'alternativas': ['Química exclusiva',
                                  'Radiante exclusiva de origen solar',
                                  'Potencial exclusiva',
                                  'Cinética exclusiva',
                                  'Gravitacional'],
                 'correcta': 'E'},
                {'pregunta': 'La radiación solar que llega a la superficie '
                             'terrestre varía según la latitud, la altura, '
                             'la orografía y:',
                 'alternativas': ['El color del suelo',
                                  'La velocidad de rotación',
                                  'El tipo de roca',
                                  'La profundidad marina',
                                  'La nubosidad'],
                 'correcta': 'E'},
                {'pregunta': 'La historia de la energía en un ecosistema '
                             'está en gran parte relacionada con la historia '
                             'de:',
                 'alternativas': ['El carbono',
                                  'El nitrógeno',
                                  'El azufre',
                                  'El oxígeno puro',
                                  'El fósforo'],
                 'correcta': 'A'},
                {'pregunta': 'La energía almacenada en los enlaces químicos '
                             'de los carbohidratos proviene originalmente '
                             'de:',
                 'alternativas': ['La respiración celular',
                                  'La descomposición',
                                  'La glucólisis',
                                  'La quimiosíntesis exclusiva',
                                  'La fotosíntesis'],
                 'correcta': 'E'},
                {'pregunta': 'El primer nivel trófico está formado por:',
                 'alternativas': ['Los carroñeros',
                                  'Los productores u organismos autótrofos',
                                  'Los descomponedores',
                                  'Los carnívoros',
                                  'Los omnívoros'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo nivel trófico está formado por:',
                 'alternativas': ['Los consumidores primarios o herbívoros',
                                  'Los productores',
                                  'Los carnívoros',
                                  'Los carroñeros',
                                  'Los descomponedores'],
                 'correcta': 'A'},
                {'pregunta': 'El tercer nivel trófico está formado por los '
                             'consumidores secundarios, también llamados:',
                 'alternativas': ['Omnívoros exclusivos',
                                  'Depredadores o carnívoros',
                                  'Herbívoros',
                                  'Productores',
                                  'Descomponedores'],
                 'correcta': 'B'},
                {'pregunta': 'El animal del que se alimenta un depredador se '
                             'llama su:',
                 'alternativas': ['Parásito',
                                  'Huésped',
                                  'Hospedero',
                                  'Simbionte',
                                  'Presa'],
                 'correcta': 'E'},
                {'pregunta': 'Los organismos que se alimentan tanto de '
                             'plantas como de carne se llaman:',
                 'alternativas': ['Carnívoros puros',
                                  'Descomponedores',
                                  'Herbívoros',
                                  'Detritívoros exclusivos',
                                  'Omnívoros'],
                 'correcta': 'E'},
                {'pregunta': 'Los hongos y bacterias que desintegran materia '
                             'orgánica muerta se llaman:',
                 'alternativas': ['Productores',
                                  'Descomponedores',
                                  'Consumidores primarios',
                                  'Consumidores secundarios',
                                  'Herbívoros'],
                 'correcta': 'B'},
                {'pregunta': 'Una cadena alimenticia muestra cómo fluye la '
                             'energía de un organismo a otro a través de:',
                 'alternativas': ['Solo los productores',
                                  'Ningún nivel definido',
                                  'Solo los depredadores',
                                  'Un solo nivel trófico',
                                  'Cada nivel trófico'],
                 'correcta': 'E'},
                {'pregunta': 'En ecosistemas marinos, las cadenas tróficas '
                             'pueden llegar hasta:',
                 'alternativas': ['6 eslabones',
                                  '2 eslabones',
                                  '10 eslabones',
                                  '20 eslabones',
                                  '1 eslabón'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de todas las cadenas alimenticias '
                             'interconectadas de una comunidad forma:',
                 'alternativas': ['Una pirámide trófica',
                                  'Una red trófica',
                                  'Un bioma',
                                  'Una ecorregión',
                                  'Un nicho ecológico'],
                 'correcta': 'B'},
                {'pregunta': 'En las pirámides tróficas, los productores se '
                             'ubican en:',
                 'alternativas': ['El centro',
                                  'La base',
                                  'La cúspide',
                                  'No aparecen',
                                  'Fuera de la pirámide'],
                 'correcta': 'B'},
                {'pregunta': 'Los ciclos biogeoquímicos se definen como el '
                             'movimiento circular de elementos entre:',
                 'alternativas': ['Solo la atmósfera',
                                  'Solo los organismos',
                                  'El ambiente y los organismos',
                                  'Solo el agua',
                                  'Solo el suelo'],
                 'correcta': 'C'},
                {'pregunta': 'Los ciclos biogeoquímicos involucran '
                             'componentes geológicos, biológicos y:',
                 'alternativas': ['Sociales',
                                  'Químicos',
                                  'Culturales',
                                  'Económicos',
                                  'Políticos'],
                 'correcta': 'B'},
                {'pregunta': 'Los componentes geológicos de los ciclos '
                             'biogeoquímicos son atmósfera, litósfera e:',
                 'alternativas': ['Exósfera',
                                  'Ionósfera',
                                  'Hidrósfera',
                                  'Estratósfera',
                                  'Termósfera'],
                 'correcta': 'C'},
                {'pregunta': 'Los ciclos que tienen a la atmósfera como '
                             'principal reservorio se llaman ciclos:',
                 'alternativas': ['Sedimentarios',
                                  'Minerales exclusivos',
                                  'Orgánicos exclusivos',
                                  'Gaseosos',
                                  'Hídricos exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los ciclos que tienen a las rocas '
                             'sedimentarias como reservorio, y son más '
                             'lentos, se llaman ciclos:',
                 'alternativas': ['Atmosféricos',
                                  'Sedimentarios',
                                  'Rápidos',
                                  'Gaseosos',
                                  'Hídricos'],
                 'correcta': 'B'},
                {'pregunta': 'Los dos procesos básicos que participan en el '
                             'ciclo del carbono son fotosíntesis y:',
                 'alternativas': ['Digestión',
                                  'Respiración celular',
                                  'Fermentación',
                                  'Transcripción',
                                  'Excreción'],
                 'correcta': 'B'},
                {'pregunta': 'La mayor parte del carbono fijado anualmente '
                             'por fotosíntesis, un 90%, es fijado por:',
                 'alternativas': ['Las algas oceánicas',
                                  'Los animales',
                                  'Los hongos',
                                  'Los bosques',
                                  'Las bacterias del suelo'],
                 'correcta': 'A'},
                {'pregunta': 'Los moluscos combinan CO2 disuelto con calcio '
                             'para formar:',
                 'alternativas': ['Carbonato de calcio en sus conchas',
                                  'Dióxido de carbono puro',
                                  'Metano',
                                  'Bicarbonato de sodio',
                                  'Ácido carbónico'],
                 'correcta': 'A'},
                {'pregunta': 'Los combustibles fósiles, como el carbón y el '
                             'petróleo, se forman de restos orgánicos '
                             'transformados por:',
                 'alternativas': ['Fotosíntesis directa',
                                  'Radiación solar directa',
                                  'Alta temperatura y presión durante '
                                  'millones de años',
                                  'Reacciones químicas instantáneas',
                                  'Congelación'],
                 'correcta': 'C'},
                {'pregunta': 'La atmósfera está formada por gas nitrógeno '
                             'libre en una proporción aproximada de:',
                 'alternativas': ['21%', '95%', '78%', '10%', '50%'],
                 'correcta': 'C'},
                {'pregunta': 'Las plantas y animales no pueden usar '
                             'directamente el nitrógeno atmosférico porque '
                             'debe convertirse primero en:',
                 'alternativas': ['Metano',
                                  'Dióxido de carbono',
                                  'Ozono',
                                  'Oxígeno',
                                  'Nitratos'],
                 'correcta': 'E'},
                {'pregunta': 'El ciclo del nitrógeno incluye los procesos de '
                             'fijación, amonificación, nitrificación y:',
                 'alternativas': ['Desnitrificación',
                                  'Fotosíntesis',
                                  'Respiración',
                                  'Glucólisis',
                                  'Fermentación'],
                 'correcta': 'A'},
                {'pregunta': 'En la fijación de nitrógeno, las bacterias '
                             'convierten el N2 atmosférico en:',
                 'alternativas': ['Oxígeno',
                                  'Nitratos directamente',
                                  'Dióxido de carbono',
                                  'Amoníaco (NH3)',
                                  'Ácido sulfúrico'],
                 'correcta': 'D'},
                {'pregunta': 'Las bacterias fijadoras de nitrógeno viven en '
                             'nódulos de las raíces de plantas llamadas:',
                 'alternativas': ['Coníferas',
                                  'Gramíneas',
                                  'Helechos',
                                  'Leguminosas, como el frijol',
                                  'Cactáceas'],
                 'correcta': 'D'}]},
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
                {'titulo': '15.5 DETERIORO DE LA FLORA Y FAUNA',
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
                {'titulo': '15.6 TIPOS DE DETERIORO',
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
                           '{veda}.']},
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
                                  'Cumbre de París',
                                  'Protocolo de Montreal',
                                  'Cumbre de la Tierra',
                                  'Acuerdo de Copenhague'],
                 'correcta': 'D'},
                {'pregunta': 'La Cumbre de la Tierra, donde se celebró el '
                             'CDB, se llevó a cabo en:',
                 'alternativas': ['Lima, Perú',
                                  'Ginebra, Suiza',
                                  'Nueva York, EE.UU.',
                                  'Nagoya, Japón',
                                  'Río de Janeiro, Brasil'],
                 'correcta': 'E'},
                {'pregunta': 'El Convenio sobre la Diversidad Biológica se '
                             'celebró en el año:',
                 'alternativas': ['1985', '1992', '2010', '1972', '2000'],
                 'correcta': 'B'},
                {'pregunta': 'El CDB define la diversidad biológica como la '
                             'variabilidad de:',
                 'alternativas': ['Solo especies animales',
                                  'Solo especies marinas',
                                  'Organismos vivos de cualquier fuente',
                                  'Solo especies vegetales',
                                  'Solo microorganismos'],
                 'correcta': 'C'},
                {'pregunta': 'Según el CDB, la conservación de la diversidad '
                             'biológica es interés:',
                 'alternativas': ['Solo científico',
                                  'Común de toda la humanidad',
                                  'Solo económico',
                                  'Exclusivo de los países desarrollados',
                                  'Solo de organismos ambientales'],
                 'correcta': 'B'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica 2011-2020 fue adoptado en:',
                 'alternativas': ['Ginebra',
                                  'París',
                                  'Río de Janeiro',
                                  'Nagoya, Japón',
                                  'Nueva York'],
                 'correcta': 'D'},
                {'pregunta': 'El Plan Estratégico para la Diversidad '
                             'Biológica fue adoptado en el año:',
                 'alternativas': ['2010', '1992', '2020', '2000', '1985'],
                 'correcta': 'A'},
                {'pregunta': 'Como parte del Plan Estratégico, se trazaron '
                             'las metas conocidas como:',
                 'alternativas': ['Metas de Kioto',
                                  'Metas de París',
                                  'Metas de Montreal',
                                  'Metas de Aichi',
                                  'Metas de Copenhague'],
                 'correcta': 'D'},
                {'pregunta': 'El Día Internacional de la Diversidad '
                             'Biológica se celebra el:',
                 'alternativas': ['22 de mayo',
                                  '1 de enero',
                                  '22 de abril',
                                  '5 de junio',
                                  '10 de diciembre'],
                 'correcta': 'A'},
                {'pregunta': 'La biodiversidad comprende tres componentes: '
                             'genética, de especies y de:',
                 'alternativas': ['Océanos',
                                  'Suelos',
                                  'Continentes',
                                  'Ecosistemas',
                                  'Climas'],
                 'correcta': 'D'},
                {'pregunta': 'La diversidad genética se refiere a las '
                             'diferencias en:',
                 'alternativas': ['El tipo de clima',
                                  'La ubicación geográfica',
                                  'La cantidad de ecosistemas',
                                  'El número de especies',
                                  'El material genético entre poblaciones e '
                                  'individuos'],
                 'correcta': 'E'},
                {'pregunta': 'La diversidad de especies se refiere al número '
                             'de especies diferentes presentes en:',
                 'alternativas': ['Solo un país',
                                  'Solo un continente',
                                  'Un área determinada',
                                  'Solo un océano',
                                  'Todo el planeta exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'La diversidad de especies tiene dos '
                             'componentes: la riqueza de especies y:',
                 'alternativas': ['El tipo de suelo',
                                  'La ubicación',
                                  'El tamaño del área',
                                  'Sus abundancias relativas',
                                  'El clima'],
                 'correcta': 'D'},
                {'pregunta': 'La diversidad de ecosistemas se refiere a la '
                             'variedad de:',
                 'alternativas': ['Climas exclusivamente',
                                  'Sistemas ecológicos en una región',
                                  'Especies individuales',
                                  'Recursos minerales',
                                  'Genes específicos'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú es reconocido como un centro mundial '
                             'de origen de recursos genéticos de plantas '
                             'como:',
                 'alternativas': ['El arroz y la soya',
                                  'El café y el cacao exclusivamente',
                                  'La vid y el olivo',
                                  'La papa, el maíz y el tomate',
                                  'El trigo y la cebada'],
                 'correcta': 'D'},
                {'pregunta': 'La riqueza genética del Perú está asociada con '
                             'la riqueza cultural desarrollada por:',
                 'alternativas': ['Colonizadores europeos',
                                  'Organismos internacionales',
                                  'Los pueblos indígenas',
                                  'Empresas multinacionales',
                                  'Científicos extranjeros'],
                 'correcta': 'C'},
                {'pregunta': 'La distribución global de la diversidad de '
                             'especies depende de gradientes latitudinales, '
                             'de altitud y de:',
                 'alternativas': ['Densidad urbana',
                                  'Población humana',
                                  'Comercio internacional',
                                  'Actividad industrial',
                                  'Precipitación'],
                 'correcta': 'E'},
                {'pregunta': 'La conservación de la biodiversidad está '
                             'íntimamente asociada con el uso de:',
                 'alternativas': ['Solo el comercio internacional',
                                  'Solo la tecnología',
                                  'Solo el capital financiero',
                                  'Solo la política exterior',
                                  'Los recursos naturales y la tierra'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando las actividades humanas se incrementan '
                             'por encima de cierto umbral, los efectos sobre '
                             'los sistemas naturales son:',
                 'alternativas': ['Siempre positivos',
                                  'Inexistentes',
                                  'Reversibles automáticamente',
                                  'Más significativos y prolongados',
                                  'Insignificantes'],
                 'correcta': 'D'},
                {'pregunta': 'Además de los tres componentes clásicos, en la '
                             'actualidad se reconoce también como componente '
                             'de la biodiversidad a la diversidad:',
                 'alternativas': ['Militar',
                                  'Política',
                                  'Religiosa',
                                  'Económica',
                                  'Cultural'],
                 'correcta': 'E'},
                {'pregunta': 'Los servicios que suministran bienes con valor '
                             'monetario directo, como alimentos y madera, se '
                             'llaman servicios de:',
                 'alternativas': ['Regulación',
                                  'Aprovisionamiento',
                                  'Apoyo',
                                  'Culturales',
                                  'Ninguno de los anteriores'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios que incluyen la regulación del '
                             'clima y la polinización se llaman servicios:',
                 'alternativas': ['Ninguno de los anteriores',
                                  'Reguladores',
                                  'De aprovisionamiento',
                                  'De apoyo',
                                  'Culturales'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios que incluyen valor espiritual, '
                             'recreación y ecoturismo se llaman servicios:',
                 'alternativas': ['Ninguno de los anteriores',
                                  'De aprovisionamiento',
                                  'De apoyo',
                                  'Reguladores',
                                  'Culturales'],
                 'correcta': 'E'},
                {'pregunta': 'Los servicios esenciales para el '
                             'funcionamiento del ecosistema, como la '
                             'formación de suelos, se llaman servicios de:',
                 'alternativas': ['Cultura',
                                  'Aprovisionamiento',
                                  'Apoyo o soporte',
                                  'Regulación',
                                  'Ninguno de los anteriores'],
                 'correcta': 'C'},
                {'pregunta': 'En el Perú, una de las actividades más '
                             'rentables relacionadas con la biodiversidad '
                             'es:',
                 'alternativas': ['La pesquería',
                                  'La minería exclusiva',
                                  'La banca',
                                  'La industria textil',
                                  'El comercio internacional'],
                 'correcta': 'A'},
                {'pregunta': 'La causa principal de extinción de especies en '
                             'la actualidad es:',
                 'alternativas': ['Las enfermedades exclusivas',
                                  'Los desastres naturales exclusivos',
                                  'La destrucción del hábitat por '
                                  'actividades humanas',
                                  'La competencia natural exclusiva',
                                  'El cambio de estaciones'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las causas de pérdida de biodiversidad '
                             'figuran el cambio de uso de suelo y:',
                 'alternativas': ['La conservación estricta',
                                  'El aumento de áreas protegidas',
                                  'El crecimiento de bosques',
                                  'La sobreexplotación de recursos bióticos',
                                  'La reforestación'],
                 'correcta': 'D'},
                {'pregunta': 'En la Amazonía peruana, el cambio de uso de '
                             'suelo se debe principalmente a monocultivos '
                             'extensivos y:',
                 'alternativas': ['La investigación científica',
                                  'La protección estatal',
                                  'La deforestación por tala y quema',
                                  'El turismo sostenible',
                                  'La reforestación'],
                 'correcta': 'C'},
                {'pregunta': 'Un peligro adicional para la biodiversidad es '
                             'la introducción de:',
                 'alternativas': ['Reservas comunales',
                                  'Áreas protegidas',
                                  'Organismos vivos modificados (OVM)',
                                  'Especies nativas',
                                  'Parques nacionales'],
                 'correcta': 'C'},
                {'pregunta': 'La flora y la fauna son recursos naturales:',
                 'alternativas': ['No renovables',
                                  'Inagotables sin límite',
                                  'Renovables',
                                  'Artificiales',
                                  'Inexistentes en el Perú'],
                 'correcta': 'C'},
                {'pregunta': 'La pérdida o reducción de la variabilidad '
                             'genética de una especie se llama:',
                 'alternativas': ['Especiación',
                                  'Deriva génica',
                                  'Erosión genética',
                                  'Mutación dirigida',
                                  'Selección natural'],
                 'correcta': 'C'},
                {'pregunta': 'Una causa de erosión genética es la '
                             'introducción de variedades exóticas en lugar '
                             'de:',
                 'alternativas': ['Variedades transgénicas',
                                  'Las variedades nativas o locales',
                                  'Variedades híbridas',
                                  'Ninguna variedad',
                                  'Variedades importadas'],
                 'correcta': 'B'},
                {'pregunta': 'La chinchilla es un ejemplo emblemático de '
                             'especie extinta en su hábitat andino debido a:',
                 'alternativas': ['El cambio climático exclusivo',
                                  'La sobreexplotación',
                                  'La migración voluntaria',
                                  'La competencia natural',
                                  'Una enfermedad viral'],
                 'correcta': 'B'},
                {'pregunta': 'El uso excesivo de biomasa se refiere a la '
                             'utilización insostenible de materia orgánica '
                             'de:',
                 'alternativas': ['Solo aire',
                                  'Solo minerales',
                                  'Solo agua',
                                  'Solo rocas',
                                  'Plantas y animales'],
                 'correcta': 'E'},
                {'pregunta': 'La extracción selectiva sin control afecta '
                             'especies de alta demanda comercial como el '
                             'cedro y:',
                 'alternativas': ['El sauce',
                                  'El pino',
                                  'La caoba',
                                  'El ciprés',
                                  'El eucalipto'],
                 'correcta': 'C'},
                {'pregunta': 'Entre la fauna peruana afectada por extracción '
                             'selectiva figuran la vicuña y:',
                 'alternativas': ['La tortuga charapa',
                                  'El ratón',
                                  'La rana común',
                                  'El gato doméstico',
                                  'La paloma común'],
                 'correcta': 'A'},
                {'pregunta': 'La pesca insostenible que no respeta las '
                             'épocas de veda se llama:',
                 'alternativas': ['Pesca sostenible',
                                  'Pesca deportiva',
                                  'Pesca artesanal',
                                  'Pesca no planificada',
                                  'Acuicultura'],
                 'correcta': 'D'},
                {'pregunta': 'Especies como la anchoveta, sardina y merluza '
                             'han reducido sus poblaciones debido a:',
                 'alternativas': ['Causas exclusivamente naturales',
                                  'La migración voluntaria',
                                  'El aumento de depredadores naturales',
                                  'Cambios genéticos espontáneos',
                                  'Actividades antrópicas como la pesca no '
                                  'planificada'],
                 'correcta': 'E'}]},
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
                {'titulo': '16.5 CONSERVACIÓN DEL MEDIO AMBIENTE',
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
                {'titulo': '16.6 FORESTACIÓN Y REFORESTACIÓN',
                 'items': ['La {forestación} es poblar con árboles áreas que '
                           'nunca o hace mucho tiempo tuvieron bosque.',
                           'La {reforestación} es repoblar con especies '
                           'arbóreas suelos que sí tuvieron cobertura '
                           'forestal antes.',
                           'En la cuenca de {Patacancha}, Ollantaytambo, se '
                           'ha forestado con Polylepis sp. o {queuña}.',
                           'En la cuenca de {Tambomachay}, Cusco, se ha '
                           'reforestado también con {queuña}.']},
                {'titulo': '16.7 ÁREAS NATURALES PROTEGIDAS DEL PERÚ (ANP)',
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
                           'aprovechamiento de recursos naturales.']},
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
                 'alternativas': ['Ciclo biogeoquímico normal',
                                  'Aumento de biodiversidad',
                                  'Equilibrio ambiental',
                                  'Ninguna alteración',
                                  'Desequilibrio ambiental'],
                 'correcta': 'E'},
                {'pregunta': 'La contaminación se define como la adición de '
                             'sustancias al ambiente en cantidades que:',
                 'alternativas': ['Sobrepasan los niveles regulares de la '
                                  'naturaleza',
                                  'No afectan a ningún organismo',
                                  'Mejoran el ecosistema',
                                  'Se mantienen bajo los niveles normales',
                                  'Son siempre imperceptibles'],
                 'correcta': 'A'},
                {'pregunta': 'A mayor población e índice de uso de recursos '
                             'naturales en un área, generalmente se '
                             'presentan:',
                 'alternativas': ['Mayor biodiversidad automática',
                                  'Menor consumo energético',
                                  'Ningún cambio ambiental',
                                  'Más problemas de contaminación',
                                  'Menos problemas ambientales'],
                 'correcta': 'D'},
                {'pregunta': 'La contaminación causada por fuentes como '
                             'volcanes o efectos geoclimáticos se llama '
                             'contaminación:',
                 'alternativas': ['Antrópica',
                                  'Física exclusiva',
                                  'Biológica exclusiva',
                                  'Química exclusiva',
                                  'Natural'],
                 'correcta': 'E'},
                {'pregunta': 'La contaminación producida o distribuida por '
                             'el ser humano se llama contaminación:',
                 'alternativas': ['Geológica',
                                  'Cósmica',
                                  'Volcánica',
                                  'Natural',
                                  'Antrópica'],
                 'correcta': 'E'},
                {'pregunta': 'Una de las principales fuentes de '
                             'contaminación antropogénica es:',
                 'alternativas': ['Las mareas',
                                  'Los volcanes',
                                  'La radiación solar natural',
                                  'Los terremotos',
                                  'La agricultura industrializada'],
                 'correcta': 'E'},
                {'pregunta': 'Los contaminantes causados por microorganismos '
                             'como bacterias y virus se llaman '
                             'contaminantes:',
                 'alternativas': ['Físicos',
                                  'Sonoros exclusivos',
                                  'Químicos',
                                  'Biológicos',
                                  'Térmicos exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'El vibrión colérico, presente en aguas de ríos '
                             'latinoamericanos, es un ejemplo de '
                             'contaminante:',
                 'alternativas': ['Térmico',
                                  'Biológico',
                                  'Químico',
                                  'Físico',
                                  'Sonoro'],
                 'correcta': 'B'},
                {'pregunta': 'Los contaminantes relacionados con la energía, '
                             'como el ruido o las altas temperaturas, se '
                             'llaman contaminantes:',
                 'alternativas': ['Químicos',
                                  'Biológicos',
                                  'Naturales exclusivos',
                                  'Físicos',
                                  'Orgánicos exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los contaminantes físicos pueden influir en el '
                             'desarrollo de enfermedades humanas de tipo:',
                 'alternativas': ['Psico-neurológicas',
                                  'Solo cardiovasculares exclusivas',
                                  'Solo óseas',
                                  'Solo dermatológicas',
                                  'Solo digestivas'],
                 'correcta': 'A'},
                {'pregunta': 'Los contaminantes provocados por sustancias '
                             'orgánicas o inorgánicas se llaman '
                             'contaminantes:',
                 'alternativas': ['Físicos',
                                  'Biológicos',
                                  'Radiactivos exclusivos',
                                  'Sonoros',
                                  'Químicos'],
                 'correcta': 'E'},
                {'pregunta': 'El impacto más notorio de la contaminación '
                             'química se dio durante:',
                 'alternativas': ['La Revolución Francesa',
                                  'El auge industrial de la Segunda Guerra '
                                  'Mundial',
                                  'La colonización americana',
                                  'La Primera Guerra Mundial exclusivamente',
                                  'La Edad Media'],
                 'correcta': 'B'},
                {'pregunta': 'La contaminación química actualmente es la '
                             'principal causante de:',
                 'alternativas': ['La reproducción celular',
                                  'El calentamiento global',
                                  'La mitosis',
                                  'La fotosíntesis',
                                  'La biodiversidad'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los gases que provocan el calentamiento '
                             'global se mencionan los:',
                 'alternativas': ['Vapor de agua exclusivamente',
                                  'Gases inertes',
                                  'CFC (clorofluorocarbonos)',
                                  'Oxígeno puro',
                                  'Gases nobles'],
                 'correcta': 'C'},
                {'pregunta': 'El agua cubre de la superficie del planeta '
                             'aproximadamente:',
                 'alternativas': ['20%', '30%', '90%', '71%', '50%'],
                 'correcta': 'D'},
                {'pregunta': 'Aunque el agua cubre gran parte del planeta, '
                             'está disponible en cantidades:',
                 'alternativas': ['Excesivas en todas las regiones',
                                  'Infinitas',
                                  'Limitadas y distribuidas de forma no '
                                  'uniforme',
                                  'Ilimitadas',
                                  'Iguales en todo el mundo'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las sustancias químicas que contaminan '
                             'el agua figuran el petróleo y los:',
                 'alternativas': ['Detergentes sintéticos',
                                  'Oxígenos disueltos',
                                  'Minerales esenciales',
                                  'Gases nobles',
                                  'Nutrientes naturales'],
                 'correcta': 'A'},
                {'pregunta': 'Los contaminantes físicos del agua alteran '
                             'principalmente su:',
                 'alternativas': ['pH exclusivamente',
                                  'Salinidad exclusiva',
                                  'Transparencia',
                                  'Composición química exclusiva',
                                  'Temperatura exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando se impide la entrada de luz al agua por '
                             'contaminación física, los productores del '
                             'ecosistema:',
                 'alternativas': ['Aumentan su fotosíntesis',
                                  'No se ven afectados',
                                  'Cambian de especie',
                                  'Deben emigrar o morir',
                                  'Se multiplican más rápido'],
                 'correcta': 'D'},
                {'pregunta': 'Durante los últimos 200 años, el hombre ha '
                             'agregado al ambiente grandes cantidades de:',
                 'alternativas': ['Solo nitrógeno',
                                  'Productos químicos y agentes físicos',
                                  'Solo agua pura',
                                  'Solo materia orgánica natural',
                                  'Solo oxígeno'],
                 'correcta': 'B'},
                {'pregunta': 'Según la UICN (1980), la conservación es la '
                             'gestión de la biosfera para beneficio de las '
                             'generaciones presentes y:',
                 'alternativas': ['Futuras',
                                  'Ninguna otra generación',
                                  'Solo las próximas dos décadas',
                                  'Pasadas exclusivamente',
                                  'Solo la actual'],
                 'correcta': 'A'},
                {'pregunta': 'Uno de los tres objetivos de la conservación '
                             'es preservar la diversidad:',
                 'alternativas': ['Religiosa',
                                  'Cultural exclusiva',
                                  'Genética',
                                  'Política',
                                  'Económica'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente que sostiene que los recursos '
                             'naturales deben mantenerse sin tocar, «bajo '
                             'llave», se llama:',
                 'alternativas': ['Desarrollismo',
                                  'Extractivismo',
                                  'Proteccionismo',
                                  'Mito de la inagotabilidad',
                                  'Conservacionismo'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente basada en el desarrollo '
                             'sostenible y el uso racional de los recursos '
                             'se llama:',
                 'alternativas': ['Explotacionismo',
                                  'Mito de la inagotabilidad',
                                  'Proteccionismo',
                                  'Extractivismo',
                                  'Conservacionismo'],
                 'correcta': 'E'},
                {'pregunta': 'La conservación de componentes de la '
                             'biodiversidad fuera de su hábitat natural se '
                             'llama conservación:',
                 'alternativas': ['In situ',
                                  'Indirecta',
                                  'Directa',
                                  'Ex situ',
                                  'Mixta'],
                 'correcta': 'D'},
                {'pregunta': 'La conservación de especies dentro de sus '
                             'entornos naturales, como en áreas protegidas, '
                             'se llama conservación:',
                 'alternativas': ['Ex situ',
                                  'Artificial',
                                  'Indirecta',
                                  'In situ',
                                  'Externa'],
                 'correcta': 'D'},
                {'pregunta': 'Poblar con árboles áreas que nunca tuvieron '
                             'bosque se llama:',
                 'alternativas': ['Reforestación',
                                  'Forestación',
                                  'Deforestación',
                                  'Agroforestería',
                                  'Silvicultura exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Repoblar con árboles suelos que sí tuvieron '
                             'cobertura forestal antes se llama:',
                 'alternativas': ['Extracción forestal',
                                  'Forestación',
                                  'Tala selectiva',
                                  'Reforestación',
                                  'Deforestación'],
                 'correcta': 'D'},
                {'pregunta': 'En la cuenca de Patacancha, Ollantaytambo, se '
                             'ha forestado principalmente con:',
                 'alternativas': ['Eucalipto',
                                  'Pino',
                                  'Ciprés',
                                  'Molle',
                                  'Queuña (Polylepis sp.)'],
                 'correcta': 'E'},
                {'pregunta': 'Las Áreas Naturales Protegidas del Perú están '
                             'reguladas por la Ley N°:',
                 'alternativas': ['26300',
                                  '27444',
                                  '28611',
                                  '30220',
                                  '29834'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo de la Constitución que obliga al '
                             'Estado a promover la conservación de las ANP '
                             'es el:',
                 'alternativas': ['Artículo 24',
                                  'Artículo 68',
                                  'Artículo 2',
                                  'Artículo 189',
                                  'Artículo 200'],
                 'correcta': 'B'},
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
                                  'SUNARP',
                                  'SERNANP',
                                  'MINAM',
                                  'SINANPE'],
                 'correcta': 'E'},
                {'pregunta': 'Las Áreas Naturales Protegidas con estatus '
                             'definitivo se clasifican en un número de '
                             'categorías igual a:',
                 'alternativas': ['Seis', 'Tres', 'Nueve', 'Doce', 'Cinco'],
                 'correcta': 'C'},
                {'pregunta': 'De las nueve categorías de ANP, el número de '
                             'categorías de uso indirecto es:',
                 'alternativas': ['Seis', 'Tres', 'Uno', 'Nueve', 'Cinco'],
                 'correcta': 'B'},
                {'pregunta': 'Las áreas de uso indirecto permiten '
                             'investigación científica y turismo, pero no '
                             'permiten:',
                 'alternativas': ['La extracción de recursos naturales',
                                  'La visita de turistas',
                                  'La educación ambiental',
                                  'El acceso de científicos',
                                  'La investigación académica'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las áreas de uso indirecto se cuentan '
                             'los Parques Nacionales y los:',
                 'alternativas': ['Santuarios Nacionales',
                                  'Refugios de vida silvestre',
                                  'Bosques de protección',
                                  'Cotos de caza',
                                  'Reservas comunales'],
                 'correcta': 'A'},
                {'pregunta': 'Las áreas de uso directo, a diferencia de las '
                             'de uso indirecto, sí permiten:',
                 'alternativas': ['Solo turismo',
                                  'Ninguna actividad',
                                  'Solo educación',
                                  'Solo investigación',
                                  'El aprovechamiento de recursos naturales'],
                 'correcta': 'E'}]}]
