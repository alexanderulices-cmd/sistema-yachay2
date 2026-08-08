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
                           '{pensar} y el ser.',
                           'Según {Wittgenstein}, la filosofía es una '
                           'actividad orientada hacia el esclarecimiento del '
                           '{lenguaje}, indagando si los enunciados tienen '
                           'sentido.']},
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
                           '{totalitario}.']},
                {'titulo': '1.6 DISCIPLINAS FILOSÓFICAS',
                 'items': ['La {gnoseología} o Teoría del Conocimiento '
                           'analiza la naturaleza, posibilidad y {límites} '
                           'del conocimiento en general.',
                           'La {epistemología} es el estudio crítico del '
                           'conocimiento {científico}, su fundamento y '
                           'metodología.',
                           'La {axiología} estudia el problema de los '
                           '{valores}: su existencia, origen, naturaleza y '
                           'características.',
                           'La {ética} estudia la conducta o comportamiento '
                           '{moral} del hombre en sociedad.',
                           'La {lógica} estudia los principios, métodos y '
                           'reglas para distinguir el {razonamiento} '
                           'correcto del incorrecto.',
                           'La {ontología} es el estudio del {ser} de las '
                           'cosas, del ser en tanto ser.',
                           'La {estética} trata de lo {bello} y los '
                           'diferentes modos de aprehensión de realidades '
                           'bellas.',
                           'La {antropología filosófica} estudia la esencia '
                           'del {hombre}, su significado y la finalidad de '
                           'su existencia.']}],
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
                          'Teoría del {Big Bang}']]},
              {'titulo': 'DISCIPLINAS FILOSÓFICAS Y SU OBJETO DE ESTUDIO',
               'despues_de': '1.6 DISCIPLINAS FILOSÓFICAS',
               'encabezados': ['Disciplina', 'Objeto de estudio'],
               'filas': [['{Gnoseología}', 'El conocimiento en {general}'],
                         ['{Epistemología}', 'El conocimiento {científico}'],
                         ['{Axiología}', 'Los {valores}'],
                         ['{Ética}', 'La conducta {moral}'],
                         ['{Lógica}', 'El {razonamiento} correcto'],
                         ['{Ontología}', 'El {ser} de las cosas'],
                         ['{Estética}', 'Lo {bello}']]}],
  'preguntas': [{'pregunta': 'El conjunto de mitos con que las primeras '
                             'civilizaciones explicaron el origen del '
                             'universo se denomina:',
                 'alternativas': ['Astronomía',
                                  'Cosmogonía',
                                  'Ontología',
                                  'Metafísica',
                                  'Cosmología'],
                 'correcta': 'B'},
                {'pregunta': 'El autor del poema «Teogonía» fue:',
                 'alternativas': ['Hesíodo',
                                  'Ptolomeo',
                                  'Aristóteles',
                                  'Homero',
                                  'Platón'],
                 'correcta': 'A'},
                {'pregunta': 'La cosmología se diferencia de la cosmogonía '
                             'porque explica mediante:',
                 'alternativas': ['Conceptos científicos y verificación',
                                  'Relatos y mitos',
                                  'Poemas épicos',
                                  'Tradiciones orales',
                                  'Revelaciones divinas'],
                 'correcta': 'A'},
                {'pregunta': 'El geocentrismo fue respaldado por:',
                 'alternativas': ['Copérnico',
                                  'Galileo',
                                  'Ptolomeo y Aristóteles',
                                  'Hubble',
                                  'Kepler'],
                 'correcta': 'C'},
                {'pregunta': 'El heliocentrismo fue sostenido por:',
                 'alternativas': ['Nicolás Copérnico',
                                  'Ptolomeo',
                                  'Hesíodo',
                                  'Sócrates',
                                  'Aristóteles'],
                 'correcta': 'A'},
                {'pregunta': 'Según el Big Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['1 000 millones de años',
                                  '100 000 años',
                                  '4 000 millones de años',
                                  '14 000 millones de años',
                                  '500 millones de años'],
                 'correcta': 'D'},
                {'pregunta': 'Hubble descubrió en 1929 que las galaxias:',
                 'alternativas': ['Giran alrededor de la Tierra',
                                  'Están fijas en la bóveda celeste',
                                  'Se acercan entre sí',
                                  'Permanecen inmóviles',
                                  'Se alejan unas de otras'],
                 'correcta': 'E'},
                {'pregunta': 'Según la ley de Hubble, la velocidad de una '
                             'galaxia es proporcional a su:',
                 'alternativas': ['Edad',
                                  'Masa',
                                  'Distancia',
                                  'Luminosidad',
                                  'Temperatura'],
                 'correcta': 'C'},
                {'pregunta': 'Si una fuente de luz se aleja de nosotros, su '
                             'espectro se desplaza hacia el:',
                 'alternativas': ['Azul',
                                  'Amarillo',
                                  'Verde',
                                  'Rojo',
                                  'Violeta'],
                 'correcta': 'D'},
                {'pregunta': 'Se atribuye el primer uso del término '
                             '«filosofía» a:',
                 'alternativas': ['Pitágoras de Samos',
                                  'Platón',
                                  'Aristóteles',
                                  'Tales de Mileto',
                                  'Sócrates'],
                 'correcta': 'A'},
                {'pregunta': 'Para Platón, el origen de la filosofía está '
                             'en:',
                 'alternativas': ['El lenguaje',
                                  'La duda',
                                  'La necesidad',
                                  'El asombro',
                                  'La fe'],
                 'correcta': 'D'},
                {'pregunta': 'Etimológicamente, filosofía significa:',
                 'alternativas': ['Amor a la sabiduría',
                                  'Búsqueda de Dios',
                                  'Ciencia del pensar',
                                  'Estudio del cosmos',
                                  'Estudio del ser'],
                 'correcta': 'A'},
                {'pregunta': 'Para Aristóteles, la filosofía es la ciencia '
                             'de:',
                 'alternativas': ['Los fenómenos naturales',
                                  'La conducta humana',
                                  'Los primeros principios y las primeras '
                                  'causas',
                                  'El lenguaje',
                                  'La sociedad'],
                 'correcta': 'C'},
                {'pregunta': 'La filosofía primera, según Aristóteles, se '
                             'denomina también:',
                 'alternativas': ['Física',
                                  'Metafísica',
                                  'Ética',
                                  'Lógica',
                                  'Gnoseología'],
                 'correcta': 'B'},
                {'pregunta': 'Según Russell, la filosofía nació de la unión '
                             'o el conflicto de dos impulsos:',
                 'alternativas': ['Racional y emocional',
                                  'Místico y científico',
                                  'Práctico y teórico',
                                  'Individual y social',
                                  'Estético y ético'],
                 'correcta': 'B'},
                {'pregunta': 'Para Rosental, la cuestión fundamental de la '
                             'filosofía es la relación entre:',
                 'alternativas': ['El pensar y el ser',
                                  'La causa y el efecto',
                                  'La forma y la materia',
                                  'Lo bello y lo útil',
                                  'El bien y el mal'],
                 'correcta': 'A'},
                {'pregunta': 'La actitud filosófica se define como la '
                             'disposición por comprender:',
                 'alternativas': ['Los hechos históricos',
                                  'Únicamente lo mensurable',
                                  'El porqué y el para qué de las cosas',
                                  'Las creencias religiosas',
                                  'Solo el cómo de las cosas'],
                 'correcta': 'C'},
                {'pregunta': 'NO es una característica de la actitud '
                             'filosófica:',
                 'alternativas': ['Dogmática',
                                  'Trascendental',
                                  'Crítica',
                                  'Problemática',
                                  'Universal'],
                 'correcta': 'A'},
                {'pregunta': 'Que la actitud filosófica sea «incondicional» '
                             'significa que:',
                 'alternativas': ['Depende de la autoridad',
                                  'Persigue fines económicos',
                                  'Busca el saber por el saber mismo',
                                  'Se somete a la religión',
                                  'Acepta cualquier opinión'],
                 'correcta': 'C'},
                {'pregunta': 'La filosofía, como reflexión racional y '
                             'sistemática, se origina en:',
                 'alternativas': ['China',
                                  'Grecia',
                                  'Egipto',
                                  'Mesopotamia',
                                  'La India'],
                 'correcta': 'B'},
                {'pregunta': 'El problema fundamental de la filosofía trata '
                             'sobre la relación entre:',
                 'alternativas': ['El ser y el pensar',
                                  'El tiempo y el espacio',
                                  'El bien y el mal',
                                  'La vida y la muerte',
                                  'La razón y la fe'],
                 'correcta': 'A'},
                {'pregunta': 'El primer aspecto del problema fundamental '
                             'busca resolver si es primario:',
                 'alternativas': ['La razón o la fe',
                                  'El tiempo o el espacio',
                                  'La materia o la conciencia',
                                  'La ciencia o el arte',
                                  'El bien o el mal'],
                 'correcta': 'C'},
                {'pregunta': 'El segundo aspecto del problema fundamental '
                             'responde si el mundo es:',
                 'alternativas': ['Ordenado o caótico',
                                  'Bueno o malo',
                                  'Material o espiritual',
                                  'Finito o infinito',
                                  'Cognoscible o no'],
                 'correcta': 'E'},
                {'pregunta': 'Los filósofos que consideran que la materia es '
                             'primaria y engendra la conciencia se sitúan en '
                             'el:',
                 'alternativas': ['Idealismo',
                                  'Materialismo',
                                  'Escepticismo',
                                  'Empirismo exclusivo',
                                  'Racionalismo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los filósofos que consideran primario al '
                             'espíritu y niegan que el mundo sea cognoscible '
                             'se sitúan en el:',
                 'alternativas': ['Positivismo',
                                  'Racionalismo',
                                  'Materialismo',
                                  'Empirismo',
                                  'Idealismo'],
                 'correcta': 'E'},
                {'pregunta': 'Según Wittgenstein, la concepción de la '
                             'filosofía es la actividad orientada hacia el '
                             'esclarecimiento del:',
                 'alternativas': ['Ser y la existencia',
                                  'Lenguaje',
                                  'Poder político',
                                  'Alma humana',
                                  'Cosmos'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que analiza la '
                             'naturaleza, posibilidad y límites del '
                             'conocimiento en general se llama:',
                 'alternativas': ['Epistemología',
                                  'Gnoseología',
                                  'Axiología',
                                  'Ontología',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que es el estudio '
                             'crítico del conocimiento científico, su '
                             'fundamento y metodología, se llama:',
                 'alternativas': ['Gnoseología',
                                  'Epistemología',
                                  'Ética',
                                  'Lógica',
                                  'Antropología filosófica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia el '
                             'problema de los valores, su existencia y '
                             'naturaleza, se llama:',
                 'alternativas': ['Ética',
                                  'Axiología',
                                  'Ontología',
                                  'Estética',
                                  'Gnoseología'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia la '
                             'conducta o comportamiento moral del hombre en '
                             'sociedad se llama:',
                 'alternativas': ['Axiología',
                                  'Ética',
                                  'Ontología',
                                  'Lógica',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia los '
                             'principios y reglas para distinguir el '
                             'razonamiento correcto del incorrecto se llama:',
                 'alternativas': ['Ética',
                                  'Lógica',
                                  'Ontología',
                                  'Gnoseología',
                                  'Axiología'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que es el estudio del '
                             'ser de las cosas, del ser en tanto ser, se '
                             'llama:',
                 'alternativas': ['Gnoseología',
                                  'Ontología',
                                  'Ética',
                                  'Axiología',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que trata de lo bello '
                             'y los diferentes modos de aprehensión de '
                             'realidades bellas se llama:',
                 'alternativas': ['Ética',
                                  'Estética',
                                  'Axiología',
                                  'Ontología',
                                  'Lógica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia la '
                             'esencia del hombre, su significado y la '
                             'finalidad de su existencia, se llama:',
                 'alternativas': ['Gnoseología',
                                  'Antropología filosófica',
                                  'Ontología',
                                  'Axiología',
                                  'Lógica'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'COSMOGONÍA Y COSMOLOGÍA',
                      'items': ['Cosmogonía: de kosmos = mundo y goneia = '
                                'nacimiento. Conjunto de mitos y narraciones '
                                'con que las primeras civilizaciones '
                                'explicaron el origen del universo.',
                                'Hesíodo, en su poema «Teogonía», narra la '
                                'creación del mundo a partir del caos.',
                                'Cosmología: de kosmos y logos = estudio. '
                                'Estudia el universo mediante modelos '
                                'contrastables empírica y '
                                'experimentalmente.']},
                     {'titulo': 'TEORÍA DEL BIG BANG',
                      'items': ['Modelo cosmológico según el cual el '
                                'universo se originó en una singularidad '
                                'espaciotemporal de densidad infinita, hace '
                                'unos 14 000 millones de años.',
                                'Hubble descubrió en 1929 que la distancia '
                                'entre galaxias es cada vez mayor.',
                                'Ley de Hubble: la velocidad de una galaxia '
                                'es proporcional a su distancia.']},
                     {'titulo': 'ORIGEN Y CONCEPCIONES DE LA FILOSOFÍA',
                      'items': ['Como reflexión racional y sistemática se '
                                'origina en Grecia, siglos VII–VI a.C.',
                                'Se atribuye a Pitágoras de Samos el primer '
                                'uso del término filosofía. Sócrates se '
                                'llamó a sí mismo «amante de la sabiduría».',
                                'Platón decía que el asombro es el origen de '
                                'la filosofía; Aristóteles, que es la '
                                'admiración lo que impulsa a filosofar.']},
                     {'titulo': 'PROBLEMA FUNDAMENTAL DE LA FILOSOFÍA',
                      'items': ['El problema fundamental de la filosofía es '
                                'el carácter de la relación entre el ser y '
                                'el pensar, entre lo material y lo '
                                'espiritual.',
                                'El primer aspecto de este problema busca '
                                'resolver si la materia es lo primario, o lo '
                                'es la conciencia.',
                                'El segundo aspecto responde si el mundo es '
                                'cognoscible o no, es decir, si la razón '
                                'humana puede penetrar sus misterios.']},
                     {'titulo': 'ACTITUD FILOSÓFICA',
                      'items': ['Es la disposición humana por comprender el '
                                'porqué y el para qué de las cosas.',
                                'Características: problemática, crítica, '
                                'incondicional, universal, trascendental, '
                                'racional y reflexiva, y un saber '
                                'totalitario.']},
                     {'titulo': 'DISCIPLINAS FILOSÓFICAS',
                      'items': ['La gnoseología o Teoría del Conocimiento '
                                'analiza la naturaleza, posibilidad y '
                                'límites del conocimiento en general.',
                                'La epistemología es el estudio crítico del '
                                'conocimiento científico, su fundamento y '
                                'metodología.',
                                'La axiología estudia el problema de los '
                                'valores: su existencia, origen, naturaleza '
                                'y características.']}]},
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
                 'alternativas': ['Arjé',
                                  'Ápeiron',
                                  'Eidos',
                                  'Nous',
                                  'Logos'],
                 'correcta': 'A'},
                {'pregunta': 'Para Tales de Mileto, el principio de todas '
                             'las cosas es:',
                 'alternativas': ['El átomo',
                                  'La tierra',
                                  'El aire',
                                  'El fuego',
                                  'El agua'],
                 'correcta': 'E'},
                {'pregunta': 'El ápeiron, lo indeterminado e infinito, fue '
                             'propuesto por:',
                 'alternativas': ['Tales',
                                  'Parménides',
                                  'Anaximandro',
                                  'Anaxímenes',
                                  'Heráclito'],
                 'correcta': 'C'},
                {'pregunta': 'Para Heráclito de Éfeso, el arjé es:',
                 'alternativas': ['El ápeiron',
                                  'El aire',
                                  'El número',
                                  'El fuego',
                                  'El agua'],
                 'correcta': 'D'},
                {'pregunta': 'La frase «nadie se baña dos veces en el mismo '
                             'río» corresponde a:',
                 'alternativas': ['Demócrito',
                                  'Heráclito',
                                  'Protágoras',
                                  'Parménides',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'Parménides de Elea sostuvo que el ser es:',
                 'alternativas': ['Múltiple',
                                  'Cambiante',
                                  'Inmutable',
                                  'Material',
                                  'Divisible'],
                 'correcta': 'C'},
                {'pregunta': 'Demócrito de Abdera afirmó que todo está '
                             'compuesto por:',
                 'alternativas': ['Fuego',
                                  'Números',
                                  'Ideas',
                                  'Átomos',
                                  'Agua'],
                 'correcta': 'D'},
                {'pregunta': '«El hombre es la medida de todas las cosas» '
                             'pertenece a:',
                 'alternativas': ['Aristóteles',
                                  'Platón',
                                  'Gorgias',
                                  'Sócrates',
                                  'Protágoras'],
                 'correcta': 'E'},
                {'pregunta': 'El método socrático de dar a luz las ideas '
                             'mediante preguntas se llama:',
                 'alternativas': ['Silogismo',
                                  'Inducción',
                                  'Dialéctica',
                                  'Mayéutica',
                                  'Ironía'],
                 'correcta': 'D'},
                {'pregunta': 'La frase «solo sé que nada sé» se atribuye a:',
                 'alternativas': ['Heráclito',
                                  'Protágoras',
                                  'Epicuro',
                                  'Sócrates',
                                  'Platón'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de las Ideas fue formulada por:',
                 'alternativas': ['Sócrates',
                                  'Parménides',
                                  'Platón',
                                  'Aristóteles',
                                  'Demócrito'],
                 'correcta': 'C'},
                {'pregunta': 'Según Platón, el mundo de las Ideas eternas es '
                             'el mundo:',
                 'alternativas': ['Corpóreo',
                                  'Aparente',
                                  'Sensible',
                                  'Inteligible',
                                  'Material'],
                 'correcta': 'D'},
                {'pregunta': 'La escuela fundada por Platón fue:',
                 'alternativas': ['La Academia',
                                  'El Jardín',
                                  'El Liceo',
                                  'La Stoa',
                                  'El Pórtico'],
                 'correcta': 'A'},
                {'pregunta': 'La escuela fundada por Aristóteles fue:',
                 'alternativas': ['El Liceo',
                                  'La Academia',
                                  'El Jardín',
                                  'La Escuela de Mileto',
                                  'La Stoa'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría hilemórfica de Aristóteles sostiene '
                             'que todo ser se compone de:',
                 'alternativas': ['Acto y potencia únicamente',
                                  'Materia y forma',
                                  'Cuerpo y alma',
                                  'Idea y copia',
                                  'Ser y no ser'],
                 'correcta': 'B'},
                {'pregunta': 'Aristóteles es considerado el padre de la:',
                 'alternativas': ['Política',
                                  'Estética',
                                  'Lógica',
                                  'Ética',
                                  'Psicología'],
                 'correcta': 'C'},
                {'pregunta': 'Para Epicuro, el fin de la vida es el placer '
                             'entendido como:',
                 'alternativas': ['Ausencia de dolor y serenidad',
                                  'Fama',
                                  'Goce sensorial ilimitado',
                                  'Poder político',
                                  'Acumulación de bienes'],
                 'correcta': 'A'},
                {'pregunta': 'El estado de serenidad e imperturbabilidad en '
                             'Epicuro se denomina:',
                 'alternativas': ['Eudaimonía',
                                  'Ataraxia',
                                  'Areté',
                                  'Nous',
                                  'Catarsis'],
                 'correcta': 'B'},
                {'pregunta': 'Marco Aurelio perteneció a la escuela:',
                 'alternativas': ['Platónica',
                                  'Escéptica',
                                  'Cínica',
                                  'Epicúrea',
                                  'Estoica'],
                 'correcta': 'E'},
                {'pregunta': 'Los sofistas se caracterizaron por:',
                 'alternativas': ['Buscar verdades absolutas',
                                  'Estudiar los astros',
                                  'Enseñar retórica por dinero y defender el '
                                  'relativismo',
                                  'Fundar la lógica formal',
                                  'Rechazar la política'],
                 'correcta': 'C'},
                {'pregunta': 'Pitágoras de Samos fundó una escuela '
                             'místico-filosófica en la ciudad de:',
                 'alternativas': ['Crotona',
                                  'Mileto',
                                  'Elea',
                                  'Abdera',
                                  'Éfeso'],
                 'correcta': 'A'},
                {'pregunta': 'La doctrina pitagórica sobre la inmortalidad y '
                             'transmigración de las almas se llama:',
                 'alternativas': ['Mayéutica',
                                  'Hilozoísmo',
                                  'Reminiscencia',
                                  'Dialéctica',
                                  'Metempsicosis'],
                 'correcta': 'E'},
                {'pregunta': 'Para Pitágoras, el arjé o principio de todas '
                             'las cosas son:',
                 'alternativas': ['Los átomos',
                                  'El agua',
                                  'Los números',
                                  'El aire',
                                  'El fuego'],
                 'correcta': 'C'},
                {'pregunta': 'El número considerado más valorado por los '
                             'pitagóricos, representado en la tetraktys, fue '
                             'el:',
                 'alternativas': ['100', '7', '10', '4', '1'],
                 'correcta': 'C'},
                {'pregunta': 'El filósofo con quien se inicia la Metafísica '
                             'y el conocimiento científico fue:',
                 'alternativas': ['Pitágoras',
                                  'Tales de Mileto',
                                  'Demócrito',
                                  'Heráclito',
                                  'Parménides de Elea'],
                 'correcta': 'E'},
                {'pregunta': 'La afirmación ontológica central de Parménides '
                             'fue:',
                 'alternativas': ['«Todo fluye»',
                                  '«Solo sé que nada sé»',
                                  '«El hombre es la medida de todas las '
                                  'cosas»',
                                  '«El ser es»',
                                  '«Conócete a ti mismo»'],
                 'correcta': 'D'},
                {'pregunta': 'Para Parménides, admitir el cambio o devenir '
                             'equivale a admitir:',
                 'alternativas': ['El arjé',
                                  'El no ser',
                                  'El ser',
                                  'El logos',
                                  'La razón'],
                 'correcta': 'B'},
                {'pregunta': 'Parménides formuló, aunque de manera '
                             'implícita, el principio lógico de:',
                 'alternativas': ['Tercero excluido exclusivo',
                                  'Causalidad',
                                  'Identidad',
                                  'Razón suficiente',
                                  'No contradicción exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'Demócrito desarrolló su teoría atómica a '
                             'partir de las ideas de su maestro:',
                 'alternativas': ['Pitágoras',
                                  'Leucipo',
                                  'Parménides',
                                  'Anaximandro',
                                  'Tales'],
                 'correcta': 'B'},
                {'pregunta': 'El sofista considerado el creador de la '
                             'sofística, autor de «Sobre la naturaleza o el '
                             'no ser», fue:',
                 'alternativas': ['Sócrates',
                                  'Antístenes',
                                  'Trasímaco',
                                  'Protágoras',
                                  'Gorgias'],
                 'correcta': 'E'},
                {'pregunta': 'Gorgias sostenía, entre sus tres tesis, que si '
                             'algo existiera:',
                 'alternativas': ['No podría ser conocido por el hombre',
                                  'Sería visible para todos',
                                  'Se transformaría en fuego',
                                  'Sería eterno',
                                  'Sería material'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'LOS PRESOCRÁTICOS',
                      'items': ['Buscaron el arjé: el principio u origen de '
                                'todas las cosas.',
                                'Tales de Mileto: el principio de todo es el '
                                'agua. Fundador de la Escuela Jónica, '
                                'considerado el primer filósofo.',
                                'Anaximandro: el arjé es el ápeiron, lo '
                                'indeterminado e infinito.',
                                'Anaxímenes: el principio es el aire.',
                                'Heráclito de Éfeso: el arjé es el fuego; '
                                'todo cambia —«nadie se baña dos veces en el '
                                'mismo río»—. Doctrina del devenir.',
                                'Pitágoras de Samos fundó en Crotona una '
                                'escuela místico-filosófica basada en la '
                                'doctrina de la metempsicosis, la '
                                'transmigración de las almas.']},
                     {'titulo': 'SOFISTAS Y SÓCRATES',
                      'items': ['Los sofistas enseñaban retórica a cambio de '
                                'dinero y defendían el relativismo.',
                                'Protágoras: «el hombre es la medida de '
                                'todas las cosas».',
                                'Gorgias de Leontinos fue considerado el '
                                'creador de la sofística; sostuvo en su '
                                'tratado «Sobre la naturaleza o el no ser» '
                                'tres tesis: nada existe, si algo existiera '
                                'no podría conocerse, y si pudiera conocerse '
                                'no podría comunicarse.',
                                'Sócrates se opuso al relativismo; su método '
                                'fue la mayéutica, el arte de dar a luz '
                                'ideas mediante preguntas.',
                                'Su lema fue «conócete a ti mismo» y '
                                'afirmaba «solo sé que nada sé».']},
                     {'titulo': 'PLATÓN Y ARISTÓTELES',
                      'items': ['Platón: teoría de las Ideas. Existen dos '
                                'mundos: el sensible, cambiante y aparente, '
                                'y el inteligible, de las Ideas eternas.',
                                'Su alegoría más famosa es el mito de la '
                                'caverna. Fundó la Academia.',
                                'Aristóteles: discípulo de Platón; fundó el '
                                'Liceo. Rechazó el mundo separado de las '
                                'Ideas.',
                                'Sostuvo que todo ser se compone de materia '
                                'y forma: teoría hilemórfica.',
                                'Distinguió cuatro causas: material, formal, '
                                'eficiente y final. Es el padre de la '
                                'lógica.']},
                     {'titulo': 'EPICURO Y EL ESTOICISMO',
                      'items': ['Epicuro de Samos: el fin de la vida es el '
                                'placer entendido como ausencia de dolor y '
                                'serenidad o ataraxia.',
                                'Marco Aurelio, emperador y filósofo '
                                'estoico, sostuvo que se debe vivir conforme '
                                'a la razón y aceptar el destino.']}]},
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
                 'alternativas': ['Teocéntrico',
                                  'Antropocéntrico',
                                  'Empírico',
                                  'Logocéntrico',
                                  'Cosmocéntrico'],
                 'correcta': 'A'},
                {'pregunta': 'En la Edad Media la filosofía fue considerada:',
                 'alternativas': ['Sierva de la teología',
                                  'Independiente de la fe',
                                  'Un arte liberal menor',
                                  'Ciencia suprema',
                                  'Sinónimo de retórica'],
                 'correcta': 'A'},
                {'pregunta': 'El problema central de la filosofía medieval '
                             'fue la relación entre:',
                 'alternativas': ['Bien y mal',
                                  'Cuerpo y alma',
                                  'Ser y pensar',
                                  'Razón y fe',
                                  'Materia y forma'],
                 'correcta': 'D'},
                {'pregunta': 'San Agustín de Hipona estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Epicuro',
                                  'Aristóteles',
                                  'Platón',
                                  'Demócrito',
                                  'Los estoicos'],
                 'correcta': 'C'},
                {'pregunta': 'Una obra fundamental de San Agustín es:',
                 'alternativas': ['La ciudad de Dios',
                                  'La República',
                                  'Suma Teológica',
                                  'El Príncipe',
                                  'Órganon'],
                 'correcta': 'A'},
                {'pregunta': 'La doctrina agustiniana según la cual Dios '
                             'ilumina la mente humana se llama:',
                 'alternativas': ['Revelación',
                                  'Emanación',
                                  'Analogía',
                                  'Iluminación',
                                  'Predestinación'],
                 'correcta': 'D'},
                {'pregunta': '«Cree para comprender y comprende para creer» '
                             'corresponde a:',
                 'alternativas': ['San Agustín',
                                  'Maquiavelo',
                                  'Aristóteles',
                                  'Platón',
                                  'Santo Tomás'],
                 'correcta': 'A'},
                {'pregunta': 'La etapa de los Padres de la Iglesia se '
                             'denomina:',
                 'alternativas': ['Humanismo',
                                  'Renacimiento',
                                  'Escolástica',
                                  'Ilustración',
                                  'Patrística'],
                 'correcta': 'E'},
                {'pregunta': 'Santo Tomás de Aquino estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Platón',
                                  'Parménides',
                                  'Aristóteles',
                                  'Heráclito',
                                  'Epicuro'],
                 'correcta': 'C'},
                {'pregunta': 'La obra principal de Santo Tomás de Aquino es:',
                 'alternativas': ['Suma Teológica',
                                  'Confesiones',
                                  'La ciudad de Dios',
                                  'El Príncipe',
                                  'Metafísica'],
                 'correcta': 'A'},
                {'pregunta': 'Santo Tomás formuló para demostrar la '
                             'existencia de Dios:',
                 'alternativas': ['Cuatro causas',
                                  'Dos silogismos',
                                  'Las cinco vías',
                                  'Tres pruebas',
                                  'Siete argumentos'],
                 'correcta': 'C'},
                {'pregunta': 'Para Santo Tomás, la razón y la fe:',
                 'alternativas': ['Se contradicen',
                                  'Se complementan',
                                  'No se relacionan',
                                  'Se excluyen',
                                  'Son idénticas'],
                 'correcta': 'B'},
                {'pregunta': 'La escolástica se basó como método en:',
                 'alternativas': ['La observación astronómica',
                                  'El diálogo socrático',
                                  'La introspección',
                                  'La experimentación',
                                  'La disputa y el comentario de textos'],
                 'correcta': 'E'},
                {'pregunta': 'El Renacimiento se caracterizó por el:',
                 'alternativas': ['Antropocentrismo',
                                  'Geocentrismo',
                                  'Teocentrismo',
                                  'Dogmatismo',
                                  'Escepticismo'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de «El Príncipe» fue:',
                 'alternativas': ['Galileo',
                                  'Descartes',
                                  'Nicolás Maquiavelo',
                                  'Erasmo',
                                  'Tomás Moro'],
                 'correcta': 'C'},
                {'pregunta': 'Maquiavelo es conocido por separar la política '
                             'de:',
                 'alternativas': ['La religión únicamente',
                                  'La historia',
                                  'El derecho',
                                  'La moral',
                                  'La economía'],
                 'correcta': 'D'},
                {'pregunta': 'La máxima «el fin justifica los medios» se '
                             'atribuye a:',
                 'alternativas': ['San Agustín',
                                  'Santo Tomás',
                                  'Platón',
                                  'Maquiavelo',
                                  'Epicuro'],
                 'correcta': 'D'},
                {'pregunta': 'El Renacimiento recuperó la cultura:',
                 'alternativas': ['Egipcia',
                                  'Medieval',
                                  'Germánica',
                                  'Grecolatina',
                                  'Oriental'],
                 'correcta': 'D'},
                {'pregunta': 'El movimiento que valoró la dignidad y las '
                             'capacidades del ser humano se llamó:',
                 'alternativas': ['Escepticismo',
                                  'Estoicismo',
                                  'Humanismo',
                                  'Positivismo',
                                  'Escolasticismo'],
                 'correcta': 'C'},
                {'pregunta': 'La expresión latina «ancilla theologiae» '
                             'significa que la filosofía era:',
                 'alternativas': ['Madre de la lógica',
                                  'Sierva de la teología',
                                  'Reina de las ciencias',
                                  'Enemiga de la fe',
                                  'Base de la política'],
                 'correcta': 'B'},
                {'pregunta': 'El astrónomo polaco que formuló la teoría '
                             'heliocéntrica en el Renacimiento fue:',
                 'alternativas': ['Tycho Brahe',
                                  'Giordano Bruno',
                                  'Johannes Kepler',
                                  'Nicolás Copérnico',
                                  'Galileo Galilei'],
                 'correcta': 'D'},
                {'pregunta': 'La obra de Copérnico que expone la teoría '
                             'heliocéntrica se titula:',
                 'alternativas': ['Diálogo sobre los dos máximos sistemas',
                                  'Sidereus Nuncius',
                                  'Almagesto',
                                  'De Revolutionibus Orbium Coelestium',
                                  'Novum Organum'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría heliocéntrica de Copérnico resolvía '
                             'los problemas del modelo geocéntrico planteado '
                             'por:',
                 'alternativas': ['Ptolomeo',
                                  'Platón',
                                  'Pitágoras',
                                  'Aristóteles',
                                  'Eratóstenes'],
                 'correcta': 'A'},
                {'pregunta': 'San Agustín de Hipona nació en la ciudad de '
                             'Tagaste, ubicada en la actual:',
                 'alternativas': ['Argelia',
                                  'Libia',
                                  'Marruecos',
                                  'Túnez',
                                  'Egipto'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CARACTERÍSTICAS DE LA EDAD MEDIA',
                      'items': ['El pensamiento medieval fue teocéntrico: '
                                'Dios es el centro de toda explicación.',
                                'La filosofía fue considerada sierva de la '
                                'teología («ancilla theologiae»).',
                                'Problema central: la relación entre razón y '
                                'fe.']},
                     {'titulo': 'LA PATRÍSTICA',
                      'items': ['Etapa de los Padres de la Iglesia, que '
                                'defendieron el cristianismo frente al '
                                'paganismo.',
                                'San Agustín de Hipona: influido por Platón. '
                                'Obras «Confesiones» y «La ciudad de Dios».',
                                'Sostuvo la doctrina de la iluminación: Dios '
                                'ilumina la mente para conocer la verdad.',
                                'Su lema fue «cree para comprender y '
                                'comprende para creer».',
                                'San Agustín nació en Tagaste, en la actual '
                                'Argelia.']},
                     {'titulo': 'LA ESCOLÁSTICA',
                      'items': ['Método de enseñanza medieval basado en la '
                                'disputa y el comentario de textos.',
                                'Santo Tomás de Aquino: influido por '
                                'Aristóteles. Su obra principal es la «Suma '
                                'Teológica».',
                                'Formuló las cinco vías para demostrar '
                                'racionalmente la existencia de Dios.',
                                'Sostuvo que razón y fe no se contradicen, '
                                'sino que se complementan.']},
                     {'titulo': 'EL RENACIMIENTO',
                      'items': ['Se caracteriza por el antropocentrismo: el '
                                'hombre pasa a ser el centro.',
                                'Recuperación de la cultura grecolatina y '
                                'valoración del humanismo.',
                                'Nicolás Copérnico, astrónomo polaco '
                                '(1473-1543), formuló la teoría '
                                'heliocéntrica: la Tierra gira sobre su eje '
                                'y orbita alrededor del Sol.',
                                'Su obra «De Revolutionibus Orbium '
                                'Coelestium» resolvía los problemas del '
                                'modelo geocéntrico de Ptolomeo.',
                                'Nicolás Maquiavelo: autor de «El Príncipe». '
                                'Separó la política de la moral; se le '
                                'atribuye la máxima «el fin justifica los '
                                'medios».']}]},
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
                 'alternativas': ['Hegel',
                                  'Kant',
                                  'Locke',
                                  'René Descartes',
                                  'Bacon'],
                 'correcta': 'D'},
                {'pregunta': 'El principio «pienso, luego existo» pertenece '
                             'a:',
                 'alternativas': ['Kant',
                                  'Hegel',
                                  'Descartes',
                                  'Locke',
                                  'Marx'],
                 'correcta': 'C'},
                {'pregunta': 'El método cartesiano parte de:',
                 'alternativas': ['La duda metódica',
                                  'La experiencia sensible',
                                  'La revelación',
                                  'La observación',
                                  'La inducción'],
                 'correcta': 'A'},
                {'pregunta': 'Para el empirismo, todo conocimiento proviene '
                             'de:',
                 'alternativas': ['La revelación',
                                  'La experiencia',
                                  'La razón pura',
                                  'La intuición',
                                  'Las ideas innatas'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke sostuvo que la mente al nacer es:',
                 'alternativas': ['Una tabla rasa',
                                  'Un reflejo divino',
                                  'Un espejo del cosmos',
                                  'Una sustancia pensante',
                                  'Un depósito de ideas innatas'],
                 'correcta': 'A'},
                {'pregunta': 'La síntesis entre racionalismo y empirismo fue '
                             'realizada por:',
                 'alternativas': ['Hegel',
                                  'Marx',
                                  'Descartes',
                                  'Kant',
                                  'Locke'],
                 'correcta': 'D'},
                {'pregunta': 'El lema «atrévete a saber» corresponde a:',
                 'alternativas': ['Marx',
                                  'Hegel',
                                  'Kant',
                                  'Mariátegui',
                                  'Descartes'],
                 'correcta': 'C'},
                {'pregunta': 'Kant llamó «noúmeno» a:',
                 'alternativas': ['La idea innata',
                                  'El juicio sintético',
                                  'La cosa en sí, incognoscible',
                                  'Lo que aparece a los sentidos',
                                  'El imperativo moral'],
                 'correcta': 'C'},
                {'pregunta': 'El imperativo categórico de Kant exige obrar '
                             'de modo que la acción pueda ser:',
                 'alternativas': ['Aprobada socialmente',
                                  'Útil para uno mismo',
                                  'Rentable',
                                  'Ley universal',
                                  'Placentera'],
                 'correcta': 'D'},
                {'pregunta': 'Los tres momentos de la dialéctica hegeliana '
                             'son:',
                 'alternativas': ['Duda, método y certeza',
                                  'Causa, efecto y fin',
                                  'Tesis, antítesis y síntesis',
                                  'Ser, no ser y devenir',
                                  'Materia, forma y acto'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema filosófico de Hegel es:',
                 'alternativas': ['Empirista',
                                  'Materialista',
                                  'Escéptico',
                                  'Positivista',
                                  'Idealista'],
                 'correcta': 'E'},
                {'pregunta': 'Marx invirtió la dialéctica de Hegel y '
                             'desarrolló:',
                 'alternativas': ['El criticismo',
                                  'El pragmatismo',
                                  'El empirismo',
                                  'El idealismo absoluto',
                                  'El materialismo dialéctico e histórico'],
                 'correcta': 'E'},
                {'pregunta': 'Para Marx, la infraestructura económica '
                             'determina:',
                 'alternativas': ['El lenguaje únicamente',
                                  'La superestructura jurídica, política e '
                                  'ideológica',
                                  'El clima',
                                  'La geografía',
                                  'La biología'],
                 'correcta': 'B'},
                {'pregunta': '«Los filósofos se han limitado a interpretar '
                             'el mundo; de lo que se trata es de '
                             'transformarlo» pertenece a:',
                 'alternativas': ['Marx',
                                  'Hegel',
                                  'Kant',
                                  'Salazar Bondy',
                                  'Mariátegui'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de «7 ensayos de interpretación de la '
                             'realidad peruana» es:',
                 'alternativas': ['Augusto Salazar Bondy',
                                  'Francisco Miró Quesada',
                                  'José Carlos Mariátegui',
                                  'Víctor Raúl Haya de la Torre',
                                  'González Prada'],
                 'correcta': 'C'},
                {'pregunta': 'Para Mariátegui, el problema del indio es '
                             'fundamentalmente un problema:',
                 'alternativas': ['Religioso',
                                  'Educativo',
                                  'Racial',
                                  'Administrativo',
                                  'De la tierra'],
                 'correcta': 'E'},
                {'pregunta': 'El autor de «¿Existe una filosofía de nuestra '
                             'América?» es:',
                 'alternativas': ['Augusto Salazar Bondy',
                                  'Francisco Miró Quesada',
                                  'Mariátegui',
                                  'Antenor Orrego',
                                  'Alejandro Deustua'],
                 'correcta': 'A'},
                {'pregunta': 'Según Salazar Bondy, la filosofía '
                             'latinoamericana ha sido:',
                 'alternativas': ['Imitativa, reflejo de una sociedad '
                                  'dominada',
                                  'Inexistente',
                                  'Original y autónoma',
                                  'Superior a la europea',
                                  'Puramente científica'],
                 'correcta': 'A'},
                {'pregunta': 'Mariátegui aplicó al análisis del Perú el '
                             'método:',
                 'alternativas': ['Positivista',
                                  'Existencialista',
                                  'Escolástico',
                                  'Fenomenológico',
                                  'Marxista'],
                 'correcta': 'E'},
                {'pregunta': 'El criticismo kantiano sostiene que el '
                             'conocimiento resulta de:',
                 'alternativas': ['Solo la razón',
                                  'La revelación divina',
                                  'La unión de razón y experiencia',
                                  'Solo los sentidos',
                                  'La tradición'],
                 'correcta': 'C'},
                {'pregunta': 'El filósofo inglés materialista que propuso el '
                             'método inductivo en su obra Novum Organum fue:',
                 'alternativas': ['John Locke',
                                  'Thomas Aquino',
                                  'David Hume',
                                  'Tomás Hobbes',
                                  'Francisco Bacon'],
                 'correcta': 'E'},
                {'pregunta': 'Bacon sostuvo que antes de investigar hay que '
                             'eliminar de la mente los:',
                 'alternativas': ['Postulados',
                                  'Silogismos',
                                  'Dogmas',
                                  'Ídolos',
                                  'Axiomas'],
                 'correcta': 'D'},
                {'pregunta': 'El ídolo baconiano que consiste en interpretar '
                             'antropomórficamente la naturaleza se llama '
                             'ídolo de la:',
                 'alternativas': ['Foro',
                                  'Tribu',
                                  'Ciudad',
                                  'Teatro',
                                  'Caverna'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano originado en los prejuicios '
                             'personales de cada individuo se llama ídolo de '
                             'la:',
                 'alternativas': ['Teatro',
                                  'Foro',
                                  'Escuela',
                                  'Caverna',
                                  'Tribu'],
                 'correcta': 'D'},
                {'pregunta': 'El ídolo baconiano relacionado con el mal uso '
                             'del lenguaje se llama ídolo del:',
                 'alternativas': ['Templo',
                                  'Foro',
                                  'Tribu',
                                  'Teatro',
                                  'Palacio'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano relacionado con la '
                             'aceptación acrítica de autoridades se llama '
                             'ídolo del:',
                 'alternativas': ['Teatro',
                                  'Caverna',
                                  'Mercado',
                                  'Foro',
                                  'Tribu'],
                 'correcta': 'A'},
                {'pregunta': 'Descartes distinguió tres sustancias: la res '
                             'extensa, la res necesaria y la:',
                 'alternativas': ['Res naturae',
                                  'Res finita',
                                  'Res divina exclusiva',
                                  'Res cogitans',
                                  'Res publica'],
                 'correcta': 'D'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'espiritual, cuya esencia es el pensamiento, se '
                             'llama:',
                 'alternativas': ['Res corporal',
                                  'Res mundi',
                                  'Res necesaria',
                                  'Res cogitans',
                                  'Res extensa'],
                 'correcta': 'D'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'corporal, cuya esencia es la extensión, se '
                             'llama:',
                 'alternativas': ['Res cogitans',
                                  'Res extensa',
                                  'Res divina',
                                  'Res mentis',
                                  'Res necesaria'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke distinguió dos tipos de '
                             'experiencia: la interna y la:',
                 'alternativas': ['Innata',
                                  'Trascendental',
                                  'Racional',
                                  'Espiritual',
                                  'Externa'],
                 'correcta': 'E'},
                {'pregunta': 'La experiencia que surge cuando la mente '
                             'reflexiona sobre sus propias sensaciones, '
                             'según Locke, se llama experiencia:',
                 'alternativas': ['Interna',
                                  'Externa',
                                  'Sensorial exclusiva',
                                  'Innata',
                                  'Trascendental'],
                 'correcta': 'A'},
                {'pregunta': 'Tomás Hobbes sostuvo que en estado natural el '
                             'hombre es:',
                 'alternativas': ['Racional puro',
                                  'Antisocial, movido por el deseo y el '
                                  'temor',
                                  'Altruista',
                                  'Pacífico por instinto',
                                  'Sociable por naturaleza'],
                 'correcta': 'B'},
                {'pregunta': 'La célebre frase de Hobbes que describe la '
                             'naturaleza humana en estado natural es:',
                 'alternativas': ['«El hombre es un lobo para el hombre»',
                                  '«El hombre es un junco pensante»',
                                  '«El hombre es un animal político»',
                                  '«El hombre nace bueno»',
                                  '«El hombre es la medida de todas las '
                                  'cosas»'],
                 'correcta': 'A'},
                {'pregunta': 'Según Hobbes, para superar el estado de guerra '
                             'de todos contra todos, los hombres deben '
                             'establecer un:',
                 'alternativas': ['Sistema feudal',
                                  'Gobierno directo',
                                  'Concilio religioso',
                                  'Imperio universal',
                                  'Contrato social'],
                 'correcta': 'E'},
                {'pregunta': 'La obra más conocida de Hobbes, donde expone '
                             'su teoría del contrato social, es:',
                 'alternativas': ['Utopía',
                                  'El Leviatán',
                                  'El Contrato Social',
                                  'Dos Tratados sobre el Gobierno',
                                  'El Príncipe'],
                 'correcta': 'B'},
                {'pregunta': 'Friedrich Nietzsche es considerado el filósofo '
                             'más importante del siglo XIX en la corriente '
                             'del:',
                 'alternativas': ['Positivismo',
                                  'Voluntarismo',
                                  'Empirismo',
                                  'Racionalismo',
                                  'Idealismo absoluto'],
                 'correcta': 'B'},
                {'pregunta': 'Nietzsche estuvo influenciado principalmente '
                             'por el filósofo:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Locke',
                                  'Schopenhauer',
                                  'Hegel'],
                 'correcta': 'D'},
                {'pregunta': 'Nietzsche distinguió la moral del amo, que '
                             'exalta la fuerza, de la moral:',
                 'alternativas': ['Científica',
                                  'Del esclavo',
                                  'Racional',
                                  'Universal',
                                  'Divina'],
                 'correcta': 'B'},
                {'pregunta': 'Para Nietzsche, la moral del esclavo, que '
                             'exalta la compasión y la resignación, es la '
                             'moral de los:',
                 'alternativas': ['Filósofos griegos',
                                  'Guerreros',
                                  'Comerciantes',
                                  'Cristianos',
                                  'Científicos'],
                 'correcta': 'D'},
                {'pregunta': 'Nietzsche proclamó una idea célebre conocida '
                             'como:',
                 'alternativas': ['El regreso de Dios',
                                  'El nacimiento de Dios',
                                  'La duda de Dios',
                                  'El silencio de Dios',
                                  'La muerte de Dios'],
                 'correcta': 'E'},
                {'pregunta': 'El ideal nietzscheano del hombre que acepta la '
                             'muerte de Dios y vive fiel a la tierra se '
                             'llama:',
                 'alternativas': ['El hombre justo',
                                  'El hombre virtuoso',
                                  'El hombre racional',
                                  'El superhombre',
                                  'El hombre sabio'],
                 'correcta': 'D'},
                {'pregunta': 'Una de las obras principales de Nietzsche es:',
                 'alternativas': ['Utopía',
                                  'El Príncipe',
                                  'Así habló Zaratustra',
                                  'Confesiones',
                                  'El Leviatán'],
                 'correcta': 'C'},
                {'pregunta': 'Manuel González Prada mostró su inclinación '
                             'filosófica hacia el:',
                 'alternativas': ['Idealismo',
                                  'Empirismo puro',
                                  'Racionalismo',
                                  'Existencialismo',
                                  'Positivismo'],
                 'correcta': 'E'},
                {'pregunta': 'El balance que hizo González Prada de la '
                             'Independencia del Perú fue:',
                 'alternativas': ['Neutral',
                                  'Triunfalista',
                                  'Indiferente',
                                  'Optimista',
                                  'Pesimista'],
                 'correcta': 'E'},
                {'pregunta': 'Según González Prada, la derrota del Perú en '
                             'la Guerra del Pacífico se debió principalmente '
                             'a:',
                 'alternativas': ['La falta de armamento',
                                  'La ignorancia y el espíritu de '
                                  'servidumbre',
                                  'La superioridad militar chilena '
                                  'exclusivamente',
                                  'El clima',
                                  'La distancia geográfica'],
                 'correcta': 'B'},
                {'pregunta': 'González Prada consideraba que el Estado era '
                             'un instrumento de los poderosos para '
                             'perpetuar:',
                 'alternativas': ['El progreso',
                                  'La servidumbre de los más débiles',
                                  'La educación',
                                  'El comercio',
                                  'La ciencia'],
                 'correcta': 'B'},
                {'pregunta': 'Para González Prada, el Perú verdadero y '
                             'profundo es el que pertenece a:',
                 'alternativas': ['Los indígenas',
                                  'El clero',
                                  'Los extranjeros',
                                  'La oligarquía',
                                  'Los criollos'],
                 'correcta': 'A'},
                {'pregunta': 'La obra principal de González Prada, que '
                             'influyó en Mariátegui y Haya de la Torre, es:',
                 'alternativas': ['Anarquía',
                                  'El Perú profundo',
                                  'Horas de lucha',
                                  'Nuevas páginas libres',
                                  'Páginas Libres'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'RACIONALISMO Y EMPIRISMO',
                      'items': ['Francisco Bacon, materialista inglés, '
                                'propuso el método inductivo en su obra '
                                '«Novum Organum».',
                                'Bacon sostuvo que antes de investigar hay '
                                'que eliminar los ídolos de la mente: '
                                'prejuicios que impiden el conocimiento '
                                'verdadero.',
                                'Los cuatro ídolos de Bacon son: de la tribu '
                                '(interpretación antropomórfica), de la '
                                'caverna (prejuicios personales), del foro '
                                '(mal uso del lenguaje) y del teatro '
                                '(aceptación acrítica de autoridades).']},
                     {'titulo': 'THOMAS HOBBES Y EL CONTRATO SOCIAL',
                      'items': ['Tomás Hobbes, filósofo inglés, sostuvo que '
                                'las leyes que rigen al hombre son las '
                                'mismas que rigen el universo.',
                                'Para Hobbes, en estado natural el hombre es '
                                'antisocial y se mueve por el deseo y el '
                                'temor.',
                                'Su célebre frase «el hombre es un lobo para '
                                'el hombre» describe el estado de «guerra de '
                                'todos contra todos».']},
                     {'titulo': 'KANT Y HEGEL',
                      'items': ['Immanuel Kant: realizó la síntesis entre '
                                'racionalismo y empirismo, llamada '
                                'criticismo. Su lema fue «atrévete a saber» '
                                '(sapere aude).',
                                'Distinguió el fenómeno, lo que podemos '
                                'conocer, del noúmeno o cosa en sí, '
                                'incognoscible.',
                                'En ética formuló el imperativo categórico: '
                                'obra de tal modo que tu acción pueda '
                                'convertirse en ley universal.']},
                     {'titulo': 'FRIEDRICH NIETZSCHE',
                      'items': ['Friedrich Nietzsche es considerado el '
                                'filósofo más importante del voluntarismo '
                                'del siglo XIX.',
                                'Estuvo influenciado por Schopenhauer y su '
                                'obra «El mundo como voluntad y '
                                'representación».',
                                'Distinguió dos tipos de moral: la moral del '
                                'amo, que exalta la fuerza y la nobleza, y '
                                'la moral del esclavo, que exalta la '
                                'compasión y la resignación.']},
                     {'titulo': 'MARX Y EL MATERIALISMO',
                      'items': ['Carlos Marx: invirtió la dialéctica de '
                                'Hegel y creó el materialismo dialéctico e '
                                'histórico.',
                                'Sostuvo que la infraestructura económica '
                                'determina la superestructura jurídica, '
                                'política e ideológica.',
                                '«Los filósofos se han limitado a '
                                'interpretar el mundo; de lo que se trata es '
                                'de transformarlo».']},
                     {'titulo': 'MANUEL GONZÁLEZ PRADA',
                      'items': ['Manuel González Prada (1846-1918) mostró su '
                                'inclinación al positivismo peruano, como '
                                'respuesta a la crisis tras el caudillismo y '
                                'la guerra con Chile.',
                                'Su balance de la Independencia peruana fue '
                                'pesimista: la calificó de una «orgía» que '
                                'dejó heces, manchada por la guerra civil.',
                                'Según González Prada, la ignorancia y el '
                                'espíritu de servidumbre determinaron la '
                                'derrota del Perú en la Guerra del '
                                'Pacífico.']},
                     {'titulo': 'FILOSOFÍA EN EL PERÚ',
                      'items': ['José Carlos Mariátegui: autor de «7 ensayos '
                                'de interpretación de la realidad peruana». '
                                'Aplicó el marxismo al análisis del Perú, '
                                'señalando que el problema del indio es un '
                                'problema de la tierra.',
                                'Augusto Salazar Bondy: autor de «¿Existe '
                                'una filosofía de nuestra América?». Sostuvo '
                                'que nuestra filosofía ha sido imitativa por '
                                'ser reflejo de una sociedad dominada.']}]},
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
                 'alternativas': ['Ontología',
                                  'Axiología',
                                  'Gnoseología',
                                  'Antropología filosófica',
                                  'Ética'],
                 'correcta': 'D'},
                {'pregunta': 'La antropología filosófica se diferencia de la '
                             'cultural porque:',
                 'alternativas': ['Analiza idiomas',
                                  'Estudia fósiles',
                                  'Describe costumbres',
                                  'Reflexiona sobre el ser del hombre',
                                  'Mide cráneos'],
                 'correcta': 'D'},
                {'pregunta': 'El creacionismo sostiene que el hombre fue:',
                 'alternativas': ['Resultado de mutaciones',
                                  'Fruto de la evolución',
                                  'Autogenerado',
                                  'Creado por un ser superior',
                                  'Producto del azar'],
                 'correcta': 'D'},
                {'pregunta': 'El mito griego que explica el origen del '
                             'hombre mediante un titán es el de:',
                 'alternativas': ['Sísifo',
                                  'Narciso',
                                  'Prometeo',
                                  'Ícaro',
                                  'Edipo'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría de la evolución por selección '
                             'natural fue formulada por:',
                 'alternativas': ['De Vries',
                                  'Mendel',
                                  'Wallace únicamente',
                                  'Lamarck',
                                  'Charles Darwin'],
                 'correcta': 'E'},
                {'pregunta': 'El neodarwinismo complementa a Darwin con los '
                             'aportes de:',
                 'alternativas': ['La teología',
                                  'La geología',
                                  'La genética y las mutaciones',
                                  'La astronomía',
                                  'La lingüística'],
                 'correcta': 'C'},
                {'pregunta': 'Como ser natural, el hombre se caracteriza '
                             'por:',
                 'alternativas': ['Producir cultura',
                                  'Crear valores',
                                  'Poseer un cuerpo biológico sujeto a leyes '
                                  'naturales',
                                  'Ser libre',
                                  'Su capacidad simbólica'],
                 'correcta': 'C'},
                {'pregunta': 'Como ser espiritual, el hombre posee:',
                 'alternativas': ['Conciencia, libertad y capacidad de crear '
                                  'cultura',
                                  'Solo necesidades biológicas',
                                  'Instintos',
                                  'Únicamente sensaciones',
                                  'Reflejos condicionados'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión «zoon politikon», que define al '
                             'hombre como ser social, es de:',
                 'alternativas': ['Rousseau',
                                  'Platón',
                                  'Sócrates',
                                  'Hobbes',
                                  'Aristóteles'],
                 'correcta': 'E'},
                {'pregunta': 'Lo que distingue al hombre del resto de '
                             'animales, según la antropología filosófica, '
                             'es:',
                 'alternativas': ['Su fuerza física',
                                  'Su tamaño',
                                  'Su racionalidad y capacidad simbólica',
                                  'Su alimentación',
                                  'Su longevidad'],
                 'correcta': 'C'},
                {'pregunta': 'La capacidad humana de transformar la '
                             'naturaleza mediante la actividad consciente '
                             'es:',
                 'alternativas': ['La adaptación pasiva',
                                  'El reflejo',
                                  'La mutación',
                                  'El instinto',
                                  'El trabajo'],
                 'correcta': 'E'},
                {'pregunta': 'La tradición judeocristiana corresponde a la '
                             'teoría:',
                 'alternativas': ['Neodarwinista',
                                  'Materialista',
                                  'Positivista',
                                  'Evolucionista',
                                  'Creacionista'],
                 'correcta': 'E'},
                {'pregunta': 'El hombre es considerado un ser bidimensional '
                             'porque es a la vez:',
                 'alternativas': ['Bueno y malo',
                                  'Racional e irracional',
                                  'Natural y espiritual',
                                  'Individual y aislado',
                                  'Joven y viejo'],
                 'correcta': 'C'},
                {'pregunta': 'El lenguaje simbólico es una característica:',
                 'alternativas': ['Compartida con todos los animales',
                                  'Exclusiva de los primates',
                                  'Puramente instintiva',
                                  'Innata y no aprendida',
                                  'Propia del ser humano'],
                 'correcta': 'E'},
                {'pregunta': 'La antropología filosófica se pregunta '
                             'fundamentalmente por:',
                 'alternativas': ['Los restos arqueológicos',
                                  'La anatomía comparada',
                                  'La distribución geográfica',
                                  'Las costumbres de los pueblos',
                                  'La esencia y el sentido de la existencia '
                                  'humana'],
                 'correcta': 'E'},
                {'pregunta': 'La cultura, según la antropología filosófica, '
                             'es producto de la dimensión:',
                 'alternativas': ['Espiritual',
                                  'Genética',
                                  'Refleja',
                                  'Biológica',
                                  'Instintiva'],
                 'correcta': 'A'},
                {'pregunta': 'La libertad humana implica fundamentalmente la '
                             'capacidad de:',
                 'alternativas': ['Evitar toda norma',
                                  'Seguir los instintos',
                                  'Someterse al destino',
                                  'Hacer cualquier cosa sin límites',
                                  'Elegir y responder por los propios actos'],
                 'correcta': 'E'},
                {'pregunta': 'Para el evolucionismo, el hombre y los '
                             'primates actuales comparten:',
                 'alternativas': ['Igual capacidad simbólica',
                                  'El mismo lenguaje',
                                  'Un antepasado común',
                                  'La misma cultura',
                                  'Idéntica especie'],
                 'correcta': 'C'},
                {'pregunta': 'Las necesidades e instintos corresponden a la '
                             'dimensión humana:',
                 'alternativas': ['Simbólica',
                                  'Espiritual',
                                  'Cultural',
                                  'Natural o biológica',
                                  'Axiológica'],
                 'correcta': 'D'},
                {'pregunta': 'El ser humano crea valores, normas y símbolos '
                             'porque es un ser:',
                 'alternativas': ['Determinado genéticamente',
                                  'Aislado',
                                  'Cultural y espiritual',
                                  'Puramente biológico',
                                  'Instintivo'],
                 'correcta': 'C'},
                {'pregunta': 'Los representantes de la Teoría Sintética o '
                             'Neodarwinismo son Dobzhansky, Mayr y:',
                 'alternativas': ['Lamarck',
                                  'Wallace',
                                  'Mendel',
                                  'Simpson',
                                  'Haeckel'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Disciplina filosófica que estudia al hombre '
                                'en su totalidad: su esencia, su origen y el '
                                'sentido de su existencia.',
                                'Se diferencia de la antropología cultural '
                                'porque no describe costumbres, sino que '
                                'reflexiona sobre el ser del hombre.']},
                     {'titulo': 'TEORÍAS SOBRE EL ORIGEN DEL HOMBRE',
                      'items': ['Creacionismo: el hombre fue creado por un '
                                'ser superior. Incluye la tradición '
                                'judeocristiana y el mito griego de '
                                'Prometeo.',
                                'Evolucionismo: el hombre es producto de un '
                                'proceso de evolución; formulado por Charles '
                                'Darwin mediante la selección natural.',
                                'Neodarwinismo o Teoría Sintética: '
                                'complementa a Darwin con los aportes de la '
                                'genética; sus representantes son '
                                'Dobzhansky, Mayr y Simpson.']},
                     {'titulo': 'Y 5.4 EL HOMBRE COMO SER NATURAL Y '
                                'ESPIRITUAL',
                      'items': ['Como ser natural: posee un cuerpo biológico '
                                'sujeto a las leyes de la naturaleza, con '
                                'necesidades e instintos.',
                                'Como ser espiritual: posee conciencia, '
                                'libertad, capacidad de crear cultura, '
                                'valores y símbolos.',
                                'El hombre es un ser social por naturaleza, '
                                'según Aristóteles («zoon politikon»).',
                                'Es también un ser racional, capaz de '
                                'lenguaje simbólico y de trabajo '
                                'transformador.']}]},
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
                                  'Axiología',
                                  'Gnoseología',
                                  'Lógica',
                                  'Ontología'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, gnoseología proviene de '
                             'gnosis, que significa:',
                 'alternativas': ['Ser',
                                  'Palabra',
                                  'Conocimiento',
                                  'Ley',
                                  'Valor'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento del conocimiento que designa a '
                             'quien conoce es:',
                 'alternativas': ['La imagen',
                                  'El sujeto cognoscente',
                                  'El objeto',
                                  'La verdad',
                                  'El método'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental que el sujeto elabora '
                             'del objeto se denomina:',
                 'alternativas': ['Concepto puro',
                                  'Juicio',
                                  'Idea innata',
                                  'Imagen',
                                  'Símbolo'],
                 'correcta': 'D'},
                {'pregunta': 'En el acto de conocer, el objeto:',
                 'alternativas': ['Se transforma',
                                  'Desaparece',
                                  'Se subjetiviza',
                                  'Permanece inalterado',
                                  'Se destruye'],
                 'correcta': 'D'},
                {'pregunta': 'El conocimiento obtenido a través de los '
                             'sentidos es:',
                 'alternativas': ['Racional',
                                  'Sensible',
                                  'Científico',
                                  'Universal',
                                  'Abstracto'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento sensible se caracteriza por '
                             'ser:',
                 'alternativas': ['Universal y abstracto',
                                  'Singular, concreto y subjetivo',
                                  'Deductivo',
                                  'Apriorístico',
                                  'Necesario'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento racional se caracteriza por '
                             'ser:',
                 'alternativas': ['Universal, abstracto y objetivo',
                                  'Sensorial',
                                  'Concreto',
                                  'Momentáneo',
                                  'Singular'],
                 'correcta': 'A'},
                {'pregunta': 'El conocimiento espontáneo, no verificado ni '
                             'sistemático es el:',
                 'alternativas': ['Filosófico',
                                  'Técnico',
                                  'Científico',
                                  'Teológico',
                                  'Vulgar'],
                 'correcta': 'E'},
                {'pregunta': 'El conocimiento científico se caracteriza por '
                             'ser:',
                 'alternativas': ['Metódico, sistemático y verificable',
                                  'Dogmático',
                                  'Intuitivo',
                                  'Espontáneo',
                                  'Subjetivo'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría que define la verdad como adecuación '
                             'entre el pensamiento y la realidad es la de:',
                 'alternativas': ['La coherencia',
                                  'La correspondencia',
                                  'El pragmatismo',
                                  'La utilidad',
                                  'El consenso'],
                 'correcta': 'B'},
                {'pregunta': 'La concepción clásica de la verdad se atribuye '
                             'a:',
                 'alternativas': ['Kant',
                                  'Hegel',
                                  'Descartes',
                                  'James',
                                  'Aristóteles'],
                 'correcta': 'E'},
                {'pregunta': 'Para la teoría pragmática, es verdadero '
                             'aquello que:',
                 'alternativas': ['No se contradice',
                                  'Resulta útil o funciona en la práctica',
                                  'Es evidente',
                                  'Corresponde a la realidad',
                                  'Es revelado'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría de la coherencia, un enunciado '
                             'es verdadero si:',
                 'alternativas': ['Es intuitivo',
                                  'Es útil',
                                  'No contradice al sistema del que forma '
                                  'parte',
                                  'Lo dice una autoridad',
                                  'Se comprueba experimentalmente'],
                 'correcta': 'C'},
                {'pregunta': 'Los tres elementos del conocimiento son '
                             'sujeto, objeto e:',
                 'alternativas': ['Imagen',
                                  'Interés',
                                  'Instrumento',
                                  'Interpretación',
                                  'Método'],
                 'correcta': 'A'},
                {'pregunta': 'La gnoseología estudia del conocimiento su '
                             'origen, su esencia y sus:',
                 'alternativas': ['Costos',
                                  'Aplicaciones',
                                  'Límites',
                                  'Autores',
                                  'Instrumentos'],
                 'correcta': 'C'},
                {'pregunta': 'Percibir el color rojo de una manzana '
                             'corresponde al conocimiento:',
                 'alternativas': ['Racional',
                                  'Científico',
                                  'Sensible',
                                  'Deductivo',
                                  'Abstracto'],
                 'correcta': 'C'},
                {'pregunta': 'Comprender el concepto de «justicia» '
                             'corresponde al conocimiento:',
                 'alternativas': ['Racional',
                                  'Perceptivo',
                                  'Empírico puro',
                                  'Instintivo',
                                  'Sensible'],
                 'correcta': 'A'},
                {'pregunta': 'En la relación cognoscitiva, aquello que es '
                             'conocido se denomina:',
                 'alternativas': ['Imagen',
                                  'Sujeto',
                                  'Fin',
                                  'Método',
                                  'Objeto'],
                 'correcta': 'E'},
                {'pregunta': 'La afirmación «la nieve es blanca es verdadera '
                             'si la nieve es blanca» ilustra la teoría de:',
                 'alternativas': ['La autoridad',
                                  'La correspondencia',
                                  'El consenso',
                                  'La coherencia',
                                  'El pragmatismo'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Del griego gnosis = conocimiento y logos = '
                                'estudio. Es la disciplina que estudia el '
                                'conocimiento en general: su origen, su '
                                'esencia y sus límites.']},
                     {'titulo': 'ESTRUCTURA DEL CONOCIMIENTO',
                      'items': ['El sujeto cognoscente: quien conoce.',
                                'El objeto de conocimiento: aquello que es '
                                'conocido.',
                                'La imagen o representación mental que el '
                                'sujeto elabora del objeto.',
                                'En el acto de conocer, el sujeto sale de sí '
                                'y aprehende las propiedades del objeto; el '
                                'objeto permanece inalterado.']},
                     {'titulo': 'CLASES DE CONOCIMIENTO',
                      'items': ['Conocimiento sensible: se obtiene por los '
                                'sentidos; es singular, concreto y '
                                'subjetivo.',
                                'Conocimiento lógico o racional: se obtiene '
                                'por la razón; es universal, abstracto y '
                                'objetivo.',
                                'El conocimiento vulgar es espontáneo y no '
                                'verificado; el científico es metódico, '
                                'sistemático y verificable.']},
                     {'titulo': 'LA VERDAD',
                      'items': ['Teoría de la correspondencia: la verdad es '
                                'la adecuación entre el pensamiento y la '
                                'realidad. Es la concepción clásica o '
                                'aristotélica.',
                                'Teoría pragmática: es verdadero aquello que '
                                'resulta útil o funciona en la práctica.',
                                'Teoría de la coherencia: un enunciado es '
                                'verdadero si no contradice al conjunto del '
                                'sistema.']}]},
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
                 'alternativas': ['Fenomenalismo',
                                  'Dogmatismo',
                                  'Escepticismo',
                                  'Relativismo',
                                  'Criticismo'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo niega la posibilidad de '
                             'alcanzar:',
                 'alternativas': ['La experiencia',
                                  'La razón',
                                  'El lenguaje',
                                  'Un conocimiento seguro',
                                  'La percepción'],
                 'correcta': 'D'},
                {'pregunta': 'El representante clásico del escepticismo es:',
                 'alternativas': ['Pirrón de Elis',
                                  'Descartes',
                                  'Berkeley',
                                  'Kant',
                                  'Locke'],
                 'correcta': 'A'},
                {'pregunta': 'La posición intermedia que afirma que el '
                             'conocimiento es posible pero con límites es '
                             'el:',
                 'alternativas': ['Empirismo',
                                  'Criticismo',
                                  'Dogmatismo',
                                  'Idealismo',
                                  'Escepticismo'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo fue formulado por:',
                 'alternativas': ['Hegel',
                                  'Descartes',
                                  'Hume',
                                  'Pirrón',
                                  'Kant'],
                 'correcta': 'E'},
                {'pregunta': 'Para el racionalismo, el origen del '
                             'conocimiento es:',
                 'alternativas': ['La percepción',
                                  'La razón',
                                  'La costumbre',
                                  'La experiencia',
                                  'La revelación'],
                 'correcta': 'B'},
                {'pregunta': 'El principal representante del empirismo es:',
                 'alternativas': ['Hegel',
                                  'Kant',
                                  'John Locke',
                                  'Descartes',
                                  'Platón'],
                 'correcta': 'C'},
                {'pregunta': '«Los conceptos sin intuiciones son vacíos, las '
                             'intuiciones sin conceptos son ciegas» '
                             'corresponde a:',
                 'alternativas': ['Locke',
                                  'Kant',
                                  'Hume',
                                  'Descartes',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «ser es ser percibido» pertenece a:',
                 'alternativas': ['Descartes',
                                  'Platón',
                                  'Kant',
                                  'Berkeley',
                                  'Hume'],
                 'correcta': 'D'},
                {'pregunta': 'El idealismo subjetivo sostiene que la '
                             'realidad depende de:',
                 'alternativas': ['El lenguaje',
                                  'La conciencia del sujeto',
                                  'La sociedad',
                                  'Las leyes físicas',
                                  'La materia'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo objetivo afirma que existe una '
                             'realidad ideal:',
                 'alternativas': ['Independiente del sujeto',
                                  'Puramente material',
                                  'Sensorial',
                                  'Inexistente',
                                  'Creada por el sujeto'],
                 'correcta': 'A'},
                {'pregunta': 'Las Ideas de Platón y el Espíritu de Hegel son '
                             'ejemplos de:',
                 'alternativas': ['Empirismo',
                                  'Idealismo subjetivo',
                                  'Materialismo',
                                  'Escepticismo',
                                  'Idealismo objetivo'],
                 'correcta': 'E'},
                {'pregunta': 'El materialismo sostiene que lo primario es:',
                 'alternativas': ['El espíritu',
                                  'La materia',
                                  'La conciencia',
                                  'La idea',
                                  'El lenguaje'],
                 'correcta': 'B'},
                {'pregunta': 'El fenomenalismo sostiene que solo conocemos:',
                 'alternativas': ['El noúmeno',
                                  'Los fenómenos',
                                  'Las ideas innatas',
                                  'La esencia',
                                  'La cosa en sí'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo que niega toda posibilidad de '
                             'conocer se denomina:',
                 'alternativas': ['Absoluto',
                                  'Moderado',
                                  'Relativo',
                                  'Metódico',
                                  'Parcial'],
                 'correcta': 'A'},
                {'pregunta': 'El problema de la POSIBILIDAD del conocimiento '
                             'se pregunta si:',
                 'alternativas': ['Cuál es la esencia del ser',
                                  'Para qué sirve el saber',
                                  'Si es posible conocer con certeza',
                                  'Qué es la verdad',
                                  'De dónde proviene el conocimiento'],
                 'correcta': 'C'},
                {'pregunta': 'El problema del ORIGEN del conocimiento se '
                             'pregunta:',
                 'alternativas': ['De dónde proviene el conocimiento',
                                  'Qué es lo real',
                                  'Cuál es el fin del hombre',
                                  'Qué es el valor',
                                  'Si es posible conocer'],
                 'correcta': 'A'},
                {'pregunta': 'Descartes es representante del:',
                 'alternativas': ['Escepticismo absoluto',
                                  'Racionalismo',
                                  'Fenomenalismo',
                                  'Empirismo',
                                  'Materialismo'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo kantiano supera la oposición '
                             'entre:',
                 'alternativas': ['Ciencia y religión',
                                  'Ética y lógica',
                                  'Dogmatismo y realismo',
                                  'Racionalismo y empirismo',
                                  'Idealismo y materialismo'],
                 'correcta': 'D'},
                {'pregunta': 'Para el materialismo, la conciencia es:',
                 'alternativas': ['Lo primario',
                                  'Independiente del cerebro',
                                  'Un producto de la materia',
                                  'Una sustancia separada',
                                  'Anterior al mundo'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente que sostiene que la experiencia '
                             'es la única fuente del conocimiento se llama:',
                 'alternativas': ['Dogmatismo',
                                  'Racionalismo',
                                  'Criticismo',
                                  'Idealismo',
                                  'Empirismo'],
                 'correcta': 'E'},
                {'pregunta': 'El método propio del empirismo es:',
                 'alternativas': ['La deducción',
                                  'La intuición exclusiva',
                                  'La dialéctica',
                                  'La analogía',
                                  'La inducción'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los representantes del empirismo figuran '
                             'Locke, Hume, Berkeley y:',
                 'alternativas': ['Descartes',
                                  'Leibniz',
                                  'Malebranche',
                                  'Francisco Bacon',
                                  'Spinoza'],
                 'correcta': 'D'},
                {'pregunta': 'La corriente que sostiene que la razón es la '
                             'única fuente del conocimiento se llama:',
                 'alternativas': ['Empirismo',
                                  'Racionalismo',
                                  'Agnosticismo',
                                  'Escepticismo',
                                  'Fenomenalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El método propio del racionalismo es:',
                 'alternativas': ['El experimento exclusivo',
                                  'La intuición sensible',
                                  'La observación exclusiva',
                                  'La inducción',
                                  'La deducción'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los representantes del racionalismo '
                             'figuran Descartes, Spinoza y:',
                 'alternativas': ['Leibniz',
                                  'Locke',
                                  'Hume',
                                  'Bacon',
                                  'Berkeley'],
                 'correcta': 'A'},
                {'pregunta': 'La corriente que sostiene que el conocimiento '
                             'surge de la unión de experiencia y razón se '
                             'llama:',
                 'alternativas': ['Empirismo',
                                  'Racionalismo puro',
                                  'Escepticismo',
                                  'Dogmatismo',
                                  'Criticismo'],
                 'correcta': 'E'},
                {'pregunta': 'El representante del criticismo, autor de la '
                             'frase «no hay experiencia sin razón ni razón '
                             'sin experiencia», fue:',
                 'alternativas': ['Locke',
                                  'Manuel Kant',
                                  'Hume',
                                  'Hegel',
                                  'Descartes'],
                 'correcta': 'B'},
                {'pregunta': 'La postura que admite que el conocimiento sí '
                             'es posible se llama:',
                 'alternativas': ['Fenomenalismo',
                                  'Dogmatismo',
                                  'Escepticismo',
                                  'Idealismo',
                                  'Agnosticismo'],
                 'correcta': 'B'},
                {'pregunta': 'Los representantes del dogmatismo, según el '
                             'texto, fueron los:',
                 'alternativas': ['Presocráticos',
                                  'Sofistas',
                                  'Positivistas',
                                  'Escolásticos',
                                  'Estoicos'],
                 'correcta': 'A'},
                {'pregunta': 'El fundador del escepticismo, quien afirmaba '
                             'que el conocimiento no es posible, fue:',
                 'alternativas': ['Sócrates',
                                  'Pirrón de Elis',
                                  'Protágoras',
                                  'Gorgias',
                                  'Demócrito'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo radical o absoluto, que afirma '
                             'que el conocimiento es imposible, tiene como '
                             'representante a:',
                 'alternativas': ['Gorgias',
                                  'Protágoras',
                                  'Sócrates',
                                  'Pirrón',
                                  'Platón'],
                 'correcta': 'A'},
                {'pregunta': 'El escepticismo relativo, que afirma que toda '
                             'verdad es relativa, tiene como representante '
                             'a:',
                 'alternativas': ['Heráclito',
                                  'Protágoras',
                                  'Gorgias',
                                  'Pirrón',
                                  'Demócrito'],
                 'correcta': 'B'},
                {'pregunta': 'La postura que admite la imposibilidad de '
                             'conocer la «cosa en sí» se llama:',
                 'alternativas': ['Idealismo objetivo',
                                  'Agnosticismo',
                                  'Materialismo',
                                  'Escepticismo radical',
                                  'Dogmatismo'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del agnosticismo, según el '
                             'texto, fue:',
                 'alternativas': ['Berkeley',
                                  'Protágoras',
                                  'Manuel Kant',
                                  'Pirrón',
                                  'Gorgias'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente que sostiene que el objeto del '
                             'conocimiento no es real sino ideal se llama:',
                 'alternativas': ['Idealismo',
                                  'Fenomenalismo',
                                  'Dogmatismo',
                                  'Materialismo',
                                  'Empirismo'],
                 'correcta': 'A'},
                {'pregunta': 'El idealismo subjetivo, que afirma que toda '
                             'realidad está encerrada en la conciencia, '
                             'tiene como representante a:',
                 'alternativas': ['Hegel',
                                  'Platón',
                                  'Aristóteles',
                                  'Berkeley',
                                  'Kant'],
                 'correcta': 'D'},
                {'pregunta': 'El idealismo objetivo, que sostiene que las '
                             'ideas existen por sí mismas, tiene como '
                             'representantes a Platón y:',
                 'alternativas': ['Hegel',
                                  'Berkeley',
                                  'Locke',
                                  'Descartes',
                                  'Kant'],
                 'correcta': 'A'},
                {'pregunta': 'El materialismo sostiene que el criterio de '
                             'verdad del conocimiento es:',
                 'alternativas': ['La fe',
                                  'La revelación',
                                  'La autoridad',
                                  'La intuición',
                                  'La praxis'],
                 'correcta': 'E'},
                {'pregunta': 'El fenomenalismo sostiene que el sujeto solo '
                             'puede captar el fenómeno, mas no:',
                 'alternativas': ['La esencia o noúmeno',
                                  'La apariencia',
                                  'Los sentidos',
                                  'La experiencia',
                                  'El lenguaje'],
                 'correcta': 'A'},
                {'pregunta': 'El representante del fenomenalismo, según el '
                             'texto, fue:',
                 'alternativas': ['Manuel Kant',
                                  'Platón',
                                  'Locke',
                                  'Berkeley',
                                  'Hegel'],
                 'correcta': 'A'},
                {'pregunta': 'Los representantes del dogmatismo, corriente '
                             'que confía en la posibilidad del conocimiento, '
                             'fueron los:',
                 'alternativas': ['Sofistas',
                                  'Estoicos',
                                  'Positivistas',
                                  'Presocráticos',
                                  'Escépticos'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo radical o absoluto, que niega '
                             'toda posibilidad de conocer, está representado '
                             'por:',
                 'alternativas': ['Platón',
                                  'Pirrón',
                                  'Sócrates',
                                  'Gorgias',
                                  'Protágoras'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo relativo, que sostiene que '
                             'toda verdad es relativa, está representado '
                             'por:',
                 'alternativas': ['Heráclito',
                                  'Protágoras',
                                  'Gorgias',
                                  'Demócrito',
                                  'Pirrón'],
                 'correcta': 'B'},
                {'pregunta': 'Además del criticismo, la imposibilidad de '
                             'conocer la «cosa en sí» también es sostenida, '
                             'bajo el nombre de agnosticismo, por:',
                 'alternativas': ['Locke',
                                  'Hume',
                                  'Descartes',
                                  'Kant',
                                  'Berkeley'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los representantes del racionalismo, '
                             'además de Descartes, figuran Leibniz, Spinoza '
                             'y:',
                 'alternativas': ['Locke',
                                  'Hume',
                                  'Berkeley',
                                  'Malebranche',
                                  'Bacon'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los representantes del empirismo, además '
                             'de Locke y Hume, figuran Bacon y:',
                 'alternativas': ['Descartes',
                                  'Leibniz',
                                  'Malebranche',
                                  'Spinoza',
                                  'Berkeley'],
                 'correcta': 'E'},
                {'pregunta': 'Para el materialismo, el criterio de verdad '
                             'del conocimiento es:',
                 'alternativas': ['La revelación',
                                  'La praxis',
                                  'La intuición',
                                  'La fe',
                                  'La autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'El representante del fenomenalismo, que '
                             'sostiene que solo conocemos los fenómenos, es:',
                 'alternativas': ['Locke',
                                  'Kant',
                                  'Platón',
                                  'Hegel',
                                  'Berkeley'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'POSIBILIDAD DEL CONOCIMIENTO',
                      'items': ['Dogmatismo: sostiene que el conocimiento es '
                                'posible y seguro; representantes: los '
                                'presocráticos.',
                                'Escepticismo: niega la posibilidad de '
                                'alcanzar un conocimiento seguro. Su '
                                'representante clásico es Pirrón de Elis.',
                                'El escepticismo radical o absoluto, '
                                'representado por Gorgias, niega toda '
                                'posibilidad de conocer.',
                                'El escepticismo relativo, representado por '
                                'Protágoras, sostiene que toda verdad es '
                                'relativa.',
                                'El escepticismo absoluto niega toda '
                                'posibilidad de conocer; el relativo solo la '
                                'duda en algunos campos.',
                                'Criticismo: posición intermedia sostenida '
                                'por Kant; el conocimiento es posible pero '
                                'con límites.']},
                     {'titulo': 'ORIGEN DEL CONOCIMIENTO',
                      'items': ['Racionalismo: el origen del conocimiento es '
                                'la razón; su método es la deducción. '
                                'Representantes: Descartes, Leibniz, Spinoza '
                                'y Malebranche.',
                                'Empirismo: el origen es la experiencia; su '
                                'método es la inducción. Representantes: '
                                'Locke, Hume, Bacon y Berkeley.',
                                'Criticismo: razón y experiencia se '
                                'complementan; «los conceptos sin '
                                'intuiciones son vacíos, las intuiciones sin '
                                'conceptos son ciegas».']},
                     {'titulo': 'ESENCIA DEL CONOCIMIENTO',
                      'items': ['Idealismo subjetivo: la realidad depende de '
                                'la conciencia del sujeto. «Ser es ser '
                                'percibido» (Berkeley).',
                                'Idealismo objetivo: existe una realidad '
                                'ideal independiente del sujeto, como las '
                                'Ideas de Platón o el Espíritu de Hegel.',
                                'Materialismo: la materia es lo primario; el '
                                'mundo es cognoscible y la praxis es el '
                                'criterio de verdad.',
                                'Fenomenalismo: solo conocemos los '
                                'fenómenos, no la cosa en sí o noúmeno; '
                                'representante: Kant.']}]},
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
                {'titulo': '8.1.1 CARACTERÍSTICAS DE LA CIENCIA',
                 'items': ['La ciencia es {especializada} porque solo '
                           'investiga una clase determinada de objetos, y '
                           '{metódica} porque su proceder responde a un '
                           'plan.',
                           'Es {sistemática} porque sus conocimientos forman '
                           'un sistema articulado, y {objetiva} porque busca '
                           'reflejar la realidad tal cual es.',
                           'Es {explicativa} porque busca responder al '
                           'porqué de las cosas, y {experimental} porque '
                           'puede probarse y comprobarse.',
                           'Es {universal} porque es válida para todos los '
                           'hombres, y {falible} porque es pasible de error, '
                           'aunque perfectible.',
                           'Es {falsacionista} porque la verdad de una '
                           'hipótesis puede demostrarse también por su '
                           '{falsedad}.',
                           'Es {predictiva} porque prevé situaciones '
                           'futuras, y de {contrastación} porque toda teoría '
                           'está sometida a prueba.']},
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
                           '{sociales} (historia, economía, sociología).']}],
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
                 'alternativas': ['Epistemología',
                                  'Lógica',
                                  'Gnoseología',
                                  'Ontología',
                                  'Axiología'],
                 'correcta': 'A'},
                {'pregunta': 'Etimológicamente, «episteme» significa:',
                 'alternativas': ['Valor',
                                  'Ser',
                                  'Alma',
                                  'Ciencia',
                                  'Palabra'],
                 'correcta': 'D'},
                {'pregunta': 'La diferencia entre gnoseología y '
                             'epistemología es que la primera estudia:',
                 'alternativas': ['Los valores',
                                  'La conducta',
                                  'El lenguaje',
                                  'Solo la ciencia',
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
                 'alternativas': ['La conjetura',
                                  'La hipótesis',
                                  'El postulado',
                                  'La ley científica',
                                  'El axioma'],
                 'correcta': 'D'},
                {'pregunta': 'La suposición provisional que debe ser '
                             'contrastada se denomina:',
                 'alternativas': ['Corolario',
                                  'Ley',
                                  'Teoría',
                                  'Hipótesis',
                                  'Axioma'],
                 'correcta': 'D'},
                {'pregunta': 'La proposición evidente que se acepta sin '
                             'demostración es:',
                 'alternativas': ['El axioma',
                                  'La ley',
                                  'La hipótesis',
                                  'La teoría',
                                  'El teorema'],
                 'correcta': 'A'},
                {'pregunta': 'El método que va de lo particular a lo general '
                             'es:',
                 'alternativas': ['Deductivo',
                                  'Inductivo',
                                  'Analógico',
                                  'Hermenéutico',
                                  'Dialéctico'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo general a lo particular '
                             'es:',
                 'alternativas': ['Analógico',
                                  'Comparativo',
                                  'Estadístico',
                                  'Deductivo',
                                  'Inductivo'],
                 'correcta': 'D'},
                {'pregunta': 'El método general de la ciencia moderna se '
                             'denomina:',
                 'alternativas': ['Fenomenológico',
                                  'Dialéctico',
                                  'Intuitivo',
                                  'Escolástico',
                                  'Hipotético-deductivo'],
                 'correcta': 'E'},
                {'pregunta': 'NO es una función de la ciencia:',
                 'alternativas': ['Dogmatizar',
                                  'Describir',
                                  'Predecir',
                                  'Sistematizar',
                                  'Explicar'],
                 'correcta': 'A'},
                {'pregunta': 'Mario Bunge clasificó las ciencias en formales '
                             'y:',
                 'alternativas': ['Fácticas',
                                  'Humanas',
                                  'Exactas',
                                  'Puras',
                                  'Aplicadas'],
                 'correcta': 'A'},
                {'pregunta': 'Las ciencias formales tienen como objeto de '
                             'estudio entes:',
                 'alternativas': ['Reales',
                                  'Ideales',
                                  'Naturales',
                                  'Materiales',
                                  'Sociales'],
                 'correcta': 'B'},
                {'pregunta': 'Son ciencias formales:',
                 'alternativas': ['Historia y economía',
                                  'Psicología y sociología',
                                  'Física y química',
                                  'Biología y geología',
                                  'Lógica y matemática'],
                 'correcta': 'E'},
                {'pregunta': 'La biología pertenece a las ciencias:',
                 'alternativas': ['Aplicadas exclusivamente',
                                  'Formales',
                                  'Ideales',
                                  'Fácticas sociales',
                                  'Fácticas naturales'],
                 'correcta': 'E'},
                {'pregunta': 'La historia y la economía pertenecen a las '
                             'ciencias:',
                 'alternativas': ['Fácticas sociales',
                                  'Formales',
                                  'Puras',
                                  'Exactas',
                                  'Fácticas naturales'],
                 'correcta': 'A'},
                {'pregunta': 'El primer paso del método científico es:',
                 'alternativas': ['La experimentación',
                                  'La hipótesis',
                                  'La ley',
                                  'La observación',
                                  'La conclusión'],
                 'correcta': 'D'},
                {'pregunta': 'La contrastación de una hipótesis se realiza '
                             'mediante:',
                 'alternativas': ['La experimentación',
                                  'La tradición',
                                  'La intuición',
                                  'La revelación',
                                  'La autoridad'],
                 'correcta': 'A'},
                {'pregunta': 'Que la ciencia pueda anticipar hechos futuros '
                             'corresponde a su función:',
                 'alternativas': ['Predictiva',
                                  'Estética',
                                  'Descriptiva',
                                  'Normativa',
                                  'Explicativa'],
                 'correcta': 'A'},
                {'pregunta': 'Las ciencias fácticas se caracterizan porque '
                             'su objeto es:',
                 'alternativas': ['Abstracto puro',
                                  'Formal',
                                  'Ideal',
                                  'Real',
                                  'Simbólico'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ciencia investigue solo una clase '
                             'determinada de objetos corresponde a la '
                             'característica de ser:',
                 'alternativas': ['Especializada',
                                  'Sistemática',
                                  'Falible',
                                  'Universal',
                                  'Predictiva'],
                 'correcta': 'A'},
                {'pregunta': 'Que el proceder de la ciencia responda a un '
                             'plan organizado corresponde a que es:',
                 'alternativas': ['Falsacionista',
                                  'Objetiva',
                                  'Experimental',
                                  'Explicativa',
                                  'Metódica'],
                 'correcta': 'E'},
                {'pregunta': 'Que los conocimientos científicos formen un '
                             'sistema articulado corresponde a que la '
                             'ciencia es:',
                 'alternativas': ['Contrastable',
                                  'Predictiva',
                                  'Universal',
                                  'Sistemática',
                                  'Especializada'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ciencia busque reflejar la realidad tal '
                             'cual es corresponde a que es:',
                 'alternativas': ['Falible',
                                  'Especializada',
                                  'Sistemática',
                                  'Objetiva',
                                  'Metódica'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ciencia busque responder al porqué de '
                             'las cosas corresponde a que es:',
                 'alternativas': ['Universal',
                                  'Experimental',
                                  'Falible',
                                  'Predictiva',
                                  'Explicativa'],
                 'correcta': 'E'},
                {'pregunta': 'Que la ciencia pueda probarse y comprobarse '
                             'cuantas veces sea necesario corresponde a que '
                             'es:',
                 'alternativas': ['Objetiva',
                                  'Metódica',
                                  'Explicativa',
                                  'Sistemática',
                                  'Experimental'],
                 'correcta': 'E'},
                {'pregunta': 'Que la ciencia sea válida para todos los '
                             'hombres corresponde a que es:',
                 'alternativas': ['Universal',
                                  'Predictiva',
                                  'Contrastable',
                                  'Falible',
                                  'Especializada'],
                 'correcta': 'A'},
                {'pregunta': 'Que la ciencia sea pasible de error, aunque '
                             'perfectible, corresponde a que es:',
                 'alternativas': ['Universal',
                                  'Objetiva',
                                  'Sistemática',
                                  'Falible',
                                  'Metódica'],
                 'correcta': 'D'},
                {'pregunta': 'Que una hipótesis pueda demostrarse verdadera '
                             'también por su falsedad corresponde a que la '
                             'ciencia es:',
                 'alternativas': ['Universal',
                                  'Objetiva',
                                  'Predictiva',
                                  'Falsacionista',
                                  'Explicativa'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ciencia prevea situaciones futuras a '
                             'partir de leyes o teorías corresponde a que '
                             'es:',
                 'alternativas': ['Metódica',
                                  'Experimental',
                                  'Predictiva',
                                  'Falsacionista',
                                  'Sistemática'],
                 'correcta': 'C'},
                {'pregunta': 'Que toda teoría científica esté sometida a '
                             'prueba para confirmarla o debilitarla '
                             'corresponde a que la ciencia tiene:',
                 'alternativas': ['Sistematicidad',
                                  'Objetividad',
                                  'Universalidad',
                                  'Especialización',
                                  'Contrastación o refutabilidad'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Del griego episteme = ciencia y logos = '
                                'estudio. Es la disciplina que estudia el '
                                'conocimiento científico: su estructura, sus '
                                'métodos y su validez.',
                                'Se distingue de la gnoseología porque esta '
                                'estudia el conocimiento en general y la '
                                'epistemología solo el científico.']},
                     {'titulo': 'CARACTERÍSTICAS DE LA CIENCIA',
                      'items': ['La ciencia es especializada porque solo '
                                'investiga una clase determinada de objetos, '
                                'y metódica porque su proceder responde a un '
                                'plan.',
                                'Es sistemática porque sus conocimientos '
                                'forman un sistema articulado, y objetiva '
                                'porque busca reflejar la realidad tal cual '
                                'es.',
                                'Es explicativa porque busca responder al '
                                'porqué de las cosas, y experimental porque '
                                'puede probarse y comprobarse.',
                                'Es universal porque es válida para todos '
                                'los hombres, y falible porque es pasible de '
                                'error, aunque perfectible.',
                                'Es falsacionista porque la verdad de una '
                                'hipótesis puede demostrarse también por su '
                                'falsedad.',
                                'Es predictiva porque prevé situaciones '
                                'futuras, y de contrastación porque toda '
                                'teoría está sometida a prueba.']},
                     {'titulo': 'ESTRUCTURA DE LA CIENCIA',
                      'items': ['Teoría científica: conjunto sistemático de '
                                'leyes e hipótesis que explican un ámbito de '
                                'la realidad.',
                                'Ley científica: enunciado que expresa una '
                                'relación constante y necesaria entre '
                                'fenómenos.',
                                'Hipótesis: suposición o respuesta '
                                'provisional que debe ser contrastada.',
                                'Axioma: proposición evidente que se acepta '
                                'sin demostración.']},
                     {'titulo': 'EL MÉTODO CIENTÍFICO',
                      'items': ['El método hipotético-deductivo comprende: '
                                'observación, formulación del problema, '
                                'planteamiento de la hipótesis, deducción de '
                                'consecuencias, experimentación y '
                                'conclusión.',
                                'El método inductivo va de lo particular a '
                                'lo general; el deductivo, de lo general a '
                                'lo particular.']},
                     {'titulo': 'FUNCIONES Y CLASIFICACIÓN',
                      'items': ['Funciones de la ciencia: describir, '
                                'explicar y predecir.',
                                'Mario Bunge clasificó las ciencias en '
                                'formales (lógica y matemática, de objeto '
                                'ideal) y fácticas (de objeto real).',
                                'Las fácticas se dividen en ciencias '
                                'naturales (física, química, biología) y '
                                'ciencias sociales (historia, economía, '
                                'sociología).']}]},
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
                {'titulo': '9.5 EL PROBLEMA DE LA CONDUCTA MORALMENTE BUENA',
                 'items': ['Cuatro teorías clásicas explican en qué consiste '
                           'actuar moralmente bien: hedonismo, eudemonismo, '
                           'utilitarismo y {formalismo}.',
                           'El {hedonismo} de Epicuro (341-271 a.C.) '
                           'sostiene que el bien y el fin supremo de la vida '
                           'humana es el {placer}.',
                           'A diferencia de Aristipo de Cirene, que solo '
                           'consideraba los placeres {sensibles}, Epicuro '
                           'defendía un cálculo racional y {prudente} de los '
                           'placeres.',
                           'El {eudemonismo} de Aristóteles (384-322 a.C.) '
                           'pregona la {felicidad} como meta suprema de toda '
                           'la actividad moral del hombre.',
                           'Para Aristóteles, la virtud es el equilibrio '
                           'entre dos extremos, la ley del {término medio}: '
                           'entre temeridad y cobardía está la {valentía}.',
                           'San Agustín y, sobre todo, {Santo Tomás de '
                           'Aquino}, situaron la contemplación de {Dios} '
                           'como el bien y felicidad suprema del hombre '
                           'cristiano.',
                           'El {utilitarismo} de Jeremy Bentham y {John '
                           'Stuart Mill} sostiene que una acción es moral si '
                           'es útil, es decir, si produce {felicidad}.',
                           'El utilitarismo defiende la {utilidad pública}: '
                           'la mayor felicidad para el mayor número de '
                           'personas, no el beneficio individual.',
                           'El {formalismo} de Immanuel Kant sostiene que la '
                           'moral no debe dar normas concretas, sino '
                           'establecer la {forma} que toda norma moral debe '
                           'tener.',
                           'Para Kant, la norma moral se expresa mediante '
                           '{imperativos categóricos} (incondicionados), a '
                           'diferencia de los imperativos {hipotéticos}.',
                           'El imperativo categórico kantiano dice: «Obra de '
                           'tal modo que tu acción pueda convertirse en ley '
                           '{universal}».']},
                {'titulo': '9.6 LA PERSONA MORAL Y LA SANCIÓN',
                 'items': ['La {persona} es el sujeto con conciencia de sus '
                           'actos, capaz de crear valores y conducir su '
                           'existencia según principios.',
                           'El {individuo} es cualquier ser sin conciencia '
                           'de sus actos, que gobierna su existencia por '
                           'instintos, como los infantes.',
                           'Las características de la persona moral son: '
                           'conciencia moral, {libertad moral} y '
                           'responsabilidad {moral}.',
                           'La {sanción moral} es el castigo interno, '
                           'subjetivo, que recibe la persona por una acción '
                           'negativa: el {remordimiento}.',
                           'La {sanción jurídica} es la pena impuesta por el '
                           'Estado a quien viola una ley, regulada por los '
                           '{tribunales}.']}],
  'cuadros': [{'titulo': '9.4 CORRIENTES ÉTICAS',
               'encabezados': ['Corriente', 'Representante', 'Fin moral'],
               'filas': [['{Eudemonismo}', '{Aristóteles}', 'La {felicidad}'],
                         ['Ética del {deber}', '{Kant}', 'Obrar por {deber}'],
                         ['{Utilitarismo}',
                          'Stuart {Mill}',
                          'Mayor felicidad del mayor {número}']]}],
  'preguntas': [{'pregunta': 'La disciplina filosófica que estudia los '
                             'valores es la:',
                 'alternativas': ['Gnoseología',
                                  'Ética',
                                  'Ontología',
                                  'Estética',
                                  'Axiología'],
                 'correcta': 'E'},
                {'pregunta': 'Etimológicamente, «axios» significa:',
                 'alternativas': ['Fin', 'Valor', 'Ley', 'Costumbre', 'Bien'],
                 'correcta': 'B'},
                {'pregunta': 'Que todo valor tenga su contravalor '
                             'corresponde a la característica de:',
                 'alternativas': ['Polaridad',
                                  'Materia',
                                  'Jerarquía',
                                  'Historicidad',
                                  'Objetividad'],
                 'correcta': 'A'},
                {'pregunta': 'Que unos valores valgan más que otros '
                             'corresponde a la característica de:',
                 'alternativas': ['Subjetividad',
                                  'Universalidad',
                                  'Jerarquía',
                                  'Relatividad',
                                  'Polaridad'],
                 'correcta': 'C'},
                {'pregunta': 'La jerarquía de valores en sensibles, vitales, '
                             'espirituales y religiosos fue propuesta por:',
                 'alternativas': ['Max Scheler',
                                  'Aristóteles',
                                  'Stuart Mill',
                                  'Kant',
                                  'Nietzsche'],
                 'correcta': 'A'},
                {'pregunta': 'Para el subjetivismo, el valor depende de:',
                 'alternativas': ['La sociedad',
                                  'Dios',
                                  'El sujeto que valora',
                                  'La razón pura',
                                  'El objeto'],
                 'correcta': 'C'},
                {'pregunta': 'Para el objetivismo, los valores:',
                 'alternativas': ['Son ilusiones',
                                  'Varían con la moda',
                                  'Existen independientemente del sujeto',
                                  'Los crea el sujeto',
                                  'No existen'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría según la cual el valor surge de la '
                             'relación entre sujeto y objeto es el:',
                 'alternativas': ['Nihilismo',
                                  'Subjetivismo',
                                  'Formalismo',
                                  'Relacionismo',
                                  'Objetivismo'],
                 'correcta': 'D'},
                {'pregunta': 'El socioculturalismo sostiene que los valores '
                             'son producto de:',
                 'alternativas': ['La revelación',
                                  'La razón individual',
                                  'La sociedad y la cultura',
                                  'El azar',
                                  'La naturaleza biológica'],
                 'correcta': 'C'},
                {'pregunta': 'La disciplina filosófica que reflexiona '
                             'teóricamente sobre la moral es la:',
                 'alternativas': ['Política',
                                  'Ética',
                                  'Moral',
                                  'Estética',
                                  'Axiología'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de normas y costumbres concretas '
                             'de una sociedad constituye la:',
                 'alternativas': ['Moral',
                                  'Ética',
                                  'Estética',
                                  'Ciencia',
                                  'Lógica'],
                 'correcta': 'A'},
                {'pregunta': 'La diferencia entre ética y moral es que la '
                             'ética es:',
                 'alternativas': ['Religiosa',
                                  'Práctica y la moral teórica',
                                  'Estética',
                                  'Teórica y la moral práctica',
                                  'Legal'],
                 'correcta': 'D'},
                {'pregunta': 'El eudemonismo, que sitúa el fin de la vida en '
                             'la felicidad, corresponde a:',
                 'alternativas': ['Aristóteles',
                                  'Nietzsche',
                                  'Stuart Mill',
                                  'Kant',
                                  'Epicuro'],
                 'correcta': 'A'},
                {'pregunta': 'La ética del deber fue formulada por:',
                 'alternativas': ['Aristóteles',
                                  'Mill',
                                  'Scheler',
                                  'Bentham',
                                  'Kant'],
                 'correcta': 'E'},
                {'pregunta': 'El utilitarismo, que busca la mayor felicidad '
                             'para el mayor número, se asocia a:',
                 'alternativas': ['Kant',
                                  'Platón',
                                  'Sócrates',
                                  'Aristóteles',
                                  'Stuart Mill'],
                 'correcta': 'E'},
                {'pregunta': 'NO es un valor ético fundamental:',
                 'alternativas': ['La rentabilidad',
                                  'La solidaridad',
                                  'La justicia',
                                  'La dignidad',
                                  'El bien'],
                 'correcta': 'A'},
                {'pregunta': 'El proceso por el cual el sujeto atribuye un '
                             'valor a algo se denomina:',
                 'alternativas': ['Percepción',
                                  'Inferencia',
                                  'Deducción',
                                  'Juicio lógico',
                                  'Acto valorativo'],
                 'correcta': 'E'},
                {'pregunta': 'En la jerarquía de Scheler, el valor más alto '
                             'corresponde a los valores:',
                 'alternativas': ['Útiles',
                                  'Vitales',
                                  'Sensibles',
                                  'Económicos',
                                  'Religiosos'],
                 'correcta': 'E'},
                {'pregunta': 'Para Kant, una acción es moralmente valiosa '
                             'cuando se realiza:',
                 'alternativas': ['Por miedo',
                                  'Por placer',
                                  'Por costumbre',
                                  'Por deber',
                                  'Por interés'],
                 'correcta': 'D'},
                {'pregunta': 'La afirmación «los valores cambian según la '
                             'época y la cultura» corresponde al:',
                 'alternativas': ['Socioculturalismo',
                                  'Objetivismo',
                                  'Racionalismo',
                                  'Absolutismo moral',
                                  'Formalismo'],
                 'correcta': 'A'},
                {'pregunta': 'El hedonismo de Epicuro sostiene que el bien y '
                             'el fin supremo de la vida humana es:',
                 'alternativas': ['La felicidad social',
                                  'El placer',
                                  'La razón pura',
                                  'El poder',
                                  'El deber'],
                 'correcta': 'B'},
                {'pregunta': 'A diferencia de Epicuro, el filósofo que solo '
                             'consideraba los placeres puramente sensibles '
                             'fue:',
                 'alternativas': ['Kant',
                                  'Platón',
                                  'Aristóteles',
                                  'Sócrates',
                                  'Aristipo de Cirene'],
                 'correcta': 'E'},
                {'pregunta': 'El eudemonismo de Aristóteles pregona como '
                             'meta suprema de la actividad moral:',
                 'alternativas': ['La utilidad',
                                  'El deber',
                                  'La felicidad',
                                  'El placer',
                                  'El poder'],
                 'correcta': 'C'},
                {'pregunta': 'Según Aristóteles, la virtud es el equilibrio '
                             'entre dos extremos, conocido como la ley:',
                 'alternativas': ['De la utilidad',
                                  'Del imperativo',
                                  'Del término medio',
                                  'Del mayor bien',
                                  'Del deber'],
                 'correcta': 'C'},
                {'pregunta': 'Entre la temeridad y la cobardía, la virtud '
                             'según Aristóteles sería:',
                 'alternativas': ['La fortaleza',
                                  'La prudencia',
                                  'La justicia',
                                  'La templanza',
                                  'La valentía'],
                 'correcta': 'E'},
                {'pregunta': 'El pensador cristiano que, junto con San '
                             'Agustín, situó la contemplación de Dios como '
                             'felicidad suprema fue:',
                 'alternativas': ['Santo Tomás de Aquino',
                                  'Kant',
                                  'Aristóteles',
                                  'Bentham',
                                  'Epicuro'],
                 'correcta': 'A'},
                {'pregunta': 'El utilitarismo sostiene que una acción es '
                             'moral si:',
                 'alternativas': ['Obedece a la autoridad',
                                  'Busca el placer individual',
                                  'Sigue la tradición',
                                  'Cumple con el deber',
                                  'Es útil, es decir, produce felicidad'],
                 'correcta': 'E'},
                {'pregunta': 'Los principales representantes del '
                             'utilitarismo son Jeremy Bentham y:',
                 'alternativas': ['John Stuart Mill',
                                  'Aristóteles',
                                  'Immanuel Kant',
                                  'Epicuro',
                                  'San Agustín'],
                 'correcta': 'A'},
                {'pregunta': 'El utilitarismo defiende la utilidad pública, '
                             'es decir, la mayor felicidad para:',
                 'alternativas': ['El individuo exclusivamente',
                                  'El mayor número de personas',
                                  'El gobernante',
                                  'Una sola clase social',
                                  'La clase dominante'],
                 'correcta': 'B'},
                {'pregunta': 'El formalismo ético, representado por Kant, '
                             'sostiene que la moral debe establecer:',
                 'alternativas': ['Normas concretas de conducta',
                                  'La forma que toda norma moral debe tener',
                                  'El placer como fin',
                                  'Solo el bien individual',
                                  'La felicidad social exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Según Kant, la norma moral se expresa '
                             'mediante:',
                 'alternativas': ['Imperativos categóricos',
                                  'Silogismos morales',
                                  'Costumbres sociales',
                                  'Leyes civiles',
                                  'Imperativos hipotéticos'],
                 'correcta': 'A'},
                {'pregunta': 'El imperativo categórico de Kant establece: '
                             'obra de tal modo que tu acción pueda '
                             'convertirse en:',
                 'alternativas': ['Norma jurídica',
                                  'Costumbre social',
                                  'Ley personal',
                                  'Ley universal',
                                  'Placer compartido'],
                 'correcta': 'D'},
                {'pregunta': 'El sujeto con conciencia de sus actos, capaz '
                             'de crear valores y conducir su existencia '
                             'según principios, se llama:',
                 'alternativas': ['Sujeto moral pasivo',
                                  'Ente',
                                  'Persona',
                                  'Individuo',
                                  'Agente neutro'],
                 'correcta': 'C'},
                {'pregunta': 'El ser sin conciencia de sus actos, que '
                             'gobierna su existencia por instintos, se '
                             'llama:',
                 'alternativas': ['Sujeto moral',
                                  'Individuo',
                                  'Agente racional',
                                  'Ciudadano',
                                  'Persona'],
                 'correcta': 'B'},
                {'pregunta': 'El castigo interno, subjetivo, que recibe una '
                             'persona por una acción negativa, expresado '
                             'como remordimiento, se llama:',
                 'alternativas': ['Multa',
                                  'Sanción moral',
                                  'Condena social',
                                  'Pena civil',
                                  'Sanción jurídica'],
                 'correcta': 'B'},
                {'pregunta': 'La pena impuesta por el Estado a quien viola '
                             'una ley, regulada por los tribunales, se '
                             'llama:',
                 'alternativas': ['Culpa subjetiva',
                                  'Sanción jurídica',
                                  'Autocrítica',
                                  'Remordimiento',
                                  'Sanción moral'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'AXIOLOGÍA',
                      'items': ['Del griego axios = valor y logos = estudio. '
                                'Es la disciplina filosófica que estudia los '
                                'valores.',
                                'El acto valorativo es el proceso por el '
                                'cual el sujeto atribuye un valor a un '
                                'objeto o conducta.']},
                     {'titulo': 'CARACTERÍSTICAS Y CLASIFICACIÓN',
                      'items': ['Características de los valores: polaridad '
                                '(todo valor tiene su contravalor: '
                                'bueno-malo), jerarquía (unos valen más que '
                                'otros), materia y objetividad o '
                                'subjetividad según la corriente.',
                                'Max Scheler clasificó los valores en '
                                'jerarquía: sensibles, vitales, espirituales '
                                'y religiosos.',
                                'Valores éticos fundamentales: el bien, la '
                                'justicia, la dignidad y la solidaridad.']},
                     {'titulo': 'TEORÍAS DEL VALOR',
                      'items': ['Subjetivismo: el valor depende del sujeto, '
                                'de su agrado o interés; no existe fuera de '
                                'la valoración.',
                                'Objetivismo: los valores existen '
                                'independientemente del sujeto; se '
                                'descubren, no se crean.',
                                'Relacionismo: el valor surge de la relación '
                                'entre el sujeto y el objeto.']},
                     {'titulo': 'LA ÉTICA Y LA MORAL',
                      'items': ['La ética es la disciplina filosófica que '
                                'reflexiona sobre la moral; es teórica.',
                                'La moral es el conjunto de normas y '
                                'costumbres concretas de una sociedad; es '
                                'práctica.',
                                'Corrientes éticas: el eudemonismo de '
                                'Aristóteles (el fin es la felicidad), la '
                                'ética kantiana del deber, y el utilitarismo '
                                'de Stuart Mill (la mayor felicidad para el '
                                'mayor número).']},
                     {'titulo': 'EL PROBLEMA DE LA CONDUCTA MORALMENTE BUENA',
                      'items': ['Cuatro teorías clásicas explican en qué '
                                'consiste actuar moralmente bien: hedonismo, '
                                'eudemonismo, utilitarismo y formalismo.',
                                'El hedonismo de Epicuro (341-271 a.C.) '
                                'sostiene que el bien y el fin supremo de la '
                                'vida humana es el placer.',
                                'A diferencia de Aristipo de Cirene, que '
                                'solo consideraba los placeres sensibles, '
                                'Epicuro defendía un cálculo racional y '
                                'prudente de los placeres.']},
                     {'titulo': 'LA PERSONA MORAL Y LA SANCIÓN',
                      'items': ['La persona es el sujeto con conciencia de '
                                'sus actos, capaz de crear valores y '
                                'conducir su existencia según principios.',
                                'El individuo es cualquier ser sin '
                                'conciencia de sus actos, que gobierna su '
                                'existencia por instintos, como los '
                                'infantes.',
                                'Las características de la persona moral '
                                'son: conciencia moral, libertad moral y '
                                'responsabilidad moral.']}]},
 {'num': 10,
  'titulo': 'Lógica, lenguaje y pensamiento',
  'secciones': [{'titulo': '10.1 DEFINICIÓN DE LÓGICA',
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
                           '{jurídica}».',
                           '{Protágoras}, el sofista más importante, sostuvo '
                           'que «el hombre es la medida de todas las cosas» '
                           '({homo mensura}).',
                           '{Sócrates} descubrió el concepto de la '
                           '{definición} y de la inducción mediante la '
                           'mayéutica.',
                           '{Platón} es considerado el creador del Principio '
                           'de {no Contradicción}.',
                           '{Boecio}, filósofo ecléctico, tradujo al latín '
                           'obras de Aristóteles y creó el Cuadro '
                           'Tradicional de {Oposición}.',
                           'En la lógica moderna, {Wilhelm Leibniz} intentó '
                           'construir un Lenguaje Universal ({Característica '
                           'Universalis}).',
                           '{George Boole} es considerado el fundador de la '
                           '{lógica simbólica}; publicó en 1854 '
                           '«Investigación sobre las leyes del pensamiento».',
                           '{Łukasiewicz}, filósofo y lógico polaco, propuso '
                           'la lógica {trivalente}, con un tercer valor de '
                           'verdad además de verdadero y falso.']},
                {'titulo': '10.3 RAMAS DE LA LÓGICA',
                 'items': ['La {lógica formal} estudia los actos del pensar '
                           '(concepto, juicio, razonamiento y demostración) '
                           'según su {estructura}, sin importar el '
                           'contenido.',
                           'La {lógica proposicional}, o lógica de '
                           'enunciados, estudia las proposiciones como '
                           '{bloque}, y las relaciones y conectivos entre '
                           'ellas.',
                           'Una {proposición} es una expresión lingüística '
                           'con la propiedad de ser {verdadera} o falsa; '
                           'tiene sujeto, predicado y cópula.',
                           'La {lógica de clases} estudia las relaciones '
                           'formales entre las clases que aparecen en una '
                           'proposición {categórica}.',
                           'Una {clase} es el conjunto de objetos con '
                           'propiedades comunes; por sí sola no es ni '
                           '{verdadera} ni falsa.']},
                {'titulo': '10.4 FUNCIONES BÁSICAS DEL LENGUAJE',
                 'items': ['Función {informativa} o descriptiva: transmite '
                           'información; puede ser {verdadera} o falsa.',
                           'Función {expresiva}: manifiesta {emociones} y '
                           'sentimientos; no es verdadera ni falsa.',
                           'Función {directiva}: busca provocar una '
                           '{conducta}; órdenes, ruegos y pedidos.']},
                {'titulo': '10.5 LENGUAJE NATURAL Y FORMALIZADO',
                 'items': ['El lenguaje {natural} es el de uso cotidiano; es '
                           'rico pero {ambiguo} y vago.',
                           'El lenguaje {formalizado} usa símbolos, es '
                           '{preciso}, unívoco y sin ambigüedad.',
                           'La {argumentación} es el conjunto de razones '
                           '(premisas) que sustentan una {conclusión}.']}],
  'cuadros': [{'titulo': '10.3 FUNCIONES DEL LENGUAJE',
               'encabezados': ['Función', 'Finalidad', '¿Verdadera o falsa?'],
               'filas': [['{Informativa}',
                          'Transmitir {información}',
                          '{Sí}'],
                         ['{Expresiva}', 'Manifestar {emociones}', '{No}'],
                         ['{Directiva}', 'Provocar una {conducta}', 'No']]}],
  'preguntas': [{'pregunta': 'La lógica es la ciencia formal que estudia:',
                 'alternativas': ['La validez o corrección de los '
                                  'razonamientos',
                                  'El origen del conocimiento',
                                  'La verdad de los hechos',
                                  'Los valores morales',
                                  'El lenguaje literario'],
                 'correcta': 'A'},
                {'pregunta': 'La lógica estudia de los razonamientos su:',
                 'alternativas': ['Forma',
                                  'Utilidad',
                                  'Contenido',
                                  'Belleza',
                                  'Origen histórico'],
                 'correcta': 'A'},
                {'pregunta': 'El fundador de la lógica es:',
                 'alternativas': ['Platón',
                                  'Aristóteles',
                                  'Boole',
                                  'Porfirio',
                                  'Frege'],
                 'correcta': 'B'},
                {'pregunta': 'La obra lógica de Aristóteles se reunió bajo '
                             'el nombre de:',
                 'alternativas': ['República',
                                  'Órganon',
                                  'Metafísica',
                                  'Isagoge',
                                  'Principia'],
                 'correcta': 'B'},
                {'pregunta': 'El «árbol» que ordena géneros y especies fue '
                             'elaborado por:',
                 'alternativas': ['Russell',
                                  'Porfirio de Tiro',
                                  'Aristóteles',
                                  'Frege',
                                  'Boole'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica moderna o simbólica se caracteriza '
                             'por emplear:',
                 'alternativas': ['Lenguaje natural',
                                  'Silogismos únicamente',
                                  'Ejemplos históricos',
                                  'Metáforas',
                                  'Símbolos matemáticos'],
                 'correcta': 'E'},
                {'pregunta': 'El filósofo peruano destacado en lógica '
                             'jurídica es:',
                 'alternativas': ['Antenor Orrego',
                                  'Deustua',
                                  'Mariátegui',
                                  'Francisco Miró Quesada Cantuarias',
                                  'Salazar Bondy'],
                 'correcta': 'D'},
                {'pregunta': 'La función del lenguaje que transmite '
                             'información y puede ser verdadera o falsa es '
                             'la:',
                 'alternativas': ['Poética',
                                  'Directiva',
                                  'Informativa',
                                  'Expresiva',
                                  'Fática'],
                 'correcta': 'C'},
                {'pregunta': 'La función del lenguaje que manifiesta '
                             'emociones es la:',
                 'alternativas': ['Directiva',
                                  'Metalingüística',
                                  'Descriptiva',
                                  'Informativa',
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
                 'alternativas': ['Informativa',
                                  'Expresiva',
                                  'Directiva',
                                  'Apelativa',
                                  'Referencial'],
                 'correcta': 'B'},
                {'pregunta': '«El Cusco está en el Perú» corresponde a la '
                             'función:',
                 'alternativas': ['Expresiva',
                                  'Informativa',
                                  'Poética',
                                  'Emotiva',
                                  'Directiva'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje natural se caracteriza por ser:',
                 'alternativas': ['Unívoco',
                                  'Simbólico',
                                  'Preciso',
                                  'Artificial',
                                  'Ambiguo y vago'],
                 'correcta': 'E'},
                {'pregunta': 'El lenguaje formalizado se caracteriza por '
                             'ser:',
                 'alternativas': ['Literario',
                                  'Preciso y unívoco',
                                  'Emotivo',
                                  'Coloquial',
                                  'Ambiguo'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de razones que sustentan una '
                             'conclusión constituye:',
                 'alternativas': ['Una descripción',
                                  'Una exclamación',
                                  'Una argumentación',
                                  'Una narración',
                                  'Una orden'],
                 'correcta': 'C'},
                {'pregunta': 'Las ramas principales de la lógica son la '
                             'formal clásica, la proposicional y la de:',
                 'alternativas': ['Clases',
                                  'Conjuntos',
                                  'Números',
                                  'Relaciones',
                                  'Predicados exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Las expresiones directivas NO pueden ser '
                             'calificadas como:',
                 'alternativas': ['Verdaderas o falsas',
                                  'Correctas o incorrectas',
                                  'Corteses o descorteses',
                                  'Claras u oscuras',
                                  'Útiles o inútiles'],
                 'correcta': 'A'},
                {'pregunta': 'En una argumentación, las razones que '
                             'sustentan se denominan:',
                 'alternativas': ['Falacias',
                                  'Conclusiones',
                                  'Axiomas',
                                  'Corolarios',
                                  'Premisas'],
                 'correcta': 'E'},
                {'pregunta': 'La lógica se clasifica como una ciencia:',
                 'alternativas': ['Experimental',
                                  'Aplicada',
                                  'Fáctica natural',
                                  'Formal',
                                  'Fáctica social'],
                 'correcta': 'D'},
                {'pregunta': 'La «Isagoge» fue escrita por:',
                 'alternativas': ['Aristóteles',
                                  'Frege',
                                  'Boecio',
                                  'Porfirio de Tiro',
                                  'Boole'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la lógica que estudia los actos del '
                             'pensar según su estructura, sin importar el '
                             'contenido, se llama lógica:',
                 'alternativas': ['Proposicional',
                                  'Material',
                                  'Simbólica exclusiva',
                                  'De clases',
                                  'Formal'],
                 'correcta': 'E'},
                {'pregunta': 'La lógica que estudia las proposiciones en '
                             'bloque y sus conectivos se llama lógica:',
                 'alternativas': ['De clases',
                                  'Proposicional o de enunciados',
                                  'Formal',
                                  'Deductiva exclusiva',
                                  'Modal'],
                 'correcta': 'B'},
                {'pregunta': 'Una proposición es una expresión lingüística '
                             'que tiene la propiedad de ser:',
                 'alternativas': ['Ambigua siempre',
                                  'Solo falsa',
                                  'Solo verdadera',
                                  'Verdadera o falsa',
                                  'Ni verdadera ni falsa'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la lógica que estudia las '
                             'relaciones formales entre clases se llama '
                             'lógica:',
                 'alternativas': ['Modal',
                                  'Simbólica',
                                  'Proposicional',
                                  'De clases',
                                  'Formal'],
                 'correcta': 'D'},
                {'pregunta': 'Una clase, por sí sola, sin establecer '
                             'relaciones de pertenencia, no es ni verdadera '
                             'ni:',
                 'alternativas': ['Universal',
                                  'Particular',
                                  'Real',
                                  'Falsa',
                                  'Categórica'],
                 'correcta': 'D'},
                {'pregunta': 'El sofista considerado el más importante, '
                             'autor de la frase «el hombre es la medida de '
                             'todas las cosas», fue:',
                 'alternativas': ['Gorgias',
                                  'Protágoras',
                                  'Sócrates',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'En el campo de la lógica, Sócrates es '
                             'reconocido por descubrir el concepto de la '
                             'definición y de:',
                 'alternativas': ['La tautología',
                                  'La deducción',
                                  'El silogismo',
                                  'La analogía',
                                  'La inducción'],
                 'correcta': 'E'},
                {'pregunta': 'Platón es considerado el creador de qué '
                             'principio lógico:',
                 'alternativas': ['De Razón Suficiente',
                                  'De Identidad',
                                  'Del Tercio Excluido',
                                  'De no Contradicción',
                                  'De Causalidad'],
                 'correcta': 'D'},
                {'pregunta': 'El filósofo medieval que tradujo al latín '
                             'obras de Aristóteles y creó el Cuadro '
                             'Tradicional de Oposición fue:',
                 'alternativas': ['Porfirio de Tiro',
                                  'San Agustín',
                                  'Duns Escoto',
                                  'Santo Tomás de Aquino',
                                  'Boecio'],
                 'correcta': 'E'},
                {'pregunta': 'En la lógica moderna, el filósofo que intentó '
                             'construir un Lenguaje Universal fue:',
                 'alternativas': ['Wilhelm Leibniz',
                                  'Kant',
                                  'George Boole',
                                  'Aristóteles',
                                  'Descartes'],
                 'correcta': 'A'},
                {'pregunta': 'El fundador de la lógica simbólica, autor de '
                             '«Investigación sobre las leyes del '
                             'pensamiento» (1854), fue:',
                 'alternativas': ['Gottlob Frege',
                                  'Wilhelm Leibniz',
                                  'George Boole',
                                  'Bertrand Russell',
                                  'Aristóteles'],
                 'correcta': 'C'},
                {'pregunta': 'El pensador que propuso la lógica trivalente '
                             'fue:',
                 'alternativas': ['Aristóteles',
                                  'Łukasiewicz',
                                  'Wittgenstein',
                                  'Leibniz',
                                  'Frege'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'DEFINICIÓN DE LÓGICA',
                      'items': ['La lógica es la ciencia formal que estudia '
                                'la validez o corrección de los '
                                'razonamientos.',
                                'Estudia la forma del razonamiento, no su '
                                'contenido ni su verdad material.',
                                'Ramas: la lógica formal clásica '
                                '(aristotélica), la lógica proposicional y '
                                'la lógica de clases.']},
                     {'titulo': 'HISTORIA DE LA LÓGICA',
                      'items': ['Aristóteles es el fundador de la lógica; su '
                                'obra se reunió bajo el nombre de «Órganon».',
                                'En la lógica medieval destaca Porfirio de '
                                'Tiro con su «Isagoge» y el árbol de '
                                'Porfirio.',
                                'La lógica moderna o simbólica emplea '
                                'símbolos matemáticos; destacan Boole, Frege '
                                'y Russell.',
                                'En el Perú destaca Francisco Miró Quesada '
                                'Cantuarias, quien acuñó el término «lógica '
                                'jurídica».',
                                'Protágoras, el sofista más importante, '
                                'sostuvo que «el hombre es la medida de '
                                'todas las cosas» (homo mensura).',
                                'Sócrates descubrió el concepto de la '
                                'definición y de la inducción mediante la '
                                'mayéutica.']},
                     {'titulo': 'RAMAS DE LA LÓGICA',
                      'items': ['La lógica formal estudia los actos del '
                                'pensar (concepto, juicio, razonamiento y '
                                'demostración) según su estructura, sin '
                                'importar el contenido.',
                                'La lógica proposicional, o lógica de '
                                'enunciados, estudia las proposiciones como '
                                'bloque, y las relaciones y conectivos entre '
                                'ellas.',
                                'Una proposición es una expresión '
                                'lingüística con la propiedad de ser '
                                'verdadera o falsa; tiene sujeto, predicado '
                                'y cópula.',
                                'La lógica de clases estudia las relaciones '
                                'formales entre las clases que aparecen en '
                                'una proposición categórica.',
                                'Una clase es el conjunto de objetos con '
                                'propiedades comunes; por sí sola no es ni '
                                'verdadera ni falsa.']},
                     {'titulo': 'FUNCIONES BÁSICAS DEL LENGUAJE',
                      'items': ['Función informativa o descriptiva: '
                                'transmite información; puede ser verdadera '
                                'o falsa.',
                                'Función expresiva: manifiesta emociones y '
                                'sentimientos; no es verdadera ni falsa.',
                                'Función directiva: busca provocar una '
                                'conducta; órdenes, ruegos y pedidos.']},
                     {'titulo': 'LENGUAJE NATURAL Y FORMALIZADO',
                      'items': ['El lenguaje natural es el de uso cotidiano; '
                                'es rico pero ambiguo y vago.',
                                'El lenguaje formalizado usa símbolos, es '
                                'preciso, unívoco y sin ambigüedad.',
                                'La argumentación es el conjunto de razones '
                                '(premisas) que sustentan una '
                                'conclusión.']}]},
 {'num': 11,
  'titulo': 'Falacias',
  'secciones': [{'titulo': '11.1 FALACIAS FORMALES',
                 'items': ['Una {falacia} es un razonamiento que parece '
                           'válido pero no lo es.',
                           'Las falacias {formales} tienen un error en la '
                           '{estructura} o forma del razonamiento.',
                           'La falacia de {afirmación del consecuente} se '
                           'comete al invertir la ley del {Modus Ponens}: de '
                           '(p→q) y q, se concluye erróneamente p. Ejemplo: '
                           '«si la población aumenta, escasean las '
                           'subsistencias; escasean las subsistencias; por '
                           'lo tanto, {aumentó} la población».']},
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
                           'palabra que se {acentúa} o destaca.']}],
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
                                  'Carece de premisas',
                                  'Siempre es verdadero',
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
                 'alternativas': ['Están bien formuladas',
                                  'Son verdaderas',
                                  'No son pertinentes para la conclusión',
                                  'Son evidentes',
                                  'Son numerosas'],
                 'correcta': 'C'},
                {'pregunta': '«No debemos creer en las teorías de Marx, '
                             'recuerda que fue comunista» es una falacia:',
                 'alternativas': ['De equívoco',
                                  'Ad hominem',
                                  'Ad báculum',
                                  'Ad ignorantiam',
                                  'Ad populum'],
                 'correcta': 'B'},
                {'pregunta': '«Dios existe, porque nadie ha demostrado su '
                             'inexistencia» es una falacia:',
                 'alternativas': ['Ad hominem',
                                  'Ad ignorantiam',
                                  'Ad verecundiam',
                                  'Ad populum',
                                  'Causa falsa'],
                 'correcta': 'B'},
                {'pregunta': '«Si presenta un reclamo, su permanencia en la '
                             'empresa puede acortarse» es una falacia:',
                 'alternativas': ['De énfasis',
                                  'Ad hominem',
                                  'Ad populum',
                                  'Ad báculum',
                                  'Ignoratio elenchi'],
                 'correcta': 'D'},
                {'pregunta': '«Este jabón es bueno, lo usa un cantante '
                             'famoso» es una falacia:',
                 'alternativas': ['Ad verecundiam',
                                  'Causa falsa',
                                  'Anfibología',
                                  'Ad populum',
                                  'Ad báculum'],
                 'correcta': 'A'},
                {'pregunta': '«Tome esta bebida, lo nuestro está primero» es '
                             'una falacia:',
                 'alternativas': ['De equívoco',
                                  'Ad hominem',
                                  'Ad populum',
                                  'Ad báculum',
                                  'Ad ignorantiam'],
                 'correcta': 'C'},
                {'pregunta': '«Me levanté con el pie izquierdo, hoy será un '
                             'mal día» es una falacia de:',
                 'alternativas': ['Ambigüedad',
                                  'Autoridad',
                                  'Fuerza',
                                  'Causa falsa',
                                  'Ignorancia'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando un razonamiento prueba una conclusión '
                             'distinta de la que pretendía, se comete:',
                 'alternativas': ['Ad hominem',
                                  'Ad báculum',
                                  'Equívoco',
                                  'Ignoratio elenchi',
                                  'Énfasis'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia ad hominem del tipo ofensivo '
                             'consiste en:',
                 'alternativas': ['Usar palabras ambiguas',
                                  'Atacar a quien hace la afirmación',
                                  'Citar una autoridad',
                                  'Apelar a la fuerza',
                                  'Apelar al pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'La falacia que aprovecha las circunstancias '
                             'personales del adversario es la ad hominem:',
                 'alternativas': ['Emotiva',
                                  'Ofensiva',
                                  'Formal',
                                  'Directa',
                                  'Circunstancial'],
                 'correcta': 'E'},
                {'pregunta': 'Las falacias de ambigüedad se producen cuando '
                             'el razonamiento contiene:',
                 'alternativas': ['Muchas premisas',
                                  'Datos numéricos',
                                  'Citas de autoridad',
                                  'Palabras o frases ambiguas',
                                  'Conclusiones falsas'],
                 'correcta': 'D'},
                {'pregunta': 'Usar la palabra «banco» con dos significados '
                             'distintos en un mismo razonamiento es una '
                             'falacia de:',
                 'alternativas': ['Causa falsa',
                                  'Énfasis',
                                  'Anfibología',
                                  'Equívoco',
                                  'Autoridad'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando la ambigüedad proviene de la '
                             'construcción gramatical se comete:',
                 'alternativas': ['Equívoco',
                                  'Énfasis',
                                  'Ad populum',
                                  'Ad báculum',
                                  'Anfibología'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando el significado cambia según la palabra '
                             'acentuada se comete la falacia de:',
                 'alternativas': ['Causa falsa',
                                  'Equívoco',
                                  'Ignoratio elenchi',
                                  'Énfasis',
                                  'Anfibología'],
                 'correcta': 'D'},
                {'pregunta': 'El recurso favorito de propagandistas y '
                             'demagogos es la falacia:',
                 'alternativas': ['Ad verecundiam',
                                  'Ad populum',
                                  'Ad báculum',
                                  'De equívoco',
                                  'Formal'],
                 'correcta': 'B'},
                {'pregunta': '«La fuerza hace el derecho» resume la falacia:',
                 'alternativas': ['Ad populum',
                                  'Ad hominem',
                                  'Ad ignorantiam',
                                  'De énfasis',
                                  'Ad báculum'],
                 'correcta': 'E'},
                {'pregunta': 'La falacia ad verecundiam se comete al apelar '
                             'a una autoridad:',
                 'alternativas': ['Fuera de su ámbito de especialidad',
                                  'Científica',
                                  'Legítima',
                                  'Académica',
                                  'Reconocida en su campo'],
                 'correcta': 'A'},
                {'pregunta': 'Confundir la simple sucesión temporal con una '
                             'relación causal corresponde a la falacia de:',
                 'alternativas': ['Ad báculum',
                                  'Ad populum',
                                  'Anfibología',
                                  'Causa falsa',
                                  'Equívoco'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia formal que se comete al invertir la '
                             'ley del Modus Ponens se llama:',
                 'alternativas': ['Negación del antecedente',
                                  'Ignoratio elenchi',
                                  'Petición de principio',
                                  'Afirmación del consecuente',
                                  'Ad hominem'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'FALACIAS FORMALES',
                      'items': ['Una falacia es un razonamiento que parece '
                                'válido pero no lo es.',
                                'Las falacias formales tienen un error en la '
                                'estructura o forma del razonamiento.',
                                'La falacia de afirmación del consecuente se '
                                'comete al invertir la ley del Modus Ponens: '
                                'de (p→q) y q, se concluye erróneamente p. '
                                'Ejemplo: «si la población aumenta, escasean '
                                'las subsistencias; escasean las '
                                'subsistencias; por lo tanto, aumentó la '
                                'población».']},
                     {'titulo': 'FALACIAS DE ATINENCIA',
                      'items': ['Se cometen cuando las premisas no son '
                                'pertinentes para la conclusión.',
                                'Ignoratio elenchi o conclusión inatinente: '
                                'se prueba una conclusión diferente de la '
                                'que se pretendía.',
                                'Causa falsa: concluir que un hecho causa '
                                'otro solo porque lo precede. Ejemplo: «me '
                                'levanté con el pie izquierdo, hoy será un '
                                'mal día».',
                                'Ad populum: apelación emocional al pueblo o '
                                'a la galería. Recurso favorito de '
                                'propagandistas y demagogos.',
                                'Ad hominem: se ataca a la persona en vez de '
                                'refutar su argumento. Puede ser ofensivo o '
                                'circunstancial.',
                                'Ad ignorantiam: afirmar que algo es '
                                'verdadero porque no se ha demostrado su '
                                'falsedad.']},
                     {'titulo': 'FALACIAS DE AMBIGÜEDAD',
                      'items': ['Aparecen cuando el razonamiento contiene '
                                'palabras o frases ambiguas.',
                                'Equívoco: se usa una palabra con dos o más '
                                'significados distintos en el mismo '
                                'razonamiento.',
                                'Anfibología: la ambigüedad proviene de la '
                                'construcción gramatical de la frase.',
                                'Énfasis: el significado cambia según la '
                                'palabra que se acentúa o destaca.']}]},
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
                {'titulo': '12.4 RAZONAMIENTOS VÁLIDOS: REGLAS DE INFERENCIA',
                 'items': ['El {Modus Ponendo Ponens} (MPP): de una premisa '
                           'condicional, si se afirma el {antecedente}, se '
                           'concluye la afirmación del {consecuente}.',
                           'Ejemplo de MPP: «Si Luis es ingeniero, es '
                           'profesional. Luis es ingeniero. Por lo tanto, '
                           'Luis es {profesional}».',
                           'El {Modus Tollendo Tollens} (MTT): de una '
                           'premisa condicional, si se {niega} el '
                           'consecuente, se concluye la negación del '
                           '{antecedente}.',
                           'El {Silogismo Disyuntivo} (SD): de una '
                           'proposición disyuntiva, si se niega uno de los '
                           'extremos, se concluye la afirmación del {otro} '
                           'extremo.',
                           'El {Silogismo Hipotético Puro} (SHP): con dos '
                           'premisas condicionales donde el consecuente de '
                           'la primera es el antecedente de la segunda, se '
                           'concluye antecedente de la primera con '
                           '{consecuente} de la segunda.',
                           'Ejemplo de SHP: «Si es viernes, nos vamos de '
                           'paseo. Si nos vamos de paseo, estamos felices. '
                           'Por lo tanto, si es viernes, estamos {felices}».',
                           'La {Transitividad Simétrica} (TS) es la '
                           'transitividad de {bicondicionales}, con la misma '
                           'estructura que el SHP pero con premisas '
                           'bicondicionales.']}],
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
                 'alternativas': ['Claro u oscuro',
                                  'Justo o injusto',
                                  'Verdadero o falso',
                                  'Bello o feo',
                                  'Útil o inútil'],
                 'correcta': 'C'},
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
                                  'Compuesta',
                                  'Condicional',
                                  'Molecular',
                                  'Bicondicional'],
                 'correcta': 'A'},
                {'pregunta': 'La proposición que contiene uno o más '
                             'operadores se denomina:',
                 'alternativas': ['Atómica',
                                  'Simple',
                                  'Variable',
                                  'Compuesta o molecular',
                                  'Constante'],
                 'correcta': 'D'},
                {'pregunta': 'Las variables proposicionales se representan '
                             'con:',
                 'alternativas': ['Números',
                                  'Letras griegas',
                                  'Símbolos matemáticos',
                                  'Letras minúsculas p, q, r, s',
                                  'Palabras'],
                 'correcta': 'D'},
                {'pregunta': 'El único conector monádico de la lógica '
                             'proposicional es:',
                 'alternativas': ['La disyunción',
                                  'La negación',
                                  'La condicional',
                                  'La bicondicional',
                                  'La conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∧ corresponde a la:',
                 'alternativas': ['Bicondicional',
                                  'Condicional',
                                  'Negación',
                                  'Disyunción',
                                  'Conjunción'],
                 'correcta': 'E'},
                {'pregunta': 'El símbolo → corresponde a la:',
                 'alternativas': ['Condicional',
                                  'Negación',
                                  'Disyunción fuerte',
                                  'Conjunción',
                                  'Bicondicional'],
                 'correcta': 'A'},
                {'pregunta': 'El símbolo ↔ se lee:',
                 'alternativas': ['Y',
                                  'No',
                                  'Si... entonces',
                                  'Si y solo si',
                                  'O'],
                 'correcta': 'D'},
                {'pregunta': 'La disyunción débil se lee como:',
                 'alternativas': ['No',
                                  'Si... entonces',
                                  'O (inclusivo)',
                                  'Si y solo si',
                                  'Y'],
                 'correcta': 'C'},
                {'pregunta': 'Los paréntesis, corchetes y llaves son '
                             'símbolos:',
                 'alternativas': ['Variables',
                                  'Monádicos',
                                  'Diádicos',
                                  'Constantes',
                                  'Auxiliares'],
                 'correcta': 'E'},
                {'pregunta': '«El zorrino no es mamífero» se formaliza como:',
                 'alternativas': ['p', '~p', 'p → q', 'p ∧ q', 'p ∨ q'],
                 'correcta': 'B'},
                {'pregunta': '«La vaca es mamífero y el caballo también» se '
                             'formaliza como:',
                 'alternativas': ['p → q', '~p', 'p ↔ q', 'p ∨ q', 'p ∧ q'],
                 'correcta': 'E'},
                {'pregunta': '«El asno es mamífero pero el loro no» se '
                             'formaliza como:',
                 'alternativas': ['p → ~q',
                                  'p ∨ q',
                                  'p ∧ ~q',
                                  'p ∧ q',
                                  '~p ∧ q'],
                 'correcta': 'C'},
                {'pregunta': 'Una fórmula atómica se representa con:',
                 'alternativas': ['Una sola variable',
                                  'Un conector',
                                  'Dos variables',
                                  'Tres operadores',
                                  'Paréntesis'],
                 'correcta': 'A'},
                {'pregunta': '«Si llueve entonces me quedo» se formaliza '
                             'como:',
                 'alternativas': ['p ↔ q', 'p ∨ q', '~p', 'p → q', 'p ∧ q'],
                 'correcta': 'D'},
                {'pregunta': 'Los conectores que unen dos variables se '
                             'denominan:',
                 'alternativas': ['Monádicos',
                                  'Variables',
                                  'Auxiliares',
                                  'Diádicos o binarios',
                                  'Atómicos'],
                 'correcta': 'D'},
                {'pregunta': '«Estudio si y solo si tengo tiempo» se '
                             'formaliza como:',
                 'alternativas': ['p ∧ q', 'p ∨ q', 'p ↔ q', '~p', 'p → q'],
                 'correcta': 'C'},
                {'pregunta': 'Las órdenes y las exclamaciones NO son '
                             'proposiciones porque:',
                 'alternativas': ['Carecen de sujeto',
                                  'Son muy breves',
                                  'No pueden ser verdaderas ni falsas',
                                  'Son emotivas siempre',
                                  'No usan verbos'],
                 'correcta': 'C'},
                {'pregunta': 'El símbolo ~ representa la:',
                 'alternativas': ['Negación',
                                  'Conjunción',
                                  'Disyunción',
                                  'Implicación',
                                  'Equivalencia'],
                 'correcta': 'A'},
                {'pregunta': 'La regla que dice que de una premisa '
                             'condicional, si se afirma el antecedente, se '
                             'concluye el consecuente, se llama:',
                 'alternativas': ['Transitividad Simétrica',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Disyuntivo',
                                  'Modus Tollendo Tollens',
                                  'Silogismo Hipotético Puro'],
                 'correcta': 'B'},
                {'pregunta': 'En el argumento «Si Luis es ingeniero, es '
                             'profesional. Luis es ingeniero. Por lo tanto, '
                             'es profesional», se aplica:',
                 'alternativas': ['Silogismo Disyuntivo',
                                  'Modus Ponendo Ponens',
                                  'Ninguna regla válida',
                                  'Modus Tollendo Tollens',
                                  'Transitividad Simétrica'],
                 'correcta': 'B'},
                {'pregunta': 'La regla que, de una premisa condicional, '
                             'niega el consecuente para concluir la negación '
                             'del antecedente, se llama:',
                 'alternativas': ['Silogismo Disyuntivo',
                                  'Transitividad Simétrica',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Hipotético Puro',
                                  'Modus Tollendo Tollens'],
                 'correcta': 'E'},
                {'pregunta': 'La regla que, de una proposición disyuntiva, '
                             'niega un extremo para concluir la afirmación '
                             'del otro, se llama:',
                 'alternativas': ['Silogismo Hipotético Puro',
                                  'Silogismo Disyuntivo',
                                  'Transitividad Simétrica',
                                  'Modus Tollendo Tollens',
                                  'Modus Ponendo Ponens'],
                 'correcta': 'B'},
                {'pregunta': 'La regla que combina dos premisas '
                             'condicionales, donde el consecuente de la '
                             'primera es el antecedente de la segunda, se '
                             'llama:',
                 'alternativas': ['Transitividad Simétrica',
                                  'Modus Tollendo Tollens',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Disyuntivo',
                                  'Silogismo Hipotético Puro'],
                 'correcta': 'E'},
                {'pregunta': 'En el argumento «Si es viernes, nos vamos de '
                             'paseo. Si nos vamos de paseo, estamos felices. '
                             'Por lo tanto, si es viernes, estamos felices», '
                             'se aplica:',
                 'alternativas': ['Modus Tollendo Tollens',
                                  'Silogismo Hipotético Puro',
                                  'Silogismo Disyuntivo',
                                  'Ninguna regla válida',
                                  'Modus Ponendo Ponens'],
                 'correcta': 'B'},
                {'pregunta': 'La transitividad de bicondicionales, con '
                             'estructura similar al Silogismo Hipotético '
                             'Puro pero con premisas bicondicionales, se '
                             'llama:',
                 'alternativas': ['Silogismo Disyuntivo',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Categórico',
                                  'Transitividad Simétrica',
                                  'Modus Tollendo Tollens'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'LA PROPOSICIÓN',
                      'items': ['Es todo enunciado del que se puede afirmar '
                                'que es verdadero o falso.',
                                'No son proposiciones las preguntas, las '
                                'órdenes, los deseos ni las exclamaciones.',
                                'Proposición simple o atómica: no contiene '
                                'ningún operador lógico. Se representa con '
                                'una sola variable.',
                                'Proposición compuesta o molecular: contiene '
                                'uno o más operadores.']},
                     {'titulo': 'SIGNOS LÓGICOS',
                      'items': ['Variables: representan proposiciones '
                                'simples; se usan las letras minúsculas p, '
                                'q, r, s.',
                                'Conectores monádicos: afectan a una sola '
                                'variable. El único es la negación (~).',
                                'Conectores diádicos o binarios: unen dos '
                                'variables. Son la conjunción, la disyunción '
                                'débil, la disyunción fuerte, la condicional '
                                'y la bicondicional.',
                                'Símbolos auxiliares: paréntesis, corchetes '
                                'y llaves, que sirven para agrupar.']},
                     {'titulo': 'FORMALIZACIÓN',
                      'items': ['Fórmula atómica: se representa con una sola '
                                'variable. Ejemplo: «El asno es vertebrado» '
                                '= p.',
                                'Fórmula molecular: contiene uno o más '
                                'operadores. Ejemplo: «El zorrino no es '
                                'mamífero» = ~p.',
                                '«La vaca es mamífero y el caballo también» '
                                'se formaliza como p ∧ q.',
                                '«El asno es mamífero pero el loro no» se '
                                'formaliza como p ∧ ~q.']},
                     {'titulo': 'RAZONAMIENTOS VÁLIDOS: REGLAS DE INFERENCIA',
                      'items': ['El Modus Ponendo Ponens (MPP): de una '
                                'premisa condicional, si se afirma el '
                                'antecedente, se concluye la afirmación del '
                                'consecuente.',
                                'Ejemplo de MPP: «Si Luis es ingeniero, es '
                                'profesional. Luis es ingeniero. Por lo '
                                'tanto, Luis es profesional».',
                                'El Modus Tollendo Tollens (MTT): de una '
                                'premisa condicional, si se niega el '
                                'consecuente, se concluye la negación del '
                                'antecedente.',
                                'El Silogismo Disyuntivo (SD): de una '
                                'proposición disyuntiva, si se niega uno de '
                                'los extremos, se concluye la afirmación del '
                                'otro extremo.',
                                'El Silogismo Hipotético Puro (SHP): con dos '
                                'premisas condicionales donde el consecuente '
                                'de la primera es el antecedente de la '
                                'segunda, se concluye antecedente de la '
                                'primera con consecuente de la segunda.',
                                'Ejemplo de SHP: «Si es viernes, nos vamos '
                                'de paseo. Si nos vamos de paseo, estamos '
                                'felices. Por lo tanto, si es viernes, '
                                'estamos felices».']}]},
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
                {'titulo': '13.3 VALIDEZ MEDIANTE TABLAS DE VERDAD',
                 'items': ['Un razonamiento es {válido} cuando es imposible '
                           'que las premisas sean verdaderas y la conclusión '
                           '{falsa} a la vez.',
                           'Para comprobar la validez con tablas de verdad, '
                           'se construye la fórmula «({premisas}) → '
                           'conclusión»; si resulta {tautológica}, el '
                           'razonamiento es válido.',
                           'Si en alguna fila las premisas son verdaderas y '
                           'la conclusión {falsa}, el razonamiento es '
                           '{inválido}.',
                           'La {Ley de De Morgan} establece que la negación '
                           'de una conjunción equivale a la {disyunción} de '
                           'las negaciones: ~(p ∧ q) ≡ (~p ∨ ~q).']}],
  'cuadros': [{'titulo': '13.2 ESQUEMAS SEGÚN SU RESULTADO',
               'encabezados': ['Esquema', 'Resultado'],
               'filas': [['{Tautología}', '{Verdadera} en todos los casos'],
                         ['{Contradicción}', '{Falsa} en todos los casos'],
                         ['{Contingencia}',
                          'Verdadera en {algunos} casos']]}],
  'preguntas': [{'pregunta': 'El diagrama que muestra todos los valores '
                             'posibles de una fórmula se denomina:',
                 'alternativas': ['Silogismo',
                                  'Diagrama de Venn',
                                  'Árbol de Porfirio',
                                  'Cuadro de oposición',
                                  'Tabla de verdad'],
                 'correcta': 'E'},
                {'pregunta': 'El número de combinaciones de una tabla de '
                             'verdad se calcula con:',
                 'alternativas': ['n+2', '2ⁿ', 'n²', '2n', 'n!'],
                 'correcta': 'B'},
                {'pregunta': 'Una fórmula con 3 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['3', '12', '8', '6', '9'],
                 'correcta': 'C'},
                {'pregunta': 'Una fórmula con 2 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['4', '6', '8', '3', '2'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula que resulta verdadera en todos los '
                             'casos es una:',
                 'alternativas': ['Antinomia',
                                  'Consistencia',
                                  'Tautología',
                                  'Contradicción',
                                  'Contingencia'],
                 'correcta': 'C'},
                {'pregunta': 'La fórmula que resulta falsa en todos los '
                             'casos es una:',
                 'alternativas': ['Contradicción',
                                  'Contingencia',
                                  'Implicación',
                                  'Equivalencia',
                                  'Tautología'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula verdadera en algunos casos y falsa '
                             'en otros es una:',
                 'alternativas': ['Contradicción',
                                  'Tautología',
                                  'Identidad',
                                  'Negación',
                                  'Contingencia'],
                 'correcta': 'E'},
                {'pregunta': 'El Modus Ponendo Ponens concluye q a partir '
                             'de:',
                 'alternativas': ['p → q y q → r',
                                  'p → q y ~q',
                                  'p → q y p',
                                  '~(p ∧ q)',
                                  'p ∨ q y ~p'],
                 'correcta': 'C'},
                {'pregunta': 'El Modus Tollendo Tollens concluye ~p a partir '
                             'de:',
                 'alternativas': ['p ∧ q',
                                  'p → q y ~q',
                                  'q → r',
                                  'p → q y p',
                                  'p ∨ q y ~p'],
                 'correcta': 'B'},
                {'pregunta': 'El Silogismo Disyuntivo concluye q a partir '
                             'de:',
                 'alternativas': ['p ∨ q y ~p',
                                  'p → q y ~q',
                                  'p ∧ q',
                                  'p ↔ q',
                                  'p → q y p'],
                 'correcta': 'A'},
                {'pregunta': 'El Silogismo Hipotético Puro concluye p → r a '
                             'partir de:',
                 'alternativas': ['p → q y p',
                                  'p ↔ q',
                                  'p ∨ q',
                                  '~p ∧ q',
                                  'p → q y q → r'],
                 'correcta': 'E'},
                {'pregunta': 'La ley que transforma la negación de una '
                             'conjunción en disyunción de negaciones es la '
                             'de:',
                 'alternativas': ['Identidad',
                                  'Transitividad',
                                  'De Morgan',
                                  'Contradicción',
                                  'Tercio excluido'],
                 'correcta': 'C'},
                {'pregunta': 'Si «si estudio apruebo» y «estudio», entonces '
                             '«apruebo». Este razonamiento es un:',
                 'alternativas': ['MPP', 'MTT', 'De Morgan', 'SD', 'SHP'],
                 'correcta': 'A'},
                {'pregunta': 'Si «si llueve me mojo» y «no me mojé», '
                             'entonces «no llovió». Este razonamiento es un:',
                 'alternativas': ['SD', 'MPP', 'SHP', 'DCC', 'MTT'],
                 'correcta': 'E'},
                {'pregunta': 'En una tabla de verdad, el brazo derecho de la '
                             'cruz se denomina:',
                 'alternativas': ['Cuerpo',
                                  'Columna',
                                  'Base',
                                  'Eje',
                                  'Margen'],
                 'correcta': 'A'},
                {'pregunta': 'En una tabla de verdad, el brazo izquierdo se '
                             'denomina:',
                 'alternativas': ['Cabecera',
                                  'Cuerpo',
                                  'Margen',
                                  'Pie',
                                  'Fila'],
                 'correcta': 'C'},
                {'pregunta': 'Una fórmula con 4 variables tendrá un número '
                             'de combinaciones igual a:',
                 'alternativas': ['12', '32', '8', '4', '16'],
                 'correcta': 'E'},
                {'pregunta': 'La tautología se representa habitualmente con '
                             'la letra:',
                 'alternativas': ['F', 'C', 'A', 'V', 'T'],
                 'correcta': 'E'},
                {'pregunta': 'Si «o voy al cine o voy al teatro» y «no voy '
                             'al cine», concluyo «voy al teatro». Es un:',
                 'alternativas': ['MTT',
                                  'MPP',
                                  'SHP',
                                  'Silogismo disyuntivo',
                                  'Dilema'],
                 'correcta': 'D'},
                {'pregunta': 'El dilema constructivo compuesto se abrevia '
                             'como:',
                 'alternativas': ['MTT', 'SD', 'DCC', 'SHP', 'MPP'],
                 'correcta': 'C'},
                {'pregunta': 'Un razonamiento es válido cuando es imposible '
                             'que las premisas sean verdaderas y la '
                             'conclusión:',
                 'alternativas': ['Tenga sentido',
                                  'Falsa',
                                  'También verdadera',
                                  'Contingente',
                                  'Tautológica'],
                 'correcta': 'B'},
                {'pregunta': 'Para comprobar la validez de un razonamiento '
                             'con tablas de verdad, se construye la fórmula '
                             '«(premisas) → conclusión»; si resulta '
                             'tautológica, el razonamiento es:',
                 'alternativas': ['Indeterminado',
                                  'Contingente',
                                  'Válido',
                                  'Inválido',
                                  'Contradictorio'],
                 'correcta': 'C'},
                {'pregunta': 'Si en alguna fila de la tabla las premisas son '
                             'verdaderas y la conclusión falsa, el '
                             'razonamiento es:',
                 'alternativas': ['Inválido',
                                  'Válido',
                                  'Contingente exclusivo',
                                  'Tautológico',
                                  'Necesario'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de De Morgan establece que la negación '
                             'de una conjunción equivale a:',
                 'alternativas': ['La disyunción de las negaciones',
                                  'El bicondicional de las negaciones',
                                  'La negación de la disyunción',
                                  'La conjunción de las negaciones exclusiva',
                                  'La conjunción de las afirmaciones'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'LA TABLA DE VERDAD',
                      'items': ['Es el diagrama que muestra todos los '
                                'valores posibles de una fórmula molecular.',
                                'El número de combinaciones o arreglos se '
                                'calcula con la fórmula 2ⁿ, donde n es el '
                                'número de variables.',
                                'Con 2 variables hay 4 combinaciones; con 3 '
                                'variables, 8.']},
                     {'titulo': 'PRINCIPALES ESQUEMAS',
                      'items': ['Tautología: la fórmula resulta verdadera en '
                                'todos los casos.',
                                'Contradicción: la fórmula resulta falsa en '
                                'todos los casos.',
                                'Contingencia o consistencia: resulta '
                                'verdadera en algunos casos y falsa en '
                                'otros.']},
                     {'titulo': 'VALIDEZ MEDIANTE TABLAS DE VERDAD',
                      'items': ['Un razonamiento es válido cuando es '
                                'imposible que las premisas sean verdaderas '
                                'y la conclusión falsa a la vez.',
                                'Para comprobar la validez con tablas de '
                                'verdad, se construye la fórmula «(premisas) '
                                '→ conclusión»; si resulta tautológica, el '
                                'razonamiento es válido.',
                                'Si en alguna fila las premisas son '
                                'verdaderas y la conclusión falsa, el '
                                'razonamiento es inválido.',
                                'La Ley de De Morgan establece que la '
                                'negación de una conjunción equivale a la '
                                'disyunción de las negaciones: ~(p ∧ q) ≡ '
                                '(~p ∨ ~q).']}]},
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
                           '{semejanza} entre casos.']}],
  'cuadros': [{'titulo': '14.3 JUICIOS CATEGÓRICOS TÍPICOS',
               'encabezados': ['Tipo', 'Cantidad', 'Cualidad'],
               'filas': [['{A}', '{Universal}', '{Afirmativo}'],
                         ['{E}', 'Universal', '{Negativo}'],
                         ['{I}', '{Particular}', 'Afirmativo'],
                         ['{O}', 'Particular', '{Negativo}']]}],
  'preguntas': [{'pregunta': 'El principio según el cual toda cosa es '
                             'idéntica a sí misma es el de:',
                 'alternativas': ['Causalidad',
                                  'Tercio excluido',
                                  'Razón suficiente',
                                  'Identidad',
                                  'No contradicción'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que niega que una proposición sea '
                             'verdadera y falsa a la vez es el de:',
                 'alternativas': ['No contradicción',
                                  'Tercio excluido',
                                  'Razón suficiente',
                                  'Analogía',
                                  'Identidad'],
                 'correcta': 'A'},
                {'pregunta': 'El principio que afirma que entre dos '
                             'contradictorias no hay una tercera posibilidad '
                             'es el de:',
                 'alternativas': ['Tercio excluido',
                                  'Causalidad',
                                  'Identidad',
                                  'No contradicción',
                                  'Suficiencia'],
                 'correcta': 'A'},
                {'pregunta': 'La representación mental de un objeto es el:',
                 'alternativas': ['Razonamiento',
                                  'Silogismo',
                                  'Juicio',
                                  'Concepto',
                                  'Término'],
                 'correcta': 'D'},
                {'pregunta': 'El número de objetos a los que se aplica un '
                             'concepto es su:',
                 'alternativas': ['Esencia',
                                  'Cualidad',
                                  'Cantidad',
                                  'Extensión',
                                  'Comprensión'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de notas o características de un '
                             'concepto es su:',
                 'alternativas': ['Extensión',
                                  'Cantidad',
                                  'Cualidad',
                                  'Comprensión',
                                  'Relación'],
                 'correcta': 'D'},
                {'pregunta': 'Extensión y comprensión son entre sí:',
                 'alternativas': ['Idénticas',
                                  'Directamente proporcionales',
                                  'Inversamente proporcionales',
                                  'Independientes',
                                  'Equivalentes'],
                 'correcta': 'C'},
                {'pregunta': 'La operación mental que afirma o niega algo de '
                             'algo es el:',
                 'alternativas': ['Juicio',
                                  'Término',
                                  'Silogismo',
                                  'Razonamiento',
                                  'Concepto'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión verbal del juicio es la:',
                 'alternativas': ['Oración interrogativa',
                                  'Interjección',
                                  'Proposición',
                                  'Frase',
                                  'Palabra'],
                 'correcta': 'C'},
                {'pregunta': 'Los juicios se dividen por su cantidad en '
                             'universales y:',
                 'alternativas': ['Afirmativos',
                                  'Particulares',
                                  'Categóricos',
                                  'Negativos',
                                  'Hipotéticos'],
                 'correcta': 'B'},
                {'pregunta': 'Los juicios se dividen por su cualidad en '
                             'afirmativos y:',
                 'alternativas': ['Negativos',
                                  'Compuestos',
                                  'Simples',
                                  'Particulares',
                                  'Universales'],
                 'correcta': 'A'},
                {'pregunta': 'El juicio tipo A es:',
                 'alternativas': ['Particular afirmativo',
                                  'Singular',
                                  'Particular negativo',
                                  'Universal afirmativo',
                                  'Universal negativo'],
                 'correcta': 'D'},
                {'pregunta': 'El juicio tipo E es:',
                 'alternativas': ['Particular negativo',
                                  'Indefinido',
                                  'Universal afirmativo',
                                  'Universal negativo',
                                  'Particular afirmativo'],
                 'correcta': 'D'},
                {'pregunta': 'El juicio tipo I es:',
                 'alternativas': ['Particular afirmativo',
                                  'Singular',
                                  'Universal afirmativo',
                                  'Particular negativo',
                                  'Universal negativo'],
                 'correcta': 'A'},
                {'pregunta': 'El juicio tipo O es:',
                 'alternativas': ['Particular afirmativo',
                                  'Universal negativo',
                                  'Particular negativo',
                                  'Universal afirmativo',
                                  'Hipotético'],
                 'correcta': 'C'},
                {'pregunta': '«Todos los hombres son mortales» es un juicio '
                             'de tipo:',
                 'alternativas': ['A', 'O', 'I', 'E', 'U'],
                 'correcta': 'A'},
                {'pregunta': '«Ningún metal es líquido» es un juicio de '
                             'tipo:',
                 'alternativas': ['I', 'O', 'A', 'U', 'E'],
                 'correcta': 'E'},
                {'pregunta': 'El razonamiento que va de lo general a lo '
                             'particular es:',
                 'alternativas': ['Inductivo',
                                  'Dialéctico',
                                  'Deductivo',
                                  'Analógico',
                                  'Abductivo'],
                 'correcta': 'C'},
                {'pregunta': 'El razonamiento cuya conclusión es solo '
                             'probable es el:',
                 'alternativas': ['Deductivo',
                                  'Inductivo',
                                  'Apodíctico',
                                  'Formal',
                                  'Silogístico'],
                 'correcta': 'B'},
                {'pregunta': 'El razonamiento que concluye por semejanza '
                             'entre casos es el:',
                 'alternativas': ['Deductivo',
                                  'Silogístico',
                                  'Inductivo completo',
                                  'Analógico',
                                  'Hipotético'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'PRINCIPIOS LÓGICOS',
                      'items': ['Principio de identidad: toda cosa es '
                                'idéntica a sí misma. Se expresa «p es p».',
                                'Principio de no contradicción: una '
                                'proposición no puede ser verdadera y falsa '
                                'a la vez.',
                                'Principio del tercio excluido: entre dos '
                                'proposiciones contradictorias, una es '
                                'verdadera y la otra falsa; no hay una '
                                'tercera posibilidad.']},
                     {'titulo': 'EL CONCEPTO',
                      'items': ['Es la representación mental de un objeto. '
                                'Sus características pueden ser esenciales o '
                                'accidentales.',
                                'Propiedades del concepto: la extensión, que '
                                'es el número de objetos a los que se '
                                'aplica, y la comprensión, que es el '
                                'conjunto de notas o características.',
                                'Ambas son inversamente proporcionales: a '
                                'mayor extensión, menor comprensión.']},
                     {'titulo': 'EL JUICIO',
                      'items': ['Es la operación mental que afirma o niega '
                                'algo de algo. Su expresión verbal es la '
                                'proposición.',
                                'Por su cantidad: universales y '
                                'particulares.',
                                'Por su cualidad: afirmativos y negativos.',
                                'Juicios categóricos típicos: A (universal '
                                'afirmativo), E (universal negativo), I '
                                '(particular afirmativo) y O (particular '
                                'negativo).']},
                     {'titulo': 'EL RAZONAMIENTO',
                      'items': ['Razonamiento deductivo: va de lo general a '
                                'lo particular; la conclusión se sigue '
                                'necesariamente.',
                                'Razonamiento inductivo: va de lo particular '
                                'a lo general; la conclusión es probable.',
                                'Razonamiento analógico: concluye por '
                                'semejanza entre casos.']}]},
 {'num': 15,
  'titulo': 'Inferencias',
  'secciones': [{'titulo': '15.1 INFERENCIAS INMEDIATAS',
                 'items': ['Son aquellas en que se obtiene una conclusión a '
                           'partir de una {sola} premisa.',
                           'Por {oposición}: se basan en el cuadro '
                           'tradicional de oposición, o cuadro de {Boecio}, '
                           'entre juicios A, E, I, O. Comprende '
                           'contradicción, contrariedad, {subcontrariedad} y '
                           'subalternación.',
                           'Por {conversión}: se intercambian el {sujeto} y '
                           'el {predicado}. Ejemplo: «Ningún S es P» se '
                           'convierte en «Ningún {P} es S».',
                           'Por {obversión}: se cambia la {cualidad} del '
                           'juicio y se niega el {predicado}. «Todo S es P» '
                           'se obvierte en «Ningún S es {no-P}».',
                           'Son {contradictorias} los pares A—O y E—{I}: no '
                           'pueden ser ambas verdaderas ni ambas falsas.',
                           'En la {subalternación}, la proposición universal '
                           '(subalternante) implica a la particular '
                           '(subalterna); si la universal es verdadera, la '
                           'subalterna también lo es; si la universal es '
                           'falsa, la subalterna queda {indeterminada}.']},
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
                           'posición del término {medio}: son {cuatro}.']}],
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
                 'alternativas': ['Silogística',
                                  'Deductiva compuesta',
                                  'Analógica',
                                  'Mediata',
                                  'Inmediata'],
                 'correcta': 'E'},
                {'pregunta': 'La inferencia en que se intercambian sujeto y '
                             'predicado se denomina:',
                 'alternativas': ['Conversión',
                                  'Contraposición',
                                  'Obversión',
                                  'Subalternación',
                                  'Oposición'],
                 'correcta': 'A'},
                {'pregunta': 'La inferencia en que se cambia la cualidad y '
                             'se niega el predicado es la:',
                 'alternativas': ['Contrapuesta total',
                                  'Contrariedad',
                                  'Obversión',
                                  'Subalternación',
                                  'Conversión'],
                 'correcta': 'C'},
                {'pregunta': '«Todo S es P» obvertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Algún S no es P',
                                  'Ningún S es no-P',
                                  'Ningún P es S',
                                  'Algún S es P'],
                 'correcta': 'C'},
                {'pregunta': 'El cuadro de oposición relaciona los juicios:',
                 'alternativas': ['Deductivos e inductivos',
                                  'A, E, I, O',
                                  'Verdaderos y falsos',
                                  'Simples y compuestos',
                                  'Mayor y menor'],
                 'correcta': 'B'},
                {'pregunta': 'La inferencia que parte de dos o más premisas '
                             'se denomina:',
                 'alternativas': ['Mediata',
                                  'Inmediata',
                                  'Directa',
                                  'Unilateral',
                                  'Simple'],
                 'correcta': 'A'},
                {'pregunta': 'La forma típica de la inferencia mediata es '
                             'el:',
                 'alternativas': ['Sorites',
                                  'Epiquerema',
                                  'Dilema',
                                  'Silogismo',
                                  'Entimema'],
                 'correcta': 'D'},
                {'pregunta': 'El silogismo categórico consta de:',
                 'alternativas': ['Cinco proposiciones',
                                  'Una proposición',
                                  'Dos proposiciones',
                                  'Tres proposiciones',
                                  'Cuatro proposiciones'],
                 'correcta': 'D'},
                {'pregunta': 'El término que aparece en ambas premisas pero '
                             'no en la conclusión es el:',
                 'alternativas': ['Sujeto',
                                  'Predicado',
                                  'Mayor',
                                  'Medio',
                                  'Menor'],
                 'correcta': 'D'},
                {'pregunta': 'El término mayor del silogismo es el:',
                 'alternativas': ['Término medio',
                                  'Predicado de la conclusión',
                                  'Sujeto de la conclusión',
                                  'Que aparece dos veces',
                                  'Que se omite'],
                 'correcta': 'B'},
                {'pregunta': 'El término menor del silogismo es el:',
                 'alternativas': ['Sujeto de la conclusión',
                                  'Que no aparece',
                                  'Término medio',
                                  'Predicado de la conclusión',
                                  'Universal'],
                 'correcta': 'A'},
                {'pregunta': 'De dos premisas negativas:',
                 'alternativas': ['Se sigue una conclusión afirmativa',
                                  'Se sigue una conclusión negativa',
                                  'Se sigue siempre una universal',
                                  'No se sigue conclusión alguna',
                                  'Se sigue una particular'],
                 'correcta': 'D'},
                {'pregunta': 'De dos premisas particulares:',
                 'alternativas': ['No se sigue conclusión alguna',
                                  'Se sigue una conclusión particular',
                                  'Se sigue una negativa',
                                  'Se sigue una universal',
                                  'Se sigue una afirmativa'],
                 'correcta': 'A'},
                {'pregunta': 'El término medio debe estar distribuido:',
                 'alternativas': ['Siempre dos veces',
                                  'Nunca',
                                  'Al menos una vez',
                                  'En el predicado',
                                  'Solo en la conclusión'],
                 'correcta': 'C'},
                {'pregunta': 'Las figuras del silogismo se determinan por la '
                             'posición del:',
                 'alternativas': ['Término menor',
                                  'Sujeto',
                                  'Término mayor',
                                  'Predicado',
                                  'Término medio'],
                 'correcta': 'E'},
                {'pregunta': 'El número de figuras del silogismo es:',
                 'alternativas': ['Seis', 'Tres', 'Ocho', 'Cuatro', 'Dos'],
                 'correcta': 'D'},
                {'pregunta': '«Ningún S es P» convertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Algún P es S',
                                  'Ningún P es S',
                                  'Algún S no es P',
                                  'Todo S es no-P'],
                 'correcta': 'C'},
                {'pregunta': 'La contrapuesta total se obtiene:',
                 'alternativas': ['Negando la conclusión',
                                  'Cambiando solo la cualidad',
                                  'Solo obvirtiendo',
                                  'Negando ambos términos e '
                                  'intercambiándolos',
                                  'Solo convirtiendo'],
                 'correcta': 'D'},
                {'pregunta': 'La relación entre A y O en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Contradicción',
                                  'Subalternación',
                                  'Subcontrariedad',
                                  'Contrariedad',
                                  'Equivalencia'],
                 'correcta': 'A'},
                {'pregunta': 'La relación entre A y E en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Identidad',
                                  'Contradicción',
                                  'Subcontrariedad',
                                  'Contrariedad',
                                  'Subalternación'],
                 'correcta': 'D'},
                {'pregunta': 'El cuadro tradicional de oposición entre los '
                             'juicios A, E, I, O también se conoce como '
                             'cuadro de:',
                 'alternativas': ['Boecio',
                                  'Leibniz',
                                  'Porfirio',
                                  'Kant',
                                  'Aristóteles'],
                 'correcta': 'A'},
                {'pregunta': 'En el cuadro de oposición, los pares de '
                             'proposiciones contradictorias son:',
                 'alternativas': ['A—O y E—I',
                                  'A—E y I—O',
                                  'Solo I—O',
                                  'A—I y E—O',
                                  'Solo A—E'],
                 'correcta': 'A'},
                {'pregunta': 'En la subalternación, si la proposición '
                             'universal (subalternante) es verdadera, la '
                             'particular (subalterna) es:',
                 'alternativas': ['También verdadera',
                                  'Indeterminada',
                                  'Contradictoria',
                                  'Falsa',
                                  'Imposible'],
                 'correcta': 'A'},
                {'pregunta': 'En la subalternación, si la proposición '
                             'universal es falsa, la particular subalterna '
                             'queda:',
                 'alternativas': ['También falsa',
                                  'Indeterminada',
                                  'Verdadera',
                                  'Imposible de evaluar',
                                  'Contradictoria'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'INFERENCIAS INMEDIATAS',
                      'items': ['Son aquellas en que se obtiene una '
                                'conclusión a partir de una sola premisa.',
                                'Por oposición: se basan en el cuadro '
                                'tradicional de oposición, o cuadro de '
                                'Boecio, entre juicios A, E, I, O. Comprende '
                                'contradicción, contrariedad, '
                                'subcontrariedad y subalternación.',
                                'Por conversión: se intercambian el sujeto y '
                                'el predicado. Ejemplo: «Ningún S es P» se '
                                'convierte en «Ningún P es S».',
                                'Por obversión: se cambia la cualidad del '
                                'juicio y se niega el predicado. «Todo S es '
                                'P» se obvierte en «Ningún S es no-P».',
                                'Son contradictorias los pares A—O y E—I: no '
                                'pueden ser ambas verdaderas ni ambas '
                                'falsas.',
                                'En la subalternación, la proposición '
                                'universal (subalternante) implica a la '
                                'particular (subalterna); si la universal es '
                                'verdadera, la subalterna también lo es; si '
                                'la universal es falsa, la subalterna queda '
                                'indeterminada.']},
                     {'titulo': 'Y 15.3 CONTRAPUESTA E INFERENCIA MEDIATA',
                      'items': ['Por contrapuesta parcial: se obtiene '
                                'combinando obversión y conversión.',
                                'Por contrapuesta total: se niegan ambos '
                                'términos y se intercambian.',
                                'La inferencia mediata obtiene la conclusión '
                                'a partir de dos o más premisas; su forma '
                                'típica es el silogismo.']},
                     {'titulo': 'EL SILOGISMO CATEGÓRICO',
                      'items': ['Consta de tres proposiciones: premisa '
                                'mayor, premisa menor y conclusión.',
                                'Y de tres términos: mayor (P, predicado de '
                                'la conclusión), menor (S, sujeto de la '
                                'conclusión) y medio (M), que aparece en '
                                'ambas premisas pero no en la conclusión.',
                                'Reglas principales: de dos premisas '
                                'negativas no se sigue conclusión; de dos '
                                'premisas particulares tampoco; el término '
                                'medio debe estar distribuido al menos una '
                                'vez.',
                                'Las figuras del silogismo se determinan por '
                                'la posición del término medio: son '
                                'cuatro.']}]},
 {'num': 16,
  'titulo': 'Lógica de clases',
  'secciones': [{'titulo': '16.1 EL ÁLGEBRA BOOLEANA',
                 'items': ['Fue desarrollada por George {Boole}. Aplica '
                           'procedimientos {algebraicos} al razonamiento '
                           'lógico.',
                           'Una {clase} es el conjunto de todos los objetos '
                           'que poseen una {característica} común.',
                           'Clase {universal}: contiene todos los elementos '
                           'del universo del discurso —llamado así por {De '
                           'Morgan}—; se representa por {1}.',
                           'Clase {vacía} o nula: no contiene ningún '
                           'elemento; se representa por {0} o por la letra '
                           'griega {fi}.']},
                {'titulo': '16.2 TIPOS DE CLASES',
                 'items': ['Clase {universal}, clase {particular} y '
                           '{complemento} de una clase.',
                           'El {complemento} de una clase A está formado por '
                           'todos los elementos que {no} pertenecen a A. Se '
                           'simboliza {Ā}.',
                           'Clase {no vacía}: tiene al menos un elemento, '
                           'como la clase de los {alcaldes} o la clase de '
                           'libros.',
                           'El {álgebra booleana} también rige circuitos '
                           'digitales; Claudio {Shannon} desarrolló sus '
                           'primeras aplicaciones en {1938}.']},
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
                           'clase pero {no} a la otra.']}],
  'cuadros': [{'titulo': '16. CLASES Y SÍMBOLOS',
               'encabezados': ['Concepto', 'Símbolo'],
               'filas': [['Clase {universal}', '{1}'],
                         ['Clase {vacía}', '{0}'],
                         ['{Complemento} de A', '{Ā}'],
                         ['{Unión}', '{∪}'],
                         ['{Intersección}', '{∩}']]}],
  'preguntas': [{'pregunta': 'El álgebra que aplica procedimientos '
                             'algebraicos a la lógica fue desarrollada por:',
                 'alternativas': ['Frege',
                                  'Venn',
                                  'George Boole',
                                  'Russell',
                                  'Aristóteles'],
                 'correcta': 'C'},
                {'pregunta': 'El conjunto de todos los objetos que poseen '
                             'una característica común es una:',
                 'alternativas': ['Proposición',
                                  'Premisa',
                                  'Inferencia',
                                  'Variable',
                                  'Clase'],
                 'correcta': 'E'},
                {'pregunta': 'La clase que contiene todos los elementos del '
                             'universo del discurso es la clase:',
                 'alternativas': ['Particular',
                                  'Nula',
                                  'Universal',
                                  'Vacía',
                                  'Complementaria'],
                 'correcta': 'C'},
                {'pregunta': 'La clase universal se representa con el '
                             'símbolo:',
                 'alternativas': ['∩', 'Ā', '0', '∪', '1'],
                 'correcta': 'E'},
                {'pregunta': 'La clase que no contiene ningún elemento se '
                             'denomina:',
                 'alternativas': ['Particular',
                                  'Vacía o nula',
                                  'Unitaria',
                                  'Universal',
                                  'Complementaria'],
                 'correcta': 'B'},
                {'pregunta': 'La clase vacía se representa con el símbolo:',
                 'alternativas': ['∅ únicamente', '0', '∪', '1', 'Ā'],
                 'correcta': 'B'},
                {'pregunta': 'El complemento de una clase A está formado por '
                             'los elementos que:',
                 'alternativas': ['Pertenecen a A',
                                  'No pertenecen a A',
                                  'Son comunes',
                                  'Son universales',
                                  'Pertenecen a A y B'],
                 'correcta': 'B'},
                {'pregunta': 'El complemento de la clase A se simboliza:',
                 'alternativas': ['1', 'A∩B', 'A∪B', 'A-B', 'Ā'],
                 'correcta': 'E'},
                {'pregunta': 'La relación en que todos los elementos de una '
                             'clase están contenidos en otra es:',
                 'alternativas': ['Igualdad',
                                  'Inclusión',
                                  'Diferencia',
                                  'Complemento',
                                  'Exclusión'],
                 'correcta': 'B'},
                {'pregunta': 'La relación en que dos clases tienen '
                             'exactamente los mismos elementos es:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Exclusión',
                                  'Igualdad',
                                  'Inclusión'],
                 'correcta': 'D'},
                {'pregunta': 'La relación en que dos clases no tienen ningún '
                             'elemento en común es:',
                 'alternativas': ['Igualdad',
                                  'Inclusión',
                                  'Complemento',
                                  'Unión',
                                  'Exclusión'],
                 'correcta': 'E'},
                {'pregunta': 'La operación que reúne los elementos de ambas '
                             'clases es la:',
                 'alternativas': ['Inclusión',
                                  'Unión',
                                  'Complementación',
                                  'Diferencia',
                                  'Intersección'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que reúne solo los elementos '
                             'comunes es la:',
                 'alternativas': ['Diferencia',
                                  'Suma',
                                  'Intersección',
                                  'Complemento',
                                  'Unión'],
                 'correcta': 'C'},
                {'pregunta': 'El símbolo ∪ representa la:',
                 'alternativas': ['Inclusión',
                                  'Unión',
                                  'Exclusión',
                                  'Intersección',
                                  'Diferencia'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∩ representa la:',
                 'alternativas': ['Intersección',
                                  'Complemento',
                                  'Diferencia',
                                  'Unión',
                                  'Igualdad'],
                 'correcta': 'A'},
                {'pregunta': 'La operación que toma los elementos de una '
                             'clase que no están en la otra es la:',
                 'alternativas': ['Inclusión',
                                  'Intersección',
                                  'Unión',
                                  'Igualdad',
                                  'Diferencia'],
                 'correcta': 'E'},
                {'pregunta': 'La lógica de clases se ocupa de las relaciones '
                             'entre:',
                 'alternativas': ['Clases o conjuntos',
                                  'Silogismos',
                                  'Valores',
                                  'Proposiciones',
                                  'Falacias'],
                 'correcta': 'A'},
                {'pregunta': '«Los peruanos» y «los no peruanos» son entre '
                             'sí:',
                 'alternativas': ['Una sola clase',
                                  'Clases iguales',
                                  'Clases idénticas',
                                  'Clases incluidas',
                                  'Clases complementarias'],
                 'correcta': 'E'},
                {'pregunta': 'La unión también recibe el nombre de:',
                 'alternativas': ['Resta',
                                  'Cociente',
                                  'Suma',
                                  'Producto',
                                  'Potencia'],
                 'correcta': 'C'},
                {'pregunta': 'La intersección también recibe el nombre de:',
                 'alternativas': ['Diferencia',
                                  'Suma',
                                  'Producto',
                                  'Unión',
                                  'Complemento'],
                 'correcta': 'C'},
                {'pregunta': 'El concepto de «universo del discurso», para '
                             'referirse a la clase universal, fue llamado '
                             'así por:',
                 'alternativas': ['George Boole',
                                  'Aristóteles',
                                  'De Morgan',
                                  'Leibniz',
                                  'Porfirio'],
                 'correcta': 'C'},
                {'pregunta': 'Además del número cero, la clase vacía también '
                             'se puede simbolizar con la letra griega:',
                 'alternativas': ['Alfa', 'Fi', 'Omega', 'Pi', 'Sigma'],
                 'correcta': 'B'},
                {'pregunta': 'La clase que tiene al menos un elemento, como '
                             'la clase de los alcaldes, se llama clase:',
                 'alternativas': ['No vacía',
                                  'Universal exclusiva',
                                  'Vacía',
                                  'Nula',
                                  'Complementaria'],
                 'correcta': 'A'},
                {'pregunta': 'El científico que desarrolló las primeras '
                             'aplicaciones del álgebra booleana a circuitos '
                             'digitales, en 1938, fue:',
                 'alternativas': ['George Boole',
                                  'Alan Turing',
                                  'Gottlob Frege',
                                  'Augustus De Morgan',
                                  'Claudio Shannon'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'EL ÁLGEBRA BOOLEANA',
                      'items': ['Fue desarrollada por George Boole. Aplica '
                                'procedimientos algebraicos al razonamiento '
                                'lógico.',
                                'Una clase es el conjunto de todos los '
                                'objetos que poseen una característica '
                                'común.',
                                'Clase universal: contiene todos los '
                                'elementos del universo del discurso '
                                '—llamado así por De Morgan—; se representa '
                                'por 1.',
                                'Clase vacía o nula: no contiene ningún '
                                'elemento; se representa por 0 o por la '
                                'letra griega fi.']},
                     {'titulo': 'TIPOS DE CLASES',
                      'items': ['Clase universal, clase particular y '
                                'complemento de una clase.',
                                'El complemento de una clase A está formado '
                                'por todos los elementos que no pertenecen a '
                                'A. Se simboliza Ā.',
                                'Clase no vacía: tiene al menos un elemento, '
                                'como la clase de los alcaldes o la clase de '
                                'libros.',
                                'El álgebra booleana también rige circuitos '
                                'digitales; Claudio Shannon desarrolló sus '
                                'primeras aplicaciones en 1938.']},
                     {'titulo': 'RELACIONES ENTRE CLASES',
                      'items': ['Inclusión: todos los elementos de una clase '
                                'están contenidos en otra.',
                                'Igualdad: dos clases tienen exactamente los '
                                'mismos elementos.',
                                'Exclusión: dos clases no tienen ningún '
                                'elemento en común.']},
                     {'titulo': 'OPERACIONES CON CLASES',
                      'items': ['Unión o suma: reúne los elementos de ambas '
                                'clases. Se simboliza ∪.',
                                'Intersección o producto: reúne los '
                                'elementos comunes a ambas clases. Se '
                                'simboliza ∩.',
                                'Diferencia: elementos que pertenecen a una '
                                'clase pero no a la otra.']}]},
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
                           '{universales} y después las particulares.',
                           'De los 256 modos posibles del silogismo '
                           'categórico, solo {19} son considerados válidos '
                           'según la lógica tradicional.',
                           'La {ley del contenido existencial} se aplica '
                           'cuando ambas premisas son universales y la '
                           'conclusión es {particular}.']}],
  'cuadros': [{'titulo': '17.1 SIMBOLOGÍA DE LOS DIAGRAMAS',
               'encabezados': ['Signo', 'Significado'],
               'filas': [['{Sombreado}', 'La región está {vacía}'],
                         ['{X}', 'La región tiene al menos un {elemento}'],
                         ['Región {en blanco}',
                          'No se sabe si tiene elementos']]}],
  'preguntas': [{'pregunta': 'Los diagramas que representan clases mediante '
                             'círculos fueron ideados por:',
                 'alternativas': ['Venn',
                                  'Boole',
                                  'Frege',
                                  'Russell',
                                  'Euler únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'En un diagrama de Venn, el sombreado indica '
                             'que la región:',
                 'alternativas': ['Es dudosa',
                                  'Es universal',
                                  'Es infinita',
                                  'Tiene elementos',
                                  'Está vacía'],
                 'correcta': 'E'},
                {'pregunta': 'En un diagrama de Venn, la X indica que la '
                             'región:',
                 'alternativas': ['Es universal',
                                  'Es complementaria',
                                  'Tiene al menos un elemento',
                                  'Se excluye',
                                  'Está vacía'],
                 'correcta': 'C'},
                {'pregunta': '«Ningún S es P» se representa sombreando:',
                 'alternativas': ['El círculo P',
                                  'Nada',
                                  'La región fuera de ambos',
                                  'La región común a S y P',
                                  'Todo el círculo S'],
                 'correcta': 'D'},
                {'pregunta': '«Algún S es P» se representa colocando una X '
                             'en:',
                 'alternativas': ['Fuera de ambos círculos',
                                  'La región común a S y P',
                                  'La parte de S fuera de P',
                                  'El universo',
                                  'El círculo P completo'],
                 'correcta': 'B'},
                {'pregunta': '«Todo S es P» se representa sombreando:',
                 'alternativas': ['El universo',
                                  'La región común',
                                  'La parte de S que no es P',
                                  'Todo el círculo P',
                                  'Fuera de ambos'],
                 'correcta': 'C'},
                {'pregunta': '«Algún S no es P» se representa con una X en:',
                 'alternativas': ['La región común',
                                  'El centro',
                                  'La parte de S fuera de P',
                                  'Fuera de ambos',
                                  'El círculo P'],
                 'correcta': 'C'},
                {'pregunta': 'Con dos clases, el número de regiones que se '
                             'generan es:',
                 'alternativas': ['8', '6', '4', '2', '3'],
                 'correcta': 'C'},
                {'pregunta': 'Las proposiciones típicas son las que '
                             'corresponden a las formas:',
                 'alternativas': ['A, E, I, O',
                                  'Deductivas',
                                  'Universales solamente',
                                  'Verdaderas y falsas',
                                  'Simples y compuestas'],
                 'correcta': 'A'},
                {'pregunta': 'Las proposiciones atípicas requieren ser:',
                 'alternativas': ['Rechazadas',
                                  'Ignoradas',
                                  'Convertidas en falacias',
                                  'Negadas',
                                  'Traducidas a una forma típica'],
                 'correcta': 'E'},
                {'pregunta': 'Expresiones como «solo» y «únicamente» suelen '
                             'equivaler a juicios:',
                 'alternativas': ['Particulares',
                                  'Negativos siempre',
                                  'Universales',
                                  'Singulares',
                                  'Indefinidos'],
                 'correcta': 'C'},
                {'pregunta': 'Para evaluar la validez de un silogismo se '
                             'usan:',
                 'alternativas': ['Cuatro círculos',
                                  'Cinco círculos',
                                  'Tres círculos',
                                  'Dos círculos',
                                  'Un círculo'],
                 'correcta': 'C'},
                {'pregunta': 'Al evaluar un silogismo por diagramas, se '
                             'diagraman:',
                 'alternativas': ['Todo simultáneamente',
                                  'Solo la mayor',
                                  'Solo las premisas',
                                  'La conclusión primero',
                                  'Solo la menor'],
                 'correcta': 'C'},
                {'pregunta': 'Un silogismo es válido si, al diagramar las '
                             'premisas:',
                 'alternativas': ['Queda automáticamente representada la '
                                  'conclusión',
                                  'No hay ninguna X',
                                  'Queda alguna región vacía',
                                  'Las premisas son verdaderas',
                                  'Se sombrean todos los círculos'],
                 'correcta': 'A'},
                {'pregunta': 'Al diagramar conviene comenzar por las '
                             'premisas:',
                 'alternativas': ['Afirmativas',
                                  'Particulares',
                                  'Universales',
                                  'Negativas',
                                  'Más largas'],
                 'correcta': 'C'},
                {'pregunta': 'Una región en blanco en un diagrama de Venn '
                             'significa que:',
                 'alternativas': ['No se sabe si tiene elementos',
                                  'Está vacía',
                                  'Es contradictoria',
                                  'Tiene elementos',
                                  'Es universal'],
                 'correcta': 'A'},
                {'pregunta': 'El diagrama de Venn permite determinar de un '
                             'silogismo su:',
                 'alternativas': ['Verdad material',
                                  'Belleza',
                                  'Utilidad',
                                  'Origen',
                                  'Validez formal'],
                 'correcta': 'E'},
                {'pregunta': 'Los diagramas de Venn representan '
                             'gráficamente:',
                 'alternativas': ['Falacias',
                                  'Proposiciones compuestas',
                                  'Clases y sus relaciones',
                                  'Tablas de verdad',
                                  'Conectores lógicos'],
                 'correcta': 'C'},
                {'pregunta': 'En la diagramación, el círculo que se dibuja '
                             'para el término medio:',
                 'alternativas': ['Se marca con X',
                                  'No se dibuja',
                                  'Se sombrea siempre',
                                  'Se dibuja aparte',
                                  'Se dibuja intersecando a los otros dos'],
                 'correcta': 'E'},
                {'pregunta': 'Diagramar la conclusión antes que las premisas '
                             'constituye:',
                 'alternativas': ['Un error de método',
                                  'Un atajo permitido',
                                  'Una regla de Venn',
                                  'Una simplificación válida',
                                  'El procedimiento correcto'],
                 'correcta': 'A'},
                {'pregunta': 'De los 256 modos posibles del silogismo '
                             'categórico, el número considerado válido según '
                             'la lógica tradicional es:',
                 'alternativas': ['24', '15', '30', '256', '19'],
                 'correcta': 'E'},
                {'pregunta': 'La ley del contenido existencial se aplica en '
                             'un silogismo cuando ambas premisas son '
                             'universales y la conclusión es:',
                 'alternativas': ['Negativa exclusiva',
                                  'Indefinida',
                                  'También universal',
                                  'Particular',
                                  'Afirmativa exclusiva'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'DIAGRAMACIÓN DE UNA CLASE',
                      'items': ['Los diagramas de Venn representan '
                                'gráficamente las clases mediante círculos.',
                                'El sombreado indica que la región está '
                                'vacía; una X indica que la región tiene al '
                                'menos un elemento.',
                                '«Ningún S es P» se representa sombreando la '
                                'región común a ambos círculos.',
                                '«Algún S es P» se representa colocando una '
                                'X en la región común.']},
                     {'titulo': 'DIAGRAMACIÓN DE DOS CLASES',
                      'items': ['Con dos clases se generan 4 regiones '
                                'distintas.',
                                '«Todo S es P» se representa sombreando la '
                                'parte de S que no es P.',
                                '«Algún S no es P» se representa con una X '
                                'en la parte de S fuera de P.']},
                     {'titulo': 'PROPOSICIONES TÍPICAS Y ATÍPICAS',
                      'items': ['Proposiciones típicas: las que corresponden '
                                'a las formas A, E, I y O.',
                                'Proposiciones atípicas: deben ser '
                                'traducidas previamente a una forma típica '
                                'para poder diagramarse.',
                                'Ejemplos de atípicas: «solo», «únicamente», '
                                '«nadie salvo», que suelen equivaler a '
                                'juicios universales.']},
                     {'titulo': 'VALIDEZ DEL SILOGISMO POR DIAGRAMAS',
                      'items': ['Para evaluar un silogismo se usan tres '
                                'círculos, uno por cada término.',
                                'Se diagraman primero las premisas, nunca la '
                                'conclusión.',
                                'Si al diagramar las premisas queda '
                                'automáticamente representada la conclusión, '
                                'el silogismo es válido.',
                                'Conviene diagramar primero las premisas '
                                'universales y después las particulares.',
                                'De los 256 modos posibles del silogismo '
                                'categórico, solo 19 son considerados '
                                'válidos según la lógica tradicional.',
                                'La ley del contenido existencial se aplica '
                                'cuando ambas premisas son universales y la '
                                'conclusión es particular.']}]}]
