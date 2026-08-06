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
                 'correcta': 'B'}]},
 {'num': 3,
  'titulo': 'Bienes y Servicios',
  'secciones': [{'titulo': '3.1 CONCEPTO DE BIENES Y RECURSOS ECONÓMICOS',
                 'items': ['Los bienes son objetos que satisfacen '
                           'necesidades humanas; también se les conoce como '
                           '{satisfactores}.',
                           'Un {recurso económico} es todo recurso natural '
                           'susceptible de ser transformado en bienes y '
                           'riqueza.']},
                {'titulo': '3.2 BIENES LIBRES Y BIENES ECONÓMICOS',
                 'items': ['Los bienes {no económicos} o libres son '
                           'abundantes en la naturaleza y no tienen relación '
                           'de {pertenencia}.',
                           'Los bienes libres se aprovechan con un {mínimo} '
                           'esfuerzo; ejemplo: el aire y la energía solar.',
                           'Los bienes {económicos} requieren de la '
                           'intervención del ser humano para extraerlos o '
                           'transformarlos.',
                           'Los bienes económicos son {escasos}, lo que les '
                           'genera valor de {cambio}.',
                           'Los bienes económicos son útiles porque poseen '
                           'valor de {uso}, y son susceptibles de ser '
                           '{transados} o vendidos.']},
                {'titulo': '3.3 CLASIFICACIÓN DE LOS BIENES ECONÓMICOS',
                 'items': ['Por su naturaleza, los bienes pueden ser '
                           '{materiales} o tangibles, y {inmateriales} o '
                           'intangibles.',
                           'Por su función, los bienes {intermedios} '
                           'requieren transformación previa; los bienes '
                           '{finales} están listos para el consumo.',
                           'Los bienes intermedios también se llaman '
                           '{presatisfacientes}; los bienes finales se '
                           'llaman {satisfacientes}.',
                           'Por su duración, los bienes {fungibles} se '
                           'utilizan una sola vez, como los alimentos.',
                           'Los bienes {infungibles} se utilizan varias '
                           'veces y no se agotan en su primer uso, como los '
                           'vestidos.',
                           'Según el Código Civil peruano de {1984}, los '
                           'bienes se clasifican en muebles e {inmuebles}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los bienes también son conocidos con el nombre '
                           'de {Satisfactores}.',
                           'Un recurso económico se define como aquel '
                           'susceptible de ser transformado en {Bienes y '
                           'riqueza}.',
                           'Los bienes no económicos o libres se '
                           'caracterizan por ser {Abundantes en la '
                           'naturaleza}.',
                           'Los bienes libres se caracterizan porque {No '
                           'tienen relación de pertenencia}.',
                           'Un ejemplo típico de bien libre es {El aire}.',
                           'Los bienes económicos requieren, para obtenerse, '
                           'la intervención de {El ser humano con su '
                           'esfuerzo}.',
                           'Los bienes económicos son escasos, lo que les '
                           'genera {Valor de cambio}.',
                           'Por su naturaleza, los bienes que pueden ser '
                           'percibidos por los sentidos se llaman bienes '
                           '{Materiales o tangibles}.',
                           'Las ideas, teorías y derechos de autor son '
                           'ejemplos de bienes {Inmateriales o intangibles}.',
                           'Los bienes que requieren transformación previa '
                           'antes de consumirse se llaman bienes '
                           '{Intermedios}.',
                           'Los bienes intermedios también se denominan '
                           'bienes {Presatisfacientes}.',
                           'Los bienes listos para el consumo directo se '
                           'llaman bienes {Finales o satisfacientes}.',
                           'La harina para hacer fideos es un ejemplo de '
                           'bien {Intermedio}.',
                           'El pan, la ropa y la leche son ejemplos de '
                           'bienes {Finales}.',
                           'Los bienes que se utilizan una sola vez y '
                           'desaparecen en su primer uso se llaman bienes '
                           '{Fungibles}.',
                           'Los bienes que se utilizan varias veces sin '
                           'agotarse en el primer uso se llaman bienes '
                           '{Infungibles o duraderos}.',
                           'Los alimentos y las materias primas son ejemplos '
                           'de bienes {Fungibles}.',
                           'Los vestidos, zapatos y libros son ejemplos de '
                           'bienes {Infungibles}.',
                           'El Código Civil peruano que clasifica los bienes '
                           'en muebles e inmuebles está vigente desde '
                           '{1984}.',
                           'Los bienes muebles se caracterizan porque pueden '
                           'trasladarse de un lugar a otro {Con suma '
                           'facilidad y sin ser destruidos}.']},
                {'titulo': '3.5 BIENES PÚBLICOS',
                 'items': ['Un {bien público} es aquel cuyo consumo es '
                           '{indivisible} y puede ser compartido por todos '
                           'sin exclusión.',
                           'Los bienes públicos {puros} tienen coste '
                           'marginal {nulo} por cada usuario adicional, como '
                           'la defensa nacional.',
                           'Los bienes públicos {impuros} tienen consumo '
                           'parcialmente {rival}, como las vías públicas.',
                           'Los bienes públicos se caracterizan por '
                           'consumirse {conjuntamente}, sin poder excluir a '
                           'nadie, y sin {rivalidad}.']},
                {'titulo': '3.6 LOS SERVICIOS: CONCEPTO Y CARACTERÍSTICAS',
                 'items': ['Los {servicios} son actividades económicas que '
                           'satisfacen directamente necesidades de otras '
                           'personas.',
                           'Los servicios también se conocen como trabajo '
                           '{no productivo}, a diferencia del trabajo que '
                           'crea bienes materiales.',
                           'Los servicios son {inmateriales} o intangibles: '
                           'no pueden percibirse materialmente.',
                           'Los servicios se {consumen} al mismo tiempo que '
                           'se producen, por lo que no pueden {acumularse} '
                           'ni ahorrarse.',
                           'La prestación de un servicio requiere del uso de '
                           '{bienes} necesarios para realizarla.']},
                {'titulo': '3.7 CLASIFICACIÓN DE LOS SERVICIOS',
                 'items': ['Según quién los brinda, los servicios pueden ser '
                           '{privados}, administrados por la empresa '
                           'privada, o {públicos}.',
                           'Los servicios económicos tienen como precio una '
                           '{tarifa}.']}],
  'cuadros': [{'titulo': '3.2 BIENES LIBRES FRENTE A BIENES ECONÓMICOS',
               'encabezados': ['Aspecto',
                               'Bienes libres',
                               'Bienes económicos'],
               'filas': [['Abundancia', '{Abundantes}', '{Escasos}'],
                         ['Propietario', '{No} tienen', '{Sí} tienen'],
                         ['Esfuerzo',
                          '{Mínimo}',
                          'Con {tecnología} y trabajo']]}],
  'preguntas': [{'pregunta': 'Los bienes también son conocidos con el nombre '
                             'de:',
                 'alternativas': ['Recursos naturales',
                                  'Satisfactores',
                                  'Factores productivos',
                                  'Insumos exclusivos',
                                  'Servicios'],
                 'correcta': 'B'},
                {'pregunta': 'Un recurso económico se define como aquel '
                             'susceptible de ser transformado en:',
                 'alternativas': ['Dinero exclusivamente',
                                  'Bienes y riqueza',
                                  'Impuestos',
                                  'Deuda pública',
                                  'Inflación'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes no económicos o libres se '
                             'caracterizan por ser:',
                 'alternativas': ['Escasos',
                                  'Abundantes en la naturaleza',
                                  'Producidos por el hombre',
                                  'Costosos',
                                  'Transables en el mercado'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes libres se caracterizan porque:',
                 'alternativas': ['Tienen propietario',
                                  'No tienen relación de pertenencia',
                                  'Requieren gran esfuerzo',
                                  'Son transformados industrialmente',
                                  'Generan valor de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'Un ejemplo típico de bien libre es:',
                 'alternativas': ['Un automóvil',
                                  'El aire',
                                  'Una computadora',
                                  'Una vivienda',
                                  'Un libro'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes económicos requieren, para '
                             'obtenerse, la intervención de:',
                 'alternativas': ['La naturaleza sin más',
                                  'El ser humano con su esfuerzo',
                                  'Ningún factor productivo',
                                  'Solo el clima',
                                  'Solo el azar'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes económicos son escasos, lo que les '
                             'genera:',
                 'alternativas': ['Valor de uso únicamente',
                                  'Valor de cambio',
                                  'Abundancia',
                                  'Gratuidad',
                                  'Ausencia de mercado'],
                 'correcta': 'B'},
                {'pregunta': 'Por su naturaleza, los bienes que pueden ser '
                             'percibidos por los sentidos se llaman bienes:',
                 'alternativas': ['Inmateriales',
                                  'Materiales o tangibles',
                                  'Intermedios',
                                  'Fungibles',
                                  'Finales'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas, teorías y derechos de autor son '
                             'ejemplos de bienes:',
                 'alternativas': ['Materiales',
                                  'Inmateriales o intangibles',
                                  'Fungibles',
                                  'De consumo industrial',
                                  'Muebles'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes que requieren transformación previa '
                             'antes de consumirse se llaman bienes:',
                 'alternativas': ['Finales',
                                  'Intermedios',
                                  'Fungibles',
                                  'Libres',
                                  'Inmuebles'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes intermedios también se denominan '
                             'bienes:',
                 'alternativas': ['Satisfacientes',
                                  'Presatisfacientes',
                                  'Finales',
                                  'Muebles',
                                  'Libres'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes listos para el consumo directo se '
                             'llaman bienes:',
                 'alternativas': ['Intermedios',
                                  'Finales o satisfacientes',
                                  'Presatisfacientes',
                                  'Libres',
                                  'Inmuebles'],
                 'correcta': 'B'},
                {'pregunta': 'La harina para hacer fideos es un ejemplo de '
                             'bien:',
                 'alternativas': ['Final',
                                  'Intermedio',
                                  'Libre',
                                  'Inmueble',
                                  'Fungible exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El pan, la ropa y la leche son ejemplos de '
                             'bienes:',
                 'alternativas': ['Intermedios',
                                  'Finales',
                                  'Libres',
                                  'Inmuebles',
                                  'No económicos'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes que se utilizan una sola vez y '
                             'desaparecen en su primer uso se llaman bienes:',
                 'alternativas': ['Infungibles',
                                  'Fungibles',
                                  'Inmuebles',
                                  'Intermedios',
                                  'Libres'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes que se utilizan varias veces sin '
                             'agotarse en el primer uso se llaman bienes:',
                 'alternativas': ['Fungibles',
                                  'Infungibles o duraderos',
                                  'Libres',
                                  'Presatisfacientes',
                                  'Muebles exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los alimentos y las materias primas son '
                             'ejemplos de bienes:',
                 'alternativas': ['Infungibles',
                                  'Fungibles',
                                  'Inmuebles',
                                  'Finales exclusivos',
                                  'Libres'],
                 'correcta': 'B'},
                {'pregunta': 'Los vestidos, zapatos y libros son ejemplos de '
                             'bienes:',
                 'alternativas': ['Fungibles',
                                  'Infungibles',
                                  'Libres',
                                  'Intermedios exclusivos',
                                  'No económicos'],
                 'correcta': 'B'},
                {'pregunta': 'El Código Civil peruano que clasifica los '
                             'bienes en muebles e inmuebles está vigente '
                             'desde:',
                 'alternativas': ['1970', '1984', '1993', '2000', '1950'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes muebles se caracterizan porque '
                             'pueden trasladarse de un lugar a otro:',
                 'alternativas': ['Solo con gran dificultad',
                                  'Con suma facilidad y sin ser destruidos',
                                  'Nunca',
                                  'Solo destruyéndolos',
                                  'Solo con maquinaria pesada'],
                 'correcta': 'B'},
                {'pregunta': 'Un bien público se caracteriza porque su '
                             'consumo es:',
                 'alternativas': ['Exclusivo de quien paga',
                                  'Indivisible y compartido sin exclusión',
                                  'Solo para el Estado',
                                  'Prohibido para particulares',
                                  'Limitado a una sola persona'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes públicos puros tienen un coste '
                             'marginal, por cada usuario adicional, que es:',
                 'alternativas': ['Muy alto',
                                  'Nulo',
                                  'Variable según el consumidor',
                                  'Igual al precio de mercado',
                                  'Creciente exponencialmente'],
                 'correcta': 'B'},
                {'pregunta': 'La defensa nacional es un ejemplo típico de '
                             'bien público:',
                 'alternativas': ['Impuro',
                                  'Puro',
                                  'Privado',
                                  'Mixto exclusivo',
                                  'Rival'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes públicos impuros, como las vías '
                             'públicas, tienen un consumo:',
                 'alternativas': ['No rival en absoluto',
                                  'Parcialmente rival',
                                  'Totalmente excluyente',
                                  'Solo privado',
                                  'Inexistente'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes públicos se caracterizan por '
                             'consumirse conjuntamente y sin:',
                 'alternativas': ['Costo alguno',
                                  'Rivalidad',
                                  'Ningún usuario',
                                  'Producción estatal',
                                  'Regulación'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se definen como actividades '
                             'económicas que satisfacen directamente '
                             'necesidades de:',
                 'alternativas': ['Solo quien las produce',
                                  'Otras personas',
                                  'Solo el Estado',
                                  'Ninguna persona en particular',
                                  'Solo empresas'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios también se conocen con el nombre '
                             'de trabajo:',
                 'alternativas': ['Productivo',
                                  'No productivo',
                                  'Manual exclusivo',
                                  'Intelectual exclusivo',
                                  'Físico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se caracterizan por ser '
                             'inmateriales, es decir:',
                 'alternativas': ['Se pueden almacenar',
                                  'No pueden percibirse materialmente',
                                  'Son siempre gratuitos',
                                  'Solo los presta el Estado',
                                  'Duran para siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se consumen al mismo tiempo que '
                             'se:',
                 'alternativas': ['Almacenan',
                                  'Producen',
                                  'Exportan',
                                  'Prohíben',
                                  'Regulan'],
                 'correcta': 'B'},
                {'pregunta': 'Debido a que se consumen al momento de '
                             'producirse, los servicios no pueden:',
                 'alternativas': ['Venderse',
                                  'Acumularse o ahorrarse',
                                  'Prestarse',
                                  'Tener tarifa',
                                  'Ser regulados'],
                 'correcta': 'B'},
                {'pregunta': 'La prestación de cualquier servicio requiere '
                             'del uso de:',
                 'alternativas': ['Ningún recurso adicional',
                                  'Bienes u objetos necesarios',
                                  'Solo dinero',
                                  'Solo mano de obra sin herramientas',
                                  'Solo tecnología avanzada'],
                 'correcta': 'B'},
                {'pregunta': 'Según quién los brinda, los servicios pueden '
                             'clasificarse en privados y:',
                 'alternativas': ['Informales',
                                  'Públicos',
                                  'Ilegales',
                                  'Extranjeros exclusivos',
                                  'Gratuitos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios privados son administrados y '
                             'organizados por:',
                 'alternativas': ['El Estado exclusivamente',
                                  'La empresa privada',
                                  'Organismos internacionales',
                                  'El gobierno regional exclusivo',
                                  'Ninguna institución'],
                 'correcta': 'B'},
                {'pregunta': 'Se considera que un servicio es económico '
                             'cuando tiene como precio:',
                 'alternativas': ['Un impuesto',
                                  'Una tarifa',
                                  'Un salario',
                                  'Una multa',
                                  'Un subsidio'],
                 'correcta': 'B'},
                {'pregunta': 'La atención médica, la educación y el '
                             'transporte público son ejemplos de:',
                 'alternativas': ['Bienes tangibles',
                                  'Servicios',
                                  'Bienes públicos puros exclusivos',
                                  'Materias primas',
                                  'Bienes de capital'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'Proceso Económico',
  'secciones': [{'titulo': '4.1 CONCEPTO Y FASES',
                 'items': ['El proceso económico es el conjunto de '
                           'actividades económicas que realizan los seres '
                           'humanos para obtener recursos que satisfagan sus '
                           '{necesidades}.',
                           'El proceso económico es {continuo} e '
                           'interrelacionado, y sintetiza la actividad '
                           'económica global de una sociedad.',
                           'Las cinco fases del proceso económico son: '
                           '{producción}, circulación, distribución, '
                           '{consumo} e inversión.']},
                {'titulo': '4.2 LAS FASES DEL PROCESO ECONÓMICO',
                 'items': ['La {producción} es la actividad social orientada '
                           'a generar los bienes y servicios que permiten '
                           'satisfacer necesidades.',
                           'En la producción aparece el {valor agregado} '
                           'sobre elementos como las materias primas.',
                           'La {circulación} es la fase donde la producción '
                           'se traslada hacia los mercados para su '
                           'intercambio.',
                           'La {distribución} reparte la riqueza generada '
                           'entre los factores productivos: el trabajador '
                           'recibe {salario}, el empresario ganancias, el '
                           'Estado impuestos.',
                           'El {consumo} es la utilización del producto '
                           'social para satisfacer las necesidades mediante '
                           'el uso de bienes y servicios.',
                           'La {inversión} es la utilización del ahorro para '
                           'financiar un nuevo proceso productivo mediante '
                           'bienes de {capital}.']},
                {'titulo': '4.3 LOS SECTORES PRODUCTIVOS',
                 'items': ['El sector {primario} o agropecuario obtiene el '
                           'producto directamente de los recursos naturales, '
                           'sin transformación industrial.',
                           'El sector primario incluye la agricultura, '
                           'ganadería, silvicultura, caza y pesca, pero {no} '
                           'incluye la minería.',
                           'El sector {secundario} o industrial comprende la '
                           'extracción y transformación industrial de '
                           'materias primas.',
                           'El sector secundario se divide en el subsector '
                           '{extractivo} (minero y petrolífero) y el de '
                           '{transformación}.',
                           'El sector {terciario} o de servicios incluye el '
                           'comercio, la banca, el transporte y las '
                           'comunicaciones.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El proceso económico se define como el conjunto '
                           'de actividades para obtener recursos que '
                           'satisfagan {Las necesidades humanas}.',
                           'El número de fases del proceso económico es '
                           '{Cinco}.',
                           'La fase del proceso económico orientada a '
                           'generar bienes y servicios es {La producción}.',
                           'En la fase de producción aparece el llamado '
                           '{Valor agregado}.',
                           'La fase donde la producción se traslada hacia '
                           'los mercados para su intercambio es {La '
                           'circulación}.',
                           'La fase que reparte la riqueza entre los '
                           'factores productivos es {La distribución}.',
                           'En la fase de distribución, el trabajador '
                           'percibe sus ingresos vía {Salario}.',
                           'En la fase de distribución, el Estado obtiene '
                           'ingresos mediante {Impuestos}.',
                           'La fase de utilización del producto para '
                           'satisfacer necesidades personales es {El '
                           'consumo}.',
                           'La fase que utiliza el ahorro para financiar un '
                           'nuevo proceso productivo es {La inversión}.',
                           'La inversión se realiza mediante la adquisición '
                           'de bienes de {Capital}.',
                           'El sector que obtiene el producto directamente '
                           'de los recursos naturales es el sector '
                           '{Primario}.',
                           'El sector primario incluye la agricultura, '
                           'ganadería, silvicultura, caza y {La pesca}.',
                           'La minería y la extracción de petróleo se '
                           'consideran parte del sector {Industrial o '
                           'secundario}.',
                           'El sector secundario comprende la extracción y '
                           'transformación industrial de {Materias primas}.',
                           'El sector secundario se divide en el subsector '
                           'extractivo y el subsector de {Transformación}.',
                           'El sector que incluye el comercio, la banca y el '
                           'transporte es el sector {Terciario o de '
                           'servicios}.',
                           'El modelo de comercio directo entre empresa y '
                           'consumidor, favorecido por internet, se conoce '
                           'como {B2C}.',
                           'El proceso económico es descrito en el texto '
                           'como un proceso {Continuo e interrelacionado}.',
                           'Bajo el capitalismo, según el texto, entre '
                           'producción y consumo puede surgir {Una '
                           'contradicción cuando el consumo se retrasa de la '
                           'producción}.']},
                {'titulo': '4.4 LA PRODUCCIÓN Y LOS FACTORES PRODUCTIVOS',
                 'items': ['La {producción} es la primera fase del proceso '
                           'económico, donde se combinan racionalmente los '
                           'factores para transformar recursos en bienes.',
                           'El {proceso productivo} son las etapas donde las '
                           'materias primas se transforman agregando valor, '
                           'mediante {trabajo} y capital.',
                           'Los {factores productivos básicos o clásicos} '
                           'son naturaleza, trabajo, capital y empresa.',
                           'Los {factores productivos modernos} incluyen al '
                           'Estado como regulador y estabilizador.']},
                {'titulo': '4.5 RETRIBUCIÓN DE LOS FACTORES PRODUCTIVOS',
                 'items': ['El factor {naturaleza} recibe como retribución '
                           'la {renta}.',
                           'El factor {trabajo} recibe como retribución el '
                           '{salario}.',
                           'El factor {capital} recibe como retribución el '
                           '{interés}.',
                           'El factor {empresa} recibe como retribución la '
                           '{ganancia} o utilidad.',
                           'El factor {Estado} recibe como retribución los '
                           '{impuestos} o tributación.',
                           'La {empresa} es considerada el factor productivo '
                           '{organizador}, que reúne y combina a los demás '
                           'factores.']},
                {'titulo': '4.6 LA FUNCIÓN DE PRODUCCIÓN',
                 'items': ['La {función de producción} es una relación '
                           'técnica que expresa los máximos niveles de '
                           'producción según la combinación de factores.',
                           'En la función de producción, tanto el producto '
                           'como los factores se miden en unidades '
                           '{físicas}, no monetarias.',
                           'Los factores productivos {fijos} no se pueden '
                           'modificar en el corto plazo, como fábricas y '
                           'maquinaria.',
                           'Los factores productivos {variables} sí se '
                           'pueden modificar en el corto plazo, como '
                           'materias primas e insumos.']},
                {'titulo': '4.7 PRODUCTIVIDAD',
                 'items': ['La {productividad} mide cuántos bienes y '
                           'servicios se producen por cada factor utilizado '
                           'en un periodo.',
                           'El objetivo de la productividad es medir la '
                           '{eficiencia} de producción por cada factor o '
                           'recurso.',
                           'A menor cantidad de recursos necesarios para '
                           'producir lo mismo, {mayor} es la productividad.',
                           'La {productividad media} se obtiene dividiendo '
                           'la producción total entre el total de unidades '
                           'del factor utilizado.']},
                {'titulo': '4.8 COMPETITIVIDAD',
                 'items': ['La {competitividad} es la capacidad de una '
                           'empresa de desarrollar y mantener {ventajas '
                           'comparativas}.',
                           'Una {ventaja comparativa} es un recurso o '
                           'atributo que posee una empresa y del que carecen '
                           'sus {competidores}.',
                           'Según {Michael Porter}, la ventaja competitiva '
                           'se relaciona con el valor que una empresa crea '
                           'para sus {compradores}.',
                           'La competitividad {interna} busca la mayor '
                           'eficiencia posible de los recursos propios de la '
                           'organización.',
                           'La competitividad {externa} busca ventajas '
                           'competitivas en el contexto del {mercado}, '
                           'evaluando factores como la innovación.']}],
  'cuadros': [{'titulo': '4.3 LOS TRES SECTORES PRODUCTIVOS',
               'encabezados': ['Sector', 'Actividad principal'],
               'filas': [['{Primario}', 'Agricultura, ganadería y {pesca}'],
                         ['{Secundario}', 'Industria y {transformación}'],
                         ['{Terciario}', 'Comercio y {servicios}']]}],
  'preguntas': [{'pregunta': 'El proceso económico se define como el '
                             'conjunto de actividades para obtener recursos '
                             'que satisfagan:',
                 'alternativas': ['Solo deseos superfluos',
                                  'Las necesidades humanas',
                                  'Solo la riqueza estatal',
                                  'Solo la producción industrial',
                                  'El comercio exterior únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'El número de fases del proceso económico es:',
                 'alternativas': ['Tres', 'Cinco', 'Siete', 'Dos', 'Diez'],
                 'correcta': 'B'},
                {'pregunta': 'La fase del proceso económico orientada a '
                             'generar bienes y servicios es:',
                 'alternativas': ['La distribución',
                                  'La producción',
                                  'El consumo',
                                  'La circulación',
                                  'La inversión'],
                 'correcta': 'B'},
                {'pregunta': 'En la fase de producción aparece el llamado:',
                 'alternativas': ['Salario mínimo',
                                  'Valor agregado',
                                  'Producto bruto',
                                  'Interés bancario',
                                  'Tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'La fase donde la producción se traslada hacia '
                             'los mercados para su intercambio es:',
                 'alternativas': ['La producción',
                                  'La circulación',
                                  'La distribución',
                                  'El consumo',
                                  'La inversión'],
                 'correcta': 'B'},
                {'pregunta': 'La fase que reparte la riqueza entre los '
                             'factores productivos es:',
                 'alternativas': ['La producción',
                                  'La distribución',
                                  'La circulación',
                                  'El consumo',
                                  'La inversión'],
                 'correcta': 'B'},
                {'pregunta': 'En la fase de distribución, el trabajador '
                             'percibe sus ingresos vía:',
                 'alternativas': ['Impuestos',
                                  'Salario',
                                  'Dividendos exclusivos',
                                  'Subsidios',
                                  'Herencia'],
                 'correcta': 'B'},
                {'pregunta': 'En la fase de distribución, el Estado obtiene '
                             'ingresos mediante:',
                 'alternativas': ['Salarios',
                                  'Impuestos',
                                  'Ganancias empresariales',
                                  'Ahorro privado',
                                  'Inversión extranjera'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de utilización del producto para '
                             'satisfacer necesidades personales es:',
                 'alternativas': ['La producción',
                                  'El consumo',
                                  'La circulación',
                                  'La distribución',
                                  'La inversión'],
                 'correcta': 'B'},
                {'pregunta': 'La fase que utiliza el ahorro para financiar '
                             'un nuevo proceso productivo es:',
                 'alternativas': ['El consumo',
                                  'La inversión',
                                  'La distribución',
                                  'La circulación',
                                  'La producción'],
                 'correcta': 'B'},
                {'pregunta': 'La inversión se realiza mediante la '
                             'adquisición de bienes de:',
                 'alternativas': ['Consumo final',
                                  'Capital',
                                  'Uso personal',
                                  'Lujo exclusivo',
                                  'Intercambio directo'],
                 'correcta': 'B'},
                {'pregunta': 'El sector que obtiene el producto directamente '
                             'de los recursos naturales es el sector:',
                 'alternativas': ['Secundario',
                                  'Primario',
                                  'Terciario',
                                  'Financiero',
                                  'Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'El sector primario incluye la agricultura, '
                             'ganadería, silvicultura, caza y:',
                 'alternativas': ['La minería',
                                  'La pesca',
                                  'La industria textil',
                                  'La banca',
                                  'El comercio'],
                 'correcta': 'B'},
                {'pregunta': 'La minería y la extracción de petróleo se '
                             'consideran parte del sector:',
                 'alternativas': ['Primario',
                                  'Industrial o secundario',
                                  'Terciario',
                                  'Financiero',
                                  'Agropecuario'],
                 'correcta': 'B'},
                {'pregunta': 'El sector secundario comprende la extracción y '
                             'transformación industrial de:',
                 'alternativas': ['Servicios financieros',
                                  'Materias primas',
                                  'Información digital',
                                  'Capital humano',
                                  'Bienes intangibles'],
                 'correcta': 'B'},
                {'pregunta': 'El sector secundario se divide en el subsector '
                             'extractivo y el subsector de:',
                 'alternativas': ['Comercio',
                                  'Transformación',
                                  'Servicios',
                                  'Distribución final',
                                  'Consumo'],
                 'correcta': 'B'},
                {'pregunta': 'El sector que incluye el comercio, la banca y '
                             'el transporte es el sector:',
                 'alternativas': ['Primario',
                                  'Secundario',
                                  'Terciario o de servicios',
                                  'Agropecuario',
                                  'Industrial'],
                 'correcta': 'C'},
                {'pregunta': 'El modelo de comercio directo entre empresa y '
                             'consumidor, favorecido por internet, se conoce '
                             'como:',
                 'alternativas': ['B2B', 'B2C', 'C2C', 'G2G', 'P2P'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso económico es descrito en el texto '
                             'como un proceso:',
                 'alternativas': ['Aislado y discontinuo',
                                  'Continuo e interrelacionado',
                                  'Sin relación entre sus fases',
                                  'Exclusivamente teórico',
                                  'Estático'],
                 'correcta': 'B'},
                {'pregunta': 'Bajo el capitalismo, según el texto, entre '
                             'producción y consumo puede surgir:',
                 'alternativas': ['Una armonía perfecta',
                                  'Una contradicción cuando el consumo se '
                                  'retrasa de la producción',
                                  'Un equilibrio automático total',
                                  'La eliminación de la escasez',
                                  'Un crecimiento sin límites'],
                 'correcta': 'B'},
                {'pregunta': 'La producción se define como la primera fase '
                             'del proceso económico donde se combinan:',
                 'alternativas': ['Solo el capital',
                                  'Racionalmente los factores de producción',
                                  'Solo el trabajo',
                                  'Solo la naturaleza',
                                  'Solo el Estado'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores productivos básicos o clásicos '
                             'son naturaleza, trabajo, capital y:',
                 'alternativas': ['Estado',
                                  'Empresa',
                                  'Dinero',
                                  'Tecnología',
                                  'Comercio'],
                 'correcta': 'B'},
                {'pregunta': 'El factor productivo naturaleza recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'La renta',
                                  'El interés',
                                  'La ganancia',
                                  'El impuesto'],
                 'correcta': 'B'},
                {'pregunta': 'El factor productivo trabajo recibe como '
                             'retribución:',
                 'alternativas': ['La renta',
                                  'El salario',
                                  'El interés',
                                  'La ganancia',
                                  'El impuesto'],
                 'correcta': 'B'},
                {'pregunta': 'El factor productivo capital recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'El interés',
                                  'La renta',
                                  'El impuesto',
                                  'La tarifa'],
                 'correcta': 'B'},
                {'pregunta': 'El factor productivo empresa recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'La ganancia o utilidad',
                                  'La renta',
                                  'El interés',
                                  'El impuesto'],
                 'correcta': 'B'},
                {'pregunta': 'El factor productivo Estado recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'Los impuestos o tributación',
                                  'La renta',
                                  'El interés',
                                  'La ganancia'],
                 'correcta': 'B'},
                {'pregunta': 'La empresa es considerada el factor '
                             'productivo:',
                 'alternativas': ['Pasivo',
                                  'Organizador',
                                  'Regulador exclusivo',
                                  'Estabilizador exclusivo',
                                  'Originario'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, como factor productivo moderno, '
                             'cumple un papel:',
                 'alternativas': ['Pasivo',
                                  'Regulador y estabilizador',
                                  'Solo consultivo',
                                  'Nulo en la economía',
                                  'Solo simbólico'],
                 'correcta': 'B'},
                {'pregunta': 'La función de producción expresa los máximos '
                             'niveles de producción según la combinación de:',
                 'alternativas': ['Solo el capital',
                                  'Los factores productivos',
                                  'Solo el trabajo',
                                  'Solo la naturaleza',
                                  'Solo la tecnología'],
                 'correcta': 'B'},
                {'pregunta': 'En la función de producción, el producto y los '
                             'factores se miden en unidades:',
                 'alternativas': ['Monetarias',
                                  'Físicas',
                                  'Porcentuales',
                                  'Relativas exclusivamente',
                                  'Subjetivas'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores productivos que no se pueden '
                             'modificar en el corto plazo, como fábricas, se '
                             'llaman factores:',
                 'alternativas': ['Variables',
                                  'Fijos',
                                  'Externos',
                                  'Modernos exclusivos',
                                  'Clásicos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores productivos que sí se pueden '
                             'modificar en el corto plazo, como insumos, se '
                             'llaman factores:',
                 'alternativas': ['Fijos',
                                  'Variables',
                                  'Externos exclusivos',
                                  'Básicos exclusivos',
                                  'Modernos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'La productividad mide cuántos bienes y '
                             'servicios se producen por cada:',
                 'alternativas': ['Unidad monetaria exclusiva',
                                  'Factor utilizado',
                                  'Cliente atendido',
                                  'Impuesto pagado',
                                  'Trabajador despedido'],
                 'correcta': 'B'},
                {'pregunta': 'A menor cantidad de recursos necesarios para '
                             'producir la misma cantidad, la productividad:',
                 'alternativas': ['Disminuye',
                                  'Aumenta',
                                  'Se mantiene igual siempre',
                                  'Desaparece',
                                  'Se vuelve negativa'],
                 'correcta': 'B'},
                {'pregunta': 'La productividad media se obtiene dividiendo '
                             'la producción total entre:',
                 'alternativas': ['El precio de mercado',
                                  'El total de unidades del factor utilizado',
                                  'Los ingresos totales',
                                  'El número de empresas',
                                  'La inflación acumulada'],
                 'correcta': 'B'},
                {'pregunta': 'La competitividad es la capacidad de una '
                             'empresa de desarrollar y mantener:',
                 'alternativas': ['Deudas',
                                  'Ventajas comparativas',
                                  'Pérdidas constantes',
                                  'Menor producción',
                                  'Menor calidad'],
                 'correcta': 'B'},
                {'pregunta': 'Una ventaja comparativa es un recurso o '
                             'atributo del que carecen:',
                 'alternativas': ['Los clientes',
                                  'Los competidores',
                                  'Los proveedores',
                                  'El Estado',
                                  'Los trabajadores'],
                 'correcta': 'B'},
                {'pregunta': 'Según Michael Porter, la ventaja competitiva '
                             'se relaciona con el valor creado para:',
                 'alternativas': ['El Estado',
                                  'Los compradores',
                                  'Los competidores',
                                  'Los proveedores exclusivos',
                                  'El gobierno'],
                 'correcta': 'B'},
                {'pregunta': 'La competitividad interna busca la mayor '
                             'eficiencia posible de los recursos:',
                 'alternativas': ['Externos exclusivamente',
                                  'Propios de la organización',
                                  'Del gobierno',
                                  'De la competencia',
                                  'Del mercado internacional'],
                 'correcta': 'B'},
                {'pregunta': 'La competitividad externa evalúa factores como '
                             'la innovación y:',
                 'alternativas': ['Solo los precios internos',
                                  'La estabilidad económica',
                                  'Solo el clima laboral',
                                  'Solo los salarios internos',
                                  'Solo la ubicación geográfica'],
                 'correcta': 'B'}]},
 {'num': 5,
  'titulo': 'Trabajo',
  'secciones': [{'titulo': '5.1 CONCEPTO',
                 'items': ['El trabajo es el conjunto de aptitudes físicas y '
                           'mentales, propias solamente del {hombre}, para '
                           'intervenir en la actividad económica.',
                           'El trabajo permite generar un {nuevo valor}, '
                           'expresado en bienes y servicios.']},
                {'titulo': '5.2 EL CICLO PHVA O CÍRCULO DE DEMING',
                 'items': ['El ciclo PDCA, en español PHVA, corresponde a '
                           'las etapas de Planificar, {Hacer}, Verificar y '
                           '{Actuar}.',
                           'El ciclo PHVA también se conoce como el círculo '
                           'de {Deming}, en honor a su autor {Edwards '
                           'Deming}.',
                           'En la etapa de {Planificar}, se identifican las '
                           'actividades susceptibles de mejora y se fijan '
                           'los objetivos.',
                           'En la etapa de {Hacer}, se ejecutan los cambios '
                           'necesarios, aplicando de preferencia una prueba '
                           '{piloto}.',
                           'En la etapa de {Verificar}, se comprueba el buen '
                           'funcionamiento de la mejora implementada.',
                           'En la etapa de {Actuar}, se estudian los '
                           'resultados y se decide implantar la mejora en '
                           'forma {definitiva} o descartarla.']},
                {'titulo': '5.3 DIVISIÓN DEL TRABAJO',
                 'items': ['La división del trabajo es la {especialización} '
                           'del trabajo cooperativo en tareas específicas y '
                           'regladas.',
                           'El objetivo de la división del trabajo es la '
                           'especialización para aumentar la '
                           '{productividad}.',
                           'La división {social} del trabajo ocurre cuando '
                           'los seres humanos se dedican a actividades '
                           'especializadas diversas.',
                           'La división {interna} del trabajo ocurre cuando '
                           'cada trabajador se dedica a una parte de un '
                           'trabajo complejo, propio de la gran {industria}.',
                           'La división {internacional} del trabajo es la '
                           'especialización de los países según su '
                           'eficiencia productiva.']},
                {'titulo': '5.4 CARACTERÍSTICAS DEL TRABAJO',
                 'items': ['El trabajo requiere {liderazgo}, la figura de '
                           'quien dirige a los trabajadores hacia los '
                           'objetivos.',
                           'El trabajo requiere {motivación}, el compromiso '
                           'que estimula el cumplimiento de las '
                           'obligaciones.',
                           'El trabajo implica un {esfuerzo} del organismo, '
                           'sea físico o intelectual.',
                           'El trabajo tiene un fin {económico}, orientado a '
                           'la producción de bienes y servicios; en esto se '
                           'diferencia del {deporte}.',
                           'El trabajo {dignifica} al hombre, otorgándole la '
                           'estimación y el respeto de sus semejantes.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El trabajo se define como el conjunto de '
                           'aptitudes físicas y mentales propias de '
                           '{Solamente el hombre}.',
                           'El trabajo permite generar un nuevo valor '
                           'expresado en {Bienes y servicios}.',
                           'El ciclo PHVA también se conoce como el círculo '
                           'de {Deming}.',
                           'Las siglas PHVA corresponden a Planificar, '
                           'Hacer, Verificar y {Actuar}.',
                           'En la etapa de Planificar del ciclo PHVA se '
                           'identifican actividades susceptibles de '
                           '{Mejora}.',
                           'En la etapa de Hacer se recomienda aplicar antes '
                           'de un cambio a gran escala una {Prueba piloto a '
                           'pequeña escala}.',
                           'En la etapa de Verificar se comprueba {El buen '
                           'funcionamiento de la mejora implementada}.',
                           'En la etapa de Actuar, si los resultados son '
                           'satisfactorios, se procede a {Implantar la '
                           'mejora en forma definitiva y a gran escala}.',
                           'La división del trabajo se define como la '
                           'especialización del trabajo cooperativo en '
                           '{Tareas específicas y regladas}.',
                           'El objetivo de la división del trabajo es la '
                           'especialización para aumentar {La '
                           'productividad}.',
                           'La división del trabajo en la que los seres '
                           'humanos se dedican a actividades especializadas '
                           'diversas desde la antigüedad es la división '
                           '{Social}.',
                           'La división del trabajo propia de la gran '
                           'industria moderna, donde cada obrero hace una '
                           'parte de un proceso complejo, es la división '
                           '{Interna}.',
                           'La especialización de los países según su '
                           'eficiencia productiva se llama división '
                           '{Internacional del trabajo}.',
                           'Entre las características del trabajo figura la '
                           'necesidad de una figura que dirija al equipo, '
                           'llamada {Liderazgo}.',
                           'El compromiso que estimula el cumplimiento de '
                           'las obligaciones laborales se llama '
                           '{Motivación}.',
                           'El trabajo se diferencia del deporte '
                           'principalmente porque el trabajo tiene un fin '
                           '{Económico}.',
                           'El trabajo es descrito como una actividad '
                           'consciente porque el individuo {Sabe lo que hace '
                           'y conoce el fin que persigue}.',
                           'Según el texto, el trabajo dignifica al hombre '
                           'porque le otorga {La estimación y el respeto de '
                           'sus semejantes}.',
                           'Un sistema de trabajo comprende, entre otros '
                           'aspectos, la estructura de tareas y su '
                           '{Sincronización}.',
                           'La mejora continua busca optimizar la calidad de '
                           'un producto, proceso o {Servicio}.']},
                {'titulo': '5.5 MODALIDADES DE LA DIVISIÓN DEL TRABAJO',
                 'items': ['La división {social} del trabajo surge cuando '
                           'los seres humanos se dedican a actividades '
                           'especializadas diversas.',
                           'La división {interna} del trabajo es propia de '
                           'la industria moderna, cuando cada obrero realiza '
                           'una parte de un trabajo complejo.',
                           'La división {internacional} del trabajo es la '
                           'especialización de los países, produciendo lo '
                           'que son más {eficientes}.']},
                {'titulo': '5.6 EL SALARIO: CONCEPTO Y ORIGEN',
                 'items': ['El {salario}, o remuneración, es la suma de '
                           'dinero que recibe un trabajador de su empleador '
                           'por su trabajo.',
                           'El pago diario del salario recibe el nombre de '
                           '{jornal}, del término jornada.',
                           'El término «salario» proviene del vocablo latino '
                           '«{salarium}», que significa «pago de {sal}».',
                           'En la antigua Roma, la sal era un bien escaso '
                           'usado como antiséptico, y se pagaba a los '
                           'legionarios que custodiaban la «Vía '
                           '{Salaria}».']},
                {'titulo': '5.7 FORMAS DE REMUNERACIÓN',
                 'items': ['El {jornal} es la retribución que recibe el '
                           'obrero por cada jornada laboral, pagada por lo '
                           'general semanalmente.',
                           'El {sueldo}, o haber, es el pago que perciben '
                           'los empleados del sector público o {privado}.']}],
  'cuadros': [{'titulo': '5.2 LAS CUATRO ETAPAS DEL CICLO PHVA',
               'encabezados': ['Etapa', 'Acción'],
               'filas': [['{Planificar}',
                          'Identificar mejoras y fijar {objetivos}'],
                         ['{Hacer}',
                          'Ejecutar los cambios, con prueba {piloto}'],
                         ['{Verificar}',
                          'Comprobar el buen {funcionamiento}'],
                         ['{Actuar}',
                          'Implantar la mejora o {descartarla}']]}],
  'preguntas': [{'pregunta': 'El trabajo se define como el conjunto de '
                             'aptitudes físicas y mentales propias de:',
                 'alternativas': ['Cualquier ser vivo',
                                  'Solamente el hombre',
                                  'Solo las máquinas',
                                  'Solo los animales',
                                  'La naturaleza en general'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo permite generar un nuevo valor '
                             'expresado en:',
                 'alternativas': ['Solo dinero',
                                  'Bienes y servicios',
                                  'Solo tiempo libre',
                                  'Solo información',
                                  'Solo tecnología'],
                 'correcta': 'B'},
                {'pregunta': 'El ciclo PHVA también se conoce como el '
                             'círculo de:',
                 'alternativas': ['Smith',
                                  'Deming',
                                  'Keynes',
                                  'Marx',
                                  'Wieser'],
                 'correcta': 'B'},
                {'pregunta': 'Las siglas PHVA corresponden a Planificar, '
                             'Hacer, Verificar y:',
                 'alternativas': ['Analizar',
                                  'Actuar',
                                  'Aplicar',
                                  'Ajustar',
                                  'Aprobar'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de Planificar del ciclo PHVA se '
                             'identifican actividades susceptibles de:',
                 'alternativas': ['Eliminación total',
                                  'Mejora',
                                  'Privatización',
                                  'Reducción de personal',
                                  'Externalización'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de Hacer se recomienda aplicar '
                             'antes de un cambio a gran escala una:',
                 'alternativas': ['Auditoría externa',
                                  'Prueba piloto a pequeña escala',
                                  'Reducción de costos',
                                  'Fusión empresarial',
                                  'Campaña publicitaria'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de Verificar se comprueba:',
                 'alternativas': ['El presupuesto anual',
                                  'El buen funcionamiento de la mejora '
                                  'implementada',
                                  'La rentabilidad accionaria',
                                  'El tipo de cambio',
                                  'La inflación mensual'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de Actuar, si los resultados son '
                             'satisfactorios, se procede a:',
                 'alternativas': ['Descartar la mejora',
                                  'Implantar la mejora en forma definitiva y '
                                  'a gran escala',
                                  'Repetir solo la primera etapa',
                                  'Suspender el proyecto',
                                  'Reducir el personal'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo se define como la '
                             'especialización del trabajo cooperativo en:',
                 'alternativas': ['Tareas generales sin orden',
                                  'Tareas específicas y regladas',
                                  'Actividades improvisadas',
                                  'Un solo puesto fijo',
                                  'Ninguna tarea concreta'],
                 'correcta': 'B'},
                {'pregunta': 'El objetivo de la división del trabajo es la '
                             'especialización para aumentar:',
                 'alternativas': ['El desempleo',
                                  'La productividad',
                                  'La informalidad',
                                  'El ocio',
                                  'La inflación'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo en la que los seres '
                             'humanos se dedican a actividades '
                             'especializadas diversas desde la antigüedad es '
                             'la división:',
                 'alternativas': ['Interna',
                                  'Social',
                                  'Internacional',
                                  'Técnica exclusiva',
                                  'Empresarial'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo propia de la gran '
                             'industria moderna, donde cada obrero hace una '
                             'parte de un proceso complejo, es la división:',
                 'alternativas': ['Social',
                                  'Interna',
                                  'Internacional',
                                  'Artesanal',
                                  'Rural'],
                 'correcta': 'B'},
                {'pregunta': 'La especialización de los países según su '
                             'eficiencia productiva se llama división:',
                 'alternativas': ['Social del trabajo',
                                  'Internacional del trabajo',
                                  'Interna del trabajo',
                                  'Rural del trabajo',
                                  'Artesanal del trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las características del trabajo figura '
                             'la necesidad de una figura que dirija al '
                             'equipo, llamada:',
                 'alternativas': ['Motivación',
                                  'Liderazgo',
                                  'Interdependencia',
                                  'Esfuerzo',
                                  'Dignidad'],
                 'correcta': 'B'},
                {'pregunta': 'El compromiso que estimula el cumplimiento de '
                             'las obligaciones laborales se llama:',
                 'alternativas': ['Liderazgo',
                                  'Motivación',
                                  'Interdependencia',
                                  'Fin económico',
                                  'Actividad consciente'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo se diferencia del deporte '
                             'principalmente porque el trabajo tiene un fin:',
                 'alternativas': ['Recreativo',
                                  'Económico',
                                  'Artístico exclusivo',
                                  'Espiritual',
                                  'Sin propósito definido'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo es descrito como una actividad '
                             'consciente porque el individuo:',
                 'alternativas': ['Actúa como un autómata',
                                  'Sabe lo que hace y conoce el fin que '
                                  'persigue',
                                  'No tiene ningún objetivo',
                                  'Actúa por instinto puro',
                                  'Repite acciones sin sentido'],
                 'correcta': 'B'},
                {'pregunta': 'Según el texto, el trabajo dignifica al hombre '
                             'porque le otorga:',
                 'alternativas': ['Solo dinero',
                                  'La estimación y el respeto de sus '
                                  'semejantes',
                                  'Menos responsabilidades',
                                  'Más tiempo libre exclusivamente',
                                  'Ninguna consecuencia social'],
                 'correcta': 'B'},
                {'pregunta': 'Un sistema de trabajo comprende, entre otros '
                             'aspectos, la estructura de tareas y su:',
                 'alternativas': ['Eliminación total',
                                  'Sincronización',
                                  'Privatización',
                                  'Anulación',
                                  'Improvisación'],
                 'correcta': 'B'},
                {'pregunta': 'La mejora continua busca optimizar la calidad '
                             'de un producto, proceso o:',
                 'alternativas': ['Solo el precio',
                                  'Servicio',
                                  'Solo el empaque',
                                  'Solo la publicidad',
                                  'Solo el transporte'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo en la que los seres '
                             'humanos se dedican a actividades diversas '
                             'desde la antigüedad se llama división:',
                 'alternativas': ['Interna',
                                  'Social',
                                  'Internacional',
                                  'Técnica exclusiva',
                                  'Empresarial'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo propia de la industria '
                             'moderna, donde cada obrero realiza una parte '
                             'de un proceso, se llama división:',
                 'alternativas': ['Social',
                                  'Interna',
                                  'Internacional',
                                  'Rural',
                                  'Artesanal'],
                 'correcta': 'B'},
                {'pregunta': 'La especialización de los países en producir '
                             'lo que son más eficientes se llama división:',
                 'alternativas': ['Social del trabajo',
                                  'Internacional del trabajo',
                                  'Interna del trabajo',
                                  'Rural del trabajo',
                                  'Artesanal del trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'El salario se define como la suma de dinero '
                             'que recibe periódicamente un trabajador de su:',
                 'alternativas': ['Familia',
                                  'Empleador',
                                  'Sindicato',
                                  'Gobierno exclusivamente',
                                  'Banco'],
                 'correcta': 'B'},
                {'pregunta': 'El pago diario del salario recibe el nombre '
                             'de:',
                 'alternativas': ['Sueldo',
                                  'Jornal',
                                  'Haber',
                                  'Estipendio exclusivo',
                                  'Honorario'],
                 'correcta': 'B'},
                {'pregunta': 'El término «salario» proviene del vocablo '
                             'latino «salarium», que significa:',
                 'alternativas': ['Pago de oro',
                                  'Pago de sal',
                                  'Pago de trigo',
                                  'Pago de agua',
                                  'Pago de vino'],
                 'correcta': 'B'},
                {'pregunta': 'En la antigua Roma, la sal era un bien escaso '
                             'usado como:',
                 'alternativas': ['Moneda exclusiva',
                                  'Antiséptico y preservante de alimentos',
                                  'Combustible',
                                  'Material de construcción',
                                  'Colorante'],
                 'correcta': 'B'},
                {'pregunta': 'La ruta romana por la cual ingresaba la sal a '
                             'Roma se llamaba:',
                 'alternativas': ['Vía Apia',
                                  'Vía Salaria',
                                  'Vía Flaminia',
                                  'Vía Aurelia',
                                  'Vía Domicia'],
                 'correcta': 'B'},
                {'pregunta': 'El jornal es la retribución que recibe el '
                             'obrero por cada:',
                 'alternativas': ['Mes trabajado',
                                  'Jornada laboral',
                                  'Año de servicio',
                                  'Proyecto terminado',
                                  'Cliente atendido'],
                 'correcta': 'B'},
                {'pregunta': 'El jornal se paga, por lo general, de forma:',
                 'alternativas': ['Mensual',
                                  'Semanal',
                                  'Anual',
                                  'Trimestral',
                                  'Solo al final del contrato'],
                 'correcta': 'B'},
                {'pregunta': 'El sueldo, también llamado haber, es el pago '
                             'que perciben:',
                 'alternativas': ['Solo los obreros',
                                  'Los empleados del sector público o '
                                  'privado',
                                  'Solo los desempleados',
                                  'Solo los jubilados',
                                  'Solo los estudiantes'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo es considerado en la actualidad un '
                             'derecho:',
                 'alternativas': ['Exclusivo de adultos mayores',
                                  'Humano social',
                                  'Solo comercial',
                                  'Solo privado',
                                  'Opcional del Estado'],
                 'correcta': 'B'}]},
 {'num': 6,
  'titulo': 'Capital',
  'secciones': [{'titulo': '6.1 CONCEPTO',
                 'items': ['Para la ciencia económica, el capital es el '
                           'conjunto de objetos fabricados por el hombre '
                           'para ser usados en la producción de otros '
                           '{bienes}.',
                           'El capital comprende las maquinarias, equipos, '
                           'instalaciones y edificios, correspondiendo '
                           'contablemente al concepto de {activo fijo}.',
                           'Para la ciencia contable, el capital incluye '
                           'también el activo {circulante}, es decir el '
                           'capital financiero.',
                           'El {capital de trabajo} es la diferencia entre '
                           'el activo circulante y el pasivo a corto '
                           'plazo.']},
                {'titulo': '6.2 FORMAS DE OBTENCIÓN DEL CAPITAL (TEORÍA '
                           'NEOCLÁSICA)',
                 'items': ['El capital surge por la acción del {hombre} '
                           'sobre la naturaleza, combinando los factores '
                           'originarios de trabajo y {naturaleza}.',
                           'El capital también se forma por medio del '
                           '{excedente económico}, separando parte de lo '
                           'producido para un nuevo proceso productivo.',
                           'El capital se forma también por medio del '
                           '{ahorro}, propio de los modos de producción '
                           'capitalistas.',
                           'La teoría de la {abstinencia} sobre la formación '
                           'del capital fue desarrollada por {Nassau '
                           'Senior}.',
                           'Según la teoría de la abstinencia, no consumir '
                           'toda la riqueza permite liberar recursos para '
                           'producir bienes de {capital} mediante la '
                           'inversión.',
                           'Según Senior, la demanda del capital depende de '
                           'su nivel de {productividad}.']},
                {'titulo': '6.3 ROL DEL CAPITAL EN LA PRODUCCIÓN',
                 'items': ['El capital sirve para la creación de nuevas '
                           '{empresas}, la ampliación de las existentes y la '
                           'realización de grandes {obras}.',
                           'El capital {no interviene} directamente en la '
                           'satisfacción de necesidades humanas, solo en '
                           'forma {indirecta}.',
                           'El capital está sujeto a {desgaste} y deterioro '
                           'por su uso, lo que contablemente se denomina '
                           '{depreciación}.',
                           'En época de {crisis} económica aumenta la '
                           'demanda de capital por falta de capitales '
                           'disponibles.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Para la ciencia económica, el capital es el '
                           'conjunto de objetos fabricados por el hombre '
                           'para {Ser usados en la producción de otros '
                           'bienes}.',
                           'El capital, en su concepción económica, '
                           'corresponde contablemente al concepto de {Activo '
                           'fijo}.',
                           'Para la ciencia contable, el capital incluye '
                           'también el activo {Circulante}.',
                           'El capital de trabajo se define como la '
                           'diferencia entre el activo circulante y {El '
                           'pasivo a corto plazo}.',
                           'Según la teoría neoclásica, el capital surge de '
                           'la combinación de trabajo y {Naturaleza}.',
                           'Una forma de obtención del capital es mediante '
                           'el sobrante de la producción, llamado {Excedente '
                           'económico}.',
                           'La teoría de la abstinencia sobre la formación '
                           'del capital fue desarrollada por {Nassau '
                           'Senior}.',
                           'Según la teoría de la abstinencia, no consumir '
                           'toda la riqueza permite {Liberar recursos para '
                           'producir bienes de capital}.',
                           'Según Nassau Senior, la demanda del capital '
                           'depende de su nivel de {Productividad}.',
                           'La teoría de la abstinencia justifica el cobro '
                           'de intereses en base a virtudes como {La '
                           'previsión, sobriedad y frugalidad}.',
                           'El capital sirve, entre otras cosas, para la '
                           'creación de nuevas {Empresas}.',
                           'El capital condiciona, según el texto {Las '
                           'diversas formas de trabajo}.',
                           'El capital, según el texto, interviene en la '
                           'satisfacción de necesidades humanas de forma '
                           '{Indirecta, al incrementar la producción}.',
                           'El desgaste del capital por su uso se '
                           'contabiliza mediante la {Depreciación}.',
                           'En época de crisis económica, la demanda de '
                           'capital tiende a {Aumentar por falta de '
                           'capitales}.',
                           'En época de prosperidad, el valor del capital '
                           'tiende a {Estabilizarse o bajar}.',
                           'Un ejemplo de capital, según el texto, es la '
                           'cadena de montaje de una empresa como {Toyota}.',
                           'El capital, según la ciencia económica, se '
                           'diferencia de la inversión porque esta última '
                           'comprende {El activo fijo más el activo '
                           'circulante}.',
                           'Cuando el hombre mezcló agua con tierra para '
                           'construir adobes, se ejemplifica el origen del '
                           'capital por {La acción del hombre sobre la '
                           'naturaleza}.',
                           'El proceso de acumulación por excedente '
                           'económico se dio principalmente en modos de '
                           'producción {Precapitalistas y las primeras fases '
                           'del capitalismo}.']},
                {'titulo': '6.5 CLASES DE CAPITAL (TEORÍA CLÁSICA)',
                 'items': ['El {capital productivo} son bienes usados en la '
                           'producción de nuevos bienes, como maquinaria '
                           'industrial.',
                           'El {capital fijo} son bienes que sirven en '
                           'varios procesos productivos, trasladando su '
                           'valor por {partes}.',
                           'El {capital circulante} son bienes empleados en '
                           'un solo proceso productivo, como el trigo o el '
                           'algodón.',
                           'El {capital lucrativo} son bienes que sin '
                           'destinarse a la producción generan renta, como '
                           'una casa en {alquiler}.']},
                {'titulo': '6.6 OTROS TIPOS DE CAPITAL',
                 'items': ['El {capital comercial} se originó en la fase '
                           'mercantilista del capitalismo, con el excedente '
                           'del comercio {exterior}.',
                           'El {capital industrial} se originó en la etapa '
                           'industrial, para adquirir materias primas, mano '
                           'de obra y {maquinaria}.',
                           'El {capital bancario} surgió cuando la burguesía '
                           'industrial creó las primeras entidades '
                           '{financieras}.',
                           'Los bancos generan excedente porque cobran mayor '
                           'tasa de interés en {préstamos} que la que pagan '
                           'a los {ahorristas}.',
                           'El {capital financiero} corresponde a la etapa '
                           'monopólica del capitalismo, y surge de la fusión '
                           'del capital industrial y {bancario}.']}],
  'cuadros': [{'titulo': '6.2 FORMAS DE OBTENCIÓN DEL CAPITAL',
               'encabezados': ['Forma', 'Mecanismo'],
               'filas': [['Acción del {hombre}', 'Sobre la {naturaleza}'],
                         ['{Excedente} económico',
                          'Sobrante de la {producción}'],
                         ['{Ahorro}',
                          'Teoría de la {abstinencia} de Nassau Senior']]}],
  'preguntas': [{'pregunta': 'Para la ciencia económica, el capital es el '
                             'conjunto de objetos fabricados por el hombre '
                             'para:',
                 'alternativas': ['El consumo directo',
                                  'Ser usados en la producción de otros '
                                  'bienes',
                                  'La exportación exclusiva',
                                  'El ahorro personal',
                                  'El pago de impuestos'],
                 'correcta': 'B'},
                {'pregunta': 'El capital, en su concepción económica, '
                             'corresponde contablemente al concepto de:',
                 'alternativas': ['Activo circulante',
                                  'Activo fijo',
                                  'Pasivo a corto plazo',
                                  'Patrimonio neto',
                                  'Capital de trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'Para la ciencia contable, el capital incluye '
                             'también el activo:',
                 'alternativas': ['Fijo exclusivamente',
                                  'Circulante',
                                  'Ninguno adicional',
                                  'Solo inmuebles',
                                  'Solo maquinaria'],
                 'correcta': 'B'},
                {'pregunta': 'El capital de trabajo se define como la '
                             'diferencia entre el activo circulante y:',
                 'alternativas': ['El activo fijo',
                                  'El pasivo a corto plazo',
                                  'El patrimonio total',
                                  'Las utilidades anuales',
                                  'El capital social'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría neoclásica, el capital surge '
                             'de la combinación de trabajo y:',
                 'alternativas': ['Dinero',
                                  'Naturaleza',
                                  'Tecnología exclusiva',
                                  'Comercio',
                                  'Impuestos'],
                 'correcta': 'B'},
                {'pregunta': 'Una forma de obtención del capital es mediante '
                             'el sobrante de la producción, llamado:',
                 'alternativas': ['Ahorro',
                                  'Excedente económico',
                                  'Depreciación',
                                  'Inversión extranjera',
                                  'Capital de trabajo'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la abstinencia sobre la formación '
                             'del capital fue desarrollada por:',
                 'alternativas': ['Adam Smith',
                                  'Nassau Senior',
                                  'Karl Marx',
                                  'Friedrich von Wieser',
                                  'John Keynes'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría de la abstinencia, no consumir '
                             'toda la riqueza permite:',
                 'alternativas': ['Aumentar la inflación',
                                  'Liberar recursos para producir bienes de '
                                  'capital',
                                  'Reducir la producción total',
                                  'Eliminar el ahorro',
                                  'Incrementar el consumo inmediato'],
                 'correcta': 'B'},
                {'pregunta': 'Según Nassau Senior, la demanda del capital '
                             'depende de su nivel de:',
                 'alternativas': ['Escasez',
                                  'Productividad',
                                  'Antigüedad',
                                  'Ubicación geográfica',
                                  'Color'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la abstinencia justifica el cobro '
                             'de intereses en base a virtudes como:',
                 'alternativas': ['El derroche',
                                  'La previsión, sobriedad y frugalidad',
                                  'La generosidad excesiva',
                                  'El consumo inmediato',
                                  'La imprevisión'],
                 'correcta': 'B'},
                {'pregunta': 'El capital sirve, entre otras cosas, para la '
                             'creación de nuevas:',
                 'alternativas': ['Necesidades',
                                  'Empresas',
                                  'Crisis económicas',
                                  'Deudas públicas',
                                  'Inflaciones'],
                 'correcta': 'B'},
                {'pregunta': 'El capital condiciona, según el texto:',
                 'alternativas': ['Las diversas formas de trabajo',
                                  'Solo el clima',
                                  'Solo la política',
                                  'Solo la religión',
                                  'Solo el idioma'],
                 'correcta': 'A'},
                {'pregunta': 'El capital, según el texto, interviene en la '
                             'satisfacción de necesidades humanas de forma:',
                 'alternativas': ['Directa exclusivamente',
                                  'Indirecta, al incrementar la producción',
                                  'Nula',
                                  'Solo simbólica',
                                  'Aleatoria'],
                 'correcta': 'B'},
                {'pregunta': 'El desgaste del capital por su uso se '
                             'contabiliza mediante la:',
                 'alternativas': ['Inflación',
                                  'Depreciación',
                                  'Inversión',
                                  'Demanda',
                                  'Oferta'],
                 'correcta': 'B'},
                {'pregunta': 'En época de crisis económica, la demanda de '
                             'capital tiende a:',
                 'alternativas': ['Disminuir siempre',
                                  'Aumentar por falta de capitales',
                                  'Desaparecer',
                                  'Mantenerse igual siempre',
                                  'Volverse negativa'],
                 'correcta': 'B'},
                {'pregunta': 'En época de prosperidad, el valor del capital '
                             'tiende a:',
                 'alternativas': ['Aumentar siempre bruscamente',
                                  'Estabilizarse o bajar',
                                  'Desaparecer',
                                  'Volverse negativo',
                                  'Duplicarse automáticamente'],
                 'correcta': 'B'},
                {'pregunta': 'Un ejemplo de capital, según el texto, es la '
                             'cadena de montaje de una empresa como:',
                 'alternativas': ['Un supermercado',
                                  'Toyota',
                                  'Un banco',
                                  'Una universidad',
                                  'Un hospital'],
                 'correcta': 'B'},
                {'pregunta': 'El capital, según la ciencia económica, se '
                             'diferencia de la inversión porque esta última '
                             'comprende:',
                 'alternativas': ['Solo el activo fijo',
                                  'El activo fijo más el activo circulante',
                                  'Solo el ahorro',
                                  'Solo el consumo',
                                  'Ningún activo'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el hombre mezcló agua con tierra para '
                             'construir adobes, se ejemplifica el origen del '
                             'capital por:',
                 'alternativas': ['El ahorro',
                                  'La acción del hombre sobre la naturaleza',
                                  'El excedente económico exclusivo',
                                  'La teoría de la abstinencia',
                                  'La inversión extranjera'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso de acumulación por excedente '
                             'económico se dio principalmente en modos de '
                             'producción:',
                 'alternativas': ['Exclusivamente modernos',
                                  'Precapitalistas y las primeras fases del '
                                  'capitalismo',
                                  'Solo socialistas',
                                  'Solo feudales tardíos',
                                  'Solo poscapitalistas'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría clásica, los bienes usados en '
                             'la producción de nuevos bienes, como '
                             'maquinaria, forman el capital:',
                 'alternativas': ['Lucrativo',
                                  'Productivo',
                                  'Bancario',
                                  'Comercial',
                                  'Financiero'],
                 'correcta': 'B'},
                {'pregunta': 'El capital que sirve en varios procesos '
                             'productivos, trasladando su valor por partes, '
                             'es el capital:',
                 'alternativas': ['Circulante',
                                  'Fijo',
                                  'Lucrativo',
                                  'Comercial',
                                  'Bancario'],
                 'correcta': 'B'},
                {'pregunta': 'El capital empleado en un solo proceso '
                             'productivo, como el trigo o el algodón, es el '
                             'capital:',
                 'alternativas': ['Fijo',
                                  'Circulante',
                                  'Lucrativo',
                                  'Industrial',
                                  'Financiero'],
                 'correcta': 'B'},
                {'pregunta': 'El capital que genera renta sin destinarse '
                             'directamente a la producción, como una casa en '
                             'alquiler, es el capital:',
                 'alternativas': ['Fijo',
                                  'Lucrativo',
                                  'Circulante',
                                  'Productivo',
                                  'Bancario'],
                 'correcta': 'B'},
                {'pregunta': 'El capital comercial se originó en la fase '
                             'mercantilista del capitalismo, priorizando:',
                 'alternativas': ['La industria pesada',
                                  'El comercio exterior',
                                  'La banca',
                                  'La agricultura exclusiva',
                                  'La minería exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El capital industrial se originó en la etapa '
                             'industrial para adquirir, entre otros '
                             'recursos:',
                 'alternativas': ['Solo dinero',
                                  'Materias primas, mano de obra y '
                                  'maquinaria',
                                  'Solo tierras',
                                  'Solo patentes',
                                  'Solo software'],
                 'correcta': 'B'},
                {'pregunta': 'El capital bancario surgió cuando la burguesía '
                             'industrial creó las primeras:',
                 'alternativas': ['Fábricas',
                                  'Entidades financieras (bancos)',
                                  'Colonias',
                                  'Universidades',
                                  'Bolsas de valores exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Los bancos generan excedente porque la tasa de '
                             'interés que cobran en préstamos es:',
                 'alternativas': ['Igual a la que pagan a ahorristas',
                                  'Mayor a la que pagan a los ahorristas',
                                  'Menor a la que pagan a ahorristas',
                                  'Inexistente',
                                  'Regulada por otro banco'],
                 'correcta': 'B'},
                {'pregunta': 'El capital financiero corresponde a la etapa:',
                 'alternativas': ['Mercantilista',
                                  'Monopólica del capitalismo',
                                  'Feudal',
                                  'Precapitalista',
                                  'Socialista'],
                 'correcta': 'B'},
                {'pregunta': 'El capital financiero surge de la fusión del '
                             'capital industrial y el capital:',
                 'alternativas': ['Comercial',
                                  'Bancario',
                                  'Lucrativo',
                                  'Fijo',
                                  'Circulante'],
                 'correcta': 'B'}]},
 {'num': 7,
  'titulo': 'Naturaleza',
  'secciones': [{'titulo': '7.1 CONCEPTO Y CARACTERÍSTICAS',
                 'items': ['La naturaleza es el conjunto de elementos '
                           '{preexistentes} al hombre que componen la '
                           'realidad física.',
                           'La naturaleza se denomina también reservas '
                           'naturales o factor {tierra}.',
                           'La naturaleza es un factor productivo '
                           '{originario}, anterior a la producción, y no '
                           'resulta de ningún proceso productivo.',
                           'La naturaleza cumple un rol {pasivo} en la '
                           'producción, ya que es útil en cuanto es '
                           'conquistada por el hombre.',
                           'La naturaleza es un factor {condicionante} de la '
                           'actividad productiva, como la agricultura '
                           'condicionada por el clima.',
                           'Su dotación es {limitada}, es decir, escasa, por '
                           'lo que su explotación requiere racionamiento.',
                           'El propietario de la naturaleza como factor '
                           'productivo recibe una retribución llamada '
                           '{renta}.']},
                {'titulo': '7.2 ASPECTOS DE LA NATURALEZA',
                 'items': ['El {medio geográfico}, o medio ambiente, '
                           'comprende el territorio y el clima.',
                           'El {territorio} está constituido por el suelo, '
                           'subsuelo, relieve orográfico y situación '
                           'geográfica.',
                           'El {clima} es el conjunto de caracteres '
                           'atmosféricos que distinguen una región y '
                           'condicionan las actividades económicas.',
                           'El Perú cuenta con más de {80} microclimas, lo '
                           'que posibilita la producción agrícola fuera de '
                           'estación.',
                           'Las {materias brutas}, o riqueza potencial, son '
                           'elementos primarios sin extraer ni modificar por '
                           'el hombre.',
                           'Las {materias primas} son elementos que la '
                           'naturaleza ofrece y que sirven de base para '
                           'elaborar bienes, tras ser extraídos y '
                           'transformados.',
                           'Las materias primas provienen de tres fuentes: '
                           'de origen {animal}, de origen {vegetal} y de '
                           'origen mineral.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La naturaleza, como factor productivo, se define '
                           'como el conjunto de elementos {Preexistentes al '
                           'hombre}.',
                           'La naturaleza también se denomina reservas '
                           'naturales o factor {Tierra}.',
                           'La naturaleza es considerada un factor '
                           'productivo originario porque {Es anterior a la '
                           'producción}.',
                           'La naturaleza cumple en la producción un rol '
                           '{Pasivo}.',
                           'La naturaleza es un factor condicionante porque, '
                           'por ejemplo, la agricultura depende de {El suelo '
                           'y el clima}.',
                           'La dotación de recursos naturales es, en general '
                           '{Limitada o escasa}.',
                           'El propietario de un recurso natural recibe una '
                           'retribución llamada {Renta}.',
                           'El medio geográfico, o medio ambiente, comprende '
                           'principalmente {El territorio y el clima}.',
                           'El territorio está constituido por el suelo, '
                           'subsuelo, relieve orográfico y {La situación '
                           'geográfica}.',
                           'El clima condiciona directamente actividades '
                           'económicas como {La agricultura y la producción '
                           'textil}.',
                           'El Perú cuenta con un número de microclimas '
                           'superior a {80}.',
                           'Los elementos primarios sin extraer ni modificar '
                           'por el hombre se llaman {Materias brutas}.',
                           'Los elementos que la naturaleza ofrece y sirven '
                           'de base para elaborar bienes finales se llaman '
                           '{Materias primas}.',
                           'El algodón, fruto del trabajo agrícola, es un '
                           'ejemplo de {Materia prima}.',
                           'Las materias primas provienen de tres fuentes: '
                           'animal, vegetal y {Mineral}.',
                           'La lana, las carnes y el marfil son ejemplos de '
                           'materias primas de origen {Animal}.',
                           'Para aprovechar los recursos naturales, el ser '
                           'humano debe aplicar {Su fuerza de trabajo}.',
                           'La naturaleza se presenta como un depósito de '
                           'materias brutas y fuentes de {Energías}.',
                           'En la sierra sur del Perú, la producción de papa '
                           'se explica por la influencia de {El suelo y el '
                           'clima}.',
                           'El descanso de tierras y la rotación de cultivos '
                           'en la sierra ejemplifican {Una búsqueda de '
                           'armonía entre el hombre y la naturaleza}.']}],
  'cuadros': [{'titulo': '7.1 CARACTERÍSTICAS DE LA NATURALEZA COMO FACTOR '
                         'PRODUCTIVO',
               'encabezados': ['Característica', 'Significado'],
               'filas': [['{Originario}', 'Anterior a la {producción}'],
                         ['{Pasivo}', 'Útil al ser {conquistado}'],
                         ['{Condicionante}',
                          'Influye en la {actividad} productiva'],
                         ['{Limitado}',
                          'Escaso, requiere {racionamiento}']]}],
  'preguntas': [{'pregunta': 'La naturaleza, como factor productivo, se '
                             'define como el conjunto de elementos:',
                 'alternativas': ['Creados por el hombre',
                                  'Preexistentes al hombre',
                                  'Producidos industrialmente',
                                  'Exclusivamente urbanos',
                                  'Artificiales'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza también se denomina reservas '
                             'naturales o factor:',
                 'alternativas': ['Trabajo',
                                  'Tierra',
                                  'Capital',
                                  'Empresa',
                                  'Dinero'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza es considerada un factor '
                             'productivo originario porque:',
                 'alternativas': ['Resulta de un proceso productivo previo',
                                  'Es anterior a la producción',
                                  'Depende del capital',
                                  'Se crea con tecnología',
                                  'Requiere siempre inversión'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza cumple en la producción un rol:',
                 'alternativas': ['Activo y determinante',
                                  'Pasivo',
                                  'Exclusivamente financiero',
                                  'Secundario nulo',
                                  'Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza es un factor condicionante '
                             'porque, por ejemplo, la agricultura depende '
                             'de:',
                 'alternativas': ['Solo el capital disponible',
                                  'El suelo y el clima',
                                  'Solo la mano de obra',
                                  'Solo la tecnología',
                                  'Solo el mercado'],
                 'correcta': 'B'},
                {'pregunta': 'La dotación de recursos naturales es, en '
                             'general:',
                 'alternativas': ['Ilimitada',
                                  'Limitada o escasa',
                                  'Infinita',
                                  'Renovable siempre al 100%',
                                  'Sin ningún costo'],
                 'correcta': 'B'},
                {'pregunta': 'El propietario de un recurso natural recibe '
                             'una retribución llamada:',
                 'alternativas': ['Salario',
                                  'Renta',
                                  'Interés',
                                  'Ganancia empresarial',
                                  'Dividendo'],
                 'correcta': 'B'},
                {'pregunta': 'El medio geográfico, o medio ambiente, '
                             'comprende principalmente:',
                 'alternativas': ['Solo el clima',
                                  'El territorio y el clima',
                                  'Solo el suelo',
                                  'Solo la fauna',
                                  'Solo el subsuelo'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio está constituido por el suelo, '
                             'subsuelo, relieve orográfico y:',
                 'alternativas': ['El comercio',
                                  'La situación geográfica',
                                  'El sistema financiero',
                                  'La moneda nacional',
                                  'El presupuesto público'],
                 'correcta': 'B'},
                {'pregunta': 'El clima condiciona directamente actividades '
                             'económicas como:',
                 'alternativas': ['El comercio internacional exclusivamente',
                                  'La agricultura y la producción textil',
                                  'La banca central',
                                  'El sistema tributario',
                                  'La política monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú cuenta con un número de microclimas '
                             'superior a:',
                 'alternativas': ['10', '80', '5', '20', '200'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos primarios sin extraer ni '
                             'modificar por el hombre se llaman:',
                 'alternativas': ['Materias primas',
                                  'Materias brutas',
                                  'Bienes finales',
                                  'Bienes de capital',
                                  'Insumos industriales'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos que la naturaleza ofrece y '
                             'sirven de base para elaborar bienes finales se '
                             'llaman:',
                 'alternativas': ['Materias brutas',
                                  'Materias primas',
                                  'Bienes libres',
                                  'Recursos financieros',
                                  'Activos fijos'],
                 'correcta': 'B'},
                {'pregunta': 'El algodón, fruto del trabajo agrícola, es un '
                             'ejemplo de:',
                 'alternativas': ['Materia bruta',
                                  'Materia prima',
                                  'Bien final',
                                  'Bien de capital',
                                  'Recurso financiero'],
                 'correcta': 'B'},
                {'pregunta': 'Las materias primas provienen de tres fuentes: '
                             'animal, vegetal y:',
                 'alternativas': ['Industrial',
                                  'Mineral',
                                  'Financiera',
                                  'Comercial',
                                  'Digital'],
                 'correcta': 'B'},
                {'pregunta': 'La lana, las carnes y el marfil son ejemplos '
                             'de materias primas de origen:',
                 'alternativas': ['Vegetal',
                                  'Animal',
                                  'Mineral',
                                  'Industrial',
                                  'Financiero'],
                 'correcta': 'B'},
                {'pregunta': 'Para aprovechar los recursos naturales, el ser '
                             'humano debe aplicar:',
                 'alternativas': ['Solo capital',
                                  'Su fuerza de trabajo',
                                  'Solo tecnología importada',
                                  'Solo comercio exterior',
                                  'Ningún esfuerzo adicional'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza se presenta como un depósito de '
                             'materias brutas y fuentes de:',
                 'alternativas': ['Comercio',
                                  'Energías',
                                  'Impuestos',
                                  'Créditos',
                                  'Inflación'],
                 'correcta': 'B'},
                {'pregunta': 'En la sierra sur del Perú, la producción de '
                             'papa se explica por la influencia de:',
                 'alternativas': ['El comercio exterior',
                                  'El suelo y el clima',
                                  'La política monetaria',
                                  'El sistema financiero',
                                  'La tecnología importada'],
                 'correcta': 'B'},
                {'pregunta': 'El descanso de tierras y la rotación de '
                             'cultivos en la sierra ejemplifican:',
                 'alternativas': ['La imposición total del hombre sobre la '
                                  'naturaleza',
                                  'Una búsqueda de armonía entre el hombre y '
                                  'la naturaleza',
                                  'El abandono total de la agricultura',
                                  'La eliminación del factor tierra',
                                  'La sustitución de la tierra por capital'],
                 'correcta': 'B'}]},
 {'num': 8,
  'titulo': 'Empresa',
  'secciones': [{'titulo': '8.1 CONCEPTO',
                 'items': ['La empresa es una unidad económica de producción '
                           'de bienes o prestación de {servicios}.',
                           'La empresa combina los factores clásicos de la '
                           'producción: {naturaleza}, trabajo y {capital}.',
                           'Quien dirige la empresa es el {empresario}, que '
                           'busca la maximización de {ganancias} optimizando '
                           'el uso de recursos.']},
                {'titulo': '8.2 CARACTERÍSTICAS GENERALES',
                 'items': ['La empresa tiene un fin {económico}: se organiza '
                           'para generar riqueza mediante la producción.',
                           'La empresa tiene un fin {mercantil}: su '
                           'producción se destina al intercambio en el '
                           '{mercado}.',
                           'La empresa tiene un fin {lucrativo}: el '
                           'empresario busca maximizar ganancias minimizando '
                           '{costos}.',
                           'La empresa asume una responsabilidad {económica} '
                           'y {social} ante la sociedad.']},
                {'titulo': '8.3 CLASIFICACIÓN SEGÚN EL PROPIETARIO',
                 'items': ['Las empresas {privadas} están constituidas por '
                           'el aporte de personas o instituciones '
                           'particulares, con fin de {lucro}.',
                           'Las empresas {públicas} reciben el capital '
                           'social del Estado, y su finalidad no es '
                           'exclusivamente el lucro sino prestar {servicios} '
                           'a la colectividad.',
                           'Las empresas {mixtas} reciben capital en parte '
                           'del Estado y en parte de instituciones privadas.',
                           'Para ser mixta, el Estado debe tener un mínimo '
                           'de {20}% de las acciones y poder de decisión.']},
                {'titulo': '8.4 CLASIFICACIÓN SEGÚN EL ASPECTO JURÍDICO',
                 'items': ['Las empresas {individuales} no tienen socios; el '
                           'propietario es el único que aporta el capital.',
                           'En la empresa {unipersonal}, la responsabilidad '
                           'del propietario es {ilimitada}: responde con '
                           'todo su patrimonio.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La empresa se define como una unidad económica '
                           'de producción de bienes o {Prestación de '
                           'servicios}.',
                           'La empresa combina los factores clásicos de '
                           'producción: naturaleza, trabajo y {Capital}.',
                           'Quien dirige la empresa, buscando maximizar '
                           'ganancias, es {El empresario}.',
                           'Que la empresa se organice para generar riqueza '
                           'corresponde a su fin {Económico}.',
                           'Que la producción de la empresa se destine al '
                           'intercambio en el mercado corresponde a su fin '
                           '{Mercantil}.',
                           'Que el empresario busque maximizar ganancias '
                           'minimizando costos corresponde a su fin '
                           '{Lucrativo}.',
                           'La responsabilidad de proveer bienes que no '
                           'causen peligro en su consumo corresponde a la '
                           'responsabilidad {Social}.',
                           'Las empresas constituidas por el aporte de '
                           'personas o instituciones particulares son las '
                           'empresas {Privadas}.',
                           'Las empresas en las que el Estado aporta el '
                           'capital social se llaman empresas {Públicas}.',
                           'La finalidad de las empresas públicas es '
                           'principalmente {Prestar servicios a la '
                           'colectividad}.',
                           'Las empresas en las que el capital proviene en '
                           'parte del Estado y en parte de privados se '
                           'llaman empresas {Mixtas}.',
                           'Para ser considerada mixta, el Estado debe tener '
                           'como mínimo un porcentaje de acciones de {20%}.',
                           'El proceso mediante el cual el Estado transfiere '
                           'su participación empresarial al sector privado '
                           'se llama {Privatización}.',
                           'Las empresas en las que no existen socios y el '
                           'propietario aporta todo el capital son las '
                           'empresas {Individuales}.',
                           'En la empresa unipersonal, la responsabilidad '
                           'del propietario es {Ilimitada, responde con todo '
                           'su patrimonio}.',
                           'Para constituir una empresa unipersonal {No se '
                           'requiere escritura pública}.',
                           'Las empresas privadas de varios propietarios se '
                           'conocen como {Sociedades mercantiles}.',
                           'Entre los precios más importantes para las '
                           'decisiones empresariales figura el costo de la '
                           'mano de obra, es decir {Los salarios}.',
                           'La importancia de la empresa radica, entre otros '
                           'aspectos, en el incremento constante de {La '
                           'productividad}.',
                           'La empresa es descrita como el centro del '
                           'proceso productivo en una economía '
                           '{Capitalista}.']},
                {'titulo': '8.5 LA EMPRESA INDIVIDUAL DE RESPONSABILIDAD '
                           'LIMITADA (EIRL)',
                 'items': ['En la {EIRL}, el propietario único acude al '
                           'Registro Mercantil, constituyendo una persona '
                           'jurídica con patrimonio {propio}.',
                           'En la EIRL, la responsabilidad está {limitada} '
                           'al patrimonio de la empresa; el titular no '
                           'responde con su patrimonio personal.',
                           'En la EIRL, el {titular} es el órgano máximo; la '
                           '{gerencia} administra y representa a la '
                           'empresa.']},
                {'titulo': '8.6 EMPRESAS SOCIETARIAS',
                 'items': ['La {sociedad civil} agrupa a personas que '
                           'aportan bienes o servicios para ejercer una '
                           'profesión, como estudios de {abogados}.',
                           'Las {sociedades mercantiles} se forman para '
                           'desarrollar actividades con fines {lucrativos}.',
                           'En la {Sociedad Colectiva}, los socios responden '
                           'de forma {ilimitada} y solidaria por las deudas '
                           'sociales.',
                           'En la {Sociedad Comercial de Responsabilidad '
                           'Limitada} (S.R.L.), participan entre {2} y 20 '
                           'socios, llamados {participacionistas}.',
                           'En la S.R.L., la responsabilidad de los socios '
                           'está {limitada} al monto aportado al capital '
                           'social.',
                           'La {Sociedad Anónima} (S.A.) tiene su capital '
                           'representado por {acciones} nominativas.',
                           'En la Sociedad Anónima, los socios se llaman '
                           '{accionistas}, y ninguno responde con su '
                           'patrimonio personal por las deudas.',
                           'La {Junta General de Accionistas} es el órgano '
                           'máximo y soberano de la Sociedad Anónima.']}],
  'cuadros': [{'titulo': '8.3 CLASIFICACIÓN DE LA EMPRESA SEGÚN EL '
                         'PROPIETARIO',
               'encabezados': ['Tipo', 'Aportante del capital'],
               'filas': [['{Privada}',
                          '{Personas} o instituciones particulares'],
                         ['{Pública}', 'El {Estado}'],
                         ['{Mixta}', 'Estado y {privados} a la vez']]}],
  'preguntas': [{'pregunta': 'La empresa se define como una unidad económica '
                             'de producción de bienes o:',
                 'alternativas': ['Consumo exclusivo',
                                  'Prestación de servicios',
                                  'Ahorro personal',
                                  'Recaudación tributaria',
                                  'Emisión monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'La empresa combina los factores clásicos de '
                             'producción: naturaleza, trabajo y:',
                 'alternativas': ['Comercio',
                                  'Capital',
                                  'Dinero exclusivamente',
                                  'Impuestos',
                                  'Publicidad'],
                 'correcta': 'B'},
                {'pregunta': 'Quien dirige la empresa, buscando maximizar '
                             'ganancias, es:',
                 'alternativas': ['El Estado',
                                  'El empresario',
                                  'El consumidor',
                                  'El trabajador exclusivamente',
                                  'El banco central'],
                 'correcta': 'B'},
                {'pregunta': 'Que la empresa se organice para generar '
                             'riqueza corresponde a su fin:',
                 'alternativas': ['Mercantil',
                                  'Económico',
                                  'Lucrativo exclusivo',
                                  'Social',
                                  'Jurídico'],
                 'correcta': 'B'},
                {'pregunta': 'Que la producción de la empresa se destine al '
                             'intercambio en el mercado corresponde a su '
                             'fin:',
                 'alternativas': ['Económico',
                                  'Mercantil',
                                  'Social',
                                  'Jurídico',
                                  'Ninguno en particular'],
                 'correcta': 'B'},
                {'pregunta': 'Que el empresario busque maximizar ganancias '
                             'minimizando costos corresponde a su fin:',
                 'alternativas': ['Mercantil',
                                  'Lucrativo',
                                  'Social',
                                  'Económico general',
                                  'Jurídico'],
                 'correcta': 'B'},
                {'pregunta': 'La responsabilidad de proveer bienes que no '
                             'causen peligro en su consumo corresponde a la '
                             'responsabilidad:',
                 'alternativas': ['Económica',
                                  'Social',
                                  'Jurídica exclusiva',
                                  'Tributaria',
                                  'Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas constituidas por el aporte de '
                             'personas o instituciones particulares son las '
                             'empresas:',
                 'alternativas': ['Públicas',
                                  'Privadas',
                                  'Mixtas',
                                  'Estatales',
                                  'Municipales exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas en las que el Estado aporta el '
                             'capital social se llaman empresas:',
                 'alternativas': ['Privadas',
                                  'Públicas',
                                  'Mixtas',
                                  'Individuales',
                                  'Unipersonales'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad de las empresas públicas es '
                             'principalmente:',
                 'alternativas': ['El lucro exclusivo',
                                  'Prestar servicios a la colectividad',
                                  'La especulación financiera',
                                  'El comercio exterior únicamente',
                                  'La evasión tributaria'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas en las que el capital proviene en '
                             'parte del Estado y en parte de privados se '
                             'llaman empresas:',
                 'alternativas': ['Públicas',
                                  'Mixtas',
                                  'Privadas',
                                  'Individuales',
                                  'Unipersonales'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser considerada mixta, el Estado debe '
                             'tener como mínimo un porcentaje de acciones '
                             'de:',
                 'alternativas': ['5%', '20%', '50%', '80%', '100%'],
                 'correcta': 'B'},
                {'pregunta': 'El proceso mediante el cual el Estado '
                             'transfiere su participación empresarial al '
                             'sector privado se llama:',
                 'alternativas': ['Nacionalización',
                                  'Privatización',
                                  'Estatización',
                                  'Colectivización',
                                  'Municipalización'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas en las que no existen socios y el '
                             'propietario aporta todo el capital son las '
                             'empresas:',
                 'alternativas': ['Mixtas',
                                  'Individuales',
                                  'Públicas',
                                  'Sociedades mercantiles',
                                  'Cooperativas'],
                 'correcta': 'B'},
                {'pregunta': 'En la empresa unipersonal, la responsabilidad '
                             'del propietario es:',
                 'alternativas': ['Limitada al capital aportado',
                                  'Ilimitada, responde con todo su '
                                  'patrimonio',
                                  'Nula',
                                  'Compartida con el Estado',
                                  'Transferible a terceros'],
                 'correcta': 'B'},
                {'pregunta': 'Para constituir una empresa unipersonal:',
                 'alternativas': ['Se requiere escritura pública obligatoria',
                                  'No se requiere escritura pública',
                                  'Se necesita autorización del Congreso',
                                  'Se requiere capital extranjero',
                                  'Se necesita ser una sociedad mercantil'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas privadas de varios propietarios '
                             'se conocen como:',
                 'alternativas': ['Empresas unipersonales',
                                  'Sociedades mercantiles',
                                  'Empresas públicas',
                                  'Empresas mixtas obligatorias',
                                  'Cooperativas estatales'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los precios más importantes para las '
                             'decisiones empresariales figura el costo de la '
                             'mano de obra, es decir:',
                 'alternativas': ['Los impuestos',
                                  'Los salarios',
                                  'Las utilidades',
                                  'El tipo de cambio',
                                  'La inflación'],
                 'correcta': 'B'},
                {'pregunta': 'La importancia de la empresa radica, entre '
                             'otros aspectos, en el incremento constante de:',
                 'alternativas': ['La informalidad',
                                  'La productividad',
                                  'La evasión fiscal',
                                  'El endeudamiento',
                                  'La especulación'],
                 'correcta': 'B'},
                {'pregunta': 'La empresa es descrita como el centro del '
                             'proceso productivo en una economía:',
                 'alternativas': ['Feudal',
                                  'Capitalista',
                                  'Primitiva',
                                  'De trueque',
                                  'Autárquica'],
                 'correcta': 'B'},
                {'pregunta': 'En la EIRL, el propietario único acude al '
                             'Registro Mercantil para constituir una persona '
                             'jurídica con:',
                 'alternativas': ['Patrimonio del propietario exclusivamente',
                                  'Patrimonio propio, independiente del '
                                  'propietario',
                                  'Ningún patrimonio',
                                  'Patrimonio compartido con el Estado',
                                  'Patrimonio de terceros'],
                 'correcta': 'B'},
                {'pregunta': 'En la EIRL, la responsabilidad de la empresa '
                             'está limitada a:',
                 'alternativas': ['El patrimonio personal del titular',
                                  'El patrimonio de la empresa',
                                  'Ningún límite',
                                  'El doble del capital aportado',
                                  'La mitad del capital aportado'],
                 'correcta': 'B'},
                {'pregunta': 'En la EIRL, el órgano máximo que decide sobre '
                             'los bienes y actividades es:',
                 'alternativas': ['La gerencia',
                                  'El titular',
                                  'La junta de socios',
                                  'El directorio',
                                  'Los accionistas'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad civil es utilizada frecuentemente '
                             'por estudios de abogados y otras:',
                 'alternativas': ['Fábricas industriales',
                                  'Asociaciones profesionales',
                                  'Minas',
                                  'Granjas',
                                  'Empresas navieras'],
                 'correcta': 'B'},
                {'pregunta': 'Las sociedades mercantiles se forman con la '
                             'finalidad de desarrollar actividades:',
                 'alternativas': ['Sin fines de lucro',
                                  'Con fines lucrativos',
                                  'Solo educativas',
                                  'Solo benéficas',
                                  'Solo religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'En la Sociedad Colectiva, los socios responden '
                             'por las deudas sociales de forma:',
                 'alternativas': ['Limitada',
                                  'Ilimitada y solidaria',
                                  'Nula',
                                  'Proporcional exclusivamente',
                                  'Estatal'],
                 'correcta': 'B'},
                {'pregunta': 'La Sociedad Comercial de Responsabilidad '
                             'Limitada (S.R.L.) puede tener entre 2 y un '
                             'máximo de:',
                 'alternativas': ['10 socios',
                                  '20 socios',
                                  '50 socios',
                                  '100 socios',
                                  '5 socios'],
                 'correcta': 'B'},
                {'pregunta': 'En la S.R.L., los socios se denominan:',
                 'alternativas': ['Accionistas',
                                  'Socios participacionistas',
                                  'Socios colectivos',
                                  'Titulares',
                                  'Gerentes'],
                 'correcta': 'B'},
                {'pregunta': 'En la S.R.L., la responsabilidad de los socios '
                             'está limitada a:',
                 'alternativas': ['Todo su patrimonio personal',
                                  'El monto aportado al capital social',
                                  'El doble del aporte',
                                  'Ningún límite',
                                  'La ganancia obtenida'],
                 'correcta': 'B'},
                {'pregunta': 'El capital de la Sociedad Anónima (S.A.) está '
                             'representado por:',
                 'alternativas': ['Participaciones',
                                  'Acciones nominativas',
                                  'Bonos',
                                  'Cuotas fijas',
                                  'Aportes simples'],
                 'correcta': 'B'},
                {'pregunta': 'En la Sociedad Anónima, los socios reciben el '
                             'nombre de:',
                 'alternativas': ['Participacionistas',
                                  'Accionistas',
                                  'Socios colectivos',
                                  'Titulares',
                                  'Gestores'],
                 'correcta': 'B'},
                {'pregunta': 'En la Sociedad Anónima, la responsabilidad de '
                             'los accionistas frente a las deudas de la '
                             'empresa es:',
                 'alternativas': ['Ilimitada y personal',
                                  'Limitada, sin comprometer su patrimonio '
                                  'personal',
                                  'Solidaria total',
                                  'Inexistente legalmente',
                                  'Compartida con el Estado'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano máximo y soberano de la Sociedad '
                             'Anónima es:',
                 'alternativas': ['El Directorio',
                                  'La Junta General de Accionistas',
                                  'La Gerencia General',
                                  'El Titular',
                                  'El Consejo de Vigilancia'],
                 'correcta': 'B'}]},
 {'num': 9,
  'titulo': 'Demanda',
  'secciones': [{'titulo': '9.1 CONCEPTO',
                 'items': ['La demanda es la cantidad de bienes y servicios '
                           'que un comprador puede y {desea} adquirir a '
                           'diferentes niveles de precios.',
                           'La demanda expresa la conducta {racional} del '
                           'consumidor en el mercado.',
                           'Para que exista demanda deben estar presentes '
                           'siempre el {deseo} y la capacidad de {compra}.',
                           'Quien desea un bien pero no tiene capacidad '
                           'adquisitiva es consumidor con necesidades, pero '
                           '{no} es demandante.']},
                {'titulo': '9.2 EL PRECIO DEL PRODUCTO',
                 'items': ['El {precio} del producto es el factor más '
                           'importante para demandar un bien.',
                           'La cantidad demandada {aumenta} si el precio del '
                           'bien disminuye, y disminuye si el precio '
                           '{aumenta}.']},
                {'titulo': '9.3 BIENES SUSTITUTOS Y COMPLEMENTARIOS',
                 'items': ['Los bienes {sustitutos} pueden reemplazarse el '
                           'uno al otro, dando una satisfacción similar, '
                           'como el pollo y el {pescado}.',
                           'Cuando el aumento del precio de un bien produce '
                           'un aumento en la demanda de otro, se dice que '
                           'ambos bienes son {sustitutos}.',
                           'Los bienes {complementarios} se consumen a la '
                           'vez, como los autos y la {gasolina}.',
                           'Cuando dos bienes son complementarios, la '
                           'disminución del precio de uno genera un '
                           '{aumento} en la demanda del otro.']},
                {'titulo': '9.4 INGRESO, RIQUEZA Y OTROS FACTORES',
                 'items': ['El {ingreso} es la suma de sueldos, utilidades, '
                           'intereses y rentas que recibe una persona en un '
                           'periodo.',
                           'La {riqueza} es el valor total de las '
                           'pertenencias de una familia, descontadas sus '
                           '{deudas}.',
                           'Los bienes cuya demanda aumenta cuando sube el '
                           'ingreso se llaman bienes {normales}.',
                           'Los bienes cuya demanda baja cuando el ingreso '
                           'aumenta se llaman bienes {inferiores}.',
                           'Los {gustos y preferencias} son un aspecto '
                           'subjetivo que varía según edad, sexo y moda.',
                           'La demanda actual también depende de los precios '
                           '{futuros} esperados de un bien.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La demanda se define como la cantidad de bienes '
                           'que un comprador puede y {Desea adquirir a '
                           'diferentes precios}.',
                           'La demanda expresa la conducta racional de {El '
                           'consumidor en el mercado}.',
                           'Para que exista demanda deben estar presentes '
                           'siempre el deseo y {La capacidad de compra}.',
                           'Una persona que desea un bien pero no tiene '
                           'dinero para comprarlo es {Un consumidor con '
                           'necesidades, pero no demandante}.',
                           'El factor más importante para demandar un '
                           'producto es {El precio del producto}.',
                           'Cuando el precio de un bien disminuye, la '
                           'cantidad demandada, por regla general {Aumenta}.',
                           'Los bienes que pueden reemplazarse el uno al '
                           'otro dando una satisfacción similar se llaman '
                           'bienes {Sustitutos}.',
                           'El pollo y el pescado son un ejemplo típico de '
                           'bienes {Sustitutos}.',
                           'Cuando el aumento del precio de un bien genera '
                           'un aumento en la demanda de otro, ambos bienes '
                           'son {Sustitutos}.',
                           'Los bienes que se consumen a la vez, como los '
                           'autos y la gasolina, son bienes '
                           '{Complementarios}.',
                           'Cuando dos bienes son complementarios, la '
                           'disminución del precio de uno genera en la '
                           'demanda del otro {Un aumento}.',
                           'El ingreso se define como la suma de sueldos, '
                           'utilidades, intereses y {Rentas}.',
                           'La riqueza se define como el valor total de las '
                           'pertenencias de una familia, descontadas {Sus '
                           'deudas}.',
                           'Los bienes cuya demanda baja cuando el ingreso '
                           'familiar aumenta se llaman bienes {Inferiores}.',
                           'Los gustos y preferencias del consumidor son un '
                           'aspecto {Subjetivo, que varía según edad, sexo y '
                           'moda}.',
                           'La demanda actual de un bien también depende de '
                           '{Los precios futuros esperados}.',
                           'En verano aumenta la demanda de helados y '
                           'gaseosas debido al factor {Clima}.',
                           'Si las amas de casa esperan que el precio del '
                           'pollo suba el próximo mes, la demanda presente '
                           'de pollo probablemente {Aumentará}.',
                           'Las inversiones en publicidad buscan influir '
                           'principalmente en {Los gustos y preferencias de '
                           'los consumidores}.']},
                {'titulo': '9.5 ELASTICIDAD PRECIO DE LA DEMANDA',
                 'items': ['La {elasticidad precio} de la demanda mide el '
                           'grado de sensibilidad de la cantidad demandada '
                           'ante variaciones del {precio}.',
                           'La elasticidad expresa la variación {porcentual} '
                           'de la cantidad demandada ante la variación '
                           'porcentual del precio.',
                           'El signo de la elasticidad precio siempre es '
                           '{negativo}, porque la demanda tiene pendiente '
                           'negativa.',
                           'Con fines prácticos, se prefiere utilizar el '
                           'valor {absoluto} de la elasticidad.']},
                {'titulo': '9.6 TIPOS DE ELASTICIDAD PRECIO',
                 'items': ['La demanda {perfectamente elástica} tiene un '
                           'valor de elasticidad {infinito}; el bien tiene '
                           'sustitutos perfectos.',
                           'La demanda {relativamente elástica} tiene valor '
                           'absoluto {mayor} a 1: la cantidad reacciona más '
                           'que proporcionalmente.',
                           'La demanda {unitaria} tiene valor absoluto igual '
                           'a {1}: la cantidad varía en el mismo porcentaje '
                           'que el precio.',
                           'La demanda {relativamente inelástica} tiene '
                           'valor absoluto {menor} a 1: la cantidad '
                           'reacciona menos que proporcionalmente.']}],
  'cuadros': [{'titulo': '9.3 SUSTITUTOS FRENTE A COMPLEMENTARIOS',
               'encabezados': ['Tipo de bien',
                               'Efecto del alza de precio de uno sobre el '
                               'otro'],
               'filas': [['{Sustitutos}', '{Aumenta} la demanda del otro'],
                         ['{Complementarios}',
                          '{Disminuye} la demanda del otro']]}],
  'preguntas': [{'pregunta': 'La demanda se define como la cantidad de '
                             'bienes que un comprador puede y:',
                 'alternativas': ['Debe adquirir obligatoriamente',
                                  'Desea adquirir a diferentes precios',
                                  'Produce directamente',
                                  'Vende en el mercado',
                                  'Almacena indefinidamente'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda expresa la conducta racional de:',
                 'alternativas': ['El productor',
                                  'El consumidor en el mercado',
                                  'El Estado',
                                  'El banco central',
                                  'El importador'],
                 'correcta': 'B'},
                {'pregunta': 'Para que exista demanda deben estar presentes '
                             'siempre el deseo y:',
                 'alternativas': ['La publicidad',
                                  'La capacidad de compra',
                                  'La escasez absoluta',
                                  'El crédito bancario',
                                  'La inflación'],
                 'correcta': 'B'},
                {'pregunta': 'Una persona que desea un bien pero no tiene '
                             'dinero para comprarlo es:',
                 'alternativas': ['Un demandante pleno',
                                  'Un consumidor con necesidades, pero no '
                                  'demandante',
                                  'Un oferente',
                                  'Un productor',
                                  'Un inversionista'],
                 'correcta': 'B'},
                {'pregunta': 'El factor más importante para demandar un '
                             'producto es:',
                 'alternativas': ['La publicidad',
                                  'El precio del producto',
                                  'El clima',
                                  'La moda',
                                  'El color del empaque'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el precio de un bien disminuye, la '
                             'cantidad demandada, por regla general:',
                 'alternativas': ['Disminuye',
                                  'Aumenta',
                                  'Se mantiene igual siempre',
                                  'Desaparece',
                                  'Se vuelve negativa'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes que pueden reemplazarse el uno al '
                             'otro dando una satisfacción similar se llaman '
                             'bienes:',
                 'alternativas': ['Complementarios',
                                  'Sustitutos',
                                  'Inferiores',
                                  'Normales',
                                  'De lujo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El pollo y el pescado son un ejemplo típico de '
                             'bienes:',
                 'alternativas': ['Complementarios',
                                  'Sustitutos',
                                  'Inferiores exclusivos',
                                  'De lujo',
                                  'Normales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el aumento del precio de un bien genera '
                             'un aumento en la demanda de otro, ambos bienes '
                             'son:',
                 'alternativas': ['Complementarios',
                                  'Sustitutos',
                                  'Inferiores',
                                  'Normales',
                                  'Independientes'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes que se consumen a la vez, como los '
                             'autos y la gasolina, son bienes:',
                 'alternativas': ['Sustitutos',
                                  'Complementarios',
                                  'Inferiores',
                                  'Normales exclusivos',
                                  'De lujo'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando dos bienes son complementarios, la '
                             'disminución del precio de uno genera en la '
                             'demanda del otro:',
                 'alternativas': ['Una disminución',
                                  'Un aumento',
                                  'Ningún efecto',
                                  'Una eliminación total',
                                  'Un efecto aleatorio'],
                 'correcta': 'B'},
                {'pregunta': 'El ingreso se define como la suma de sueldos, '
                             'utilidades, intereses y:',
                 'alternativas': ['Deudas',
                                  'Rentas',
                                  'Impuestos',
                                  'Ahorros exclusivos',
                                  'Inversiones exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'La riqueza se define como el valor total de '
                             'las pertenencias de una familia, descontadas:',
                 'alternativas': ['Sus ingresos',
                                  'Sus deudas',
                                  'Sus gastos mensuales',
                                  'Sus impuestos',
                                  'Sus ahorros'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes cuya demanda aumenta cuando sube el '
                             'ingreso se llaman bienes:',
                 'alternativas': ['Inferiores',
                                  'Normales',
                                  'Sustitutos exclusivos',
                                  'Complementarios exclusivos',
                                  'De primera necesidad únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes cuya demanda baja cuando el ingreso '
                             'familiar aumenta se llaman bienes:',
                 'alternativas': ['Normales',
                                  'Inferiores',
                                  'Sustitutos',
                                  'Complementarios',
                                  'De lujo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los gustos y preferencias del consumidor son '
                             'un aspecto:',
                 'alternativas': ['Objetivo y fijo',
                                  'Subjetivo, que varía según edad, sexo y '
                                  'moda',
                                  'Sin relación con la demanda',
                                  'Determinado exclusivamente por el Estado',
                                  'Igual para todos los consumidores'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda actual de un bien también depende '
                             'de:',
                 'alternativas': ['Solo el precio pasado',
                                  'Los precios futuros esperados',
                                  'Solo la producción actual',
                                  'Solo el clima',
                                  'Solo la publicidad pasada'],
                 'correcta': 'B'},
                {'pregunta': 'En verano aumenta la demanda de helados y '
                             'gaseosas debido al factor:',
                 'alternativas': ['Precio',
                                  'Ingreso',
                                  'Clima',
                                  'Riqueza',
                                  'Publicidad'],
                 'correcta': 'C'},
                {'pregunta': 'Si las amas de casa esperan que el precio del '
                             'pollo suba el próximo mes, la demanda presente '
                             'de pollo probablemente:',
                 'alternativas': ['Disminuirá',
                                  'Aumentará',
                                  'No cambiará',
                                  'Desaparecerá',
                                  'Se volverá negativa'],
                 'correcta': 'B'},
                {'pregunta': 'Las inversiones en publicidad buscan influir '
                             'principalmente en:',
                 'alternativas': ['El precio de mercado',
                                  'Los gustos y preferencias de los '
                                  'consumidores',
                                  'La tasa de interés',
                                  'El tipo de cambio',
                                  'La oferta monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'La elasticidad precio de la demanda mide el '
                             'grado de sensibilidad de la cantidad demandada '
                             'ante variaciones del:',
                 'alternativas': ['Ingreso',
                                  'Precio',
                                  'Gusto del consumidor',
                                  'Clima',
                                  'Costo de producción'],
                 'correcta': 'B'},
                {'pregunta': 'La elasticidad precio expresa la variación '
                             'porcentual de la cantidad demandada ante la '
                             'variación:',
                 'alternativas': ['Absoluta del ingreso',
                                  'Porcentual del precio',
                                  'Del tipo de cambio',
                                  'De la oferta monetaria',
                                  'Del PBI'],
                 'correcta': 'B'},
                {'pregunta': 'El signo de la elasticidad precio de la '
                             'demanda siempre es:',
                 'alternativas': ['Positivo',
                                  'Negativo',
                                  'Cero',
                                  'Indefinido',
                                  'Variable según el país'],
                 'correcta': 'B'},
                {'pregunta': 'Con fines prácticos, para interpretar la '
                             'elasticidad se prefiere utilizar su valor:',
                 'alternativas': ['Relativo',
                                  'Absoluto',
                                  'Negativo directo',
                                  'Porcentual sin signo alguno',
                                  'Promedio histórico'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda perfectamente elástica tiene un '
                             'valor de elasticidad:',
                 'alternativas': ['Igual a cero',
                                  'Infinito',
                                  'Igual a uno',
                                  'Negativo puro',
                                  'Indeterminado'],
                 'correcta': 'B'},
                {'pregunta': 'Un bien con demanda perfectamente elástica se '
                             'caracteriza por tener:',
                 'alternativas': ['Ningún sustituto',
                                  'Gran cantidad de sustitutos perfectos',
                                  'Un solo comprador',
                                  'Precio fijo por ley',
                                  'Oferta ilimitada'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda relativamente elástica tiene un '
                             'valor absoluto de elasticidad:',
                 'alternativas': ['Menor a 1',
                                  'Mayor a 1',
                                  'Igual a 1',
                                  'Igual a cero',
                                  'Negativo sin valor'],
                 'correcta': 'B'},
                {'pregunta': 'En la demanda relativamente elástica, la '
                             'cantidad demandada reacciona, frente al '
                             'precio, de forma:',
                 'alternativas': ['Menos que proporcional',
                                  'Más que proporcional',
                                  'Idéntica siempre',
                                  'Nula',
                                  'Aleatoria'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda de elasticidad unitaria tiene un '
                             'valor absoluto igual a:',
                 'alternativas': ['0', '1', 'Infinito', '2', '0,5'],
                 'correcta': 'B'},
                {'pregunta': 'En la demanda unitaria, si el precio sube 1%, '
                             'la cantidad demandada se reduce en:',
                 'alternativas': ['0,5%',
                                  '1%',
                                  '2%',
                                  '10%',
                                  'Ninguna variación'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda relativamente inelástica tiene un '
                             'valor absoluto de elasticidad:',
                 'alternativas': ['Mayor a 1',
                                  'Menor a 1',
                                  'Igual a 1',
                                  'Infinito',
                                  'Negativo puro'],
                 'correcta': 'B'},
                {'pregunta': 'En la demanda relativamente inelástica, la '
                             'cantidad demandada reacciona ante el precio de '
                             'forma:',
                 'alternativas': ['Más que proporcional',
                                  'Menos que proporcional',
                                  'Idéntica al precio',
                                  'Inversa exacta',
                                  'Nula'],
                 'correcta': 'B'}]},
 {'num': 10,
  'titulo': 'Oferta',
  'secciones': [{'titulo': '10.1 CONCEPTO',
                 'items': ['La oferta es la cantidad de un bien o servicio '
                           'que los vendedores-productores están dispuestos '
                           'a {vender} a diversos niveles de precios.',
                           'La oferta refleja el comportamiento de los '
                           '{vendedores}, que expresan sus deseos de venta '
                           'en función de los precios del mercado.']},
                {'titulo': '10.2 EL PRECIO Y LOS COSTOS DE PRODUCCIÓN',
                 'items': ['Un precio {elevado} motiva a los ofertantes a '
                           'producir y vender {más}.',
                           'Los {costos de producción} dependen de los '
                           'precios de los insumos, la mano de obra y los '
                           '{impuestos}.',
                           'Un campesino producirá el cultivo que le genere '
                           'buenas {ganancias}, no solo que cubra sus '
                           'costos.']},
                {'titulo': '10.3 BIENES ALTERNATIVOS Y COMPLEMENTARIOS EN LA '
                           'PRODUCCIÓN',
                 'items': ['Los productos {alternativos} pueden producirse '
                           'indistintamente con los mismos factores, como el '
                           'pan y los panetones.',
                           'Los productos {complementarios} en la '
                           'producción, o conjuntos, se producen como un '
                           'lote, como la lana y la carne de {oveja}.',
                           'Al subir el precio del petróleo aumenta también '
                           'la producción de {kerosene}, por ser productos '
                           'complementarios.']},
                {'titulo': '10.4 OTROS FACTORES QUE AFECTAN LA OFERTA',
                 'items': ['Los {precios esperados} del bien son la '
                           'expectativa de los ofertantes respecto a los '
                           'precios futuros.',
                           'Las {condiciones climáticas}, como sequías o '
                           'inundaciones, reducen la producción y por tanto '
                           'la oferta.',
                           'Las políticas económicas {liberales} reducen '
                           'impuestos a bienes importados, aumentando la '
                           'oferta.',
                           'Las políticas {proteccionistas} elevan aranceles '
                           'y reducen la oferta de bienes importados.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La oferta se define como la cantidad de un bien '
                           'que los vendedores están dispuestos a {Vender a '
                           'diversos precios}.',
                           'La oferta refleja el comportamiento de {Los '
                           'vendedores o productores}.',
                           'Un precio elevado motiva a los ofertantes a '
                           '{Producir y vender más}.',
                           'Los costos de producción dependen de los precios '
                           'de los insumos, la mano de obra y {Los '
                           'impuestos}.',
                           'Un campesino elegirá producir el cultivo que le '
                           'genere {Buenas ganancias}.',
                           'Los productos que pueden fabricarse '
                           'indistintamente con los mismos factores de '
                           'producción se llaman productos {Alternativos}.',
                           'El pan, los bizcochos y los panetones son '
                           'ejemplos de productos {Alternativos en la '
                           'producción}.',
                           'Los productos que se producen como un lote '
                           'conjunto se llaman productos {Complementarios en '
                           'la producción}.',
                           'La lana y la carne de oveja son un ejemplo de '
                           'productos {Complementarios en la producción}.',
                           'Si sube el precio del petróleo, la producción de '
                           'kerosene tiende a {Aumentar}.',
                           'La expectativa de los ofertantes respecto a los '
                           'precios futuros se llama {Precios esperados del '
                           'bien}.',
                           'Si los ofertantes esperan una caída del precio '
                           'futuro, tienden a {Incrementar la producción '
                           'actual}.',
                           'Las sequías e inundaciones son ejemplos del '
                           'factor {Condiciones climáticas}.',
                           'Las condiciones climáticas adversas, como '
                           'sequías, provocan que la oferta {Se reduzca}.',
                           'Las políticas económicas liberales, al reducir '
                           'impuestos a bienes importados, generan {Aumento '
                           'de la oferta por mayores importaciones}.',
                           'Las políticas proteccionistas, al elevar '
                           'aranceles, tienden a {Reducir la oferta de '
                           'bienes importados}.',
                           'Entre los factores que afectan la oferta se '
                           'consideran también las expectativas de {Los '
                           'empresarios}.',
                           'En una carpintería, la producción de mesas, '
                           'camas y sillas ejemplifica productos '
                           '{Alternativos en la producción}.',
                           'El precio de un bien va acompañado del margen de '
                           '{Ganancia del productor}.',
                           'La oferta expresa, en esencia, los deseos de '
                           'venta o producción en función de {Los distintos '
                           'precios existentes en el mercado}.']},
                {'titulo': '10.5 EL EQUILIBRIO DEL MERCADO',
                 'items': ['El {equilibrio del mercado} es la situación en '
                           'la que el nivel de producción (oferta) coincide '
                           'con el nivel de {consumo} (demanda).',
                           'En el equilibrio, la cantidad {ofertada} es '
                           'igual a la cantidad {demandada}: Qd = Qo.',
                           'La {cantidad de equilibrio} es aquella en que '
                           'coinciden las decisiones de ofertantes y '
                           'demandantes.',
                           'El {precio de equilibrio} es aquel en el cual la '
                           'cantidad ofertada es igual a la cantidad '
                           'demandada.',
                           'Gráficamente, el equilibrio se forma en la '
                           '{intersección} entre las curvas de oferta y '
                           'demanda.',
                           'Cuando el precio está por debajo del equilibrio, '
                           'se genera {escasez}, con presión al {alza} sobre '
                           'el precio.',
                           'Cuando el precio está por encima del equilibrio, '
                           'se genera {abundancia} o sobreproducción, con '
                           'presión a la {baja}.']}],
  'cuadros': [{'titulo': '10.4 FACTORES QUE AFECTAN LA OFERTA',
               'encabezados': ['Factor', 'Efecto'],
               'filas': [['{Precio} del producto',
                          'A mayor precio, mayor {oferta}'],
                         ['{Costos} de producción',
                          'A mayor costo, menor oferta'],
                         ['{Condiciones climáticas}',
                          'Sequías reducen la {producción}']]}],
  'preguntas': [{'pregunta': 'La oferta se define como la cantidad de un '
                             'bien que los vendedores están dispuestos a:',
                 'alternativas': ['Comprar',
                                  'Vender a diversos precios',
                                  'Almacenar indefinidamente',
                                  'Regalar',
                                  'Importar exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La oferta refleja el comportamiento de:',
                 'alternativas': ['Los consumidores',
                                  'Los vendedores o productores',
                                  'El Estado exclusivamente',
                                  'Los bancos',
                                  'Los importadores'],
                 'correcta': 'B'},
                {'pregunta': 'Un precio elevado motiva a los ofertantes a:',
                 'alternativas': ['Producir y vender menos',
                                  'Producir y vender más',
                                  'Dejar de producir',
                                  'Reducir la calidad',
                                  'Cerrar la empresa'],
                 'correcta': 'B'},
                {'pregunta': 'Los costos de producción dependen de los '
                             'precios de los insumos, la mano de obra y:',
                 'alternativas': ['La publicidad',
                                  'Los impuestos',
                                  'El clima exclusivamente',
                                  'La moda',
                                  'El tipo de cambio exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Un campesino elegirá producir el cultivo que '
                             'le genere:',
                 'alternativas': ['Solo cubrir costos',
                                  'Buenas ganancias',
                                  'Pérdidas mínimas',
                                  'Ningún beneficio',
                                  'Solo prestigio social'],
                 'correcta': 'B'},
                {'pregunta': 'Los productos que pueden fabricarse '
                             'indistintamente con los mismos factores de '
                             'producción se llaman productos:',
                 'alternativas': ['Complementarios',
                                  'Alternativos',
                                  'Sustitutos en demanda',
                                  'Inferiores',
                                  'Normales'],
                 'correcta': 'B'},
                {'pregunta': 'El pan, los bizcochos y los panetones son '
                             'ejemplos de productos:',
                 'alternativas': ['Complementarios en la producción',
                                  'Alternativos en la producción',
                                  'Sustitutos en la demanda',
                                  'Inferiores',
                                  'De lujo'],
                 'correcta': 'B'},
                {'pregunta': 'Los productos que se producen como un lote '
                             'conjunto se llaman productos:',
                 'alternativas': ['Alternativos',
                                  'Complementarios en la producción',
                                  'Sustitutos',
                                  'Inferiores',
                                  'Normales'],
                 'correcta': 'B'},
                {'pregunta': 'La lana y la carne de oveja son un ejemplo de '
                             'productos:',
                 'alternativas': ['Alternativos',
                                  'Complementarios en la producción',
                                  'Sustitutos en demanda',
                                  'Inferiores',
                                  'De lujo'],
                 'correcta': 'B'},
                {'pregunta': 'Si sube el precio del petróleo, la producción '
                             'de kerosene tiende a:',
                 'alternativas': ['Disminuir',
                                  'Aumentar',
                                  'Desaparecer',
                                  'Mantenerse igual siempre',
                                  'Volverse negativa'],
                 'correcta': 'B'},
                {'pregunta': 'La expectativa de los ofertantes respecto a '
                             'los precios futuros se llama:',
                 'alternativas': ['Precio actual',
                                  'Precios esperados del bien',
                                  'Costo de producción',
                                  'Elasticidad',
                                  'Demanda derivada'],
                 'correcta': 'B'},
                {'pregunta': 'Si los ofertantes esperan una caída del precio '
                             'futuro, tienden a:',
                 'alternativas': ['Reducir la producción actual',
                                  'Incrementar la producción actual',
                                  'Detener toda producción',
                                  'Aumentar precios actuales sin producir '
                                  'más',
                                  'Cerrar el negocio'],
                 'correcta': 'B'},
                {'pregunta': 'Las sequías e inundaciones son ejemplos del '
                             'factor:',
                 'alternativas': ['Precio del bien',
                                  'Condiciones climáticas',
                                  'Costos de producción',
                                  'Precios esperados',
                                  'Políticas económicas'],
                 'correcta': 'B'},
                {'pregunta': 'Las condiciones climáticas adversas, como '
                             'sequías, provocan que la oferta:',
                 'alternativas': ['Aumente',
                                  'Se reduzca',
                                  'Se mantenga constante siempre',
                                  'Desaparezca por completo',
                                  'Se duplique'],
                 'correcta': 'B'},
                {'pregunta': 'Las políticas económicas liberales, al reducir '
                             'impuestos a bienes importados, generan:',
                 'alternativas': ['Disminución de la oferta',
                                  'Aumento de la oferta por mayores '
                                  'importaciones',
                                  'Ningún cambio en la oferta',
                                  'Reducción de las importaciones',
                                  'Aumento de aranceles'],
                 'correcta': 'B'},
                {'pregunta': 'Las políticas proteccionistas, al elevar '
                             'aranceles, tienden a:',
                 'alternativas': ['Aumentar la oferta de importados',
                                  'Reducir la oferta de bienes importados',
                                  'No afectar la oferta',
                                  'Eliminar toda importación totalmente',
                                  'Bajar los precios internos siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los factores que afectan la oferta se '
                             'consideran también las expectativas de:',
                 'alternativas': ['Los consumidores exclusivamente',
                                  'Los empresarios',
                                  'El gobierno exclusivamente',
                                  'Los bancos centrales',
                                  'Los organismos internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'En una carpintería, la producción de mesas, '
                             'camas y sillas ejemplifica productos:',
                 'alternativas': ['Complementarios',
                                  'Alternativos en la producción',
                                  'Sustitutos en demanda',
                                  'Inferiores',
                                  'De lujo'],
                 'correcta': 'B'},
                {'pregunta': 'El precio de un bien va acompañado del margen '
                             'de:',
                 'alternativas': ['Pérdida',
                                  'Ganancia del productor',
                                  'Descuento fijo',
                                  'Impuesto único',
                                  'Subsidio estatal'],
                 'correcta': 'B'},
                {'pregunta': 'La oferta expresa, en esencia, los deseos de '
                             'venta o producción en función de:',
                 'alternativas': ['Los gustos del consumidor',
                                  'Los distintos precios existentes en el '
                                  'mercado',
                                  'La publicidad exclusivamente',
                                  'El clima únicamente',
                                  'La moda del momento'],
                 'correcta': 'B'},
                {'pregunta': 'El equilibrio del mercado se define como la '
                             'situación en que el nivel de oferta coincide '
                             'con el nivel de:',
                 'alternativas': ['Producción industrial',
                                  'Consumo o demanda',
                                  'Importaciones',
                                  'Exportaciones',
                                  'Inversión pública'],
                 'correcta': 'B'},
                {'pregunta': 'En el equilibrio de mercado, la cantidad '
                             'ofertada es:',
                 'alternativas': ['Mayor que la demandada siempre',
                                  'Igual a la cantidad demandada',
                                  'Menor que la demandada siempre',
                                  'Independiente de la demanda',
                                  'Cero'],
                 'correcta': 'B'},
                {'pregunta': 'La cantidad en que coinciden las decisiones de '
                             'ofertantes y demandantes se llama:',
                 'alternativas': ['Cantidad óptima',
                                  'Cantidad de equilibrio',
                                  'Cantidad máxima',
                                  'Cantidad mínima',
                                  'Cantidad neta'],
                 'correcta': 'B'},
                {'pregunta': 'El precio en el cual la cantidad ofertada es '
                             'igual a la cantidad demandada se llama:',
                 'alternativas': ['Precio de mercado libre',
                                  'Precio de equilibrio',
                                  'Precio máximo',
                                  'Precio mínimo',
                                  'Precio sombra'],
                 'correcta': 'B'},
                {'pregunta': 'Gráficamente, el equilibrio del mercado se '
                             'forma en:',
                 'alternativas': ['El origen de coordenadas',
                                  'La intersección de las curvas de oferta y '
                                  'demanda',
                                  'El punto más alto de la curva de oferta',
                                  'El punto más bajo de la curva de demanda',
                                  'Un punto fuera del gráfico'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el precio está por debajo del '
                             'equilibrio, se genera una situación de:',
                 'alternativas': ['Abundancia',
                                  'Escasez',
                                  'Equilibrio perfecto',
                                  'Sobreproducción',
                                  'Estabilidad total'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando hay escasez en el mercado, la presión '
                             'sobre el precio es:',
                 'alternativas': ['A la baja',
                                  'Al alza',
                                  'Nula',
                                  'Indeterminada',
                                  'Negativa'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el precio está por encima del '
                             'equilibrio, se genera una situación de:',
                 'alternativas': ['Escasez',
                                  'Abundancia o sobreproducción',
                                  'Equilibrio estable',
                                  'Déficit',
                                  'Inflación directa'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando hay abundancia en el mercado, la '
                             'presión sobre el precio es:',
                 'alternativas': ['Al alza',
                                  'A la baja',
                                  'Nula',
                                  'Estable siempre',
                                  'Indefinida'],
                 'correcta': 'B'},
                {'pregunta': 'En el punto de equilibrio, se vende todo lo '
                             'que se ofrece y se puede comprar:',
                 'alternativas': ['Solo una parte de lo demandado',
                                  'Todo lo que se desea demandar',
                                  'Nada en absoluto',
                                  'El doble de lo ofertado',
                                  'Solo productos de lujo'],
                 'correcta': 'B'}]},
 {'num': 11,
  'titulo': 'Mercado',
  'secciones': [{'titulo': '11.1 CONCEPTO Y COMPONENTES',
                 'items': ['El mercado es el espacio donde interactúan las '
                           'unidades económicas en las transacciones de '
                           'compra y {venta}, generando oferta y demanda.',
                           'Los componentes de la estructura de mercado son '
                           'la {oferta}, la demanda, el {precio}, y el nivel '
                           'de {equilibrio}.',
                           'Para bienes se le llama {precio}; para servicios '
                           'se le llama {tarifa}.']},
                {'titulo': '11.2 CARACTERÍSTICAS DEL MERCADO',
                 'items': ['El mercado no requiere necesariamente la '
                           'presencia {física} de compradores y vendedores.',
                           'Todo mercado obedece al comportamiento de las '
                           'leyes económicas de la oferta y la {demanda}.',
                           'Toda transacción económica en un mercado insume '
                           'un determinado periodo de {tiempo}.']},
                {'titulo': '11.3 CLASIFICACIÓN SEGÚN EL ÁREA GEOGRÁFICA',
                 'items': ['Los mercados {locales} abarcan un espacio '
                           'restringido, como una ciudad o provincia.',
                           'Los mercados {regionales internos} abarcan una o '
                           'más regiones dentro de un mismo país.',
                           'Los mercados {regionales externos} abarcan más '
                           'de dos países mediante acuerdos, como el '
                           '{MERCOSUR}.',
                           'Los mercados {nacionales} abarcan todo el '
                           'espacio geográfico de un país.',
                           'Los mercados {internacionales} involucran a '
                           'varios países, sujetos a la {OMC}.']},
                {'titulo': '11.4 CLASIFICACIÓN SEGÚN EL NÚMERO DE VENDEDORES',
                 'items': ['El mercado de competencia {perfecta} se '
                           'caracteriza por libre ingreso y salida, sin '
                           'poder de fijación de {precios}.',
                           'El mercado de competencia {imperfecta} tiene '
                           'barreras de ingreso y salida, con poder para '
                           'fijar {precios}.',
                           'La competencia imperfecta va desde el '
                           '{monopolio} puro hasta el oligopolio y la '
                           'competencia monopolística.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El mercado se define como el espacio donde '
                           'interactúan las unidades económicas en '
                           'transacciones de {Compra y venta}.',
                           'Los componentes de la estructura de mercado son '
                           'oferta, demanda, precio y {El nivel de '
                           'equilibrio}.',
                           'Para los servicios, el precio se denomina '
                           '{Tarifa}.',
                           'Para que se constituya un mercado, la presencia '
                           'física de compradores y vendedores es {No '
                           'necesariamente obligatoria}.',
                           'Todo mercado obedece al comportamiento de las '
                           'leyes económicas de {La oferta y la demanda}.',
                           'Los mercados cuyo ámbito es una ciudad, distrito '
                           'o provincia se llaman mercados {Locales}.',
                           'Los mercados que abarcan varias regiones dentro '
                           'de un mismo país se llaman mercados {Regionales '
                           'internos}.',
                           'Los mercados que abarcan más de dos países '
                           'mediante acuerdos comerciales se llaman mercados '
                           '{Regionales externos}.',
                           'El MERCOSUR y la Unión Europea son ejemplos de '
                           'mercados {Regionales externos}.',
                           'Los mercados internacionales suelen estar '
                           'sujetos a los acuerdos de {La Organización '
                           'Mundial de Comercio (OMC)}.',
                           'El mercado que abarca todo el espacio geográfico '
                           'de un país se llama mercado {Nacional}.',
                           'El mercado caracterizado por libre ingreso y '
                           'salida de vendedores, sin poder de fijación de '
                           'precios, es de {Competencia perfecta}.',
                           'El mercado caracterizado por barreras de ingreso '
                           'y poder para fijar precios es de {Competencia '
                           'imperfecta}.',
                           'La competencia imperfecta comprende, entre otras '
                           'formas, al monopolio, al oligopolio y a la '
                           'competencia {Monopolística}.',
                           'En un mercado de competencia imperfecta con '
                           'monopolio, quien fija el precio es {El '
                           'monopolista}.',
                           'En el mercado de trabajo, el precio del factor '
                           'trabajo se fija como {Sueldo o salario}.',
                           'En el mercado de capitales, el precio del factor '
                           'capital se fija como {Tasa de interés}.',
                           'Los mercados donde se transan grandes volúmenes '
                           'de bienes en poco tiempo, con precios más bajos, '
                           'se llaman mercados {Mayoristas}.',
                           'Toda transacción económica realizada en un '
                           'mercado insume {Un determinado periodo de '
                           'tiempo}.',
                           'El mercado, según la ciencia económica, '
                           'determina y fija {Los precios}.']}],
  'cuadros': [{'titulo': '11.3 CLASIFICACIÓN DE MERCADOS SEGÚN EL ÁREA '
                         'GEOGRÁFICA',
               'encabezados': ['Tipo', 'Alcance'],
               'filas': [['{Local}', 'Una ciudad o {provincia}'],
                         ['{Regional interno}',
                          'Varias regiones de un {país}'],
                         ['{Nacional}', 'Todo el {país}'],
                         ['{Internacional}', 'Varios {países}']]}],
  'preguntas': [{'pregunta': 'El mercado se define como el espacio donde '
                             'interactúan las unidades económicas en '
                             'transacciones de:',
                 'alternativas': ['Producción exclusiva',
                                  'Compra y venta',
                                  'Ahorro únicamente',
                                  'Tributación',
                                  'Emisión monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'Los componentes de la estructura de mercado '
                             'son oferta, demanda, precio y:',
                 'alternativas': ['Inflación',
                                  'El nivel de equilibrio',
                                  'El tipo de cambio',
                                  'El PBI',
                                  'La tasa de interés'],
                 'correcta': 'B'},
                {'pregunta': 'Para los servicios, el precio se denomina:',
                 'alternativas': ['Costo',
                                  'Tarifa',
                                  'Salario',
                                  'Interés',
                                  'Dividendo'],
                 'correcta': 'B'},
                {'pregunta': 'Para que se constituya un mercado, la '
                             'presencia física de compradores y vendedores '
                             'es:',
                 'alternativas': ['Siempre obligatoria',
                                  'No necesariamente obligatoria',
                                  'Imposible sin ella',
                                  'Exigida por ley',
                                  'Requisito único'],
                 'correcta': 'B'},
                {'pregunta': 'Todo mercado obedece al comportamiento de las '
                             'leyes económicas de:',
                 'alternativas': ['La inflación exclusivamente',
                                  'La oferta y la demanda',
                                  'El tipo de cambio',
                                  'El PBI',
                                  'La tasa de interés'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercados cuyo ámbito es una ciudad, '
                             'distrito o provincia se llaman mercados:',
                 'alternativas': ['Nacionales',
                                  'Locales',
                                  'Internacionales',
                                  'Regionales externos',
                                  'Mayoristas'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercados que abarcan varias regiones '
                             'dentro de un mismo país se llaman mercados:',
                 'alternativas': ['Locales',
                                  'Regionales internos',
                                  'Internacionales',
                                  'Regionales externos',
                                  'Nacionales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercados que abarcan más de dos países '
                             'mediante acuerdos comerciales se llaman '
                             'mercados:',
                 'alternativas': ['Locales',
                                  'Regionales externos',
                                  'Nacionales',
                                  'Regionales internos',
                                  'De insumos'],
                 'correcta': 'B'},
                {'pregunta': 'El MERCOSUR y la Unión Europea son ejemplos de '
                             'mercados:',
                 'alternativas': ['Locales',
                                  'Regionales externos',
                                  'Nacionales',
                                  'Regionales internos',
                                  'De capitales'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercados internacionales suelen estar '
                             'sujetos a los acuerdos de:',
                 'alternativas': ['Solo un país',
                                  'La Organización Mundial de Comercio (OMC)',
                                  'Solo bancos privados',
                                  'Ningún organismo',
                                  'Solo gobiernos locales'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado que abarca todo el espacio '
                             'geográfico de un país se llama mercado:',
                 'alternativas': ['Local',
                                  'Nacional',
                                  'Regional interno',
                                  'Internacional',
                                  'Mayorista exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado caracterizado por libre ingreso y '
                             'salida de vendedores, sin poder de fijación de '
                             'precios, es de:',
                 'alternativas': ['Competencia imperfecta',
                                  'Competencia perfecta',
                                  'Monopolio puro',
                                  'Oligopolio',
                                  'Monopsonio'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado caracterizado por barreras de '
                             'ingreso y poder para fijar precios es de:',
                 'alternativas': ['Competencia perfecta',
                                  'Competencia imperfecta',
                                  'Libre concurrencia total',
                                  'Mercado local exclusivo',
                                  'Ninguno de los anteriores'],
                 'correcta': 'B'},
                {'pregunta': 'La competencia imperfecta comprende, entre '
                             'otras formas, al monopolio, al oligopolio y a '
                             'la competencia:',
                 'alternativas': ['Perfecta',
                                  'Monopolística',
                                  'Local',
                                  'Interna exclusiva',
                                  'Regional'],
                 'correcta': 'B'},
                {'pregunta': 'En un mercado de competencia imperfecta con '
                             'monopolio, quien fija el precio es:',
                 'alternativas': ['El consumidor',
                                  'El monopolista',
                                  'El Estado siempre',
                                  'El mercado internacional',
                                  'Un organismo neutral'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado de trabajo, el precio del factor '
                             'trabajo se fija como:',
                 'alternativas': ['Interés',
                                  'Sueldo o salario',
                                  'Renta',
                                  'Dividendo',
                                  'Tarifa'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado de capitales, el precio del '
                             'factor capital se fija como:',
                 'alternativas': ['Salario',
                                  'Tasa de interés',
                                  'Renta agrícola',
                                  'Tarifa de servicio',
                                  'Impuesto'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercados donde se transan grandes '
                             'volúmenes de bienes en poco tiempo, con '
                             'precios más bajos, se llaman mercados:',
                 'alternativas': ['Minoristas',
                                  'Mayoristas',
                                  'Locales exclusivos',
                                  'De capitales',
                                  'De insumos'],
                 'correcta': 'B'},
                {'pregunta': 'Toda transacción económica realizada en un '
                             'mercado insume:',
                 'alternativas': ['Ningún tiempo',
                                  'Un determinado periodo de tiempo',
                                  'Solo un instante siempre',
                                  'Tiempo infinito',
                                  'Un periodo fijo de un año'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado, según la ciencia económica, '
                             'determina y fija:',
                 'alternativas': ['Solo los salarios',
                                  'Los precios',
                                  'Solo los impuestos',
                                  'Solo el tipo de cambio',
                                  'Solo la inflación'],
                 'correcta': 'B'}]},
 {'num': 12,
  'titulo': 'Dinero e Inflación',
  'secciones': [{'titulo': '12.1 FUNCIONES DEL DINERO',
                 'items': ['La función de {medio de pago} o de cambio es la '
                           'más importante del dinero, y facilita las '
                           'transacciones {comerciales}.',
                           'La función de {unidad de cuenta} o medida de '
                           'valor permite estimar el valor de los demás '
                           'bienes; en el Perú es el {nuevo sol}.',
                           'La función de {depósito de valor} permite '
                           'conservar poder adquisitivo para necesidades '
                           'futuras, generando el {ahorro}.',
                           'La función de {patrón de pagos diferidos} '
                           'permite realizar pagos a futuro, como en las '
                           'compras al {crédito}.']},
                {'titulo': '12.2 CARACTERÍSTICAS DEL DINERO',
                 'items': ['El {poder adquisitivo} es la capacidad de compra '
                           'que tiene el dinero.',
                           'La {estabilidad} implica que el dinero mantenga '
                           'su poder adquisitivo en el tiempo; la '
                           '{inflación} le hace perder estabilidad.',
                           'La {divisibilidad} exige que la unidad monetaria '
                           'tenga múltiplos y {submúltiplos}.',
                           'La {homogeneidad} exige que billetes de igual '
                           'denominación tengan las mismas características, '
                           'para evitar la {falsificación}.',
                           'La {durabilidad} exige que el dinero esté hecho '
                           'de material {resistente}.',
                           'La {elasticidad} es la facilidad de la autoridad '
                           'monetaria, el {BCR}, para aumentar o disminuir '
                           'la cantidad de dinero.']},
                {'titulo': '12.3 VALORES DEL DINERO',
                 'items': ['El valor {intrínseco} es el valor que tiene el '
                           'dinero por sí mismo, y se subdivide en valor '
                           '{real} y valor nominal.',
                           'El valor {real} viene dado por el costo de '
                           '{fabricación} del dinero.',
                           'El valor {nominal} o legal es el establecido por '
                           'la autoridad monetaria e impreso en la moneda.',
                           'El valor {extrínseco} es el valor de cambio del '
                           'dinero, su capacidad de {compra} en el '
                           'mercado.']},
                {'titulo': '12.4 CLASES DE DINERO',
                 'items': ['Según su naturaleza, el dinero puede ser '
                           '{metálico} o de papel.',
                           'El dinero metálico {tipo} se acuña con metales '
                           'finos como el oro y tiene poder cancelatorio '
                           '{ilimitado}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La función más importante del dinero, que '
                           'facilita las transacciones comerciales, es '
                           '{Medio de pago o de cambio}.',
                           'La función del dinero que permite estimar el '
                           'valor de los demás bienes se llama {Unidad de '
                           'cuenta o medida de valor}.',
                           'En el Perú, la unidad de cuenta es {El nuevo '
                           'sol}.',
                           'La función del dinero que permite conservar '
                           'poder adquisitivo para el futuro se llama '
                           '{Depósito de valor}.',
                           'La función que permite realizar pagos a futuro, '
                           'como compras al crédito, se llama {Patrón de '
                           'pagos diferidos}.',
                           'La capacidad de compra que tiene el dinero se '
                           'llama {Poder adquisitivo}.',
                           'Que el dinero mantenga su poder adquisitivo en '
                           'el tiempo corresponde a la característica de '
                           '{Estabilidad}.',
                           'La inflación hace que el dinero pierda '
                           '{Estabilidad}.',
                           'Que la unidad monetaria tenga múltiplos y '
                           'submúltiplos corresponde a la característica de '
                           '{Divisibilidad}.',
                           'Que los billetes de igual denominación tengan '
                           'las mismas características corresponde a la '
                           'característica de {Homogeneidad}.',
                           'Que el dinero esté hecho de material resistente '
                           'corresponde a la característica de '
                           '{Durabilidad}.',
                           'La facilidad de la autoridad monetaria para '
                           'aumentar o disminuir la cantidad de dinero se '
                           'llama {Elasticidad}.',
                           'La autoridad monetaria del Perú, encargada de la '
                           'elasticidad del dinero, es {El Banco Central de '
                           'Reserva (BCR)}.',
                           'El valor que tiene el dinero por sí mismo se '
                           'llama valor {Intrínseco}.',
                           'El valor intrínseco se subdivide en valor real y '
                           'valor {Nominal o legal}.',
                           'El valor real del dinero viene dado por {El '
                           'costo de fabricación del dinero}.',
                           'El valor establecido por la autoridad monetaria '
                           'e impreso en la moneda se llama valor {Nominal o '
                           'legal}.',
                           'El valor de cambio del dinero, expresado en su '
                           'capacidad de compra en el mercado, se llama '
                           'valor {Extrínseco}.',
                           'Según su naturaleza, el dinero puede ser '
                           'metálico o {De papel}.',
                           'El dinero metálico tipo, acuñado con oro o '
                           'plata, tiene un poder cancelatorio '
                           '{Ilimitado}.']},
                {'titulo': '12.5 LA INFLACIÓN: CONCEPTO Y MEDICIÓN',
                 'items': ['La {inflación} es un incremento generalizado y '
                           'continuo de precios, equivalente a la '
                           '{desvalorización} de la moneda.',
                           'Una caída generalizada y continua de precios se '
                           'llama {deflación}.',
                           'La inflación se mide por la variación del '
                           '{Índice de Precios al Consumidor} (IPC).',
                           'El {IPC} mide el nivel de variación mensual de '
                           'los precios de la {canasta familiar}.',
                           'La {tasa de inflación} es el cambio porcentual '
                           'del nivel de precios en un periodo, generalmente '
                           'un {mes}.']},
                {'titulo': '12.6 CLASES DE INFLACIÓN',
                 'items': ['La inflación {moderada} tiene precios que suben '
                           'entre {0}% y 10% anual, con tasa de un dígito.',
                           'La inflación {galopante} varía entre 10% y '
                           '{1000}% anual, con tasa de dos o tres dígitos.',
                           'La {hiperinflación} supera el {1000}% anual, o '
                           'el 50% mensual, con tasa mayor a cuatro '
                           'dígitos.']},
                {'titulo': '12.7 CONSECUENCIAS DE LA INFLACIÓN',
                 'items': ['Entre las consecuencias de la inflación están la '
                           'pérdida del {poder adquisitivo}, la disminución '
                           'del salario {real}, y la {dolarización} de la '
                           'economía.',
                           'La inflación también genera {especulación} y '
                           'acaparamiento, disminución del {ahorro}, y '
                           'empobrecimiento de los {trabajadores}.']}],
  'cuadros': [{'titulo': '12.1 LAS CUATRO FUNCIONES DEL DINERO',
               'encabezados': ['Función', 'Utilidad'],
               'filas': [['{Medio de pago}', 'Facilita {transacciones}'],
                         ['{Unidad de cuenta}',
                          'Mide el {valor} de los bienes'],
                         ['{Depósito de valor}', 'Genera {ahorro}'],
                         ['Patrón de {pagos diferidos}',
                          'Permite el {crédito}']]}],
  'preguntas': [{'pregunta': 'La función más importante del dinero, que '
                             'facilita las transacciones comerciales, es:',
                 'alternativas': ['Depósito de valor',
                                  'Medio de pago o de cambio',
                                  'Patrón de pagos diferidos',
                                  'Unidad de cuenta',
                                  'Ninguna en particular'],
                 'correcta': 'B'},
                {'pregunta': 'La función del dinero que permite estimar el '
                             'valor de los demás bienes se llama:',
                 'alternativas': ['Medio de pago',
                                  'Unidad de cuenta o medida de valor',
                                  'Depósito de valor',
                                  'Patrón de pagos diferidos',
                                  'Reserva internacional'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, la unidad de cuenta es:',
                 'alternativas': ['El dólar',
                                  'El nuevo sol',
                                  'El euro',
                                  'El peso',
                                  'La libra'],
                 'correcta': 'B'},
                {'pregunta': 'La función del dinero que permite conservar '
                             'poder adquisitivo para el futuro se llama:',
                 'alternativas': ['Medio de pago',
                                  'Depósito de valor',
                                  'Unidad de cuenta',
                                  'Patrón de pagos diferidos',
                                  'Ninguna'],
                 'correcta': 'B'},
                {'pregunta': 'La función que permite realizar pagos a '
                             'futuro, como compras al crédito, se llama:',
                 'alternativas': ['Medio de pago',
                                  'Patrón de pagos diferidos',
                                  'Unidad de cuenta',
                                  'Depósito de valor',
                                  'Reserva de emergencia'],
                 'correcta': 'B'},
                {'pregunta': 'La capacidad de compra que tiene el dinero se '
                             'llama:',
                 'alternativas': ['Estabilidad',
                                  'Poder adquisitivo',
                                  'Divisibilidad',
                                  'Homogeneidad',
                                  'Elasticidad'],
                 'correcta': 'B'},
                {'pregunta': 'Que el dinero mantenga su poder adquisitivo en '
                             'el tiempo corresponde a la característica de:',
                 'alternativas': ['Poder adquisitivo',
                                  'Estabilidad',
                                  'Divisibilidad',
                                  'Durabilidad',
                                  'Elasticidad'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación hace que el dinero pierda:',
                 'alternativas': ['Divisibilidad',
                                  'Estabilidad',
                                  'Homogeneidad',
                                  'Durabilidad',
                                  'Elasticidad'],
                 'correcta': 'B'},
                {'pregunta': 'Que la unidad monetaria tenga múltiplos y '
                             'submúltiplos corresponde a la característica '
                             'de:',
                 'alternativas': ['Homogeneidad',
                                  'Divisibilidad',
                                  'Durabilidad',
                                  'Elasticidad',
                                  'Poder adquisitivo'],
                 'correcta': 'B'},
                {'pregunta': 'Que los billetes de igual denominación tengan '
                             'las mismas características corresponde a la '
                             'característica de:',
                 'alternativas': ['Divisibilidad',
                                  'Homogeneidad',
                                  'Durabilidad',
                                  'Elasticidad',
                                  'Estabilidad'],
                 'correcta': 'B'},
                {'pregunta': 'Que el dinero esté hecho de material '
                             'resistente corresponde a la característica de:',
                 'alternativas': ['Homogeneidad',
                                  'Durabilidad',
                                  'Divisibilidad',
                                  'Elasticidad',
                                  'Poder adquisitivo'],
                 'correcta': 'B'},
                {'pregunta': 'La facilidad de la autoridad monetaria para '
                             'aumentar o disminuir la cantidad de dinero se '
                             'llama:',
                 'alternativas': ['Estabilidad',
                                  'Elasticidad',
                                  'Divisibilidad',
                                  'Homogeneidad',
                                  'Durabilidad'],
                 'correcta': 'B'},
                {'pregunta': 'La autoridad monetaria del Perú, encargada de '
                             'la elasticidad del dinero, es:',
                 'alternativas': ['La SUNAT',
                                  'El Banco Central de Reserva (BCR)',
                                  'El MEF',
                                  'La SBS',
                                  'El Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'El valor que tiene el dinero por sí mismo se '
                             'llama valor:',
                 'alternativas': ['Extrínseco',
                                  'Intrínseco',
                                  'De cambio exclusivo',
                                  'De mercado',
                                  'Nominal exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El valor intrínseco se subdivide en valor real '
                             'y valor:',
                 'alternativas': ['Extrínseco',
                                  'Nominal o legal',
                                  'De cambio',
                                  'De mercado',
                                  'De uso'],
                 'correcta': 'B'},
                {'pregunta': 'El valor real del dinero viene dado por:',
                 'alternativas': ['Su valor de cambio en el mercado',
                                  'El costo de fabricación del dinero',
                                  'Su capacidad de compra',
                                  'La inflación acumulada',
                                  'El tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El valor establecido por la autoridad '
                             'monetaria e impreso en la moneda se llama '
                             'valor:',
                 'alternativas': ['Real',
                                  'Nominal o legal',
                                  'Extrínseco',
                                  'De mercado',
                                  'De cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El valor de cambio del dinero, expresado en su '
                             'capacidad de compra en el mercado, se llama '
                             'valor:',
                 'alternativas': ['Intrínseco',
                                  'Extrínseco',
                                  'Real',
                                  'Nominal',
                                  'De fabricación'],
                 'correcta': 'B'},
                {'pregunta': 'Según su naturaleza, el dinero puede ser '
                             'metálico o:',
                 'alternativas': ['Digital exclusivamente',
                                  'De papel',
                                  'Solo electrónico',
                                  'Solo bancario',
                                  'Solo virtual'],
                 'correcta': 'B'},
                {'pregunta': 'El dinero metálico tipo, acuñado con oro o '
                             'plata, tiene un poder cancelatorio:',
                 'alternativas': ['Limitado',
                                  'Ilimitado',
                                  'Nulo',
                                  'Temporal exclusivo',
                                  'Solo simbólico'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación se define como un incremento '
                             'generalizado y continuo de:',
                 'alternativas': ['Salarios',
                                  'Precios',
                                  'Impuestos',
                                  'Exportaciones',
                                  'Ahorros'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación equivale a la desvalorización de:',
                 'alternativas': ['Los bienes de capital',
                                  'La moneda',
                                  'Las exportaciones',
                                  'Los salarios exclusivamente',
                                  'El PBI'],
                 'correcta': 'B'},
                {'pregunta': 'Una caída generalizada y continua de precios '
                             'se llama:',
                 'alternativas': ['Estanflación',
                                  'Deflación',
                                  'Hiperinflación',
                                  'Recesión',
                                  'Devaluación'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación se mide oficialmente por la '
                             'variación del:',
                 'alternativas': ['PBI nominal',
                                  'Índice de Precios al Consumidor (IPC)',
                                  'Tipo de cambio',
                                  'Salario mínimo',
                                  'Índice de desarrollo humano'],
                 'correcta': 'B'},
                {'pregunta': 'El IPC mide el nivel de variación mensual de '
                             'los precios de:',
                 'alternativas': ['Solo bienes de lujo',
                                  'La canasta familiar de bienes y servicios',
                                  'Solo insumos industriales',
                                  'Solo bienes importados',
                                  'Solo bienes exportados'],
                 'correcta': 'B'},
                {'pregunta': 'La tasa de inflación es el cambio porcentual '
                             'del nivel de precios, generalmente medido en:',
                 'alternativas': ['Un día',
                                  'Un mes',
                                  'Un lustro',
                                  'Una década',
                                  'Un semestre exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación moderada se presenta cuando los '
                             'precios suben en un rango de:',
                 'alternativas': ['0% a 10% anual',
                                  '10% a 1000% anual',
                                  'Más de 1000% anual',
                                  'Solo 50% mensual',
                                  'Ningún rango definido'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación con tasa porcentual de un solo '
                             'dígito se llama inflación:',
                 'alternativas': ['Galopante',
                                  'Moderada',
                                  'Hiperinflación',
                                  'Estructural',
                                  'Importada'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación galopante varía en un rango de:',
                 'alternativas': ['0% a 10% anual',
                                  '10% a 1000% anual',
                                  'Más de 5000% anual',
                                  'Solo negativo',
                                  '0% exacto'],
                 'correcta': 'B'},
                {'pregunta': 'La hiperinflación se caracteriza por superar '
                             'un incremento anual de:',
                 'alternativas': ['10%', '1000%', '100%', '50%', '5%'],
                 'correcta': 'B'},
                {'pregunta': 'La hiperinflación también puede medirse cuando '
                             'supera un incremento mensual de:',
                 'alternativas': ['5%', '50%', '10%', '1%', '500%'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las consecuencias de la inflación figura '
                             'la pérdida del poder:',
                 'alternativas': ['Legislativo',
                                  'Adquisitivo del dinero',
                                  'Judicial',
                                  'Ejecutivo',
                                  'Electoral'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación provoca que el salario real:',
                 'alternativas': ['Aumente siempre',
                                  'Disminuya',
                                  'Se mantenga igual siempre',
                                  'Desaparezca',
                                  'Se duplique'],
                 'correcta': 'B'},
                {'pregunta': 'Un fenómeno que ocurre en economías con alta '
                             'inflación es la creciente sustitución de la '
                             'moneda local por moneda extranjera, llamada:',
                 'alternativas': ['Euroización',
                                  'Dolarización',
                                  'Nacionalización monetaria',
                                  'Estatización',
                                  'Regionalización'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación provoca, entre otras '
                             'consecuencias, la disminución del:',
                 'alternativas': ['Consumo exclusivo',
                                  'Ahorro',
                                  'Gasto público',
                                  'Comercio exterior',
                                  'Tipo de cambio'],
                 'correcta': 'B'}]},
 {'num': 13,
  'titulo': 'Sistema Financiero y Crédito',
  'secciones': [{'titulo': '13.1 INTERMEDIACIÓN FINANCIERA',
                 'items': ['La {intermediación financiera} es el proceso por '
                           'el cual se trasladan recursos de los agentes '
                           '{superavitarios} hacia los agentes deficitarios.',
                           'En la intermediación {directa}, el agente '
                           'superavitario asume directamente el {riesgo} de '
                           'otorgar sus recursos al deficitario.',
                           'En la intermediación directa se negocian '
                           '{títulos valores}: bonos de renta fija y '
                           'acciones de renta {variable}.']},
                {'titulo': '13.2 MERCADOS PRIMARIO Y SECUNDARIO',
                 'items': ['El mercado {primario} es donde se colocan por '
                           'primera vez los valores emitidos, por oferta '
                           'pública o privada.',
                           'El mercado {secundario} es donde se revenden los '
                           'valores ya adquiridos, dando {liquidez} a esos '
                           'valores.',
                           'En el mercado primario intervienen los {bancos '
                           'de inversión}; en el mercado secundario, las '
                           '{sociedades agentes de bolsa}.']},
                {'titulo': '13.3 VENTAJAS DE LA INTERMEDIACIÓN DIRECTA',
                 'items': ['Los {costos} de operación son menores para ambos '
                           'agentes.',
                           'Permite al agente deficitario acceder a grandes '
                           'sumas sin necesidad de {prendar} sus activos.',
                           'Ofrece mayor {variedad} de instrumentos '
                           'financieros al agente deficitario.']},
                {'titulo': '13.4 INSTRUMENTOS Y PRINCIPALES INSTITUCIONES',
                 'items': ['Los instrumentos de renta {fija} son títulos de '
                           'deuda que generan pago fijo de intereses y '
                           'devolución del capital.',
                           'Los instrumentos de renta {variable} dan al '
                           'inversionista derecho al {patrimonio} de la '
                           'empresa emisora.',
                           'La {Superintendencia del Mercado de Valores} '
                           '(SMV) promueve y reglamenta el mercado de '
                           'valores en el Perú.',
                           'Los {bancos de inversión} asesoran a la empresa '
                           'emisora e intermedian entre esta y los '
                           'inversionistas.',
                           'La {Bolsa de Valores} es una asociación civil '
                           'sin fines de lucro que facilita la negociación '
                           'de valores mobiliarios.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La intermediación financiera es el proceso que '
                           'traslada recursos de los agentes superavitarios '
                           'hacia los agentes {Deficitarios}.',
                           'En la intermediación financiera directa, el '
                           'riesgo lo asume directamente {El agente '
                           'superavitario}.',
                           'En la intermediación directa se negocian títulos '
                           'valores como bonos y {Acciones}.',
                           'Los bonos son instrumentos de renta {Fija}.',
                           'Las acciones son instrumentos de renta '
                           '{Variable}.',
                           'El mercado donde se colocan por primera vez los '
                           'valores emitidos se llama mercado {Primario}.',
                           'El mercado donde se revenden los valores ya '
                           'adquiridos se llama mercado {Secundario}.',
                           'La existencia del mercado secundario permite dar '
                           'a los valores {Liquidez}.',
                           'En el mercado primario, el medio de contacto se '
                           'da a través de {Los bancos de inversión}.',
                           'En el mercado secundario, el medio de contacto '
                           'se da a través de {Las sociedades agentes de '
                           'bolsa}.',
                           'Una ventaja de la intermediación directa es que '
                           'los costos de operación son {Menores para ambos '
                           'agentes}.',
                           'La intermediación directa permite al agente '
                           'deficitario acceder a grandes sumas de dinero '
                           '{Por lo general sin prendar sus activos}.',
                           'Los instrumentos de renta fija generan el pago '
                           'fijo de intereses y la devolución de {El '
                           'capital}.',
                           'Los instrumentos de renta variable dan al '
                           'inversionista derecho al patrimonio de {La '
                           'empresa emisora}.',
                           'Los bonos corporativos y las letras hipotecarias '
                           'son instrumentos de renta fija de {Largo plazo}.',
                           'Los pagarés y las letras de cambio son '
                           'instrumentos de renta fija de {Corto plazo}.',
                           'La institución que promueve y reglamenta el '
                           'mercado de valores en el Perú es {La '
                           'Superintendencia del Mercado de Valores (SMV)}.',
                           'Los bancos de inversión actúan como '
                           'intermediarios entre la empresa emisora y {Los '
                           'inversionistas}.',
                           'La Bolsa de Valores es una asociación civil {Sin '
                           'fines de lucro}.',
                           'La Bolsa de Valores facilita la negociación de '
                           '{Valores mobiliarios registrados}.']}],
  'cuadros': [{'titulo': '13.2 MERCADO PRIMARIO FRENTE A SECUNDARIO',
               'encabezados': ['Mercado', 'Función'],
               'filas': [['{Primario}', 'Primera {colocación} de valores'],
                         ['{Secundario}',
                          '{Reventa} de valores, da liquidez']]}],
  'preguntas': [{'pregunta': 'La intermediación financiera es el proceso que '
                             'traslada recursos de los agentes '
                             'superavitarios hacia los agentes:',
                 'alternativas': ['Estatales',
                                  'Deficitarios',
                                  'Internacionales',
                                  'Extranjeros exclusivamente',
                                  'Bancarios exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'En la intermediación financiera directa, el '
                             'riesgo lo asume directamente:',
                 'alternativas': ['El Estado',
                                  'El agente superavitario',
                                  'Un banco comercial intermediario',
                                  'El Banco Central',
                                  'Ningún agente'],
                 'correcta': 'B'},
                {'pregunta': 'En la intermediación directa se negocian '
                             'títulos valores como bonos y:',
                 'alternativas': ['Monedas extranjeras',
                                  'Acciones',
                                  'Solo efectivo',
                                  'Solo cheques',
                                  'Solo letras de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'Los bonos son instrumentos de renta:',
                 'alternativas': ['Variable',
                                  'Fija',
                                  'Mixta obligatoria',
                                  'Nula',
                                  'Indeterminada'],
                 'correcta': 'B'},
                {'pregunta': 'Las acciones son instrumentos de renta:',
                 'alternativas': ['Fija',
                                  'Variable',
                                  'Nula',
                                  'Garantizada siempre',
                                  'Indeterminada'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado donde se colocan por primera vez '
                             'los valores emitidos se llama mercado:',
                 'alternativas': ['Secundario',
                                  'Primario',
                                  'Informal',
                                  'Cambiario',
                                  'De divisas'],
                 'correcta': 'B'},
                {'pregunta': 'El mercado donde se revenden los valores ya '
                             'adquiridos se llama mercado:',
                 'alternativas': ['Primario',
                                  'Secundario',
                                  'Informal',
                                  'De futuros exclusivo',
                                  'Cambiario'],
                 'correcta': 'B'},
                {'pregunta': 'La existencia del mercado secundario permite '
                             'dar a los valores:',
                 'alternativas': ['Menor rentabilidad',
                                  'Liquidez',
                                  'Mayor riesgo únicamente',
                                  'Menor variedad',
                                  'Ninguna ventaja'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado primario, el medio de contacto '
                             'se da a través de:',
                 'alternativas': ['Las sociedades agentes de bolsa',
                                  'Los bancos de inversión',
                                  'El BCR exclusivamente',
                                  'La SUNAT',
                                  'Las AFP'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado secundario, el medio de contacto '
                             'se da a través de:',
                 'alternativas': ['Los bancos de inversión',
                                  'Las sociedades agentes de bolsa',
                                  'El MEF',
                                  'La SUNAT',
                                  'El BCR'],
                 'correcta': 'B'},
                {'pregunta': 'Una ventaja de la intermediación directa es '
                             'que los costos de operación son:',
                 'alternativas': ['Mayores para ambos agentes',
                                  'Menores para ambos agentes',
                                  'Iguales siempre',
                                  'Inexistentes',
                                  'Solo a cargo del Estado'],
                 'correcta': 'B'},
                {'pregunta': 'La intermediación directa permite al agente '
                             'deficitario acceder a grandes sumas de dinero:',
                 'alternativas': ['Solo prendando todos sus activos',
                                  'Por lo general sin prendar sus activos',
                                  'Nunca',
                                  'Solo con aval estatal',
                                  'Solo mediante subastas'],
                 'correcta': 'B'},
                {'pregunta': 'Los instrumentos de renta fija generan el pago '
                             'fijo de intereses y la devolución de:',
                 'alternativas': ['Las acciones',
                                  'El capital',
                                  'Los dividendos',
                                  'Las utilidades variables',
                                  'El tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'Los instrumentos de renta variable dan al '
                             'inversionista derecho al patrimonio de:',
                 'alternativas': ['El Estado',
                                  'La empresa emisora',
                                  'El Banco Central',
                                  'La SUNAT',
                                  'Ningún ente en particular'],
                 'correcta': 'B'},
                {'pregunta': 'Los bonos corporativos y las letras '
                             'hipotecarias son instrumentos de renta fija '
                             'de:',
                 'alternativas': ['Corto plazo',
                                  'Largo plazo',
                                  'Plazo indefinido',
                                  'Un solo día',
                                  'Ninguna duración fija'],
                 'correcta': 'B'},
                {'pregunta': 'Los pagarés y las letras de cambio son '
                             'instrumentos de renta fija de:',
                 'alternativas': ['Largo plazo',
                                  'Corto plazo',
                                  'Plazo indeterminado',
                                  'Solo internacional',
                                  'Solo estatal'],
                 'correcta': 'B'},
                {'pregunta': 'La institución que promueve y reglamenta el '
                             'mercado de valores en el Perú es:',
                 'alternativas': ['El BCR',
                                  'La Superintendencia del Mercado de '
                                  'Valores (SMV)',
                                  'La SUNAT',
                                  'El MEF',
                                  'La SBS exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los bancos de inversión actúan como '
                             'intermediarios entre la empresa emisora y:',
                 'alternativas': ['El Estado',
                                  'Los inversionistas',
                                  'La SUNAT',
                                  'El Banco Central',
                                  'Los consumidores finales'],
                 'correcta': 'B'},
                {'pregunta': 'La Bolsa de Valores es una asociación civil:',
                 'alternativas': ['Con fines de lucro',
                                  'Sin fines de lucro',
                                  'Estatal exclusiva',
                                  'Internacional exclusiva',
                                  'Bancaria'],
                 'correcta': 'B'},
                {'pregunta': 'La Bolsa de Valores facilita la negociación '
                             'de:',
                 'alternativas': ['Solo bienes físicos',
                                  'Valores mobiliarios registrados',
                                  'Solo divisas',
                                  'Solo bienes raíces',
                                  'Solo créditos hipotecarios'],
                 'correcta': 'B'}]},
 {'num': 14,
  'titulo': 'Distribución',
  'secciones': [{'titulo': '14.1 LA DISTRIBUCIÓN DE LA RIQUEZA',
                 'items': ['La distribución de la riqueza es la forma en que '
                           'el producto total generado por un país se '
                           'reparte entre {trabajadores} y empresarios.',
                           'El modo de reparto está determinado por las '
                           '{políticas económicas} que fija el Estado.',
                           'El reparto del producto bruto entre las clases '
                           'sociales no es {equitativo}: la mayor parte se '
                           'destina a los que más {tienen}.',
                           'El {Estado} interviene en el mercado para lograr '
                           'que la redistribución de la riqueza llegue a '
                           'todos los sectores.',
                           'La intervención estatal {excesiva} puede '
                           'distorsionar el mercado y generar problemas '
                           'macroeconómicos.']},
                {'titulo': '14.2 EL CONSUMO',
                 'items': ['El consumo es la acción de utilizar o gastar un '
                           'bien o servicio para atender {necesidades} '
                           'humanas.',
                           'En economía, el consumo se considera la fase '
                           '{final} del proceso productivo.',
                           'El {consumo privado} representa las compras de '
                           'familias y empresas privadas; el {consumo '
                           'público} son las compras del Estado.',
                           'El consumo es uno de los principales medidores '
                           'del {Producto Interno Bruto} (PIB) de un país.',
                           'Para {Keynes}, el consumo es lo más importante '
                           'en una economía porque estimula la {demanda}.']},
                {'titulo': '14.3 EL AHORRO',
                 'items': ['El ahorro es la parte del ingreso personal '
                           'disponible que {no} se consume.',
                           'El ahorro implica el sacrificio del consumo '
                           '{presente} por el consumo {futuro}.',
                           'El ahorro se compone del {excedente} de dinero o '
                           'recursos devengados durante el proceso '
                           'productivo.',
                           'La primera sociedad de ahorro y préstamo surgió '
                           'en el siglo {XV}, tras las Revoluciones '
                           '{Burguesas}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La distribución de la riqueza se define como la '
                           'forma en que el producto total se reparte entre '
                           '{Trabajadores y empresarios}.',
                           'El modo en que se reparte la riqueza está '
                           'determinado por {Las políticas económicas del '
                           'Estado}.',
                           'El reparto del producto bruto entre las clases '
                           'sociales, según el texto, es {No equitativo}.',
                           'El Estado interviene en el mercado buscando que '
                           'la redistribución de la riqueza {Llegue a todos '
                           'los sectores}.',
                           'La intervención estatal excesiva en la '
                           'distribución puede {Distorsionar el mercado y '
                           'generar problemas macroeconómicos}.',
                           'El consumo se define como la acción de utilizar '
                           'o gastar un bien para atender {Necesidades '
                           'humanas}.',
                           'En economía, el consumo se considera la fase '
                           '{Final del proceso productivo}.',
                           'Las compras de productos que realizan familias y '
                           'empresas privadas constituyen el consumo '
                           '{Privado}.',
                           'Las compras que realiza el Estado constituyen el '
                           'consumo {Público}.',
                           'El consumo es uno de los principales medidores '
                           'de {El Producto Interno Bruto (PIB)}.',
                           'Para Keynes, el consumo es lo más importante en '
                           'una economía porque {Estimula la demanda}.',
                           'Keynes desarrolló la función consumo en su obra '
                           '{Teoría general del empleo, el interés y el '
                           'dinero}.',
                           'Para Marx, el consumo de las personas depende '
                           'principalmente de {El lugar que ocupan en la '
                           'sociedad (capitalista u obrero)}.',
                           'El ahorro se define como la parte del ingreso '
                           'personal disponible que {No se consume}.',
                           'El ahorro implica el sacrificio del consumo '
                           'presente por el consumo {Futuro}.',
                           'El ahorro normalmente se compone del excedente '
                           'de dinero devengado durante el proceso '
                           '{Productivo}.',
                           'La primera sociedad de ahorro y préstamo surgió '
                           'durante el siglo {XV}.',
                           'La primera sociedad de ahorro y préstamo surgió '
                           'como parte del nuevo orden traído por {Las '
                           'Revoluciones Burguesas}.',
                           'El deseo desmedido de ahorro, sacrificando '
                           'gastos necesarios, se vincula culturalmente con '
                           '{La avaricia}.',
                           'Existen bienes que se agotan al consumirse, como '
                           'los alimentos, y otros que solo se transforman, '
                           'como {Un viaje en avión}.']}],
  'cuadros': [{'titulo': '14.2 CONSUMO PRIVADO Y PÚBLICO',
               'encabezados': ['Tipo', 'Quién compra'],
               'filas': [['{Privado}', 'Familias y {empresas} privadas'],
                         ['{Público}', 'El {Estado}']]}],
  'preguntas': [{'pregunta': 'La distribución de la riqueza se define como '
                             'la forma en que el producto total se reparte '
                             'entre:',
                 'alternativas': ['Solo el Estado',
                                  'Trabajadores y empresarios',
                                  'Solo bancos',
                                  'Solo importadores',
                                  'Solo el sector externo'],
                 'correcta': 'B'},
                {'pregunta': 'El modo en que se reparte la riqueza está '
                             'determinado por:',
                 'alternativas': ['El azar',
                                  'Las políticas económicas del Estado',
                                  'Solo el clima',
                                  'Solo la religión',
                                  'Solo la geografía'],
                 'correcta': 'B'},
                {'pregunta': 'El reparto del producto bruto entre las clases '
                             'sociales, según el texto, es:',
                 'alternativas': ['Perfectamente equitativo',
                                  'No equitativo',
                                  'Igual para todos siempre',
                                  'Determinado por sorteo',
                                  'Aleatorio'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado interviene en el mercado buscando '
                             'que la redistribución de la riqueza:',
                 'alternativas': ['Beneficie solo a un sector',
                                  'Llegue a todos los sectores',
                                  'Sea eliminada por completo',
                                  'Dependa solo del mercado',
                                  'Se concentre en pocas manos'],
                 'correcta': 'B'},
                {'pregunta': 'La intervención estatal excesiva en la '
                             'distribución puede:',
                 'alternativas': ['Mejorar automáticamente el mercado',
                                  'Distorsionar el mercado y generar '
                                  'problemas macroeconómicos',
                                  'Eliminar toda desigualdad de forma '
                                  'perfecta',
                                  'No tener ningún efecto',
                                  'Aumentar la producción sin límites'],
                 'correcta': 'B'},
                {'pregunta': 'El consumo se define como la acción de '
                             'utilizar o gastar un bien para atender:',
                 'alternativas': ['Solo deseos superfluos',
                                  'Necesidades humanas',
                                  'Solo el ahorro',
                                  'Solo la inversión',
                                  'Solo el comercio exterior'],
                 'correcta': 'B'},
                {'pregunta': 'En economía, el consumo se considera la fase:',
                 'alternativas': ['Inicial del proceso productivo',
                                  'Final del proceso productivo',
                                  'Intermedia exclusivamente',
                                  'Externa al proceso productivo',
                                  'Previa a la producción'],
                 'correcta': 'B'},
                {'pregunta': 'Las compras de productos que realizan familias '
                             'y empresas privadas constituyen el consumo:',
                 'alternativas': ['Público',
                                  'Privado',
                                  'Estatal',
                                  'Externo',
                                  'Internacional'],
                 'correcta': 'B'},
                {'pregunta': 'Las compras que realiza el Estado constituyen '
                             'el consumo:',
                 'alternativas': ['Privado',
                                  'Público',
                                  'Familiar',
                                  'Empresarial exclusivo',
                                  'Externo'],
                 'correcta': 'B'},
                {'pregunta': 'El consumo es uno de los principales medidores '
                             'de:',
                 'alternativas': ['La tasa de interés',
                                  'El Producto Interno Bruto (PIB)',
                                  'El tipo de cambio',
                                  'La inflación exclusivamente',
                                  'El costo de oportunidad'],
                 'correcta': 'B'},
                {'pregunta': 'Para Keynes, el consumo es lo más importante '
                             'en una economía porque:',
                 'alternativas': ['Reduce la demanda',
                                  'Estimula la demanda',
                                  'Elimina la producción',
                                  'Aumenta la inflación siempre',
                                  'Detiene el crecimiento'],
                 'correcta': 'B'},
                {'pregunta': 'Keynes desarrolló la función consumo en su '
                             'obra:',
                 'alternativas': ['El Capital',
                                  'Teoría general del empleo, el interés y '
                                  'el dinero',
                                  'La riqueza de las naciones',
                                  'Principios de economía',
                                  'Historia del pensamiento económico'],
                 'correcta': 'B'},
                {'pregunta': 'Para Marx, el consumo de las personas depende '
                             'principalmente de:',
                 'alternativas': ['Su edad',
                                  'El lugar que ocupan en la sociedad '
                                  '(capitalista u obrero)',
                                  'Su nacionalidad',
                                  'Su religión',
                                  'Su género'],
                 'correcta': 'B'},
                {'pregunta': 'El ahorro se define como la parte del ingreso '
                             'personal disponible que:',
                 'alternativas': ['Se consume totalmente',
                                  'No se consume',
                                  'Se pierde por inflación',
                                  'Se transfiere al Estado obligatoriamente',
                                  'Desaparece con el tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'El ahorro implica el sacrificio del consumo '
                             'presente por el consumo:',
                 'alternativas': ['Pasado',
                                  'Futuro',
                                  'Ajeno',
                                  'Estatal',
                                  'Internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El ahorro normalmente se compone del excedente '
                             'de dinero devengado durante el proceso:',
                 'alternativas': ['Educativo',
                                  'Productivo',
                                  'Electoral',
                                  'Judicial',
                                  'Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'La primera sociedad de ahorro y préstamo '
                             'surgió durante el siglo:',
                 'alternativas': ['XII', 'XV', 'XVIII', 'XX', 'X'],
                 'correcta': 'B'},
                {'pregunta': 'La primera sociedad de ahorro y préstamo '
                             'surgió como parte del nuevo orden traído por:',
                 'alternativas': ['Las guerras mundiales',
                                  'Las Revoluciones Burguesas',
                                  'La Revolución Industrial exclusivamente',
                                  'El feudalismo',
                                  'La colonización americana'],
                 'correcta': 'B'},
                {'pregunta': 'El deseo desmedido de ahorro, sacrificando '
                             'gastos necesarios, se vincula culturalmente '
                             'con:',
                 'alternativas': ['La generosidad',
                                  'La avaricia',
                                  'La prudencia exclusiva',
                                  'El altruismo',
                                  'La solidaridad'],
                 'correcta': 'B'},
                {'pregunta': 'Existen bienes que se agotan al consumirse, '
                             'como los alimentos, y otros que solo se '
                             'transforman, como:',
                 'alternativas': ['Un libro de texto',
                                  'Un viaje en avión',
                                  'Una casa',
                                  'Un terreno',
                                  'Una joya'],
                 'correcta': 'B'}]},
 {'num': 15,
  'titulo': 'Sector Público y Presupuesto Nacional',
  'secciones': [{'titulo': '15.1 CONCEPTO DE SECTOR PÚBLICO',
                 'items': ['El sector público es el sector de la economía '
                           'conformado por instituciones que actúan a nombre '
                           'del {Estado}.',
                           'El sector público está representado por el '
                           'Gobierno en sus niveles {Nacional}, Regional y '
                           '{Local}.',
                           'La finalidad del sector público es buscar el '
                           '{bienestar general} de todos los ciudadanos.',
                           'El Estado cuenta con las {finanzas públicas} '
                           'como conjunto de instrumentos '
                           'técnico-económicos-sociales.']},
                {'titulo': '15.2 FUNCIONES DEL ESTADO',
                 'items': ['Las tres funciones clásicas del Estado son: '
                           '{redistribución} de la renta, estabilización de '
                           'la economía y {asignación} de recursos.',
                           'Los instrumentos del Estado para influir en la '
                           'economía son los {impuestos}, el gasto público y '
                           'las {transferencias}, y la regulación.',
                           'Según {Musgrave}, el Estado tiene además las '
                           'funciones de promoción del {crecimiento} y '
                           'regulación económica.']},
                {'titulo': '15.3 CONTABILIDAD NACIONAL Y EL PBI',
                 'items': ['La {contabilidad nacional}, o contabilidad '
                           'social, describe la medición de las actividades '
                           'económicas de un país.',
                           'El {Producto Bruto Interno} (PBI) es el valor '
                           'monetario de todos los bienes y servicios '
                           'finales producidos en un país en un periodo '
                           'determinado.',
                           'El PBI también se conoce como {Producto '
                           'Geográfico Bruto}.',
                           'El PBI se valora a {precios de mercado} vigentes '
                           'en el año de referencia.',
                           'El PBI cuantifica la producción de los '
                           '{residentes} del país, sean nacionales o '
                           'extranjeros.']},
                {'titulo': '15.4 PBI NOMINAL Y PBI REAL',
                 'items': ['El PBI {nominal} mide el valor de la producción '
                           'usando los precios del {mismo} año que se mide.',
                           'El PBI {real} mide las variaciones en la '
                           'producción física entre dos periodos, usando los '
                           'precios de un {año base}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El sector público está conformado por '
                           'instituciones que actúan a nombre de {El '
                           'Estado}.',
                           'El sector público está representado por el '
                           'Gobierno en los niveles nacional, regional y '
                           '{Local}.',
                           'La finalidad del sector público es buscar {El '
                           'bienestar general de los ciudadanos}.',
                           'El conjunto de instrumentos '
                           'técnico-económicos-sociales con que cuenta el '
                           'Estado se llama {Finanzas públicas}.',
                           'Las tres funciones clásicas del Estado son '
                           'redistribución de la renta, estabilización de la '
                           'economía y {Asignación de recursos}.',
                           'Entre los instrumentos del Estado para influir '
                           'en la economía figuran los impuestos, el gasto '
                           'público y {La regulación}.',
                           'Según Musgrave, además de las funciones '
                           'clásicas, el Estado cumple la función de '
                           'promoción del crecimiento y {La regulación '
                           'económica}.',
                           'La contabilidad nacional también se conoce como '
                           '{Contabilidad social}.',
                           'El Producto Bruto Interno (PBI) mide el valor '
                           'monetario de todos los bienes y servicios '
                           '{Finales}.',
                           'El PBI también se conoce con el nombre de '
                           '{Producto Geográfico Bruto}.',
                           'El PBI se valoriza a los precios {De mercado '
                           'vigentes en el año de referencia}.',
                           'El PBI cuantifica la producción de {Los '
                           'residentes del país, sean nacionales o '
                           'extranjeros}.',
                           'El indicador que mide el valor de la producción '
                           'usando los precios del mismo año medido se llama '
                           '{PBI nominal}.',
                           'El indicador que mide las variaciones en la '
                           'producción física entre dos periodos, usando '
                           'precios constantes, se llama {PBI real}.',
                           'Para calcular el PBI real se usan los precios de '
                           '{Un año base fijo}.',
                           'El PBI nominal se modifica año tras año debido a '
                           'variaciones en {Los precios de mercado y la '
                           'producción física}.',
                           'El dinero, en la medición del PBI, sirve '
                           'principalmente como {Unidad de cuenta para '
                           'cuantificar la producción}.',
                           'El PBI se calcula generalmente en un periodo de '
                           '{Un año}.',
                           'El Estado, para influir en la economía, puede '
                           'optar por la intervención directa u ofrecer '
                           '{Incentivos al sector privado}.',
                           'El PBI es considerado, para economías como la '
                           'peruana, el agregado macroeconómico {Más '
                           'importante}.']}],
  'cuadros': [{'titulo': '15.2 LAS TRES FUNCIONES CLÁSICAS DEL ESTADO',
               'encabezados': ['Función', 'Objetivo'],
               'filas': [['{Redistribución} de la renta',
                          'Repartir {equitativamente} la riqueza'],
                         ['{Estabilización}',
                          'Mantener el {equilibrio} económico'],
                         ['{Asignación} de recursos',
                          'Uso {eficiente} de los recursos']]}],
  'preguntas': [{'pregunta': 'El sector público está conformado por '
                             'instituciones que actúan a nombre de:',
                 'alternativas': ['Las empresas privadas',
                                  'El Estado',
                                  'Los bancos privados',
                                  'Los organismos internacionales '
                                  'exclusivamente',
                                  'Los sindicatos'],
                 'correcta': 'B'},
                {'pregunta': 'El sector público está representado por el '
                             'Gobierno en los niveles nacional, regional y:',
                 'alternativas': ['Internacional',
                                  'Local',
                                  'Continental',
                                  'Empresarial',
                                  'Sindical'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad del sector público es buscar:',
                 'alternativas': ['Solo la ganancia empresarial',
                                  'El bienestar general de los ciudadanos',
                                  'Solo el comercio exterior',
                                  'Solo la recaudación fiscal',
                                  'Solo la estabilidad monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de instrumentos '
                             'técnico-económicos-sociales con que cuenta el '
                             'Estado se llama:',
                 'alternativas': ['Comercio exterior',
                                  'Finanzas públicas',
                                  'Mercado de valores',
                                  'Sistema bancario privado',
                                  'Bolsa de valores'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres funciones clásicas del Estado son '
                             'redistribución de la renta, estabilización de '
                             'la economía y:',
                 'alternativas': ['Privatización',
                                  'Asignación de recursos',
                                  'Comercio exterior',
                                  'Emisión monetaria exclusiva',
                                  'Endeudamiento'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los instrumentos del Estado para influir '
                             'en la economía figuran los impuestos, el gasto '
                             'público y:',
                 'alternativas': ['Solo la publicidad estatal',
                                  'La regulación',
                                  'Solo el comercio informal',
                                  'Solo el crédito privado',
                                  'Solo la migración'],
                 'correcta': 'B'},
                {'pregunta': 'Según Musgrave, además de las funciones '
                             'clásicas, el Estado cumple la función de '
                             'promoción del crecimiento y:',
                 'alternativas': ['La privatización total',
                                  'La regulación económica',
                                  'La eliminación de impuestos',
                                  'El cierre de empresas públicas',
                                  'La reducción del gasto social'],
                 'correcta': 'B'},
                {'pregunta': 'La contabilidad nacional también se conoce '
                             'como:',
                 'alternativas': ['Contabilidad empresarial',
                                  'Contabilidad social',
                                  'Contabilidad bancaria',
                                  'Contabilidad fiscal exclusiva',
                                  'Contabilidad internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El Producto Bruto Interno (PBI) mide el valor '
                             'monetario de todos los bienes y servicios:',
                 'alternativas': ['Intermedios exclusivamente',
                                  'Finales',
                                  'Importados solamente',
                                  'No transados',
                                  'Informales'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI también se conoce con el nombre de:',
                 'alternativas': ['Producto Nacional Neto',
                                  'Producto Geográfico Bruto',
                                  'Ingreso Nacional Disponible',
                                  'Renta Nacional Bruta',
                                  'Balanza Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI se valoriza a los precios:',
                 'alternativas': ['Históricos fijos',
                                  'De mercado vigentes en el año de '
                                  'referencia',
                                  'Internacionales exclusivamente',
                                  'Solo del sector agrícola',
                                  'Solo mayoristas'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI cuantifica la producción de:',
                 'alternativas': ['Solo los nacionales fuera del país',
                                  'Los residentes del país, sean nacionales '
                                  'o extranjeros',
                                  'Solo las empresas estatales',
                                  'Solo el sector exportador',
                                  'Solo las multinacionales'],
                 'correcta': 'B'},
                {'pregunta': 'El indicador que mide el valor de la '
                             'producción usando los precios del mismo año '
                             'medido se llama:',
                 'alternativas': ['PBI real',
                                  'PBI nominal',
                                  'PBI per cápita',
                                  'PBI potencial',
                                  'PBI ajustado'],
                 'correcta': 'B'},
                {'pregunta': 'El indicador que mide las variaciones en la '
                             'producción física entre dos periodos, usando '
                             'precios constantes, se llama:',
                 'alternativas': ['PBI nominal',
                                  'PBI real',
                                  'PBI corriente',
                                  'PBI bruto exclusivo',
                                  'PBI ajustado por inflación '
                                  'exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Para calcular el PBI real se usan los precios '
                             'de:',
                 'alternativas': ['Cada año distinto',
                                  'Un año base fijo',
                                  'Solo el año más reciente',
                                  'Ningún año en particular',
                                  'El año siguiente'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI nominal se modifica año tras año debido '
                             'a variaciones en:',
                 'alternativas': ['Solo la población',
                                  'Los precios de mercado y la producción '
                                  'física',
                                  'Solo el clima',
                                  'Solo la moneda extranjera',
                                  'Solo el tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El dinero, en la medición del PBI, sirve '
                             'principalmente como:',
                 'alternativas': ['Medio de ahorro exclusivo',
                                  'Unidad de cuenta para cuantificar la '
                                  'producción',
                                  'Depósito de valor exclusivo',
                                  'Patrón de pagos diferidos exclusivo',
                                  'Reserva internacional'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI se calcula generalmente en un periodo '
                             'de:',
                 'alternativas': ['Una semana',
                                  'Un año',
                                  'Un mes',
                                  'Un día',
                                  'Una década'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado, para influir en la economía, puede '
                             'optar por la intervención directa u ofrecer:',
                 'alternativas': ['Ningún tipo de apoyo',
                                  'Incentivos al sector privado',
                                  'Solo sanciones',
                                  'Solo prohibiciones totales',
                                  'Solo aranceles'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI es considerado, para economías como la '
                             'peruana, el agregado macroeconómico:',
                 'alternativas': ['Menos relevante',
                                  'Más importante',
                                  'Sin ninguna utilidad',
                                  'Solo referencial',
                                  'Ajeno a otras variables'],
                 'correcta': 'B'}]},
 {'num': 16,
  'titulo': 'Sector Externo',
  'secciones': [{'titulo': '16.1 CONCEPTO DE SECTOR EXTERNO',
                 'items': ['Ningún país tiene una economía {autárquica}; '
                           'requiere bienes y servicios de otros países para '
                           'su desarrollo.',
                           'Un país recurre al comercio exterior porque no '
                           'posee suficientes {recursos naturales}, mano de '
                           'obra calificada o {tecnología}.',
                           'En el Perú, el organismo rector de la política '
                           'económica comercial externa es el {Ministerio de '
                           'Economía y Finanzas}.',
                           'El sector externo está supeditado a '
                           'instituciones supranacionales como la '
                           '{Organización Mundial de Comercio} (OMC).']},
                {'titulo': '16.2 TEORÍAS DEL COMERCIO INTERNACIONAL',
                 'items': ['Los {mercantilistas} postulaban que un país '
                           'debía exportar todo lo posible e importar solo '
                           'lo necesario, recibiendo {metales preciosos} '
                           'como pago.',
                           'La teoría de la {ventaja absoluta} fue planteada '
                           'por {Adam Smith}: un país debe especializarse en '
                           'el bien que produce con menor {costo}.',
                           'La teoría de la {ventaja comparativa} fue '
                           'planteada por {David Ricardo}, discípulo de '
                           'Smith, 37 años después.',
                           'Según la ventaja comparativa, un país debe '
                           'especializarse en lo que es relativamente más '
                           '{productivo}, según su {costo de oportunidad}.',
                           'La teoría de la {ventaja competitiva} fue '
                           'planteada por {Michael Porter} en la década de '
                           'los 80.',
                           'Según Porter, los países deben emplear '
                           '{estrategias} empresariales para competir, no '
                           'solo depender de factores naturales.']},
                {'titulo': '16.3 FORMAS DE COMERCIO INTERNACIONAL',
                 'items': ['Las {exportaciones} son la venta de bienes y '
                           'servicios nacionales al resto del mundo, y '
                           'generan ingreso de {divisas}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Ningún país tiene una economía {Autárquica}.',
                           'Un país recurre al comercio exterior, entre '
                           'otras razones, porque no posee suficiente '
                           '{Tecnología y recursos naturales}.',
                           'En el Perú, el organismo rector de la política '
                           'económica comercial externa es {El Ministerio de '
                           'Economía y Finanzas}.',
                           'El sector externo está supeditado a '
                           'instituciones supranacionales como {La '
                           'Organización Mundial de Comercio (OMC)}.',
                           'Los mercantilistas postulaban que un país debía '
                           'exportar todo lo posible e importar {Solo lo '
                           'necesario}.',
                           'Según los mercantilistas, el pago de las '
                           'exportaciones debía recibirse en {Metales '
                           'preciosos}.',
                           'La teoría de la ventaja absoluta fue planteada '
                           'por {Adam Smith}.',
                           'Según la teoría de la ventaja absoluta, un país '
                           'debe especializarse en el bien que produce con '
                           '{Menor costo}.',
                           'La teoría de la ventaja comparativa fue '
                           'planteada por {David Ricardo}.',
                           'David Ricardo formuló su teoría años después de '
                           'la teoría de Adam Smith, aproximadamente {37 '
                           'años}.',
                           'Según la teoría de la ventaja comparativa, la '
                           'ventaja procede del {Costo de oportunidad en la '
                           'producción de cada bien}.',
                           'La teoría de la ventaja competitiva fue '
                           'planteada por {David Ricardo}.',
                           'Michael Porter planteó su teoría de la ventaja '
                           'competitiva en la década de {Los 80}.',
                           'Según Porter, los países deben competir '
                           'empleando, además de factores naturales '
                           '{Estrategias empresariales y de mercado}.',
                           'Las exportaciones se definen como la venta de '
                           'bienes y servicios nacionales {Al resto del '
                           'mundo}.',
                           'Las exportaciones generan para el país '
                           'exportador ingresos de {Divisas}.',
                           'En el Perú, la institución encargada de las '
                           'leyes aduaneras y el código tributario es {La '
                           'SUNAT}.',
                           'La Cámara Internacional de París diseña los '
                           'INCOTERMS para fijar precios como {FOB y CIF}.',
                           'El BCR, en coordinación con el MEF, maneja '
                           'principalmente {El tipo de cambio}.',
                           'El comercio exterior surge, entre otras razones, '
                           'porque no todas las mercancías son libres de '
                           'comerciar y requieren {Leyes, reglamentos e '
                           'instituciones}.']}],
  'cuadros': [{'titulo': '16.2 TEORÍAS DEL COMERCIO INTERNACIONAL',
               'encabezados': ['Teoría', 'Autor'],
               'filas': [['Ventaja {absoluta}', '{Adam Smith}'],
                         ['Ventaja {comparativa}', '{David Ricardo}'],
                         ['Ventaja {competitiva}', '{Michael Porter}']]}],
  'preguntas': [{'pregunta': 'Ningún país tiene una economía:',
                 'alternativas': ['Abierta',
                                  'Autárquica',
                                  'De mercado',
                                  'Mixta',
                                  'Global'],
                 'correcta': 'B'},
                {'pregunta': 'Un país recurre al comercio exterior, entre '
                             'otras razones, porque no posee suficiente:',
                 'alternativas': ['Población',
                                  'Tecnología y recursos naturales',
                                  'Territorio',
                                  'Historia',
                                  'Cultura'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, el organismo rector de la política '
                             'económica comercial externa es:',
                 'alternativas': ['El BCR',
                                  'El Ministerio de Economía y Finanzas',
                                  'La SUNAT exclusivamente',
                                  'El Congreso',
                                  'La SBS'],
                 'correcta': 'B'},
                {'pregunta': 'El sector externo está supeditado a '
                             'instituciones supranacionales como:',
                 'alternativas': ['Solo bancos privados',
                                  'La Organización Mundial de Comercio (OMC)',
                                  'Solo gobiernos locales',
                                  'Solo universidades',
                                  'Solo ONGs'],
                 'correcta': 'B'},
                {'pregunta': 'Los mercantilistas postulaban que un país '
                             'debía exportar todo lo posible e importar:',
                 'alternativas': ['Todo lo posible también',
                                  'Solo lo necesario',
                                  'Nada en absoluto',
                                  'Solo metales preciosos',
                                  'Solo tecnología'],
                 'correcta': 'B'},
                {'pregunta': 'Según los mercantilistas, el pago de las '
                             'exportaciones debía recibirse en:',
                 'alternativas': ['Bienes de consumo',
                                  'Metales preciosos',
                                  'Servicios',
                                  'Tecnología',
                                  'Mano de obra'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la ventaja absoluta fue planteada '
                             'por:',
                 'alternativas': ['David Ricardo',
                                  'Adam Smith',
                                  'Michael Porter',
                                  'John Keynes',
                                  'Karl Marx'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría de la ventaja absoluta, un '
                             'país debe especializarse en el bien que '
                             'produce con:',
                 'alternativas': ['Mayor costo',
                                  'Menor costo',
                                  'Mayor precio de venta',
                                  'Menor calidad',
                                  'Mayor cantidad de insumos'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la ventaja comparativa fue '
                             'planteada por:',
                 'alternativas': ['Adam Smith',
                                  'David Ricardo',
                                  'Michael Porter',
                                  'Raymond Barre',
                                  'Friedrich von Wieser'],
                 'correcta': 'B'},
                {'pregunta': 'David Ricardo formuló su teoría años después '
                             'de la teoría de Adam Smith, aproximadamente:',
                 'alternativas': ['10 años',
                                  '37 años',
                                  '100 años',
                                  '5 años',
                                  '200 años'],
                 'correcta': 'B'},
                {'pregunta': 'Según la teoría de la ventaja comparativa, la '
                             'ventaja procede del:',
                 'alternativas': ['Tamaño del país',
                                  'Costo de oportunidad en la producción de '
                                  'cada bien',
                                  'Número de habitantes',
                                  'Clima favorable exclusivamente',
                                  'Idioma oficial'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la ventaja competitiva fue '
                             'planteada por:',
                 'alternativas': ['Adam Smith',
                                  'David Ricardo',
                                  'Michael Porter',
                                  'Raymond Barre',
                                  'Nassau Senior'],
                 'correcta': 'B'},
                {'pregunta': 'Michael Porter planteó su teoría de la ventaja '
                             'competitiva en la década de:',
                 'alternativas': ['Los 60',
                                  'Los 80',
                                  'Los 40',
                                  'Los 2000',
                                  'Los 20'],
                 'correcta': 'B'},
                {'pregunta': 'Según Porter, los países deben competir '
                             'empleando, además de factores naturales:',
                 'alternativas': ['Solo su ubicación geográfica',
                                  'Estrategias empresariales y de mercado',
                                  'Solo mano de obra barata',
                                  'Solo aranceles altos',
                                  'Solo subsidios estatales'],
                 'correcta': 'B'},
                {'pregunta': 'Las exportaciones se definen como la venta de '
                             'bienes y servicios nacionales:',
                 'alternativas': ['Dentro del propio país',
                                  'Al resto del mundo',
                                  'Solo a países vecinos',
                                  'Solo en moneda nacional',
                                  'Solo a empresas estatales'],
                 'correcta': 'B'},
                {'pregunta': 'Las exportaciones generan para el país '
                             'exportador ingresos de:',
                 'alternativas': ['Impuestos exclusivamente',
                                  'Divisas',
                                  'Deuda externa',
                                  'Inflación',
                                  'Aranceles'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, la institución encargada de las '
                             'leyes aduaneras y el código tributario es:',
                 'alternativas': ['El BCR',
                                  'La SUNAT',
                                  'El MEF exclusivamente',
                                  'La SBS',
                                  'El INDECOPI'],
                 'correcta': 'B'},
                {'pregunta': 'La Cámara Internacional de París diseña los '
                             'INCOTERMS para fijar precios como:',
                 'alternativas': ['Solo precios internos',
                                  'FOB y CIF',
                                  'Solo precios de exportación agrícola',
                                  'Solo aranceles',
                                  'Solo tipos de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El BCR, en coordinación con el MEF, maneja '
                             'principalmente:',
                 'alternativas': ['Los aranceles',
                                  'El tipo de cambio',
                                  'Los impuestos internos',
                                  'El presupuesto educativo',
                                  'Las tarifas municipales'],
                 'correcta': 'B'},
                {'pregunta': 'El comercio exterior surge, entre otras '
                             'razones, porque no todas las mercancías son '
                             'libres de comerciar y requieren:',
                 'alternativas': ['Ninguna regulación',
                                  'Leyes, reglamentos e instituciones',
                                  'Solo acuerdos verbales',
                                  'Solo tratados bilaterales',
                                  'Prohibición total'],
                 'correcta': 'B'}]},
 {'num': 17,
  'titulo': 'Crisis y Ciclos Económicos',
  'secciones': [{'titulo': '17.1 CONCEPTO DEL CICLO ECONÓMICO',
                 'items': ['El proceso económico no se desarrolla de manera '
                           '{lineal} y continua, sino por ciclos de '
                           'abundancia y {retroceso}.',
                           'El ciclo económico es parte {natural} de la '
                           'evolución de una economía de mercado.']},
                {'titulo': '17.2 LAS CUATRO FASES DEL CICLO ECONÓMICO',
                 'items': ['La {depresión} se caracteriza por fuerte '
                           'desempleo, incapacidad de consumo y reducción de '
                           'la {demanda}.',
                           'La {recuperación} presenta crecimiento de la '
                           'producción, incremento de empleos e {ingresos}.',
                           'El {auge} recupera todos los sectores '
                           'económicos, con optimismo hasta llegar a un '
                           'grado de {inestabilidad}.',
                           'La {recesión} inicia con la inestabilidad del '
                           'auge: se frenan las inversiones y sube el '
                           '{desempleo}.']},
                {'titulo': '17.3 CONCEPTO Y CARACTERÍSTICAS DE LA CRISIS',
                 'items': ['La crisis económica es la {alteración} o '
                           'perturbación del proceso económico durante un '
                           'periodo determinado.',
                           'La crisis puede afectar al sector {real} '
                           '(producción, consumo, inversión) o al sector '
                           '{monetario} (crédito, reservas).',
                           'La {periodicidad} de la crisis implica que se '
                           'presenta cada cierto tiempo, con cierta '
                           '{regularidad}.',
                           'En la economía peruana, las crisis se han '
                           'presentado cada {8} a 10 años.',
                           'La crisis tiene tendencia a {propagarse}: se '
                           'inicia en un sector y afecta a otros por efecto '
                           '{dominó}.',
                           'Las crisis tienen {distinta intensidad}: los '
                           'países desarrollados suelen superarlas con mayor '
                           '{rapidez}.']},
                {'titulo': '17.4 SÍNTOMAS Y CAUSAS DE LA CRISIS',
                 'items': ['El síntoma más alarmante y preciso de la crisis '
                           'es el {incremento} de los precios.',
                           'La {superproducción} o sobreproducción es la '
                           'producción excesiva de bienes sin salida en el '
                           'mercado.',
                           'La {subproducción} es la escasez de bienes y '
                           'servicios, asociada a economías de bajo '
                           '{desarrollo}.',
                           'El {subconsumo} ocurre cuando hay mucha gente '
                           'sin capacidad adquisitiva, agravando el exceso '
                           'de bienes.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El proceso económico se desarrolla, según el '
                           'texto, de manera {Cíclica, con abundancia y '
                           'retroceso}.',
                           'La fase del ciclo caracterizada por fuerte '
                           'desempleo y caída de la demanda es {La '
                           'depresión}.',
                           'La fase donde crece la producción, el empleo y '
                           'el ingreso se llama {Recuperación}.',
                           'La fase en que se recuperan todos los sectores '
                           'de la economía, con pleno empleo, se llama '
                           '{Recesión}.',
                           'La fase que inicia con la inestabilidad del '
                           'auge, frenando las inversiones, se llama '
                           '{Recesión}.',
                           'El final de la recesión, según el texto, conduce '
                           'a {La depresión}.',
                           'La crisis económica se define como la alteración '
                           'o perturbación de {El proceso económico}.',
                           'La crisis puede afectar al sector real, que '
                           'comprende producción, consumo e inversión, y al '
                           'sector {Monetario}.',
                           'La característica de la crisis que implica que '
                           'se presenta cada cierto tiempo se llama '
                           '{Periodicidad}.',
                           'En la economía peruana, las crisis se han '
                           'presentado con una periodicidad aproximada de {8 '
                           'a 10 años}.',
                           'La característica de la crisis que implica que '
                           'se inicia en un sector y afecta a otros se llama '
                           '{Tendencia a propagarse}.',
                           'El efecto por el cual una crisis se traslada de '
                           'un sector a otro se conoce como efecto {Dominó}.',
                           'La característica de la crisis según la cual '
                           'afecta más a unos países que a otros se llama '
                           '{Distinta intensidad}.',
                           'Los países desarrollados, frente a una crisis, '
                           'suelen {Superarla con mayor rapidez}.',
                           'El síntoma más alarmante y preciso de una crisis '
                           'económica es {El incremento de los precios}.',
                           'La producción excesiva de bienes sin salida en '
                           'los mercados se llama {Superproducción o '
                           'sobreproducción}.',
                           'La escasez de bienes y servicios en el mercado, '
                           'asociada a economías de bajo desarrollo, se '
                           'llama {Subproducción}.',
                           'El problema que se agrava cuando mucha gente '
                           'carece de capacidad adquisitiva se llama '
                           '{Subconsumo}.',
                           'Entre los síntomas de la crisis figura la caída '
                           'en las cotizaciones de los valores mobiliarios '
                           'en {La bolsa de valores}.',
                           'Las causas de la crisis que afectan directamente '
                           'a la actividad económica se llaman causas '
                           '{Endógenas o económicas}.']}],
  'cuadros': [{'titulo': '17.2 LAS CUATRO FASES DEL CICLO ECONÓMICO',
               'encabezados': ['Fase', 'Característica principal'],
               'filas': [['{Depresión}', 'Fuerte {desempleo}'],
                         ['{Recuperación}', 'Crece la {producción}'],
                         ['{Auge}', '{Optimismo} e inestabilidad'],
                         ['{Recesión}', 'Se frenan las {inversiones}']]}],
  'preguntas': [{'pregunta': 'El proceso económico se desarrolla, según el '
                             'texto, de manera:',
                 'alternativas': ['Lineal y continua',
                                  'Cíclica, con abundancia y retroceso',
                                  'Sin ningún patrón',
                                  'Siempre ascendente',
                                  'Siempre descendente'],
                 'correcta': 'B'},
                {'pregunta': 'La fase del ciclo caracterizada por fuerte '
                             'desempleo y caída de la demanda es:',
                 'alternativas': ['El auge',
                                  'La depresión',
                                  'La recuperación',
                                  'La recesión',
                                  'El crecimiento'],
                 'correcta': 'B'},
                {'pregunta': 'La fase donde crece la producción, el empleo y '
                             'el ingreso se llama:',
                 'alternativas': ['Depresión',
                                  'Recuperación',
                                  'Recesión',
                                  'Estancamiento',
                                  'Crisis'],
                 'correcta': 'B'},
                {'pregunta': 'La fase en que se recuperan todos los sectores '
                             'de la economía, con pleno empleo, se llama:',
                 'alternativas': ['Depresión',
                                  'Recesión',
                                  'Auge',
                                  'Subproducción',
                                  'Subconsumo'],
                 'correcta': 'B'},
                {'pregunta': 'La fase que inicia con la inestabilidad del '
                             'auge, frenando las inversiones, se llama:',
                 'alternativas': ['Recuperación',
                                  'Recesión',
                                  'Depresión total inmediata',
                                  'Auge sostenido',
                                  'Superproducción'],
                 'correcta': 'B'},
                {'pregunta': 'El final de la recesión, según el texto, '
                             'conduce a:',
                 'alternativas': ['El auge directamente',
                                  'La depresión',
                                  'La recuperación inmediata',
                                  'El crecimiento sostenido',
                                  'La estabilidad total'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis económica se define como la '
                             'alteración o perturbación de:',
                 'alternativas': ['Solo el sistema político',
                                  'El proceso económico',
                                  'Solo el sistema educativo',
                                  'Solo el clima',
                                  'Solo la demografía'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis puede afectar al sector real, que '
                             'comprende producción, consumo e inversión, y '
                             'al sector:',
                 'alternativas': ['Educativo',
                                  'Monetario',
                                  'Deportivo',
                                  'Cultural',
                                  'Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'La característica de la crisis que implica que '
                             'se presenta cada cierto tiempo se llama:',
                 'alternativas': ['Propagación',
                                  'Periodicidad',
                                  'Intensidad',
                                  'Sincronía',
                                  'Estabilidad'],
                 'correcta': 'B'},
                {'pregunta': 'En la economía peruana, las crisis se han '
                             'presentado con una periodicidad aproximada de:',
                 'alternativas': ['1 a 2 años',
                                  '8 a 10 años',
                                  '20 a 30 años',
                                  '50 años',
                                  'Cada mes'],
                 'correcta': 'B'},
                {'pregunta': 'La característica de la crisis que implica que '
                             'se inicia en un sector y afecta a otros se '
                             'llama:',
                 'alternativas': ['Periodicidad',
                                  'Tendencia a propagarse',
                                  'Intensidad uniforme',
                                  'Estabilidad',
                                  'Regularidad exacta'],
                 'correcta': 'B'},
                {'pregunta': 'El efecto por el cual una crisis se traslada '
                             'de un sector a otro se conoce como efecto:',
                 'alternativas': ['Rebote',
                                  'Dominó',
                                  'Elástico',
                                  'Multiplicador exclusivo',
                                  'Boomerang'],
                 'correcta': 'B'},
                {'pregunta': 'La característica de la crisis según la cual '
                             'afecta más a unos países que a otros se llama:',
                 'alternativas': ['Periodicidad',
                                  'Distinta intensidad',
                                  'Propagación',
                                  'Regularidad',
                                  'Uniformidad'],
                 'correcta': 'B'},
                {'pregunta': 'Los países desarrollados, frente a una crisis, '
                             'suelen:',
                 'alternativas': ['Superarla con mayor dificultad',
                                  'Superarla con mayor rapidez',
                                  'No verse afectados nunca',
                                  'Sufrir siempre más que los demás',
                                  'Ser inmunes a toda crisis'],
                 'correcta': 'B'},
                {'pregunta': 'El síntoma más alarmante y preciso de una '
                             'crisis económica es:',
                 'alternativas': ['La reducción de precios',
                                  'El incremento de los precios',
                                  'El aumento del ahorro',
                                  'La disminución del desempleo',
                                  'El crecimiento sostenido'],
                 'correcta': 'B'},
                {'pregunta': 'La producción excesiva de bienes sin salida en '
                             'los mercados se llama:',
                 'alternativas': ['Subproducción',
                                  'Superproducción o sobreproducción',
                                  'Subconsumo',
                                  'Subempleo',
                                  'Hiperinflación'],
                 'correcta': 'B'},
                {'pregunta': 'La escasez de bienes y servicios en el '
                             'mercado, asociada a economías de bajo '
                             'desarrollo, se llama:',
                 'alternativas': ['Superproducción',
                                  'Subproducción',
                                  'Subconsumo',
                                  'Sobreoferta',
                                  'Hiperinflación'],
                 'correcta': 'B'},
                {'pregunta': 'El problema que se agrava cuando mucha gente '
                             'carece de capacidad adquisitiva se llama:',
                 'alternativas': ['Superproducción',
                                  'Subconsumo',
                                  'Subproducción exclusiva',
                                  'Hiperinflación',
                                  'Deflación'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los síntomas de la crisis figura la '
                             'caída en las cotizaciones de los valores '
                             'mobiliarios en:',
                 'alternativas': ['El mercado laboral',
                                  'La bolsa de valores',
                                  'El sector agrícola',
                                  'El comercio informal',
                                  'El turismo'],
                 'correcta': 'B'},
                {'pregunta': 'Las causas de la crisis que afectan '
                             'directamente a la actividad económica se '
                             'llaman causas:',
                 'alternativas': ['Exógenas',
                                  'Endógenas o económicas',
                                  'Climáticas',
                                  'Sociales exclusivas',
                                  'Culturales'],
                 'correcta': 'B'}]},
 {'num': 18,
  'titulo': 'Desarrollo y Crecimiento Económico',
  'secciones': [{'titulo': '18.1 CONCEPTO DE DESARROLLO ECONÓMICO',
                 'items': ['El desarrollo económico es la capacidad de un '
                           'país para generar {riqueza}, reflejada en la '
                           'calidad de {vida} de sus habitantes.',
                           'El desarrollo económico se vincula tanto a la '
                           'capacidad {productiva} de una nación como al '
                           '{bienestar} de los ciudadanos.',
                           'El crecimiento económico implica un incremento '
                           'significativo de los ingresos, o {renta per '
                           'cápita}.',
                           'La fórmula más eficaz para medir el bienestar de '
                           'un pueblo es el {IDH} (Índice de Desarrollo '
                           'Humano).']},
                {'titulo': '18.2 CARACTERÍSTICAS DEL DESARROLLO ECONÓMICO',
                 'items': ['El país con desarrollo económico utiliza sus '
                           'recursos potenciales, con muy poco capital '
                           '{ocioso}.',
                           'El desarrollo económico requiere '
                           '{sostenibilidad}: un crecimiento con buenos '
                           '{fundamentos}.',
                           'El desarrollo económico requiere {conciencia '
                           'medioambiental}, sin agotar los recursos '
                           'naturales.',
                           'El desarrollo económico requiere {orden social}: '
                           'instituciones públicas confiables.']},
                {'titulo': '18.3 EL ÍNDICE DE DESARROLLO HUMANO (IDH)',
                 'items': ['El IDH fue creado por el {Programa de las '
                           'Naciones Unidas para el Desarrollo} (PNUD).',
                           'El IDH considera tres variables: {esperanza de '
                           'vida} al nacer, educación, y {PIB per cápita}.',
                           'El IDH otorga valores entre {0} y {1}, siendo 1 '
                           'la calificación más alta.']},
                {'titulo': '18.4 CRECIMIENTO ECONÓMICO',
                 'items': ['El crecimiento económico es la evolución '
                           '{positiva} de los estándares de vida, medida por '
                           'la capacidad productiva y la renta.',
                           'El indicador más utilizado para medir el '
                           'crecimiento económico son las fluctuaciones del '
                           '{PIB}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El desarrollo económico se refiere a la '
                           'capacidad de un país de generar {Riqueza}.',
                           'El desarrollo económico debe reflejarse en {La '
                           'calidad de vida de los habitantes}.',
                           'El crecimiento económico implica un incremento '
                           'significativo de {Los ingresos o renta per '
                           'cápita}.',
                           'La fórmula más eficaz para medir el bienestar de '
                           'un pueblo, según el texto, es {El IDH (Índice de '
                           'Desarrollo Humano)}.',
                           'Una característica del desarrollo económico es '
                           'que el país utiliza sus recursos potenciales con '
                           '{Muy poco capital ocioso}.',
                           'El desarrollo económico requiere que el '
                           'crecimiento sea {Sostenible, con buenos '
                           'fundamentos}.',
                           'El desarrollo económico implica una conciencia '
                           '{Medioambiental}.',
                           'El desarrollo económico requiere orden social, '
                           'es decir, instituciones públicas {Confiables que '
                           'cumplen sus funciones}.',
                           'El Índice de Desarrollo Humano (IDH) fue creado '
                           'por {El Programa de las Naciones Unidas para el '
                           'Desarrollo (PNUD)}.',
                           'El IDH considera la esperanza de vida al nacer, '
                           'la educación y {El PIB per cápita}.',
                           'La variable del IDH que analiza el promedio de '
                           'edad de las personas fallecidas se llama '
                           '{Esperanza de vida al nacer}.',
                           'La variable del IDH que recoge el nivel de '
                           'alfabetización y estudios alcanzados es '
                           '{Educación}.',
                           'La variable del IDH que evalúa el acceso a los '
                           'recursos económicos necesarios es {Educación}.',
                           'El IDH otorga valores en un rango de {0 a 1}.',
                           'En el IDH, el valor más alto de desarrollo '
                           'corresponde a {1}.',
                           'El crecimiento económico se define como la '
                           'evolución positiva de los estándares de vida '
                           'medidos por la capacidad productiva y {La '
                           'renta}.',
                           'El indicador más utilizado para medir el '
                           'crecimiento económico es {Las fluctuaciones del '
                           'PIB}.',
                           'Entre los factores determinantes del desarrollo '
                           'económico figura el acceso a {Recursos naturales '
                           'y fuentes de energía}.',
                           'Otro factor determinante del desarrollo es la '
                           'estabilidad {Política}.',
                           'Los países que han logrado el desarrollo, según '
                           'el texto, han invertido principalmente en {Sus '
                           'habitantes}.']}],
  'cuadros': [{'titulo': '18.3 LAS TRES VARIABLES DEL IDH',
               'encabezados': ['Variable', 'Qué mide'],
               'filas': [['{Esperanza de vida}',
                          'Promedio de edad al {fallecer}'],
                         ['{Educación}',
                          'Alfabetización y nivel de {estudios}'],
                         ['{PIB per cápita}',
                          'Acceso a recursos {económicos}']]}],
  'preguntas': [{'pregunta': 'El desarrollo económico se refiere a la '
                             'capacidad de un país de generar:',
                 'alternativas': ['Deuda',
                                  'Riqueza',
                                  'Inflación',
                                  'Desempleo',
                                  'Pobreza'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo económico debe reflejarse en:',
                 'alternativas': ['Solo el PBI total',
                                  'La calidad de vida de los habitantes',
                                  'Solo las exportaciones',
                                  'Solo la inversión extranjera',
                                  'Solo el tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El crecimiento económico implica un incremento '
                             'significativo de:',
                 'alternativas': ['El desempleo',
                                  'Los ingresos o renta per cápita',
                                  'La pobreza',
                                  'La inflación',
                                  'La deuda externa'],
                 'correcta': 'B'},
                {'pregunta': 'La fórmula más eficaz para medir el bienestar '
                             'de un pueblo, según el texto, es:',
                 'alternativas': ['El PBI nominal',
                                  'El IDH (Índice de Desarrollo Humano)',
                                  'La tasa de interés',
                                  'El tipo de cambio',
                                  'La balanza comercial'],
                 'correcta': 'B'},
                {'pregunta': 'Una característica del desarrollo económico es '
                             'que el país utiliza sus recursos potenciales '
                             'con:',
                 'alternativas': ['Alto capital ocioso',
                                  'Muy poco capital ocioso',
                                  'Ningún recurso disponible',
                                  'Recursos completamente agotados',
                                  'Solo recursos importados'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo económico requiere que el '
                             'crecimiento sea:',
                 'alternativas': ['Temporal y aislado',
                                  'Sostenible, con buenos fundamentos',
                                  'Solo a corto plazo',
                                  'Sin ninguna base productiva',
                                  'Dependiente exclusivamente de la '
                                  'exportación'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo económico implica una '
                             'conciencia:',
                 'alternativas': ['Solo comercial',
                                  'Medioambiental',
                                  'Solo financiera',
                                  'Solo militar',
                                  'Solo religiosa'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo económico requiere orden social, '
                             'es decir, instituciones públicas:',
                 'alternativas': ['Débiles y sin control',
                                  'Confiables que cumplen sus funciones',
                                  'Innecesarias',
                                  'Privatizadas totalmente',
                                  'Sin ninguna regulación'],
                 'correcta': 'B'},
                {'pregunta': 'El Índice de Desarrollo Humano (IDH) fue '
                             'creado por:',
                 'alternativas': ['El Banco Mundial',
                                  'El Programa de las Naciones Unidas para '
                                  'el Desarrollo (PNUD)',
                                  'El FMI',
                                  'La OMC',
                                  'La OCDE'],
                 'correcta': 'B'},
                {'pregunta': 'El IDH considera la esperanza de vida al '
                             'nacer, la educación y:',
                 'alternativas': ['El tipo de cambio',
                                  'El PIB per cápita',
                                  'La inflación',
                                  'La tasa de interés',
                                  'El desempleo'],
                 'correcta': 'B'},
                {'pregunta': 'La variable del IDH que analiza el promedio de '
                             'edad de las personas fallecidas se llama:',
                 'alternativas': ['Educación',
                                  'Esperanza de vida al nacer',
                                  'PIB per cápita',
                                  'Tasa de natalidad',
                                  'Mortalidad infantil'],
                 'correcta': 'B'},
                {'pregunta': 'La variable del IDH que recoge el nivel de '
                             'alfabetización y estudios alcanzados es:',
                 'alternativas': ['Esperanza de vida',
                                  'Educación',
                                  'PIB per cápita',
                                  'Ingreso nacional',
                                  'Empleo'],
                 'correcta': 'B'},
                {'pregunta': 'La variable del IDH que evalúa el acceso a los '
                             'recursos económicos necesarios es:',
                 'alternativas': ['Esperanza de vida',
                                  'Educación',
                                  'PIB per cápita',
                                  'Tasa de interés',
                                  'Balanza comercial'],
                 'correcta': 'B'},
                {'pregunta': 'El IDH otorga valores en un rango de:',
                 'alternativas': ['0 a 100',
                                  '0 a 1',
                                  '1 a 10',
                                  '0 a 1000',
                                  '-1 a 1'],
                 'correcta': 'B'},
                {'pregunta': 'En el IDH, el valor más alto de desarrollo '
                             'corresponde a:',
                 'alternativas': ['0', '1', '50', '100', '-1'],
                 'correcta': 'B'},
                {'pregunta': 'El crecimiento económico se define como la '
                             'evolución positiva de los estándares de vida '
                             'medidos por la capacidad productiva y:',
                 'alternativas': ['Solo la población',
                                  'La renta',
                                  'Solo el clima',
                                  'Solo la cultura',
                                  'Solo la religión'],
                 'correcta': 'B'},
                {'pregunta': 'El indicador más utilizado para medir el '
                             'crecimiento económico es:',
                 'alternativas': ['La tasa de interés',
                                  'Las fluctuaciones del PIB',
                                  'El tipo de cambio',
                                  'La inflación exclusivamente',
                                  'El desempleo exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los factores determinantes del '
                             'desarrollo económico figura el acceso a:',
                 'alternativas': ['Solo territorio extenso',
                                  'Recursos naturales y fuentes de energía',
                                  'Solo mano de obra barata',
                                  'Solo aranceles bajos',
                                  'Solo comercio informal'],
                 'correcta': 'B'},
                {'pregunta': 'Otro factor determinante del desarrollo es la '
                             'estabilidad:',
                 'alternativas': ['Climática exclusiva',
                                  'Política',
                                  'Solo religiosa',
                                  'Solo cultural',
                                  'Solo deportiva'],
                 'correcta': 'B'},
                {'pregunta': 'Los países que han logrado el desarrollo, '
                             'según el texto, han invertido principalmente '
                             'en:',
                 'alternativas': ['Solo armamento',
                                  'Sus habitantes',
                                  'Solo infraestructura vial',
                                  'Solo turismo',
                                  'Solo minería'],
                 'correcta': 'B'}]}]
