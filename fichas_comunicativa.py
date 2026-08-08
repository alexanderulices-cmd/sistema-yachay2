# ================================================================
# FICHAS DE COMPETENCIA COMUNICATIVA — CEPRU UNSAAC
# Basado en el material oficial «Competencia Comunicativa», Área A.
# ================================================================
"""Mismo formato que Historia: por cada balota, ficha de texto para
completar a dos columnas y banco de 20 preguntas, en versión alumno y
versión docente. Reutiliza el motor de fichas_historia.py.

ESTADO: 3 de 16 temas completos. Los 13 restantes se agregan por
tandas, igual que se hizo con Geografía y Cívica.

Integración: se usa a través de academia_cepru.py, no directamente.
"""

import io

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)


COMUNICATIVA_TEMAS = [{'num': 1,
  'titulo': 'La Comunicación',
  'secciones': [{'titulo': '1.1 CONCEPTO Y FASES',
                 'items': ['La comunicación es el acto, hecho o proceso a '
                           'través del cual dos o más individuos '
                           '{interactúan} para intercambiar información, '
                           'ideas o sentimientos.',
                           'La fase {psíquica} de la comunicación está '
                           'constituida por la codificación del emisor y la '
                           'decodificación del receptor.',
                           'La fase {fisiológica} se refiere al '
                           'funcionamiento del aparato fonador y de la '
                           'audición.',
                           'La fase {física} abarca el desplazamiento del '
                           'mensaje a través de canales naturales o '
                           'artificiales.']},
                {'titulo': '1.2 ELEMENTOS DE LA COMUNICACIÓN',
                 'items': ['El {emisor} o hablante es quien codifica el '
                           'mensaje mentalmente y lo transmite a su '
                           'interlocutor.',
                           'El {receptor} u oyente percibe el mensaje y lo '
                           'decodifica para comprender lo que el emisor '
                           'quiso comunicar.',
                           'El {canal} es el medio físico a través del cual '
                           'se transporta el mensaje, como el aire o '
                           'internet.',
                           'El {código} es el sistema de signos '
                           'convencionales que emisor y receptor conocen '
                           'para construir el mensaje.',
                           'El {mensaje} es la información o contenido que '
                           'el emisor quiere dar a conocer al receptor.',
                           'El {referente} es el conjunto de objetos o '
                           'fenómenos de la realidad a los que se hace '
                           'mención en el acto comunicativo.',
                           'La {circunstancia}, también llamada situación o '
                           'contexto, comprende el lugar, momento y '
                           'condiciones del acto comunicativo.']},
                {'titulo': '1.3 CLASES DE COMUNICACIÓN POR EL CÓDIGO',
                 'items': ['La comunicación {lingüística} utiliza el idioma '
                           'para codificar el mensaje, de forma oral o '
                           'escrita.',
                           'La comunicación oral desarrolla una interacción '
                           '{sincrónica} y es momentánea o efímera.',
                           'La comunicación escrita se desarrolla de manera '
                           '{asincrónica} y requiere planificación previa '
                           'del texto.',
                           'La comunicación {no lingüística} utiliza '
                           'cualquier medio ajeno a la palabra oral o '
                           'escrita.',
                           'La {kinésica} estudia los movimientos '
                           'corporales, posturas y gestos.',
                           'La {proxémica} estudia las relaciones de '
                           'proximidad o alejamiento entre los '
                           'interlocutores.',
                           'La {cronémica} estudia el uso del tiempo durante '
                           'la comunicación.']},
                {'titulo': '1.4 CLASES DE COMUNICACIÓN POR LA RELACIÓN '
                           'EMISOR-RECEPTOR',
                 'items': ['La comunicación {intrapersonal} se produce en '
                           'una misma persona, como en el monólogo interior.',
                           'La comunicación {interpersonal} se produce '
                           'cuando interactúan dos personas.',
                           'La comunicación {grupal} se da cuando un '
                           'conjunto de personas transfiere mensajes en '
                           'busca de objetivos comunes.',
                           'La comunicación {pública} es la interacción '
                           'entre ciudadanos y medios de comunicación '
                           'masivos.']},
                {'titulo': '1.5 FUNCIONES DE LA COMUNICACIÓN',
                 'items': ['La función {social} permite al comunicador '
                           'interactuar apropiadamente según las situaciones '
                           'sociales de los diferentes {estratos}.',
                           'La función {simbólica} representa hechos, '
                           'objetos o sentimientos por medio de símbolos, '
                           'señales y {signos}.',
                           'La función {lingüística} está ligada al estilo '
                           'del lenguaje usado en el mensaje: formal, '
                           'informal, especializado, {culto}, estándar, etc.',
                           'La función {organizativa} ordena a las personas '
                           'por puestos, estratos y jerarquías, generando '
                           '{normas}, roles y funciones.',
                           'La función {cultural} transmite hábitos, '
                           'costumbres, valores y creencias que conforman la '
                           '{cultura} de un grupo.']},
                {'titulo': '1.6 NATURALEZA DE LA COMUNICACIÓN',
                 'items': ['El carácter {integrador} implica que la '
                           'comunicación se integra con personas que tienen '
                           'la posibilidad de relacionarse y {conocerse}.',
                           'El carácter {transaccional} se da por la '
                           'interacción de personas que pueden comunicarse '
                           'entre sí y logran {entenderse}.',
                           'El carácter {dinámico} implica que la '
                           'comunicación fluye de forma continua, en cambio '
                           '{constante}.',
                           'El carácter {recíproco} implica que, por medio '
                           'de la comunicación, los hombres ejercen una '
                           'influencia {mutua}.']},
                {'titulo': '1.7 FACTORES QUE INFLUYEN EN LA COMUNICACIÓN',
                 'items': ['El {nivel de conocimiento} es la cantidad y '
                           'calidad de información que se tiene acerca del '
                           '{referente}.',
                           'La {competencia lexicológica} es el dominio del '
                           'vocabulario del código lingüístico; permite '
                           'hablar y escribir con {claridad}.',
                           'Las {actitudes} son los comportamientos, '
                           'motivaciones y reacciones que adoptamos, como el '
                           'interés, el {nerviosismo} o la duda.',
                           'El {contexto sociocultural} considera el sistema '
                           'social o los estratos sociales en que se da el '
                           '{intercambio} de información.']},
                {'titulo': '1.8 EL RUIDO Y LA REDUNDANCIA',
                 'items': ['El {ruido} es el factor de degradación que '
                           'distorsiona la calidad del mensaje o cualquier '
                           'interferencia ajena a los elementos de la '
                           '{comunicación}.',
                           'Los {ruidos no intencionados} incluyen el ruido '
                           'físico, fisiológico, psicológico y {semántico}.',
                           'El ruido {físico} ocurre en el ambiente, como '
                           'interferencias en el {canal}: distorsiones '
                           'sonoras, baja señal de internet.',
                           'El ruido {fisiológico} surge por defectos '
                           'orgánicos de los interlocutores, como '
                           'alteraciones {visuales} y auditivas.',
                           'El ruido {psicológico} se produce en el interior '
                           'del individuo: emociones, miedo, {ansiedad}.',
                           'El ruido {semántico} ocurre cuando el receptor '
                           'interpreta las palabras del emisor de manera '
                           '{distinta} a la intención original.',
                           'Los {ruidos intencionados} incluyen el ruido '
                           'técnico o blanco, como omitir deliberadamente '
                           'parte del {mensaje}.',
                           'La {redundancia} es el factor de '
                           'perfeccionamiento que reduce los efectos del '
                           'ruido, reforzando la {claridad} del mensaje.']}],
  'cuadros': [{'titulo': '1.3 DISCIPLINAS DE LA COMUNICACIÓN NO LINGÜÍSTICA',
               'encabezados': ['Disciplina', 'Estudia'],
               'filas': [['{Kinésica}', 'Movimientos, posturas y {gestos}'],
                         ['{Proxémica}',
                          'Relaciones de {proximidad} o alejamiento'],
                         ['{Oculésica}', 'El {contacto} ocular'],
                         ['{Háptica}', 'El contacto físico y sus {efectos}'],
                         ['{Cronémica}', 'El uso del {tiempo}']]},
              {'titulo': 'LAS 5 FUNCIONES DE LA COMUNICACIÓN',
               'despues_de': '1.5 FUNCIONES DE LA COMUNICACIÓN',
               'encabezados': ['Función', 'Se manifiesta en...'],
               'filas': [['{Social}',
                          'Roles dentro de un sistema social: laboral, '
                          'familiar, {religioso}'],
                         ['{Simbólica}',
                          'Representación mediante símbolos, señales y '
                          '{signos}'],
                         ['{Lingüística}',
                          'Estilo del mensaje: formal, informal, {culto}, '
                          'popular'],
                         ['{Organizativa}',
                          'Jerarquías, normas y roles en una {estructura} '
                          'social'],
                         ['{Cultural}',
                          'Transmisión de hábitos, costumbres y '
                          '{valores}']]}],
  'preguntas': [{'pregunta': 'La comunicación se define como el proceso a '
                             'través del cual dos o más individuos:',
                 'alternativas': ['Interactúan para intercambiar información',
                                  'Compiten entre sí',
                                  'Ejercen autoridad',
                                  'Compran bienes',
                                  'Se aíslan mutuamente'],
                 'correcta': 'A'},
                {'pregunta': 'La fase de la comunicación constituida por la '
                             'codificación y decodificación mental es la '
                             'fase:',
                 'alternativas': ['Física',
                                  'Cultural',
                                  'Fisiológica',
                                  'Social',
                                  'Psíquica'],
                 'correcta': 'E'},
                {'pregunta': 'La fase que se refiere al funcionamiento del '
                             'aparato fonador y la audición es la fase:',
                 'alternativas': ['Semántica',
                                  'Social',
                                  'Fisiológica',
                                  'Psíquica',
                                  'Física'],
                 'correcta': 'C'},
                {'pregunta': 'El elemento de la comunicación que codifica y '
                             'transmite el mensaje es:',
                 'alternativas': ['El referente',
                                  'El receptor',
                                  'El código',
                                  'El canal',
                                  'El emisor'],
                 'correcta': 'E'},
                {'pregunta': 'El elemento que percibe y decodifica el '
                             'mensaje es:',
                 'alternativas': ['El código',
                                  'El canal',
                                  'El emisor',
                                  'El receptor',
                                  'El mensaje'],
                 'correcta': 'D'},
                {'pregunta': 'El medio físico a través del cual se '
                             'transporta el mensaje se llama:',
                 'alternativas': ['Código',
                                  'Emisor',
                                  'Referente',
                                  'Circunstancia',
                                  'Canal'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema de signos convencionales que usan '
                             'emisor y receptor se llama:',
                 'alternativas': ['Referente',
                                  'Código',
                                  'Mensaje',
                                  'Circunstancia',
                                  'Canal'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de objetos o fenómenos a los que '
                             'se hace mención en el acto comunicativo es:',
                 'alternativas': ['El canal',
                                  'El referente',
                                  'El emisor',
                                  'El receptor',
                                  'El código'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar y momento en que se desarrolla el '
                             'acto comunicativo se denomina:',
                 'alternativas': ['Mensaje',
                                  'Referente',
                                  'Circunstancia o contexto',
                                  'Canal',
                                  'Código'],
                 'correcta': 'C'},
                {'pregunta': 'La comunicación que utiliza el idioma para '
                             'codificar el mensaje es la comunicación:',
                 'alternativas': ['Lingüística',
                                  'Proxémica',
                                  'Kinésica',
                                  'Cromática',
                                  'No lingüística'],
                 'correcta': 'A'},
                {'pregunta': 'La comunicación oral se caracteriza por ser:',
                 'alternativas': ['Sin recursos no verbales',
                                  'Duradera y planificada',
                                  'Asincrónica',
                                  'Sincrónica y momentánea',
                                  'Siempre escrita'],
                 'correcta': 'D'},
                {'pregunta': 'La comunicación escrita se caracteriza por '
                             'ser:',
                 'alternativas': ['Sin cohesión',
                                  'Asincrónica y planificada',
                                  'Sincrónica',
                                  'Efímera',
                                  'Sin puntuación'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia los movimientos '
                             'corporales y gestos es la:',
                 'alternativas': ['Kinésica',
                                  'Háptica',
                                  'Proxémica',
                                  'Acústica',
                                  'Cronémica'],
                 'correcta': 'A'},
                {'pregunta': 'La disciplina que estudia las relaciones de '
                             'proximidad entre interlocutores es la:',
                 'alternativas': ['Cromática',
                                  'Oculésica',
                                  'Facial',
                                  'Kinésica',
                                  'Proxémica'],
                 'correcta': 'E'},
                {'pregunta': 'La disciplina que estudia el contacto ocular '
                             'durante la comunicación es la:',
                 'alternativas': ['Acústica',
                                  'Cronémica',
                                  'Oculésica',
                                  'Kinésica',
                                  'Háptica'],
                 'correcta': 'C'},
                {'pregunta': 'La disciplina que estudia el uso del tiempo en '
                             'la comunicación es la:',
                 'alternativas': ['Cronémica',
                                  'Proxémica',
                                  'Háptica',
                                  'Facial',
                                  'Cromática'],
                 'correcta': 'A'},
                {'pregunta': 'El monólogo interior y el soliloquio son '
                             'ejemplos de comunicación:',
                 'alternativas': ['Pública',
                                  'Masiva',
                                  'Interpersonal',
                                  'Grupal',
                                  'Intrapersonal'],
                 'correcta': 'E'},
                {'pregunta': 'La comunicación que se produce cuando '
                             'interactúan dos personas es la:',
                 'alternativas': ['Pública',
                                  'Social',
                                  'Intrapersonal',
                                  'Grupal',
                                  'Interpersonal'],
                 'correcta': 'E'},
                {'pregunta': 'La interacción entre ciudadanos y medios de '
                             'comunicación masivos es la comunicación:',
                 'alternativas': ['Interpersonal',
                                  'Privada',
                                  'Pública',
                                  'Intrapersonal',
                                  'Grupal'],
                 'correcta': 'C'},
                {'pregunta': 'La comunicación grupal se orienta al '
                             'cumplimiento de:',
                 'alternativas': ['Objetivos individuales',
                                  'Objetivos comunes del grupo',
                                  'Metas ajenas al grupo',
                                  'Ninguna finalidad',
                                  'Reglas externas impuestas'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el objetivo de la comunicación es '
                             'mantener las relaciones interpersonales con '
                             'otros individuos, se aprecia la función:',
                 'alternativas': ['Lingüística',
                                  'Social',
                                  'Organizativa',
                                  'Cultural',
                                  'Simbólica'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación que representa '
                             'hechos, objetos o sentimientos por medio de '
                             'símbolos, señales y signos se llama función:',
                 'alternativas': ['Social',
                                  'Simbólica',
                                  'Lingüística',
                                  'Organizativa',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación ligada al estilo '
                             'del lenguaje usado en el mensaje (formal, '
                             'informal, culto, popular) se llama función:',
                 'alternativas': ['Social',
                                  'Lingüística',
                                  'Simbólica',
                                  'Cultural',
                                  'Organizativa'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación que ordena a las '
                             'personas por puestos, estratos y jerarquías se '
                             'llama función:',
                 'alternativas': ['Cultural',
                                  'Organizativa',
                                  'Social',
                                  'Simbólica',
                                  'Lingüística'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación que transmite '
                             'hábitos, costumbres, valores y creencias se '
                             'llama función:',
                 'alternativas': ['Organizativa',
                                  'Cultural',
                                  'Social',
                                  'Simbólica',
                                  'Lingüística'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter de la comunicación que implica que '
                             'esta se integra con personas que tienen '
                             'posibilidad de relacionarse se llama carácter:',
                 'alternativas': ['Dinámico',
                                  'Integrador',
                                  'Recíproco',
                                  'Transaccional',
                                  'Fijo'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter de la comunicación dado por la '
                             'interacción de personas que logran entenderse '
                             'entre sí se llama carácter:',
                 'alternativas': ['Integrador',
                                  'Transaccional',
                                  'Dinámico',
                                  'Recíproco',
                                  'Estático'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter de la comunicación que implica que '
                             'esta fluye de forma continua y en cambio '
                             'constante se llama carácter:',
                 'alternativas': ['Recíproco',
                                  'Dinámico',
                                  'Integrador',
                                  'Transaccional',
                                  'Fijo'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter de la comunicación por el cual los '
                             'hombres ejercen una influencia mutua se llama '
                             'carácter:',
                 'alternativas': ['Dinámico',
                                  'Recíproco',
                                  'Integrador',
                                  'Transaccional',
                                  'Unilateral'],
                 'correcta': 'B'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido a la cantidad y calidad de '
                             'información que se tiene sobre el referente se '
                             'llama:',
                 'alternativas': ['Competencia lexicológica',
                                  'Nivel de conocimiento',
                                  'Actitudes',
                                  'Contexto sociocultural',
                                  'Redundancia'],
                 'correcta': 'B'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido al dominio del vocabulario del código '
                             'lingüístico se llama:',
                 'alternativas': ['Nivel de conocimiento',
                                  'Competencia lexicológica',
                                  'Actitudes',
                                  'Contexto sociocultural',
                                  'Ruido'],
                 'correcta': 'B'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido a los comportamientos, motivaciones y '
                             'reacciones del interlocutor se llama:',
                 'alternativas': ['Nivel de conocimiento',
                                  'Actitudes',
                                  'Competencia lexicológica',
                                  'Redundancia',
                                  'Contexto'],
                 'correcta': 'B'},
                {'pregunta': 'El factor de degradación que distorsiona la '
                             'calidad del mensaje o interfiere en la '
                             'comunicación se llama:',
                 'alternativas': ['Redundancia',
                                  'Ruido',
                                  'Competencia',
                                  'Contexto',
                                  'Actitud'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido que ocurre en el ambiente, como '
                             'interferencias en el canal (distorsiones '
                             'sonoras, baja señal), se llama ruido:',
                 'alternativas': ['Fisiológico',
                                  'Físico',
                                  'Psicológico',
                                  'Semántico',
                                  'Técnico'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido que surge por defectos orgánicos de '
                             'los interlocutores, como alteraciones visuales '
                             'o auditivas, se llama ruido:',
                 'alternativas': ['Físico',
                                  'Fisiológico',
                                  'Psicológico',
                                  'Semántico',
                                  'Técnico'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido que se produce en el interior del '
                             'individuo, como emociones, miedo o ansiedad, '
                             'se llama ruido:',
                 'alternativas': ['Físico',
                                  'Psicológico',
                                  'Fisiológico',
                                  'Semántico',
                                  'Técnico'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido que ocurre cuando el receptor '
                             'interpreta las palabras del emisor de manera '
                             'distinta a la intención original se llama '
                             'ruido:',
                 'alternativas': ['Físico',
                                  'Semántico',
                                  'Fisiológico',
                                  'Psicológico',
                                  'Técnico'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido intencionado en el que '
                             'deliberadamente se omite parte o todo el '
                             'mensaje se llama ruido:',
                 'alternativas': ['Semántico',
                                  'Técnico o blanco',
                                  'Físico',
                                  'Fisiológico',
                                  'Psicológico'],
                 'correcta': 'B'},
                {'pregunta': 'El factor de perfeccionamiento que reduce los '
                             'efectos del ruido y refuerza la claridad del '
                             'mensaje se llama:',
                 'alternativas': ['Competencia lexicológica',
                                  'Redundancia',
                                  'Nivel de conocimiento',
                                  'Contexto sociocultural',
                                  'Actitud'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'El Lenguaje',
  'secciones': [{'titulo': '2.1 CONCEPTO',
                 'items': ['Según la RAE, el lenguaje es la facultad del ser '
                           'humano de expresarse y comunicarse mediante el '
                           'sonido {articulado} u otros sistemas de signos.',
                           'Según Sapir, el lenguaje es un método '
                           'exclusivamente {humano} y no instintivo de '
                           'comunicar ideas, emociones y deseos.',
                           'Según Pinker, el lenguaje es una capacidad '
                           '{innata} del Homo sapiens, un mecanismo '
                           '{biológico} moldeado por la evolución.',
                           'Según {Noam Chomsky}, el lenguaje es una '
                           'facultad innata del ser humano regida por una '
                           '{gramática universal}.']},
                {'titulo': '2.2 CARACTERÍSTICAS DEL LENGUAJE',
                 'items': ['El lenguaje es {universal}, porque todos los '
                           'seres humanos lo utilizan en su interrelación.',
                           'El lenguaje es {multiforme}, porque se '
                           'manifiesta de muchas maneras: oral, escrita, '
                           'gestual, musical.',
                           'El lenguaje es {convencional}, porque no es '
                           'producto individual sino resultado de un acuerdo '
                           '{comunitario}.',
                           'El lenguaje es {sistémico}, porque funciona de '
                           'acuerdo a ciertas normas o reglas.',
                           'El lenguaje es {simbólico}, porque una palabra '
                           'representa algo concreto o abstracto.',
                           'El lenguaje es {aprendido}, porque constituye un '
                           'legado cultural adquirido en sociedad.',
                           'El lenguaje es {innato}, porque la capacidad de '
                           'aprender una lengua es connatural al ser '
                           'humano.']},
                {'titulo': '2.3 FUNCIONES DEL LENGUAJE',
                 'items': ['La función {expresiva} o emotiva está centrada '
                           'en el emisor y manifiesta emociones o '
                           'sentimientos.',
                           'La función {apelativa} o conativa está centrada '
                           'en el receptor; busca que el oyente actúe '
                           'mediante órdenes o ruegos.',
                           'La función {representativa} o referencial está '
                           'centrada en el contenido y se encuentra en '
                           'textos {informativos}.',
                           'La función {metalingüística} se usa cuando el '
                           'código sirve para referirse al código mismo.',
                           'La función {fática} se centra en el canal y '
                           'busca mantener el contacto entre los '
                           'interlocutores.',
                           'La función {poética} o estética está centrada en '
                           'el mensaje y se usa con fines artísticos en '
                           'obras literarias.']},
                {'titulo': '2.4 PLANOS DEL LENGUAJE: LENGUA Y HABLA',
                 'items': ['Según {Ferdinand de Saussure}, el lenguaje tiene '
                           'dos planos interdependientes: lengua y habla.',
                           'La {lengua} es de carácter social: un sistema de '
                           'signos lingüísticos convencionales que usa una '
                           'comunidad.',
                           'El {habla} es de carácter individual: el uso '
                           'personal de la lengua, realizado mediante los '
                           'órganos de fonación.']},
                {'titulo': '2.5 EL DIALECTO (VARIACIÓN DIATÓPICA)',
                 'items': ['El {dialecto} es la variación de una lengua que '
                           'se manifiesta según factores regionales, '
                           'geográficos o {territoriales}.',
                           'La variación dialectal {lexicológica} ocurre '
                           'cuando cambia el vocabulario de una región a '
                           'otra: «casaca» (Perú) y «{chamarra}» (México).',
                           'La variación dialectal {semántica} ocurre cuando '
                           'una misma palabra tiene significados distintos: '
                           '«mona» significa mujer bonita en Venezuela y '
                           'hembra del {mono} en Perú.',
                           'La variación dialectal {morfológica} se da en la '
                           'forma y estructura de las palabras: «ratico» '
                           '(Venezuela) frente a «{ratito}» (Perú).',
                           'La variación dialectal {sintáctica} se '
                           'manifiesta en la estructura de la oración.',
                           'La variación dialectal {fonética} se percibe en '
                           'la entonación y pronunciación: «{yama}» en la '
                           'costa peruana frente a «llama» en la sierra.']},
                {'titulo': '2.6 EL SOCIOLECTO (VARIACIÓN DIASTRÁTICA)',
                 'items': ['El {sociolecto} es la variación de una lengua a '
                           'nivel social, ubicada en el eje {vertical}.',
                           'El sociolecto se subdivide en tres niveles: '
                           '{acrolecto}, mesolecto y {basilecto}.']},
                {'titulo': '2.7 EL IDIOLECTO (VARIACIÓN DIAFÁSICA)',
                 'items': ['El {idiolecto} es la variación que sufre una '
                           'lengua a nivel {individual}: cada persona tiene '
                           'su forma peculiar de hablar.',
                           'El idiolecto se ubica en la intersección de los '
                           'ejes {horizontal} y vertical.']},
                {'titulo': '2.8 EL INTERLECTO',
                 'items': ['El {interlecto} es el sistema transitorio de '
                           'habla entre la lengua materna y la {segunda '
                           'lengua} de un aprendiz.',
                           'Según {Alberto Escobar}, el interlecto es un '
                           'dialecto social ubicado especialmente en áreas '
                           'rurales y {urbano-marginales}.',
                           'Un rasgo fonético del interlecto es la '
                           '{neutralización} de las vocales i-e, o-u, como '
                           'en «{oniversidad}» o «siñor».',
                           'Un rasgo gramatical del interlecto es la '
                           '{omisión} del artículo, como en «pásame '
                           '{libro}».',
                           'Un rasgo semántico del interlecto es la '
                           'tendencia a interpolar voces de la lengua '
                           '{vernácula} como préstamos.']},
                {'titulo': '2.9 EL SIGNO: TIPOS',
                 'items': ['El {signo} es la representación de algo que, por '
                           'naturaleza o convención, es representado; '
                           'facilita la {comunicación}.',
                           'Los {signos naturales} guardan relación física '
                           'de causa-efecto o proximidad con el objeto; '
                           'también se llaman {indicios}.',
                           'Ejemplos de indicio: la {fiebre} es síntoma de '
                           'infección; el humo es indicio de {fuego}; las '
                           'nubes negras, indicio de lluvia.',
                           'Los {signos artificiales} se dividen en ícono y '
                           '{símbolo}.',
                           'El {ícono} mantiene relación de {semejanza} con '
                           'el objeto representado, como fotografías, mapas '
                           'o dibujos.',
                           'El {símbolo} tiene carácter {convencional} y '
                           'arbitrario: la cruz simboliza el cristianismo; '
                           'la balanza, la justicia.']},
                {'titulo': '2.10 EL SIGNO LINGÜÍSTICO Y SUS PLANOS',
                 'items': ['El {signo lingüístico} es una entidad psíquica '
                           'de dos caras: concepto e imagen {acústica}, '
                           'asociadas de forma indisoluble.',
                           'El {significado} es el concepto o idea abstracta '
                           'que el hablante extrae de la {realidad}.',
                           'El {significante} es la imagen acústica o huella '
                           'psíquica del {sonido}.']},
                {'titulo': '2.11 CARACTERÍSTICAS DEL SIGNO LINGÜÍSTICO',
                 'items': ['El signo lingüístico es {arbitrario}: la '
                           'relación entre significado y significante es '
                           'convencional, no responde a ningún {motivo}.',
                           'El signo lingüístico es {lineal}: los fonemas se '
                           'desenvuelven uno tras otro en el {tiempo}.',
                           'El signo lingüístico es {inmutable}: no cambia '
                           'de un momento a otro por decisión de un '
                           '{hablante}, en el eje sincrónico.',
                           'El signo lingüístico es {mutable}: la relación '
                           'entre significado y significante cambia a través '
                           'del {tiempo}.',
                           'El signo lingüístico es {articulado}: las '
                           'unidades mayores son divisibles en partes más '
                           '{pequeñas}, reconocibles e intercambiables.']}],
  'cuadros': [{'titulo': '2.3 LAS SEIS FUNCIONES DEL LENGUAJE',
               'encabezados': ['Función', 'Centrada en'],
               'filas': [['{Expresiva}', 'El {emisor}'],
                         ['{Apelativa}', 'El {receptor}'],
                         ['{Referencial}', 'El {contenido}'],
                         ['{Metalingüística}', 'El {código}'],
                         ['{Fática}', 'El {canal}'],
                         ['{Poética}', 'El {mensaje}']]},
              {'titulo': 'NIVELES DEL SOCIOLECTO',
               'despues_de': '2.6 EL SOCIOLECTO (VARIACIÓN DIASTRÁTICA)',
               'encabezados': ['Nivel', 'Sector social', 'Ejemplo'],
               'filas': [['{Acrolecto}',
                          'Sectores altos, educados o cultos',
                          '«{dinero}»'],
                         ['{Mesolecto}', 'Sectores medios', '«{plata}»'],
                         ['{Basilecto}',
                          'Sectores sin acceso a educación formal',
                          '«{lana}»']]}],
  'preguntas': [{'pregunta': 'Según la RAE, el lenguaje es la facultad de '
                             'expresarse mediante el sonido articulado u '
                             'otros:',
                 'alternativas': ['Sistemas de signos',
                                  'Instintos',
                                  'Reflejos biológicos',
                                  'Ruidos naturales',
                                  'Impulsos'],
                 'correcta': 'A'},
                {'pregunta': 'Según Sapir, el lenguaje es un método '
                             'exclusivamente humano y:',
                 'alternativas': ['No instintivo',
                                  'Instintivo',
                                  'Genético únicamente',
                                  'Animal',
                                  'Universal en todas las especies'],
                 'correcta': 'A'},
                {'pregunta': 'Según Pinker, el lenguaje es una capacidad:',
                 'alternativas': ['Aprendida exclusivamente',
                                  'Innata del Homo sapiens',
                                  'Artificial',
                                  'Exclusiva de algunas culturas',
                                  'Adquirida solo en la escuela'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje sea usado por todos los seres '
                             'humanos corresponde a la característica de '
                             'ser:',
                 'alternativas': ['Universal',
                                  'Innato',
                                  'Sistémico',
                                  'Multiforme',
                                  'Simbólico'],
                 'correcta': 'A'},
                {'pregunta': 'Que el lenguaje se manifieste de forma oral, '
                             'escrita, gestual o musical corresponde a que '
                             'es:',
                 'alternativas': ['Multiforme',
                                  'Universal',
                                  'Aprendido',
                                  'Convencional',
                                  'Racional'],
                 'correcta': 'A'},
                {'pregunta': 'Que el lenguaje sea resultado de un acuerdo '
                             'comunitario corresponde a que es:',
                 'alternativas': ['Cultural exclusivo',
                                  'Convencional',
                                  'Innato',
                                  'Simbólico',
                                  'Sistémico'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje funcione de acuerdo a normas o '
                             'reglas corresponde a que es:',
                 'alternativas': ['Multiforme',
                                  'Sistémico',
                                  'Innato',
                                  'Simbólico',
                                  'Racional'],
                 'correcta': 'B'},
                {'pregunta': 'Que una palabra represente algo concreto o '
                             'abstracto corresponde a que el lenguaje es:',
                 'alternativas': ['Universal',
                                  'Aprendido',
                                  'Convencional',
                                  'Simbólico',
                                  'Sistémico'],
                 'correcta': 'D'},
                {'pregunta': 'La función del lenguaje centrada en el emisor, '
                             'que manifiesta emociones, es la función:',
                 'alternativas': ['Poética',
                                  'Fática',
                                  'Referencial',
                                  'Apelativa',
                                  'Expresiva'],
                 'correcta': 'E'},
                {'pregunta': 'La función centrada en el receptor, que busca '
                             'que actúe mediante órdenes, es la función:',
                 'alternativas': ['Poética',
                                  'Apelativa',
                                  'Metalingüística',
                                  'Expresiva',
                                  'Fática'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el contenido, propia de '
                             'textos informativos, es la función:',
                 'alternativas': ['Apelativa',
                                  'Referencial o representativa',
                                  'Expresiva',
                                  'Fática',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'La función que se usa cuando el código se '
                             'refiere al código mismo es la función:',
                 'alternativas': ['Expresiva',
                                  'Fática',
                                  'Poética',
                                  'Referencial',
                                  'Metalingüística'],
                 'correcta': 'E'},
                {'pregunta': 'La función centrada en el canal, que mantiene '
                             'el contacto entre interlocutores, es la '
                             'función:',
                 'alternativas': ['Expresiva',
                                  'Referencial',
                                  'Poética',
                                  'Apelativa',
                                  'Fática'],
                 'correcta': 'E'},
                {'pregunta': 'La función centrada en el mensaje, propia de '
                             'las obras literarias, es la función:',
                 'alternativas': ['Metalingüística',
                                  'Referencial',
                                  'Poética',
                                  'Apelativa',
                                  'Fática'],
                 'correcta': 'C'},
                {'pregunta': '«¡Cállate!» es un ejemplo de la función del '
                             'lenguaje:',
                 'alternativas': ['Fática',
                                  'Apelativa',
                                  'Expresiva',
                                  'Referencial',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': '«El precio del gas subió excesivamente» es un '
                             'ejemplo de la función:',
                 'alternativas': ['Fática',
                                  'Referencial',
                                  'Expresiva',
                                  'Apelativa',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'Según Saussure, el lenguaje tiene dos planos '
                             'interdependientes: lengua y:',
                 'alternativas': ['Texto',
                                  'Discurso',
                                  'Habla',
                                  'Sintaxis',
                                  'Gramática'],
                 'correcta': 'C'},
                {'pregunta': 'La lengua, según Saussure, es de carácter:',
                 'alternativas': ['Instintivo',
                                  'Privado',
                                  'Biológico',
                                  'Individual',
                                  'Social'],
                 'correcta': 'E'},
                {'pregunta': 'El habla, según Saussure, es de carácter:',
                 'alternativas': ['Universal',
                                  'Convencional exclusivo',
                                  'Colectivo',
                                  'Social',
                                  'Individual'],
                 'correcta': 'E'},
                {'pregunta': 'El habla se realiza físicamente por medio de:',
                 'alternativas': ['La memoria colectiva',
                                  'Los diccionarios',
                                  'Los signos escritos',
                                  'Los órganos de fonación',
                                  'Las normas gramaticales'],
                 'correcta': 'D'},
                {'pregunta': 'Según Noam Chomsky, el lenguaje es una '
                             'facultad innata del ser humano regida por una:',
                 'alternativas': ['Convención social',
                                  'Gramática universal',
                                  'Norma arbitraria',
                                  'Tradición cultural',
                                  'Selección natural'],
                 'correcta': 'B'},
                {'pregunta': 'El dialecto es la variación de una lengua que '
                             'se manifiesta según factores:',
                 'alternativas': ['Individuales',
                                  'Regionales, geográficos o territoriales',
                                  'Sociales exclusivamente',
                                  'Generacionales exclusivamente',
                                  'Educativos exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal en la que cambia el '
                             'vocabulario de una región a otra, como '
                             '«casaca» y «chamarra», se llama variación:',
                 'alternativas': ['Semántica',
                                  'Lexicológica',
                                  'Morfológica',
                                  'Sintáctica',
                                  'Fonética'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal en la que una misma '
                             'palabra tiene significados distintos, como '
                             '«mona», se llama variación:',
                 'alternativas': ['Lexicológica',
                                  'Semántica',
                                  'Morfológica',
                                  'Sintáctica',
                                  'Fonética'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal que se da en la forma y '
                             'estructura de las palabras, como «ratico» y '
                             '«ratito», se llama variación:',
                 'alternativas': ['Semántica',
                                  'Morfológica',
                                  'Sintáctica',
                                  'Fonética',
                                  'Lexicológica'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal que se percibe en la '
                             'entonación y pronunciación, como «yama» y '
                             '«llama», se llama variación:',
                 'alternativas': ['Morfológica',
                                  'Fonética',
                                  'Sintáctica',
                                  'Semántica',
                                  'Lexicológica'],
                 'correcta': 'B'},
                {'pregunta': 'El sociolecto es la variación de una lengua a '
                             'nivel:',
                 'alternativas': ['Individual',
                                  'Social',
                                  'Regional',
                                  'Temporal',
                                  'Generacional exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El sociolecto se subdivide en acrolecto, '
                             'basilecto y:',
                 'alternativas': ['Idiolecto',
                                  'Mesolecto',
                                  'Interlecto',
                                  'Dialecto',
                                  'Sociolema'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel sociolectal de los sectores altos, '
                             'educados o cultos se llama:',
                 'alternativas': ['Basilecto',
                                  'Acrolecto',
                                  'Mesolecto',
                                  'Interlecto',
                                  'Idiolecto'],
                 'correcta': 'B'},
                {'pregunta': 'El nivel sociolectal de los sectores sin '
                             'acceso a educación formal se llama:',
                 'alternativas': ['Acrolecto',
                                  'Basilecto',
                                  'Mesolecto',
                                  'Interlecto',
                                  'Idiolecto'],
                 'correcta': 'B'},
                {'pregunta': 'El idiolecto es la variación que sufre una '
                             'lengua a nivel:',
                 'alternativas': ['Social',
                                  'Individual',
                                  'Regional',
                                  'Generacional',
                                  'Temporal'],
                 'correcta': 'B'},
                {'pregunta': 'El interlecto es el sistema transitorio de '
                             'habla entre la lengua materna y:',
                 'alternativas': ['El dialecto regional',
                                  'La segunda lengua de un aprendiz',
                                  'El sociolecto',
                                  'El idiolecto personal',
                                  'La lengua estándar'],
                 'correcta': 'B'},
                {'pregunta': 'Según Alberto Escobar, el interlecto es un '
                             'dialecto social ubicado especialmente en '
                             'áreas:',
                 'alternativas': ['Urbanas exclusivamente',
                                  'Rurales y urbano-marginales',
                                  'Costeras exclusivamente',
                                  'Universitarias',
                                  'Empresariales'],
                 'correcta': 'B'},
                {'pregunta': 'Un signo que guarda relación física de '
                             'causa-efecto con el objeto que representa, '
                             'como el humo y el fuego, se llama:',
                 'alternativas': ['Símbolo',
                                  'Indicio',
                                  'Ícono',
                                  'Signo lingüístico',
                                  'Significante'],
                 'correcta': 'B'},
                {'pregunta': 'Un signo que mantiene relación de semejanza '
                             'con el objeto representado, como una '
                             'fotografía, se llama:',
                 'alternativas': ['Indicio',
                                  'Ícono',
                                  'Símbolo',
                                  'Signo natural exclusivo',
                                  'Significado'],
                 'correcta': 'B'},
                {'pregunta': 'Un signo de carácter convencional y '
                             'arbitrario, como la cruz que representa el '
                             'cristianismo, se llama:',
                 'alternativas': ['Indicio',
                                  'Símbolo',
                                  'Ícono',
                                  'Signo natural',
                                  'Significante'],
                 'correcta': 'B'},
                {'pregunta': 'El signo lingüístico es una entidad psíquica '
                             'de dos caras: concepto e imagen:',
                 'alternativas': ['Visual',
                                  'Acústica',
                                  'Táctil',
                                  'Olfativa',
                                  'Gustativa'],
                 'correcta': 'B'},
                {'pregunta': 'El concepto o idea abstracta que el hablante '
                             'extrae de la realidad se llama:',
                 'alternativas': ['Significante',
                                  'Significado',
                                  'Referente',
                                  'Símbolo',
                                  'Ícono'],
                 'correcta': 'B'},
                {'pregunta': 'La imagen acústica o huella psíquica del '
                             'sonido se llama:',
                 'alternativas': ['Significado',
                                  'Significante',
                                  'Referente',
                                  'Concepto',
                                  'Símbolo'],
                 'correcta': 'B'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual la relación entre significado y '
                             'significante es convencional se llama:',
                 'alternativas': ['Lineal',
                                  'Arbitraria',
                                  'Inmutable',
                                  'Mutable',
                                  'Articulada'],
                 'correcta': 'B'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual los fonemas se desenvuelven uno tras '
                             'otro en el tiempo se llama:',
                 'alternativas': ['Arbitraria',
                                  'Lineal',
                                  'Inmutable',
                                  'Mutable',
                                  'Articulada'],
                 'correcta': 'B'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual este no cambia por decisión de un '
                             'hablante en un momento dado se llama:',
                 'alternativas': ['Mutable',
                                  'Inmutable',
                                  'Lineal',
                                  'Arbitraria',
                                  'Articulada'],
                 'correcta': 'B'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual la relación significado-significante '
                             'cambia a través del tiempo se llama:',
                 'alternativas': ['Inmutable',
                                  'Mutable',
                                  'Lineal',
                                  'Arbitraria',
                                  'Articulada'],
                 'correcta': 'B'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual las unidades mayores son divisibles en '
                             'partes más pequeñas se llama:',
                 'alternativas': ['Lineal',
                                  'Articulada',
                                  'Inmutable',
                                  'Mutable',
                                  'Arbitraria'],
                 'correcta': 'B'}]},
 {'num': 3,
  'titulo': 'Fonología y Fonética',
  'secciones': [{'titulo': '3.1 CONCEPTO DE FONOLOGÍA Y FONÉTICA',
                 'items': ['La {fonología} estudia cómo se estructuran los '
                           'segmentos de la lengua para transmitir '
                           'significados, es decir, los sonidos en su '
                           'carácter {distintivo}.',
                           'La {fonética} estudia los mecanismos de '
                           'producción, transmisión y percepción de la señal '
                           'sonora del habla.',
                           'En español existen {24} fonemas, representados '
                           'en la escritura por 27 letras y 5 {dígrafos}.']},
                {'titulo': '3.2 FONEMAS Y FONOS',
                 'items': ['Los {fonemas} son sonidos ideales, mentales, '
                           'limitados o finitos, y se representan entre '
                           '{barras} / /.',
                           'Los {fonos} son la materialización o realización '
                           'de un fonema a través del habla, y se '
                           'representan entre {corchetes} [ ].',
                           'Los fonemas son unidades de estudio de la '
                           '{Fonología}; los fonos son unidades de estudio '
                           'de la {Fonética}.',
                           'Un {par mínimo}, como /beso/ y /peso/, permite '
                           'identificar fonemas distintos por el cambio de '
                           'significado.']},
                {'titulo': '3.3 EL FONEMA Y LOS RASGOS DISTINTIVOS',
                 'items': ['El {fonema} es el segmento fonológico que no '
                           'puede descomponerse en unidades menores y que '
                           'distingue significados.',
                           'Los {rasgos distintivos} son los elementos '
                           'constitutivos de un fonema cuya modificación '
                           'produce un contraste significativo.',
                           'El fonema /p/ tiene los rasgos distintivos '
                           'bilabial, oclusivo, {sordo} y oral.',
                           'El fonema /b/ tiene los rasgos distintivos '
                           'bilabial, oclusivo, {sonoro} y oral.',
                           '«Peso» y «beso» se diferencian por un único '
                           'rasgo distintivo: el valor de la {sonoridad}.']},
                {'titulo': '3.4 FONEMAS VOCÁLICOS Y SU CLASIFICACIÓN',
                 'items': ['El español tiene {24} fonemas segmentales: 5 son '
                           '{vocálicos} y 19 consonánticos.',
                           'En los {fonemas vocálicos}, el flujo de aire no '
                           'encuentra ningún {obstáculo} para atravesar el '
                           'canal fonatorio: /a/, /e/, /i/, /o/, /u/.',
                           'Por el grado de abertura de la boca: vocales '
                           '{cerradas} (/i/, /u/), semiabiertas (/e/, /o/), '
                           'y vocal {abierta} (/a/).',
                           'Por la posición de la lengua: vocales '
                           '{anteriores} o palatales (/e/, /i/), vocal '
                           '{central} (/a/), y vocales posteriores o velares '
                           '(/o/, /u/).',
                           'Por el grado de sonoridad: vocales {agudas} '
                           '(/e/, /i/), vocal media (/a/), y vocales '
                           '{graves} (/o/, /u/).',
                           'Por la vibración de las cuerdas vocales, todas '
                           'las vocales del español son {sonoras}; no '
                           'existen vocales {sordas}.',
                           'El {triángulo vocálico} fue propuesto por {F. '
                           'Hellwag} en 1781.']},
                {'titulo': '3.5 FONEMAS CONSONÁNTICOS: PUNTO DE ARTICULACIÓN',
                 'items': ['En los {fonemas consonánticos} se produce una '
                           'interrupción total o parcial del flujo de aire, '
                           'combinando movimientos de {lengua}, labios y '
                           'dientes.',
                           'Por el {punto de articulación}: son {bilabiales} '
                           'los fonemas /p/, /b/, /m/, donde intervienen '
                           'ambos labios.',
                           'Es {labiodental} el fonema /f/, donde el labio '
                           'inferior se dirige hacia los dientes {incisivos} '
                           'superiores.',
                           'Son {dentales} los fonemas /t/, /d/, donde el '
                           'ápice de la lengua toca los {dientes} incisivos '
                           'superiores.',
                           'Es {interdental} el fonema /z/, donde el ápice '
                           'de la lengua se ubica entre los {dientes}.',
                           'Son {alveolares} los fonemas /s/, /n/, /l/, /r/, '
                           '/rr/, donde el ápice de la lengua se dirige '
                           'hacia los {alvéolos}.',
                           'Son {palatales} los fonemas /ch/, /y/, /ll/, '
                           '/ñ/, donde el dorso de la lengua se dirige hacia '
                           'el {paladar} medio.',
                           'Son {velares} los fonemas /k/, /g/, /j/, donde '
                           'la raíz de la lengua se dirige hacia el {velo} '
                           'del paladar.']},
                {'titulo': '3.6 FONEMAS CONSONÁNTICOS: MODO DE ARTICULACIÓN',
                 'items': ['Por el {modo de articulación}: son {oclusivos} '
                           'los fonemas /p/, /b/, /d/, /k/, /g/, /t/, donde '
                           'el aire encuentra un cierre momentáneo con breve '
                           '{explosión}.',
                           'Son {fricativos} los fonemas /f/, /z/, /s/, /y/, '
                           '/j/, donde el aire pasa friccionando o {rozando} '
                           'las paredes del canal.',
                           'Es {africado} el fonema /ch/, que resulta de la '
                           'combinación de la oclusiva con la {fricativa}.',
                           'Son {laterales} los fonemas /l/, /ll/, donde el '
                           'aire sale por los {lados} de la lengua.',
                           'Son {nasales} los fonemas /m/, /n/, /ñ/, donde '
                           'el aire sale por la cavidad {nasal} y la cavidad '
                           'oral.',
                           'Son {vibrantes} los fonemas /rr/, /r/, donde el '
                           'órgano activo vibra {obstruyendo} y abriendo el '
                           'paso del aire.',
                           'Por el grado de vibración de las cuerdas '
                           'vocales, los fonemas consonánticos se clasifican '
                           'en {sonoros} y sordos.']},
                {'titulo': '3.7 ELEMENTOS SEGMENTALES Y SUPRASEGMENTALES',
                 'items': ['Los elementos {segmentales} constituyen la '
                           'cadena hablada, definidos según criterios '
                           'articulatorios, acústicos y perceptivos.',
                           'Los elementos {suprasegmentales}, como la '
                           'entonación y el acento, se superponen a la '
                           'cadena de sonidos.']},
                {'titulo': '3.8 RAMAS DE LA FONÉTICA',
                 'items': ['La {fonética articulatoria} estudia cómo se '
                           'producen los sonidos mediante los órganos del '
                           '{habla}.',
                           'La {fonética acústica} estudia las propiedades '
                           'físicas de las ondas sonoras del {habla}.',
                           'La {fonética descriptiva} o auditiva estudia '
                           'cómo el oído {percibe} los sonidos del habla.']}],
  'cuadros': [{'titulo': '3.2 FONEMAS FRENTE A FONOS',
               'encabezados': ['Aspecto', 'Fonema', 'Fono'],
               'filas': [['Naturaleza',
                          '{Ideal}, mental',
                          '{Real}, materializado'],
                         ['Cantidad',
                          '{Limitados} o finitos',
                          '{Ilimitados} o infinitos'],
                         ['Representación',
                          'Entre {barras} / /',
                          'Entre {corchetes} [ ]'],
                         ['Disciplina', '{Fonología}', '{Fonética}']]}],
  'preguntas': [{'pregunta': 'La disciplina que estudia los sonidos de la '
                             'lengua en su carácter distintivo de '
                             'significados es la:',
                 'alternativas': ['Semántica',
                                  'Fonología',
                                  'Sintaxis',
                                  'Morfología',
                                  'Fonética'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia los mecanismos de '
                             'producción física de los sonidos del habla es '
                             'la:',
                 'alternativas': ['Pragmática',
                                  'Fonología',
                                  'Semántica',
                                  'Morfología',
                                  'Fonética'],
                 'correcta': 'E'},
                {'pregunta': 'El número de fonemas del español es:',
                 'alternativas': ['27', '20', '30', '24', '22'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonemas se representan entre:',
                 'alternativas': ['Corchetes [ ]',
                                  'Barras / /',
                                  'Llaves { }',
                                  'Comillas « »',
                                  'Paréntesis ( )'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonos se representan entre:',
                 'alternativas': ['Corchetes [ ]',
                                  'Barras / /',
                                  'Paréntesis ( )',
                                  'Comillas « »',
                                  'Llaves { }'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonemas son unidades de estudio de la:',
                 'alternativas': ['Semántica',
                                  'Morfología',
                                  'Sintaxis',
                                  'Fonología',
                                  'Fonética'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonos son unidades de estudio de la:',
                 'alternativas': ['Semántica',
                                  'Fonética',
                                  'Fonología',
                                  'Pragmática',
                                  'Morfología'],
                 'correcta': 'B'},
                {'pregunta': 'Un fonema se define como un segmento '
                             'fonológico que:',
                 'alternativas': ['Es siempre visible por escrito',
                                  'Se puede descomponer en unidades menores',
                                  'No existe en la lengua oral',
                                  'Carece de valor distintivo',
                                  'No puede descomponerse en unidades '
                                  'sucesivas menores'],
                 'correcta': 'E'},
                {'pregunta': 'Los fonemas son sonidos:',
                 'alternativas': ['Sin valor distintivo',
                                  'Reales y materializados',
                                  'Ideales y mentales',
                                  'Infinitos',
                                  'Exclusivamente escritos'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonos son la materialización de un fonema '
                             'a través:',
                 'alternativas': ['De la gramática',
                                  'De la lectura silenciosa',
                                  'Del habla',
                                  'De la memoria',
                                  'De la escritura'],
                 'correcta': 'C'},
                {'pregunta': 'Un par mínimo, como «beso» y «peso», sirve '
                             'para identificar:',
                 'alternativas': ['Palabras sin relación',
                                  'Homófonos idénticos',
                                  'Sinónimos',
                                  'Fonemas distintos por el cambio de '
                                  'significado',
                                  'Antónimos'],
                 'correcta': 'D'},
                {'pregunta': 'Los elementos constitutivos de un fonema, cuya '
                             'modificación causa contraste significativo, '
                             'son los:',
                 'alternativas': ['Grafemas',
                                  'Fonos',
                                  'Dígrafos',
                                  'Rasgos distintivos',
                                  'Morfemas'],
                 'correcta': 'D'},
                {'pregunta': 'El fonema /p/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sordo',
                                  'Vibrante',
                                  'Nasal',
                                  'Fricativo',
                                  'Sonoro'],
                 'correcta': 'A'},
                {'pregunta': 'El fonema /b/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sonoro',
                                  'Sordo',
                                  'Nasal',
                                  'Lateral',
                                  'Vibrante'],
                 'correcta': 'A'},
                {'pregunta': '«Peso» y «beso» se diferencian por el rasgo '
                             'distintivo de:',
                 'alternativas': ['El punto de articulación',
                                  'El modo nasal',
                                  'La sonoridad',
                                  'La sílaba tónica',
                                  'La vocal final'],
                 'correcta': 'C'},
                {'pregunta': 'Los elementos que constituyen la cadena '
                             'hablada y se estudian con criterios '
                             'articulatorios son los elementos:',
                 'alternativas': ['Semánticos',
                                  'Segmentales',
                                  'Morfológicos',
                                  'Sintácticos',
                                  'Suprasegmentales'],
                 'correcta': 'B'},
                {'pregunta': 'La entonación y el acento son ejemplos de '
                             'elementos:',
                 'alternativas': ['Léxicos',
                                  'Segmentales',
                                  'Suprasegmentales',
                                  'Sintácticos',
                                  'Morfológicos'],
                 'correcta': 'C'},
                {'pregunta': 'El número de dígrafos en la escritura del '
                             'español es:',
                 'alternativas': ['5', '2', '3', '7', '10'],
                 'correcta': 'A'},
                {'pregunta': 'En español, /b/ y /l/ son fonemas distintos '
                             'porque existen pares de palabras como:',
                 'alternativas': ['Ola y hola',
                                  'Vaca y baca',
                                  'Casa y caza',
                                  'Tubo y tuvo',
                                  'Bata y lata'],
                 'correcta': 'E'},
                {'pregunta': 'Los fonemas carecen de significación:',
                 'alternativas': ['Solo en la escritura',
                                  'Siempre en combinación',
                                  'Por sí solos',
                                  'Solo en el habla informal',
                                  'En cualquier contexto'],
                 'correcta': 'C'},
                {'pregunta': 'La rama de la fonética que estudia cómo se '
                             'producen los sonidos mediante los órganos del '
                             'habla es la fonética:',
                 'alternativas': ['Acústica',
                                  'Articulatoria',
                                  'Descriptiva',
                                  'Auditiva exclusiva',
                                  'Fonológica'],
                 'correcta': 'B'},
                {'pregunta': 'La rama de la fonética que estudia las '
                             'propiedades físicas de las ondas sonoras es la '
                             'fonética:',
                 'alternativas': ['Articulatoria',
                                  'Acústica',
                                  'Descriptiva',
                                  'Perceptiva exclusiva',
                                  'Fonológica'],
                 'correcta': 'B'},
                {'pregunta': 'El español tiene 24 fonemas segmentales, de '
                             'los cuales el número de fonemas vocálicos es:',
                 'alternativas': ['3', '5', '7', '19', '10'],
                 'correcta': 'B'},
                {'pregunta': 'En los fonemas vocálicos, durante su '
                             'producción, el flujo de aire:',
                 'alternativas': ['Encuentra un obstáculo total',
                                  'No encuentra ningún obstáculo',
                                  'Se interrumpe parcialmente',
                                  'Vibra en las cuerdas vocales',
                                  'Se detiene completamente'],
                 'correcta': 'B'},
                {'pregunta': 'Por el grado de abertura de la boca, las '
                             'vocales /i/ y /u/ se clasifican como:',
                 'alternativas': ['Abiertas',
                                  'Cerradas',
                                  'Semiabiertas',
                                  'Centrales',
                                  'Posteriores'],
                 'correcta': 'B'},
                {'pregunta': 'Por la posición de la lengua, la vocal /a/ se '
                             'clasifica como vocal:',
                 'alternativas': ['Anterior o palatal',
                                  'Central',
                                  'Posterior o velar',
                                  'Cerrada',
                                  'Aguda'],
                 'correcta': 'B'},
                {'pregunta': 'Por el grado de sonoridad, las vocales /o/ y '
                             '/u/ se clasifican como vocales:',
                 'alternativas': ['Agudas',
                                  'Graves',
                                  'Medias',
                                  'Cerradas',
                                  'Abiertas'],
                 'correcta': 'B'},
                {'pregunta': 'Respecto a la vibración de las cuerdas '
                             'vocales, en español:',
                 'alternativas': ['Existen vocales sordas y sonoras por '
                                  'igual',
                                  'Todas las vocales son sonoras',
                                  'Todas las vocales son sordas',
                                  'Solo /a/ es sonora',
                                  'Ninguna vocal es sonora'],
                 'correcta': 'B'},
                {'pregunta': 'El triángulo vocálico, herramienta para '
                             'clasificar las vocales, fue propuesto en 1781 '
                             'por:',
                 'alternativas': ['Ferdinand de Saussure',
                                  'F. Hellwag',
                                  'Noam Chomsky',
                                  'Roman Jakobson',
                                  'André Martinet'],
                 'correcta': 'B'},
                {'pregunta': 'En los fonemas consonánticos, durante su '
                             'realización, se produce:',
                 'alternativas': ['Ninguna interrupción del flujo de aire',
                                  'Una interrupción total o parcial del '
                                  'flujo de aire',
                                  'Solo vibración de cuerdas vocales',
                                  'Solo resonancia nasal',
                                  'Solo fricción labial'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /p/, /b/ y /m/, donde intervienen '
                             'ambos labios, se clasifican por su punto de '
                             'articulación como:',
                 'alternativas': ['Labiodentales',
                                  'Bilabiales',
                                  'Dentales',
                                  'Alveolares',
                                  'Palatales'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /f/, donde el labio inferior se '
                             'dirige hacia los dientes incisivos superiores, '
                             'se clasifica como:',
                 'alternativas': ['Bilabial',
                                  'Labiodental',
                                  'Dental',
                                  'Interdental',
                                  'Alveolar'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /s/, /n/, /l/, /r/, /rr/, donde el '
                             'ápice de la lengua se dirige hacia los '
                             'alvéolos, se clasifican como:',
                 'alternativas': ['Dentales',
                                  'Alveolares',
                                  'Palatales',
                                  'Velares',
                                  'Interdentales'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /ch/, /y/, /ll/, /ñ/, donde el '
                             'dorso de la lengua se dirige hacia el paladar '
                             'medio, se clasifican como:',
                 'alternativas': ['Alveolares',
                                  'Palatales',
                                  'Velares',
                                  'Dentales',
                                  'Bilabiales'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /k/, /g/, /j/, donde la raíz de la '
                             'lengua se dirige hacia el velo del paladar, se '
                             'clasifican como:',
                 'alternativas': ['Palatales',
                                  'Velares',
                                  'Alveolares',
                                  'Dentales',
                                  'Labiodentales'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /p/, /b/, /d/, /k/, /g/, /t/, '
                             'donde el aire encuentra un cierre momentáneo '
                             'con breve explosión, se clasifican por su modo '
                             'de articulación como:',
                 'alternativas': ['Fricativos',
                                  'Oclusivos',
                                  'Africados',
                                  'Laterales',
                                  'Nasales'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /f/, /z/, /s/, /y/, /j/, donde el '
                             'aire pasa friccionando las paredes del canal, '
                             'se clasifican como:',
                 'alternativas': ['Oclusivos',
                                  'Fricativos',
                                  'Africados',
                                  'Vibrantes',
                                  'Nasales'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /ch/, que resulta de la combinación '
                             'de una oclusiva con una fricativa, se '
                             'clasifica como:',
                 'alternativas': ['Oclusivo',
                                  'Africado',
                                  'Fricativo',
                                  'Lateral',
                                  'Nasal'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /m/, /n/, /ñ/, donde el aire sale '
                             'por la cavidad nasal y la cavidad oral, se '
                             'clasifican como:',
                 'alternativas': ['Laterales',
                                  'Nasales',
                                  'Vibrantes',
                                  'Oclusivos',
                                  'Fricativos'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas /rr/ y /r/, donde el órgano activo '
                             'vibra obstruyendo y abriendo el paso del aire, '
                             'se clasifican como:',
                 'alternativas': ['Nasales',
                                  'Vibrantes',
                                  'Laterales',
                                  'Fricativos',
                                  'Oclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /g/, clasificado por punto de '
                             'articulación, modo de articulación y '
                             'sonoridad, corresponde a:',
                 'alternativas': ['Velar - fricativo - sordo',
                                  'Velar - oclusivo - sonoro',
                                  'Bilabial - oclusivo - sonoro',
                                  'Alveolar - vibrante - sonoro',
                                  'Palatal - africado - sordo'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /j/, clasificado por punto de '
                             'articulación, modo de articulación y '
                             'sonoridad, corresponde a:',
                 'alternativas': ['Velar - oclusivo - sonoro',
                                  'Velar - fricativo - sordo',
                                  'Bilabial - nasal - sonoro',
                                  'Alveolar - lateral - sonoro',
                                  'Palatal - africado - sordo'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'La Sílaba',
  'secciones': [{'titulo': '4.1 CONCEPTO',
                 'items': ['La sílaba es la unidad estructural que actúa '
                           'como principio {organizador} de la lengua.',
                           'La sílaba se agrupa en torno al segmento de '
                           'máxima {sonoridad}, que constituye su núcleo.',
                           'En español, el núcleo silábico es siempre '
                           '{vocálico}.',
                           'En la palabra «pan», la vocal /a/ constituye el '
                           'pico de sonoridad, y las consonantes /p/ y /n/ '
                           'son los {márgenes} consonánticos.']},
                {'titulo': '4.2 CONSTITUYENTES SILÁBICOS',
                 'items': ['El {núcleo} es la cumbre o centro de la sílaba, '
                           'constituido por una sola vocal.',
                           'El {inicio} o ataque es el margen silábico '
                           'anterior, de naturaleza consonántica, en '
                           'posición explosiva.',
                           'La {coda} es el margen silábico posterior, de '
                           'naturaleza consonántica, en posición implosiva.',
                           'La {rima} silábica está constituida por el '
                           'núcleo y la coda, o solo por el núcleo.']},
                {'titulo': '4.3 EL SILABEO O DIVISIÓN SILÁBICA',
                 'items': ['El {silabeo} consiste en pronunciar o escribir '
                           'en forma separada las sílabas de una palabra.',
                           'Una consonante entre dos vocales siempre forma '
                           'sílaba con la vocal que la {sigue}: pa-to.',
                           'Los grupos tautosilábicos como pr, br, tr, cr, '
                           'pl, bl, cl son {inseparables} y forman sílaba '
                           'con la vocal siguiente.',
                           'Cuando una sílaba termina en consonante y la '
                           'siguiente comienza en otra consonante, se '
                           '{separan} entre ambas: as-ma.',
                           'No existe en español frontera silábica en la '
                           'secuencia {consonante-vocal}.']},
                {'titulo': '4.4 GRUPOS TAUTOSILÁBICOS Y DIPTONGOS',
                 'items': ['Los {grupos tautosilábicos} ocurren cuando dos '
                           'elementos contiguos pertenecen a la misma '
                           '{sílaba}: combinaciones pl, pr, cl, cr, fl, fr, '
                           'bl, br, gl, gr, tl, tr.',
                           'El {diptongo} es la concurrencia de dos vocales '
                           'que forman una sola {sílaba}.',
                           'El diptongo {creciente} combina una vocal '
                           'cerrada y una abierta, o dos vocales cerradas '
                           'diferentes; ejemplo: {pue}s.',
                           'El diptongo {decreciente} combina una vocal '
                           'abierta y una cerrada; ejemplo: {ai}re.']},
                {'titulo': '4.5 EL TRIPTONGO',
                 'items': ['El {triptongo} está constituido por dos vocales '
                           'cerradas (débiles) y una abierta (fuerte) en '
                           'medio, según el esquema VC + {VA} + VC.',
                           'Las vocales del triptongo se pronuncian como una '
                           'sola sílaba y no pueden {separarse}; ejemplo: '
                           '{cam-biáis}.']},
                {'titulo': '4.6 EL HIATO (GRUPOS HETEROSILÁBICOS)',
                 'items': ['En los {grupos heterosilábicos}, dos segmentos '
                           'consecutivos se integran en sílabas '
                           '{diferentes}: es el caso del hiato.',
                           'El {hiato} son dos vocales seguidas que se '
                           'separan para formar dos {sílabas}.',
                           'Cuando hay dos vocales {fuertes} (abiertas) '
                           'juntas, siempre se produce hiato; ejemplo: '
                           'pe-{ón}.',
                           'Cuando hay una vocal {débil} (cerrada) tónica '
                           'junto a una fuerte, se deshace el diptongo y se '
                           'forma un hiato; ejemplo: {dí}-a.']},
                {'titulo': '4.7 PRINCIPIOS DE ORDENACIÓN DE LOS SEGMENTOS',
                 'items': ['Los sonidos dentro de la sílaba se organizan '
                           'según la {escala universal de sonoridad}, donde '
                           'las {vocales} son las unidades más '
                           'perceptibles.']}],
  'cuadros': [{'titulo': '4.2 CONSTITUYENTES DE LA SÍLABA',
               'encabezados': ['Constituyente', 'Posición', 'Naturaleza'],
               'filas': [['{Núcleo}', 'Centro', '{Vocálica}'],
                         ['{Inicio}', 'Margen anterior', '{Consonántica}'],
                         ['{Coda}', 'Margen posterior', 'Consonántica']]}],
  'preguntas': [{'pregunta': 'La sílaba se define como la unidad estructural '
                             'que actúa como principio:',
                 'alternativas': ['Organizador de la lengua',
                                  'Sintáctico',
                                  'Morfológico exclusivo',
                                  'Semántico',
                                  'Pragmático'],
                 'correcta': 'A'},
                {'pregunta': 'La sílaba se agrupa en torno al segmento de '
                             'máxima:',
                 'alternativas': ['Consonancia',
                                  'Intensidad tonal',
                                  'Sonoridad',
                                  'Frecuencia',
                                  'Duración'],
                 'correcta': 'C'},
                {'pregunta': 'En español, el núcleo silábico es siempre de '
                             'naturaleza:',
                 'alternativas': ['Fricativa',
                                  'Consonántica',
                                  'Mixta obligatoria',
                                  'Nasal',
                                  'Vocálica'],
                 'correcta': 'E'},
                {'pregunta': 'El constituyente silábico que es la cumbre o '
                             'centro de la sílaba es:',
                 'alternativas': ['El núcleo',
                                  'El inicio',
                                  'La coda',
                                  'El ataque',
                                  'La rima'],
                 'correcta': 'A'},
                {'pregunta': 'El margen silábico anterior, de naturaleza '
                             'consonántica, se llama:',
                 'alternativas': ['Rima',
                                  'Núcleo',
                                  'Inicio o ataque',
                                  'Coda',
                                  'Centro'],
                 'correcta': 'C'},
                {'pregunta': 'El margen silábico posterior, en posición '
                             'implosiva, se llama:',
                 'alternativas': ['Ataque',
                                  'Coda',
                                  'Inicio',
                                  'Núcleo',
                                  'Centro'],
                 'correcta': 'B'},
                {'pregunta': 'La rima silábica está constituida por:',
                 'alternativas': ['Solo el inicio',
                                  'Ningún elemento fijo',
                                  'Solo la coda',
                                  'El núcleo y la coda',
                                  'El inicio y la coda'],
                 'correcta': 'D'},
                {'pregunta': 'El silabeo consiste en:',
                 'alternativas': ['Unir todas las sílabas',
                                  'Contar las consonantes',
                                  'Pronunciar o escribir separadas las '
                                  'sílabas de una palabra',
                                  'Acentuar todas las palabras',
                                  'Eliminar las vocales'],
                 'correcta': 'C'},
                {'pregunta': 'Una consonante entre dos vocales siempre forma '
                             'sílaba con la vocal que:',
                 'alternativas': ['La sigue',
                                  'Es átona',
                                  'La precede',
                                  'Es tónica',
                                  'Está más lejos'],
                 'correcta': 'A'},
                {'pregunta': 'En la palabra «pato», la separación silábica '
                             'correcta es:',
                 'alternativas': ['P-ato',
                                  'Pa-to',
                                  'Pato completo',
                                  'Pa-t-o',
                                  'Pat-o'],
                 'correcta': 'B'},
                {'pregunta': 'Los grupos tautosilábicos pr, br, tr, cr, pl, '
                             'bl, cl se caracterizan por ser:',
                 'alternativas': ['Nulos en español',
                                  'Solo finales de palabra',
                                  'Vocálicos',
                                  'Inseparables',
                                  'Separables siempre'],
                 'correcta': 'D'},
                {'pregunta': 'En la palabra «apretar», el grupo «pr» se '
                             'mantiene:',
                 'alternativas': ['Eliminado',
                                  'Acentuado siempre',
                                  'Junto, formando sílaba con la vocal '
                                  'siguiente',
                                  'Separado en dos sílabas',
                                  'Sustituido por otra letra'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando una sílaba termina en consonante y la '
                             'siguiente comienza en otra consonante, ambas '
                             'se:',
                 'alternativas': ['Eliminan',
                                  'Convierten en vocales',
                                  'Ignoran en el silabeo',
                                  'Unen en una sola sílaba',
                                  'Separan entre ambas consonantes'],
                 'correcta': 'E'},
                {'pregunta': 'En la palabra «asma», la separación silábica '
                             'es:',
                 'alternativas': ['As-ma',
                                  'A-s-ma',
                                  'A-sma',
                                  'Asma sin dividir',
                                  'Asm-a'],
                 'correcta': 'A'},
                {'pregunta': 'En español NO existe frontera silábica en la '
                             'secuencia:',
                 'alternativas': ['Consonante-vocal',
                                  'Diptongo-consonante',
                                  'Consonante-consonante',
                                  'Vocal-consonante',
                                  'Vocal-vocal'],
                 'correcta': 'A'},
                {'pregunta': 'En la palabra «Cuba», la separación silábica '
                             'correcta es:',
                 'alternativas': ['Cub-a',
                                  'Cu-ba',
                                  'C-uba',
                                  'Cu-b-a',
                                  'Cuba sin dividir'],
                 'correcta': 'B'},
                {'pregunta': 'Un vocablo monosilábico, como «pan», tiene:',
                 'alternativas': ['Dos sílabas',
                                  'Una sola sílaba',
                                  'Cuatro sílabas o más',
                                  'Tres sílabas',
                                  'Ninguna sílaba'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «amor» se divide silábicamente '
                             'como:',
                 'alternativas': ['Amo-r',
                                  'Amor sin dividir',
                                  'Am-or',
                                  'A-m-or',
                                  'A-mor'],
                 'correcta': 'E'},
                {'pregunta': 'El núcleo silábico, según el texto, resulta '
                             'determinante para asignar:',
                 'alternativas': ['La categoría sintáctica',
                                  'El género gramatical',
                                  'El número gramatical',
                                  'El acento léxico',
                                  'El sujeto de la oración'],
                 'correcta': 'D'},
                {'pregunta': 'Un sonido o grupo de sonidos pronunciados en '
                             'un solo golpe de voz constituye:',
                 'alternativas': ['Un fonema aislado',
                                  'Una sílaba',
                                  'Un morfema',
                                  'Un sintagma',
                                  'Una oración'],
                 'correcta': 'B'},
                {'pregunta': 'Las vocales solas, por sí mismas, pueden '
                             'constituir:',
                 'alternativas': ['Ningún elemento fónico',
                                  'Solo diptongos',
                                  'Sílabas',
                                  'Solo consonantes',
                                  'Solo palabras compuestas'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando dos elementos contiguos, como una '
                             'consonante y una líquida (pl, tr, cl), '
                             'pertenecen a la misma sílaba, se llaman '
                             'grupos:',
                 'alternativas': ['Heterosilábicos',
                                  'Tautosilábicos',
                                  'Vocálicos',
                                  'Consonánticos exclusivos',
                                  'Silábicos simples'],
                 'correcta': 'B'},
                {'pregunta': 'La concurrencia de dos vocales que forman una '
                             'sola sílaba se llama:',
                 'alternativas': ['Hiato',
                                  'Diptongo',
                                  'Triptongo',
                                  'Sinéresis exclusiva',
                                  'Sinalefa exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El diptongo que combina una vocal cerrada y '
                             'una abierta (en ese orden), como en «pues», se '
                             'llama diptongo:',
                 'alternativas': ['Decreciente',
                                  'Creciente',
                                  'Neutro',
                                  'Homogéneo',
                                  'Simple'],
                 'correcta': 'B'},
                {'pregunta': 'El diptongo que combina una vocal abierta y '
                             'una cerrada (en ese orden), como en «aire», se '
                             'llama diptongo:',
                 'alternativas': ['Creciente',
                                  'Decreciente',
                                  'Neutro',
                                  'Homogéneo',
                                  'Compuesto'],
                 'correcta': 'B'},
                {'pregunta': 'El triptongo está constituido, según el '
                             'esquema VC+VA+VC, por dos vocales cerradas y '
                             'una vocal:',
                 'alternativas': ['Cerrada adicional',
                                  'Abierta',
                                  'Neutra',
                                  'Nasal',
                                  'Tónica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Las vocales de un triptongo se pronuncian como '
                             'una sola sílaba y, bajo ninguna circunstancia, '
                             'pueden:',
                 'alternativas': ['Llevar tilde',
                                  'Separarse',
                                  'Repetirse',
                                  'Combinarse con consonantes',
                                  'Iniciar palabra'],
                 'correcta': 'B'},
                {'pregunta': 'Dos segmentos consecutivos que se integran en '
                             'sílabas diferentes forman grupos:',
                 'alternativas': ['Tautosilábicos',
                                  'Heterosilábicos',
                                  'Diptongados',
                                  'Triptongados',
                                  'Fonéticos simples'],
                 'correcta': 'B'},
                {'pregunta': 'Dos vocales seguidas que se separan para '
                             'formar dos sílabas distintas constituyen:',
                 'alternativas': ['Un diptongo',
                                  'Un hiato',
                                  'Un triptongo',
                                  'Una sinalefa',
                                  'Un grupo tautosilábico'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando hay dos vocales fuertes o abiertas '
                             'juntas, como en «peón», siempre se produce:',
                 'alternativas': ['Diptongo',
                                  'Hiato',
                                  'Triptongo',
                                  'Sinéresis',
                                  'Elisión'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una vocal débil o cerrada es tónica '
                             '(lleva tilde) junto a una vocal fuerte, como '
                             'en «día», el diptongo se deshace y se forma:',
                 'alternativas': ['Un triptongo',
                                  'Un hiato',
                                  'Una sinalefa',
                                  'Un grupo consonántico',
                                  'Una elisión'],
                 'correcta': 'B'},
                {'pregunta': 'Los sonidos dentro de la sílaba se organizan '
                             'de acuerdo con la:',
                 'alternativas': ['Escala fonética simple',
                                  'Escala universal de sonoridad',
                                  'Norma académica',
                                  'Regla de acentuación',
                                  'Ley de Grimm'],
                 'correcta': 'B'}]},
 {'num': 5,
  'titulo': 'Acentuación Gráfica o Tildación',
  'secciones': [{'titulo': '5.1 CONCEPTO Y ACENTO PROSÓDICO',
                 'items': ['La {tilde}, o acento gráfico, es el signo '
                           'diacrítico que marca la acentuación de una '
                           'palabra por escrito.',
                           'No todas las palabras {tónicas} se escriben con '
                           'tilde sobre su sílaba tónica.',
                           'El acento {prosódico} diferencia en la '
                           'pronunciación una sílaba determinada, '
                           'contrastándola con el resto.',
                           'La función {contrastiva} del acento permite '
                           'diferenciar unidades acentuadas de inacentuadas.',
                           'La función {distintiva} permite diferenciar el '
                           'significado de palabras que solo se distinguen '
                           'por la tonicidad, como «médico» y «medicó».',
                           'La función {culminativa} permite percibir los '
                           'grupos acentuales que componen el discurso.']},
                {'titulo': '5.2 REGLAS SEGÚN LA POSICIÓN DEL ACENTO',
                 'items': ['Las palabras {monosilábicas} nunca se acentúan '
                           'gráficamente, salvo en los casos de tilde '
                           '{diacrítica}.',
                           'Las palabras {agudas} u oxítonas tienen la '
                           'sílaba tónica en la última posición.',
                           'Las palabras agudas llevan tilde cuando terminan '
                           'en {n}, {s} o vocal.',
                           'Las palabras {llanas} o graves, paroxítonas, '
                           'tienen la sílaba tónica en la penúltima '
                           'posición.',
                           'Las palabras llanas llevan tilde cuando terminan '
                           'en consonante distinta de {n}, s o vocal.',
                           'Las palabras {esdrújulas} o proparoxítonas '
                           'tienen la sílaba tónica en la antepenúltima '
                           'posición, y todas llevan {tilde}.',
                           'Las palabras {sobresdrújulas} tienen la sílaba '
                           'tónica anterior a la antepenúltima; son '
                           'compuestas y todas llevan tilde.']},
                {'titulo': '5.3 ACENTUACIÓN DE SECUENCIAS VOCÁLICAS',
                 'items': ['Las palabras con {diptongo} se acentúan '
                           'gráficamente según las reglas {generales} de '
                           'acentuación (agudas, llanas, esdrújulas).',
                           'Cuando una palabra con diptongo debe tildarse, '
                           'la tilde se coloca sobre la vocal {abierta} del '
                           'diptongo (o la segunda, si ambas son cerradas): '
                           '{rufián}, recién.',
                           'Las palabras con {triptongo} también siguen las '
                           'reglas generales; cuando deben tildarse, la '
                           'tilde va siempre sobre la vocal {abierta}: '
                           'apreciáis, cambiéis.',
                           'Las palabras con {hiato} siempre llevan tilde en '
                           'la vocal {cerrada}, sin importar las reglas '
                           'generales; ejemplo: {sabías}, actúe, oído.',
                           'Estas palabras con hiato de vocal cerrada tónica '
                           'llevan tilde aunque sean llanas terminadas en n, '
                           's o vocal, o agudas terminadas en consonante '
                           'distinta de {n} o s: raíz, oír, baúl, maíz.',
                           'Las palabras con hiato de dos vocales {abiertas} '
                           '(fuertes) se someten a las reglas generales de '
                           'acentuación: Jaén, traerás, peleó.']},
                {'titulo': '5.4 TILDE DIACRÍTICA EN MONOSÍLABOS',
                 'items': ['La {tilde diacrítica} es la excepción a la regla '
                           'de los monosílabos; distingue palabras {tónicas} '
                           'de sus homónimas átonas.',
                           '{Tú} es pronombre personal (tú eres); {tu} sin '
                           'tilde es adjetivo posesivo (tu casa).',
                           '{Él} es pronombre personal (él es tímido); {el} '
                           'sin tilde es artículo determinante.',
                           '{Mí} es pronombre personal (para mí); {mi} sin '
                           'tilde es adjetivo posesivo o nota musical.',
                           '{Sí} es adverbio de afirmación o pronombre '
                           '(volvió en sí); {si} sin tilde es conjunción '
                           'condicional.',
                           '{Té} es sustantivo, la infusión; {te} sin tilde '
                           'es pronombre personal.',
                           '{Dé} es forma del verbo dar; {de} sin tilde es '
                           'preposición.',
                           '{Sé} es forma del verbo ser o saber; {se} sin '
                           'tilde es pronombre personal.',
                           '{Más} es cuantificador; {mas} sin tilde es '
                           'conjunción adversativa equivalente a «pero».']},
                {'titulo': '5.5 TILDE DIACRÍTICA EN INTERROGATIVOS Y '
                           'EXCLAMATIVOS',
                 'items': ['Las palabras {qué}, cuál, quién, cómo, cuán, '
                           'cuánto, cuándo, dónde y adónde llevan tilde '
                           'cuando son {interrogativas} o exclamativas.',
                           'Los interrogativos y exclamativos pueden ir '
                           'precedidos de una {preposición} sin dejar de '
                           'llevar tilde: ¿Por qué...?, ¿Hasta cuándo...?',
                           'Existen interrogativas y exclamativas '
                           '{indirectas} que también llevan tilde: «Preguntó '
                           'qué tenía que hacer».',
                           'Estas palabras se escriben {sin tilde} cuando '
                           'funcionan como relativos, conjunciones o '
                           'preposiciones: «las flores que trajiste».']},
                {'titulo': '5.6 TILDE EN SOLO, DEMOSTRATIVOS Y AUN/AÚN',
                 'items': ['La palabra {solo} no lleva tilde, ya sea como '
                           'adverbio (equivalente a «solamente») o como '
                           '{adjetivo}.',
                           'Los demostrativos {este}, ese y aquel (con '
                           'femeninos y plurales) no llevan tilde, sea como '
                           '{pronombres} o como determinantes.',
                           '{Aún}, con tilde, puede sustituirse por '
                           '«{todavía}»: con valor temporal o '
                           'ponderativo-intensivo.',
                           '{Aun}, sin tilde, tiene valor '
                           'inclusivo-ponderativo (equivale a «incluso», '
                           '«hasta») o valor {concesivo} (equivale a '
                           '«aunque»).']}],
  'cuadros': [{'titulo': '5.2 REGLAS DE ACENTUACIÓN SEGÚN LA POSICIÓN',
               'encabezados': ['Tipo', 'Sílaba tónica', 'Regla de tilde'],
               'filas': [['{Aguda}', '{Última}', 'Termina en n, s o vocal'],
                         ['{Llana}',
                          '{Penúltima}',
                          'No termina en n, s ni vocal'],
                         ['{Esdrújula}',
                          '{Antepenúltima}',
                          'Siempre lleva tilde'],
                         ['{Sobresdrújula}',
                          'Anterior a la antepenúltima',
                          'Siempre lleva {tilde}']]},
              {'titulo': 'PARES DE TILDE DIACRÍTICA EN MONOSÍLABOS',
               'despues_de': '5.4 TILDE DIACRÍTICA EN MONOSÍLABOS',
               'encabezados': ['Con tilde', 'Sin tilde'],
               'filas': [['{Tú} (pronombre)', '{Tu} (posesivo)'],
                         ['{Él} (pronombre)', '{El} (artículo)'],
                         ['{Mí} (pronombre)', '{Mi} (posesivo/nota musical)'],
                         ['{Sí} (afirmación/pronombre)',
                          '{Si} (condicional)'],
                         ['{Té} (sustantivo, infusión)', '{Te} (pronombre)'],
                         ['{Dé} (verbo dar)', '{De} (preposición)'],
                         ['{Sé} (verbo ser/saber)', '{Se} (pronombre)'],
                         ['{Más} (cuantificador)',
                          '{Mas} (conjunción, «pero»)']]}],
  'preguntas': [{'pregunta': 'El signo diacrítico que marca la acentuación '
                             'de una palabra por escrito se llama:',
                 'alternativas': ['Diéresis',
                                  'Apóstrofo',
                                  'Guion',
                                  'Cedilla',
                                  'Tilde'],
                 'correcta': 'E'},
                {'pregunta': 'El acento que diferencia en la pronunciación '
                             'una sílaba, contrastándola con el resto, es el '
                             'acento:',
                 'alternativas': ['Diacrítico',
                                  'Ortográfico exclusivo',
                                  'Fonológico puro',
                                  'Gráfico',
                                  'Prosódico'],
                 'correcta': 'E'},
                {'pregunta': 'La función del acento que diferencia unidades '
                             'acentuadas de inacentuadas es la función:',
                 'alternativas': ['Culminativa',
                                  'Contrastiva',
                                  'Gráfica',
                                  'Distintiva',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'La función del acento que diferencia el '
                             'significado de palabras como «médico» y '
                             '«medicó» es la función:',
                 'alternativas': ['Distintiva',
                                  'Ortográfica',
                                  'Contrastiva',
                                  'Culminativa',
                                  'Prosódica pura'],
                 'correcta': 'A'},
                {'pregunta': 'La función que permite percibir los grupos '
                             'acentuales del discurso es la función:',
                 'alternativas': ['Gráfica',
                                  'Semántica',
                                  'Contrastiva',
                                  'Distintiva',
                                  'Culminativa'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras monosilábicas, por regla general:',
                 'alternativas': ['Se acentúan según el contexto',
                                  'Siempre llevan tilde',
                                  'Llevan tilde si son agudas',
                                  'Llevan doble tilde',
                                  'Nunca se acentúan gráficamente, salvo '
                                  'tilde diacrítica'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras agudas tienen la sílaba tónica en '
                             'la posición:',
                 'alternativas': ['Última',
                                  'Antepenúltima',
                                  'Anterior a la antepenúltima',
                                  'Penúltima',
                                  'Primera'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras agudas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['Cualquier consonante',
                                  'La letra y siempre',
                                  'Ninguna terminación específica',
                                  'Solo consonantes dobles',
                                  'N, s o vocal'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras llanas o graves tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Anterior a la antepenúltima',
                                  'Primera',
                                  'Última',
                                  'Antepenúltima',
                                  'Penúltima'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras llanas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['Solo vocal',
                                  'Ninguna terminación',
                                  'N, s o vocal',
                                  'Solo la letra y',
                                  'Consonante distinta de n, s o vocal'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras esdrújulas tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Antepenúltima',
                                  'Penúltima',
                                  'Primera exclusivamente',
                                  'Última',
                                  'Anterior a la antepenúltima'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras esdrújulas, en cuanto a la tilde:',
                 'alternativas': ['Llevan tilde solo si terminan en vocal',
                                  'Todas llevan tilde',
                                  'Nunca llevan tilde',
                                  'Solo algunas llevan tilde',
                                  'Dependen del contexto'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras sobresdrújulas tienen la sílaba '
                             'tónica:',
                 'alternativas': ['En la última posición',
                                  'En la antepenúltima',
                                  'Sin posición fija',
                                  'Anterior a la antepenúltima',
                                  'En la penúltima'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras sobresdrújulas se caracterizan '
                             'por ser:',
                 'alternativas': ['Monosilábicas',
                                  'Siempre simples',
                                  'Compuestas, y todas llevan tilde',
                                  'Solo verbos',
                                  'Sin tilde nunca'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «cuéntaselo» es un ejemplo de '
                             'palabra:',
                 'alternativas': ['Llana',
                                  'Esdrújula',
                                  'Sobresdrújula',
                                  'Monosilábica',
                                  'Aguda'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «césped» es un ejemplo de palabra:',
                 'alternativas': ['Llana',
                                  'Monosilábica',
                                  'Sobresdrújula',
                                  'Esdrújula',
                                  'Aguda'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «comité» lleva tilde porque es '
                             'aguda terminada en:',
                 'alternativas': ['Consonante doble',
                                  'Vocal',
                                  'S',
                                  'Consonante distinta de n o s',
                                  'N'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «botón» lleva tilde porque es aguda '
                             'terminada en:',
                 'alternativas': ['La letra y',
                                  'S',
                                  'Consonante doble',
                                  'N',
                                  'Vocal'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «jueves» no lleva tilde porque, '
                             'siendo llana, termina en:',
                 'alternativas': ['Consonante distinta de n o s',
                                  'Vocal abierta tónica',
                                  'S',
                                  'La letra y',
                                  'Consonante doble'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «música» es un ejemplo de palabra:',
                 'alternativas': ['Sobresdrújula',
                                  'Monosilábica',
                                  'Llana',
                                  'Aguda',
                                  'Esdrújula'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras con diptongo se acentúan '
                             'gráficamente de acuerdo con:',
                 'alternativas': ['Una regla especial exclusiva',
                                  'Las reglas generales de acentuación',
                                  'No se acentúan nunca',
                                  'Solo la posición del hiato',
                                  'Reglas del triptongo'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una palabra con diptongo debe llevar '
                             'tilde, esta se coloca sobre:',
                 'alternativas': ['La vocal cerrada siempre',
                                  'La vocal abierta del diptongo',
                                  'La primera vocal siempre',
                                  'La última letra de la palabra',
                                  'Ninguna vocal específica'],
                 'correcta': 'B'},
                {'pregunta': 'En las palabras con triptongo que deben '
                             'tildarse, como «apreciáis», la tilde se coloca '
                             'sobre:',
                 'alternativas': ['La primera vocal cerrada',
                                  'La vocal abierta',
                                  'La segunda vocal cerrada',
                                  'La consonante final',
                                  'Ninguna vocal'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras con hiato siempre llevan tilde '
                             'en:',
                 'alternativas': ['La vocal abierta',
                                  'La vocal cerrada',
                                  'La consonante final',
                                  'La primera sílaba',
                                  'La última sílaba únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «sabías», con hiato, lleva tilde en '
                             'la vocal cerrada a pesar de ser una palabra:',
                 'alternativas': ['Aguda terminada en consonante',
                                  'Llana terminada en vocal',
                                  'Esdrújula',
                                  'Sobresdrújula',
                                  'Monosilábica'],
                 'correcta': 'B'},
                {'pregunta': 'Palabras como «raíz» y «maíz» llevan tilde en '
                             'el hiato a pesar de ser palabras agudas '
                             'terminadas en:',
                 'alternativas': ['N o s',
                                  'Consonante distinta de n o s',
                                  'Vocal',
                                  'Y',
                                  'Consonante doble'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una palabra tiene hiato de dos vocales '
                             'abiertas o fuertes juntas, como «Jaén» o '
                             '«peleó», la acentuación sigue:',
                 'alternativas': ['Una regla exclusiva del hiato',
                                  'Las reglas generales de acentuación',
                                  'No se acentúan nunca',
                                  'Solo la regla del diptongo',
                                  'Ninguna regla específica'],
                 'correcta': 'B'},
                {'pregunta': 'En la oración «Tú eres Santiago», la palabra '
                             '«tú» lleva tilde porque funciona como:',
                 'alternativas': ['Adjetivo posesivo',
                                  'Pronombre personal',
                                  'Conjunción',
                                  'Preposición',
                                  'Adverbio'],
                 'correcta': 'B'},
                {'pregunta': 'En la oración «Tu casa es muy hermosa», la '
                             'palabra «tu» no lleva tilde porque funciona '
                             'como:',
                 'alternativas': ['Pronombre personal',
                                  'Adjetivo posesivo',
                                  'Conjunción',
                                  'Adverbio',
                                  'Preposición'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «sí», con tilde, funciona como '
                             'adverbio de afirmación o como pronombre '
                             'personal, mientras que «si», sin tilde, '
                             'funciona como:',
                 'alternativas': ['Sustantivo exclusivo',
                                  'Conjunción condicional',
                                  'Adjetivo',
                                  'Adverbio de lugar',
                                  'Pronombre personal'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «dé», forma del verbo dar, lleva '
                             'tilde para distinguirse de «de», que sin tilde '
                             'funciona como:',
                 'alternativas': ['Pronombre',
                                  'Preposición',
                                  'Adverbio',
                                  'Conjunción',
                                  'Adjetivo'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «más», cuantificador, lleva tilde '
                             'para distinguirse de «mas», que sin tilde es '
                             'una conjunción equivalente a:',
                 'alternativas': ['Y', 'Pero', 'O', 'Porque', 'Aunque'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras qué, cuál, quién, cómo, dónde y '
                             'cuándo se escriben con tilde diacrítica cuando '
                             'son:',
                 'alternativas': ['Relativos o conjunciones',
                                  'Interrogativas o exclamativas',
                                  'Preposiciones',
                                  'Adverbios de modo exclusivos',
                                  'Artículos'],
                 'correcta': 'B'},
                {'pregunta': 'En la oración «¿Por qué ha dicho eso?», la '
                             'palabra «qué» lleva tilde a pesar de estar '
                             'precedida por una:',
                 'alternativas': ['Conjunción',
                                  'Preposición',
                                  'Otro interrogativo',
                                  'Un artículo',
                                  'Un pronombre'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras qué, cuál, quién, cómo, dónde y '
                             'cuándo se escriben sin tilde cuando funcionan '
                             'como:',
                 'alternativas': ['Interrogativas directas',
                                  'Relativos, conjunciones o preposiciones',
                                  'Exclamativas indirectas',
                                  'Adjetivos calificativos',
                                  'Sustantivos'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «solo» no lleva tilde, ya sea que '
                             'funcione como adverbio (solamente) o como:',
                 'alternativas': ['Sustantivo',
                                  'Adjetivo',
                                  'Pronombre',
                                  'Conjunción',
                                  'Preposición'],
                 'correcta': 'B'},
                {'pregunta': 'Los demostrativos este, ese y aquel, con sus '
                             'femeninos y plurales, no llevan tilde, sea que '
                             'funcionen como pronombres o como:',
                 'alternativas': ['Sustantivos',
                                  'Determinantes',
                                  'Adverbios',
                                  'Conjunciones',
                                  'Preposiciones'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «aún», con tilde, puede sustituirse '
                             'por «todavía», con valor temporal o:',
                 'alternativas': ['Concesivo',
                                  'Ponderativo o intensivo',
                                  'Inclusivo',
                                  'Condicional',
                                  'Adversativo'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «aun», sin tilde, tiene valor '
                             'inclusivo-ponderativo (equivalente a '
                             '«incluso») o valor:',
                 'alternativas': ['Temporal',
                                  'Concesivo',
                                  'Intensivo exclusivo',
                                  'Afirmativo',
                                  'Interrogativo'],
                 'correcta': 'B'}]},
 {'num': 6,
  'titulo': 'Uso de las Letras Mayúsculas y Minúsculas',
  'secciones': [{'titulo': '6.1 CONSIDERACIONES BÁSICAS',
                 'items': ['La escritura enteramente en {mayúsculas} es '
                           'propia de las siglas, los números romanos y '
                           'textos cortos informativos.',
                           'El uso combinado de minúsculas y mayúsculas '
                           'dentro de una palabra debe {evitarse} en la '
                           'escritura normal.',
                           'La {mayúscula inicial} marca el inicio de '
                           'enunciados, párrafos y delimita los nombres '
                           'propios.']},
                {'titulo': '6.2 SIGLAS Y NOMBRES CIENTÍFICOS',
                 'items': ['Las {siglas} se escriben con mayúscula todas las '
                           'letras que las componen, como PNP o {DNI}.',
                           'Las siglas se escriben {sin} puntos, mientras '
                           'que las abreviaturas sí los llevan, como pág. o '
                           '{Sr.}',
                           'Los nombres latinos de especies, como Homo '
                           'sapiens, se escriben con mayúscula inicial y en '
                           '{cursiva}.',
                           'La palabra {Dios} se escribe con mayúscula '
                           'cuando se usa sin artículo como nombre propio '
                           'del ser supremo monoteísta.']},
                {'titulo': '6.3 CASOS ESPECIALES DE MAYÚSCULA INICIAL',
                 'items': ['Si los dígrafos ch, ll, gu o qu aparecen al '
                           'inicio de una palabra con mayúscula, solo la '
                           '{primera} letra se escribe en mayúscula, como en '
                           '«{Chávez}» o «Quito».',
                           'La mayúscula de las letras {i} y j carece del '
                           'punto sobrescrito característico de su forma '
                           'minúscula.',
                           'La {antonomasia} es el fenómeno por el cual un '
                           'nombre común reemplaza a un nombre propio, como '
                           '«el Salvador» por Jesucristo.',
                           'La {personificación} atribuye rasgos humanos a '
                           'conceptos abstractos, como en «la Muerte se '
                           'presentó».']},
                {'titulo': '6.4 LA MAYÚSCULA CONDICIONADA POR LA PUNTUACIÓN',
                 'items': ['Se escribe con mayúscula la primera palabra de '
                           'un escrito y la que va después de un {punto}.',
                           'Se escribe con mayúscula la palabra que sigue a '
                           'los puntos {suspensivos} cuando estos cierran un '
                           'enunciado.',
                           'Si los puntos suspensivos no cierran el '
                           'enunciado, la palabra siguiente se escribe con '
                           '{minúscula}.',
                           'Después de {dos puntos} se escribe mayúscula '
                           'cuando estos anuncian el inicio de una unidad '
                           'independiente, como en el saludo de una '
                           '{carta}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La escritura enteramente en mayúsculas es propia '
                           'de las siglas, los números romanos y {Los textos '
                           'cortos informativos}.',
                           'El uso combinado de minúsculas y mayúsculas '
                           'dentro de una misma palabra debe {Evitarse en la '
                           'escritura normal}.',
                           'Las siglas se escriben con mayúscula {Todas las '
                           'letras que las componen}.',
                           'Las siglas, a diferencia de las abreviaturas, se '
                           'escriben {Sin puntos}.',
                           'Las abreviaturas, a diferencia de las siglas, se '
                           'escriben {Con puntos}.',
                           'Los nombres latinos de especies, como «Homo '
                           'sapiens», se escriben con mayúscula inicial y '
                           '{En cursiva}.',
                           'La palabra «Dios» se escribe con mayúscula '
                           'cuando se usa {Sin artículo, como nombre propio '
                           'del ser supremo monoteísta}.',
                           'Si un dígrafo como «ch» o «ll» aparece al inicio '
                           'de una palabra con mayúscula, se escribe en '
                           'mayúscula {Solo la primera letra}.',
                           'La mayúscula de las letras i y j, a diferencia '
                           'de su forma minúscula {Carece del punto '
                           'sobrescrito}.',
                           'El fenómeno por el cual un nombre común '
                           'reemplaza completamente a un nombre propio se '
                           'llama {Antonomasia}.',
                           'El fenómeno que atribuye rasgos humanos a '
                           'conceptos abstractos, como «la Muerte», se llama '
                           '{Personificación}.',
                           'Se escribe con mayúscula la primera palabra de '
                           'un escrito y la que va después de {Un punto}.',
                           'La palabra que sigue a los puntos suspensivos, '
                           'cuando estos cierran un enunciado, se escribe '
                           'con {Mayúscula}.',
                           'Después de dos puntos se escribe mayúscula '
                           'cuando anuncian el inicio de una unidad '
                           'independiente, como en {El saludo de una carta}.',
                           'Los documentos jurídicos que usan mayúscula '
                           'total suelen presentar palabras como '
                           '{CERTIFICA}.',
                           'La mayúscula inicial marca y delimita, entre '
                           'otras cosas {Los nombres propios}.',
                           'Las siglas «RAE» y «AVE» ejemplifican el uso de '
                           'mayúsculas para {Formar e identificar siglas}.',
                           'Los números romanos, como «XXI», se escriben '
                           '{Enteramente en mayúsculas}.']}],
  'cuadros': [{'titulo': '6.2 SIGLAS FRENTE A ABREVIATURAS',
               'encabezados': ['Tipo', 'Lleva puntos', 'Ejemplo'],
               'filas': [['{Siglas}', '{No}', 'PNP, DNI'],
                         ['{Abreviaturas}', '{Sí}', 'pág., Sr.']]}],
  'preguntas': [{'pregunta': 'La escritura enteramente en mayúsculas es '
                             'propia de las siglas, los números romanos y:',
                 'alternativas': ['Las preposiciones',
                                  'Los textos cortos informativos',
                                  'Los artículos',
                                  'Los adjetivos calificativos',
                                  'Los verbos irregulares'],
                 'correcta': 'B'},
                {'pregunta': 'El uso combinado de minúsculas y mayúsculas '
                             'dentro de una misma palabra debe:',
                 'alternativas': ['Prohibirse en las siglas',
                                  'Fomentarse siempre',
                                  'Aplicarse en cartas oficiales',
                                  'Evitarse en la escritura normal',
                                  'Usarse en todo texto formal'],
                 'correcta': 'D'},
                {'pregunta': 'Las siglas se escriben con mayúscula:',
                 'alternativas': ['Solo las consonantes',
                                  'Solo la primera letra',
                                  'Todas las letras que las componen',
                                  'Ninguna letra en particular',
                                  'Solo las vocales'],
                 'correcta': 'C'},
                {'pregunta': 'Las siglas, a diferencia de las abreviaturas, '
                             'se escriben:',
                 'alternativas': ['Con guion final',
                                  'Solo entre comillas',
                                  'Con puntos',
                                  'Sin puntos',
                                  'Solo en cursiva'],
                 'correcta': 'D'},
                {'pregunta': 'Las abreviaturas, a diferencia de las siglas, '
                             'se escriben:',
                 'alternativas': ['Solo en números',
                                  'En cursiva obligatoria',
                                  'Sin puntos',
                                  'Sin mayúsculas nunca',
                                  'Con puntos'],
                 'correcta': 'E'},
                {'pregunta': 'Los nombres latinos de especies, como «Homo '
                             'sapiens», se escriben con mayúscula inicial y:',
                 'alternativas': ['Subrayados',
                                  'Entre comillas',
                                  'En cursiva',
                                  'Entre paréntesis',
                                  'En negrita'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «Dios» se escribe con mayúscula '
                             'cuando se usa:',
                 'alternativas': ['Nunca en español',
                                  'Solo en textos religiosos católicos',
                                  'Solo en mayúscula total',
                                  'Sin artículo, como nombre propio del ser '
                                  'supremo monoteísta',
                                  'Con artículo, en sentido genérico'],
                 'correcta': 'D'},
                {'pregunta': 'Si un dígrafo como «ch» o «ll» aparece al '
                             'inicio de una palabra con mayúscula, se '
                             'escribe en mayúscula:',
                 'alternativas': ['Ambas letras del dígrafo',
                                  'Solo la primera letra',
                                  'Todo en minúscula',
                                  'Ninguna letra',
                                  'Solo la segunda letra'],
                 'correcta': 'B'},
                {'pregunta': 'La mayúscula de las letras i y j, a diferencia '
                             'de su forma minúscula:',
                 'alternativas': ['Lleva doble punto',
                                  'No existe en mayúscula',
                                  'Carece del punto sobrescrito',
                                  'Se escribe en cursiva siempre',
                                  'Lleva tilde obligatoria'],
                 'correcta': 'C'},
                {'pregunta': 'El fenómeno por el cual un nombre común '
                             'reemplaza completamente a un nombre propio se '
                             'llama:',
                 'alternativas': ['Personificación',
                                  'Metonimia',
                                  'Sinécdoque',
                                  'Antonomasia',
                                  'Hipérbole'],
                 'correcta': 'D'},
                {'pregunta': 'El fenómeno que atribuye rasgos humanos a '
                             'conceptos abstractos, como «la Muerte», se '
                             'llama:',
                 'alternativas': ['Ironía',
                                  'Personificación',
                                  'Comparación',
                                  'Metáfora exclusiva',
                                  'Antonomasia'],
                 'correcta': 'B'},
                {'pregunta': 'Se escribe con mayúscula la primera palabra de '
                             'un escrito y la que va después de:',
                 'alternativas': ['Un paréntesis',
                                  'Un guion',
                                  'Una coma',
                                  'Unas comillas',
                                  'Un punto'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra que sigue a los puntos suspensivos, '
                             'cuando estos cierran un enunciado, se escribe '
                             'con:',
                 'alternativas': ['Comillas',
                                  'Mayúscula',
                                  'Cursiva obligatoria',
                                  'Minúscula siempre',
                                  'Negrita'],
                 'correcta': 'B'},
                {'pregunta': 'Si los puntos suspensivos NO cierran el '
                             'enunciado, la palabra siguiente se escribe '
                             'con:',
                 'alternativas': ['Minúscula',
                                  'Subrayado',
                                  'Cursiva',
                                  'Negrita obligatoria',
                                  'Mayúscula'],
                 'correcta': 'A'},
                {'pregunta': 'Después de dos puntos se escribe mayúscula '
                             'cuando anuncian el inicio de una unidad '
                             'independiente, como en:',
                 'alternativas': ['Una enumeración simple',
                                  'Un ejemplo cualquiera',
                                  'Una lista de compras',
                                  'Una cita textual breve',
                                  'El saludo de una carta'],
                 'correcta': 'E'},
                {'pregunta': 'Los documentos jurídicos que usan mayúscula '
                             'total suelen presentar palabras como:',
                 'alternativas': ['Estimado',
                                  'Atentamente',
                                  'Saludos',
                                  'CERTIFICA',
                                  'Considerando'],
                 'correcta': 'D'},
                {'pregunta': 'La mayúscula inicial marca y delimita, entre '
                             'otras cosas:',
                 'alternativas': ['Los nombres propios',
                                  'Las conjunciones',
                                  'Las preposiciones',
                                  'Los artículos indeterminados',
                                  'Los verbos conjugados'],
                 'correcta': 'A'},
                {'pregunta': '«El Salvador» usado para referirse a '
                             'Jesucristo es un ejemplo de:',
                 'alternativas': ['Ironía',
                                  'Metáfora pura',
                                  'Antonomasia',
                                  'Personificación',
                                  'Sinécdoque'],
                 'correcta': 'C'},
                {'pregunta': 'Las siglas «RAE» y «AVE» ejemplifican el uso '
                             'de mayúsculas para:',
                 'alternativas': ['Nombres propios de personas',
                                  'Formar e identificar siglas',
                                  'Documentos jurídicos',
                                  'Números romanos',
                                  'Cartas formales'],
                 'correcta': 'B'},
                {'pregunta': 'Los números romanos, como «XXI», se escriben:',
                 'alternativas': ['En minúscula',
                                  'Enteramente en mayúsculas',
                                  'Con tilde',
                                  'Entre comillas',
                                  'En cursiva obligatoria'],
                 'correcta': 'B'}]},
 {'num': 7,
  'titulo': 'Signos de Puntuación',
  'secciones': [{'titulo': '7.1 CONCEPTO Y FUNCIONES',
                 'items': ['Los signos de puntuación son signos '
                           '{ortográficos} que organizan el discurso para '
                           'facilitar su {comprensión}.',
                           'Los signos de puntuación ponen de manifiesto las '
                           'relaciones {sintácticas} y lógicas entre los '
                           'constituyentes del texto.',
                           'Una función de los signos de puntuación es '
                           'indicar los {límites} de las unidades '
                           'discursivas.',
                           'Otra función es indicar la {modalidad} de los '
                           'enunciados: enunciativa, interrogativa o '
                           'exclamativa.',
                           'Otra función es indicar la {omisión} de una '
                           'parte del enunciado, como en «A quien '
                           'madruga…».']},
                {'titulo': '7.2 EL PUNTO',
                 'items': ['El punto se usa en las {abreviaturas}, como '
                           '«Sra.» o «pág.».',
                           'El punto se usa también en {fechas} y horas, '
                           'como 22.02.22.',
                           'Nunca se escribe punto al final de {títulos} y '
                           'subtítulos de libros, artículos u obras de arte.',
                           'Tampoco se escribe punto después de los '
                           '{nombres} de autor en portadas o firmas de '
                           'documentos.',
                           'Tampoco se usa punto en {dedicatorias}, ni en '
                           'eslóganes, ni en direcciones {electrónicas}.']},
                {'titulo': '7.3 LA COMA',
                 'items': ['La coma {incidental} se usa para intercalar '
                           'información aclaratoria dentro del enunciado.',
                           'La coma {vocativa} se usa para separar el nombre '
                           'de la persona a quien nos dirigimos, como en '
                           '«Eduardo, no quiero que salgas tan tarde».']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los signos de puntuación son signos ortográficos '
                           'que organizan el discurso para facilitar su '
                           '{Comprensión}.',
                           'Una función de los signos de puntuación es '
                           'indicar los límites de {Las unidades '
                           'discursivas}.',
                           'La función que indica si un enunciado es '
                           'interrogativo o exclamativo es la función de '
                           '{Modalidad del enunciado}.',
                           'El punto se usa correctamente en {Las '
                           'abreviaturas}.',
                           'El punto se usa también en {Fechas y horas}.',
                           'Los nombres de autor en portadas, prólogos o '
                           'firmas de documentos se escriben {Sin punto '
                           'final}.',
                           'Las dedicatorias, como «Para William», se '
                           'escriben {Sin punto final}.',
                           'Los eslóganes publicitarios, por regla general, '
                           'se escriben {Sin punto final}.',
                           'Las direcciones electrónicas, como '
                           'www.unsaac.edu.pe, se escriben {Sin punto '
                           'final}.',
                           'La coma que intercala información aclaratoria '
                           'dentro del enunciado es la coma {Incidental}.',
                           'La coma que separa el nombre de la persona a '
                           'quien nos dirigimos es la coma {Vocativa}.',
                           'En «Eduardo, no quiero que salgas tan tarde», la '
                           'coma usada es la coma {Vocativa}.',
                           'En «La mansión, abandonada, se convirtió en '
                           'refugio», la coma usada es la coma {Incidental}.',
                           'El punto se usa en abreviaturas como {Sra.}.',
                           'Las enumeraciones en forma de lista, como en un '
                           'examen de opción múltiple, se escriben {Sin '
                           'punto final en cada ítem}.',
                           'Los pies de imagen y cabeceras de cuadros, '
                           'cuando son breves, se escriben {Generalmente sin '
                           'punto}.',
                           'Los signos de puntuación señalan el carácter '
                           'especial de fragmentos como {Citas e incisos}.',
                           'El punto se usa correctamente después de una '
                           'hora como {17.30}.']}],
  'cuadros': [{'titulo': '7.2 CASOS SIN PUNTO FINAL',
               'encabezados': ['Caso', 'Ejemplo'],
               'filas': [['{Títulos} de obras', 'El viejo y el {mar}'],
                         ['Nombres de {autor}', 'Firma en un documento'],
                         ['{Dedicatorias}', 'Para William'],
                         ['{Eslóganes}',
                          'Turismo en Cusco, vívelo en directo'],
                         ['Direcciones {electrónicas}',
                          'www.unsaac.edu.pe']]}],
  'preguntas': [{'pregunta': 'Los signos de puntuación son signos '
                             'ortográficos que organizan el discurso para '
                             'facilitar su:',
                 'alternativas': ['Memorización',
                                  'Eliminación',
                                  'Pronunciación exclusiva',
                                  'Traducción',
                                  'Comprensión'],
                 'correcta': 'E'},
                {'pregunta': 'Una función de los signos de puntuación es '
                             'indicar los límites de:',
                 'alternativas': ['Las sílabas',
                                  'Las unidades discursivas',
                                  'Las palabras sueltas',
                                  'Los fonemas',
                                  'Los morfemas'],
                 'correcta': 'B'},
                {'pregunta': 'La función que indica si un enunciado es '
                             'interrogativo o exclamativo es la función de:',
                 'alternativas': ['Modalidad del enunciado',
                                  'Límites discursivos',
                                  'Cohesión',
                                  'Referencia',
                                  'Omisión'],
                 'correcta': 'A'},
                {'pregunta': 'El punto se usa correctamente en:',
                 'alternativas': ['Las abreviaturas',
                                  'Los eslóganes',
                                  'Las direcciones electrónicas',
                                  'Las dedicatorias',
                                  'Los títulos de libros'],
                 'correcta': 'A'},
                {'pregunta': 'El punto se usa también en:',
                 'alternativas': ['Las direcciones web',
                                  'Los títulos de obras de arte',
                                  'Los eslóganes publicitarios',
                                  'Los nombres de autor en portadas',
                                  'Fechas y horas'],
                 'correcta': 'E'},
                {'pregunta': 'NO se escribe punto al final de:',
                 'alternativas': ['Los títulos y subtítulos de libros',
                                  'Una fecha completa',
                                  'Una abreviatura',
                                  'Un párrafo normal',
                                  'Una hora exacta'],
                 'correcta': 'A'},
                {'pregunta': 'Los nombres de autor en portadas, prólogos o '
                             'firmas de documentos se escriben:',
                 'alternativas': ['Entre comillas obligatorias',
                                  'Con punto final',
                                  'Subrayados siempre',
                                  'En mayúscula total',
                                  'Sin punto final'],
                 'correcta': 'E'},
                {'pregunta': 'Las dedicatorias, como «Para William», se '
                             'escriben:',
                 'alternativas': ['Entre paréntesis',
                                  'Sin punto final',
                                  'Con punto final',
                                  'Con doble punto',
                                  'En cursiva obligatoria'],
                 'correcta': 'B'},
                {'pregunta': 'Los eslóganes publicitarios, por regla '
                             'general, se escriben:',
                 'alternativas': ['Entre comillas siempre',
                                  'Con punto final',
                                  'Solo en mayúsculas',
                                  'Sin punto final',
                                  'Con coma final'],
                 'correcta': 'D'},
                {'pregunta': 'Las direcciones electrónicas, como '
                             'www.unsaac.edu.pe, se escriben:',
                 'alternativas': ['Entre corchetes',
                                  'Con guion final',
                                  'Solo en mayúsculas',
                                  'Con punto final obligatorio',
                                  'Sin punto final'],
                 'correcta': 'E'},
                {'pregunta': 'La coma que intercala información aclaratoria '
                             'dentro del enunciado es la coma:',
                 'alternativas': ['Enumerativa',
                                  'Elíptica',
                                  'Vocativa',
                                  'Incidental',
                                  'Hiperbática'],
                 'correcta': 'D'},
                {'pregunta': 'La coma que separa el nombre de la persona a '
                             'quien nos dirigimos es la coma:',
                 'alternativas': ['Enumerativa',
                                  'Vocativa',
                                  'Distributiva',
                                  'Incidental',
                                  'Explicativa'],
                 'correcta': 'B'},
                {'pregunta': 'En «Eduardo, no quiero que salgas tan tarde», '
                             'la coma usada es la coma:',
                 'alternativas': ['Vocativa',
                                  'Incidental',
                                  'Elíptica',
                                  'Enumerativa',
                                  'Hiperbática'],
                 'correcta': 'A'},
                {'pregunta': 'En «La mansión, abandonada, se convirtió en '
                             'refugio», la coma usada es la coma:',
                 'alternativas': ['Incidental',
                                  'Vocativa',
                                  'Final',
                                  'Enumerativa',
                                  'Distributiva'],
                 'correcta': 'A'},
                {'pregunta': 'El punto se usa en abreviaturas como:',
                 'alternativas': ['Sra.', 'AFP', 'ONU', 'RAE', 'DNI'],
                 'correcta': 'A'},
                {'pregunta': 'Las enumeraciones en forma de lista, como en '
                             'un examen de opción múltiple, se escriben:',
                 'alternativas': ['En un solo párrafo continuo',
                                  'Con punto final en cada ítem '
                                  'obligatoriamente',
                                  'Solo con punto y coma',
                                  'Solo con coma',
                                  'Sin punto final en cada ítem'],
                 'correcta': 'E'},
                {'pregunta': 'Los pies de imagen y cabeceras de cuadros, '
                             'cuando son breves, se escriben:',
                 'alternativas': ['Con dos puntos finales',
                                  'Siempre con punto',
                                  'En mayúscula total',
                                  'Entre comillas obligatorias',
                                  'Generalmente sin punto'],
                 'correcta': 'E'},
                {'pregunta': 'Los signos de puntuación señalan el carácter '
                             'especial de fragmentos como:',
                 'alternativas': ['Solo los títulos',
                                  'Solo los nombres propios',
                                  'Solo las siglas',
                                  'Solo los números',
                                  'Citas e incisos'],
                 'correcta': 'E'},
                {'pregunta': '«A quien madruga…» ejemplifica la función de '
                             'los signos de puntuación de indicar:',
                 'alternativas': ['Límites discursivos',
                                  'Una fecha',
                                  'Una cita textual',
                                  'Modalidad interrogativa',
                                  'La omisión de una parte del enunciado'],
                 'correcta': 'E'},
                {'pregunta': 'El punto se usa correctamente después de una '
                             'hora como:',
                 'alternativas': ['17:30 con coma',
                                  'Diecisiete treinta escrito',
                                  '17.30',
                                  '1730 sin separador',
                                  '17-30'],
                 'correcta': 'C'}]},
 {'num': 8,
  'titulo': 'El Sustantivo',
  'secciones': [{'titulo': '8.1 CRITERIOS PARA DEFINIR EL SUSTANTIVO',
                 'items': ['Según el criterio {semántico}, el sustantivo '
                           'designa a los seres y objetos de la realidad, de '
                           'existencia {concreta} o abstracta.',
                           'Según el criterio {morfológico}, el sustantivo '
                           'es una palabra variable con morfemas de {género} '
                           'y número.',
                           'Según el criterio {sintáctico}, el sustantivo '
                           'forma grupos nominales capaces de cumplir '
                           'funciones como sujeto o complemento.']},
                {'titulo': '8.2 FUNCIONES DEL SUSTANTIVO',
                 'items': ['El sustantivo puede funcionar como núcleo del '
                           '{sujeto}, del complemento directo, indirecto o '
                           '{circunstancial}.',
                           'El sustantivo puede funcionar como núcleo del '
                           '{vocativo}, como en «Señorita, aquí tiene su '
                           'cuaderno».',
                           'El sustantivo puede funcionar como núcleo de la '
                           '{aposición}, como en «Ricardo Palma, el '
                           'bibliotecario mendigo».',
                           'El sustantivo puede funcionar como núcleo del '
                           'complemento {agente}, en oraciones de voz '
                           'pasiva.']},
                {'titulo': '8.3 SUSTANTIVOS PROPIOS Y COMUNES',
                 'items': ['Los sustantivos {propios} nombran a los seres '
                           'diferenciándolos de los demás de su misma '
                           'especie, y se escriben con {mayúscula} inicial.',
                           'Los sustantivos {comunes} nombran a todos los '
                           'seres de una clase, y se escriben con '
                           '{minúscula} inicial.']},
                {'titulo': '8.4 OTRAS CLASIFICACIONES DEL SUSTANTIVO',
                 'items': ['Los sustantivos {contables} designan entidades '
                           'que se pueden contar, como «tres planetas».',
                           'Los sustantivos {no contables} denotan '
                           'magnitudes o sustancias, como «un poco de café».',
                           'Los sustantivos {concretos} nombran seres '
                           'percibidos por los sentidos, con existencia '
                           '{independiente}.',
                           'Los sustantivos {abstractos} nombran seres '
                           'conocidos mediante un proceso mental de '
                           '{abstracción}.',
                           'Los sustantivos {individuales} nombran a un solo '
                           'ser; los sustantivos {colectivos} designan, en '
                           'singular, un conjunto de seres.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, el sustantivo '
                           'designa {Seres y objetos de la realidad}.',
                           'Según el criterio morfológico, el sustantivo es '
                           'una palabra {Variable, con morfemas de género y '
                           'número}.',
                           'Según el criterio sintáctico, el sustantivo '
                           'forma grupos nominales que pueden cumplir '
                           'función de {Sujeto, complemento directo, '
                           'indirecto, entre otros}.',
                           'En «El profesor viajará muy pronto», el '
                           'sustantivo «profesor» funciona como núcleo de '
                           '{El sujeto}.',
                           'En «Señorita, aquí tiene su cuaderno», '
                           '«Señorita» funciona como núcleo del {Vocativo}.',
                           'En «Ricardo Palma, el bibliotecario mendigo, '
                           'escribió Tradiciones peruanas», «el '
                           'bibliotecario mendigo» es núcleo de {La '
                           'aposición}.',
                           'En «El cuento fue leído por el niño», «el niño» '
                           'funciona como núcleo del complemento {Agente}.',
                           'Los sustantivos que nombran a los seres '
                           'diferenciándolos de los demás de su especie son '
                           'los sustantivos {Propios}.',
                           'Los sustantivos propios, ortográficamente, se '
                           'escriben con {Mayúscula inicial}.',
                           'Los sustantivos que nombran a todos los seres de '
                           'una clase son los sustantivos {Comunes}.',
                           'Los sustantivos que designan entidades que se '
                           'pueden contar son los sustantivos {Contables}.',
                           'Los sustantivos que denotan magnitudes o '
                           'sustancias, como «un poco de café», son los '
                           'sustantivos {No contables}.',
                           'Los sustantivos que nombran seres percibidos por '
                           'los sentidos son los sustantivos {Concretos}.',
                           'Los sustantivos que se conocen mediante un '
                           'proceso mental de abstracción son los '
                           'sustantivos {Abstractos}.',
                           'Los sustantivos que nombran a un solo ser son '
                           'los sustantivos {Individuales}.',
                           'Los sustantivos colectivos, en número singular, '
                           'designan {Un conjunto de seres}.',
                           'En «Aquellos jóvenes parecen buenos '
                           'profesionales», «profesionales» funciona como '
                           'núcleo de {El atributo}.']}],
  'cuadros': [{'titulo': '8.4 CLASIFICACIONES DEL SUSTANTIVO',
               'encabezados': ['Clasificación', 'Tipos'],
               'filas': [['Por su extensión', '{Propios} y comunes'],
                         ['Por su cuantificación',
                          '{Contables} y no contables'],
                         ['Por su percepción', '{Concretos} y abstractos'],
                         ['Por su número', '{Individuales} y colectivos']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el sustantivo '
                             'designa:',
                 'alternativas': ['Solo relaciones lógicas',
                                  'Solo cantidades',
                                  'Solo acciones',
                                  'Solo cualidades',
                                  'Seres y objetos de la realidad'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio morfológico, el sustantivo '
                             'es una palabra:',
                 'alternativas': ['Sin composición posible',
                                  'Sin flexión',
                                  'Invariable',
                                  'Variable, con morfemas de género y número',
                                  'Exclusivamente derivada'],
                 'correcta': 'D'},
                {'pregunta': 'Según el criterio sintáctico, el sustantivo '
                             'forma grupos nominales que pueden cumplir '
                             'función de:',
                 'alternativas': ['Solo conjunción',
                                  'Solo verbo',
                                  'Solo adjetivo',
                                  'Solo preposición',
                                  'Sujeto, complemento directo, indirecto, '
                                  'entre otros'],
                 'correcta': 'E'},
                {'pregunta': 'En «El profesor viajará muy pronto», el '
                             'sustantivo «profesor» funciona como núcleo de:',
                 'alternativas': ['El vocativo',
                                  'El complemento directo',
                                  'La aposición',
                                  'El complemento agente',
                                  'El sujeto'],
                 'correcta': 'E'},
                {'pregunta': 'En «Señorita, aquí tiene su cuaderno», '
                             '«Señorita» funciona como núcleo del:',
                 'alternativas': ['Sujeto',
                                  'Complemento indirecto',
                                  'Vocativo',
                                  'Atributo',
                                  'Complemento directo'],
                 'correcta': 'C'},
                {'pregunta': 'En «Ricardo Palma, el bibliotecario mendigo, '
                             'escribió Tradiciones peruanas», «el '
                             'bibliotecario mendigo» es núcleo de:',
                 'alternativas': ['El complemento circunstancial',
                                  'El atributo',
                                  'La aposición',
                                  'El vocativo',
                                  'El sujeto'],
                 'correcta': 'C'},
                {'pregunta': 'En «El cuento fue leído por el niño», «el '
                             'niño» funciona como núcleo del complemento:',
                 'alternativas': ['Indirecto',
                                  'Circunstancial',
                                  'De régimen',
                                  'Directo',
                                  'Agente'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que nombran a los seres '
                             'diferenciándolos de los demás de su especie '
                             'son los sustantivos:',
                 'alternativas': ['Propios',
                                  'Colectivos',
                                  'Comunes',
                                  'Contables',
                                  'Abstractos'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos propios, ortográficamente, se '
                             'escriben con:',
                 'alternativas': ['Cursiva obligatoria',
                                  'Comillas siempre',
                                  'Guion inicial',
                                  'Minúscula inicial',
                                  'Mayúscula inicial'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que nombran a todos los seres '
                             'de una clase son los sustantivos:',
                 'alternativas': ['Propios',
                                  'Contables',
                                  'Colectivos exclusivos',
                                  'Individuales exclusivos',
                                  'Comunes'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que designan entidades que se '
                             'pueden contar son los sustantivos:',
                 'alternativas': ['Abstractos',
                                  'Contables',
                                  'No contables',
                                  'Propios',
                                  'Colectivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que denotan magnitudes o '
                             'sustancias, como «un poco de café», son los '
                             'sustantivos:',
                 'alternativas': ['Contables',
                                  'Propios',
                                  'Individuales',
                                  'Colectivos',
                                  'No contables'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que nombran seres percibidos '
                             'por los sentidos son los sustantivos:',
                 'alternativas': ['Colectivos',
                                  'Abstractos',
                                  'No contables',
                                  'Comunes exclusivos',
                                  'Concretos'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que se conocen mediante un '
                             'proceso mental de abstracción son los '
                             'sustantivos:',
                 'alternativas': ['Contables',
                                  'Propios exclusivos',
                                  'Individuales',
                                  'Abstractos',
                                  'Concretos'],
                 'correcta': 'D'},
                {'pregunta': '«Hermosura», «paz» y «ambición» son ejemplos '
                             'de sustantivos:',
                 'alternativas': ['Colectivos',
                                  'Contables',
                                  'Propios',
                                  'Abstractos',
                                  'Concretos'],
                 'correcta': 'D'},
                {'pregunta': '«Cóndor», «árbol» y «lapicero» son ejemplos de '
                             'sustantivos:',
                 'alternativas': ['Concretos',
                                  'Abstractos',
                                  'Colectivos exclusivos',
                                  'Propios',
                                  'No contables'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos que nombran a un solo ser son '
                             'los sustantivos:',
                 'alternativas': ['No contables',
                                  'Propios exclusivos',
                                  'Colectivos',
                                  'Individuales',
                                  'Abstractos'],
                 'correcta': 'D'},
                {'pregunta': '«Arboleda», «enjambre» y «cardumen» son '
                             'ejemplos de sustantivos:',
                 'alternativas': ['No contables exclusivos',
                                  'Propios',
                                  'Colectivos',
                                  'Abstractos',
                                  'Individuales'],
                 'correcta': 'C'},
                {'pregunta': 'Los sustantivos colectivos, en número '
                             'singular, designan:',
                 'alternativas': ['Un conjunto de seres',
                                  'Un solo ser',
                                  'Una cualidad abstracta',
                                  'Una relación lógica',
                                  'Una acción'],
                 'correcta': 'A'},
                {'pregunta': 'En «Aquellos jóvenes parecen buenos '
                             'profesionales», «profesionales» funciona como '
                             'núcleo de:',
                 'alternativas': ['La aposición',
                                  'El sujeto',
                                  'El complemento agente',
                                  'El vocativo',
                                  'El atributo'],
                 'correcta': 'E'}]},
 {'num': 9,
  'titulo': 'El Pronombre',
  'secciones': [{'titulo': '9.1 CRITERIOS PARA DEFINIR EL PRONOMBRE',
                 'items': ['Según el criterio {semántico}, el pronombre '
                           'indica la existencia de seres sin {nombrarlos} '
                           'directamente.',
                           'El pronombre es una palabra {no-connotativa}, '
                           'porque no señala cualidades o características '
                           'del sustantivo.',
                           'El pronombre es una palabra {no descriptiva}, '
                           'porque señala al ser sin conceptuarlo.',
                           'El pronombre tiene significación {ocasional}: '
                           'fuera de contexto, palabras como «ella» o «tú» '
                           'carecen de significado fijo.',
                           'Cuando el pronombre se carga de significado '
                           'dentro de un contexto, adquiere un valor '
                           '{referencial}.',
                           'Según el criterio {morfológico}, el pronombre es '
                           'una palabra variable que expresa género, número '
                           'y {persona}.',
                           'Según el criterio {sintáctico}, el pronombre '
                           'puede funcionar como sustantivo, {adjetivo} o '
                           'adverbio.']},
                {'titulo': '9.2 CASOS DEL PRONOMBRE PERSONAL',
                 'items': ['El caso {nominativo} o recto corresponde a '
                           'pronombres como «yo», «tú», «él», que funcionan '
                           'como sujeto.',
                           'El caso {acusativo}, de complemento directo, '
                           'corresponde a pronombres como «me», «te», «lo», '
                           '«la».',
                           'El caso {dativo}, de complemento indirecto, '
                           'corresponde a pronombres como «me», «te», «le», '
                           '«les».',
                           'El caso {preposicional} corresponde a pronombres '
                           'como «mí», «ti», «él», usados después de una '
                           'preposición.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, el pronombre indica '
                           'la existencia de seres {Sin nombrarlos '
                           'directamente}.',
                           'El pronombre es descrito como una palabra '
                           '{No-connotativa}.',
                           'El pronombre es una palabra no descriptiva '
                           'porque {Señala al ser sin conceptuarlo}.',
                           'Que el pronombre tenga significación ocasional '
                           'significa que {Fuera de contexto carece de '
                           'significado definido}.',
                           'Según el criterio morfológico, el pronombre es '
                           'una palabra {Variable, con accidentes de género, '
                           'número y persona}.',
                           'Según el criterio sintáctico, el pronombre puede '
                           'funcionar como sustantivo, adjetivo o '
                           '{Adverbio}.',
                           'El caso del pronombre que funciona como sujeto '
                           'se llama caso {Nominativo o recto}.',
                           'El caso del pronombre que funciona como '
                           'complemento directo se llama caso {Acusativo}.',
                           'El caso del pronombre que funciona como '
                           'complemento indirecto se llama caso {Dativo}.',
                           'El caso del pronombre usado después de una '
                           'preposición se llama caso {Preposicional}.',
                           'En «Yo no lo sabía», el pronombre «yo» está en '
                           'caso {Nominativo}.',
                           'En «No me entienden», el pronombre «me» funciona '
                           'en caso {Acusativo}.',
                           'En «Me duelen las muelas», el pronombre «me» '
                           'funciona en caso {Dativo}.',
                           'En «Confiaba en él», el pronombre «él» está en '
                           'caso {Preposicional}.',
                           'En «Ese se cayó anoche», el pronombre «ese» '
                           'ejemplifica que el pronombre es una palabra {No '
                           'descriptiva}.',
                           'En «Esas niñas son más honestas que aquellas», '
                           'el primer pronombre «esas» funciona como '
                           '{Adjetivo}.',
                           'En «Todos estudiaban aquí», el pronombre «todos» '
                           'funciona como {Sustantivo (núcleo del sujeto)}.',
                           'Los pronombres «ella», «tú», «ellos» aislados, '
                           'sin contexto, tienen significado {Vacío o '
                           'indefinido}.',
                           'El pronombre, a diferencia del sustantivo, se '
                           'caracteriza principalmente por {Señalar al ser '
                           'sin nombrarlo con precisión}.']}],
  'cuadros': [{'titulo': '9.2 CASOS DEL PRONOMBRE PERSONAL (1ª PERSONA)',
               'encabezados': ['Caso', 'Pronombre', 'Función'],
               'filas': [['{Nominativo}', 'Yo, nosotros', '{Sujeto}'],
                         ['{Acusativo}', 'Me, nos', 'Complemento {directo}'],
                         ['{Dativo}', 'Me, nos', 'Complemento {indirecto}'],
                         ['{Preposicional}',
                          'Mí, conmigo',
                          'Tras {preposición}']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el pronombre '
                             'indica la existencia de seres:',
                 'alternativas': ['Con cualidades específicas',
                                  'Solo en plural',
                                  'Solo en femenino',
                                  'Nombrándolos con precisión',
                                  'Sin nombrarlos directamente'],
                 'correcta': 'E'},
                {'pregunta': 'El pronombre es descrito como una palabra:',
                 'alternativas': ['Connotativa',
                                  'Siempre concreta',
                                  'Invariable',
                                  'Exclusivamente descriptiva',
                                  'No-connotativa'],
                 'correcta': 'E'},
                {'pregunta': 'El pronombre es una palabra no descriptiva '
                             'porque:',
                 'alternativas': ['Solo se usa en plural',
                                  'Señala cualidades del sustantivo',
                                  'Tiene significado fijo siempre',
                                  'Nombra directamente al ser',
                                  'Señala al ser sin conceptuarlo'],
                 'correcta': 'E'},
                {'pregunta': 'Que el pronombre tenga significación ocasional '
                             'significa que:',
                 'alternativas': ['Es sinónimo de un sustantivo fijo',
                                  'Fuera de contexto carece de significado '
                                  'definido',
                                  'Solo funciona en singular',
                                  'Siempre tiene el mismo significado',
                                  'Nunca tiene significado'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el pronombre se carga de significado '
                             'dentro de un contexto, adquiere un valor:',
                 'alternativas': ['Ortográfico',
                                  'Fonológico',
                                  'Morfológico exclusivo',
                                  'Referencial',
                                  'Descriptivo'],
                 'correcta': 'D'},
                {'pregunta': 'Según el criterio morfológico, el pronombre es '
                             'una palabra:',
                 'alternativas': ['Variable, con accidentes de género, '
                                  'número y persona',
                                  'Invariable',
                                  'Exclusivamente masculina',
                                  'Sin flexión alguna',
                                  'Solo singular'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio sintáctico, el pronombre '
                             'puede funcionar como sustantivo, adjetivo o:',
                 'alternativas': ['Artículo',
                                  'Interjección',
                                  'Preposición',
                                  'Conjunción',
                                  'Adverbio'],
                 'correcta': 'E'},
                {'pregunta': 'El caso del pronombre que funciona como sujeto '
                             'se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Nominativo o recto',
                                  'Vocativo',
                                  'Preposicional',
                                  'Dativo'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento directo se llama caso:',
                 'alternativas': ['Nominativo',
                                  'Recto',
                                  'Dativo',
                                  'Acusativo',
                                  'Preposicional'],
                 'correcta': 'D'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento indirecto se llama caso:',
                 'alternativas': ['Vocativo',
                                  'Dativo',
                                  'Acusativo',
                                  'Preposicional',
                                  'Nominativo'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre usado después de una '
                             'preposición se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Dativo',
                                  'Nominativo',
                                  'Preposicional',
                                  'Recto'],
                 'correcta': 'D'},
                {'pregunta': 'En «Yo no lo sabía», el pronombre «yo» está en '
                             'caso:',
                 'alternativas': ['Vocativo',
                                  'Nominativo',
                                  'Dativo',
                                  'Preposicional',
                                  'Acusativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «No me entienden», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Preposicional',
                                  'Nominativo',
                                  'Acusativo',
                                  'Recto',
                                  'Vocativo'],
                 'correcta': 'C'},
                {'pregunta': 'En «Me duelen las muelas», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Dativo',
                                  'Recto',
                                  'Acusativo',
                                  'Preposicional',
                                  'Nominativo'],
                 'correcta': 'A'},
                {'pregunta': 'En «Confiaba en él», el pronombre «él» está en '
                             'caso:',
                 'alternativas': ['Acusativo',
                                  'Preposicional',
                                  'Recto',
                                  'Nominativo',
                                  'Dativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Ese se cayó anoche», el pronombre «ese» '
                             'ejemplifica que el pronombre es una palabra:',
                 'alternativas': ['No descriptiva',
                                  'Exclusivamente adjetiva',
                                  'Connotativa',
                                  'Fija en significado',
                                  'Descriptiva'],
                 'correcta': 'A'},
                {'pregunta': 'En «Esas niñas son más honestas que aquellas», '
                             'el primer pronombre «esas» funciona como:',
                 'alternativas': ['Conjunción',
                                  'Preposición',
                                  'Adverbio',
                                  'Sustantivo',
                                  'Adjetivo'],
                 'correcta': 'E'},
                {'pregunta': 'En «Todos estudiaban aquí», el pronombre '
                             '«todos» funciona como:',
                 'alternativas': ['Vocativo',
                                  'Preposición',
                                  'Sustantivo (núcleo del sujeto)',
                                  'Adjetivo',
                                  'Adverbio'],
                 'correcta': 'C'},
                {'pregunta': 'Los pronombres «ella», «tú», «ellos» aislados, '
                             'sin contexto, tienen significado:',
                 'alternativas': ['Siempre concreto',
                                  'Exclusivamente plural',
                                  'Fijo y estable',
                                  'Vacío o indefinido',
                                  'Descriptivo detallado'],
                 'correcta': 'D'},
                {'pregunta': 'El pronombre, a diferencia del sustantivo, se '
                             'caracteriza principalmente por:',
                 'alternativas': ['Tener siempre género femenino',
                                  'No poder funcionar como sujeto',
                                  'Ser siempre invariable',
                                  'Señalar al ser sin nombrarlo con '
                                  'precisión',
                                  'Nombrar directamente al ser con sus '
                                  'cualidades'],
                 'correcta': 'D'}]},
 {'num': 10,
  'titulo': 'El Adjetivo',
  'secciones': [{'titulo': '10.1 CRITERIOS PARA DEFINIR EL ADJETIVO',
                 'items': ['Según el criterio {semántico}, el adjetivo '
                           'agrega información o {califica} al sustantivo, y '
                           'también lo {determina}.',
                           'Según el criterio {morfológico}, el adjetivo es '
                           'una palabra variable con morfemas de {género} y '
                           'número.',
                           'Según el criterio {sintáctico}, la función '
                           'principal del adjetivo es modificar directamente '
                           'al {sustantivo}, como M.D.',
                           'El adjetivo también puede funcionar como núcleo '
                           'del {predicativo} o del {atributo} del verbo '
                           'copulativo.']},
                {'titulo': '10.2 ADJETIVOS CALIFICATIVOS',
                 'items': ['Los adjetivos {calificativos} expresan '
                           'cualidades o estados del sustantivo al cual '
                           'modifican.',
                           'El adjetivo {especificativo} o restrictivo '
                           'precisa de qué sustantivo se trata y puede '
                           'restringir su extensión.',
                           'El adjetivo {explicativo} o no restrictivo '
                           'aparece entre pausas, va antepuesto y no tiene '
                           'carga {excluyente}.',
                           'El adjetivo {epíteto} señala una cualidad propia '
                           'del sustantivo; antepuesto tiene propósito '
                           '{poético}.']},
                {'titulo': '10.3 ADJETIVOS GENTILICIOS',
                 'items': ['Los adjetivos {gentilicios} califican al '
                           'sustantivo por su lugar de {origen} o '
                           'procedencia.',
                           'El sufijo {-eño/-eña} forma gentilicios como '
                           '«limeña»; el sufijo {-ense} forma gentilicios '
                           'como «bonaerense».',
                           'El sufijo {-és/-esa} forma gentilicios como '
                           '«cordobés»; el sufijo {-ano/-ana} forma '
                           'gentilicios como «italiana».']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, el adjetivo agrega '
                           'información o {Califica al sustantivo}.',
                           'Según el criterio morfológico, el adjetivo es '
                           'una palabra {Variable, con género y número}.',
                           'La función principal del adjetivo, según el '
                           'criterio sintáctico, es modificar directamente '
                           '{Al sustantivo}.',
                           'Además de modificar al sustantivo, el adjetivo '
                           'puede funcionar como núcleo del {Predicativo o '
                           'atributo}.',
                           'Los adjetivos que expresan cualidades o estados '
                           'del sustantivo son los adjetivos '
                           '{Calificativos}.',
                           'El adjetivo que precisa de qué sustantivo se '
                           'trata y puede restringir su extensión es el '
                           'adjetivo {Especificativo o restrictivo}.',
                           'El adjetivo que aparece entre pausas y no tiene '
                           'carga excluyente es el adjetivo {Explicativo o '
                           'no restrictivo}.',
                           'El adjetivo que señala una cualidad propia del '
                           'sustantivo, con valor poético cuando va '
                           'antepuesto, es el {Explicativo}.',
                           'En «blanca nieve», el adjetivo «blanca» es un '
                           'ejemplo de adjetivo {Epíteto}.',
                           'En «Los jugadores, contentos con el resultado, '
                           'lo celebraron», el adjetivo «contentos» es '
                           '{Explicativo}.',
                           'En «gatos negros», el adjetivo «negros» es un '
                           'ejemplo de adjetivo {Especificativo}.',
                           'Los adjetivos gentilicios califican al '
                           'sustantivo por su {Lugar de origen o '
                           'procedencia}.',
                           'El sufijo «-eño/-eña» forma gentilicios como '
                           '{Limeña}.',
                           'El sufijo «-ense» forma gentilicios como '
                           '{Bonaerense}.',
                           'El sufijo «-és/-esa» forma gentilicios como '
                           '{Cordobés}.',
                           'En «El joven austriaco ganó un premio», el '
                           'adjetivo «austriaco» es un adjetivo '
                           '{Gentilicio}.',
                           'En «María llegó muy cansada», el adjetivo '
                           '«cansada» funciona como núcleo del '
                           '{Predicativo}.',
                           'En «La población está asustada», el adjetivo '
                           '«asustada» funciona como {Atributo}.',
                           'El adjetivo epíteto, en posición pospuesta, '
                           'suele tener una intención {Coloquial}.',
                           'En «lámpara portátil», el adjetivo «portátil» '
                           'cumple una función {Especificativa}.']}],
  'cuadros': [{'titulo': '10.2 CLASES DE ADJETIVO CALIFICATIVO',
               'encabezados': ['Clase', 'Característica'],
               'filas': [['{Especificativo}', '{Precisa} y puede restringir'],
                         ['{Explicativo}',
                          'Entre pausas, sin carga {excluyente}'],
                         ['{Epíteto}', 'Cualidad {propia}, valor poético']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el adjetivo '
                             'agrega información o:',
                 'alternativas': ['Reemplaza al verbo',
                                  'Califica al sustantivo',
                                  'Elimina el sustantivo',
                                  'Sustituye al sustantivo',
                                  'Actúa como preposición'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el adjetivo es '
                             'una palabra:',
                 'alternativas': ['Sin flexión alguna',
                                  'Solo singular',
                                  'Solo masculina',
                                  'Invariable',
                                  'Variable, con género y número'],
                 'correcta': 'E'},
                {'pregunta': 'La función principal del adjetivo, según el '
                             'criterio sintáctico, es modificar '
                             'directamente:',
                 'alternativas': ['Al verbo',
                                  'A la conjunción',
                                  'Al sustantivo',
                                  'Al adverbio',
                                  'A la preposición'],
                 'correcta': 'C'},
                {'pregunta': 'Además de modificar al sustantivo, el adjetivo '
                             'puede funcionar como núcleo del:',
                 'alternativas': ['Complemento directo únicamente',
                                  'Complemento agente',
                                  'Predicativo o atributo',
                                  'Sujeto exclusivamente',
                                  'Vocativo'],
                 'correcta': 'C'},
                {'pregunta': 'Los adjetivos que expresan cualidades o '
                             'estados del sustantivo son los adjetivos:',
                 'alternativas': ['Numerales',
                                  'Gentilicios',
                                  'Determinativos exclusivos',
                                  'Posesivos',
                                  'Calificativos'],
                 'correcta': 'E'},
                {'pregunta': 'El adjetivo que precisa de qué sustantivo se '
                             'trata y puede restringir su extensión es el '
                             'adjetivo:',
                 'alternativas': ['Especificativo o restrictivo',
                                  'Posesivo',
                                  'Epíteto',
                                  'Explicativo',
                                  'Gentilicio'],
                 'correcta': 'A'},
                {'pregunta': 'El adjetivo que aparece entre pausas y no '
                             'tiene carga excluyente es el adjetivo:',
                 'alternativas': ['Especificativo',
                                  'Explicativo o no restrictivo',
                                  'Gentilicio',
                                  'Numeral',
                                  'Epíteto'],
                 'correcta': 'B'},
                {'pregunta': 'El adjetivo que señala una cualidad propia del '
                             'sustantivo, con valor poético cuando va '
                             'antepuesto, es el:',
                 'alternativas': ['Explicativo',
                                  'Determinativo',
                                  'Especificativo',
                                  'Epíteto',
                                  'Gentilicio'],
                 'correcta': 'A'},
                {'pregunta': 'En «blanca nieve», el adjetivo «blanca» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Numeral',
                                  'Gentilicio',
                                  'Explicativo',
                                  'Especificativo',
                                  'Epíteto'],
                 'correcta': 'E'},
                {'pregunta': 'En «Los jugadores, contentos con el resultado, '
                             'lo celebraron», el adjetivo «contentos» es:',
                 'alternativas': ['Especificativo',
                                  'Posesivo',
                                  'Explicativo',
                                  'Gentilicio',
                                  'Epíteto'],
                 'correcta': 'C'},
                {'pregunta': 'En «gatos negros», el adjetivo «negros» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Explicativo',
                                  'Numeral',
                                  'Epíteto exclusivo',
                                  'Especificativo',
                                  'Gentilicio'],
                 'correcta': 'D'},
                {'pregunta': 'Los adjetivos gentilicios califican al '
                             'sustantivo por su:',
                 'alternativas': ['Cantidad',
                                  'Forma',
                                  'Color',
                                  'Tamaño',
                                  'Lugar de origen o procedencia'],
                 'correcta': 'E'},
                {'pregunta': 'El sufijo «-eño/-eña» forma gentilicios como:',
                 'alternativas': ['Cordobés',
                                  'Chileno',
                                  'Bonaerense',
                                  'Limeña',
                                  'Italiana'],
                 'correcta': 'D'},
                {'pregunta': 'El sufijo «-ense» forma gentilicios como:',
                 'alternativas': ['Limeña',
                                  'Habanera',
                                  'Cordobés',
                                  'Italiana',
                                  'Bonaerense'],
                 'correcta': 'E'},
                {'pregunta': 'El sufijo «-és/-esa» forma gentilicios como:',
                 'alternativas': ['Chileno',
                                  'Limeña',
                                  'Europeo',
                                  'Cordobés',
                                  'Bonaerense'],
                 'correcta': 'D'},
                {'pregunta': 'En «El joven austriaco ganó un premio», el '
                             'adjetivo «austriaco» es un adjetivo:',
                 'alternativas': ['Calificativo especificativo',
                                  'Epíteto',
                                  'Explicativo',
                                  'Posesivo',
                                  'Gentilicio'],
                 'correcta': 'E'},
                {'pregunta': 'En «María llegó muy cansada», el adjetivo '
                             '«cansada» funciona como núcleo del:',
                 'alternativas': ['Complemento indirecto',
                                  'Vocativo',
                                  'Predicativo',
                                  'Complemento directo',
                                  'Sujeto'],
                 'correcta': 'C'},
                {'pregunta': 'En «La población está asustada», el adjetivo '
                             '«asustada» funciona como:',
                 'alternativas': ['Complemento directo',
                                  'Aposición',
                                  'Vocativo',
                                  'Sujeto',
                                  'Atributo'],
                 'correcta': 'E'},
                {'pregunta': 'El adjetivo epíteto, en posición pospuesta, '
                             'suele tener una intención:',
                 'alternativas': ['Poética exclusiva',
                                  'Legal',
                                  'Científica',
                                  'Coloquial',
                                  'Matemática'],
                 'correcta': 'D'},
                {'pregunta': 'En «lámpara portátil», el adjetivo «portátil» '
                             'cumple una función:',
                 'alternativas': ['Especificativa',
                                  'Gentilicia',
                                  'Numeral',
                                  'Epíteto',
                                  'Explicativa'],
                 'correcta': 'A'}]},
 {'num': 11,
  'titulo': 'El Artículo y el Adverbio',
  'secciones': [{'titulo': '11.1 CRITERIOS DEL ARTÍCULO',
                 'items': ['Según el criterio {semántico}, el artículo '
                           'carece de significado lexical propio, pero posee '
                           'significado {gramatical}.',
                           'El artículo siempre {precede} al sustantivo.',
                           'Según el criterio {morfológico}, el artículo es '
                           'una palabra variable que concuerda en género y '
                           '{número} con el sustantivo.',
                           'Según el criterio {sintáctico}, el artículo '
                           'funciona como modificador directo y como '
                           '{sustantivador} universal.']},
                {'titulo': '11.2 CLASIFICACIÓN DEL ARTÍCULO',
                 'items': ['El artículo {determinado}, o definido, hace '
                           'referencia a un sustantivo conocido: el, la, '
                           'los, {las}.',
                           'El artículo {indeterminado}, o indefinido, hace '
                           'referencia a seres no conocidos: un, una, unos, '
                           '{unas}.',
                           'El artículo {neutro} «lo» sirve para sustantivar '
                           'a los adjetivos, convirtiéndolos en sustantivos '
                           '{abstractos}.']},
                {'titulo': '11.3 LA CONTRACCIÓN DEL ARTÍCULO',
                 'items': ['El único artículo que puede contraerse es {el}, '
                           'cuando se une a las preposiciones a o {de}.',
                           'La preposición «a» más «el» forma la contracción '
                           '{al}; la preposición «de» más «el» forma la '
                           'contracción {del}.',
                           'Las contracciones se usan solo ante sustantivos '
                           '{comunes}.',
                           'Si el artículo forma parte de un {topónimo}, '
                           'como «El Salvador», no procede la contracción.']},
                {'titulo': '11.4 EL ADVERBIO',
                 'items': ['El adverbio es una palabra {invariable} que '
                           'modifica al verbo, al adjetivo o a otro '
                           'adverbio.',
                           'Los adverbios se clasifican según su significado '
                           'en adverbios de {lugar}, tiempo, modo, cantidad, '
                           'afirmación, negación y duda.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, el artículo carece '
                           'de significado lexical pero posee significado '
                           '{Gramatical}.',
                           'El artículo, en su posición dentro de la '
                           'oración, siempre {Precede al sustantivo}.',
                           'Según el criterio morfológico, el artículo '
                           'concuerda con el sustantivo en {Género y '
                           'número}.',
                           'El artículo que hace referencia a un sustantivo '
                           'conocido por el hablante se llama artículo '
                           '{Determinado}.',
                           'El artículo que hace referencia a seres no '
                           'conocidos se llama artículo {Indeterminado}.',
                           'El artículo neutro del español es {Lo}.',
                           'El artículo neutro «lo» sirve para sustantivar '
                           '{Adjetivos}.',
                           'En «Lo bueno supervive a través del tiempo», «lo '
                           'bueno» funciona como un sustantivo {Abstracto}.',
                           'El único artículo que se puede contraer es {El}.',
                           'El artículo «el» se contrae con las '
                           'preposiciones «a» y {De}.',
                           'La contracción de «a» más «el» da como resultado '
                           '{Al}.',
                           'La contracción de «de» más «el» da como '
                           'resultado {Del}.',
                           'Las contracciones del artículo se usan solamente '
                           'ante sustantivos {Comunes}.',
                           'Si el artículo forma parte de un topónimo, como '
                           '«El Salvador», la contracción {No procede}.',
                           'En «Viajaremos a El Cairo», la ausencia de '
                           'contracción se debe a que {El artículo forma '
                           'parte del topónimo}.',
                           'El adverbio, en cuanto a su morfología, es una '
                           'palabra {Invariable}.',
                           'El adverbio puede modificar al verbo, al '
                           'adjetivo o {A otro adverbio}.',
                           'Los adverbios se clasifican, entre otras '
                           'categorías, en adverbios de lugar, tiempo y '
                           '{Modo}.',
                           'En «El ayer quedó en olvido», el artículo «el» '
                           'sustantiva a {Un adverbio temporal}.',
                           'En «Un día te entregaré unos regalos», los '
                           'artículos usados son de tipo {Indeterminado}.']}],
  'cuadros': [{'titulo': '11.2 CLASES DE ARTÍCULO',
               'encabezados': ['Clase', 'Masculino singular', 'Referencia'],
               'filas': [['{Determinado}', 'El', 'Sustantivo {conocido}'],
                         ['{Indeterminado}', 'Un', 'Ser {no} conocido'],
                         ['{Neutro}', 'Lo', 'Sustantiva {adjetivos}']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el artículo '
                             'carece de significado lexical pero posee '
                             'significado:',
                 'alternativas': ['Pragmático',
                                  'Ninguno',
                                  'Fonológico',
                                  'Morfológico exclusivo',
                                  'Gramatical'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo, en su posición dentro de la '
                             'oración, siempre:',
                 'alternativas': ['Aparece solo en plural',
                                  'Sigue al sustantivo',
                                  'Se ubica al final de la oración',
                                  'Reemplaza al verbo',
                                  'Precede al sustantivo'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio morfológico, el artículo '
                             'concuerda con el sustantivo en:',
                 'alternativas': ['Solo persona gramatical',
                                  'Modo verbal',
                                  'Género y número',
                                  'Solo tiempo verbal',
                                  'Aspecto verbal'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo que hace referencia a un '
                             'sustantivo conocido por el hablante se llama '
                             'artículo:',
                 'alternativas': ['Indeterminado',
                                  'Neutro',
                                  'Determinado',
                                  'Posesivo',
                                  'Demostrativo'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo que hace referencia a seres no '
                             'conocidos se llama artículo:',
                 'alternativas': ['Determinado',
                                  'Recto',
                                  'Indeterminado',
                                  'Definido',
                                  'Neutro'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo neutro del español es:',
                 'alternativas': ['Un', 'Lo', 'El', 'Una', 'La'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo neutro «lo» sirve para '
                             'sustantivar:',
                 'alternativas': ['Conjunciones',
                                  'Artículos',
                                  'Preposiciones',
                                  'Adjetivos',
                                  'Verbos'],
                 'correcta': 'D'},
                {'pregunta': 'En «Lo bueno supervive a través del tiempo», '
                             '«lo bueno» funciona como un sustantivo:',
                 'alternativas': ['Colectivo',
                                  'Contable',
                                  'Abstracto',
                                  'Propio',
                                  'Concreto'],
                 'correcta': 'C'},
                {'pregunta': 'El único artículo que se puede contraer es:',
                 'alternativas': ['Las', 'La', 'El', 'Los', 'Un'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo «el» se contrae con las '
                             'preposiciones «a» y:',
                 'alternativas': ['Por', 'De', 'Sin', 'Con', 'Para'],
                 'correcta': 'B'},
                {'pregunta': 'La contracción de «a» más «el» da como '
                             'resultado:',
                 'alternativas': ['Del', 'Al', 'Aal', 'A el siempre', 'Ael'],
                 'correcta': 'B'},
                {'pregunta': 'La contracción de «de» más «el» da como '
                             'resultado:',
                 'alternativas': ['Dle',
                                  'De el siempre',
                                  'Dell',
                                  'Al',
                                  'Del'],
                 'correcta': 'E'},
                {'pregunta': 'Las contracciones del artículo se usan '
                             'solamente ante sustantivos:',
                 'alternativas': ['Colectivos exclusivos',
                                  'Propios siempre',
                                  'Comunes',
                                  'Abstractos',
                                  'Contables únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'Si el artículo forma parte de un topónimo, '
                             'como «El Salvador», la contracción:',
                 'alternativas': ['Es obligatoria',
                                  'Depende del contexto oral',
                                  'No procede',
                                  'Es opcional siempre',
                                  'Se aplica solo por escrito'],
                 'correcta': 'C'},
                {'pregunta': 'En «Viajaremos a El Cairo», la ausencia de '
                             'contracción se debe a que:',
                 'alternativas': ['El artículo forma parte del topónimo',
                                  'Es un error ortográfico',
                                  'Es una excepción sin explicación',
                                  'El Cairo no es un lugar real',
                                  'La preposición no lo permite nunca'],
                 'correcta': 'A'},
                {'pregunta': 'El adverbio, en cuanto a su morfología, es una '
                             'palabra:',
                 'alternativas': ['Solo masculina',
                                  'Variable en género y número',
                                  'Con flexión verbal',
                                  'Solo plural',
                                  'Invariable'],
                 'correcta': 'E'},
                {'pregunta': 'El adverbio puede modificar al verbo, al '
                             'adjetivo o:',
                 'alternativas': ['Al sustantivo directamente',
                                  'Al pronombre exclusivamente',
                                  'A otro adverbio',
                                  'A la conjunción',
                                  'Al artículo'],
                 'correcta': 'C'},
                {'pregunta': 'Los adverbios se clasifican, entre otras '
                             'categorías, en adverbios de lugar, tiempo y:',
                 'alternativas': ['Persona',
                                  'Caso',
                                  'Número',
                                  'Género',
                                  'Modo'],
                 'correcta': 'E'},
                {'pregunta': 'En «El ayer quedó en olvido», el artículo «el» '
                             'sustantiva a:',
                 'alternativas': ['Un adjetivo',
                                  'Una conjunción',
                                  'Un adverbio temporal',
                                  'Un verbo',
                                  'Una preposición'],
                 'correcta': 'C'},
                {'pregunta': 'En «Un día te entregaré unos regalos», los '
                             'artículos usados son de tipo:',
                 'alternativas': ['Contraído',
                                  'Determinado',
                                  'Neutro',
                                  'Indeterminado',
                                  'Demostrativo'],
                 'correcta': 'D'}]},
 {'num': 12,
  'titulo': 'El Verbo',
  'secciones': [{'titulo': '12.1 CRITERIOS PARA DEFINIR EL VERBO',
                 'items': ['Según el criterio {semántico}, el verbo expresa '
                           'acción, inacción, pasión, {estado}, existencia y '
                           'transformación.',
                           'Según el criterio {morfológico}, el verbo es una '
                           'palabra variable con accidentes de número, '
                           'persona, tiempo, {modo} y aspecto.',
                           'Según el criterio {sintáctico}, el verbo '
                           'funciona como núcleo del {predicado} verbal.']},
                {'titulo': '12.2 VERBOS COPULATIVOS Y NO COPULATIVOS',
                 'items': ['Los verbos {copulativos} no manifiestan idea con '
                           'sentido pleno y sirven de nexo entre el sujeto y '
                           'su {atributo}: ser, estar, parecer.',
                           'Los verbos {no copulativos}, o predicativos, '
                           'expresan por sí solos idea con sentido pleno.']},
                {'titulo': '12.3 CLASES DE VERBOS NO COPULATIVOS',
                 'items': ['Los verbos {transitivos} expresan una acción que '
                           'transita del sujeto a un objeto, y tienen '
                           'complemento {directo}.',
                           'Los verbos {intransitivos} no tienen complemento '
                           'directo, sino circunstanciales o de régimen.',
                           'Los verbos {reflexivos} tienen una acción que se '
                           'refleja sobre el mismo sujeto; se comprueban con '
                           'el refuerzo «{mismo}».',
                           'Los verbos {cuasireflexivos} usan los pronombres '
                           'me, te, se como énfasis, sin representar '
                           '{transitividad}, y no aceptan el refuerzo '
                           '«mismo».',
                           'Los verbos {recíprocos} tienen sujeto plural con '
                           'acción mutua entre ellos, y aceptan el refuerzo '
                           '«{mutuamente}».']},
                {'titulo': '12.4 VERBOS IMPERSONALES',
                 'items': ['Los verbos {impersonales} son aquellos cuyo '
                           'sujeto se desconoce o no se precisa con '
                           'exactitud.',
                           'Los verbos que se refieren a fenómenos de la '
                           '{naturaleza}, como llover o nevar, son '
                           'impersonales.',
                           'Los verbos con el signo de impersonalidad '
                           'pronominal «{se}», como «se traspasa local», '
                           'también son impersonales.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, el verbo expresa '
                           'acción, inacción, pasión, estado y {Existencia}.',
                           'Según el criterio morfológico, el verbo presenta '
                           'accidentes de número, persona, tiempo, modo y '
                           '{Aspecto}.',
                           'Según el criterio sintáctico, el verbo funciona '
                           'como núcleo {Del predicado verbal}.',
                           'Los verbos que sirven de nexo entre el sujeto y '
                           'su atributo se llaman verbos {Copulativos}.',
                           'Un ejemplo de verbo copulativo es {Ser}.',
                           'Los verbos que expresan por sí solos una idea '
                           'con sentido pleno se llaman verbos {No '
                           'copulativos o predicativos}.',
                           'Los verbos que tienen complemento directo se '
                           'llaman verbos {Transitivos}.',
                           'Los verbos que no tienen complemento directo se '
                           'llaman verbos {Intransitivos}.',
                           'Los verbos cuya acción recae sobre el mismo '
                           'sujeto que la realiza se llaman verbos '
                           '{Reflexivos}.',
                           'El carácter reflexivo de un verbo se comprueba '
                           'añadiendo el refuerzo {«Mismo(a)»}.',
                           'Los verbos que usan pronombres como énfasis sin '
                           'representar transitividad se llaman verbos '
                           '{Cuasireflexivos}.',
                           'Los verbos con sujeto plural que ejercen una '
                           'acción mutua entre ellos se llaman verbos '
                           '{Recíprocos}.',
                           'El carácter recíproco de un verbo se comprueba '
                           'con el refuerzo {«Mutuamente» o '
                           '«recíprocamente»}.',
                           'Los verbos cuyo sujeto se desconoce o no se '
                           'precisa se llaman verbos {Impersonales}.',
                           'En «Yo me caigo», a diferencia de «yo caigo», el '
                           'pronombre «me» {Da solo énfasis, sin representar '
                           'transitividad}.',
                           'Los verbos «ser», «estar» y «parecer» pertenecen '
                           'a la clase de verbos {Copulativos}.']}],
  'cuadros': [{'titulo': '12.3 CLASES DE VERBOS SEGÚN LA TRANSITIVIDAD',
               'encabezados': ['Clase', 'Característica'],
               'filas': [['{Transitivo}', 'Tiene complemento {directo}'],
                         ['{Intransitivo}', 'No tiene complemento {directo}'],
                         ['{Reflexivo}',
                          'La acción recae en el mismo {sujeto}'],
                         ['{Recíproco}',
                          'Acción {mutua} entre sujetos plurales']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el verbo expresa '
                             'acción, inacción, pasión, estado y:',
                 'alternativas': ['Solo lugar',
                                  'Solo posesión',
                                  'Solo cantidad',
                                  'Solo cualidad',
                                  'Existencia'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio morfológico, el verbo '
                             'presenta accidentes de número, persona, '
                             'tiempo, modo y:',
                 'alternativas': ['Especie',
                                  'Grado',
                                  'Aspecto',
                                  'Caso',
                                  'Género'],
                 'correcta': 'C'},
                {'pregunta': 'Según el criterio sintáctico, el verbo '
                             'funciona como núcleo:',
                 'alternativas': ['Del sujeto',
                                  'Del complemento agente exclusivo',
                                  'Del predicado verbal',
                                  'Del vocativo',
                                  'De la aposición'],
                 'correcta': 'C'},
                {'pregunta': 'Los verbos que sirven de nexo entre el sujeto '
                             'y su atributo se llaman verbos:',
                 'alternativas': ['Reflexivos',
                                  'Transitivos',
                                  'Recíprocos',
                                  'Copulativos',
                                  'Impersonales'],
                 'correcta': 'D'},
                {'pregunta': 'Un ejemplo de verbo copulativo es:',
                 'alternativas': ['Comer',
                                  'Ser',
                                  'Escribir',
                                  'Saltar',
                                  'Correr'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que expresan por sí solos una idea '
                             'con sentido pleno se llaman verbos:',
                 'alternativas': ['Semicopulativos únicamente',
                                  'Auxiliares',
                                  'Copulativos',
                                  'Impersonales exclusivos',
                                  'No copulativos o predicativos'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos que tienen complemento directo se '
                             'llaman verbos:',
                 'alternativas': ['Copulativos',
                                  'Intransitivos',
                                  'Impersonales',
                                  'Transitivos',
                                  'Recíprocos exclusivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los verbos que no tienen complemento directo '
                             'se llaman verbos:',
                 'alternativas': ['Recíprocos',
                                  'Reflexivos exclusivos',
                                  'Intransitivos',
                                  'Transitivos',
                                  'Copulativos'],
                 'correcta': 'C'},
                {'pregunta': 'Los verbos cuya acción recae sobre el mismo '
                             'sujeto que la realiza se llaman verbos:',
                 'alternativas': ['Recíprocos',
                                  'Reflexivos',
                                  'Impersonales',
                                  'Transitivos exclusivos',
                                  'Copulativos'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter reflexivo de un verbo se comprueba '
                             'añadiendo el refuerzo:',
                 'alternativas': ['«Mutuamente»',
                                  '«Uno a otro»',
                                  '«Entre sí»',
                                  '«Recíprocamente»',
                                  '«Mismo(a)»'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos que usan pronombres como énfasis '
                             'sin representar transitividad se llaman '
                             'verbos:',
                 'alternativas': ['Transitivos',
                                  'Recíprocos',
                                  'Reflexivos',
                                  'Copulativos',
                                  'Cuasireflexivos'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos cuasireflexivos, a diferencia de '
                             'los reflexivos, NO aceptan el refuerzo:',
                 'alternativas': ['«Mutuamente»',
                                  '«Entre todos»',
                                  '«Recíprocamente»',
                                  '«Mismo(a)»',
                                  'Ninguno de los anteriores'],
                 'correcta': 'D'},
                {'pregunta': 'Los verbos con sujeto plural que ejercen una '
                             'acción mutua entre ellos se llaman verbos:',
                 'alternativas': ['Cuasireflexivos',
                                  'Impersonales',
                                  'Recíprocos',
                                  'Reflexivos',
                                  'Transitivos'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter recíproco de un verbo se comprueba '
                             'con el refuerzo:',
                 'alternativas': ['«Exclusivamente»',
                                  '«A sí mismo»',
                                  '«Mismo(a)»',
                                  '«Solamente»',
                                  '«Mutuamente» o «recíprocamente»'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos cuyo sujeto se desconoce o no se '
                             'precisa se llaman verbos:',
                 'alternativas': ['Impersonales',
                                  'Transitivos',
                                  'Copulativos',
                                  'Recíprocos',
                                  'Reflexivos'],
                 'correcta': 'A'},
                {'pregunta': '«Llovió en Cusco» es un ejemplo de verbo '
                             'impersonal referido a:',
                 'alternativas': ['Un fenómeno de la naturaleza',
                                  'Un verbo copulativo',
                                  'Una acción transitiva',
                                  'Una acción recíproca',
                                  'Un fenómeno social'],
                 'correcta': 'A'},
                {'pregunta': '«Se traspasa local comercial» ejemplifica un '
                             'verbo impersonal con el signo:',
                 'alternativas': ['De impersonalidad pronominal «se»',
                                  'De reflexividad',
                                  'De reciprocidad',
                                  'De pasiva refleja exclusiva',
                                  'De copulación'],
                 'correcta': 'A'},
                {'pregunta': '«Dicen que te vas a casar» ejemplifica un '
                             'verbo impersonal porque:',
                 'alternativas': ['El sujeto es plural y conocido',
                                  'No se conoce o no se quiere dar a conocer '
                                  'el sujeto',
                                  'Expresa un fenómeno natural',
                                  'Tiene complemento directo explícito',
                                  'Es un verbo copulativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Yo me caigo», a diferencia de «yo caigo», '
                             'el pronombre «me»:',
                 'alternativas': ['Sustituye al sujeto',
                                  'Da solo énfasis, sin representar '
                                  'transitividad',
                                  'Es un artículo neutro',
                                  'Funciona como complemento directo',
                                  'Indica reciprocidad'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos «ser», «estar» y «parecer» '
                             'pertenecen a la clase de verbos:',
                 'alternativas': ['Cuasireflexivos',
                                  'Impersonales',
                                  'Recíprocos',
                                  'Transitivos',
                                  'Copulativos'],
                 'correcta': 'E'}]},
 {'num': 13,
  'titulo': 'Conectores Lógico-Semánticos: La Preposición',
  'secciones': [{'titulo': '13.1 CRITERIOS DE LA PREPOSICIÓN',
                 'items': ['Según el criterio {semántico}, la preposición no '
                           'tiene significación por sí sola: su sentido es '
                           'de carácter {contextual}.',
                           'Según el criterio {morfológico}, la preposición '
                           'no sufre variaciones formales; carece de '
                           '{morfemas}.',
                           'Según el criterio {sintáctico}, la preposición '
                           'funciona como conectivo o nexo {subordinante}.',
                           'En el predicado, las preposiciones {por} y {de} '
                           'encabezan al agente, solo en voz pasiva.']},
                {'titulo': '13.2 USOS DE ALGUNAS PREPOSICIONES',
                 'items': ['La preposición «a» puede indicar dirección, '
                           'lugar, {tiempo} o modo.',
                           'La preposición «{ante}» significa «delante» o '
                           '«en presencia de».',
                           'La preposición «{bajo}» puede indicar situación '
                           'inferior o {subordinación}.',
                           'La preposición «{con}» puede indicar compañía, '
                           'unión, medio o {contenido}.',
                           'La preposición «{contra}» indica oposición o '
                           'ubicación.',
                           'La preposición «{de}» puede indicar posesión, '
                           'origen, material o {tema}.',
                           'La preposición «{desde}» indica principio de '
                           'tiempo o de {lugar}.',
                           'La preposición «{hacia}» indica dirección o una '
                           '{tendencia}.',
                           'La preposición «{hasta}» indica término de '
                           'lugar, acción o {tiempo}.',
                           'La preposición «{para}» indica finalidad, tiempo '
                           'o {dirección}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según el criterio semántico, la preposición '
                           'tiene un significado de carácter {Contextual}.',
                           'Según el criterio morfológico, la preposición se '
                           'caracteriza por {No sufrir variaciones '
                           'formales}.',
                           'Según el criterio sintáctico, la preposición '
                           'funciona como {Conectivo o nexo subordinante}.',
                           'En «La casa de Patricia fue construida por los '
                           'albañiles», la preposición que encabeza al '
                           'agente es {Por}.',
                           'Las preposiciones que encabezan al agente en voz '
                           'pasiva son {Por y de}.',
                           'La preposición «ante» significa {Delante de o en '
                           'presencia de}.',
                           'La preposición «bajo» puede indicar situación '
                           'inferior o {Subordinación}.',
                           'En «Con mucho estudio puedes conseguir la beca», '
                           'la preposición «con» indica {Medio para '
                           'conseguir algo}.',
                           'La preposición «contra» indica principalmente '
                           '{Oposición o ubicación}.',
                           'En «El departamento de mi amiga», la preposición '
                           '«de» indica {Posesión o pertenencia}.',
                           'En «Yo soy de Apurímac», la preposición «de» '
                           'indica {Origen o procedencia}.',
                           'La preposición «desde» indica principio de '
                           'tiempo o de {Lugar}.',
                           'La preposición «hacia» indica dirección o {Una '
                           'tendencia}.',
                           'La preposición «hasta» puede indicar término de '
                           'lugar, acción o {Tiempo}.',
                           'La preposición «para» puede indicar finalidad, '
                           'tiempo o {Dirección}.',
                           'En el sujeto, la preposición encabeza al '
                           '{Modificador indirecto}.',
                           'En «Estamos pasando bajo el puente», la '
                           'preposición «bajo» indica {Situación inferior}.',
                           'En «Dame un té con leche», la preposición «con» '
                           'indica {Contenido o unión de cosas}.',
                           'En «Este informe es para mi jefe», la '
                           'preposición «para» indica {Finalidad}.']}],
  'cuadros': [{'titulo': '13.2 LAS PREPOSICIONES DEL ESPAÑOL',
               'encabezados': ['Grupo', 'Preposiciones'],
               'filas': [['Básicas', 'a, ante, bajo, {con}, contra, de'],
                         ['Medias', 'desde, en, {entre}, hacia, hasta'],
                         ['Finales', '{para}, por, según, sin, sobre, tras'],
                         ['{Arcaicas}', 'so, cabe']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, la preposición '
                             'tiene un significado de carácter:',
                 'alternativas': ['Morfológico puro',
                                  'Inexistente',
                                  'Fonológico exclusivo',
                                  'Fijo y absoluto',
                                  'Contextual'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio morfológico, la preposición '
                             'se caracteriza por:',
                 'alternativas': ['Cambiar según el sujeto',
                                  'Concordar en persona',
                                  'No sufrir variaciones formales',
                                  'Tener flexión verbal',
                                  'Presentar variaciones de género y número'],
                 'correcta': 'C'},
                {'pregunta': 'Según el criterio sintáctico, la preposición '
                             'funciona como:',
                 'alternativas': ['Núcleo del sujeto',
                                  'Conectivo o nexo subordinante',
                                  'Sujeto de la oración',
                                  'Modificador indirecto exclusivo',
                                  'Núcleo del predicado'],
                 'correcta': 'B'},
                {'pregunta': 'En «La casa de Patricia fue construida por los '
                             'albañiles», la preposición que encabeza al '
                             'agente es:',
                 'alternativas': ['Por', 'Con', 'Para', 'De', 'En'],
                 'correcta': 'A'},
                {'pregunta': 'Las preposiciones que encabezan al agente en '
                             'voz pasiva son:',
                 'alternativas': ['Con y sin',
                                  'Por y de',
                                  'A y ante',
                                  'Para y desde',
                                  'Entre y hacia'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «ante» significa:',
                 'alternativas': ['Lejos de',
                                  'Junto a',
                                  'Después de',
                                  'Delante de o en presencia de',
                                  'Debajo de'],
                 'correcta': 'D'},
                {'pregunta': 'La preposición «bajo» puede indicar situación '
                             'inferior o:',
                 'alternativas': ['Finalidad',
                                  'Compañía',
                                  'Origen',
                                  'Subordinación',
                                  'Tiempo exclusivo'],
                 'correcta': 'D'},
                {'pregunta': 'En «Con mucho estudio puedes conseguir la '
                             'beca», la preposición «con» indica:',
                 'alternativas': ['Tiempo',
                                  'Oposición',
                                  'Contenido',
                                  'Compañía',
                                  'Medio para conseguir algo'],
                 'correcta': 'E'},
                {'pregunta': 'La preposición «contra» indica principalmente:',
                 'alternativas': ['Procedencia',
                                  'Compañía',
                                  'Finalidad',
                                  'Oposición o ubicación',
                                  'Posesión'],
                 'correcta': 'D'},
                {'pregunta': 'En «El departamento de mi amiga», la '
                             'preposición «de» indica:',
                 'alternativas': ['Posesión o pertenencia',
                                  'Tiempo',
                                  'Tema',
                                  'Origen',
                                  'Material'],
                 'correcta': 'A'},
                {'pregunta': 'En «Yo soy de Apurímac», la preposición «de» '
                             'indica:',
                 'alternativas': ['Tiempo',
                                  'Origen o procedencia',
                                  'Tema o asunto',
                                  'Posesión',
                                  'Material'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «desde» indica principio de '
                             'tiempo o de:',
                 'alternativas': ['Compañía',
                                  'Oposición',
                                  'Finalidad',
                                  'Lugar',
                                  'Modo'],
                 'correcta': 'D'},
                {'pregunta': 'La preposición «hacia» indica dirección o:',
                 'alternativas': ['Material',
                                  'Compañía',
                                  'Oposición',
                                  'Una tendencia',
                                  'Posesión'],
                 'correcta': 'D'},
                {'pregunta': 'La preposición «hasta» puede indicar término '
                             'de lugar, acción o:',
                 'alternativas': ['Material',
                                  'Compañía',
                                  'Tiempo',
                                  'Posesión',
                                  'Oposición'],
                 'correcta': 'C'},
                {'pregunta': 'La preposición «para» puede indicar finalidad, '
                             'tiempo o:',
                 'alternativas': ['Oposición',
                                  'Material',
                                  'Posesión exclusiva',
                                  'Compañía',
                                  'Dirección'],
                 'correcta': 'E'},
                {'pregunta': 'En el sujeto, la preposición encabeza al:',
                 'alternativas': ['Modificador indirecto',
                                  'Predicado nominal',
                                  'Vocativo',
                                  'Complemento directo',
                                  'Núcleo del sujeto'],
                 'correcta': 'A'},
                {'pregunta': '«So» y «cabe» son ejemplos de preposiciones:',
                 'alternativas': ['Arcaicas',
                                  'Modernas de uso frecuente',
                                  'Neológicas',
                                  'Extranjeras',
                                  'Compuestas'],
                 'correcta': 'A'},
                {'pregunta': 'En «Estamos pasando bajo el puente», la '
                             'preposición «bajo» indica:',
                 'alternativas': ['Situación inferior',
                                  'Finalidad',
                                  'Tiempo',
                                  'Compañía',
                                  'Subordinación'],
                 'correcta': 'A'},
                {'pregunta': 'En «Dame un té con leche», la preposición '
                             '«con» indica:',
                 'alternativas': ['Contenido o unión de cosas',
                                  'Tiempo',
                                  'Medio',
                                  'Compañía de personas',
                                  'Oposición'],
                 'correcta': 'A'},
                {'pregunta': 'En «Este informe es para mi jefe», la '
                             'preposición «para» indica:',
                 'alternativas': ['Tiempo',
                                  'Finalidad',
                                  'Origen',
                                  'Compañía',
                                  'Dirección'],
                 'correcta': 'B'}]},
 {'num': 14,
  'titulo': 'La Sintaxis y la Oración Gramatical',
  'secciones': [{'titulo': '14.1 CONCEPTO DE SINTAXIS Y SINTAGMA',
                 'items': ['«Sintaxis» es un término de origen {griego} que '
                           'significa «orden o {disposición}».',
                           'La sintaxis estudia las relaciones entre los '
                           'elementos de una frase y las {funciones} que '
                           'desempeña cada palabra.',
                           'La unidad básica de la sintaxis es el '
                           '{sintagma}.',
                           'El sintagma es una unidad sintáctica formada por '
                           'una o más palabras dotadas de {sentido} y valor '
                           '{funcional}.']},
                {'titulo': '14.2 EL SINTAGMA NOMINAL',
                 'items': ['El sintagma nominal (SN), o frase nominal, está '
                           'formado por un sustantivo u otra categoría '
                           '{sustantivada} que constituye su {núcleo}.',
                           'El {núcleo} del sintagma nominal siempre es un '
                           'sustantivo o palabra sustantivada.',
                           'Los {modificadores} del sintagma nominal '
                           'dependen del núcleo y giran alrededor de él.']},
                {'titulo': '14.3 MODIFICADORES DEL SINTAGMA NOMINAL',
                 'items': ['El {modificador directo} (MD) se une al núcleo '
                           'sin enlace; son artículos y {adjetivos}.',
                           'El {modificador indirecto} (MI) se une al núcleo '
                           'mediante preposiciones o conjunciones '
                           '{comparativas}.',
                           'La {aposición} (AP) tiene el mismo valor que el '
                           'núcleo y puede {conmutarse} con él.',
                           'La aposición {explicativa} se separa por comas y '
                           'es {sinónima} del núcleo, como en «Pachacútec, '
                           'el constructor de Machu Picchu».',
                           'La aposición {especificativa} singulariza al '
                           'nombre y no va entre {comas}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El término «sintaxis» es de origen griego y '
                           'significa {Orden o disposición}.',
                           'La sintaxis, como disciplina lingüística, '
                           'estudia las relaciones entre los elementos de '
                           'una frase y {Las funciones que desempeña cada '
                           'palabra}.',
                           'La unidad básica de la sintaxis es {El '
                           'sintagma}.',
                           'El sintagma se define como una unidad formada '
                           'por palabras dotadas de sentido y valor '
                           '{Funcional}.',
                           'El sintagma nominal también se conoce como '
                           '{Frase nominal o grupo nominal}.',
                           'El núcleo del sintagma nominal siempre es {Un '
                           'sustantivo o palabra sustantivada}.',
                           'Los modificadores del sintagma nominal dependen '
                           'de {El núcleo}.',
                           'El modificador que se une al núcleo del SN sin '
                           'ningún enlace se llama {Modificador directo}.',
                           'Las palabras que funcionan típicamente como '
                           'modificador directo son {Los artículos y '
                           'adjetivos}.',
                           'El modificador que se une al núcleo mediante '
                           'preposiciones se llama {Modificador indirecto}.',
                           'El modificador del SN que tiene el mismo valor '
                           'que el núcleo y puede conmutarse con él es {La '
                           'aposición}.',
                           'La aposición que se separa por comas y es '
                           'sinónima del núcleo se llama aposición '
                           '{Explicativa}.',
                           'En «Pachacútec, el constructor de Machu Picchu, '
                           'fue el noveno Inca», el segmento entre comas es '
                           'una aposición {Explicativa}.',
                           'La aposición que singulariza al nombre y no va '
                           'entre comas se llama aposición {Especificativa}.',
                           'En «El río Vilcanota recorre el Valle Sagrado», '
                           '«Vilcanota» funciona como una aposición '
                           '{Especificativa}.',
                           'En «El estudiante proactivo logró su propósito», '
                           '«proactivo» funciona como {Modificador directo}.',
                           'En «Los estudiantes con empeño logran todo», '
                           '«con empeño» funciona como {Modificador '
                           'indirecto}.',
                           'En «Cusco, capital histórica del Perú, es una '
                           'ciudad milenaria», «capital histórica del Perú» '
                           'es una aposición {Explicativa}.',
                           'Ortográficamente, la aposición explicativa '
                           'siempre aparece {Separada entre comas}.',
                           'Semánticamente, los elementos de una aposición '
                           'explicativa son {Sinónimos}.']}],
  'cuadros': [{'titulo': '14.3 MODIFICADORES DEL SINTAGMA NOMINAL',
               'encabezados': ['Modificador', 'Se une al núcleo'],
               'filas': [['{Directo}', '{Sin} enlace'],
                         ['{Indirecto}', 'Mediante {preposición}'],
                         ['{Aposición}', 'Mismo {valor} que el núcleo']]}],
  'preguntas': [{'pregunta': 'El término «sintaxis» es de origen griego y '
                             'significa:',
                 'alternativas': ['Comunicación',
                                  'Orden o disposición',
                                  'Significado',
                                  'Sonido',
                                  'Escritura'],
                 'correcta': 'B'},
                {'pregunta': 'La sintaxis, como disciplina lingüística, '
                             'estudia las relaciones entre los elementos de '
                             'una frase y:',
                 'alternativas': ['Solo su ortografía',
                                  'Solo su significado aislado',
                                  'Solo su origen etimológico',
                                  'Solo su pronunciación',
                                  'Las funciones que desempeña cada palabra'],
                 'correcta': 'E'},
                {'pregunta': 'La unidad básica de la sintaxis es:',
                 'alternativas': ['El morfema',
                                  'El grafema',
                                  'La sílaba',
                                  'El fonema',
                                  'El sintagma'],
                 'correcta': 'E'},
                {'pregunta': 'El sintagma se define como una unidad formada '
                             'por palabras dotadas de sentido y valor:',
                 'alternativas': ['Ortográfico',
                                  'Funcional',
                                  'Semántico aislado',
                                  'Fonológico',
                                  'Morfológico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El sintagma nominal también se conoce como:',
                 'alternativas': ['Predicado nominal exclusivo',
                                  'Frase nominal o grupo nominal',
                                  'Complemento circunstancial',
                                  'Sintagma verbal',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo del sintagma nominal siempre es:',
                 'alternativas': ['Un adverbio',
                                  'Una preposición',
                                  'Un sustantivo o palabra sustantivada',
                                  'Una conjunción',
                                  'Un verbo'],
                 'correcta': 'C'},
                {'pregunta': 'Los modificadores del sintagma nominal '
                             'dependen de:',
                 'alternativas': ['El predicado verbal',
                                  'El verbo principal',
                                  'El núcleo',
                                  'El complemento circunstancial',
                                  'El sujeto de otra oración'],
                 'correcta': 'C'},
                {'pregunta': 'El modificador que se une al núcleo del SN sin '
                             'ningún enlace se llama:',
                 'alternativas': ['Aposición explicativa',
                                  'Modificador directo',
                                  'Modificador indirecto',
                                  'Complemento agente',
                                  'Aposición especificativa'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras que funcionan típicamente como '
                             'modificador directo son:',
                 'alternativas': ['Los verbos',
                                  'Las preposiciones',
                                  'Las conjunciones',
                                  'Los adverbios',
                                  'Los artículos y adjetivos'],
                 'correcta': 'E'},
                {'pregunta': 'El modificador que se une al núcleo mediante '
                             'preposiciones se llama:',
                 'alternativas': ['Núcleo secundario',
                                  'Vocativo',
                                  'Modificador indirecto',
                                  'Modificador directo',
                                  'Aposición'],
                 'correcta': 'C'},
                {'pregunta': 'El modificador del SN que tiene el mismo valor '
                             'que el núcleo y puede conmutarse con él es:',
                 'alternativas': ['El modificador directo',
                                  'La aposición',
                                  'El artículo',
                                  'El modificador indirecto',
                                  'El adjetivo calificativo'],
                 'correcta': 'B'},
                {'pregunta': 'La aposición que se separa por comas y es '
                             'sinónima del núcleo se llama aposición:',
                 'alternativas': ['Neutra',
                                  'Indirecta',
                                  'Directa',
                                  'Explicativa',
                                  'Especificativa'],
                 'correcta': 'D'},
                {'pregunta': 'En «Pachacútec, el constructor de Machu '
                             'Picchu, fue el noveno Inca», el segmento entre '
                             'comas es una aposición:',
                 'alternativas': ['Neutra',
                                  'Explicativa',
                                  'Indirecta',
                                  'Especificativa',
                                  'Directa'],
                 'correcta': 'B'},
                {'pregunta': 'La aposición que singulariza al nombre y no va '
                             'entre comas se llama aposición:',
                 'alternativas': ['Explicativa',
                                  'Indirecta',
                                  'Neutra',
                                  'Especificativa',
                                  'Directa'],
                 'correcta': 'D'},
                {'pregunta': 'En «El río Vilcanota recorre el Valle '
                             'Sagrado», «Vilcanota» funciona como una '
                             'aposición:',
                 'alternativas': ['Especificativa',
                                  'Directa',
                                  'Explicativa',
                                  'Indirecta',
                                  'Neutra'],
                 'correcta': 'A'},
                {'pregunta': 'En «El estudiante proactivo logró su '
                             'propósito», «proactivo» funciona como:',
                 'alternativas': ['Núcleo del SN',
                                  'Modificador directo',
                                  'Modificador indirecto',
                                  'Vocativo',
                                  'Aposición'],
                 'correcta': 'B'},
                {'pregunta': 'En «Los estudiantes con empeño logran todo», '
                             '«con empeño» funciona como:',
                 'alternativas': ['Núcleo',
                                  'Aposición explicativa',
                                  'Modificador directo',
                                  'Vocativo',
                                  'Modificador indirecto'],
                 'correcta': 'E'},
                {'pregunta': 'En «Cusco, capital histórica del Perú, es una '
                             'ciudad milenaria», «capital histórica del '
                             'Perú» es una aposición:',
                 'alternativas': ['Directa',
                                  'Neutra',
                                  'Especificativa',
                                  'Explicativa',
                                  'Indirecta'],
                 'correcta': 'D'},
                {'pregunta': 'Ortográficamente, la aposición explicativa '
                             'siempre aparece:',
                 'alternativas': ['Subrayada',
                                  'Separada entre comas',
                                  'Entre paréntesis obligatorios',
                                  'Sin ninguna puntuación',
                                  'En mayúscula total'],
                 'correcta': 'B'},
                {'pregunta': 'Semánticamente, los elementos de una aposición '
                             'explicativa son:',
                 'alternativas': ['Parónimos',
                                  'Antónimos',
                                  'Sin relación semántica',
                                  'Sinónimos',
                                  'Homófonos'],
                 'correcta': 'D'}]},
 {'num': 15,
  'titulo': 'El Texto y la Lectura',
  'secciones': [{'titulo': '15.1 CONCEPTO DEL TEXTO',
                 'items': ['«Texto» proviene del latín «{textus}», que '
                           'significa «{tejido}».',
                           'El texto es una unidad {semántico-estructural}, '
                           'de contenido y forma, que tiene como base al '
                           '{párrafo}.',
                           'El texto tiene un carácter {comunicativo}, un '
                           'carácter {pragmático} y un carácter '
                           'estructurado.',
                           'El texto es la secuencia lingüística con sentido '
                           '{pleno} que un hablante quiere comunicar.']},
                {'titulo': '15.2 ESTRUCTURA INTERNA DEL TEXTO',
                 'items': ['La {idea principal} es la tesis o planteamiento '
                           'central que el autor desarrolla, el núcleo del '
                           '{discurso}.',
                           'Las {ideas secundarias} sirven de argumento a la '
                           'idea principal, fundamentándola y explicándola.',
                           'El {tema} es todo aquello de lo que se habla en '
                           'el texto, el asunto descrito y desarrollado.',
                           'El {título} es una frase breve que sintetiza la '
                           'idea central del texto.']},
                {'titulo': '15.3 CLASES DE TEXTO POR SU FORMA',
                 'items': ['El texto {narrativo} presenta una sucesión de '
                           'acciones en el tiempo, para contar hechos reales '
                           'o {ficticios}.',
                           'El texto {descriptivo} representa por medio de '
                           'palabras un objeto, paisaje o persona, como una '
                           '{pintura} verbal.',
                           'El texto {argumentativo} presenta una tesis y '
                           'argumentos con el objetivo de {persuadir} al '
                           'lector.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El término «texto» proviene del latín «textus», '
                           'que significa {Tejido}.',
                           'El texto se define como una unidad de contenido '
                           'y forma que tiene como base {El párrafo}.',
                           'El texto tiene un carácter comunicativo, un '
                           'carácter pragmático y un carácter '
                           '{Estructurado}.',
                           'El texto se define como la secuencia lingüística '
                           'con sentido {Pleno}.',
                           'La tesis o planteamiento central que el autor '
                           'desarrolla en un texto se llama {Idea '
                           'principal}.',
                           'Las ideas que sirven de argumento a la idea '
                           'principal se llaman {Ideas secundarias}.',
                           'Todo aquello de lo que se habla en un texto, el '
                           'asunto general, se llama {Tema}.',
                           'La frase breve que sintetiza la idea central de '
                           'un texto se llama {Título}.',
                           'El texto que presenta una sucesión de acciones '
                           'en el tiempo se llama texto {Narrativo}.',
                           'La finalidad del texto narrativo es {Contar '
                           'acontecimientos reales o ficticios}.',
                           'El texto que representa con palabras un objeto, '
                           'paisaje o persona se llama texto {Descriptivo}.',
                           'El texto descriptivo es comparado en el texto '
                           'con {Una pintura hecha con palabras}.',
                           'El texto que presenta una tesis con argumentos '
                           'para persuadir al lector se llama texto '
                           '{Argumentativo}.',
                           'La finalidad principal del texto argumentativo '
                           'es {Persuadir al lector sobre un punto de '
                           'vista}.',
                           'El carácter comunicativo del texto se relaciona '
                           'con {Su extensión física}.',
                           'El carácter pragmático del texto implica que se '
                           'produce con {Una intención y en una situación '
                           'concreta}.',
                           'Descubrir la idea de mayor jerarquía en un texto '
                           'es fundamental para lograr {Una comprensión '
                           'cabal del texto}.',
                           'Las ideas secundarias cumplen el papel de '
                           'fundamentar, explicar y {Presentar con diversos '
                           'recursos la idea principal}.',
                           'El tema de un texto puede ser un aspecto general '
                           'como {El cáncer, la violencia o la política}.',
                           'El texto, según el concepto general, es un acto '
                           'de habla o una serie de actos lingüísticos '
                           'realizados en {Una situación comunicativa '
                           'determinada}.']}],
  'cuadros': [{'titulo': '15.3 CLASES DE TEXTO POR SU FORMA',
               'encabezados': ['Clase', 'Finalidad'],
               'filas': [['{Narrativo}', '{Contar} acontecimientos'],
                         ['{Descriptivo}', '{Representar} con palabras'],
                         ['{Argumentativo}', '{Persuadir} al lector']]}],
  'preguntas': [{'pregunta': 'El término «texto» proviene del latín '
                             '«textus», que significa:',
                 'alternativas': ['Escrito',
                                  'Tejido',
                                  'Idea',
                                  'Discurso',
                                  'Palabra'],
                 'correcta': 'B'},
                {'pregunta': 'El texto se define como una unidad de '
                             'contenido y forma que tiene como base:',
                 'alternativas': ['El morfema',
                                  'El párrafo',
                                  'La oración simple',
                                  'El fonema',
                                  'La sílaba'],
                 'correcta': 'B'},
                {'pregunta': 'El texto tiene un carácter comunicativo, un '
                             'carácter pragmático y un carácter:',
                 'alternativas': ['Improvisado',
                                  'Fonológico exclusivo',
                                  'Aleatorio',
                                  'Estructurado',
                                  'Musical'],
                 'correcta': 'D'},
                {'pregunta': 'El texto se define como la secuencia '
                             'lingüística con sentido:',
                 'alternativas': ['Nulo',
                                  'Fragmentado',
                                  'Exclusivamente literal',
                                  'Ambiguo',
                                  'Pleno'],
                 'correcta': 'E'},
                {'pregunta': 'La tesis o planteamiento central que el autor '
                             'desarrolla en un texto se llama:',
                 'alternativas': ['Tema general',
                                  'Subtítulo',
                                  'Título',
                                  'Idea principal',
                                  'Idea secundaria'],
                 'correcta': 'D'},
                {'pregunta': 'Las ideas que sirven de argumento a la idea '
                             'principal se llaman:',
                 'alternativas': ['Conclusiones exclusivas',
                                  'Ideas secundarias',
                                  'Títulos',
                                  'Temas',
                                  'Ideas principales'],
                 'correcta': 'B'},
                {'pregunta': 'Todo aquello de lo que se habla en un texto, '
                             'el asunto general, se llama:',
                 'alternativas': ['Idea secundaria',
                                  'Idea principal',
                                  'Título',
                                  'Argumento',
                                  'Tema'],
                 'correcta': 'E'},
                {'pregunta': 'La frase breve que sintetiza la idea central '
                             'de un texto se llama:',
                 'alternativas': ['Tema',
                                  'Idea secundaria',
                                  'Argumento',
                                  'Título',
                                  'Párrafo'],
                 'correcta': 'D'},
                {'pregunta': 'El texto que presenta una sucesión de acciones '
                             'en el tiempo se llama texto:',
                 'alternativas': ['Argumentativo',
                                  'Descriptivo',
                                  'Expositivo puro',
                                  'Instructivo',
                                  'Narrativo'],
                 'correcta': 'E'},
                {'pregunta': 'La finalidad del texto narrativo es:',
                 'alternativas': ['Definir conceptos',
                                  'Dar instrucciones',
                                  'Contar acontecimientos reales o ficticios',
                                  'Persuadir al lector',
                                  'Describir un objeto'],
                 'correcta': 'C'},
                {'pregunta': 'El texto que representa con palabras un '
                             'objeto, paisaje o persona se llama texto:',
                 'alternativas': ['Argumentativo',
                                  'Narrativo',
                                  'Descriptivo',
                                  'Expositivo',
                                  'Dialógico'],
                 'correcta': 'C'},
                {'pregunta': 'El texto descriptivo es comparado en el texto '
                             'con:',
                 'alternativas': ['Una noticia breve',
                                  'Una fórmula matemática',
                                  'Una pintura hecha con palabras',
                                  'Un poema exclusivamente',
                                  'Un discurso político'],
                 'correcta': 'C'},
                {'pregunta': 'El texto que presenta una tesis con argumentos '
                             'para persuadir al lector se llama texto:',
                 'alternativas': ['Descriptivo',
                                  'Narrativo',
                                  'Dialógico',
                                  'Argumentativo',
                                  'Instructivo'],
                 'correcta': 'D'},
                {'pregunta': 'La finalidad principal del texto argumentativo '
                             'es:',
                 'alternativas': ['Describir un paisaje',
                                  'Persuadir al lector sobre un punto de '
                                  'vista',
                                  'Dar una receta',
                                  'Enumerar datos',
                                  'Narrar hechos'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter comunicativo del texto se '
                             'relaciona con:',
                 'alternativas': ['Su función social',
                                  'Su color',
                                  'Su formato de impresión',
                                  'Su extensión física',
                                  'Su tipografía'],
                 'correcta': 'D'},
                {'pregunta': 'El carácter pragmático del texto implica que '
                             'se produce con:',
                 'alternativas': ['Solo fines comerciales',
                                  'Ninguna intención',
                                  'Una intención y en una situación concreta',
                                  'Solo fines estéticos',
                                  'Total aleatoriedad'],
                 'correcta': 'C'},
                {'pregunta': 'Descubrir la idea de mayor jerarquía en un '
                             'texto es fundamental para lograr:',
                 'alternativas': ['Solo memorizar el texto',
                                  'Una comprensión cabal del texto',
                                  'Evitar el análisis',
                                  'Reducir el vocabulario',
                                  'Ignorar las ideas secundarias'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas secundarias cumplen el papel de '
                             'fundamentar, explicar y:',
                 'alternativas': ['Contradecir la idea principal',
                                  'Presentar con diversos recursos la idea '
                                  'principal',
                                  'Eliminar la idea principal',
                                  'Reemplazar el tema',
                                  'Sustituir el título'],
                 'correcta': 'B'},
                {'pregunta': 'El tema de un texto puede ser un aspecto '
                             'general como:',
                 'alternativas': ['Solo una fecha',
                                  'Solo un número',
                                  'El cáncer, la violencia o la política',
                                  'Solo un lugar geográfico',
                                  'Solo un nombre propio'],
                 'correcta': 'C'},
                {'pregunta': 'El texto, según el concepto general, es un '
                             'acto de habla o una serie de actos '
                             'lingüísticos realizados en:',
                 'alternativas': ['Ausencia total de intención',
                                  'Cualquier situación sin contexto',
                                  'Un contexto irrelevante',
                                  'Una situación comunicativa determinada',
                                  'Un vacío comunicativo'],
                 'correcta': 'D'}]},
 {'num': 16,
  'titulo': 'Relaciones Semánticas',
  'secciones': [{'titulo': '16.1 LA SINONIMIA',
                 'items': ['Etimológicamente, «sinónimo» proviene del griego '
                           '«sin» ({con}) y «onomas» (nombre), es decir, '
                           '{equivalencia} de significados.',
                           'La sinonimia es la semejanza de significados '
                           'entre términos comprendidos en un mismo {campo '
                           'semántico}.',
                           'Los sinónimos pertenecen a la misma clase '
                           '{gramatical} y poseen significados parecidos.',
                           'Los sinónimos {absolutos} o directos tienen el '
                           'mismo significado sin importar el {contexto}, '
                           'como «casa» y «vivienda».',
                           'Los sinónimos {relativos} o indirectos cambian '
                           'de sentido según el {contexto} de la oración.']},
                {'titulo': '16.2 LA ANTONIMIA',
                 'items': ['Los {antónimos} son palabras de la misma '
                           'categoría gramatical que expresan significados '
                           '{contrarios}.',
                           'Los antónimos {absolutos} expresan ideas total y '
                           'exactamente contrarias, como «introvertido» y '
                           '«{extrovertido}».',
                           'Los antónimos {relativos} muestran ideas '
                           'parcialmente opuestas, sin oposición {plena}.']},
                {'titulo': '16.3 LA PARONIMIA',
                 'items': ['La {paronimia} ocurre cuando dos palabras se '
                           'asemejan en su {sonido} pero se escriben '
                           'distinto y tienen significados diferentes.',
                           'Los parónimos por el {acento} cambian de '
                           'significado según sean esdrújulas, llanas o '
                           '{agudas}, como «ánimo», «animo» y «animó».',
                           'Los parónimos por la {escritura} tienen '
                           'significados distintos, como «actitud» (postura) '
                           'y «{aptitud}» (idoneidad).']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Etimológicamente, «sinónimo» significa '
                           '{Equivalencia o afinidad de significados}.',
                           'Los sinónimos, además de significados parecidos, '
                           'pertenecen a la misma {Clase gramatical}.',
                           'Los sinónimos que mantienen el mismo significado '
                           'sin importar el contexto se llaman sinónimos '
                           '{Absolutos}.',
                           'Los sinónimos que cambian de sentido según el '
                           'contexto se llaman sinónimos {Relativos o '
                           'indirectos}.',
                           'Los antónimos se definen como palabras de la '
                           'misma categoría gramatical que expresan '
                           'significados {Contrarios}.',
                           'Los antónimos que expresan ideas total y '
                           'exactamente contrarias se llaman antónimos '
                           '{Absolutos}.',
                           'Los antónimos que muestran ideas parcialmente '
                           'opuestas se llaman antónimos {Relativos}.',
                           'La paronimia ocurre cuando dos palabras se '
                           'asemejan en {Su sonido, pero se escriben '
                           'diferente}.',
                           'Los parónimos, a diferencia de los sinónimos, '
                           'tienen significados {Distintos}.',
                           'Los parónimos diferenciados por el acento, como '
                           '«ánimo», «animo» y «animó», son parónimos por '
                           '{El acento}.',
                           'En «El sacerdote habló de la oración» y «El '
                           'alumno escribió una oración», la palabra '
                           '«oración» ejemplifica {Un sinónimo relativo}.',
                           'Alcalde y alcaide son un ejemplo de {Parónimos '
                           'por la escritura}.',
                           'Las tres relaciones semánticas estudiadas son '
                           'sinonimia, antonimia y {Paronimia}.']}],
  'cuadros': [{'titulo': '16.1-16.3 LAS TRES RELACIONES SEMÁNTICAS',
               'encabezados': ['Relación', 'Característica'],
               'filas': [['{Sinonimia}', 'Significados {semejantes}'],
                         ['{Antonimia}', 'Significados {contrarios}'],
                         ['{Paronimia}',
                          'Sonido {semejante}, significado distinto']]}],
  'preguntas': [{'pregunta': 'Etimológicamente, «sinónimo» significa:',
                 'alternativas': ['Equivalencia o afinidad de significados',
                                  'Oposición de ideas',
                                  'Ausencia de significado',
                                  'Escritura similar',
                                  'Sonido contrario'],
                 'correcta': 'A'},
                {'pregunta': 'La sinonimia es la semejanza de significados '
                             'entre términos comprendidos en un mismo:',
                 'alternativas': ['Campo gráfico',
                                  'Campo morfológico exclusivo',
                                  'Campo fonológico',
                                  'Campo sintáctico exclusivo',
                                  'Campo semántico'],
                 'correcta': 'E'},
                {'pregunta': 'Los sinónimos, además de significados '
                             'parecidos, pertenecen a la misma:',
                 'alternativas': ['Categoría fonológica',
                                  'Categoría ortográfica',
                                  'Raíz etimológica exclusiva',
                                  'Clase gramatical',
                                  'Familia léxica exclusiva'],
                 'correcta': 'D'},
                {'pregunta': 'Los sinónimos que mantienen el mismo '
                             'significado sin importar el contexto se llaman '
                             'sinónimos:',
                 'alternativas': ['Absolutos',
                                  'Relativos',
                                  'Contextuales',
                                  'Parciales',
                                  'Indirectos'],
                 'correcta': 'A'},
                {'pregunta': '«Casa» y «vivienda» son un ejemplo de '
                             'sinónimos:',
                 'alternativas': ['Parónimos',
                                  'Absolutos',
                                  'Antónimos',
                                  'Relativos',
                                  'Parciales'],
                 'correcta': 'B'},
                {'pregunta': 'Los sinónimos que cambian de sentido según el '
                             'contexto se llaman sinónimos:',
                 'alternativas': ['Parciales fijos',
                                  'Universales',
                                  'Directos',
                                  'Absolutos',
                                  'Relativos o indirectos'],
                 'correcta': 'E'},
                {'pregunta': 'Los antónimos se definen como palabras de la '
                             'misma categoría gramatical que expresan '
                             'significados:',
                 'alternativas': ['Idénticos',
                                  'Ambiguos',
                                  'Neutros',
                                  'Semejantes',
                                  'Contrarios'],
                 'correcta': 'E'},
                {'pregunta': 'Los antónimos que expresan ideas total y '
                             'exactamente contrarias se llaman antónimos:',
                 'alternativas': ['Semánticos exclusivos',
                                  'Parciales',
                                  'Indirectos',
                                  'Absolutos',
                                  'Relativos'],
                 'correcta': 'D'},
                {'pregunta': '«Introvertido» y «extrovertido» son un ejemplo '
                             'de antónimos:',
                 'alternativas': ['Relativos',
                                  'Absolutos',
                                  'Parciales',
                                  'Parónimos',
                                  'Sinónimos'],
                 'correcta': 'B'},
                {'pregunta': 'Los antónimos que muestran ideas parcialmente '
                             'opuestas se llaman antónimos:',
                 'alternativas': ['Absolutos',
                                  'Relativos',
                                  'Puros',
                                  'Totales',
                                  'Directos'],
                 'correcta': 'B'},
                {'pregunta': '«Cima» y «planicie» son un ejemplo de '
                             'antónimos:',
                 'alternativas': ['Homófonos',
                                  'Absolutos',
                                  'Relativos',
                                  'Sinónimos',
                                  'Parónimos'],
                 'correcta': 'C'},
                {'pregunta': 'La paronimia ocurre cuando dos palabras se '
                             'asemejan en:',
                 'alternativas': ['Su sonido, pero se escriben diferente',
                                  'Su significado',
                                  'Su extensión',
                                  'Su categoría gramatical exclusivamente',
                                  'Su origen etimológico exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los parónimos, a diferencia de los sinónimos, '
                             'tienen significados:',
                 'alternativas': ['Iguales',
                                  'Idénticos siempre',
                                  'Distintos',
                                  'Opuestos exactamente',
                                  'Ambiguos'],
                 'correcta': 'C'},
                {'pregunta': 'Los parónimos diferenciados por el acento, '
                             'como «ánimo», «animo» y «animó», son parónimos '
                             'por:',
                 'alternativas': ['El acento',
                                  'El significado',
                                  'La escritura',
                                  'La categoría gramatical',
                                  'El origen'],
                 'correcta': 'A'},
                {'pregunta': '«Actitud» (postura) y «aptitud» (idoneidad) '
                             'son un ejemplo de parónimos por:',
                 'alternativas': ['La escritura',
                                  'El sonido idéntico',
                                  'El significado igual',
                                  'La sinonimia',
                                  'El acento'],
                 'correcta': 'A'},
                {'pregunta': '«Absolver» (perdonar) y «absorber» (beber) son '
                             'un ejemplo de parónimos por:',
                 'alternativas': ['El acento',
                                  'La escritura',
                                  'La antonimia',
                                  'El campo semántico',
                                  'La sinonimia'],
                 'correcta': 'B'},
                {'pregunta': 'En «El sacerdote habló de la oración» y «El '
                             'alumno escribió una oración», la palabra '
                             '«oración» ejemplifica:',
                 'alternativas': ['Un parónimo por el acento',
                                  'Un sinónimo absoluto',
                                  'Un antónimo relativo',
                                  'Un antónimo absoluto',
                                  'Un sinónimo relativo'],
                 'correcta': 'E'},
                {'pregunta': '«Rapidez» y «lentitud» son un ejemplo de:',
                 'alternativas': ['Homófonos',
                                  'Sinónimos absolutos',
                                  'Parónimos por el acento',
                                  'Sinónimos relativos',
                                  'Antónimos'],
                 'correcta': 'E'},
                {'pregunta': 'Alcalde y alcaide son un ejemplo de:',
                 'alternativas': ['Antónimos absolutos',
                                  'Sinónimos absolutos',
                                  'Antónimos relativos',
                                  'Sinónimos relativos',
                                  'Parónimos por la escritura'],
                 'correcta': 'E'},
                {'pregunta': 'Las tres relaciones semánticas estudiadas son '
                             'sinonimia, antonimia y:',
                 'alternativas': ['Fonética',
                                  'Sintaxis',
                                  'Ortografía',
                                  'Paronimia',
                                  'Morfología'],
                 'correcta': 'D'}]}]
