# ================================================================
# FICHAS DE ECONOMÍA — CEPRU UNSAAC
# Basado en el material oficial «Economía», Área C.
# ================================================================
"""Mismo formato que Historia: por cada balota, ficha de texto para
completar a dos columnas y banco de 20 preguntas, en versión alumno y
versión docente. Reutiliza el motor de fichas_historia.py.

ESTADO: 2 de 18 temas completos. Los 16 restantes se agregan por
tandas, igual que se hizo con Geografía y Cívica.

Integración: se usa a través de academia_cepru.py, no directamente.
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


ECONOMIA_TEMAS = [{'num': 1,
  'titulo': 'Conceptos Generales',
  'secciones': [{'titulo': '1.1 CONCEPTO DE ECONOMÍA',
                 'items': ['Según Raymond Barre, la economía es la ciencia '
                           'social dirigida a la administración de los '
                           '{escasos} recursos de las sociedades humanas.',
                           'La economía estudia la tensión entre los deseos '
                           '{ilimitados} y los medios {limitados} de los '
                           'agentes económicos.',
                           'La dicotomía central de la ciencia económica es '
                           '«múltiples necesidades por satisfacer» frente a '
                           'recursos {escasos}.']},
                {'titulo': '1.2 OBJETO DE ESTUDIO Y FINES',
                 'items': ['El objeto de estudio de la economía tiene como '
                           'fuente la {escasez} de recursos.',
                           'Los tres problemas económicos fundamentales son: '
                           '¿qué producir?, ¿{cuánto} producir? y ¿para '
                           'quién {producir}?',
                           'La economía {positiva} describe los fenómenos '
                           'económicos «lo que es»; la economía {normativa} '
                           'plantea «lo que debería ser».',
                           'El fin {práctico} de la economía es buscar el '
                           'bienestar general y una justa distribución de la '
                           '{riqueza}.']},
                {'titulo': '1.3 ESCASEZ Y COSTO DE OPORTUNIDAD',
                 'items': ['El {costo de oportunidad} es el costo de la '
                           'alternativa a la que se renuncia al tomar una '
                           'decisión.',
                           'El término «costo de oportunidad» fue acuñado '
                           'por {Friedrich von Wieser} en su obra de 1914.',
                           'El costo de oportunidad también se conoce como '
                           '«el valor de la mejor {opción} no seleccionada».',
                           'Toda {elección} conlleva un costo de '
                           'oportunidad, porque los recursos disponibles son '
                           'limitados.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según Raymond Barre, la economía es una ciencia '
                           'dirigida a la administración de recursos '
                           '{Escasos}.',
                           'La economía estudia la tensión entre los deseos '
                           'ilimitados y los medios {Limitados}.',
                           'El objeto de estudio de la economía tiene como '
                           'fuente principal {La escasez de recursos}.',
                           'Uno de los tres problemas económicos '
                           'fundamentales es {¿Qué producir?}.',
                           'La economía que describe los fenómenos '
                           'económicos tal como son se llama economía '
                           '{Positiva}.',
                           'La economía que plantea cómo deberían ser las '
                           'cosas se llama economía {Normativa}.',
                           'El fin práctico de la economía busca el '
                           'bienestar general y una distribución {Justa de '
                           'la riqueza}.',
                           'El costo de oportunidad se define como el costo '
                           'de {La alternativa a la que se renuncia al '
                           'decidir}.',
                           'El término «costo de oportunidad» fue acuñado '
                           'por {Friedrich von Wieser}.',
                           'El costo de oportunidad también se conoce como '
                           '{El valor de la mejor opción no seleccionada}.',
                           'Toda elección económica conlleva necesariamente '
                           '{Un costo de oportunidad}.',
                           'La obra donde se acuñó el término costo de '
                           'oportunidad se publicó en {1914}.',
                           'Si una población elige construir una escuela en '
                           'vez de una carretera, el costo de oportunidad es '
                           '{La carretera que se dejó de construir}.',
                           'El costo de oportunidad se aplica principalmente '
                           'en el ámbito {Financiero y económico}.',
                           'El costo de oportunidad se basa fundamentalmente '
                           'en la rentabilidad {Futura}.',
                           'La escasez obliga a la sociedad a determinar qué '
                           'necesidades satisfacer, lo que genera {La '
                           'elección}.',
                           'Según Barre, la economía estudia el '
                           'comportamiento humano en el uso de los recursos '
                           '{Con un costo}.',
                           'El objeto de estudio de la economía comprende '
                           'los fenómenos, hechos y conducta {Económicos}.',
                           'La dicotomía necesidades-recursos se resuelve '
                           'dando prioridad a las necesidades y generando '
                           'programas {De gasto ilimitado}.',
                           'El coste de oportunidad representa recursos que '
                           'se dejan de percibir por {No haber elegido la '
                           'mejor alternativa posible}.']}],
  'cuadros': [{'titulo': '1.3 ECONOMÍA POSITIVA Y NORMATIVA',
               'encabezados': ['Enfoque', 'Pregunta que responde'],
               'filas': [['Economía {positiva}', '«Lo que {es}»'],
                         ['Economía {normativa}',
                          '«Lo que {debería} ser»']]}],
  'preguntas': [{'pregunta': 'Según Raymond Barre, la economía es una '
                             'ciencia dirigida a la administración de '
                             'recursos:',
                 'alternativas': ['Abundantes',
                                  'Escasos',
                                  'Ilimitados',
                                  'Gratuitos',
                                  'Renovables exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La economía estudia la tensión entre los '
                             'deseos ilimitados y los medios:',
                 'alternativas': ['Abundantes',
                                  'Limitados',
                                  'Infinitos',
                                  'Renovables',
                                  'Gratuitos'],
                 'correcta': 'B'},
                {'pregunta': 'El objeto de estudio de la economía tiene como '
                             'fuente principal:',
                 'alternativas': ['La abundancia',
                                  'La escasez de recursos',
                                  'El comercio internacional',
                                  'La política monetaria',
                                  'El crecimiento poblacional'],
                 'correcta': 'B'},
                {'pregunta': 'Uno de los tres problemas económicos '
                             'fundamentales es:',
                 'alternativas': ['¿Cuándo producir?',
                                  '¿Qué producir?',
                                  '¿Dónde comprar?',
                                  '¿Quién gobierna?',
                                  '¿Cómo votar?'],
                 'correcta': 'B'},
                {'pregunta': 'La economía que describe los fenómenos '
                             'económicos tal como son se llama economía:',
                 'alternativas': ['Normativa',
                                  'Positiva',
                                  'Aplicada',
                                  'Social',
                                  'Financiera'],
                 'correcta': 'B'},
                {'pregunta': 'La economía que plantea cómo deberían ser las '
                             'cosas se llama economía:',
                 'alternativas': ['Positiva',
                                  'Normativa',
                                  'Descriptiva',
                                  'Clásica',
                                  'Neutra'],
                 'correcta': 'B'},
                {'pregunta': 'El fin práctico de la economía busca el '
                             'bienestar general y una distribución:',
                 'alternativas': ['Desigual de la riqueza',
                                  'Justa de la riqueza',
                                  'Nula de recursos',
                                  'Exclusiva para el Estado',
                                  'Solo para las empresas'],
                 'correcta': 'B'},
                {'pregunta': 'El costo de oportunidad se define como el '
                             'costo de:',
                 'alternativas': ['Todo lo que se compra',
                                  'La alternativa a la que se renuncia al '
                                  'decidir',
                                  'El dinero disponible',
                                  'El tiempo libre',
                                  'La inflación anual'],
                 'correcta': 'B'},
                {'pregunta': 'El término «costo de oportunidad» fue acuñado '
                             'por:',
                 'alternativas': ['Adam Smith',
                                  'Friedrich von Wieser',
                                  'Karl Marx',
                                  'John Maynard Keynes',
                                  'David Ricardo'],
                 'correcta': 'B'},
                {'pregunta': 'El costo de oportunidad también se conoce '
                             'como:',
                 'alternativas': ['El precio de mercado',
                                  'El valor de la mejor opción no '
                                  'seleccionada',
                                  'La tasa de interés',
                                  'El producto bruto interno',
                                  'La inflación acumulada'],
                 'correcta': 'B'},
                {'pregunta': 'Toda elección económica conlleva '
                             'necesariamente:',
                 'alternativas': ['Una ganancia garantizada',
                                  'Un costo de oportunidad',
                                  'La eliminación de la escasez',
                                  'Un aumento de precios',
                                  'Una pérdida total'],
                 'correcta': 'B'},
                {'pregunta': 'La obra donde se acuñó el término costo de '
                             'oportunidad se publicó en:',
                 'alternativas': ['1890', '1914', '1950', '1776', '2000'],
                 'correcta': 'B'},
                {'pregunta': 'Si una población elige construir una escuela '
                             'en vez de una carretera, el costo de '
                             'oportunidad es:',
                 'alternativas': ['El dinero gastado en la escuela',
                                  'La carretera que se dejó de construir',
                                  'El tiempo de construcción',
                                  'El material usado',
                                  'Los trabajadores empleados'],
                 'correcta': 'B'},
                {'pregunta': 'El costo de oportunidad se aplica '
                             'principalmente en el ámbito:',
                 'alternativas': ['Solo deportivo',
                                  'Financiero y económico',
                                  'Solo artístico',
                                  'Solo educativo',
                                  'Solo religioso'],
                 'correcta': 'B'},
                {'pregunta': 'El costo de oportunidad se basa '
                             'fundamentalmente en la rentabilidad:',
                 'alternativas': ['Pasada',
                                  'Futura',
                                  'Inexistente',
                                  'Solo inmediata',
                                  'Solo simbólica'],
                 'correcta': 'B'},
                {'pregunta': 'La escasez obliga a la sociedad a determinar '
                             'qué necesidades satisfacer, lo que genera:',
                 'alternativas': ['Abundancia',
                                  'La elección',
                                  'Igualdad absoluta',
                                  'Ausencia de problemas',
                                  'Riqueza ilimitada'],
                 'correcta': 'B'},
                {'pregunta': 'Según Barre, la economía estudia el '
                             'comportamiento humano en el uso de los '
                             'recursos:',
                 'alternativas': ['Sin ningún costo',
                                  'Con un costo',
                                  'De forma gratuita',
                                  'Sin limitaciones',
                                  'De manera aleatoria'],
                 'correcta': 'B'},
                {'pregunta': 'El objeto de estudio de la economía comprende '
                             'los fenómenos, hechos y conducta:',
                 'alternativas': ['Políticos',
                                  'Económicos',
                                  'Religiosos',
                                  'Deportivos',
                                  'Artísticos'],
                 'correcta': 'B'},
                {'pregunta': 'La dicotomía necesidades-recursos se resuelve '
                             'dando prioridad a las necesidades y generando '
                             'programas:',
                 'alternativas': ['De uso óptimo de los recursos',
                                  'De gasto ilimitado',
                                  'De abandono de la producción',
                                  'Sin ninguna planificación',
                                  'De reducción poblacional'],
                 'correcta': 'B'},
                {'pregunta': 'El coste de oportunidad representa recursos '
                             'que se dejan de percibir por:',
                 'alternativas': ['Elegir siempre correctamente',
                                  'No haber elegido la mejor alternativa '
                                  'posible',
                                  'Tener recursos ilimitados',
                                  'No participar en el mercado',
                                  'Ahorrar en exceso'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'Necesidades Humanas',
  'secciones': [{'titulo': '2.1 CONCEPTO Y ORIGEN',
                 'items': ['Necesidad es la sensación de {carencia} o '
                           'insuficiencia, material o inmaterial, que el '
                           'hombre experimenta por sus exigencias corporales '
                           'o espirituales.',
                           'Las necesidades tienen carácter {relativo}, '
                           'porque el concepto de bienestar no es uniforme '
                           'para todos los hombres.',
                           'Un origen de las necesidades es la exigencia '
                           '{biológica} de reponer las energías del '
                           'organismo.',
                           'Otro origen es el permanente {desarrollo} de la '
                           'sociedad, que aumenta los bienes y servicios que '
                           'el hombre precisa.']},
                {'titulo': '2.2 LA PIRÁMIDE DE MASLOW',
                 'items': ['La teoría de la jerarquización de las '
                           'necesidades fue planteada en la década de los 40 '
                           'por {Abraham Maslow}.',
                           'Maslow expuso su teoría en el libro «{Motivation '
                           'and Personality}», de 1954.',
                           'El primer nivel de la pirámide corresponde a las '
                           'necesidades {fisiológicas}, como la alimentación '
                           'y el descanso.',
                           'El segundo nivel corresponde a las necesidades '
                           'de {seguridad}, como un seguro médico.',
                           'El tercer nivel corresponde a las necesidades '
                           '{sociales} o de filiación, como la amistad.',
                           'El cuarto nivel corresponde a las necesidades de '
                           '{estima}, como el prestigio y el reconocimiento.',
                           'El quinto y último nivel corresponde a las '
                           'necesidades de {autorrealización}.']},
                {'titulo': '2.3 LEYES DE LAS NECESIDADES',
                 'items': ['La ley de la {infinidad} de las necesidades '
                           'establece que el ser humano tiene múltiples '
                           'necesidades en permanente incremento.',
                           'La ley de {saturación} de las necesidades, o '
                           'limitadas en capacidad, indica que basta una '
                           'cantidad determinada de un bien para satisfacer '
                           'una necesidad.',
                           'La ley de saturación también se conoce como la '
                           'ley de {Gossen}, formulada por Hermann Heinrich '
                           'Gossen.',
                           'Según la ley de Gossen, la satisfacción '
                           'suplementaria de un bien disminuye a medida que '
                           'aumenta la cantidad {consumida}.',
                           'La ley de la {variación} en intensidad indica '
                           'que las necesidades no se perciben con la misma '
                           'urgencia.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Una necesidad se define como la sensación de '
                           '{Carencia o insuficiencia}.',
                           'Las necesidades tienen un carácter {Relativo}.',
                           'La exigencia biológica de reponer energías es un '
                           'origen de las necesidades de tipo {Biológico}.',
                           'La teoría de la jerarquización de las '
                           'necesidades fue planteada por {Abraham Maslow}.',
                           'Maslow planteó su teoría de las necesidades en '
                           'la década de {Los 40}.',
                           'La obra donde Maslow expone su teoría se titula '
                           '{Motivation and Personality}.',
                           'El primer nivel de la pirámide de Maslow '
                           'corresponde a las necesidades {Fisiológicas}.',
                           'Las necesidades de seguridad incluyen, por '
                           'ejemplo {Un seguro médico}.',
                           'Las necesidades sociales también se conocen como '
                           'necesidades de {Filiación}.',
                           'Las necesidades de estima se expresan en el '
                           'sentimiento de independencia y {Prestigio y '
                           'reconocimiento}.',
                           'El nivel más alto de la pirámide de Maslow '
                           'corresponde a las necesidades de '
                           '{Autorrealización}.',
                           'La ley que establece que el ser humano tiene '
                           'múltiples necesidades en aumento se llama ley de '
                           '{Infinidad de las necesidades}.',
                           'La ley que indica que basta una cantidad '
                           'determinada de un bien para satisfacer una '
                           'necesidad es la ley de {Saturación o limitadas '
                           'en capacidad}.',
                           'La ley de saturación también se conoce como la '
                           'ley de {Gossen}.',
                           'Según la ley de Gossen, la satisfacción '
                           'suplementaria de un bien {Disminuye a medida que '
                           'aumenta el consumo}.',
                           'Hermann Heinrich Gossen es recordado en la '
                           'historia del pensamiento {Económico}.',
                           'La ley de la variación en intensidad indica que '
                           'las necesidades {No se perciben con la misma '
                           'urgencia}.',
                           'El desarrollo permanente de la sociedad genera '
                           'un aumento de {Los bienes y servicios que el '
                           'hombre precisa}.',
                           'El hombre es considerado, según el texto, un ser '
                           '{Biopsicosocial}.',
                           'Las necesidades deben ser aplacadas mediante el '
                           'consumo de {Bienes y servicios}.']}],
  'cuadros': [{'titulo': '2.2 NIVELES DE LA PIRÁMIDE DE MASLOW',
               'encabezados': ['Nivel', 'Necesidad'],
               'filas': [['1', '{Fisiológicas}'],
                         ['2', '{Seguridad}'],
                         ['3', '{Sociales} o filiación'],
                         ['4', 'De {estima}'],
                         ['5', '{Autorrealización}']]}],
  'preguntas': [{'pregunta': 'Una necesidad se define como la sensación de:',
                 'alternativas': ['Abundancia',
                                  'Carencia o insuficiencia',
                                  'Riqueza excesiva',
                                  'Satisfacción plena',
                                  'Bienestar total'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades tienen un carácter:',
                 'alternativas': ['Absoluto e igual para todos',
                                  'Relativo',
                                  'Inexistente',
                                  'Fijo por ley',
                                  'Universal idéntico'],
                 'correcta': 'B'},
                {'pregunta': 'La exigencia biológica de reponer energías es '
                             'un origen de las necesidades de tipo:',
                 'alternativas': ['Social',
                                  'Biológico',
                                  'Político',
                                  'Cultural exclusivo',
                                  'Artístico'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la jerarquización de las '
                             'necesidades fue planteada por:',
                 'alternativas': ['Adam Smith',
                                  'Abraham Maslow',
                                  'Karl Marx',
                                  'Hermann Gossen',
                                  'John Keynes'],
                 'correcta': 'B'},
                {'pregunta': 'Maslow planteó su teoría de las necesidades en '
                             'la década de:',
                 'alternativas': ['Los 20',
                                  'Los 40',
                                  'Los 60',
                                  'Los 80',
                                  'Los 90'],
                 'correcta': 'B'},
                {'pregunta': 'La obra donde Maslow expone su teoría se '
                             'titula:',
                 'alternativas': ['El Capital',
                                  'Motivation and Personality',
                                  'La riqueza de las naciones',
                                  'Teoría general del empleo',
                                  'Principios de economía'],
                 'correcta': 'B'},
                {'pregunta': 'El primer nivel de la pirámide de Maslow '
                             'corresponde a las necesidades:',
                 'alternativas': ['De estima',
                                  'Fisiológicas',
                                  'Sociales',
                                  'De seguridad',
                                  'De autorrealización'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades de seguridad incluyen, por '
                             'ejemplo:',
                 'alternativas': ['La amistad',
                                  'Un seguro médico',
                                  'El prestigio',
                                  'La alimentación',
                                  'El ocio'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades sociales también se conocen '
                             'como necesidades de:',
                 'alternativas': ['Estima',
                                  'Filiación',
                                  'Autorrealización',
                                  'Seguridad',
                                  'Subsistencia'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades de estima se expresan en el '
                             'sentimiento de independencia y:',
                 'alternativas': ['Hambre',
                                  'Prestigio y reconocimiento',
                                  'Sed',
                                  'Sueño',
                                  'Frío'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel más alto de la pirámide de Maslow '
                             'corresponde a las necesidades de:',
                 'alternativas': ['Seguridad',
                                  'Autorrealización',
                                  'Estima',
                                  'Fisiológicas',
                                  'Sociales'],
                 'correcta': 'B'},
                {'pregunta': 'La ley que establece que el ser humano tiene '
                             'múltiples necesidades en aumento se llama ley '
                             'de:',
                 'alternativas': ['Saturación',
                                  'Infinidad de las necesidades',
                                  'Variación en intensidad',
                                  'Gossen exclusivamente',
                                  'Escasez'],
                 'correcta': 'B'},
                {'pregunta': 'La ley que indica que basta una cantidad '
                             'determinada de un bien para satisfacer una '
                             'necesidad es la ley de:',
                 'alternativas': ['Infinidad',
                                  'Saturación o limitadas en capacidad',
                                  'Variación en intensidad',
                                  'Oferta',
                                  'Demanda'],
                 'correcta': 'B'},
                {'pregunta': 'La ley de saturación también se conoce como la '
                             'ley de:',
                 'alternativas': ['Maslow',
                                  'Gossen',
                                  'Barre',
                                  'Wieser',
                                  'Smith'],
                 'correcta': 'B'},
                {'pregunta': 'Según la ley de Gossen, la satisfacción '
                             'suplementaria de un bien:',
                 'alternativas': ['Aumenta indefinidamente',
                                  'Disminuye a medida que aumenta el consumo',
                                  'Se mantiene constante',
                                  'No tiene relación con el consumo',
                                  'Se duplica siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Hermann Heinrich Gossen es recordado en la '
                             'historia del pensamiento:',
                 'alternativas': ['Político',
                                  'Económico',
                                  'Religioso',
                                  'Artístico',
                                  'Militar'],
                 'correcta': 'B'},
                {'pregunta': 'La ley de la variación en intensidad indica '
                             'que las necesidades:',
                 'alternativas': ['Se satisfacen todas con la misma urgencia',
                                  'No se perciben con la misma urgencia',
                                  'Son siempre iguales',
                                  'No varían nunca',
                                  'Desaparecen con el tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo permanente de la sociedad genera '
                             'un aumento de:',
                 'alternativas': ['La escasez absoluta',
                                  'Los bienes y servicios que el hombre '
                                  'precisa',
                                  'La pobreza generalizada',
                                  'El desempleo',
                                  'La informalidad'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre es considerado, según el texto, un '
                             'ser:',
                 'alternativas': ['Puramente biológico',
                                  'Biopsicosocial',
                                  'Solo económico',
                                  'Exclusivamente racional',
                                  'Solo espiritual'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades deben ser aplacadas mediante '
                             'el consumo de:',
                 'alternativas': ['Solo dinero',
                                  'Bienes y servicios',
                                  'Solo tiempo libre',
                                  'Solo información',
                                  'Solo tecnología'],
                 'correcta': 'B'}]}]
