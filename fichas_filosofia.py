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
                 'alternativas': ['Metafísica',
                                  'Cosmología',
                                  'Cosmogonía',
                                  'Ontología',
                                  'Astronomía'],
                 'correcta': 'C'},
                {'pregunta': 'El autor del poema «Teogonía» fue:',
                 'alternativas': ['Ptolomeo',
                                  'Aristóteles',
                                  'Platón',
                                  'Homero',
                                  'Hesíodo'],
                 'correcta': 'E'},
                {'pregunta': 'La cosmología se diferencia de la cosmogonía '
                             'porque explica mediante:',
                 'alternativas': ['Relatos y mitos',
                                  'Tradiciones orales',
                                  'Revelaciones divinas',
                                  'Poemas épicos',
                                  'Conceptos científicos y verificación'],
                 'correcta': 'E'},
                {'pregunta': 'El geocentrismo fue respaldado por:',
                 'alternativas': ['Ptolomeo y Aristóteles',
                                  'Galileo',
                                  'Kepler',
                                  'Copérnico',
                                  'Hubble'],
                 'correcta': 'A'},
                {'pregunta': 'El heliocentrismo fue sostenido por:',
                 'alternativas': ['Sócrates',
                                  'Ptolomeo',
                                  'Aristóteles',
                                  'Nicolás Copérnico',
                                  'Hesíodo'],
                 'correcta': 'D'},
                {'pregunta': 'Según el Big Bang, el universo se originó hace '
                             'aproximadamente:',
                 'alternativas': ['1 000 millones de años',
                                  '4 000 millones de años',
                                  '14 000 millones de años',
                                  '100 000 años',
                                  '500 millones de años'],
                 'correcta': 'C'},
                {'pregunta': 'Hubble descubrió en 1929 que las galaxias:',
                 'alternativas': ['Están fijas en la bóveda celeste',
                                  'Se alejan unas de otras',
                                  'Se acercan entre sí',
                                  'Permanecen inmóviles',
                                  'Giran alrededor de la Tierra'],
                 'correcta': 'B'},
                {'pregunta': 'Según la ley de Hubble, la velocidad de una '
                             'galaxia es proporcional a su:',
                 'alternativas': ['Luminosidad',
                                  'Edad',
                                  'Distancia',
                                  'Masa',
                                  'Temperatura'],
                 'correcta': 'C'},
                {'pregunta': 'Si una fuente de luz se aleja de nosotros, su '
                             'espectro se desplaza hacia el:',
                 'alternativas': ['Amarillo',
                                  'Rojo',
                                  'Violeta',
                                  'Verde',
                                  'Azul'],
                 'correcta': 'B'},
                {'pregunta': 'Se atribuye el primer uso del término '
                             '«filosofía» a:',
                 'alternativas': ['Tales de Mileto',
                                  'Aristóteles',
                                  'Platón',
                                  'Sócrates',
                                  'Pitágoras de Samos'],
                 'correcta': 'E'},
                {'pregunta': 'Para Platón, el origen de la filosofía está '
                             'en:',
                 'alternativas': ['La duda',
                                  'El lenguaje',
                                  'El asombro',
                                  'La fe',
                                  'La necesidad'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, filosofía significa:',
                 'alternativas': ['Ciencia del pensar',
                                  'Amor a la sabiduría',
                                  'Estudio del ser',
                                  'Estudio del cosmos',
                                  'Búsqueda de Dios'],
                 'correcta': 'B'},
                {'pregunta': 'Para Aristóteles, la filosofía es la ciencia '
                             'de:',
                 'alternativas': ['La conducta humana',
                                  'El lenguaje',
                                  'Los fenómenos naturales',
                                  'La sociedad',
                                  'Los primeros principios y las primeras '
                                  'causas'],
                 'correcta': 'E'},
                {'pregunta': 'La filosofía primera, según Aristóteles, se '
                             'denomina también:',
                 'alternativas': ['Lógica',
                                  'Física',
                                  'Metafísica',
                                  'Ética',
                                  'Gnoseología'],
                 'correcta': 'C'},
                {'pregunta': 'Según Russell, la filosofía nació de la unión '
                             'o el conflicto de dos impulsos:',
                 'alternativas': ['Místico y científico',
                                  'Práctico y teórico',
                                  'Individual y social',
                                  'Estético y ético',
                                  'Racional y emocional'],
                 'correcta': 'A'},
                {'pregunta': 'Para Rosental, la cuestión fundamental de la '
                             'filosofía es la relación entre:',
                 'alternativas': ['La causa y el efecto',
                                  'El pensar y el ser',
                                  'El bien y el mal',
                                  'Lo bello y lo útil',
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
                 'alternativas': ['Universal',
                                  'Crítica',
                                  'Problemática',
                                  'Dogmática',
                                  'Trascendental'],
                 'correcta': 'D'},
                {'pregunta': 'Que la actitud filosófica sea «incondicional» '
                             'significa que:',
                 'alternativas': ['Depende de la autoridad',
                                  'Persigue fines económicos',
                                  'Acepta cualquier opinión',
                                  'Busca el saber por el saber mismo',
                                  'Se somete a la religión'],
                 'correcta': 'D'},
                {'pregunta': 'La filosofía, como reflexión racional y '
                             'sistemática, se origina en:',
                 'alternativas': ['China',
                                  'Mesopotamia',
                                  'Grecia',
                                  'La India',
                                  'Egipto'],
                 'correcta': 'C'},
                {'pregunta': 'El problema fundamental de la filosofía trata '
                             'sobre la relación entre:',
                 'alternativas': ['La razón y la fe',
                                  'La vida y la muerte',
                                  'El bien y el mal',
                                  'El ser y el pensar',
                                  'El tiempo y el espacio'],
                 'correcta': 'D'},
                {'pregunta': 'El primer aspecto del problema fundamental '
                             'busca resolver si es primario:',
                 'alternativas': ['El bien o el mal',
                                  'La materia o la conciencia',
                                  'La razón o la fe',
                                  'La ciencia o el arte',
                                  'El tiempo o el espacio'],
                 'correcta': 'B'},
                {'pregunta': 'El segundo aspecto del problema fundamental '
                             'responde si el mundo es:',
                 'alternativas': ['Ordenado o caótico',
                                  'Cognoscible o no',
                                  'Bueno o malo',
                                  'Finito o infinito',
                                  'Material o espiritual'],
                 'correcta': 'B'},
                {'pregunta': 'Los filósofos que consideran que la materia es '
                             'primaria y engendra la conciencia se sitúan en '
                             'el:',
                 'alternativas': ['Idealismo',
                                  'Escepticismo',
                                  'Empirismo exclusivo',
                                  'Racionalismo exclusivo',
                                  'Materialismo'],
                 'correcta': 'E'},
                {'pregunta': 'Los filósofos que consideran primario al '
                             'espíritu y niegan que el mundo sea cognoscible '
                             'se sitúan en el:',
                 'alternativas': ['Racionalismo',
                                  'Materialismo',
                                  'Empirismo',
                                  'Positivismo',
                                  'Idealismo'],
                 'correcta': 'E'},
                {'pregunta': 'Según Wittgenstein, la concepción de la '
                             'filosofía es la actividad orientada hacia el '
                             'esclarecimiento del:',
                 'alternativas': ['Ser y la existencia',
                                  'Alma humana',
                                  'Cosmos',
                                  'Lenguaje',
                                  'Poder político'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina filosófica que analiza la '
                             'naturaleza, posibilidad y límites del '
                             'conocimiento en general se llama:',
                 'alternativas': ['Ontología',
                                  'Axiología',
                                  'Epistemología',
                                  'Gnoseología',
                                  'Estética'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina filosófica que es el estudio '
                             'crítico del conocimiento científico, su '
                             'fundamento y metodología, se llama:',
                 'alternativas': ['Gnoseología',
                                  'Epistemología',
                                  'Lógica',
                                  'Ética',
                                  'Antropología filosófica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia el '
                             'problema de los valores, su existencia y '
                             'naturaleza, se llama:',
                 'alternativas': ['Axiología',
                                  'Estética',
                                  'Ontología',
                                  'Ética',
                                  'Gnoseología'],
                 'correcta': 'A'},
                {'pregunta': 'La disciplina filosófica que estudia la '
                             'conducta o comportamiento moral del hombre en '
                             'sociedad se llama:',
                 'alternativas': ['Axiología',
                                  'Ontología',
                                  'Ética',
                                  'Estética',
                                  'Lógica'],
                 'correcta': 'C'},
                {'pregunta': 'La disciplina filosófica que estudia los '
                             'principios y reglas para distinguir el '
                             'razonamiento correcto del incorrecto se llama:',
                 'alternativas': ['Axiología',
                                  'Gnoseología',
                                  'Lógica',
                                  'Ontología',
                                  'Ética'],
                 'correcta': 'C'},
                {'pregunta': 'La disciplina filosófica que es el estudio del '
                             'ser de las cosas, del ser en tanto ser, se '
                             'llama:',
                 'alternativas': ['Gnoseología',
                                  'Estética',
                                  'Axiología',
                                  'Ontología',
                                  'Ética'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina filosófica que trata de lo bello '
                             'y los diferentes modos de aprehensión de '
                             'realidades bellas se llama:',
                 'alternativas': ['Ontología',
                                  'Axiología',
                                  'Lógica',
                                  'Ética',
                                  'Estética'],
                 'correcta': 'E'},
                {'pregunta': 'La disciplina filosófica que estudia la '
                             'esencia del hombre, su significado y la '
                             'finalidad de su existencia, se llama:',
                 'alternativas': ['Axiología',
                                  'Gnoseología',
                                  'Ontología',
                                  'Antropología filosófica',
                                  'Lógica'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de narraciones e historias de las '
                             'primeras civilizaciones acerca del origen del '
                             'universo corresponde a: (I CEPRU 2023)',
                 'alternativas': ['Teogonía',
                                  'B y C son correctas',
                                  'Cosmogonía',
                                  'Antropogonía',
                                  'Cosmología'],
                 'correcta': 'C'},
                {'pregunta': 'El fundamento moral de Kant señala que: (I '
                             'CEPRU 2025)',
                 'alternativas': ['Las acciones morales se realizan solo por '
                                  'respeto al deber y obediencia a la ley '
                                  'que dicta nuestra conciencia',
                                  'No existe hombre malo, solo ignorante, y '
                                  'la virtud está en el conocimiento',
                                  'La felicidad en la contemplación de Dios',
                                  'Ninguna de las anteriores',
                                  'La utilidad pública y la felicidad para '
                                  'la mayoría'],
                 'correcta': 'A'},
                {'pregunta': 'La concepción filosófica de Aristóteles, '
                             'también llamado «El Estagirita», es: (Primera '
                             'Oportunidad UNSAAC 2023)',
                 'alternativas': ['Estudio de las leyes universales de la '
                                  'naturaleza, sociedad y pensamiento',
                                  'La filosofía es tierra de nadie, entre la '
                                  'ciencia y la religión',
                                  'Pasión del espíritu humano por conocerse '
                                  'a sí mismo',
                                  'Ciencia de los primeros principios y de '
                                  'las primeras causas de lo que es',
                                  'Un compendio de resultados de la ciencia, '
                                  'y el filósofo es especialista en '
                                  'generalidades'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría del Big Bang o de la gran explosión '
                             'plantea que esta se produjo aproximadamente '
                             'hace: (Ordinario UNSAAC 2014-II)',
                 'alternativas': ['50 mil millones de años',
                                  '25 mil millones de años',
                                  '10 millones de años',
                                  '5 mil millones de años',
                                  '15 mil millones de años'],
                 'correcta': 'E'},
                {'pregunta': 'El hombre que somete todo conocimiento a una '
                             'crítica rigurosa adopta una actitud: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['Teórica',
                                  'Problemática',
                                  'Fundamental',
                                  'Filosófica',
                                  'Universal'],
                 'correcta': 'D'},
                {'pregunta': 'La cosmogonía es: (I CEPRU 2025-I)',
                 'alternativas': ['El conjunto de modelos del universo que '
                                  'permiten entenderlo en términos '
                                  'experimentales',
                                  'La gran explosión de la materia por la '
                                  'cual el universo sigue en expansión',
                                  'El conjunto de tratados y corrientes '
                                  'científicas que explican el origen del '
                                  'mundo',
                                  'El conjunto de historias y narraciones '
                                  'que trataron de explicar el origen del '
                                  'universo',
                                  'El modelo matemático y científico que '
                                  'afirma un despliegue dinámico de la '
                                  'materia'],
                 'correcta': 'D'},
                {'pregunta': 'El problema fundamental de la filosofía '
                             'subyace en: (Banco UNSAAC)',
                 'alternativas': ['Las posiciones materialistas e idealistas',
                                  'La oposición entre la materia y la forma',
                                  'La dialéctica de la historia',
                                  'Las posiciones empiristas y racionalistas',
                                  'La postura monista y dualista'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'COSMOGONÍA Y COSMOLOGÍA',
                      'items': ['Cosmogonía: de kosmos = mundo y goneia = '
                                'nacimiento. Conjunto de mitos y narraciones '
                                'con que las primeras civilizaciones '
                                'explicaron el origen del universo.',
                                'Hesíodo, en su poema «Teogonía», narra la '
                                'creación del mundo a partir del caos.',
                                'Cosmología: de kosmos y logos = estudio. '
                                'Estudia el universo mediante modelos '
                                'contrastables empírica y experimentalmente.',
                                'La diferencia está en que la cosmología '
                                'explica por conceptos científicos y '
                                'verificación, y la cosmogonía por relatos y '
                                'mitos.',
                                'Dos posturas marcaron la historia: el '
                                'geocentrismo, respaldado por Ptolomeo y '
                                'Aristóteles, y el heliocentrismo, por '
                                'Nicolás Copérnico.']},
                     {'titulo': 'TEORÍA DEL BIG BANG',
                      'items': ['Modelo cosmológico según el cual el '
                                'universo se originó en una singularidad '
                                'espaciotemporal de densidad infinita, hace '
                                'unos 14 000 millones de años.',
                                'Hubble descubrió en 1929 que la distancia '
                                'entre galaxias es cada vez mayor.',
                                'Ley de Hubble: la velocidad de una galaxia '
                                'es proporcional a su distancia.',
                                'Si una fuente de luz se aleja, su espectro '
                                'se desplaza al rojo; si se acerca, al '
                                'azul.']},
                     {'titulo': 'ORIGEN Y CONCEPCIONES DE LA FILOSOFÍA',
                      'items': ['Como reflexión racional y sistemática se '
                                'origina en Grecia, siglos VII–VI a.C.',
                                'Se atribuye a Pitágoras de Samos el primer '
                                'uso del término filosofía. Sócrates se '
                                'llamó a sí mismo «amante de la sabiduría».',
                                'Platón decía que el asombro es el origen de '
                                'la filosofía; Aristóteles, que es la '
                                'admiración lo que impulsa a filosofar.',
                                'Etimología: philein = amor y sophos = '
                                'sabiduría.',
                                'Concepción aristotélica: la filosofía es la '
                                'ciencia de los primeros principios y las '
                                'primeras causas; por eso se la llama '
                                'Metafísica o filosofía primera.',
                                'Concepción russelliana: nace de dos '
                                'impulsos, el místico y el científico; es '
                                'una tierra de nadie entre la ciencia y la '
                                'religión.',
                                'Concepción de Rosental: ciencia sobre las '
                                'leyes universales del ser y del '
                                'pensamiento; su cuestión fundamental es la '
                                'relación entre el pensar y el ser.',
                                'Según Wittgenstein, la filosofía es una '
                                'actividad orientada hacia el '
                                'esclarecimiento del lenguaje, indagando si '
                                'los enunciados tienen sentido.']},
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
                                'humana puede penetrar sus misterios.',
                                'Los filósofos que consideran que la materia '
                                'es primaria y la conciencia secundaria se '
                                'sitúan en el materialismo.',
                                'Los filósofos que consideran que lo '
                                'primario es el espíritu y niegan que el '
                                'mundo sea cognoscible se sitúan en el '
                                'idealismo.']},
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
                                'y características.',
                                'La ética estudia la conducta o '
                                'comportamiento moral del hombre en '
                                'sociedad.',
                                'La lógica estudia los principios, métodos y '
                                'reglas para distinguir el razonamiento '
                                'correcto del incorrecto.',
                                'La ontología es el estudio del ser de las '
                                'cosas, del ser en tanto ser.',
                                'La estética trata de lo bello y los '
                                'diferentes modos de aprehensión de '
                                'realidades bellas.',
                                'La antropología filosófica estudia la '
                                'esencia del hombre, su significado y la '
                                'finalidad de su existencia.']}],
  'qr_reto': [{'pregunta': 'La disciplina filosófica que es el estudio del '
                           'ser de las cosas, del ser en tanto ser, se '
                           'llama:',
               'respuesta': 'Ontología'},
              {'pregunta': 'La filosofía, como reflexión racional y '
                           'sistemática, se origina en:',
               'respuesta': 'Grecia'},
              {'pregunta': 'Para Aristóteles, la filosofía es la ciencia de:',
               'respuesta': 'Los primeros principios y las primeras causas'}],
  'qr_dato': 'Según Wittgenstein, la filosofía es una actividad orientada '
             'hacia el esclarecimiento del lenguaje, indagando si los '
             'enunciados tienen sentido.'},
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
                 'alternativas': ['Nous',
                                  'Logos',
                                  'Ápeiron',
                                  'Eidos',
                                  'Arjé'],
                 'correcta': 'E'},
                {'pregunta': 'Para Tales de Mileto, el principio de todas '
                             'las cosas es:',
                 'alternativas': ['El fuego',
                                  'La tierra',
                                  'El átomo',
                                  'El agua',
                                  'El aire'],
                 'correcta': 'D'},
                {'pregunta': 'El ápeiron, lo indeterminado e infinito, fue '
                             'propuesto por:',
                 'alternativas': ['Anaxímenes',
                                  'Parménides',
                                  'Anaximandro',
                                  'Tales',
                                  'Heráclito'],
                 'correcta': 'C'},
                {'pregunta': 'Para Heráclito de Éfeso, el arjé es:',
                 'alternativas': ['El aire',
                                  'El ápeiron',
                                  'El fuego',
                                  'El número',
                                  'El agua'],
                 'correcta': 'C'},
                {'pregunta': 'La frase «nadie se baña dos veces en el mismo '
                             'río» corresponde a:',
                 'alternativas': ['Demócrito',
                                  'Parménides',
                                  'Protágoras',
                                  'Sócrates',
                                  'Heráclito'],
                 'correcta': 'E'},
                {'pregunta': 'Parménides de Elea sostuvo que el ser es:',
                 'alternativas': ['Inmutable',
                                  'Múltiple',
                                  'Divisible',
                                  'Cambiante',
                                  'Material'],
                 'correcta': 'A'},
                {'pregunta': 'Demócrito de Abdera afirmó que todo está '
                             'compuesto por:',
                 'alternativas': ['Números',
                                  'Fuego',
                                  'Ideas',
                                  'Átomos',
                                  'Agua'],
                 'correcta': 'D'},
                {'pregunta': '«El hombre es la medida de todas las cosas» '
                             'pertenece a:',
                 'alternativas': ['Aristóteles',
                                  'Sócrates',
                                  'Gorgias',
                                  'Protágoras',
                                  'Platón'],
                 'correcta': 'D'},
                {'pregunta': 'El método socrático de dar a luz las ideas '
                             'mediante preguntas se llama:',
                 'alternativas': ['Inducción',
                                  'Mayéutica',
                                  'Dialéctica',
                                  'Silogismo',
                                  'Ironía'],
                 'correcta': 'B'},
                {'pregunta': 'La frase «solo sé que nada sé» se atribuye a:',
                 'alternativas': ['Platón',
                                  'Sócrates',
                                  'Epicuro',
                                  'Protágoras',
                                  'Heráclito'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de las Ideas fue formulada por:',
                 'alternativas': ['Demócrito',
                                  'Parménides',
                                  'Sócrates',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'D'},
                {'pregunta': 'Según Platón, el mundo de las Ideas eternas es '
                             'el mundo:',
                 'alternativas': ['Sensible',
                                  'Corpóreo',
                                  'Material',
                                  'Aparente',
                                  'Inteligible'],
                 'correcta': 'E'},
                {'pregunta': 'La escuela fundada por Platón fue:',
                 'alternativas': ['La Stoa',
                                  'El Jardín',
                                  'El Pórtico',
                                  'El Liceo',
                                  'La Academia'],
                 'correcta': 'E'},
                {'pregunta': 'La escuela fundada por Aristóteles fue:',
                 'alternativas': ['La Stoa',
                                  'El Jardín',
                                  'La Escuela de Mileto',
                                  'El Liceo',
                                  'La Academia'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría hilemórfica de Aristóteles sostiene '
                             'que todo ser se compone de:',
                 'alternativas': ['Ser y no ser',
                                  'Materia y forma',
                                  'Acto y potencia únicamente',
                                  'Cuerpo y alma',
                                  'Idea y copia'],
                 'correcta': 'B'},
                {'pregunta': 'Aristóteles es considerado el padre de la:',
                 'alternativas': ['Psicología',
                                  'Lógica',
                                  'Estética',
                                  'Política',
                                  'Ética'],
                 'correcta': 'B'},
                {'pregunta': 'Para Epicuro, el fin de la vida es el placer '
                             'entendido como:',
                 'alternativas': ['Goce sensorial ilimitado',
                                  'Acumulación de bienes',
                                  'Fama',
                                  'Ausencia de dolor y serenidad',
                                  'Poder político'],
                 'correcta': 'D'},
                {'pregunta': 'El estado de serenidad e imperturbabilidad en '
                             'Epicuro se denomina:',
                 'alternativas': ['Eudaimonía',
                                  'Areté',
                                  'Catarsis',
                                  'Nous',
                                  'Ataraxia'],
                 'correcta': 'E'},
                {'pregunta': 'Marco Aurelio perteneció a la escuela:',
                 'alternativas': ['Platónica',
                                  'Epicúrea',
                                  'Cínica',
                                  'Escéptica',
                                  'Estoica'],
                 'correcta': 'E'},
                {'pregunta': 'Los sofistas se caracterizaron por:',
                 'alternativas': ['Buscar verdades absolutas',
                                  'Fundar la lógica formal',
                                  'Estudiar los astros',
                                  'Rechazar la política',
                                  'Enseñar retórica por dinero y defender el '
                                  'relativismo'],
                 'correcta': 'E'},
                {'pregunta': 'Pitágoras de Samos fundó una escuela '
                             'místico-filosófica en la ciudad de:',
                 'alternativas': ['Abdera',
                                  'Crotona',
                                  'Éfeso',
                                  'Mileto',
                                  'Elea'],
                 'correcta': 'B'},
                {'pregunta': 'La doctrina pitagórica sobre la inmortalidad y '
                             'transmigración de las almas se llama:',
                 'alternativas': ['Metempsicosis',
                                  'Dialéctica',
                                  'Mayéutica',
                                  'Reminiscencia',
                                  'Hilozoísmo'],
                 'correcta': 'A'},
                {'pregunta': 'Para Pitágoras, el arjé o principio de todas '
                             'las cosas son:',
                 'alternativas': ['El agua',
                                  'Los átomos',
                                  'Los números',
                                  'El aire',
                                  'El fuego'],
                 'correcta': 'C'},
                {'pregunta': 'El número considerado más valorado por los '
                             'pitagóricos, representado en la tetraktys, fue '
                             'el:',
                 'alternativas': ['7', '10', '1', '4', '100'],
                 'correcta': 'B'},
                {'pregunta': 'El filósofo con quien se inicia la Metafísica '
                             'y el conocimiento científico fue:',
                 'alternativas': ['Pitágoras',
                                  'Heráclito',
                                  'Demócrito',
                                  'Parménides de Elea',
                                  'Tales de Mileto'],
                 'correcta': 'D'},
                {'pregunta': 'La afirmación ontológica central de Parménides '
                             'fue:',
                 'alternativas': ['«El ser es»',
                                  '«Conócete a ti mismo»',
                                  '«Todo fluye»',
                                  '«El hombre es la medida de todas las '
                                  'cosas»',
                                  '«Solo sé que nada sé»'],
                 'correcta': 'A'},
                {'pregunta': 'Para Parménides, admitir el cambio o devenir '
                             'equivale a admitir:',
                 'alternativas': ['La razón',
                                  'El arjé',
                                  'El logos',
                                  'El ser',
                                  'El no ser'],
                 'correcta': 'E'},
                {'pregunta': 'Parménides formuló, aunque de manera '
                             'implícita, el principio lógico de:',
                 'alternativas': ['Causalidad',
                                  'Identidad',
                                  'Razón suficiente',
                                  'No contradicción exclusivo',
                                  'Tercero excluido exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Demócrito desarrolló su teoría atómica a '
                             'partir de las ideas de su maestro:',
                 'alternativas': ['Anaximandro',
                                  'Leucipo',
                                  'Parménides',
                                  'Tales',
                                  'Pitágoras'],
                 'correcta': 'B'},
                {'pregunta': 'El sofista considerado el creador de la '
                             'sofística, autor de «Sobre la naturaleza o el '
                             'no ser», fue:',
                 'alternativas': ['Sócrates',
                                  'Antístenes',
                                  'Gorgias',
                                  'Protágoras',
                                  'Trasímaco'],
                 'correcta': 'C'},
                {'pregunta': 'Gorgias sostenía, entre sus tres tesis, que si '
                             'algo existiera:',
                 'alternativas': ['Sería material',
                                  'Se transformaría en fuego',
                                  'Sería eterno',
                                  'No podría ser conocido por el hombre',
                                  'Sería visible para todos'],
                 'correcta': 'D'},
                {'pregunta': 'Propuso la teoría atómica: (Primera '
                             'Oportunidad UNSAAC 2025)',
                 'alternativas': ['Anaxímenes de Mileto',
                                  'Heráclito de Éfeso',
                                  'Demócrito de Abdera',
                                  'Pitágoras de Samos',
                                  'Parménides de Elea'],
                 'correcta': 'C'},
                {'pregunta': 'El filósofo que, en relación a la ética, '
                             'sostuvo que el mal es producto de la '
                             'ignorancia y la verdad se busca practicando la '
                             'virtud, es: (Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Protágoras',
                                  'Aristóteles',
                                  'Platón',
                                  'Heráclito',
                                  'Sócrates'],
                 'correcta': 'E'},
                {'pregunta': 'La «Metafísica» es una obra de: (I CEPRU 2023)',
                 'alternativas': ['Pitágoras',
                                  'Platón',
                                  'Aristóteles',
                                  'Gorgias',
                                  'Sócrates'],
                 'correcta': 'C'},
                {'pregunta': 'El argumento «El origen y fundamento de todas '
                             'las cosas es el agua» fue sustentado por el '
                             'filósofo: (Primera Oportunidad UNSAAC 2023)',
                 'alternativas': ['Demócrito de Abdera',
                                  'Pitágoras de Samos',
                                  'Heráclito de Éfeso',
                                  'Parménides de Elea',
                                  'Tales de Mileto'],
                 'correcta': 'E'},
                {'pregunta': 'El filósofo y famoso astrónomo griego, '
                             'considerado el padre de la filosofía, es: '
                             '(Ordinario UNSAAC 2014-II)',
                 'alternativas': ['Tales de Mileto',
                                  'Parménides de Elea',
                                  'Sócrates de Atenas',
                                  'Empédocles de Agrigento',
                                  'Heráclito de Éfeso'],
                 'correcta': 'A'},
                {'pregunta': 'La dependencia de los seres respecto a otras '
                             'realidades que sustentan su existencia, y la '
                             'necesidad de un primer principio incausado '
                             'similar al motor inmóvil de Aristóteles, '
                             'corresponden a: (I CEPRU 2019-I)',
                 'alternativas': ['Prueba de los grados de perfección - '
                                  'prueba del orden',
                                  'Prueba de la finalidad - prueba de la '
                                  'causa eficiente',
                                  'Prueba del ser necesario - prueba de la '
                                  'causa eficiente',
                                  'Prueba del movimiento - prueba de la '
                                  'causa eficiente',
                                  'Prueba del ser necesario - prueba de los '
                                  'grados de perfección'],
                 'correcta': 'C'},
                {'pregunta': 'Los tipos de justicia (general y particular), '
                             'así como las partes del método planteado por '
                             'Descartes, pueden hallarse respectivamente en '
                             'las obras: (II CEPRU 2019-I)',
                 'alternativas': ['Gorgias - Discurso del método',
                                  'Ética a Nicómaco - Discurso del método',
                                  'Ética a Nicómaco - Fenomenología del '
                                  'espíritu',
                                  'Magna Moralia - Dignidad de las ciencias',
                                  'Diálogos - Discurso del método'],
                 'correcta': 'B'},
                {'pregunta': 'El investigador científico que, en su obra «El '
                             'origen de las especies», manifestó que la '
                             'naturaleza viva evoluciona por selección '
                             'natural, es: (II CEPRU 2019-I)',
                 'alternativas': ['Renato Descartes',
                                  'Charles Darwin',
                                  'Friedrich Hegel',
                                  'Francis Bacon',
                                  'Karl Marx'],
                 'correcta': 'B'},
                {'pregunta': 'El enunciado «Las cosas son números y los '
                             'números son cosas» corresponde a: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['Protágoras',
                                  'Parménides',
                                  'Demócrito',
                                  'Pitágoras de Samos',
                                  'Heráclito'],
                 'correcta': 'D'},
                {'pregunta': 'La mayéutica socrática tenía como objetivo: (I '
                             'CEPRU 2025-I)',
                 'alternativas': ['Ganar simpatizantes para ejercer la '
                                  'política',
                                  'Imponer las ideas del maestro a sus '
                                  'discípulos',
                                  'Utilizar la retórica para convencer a los '
                                  'ciudadanos',
                                  'Engañar con medias verdades al '
                                  'interlocutor',
                                  'Dar a luz la verdad que está en el '
                                  'interior del hombre'],
                 'correcta': 'E'},
                {'pregunta': 'Según Platón, la virtud que caracteriza a la '
                             'sociedad en su conjunto es: (Banco UNSAAC)',
                 'alternativas': ['Templanza',
                                  'Humildad',
                                  'Prudencia',
                                  'Fortaleza',
                                  'Justicia'],
                 'correcta': 'E'}],
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
                                'transmigración de las almas.',
                                'Para Pitágoras, el arjé son los números: '
                                '«las cosas son números y los números son '
                                'cosas». El número 10 era el más valorado, '
                                'representado en la tetraktys.',
                                'Parménides de Elea, con quien se inicia la '
                                'Metafísica, sostuvo la afirmación '
                                'ontológica: «el ser es», negando la '
                                'posibilidad del cambio.',
                                'Para Parménides, admitir el cambio o '
                                'devenir es admitir el no ser; formuló, '
                                'aunque implícitamente, el Principio de '
                                'Identidad.',
                                'Demócrito de Abdera: todo está compuesto '
                                'por átomos, partículas indivisibles, según '
                                'la teoría heredada de su maestro Leucipo.']},
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
                                'a la razón y aceptar el destino.']}],
  'qr_reto': [{'pregunta': 'Para Heráclito de Éfeso, el arjé es:',
               'respuesta': 'El fuego'},
              {'pregunta': 'Pitágoras de Samos fundó una escuela '
                           'místico-filosófica en la ciudad de:',
               'respuesta': 'Crotona'},
              {'pregunta': 'La escuela fundada por Aristóteles fue:',
               'respuesta': 'El Liceo'}],
  'qr_dato': 'Epicuro de Samos: el fin de la vida es el placer entendido '
             'como ausencia de dolor y serenidad o ataraxia.'},
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
                {'titulo': '3.4 LAS CINCO VÍAS DE SANTO TOMÁS DE AQUINO',
                 'items': ['{Prueba del Movimiento}: todo lo que se mueve es '
                           'movido por otro; no siendo posible una serie '
                           'infinita, debe existir un {primer motor '
                           'inmóvil}, que es Dios.',
                           '{Prueba de la Causa Eficiente}: ninguna causa '
                           'puede ser causa de sí misma; debe existir una '
                           '{primera causa incausada}, que es Dios.',
                           '{Prueba del Ser Necesario}: existen seres '
                           'contingentes que comienzan y dejan de existir; '
                           'deben tener su causa en un {primer ser '
                           'necesario}, que es Dios.',
                           '{Prueba de los Grados de Perfección}: observamos '
                           'distintos grados de bondad y belleza, lo que '
                           'implica un {ser supremo} u óptimo como modelo de '
                           'comparación, que es Dios.',
                           '{Prueba del Orden o Finalidad}: los seres '
                           'inorgánicos actúan con un fin sin poseer '
                           'inteligencia; deben ser dirigidos por un {ser '
                           'inteligente} superior, que es Dios.']},
                {'titulo': '3.5 EL RENACIMIENTO',
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
                 'alternativas': ['Empírico',
                                  'Teocéntrico',
                                  'Cosmocéntrico',
                                  'Antropocéntrico',
                                  'Logocéntrico'],
                 'correcta': 'B'},
                {'pregunta': 'En la Edad Media la filosofía fue considerada:',
                 'alternativas': ['Ciencia suprema',
                                  'Independiente de la fe',
                                  'Sinónimo de retórica',
                                  'Sierva de la teología',
                                  'Un arte liberal menor'],
                 'correcta': 'D'},
                {'pregunta': 'El problema central de la filosofía medieval '
                             'fue la relación entre:',
                 'alternativas': ['Razón y fe',
                                  'Cuerpo y alma',
                                  'Ser y pensar',
                                  'Bien y mal',
                                  'Materia y forma'],
                 'correcta': 'A'},
                {'pregunta': 'San Agustín de Hipona estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Demócrito',
                                  'Los estoicos',
                                  'Platón',
                                  'Epicuro',
                                  'Aristóteles'],
                 'correcta': 'C'},
                {'pregunta': 'Una obra fundamental de San Agustín es:',
                 'alternativas': ['El Príncipe',
                                  'La República',
                                  'La ciudad de Dios',
                                  'Órganon',
                                  'Suma Teológica'],
                 'correcta': 'C'},
                {'pregunta': 'La doctrina agustiniana según la cual Dios '
                             'ilumina la mente humana se llama:',
                 'alternativas': ['Predestinación',
                                  'Iluminación',
                                  'Analogía',
                                  'Revelación',
                                  'Emanación'],
                 'correcta': 'B'},
                {'pregunta': '«Cree para comprender y comprende para creer» '
                             'corresponde a:',
                 'alternativas': ['Platón',
                                  'Santo Tomás',
                                  'Maquiavelo',
                                  'San Agustín',
                                  'Aristóteles'],
                 'correcta': 'D'},
                {'pregunta': 'La etapa de los Padres de la Iglesia se '
                             'denomina:',
                 'alternativas': ['Patrística',
                                  'Escolástica',
                                  'Humanismo',
                                  'Renacimiento',
                                  'Ilustración'],
                 'correcta': 'A'},
                {'pregunta': 'Santo Tomás de Aquino estuvo influido '
                             'principalmente por:',
                 'alternativas': ['Parménides',
                                  'Epicuro',
                                  'Heráclito',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'E'},
                {'pregunta': 'La obra principal de Santo Tomás de Aquino es:',
                 'alternativas': ['El Príncipe',
                                  'Confesiones',
                                  'La ciudad de Dios',
                                  'Metafísica',
                                  'Suma Teológica'],
                 'correcta': 'E'},
                {'pregunta': 'Santo Tomás formuló para demostrar la '
                             'existencia de Dios:',
                 'alternativas': ['Cuatro causas',
                                  'Dos silogismos',
                                  'Las cinco vías',
                                  'Tres pruebas',
                                  'Siete argumentos'],
                 'correcta': 'C'},
                {'pregunta': 'Para Santo Tomás, la razón y la fe:',
                 'alternativas': ['Son idénticas',
                                  'Se contradicen',
                                  'No se relacionan',
                                  'Se complementan',
                                  'Se excluyen'],
                 'correcta': 'D'},
                {'pregunta': 'La escolástica se basó como método en:',
                 'alternativas': ['La observación astronómica',
                                  'La experimentación',
                                  'La disputa y el comentario de textos',
                                  'El diálogo socrático',
                                  'La introspección'],
                 'correcta': 'C'},
                {'pregunta': 'El Renacimiento se caracterizó por el:',
                 'alternativas': ['Dogmatismo',
                                  'Antropocentrismo',
                                  'Escepticismo',
                                  'Geocentrismo',
                                  'Teocentrismo'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «El Príncipe» fue:',
                 'alternativas': ['Erasmo',
                                  'Descartes',
                                  'Galileo',
                                  'Tomás Moro',
                                  'Nicolás Maquiavelo'],
                 'correcta': 'E'},
                {'pregunta': 'Maquiavelo es conocido por separar la política '
                             'de:',
                 'alternativas': ['La historia',
                                  'La moral',
                                  'La economía',
                                  'La religión únicamente',
                                  'El derecho'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima «el fin justifica los medios» se '
                             'atribuye a:',
                 'alternativas': ['San Agustín',
                                  'Maquiavelo',
                                  'Platón',
                                  'Epicuro',
                                  'Santo Tomás'],
                 'correcta': 'B'},
                {'pregunta': 'El Renacimiento recuperó la cultura:',
                 'alternativas': ['Oriental',
                                  'Egipcia',
                                  'Medieval',
                                  'Grecolatina',
                                  'Germánica'],
                 'correcta': 'D'},
                {'pregunta': 'El movimiento que valoró la dignidad y las '
                             'capacidades del ser humano se llamó:',
                 'alternativas': ['Humanismo',
                                  'Positivismo',
                                  'Estoicismo',
                                  'Escolasticismo',
                                  'Escepticismo'],
                 'correcta': 'A'},
                {'pregunta': 'La expresión latina «ancilla theologiae» '
                             'significa que la filosofía era:',
                 'alternativas': ['Sierva de la teología',
                                  'Base de la política',
                                  'Enemiga de la fe',
                                  'Reina de las ciencias',
                                  'Madre de la lógica'],
                 'correcta': 'A'},
                {'pregunta': 'El astrónomo polaco que formuló la teoría '
                             'heliocéntrica en el Renacimiento fue:',
                 'alternativas': ['Galileo Galilei',
                                  'Giordano Bruno',
                                  'Johannes Kepler',
                                  'Nicolás Copérnico',
                                  'Tycho Brahe'],
                 'correcta': 'D'},
                {'pregunta': 'La obra de Copérnico que expone la teoría '
                             'heliocéntrica se titula:',
                 'alternativas': ['Sidereus Nuncius',
                                  'Novum Organum',
                                  'De Revolutionibus Orbium Coelestium',
                                  'Diálogo sobre los dos máximos sistemas',
                                  'Almagesto'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría heliocéntrica de Copérnico resolvía '
                             'los problemas del modelo geocéntrico planteado '
                             'por:',
                 'alternativas': ['Ptolomeo',
                                  'Pitágoras',
                                  'Aristóteles',
                                  'Eratóstenes',
                                  'Platón'],
                 'correcta': 'A'},
                {'pregunta': 'San Agustín de Hipona nació en la ciudad de '
                             'Tagaste, ubicada en la actual:',
                 'alternativas': ['Marruecos',
                                  'Egipto',
                                  'Libia',
                                  'Túnez',
                                  'Argelia'],
                 'correcta': 'E'},
                {'pregunta': 'El filósofo que planteó las cinco vías para '
                             'demostrar la existencia de Dios fue: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['Maquiavelo',
                                  'Santo Tomás de Aquino',
                                  'Platón',
                                  'Aristóteles',
                                  'San Agustín de Hipona'],
                 'correcta': 'B'},
                {'pregunta': 'Una característica del pensamiento en la Edad '
                             'Media fue: (I CEPRU 2025-I)',
                 'alternativas': ['Buscar armonizar la fe cristiana con la '
                                  'razón, con dominio religioso',
                                  'El surgimiento de la ciencia moderna y el '
                                  'saber experimental',
                                  'Cultivar las artes, el humanismo y el '
                                  'conocimiento científico',
                                  'Dejar de lado los dogmas de la fe '
                                  'cristiana y el teocentrismo',
                                  'El surgimiento del empirismo y '
                                  'materialismo'],
                 'correcta': 'A'},
                {'pregunta': 'El filósofo representante de la Escolástica, '
                             'autor de la Suma Teológica, es: (Banco UNSAAC)',
                 'alternativas': ['San Anselmo de Canterbury',
                                  'Santo Tomás de Aquino',
                                  'San Agustín de Hipona',
                                  'San Alberto Magno',
                                  'San Ambrosio de Milán'],
                 'correcta': 'B'},
                {'pregunta': '«El Príncipe», escrito por Nicolás Maquiavelo, '
                             'está dedicado a: (II CEPRU 2019-II)',
                 'alternativas': ['Pedro de Cosme de Médici',
                                  'Lorenzo de Médici',
                                  'Su Santidad',
                                  'Juliano de Médici',
                                  'Cosme de Médici'],
                 'correcta': 'B'},
                {'pregunta': 'La vía de Santo Tomás que afirma que todo lo '
                             'que se mueve es movido por otro, llegando a un '
                             'primer motor inmóvil, se llama prueba:',
                 'alternativas': ['Del Ser Necesario',
                                  'De la Causa Eficiente',
                                  'Del Orden o Finalidad',
                                  'De los Grados de Perfección',
                                  'Del Movimiento'],
                 'correcta': 'E'},
                {'pregunta': 'La vía de Santo Tomás que afirma que ninguna '
                             'causa puede ser causa de sí misma, llegando a '
                             'una primera causa incausada, se llama prueba:',
                 'alternativas': ['De los Grados de Perfección',
                                  'De la Causa Eficiente',
                                  'Del Movimiento',
                                  'Del Orden o Finalidad',
                                  'Del Ser Necesario'],
                 'correcta': 'B'},
                {'pregunta': 'La vía de Santo Tomás que afirma que los seres '
                             'contingentes deben tener su causa en un primer '
                             'ser necesario se llama prueba:',
                 'alternativas': ['Del Ser Necesario',
                                  'De la Causa Eficiente',
                                  'Del Orden o Finalidad',
                                  'Del Movimiento',
                                  'De los Grados de Perfección'],
                 'correcta': 'A'},
                {'pregunta': 'La vía de Santo Tomás que se basa en observar '
                             'distintos grados de bondad y belleza, '
                             'implicando un ser supremo como modelo, se '
                             'llama prueba:',
                 'alternativas': ['De los Grados de Perfección',
                                  'Del Movimiento',
                                  'Del Orden o Finalidad',
                                  'De la Causa Eficiente',
                                  'Del Ser Necesario'],
                 'correcta': 'A'},
                {'pregunta': 'La vía de Santo Tomás que sostiene que los '
                             'seres inorgánicos actúan con un fin dirigidos '
                             'por un ser inteligente se llama prueba:',
                 'alternativas': ['Del Movimiento',
                                  'De los Grados de Perfección',
                                  'Del Orden o Finalidad',
                                  'Del Ser Necesario',
                                  'De la Causa Eficiente'],
                 'correcta': 'C'}],
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
                     {'titulo': 'LAS CINCO VÍAS DE SANTO TOMÁS DE AQUINO',
                      'items': ['Prueba del Movimiento: todo lo que se mueve '
                                'es movido por otro; no siendo posible una '
                                'serie infinita, debe existir un primer '
                                'motor inmóvil, que es Dios.',
                                'Prueba de la Causa Eficiente: ninguna causa '
                                'puede ser causa de sí misma; debe existir '
                                'una primera causa incausada, que es Dios.',
                                'Prueba del Ser Necesario: existen seres '
                                'contingentes que comienzan y dejan de '
                                'existir; deben tener su causa en un primer '
                                'ser necesario, que es Dios.',
                                'Prueba de los Grados de Perfección: '
                                'observamos distintos grados de bondad y '
                                'belleza, lo que implica un ser supremo u '
                                'óptimo como modelo de comparación, que es '
                                'Dios.',
                                'Prueba del Orden o Finalidad: los seres '
                                'inorgánicos actúan con un fin sin poseer '
                                'inteligencia; deben ser dirigidos por un '
                                'ser inteligente superior, que es Dios.']},
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
                                'medios».']}],
  'qr_reto': [{'pregunta': 'El movimiento que valoró la dignidad y las '
                           'capacidades del ser humano se llamó:',
               'respuesta': 'Humanismo'},
              {'pregunta': 'La escolástica se basó como método en:',
               'respuesta': 'La disputa y el comentario de textos'},
              {'pregunta': 'San Agustín de Hipona nació en la ciudad de '
                           'Tagaste, ubicada en la actual:',
               'respuesta': 'Argelia'}],
  'qr_dato': 'Etapa de los Padres de la Iglesia, que defendieron el '
             'cristianismo frente al paganismo.'},
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
                 'alternativas': ['René Descartes',
                                  'Kant',
                                  'Locke',
                                  'Hegel',
                                  'Bacon'],
                 'correcta': 'A'},
                {'pregunta': 'El principio «pienso, luego existo» pertenece '
                             'a:',
                 'alternativas': ['Descartes',
                                  'Locke',
                                  'Marx',
                                  'Hegel',
                                  'Kant'],
                 'correcta': 'A'},
                {'pregunta': 'El método cartesiano parte de:',
                 'alternativas': ['La inducción',
                                  'La observación',
                                  'La duda metódica',
                                  'La experiencia sensible',
                                  'La revelación'],
                 'correcta': 'C'},
                {'pregunta': 'Para el empirismo, todo conocimiento proviene '
                             'de:',
                 'alternativas': ['La razón pura',
                                  'La intuición',
                                  'Las ideas innatas',
                                  'La revelación',
                                  'La experiencia'],
                 'correcta': 'E'},
                {'pregunta': 'John Locke sostuvo que la mente al nacer es:',
                 'alternativas': ['Una sustancia pensante',
                                  'Un depósito de ideas innatas',
                                  'Una tabla rasa',
                                  'Un reflejo divino',
                                  'Un espejo del cosmos'],
                 'correcta': 'C'},
                {'pregunta': 'La síntesis entre racionalismo y empirismo fue '
                             'realizada por:',
                 'alternativas': ['Descartes',
                                  'Marx',
                                  'Locke',
                                  'Hegel',
                                  'Kant'],
                 'correcta': 'E'},
                {'pregunta': 'El lema «atrévete a saber» corresponde a:',
                 'alternativas': ['Hegel',
                                  'Marx',
                                  'Kant',
                                  'Mariátegui',
                                  'Descartes'],
                 'correcta': 'C'},
                {'pregunta': 'Kant llamó «noúmeno» a:',
                 'alternativas': ['La idea innata',
                                  'El juicio sintético',
                                  'El imperativo moral',
                                  'Lo que aparece a los sentidos',
                                  'La cosa en sí, incognoscible'],
                 'correcta': 'E'},
                {'pregunta': 'El imperativo categórico de Kant exige obrar '
                             'de modo que la acción pueda ser:',
                 'alternativas': ['Rentable',
                                  'Aprobada socialmente',
                                  'Placentera',
                                  'Útil para uno mismo',
                                  'Ley universal'],
                 'correcta': 'E'},
                {'pregunta': 'Los tres momentos de la dialéctica hegeliana '
                             'son:',
                 'alternativas': ['Ser, no ser y devenir',
                                  'Tesis, antítesis y síntesis',
                                  'Causa, efecto y fin',
                                  'Materia, forma y acto',
                                  'Duda, método y certeza'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema filosófico de Hegel es:',
                 'alternativas': ['Materialista',
                                  'Empirista',
                                  'Positivista',
                                  'Escéptico',
                                  'Idealista'],
                 'correcta': 'E'},
                {'pregunta': 'Marx invirtió la dialéctica de Hegel y '
                             'desarrolló:',
                 'alternativas': ['El pragmatismo',
                                  'El idealismo absoluto',
                                  'El materialismo dialéctico e histórico',
                                  'El empirismo',
                                  'El criticismo'],
                 'correcta': 'C'},
                {'pregunta': 'Para Marx, la infraestructura económica '
                             'determina:',
                 'alternativas': ['La biología',
                                  'El lenguaje únicamente',
                                  'La superestructura jurídica, política e '
                                  'ideológica',
                                  'El clima',
                                  'La geografía'],
                 'correcta': 'C'},
                {'pregunta': '«Los filósofos se han limitado a interpretar '
                             'el mundo; de lo que se trata es de '
                             'transformarlo» pertenece a:',
                 'alternativas': ['Mariátegui',
                                  'Kant',
                                  'Salazar Bondy',
                                  'Hegel',
                                  'Marx'],
                 'correcta': 'E'},
                {'pregunta': 'El autor de «7 ensayos de interpretación de la '
                             'realidad peruana» es:',
                 'alternativas': ['Francisco Miró Quesada',
                                  'Augusto Salazar Bondy',
                                  'José Carlos Mariátegui',
                                  'Víctor Raúl Haya de la Torre',
                                  'González Prada'],
                 'correcta': 'C'},
                {'pregunta': 'Para Mariátegui, el problema del indio es '
                             'fundamentalmente un problema:',
                 'alternativas': ['Religioso',
                                  'Racial',
                                  'De la tierra',
                                  'Educativo',
                                  'Administrativo'],
                 'correcta': 'C'},
                {'pregunta': 'El autor de «¿Existe una filosofía de nuestra '
                             'América?» es:',
                 'alternativas': ['Antenor Orrego',
                                  'Augusto Salazar Bondy',
                                  'Alejandro Deustua',
                                  'Francisco Miró Quesada',
                                  'Mariátegui'],
                 'correcta': 'B'},
                {'pregunta': 'Según Salazar Bondy, la filosofía '
                             'latinoamericana ha sido:',
                 'alternativas': ['Superior a la europea',
                                  'Inexistente',
                                  'Original y autónoma',
                                  'Puramente científica',
                                  'Imitativa, reflejo de una sociedad '
                                  'dominada'],
                 'correcta': 'E'},
                {'pregunta': 'Mariátegui aplicó al análisis del Perú el '
                             'método:',
                 'alternativas': ['Escolástico',
                                  'Positivista',
                                  'Existencialista',
                                  'Fenomenológico',
                                  'Marxista'],
                 'correcta': 'E'},
                {'pregunta': 'El criticismo kantiano sostiene que el '
                             'conocimiento resulta de:',
                 'alternativas': ['La revelación divina',
                                  'La unión de razón y experiencia',
                                  'La tradición',
                                  'Solo los sentidos',
                                  'Solo la razón'],
                 'correcta': 'B'},
                {'pregunta': 'El filósofo inglés materialista que propuso el '
                             'método inductivo en su obra Novum Organum fue:',
                 'alternativas': ['Thomas Aquino',
                                  'David Hume',
                                  'John Locke',
                                  'Francisco Bacon',
                                  'Tomás Hobbes'],
                 'correcta': 'D'},
                {'pregunta': 'Bacon sostuvo que antes de investigar hay que '
                             'eliminar de la mente los:',
                 'alternativas': ['Dogmas',
                                  'Ídolos',
                                  'Silogismos',
                                  'Postulados',
                                  'Axiomas'],
                 'correcta': 'B'},
                {'pregunta': 'El ídolo baconiano que consiste en interpretar '
                             'antropomórficamente la naturaleza se llama '
                             'ídolo de la:',
                 'alternativas': ['Caverna',
                                  'Foro',
                                  'Ciudad',
                                  'Tribu',
                                  'Teatro'],
                 'correcta': 'D'},
                {'pregunta': 'El ídolo baconiano originado en los prejuicios '
                             'personales de cada individuo se llama ídolo de '
                             'la:',
                 'alternativas': ['Caverna',
                                  'Foro',
                                  'Escuela',
                                  'Tribu',
                                  'Teatro'],
                 'correcta': 'A'},
                {'pregunta': 'El ídolo baconiano relacionado con el mal uso '
                             'del lenguaje se llama ídolo del:',
                 'alternativas': ['Palacio',
                                  'Teatro',
                                  'Foro',
                                  'Tribu',
                                  'Templo'],
                 'correcta': 'C'},
                {'pregunta': 'El ídolo baconiano relacionado con la '
                             'aceptación acrítica de autoridades se llama '
                             'ídolo del:',
                 'alternativas': ['Caverna',
                                  'Foro',
                                  'Tribu',
                                  'Teatro',
                                  'Mercado'],
                 'correcta': 'D'},
                {'pregunta': 'Descartes distinguió tres sustancias: la res '
                             'extensa, la res necesaria y la:',
                 'alternativas': ['Res divina exclusiva',
                                  'Res cogitans',
                                  'Res naturae',
                                  'Res publica',
                                  'Res finita'],
                 'correcta': 'B'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'espiritual, cuya esencia es el pensamiento, se '
                             'llama:',
                 'alternativas': ['Res corporal',
                                  'Res extensa',
                                  'Res necesaria',
                                  'Res cogitans',
                                  'Res mundi'],
                 'correcta': 'D'},
                {'pregunta': 'En la filosofía cartesiana, la sustancia '
                             'corporal, cuya esencia es la extensión, se '
                             'llama:',
                 'alternativas': ['Res cogitans',
                                  'Res mentis',
                                  'Res necesaria',
                                  'Res extensa',
                                  'Res divina'],
                 'correcta': 'D'},
                {'pregunta': 'John Locke distinguió dos tipos de '
                             'experiencia: la interna y la:',
                 'alternativas': ['Externa',
                                  'Trascendental',
                                  'Espiritual',
                                  'Racional',
                                  'Innata'],
                 'correcta': 'A'},
                {'pregunta': 'La experiencia que surge cuando la mente '
                             'reflexiona sobre sus propias sensaciones, '
                             'según Locke, se llama experiencia:',
                 'alternativas': ['Interna',
                                  'Sensorial exclusiva',
                                  'Trascendental',
                                  'Externa',
                                  'Innata'],
                 'correcta': 'A'},
                {'pregunta': 'Tomás Hobbes sostuvo que en estado natural el '
                             'hombre es:',
                 'alternativas': ['Altruista',
                                  'Sociable por naturaleza',
                                  'Racional puro',
                                  'Pacífico por instinto',
                                  'Antisocial, movido por el deseo y el '
                                  'temor'],
                 'correcta': 'E'},
                {'pregunta': 'La célebre frase de Hobbes que describe la '
                             'naturaleza humana en estado natural es:',
                 'alternativas': ['«El hombre nace bueno»',
                                  '«El hombre es un animal político»',
                                  '«El hombre es la medida de todas las '
                                  'cosas»',
                                  '«El hombre es un junco pensante»',
                                  '«El hombre es un lobo para el hombre»'],
                 'correcta': 'E'},
                {'pregunta': 'Según Hobbes, para superar el estado de guerra '
                             'de todos contra todos, los hombres deben '
                             'establecer un:',
                 'alternativas': ['Sistema feudal',
                                  'Concilio religioso',
                                  'Gobierno directo',
                                  'Contrato social',
                                  'Imperio universal'],
                 'correcta': 'D'},
                {'pregunta': 'La obra más conocida de Hobbes, donde expone '
                             'su teoría del contrato social, es:',
                 'alternativas': ['El Contrato Social',
                                  'Utopía',
                                  'Dos Tratados sobre el Gobierno',
                                  'El Leviatán',
                                  'El Príncipe'],
                 'correcta': 'D'},
                {'pregunta': 'Friedrich Nietzsche es considerado el filósofo '
                             'más importante del siglo XIX en la corriente '
                             'del:',
                 'alternativas': ['Positivismo',
                                  'Racionalismo',
                                  'Empirismo',
                                  'Idealismo absoluto',
                                  'Voluntarismo'],
                 'correcta': 'E'},
                {'pregunta': 'Nietzsche estuvo influenciado principalmente '
                             'por el filósofo:',
                 'alternativas': ['Locke',
                                  'Kant',
                                  'Schopenhauer',
                                  'Hegel',
                                  'Descartes'],
                 'correcta': 'C'},
                {'pregunta': 'Nietzsche distinguió la moral del amo, que '
                             'exalta la fuerza, de la moral:',
                 'alternativas': ['Divina',
                                  'Científica',
                                  'Del esclavo',
                                  'Universal',
                                  'Racional'],
                 'correcta': 'C'},
                {'pregunta': 'Para Nietzsche, la moral del esclavo, que '
                             'exalta la compasión y la resignación, es la '
                             'moral de los:',
                 'alternativas': ['Científicos',
                                  'Comerciantes',
                                  'Guerreros',
                                  'Filósofos griegos',
                                  'Cristianos'],
                 'correcta': 'E'},
                {'pregunta': 'Nietzsche proclamó una idea célebre conocida '
                             'como:',
                 'alternativas': ['La duda de Dios',
                                  'El nacimiento de Dios',
                                  'El regreso de Dios',
                                  'La muerte de Dios',
                                  'El silencio de Dios'],
                 'correcta': 'D'},
                {'pregunta': 'El ideal nietzscheano del hombre que acepta la '
                             'muerte de Dios y vive fiel a la tierra se '
                             'llama:',
                 'alternativas': ['El hombre sabio',
                                  'El superhombre',
                                  'El hombre justo',
                                  'El hombre racional',
                                  'El hombre virtuoso'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las obras principales de Nietzsche es:',
                 'alternativas': ['El Príncipe',
                                  'El Leviatán',
                                  'Utopía',
                                  'Confesiones',
                                  'Así habló Zaratustra'],
                 'correcta': 'E'},
                {'pregunta': 'Manuel González Prada mostró su inclinación '
                             'filosófica hacia el:',
                 'alternativas': ['Positivismo',
                                  'Idealismo',
                                  'Racionalismo',
                                  'Existencialismo',
                                  'Empirismo puro'],
                 'correcta': 'A'},
                {'pregunta': 'El balance que hizo González Prada de la '
                             'Independencia del Perú fue:',
                 'alternativas': ['Neutral',
                                  'Optimista',
                                  'Pesimista',
                                  'Indiferente',
                                  'Triunfalista'],
                 'correcta': 'C'},
                {'pregunta': 'Según González Prada, la derrota del Perú en '
                             'la Guerra del Pacífico se debió principalmente '
                             'a:',
                 'alternativas': ['La ignorancia y el espíritu de '
                                  'servidumbre',
                                  'La falta de armamento',
                                  'La superioridad militar chilena '
                                  'exclusivamente',
                                  'La distancia geográfica',
                                  'El clima'],
                 'correcta': 'A'},
                {'pregunta': 'González Prada consideraba que el Estado era '
                             'un instrumento de los poderosos para '
                             'perpetuar:',
                 'alternativas': ['La servidumbre de los más débiles',
                                  'La educación',
                                  'La ciencia',
                                  'El progreso',
                                  'El comercio'],
                 'correcta': 'A'},
                {'pregunta': 'Para González Prada, el Perú verdadero y '
                             'profundo es el que pertenece a:',
                 'alternativas': ['Los criollos',
                                  'La oligarquía',
                                  'Los extranjeros',
                                  'Los indígenas',
                                  'El clero'],
                 'correcta': 'D'},
                {'pregunta': 'La obra principal de González Prada, que '
                             'influyó en Mariátegui y Haya de la Torre, es:',
                 'alternativas': ['Páginas Libres',
                                  'Anarquía',
                                  'Nuevas páginas libres',
                                  'Horas de lucha',
                                  'El Perú profundo'],
                 'correcta': 'A'},
                {'pregunta': 'Respecto al conocimiento, Descartes afirmó '
                             'que: (Primera Oportunidad UNSAAC 2025)',
                 'alternativas': ['Nada hay en el entendimiento que no haya '
                                  'estado primero en los sentidos',
                                  'El hombre nace con ideas innatas en el '
                                  'entendimiento',
                                  'No existen ideas innatas en la mente del '
                                  'hombre',
                                  'Debemos confiar en nuestros sentidos, ya '
                                  'que nos dan conocimiento',
                                  'La mente del hombre es como una tabula '
                                  'rasa'],
                 'correcta': 'B'},
                {'pregunta': 'La postura filosófica de Friedrich Hegel, así '
                             'como su obra principal, corresponden a: (I '
                             'CEPRU 2019-I)',
                 'alternativas': ['Idealismo objetivo - Fenomenología del '
                                  'espíritu',
                                  'Materialismo dialéctico - Manifiesto '
                                  'comunista',
                                  'Idealismo subjetivo - La Sagrada Familia',
                                  'Materialismo mecanicista - El Capital',
                                  'Realismo moderado - Fenomenología del '
                                  'espíritu'],
                 'correcta': 'A'},
                {'pregunta': 'Según Hegel, los ciudadanos existen gracias a: '
                             '(II CEPRU 2018-II)',
                 'alternativas': ['El Estado',
                                  'La realidad',
                                  'La subjetividad',
                                  'La objetividad',
                                  'La sociedad'],
                 'correcta': 'A'},
                {'pregunta': 'Pertenece al pensamiento de Leibniz: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['Su proyecto es la realización de los '
                                  'axiomas de Peano',
                                  'Inventa las tablas de verdad',
                                  'Una de sus obras se denomina '
                                  '«Monadología»',
                                  'Escribe la obra «Tractatus '
                                  'Logico-Philosophicus»',
                                  'Su proyecto es denominado '
                                  '«Conceptografía»'],
                 'correcta': 'C'},
                {'pregunta': 'Para Renato Descartes, la idea de Dios es: (I '
                             'CEPRU 2025-I)',
                 'alternativas': ['Admirable',
                                  'Descartado',
                                  'Comprendido',
                                  'Innato',
                                  'Correspondido'],
                 'correcta': 'D'},
                {'pregunta': 'George Hegel es representante del: (I CEPRU '
                             '2025-I)',
                 'alternativas': ['Materialismo histórico',
                                  'Materialismo mecanicista',
                                  'Materialismo dialéctico',
                                  'Idealismo subjetivo',
                                  'Idealismo objetivo'],
                 'correcta': 'E'},
                {'pregunta': 'El filósofo representante del racionalismo '
                             'moderno, autor del «Discurso del método», fue: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Francis Bacon',
                                  'Immanuel Kant',
                                  'Friedrich Hegel',
                                  'René Descartes',
                                  'Karl Marx'],
                 'correcta': 'D'}],
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
                                '(aceptación acrítica de autoridades).',
                                'René Descartes, padre de la filosofía '
                                'moderna, fundó el racionalismo. Su método '
                                'parte de la duda metódica.',
                                'Su principio fundamental es «pienso, luego '
                                'existo» (cogito ergo sum).',
                                'Descartes distinguió tres sustancias: la '
                                'res extensa (sustancia corporal), la res '
                                'cogitans (sustancia espiritual o '
                                'pensamiento), y la res necesaria (Dios).']},
                     {'titulo': 'THOMAS HOBBES Y EL CONTRATO SOCIAL',
                      'items': ['Tomás Hobbes, filósofo inglés, sostuvo que '
                                'las leyes que rigen al hombre son las '
                                'mismas que rigen el universo.',
                                'Para Hobbes, en estado natural el hombre es '
                                'antisocial y se mueve por el deseo y el '
                                'temor.',
                                'Su célebre frase «el hombre es un lobo para '
                                'el hombre» describe el estado de «guerra de '
                                'todos contra todos».',
                                'Para superar ese estado, los hombres deben '
                                'establecer un «contrato social», '
                                'transfiriendo sus derechos a un soberano '
                                'absoluto.',
                                'Su obra más conocida, donde expone esta '
                                'teoría, es el «Leviatán».']},
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
                                'convertirse en ley universal.',
                                'Hegel: desarrolló el método dialéctico, con '
                                'tres momentos: tesis, antítesis y síntesis. '
                                'Su sistema es idealista.']},
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
                                'compasión y la resignación.',
                                'Para Nietzsche, la moral del esclavo es la '
                                'moral de los cristianos, que predican el '
                                'amor al prójimo y la renuncia a la vida.',
                                'Proclamó la «muerte de Dios»: solo tras '
                                'ella surgirá un nuevo hombre que acepte la '
                                'vida y el eterno retorno.',
                                'Planteó el ideal del superhombre, que '
                                'acepta la muerte de Dios y vive fiel a la '
                                'tierra, sin buscar mundos trascendentes.']},
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
                                'derrota del Perú en la Guerra del Pacífico.',
                                'Fue antirreligioso, anarquista y anti '
                                'hispanista; consideró al Estado un '
                                'instrumento de los poderosos para perpetuar '
                                'la servidumbre.',
                                'Sostuvo que el Perú verdadero y profundo es '
                                'el que pertenece a los indígenas, y culpó a '
                                'la oligarquía de la crisis nacional.',
                                'Su obra principal, «Páginas Libres», '
                                'influyó profundamente en Abraham '
                                'Valdelomar, Haya de la Torre y '
                                'Mariátegui.']},
                     {'titulo': 'FILOSOFÍA EN EL PERÚ',
                      'items': ['José Carlos Mariátegui: autor de «7 ensayos '
                                'de interpretación de la realidad peruana». '
                                'Aplicó el marxismo al análisis del Perú, '
                                'señalando que el problema del indio es un '
                                'problema de la tierra.',
                                'Augusto Salazar Bondy: autor de «¿Existe '
                                'una filosofía de nuestra América?». Sostuvo '
                                'que nuestra filosofía ha sido imitativa por '
                                'ser reflejo de una sociedad dominada.']}],
  'qr_reto': [{'pregunta': 'Según Salazar Bondy, la filosofía '
                           'latinoamericana ha sido:',
               'respuesta': 'Imitativa, reflejo de una sociedad dominada'},
              {'pregunta': 'El ídolo baconiano relacionado con el mal uso '
                           'del lenguaje se llama ídolo del:',
               'respuesta': 'Foro'},
              {'pregunta': 'El ideal nietzscheano del hombre que acepta la '
                           'muerte de Dios y vive fiel a la tierra se llama:',
               'respuesta': 'El superhombre'}],
  'qr_dato': 'Hegel: desarrolló el método dialéctico, con tres momentos: '
             'tesis, antítesis y síntesis. Su sistema es idealista.'},
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
                {'titulo': '5.3 MECANISMOS DE LA TEORÍA SINTÉTICA '
                           '(NEODARWINISMO)',
                 'items': ['La {selección natural}, igual que en la teoría '
                           'de Darwin, sigue siendo un mecanismo central.',
                           'Las {mutaciones} son cambios aleatorios en la '
                           'estructura genética de los organismos.',
                           'La {deriva genética} modifica, a lo largo de '
                           'varias generaciones, la estructura genética de '
                           'las poblaciones.',
                           'El {flujo genético} es el proceso por el cual '
                           'las poblaciones se vuelven genéticamente '
                           '{homogéneas}.',
                           'Charles Darwin escribió, entre sus obras más '
                           'importantes, «El origen de las {especies}» y «El '
                           'origen del hombre».']},
                {'titulo': '5.4 EL HOMBRE COMO SER NATURAL Y ESPIRITUAL',
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
                {'titulo': '5.5 RASGOS BIOLÓGICOS DEL HOMBRE COMO SER '
                           'NATURAL',
                 'items': ['La posición {bípeda}, vertical y erecta, es uno '
                           'de los rasgos biológicos originales del hombre.',
                           'La constitución y uso de la {mano} como órgano '
                           'de aprehensión permitió al hombre inventar '
                           'instrumentos de producción.',
                           'El hombre posee un {cerebro} excepcionalmente '
                           'grande respecto a otras especies.',
                           'El hombre tiene un {lento} proceso de '
                           'maduración: es el animal de niñez más larga y '
                           'general.',
                           'El {lenguaje articulado} se logró a través de la '
                           'especialización de los órganos fonadores.']}],
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
                                  'Antropología filosófica',
                                  'Ontología'],
                 'correcta': 'D'},
                {'pregunta': 'La antropología filosófica se diferencia de la '
                             'cultural porque:',
                 'alternativas': ['Describe costumbres',
                                  'Mide cráneos',
                                  'Estudia fósiles',
                                  'Reflexiona sobre el ser del hombre',
                                  'Analiza idiomas'],
                 'correcta': 'D'},
                {'pregunta': 'El creacionismo sostiene que el hombre fue:',
                 'alternativas': ['Creado por un ser superior',
                                  'Autogenerado',
                                  'Fruto de la evolución',
                                  'Resultado de mutaciones',
                                  'Producto del azar'],
                 'correcta': 'A'},
                {'pregunta': 'El mito griego que explica el origen del '
                             'hombre mediante un titán es el de:',
                 'alternativas': ['Ícaro',
                                  'Narciso',
                                  'Edipo',
                                  'Prometeo',
                                  'Sísifo'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de la evolución por selección '
                             'natural fue formulada por:',
                 'alternativas': ['Charles Darwin',
                                  'Mendel',
                                  'Wallace únicamente',
                                  'De Vries',
                                  'Lamarck'],
                 'correcta': 'A'},
                {'pregunta': 'El neodarwinismo complementa a Darwin con los '
                             'aportes de:',
                 'alternativas': ['La genética y las mutaciones',
                                  'La astronomía',
                                  'La teología',
                                  'La geología',
                                  'La lingüística'],
                 'correcta': 'A'},
                {'pregunta': 'Como ser natural, el hombre se caracteriza '
                             'por:',
                 'alternativas': ['Ser libre',
                                  'Su capacidad simbólica',
                                  'Poseer un cuerpo biológico sujeto a leyes '
                                  'naturales',
                                  'Crear valores',
                                  'Producir cultura'],
                 'correcta': 'C'},
                {'pregunta': 'Como ser espiritual, el hombre posee:',
                 'alternativas': ['Solo necesidades biológicas',
                                  'Conciencia, libertad y capacidad de crear '
                                  'cultura',
                                  'Reflejos condicionados',
                                  'Únicamente sensaciones',
                                  'Instintos'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión «zoon politikon», que define al '
                             'hombre como ser social, es de:',
                 'alternativas': ['Platón',
                                  'Rousseau',
                                  'Aristóteles',
                                  'Sócrates',
                                  'Hobbes'],
                 'correcta': 'C'},
                {'pregunta': 'Lo que distingue al hombre del resto de '
                             'animales, según la antropología filosófica, '
                             'es:',
                 'alternativas': ['Su fuerza física',
                                  'Su longevidad',
                                  'Su alimentación',
                                  'Su tamaño',
                                  'Su racionalidad y capacidad simbólica'],
                 'correcta': 'E'},
                {'pregunta': 'La capacidad humana de transformar la '
                             'naturaleza mediante la actividad consciente '
                             'es:',
                 'alternativas': ['La mutación',
                                  'El instinto',
                                  'La adaptación pasiva',
                                  'El reflejo',
                                  'El trabajo'],
                 'correcta': 'E'},
                {'pregunta': 'La tradición judeocristiana corresponde a la '
                             'teoría:',
                 'alternativas': ['Materialista',
                                  'Neodarwinista',
                                  'Positivista',
                                  'Creacionista',
                                  'Evolucionista'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre es considerado un ser bidimensional '
                             'porque es a la vez:',
                 'alternativas': ['Bueno y malo',
                                  'Natural y espiritual',
                                  'Racional e irracional',
                                  'Joven y viejo',
                                  'Individual y aislado'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje simbólico es una característica:',
                 'alternativas': ['Compartida con todos los animales',
                                  'Propia del ser humano',
                                  'Exclusiva de los primates',
                                  'Puramente instintiva',
                                  'Innata y no aprendida'],
                 'correcta': 'B'},
                {'pregunta': 'La antropología filosófica se pregunta '
                             'fundamentalmente por:',
                 'alternativas': ['La anatomía comparada',
                                  'La esencia y el sentido de la existencia '
                                  'humana',
                                  'Los restos arqueológicos',
                                  'La distribución geográfica',
                                  'Las costumbres de los pueblos'],
                 'correcta': 'B'},
                {'pregunta': 'La cultura, según la antropología filosófica, '
                             'es producto de la dimensión:',
                 'alternativas': ['Instintiva',
                                  'Refleja',
                                  'Genética',
                                  'Espiritual',
                                  'Biológica'],
                 'correcta': 'D'},
                {'pregunta': 'La libertad humana implica fundamentalmente la '
                             'capacidad de:',
                 'alternativas': ['Seguir los instintos',
                                  'Someterse al destino',
                                  'Elegir y responder por los propios actos',
                                  'Hacer cualquier cosa sin límites',
                                  'Evitar toda norma'],
                 'correcta': 'C'},
                {'pregunta': 'Para el evolucionismo, el hombre y los '
                             'primates actuales comparten:',
                 'alternativas': ['El mismo lenguaje',
                                  'Idéntica especie',
                                  'Igual capacidad simbólica',
                                  'Un antepasado común',
                                  'La misma cultura'],
                 'correcta': 'D'},
                {'pregunta': 'Las necesidades e instintos corresponden a la '
                             'dimensión humana:',
                 'alternativas': ['Axiológica',
                                  'Cultural',
                                  'Natural o biológica',
                                  'Simbólica',
                                  'Espiritual'],
                 'correcta': 'C'},
                {'pregunta': 'El ser humano crea valores, normas y símbolos '
                             'porque es un ser:',
                 'alternativas': ['Determinado genéticamente',
                                  'Puramente biológico',
                                  'Instintivo',
                                  'Aislado',
                                  'Cultural y espiritual'],
                 'correcta': 'E'},
                {'pregunta': 'Los representantes de la Teoría Sintética o '
                             'Neodarwinismo son Dobzhansky, Mayr y:',
                 'alternativas': ['Mendel',
                                  'Simpson',
                                  'Haeckel',
                                  'Wallace',
                                  'Lamarck'],
                 'correcta': 'B'},
                {'pregunta': 'El problema del hombre es estudiado por la: (I '
                             'CEPRU 2025)',
                 'alternativas': ['Ética',
                                  'Estética',
                                  'Antropología filosófica',
                                  'Epistemología',
                                  'Teoría del conocimiento'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría que menciona que el hombre fue '
                             'creado por un ser supremo a su imagen y '
                             'semejanza es: (Primera Oportunidad UNSAAC '
                             '2023)',
                 'alternativas': ['Deriva continental',
                                  'Evolucionismo',
                                  'Neodarwinismo',
                                  'Creacionismo',
                                  'Teoría sintética'],
                 'correcta': 'D'},
                {'pregunta': 'La afirmación «Las especies se transforman a '
                             'lo largo de sucesivas generaciones» '
                             'corresponde a la teoría: (Primera Oportunidad '
                             'UNSAAC 2023)',
                 'alternativas': ['Consecuencialista',
                                  'Creacionista',
                                  'Sociologista',
                                  'Espiritualista',
                                  'Evolucionista'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto de prácticas, hechos, '
                             'instituciones y determinaciones del gobierno, '
                             'de un Estado y de la sociedad civil, se '
                             'refiere a: (Ordinario UNSAAC 2014-II)',
                 'alternativas': ['Ciencia',
                                  'Anarquía',
                                  'Política',
                                  'Religión',
                                  'Predicción'],
                 'correcta': 'C'},
                {'pregunta': 'Que los ídolos de la caverna, descritos por '
                             'Francis Bacon, abarquen parte de la '
                             'interioridad espiritual del hombre, siendo '
                             'esta a su vez producto de la materia, '
                             'advierte: (I CEPRU 2019-I)',
                 'alternativas': ['Un evolucionismo sutil a partir de una '
                                  'sustancia espiritual',
                                  'La postura monista respecto a la esencia '
                                  'del hombre',
                                  'Un idealismo enmascarado respecto a la '
                                  'esencia del hombre',
                                  'Una postura materialista respecto al '
                                  'problema fundamental de la filosofía',
                                  'La necesidad de un ente espiritual que da '
                                  'origen al ser'],
                 'correcta': 'D'},
                {'pregunta': 'El ser humano está constituido de materia y '
                             'espíritu; sin embargo, el espiritualismo '
                             'sostiene que el hombre es: (II CEPRU 2019-I)',
                 'alternativas': ['Un ser real y existencial',
                                  'Un ser de origen eminentemente espiritual',
                                  'La mezcla de lo espiritual y material',
                                  'El conjunto de las relaciones sociales',
                                  'Un conjunto de relaciones ideológicas'],
                 'correcta': 'B'},
                {'pregunta': 'Que el hombre esté compuesto de cuerpo y alma '
                             'corresponde al dualismo: (I CEPRU 2025-I)',
                 'alternativas': ['Académico',
                                  'Cosmológico',
                                  'Orgánico',
                                  'Antropológico',
                                  'Genético'],
                 'correcta': 'D'},
                {'pregunta': 'Las capacidades del hombre referidas al '
                             'pensamiento, razonamiento, sentimiento y '
                             'consciencia lo muestran como un ser: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Material',
                                  'Culto',
                                  'Natural',
                                  'Espiritual',
                                  'Espontáneo'],
                 'correcta': 'D'},
                {'pregunta': 'Uno de los rasgos biológicos originales del '
                             'hombre, relacionado con su forma de '
                             'desplazarse, es la posición:',
                 'alternativas': ['Bípeda, vertical y erecta',
                                  'Cuadrúpeda',
                                  'Reptante',
                                  'Sedente',
                                  'Suspendida'],
                 'correcta': 'A'},
                {'pregunta': 'El órgano que, como instrumento de '
                             'aprehensión, permitió al hombre inventar '
                             'diversos instrumentos de producción es:',
                 'alternativas': ['La boca',
                                  'La mano',
                                  'El oído',
                                  'El ojo',
                                  'El pie'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo biológico notable del hombre, '
                             'referido a su proceso de crecimiento, es tener '
                             'una maduración:',
                 'alternativas': ['Regresiva',
                                  'Instantánea',
                                  'Lenta y prolongada',
                                  'Ausente',
                                  'Rápida y breve'],
                 'correcta': 'C'},
                {'pregunta': 'El lenguaje articulado del hombre se logró a '
                             'través de la especialización de los órganos:',
                 'alternativas': ['Digestivos',
                                  'Sensoriales exclusivos',
                                  'Respiratorios exclusivos',
                                  'Motores',
                                  'Fonadores'],
                 'correcta': 'E'},
                {'pregunta': 'En la Teoría Sintética o Neodarwinismo, los '
                             'cambios aleatorios en la estructura genética '
                             'de los organismos se llaman:',
                 'alternativas': ['Mutaciones',
                                  'Selección natural',
                                  'Flujo genético',
                                  'Deriva genética',
                                  'Adaptación'],
                 'correcta': 'A'},
                {'pregunta': 'En la Teoría Sintética, el proceso por el cual '
                             'las poblaciones se vuelven genéticamente '
                             'homogéneas se llama:',
                 'alternativas': ['Selección natural',
                                  'Mutación',
                                  'Deriva genética',
                                  'Flujo genético',
                                  'Herencia'],
                 'correcta': 'D'},
                {'pregunta': 'En la Teoría Sintética, la modificación de la '
                             'estructura genética de las poblaciones a lo '
                             'largo de varias generaciones se llama:',
                 'alternativas': ['Adaptación',
                                  'Mutación',
                                  'Selección natural',
                                  'Flujo genético',
                                  'Deriva genética'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las obras más representativas de Charles '
                             'Darwin se encuentra:',
                 'alternativas': ['La lógica de la investigación científica',
                                  'El discurso del método',
                                  'Así habló Zaratustra',
                                  'El capital',
                                  'El origen de las especies'],
                 'correcta': 'E'}],
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
                     {'titulo': 'MECANISMOS DE LA TEORÍA SINTÉTICA '
                                '(NEODARWINISMO)',
                      'items': ['La selección natural, igual que en la '
                                'teoría de Darwin, sigue siendo un mecanismo '
                                'central.',
                                'Las mutaciones son cambios aleatorios en la '
                                'estructura genética de los organismos.',
                                'La deriva genética modifica, a lo largo de '
                                'varias generaciones, la estructura genética '
                                'de las poblaciones.',
                                'El flujo genético es el proceso por el cual '
                                'las poblaciones se vuelven genéticamente '
                                'homogéneas.',
                                'Charles Darwin escribió, entre sus obras '
                                'más importantes, «El origen de las '
                                'especies» y «El origen del hombre».']},
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
                                'transformador.']},
                     {'titulo': 'RASGOS BIOLÓGICOS DEL HOMBRE COMO SER '
                                'NATURAL',
                      'items': ['La posición bípeda, vertical y erecta, es '
                                'uno de los rasgos biológicos originales del '
                                'hombre.',
                                'La constitución y uso de la mano como '
                                'órgano de aprehensión permitió al hombre '
                                'inventar instrumentos de producción.',
                                'El hombre posee un cerebro excepcionalmente '
                                'grande respecto a otras especies.',
                                'El hombre tiene un lento proceso de '
                                'maduración: es el animal de niñez más larga '
                                'y general.',
                                'El lenguaje articulado se logró a través de '
                                'la especialización de los órganos '
                                'fonadores.']}],
  'qr_reto': [{'pregunta': 'El hombre es considerado un ser bidimensional '
                           'porque es a la vez:',
               'respuesta': 'Natural y espiritual'},
              {'pregunta': 'Lo que distingue al hombre del resto de '
                           'animales, según la antropología filosófica, es:',
               'respuesta': 'Su racionalidad y capacidad simbólica'},
              {'pregunta': 'El lenguaje simbólico es una característica:',
               'respuesta': 'Propia del ser humano'}],
  'qr_dato': 'Disciplina filosófica que estudia al hombre en su totalidad: '
             'su esencia, su origen y el sentido de su existencia.'},
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
                                  'Axiología',
                                  'Lógica',
                                  'Ontología'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, gnoseología proviene de '
                             'gnosis, que significa:',
                 'alternativas': ['Palabra',
                                  'Conocimiento',
                                  'Ley',
                                  'Valor',
                                  'Ser'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento del conocimiento que designa a '
                             'quien conoce es:',
                 'alternativas': ['El método',
                                  'El sujeto cognoscente',
                                  'La imagen',
                                  'La verdad',
                                  'El objeto'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental que el sujeto elabora '
                             'del objeto se denomina:',
                 'alternativas': ['Imagen',
                                  'Juicio',
                                  'Símbolo',
                                  'Concepto puro',
                                  'Idea innata'],
                 'correcta': 'A'},
                {'pregunta': 'En el acto de conocer, el objeto:',
                 'alternativas': ['Desaparece',
                                  'Se subjetiviza',
                                  'Se destruye',
                                  'Se transforma',
                                  'Permanece inalterado'],
                 'correcta': 'E'},
                {'pregunta': 'El conocimiento obtenido a través de los '
                             'sentidos es:',
                 'alternativas': ['Racional',
                                  'Sensible',
                                  'Abstracto',
                                  'Científico',
                                  'Universal'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento sensible se caracteriza por '
                             'ser:',
                 'alternativas': ['Apriorístico',
                                  'Singular, concreto y subjetivo',
                                  'Deductivo',
                                  'Necesario',
                                  'Universal y abstracto'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento racional se caracteriza por '
                             'ser:',
                 'alternativas': ['Momentáneo',
                                  'Sensorial',
                                  'Singular',
                                  'Concreto',
                                  'Universal, abstracto y objetivo'],
                 'correcta': 'E'},
                {'pregunta': 'El conocimiento espontáneo, no verificado ni '
                             'sistemático es el:',
                 'alternativas': ['Filosófico',
                                  'Vulgar',
                                  'Técnico',
                                  'Científico',
                                  'Teológico'],
                 'correcta': 'B'},
                {'pregunta': 'El conocimiento científico se caracteriza por '
                             'ser:',
                 'alternativas': ['Intuitivo',
                                  'Metódico, sistemático y verificable',
                                  'Subjetivo',
                                  'Dogmático',
                                  'Espontáneo'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría que define la verdad como adecuación '
                             'entre el pensamiento y la realidad es la de:',
                 'alternativas': ['La coherencia',
                                  'El pragmatismo',
                                  'El consenso',
                                  'La correspondencia',
                                  'La utilidad'],
                 'correcta': 'D'},
                {'pregunta': 'La concepción clásica de la verdad se atribuye '
                             'a:',
                 'alternativas': ['Descartes',
                                  'Hegel',
                                  'Aristóteles',
                                  'James',
                                  'Kant'],
                 'correcta': 'C'},
                {'pregunta': 'Para la teoría pragmática, es verdadero '
                             'aquello que:',
                 'alternativas': ['Resulta útil o funciona en la práctica',
                                  'Corresponde a la realidad',
                                  'Es revelado',
                                  'No se contradice',
                                  'Es evidente'],
                 'correcta': 'A'},
                {'pregunta': 'Según la teoría de la coherencia, un enunciado '
                             'es verdadero si:',
                 'alternativas': ['Es útil',
                                  'Se comprueba experimentalmente',
                                  'Lo dice una autoridad',
                                  'No contradice al sistema del que forma '
                                  'parte',
                                  'Es intuitivo'],
                 'correcta': 'D'},
                {'pregunta': 'Los tres elementos del conocimiento son '
                             'sujeto, objeto e:',
                 'alternativas': ['Interpretación',
                                  'Instrumento',
                                  'Método',
                                  'Imagen',
                                  'Interés'],
                 'correcta': 'D'},
                {'pregunta': 'La gnoseología estudia del conocimiento su '
                             'origen, su esencia y sus:',
                 'alternativas': ['Autores',
                                  'Instrumentos',
                                  'Límites',
                                  'Costos',
                                  'Aplicaciones'],
                 'correcta': 'C'},
                {'pregunta': 'Percibir el color rojo de una manzana '
                             'corresponde al conocimiento:',
                 'alternativas': ['Abstracto',
                                  'Deductivo',
                                  'Sensible',
                                  'Racional',
                                  'Científico'],
                 'correcta': 'C'},
                {'pregunta': 'Comprender el concepto de «justicia» '
                             'corresponde al conocimiento:',
                 'alternativas': ['Racional',
                                  'Empírico puro',
                                  'Sensible',
                                  'Instintivo',
                                  'Perceptivo'],
                 'correcta': 'A'},
                {'pregunta': 'En la relación cognoscitiva, aquello que es '
                             'conocido se denomina:',
                 'alternativas': ['Método',
                                  'Sujeto',
                                  'Fin',
                                  'Objeto',
                                  'Imagen'],
                 'correcta': 'D'},
                {'pregunta': 'La afirmación «la nieve es blanca es verdadera '
                             'si la nieve es blanca» ilustra la teoría de:',
                 'alternativas': ['El consenso',
                                  'La autoridad',
                                  'La coherencia',
                                  'La correspondencia',
                                  'El pragmatismo'],
                 'correcta': 'D'},
                {'pregunta': 'En gnoseología, la corriente que afirma que la '
                             'verdad está relacionada con la fe y la '
                             'espiritualidad es el: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Dogmatismo Religioso',
                                  'Fenomenalismo',
                                  'Escepticismo',
                                  'Dogmatismo Ingenuo',
                                  'Agnosticismo'],
                 'correcta': 'A'},
                {'pregunta': 'El conocimiento empírico lo adquirimos por '
                             'medio: (I CEPRU 2025)',
                 'alternativas': ['De la inferencia',
                                  'De la experiencia',
                                  'Del entendimiento',
                                  'De la razón',
                                  'Del proceso lógico'],
                 'correcta': 'B'},
                {'pregunta': 'Renato Descartes argumentó que el origen del '
                             'conocimiento válido sobre la realidad proviene '
                             'de la: (Primera Oportunidad UNSAAC 2023)',
                 'alternativas': ['Experiencia',
                                  'Sensación',
                                  'Práctica',
                                  'Percepción',
                                  'Razón'],
                 'correcta': 'E'},
                {'pregunta': 'En el problema del conocimiento, el '
                             'planteamiento materialista afirma que: '
                             '(Ordinario UNSAAC 2014-II)',
                 'alternativas': ['No se puede conocer las esencias',
                                  'No es posible el conocimiento objetivo',
                                  'Se conocen solo las apariencias',
                                  'El conocimiento es infinito e inagotable',
                                  'Nada existe, y si algo existe, no se '
                                  'puede conocer'],
                 'correcta': 'D'},
                {'pregunta': 'Afirmar que el destino del hombre está trazado '
                             'por una deidad superior, y que sin embargo, '
                             'mediante la razón y la voluntad puede acatar o '
                             'desacatar dichos designios, corresponde a: (I '
                             'CEPRU 2019-I)',
                 'alternativas': ['Providencialismo',
                                  'Negativismo',
                                  'Indeterminismo',
                                  'Fatalismo',
                                  'Espontaneísmo'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando la representación o imagen mental '
                             'coincide con la realidad objetiva, la verdad '
                             'se rige por la teoría: (I CEPRU 2019-I)',
                 'alternativas': ['Correspondencia',
                                  'Intuicionista',
                                  'Isomórfica',
                                  'Dialéctica',
                                  'Pragmática'],
                 'correcta': 'A'},
                {'pregunta': 'El proceso de conocer, acto de aprehensión, '
                             'necesita la presencia de: (II CEPRU 2019-I)',
                 'alternativas': ['Sujeto capaz e ideales abstractos',
                                  'Sujeto cognoscente y objeto cognoscible',
                                  'Validez cognitiva y solidez empírica',
                                  'Objetos cognoscibles e incognoscibles',
                                  'Sujeto valorante y objetivos estéticos'],
                 'correcta': 'B'},
                {'pregunta': 'Que las cosas no se creen ni se destruyan, '
                             'sino que solo se transformen, es un '
                             'planteamiento: (II CEPRU 2019-I)',
                 'alternativas': ['Materialista',
                                  'Criticista',
                                  'Relativista',
                                  'Agnosticista',
                                  'Idealista'],
                 'correcta': 'A'},
                {'pregunta': 'El conocimiento en su fase racional o lógica '
                             'implica: (II CEPRU 2018-II)',
                 'alternativas': ['Generalización, síntesis y abstracción',
                                  'Sensación, percepción e imagen',
                                  'Saber, conocer e intuir',
                                  'Científico, hipotético y riguroso',
                                  'Esencia, hipótesis y teoría'],
                 'correcta': 'A'},
                {'pregunta': 'En relación a las teorías de la verdad, la '
                             'tesis del materialismo marxista está asociada '
                             'a: (Banco UNSAAC)',
                 'alternativas': ['Realismo',
                                  'Agnosticismo',
                                  'Idealismo subjetivo',
                                  'Idealismo objetivo',
                                  'Fenomenalismo'],
                 'correcta': 'A'},
                {'pregunta': 'Según el determinismo del materialismo '
                             'dialéctico, la libertad consiste en la '
                             'conexión entre: (Banco UNSAAC)',
                 'alternativas': ['Necesidad natural e ideal',
                                  'Actividad humana, las leyes naturales y '
                                  'sociales',
                                  'Conducta y los actos del hombre',
                                  'Libre albedrío y libertad absoluta',
                                  'Voluntad y deseo del hombre'],
                 'correcta': 'B'},
                {'pregunta': 'Si el conocimiento humano parte de la '
                             'experiencia sensorial y se orienta hacia una '
                             'fase compleja de carácter teórico, esta última '
                             'fase implica: (Banco UNSAAC)',
                 'alternativas': ['Idealización filosófica',
                                  'Procesamiento lógico de la realidad',
                                  'Imaginación de una realidad',
                                  'Abstracción de un hecho',
                                  'Representación mental de una cosa'],
                 'correcta': 'D'}],
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
                                'sistema.']}],
  'qr_reto': [{'pregunta': 'La disciplina que estudia el conocimiento en '
                           'general se denomina:',
               'respuesta': 'Gnoseología'},
              {'pregunta': 'El conocimiento racional se caracteriza por ser:',
               'respuesta': 'Universal, abstracto y objetivo'},
              {'pregunta': 'En gnoseología, la corriente que afirma que la '
                           'verdad está relacionada con la fe y la '
                           'espiritualidad es el:',
               'respuesta': 'Dogmatismo Religioso'}],
  'qr_dato': 'En el acto de conocer, el sujeto sale de sí y aprehende las '
             'propiedades del objeto; el objeto permanece inalterado.'},
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
                 'alternativas': ['Escepticismo',
                                  'Relativismo',
                                  'Fenomenalismo',
                                  'Dogmatismo',
                                  'Criticismo'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo niega la posibilidad de '
                             'alcanzar:',
                 'alternativas': ['El lenguaje',
                                  'La razón',
                                  'Un conocimiento seguro',
                                  'La experiencia',
                                  'La percepción'],
                 'correcta': 'C'},
                {'pregunta': 'El representante clásico del escepticismo es:',
                 'alternativas': ['Berkeley',
                                  'Pirrón de Elis',
                                  'Descartes',
                                  'Locke',
                                  'Kant'],
                 'correcta': 'B'},
                {'pregunta': 'La posición intermedia que afirma que el '
                             'conocimiento es posible pero con límites es '
                             'el:',
                 'alternativas': ['Empirismo',
                                  'Escepticismo',
                                  'Criticismo',
                                  'Dogmatismo',
                                  'Idealismo'],
                 'correcta': 'C'},
                {'pregunta': 'El criticismo fue formulado por:',
                 'alternativas': ['Descartes',
                                  'Pirrón',
                                  'Hume',
                                  'Kant',
                                  'Hegel'],
                 'correcta': 'D'},
                {'pregunta': 'Para el racionalismo, el origen del '
                             'conocimiento es:',
                 'alternativas': ['La razón',
                                  'La revelación',
                                  'La costumbre',
                                  'La experiencia',
                                  'La percepción'],
                 'correcta': 'A'},
                {'pregunta': 'El principal representante del empirismo es:',
                 'alternativas': ['Hegel',
                                  'Platón',
                                  'Kant',
                                  'John Locke',
                                  'Descartes'],
                 'correcta': 'D'},
                {'pregunta': '«Los conceptos sin intuiciones son vacíos, las '
                             'intuiciones sin conceptos son ciegas» '
                             'corresponde a:',
                 'alternativas': ['Kant',
                                  'Hume',
                                  'Locke',
                                  'Descartes',
                                  'Berkeley'],
                 'correcta': 'A'},
                {'pregunta': 'La frase «ser es ser percibido» pertenece a:',
                 'alternativas': ['Berkeley',
                                  'Hume',
                                  'Kant',
                                  'Platón',
                                  'Descartes'],
                 'correcta': 'A'},
                {'pregunta': 'El idealismo subjetivo sostiene que la '
                             'realidad depende de:',
                 'alternativas': ['La sociedad',
                                  'La conciencia del sujeto',
                                  'La materia',
                                  'El lenguaje',
                                  'Las leyes físicas'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo objetivo afirma que existe una '
                             'realidad ideal:',
                 'alternativas': ['Independiente del sujeto',
                                  'Inexistente',
                                  'Sensorial',
                                  'Puramente material',
                                  'Creada por el sujeto'],
                 'correcta': 'A'},
                {'pregunta': 'Las Ideas de Platón y el Espíritu de Hegel son '
                             'ejemplos de:',
                 'alternativas': ['Escepticismo',
                                  'Materialismo',
                                  'Empirismo',
                                  'Idealismo objetivo',
                                  'Idealismo subjetivo'],
                 'correcta': 'D'},
                {'pregunta': 'El materialismo sostiene que lo primario es:',
                 'alternativas': ['La idea',
                                  'El lenguaje',
                                  'La conciencia',
                                  'La materia',
                                  'El espíritu'],
                 'correcta': 'D'},
                {'pregunta': 'El fenomenalismo sostiene que solo conocemos:',
                 'alternativas': ['La cosa en sí',
                                  'El noúmeno',
                                  'Los fenómenos',
                                  'La esencia',
                                  'Las ideas innatas'],
                 'correcta': 'C'},
                {'pregunta': 'El escepticismo que niega toda posibilidad de '
                             'conocer se denomina:',
                 'alternativas': ['Metódico',
                                  'Absoluto',
                                  'Parcial',
                                  'Relativo',
                                  'Moderado'],
                 'correcta': 'B'},
                {'pregunta': 'El problema de la POSIBILIDAD del conocimiento '
                             'se pregunta si:',
                 'alternativas': ['Cuál es la esencia del ser',
                                  'De dónde proviene el conocimiento',
                                  'Si es posible conocer con certeza',
                                  'Qué es la verdad',
                                  'Para qué sirve el saber'],
                 'correcta': 'C'},
                {'pregunta': 'El problema del ORIGEN del conocimiento se '
                             'pregunta:',
                 'alternativas': ['Cuál es el fin del hombre',
                                  'Qué es lo real',
                                  'De dónde proviene el conocimiento',
                                  'Qué es el valor',
                                  'Si es posible conocer'],
                 'correcta': 'C'},
                {'pregunta': 'Descartes es representante del:',
                 'alternativas': ['Fenomenalismo',
                                  'Materialismo',
                                  'Escepticismo absoluto',
                                  'Racionalismo',
                                  'Empirismo'],
                 'correcta': 'D'},
                {'pregunta': 'El criticismo kantiano supera la oposición '
                             'entre:',
                 'alternativas': ['Dogmatismo y realismo',
                                  'Ciencia y religión',
                                  'Idealismo y materialismo',
                                  'Ética y lógica',
                                  'Racionalismo y empirismo'],
                 'correcta': 'E'},
                {'pregunta': 'Para el materialismo, la conciencia es:',
                 'alternativas': ['Lo primario',
                                  'Anterior al mundo',
                                  'Independiente del cerebro',
                                  'Un producto de la materia',
                                  'Una sustancia separada'],
                 'correcta': 'D'},
                {'pregunta': 'La corriente que sostiene que la experiencia '
                             'es la única fuente del conocimiento se llama:',
                 'alternativas': ['Criticismo',
                                  'Racionalismo',
                                  'Empirismo',
                                  'Idealismo',
                                  'Dogmatismo'],
                 'correcta': 'C'},
                {'pregunta': 'El método propio del empirismo es:',
                 'alternativas': ['La analogía',
                                  'La deducción',
                                  'La inducción',
                                  'La intuición exclusiva',
                                  'La dialéctica'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los representantes del empirismo figuran '
                             'Locke, Hume, Berkeley y:',
                 'alternativas': ['Descartes',
                                  'Malebranche',
                                  'Spinoza',
                                  'Leibniz',
                                  'Francisco Bacon'],
                 'correcta': 'E'},
                {'pregunta': 'La corriente que sostiene que la razón es la '
                             'única fuente del conocimiento se llama:',
                 'alternativas': ['Fenomenalismo',
                                  'Agnosticismo',
                                  'Escepticismo',
                                  'Empirismo',
                                  'Racionalismo'],
                 'correcta': 'E'},
                {'pregunta': 'El método propio del racionalismo es:',
                 'alternativas': ['El experimento exclusivo',
                                  'La deducción',
                                  'La intuición sensible',
                                  'La observación exclusiva',
                                  'La inducción'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los representantes del racionalismo '
                             'figuran Descartes, Spinoza y:',
                 'alternativas': ['Locke',
                                  'Berkeley',
                                  'Bacon',
                                  'Hume',
                                  'Leibniz'],
                 'correcta': 'E'},
                {'pregunta': 'La corriente que sostiene que el conocimiento '
                             'surge de la unión de experiencia y razón se '
                             'llama:',
                 'alternativas': ['Escepticismo',
                                  'Dogmatismo',
                                  'Racionalismo puro',
                                  'Empirismo',
                                  'Criticismo'],
                 'correcta': 'E'},
                {'pregunta': 'El representante del criticismo, autor de la '
                             'frase «no hay experiencia sin razón ni razón '
                             'sin experiencia», fue:',
                 'alternativas': ['Manuel Kant',
                                  'Descartes',
                                  'Hume',
                                  'Locke',
                                  'Hegel'],
                 'correcta': 'A'},
                {'pregunta': 'La postura que admite que el conocimiento sí '
                             'es posible se llama:',
                 'alternativas': ['Fenomenalismo',
                                  'Escepticismo',
                                  'Dogmatismo',
                                  'Idealismo',
                                  'Agnosticismo'],
                 'correcta': 'C'},
                {'pregunta': 'Los representantes del dogmatismo, según el '
                             'texto, fueron los:',
                 'alternativas': ['Presocráticos',
                                  'Sofistas',
                                  'Escolásticos',
                                  'Estoicos',
                                  'Positivistas'],
                 'correcta': 'A'},
                {'pregunta': 'El fundador del escepticismo, quien afirmaba '
                             'que el conocimiento no es posible, fue:',
                 'alternativas': ['Demócrito',
                                  'Sócrates',
                                  'Protágoras',
                                  'Pirrón de Elis',
                                  'Gorgias'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo radical o absoluto, que afirma '
                             'que el conocimiento es imposible, tiene como '
                             'representante a:',
                 'alternativas': ['Pirrón',
                                  'Gorgias',
                                  'Platón',
                                  'Sócrates',
                                  'Protágoras'],
                 'correcta': 'B'},
                {'pregunta': 'El escepticismo relativo, que afirma que toda '
                             'verdad es relativa, tiene como representante '
                             'a:',
                 'alternativas': ['Heráclito',
                                  'Pirrón',
                                  'Gorgias',
                                  'Protágoras',
                                  'Demócrito'],
                 'correcta': 'D'},
                {'pregunta': 'La postura que admite la imposibilidad de '
                             'conocer la «cosa en sí» se llama:',
                 'alternativas': ['Agnosticismo',
                                  'Idealismo objetivo',
                                  'Materialismo',
                                  'Dogmatismo',
                                  'Escepticismo radical'],
                 'correcta': 'A'},
                {'pregunta': 'El representante del agnosticismo, según el '
                             'texto, fue:',
                 'alternativas': ['Berkeley',
                                  'Manuel Kant',
                                  'Gorgias',
                                  'Protágoras',
                                  'Pirrón'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que sostiene que el objeto del '
                             'conocimiento no es real sino ideal se llama:',
                 'alternativas': ['Materialismo',
                                  'Idealismo',
                                  'Dogmatismo',
                                  'Empirismo',
                                  'Fenomenalismo'],
                 'correcta': 'B'},
                {'pregunta': 'El idealismo subjetivo, que afirma que toda '
                             'realidad está encerrada en la conciencia, '
                             'tiene como representante a:',
                 'alternativas': ['Berkeley',
                                  'Hegel',
                                  'Kant',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'A'},
                {'pregunta': 'El idealismo objetivo, que sostiene que las '
                             'ideas existen por sí mismas, tiene como '
                             'representantes a Platón y:',
                 'alternativas': ['Hegel',
                                  'Descartes',
                                  'Berkeley',
                                  'Kant',
                                  'Locke'],
                 'correcta': 'A'},
                {'pregunta': 'El materialismo sostiene que el criterio de '
                             'verdad del conocimiento es:',
                 'alternativas': ['La autoridad',
                                  'La praxis',
                                  'La revelación',
                                  'La fe',
                                  'La intuición'],
                 'correcta': 'B'},
                {'pregunta': 'El fenomenalismo sostiene que el sujeto solo '
                             'puede captar el fenómeno, mas no:',
                 'alternativas': ['La experiencia',
                                  'La apariencia',
                                  'El lenguaje',
                                  'La esencia o noúmeno',
                                  'Los sentidos'],
                 'correcta': 'D'},
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
                 'alternativas': ['Estoicos',
                                  'Escépticos',
                                  'Sofistas',
                                  'Presocráticos',
                                  'Positivistas'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo radical o absoluto, que niega '
                             'toda posibilidad de conocer, está representado '
                             'por:',
                 'alternativas': ['Sócrates',
                                  'Protágoras',
                                  'Pirrón',
                                  'Gorgias',
                                  'Platón'],
                 'correcta': 'D'},
                {'pregunta': 'El escepticismo relativo, que sostiene que '
                             'toda verdad es relativa, está representado '
                             'por:',
                 'alternativas': ['Gorgias',
                                  'Demócrito',
                                  'Protágoras',
                                  'Heráclito',
                                  'Pirrón'],
                 'correcta': 'C'},
                {'pregunta': 'Además del criticismo, la imposibilidad de '
                             'conocer la «cosa en sí» también es sostenida, '
                             'bajo el nombre de agnosticismo, por:',
                 'alternativas': ['Descartes',
                                  'Hume',
                                  'Berkeley',
                                  'Kant',
                                  'Locke'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los representantes del racionalismo, '
                             'además de Descartes, figuran Leibniz, Spinoza '
                             'y:',
                 'alternativas': ['Hume',
                                  'Berkeley',
                                  'Bacon',
                                  'Malebranche',
                                  'Locke'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los representantes del empirismo, además '
                             'de Locke y Hume, figuran Bacon y:',
                 'alternativas': ['Leibniz',
                                  'Descartes',
                                  'Berkeley',
                                  'Malebranche',
                                  'Spinoza'],
                 'correcta': 'C'},
                {'pregunta': 'Para el materialismo, el criterio de verdad '
                             'del conocimiento es:',
                 'alternativas': ['La praxis',
                                  'La fe',
                                  'La revelación',
                                  'La autoridad',
                                  'La intuición'],
                 'correcta': 'A'},
                {'pregunta': 'El representante del fenomenalismo, que '
                             'sostiene que solo conocemos los fenómenos, es:',
                 'alternativas': ['Platón',
                                  'Hegel',
                                  'Locke',
                                  'Kant',
                                  'Berkeley'],
                 'correcta': 'D'},
                {'pregunta': 'John Locke, en cuanto al origen del '
                             'conocimiento, es representante del: (I CEPRU '
                             '2019-I)',
                 'alternativas': ['Criticismo',
                                  'Empirismo',
                                  'Escepticismo',
                                  'Materialismo',
                                  'Agnosticismo'],
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
                                'con límites.',
                                'El agnosticismo, sostenido también por '
                                'Kant, admite la imposibilidad de conocer la '
                                '«cosa en sí».']},
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
                                'representante: Kant.']}],
  'qr_reto': [{'pregunta': 'Entre los representantes del racionalismo '
                           'figuran Descartes, Spinoza y:',
               'respuesta': 'Leibniz'},
              {'pregunta': 'El escepticismo relativo, que afirma que toda '
                           'verdad es relativa, tiene como representante a:',
               'respuesta': 'Protágoras'},
              {'pregunta': 'El criticismo fue formulado por:',
               'respuesta': 'Kant'}],
  'qr_dato': 'Empirismo: el origen es la experiencia; su método es la '
             'inducción. Representantes: Locke, Hume, Bacon y Berkeley.'},
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
                 'alternativas': ['Ontología',
                                  'Axiología',
                                  'Epistemología',
                                  'Lógica',
                                  'Gnoseología'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, «episteme» significa:',
                 'alternativas': ['Valor',
                                  'Palabra',
                                  'Alma',
                                  'Ciencia',
                                  'Ser'],
                 'correcta': 'D'},
                {'pregunta': 'La diferencia entre gnoseología y '
                             'epistemología es que la primera estudia:',
                 'alternativas': ['La conducta',
                                  'El lenguaje',
                                  'Los valores',
                                  'El conocimiento en general',
                                  'Solo la ciencia'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto sistemático de leyes e hipótesis '
                             'que explican un ámbito de la realidad es:',
                 'alternativas': ['Una teoría científica',
                                  'Una hipótesis',
                                  'Un dato',
                                  'Una observación',
                                  'Un axioma'],
                 'correcta': 'A'},
                {'pregunta': 'El enunciado que expresa una relación '
                             'constante y necesaria entre fenómenos es:',
                 'alternativas': ['La conjetura',
                                  'La hipótesis',
                                  'El axioma',
                                  'El postulado',
                                  'La ley científica'],
                 'correcta': 'E'},
                {'pregunta': 'La suposición provisional que debe ser '
                             'contrastada se denomina:',
                 'alternativas': ['Ley',
                                  'Hipótesis',
                                  'Axioma',
                                  'Teoría',
                                  'Corolario'],
                 'correcta': 'B'},
                {'pregunta': 'La proposición evidente que se acepta sin '
                             'demostración es:',
                 'alternativas': ['La ley',
                                  'El axioma',
                                  'La hipótesis',
                                  'La teoría',
                                  'El teorema'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo particular a lo general '
                             'es:',
                 'alternativas': ['Hermenéutico',
                                  'Inductivo',
                                  'Analógico',
                                  'Dialéctico',
                                  'Deductivo'],
                 'correcta': 'B'},
                {'pregunta': 'El método que va de lo general a lo particular '
                             'es:',
                 'alternativas': ['Comparativo',
                                  'Estadístico',
                                  'Deductivo',
                                  'Analógico',
                                  'Inductivo'],
                 'correcta': 'C'},
                {'pregunta': 'El método general de la ciencia moderna se '
                             'denomina:',
                 'alternativas': ['Intuitivo',
                                  'Hipotético-deductivo',
                                  'Escolástico',
                                  'Dialéctico',
                                  'Fenomenológico'],
                 'correcta': 'B'},
                {'pregunta': 'NO es una función de la ciencia:',
                 'alternativas': ['Dogmatizar',
                                  'Predecir',
                                  'Describir',
                                  'Explicar',
                                  'Sistematizar'],
                 'correcta': 'A'},
                {'pregunta': 'Mario Bunge clasificó las ciencias en formales '
                             'y:',
                 'alternativas': ['Humanas',
                                  'Exactas',
                                  'Puras',
                                  'Aplicadas',
                                  'Fácticas'],
                 'correcta': 'E'},
                {'pregunta': 'Las ciencias formales tienen como objeto de '
                             'estudio entes:',
                 'alternativas': ['Reales',
                                  'Naturales',
                                  'Ideales',
                                  'Materiales',
                                  'Sociales'],
                 'correcta': 'C'},
                {'pregunta': 'Son ciencias formales:',
                 'alternativas': ['Lógica y matemática',
                                  'Psicología y sociología',
                                  'Historia y economía',
                                  'Biología y geología',
                                  'Física y química'],
                 'correcta': 'A'},
                {'pregunta': 'La biología pertenece a las ciencias:',
                 'alternativas': ['Fácticas sociales',
                                  'Formales',
                                  'Aplicadas exclusivamente',
                                  'Fácticas naturales',
                                  'Ideales'],
                 'correcta': 'D'},
                {'pregunta': 'La historia y la economía pertenecen a las '
                             'ciencias:',
                 'alternativas': ['Puras',
                                  'Exactas',
                                  'Fácticas sociales',
                                  'Fácticas naturales',
                                  'Formales'],
                 'correcta': 'C'},
                {'pregunta': 'El primer paso del método científico es:',
                 'alternativas': ['La experimentación',
                                  'La conclusión',
                                  'La hipótesis',
                                  'La observación',
                                  'La ley'],
                 'correcta': 'D'},
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
                 'alternativas': ['Normativa',
                                  'Predictiva',
                                  'Descriptiva',
                                  'Explicativa',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciencias fácticas se caracterizan porque '
                             'su objeto es:',
                 'alternativas': ['Ideal',
                                  'Formal',
                                  'Real',
                                  'Abstracto puro',
                                  'Simbólico'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ciencia investigue solo una clase '
                             'determinada de objetos corresponde a la '
                             'característica de ser:',
                 'alternativas': ['Falible',
                                  'Sistemática',
                                  'Especializada',
                                  'Universal',
                                  'Predictiva'],
                 'correcta': 'C'},
                {'pregunta': 'Que el proceder de la ciencia responda a un '
                             'plan organizado corresponde a que es:',
                 'alternativas': ['Falsacionista',
                                  'Experimental',
                                  'Objetiva',
                                  'Metódica',
                                  'Explicativa'],
                 'correcta': 'D'},
                {'pregunta': 'Que los conocimientos científicos formen un '
                             'sistema articulado corresponde a que la '
                             'ciencia es:',
                 'alternativas': ['Sistemática',
                                  'Predictiva',
                                  'Universal',
                                  'Especializada',
                                  'Contrastable'],
                 'correcta': 'A'},
                {'pregunta': 'Que la ciencia busque reflejar la realidad tal '
                             'cual es corresponde a que es:',
                 'alternativas': ['Metódica',
                                  'Sistemática',
                                  'Objetiva',
                                  'Especializada',
                                  'Falible'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ciencia busque responder al porqué de '
                             'las cosas corresponde a que es:',
                 'alternativas': ['Universal',
                                  'Explicativa',
                                  'Predictiva',
                                  'Falible',
                                  'Experimental'],
                 'correcta': 'B'},
                {'pregunta': 'Que la ciencia pueda probarse y comprobarse '
                             'cuantas veces sea necesario corresponde a que '
                             'es:',
                 'alternativas': ['Metódica',
                                  'Sistemática',
                                  'Experimental',
                                  'Objetiva',
                                  'Explicativa'],
                 'correcta': 'C'},
                {'pregunta': 'Que la ciencia sea válida para todos los '
                             'hombres corresponde a que es:',
                 'alternativas': ['Predictiva',
                                  'Universal',
                                  'Falible',
                                  'Especializada',
                                  'Contrastable'],
                 'correcta': 'B'},
                {'pregunta': 'Que la ciencia sea pasible de error, aunque '
                             'perfectible, corresponde a que es:',
                 'alternativas': ['Universal',
                                  'Falible',
                                  'Objetiva',
                                  'Sistemática',
                                  'Metódica'],
                 'correcta': 'B'},
                {'pregunta': 'Que una hipótesis pueda demostrarse verdadera '
                             'también por su falsedad corresponde a que la '
                             'ciencia es:',
                 'alternativas': ['Predictiva',
                                  'Universal',
                                  'Objetiva',
                                  'Falsacionista',
                                  'Explicativa'],
                 'correcta': 'D'},
                {'pregunta': 'Que la ciencia prevea situaciones futuras a '
                             'partir de leyes o teorías corresponde a que '
                             'es:',
                 'alternativas': ['Predictiva',
                                  'Experimental',
                                  'Sistemática',
                                  'Falsacionista',
                                  'Metódica'],
                 'correcta': 'A'},
                {'pregunta': 'Que toda teoría científica esté sometida a '
                             'prueba para confirmarla o debilitarla '
                             'corresponde a que la ciencia tiene:',
                 'alternativas': ['Especialización',
                                  'Universalidad',
                                  'Sistematicidad',
                                  'Objetividad',
                                  'Contrastación o refutabilidad'],
                 'correcta': 'E'},
                {'pregunta': 'Según Mario Bunge, las ciencias se clasifican '
                             'en: (Primera Oportunidad UNSAAC 2023)',
                 'alternativas': ['Fácticas y ambientales',
                                  'Formales e informales',
                                  'Sociales y económicas',
                                  'Formales y fácticas',
                                  'Fácticas y virtuales'],
                 'correcta': 'D'},
                {'pregunta': 'Precisar cómo se manifiesta el hecho o '
                             'fenómeno, respondiendo a la pregunta ¿Cómo '
                             'es?, corresponde a la: (I CEPRU 2019-I)',
                 'alternativas': ['Demostración',
                                  'Predicción',
                                  'Descripción',
                                  'Explicación',
                                  'Discriminación'],
                 'correcta': 'C'},
                {'pregunta': 'La Lógica y la Matemática, por un lado, y la '
                             'Política y el Derecho, por otro, según la '
                             'clasificación de Mario Bunge, son ciencias: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Sociales - Naturales',
                                  'Axiomáticas - Sociales',
                                  'Fácticas - Experimentales',
                                  'Nomotéticas - Formales',
                                  'Formales - Fácticas'],
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
                                'sociología).']}],
  'qr_reto': [{'pregunta': 'Mario Bunge clasificó las ciencias en formales '
                           'y:',
               'respuesta': 'Fácticas'},
              {'pregunta': 'La disciplina que estudia el conocimiento '
                           'científico es la:',
               'respuesta': 'Epistemología'},
              {'pregunta': 'Que la ciencia busque reflejar la realidad tal '
                           'cual es corresponde a que es:',
               'respuesta': 'Objetiva'}],
  'qr_dato': 'Ley científica: enunciado que expresa una relación constante y '
             'necesaria entre fenómenos.'},
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
                {'titulo': '9.3 CLASIFICACIÓN DE LOS VALORES SEGÚN MAX '
                           'SCHELER',
                 'items': ['Valores {sensibles} (sensorial-hedonísticos): '
                           'ponen en juego los sentidos; ejemplo, '
                           'agradable-{doloroso}.',
                           'Valores {vitales}: relacionados a la vida y la '
                           'salud; ejemplo, sano-{enfermo}.',
                           'Valores {lógicos}: se traducen en las '
                           'ideologías, ideas, criterios y la {verdad}.',
                           'Valores {estéticos}: relacionados con la belleza '
                           'y el arte; ejemplo, bello-{feo}.',
                           'Valores ético-{morales}: relacionados con el '
                           'bien y la virtud; ejemplo, correcto-incorrecto.',
                           'Valores {religiosos}: relacionados con la fe y '
                           'creencia; ejemplo, lo terrenal, {beato}, '
                           'profano.',
                           'Valores teóricos-{cognoscitivos}: relacionados '
                           'con el conocimiento; ejemplo, verdadero-falso.',
                           'Valores económico-{técnicos}: relacionados con '
                           'la utilidad y ganancias; ejemplo, caro-{barato}.',
                           'Valores social-{jurídicos}: relacionados con la '
                           'realidad social y la justicia; ejemplo, '
                           '{igualdad}, orden.',
                           'Valores {políticos}: relacionados con la '
                           'búsqueda del poder; ejemplo, orden, {bienestar}.',
                           'Valores {históricos}: relacionados con los '
                           'acontecimientos históricos; ejemplo, '
                           '{heroísmo}.']},
                {'titulo': '9.4 TEORÍAS DEL VALOR',
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
                {'titulo': '9.5 LA ÉTICA Y LA MORAL',
                 'items': ['La {ética} es la disciplina filosófica que '
                           'reflexiona sobre la {moral}; es teórica.',
                           'La {moral} es el conjunto de normas y costumbres '
                           'concretas de una sociedad; es {práctica}.',
                           'Corrientes éticas: el {eudemonismo} de '
                           '{Aristóteles} (el fin es la {felicidad}), la '
                           'ética {kantiana} del deber, y el {utilitarismo} '
                           'de Stuart {Mill} (la mayor felicidad para el '
                           'mayor {número}).']},
                {'titulo': '9.6 EL PROBLEMA DE LA CONDUCTA MORALMENTE BUENA',
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
                {'titulo': '9.7 LA PERSONA MORAL Y LA SANCIÓN',
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
                                  'Axiología',
                                  'Ontología',
                                  'Ética',
                                  'Estética'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «axios» significa:',
                 'alternativas': ['Valor', 'Bien', 'Costumbre', 'Fin', 'Ley'],
                 'correcta': 'A'},
                {'pregunta': 'Que todo valor tenga su contravalor '
                             'corresponde a la característica de:',
                 'alternativas': ['Jerarquía',
                                  'Materia',
                                  'Objetividad',
                                  'Polaridad',
                                  'Historicidad'],
                 'correcta': 'D'},
                {'pregunta': 'Que unos valores valgan más que otros '
                             'corresponde a la característica de:',
                 'alternativas': ['Relatividad',
                                  'Polaridad',
                                  'Subjetividad',
                                  'Jerarquía',
                                  'Universalidad'],
                 'correcta': 'D'},
                {'pregunta': 'La jerarquía de valores en sensibles, vitales, '
                             'espirituales y religiosos fue propuesta por:',
                 'alternativas': ['Kant',
                                  'Aristóteles',
                                  'Stuart Mill',
                                  'Nietzsche',
                                  'Max Scheler'],
                 'correcta': 'E'},
                {'pregunta': 'Para el subjetivismo, el valor depende de:',
                 'alternativas': ['El objeto',
                                  'El sujeto que valora',
                                  'La razón pura',
                                  'La sociedad',
                                  'Dios'],
                 'correcta': 'B'},
                {'pregunta': 'Para el objetivismo, los valores:',
                 'alternativas': ['No existen',
                                  'Existen independientemente del sujeto',
                                  'Son ilusiones',
                                  'Los crea el sujeto',
                                  'Varían con la moda'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría según la cual el valor surge de la '
                             'relación entre sujeto y objeto es el:',
                 'alternativas': ['Nihilismo',
                                  'Relacionismo',
                                  'Formalismo',
                                  'Objetivismo',
                                  'Subjetivismo'],
                 'correcta': 'B'},
                {'pregunta': 'El socioculturalismo sostiene que los valores '
                             'son producto de:',
                 'alternativas': ['La sociedad y la cultura',
                                  'El azar',
                                  'La naturaleza biológica',
                                  'La revelación',
                                  'La razón individual'],
                 'correcta': 'A'},
                {'pregunta': 'La disciplina filosófica que reflexiona '
                             'teóricamente sobre la moral es la:',
                 'alternativas': ['Ética',
                                  'Moral',
                                  'Política',
                                  'Estética',
                                  'Axiología'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto de normas y costumbres concretas '
                             'de una sociedad constituye la:',
                 'alternativas': ['Ciencia',
                                  'Estética',
                                  'Ética',
                                  'Lógica',
                                  'Moral'],
                 'correcta': 'E'},
                {'pregunta': 'La diferencia entre ética y moral es que la '
                             'ética es:',
                 'alternativas': ['Legal',
                                  'Práctica y la moral teórica',
                                  'Teórica y la moral práctica',
                                  'Estética',
                                  'Religiosa'],
                 'correcta': 'C'},
                {'pregunta': 'El eudemonismo, que sitúa el fin de la vida en '
                             'la felicidad, corresponde a:',
                 'alternativas': ['Epicuro',
                                  'Aristóteles',
                                  'Kant',
                                  'Nietzsche',
                                  'Stuart Mill'],
                 'correcta': 'B'},
                {'pregunta': 'La ética del deber fue formulada por:',
                 'alternativas': ['Aristóteles',
                                  'Mill',
                                  'Kant',
                                  'Scheler',
                                  'Bentham'],
                 'correcta': 'C'},
                {'pregunta': 'El utilitarismo, que busca la mayor felicidad '
                             'para el mayor número, se asocia a:',
                 'alternativas': ['Sócrates',
                                  'Stuart Mill',
                                  'Kant',
                                  'Platón',
                                  'Aristóteles'],
                 'correcta': 'B'},
                {'pregunta': 'NO es un valor ético fundamental:',
                 'alternativas': ['La dignidad',
                                  'La rentabilidad',
                                  'El bien',
                                  'La solidaridad',
                                  'La justicia'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso por el cual el sujeto atribuye un '
                             'valor a algo se denomina:',
                 'alternativas': ['Percepción',
                                  'Deducción',
                                  'Juicio lógico',
                                  'Inferencia',
                                  'Acto valorativo'],
                 'correcta': 'E'},
                {'pregunta': 'En la jerarquía de Scheler, el valor más alto '
                             'corresponde a los valores:',
                 'alternativas': ['Sensibles',
                                  'Útiles',
                                  'Económicos',
                                  'Vitales',
                                  'Religiosos'],
                 'correcta': 'E'},
                {'pregunta': 'Para Kant, una acción es moralmente valiosa '
                             'cuando se realiza:',
                 'alternativas': ['Por costumbre',
                                  'Por placer',
                                  'Por interés',
                                  'Por miedo',
                                  'Por deber'],
                 'correcta': 'E'},
                {'pregunta': 'La afirmación «los valores cambian según la '
                             'época y la cultura» corresponde al:',
                 'alternativas': ['Socioculturalismo',
                                  'Formalismo',
                                  'Absolutismo moral',
                                  'Objetivismo',
                                  'Racionalismo'],
                 'correcta': 'A'},
                {'pregunta': 'El hedonismo de Epicuro sostiene que el bien y '
                             'el fin supremo de la vida humana es:',
                 'alternativas': ['El deber',
                                  'El poder',
                                  'La felicidad social',
                                  'El placer',
                                  'La razón pura'],
                 'correcta': 'D'},
                {'pregunta': 'A diferencia de Epicuro, el filósofo que solo '
                             'consideraba los placeres puramente sensibles '
                             'fue:',
                 'alternativas': ['Aristóteles',
                                  'Sócrates',
                                  'Kant',
                                  'Platón',
                                  'Aristipo de Cirene'],
                 'correcta': 'E'},
                {'pregunta': 'El eudemonismo de Aristóteles pregona como '
                             'meta suprema de la actividad moral:',
                 'alternativas': ['El placer',
                                  'El deber',
                                  'La utilidad',
                                  'El poder',
                                  'La felicidad'],
                 'correcta': 'E'},
                {'pregunta': 'Según Aristóteles, la virtud es el equilibrio '
                             'entre dos extremos, conocido como la ley:',
                 'alternativas': ['Del mayor bien',
                                  'Del término medio',
                                  'Del imperativo',
                                  'Del deber',
                                  'De la utilidad'],
                 'correcta': 'B'},
                {'pregunta': 'Entre la temeridad y la cobardía, la virtud '
                             'según Aristóteles sería:',
                 'alternativas': ['La templanza',
                                  'La prudencia',
                                  'La fortaleza',
                                  'La valentía',
                                  'La justicia'],
                 'correcta': 'D'},
                {'pregunta': 'El pensador cristiano que, junto con San '
                             'Agustín, situó la contemplación de Dios como '
                             'felicidad suprema fue:',
                 'alternativas': ['Bentham',
                                  'Aristóteles',
                                  'Santo Tomás de Aquino',
                                  'Epicuro',
                                  'Kant'],
                 'correcta': 'C'},
                {'pregunta': 'El utilitarismo sostiene que una acción es '
                             'moral si:',
                 'alternativas': ['Es útil, es decir, produce felicidad',
                                  'Cumple con el deber',
                                  'Sigue la tradición',
                                  'Obedece a la autoridad',
                                  'Busca el placer individual'],
                 'correcta': 'A'},
                {'pregunta': 'Los principales representantes del '
                             'utilitarismo son Jeremy Bentham y:',
                 'alternativas': ['Aristóteles',
                                  'John Stuart Mill',
                                  'San Agustín',
                                  'Immanuel Kant',
                                  'Epicuro'],
                 'correcta': 'B'},
                {'pregunta': 'El utilitarismo defiende la utilidad pública, '
                             'es decir, la mayor felicidad para:',
                 'alternativas': ['El gobernante',
                                  'Una sola clase social',
                                  'La clase dominante',
                                  'El individuo exclusivamente',
                                  'El mayor número de personas'],
                 'correcta': 'E'},
                {'pregunta': 'El formalismo ético, representado por Kant, '
                             'sostiene que la moral debe establecer:',
                 'alternativas': ['La felicidad social exclusivamente',
                                  'Normas concretas de conducta',
                                  'El placer como fin',
                                  'Solo el bien individual',
                                  'La forma que toda norma moral debe tener'],
                 'correcta': 'E'},
                {'pregunta': 'Según Kant, la norma moral se expresa '
                             'mediante:',
                 'alternativas': ['Leyes civiles',
                                  'Imperativos categóricos',
                                  'Costumbres sociales',
                                  'Silogismos morales',
                                  'Imperativos hipotéticos'],
                 'correcta': 'B'},
                {'pregunta': 'El imperativo categórico de Kant establece: '
                             'obra de tal modo que tu acción pueda '
                             'convertirse en:',
                 'alternativas': ['Costumbre social',
                                  'Norma jurídica',
                                  'Ley universal',
                                  'Ley personal',
                                  'Placer compartido'],
                 'correcta': 'C'},
                {'pregunta': 'El sujeto con conciencia de sus actos, capaz '
                             'de crear valores y conducir su existencia '
                             'según principios, se llama:',
                 'alternativas': ['Agente neutro',
                                  'Sujeto moral pasivo',
                                  'Persona',
                                  'Ente',
                                  'Individuo'],
                 'correcta': 'C'},
                {'pregunta': 'El ser sin conciencia de sus actos, que '
                             'gobierna su existencia por instintos, se '
                             'llama:',
                 'alternativas': ['Sujeto moral',
                                  'Agente racional',
                                  'Individuo',
                                  'Ciudadano',
                                  'Persona'],
                 'correcta': 'C'},
                {'pregunta': 'El castigo interno, subjetivo, que recibe una '
                             'persona por una acción negativa, expresado '
                             'como remordimiento, se llama:',
                 'alternativas': ['Condena social',
                                  'Pena civil',
                                  'Multa',
                                  'Sanción moral',
                                  'Sanción jurídica'],
                 'correcta': 'D'},
                {'pregunta': 'La pena impuesta por el Estado a quien viola '
                             'una ley, regulada por los tribunales, se '
                             'llama:',
                 'alternativas': ['Autocrítica',
                                  'Sanción jurídica',
                                  'Sanción moral',
                                  'Culpa subjetiva',
                                  'Remordimiento'],
                 'correcta': 'B'},
                {'pregunta': 'Las características del valor son: (Banco '
                             'UNSAAC 2025)',
                 'alternativas': ['Veracidad y sensualidad',
                                  'Integridad e intuición',
                                  'Polaridad y jerarquía',
                                  'Subjetividad y selectividad',
                                  'Grado y metodicidad'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría del valor que consiste en la '
                             'dependencia de los valores respecto al sujeto '
                             'se llama: (I CEPRU 2023)',
                 'alternativas': ['Relacionismo',
                                  'Subjetivismo',
                                  'Escepticismo',
                                  'Objetivismo',
                                  'Naturalismo'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina filosófica que estudia el '
                             'problema del valor es la: (Primera Oportunidad '
                             'UNSAAC 2023)',
                 'alternativas': ['Axiología',
                                  'Estética',
                                  'Ética',
                                  'Ontología',
                                  'Gnoseología'],
                 'correcta': 'A'},
                {'pregunta': 'En el problema axiológico, la jerarquización '
                             'significa: (Ordinario UNSAAC 2014-II)',
                 'alternativas': ['Reconocer mayor importancia de un valor '
                                  'sobre los demás',
                                  'Los valores se encuentran en los objetos',
                                  'Los valores se presentan en su polaridad',
                                  'Los valores son subjetivos',
                                  'El sujeto reconoce y aprecia los objetos'],
                 'correcta': 'A'},
                {'pregunta': 'Que el valor no sea una proyección del sujeto '
                             'al objeto, sino que el sujeto deba descubrir '
                             'los valores contenidos en el objeto, '
                             'corresponde a: (I CEPRU 2019-I)',
                 'alternativas': ['Objetivismo',
                                  'Relacionismo',
                                  'Impresionismo',
                                  'Utilitarismo',
                                  'Subjetivismo'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando los actos humanos se sancionan mediante '
                             'la consciencia, la sanción es: (I CEPRU '
                             '2019-I)',
                 'alternativas': ['Política',
                                  'Moral',
                                  'Jurídica',
                                  'Comunitaria',
                                  'Religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'El acto que consiste en dar y repartir en un '
                             'reparto mutuo de bienes entre dos o más '
                             'personas es justicia: (III CEPRU 2023-II)',
                 'alternativas': ['Legal',
                                  'Equitativa',
                                  'Social',
                                  'Distributiva',
                                  'Conmutativa'],
                 'correcta': 'E'},
                {'pregunta': 'La disciplina filosófica que estudia el '
                             'problema de la esencia e importancia del valor '
                             'en sociedad es la: (I CEPRU 2025-I)',
                 'alternativas': ['Lógica',
                                  'Gnoseología',
                                  'Ontología',
                                  'Epistemología',
                                  'Axiología'],
                 'correcta': 'E'},
                {'pregunta': 'El esfuerzo que hace un ser humano por '
                             'alcanzar la perfección viene de: (I CEPRU '
                             '2021-II)',
                 'alternativas': ['Considerar al bien como un fin',
                                  'Considerar al bien como un medio',
                                  'Considerar al mal como un antivalor',
                                  'Considerar al mal como el antivalor '
                                  'supremo',
                                  'Considerar al bien como un valor '
                                  'inherente al ser humano'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría axiológica que sostiene que el valor '
                             'se encuentra en la persona que valora, porque '
                             'el objeto no es capaz de valorarse a sí mismo, '
                             'se denomina: (Banco UNSAAC)',
                 'alternativas': ['Naturalismo',
                                  'Relacionismo',
                                  'Subjetivismo',
                                  'Idealismo',
                                  'Objetivismo'],
                 'correcta': 'C'},
                {'pregunta': 'Que jóvenes extranjeros lleguen al Perú para '
                             'ayudar desinteresadamente en la reconstrucción '
                             'de poblados destruidos por un terremoto es '
                             'muestra de: (II CEPRU 2020-I)',
                 'alternativas': ['Justicia',
                                  'Valentía',
                                  'Dignidad',
                                  'Igualdad',
                                  'Solidaridad'],
                 'correcta': 'E'},
                {'pregunta': 'En el enunciado «Entre el conjunto de valores, '
                             'la justicia es un valor preferido por las '
                             'poblaciones andinas y amazónicas», la '
                             'característica del valor observada es: (I '
                             'CEPRU 2021-I)',
                 'alternativas': ['Gradualidad',
                                  'Mensurabilidad',
                                  'Polaridad',
                                  'Jerarquía',
                                  'Objetividad'],
                 'correcta': 'D'},
                {'pregunta': 'Que el hombre sea valioso y fin en sí mismo es '
                             'un valor ético asociado a: (I CEPRU 2021-I)',
                 'alternativas': ['Solidaridad',
                                  'Justicia',
                                  'Libertad',
                                  'Templanza',
                                  'Dignidad'],
                 'correcta': 'E'},
                {'pregunta': 'La ley que dicta nuestra propia conciencia (el '
                             'deber), como mandato incondicional y '
                             'universal, es decir: (II CEPRU 2019-II)',
                 'alternativas': ['Una acción moral',
                                  'Imperativo categórico',
                                  'Ley amoral',
                                  'Una acción amoral',
                                  'Dos o más respuestas son correctas'],
                 'correcta': 'B'},
                {'pregunta': 'Según la clasificación de Max Scheler, los '
                             'valores que ponen en juego los sentidos, como '
                             'agradable-doloroso, son valores:',
                 'alternativas': ['Religiosos',
                                  'Estéticos',
                                  'Sensibles',
                                  'Vitales',
                                  'Lógicos'],
                 'correcta': 'C'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'vida y la salud, como sano-enfermo, son '
                             'valores:',
                 'alternativas': ['Lógicos',
                                  'Éticos',
                                  'Vitales',
                                  'Sensibles',
                                  'Teóricos'],
                 'correcta': 'C'},
                {'pregunta': 'Según Scheler, los valores que se traducen en '
                             'las ideologías, ideas y la verdad son valores:',
                 'alternativas': ['Estéticos',
                                  'Sensibles',
                                  'Lógicos',
                                  'Religiosos',
                                  'Vitales'],
                 'correcta': 'C'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'belleza y el arte, como bello-feo, son '
                             'valores:',
                 'alternativas': ['Estéticos',
                                  'Vitales',
                                  'Lógicos',
                                  'Sensibles',
                                  'Históricos'],
                 'correcta': 'A'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'fe y la creencia son valores:',
                 'alternativas': ['Sociales',
                                  'Religiosos',
                                  'Políticos',
                                  'Éticos',
                                  'Teóricos'],
                 'correcta': 'B'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'utilidad y las ganancias, como caro-barato, '
                             'son valores:',
                 'alternativas': ['Sociales',
                                  'Políticos',
                                  'Teóricos',
                                  'Económico-técnicos',
                                  'Lógicos'],
                 'correcta': 'D'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'realidad social y la justicia, como igualdad y '
                             'orden, son valores:',
                 'alternativas': ['Estéticos',
                                  'Religiosos',
                                  'Vitales',
                                  'Social-jurídicos',
                                  'Políticos'],
                 'correcta': 'D'},
                {'pregunta': 'Según Scheler, los valores relacionados con la '
                             'búsqueda del poder son valores:',
                 'alternativas': ['Jurídicos',
                                  'Religiosos',
                                  'Históricos',
                                  'Sociales',
                                  'Políticos'],
                 'correcta': 'E'}],
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
                     {'titulo': 'CLASIFICACIÓN DE LOS VALORES SEGÚN MAX '
                                'SCHELER',
                      'items': ['Valores sensibles (sensorial-hedonísticos): '
                                'ponen en juego los sentidos; ejemplo, '
                                'agradable-doloroso.',
                                'Valores vitales: relacionados a la vida y '
                                'la salud; ejemplo, sano-enfermo.',
                                'Valores lógicos: se traducen en las '
                                'ideologías, ideas, criterios y la verdad.',
                                'Valores estéticos: relacionados con la '
                                'belleza y el arte; ejemplo, bello-feo.',
                                'Valores ético-morales: relacionados con el '
                                'bien y la virtud; ejemplo, '
                                'correcto-incorrecto.',
                                'Valores religiosos: relacionados con la fe '
                                'y creencia; ejemplo, lo terrenal, beato, '
                                'profano.']},
                     {'titulo': 'TEORÍAS DEL VALOR',
                      'items': ['Subjetivismo: el valor depende del sujeto, '
                                'de su agrado o interés; no existe fuera de '
                                'la valoración.',
                                'Objetivismo: los valores existen '
                                'independientemente del sujeto; se '
                                'descubren, no se crean.',
                                'Relacionismo: el valor surge de la relación '
                                'entre el sujeto y el objeto.',
                                'Socioculturalismo: los valores son producto '
                                'de la sociedad y la cultura, y varían '
                                'históricamente.']},
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
                                'prudente de los placeres.',
                                'El eudemonismo de Aristóteles (384-322 '
                                'a.C.) pregona la felicidad como meta '
                                'suprema de toda la actividad moral del '
                                'hombre.',
                                'Para Aristóteles, la virtud es el '
                                'equilibrio entre dos extremos, la ley del '
                                'término medio: entre temeridad y cobardía '
                                'está la valentía.',
                                'San Agustín y, sobre todo, Santo Tomás de '
                                'Aquino, situaron la contemplación de Dios '
                                'como el bien y felicidad suprema del hombre '
                                'cristiano.']},
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
                                'responsabilidad moral.',
                                'La sanción moral es el castigo interno, '
                                'subjetivo, que recibe la persona por una '
                                'acción negativa: el remordimiento.',
                                'La sanción jurídica es la pena impuesta por '
                                'el Estado a quien viola una ley, regulada '
                                'por los tribunales.']}],
  'qr_reto': [{'pregunta': 'La pena impuesta por el Estado a quien viola una '
                           'ley, regulada por los tribunales, se llama:',
               'respuesta': 'Sanción jurídica'},
              {'pregunta': 'El utilitarismo sostiene que una acción es moral '
                           'si:',
               'respuesta': 'Es útil, es decir, produce felicidad'},
              {'pregunta': 'El imperativo categórico de Kant establece: obra '
                           'de tal modo que tu acción pueda convertirse en:',
               'respuesta': 'Ley universal'}],
  'qr_dato': 'Corrientes éticas: el eudemonismo de Aristóteles (el fin es la '
             'felicidad), la ética kantiana del deber, y el utilitarismo de '
             'Stuart Mill (la mayor felicidad para el mayor número).'},
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
                                  'El lenguaje literario',
                                  'La verdad de los hechos',
                                  'El origen del conocimiento',
                                  'Los valores morales'],
                 'correcta': 'A'},
                {'pregunta': 'La lógica estudia de los razonamientos su:',
                 'alternativas': ['Origen histórico',
                                  'Belleza',
                                  'Utilidad',
                                  'Contenido',
                                  'Forma'],
                 'correcta': 'E'},
                {'pregunta': 'El fundador de la lógica es:',
                 'alternativas': ['Frege',
                                  'Aristóteles',
                                  'Porfirio',
                                  'Platón',
                                  'Boole'],
                 'correcta': 'B'},
                {'pregunta': 'La obra lógica de Aristóteles se reunió bajo '
                             'el nombre de:',
                 'alternativas': ['Principia',
                                  'República',
                                  'Órganon',
                                  'Isagoge',
                                  'Metafísica'],
                 'correcta': 'C'},
                {'pregunta': 'El «árbol» que ordena géneros y especies fue '
                             'elaborado por:',
                 'alternativas': ['Russell',
                                  'Aristóteles',
                                  'Porfirio de Tiro',
                                  'Boole',
                                  'Frege'],
                 'correcta': 'C'},
                {'pregunta': 'La lógica moderna o simbólica se caracteriza '
                             'por emplear:',
                 'alternativas': ['Ejemplos históricos',
                                  'Símbolos matemáticos',
                                  'Lenguaje natural',
                                  'Silogismos únicamente',
                                  'Metáforas'],
                 'correcta': 'B'},
                {'pregunta': 'El filósofo peruano destacado en lógica '
                             'jurídica es:',
                 'alternativas': ['Antenor Orrego',
                                  'Francisco Miró Quesada Cantuarias',
                                  'Mariátegui',
                                  'Deustua',
                                  'Salazar Bondy'],
                 'correcta': 'B'},
                {'pregunta': 'La función del lenguaje que transmite '
                             'información y puede ser verdadera o falsa es '
                             'la:',
                 'alternativas': ['Directiva',
                                  'Expresiva',
                                  'Poética',
                                  'Fática',
                                  'Informativa'],
                 'correcta': 'E'},
                {'pregunta': 'La función del lenguaje que manifiesta '
                             'emociones es la:',
                 'alternativas': ['Descriptiva',
                                  'Informativa',
                                  'Metalingüística',
                                  'Directiva',
                                  'Expresiva'],
                 'correcta': 'E'},
                {'pregunta': '«Cierra la puerta» corresponde a la función:',
                 'alternativas': ['Directiva',
                                  'Poética',
                                  'Descriptiva',
                                  'Expresiva',
                                  'Informativa'],
                 'correcta': 'A'},
                {'pregunta': '«¡Qué hermoso atardecer!» corresponde a la '
                             'función:',
                 'alternativas': ['Referencial',
                                  'Apelativa',
                                  'Informativa',
                                  'Expresiva',
                                  'Directiva'],
                 'correcta': 'D'},
                {'pregunta': '«El Cusco está en el Perú» corresponde a la '
                             'función:',
                 'alternativas': ['Emotiva',
                                  'Informativa',
                                  'Directiva',
                                  'Expresiva',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'El lenguaje natural se caracteriza por ser:',
                 'alternativas': ['Ambiguo y vago',
                                  'Artificial',
                                  'Preciso',
                                  'Unívoco',
                                  'Simbólico'],
                 'correcta': 'A'},
                {'pregunta': 'El lenguaje formalizado se caracteriza por '
                             'ser:',
                 'alternativas': ['Coloquial',
                                  'Emotivo',
                                  'Ambiguo',
                                  'Literario',
                                  'Preciso y unívoco'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto de razones que sustentan una '
                             'conclusión constituye:',
                 'alternativas': ['Una exclamación',
                                  'Una argumentación',
                                  'Una narración',
                                  'Una descripción',
                                  'Una orden'],
                 'correcta': 'B'},
                {'pregunta': 'Las ramas principales de la lógica son la '
                             'formal clásica, la proposicional y la de:',
                 'alternativas': ['Relaciones',
                                  'Predicados exclusivamente',
                                  'Clases',
                                  'Números',
                                  'Conjuntos'],
                 'correcta': 'C'},
                {'pregunta': 'Las expresiones directivas NO pueden ser '
                             'calificadas como:',
                 'alternativas': ['Corteses o descorteses',
                                  'Útiles o inútiles',
                                  'Claras u oscuras',
                                  'Verdaderas o falsas',
                                  'Correctas o incorrectas'],
                 'correcta': 'D'},
                {'pregunta': 'En una argumentación, las razones que '
                             'sustentan se denominan:',
                 'alternativas': ['Corolarios',
                                  'Axiomas',
                                  'Premisas',
                                  'Conclusiones',
                                  'Falacias'],
                 'correcta': 'C'},
                {'pregunta': 'La lógica se clasifica como una ciencia:',
                 'alternativas': ['Fáctica natural',
                                  'Formal',
                                  'Fáctica social',
                                  'Experimental',
                                  'Aplicada'],
                 'correcta': 'B'},
                {'pregunta': 'La «Isagoge» fue escrita por:',
                 'alternativas': ['Aristóteles',
                                  'Porfirio de Tiro',
                                  'Boecio',
                                  'Frege',
                                  'Boole'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la lógica que estudia los actos del '
                             'pensar según su estructura, sin importar el '
                             'contenido, se llama lógica:',
                 'alternativas': ['De clases',
                                  'Formal',
                                  'Proposicional',
                                  'Material',
                                  'Simbólica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'La lógica que estudia las proposiciones en '
                             'bloque y sus conectivos se llama lógica:',
                 'alternativas': ['De clases',
                                  'Formal',
                                  'Deductiva exclusiva',
                                  'Modal',
                                  'Proposicional o de enunciados'],
                 'correcta': 'E'},
                {'pregunta': 'Una proposición es una expresión lingüística '
                             'que tiene la propiedad de ser:',
                 'alternativas': ['Solo falsa',
                                  'Solo verdadera',
                                  'Ambigua siempre',
                                  'Verdadera o falsa',
                                  'Ni verdadera ni falsa'],
                 'correcta': 'D'},
                {'pregunta': 'La rama de la lógica que estudia las '
                             'relaciones formales entre clases se llama '
                             'lógica:',
                 'alternativas': ['De clases',
                                  'Modal',
                                  'Simbólica',
                                  'Proposicional',
                                  'Formal'],
                 'correcta': 'A'},
                {'pregunta': 'Una clase, por sí sola, sin establecer '
                             'relaciones de pertenencia, no es ni verdadera '
                             'ni:',
                 'alternativas': ['Universal',
                                  'Particular',
                                  'Real',
                                  'Categórica',
                                  'Falsa'],
                 'correcta': 'E'},
                {'pregunta': 'El sofista considerado el más importante, '
                             'autor de la frase «el hombre es la medida de '
                             'todas las cosas», fue:',
                 'alternativas': ['Sócrates',
                                  'Gorgias',
                                  'Platón',
                                  'Aristóteles',
                                  'Protágoras'],
                 'correcta': 'E'},
                {'pregunta': 'En el campo de la lógica, Sócrates es '
                             'reconocido por descubrir el concepto de la '
                             'definición y de:',
                 'alternativas': ['La deducción',
                                  'La analogía',
                                  'La tautología',
                                  'El silogismo',
                                  'La inducción'],
                 'correcta': 'E'},
                {'pregunta': 'Platón es considerado el creador de qué '
                             'principio lógico:',
                 'alternativas': ['De Identidad',
                                  'De Causalidad',
                                  'De Razón Suficiente',
                                  'De no Contradicción',
                                  'Del Tercio Excluido'],
                 'correcta': 'D'},
                {'pregunta': 'El filósofo medieval que tradujo al latín '
                             'obras de Aristóteles y creó el Cuadro '
                             'Tradicional de Oposición fue:',
                 'alternativas': ['Duns Escoto',
                                  'Boecio',
                                  'Santo Tomás de Aquino',
                                  'Porfirio de Tiro',
                                  'San Agustín'],
                 'correcta': 'B'},
                {'pregunta': 'En la lógica moderna, el filósofo que intentó '
                             'construir un Lenguaje Universal fue:',
                 'alternativas': ['Descartes',
                                  'Kant',
                                  'Wilhelm Leibniz',
                                  'George Boole',
                                  'Aristóteles'],
                 'correcta': 'C'},
                {'pregunta': 'El fundador de la lógica simbólica, autor de '
                             '«Investigación sobre las leyes del '
                             'pensamiento» (1854), fue:',
                 'alternativas': ['Bertrand Russell',
                                  'Aristóteles',
                                  'George Boole',
                                  'Gottlob Frege',
                                  'Wilhelm Leibniz'],
                 'correcta': 'C'},
                {'pregunta': 'El pensador que propuso la lógica trivalente '
                             'fue:',
                 'alternativas': ['Leibniz',
                                  'Frege',
                                  'Aristóteles',
                                  'Łukasiewicz',
                                  'Wittgenstein'],
                 'correcta': 'D'},
                {'pregunta': 'La fórmula correcta del razonamiento válido '
                             'Modus Ponendo Ponens es: (Banco UNSAAC)',
                 'alternativas': ['[((p ∨ q) ∧ ~p) → q]',
                                  '[((p → q) ∧ ~q) → ~p]',
                                  '[((p → q) ∧ p) → q]',
                                  '[((p ∨ q) ∧ p) → q]',
                                  '(p → q) → (p ∨ q)'],
                 'correcta': 'C'},
                {'pregunta': 'La Lógica Paraconsistente, campo de estudio de '
                             'sistemas lógicos tolerantes a la '
                             'inconsistencia, fue propuesta por: (Primera '
                             'Oportunidad UNSAAC 2023)',
                 'alternativas': ['Francisco Miró Quesada Cantuarias',
                                  'George Boole',
                                  'Luis Piscoya Hermoza',
                                  'José Antonio Russo',
                                  'Augusto Salazar Bondy'],
                 'correcta': 'A'},
                {'pregunta': 'Bertrand Russell y Alfred Whitehead '
                             'escribieron la monumental obra: (II CEPRU '
                             '2019-I)',
                 'alternativas': ['Conceptografía',
                                  'Discurso del Método',
                                  'Principia Mathematica',
                                  'Tractatus Logico-Philosophicus',
                                  'Materialismo y Empiriocriticismo'],
                 'correcta': 'C'},
                {'pregunta': 'Según Mario Bunge, la lógica es una ciencia: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Formal',
                                  'Trascendente',
                                  'Inmanente',
                                  'Práctica',
                                  'Concreta'],
                 'correcta': 'A'},
                {'pregunta': 'La lógica formal estudia: (IV CEPRU 2023-II)',
                 'alternativas': ['Las proposiciones y los operadores '
                                  'lógicos',
                                  'La estructura de las clases S y P',
                                  'La estructura lógica interna de las '
                                  'oraciones',
                                  'Las relaciones entre clases',
                                  'El conjunto de conceptos, ideas, juicios '
                                  'y razonamientos'],
                 'correcta': 'A'},
                {'pregunta': 'El enunciado que presenta una proposición '
                             'compuesta es: (IV CEPRU 2023-II)',
                 'alternativas': ['El presidente del Perú',
                                  'Abrígate cada vez que llueva',
                                  'Marco, el de la mochila roja',
                                  'Sofía y Karla son primas',
                                  'Carmen no está despierta, ni dormida'],
                 'correcta': 'E'}],
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
                                'mayéutica.',
                                'Platón es considerado el creador del '
                                'Principio de no Contradicción.',
                                'Boecio, filósofo ecléctico, tradujo al '
                                'latín obras de Aristóteles y creó el Cuadro '
                                'Tradicional de Oposición.',
                                'En la lógica moderna, Wilhelm Leibniz '
                                'intentó construir un Lenguaje Universal '
                                '(Característica Universalis).',
                                'George Boole es considerado el fundador de '
                                'la lógica simbólica; publicó en 1854 '
                                '«Investigación sobre las leyes del '
                                'pensamiento».']},
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
                                '(premisas) que sustentan una conclusión.']}],
  'qr_reto': [{'pregunta': 'En el campo de la lógica, Sócrates es reconocido '
                           'por descubrir el concepto de la definición y de:',
               'respuesta': 'La inducción'},
              {'pregunta': 'En la lógica moderna, el filósofo que intentó '
                           'construir un Lenguaje Universal fue:',
               'respuesta': 'Wilhelm Leibniz'},
              {'pregunta': 'El fundador de la lógica es:',
               'respuesta': 'Aristóteles'}],
  'qr_dato': 'La argumentación es el conjunto de razones (premisas) que '
             'sustentan una conclusión.'},
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
                 'alternativas': ['Es formalmente correcto',
                                  'No tiene conclusión',
                                  'Carece de premisas',
                                  'Siempre es verdadero',
                                  'Parece válido pero no lo es'],
                 'correcta': 'E'},
                {'pregunta': 'Las falacias formales tienen un error en:',
                 'alternativas': ['La ortografía',
                                  'El contenido',
                                  'Las premisas verdaderas',
                                  'La estructura del razonamiento',
                                  'El vocabulario'],
                 'correcta': 'D'},
                {'pregunta': 'Las falacias de atinencia se cometen cuando '
                             'las premisas:',
                 'alternativas': ['Son numerosas',
                                  'Son verdaderas',
                                  'No son pertinentes para la conclusión',
                                  'Están bien formuladas',
                                  'Son evidentes'],
                 'correcta': 'C'},
                {'pregunta': '«No debemos creer en las teorías de Marx, '
                             'recuerda que fue comunista» es una falacia:',
                 'alternativas': ['De equívoco',
                                  'Ad ignorantiam',
                                  'Ad hominem',
                                  'Ad populum',
                                  'Ad báculum'],
                 'correcta': 'C'},
                {'pregunta': '«Dios existe, porque nadie ha demostrado su '
                             'inexistencia» es una falacia:',
                 'alternativas': ['Ad hominem',
                                  'Ad populum',
                                  'Ad verecundiam',
                                  'Causa falsa',
                                  'Ad ignorantiam'],
                 'correcta': 'E'},
                {'pregunta': '«Si presenta un reclamo, su permanencia en la '
                             'empresa puede acortarse» es una falacia:',
                 'alternativas': ['De énfasis',
                                  'Ad báculum',
                                  'Ignoratio elenchi',
                                  'Ad populum',
                                  'Ad hominem'],
                 'correcta': 'B'},
                {'pregunta': '«Este jabón es bueno, lo usa un cantante '
                             'famoso» es una falacia:',
                 'alternativas': ['Ad verecundiam',
                                  'Anfibología',
                                  'Causa falsa',
                                  'Ad báculum',
                                  'Ad populum'],
                 'correcta': 'A'},
                {'pregunta': '«Tome esta bebida, lo nuestro está primero» es '
                             'una falacia:',
                 'alternativas': ['Ad ignorantiam',
                                  'Ad báculum',
                                  'Ad populum',
                                  'Ad hominem',
                                  'De equívoco'],
                 'correcta': 'C'},
                {'pregunta': '«Me levanté con el pie izquierdo, hoy será un '
                             'mal día» es una falacia de:',
                 'alternativas': ['Autoridad',
                                  'Ignorancia',
                                  'Fuerza',
                                  'Causa falsa',
                                  'Ambigüedad'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando un razonamiento prueba una conclusión '
                             'distinta de la que pretendía, se comete:',
                 'alternativas': ['Equívoco',
                                  'Énfasis',
                                  'Ad báculum',
                                  'Ad hominem',
                                  'Ignoratio elenchi'],
                 'correcta': 'E'},
                {'pregunta': 'La falacia ad hominem del tipo ofensivo '
                             'consiste en:',
                 'alternativas': ['Atacar a quien hace la afirmación',
                                  'Citar una autoridad',
                                  'Apelar al pueblo',
                                  'Apelar a la fuerza',
                                  'Usar palabras ambiguas'],
                 'correcta': 'A'},
                {'pregunta': 'La falacia que aprovecha las circunstancias '
                             'personales del adversario es la ad hominem:',
                 'alternativas': ['Directa',
                                  'Formal',
                                  'Circunstancial',
                                  'Ofensiva',
                                  'Emotiva'],
                 'correcta': 'C'},
                {'pregunta': 'Las falacias de ambigüedad se producen cuando '
                             'el razonamiento contiene:',
                 'alternativas': ['Muchas premisas',
                                  'Conclusiones falsas',
                                  'Datos numéricos',
                                  'Palabras o frases ambiguas',
                                  'Citas de autoridad'],
                 'correcta': 'D'},
                {'pregunta': 'Usar la palabra «banco» con dos significados '
                             'distintos en un mismo razonamiento es una '
                             'falacia de:',
                 'alternativas': ['Anfibología',
                                  'Causa falsa',
                                  'Equívoco',
                                  'Autoridad',
                                  'Énfasis'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando la ambigüedad proviene de la '
                             'construcción gramatical se comete:',
                 'alternativas': ['Ad báculum',
                                  'Equívoco',
                                  'Ad populum',
                                  'Anfibología',
                                  'Énfasis'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando el significado cambia según la palabra '
                             'acentuada se comete la falacia de:',
                 'alternativas': ['Anfibología',
                                  'Causa falsa',
                                  'Ignoratio elenchi',
                                  'Énfasis',
                                  'Equívoco'],
                 'correcta': 'D'},
                {'pregunta': 'El recurso favorito de propagandistas y '
                             'demagogos es la falacia:',
                 'alternativas': ['Ad verecundiam',
                                  'De equívoco',
                                  'Formal',
                                  'Ad báculum',
                                  'Ad populum'],
                 'correcta': 'E'},
                {'pregunta': '«La fuerza hace el derecho» resume la falacia:',
                 'alternativas': ['De énfasis',
                                  'Ad hominem',
                                  'Ad populum',
                                  'Ad báculum',
                                  'Ad ignorantiam'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia ad verecundiam se comete al apelar '
                             'a una autoridad:',
                 'alternativas': ['Académica',
                                  'Científica',
                                  'Legítima',
                                  'Fuera de su ámbito de especialidad',
                                  'Reconocida en su campo'],
                 'correcta': 'D'},
                {'pregunta': 'Confundir la simple sucesión temporal con una '
                             'relación causal corresponde a la falacia de:',
                 'alternativas': ['Anfibología',
                                  'Equívoco',
                                  'Ad báculum',
                                  'Causa falsa',
                                  'Ad populum'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia formal que se comete al invertir la '
                             'ley del Modus Ponens se llama:',
                 'alternativas': ['Petición de principio',
                                  'Ignoratio elenchi',
                                  'Ad hominem',
                                  'Negación del antecedente',
                                  'Afirmación del consecuente'],
                 'correcta': 'E'},
                {'pregunta': 'Al considerar que, si ayer vi un gato negro y '
                             'me fue mal, es por culpa del gato, la falacia '
                             'en la que se cae es: (Primera Oportunidad '
                             'UNSAAC 2025)',
                 'alternativas': ['Ad hominem',
                                  'Ignoratio Elenchi',
                                  'Ad Ignorantiam',
                                  'Causa Falsa',
                                  'Ad verecundiam'],
                 'correcta': 'D'},
                {'pregunta': 'La falacia no formal Ad Populum (apelación '
                             'inadecuada al pueblo) se aprecia en: (Primera '
                             'Oportunidad UNSAAC 2023)',
                 'alternativas': ['Hoy me levanté con el pie izquierdo, no '
                                  'me saldrán bien las cosas',
                                  'El perro de mi vecino se llama Coco',
                                  'Tome Coca Cola, que es una bebida de '
                                  'sabor nacional',
                                  'Si la población aumenta, la subsistencia '
                                  'disminuye',
                                  'Si el carro se malogra, entonces el '
                                  'chofer es malo'],
                 'correcta': 'C'},
                {'pregunta': 'Es una falacia de atingencia: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['La gata es muy útil',
                                  'La camisa de cuadritos está sucia',
                                  'Deja de seguirme, o llamaré a la policía',
                                  'Trae las velas para navegar',
                                  'El perro de mi vecino está en mi patio'],
                 'correcta': 'C'},
                {'pregunta': 'En el enunciado «La ardilla de mi prima es '
                             'veloz», se determina la falacia de: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['Anfibología',
                                  'Equívoco',
                                  'Énfasis',
                                  'Causa falsa',
                                  'Ad hominem'],
                 'correcta': 'A'}],
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
                                'falsedad.',
                                'Ad báculum: apelación a la fuerza o a la '
                                'amenaza. «La fuerza hace el derecho».',
                                'Ad verecundiam: apelación a una autoridad '
                                'fuera de su ámbito de especialidad.']},
                     {'titulo': 'FALACIAS DE AMBIGÜEDAD',
                      'items': ['Aparecen cuando el razonamiento contiene '
                                'palabras o frases ambiguas.',
                                'Equívoco: se usa una palabra con dos o más '
                                'significados distintos en el mismo '
                                'razonamiento.',
                                'Anfibología: la ambigüedad proviene de la '
                                'construcción gramatical de la frase.',
                                'Énfasis: el significado cambia según la '
                                'palabra que se acentúa o destaca.']}],
  'qr_reto': [{'pregunta': '«Si presenta un reclamo, su permanencia en la '
                           'empresa puede acortarse» es una falacia:',
               'respuesta': 'Ad báculum'},
              {'pregunta': 'La falacia formal que se comete al invertir la '
                           'ley del Modus Ponens se llama:',
               'respuesta': 'Afirmación del consecuente'},
              {'pregunta': '«Me levanté con el pie izquierdo, hoy será un '
                           'mal día» es una falacia de:',
               'respuesta': 'Causa falsa'}],
  'qr_dato': 'Ad báculum: apelación a la fuerza o a la amenaza. «La fuerza '
             'hace el derecho».'},
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
                 'alternativas': ['Justo o injusto',
                                  'Útil o inútil',
                                  'Claro u oscuro',
                                  'Bello o feo',
                                  'Verdadero o falso'],
                 'correcta': 'E'},
                {'pregunta': 'NO es una proposición:',
                 'alternativas': ['Lima es la capital',
                                  'El Cusco está en el Perú',
                                  'Dos más dos es cuatro',
                                  '¿Qué hora es?',
                                  'La nieve es blanca'],
                 'correcta': 'D'},
                {'pregunta': 'La proposición que no contiene ningún operador '
                             'lógico se denomina:',
                 'alternativas': ['Compuesta',
                                  'Bicondicional',
                                  'Condicional',
                                  'Simple o atómica',
                                  'Molecular'],
                 'correcta': 'D'},
                {'pregunta': 'La proposición que contiene uno o más '
                             'operadores se denomina:',
                 'alternativas': ['Compuesta o molecular',
                                  'Simple',
                                  'Atómica',
                                  'Variable',
                                  'Constante'],
                 'correcta': 'A'},
                {'pregunta': 'Las variables proposicionales se representan '
                             'con:',
                 'alternativas': ['Palabras',
                                  'Letras minúsculas p, q, r, s',
                                  'Símbolos matemáticos',
                                  'Letras griegas',
                                  'Números'],
                 'correcta': 'B'},
                {'pregunta': 'El único conector monádico de la lógica '
                             'proposicional es:',
                 'alternativas': ['La negación',
                                  'La bicondicional',
                                  'La disyunción',
                                  'La conjunción',
                                  'La condicional'],
                 'correcta': 'A'},
                {'pregunta': 'El símbolo ∧ corresponde a la:',
                 'alternativas': ['Disyunción',
                                  'Negación',
                                  'Bicondicional',
                                  'Condicional',
                                  'Conjunción'],
                 'correcta': 'E'},
                {'pregunta': 'El símbolo → corresponde a la:',
                 'alternativas': ['Negación',
                                  'Bicondicional',
                                  'Disyunción fuerte',
                                  'Condicional',
                                  'Conjunción'],
                 'correcta': 'D'},
                {'pregunta': 'El símbolo ↔ se lee:',
                 'alternativas': ['O',
                                  'Y',
                                  'Si y solo si',
                                  'Si... entonces',
                                  'No'],
                 'correcta': 'C'},
                {'pregunta': 'La disyunción débil se lee como:',
                 'alternativas': ['Y',
                                  'O (inclusivo)',
                                  'Si y solo si',
                                  'No',
                                  'Si... entonces'],
                 'correcta': 'B'},
                {'pregunta': 'Los paréntesis, corchetes y llaves son '
                             'símbolos:',
                 'alternativas': ['Auxiliares',
                                  'Variables',
                                  'Constantes',
                                  'Monádicos',
                                  'Diádicos'],
                 'correcta': 'A'},
                {'pregunta': '«El zorrino no es mamífero» se formaliza como:',
                 'alternativas': ['~p', 'p → q', 'p ∨ q', 'p ∧ q', 'p'],
                 'correcta': 'A'},
                {'pregunta': '«La vaca es mamífero y el caballo también» se '
                             'formaliza como:',
                 'alternativas': ['p ∧ q', 'p ∨ q', 'p ↔ q', '~p', 'p → q'],
                 'correcta': 'A'},
                {'pregunta': '«El asno es mamífero pero el loro no» se '
                             'formaliza como:',
                 'alternativas': ['p ∧ q',
                                  'p ∨ q',
                                  'p ∧ ~q',
                                  'p → ~q',
                                  '~p ∧ q'],
                 'correcta': 'C'},
                {'pregunta': 'Una fórmula atómica se representa con:',
                 'alternativas': ['Dos variables',
                                  'Paréntesis',
                                  'Un conector',
                                  'Tres operadores',
                                  'Una sola variable'],
                 'correcta': 'E'},
                {'pregunta': '«Si llueve entonces me quedo» se formaliza '
                             'como:',
                 'alternativas': ['p ∧ q', 'p ∨ q', 'p ↔ q', '~p', 'p → q'],
                 'correcta': 'E'},
                {'pregunta': 'Los conectores que unen dos variables se '
                             'denominan:',
                 'alternativas': ['Monádicos',
                                  'Variables',
                                  'Atómicos',
                                  'Auxiliares',
                                  'Diádicos o binarios'],
                 'correcta': 'E'},
                {'pregunta': '«Estudio si y solo si tengo tiempo» se '
                             'formaliza como:',
                 'alternativas': ['~p', 'p → q', 'p ↔ q', 'p ∨ q', 'p ∧ q'],
                 'correcta': 'C'},
                {'pregunta': 'Las órdenes y las exclamaciones NO son '
                             'proposiciones porque:',
                 'alternativas': ['Son emotivas siempre',
                                  'Carecen de sujeto',
                                  'No usan verbos',
                                  'Son muy breves',
                                  'No pueden ser verdaderas ni falsas'],
                 'correcta': 'E'},
                {'pregunta': 'El símbolo ~ representa la:',
                 'alternativas': ['Implicación',
                                  'Equivalencia',
                                  'Conjunción',
                                  'Negación',
                                  'Disyunción'],
                 'correcta': 'D'},
                {'pregunta': 'La regla que dice que de una premisa '
                             'condicional, si se afirma el antecedente, se '
                             'concluye el consecuente, se llama:',
                 'alternativas': ['Silogismo Disyuntivo',
                                  'Silogismo Hipotético Puro',
                                  'Modus Ponendo Ponens',
                                  'Transitividad Simétrica',
                                  'Modus Tollendo Tollens'],
                 'correcta': 'C'},
                {'pregunta': 'En el argumento «Si Luis es ingeniero, es '
                             'profesional. Luis es ingeniero. Por lo tanto, '
                             'es profesional», se aplica:',
                 'alternativas': ['Silogismo Disyuntivo',
                                  'Modus Ponendo Ponens',
                                  'Transitividad Simétrica',
                                  'Ninguna regla válida',
                                  'Modus Tollendo Tollens'],
                 'correcta': 'B'},
                {'pregunta': 'La regla que, de una premisa condicional, '
                             'niega el consecuente para concluir la negación '
                             'del antecedente, se llama:',
                 'alternativas': ['Transitividad Simétrica',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Disyuntivo',
                                  'Modus Tollendo Tollens',
                                  'Silogismo Hipotético Puro'],
                 'correcta': 'D'},
                {'pregunta': 'La regla que, de una proposición disyuntiva, '
                             'niega un extremo para concluir la afirmación '
                             'del otro, se llama:',
                 'alternativas': ['Modus Tollendo Tollens',
                                  'Silogismo Disyuntivo',
                                  'Silogismo Hipotético Puro',
                                  'Transitividad Simétrica',
                                  'Modus Ponendo Ponens'],
                 'correcta': 'B'},
                {'pregunta': 'La regla que combina dos premisas '
                             'condicionales, donde el consecuente de la '
                             'primera es el antecedente de la segunda, se '
                             'llama:',
                 'alternativas': ['Transitividad Simétrica',
                                  'Silogismo Hipotético Puro',
                                  'Modus Tollendo Tollens',
                                  'Modus Ponendo Ponens',
                                  'Silogismo Disyuntivo'],
                 'correcta': 'B'},
                {'pregunta': 'En el argumento «Si es viernes, nos vamos de '
                             'paseo. Si nos vamos de paseo, estamos felices. '
                             'Por lo tanto, si es viernes, estamos felices», '
                             'se aplica:',
                 'alternativas': ['Ninguna regla válida',
                                  'Modus Ponendo Ponens',
                                  'Modus Tollendo Tollens',
                                  'Silogismo Disyuntivo',
                                  'Silogismo Hipotético Puro'],
                 'correcta': 'E'},
                {'pregunta': 'La transitividad de bicondicionales, con '
                             'estructura similar al Silogismo Hipotético '
                             'Puro pero con premisas bicondicionales, se '
                             'llama:',
                 'alternativas': ['Silogismo Categórico',
                                  'Silogismo Disyuntivo',
                                  'Modus Tollendo Tollens',
                                  'Transitividad Simétrica',
                                  'Modus Ponendo Ponens'],
                 'correcta': 'D'},
                {'pregunta': '«Las margaritas se marchitaron porque el '
                             'jardinero ni las regó, ni las cuidó» se '
                             'expresa en la fórmula molecular: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['(~q ∧ ~r) → p',
                                  '(~p ∧ ~q) → r',
                                  '(~p ∨ ~q) → r',
                                  'p → (~q ∧ ~r)',
                                  'p ↓ (~q → ~r)'],
                 'correcta': 'A'}],
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
                                'estamos felices».',
                                'La Transitividad Simétrica (TS) es la '
                                'transitividad de bicondicionales, con la '
                                'misma estructura que el SHP pero con '
                                'premisas bicondicionales.']}],
  'qr_reto': [{'pregunta': 'Los paréntesis, corchetes y llaves son símbolos:',
               'respuesta': 'Auxiliares'},
              {'pregunta': '«El zorrino no es mamífero» se formaliza como:',
               'respuesta': '~p'},
              {'pregunta': 'La regla que combina dos premisas condicionales, '
                           'donde el consecuente de la primera es el '
                           'antecedente de la segunda, se llama:',
               'respuesta': 'Silogismo Hipotético Puro'}],
  'qr_dato': 'Fórmula molecular: contiene uno o más operadores. Ejemplo: «El '
             'zorrino no es mamífero» = ~p.'},
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
                {'titulo': '13.2 LOS SEIS OPERADORES: CONDICIONES DE VERDAD',
                 'items': ['La {conjunción} es verdadera solo cuando ambas '
                           'proposiciones son {verdaderas}; en los demás '
                           'casos es falsa.',
                           'La {disyunción inclusiva o débil} es falsa solo '
                           'cuando ambas proposiciones son {falsas}; en los '
                           'demás casos es verdadera.',
                           'La {disyunción exclusiva o fuerte} es verdadera '
                           'cuando las proposiciones tienen valores '
                           '{contrarios}; en los demás casos es falsa.',
                           'La {condicional o implicación} es falsa solo '
                           'cuando el antecedente es {verdadero} y el '
                           'consecuente falso; en los demás casos es '
                           'verdadera.',
                           'La {bicondicional o equivalencia} es falsa '
                           'cuando las proposiciones tienen valores '
                           '{contrarios}; en los demás casos es verdadera.',
                           'La {negación} es verdadera cuando su proposición '
                           'original es {falsa}, y falsa cuando la original '
                           'es verdadera.']},
                {'titulo': '13.3 PRINCIPALES ESQUEMAS',
                 'items': ['{Tautología}: la fórmula resulta {verdadera} en '
                           'todos los casos.',
                           '{Contradicción}: la fórmula resulta {falsa} en '
                           'todos los casos.',
                           '{Contingencia} o consistencia: resulta verdadera '
                           'en algunos casos y {falsa} en otros.']},
                {'titulo': '13.4 VALIDEZ MEDIANTE TABLAS DE VERDAD',
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
                 'alternativas': ['Tabla de verdad',
                                  'Cuadro de oposición',
                                  'Árbol de Porfirio',
                                  'Silogismo',
                                  'Diagrama de Venn'],
                 'correcta': 'A'},
                {'pregunta': 'El número de combinaciones de una tabla de '
                             'verdad se calcula con:',
                 'alternativas': ['n+2', 'n!', '2n', '2ⁿ', 'n²'],
                 'correcta': 'D'},
                {'pregunta': 'Una fórmula con 3 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['9', '3', '6', '12', '8'],
                 'correcta': 'E'},
                {'pregunta': 'Una fórmula con 2 variables tiene un número de '
                             'combinaciones igual a:',
                 'alternativas': ['6', '3', '2', '4', '8'],
                 'correcta': 'D'},
                {'pregunta': 'La fórmula que resulta verdadera en todos los '
                             'casos es una:',
                 'alternativas': ['Contradicción',
                                  'Antinomia',
                                  'Tautología',
                                  'Contingencia',
                                  'Consistencia'],
                 'correcta': 'C'},
                {'pregunta': 'La fórmula que resulta falsa en todos los '
                             'casos es una:',
                 'alternativas': ['Implicación',
                                  'Contradicción',
                                  'Contingencia',
                                  'Tautología',
                                  'Equivalencia'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula verdadera en algunos casos y falsa '
                             'en otros es una:',
                 'alternativas': ['Contradicción',
                                  'Contingencia',
                                  'Tautología',
                                  'Identidad',
                                  'Negación'],
                 'correcta': 'B'},
                {'pregunta': 'El Modus Ponendo Ponens concluye q a partir '
                             'de:',
                 'alternativas': ['p → q y ~q',
                                  'p ∨ q y ~p',
                                  'p → q y q → r',
                                  '~(p ∧ q)',
                                  'p → q y p'],
                 'correcta': 'E'},
                {'pregunta': 'El Modus Tollendo Tollens concluye ~p a partir '
                             'de:',
                 'alternativas': ['p ∧ q',
                                  'q → r',
                                  'p ∨ q y ~p',
                                  'p → q y ~q',
                                  'p → q y p'],
                 'correcta': 'D'},
                {'pregunta': 'El Silogismo Disyuntivo concluye q a partir '
                             'de:',
                 'alternativas': ['p ↔ q',
                                  'p → q y ~q',
                                  'p ∨ q y ~p',
                                  'p ∧ q',
                                  'p → q y p'],
                 'correcta': 'C'},
                {'pregunta': 'El Silogismo Hipotético Puro concluye p → r a '
                             'partir de:',
                 'alternativas': ['p ∨ q',
                                  'p ↔ q',
                                  'p → q y p',
                                  'p → q y q → r',
                                  '~p ∧ q'],
                 'correcta': 'D'},
                {'pregunta': 'La ley que transforma la negación de una '
                             'conjunción en disyunción de negaciones es la '
                             'de:',
                 'alternativas': ['Identidad',
                                  'Tercio excluido',
                                  'Contradicción',
                                  'De Morgan',
                                  'Transitividad'],
                 'correcta': 'D'},
                {'pregunta': 'Si «si estudio apruebo» y «estudio», entonces '
                             '«apruebo». Este razonamiento es un:',
                 'alternativas': ['MPP', 'SD', 'MTT', 'SHP', 'De Morgan'],
                 'correcta': 'A'},
                {'pregunta': 'Si «si llueve me mojo» y «no me mojé», '
                             'entonces «no llovió». Este razonamiento es un:',
                 'alternativas': ['MTT', 'SD', 'MPP', 'SHP', 'DCC'],
                 'correcta': 'A'},
                {'pregunta': 'En una tabla de verdad, el brazo derecho de la '
                             'cruz se denomina:',
                 'alternativas': ['Base',
                                  'Eje',
                                  'Margen',
                                  'Cuerpo',
                                  'Columna'],
                 'correcta': 'D'},
                {'pregunta': 'En una tabla de verdad, el brazo izquierdo se '
                             'denomina:',
                 'alternativas': ['Cabecera',
                                  'Pie',
                                  'Cuerpo',
                                  'Margen',
                                  'Fila'],
                 'correcta': 'D'},
                {'pregunta': 'Una fórmula con 4 variables tendrá un número '
                             'de combinaciones igual a:',
                 'alternativas': ['8', '4', '16', '12', '32'],
                 'correcta': 'C'},
                {'pregunta': 'La tautología se representa habitualmente con '
                             'la letra:',
                 'alternativas': ['F', 'T', 'A', 'C', 'V'],
                 'correcta': 'B'},
                {'pregunta': 'Si «o voy al cine o voy al teatro» y «no voy '
                             'al cine», concluyo «voy al teatro». Es un:',
                 'alternativas': ['MTT',
                                  'Dilema',
                                  'MPP',
                                  'Silogismo disyuntivo',
                                  'SHP'],
                 'correcta': 'D'},
                {'pregunta': 'El dilema constructivo compuesto se abrevia '
                             'como:',
                 'alternativas': ['DCC', 'SHP', 'SD', 'MTT', 'MPP'],
                 'correcta': 'A'},
                {'pregunta': 'Un razonamiento es válido cuando es imposible '
                             'que las premisas sean verdaderas y la '
                             'conclusión:',
                 'alternativas': ['Falsa',
                                  'También verdadera',
                                  'Tenga sentido',
                                  'Contingente',
                                  'Tautológica'],
                 'correcta': 'A'},
                {'pregunta': 'Para comprobar la validez de un razonamiento '
                             'con tablas de verdad, se construye la fórmula '
                             '«(premisas) → conclusión»; si resulta '
                             'tautológica, el razonamiento es:',
                 'alternativas': ['Válido',
                                  'Contradictorio',
                                  'Contingente',
                                  'Inválido',
                                  'Indeterminado'],
                 'correcta': 'A'},
                {'pregunta': 'Si en alguna fila de la tabla las premisas son '
                             'verdaderas y la conclusión falsa, el '
                             'razonamiento es:',
                 'alternativas': ['Contingente exclusivo',
                                  'Válido',
                                  'Inválido',
                                  'Necesario',
                                  'Tautológico'],
                 'correcta': 'C'},
                {'pregunta': 'La Ley de De Morgan establece que la negación '
                             'de una conjunción equivale a:',
                 'alternativas': ['La negación de la disyunción',
                                  'La conjunción de las negaciones exclusiva',
                                  'El bicondicional de las negaciones',
                                  'La conjunción de las afirmaciones',
                                  'La disyunción de las negaciones'],
                 'correcta': 'E'},
                {'pregunta': 'El operador lógico verdadero solo cuando ambas '
                             'proposiciones son verdaderas se llama:',
                 'alternativas': ['Bicondicional',
                                  'Conjunción',
                                  'Negación',
                                  'Condicional',
                                  'Disyunción'],
                 'correcta': 'B'},
                {'pregunta': 'El operador lógico falso solo cuando ambas '
                             'proposiciones son falsas, llamado disyunción '
                             'inclusiva, también se conoce como disyunción:',
                 'alternativas': ['Exclusiva',
                                  'Fuerte',
                                  'Débil',
                                  'Estricta',
                                  'Condicional'],
                 'correcta': 'C'},
                {'pregunta': 'El operador lógico verdadero cuando las '
                             'proposiciones tienen valores contrarios, '
                             'llamado disyunción exclusiva, también se '
                             'conoce como disyunción:',
                 'alternativas': ['Fuerte',
                                  'Débil',
                                  'Simple',
                                  'Condicional',
                                  'Inclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'El operador condicional o implicación es falso '
                             'únicamente cuando el antecedente es verdadero '
                             'y el consecuente es:',
                 'alternativas': ['Tautológico',
                                  'Falso',
                                  'Contingente',
                                  'Indeterminado',
                                  'Verdadero'],
                 'correcta': 'B'},
                {'pregunta': 'El operador bicondicional o equivalencia es '
                             'falso cuando las proposiciones tienen valores:',
                 'alternativas': ['Iguales',
                                  'Falsos',
                                  'Contrarios',
                                  'Verdaderos',
                                  'Indeterminados'],
                 'correcta': 'C'},
                {'pregunta': 'El operador de negación es verdadero cuando su '
                             'proposición original es:',
                 'alternativas': ['Falsa',
                                  'Contradictoria',
                                  'Verdadera',
                                  'Tautológica',
                                  'Contingente'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'LA TABLA DE VERDAD',
                      'items': ['Es el diagrama que muestra todos los '
                                'valores posibles de una fórmula molecular.',
                                'El número de combinaciones o arreglos se '
                                'calcula con la fórmula 2ⁿ, donde n es el '
                                'número de variables.',
                                'Con 2 variables hay 4 combinaciones; con 3 '
                                'variables, 8.']},
                     {'titulo': 'LOS SEIS OPERADORES: CONDICIONES DE VERDAD',
                      'items': ['La conjunción es verdadera solo cuando '
                                'ambas proposiciones son verdaderas; en los '
                                'demás casos es falsa.',
                                'La disyunción inclusiva o débil es falsa '
                                'solo cuando ambas proposiciones son falsas; '
                                'en los demás casos es verdadera.',
                                'La disyunción exclusiva o fuerte es '
                                'verdadera cuando las proposiciones tienen '
                                'valores contrarios; en los demás casos es '
                                'falsa.',
                                'La condicional o implicación es falsa solo '
                                'cuando el antecedente es verdadero y el '
                                'consecuente falso; en los demás casos es '
                                'verdadera.',
                                'La bicondicional o equivalencia es falsa '
                                'cuando las proposiciones tienen valores '
                                'contrarios; en los demás casos es '
                                'verdadera.',
                                'La negación es verdadera cuando su '
                                'proposición original es falsa, y falsa '
                                'cuando la original es verdadera.']},
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
                                '(~p ∨ ~q).']}],
  'qr_reto': [{'pregunta': 'La fórmula que resulta falsa en todos los casos '
                           'es una:',
               'respuesta': 'Contradicción'},
              {'pregunta': 'Una fórmula con 3 variables tiene un número de '
                           'combinaciones igual a:',
               'respuesta': '8'},
              {'pregunta': 'El Silogismo Hipotético Puro concluye p → r a '
                           'partir de:',
               'respuesta': 'p → q y q → r'}],
  'qr_dato': 'Si en alguna fila las premisas son verdaderas y la conclusión '
             'falsa, el razonamiento es inválido.'},
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
                 'alternativas': ['Tercio excluido',
                                  'Razón suficiente',
                                  'Causalidad',
                                  'No contradicción',
                                  'Identidad'],
                 'correcta': 'E'},
                {'pregunta': 'El principio que niega que una proposición sea '
                             'verdadera y falsa a la vez es el de:',
                 'alternativas': ['Tercio excluido',
                                  'Analogía',
                                  'Razón suficiente',
                                  'No contradicción',
                                  'Identidad'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que afirma que entre dos '
                             'contradictorias no hay una tercera posibilidad '
                             'es el de:',
                 'alternativas': ['No contradicción',
                                  'Tercio excluido',
                                  'Suficiencia',
                                  'Identidad',
                                  'Causalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La representación mental de un objeto es el:',
                 'alternativas': ['Concepto',
                                  'Razonamiento',
                                  'Juicio',
                                  'Silogismo',
                                  'Término'],
                 'correcta': 'A'},
                {'pregunta': 'El número de objetos a los que se aplica un '
                             'concepto es su:',
                 'alternativas': ['Cantidad',
                                  'Extensión',
                                  'Esencia',
                                  'Comprensión',
                                  'Cualidad'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de notas o características de un '
                             'concepto es su:',
                 'alternativas': ['Comprensión',
                                  'Cualidad',
                                  'Extensión',
                                  'Relación',
                                  'Cantidad'],
                 'correcta': 'A'},
                {'pregunta': 'Extensión y comprensión son entre sí:',
                 'alternativas': ['Equivalentes',
                                  'Idénticas',
                                  'Inversamente proporcionales',
                                  'Directamente proporcionales',
                                  'Independientes'],
                 'correcta': 'C'},
                {'pregunta': 'La operación mental que afirma o niega algo de '
                             'algo es el:',
                 'alternativas': ['Silogismo',
                                  'Juicio',
                                  'Razonamiento',
                                  'Término',
                                  'Concepto'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión verbal del juicio es la:',
                 'alternativas': ['Proposición',
                                  'Interjección',
                                  'Oración interrogativa',
                                  'Frase',
                                  'Palabra'],
                 'correcta': 'A'},
                {'pregunta': 'Los juicios se dividen por su cantidad en '
                             'universales y:',
                 'alternativas': ['Hipotéticos',
                                  'Negativos',
                                  'Categóricos',
                                  'Afirmativos',
                                  'Particulares'],
                 'correcta': 'E'},
                {'pregunta': 'Los juicios se dividen por su cualidad en '
                             'afirmativos y:',
                 'alternativas': ['Compuestos',
                                  'Negativos',
                                  'Particulares',
                                  'Simples',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'El juicio tipo A es:',
                 'alternativas': ['Particular afirmativo',
                                  'Singular',
                                  'Universal negativo',
                                  'Particular negativo',
                                  'Universal afirmativo'],
                 'correcta': 'E'},
                {'pregunta': 'El juicio tipo E es:',
                 'alternativas': ['Universal negativo',
                                  'Particular negativo',
                                  'Indefinido',
                                  'Universal afirmativo',
                                  'Particular afirmativo'],
                 'correcta': 'A'},
                {'pregunta': 'El juicio tipo I es:',
                 'alternativas': ['Particular afirmativo',
                                  'Singular',
                                  'Particular negativo',
                                  'Universal negativo',
                                  'Universal afirmativo'],
                 'correcta': 'A'},
                {'pregunta': 'El juicio tipo O es:',
                 'alternativas': ['Universal afirmativo',
                                  'Particular negativo',
                                  'Particular afirmativo',
                                  'Hipotético',
                                  'Universal negativo'],
                 'correcta': 'B'},
                {'pregunta': '«Todos los hombres son mortales» es un juicio '
                             'de tipo:',
                 'alternativas': ['A', 'U', 'O', 'I', 'E'],
                 'correcta': 'A'},
                {'pregunta': '«Ningún metal es líquido» es un juicio de '
                             'tipo:',
                 'alternativas': ['O', 'E', 'I', 'A', 'U'],
                 'correcta': 'B'},
                {'pregunta': 'El razonamiento que va de lo general a lo '
                             'particular es:',
                 'alternativas': ['Inductivo',
                                  'Abductivo',
                                  'Deductivo',
                                  'Analógico',
                                  'Dialéctico'],
                 'correcta': 'C'},
                {'pregunta': 'El razonamiento cuya conclusión es solo '
                             'probable es el:',
                 'alternativas': ['Inductivo',
                                  'Deductivo',
                                  'Formal',
                                  'Silogístico',
                                  'Apodíctico'],
                 'correcta': 'A'},
                {'pregunta': 'El razonamiento que concluye por semejanza '
                             'entre casos es el:',
                 'alternativas': ['Deductivo',
                                  'Inductivo completo',
                                  'Silogístico',
                                  'Hipotético',
                                  'Analógico'],
                 'correcta': 'E'},
                {'pregunta': 'El pensador que propuso la lógica trivalente '
                             'fue: (IV CEPRU 2023-II)',
                 'alternativas': ['Cantuarias',
                                  'Leibniz',
                                  'Aristóteles',
                                  'Wittgenstein',
                                  'Lukasiewicz'],
                 'correcta': 'E'},
                {'pregunta': 'El enunciado «No es cierto que el número 3 sea '
                             'impar y el número 3 no sea impar a la vez» se '
                             'denomina principio de: (IV CEPRU 2023-II)',
                 'alternativas': ['Tercio excluido',
                                  'Razón suficiente',
                                  'Clases',
                                  'Identidad',
                                  'No contradicción'],
                 'correcta': 'E'},
                {'pregunta': 'En la lógica dialéctica, el paso en forma de '
                             'salto de la vieja calidad a una calidad nueva '
                             'se denomina ley de: (I CEPRU 2024-II)',
                 'alternativas': ['La negación de la negación',
                                  'Tránsito de lo cuantitativo a lo '
                                  'cualitativo',
                                  'Unidad y lucha de contrarios',
                                  'Núcleo esencial',
                                  'La selección natural de especies'],
                 'correcta': 'B'}],
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
                                'semejanza entre casos.']}],
  'qr_reto': [{'pregunta': 'El juicio tipo A es:',
               'respuesta': 'Universal afirmativo'},
              {'pregunta': 'El número de objetos a los que se aplica un '
                           'concepto es su:',
               'respuesta': 'Extensión'},
              {'pregunta': 'El conjunto de notas o características de un '
                           'concepto es su:',
               'respuesta': 'Comprensión'}],
  'qr_dato': 'Razonamiento inductivo: va de lo particular a lo general; la '
             'conclusión es probable.'},
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
                {'titulo': '15.2 OPOSICIÓN: CONTRARIOS Y SUBCONTRARIOS',
                 'items': ['Son {contrarios} los enunciados universales A—E: '
                           'nunca pueden ser {verdaderos} a la vez, pero sí '
                           'pueden ser ambos {falsos}.',
                           'Si «Todos los caballos son solípedos» (A) es '
                           'verdadero, entonces «Ningún caballo es solípedo» '
                           '(E) es {falso}.',
                           'Son {subcontrarios} los enunciados particulares '
                           'I—O: nunca pueden ser {falsos} a la vez, pero sí '
                           'pueden ser ambos {verdaderos}.',
                           'Si «Algunos insectos son vertebrados» (I) es '
                           'falso, entonces «Algunos insectos no son '
                           'vertebrados» (O) es {verdadero}.']},
                {'titulo': '15.3 TIPOS DE CONVERSIÓN',
                 'items': ['La {conversión simple} conserva la cantidad; es '
                           'totalmente válida en los casos de proposiciones '
                           '{E} e I.',
                           'Ejemplo de conversión simple: «Ningún escritor '
                           'es analfabeto» (E) se convierte en «Ningún '
                           '{analfabeto} es escritor» (E).',
                           'La {conversión por accidente} o limitación solo '
                           'conserva la extensión; cambia la cantidad de '
                           'universal a {particular}.',
                           'Ejemplo: «Todos los animales son mamíferos» (A) '
                           'se convierte en «Algunos mamíferos son '
                           '{animales}» (I).',
                           'La proposición {O} no tiene conversa válida.']},
                {'titulo': '15.4 CONTRAPUESTA E INFERENCIA MEDIATA',
                 'items': ['Por contrapuesta {parcial}: se obtiene '
                           'combinando obversión y conversión.',
                           'Por contrapuesta {total}: se niegan ambos '
                           'términos y se {intercambian}.',
                           'La inferencia {mediata} obtiene la conclusión a '
                           'partir de {dos} o más premisas; su forma típica '
                           'es el {silogismo}.']},
                {'titulo': '15.5 EL SILOGISMO CATEGÓRICO',
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
                 'alternativas': ['Deductiva compuesta',
                                  'Inmediata',
                                  'Analógica',
                                  'Mediata',
                                  'Silogística'],
                 'correcta': 'B'},
                {'pregunta': 'La inferencia en que se intercambian sujeto y '
                             'predicado se denomina:',
                 'alternativas': ['Contraposición',
                                  'Oposición',
                                  'Conversión',
                                  'Subalternación',
                                  'Obversión'],
                 'correcta': 'C'},
                {'pregunta': 'La inferencia en que se cambia la cualidad y '
                             'se niega el predicado es la:',
                 'alternativas': ['Obversión',
                                  'Contrariedad',
                                  'Contrapuesta total',
                                  'Subalternación',
                                  'Conversión'],
                 'correcta': 'A'},
                {'pregunta': '«Todo S es P» obvertido resulta:',
                 'alternativas': ['Todo P es S',
                                  'Ningún S es no-P',
                                  'Algún S no es P',
                                  'Ningún P es S',
                                  'Algún S es P'],
                 'correcta': 'B'},
                {'pregunta': 'El cuadro de oposición relaciona los juicios:',
                 'alternativas': ['Deductivos e inductivos',
                                  'Verdaderos y falsos',
                                  'Mayor y menor',
                                  'Simples y compuestos',
                                  'A, E, I, O'],
                 'correcta': 'E'},
                {'pregunta': 'La inferencia que parte de dos o más premisas '
                             'se denomina:',
                 'alternativas': ['Inmediata',
                                  'Mediata',
                                  'Unilateral',
                                  'Directa',
                                  'Simple'],
                 'correcta': 'B'},
                {'pregunta': 'La forma típica de la inferencia mediata es '
                             'el:',
                 'alternativas': ['Dilema',
                                  'Sorites',
                                  'Epiquerema',
                                  'Entimema',
                                  'Silogismo'],
                 'correcta': 'E'},
                {'pregunta': 'El silogismo categórico consta de:',
                 'alternativas': ['Tres proposiciones',
                                  'Dos proposiciones',
                                  'Una proposición',
                                  'Cuatro proposiciones',
                                  'Cinco proposiciones'],
                 'correcta': 'A'},
                {'pregunta': 'El término que aparece en ambas premisas pero '
                             'no en la conclusión es el:',
                 'alternativas': ['Predicado',
                                  'Mayor',
                                  'Medio',
                                  'Sujeto',
                                  'Menor'],
                 'correcta': 'C'},
                {'pregunta': 'El término mayor del silogismo es el:',
                 'alternativas': ['Que se omite',
                                  'Predicado de la conclusión',
                                  'Término medio',
                                  'Que aparece dos veces',
                                  'Sujeto de la conclusión'],
                 'correcta': 'B'},
                {'pregunta': 'El término menor del silogismo es el:',
                 'alternativas': ['Universal',
                                  'Término medio',
                                  'Predicado de la conclusión',
                                  'Que no aparece',
                                  'Sujeto de la conclusión'],
                 'correcta': 'E'},
                {'pregunta': 'De dos premisas negativas:',
                 'alternativas': ['Se sigue una conclusión negativa',
                                  'Se sigue una conclusión afirmativa',
                                  'Se sigue siempre una universal',
                                  'No se sigue conclusión alguna',
                                  'Se sigue una particular'],
                 'correcta': 'D'},
                {'pregunta': 'De dos premisas particulares:',
                 'alternativas': ['No se sigue conclusión alguna',
                                  'Se sigue una negativa',
                                  'Se sigue una universal',
                                  'Se sigue una afirmativa',
                                  'Se sigue una conclusión particular'],
                 'correcta': 'A'},
                {'pregunta': 'El término medio debe estar distribuido:',
                 'alternativas': ['Nunca',
                                  'Solo en la conclusión',
                                  'Al menos una vez',
                                  'Siempre dos veces',
                                  'En el predicado'],
                 'correcta': 'C'},
                {'pregunta': 'Las figuras del silogismo se determinan por la '
                             'posición del:',
                 'alternativas': ['Sujeto',
                                  'Predicado',
                                  'Término mayor',
                                  'Término medio',
                                  'Término menor'],
                 'correcta': 'D'},
                {'pregunta': 'El número de figuras del silogismo es:',
                 'alternativas': ['Ocho', 'Tres', 'Seis', 'Cuatro', 'Dos'],
                 'correcta': 'D'},
                {'pregunta': '«Ningún S es P» convertido resulta:',
                 'alternativas': ['Algún S no es P',
                                  'Algún P es S',
                                  'Ningún P es S',
                                  'Todo P es S',
                                  'Todo S es no-P'],
                 'correcta': 'C'},
                {'pregunta': 'La contrapuesta total se obtiene:',
                 'alternativas': ['Solo convirtiendo',
                                  'Cambiando solo la cualidad',
                                  'Negando ambos términos e '
                                  'intercambiándolos',
                                  'Negando la conclusión',
                                  'Solo obvirtiendo'],
                 'correcta': 'C'},
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
                 'alternativas': ['Subcontrariedad',
                                  'Subalternación',
                                  'Contrariedad',
                                  'Identidad',
                                  'Contradicción'],
                 'correcta': 'C'},
                {'pregunta': 'El cuadro tradicional de oposición entre los '
                             'juicios A, E, I, O también se conoce como '
                             'cuadro de:',
                 'alternativas': ['Boecio',
                                  'Porfirio',
                                  'Kant',
                                  'Leibniz',
                                  'Aristóteles'],
                 'correcta': 'A'},
                {'pregunta': 'En el cuadro de oposición, los pares de '
                             'proposiciones contradictorias son:',
                 'alternativas': ['A—O y E—I',
                                  'A—I y E—O',
                                  'Solo I—O',
                                  'Solo A—E',
                                  'A—E y I—O'],
                 'correcta': 'A'},
                {'pregunta': 'En la subalternación, si la proposición '
                             'universal (subalternante) es verdadera, la '
                             'particular (subalterna) es:',
                 'alternativas': ['También verdadera',
                                  'Imposible',
                                  'Contradictoria',
                                  'Falsa',
                                  'Indeterminada'],
                 'correcta': 'A'},
                {'pregunta': 'En la subalternación, si la proposición '
                             'universal es falsa, la particular subalterna '
                             'queda:',
                 'alternativas': ['También falsa',
                                  'Imposible de evaluar',
                                  'Indeterminada',
                                  'Contradictoria',
                                  'Verdadera'],
                 'correcta': 'C'},
                {'pregunta': 'De las premisas «Los cusqueños son peruanos» y '
                             '«Los anteños son cusqueños», la conclusión '
                             'pertinente sería: (Primera Oportunidad UNSAAC '
                             '2025)',
                 'alternativas': ['Todo cusqueño es peruano',
                                  'Los peruanos son anteños',
                                  'Algunos anteños son cusqueños',
                                  'Los cusqueños no son peruanos',
                                  'Los anteños son peruanos'],
                 'correcta': 'E'},
                {'pregunta': '«Todos los felinos andinos son carnívoros. El '
                             'puma es un felino; entonces, el puma es un '
                             'carnívoro» es un razonamiento de tipo: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Disyuntivo',
                                  'Hipotético',
                                  'Deductivo',
                                  'Inductivo',
                                  'Analógico'],
                 'correcta': 'C'},
                {'pregunta': 'El autor del cuadro de oposición es: (IV CEPRU '
                             '2023-II)',
                 'alternativas': ['Aristóteles',
                                  'Boecio',
                                  'Plotino',
                                  'Porfirio',
                                  'Sócrates'],
                 'correcta': 'B'},
                {'pregunta': 'Los enunciados universales A—E, que nunca '
                             'pueden ser verdaderos a la vez pero sí pueden '
                             'ser ambos falsos, se llaman:',
                 'alternativas': ['Contrarios',
                                  'Contradictorios',
                                  'Subalternos',
                                  'Convertibles',
                                  'Subcontrarios'],
                 'correcta': 'A'},
                {'pregunta': 'Los enunciados particulares I—O, que nunca '
                             'pueden ser falsos a la vez pero sí pueden ser '
                             'ambos verdaderos, se llaman:',
                 'alternativas': ['Obversos',
                                  'Contrarios',
                                  'Subalternantes',
                                  'Subcontrarios',
                                  'Contradictorios'],
                 'correcta': 'D'},
                {'pregunta': 'Si «Todos los caballos son solípedos» (A) es '
                             'verdadero, entonces «Ningún caballo es '
                             'solípedo» (E), por ser contrarios, es:',
                 'alternativas': ['Contradictorio',
                                  'Verdadero',
                                  'Falso',
                                  'También verdadero',
                                  'Indeterminado'],
                 'correcta': 'C'},
                {'pregunta': 'El tipo de conversión que conserva la '
                             'cantidad, siendo totalmente válida en los '
                             'casos E e I, se llama conversión:',
                 'alternativas': ['Simple',
                                  'Parcial',
                                  'Obvertida',
                                  'Por accidente',
                                  'Por limitación'],
                 'correcta': 'A'},
                {'pregunta': 'El tipo de conversión que solo conserva la '
                             'extensión, cambiando la cantidad de universal '
                             'a particular, se llama conversión:',
                 'alternativas': ['Por accidente o limitación',
                                  'Total',
                                  'Simple',
                                  'Directa',
                                  'Contrapuesta'],
                 'correcta': 'A'},
                {'pregunta': 'En la conversión de «Todos los animales son '
                             'mamíferos» (A), la conversa válida «Algunos '
                             'mamíferos son animales» corresponde a la '
                             'proposición:',
                 'alternativas': ['A',
                                  'E',
                                  'Ninguna, no tiene conversa',
                                  'O',
                                  'I'],
                 'correcta': 'E'},
                {'pregunta': 'La proposición categórica que no tiene '
                             'conversa válida es la proposición:',
                 'alternativas': ['O',
                                  'I',
                                  'E',
                                  'Ninguna, todas tienen conversa',
                                  'A'],
                 'correcta': 'A'}],
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
                     {'titulo': 'OPOSICIÓN: CONTRARIOS Y SUBCONTRARIOS',
                      'items': ['Son contrarios los enunciados universales '
                                'A—E: nunca pueden ser verdaderos a la vez, '
                                'pero sí pueden ser ambos falsos.',
                                'Si «Todos los caballos son solípedos» (A) '
                                'es verdadero, entonces «Ningún caballo es '
                                'solípedo» (E) es falso.',
                                'Son subcontrarios los enunciados '
                                'particulares I—O: nunca pueden ser falsos a '
                                'la vez, pero sí pueden ser ambos '
                                'verdaderos.',
                                'Si «Algunos insectos son vertebrados» (I) '
                                'es falso, entonces «Algunos insectos no son '
                                'vertebrados» (O) es verdadero.']},
                     {'titulo': 'TIPOS DE CONVERSIÓN',
                      'items': ['La conversión simple conserva la cantidad; '
                                'es totalmente válida en los casos de '
                                'proposiciones E e I.',
                                'Ejemplo de conversión simple: «Ningún '
                                'escritor es analfabeto» (E) se convierte en '
                                '«Ningún analfabeto es escritor» (E).',
                                'La conversión por accidente o limitación '
                                'solo conserva la extensión; cambia la '
                                'cantidad de universal a particular.',
                                'Ejemplo: «Todos los animales son mamíferos» '
                                '(A) se convierte en «Algunos mamíferos son '
                                'animales» (I).',
                                'La proposición O no tiene conversa '
                                'válida.']},
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
                                'cuatro.']}],
  'qr_reto': [{'pregunta': 'De dos premisas negativas:',
               'respuesta': 'No se sigue conclusión alguna'},
              {'pregunta': 'De las premisas «Los cusqueños son peruanos» y '
                           '«Los anteños son cusqueños», la conclusión '
                           'pertinente sería:',
               'respuesta': 'Los anteños son peruanos'},
              {'pregunta': '«Todos los felinos andinos son carnívoros. El '
                           'puma es un felino; entonces, el puma es un '
                           'carnívoro» es un razonamiento de tipo:',
               'respuesta': 'Deductivo'}],
  'qr_dato': 'Reglas principales: de dos premisas negativas no se sigue '
             'conclusión; de dos premisas particulares tampoco; el término '
             'medio debe estar distribuido al menos una vez.'},
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
                                  'Aristóteles',
                                  'Russell',
                                  'George Boole'],
                 'correcta': 'E'},
                {'pregunta': 'El conjunto de todos los objetos que poseen '
                             'una característica común es una:',
                 'alternativas': ['Inferencia',
                                  'Variable',
                                  'Proposición',
                                  'Premisa',
                                  'Clase'],
                 'correcta': 'E'},
                {'pregunta': 'La clase que contiene todos los elementos del '
                             'universo del discurso es la clase:',
                 'alternativas': ['Particular',
                                  'Universal',
                                  'Nula',
                                  'Complementaria',
                                  'Vacía'],
                 'correcta': 'B'},
                {'pregunta': 'La clase universal se representa con el '
                             'símbolo:',
                 'alternativas': ['1', '∩', '0', 'Ā', '∪'],
                 'correcta': 'A'},
                {'pregunta': 'La clase que no contiene ningún elemento se '
                             'denomina:',
                 'alternativas': ['Unitaria',
                                  'Complementaria',
                                  'Universal',
                                  'Vacía o nula',
                                  'Particular'],
                 'correcta': 'D'},
                {'pregunta': 'La clase vacía se representa con el símbolo:',
                 'alternativas': ['0', '1', 'Ā', '∪', '∅ únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'El complemento de una clase A está formado por '
                             'los elementos que:',
                 'alternativas': ['No pertenecen a A',
                                  'Pertenecen a A y B',
                                  'Pertenecen a A',
                                  'Son universales',
                                  'Son comunes'],
                 'correcta': 'A'},
                {'pregunta': 'El complemento de la clase A se simboliza:',
                 'alternativas': ['A-B', 'A∩B', 'Ā', 'A∪B', '1'],
                 'correcta': 'C'},
                {'pregunta': 'La relación en que todos los elementos de una '
                             'clase están contenidos en otra es:',
                 'alternativas': ['Complemento',
                                  'Igualdad',
                                  'Diferencia',
                                  'Exclusión',
                                  'Inclusión'],
                 'correcta': 'E'},
                {'pregunta': 'La relación en que dos clases tienen '
                             'exactamente los mismos elementos es:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Inclusión',
                                  'Igualdad',
                                  'Exclusión'],
                 'correcta': 'D'},
                {'pregunta': 'La relación en que dos clases no tienen ningún '
                             'elemento en común es:',
                 'alternativas': ['Complemento',
                                  'Unión',
                                  'Exclusión',
                                  'Igualdad',
                                  'Inclusión'],
                 'correcta': 'C'},
                {'pregunta': 'La operación que reúne los elementos de ambas '
                             'clases es la:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Complementación',
                                  'Inclusión',
                                  'Diferencia'],
                 'correcta': 'B'},
                {'pregunta': 'La operación que reúne solo los elementos '
                             'comunes es la:',
                 'alternativas': ['Intersección',
                                  'Unión',
                                  'Diferencia',
                                  'Suma',
                                  'Complemento'],
                 'correcta': 'A'},
                {'pregunta': 'El símbolo ∪ representa la:',
                 'alternativas': ['Exclusión',
                                  'Inclusión',
                                  'Intersección',
                                  'Diferencia',
                                  'Unión'],
                 'correcta': 'E'},
                {'pregunta': 'El símbolo ∩ representa la:',
                 'alternativas': ['Unión',
                                  'Complemento',
                                  'Diferencia',
                                  'Igualdad',
                                  'Intersección'],
                 'correcta': 'E'},
                {'pregunta': 'La operación que toma los elementos de una '
                             'clase que no están en la otra es la:',
                 'alternativas': ['Intersección',
                                  'Inclusión',
                                  'Diferencia',
                                  'Igualdad',
                                  'Unión'],
                 'correcta': 'C'},
                {'pregunta': 'La lógica de clases se ocupa de las relaciones '
                             'entre:',
                 'alternativas': ['Falacias',
                                  'Clases o conjuntos',
                                  'Valores',
                                  'Silogismos',
                                  'Proposiciones'],
                 'correcta': 'B'},
                {'pregunta': '«Los peruanos» y «los no peruanos» son entre '
                             'sí:',
                 'alternativas': ['Clases complementarias',
                                  'Clases incluidas',
                                  'Clases idénticas',
                                  'Una sola clase',
                                  'Clases iguales'],
                 'correcta': 'A'},
                {'pregunta': 'La unión también recibe el nombre de:',
                 'alternativas': ['Resta',
                                  'Cociente',
                                  'Suma',
                                  'Potencia',
                                  'Producto'],
                 'correcta': 'C'},
                {'pregunta': 'La intersección también recibe el nombre de:',
                 'alternativas': ['Suma',
                                  'Producto',
                                  'Complemento',
                                  'Unión',
                                  'Diferencia'],
                 'correcta': 'B'},
                {'pregunta': 'El concepto de «universo del discurso», para '
                             'referirse a la clase universal, fue llamado '
                             'así por:',
                 'alternativas': ['De Morgan',
                                  'Leibniz',
                                  'George Boole',
                                  'Aristóteles',
                                  'Porfirio'],
                 'correcta': 'A'},
                {'pregunta': 'Además del número cero, la clase vacía también '
                             'se puede simbolizar con la letra griega:',
                 'alternativas': ['Omega', 'Fi', 'Alfa', 'Sigma', 'Pi'],
                 'correcta': 'B'},
                {'pregunta': 'La clase que tiene al menos un elemento, como '
                             'la clase de los alcaldes, se llama clase:',
                 'alternativas': ['Complementaria',
                                  'Nula',
                                  'Universal exclusiva',
                                  'Vacía',
                                  'No vacía'],
                 'correcta': 'E'},
                {'pregunta': 'El científico que desarrolló las primeras '
                             'aplicaciones del álgebra booleana a circuitos '
                             'digitales, en 1938, fue:',
                 'alternativas': ['Alan Turing',
                                  'George Boole',
                                  'Claudio Shannon',
                                  'Augustus De Morgan',
                                  'Gottlob Frege'],
                 'correcta': 'C'},
                {'pregunta': 'En el enunciado «El número de árboles» se '
                             'cumple la propiedad denominada: (I CEPRU '
                             '2024-II)',
                 'alternativas': ['Comprensión',
                                  'No-accidental',
                                  'Accidental',
                                  'Extensión',
                                  'Esencial'],
                 'correcta': 'D'},
                {'pregunta': 'En el cuadro de Boecio, la contraria de '
                             '«Ningún alumno es ateo» corresponde a: (I '
                             'CEPRU 2024-II)',
                 'alternativas': ['Algún alumno es ateo',
                                  'Ningún no-alumno es ateo',
                                  'Todo alumno es ateo',
                                  'Algunos alumnos no son ateos',
                                  'Algunos ateos son alumnos'],
                 'correcta': 'C'},
                {'pregunta': 'La obversa de «Los impopulares son no '
                             'exaltados» es: (I CEPRU 2024-II)',
                 'alternativas': ['Falso que algunos populares sean '
                                  'exaltados',
                                  'Los impopulares son serios',
                                  'No se acepta que los impopulares sean no '
                                  'exaltados',
                                  'Ningún impopular es exaltado',
                                  'Ningún popular no es no exaltado'],
                 'correcta': 'D'}],
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
                                'clase pero no a la otra.']}],
  'qr_reto': [{'pregunta': 'La clase universal se representa con el símbolo:',
               'respuesta': '1'},
              {'pregunta': 'La operación que toma los elementos de una clase '
                           'que no están en la otra es la:',
               'respuesta': 'Diferencia'},
              {'pregunta': 'El conjunto de todos los objetos que poseen una '
                           'característica común es una:',
               'respuesta': 'Clase'}],
  'qr_dato': 'Unión o suma: reúne los elementos de ambas clases. Se '
             'simboliza ∪.'},
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
                {'titulo': '17.4 ECUACIONES BOOLEANAS DE LAS PROPOSICIONES '
                           'TÍPICAS',
                 'items': ['La ecuación booleana de «Todo S es P» (A) es: {S '
                           '∩ P̅} = Φ (la intersección de S con el '
                           'complemento de P es vacía).',
                           'La ecuación booleana de «Ningún S es P» (E) es: '
                           '{S ∩ P} = Φ.',
                           'La ecuación booleana de «Algún S es P» (I) es: '
                           '{S ∩ P} ≠ Φ.',
                           'La ecuación booleana de «Algún S no es P» (O) '
                           'es: {S ∩ P̅} ≠ Φ.',
                           'El símbolo {Φ} representa la clase nula o vacía; '
                           'S ≠ Φ afirma que la clase S tiene {miembros}.',
                           'Con tres círculos rotulados S, P y M se '
                           'diagraman {ocho} clases distintas para evaluar '
                           'un silogismo.']},
                {'titulo': '17.5 VALIDEZ DEL SILOGISMO POR DIAGRAMAS',
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
                 'alternativas': ['Euler únicamente',
                                  'Boole',
                                  'Russell',
                                  'Venn',
                                  'Frege'],
                 'correcta': 'D'},
                {'pregunta': 'En un diagrama de Venn, el sombreado indica '
                             'que la región:',
                 'alternativas': ['Es dudosa',
                                  'Está vacía',
                                  'Es universal',
                                  'Es infinita',
                                  'Tiene elementos'],
                 'correcta': 'B'},
                {'pregunta': 'En un diagrama de Venn, la X indica que la '
                             'región:',
                 'alternativas': ['Se excluye',
                                  'Tiene al menos un elemento',
                                  'Es complementaria',
                                  'Está vacía',
                                  'Es universal'],
                 'correcta': 'B'},
                {'pregunta': '«Ningún S es P» se representa sombreando:',
                 'alternativas': ['El círculo P',
                                  'Nada',
                                  'Todo el círculo S',
                                  'La región común a S y P',
                                  'La región fuera de ambos'],
                 'correcta': 'D'},
                {'pregunta': '«Algún S es P» se representa colocando una X '
                             'en:',
                 'alternativas': ['Fuera de ambos círculos',
                                  'El círculo P completo',
                                  'La parte de S fuera de P',
                                  'El universo',
                                  'La región común a S y P'],
                 'correcta': 'E'},
                {'pregunta': '«Todo S es P» se representa sombreando:',
                 'alternativas': ['Todo el círculo P',
                                  'El universo',
                                  'Fuera de ambos',
                                  'La parte de S que no es P',
                                  'La región común'],
                 'correcta': 'D'},
                {'pregunta': '«Algún S no es P» se representa con una X en:',
                 'alternativas': ['El centro',
                                  'La región común',
                                  'La parte de S fuera de P',
                                  'El círculo P',
                                  'Fuera de ambos'],
                 'correcta': 'C'},
                {'pregunta': 'Con dos clases, el número de regiones que se '
                             'generan es:',
                 'alternativas': ['3', '4', '6', '2', '8'],
                 'correcta': 'B'},
                {'pregunta': 'Las proposiciones típicas son las que '
                             'corresponden a las formas:',
                 'alternativas': ['A, E, I, O',
                                  'Verdaderas y falsas',
                                  'Simples y compuestas',
                                  'Deductivas',
                                  'Universales solamente'],
                 'correcta': 'A'},
                {'pregunta': 'Las proposiciones atípicas requieren ser:',
                 'alternativas': ['Ignoradas',
                                  'Rechazadas',
                                  'Traducidas a una forma típica',
                                  'Negadas',
                                  'Convertidas en falacias'],
                 'correcta': 'C'},
                {'pregunta': 'Expresiones como «solo» y «únicamente» suelen '
                             'equivaler a juicios:',
                 'alternativas': ['Universales',
                                  'Negativos siempre',
                                  'Particulares',
                                  'Indefinidos',
                                  'Singulares'],
                 'correcta': 'A'},
                {'pregunta': 'Para evaluar la validez de un silogismo se '
                             'usan:',
                 'alternativas': ['Cinco círculos',
                                  'Cuatro círculos',
                                  'Dos círculos',
                                  'Tres círculos',
                                  'Un círculo'],
                 'correcta': 'D'},
                {'pregunta': 'Al evaluar un silogismo por diagramas, se '
                             'diagraman:',
                 'alternativas': ['Todo simultáneamente',
                                  'Solo la menor',
                                  'Solo las premisas',
                                  'Solo la mayor',
                                  'La conclusión primero'],
                 'correcta': 'C'},
                {'pregunta': 'Un silogismo es válido si, al diagramar las '
                             'premisas:',
                 'alternativas': ['Queda automáticamente representada la '
                                  'conclusión',
                                  'Se sombrean todos los círculos',
                                  'No hay ninguna X',
                                  'Las premisas son verdaderas',
                                  'Queda alguna región vacía'],
                 'correcta': 'A'},
                {'pregunta': 'Al diagramar conviene comenzar por las '
                             'premisas:',
                 'alternativas': ['Particulares',
                                  'Universales',
                                  'Negativas',
                                  'Más largas',
                                  'Afirmativas'],
                 'correcta': 'B'},
                {'pregunta': 'Una región en blanco en un diagrama de Venn '
                             'significa que:',
                 'alternativas': ['Tiene elementos',
                                  'Es contradictoria',
                                  'No se sabe si tiene elementos',
                                  'Está vacía',
                                  'Es universal'],
                 'correcta': 'C'},
                {'pregunta': 'El diagrama de Venn permite determinar de un '
                             'silogismo su:',
                 'alternativas': ['Validez formal',
                                  'Origen',
                                  'Verdad material',
                                  'Utilidad',
                                  'Belleza'],
                 'correcta': 'A'},
                {'pregunta': 'Los diagramas de Venn representan '
                             'gráficamente:',
                 'alternativas': ['Falacias',
                                  'Conectores lógicos',
                                  'Proposiciones compuestas',
                                  'Tablas de verdad',
                                  'Clases y sus relaciones'],
                 'correcta': 'E'},
                {'pregunta': 'En la diagramación, el círculo que se dibuja '
                             'para el término medio:',
                 'alternativas': ['Se dibuja intersecando a los otros dos',
                                  'No se dibuja',
                                  'Se dibuja aparte',
                                  'Se sombrea siempre',
                                  'Se marca con X'],
                 'correcta': 'A'},
                {'pregunta': 'Diagramar la conclusión antes que las premisas '
                             'constituye:',
                 'alternativas': ['Un error de método',
                                  'Una regla de Venn',
                                  'Un atajo permitido',
                                  'El procedimiento correcto',
                                  'Una simplificación válida'],
                 'correcta': 'A'},
                {'pregunta': 'De los 256 modos posibles del silogismo '
                             'categórico, el número considerado válido según '
                             'la lógica tradicional es:',
                 'alternativas': ['24', '256', '19', '15', '30'],
                 'correcta': 'C'},
                {'pregunta': 'La ley del contenido existencial se aplica en '
                             'un silogismo cuando ambas premisas son '
                             'universales y la conclusión es:',
                 'alternativas': ['Particular',
                                  'Indefinida',
                                  'Afirmativa exclusiva',
                                  'También universal',
                                  'Negativa exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La ecuación booleana de la proposición «Ningún '
                             'S es P» (E) es:',
                 'alternativas': ['S ∩ P̅ ≠ Φ',
                                  'S = Φ',
                                  'S ∩ P̅ = Φ',
                                  'S ∩ P = Φ',
                                  'S ∩ P ≠ Φ'],
                 'correcta': 'D'},
                {'pregunta': 'La ecuación booleana de la proposición «Algún '
                             'S es P» (I) es:',
                 'alternativas': ['S ≠ Φ',
                                  'S ∩ P̅ = Φ',
                                  'S ∩ P = Φ',
                                  'S ∩ P̅ ≠ Φ',
                                  'S ∩ P ≠ Φ'],
                 'correcta': 'E'},
                {'pregunta': 'La ecuación booleana de la proposición «Todo S '
                             'es P» (A) es:',
                 'alternativas': ['S ∩ P̅ ≠ Φ',
                                  'S ∩ P̅ = Φ',
                                  'S ∩ P ≠ Φ',
                                  'S ∩ P = Φ',
                                  'S = Φ'],
                 'correcta': 'B'},
                {'pregunta': 'El símbolo que representa la clase nula o '
                             'vacía en la lógica de clases es:',
                 'alternativas': ['Φ', '∪', '∩', '≠', 'S'],
                 'correcta': 'A'},
                {'pregunta': 'Para diagramar y evaluar la validez de un '
                             'silogismo mediante diagramas de Venn se '
                             'necesitan tres círculos rotulados S, P y:',
                 'alternativas': ['R', 'Q', 'T', 'N', 'M'],
                 'correcta': 'E'},
                {'pregunta': 'Con tres círculos rotulados S, P y M en un '
                             'diagrama de Venn, se representan un número de '
                             'clases distintas igual a:',
                 'alternativas': ['Cuatro', 'Ocho', 'Doce', 'Seis', 'Diez'],
                 'correcta': 'B'}],
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
                     {'titulo': 'ECUACIONES BOOLEANAS DE LAS PROPOSICIONES '
                                'TÍPICAS',
                      'items': ['La ecuación booleana de «Todo S es P» (A) '
                                'es: S ∩ P̅ = Φ (la intersección de S con el '
                                'complemento de P es vacía).',
                                'La ecuación booleana de «Ningún S es P» (E) '
                                'es: S ∩ P = Φ.',
                                'La ecuación booleana de «Algún S es P» (I) '
                                'es: S ∩ P ≠ Φ.',
                                'La ecuación booleana de «Algún S no es P» '
                                '(O) es: S ∩ P̅ ≠ Φ.',
                                'El símbolo Φ representa la clase nula o '
                                'vacía; S ≠ Φ afirma que la clase S tiene '
                                'miembros.',
                                'Con tres círculos rotulados S, P y M se '
                                'diagraman ocho clases distintas para '
                                'evaluar un silogismo.']},
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
                                'conclusión es particular.']}],
  'qr_reto': [{'pregunta': 'Expresiones como «solo» y «únicamente» suelen '
                           'equivaler a juicios:',
               'respuesta': 'Universales'},
              {'pregunta': 'La ley del contenido existencial se aplica en un '
                           'silogismo cuando ambas premisas son universales '
                           'y la conclusión es:',
               'respuesta': 'Particular'},
              {'pregunta': 'Al diagramar conviene comenzar por las premisas:',
               'respuesta': 'Universales'}],
  'qr_dato': 'La ley del contenido existencial se aplica cuando ambas '
             'premisas son universales y la conclusión es particular.'}]
