# ================================================================
# FICHAS DE FILOSOFÍA Y LÓGICA — CEPRU UNSAAC
# Basado en el material oficial «Filosofía y Lógica», Área D.
# ================================================================
"""Mismo formato que el módulo de Historia: por cada balota genera la
ficha de texto para completar a dos columnas y el banco de 20 preguntas
con cinco alternativas, en versión alumno y versión docente.

Reutiliza el motor de fichas_historia.py en lugar de duplicarlo: si un
día se corrige el diseño del PDF, se corrige en un solo sitio y ambos
cursos quedan iguales.

Integración en sistema_web.py:
    from fichas_filosofia import tab_fichas_filosofia
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


BALOTAS_FILO = [{'num': 1,
  'titulo': 'El problema del cosmos y concepciones de filosofía',
  'secciones': [{'titulo': '1.1 COSMOGONÍA Y COSMOLOGÍA',
                 'items': ['{Cosmogonía}: de kosmos = mundo y goneia = '
                           '{nacimiento}. Conjunto de {mitos} y narraciones '
                           'con que las primeras civilizaciones explicaron '
                           'el origen del universo.',
                           '{Hesíodo}, en su poema «{Teogonía}», narra la '
                           'creación del mundo a partir del {caos}.',
                           '{Cosmología}: de kosmos y logos = {estudio}. '
                           'Estudia el universo mediante modelos '
                           '{contrastables} empírica y experimentalmente.',
                           'La diferencia está en que la cosmología explica '
                           'por {conceptos} científicos y verificación, y la '
                           'cosmogonía por {relatos} y mitos.',
                           'Dos posturas marcaron la historia: el '
                           '{geocentrismo}, respaldado por {Ptolomeo} y '
                           'Aristóteles, y el {heliocentrismo}, por Nicolás '
                           '{Copérnico}.']},
                {'titulo': '1.2 TEORÍA DEL BIG BANG',
                 'items': ['Modelo cosmológico según el cual el universo se '
                           'originó en una {singularidad} espaciotemporal de '
                           'densidad infinita, hace unos {14 000} millones '
                           'de años.',
                           '{Hubble} descubrió en {1929} que la distancia '
                           'entre galaxias es cada vez mayor.',
                           'Ley de Hubble: la {velocidad} de una galaxia es '
                           'proporcional a su {distancia}.',
                           'Si una fuente de luz se aleja, su espectro se '
                           'desplaza al {rojo}; si se acerca, al {azul}.']},
                {'titulo': '1.3 ORIGEN Y CONCEPCIONES DE LA FILOSOFÍA',
                 'items': ['Como reflexión racional y sistemática se origina '
                           'en {Grecia}, siglos VII–VI a.C.',
                           'Se atribuye a {Pitágoras} de Samos el primer uso '
                           'del término filosofía. {Sócrates} se llamó a sí '
                           'mismo «amante de la {sabiduría}».',
                           '{Platón} decía que el {asombro} es el origen de '
                           'la filosofía; {Aristóteles}, que es la '
                           '{admiración} lo que impulsa a filosofar.',
                           'Etimología: philein = {amor} y sophos = '
                           '{sabiduría}.',
                           'Concepción {aristotélica}: la filosofía es la '
                           'ciencia de los primeros {principios} y las '
                           'primeras {causas}; por eso se la llama '
                           '{Metafísica} o filosofía primera.',
                           'Concepción {russelliana}: nace de dos impulsos, '
                           'el {místico} y el {científico}; es una tierra de '
                           'nadie entre la ciencia y la {religión}.',
                           'Concepción de {Rosental}: ciencia sobre las '
                           'leyes {universales} del ser y del pensamiento; '
                           'su cuestión fundamental es la relación entre el '
                           '{pensar} y el ser.']},
                {'titulo': '1.4 PROBLEMA FUNDAMENTAL DE LA FILOSOFÍA',
                 'items': ['El problema fundamental de la filosofía es el '
                           'carácter de la relación entre el {ser} y el '
                           '{pensar}, entre lo material y lo espiritual.',
                           'El primer aspecto de este problema busca '
                           'resolver si la {materia} es lo primario, o lo es '
                           'la {conciencia}.',
                           'El segundo aspecto responde si el mundo es '
                           '{cognoscible} o no, es decir, si la razón humana '
                           'puede penetrar sus misterios.',
                           'Los filósofos que consideran que la materia es '
                           'primaria y la conciencia secundaria se sitúan en '
                           'el {materialismo}.',
                           'Los filósofos que consideran que lo primario es '
                           'el {espíritu} y niegan que el mundo sea '
                           'cognoscible se sitúan en el {idealismo}.']},
                {'titulo': '1.5 ACTITUD FILOSÓFICA',
                 'items': ['Es la disposición humana por comprender el '
                           '{porqué} y el {para qué} de las cosas.',
                           'Características: {problemática}, {crítica}, '
                           '{incondicional}, {universal}, {trascendental}, '
                           'racional y {reflexiva}, y un saber '
                           '{totalitario}.']}],
  'cuadros': [{'titulo': '1. COSMOGONÍA FRENTE A COSMOLOGÍA',
               'encabezados': ['Aspecto', 'Cosmogonía', 'Cosmología'],
               'filas': [['Explica por',
                          '{Mitos} y relatos',
                          '{Conceptos} científicos'],
                         ['Método',
                          '{Narrativo}',
                          '{Contrastación} y verificación'],
                         ['Ejemplo',
                          'Teogonía de {Hesíodo}',
                          'Teoría del {Big Bang}']]}],
  'preguntas': [{'pregunta': 'El conjunto de mitos con que las primeras '
                             'civilizaciones explicaron el origen del '
                             'universo se denomina:',
                 'alternativas': ['Metafísica',
                                  'Astronomía',
                                  'Cosmogonía',
                                  'Cosmología',
                                  'Ontología'],
                 'correcta': 'C'},
                {'pregunta': 'El autor del poema «Teogonía» fue:',
                 'alternativas': ['Aristóteles',
                                  'Ptolomeo',
                                  'Hesíodo',
                                  'Homero',
                                  'Platón'],
                 'correcta': 'C'},
                {'pregunta': 'La cosmología se diferencia de la cosmogonía '
                             'porque explica mediante:',
                 'alternativas': ['Relatos y mitos',
                                  'Conceptos científicos y verificación',
                                  'Tradiciones orales',
                                  'Poemas épicos',
                                  'Revelaciones divinas'],
                 'correcta': 'B'},
                {'pregunta': 'El geocentrismo fue respaldado por:',
                 'alternativas': ['Kepler',
                                  'Ptolomeo y Aristóteles',
                                  'Hubble',
                                  'Copérnico',
                                  'Galileo'],
                 'correcta': 'B'},
                {'pregunta': 'El heliocentrismo fue sostenido por:',
                 'alternativas': ['Aristóteles',
                                  'Nicolás Copérnico',
                                  'Hesíodo',
                                  'Ptolomeo',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Big Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['14 000 millones de años',
                                  '500 millones de años',
                                  '1 000 millones de años',
                                  '4 000 millones de años',
                                  '100 000 años'],
                 'correcta': 'A'},
                {'pregunta': 'Hubble descubrió en 1929 que las galaxias:',
                 'alternativas': ['Están fijas en la bóveda celeste',
                                  'Se acercan entre sí',
                                  'Se alejan unas de otras',
                                  'Giran alrededor de la Tierra',
                                  'Permanecen inmóviles'],
                 'correcta': 'C'},
                {'pregunta': 'Según la ley de Hubble, la velocidad de una '
                             'galaxia es proporcional a su:',
                 'alternativas': ['Temperatura',
                                  'Edad',
                                  'Masa',
                                  'Luminosidad',
                                  'Distancia'],
                 'correcta': 'E'},
                {'pregunta': 'Si una fuente de luz se aleja de nosotros, su '
                             'espectro se desplaza hacia el:',
                 'alternativas': ['Azul',
                                  'Violeta',
                                  'Amarillo',
                                  'Rojo',
                                  'Verde'],
                 'correcta': 'D'},
                {'pregunta': 'Se atribuye el primer uso del término '
                             '«filosofía» a:',
                 'alternativas': ['Aristóteles',
                                  'Pitágoras de Samos',
                                  'Sócrates',
                                  'Platón',
                                  'Tales de Mileto'],
                 'correcta': 'B'},
                {'pregunta': 'Para Platón, el origen de la filosofía está '
                             'en:',
                 'alternativas': ['La necesidad',
                                  'La fe',
                                  'El asombro',
                                  'El lenguaje',
                                  'La duda'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, filosofía significa:',
                 'alternativas': ['Búsqueda de Dios',
                                  'Estudio del cosmos',
                                  'Ciencia del pensar',
                                  'Estudio del ser',
                                  'Amor a la sabiduría'],
                 'correcta': 'E'},
                {'pregunta': 'Para Aristóteles, la filosofía es la ciencia '
                             'de:',
                 'alternativas': ['El lenguaje',
                                  'Los fenómenos naturales',
                                  'La sociedad',
                                  'Los primeros principios y las primeras '
                                  'causas',
                                  'La conducta humana'],
                 'correcta': 'D'},
                {'pregunta': 'La filosofía primera, según Aristóteles, se '
                             'denomina también:',
                 'alternativas': ['Gnoseología',
                                  'Metafísica',
                                  'Lógica',
                                  'Física',
                                  'Ética'],
                 'correcta': 'B'},
                {'pregunta': 'Según Russell, la filosofía nació de la unión '
                             'o el conflicto de dos impulsos:',
                 'alternativas': ['Práctico y teórico',
                                  'Racional y emocional',
                                  'Místico y científico',
                                  'Estético y ético',
                                  'Individual y social'],
                 'correcta': 'C'},
                {'pregunta': 'Para Rosental, la cuestión fundamental de la '
                             'filosofía es la relación entre:',
                 'alternativas': ['Lo bello y lo útil',
                                  'La forma y la materia',
                                  'El bien y el mal',
                                  'El pensar y el ser',
                                  'La causa y el efecto'],
                 'correcta': 'D'},
                {'pregunta': 'La actitud filosófica se define como la '
                             'disposición por comprender:',
                 'alternativas': ['Únicamente lo mensurable',
                                  'Las creencias religiosas',
                                  'Los hechos históricos',
                                  'Solo el cómo de las cosas',
                                  'El porqué y el para qué de las cosas'],
                 'correcta': 'E'},
                {'pregunta': 'NO es una característica de la actitud '
                             'filosófica:',
                 'alternativas': ['Universal',
                                  'Crítica',
                                  'Trascendental',
                                  'Dogmática',
                                  'Problemática'],
                 'correcta': 'D'},
                {'pregunta': 'Que la actitud filosófica sea «incondicional» '
                             'significa que:',
                 'alternativas': ['Depende de la autoridad',
                                  'Busca el saber por el saber mismo',
                                  'Acepta cualquier opinión',
                                  'Persigue fines económicos',
                                  'Se somete a la religión'],
                 'correcta': 'B'},
                {'pregunta': 'La filosofía, como reflexión racional y '
                             'sistemática, se origina en:',
                 'alternativas': ['Grecia',
                                  'La India',
                                  'Mesopotamia',
                                  'China',
                                  'Egipto'],
                 'correcta': 'A'},
                {'pregunta': 'El problema fundamental de la filosofía trata '
                             'sobre la relación entre:',
                 'alternativas': ['El bien y el mal',
                                  'El ser y el pensar',
                                  'La vida y la muerte',
                                  'El tiempo y el espacio',
                                  'La razón y la fe'],
                 'correcta': 'B'},
                {'pregunta': 'El primer aspecto del problema fundamental '
                             'busca resolver si es primario:',
                 'alternativas': ['El tiempo o el espacio',
                                  'La materia o la conciencia',
                                  'El bien o el mal',
                                  'La razón o la fe',
                                  'La ciencia o el arte'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo aspecto del problema fundamental '
                             'responde si el mundo es:',
                 'alternativas': ['Finito o infinito',
                                  'Cognoscible o no',
                                  'Material o espiritual',
                                  'Bueno o malo',
                                  'Ordenado o caótico'],
                 'correcta': 'B'},
                {'pregunta': 'Los filósofos que consideran que la materia es '
                             'primaria y engendra la conciencia se sitúan en '
                             'el:',
                 'alternativas': ['Idealismo',
                                  'Materialismo',
                                  'Empirismo exclusivo',
                                  'Racionalismo exclusivo',
                                  'Escepticismo'],
                 'correcta': 'B'},
                {'pregunta': 'Los filósofos que consideran primario al '
                             'espíritu y niegan que el mundo sea cognoscible '
                             'se sitúan en el:',
                 'alternativas': ['Materialismo',
                                  'Idealismo',
                                  'Empirismo',
                                  'Racionalismo',
                                  'Positivismo'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'Historia de la filosofía: edad antigua',
  'secciones': [{'titulo': '2.1 LOS PRESOCRÁTICOS',
                 'items': ['Buscaron el {arjé}: el principio u origen de '
                           'todas las cosas.',
                           '{Tales de Mileto}: el principio de todo es el '
                           '{agua}. Fundador de la Escuela {Jónica}, '
                           'considerado el primer filósofo.',
                           '{Anaximandro}: el arjé es el {ápeiron}, lo '
                           'indeterminado e infinito.',
                           '{Anaxímenes}: el principio es el {aire}.',
                           '{Heráclito} de Éfeso: el arjé es el {fuego}; '
                           'todo {cambia} —«nadie se baña dos veces en el '
                           'mismo río»—. Doctrina del {devenir}.',
                           '{Pitágoras} de Samos fundó en {Crotona} una '
                           'escuela místico-filosófica basada en la doctrina '
                           'de la {metempsicosis}, la transmigración de las '
                           'almas.',
                           'Para Pitágoras, el arjé son los {números}: «las '
                           'cosas son números y los números son cosas». El '
                           'número {10} era el más valorado, representado en '
                           'la {tetraktys}.',
                           '{Parménides} de Elea, con quien se inicia la '
                           '{Metafísica}, sostuvo la afirmación ontológica: '
                           '«el {ser} es», negando la posibilidad del '
                           '{cambio}.',
                           'Para Parménides, admitir el cambio o devenir es '
                           'admitir el {no ser}; formuló, aunque '
                           'implícitamente, el Principio de {Identidad}.',
                           '{Demócrito} de Abdera: todo está compuesto por '
                           '{átomos}, partículas indivisibles, según la '
                           'teoría heredada de su maestro {Leucipo}.']},
                {'titulo': '2.2 SOFISTAS Y SÓCRATES',
                 'items': ['Los {sofistas} enseñaban {retórica} a cambio de '
                           'dinero y defendían el {relativismo}.',
                           '{Protágoras}: «el {hombre} es la medida de todas '
                           'las cosas».',
                           '{Gorgias} de Leontinos fue considerado el '
                           'creador de la sofística; sostuvo en su tratado '
                           '«Sobre la naturaleza o el no ser» tres tesis: '
                           'nada existe, si algo existiera no podría '
                           'conocerse, y si pudiera conocerse no podría '
                           '{comunicarse}.',
                           '{Sócrates} se opuso al relativismo; su método '
                           'fue la {mayéutica}, el arte de dar a luz {ideas} '
                           'mediante preguntas.',
                           'Su lema fue «{conócete a ti mismo}» y afirmaba '
                           '«solo sé que {nada} sé».']},
                {'titulo': '2.3 PLATÓN Y ARISTÓTELES',
                 'items': ['{Platón}: teoría de las {Ideas}. Existen dos '
                           'mundos: el {sensible}, cambiante y aparente, y '
                           'el {inteligible}, de las Ideas eternas.',
                           'Su alegoría más famosa es el mito de la '
                           '{caverna}. Fundó la {Academia}.',
                           '{Aristóteles}: discípulo de Platón; fundó el '
                           '{Liceo}. Rechazó el mundo separado de las Ideas.',
                           'Sostuvo que todo ser se compone de {materia} y '
                           '{forma}: teoría {hilemórfica}.',
                           'Distinguió cuatro causas: material, formal, '
                           '{eficiente} y {final}. Es el padre de la '
                           '{lógica}.']},
                {'titulo': '2.4 EPICURO Y EL ESTOICISMO',
                 'items': ['{Epicuro} de Samos: el fin de la vida es el '
                           '{placer} entendido como ausencia de dolor y '
                           'serenidad o {ataraxia}.',
                           '{Marco Aurelio}, emperador y filósofo {estoico}, '
                           'sostuvo que se debe vivir conforme a la {razón} '
                           'y aceptar el destino.']}],
  'cuadros': [{'titulo': '2.1 EL ARJÉ SEGÚN LOS PRESOCRÁTICOS',
               'encabezados': ['Filósofo', 'Principio (arjé)'],
               'filas': [['{Tales} de Mileto', 'El {agua}'],
                         ['{Anaximandro}', 'El {ápeiron}'],
                         ['{Anaxímenes}', 'El {aire}'],
                         ['{Heráclito}', 'El {fuego}'],
                         ['{Pitágoras}', 'Los {números}'],
                         ['{Demócrito}', 'Los {átomos}']]}],
  'preguntas': [{'pregunta': 'El principio u origen de todas las cosas '
                             'buscado por los presocráticos se denomina:',
                 'alternativas': ['Ápeiron',
                                  'Logos',
                                  'Nous',
                                  'Arjé',
                                  'Eidos'],
                 'correcta': 'D'},
                {'pregunta': 'Para Tales de Mileto, el principio de todas '
                             'las cosas es:',
                 'alternativas': ['El átomo',
                                  'El aire',
                                  'El agua',
                                  'El fuego',
                                  'La tierra'],
                 'correcta': 'C'},
                {'pregunta': 'El ápeiron, lo indeterminado e infinito, fue '
                             'propuesto por:',
                 'alternativas': ['Anaximandro',
                                  'Heráclito',
                                  'Anaxímenes',
                                  'Parménides',
                                  'Tales'],
                 'correcta': 'A'},
                {'pregunta': 'Para Heráclito de Éfeso, el arjé es:',
                 'alternativas': ['El número',
                                  'El agua',
                                  'El fuego',
                                  'El aire',
                                  'El ápeiron'],
                 'correcta': 'C'},
                {'pregunta': 'La frase «nadie se baña dos veces en el mismo '
                             'río» corresponde a:',
                 'alternativas': ['Parménides',
                                  'Sócrates',
                                  'Protágoras',
                                  'Heráclito',
                                  'Demócrito'],
                 'correcta': 'D'},
                {'pregunta': 'Parménides de Elea sostuvo que el ser es:',
                 'alternativas': ['Inmutable',
                                  'Divisible',
                                  'Cambiante',
                                  'Múltiple',
                                  'Material'],
                 'correcta': 'A'},
                {'pregunta': 'Demócrito de Abdera afirmó que todo está '
                             'compuesto por:',
                 'alternativas': ['Números',
                                  'Fuego',
                                  'Átomos',
                                  'Ideas',
                                  'Agua'],
                 'correcta': 'C'},
                {'pregunta': '«El hombre es la medida de todas las cosas» '
                             'pertenece a:',
                 'alternativas': ['Gorgias',
                                  'Protágoras',
                                  'Aristóteles',
                                  'Platón',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'El método socrático de dar a luz las ideas '
                             'mediante preguntas se llama:',
                 'alternativas': ['Ironía',
                                  'Mayéutica',
                                  'Dialéctica',
                                  'Silogismo',
                                  'Inducción'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «solo sé que nada sé» se atribuye a:',
                 'alternativas': ['Heráclito',
                                  'Epicuro',
                                  'Protágoras',
                                  'Platón',
                                  'Sócrates'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría de las Ideas fue formulada por:',
                 'alternativas': ['Sócrates',
                                  'Platón',
                                  'Parménides',
                                  'Demócrito',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'Según Platón, el mundo de las Ideas eternas es '
                             'el mundo:',
                 'alternativas': ['Material',
                                  'Aparente',
                                  'Corpóreo',
                                  'Sensible',
                                  'Inteligible'],
                 'correcta': 'E'},
                {'pregunta': 'La escuela fundada por Platón fue:',
                 'alternativas': ['La Academia',
                                  'La Stoa',
                                  'El Jardín',
                                  'El Liceo',
                                  'El Pórtico'],
                 'correcta': 'A'},
                {'pregunta': 'La escuela fundada por Aristóteles fue:',
                 'alternativas': ['El Jardín',
                                  'La Stoa',
                                  'El Liceo',
                                  'La Academia',
                                  'La Escuela de Mileto'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría hilemórfica de Aristóteles sostiene '
                             'que todo ser se compone de:',
                 'alternativas': ['Idea y copia',
                                  'Ser y no ser',
                                  'Acto y potencia únicamente',
                                  'Materia y forma',
                                  'Cuerpo y alma'],
                 'correcta': 'D'},
                {'pregunta': 'Aristóteles es considerado el padre de la:',
                 'alternativas': ['Política',
                                  'Lógica',
                                  'Ética',
                                  'Psicología',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Para Epicuro, el fin de la vida es el placer '
                             'entendido como:',
                 'alternativas': ['Ausencia de dolor y serenidad',
                                  'Poder político',
                                  'Fama',
                                  'Acumulación de bienes',
                                  'Goce sensorial ilimitado'],
                 'correcta': 'A'},
                {'pregunta': 'El estado de serenidad e imperturbabilidad en '
                             'Epicuro se denomina:',
                 'alternativas': ['Eudaimonía',
                                  'Ataraxia',
                                  'Nous',
                                  'Catarsis',
                                  'Areté'],
                 'correcta': 'B'},
                {'pregunta': 'Marco Aurelio perteneció a la escuela:',
                 'alternativas': ['Cínica',
                                  'Epicúrea',
                                  'Platónica',
                                  'Escéptica',
                                  'Estoica'],
                 'correcta': 'E'},
                {'pregunta': 'Los sofistas se caracterizaron por:',
                 'alternativas': ['Estudiar los astros',
                                  'Enseñar retórica por dinero y defender el '
                                  'relativismo',
                                  'Buscar verdades absolutas',
                                  'Fundar la lógica formal',
                                  'Rechazar la política'],
                 'correcta': 'B'},
                {'pregunta': 'Pitágoras de Samos fundó una escuela '
                             'místico-filosófica en la ciudad de:',
                 'alternativas': ['Mileto',
                                  'Crotona',
                                  'Éfeso',
                                  'Elea',
                                  'Abdera'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina pitagórica sobre la inmortalidad y '
                             'transmigración de las almas se llama:',
                 'alternativas': ['Mayéutica',
                                  'Metempsicosis',
                                  'Dialéctica',
                                  'Reminiscencia',
                                  'Hilozoísmo'],
                 'correcta': 'B'},
                {'pregunta': 'Para Pitágoras, el arjé o principio de todas '
                             'las cosas son:',
                 'alternativas': ['Los átomos',
                                  'Los números',
                                  'El fuego',
                                  'El agua',
                                  'El aire'],
                 'correcta': 'B'},
                {'pregunta': 'El número considerado más valorado por los '
                             'pitagóricos, representado en la tetraktys, fue '
                             'el:',
                 'alternativas': ['4', '10', '7', '1', '100'],
                 'correcta': 'B'},
                {'pregunta': 'El filósofo con quien se inicia la Metafísica '
                             'y el conocimiento científico fue:',
                 'alternativas': ['Heráclito',
                                  'Parménides de Elea',
                                  'Tales de Mileto',
                                  'Demócrito',
                                  'Pitágoras'],
                 'correcta': 'B'},
                {'pregunta': 'La afirmación ontológica central de Parménides '
                             'fue:',
                 'alternativas': ['«Todo fluye»',
                                  '«El ser es»',
                                  '«El hombre es la medida de todas las '
                                  'cosas»',
                                  '«Conócete a ti mismo»',
                                  '«Solo sé que nada sé»'],
                 'correcta': 'B'},
                {'pregunta': 'Para Parménides, admitir el cambio o devenir '
                             'equivale a admitir:',
                 'alternativas': ['El ser',
                                  'El no ser',
                                  'La razón',
                                  'El logos',
                                  'El arjé'],
                 'correcta': 'B'},
                {'pregunta': 'Parménides formuló, aunque de manera '
                             'implícita, el principio lógico de:',
                 'alternativas': ['No contradicción exclusivo',
                                  'Identidad',
                                  'Tercero excluido exclusivo',
                                  'Causalidad',
                                  'Razón suficiente'],
                 'correcta': 'B'},
                {'pregunta': 'Demócrito desarrolló su teoría atómica a '
                             'partir de las ideas de su maestro:',
                 'alternativas': ['Tales',
                                  'Leucipo',
                                  'Anaximandro',
                                  'Parménides',
                                  'Pitágoras'],
                 'correcta': 'B'},
                {'pregunta': 'El sofista considerado el creador de la '
                             'sofística, autor de «Sobre la naturaleza o el '
                             'no ser», fue:',
                 'alternativas': ['Protágoras',
                                  'Gorgias',
                                  'Sócrates',
                                  'Antístenes',
                                  'Trasímaco'],
                 'correcta': 'B'},
                {'pregunta': 'Gorgias sostenía, entre sus tres tesis, que si '
                             'algo existiera:',
                 'alternativas': ['Sería visible para todos',
                                  'No podría ser conocido por el hombre',
                                  'Sería eterno',
                                  'Se transformaría en fuego',
                                  'Sería material'],
                 'correcta': 'B'}]},
 {'num': 3,
  'titulo': 'Edad medieval y renacimiento',
  'secciones': [{'titulo': '3.1 CARACTERÍSTICAS DE LA EDAD MEDIA',
                 'items': ['El pensamiento medieval fue {teocéntrico}: '
                           '{Dios} es el centro de toda explicación.',
                           'La filosofía fue considerada {sierva} de la '
                           'teología («ancilla theologiae»).',
                           'Problema central: la relación entre {razón} y '
                           '{fe}.']},
                {'titulo': '3.2 LA PATRÍSTICA',
                 'items': ['Etapa de los {Padres} de la Iglesia, que '
                           'defendieron el cristianismo frente al paganismo.',
                           '{San Agustín} de Hipona: influido por {Platón}. '
                           'Obras «{Confesiones}» y «La ciudad de {Dios}».',
                           'Sostuvo la doctrina de la {iluminación}: Dios '
                           'ilumina la mente para conocer la {verdad}.',
                           'Su lema fue «{cree} para comprender y comprende '
                           'para creer».',
                           'San Agustín nació en {Tagaste}, en la actual '
                           '{Argelia}.']},
                {'titulo': '3.3 LA ESCOLÁSTICA',
                 'items': ['Método de enseñanza medieval basado en la '
                           '{disputa} y el comentario de textos.',
                           '{Santo Tomás de Aquino}: influido por '
                           '{Aristóteles}. Su obra principal es la «{Suma '
                           'Teológica}».',
                           'Formuló las cinco {vías} para demostrar '
                           'racionalmente la existencia de {Dios}.',
                           'Sostuvo que razón y fe no se {contradicen}, sino '
                           'que se {complementan}.']},
                {'titulo': '3.4 EL RENACIMIENTO',
                 'items': ['Se caracteriza por el {antropocentrismo}: el '
                           '{hombre} pasa a ser el centro.',
                           'Recuperación de la cultura {grecolatina} y '
                           'valoración del {humanismo}.',
                           '{Nicolás Copérnico}, astrónomo polaco '
                           '(1473-1543), formuló la teoría {heliocéntrica}: '
                           'la Tierra gira sobre su eje y orbita alrededor '
                           'del Sol.',
                           'Su obra «{De Revolutionibus Orbium Coelestium}» '
                           'resolvía los problemas del modelo geocéntrico de '
                           '{Ptolomeo}.',
                           '{Nicolás Maquiavelo}: autor de «El {Príncipe}». '
                           'Separó la {política} de la moral; se le atribuye '
                           'la máxima «el {fin} justifica los medios».']}],
  'cuadros': [{'titulo': '3. DOS ETAPAS DEL PENSAMIENTO MEDIEVAL',
               'encabezados': ['Etapa', 'Representante', 'Influencia'],
               'filas': [['{Patrística}', 'San {Agustín}', '{Platón}'],
                         ['{Escolástica}',
                          'Santo Tomás de {Aquino}',
                          '{Aristóteles}']]}],
  'preguntas': [{'pregunta': 'El pensamiento medieval se caracterizó por '
                             'ser:',
                 'alternativas': ['Antropocéntrico',
                                  'Logocéntrico',
                                  'Cosmocéntrico',
                                  'Teocéntrico',
                                  'Empírico'],
                 'correcta': 'D'},
                {'pregunta': 'En la Edad Media la filosofía fue considerada:',
                 'alternativas': ['Un arte liberal menor',
                                  'Independiente de la fe',
                                  'Sinónimo de retórica',
                                  'Sierva de la teología',
                                  'Ciencia suprema'],
                 'correcta': 'D'},
                {'pregunta': 'El problema central de la filosofía medieval '
                             'fue la relación entre:',
                 'alternativas': ['Ser y pensar',
                                  'Razón y fe',
                                  'Cuerpo y alma',
                                  'Bien y mal',
                                  'Materia y forma'],
                 'correcta': 'B'},
                {'pregunta': 'San Agustín de Hipona estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Aristóteles',
                                  'Demócrito',
                                  'Platón',
                                  'Epicuro',
                                  'Los estoicos'],
                 'correcta': 'C'},
                {'pregunta': 'Una obra fundamental de San Agustín es:',
                 'alternativas': ['La República',
                                  'La ciudad de Dios',
                                  'Órganon',
                                  'Suma Teológica',
                                  'El Príncipe'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina agustiniana según la cual Dios '
                             'ilumina la mente humana se llama:',
                 'alternativas': ['Analogía',
                                  'Iluminación',
                                  'Revelación',
                                  'Emanación',
                                  'Predestinación'],
                 'correcta': 'B'},
                {'pregunta': '«Cree para comprender y comprende para creer» '
                             'corresponde a:',
                 'alternativas': ['Platón',
                                  'Santo Tomás',
                                  'Aristóteles',
                                  'Maquiavelo',
                                  'San Agustín'],
                 'correcta': 'E'},
                {'pregunta': 'La etapa de los Padres de la Iglesia se '
                             'denomina:',
                 'alternativas': ['Humanismo',
                                  'Escolástica',
                                  'Ilustración',
                                  'Renacimiento',
                                  'Patrística'],
                 'correcta': 'E'},
                {'pregunta': 'Santo Tomás de Aquino estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Heráclito',
                                  'Parménides',
                                  'Platón',
                                  'Epicuro',
                                  'Aristóteles'],
                 'correcta': 'E'},
                {'pregunta': 'La obra principal de Santo Tomás de Aquino es:',
                 'alternativas': ['Suma Teológica',
                                  'El Príncipe',
                                  'Metafísica',
                                  'Confesiones',
                                  'La ciudad de Dios'],
                 'correcta': 'A'},
                {'pregunta': 'Santo Tomás formuló para demostrar la '
                             'existencia de Dios:',
                 'alternativas': ['Dos silogismos',
                                  'Siete argumentos',
                                  'Las cinco vías',
                                  'Cuatro causas',
                                  'Tres pruebas'],
                 'correcta': 'C'},
                {'pregunta': 'Para Santo Tomás, la razón y la fe:',
                 'alternativas': ['No se relacionan',
                                  'Se complementan',
                                  'Se contradicen',
                                  'Se excluyen',
                                  'Son idénticas'],
                 'correcta': 'B'},
                {'pregunta': 'La escolástica se basó como método en:',
                 'alternativas': ['La disputa y el comentario de textos',
                                  'La experimentación',
                                  'La observación astronómica',
                                  'El diálogo socrático',
                                  'La introspección'],
                 'correcta': 'A'},
                {'pregunta': 'El Renacimiento se caracterizó por el:',
                 'alternativas': ['Dogmatismo',
                                  'Antropocentrismo',
                                  'Escepticismo',
                                  'Teocentrismo',
                                  'Geocentrismo'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «El Príncipe» fue:',
                 'alternativas': ['Nicolás Maquiavelo',
                                  'Descartes',
                                  'Erasmo',
                                  'Tomás Moro',
                                  'Galileo'],
                 'correcta': 'A'},
                {'pregunta': 'Maquiavelo es conocido por separar la política '
                             'de:',
                 'alternativas': ['La religión únicamente',
                                  'La economía',
                                  'El derecho',
                                  'La historia',
                                  'La moral'],
                 'correcta': 'E'},
                {'pregunta': 'La máxima «el fin justifica los medios» se '
                             'atribuye a:',
                 'alternativas': ['Epicuro',
                                  'Platón',
                                  'Maquiavelo',
                                  'Santo Tomás',
                                  'San Agustín'],
                 'correcta': 'C'},
                {'pregunta': 'El Renacimiento recuperó la cultura:',
                 'alternativas': ['Oriental',
                                  'Grecolatina',
                                  'Egipcia',
                                  'Medieval',
                                  'Germánica'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento que valoró la dignidad y las '
                             'capacidades del ser humano se llamó:',
                 'alternativas': ['Estoicismo',
                                  'Escepticismo',
                                  'Humanismo',
                                  'Positivismo',
                                  'Escolasticismo'],
                 'correcta': 'C'},
                {'pregunta': 'La expresión latina «ancilla theologiae» '
                             'significa que la filosofía era:',
                 'alternativas': ['Sierva de la teología',
                                  'Base de la política',
                                  'Madre de la lógica',
                                  'Reina de las ciencias',
                                  'Enemiga de la fe'],
                 'correcta': 'A'},
                {'pregunta': 'El astrónomo polaco que formuló la teoría '
                             'heliocéntrica en el Renacimiento fue:',
                 'alternativas': ['Galileo Galilei',
                                  'Nicolás Copérnico',
                                  'Johannes Kepler',
                                  'Giordano Bruno',
                                  'Tycho Brahe'],
                 'correcta': 'B'},
                {'pregunta': 'La obra de Copérnico que expone la teoría '
                             'heliocéntrica se titula:',
                 'alternativas': ['Novum Organum',
                                  'De Revolutionibus Orbium Coelestium',
                                  'Almagesto',
                                  'Diálogo sobre los dos máximos sistemas',
                                  'Sidereus Nuncius'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría heliocéntrica de Copérnico resolvía '
                             'los problemas del modelo geocéntrico planteado '
                             'por:',
                 'alternativas': ['Aristóteles',
                                  'Ptolomeo',
                                  'Pitágoras',
                                  'Platón',
                                  'Eratóstenes'],
                 'correcta': 'B'},
                {'pregunta': 'San Agustín de Hipona nació en la ciudad de '
                             'Tagaste, ubicada en la actual:',
                 'alternativas': ['Egipto',
                                  'Argelia',
                                  'Túnez',
                                  'Marruecos',
                                  'Libia'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'La filosofía moderna y filosofía en el Perú',
  'secciones': [{'titulo': '4.1 RACIONALISMO Y EMPIRISMO',
                 'items': ['{Francisco Bacon}, materialista inglés, propuso '
                           'el método {inductivo} en su obra «{Novum '
                           'Organum}».',
                           'Bacon sostuvo que antes de investigar hay que '
                           'eliminar los {ídolos} de la mente: prejuicios '
                           'que impiden el conocimiento verdadero.',
                           'Los cuatro ídolos de Bacon son: de la {tribu} '
                           '(interpretación antropomórfica), de la {caverna} '
                           '(prejuicios personales), del {foro} (mal uso del '
                           'lenguaje) y del {teatro} (aceptación acrítica de '
                           'autoridades).',
                           '{René Descartes}, padre de la filosofía moderna, '
                           'fundó el {racionalismo}. Su método parte de la '
                           '{duda} metódica.',
                           'Su principio fundamental es «pienso, luego '
                           '{existo}» ({cogito ergo sum}).',
                           'Descartes distinguió tres sustancias: la {res '
                           'extensa} (sustancia corporal), la {res cogitans} '
                           '(sustancia espiritual o pensamiento), y la res '
                           '{necesaria} (Dios).',
                           '{John Locke}: fundador del {empirismo}. La mente '
                           'al nacer es una {tabla rasa}; todo conocimiento '
                           'proviene de la {experiencia}.',
                           'Locke distinguió dos tipos de experiencia: la '
                           '{externa}, por contacto con los objetos mediante '
                           'los sentidos, y la {interna}, por reflexión de '
                           'la mente sobre sí misma.']},
                {'titulo': '4.1.1 THOMAS HOBBES Y EL CONTRATO SOCIAL',
                 'items': ['{Tomás Hobbes}, filósofo inglés, sostuvo que las '
                           'leyes que rigen al hombre son las mismas que '
                           'rigen el {universo}.',
                           'Para Hobbes, en estado natural el hombre es '
                           '{antisocial} y se mueve por el deseo y el '
                           '{temor}.',
                           'Su célebre frase «el {hombre} es un lobo para el '
                           'hombre» describe el estado de «{guerra} de todos '
                           'contra todos».',
                           'Para superar ese estado, los hombres deben '
                           'establecer un «{contrato social}», transfiriendo '
                           'sus derechos a un {soberano} absoluto.',
                           'Su obra más conocida, donde expone esta teoría, '
                           'es el «{Leviatán}».']},
                {'titulo': '4.2 KANT Y HEGEL',
                 'items': ['{Immanuel Kant}: realizó la síntesis entre '
                           'racionalismo y empirismo, llamada {criticismo}. '
                           'Su lema fue «{atrévete a saber}» (sapere aude).',
                           'Distinguió el {fenómeno}, lo que podemos '
                           'conocer, del {noúmeno} o cosa en sí, '
                           'incognoscible.',
                           'En ética formuló el {imperativo} categórico: '
                           'obra de tal modo que tu acción pueda convertirse '
                           'en ley {universal}.',
                           '{Hegel}: desarrolló el método {dialéctico}, con '
                           'tres momentos: {tesis}, {antítesis} y '
                           '{síntesis}. Su sistema es {idealista}.']},
                {'titulo': '4.2.1 FRIEDRICH NIETZSCHE',
                 'items': ['{Friedrich Nietzsche} es considerado el filósofo '
                           'más importante del {voluntarismo} del siglo XIX.',
                           'Estuvo influenciado por {Schopenhauer} y su obra '
                           '«El mundo como voluntad y {representación}».',
                           'Distinguió dos tipos de moral: la moral del '
                           '{amo}, que exalta la fuerza y la nobleza, y la '
                           'moral del {esclavo}, que exalta la compasión y '
                           'la {resignación}.',
                           'Para Nietzsche, la moral del esclavo es la moral '
                           'de los {cristianos}, que predican el amor al '
                           'prójimo y la renuncia a la vida.',
                           'Proclamó la «{muerte de Dios}»: solo tras ella '
                           'surgirá un nuevo hombre que acepte la vida y el '
                           '{eterno retorno}.',
                           'Planteó el ideal del {superhombre}, que acepta '
                           'la muerte de Dios y vive fiel a la {tierra}, sin '
                           'buscar mundos trascendentes.',
                           'Entre sus obras principales figuran «Así habló '
                           '{Zaratustra}», «Más allá del bien y del mal» y '
                           '«La genealogía de la {moral}».']},
                {'titulo': '4.3 MARX Y EL MATERIALISMO',
                 'items': ['{Carlos Marx}: invirtió la dialéctica de Hegel y '
                           'creó el materialismo {dialéctico} e histórico.',
                           'Sostuvo que la {infraestructura} económica '
                           'determina la {superestructura} jurídica, '
                           'política e ideológica.',
                           '«Los filósofos se han limitado a interpretar el '
                           'mundo; de lo que se trata es de '
                           '{transformarlo}».']},
                {'titulo': '4.4.1 MANUEL GONZÁLEZ PRADA',
                 'items': ['{Manuel González Prada} (1846-1918) mostró su '
                           'inclinación al {positivismo} peruano, como '
                           'respuesta a la crisis tras el caudillismo y la '
                           'guerra con Chile.',
                           'Su balance de la Independencia peruana fue '
                           '{pesimista}: la calificó de una «orgía» que dejó '
                           'heces, manchada por la guerra civil.',
                           'Según González Prada, la {ignorancia} y el '
                           'espíritu de servidumbre determinaron la derrota '
                           'del Perú en la Guerra del {Pacífico}.',
                           'Fue {antirreligioso}, anarquista y {anti '
                           'hispanista}; consideró al Estado un instrumento '
                           'de los poderosos para perpetuar la '
                           '{servidumbre}.',
                           'Sostuvo que el Perú verdadero y profundo es el '
                           'que pertenece a los {indígenas}, y culpó a la '
                           '{oligarquía} de la crisis nacional.',
                           'Su obra principal, «{Páginas Libres}», influyó '
                           'profundamente en Abraham Valdelomar, Haya de la '
                           'Torre y {Mariátegui}.']},
                {'titulo': '4.4 FILOSOFÍA EN EL PERÚ',
                 'items': ['{José Carlos Mariátegui}: autor de «{7 ensayos} '
                           'de interpretación de la realidad peruana». '
                           'Aplicó el {marxismo} al análisis del Perú, '
                           'señalando que el problema del {indio} es un '
                           'problema de la {tierra}.',
                           '{Augusto Salazar Bondy}: autor de «¿Existe una '
                           'filosofía de nuestra {América}?». Sostuvo que '
                           'nuestra filosofía ha sido {imitativa} por ser '
                           'reflejo de una sociedad {dominada}.']}],
  'cuadros': [{'titulo': '4. CORRIENTES DE LA FILOSOFÍA MODERNA',
               'encabezados': ['Corriente',
                               'Representante',
                               'Fuente del conocimiento'],
               'filas': [['{Racionalismo}', '{Descartes}', 'La {razón}'],
                         ['{Empirismo}', '{Locke}', 'La {experiencia}'],
                         ['{Criticismo}',
                          '{Kant}',
                          'Razón y experiencia {unidas}']]}],
  'preguntas': [{'pregunta': 'El padre de la filosofía moderna es:',
                 'alternativas': ['Locke',
                                  'Bacon',
                                  'René Descartes',
                                  'Hegel',
                                  'Kant'],
                 'correcta': 'C'},
                {'pregunta': 'El principio «pienso, luego existo» pertenece '
                             'a:',
                 'alternativas': ['Hegel',
                                  'Kant',
                                  'Locke',
                                  'Marx',
                                  'Descartes'],
                 'correcta': 'E'},
                {'pregunta': 'El método cartesiano parte de:',
                 'alternativas': ['La observación',
                                  'La duda metódica',
                                  'La experiencia sensible',
                                  'La inducción',
                                  'La revelación'],
                 'correcta': 'B'},
                {'pregunta': 'Para el empirismo, todo conocimiento proviene '
                             'de:',
                 'alternativas': ['La intuición',
                                  'Las ideas innatas',
                                  'La revelación',
                                  'La razón pura',
                                  'La experiencia'],
                 'correcta': 'E'},
                {'pregunta': 'John Locke sostuvo que la mente al nacer es:',
                 'alternativas': ['Una tabla rasa',
                                  'Un espejo del cosmos',
                                  'Un reflejo divino',
                                  'Un depósito de ideas innatas',
                                  'Una sustancia pensante'],
                 'correcta': 'A'},
                {'pregunta': 'La síntesis entre racionalismo y empirismo fue '
                             'realizada por:',
                 'alternativas': ['Kant',
                                  'Hegel',
                                  'Descartes',
                                  'Locke',
                                  'Marx'],
                 'correcta': 'A'},
                {'pregunta': 'El lema «atrévete a saber» corresponde a:',
                 'alternativas': ['Hegel',
                                  'Marx',
                                  'Mariátegui',
                                  'Kant',
                                  'Descartes'],
                 'correcta': 'D'},
                {'pregunta': 'Kant llamó «noúmeno» a:',
                 'alternativas': ['La idea innata',
                                  'El juicio sintético',
                                  'La cosa en sí, incognoscible',
                                  'Lo que aparece a los sentidos',
                                  'El imperativo moral'],
                 'correcta': 'C'},
                {'pregunta': 'El imperativo categórico de Kant exige obrar '
                             'de modo que la acción pueda ser:',
                 'alternativas': ['Rentable',
                                  'Placentera',
                                  'Ley universal',
                                  'Útil para uno mismo',
                                  'Aprobada socialmente'],
                 'correcta': 'C'},
                {'pregunta': 'Los tres momentos de la dialéctica hegeliana '
                             'son:',
                 'alternativas': ['Materia, forma y acto',
                                  'Ser, no ser y devenir',
                                  'Tesis, antítesis y síntesis',
                                  'Duda, método y certeza',
                                  'Causa, efecto y fin'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema filosófico de Hegel es:',
                 'alternativas': ['Idealista',
                                  'Empirista',
                                  'Positivista',
                                  'Materialista',
                                  'Escéptico'],
                 'correcta': 'A'},
                {'pregunta': 'Marx invirtió la dialéctica de Hegel y '
                             'desarrolló:',
                 'alternativas': ['El pragmatismo',
                                  'El materialismo dialéctico e histórico',
                                  'El criticismo',
                                  'El empirismo',
                                  'El idealismo absoluto'],
                 'correcta': 'B'},
                {'pregunta': 'Para Marx, la infraestructura económica '
                             'determina:',
                 'alternativas': ['La superestructura jurídica, política e '
                                  'ideológica',
                                  'La geografía',
                                  'La biología',
                                  'El lenguaje únicamente',
                                  'El clima'],
                 'correcta': 'A'},
                {'pregunta': '«Los filósofos se han limitado a interpretar '
                             'el mundo; de lo que se trata es de '
                             'transformarlo» pertenece a:',
                 'alternativas': ['Hegel',
                                  'Salazar Bondy',
                                  'Mariátegui',
                                  'Kant',
                                  'Marx'],
                 'correcta': 'E'},
                {'pregunta': 'El autor de «7 ensayos de interpretación de la '
                             'realidad peruana» es:',
                 'alternativas': ['González Prada',
                                  'Francisco Miró Quesada',
                                  'Augusto Salazar Bondy',
                                  'José Carlos Mariátegui',
                                  'Víctor Raúl Haya de la Torre'],
                 'correcta': 'D'},
                {'pregunta': 'Para Mariátegui, el problema del indio es '
                             'fundamentalmente un problema:',
                 'alternativas': ['Religioso',
                                  'Educativo',
                                  'Administrativo',
                                  'De la tierra',
                                  'Racial'],
                 'correcta': 'D'},
                {'pregunta': 'El autor de «¿Existe una filosofía de nuestra '
                             'América?» es:',
                 'alternativas': ['Francisco Miró Quesada',
                                  'Augusto Salazar Bondy',
                                  'Mariátegui',
                                  'Antenor Orrego',
                                  'Alejandro Deustua'],
                 'correcta': 'B'},
                {'pregunta': 'Según Salazar Bondy, la filosofía '
                             'latinoamericana ha sido:',
                 'alternativas': ['Superior a la europea',
                                  'Puramente científica',
                                  'Imitativa, reflejo de una sociedad '
                                  'dominada',
                                  'Original y autónoma',
                                  'Inexistente'],
                 'correcta': 'C'},
                {'pregunta': 'Mariátegui aplicó al análisis del Perú el '
                             'método:',
                 'alternativas': ['Existencialista',
                                  'Marxista',
                                  'Fenomenológico',
                                  'Escolástico',
                                  'Positivista'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo kantiano sostiene que el '
                             'conocimiento resulta de:',
                 'alternativas': ['La unión de razón y experiencia',
                                  'Solo la razón',
                                  'La revelación divina',
                                  'La tradición',
                                  'Solo los sentidos'],
                 'correcta': 'A'},
                {'pregunta': 'El filósofo inglés materialista que propuso el '
                             'método inductivo en su obra Novum Organum fue:',
                 'alternativas': ['John Locke',
                                  'Francisco Bacon',
                                  'Tomás Hobbes',
                                  'David Hume',
                                  'Thomas Aquino'],
                 'correcta': 'B'},
                {'pregunta': 'Bacon sostuvo que antes de investigar hay que '
                             'eliminar de la mente los:',
                 'alternativas': ['Silogismos',
                                  'Ídolos',
                                  'Axiomas',
                                  'Postulados',
                                  'Dogmas'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano que consiste en interpretar '
                             'antropomórficamente la naturaleza se llama '
                             'ídolo de la:',
                 'alternativas': ['Caverna',
                                  'Tribu',
                                  'Foro',
                                  'Teatro',
                                  'Ciudad'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano originado en los prejuicios '
                             'personales de cada individuo se llama ídolo de '
                             'la:',
                 'alternativas': ['Tribu',
                                  'Caverna',
                                  'Foro',
                                  'Teatro',
                                  'Escuela'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano relacionado con el mal uso '
                             'del lenguaje se llama ídolo del:',
                 'alternativas': ['Teatro',
                                  'Foro',
                                  'Tribu',
                                  'Templo',
                                  'Palacio'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano relacionado con la '
                             'aceptación acrítica de autoridades se llama '
                             'ídolo del:',
                 'alternativas': ['Foro',
                                  'Teatro',
                                  'Tribu',
                                  'Caverna',
                                  'Mercado'],
                 'correcta': 'B'},
                {'pregunta': 'Descartes distinguió tres sustancias: la res '
                             'extensa, la res necesaria y la:',
                 'alternativas': ['Res publica',
                                  'Res cogitans',
                                  'Res divina exclusiva',
                                  'Res naturae',
                                  'Res finita'],
                 'correcta': 'B'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'espiritual, cuya esencia es el pensamiento, se '
                             'llama:',
                 'alternativas': ['Res extensa',
                                  'Res cogitans',
                                  'Res necesaria',
                                  'Res corporal',
                                  'Res mundi'],
                 'correcta': 'B'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'corporal, cuya esencia es la extensión, se '
                             'llama:',
                 'alternativas': ['Res cogitans',
                                  'Res extensa',
                                  'Res necesaria',
                                  'Res divina',
                                  'Res mentis'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke distinguió dos tipos de '
                             'experiencia: la interna y la:',
                 'alternativas': ['Trascendental',
                                  'Externa',
                                  'Espiritual',
                                  'Innata',
                                  'Racional'],
                 'correcta': 'B'},
                {'pregunta': 'La experiencia que surge cuando la mente '
                             'reflexiona sobre sus propias sensaciones, '
                             'según Locke, se llama experiencia:',
                 'alternativas': ['Externa',
                                  'Interna',
                                  'Sensorial exclusiva',
                                  'Innata',
                                  'Trascendental'],
                 'correcta': 'B'},
                {'pregunta': 'Tomás Hobbes sostuvo que en estado natural el '
                             'hombre es:',
                 'alternativas': ['Sociable por naturaleza',
                                  'Antisocial, movido por el deseo y el '
                                  'temor',
                                  'Racional puro',
                                  'Altruista',
                                  'Pacífico por instinto'],
                 'correcta': 'B'},
                {'pregunta': 'La célebre frase de Hobbes que describe la '
                             'naturaleza humana en estado natural es:',
                 'alternativas': ['«El hombre es la medida de todas las '
                                  'cosas»',
                                  '«El hombre es un lobo para el hombre»',
                                  '«El hombre nace bueno»',
                                  '«El hombre es un animal político»',
                                  '«El hombre es un junco pensante»'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hobbes, para superar el estado de guerra '
                             'de todos contra todos, los hombres deben '
                             'establecer un:',
                 'alternativas': ['Imperio universal',
                                  'Contrato social',
                                  'Sistema feudal',
                                  'Gobierno directo',
                                  'Concilio religioso'],
                 'correcta': 'B'},
                {'pregunta': 'La obra más conocida de Hobbes, donde expone '
                             'su teoría del contrato social, es:',
                 'alternativas': ['El Príncipe',
                                  'El Leviatán',
                                  'Utopía',
                                  'El Contrato Social',
                                  'Dos Tratados sobre el Gobierno'],
                 'correcta': 'B'},
                {'pregunta': 'Friedrich Nietzsche es considerado el filósofo '
                             'más importante del siglo XIX en la corriente '
                             'del:',
                 'alternativas': ['Racionalismo',
                                  'Voluntarismo',
                                  'Empirismo',
                                  'Positivismo',
                                  'Idealismo absoluto'],
                 'correcta': 'B'},
                {'pregunta': 'Nietzsche estuvo influenciado principalmente '
                             'por el filósofo:',
                 'alternativas': ['Hegel',
                                  'Schopenhauer',
                                  'Kant',
                                  'Descartes',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'Nietzsche distinguió la moral del amo, que '
                             'exalta la fuerza, de la moral:',
                 'alternativas': ['Divina',
                                  'Del esclavo',
                                  'Universal',
                                  'Racional',
                                  'Científica'],
                 'correcta': 'B'},
                {'pregunta': 'Para Nietzsche, la moral del esclavo, que '
                             'exalta la compasión y la resignación, es la '
                             'moral de los:',
                 'alternativas': ['Filósofos griegos',
                                  'Cristianos',
                                  'Guerreros',
                                  'Científicos',
                                  'Comerciantes'],
                 'correcta': 'B'},
                {'pregunta': 'Nietzsche proclamó una idea célebre conocida '
                             'como:',
                 'alternativas': ['El nacimiento de Dios',
                                  'La muerte de Dios',
                                  'El regreso de Dios',
                                  'La duda de Dios',
                                  'El silencio de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'El ideal nietzscheano del hombre que acepta la '
                             'muerte de Dios y vive fiel a la tierra se '
                             'llama:',
                 'alternativas': ['El hombre racional',
                                  'El superhombre',
                                  'El hombre virtuoso',
                                  'El hombre sabio',
                                  'El hombre justo'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las obras principales de Nietzsche es:',
                 'alternativas': ['El Príncipe',
                                  'Así habló Zaratustra',
                                  'Utopía',
                                  'El Leviatán',
                                  'Confesiones'],
                 'correcta': 'B'},
                {'pregunta': 'Manuel González Prada mostró su inclinación '
                             'filosófica hacia el:',
                 'alternativas': ['Idealismo',
                                  'Positivismo',
                                  'Racionalismo',
                                  'Empirismo puro',
                                  'Existencialismo'],
                 'correcta': 'B'},
                {'pregunta': 'El balance que hizo González Prada de la '
                             'Independencia del Perú fue:',
                 'alternativas': ['Optimista',
                                  'Pesimista',
                                  'Neutral',
                                  'Indiferente',
                                  'Triunfalista'],
                 'correcta': 'B'},
                {'pregunta': 'Según González Prada, la derrota del Perú en '
                             'la Guerra del Pacífico se debió principalmente '
                             'a:',
                 'alternativas': ['La superioridad militar chilena '
                                  'exclusivamente',
                                  'La ignorancia y el espíritu de '
                                  'servidumbre',
                                  'La falta de armamento',
                                  'El clima',
                                  'La distancia geográfica'],
                 'correcta': 'B'},
                {'pregunta': 'González Prada consideraba que el Estado era '
                             'un instrumento de los poderosos para '
                             'perpetuar:',
                 'alternativas': ['El progreso',
                                  'La servidumbre de los más débiles',
                                  'La ciencia',
                                  'La educación',
                                  'El comercio'],
                 'correcta': 'B'},
                {'pregunta': 'Para González Prada, el Perú verdadero y '
                             'profundo es el que pertenece a:',
                 'alternativas': ['Los criollos',
                                  'Los indígenas',
                                  'La oligarquía',
                                  'El clero',
                                  'Los extranjeros'],
                 'correcta': 'B'},
                {'pregunta': 'La obra principal de González Prada, que '
                             'influyó en Mariátegui y Haya de la Torre, es:',
                 'alternativas': ['Horas de lucha',
                                  'Páginas Libres',
                                  'Anarquía',
                                  'Nuevas páginas libres',
                                  'El Perú profundo'],
                 'correcta': 'B'}]},
 {'num': 5,
  'titulo': 'Antropología filosófica: el problema del hombre',
  'secciones': [{'titulo': '5.1 CONCEPTO',
                 'items': ['Disciplina filosófica que estudia al {hombre} en '
                           'su totalidad: su esencia, su origen y el sentido '
                           'de su {existencia}.',
                           'Se diferencia de la antropología {cultural} '
                           'porque no describe costumbres, sino que '
                           'reflexiona sobre el {ser} del hombre.']},
                {'titulo': '5.2 TEORÍAS SOBRE EL ORIGEN DEL HOMBRE',
                 'items': ['{Creacionismo}: el hombre fue creado por un ser '
                           '{superior}. Incluye la tradición '
                           '{judeocristiana} y el mito griego de {Prometeo}.',
                           '{Evolucionismo}: el hombre es producto de un '
                           'proceso de {evolución}; formulado por Charles '
                           '{Darwin} mediante la selección {natural}.',
                           '{Neodarwinismo} o Teoría Sintética: complementa '
                           'a Darwin con los aportes de la genética; sus '
                           'representantes son {Dobzhansky}, Mayr y '
                           '{Simpson}.']},
                {'titulo': '5.3 y 5.4 EL HOMBRE COMO SER NATURAL Y '
                           'ESPIRITUAL',
                 'items': ['Como ser {natural}: posee un cuerpo {biológico} '
                           'sujeto a las leyes de la naturaleza, con '
                           'necesidades e instintos.',
                           'Como ser {espiritual}: posee {conciencia}, '
                           'libertad, capacidad de crear {cultura}, valores '
                           'y símbolos.',
                           'El hombre es un ser {social} por naturaleza, '
                           'según {Aristóteles} («zoon politikon»).',
                           'Es también un ser {racional}, capaz de '
                           '{lenguaje} simbólico y de trabajo '
                           'transformador.']}],
  'cuadros': [{'titulo': '5.2 TEORÍAS SOBRE EL ORIGEN DEL HOMBRE',
               'encabezados': ['Teoría', 'Sostiene', 'Representante'],
               'filas': [['{Creacionismo}',
                          'Creación por un ser {superior}',
                          'Tradición {judeocristiana}'],
                         ['{Evolucionismo}',
                          '{Selección} natural',
                          '{Darwin}'],
                         ['{Neodarwinismo}',
                          'Evolución más {genética}',
                          'Biología moderna']]}],
  'preguntas': [{'pregunta': 'La disciplina filosófica que estudia al hombre '
                             'en su totalidad es:',
                 'alternativas': ['Ética',
                                  'Axiología',
                                  'Gnoseología',
                                  'Ontología',
                                  'Antropología filosófica'],
                 'correcta': 'E'},
                {'pregunta': 'La antropología filosófica se diferencia de la '
                             'cultural porque:',
                 'alternativas': ['Estudia fósiles',
                                  'Describe costumbres',
                                  'Mide cráneos',
                                  'Reflexiona sobre el ser del hombre',
                                  'Analiza idiomas'],
                 'correcta': 'D'},
                {'pregunta': 'El creacionismo sostiene que el hombre fue:',
                 'alternativas': ['Resultado de mutaciones',
                                  'Autogenerado',
                                  'Creado por un ser superior',
                                  'Producto del azar',
                                  'Fruto de la evolución'],
                 'correcta': 'C'},
                {'pregunta': 'El mito griego que explica el origen del '
                             'hombre mediante un titán es el de:',
                 'alternativas': ['Sísifo',
                                  'Narciso',
                                  'Ícaro',
                                  'Prometeo',
                                  'Edipo'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de la evolución por selección '
                             'natural fue formulada por:',
                 'alternativas': ['De Vries',
                                  'Charles Darwin',
                                  'Lamarck',
                                  'Wallace únicamente',
                                  'Mendel'],
                 'correcta': 'B'},
                {'pregunta': 'El neodarwinismo complementa a Darwin con los '
                             'aportes de:',
                 'alternativas': ['La astronomía',
                                  'La geología',
                                  'La teología',
                                  'La genética y las mutaciones',
                                  'La lingüística'],
                 'correcta': 'D'},
                {'pregunta': 'Como ser natural, el hombre se caracteriza '
                             'por:',
                 'alternativas': ['Crear valores',
                                  'Poseer un cuerpo biológico sujeto a leyes '
                                  'naturales',
                                  'Ser libre',
                                  'Producir cultura',
                                  'Su capacidad simbólica'],
                 'correcta': 'B'},
                {'pregunta': 'Como ser espiritual, el hombre posee:',
                 'alternativas': ['Conciencia, libertad y capacidad de crear '
                                  'cultura',
                                  'Únicamente sensaciones',
                                  'Instintos',
                                  'Reflejos condicionados',
                                  'Solo necesidades biológicas'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión «zoon politikon», que define al '
                             'hombre como ser social, es de:',
                 'alternativas': ['Platón',
                                  'Rousseau',
                                  'Aristóteles',
                                  'Hobbes',
                                  'Sócrates'],
                 'correcta': 'C'},
                {'pregunta': 'Lo que distingue al hombre del resto de '
                             'animales, según la antropología filosófica, '
                             'es:',
                 'alternativas': ['Su racionalidad y capacidad simbólica',
                                  'Su tamaño',
                                  'Su fuerza física',
                                  'Su alimentación',
                                  'Su longevidad'],
                 'correcta': 'A'},
                {'pregunta': 'La capacidad humana de transformar la '
                             'naturaleza mediante la actividad consciente '
                             'es:',
                 'alternativas': ['La adaptación pasiva',
                                  'La mutación',
                                  'El instinto',
                                  'El trabajo',
                                  'El reflejo'],
                 'correcta': 'D'},
                {'pregunta': 'La tradición judeocristiana corresponde a la '
                             'teoría:',
                 'alternativas': ['Neodarwinista',
                                  'Materialista',
                                  'Positivista',
                                  'Creacionista',
                                  'Evolucionista'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre es considerado un ser bidimensional '
                             'porque es a la vez:',
                 'alternativas': ['Racional e irracional',
                                  'Joven y viejo',
                                  'Individual y aislado',
                                  'Bueno y malo',
                                  'Natural y espiritual'],
                 'correcta': 'E'},
                {'pregunta': 'El lenguaje simbólico es una característica:',
                 'alternativas': ['Innata y no aprendida',
                                  'Compartida con todos los animales',
                                  'Exclusiva de los primates',
                                  'Puramente instintiva',
                                  'Propia del ser humano'],
                 'correcta': 'E'},
                {'pregunta': 'La antropología filosófica se pregunta '
                             'fundamentalmente por:',
                 'alternativas': ['La esencia y el sentido de la existencia '
                                  'humana',
                                  'Las costumbres de los pueblos',
                                  'La anatomía comparada',
                                  'La distribución geográfica',
                                  'Los restos arqueológicos'],
                 'correcta': 'A'},
                {'pregunta': 'La cultura, según la antropología filosófica, '
                             'es producto de la dimensión:',
                 'alternativas': ['Genética',
                                  'Espiritual',
                                  'Instintiva',
                                  'Biológica',
                                  'Refleja'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad humana implica fundamentalmente la '
                             'capacidad de:',
                 'alternativas': ['Seguir los instintos',
                                  'Hacer cualquier cosa sin límites',
                                  'Elegir y responder por los propios actos',
                                  'Evitar toda norma',
                                  'Someterse al destino'],
                 'correcta': 'C'},
                {'pregunta': 'Para el evolucionismo, el hombre y los '
                             'primates actuales comparten:',
                 'alternativas': ['El mismo lenguaje',
                                  'Idéntica especie',
                                  'La misma cultura',
                                  'Un antepasado común',
                                  'Igual capacidad simbólica'],
                 'correcta': 'D'},
                {'pregunta': 'Las necesidades e instintos corresponden a la '
                             'dimensión humana:',
                 'alternativas': ['Cultural',
                                  'Natural o biológica',
                                  'Espiritual',
                                  'Simbólica',
                                  'Axiológica'],
                 'correcta': 'B'},
                {'pregunta': 'El ser humano crea valores, normas y símbolos '
                             'porque es un ser:',
                 'alternativas': ['Aislado',
                                  'Instintivo',
                                  'Puramente biológico',
                                  'Cultural y espiritual',
                                  'Determinado genéticamente'],
                 'correcta': 'D'},
                {'pregunta': 'Los representantes de la Teoría Sintética o '
                             'Neodarwinismo son Dobzhansky, Mayr y:',
                 'alternativas': ['Lamarck',
                                  'Simpson',
                                  'Wallace',
                                  'Mendel',
                                  'Haeckel'],
                 'correcta': 'B'}]},
 {'num': 6,
  'titulo': 'Gnoseología: problema del conocimiento',
  'secciones': [{'titulo': '6.1 CONCEPTO',
                 'items': ['Del griego gnosis = {conocimiento} y logos = '
                           '{estudio}. Es la disciplina que estudia el '
                           'conocimiento en general: su origen, su {esencia} '
                           'y sus {límites}.']},
                {'titulo': '6.2 ESTRUCTURA DEL CONOCIMIENTO',
                 'items': ['El {sujeto} cognoscente: quien conoce.',
                           'El {objeto} de conocimiento: aquello que es '
                           'conocido.',
                           'La {imagen} o representación mental que el '
                           'sujeto elabora del objeto.',
                           'En el acto de conocer, el sujeto {sale} de sí y '
                           'aprehende las propiedades del objeto; el objeto '
                           'permanece {inalterado}.']},
                {'titulo': '6.3 CLASES DE CONOCIMIENTO',
                 'items': ['Conocimiento {sensible}: se obtiene por los '
                           '{sentidos}; es singular, concreto y subjetivo.',
                           'Conocimiento {lógico} o racional: se obtiene por '
                           'la {razón}; es universal, abstracto y objetivo.',
                           'El conocimiento {vulgar} es espontáneo y no '
                           'verificado; el {científico} es metódico, '
                           'sistemático y {verificable}.']},
                {'titulo': '6.4 LA VERDAD',
                 'items': ['Teoría de la {correspondencia}: la verdad es la '
                           'adecuación entre el {pensamiento} y la realidad. '
                           'Es la concepción {clásica} o aristotélica.',
                           'Teoría {pragmática}: es verdadero aquello que '
                           'resulta {útil} o funciona en la práctica.',
                           'Teoría de la {coherencia}: un enunciado es '
                           'verdadero si no {contradice} al conjunto del '
                           'sistema.']}],
  'cuadros': [{'titulo': '6.3 CLASES DE CONOCIMIENTO',
               'encabezados': ['Clase', 'Se obtiene por', 'Carácter'],
               'filas': [['{Sensible}',
                          'Los {sentidos}',
                          'Singular y {concreto}'],
                         ['{Racional}',
                          'La {razón}',
                          'Universal y {abstracto}']]}],
  'preguntas': [{'pregunta': 'La disciplina que estudia el conocimiento en '
                             'general se denomina:',
                 'alternativas': ['Ética',
                                  'Gnoseología',
                                  'Ontología',
                                  'Lógica',
                                  'Axiología'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, gnoseología proviene de '
                             'gnosis, que significa:',
                 'alternativas': ['Palabra',
                                  'Conocimiento',
                                  'Valor',
                                  'Ley',
                                  'Ser'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento del conocimiento que designa a '
                             'quien conoce es:',
                 'alternativas': ['La verdad',
                                  'El sujeto cognoscente',
                                  'El objeto',
                                  'La imagen',
                                  'El método'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental que el sujeto elabora '
                             'del objeto se denomina:',
                 'alternativas': ['Idea innata',
                                  'Imagen',
                                  'Símbolo',
                                  'Concepto puro',
                                  'Juicio'],
                 'correcta': 'B'},
                {'pregunta': 'En el acto de conocer, el objeto:',
                 'alternativas': ['Permanece inalterado',
                                  'Se subjetiviza',
                                  'Se transforma',
                                  'Desaparece',
                                  'Se destruye'],
                 'correcta': 'A'},
                {'pregunta': 'El conocimiento obtenido a través de los '
                             'sentidos es:',
                 'alternativas': ['Sensible',
                                  'Racional',
                                  'Científico',
                                  'Abstracto',
                                  'Universal'],
                 'correcta': 'A'},
                {'pregunta': 'El conocimiento sensible se caracteriza por '
                             'ser:',
                 'alternativas': ['Universal y abstracto',
                                  'Necesario',
                                  'Deductivo',
                                  'Singular, concreto y subjetivo',
                                  'Apriorístico'],
                 'correcta': 'D'},
                {'pregunta': 'El conocimiento racional se caracteriza por '
                             'ser:',
                 'alternativas': ['Sensorial',
                                  'Universal, abstracto y objetivo',
                                  'Concreto',
                                  'Momentáneo',
                                  'Singular'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento espontáneo, no verificado ni '
                             'sistemático es el:',
                 'alternativas': ['Teológico',
                                  'Técnico',
                                  'Científico',
                                  'Vulgar',
                                  'Filosófico'],
                 'correcta': 'D'},
                {'pregunta': 'El conocimiento científico se caracteriza por '
                             'ser:',
                 'alternativas': ['Dogmático',
                                  'Metódico, sistemático y verificable',
                                  'Subjetivo',
                                  'Espontáneo',
                                  'Intuitivo'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría que define la verdad como adecuación '
                             'entre el pensamiento y la realidad es la de:',
                 'alternativas': ['El consenso',
                                  'La coherencia',
                                  'La correspondencia',
                                  'El pragmatismo',
                                  'La utilidad'],
                 'correcta': 'C'},
                {'pregunta': 'La concepción clásica de la verdad se atribuye '
                             'a:',
                 'alternativas': ['James',
                                  'Descartes',
                                  'Hegel',
                                  'Aristóteles',
                                  'Kant'],
                 'correcta': 'D'},
                {'pregunta': 'Para la teoría pragmática, es verdadero '
                             'aquello que:',
                 'alternativas': ['Es revelado',
                                  'No se contradice',
                                  'Corresponde a la realidad',
                                  'Resulta útil o funciona en la práctica',
                                  'Es evidente'],
                 'correcta': 'D'},
                {'pregunta': 'Según la teoría de la coherencia, un enunciado '
                             'es verdadero si:',
                 'alternativas': ['Es intuitivo',
                                  'Es útil',
                                  'Lo dice una autoridad',
                                  'Se comprueba experimentalmente',
                                  'No contradice al sistema del que forma '
                                  'parte'],
                 'correcta': 'E'},
                {'pregunta': 'Los tres elementos del conocimiento son '
                             'sujeto, objeto e:',
                 'alternativas': ['Instrumento',
                                  'Imagen',
                                  'Interpretación',
                                  'Método',
                                  'Interés'],
                 'correcta': 'B'},
                {'pregunta': 'La gnoseología estudia del conocimiento su '
                             'origen, su esencia y sus:',
                 'alternativas': ['Costos',
                                  'Límites',
                                  'Instrumentos',
                                  'Autores',
                                  'Aplicaciones'],
                 'correcta': 'B'},
                {'pregunta': 'Percibir el color rojo de una manzana '
                             'corresponde al conocimiento:',
                 'alternativas': ['Científico',
                                  'Abstracto',
                                  'Racional',
                                  'Deductivo',
                                  'Sensible'],
                 'correcta': 'E'},
                {'pregunta': 'Comprender el concepto de «justicia» '
                             'corresponde al conocimiento:',
                 'alternativas': ['Sensible',
                                  'Perceptivo',
                                  'Instintivo',
                                  'Racional',
                                  'Empírico puro'],
                 'correcta': 'D'},
                {'pregunta': 'En la relación cognoscitiva, aquello que es '
                             'conocido se denomina:',
                 'alternativas': ['Sujeto',
                                  'Imagen',
                                  'Fin',
                                  'Método',
                                  'Objeto'],
                 'correcta': 'E'},
                {'pregunta': 'La afirmación «la nieve es blanca es verdadera '
                             'si la nieve es blanca» ilustra la teoría de:',
                 'alternativas': ['El consenso',
                                  'La coherencia',
                                  'La correspondencia',
                                  'La autoridad',
                                  'El pragmatismo'],
                 'correcta': 'C'}]},
 {'num': 7,
  'titulo': 'Corrientes del problema del conocimiento',
  'secciones': [{'titulo': '7.1 POSIBILIDAD DEL CONOCIMIENTO',
                 'items': ['{Dogmatismo}: sostiene que el conocimiento es '
                           '{posible} y seguro; representantes: los '
                           '{presocráticos}.',
                           '{Escepticismo}: niega la posibilidad de alcanzar '
                           'un conocimiento {seguro}. Su representante '
                           'clásico es {Pirrón} de Elis.',
                           'El escepticismo {radical} o absoluto, '
                           'representado por {Gorgias}, niega toda '
                           'posibilidad de conocer.',
                           'El escepticismo {relativo}, representado por '
                           '{Protágoras}, sostiene que toda verdad es '
                           'relativa.',
                           'El escepticismo {absoluto} niega toda '
                           'posibilidad de conocer; el {relativo} solo la '
                           'duda en algunos campos.',
                           '{Criticismo}: posición intermedia sostenida por '
                           '{Kant}; el conocimiento es posible pero con '
                           '{límites}.',
                           'El {agnosticismo}, sostenido también por {Kant}, '
                           'admite la imposibilidad de conocer la «cosa en '
                           'sí».']},
                {'titulo': '7.2 ORIGEN DEL CONOCIMIENTO',
                 'items': ['{Racionalismo}: el origen del conocimiento es la '
                           '{razón}; su método es la deducción. '
                           'Representantes: {Descartes}, Leibniz, Spinoza y '
                           '{Malebranche}.',
                           '{Empirismo}: el origen es la {experiencia}; su '
                           'método es la inducción. Representantes: {Locke}, '
                           'Hume, Bacon y {Berkeley}.',
                           '{Criticismo}: razón y experiencia se '
                           '{complementan}; «los conceptos sin intuiciones '
                           'son {vacíos}, las intuiciones sin conceptos son '
                           '{ciegas}».']},
                {'titulo': '7.3 ESENCIA DEL CONOCIMIENTO',
                 'items': ['{Idealismo} subjetivo: la realidad depende de la '
                           '{conciencia} del sujeto. «Ser es ser '
                           '{percibido}» ({Berkeley}).',
                           'Idealismo {objetivo}: existe una realidad ideal '
                           'independiente del sujeto, como las Ideas de '
                           '{Platón} o el Espíritu de {Hegel}.',
                           '{Materialismo}: la {materia} es lo primario; el '
                           'mundo es cognoscible y la {praxis} es el '
                           'criterio de verdad.',
                           '{Fenomenalismo}: solo conocemos los {fenómenos}, '
                           'no la cosa en sí o {noúmeno}; representante: '
                           '{Kant}.']}],
  'cuadros': [{'titulo': '7. CORRIENTES GNOSEOLÓGICAS',
               'encabezados': ['Problema', 'Corriente', 'Representante'],
               'filas': [['Posibilidad', '{Escepticismo}', '{Pirrón}'],
                         ['Origen', '{Racionalismo}', '{Descartes}'],
                         ['Origen', '{Empirismo}', '{Locke}'],
                         ['Esencia', 'Idealismo {subjetivo}', '{Berkeley}'],
                         ['Esencia', '{Materialismo}', '{Marx}']]}],
  'preguntas': [{'pregunta': 'La corriente que sostiene que el conocimiento '
                             'es posible y seguro, sin cuestionamientos, es '
                             'el:',
                 'alternativas': ['Dogmatismo',
                                  'Fenomenalismo',
                                  'Escepticismo',
                                  'Relativismo',
                                  'Criticismo'],
                 'correcta': 'A'},
                {'pregunta': 'El escepticismo niega la posibilidad de '
                             'alcanzar:',
                 'alternativas': ['La percepción',
                                  'La razón',
                                  'Un conocimiento seguro',
                                  'El lenguaje',
                                  'La experiencia'],
                 'correcta': 'C'},
                {'pregunta': 'El representante clásico del escepticismo es:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Pirrón de Elis',
                                  'Berkeley',
                                  'Locke'],
                 'correcta': 'C'},
                {'pregunta': 'La posición intermedia que afirma que el '
                             'conocimiento es posible pero con límites es '
                             'el:',
                 'alternativas': ['Criticismo',
                                  'Dogmatismo',
                                  'Escepticismo',
                                  'Empirismo',
                                  'Idealismo'],
                 'correcta': 'A'},
                {'pregunta': 'El criticismo fue formulado por:',
                 'alternativas': ['Kant',
                                  'Pirrón',
                                  'Hume',
                                  'Hegel',
                                  'Descartes'],
                 'correcta': 'A'},
                {'pregunta': 'Para el racionalismo, el origen del '
                             'conocimiento es:',
                 'alternativas': ['La experiencia',
                                  'La percepción',
                                  'La costumbre',
                                  'La revelación',
                                  'La razón'],
                 'correcta': 'E'},
                {'pregunta': 'El principal representante del empirismo es:',
                 'alternativas': ['John Locke',
                                  'Kant',
                                  'Platón',
                                  'Hegel',
                                  'Descartes'],
                 'correcta': 'A'},
                {'pregunta': '«Los conceptos sin intuiciones son vacíos, las '
                             'intuiciones sin conceptos son ciegas» '
                             'corresponde a:',
                 'alternativas': ['Hume',
                                  'Descartes',
                                  'Locke',
                                  'Berkeley',
                                  'Kant'],
                 'correcta': 'E'},
                {'pregunta': 'La frase «ser es ser percibido» pertenece a:',
                 'alternativas': ['Hume',
                                  'Kant',
                                  'Platón',
                                  'Descartes',
                                  'Berkeley'],
                 'correcta': 'E'},
                {'pregunta': 'El idealismo subjetivo sostiene que la '
                             'realidad depende de:',
                 'alternativas': ['El lenguaje',
                                  'Las leyes físicas',
                                  'La conciencia del sujeto',
                                  'La sociedad',
                                  'La materia'],
                 'correcta': 'C'},
                {'pregunta': 'El idealismo objetivo afirma que existe una '
                             'realidad ideal:',
                 'alternativas': ['Creada por el sujeto',
                                  'Puramente material',
                                  'Sensorial',
                                  'Independiente del sujeto',
                                  'Inexistente'],
                 'correcta': 'D'},
                {'pregunta': 'Las Ideas de Platón y el Espíritu de Hegel son '
                             'ejemplos de:',
                 'alternativas': ['Escepticismo',
                                  'Idealismo subjetivo',
                                  'Materialismo',
                                  'Idealismo objetivo',
                                  'Empirismo'],
                 'correcta': 'D'},
                {'pregunta': 'El materialismo sostiene que lo primario es:',
                 'alternativas': ['La conciencia',
                                  'La idea',
                                  'El espíritu',
                                  'La materia',
                                  'El lenguaje'],
                 'correcta': 'D'},
                {'pregunta': 'El fenomenalismo sostiene que solo conocemos:',
                 'alternativas': ['El noúmeno',
                                  'La cosa en sí',
                                  'Las ideas innatas',
                                  'Los fenómenos',
                                  'La esencia'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo que niega toda posibilidad de '
                             'conocer se denomina:',
                 'alternativas': ['Parcial',
                                  'Metódico',
                                  'Moderado',
                                  'Absoluto',
                                  'Relativo'],
                 'correcta': 'D'},
                {'pregunta': 'El problema de la POSIBILIDAD del conocimiento '
                             'se pregunta si:',
                 'alternativas': ['Para qué sirve el saber',
                                  'Si es posible conocer con certeza',
                                  'Cuál es la esencia del ser',
                                  'Qué es la verdad',
                                  'De dónde proviene el conocimiento'],
                 'correcta': 'B'},
                {'pregunta': 'El problema del ORIGEN del conocimiento se '
                             'pregunta:',
                 'alternativas': ['De dónde proviene el conocimiento',
                                  'Cuál es el fin del hombre',
                                  'Si es posible conocer',
                                  'Qué es lo real',
                                  'Qué es el valor'],
                 'correcta': 'A'},
                {'pregunta': 'Descartes es representante del:',
                 'alternativas': ['Fenomenalismo',
                                  'Escepticismo absoluto',
                                  'Empirismo',
                                  'Materialismo',
                                  'Racionalismo'],
                 'correcta': 'E'},
                {'pregunta': 'El criticismo kantiano supera la oposición '
                             'entre:',
                 'alternativas': ['Dogmatismo y realismo',
                                  'Racionalismo y empirismo',
                                  'Ética y lógica',
                                  'Idealismo y materialismo',
                                  'Ciencia y religión'],
                 'correcta': 'B'},
                {'pregunta': 'Para el materialismo, la conciencia es:',
                 'alternativas': ['Anterior al mundo',
                                  'Un producto de la materia',
                                  'Una sustancia separada',
                                  'Lo primario',
                                  'Independiente del cerebro'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que sostiene que la experiencia '
                             'es la única fuente del conocimiento se llama:',
                 'alternativas': ['Racionalismo',
                                  'Empirismo',
                                  'Criticismo',
                                  'Dogmatismo',
                                  'Idealismo'],
                 'correcta': 'B'},
                {'pregunta': 'El método propio del empirismo es:',
                 'alternativas': ['La deducción',
                                  'La inducción',
                                  'La intuición exclusiva',
                                  'La dialéctica',
                                  'La analogía'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los representantes del empirismo figuran '
                             'Locke, Hume, Berkeley y:',
                 'alternativas': ['Descartes',
                                  'Francisco Bacon',
                                  'Leibniz',
                                  'Spinoza',
                                  'Malebranche'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que sostiene que la razón es la '
                             'única fuente del conocimiento se llama:',
                 'alternativas': ['Empirismo',
                                  'Racionalismo',
                                  'Escepticismo',
                                  'Agnosticismo',
                                  'Fenomenalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El método propio del racionalismo es:',
                 'alternativas': ['La inducción',
                                  'La deducción',
                                  'La observación exclusiva',
                                  'El experimento exclusivo',
                                  'La intuición sensible'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los representantes del racionalismo '
                             'figuran Descartes, Spinoza y:',
                 'alternativas': ['Locke',
                                  'Leibniz',
                                  'Hume',
                                  'Berkeley',
                                  'Bacon'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que sostiene que el conocimiento '
                             'surge de la unión de experiencia y razón se '
                             'llama:',
                 'alternativas': ['Empirismo',
                                  'Criticismo',
                                  'Racionalismo puro',
                                  'Dogmatismo',
                                  'Escepticismo'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del criticismo, autor de la '
                             'frase «no hay experiencia sin razón ni razón '
                             'sin experiencia», fue:',
                 'alternativas': ['Descartes',
                                  'Manuel Kant',
                                  'Locke',
                                  'Hegel',
                                  'Hume'],
                 'correcta': 'B'},
                {'pregunta': 'La postura que admite que el conocimiento sí '
                             'es posible se llama:',
                 'alternativas': ['Escepticismo',
                                  'Dogmatismo',
                                  'Agnosticismo',
                                  'Fenomenalismo',
                                  'Idealismo'],
                 'correcta': 'B'},
                {'pregunta': 'Los representantes del dogmatismo, según el '
                             'texto, fueron los:',
                 'alternativas': ['Sofistas',
                                  'Presocráticos',
                                  'Estoicos',
                                  'Escolásticos',
                                  'Positivistas'],
                 'correcta': 'B'},
                {'pregunta': 'El fundador del escepticismo, quien afirmaba '
                             'que el conocimiento no es posible, fue:',
                 'alternativas': ['Gorgias',
                                  'Pirrón de Elis',
                                  'Protágoras',
                                  'Sócrates',
                                  'Demócrito'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo radical o absoluto, que afirma '
                             'que el conocimiento es imposible, tiene como '
                             'representante a:',
                 'alternativas': ['Protágoras',
                                  'Gorgias',
                                  'Pirrón',
                                  'Sócrates',
                                  'Platón'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo relativo, que afirma que toda '
                             'verdad es relativa, tiene como representante '
                             'a:',
                 'alternativas': ['Gorgias',
                                  'Protágoras',
                                  'Pirrón',
                                  'Heráclito',
                                  'Demócrito'],
                 'correcta': 'B'},
                {'pregunta': 'La postura que admite la imposibilidad de '
                             'conocer la «cosa en sí» se llama:',
                 'alternativas': ['Dogmatismo',
                                  'Agnosticismo',
                                  'Escepticismo radical',
                                  'Materialismo',
                                  'Idealismo objetivo'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del agnosticismo, según el '
                             'texto, fue:',
                 'alternativas': ['Pirrón',
                                  'Manuel Kant',
                                  'Gorgias',
                                  'Protágoras',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que sostiene que el objeto del '
                             'conocimiento no es real sino ideal se llama:',
                 'alternativas': ['Materialismo',
                                  'Idealismo',
                                  'Fenomenalismo',
                                  'Empirismo',
                                  'Dogmatismo'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo subjetivo, que afirma que toda '
                             'realidad está encerrada en la conciencia, '
                             'tiene como representante a:',
                 'alternativas': ['Platón',
                                  'Berkeley',
                                  'Hegel',
                                  'Kant',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo objetivo, que sostiene que las '
                             'ideas existen por sí mismas, tiene como '
                             'representantes a Platón y:',
                 'alternativas': ['Berkeley',
                                  'Hegel',
                                  'Kant',
                                  'Descartes',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'El materialismo sostiene que el criterio de '
                             'verdad del conocimiento es:',
                 'alternativas': ['La fe',
                                  'La praxis',
                                  'La intuición',
                                  'La revelación',
                                  'La autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'El fenomenalismo sostiene que el sujeto solo '
                             'puede captar el fenómeno, mas no:',
                 'alternativas': ['La apariencia',
                                  'La esencia o noúmeno',
                                  'Los sentidos',
                                  'La experiencia',
                                  'El lenguaje'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del fenomenalismo, según el '
                             'texto, fue:',
                 'alternativas': ['Berkeley',
                                  'Manuel Kant',
                                  'Hegel',
                                  'Platón',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'Los representantes del dogmatismo, corriente '
                             'que confía en la posibilidad del conocimiento, '
                             'fueron los:',
                 'alternativas': ['Sofistas',
                                  'Presocráticos',
                                  'Escépticos',
                                  'Estoicos',
                                  'Positivistas'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo radical o absoluto, que niega '
                             'toda posibilidad de conocer, está representado '
                             'por:',
                 'alternativas': ['Protágoras',
                                  'Gorgias',
                                  'Pirrón',
                                  'Sócrates',
                                  'Platón'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo relativo, que sostiene que '
                             'toda verdad es relativa, está representado '
                             'por:',
                 'alternativas': ['Gorgias',
                                  'Protágoras',
                                  'Pirrón',
                                  'Demócrito',
                                  'Heráclito'],
                 'correcta': 'B'},
                {'pregunta': 'Además del criticismo, la imposibilidad de '
                             'conocer la «cosa en sí» también es sostenida, '
                             'bajo el nombre de agnosticismo, por:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Locke',
                                  'Hume',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los representantes del racionalismo, '
                             'además de Descartes, figuran Leibniz, Spinoza '
                             'y:',
                 'alternativas': ['Locke',
                                  'Malebranche',
                                  'Hume',
                                  'Bacon',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los representantes del empirismo, además '
                             'de Locke y Hume, figuran Bacon y:',
                 'alternativas': ['Descartes',
                                  'Berkeley',
                                  'Leibniz',
                                  'Spinoza',
                                  'Malebranche'],
                 'correcta': 'B'},
                {'pregunta': 'Para el materialismo, el criterio de verdad '
                             'del conocimiento es:',
                 'alternativas': ['La fe',
                                  'La praxis',
                                  'La revelación',
                                  'La autoridad',
                                  'La intuición'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del fenomenalismo, que '
                             'sostiene que solo conocemos los fenómenos, es:',
                 'alternativas': ['Berkeley',
                                  'Kant',
                                  'Platón',
                                  'Hegel',
                                  'Locke'],
                 'correcta': 'B'}]},
 {'num': 8,
  'titulo': 'Problema de la ciencia: epistemología',
  'secciones': [{'titulo': '8.1 CONCEPTO',
                 'items': ['Del griego episteme = {ciencia} y logos = '
                           'estudio. Es la disciplina que estudia el '
                           'conocimiento {científico}: su estructura, sus '
                           'métodos y su {validez}.',
                           'Se distingue de la gnoseología porque esta '
                           'estudia el conocimiento {en general} y la '
                           'epistemología solo el {científico}.']},
                {'titulo': '8.2 ESTRUCTURA DE LA CIENCIA',
                 'items': ['{Teoría} científica: conjunto sistemático de '
                           '{leyes} e hipótesis que explican un ámbito de la '
                           'realidad.',
                           '{Ley} científica: enunciado que expresa una '
                           'relación {constante} y necesaria entre '
                           'fenómenos.',
                           '{Hipótesis}: suposición o respuesta provisional '
                           'que debe ser {contrastada}.',
                           '{Axioma}: proposición evidente que se acepta sin '
                           '{demostración}.']},
                {'titulo': '8.3 EL MÉTODO CIENTÍFICO',
                 'items': ['El método {hipotético-deductivo} comprende: '
                           'observación, formulación del {problema}, '
                           'planteamiento de la {hipótesis}, {deducción} de '
                           'consecuencias, {experimentación} y conclusión.',
                           'El método {inductivo} va de lo {particular} a lo '
                           'general; el {deductivo}, de lo {general} a lo '
                           'particular.']},
                {'titulo': '8.4 FUNCIONES Y CLASIFICACIÓN',
                 'items': ['Funciones de la ciencia: {describir}, {explicar} '
                           'y {predecir}.',
                           '{Mario Bunge} clasificó las ciencias en '
                           '{formales} (lógica y matemática, de objeto '
                           'ideal) y {fácticas} (de objeto real).',
                           'Las fácticas se dividen en ciencias {naturales} '
                           '(física, química, biología) y ciencias '
                           '{sociales} (historia, economía, sociología).']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La disciplina que estudia el conocimiento '
                           'científico es la {Epistemología}.',
                           'Etimológicamente, «episteme» significa '
                           '{Ciencia}.',
                           'La diferencia entre gnoseología y epistemología '
                           'es que la primera estudia {El conocimiento en '
                           'general}.',
                           'El conjunto sistemático de leyes e hipótesis que '
                           'explican un ámbito de la realidad es {Una teoría '
                           'científica}.',
                           'El enunciado que expresa una relación constante '
                           'y necesaria entre fenómenos es {La ley '
                           'científica}.',
                           'La suposición provisional que debe ser '
                           'contrastada se denomina {Hipótesis}.',
                           'La proposición evidente que se acepta sin '
                           'demostración es {El axioma}.',
                           'El método que va de lo particular a lo general '
                           'es {Inductivo}.',
                           'El método que va de lo general a lo particular '
                           'es {Deductivo}.',
                           'El método general de la ciencia moderna se '
                           'denomina {Hipotético-deductivo}.',
                           'Mario Bunge clasificó las ciencias en formales y '
                           '{Fácticas}.',
                           'Las ciencias formales tienen como objeto de '
                           'estudio entes {Ideales}.',
                           'Son ciencias formales {Lógica y matemática}.',
                           'La biología pertenece a las ciencias {Fácticas '
                           'naturales}.',
                           'La historia y la economía pertenecen a las '
                           'ciencias {Fácticas sociales}.',
                           'El primer paso del método científico es {La '
                           'observación}.',
                           'La contrastación de una hipótesis se realiza '
                           'mediante {La experimentación}.',
                           'Que la ciencia pueda anticipar hechos futuros '
                           'corresponde a su función {Predictiva}.',
                           'Las ciencias fácticas se caracterizan porque su '
                           'objeto es {Real}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El método científico regula el planteamiento de '
                           'problemas y la puesta a prueba de las '
                           '{hipótesis} formuladas como soluciones.',
                           'La hipótesis es un ensayo preliminar de solución '
                           'que la ciencia espera confirmar mediante la '
                           '{contrastación} empírica.',
                           'La predicción, una de las funciones de la '
                           'ciencia, permite prever situaciones futuras a '
                           'partir de un hecho, ley o {teoría}.']}],
  'cuadros': [{'titulo': '8.4 CLASIFICACIÓN DE LAS CIENCIAS (BUNGE)',
               'encabezados': ['Tipo', 'Objeto', 'Ejemplos'],
               'filas': [['{Formales}', '{Ideal}', '{Lógica} y matemática'],
                         ['Fácticas {naturales}',
                          '{Real}',
                          'Física, química, {biología}'],
                         ['Fácticas {sociales}',
                          'Real',
                          '{Historia}, economía, sociología']]}],
  'preguntas': [{'pregunta': 'La disciplina que estudia el conocimiento '
                             'científico es la:',
                 'alternativas': ['Ontología',
                                  'Lógica',
                                  'Axiología',
                                  'Epistemología',
                                  'Gnoseología'],
                 'correcta': 'D'},
                {'pregunta': 'Etimológicamente, «episteme» significa:',
                 'alternativas': ['Ciencia',
                                  'Ser',
                                  'Alma',
                                  'Valor',
                                  'Palabra'],
                 'correcta': 'A'},
                {'pregunta': 'La diferencia entre gnoseología y '
                             'epistemología es que la primera estudia:',
                 'alternativas': ['Solo la ciencia',
                                  'La conducta',
                                  'Los valores',
                                  'El lenguaje',
                                  'El conocimiento en general'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto sistemático de leyes e hipótesis '
                             'que explican un ámbito de la realidad es:',
                 'alternativas': ['Una observación',
                                  'Una teoría científica',
                                  'Un dato',
                                  'Un axioma',
                                  'Una hipótesis'],
                 'correcta': 'B'},
                {'pregunta': 'El enunciado que expresa una relación '
                             'constante y necesaria entre fenómenos es:',
                 'alternativas': ['El axioma',
                                  'La hipótesis',
                                  'La ley científica',
                                  'La conjetura',
                                  'El postulado'],
                 'correcta': 'C'},
                {'pregunta': 'La suposición provisional que debe ser '
                             'contrastada se denomina:',
                 'alternativas': ['Ley',
                                  'Teoría',
                                  'Corolario',
                                  'Hipótesis',
                                  'Axioma'],
                 'correcta': 'D'},
                {'pregunta': 'La proposición evidente que se acepta sin '
                             'demostración es:',
                 'alternativas': ['El axioma',
                                  'La teoría',
                                  'La ley',
                                  'El teorema',
                                  'La hipótesis'],
                 'correcta': 'A'},
                {'pregunta': 'El método que va de lo particular a lo general '
                             'es:',
                 'alternativas': ['Dialéctico',
                                  'Inductivo',
                                  'Analógico',
                                  'Hermenéutico',
                                  'Deductivo'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo general a lo particular '
                             'es:',
                 'alternativas': ['Estadístico',
                                  'Analógico',
                                  'Comparativo',
                                  'Deductivo',
                                  'Inductivo'],
                 'correcta': 'D'},
                {'pregunta': 'El método general de la ciencia moderna se '
                             'denomina:',
                 'alternativas': ['Hipotético-deductivo',
                                  'Escolástico',
                                  'Intuitivo',
                                  'Dialéctico',
                                  'Fenomenológico'],
                 'correcta': 'A'},
                {'pregunta': 'NO es una función de la ciencia:',
                 'alternativas': ['Explicar',
                                  'Predecir',
                                  'Describir',
                                  'Sistematizar',
                                  'Dogmatizar'],
                 'correcta': 'E'},
                {'pregunta': 'Mario Bunge clasificó las ciencias en formales '
                             'y:',
                 'alternativas': ['Humanas',
                                  'Exactas',
                                  'Puras',
                                  'Fácticas',
                                  'Aplicadas'],
                 'correcta': 'D'},
                {'pregunta': 'Las ciencias formales tienen como objeto de '
                             'estudio entes:',
                 'alternativas': ['Sociales',
                                  'Ideales',
                                  'Reales',
                                  'Materiales',
                                  'Naturales'],
                 'correcta': 'B'},
                {'pregunta': 'Son ciencias formales:',
                 'alternativas': ['Lógica y matemática',
                                  'Física y química',
                                  'Biología y geología',
                                  'Psicología y sociología',
                                  'Historia y economía'],
                 'correcta': 'A'},
                {'pregunta': 'La biología pertenece a las ciencias:',
                 'alternativas': ['Formales',
                                  'Ideales',
                                  'Aplicadas exclusivamente',
                                  'Fácticas sociales',
                                  'Fácticas naturales'],
                 'correcta': 'E'},
                {'pregunta': 'La historia y la economía pertenecen a las '
                             'ciencias:',
                 'alternativas': ['Fácticas naturales',
                                  'Formales',
                                  'Fácticas sociales',
                                  'Exactas',
                                  'Puras'],
                 'correcta': 'C'},
                {'pregunta': 'El primer paso del método científico es:',
                 'alternativas': ['La observación',
                                  'La experimentación',
                                  'La conclusión',
                                  'La hipótesis',
                                  'La ley'],
                 'correcta': 'A'},
                {'pregunta': 'La contrastación de una hipótesis se realiza '
                             'mediante:',
                 'alternativas': ['La autoridad',
                                  'La revelación',
                                  'La experimentación',
                                  'La tradición',
                                  'La intuición'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ciencia pueda anticipar hechos futuros '
                             'corresponde a su función:',
                 'alternativas': ['Normativa',
                                  'Estética',
                                  'Descriptiva',
                                  'Explicativa',
                                  'Predictiva'],
                 'correcta': 'E'},
                {'pregunta': 'Las ciencias fácticas se caracterizan porque '
                             'su objeto es:',
                 'alternativas': ['Ideal',
                                  'Formal',
                                  'Real',
                                  'Abstracto puro',
                                  'Simbólico'],
                 'correcta': 'C'}]},
 {'num': 9,
  'titulo': 'Problema del valor y la ética',
  'secciones': [{'titulo': '9.1 AXIOLOGÍA',
                 'items': ['Del griego axios = {valor} y logos = estudio. Es '
                           'la disciplina filosófica que estudia los '
                           '{valores}.',
                           'El {acto valorativo} es el proceso por el cual '
                           'el sujeto atribuye un valor a un objeto o '
                           'conducta.']},
                {'titulo': '9.2 CARACTERÍSTICAS Y CLASIFICACIÓN',
                 'items': ['Características de los valores: {polaridad} '
                           '(todo valor tiene su contravalor: bueno-malo), '
                           '{jerarquía} (unos valen más que otros), '
                           '{materia} y {objetividad} o subjetividad según '
                           'la corriente.',
                           '{Max Scheler} clasificó los valores en '
                           'jerarquía: sensibles, {vitales}, espirituales y '
                           '{religiosos}.',
                           'Valores éticos fundamentales: el {bien}, la '
                           '{justicia}, la {dignidad} y la {solidaridad}.']},
                {'titulo': '9.3 TEORÍAS DEL VALOR',
                 'items': ['{Subjetivismo}: el valor depende del {sujeto}, '
                           'de su agrado o interés; no existe fuera de la '
                           'valoración.',
                           '{Objetivismo}: los valores existen '
                           '{independientemente} del sujeto; se descubren, '
                           'no se crean.',
                           '{Relacionismo}: el valor surge de la {relación} '
                           'entre el sujeto y el objeto.',
                           '{Socioculturalismo}: los valores son producto de '
                           'la {sociedad} y la cultura, y varían '
                           'históricamente.']},
                {'titulo': '9.4 LA ÉTICA Y LA MORAL',
                 'items': ['La {ética} es la disciplina filosófica que '
                           'reflexiona sobre la {moral}; es teórica.',
                           'La {moral} es el conjunto de normas y costumbres '
                           'concretas de una sociedad; es {práctica}.',
                           'Corrientes éticas: el {eudemonismo} de '
                           '{Aristóteles} (el fin es la {felicidad}), la '
                           'ética {kantiana} del deber, y el {utilitarismo} '
                           'de Stuart {Mill} (la mayor felicidad para el '
                           'mayor {número}).']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La disciplina filosófica que estudia los valores '
                           'es la {Axiología}.',
                           'Etimológicamente, «axios» significa {Valor}.',
                           'Que todo valor tenga su contravalor corresponde '
                           'a la característica de {Polaridad}.',
                           'Que unos valores valgan más que otros '
                           'corresponde a la característica de {Jerarquía}.',
                           'La jerarquía de valores en sensibles, vitales, '
                           'espirituales y religiosos fue propuesta por {Max '
                           'Scheler}.',
                           'Para el subjetivismo, el valor depende de {El '
                           'sujeto que valora}.',
                           'Para el objetivismo, los valores {Existen '
                           'independientemente del sujeto}.',
                           'La teoría según la cual el valor surge de la '
                           'relación entre sujeto y objeto es el '
                           '{Relacionismo}.',
                           'El socioculturalismo sostiene que los valores '
                           'son producto de {La sociedad y la cultura}.',
                           'La disciplina filosófica que reflexiona '
                           'teóricamente sobre la moral es la {Ética}.',
                           'El conjunto de normas y costumbres concretas de '
                           'una sociedad constituye la {Moral}.',
                           'La diferencia entre ética y moral es que la '
                           'ética es {Teórica y la moral práctica}.',
                           'El eudemonismo, que sitúa el fin de la vida en '
                           'la felicidad, corresponde a {Aristóteles}.',
                           'La ética del deber fue formulada por {Kant}.',
                           'El utilitarismo, que busca la mayor felicidad '
                           'para el mayor número, se asocia a {Stuart Mill}.',
                           'El proceso por el cual el sujeto atribuye un '
                           'valor a algo se denomina {Acto valorativo}.',
                           'En la jerarquía de Scheler, el valor más alto '
                           'corresponde a los valores {Religiosos}.',
                           'Para Kant, una acción es moralmente valiosa '
                           'cuando se realiza {Por deber}.',
                           'La afirmación «los valores cambian según la '
                           'época y la cultura» corresponde al '
                           '{Socioculturalismo}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La axiología, del griego axios (valor) y logos '
                           '(tratado), estudia la forma, el significado y el '
                           'fundamento de los juicios {valorativos}.',
                           'El eudemonismo de Aristóteles considera la '
                           'felicidad como la meta suprema de la actividad '
                           '{moral} del hombre.',
                           'Para Aristóteles, la virtud es el equilibrio '
                           'entre el exceso y el defecto: la ley del '
                           '{término medio}.',
                           'Los utilitaristas Bentham y Stuart Mill '
                           'defendían la felicidad de la {mayoría}, sin '
                           'admitir una versión egoísta del bien.',
                           'El imperativo categórico de Kant exige obrar de '
                           'tal modo que la acción pueda convertirse en {ley '
                           'universal}.',
                           'El bien es considerado el valor supremo de la '
                           'persona, según Sócrates y Platón, y de la '
                           'sociedad, según {John Stuart Mill}.',
                           'Aristóteles distinguió la justicia general, '
                           'referida al Estado, de la justicia {particular}, '
                           'referida a los individuos.']}],
  'cuadros': [{'titulo': '9.4 CORRIENTES ÉTICAS',
               'encabezados': ['Corriente', 'Representante', 'Fin moral'],
               'filas': [['{Eudemonismo}', '{Aristóteles}', 'La {felicidad}'],
                         ['Ética del {deber}', '{Kant}', 'Obrar por {deber}'],
                         ['{Utilitarismo}',
                          'Stuart {Mill}',
                          'Mayor felicidad del mayor {número}']]}],
  'preguntas': [{'pregunta': 'La disciplina filosófica que estudia los '
                             'valores es la:',
                 'alternativas': ['Estética',
                                  'Gnoseología',
                                  'Ontología',
                                  'Axiología',
                                  'Ética'],
                 'correcta': 'D'},
                {'pregunta': 'Etimológicamente, «axios» significa:',
                 'alternativas': ['Ley', 'Bien', 'Fin', 'Costumbre', 'Valor'],
                 'correcta': 'E'},
                {'pregunta': 'Que todo valor tenga su contravalor '
                             'corresponde a la característica de:',
                 'alternativas': ['Materia',
                                  'Polaridad',
                                  'Jerarquía',
                                  'Objetividad',
                                  'Historicidad'],
                 'correcta': 'B'},
                {'pregunta': 'Que unos valores valgan más que otros '
                             'corresponde a la característica de:',
                 'alternativas': ['Jerarquía',
                                  'Relatividad',
                                  'Universalidad',
                                  'Subjetividad',
                                  'Polaridad'],
                 'correcta': 'A'},
                {'pregunta': 'La jerarquía de valores en sensibles, vitales, '
                             'espirituales y religiosos fue propuesta por:',
                 'alternativas': ['Aristóteles',
                                  'Max Scheler',
                                  'Kant',
                                  'Stuart Mill',
                                  'Nietzsche'],
                 'correcta': 'B'},
                {'pregunta': 'Para el subjetivismo, el valor depende de:',
                 'alternativas': ['El sujeto que valora',
                                  'La sociedad',
                                  'La razón pura',
                                  'El objeto',
                                  'Dios'],
                 'correcta': 'A'},
                {'pregunta': 'Para el objetivismo, los valores:',
                 'alternativas': ['Son ilusiones',
                                  'Existen independientemente del sujeto',
                                  'Los crea el sujeto',
                                  'Varían con la moda',
                                  'No existen'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría según la cual el valor surge de la '
                             'relación entre sujeto y objeto es el:',
                 'alternativas': ['Formalismo',
                                  'Objetivismo',
                                  'Nihilismo',
                                  'Relacionismo',
                                  'Subjetivismo'],
                 'correcta': 'D'},
                {'pregunta': 'El socioculturalismo sostiene que los valores '
                             'son producto de:',
                 'alternativas': ['La revelación',
                                  'La razón individual',
                                  'La naturaleza biológica',
                                  'La sociedad y la cultura',
                                  'El azar'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina filosófica que reflexiona '
                             'teóricamente sobre la moral es la:',
                 'alternativas': ['Política',
                                  'Moral',
                                  'Ética',
                                  'Estética',
                                  'Axiología'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de normas y costumbres concretas '
                             'de una sociedad constituye la:',
                 'alternativas': ['Estética',
                                  'Ética',
                                  'Ciencia',
                                  'Moral',
                                  'Lógica'],
                 'correcta': 'D'},
                {'pregunta': 'La diferencia entre ética y moral es que la '
                             'ética es:',
                 'alternativas': ['Práctica y la moral teórica',
                                  'Estética',
                                  'Teórica y la moral práctica',
                                  'Religiosa',
                                  'Legal'],
                 'correcta': 'C'},
                {'pregunta': 'El eudemonismo, que sitúa el fin de la vida en '
                             'la felicidad, corresponde a:',
                 'alternativas': ['Epicuro',
                                  'Stuart Mill',
                                  'Aristóteles',
                                  'Nietzsche',
                                  'Kant'],
                 'correcta': 'C'},
                {'pregunta': 'La ética del deber fue formulada por:',
                 'alternativas': ['Mill',
                                  'Kant',
                                  'Aristóteles',
                                  'Bentham',
                                  'Scheler'],
                 'correcta': 'B'},
                {'pregunta': 'El utilitarismo, que busca la mayor felicidad '
                             'para el mayor número, se asocia a:',
                 'alternativas': ['Kant',
                                  'Platón',
                                  'Sócrates',
                                  'Aristóteles',
                                  'Stuart Mill'],
                 'correcta': 'E'},
                {'pregunta': 'NO es un valor ético fundamental:',
                 'alternativas': ['La justicia',
                                  'El bien',
                                  'La dignidad',
                                  'La rentabilidad',
                                  'La solidaridad'],
                 'correcta': 'D'},
                {'pregunta': 'El proceso por el cual el sujeto atribuye un '
                             'valor a algo se denomina:',
                 'alternativas': ['Deducción',
                                  'Acto valorativo',
                                  'Percepción',
                                  'Inferencia',
                                  'Juicio lógico'],
                 'correcta': 'B'},
                {'pregunta': 'En la jerarquía de Scheler, el valor más alto '
                             'corresponde a los valores:',
                 'alternativas': ['Religiosos',
                                  'Vitales',
                                  'Útiles',
                                  'Económicos',
                                  'Sensibles'],
                 'correcta': 'A'},
                {'pregunta': 'Para Kant, una acción es moralmente valiosa '
                             'cuando se realiza:',
                 'alternativas': ['Por deber',
                                  'Por interés',
                                  'Por placer',
                                  'Por miedo',
                                  'Por costumbre'],
                 'correcta': 'A'},
                {'pregunta': 'La afirmación «los valores cambian según la '
                             'época y la cultura» corresponde al:',
                 'alternativas': ['Socioculturalismo',
                                  'Objetivismo',
                                  'Racionalismo',
                                  'Formalismo',
                                  'Absolutismo moral'],
                 'correcta': 'A'}]},
 {'num': 10,
  'titulo': 'Lógica, lenguaje y pensamiento',
  'secciones': [{'titulo': '10.1 DEFINICIÓN Y RAMAS',
                 'items': ['La {lógica} es la ciencia formal que estudia la '
                           '{validez} o corrección de los razonamientos.',
                           'Estudia la {forma} del razonamiento, no su '
                           'contenido ni su verdad {material}.',
                           'Ramas: la lógica {formal} clásica '
                           '(aristotélica), la lógica {proposicional} y la '
                           'lógica de {clases}.']},
                {'titulo': '10.2 HISTORIA DE LA LÓGICA',
                 'items': ['{Aristóteles} es el fundador de la lógica; su '
                           'obra se reunió bajo el nombre de «{Órganon}».',
                           'En la lógica medieval destaca {Porfirio} de Tiro '
                           'con su «Isagoge» y el {árbol} de Porfirio.',
                           'La lógica {moderna} o simbólica emplea símbolos '
                           'matemáticos; destacan {Boole}, Frege y Russell.',
                           'En el Perú destaca {Francisco Miró Quesada} '
                           'Cantuarias, quien acuñó el término «lógica '
                           '{jurídica}».']},
                {'titulo': '10.3 FUNCIONES BÁSICAS DEL LENGUAJE',
                 'items': ['Función {informativa} o descriptiva: transmite '
                           'información; puede ser {verdadera} o falsa.',
                           'Función {expresiva}: manifiesta {emociones} y '
                           'sentimientos; no es verdadera ni falsa.',
                           'Función {directiva}: busca provocar una '
                           '{conducta}; órdenes, ruegos y pedidos.']},
                {'titulo': '10.4 LENGUAJE NATURAL Y FORMALIZADO',
                 'items': ['El lenguaje {natural} es el de uso cotidiano; es '
                           'rico pero {ambiguo} y vago.',
                           'El lenguaje {formalizado} usa símbolos, es '
                           '{preciso}, unívoco y sin ambigüedad.',
                           'La {argumentación} es el conjunto de razones '
                           '(premisas) que sustentan una {conclusión}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La lógica es la ciencia formal que estudia {La '
                           'validez o corrección de los razonamientos}.',
                           'La lógica estudia de los razonamientos su '
                           '{Forma}.',
                           'El fundador de la lógica es {Aristóteles}.',
                           'La obra lógica de Aristóteles se reunió bajo el '
                           'nombre de {Órganon}.',
                           'El «árbol» que ordena géneros y especies fue '
                           'elaborado por {Porfirio de Tiro}.',
                           'La lógica moderna o simbólica se caracteriza por '
                           'emplear {Símbolos matemáticos}.',
                           'El filósofo peruano destacado en lógica jurídica '
                           'es {Francisco Miró Quesada Cantuarias}.',
                           'La función del lenguaje que transmite '
                           'información y puede ser verdadera o falsa es la '
                           '{Informativa}.',
                           'La función del lenguaje que manifiesta emociones '
                           'es la {Expresiva}.',
                           'El lenguaje natural se caracteriza por ser '
                           '{Ambiguo y vago}.',
                           'El lenguaje formalizado se caracteriza por ser '
                           '{Preciso y unívoco}.',
                           'El conjunto de razones que sustentan una '
                           'conclusión constituye {Una argumentación}.',
                           'Las ramas principales de la lógica son la formal '
                           'clásica, la proposicional y la de {Clases}.',
                           'En una argumentación, las razones que sustentan '
                           'se denominan {Premisas}.',
                           'La lógica se clasifica como una ciencia '
                           '{Formal}.',
                           'La «Isagoge» fue escrita por {Porfirio de '
                           'Tiro}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El punto de partida de la lógica formal se '
                           'encuentra en los trabajos de {Aristóteles} sobre '
                           'la silogística.',
                           'A Aristóteles se le atribuye la obra «{el '
                           'Organon}», un conjunto de tratados lógicos.',
                           'Leibniz propuso que algunas verdades son '
                           '{tautológicas}, y desarrolló la idea de '
                           'proposiciones idénticas.',
                           'Giuseppe Peano publicó el «{Formulario '
                           'Matemático}», obra que influyó directamente en '
                           'el proyecto de Russell y Whitehead.',
                           'Bertrand Russell y Whitehead culminaron su '
                           'proyecto lógico en la obra «{Principia '
                           'Mathematica}», publicada en tres volúmenes.',
                           'Wittgenstein introdujo el método de las {tablas '
                           'de verdad} para evaluar los esquemas '
                           'moleculares.',
                           'El lógico polaco {Lukasiewicz} perteneció al '
                           'Círculo de Viena y estudió la silogística '
                           'aristotélica desde la lógica matemática.',
                           'Las tres funciones básicas del lenguaje son '
                           'informativa, expresiva y {directiva}.']}],
  'cuadros': [{'titulo': '10.3 FUNCIONES DEL LENGUAJE',
               'encabezados': ['Función', 'Finalidad', '¿Verdadera o falsa?'],
               'filas': [['{Informativa}',
                          'Transmitir {información}',
                          '{Sí}'],
                         ['{Expresiva}', 'Manifestar {emociones}', '{No}'],
                         ['{Directiva}', 'Provocar una {conducta}', 'No']]}],
  'preguntas': [{'pregunta': 'La lógica es la ciencia formal que estudia:',
                 'alternativas': ['El lenguaje literario',
                                  'El origen del conocimiento',
                                  'La validez o corrección de los '
                                  'razonamientos',
                                  'Los valores morales',
                                  'La verdad de los hechos'],
                 'correcta': 'C'},
                {'pregunta': 'La lógica estudia de los razonamientos su:',
                 'alternativas': ['Utilidad',
                                  'Forma',
                                  'Origen histórico',
                                  'Contenido',
                                  'Belleza'],
                 'correcta': 'B'},
                {'pregunta': 'El fundador de la lógica es:',
                 'alternativas': ['Porfirio',
                                  'Boole',
                                  'Aristóteles',
                                  'Frege',
                                  'Platón'],
                 'correcta': 'C'},
                {'pregunta': 'La obra lógica de Aristóteles se reunió bajo '
                             'el nombre de:',
                 'alternativas': ['Isagoge',
                                  'República',
                                  'Metafísica',
                                  'Órganon',
                                  'Principia'],
                 'correcta': 'D'},
                {'pregunta': 'El «árbol» que ordena géneros y especies fue '
                             'elaborado por:',
                 'alternativas': ['Frege',
                                  'Russell',
                                  'Boole',
                                  'Aristóteles',
                                  'Porfirio de Tiro'],
                 'correcta': 'E'},
                {'pregunta': 'La lógica moderna o simbólica se caracteriza '
                             'por emplear:',
                 'alternativas': ['Metáforas',
                                  'Silogismos únicamente',
                                  'Símbolos matemáticos',
                                  'Ejemplos históricos',
                                  'Lenguaje natural'],
                 'correcta': 'C'},
                {'pregunta': 'El filósofo peruano destacado en lógica '
                             'jurídica es:',
                 'alternativas': ['Deustua',
                                  'Salazar Bondy',
                                  'Mariátegui',
                                  'Francisco Miró Quesada Cantuarias',
                                  'Antenor Orrego'],
                 'correcta': 'D'},
                {'pregunta': 'La función del lenguaje que transmite '
                             'información y puede ser verdadera o falsa es '
                             'la:',
                 'alternativas': ['Fática',
                                  'Directiva',
                                  'Poética',
                                  'Informativa',
                                  'Expresiva'],
                 'correcta': 'D'},
                {'pregunta': 'La función del lenguaje que manifiesta '
                             'emociones es la:',
                 'alternativas': ['Informativa',
                                  'Metalingüística',
                                  'Descriptiva',
                                  'Directiva',
                                  'Expresiva'],
                 'correcta': 'E'},
                {'pregunta': '«Cierra la puerta» corresponde a la función:',
                 'alternativas': ['Expresiva',
                                  'Directiva',
                                  'Descriptiva',
                                  'Informativa',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': '«¡Qué hermoso atardecer!» corresponde a la '
                             'función:',
                 'alternativas': ['Directiva',
                                  'Referencial',
                                  'Apelativa',
                                  'Informativa',
                                  'Expresiva'],
                 'correcta': 'E'},
                {'pregunta': '«El Cusco está en el Perú» corresponde a la '
                             'función:',
                 'alternativas': ['Directiva',
                                  'Emotiva',
                                  'Poética',
                                  'Expresiva',
                                  'Informativa'],
                 'correcta': 'E'},
                {'pregunta': 'El lenguaje natural se caracteriza por ser:',
                 'alternativas': ['Artificial',
                                  'Ambiguo y vago',
                                  'Unívoco',
                                  'Simbólico',
                                  'Preciso'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje formalizado se caracteriza por '
                             'ser:',
                 'alternativas': ['Preciso y unívoco',
                                  'Literario',
                                  'Ambiguo',
                                  'Coloquial',
                                  'Emotivo'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de razones que sustentan una '
                             'conclusión constituye:',
                 'alternativas': ['Una narración',
                                  'Una descripción',
                                  'Una argumentación',
                                  'Una orden',
                                  'Una exclamación'],
                 'correcta': 'C'},
                {'pregunta': 'Las ramas principales de la lógica son la '
                             'formal clásica, la proposicional y la de:',
                 'alternativas': ['Predicados exclusivamente',
                                  'Números',
                                  'Clases',
                                  'Conjuntos',
                                  'Relaciones'],
                 'correcta': 'C'},
                {'pregunta': 'Las expresiones directivas NO pueden ser '
                             'calificadas como:',
                 'alternativas': ['Claras u oscuras',
                                  'Corteses o descorteses',
                                  'Correctas o incorrectas',
                                  'Verdaderas o falsas',
                                  'Útiles o inútiles'],
                 'correcta': 'D'},
                {'pregunta': 'En una argumentación, las razones que '
                             'sustentan se denominan:',
                 'alternativas': ['Corolarios',
                                  'Premisas',
                                  'Falacias',
                                  'Axiomas',
                                  'Conclusiones'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica se clasifica como una ciencia:',
                 'alternativas': ['Fáctica social',
                                  'Aplicada',
                                  'Experimental',
                                  'Fáctica natural',
                                  'Formal'],
                 'correcta': 'E'},
                {'pregunta': 'La «Isagoge» fue escrita por:',
                 'alternativas': ['Aristóteles',
                                  'Frege',
                                  'Boecio',
                                  'Boole',
                                  'Porfirio de Tiro'],
                 'correcta': 'E'}]},
 {'num': 11,
  'titulo': 'Falacias',
  'secciones': [{'titulo': '11.1 FALACIAS FORMALES',
                 'items': ['Una {falacia} es un razonamiento que parece '
                           'válido pero no lo es.',
                           'Las falacias {formales} tienen un error en la '
                           '{estructura} o forma del razonamiento.']},
                {'titulo': '11.2 FALACIAS DE ATINENCIA',
                 'items': ['Se cometen cuando las premisas no son '
                           '{pertinentes} para la conclusión.',
                           '{Ignoratio elenchi} o conclusión inatinente: se '
                           'prueba una conclusión {diferente} de la que se '
                           'pretendía.',
                           '{Causa falsa}: concluir que un hecho causa otro '
                           'solo porque lo {precede}. Ejemplo: «me levanté '
                           'con el pie izquierdo, hoy será un mal día».',
                           '{Ad populum}: apelación emocional al {pueblo} o '
                           'a la galería. Recurso favorito de propagandistas '
                           'y {demagogos}.',
                           '{Ad hominem}: se ataca a la {persona} en vez de '
                           'refutar su argumento. Puede ser {ofensivo} o '
                           '{circunstancial}.',
                           '{Ad ignorantiam}: afirmar que algo es verdadero '
                           'porque no se ha demostrado su {falsedad}.',
                           '{Ad báculum}: apelación a la {fuerza} o a la '
                           'amenaza. «La fuerza hace el {derecho}».',
                           '{Ad verecundiam}: apelación a una {autoridad} '
                           'fuera de su ámbito de especialidad.']},
                {'titulo': '11.3 FALACIAS DE AMBIGÜEDAD',
                 'items': ['Aparecen cuando el razonamiento contiene '
                           'palabras o frases {ambiguas}.',
                           '{Equívoco}: se usa una palabra con dos o más '
                           '{significados} distintos en el mismo '
                           'razonamiento.',
                           '{Anfibología}: la ambigüedad proviene de la '
                           '{construcción} gramatical de la frase.',
                           '{Énfasis}: el significado cambia según la '
                           'palabra que se {acentúa} o destaca.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['Una falacia es un razonamiento que {Parece '
                           'válido pero no lo es}.',
                           'Las falacias formales tienen un error en {La '
                           'estructura del razonamiento}.',
                           'Las falacias de atinencia se cometen cuando las '
                           'premisas {No son pertinentes para la '
                           'conclusión}.',
                           'Cuando un razonamiento prueba una conclusión '
                           'distinta de la que pretendía, se comete '
                           '{Ignoratio elenchi}.',
                           'La falacia ad hominem del tipo ofensivo consiste '
                           'en {Atacar a quien hace la afirmación}.',
                           'La falacia que aprovecha las circunstancias '
                           'personales del adversario es la ad hominem '
                           '{Circunstancial}.',
                           'Las falacias de ambigüedad se producen cuando el '
                           'razonamiento contiene {Palabras o frases '
                           'ambiguas}.',
                           'Usar la palabra «banco» con dos significados '
                           'distintos en un mismo razonamiento es una '
                           'falacia de {Equívoco}.',
                           'Cuando la ambigüedad proviene de la construcción '
                           'gramatical se comete {Anfibología}.',
                           'Cuando el significado cambia según la palabra '
                           'acentuada se comete la falacia de {Énfasis}.',
                           'El recurso favorito de propagandistas y '
                           'demagogos es la falacia {Ad populum}.',
                           'La falacia ad verecundiam se comete al apelar a '
                           'una autoridad {Fuera de su ámbito de '
                           'especialidad}.',
                           'Confundir la simple sucesión temporal con una '
                           'relación causal corresponde a la falacia de '
                           '{Causa falsa}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Las falacias se dividen en dos grandes tipos: '
                           '{formales} y no formales.',
                           'Las falacias no formales, del lenguaje común, se '
                           'dividen en falacias de atinencia y de '
                           '{ambigüedad}.',
                           'Las falacias formales se cometen cuando se viola '
                           'alguna de las leyes de la {lógica clásica}.']}],
  'cuadros': [{'titulo': '11.2 FALACIAS DE ATINENCIA',
               'encabezados': ['Falacia', 'En qué consiste'],
               'filas': [['{Ad hominem}', 'Atacar a la {persona}'],
                         ['{Ad populum}',
                          'Apelar al {pueblo} emocionalmente'],
                         ['{Ad báculum}', 'Apelar a la {fuerza}'],
                         ['{Ad verecundiam}',
                          'Apelar a una {autoridad} inapropiada'],
                         ['{Ad ignorantiam}', 'Apelar a la {ignorancia}'],
                         ['{Causa falsa}',
                          'Confundir sucesión con {causa}']]}],
  'preguntas': [{'pregunta': 'Una falacia es un razonamiento que:',
                 'alternativas': ['No tiene conclusión',
                                  'Es formalmente correcto',
                                  'Siempre es verdadero',
                                  'Carece de premisas',
                                  'Parece válido pero no lo es'],
                 'correcta': 'E'},
                {'pregunta': 'Las falacias formales tienen un error en:',
                 'alternativas': ['La estructura del razonamiento',
                                  'Las premisas verdaderas',
                                  'La ortografía',
                                  'El contenido',
                                  'El vocabulario'],
                 'correcta': 'A'},
                {'pregunta': 'Las falacias de atinencia se cometen cuando '
                             'las premisas:',
                 'alternativas': ['Son numerosas',
                                  'Están bien formuladas',
                                  'No son pertinentes para la conclusión',
                                  'Son evidentes',
                                  'Son verdaderas'],
                 'correcta': 'C'},
                {'pregunta': '«No debemos creer en las teorías de Marx, '
                             'recuerda que fue comunista» es una falacia:',
                 'alternativas': ['Ad báculum',
                                  'De equívoco',
                                  'Ad populum',
                                  'Ad ignorantiam',
                                  'Ad hominem'],
                 'correcta': 'E'},
                {'pregunta': '«Dios existe, porque nadie ha demostrado su '
                             'inexistencia» es una falacia:',
                 'alternativas': ['Ad hominem',
                                  'Ad populum',
                                  'Ad ignorantiam',
                                  'Ad verecundiam',
                                  'Causa falsa'],
                 'correcta': 'C'},
                {'pregunta': '«Si presenta un reclamo, su permanencia en la '
                             'empresa puede acortarse» es una falacia:',
                 'alternativas': ['Ad hominem',
                                  'De énfasis',
                                  'Ad báculum',
                                  'Ad populum',
                                  'Ignoratio elenchi'],
                 'correcta': 'C'},
                {'pregunta': '«Este jabón es bueno, lo usa un cantante '
                             'famoso» es una falacia:',
                 'alternativas': ['Ad populum',
                                  'Ad báculum',
                                  'Ad verecundiam',
                                  'Causa falsa',
                                  'Anfibología'],
                 'correcta': 'C'},
                {'pregunta': '«Tome esta bebida, lo nuestro está primero» es '
                             'una falacia:',
                 'alternativas': ['Ad báculum',
                                  'Ad populum',
                                  'De equívoco',
                                  'Ad ignorantiam',
                                  'Ad hominem'],
                 'correcta': 'B'},
                {'pregunta': '«Me levanté con el pie izquierdo, hoy será un '
                             'mal día» es una falacia de:',
                 'alternativas': ['Causa falsa',
                                  'Ambigüedad',
                                  'Fuerza',
                                  'Ignorancia',
                                  'Autoridad'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando un razonamiento prueba una conclusión '
                             'distinta de la que pretendía, se comete:',
                 'alternativas': ['Ignoratio elenchi',
                                  'Ad báculum',
                                  'Énfasis',
                                  'Ad hominem',
                                  'Equívoco'],
                 'correcta': 'A'},
                {'pregunta': 'La falacia ad hominem del tipo ofensivo '
                             'consiste en:',
                 'alternativas': ['Apelar al pueblo',
                                  'Citar una autoridad',
                                  'Usar palabras ambiguas',
                                  'Atacar a quien hace la afirmación',
                                  'Apelar a la fuerza'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia que aprovecha las circunstancias '
                             'personales del adversario es la ad hominem:',
                 'alternativas': ['Circunstancial',
                                  'Emotiva',
                                  'Directa',
                                  'Ofensiva',
                                  'Formal'],
                 'correcta': 'A'},
                {'pregunta': 'Las falacias de ambigüedad se producen cuando '
                             'el razonamiento contiene:',
                 'alternativas': ['Conclusiones falsas',
                                  'Palabras o frases ambiguas',
                                  'Citas de autoridad',
                                  'Muchas premisas',
                                  'Datos numéricos'],
                 'correcta': 'B'},
                {'pregunta': 'Usar la palabra «banco» con dos significados '
                             'distintos en un mismo razonamiento es una '
                             'falacia de:',
                 'alternativas': ['Causa falsa',
                                  'Autoridad',
                                  'Énfasis',
                                  'Anfibología',
                                  'Equívoco'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando la ambigüedad proviene de la '
                             'construcción gramatical se comete:',
                 'alternativas': ['Equívoco',
                                  'Énfasis',
                                  'Ad báculum',
                                  'Ad populum',
                                  'Anfibología'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando el significado cambia según la palabra '
                             'acentuada se comete la falacia de:',
                 'alternativas': ['Anfibología',
                                  'Causa falsa',
                                  'Equívoco',
                                  'Ignoratio elenchi',
                                  'Énfasis'],
                 'correcta': 'E'},
                {'pregunta': 'El recurso favorito de propagandistas y '
                             'demagogos es la falacia:',
                 'alternativas': ['De equívoco',
                                  'Ad verecundiam',
                                  'Ad báculum',
                                  'Formal',
                                  'Ad populum'],
                 'correcta': 'E'},
                {'pregunta': '«La fuerza hace el derecho» resume la falacia:',
                 'alternativas': ['Ad hominem',
                                  'Ad báculum',
                                  'De énfasis',
                                  'Ad ignorantiam',
                                  'Ad populum'],
                 'correcta': 'B'},
                {'pregunta': 'La falacia ad verecundiam se comete al apelar '
                             'a una autoridad:',
                 'alternativas': ['Reconocida en su campo',
                                  'Fuera de su ámbito de especialidad',
                                  'Legítima',
                                  'Académica',
                                  'Científica'],
                 'correcta': 'B'},
                {'pregunta': 'Confundir la simple sucesión temporal con una '
                             'relación causal corresponde a la falacia de:',
                 'alternativas': ['Ad báculum',
                                  'Causa falsa',
                                  'Anfibología',
                                  'Ad populum',
                                  'Equívoco'],
                 'correcta': 'B'}]},
 {'num': 12,
  'titulo': 'Pruebas formales en la lógica proposicional',
  'secciones': [{'titulo': '12.1 LA PROPOSICIÓN',
                 'items': ['Es todo enunciado del que se puede afirmar que '
                           'es {verdadero} o {falso}.',
                           'No son proposiciones las {preguntas}, las '
                           '{órdenes}, los deseos ni las {exclamaciones}.',
                           'Proposición {simple} o atómica: no contiene '
                           'ningún {operador} lógico. Se representa con una '
                           'sola {variable}.',
                           'Proposición {compuesta} o molecular: contiene '
                           'uno o más {operadores}.']},
                {'titulo': '12.2 SIGNOS LÓGICOS',
                 'items': ['{Variables}: representan proposiciones simples; '
                           'se usan las letras minúsculas {p}, q, r, s.',
                           'Conectores {monádicos}: afectan a una sola '
                           'variable. El único es la {negación} (~).',
                           'Conectores {diádicos} o binarios: unen dos '
                           'variables. Son la {conjunción}, la disyunción '
                           '{débil}, la disyunción {fuerte}, la '
                           '{condicional} y la {bicondicional}.',
                           'Símbolos {auxiliares}: paréntesis, corchetes y '
                           '{llaves}, que sirven para agrupar.']},
                {'titulo': '12.3 FORMALIZACIÓN',
                 'items': ['Fórmula {atómica}: se representa con una sola '
                           'variable. Ejemplo: «El asno es vertebrado» = '
                           '{p}.',
                           'Fórmula {molecular}: contiene uno o más '
                           'operadores. Ejemplo: «El zorrino no es mamífero» '
                           '= {~p}.',
                           '«La vaca es mamífero y el caballo también» se '
                           'formaliza como {p ∧ q}.',
                           '«El asno es mamífero pero el loro no» se '
                           'formaliza como {p ∧ ~q}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['Una proposición es todo enunciado del que se '
                           'puede afirmar que es {Verdadero o falso}.',
                           'La proposición que no contiene ningún operador '
                           'lógico se denomina {Simple o atómica}.',
                           'La proposición que contiene uno o más operadores '
                           'se denomina {Compuesta o molecular}.',
                           'Las variables proposicionales se representan con '
                           '{Letras minúsculas p, q, r, s}.',
                           'El único conector monádico de la lógica '
                           'proposicional es {La negación}.',
                           'El símbolo ∧ corresponde a la {Conjunción}.',
                           'El símbolo → corresponde a la {Condicional}.',
                           'El símbolo ↔ se lee {Si y solo si}.',
                           'La disyunción débil se lee como {O (inclusivo)}.',
                           'Los paréntesis, corchetes y llaves son símbolos '
                           '{Auxiliares}.',
                           'Una fórmula atómica se representa con {Una sola '
                           'variable}.',
                           'Los conectores que unen dos variables se '
                           'denominan {Diádicos o binarios}.',
                           'El símbolo ~ representa la {Negación}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Las proposiciones predicativas relacionan un '
                           'sujeto con una cualidad; las {relacionales} '
                           'vinculan dos o más sujetos entre sí.',
                           'Las proposiciones compuestas también se llaman '
                           '{coligativas}, porque unen proposiciones simples '
                           'mediante conectores lógicos.',
                           'En la disyunción débil, ambas alternativas '
                           'pueden cumplirse a la vez; en la disyunción '
                           '{fuerte} o exclusiva, no pueden darse '
                           'simultáneamente.',
                           'Los conectores monádicos afectan a una sola '
                           '{variable}; los diádicos requieren dos o más.']}],
  'cuadros': [{'titulo': '12.2 CONECTORES LÓGICOS',
               'encabezados': ['Conector', 'Símbolo', 'Se lee'],
               'filas': [['{Negación}', '~', '{no}'],
                         ['{Conjunción}', '∧', '{y}'],
                         ['Disyunción {débil}', '∨', '{o} (inclusivo)'],
                         ['Disyunción {fuerte}', '↮', 'o... o (exclusivo)'],
                         ['{Condicional}', '→', '{si... entonces}'],
                         ['{Bicondicional}', '↔', '{si y solo si}']]}],
  'preguntas': [{'pregunta': 'Una proposición es todo enunciado del que se '
                             'puede afirmar que es:',
                 'alternativas': ['Justo o injusto',
                                  'Claro u oscuro',
                                  'Bello o feo',
                                  'Útil o inútil',
                                  'Verdadero o falso'],
                 'correcta': 'E'},
                {'pregunta': 'NO es una proposición:',
                 'alternativas': ['Lima es la capital',
                                  'El Cusco está en el Perú',
                                  'La nieve es blanca',
                                  '¿Qué hora es?',
                                  'Dos más dos es cuatro'],
                 'correcta': 'D'},
                {'pregunta': 'La proposición que no contiene ningún operador '
                             'lógico se denomina:',
                 'alternativas': ['Simple o atómica',
                                  'Molecular',
                                  'Bicondicional',
                                  'Compuesta',
                                  'Condicional'],
                 'correcta': 'A'},
                {'pregunta': 'La proposición que contiene uno o más '
                             'operadores se denomina:',
                 'alternativas': ['Compuesta o molecular',
                                  'Simple',
                                  'Constante',
                                  'Variable',
                                  'Atómica'],
                 'correcta': 'A'},
                {'pregunta': 'Las variables proposicionales se representan '
                             'con:',
                 'alternativas': ['Letras griegas',
                                  'Números',
                                  'Símbolos matemáticos',
                                  'Palabras',
                                  'Letras minúsculas p, q, r, s'],
                 'correcta': 'E'},
                {'pregunta': 'El único conector monádico de la lógica '
                             'proposicional es:',
                 'alternativas': ['La condicional',
                                  'La bicondicional',
                                  'La conjunción',
                                  'La negación',
                                  'La disyunción'],
                 'correcta': 'D'},
                {'pregunta': 'El símbolo ∧ corresponde a la:',
                 'alternativas': ['Disyunción',
                                  'Conjunción',
                                  'Condicional',
                                  'Negación',
                                  'Bicondicional'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo → corresponde a la:',
                 'alternativas': ['Conjunción',
                                  'Condicional',
                                  'Disyunción fuerte',
                                  'Negación',
                                  'Bicondicional'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ↔ se lee:',
                 'alternativas': ['Si... entonces',
                                  'O',
                                  'Y',
                                  'Si y solo si',
                                  'No'],
                 'correcta': 'D'},
                {'pregunta': 'La disyunción débil se lee como:',
                 'alternativas': ['No',
                                  'Si... entonces',
                                  'Y',
                                  'O (inclusivo)',
                                  'Si y solo si'],
                 'correcta': 'D'},
                {'pregunta': 'Los paréntesis, corchetes y llaves son '
                             'símbolos:',
                 'alternativas': ['Monádicos',
                                  'Auxiliares',
                                  'Variables',
                                  'Constantes',
                                  'Diádicos'],
                 'correcta': 'B'},
                {'pregunta': '«El zorrino no es mamífero» se formaliza como:',
                 'alternativas': ['p', 'p → q', '~p', 'p ∨ q', 'p ∧ q'],
                 'correcta': 'C'},
                {'pregunta': '«La vaca es mamífero y el caballo también» se '
                             'formaliza como:',
                 'alternativas': ['~p', 'p ∧ q', 'p ↔ q', 'p ∨ q', 'p → q'],
                 'correcta': 'B'},
                {'pregunta': '«El asno es mamífero pero el loro no» se '
                             'formaliza como:',
                 'alternativas': ['p ∧ q',
                                  'p → ~q',
                                  '~p ∧ q',
                                  'p ∧ ~q',
                                  'p ∨ q'],
                 'correcta': 'D'},
                {'pregunta': 'Una fórmula atómica se representa con:',
                 'alternativas': ['Tres operadores',
                                  'Una sola variable',
                                  'Dos variables',
                                  'Un conector',
                                  'Paréntesis'],
                 'correcta': 'B'},
                {'pregunta': '«Si llueve entonces me quedo» se formaliza '
                             'como:',
                 'alternativas': ['p ∨ q', 'p → q', '~p', 'p ∧ q', 'p ↔ q'],
                 'correcta': 'B'},
                {'pregunta': 'Los conectores que unen dos variables se '
                             'denominan:',
                 'alternativas': ['Diádicos o binarios',
                                  'Monádicos',
                                  'Auxiliares',
                                  'Atómicos',
                                  'Variables'],
                 'correcta': 'A'},
                {'pregunta': '«Estudio si y solo si tengo tiempo» se '
                             'formaliza como:',
                 'alternativas': ['~p', 'p ∧ q', 'p ∨ q', 'p ↔ q', 'p → q'],
                 'correcta': 'D'},
                {'pregunta': 'Las órdenes y las exclamaciones NO son '
                             'proposiciones porque:',
                 'alternativas': ['No usan verbos',
                                  'No pueden ser verdaderas ni falsas',
                                  'Son emotivas siempre',
                                  'Son muy breves',
                                  'Carecen de sujeto'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ~ representa la:',
                 'alternativas': ['Conjunción',
                                  'Negación',
                                  'Implicación',
                                  'Disyunción',
                                  'Equivalencia'],
                 'correcta': 'B'}]},
 {'num': 13,
  'titulo': 'Tablas de verdad y razonamientos válidos',
  'secciones': [{'titulo': '13.1 LA TABLA DE VERDAD',
                 'items': ['Es el diagrama que muestra todos los valores '
                           'posibles de una fórmula {molecular}.',
                           'El número de combinaciones o {arreglos} se '
                           'calcula con la fórmula {2ⁿ}, donde n es el '
                           'número de {variables}.',
                           'Con 2 variables hay {4} combinaciones; con 3 '
                           'variables, {8}.']},
                {'titulo': '13.2 PRINCIPALES ESQUEMAS',
                 'items': ['{Tautología}: la fórmula resulta {verdadera} en '
                           'todos los casos.',
                           '{Contradicción}: la fórmula resulta {falsa} en '
                           'todos los casos.',
                           '{Contingencia} o consistencia: resulta verdadera '
                           'en algunos casos y {falsa} en otros.']},
                {'titulo': '13.3 RAZONAMIENTOS VÁLIDOS',
                 'items': ['{Modus ponendo ponens} (MPP): si p → q, y se '
                           'afirma {p}, entonces se concluye {q}.',
                           '{Modus tollendo tollens} (MTT): si p → q, y se '
                           'niega {q}, entonces se concluye {~p}.',
                           '{Silogismo disyuntivo} (SD): si p ∨ q, y se '
                           'niega {p}, entonces se concluye {q}.',
                           '{Silogismo hipotético puro} (SHP): si p → q y q '
                           '→ r, entonces {p → r}.',
                           '{Ley de De Morgan}: la negación de una '
                           'conjunción equivale a la {disyunción} de las '
                           'negaciones.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El diagrama que muestra todos los valores '
                           'posibles de una fórmula se denomina {Tabla de '
                           'verdad}.',
                           'El número de combinaciones de una tabla de '
                           'verdad se calcula con {2ⁿ}.',
                           'Una fórmula con 3 variables tiene un número de '
                           'combinaciones igual a {8}.',
                           'Una fórmula con 2 variables tiene un número de '
                           'combinaciones igual a {4}.',
                           'La fórmula que resulta verdadera en todos los '
                           'casos es una {Tautología}.',
                           'La fórmula que resulta falsa en todos los casos '
                           'es una {Contradicción}.',
                           'La fórmula verdadera en algunos casos y falsa en '
                           'otros es una {Contingencia}.',
                           'El Modus Ponendo Ponens concluye q a partir de '
                           '{p → q y p}.',
                           'El Modus Tollendo Tollens concluye ~p a partir '
                           'de {p → q y ~q}.',
                           'El Silogismo Disyuntivo concluye q a partir de '
                           '{p ∨ q y ~p}.',
                           'El Silogismo Hipotético Puro concluye p → r a '
                           'partir de {p → q y q → r}.',
                           'La ley que transforma la negación de una '
                           'conjunción en disyunción de negaciones es la de '
                           '{De Morgan}.',
                           'Si «si estudio apruebo» y «estudio», entonces '
                           '«apruebo». Este razonamiento es un {MPP}.',
                           'Si «si llueve me mojo» y «no me mojé», entonces '
                           '«no llovió». Este razonamiento es un {MTT}.',
                           'En una tabla de verdad, el brazo derecho de la '
                           'cruz se denomina {Cuerpo}.',
                           'En una tabla de verdad, el brazo izquierdo se '
                           'denomina {Margen}.',
                           'Una fórmula con 4 variables tendrá un número de '
                           'combinaciones igual a {16}.',
                           'La tautología se representa habitualmente con la '
                           'letra {T}.',
                           'Si «o voy al cine o voy al teatro» y «no voy al '
                           'cine», concluyo «voy al teatro». Es un '
                           '{Silogismo disyuntivo}.',
                           'El dilema constructivo compuesto se abrevia como '
                           '{DCC}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Las variables de una tabla de verdad se ubican '
                           'en la parte superior, y en la parte inferior se '
                           'ordenan todas las combinaciones de verdad y '
                           '{falsedad}.',
                           'El Silogismo Hipotético Puro se expresa mediante '
                           'la fórmula [(p → q) ∧ (q → r)] → (p → {r}).',
                           'El Principio de Identidad se atribuye a '
                           '{Parménides}, quien planteó que todo objeto es '
                           'idéntico a sí mismo.',
                           'El Principio de No Contradicción se atribuye a '
                           '{Platón}, y sostiene que el mundo sensible y el '
                           'inteligible no pueden ser lo mismo a la vez.',
                           'El Principio del Tercio Excluido fue formulado '
                           'por {Aristóteles}.',
                           'Las leyes de la lógica dialéctica, distintas de '
                           'la lógica formal, incluyen la ley del tránsito '
                           'de lo cuantitativo a lo cualitativo y la ley de '
                           'la {negación} de la negación.']}],
  'cuadros': [{'titulo': '13.2 ESQUEMAS SEGÚN SU RESULTADO',
               'encabezados': ['Esquema', 'Resultado'],
               'filas': [['{Tautología}', '{Verdadera} en todos los casos'],
                         ['{Contradicción}', '{Falsa} en todos los casos'],
                         ['{Contingencia}',
                          'Verdadera en {algunos} casos']]}],
  'preguntas': [{'pregunta': 'El diagrama que muestra todos los valores '
                             'posibles de una fórmula se denomina:',
                 'alternativas': ['Cuadro de oposición',
                                  'Árbol de Porfirio',
                                  'Diagrama de Venn',
                                  'Tabla de verdad',
                                  'Silogismo'],
                 'correcta': 'D'},
                {'pregunta': 'El número de combinaciones de una tabla de '
                             'verdad se calcula con:',
                 'alternativas': ['n+2', 'n²', '2n', 'n!', '2ⁿ'],
                 'correcta': 'E'},
                {'pregunta': 'Una fórmula con 3 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['8', '6', '3', '12', '9'],
                 'correcta': 'A'},
                {'pregunta': 'Una fórmula con 2 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['4', '8', '6', '3', '2'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula que resulta verdadera en todos los '
                             'casos es una:',
                 'alternativas': ['Contradicción',
                                  'Consistencia',
                                  'Tautología',
                                  'Antinomia',
                                  'Contingencia'],
                 'correcta': 'C'},
                {'pregunta': 'La fórmula que resulta falsa en todos los '
                             'casos es una:',
                 'alternativas': ['Implicación',
                                  'Tautología',
                                  'Equivalencia',
                                  'Contingencia',
                                  'Contradicción'],
                 'correcta': 'E'},
                {'pregunta': 'La fórmula verdadera en algunos casos y falsa '
                             'en otros es una:',
                 'alternativas': ['Contingencia',
                                  'Negación',
                                  'Tautología',
                                  'Contradicción',
                                  'Identidad'],
                 'correcta': 'A'},
                {'pregunta': 'El Modus Ponendo Ponens concluye q a partir '
                             'de:',
                 'alternativas': ['p → q y ~q',
                                  'p → q y q → r',
                                  '~(p ∧ q)',
                                  'p → q y p',
                                  'p ∨ q y ~p'],
                 'correcta': 'D'},
                {'pregunta': 'El Modus Tollendo Tollens concluye ~p a partir '
                             'de:',
                 'alternativas': ['p ∨ q y ~p',
                                  'p → q y ~q',
                                  'q → r',
                                  'p → q y p',
                                  'p ∧ q'],
                 'correcta': 'B'},
                {'pregunta': 'El Silogismo Disyuntivo concluye q a partir '
                             'de:',
                 'alternativas': ['p ∨ q y ~p',
                                  'p → q y ~q',
                                  'p ↔ q',
                                  'p → q y p',
                                  'p ∧ q'],
                 'correcta': 'A'},
                {'pregunta': 'El Silogismo Hipotético Puro concluye p → r a '
                             'partir de:',
                 'alternativas': ['p → q y p',
                                  'p ∨ q',
                                  '~p ∧ q',
                                  'p ↔ q',
                                  'p → q y q → r'],
                 'correcta': 'E'},
                {'pregunta': 'La ley que transforma la negación de una '
                             'conjunción en disyunción de negaciones es la '
                             'de:',
                 'alternativas': ['De Morgan',
                                  'Contradicción',
                                  'Tercio excluido',
                                  'Transitividad',
                                  'Identidad'],
                 'correcta': 'A'},
                {'pregunta': 'Si «si estudio apruebo» y «estudio», entonces '
                             '«apruebo». Este razonamiento es un:',
                 'alternativas': ['MPP', 'SD', 'MTT', 'De Morgan', 'SHP'],
                 'correcta': 'A'},
                {'pregunta': 'Si «si llueve me mojo» y «no me mojé», '
                             'entonces «no llovió». Este razonamiento es un:',
                 'alternativas': ['MPP', 'SHP', 'MTT', 'SD', 'DCC'],
                 'correcta': 'C'},
                {'pregunta': 'En una tabla de verdad, el brazo derecho de la '
                             'cruz se denomina:',
                 'alternativas': ['Columna',
                                  'Cuerpo',
                                  'Base',
                                  'Margen',
                                  'Eje'],
                 'correcta': 'B'},
                {'pregunta': 'En una tabla de verdad, el brazo izquierdo se '
                             'denomina:',
                 'alternativas': ['Fila',
                                  'Cuerpo',
                                  'Pie',
                                  'Margen',
                                  'Cabecera'],
                 'correcta': 'D'},
                {'pregunta': 'Una fórmula con 4 variables tendrá un número '
                             'de combinaciones igual a:',
                 'alternativas': ['16', '12', '8', '4', '32'],
                 'correcta': 'A'},
                {'pregunta': 'La tautología se representa habitualmente con '
                             'la letra:',
                 'alternativas': ['V', 'A', 'F', 'T', 'C'],
                 'correcta': 'D'},
                {'pregunta': 'Si «o voy al cine o voy al teatro» y «no voy '
                             'al cine», concluyo «voy al teatro». Es un:',
                 'alternativas': ['Silogismo disyuntivo',
                                  'Dilema',
                                  'SHP',
                                  'MPP',
                                  'MTT'],
                 'correcta': 'A'},
                {'pregunta': 'El dilema constructivo compuesto se abrevia '
                             'como:',
                 'alternativas': ['DCC', 'SHP', 'SD', 'MTT', 'MPP'],
                 'correcta': 'A'}]},
 {'num': 14,
  'titulo': 'Principios lógicos y lógica formal clásica',
  'secciones': [{'titulo': '14.1 PRINCIPIOS LÓGICOS',
                 'items': ['Principio de {identidad}: toda cosa es '
                           '{idéntica} a sí misma. Se expresa «p es {p}».',
                           'Principio de no {contradicción}: una proposición '
                           'no puede ser {verdadera} y falsa a la vez.',
                           'Principio del {tercio excluido}: entre dos '
                           'proposiciones contradictorias, una es verdadera '
                           'y la otra {falsa}; no hay una {tercera} '
                           'posibilidad.']},
                {'titulo': '14.2 EL CONCEPTO',
                 'items': ['Es la representación {mental} de un objeto. Sus '
                           'características pueden ser {esenciales} o '
                           'accidentales.',
                           'Propiedades del concepto: la {extensión}, que es '
                           'el número de objetos a los que se aplica, y la '
                           '{comprensión}, que es el conjunto de {notas} o '
                           'características.',
                           'Ambas son inversamente {proporcionales}: a mayor '
                           'extensión, menor {comprensión}.']},
                {'titulo': '14.3 EL JUICIO',
                 'items': ['Es la operación mental que {afirma} o niega algo '
                           'de algo. Su expresión verbal es la '
                           '{proposición}.',
                           'Por su {cantidad}: universales y {particulares}.',
                           'Por su {cualidad}: {afirmativos} y negativos.',
                           'Juicios categóricos típicos: {A} (universal '
                           'afirmativo), {E} (universal negativo), {I} '
                           '(particular afirmativo) y {O} (particular '
                           'negativo).']},
                {'titulo': '14.4 EL RAZONAMIENTO',
                 'items': ['Razonamiento {deductivo}: va de lo {general} a '
                           'lo particular; la conclusión se sigue '
                           'necesariamente.',
                           'Razonamiento {inductivo}: va de lo {particular} '
                           'a lo general; la conclusión es {probable}.',
                           'Razonamiento {analógico}: concluye por '
                           '{semejanza} entre casos.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El principio según el cual toda cosa es idéntica '
                           'a sí misma es el de {Identidad}.',
                           'El principio que niega que una proposición sea '
                           'verdadera y falsa a la vez es el de {No '
                           'contradicción}.',
                           'El principio que afirma que entre dos '
                           'contradictorias no hay una tercera posibilidad '
                           'es el de {Tercio excluido}.',
                           'La representación mental de un objeto es el '
                           '{Concepto}.',
                           'El número de objetos a los que se aplica un '
                           'concepto es su {Extensión}.',
                           'El conjunto de notas o características de un '
                           'concepto es su {Comprensión}.',
                           'Extensión y comprensión son entre sí '
                           '{Inversamente proporcionales}.',
                           'La operación mental que afirma o niega algo de '
                           'algo es el {Juicio}.',
                           'La expresión verbal del juicio es la '
                           '{Proposición}.',
                           'Los juicios se dividen por su cantidad en '
                           'universales y {Particulares}.',
                           'Los juicios se dividen por su cualidad en '
                           'afirmativos y {Negativos}.',
                           'El juicio tipo A es {Universal afirmativo}.',
                           'El juicio tipo E es {Universal negativo}.',
                           'El juicio tipo I es {Particular afirmativo}.',
                           'El juicio tipo O es {Particular negativo}.',
                           'El razonamiento que va de lo general a lo '
                           'particular es {Deductivo}.',
                           'El razonamiento cuya conclusión es solo probable '
                           'es el {Inductivo}.',
                           'El razonamiento que concluye por semejanza entre '
                           'casos es el {Analógico}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El objeto formal del concepto sujeto, según su '
                           'extensión, da origen a juicios universales, '
                           'particulares e {individuales}.',
                           'Immanuel Kant propuso, además de los juicios '
                           'afirmativo y negativo, los llamados juicios '
                           '{infinitos}.',
                           'Según su modalidad, los juicios pueden ser '
                           'asertóricos, problemáticos y {apodícticos}, '
                           'según el grado de certeza que expresan.',
                           'Francis Bacon es autor del «Novum Organum», '
                           'también llamado el nuevo {Organon}.',
                           'El razonamiento deductivo va de lo universal a '
                           'lo particular; el {inductivo} va de casos '
                           'particulares a una conclusión universal.',
                           'El razonamiento {analógico} concluye por '
                           'semejanza entre un caso conocido y otro '
                           'nuevo.']}],
  'cuadros': [{'titulo': '14.3 JUICIOS CATEGÓRICOS TÍPICOS',
               'encabezados': ['Tipo', 'Cantidad', 'Cualidad'],
               'filas': [['{A}', '{Universal}', '{Afirmativo}'],
                         ['{E}', 'Universal', '{Negativo}'],
                         ['{I}', '{Particular}', 'Afirmativo'],
                         ['{O}', 'Particular', '{Negativo}']]}],
  'preguntas': [{'pregunta': 'El principio según el cual toda cosa es '
                             'idéntica a sí misma es el de:',
                 'alternativas': ['Razón suficiente',
                                  'No contradicción',
                                  'Tercio excluido',
                                  'Identidad',
                                  'Causalidad'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que niega que una proposición sea '
                             'verdadera y falsa a la vez es el de:',
                 'alternativas': ['Identidad',
                                  'Razón suficiente',
                                  'Tercio excluido',
                                  'No contradicción',
                                  'Analogía'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que afirma que entre dos '
                             'contradictorias no hay una tercera posibilidad '
                             'es el de:',
                 'alternativas': ['Causalidad',
                                  'Suficiencia',
                                  'Tercio excluido',
                                  'No contradicción',
                                  'Identidad'],
                 'correcta': 'C'},
                {'pregunta': 'La representación mental de un objeto es el:',
                 'alternativas': ['Juicio',
                                  'Término',
                                  'Concepto',
                                  'Silogismo',
                                  'Razonamiento'],
                 'correcta': 'C'},
                {'pregunta': 'El número de objetos a los que se aplica un '
                             'concepto es su:',
                 'alternativas': ['Cantidad',
                                  'Comprensión',
                                  'Esencia',
                                  'Extensión',
                                  'Cualidad'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de notas o características de un '
                             'concepto es su:',
                 'alternativas': ['Extensión',
                                  'Relación',
                                  'Comprensión',
                                  'Cualidad',
                                  'Cantidad'],
                 'correcta': 'C'},
                {'pregunta': 'Extensión y comprensión son entre sí:',
                 'alternativas': ['Inversamente proporcionales',
                                  'Independientes',
                                  'Equivalentes',
                                  'Idénticas',
                                  'Directamente proporcionales'],
                 'correcta': 'A'},
                {'pregunta': 'La operación mental que afirma o niega algo de '
                             'algo es el:',
                 'alternativas': ['Concepto',
                                  'Término',
                                  'Razonamiento',
                                  'Silogismo',
                                  'Juicio'],
                 'correcta': 'E'},
                {'pregunta': 'La expresión verbal del juicio es la:',
                 'alternativas': ['Interjección',
                                  'Frase',
                                  'Oración interrogativa',
                                  'Proposición',
                                  'Palabra'],
                 'correcta': 'D'},
                {'pregunta': 'Los juicios se dividen por su cantidad en '
                             'universales y:',
                 'alternativas': ['Hipotéticos',
                                  'Negativos',
                                  'Afirmativos',
                                  'Categóricos',
                                  'Particulares'],
                 'correcta': 'E'},
                {'pregunta': 'Los juicios se dividen por su cualidad en '
                             'afirmativos y:',
                 'alternativas': ['Particulares',
                                  'Negativos',
                                  'Simples',
                                  'Universales',
                                  'Compuestos'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo A es:',
                 'alternativas': ['Singular',
                                  'Universal negativo',
                                  'Universal afirmativo',
                                  'Particular negativo',
                                  'Particular afirmativo'],
                 'correcta': 'C'},
                {'pregunta': 'El juicio tipo E es:',
                 'alternativas': ['Particular afirmativo',
                                  'Universal afirmativo',
                                  'Particular negativo',
                                  'Universal negativo',
                                  'Indefinido'],
                 'correcta': 'D'},
                {'pregunta': 'El juicio tipo I es:',
                 'alternativas': ['Singular',
                                  'Particular negativo',
                                  'Particular afirmativo',
                                  'Universal afirmativo',
                                  'Universal negativo'],
                 'correcta': 'C'},
                {'pregunta': 'El juicio tipo O es:',
                 'alternativas': ['Universal afirmativo',
                                  'Particular negativo',
                                  'Universal negativo',
                                  'Hipotético',
                                  'Particular afirmativo'],
                 'correcta': 'B'},
                {'pregunta': '«Todos los hombres son mortales» es un juicio '
                             'de tipo:',
                 'alternativas': ['A', 'O', 'I', 'E', 'U'],
                 'correcta': 'A'},
                {'pregunta': '«Ningún metal es líquido» es un juicio de '
                             'tipo:',
                 'alternativas': ['O', 'I', 'A', 'E', 'U'],
                 'correcta': 'D'},
                {'pregunta': 'El razonamiento que va de lo general a lo '
                             'particular es:',
                 'alternativas': ['Analógico',
                                  'Abductivo',
                                  'Dialéctico',
                                  'Inductivo',
                                  'Deductivo'],
                 'correcta': 'E'},
                {'pregunta': 'El razonamiento cuya conclusión es solo '
                             'probable es el:',
                 'alternativas': ['Inductivo',
                                  'Apodíctico',
                                  'Formal',
                                  'Silogístico',
                                  'Deductivo'],
                 'correcta': 'A'},
                {'pregunta': 'El razonamiento que concluye por semejanza '
                             'entre casos es el:',
                 'alternativas': ['Inductivo completo',
                                  'Hipotético',
                                  'Deductivo',
                                  'Silogístico',
                                  'Analógico'],
                 'correcta': 'E'}]},
 {'num': 15,
  'titulo': 'Inferencias',
  'secciones': [{'titulo': '15.1 INFERENCIAS INMEDIATAS',
                 'items': ['Son aquellas en que se obtiene una conclusión a '
                           'partir de una {sola} premisa.',
                           'Por {oposición}: se basan en el cuadro de '
                           'oposición entre juicios A, E, I, O. Comprende '
                           'las relaciones de {contradicción}, contrariedad, '
                           '{subcontrariedad} y subalternación.',
                           'Por {conversión}: se intercambian el {sujeto} y '
                           'el {predicado}. Ejemplo: «Ningún S es P» se '
                           'convierte en «Ningún {P} es S».',
                           'Por {obversión}: se cambia la {cualidad} del '
                           'juicio y se niega el {predicado}. «Todo S es P» '
                           'se obvierte en «Ningún S es {no-P}».']},
                {'titulo': '15.2 y 15.3 CONTRAPUESTA E INFERENCIA MEDIATA',
                 'items': ['Por contrapuesta {parcial}: se obtiene '
                           'combinando obversión y conversión.',
                           'Por contrapuesta {total}: se niegan ambos '
                           'términos y se {intercambian}.',
                           'La inferencia {mediata} obtiene la conclusión a '
                           'partir de {dos} o más premisas; su forma típica '
                           'es el {silogismo}.']},
                {'titulo': '15.4 EL SILOGISMO CATEGÓRICO',
                 'items': ['Consta de tres proposiciones: premisa {mayor}, '
                           'premisa {menor} y {conclusión}.',
                           'Y de tres términos: {mayor} (P, predicado de la '
                           'conclusión), {menor} (S, sujeto de la '
                           'conclusión) y {medio} (M), que aparece en ambas '
                           'premisas pero no en la {conclusión}.',
                           'Reglas principales: de dos premisas {negativas} '
                           'no se sigue conclusión; de dos premisas '
                           '{particulares} tampoco; el término medio debe '
                           'estar {distribuido} al menos una vez.',
                           'Las {figuras} del silogismo se determinan por la '
                           'posición del término {medio}: son {cuatro}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La inferencia que obtiene una conclusión a '
                           'partir de una sola premisa es {Inmediata}.',
                           'La inferencia en que se intercambian sujeto y '
                           'predicado se denomina {Conversión}.',
                           'La inferencia en que se cambia la cualidad y se '
                           'niega el predicado es la {Obversión}.',
                           'El cuadro de oposición relaciona los juicios {A, '
                           'E, I, O}.',
                           'La inferencia que parte de dos o más premisas se '
                           'denomina {Mediata}.',
                           'La forma típica de la inferencia mediata es el '
                           '{Silogismo}.',
                           'El silogismo categórico consta de {Tres '
                           'proposiciones}.',
                           'El término que aparece en ambas premisas pero no '
                           'en la conclusión es el {Medio}.',
                           'El término mayor del silogismo es el {Predicado '
                           'de la conclusión}.',
                           'El término menor del silogismo es el {Sujeto de '
                           'la conclusión}.',
                           'De dos premisas negativas {No se sigue '
                           'conclusión alguna}.',
                           'De dos premisas particulares {No se sigue '
                           'conclusión alguna}.',
                           'El término medio debe estar distribuido {Al '
                           'menos una vez}.',
                           'Las figuras del silogismo se determinan por la '
                           'posición del {Término medio}.',
                           'El número de figuras del silogismo es {Cuatro}.',
                           'La contrapuesta total se obtiene {Negando ambos '
                           'términos e intercambiándolos}.',
                           'La relación entre A y O en el cuadro de '
                           'oposición es de {Contradicción}.',
                           'La relación entre A y E en el cuadro de '
                           'oposición es de {Contrariedad}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El cuadro tradicional de oposición entre los '
                           'juicios A, E, I, O también es conocido como el '
                           'cuadro de {Boecio}.',
                           'Dos proposiciones contrarias (A y E) nunca '
                           'pueden ser verdaderas a la vez, pero sí pueden '
                           'ser {falsas} ambas.',
                           'En la conversión, se intercambian el sujeto y el '
                           'predicado; en la {obversión}, se cambia la '
                           'cualidad del juicio y se niega el predicado.',
                           'En la obversión, ni el sujeto ni la {cantidad} '
                           'del juicio cambian; permanecen invariables.',
                           'El complemento de una clase está formado por '
                           'todos los elementos que no pertenecen a la clase '
                           '{original}.',
                           'En un silogismo válido, si ambas premisas son '
                           'universales, al menos una debe ser '
                           '{negativa}.']}],
  'cuadros': [{'titulo': '15.4 ESTRUCTURA DEL SILOGISMO',
               'encabezados': ['Elemento', 'Símbolo', 'Ubicación'],
               'filas': [['Término {mayor}',
                          '{P}',
                          'Predicado de la {conclusión}'],
                         ['Término {menor}',
                          '{S}',
                          '{Sujeto} de la conclusión'],
                         ['Término {medio}', '{M}', 'En ambas {premisas}']]}],
  'preguntas': [{'pregunta': 'La inferencia que obtiene una conclusión a '
                             'partir de una sola premisa es:',
                 'alternativas': ['Mediata',
                                  'Silogística',
                                  'Analógica',
                                  'Inmediata',
                                  'Deductiva compuesta'],
                 'correcta': 'D'},
                {'pregunta': 'La inferencia en que se intercambian sujeto y '
                             'predicado se denomina:',
                 'alternativas': ['Conversión',
                                  'Subalternación',
                                  'Obversión',
                                  'Oposición',
                                  'Contraposición'],
                 'correcta': 'A'},
                {'pregunta': 'La inferencia en que se cambia la cualidad y '
                             'se niega el predicado es la:',
                 'alternativas': ['Conversión',
                                  'Contrapuesta total',
                                  'Subalternación',
                                  'Contrariedad',
                                  'Obversión'],
                 'correcta': 'E'},
                {'pregunta': '«Todo S es P» obvertido resulta:',
                 'alternativas': ['Algún S no es P',
                                  'Ningún P es S',
                                  'Ningún S es no-P',
                                  'Todo P es S',
                                  'Algún S es P'],
                 'correcta': 'C'},
                {'pregunta': 'El cuadro de oposición relaciona los juicios:',
                 'alternativas': ['Simples y compuestos',
                                  'Mayor y menor',
                                  'Deductivos e inductivos',
                                  'Verdaderos y falsos',
                                  'A, E, I, O'],
                 'correcta': 'E'},
                {'pregunta': 'La inferencia que parte de dos o más premisas '
                             'se denomina:',
                 'alternativas': ['Simple',
                                  'Mediata',
                                  'Unilateral',
                                  'Inmediata',
                                  'Directa'],
                 'correcta': 'B'},
                {'pregunta': 'La forma típica de la inferencia mediata es '
                             'el:',
                 'alternativas': ['Sorites',
                                  'Entimema',
                                  'Epiquerema',
                                  'Dilema',
                                  'Silogismo'],
                 'correcta': 'E'},
                {'pregunta': 'El silogismo categórico consta de:',
                 'alternativas': ['Cuatro proposiciones',
                                  'Una proposición',
                                  'Cinco proposiciones',
                                  'Dos proposiciones',
                                  'Tres proposiciones'],
                 'correcta': 'E'},
                {'pregunta': 'El término que aparece en ambas premisas pero '
                             'no en la conclusión es el:',
                 'alternativas': ['Predicado',
                                  'Menor',
                                  'Medio',
                                  'Sujeto',
                                  'Mayor'],
                 'correcta': 'C'},
                {'pregunta': 'El término mayor del silogismo es el:',
                 'alternativas': ['Sujeto de la conclusión',
                                  'Que aparece dos veces',
                                  'Que se omite',
                                  'Predicado de la conclusión',
                                  'Término medio'],
                 'correcta': 'D'},
                {'pregunta': 'El término menor del silogismo es el:',
                 'alternativas': ['Sujeto de la conclusión',
                                  'Que no aparece',
                                  'Universal',
                                  'Predicado de la conclusión',
                                  'Término medio'],
                 'correcta': 'A'},
                {'pregunta': 'De dos premisas negativas:',
                 'alternativas': ['Se sigue una conclusión negativa',
                                  'Se sigue una particular',
                                  'Se sigue siempre una universal',
                                  'Se sigue una conclusión afirmativa',
                                  'No se sigue conclusión alguna'],
                 'correcta': 'E'},
                {'pregunta': 'De dos premisas particulares:',
                 'alternativas': ['Se sigue una negativa',
                                  'Se sigue una afirmativa',
                                  'Se sigue una universal',
                                  'Se sigue una conclusión particular',
                                  'No se sigue conclusión alguna'],
                 'correcta': 'E'},
                {'pregunta': 'El término medio debe estar distribuido:',
                 'alternativas': ['Siempre dos veces',
                                  'Nunca',
                                  'En el predicado',
                                  'Al menos una vez',
                                  'Solo en la conclusión'],
                 'correcta': 'D'},
                {'pregunta': 'Las figuras del silogismo se determinan por la '
                             'posición del:',
                 'alternativas': ['Término menor',
                                  'Término mayor',
                                  'Término medio',
                                  'Sujeto',
                                  'Predicado'],
                 'correcta': 'C'},
                {'pregunta': 'El número de figuras del silogismo es:',
                 'alternativas': ['Ocho', 'Seis', 'Tres', 'Cuatro', 'Dos'],
                 'correcta': 'D'},
                {'pregunta': '«Ningún S es P» convertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Todo S es no-P',
                                  'Ningún P es S',
                                  'Algún P es S',
                                  'Algún S no es P'],
                 'correcta': 'C'},
                {'pregunta': 'La contrapuesta total se obtiene:',
                 'alternativas': ['Cambiando solo la cualidad',
                                  'Solo convirtiendo',
                                  'Negando la conclusión',
                                  'Negando ambos términos e '
                                  'intercambiándolos',
                                  'Solo obvirtiendo'],
                 'correcta': 'D'},
                {'pregunta': 'La relación entre A y O en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Subcontrariedad',
                                  'Contradicción',
                                  'Contrariedad',
                                  'Subalternación',
                                  'Equivalencia'],
                 'correcta': 'B'},
                {'pregunta': 'La relación entre A y E en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Subalternación',
                                  'Identidad',
                                  'Subcontrariedad',
                                  'Contradicción',
                                  'Contrariedad'],
                 'correcta': 'E'}]},
 {'num': 16,
  'titulo': 'Lógica de clases',
  'secciones': [{'titulo': '16.1 EL ÁLGEBRA BOOLEANA',
                 'items': ['Fue desarrollada por George {Boole}. Aplica '
                           'procedimientos {algebraicos} al razonamiento '
                           'lógico.',
                           'Una {clase} es el conjunto de todos los objetos '
                           'que poseen una {característica} común.',
                           'Clase {universal}: contiene todos los elementos '
                           'del universo del discurso; se representa por '
                           '{1}.',
                           'Clase {vacía} o nula: no contiene ningún '
                           'elemento; se representa por {0}.']},
                {'titulo': '16.2 TIPOS DE CLASES',
                 'items': ['Clase {universal}, clase {particular} y '
                           '{complemento} de una clase.',
                           'El {complemento} de una clase A está formado por '
                           'todos los elementos que {no} pertenecen a A. Se '
                           'simboliza {Ā}.']},
                {'titulo': '16.3 RELACIONES ENTRE CLASES',
                 'items': ['{Inclusión}: todos los elementos de una clase '
                           'están contenidos en {otra}.',
                           '{Igualdad}: dos clases tienen exactamente los '
                           '{mismos} elementos.',
                           '{Exclusión}: dos clases no tienen ningún '
                           'elemento en {común}.']},
                {'titulo': '16.4 OPERACIONES CON CLASES',
                 'items': ['{Unión} o suma: reúne los elementos de {ambas} '
                           'clases. Se simboliza {∪}.',
                           '{Intersección} o producto: reúne los elementos '
                           '{comunes} a ambas clases. Se simboliza {∩}.',
                           '{Diferencia}: elementos que pertenecen a una '
                           'clase pero {no} a la otra.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El álgebra que aplica procedimientos algebraicos '
                           'a la lógica fue desarrollada por {George Boole}.',
                           'El conjunto de todos los objetos que poseen una '
                           'característica común es una {Clase}.',
                           'La clase que contiene todos los elementos del '
                           'universo del discurso es la clase {Universal}.',
                           'La clase universal se representa con el símbolo '
                           '{1}.',
                           'La clase que no contiene ningún elemento se '
                           'denomina {Vacía o nula}.',
                           'La clase vacía se representa con el símbolo {0}.',
                           'El complemento de una clase A está formado por '
                           'los elementos que {No pertenecen a A}.',
                           'El complemento de la clase A se simboliza {Ā}.',
                           'La relación en que todos los elementos de una '
                           'clase están contenidos en otra es {Inclusión}.',
                           'La relación en que dos clases tienen exactamente '
                           'los mismos elementos es {Igualdad}.',
                           'La relación en que dos clases no tienen ningún '
                           'elemento en común es {Exclusión}.',
                           'La operación que reúne los elementos de ambas '
                           'clases es la {Unión}.',
                           'La operación que reúne solo los elementos '
                           'comunes es la {Intersección}.',
                           'El símbolo ∪ representa la {Unión}.',
                           'El símbolo ∩ representa la {Intersección}.',
                           'La operación que toma los elementos de una clase '
                           'que no están en la otra es la {Diferencia}.',
                           'La lógica de clases se ocupa de las relaciones '
                           'entre {Clases o conjuntos}.',
                           'La unión también recibe el nombre de {Suma}.',
                           'La intersección también recibe el nombre de '
                           '{Producto}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El conjunto de todos los elementos posibles en '
                           'un contexto dado se llama, según De Morgan, '
                           '{universo del discurso}.',
                           'La clase vacía se simboliza con el número cero o '
                           'con la letra griega {fi}.',
                           'El complemento de una clase A se simboliza como '
                           '{Ā} (A con una raya encima).',
                           'Las operaciones básicas entre clases son la '
                           'unión o suma, la {intersección} y la diferencia.',
                           'Dos clases son iguales cuando todos sus '
                           'elementos son {comunes} a ambas.']}],
  'cuadros': [{'titulo': '16. CLASES Y SÍMBOLOS',
               'encabezados': ['Concepto', 'Símbolo'],
               'filas': [['Clase {universal}', '{1}'],
                         ['Clase {vacía}', '{0}'],
                         ['{Complemento} de A', '{Ā}'],
                         ['{Unión}', '{∪}'],
                         ['{Intersección}', '{∩}']]}],
  'preguntas': [{'pregunta': 'El álgebra que aplica procedimientos '
                             'algebraicos a la lógica fue desarrollada por:',
                 'alternativas': ['Russell',
                                  'Aristóteles',
                                  'Frege',
                                  'George Boole',
                                  'Venn'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de todos los objetos que poseen '
                             'una característica común es una:',
                 'alternativas': ['Proposición',
                                  'Variable',
                                  'Premisa',
                                  'Inferencia',
                                  'Clase'],
                 'correcta': 'E'},
                {'pregunta': 'La clase que contiene todos los elementos del '
                             'universo del discurso es la clase:',
                 'alternativas': ['Universal',
                                  'Nula',
                                  'Complementaria',
                                  'Particular',
                                  'Vacía'],
                 'correcta': 'A'},
                {'pregunta': 'La clase universal se representa con el '
                             'símbolo:',
                 'alternativas': ['Ā', '0', '1', '∪', '∩'],
                 'correcta': 'C'},
                {'pregunta': 'La clase que no contiene ningún elemento se '
                             'denomina:',
                 'alternativas': ['Particular',
                                  'Complementaria',
                                  'Unitaria',
                                  'Vacía o nula',
                                  'Universal'],
                 'correcta': 'D'},
                {'pregunta': 'La clase vacía se representa con el símbolo:',
                 'alternativas': ['0', '∪', '1', '∅ únicamente', 'Ā'],
                 'correcta': 'A'},
                {'pregunta': 'El complemento de una clase A está formado por '
                             'los elementos que:',
                 'alternativas': ['Pertenecen a A y B',
                                  'No pertenecen a A',
                                  'Son comunes',
                                  'Son universales',
                                  'Pertenecen a A'],
                 'correcta': 'B'},
                {'pregunta': 'El complemento de la clase A se simboliza:',
                 'alternativas': ['A∪B', 'A∩B', '1', 'A-B', 'Ā'],
                 'correcta': 'E'},
                {'pregunta': 'La relación en que todos los elementos de una '
                             'clase están contenidos en otra es:',
                 'alternativas': ['Exclusión',
                                  'Complemento',
                                  'Diferencia',
                                  'Igualdad',
                                  'Inclusión'],
                 'correcta': 'E'},
                {'pregunta': 'La relación en que dos clases tienen '
                             'exactamente los mismos elementos es:',
                 'alternativas': ['Exclusión',
                                  'Intersección',
                                  'Igualdad',
                                  'Unión',
                                  'Inclusión'],
                 'correcta': 'C'},
                {'pregunta': 'La relación en que dos clases no tienen ningún '
                             'elemento en común es:',
                 'alternativas': ['Unión',
                                  'Igualdad',
                                  'Complemento',
                                  'Exclusión',
                                  'Inclusión'],
                 'correcta': 'D'},
                {'pregunta': 'La operación que reúne los elementos de ambas '
                             'clases es la:',
                 'alternativas': ['Inclusión',
                                  'Unión',
                                  'Diferencia',
                                  'Intersección',
                                  'Complementación'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que reúne solo los elementos '
                             'comunes es la:',
                 'alternativas': ['Complemento',
                                  'Suma',
                                  'Unión',
                                  'Diferencia',
                                  'Intersección'],
                 'correcta': 'E'},
                {'pregunta': 'El símbolo ∪ representa la:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Inclusión',
                                  'Exclusión',
                                  'Diferencia'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∩ representa la:',
                 'alternativas': ['Unión',
                                  'Intersección',
                                  'Complemento',
                                  'Diferencia',
                                  'Igualdad'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que toma los elementos de una '
                             'clase que no están en la otra es la:',
                 'alternativas': ['Diferencia',
                                  'Igualdad',
                                  'Unión',
                                  'Inclusión',
                                  'Intersección'],
                 'correcta': 'A'},
                {'pregunta': 'La lógica de clases se ocupa de las relaciones '
                             'entre:',
                 'alternativas': ['Clases o conjuntos',
                                  'Valores',
                                  'Silogismos',
                                  'Proposiciones',
                                  'Falacias'],
                 'correcta': 'A'},
                {'pregunta': '«Los peruanos» y «los no peruanos» son entre '
                             'sí:',
                 'alternativas': ['Clases iguales',
                                  'Clases incluidas',
                                  'Clases idénticas',
                                  'Clases complementarias',
                                  'Una sola clase'],
                 'correcta': 'D'},
                {'pregunta': 'La unión también recibe el nombre de:',
                 'alternativas': ['Suma',
                                  'Producto',
                                  'Resta',
                                  'Potencia',
                                  'Cociente'],
                 'correcta': 'A'},
                {'pregunta': 'La intersección también recibe el nombre de:',
                 'alternativas': ['Producto',
                                  'Suma',
                                  'Diferencia',
                                  'Unión',
                                  'Complemento'],
                 'correcta': 'A'}]},
 {'num': 17,
  'titulo': 'Fórmulas booleanas y diagramas de Venn',
  'secciones': [{'titulo': '17.1 DIAGRAMACIÓN DE UNA CLASE',
                 'items': ['Los diagramas de {Venn} representan gráficamente '
                           'las clases mediante {círculos}.',
                           'El sombreado indica que la región está {vacía}; '
                           'una {X} indica que la región tiene al menos un '
                           '{elemento}.',
                           '«Ningún S es P» se representa sombreando la '
                           'región {común} a ambos círculos.',
                           '«Algún S es P» se representa colocando una {X} '
                           'en la región común.']},
                {'titulo': '17.2 DIAGRAMACIÓN DE DOS CLASES',
                 'items': ['Con dos clases se generan {4} regiones '
                           'distintas.',
                           '«Todo S es P» se representa sombreando la parte '
                           'de {S} que no es P.',
                           '«Algún S no es P» se representa con una X en la '
                           'parte de S {fuera} de P.']},
                {'titulo': '17.3 PROPOSICIONES TÍPICAS Y ATÍPICAS',
                 'items': ['Proposiciones {típicas}: las que corresponden a '
                           'las formas {A}, E, {I} y O.',
                           'Proposiciones {atípicas}: deben ser {traducidas} '
                           'previamente a una forma típica para poder '
                           'diagramarse.',
                           'Ejemplos de atípicas: «solo», «únicamente», '
                           '«nadie salvo», que suelen equivaler a juicios '
                           '{universales}.']},
                {'titulo': '17.4 VALIDEZ DEL SILOGISMO POR DIAGRAMAS',
                 'items': ['Para evaluar un silogismo se usan {tres} '
                           'círculos, uno por cada término.',
                           'Se diagraman primero las {premisas}, nunca la '
                           'conclusión.',
                           'Si al diagramar las premisas queda '
                           'automáticamente representada la {conclusión}, el '
                           'silogismo es {válido}.',
                           'Conviene diagramar primero las premisas '
                           '{universales} y después las particulares.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['Los diagramas que representan clases mediante '
                           'círculos fueron ideados por {Venn}.',
                           'En un diagrama de Venn, el sombreado indica que '
                           'la región {Está vacía}.',
                           'En un diagrama de Venn, la X indica que la '
                           'región {Tiene al menos un elemento}.',
                           'Con dos clases, el número de regiones que se '
                           'generan es {4}.',
                           'Las proposiciones típicas son las que '
                           'corresponden a las formas {A, E, I, O}.',
                           'Las proposiciones atípicas requieren ser '
                           '{Traducidas a una forma típica}.',
                           'Expresiones como «solo» y «únicamente» suelen '
                           'equivaler a juicios {Universales}.',
                           'Para evaluar la validez de un silogismo se usan '
                           '{Tres círculos}.',
                           'Al evaluar un silogismo por diagramas, se '
                           'diagraman {Solo las premisas}.',
                           'Un silogismo es válido si, al diagramar las '
                           'premisas {Queda automáticamente representada la '
                           'conclusión}.',
                           'Al diagramar conviene comenzar por las premisas '
                           '{Universales}.',
                           'Una región en blanco en un diagrama de Venn '
                           'significa que {No se sabe si tiene elementos}.',
                           'El diagrama de Venn permite determinar de un '
                           'silogismo su {Validez formal}.',
                           'Los diagramas de Venn representan gráficamente '
                           '{Clases y sus relaciones}.',
                           'En la diagramación, el círculo que se dibuja '
                           'para el término medio {Se dibuja intersecando a '
                           'los otros dos}.',
                           'Diagramar la conclusión antes que las premisas '
                           'constituye {Un error de método}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Afirmar que una clase S tiene miembros equivale '
                           'a {negar} que sea vacía.',
                           'Para resolver una proposición atípica se sigue '
                           'una secuencia: hallar su estructura formal, '
                           'determinar la fórmula atípica y luego la fórmula '
                           '{booleana}.',
                           'Al diagramar un silogismo con tres círculos, '
                           'estos se rotulan con las letras {S}, P y M.',
                           'Un silogismo se considera válido cuando, al '
                           'diagramar las premisas, la conclusión queda '
                           'representada de forma {automática}.',
                           'La ley del contenido existencial se aplica '
                           'cuando ambas premisas son universales y la '
                           '{conclusión} es particular.']}],
  'cuadros': [{'titulo': '17.1 SIMBOLOGÍA DE LOS DIAGRAMAS',
               'encabezados': ['Signo', 'Significado'],
               'filas': [['{Sombreado}', 'La región está {vacía}'],
                         ['{X}', 'La región tiene al menos un {elemento}'],
                         ['Región {en blanco}',
                          'No se sabe si tiene elementos']]}],
  'preguntas': [{'pregunta': 'Los diagramas que representan clases mediante '
                             'círculos fueron ideados por:',
                 'alternativas': ['Boole',
                                  'Venn',
                                  'Frege',
                                  'Euler únicamente',
                                  'Russell'],
                 'correcta': 'B'},
                {'pregunta': 'En un diagrama de Venn, el sombreado indica '
                             'que la región:',
                 'alternativas': ['Es universal',
                                  'Está vacía',
                                  'Es dudosa',
                                  'Tiene elementos',
                                  'Es infinita'],
                 'correcta': 'B'},
                {'pregunta': 'En un diagrama de Venn, la X indica que la '
                             'región:',
                 'alternativas': ['Es universal',
                                  'Está vacía',
                                  'Se excluye',
                                  'Tiene al menos un elemento',
                                  'Es complementaria'],
                 'correcta': 'D'},
                {'pregunta': '«Ningún S es P» se representa sombreando:',
                 'alternativas': ['La región común a S y P',
                                  'Nada',
                                  'Todo el círculo S',
                                  'La región fuera de ambos',
                                  'El círculo P'],
                 'correcta': 'A'},
                {'pregunta': '«Algún S es P» se representa colocando una X '
                             'en:',
                 'alternativas': ['El universo',
                                  'Fuera de ambos círculos',
                                  'La parte de S fuera de P',
                                  'El círculo P completo',
                                  'La región común a S y P'],
                 'correcta': 'E'},
                {'pregunta': '«Todo S es P» se representa sombreando:',
                 'alternativas': ['El universo',
                                  'Fuera de ambos',
                                  'La región común',
                                  'Todo el círculo P',
                                  'La parte de S que no es P'],
                 'correcta': 'E'},
                {'pregunta': '«Algún S no es P» se representa con una X en:',
                 'alternativas': ['La parte de S fuera de P',
                                  'Fuera de ambos',
                                  'La región común',
                                  'El círculo P',
                                  'El centro'],
                 'correcta': 'A'},
                {'pregunta': 'Con dos clases, el número de regiones que se '
                             'generan es:',
                 'alternativas': ['2', '8', '4', '6', '3'],
                 'correcta': 'C'},
                {'pregunta': 'Las proposiciones típicas son las que '
                             'corresponden a las formas:',
                 'alternativas': ['Universales solamente',
                                  'Simples y compuestas',
                                  'Deductivas',
                                  'Verdaderas y falsas',
                                  'A, E, I, O'],
                 'correcta': 'E'},
                {'pregunta': 'Las proposiciones atípicas requieren ser:',
                 'alternativas': ['Rechazadas',
                                  'Negadas',
                                  'Convertidas en falacias',
                                  'Traducidas a una forma típica',
                                  'Ignoradas'],
                 'correcta': 'D'},
                {'pregunta': 'Expresiones como «solo» y «únicamente» suelen '
                             'equivaler a juicios:',
                 'alternativas': ['Universales',
                                  'Singulares',
                                  'Negativos siempre',
                                  'Particulares',
                                  'Indefinidos'],
                 'correcta': 'A'},
                {'pregunta': 'Para evaluar la validez de un silogismo se '
                             'usan:',
                 'alternativas': ['Un círculo',
                                  'Cuatro círculos',
                                  'Tres círculos',
                                  'Dos círculos',
                                  'Cinco círculos'],
                 'correcta': 'C'},
                {'pregunta': 'Al evaluar un silogismo por diagramas, se '
                             'diagraman:',
                 'alternativas': ['La conclusión primero',
                                  'Solo las premisas',
                                  'Solo la menor',
                                  'Todo simultáneamente',
                                  'Solo la mayor'],
                 'correcta': 'B'},
                {'pregunta': 'Un silogismo es válido si, al diagramar las '
                             'premisas:',
                 'alternativas': ['Queda automáticamente representada la '
                                  'conclusión',
                                  'Las premisas son verdaderas',
                                  'Queda alguna región vacía',
                                  'No hay ninguna X',
                                  'Se sombrean todos los círculos'],
                 'correcta': 'A'},
                {'pregunta': 'Al diagramar conviene comenzar por las '
                             'premisas:',
                 'alternativas': ['Universales',
                                  'Más largas',
                                  'Particulares',
                                  'Afirmativas',
                                  'Negativas'],
                 'correcta': 'A'},
                {'pregunta': 'Una región en blanco en un diagrama de Venn '
                             'significa que:',
                 'alternativas': ['Está vacía',
                                  'Es universal',
                                  'Tiene elementos',
                                  'No se sabe si tiene elementos',
                                  'Es contradictoria'],
                 'correcta': 'D'},
                {'pregunta': 'El diagrama de Venn permite determinar de un '
                             'silogismo su:',
                 'alternativas': ['Utilidad',
                                  'Origen',
                                  'Validez formal',
                                  'Belleza',
                                  'Verdad material'],
                 'correcta': 'C'},
                {'pregunta': 'Los diagramas de Venn representan '
                             'gráficamente:',
                 'alternativas': ['Tablas de verdad',
                                  'Conectores lógicos',
                                  'Proposiciones compuestas',
                                  'Clases y sus relaciones',
                                  'Falacias'],
                 'correcta': 'D'},
                {'pregunta': 'En la diagramación, el círculo que se dibuja '
                             'para el término medio:',
                 'alternativas': ['Se dibuja intersecando a los otros dos',
                                  'Se dibuja aparte',
                                  'No se dibuja',
                                  'Se marca con X',
                                  'Se sombrea siempre'],
                 'correcta': 'A'},
                {'pregunta': 'Diagramar la conclusión antes que las premisas '
                             'constituye:',
                 'alternativas': ['Una simplificación válida',
                                  'Un atajo permitido',
                                  'Una regla de Venn',
                                  'Un error de método',
                                  'El procedimiento correcto'],
                 'correcta': 'D'}]}]
