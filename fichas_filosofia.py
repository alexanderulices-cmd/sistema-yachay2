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
                {'titulo': '1.4 ACTITUD FILOSÓFICA',
                 'items': ['Es la disposición humana por comprender el '
                           '{porqué} y el {para qué} de las cosas.',
                           'Características: {problemática}, {crítica}, '
                           '{incondicional}, {universal}, {trascendental}, '
                           'racional y {reflexiva}, y un saber '
                           '{totalitario}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El conjunto de mitos con que las primeras '
                           'civilizaciones explicaron el origen del universo '
                           'se denomina {Cosmogonía}.',
                           'El autor del poema «Teogonía» fue {Hesíodo}.',
                           'La cosmología se diferencia de la cosmogonía '
                           'porque explica mediante {Conceptos científicos y '
                           'verificación}.',
                           'El geocentrismo fue respaldado por {Ptolomeo y '
                           'Aristóteles}.',
                           'El heliocentrismo fue sostenido por {Nicolás '
                           'Copérnico}.',
                           'Según el Big Bang, el universo se originó hace '
                           'aproximadamente {14 000 millones de años}.',
                           'Hubble descubrió en 1929 que las galaxias {Se '
                           'alejan unas de otras}.',
                           'Según la ley de Hubble, la velocidad de una '
                           'galaxia es proporcional a su {Distancia}.',
                           'Si una fuente de luz se aleja de nosotros, su '
                           'espectro se desplaza hacia el {Rojo}.',
                           'Se atribuye el primer uso del término '
                           '«filosofía» a {Pitágoras de Samos}.',
                           'Para Platón, el origen de la filosofía está en '
                           '{El asombro}.',
                           'Etimológicamente, filosofía significa {Amor a la '
                           'sabiduría}.',
                           'Para Aristóteles, la filosofía es la ciencia de '
                           '{Los primeros principios y las primeras causas}.',
                           'La filosofía primera, según Aristóteles, se '
                           'denomina también {Metafísica}.',
                           'Según Russell, la filosofía nació de la unión o '
                           'el conflicto de dos impulsos {Místico y '
                           'científico}.',
                           'Para Rosental, la cuestión fundamental de la '
                           'filosofía es la relación entre {El pensar y el '
                           'ser}.',
                           'La actitud filosófica se define como la '
                           'disposición por comprender {El porqué y el para '
                           'qué de las cosas}.',
                           'Que la actitud filosófica sea «incondicional» '
                           'significa que {Busca el saber por el saber '
                           'mismo}.',
                           'La filosofía, como reflexión racional y '
                           'sistemática, se origina en {Grecia}.']}],
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
                 'alternativas': ['Cosmología',
                                  'Cosmogonía',
                                  'Ontología',
                                  'Astronomía',
                                  'Metafísica'],
                 'correcta': 'B'},
                {'pregunta': 'El autor del poema «Teogonía» fue:',
                 'alternativas': ['Homero',
                                  'Hesíodo',
                                  'Platón',
                                  'Ptolomeo',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'La cosmología se diferencia de la cosmogonía '
                             'porque explica mediante:',
                 'alternativas': ['Relatos y mitos',
                                  'Conceptos científicos y verificación',
                                  'Revelaciones divinas',
                                  'Tradiciones orales',
                                  'Poemas épicos'],
                 'correcta': 'B'},
                {'pregunta': 'El geocentrismo fue respaldado por:',
                 'alternativas': ['Copérnico',
                                  'Ptolomeo y Aristóteles',
                                  'Galileo',
                                  'Kepler',
                                  'Hubble'],
                 'correcta': 'B'},
                {'pregunta': 'El heliocentrismo fue sostenido por:',
                 'alternativas': ['Ptolomeo',
                                  'Nicolás Copérnico',
                                  'Aristóteles',
                                  'Hesíodo',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'Según el Big Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['4 000 millones de años',
                                  '14 000 millones de años',
                                  '1 000 millones de años',
                                  '100 000 años',
                                  '500 millones de años'],
                 'correcta': 'B'},
                {'pregunta': 'Hubble descubrió en 1929 que las galaxias:',
                 'alternativas': ['Permanecen inmóviles',
                                  'Se alejan unas de otras',
                                  'Se acercan entre sí',
                                  'Giran alrededor de la Tierra',
                                  'Están fijas en la bóveda celeste'],
                 'correcta': 'B'},
                {'pregunta': 'Según la ley de Hubble, la velocidad de una '
                             'galaxia es proporcional a su:',
                 'alternativas': ['Masa',
                                  'Distancia',
                                  'Temperatura',
                                  'Luminosidad',
                                  'Edad'],
                 'correcta': 'B'},
                {'pregunta': 'Si una fuente de luz se aleja de nosotros, su '
                             'espectro se desplaza hacia el:',
                 'alternativas': ['Azul',
                                  'Rojo',
                                  'Verde',
                                  'Violeta',
                                  'Amarillo'],
                 'correcta': 'B'},
                {'pregunta': 'Se atribuye el primer uso del término '
                             '«filosofía» a:',
                 'alternativas': ['Sócrates',
                                  'Pitágoras de Samos',
                                  'Platón',
                                  'Aristóteles',
                                  'Tales de Mileto'],
                 'correcta': 'B'},
                {'pregunta': 'Para Platón, el origen de la filosofía está '
                             'en:',
                 'alternativas': ['La duda',
                                  'El asombro',
                                  'La fe',
                                  'La necesidad',
                                  'El lenguaje'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, filosofía significa:',
                 'alternativas': ['Estudio del ser',
                                  'Amor a la sabiduría',
                                  'Ciencia del pensar',
                                  'Estudio del cosmos',
                                  'Búsqueda de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'Para Aristóteles, la filosofía es la ciencia '
                             'de:',
                 'alternativas': ['Los fenómenos naturales',
                                  'Los primeros principios y las primeras '
                                  'causas',
                                  'La conducta humana',
                                  'El lenguaje',
                                  'La sociedad'],
                 'correcta': 'B'},
                {'pregunta': 'La filosofía primera, según Aristóteles, se '
                             'denomina también:',
                 'alternativas': ['Lógica',
                                  'Metafísica',
                                  'Ética',
                                  'Física',
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
                 'alternativas': ['El bien y el mal',
                                  'El pensar y el ser',
                                  'Lo bello y lo útil',
                                  'La causa y el efecto',
                                  'La forma y la materia'],
                 'correcta': 'B'},
                {'pregunta': 'La actitud filosófica se define como la '
                             'disposición por comprender:',
                 'alternativas': ['Solo el cómo de las cosas',
                                  'El porqué y el para qué de las cosas',
                                  'Únicamente lo mensurable',
                                  'Los hechos históricos',
                                  'Las creencias religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'NO es una característica de la actitud '
                             'filosófica:',
                 'alternativas': ['Crítica',
                                  'Universal',
                                  'Trascendental',
                                  'Problemática',
                                  'Dogmática'],
                 'correcta': 'E'},
                {'pregunta': 'Que la actitud filosófica sea «incondicional» '
                             'significa que:',
                 'alternativas': ['Acepta cualquier opinión',
                                  'Busca el saber por el saber mismo',
                                  'Depende de la autoridad',
                                  'Se somete a la religión',
                                  'Persigue fines económicos'],
                 'correcta': 'B'},
                {'pregunta': 'La filosofía, como reflexión racional y '
                             'sistemática, se origina en:',
                 'alternativas': ['Egipto',
                                  'Grecia',
                                  'La India',
                                  'China',
                                  'Mesopotamia'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'Historia de la filosofía: edad antigua',
  'secciones': [{'titulo': '2.1 LOS PRESOCRÁTICOS',
                 'items': ['Buscaron el {arjé}: el principio u origen de '
                           'todas las cosas.',
                           '{Tales de Mileto}: el principio de todo es el '
                           '{agua}. Considerado el primer filósofo.',
                           '{Anaximandro}: el arjé es el {ápeiron}, lo '
                           'indeterminado e infinito.',
                           '{Anaxímenes}: el principio es el {aire}.',
                           '{Heráclito} de Éfeso: el arjé es el {fuego}; '
                           'todo {cambia} —«nadie se baña dos veces en el '
                           'mismo río»—. Doctrina del {devenir}.',
                           '{Parménides} de Elea: sostuvo lo contrario, que '
                           'el {ser} es inmutable y el cambio es una '
                           '{ilusión} de los sentidos.',
                           '{Demócrito} de Abdera: todo está compuesto por '
                           '{átomos}, partículas indivisibles.']},
                {'titulo': '2.2 SOFISTAS Y SÓCRATES',
                 'items': ['Los {sofistas} enseñaban {retórica} a cambio de '
                           'dinero y defendían el {relativismo}.',
                           '{Protágoras}: «el {hombre} es la medida de todas '
                           'las cosas».',
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
                           'y aceptar el destino.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El principio u origen de todas las cosas buscado '
                           'por los presocráticos se denomina {Arjé}.',
                           'Para Tales de Mileto, el principio de todas las '
                           'cosas es {El agua}.',
                           'El ápeiron, lo indeterminado e infinito, fue '
                           'propuesto por {Anaximandro}.',
                           'Para Heráclito de Éfeso, el arjé es {El fuego}.',
                           'La frase «nadie se baña dos veces en el mismo '
                           'río» corresponde a {Heráclito}.',
                           'Parménides de Elea sostuvo que el ser es '
                           '{Inmutable}.',
                           'Demócrito de Abdera afirmó que todo está '
                           'compuesto por {Átomos}.',
                           'El método socrático de dar a luz las ideas '
                           'mediante preguntas se llama {Mayéutica}.',
                           'La frase «solo sé que nada sé» se atribuye a '
                           '{Sócrates}.',
                           'La teoría de las Ideas fue formulada por '
                           '{Platón}.',
                           'Según Platón, el mundo de las Ideas eternas es '
                           'el mundo {Inteligible}.',
                           'La escuela fundada por Platón fue {La Academia}.',
                           'La escuela fundada por Aristóteles fue {El '
                           'Liceo}.',
                           'La teoría hilemórfica de Aristóteles sostiene '
                           'que todo ser se compone de {Materia y forma}.',
                           'Aristóteles es considerado el padre de la '
                           '{Lógica}.',
                           'Para Epicuro, el fin de la vida es el placer '
                           'entendido como {Ausencia de dolor y serenidad}.',
                           'El estado de serenidad e imperturbabilidad en '
                           'Epicuro se denomina {Ataraxia}.',
                           'Marco Aurelio perteneció a la escuela {Estoica}.',
                           'Los sofistas se caracterizaron por {Enseñar '
                           'retórica por dinero y defender el '
                           'relativismo}.']}],
  'cuadros': [{'titulo': '2.1 EL ARJÉ SEGÚN LOS PRESOCRÁTICOS',
               'encabezados': ['Filósofo', 'Principio (arjé)'],
               'filas': [['{Tales} de Mileto', 'El {agua}'],
                         ['{Anaximandro}', 'El {ápeiron}'],
                         ['{Anaxímenes}', 'El {aire}'],
                         ['{Heráclito}', 'El {fuego}'],
                         ['{Demócrito}', 'Los {átomos}']]}],
  'preguntas': [{'pregunta': 'El principio u origen de todas las cosas '
                             'buscado por los presocráticos se denomina:',
                 'alternativas': ['Logos',
                                  'Arjé',
                                  'Nous',
                                  'Eidos',
                                  'Ápeiron'],
                 'correcta': 'B'},
                {'pregunta': 'Para Tales de Mileto, el principio de todas '
                             'las cosas es:',
                 'alternativas': ['El fuego',
                                  'El agua',
                                  'El aire',
                                  'La tierra',
                                  'El átomo'],
                 'correcta': 'B'},
                {'pregunta': 'El ápeiron, lo indeterminado e infinito, fue '
                             'propuesto por:',
                 'alternativas': ['Tales',
                                  'Anaximandro',
                                  'Anaxímenes',
                                  'Heráclito',
                                  'Parménides'],
                 'correcta': 'B'},
                {'pregunta': 'Para Heráclito de Éfeso, el arjé es:',
                 'alternativas': ['El agua',
                                  'El fuego',
                                  'El aire',
                                  'El ápeiron',
                                  'El número'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «nadie se baña dos veces en el mismo '
                             'río» corresponde a:',
                 'alternativas': ['Parménides',
                                  'Heráclito',
                                  'Demócrito',
                                  'Protágoras',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'Parménides de Elea sostuvo que el ser es:',
                 'alternativas': ['Cambiante',
                                  'Inmutable',
                                  'Múltiple',
                                  'Divisible',
                                  'Material'],
                 'correcta': 'B'},
                {'pregunta': 'Demócrito de Abdera afirmó que todo está '
                             'compuesto por:',
                 'alternativas': ['Agua',
                                  'Átomos',
                                  'Ideas',
                                  'Fuego',
                                  'Números'],
                 'correcta': 'B'},
                {'pregunta': '«El hombre es la medida de todas las cosas» '
                             'pertenece a:',
                 'alternativas': ['Sócrates',
                                  'Protágoras',
                                  'Platón',
                                  'Gorgias',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'El método socrático de dar a luz las ideas '
                             'mediante preguntas se llama:',
                 'alternativas': ['Dialéctica',
                                  'Mayéutica',
                                  'Ironía',
                                  'Silogismo',
                                  'Inducción'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «solo sé que nada sé» se atribuye a:',
                 'alternativas': ['Platón',
                                  'Sócrates',
                                  'Protágoras',
                                  'Heráclito',
                                  'Epicuro'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de las Ideas fue formulada por:',
                 'alternativas': ['Aristóteles',
                                  'Platón',
                                  'Sócrates',
                                  'Demócrito',
                                  'Parménides'],
                 'correcta': 'B'},
                {'pregunta': 'Según Platón, el mundo de las Ideas eternas es '
                             'el mundo:',
                 'alternativas': ['Sensible',
                                  'Inteligible',
                                  'Material',
                                  'Aparente',
                                  'Corpóreo'],
                 'correcta': 'B'},
                {'pregunta': 'La escuela fundada por Platón fue:',
                 'alternativas': ['El Liceo',
                                  'La Academia',
                                  'El Jardín',
                                  'La Stoa',
                                  'El Pórtico'],
                 'correcta': 'B'},
                {'pregunta': 'La escuela fundada por Aristóteles fue:',
                 'alternativas': ['La Academia',
                                  'El Liceo',
                                  'El Jardín',
                                  'La Stoa',
                                  'La Escuela de Mileto'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría hilemórfica de Aristóteles sostiene '
                             'que todo ser se compone de:',
                 'alternativas': ['Cuerpo y alma',
                                  'Materia y forma',
                                  'Ser y no ser',
                                  'Acto y potencia únicamente',
                                  'Idea y copia'],
                 'correcta': 'B'},
                {'pregunta': 'Aristóteles es considerado el padre de la:',
                 'alternativas': ['Ética',
                                  'Lógica',
                                  'Estética',
                                  'Política',
                                  'Psicología'],
                 'correcta': 'B'},
                {'pregunta': 'Para Epicuro, el fin de la vida es el placer '
                             'entendido como:',
                 'alternativas': ['Goce sensorial ilimitado',
                                  'Ausencia de dolor y serenidad',
                                  'Acumulación de bienes',
                                  'Poder político',
                                  'Fama'],
                 'correcta': 'B'},
                {'pregunta': 'El estado de serenidad e imperturbabilidad en '
                             'Epicuro se denomina:',
                 'alternativas': ['Eudaimonía',
                                  'Ataraxia',
                                  'Areté',
                                  'Catarsis',
                                  'Nous'],
                 'correcta': 'B'},
                {'pregunta': 'Marco Aurelio perteneció a la escuela:',
                 'alternativas': ['Epicúrea',
                                  'Estoica',
                                  'Cínica',
                                  'Escéptica',
                                  'Platónica'],
                 'correcta': 'B'},
                {'pregunta': 'Los sofistas se caracterizaron por:',
                 'alternativas': ['Buscar verdades absolutas',
                                  'Enseñar retórica por dinero y defender el '
                                  'relativismo',
                                  'Rechazar la política',
                                  'Fundar la lógica formal',
                                  'Estudiar los astros'],
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
                           'para creer».']},
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
                           '{Nicolás Maquiavelo}: autor de «El {Príncipe}». '
                           'Separó la {política} de la moral; se le atribuye '
                           'la máxima «el {fin} justifica los medios».']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El pensamiento medieval se caracterizó por ser '
                           '{Teocéntrico}.',
                           'En la Edad Media la filosofía fue considerada '
                           '{Sierva de la teología}.',
                           'El problema central de la filosofía medieval fue '
                           'la relación entre {Razón y fe}.',
                           'San Agustín de Hipona estuvo influido '
                           'principalmente por {Platón}.',
                           'Una obra fundamental de San Agustín es {La '
                           'ciudad de Dios}.',
                           'La doctrina agustiniana según la cual Dios '
                           'ilumina la mente humana se llama {Iluminación}.',
                           'La etapa de los Padres de la Iglesia se denomina '
                           '{Patrística}.',
                           'Santo Tomás de Aquino estuvo influido '
                           'principalmente por {Aristóteles}.',
                           'La obra principal de Santo Tomás de Aquino es '
                           '{Suma Teológica}.',
                           'Santo Tomás formuló para demostrar la existencia '
                           'de Dios {Las cinco vías}.',
                           'Para Santo Tomás, la razón y la fe {Se '
                           'complementan}.',
                           'La escolástica se basó como método en {La '
                           'disputa y el comentario de textos}.',
                           'El Renacimiento se caracterizó por el '
                           '{Antropocentrismo}.',
                           'El autor de «El Príncipe» fue {Nicolás '
                           'Maquiavelo}.',
                           'Maquiavelo es conocido por separar la política '
                           'de {La moral}.',
                           'La máxima «el fin justifica los medios» se '
                           'atribuye a {Maquiavelo}.',
                           'El Renacimiento recuperó la cultura '
                           '{Grecolatina}.',
                           'El movimiento que valoró la dignidad y las '
                           'capacidades del ser humano se llamó {Humanismo}.',
                           'La expresión latina «ancilla theologiae» '
                           'significa que la filosofía era {Sierva de la '
                           'teología}.']}],
  'cuadros': [{'titulo': '3. DOS ETAPAS DEL PENSAMIENTO MEDIEVAL',
               'encabezados': ['Etapa', 'Representante', 'Influencia'],
               'filas': [['{Patrística}', 'San {Agustín}', '{Platón}'],
                         ['{Escolástica}',
                          'Santo Tomás de {Aquino}',
                          '{Aristóteles}']]}],
  'preguntas': [{'pregunta': 'El pensamiento medieval se caracterizó por '
                             'ser:',
                 'alternativas': ['Antropocéntrico',
                                  'Teocéntrico',
                                  'Cosmocéntrico',
                                  'Logocéntrico',
                                  'Empírico'],
                 'correcta': 'B'},
                {'pregunta': 'En la Edad Media la filosofía fue considerada:',
                 'alternativas': ['Ciencia suprema',
                                  'Sierva de la teología',
                                  'Independiente de la fe',
                                  'Sinónimo de retórica',
                                  'Un arte liberal menor'],
                 'correcta': 'B'},
                {'pregunta': 'El problema central de la filosofía medieval '
                             'fue la relación entre:',
                 'alternativas': ['Ser y pensar',
                                  'Razón y fe',
                                  'Materia y forma',
                                  'Cuerpo y alma',
                                  'Bien y mal'],
                 'correcta': 'B'},
                {'pregunta': 'San Agustín de Hipona estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Aristóteles',
                                  'Platón',
                                  'Demócrito',
                                  'Epicuro',
                                  'Los estoicos'],
                 'correcta': 'B'},
                {'pregunta': 'Una obra fundamental de San Agustín es:',
                 'alternativas': ['Suma Teológica',
                                  'La ciudad de Dios',
                                  'El Príncipe',
                                  'Órganon',
                                  'La República'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina agustiniana según la cual Dios '
                             'ilumina la mente humana se llama:',
                 'alternativas': ['Iluminación',
                                  'Revelación',
                                  'Predestinación',
                                  'Emanación',
                                  'Analogía'],
                 'correcta': 'A'},
                {'pregunta': '«Cree para comprender y comprende para creer» '
                             'corresponde a:',
                 'alternativas': ['Santo Tomás',
                                  'San Agustín',
                                  'Maquiavelo',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'La etapa de los Padres de la Iglesia se '
                             'denomina:',
                 'alternativas': ['Escolástica',
                                  'Patrística',
                                  'Humanismo',
                                  'Renacimiento',
                                  'Ilustración'],
                 'correcta': 'B'},
                {'pregunta': 'Santo Tomás de Aquino estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Platón',
                                  'Aristóteles',
                                  'Heráclito',
                                  'Epicuro',
                                  'Parménides'],
                 'correcta': 'B'},
                {'pregunta': 'La obra principal de Santo Tomás de Aquino es:',
                 'alternativas': ['Confesiones',
                                  'Suma Teológica',
                                  'La ciudad de Dios',
                                  'El Príncipe',
                                  'Metafísica'],
                 'correcta': 'B'},
                {'pregunta': 'Santo Tomás formuló para demostrar la '
                             'existencia de Dios:',
                 'alternativas': ['Tres pruebas',
                                  'Las cinco vías',
                                  'Siete argumentos',
                                  'Dos silogismos',
                                  'Cuatro causas'],
                 'correcta': 'B'},
                {'pregunta': 'Para Santo Tomás, la razón y la fe:',
                 'alternativas': ['Se contradicen',
                                  'Se complementan',
                                  'Son idénticas',
                                  'Se excluyen',
                                  'No se relacionan'],
                 'correcta': 'B'},
                {'pregunta': 'La escolástica se basó como método en:',
                 'alternativas': ['La experimentación',
                                  'La disputa y el comentario de textos',
                                  'La observación astronómica',
                                  'La introspección',
                                  'El diálogo socrático'],
                 'correcta': 'B'},
                {'pregunta': 'El Renacimiento se caracterizó por el:',
                 'alternativas': ['Teocentrismo',
                                  'Antropocentrismo',
                                  'Geocentrismo',
                                  'Escepticismo',
                                  'Dogmatismo'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «El Príncipe» fue:',
                 'alternativas': ['Erasmo',
                                  'Nicolás Maquiavelo',
                                  'Tomás Moro',
                                  'Galileo',
                                  'Descartes'],
                 'correcta': 'B'},
                {'pregunta': 'Maquiavelo es conocido por separar la política '
                             'de:',
                 'alternativas': ['La economía',
                                  'La moral',
                                  'La religión únicamente',
                                  'La historia',
                                  'El derecho'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima «el fin justifica los medios» se '
                             'atribuye a:',
                 'alternativas': ['Santo Tomás',
                                  'Maquiavelo',
                                  'San Agustín',
                                  'Platón',
                                  'Epicuro'],
                 'correcta': 'B'},
                {'pregunta': 'El Renacimiento recuperó la cultura:',
                 'alternativas': ['Egipcia',
                                  'Grecolatina',
                                  'Oriental',
                                  'Medieval',
                                  'Germánica'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento que valoró la dignidad y las '
                             'capacidades del ser humano se llamó:',
                 'alternativas': ['Escolasticismo',
                                  'Humanismo',
                                  'Estoicismo',
                                  'Escepticismo',
                                  'Positivismo'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión latina «ancilla theologiae» '
                             'significa que la filosofía era:',
                 'alternativas': ['Reina de las ciencias',
                                  'Sierva de la teología',
                                  'Madre de la lógica',
                                  'Enemiga de la fe',
                                  'Base de la política'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'La filosofía moderna y filosofía en el Perú',
  'secciones': [{'titulo': '4.1 RACIONALISMO Y EMPIRISMO',
                 'items': ['{René Descartes}, padre de la filosofía moderna, '
                           'fundó el {racionalismo}. Su método parte de la '
                           '{duda} metódica.',
                           'Su principio fundamental es «pienso, luego '
                           '{existo}» ({cogito ergo sum}).',
                           '{John Locke}: fundador del {empirismo}. La mente '
                           'al nacer es una {tabla rasa}; todo conocimiento '
                           'proviene de la {experiencia}.']},
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
                {'titulo': '4.3 MARX Y EL MATERIALISMO',
                 'items': ['{Carlos Marx}: invirtió la dialéctica de Hegel y '
                           'creó el materialismo {dialéctico} e histórico.',
                           'Sostuvo que la {infraestructura} económica '
                           'determina la {superestructura} jurídica, '
                           'política e ideológica.',
                           '«Los filósofos se han limitado a interpretar el '
                           'mundo; de lo que se trata es de '
                           '{transformarlo}».']},
                {'titulo': '4.4 FILOSOFÍA EN EL PERÚ',
                 'items': ['{José Carlos Mariátegui}: autor de «{7 ensayos} '
                           'de interpretación de la realidad peruana». '
                           'Aplicó el {marxismo} al análisis del Perú, '
                           'señalando que el problema del {indio} es un '
                           'problema de la {tierra}.',
                           '{Augusto Salazar Bondy}: autor de «¿Existe una '
                           'filosofía de nuestra {América}?». Sostuvo que '
                           'nuestra filosofía ha sido {imitativa} por ser '
                           'reflejo de una sociedad {dominada}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El padre de la filosofía moderna es {René '
                           'Descartes}.',
                           'El principio «pienso, luego existo» pertenece a '
                           '{Descartes}.',
                           'El método cartesiano parte de {La duda '
                           'metódica}.',
                           'Para el empirismo, todo conocimiento proviene de '
                           '{La experiencia}.',
                           'John Locke sostuvo que la mente al nacer es {Una '
                           'tabla rasa}.',
                           'La síntesis entre racionalismo y empirismo fue '
                           'realizada por {Kant}.',
                           'El lema «atrévete a saber» corresponde a {Kant}.',
                           'Kant llamó «noúmeno» a {La cosa en sí, '
                           'incognoscible}.',
                           'El imperativo categórico de Kant exige obrar de '
                           'modo que la acción pueda ser {Ley universal}.',
                           'Los tres momentos de la dialéctica hegeliana son '
                           '{Tesis, antítesis y síntesis}.',
                           'El sistema filosófico de Hegel es {Idealista}.',
                           'Marx invirtió la dialéctica de Hegel y '
                           'desarrolló {El materialismo dialéctico e '
                           'histórico}.',
                           'Para Marx, la infraestructura económica '
                           'determina {La superestructura jurídica, política '
                           'e ideológica}.',
                           'El autor de «7 ensayos de interpretación de la '
                           'realidad peruana» es {José Carlos Mariátegui}.',
                           'Para Mariátegui, el problema del indio es '
                           'fundamentalmente un problema {De la tierra}.',
                           'El autor de «¿Existe una filosofía de nuestra '
                           'América?» es {Augusto Salazar Bondy}.',
                           'Según Salazar Bondy, la filosofía '
                           'latinoamericana ha sido {Imitativa, reflejo de '
                           'una sociedad dominada}.',
                           'Mariátegui aplicó al análisis del Perú el método '
                           '{Marxista}.',
                           'El criticismo kantiano sostiene que el '
                           'conocimiento resulta de {La unión de razón y '
                           'experiencia}.']}],
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
                                  'René Descartes',
                                  'Kant',
                                  'Hegel',
                                  'Bacon'],
                 'correcta': 'B'},
                {'pregunta': 'El principio «pienso, luego existo» pertenece '
                             'a:',
                 'alternativas': ['Kant',
                                  'Descartes',
                                  'Locke',
                                  'Hegel',
                                  'Marx'],
                 'correcta': 'B'},
                {'pregunta': 'El método cartesiano parte de:',
                 'alternativas': ['La observación',
                                  'La duda metódica',
                                  'La revelación',
                                  'La inducción',
                                  'La experiencia sensible'],
                 'correcta': 'B'},
                {'pregunta': 'Para el empirismo, todo conocimiento proviene '
                             'de:',
                 'alternativas': ['La razón pura',
                                  'La experiencia',
                                  'Las ideas innatas',
                                  'La revelación',
                                  'La intuición'],
                 'correcta': 'B'},
                {'pregunta': 'John Locke sostuvo que la mente al nacer es:',
                 'alternativas': ['Un depósito de ideas innatas',
                                  'Una tabla rasa',
                                  'Un espejo del cosmos',
                                  'Una sustancia pensante',
                                  'Un reflejo divino'],
                 'correcta': 'B'},
                {'pregunta': 'La síntesis entre racionalismo y empirismo fue '
                             'realizada por:',
                 'alternativas': ['Hegel',
                                  'Kant',
                                  'Marx',
                                  'Descartes',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'El lema «atrévete a saber» corresponde a:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Hegel',
                                  'Marx',
                                  'Mariátegui'],
                 'correcta': 'B'},
                {'pregunta': 'Kant llamó «noúmeno» a:',
                 'alternativas': ['Lo que aparece a los sentidos',
                                  'La cosa en sí, incognoscible',
                                  'La idea innata',
                                  'El juicio sintético',
                                  'El imperativo moral'],
                 'correcta': 'B'},
                {'pregunta': 'El imperativo categórico de Kant exige obrar '
                             'de modo que la acción pueda ser:',
                 'alternativas': ['Útil para uno mismo',
                                  'Ley universal',
                                  'Aprobada socialmente',
                                  'Placentera',
                                  'Rentable'],
                 'correcta': 'B'},
                {'pregunta': 'Los tres momentos de la dialéctica hegeliana '
                             'son:',
                 'alternativas': ['Causa, efecto y fin',
                                  'Tesis, antítesis y síntesis',
                                  'Ser, no ser y devenir',
                                  'Materia, forma y acto',
                                  'Duda, método y certeza'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema filosófico de Hegel es:',
                 'alternativas': ['Materialista',
                                  'Idealista',
                                  'Empirista',
                                  'Escéptico',
                                  'Positivista'],
                 'correcta': 'B'},
                {'pregunta': 'Marx invirtió la dialéctica de Hegel y '
                             'desarrolló:',
                 'alternativas': ['El idealismo absoluto',
                                  'El materialismo dialéctico e histórico',
                                  'El criticismo',
                                  'El empirismo',
                                  'El pragmatismo'],
                 'correcta': 'B'},
                {'pregunta': 'Para Marx, la infraestructura económica '
                             'determina:',
                 'alternativas': ['La geografía',
                                  'La superestructura jurídica, política e '
                                  'ideológica',
                                  'El clima',
                                  'La biología',
                                  'El lenguaje únicamente'],
                 'correcta': 'B'},
                {'pregunta': '«Los filósofos se han limitado a interpretar '
                             'el mundo; de lo que se trata es de '
                             'transformarlo» pertenece a:',
                 'alternativas': ['Hegel',
                                  'Marx',
                                  'Kant',
                                  'Mariátegui',
                                  'Salazar Bondy'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «7 ensayos de interpretación de la '
                             'realidad peruana» es:',
                 'alternativas': ['Augusto Salazar Bondy',
                                  'José Carlos Mariátegui',
                                  'Víctor Raúl Haya de la Torre',
                                  'Francisco Miró Quesada',
                                  'González Prada'],
                 'correcta': 'B'},
                {'pregunta': 'Para Mariátegui, el problema del indio es '
                             'fundamentalmente un problema:',
                 'alternativas': ['Educativo',
                                  'De la tierra',
                                  'Racial',
                                  'Religioso',
                                  'Administrativo'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «¿Existe una filosofía de nuestra '
                             'América?» es:',
                 'alternativas': ['Mariátegui',
                                  'Augusto Salazar Bondy',
                                  'Francisco Miró Quesada',
                                  'Antenor Orrego',
                                  'Alejandro Deustua'],
                 'correcta': 'B'},
                {'pregunta': 'Según Salazar Bondy, la filosofía '
                             'latinoamericana ha sido:',
                 'alternativas': ['Original y autónoma',
                                  'Imitativa, reflejo de una sociedad '
                                  'dominada',
                                  'Puramente científica',
                                  'Inexistente',
                                  'Superior a la europea'],
                 'correcta': 'B'},
                {'pregunta': 'Mariátegui aplicó al análisis del Perú el '
                             'método:',
                 'alternativas': ['Fenomenológico',
                                  'Marxista',
                                  'Positivista',
                                  'Existencialista',
                                  'Escolástico'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo kantiano sostiene que el '
                             'conocimiento resulta de:',
                 'alternativas': ['Solo la razón',
                                  'La unión de razón y experiencia',
                                  'Solo los sentidos',
                                  'La revelación divina',
                                  'La tradición'],
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
                           '{Neodarwinismo}: complementa a Darwin con los '
                           'aportes de la {genética} y las {mutaciones}.']},
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
                           'transformador.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La disciplina filosófica que estudia al hombre '
                           'en su totalidad es {Antropología filosófica}.',
                           'La antropología filosófica se diferencia de la '
                           'cultural porque {Reflexiona sobre el ser del '
                           'hombre}.',
                           'El creacionismo sostiene que el hombre fue '
                           '{Creado por un ser superior}.',
                           'El mito griego que explica el origen del hombre '
                           'mediante un titán es el de {Prometeo}.',
                           'La teoría de la evolución por selección natural '
                           'fue formulada por {Charles Darwin}.',
                           'El neodarwinismo complementa a Darwin con los '
                           'aportes de {La genética y las mutaciones}.',
                           'Como ser natural, el hombre se caracteriza por '
                           '{Poseer un cuerpo biológico sujeto a leyes '
                           'naturales}.',
                           'Como ser espiritual, el hombre posee '
                           '{Conciencia, libertad y capacidad de crear '
                           'cultura}.',
                           'La expresión «zoon politikon», que define al '
                           'hombre como ser social, es de {Aristóteles}.',
                           'Lo que distingue al hombre del resto de '
                           'animales, según la antropología filosófica, es '
                           '{Su racionalidad y capacidad simbólica}.',
                           'La capacidad humana de transformar la naturaleza '
                           'mediante la actividad consciente es {El '
                           'trabajo}.',
                           'La tradición judeocristiana corresponde a la '
                           'teoría {Creacionista}.',
                           'El hombre es considerado un ser bidimensional '
                           'porque es a la vez {Natural y espiritual}.',
                           'El lenguaje simbólico es una característica '
                           '{Propia del ser humano}.',
                           'La antropología filosófica se pregunta '
                           'fundamentalmente por {La esencia y el sentido de '
                           'la existencia humana}.',
                           'La cultura, según la antropología filosófica, es '
                           'producto de la dimensión {Espiritual}.',
                           'La libertad humana implica fundamentalmente la '
                           'capacidad de {Elegir y responder por los propios '
                           'actos}.',
                           'Para el evolucionismo, el hombre y los primates '
                           'actuales comparten {Un antepasado común}.',
                           'Las necesidades e instintos corresponden a la '
                           'dimensión humana {Natural o biológica}.',
                           'El ser humano crea valores, normas y símbolos '
                           'porque es un ser {Cultural y espiritual}.']}],
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
                 'alternativas': ['Gnoseología',
                                  'Antropología filosófica',
                                  'Axiología',
                                  'Ontología',
                                  'Ética'],
                 'correcta': 'B'},
                {'pregunta': 'La antropología filosófica se diferencia de la '
                             'cultural porque:',
                 'alternativas': ['Describe costumbres',
                                  'Reflexiona sobre el ser del hombre',
                                  'Estudia fósiles',
                                  'Analiza idiomas',
                                  'Mide cráneos'],
                 'correcta': 'B'},
                {'pregunta': 'El creacionismo sostiene que el hombre fue:',
                 'alternativas': ['Producto del azar',
                                  'Creado por un ser superior',
                                  'Resultado de mutaciones',
                                  'Fruto de la evolución',
                                  'Autogenerado'],
                 'correcta': 'B'},
                {'pregunta': 'El mito griego que explica el origen del '
                             'hombre mediante un titán es el de:',
                 'alternativas': ['Sísifo',
                                  'Prometeo',
                                  'Ícaro',
                                  'Narciso',
                                  'Edipo'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la evolución por selección '
                             'natural fue formulada por:',
                 'alternativas': ['Lamarck',
                                  'Charles Darwin',
                                  'Mendel',
                                  'De Vries',
                                  'Wallace únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'El neodarwinismo complementa a Darwin con los '
                             'aportes de:',
                 'alternativas': ['La teología',
                                  'La genética y las mutaciones',
                                  'La astronomía',
                                  'La lingüística',
                                  'La geología'],
                 'correcta': 'B'},
                {'pregunta': 'Como ser natural, el hombre se caracteriza '
                             'por:',
                 'alternativas': ['Su capacidad simbólica',
                                  'Poseer un cuerpo biológico sujeto a leyes '
                                  'naturales',
                                  'Crear valores',
                                  'Ser libre',
                                  'Producir cultura'],
                 'correcta': 'B'},
                {'pregunta': 'Como ser espiritual, el hombre posee:',
                 'alternativas': ['Instintos',
                                  'Conciencia, libertad y capacidad de crear '
                                  'cultura',
                                  'Solo necesidades biológicas',
                                  'Reflejos condicionados',
                                  'Únicamente sensaciones'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión «zoon politikon», que define al '
                             'hombre como ser social, es de:',
                 'alternativas': ['Platón',
                                  'Aristóteles',
                                  'Sócrates',
                                  'Hobbes',
                                  'Rousseau'],
                 'correcta': 'B'},
                {'pregunta': 'Lo que distingue al hombre del resto de '
                             'animales, según la antropología filosófica, '
                             'es:',
                 'alternativas': ['Su fuerza física',
                                  'Su racionalidad y capacidad simbólica',
                                  'Su tamaño',
                                  'Su longevidad',
                                  'Su alimentación'],
                 'correcta': 'B'},
                {'pregunta': 'La capacidad humana de transformar la '
                             'naturaleza mediante la actividad consciente '
                             'es:',
                 'alternativas': ['El instinto',
                                  'El trabajo',
                                  'El reflejo',
                                  'La adaptación pasiva',
                                  'La mutación'],
                 'correcta': 'B'},
                {'pregunta': 'La tradición judeocristiana corresponde a la '
                             'teoría:',
                 'alternativas': ['Evolucionista',
                                  'Creacionista',
                                  'Neodarwinista',
                                  'Materialista',
                                  'Positivista'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre es considerado un ser bidimensional '
                             'porque es a la vez:',
                 'alternativas': ['Bueno y malo',
                                  'Natural y espiritual',
                                  'Joven y viejo',
                                  'Individual y aislado',
                                  'Racional e irracional'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje simbólico es una característica:',
                 'alternativas': ['Compartida con todos los animales',
                                  'Propia del ser humano',
                                  'Exclusiva de los primates',
                                  'Innata y no aprendida',
                                  'Puramente instintiva'],
                 'correcta': 'B'},
                {'pregunta': 'La antropología filosófica se pregunta '
                             'fundamentalmente por:',
                 'alternativas': ['Las costumbres de los pueblos',
                                  'La esencia y el sentido de la existencia '
                                  'humana',
                                  'La anatomía comparada',
                                  'La distribución geográfica',
                                  'Los restos arqueológicos'],
                 'correcta': 'B'},
                {'pregunta': 'La cultura, según la antropología filosófica, '
                             'es producto de la dimensión:',
                 'alternativas': ['Biológica',
                                  'Espiritual',
                                  'Instintiva',
                                  'Genética',
                                  'Refleja'],
                 'correcta': 'B'},
                {'pregunta': 'La libertad humana implica fundamentalmente la '
                             'capacidad de:',
                 'alternativas': ['Hacer cualquier cosa sin límites',
                                  'Elegir y responder por los propios actos',
                                  'Evitar toda norma',
                                  'Someterse al destino',
                                  'Seguir los instintos'],
                 'correcta': 'B'},
                {'pregunta': 'Para el evolucionismo, el hombre y los '
                             'primates actuales comparten:',
                 'alternativas': ['Idéntica especie',
                                  'Un antepasado común',
                                  'La misma cultura',
                                  'El mismo lenguaje',
                                  'Igual capacidad simbólica'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades e instintos corresponden a la '
                             'dimensión humana:',
                 'alternativas': ['Espiritual',
                                  'Natural o biológica',
                                  'Cultural',
                                  'Simbólica',
                                  'Axiológica'],
                 'correcta': 'B'},
                {'pregunta': 'El ser humano crea valores, normas y símbolos '
                             'porque es un ser:',
                 'alternativas': ['Puramente biológico',
                                  'Cultural y espiritual',
                                  'Instintivo',
                                  'Determinado genéticamente',
                                  'Aislado'],
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
                           'sistema.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La disciplina que estudia el conocimiento en '
                           'general se denomina {Gnoseología}.',
                           'Etimológicamente, gnoseología proviene de '
                           'gnosis, que significa {Conocimiento}.',
                           'El elemento del conocimiento que designa a quien '
                           'conoce es {El sujeto cognoscente}.',
                           'La representación mental que el sujeto elabora '
                           'del objeto se denomina {Imagen}.',
                           'En el acto de conocer, el objeto {Permanece '
                           'inalterado}.',
                           'El conocimiento obtenido a través de los '
                           'sentidos es {Sensible}.',
                           'El conocimiento sensible se caracteriza por ser '
                           '{Singular, concreto y subjetivo}.',
                           'El conocimiento racional se caracteriza por ser '
                           '{Universal, abstracto y objetivo}.',
                           'El conocimiento espontáneo, no verificado ni '
                           'sistemático es el {Vulgar}.',
                           'El conocimiento científico se caracteriza por '
                           'ser {Metódico, sistemático y verificable}.',
                           'La teoría que define la verdad como adecuación '
                           'entre el pensamiento y la realidad es la de {La '
                           'correspondencia}.',
                           'La concepción clásica de la verdad se atribuye a '
                           '{Aristóteles}.',
                           'Para la teoría pragmática, es verdadero aquello '
                           'que {Resulta útil o funciona en la práctica}.',
                           'Según la teoría de la coherencia, un enunciado '
                           'es verdadero si {No contradice al sistema del '
                           'que forma parte}.',
                           'Los tres elementos del conocimiento son sujeto, '
                           'objeto e {Imagen}.',
                           'La gnoseología estudia del conocimiento su '
                           'origen, su esencia y sus {Límites}.',
                           'Percibir el color rojo de una manzana '
                           'corresponde al conocimiento {Sensible}.',
                           'Comprender el concepto de «justicia» corresponde '
                           'al conocimiento {Racional}.',
                           'En la relación cognoscitiva, aquello que es '
                           'conocido se denomina {Objeto}.',
                           'La afirmación «la nieve es blanca es verdadera '
                           'si la nieve es blanca» ilustra la teoría de {La '
                           'correspondencia}.']}],
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
                 'alternativas': ['Ontología',
                                  'Gnoseología',
                                  'Axiología',
                                  'Ética',
                                  'Lógica'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, gnoseología proviene de '
                             'gnosis, que significa:',
                 'alternativas': ['Ser',
                                  'Conocimiento',
                                  'Valor',
                                  'Palabra',
                                  'Ley'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento del conocimiento que designa a '
                             'quien conoce es:',
                 'alternativas': ['El objeto',
                                  'El sujeto cognoscente',
                                  'La imagen',
                                  'El método',
                                  'La verdad'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental que el sujeto elabora '
                             'del objeto se denomina:',
                 'alternativas': ['Concepto puro',
                                  'Imagen',
                                  'Juicio',
                                  'Idea innata',
                                  'Símbolo'],
                 'correcta': 'B'},
                {'pregunta': 'En el acto de conocer, el objeto:',
                 'alternativas': ['Se transforma',
                                  'Permanece inalterado',
                                  'Desaparece',
                                  'Se subjetiviza',
                                  'Se destruye'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento obtenido a través de los '
                             'sentidos es:',
                 'alternativas': ['Racional',
                                  'Sensible',
                                  'Abstracto',
                                  'Universal',
                                  'Científico'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento sensible se caracteriza por '
                             'ser:',
                 'alternativas': ['Universal y abstracto',
                                  'Singular, concreto y subjetivo',
                                  'Necesario',
                                  'Apriorístico',
                                  'Deductivo'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento racional se caracteriza por '
                             'ser:',
                 'alternativas': ['Singular',
                                  'Universal, abstracto y objetivo',
                                  'Concreto',
                                  'Sensorial',
                                  'Momentáneo'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento espontáneo, no verificado ni '
                             'sistemático es el:',
                 'alternativas': ['Científico',
                                  'Vulgar',
                                  'Filosófico',
                                  'Técnico',
                                  'Teológico'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento científico se caracteriza por '
                             'ser:',
                 'alternativas': ['Espontáneo',
                                  'Metódico, sistemático y verificable',
                                  'Subjetivo',
                                  'Dogmático',
                                  'Intuitivo'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría que define la verdad como adecuación '
                             'entre el pensamiento y la realidad es la de:',
                 'alternativas': ['La coherencia',
                                  'La correspondencia',
                                  'El pragmatismo',
                                  'El consenso',
                                  'La utilidad'],
                 'correcta': 'B'},
                {'pregunta': 'La concepción clásica de la verdad se atribuye '
                             'a:',
                 'alternativas': ['Descartes',
                                  'Aristóteles',
                                  'James',
                                  'Hegel',
                                  'Kant'],
                 'correcta': 'B'},
                {'pregunta': 'Para la teoría pragmática, es verdadero '
                             'aquello que:',
                 'alternativas': ['Corresponde a la realidad',
                                  'Resulta útil o funciona en la práctica',
                                  'No se contradice',
                                  'Es evidente',
                                  'Es revelado'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría de la coherencia, un enunciado '
                             'es verdadero si:',
                 'alternativas': ['Se comprueba experimentalmente',
                                  'No contradice al sistema del que forma '
                                  'parte',
                                  'Es útil',
                                  'Lo dice una autoridad',
                                  'Es intuitivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los tres elementos del conocimiento son '
                             'sujeto, objeto e:',
                 'alternativas': ['Método',
                                  'Imagen',
                                  'Instrumento',
                                  'Interés',
                                  'Interpretación'],
                 'correcta': 'B'},
                {'pregunta': 'La gnoseología estudia del conocimiento su '
                             'origen, su esencia y sus:',
                 'alternativas': ['Aplicaciones',
                                  'Límites',
                                  'Costos',
                                  'Instrumentos',
                                  'Autores'],
                 'correcta': 'B'},
                {'pregunta': 'Percibir el color rojo de una manzana '
                             'corresponde al conocimiento:',
                 'alternativas': ['Racional',
                                  'Sensible',
                                  'Abstracto',
                                  'Deductivo',
                                  'Científico'],
                 'correcta': 'B'},
                {'pregunta': 'Comprender el concepto de «justicia» '
                             'corresponde al conocimiento:',
                 'alternativas': ['Sensible',
                                  'Racional',
                                  'Instintivo',
                                  'Perceptivo',
                                  'Empírico puro'],
                 'correcta': 'B'},
                {'pregunta': 'En la relación cognoscitiva, aquello que es '
                             'conocido se denomina:',
                 'alternativas': ['Sujeto',
                                  'Objeto',
                                  'Imagen',
                                  'Método',
                                  'Fin'],
                 'correcta': 'B'},
                {'pregunta': 'La afirmación «la nieve es blanca es verdadera '
                             'si la nieve es blanca» ilustra la teoría de:',
                 'alternativas': ['La coherencia',
                                  'La correspondencia',
                                  'El pragmatismo',
                                  'El consenso',
                                  'La autoridad'],
                 'correcta': 'B'}]},
 {'num': 7,
  'titulo': 'Corrientes del problema del conocimiento',
  'secciones': [{'titulo': '7.1 POSIBILIDAD DEL CONOCIMIENTO',
                 'items': ['{Dogmatismo}: sostiene que el conocimiento es '
                           '{posible} y seguro, sin cuestionar la capacidad '
                           'del sujeto.',
                           '{Escepticismo}: niega la posibilidad de alcanzar '
                           'un conocimiento {seguro}. Su representante '
                           'clásico es {Pirrón} de Elis.',
                           'El escepticismo {absoluto} niega toda '
                           'posibilidad de conocer; el {relativo} solo la '
                           'duda en algunos campos.',
                           '{Criticismo}: posición intermedia sostenida por '
                           '{Kant}; el conocimiento es posible pero con '
                           '{límites}.']},
                {'titulo': '7.2 ORIGEN DEL CONOCIMIENTO',
                 'items': ['{Racionalismo}: el origen del conocimiento es la '
                           '{razón}. Representante: {Descartes}.',
                           '{Empirismo}: el origen es la {experiencia}. '
                           'Representantes: {Locke} y Hume.',
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
                           '{Materialismo}: la {materia} es lo primario y la '
                           'conciencia es un producto de ella.',
                           '{Fenomenalismo}: solo conocemos los {fenómenos}, '
                           'no la cosa en sí.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La corriente que sostiene que el conocimiento es '
                           'posible y seguro, sin cuestionamientos, es el '
                           '{Dogmatismo}.',
                           'El escepticismo niega la posibilidad de alcanzar '
                           '{Un conocimiento seguro}.',
                           'El representante clásico del escepticismo es '
                           '{Pirrón de Elis}.',
                           'La posición intermedia que afirma que el '
                           'conocimiento es posible pero con límites es el '
                           '{Criticismo}.',
                           'El criticismo fue formulado por {Kant}.',
                           'Para el racionalismo, el origen del conocimiento '
                           'es {La razón}.',
                           'El principal representante del empirismo es '
                           '{John Locke}.',
                           'La frase «ser es ser percibido» pertenece a '
                           '{Berkeley}.',
                           'El idealismo subjetivo sostiene que la realidad '
                           'depende de {La conciencia del sujeto}.',
                           'El idealismo objetivo afirma que existe una '
                           'realidad ideal {Independiente del sujeto}.',
                           'Las Ideas de Platón y el Espíritu de Hegel son '
                           'ejemplos de {Idealismo objetivo}.',
                           'El materialismo sostiene que lo primario es {La '
                           'materia}.',
                           'El fenomenalismo sostiene que solo conocemos '
                           '{Los fenómenos}.',
                           'El escepticismo que niega toda posibilidad de '
                           'conocer se denomina {Absoluto}.',
                           'El problema de la POSIBILIDAD del conocimiento '
                           'se pregunta si {Si es posible conocer con '
                           'certeza}.',
                           'El problema del ORIGEN del conocimiento se '
                           'pregunta {De dónde proviene el conocimiento}.',
                           'Descartes es representante del {Racionalismo}.',
                           'El criticismo kantiano supera la oposición entre '
                           '{Racionalismo y empirismo}.',
                           'Para el materialismo, la conciencia es {Un '
                           'producto de la materia}.']}],
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
                 'alternativas': ['Escepticismo',
                                  'Dogmatismo',
                                  'Criticismo',
                                  'Relativismo',
                                  'Fenomenalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo niega la posibilidad de '
                             'alcanzar:',
                 'alternativas': ['La experiencia',
                                  'Un conocimiento seguro',
                                  'La percepción',
                                  'El lenguaje',
                                  'La razón'],
                 'correcta': 'B'},
                {'pregunta': 'El representante clásico del escepticismo es:',
                 'alternativas': ['Descartes',
                                  'Pirrón de Elis',
                                  'Kant',
                                  'Locke',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'La posición intermedia que afirma que el '
                             'conocimiento es posible pero con límites es '
                             'el:',
                 'alternativas': ['Dogmatismo',
                                  'Criticismo',
                                  'Escepticismo',
                                  'Empirismo',
                                  'Idealismo'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo fue formulado por:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Hume',
                                  'Hegel',
                                  'Pirrón'],
                 'correcta': 'B'},
                {'pregunta': 'Para el racionalismo, el origen del '
                             'conocimiento es:',
                 'alternativas': ['La experiencia',
                                  'La razón',
                                  'La revelación',
                                  'La costumbre',
                                  'La percepción'],
                 'correcta': 'B'},
                {'pregunta': 'El principal representante del empirismo es:',
                 'alternativas': ['Descartes',
                                  'John Locke',
                                  'Kant',
                                  'Hegel',
                                  'Platón'],
                 'correcta': 'B'},
                {'pregunta': '«Los conceptos sin intuiciones son vacíos, las '
                             'intuiciones sin conceptos son ciegas» '
                             'corresponde a:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Locke',
                                  'Hume',
                                  'Berkeley'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «ser es ser percibido» pertenece a:',
                 'alternativas': ['Kant',
                                  'Berkeley',
                                  'Hume',
                                  'Descartes',
                                  'Platón'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo subjetivo sostiene que la '
                             'realidad depende de:',
                 'alternativas': ['La materia',
                                  'La conciencia del sujeto',
                                  'Las leyes físicas',
                                  'La sociedad',
                                  'El lenguaje'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo objetivo afirma que existe una '
                             'realidad ideal:',
                 'alternativas': ['Creada por el sujeto',
                                  'Independiente del sujeto',
                                  'Inexistente',
                                  'Puramente material',
                                  'Sensorial'],
                 'correcta': 'B'},
                {'pregunta': 'Las Ideas de Platón y el Espíritu de Hegel son '
                             'ejemplos de:',
                 'alternativas': ['Idealismo subjetivo',
                                  'Idealismo objetivo',
                                  'Materialismo',
                                  'Empirismo',
                                  'Escepticismo'],
                 'correcta': 'B'},
                {'pregunta': 'El materialismo sostiene que lo primario es:',
                 'alternativas': ['La conciencia',
                                  'La materia',
                                  'La idea',
                                  'El espíritu',
                                  'El lenguaje'],
                 'correcta': 'B'},
                {'pregunta': 'El fenomenalismo sostiene que solo conocemos:',
                 'alternativas': ['La cosa en sí',
                                  'Los fenómenos',
                                  'Las ideas innatas',
                                  'El noúmeno',
                                  'La esencia'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo que niega toda posibilidad de '
                             'conocer se denomina:',
                 'alternativas': ['Relativo',
                                  'Absoluto',
                                  'Metódico',
                                  'Parcial',
                                  'Moderado'],
                 'correcta': 'B'},
                {'pregunta': 'El problema de la POSIBILIDAD del conocimiento '
                             'se pregunta si:',
                 'alternativas': ['De dónde proviene el conocimiento',
                                  'Si es posible conocer con certeza',
                                  'Qué es la verdad',
                                  'Cuál es la esencia del ser',
                                  'Para qué sirve el saber'],
                 'correcta': 'B'},
                {'pregunta': 'El problema del ORIGEN del conocimiento se '
                             'pregunta:',
                 'alternativas': ['Si es posible conocer',
                                  'De dónde proviene el conocimiento',
                                  'Qué es lo real',
                                  'Cuál es el fin del hombre',
                                  'Qué es el valor'],
                 'correcta': 'B'},
                {'pregunta': 'Descartes es representante del:',
                 'alternativas': ['Empirismo',
                                  'Racionalismo',
                                  'Escepticismo absoluto',
                                  'Materialismo',
                                  'Fenomenalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El criticismo kantiano supera la oposición '
                             'entre:',
                 'alternativas': ['Idealismo y materialismo',
                                  'Racionalismo y empirismo',
                                  'Dogmatismo y realismo',
                                  'Ética y lógica',
                                  'Ciencia y religión'],
                 'correcta': 'B'},
                {'pregunta': 'Para el materialismo, la conciencia es:',
                 'alternativas': ['Lo primario',
                                  'Un producto de la materia',
                                  'Independiente del cerebro',
                                  'Anterior al mundo',
                                  'Una sustancia separada'],
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
                           'objeto es {Real}.']}],
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
                 'alternativas': ['Gnoseología',
                                  'Epistemología',
                                  'Axiología',
                                  'Ontología',
                                  'Lógica'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «episteme» significa:',
                 'alternativas': ['Palabra',
                                  'Ciencia',
                                  'Valor',
                                  'Ser',
                                  'Alma'],
                 'correcta': 'B'},
                {'pregunta': 'La diferencia entre gnoseología y '
                             'epistemología es que la primera estudia:',
                 'alternativas': ['Solo la ciencia',
                                  'El conocimiento en general',
                                  'Los valores',
                                  'El lenguaje',
                                  'La conducta'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto sistemático de leyes e hipótesis '
                             'que explican un ámbito de la realidad es:',
                 'alternativas': ['Una hipótesis',
                                  'Una teoría científica',
                                  'Un axioma',
                                  'Un dato',
                                  'Una observación'],
                 'correcta': 'B'},
                {'pregunta': 'El enunciado que expresa una relación '
                             'constante y necesaria entre fenómenos es:',
                 'alternativas': ['La hipótesis',
                                  'La ley científica',
                                  'El axioma',
                                  'El postulado',
                                  'La conjetura'],
                 'correcta': 'B'},
                {'pregunta': 'La suposición provisional que debe ser '
                             'contrastada se denomina:',
                 'alternativas': ['Ley',
                                  'Hipótesis',
                                  'Teoría',
                                  'Axioma',
                                  'Corolario'],
                 'correcta': 'B'},
                {'pregunta': 'La proposición evidente que se acepta sin '
                             'demostración es:',
                 'alternativas': ['La hipótesis',
                                  'El axioma',
                                  'La ley',
                                  'La teoría',
                                  'El teorema'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo particular a lo general '
                             'es:',
                 'alternativas': ['Deductivo',
                                  'Inductivo',
                                  'Analógico',
                                  'Dialéctico',
                                  'Hermenéutico'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo general a lo particular '
                             'es:',
                 'alternativas': ['Inductivo',
                                  'Deductivo',
                                  'Analógico',
                                  'Comparativo',
                                  'Estadístico'],
                 'correcta': 'B'},
                {'pregunta': 'El método general de la ciencia moderna se '
                             'denomina:',
                 'alternativas': ['Dialéctico',
                                  'Hipotético-deductivo',
                                  'Fenomenológico',
                                  'Escolástico',
                                  'Intuitivo'],
                 'correcta': 'B'},
                {'pregunta': 'NO es una función de la ciencia:',
                 'alternativas': ['Describir',
                                  'Explicar',
                                  'Predecir',
                                  'Sistematizar',
                                  'Dogmatizar'],
                 'correcta': 'E'},
                {'pregunta': 'Mario Bunge clasificó las ciencias en formales '
                             'y:',
                 'alternativas': ['Puras',
                                  'Fácticas',
                                  'Aplicadas',
                                  'Exactas',
                                  'Humanas'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciencias formales tienen como objeto de '
                             'estudio entes:',
                 'alternativas': ['Reales',
                                  'Ideales',
                                  'Materiales',
                                  'Sociales',
                                  'Naturales'],
                 'correcta': 'B'},
                {'pregunta': 'Son ciencias formales:',
                 'alternativas': ['Física y química',
                                  'Lógica y matemática',
                                  'Biología y geología',
                                  'Historia y economía',
                                  'Psicología y sociología'],
                 'correcta': 'B'},
                {'pregunta': 'La biología pertenece a las ciencias:',
                 'alternativas': ['Formales',
                                  'Fácticas naturales',
                                  'Fácticas sociales',
                                  'Aplicadas exclusivamente',
                                  'Ideales'],
                 'correcta': 'B'},
                {'pregunta': 'La historia y la economía pertenecen a las '
                             'ciencias:',
                 'alternativas': ['Formales',
                                  'Fácticas sociales',
                                  'Fácticas naturales',
                                  'Exactas',
                                  'Puras'],
                 'correcta': 'B'},
                {'pregunta': 'El primer paso del método científico es:',
                 'alternativas': ['La conclusión',
                                  'La observación',
                                  'La experimentación',
                                  'La hipótesis',
                                  'La ley'],
                 'correcta': 'B'},
                {'pregunta': 'La contrastación de una hipótesis se realiza '
                             'mediante:',
                 'alternativas': ['La autoridad',
                                  'La experimentación',
                                  'La tradición',
                                  'La intuición',
                                  'La revelación'],
                 'correcta': 'B'},
                {'pregunta': 'Que la ciencia pueda anticipar hechos futuros '
                             'corresponde a su función:',
                 'alternativas': ['Descriptiva',
                                  'Predictiva',
                                  'Explicativa',
                                  'Normativa',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciencias fácticas se caracterizan porque '
                             'su objeto es:',
                 'alternativas': ['Ideal',
                                  'Real',
                                  'Abstracto puro',
                                  'Formal',
                                  'Simbólico'],
                 'correcta': 'B'}]},
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
                           '{Socioculturalismo}.']}],
  'cuadros': [{'titulo': '9.4 CORRIENTES ÉTICAS',
               'encabezados': ['Corriente', 'Representante', 'Fin moral'],
               'filas': [['{Eudemonismo}', '{Aristóteles}', 'La {felicidad}'],
                         ['Ética del {deber}', '{Kant}', 'Obrar por {deber}'],
                         ['{Utilitarismo}',
                          'Stuart {Mill}',
                          'Mayor felicidad del mayor {número}']]}],
  'preguntas': [{'pregunta': 'La disciplina filosófica que estudia los '
                             'valores es la:',
                 'alternativas': ['Ética',
                                  'Axiología',
                                  'Estética',
                                  'Gnoseología',
                                  'Ontología'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «axios» significa:',
                 'alternativas': ['Bien', 'Valor', 'Ley', 'Costumbre', 'Fin'],
                 'correcta': 'B'},
                {'pregunta': 'Que todo valor tenga su contravalor '
                             'corresponde a la característica de:',
                 'alternativas': ['Jerarquía',
                                  'Polaridad',
                                  'Objetividad',
                                  'Materia',
                                  'Historicidad'],
                 'correcta': 'B'},
                {'pregunta': 'Que unos valores valgan más que otros '
                             'corresponde a la característica de:',
                 'alternativas': ['Polaridad',
                                  'Jerarquía',
                                  'Subjetividad',
                                  'Relatividad',
                                  'Universalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La jerarquía de valores en sensibles, vitales, '
                             'espirituales y religiosos fue propuesta por:',
                 'alternativas': ['Kant',
                                  'Max Scheler',
                                  'Aristóteles',
                                  'Stuart Mill',
                                  'Nietzsche'],
                 'correcta': 'B'},
                {'pregunta': 'Para el subjetivismo, el valor depende de:',
                 'alternativas': ['El objeto',
                                  'El sujeto que valora',
                                  'La sociedad',
                                  'La razón pura',
                                  'Dios'],
                 'correcta': 'B'},
                {'pregunta': 'Para el objetivismo, los valores:',
                 'alternativas': ['Los crea el sujeto',
                                  'Existen independientemente del sujeto',
                                  'Varían con la moda',
                                  'Son ilusiones',
                                  'No existen'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría según la cual el valor surge de la '
                             'relación entre sujeto y objeto es el:',
                 'alternativas': ['Subjetivismo',
                                  'Relacionismo',
                                  'Objetivismo',
                                  'Nihilismo',
                                  'Formalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El socioculturalismo sostiene que los valores '
                             'son producto de:',
                 'alternativas': ['La razón individual',
                                  'La sociedad y la cultura',
                                  'La naturaleza biológica',
                                  'La revelación',
                                  'El azar'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que reflexiona '
                             'teóricamente sobre la moral es la:',
                 'alternativas': ['Moral',
                                  'Ética',
                                  'Axiología',
                                  'Política',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de normas y costumbres concretas '
                             'de una sociedad constituye la:',
                 'alternativas': ['Ética',
                                  'Moral',
                                  'Lógica',
                                  'Estética',
                                  'Ciencia'],
                 'correcta': 'B'},
                {'pregunta': 'La diferencia entre ética y moral es que la '
                             'ética es:',
                 'alternativas': ['Práctica y la moral teórica',
                                  'Teórica y la moral práctica',
                                  'Religiosa',
                                  'Legal',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'El eudemonismo, que sitúa el fin de la vida en '
                             'la felicidad, corresponde a:',
                 'alternativas': ['Kant',
                                  'Aristóteles',
                                  'Stuart Mill',
                                  'Epicuro',
                                  'Nietzsche'],
                 'correcta': 'B'},
                {'pregunta': 'La ética del deber fue formulada por:',
                 'alternativas': ['Aristóteles',
                                  'Kant',
                                  'Mill',
                                  'Bentham',
                                  'Scheler'],
                 'correcta': 'B'},
                {'pregunta': 'El utilitarismo, que busca la mayor felicidad '
                             'para el mayor número, se asocia a:',
                 'alternativas': ['Kant',
                                  'Stuart Mill',
                                  'Aristóteles',
                                  'Platón',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'NO es un valor ético fundamental:',
                 'alternativas': ['El bien',
                                  'La justicia',
                                  'La dignidad',
                                  'La solidaridad',
                                  'La rentabilidad'],
                 'correcta': 'E'},
                {'pregunta': 'El proceso por el cual el sujeto atribuye un '
                             'valor a algo se denomina:',
                 'alternativas': ['Juicio lógico',
                                  'Acto valorativo',
                                  'Inferencia',
                                  'Percepción',
                                  'Deducción'],
                 'correcta': 'B'},
                {'pregunta': 'En la jerarquía de Scheler, el valor más alto '
                             'corresponde a los valores:',
                 'alternativas': ['Sensibles',
                                  'Religiosos',
                                  'Vitales',
                                  'Económicos',
                                  'Útiles'],
                 'correcta': 'B'},
                {'pregunta': 'Para Kant, una acción es moralmente valiosa '
                             'cuando se realiza:',
                 'alternativas': ['Por interés',
                                  'Por deber',
                                  'Por costumbre',
                                  'Por placer',
                                  'Por miedo'],
                 'correcta': 'B'},
                {'pregunta': 'La afirmación «los valores cambian según la '
                             'época y la cultura» corresponde al:',
                 'alternativas': ['Objetivismo',
                                  'Socioculturalismo',
                                  'Formalismo',
                                  'Absolutismo moral',
                                  'Racionalismo'],
                 'correcta': 'B'}]},
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
                           'Tiro}.']}],
  'cuadros': [{'titulo': '10.3 FUNCIONES DEL LENGUAJE',
               'encabezados': ['Función', 'Finalidad', '¿Verdadera o falsa?'],
               'filas': [['{Informativa}',
                          'Transmitir {información}',
                          '{Sí}'],
                         ['{Expresiva}', 'Manifestar {emociones}', '{No}'],
                         ['{Directiva}', 'Provocar una {conducta}', 'No']]}],
  'preguntas': [{'pregunta': 'La lógica es la ciencia formal que estudia:',
                 'alternativas': ['La verdad de los hechos',
                                  'La validez o corrección de los '
                                  'razonamientos',
                                  'Los valores morales',
                                  'El origen del conocimiento',
                                  'El lenguaje literario'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica estudia de los razonamientos su:',
                 'alternativas': ['Contenido',
                                  'Forma',
                                  'Utilidad',
                                  'Belleza',
                                  'Origen histórico'],
                 'correcta': 'B'},
                {'pregunta': 'El fundador de la lógica es:',
                 'alternativas': ['Platón',
                                  'Aristóteles',
                                  'Boole',
                                  'Frege',
                                  'Porfirio'],
                 'correcta': 'B'},
                {'pregunta': 'La obra lógica de Aristóteles se reunió bajo '
                             'el nombre de:',
                 'alternativas': ['Metafísica',
                                  'Órganon',
                                  'Isagoge',
                                  'Principia',
                                  'República'],
                 'correcta': 'B'},
                {'pregunta': 'El «árbol» que ordena géneros y especies fue '
                             'elaborado por:',
                 'alternativas': ['Aristóteles',
                                  'Porfirio de Tiro',
                                  'Boole',
                                  'Russell',
                                  'Frege'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica moderna o simbólica se caracteriza '
                             'por emplear:',
                 'alternativas': ['Silogismos únicamente',
                                  'Símbolos matemáticos',
                                  'Lenguaje natural',
                                  'Metáforas',
                                  'Ejemplos históricos'],
                 'correcta': 'B'},
                {'pregunta': 'El filósofo peruano destacado en lógica '
                             'jurídica es:',
                 'alternativas': ['Mariátegui',
                                  'Francisco Miró Quesada Cantuarias',
                                  'Salazar Bondy',
                                  'Antenor Orrego',
                                  'Deustua'],
                 'correcta': 'B'},
                {'pregunta': 'La función del lenguaje que transmite '
                             'información y puede ser verdadera o falsa es '
                             'la:',
                 'alternativas': ['Expresiva',
                                  'Informativa',
                                  'Directiva',
                                  'Poética',
                                  'Fática'],
                 'correcta': 'B'},
                {'pregunta': 'La función del lenguaje que manifiesta '
                             'emociones es la:',
                 'alternativas': ['Informativa',
                                  'Expresiva',
                                  'Directiva',
                                  'Descriptiva',
                                  'Metalingüística'],
                 'correcta': 'B'},
                {'pregunta': '«Cierra la puerta» corresponde a la función:',
                 'alternativas': ['Informativa',
                                  'Directiva',
                                  'Expresiva',
                                  'Poética',
                                  'Descriptiva'],
                 'correcta': 'B'},
                {'pregunta': '«¡Qué hermoso atardecer!» corresponde a la '
                             'función:',
                 'alternativas': ['Informativa',
                                  'Expresiva',
                                  'Directiva',
                                  'Referencial',
                                  'Apelativa'],
                 'correcta': 'B'},
                {'pregunta': '«El Cusco está en el Perú» corresponde a la '
                             'función:',
                 'alternativas': ['Expresiva',
                                  'Informativa',
                                  'Directiva',
                                  'Emotiva',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje natural se caracteriza por ser:',
                 'alternativas': ['Unívoco',
                                  'Ambiguo y vago',
                                  'Simbólico',
                                  'Preciso',
                                  'Artificial'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje formalizado se caracteriza por '
                             'ser:',
                 'alternativas': ['Ambiguo',
                                  'Preciso y unívoco',
                                  'Emotivo',
                                  'Coloquial',
                                  'Literario'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de razones que sustentan una '
                             'conclusión constituye:',
                 'alternativas': ['Una descripción',
                                  'Una argumentación',
                                  'Una narración',
                                  'Una orden',
                                  'Una exclamación'],
                 'correcta': 'B'},
                {'pregunta': 'Las ramas principales de la lógica son la '
                             'formal clásica, la proposicional y la de:',
                 'alternativas': ['Conjuntos',
                                  'Clases',
                                  'Números',
                                  'Predicados exclusivamente',
                                  'Relaciones'],
                 'correcta': 'B'},
                {'pregunta': 'Las expresiones directivas NO pueden ser '
                             'calificadas como:',
                 'alternativas': ['Correctas o incorrectas',
                                  'Verdaderas o falsas',
                                  'Claras u oscuras',
                                  'Útiles o inútiles',
                                  'Corteses o descorteses'],
                 'correcta': 'B'},
                {'pregunta': 'En una argumentación, las razones que '
                             'sustentan se denominan:',
                 'alternativas': ['Conclusiones',
                                  'Premisas',
                                  'Falacias',
                                  'Axiomas',
                                  'Corolarios'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica se clasifica como una ciencia:',
                 'alternativas': ['Fáctica natural',
                                  'Formal',
                                  'Fáctica social',
                                  'Aplicada',
                                  'Experimental'],
                 'correcta': 'B'},
                {'pregunta': 'La «Isagoge» fue escrita por:',
                 'alternativas': ['Aristóteles',
                                  'Porfirio de Tiro',
                                  'Boecio',
                                  'Boole',
                                  'Frege'],
                 'correcta': 'B'}]},
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
                           '{Causa falsa}.']}],
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
                 'alternativas': ['Siempre es verdadero',
                                  'Parece válido pero no lo es',
                                  'Carece de premisas',
                                  'Es formalmente correcto',
                                  'No tiene conclusión'],
                 'correcta': 'B'},
                {'pregunta': 'Las falacias formales tienen un error en:',
                 'alternativas': ['El contenido',
                                  'La estructura del razonamiento',
                                  'El vocabulario',
                                  'La ortografía',
                                  'Las premisas verdaderas'],
                 'correcta': 'B'},
                {'pregunta': 'Las falacias de atinencia se cometen cuando '
                             'las premisas:',
                 'alternativas': ['Son verdaderas',
                                  'No son pertinentes para la conclusión',
                                  'Son numerosas',
                                  'Están bien formuladas',
                                  'Son evidentes'],
                 'correcta': 'B'},
                {'pregunta': '«No debemos creer en las teorías de Marx, '
                             'recuerda que fue comunista» es una falacia:',
                 'alternativas': ['Ad populum',
                                  'Ad hominem',
                                  'Ad báculum',
                                  'Ad ignorantiam',
                                  'De equívoco'],
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
                 'alternativas': ['Ad populum',
                                  'Ad báculum',
                                  'Ad hominem',
                                  'De énfasis',
                                  'Ignoratio elenchi'],
                 'correcta': 'B'},
                {'pregunta': '«Este jabón es bueno, lo usa un cantante '
                             'famoso» es una falacia:',
                 'alternativas': ['Ad populum',
                                  'Ad verecundiam',
                                  'Ad báculum',
                                  'Causa falsa',
                                  'Anfibología'],
                 'correcta': 'B'},
                {'pregunta': '«Tome esta bebida, lo nuestro está primero» es '
                             'una falacia:',
                 'alternativas': ['Ad hominem',
                                  'Ad populum',
                                  'Ad báculum',
                                  'Ad ignorantiam',
                                  'De equívoco'],
                 'correcta': 'B'},
                {'pregunta': '«Me levanté con el pie izquierdo, hoy será un '
                             'mal día» es una falacia de:',
                 'alternativas': ['Ambigüedad',
                                  'Causa falsa',
                                  'Autoridad',
                                  'Fuerza',
                                  'Ignorancia'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando un razonamiento prueba una conclusión '
                             'distinta de la que pretendía, se comete:',
                 'alternativas': ['Ad hominem',
                                  'Ignoratio elenchi',
                                  'Ad báculum',
                                  'Equívoco',
                                  'Énfasis'],
                 'correcta': 'B'},
                {'pregunta': 'La falacia ad hominem del tipo ofensivo '
                             'consiste en:',
                 'alternativas': ['Apelar a la fuerza',
                                  'Atacar a quien hace la afirmación',
                                  'Citar una autoridad',
                                  'Usar palabras ambiguas',
                                  'Apelar al pueblo'],
                 'correcta': 'B'},
                {'pregunta': 'La falacia que aprovecha las circunstancias '
                             'personales del adversario es la ad hominem:',
                 'alternativas': ['Ofensiva',
                                  'Circunstancial',
                                  'Directa',
                                  'Formal',
                                  'Emotiva'],
                 'correcta': 'B'},
                {'pregunta': 'Las falacias de ambigüedad se producen cuando '
                             'el razonamiento contiene:',
                 'alternativas': ['Muchas premisas',
                                  'Palabras o frases ambiguas',
                                  'Conclusiones falsas',
                                  'Datos numéricos',
                                  'Citas de autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'Usar la palabra «banco» con dos significados '
                             'distintos en un mismo razonamiento es una '
                             'falacia de:',
                 'alternativas': ['Anfibología',
                                  'Equívoco',
                                  'Énfasis',
                                  'Causa falsa',
                                  'Autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando la ambigüedad proviene de la '
                             'construcción gramatical se comete:',
                 'alternativas': ['Equívoco',
                                  'Anfibología',
                                  'Énfasis',
                                  'Ad populum',
                                  'Ad báculum'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el significado cambia según la palabra '
                             'acentuada se comete la falacia de:',
                 'alternativas': ['Equívoco',
                                  'Énfasis',
                                  'Anfibología',
                                  'Causa falsa',
                                  'Ignoratio elenchi'],
                 'correcta': 'B'},
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
                                  'Ad báculum',
                                  'Ad hominem',
                                  'Ad ignorantiam',
                                  'De énfasis'],
                 'correcta': 'B'},
                {'pregunta': 'La falacia ad verecundiam se comete al apelar '
                             'a una autoridad:',
                 'alternativas': ['Reconocida en su campo',
                                  'Fuera de su ámbito de especialidad',
                                  'Científica',
                                  'Legítima',
                                  'Académica'],
                 'correcta': 'B'},
                {'pregunta': 'Confundir la simple sucesión temporal con una '
                             'relación causal corresponde a la falacia de:',
                 'alternativas': ['Equívoco',
                                  'Causa falsa',
                                  'Ad populum',
                                  'Anfibología',
                                  'Ad báculum'],
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
                           'El símbolo ~ representa la {Negación}.']}],
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
                 'alternativas': ['Bello o feo',
                                  'Verdadero o falso',
                                  'Útil o inútil',
                                  'Justo o injusto',
                                  'Claro u oscuro'],
                 'correcta': 'B'},
                {'pregunta': 'NO es una proposición:',
                 'alternativas': ['El Cusco está en el Perú',
                                  '¿Qué hora es?',
                                  'Dos más dos es cuatro',
                                  'La nieve es blanca',
                                  'Lima es la capital'],
                 'correcta': 'B'},
                {'pregunta': 'La proposición que no contiene ningún operador '
                             'lógico se denomina:',
                 'alternativas': ['Molecular',
                                  'Simple o atómica',
                                  'Compuesta',
                                  'Condicional',
                                  'Bicondicional'],
                 'correcta': 'B'},
                {'pregunta': 'La proposición que contiene uno o más '
                             'operadores se denomina:',
                 'alternativas': ['Atómica',
                                  'Compuesta o molecular',
                                  'Simple',
                                  'Variable',
                                  'Constante'],
                 'correcta': 'B'},
                {'pregunta': 'Las variables proposicionales se representan '
                             'con:',
                 'alternativas': ['Números',
                                  'Letras minúsculas p, q, r, s',
                                  'Letras griegas',
                                  'Símbolos matemáticos',
                                  'Palabras'],
                 'correcta': 'B'},
                {'pregunta': 'El único conector monádico de la lógica '
                             'proposicional es:',
                 'alternativas': ['La conjunción',
                                  'La negación',
                                  'La disyunción',
                                  'La condicional',
                                  'La bicondicional'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∧ corresponde a la:',
                 'alternativas': ['Negación',
                                  'Conjunción',
                                  'Disyunción',
                                  'Condicional',
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
                 'alternativas': ['Y',
                                  'Si y solo si',
                                  'O',
                                  'Si... entonces',
                                  'No'],
                 'correcta': 'B'},
                {'pregunta': 'La disyunción débil se lee como:',
                 'alternativas': ['Y',
                                  'O (inclusivo)',
                                  'Si... entonces',
                                  'No',
                                  'Si y solo si'],
                 'correcta': 'B'},
                {'pregunta': 'Los paréntesis, corchetes y llaves son '
                             'símbolos:',
                 'alternativas': ['Variables',
                                  'Auxiliares',
                                  'Monádicos',
                                  'Diádicos',
                                  'Constantes'],
                 'correcta': 'B'},
                {'pregunta': '«El zorrino no es mamífero» se formaliza como:',
                 'alternativas': ['p', '~p', 'p ∧ q', 'p → q', 'p ∨ q'],
                 'correcta': 'B'},
                {'pregunta': '«La vaca es mamífero y el caballo también» se '
                             'formaliza como:',
                 'alternativas': ['p ∨ q', 'p ∧ q', 'p → q', '~p', 'p ↔ q'],
                 'correcta': 'B'},
                {'pregunta': '«El asno es mamífero pero el loro no» se '
                             'formaliza como:',
                 'alternativas': ['p ∧ q',
                                  'p ∧ ~q',
                                  'p ∨ q',
                                  '~p ∧ q',
                                  'p → ~q'],
                 'correcta': 'B'},
                {'pregunta': 'Una fórmula atómica se representa con:',
                 'alternativas': ['Dos variables',
                                  'Una sola variable',
                                  'Tres operadores',
                                  'Un conector',
                                  'Paréntesis'],
                 'correcta': 'B'},
                {'pregunta': '«Si llueve entonces me quedo» se formaliza '
                             'como:',
                 'alternativas': ['p ∧ q', 'p → q', 'p ∨ q', 'p ↔ q', '~p'],
                 'correcta': 'B'},
                {'pregunta': 'Los conectores que unen dos variables se '
                             'denominan:',
                 'alternativas': ['Monádicos',
                                  'Diádicos o binarios',
                                  'Auxiliares',
                                  'Variables',
                                  'Atómicos'],
                 'correcta': 'B'},
                {'pregunta': '«Estudio si y solo si tengo tiempo» se '
                             'formaliza como:',
                 'alternativas': ['p → q', 'p ↔ q', 'p ∧ q', 'p ∨ q', '~p'],
                 'correcta': 'B'},
                {'pregunta': 'Las órdenes y las exclamaciones NO son '
                             'proposiciones porque:',
                 'alternativas': ['Son muy breves',
                                  'No pueden ser verdaderas ni falsas',
                                  'Carecen de sujeto',
                                  'No usan verbos',
                                  'Son emotivas siempre'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ~ representa la:',
                 'alternativas': ['Conjunción',
                                  'Negación',
                                  'Disyunción',
                                  'Implicación',
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
                           '{DCC}.']}],
  'cuadros': [{'titulo': '13.2 ESQUEMAS SEGÚN SU RESULTADO',
               'encabezados': ['Esquema', 'Resultado'],
               'filas': [['{Tautología}', '{Verdadera} en todos los casos'],
                         ['{Contradicción}', '{Falsa} en todos los casos'],
                         ['{Contingencia}',
                          'Verdadera en {algunos} casos']]}],
  'preguntas': [{'pregunta': 'El diagrama que muestra todos los valores '
                             'posibles de una fórmula se denomina:',
                 'alternativas': ['Diagrama de Venn',
                                  'Tabla de verdad',
                                  'Árbol de Porfirio',
                                  'Silogismo',
                                  'Cuadro de oposición'],
                 'correcta': 'B'},
                {'pregunta': 'El número de combinaciones de una tabla de '
                             'verdad se calcula con:',
                 'alternativas': ['n²', '2ⁿ', 'n!', '2n', 'n+2'],
                 'correcta': 'B'},
                {'pregunta': 'Una fórmula con 3 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['6', '8', '9', '3', '12'],
                 'correcta': 'B'},
                {'pregunta': 'Una fórmula con 2 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['2', '4', '6', '8', '3'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula que resulta verdadera en todos los '
                             'casos es una:',
                 'alternativas': ['Contradicción',
                                  'Tautología',
                                  'Contingencia',
                                  'Consistencia',
                                  'Antinomia'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula que resulta falsa en todos los '
                             'casos es una:',
                 'alternativas': ['Tautología',
                                  'Contradicción',
                                  'Contingencia',
                                  'Equivalencia',
                                  'Implicación'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula verdadera en algunos casos y falsa '
                             'en otros es una:',
                 'alternativas': ['Tautología',
                                  'Contingencia',
                                  'Contradicción',
                                  'Identidad',
                                  'Negación'],
                 'correcta': 'B'},
                {'pregunta': 'El Modus Ponendo Ponens concluye q a partir '
                             'de:',
                 'alternativas': ['p → q y ~q',
                                  'p → q y p',
                                  'p ∨ q y ~p',
                                  'p → q y q → r',
                                  '~(p ∧ q)'],
                 'correcta': 'B'},
                {'pregunta': 'El Modus Tollendo Tollens concluye ~p a partir '
                             'de:',
                 'alternativas': ['p → q y p',
                                  'p → q y ~q',
                                  'p ∨ q y ~p',
                                  'q → r',
                                  'p ∧ q'],
                 'correcta': 'B'},
                {'pregunta': 'El Silogismo Disyuntivo concluye q a partir '
                             'de:',
                 'alternativas': ['p → q y p',
                                  'p ∨ q y ~p',
                                  'p → q y ~q',
                                  'p ∧ q',
                                  'p ↔ q'],
                 'correcta': 'B'},
                {'pregunta': 'El Silogismo Hipotético Puro concluye p → r a '
                             'partir de:',
                 'alternativas': ['p → q y p',
                                  'p → q y q → r',
                                  'p ∨ q',
                                  '~p ∧ q',
                                  'p ↔ q'],
                 'correcta': 'B'},
                {'pregunta': 'La ley que transforma la negación de una '
                             'conjunción en disyunción de negaciones es la '
                             'de:',
                 'alternativas': ['Transitividad',
                                  'De Morgan',
                                  'Identidad',
                                  'Contradicción',
                                  'Tercio excluido'],
                 'correcta': 'B'},
                {'pregunta': 'Si «si estudio apruebo» y «estudio», entonces '
                             '«apruebo». Este razonamiento es un:',
                 'alternativas': ['MTT', 'MPP', 'SD', 'SHP', 'De Morgan'],
                 'correcta': 'B'},
                {'pregunta': 'Si «si llueve me mojo» y «no me mojé», '
                             'entonces «no llovió». Este razonamiento es un:',
                 'alternativas': ['MPP', 'MTT', 'SD', 'SHP', 'DCC'],
                 'correcta': 'B'},
                {'pregunta': 'En una tabla de verdad, el brazo derecho de la '
                             'cruz se denomina:',
                 'alternativas': ['Margen',
                                  'Cuerpo',
                                  'Base',
                                  'Eje',
                                  'Columna'],
                 'correcta': 'B'},
                {'pregunta': 'En una tabla de verdad, el brazo izquierdo se '
                             'denomina:',
                 'alternativas': ['Cuerpo',
                                  'Margen',
                                  'Cabecera',
                                  'Pie',
                                  'Fila'],
                 'correcta': 'B'},
                {'pregunta': 'Una fórmula con 4 variables tendrá un número '
                             'de combinaciones igual a:',
                 'alternativas': ['8', '16', '12', '4', '32'],
                 'correcta': 'B'},
                {'pregunta': 'La tautología se representa habitualmente con '
                             'la letra:',
                 'alternativas': ['C', 'T', 'V', 'F', 'A'],
                 'correcta': 'B'},
                {'pregunta': 'Si «o voy al cine o voy al teatro» y «no voy '
                             'al cine», concluyo «voy al teatro». Es un:',
                 'alternativas': ['MPP',
                                  'Silogismo disyuntivo',
                                  'MTT',
                                  'SHP',
                                  'Dilema'],
                 'correcta': 'B'},
                {'pregunta': 'El dilema constructivo compuesto se abrevia '
                             'como:',
                 'alternativas': ['MPP', 'DCC', 'MTT', 'SD', 'SHP'],
                 'correcta': 'B'}]},
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
                           'casos es el {Analógico}.']}],
  'cuadros': [{'titulo': '14.3 JUICIOS CATEGÓRICOS TÍPICOS',
               'encabezados': ['Tipo', 'Cantidad', 'Cualidad'],
               'filas': [['{A}', '{Universal}', '{Afirmativo}'],
                         ['{E}', 'Universal', '{Negativo}'],
                         ['{I}', '{Particular}', 'Afirmativo'],
                         ['{O}', 'Particular', '{Negativo}']]}],
  'preguntas': [{'pregunta': 'El principio según el cual toda cosa es '
                             'idéntica a sí misma es el de:',
                 'alternativas': ['No contradicción',
                                  'Identidad',
                                  'Tercio excluido',
                                  'Razón suficiente',
                                  'Causalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que niega que una proposición sea '
                             'verdadera y falsa a la vez es el de:',
                 'alternativas': ['Identidad',
                                  'No contradicción',
                                  'Tercio excluido',
                                  'Razón suficiente',
                                  'Analogía'],
                 'correcta': 'B'},
                {'pregunta': 'El principio que afirma que entre dos '
                             'contradictorias no hay una tercera posibilidad '
                             'es el de:',
                 'alternativas': ['Identidad',
                                  'Tercio excluido',
                                  'No contradicción',
                                  'Causalidad',
                                  'Suficiencia'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental de un objeto es el:',
                 'alternativas': ['Juicio',
                                  'Concepto',
                                  'Razonamiento',
                                  'Silogismo',
                                  'Término'],
                 'correcta': 'B'},
                {'pregunta': 'El número de objetos a los que se aplica un '
                             'concepto es su:',
                 'alternativas': ['Comprensión',
                                  'Extensión',
                                  'Cualidad',
                                  'Cantidad',
                                  'Esencia'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de notas o características de un '
                             'concepto es su:',
                 'alternativas': ['Extensión',
                                  'Comprensión',
                                  'Cantidad',
                                  'Cualidad',
                                  'Relación'],
                 'correcta': 'B'},
                {'pregunta': 'Extensión y comprensión son entre sí:',
                 'alternativas': ['Directamente proporcionales',
                                  'Inversamente proporcionales',
                                  'Independientes',
                                  'Idénticas',
                                  'Equivalentes'],
                 'correcta': 'B'},
                {'pregunta': 'La operación mental que afirma o niega algo de '
                             'algo es el:',
                 'alternativas': ['Concepto',
                                  'Juicio',
                                  'Razonamiento',
                                  'Término',
                                  'Silogismo'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión verbal del juicio es la:',
                 'alternativas': ['Palabra',
                                  'Proposición',
                                  'Oración interrogativa',
                                  'Frase',
                                  'Interjección'],
                 'correcta': 'B'},
                {'pregunta': 'Los juicios se dividen por su cantidad en '
                             'universales y:',
                 'alternativas': ['Afirmativos',
                                  'Particulares',
                                  'Negativos',
                                  'Hipotéticos',
                                  'Categóricos'],
                 'correcta': 'B'},
                {'pregunta': 'Los juicios se dividen por su cualidad en '
                             'afirmativos y:',
                 'alternativas': ['Universales',
                                  'Negativos',
                                  'Particulares',
                                  'Simples',
                                  'Compuestos'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo A es:',
                 'alternativas': ['Universal negativo',
                                  'Universal afirmativo',
                                  'Particular afirmativo',
                                  'Particular negativo',
                                  'Singular'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo E es:',
                 'alternativas': ['Universal afirmativo',
                                  'Universal negativo',
                                  'Particular afirmativo',
                                  'Particular negativo',
                                  'Indefinido'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo I es:',
                 'alternativas': ['Universal afirmativo',
                                  'Particular afirmativo',
                                  'Universal negativo',
                                  'Particular negativo',
                                  'Singular'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo O es:',
                 'alternativas': ['Universal negativo',
                                  'Particular negativo',
                                  'Particular afirmativo',
                                  'Universal afirmativo',
                                  'Hipotético'],
                 'correcta': 'B'},
                {'pregunta': '«Todos los hombres son mortales» es un juicio '
                             'de tipo:',
                 'alternativas': ['E', 'A', 'I', 'O', 'U'],
                 'correcta': 'B'},
                {'pregunta': '«Ningún metal es líquido» es un juicio de '
                             'tipo:',
                 'alternativas': ['A', 'E', 'I', 'O', 'U'],
                 'correcta': 'B'},
                {'pregunta': 'El razonamiento que va de lo general a lo '
                             'particular es:',
                 'alternativas': ['Inductivo',
                                  'Deductivo',
                                  'Analógico',
                                  'Abductivo',
                                  'Dialéctico'],
                 'correcta': 'B'},
                {'pregunta': 'El razonamiento cuya conclusión es solo '
                             'probable es el:',
                 'alternativas': ['Deductivo',
                                  'Inductivo',
                                  'Silogístico',
                                  'Apodíctico',
                                  'Formal'],
                 'correcta': 'B'},
                {'pregunta': 'El razonamiento que concluye por semejanza '
                             'entre casos es el:',
                 'alternativas': ['Deductivo',
                                  'Analógico',
                                  'Inductivo completo',
                                  'Silogístico',
                                  'Hipotético'],
                 'correcta': 'B'}]},
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
                           'oposición es de {Contrariedad}.']}],
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
                                  'Inmediata',
                                  'Silogística',
                                  'Deductiva compuesta',
                                  'Analógica'],
                 'correcta': 'B'},
                {'pregunta': 'La inferencia en que se intercambian sujeto y '
                             'predicado se denomina:',
                 'alternativas': ['Obversión',
                                  'Conversión',
                                  'Contraposición',
                                  'Subalternación',
                                  'Oposición'],
                 'correcta': 'B'},
                {'pregunta': 'La inferencia en que se cambia la cualidad y '
                             'se niega el predicado es la:',
                 'alternativas': ['Conversión',
                                  'Obversión',
                                  'Contrapuesta total',
                                  'Subalternación',
                                  'Contrariedad'],
                 'correcta': 'B'},
                {'pregunta': '«Todo S es P» obvertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Ningún S es no-P',
                                  'Algún S es P',
                                  'Ningún P es S',
                                  'Algún S no es P'],
                 'correcta': 'B'},
                {'pregunta': 'El cuadro de oposición relaciona los juicios:',
                 'alternativas': ['Simples y compuestos',
                                  'A, E, I, O',
                                  'Verdaderos y falsos',
                                  'Deductivos e inductivos',
                                  'Mayor y menor'],
                 'correcta': 'B'},
                {'pregunta': 'La inferencia que parte de dos o más premisas '
                             'se denomina:',
                 'alternativas': ['Inmediata',
                                  'Mediata',
                                  'Directa',
                                  'Simple',
                                  'Unilateral'],
                 'correcta': 'B'},
                {'pregunta': 'La forma típica de la inferencia mediata es '
                             'el:',
                 'alternativas': ['Dilema',
                                  'Silogismo',
                                  'Entimema',
                                  'Sorites',
                                  'Epiquerema'],
                 'correcta': 'B'},
                {'pregunta': 'El silogismo categórico consta de:',
                 'alternativas': ['Dos proposiciones',
                                  'Tres proposiciones',
                                  'Cuatro proposiciones',
                                  'Una proposición',
                                  'Cinco proposiciones'],
                 'correcta': 'B'},
                {'pregunta': 'El término que aparece en ambas premisas pero '
                             'no en la conclusión es el:',
                 'alternativas': ['Mayor',
                                  'Medio',
                                  'Menor',
                                  'Sujeto',
                                  'Predicado'],
                 'correcta': 'B'},
                {'pregunta': 'El término mayor del silogismo es el:',
                 'alternativas': ['Sujeto de la conclusión',
                                  'Predicado de la conclusión',
                                  'Término medio',
                                  'Que aparece dos veces',
                                  'Que se omite'],
                 'correcta': 'B'},
                {'pregunta': 'El término menor del silogismo es el:',
                 'alternativas': ['Predicado de la conclusión',
                                  'Sujeto de la conclusión',
                                  'Término medio',
                                  'Que no aparece',
                                  'Universal'],
                 'correcta': 'B'},
                {'pregunta': 'De dos premisas negativas:',
                 'alternativas': ['Se sigue una conclusión negativa',
                                  'No se sigue conclusión alguna',
                                  'Se sigue una conclusión afirmativa',
                                  'Se sigue siempre una universal',
                                  'Se sigue una particular'],
                 'correcta': 'B'},
                {'pregunta': 'De dos premisas particulares:',
                 'alternativas': ['Se sigue una conclusión particular',
                                  'No se sigue conclusión alguna',
                                  'Se sigue una universal',
                                  'Se sigue una negativa',
                                  'Se sigue una afirmativa'],
                 'correcta': 'B'},
                {'pregunta': 'El término medio debe estar distribuido:',
                 'alternativas': ['Nunca',
                                  'Al menos una vez',
                                  'Siempre dos veces',
                                  'Solo en la conclusión',
                                  'En el predicado'],
                 'correcta': 'B'},
                {'pregunta': 'Las figuras del silogismo se determinan por la '
                             'posición del:',
                 'alternativas': ['Término mayor',
                                  'Término medio',
                                  'Término menor',
                                  'Sujeto',
                                  'Predicado'],
                 'correcta': 'B'},
                {'pregunta': 'El número de figuras del silogismo es:',
                 'alternativas': ['Dos', 'Cuatro', 'Tres', 'Seis', 'Ocho'],
                 'correcta': 'B'},
                {'pregunta': '«Ningún S es P» convertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Ningún P es S',
                                  'Algún P es S',
                                  'Algún S no es P',
                                  'Todo S es no-P'],
                 'correcta': 'B'},
                {'pregunta': 'La contrapuesta total se obtiene:',
                 'alternativas': ['Cambiando solo la cualidad',
                                  'Negando ambos términos e '
                                  'intercambiándolos',
                                  'Solo convirtiendo',
                                  'Solo obvirtiendo',
                                  'Negando la conclusión'],
                 'correcta': 'B'},
                {'pregunta': 'La relación entre A y O en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Contrariedad',
                                  'Contradicción',
                                  'Subcontrariedad',
                                  'Subalternación',
                                  'Equivalencia'],
                 'correcta': 'B'},
                {'pregunta': 'La relación entre A y E en el cuadro de '
                             'oposición es de:',
                 'alternativas': ['Contradicción',
                                  'Contrariedad',
                                  'Subcontrariedad',
                                  'Subalternación',
                                  'Identidad'],
                 'correcta': 'B'}]},
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
                           '{Producto}.']}],
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
                                  'George Boole',
                                  'Russell',
                                  'Aristóteles',
                                  'Venn'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de todos los objetos que poseen '
                             'una característica común es una:',
                 'alternativas': ['Proposición',
                                  'Clase',
                                  'Inferencia',
                                  'Premisa',
                                  'Variable'],
                 'correcta': 'B'},
                {'pregunta': 'La clase que contiene todos los elementos del '
                             'universo del discurso es la clase:',
                 'alternativas': ['Vacía',
                                  'Universal',
                                  'Particular',
                                  'Complementaria',
                                  'Nula'],
                 'correcta': 'B'},
                {'pregunta': 'La clase universal se representa con el '
                             'símbolo:',
                 'alternativas': ['0', '1', '∪', '∩', 'Ā'],
                 'correcta': 'B'},
                {'pregunta': 'La clase que no contiene ningún elemento se '
                             'denomina:',
                 'alternativas': ['Universal',
                                  'Vacía o nula',
                                  'Particular',
                                  'Complementaria',
                                  'Unitaria'],
                 'correcta': 'B'},
                {'pregunta': 'La clase vacía se representa con el símbolo:',
                 'alternativas': ['1', '0', '∅ únicamente', 'Ā', '∪'],
                 'correcta': 'B'},
                {'pregunta': 'El complemento de una clase A está formado por '
                             'los elementos que:',
                 'alternativas': ['Pertenecen a A',
                                  'No pertenecen a A',
                                  'Pertenecen a A y B',
                                  'Son comunes',
                                  'Son universales'],
                 'correcta': 'B'},
                {'pregunta': 'El complemento de la clase A se simboliza:',
                 'alternativas': ['A∪B', 'Ā', 'A∩B', 'A-B', '1'],
                 'correcta': 'B'},
                {'pregunta': 'La relación en que todos los elementos de una '
                             'clase están contenidos en otra es:',
                 'alternativas': ['Exclusión',
                                  'Inclusión',
                                  'Igualdad',
                                  'Diferencia',
                                  'Complemento'],
                 'correcta': 'B'},
                {'pregunta': 'La relación en que dos clases tienen '
                             'exactamente los mismos elementos es:',
                 'alternativas': ['Inclusión',
                                  'Igualdad',
                                  'Exclusión',
                                  'Intersección',
                                  'Unión'],
                 'correcta': 'B'},
                {'pregunta': 'La relación en que dos clases no tienen ningún '
                             'elemento en común es:',
                 'alternativas': ['Inclusión',
                                  'Exclusión',
                                  'Igualdad',
                                  'Unión',
                                  'Complemento'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que reúne los elementos de ambas '
                             'clases es la:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Diferencia',
                                  'Complementación',
                                  'Inclusión'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que reúne solo los elementos '
                             'comunes es la:',
                 'alternativas': ['Unión',
                                  'Intersección',
                                  'Diferencia',
                                  'Suma',
                                  'Complemento'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∪ representa la:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Diferencia',
                                  'Inclusión',
                                  'Exclusión'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo ∩ representa la:',
                 'alternativas': ['Unión',
                                  'Intersección',
                                  'Diferencia',
                                  'Complemento',
                                  'Igualdad'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que toma los elementos de una '
                             'clase que no están en la otra es la:',
                 'alternativas': ['Unión',
                                  'Diferencia',
                                  'Intersección',
                                  'Inclusión',
                                  'Igualdad'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica de clases se ocupa de las relaciones '
                             'entre:',
                 'alternativas': ['Proposiciones',
                                  'Clases o conjuntos',
                                  'Silogismos',
                                  'Falacias',
                                  'Valores'],
                 'correcta': 'B'},
                {'pregunta': '«Los peruanos» y «los no peruanos» son entre '
                             'sí:',
                 'alternativas': ['Clases iguales',
                                  'Clases complementarias',
                                  'Clases incluidas',
                                  'Clases idénticas',
                                  'Una sola clase'],
                 'correcta': 'B'},
                {'pregunta': 'La unión también recibe el nombre de:',
                 'alternativas': ['Producto',
                                  'Suma',
                                  'Resta',
                                  'Cociente',
                                  'Potencia'],
                 'correcta': 'B'},
                {'pregunta': 'La intersección también recibe el nombre de:',
                 'alternativas': ['Suma',
                                  'Producto',
                                  'Diferencia',
                                  'Complemento',
                                  'Unión'],
                 'correcta': 'B'}]},
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
                           'constituye {Un error de método}.']}],
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
                                  'Euler únicamente',
                                  'Frege',
                                  'Russell'],
                 'correcta': 'B'},
                {'pregunta': 'En un diagrama de Venn, el sombreado indica '
                             'que la región:',
                 'alternativas': ['Tiene elementos',
                                  'Está vacía',
                                  'Es universal',
                                  'Es dudosa',
                                  'Es infinita'],
                 'correcta': 'B'},
                {'pregunta': 'En un diagrama de Venn, la X indica que la '
                             'región:',
                 'alternativas': ['Está vacía',
                                  'Tiene al menos un elemento',
                                  'Es complementaria',
                                  'Se excluye',
                                  'Es universal'],
                 'correcta': 'B'},
                {'pregunta': '«Ningún S es P» se representa sombreando:',
                 'alternativas': ['Todo el círculo S',
                                  'La región común a S y P',
                                  'La región fuera de ambos',
                                  'El círculo P',
                                  'Nada'],
                 'correcta': 'B'},
                {'pregunta': '«Algún S es P» se representa colocando una X '
                             'en:',
                 'alternativas': ['La parte de S fuera de P',
                                  'La región común a S y P',
                                  'El círculo P completo',
                                  'Fuera de ambos círculos',
                                  'El universo'],
                 'correcta': 'B'},
                {'pregunta': '«Todo S es P» se representa sombreando:',
                 'alternativas': ['La región común',
                                  'La parte de S que no es P',
                                  'Todo el círculo P',
                                  'Fuera de ambos',
                                  'El universo'],
                 'correcta': 'B'},
                {'pregunta': '«Algún S no es P» se representa con una X en:',
                 'alternativas': ['La región común',
                                  'La parte de S fuera de P',
                                  'El círculo P',
                                  'Fuera de ambos',
                                  'El centro'],
                 'correcta': 'B'},
                {'pregunta': 'Con dos clases, el número de regiones que se '
                             'generan es:',
                 'alternativas': ['2', '4', '3', '6', '8'],
                 'correcta': 'B'},
                {'pregunta': 'Las proposiciones típicas son las que '
                             'corresponden a las formas:',
                 'alternativas': ['Simples y compuestas',
                                  'A, E, I, O',
                                  'Verdaderas y falsas',
                                  'Universales solamente',
                                  'Deductivas'],
                 'correcta': 'B'},
                {'pregunta': 'Las proposiciones atípicas requieren ser:',
                 'alternativas': ['Rechazadas',
                                  'Traducidas a una forma típica',
                                  'Negadas',
                                  'Convertidas en falacias',
                                  'Ignoradas'],
                 'correcta': 'B'},
                {'pregunta': 'Expresiones como «solo» y «únicamente» suelen '
                             'equivaler a juicios:',
                 'alternativas': ['Particulares',
                                  'Universales',
                                  'Negativos siempre',
                                  'Indefinidos',
                                  'Singulares'],
                 'correcta': 'B'},
                {'pregunta': 'Para evaluar la validez de un silogismo se '
                             'usan:',
                 'alternativas': ['Dos círculos',
                                  'Tres círculos',
                                  'Cuatro círculos',
                                  'Un círculo',
                                  'Cinco círculos'],
                 'correcta': 'B'},
                {'pregunta': 'Al evaluar un silogismo por diagramas, se '
                             'diagraman:',
                 'alternativas': ['La conclusión primero',
                                  'Solo las premisas',
                                  'Todo simultáneamente',
                                  'Solo la mayor',
                                  'Solo la menor'],
                 'correcta': 'B'},
                {'pregunta': 'Un silogismo es válido si, al diagramar las '
                             'premisas:',
                 'alternativas': ['Queda alguna región vacía',
                                  'Queda automáticamente representada la '
                                  'conclusión',
                                  'Se sombrean todos los círculos',
                                  'No hay ninguna X',
                                  'Las premisas son verdaderas'],
                 'correcta': 'B'},
                {'pregunta': 'Al diagramar conviene comenzar por las '
                             'premisas:',
                 'alternativas': ['Particulares',
                                  'Universales',
                                  'Negativas',
                                  'Afirmativas',
                                  'Más largas'],
                 'correcta': 'B'},
                {'pregunta': 'Una región en blanco en un diagrama de Venn '
                             'significa que:',
                 'alternativas': ['Está vacía',
                                  'No se sabe si tiene elementos',
                                  'Tiene elementos',
                                  'Es universal',
                                  'Es contradictoria'],
                 'correcta': 'B'},
                {'pregunta': 'El diagrama de Venn permite determinar de un '
                             'silogismo su:',
                 'alternativas': ['Verdad material',
                                  'Validez formal',
                                  'Utilidad',
                                  'Belleza',
                                  'Origen'],
                 'correcta': 'B'},
                {'pregunta': 'Los diagramas de Venn representan '
                             'gráficamente:',
                 'alternativas': ['Proposiciones compuestas',
                                  'Clases y sus relaciones',
                                  'Tablas de verdad',
                                  'Falacias',
                                  'Conectores lógicos'],
                 'correcta': 'B'},
                {'pregunta': 'En la diagramación, el círculo que se dibuja '
                             'para el término medio:',
                 'alternativas': ['No se dibuja',
                                  'Se dibuja intersecando a los otros dos',
                                  'Se dibuja aparte',
                                  'Se sombrea siempre',
                                  'Se marca con X'],
                 'correcta': 'B'},
                {'pregunta': 'Diagramar la conclusión antes que las premisas '
                             'constituye:',
                 'alternativas': ['El procedimiento correcto',
                                  'Un error de método',
                                  'Una simplificación válida',
                                  'Una regla de Venn',
                                  'Un atajo permitido'],
                 'correcta': 'B'}]}]


# ================================================================
# INTERFAZ
# ================================================================

def _tema_completo_filo(preguntas=False):
    """Fusiona las 17 balotas en un solo documento imprimible."""
    secs, cuadros, pregs = [], [], []
    for t in BALOTAS_FILO:
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
    return {"num": "1–17", "titulo": "TEMARIO COMPLETO DE FILOSOFÍA Y LÓGICA",
            "secciones": secs, "cuadros": cuadros, "preguntas": pregs}


def tab_fichas_filosofia(config=None):
    st.subheader("🧠 Filosofía y Lógica — Fichas y banco de preguntas (CEPRU)")
    st.caption("Las 17 balotas del temario oficial de Filosofía y Lógica, "
               "Área D. Cada una genera cuatro documentos.")

    opciones = {f"Balota {t['num']} — {t['titulo']}": t for t in BALOTAS_FILO}
    sel = st.selectbox("Balota:", list(opciones.keys()), key="ff_sel")
    tema = opciones[sel]

    c1, c2, c3 = st.columns(3)
    c1.metric("Espacios para completar", contar_espacios(tema))
    c2.metric("Preguntas", len(tema["preguntas"]))
    c3.metric("Cuadros", len(tema.get("cuadros", [])))

    grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                              placeholder="GRUPO CD", key="ff_grado")

    st.markdown("##### Descargar")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt, area="Filosofía y Lógica"),
                file_name=f"filosofia_balota{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="ff_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt, area="Filosofía y Lógica"),
                file_name=f"filosofia_balota{tema['num']}_docente.pdf",
                mime="application/pdf", use_container_width=True, key="ff_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de 20 preguntas**")
        try:
            tema_b = {**tema, "preguntas": balancear(tema["preguntas"])}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt, area="Filosofía y Lógica"),
                file_name=f"filosofia_preguntas{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="ff_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt, area="Filosofía y Lógica"),
                file_name=f"filosofia_preguntas{tema['num']}_claves.pdf",
                mime="application/pdf", use_container_width=True, key="ff_pd")
        except Exception as e:
            st.error(f"No se pudo generar el banco: {e}")

    st.markdown("---")
    st.markdown("##### Descargar el temario completo")
    g1, g2 = st.columns(2)
    with g1:
        if st.button("📚 Todas las fichas (17 balotas)",
                     use_container_width=True, key="ff_todas_f"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["ff_pdf"] = generar_ficha_texto(
                        _tema_completo_filo(), False, grado_txt,
                        area="Filosofía y Lógica")
                    st.session_state["ff_nom"] = "filosofia_fichas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")
    with g2:
        if st.button("📚 Todos los bancos (340 preguntas)",
                     use_container_width=True, key="ff_todas_p"):
            with st.spinner("Generando..."):
                try:
                    st.session_state["ff_pdf"] = generar_banco_preguntas(
                        _tema_completo_filo(preguntas=True), False, grado_txt,
                        area="Filosofía y Lógica")
                    st.session_state["ff_nom"] = "filosofia_preguntas_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.get("ff_pdf"):
        st.download_button(
            "⬇️ Descargar documento completo",
            data=st.session_state["ff_pdf"],
            file_name=st.session_state.get("ff_nom", "filosofia.pdf"),
            mime="application/pdf", use_container_width=True, key="ff_dl")

    with st.expander("Ver el contenido de esta balota"):
        for sec in tema["secciones"]:
            st.markdown(f"**{sec['titulo']}**")
            for it in sec["items"]:
                st.markdown("- " + _PATRON.sub(r"**\1**", it))
        st.markdown("**Primeras cinco preguntas:**")
        for i, p in enumerate(tema["preguntas"][:5], start=1):
            st.markdown(f"{i}. {p['pregunta']}")
            for k, a in enumerate(p["alternativas"]):
                marca = " ✅" if LETRAS[k] == p["correcta"] else ""
                st.markdown(f"   {LETRAS[k]}) {a}{marca}")
