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
                {'titulo': '1.4 PRINCIPALES ESCUELAS DEL PENSAMIENTO '
                           'ECONÓMICO',
                 'items': ['{Carlos Marx} es representante de la escuela '
                           '{marxista}, que sostiene que el valor de las '
                           'mercancías proviene del trabajo.',
                           '{León Walras} es representante de la escuela '
                           '{marginalista} o neoclásica, con su teoría del '
                           'equilibrio general.',
                           '{John Maynard Keynes} es representante de la '
                           'escuela {keynesiana}, que defiende la '
                           'intervención del Estado para estimular la '
                           'demanda.']}],
  'cuadros': [{'titulo': '1.3 ECONOMÍA POSITIVA Y NORMATIVA',
               'encabezados': ['Enfoque', 'Pregunta que responde'],
               'filas': [['Economía {positiva}', '«Lo que {es}»'],
                         ['Economía {normativa}',
                          '«Lo que {debería} ser»']]}],
  'preguntas': [{'pregunta': 'Según Raymond Barre, la economía es una '
                             'ciencia dirigida a la administración de '
                             'recursos:',
                 'alternativas': ['Ilimitados',
                                  'Escasos',
                                  'Renovables exclusivamente',
                                  'Gratuitos',
                                  'Abundantes'],
                 'correcta': 'B'},
                {'pregunta': 'La economía estudia la tensión entre los '
                             'deseos ilimitados y los medios:',
                 'alternativas': ['Abundantes',
                                  'Limitados',
                                  'Renovables',
                                  'Gratuitos',
                                  'Infinitos'],
                 'correcta': 'B'},
                {'pregunta': 'El objeto de estudio de la economía tiene como '
                             'fuente principal:',
                 'alternativas': ['La escasez de recursos',
                                  'El crecimiento poblacional',
                                  'El comercio internacional',
                                  'La abundancia',
                                  'La política monetaria'],
                 'correcta': 'A'},
                {'pregunta': 'Uno de los tres problemas económicos '
                             'fundamentales es:',
                 'alternativas': ['¿Quién gobierna?',
                                  '¿Qué producir?',
                                  '¿Cómo votar?',
                                  '¿Cuándo producir?',
                                  '¿Dónde comprar?'],
                 'correcta': 'B'},
                {'pregunta': 'La economía que describe los fenómenos '
                             'económicos tal como son se llama economía:',
                 'alternativas': ['Financiera',
                                  'Positiva',
                                  'Aplicada',
                                  'Social',
                                  'Normativa'],
                 'correcta': 'B'},
                {'pregunta': 'La economía que plantea cómo deberían ser las '
                             'cosas se llama economía:',
                 'alternativas': ['Positiva',
                                  'Neutra',
                                  'Descriptiva',
                                  'Normativa',
                                  'Clásica'],
                 'correcta': 'D'},
                {'pregunta': 'El fin práctico de la economía busca el '
                             'bienestar general y una distribución:',
                 'alternativas': ['Solo para las empresas',
                                  'Nula de recursos',
                                  'Desigual de la riqueza',
                                  'Exclusiva para el Estado',
                                  'Justa de la riqueza'],
                 'correcta': 'E'},
                {'pregunta': 'El costo de oportunidad se define como el '
                             'costo de:',
                 'alternativas': ['El tiempo libre',
                                  'La alternativa a la que se renuncia al '
                                  'decidir',
                                  'Todo lo que se compra',
                                  'El dinero disponible',
                                  'La inflación anual'],
                 'correcta': 'B'},
                {'pregunta': 'El término «costo de oportunidad» fue acuñado '
                             'por:',
                 'alternativas': ['Friedrich von Wieser',
                                  'John Maynard Keynes',
                                  'Karl Marx',
                                  'Adam Smith',
                                  'David Ricardo'],
                 'correcta': 'A'},
                {'pregunta': 'El costo de oportunidad también se conoce '
                             'como:',
                 'alternativas': ['La tasa de interés',
                                  'El valor de la mejor opción no '
                                  'seleccionada',
                                  'El producto bruto interno',
                                  'El precio de mercado',
                                  'La inflación acumulada'],
                 'correcta': 'B'},
                {'pregunta': 'Toda elección económica conlleva '
                             'necesariamente:',
                 'alternativas': ['La eliminación de la escasez',
                                  'Un aumento de precios',
                                  'Una ganancia garantizada',
                                  'Una pérdida total',
                                  'Un costo de oportunidad'],
                 'correcta': 'E'},
                {'pregunta': 'La obra donde se acuñó el término costo de '
                             'oportunidad se publicó en:',
                 'alternativas': ['1914', '1776', '2000', '1890', '1950'],
                 'correcta': 'A'},
                {'pregunta': 'Si una población elige construir una escuela '
                             'en vez de una carretera, el costo de '
                             'oportunidad es:',
                 'alternativas': ['Los trabajadores empleados',
                                  'El dinero gastado en la escuela',
                                  'El tiempo de construcción',
                                  'El material usado',
                                  'La carretera que se dejó de construir'],
                 'correcta': 'E'},
                {'pregunta': 'El costo de oportunidad se aplica '
                             'principalmente en el ámbito:',
                 'alternativas': ['Financiero y económico',
                                  'Solo educativo',
                                  'Solo religioso',
                                  'Solo artístico',
                                  'Solo deportivo'],
                 'correcta': 'A'},
                {'pregunta': 'El costo de oportunidad se basa '
                             'fundamentalmente en la rentabilidad:',
                 'alternativas': ['Solo inmediata',
                                  'Solo simbólica',
                                  'Futura',
                                  'Pasada',
                                  'Inexistente'],
                 'correcta': 'C'},
                {'pregunta': 'La escasez obliga a la sociedad a determinar '
                             'qué necesidades satisfacer, lo que genera:',
                 'alternativas': ['Abundancia',
                                  'La elección',
                                  'Riqueza ilimitada',
                                  'Ausencia de problemas',
                                  'Igualdad absoluta'],
                 'correcta': 'B'},
                {'pregunta': 'Según Barre, la economía estudia el '
                             'comportamiento humano en el uso de los '
                             'recursos:',
                 'alternativas': ['De forma gratuita',
                                  'Sin ningún costo',
                                  'Sin limitaciones',
                                  'Con un costo',
                                  'De manera aleatoria'],
                 'correcta': 'D'},
                {'pregunta': 'El objeto de estudio de la economía comprende '
                             'los fenómenos, hechos y conducta:',
                 'alternativas': ['Políticos',
                                  'Religiosos',
                                  'Artísticos',
                                  'Económicos',
                                  'Deportivos'],
                 'correcta': 'D'},
                {'pregunta': 'La dicotomía necesidades-recursos se resuelve '
                             'dando prioridad a las necesidades y generando '
                             'programas:',
                 'alternativas': ['De gasto ilimitado',
                                  'De uso óptimo de los recursos',
                                  'De reducción poblacional',
                                  'De abandono de la producción',
                                  'Sin ninguna planificación'],
                 'correcta': 'A'},
                {'pregunta': 'El coste de oportunidad representa recursos '
                             'que se dejan de percibir por:',
                 'alternativas': ['No haber elegido la mejor alternativa '
                                  'posible',
                                  'Elegir siempre correctamente',
                                  'Ahorrar en exceso',
                                  'Tener recursos ilimitados',
                                  'No participar en el mercado'],
                 'correcta': 'A'},
                {'pregunta': 'El economista representante de la escuela '
                             'marxista, que sostiene que el valor de las '
                             'mercancías proviene del trabajo, es:',
                 'alternativas': ['León Walras',
                                  'Carlos Marx',
                                  'John Keynes',
                                  'Adam Smith',
                                  'David Ricardo'],
                 'correcta': 'B'},
                {'pregunta': 'El economista representante de la escuela '
                             'marginalista o neoclásica, con su teoría del '
                             'equilibrio general, es:',
                 'alternativas': ['Carlos Marx',
                                  'León Walras',
                                  'John Keynes',
                                  'Karl Menger',
                                  'Alfred Marshall'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE ECONOMÍA',
                      'items': ['Según Raymond Barre, la economía es la '
                                'ciencia social dirigida a la administración '
                                'de los escasos recursos de las sociedades '
                                'humanas.']},
                     {'titulo': 'OBJETO DE ESTUDIO Y FINES',
                      'items': ['El objeto de estudio de la economía tiene '
                                'como fuente la escasez de recursos.']},
                     {'titulo': 'ESCASEZ Y COSTO DE OPORTUNIDAD',
                      'items': ['El costo de oportunidad es el costo de la '
                                'alternativa a la que se renuncia al tomar '
                                'una decisión.']},
                     {'titulo': 'PRINCIPALES ESCUELAS DEL PENSAMIENTO '
                                'ECONÓMICO',
                      'items': ['Carlos Marx es representante de la escuela '
                                'marxista, que sostiene que el valor de las '
                                'mercancías proviene del trabajo.']}]},
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
                           'urgencia.']}],
  'cuadros': [{'titulo': '2.2 NIVELES DE LA PIRÁMIDE DE MASLOW',
               'encabezados': ['Nivel', 'Necesidad'],
               'filas': [['1', '{Fisiológicas}'],
                         ['2', '{Seguridad}'],
                         ['3', '{Sociales} o filiación'],
                         ['4', 'De {estima}'],
                         ['5', '{Autorrealización}']]}],
  'preguntas': [{'pregunta': 'Una necesidad se define como la sensación de:',
                 'alternativas': ['Riqueza excesiva',
                                  'Bienestar total',
                                  'Satisfacción plena',
                                  'Carencia o insuficiencia',
                                  'Abundancia'],
                 'correcta': 'D'},
                {'pregunta': 'Las necesidades tienen un carácter:',
                 'alternativas': ['Universal idéntico',
                                  'Absoluto e igual para todos',
                                  'Relativo',
                                  'Inexistente',
                                  'Fijo por ley'],
                 'correcta': 'C'},
                {'pregunta': 'La exigencia biológica de reponer energías es '
                             'un origen de las necesidades de tipo:',
                 'alternativas': ['Cultural exclusivo',
                                  'Social',
                                  'Biológico',
                                  'Político',
                                  'Artístico'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría de la jerarquización de las '
                             'necesidades fue planteada por:',
                 'alternativas': ['Abraham Maslow',
                                  'Adam Smith',
                                  'Karl Marx',
                                  'Hermann Gossen',
                                  'John Keynes'],
                 'correcta': 'A'},
                {'pregunta': 'Maslow planteó su teoría de las necesidades en '
                             'la década de:',
                 'alternativas': ['Los 90',
                                  'Los 60',
                                  'Los 20',
                                  'Los 80',
                                  'Los 40'],
                 'correcta': 'E'},
                {'pregunta': 'La obra donde Maslow expone su teoría se '
                             'titula:',
                 'alternativas': ['El Capital',
                                  'Principios de economía',
                                  'Teoría general del empleo',
                                  'La riqueza de las naciones',
                                  'Motivation and Personality'],
                 'correcta': 'E'},
                {'pregunta': 'El primer nivel de la pirámide de Maslow '
                             'corresponde a las necesidades:',
                 'alternativas': ['De autorrealización',
                                  'De seguridad',
                                  'De estima',
                                  'Fisiológicas',
                                  'Sociales'],
                 'correcta': 'D'},
                {'pregunta': 'Las necesidades de seguridad incluyen, por '
                             'ejemplo:',
                 'alternativas': ['La alimentación',
                                  'Un seguro médico',
                                  'El ocio',
                                  'La amistad',
                                  'El prestigio'],
                 'correcta': 'B'},
                {'pregunta': 'Las necesidades sociales también se conocen '
                             'como necesidades de:',
                 'alternativas': ['Filiación',
                                  'Subsistencia',
                                  'Autorrealización',
                                  'Estima',
                                  'Seguridad'],
                 'correcta': 'A'},
                {'pregunta': 'Las necesidades de estima se expresan en el '
                             'sentimiento de independencia y:',
                 'alternativas': ['Sed',
                                  'Prestigio y reconocimiento',
                                  'Hambre',
                                  'Frío',
                                  'Sueño'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel más alto de la pirámide de Maslow '
                             'corresponde a las necesidades de:',
                 'alternativas': ['Sociales',
                                  'Seguridad',
                                  'Estima',
                                  'Fisiológicas',
                                  'Autorrealización'],
                 'correcta': 'E'},
                {'pregunta': 'La ley que establece que el ser humano tiene '
                             'múltiples necesidades en aumento se llama ley '
                             'de:',
                 'alternativas': ['Saturación',
                                  'Escasez',
                                  'Gossen exclusivamente',
                                  'Infinidad de las necesidades',
                                  'Variación en intensidad'],
                 'correcta': 'D'},
                {'pregunta': 'La ley que indica que basta una cantidad '
                             'determinada de un bien para satisfacer una '
                             'necesidad es la ley de:',
                 'alternativas': ['Saturación o limitadas en capacidad',
                                  'Oferta',
                                  'Infinidad',
                                  'Variación en intensidad',
                                  'Demanda'],
                 'correcta': 'A'},
                {'pregunta': 'La ley de saturación también se conoce como la '
                             'ley de:',
                 'alternativas': ['Maslow',
                                  'Barre',
                                  'Gossen',
                                  'Smith',
                                  'Wieser'],
                 'correcta': 'C'},
                {'pregunta': 'Según la ley de Gossen, la satisfacción '
                             'suplementaria de un bien:',
                 'alternativas': ['Aumenta indefinidamente',
                                  'Se duplica siempre',
                                  'No tiene relación con el consumo',
                                  'Disminuye a medida que aumenta el consumo',
                                  'Se mantiene constante'],
                 'correcta': 'D'},
                {'pregunta': 'Hermann Heinrich Gossen es recordado en la '
                             'historia del pensamiento:',
                 'alternativas': ['Artístico',
                                  'Político',
                                  'Militar',
                                  'Económico',
                                  'Religioso'],
                 'correcta': 'D'},
                {'pregunta': 'La ley de la variación en intensidad indica '
                             'que las necesidades:',
                 'alternativas': ['Desaparecen con el tiempo',
                                  'No varían nunca',
                                  'Son siempre iguales',
                                  'Se satisfacen todas con la misma urgencia',
                                  'No se perciben con la misma urgencia'],
                 'correcta': 'E'},
                {'pregunta': 'El desarrollo permanente de la sociedad genera '
                             'un aumento de:',
                 'alternativas': ['La informalidad',
                                  'La escasez absoluta',
                                  'El desempleo',
                                  'Los bienes y servicios que el hombre '
                                  'precisa',
                                  'La pobreza generalizada'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre es considerado, según el texto, un '
                             'ser:',
                 'alternativas': ['Solo económico',
                                  'Puramente biológico',
                                  'Exclusivamente racional',
                                  'Solo espiritual',
                                  'Biopsicosocial'],
                 'correcta': 'E'},
                {'pregunta': 'Las necesidades deben ser aplacadas mediante '
                             'el consumo de:',
                 'alternativas': ['Solo tiempo libre',
                                  'Solo dinero',
                                  'Bienes y servicios',
                                  'Solo información',
                                  'Solo tecnología'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ORIGEN',
                      'items': ['Necesidad es la sensación de carencia o '
                                'insuficiencia, material o inmaterial, que '
                                'el hombre experimenta por sus exigencias '
                                'corporales o espirituales.']},
                     {'titulo': 'LA PIRÁMIDE DE MASLOW',
                      'items': ['La teoría de la jerarquización de las '
                                'necesidades fue planteada en la década de '
                                'los 40 por Abraham Maslow.']},
                     {'titulo': 'LEYES DE LAS NECESIDADES',
                      'items': ['La ley de la infinidad de las necesidades '
                                'establece que el ser humano tiene múltiples '
                                'necesidades en permanente incremento.']}]},
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
                 'alternativas': ['Insumos exclusivos',
                                  'Servicios',
                                  'Factores productivos',
                                  'Recursos naturales',
                                  'Satisfactores'],
                 'correcta': 'E'},
                {'pregunta': 'Un recurso económico se define como aquel '
                             'susceptible de ser transformado en:',
                 'alternativas': ['Dinero exclusivamente',
                                  'Deuda pública',
                                  'Inflación',
                                  'Bienes y riqueza',
                                  'Impuestos'],
                 'correcta': 'D'},
                {'pregunta': 'Los bienes no económicos o libres se '
                             'caracterizan por ser:',
                 'alternativas': ['Transables en el mercado',
                                  'Costosos',
                                  'Producidos por el hombre',
                                  'Abundantes en la naturaleza',
                                  'Escasos'],
                 'correcta': 'D'},
                {'pregunta': 'Los bienes libres se caracterizan porque:',
                 'alternativas': ['Requieren gran esfuerzo',
                                  'No tienen relación de pertenencia',
                                  'Generan valor de cambio',
                                  'Tienen propietario',
                                  'Son transformados industrialmente'],
                 'correcta': 'B'},
                {'pregunta': 'Un ejemplo típico de bien libre es:',
                 'alternativas': ['Una vivienda',
                                  'Un automóvil',
                                  'El aire',
                                  'Una computadora',
                                  'Un libro'],
                 'correcta': 'C'},
                {'pregunta': 'Los bienes económicos requieren, para '
                             'obtenerse, la intervención de:',
                 'alternativas': ['El ser humano con su esfuerzo',
                                  'Solo el clima',
                                  'Ningún factor productivo',
                                  'Solo el azar',
                                  'La naturaleza sin más'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes económicos son escasos, lo que les '
                             'genera:',
                 'alternativas': ['Gratuidad',
                                  'Valor de uso únicamente',
                                  'Ausencia de mercado',
                                  'Abundancia',
                                  'Valor de cambio'],
                 'correcta': 'E'},
                {'pregunta': 'Por su naturaleza, los bienes que pueden ser '
                             'percibidos por los sentidos se llaman bienes:',
                 'alternativas': ['Finales',
                                  'Materiales o tangibles',
                                  'Inmateriales',
                                  'Intermedios',
                                  'Fungibles'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas, teorías y derechos de autor son '
                             'ejemplos de bienes:',
                 'alternativas': ['Inmateriales o intangibles',
                                  'Muebles',
                                  'De consumo industrial',
                                  'Fungibles',
                                  'Materiales'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes que requieren transformación previa '
                             'antes de consumirse se llaman bienes:',
                 'alternativas': ['Intermedios',
                                  'Fungibles',
                                  'Libres',
                                  'Finales',
                                  'Inmuebles'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes intermedios también se denominan '
                             'bienes:',
                 'alternativas': ['Satisfacientes',
                                  'Finales',
                                  'Muebles',
                                  'Libres',
                                  'Presatisfacientes'],
                 'correcta': 'E'},
                {'pregunta': 'Los bienes listos para el consumo directo se '
                             'llaman bienes:',
                 'alternativas': ['Presatisfacientes',
                                  'Inmuebles',
                                  'Finales o satisfacientes',
                                  'Intermedios',
                                  'Libres'],
                 'correcta': 'C'},
                {'pregunta': 'La harina para hacer fideos es un ejemplo de '
                             'bien:',
                 'alternativas': ['Intermedio',
                                  'Final',
                                  'Libre',
                                  'Fungible exclusivo',
                                  'Inmueble'],
                 'correcta': 'A'},
                {'pregunta': 'El pan, la ropa y la leche son ejemplos de '
                             'bienes:',
                 'alternativas': ['Finales',
                                  'Libres',
                                  'No económicos',
                                  'Inmuebles',
                                  'Intermedios'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes que se utilizan una sola vez y '
                             'desaparecen en su primer uso se llaman bienes:',
                 'alternativas': ['Intermedios',
                                  'Inmuebles',
                                  'Libres',
                                  'Fungibles',
                                  'Infungibles'],
                 'correcta': 'D'},
                {'pregunta': 'Los bienes que se utilizan varias veces sin '
                             'agotarse en el primer uso se llaman bienes:',
                 'alternativas': ['Libres',
                                  'Presatisfacientes',
                                  'Muebles exclusivos',
                                  'Infungibles o duraderos',
                                  'Fungibles'],
                 'correcta': 'D'},
                {'pregunta': 'Los alimentos y las materias primas son '
                             'ejemplos de bienes:',
                 'alternativas': ['Libres',
                                  'Finales exclusivos',
                                  'Fungibles',
                                  'Infungibles',
                                  'Inmuebles'],
                 'correcta': 'C'},
                {'pregunta': 'Los vestidos, zapatos y libros son ejemplos de '
                             'bienes:',
                 'alternativas': ['Fungibles',
                                  'No económicos',
                                  'Intermedios exclusivos',
                                  'Infungibles',
                                  'Libres'],
                 'correcta': 'D'},
                {'pregunta': 'El Código Civil peruano que clasifica los '
                             'bienes en muebles e inmuebles está vigente '
                             'desde:',
                 'alternativas': ['1993', '1950', '2000', '1970', '1984'],
                 'correcta': 'E'},
                {'pregunta': 'Los bienes muebles se caracterizan porque '
                             'pueden trasladarse de un lugar a otro:',
                 'alternativas': ['Con suma facilidad y sin ser destruidos',
                                  'Solo destruyéndolos',
                                  'Solo con gran dificultad',
                                  'Solo con maquinaria pesada',
                                  'Nunca'],
                 'correcta': 'A'},
                {'pregunta': 'Un bien público se caracteriza porque su '
                             'consumo es:',
                 'alternativas': ['Indivisible y compartido sin exclusión',
                                  'Solo para el Estado',
                                  'Exclusivo de quien paga',
                                  'Limitado a una sola persona',
                                  'Prohibido para particulares'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes públicos puros tienen un coste '
                             'marginal, por cada usuario adicional, que es:',
                 'alternativas': ['Muy alto',
                                  'Variable según el consumidor',
                                  'Creciente exponencialmente',
                                  'Igual al precio de mercado',
                                  'Nulo'],
                 'correcta': 'E'},
                {'pregunta': 'La defensa nacional es un ejemplo típico de '
                             'bien público:',
                 'alternativas': ['Rival',
                                  'Impuro',
                                  'Privado',
                                  'Mixto exclusivo',
                                  'Puro'],
                 'correcta': 'E'},
                {'pregunta': 'Los bienes públicos impuros, como las vías '
                             'públicas, tienen un consumo:',
                 'alternativas': ['Solo privado',
                                  'Parcialmente rival',
                                  'Inexistente',
                                  'Totalmente excluyente',
                                  'No rival en absoluto'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes públicos se caracterizan por '
                             'consumirse conjuntamente y sin:',
                 'alternativas': ['Producción estatal',
                                  'Rivalidad',
                                  'Costo alguno',
                                  'Ningún usuario',
                                  'Regulación'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se definen como actividades '
                             'económicas que satisfacen directamente '
                             'necesidades de:',
                 'alternativas': ['Otras personas',
                                  'Solo quien las produce',
                                  'Solo el Estado',
                                  'Solo empresas',
                                  'Ninguna persona en particular'],
                 'correcta': 'A'},
                {'pregunta': 'Los servicios también se conocen con el nombre '
                             'de trabajo:',
                 'alternativas': ['Intelectual exclusivo',
                                  'No productivo',
                                  'Físico exclusivo',
                                  'Productivo',
                                  'Manual exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se caracterizan por ser '
                             'inmateriales, es decir:',
                 'alternativas': ['Duran para siempre',
                                  'No pueden percibirse materialmente',
                                  'Solo los presta el Estado',
                                  'Se pueden almacenar',
                                  'Son siempre gratuitos'],
                 'correcta': 'B'},
                {'pregunta': 'Los servicios se consumen al mismo tiempo que '
                             'se:',
                 'alternativas': ['Producen',
                                  'Almacenan',
                                  'Regulan',
                                  'Exportan',
                                  'Prohíben'],
                 'correcta': 'A'},
                {'pregunta': 'Debido a que se consumen al momento de '
                             'producirse, los servicios no pueden:',
                 'alternativas': ['Prestarse',
                                  'Acumularse o ahorrarse',
                                  'Venderse',
                                  'Tener tarifa',
                                  'Ser regulados'],
                 'correcta': 'B'},
                {'pregunta': 'La prestación de cualquier servicio requiere '
                             'del uso de:',
                 'alternativas': ['Solo tecnología avanzada',
                                  'Solo dinero',
                                  'Ningún recurso adicional',
                                  'Bienes u objetos necesarios',
                                  'Solo mano de obra sin herramientas'],
                 'correcta': 'D'},
                {'pregunta': 'Según quién los brinda, los servicios pueden '
                             'clasificarse en privados y:',
                 'alternativas': ['Gratuitos exclusivos',
                                  'Informales',
                                  'Públicos',
                                  'Extranjeros exclusivos',
                                  'Ilegales'],
                 'correcta': 'C'},
                {'pregunta': 'Los servicios privados son administrados y '
                             'organizados por:',
                 'alternativas': ['La empresa privada',
                                  'El gobierno regional exclusivo',
                                  'Organismos internacionales',
                                  'El Estado exclusivamente',
                                  'Ninguna institución'],
                 'correcta': 'A'},
                {'pregunta': 'Se considera que un servicio es económico '
                             'cuando tiene como precio:',
                 'alternativas': ['Un subsidio',
                                  'Una tarifa',
                                  'Una multa',
                                  'Un impuesto',
                                  'Un salario'],
                 'correcta': 'B'},
                {'pregunta': 'La atención médica, la educación y el '
                             'transporte público son ejemplos de:',
                 'alternativas': ['Bienes de capital',
                                  'Servicios',
                                  'Materias primas',
                                  'Bienes tangibles',
                                  'Bienes públicos puros exclusivos'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE BIENES Y RECURSOS ECONÓMICOS',
                      'items': ['Los bienes son objetos que satisfacen '
                                'necesidades humanas; también se les conoce '
                                'como satisfactores.']},
                     {'titulo': 'BIENES LIBRES Y BIENES ECONÓMICOS',
                      'items': ['Los bienes no económicos o libres son '
                                'abundantes en la naturaleza y no tienen '
                                'relación de pertenencia.']},
                     {'titulo': 'CLASIFICACIÓN DE LOS BIENES ECONÓMICOS',
                      'items': ['Por su naturaleza, los bienes pueden ser '
                                'materiales o tangibles, y inmateriales o '
                                'intangibles.']},
                     {'titulo': 'BIENES PÚBLICOS',
                      'items': ['Un bien público es aquel cuyo consumo es '
                                'indivisible y puede ser compartido por '
                                'todos sin exclusión.']},
                     {'titulo': 'LOS SERVICIOS: CONCEPTO Y CARACTERÍSTICAS',
                      'items': ['Los servicios son actividades económicas '
                                'que satisfacen directamente necesidades de '
                                'otras personas.']},
                     {'titulo': 'CLASIFICACIÓN DE LOS SERVICIOS',
                      'items': ['Según quién los brinda, los servicios '
                                'pueden ser privados, administrados por la '
                                'empresa privada, o públicos.']}]},
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
                 'alternativas': ['El comercio exterior únicamente',
                                  'Solo la producción industrial',
                                  'Las necesidades humanas',
                                  'Solo la riqueza estatal',
                                  'Solo deseos superfluos'],
                 'correcta': 'C'},
                {'pregunta': 'El número de fases del proceso económico es:',
                 'alternativas': ['Dos', 'Cinco', 'Diez', 'Tres', 'Siete'],
                 'correcta': 'B'},
                {'pregunta': 'La fase del proceso económico orientada a '
                             'generar bienes y servicios es:',
                 'alternativas': ['La circulación',
                                  'La distribución',
                                  'La producción',
                                  'La inversión',
                                  'El consumo'],
                 'correcta': 'C'},
                {'pregunta': 'En la fase de producción aparece el llamado:',
                 'alternativas': ['Salario mínimo',
                                  'Interés bancario',
                                  'Valor agregado',
                                  'Tipo de cambio',
                                  'Producto bruto'],
                 'correcta': 'C'},
                {'pregunta': 'La fase donde la producción se traslada hacia '
                             'los mercados para su intercambio es:',
                 'alternativas': ['La circulación',
                                  'La producción',
                                  'El consumo',
                                  'La inversión',
                                  'La distribución'],
                 'correcta': 'A'},
                {'pregunta': 'La fase que reparte la riqueza entre los '
                             'factores productivos es:',
                 'alternativas': ['El consumo',
                                  'La inversión',
                                  'La producción',
                                  'La distribución',
                                  'La circulación'],
                 'correcta': 'D'},
                {'pregunta': 'En la fase de distribución, el trabajador '
                             'percibe sus ingresos vía:',
                 'alternativas': ['Subsidios',
                                  'Dividendos exclusivos',
                                  'Salario',
                                  'Herencia',
                                  'Impuestos'],
                 'correcta': 'C'},
                {'pregunta': 'En la fase de distribución, el Estado obtiene '
                             'ingresos mediante:',
                 'alternativas': ['Salarios',
                                  'Inversión extranjera',
                                  'Ahorro privado',
                                  'Ganancias empresariales',
                                  'Impuestos'],
                 'correcta': 'E'},
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
                 'alternativas': ['La distribución',
                                  'El consumo',
                                  'La circulación',
                                  'La inversión',
                                  'La producción'],
                 'correcta': 'D'},
                {'pregunta': 'La inversión se realiza mediante la '
                             'adquisición de bienes de:',
                 'alternativas': ['Lujo exclusivo',
                                  'Intercambio directo',
                                  'Uso personal',
                                  'Capital',
                                  'Consumo final'],
                 'correcta': 'D'},
                {'pregunta': 'El sector que obtiene el producto directamente '
                             'de los recursos naturales es el sector:',
                 'alternativas': ['Financiero',
                                  'Terciario',
                                  'Secundario',
                                  'Primario',
                                  'Comercial'],
                 'correcta': 'D'},
                {'pregunta': 'El sector primario incluye la agricultura, '
                             'ganadería, silvicultura, caza y:',
                 'alternativas': ['La pesca',
                                  'El comercio',
                                  'La minería',
                                  'La banca',
                                  'La industria textil'],
                 'correcta': 'A'},
                {'pregunta': 'La minería y la extracción de petróleo se '
                             'consideran parte del sector:',
                 'alternativas': ['Industrial o secundario',
                                  'Agropecuario',
                                  'Primario',
                                  'Terciario',
                                  'Financiero'],
                 'correcta': 'A'},
                {'pregunta': 'El sector secundario comprende la extracción y '
                             'transformación industrial de:',
                 'alternativas': ['Información digital',
                                  'Materias primas',
                                  'Capital humano',
                                  'Bienes intangibles',
                                  'Servicios financieros'],
                 'correcta': 'B'},
                {'pregunta': 'El sector secundario se divide en el subsector '
                             'extractivo y el subsector de:',
                 'alternativas': ['Servicios',
                                  'Consumo',
                                  'Transformación',
                                  'Distribución final',
                                  'Comercio'],
                 'correcta': 'C'},
                {'pregunta': 'El sector que incluye el comercio, la banca y '
                             'el transporte es el sector:',
                 'alternativas': ['Primario',
                                  'Terciario o de servicios',
                                  'Agropecuario',
                                  'Secundario',
                                  'Industrial'],
                 'correcta': 'B'},
                {'pregunta': 'El modelo de comercio directo entre empresa y '
                             'consumidor, favorecido por internet, se conoce '
                             'como:',
                 'alternativas': ['G2G', 'P2P', 'B2B', 'C2C', 'B2C'],
                 'correcta': 'E'},
                {'pregunta': 'El proceso económico es descrito en el texto '
                             'como un proceso:',
                 'alternativas': ['Sin relación entre sus fases',
                                  'Continuo e interrelacionado',
                                  'Estático',
                                  'Exclusivamente teórico',
                                  'Aislado y discontinuo'],
                 'correcta': 'B'},
                {'pregunta': 'Bajo el capitalismo, según el texto, entre '
                             'producción y consumo puede surgir:',
                 'alternativas': ['Una armonía perfecta',
                                  'Un equilibrio automático total',
                                  'La eliminación de la escasez',
                                  'Una contradicción cuando el consumo se '
                                  'retrasa de la producción',
                                  'Un crecimiento sin límites'],
                 'correcta': 'D'},
                {'pregunta': 'La producción se define como la primera fase '
                             'del proceso económico donde se combinan:',
                 'alternativas': ['Solo el trabajo',
                                  'Solo la naturaleza',
                                  'Solo el Estado',
                                  'Racionalmente los factores de producción',
                                  'Solo el capital'],
                 'correcta': 'D'},
                {'pregunta': 'Los factores productivos básicos o clásicos '
                             'son naturaleza, trabajo, capital y:',
                 'alternativas': ['Empresa',
                                  'Comercio',
                                  'Dinero',
                                  'Estado',
                                  'Tecnología'],
                 'correcta': 'A'},
                {'pregunta': 'El factor productivo naturaleza recibe como '
                             'retribución:',
                 'alternativas': ['La ganancia',
                                  'El impuesto',
                                  'El salario',
                                  'La renta',
                                  'El interés'],
                 'correcta': 'D'},
                {'pregunta': 'El factor productivo trabajo recibe como '
                             'retribución:',
                 'alternativas': ['El impuesto',
                                  'El interés',
                                  'El salario',
                                  'La renta',
                                  'La ganancia'],
                 'correcta': 'C'},
                {'pregunta': 'El factor productivo capital recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'La tarifa',
                                  'El interés',
                                  'El impuesto',
                                  'La renta'],
                 'correcta': 'C'},
                {'pregunta': 'El factor productivo empresa recibe como '
                             'retribución:',
                 'alternativas': ['El salario',
                                  'La renta',
                                  'La ganancia o utilidad',
                                  'El impuesto',
                                  'El interés'],
                 'correcta': 'C'},
                {'pregunta': 'El factor productivo Estado recibe como '
                             'retribución:',
                 'alternativas': ['La renta',
                                  'El salario',
                                  'El interés',
                                  'La ganancia',
                                  'Los impuestos o tributación'],
                 'correcta': 'E'},
                {'pregunta': 'La empresa es considerada el factor '
                             'productivo:',
                 'alternativas': ['Pasivo',
                                  'Estabilizador exclusivo',
                                  'Originario',
                                  'Regulador exclusivo',
                                  'Organizador'],
                 'correcta': 'E'},
                {'pregunta': 'El Estado, como factor productivo moderno, '
                             'cumple un papel:',
                 'alternativas': ['Solo consultivo',
                                  'Regulador y estabilizador',
                                  'Nulo en la economía',
                                  'Pasivo',
                                  'Solo simbólico'],
                 'correcta': 'B'},
                {'pregunta': 'La función de producción expresa los máximos '
                             'niveles de producción según la combinación de:',
                 'alternativas': ['Solo el trabajo',
                                  'Solo la naturaleza',
                                  'Solo el capital',
                                  'Los factores productivos',
                                  'Solo la tecnología'],
                 'correcta': 'D'},
                {'pregunta': 'En la función de producción, el producto y los '
                             'factores se miden en unidades:',
                 'alternativas': ['Físicas',
                                  'Relativas exclusivamente',
                                  'Porcentuales',
                                  'Subjetivas',
                                  'Monetarias'],
                 'correcta': 'A'},
                {'pregunta': 'Los factores productivos que no se pueden '
                             'modificar en el corto plazo, como fábricas, se '
                             'llaman factores:',
                 'alternativas': ['Clásicos exclusivos',
                                  'Fijos',
                                  'Modernos exclusivos',
                                  'Externos',
                                  'Variables'],
                 'correcta': 'B'},
                {'pregunta': 'Los factores productivos que sí se pueden '
                             'modificar en el corto plazo, como insumos, se '
                             'llaman factores:',
                 'alternativas': ['Modernos exclusivos',
                                  'Externos exclusivos',
                                  'Básicos exclusivos',
                                  'Fijos',
                                  'Variables'],
                 'correcta': 'E'},
                {'pregunta': 'La productividad mide cuántos bienes y '
                             'servicios se producen por cada:',
                 'alternativas': ['Cliente atendido',
                                  'Trabajador despedido',
                                  'Unidad monetaria exclusiva',
                                  'Impuesto pagado',
                                  'Factor utilizado'],
                 'correcta': 'E'},
                {'pregunta': 'A menor cantidad de recursos necesarios para '
                             'producir la misma cantidad, la productividad:',
                 'alternativas': ['Se mantiene igual siempre',
                                  'Disminuye',
                                  'Aumenta',
                                  'Desaparece',
                                  'Se vuelve negativa'],
                 'correcta': 'C'},
                {'pregunta': 'La productividad media se obtiene dividiendo '
                             'la producción total entre:',
                 'alternativas': ['El total de unidades del factor utilizado',
                                  'La inflación acumulada',
                                  'El número de empresas',
                                  'El precio de mercado',
                                  'Los ingresos totales'],
                 'correcta': 'A'},
                {'pregunta': 'La competitividad es la capacidad de una '
                             'empresa de desarrollar y mantener:',
                 'alternativas': ['Menor producción',
                                  'Ventajas comparativas',
                                  'Pérdidas constantes',
                                  'Deudas',
                                  'Menor calidad'],
                 'correcta': 'B'},
                {'pregunta': 'Una ventaja comparativa es un recurso o '
                             'atributo del que carecen:',
                 'alternativas': ['Los proveedores',
                                  'El Estado',
                                  'Los competidores',
                                  'Los clientes',
                                  'Los trabajadores'],
                 'correcta': 'C'},
                {'pregunta': 'Según Michael Porter, la ventaja competitiva '
                             'se relaciona con el valor creado para:',
                 'alternativas': ['Los competidores',
                                  'Los compradores',
                                  'El Estado',
                                  'Los proveedores exclusivos',
                                  'El gobierno'],
                 'correcta': 'B'},
                {'pregunta': 'La competitividad interna busca la mayor '
                             'eficiencia posible de los recursos:',
                 'alternativas': ['De la competencia',
                                  'Del gobierno',
                                  'Externos exclusivamente',
                                  'Del mercado internacional',
                                  'Propios de la organización'],
                 'correcta': 'E'},
                {'pregunta': 'La competitividad externa evalúa factores como '
                             'la innovación y:',
                 'alternativas': ['Solo los precios internos',
                                  'Solo el clima laboral',
                                  'Solo la ubicación geográfica',
                                  'La estabilidad económica',
                                  'Solo los salarios internos'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y FASES',
                      'items': ['El proceso económico es el conjunto de '
                                'actividades económicas que realizan los '
                                'seres humanos para obtener recursos que '
                                'satisfagan sus necesidades.']},
                     {'titulo': 'LAS FASES DEL PROCESO ECONÓMICO',
                      'items': ['La producción es la actividad social '
                                'orientada a generar los bienes y servicios '
                                'que permiten satisfacer necesidades.']},
                     {'titulo': 'LOS SECTORES PRODUCTIVOS',
                      'items': ['El sector primario o agropecuario obtiene '
                                'el producto directamente de los recursos '
                                'naturales, sin transformación industrial.']},
                     {'titulo': 'LA PRODUCCIÓN Y LOS FACTORES PRODUCTIVOS',
                      'items': ['La producción es la primera fase del '
                                'proceso económico, donde se combinan '
                                'racionalmente los factores para transformar '
                                'recursos en bienes.']},
                     {'titulo': 'RETRIBUCIÓN DE LOS FACTORES PRODUCTIVOS',
                      'items': ['El factor naturaleza recibe como '
                                'retribución la renta.']},
                     {'titulo': 'LA FUNCIÓN DE PRODUCCIÓN',
                      'items': ['La función de producción es una relación '
                                'técnica que expresa los máximos niveles de '
                                'producción según la combinación de '
                                'factores.']},
                     {'titulo': 'PRODUCTIVIDAD',
                      'items': ['La productividad mide cuántos bienes y '
                                'servicios se producen por cada factor '
                                'utilizado en un periodo.']},
                     {'titulo': 'COMPETITIVIDAD',
                      'items': ['La competitividad es la capacidad de una '
                                'empresa de desarrollar y mantener ventajas '
                                'comparativas.']}]},
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
                                  'Solo las máquinas',
                                  'La naturaleza en general',
                                  'Solo los animales',
                                  'Solamente el hombre'],
                 'correcta': 'E'},
                {'pregunta': 'El trabajo permite generar un nuevo valor '
                             'expresado en:',
                 'alternativas': ['Solo dinero',
                                  'Solo tecnología',
                                  'Bienes y servicios',
                                  'Solo información',
                                  'Solo tiempo libre'],
                 'correcta': 'C'},
                {'pregunta': 'El ciclo PHVA también se conoce como el '
                             'círculo de:',
                 'alternativas': ['Deming',
                                  'Smith',
                                  'Keynes',
                                  'Wieser',
                                  'Marx'],
                 'correcta': 'A'},
                {'pregunta': 'Las siglas PHVA corresponden a Planificar, '
                             'Hacer, Verificar y:',
                 'alternativas': ['Aprobar',
                                  'Aplicar',
                                  'Ajustar',
                                  'Analizar',
                                  'Actuar'],
                 'correcta': 'E'},
                {'pregunta': 'En la etapa de Planificar del ciclo PHVA se '
                             'identifican actividades susceptibles de:',
                 'alternativas': ['Mejora',
                                  'Externalización',
                                  'Reducción de personal',
                                  'Privatización',
                                  'Eliminación total'],
                 'correcta': 'A'},
                {'pregunta': 'En la etapa de Hacer se recomienda aplicar '
                             'antes de un cambio a gran escala una:',
                 'alternativas': ['Fusión empresarial',
                                  'Reducción de costos',
                                  'Campaña publicitaria',
                                  'Auditoría externa',
                                  'Prueba piloto a pequeña escala'],
                 'correcta': 'E'},
                {'pregunta': 'En la etapa de Verificar se comprueba:',
                 'alternativas': ['El tipo de cambio',
                                  'El buen funcionamiento de la mejora '
                                  'implementada',
                                  'La inflación mensual',
                                  'El presupuesto anual',
                                  'La rentabilidad accionaria'],
                 'correcta': 'B'},
                {'pregunta': 'En la etapa de Actuar, si los resultados son '
                             'satisfactorios, se procede a:',
                 'alternativas': ['Descartar la mejora',
                                  'Implantar la mejora en forma definitiva y '
                                  'a gran escala',
                                  'Repetir solo la primera etapa',
                                  'Reducir el personal',
                                  'Suspender el proyecto'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo se define como la '
                             'especialización del trabajo cooperativo en:',
                 'alternativas': ['Tareas específicas y regladas',
                                  'Ninguna tarea concreta',
                                  'Actividades improvisadas',
                                  'Tareas generales sin orden',
                                  'Un solo puesto fijo'],
                 'correcta': 'A'},
                {'pregunta': 'El objetivo de la división del trabajo es la '
                             'especialización para aumentar:',
                 'alternativas': ['El ocio',
                                  'La inflación',
                                  'La informalidad',
                                  'El desempleo',
                                  'La productividad'],
                 'correcta': 'E'},
                {'pregunta': 'La división del trabajo en la que los seres '
                             'humanos se dedican a actividades '
                             'especializadas diversas desde la antigüedad es '
                             'la división:',
                 'alternativas': ['Interna',
                                  'Internacional',
                                  'Empresarial',
                                  'Técnica exclusiva',
                                  'Social'],
                 'correcta': 'E'},
                {'pregunta': 'La división del trabajo propia de la gran '
                             'industria moderna, donde cada obrero hace una '
                             'parte de un proceso complejo, es la división:',
                 'alternativas': ['Artesanal',
                                  'Internacional',
                                  'Rural',
                                  'Interna',
                                  'Social'],
                 'correcta': 'D'},
                {'pregunta': 'La especialización de los países según su '
                             'eficiencia productiva se llama división:',
                 'alternativas': ['Interna del trabajo',
                                  'Social del trabajo',
                                  'Internacional del trabajo',
                                  'Rural del trabajo',
                                  'Artesanal del trabajo'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las características del trabajo figura '
                             'la necesidad de una figura que dirija al '
                             'equipo, llamada:',
                 'alternativas': ['Motivación',
                                  'Esfuerzo',
                                  'Dignidad',
                                  'Interdependencia',
                                  'Liderazgo'],
                 'correcta': 'E'},
                {'pregunta': 'El compromiso que estimula el cumplimiento de '
                             'las obligaciones laborales se llama:',
                 'alternativas': ['Motivación',
                                  'Fin económico',
                                  'Liderazgo',
                                  'Actividad consciente',
                                  'Interdependencia'],
                 'correcta': 'A'},
                {'pregunta': 'El trabajo se diferencia del deporte '
                             'principalmente porque el trabajo tiene un fin:',
                 'alternativas': ['Recreativo',
                                  'Económico',
                                  'Sin propósito definido',
                                  'Espiritual',
                                  'Artístico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo es descrito como una actividad '
                             'consciente porque el individuo:',
                 'alternativas': ['Repite acciones sin sentido',
                                  'Actúa por instinto puro',
                                  'Sabe lo que hace y conoce el fin que '
                                  'persigue',
                                  'No tiene ningún objetivo',
                                  'Actúa como un autómata'],
                 'correcta': 'C'},
                {'pregunta': 'Según el texto, el trabajo dignifica al hombre '
                             'porque le otorga:',
                 'alternativas': ['Menos responsabilidades',
                                  'Solo dinero',
                                  'La estimación y el respeto de sus '
                                  'semejantes',
                                  'Más tiempo libre exclusivamente',
                                  'Ninguna consecuencia social'],
                 'correcta': 'C'},
                {'pregunta': 'Un sistema de trabajo comprende, entre otros '
                             'aspectos, la estructura de tareas y su:',
                 'alternativas': ['Anulación',
                                  'Sincronización',
                                  'Improvisación',
                                  'Privatización',
                                  'Eliminación total'],
                 'correcta': 'B'},
                {'pregunta': 'La mejora continua busca optimizar la calidad '
                             'de un producto, proceso o:',
                 'alternativas': ['Servicio',
                                  'Solo la publicidad',
                                  'Solo el empaque',
                                  'Solo el precio',
                                  'Solo el transporte'],
                 'correcta': 'A'},
                {'pregunta': 'La división del trabajo en la que los seres '
                             'humanos se dedican a actividades diversas '
                             'desde la antigüedad se llama división:',
                 'alternativas': ['Internacional',
                                  'Social',
                                  'Técnica exclusiva',
                                  'Interna',
                                  'Empresarial'],
                 'correcta': 'B'},
                {'pregunta': 'La división del trabajo propia de la industria '
                             'moderna, donde cada obrero realiza una parte '
                             'de un proceso, se llama división:',
                 'alternativas': ['Artesanal',
                                  'Rural',
                                  'Internacional',
                                  'Interna',
                                  'Social'],
                 'correcta': 'D'},
                {'pregunta': 'La especialización de los países en producir '
                             'lo que son más eficientes se llama división:',
                 'alternativas': ['Artesanal del trabajo',
                                  'Social del trabajo',
                                  'Interna del trabajo',
                                  'Rural del trabajo',
                                  'Internacional del trabajo'],
                 'correcta': 'E'},
                {'pregunta': 'El salario se define como la suma de dinero '
                             'que recibe periódicamente un trabajador de su:',
                 'alternativas': ['Banco',
                                  'Familia',
                                  'Sindicato',
                                  'Gobierno exclusivamente',
                                  'Empleador'],
                 'correcta': 'E'},
                {'pregunta': 'El pago diario del salario recibe el nombre '
                             'de:',
                 'alternativas': ['Haber',
                                  'Honorario',
                                  'Sueldo',
                                  'Estipendio exclusivo',
                                  'Jornal'],
                 'correcta': 'E'},
                {'pregunta': 'El término «salario» proviene del vocablo '
                             'latino «salarium», que significa:',
                 'alternativas': ['Pago de vino',
                                  'Pago de agua',
                                  'Pago de oro',
                                  'Pago de trigo',
                                  'Pago de sal'],
                 'correcta': 'E'},
                {'pregunta': 'En la antigua Roma, la sal era un bien escaso '
                             'usado como:',
                 'alternativas': ['Material de construcción',
                                  'Combustible',
                                  'Moneda exclusiva',
                                  'Antiséptico y preservante de alimentos',
                                  'Colorante'],
                 'correcta': 'D'},
                {'pregunta': 'La ruta romana por la cual ingresaba la sal a '
                             'Roma se llamaba:',
                 'alternativas': ['Vía Salaria',
                                  'Vía Apia',
                                  'Vía Flaminia',
                                  'Vía Domicia',
                                  'Vía Aurelia'],
                 'correcta': 'A'},
                {'pregunta': 'El jornal es la retribución que recibe el '
                             'obrero por cada:',
                 'alternativas': ['Cliente atendido',
                                  'Jornada laboral',
                                  'Proyecto terminado',
                                  'Año de servicio',
                                  'Mes trabajado'],
                 'correcta': 'B'},
                {'pregunta': 'El jornal se paga, por lo general, de forma:',
                 'alternativas': ['Trimestral',
                                  'Mensual',
                                  'Semanal',
                                  'Solo al final del contrato',
                                  'Anual'],
                 'correcta': 'C'},
                {'pregunta': 'El sueldo, también llamado haber, es el pago '
                             'que perciben:',
                 'alternativas': ['Solo los estudiantes',
                                  'Solo los obreros',
                                  'Solo los desempleados',
                                  'Los empleados del sector público o '
                                  'privado',
                                  'Solo los jubilados'],
                 'correcta': 'D'},
                {'pregunta': 'El trabajo es considerado en la actualidad un '
                             'derecho:',
                 'alternativas': ['Solo comercial',
                                  'Humano social',
                                  'Opcional del Estado',
                                  'Solo privado',
                                  'Exclusivo de adultos mayores'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['El trabajo es el conjunto de aptitudes '
                                'físicas y mentales, propias solamente del '
                                'hombre, para intervenir en la actividad '
                                'económica.']},
                     {'titulo': 'EL CICLO PHVA O CÍRCULO DE DEMING',
                      'items': ['El ciclo PDCA, en español PHVA, corresponde '
                                'a las etapas de Planificar, Hacer, '
                                'Verificar y Actuar.']},
                     {'titulo': 'DIVISIÓN DEL TRABAJO',
                      'items': ['La división del trabajo es la '
                                'especialización del trabajo cooperativo en '
                                'tareas específicas y regladas.']},
                     {'titulo': 'CARACTERÍSTICAS DEL TRABAJO',
                      'items': ['El trabajo requiere liderazgo, la figura de '
                                'quien dirige a los trabajadores hacia los '
                                'objetivos.']},
                     {'titulo': 'MODALIDADES DE LA DIVISIÓN DEL TRABAJO',
                      'items': ['La división social del trabajo surge cuando '
                                'los seres humanos se dedican a actividades '
                                'especializadas diversas.']},
                     {'titulo': 'EL SALARIO: CONCEPTO Y ORIGEN',
                      'items': ['El salario, o remuneración, es la suma de '
                                'dinero que recibe un trabajador de su '
                                'empleador por su trabajo.']},
                     {'titulo': 'FORMAS DE REMUNERACIÓN',
                      'items': ['El jornal es la retribución que recibe el '
                                'obrero por cada jornada laboral, pagada por '
                                'lo general semanalmente.']}]},
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
                 'alternativas': ['La exportación exclusiva',
                                  'El consumo directo',
                                  'El pago de impuestos',
                                  'Ser usados en la producción de otros '
                                  'bienes',
                                  'El ahorro personal'],
                 'correcta': 'D'},
                {'pregunta': 'El capital, en su concepción económica, '
                             'corresponde contablemente al concepto de:',
                 'alternativas': ['Patrimonio neto',
                                  'Pasivo a corto plazo',
                                  'Activo fijo',
                                  'Activo circulante',
                                  'Capital de trabajo'],
                 'correcta': 'C'},
                {'pregunta': 'Para la ciencia contable, el capital incluye '
                             'también el activo:',
                 'alternativas': ['Solo inmuebles',
                                  'Solo maquinaria',
                                  'Fijo exclusivamente',
                                  'Circulante',
                                  'Ninguno adicional'],
                 'correcta': 'D'},
                {'pregunta': 'El capital de trabajo se define como la '
                             'diferencia entre el activo circulante y:',
                 'alternativas': ['El activo fijo',
                                  'El patrimonio total',
                                  'El pasivo a corto plazo',
                                  'El capital social',
                                  'Las utilidades anuales'],
                 'correcta': 'C'},
                {'pregunta': 'Según la teoría neoclásica, el capital surge '
                             'de la combinación de trabajo y:',
                 'alternativas': ['Dinero',
                                  'Naturaleza',
                                  'Comercio',
                                  'Impuestos',
                                  'Tecnología exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Una forma de obtención del capital es mediante '
                             'el sobrante de la producción, llamado:',
                 'alternativas': ['Capital de trabajo',
                                  'Inversión extranjera',
                                  'Ahorro',
                                  'Excedente económico',
                                  'Depreciación'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de la abstinencia sobre la formación '
                             'del capital fue desarrollada por:',
                 'alternativas': ['Karl Marx',
                                  'John Keynes',
                                  'Adam Smith',
                                  'Nassau Senior',
                                  'Friedrich von Wieser'],
                 'correcta': 'D'},
                {'pregunta': 'Según la teoría de la abstinencia, no consumir '
                             'toda la riqueza permite:',
                 'alternativas': ['Eliminar el ahorro',
                                  'Liberar recursos para producir bienes de '
                                  'capital',
                                  'Incrementar el consumo inmediato',
                                  'Aumentar la inflación',
                                  'Reducir la producción total'],
                 'correcta': 'B'},
                {'pregunta': 'Según Nassau Senior, la demanda del capital '
                             'depende de su nivel de:',
                 'alternativas': ['Escasez',
                                  'Antigüedad',
                                  'Ubicación geográfica',
                                  'Productividad',
                                  'Color'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de la abstinencia justifica el cobro '
                             'de intereses en base a virtudes como:',
                 'alternativas': ['La imprevisión',
                                  'La generosidad excesiva',
                                  'El consumo inmediato',
                                  'El derroche',
                                  'La previsión, sobriedad y frugalidad'],
                 'correcta': 'E'},
                {'pregunta': 'El capital sirve, entre otras cosas, para la '
                             'creación de nuevas:',
                 'alternativas': ['Inflaciones',
                                  'Necesidades',
                                  'Empresas',
                                  'Deudas públicas',
                                  'Crisis económicas'],
                 'correcta': 'C'},
                {'pregunta': 'El capital condiciona, según el texto:',
                 'alternativas': ['Solo la religión',
                                  'Solo el idioma',
                                  'Solo el clima',
                                  'Las diversas formas de trabajo',
                                  'Solo la política'],
                 'correcta': 'D'},
                {'pregunta': 'El capital, según el texto, interviene en la '
                             'satisfacción de necesidades humanas de forma:',
                 'alternativas': ['Solo simbólica',
                                  'Nula',
                                  'Directa exclusivamente',
                                  'Indirecta, al incrementar la producción',
                                  'Aleatoria'],
                 'correcta': 'D'},
                {'pregunta': 'El desgaste del capital por su uso se '
                             'contabiliza mediante la:',
                 'alternativas': ['Inversión',
                                  'Oferta',
                                  'Demanda',
                                  'Inflación',
                                  'Depreciación'],
                 'correcta': 'E'},
                {'pregunta': 'En época de crisis económica, la demanda de '
                             'capital tiende a:',
                 'alternativas': ['Aumentar por falta de capitales',
                                  'Mantenerse igual siempre',
                                  'Disminuir siempre',
                                  'Volverse negativa',
                                  'Desaparecer'],
                 'correcta': 'A'},
                {'pregunta': 'En época de prosperidad, el valor del capital '
                             'tiende a:',
                 'alternativas': ['Duplicarse automáticamente',
                                  'Volverse negativo',
                                  'Desaparecer',
                                  'Aumentar siempre bruscamente',
                                  'Estabilizarse o bajar'],
                 'correcta': 'E'},
                {'pregunta': 'Un ejemplo de capital, según el texto, es la '
                             'cadena de montaje de una empresa como:',
                 'alternativas': ['Toyota',
                                  'Un hospital',
                                  'Un supermercado',
                                  'Un banco',
                                  'Una universidad'],
                 'correcta': 'A'},
                {'pregunta': 'El capital, según la ciencia económica, se '
                             'diferencia de la inversión porque esta última '
                             'comprende:',
                 'alternativas': ['Ningún activo',
                                  'Solo el consumo',
                                  'El activo fijo más el activo circulante',
                                  'Solo el ahorro',
                                  'Solo el activo fijo'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando el hombre mezcló agua con tierra para '
                             'construir adobes, se ejemplifica el origen del '
                             'capital por:',
                 'alternativas': ['La teoría de la abstinencia',
                                  'El ahorro',
                                  'La inversión extranjera',
                                  'La acción del hombre sobre la naturaleza',
                                  'El excedente económico exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'El proceso de acumulación por excedente '
                             'económico se dio principalmente en modos de '
                             'producción:',
                 'alternativas': ['Solo feudales tardíos',
                                  'Exclusivamente modernos',
                                  'Solo socialistas',
                                  'Solo poscapitalistas',
                                  'Precapitalistas y las primeras fases del '
                                  'capitalismo'],
                 'correcta': 'E'},
                {'pregunta': 'Según la teoría clásica, los bienes usados en '
                             'la producción de nuevos bienes, como '
                             'maquinaria, forman el capital:',
                 'alternativas': ['Bancario',
                                  'Financiero',
                                  'Productivo',
                                  'Lucrativo',
                                  'Comercial'],
                 'correcta': 'C'},
                {'pregunta': 'El capital que sirve en varios procesos '
                             'productivos, trasladando su valor por partes, '
                             'es el capital:',
                 'alternativas': ['Comercial',
                                  'Circulante',
                                  'Bancario',
                                  'Lucrativo',
                                  'Fijo'],
                 'correcta': 'E'},
                {'pregunta': 'El capital empleado en un solo proceso '
                             'productivo, como el trigo o el algodón, es el '
                             'capital:',
                 'alternativas': ['Fijo',
                                  'Lucrativo',
                                  'Financiero',
                                  'Circulante',
                                  'Industrial'],
                 'correcta': 'D'},
                {'pregunta': 'El capital que genera renta sin destinarse '
                             'directamente a la producción, como una casa en '
                             'alquiler, es el capital:',
                 'alternativas': ['Lucrativo',
                                  'Circulante',
                                  'Productivo',
                                  'Bancario',
                                  'Fijo'],
                 'correcta': 'A'},
                {'pregunta': 'El capital comercial se originó en la fase '
                             'mercantilista del capitalismo, priorizando:',
                 'alternativas': ['La banca',
                                  'La agricultura exclusiva',
                                  'La industria pesada',
                                  'La minería exclusiva',
                                  'El comercio exterior'],
                 'correcta': 'E'},
                {'pregunta': 'El capital industrial se originó en la etapa '
                             'industrial para adquirir, entre otros '
                             'recursos:',
                 'alternativas': ['Solo software',
                                  'Solo dinero',
                                  'Materias primas, mano de obra y '
                                  'maquinaria',
                                  'Solo tierras',
                                  'Solo patentes'],
                 'correcta': 'C'},
                {'pregunta': 'El capital bancario surgió cuando la burguesía '
                             'industrial creó las primeras:',
                 'alternativas': ['Universidades',
                                  'Colonias',
                                  'Entidades financieras (bancos)',
                                  'Fábricas',
                                  'Bolsas de valores exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'Los bancos generan excedente porque la tasa de '
                             'interés que cobran en préstamos es:',
                 'alternativas': ['Inexistente',
                                  'Regulada por otro banco',
                                  'Igual a la que pagan a ahorristas',
                                  'Menor a la que pagan a ahorristas',
                                  'Mayor a la que pagan a los ahorristas'],
                 'correcta': 'E'},
                {'pregunta': 'El capital financiero corresponde a la etapa:',
                 'alternativas': ['Socialista',
                                  'Precapitalista',
                                  'Monopólica del capitalismo',
                                  'Feudal',
                                  'Mercantilista'],
                 'correcta': 'C'},
                {'pregunta': 'El capital financiero surge de la fusión del '
                             'capital industrial y el capital:',
                 'alternativas': ['Comercial',
                                  'Fijo',
                                  'Bancario',
                                  'Circulante',
                                  'Lucrativo'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['Para la ciencia económica, el capital es el '
                                'conjunto de objetos fabricados por el '
                                'hombre para ser usados en la producción de '
                                'otros bienes.']},
                     {'titulo': 'FORMAS DE OBTENCIÓN DEL CAPITAL (TEORÍA '
                                'NEOCLÁSICA)',
                      'items': ['El capital surge por la acción del hombre '
                                'sobre la naturaleza, combinando los '
                                'factores originarios de trabajo y '
                                'naturaleza.']},
                     {'titulo': 'ROL DEL CAPITAL EN LA PRODUCCIÓN',
                      'items': ['El capital sirve para la creación de nuevas '
                                'empresas, la ampliación de las existentes y '
                                'la realización de grandes obras.']},
                     {'titulo': 'CLASES DE CAPITAL (TEORÍA CLÁSICA)',
                      'items': ['El capital productivo son bienes usados en '
                                'la producción de nuevos bienes, como '
                                'maquinaria industrial.']},
                     {'titulo': 'OTROS TIPOS DE CAPITAL',
                      'items': ['El capital comercial se originó en la fase '
                                'mercantilista del capitalismo, con el '
                                'excedente del comercio exterior.']}]},
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
                           'origen mineral.']}],
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
                 'alternativas': ['Artificiales',
                                  'Creados por el hombre',
                                  'Exclusivamente urbanos',
                                  'Producidos industrialmente',
                                  'Preexistentes al hombre'],
                 'correcta': 'E'},
                {'pregunta': 'La naturaleza también se denomina reservas '
                             'naturales o factor:',
                 'alternativas': ['Capital',
                                  'Trabajo',
                                  'Dinero',
                                  'Tierra',
                                  'Empresa'],
                 'correcta': 'D'},
                {'pregunta': 'La naturaleza es considerada un factor '
                             'productivo originario porque:',
                 'alternativas': ['Es anterior a la producción',
                                  'Se crea con tecnología',
                                  'Requiere siempre inversión',
                                  'Resulta de un proceso productivo previo',
                                  'Depende del capital'],
                 'correcta': 'A'},
                {'pregunta': 'La naturaleza cumple en la producción un rol:',
                 'alternativas': ['Pasivo',
                                  'Comercial',
                                  'Secundario nulo',
                                  'Exclusivamente financiero',
                                  'Activo y determinante'],
                 'correcta': 'A'},
                {'pregunta': 'La naturaleza es un factor condicionante '
                             'porque, por ejemplo, la agricultura depende '
                             'de:',
                 'alternativas': ['Solo el mercado',
                                  'Solo la mano de obra',
                                  'Solo el capital disponible',
                                  'Solo la tecnología',
                                  'El suelo y el clima'],
                 'correcta': 'E'},
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
                                  'Interés',
                                  'Dividendo',
                                  'Ganancia empresarial',
                                  'Renta'],
                 'correcta': 'E'},
                {'pregunta': 'El medio geográfico, o medio ambiente, '
                             'comprende principalmente:',
                 'alternativas': ['Solo la fauna',
                                  'El territorio y el clima',
                                  'Solo el clima',
                                  'Solo el subsuelo',
                                  'Solo el suelo'],
                 'correcta': 'B'},
                {'pregunta': 'El territorio está constituido por el suelo, '
                             'subsuelo, relieve orográfico y:',
                 'alternativas': ['El presupuesto público',
                                  'El comercio',
                                  'La moneda nacional',
                                  'El sistema financiero',
                                  'La situación geográfica'],
                 'correcta': 'E'},
                {'pregunta': 'El clima condiciona directamente actividades '
                             'económicas como:',
                 'alternativas': ['La política monetaria',
                                  'La agricultura y la producción textil',
                                  'La banca central',
                                  'El comercio internacional exclusivamente',
                                  'El sistema tributario'],
                 'correcta': 'B'},
                {'pregunta': 'El Perú cuenta con un número de microclimas '
                             'superior a:',
                 'alternativas': ['80', '5', '10', '20', '200'],
                 'correcta': 'A'},
                {'pregunta': 'Los elementos primarios sin extraer ni '
                             'modificar por el hombre se llaman:',
                 'alternativas': ['Insumos industriales',
                                  'Materias brutas',
                                  'Materias primas',
                                  'Bienes finales',
                                  'Bienes de capital'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos que la naturaleza ofrece y '
                             'sirven de base para elaborar bienes finales se '
                             'llaman:',
                 'alternativas': ['Recursos financieros',
                                  'Materias primas',
                                  'Materias brutas',
                                  'Bienes libres',
                                  'Activos fijos'],
                 'correcta': 'B'},
                {'pregunta': 'El algodón, fruto del trabajo agrícola, es un '
                             'ejemplo de:',
                 'alternativas': ['Bien de capital',
                                  'Materia prima',
                                  'Bien final',
                                  'Materia bruta',
                                  'Recurso financiero'],
                 'correcta': 'B'},
                {'pregunta': 'Las materias primas provienen de tres fuentes: '
                             'animal, vegetal y:',
                 'alternativas': ['Industrial',
                                  'Financiera',
                                  'Comercial',
                                  'Digital',
                                  'Mineral'],
                 'correcta': 'E'},
                {'pregunta': 'La lana, las carnes y el marfil son ejemplos '
                             'de materias primas de origen:',
                 'alternativas': ['Financiero',
                                  'Industrial',
                                  'Animal',
                                  'Vegetal',
                                  'Mineral'],
                 'correcta': 'C'},
                {'pregunta': 'Para aprovechar los recursos naturales, el ser '
                             'humano debe aplicar:',
                 'alternativas': ['Ningún esfuerzo adicional',
                                  'Su fuerza de trabajo',
                                  'Solo tecnología importada',
                                  'Solo comercio exterior',
                                  'Solo capital'],
                 'correcta': 'B'},
                {'pregunta': 'La naturaleza se presenta como un depósito de '
                             'materias brutas y fuentes de:',
                 'alternativas': ['Energías',
                                  'Créditos',
                                  'Impuestos',
                                  'Comercio',
                                  'Inflación'],
                 'correcta': 'A'},
                {'pregunta': 'En la sierra sur del Perú, la producción de '
                             'papa se explica por la influencia de:',
                 'alternativas': ['El comercio exterior',
                                  'La tecnología importada',
                                  'El sistema financiero',
                                  'La política monetaria',
                                  'El suelo y el clima'],
                 'correcta': 'E'},
                {'pregunta': 'El descanso de tierras y la rotación de '
                             'cultivos en la sierra ejemplifican:',
                 'alternativas': ['La imposición total del hombre sobre la '
                                  'naturaleza',
                                  'La sustitución de la tierra por capital',
                                  'La eliminación del factor tierra',
                                  'Una búsqueda de armonía entre el hombre y '
                                  'la naturaleza',
                                  'El abandono total de la agricultura'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y CARACTERÍSTICAS',
                      'items': ['La naturaleza es el conjunto de elementos '
                                'preexistentes al hombre que componen la '
                                'realidad física.']},
                     {'titulo': 'ASPECTOS DE LA NATURALEZA',
                      'items': ['El medio geográfico, o medio ambiente, '
                                'comprende el territorio y el clima.']}]},
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
                 'alternativas': ['Recaudación tributaria',
                                  'Consumo exclusivo',
                                  'Prestación de servicios',
                                  'Emisión monetaria',
                                  'Ahorro personal'],
                 'correcta': 'C'},
                {'pregunta': 'La empresa combina los factores clásicos de '
                             'producción: naturaleza, trabajo y:',
                 'alternativas': ['Capital',
                                  'Comercio',
                                  'Dinero exclusivamente',
                                  'Publicidad',
                                  'Impuestos'],
                 'correcta': 'A'},
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
                 'alternativas': ['Lucrativo exclusivo',
                                  'Mercantil',
                                  'Social',
                                  'Económico',
                                  'Jurídico'],
                 'correcta': 'D'},
                {'pregunta': 'Que la producción de la empresa se destine al '
                             'intercambio en el mercado corresponde a su '
                             'fin:',
                 'alternativas': ['Jurídico',
                                  'Ninguno en particular',
                                  'Económico',
                                  'Social',
                                  'Mercantil'],
                 'correcta': 'E'},
                {'pregunta': 'Que el empresario busque maximizar ganancias '
                             'minimizando costos corresponde a su fin:',
                 'alternativas': ['Económico general',
                                  'Jurídico',
                                  'Mercantil',
                                  'Social',
                                  'Lucrativo'],
                 'correcta': 'E'},
                {'pregunta': 'La responsabilidad de proveer bienes que no '
                             'causen peligro en su consumo corresponde a la '
                             'responsabilidad:',
                 'alternativas': ['Tributaria',
                                  'Social',
                                  'Económica',
                                  'Comercial',
                                  'Jurídica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas constituidas por el aporte de '
                             'personas o instituciones particulares son las '
                             'empresas:',
                 'alternativas': ['Privadas',
                                  'Estatales',
                                  'Públicas',
                                  'Mixtas',
                                  'Municipales exclusivas'],
                 'correcta': 'A'},
                {'pregunta': 'Las empresas en las que el Estado aporta el '
                             'capital social se llaman empresas:',
                 'alternativas': ['Públicas',
                                  'Privadas',
                                  'Unipersonales',
                                  'Individuales',
                                  'Mixtas'],
                 'correcta': 'A'},
                {'pregunta': 'La finalidad de las empresas públicas es '
                             'principalmente:',
                 'alternativas': ['La evasión tributaria',
                                  'El comercio exterior únicamente',
                                  'Prestar servicios a la colectividad',
                                  'La especulación financiera',
                                  'El lucro exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'Las empresas en las que el capital proviene en '
                             'parte del Estado y en parte de privados se '
                             'llaman empresas:',
                 'alternativas': ['Privadas',
                                  'Mixtas',
                                  'Individuales',
                                  'Unipersonales',
                                  'Públicas'],
                 'correcta': 'B'},
                {'pregunta': 'Para ser considerada mixta, el Estado debe '
                             'tener como mínimo un porcentaje de acciones '
                             'de:',
                 'alternativas': ['100%', '80%', '20%', '5%', '50%'],
                 'correcta': 'C'},
                {'pregunta': 'El proceso mediante el cual el Estado '
                             'transfiere su participación empresarial al '
                             'sector privado se llama:',
                 'alternativas': ['Privatización',
                                  'Colectivización',
                                  'Nacionalización',
                                  'Estatización',
                                  'Municipalización'],
                 'correcta': 'A'},
                {'pregunta': 'Las empresas en las que no existen socios y el '
                             'propietario aporta todo el capital son las '
                             'empresas:',
                 'alternativas': ['Cooperativas',
                                  'Sociedades mercantiles',
                                  'Públicas',
                                  'Mixtas',
                                  'Individuales'],
                 'correcta': 'E'},
                {'pregunta': 'En la empresa unipersonal, la responsabilidad '
                             'del propietario es:',
                 'alternativas': ['Ilimitada, responde con todo su '
                                  'patrimonio',
                                  'Nula',
                                  'Limitada al capital aportado',
                                  'Compartida con el Estado',
                                  'Transferible a terceros'],
                 'correcta': 'A'},
                {'pregunta': 'Para constituir una empresa unipersonal:',
                 'alternativas': ['Se requiere capital extranjero',
                                  'No se requiere escritura pública',
                                  'Se necesita ser una sociedad mercantil',
                                  'Se requiere escritura pública obligatoria',
                                  'Se necesita autorización del Congreso'],
                 'correcta': 'B'},
                {'pregunta': 'Las empresas privadas de varios propietarios '
                             'se conocen como:',
                 'alternativas': ['Cooperativas estatales',
                                  'Empresas públicas',
                                  'Empresas mixtas obligatorias',
                                  'Empresas unipersonales',
                                  'Sociedades mercantiles'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los precios más importantes para las '
                             'decisiones empresariales figura el costo de la '
                             'mano de obra, es decir:',
                 'alternativas': ['La inflación',
                                  'Los salarios',
                                  'El tipo de cambio',
                                  'Los impuestos',
                                  'Las utilidades'],
                 'correcta': 'B'},
                {'pregunta': 'La importancia de la empresa radica, entre '
                             'otros aspectos, en el incremento constante de:',
                 'alternativas': ['El endeudamiento',
                                  'La productividad',
                                  'La evasión fiscal',
                                  'La especulación',
                                  'La informalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La empresa es descrita como el centro del '
                             'proceso productivo en una economía:',
                 'alternativas': ['Capitalista',
                                  'Primitiva',
                                  'Autárquica',
                                  'Feudal',
                                  'De trueque'],
                 'correcta': 'A'},
                {'pregunta': 'En la EIRL, el propietario único acude al '
                             'Registro Mercantil para constituir una persona '
                             'jurídica con:',
                 'alternativas': ['Ningún patrimonio',
                                  'Patrimonio de terceros',
                                  'Patrimonio propio, independiente del '
                                  'propietario',
                                  'Patrimonio compartido con el Estado',
                                  'Patrimonio del propietario '
                                  'exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'En la EIRL, la responsabilidad de la empresa '
                             'está limitada a:',
                 'alternativas': ['El doble del capital aportado',
                                  'El patrimonio personal del titular',
                                  'Ningún límite',
                                  'La mitad del capital aportado',
                                  'El patrimonio de la empresa'],
                 'correcta': 'E'},
                {'pregunta': 'En la EIRL, el órgano máximo que decide sobre '
                             'los bienes y actividades es:',
                 'alternativas': ['Los accionistas',
                                  'El titular',
                                  'El directorio',
                                  'La gerencia',
                                  'La junta de socios'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad civil es utilizada frecuentemente '
                             'por estudios de abogados y otras:',
                 'alternativas': ['Asociaciones profesionales',
                                  'Fábricas industriales',
                                  'Empresas navieras',
                                  'Minas',
                                  'Granjas'],
                 'correcta': 'A'},
                {'pregunta': 'Las sociedades mercantiles se forman con la '
                             'finalidad de desarrollar actividades:',
                 'alternativas': ['Sin fines de lucro',
                                  'Solo benéficas',
                                  'Solo religiosas',
                                  'Solo educativas',
                                  'Con fines lucrativos'],
                 'correcta': 'E'},
                {'pregunta': 'En la Sociedad Colectiva, los socios responden '
                             'por las deudas sociales de forma:',
                 'alternativas': ['Proporcional exclusivamente',
                                  'Estatal',
                                  'Nula',
                                  'Ilimitada y solidaria',
                                  'Limitada'],
                 'correcta': 'D'},
                {'pregunta': 'La Sociedad Comercial de Responsabilidad '
                             'Limitada (S.R.L.) puede tener entre 2 y un '
                             'máximo de:',
                 'alternativas': ['10 socios',
                                  '20 socios',
                                  '5 socios',
                                  '50 socios',
                                  '100 socios'],
                 'correcta': 'B'},
                {'pregunta': 'En la S.R.L., los socios se denominan:',
                 'alternativas': ['Socios participacionistas',
                                  'Gerentes',
                                  'Socios colectivos',
                                  'Titulares',
                                  'Accionistas'],
                 'correcta': 'A'},
                {'pregunta': 'En la S.R.L., la responsabilidad de los socios '
                             'está limitada a:',
                 'alternativas': ['Todo su patrimonio personal',
                                  'La ganancia obtenida',
                                  'Ningún límite',
                                  'El doble del aporte',
                                  'El monto aportado al capital social'],
                 'correcta': 'E'},
                {'pregunta': 'El capital de la Sociedad Anónima (S.A.) está '
                             'representado por:',
                 'alternativas': ['Acciones nominativas',
                                  'Cuotas fijas',
                                  'Bonos',
                                  'Participaciones',
                                  'Aportes simples'],
                 'correcta': 'A'},
                {'pregunta': 'En la Sociedad Anónima, los socios reciben el '
                             'nombre de:',
                 'alternativas': ['Accionistas',
                                  'Titulares',
                                  'Socios colectivos',
                                  'Participacionistas',
                                  'Gestores'],
                 'correcta': 'A'},
                {'pregunta': 'En la Sociedad Anónima, la responsabilidad de '
                             'los accionistas frente a las deudas de la '
                             'empresa es:',
                 'alternativas': ['Ilimitada y personal',
                                  'Solidaria total',
                                  'Compartida con el Estado',
                                  'Limitada, sin comprometer su patrimonio '
                                  'personal',
                                  'Inexistente legalmente'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano máximo y soberano de la Sociedad '
                             'Anónima es:',
                 'alternativas': ['El Directorio',
                                  'La Junta General de Accionistas',
                                  'La Gerencia General',
                                  'El Titular',
                                  'El Consejo de Vigilancia'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['La empresa es una unidad económica de '
                                'producción de bienes o prestación de '
                                'servicios.']},
                     {'titulo': 'CARACTERÍSTICAS GENERALES',
                      'items': ['La empresa tiene un fin económico: se '
                                'organiza para generar riqueza mediante la '
                                'producción.']},
                     {'titulo': 'CLASIFICACIÓN SEGÚN EL PROPIETARIO',
                      'items': ['Las empresas privadas están constituidas '
                                'por el aporte de personas o instituciones '
                                'particulares, con fin de lucro.']},
                     {'titulo': 'CLASIFICACIÓN SEGÚN EL ASPECTO JURÍDICO',
                      'items': ['Las empresas individuales no tienen socios; '
                                'el propietario es el único que aporta el '
                                'capital.']},
                     {'titulo': 'LA EMPRESA INDIVIDUAL DE RESPONSABILIDAD '
                                'LIMITADA (EIRL)',
                      'items': ['En la EIRL, el propietario único acude al '
                                'Registro Mercantil, constituyendo una '
                                'persona jurídica con patrimonio propio.']},
                     {'titulo': 'EMPRESAS SOCIETARIAS',
                      'items': ['La sociedad civil agrupa a personas que '
                                'aportan bienes o servicios para ejercer una '
                                'profesión, como estudios de abogados.']}]},
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
                                  'Vende en el mercado',
                                  'Desea adquirir a diferentes precios',
                                  'Produce directamente',
                                  'Almacena indefinidamente'],
                 'correcta': 'C'},
                {'pregunta': 'La demanda expresa la conducta racional de:',
                 'alternativas': ['El consumidor en el mercado',
                                  'El productor',
                                  'El banco central',
                                  'El importador',
                                  'El Estado'],
                 'correcta': 'A'},
                {'pregunta': 'Para que exista demanda deben estar presentes '
                             'siempre el deseo y:',
                 'alternativas': ['La capacidad de compra',
                                  'La inflación',
                                  'La escasez absoluta',
                                  'El crédito bancario',
                                  'La publicidad'],
                 'correcta': 'A'},
                {'pregunta': 'Una persona que desea un bien pero no tiene '
                             'dinero para comprarlo es:',
                 'alternativas': ['Un demandante pleno',
                                  'Un productor',
                                  'Un oferente',
                                  'Un inversionista',
                                  'Un consumidor con necesidades, pero no '
                                  'demandante'],
                 'correcta': 'E'},
                {'pregunta': 'El factor más importante para demandar un '
                             'producto es:',
                 'alternativas': ['La publicidad',
                                  'La moda',
                                  'El color del empaque',
                                  'El precio del producto',
                                  'El clima'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando el precio de un bien disminuye, la '
                             'cantidad demandada, por regla general:',
                 'alternativas': ['Disminuye',
                                  'Desaparece',
                                  'Aumenta',
                                  'Se mantiene igual siempre',
                                  'Se vuelve negativa'],
                 'correcta': 'C'},
                {'pregunta': 'Los bienes que pueden reemplazarse el uno al '
                             'otro dando una satisfacción similar se llaman '
                             'bienes:',
                 'alternativas': ['Sustitutos',
                                  'De lujo exclusivo',
                                  'Inferiores',
                                  'Normales',
                                  'Complementarios'],
                 'correcta': 'A'},
                {'pregunta': 'El pollo y el pescado son un ejemplo típico de '
                             'bienes:',
                 'alternativas': ['Normales exclusivos',
                                  'De lujo',
                                  'Complementarios',
                                  'Sustitutos',
                                  'Inferiores exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando el aumento del precio de un bien genera '
                             'un aumento en la demanda de otro, ambos bienes '
                             'son:',
                 'alternativas': ['Independientes',
                                  'Complementarios',
                                  'Normales',
                                  'Inferiores',
                                  'Sustitutos'],
                 'correcta': 'E'},
                {'pregunta': 'Los bienes que se consumen a la vez, como los '
                             'autos y la gasolina, son bienes:',
                 'alternativas': ['Sustitutos',
                                  'Inferiores',
                                  'Normales exclusivos',
                                  'Complementarios',
                                  'De lujo'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando dos bienes son complementarios, la '
                             'disminución del precio de uno genera en la '
                             'demanda del otro:',
                 'alternativas': ['Una disminución',
                                  'Un efecto aleatorio',
                                  'Una eliminación total',
                                  'Un aumento',
                                  'Ningún efecto'],
                 'correcta': 'D'},
                {'pregunta': 'El ingreso se define como la suma de sueldos, '
                             'utilidades, intereses y:',
                 'alternativas': ['Inversiones exclusivas',
                                  'Impuestos',
                                  'Rentas',
                                  'Deudas',
                                  'Ahorros exclusivos'],
                 'correcta': 'C'},
                {'pregunta': 'La riqueza se define como el valor total de '
                             'las pertenencias de una familia, descontadas:',
                 'alternativas': ['Sus ahorros',
                                  'Sus deudas',
                                  'Sus impuestos',
                                  'Sus gastos mensuales',
                                  'Sus ingresos'],
                 'correcta': 'B'},
                {'pregunta': 'Los bienes cuya demanda aumenta cuando sube el '
                             'ingreso se llaman bienes:',
                 'alternativas': ['Normales',
                                  'Inferiores',
                                  'Complementarios exclusivos',
                                  'De primera necesidad únicamente',
                                  'Sustitutos exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Los bienes cuya demanda baja cuando el ingreso '
                             'familiar aumenta se llaman bienes:',
                 'alternativas': ['Complementarios',
                                  'Sustitutos',
                                  'Inferiores',
                                  'Normales',
                                  'De lujo exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'Los gustos y preferencias del consumidor son '
                             'un aspecto:',
                 'alternativas': ['Subjetivo, que varía según edad, sexo y '
                                  'moda',
                                  'Sin relación con la demanda',
                                  'Objetivo y fijo',
                                  'Igual para todos los consumidores',
                                  'Determinado exclusivamente por el Estado'],
                 'correcta': 'A'},
                {'pregunta': 'La demanda actual de un bien también depende '
                             'de:',
                 'alternativas': ['Solo el clima',
                                  'Solo la producción actual',
                                  'Solo el precio pasado',
                                  'Los precios futuros esperados',
                                  'Solo la publicidad pasada'],
                 'correcta': 'D'},
                {'pregunta': 'En verano aumenta la demanda de helados y '
                             'gaseosas debido al factor:',
                 'alternativas': ['Publicidad',
                                  'Precio',
                                  'Ingreso',
                                  'Riqueza',
                                  'Clima'],
                 'correcta': 'E'},
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
                 'alternativas': ['La tasa de interés',
                                  'La oferta monetaria',
                                  'Los gustos y preferencias de los '
                                  'consumidores',
                                  'El precio de mercado',
                                  'El tipo de cambio'],
                 'correcta': 'C'},
                {'pregunta': 'La elasticidad precio de la demanda mide el '
                             'grado de sensibilidad de la cantidad demandada '
                             'ante variaciones del:',
                 'alternativas': ['Clima',
                                  'Costo de producción',
                                  'Precio',
                                  'Gusto del consumidor',
                                  'Ingreso'],
                 'correcta': 'C'},
                {'pregunta': 'La elasticidad precio expresa la variación '
                             'porcentual de la cantidad demandada ante la '
                             'variación:',
                 'alternativas': ['Porcentual del precio',
                                  'Del PBI',
                                  'Absoluta del ingreso',
                                  'De la oferta monetaria',
                                  'Del tipo de cambio'],
                 'correcta': 'A'},
                {'pregunta': 'El signo de la elasticidad precio de la '
                             'demanda siempre es:',
                 'alternativas': ['Positivo',
                                  'Indefinido',
                                  'Cero',
                                  'Variable según el país',
                                  'Negativo'],
                 'correcta': 'E'},
                {'pregunta': 'Con fines prácticos, para interpretar la '
                             'elasticidad se prefiere utilizar su valor:',
                 'alternativas': ['Negativo directo',
                                  'Absoluto',
                                  'Porcentual sin signo alguno',
                                  'Relativo',
                                  'Promedio histórico'],
                 'correcta': 'B'},
                {'pregunta': 'La demanda perfectamente elástica tiene un '
                             'valor de elasticidad:',
                 'alternativas': ['Indeterminado',
                                  'Igual a uno',
                                  'Infinito',
                                  'Negativo puro',
                                  'Igual a cero'],
                 'correcta': 'C'},
                {'pregunta': 'Un bien con demanda perfectamente elástica se '
                             'caracteriza por tener:',
                 'alternativas': ['Un solo comprador',
                                  'Ningún sustituto',
                                  'Precio fijo por ley',
                                  'Gran cantidad de sustitutos perfectos',
                                  'Oferta ilimitada'],
                 'correcta': 'D'},
                {'pregunta': 'La demanda relativamente elástica tiene un '
                             'valor absoluto de elasticidad:',
                 'alternativas': ['Mayor a 1',
                                  'Igual a 1',
                                  'Igual a cero',
                                  'Negativo sin valor',
                                  'Menor a 1'],
                 'correcta': 'A'},
                {'pregunta': 'En la demanda relativamente elástica, la '
                             'cantidad demandada reacciona, frente al '
                             'precio, de forma:',
                 'alternativas': ['Más que proporcional',
                                  'Nula',
                                  'Idéntica siempre',
                                  'Aleatoria',
                                  'Menos que proporcional'],
                 'correcta': 'A'},
                {'pregunta': 'La demanda de elasticidad unitaria tiene un '
                             'valor absoluto igual a:',
                 'alternativas': ['2', 'Infinito', '0', '1', '0,5'],
                 'correcta': 'D'},
                {'pregunta': 'En la demanda unitaria, si el precio sube 1%, '
                             'la cantidad demandada se reduce en:',
                 'alternativas': ['Ninguna variación',
                                  '10%',
                                  '2%',
                                  '0,5%',
                                  '1%'],
                 'correcta': 'E'},
                {'pregunta': 'La demanda relativamente inelástica tiene un '
                             'valor absoluto de elasticidad:',
                 'alternativas': ['Menor a 1',
                                  'Infinito',
                                  'Mayor a 1',
                                  'Igual a 1',
                                  'Negativo puro'],
                 'correcta': 'A'},
                {'pregunta': 'En la demanda relativamente inelástica, la '
                             'cantidad demandada reacciona ante el precio de '
                             'forma:',
                 'alternativas': ['Inversa exacta',
                                  'Más que proporcional',
                                  'Menos que proporcional',
                                  'Idéntica al precio',
                                  'Nula'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['La demanda es la cantidad de bienes y '
                                'servicios que un comprador puede y desea '
                                'adquirir a diferentes niveles de precios.']},
                     {'titulo': 'EL PRECIO DEL PRODUCTO',
                      'items': ['El precio del producto es el factor más '
                                'importante para demandar un bien.']},
                     {'titulo': 'BIENES SUSTITUTOS Y COMPLEMENTARIOS',
                      'items': ['Los bienes sustitutos pueden reemplazarse '
                                'el uno al otro, dando una satisfacción '
                                'similar, como el pollo y el pescado.']},
                     {'titulo': 'INGRESO, RIQUEZA Y OTROS FACTORES',
                      'items': ['El ingreso es la suma de sueldos, '
                                'utilidades, intereses y rentas que recibe '
                                'una persona en un periodo.']},
                     {'titulo': 'ELASTICIDAD PRECIO DE LA DEMANDA',
                      'items': ['La elasticidad precio de la demanda mide el '
                                'grado de sensibilidad de la cantidad '
                                'demandada ante variaciones del precio.']},
                     {'titulo': 'TIPOS DE ELASTICIDAD PRECIO',
                      'items': ['La demanda perfectamente elástica tiene un '
                                'valor de elasticidad infinito; el bien '
                                'tiene sustitutos perfectos.']}]},
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
                                  'Importar exclusivamente',
                                  'Almacenar indefinidamente',
                                  'Vender a diversos precios',
                                  'Regalar'],
                 'correcta': 'D'},
                {'pregunta': 'La oferta refleja el comportamiento de:',
                 'alternativas': ['El Estado exclusivamente',
                                  'Los consumidores',
                                  'Los vendedores o productores',
                                  'Los bancos',
                                  'Los importadores'],
                 'correcta': 'C'},
                {'pregunta': 'Un precio elevado motiva a los ofertantes a:',
                 'alternativas': ['Producir y vender más',
                                  'Producir y vender menos',
                                  'Reducir la calidad',
                                  'Cerrar la empresa',
                                  'Dejar de producir'],
                 'correcta': 'A'},
                {'pregunta': 'Los costos de producción dependen de los '
                             'precios de los insumos, la mano de obra y:',
                 'alternativas': ['Los impuestos',
                                  'El clima exclusivamente',
                                  'El tipo de cambio exclusivamente',
                                  'La publicidad',
                                  'La moda'],
                 'correcta': 'A'},
                {'pregunta': 'Un campesino elegirá producir el cultivo que '
                             'le genere:',
                 'alternativas': ['Ningún beneficio',
                                  'Solo prestigio social',
                                  'Buenas ganancias',
                                  'Solo cubrir costos',
                                  'Pérdidas mínimas'],
                 'correcta': 'C'},
                {'pregunta': 'Los productos que pueden fabricarse '
                             'indistintamente con los mismos factores de '
                             'producción se llaman productos:',
                 'alternativas': ['Inferiores',
                                  'Normales',
                                  'Sustitutos en demanda',
                                  'Complementarios',
                                  'Alternativos'],
                 'correcta': 'E'},
                {'pregunta': 'El pan, los bizcochos y los panetones son '
                             'ejemplos de productos:',
                 'alternativas': ['De lujo',
                                  'Inferiores',
                                  'Sustitutos en la demanda',
                                  'Alternativos en la producción',
                                  'Complementarios en la producción'],
                 'correcta': 'D'},
                {'pregunta': 'Los productos que se producen como un lote '
                             'conjunto se llaman productos:',
                 'alternativas': ['Complementarios en la producción',
                                  'Normales',
                                  'Alternativos',
                                  'Sustitutos',
                                  'Inferiores'],
                 'correcta': 'A'},
                {'pregunta': 'La lana y la carne de oveja son un ejemplo de '
                             'productos:',
                 'alternativas': ['Complementarios en la producción',
                                  'Alternativos',
                                  'Sustitutos en demanda',
                                  'De lujo',
                                  'Inferiores'],
                 'correcta': 'A'},
                {'pregunta': 'Si sube el precio del petróleo, la producción '
                             'de kerosene tiende a:',
                 'alternativas': ['Disminuir',
                                  'Volverse negativa',
                                  'Desaparecer',
                                  'Aumentar',
                                  'Mantenerse igual siempre'],
                 'correcta': 'D'},
                {'pregunta': 'La expectativa de los ofertantes respecto a '
                             'los precios futuros se llama:',
                 'alternativas': ['Precio actual',
                                  'Demanda derivada',
                                  'Precios esperados del bien',
                                  'Elasticidad',
                                  'Costo de producción'],
                 'correcta': 'C'},
                {'pregunta': 'Si los ofertantes esperan una caída del precio '
                             'futuro, tienden a:',
                 'alternativas': ['Aumentar precios actuales sin producir '
                                  'más',
                                  'Incrementar la producción actual',
                                  'Detener toda producción',
                                  'Reducir la producción actual',
                                  'Cerrar el negocio'],
                 'correcta': 'B'},
                {'pregunta': 'Las sequías e inundaciones son ejemplos del '
                             'factor:',
                 'alternativas': ['Precios esperados',
                                  'Costos de producción',
                                  'Políticas económicas',
                                  'Condiciones climáticas',
                                  'Precio del bien'],
                 'correcta': 'D'},
                {'pregunta': 'Las condiciones climáticas adversas, como '
                             'sequías, provocan que la oferta:',
                 'alternativas': ['Se duplique',
                                  'Se mantenga constante siempre',
                                  'Aumente',
                                  'Desaparezca por completo',
                                  'Se reduzca'],
                 'correcta': 'E'},
                {'pregunta': 'Las políticas económicas liberales, al reducir '
                             'impuestos a bienes importados, generan:',
                 'alternativas': ['Reducción de las importaciones',
                                  'Aumento de aranceles',
                                  'Disminución de la oferta',
                                  'Aumento de la oferta por mayores '
                                  'importaciones',
                                  'Ningún cambio en la oferta'],
                 'correcta': 'D'},
                {'pregunta': 'Las políticas proteccionistas, al elevar '
                             'aranceles, tienden a:',
                 'alternativas': ['No afectar la oferta',
                                  'Bajar los precios internos siempre',
                                  'Reducir la oferta de bienes importados',
                                  'Aumentar la oferta de importados',
                                  'Eliminar toda importación totalmente'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los factores que afectan la oferta se '
                             'consideran también las expectativas de:',
                 'alternativas': ['El gobierno exclusivamente',
                                  'Los bancos centrales',
                                  'Los empresarios',
                                  'Los consumidores exclusivamente',
                                  'Los organismos internacionales'],
                 'correcta': 'C'},
                {'pregunta': 'En una carpintería, la producción de mesas, '
                             'camas y sillas ejemplifica productos:',
                 'alternativas': ['Alternativos en la producción',
                                  'Complementarios',
                                  'De lujo',
                                  'Sustitutos en demanda',
                                  'Inferiores'],
                 'correcta': 'A'},
                {'pregunta': 'El precio de un bien va acompañado del margen '
                             'de:',
                 'alternativas': ['Descuento fijo',
                                  'Ganancia del productor',
                                  'Impuesto único',
                                  'Subsidio estatal',
                                  'Pérdida'],
                 'correcta': 'B'},
                {'pregunta': 'La oferta expresa, en esencia, los deseos de '
                             'venta o producción en función de:',
                 'alternativas': ['Los gustos del consumidor',
                                  'El clima únicamente',
                                  'La moda del momento',
                                  'La publicidad exclusivamente',
                                  'Los distintos precios existentes en el '
                                  'mercado'],
                 'correcta': 'E'},
                {'pregunta': 'El equilibrio del mercado se define como la '
                             'situación en que el nivel de oferta coincide '
                             'con el nivel de:',
                 'alternativas': ['Exportaciones',
                                  'Inversión pública',
                                  'Consumo o demanda',
                                  'Producción industrial',
                                  'Importaciones'],
                 'correcta': 'C'},
                {'pregunta': 'En el equilibrio de mercado, la cantidad '
                             'ofertada es:',
                 'alternativas': ['Cero',
                                  'Independiente de la demanda',
                                  'Menor que la demandada siempre',
                                  'Mayor que la demandada siempre',
                                  'Igual a la cantidad demandada'],
                 'correcta': 'E'},
                {'pregunta': 'La cantidad en que coinciden las decisiones de '
                             'ofertantes y demandantes se llama:',
                 'alternativas': ['Cantidad máxima',
                                  'Cantidad neta',
                                  'Cantidad óptima',
                                  'Cantidad de equilibrio',
                                  'Cantidad mínima'],
                 'correcta': 'D'},
                {'pregunta': 'El precio en el cual la cantidad ofertada es '
                             'igual a la cantidad demandada se llama:',
                 'alternativas': ['Precio sombra',
                                  'Precio máximo',
                                  'Precio de mercado libre',
                                  'Precio mínimo',
                                  'Precio de equilibrio'],
                 'correcta': 'E'},
                {'pregunta': 'Gráficamente, el equilibrio del mercado se '
                             'forma en:',
                 'alternativas': ['El punto más bajo de la curva de demanda',
                                  'El origen de coordenadas',
                                  'La intersección de las curvas de oferta y '
                                  'demanda',
                                  'Un punto fuera del gráfico',
                                  'El punto más alto de la curva de oferta'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando el precio está por debajo del '
                             'equilibrio, se genera una situación de:',
                 'alternativas': ['Estabilidad total',
                                  'Escasez',
                                  'Sobreproducción',
                                  'Equilibrio perfecto',
                                  'Abundancia'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando hay escasez en el mercado, la presión '
                             'sobre el precio es:',
                 'alternativas': ['A la baja',
                                  'Indeterminada',
                                  'Negativa',
                                  'Nula',
                                  'Al alza'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando el precio está por encima del '
                             'equilibrio, se genera una situación de:',
                 'alternativas': ['Escasez',
                                  'Equilibrio estable',
                                  'Déficit',
                                  'Inflación directa',
                                  'Abundancia o sobreproducción'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando hay abundancia en el mercado, la '
                             'presión sobre el precio es:',
                 'alternativas': ['Estable siempre',
                                  'Al alza',
                                  'Indefinida',
                                  'A la baja',
                                  'Nula'],
                 'correcta': 'D'},
                {'pregunta': 'En el punto de equilibrio, se vende todo lo '
                             'que se ofrece y se puede comprar:',
                 'alternativas': ['Nada en absoluto',
                                  'El doble de lo ofertado',
                                  'Solo productos de lujo',
                                  'Solo una parte de lo demandado',
                                  'Todo lo que se desea demandar'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['La oferta es la cantidad de un bien o '
                                'servicio que los vendedores-productores '
                                'están dispuestos a vender a diversos '
                                'niveles de precios.']},
                     {'titulo': 'EL PRECIO Y LOS COSTOS DE PRODUCCIÓN',
                      'items': ['Un precio elevado motiva a los ofertantes a '
                                'producir y vender más.']},
                     {'titulo': 'BIENES ALTERNATIVOS Y COMPLEMENTARIOS EN LA '
                                'PRODUCCIÓN',
                      'items': ['Los productos alternativos pueden '
                                'producirse indistintamente con los mismos '
                                'factores, como el pan y los panetones.']},
                     {'titulo': 'OTROS FACTORES QUE AFECTAN LA OFERTA',
                      'items': ['Los precios esperados del bien son la '
                                'expectativa de los ofertantes respecto a '
                                'los precios futuros.']},
                     {'titulo': 'EL EQUILIBRIO DEL MERCADO',
                      'items': ['El equilibrio del mercado es la situación '
                                'en la que el nivel de producción (oferta) '
                                'coincide con el nivel de consumo '
                                '(demanda).']}]},
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
                           'competencia monopolística.']}],
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
                 'alternativas': ['Tributación',
                                  'Compra y venta',
                                  'Producción exclusiva',
                                  'Ahorro únicamente',
                                  'Emisión monetaria'],
                 'correcta': 'B'},
                {'pregunta': 'Los componentes de la estructura de mercado '
                             'son oferta, demanda, precio y:',
                 'alternativas': ['Inflación',
                                  'El tipo de cambio',
                                  'El nivel de equilibrio',
                                  'El PBI',
                                  'La tasa de interés'],
                 'correcta': 'C'},
                {'pregunta': 'Para los servicios, el precio se denomina:',
                 'alternativas': ['Dividendo',
                                  'Costo',
                                  'Salario',
                                  'Tarifa',
                                  'Interés'],
                 'correcta': 'D'},
                {'pregunta': 'Para que se constituya un mercado, la '
                             'presencia física de compradores y vendedores '
                             'es:',
                 'alternativas': ['Imposible sin ella',
                                  'Requisito único',
                                  'Exigida por ley',
                                  'Siempre obligatoria',
                                  'No necesariamente obligatoria'],
                 'correcta': 'E'},
                {'pregunta': 'Todo mercado obedece al comportamiento de las '
                             'leyes económicas de:',
                 'alternativas': ['La oferta y la demanda',
                                  'La inflación exclusivamente',
                                  'El PBI',
                                  'La tasa de interés',
                                  'El tipo de cambio'],
                 'correcta': 'A'},
                {'pregunta': 'Los mercados cuyo ámbito es una ciudad, '
                             'distrito o provincia se llaman mercados:',
                 'alternativas': ['Locales',
                                  'Regionales externos',
                                  'Internacionales',
                                  'Nacionales',
                                  'Mayoristas'],
                 'correcta': 'A'},
                {'pregunta': 'Los mercados que abarcan varias regiones '
                             'dentro de un mismo país se llaman mercados:',
                 'alternativas': ['Locales',
                                  'Regionales externos',
                                  'Internacionales',
                                  'Regionales internos',
                                  'Nacionales exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los mercados que abarcan más de dos países '
                             'mediante acuerdos comerciales se llaman '
                             'mercados:',
                 'alternativas': ['De insumos',
                                  'Regionales externos',
                                  'Nacionales',
                                  'Locales',
                                  'Regionales internos'],
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
                 'alternativas': ['Solo gobiernos locales',
                                  'Solo un país',
                                  'Ningún organismo',
                                  'Solo bancos privados',
                                  'La Organización Mundial de Comercio '
                                  '(OMC)'],
                 'correcta': 'E'},
                {'pregunta': 'El mercado que abarca todo el espacio '
                             'geográfico de un país se llama mercado:',
                 'alternativas': ['Nacional',
                                  'Regional interno',
                                  'Mayorista exclusivo',
                                  'Internacional',
                                  'Local'],
                 'correcta': 'A'},
                {'pregunta': 'El mercado caracterizado por libre ingreso y '
                             'salida de vendedores, sin poder de fijación de '
                             'precios, es de:',
                 'alternativas': ['Competencia perfecta',
                                  'Competencia imperfecta',
                                  'Oligopolio',
                                  'Monopsonio',
                                  'Monopolio puro'],
                 'correcta': 'A'},
                {'pregunta': 'El mercado caracterizado por barreras de '
                             'ingreso y poder para fijar precios es de:',
                 'alternativas': ['Mercado local exclusivo',
                                  'Competencia imperfecta',
                                  'Ninguno de los anteriores',
                                  'Competencia perfecta',
                                  'Libre concurrencia total'],
                 'correcta': 'B'},
                {'pregunta': 'La competencia imperfecta comprende, entre '
                             'otras formas, al monopolio, al oligopolio y a '
                             'la competencia:',
                 'alternativas': ['Local',
                                  'Regional',
                                  'Interna exclusiva',
                                  'Perfecta',
                                  'Monopolística'],
                 'correcta': 'E'},
                {'pregunta': 'En un mercado de competencia imperfecta con '
                             'monopolio, quien fija el precio es:',
                 'alternativas': ['El Estado siempre',
                                  'El monopolista',
                                  'Un organismo neutral',
                                  'El mercado internacional',
                                  'El consumidor'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado de trabajo, el precio del factor '
                             'trabajo se fija como:',
                 'alternativas': ['Sueldo o salario',
                                  'Dividendo',
                                  'Interés',
                                  'Renta',
                                  'Tarifa'],
                 'correcta': 'A'},
                {'pregunta': 'En el mercado de capitales, el precio del '
                             'factor capital se fija como:',
                 'alternativas': ['Renta agrícola',
                                  'Salario',
                                  'Impuesto',
                                  'Tarifa de servicio',
                                  'Tasa de interés'],
                 'correcta': 'E'},
                {'pregunta': 'Los mercados donde se transan grandes '
                             'volúmenes de bienes en poco tiempo, con '
                             'precios más bajos, se llaman mercados:',
                 'alternativas': ['De insumos',
                                  'Locales exclusivos',
                                  'Mayoristas',
                                  'Minoristas',
                                  'De capitales'],
                 'correcta': 'C'},
                {'pregunta': 'Toda transacción económica realizada en un '
                             'mercado insume:',
                 'alternativas': ['Solo un instante siempre',
                                  'Tiempo infinito',
                                  'Ningún tiempo',
                                  'Un periodo fijo de un año',
                                  'Un determinado periodo de tiempo'],
                 'correcta': 'E'},
                {'pregunta': 'El mercado, según la ciencia económica, '
                             'determina y fija:',
                 'alternativas': ['Solo la inflación',
                                  'Los precios',
                                  'Solo los salarios',
                                  'Solo los impuestos',
                                  'Solo el tipo de cambio'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y COMPONENTES',
                      'items': ['El mercado es el espacio donde interactúan '
                                'las unidades económicas en las '
                                'transacciones de compra y venta, generando '
                                'oferta y demanda.']},
                     {'titulo': 'CARACTERÍSTICAS DEL MERCADO',
                      'items': ['El mercado no requiere necesariamente la '
                                'presencia física de compradores y '
                                'vendedores.']},
                     {'titulo': 'CLASIFICACIÓN SEGÚN EL ÁREA GEOGRÁFICA',
                      'items': ['Los mercados locales abarcan un espacio '
                                'restringido, como una ciudad o provincia.']},
                     {'titulo': 'CLASIFICACIÓN SEGÚN EL NÚMERO DE VENDEDORES',
                      'items': ['El mercado de competencia perfecta se '
                                'caracteriza por libre ingreso y salida, sin '
                                'poder de fijación de precios.']}]},
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
                 'alternativas': ['Unidad de cuenta',
                                  'Depósito de valor',
                                  'Ninguna en particular',
                                  'Medio de pago o de cambio',
                                  'Patrón de pagos diferidos'],
                 'correcta': 'D'},
                {'pregunta': 'La función del dinero que permite estimar el '
                             'valor de los demás bienes se llama:',
                 'alternativas': ['Patrón de pagos diferidos',
                                  'Medio de pago',
                                  'Depósito de valor',
                                  'Unidad de cuenta o medida de valor',
                                  'Reserva internacional'],
                 'correcta': 'D'},
                {'pregunta': 'En el Perú, la unidad de cuenta es:',
                 'alternativas': ['El nuevo sol',
                                  'El peso',
                                  'El dólar',
                                  'La libra',
                                  'El euro'],
                 'correcta': 'A'},
                {'pregunta': 'La función del dinero que permite conservar '
                             'poder adquisitivo para el futuro se llama:',
                 'alternativas': ['Unidad de cuenta',
                                  'Medio de pago',
                                  'Ninguna',
                                  'Patrón de pagos diferidos',
                                  'Depósito de valor'],
                 'correcta': 'E'},
                {'pregunta': 'La función que permite realizar pagos a '
                             'futuro, como compras al crédito, se llama:',
                 'alternativas': ['Reserva de emergencia',
                                  'Unidad de cuenta',
                                  'Medio de pago',
                                  'Depósito de valor',
                                  'Patrón de pagos diferidos'],
                 'correcta': 'E'},
                {'pregunta': 'La capacidad de compra que tiene el dinero se '
                             'llama:',
                 'alternativas': ['Elasticidad',
                                  'Homogeneidad',
                                  'Estabilidad',
                                  'Divisibilidad',
                                  'Poder adquisitivo'],
                 'correcta': 'E'},
                {'pregunta': 'Que el dinero mantenga su poder adquisitivo en '
                             'el tiempo corresponde a la característica de:',
                 'alternativas': ['Estabilidad',
                                  'Divisibilidad',
                                  'Durabilidad',
                                  'Poder adquisitivo',
                                  'Elasticidad'],
                 'correcta': 'A'},
                {'pregunta': 'La inflación hace que el dinero pierda:',
                 'alternativas': ['Divisibilidad',
                                  'Homogeneidad',
                                  'Durabilidad',
                                  'Estabilidad',
                                  'Elasticidad'],
                 'correcta': 'D'},
                {'pregunta': 'Que la unidad monetaria tenga múltiplos y '
                             'submúltiplos corresponde a la característica '
                             'de:',
                 'alternativas': ['Elasticidad',
                                  'Divisibilidad',
                                  'Durabilidad',
                                  'Homogeneidad',
                                  'Poder adquisitivo'],
                 'correcta': 'B'},
                {'pregunta': 'Que los billetes de igual denominación tengan '
                             'las mismas características corresponde a la '
                             'característica de:',
                 'alternativas': ['Durabilidad',
                                  'Estabilidad',
                                  'Homogeneidad',
                                  'Divisibilidad',
                                  'Elasticidad'],
                 'correcta': 'C'},
                {'pregunta': 'Que el dinero esté hecho de material '
                             'resistente corresponde a la característica de:',
                 'alternativas': ['Durabilidad',
                                  'Elasticidad',
                                  'Poder adquisitivo',
                                  'Divisibilidad',
                                  'Homogeneidad'],
                 'correcta': 'A'},
                {'pregunta': 'La facilidad de la autoridad monetaria para '
                             'aumentar o disminuir la cantidad de dinero se '
                             'llama:',
                 'alternativas': ['Elasticidad',
                                  'Homogeneidad',
                                  'Estabilidad',
                                  'Divisibilidad',
                                  'Durabilidad'],
                 'correcta': 'A'},
                {'pregunta': 'La autoridad monetaria del Perú, encargada de '
                             'la elasticidad del dinero, es:',
                 'alternativas': ['El Congreso',
                                  'La SUNAT',
                                  'El MEF',
                                  'La SBS',
                                  'El Banco Central de Reserva (BCR)'],
                 'correcta': 'E'},
                {'pregunta': 'El valor que tiene el dinero por sí mismo se '
                             'llama valor:',
                 'alternativas': ['Nominal exclusivo',
                                  'De cambio exclusivo',
                                  'Extrínseco',
                                  'Intrínseco',
                                  'De mercado'],
                 'correcta': 'D'},
                {'pregunta': 'El valor intrínseco se subdivide en valor real '
                             'y valor:',
                 'alternativas': ['De cambio',
                                  'De mercado',
                                  'Nominal o legal',
                                  'De uso',
                                  'Extrínseco'],
                 'correcta': 'C'},
                {'pregunta': 'El valor real del dinero viene dado por:',
                 'alternativas': ['Su capacidad de compra',
                                  'Su valor de cambio en el mercado',
                                  'El costo de fabricación del dinero',
                                  'El tipo de cambio',
                                  'La inflación acumulada'],
                 'correcta': 'C'},
                {'pregunta': 'El valor establecido por la autoridad '
                             'monetaria e impreso en la moneda se llama '
                             'valor:',
                 'alternativas': ['Extrínseco',
                                  'De cambio',
                                  'De mercado',
                                  'Real',
                                  'Nominal o legal'],
                 'correcta': 'E'},
                {'pregunta': 'El valor de cambio del dinero, expresado en su '
                             'capacidad de compra en el mercado, se llama '
                             'valor:',
                 'alternativas': ['Real',
                                  'Extrínseco',
                                  'Nominal',
                                  'Intrínseco',
                                  'De fabricación'],
                 'correcta': 'B'},
                {'pregunta': 'Según su naturaleza, el dinero puede ser '
                             'metálico o:',
                 'alternativas': ['Solo virtual',
                                  'Solo bancario',
                                  'De papel',
                                  'Solo electrónico',
                                  'Digital exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'El dinero metálico tipo, acuñado con oro o '
                             'plata, tiene un poder cancelatorio:',
                 'alternativas': ['Nulo',
                                  'Solo simbólico',
                                  'Ilimitado',
                                  'Temporal exclusivo',
                                  'Limitado'],
                 'correcta': 'C'},
                {'pregunta': 'La inflación se define como un incremento '
                             'generalizado y continuo de:',
                 'alternativas': ['Precios',
                                  'Exportaciones',
                                  'Salarios',
                                  'Impuestos',
                                  'Ahorros'],
                 'correcta': 'A'},
                {'pregunta': 'La inflación equivale a la desvalorización de:',
                 'alternativas': ['El PBI',
                                  'Los salarios exclusivamente',
                                  'Los bienes de capital',
                                  'Las exportaciones',
                                  'La moneda'],
                 'correcta': 'E'},
                {'pregunta': 'Una caída generalizada y continua de precios '
                             'se llama:',
                 'alternativas': ['Deflación',
                                  'Estanflación',
                                  'Devaluación',
                                  'Hiperinflación',
                                  'Recesión'],
                 'correcta': 'A'},
                {'pregunta': 'La inflación se mide oficialmente por la '
                             'variación del:',
                 'alternativas': ['Índice de desarrollo humano',
                                  'Índice de Precios al Consumidor (IPC)',
                                  'PBI nominal',
                                  'Salario mínimo',
                                  'Tipo de cambio'],
                 'correcta': 'B'},
                {'pregunta': 'El IPC mide el nivel de variación mensual de '
                             'los precios de:',
                 'alternativas': ['Solo insumos industriales',
                                  'Solo bienes exportados',
                                  'La canasta familiar de bienes y servicios',
                                  'Solo bienes importados',
                                  'Solo bienes de lujo'],
                 'correcta': 'C'},
                {'pregunta': 'La tasa de inflación es el cambio porcentual '
                             'del nivel de precios, generalmente medido en:',
                 'alternativas': ['Un mes',
                                  'Un semestre exclusivo',
                                  'Una década',
                                  'Un día',
                                  'Un lustro'],
                 'correcta': 'A'},
                {'pregunta': 'La inflación moderada se presenta cuando los '
                             'precios suben en un rango de:',
                 'alternativas': ['0% a 10% anual',
                                  '10% a 1000% anual',
                                  'Solo 50% mensual',
                                  'Más de 1000% anual',
                                  'Ningún rango definido'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación con tasa porcentual de un solo '
                             'dígito se llama inflación:',
                 'alternativas': ['Importada',
                                  'Galopante',
                                  'Moderada',
                                  'Hiperinflación',
                                  'Estructural'],
                 'correcta': 'C'},
                {'pregunta': 'La inflación galopante varía en un rango de:',
                 'alternativas': ['Solo negativo',
                                  'Más de 5000% anual',
                                  '10% a 1000% anual',
                                  '0% exacto',
                                  '0% a 10% anual'],
                 'correcta': 'C'},
                {'pregunta': 'La hiperinflación se caracteriza por superar '
                             'un incremento anual de:',
                 'alternativas': ['50%', '100%', '10%', '5%', '1000%'],
                 'correcta': 'E'},
                {'pregunta': 'La hiperinflación también puede medirse cuando '
                             'supera un incremento mensual de:',
                 'alternativas': ['50%', '500%', '5%', '1%', '10%'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las consecuencias de la inflación figura '
                             'la pérdida del poder:',
                 'alternativas': ['Judicial',
                                  'Adquisitivo del dinero',
                                  'Legislativo',
                                  'Electoral',
                                  'Ejecutivo'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación provoca que el salario real:',
                 'alternativas': ['Se duplique',
                                  'Se mantenga igual siempre',
                                  'Desaparezca',
                                  'Aumente siempre',
                                  'Disminuya'],
                 'correcta': 'E'},
                {'pregunta': 'Un fenómeno que ocurre en economías con alta '
                             'inflación es la creciente sustitución de la '
                             'moneda local por moneda extranjera, llamada:',
                 'alternativas': ['Estatización',
                                  'Dolarización',
                                  'Nacionalización monetaria',
                                  'Euroización',
                                  'Regionalización'],
                 'correcta': 'B'},
                {'pregunta': 'La inflación provoca, entre otras '
                             'consecuencias, la disminución del:',
                 'alternativas': ['Ahorro',
                                  'Comercio exterior',
                                  'Tipo de cambio',
                                  'Consumo exclusivo',
                                  'Gasto público'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'FUNCIONES DEL DINERO',
                      'items': ['La función de medio de pago o de cambio es '
                                'la más importante del dinero, y facilita '
                                'las transacciones comerciales.']},
                     {'titulo': 'CARACTERÍSTICAS DEL DINERO',
                      'items': ['El poder adquisitivo es la capacidad de '
                                'compra que tiene el dinero.']},
                     {'titulo': 'VALORES DEL DINERO',
                      'items': ['El valor intrínseco es el valor que tiene '
                                'el dinero por sí mismo, y se subdivide en '
                                'valor real y valor nominal.']},
                     {'titulo': 'CLASES DE DINERO',
                      'items': ['Según su naturaleza, el dinero puede ser '
                                'metálico o de papel.']},
                     {'titulo': 'LA INFLACIÓN: CONCEPTO Y MEDICIÓN',
                      'items': ['La inflación es un incremento generalizado '
                                'y continuo de precios, equivalente a la '
                                'desvalorización de la moneda.']},
                     {'titulo': 'CLASES DE INFLACIÓN',
                      'items': ['La inflación moderada tiene precios que '
                                'suben entre 0% y 10% anual, con tasa de un '
                                'dígito.']},
                     {'titulo': 'CONSECUENCIAS DE LA INFLACIÓN',
                      'items': ['Entre las consecuencias de la inflación '
                                'están la pérdida del poder adquisitivo, la '
                                'disminución del salario real, y la '
                                'dolarización de la economía.']}]},
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
                {'titulo': '13.5 CLASIFICACIÓN DE LOS BANCOS',
                 'items': ['La {banca privada}, o banca múltiple, está '
                           'autorizada a realizar operaciones activas, '
                           'pasivas y {neutras} o servicios.',
                           'La {banca privada nacional} está conformada con '
                           'capitales de inversionistas de nacionalidad '
                           'peruana.',
                           'El {Banco de Crédito del Perú} cuenta con '
                           'participación mayoritaria de capitales '
                           'nacionales; su principal accionista es el Grupo '
                           '{Romero}.',
                           'La {banca privada extranjera} tiene '
                           'participación de inversionistas extranjeros; '
                           'algunas son solo sucursales con casa matriz en '
                           '{Estados Unidos} y Europa.',
                           'La {banca estatal} peruana está formada por el '
                           'Banco de la {Nación} y el Banco Central de '
                           '{Reserva} del Perú.',
                           'El {Banco de la Nación} es el agente financiero '
                           'del Estado, encargado de las actividades '
                           'financieras del sector {público}.',
                           'El antecedente del Banco de la Nación es la '
                           '{Caja de Depósitos y Consignaciones}, creada en '
                           '{1905}.',
                           'El Banco de la Nación fue creado el {27} de '
                           'enero de {1966}, mediante ley aprobada por el '
                           'Congreso.']},
                {'titulo': '13.6 LA EMPRESA BANCARIA',
                 'items': ['El {banco} es una empresa que actúa como '
                           'intermediario {indirecto} en el mercado '
                           'monetario, captando dinero del público.',
                           'La función más importante del banco es la '
                           '{función social}: apoyar sectores retardatarios '
                           'mediante préstamos, creando {empleo}.',
                           'Los bancos también apoyan al {BCR} en regular y '
                           'facilitar la moneda en circulación.']},
                {'titulo': '13.7 OPERACIONES BANCARIAS: PASIVAS',
                 'items': ['Las {operaciones pasivas} son los fondos '
                           'depositados por los clientes, que el banco usa '
                           'para sus operaciones {activas}.',
                           'El {depósito a la vista}, o cuenta corriente, '
                           'permite depósitos y retiros mediante {cheques}.',
                           'El {depósito a plazo} o a término implica dejar '
                           'el dinero por un tiempo determinado, sin poder '
                           'retirarlo antes.',
                           'El depósito de {CTS} (Compensación por Tiempo de '
                           'Servicios) es un fondo obligatorio del empleador '
                           'que sirve como seguro de {desempleo}.']},
                {'titulo': '13.8 OPERACIONES BANCARIAS: ACTIVAS',
                 'items': ['Las {operaciones activas} son aquellas en las '
                           'que el banco otorga {crédito}: préstamos, '
                           'descuentos, anticipos.',
                           'El {préstamo} es la operación mediante la cual '
                           'el banco coloca su liquidez, cobrando una tasa '
                           'de interés {activa}.',
                           'El {sobregiro bancario} ocurre cuando el cliente '
                           'gira cheques sin provisión de fondos suficiente '
                           'en su cuenta.']}],
  'cuadros': [{'titulo': '13.2 MERCADO PRIMARIO FRENTE A SECUNDARIO',
               'encabezados': ['Mercado', 'Función'],
               'filas': [['{Primario}', 'Primera {colocación} de valores'],
                         ['{Secundario}',
                          '{Reventa} de valores, da liquidez']]}],
  'preguntas': [{'pregunta': 'La intermediación financiera es el proceso que '
                             'traslada recursos de los agentes '
                             'superavitarios hacia los agentes:',
                 'alternativas': ['Deficitarios',
                                  'Extranjeros exclusivamente',
                                  'Bancarios exclusivamente',
                                  'Internacionales',
                                  'Estatales'],
                 'correcta': 'A'},
                {'pregunta': 'En la intermediación financiera directa, el '
                             'riesgo lo asume directamente:',
                 'alternativas': ['Ningún agente',
                                  'El Estado',
                                  'Un banco comercial intermediario',
                                  'El agente superavitario',
                                  'El Banco Central'],
                 'correcta': 'D'},
                {'pregunta': 'En la intermediación directa se negocian '
                             'títulos valores como bonos y:',
                 'alternativas': ['Solo cheques',
                                  'Solo efectivo',
                                  'Acciones',
                                  'Monedas extranjeras',
                                  'Solo letras de cambio'],
                 'correcta': 'C'},
                {'pregunta': 'Los bonos son instrumentos de renta:',
                 'alternativas': ['Mixta obligatoria',
                                  'Nula',
                                  'Variable',
                                  'Fija',
                                  'Indeterminada'],
                 'correcta': 'D'},
                {'pregunta': 'Las acciones son instrumentos de renta:',
                 'alternativas': ['Garantizada siempre',
                                  'Indeterminada',
                                  'Fija',
                                  'Variable',
                                  'Nula'],
                 'correcta': 'D'},
                {'pregunta': 'El mercado donde se colocan por primera vez '
                             'los valores emitidos se llama mercado:',
                 'alternativas': ['De divisas',
                                  'Informal',
                                  'Secundario',
                                  'Primario',
                                  'Cambiario'],
                 'correcta': 'D'},
                {'pregunta': 'El mercado donde se revenden los valores ya '
                             'adquiridos se llama mercado:',
                 'alternativas': ['Primario',
                                  'Secundario',
                                  'De futuros exclusivo',
                                  'Cambiario',
                                  'Informal'],
                 'correcta': 'B'},
                {'pregunta': 'La existencia del mercado secundario permite '
                             'dar a los valores:',
                 'alternativas': ['Menor rentabilidad',
                                  'Liquidez',
                                  'Menor variedad',
                                  'Ninguna ventaja',
                                  'Mayor riesgo únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'En el mercado primario, el medio de contacto '
                             'se da a través de:',
                 'alternativas': ['Las AFP',
                                  'Las sociedades agentes de bolsa',
                                  'Los bancos de inversión',
                                  'El BCR exclusivamente',
                                  'La SUNAT'],
                 'correcta': 'C'},
                {'pregunta': 'En el mercado secundario, el medio de contacto '
                             'se da a través de:',
                 'alternativas': ['Las sociedades agentes de bolsa',
                                  'El MEF',
                                  'El BCR',
                                  'Los bancos de inversión',
                                  'La SUNAT'],
                 'correcta': 'A'},
                {'pregunta': 'Una ventaja de la intermediación directa es '
                             'que los costos de operación son:',
                 'alternativas': ['Menores para ambos agentes',
                                  'Inexistentes',
                                  'Mayores para ambos agentes',
                                  'Solo a cargo del Estado',
                                  'Iguales siempre'],
                 'correcta': 'A'},
                {'pregunta': 'La intermediación directa permite al agente '
                             'deficitario acceder a grandes sumas de dinero:',
                 'alternativas': ['Nunca',
                                  'Solo con aval estatal',
                                  'Solo mediante subastas',
                                  'Solo prendando todos sus activos',
                                  'Por lo general sin prendar sus activos'],
                 'correcta': 'E'},
                {'pregunta': 'Los instrumentos de renta fija generan el pago '
                             'fijo de intereses y la devolución de:',
                 'alternativas': ['Los dividendos',
                                  'El capital',
                                  'El tipo de cambio',
                                  'Las acciones',
                                  'Las utilidades variables'],
                 'correcta': 'B'},
                {'pregunta': 'Los instrumentos de renta variable dan al '
                             'inversionista derecho al patrimonio de:',
                 'alternativas': ['El Banco Central',
                                  'La empresa emisora',
                                  'La SUNAT',
                                  'El Estado',
                                  'Ningún ente en particular'],
                 'correcta': 'B'},
                {'pregunta': 'Los bonos corporativos y las letras '
                             'hipotecarias son instrumentos de renta fija '
                             'de:',
                 'alternativas': ['Un solo día',
                                  'Plazo indefinido',
                                  'Largo plazo',
                                  'Ninguna duración fija',
                                  'Corto plazo'],
                 'correcta': 'C'},
                {'pregunta': 'Los pagarés y las letras de cambio son '
                             'instrumentos de renta fija de:',
                 'alternativas': ['Corto plazo',
                                  'Largo plazo',
                                  'Solo estatal',
                                  'Solo internacional',
                                  'Plazo indeterminado'],
                 'correcta': 'A'},
                {'pregunta': 'La institución que promueve y reglamenta el '
                             'mercado de valores en el Perú es:',
                 'alternativas': ['El BCR',
                                  'La SBS exclusivamente',
                                  'La Superintendencia del Mercado de '
                                  'Valores (SMV)',
                                  'La SUNAT',
                                  'El MEF'],
                 'correcta': 'C'},
                {'pregunta': 'Los bancos de inversión actúan como '
                             'intermediarios entre la empresa emisora y:',
                 'alternativas': ['La SUNAT',
                                  'El Estado',
                                  'El Banco Central',
                                  'Los inversionistas',
                                  'Los consumidores finales'],
                 'correcta': 'D'},
                {'pregunta': 'La Bolsa de Valores es una asociación civil:',
                 'alternativas': ['Sin fines de lucro',
                                  'Con fines de lucro',
                                  'Estatal exclusiva',
                                  'Bancaria',
                                  'Internacional exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La Bolsa de Valores facilita la negociación '
                             'de:',
                 'alternativas': ['Solo bienes raíces',
                                  'Solo divisas',
                                  'Valores mobiliarios registrados',
                                  'Solo créditos hipotecarios',
                                  'Solo bienes físicos'],
                 'correcta': 'C'},
                {'pregunta': 'El banco actúa como intermediario, en el '
                             'mercado monetario, de tipo:',
                 'alternativas': ['Directo',
                                  'Indirecto',
                                  'Privado exclusivo',
                                  'Neutral exclusivo',
                                  'Estatal exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La función más importante del banco, apoyar '
                             'sectores retardatarios mediante préstamos y '
                             'crear empleo, se llama función:',
                 'alternativas': ['Social',
                                  'Administrativa',
                                  'Económica exclusiva',
                                  'Cultural',
                                  'Política'],
                 'correcta': 'A'},
                {'pregunta': 'Los bancos también apoyan a esta institución '
                             'en regular y facilitar la moneda en '
                             'circulación:',
                 'alternativas': ['El BCR',
                                  'La SUNAT',
                                  'La SMV',
                                  'El MEF',
                                  'La SBS'],
                 'correcta': 'A'},
                {'pregunta': 'Los fondos depositados por los clientes, que '
                             'el banco usa para sus operaciones activas, se '
                             'llaman operaciones:',
                 'alternativas': ['Externas',
                                  'Neutras',
                                  'Pasivas',
                                  'Mixtas',
                                  'Activas'],
                 'correcta': 'C'},
                {'pregunta': 'El depósito que permite depósitos y retiros '
                             'mediante cheques se llama depósito:',
                 'alternativas': ['CTS exclusivo',
                                  'A la vista o cuenta corriente',
                                  'A término fijo',
                                  'A plazo',
                                  'De ahorro exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El depósito que implica dejar el dinero por un '
                             'tiempo determinado, sin poder retirarlo antes, '
                             'se llama depósito:',
                 'alternativas': ['De ahorro exclusivo',
                                  'A la vista',
                                  'CTS exclusivo',
                                  'Corriente',
                                  'A plazo o a término'],
                 'correcta': 'E'},
                {'pregunta': 'El fondo obligatorio del empleador que sirve '
                             'como seguro de desempleo para el trabajador se '
                             'llama:',
                 'alternativas': ['EPS', 'ONP', 'AFP', 'CTS', 'ESSALUD'],
                 'correcta': 'D'},
                {'pregunta': 'Las operaciones en las que el banco otorga '
                             'crédito —préstamos, descuentos, anticipos— se '
                             'llaman operaciones:',
                 'alternativas': ['Externas',
                                  'Activas',
                                  'Pasivas',
                                  'Neutras',
                                  'Mixtas'],
                 'correcta': 'B'},
                {'pregunta': 'La operación mediante la cual el banco coloca '
                             'su liquidez cobrando una tasa de interés '
                             'activa se llama:',
                 'alternativas': ['Depósito',
                                  'Sobregiro',
                                  'Ahorro',
                                  'Préstamo',
                                  'CTS'],
                 'correcta': 'D'},
                {'pregunta': 'El sobregiro bancario ocurre cuando el cliente '
                             'gira cheques:',
                 'alternativas': ['Con fondos suficientes',
                                  'Únicamente los fines de semana',
                                  'Sin provisión de fondos suficiente',
                                  'Solo en moneda extranjera',
                                  'Solo con autorización previa'],
                 'correcta': 'C'},
                {'pregunta': 'La banca privada, o banca múltiple, está '
                             'autorizada a realizar operaciones activas, '
                             'pasivas y:',
                 'alternativas': ['Estatales',
                                  'Ninguna otra',
                                  'Neutras o de servicios',
                                  'Internacionales exclusivas',
                                  'Extranjeras exclusivas'],
                 'correcta': 'C'},
                {'pregunta': 'La banca conformada con capitales de '
                             'inversionistas de nacionalidad peruana se '
                             'llama banca:',
                 'alternativas': ['Mixta',
                                  'Estatal',
                                  'Extranjera',
                                  'Privada nacional',
                                  'Internacional'],
                 'correcta': 'D'},
                {'pregunta': 'El principal accionista del Banco de Crédito '
                             'del Perú es:',
                 'alternativas': ['El Estado peruano',
                                  'Un banco extranjero',
                                  'El Grupo Romero',
                                  'La SBS',
                                  'El BCR'],
                 'correcta': 'C'},
                {'pregunta': 'Los bancos que tienen participación de '
                             'inversionistas extranjeros, algunos con casa '
                             'matriz en Estados Unidos y Europa, se llaman '
                             'banca:',
                 'alternativas': ['Privada extranjera',
                                  'Privada nacional',
                                  'Cooperativa',
                                  'Estatal',
                                  'Mixta'],
                 'correcta': 'A'},
                {'pregunta': 'La banca estatal peruana está formada por el '
                             'Banco Central de Reserva y:',
                 'alternativas': ['El Banco de la Nación',
                                  'Interbank',
                                  'El Banco de Crédito',
                                  'El BBVA',
                                  'Scotiabank'],
                 'correcta': 'A'},
                {'pregunta': 'El Banco de la Nación es considerado el agente '
                             'financiero de:',
                 'alternativas': ['Los bancos extranjeros',
                                  'La banca múltiple',
                                  'Los organismos internacionales',
                                  'El sector privado exclusivo',
                                  'El Estado'],
                 'correcta': 'E'},
                {'pregunta': 'El antecedente del Banco de la Nación, creado '
                             'en 1905, fue:',
                 'alternativas': ['La SUNAT',
                                  'El Banco Central',
                                  'El Banco Popular',
                                  'El Banco Internacional',
                                  'La Caja de Depósitos y Consignaciones'],
                 'correcta': 'E'},
                {'pregunta': 'El Banco de la Nación fue creado formalmente '
                             'mediante ley del Congreso el 27 de enero de:',
                 'alternativas': ['1927', '1966', '1990', '1905', '1963'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'INTERMEDIACIÓN FINANCIERA',
                      'items': ['La intermediación financiera es el proceso '
                                'por el cual se trasladan recursos de los '
                                'agentes superavitarios hacia los agentes '
                                'deficitarios.']},
                     {'titulo': 'MERCADOS PRIMARIO Y SECUNDARIO',
                      'items': ['El mercado primario es donde se colocan por '
                                'primera vez los valores emitidos, por '
                                'oferta pública o privada.']},
                     {'titulo': 'VENTAJAS DE LA INTERMEDIACIÓN DIRECTA',
                      'items': ['Los costos de operación son menores para '
                                'ambos agentes.']},
                     {'titulo': 'INSTRUMENTOS Y PRINCIPALES INSTITUCIONES',
                      'items': ['Los instrumentos de renta fija son títulos '
                                'de deuda que generan pago fijo de intereses '
                                'y devolución del capital.']},
                     {'titulo': 'CLASIFICACIÓN DE LOS BANCOS',
                      'items': ['La banca privada, o banca múltiple, está '
                                'autorizada a realizar operaciones activas, '
                                'pasivas y neutras o servicios.']},
                     {'titulo': 'LA EMPRESA BANCARIA',
                      'items': ['El banco es una empresa que actúa como '
                                'intermediario indirecto en el mercado '
                                'monetario, captando dinero del público.']},
                     {'titulo': 'OPERACIONES BANCARIAS: PASIVAS',
                      'items': ['Las operaciones pasivas son los fondos '
                                'depositados por los clientes, que el banco '
                                'usa para sus operaciones activas.']},
                     {'titulo': 'OPERACIONES BANCARIAS: ACTIVAS',
                      'items': ['Las operaciones activas son aquellas en las '
                                'que el banco otorga crédito: préstamos, '
                                'descuentos, anticipos.']}]},
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
                {'titulo': '14.4 TIPOS DE AHORRO',
                 'items': ['El {ahorro público} es el que realiza el Estado, '
                           'con los ingresos del comercio internacional, los '
                           'impuestos y otras actividades.',
                           'Cuando el Estado cubre sus necesidades básicas y '
                           'le sobran recursos, existe un {superávit}; si le '
                           'faltan, un {déficit}.',
                           'El {ahorro privado} lo realizan familias, '
                           'empresas e instituciones sin fines de lucro, '
                           'cuando cubren sus necesidades y les queda un '
                           '{excedente}.']},
                {'titulo': '14.5 LA INVERSIÓN',
                 'items': ['Una {inversión} es la colocación de capital para '
                           'obtener una {ganancia} futura, resignando un '
                           'beneficio {inmediato}.',
                           'Al invertir se asume un {costo de oportunidad}, '
                           'al renunciar a esos recursos en el presente por '
                           'un beneficio futuro {incierto}.',
                           'Para poder invertir es necesario haber tenido '
                           '{ingresos} y haber {ahorrado} previamente parte '
                           'de ellos.',
                           'Las cuatro variables de la inversión privada '
                           'son: el {rendimiento} esperado, el riesgo '
                           'aceptado, el {horizonte} temporal y la '
                           '{liquidez}.',
                           'Existe una relación directa entre el rendimiento '
                           'esperado y el riesgo: a mayor rendimiento, mayor '
                           '{riesgo}.',
                           'Un inversor {conservador} tiende a invertir en '
                           'productos de bajo riesgo, como títulos de renta '
                           '{fija} o depósitos a plazo.',
                           'La {liquidez} de una inversión es la rapidez con '
                           'que se puede recuperar el dinero invertido.']}],
  'cuadros': [{'titulo': '14.2 CONSUMO PRIVADO Y PÚBLICO',
               'encabezados': ['Tipo', 'Quién compra'],
               'filas': [['{Privado}', 'Familias y {empresas} privadas'],
                         ['{Público}', 'El {Estado}']]}],
  'preguntas': [{'pregunta': 'La distribución de la riqueza se define como '
                             'la forma en que el producto total se reparte '
                             'entre:',
                 'alternativas': ['Solo importadores',
                                  'Trabajadores y empresarios',
                                  'Solo el sector externo',
                                  'Solo el Estado',
                                  'Solo bancos'],
                 'correcta': 'B'},
                {'pregunta': 'El modo en que se reparte la riqueza está '
                             'determinado por:',
                 'alternativas': ['Las políticas económicas del Estado',
                                  'Solo la religión',
                                  'Solo el clima',
                                  'Solo la geografía',
                                  'El azar'],
                 'correcta': 'A'},
                {'pregunta': 'El reparto del producto bruto entre las clases '
                             'sociales, según el texto, es:',
                 'alternativas': ['Aleatorio',
                                  'Determinado por sorteo',
                                  'Igual para todos siempre',
                                  'No equitativo',
                                  'Perfectamente equitativo'],
                 'correcta': 'D'},
                {'pregunta': 'El Estado interviene en el mercado buscando '
                             'que la redistribución de la riqueza:',
                 'alternativas': ['Llegue a todos los sectores',
                                  'Beneficie solo a un sector',
                                  'Se concentre en pocas manos',
                                  'Sea eliminada por completo',
                                  'Dependa solo del mercado'],
                 'correcta': 'A'},
                {'pregunta': 'La intervención estatal excesiva en la '
                             'distribución puede:',
                 'alternativas': ['Aumentar la producción sin límites',
                                  'Mejorar automáticamente el mercado',
                                  'No tener ningún efecto',
                                  'Distorsionar el mercado y generar '
                                  'problemas macroeconómicos',
                                  'Eliminar toda desigualdad de forma '
                                  'perfecta'],
                 'correcta': 'D'},
                {'pregunta': 'El consumo se define como la acción de '
                             'utilizar o gastar un bien para atender:',
                 'alternativas': ['Solo el comercio exterior',
                                  'Solo el ahorro',
                                  'Solo la inversión',
                                  'Solo deseos superfluos',
                                  'Necesidades humanas'],
                 'correcta': 'E'},
                {'pregunta': 'En economía, el consumo se considera la fase:',
                 'alternativas': ['Intermedia exclusivamente',
                                  'Final del proceso productivo',
                                  'Inicial del proceso productivo',
                                  'Externa al proceso productivo',
                                  'Previa a la producción'],
                 'correcta': 'B'},
                {'pregunta': 'Las compras de productos que realizan familias '
                             'y empresas privadas constituyen el consumo:',
                 'alternativas': ['Privado',
                                  'Externo',
                                  'Estatal',
                                  'Público',
                                  'Internacional'],
                 'correcta': 'A'},
                {'pregunta': 'Las compras que realiza el Estado constituyen '
                             'el consumo:',
                 'alternativas': ['Empresarial exclusivo',
                                  'Público',
                                  'Externo',
                                  'Privado',
                                  'Familiar'],
                 'correcta': 'B'},
                {'pregunta': 'El consumo es uno de los principales medidores '
                             'de:',
                 'alternativas': ['La inflación exclusivamente',
                                  'El tipo de cambio',
                                  'El costo de oportunidad',
                                  'La tasa de interés',
                                  'El Producto Interno Bruto (PIB)'],
                 'correcta': 'E'},
                {'pregunta': 'Para Keynes, el consumo es lo más importante '
                             'en una economía porque:',
                 'alternativas': ['Estimula la demanda',
                                  'Aumenta la inflación siempre',
                                  'Detiene el crecimiento',
                                  'Reduce la demanda',
                                  'Elimina la producción'],
                 'correcta': 'A'},
                {'pregunta': 'Keynes desarrolló la función consumo en su '
                             'obra:',
                 'alternativas': ['Historia del pensamiento económico',
                                  'La riqueza de las naciones',
                                  'Teoría general del empleo, el interés y '
                                  'el dinero',
                                  'El Capital',
                                  'Principios de economía'],
                 'correcta': 'C'},
                {'pregunta': 'Para Marx, el consumo de las personas depende '
                             'principalmente de:',
                 'alternativas': ['Su edad',
                                  'El lugar que ocupan en la sociedad '
                                  '(capitalista u obrero)',
                                  'Su religión',
                                  'Su nacionalidad',
                                  'Su género'],
                 'correcta': 'B'},
                {'pregunta': 'El ahorro se define como la parte del ingreso '
                             'personal disponible que:',
                 'alternativas': ['Se pierde por inflación',
                                  'Desaparece con el tiempo',
                                  'Se transfiere al Estado obligatoriamente',
                                  'No se consume',
                                  'Se consume totalmente'],
                 'correcta': 'D'},
                {'pregunta': 'El ahorro implica el sacrificio del consumo '
                             'presente por el consumo:',
                 'alternativas': ['Internacional',
                                  'Ajeno',
                                  'Pasado',
                                  'Futuro',
                                  'Estatal'],
                 'correcta': 'D'},
                {'pregunta': 'El ahorro normalmente se compone del excedente '
                             'de dinero devengado durante el proceso:',
                 'alternativas': ['Electoral',
                                  'Educativo',
                                  'Religioso',
                                  'Productivo',
                                  'Judicial'],
                 'correcta': 'D'},
                {'pregunta': 'La primera sociedad de ahorro y préstamo '
                             'surgió durante el siglo:',
                 'alternativas': ['XII', 'XV', 'XVIII', 'XX', 'X'],
                 'correcta': 'B'},
                {'pregunta': 'La primera sociedad de ahorro y préstamo '
                             'surgió como parte del nuevo orden traído por:',
                 'alternativas': ['La Revolución Industrial exclusivamente',
                                  'El feudalismo',
                                  'La colonización americana',
                                  'Las guerras mundiales',
                                  'Las Revoluciones Burguesas'],
                 'correcta': 'E'},
                {'pregunta': 'El deseo desmedido de ahorro, sacrificando '
                             'gastos necesarios, se vincula culturalmente '
                             'con:',
                 'alternativas': ['La solidaridad',
                                  'La avaricia',
                                  'La prudencia exclusiva',
                                  'El altruismo',
                                  'La generosidad'],
                 'correcta': 'B'},
                {'pregunta': 'Existen bienes que se agotan al consumirse, '
                             'como los alimentos, y otros que solo se '
                             'transforman, como:',
                 'alternativas': ['Un libro de texto',
                                  'Una casa',
                                  'Un viaje en avión',
                                  'Una joya',
                                  'Un terreno'],
                 'correcta': 'C'},
                {'pregunta': 'El ahorro que realiza el Estado con los '
                             'ingresos del comercio internacional y los '
                             'impuestos se llama ahorro:',
                 'alternativas': ['Familiar exclusivo',
                                  'Público',
                                  'Empresarial exclusivo',
                                  'Privado',
                                  'Internacional'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el Estado cubre sus necesidades básicas '
                             'y le sobran recursos, se dice que existe:',
                 'alternativas': ['Recesión',
                                  'Inflación',
                                  'Superávit',
                                  'Devaluación',
                                  'Déficit'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando al Estado le faltan recursos para '
                             'cubrir sus necesidades básicas, se dice que '
                             'existe:',
                 'alternativas': ['Excedente',
                                  'Ahorro neto',
                                  'Déficit',
                                  'Superávit',
                                  'Ganancia'],
                 'correcta': 'C'},
                {'pregunta': 'El ahorro que realizan familias, empresas e '
                             'instituciones sin fines de lucro se llama '
                             'ahorro:',
                 'alternativas': ['Fiscal',
                                  'Público',
                                  'Internacional',
                                  'Estatal exclusivo',
                                  'Privado'],
                 'correcta': 'E'},
                {'pregunta': 'Una inversión, en sentido económico, es la '
                             'colocación de capital para obtener:',
                 'alternativas': ['Un consumo directo',
                                  'Un gasto inmediato',
                                  'Un ahorro exclusivo',
                                  'Una ganancia futura',
                                  'Una pérdida segura'],
                 'correcta': 'D'},
                {'pregunta': 'Al realizar una inversión, se asume un costo '
                             'de oportunidad al renunciar a los recursos '
                             'presentes por un beneficio futuro que es:',
                 'alternativas': ['Seguro',
                                  'Nulo',
                                  'Garantizado',
                                  'Incierto',
                                  'Inmediato'],
                 'correcta': 'D'},
                {'pregunta': 'Para poder invertir es necesario haber tenido '
                             'ingresos y haber:',
                 'alternativas': ['Vendido todos los activos',
                                  'Ahorrado previamente parte de esos '
                                  'ingresos',
                                  'Gastado todo previamente',
                                  'Evitado el consumo por completo',
                                  'Solicitado un préstamo obligatoriamente'],
                 'correcta': 'B'},
                {'pregunta': 'Las cuatro variables de la inversión privada '
                             'son rendimiento esperado, riesgo aceptado, '
                             'horizonte temporal y:',
                 'alternativas': ['Liquidez',
                                  'Inflación',
                                  'Impuesto',
                                  'Salario',
                                  'Tipo de cambio'],
                 'correcta': 'A'},
                {'pregunta': 'Entre el rendimiento esperado y el riesgo '
                             'asumido existe una relación directa: a mayor '
                             'rendimiento,',
                 'alternativas': ['Riesgo nulo',
                                  'Mayor riesgo',
                                  'Menor riesgo',
                                  'Menor liquidez exclusivamente',
                                  'Riesgo constante'],
                 'correcta': 'B'},
                {'pregunta': 'Un inversor conservador tiende a invertir en '
                             'productos de bajo riesgo, como títulos de '
                             'renta fija o:',
                 'alternativas': ['Depósitos a plazo',
                                  'Bonos basura',
                                  'Acciones especulativas',
                                  'Futuros de alto riesgo',
                                  'Criptomonedas'],
                 'correcta': 'A'},
                {'pregunta': 'La variable de la inversión que se refiere a '
                             'la rapidez con que se puede recuperar el '
                             'dinero invertido se llama:',
                 'alternativas': ['Horizonte temporal',
                                  'Riesgo',
                                  'Rentabilidad',
                                  'Rendimiento',
                                  'Liquidez'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'LA DISTRIBUCIÓN DE LA RIQUEZA',
                      'items': ['La distribución de la riqueza es la forma '
                                'en que el producto total generado por un '
                                'país se reparte entre trabajadores y '
                                'empresarios.']},
                     {'titulo': 'EL CONSUMO',
                      'items': ['El consumo es la acción de utilizar o '
                                'gastar un bien o servicio para atender '
                                'necesidades humanas.']},
                     {'titulo': 'EL AHORRO',
                      'items': ['El ahorro es la parte del ingreso personal '
                                'disponible que no se consume.']},
                     {'titulo': 'TIPOS DE AHORRO',
                      'items': ['El ahorro público es el que realiza el '
                                'Estado, con los ingresos del comercio '
                                'internacional, los impuestos y otras '
                                'actividades.']},
                     {'titulo': 'LA INVERSIÓN',
                      'items': ['Una inversión es la colocación de capital '
                                'para obtener una ganancia futura, '
                                'resignando un beneficio inmediato.']}]},
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
                {'titulo': '15.5 EL PRESUPUESTO PÚBLICO',
                 'items': ['El {Presupuesto Público} es el principal '
                           'instrumento de planificación {financiera} del '
                           'Estado, aprobado por {Ley}.',
                           'El presupuesto contiene el registro sistemático '
                           'de los {ingresos} que el Estado proyecta y los '
                           '{gastos} que planea realizar.',
                           'El proceso presupuestario peruano tiene {cinco} '
                           'fases: programación, formulación, aprobación, '
                           'ejecución, y control y {evaluación}.',
                           'En la {programación}, la Dirección Nacional de '
                           'Presupuesto Público del MEF estima ingresos y '
                           'prevé {gastos}.',
                           'En la {aprobación}, el anteproyecto va al '
                           'Congreso hasta el 30 de agosto, y la Ley de '
                           'Presupuesto debe aprobarse hasta el {30} de '
                           'noviembre.',
                           'En el {control y evaluación}, la Contraloría '
                           'supervisa la legalidad, y el {Congreso} '
                           'fiscaliza la ejecución.']},
                {'titulo': '15.6 PRINCIPIOS PRESUPUESTARIOS',
                 'items': ['{Equilibrio presupuestal}: los ingresos '
                           'previstos y los egresos programados deben estar '
                           '{igualados}.',
                           '{Claridad}: el presupuesto debe ser de fácil '
                           '{comprensión} para congresistas y ciudadanos.',
                           '{Exactitud}: debe elaborarse con exactitud y '
                           '{sinceridad}, sin falsear las previsiones.',
                           '{Universalidad}: debe contener el total de '
                           'ingresos y gastos de {todas} las entidades del '
                           'Estado.',
                           '{Exclusividad}: debe ser discutido y aprobado '
                           'por el Poder {Legislativo} antes de su '
                           'ejecución.',
                           '{Publicidad}: debe publicarse en el diario '
                           'oficial «{El Peruano}» para que la población '
                           'acceda a la información.']},
                {'titulo': '15.7 ESTRUCTURA DEL PRESUPUESTO',
                 'items': ['El presupuesto se elabora bajo el principio '
                           'contable de la {partida doble}: contiene '
                           'ingresos fiscales y {egresos} fiscales.']}],
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
                 'alternativas': ['Los sindicatos',
                                  'Los bancos privados',
                                  'Las empresas privadas',
                                  'El Estado',
                                  'Los organismos internacionales '
                                  'exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'El sector público está representado por el '
                             'Gobierno en los niveles nacional, regional y:',
                 'alternativas': ['Sindical',
                                  'Internacional',
                                  'Continental',
                                  'Local',
                                  'Empresarial'],
                 'correcta': 'D'},
                {'pregunta': 'La finalidad del sector público es buscar:',
                 'alternativas': ['Solo el comercio exterior',
                                  'El bienestar general de los ciudadanos',
                                  'Solo la estabilidad monetaria',
                                  'Solo la ganancia empresarial',
                                  'Solo la recaudación fiscal'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de instrumentos '
                             'técnico-económicos-sociales con que cuenta el '
                             'Estado se llama:',
                 'alternativas': ['Mercado de valores',
                                  'Bolsa de valores',
                                  'Comercio exterior',
                                  'Finanzas públicas',
                                  'Sistema bancario privado'],
                 'correcta': 'D'},
                {'pregunta': 'Las tres funciones clásicas del Estado son '
                             'redistribución de la renta, estabilización de '
                             'la economía y:',
                 'alternativas': ['Comercio exterior',
                                  'Endeudamiento',
                                  'Emisión monetaria exclusiva',
                                  'Privatización',
                                  'Asignación de recursos'],
                 'correcta': 'E'},
                {'pregunta': 'Entre los instrumentos del Estado para influir '
                             'en la economía figuran los impuestos, el gasto '
                             'público y:',
                 'alternativas': ['La regulación',
                                  'Solo el crédito privado',
                                  'Solo la publicidad estatal',
                                  'Solo la migración',
                                  'Solo el comercio informal'],
                 'correcta': 'A'},
                {'pregunta': 'Según Musgrave, además de las funciones '
                             'clásicas, el Estado cumple la función de '
                             'promoción del crecimiento y:',
                 'alternativas': ['La privatización total',
                                  'La regulación económica',
                                  'El cierre de empresas públicas',
                                  'La eliminación de impuestos',
                                  'La reducción del gasto social'],
                 'correcta': 'B'},
                {'pregunta': 'La contabilidad nacional también se conoce '
                             'como:',
                 'alternativas': ['Contabilidad social',
                                  'Contabilidad bancaria',
                                  'Contabilidad internacional',
                                  'Contabilidad fiscal exclusiva',
                                  'Contabilidad empresarial'],
                 'correcta': 'A'},
                {'pregunta': 'El Producto Bruto Interno (PBI) mide el valor '
                             'monetario de todos los bienes y servicios:',
                 'alternativas': ['Importados solamente',
                                  'No transados',
                                  'Finales',
                                  'Informales',
                                  'Intermedios exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'El PBI también se conoce con el nombre de:',
                 'alternativas': ['Ingreso Nacional Disponible',
                                  'Balanza Comercial',
                                  'Producto Nacional Neto',
                                  'Renta Nacional Bruta',
                                  'Producto Geográfico Bruto'],
                 'correcta': 'E'},
                {'pregunta': 'El PBI se valoriza a los precios:',
                 'alternativas': ['Internacionales exclusivamente',
                                  'De mercado vigentes en el año de '
                                  'referencia',
                                  'Solo del sector agrícola',
                                  'Históricos fijos',
                                  'Solo mayoristas'],
                 'correcta': 'B'},
                {'pregunta': 'El PBI cuantifica la producción de:',
                 'alternativas': ['Solo las empresas estatales',
                                  'Solo las multinacionales',
                                  'Solo los nacionales fuera del país',
                                  'Los residentes del país, sean nacionales '
                                  'o extranjeros',
                                  'Solo el sector exportador'],
                 'correcta': 'D'},
                {'pregunta': 'El indicador que mide el valor de la '
                             'producción usando los precios del mismo año '
                             'medido se llama:',
                 'alternativas': ['PBI ajustado',
                                  'PBI per cápita',
                                  'PBI potencial',
                                  'PBI nominal',
                                  'PBI real'],
                 'correcta': 'D'},
                {'pregunta': 'El indicador que mide las variaciones en la '
                             'producción física entre dos periodos, usando '
                             'precios constantes, se llama:',
                 'alternativas': ['PBI ajustado por inflación exclusivamente',
                                  'PBI bruto exclusivo',
                                  'PBI nominal',
                                  'PBI real',
                                  'PBI corriente'],
                 'correcta': 'D'},
                {'pregunta': 'Para calcular el PBI real se usan los precios '
                             'de:',
                 'alternativas': ['El año siguiente',
                                  'Ningún año en particular',
                                  'Solo el año más reciente',
                                  'Un año base fijo',
                                  'Cada año distinto'],
                 'correcta': 'D'},
                {'pregunta': 'El PBI nominal se modifica año tras año debido '
                             'a variaciones en:',
                 'alternativas': ['Solo el tipo de cambio',
                                  'Solo la moneda extranjera',
                                  'Los precios de mercado y la producción '
                                  'física',
                                  'Solo la población',
                                  'Solo el clima'],
                 'correcta': 'C'},
                {'pregunta': 'El dinero, en la medición del PBI, sirve '
                             'principalmente como:',
                 'alternativas': ['Medio de ahorro exclusivo',
                                  'Depósito de valor exclusivo',
                                  'Unidad de cuenta para cuantificar la '
                                  'producción',
                                  'Patrón de pagos diferidos exclusivo',
                                  'Reserva internacional'],
                 'correcta': 'C'},
                {'pregunta': 'El PBI se calcula generalmente en un periodo '
                             'de:',
                 'alternativas': ['Un día',
                                  'Una semana',
                                  'Un año',
                                  'Una década',
                                  'Un mes'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado, para influir en la economía, puede '
                             'optar por la intervención directa u ofrecer:',
                 'alternativas': ['Incentivos al sector privado',
                                  'Ningún tipo de apoyo',
                                  'Solo prohibiciones totales',
                                  'Solo sanciones',
                                  'Solo aranceles'],
                 'correcta': 'A'},
                {'pregunta': 'El PBI es considerado, para economías como la '
                             'peruana, el agregado macroeconómico:',
                 'alternativas': ['Más importante',
                                  'Menos relevante',
                                  'Sin ninguna utilidad',
                                  'Solo referencial',
                                  'Ajeno a otras variables'],
                 'correcta': 'A'},
                {'pregunta': 'El Presupuesto Público es el principal '
                             'instrumento de planificación financiera del '
                             'Estado, aprobado por:',
                 'alternativas': ['Ordenanza',
                                  'Decreto Supremo',
                                  'Resolución Ministerial',
                                  'Ley',
                                  'Reglamento'],
                 'correcta': 'D'},
                {'pregunta': 'El presupuesto contiene el registro '
                             'sistemático de los ingresos que proyecta el '
                             'Estado y los gastos que planea:',
                 'alternativas': ['Postergar',
                                  'Anular',
                                  'Eliminar',
                                  'Evitar',
                                  'Realizar'],
                 'correcta': 'E'},
                {'pregunta': 'El proceso presupuestario peruano está formado '
                             'por un número de fases igual a:',
                 'alternativas': ['Cinco', 'Siete', 'Tres', 'Dos', 'Diez'],
                 'correcta': 'A'},
                {'pregunta': 'La primera fase del proceso presupuestario, '
                             'donde se estiman ingresos y se prevén gastos, '
                             'se llama:',
                 'alternativas': ['Programación',
                                  'Formulación',
                                  'Ejecución',
                                  'Control',
                                  'Aprobación'],
                 'correcta': 'A'},
                {'pregunta': 'La fase en la que se asignan los recursos del '
                             'presupuesto a cada dependencia del Estado se '
                             'llama:',
                 'alternativas': ['Aprobación',
                                  'Evaluación',
                                  'Formulación',
                                  'Ejecución',
                                  'Programación'],
                 'correcta': 'C'},
                {'pregunta': 'La Ley de Presupuesto debe ser aprobada por el '
                             'Poder Legislativo como máximo hasta el:',
                 'alternativas': ['31 de diciembre',
                                  '1 de enero',
                                  '15 de octubre',
                                  '30 de noviembre',
                                  '30 de agosto'],
                 'correcta': 'D'},
                {'pregunta': 'La fase de concreción del flujo de ingresos y '
                             'gastos previstos, dirigida por la Dirección '
                             'Nacional de Presupuesto Público, se llama:',
                 'alternativas': ['Formulación',
                                  'Ejecución',
                                  'Programación',
                                  'Aprobación',
                                  'Publicación'],
                 'correcta': 'B'},
                {'pregunta': 'La supervisión de la legalidad de la ejecución '
                             'del presupuesto está a cargo de:',
                 'alternativas': ['El MEF exclusivo',
                                  'La SUNAT',
                                  'La Contraloría General de la República',
                                  'El Poder Judicial',
                                  'El Congreso'],
                 'correcta': 'C'},
                {'pregunta': 'La fiscalización de la ejecución del '
                             'presupuesto está a cargo de:',
                 'alternativas': ['La Contraloría',
                                  'El MEF exclusivo',
                                  'El Congreso de la República',
                                  'La SBS',
                                  'El BCR'],
                 'correcta': 'C'},
                {'pregunta': 'El principio presupuestario que exige que '
                             'ingresos y egresos estén igualados se llama:',
                 'alternativas': ['Claridad',
                                  'Universalidad',
                                  'Publicidad',
                                  'Equilibrio presupuestal',
                                  'Exclusividad'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que exige que el presupuesto sea '
                             'de fácil comprensión para congresistas y '
                             'ciudadanos se llama:',
                 'alternativas': ['Exactitud',
                                  'Exclusividad',
                                  'Claridad',
                                  'Documentación',
                                  'Universalidad'],
                 'correcta': 'C'},
                {'pregunta': 'El principio que exige que el presupuesto se '
                             'elabore con exactitud y sinceridad, sin '
                             'falsear previsiones, se llama:',
                 'alternativas': ['Universalidad',
                                  'Documentación',
                                  'Publicidad',
                                  'Exactitud',
                                  'Claridad'],
                 'correcta': 'D'},
                {'pregunta': 'El principio que exige que el presupuesto '
                             'contenga el total de ingresos y gastos de '
                             'todas las entidades del Estado se llama:',
                 'alternativas': ['Universalidad',
                                  'Exactitud',
                                  'Documentación',
                                  'Claridad',
                                  'Exclusividad'],
                 'correcta': 'A'},
                {'pregunta': 'El principio que exige que el presupuesto sea '
                             'discutido y aprobado por el Legislativo antes '
                             'de su ejecución se llama:',
                 'alternativas': ['Documentación',
                                  'Publicidad',
                                  'Exclusividad',
                                  'Claridad',
                                  'Universalidad'],
                 'correcta': 'C'},
                {'pregunta': 'El principio que exige la publicación del '
                             'presupuesto en el diario oficial «El Peruano» '
                             'se llama:',
                 'alternativas': ['Claridad',
                                  'Exclusividad',
                                  'Documentación',
                                  'Universalidad',
                                  'Publicidad'],
                 'correcta': 'E'},
                {'pregunta': 'El Presupuesto Público se elabora bajo el '
                             'principio contable de:',
                 'alternativas': ['El valor razonable',
                                  'La materialidad',
                                  'El costo histórico',
                                  'La partida doble',
                                  'La prudencia'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura del Presupuesto Público contiene '
                             'dos grandes cuentas: ingresos fiscales y:',
                 'alternativas': ['Patrimonio fiscal',
                                  'Egresos fiscales',
                                  'Activos fiscales',
                                  'Pasivos fiscales',
                                  'Reservas fiscales'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE SECTOR PÚBLICO',
                      'items': ['El sector público es el sector de la '
                                'economía conformado por instituciones que '
                                'actúan a nombre del Estado.']},
                     {'titulo': 'FUNCIONES DEL ESTADO',
                      'items': ['Las tres funciones clásicas del Estado son: '
                                'redistribución de la renta, estabilización '
                                'de la economía y asignación de recursos.']},
                     {'titulo': 'CONTABILIDAD NACIONAL Y EL PBI',
                      'items': ['La contabilidad nacional, o contabilidad '
                                'social, describe la medición de las '
                                'actividades económicas de un país.']},
                     {'titulo': 'PBI NOMINAL Y PBI REAL',
                      'items': ['El PBI nominal mide el valor de la '
                                'producción usando los precios del mismo año '
                                'que se mide.']},
                     {'titulo': 'EL PRESUPUESTO PÚBLICO',
                      'items': ['El Presupuesto Público es el principal '
                                'instrumento de planificación financiera del '
                                'Estado, aprobado por Ley.']},
                     {'titulo': 'PRINCIPIOS PRESUPUESTARIOS',
                      'items': ['Equilibrio presupuestal: los ingresos '
                                'previstos y los egresos programados deben '
                                'estar igualados.']},
                     {'titulo': 'ESTRUCTURA DEL PRESUPUESTO',
                      'items': ['El presupuesto se elabora bajo el principio '
                                'contable de la partida doble: contiene '
                                'ingresos fiscales y egresos fiscales.']}]},
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
                {'titulo': '16.4 ELEMENTOS DEL COMERCIO INTERNACIONAL',
                 'items': ['Las {divisas} son moneda extranjera que usan los '
                           'residentes de un país para transacciones '
                           'internacionales; deben ser monedas {duras}.',
                           'Las {reservas internacionales} son recursos, en '
                           'oro y divisas, que un país usa para pagar la '
                           'deuda externa y realizar {intercambios} '
                           'comerciales.',
                           'Los {Derechos Especiales de Giro} (DEG) son un '
                           'activo de reserva creado por el {FMI} en 1969, '
                           'asignado a países miembros desde {1970}.']},
                {'titulo': '16.5 EL TIPO DE CAMBIO',
                 'items': ['El {tipo de cambio} es el precio de una moneda '
                           'expresado en términos de {otra}.',
                           'Los {sistemas de tipo de cambio}, o regímenes '
                           'cambiarios, definen cómo se determina el precio '
                           'de la moneda extranjera.',
                           'El tipo de cambio {fijo} lo determina el Banco '
                           'Central por tiempo indefinido; si es menor al '
                           'equilibrio, {disminuyen} las reservas.',
                           'El tipo de cambio {flexible} se subdivide en '
                           'flotación limpia y flotación {sucia} o '
                           'administrada.',
                           'La {flotación limpia}, o libre, se determina por '
                           'las fuerzas de la {oferta} y la demanda de '
                           'divisas.',
                           'La {flotación sucia}, o tipo de cambio '
                           'administrado, deja flotar el tipo de cambio pero '
                           'el {BCR} interviene para guiarlo.']},
                {'titulo': '16.6 LA BALANZA DE PAGOS',
                 'items': ['La {balanza de pagos} es el registro contable de '
                           'todas las transacciones económicas y financieras '
                           'de un país con el resto del {mundo}.',
                           'La {Balanza en Cuenta Corriente} (BCC) registra '
                           'todas las transacciones de valores económicos, '
                           'salvo los recursos {financieros}.',
                           'Si la BCC es {negativa}, salen más divisas de '
                           'las que ingresan, y el país necesita financiar '
                           'el {déficit}.',
                           'La {Balanza Comercial} (BC) registra el '
                           'intercambio de bienes: {exportaciones} (X), que '
                           'generan ingreso de divisas, e importaciones (M), '
                           'que generan {salida}.',
                           'La {Balanza de Servicios} (BS) registra '
                           'transacciones de servicios: transporte, viajes, '
                           'comunicaciones, {seguros}, entre otros.',
                           'La {Renta de Factores} (RF) registra intereses '
                           'de deuda, remesa de utilidades y {dividendos} '
                           'por inversiones.',
                           'Las {Transferencias Corrientes} (TC) registran '
                           'ingresos y pagos de transferencias unilaterales '
                           'sin contrapartida, como las {remesas} de '
                           'emigrantes.',
                           'La fórmula de la Balanza en Cuenta Corriente es: '
                           'BCC = BC + BS + {RF} + TC.']},
                {'titulo': '16.7 LA CUENTA FINANCIERA',
                 'items': ['La {Cuenta Financiera} (CF) registra el ingreso '
                           'y salida de divisas destinadas a inversiones '
                           'productivas o {especulativas}.',
                           'La CF se divide en Sector {Privado}, Sector '
                           'Público y Capitales de {Corto Plazo}.',
                           'Los {capitales de corto plazo} entran o salen '
                           'del país en periodos menores a un año; se les '
                           'llama capitales {golondrinos} o volátiles.',
                           'La fórmula de la Cuenta Financiera es: CF = SPr '
                           '+ {SPu} + CCP.']},
                {'titulo': '16.8 FINANCIAMIENTO EXCEPCIONAL Y DEUDA EXTERNA',
                 'items': ['El {financiamiento excepcional}, o cuenta de '
                           'ajuste, registra préstamos del exterior, atrasos '
                           'en pagos y {condonación} de deuda.',
                           'La {deuda externa} es el conjunto de '
                           'obligaciones que tiene un país con acreedores '
                           'que residen en el {extranjero}.',
                           'La deuda externa se compone de deuda {pública} '
                           '(contraída por el Estado) y deuda {privada} '
                           '(contraída por empresas y familias).',
                           'Entre las causas de endeudamiento externo están '
                           'las inversiones en infraestructura, las '
                           '{catástrofes} naturales y la mala '
                           '{administración}.']},
                {'titulo': '16.9 CLASES DE DEUDA Y CARACTERÍSTICAS',
                 'items': ['La {deuda interna} es la porción de la deuda '
                           'pública cuyos acreedores son ciudadanos de la '
                           'misma {nación}.',
                           'La {deuda externa} tiene acreedores extranjeros; '
                           'posibilita fondos sin menoscabo del {ahorro} '
                           'nacional.',
                           'Los principales prestamistas de la deuda externa '
                           'son la banca comercial {privada}.',
                           'La finalidad de la deuda externa es estabilizar '
                           'economías en {crisis} e impulsar su crecimiento, '
                           'aunque con efectos {negativos} para la '
                           'población.']},
                {'titulo': '16.10 ORGANISMOS MULTILATERALES',
                 'items': ['El {Fondo Monetario Internacional} (FMI), '
                           'fundado en {1945}, fomenta la cooperación '
                           'monetaria y la estabilidad {financiera}.',
                           'El {Banco Interamericano de Desarrollo} (BID), '
                           'creado en {1959} con sede en Washington, '
                           'financia proyectos de desarrollo en América '
                           '{Latina}.',
                           'El {Banco Mundial} es una entidad especializada '
                           'de la {ONU}, integrada por el BIRF, la AIF, la '
                           'CFI, el OMGI y el CIADI.',
                           'El {BIRF} (Banco Internacional de Reconstrucción '
                           'y Fomento), creado en {1945}, busca reducir la '
                           'pobreza en países en desarrollo.',
                           'El {Club de París} es un espacio de negociación '
                           'entre acreedores oficiales y países deudores, '
                           'creado en {1956}.']},
                {'titulo': '16.11 BLOQUES ECONÓMICOS',
                 'items': ['Un {bloque económico} es un conjunto de países '
                           'que se asocian para impulsar el intercambio '
                           '{comercial} entre ellos, bajando aranceles '
                           'mutuos.',
                           'La {Unión Europea} (UE) es una asociación '
                           'económica y política formada por 28 países, con '
                           'moneda {única} y capital en Bruselas.',
                           'El {MERCOSUR} (Mercado Común del Sur) fue '
                           'instituido inicialmente por Argentina, Brasil, '
                           '{Paraguay} y Uruguay.',
                           'La {Comunidad Andina} (CAN) se originó del '
                           'Acuerdo de {Cartagena}, firmado en 1969; sus '
                           'países miembros son Bolivia, Colombia, Ecuador y '
                           '{Perú}.',
                           'La {UNASUR} agrupó a doce países sudamericanos, '
                           'pero varios miembros suspendieron su '
                           'participación desde {2018}.',
                           'El {NAFTA} (Tratado de Libre Comercio de América '
                           'del Norte) entró en vigor en {1994}, conformado '
                           'por Canadá, México y Estados Unidos.',
                           'El {APEC} (Foro de Cooperación Económica '
                           'Asia-Pacífico) busca facilitar el crecimiento '
                           'económico y el comercio en la región '
                           '{Asia}-Pacífico.']},
                {'titulo': '16.12 TRATADOS DE LIBRE COMERCIO',
                 'items': ['Un {Tratado de Libre Comercio} (TLC) es un '
                           'acuerdo comercial vinculante entre dos o más '
                           'países, con preferencias arancelarias {mutuas}.',
                           'Los TLC tienen plazo {indefinido}: permanecen '
                           'vigentes a lo largo del tiempo, con carácter de '
                           '{perpetuidad}.',
                           'Entre los objetivos de un TLC están eliminar '
                           'barreras {arancelarias}, promover la competencia '
                           'justa y proteger la propiedad {intelectual}.',
                           'Para el Perú, los TLC buscan ampliar el '
                           '{mercado} de las empresas peruanas, dado el '
                           'reducido tamaño del mercado {local}.']},
                {'titulo': '16.13 LA GLOBALIZACIÓN',
                 'items': ['La {globalización} es el aumento continuo de la '
                           'interconexión entre naciones en el plano '
                           'económico, político, social y {tecnológico}.',
                           'El término se usa desde los años {ochenta}, '
                           'cuando los adelantos tecnológicos aceleraron las '
                           'transacciones internacionales.',
                           'El {capital comercial} se usa en la '
                           'comercialización de bienes y servicios en el '
                           'mercado mundial para obtener ganancias.',
                           'El {capital productivo} se invierte en la compra '
                           'de factores de producción para fabricar bienes y '
                           'servicios.',
                           'El {capital financiero} es el dinero invertido '
                           'en otro país como inversión directa extranjera o '
                           'mediante {créditos}.',
                           'Entre los actores de la globalización están los '
                           'bancos {multinacionales}, las empresas '
                           'multinacionales y las instituciones '
                           '{internacionales}.',
                           'Una ventaja de la globalización es el acceso a '
                           '{mercados} más grandes y el aprovechamiento de '
                           'la economía de {escala}.']}],
  'cuadros': [{'titulo': '16.2 TEORÍAS DEL COMERCIO INTERNACIONAL',
               'encabezados': ['Teoría', 'Autor'],
               'filas': [['Ventaja {absoluta}', '{Adam Smith}'],
                         ['Ventaja {comparativa}', '{David Ricardo}'],
                         ['Ventaja {competitiva}', '{Michael Porter}']]}],
  'preguntas': [{'pregunta': 'Ningún país tiene una economía:',
                 'alternativas': ['Autárquica',
                                  'Mixta',
                                  'De mercado',
                                  'Global',
                                  'Abierta'],
                 'correcta': 'A'},
                {'pregunta': 'Un país recurre al comercio exterior, entre '
                             'otras razones, porque no posee suficiente:',
                 'alternativas': ['Cultura',
                                  'Tecnología y recursos naturales',
                                  'Población',
                                  'Historia',
                                  'Territorio'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, el organismo rector de la política '
                             'económica comercial externa es:',
                 'alternativas': ['La SUNAT exclusivamente',
                                  'La SBS',
                                  'El Ministerio de Economía y Finanzas',
                                  'El Congreso',
                                  'El BCR'],
                 'correcta': 'C'},
                {'pregunta': 'El sector externo está supeditado a '
                             'instituciones supranacionales como:',
                 'alternativas': ['Solo gobiernos locales',
                                  'Solo bancos privados',
                                  'Solo universidades',
                                  'Solo ONGs',
                                  'La Organización Mundial de Comercio '
                                  '(OMC)'],
                 'correcta': 'E'},
                {'pregunta': 'Los mercantilistas postulaban que un país '
                             'debía exportar todo lo posible e importar:',
                 'alternativas': ['Solo tecnología',
                                  'Nada en absoluto',
                                  'Todo lo posible también',
                                  'Solo metales preciosos',
                                  'Solo lo necesario'],
                 'correcta': 'E'},
                {'pregunta': 'Según los mercantilistas, el pago de las '
                             'exportaciones debía recibirse en:',
                 'alternativas': ['Metales preciosos',
                                  'Bienes de consumo',
                                  'Mano de obra',
                                  'Tecnología',
                                  'Servicios'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría de la ventaja absoluta fue planteada '
                             'por:',
                 'alternativas': ['Adam Smith',
                                  'David Ricardo',
                                  'John Keynes',
                                  'Michael Porter',
                                  'Karl Marx'],
                 'correcta': 'A'},
                {'pregunta': 'Según la teoría de la ventaja absoluta, un '
                             'país debe especializarse en el bien que '
                             'produce con:',
                 'alternativas': ['Mayor cantidad de insumos',
                                  'Mayor costo',
                                  'Mayor precio de venta',
                                  'Menor calidad',
                                  'Menor costo'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría de la ventaja comparativa fue '
                             'planteada por:',
                 'alternativas': ['David Ricardo',
                                  'Raymond Barre',
                                  'Michael Porter',
                                  'Friedrich von Wieser',
                                  'Adam Smith'],
                 'correcta': 'A'},
                {'pregunta': 'David Ricardo formuló su teoría años después '
                             'de la teoría de Adam Smith, aproximadamente:',
                 'alternativas': ['10 años',
                                  '5 años',
                                  '37 años',
                                  '200 años',
                                  '100 años'],
                 'correcta': 'C'},
                {'pregunta': 'Según la teoría de la ventaja comparativa, la '
                             'ventaja procede del:',
                 'alternativas': ['Clima favorable exclusivamente',
                                  'Idioma oficial',
                                  'Costo de oportunidad en la producción de '
                                  'cada bien',
                                  'Tamaño del país',
                                  'Número de habitantes'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría de la ventaja competitiva fue '
                             'planteada por:',
                 'alternativas': ['Adam Smith',
                                  'Raymond Barre',
                                  'Nassau Senior',
                                  'Michael Porter',
                                  'David Ricardo'],
                 'correcta': 'E'},
                {'pregunta': 'Michael Porter planteó su teoría de la ventaja '
                             'competitiva en la década de:',
                 'alternativas': ['Los 2000',
                                  'Los 40',
                                  'Los 20',
                                  'Los 80',
                                  'Los 60'],
                 'correcta': 'D'},
                {'pregunta': 'Según Porter, los países deben competir '
                             'empleando, además de factores naturales:',
                 'alternativas': ['Solo subsidios estatales',
                                  'Solo su ubicación geográfica',
                                  'Solo mano de obra barata',
                                  'Solo aranceles altos',
                                  'Estrategias empresariales y de mercado'],
                 'correcta': 'E'},
                {'pregunta': 'Las exportaciones se definen como la venta de '
                             'bienes y servicios nacionales:',
                 'alternativas': ['Al resto del mundo',
                                  'Dentro del propio país',
                                  'Solo en moneda nacional',
                                  'Solo a empresas estatales',
                                  'Solo a países vecinos'],
                 'correcta': 'A'},
                {'pregunta': 'Las exportaciones generan para el país '
                             'exportador ingresos de:',
                 'alternativas': ['Deuda externa',
                                  'Divisas',
                                  'Impuestos exclusivamente',
                                  'Aranceles',
                                  'Inflación'],
                 'correcta': 'B'},
                {'pregunta': 'En el Perú, la institución encargada de las '
                             'leyes aduaneras y el código tributario es:',
                 'alternativas': ['El INDECOPI',
                                  'El MEF exclusivamente',
                                  'La SUNAT',
                                  'La SBS',
                                  'El BCR'],
                 'correcta': 'C'},
                {'pregunta': 'La Cámara Internacional de París diseña los '
                             'INCOTERMS para fijar precios como:',
                 'alternativas': ['Solo tipos de cambio',
                                  'Solo aranceles',
                                  'Solo precios de exportación agrícola',
                                  'Solo precios internos',
                                  'FOB y CIF'],
                 'correcta': 'E'},
                {'pregunta': 'El BCR, en coordinación con el MEF, maneja '
                             'principalmente:',
                 'alternativas': ['El presupuesto educativo',
                                  'Los aranceles',
                                  'Los impuestos internos',
                                  'El tipo de cambio',
                                  'Las tarifas municipales'],
                 'correcta': 'D'},
                {'pregunta': 'El comercio exterior surge, entre otras '
                             'razones, porque no todas las mercancías son '
                             'libres de comerciar y requieren:',
                 'alternativas': ['Leyes, reglamentos e instituciones',
                                  'Prohibición total',
                                  'Solo tratados bilaterales',
                                  'Ninguna regulación',
                                  'Solo acuerdos verbales'],
                 'correcta': 'A'},
                {'pregunta': 'Las divisas, para cumplir su función de medio '
                             'de pago internacional, deben ser monedas:',
                 'alternativas': ['Blandas',
                                  'Sin valor',
                                  'De curso interno exclusivo',
                                  'Duras',
                                  'Regionales exclusivas'],
                 'correcta': 'D'},
                {'pregunta': 'Los recursos en oro y divisas que un país usa '
                             'para pagar deuda externa se llaman:',
                 'alternativas': ['Divisas exclusivas',
                                  'DEG exclusivos',
                                  'Reservas internacionales',
                                  'Bonos soberanos',
                                  'Activos fijos'],
                 'correcta': 'C'},
                {'pregunta': 'Los Derechos Especiales de Giro (DEG) fueron '
                             'creados por el Fondo Monetario Internacional '
                             'en el año:',
                 'alternativas': ['1988', '1959', '1969', '1994', '1945'],
                 'correcta': 'C'},
                {'pregunta': 'El tipo de cambio se define como el precio de '
                             'una moneda expresado en términos de:',
                 'alternativas': ['Bienes y servicios',
                                  'Otra moneda',
                                  'Trabajo',
                                  'Oro',
                                  'Divisas exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El tipo de cambio determinado por el Banco '
                             'Central por tiempo indefinido se llama tipo de '
                             'cambio:',
                 'alternativas': ['Flotante',
                                  'Sucio',
                                  'Administrado',
                                  'Fijo',
                                  'Flexible'],
                 'correcta': 'D'},
                {'pregunta': 'El tipo de cambio determinado por las fuerzas '
                             'de oferta y demanda de divisas se llama:',
                 'alternativas': ['Fijo',
                                  'Regulado',
                                  'Controlado',
                                  'Administrado',
                                  'Flotación limpia o libre'],
                 'correcta': 'E'},
                {'pregunta': 'El tipo de cambio flotante en el que el BCR '
                             'interviene ocasionalmente para guiarlo se '
                             'llama:',
                 'alternativas': ['Tipo bloqueado',
                                  'Tipo controlado',
                                  'Tipo fijo',
                                  'Flotación sucia o administrado',
                                  'Flotación limpia'],
                 'correcta': 'D'},
                {'pregunta': 'La balanza de pagos se define como el registro '
                             'contable de las transacciones económicas y '
                             'financieras de un país con:',
                 'alternativas': ['Sus propias regiones',
                                  'Solo sus vecinos',
                                  'El resto del mundo',
                                  'Solo América Latina',
                                  'Solo la Unión Europea'],
                 'correcta': 'C'},
                {'pregunta': 'La Balanza en Cuenta Corriente registra todas '
                             'las transacciones de valores económicos, '
                             'salvo:',
                 'alternativas': ['El comercio exterior',
                                  'Los recursos financieros',
                                  'Los bienes',
                                  'Los servicios',
                                  'Las transferencias'],
                 'correcta': 'B'},
                {'pregunta': 'La Balanza Comercial registra el intercambio '
                             'de bienes mediante exportaciones e:',
                 'alternativas': ['Transferencias',
                                  'Intereses',
                                  'Importaciones',
                                  'Inversiones',
                                  'Remesas'],
                 'correcta': 'C'},
                {'pregunta': 'Las exportaciones (X) generan ingreso de '
                             'divisas; las importaciones (M) generan:',
                 'alternativas': ['También ingreso',
                                  'Superávit automático',
                                  'Ningún efecto',
                                  'Salida de divisas',
                                  'Reservas adicionales'],
                 'correcta': 'D'},
                {'pregunta': 'La subcuenta que registra intereses de deuda, '
                             'remesa de utilidades y dividendos se llama:',
                 'alternativas': ['Transferencias Corrientes',
                                  'Cuenta Financiera',
                                  'Renta de Factores',
                                  'Balanza Comercial',
                                  'Balanza de Servicios'],
                 'correcta': 'C'},
                {'pregunta': 'Las remesas de emigrantes se registran dentro '
                             'de:',
                 'alternativas': ['La Renta de Factores',
                                  'El Financiamiento Excepcional',
                                  'La Cuenta Financiera',
                                  'La Balanza Comercial',
                                  'Las Transferencias Corrientes'],
                 'correcta': 'E'},
                {'pregunta': 'La fórmula de la Balanza en Cuenta Corriente '
                             'es BCC = BC + BS + RF +:',
                 'alternativas': ['CF', 'CCP', 'TC', 'SPr', 'DEG'],
                 'correcta': 'C'},
                {'pregunta': 'La Cuenta Financiera registra el ingreso y '
                             'salida de divisas destinadas a inversiones '
                             'productivas o:',
                 'alternativas': ['Comerciales exclusivas',
                                  'De transferencia',
                                  'De donación',
                                  'Especulativas',
                                  'De consumo'],
                 'correcta': 'D'},
                {'pregunta': 'Los capitales que entran o salen de un país en '
                             'periodos menores a un año se llaman capitales:',
                 'alternativas': ['Productivos',
                                  'De largo plazo exclusivos',
                                  'Fijos',
                                  'Estructurales',
                                  'Golondrinos o de corto plazo'],
                 'correcta': 'E'},
                {'pregunta': 'El financiamiento excepcional, o cuenta de '
                             'ajuste, registra préstamos del exterior, '
                             'atrasos en pagos y:',
                 'alternativas': ['Reservas internacionales',
                                  'Exportaciones adicionales',
                                  'Nuevas inversiones',
                                  'Remesas familiares',
                                  'Condonación de deuda'],
                 'correcta': 'E'},
                {'pregunta': 'La deuda externa es el conjunto de '
                             'obligaciones que tiene un país con acreedores '
                             'que residen:',
                 'alternativas': ['Solo en bancos locales',
                                  'En ninguna parte',
                                  'En el extranjero',
                                  'En el mismo país',
                                  'Solo en el gobierno'],
                 'correcta': 'C'},
                {'pregunta': 'La deuda pública, contraída por el Estado, se '
                             'diferencia de la deuda:',
                 'alternativas': ['Municipal',
                                  'Externa exclusiva',
                                  'Interna exclusiva',
                                  'Privada, contraída por empresas y '
                                  'familias',
                                  'Regional'],
                 'correcta': 'D'},
                {'pregunta': 'La deuda cuyos acreedores son ciudadanos de la '
                             'misma nación se llama deuda:',
                 'alternativas': ['Interna',
                                  'Regional',
                                  'Privada exclusiva',
                                  'Externa',
                                  'Pública exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'El Fondo Monetario Internacional (FMI) fue '
                             'fundado en el año:',
                 'alternativas': ['1994', '1945', '1969', '1959', '1944'],
                 'correcta': 'B'},
                {'pregunta': 'El Banco Interamericano de Desarrollo (BID) '
                             'tiene su sede en:',
                 'alternativas': ['Ginebra',
                                  'París',
                                  'Washington',
                                  'Nueva York',
                                  'Bruselas'],
                 'correcta': 'C'},
                {'pregunta': 'El Banco Mundial es una entidad especializada '
                             'de:',
                 'alternativas': ['El FMI exclusivo',
                                  'La Unión Europea',
                                  'La OMC',
                                  'La ONU',
                                  'La OEA'],
                 'correcta': 'D'},
                {'pregunta': 'El Club de París es un espacio de negociación '
                             'entre acreedores oficiales y:',
                 'alternativas': ['Inversionistas individuales',
                                  'Organismos regionales',
                                  'Países deudores',
                                  'Bancos privados',
                                  'Empresas multinacionales'],
                 'correcta': 'C'},
                {'pregunta': 'Un bloque económico se define como un conjunto '
                             'de países que se asocian para impulsar:',
                 'alternativas': ['El intercambio comercial entre ellos',
                                  'El aislamiento económico',
                                  'El proteccionismo extremo',
                                  'La guerra comercial',
                                  'La competencia desleal'],
                 'correcta': 'A'},
                {'pregunta': 'La Unión Europea está formada por un número de '
                             'países igual a:',
                 'alternativas': ['10', '35', '28', '50', '15'],
                 'correcta': 'C'},
                {'pregunta': 'El MERCOSUR fue instituido inicialmente por '
                             'Argentina, Brasil, Uruguay y:',
                 'alternativas': ['Colombia',
                                  'Bolivia',
                                  'Paraguay',
                                  'Perú',
                                  'Chile'],
                 'correcta': 'C'},
                {'pregunta': 'La Comunidad Andina (CAN) se originó del '
                             'Acuerdo de Cartagena, firmado en:',
                 'alternativas': ['1945', '1969', '1959', '1994', '1988'],
                 'correcta': 'B'},
                {'pregunta': 'Los países miembros originales de la Comunidad '
                             'Andina son Bolivia, Colombia, Ecuador y:',
                 'alternativas': ['Perú',
                                  'Brasil',
                                  'Venezuela',
                                  'Chile',
                                  'Argentina'],
                 'correcta': 'A'},
                {'pregunta': 'El NAFTA, tratado de libre comercio de América '
                             'del Norte, entró en vigor en:',
                 'alternativas': ['1969', '1989', '1994', '1959', '2000'],
                 'correcta': 'C'},
                {'pregunta': 'El NAFTA está conformado por Canadá, Estados '
                             'Unidos y:',
                 'alternativas': ['Perú',
                                  'Chile',
                                  'Brasil',
                                  'Colombia',
                                  'México'],
                 'correcta': 'E'},
                {'pregunta': 'Un Tratado de Libre Comercio (TLC) es un '
                             'acuerdo comercial vinculante con preferencias '
                             'arancelarias:',
                 'alternativas': ['Unilaterales',
                                  'Solo para un país',
                                  'Temporales exclusivamente',
                                  'Mutuas',
                                  'Nulas'],
                 'correcta': 'D'},
                {'pregunta': 'Los TLC tienen un plazo:',
                 'alternativas': ['Indefinido, con carácter de perpetuidad',
                                  'De diez años exactos',
                                  'De un año',
                                  'De cinco años exactos',
                                  'Renovable cada mes'],
                 'correcta': 'A'},
                {'pregunta': 'La globalización se define como el aumento '
                             'continuo de la interconexión entre naciones en '
                             'el plano económico, político, social y:',
                 'alternativas': ['Religioso exclusivo',
                                  'Deportivo',
                                  'Tecnológico',
                                  'Militar exclusivo',
                                  'Artístico exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El término «globalización» se utiliza '
                             'ampliamente desde la década de:',
                 'alternativas': ['Los años 2000',
                                  'Los noventa',
                                  'Los setenta',
                                  'Los ochenta',
                                  'Los sesenta'],
                 'correcta': 'D'},
                {'pregunta': 'El capital que se invierte en la compra de '
                             'factores de producción para fabricar bienes se '
                             'llama capital:',
                 'alternativas': ['De reserva',
                                  'Especulativo',
                                  'Comercial',
                                  'Financiero',
                                  'Productivo'],
                 'correcta': 'E'},
                {'pregunta': 'El dinero invertido en otro país como '
                             'inversión directa extranjera o mediante '
                             'créditos se llama capital:',
                 'alternativas': ['Fijo',
                                  'Financiero',
                                  'Productivo',
                                  'De reserva',
                                  'Comercial'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los actores de la globalización están '
                             'los bancos multinacionales y las empresas:',
                 'alternativas': ['Artesanales',
                                  'Familiares',
                                  'Estatales exclusivas',
                                  'Locales exclusivas',
                                  'Multinacionales'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE SECTOR EXTERNO / TEORÍAS DEL '
                                'COMERCIO INTERNACIONAL',
                      'items': ['Ningún país tiene una economía autárquica; '
                                'requiere bienes y servicios de otros países '
                                'para su desarrollo.',
                                'Los mercantilistas postulaban que un país '
                                'debía exportar todo lo posible e importar '
                                'solo lo necesario, recibiendo metales '
                                'preciosos como pago.']},
                     {'titulo': 'FORMAS DE COMERCIO INTERNACIONAL / '
                                'ELEMENTOS DEL COMERCIO INTERNACIONAL',
                      'items': ['Las exportaciones son la venta de bienes y '
                                'servicios nacionales al resto del mundo, y '
                                'generan ingreso de divisas.',
                                'Las divisas son moneda extranjera que usan '
                                'los residentes de un país para '
                                'transacciones internacionales; deben ser '
                                'monedas duras.']},
                     {'titulo': 'EL TIPO DE CAMBIO / LA BALANZA DE PAGOS',
                      'items': ['El tipo de cambio es el precio de una '
                                'moneda expresado en términos de otra.',
                                'La balanza de pagos es el registro contable '
                                'de todas las transacciones económicas y '
                                'financieras de un país con el resto del '
                                'mundo.']},
                     {'titulo': 'LA CUENTA FINANCIERA / FINANCIAMIENTO '
                                'EXCEPCIONAL Y DEUDA EXTERNA',
                      'items': ['La Cuenta Financiera (CF) registra el '
                                'ingreso y salida de divisas destinadas a '
                                'inversiones productivas o especulativas.',
                                'El financiamiento excepcional, o cuenta de '
                                'ajuste, registra préstamos del exterior, '
                                'atrasos en pagos y condonación de deuda.']},
                     {'titulo': 'CLASES DE DEUDA Y CARACTERÍSTICAS / '
                                'ORGANISMOS MULTILATERALES',
                      'items': ['La deuda interna es la porción de la deuda '
                                'pública cuyos acreedores son ciudadanos de '
                                'la misma nación.',
                                'El Fondo Monetario Internacional (FMI), '
                                'fundado en 1945, fomenta la cooperación '
                                'monetaria y la estabilidad financiera.']},
                     {'titulo': 'BLOQUES ECONÓMICOS / TRATADOS DE LIBRE '
                                'COMERCIO',
                      'items': ['Un bloque económico es un conjunto de '
                                'países que se asocian para impulsar el '
                                'intercambio comercial entre ellos, bajando '
                                'aranceles mutuos.',
                                'Un Tratado de Libre Comercio (TLC) es un '
                                'acuerdo comercial vinculante entre dos o '
                                'más países, con preferencias arancelarias '
                                'mutuas.']},
                     {'titulo': 'LA GLOBALIZACIÓN',
                      'items': ['La globalización es el aumento continuo de '
                                'la interconexión entre naciones en el plano '
                                'económico, político, social y '
                                'tecnológico.']}]},
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
                {'titulo': '17.5 TIPOS Y EJEMPLOS DE CRISIS ECONÓMICAS',
                 'items': ['La {crisis de oferta} ocurre cuando hay '
                           'problemas en la oferta y no se puede cubrir el '
                           'total {demandado}.',
                           'La {crisis de demanda} ocurre cuando no es '
                           'posible comercializar todo el stock, generando '
                           '{estancamiento} del mercado.',
                           'La {crisis energética} ocurre cuando el alto '
                           'precio de la energía se traslada a los productos '
                           'de consumo, generando {inflación}.',
                           'La {crisis financiera} ocurre cuando hay falta '
                           'de confianza en el sector financiero y se '
                           'desploma el valor en la {bolsa}.',
                           'La {crisis cambiaria} ocurre cuando un país no '
                           'puede defender el valor de su moneda, '
                           'produciéndose una {devaluación}.',
                           'La crisis de {1929}, llamada «Gran Depresión», '
                           'fue una crisis financiera causada por la caída '
                           'de la bolsa de {Estados Unidos}.',
                           'La crisis económica del {2008} fue causada por '
                           'el colapso de la burbuja {inmobiliaria} de '
                           'Estados Unidos.',
                           'La crisis económica de {2020} fue causada por la '
                           'pandemia del {COVID-19}, afectando '
                           'principalmente al sector terciario.']},
                {'titulo': '17.6 LA POLÍTICA ECONÓMICA',
                 'items': ['La {política económica} es el conjunto de '
                           'medidas que adopta un Gobierno para alcanzar '
                           'objetivos concretos en materia {económica}.',
                           'La intervención del Gobierno se caracteriza por '
                           'la imposición {coactiva} de sus decisiones sobre '
                           'el sector público y {privado}.',
                           'Para la previsión económica se analizan {series '
                           'temporales}: datos ordenados en el tiempo, '
                           'tomados en periodos {regulares}.']},
                {'titulo': '17.7 POLÍTICA MONETARIA Y FISCAL',
                 'items': ['La {política monetaria} regula el crédito en el '
                           'sistema financiero para lograr la {estabilidad} '
                           'del valor del dinero.',
                           'El objetivo inmediato de la política monetaria '
                           'es el control de la {oferta monetaria} o '
                           'liquidez del sistema financiero.',
                           'Una política monetaria {expansiva} '
                           '(reactivadora) aumenta la oferta monetaria, '
                           'reduce la tasa de interés y posibilita mayor '
                           '{inversión}.',
                           'Una política monetaria {contractiva} (recesiva) '
                           'se orienta a controlar la {inflación} y '
                           'estabilizar la economía.',
                           'La formulación de la política monetaria en el '
                           'Perú está a cargo del {Banco Central de Reserva} '
                           '(BCRP).',
                           'La {política fiscal} administra los ingresos, '
                           'gastos y financiamiento del sector público, '
                           'mediante el manejo del {Presupuesto Público}.']},
                {'titulo': '17.8 INSTRUMENTOS DE LA POLÍTICA MONETARIA',
                 'items': ['Las {Operaciones de Mercado Abierto} son la '
                           'compra y venta de activos financieros para '
                           'aumentar o disminuir la {masa monetaria}.',
                           'Las {Operaciones de Redescuento} son cuando el '
                           'banco central descuenta letras que los bancos '
                           'comerciales ya descontaron a sus {clientes}.',
                           'El {Encaje Legal} son reservas de activos '
                           'líquidos que las empresas del sistema financiero '
                           'deben mantener para fines de {regulación} '
                           'monetaria.']}],
  'cuadros': [{'titulo': '17.2 LAS CUATRO FASES DEL CICLO ECONÓMICO',
               'encabezados': ['Fase', 'Característica principal'],
               'filas': [['{Depresión}', 'Fuerte {desempleo}'],
                         ['{Recuperación}', 'Crece la {producción}'],
                         ['{Auge}', '{Optimismo} e inestabilidad'],
                         ['{Recesión}', 'Se frenan las {inversiones}']]}],
  'preguntas': [{'pregunta': 'El proceso económico se desarrolla, según el '
                             'texto, de manera:',
                 'alternativas': ['Cíclica, con abundancia y retroceso',
                                  'Lineal y continua',
                                  'Sin ningún patrón',
                                  'Siempre descendente',
                                  'Siempre ascendente'],
                 'correcta': 'A'},
                {'pregunta': 'La fase del ciclo caracterizada por fuerte '
                             'desempleo y caída de la demanda es:',
                 'alternativas': ['El auge',
                                  'El crecimiento',
                                  'La recuperación',
                                  'La recesión',
                                  'La depresión'],
                 'correcta': 'E'},
                {'pregunta': 'La fase donde crece la producción, el empleo y '
                             'el ingreso se llama:',
                 'alternativas': ['Depresión',
                                  'Estancamiento',
                                  'Recesión',
                                  'Recuperación',
                                  'Crisis'],
                 'correcta': 'D'},
                {'pregunta': 'La fase en que se recuperan todos los sectores '
                             'de la economía, con pleno empleo, se llama:',
                 'alternativas': ['Depresión',
                                  'Subconsumo',
                                  'Auge',
                                  'Recesión',
                                  'Subproducción'],
                 'correcta': 'D'},
                {'pregunta': 'La fase que inicia con la inestabilidad del '
                             'auge, frenando las inversiones, se llama:',
                 'alternativas': ['Auge sostenido',
                                  'Superproducción',
                                  'Recesión',
                                  'Depresión total inmediata',
                                  'Recuperación'],
                 'correcta': 'C'},
                {'pregunta': 'El final de la recesión, según el texto, '
                             'conduce a:',
                 'alternativas': ['El crecimiento sostenido',
                                  'La depresión',
                                  'La recuperación inmediata',
                                  'El auge directamente',
                                  'La estabilidad total'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis económica se define como la '
                             'alteración o perturbación de:',
                 'alternativas': ['Solo el clima',
                                  'Solo el sistema educativo',
                                  'Solo el sistema político',
                                  'Solo la demografía',
                                  'El proceso económico'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis puede afectar al sector real, que '
                             'comprende producción, consumo e inversión, y '
                             'al sector:',
                 'alternativas': ['Cultural',
                                  'Educativo',
                                  'Deportivo',
                                  'Religioso',
                                  'Monetario'],
                 'correcta': 'E'},
                {'pregunta': 'La característica de la crisis que implica que '
                             'se presenta cada cierto tiempo se llama:',
                 'alternativas': ['Periodicidad',
                                  'Intensidad',
                                  'Sincronía',
                                  'Propagación',
                                  'Estabilidad'],
                 'correcta': 'A'},
                {'pregunta': 'En la economía peruana, las crisis se han '
                             'presentado con una periodicidad aproximada de:',
                 'alternativas': ['50 años',
                                  '1 a 2 años',
                                  '20 a 30 años',
                                  'Cada mes',
                                  '8 a 10 años'],
                 'correcta': 'E'},
                {'pregunta': 'La característica de la crisis que implica que '
                             'se inicia en un sector y afecta a otros se '
                             'llama:',
                 'alternativas': ['Tendencia a propagarse',
                                  'Periodicidad',
                                  'Estabilidad',
                                  'Regularidad exacta',
                                  'Intensidad uniforme'],
                 'correcta': 'A'},
                {'pregunta': 'El efecto por el cual una crisis se traslada '
                             'de un sector a otro se conoce como efecto:',
                 'alternativas': ['Rebote',
                                  'Multiplicador exclusivo',
                                  'Boomerang',
                                  'Elástico',
                                  'Dominó'],
                 'correcta': 'E'},
                {'pregunta': 'La característica de la crisis según la cual '
                             'afecta más a unos países que a otros se llama:',
                 'alternativas': ['Periodicidad',
                                  'Regularidad',
                                  'Uniformidad',
                                  'Distinta intensidad',
                                  'Propagación'],
                 'correcta': 'D'},
                {'pregunta': 'Los países desarrollados, frente a una crisis, '
                             'suelen:',
                 'alternativas': ['No verse afectados nunca',
                                  'Superarla con mayor dificultad',
                                  'Ser inmunes a toda crisis',
                                  'Sufrir siempre más que los demás',
                                  'Superarla con mayor rapidez'],
                 'correcta': 'E'},
                {'pregunta': 'El síntoma más alarmante y preciso de una '
                             'crisis económica es:',
                 'alternativas': ['La disminución del desempleo',
                                  'El incremento de los precios',
                                  'El crecimiento sostenido',
                                  'La reducción de precios',
                                  'El aumento del ahorro'],
                 'correcta': 'B'},
                {'pregunta': 'La producción excesiva de bienes sin salida en '
                             'los mercados se llama:',
                 'alternativas': ['Hiperinflación',
                                  'Subconsumo',
                                  'Subempleo',
                                  'Subproducción',
                                  'Superproducción o sobreproducción'],
                 'correcta': 'E'},
                {'pregunta': 'La escasez de bienes y servicios en el '
                             'mercado, asociada a economías de bajo '
                             'desarrollo, se llama:',
                 'alternativas': ['Subconsumo',
                                  'Subproducción',
                                  'Hiperinflación',
                                  'Superproducción',
                                  'Sobreoferta'],
                 'correcta': 'B'},
                {'pregunta': 'El problema que se agrava cuando mucha gente '
                             'carece de capacidad adquisitiva se llama:',
                 'alternativas': ['Subproducción exclusiva',
                                  'Hiperinflación',
                                  'Subconsumo',
                                  'Superproducción',
                                  'Deflación'],
                 'correcta': 'C'},
                {'pregunta': 'Entre los síntomas de la crisis figura la '
                             'caída en las cotizaciones de los valores '
                             'mobiliarios en:',
                 'alternativas': ['El comercio informal',
                                  'El mercado laboral',
                                  'El sector agrícola',
                                  'El turismo',
                                  'La bolsa de valores'],
                 'correcta': 'E'},
                {'pregunta': 'Las causas de la crisis que afectan '
                             'directamente a la actividad económica se '
                             'llaman causas:',
                 'alternativas': ['Climáticas',
                                  'Sociales exclusivas',
                                  'Exógenas',
                                  'Culturales',
                                  'Endógenas o económicas'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis que ocurre cuando hay problemas en '
                             'la oferta y no se puede cubrir el total '
                             'demandado se llama crisis de:',
                 'alternativas': ['Confianza',
                                  'Demanda',
                                  'Liquidez',
                                  'Oferta',
                                  'Cambio'],
                 'correcta': 'D'},
                {'pregunta': 'La crisis que ocurre cuando no es posible '
                             'comercializar todo el stock disponible se '
                             'llama crisis de:',
                 'alternativas': ['Oferta',
                                  'Demanda',
                                  'Confianza',
                                  'Energía',
                                  'Cambio'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis en la que el alto precio de la '
                             'energía se traslada a los productos de consumo '
                             'se llama crisis:',
                 'alternativas': ['De oferta',
                                  'De demanda',
                                  'Financiera',
                                  'Cambiaria',
                                  'Energética'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis causada por la falta de confianza en '
                             'el sector financiero y el desplome de la bolsa '
                             'se llama crisis:',
                 'alternativas': ['De demanda',
                                  'Energética',
                                  'De oferta',
                                  'Cambiaria',
                                  'Financiera'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis en la que un país no puede defender '
                             'el valor de su moneda, produciendo una '
                             'devaluación, se llama crisis:',
                 'alternativas': ['De oferta',
                                  'Financiera',
                                  'Cambiaria',
                                  'De demanda',
                                  'Energética'],
                 'correcta': 'C'},
                {'pregunta': 'La crisis de 1929, llamada «Gran Depresión», '
                             'fue causada por la caída de la bolsa de:',
                 'alternativas': ['Alemania',
                                  'Reino Unido',
                                  'Japón',
                                  'Estados Unidos',
                                  'Francia'],
                 'correcta': 'D'},
                {'pregunta': 'La crisis económica del 2008 fue causada por '
                             'el colapso de la burbuja:',
                 'alternativas': ['Tecnológica',
                                  'Petrolera',
                                  'Cambiaria',
                                  'Agrícola',
                                  'Inmobiliaria'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis económica del 2020 fue causada '
                             'principalmente por:',
                 'alternativas': ['Un desastre natural',
                                  'Una crisis bancaria',
                                  'Una hiperinflación',
                                  'Una guerra comercial',
                                  'La pandemia del COVID-19'],
                 'correcta': 'E'},
                {'pregunta': 'La política económica se define como el '
                             'conjunto de medidas que adopta el Gobierno '
                             'para alcanzar objetivos concretos en materia:',
                 'alternativas': ['Religiosa',
                                  'Económica',
                                  'Deportiva',
                                  'Artística',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'La intervención del Gobierno en la economía se '
                             'caracteriza por la imposición de sus '
                             'decisiones de forma:',
                 'alternativas': ['Opcional',
                                  'Coactiva',
                                  'Voluntaria',
                                  'Simbólica',
                                  'Consultiva exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Para la previsión económica se analizan datos '
                             'ordenados en el tiempo, tomados en periodos '
                             'regulares, llamados:',
                 'alternativas': ['Índices simples',
                                  'Series temporales',
                                  'Encuestas',
                                  'Datos aleatorios',
                                  'Muestras únicas'],
                 'correcta': 'B'},
                {'pregunta': 'La política monetaria regula el crédito en el '
                             'sistema financiero para lograr:',
                 'alternativas': ['El desempleo',
                                  'La recesión permanente',
                                  'La devaluación constante',
                                  'La estabilidad del valor del dinero',
                                  'El aumento de precios'],
                 'correcta': 'D'},
                {'pregunta': 'El objetivo inmediato de la política monetaria '
                             'es el control de:',
                 'alternativas': ['El gasto público',
                                  'Los impuestos exclusivamente',
                                  'Las exportaciones',
                                  'La oferta monetaria o liquidez',
                                  'La deuda pública exclusiva'],
                 'correcta': 'D'},
                {'pregunta': 'Una política monetaria que aumenta la oferta '
                             'monetaria y reduce la tasa de interés se llama '
                             'política:',
                 'alternativas': ['Fiscal exclusiva',
                                  'Contractiva',
                                  'Neutra',
                                  'Expansiva',
                                  'Cambiaria'],
                 'correcta': 'D'},
                {'pregunta': 'Una política monetaria orientada a controlar '
                             'la inflación y estabilizar la economía se '
                             'llama política:',
                 'alternativas': ['Fiscal exclusiva',
                                  'Comercial',
                                  'Contractiva',
                                  'Expansiva',
                                  'Cambiaria'],
                 'correcta': 'C'},
                {'pregunta': 'En el Perú, la formulación de la política '
                             'monetaria está a cargo de:',
                 'alternativas': ['El Banco Central de Reserva (BCRP)',
                                  'El MEF',
                                  'La SBS',
                                  'El Congreso',
                                  'La SUNAT'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la política económica encargada de '
                             'administrar ingresos, gastos y financiamiento '
                             'del sector público se llama política:',
                 'alternativas': ['Comercial',
                                  'Cambiaria',
                                  'Monetaria',
                                  'Fiscal',
                                  'Salarial'],
                 'correcta': 'D'},
                {'pregunta': 'La política fiscal implica en gran medida el '
                             'manejo de:',
                 'alternativas': ['La oferta monetaria',
                                  'El encaje legal',
                                  'La tasa de interés',
                                  'El tipo de cambio',
                                  'El Presupuesto Público'],
                 'correcta': 'E'},
                {'pregunta': 'La compra y venta de activos financieros para '
                             'aumentar o disminuir la masa monetaria se '
                             'llama:',
                 'alternativas': ['Devaluación',
                                  'Política Fiscal',
                                  'Operaciones de Redescuento',
                                  'Encaje Legal',
                                  'Operaciones de Mercado Abierto'],
                 'correcta': 'E'},
                {'pregunta': 'La operación mediante la cual el banco central '
                             'descuenta letras que los bancos comerciales ya '
                             'descontaron a sus clientes se llama:',
                 'alternativas': ['Operaciones de Redescuento',
                                  'Operaciones de Mercado Abierto',
                                  'Encaje Legal',
                                  'Política Fiscal',
                                  'Devaluación'],
                 'correcta': 'A'},
                {'pregunta': 'Las reservas de activos líquidos que las '
                             'empresas del sistema financiero deben mantener '
                             'por regulación se llaman:',
                 'alternativas': ['Encaje Legal',
                                  'Presupuesto Público',
                                  'Redescuento',
                                  'Operaciones de Mercado Abierto',
                                  'Divisas'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DEL CICLO ECONÓMICO',
                      'items': ['El proceso económico no se desarrolla de '
                                'manera lineal y continua, sino por ciclos '
                                'de abundancia y retroceso.']},
                     {'titulo': 'LAS CUATRO FASES DEL CICLO ECONÓMICO',
                      'items': ['La depresión se caracteriza por fuerte '
                                'desempleo, incapacidad de consumo y '
                                'reducción de la demanda.']},
                     {'titulo': 'CONCEPTO Y CARACTERÍSTICAS DE LA CRISIS',
                      'items': ['La crisis económica es la alteración o '
                                'perturbación del proceso económico durante '
                                'un periodo determinado.']},
                     {'titulo': 'SÍNTOMAS Y CAUSAS DE LA CRISIS',
                      'items': ['El síntoma más alarmante y preciso de la '
                                'crisis es el incremento de los precios.']},
                     {'titulo': 'TIPOS Y EJEMPLOS DE CRISIS ECONÓMICAS',
                      'items': ['La crisis de oferta ocurre cuando hay '
                                'problemas en la oferta y no se puede cubrir '
                                'el total demandado.']},
                     {'titulo': 'LA POLÍTICA ECONÓMICA',
                      'items': ['La política económica es el conjunto de '
                                'medidas que adopta un Gobierno para '
                                'alcanzar objetivos concretos en materia '
                                'económica.']},
                     {'titulo': 'POLÍTICA MONETARIA Y FISCAL',
                      'items': ['La política monetaria regula el crédito en '
                                'el sistema financiero para lograr la '
                                'estabilidad del valor del dinero.']},
                     {'titulo': 'INSTRUMENTOS DE LA POLÍTICA MONETARIA',
                      'items': ['Las Operaciones de Mercado Abierto son la '
                                'compra y venta de activos financieros para '
                                'aumentar o disminuir la masa monetaria.']}]},
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
                {'titulo': '18.5 FACTORES DE CRECIMIENTO ECONÓMICO',
                 'items': ['La {inversión en capital} es clave para que los '
                           'trabajadores realicen su labor con mejores '
                           'condiciones y más {herramientas}.',
                           'La {educación}, o inversión en capital humano, '
                           'dota de preparación a los participantes del '
                           'proceso {productivo}.',
                           'La {tecnología} facilita la evolución de los '
                           'modelos de trabajo, las herramientas y la '
                           '{investigación}.']},
                {'titulo': '18.6 MEDICIÓN DEL CRECIMIENTO ECONÓMICO',
                 'items': ['El crecimiento económico se mide por la '
                           'tendencia del {PBI} a través del tiempo, '
                           'hallando su {tasa}.',
                           'Para comparar entre economías, el crecimiento se '
                           'expresa en términos «{per cápita}» o por '
                           'habitante.',
                           'El {PIB per cápita} se calcula dividiendo el '
                           'Producto Interior Bruto entre el número de '
                           '{habitantes}.']},
                {'titulo': '18.7 EL DESARROLLO SOSTENIBLE',
                 'items': ['El {desarrollo sostenible}, o sustentable, '
                           'asegura las necesidades presentes sin '
                           'comprometer la capacidad de las {futuras} '
                           'generaciones.',
                           'El desarrollo sostenible busca una explotación '
                           'más {racional} de los recursos, que cuide el '
                           'medio ambiente y el {planeta}.']},
                {'titulo': '18.8 CARACTERÍSTICAS DEL DESARROLLO SOSTENIBLE',
                 'items': ['El desarrollo sostenible actúa en tres áreas: la '
                           '{sociedad} y las personas, la {economía}, y el '
                           'planeta.',
                           'Entre sus características están el cuidado del '
                           '{agua}, el aumento del {reciclaje}, y la '
                           'protección del medioambiente.',
                           'También incluye la recuperación de '
                           '{ecosistemas}, el uso de tecnologías {limpias}, '
                           'y el aumento de la calidad de {vida}.',
                           'La {autosuficiencia regional} es la capacidad de '
                           'una comunidad de cuidar los recursos naturales '
                           'de su propia {área}.']},
                {'titulo': '18.9 LA ECONOMÍA CIRCULAR',
                 'items': ['La {economía circular} busca mejorar la '
                           'eficiencia en el uso de los recursos, mediante '
                           'el aprovechamiento, la {reutilización} y el '
                           'reciclaje.',
                           'Su objetivo es «cerrar el {ciclo de vida}» de '
                           'los productos, reduciendo el consumo de materias '
                           'primas, agua y {energía}.',
                           'Se opone al modelo {lineal} actual, basado en '
                           '«comprar, usar y {tirar}».',
                           'Entre sus beneficios están el aprovechamiento de '
                           'recursos, la reducción de {residuos} y gases '
                           'contaminantes, y el ahorro {empresarial}.',
                           'Según el Parlamento Europeo, la economía '
                           'circular podría generar cerca de {580 000} '
                           'empleos en toda la Unión Europea.']}],
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
                 'alternativas': ['Pobreza',
                                  'Desempleo',
                                  'Riqueza',
                                  'Inflación',
                                  'Deuda'],
                 'correcta': 'C'},
                {'pregunta': 'El desarrollo económico debe reflejarse en:',
                 'alternativas': ['Solo el tipo de cambio',
                                  'La calidad de vida de los habitantes',
                                  'Solo el PBI total',
                                  'Solo las exportaciones',
                                  'Solo la inversión extranjera'],
                 'correcta': 'B'},
                {'pregunta': 'El crecimiento económico implica un incremento '
                             'significativo de:',
                 'alternativas': ['Los ingresos o renta per cápita',
                                  'La deuda externa',
                                  'El desempleo',
                                  'La inflación',
                                  'La pobreza'],
                 'correcta': 'A'},
                {'pregunta': 'La fórmula más eficaz para medir el bienestar '
                             'de un pueblo, según el texto, es:',
                 'alternativas': ['El tipo de cambio',
                                  'El PBI nominal',
                                  'El IDH (Índice de Desarrollo Humano)',
                                  'La balanza comercial',
                                  'La tasa de interés'],
                 'correcta': 'C'},
                {'pregunta': 'Una característica del desarrollo económico es '
                             'que el país utiliza sus recursos potenciales '
                             'con:',
                 'alternativas': ['Alto capital ocioso',
                                  'Ningún recurso disponible',
                                  'Solo recursos importados',
                                  'Recursos completamente agotados',
                                  'Muy poco capital ocioso'],
                 'correcta': 'E'},
                {'pregunta': 'El desarrollo económico requiere que el '
                             'crecimiento sea:',
                 'alternativas': ['Sin ninguna base productiva',
                                  'Sostenible, con buenos fundamentos',
                                  'Solo a corto plazo',
                                  'Dependiente exclusivamente de la '
                                  'exportación',
                                  'Temporal y aislado'],
                 'correcta': 'B'},
                {'pregunta': 'El desarrollo económico implica una '
                             'conciencia:',
                 'alternativas': ['Solo financiera',
                                  'Solo militar',
                                  'Medioambiental',
                                  'Solo comercial',
                                  'Solo religiosa'],
                 'correcta': 'C'},
                {'pregunta': 'El desarrollo económico requiere orden social, '
                             'es decir, instituciones públicas:',
                 'alternativas': ['Sin ninguna regulación',
                                  'Débiles y sin control',
                                  'Privatizadas totalmente',
                                  'Confiables que cumplen sus funciones',
                                  'Innecesarias'],
                 'correcta': 'D'},
                {'pregunta': 'El Índice de Desarrollo Humano (IDH) fue '
                             'creado por:',
                 'alternativas': ['El FMI',
                                  'La OMC',
                                  'La OCDE',
                                  'El Banco Mundial',
                                  'El Programa de las Naciones Unidas para '
                                  'el Desarrollo (PNUD)'],
                 'correcta': 'E'},
                {'pregunta': 'El IDH considera la esperanza de vida al '
                             'nacer, la educación y:',
                 'alternativas': ['La inflación',
                                  'El tipo de cambio',
                                  'El PIB per cápita',
                                  'El desempleo',
                                  'La tasa de interés'],
                 'correcta': 'C'},
                {'pregunta': 'La variable del IDH que analiza el promedio de '
                             'edad de las personas fallecidas se llama:',
                 'alternativas': ['Educación',
                                  'Esperanza de vida al nacer',
                                  'PIB per cápita',
                                  'Mortalidad infantil',
                                  'Tasa de natalidad'],
                 'correcta': 'B'},
                {'pregunta': 'La variable del IDH que recoge el nivel de '
                             'alfabetización y estudios alcanzados es:',
                 'alternativas': ['Ingreso nacional',
                                  'Educación',
                                  'PIB per cápita',
                                  'Esperanza de vida',
                                  'Empleo'],
                 'correcta': 'B'},
                {'pregunta': 'La variable del IDH que evalúa el acceso a los '
                             'recursos económicos necesarios es:',
                 'alternativas': ['PIB per cápita',
                                  'Educación',
                                  'Balanza comercial',
                                  'Tasa de interés',
                                  'Esperanza de vida'],
                 'correcta': 'B'},
                {'pregunta': 'El IDH otorga valores en un rango de:',
                 'alternativas': ['-1 a 1',
                                  '0 a 1',
                                  '0 a 1000',
                                  '1 a 10',
                                  '0 a 100'],
                 'correcta': 'B'},
                {'pregunta': 'En el IDH, el valor más alto de desarrollo '
                             'corresponde a:',
                 'alternativas': ['50', '-1', '100', '0', '1'],
                 'correcta': 'E'},
                {'pregunta': 'El crecimiento económico se define como la '
                             'evolución positiva de los estándares de vida '
                             'medidos por la capacidad productiva y:',
                 'alternativas': ['Solo el clima',
                                  'La renta',
                                  'Solo la religión',
                                  'Solo la población',
                                  'Solo la cultura'],
                 'correcta': 'B'},
                {'pregunta': 'El indicador más utilizado para medir el '
                             'crecimiento económico es:',
                 'alternativas': ['La inflación exclusivamente',
                                  'El tipo de cambio',
                                  'La tasa de interés',
                                  'Las fluctuaciones del PIB',
                                  'El desempleo exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Entre los factores determinantes del '
                             'desarrollo económico figura el acceso a:',
                 'alternativas': ['Solo mano de obra barata',
                                  'Solo comercio informal',
                                  'Solo territorio extenso',
                                  'Solo aranceles bajos',
                                  'Recursos naturales y fuentes de energía'],
                 'correcta': 'E'},
                {'pregunta': 'Otro factor determinante del desarrollo es la '
                             'estabilidad:',
                 'alternativas': ['Solo deportiva',
                                  'Solo cultural',
                                  'Solo religiosa',
                                  'Climática exclusiva',
                                  'Política'],
                 'correcta': 'E'},
                {'pregunta': 'Los países que han logrado el desarrollo, '
                             'según el texto, han invertido principalmente '
                             'en:',
                 'alternativas': ['Solo armamento',
                                  'Solo infraestructura vial',
                                  'Solo turismo',
                                  'Solo minería',
                                  'Sus habitantes'],
                 'correcta': 'E'},
                {'pregunta': 'El factor de crecimiento económico que dota a '
                             'los trabajadores de más herramientas para '
                             'producir se llama:',
                 'alternativas': ['Comercio',
                                  'Inversión en capital',
                                  'Innovación',
                                  'Tecnología',
                                  'Educación'],
                 'correcta': 'B'},
                {'pregunta': 'El factor de crecimiento económico también '
                             'llamado inversión en capital humano es:',
                 'alternativas': ['La tecnología',
                                  'El comercio exterior',
                                  'El ahorro',
                                  'La educación',
                                  'La inversión física'],
                 'correcta': 'D'},
                {'pregunta': 'El factor de crecimiento económico que '
                             'facilita la evolución de herramientas y medios '
                             'de producción es:',
                 'alternativas': ['La educación',
                                  'El consumo',
                                  'La tecnología',
                                  'El ahorro',
                                  'La inversión en capital'],
                 'correcta': 'C'},
                {'pregunta': 'El crecimiento económico se mide, en el '
                             'tiempo, hallando la tasa de:',
                 'alternativas': ['El empleo',
                                  'La inflación',
                                  'El tipo de cambio',
                                  'Las exportaciones',
                                  'El PBI'],
                 'correcta': 'E'},
                {'pregunta': 'Para comparar el crecimiento entre economías '
                             'de distinto tamaño, se expresa en términos:',
                 'alternativas': ['Per cápita o por habitante',
                                  'Absolutos',
                                  'Nominales exclusivos',
                                  'Reales exclusivos',
                                  'Porcentuales del PBI mundial'],
                 'correcta': 'A'},
                {'pregunta': 'El PIB per cápita se calcula dividiendo el PIB '
                             'entre:',
                 'alternativas': ['La superficie del país',
                                  'El número de trabajadores exclusivamente',
                                  'El número de empresas',
                                  'El número de habitantes',
                                  'El número de exportaciones'],
                 'correcta': 'D'},
                {'pregunta': 'El desarrollo sostenible asegura las '
                             'necesidades presentes sin comprometer la '
                             'capacidad de:',
                 'alternativas': ['Las futuras generaciones',
                                  'Ninguna generación',
                                  'Los inversionistas actuales',
                                  'Las empresas actuales',
                                  'El Estado actual'],
                 'correcta': 'A'},
                {'pregunta': 'El desarrollo sostenible actúa en tres áreas: '
                             'la sociedad y las personas, el planeta, y:',
                 'alternativas': ['La tecnología exclusiva',
                                  'El deporte',
                                  'La política',
                                  'La economía',
                                  'La religión'],
                 'correcta': 'D'},
                {'pregunta': 'Entre las características del desarrollo '
                             'sostenible está el cuidado del agua y el '
                             'aumento del:',
                 'alternativas': ['Comercio',
                                  'Consumo',
                                  'Endeudamiento',
                                  'Reciclaje',
                                  'Gasto público'],
                 'correcta': 'D'},
                {'pregunta': 'La capacidad de una comunidad de cuidar los '
                             'recursos naturales de su propia área se llama:',
                 'alternativas': ['Desarrollo sostenible general',
                                  'Autosuficiencia regional',
                                  'Globalización local',
                                  'Economía circular',
                                  'Descentralización'],
                 'correcta': 'B'},
                {'pregunta': 'La economía circular busca mejorar la '
                             'eficiencia en el uso de recursos mediante el '
                             'aprovechamiento y:',
                 'alternativas': ['La exportación exclusiva',
                                  'El consumo excesivo',
                                  'La importación masiva',
                                  'La reutilización y el reciclaje',
                                  'El almacenamiento indefinido'],
                 'correcta': 'D'},
                {'pregunta': 'El objetivo de la economía circular es «cerrar '
                             'el ciclo de vida» de los productos, reduciendo '
                             'el consumo de materias primas, agua y:',
                 'alternativas': ['Capital',
                                  'Trabajo',
                                  'Energía',
                                  'Tiempo',
                                  'Dinero'],
                 'correcta': 'C'},
                {'pregunta': 'La economía circular se opone al modelo lineal '
                             'actual, basado en «comprar, usar y»:',
                 'alternativas': ['Guardar',
                                  'Reparar',
                                  'Vender',
                                  'Tirar',
                                  'Reciclar'],
                 'correcta': 'D'},
                {'pregunta': 'Según el Parlamento Europeo, la economía '
                             'circular podría generar en la Unión Europea '
                             'aproximadamente:',
                 'alternativas': ['2 millones de empleos',
                                  '5 000 empleos',
                                  '580 000 empleos',
                                  '100 000 empleos',
                                  '50 000 empleos'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE DESARROLLO ECONÓMICO / '
                                'CARACTERÍSTICAS DEL DESARROLLO ECONÓMICO',
                      'items': ['El desarrollo económico es la capacidad de '
                                'un país para generar riqueza, reflejada en '
                                'la calidad de vida de sus habitantes.',
                                'El país con desarrollo económico utiliza '
                                'sus recursos potenciales, con muy poco '
                                'capital ocioso.']},
                     {'titulo': 'EL ÍNDICE DE DESARROLLO HUMANO (IDH) / '
                                'CRECIMIENTO ECONÓMICO',
                      'items': ['El IDH fue creado por el Programa de las '
                                'Naciones Unidas para el Desarrollo (PNUD).',
                                'El crecimiento económico es la evolución '
                                'positiva de los estándares de vida, medida '
                                'por la capacidad productiva y la renta.']},
                     {'titulo': 'FACTORES DE CRECIMIENTO ECONÓMICO / '
                                'MEDICIÓN DEL CRECIMIENTO ECONÓMICO',
                      'items': ['La inversión en capital es clave para que '
                                'los trabajadores realicen su labor con '
                                'mejores condiciones y más herramientas.',
                                'El crecimiento económico se mide por la '
                                'tendencia del PBI a través del tiempo, '
                                'hallando su tasa.']},
                     {'titulo': 'EL DESARROLLO SOSTENIBLE / CARACTERÍSTICAS '
                                'DEL DESARROLLO SOSTENIBLE',
                      'items': ['El desarrollo sostenible, o sustentable, '
                                'asegura las necesidades presentes sin '
                                'comprometer la capacidad de las futuras '
                                'generaciones.',
                                'El desarrollo sostenible actúa en tres '
                                'áreas: la sociedad y las personas, la '
                                'economía, y el planeta.']},
                     {'titulo': 'LA ECONOMÍA CIRCULAR',
                      'items': ['La economía circular busca mejorar la '
                                'eficiencia en el uso de los recursos, '
                                'mediante el aprovechamiento, la '
                                'reutilización y el reciclaje.']}]}]
