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
                 'alternativas': ['Se aíslan mutuamente',
                                  'Interactúan para intercambiar información',
                                  'Compiten entre sí',
                                  'Compran bienes',
                                  'Ejercen autoridad'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de la comunicación constituida por la '
                             'codificación y decodificación mental es la '
                             'fase:',
                 'alternativas': ['Psíquica',
                                  'Física',
                                  'Fisiológica',
                                  'Social',
                                  'Cultural'],
                 'correcta': 'A'},
                {'pregunta': 'La fase que se refiere al funcionamiento del '
                             'aparato fonador y la audición es la fase:',
                 'alternativas': ['Social',
                                  'Semántica',
                                  'Física',
                                  'Fisiológica',
                                  'Psíquica'],
                 'correcta': 'D'},
                {'pregunta': 'El elemento de la comunicación que codifica y '
                             'transmite el mensaje es:',
                 'alternativas': ['El receptor',
                                  'El referente',
                                  'El código',
                                  'El emisor',
                                  'El canal'],
                 'correcta': 'D'},
                {'pregunta': 'El elemento que percibe y decodifica el '
                             'mensaje es:',
                 'alternativas': ['El emisor',
                                  'El mensaje',
                                  'El canal',
                                  'El receptor',
                                  'El código'],
                 'correcta': 'D'},
                {'pregunta': 'El medio físico a través del cual se '
                             'transporta el mensaje se llama:',
                 'alternativas': ['Código',
                                  'Canal',
                                  'Referente',
                                  'Circunstancia',
                                  'Emisor'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de signos convencionales que usan '
                             'emisor y receptor se llama:',
                 'alternativas': ['Mensaje',
                                  'Circunstancia',
                                  'Canal',
                                  'Código',
                                  'Referente'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto de objetos o fenómenos a los que '
                             'se hace mención en el acto comunicativo es:',
                 'alternativas': ['El canal',
                                  'El referente',
                                  'El receptor',
                                  'El emisor',
                                  'El código'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar y momento en que se desarrolla el '
                             'acto comunicativo se denomina:',
                 'alternativas': ['Referente',
                                  'Código',
                                  'Circunstancia o contexto',
                                  'Mensaje',
                                  'Canal'],
                 'correcta': 'C'},
                {'pregunta': 'La comunicación que utiliza el idioma para '
                             'codificar el mensaje es la comunicación:',
                 'alternativas': ['Lingüística',
                                  'Proxémica',
                                  'No lingüística',
                                  'Kinésica',
                                  'Cromática'],
                 'correcta': 'A'},
                {'pregunta': 'La comunicación oral se caracteriza por ser:',
                 'alternativas': ['Siempre escrita',
                                  'Sin recursos no verbales',
                                  'Duradera y planificada',
                                  'Asincrónica',
                                  'Sincrónica y momentánea'],
                 'correcta': 'E'},
                {'pregunta': 'La comunicación escrita se caracteriza por '
                             'ser:',
                 'alternativas': ['Sin puntuación',
                                  'Efímera',
                                  'Sincrónica',
                                  'Asincrónica y planificada',
                                  'Sin cohesión'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina que estudia los movimientos '
                             'corporales y gestos es la:',
                 'alternativas': ['Acústica',
                                  'Háptica',
                                  'Cronémica',
                                  'Proxémica',
                                  'Kinésica'],
                 'correcta': 'E'},
                {'pregunta': 'La disciplina que estudia las relaciones de '
                             'proximidad entre interlocutores es la:',
                 'alternativas': ['Cromática',
                                  'Facial',
                                  'Proxémica',
                                  'Kinésica',
                                  'Oculésica'],
                 'correcta': 'C'},
                {'pregunta': 'La disciplina que estudia el contacto ocular '
                             'durante la comunicación es la:',
                 'alternativas': ['Oculésica',
                                  'Acústica',
                                  'Háptica',
                                  'Kinésica',
                                  'Cronémica'],
                 'correcta': 'A'},
                {'pregunta': 'La disciplina que estudia el uso del tiempo en '
                             'la comunicación es la:',
                 'alternativas': ['Cromática',
                                  'Proxémica',
                                  'Cronémica',
                                  'Háptica',
                                  'Facial'],
                 'correcta': 'C'},
                {'pregunta': 'El monólogo interior y el soliloquio son '
                             'ejemplos de comunicación:',
                 'alternativas': ['Intrapersonal',
                                  'Pública',
                                  'Grupal',
                                  'Interpersonal',
                                  'Masiva'],
                 'correcta': 'A'},
                {'pregunta': 'La comunicación que se produce cuando '
                             'interactúan dos personas es la:',
                 'alternativas': ['Intrapersonal',
                                  'Pública',
                                  'Grupal',
                                  'Interpersonal',
                                  'Social'],
                 'correcta': 'D'},
                {'pregunta': 'La interacción entre ciudadanos y medios de '
                             'comunicación masivos es la comunicación:',
                 'alternativas': ['Pública',
                                  'Interpersonal',
                                  'Grupal',
                                  'Intrapersonal',
                                  'Privada'],
                 'correcta': 'A'},
                {'pregunta': 'La comunicación grupal se orienta al '
                             'cumplimiento de:',
                 'alternativas': ['Reglas externas impuestas',
                                  'Objetivos comunes del grupo',
                                  'Objetivos individuales',
                                  'Metas ajenas al grupo',
                                  'Ninguna finalidad'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el objetivo de la comunicación es '
                             'mantener las relaciones interpersonales con '
                             'otros individuos, se aprecia la función:',
                 'alternativas': ['Social',
                                  'Organizativa',
                                  'Cultural',
                                  'Lingüística',
                                  'Simbólica'],
                 'correcta': 'A'},
                {'pregunta': 'La función de la comunicación que representa '
                             'hechos, objetos o sentimientos por medio de '
                             'símbolos, señales y signos se llama función:',
                 'alternativas': ['Simbólica',
                                  'Lingüística',
                                  'Organizativa',
                                  'Social',
                                  'Cultural'],
                 'correcta': 'A'},
                {'pregunta': 'La función de la comunicación ligada al estilo '
                             'del lenguaje usado en el mensaje (formal, '
                             'informal, culto, popular) se llama función:',
                 'alternativas': ['Organizativa',
                                  'Lingüística',
                                  'Simbólica',
                                  'Social',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación que ordena a las '
                             'personas por puestos, estratos y jerarquías se '
                             'llama función:',
                 'alternativas': ['Lingüística',
                                  'Organizativa',
                                  'Simbólica',
                                  'Social',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'La función de la comunicación que transmite '
                             'hábitos, costumbres, valores y creencias se '
                             'llama función:',
                 'alternativas': ['Lingüística',
                                  'Simbólica',
                                  'Cultural',
                                  'Organizativa',
                                  'Social'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter de la comunicación que implica que '
                             'esta se integra con personas que tienen '
                             'posibilidad de relacionarse se llama carácter:',
                 'alternativas': ['Dinámico',
                                  'Fijo',
                                  'Transaccional',
                                  'Recíproco',
                                  'Integrador'],
                 'correcta': 'E'},
                {'pregunta': 'El carácter de la comunicación dado por la '
                             'interacción de personas que logran entenderse '
                             'entre sí se llama carácter:',
                 'alternativas': ['Recíproco',
                                  'Estático',
                                  'Transaccional',
                                  'Integrador',
                                  'Dinámico'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter de la comunicación que implica que '
                             'esta fluye de forma continua y en cambio '
                             'constante se llama carácter:',
                 'alternativas': ['Fijo',
                                  'Integrador',
                                  'Dinámico',
                                  'Transaccional',
                                  'Recíproco'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter de la comunicación por el cual los '
                             'hombres ejercen una influencia mutua se llama '
                             'carácter:',
                 'alternativas': ['Dinámico',
                                  'Unilateral',
                                  'Integrador',
                                  'Transaccional',
                                  'Recíproco'],
                 'correcta': 'E'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido a la cantidad y calidad de '
                             'información que se tiene sobre el referente se '
                             'llama:',
                 'alternativas': ['Redundancia',
                                  'Competencia lexicológica',
                                  'Actitudes',
                                  'Nivel de conocimiento',
                                  'Contexto sociocultural'],
                 'correcta': 'D'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido al dominio del vocabulario del código '
                             'lingüístico se llama:',
                 'alternativas': ['Contexto sociocultural',
                                  'Competencia lexicológica',
                                  'Nivel de conocimiento',
                                  'Actitudes',
                                  'Ruido'],
                 'correcta': 'B'},
                {'pregunta': 'El factor que influye en la comunicación '
                             'referido a los comportamientos, motivaciones y '
                             'reacciones del interlocutor se llama:',
                 'alternativas': ['Redundancia',
                                  'Actitudes',
                                  'Nivel de conocimiento',
                                  'Competencia lexicológica',
                                  'Contexto'],
                 'correcta': 'B'},
                {'pregunta': 'El factor de degradación que distorsiona la '
                             'calidad del mensaje o interfiere en la '
                             'comunicación se llama:',
                 'alternativas': ['Actitud',
                                  'Redundancia',
                                  'Ruido',
                                  'Contexto',
                                  'Competencia'],
                 'correcta': 'C'},
                {'pregunta': 'El ruido que ocurre en el ambiente, como '
                             'interferencias en el canal (distorsiones '
                             'sonoras, baja señal), se llama ruido:',
                 'alternativas': ['Fisiológico',
                                  'Físico',
                                  'Técnico',
                                  'Psicológico',
                                  'Semántico'],
                 'correcta': 'B'},
                {'pregunta': 'El ruido que surge por defectos orgánicos de '
                             'los interlocutores, como alteraciones visuales '
                             'o auditivas, se llama ruido:',
                 'alternativas': ['Fisiológico',
                                  'Físico',
                                  'Técnico',
                                  'Psicológico',
                                  'Semántico'],
                 'correcta': 'A'},
                {'pregunta': 'El ruido que se produce en el interior del '
                             'individuo, como emociones, miedo o ansiedad, '
                             'se llama ruido:',
                 'alternativas': ['Psicológico',
                                  'Físico',
                                  'Técnico',
                                  'Semántico',
                                  'Fisiológico'],
                 'correcta': 'A'},
                {'pregunta': 'El ruido que ocurre cuando el receptor '
                             'interpreta las palabras del emisor de manera '
                             'distinta a la intención original se llama '
                             'ruido:',
                 'alternativas': ['Semántico',
                                  'Psicológico',
                                  'Fisiológico',
                                  'Técnico',
                                  'Físico'],
                 'correcta': 'A'},
                {'pregunta': 'El ruido intencionado en el que '
                             'deliberadamente se omite parte o todo el '
                             'mensaje se llama ruido:',
                 'alternativas': ['Psicológico',
                                  'Semántico',
                                  'Técnico o blanco',
                                  'Físico',
                                  'Fisiológico'],
                 'correcta': 'C'},
                {'pregunta': 'El factor de perfeccionamiento que reduce los '
                             'efectos del ruido y refuerza la claridad del '
                             'mensaje se llama:',
                 'alternativas': ['Nivel de conocimiento',
                                  'Actitud',
                                  'Competencia lexicológica',
                                  'Redundancia',
                                  'Contexto sociocultural'],
                 'correcta': 'D'},
                {'pregunta': 'El lenguaje no es un producto individual sino '
                             'el resultado de un trabajo colectivo; esta '
                             'característica se refiere a que es: '
                             '(Dirimencia 2018-I)',
                 'alternativas': ['Aprendido',
                                  'Universal',
                                  'Racional',
                                  'Sistemático',
                                  'Convencional'],
                 'correcta': 'E'},
                {'pregunta': 'El lenguaje es: (Dirimencia 2017-II)',
                 'alternativas': ['Utilizado solo por algunos sectores '
                                  'sociales',
                                  'Una facultad exclusiva de los seres '
                                  'humanos para comunicarse',
                                  'Un sistema de signos no convencionales '
                                  'para la comunicación',
                                  'Un fenómeno instintivo e incomplejo',
                                  'Una facultad de todos los seres vivos '
                                  'para interactuar'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y FASES',
                      'items': ['La comunicación es el acto, hecho o proceso '
                                'a través del cual dos o más individuos '
                                'interactúan para intercambiar información, '
                                'ideas o sentimientos.',
                                'La fase psíquica de la comunicación está '
                                'constituida por la codificación del emisor '
                                'y la decodificación del receptor.',
                                'La fase fisiológica se refiere al '
                                'funcionamiento del aparato fonador y de la '
                                'audición.']},
                     {'titulo': 'ELEMENTOS DE LA COMUNICACIÓN',
                      'items': ['El emisor o hablante es quien codifica el '
                                'mensaje mentalmente y lo transmite a su '
                                'interlocutor.',
                                'El receptor u oyente percibe el mensaje y '
                                'lo decodifica para comprender lo que el '
                                'emisor quiso comunicar.',
                                'El canal es el medio físico a través del '
                                'cual se transporta el mensaje, como el aire '
                                'o internet.']},
                     {'titulo': 'CLASES DE COMUNICACIÓN POR EL CÓDIGO',
                      'items': ['La comunicación lingüística utiliza el '
                                'idioma para codificar el mensaje, de forma '
                                'oral o escrita.',
                                'La comunicación oral desarrolla una '
                                'interacción sincrónica y es momentánea o '
                                'efímera.',
                                'La comunicación escrita se desarrolla de '
                                'manera asincrónica y requiere planificación '
                                'previa del texto.']},
                     {'titulo': 'CLASES DE COMUNICACIÓN POR LA RELACIÓN '
                                'EMISOR-RECEPTOR',
                      'items': ['La comunicación intrapersonal se produce en '
                                'una misma persona, como en el monólogo '
                                'interior.',
                                'La comunicación interpersonal se produce '
                                'cuando interactúan dos personas.',
                                'La comunicación grupal se da cuando un '
                                'conjunto de personas transfiere mensajes en '
                                'busca de objetivos comunes.']},
                     {'titulo': 'FUNCIONES DE LA COMUNICACIÓN',
                      'items': ['La función social permite al comunicador '
                                'interactuar apropiadamente según las '
                                'situaciones sociales de los diferentes '
                                'estratos.',
                                'La función simbólica representa hechos, '
                                'objetos o sentimientos por medio de '
                                'símbolos, señales y signos.',
                                'La función lingüística está ligada al '
                                'estilo del lenguaje usado en el mensaje: '
                                'formal, informal, especializado, culto, '
                                'estándar, etc.']},
                     {'titulo': 'NATURALEZA DE LA COMUNICACIÓN',
                      'items': ['El carácter integrador implica que la '
                                'comunicación se integra con personas que '
                                'tienen la posibilidad de relacionarse y '
                                'conocerse.',
                                'El carácter transaccional se da por la '
                                'interacción de personas que pueden '
                                'comunicarse entre sí y logran entenderse.',
                                'El carácter dinámico implica que la '
                                'comunicación fluye de forma continua, en '
                                'cambio constante.']},
                     {'titulo': 'FACTORES QUE INFLUYEN EN LA COMUNICACIÓN',
                      'items': ['El nivel de conocimiento es la cantidad y '
                                'calidad de información que se tiene acerca '
                                'del referente.',
                                'La competencia lexicológica es el dominio '
                                'del vocabulario del código lingüístico; '
                                'permite hablar y escribir con claridad.',
                                'Las actitudes son los comportamientos, '
                                'motivaciones y reacciones que adoptamos, '
                                'como el interés, el nerviosismo o la '
                                'duda.']},
                     {'titulo': 'EL RUIDO Y LA REDUNDANCIA',
                      'items': ['El ruido es el factor de degradación que '
                                'distorsiona la calidad del mensaje o '
                                'cualquier interferencia ajena a los '
                                'elementos de la comunicación.',
                                'Los ruidos no intencionados incluyen el '
                                'ruido físico, fisiológico, psicológico y '
                                'semántico.',
                                'El ruido físico ocurre en el ambiente, como '
                                'interferencias en el canal: distorsiones '
                                'sonoras, baja señal de internet.']}]},
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
                 'alternativas': ['Reflejos biológicos',
                                  'Instintos',
                                  'Sistemas de signos',
                                  'Impulsos',
                                  'Ruidos naturales'],
                 'correcta': 'C'},
                {'pregunta': 'Según Sapir, el lenguaje es un método '
                             'exclusivamente humano y:',
                 'alternativas': ['Universal en todas las especies',
                                  'Animal',
                                  'No instintivo',
                                  'Genético únicamente',
                                  'Instintivo'],
                 'correcta': 'C'},
                {'pregunta': 'Según Pinker, el lenguaje es una capacidad:',
                 'alternativas': ['Exclusiva de algunas culturas',
                                  'Innata del Homo sapiens',
                                  'Adquirida solo en la escuela',
                                  'Aprendida exclusivamente',
                                  'Artificial'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje sea usado por todos los seres '
                             'humanos corresponde a la característica de '
                             'ser:',
                 'alternativas': ['Simbólico',
                                  'Universal',
                                  'Innato',
                                  'Sistémico',
                                  'Multiforme'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje se manifieste de forma oral, '
                             'escrita, gestual o musical corresponde a que '
                             'es:',
                 'alternativas': ['Aprendido',
                                  'Convencional',
                                  'Racional',
                                  'Multiforme',
                                  'Universal'],
                 'correcta': 'D'},
                {'pregunta': 'Que el lenguaje sea resultado de un acuerdo '
                             'comunitario corresponde a que es:',
                 'alternativas': ['Sistémico',
                                  'Simbólico',
                                  'Innato',
                                  'Cultural exclusivo',
                                  'Convencional'],
                 'correcta': 'E'},
                {'pregunta': 'Que el lenguaje funcione de acuerdo a normas o '
                             'reglas corresponde a que es:',
                 'alternativas': ['Racional',
                                  'Multiforme',
                                  'Innato',
                                  'Simbólico',
                                  'Sistémico'],
                 'correcta': 'E'},
                {'pregunta': 'Que una palabra represente algo concreto o '
                             'abstracto corresponde a que el lenguaje es:',
                 'alternativas': ['Universal',
                                  'Aprendido',
                                  'Sistémico',
                                  'Convencional',
                                  'Simbólico'],
                 'correcta': 'E'},
                {'pregunta': 'La función del lenguaje centrada en el emisor, '
                             'que manifiesta emociones, es la función:',
                 'alternativas': ['Fática',
                                  'Expresiva',
                                  'Poética',
                                  'Referencial',
                                  'Apelativa'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el receptor, que busca '
                             'que actúe mediante órdenes, es la función:',
                 'alternativas': ['Poética',
                                  'Fática',
                                  'Expresiva',
                                  'Apelativa',
                                  'Metalingüística'],
                 'correcta': 'D'},
                {'pregunta': 'La función centrada en el contenido, propia de '
                             'textos informativos, es la función:',
                 'alternativas': ['Poética',
                                  'Referencial o representativa',
                                  'Expresiva',
                                  'Fática',
                                  'Apelativa'],
                 'correcta': 'B'},
                {'pregunta': 'La función que se usa cuando el código se '
                             'refiere al código mismo es la función:',
                 'alternativas': ['Poética',
                                  'Fática',
                                  'Metalingüística',
                                  'Referencial',
                                  'Expresiva'],
                 'correcta': 'C'},
                {'pregunta': 'La función centrada en el canal, que mantiene '
                             'el contacto entre interlocutores, es la '
                             'función:',
                 'alternativas': ['Expresiva',
                                  'Referencial',
                                  'Fática',
                                  'Apelativa',
                                  'Poética'],
                 'correcta': 'C'},
                {'pregunta': 'La función centrada en el mensaje, propia de '
                             'las obras literarias, es la función:',
                 'alternativas': ['Metalingüística',
                                  'Fática',
                                  'Apelativa',
                                  'Referencial',
                                  'Poética'],
                 'correcta': 'E'},
                {'pregunta': '«¡Cállate!» es un ejemplo de la función del '
                             'lenguaje:',
                 'alternativas': ['Fática',
                                  'Referencial',
                                  'Apelativa',
                                  'Expresiva',
                                  'Poética'],
                 'correcta': 'C'},
                {'pregunta': '«El precio del gas subió excesivamente» es un '
                             'ejemplo de la función:',
                 'alternativas': ['Referencial',
                                  'Fática',
                                  'Poética',
                                  'Apelativa',
                                  'Expresiva'],
                 'correcta': 'A'},
                {'pregunta': 'Según Saussure, el lenguaje tiene dos planos '
                             'interdependientes: lengua y:',
                 'alternativas': ['Gramática',
                                  'Discurso',
                                  'Sintaxis',
                                  'Habla',
                                  'Texto'],
                 'correcta': 'D'},
                {'pregunta': 'La lengua, según Saussure, es de carácter:',
                 'alternativas': ['Biológico',
                                  'Social',
                                  'Privado',
                                  'Instintivo',
                                  'Individual'],
                 'correcta': 'B'},
                {'pregunta': 'El habla, según Saussure, es de carácter:',
                 'alternativas': ['Universal',
                                  'Convencional exclusivo',
                                  'Colectivo',
                                  'Individual',
                                  'Social'],
                 'correcta': 'D'},
                {'pregunta': 'El habla se realiza físicamente por medio de:',
                 'alternativas': ['Los diccionarios',
                                  'Las normas gramaticales',
                                  'Los órganos de fonación',
                                  'Los signos escritos',
                                  'La memoria colectiva'],
                 'correcta': 'C'},
                {'pregunta': 'Según Noam Chomsky, el lenguaje es una '
                             'facultad innata del ser humano regida por una:',
                 'alternativas': ['Norma arbitraria',
                                  'Convención social',
                                  'Selección natural',
                                  'Tradición cultural',
                                  'Gramática universal'],
                 'correcta': 'E'},
                {'pregunta': 'El dialecto es la variación de una lengua que '
                             'se manifiesta según factores:',
                 'alternativas': ['Generacionales exclusivamente',
                                  'Regionales, geográficos o territoriales',
                                  'Educativos exclusivamente',
                                  'Sociales exclusivamente',
                                  'Individuales'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal en la que cambia el '
                             'vocabulario de una región a otra, como '
                             '«casaca» y «chamarra», se llama variación:',
                 'alternativas': ['Sintáctica',
                                  'Fonética',
                                  'Lexicológica',
                                  'Morfológica',
                                  'Semántica'],
                 'correcta': 'C'},
                {'pregunta': 'La variación dialectal en la que una misma '
                             'palabra tiene significados distintos, como '
                             '«mona», se llama variación:',
                 'alternativas': ['Lexicológica',
                                  'Semántica',
                                  'Fonética',
                                  'Sintáctica',
                                  'Morfológica'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal que se da en la forma y '
                             'estructura de las palabras, como «ratico» y '
                             '«ratito», se llama variación:',
                 'alternativas': ['Sintáctica',
                                  'Morfológica',
                                  'Fonética',
                                  'Lexicológica',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'La variación dialectal que se percibe en la '
                             'entonación y pronunciación, como «yama» y '
                             '«llama», se llama variación:',
                 'alternativas': ['Semántica',
                                  'Lexicológica',
                                  'Morfológica',
                                  'Sintáctica',
                                  'Fonética'],
                 'correcta': 'E'},
                {'pregunta': 'El sociolecto es la variación de una lengua a '
                             'nivel:',
                 'alternativas': ['Social',
                                  'Individual',
                                  'Generacional exclusivo',
                                  'Regional',
                                  'Temporal'],
                 'correcta': 'A'},
                {'pregunta': 'El sociolecto se subdivide en acrolecto, '
                             'basilecto y:',
                 'alternativas': ['Sociolema',
                                  'Idiolecto',
                                  'Dialecto',
                                  'Interlecto',
                                  'Mesolecto'],
                 'correcta': 'E'},
                {'pregunta': 'El nivel sociolectal de los sectores altos, '
                             'educados o cultos se llama:',
                 'alternativas': ['Acrolecto',
                                  'Interlecto',
                                  'Basilecto',
                                  'Idiolecto',
                                  'Mesolecto'],
                 'correcta': 'A'},
                {'pregunta': 'El nivel sociolectal de los sectores sin '
                             'acceso a educación formal se llama:',
                 'alternativas': ['Interlecto',
                                  'Idiolecto',
                                  'Acrolecto',
                                  'Basilecto',
                                  'Mesolecto'],
                 'correcta': 'D'},
                {'pregunta': 'El idiolecto es la variación que sufre una '
                             'lengua a nivel:',
                 'alternativas': ['Regional',
                                  'Social',
                                  'Temporal',
                                  'Generacional',
                                  'Individual'],
                 'correcta': 'E'},
                {'pregunta': 'El interlecto es el sistema transitorio de '
                             'habla entre la lengua materna y:',
                 'alternativas': ['El idiolecto personal',
                                  'El sociolecto',
                                  'La lengua estándar',
                                  'La segunda lengua de un aprendiz',
                                  'El dialecto regional'],
                 'correcta': 'D'},
                {'pregunta': 'Según Alberto Escobar, el interlecto es un '
                             'dialecto social ubicado especialmente en '
                             'áreas:',
                 'alternativas': ['Rurales y urbano-marginales',
                                  'Empresariales',
                                  'Universitarias',
                                  'Costeras exclusivamente',
                                  'Urbanas exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Un signo que guarda relación física de '
                             'causa-efecto con el objeto que representa, '
                             'como el humo y el fuego, se llama:',
                 'alternativas': ['Indicio',
                                  'Ícono',
                                  'Significante',
                                  'Símbolo',
                                  'Signo lingüístico'],
                 'correcta': 'A'},
                {'pregunta': 'Un signo que mantiene relación de semejanza '
                             'con el objeto representado, como una '
                             'fotografía, se llama:',
                 'alternativas': ['Indicio',
                                  'Signo natural exclusivo',
                                  'Significado',
                                  'Símbolo',
                                  'Ícono'],
                 'correcta': 'E'},
                {'pregunta': 'Un signo de carácter convencional y '
                             'arbitrario, como la cruz que representa el '
                             'cristianismo, se llama:',
                 'alternativas': ['Símbolo',
                                  'Significante',
                                  'Signo natural',
                                  'Indicio',
                                  'Ícono'],
                 'correcta': 'A'},
                {'pregunta': 'El signo lingüístico es una entidad psíquica '
                             'de dos caras: concepto e imagen:',
                 'alternativas': ['Táctil',
                                  'Olfativa',
                                  'Visual',
                                  'Acústica',
                                  'Gustativa'],
                 'correcta': 'D'},
                {'pregunta': 'El concepto o idea abstracta que el hablante '
                             'extrae de la realidad se llama:',
                 'alternativas': ['Referente',
                                  'Significante',
                                  'Símbolo',
                                  'Significado',
                                  'Ícono'],
                 'correcta': 'D'},
                {'pregunta': 'La imagen acústica o huella psíquica del '
                             'sonido se llama:',
                 'alternativas': ['Significado',
                                  'Símbolo',
                                  'Concepto',
                                  'Referente',
                                  'Significante'],
                 'correcta': 'E'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual la relación entre significado y '
                             'significante es convencional se llama:',
                 'alternativas': ['Articulada',
                                  'Lineal',
                                  'Arbitraria',
                                  'Inmutable',
                                  'Mutable'],
                 'correcta': 'C'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual los fonemas se desenvuelven uno tras '
                             'otro en el tiempo se llama:',
                 'alternativas': ['Mutable',
                                  'Arbitraria',
                                  'Lineal',
                                  'Inmutable',
                                  'Articulada'],
                 'correcta': 'C'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual este no cambia por decisión de un '
                             'hablante en un momento dado se llama:',
                 'alternativas': ['Arbitraria',
                                  'Mutable',
                                  'Lineal',
                                  'Articulada',
                                  'Inmutable'],
                 'correcta': 'E'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual la relación significado-significante '
                             'cambia a través del tiempo se llama:',
                 'alternativas': ['Arbitraria',
                                  'Inmutable',
                                  'Articulada',
                                  'Lineal',
                                  'Mutable'],
                 'correcta': 'E'},
                {'pregunta': 'La característica del signo lingüístico según '
                             'la cual las unidades mayores son divisibles en '
                             'partes más pequeñas se llama:',
                 'alternativas': ['Articulada',
                                  'Arbitraria',
                                  'Mutable',
                                  'Lineal',
                                  'Inmutable'],
                 'correcta': 'A'},
                {'pregunta': 'El habla, en relación a la lengua, es: '
                             '(Dirimencia 2018-I)',
                 'alternativas': ['Estable',
                                  'Latente',
                                  'Mental',
                                  'Patente',
                                  'Social'],
                 'correcta': 'D'},
                {'pregunta': 'El lenguaje, por ser un legado cultural y '
                             'adquirido en sociedad, tiene un carácter: '
                             '(Dirimencia 2017-II)',
                 'alternativas': ['Aprendido',
                                  'Cultural',
                                  'Multiforme',
                                  'Convencional',
                                  'Universal'],
                 'correcta': 'A'},
                {'pregunta': 'Los niveles básicos de la lengua son: '
                             '(Dirimencia 2017-II)',
                 'alternativas': ['Semántico - ortográfico - sintáctico - '
                                  'lexicológico',
                                  'Fonológico - fonético - lexicológico - '
                                  'pragmático',
                                  'Fonético - morfológico - ortográfico',
                                  'Morfológico - semántico - sintáctico - '
                                  'lexicológico',
                                  'Fonológico - morfológico - sintáctico - '
                                  'semántico'],
                 'correcta': 'E'},
                {'pregunta': 'Cuando Mario Vargas Llosa realiza un discurso '
                             'académico en una prestigiosa universidad, '
                             'emplea el nivel sociolecto denominado: '
                             '(Dirimencia 2018-I)',
                 'alternativas': ['Idiolecto',
                                  'Acrolecto',
                                  'Basilecto',
                                  'Mesolecto',
                                  'Dialecto'],
                 'correcta': 'B'},
                {'pregunta': 'La expresión que pertenece a la variación '
                             'diastrática del acrolecto es: (Dirimencia '
                             '2017-II)',
                 'alternativas': ['El policía puso muchas infracciones de '
                                  'tránsito',
                                  'Enrique no tiene plata para su desayuno',
                                  'Todos le llamaban «tecla» porque '
                                  'aparentaba tener ochenta años',
                                  'A Carlos le duele la barriga '
                                  'terriblemente',
                                  'Los niños estaban con dolor de panza'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO / CARACTERÍSTICAS DEL LENGUAJE',
                      'items': ['Según la RAE, el lenguaje es la facultad '
                                'del ser humano de expresarse y comunicarse '
                                'mediante el sonido articulado u otros '
                                'sistemas de signos.',
                                'Según Sapir, el lenguaje es un método '
                                'exclusivamente humano y no instintivo de '
                                'comunicar ideas, emociones y deseos.',
                                'El lenguaje es universal, porque todos los '
                                'seres humanos lo utilizan en su '
                                'interrelación.',
                                'El lenguaje es multiforme, porque se '
                                'manifiesta de muchas maneras: oral, '
                                'escrita, gestual, musical.']},
                     {'titulo': 'FUNCIONES DEL LENGUAJE / PLANOS DEL '
                                'LENGUAJE: LENGUA Y HABLA',
                      'items': ['La función expresiva o emotiva está '
                                'centrada en el emisor y manifiesta '
                                'emociones o sentimientos.',
                                'La función apelativa o conativa está '
                                'centrada en el receptor; busca que el '
                                'oyente actúe mediante órdenes o ruegos.',
                                'Según Ferdinand de Saussure, el lenguaje '
                                'tiene dos planos interdependientes: lengua '
                                'y habla.',
                                'La lengua es de carácter social: un sistema '
                                'de signos lingüísticos convencionales que '
                                'usa una comunidad.']},
                     {'titulo': 'EL DIALECTO (VARIACIÓN DIATÓPICA) / EL '
                                'SOCIOLECTO (VARIACIÓN DIASTRÁTICA)',
                      'items': ['El dialecto es la variación de una lengua '
                                'que se manifiesta según factores '
                                'regionales, geográficos o territoriales.',
                                'La variación dialectal lexicológica ocurre '
                                'cuando cambia el vocabulario de una región '
                                'a otra: «casaca» (Perú) y «chamarra» '
                                '(México).',
                                'El sociolecto es la variación de una lengua '
                                'a nivel social, ubicada en el eje vertical.',
                                'El sociolecto se subdivide en tres niveles: '
                                'acrolecto, mesolecto y basilecto.']},
                     {'titulo': 'EL IDIOLECTO (VARIACIÓN DIAFÁSICA) / EL '
                                'INTERLECTO',
                      'items': ['El idiolecto es la variación que sufre una '
                                'lengua a nivel individual: cada persona '
                                'tiene su forma peculiar de hablar.',
                                'El idiolecto se ubica en la intersección de '
                                'los ejes horizontal y vertical.',
                                'El interlecto es el sistema transitorio de '
                                'habla entre la lengua materna y la segunda '
                                'lengua de un aprendiz.',
                                'Según Alberto Escobar, el interlecto es un '
                                'dialecto social ubicado especialmente en '
                                'áreas rurales y urbano-marginales.']},
                     {'titulo': 'EL SIGNO: TIPOS / EL SIGNO LINGÜÍSTICO Y '
                                'SUS PLANOS',
                      'items': ['El signo es la representación de algo que, '
                                'por naturaleza o convención, es '
                                'representado; facilita la comunicación.',
                                'Los signos naturales guardan relación '
                                'física de causa-efecto o proximidad con el '
                                'objeto; también se llaman indicios.',
                                'El signo lingüístico es una entidad '
                                'psíquica de dos caras: concepto e imagen '
                                'acústica, asociadas de forma indisoluble.',
                                'El significado es el concepto o idea '
                                'abstracta que el hablante extrae de la '
                                'realidad.']},
                     {'titulo': 'CARACTERÍSTICAS DEL SIGNO LINGÜÍSTICO',
                      'items': ['El signo lingüístico es arbitrario: la '
                                'relación entre significado y significante '
                                'es convencional, no responde a ningún '
                                'motivo.',
                                'El signo lingüístico es lineal: los fonemas '
                                'se desenvuelven uno tras otro en el '
                                'tiempo.']}]},
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
                 'alternativas': ['Sintaxis',
                                  'Fonética',
                                  'Semántica',
                                  'Fonología',
                                  'Morfología'],
                 'correcta': 'D'},
                {'pregunta': 'La disciplina que estudia los mecanismos de '
                             'producción física de los sonidos del habla es '
                             'la:',
                 'alternativas': ['Fonética',
                                  'Semántica',
                                  'Fonología',
                                  'Pragmática',
                                  'Morfología'],
                 'correcta': 'A'},
                {'pregunta': 'El número de fonemas del español es:',
                 'alternativas': ['24', '27', '22', '20', '30'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonemas se representan entre:',
                 'alternativas': ['Llaves { }',
                                  'Paréntesis ( )',
                                  'Barras / /',
                                  'Comillas « »',
                                  'Corchetes [ ]'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonos se representan entre:',
                 'alternativas': ['Comillas « »',
                                  'Barras / /',
                                  'Corchetes [ ]',
                                  'Llaves { }',
                                  'Paréntesis ( )'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonemas son unidades de estudio de la:',
                 'alternativas': ['Fonética',
                                  'Fonología',
                                  'Sintaxis',
                                  'Morfología',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonos son unidades de estudio de la:',
                 'alternativas': ['Pragmática',
                                  'Semántica',
                                  'Morfología',
                                  'Fonética',
                                  'Fonología'],
                 'correcta': 'D'},
                {'pregunta': 'Un fonema se define como un segmento '
                             'fonológico que:',
                 'alternativas': ['Se puede descomponer en unidades menores',
                                  'Carece de valor distintivo',
                                  'No puede descomponerse en unidades '
                                  'sucesivas menores',
                                  'Es siempre visible por escrito',
                                  'No existe en la lengua oral'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonemas son sonidos:',
                 'alternativas': ['Sin valor distintivo',
                                  'Infinitos',
                                  'Reales y materializados',
                                  'Ideales y mentales',
                                  'Exclusivamente escritos'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonos son la materialización de un fonema '
                             'a través:',
                 'alternativas': ['De la escritura',
                                  'De la lectura silenciosa',
                                  'Del habla',
                                  'De la memoria',
                                  'De la gramática'],
                 'correcta': 'C'},
                {'pregunta': 'Un par mínimo, como «beso» y «peso», sirve '
                             'para identificar:',
                 'alternativas': ['Antónimos',
                                  'Palabras sin relación',
                                  'Sinónimos',
                                  'Homófonos idénticos',
                                  'Fonemas distintos por el cambio de '
                                  'significado'],
                 'correcta': 'E'},
                {'pregunta': 'Los elementos constitutivos de un fonema, cuya '
                             'modificación causa contraste significativo, '
                             'son los:',
                 'alternativas': ['Morfemas',
                                  'Dígrafos',
                                  'Fonos',
                                  'Rasgos distintivos',
                                  'Grafemas'],
                 'correcta': 'D'},
                {'pregunta': 'El fonema /p/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sordo',
                                  'Vibrante',
                                  'Sonoro',
                                  'Fricativo',
                                  'Nasal'],
                 'correcta': 'A'},
                {'pregunta': 'El fonema /b/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sonoro',
                                  'Nasal',
                                  'Sordo',
                                  'Vibrante',
                                  'Lateral'],
                 'correcta': 'A'},
                {'pregunta': '«Peso» y «beso» se diferencian por el rasgo '
                             'distintivo de:',
                 'alternativas': ['El modo nasal',
                                  'La vocal final',
                                  'El punto de articulación',
                                  'La sonoridad',
                                  'La sílaba tónica'],
                 'correcta': 'D'},
                {'pregunta': 'Los elementos que constituyen la cadena '
                             'hablada y se estudian con criterios '
                             'articulatorios son los elementos:',
                 'alternativas': ['Suprasegmentales',
                                  'Segmentales',
                                  'Sintácticos',
                                  'Semánticos',
                                  'Morfológicos'],
                 'correcta': 'B'},
                {'pregunta': 'La entonación y el acento son ejemplos de '
                             'elementos:',
                 'alternativas': ['Suprasegmentales',
                                  'Segmentales',
                                  'Léxicos',
                                  'Sintácticos',
                                  'Morfológicos'],
                 'correcta': 'A'},
                {'pregunta': 'El número de dígrafos en la escritura del '
                             'español es:',
                 'alternativas': ['10', '7', '2', '5', '3'],
                 'correcta': 'D'},
                {'pregunta': 'En español, /b/ y /l/ son fonemas distintos '
                             'porque existen pares de palabras como:',
                 'alternativas': ['Tubo y tuvo',
                                  'Vaca y baca',
                                  'Bata y lata',
                                  'Ola y hola',
                                  'Casa y caza'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonemas carecen de significación:',
                 'alternativas': ['Por sí solos',
                                  'Solo en el habla informal',
                                  'En cualquier contexto',
                                  'Siempre en combinación',
                                  'Solo en la escritura'],
                 'correcta': 'A'},
                {'pregunta': 'La rama de la fonética que estudia cómo se '
                             'producen los sonidos mediante los órganos del '
                             'habla es la fonética:',
                 'alternativas': ['Acústica',
                                  'Descriptiva',
                                  'Articulatoria',
                                  'Fonológica',
                                  'Auditiva exclusiva'],
                 'correcta': 'C'},
                {'pregunta': 'La rama de la fonética que estudia las '
                             'propiedades físicas de las ondas sonoras es la '
                             'fonética:',
                 'alternativas': ['Fonológica',
                                  'Acústica',
                                  'Descriptiva',
                                  'Articulatoria',
                                  'Perceptiva exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'El español tiene 24 fonemas segmentales, de '
                             'los cuales el número de fonemas vocálicos es:',
                 'alternativas': ['10', '7', '3', '19', '5'],
                 'correcta': 'E'},
                {'pregunta': 'En los fonemas vocálicos, durante su '
                             'producción, el flujo de aire:',
                 'alternativas': ['Vibra en las cuerdas vocales',
                                  'Encuentra un obstáculo total',
                                  'Se interrumpe parcialmente',
                                  'No encuentra ningún obstáculo',
                                  'Se detiene completamente'],
                 'correcta': 'D'},
                {'pregunta': 'Por el grado de abertura de la boca, las '
                             'vocales /i/ y /u/ se clasifican como:',
                 'alternativas': ['Centrales',
                                  'Semiabiertas',
                                  'Cerradas',
                                  'Abiertas',
                                  'Posteriores'],
                 'correcta': 'C'},
                {'pregunta': 'Por la posición de la lengua, la vocal /a/ se '
                             'clasifica como vocal:',
                 'alternativas': ['Central',
                                  'Anterior o palatal',
                                  'Cerrada',
                                  'Posterior o velar',
                                  'Aguda'],
                 'correcta': 'A'},
                {'pregunta': 'Por el grado de sonoridad, las vocales /o/ y '
                             '/u/ se clasifican como vocales:',
                 'alternativas': ['Agudas',
                                  'Graves',
                                  'Abiertas',
                                  'Medias',
                                  'Cerradas'],
                 'correcta': 'B'},
                {'pregunta': 'Respecto a la vibración de las cuerdas '
                             'vocales, en español:',
                 'alternativas': ['Existen vocales sordas y sonoras por '
                                  'igual',
                                  'Todas las vocales son sonoras',
                                  'Ninguna vocal es sonora',
                                  'Solo /a/ es sonora',
                                  'Todas las vocales son sordas'],
                 'correcta': 'B'},
                {'pregunta': 'El triángulo vocálico, herramienta para '
                             'clasificar las vocales, fue propuesto en 1781 '
                             'por:',
                 'alternativas': ['Noam Chomsky',
                                  'André Martinet',
                                  'F. Hellwag',
                                  'Ferdinand de Saussure',
                                  'Roman Jakobson'],
                 'correcta': 'C'},
                {'pregunta': 'En los fonemas consonánticos, durante su '
                             'realización, se produce:',
                 'alternativas': ['Una interrupción total o parcial del '
                                  'flujo de aire',
                                  'Ninguna interrupción del flujo de aire',
                                  'Solo fricción labial',
                                  'Solo vibración de cuerdas vocales',
                                  'Solo resonancia nasal'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonemas /p/, /b/ y /m/, donde intervienen '
                             'ambos labios, se clasifican por su punto de '
                             'articulación como:',
                 'alternativas': ['Labiodentales',
                                  'Alveolares',
                                  'Dentales',
                                  'Palatales',
                                  'Bilabiales'],
                 'correcta': 'E'},
                {'pregunta': 'El fonema /f/, donde el labio inferior se '
                             'dirige hacia los dientes incisivos superiores, '
                             'se clasifica como:',
                 'alternativas': ['Labiodental',
                                  'Dental',
                                  'Bilabial',
                                  'Alveolar',
                                  'Interdental'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonemas /s/, /n/, /l/, /r/, /rr/, donde el '
                             'ápice de la lengua se dirige hacia los '
                             'alvéolos, se clasifican como:',
                 'alternativas': ['Dentales',
                                  'Interdentales',
                                  'Velares',
                                  'Alveolares',
                                  'Palatales'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonemas /ch/, /y/, /ll/, /ñ/, donde el '
                             'dorso de la lengua se dirige hacia el paladar '
                             'medio, se clasifican como:',
                 'alternativas': ['Velares',
                                  'Dentales',
                                  'Bilabiales',
                                  'Palatales',
                                  'Alveolares'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonemas /k/, /g/, /j/, donde la raíz de la '
                             'lengua se dirige hacia el velo del paladar, se '
                             'clasifican como:',
                 'alternativas': ['Labiodentales',
                                  'Palatales',
                                  'Alveolares',
                                  'Velares',
                                  'Dentales'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonemas /p/, /b/, /d/, /k/, /g/, /t/, '
                             'donde el aire encuentra un cierre momentáneo '
                             'con breve explosión, se clasifican por su modo '
                             'de articulación como:',
                 'alternativas': ['Nasales',
                                  'Fricativos',
                                  'Africados',
                                  'Oclusivos',
                                  'Laterales'],
                 'correcta': 'D'},
                {'pregunta': 'Los fonemas /f/, /z/, /s/, /y/, /j/, donde el '
                             'aire pasa friccionando las paredes del canal, '
                             'se clasifican como:',
                 'alternativas': ['Oclusivos',
                                  'Vibrantes',
                                  'Fricativos',
                                  'Nasales',
                                  'Africados'],
                 'correcta': 'C'},
                {'pregunta': 'El fonema /ch/, que resulta de la combinación '
                             'de una oclusiva con una fricativa, se '
                             'clasifica como:',
                 'alternativas': ['Africado',
                                  'Oclusivo',
                                  'Fricativo',
                                  'Lateral',
                                  'Nasal'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonemas /m/, /n/, /ñ/, donde el aire sale '
                             'por la cavidad nasal y la cavidad oral, se '
                             'clasifican como:',
                 'alternativas': ['Vibrantes',
                                  'Fricativos',
                                  'Nasales',
                                  'Oclusivos',
                                  'Laterales'],
                 'correcta': 'C'},
                {'pregunta': 'Los fonemas /rr/ y /r/, donde el órgano activo '
                             'vibra obstruyendo y abriendo el paso del aire, '
                             'se clasifican como:',
                 'alternativas': ['Oclusivos',
                                  'Nasales',
                                  'Laterales',
                                  'Vibrantes',
                                  'Fricativos'],
                 'correcta': 'D'},
                {'pregunta': 'El fonema /g/, clasificado por punto de '
                             'articulación, modo de articulación y '
                             'sonoridad, corresponde a:',
                 'alternativas': ['Bilabial - oclusivo - sonoro',
                                  'Palatal - africado - sordo',
                                  'Velar - fricativo - sordo',
                                  'Velar - oclusivo - sonoro',
                                  'Alveolar - vibrante - sonoro'],
                 'correcta': 'D'},
                {'pregunta': 'El fonema /j/, clasificado por punto de '
                             'articulación, modo de articulación y '
                             'sonoridad, corresponde a:',
                 'alternativas': ['Bilabial - nasal - sonoro',
                                  'Velar - fricativo - sordo',
                                  'Alveolar - lateral - sonoro',
                                  'Velar - oclusivo - sonoro',
                                  'Palatal - africado - sordo'],
                 'correcta': 'B'},
                {'pregunta': 'Las unidades suprasegmentales son: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Sonidos acústicos y mentales',
                                  'Ritmo y cadencia',
                                  'Vocales y consonantes',
                                  'Acento y entonación',
                                  'Fonética y Fonología'],
                 'correcta': 'D'},
                {'pregunta': 'La Fonética Articulatoria está centrada en: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Los fonemas',
                                  'El canal',
                                  'El receptor',
                                  'El referente',
                                  'El emisor'],
                 'correcta': 'E'},
                {'pregunta': 'La acción coordinada del conjunto de '
                             'estructuras anatómicas que constituyen el '
                             'aparato fonador y resonador interviene en: '
                             '(Banco UNSAAC)',
                 'alternativas': ['El debate académico-científico',
                                  'El sentido de las expresiones',
                                  'La producción de los sonidos',
                                  'Solo en los fonemas vocálicos',
                                  'El habla culta de las personas'],
                 'correcta': 'C'},
                {'pregunta': 'La producción de los sonidos en el acto del '
                             'habla está materializada en los: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Textos',
                                  'Grafemas',
                                  'Fonemas',
                                  'Sonidos inarticulados',
                                  'Fonos'],
                 'correcta': 'E'},
                {'pregunta': 'La disciplina lingüística que analiza las '
                             'características físicas de las ondas sonoras '
                             'que conforman los sonidos de la lengua se '
                             'denomina fonética: (Banco UNSAAC)',
                 'alternativas': ['Descriptiva',
                                  'Articulatoria',
                                  'Perceptiva',
                                  'Acústica',
                                  'General'],
                 'correcta': 'D'},
                {'pregunta': 'La estructura física de los sonidos del habla '
                             'puede ser medida a través de la: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Duración, frecuencia y amplitud',
                                  'Frecuencia, ritmo y acento',
                                  'Amplitud, duración y voz',
                                  'Acento, fonema y grafema',
                                  'Onda, frecuencia y amplitud'],
                 'correcta': 'A'},
                {'pregunta': 'El acento es un fonema suprasegmental y se '
                             'evidencia a través de la función: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Distintiva',
                                  'Ortográfica',
                                  'Contrastiva',
                                  'Metalingüística',
                                  'Culminativa'],
                 'correcta': 'E'},
                {'pregunta': 'La fonación se produce fundamentalmente en la '
                             'cavidad: (Dirimencia 2018-I)',
                 'alternativas': ['Nasal',
                                  'Infraglótica',
                                  'Glótica',
                                  'Supraglótica',
                                  'Oral'],
                 'correcta': 'C'},
                {'pregunta': 'Los movimientos de espiración e inspiración en '
                             'el acto del habla corresponden a mecanismos de '
                             'la: (Dirimencia 2018-I)',
                 'alternativas': ['Respiración',
                                  'Fonación',
                                  'Articulación',
                                  'Vocalización',
                                  'Sonorización'],
                 'correcta': 'A'},
                {'pregunta': 'La cavidad en la que se origina el aire '
                             'utilizado para la fonación es la: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Faríngea',
                                  'Glótica',
                                  'Subglótica',
                                  'Supraglótica',
                                  'Laríngea'],
                 'correcta': 'C'},
                {'pregunta': 'El término que solo presenta fonemas '
                             'consonánticos bilabiales es: (Banco UNSAAC)',
                 'alternativas': ['Risa', 'Tiza', 'Pomo', 'Panel', 'Goma'],
                 'correcta': 'C'},
                {'pregunta': 'La fonética que estudia la producción de '
                             'sonidos del habla se denomina: (Banco UNSAAC)',
                 'alternativas': ['Articulatoria',
                                  'Ortoepía',
                                  'Acústica',
                                  'Perceptiva',
                                  'Genérica'],
                 'correcta': 'A'},
                {'pregunta': 'Los fonos se originan en la cavidad: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Nasal',
                                  'Subglótica',
                                  'Oral',
                                  'Glótica',
                                  'Supraglótica'],
                 'correcta': 'E'},
                {'pregunta': 'La Fonética Acústica está relacionada al: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Contexto',
                                  'Emisor',
                                  'Canal',
                                  'Receptor',
                                  'Mensaje'],
                 'correcta': 'C'},
                {'pregunta': 'La amplitud, como parámetro de medida de las '
                             'ondas sonoras, mide: (Banco UNSAAC)',
                 'alternativas': ['La vibración',
                                  'La intensidad',
                                  'La rapidez',
                                  'El movimiento',
                                  'El tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'La fonética que se ocupa de analizar los '
                             'sonidos particulares de una lengua, como el '
                             'quechua, es la: (Banco UNSAAC)',
                 'alternativas': ['Fisiológica',
                                  'Descriptiva',
                                  'Articulatoria',
                                  'Acústica',
                                  'Perceptiva'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «cítara» es un sustantivo y '
                             '«citará» un verbo en tiempo futuro; entonces '
                             'se aprecia la función: (Banco UNSAAC)',
                 'alternativas': ['Disyuntiva del acento',
                                  'Culminativa del acento',
                                  'Homonímica del sustantivo',
                                  'Distintiva del acento',
                                  'Homofónica del sustantivo'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE FONOLOGÍA Y FONÉTICA',
                      'items': ['La fonología estudia cómo se estructuran '
                                'los segmentos de la lengua para transmitir '
                                'significados, es decir, los sonidos en su '
                                'carácter distintivo.',
                                'La fonética estudia los mecanismos de '
                                'producción, transmisión y percepción de la '
                                'señal sonora del habla.',
                                'En español existen 24 fonemas, '
                                'representados en la escritura por 27 letras '
                                'y 5 dígrafos.']},
                     {'titulo': 'FONEMAS Y FONOS',
                      'items': ['Los fonemas son sonidos ideales, mentales, '
                                'limitados o finitos, y se representan entre '
                                'barras / /.',
                                'Los fonos son la materialización o '
                                'realización de un fonema a través del '
                                'habla, y se representan entre corchetes [ '
                                '].',
                                'Los fonemas son unidades de estudio de la '
                                'Fonología; los fonos son unidades de '
                                'estudio de la Fonética.']},
                     {'titulo': 'EL FONEMA Y LOS RASGOS DISTINTIVOS',
                      'items': ['El fonema es el segmento fonológico que no '
                                'puede descomponerse en unidades menores y '
                                'que distingue significados.',
                                'Los rasgos distintivos son los elementos '
                                'constitutivos de un fonema cuya '
                                'modificación produce un contraste '
                                'significativo.',
                                'El fonema /p/ tiene los rasgos distintivos '
                                'bilabial, oclusivo, sordo y oral.']},
                     {'titulo': 'FONEMAS VOCÁLICOS Y SU CLASIFICACIÓN',
                      'items': ['El español tiene 24 fonemas segmentales: 5 '
                                'son vocálicos y 19 consonánticos.',
                                'En los fonemas vocálicos, el flujo de aire '
                                'no encuentra ningún obstáculo para '
                                'atravesar el canal fonatorio: /a/, /e/, '
                                '/i/, /o/, /u/.',
                                'Por el grado de abertura de la boca: '
                                'vocales cerradas (/i/, /u/), semiabiertas '
                                '(/e/, /o/), y vocal abierta (/a/).']},
                     {'titulo': 'FONEMAS CONSONÁNTICOS: PUNTO DE '
                                'ARTICULACIÓN',
                      'items': ['En los fonemas consonánticos se produce una '
                                'interrupción total o parcial del flujo de '
                                'aire, combinando movimientos de lengua, '
                                'labios y dientes.',
                                'Por el punto de articulación: son '
                                'bilabiales los fonemas /p/, /b/, /m/, donde '
                                'intervienen ambos labios.',
                                'Es labiodental el fonema /f/, donde el '
                                'labio inferior se dirige hacia los dientes '
                                'incisivos superiores.']},
                     {'titulo': 'FONEMAS CONSONÁNTICOS: MODO DE ARTICULACIÓN',
                      'items': ['Por el modo de articulación: son oclusivos '
                                'los fonemas /p/, /b/, /d/, /k/, /g/, /t/, '
                                'donde el aire encuentra un cierre '
                                'momentáneo con breve explosión.',
                                'Son fricativos los fonemas /f/, /z/, /s/, '
                                '/y/, /j/, donde el aire pasa friccionando o '
                                'rozando las paredes del canal.',
                                'Es africado el fonema /ch/, que resulta de '
                                'la combinación de la oclusiva con la '
                                'fricativa.']},
                     {'titulo': 'ELEMENTOS SEGMENTALES Y SUPRASEGMENTALES',
                      'items': ['Los elementos segmentales constituyen la '
                                'cadena hablada, definidos según criterios '
                                'articulatorios, acústicos y perceptivos.',
                                'Los elementos suprasegmentales, como la '
                                'entonación y el acento, se superponen a la '
                                'cadena de sonidos.']},
                     {'titulo': 'RAMAS DE LA FONÉTICA',
                      'items': ['La fonética articulatoria estudia cómo se '
                                'producen los sonidos mediante los órganos '
                                'del habla.',
                                'La fonética acústica estudia las '
                                'propiedades físicas de las ondas sonoras '
                                'del habla.',
                                'La fonética descriptiva o auditiva estudia '
                                'cómo el oído percibe los sonidos del '
                                'habla.']}]},
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
                 'alternativas': ['Morfológico exclusivo',
                                  'Organizador de la lengua',
                                  'Semántico',
                                  'Pragmático',
                                  'Sintáctico'],
                 'correcta': 'B'},
                {'pregunta': 'La sílaba se agrupa en torno al segmento de '
                             'máxima:',
                 'alternativas': ['Consonancia',
                                  'Frecuencia',
                                  'Intensidad tonal',
                                  'Sonoridad',
                                  'Duración'],
                 'correcta': 'D'},
                {'pregunta': 'En español, el núcleo silábico es siempre de '
                             'naturaleza:',
                 'alternativas': ['Fricativa',
                                  'Vocálica',
                                  'Consonántica',
                                  'Nasal',
                                  'Mixta obligatoria'],
                 'correcta': 'B'},
                {'pregunta': 'El constituyente silábico que es la cumbre o '
                             'centro de la sílaba es:',
                 'alternativas': ['El núcleo',
                                  'La rima',
                                  'La coda',
                                  'El inicio',
                                  'El ataque'],
                 'correcta': 'A'},
                {'pregunta': 'El margen silábico anterior, de naturaleza '
                             'consonántica, se llama:',
                 'alternativas': ['Núcleo',
                                  'Rima',
                                  'Coda',
                                  'Centro',
                                  'Inicio o ataque'],
                 'correcta': 'E'},
                {'pregunta': 'El margen silábico posterior, en posición '
                             'implosiva, se llama:',
                 'alternativas': ['Centro',
                                  'Ataque',
                                  'Coda',
                                  'Núcleo',
                                  'Inicio'],
                 'correcta': 'C'},
                {'pregunta': 'La rima silábica está constituida por:',
                 'alternativas': ['El inicio y la coda',
                                  'Solo la coda',
                                  'Solo el inicio',
                                  'El núcleo y la coda',
                                  'Ningún elemento fijo'],
                 'correcta': 'D'},
                {'pregunta': 'El silabeo consiste en:',
                 'alternativas': ['Unir todas las sílabas',
                                  'Eliminar las vocales',
                                  'Contar las consonantes',
                                  'Pronunciar o escribir separadas las '
                                  'sílabas de una palabra',
                                  'Acentuar todas las palabras'],
                 'correcta': 'D'},
                {'pregunta': 'Una consonante entre dos vocales siempre forma '
                             'sílaba con la vocal que:',
                 'alternativas': ['Es tónica',
                                  'Está más lejos',
                                  'La sigue',
                                  'La precede',
                                  'Es átona'],
                 'correcta': 'C'},
                {'pregunta': 'En la palabra «pato», la separación silábica '
                             'correcta es:',
                 'alternativas': ['Pa-t-o',
                                  'P-ato',
                                  'Pato completo',
                                  'Pa-to',
                                  'Pat-o'],
                 'correcta': 'D'},
                {'pregunta': 'Los grupos tautosilábicos pr, br, tr, cr, pl, '
                             'bl, cl se caracterizan por ser:',
                 'alternativas': ['Separables siempre',
                                  'Nulos en español',
                                  'Vocálicos',
                                  'Inseparables',
                                  'Solo finales de palabra'],
                 'correcta': 'D'},
                {'pregunta': 'En la palabra «apretar», el grupo «pr» se '
                             'mantiene:',
                 'alternativas': ['Eliminado',
                                  'Junto, formando sílaba con la vocal '
                                  'siguiente',
                                  'Acentuado siempre',
                                  'Separado en dos sílabas',
                                  'Sustituido por otra letra'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una sílaba termina en consonante y la '
                             'siguiente comienza en otra consonante, ambas '
                             'se:',
                 'alternativas': ['Convierten en vocales',
                                  'Eliminan',
                                  'Unen en una sola sílaba',
                                  'Ignoran en el silabeo',
                                  'Separan entre ambas consonantes'],
                 'correcta': 'E'},
                {'pregunta': 'En la palabra «asma», la separación silábica '
                             'es:',
                 'alternativas': ['As-ma',
                                  'A-s-ma',
                                  'A-sma',
                                  'Asm-a',
                                  'Asma sin dividir'],
                 'correcta': 'A'},
                {'pregunta': 'En español NO existe frontera silábica en la '
                             'secuencia:',
                 'alternativas': ['Consonante-consonante',
                                  'Vocal-vocal',
                                  'Diptongo-consonante',
                                  'Consonante-vocal',
                                  'Vocal-consonante'],
                 'correcta': 'D'},
                {'pregunta': 'En la palabra «Cuba», la separación silábica '
                             'correcta es:',
                 'alternativas': ['Cuba sin dividir',
                                  'Cu-b-a',
                                  'Cub-a',
                                  'C-uba',
                                  'Cu-ba'],
                 'correcta': 'E'},
                {'pregunta': 'Un vocablo monosilábico, como «pan», tiene:',
                 'alternativas': ['Ninguna sílaba',
                                  'Dos sílabas',
                                  'Tres sílabas',
                                  'Una sola sílaba',
                                  'Cuatro sílabas o más'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «amor» se divide silábicamente '
                             'como:',
                 'alternativas': ['A-m-or',
                                  'Amo-r',
                                  'A-mor',
                                  'Am-or',
                                  'Amor sin dividir'],
                 'correcta': 'C'},
                {'pregunta': 'El núcleo silábico, según el texto, resulta '
                             'determinante para asignar:',
                 'alternativas': ['El acento léxico',
                                  'El número gramatical',
                                  'La categoría sintáctica',
                                  'El sujeto de la oración',
                                  'El género gramatical'],
                 'correcta': 'A'},
                {'pregunta': 'Un sonido o grupo de sonidos pronunciados en '
                             'un solo golpe de voz constituye:',
                 'alternativas': ['Una sílaba',
                                  'Un sintagma',
                                  'Un fonema aislado',
                                  'Una oración',
                                  'Un morfema'],
                 'correcta': 'A'},
                {'pregunta': 'Las vocales solas, por sí mismas, pueden '
                             'constituir:',
                 'alternativas': ['Solo palabras compuestas',
                                  'Sílabas',
                                  'Ningún elemento fónico',
                                  'Solo consonantes',
                                  'Solo diptongos'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando dos elementos contiguos, como una '
                             'consonante y una líquida (pl, tr, cl), '
                             'pertenecen a la misma sílaba, se llaman '
                             'grupos:',
                 'alternativas': ['Tautosilábicos',
                                  'Silábicos simples',
                                  'Vocálicos',
                                  'Consonánticos exclusivos',
                                  'Heterosilábicos'],
                 'correcta': 'A'},
                {'pregunta': 'La concurrencia de dos vocales que forman una '
                             'sola sílaba se llama:',
                 'alternativas': ['Diptongo',
                                  'Triptongo',
                                  'Hiato',
                                  'Sinalefa exclusiva',
                                  'Sinéresis exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'El diptongo que combina una vocal cerrada y '
                             'una abierta (en ese orden), como en «pues», se '
                             'llama diptongo:',
                 'alternativas': ['Creciente',
                                  'Decreciente',
                                  'Neutro',
                                  'Homogéneo',
                                  'Simple'],
                 'correcta': 'A'},
                {'pregunta': 'El diptongo que combina una vocal abierta y '
                             'una cerrada (en ese orden), como en «aire», se '
                             'llama diptongo:',
                 'alternativas': ['Decreciente',
                                  'Neutro',
                                  'Creciente',
                                  'Homogéneo',
                                  'Compuesto'],
                 'correcta': 'A'},
                {'pregunta': 'El triptongo está constituido, según el '
                             'esquema VC+VA+VC, por dos vocales cerradas y '
                             'una vocal:',
                 'alternativas': ['Tónica exclusiva',
                                  'Nasal',
                                  'Neutra',
                                  'Abierta',
                                  'Cerrada adicional'],
                 'correcta': 'D'},
                {'pregunta': 'Las vocales de un triptongo se pronuncian como '
                             'una sola sílaba y, bajo ninguna circunstancia, '
                             'pueden:',
                 'alternativas': ['Combinarse con consonantes',
                                  'Repetirse',
                                  'Separarse',
                                  'Llevar tilde',
                                  'Iniciar palabra'],
                 'correcta': 'C'},
                {'pregunta': 'Dos segmentos consecutivos que se integran en '
                             'sílabas diferentes forman grupos:',
                 'alternativas': ['Diptongados',
                                  'Fonéticos simples',
                                  'Heterosilábicos',
                                  'Triptongados',
                                  'Tautosilábicos'],
                 'correcta': 'C'},
                {'pregunta': 'Dos vocales seguidas que se separan para '
                             'formar dos sílabas distintas constituyen:',
                 'alternativas': ['Un diptongo',
                                  'Una sinalefa',
                                  'Un hiato',
                                  'Un triptongo',
                                  'Un grupo tautosilábico'],
                 'correcta': 'C'},
                {'pregunta': 'Cuando hay dos vocales fuertes o abiertas '
                             'juntas, como en «peón», siempre se produce:',
                 'alternativas': ['Triptongo',
                                  'Hiato',
                                  'Sinéresis',
                                  'Diptongo',
                                  'Elisión'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una vocal débil o cerrada es tónica '
                             '(lleva tilde) junto a una vocal fuerte, como '
                             'en «día», el diptongo se deshace y se forma:',
                 'alternativas': ['Una sinalefa',
                                  'Un hiato',
                                  'Un grupo consonántico',
                                  'Una elisión',
                                  'Un triptongo'],
                 'correcta': 'B'},
                {'pregunta': 'Los sonidos dentro de la sílaba se organizan '
                             'de acuerdo con la:',
                 'alternativas': ['Ley de Grimm',
                                  'Norma académica',
                                  'Escala fonética simple',
                                  'Regla de acentuación',
                                  'Escala universal de sonoridad'],
                 'correcta': 'E'},
                {'pregunta': 'De acuerdo con los principios de ordenación de '
                             'los segmentos en la sílaba, los márgenes '
                             'extremos en la Escala Universal de Sonoridad '
                             'son: (Banco UNSAAC)',
                 'alternativas': ['Vocales silábicas - nasales',
                                  'Vocales satelitales - africada',
                                  'Vocales silábicas - oclusivas',
                                  'Vocales - consonantes',
                                  'Aproximantes - fricativas'],
                 'correcta': 'C'},
                {'pregunta': 'La sílaba subrayada en la palabra '
                             '«Tráns-fu-ga» es del tipo: (Banco UNSAAC)',
                 'alternativas': ['CCVCS',
                                  'CSVCC',
                                  'CCVSC',
                                  'CCVCC',
                                  'CSVCS'],
                 'correcta': 'A'},
                {'pregunta': 'Por el grado de abertura de la vocal, la '
                             'palabra «vértigo» presenta la secuencia de '
                             'fonemas vocálicos: (Banco UNSAAC)',
                 'alternativas': ['Semiabierto - cerrado - semiabierto',
                                  'Anterior - cerrado - velar',
                                  'Intermedio - semiabierto - cerrado',
                                  'Abierto - semiabierto - semiabierto',
                                  'Abierto - cerrado - abierto'],
                 'correcta': 'A'},
                {'pregunta': 'Las sílabas que presenta la palabra FRAGUA '
                             'son: (Banco UNSAAC)',
                 'alternativas': ['Diptongadas',
                                  'Tautosilábicas',
                                  'Cerradas',
                                  'Heterosilábicas',
                                  'Trabadas'],
                 'correcta': 'B'},
                {'pregunta': 'De acuerdo a la Escala Universal de Sonoridad, '
                             'la palabra PLAN presenta, en orden '
                             'decreciente: (Banco UNSAAC)',
                 'alternativas': ['A>N>P>L',
                                  'P<N<L<A',
                                  'A>L>N>P',
                                  'A>N>L>P',
                                  'P<L<N<A'],
                 'correcta': 'D'},
                {'pregunta': 'De acuerdo a la Escala Universal de Sonoridad: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Las consonantes líquidas son menos '
                                  'perceptibles que las oclusivas',
                                  'Las consonantes nasales son más '
                                  'perceptibles que las líquidas',
                                  'Las consonantes nasales son menos '
                                  'perceptibles que las líquidas',
                                  'Las consonantes oclusivas son más '
                                  'perceptibles que las fricativas',
                                  'Las vocales silábicas son menos '
                                  'perceptibles que las satelitales'],
                 'correcta': 'C'},
                {'pregunta': 'Tomando en cuenta los tipos de sílaba, la '
                             'palabra «constructivo» presenta la siguiente '
                             'estructura: (Banco UNSAAC)',
                 'alternativas': ['CVCC - CCVS - VC - CV',
                                  'CVCC - CVCC - CV - CV',
                                  'CVCS - CCVC - CV - VC',
                                  'CVSC - CCVS - CV - VC',
                                  'CVCC - CCVC - CV - CV'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['La sílaba es la unidad estructural que '
                                'actúa como principio organizador de la '
                                'lengua.',
                                'La sílaba se agrupa en torno al segmento de '
                                'máxima sonoridad, que constituye su núcleo.',
                                'En español, el núcleo silábico es siempre '
                                'vocálico.']},
                     {'titulo': 'CONSTITUYENTES SILÁBICOS',
                      'items': ['El núcleo es la cumbre o centro de la '
                                'sílaba, constituido por una sola vocal.',
                                'El inicio o ataque es el margen silábico '
                                'anterior, de naturaleza consonántica, en '
                                'posición explosiva.',
                                'La coda es el margen silábico posterior, de '
                                'naturaleza consonántica, en posición '
                                'implosiva.']},
                     {'titulo': 'EL SILABEO O DIVISIÓN SILÁBICA',
                      'items': ['El silabeo consiste en pronunciar o '
                                'escribir en forma separada las sílabas de '
                                'una palabra.',
                                'Una consonante entre dos vocales siempre '
                                'forma sílaba con la vocal que la sigue: '
                                'pa-to.',
                                'Los grupos tautosilábicos como pr, br, tr, '
                                'cr, pl, bl, cl son inseparables y forman '
                                'sílaba con la vocal siguiente.']},
                     {'titulo': 'GRUPOS TAUTOSILÁBICOS Y DIPTONGOS',
                      'items': ['Los grupos tautosilábicos ocurren cuando '
                                'dos elementos contiguos pertenecen a la '
                                'misma sílaba: combinaciones pl, pr, cl, cr, '
                                'fl, fr, bl, br, gl, gr, tl, tr.',
                                'El diptongo es la concurrencia de dos '
                                'vocales que forman una sola sílaba.',
                                'El diptongo creciente combina una vocal '
                                'cerrada y una abierta, o dos vocales '
                                'cerradas diferentes; ejemplo: pues.']},
                     {'titulo': 'EL TRIPTONGO',
                      'items': ['El triptongo está constituido por dos '
                                'vocales cerradas (débiles) y una abierta '
                                '(fuerte) en medio, según el esquema VC + VA '
                                '+ VC.',
                                'Las vocales del triptongo se pronuncian '
                                'como una sola sílaba y no pueden separarse; '
                                'ejemplo: cam-biáis.']},
                     {'titulo': 'EL HIATO (GRUPOS HETEROSILÁBICOS)',
                      'items': ['En los grupos heterosilábicos, dos '
                                'segmentos consecutivos se integran en '
                                'sílabas diferentes: es el caso del hiato.',
                                'El hiato son dos vocales seguidas que se '
                                'separan para formar dos sílabas.',
                                'Cuando hay dos vocales fuertes (abiertas) '
                                'juntas, siempre se produce hiato; ejemplo: '
                                'pe-ón.']},
                     {'titulo': 'PRINCIPIOS DE ORDENACIÓN DE LOS SEGMENTOS',
                      'items': ['Los sonidos dentro de la sílaba se '
                                'organizan según la escala universal de '
                                'sonoridad, donde las vocales son las '
                                'unidades más perceptibles.']}]},
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
                 'alternativas': ['Apóstrofo',
                                  'Diéresis',
                                  'Guion',
                                  'Tilde',
                                  'Cedilla'],
                 'correcta': 'D'},
                {'pregunta': 'El acento que diferencia en la pronunciación '
                             'una sílaba, contrastándola con el resto, es el '
                             'acento:',
                 'alternativas': ['Diacrítico',
                                  'Prosódico',
                                  'Gráfico',
                                  'Fonológico puro',
                                  'Ortográfico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La función del acento que diferencia unidades '
                             'acentuadas de inacentuadas es la función:',
                 'alternativas': ['Contrastiva',
                                  'Gráfica',
                                  'Semántica',
                                  'Culminativa',
                                  'Distintiva'],
                 'correcta': 'A'},
                {'pregunta': 'La función del acento que diferencia el '
                             'significado de palabras como «médico» y '
                             '«medicó» es la función:',
                 'alternativas': ['Culminativa',
                                  'Contrastiva',
                                  'Ortográfica',
                                  'Prosódica pura',
                                  'Distintiva'],
                 'correcta': 'E'},
                {'pregunta': 'La función que permite percibir los grupos '
                             'acentuales del discurso es la función:',
                 'alternativas': ['Gráfica',
                                  'Distintiva',
                                  'Contrastiva',
                                  'Culminativa',
                                  'Semántica'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras monosilábicas, por regla general:',
                 'alternativas': ['Llevan doble tilde',
                                  'Siempre llevan tilde',
                                  'Se acentúan según el contexto',
                                  'Llevan tilde si son agudas',
                                  'Nunca se acentúan gráficamente, salvo '
                                  'tilde diacrítica'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras agudas tienen la sílaba tónica en '
                             'la posición:',
                 'alternativas': ['Primera',
                                  'Anterior a la antepenúltima',
                                  'Última',
                                  'Antepenúltima',
                                  'Penúltima'],
                 'correcta': 'C'},
                {'pregunta': 'Las palabras agudas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['Cualquier consonante',
                                  'Ninguna terminación específica',
                                  'Solo consonantes dobles',
                                  'N, s o vocal',
                                  'La letra y siempre'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras llanas o graves tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Primera',
                                  'Antepenúltima',
                                  'Última',
                                  'Penúltima',
                                  'Anterior a la antepenúltima'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras llanas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['Consonante distinta de n, s o vocal',
                                  'Ninguna terminación',
                                  'Solo la letra y',
                                  'N, s o vocal',
                                  'Solo vocal'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras esdrújulas tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Primera exclusivamente',
                                  'Antepenúltima',
                                  'Última',
                                  'Anterior a la antepenúltima',
                                  'Penúltima'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras esdrújulas, en cuanto a la tilde:',
                 'alternativas': ['Todas llevan tilde',
                                  'Solo algunas llevan tilde',
                                  'Dependen del contexto',
                                  'Nunca llevan tilde',
                                  'Llevan tilde solo si terminan en vocal'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras sobresdrújulas tienen la sílaba '
                             'tónica:',
                 'alternativas': ['En la última posición',
                                  'Sin posición fija',
                                  'En la antepenúltima',
                                  'Anterior a la antepenúltima',
                                  'En la penúltima'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras sobresdrújulas se caracterizan '
                             'por ser:',
                 'alternativas': ['Compuestas, y todas llevan tilde',
                                  'Sin tilde nunca',
                                  'Solo verbos',
                                  'Monosilábicas',
                                  'Siempre simples'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «cuéntaselo» es un ejemplo de '
                             'palabra:',
                 'alternativas': ['Llana',
                                  'Aguda',
                                  'Sobresdrújula',
                                  'Esdrújula',
                                  'Monosilábica'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «césped» es un ejemplo de palabra:',
                 'alternativas': ['Llana',
                                  'Sobresdrújula',
                                  'Monosilábica',
                                  'Esdrújula',
                                  'Aguda'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «comité» lleva tilde porque es '
                             'aguda terminada en:',
                 'alternativas': ['Vocal',
                                  'Consonante doble',
                                  'N',
                                  'Consonante distinta de n o s',
                                  'S'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «botón» lleva tilde porque es aguda '
                             'terminada en:',
                 'alternativas': ['Vocal',
                                  'Consonante doble',
                                  'S',
                                  'N',
                                  'La letra y'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «jueves» no lleva tilde porque, '
                             'siendo llana, termina en:',
                 'alternativas': ['Consonante doble',
                                  'La letra y',
                                  'Vocal abierta tónica',
                                  'S',
                                  'Consonante distinta de n o s'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «música» es un ejemplo de palabra:',
                 'alternativas': ['Aguda',
                                  'Monosilábica',
                                  'Esdrújula',
                                  'Llana',
                                  'Sobresdrújula'],
                 'correcta': 'C'},
                {'pregunta': 'Las palabras con diptongo se acentúan '
                             'gráficamente de acuerdo con:',
                 'alternativas': ['Las reglas generales de acentuación',
                                  'Solo la posición del hiato',
                                  'Una regla especial exclusiva',
                                  'Reglas del triptongo',
                                  'No se acentúan nunca'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando una palabra con diptongo debe llevar '
                             'tilde, esta se coloca sobre:',
                 'alternativas': ['La vocal abierta del diptongo',
                                  'Ninguna vocal específica',
                                  'La última letra de la palabra',
                                  'La vocal cerrada siempre',
                                  'La primera vocal siempre'],
                 'correcta': 'A'},
                {'pregunta': 'En las palabras con triptongo que deben '
                             'tildarse, como «apreciáis», la tilde se coloca '
                             'sobre:',
                 'alternativas': ['La primera vocal cerrada',
                                  'Ninguna vocal',
                                  'La vocal abierta',
                                  'La segunda vocal cerrada',
                                  'La consonante final'],
                 'correcta': 'C'},
                {'pregunta': 'Las palabras con hiato siempre llevan tilde '
                             'en:',
                 'alternativas': ['La vocal abierta',
                                  'La última sílaba únicamente',
                                  'La consonante final',
                                  'La vocal cerrada',
                                  'La primera sílaba'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «sabías», con hiato, lleva tilde en '
                             'la vocal cerrada a pesar de ser una palabra:',
                 'alternativas': ['Aguda terminada en consonante',
                                  'Monosilábica',
                                  'Llana terminada en vocal',
                                  'Sobresdrújula',
                                  'Esdrújula'],
                 'correcta': 'C'},
                {'pregunta': 'Palabras como «raíz» y «maíz» llevan tilde en '
                             'el hiato a pesar de ser palabras agudas '
                             'terminadas en:',
                 'alternativas': ['Vocal',
                                  'Y',
                                  'N o s',
                                  'Consonante distinta de n o s',
                                  'Consonante doble'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando una palabra tiene hiato de dos vocales '
                             'abiertas o fuertes juntas, como «Jaén» o '
                             '«peleó», la acentuación sigue:',
                 'alternativas': ['Las reglas generales de acentuación',
                                  'Solo la regla del diptongo',
                                  'Una regla exclusiva del hiato',
                                  'Ninguna regla específica',
                                  'No se acentúan nunca'],
                 'correcta': 'A'},
                {'pregunta': 'En la oración «Tú eres Santiago», la palabra '
                             '«tú» lleva tilde porque funciona como:',
                 'alternativas': ['Adverbio',
                                  'Preposición',
                                  'Pronombre personal',
                                  'Adjetivo posesivo',
                                  'Conjunción'],
                 'correcta': 'C'},
                {'pregunta': 'En la oración «Tu casa es muy hermosa», la '
                             'palabra «tu» no lleva tilde porque funciona '
                             'como:',
                 'alternativas': ['Adjetivo posesivo',
                                  'Preposición',
                                  'Pronombre personal',
                                  'Adverbio',
                                  'Conjunción'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «sí», con tilde, funciona como '
                             'adverbio de afirmación o como pronombre '
                             'personal, mientras que «si», sin tilde, '
                             'funciona como:',
                 'alternativas': ['Adverbio de lugar',
                                  'Sustantivo exclusivo',
                                  'Adjetivo',
                                  'Pronombre personal',
                                  'Conjunción condicional'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra «dé», forma del verbo dar, lleva '
                             'tilde para distinguirse de «de», que sin tilde '
                             'funciona como:',
                 'alternativas': ['Adverbio',
                                  'Pronombre',
                                  'Preposición',
                                  'Conjunción',
                                  'Adjetivo'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «más», cuantificador, lleva tilde '
                             'para distinguirse de «mas», que sin tilde es '
                             'una conjunción equivalente a:',
                 'alternativas': ['Y', 'O', 'Aunque', 'Porque', 'Pero'],
                 'correcta': 'E'},
                {'pregunta': 'Las palabras qué, cuál, quién, cómo, dónde y '
                             'cuándo se escriben con tilde diacrítica cuando '
                             'son:',
                 'alternativas': ['Relativos o conjunciones',
                                  'Adverbios de modo exclusivos',
                                  'Artículos',
                                  'Interrogativas o exclamativas',
                                  'Preposiciones'],
                 'correcta': 'D'},
                {'pregunta': 'En la oración «¿Por qué ha dicho eso?», la '
                             'palabra «qué» lleva tilde a pesar de estar '
                             'precedida por una:',
                 'alternativas': ['Preposición',
                                  'Un pronombre',
                                  'Conjunción',
                                  'Otro interrogativo',
                                  'Un artículo'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras qué, cuál, quién, cómo, dónde y '
                             'cuándo se escriben sin tilde cuando funcionan '
                             'como:',
                 'alternativas': ['Interrogativas directas',
                                  'Sustantivos',
                                  'Relativos, conjunciones o preposiciones',
                                  'Adjetivos calificativos',
                                  'Exclamativas indirectas'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «solo» no lleva tilde, ya sea que '
                             'funcione como adverbio (solamente) o como:',
                 'alternativas': ['Conjunción',
                                  'Sustantivo',
                                  'Pronombre',
                                  'Preposición',
                                  'Adjetivo'],
                 'correcta': 'E'},
                {'pregunta': 'Los demostrativos este, ese y aquel, con sus '
                             'femeninos y plurales, no llevan tilde, sea que '
                             'funcionen como pronombres o como:',
                 'alternativas': ['Preposiciones',
                                  'Adverbios',
                                  'Sustantivos',
                                  'Conjunciones',
                                  'Determinantes'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra «aún», con tilde, puede sustituirse '
                             'por «todavía», con valor temporal o:',
                 'alternativas': ['Concesivo',
                                  'Condicional',
                                  'Ponderativo o intensivo',
                                  'Adversativo',
                                  'Inclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra «aun», sin tilde, tiene valor '
                             'inclusivo-ponderativo (equivalente a '
                             '«incluso») o valor:',
                 'alternativas': ['Intensivo exclusivo',
                                  'Afirmativo',
                                  'Temporal',
                                  'Interrogativo',
                                  'Concesivo'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra que debe presentar tilde es: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Este', 'Solo', 'Libertad', 'Áspid', 'Fe'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras que se acentúan gráficamente en '
                             'la preantepenúltima sílaba (sobresdrújulas) '
                             'son: (Banco UNSAAC)',
                 'alternativas': ['Ideológico e imagíneselo',
                                  'Comuníquesenos y péndulo',
                                  'Infórmesenos e indíquesenos',
                                  'Laberíntico y premiésete',
                                  'Descuajeringado e iconográfico'],
                 'correcta': 'C'},
                {'pregunta': 'La palabra compuesta con acentuación adecuada '
                             'es: (Banco UNSAAC)',
                 'alternativas': ['Dime',
                                  'Arrepintiendose',
                                  'Pasapuré',
                                  'Comunmente',
                                  'Baloncesto'],
                 'correcta': 'C'},
                {'pregunta': 'La oración interrogativa indirecta con tilde '
                             'diacrítica es: (Banco UNSAAC)',
                 'alternativas': ['No sé quién preguntó por ti',
                                  'Esos jóvenes son como niños',
                                  '¿Dónde vendiste el reloj que te dio?',
                                  'El libro está donde lo dejaste',
                                  '¿Quién es ese joven con el inglés?'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra que en ningún caso lleva tilde es: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Aun', 'Fue', 'Te', 'De', 'Mi'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y ACENTO PROSÓDICO',
                      'items': ['La tilde, o acento gráfico, es el signo '
                                'diacrítico que marca la acentuación de una '
                                'palabra por escrito.',
                                'No todas las palabras tónicas se escriben '
                                'con tilde sobre su sílaba tónica.',
                                'El acento prosódico diferencia en la '
                                'pronunciación una sílaba determinada, '
                                'contrastándola con el resto.']},
                     {'titulo': 'REGLAS SEGÚN LA POSICIÓN DEL ACENTO',
                      'items': ['Las palabras monosilábicas nunca se '
                                'acentúan gráficamente, salvo en los casos '
                                'de tilde diacrítica.',
                                'Las palabras agudas u oxítonas tienen la '
                                'sílaba tónica en la última posición.',
                                'Las palabras agudas llevan tilde cuando '
                                'terminan en n, s o vocal.']},
                     {'titulo': 'ACENTUACIÓN DE SECUENCIAS VOCÁLICAS',
                      'items': ['Las palabras con diptongo se acentúan '
                                'gráficamente según las reglas generales de '
                                'acentuación (agudas, llanas, esdrújulas).',
                                'Cuando una palabra con diptongo debe '
                                'tildarse, la tilde se coloca sobre la vocal '
                                'abierta del diptongo (o la segunda, si '
                                'ambas son cerradas): rufián, recién.',
                                'Las palabras con triptongo también siguen '
                                'las reglas generales; cuando deben '
                                'tildarse, la tilde va siempre sobre la '
                                'vocal abierta: apreciáis, cambiéis.']},
                     {'titulo': 'TILDE DIACRÍTICA EN MONOSÍLABOS',
                      'items': ['La tilde diacrítica es la excepción a la '
                                'regla de los monosílabos; distingue '
                                'palabras tónicas de sus homónimas átonas.',
                                'Tú es pronombre personal (tú eres); tu sin '
                                'tilde es adjetivo posesivo (tu casa).',
                                'Él es pronombre personal (él es tímido); el '
                                'sin tilde es artículo determinante.']},
                     {'titulo': 'TILDE DIACRÍTICA EN INTERROGATIVOS Y '
                                'EXCLAMATIVOS',
                      'items': ['Las palabras qué, cuál, quién, cómo, cuán, '
                                'cuánto, cuándo, dónde y adónde llevan tilde '
                                'cuando son interrogativas o exclamativas.',
                                'Los interrogativos y exclamativos pueden ir '
                                'precedidos de una preposición sin dejar de '
                                'llevar tilde: ¿Por qué...?, ¿Hasta '
                                'cuándo...?',
                                'Existen interrogativas y exclamativas '
                                'indirectas que también llevan tilde: '
                                '«Preguntó qué tenía que hacer».']},
                     {'titulo': 'TILDE EN SOLO, DEMOSTRATIVOS Y AUN/AÚN',
                      'items': ['La palabra solo no lleva tilde, ya sea como '
                                'adverbio (equivalente a «solamente») o como '
                                'adjetivo.',
                                'Los demostrativos este, ese y aquel (con '
                                'femeninos y plurales) no llevan tilde, sea '
                                'como pronombres o como determinantes.',
                                'Aún, con tilde, puede sustituirse por '
                                '«todavía»: con valor temporal o '
                                'ponderativo-intensivo.']}]},
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
                {'titulo': '6.5 USO DE LAS MINÚSCULAS',
                 'items': ['Se escriben con {minúscula} los nombres de los '
                           'días de la semana, las estaciones del año y los '
                           'meses del año.',
                           'Se escriben con minúscula las {notas musicales}: '
                           'do, re, mi, fa, sol, la, si.',
                           'Se escriben con minúscula los nombres de '
                           '{vientos}, salvo que estén personificados en '
                           'poemas o relatos mitológicos.',
                           'Se escribe con minúscula {dios}, precedido de '
                           'determinante, cuando se refiere de modo genérico '
                           'al ser supremo o a divinidades politeístas.',
                           'Se escriben con minúscula los nombres de '
                           '{religiones} (budismo, cristianismo) y los '
                           '{gentilicios} (peruano, cusqueño).',
                           'Se escriben con minúscula los {tratamientos} '
                           '(usted, don, fray, san), salvo que se abrevien: '
                           'Ud., Sr., D.',
                           'Se escriben con minúscula los {títulos}, cargos '
                           'y nombres de dignidad: rey, papa, presidente, '
                           'alcalde.',
                           'Se escriben con minúscula los sustantivos que '
                           'designan {profesiones}, y los nombres de las '
                           '{lenguas}.',
                           'Se escriben con minúscula los nombres de '
                           '{hemisferios}, líneas imaginarias y polos '
                           'geográficos: el hemisferio sur, el ecuador.',
                           'Se escriben con minúscula los nombres de '
                           '{elementos químicos} y unidades de medida: '
                           'oxígeno, mercurio, metro.',
                           'Se escriben con minúscula los nombres de los '
                           '{principios activos} de medicamentos: '
                           'amoxicilina, ibuprofeno; los nombres comerciales '
                           'sí llevan mayúscula.',
                           'Se escriben con minúscula los nombres de las '
                           '{monedas}: soles, dólares, euros.']},
                {'titulo': '6.6 ACRÓNIMOS: SIGLAS QUE SE VUELVEN PALABRAS',
                 'items': ['El {acrónimo} es una sigla cuya grafía permite '
                           'leerla {secuencialmente} (no deletreada), como '
                           'OTAN o UNESCO.',
                           'Cuando el acrónimo se convierte en nombre '
                           'propio, mantiene la mayúscula {inicial}: '
                           'Mercosur, Unicef.',
                           'Cuando el acrónimo se convierte en nombre común, '
                           'se escribe enteramente en {minúsculas}: ovni, '
                           'láser, radar, uci.',
                           'Las siglas que deben {deletrearse} al leerse '
                           'mantienen siempre su escritura en mayúsculas: '
                           'FBI, DDT.',
                           'Las expresiones desarrolladas de siglas llevan '
                           'mayúscula si nombran una {institución} (Banco '
                           'Central Europeo), y minúscula si son expresiones '
                           'comunes (documento nacional de identidad).']}],
  'cuadros': [{'titulo': '6.2 SIGLAS FRENTE A ABREVIATURAS',
               'encabezados': ['Tipo', 'Lleva puntos', 'Ejemplo'],
               'filas': [['{Siglas}', '{No}', 'PNP, DNI'],
                         ['{Abreviaturas}', '{Sí}', 'pág., Sr.']]}],
  'preguntas': [{'pregunta': 'La escritura enteramente en mayúsculas es '
                             'propia de las siglas, los números romanos y:',
                 'alternativas': ['Los adjetivos calificativos',
                                  'Las preposiciones',
                                  'Los verbos irregulares',
                                  'Los artículos',
                                  'Los textos cortos informativos'],
                 'correcta': 'E'},
                {'pregunta': 'El uso combinado de minúsculas y mayúsculas '
                             'dentro de una misma palabra debe:',
                 'alternativas': ['Prohibirse en las siglas',
                                  'Usarse en todo texto formal',
                                  'Evitarse en la escritura normal',
                                  'Fomentarse siempre',
                                  'Aplicarse en cartas oficiales'],
                 'correcta': 'C'},
                {'pregunta': 'Las siglas se escriben con mayúscula:',
                 'alternativas': ['Todas las letras que las componen',
                                  'Solo las consonantes',
                                  'Solo la primera letra',
                                  'Solo las vocales',
                                  'Ninguna letra en particular'],
                 'correcta': 'A'},
                {'pregunta': 'Las siglas, a diferencia de las abreviaturas, '
                             'se escriben:',
                 'alternativas': ['Solo entre comillas',
                                  'Con guion final',
                                  'Solo en cursiva',
                                  'Con puntos',
                                  'Sin puntos'],
                 'correcta': 'E'},
                {'pregunta': 'Las abreviaturas, a diferencia de las siglas, '
                             'se escriben:',
                 'alternativas': ['Solo en números',
                                  'Sin mayúsculas nunca',
                                  'Con puntos',
                                  'Sin puntos',
                                  'En cursiva obligatoria'],
                 'correcta': 'C'},
                {'pregunta': 'Los nombres latinos de especies, como «Homo '
                             'sapiens», se escriben con mayúscula inicial y:',
                 'alternativas': ['Subrayados',
                                  'Entre comillas',
                                  'En negrita',
                                  'Entre paréntesis',
                                  'En cursiva'],
                 'correcta': 'E'},
                {'pregunta': 'La palabra «Dios» se escribe con mayúscula '
                             'cuando se usa:',
                 'alternativas': ['Solo en textos religiosos católicos',
                                  'Nunca en español',
                                  'Solo en mayúscula total',
                                  'Sin artículo, como nombre propio del ser '
                                  'supremo monoteísta',
                                  'Con artículo, en sentido genérico'],
                 'correcta': 'D'},
                {'pregunta': 'Si un dígrafo como «ch» o «ll» aparece al '
                             'inicio de una palabra con mayúscula, se '
                             'escribe en mayúscula:',
                 'alternativas': ['Solo la segunda letra',
                                  'Todo en minúscula',
                                  'Ninguna letra',
                                  'Ambas letras del dígrafo',
                                  'Solo la primera letra'],
                 'correcta': 'E'},
                {'pregunta': 'La mayúscula de las letras i y j, a diferencia '
                             'de su forma minúscula:',
                 'alternativas': ['Lleva doble punto',
                                  'Lleva tilde obligatoria',
                                  'Carece del punto sobrescrito',
                                  'No existe en mayúscula',
                                  'Se escribe en cursiva siempre'],
                 'correcta': 'C'},
                {'pregunta': 'El fenómeno por el cual un nombre común '
                             'reemplaza completamente a un nombre propio se '
                             'llama:',
                 'alternativas': ['Metonimia',
                                  'Sinécdoque',
                                  'Antonomasia',
                                  'Hipérbole',
                                  'Personificación'],
                 'correcta': 'C'},
                {'pregunta': 'El fenómeno que atribuye rasgos humanos a '
                             'conceptos abstractos, como «la Muerte», se '
                             'llama:',
                 'alternativas': ['Antonomasia',
                                  'Metáfora exclusiva',
                                  'Personificación',
                                  'Ironía',
                                  'Comparación'],
                 'correcta': 'C'},
                {'pregunta': 'Se escribe con mayúscula la primera palabra de '
                             'un escrito y la que va después de:',
                 'alternativas': ['Un punto',
                                  'Un guion',
                                  'Una coma',
                                  'Un paréntesis',
                                  'Unas comillas'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra que sigue a los puntos suspensivos, '
                             'cuando estos cierran un enunciado, se escribe '
                             'con:',
                 'alternativas': ['Negrita',
                                  'Minúscula siempre',
                                  'Comillas',
                                  'Cursiva obligatoria',
                                  'Mayúscula'],
                 'correcta': 'E'},
                {'pregunta': 'Si los puntos suspensivos NO cierran el '
                             'enunciado, la palabra siguiente se escribe '
                             'con:',
                 'alternativas': ['Cursiva',
                                  'Negrita obligatoria',
                                  'Minúscula',
                                  'Subrayado',
                                  'Mayúscula'],
                 'correcta': 'C'},
                {'pregunta': 'Después de dos puntos se escribe mayúscula '
                             'cuando anuncian el inicio de una unidad '
                             'independiente, como en:',
                 'alternativas': ['Una lista de compras',
                                  'Un ejemplo cualquiera',
                                  'El saludo de una carta',
                                  'Una cita textual breve',
                                  'Una enumeración simple'],
                 'correcta': 'C'},
                {'pregunta': 'Los documentos jurídicos que usan mayúscula '
                             'total suelen presentar palabras como:',
                 'alternativas': ['Saludos',
                                  'Atentamente',
                                  'Estimado',
                                  'Considerando',
                                  'CERTIFICA'],
                 'correcta': 'E'},
                {'pregunta': 'La mayúscula inicial marca y delimita, entre '
                             'otras cosas:',
                 'alternativas': ['Las conjunciones',
                                  'Los nombres propios',
                                  'Los artículos indeterminados',
                                  'Los verbos conjugados',
                                  'Las preposiciones'],
                 'correcta': 'B'},
                {'pregunta': '«El Salvador» usado para referirse a '
                             'Jesucristo es un ejemplo de:',
                 'alternativas': ['Personificación',
                                  'Sinécdoque',
                                  'Metáfora pura',
                                  'Antonomasia',
                                  'Ironía'],
                 'correcta': 'D'},
                {'pregunta': 'Las siglas «RAE» y «AVE» ejemplifican el uso '
                             'de mayúsculas para:',
                 'alternativas': ['Documentos jurídicos',
                                  'Cartas formales',
                                  'Números romanos',
                                  'Formar e identificar siglas',
                                  'Nombres propios de personas'],
                 'correcta': 'D'},
                {'pregunta': 'Los números romanos, como «XXI», se escriben:',
                 'alternativas': ['Enteramente en mayúsculas',
                                  'En cursiva obligatoria',
                                  'Entre comillas',
                                  'En minúscula',
                                  'Con tilde'],
                 'correcta': 'A'},
                {'pregunta': 'Los nombres de los días de la semana, las '
                             'estaciones del año y los meses se escriben '
                             'con:',
                 'alternativas': ['Mayúscula solo en los meses',
                                  'Mayúscula solo en las estaciones',
                                  'Mayúscula inicial siempre',
                                  'Minúscula',
                                  'Versalitas'],
                 'correcta': 'D'},
                {'pregunta': 'Las notas musicales (do, re, mi, fa, sol, la, '
                             'si) se escriben con:',
                 'alternativas': ['Minúscula',
                                  'Cursiva obligatoria',
                                  'Versalitas obligatorias',
                                  'Mayúscula inicial',
                                  'Mayúscula solo «sol», por ser también '
                                  'astro'],
                 'correcta': 'A'},
                {'pregunta': 'La palabra «dios», precedida de determinante y '
                             'usada de modo genérico o referida a '
                             'divinidades politeístas, se escribe con:',
                 'alternativas': ['Cursiva',
                                  'Mayúscula solo en textos religiosos',
                                  'Mayúscula inicial siempre',
                                  'Versalitas',
                                  'Minúscula'],
                 'correcta': 'E'},
                {'pregunta': 'Los tratamientos como «usted», «don» o «fray» '
                             'se escriben con minúscula, salvo cuando:',
                 'alternativas': ['Se refieren a un rey',
                                  'Van al inicio de un párrafo',
                                  'Se abrevian (Ud., Sr., D.)',
                                  'Aparecen en un título',
                                  'Van seguidos de nombre propio'],
                 'correcta': 'C'},
                {'pregunta': 'Los títulos, cargos y nombres de dignidad, '
                             'como «rey», «papa» o «presidente», se escriben '
                             'con:',
                 'alternativas': ['Minúscula',
                                  'Mayúscula solo «papa»',
                                  'Versalitas',
                                  'Cursiva',
                                  'Mayúscula inicial siempre'],
                 'correcta': 'A'},
                {'pregunta': 'Los nombres de elementos químicos y unidades '
                             'de medida, como «oxígeno» o «metro», se '
                             'escriben con:',
                 'alternativas': ['Mayúscula inicial',
                                  'Versalitas',
                                  'Minúscula',
                                  'Mayúscula en unidades exclusivamente',
                                  'Cursiva obligatoria'],
                 'correcta': 'C'},
                {'pregunta': 'Los principios activos de medicamentos, como '
                             '«ibuprofeno», se escriben con minúscula, a '
                             'diferencia de:',
                 'alternativas': ['Las contraindicaciones',
                                  'Los nombres comerciales registrados, que '
                                  'llevan mayúscula inicial',
                                  'Las dosis, que llevan mayúscula',
                                  'Las vías de administración',
                                  'Los efectos secundarios'],
                 'correcta': 'B'},
                {'pregunta': 'Una sigla cuya grafía permite leerla '
                             'secuencialmente, como OTAN o UNESCO, se llama:',
                 'alternativas': ['Acrónimo',
                                  'Epónimo',
                                  'Abreviatura',
                                  'Sigla deletreada',
                                  'Símbolo'],
                 'correcta': 'A'},
                {'pregunta': 'Cuando un acrónimo se convierte en nombre '
                             'común de uso corriente, se escribe:',
                 'alternativas': ['Enteramente en minúsculas',
                                  'Con versalitas',
                                  'Con guion intermedio',
                                  'Con mayúscula inicial',
                                  'Enteramente en mayúsculas'],
                 'correcta': 'A'},
                {'pregunta': 'Las siglas que deben deletrearse al leerse, '
                             'como FBI o DDT, mantienen siempre su '
                             'escritura:',
                 'alternativas': ['En minúsculas',
                                  'Con la inicial en mayúscula',
                                  'En mayúsculas',
                                  'En cursiva',
                                  'Con puntos entre letras'],
                 'correcta': 'C'},
                {'pregunta': 'La expresión desarrollada «documento nacional '
                             'de identidad» (DNI) se escribe con minúsculas '
                             'por ser una expresión:',
                 'alternativas': ['Un título oficial',
                                  'Común',
                                  'El nombre de una institución',
                                  'Un tratamiento',
                                  'Un acrónimo ya lexicalizado'],
                 'correcta': 'B'},
                {'pregunta': 'El enunciado con uso correcto de las letras '
                             'mayúsculas es:',
                 'alternativas': ['La ropa de Inés me recuerda la Edad Media',
                                  'Carlos Miguel trabaja en el ministerio de '
                                  'Salud',
                                  'Juan Carlos conduce su vida con Filosofía',
                                  'Mi hermana Marianela se fue a tomar el '
                                  'Sol',
                                  'Daniel, mi primo, radica en el Salvador'],
                 'correcta': 'A'},
                {'pregunta': 'La frase que denota uso adecuado de las '
                             'mayúsculas es:',
                 'alternativas': ['El Mar Negro',
                                  'El Lago de Puno',
                                  'La Bahía de Acapulco',
                                  'La ciudad de La Habana',
                                  'El Nevado Pastoruri'],
                 'correcta': 'D'},
                {'pregunta': 'En la oración «La amazonía es la región más '
                             'grande del perú», la cantidad de palabras que '
                             'se debe escribir con mayúscula es:',
                 'alternativas': ['Uno', 'Cero', 'Tres', 'Cuatro', 'Dos'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CONSIDERACIONES BÁSICAS',
                      'items': ['La escritura enteramente en mayúsculas es '
                                'propia de las siglas, los números romanos y '
                                'textos cortos informativos.',
                                'El uso combinado de minúsculas y mayúsculas '
                                'dentro de una palabra debe evitarse en la '
                                'escritura normal.',
                                'La mayúscula inicial marca el inicio de '
                                'enunciados, párrafos y delimita los nombres '
                                'propios.']},
                     {'titulo': 'SIGLAS Y NOMBRES CIENTÍFICOS',
                      'items': ['Las siglas se escriben con mayúscula todas '
                                'las letras que las componen, como PNP o '
                                'DNI.',
                                'Las siglas se escriben sin puntos, mientras '
                                'que las abreviaturas sí los llevan, como '
                                'pág. o Sr.',
                                'Los nombres latinos de especies, como Homo '
                                'sapiens, se escriben con mayúscula inicial '
                                'y en cursiva.']},
                     {'titulo': 'CASOS ESPECIALES DE MAYÚSCULA INICIAL',
                      'items': ['Si los dígrafos ch, ll, gu o qu aparecen al '
                                'inicio de una palabra con mayúscula, solo '
                                'la primera letra se escribe en mayúscula, '
                                'como en «Chávez» o «Quito».',
                                'La mayúscula de las letras i y j carece del '
                                'punto sobrescrito característico de su '
                                'forma minúscula.',
                                'La antonomasia es el fenómeno por el cual '
                                'un nombre común reemplaza a un nombre '
                                'propio, como «el Salvador» por '
                                'Jesucristo.']},
                     {'titulo': 'LA MAYÚSCULA CONDICIONADA POR LA PUNTUACIÓN',
                      'items': ['Se escribe con mayúscula la primera palabra '
                                'de un escrito y la que va después de un '
                                'punto.',
                                'Se escribe con mayúscula la palabra que '
                                'sigue a los puntos suspensivos cuando estos '
                                'cierran un enunciado.',
                                'Si los puntos suspensivos no cierran el '
                                'enunciado, la palabra siguiente se escribe '
                                'con minúscula.']},
                     {'titulo': 'USO DE LAS MINÚSCULAS',
                      'items': ['Se escriben con minúscula los nombres de '
                                'los días de la semana, las estaciones del '
                                'año y los meses del año.',
                                'Se escriben con minúscula las notas '
                                'musicales: do, re, mi, fa, sol, la, si.',
                                'Se escriben con minúscula los nombres de '
                                'vientos, salvo que estén personificados en '
                                'poemas o relatos mitológicos.']},
                     {'titulo': 'ACRÓNIMOS: SIGLAS QUE SE VUELVEN PALABRAS',
                      'items': ['El acrónimo es una sigla cuya grafía '
                                'permite leerla secuencialmente (no '
                                'deletreada), como OTAN o UNESCO.',
                                'Cuando el acrónimo se convierte en nombre '
                                'propio, mantiene la mayúscula inicial: '
                                'Mercosur, Unicef.',
                                'Cuando el acrónimo se convierte en nombre '
                                'común, se escribe enteramente en '
                                'minúsculas: ovni, láser, radar, uci.']}]},
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
                {'titulo': '7.4 LOS DOS PUNTOS',
                 'items': ['Los dos puntos se usan en {enumeraciones}: «Las '
                           'regiones del Imperio incaico fueron cuatro: '
                           'Antisuyo, Collasuyo, Chinchaysuyo y Contisuyo».',
                           'Los dos puntos preceden al {discurso directo}: '
                           "«Francisco Bolognesi expresó: 'Tengo deberes "
                           "sagrados que cumplir...'».",
                           'Los dos puntos yuxtapuestos indican '
                           '{causa-efecto}: «Se ha quedado sin trabajo: no '
                           'podrá ir de vacaciones».',
                           'Los dos puntos yuxtapuestos también indican '
                           '{conclusión} o resumen: «El arbitraje fue '
                           'injusto...: al final se perdió el partido».',
                           'Los dos puntos se usan tras {conectores '
                           'discursivos} como «ahora bien», «dicho de otro '
                           'modo», «a saber».',
                           'Los dos puntos se usan tras {vocativos formales} '
                           'en cartas: «Estimado amigo:», «Distinguidos '
                           'colegas:».',
                           'En textos {jurídicos} y administrativos '
                           '(decretos, certificados), tras los dos puntos, '
                           'la siguiente palabra va en mayúsculas: '
                           'CERTIFICA:']},
                {'titulo': '7.5 LOS PUNTOS SUSPENSIVOS',
                 'items': ['Los puntos suspensivos indican {suspensión} u '
                           'omisión del discurso: «El caso es que si '
                           'lloviese…».',
                           'Los puntos suspensivos indican suspensión con '
                           'fines {expresivos}, como duda o temor: «El niño '
                           'dice que él no ha roto el jarrón…».',
                           'Los puntos suspensivos señalan la omisión de una '
                           'parte del texto por sobrentendida, como en '
                           '{refranes}: «Más sabe el diablo por viejo que…».',
                           'Los puntos suspensivos permiten {insinuar}, '
                           'evitando su reproducción, expresiones '
                           'malsonantes.',
                           'Los puntos suspensivos se emplean al final de '
                           'enumeraciones en lugar de {etcétera}: «Puedes '
                           'leer, ver televisión, oír música…».',
                           'Entre corchetes o paréntesis, los puntos '
                           'suspensivos indican la {supresión} de una parte '
                           'de una cita textual.']},
                {'titulo': '7.6 EL PARÉNTESIS',
                 'items': ['El paréntesis se usa para aislar {incisos}: «Las '
                           'asambleas (la primera y última) se celebran en '
                           'el salón de actos».',
                           'El paréntesis aísla otros elementos '
                           '{intercalados}, como fechas o datos: «El año de '
                           'su nacimiento (1616) es el mismo en que murió '
                           'Cervantes».',
                           'El paréntesis encierra {acotaciones} de '
                           'personajes en obras teatrales: «JORGE. '
                           '(Golpeando con el bastón)».',
                           'El paréntesis, junto con puntos suspensivos, '
                           'indica la {omisión} de parte de una cita '
                           'textual: (…).']},
                {'titulo': '7.7 LAS COMILLAS',
                 'items': ['Las comillas se usan en {citas textuales} y '
                           "reproducción de pensamientos: «'Sobreviven los "
                           "que se adaptan mejor al cambio' dijo Charles "
                           'Darwin».',
                           'Las comillas marcan el carácter {especial} de '
                           'una palabra o expresión, como ironía: «Siempre '
                           "dice que las 'tortas' de esa pastelería están "
                           'riquísimas».',
                           'Las comillas se usan en usos {metalingüísticos}, '
                           'para mencionar una palabra como tal: «La palabra '
                           "'cándida' lleva tilde por ser esdrújula».",
                           'Las comillas encierran {expresiones '
                           'denominativas}, como títulos de artículos: «Su '
                           "artículo 'Importancia del lenguaje...' se "
                           'publicó en El Comercio».',
                           'Las comillas suelen encerrar {apodos} y alias '
                           'intercalados entre nombre y apellido: «Ernesto '
                           "'Che' Guevara»."]},
                {'titulo': '7.8 LA RAYA',
                 'items': ['La raya se usa para separar {incisos}: «Para él '
                           'la fidelidad —cualidad que valoraba por encima '
                           'de cualquier otra— era algo sagrado».',
                           'La raya enmarca las expresiones de un {narrador} '
                           "o transcriptor: «'Es imprescindible —señaló el "
                           "ministro— que se refuercen los controles'».",
                           'La raya se usa en {diálogos}, marcando la '
                           'intervención de cada personaje: «—¿Cómo se llama '
                           'Ud.? —Paco.»',
                           'La raya se usa en {enumeraciones} en forma de '
                           'lista, como viñeta: «Las funciones del lenguaje '
                           'son: — expresiva, — fática, — conativa...».',
                           'La raya puede encerrar {incisos dentro de otros '
                           'incisos}: «(la bibliografía existente —incluso '
                           'en español— es bastante extensa)».']},
                {'titulo': '7.9 INTERROGACIÓN Y EXCLAMACIÓN',
                 'items': ['Los signos de interrogación y exclamación se '
                           'usan en {interrogaciones} y exclamaciones '
                           'directas: «¿Cuándo vendrás?»',
                           'Estos signos pueden {omitirse} en títulos de '
                           'obras, capítulos o secciones de un texto: «Cómo '
                           'escribir bien español».',
                           'Las oraciones exclamativas pueden estar formadas '
                           'por {interjecciones} (¡Ay!), onomatopeyas '
                           '(¡Chist!) o vocativos (¡Niños!).',
                           'El signo de apertura (¿ o ¡) se coloca donde '
                           'comienza la pregunta o exclamación, no '
                           'necesariamente al inicio de la {oración}: '
                           '«Martha, ¿sabes ya cuándo vendrás?»',
                           'Estos signos se usan en enunciados aseverativos '
                           'que preceden a {apéndices confirmativos}: «El '
                           'martes es su onomástico, ¿no?»',
                           'Si concurren varias preguntas o exclamaciones '
                           '{breves} y consecutivas, cada una se escribe con '
                           'su propio signo de apertura y cierre: «¿Quién '
                           'era? ¿De dónde vino?»']}],
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
                 'alternativas': ['Comprensión',
                                  'Pronunciación exclusiva',
                                  'Eliminación',
                                  'Traducción',
                                  'Memorización'],
                 'correcta': 'A'},
                {'pregunta': 'Una función de los signos de puntuación es '
                             'indicar los límites de:',
                 'alternativas': ['Los morfemas',
                                  'Las sílabas',
                                  'Las palabras sueltas',
                                  'Las unidades discursivas',
                                  'Los fonemas'],
                 'correcta': 'D'},
                {'pregunta': 'La función que indica si un enunciado es '
                             'interrogativo o exclamativo es la función de:',
                 'alternativas': ['Modalidad del enunciado',
                                  'Cohesión',
                                  'Omisión',
                                  'Referencia',
                                  'Límites discursivos'],
                 'correcta': 'A'},
                {'pregunta': 'El punto se usa correctamente en:',
                 'alternativas': ['Las abreviaturas',
                                  'Los eslóganes',
                                  'Los títulos de libros',
                                  'Las dedicatorias',
                                  'Las direcciones electrónicas'],
                 'correcta': 'A'},
                {'pregunta': 'El punto se usa también en:',
                 'alternativas': ['Los nombres de autor en portadas',
                                  'Fechas y horas',
                                  'Los eslóganes publicitarios',
                                  'Las direcciones web',
                                  'Los títulos de obras de arte'],
                 'correcta': 'B'},
                {'pregunta': 'NO se escribe punto al final de:',
                 'alternativas': ['Una abreviatura',
                                  'Una hora exacta',
                                  'Los títulos y subtítulos de libros',
                                  'Un párrafo normal',
                                  'Una fecha completa'],
                 'correcta': 'C'},
                {'pregunta': 'Los nombres de autor en portadas, prólogos o '
                             'firmas de documentos se escriben:',
                 'alternativas': ['En mayúscula total',
                                  'Con punto final',
                                  'Sin punto final',
                                  'Subrayados siempre',
                                  'Entre comillas obligatorias'],
                 'correcta': 'C'},
                {'pregunta': 'Las dedicatorias, como «Para William», se '
                             'escriben:',
                 'alternativas': ['Entre paréntesis',
                                  'Con doble punto',
                                  'Con punto final',
                                  'Sin punto final',
                                  'En cursiva obligatoria'],
                 'correcta': 'D'},
                {'pregunta': 'Los eslóganes publicitarios, por regla '
                             'general, se escriben:',
                 'alternativas': ['Entre comillas siempre',
                                  'Solo en mayúsculas',
                                  'Con coma final',
                                  'Con punto final',
                                  'Sin punto final'],
                 'correcta': 'E'},
                {'pregunta': 'Las direcciones electrónicas, como '
                             'www.unsaac.edu.pe, se escriben:',
                 'alternativas': ['Con punto final obligatorio',
                                  'Entre corchetes',
                                  'Con guion final',
                                  'Sin punto final',
                                  'Solo en mayúsculas'],
                 'correcta': 'D'},
                {'pregunta': 'La coma que intercala información aclaratoria '
                             'dentro del enunciado es la coma:',
                 'alternativas': ['Hiperbática',
                                  'Vocativa',
                                  'Incidental',
                                  'Enumerativa',
                                  'Elíptica'],
                 'correcta': 'C'},
                {'pregunta': 'La coma que separa el nombre de la persona a '
                             'quien nos dirigimos es la coma:',
                 'alternativas': ['Incidental',
                                  'Vocativa',
                                  'Enumerativa',
                                  'Distributiva',
                                  'Explicativa'],
                 'correcta': 'B'},
                {'pregunta': 'En «Eduardo, no quiero que salgas tan tarde», '
                             'la coma usada es la coma:',
                 'alternativas': ['Enumerativa',
                                  'Elíptica',
                                  'Hiperbática',
                                  'Incidental',
                                  'Vocativa'],
                 'correcta': 'E'},
                {'pregunta': 'En «La mansión, abandonada, se convirtió en '
                             'refugio», la coma usada es la coma:',
                 'alternativas': ['Distributiva',
                                  'Incidental',
                                  'Vocativa',
                                  'Final',
                                  'Enumerativa'],
                 'correcta': 'B'},
                {'pregunta': 'El punto se usa en abreviaturas como:',
                 'alternativas': ['ONU', 'AFP', 'DNI', 'Sra.', 'RAE'],
                 'correcta': 'D'},
                {'pregunta': 'Las enumeraciones en forma de lista, como en '
                             'un examen de opción múltiple, se escriben:',
                 'alternativas': ['Con punto final en cada ítem '
                                  'obligatoriamente',
                                  'Sin punto final en cada ítem',
                                  'En un solo párrafo continuo',
                                  'Solo con coma',
                                  'Solo con punto y coma'],
                 'correcta': 'B'},
                {'pregunta': 'Los pies de imagen y cabeceras de cuadros, '
                             'cuando son breves, se escriben:',
                 'alternativas': ['Siempre con punto',
                                  'Entre comillas obligatorias',
                                  'En mayúscula total',
                                  'Generalmente sin punto',
                                  'Con dos puntos finales'],
                 'correcta': 'D'},
                {'pregunta': 'Los signos de puntuación señalan el carácter '
                             'especial de fragmentos como:',
                 'alternativas': ['Solo los números',
                                  'Solo los títulos',
                                  'Solo los nombres propios',
                                  'Citas e incisos',
                                  'Solo las siglas'],
                 'correcta': 'D'},
                {'pregunta': '«A quien madruga…» ejemplifica la función de '
                             'los signos de puntuación de indicar:',
                 'alternativas': ['Una cita textual',
                                  'Límites discursivos',
                                  'La omisión de una parte del enunciado',
                                  'Modalidad interrogativa',
                                  'Una fecha'],
                 'correcta': 'C'},
                {'pregunta': 'El punto se usa correctamente después de una '
                             'hora como:',
                 'alternativas': ['17-30',
                                  '1730 sin separador',
                                  'Diecisiete treinta escrito',
                                  '17.30',
                                  '17:30 con coma'],
                 'correcta': 'D'},
                {'pregunta': 'Los dos puntos que anteceden a una '
                             'enumeración, como en «Las regiones del Imperio '
                             'incaico fueron cuatro: Antisuyo, '
                             'Collasuyo...», cumplen la función de:',
                 'alternativas': ['Separar oraciones independientes',
                                  'Indicar duda',
                                  'Cerrar el enunciado',
                                  'Marcar una pausa breve',
                                  'Introducir una enumeración'],
                 'correcta': 'E'},
                {'pregunta': 'Los dos puntos que preceden a una cita en '
                             'discurso directo, como en «Francisco Bolognesi '
                             "expresó: '...'», cumplen la función de:",
                 'alternativas': ['Enumerar elementos',
                                  'Introducir el discurso directo',
                                  'Indicar causa-efecto',
                                  'Cerrar una lista',
                                  'Separar vocativos'],
                 'correcta': 'B'},
                {'pregunta': 'En «Se ha quedado sin trabajo: no podrá ir de '
                             'vacaciones», los dos puntos indican una '
                             'relación de:',
                 'alternativas': ['Conector discursivo',
                                  'Discurso directo',
                                  'Vocativo formal',
                                  'Enumeración',
                                  'Causa-efecto'],
                 'correcta': 'E'},
                {'pregunta': 'Tras un vocativo formal en una carta, como '
                             '«Estimado amigo:», se usa el signo de:',
                 'alternativas': ['Puntos suspensivos',
                                  'Punto y coma',
                                  'Dos puntos',
                                  'Punto final',
                                  'Coma'],
                 'correcta': 'C'},
                {'pregunta': 'En textos jurídicos y administrativos, como '
                             'decretos o certificados, tras los dos puntos '
                             '(CERTIFICA:) la palabra siguiente se escribe:',
                 'alternativas': ['Enteramente en mayúsculas',
                                  'En cursiva',
                                  'Con minúscula',
                                  'Entre comillas',
                                  'Subrayada'],
                 'correcta': 'A'},
                {'pregunta': 'Los puntos suspensivos que indican duda o '
                             'temor en el discurso, como en «El niño dice '
                             'que él no ha roto el jarrón…», tienen un fin:',
                 'alternativas': ['Jurídico',
                                  'Enumerativo',
                                  'Aclaratorio',
                                  'Expresivo',
                                  'Enciclopédico'],
                 'correcta': 'D'},
                {'pregunta': 'Los puntos suspensivos usados al final de una '
                             'enumeración pueden sustituir a la palabra:',
                 'alternativas': ['Asimismo',
                                  'También',
                                  'Incluso',
                                  'Además',
                                  'Etcétera'],
                 'correcta': 'E'},
                {'pregunta': 'Entre paréntesis o corchetes, los puntos '
                             'suspensivos (…) indican, dentro de una cita '
                             'textual, la:',
                 'alternativas': ['Continuación del texto',
                                  'Duda del autor',
                                  'Corrección de un error',
                                  'Repetición de una idea',
                                  'Supresión de una parte del texto'],
                 'correcta': 'E'},
                {'pregunta': 'El paréntesis usado para aislar un dato '
                             'intercalado, como una fecha, cumple la función '
                             'de:',
                 'alternativas': ['Marcar una pregunta',
                                  'Introducir un discurso directo',
                                  'Cerrar una enumeración',
                                  'Indicar causa-efecto',
                                  'Aislar elementos intercalados'],
                 'correcta': 'E'},
                {'pregunta': 'En una obra teatral, el paréntesis que indica '
                             'los gestos o acciones de un personaje, como '
                             '«(Golpeando con el bastón)», se llama:',
                 'alternativas': ['Réplica',
                                  'Discurso',
                                  'Diálogo',
                                  'Monólogo',
                                  'Acotación'],
                 'correcta': 'E'},
                {'pregunta': 'Las comillas usadas para reproducir '
                             'textualmente el pensamiento de un autor, como '
                             'una cita de Charles Darwin, cumplen la función '
                             'de encerrar:',
                 'alternativas': ['Apodos',
                                  'Enumeraciones',
                                  'Fechas',
                                  'Citas textuales',
                                  'Vocativos'],
                 'correcta': 'D'},
                {'pregunta': 'Las comillas usadas para marcar el carácter '
                             'especial o irónico de una palabra, como en '
                             "«sus 'negocios'», cumplen un uso:",
                 'alternativas': ['De cita textual',
                                  'De apodo',
                                  'De sentido especial o irónico',
                                  'Denominativo',
                                  'Metalingüístico'],
                 'correcta': 'C'},
                {'pregunta': 'Las comillas que encierran una palabra '
                             'mencionada como tal, como en «La palabra '
                             "'cándida' lleva tilde por ser esdrújula», "
                             'cumplen un uso:',
                 'alternativas': ['Denominativo',
                                  'Irónico',
                                  'De apodo',
                                  'Metalingüístico',
                                  'De cita'],
                 'correcta': 'D'},
                {'pregunta': 'Los apodos o alias intercalados entre el '
                             'nombre y el apellido de una persona, como en '
                             "«Ernesto 'Che' Guevara», se escriben entre:",
                 'alternativas': ['Guiones',
                                  'Rayas',
                                  'Comillas',
                                  'Paréntesis',
                                  'Corchetes'],
                 'correcta': 'C'},
                {'pregunta': 'La raya usada para separar un inciso dentro de '
                             'una oración, como en «la fidelidad —cualidad '
                             'que valoraba— era sagrada», cumple la función '
                             'de:',
                 'alternativas': ['Separar incisos',
                                  'Marcar una pregunta',
                                  'Introducir un diálogo',
                                  'Enumerar elementos',
                                  'Cerrar una cita'],
                 'correcta': 'A'},
                {'pregunta': 'La raya que enmarca las palabras de un '
                             'narrador o transcriptor dentro de una cita, '
                             "como en «'Es imprescindible —señaló el "
                             "ministro— que...'», tiene función:",
                 'alternativas': ['Enumerativa',
                                  'De narrador o transcriptor',
                                  'De apodo',
                                  'De vocativo',
                                  'De cierre de cita'],
                 'correcta': 'B'},
                {'pregunta': 'En los diálogos escritos, cada intervención de '
                             'un personaje se marca con el signo de:',
                 'alternativas': ['Los puntos suspensivos',
                                  'Los dos puntos',
                                  'El paréntesis',
                                  'Las comillas',
                                  'La raya'],
                 'correcta': 'E'},
                {'pregunta': 'En una enumeración presentada en forma de '
                             'lista o viñetas, se puede usar el signo de:',
                 'alternativas': ['Los dos puntos exclusivamente',
                                  'Los puntos suspensivos',
                                  'La raya',
                                  'Las comillas',
                                  'El paréntesis'],
                 'correcta': 'C'},
                {'pregunta': 'Los signos de interrogación y exclamación se '
                             'pueden omitir en:',
                 'alternativas': ['Cualquier oración exclamativa',
                                  'Diálogos',
                                  'Títulos de obras, capítulos o secciones '
                                  'de un texto',
                                  'Enumeraciones',
                                  'Citas textuales'],
                 'correcta': 'C'},
                {'pregunta': 'Las oraciones exclamativas pueden estar '
                             'constituidas, entre otros elementos, por '
                             'interjecciones y:',
                 'alternativas': ['Onomatopeyas',
                                  'Artículos exclusivamente',
                                  'Conjunciones exclusivamente',
                                  'Adverbios exclusivamente',
                                  'Preposiciones exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'En la oración «Martha, ¿sabes ya cuándo '
                             'vendrás?», el signo de apertura de '
                             'interrogación se coloca:',
                 'alternativas': ['Antes del vocativo siempre',
                                  'Donde comienza la pregunta, no '
                                  'necesariamente al inicio',
                                  'Después del vocativo siempre',
                                  'Al final de la oración',
                                  'Al inicio absoluto de la oración'],
                 'correcta': 'B'},
                {'pregunta': 'En un enunciado aseverativo seguido de un '
                             'apéndice confirmativo, como «El martes es su '
                             'onomástico, ¿no?», el apéndice se escribe '
                             'entre signos de:',
                 'alternativas': ['Rayas',
                                  'Comillas',
                                  'Interrogación',
                                  'Puntos suspensivos',
                                  'Exclamación'],
                 'correcta': 'C'},
                {'pregunta': 'El enunciado que presenta puntuación correcta, '
                             'es:',
                 'alternativas': ['Entre 1939 y 1945 se desarrolló la '
                                  'Segunda Guerra Mundial',
                                  'Entre 1939 y 1945, se desarrolló la '
                                  'Segunda Guerra Mundial',
                                  'Entre 1939 y 1945, se desarrolló, la '
                                  'Segunda Guerra Mundial',
                                  'Entre, 1939 y 1945 se desarrolló la '
                                  'Segunda Guerra Mundial',
                                  'Entre 1939 y 1945 se desarrolló, la '
                                  'Segunda Guerra Mundial'],
                 'correcta': 'A'},
                {'pregunta': 'Después de la expresión «Estimado cliente», en '
                             'el encabezado de una carta formal, el signo '
                             'que le corresponde es:',
                 'alternativas': ['Punto y coma',
                                  'Punto',
                                  'Punto y aparte',
                                  'Dos puntos',
                                  'Puntos suspensivos'],
                 'correcta': 'D'},
                {'pregunta': 'La coma es utilizada de manera pertinente en: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Cusco, 25 de febrero de 2018',
                                  'Carlos estudia, en la universidad',
                                  'Ellos, trabajan',
                                  'Lo olvidó, lamentablemente',
                                  'María, vive en Lima, César, en Arequipa'],
                 'correcta': 'A'},
                {'pregunta': 'El uso adecuado del punto y coma se observa '
                             'en: (Banco UNSAAC)',
                 'alternativas': ['Yo vivo; tú existes; él murió',
                                  'Azul; amarillo y rojo son colores '
                                  'primarios',
                                  'El bebé se enfermó; sus padres lo '
                                  'llevaron a la clínica',
                                  'Quillabamba; Ciudad del Eterno Verano; mi '
                                  'tierra',
                                  'Señores; estudien conscientemente'],
                 'correcta': 'A'},
                {'pregunta': 'El signo de puntuación que se utiliza para '
                             'separar párrafos se denomina: (Banco UNSAAC)',
                 'alternativas': ['Punto final',
                                  'Punto y coma',
                                  'Punto seguido',
                                  'Dos puntos',
                                  'Punto aparte'],
                 'correcta': 'E'},
                {'pregunta': 'La coma elíptica se halla en: (Dirimencia '
                             '2017-II)',
                 'alternativas': ['Mañana llegará mi hermano y el jueves, mi '
                                  'tío',
                                  'Queridos estudiantes, les deseo la mejor '
                                  'de las suertes',
                                  'Regresó preocupado, la razón, discutió '
                                  'con sus amigos',
                                  'Compraremos lápices, borradores, '
                                  'tajadores y reglas',
                                  'Eres muy bonita, pero despreocupada en '
                                  'tus estudios'],
                 'correcta': 'A'},
                {'pregunta': 'La oración en la cual se usa adecuadamente el '
                             'punto y coma es: (Dirimencia 2017-II)',
                 'alternativas': ['Los puntos cardinales de orientación son; '
                                  'este, oeste, norte y sur',
                                  'El abuelo se sintió mal de salud; sus '
                                  'familiares lo llevaron a la clínica',
                                  'Julio César; tiene que jugar carnavales '
                                  'sola con sus amigas',
                                  'Ellos estudian Competencia Lingüística; '
                                  'Aritmética; Álgebra',
                                  'En el parque zonal; los alumnos juegan '
                                  'fútbol el fin de semana'],
                 'correcta': 'B'},
                {'pregunta': 'El signo de puntuación que se usa para separar '
                             'párrafos es: (Dirimencia 2017-II)',
                 'alternativas': ['La coma hiperbática',
                                  'El punto y coma',
                                  'El punto y aparte',
                                  'El punto y seguido',
                                  'Los dos puntos'],
                 'correcta': 'C'},
                {'pregunta': 'Los signos de interrogación en la lengua '
                             'española son dos, al inicio y al final de la '
                             'expresión, y se utilizan para: (Dirimencia)',
                 'alternativas': ['Inducir',
                                  'Exclamar',
                                  'Permutar',
                                  'Inquirir',
                                  'Rememorar'],
                 'correcta': 'D'},
                {'pregunta': 'Las comillas en uso metalingüístico se '
                             'aprecian en: (Banco UNSAAC)',
                 'alternativas': ['Carlos «El Apache» Tévez juega en el '
                                  'fútbol chino',
                                  'El «vocativo» no es parte del sintagma '
                                  'nominal ni verbal',
                                  'Cuando estés en Roma compórtate como los '
                                  'romanos',
                                  'En esa joyería venden hermosos «anillos» '
                                  'de oro fino',
                                  'El lingüista Noam Chomsky escribió la '
                                  '«Teoría minimalista»'],
                 'correcta': 'B'},
                {'pregunta': 'Se aprecia coma hiperbática en: (Banco UNSAAC)',
                 'alternativas': ['Andrés, debes levantarte temprano para ir '
                                  'al colegio',
                                  'Los colores primarios son: rojo, azul y '
                                  'amarillo',
                                  'José juega fútbol; su amigo, básquet',
                                  'En el estadio, el entrenador entregó un '
                                  'premio al jugador',
                                  'Los niños estudian, los padres trabajan y '
                                  'los maestros enseñan'],
                 'correcta': 'D'},
                {'pregunta': 'El enunciado que presenta punto y coma en la '
                             'oración yuxtapuesta de causa y efecto es: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Colocó la vajilla en el cajón; los '
                                  'cubiertos en la gaveta',
                                  'Puede irse a casa; no hay nada que hacer',
                                  'El perro fue atropellado; murió '
                                  'inmediatamente',
                                  'Es un ejemplo social; lo hizo por su '
                                  'familia',
                                  'Tienes que irte a tu morada; cumpliste tu '
                                  'misión'],
                 'correcta': 'C'},
                {'pregunta': 'La expresión en la que se utiliza '
                             'correctamente el punto de abreviatura es: '
                             '(Banco UNSAAC)',
                 'alternativas': ['Miles de personas mueren en el mundo por '
                                  'el V.I.H.',
                                  'J. Pérez de Cuéllar representó a la '
                                  'O.N.U.',
                                  'La O.N.G. Calandria tiene subvención '
                                  'económica de la Comunidad Europea',
                                  'Eduardo viajó a Bs.As. para estudiar un '
                                  'posgrado',
                                  'El Mundial de Fútbol «Rusia 2018» es '
                                  'organizado por la FI.FA.'],
                 'correcta': 'D'},
                {'pregunta': 'El uso de comillas en las expresiones '
                             'denominativas se aprecia en: (Banco UNSAAC)',
                 'alternativas': ['Se ha clausurado con gran éxito la '
                                  'exposición «Las vanguardias andinas»',
                                  '«Los Heraldos Negros» pertenecen a '
                                  'Vallejo',
                                  'La palabra «cándido» lleva tilde por ser '
                                  'esdrújula',
                                  'La voz apicultura está formada a partir '
                                  'del término latino «apis»',
                                  'En el salón han puesto un «cuadro» que '
                                  'les ha costado un dineral'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO Y FUNCIONES / EL PUNTO',
                      'items': ['Los signos de puntuación son signos '
                                'ortográficos que organizan el discurso para '
                                'facilitar su comprensión.',
                                'Los signos de puntuación ponen de '
                                'manifiesto las relaciones sintácticas y '
                                'lógicas entre los constituyentes del texto.',
                                'Una función de los signos de puntuación es '
                                'indicar los límites de las unidades '
                                'discursivas.',
                                'El punto se usa en las abreviaturas, como '
                                '«Sra.» o «pág.».',
                                'El punto se usa también en fechas y horas, '
                                'como 22.02.22.',
                                'Nunca se escribe punto al final de títulos '
                                'y subtítulos de libros, artículos u obras '
                                'de arte.']},
                     {'titulo': 'LA COMA / LOS DOS PUNTOS',
                      'items': ['La coma incidental se usa para intercalar '
                                'información aclaratoria dentro del '
                                'enunciado.',
                                'La coma vocativa se usa para separar el '
                                'nombre de la persona a quien nos dirigimos, '
                                'como en «Eduardo, no quiero que salgas tan '
                                'tarde».',
                                'Los dos puntos se usan en enumeraciones: '
                                '«Las regiones del Imperio incaico fueron '
                                'cuatro: Antisuyo, Collasuyo, Chinchaysuyo y '
                                'Contisuyo».',
                                'Los dos puntos preceden al discurso '
                                'directo: «Francisco Bolognesi expresó: '
                                "'Tengo deberes sagrados que cumplir...'».",
                                'Los dos puntos yuxtapuestos indican '
                                'causa-efecto: «Se ha quedado sin trabajo: '
                                'no podrá ir de vacaciones».']},
                     {'titulo': 'LOS PUNTOS SUSPENSIVOS / EL PARÉNTESIS',
                      'items': ['Los puntos suspensivos indican suspensión u '
                                'omisión del discurso: «El caso es que si '
                                'lloviese…».',
                                'Los puntos suspensivos indican suspensión '
                                'con fines expresivos, como duda o temor: '
                                '«El niño dice que él no ha roto el '
                                'jarrón…».',
                                'Los puntos suspensivos señalan la omisión '
                                'de una parte del texto por sobrentendida, '
                                'como en refranes: «Más sabe el diablo por '
                                'viejo que…».',
                                'El paréntesis se usa para aislar incisos: '
                                '«Las asambleas (la primera y última) se '
                                'celebran en el salón de actos».',
                                'El paréntesis aísla otros elementos '
                                'intercalados, como fechas o datos: «El año '
                                'de su nacimiento (1616) es el mismo en que '
                                'murió Cervantes».',
                                'El paréntesis encierra acotaciones de '
                                'personajes en obras teatrales: «JORGE. '
                                '(Golpeando con el bastón)».']},
                     {'titulo': 'LAS COMILLAS / LA RAYA',
                      'items': ['Las comillas se usan en citas textuales y '
                                "reproducción de pensamientos: «'Sobreviven "
                                "los que se adaptan mejor al cambio' dijo "
                                'Charles Darwin».',
                                'Las comillas marcan el carácter especial de '
                                'una palabra o expresión, como ironía: '
                                "«Siempre dice que las 'tortas' de esa "
                                'pastelería están riquísimas».',
                                'Las comillas se usan en usos '
                                'metalingüísticos, para mencionar una '
                                "palabra como tal: «La palabra 'cándida' "
                                'lleva tilde por ser esdrújula».',
                                'La raya se usa para separar incisos: «Para '
                                'él la fidelidad —cualidad que valoraba por '
                                'encima de cualquier otra— era algo '
                                'sagrado».',
                                'La raya enmarca las expresiones de un '
                                "narrador o transcriptor: «'Es "
                                'imprescindible —señaló el ministro— que se '
                                "refuercen los controles'».",
                                'La raya se usa en diálogos, marcando la '
                                'intervención de cada personaje: «—¿Cómo se '
                                'llama Ud.? —Paco.»']},
                     {'titulo': 'INTERROGACIÓN Y EXCLAMACIÓN',
                      'items': ['Los signos de interrogación y exclamación '
                                'se usan en interrogaciones y exclamaciones '
                                'directas: «¿Cuándo vendrás?»',
                                'Estos signos pueden omitirse en títulos de '
                                'obras, capítulos o secciones de un texto: '
                                '«Cómo escribir bien español».',
                                'Las oraciones exclamativas pueden estar '
                                'formadas por interjecciones (¡Ay!), '
                                'onomatopeyas (¡Chist!) o vocativos '
                                '(¡Niños!).']}]},
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
                {'titulo': '8.5 TIPOS DE GÉNERO DEL SUSTANTIVO (I)',
                 'items': ['Los sustantivos {heterónimos} expresan la '
                           'diferencia masculino/femenino con términos de '
                           '{raíz diferente}: padre/madre, caballo/yegua.',
                           'Los sustantivos de {terminación variable} '
                           'manifiestan el género con morfemas sobre la '
                           'misma raíz: niño/niña; la desinencia más común '
                           'del femenino es {-a}.',
                           'Otros morfemas de género en nombres de personas '
                           'son -esa (alcalde/alcaldesa), -isa '
                           '(profeta/{profetisa}), -triz (actor/actriz) y '
                           '-ina (héroe/heroína).',
                           'Los sustantivos {comunes en cuanto al género} '
                           'pueden ser masculino o femenino sin cambiar de '
                           'forma; el género se marca en la {concordancia}: '
                           'el/la artista, el/la estudiante.']},
                {'titulo': '8.6 TIPOS DE GÉNERO DEL SUSTANTIVO (II)',
                 'items': ['Muchos sustantivos de persona con masculino en '
                           '-o, que designan profesiones, presentan el '
                           'femenino en {-a}: abogado/abogada, '
                           'ingeniero/ingeniera.',
                           'Los sustantivos que designan grados de la escala '
                           '{militar} son comunes en cuanto al género, '
                           'cualquiera sea su terminación: el/la soldado, '
                           'el/la sargento.',
                           'Los sustantivos {ambiguos} en cuanto al género '
                           'son de terminación invariable y pueden usarse '
                           'como masculino o femenino sin cambiar de '
                           'significado: el/la mar, el/la azúcar.',
                           'Los sustantivos {polisémicos} y homónimos se '
                           'diferencian en significado y género: el capital '
                           '(dinero) / la capital (ciudad); el cólera '
                           '(enfermedad) / la cólera (ira).']},
                {'titulo': '8.7 LOS SUSTANTIVOS EPICENOS',
                 'items': ['Los sustantivos {epicenos} tienen un único '
                           'género gramatical para nombrar ambos sexos, '
                           'distinguido agregando macho o {hembra}: la '
                           'avispa macho, el tiburón hembra.',
                           'Existen sustantivos epicenos de {animales} '
                           '(jirafa, hormiga, cebra), de {plantas} (palmera, '
                           'sauce) y de personas (víctima, cónyuge, '
                           'personaje, rehén).',
                           'Es {incorrecto} concordar el adjetivo con el '
                           'sexo real en sustantivos epicenos: decir «el '
                           'tiburón hembra es muy peligrosa» es '
                           '{incorrecto}; debe ser «peligroso».']},
                {'titulo': '8.8 REGLAS GENERALES DEL PLURAL',
                 'items': ['Los nombres terminados en vocal átona o tónica '
                           'hacen el plural agregando {-s}: casas, cafés, '
                           'sofás.',
                           'Los nombres terminados en -í, -ú tónicas admiten '
                           'dos variantes de plural: {bisturíes} o bisturís, '
                           'tabúes o tabús.',
                           'Los nombres acabados en las consonantes L, N, R, '
                           'D, Z, J hacen el plural en {-es}: cónsules, '
                           'leones, paredes, peces.',
                           'Los nombres terminados en -S, -X que son agudos '
                           'o monosílabos hacen el plural en -es '
                           '(autobuses); los llanos o esdrújulos permanecen '
                           '{invariables}: la dosis, las tesis, los lunes.',
                           'A los nombres terminados en -Y se añade {-es}: '
                           'bueyes, leyes, reyes.']},
                {'titulo': '8.9 EL PLURAL DE LOS COMPUESTOS',
                 'items': ['Los compuestos que forman una sola palabra '
                           'pluralizan solo el {segundo} elemento: '
                           'bocacalles, tiovivos, cortometrajes.',
                           'Cuando dos sustantivos se escriben separados y '
                           'el segundo aporta información determinativa, el '
                           'plural se marca solo en el {primero}: años luz, '
                           'coches bomba, hombres rana.',
                           'Los sustantivos macho y hembra no se pluralizan '
                           'cuando {modifican} a otro sustantivo: las '
                           'panteras macho, las avestruces hembra.',
                           'En compuestos de dos adjetivos, unidos o '
                           'separados por guion, se pluraliza solo el '
                           '{segundo}: conversaciones árabe-israelíes.']}],
  'cuadros': [{'titulo': '8.4 CLASIFICACIONES DEL SUSTANTIVO',
               'encabezados': ['Clasificación', 'Tipos'],
               'filas': [['Por su extensión', '{Propios} y comunes'],
                         ['Por su cuantificación',
                          '{Contables} y no contables'],
                         ['Por su percepción', '{Concretos} y abstractos'],
                         ['Por su número', '{Individuales} y colectivos']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el sustantivo '
                             'designa:',
                 'alternativas': ['Solo acciones',
                                  'Seres y objetos de la realidad',
                                  'Solo cantidades',
                                  'Solo cualidades',
                                  'Solo relaciones lógicas'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el sustantivo '
                             'es una palabra:',
                 'alternativas': ['Invariable',
                                  'Sin flexión',
                                  'Variable, con morfemas de género y número',
                                  'Exclusivamente derivada',
                                  'Sin composición posible'],
                 'correcta': 'C'},
                {'pregunta': 'Según el criterio sintáctico, el sustantivo '
                             'forma grupos nominales que pueden cumplir '
                             'función de:',
                 'alternativas': ['Solo verbo',
                                  'Solo adjetivo',
                                  'Solo conjunción',
                                  'Sujeto, complemento directo, indirecto, '
                                  'entre otros',
                                  'Solo preposición'],
                 'correcta': 'D'},
                {'pregunta': 'En «El profesor viajará muy pronto», el '
                             'sustantivo «profesor» funciona como núcleo de:',
                 'alternativas': ['El complemento agente',
                                  'La aposición',
                                  'El vocativo',
                                  'El complemento directo',
                                  'El sujeto'],
                 'correcta': 'E'},
                {'pregunta': 'En «Señorita, aquí tiene su cuaderno», '
                             '«Señorita» funciona como núcleo del:',
                 'alternativas': ['Vocativo',
                                  'Sujeto',
                                  'Complemento directo',
                                  'Atributo',
                                  'Complemento indirecto'],
                 'correcta': 'A'},
                {'pregunta': 'En «Ricardo Palma, el bibliotecario mendigo, '
                             'escribió Tradiciones peruanas», «el '
                             'bibliotecario mendigo» es núcleo de:',
                 'alternativas': ['El atributo',
                                  'El complemento circunstancial',
                                  'El sujeto',
                                  'La aposición',
                                  'El vocativo'],
                 'correcta': 'D'},
                {'pregunta': 'En «El cuento fue leído por el niño», «el '
                             'niño» funciona como núcleo del complemento:',
                 'alternativas': ['Agente',
                                  'De régimen',
                                  'Indirecto',
                                  'Directo',
                                  'Circunstancial'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos que nombran a los seres '
                             'diferenciándolos de los demás de su especie '
                             'son los sustantivos:',
                 'alternativas': ['Comunes',
                                  'Abstractos',
                                  'Contables',
                                  'Propios',
                                  'Colectivos'],
                 'correcta': 'D'},
                {'pregunta': 'Los sustantivos propios, ortográficamente, se '
                             'escriben con:',
                 'alternativas': ['Guion inicial',
                                  'Minúscula inicial',
                                  'Comillas siempre',
                                  'Cursiva obligatoria',
                                  'Mayúscula inicial'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que nombran a todos los seres '
                             'de una clase son los sustantivos:',
                 'alternativas': ['Comunes',
                                  'Contables',
                                  'Individuales exclusivos',
                                  'Propios',
                                  'Colectivos exclusivos'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos que designan entidades que se '
                             'pueden contar son los sustantivos:',
                 'alternativas': ['Colectivos',
                                  'Contables',
                                  'Abstractos',
                                  'No contables',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que denotan magnitudes o '
                             'sustancias, como «un poco de café», son los '
                             'sustantivos:',
                 'alternativas': ['Propios',
                                  'Colectivos',
                                  'No contables',
                                  'Individuales',
                                  'Contables'],
                 'correcta': 'C'},
                {'pregunta': 'Los sustantivos que nombran seres percibidos '
                             'por los sentidos son los sustantivos:',
                 'alternativas': ['Colectivos',
                                  'No contables',
                                  'Comunes exclusivos',
                                  'Abstractos',
                                  'Concretos'],
                 'correcta': 'E'},
                {'pregunta': 'Los sustantivos que se conocen mediante un '
                             'proceso mental de abstracción son los '
                             'sustantivos:',
                 'alternativas': ['Propios exclusivos',
                                  'Individuales',
                                  'Concretos',
                                  'Abstractos',
                                  'Contables'],
                 'correcta': 'D'},
                {'pregunta': '«Hermosura», «paz» y «ambición» son ejemplos '
                             'de sustantivos:',
                 'alternativas': ['Propios',
                                  'Abstractos',
                                  'Colectivos',
                                  'Contables',
                                  'Concretos'],
                 'correcta': 'B'},
                {'pregunta': '«Cóndor», «árbol» y «lapicero» son ejemplos de '
                             'sustantivos:',
                 'alternativas': ['Propios',
                                  'No contables',
                                  'Concretos',
                                  'Colectivos exclusivos',
                                  'Abstractos'],
                 'correcta': 'C'},
                {'pregunta': 'Los sustantivos que nombran a un solo ser son '
                             'los sustantivos:',
                 'alternativas': ['Colectivos',
                                  'No contables',
                                  'Abstractos',
                                  'Propios exclusivos',
                                  'Individuales'],
                 'correcta': 'E'},
                {'pregunta': '«Arboleda», «enjambre» y «cardumen» son '
                             'ejemplos de sustantivos:',
                 'alternativas': ['Abstractos',
                                  'Colectivos',
                                  'Individuales',
                                  'No contables exclusivos',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos colectivos, en número '
                             'singular, designan:',
                 'alternativas': ['Una cualidad abstracta',
                                  'Un solo ser',
                                  'Una relación lógica',
                                  'Un conjunto de seres',
                                  'Una acción'],
                 'correcta': 'D'},
                {'pregunta': 'En «Aquellos jóvenes parecen buenos '
                             'profesionales», «profesionales» funciona como '
                             'núcleo de:',
                 'alternativas': ['El complemento agente',
                                  'El vocativo',
                                  'La aposición',
                                  'El atributo',
                                  'El sujeto'],
                 'correcta': 'D'},
                {'pregunta': 'Los sustantivos que expresan la diferencia '
                             'masculino/femenino mediante términos de raíz '
                             'diferente, como padre/madre, se llaman:',
                 'alternativas': ['De terminación variable',
                                  'Ambiguos',
                                  'Comunes en cuanto al género',
                                  'Epicenos',
                                  'Heterónimos'],
                 'correcta': 'E'},
                {'pregunta': 'En los sustantivos de terminación variable, la '
                             'desinencia más común para marcar el femenino '
                             'es:',
                 'alternativas': ['-e', '-a', '-esa', '-triz', '-o'],
                 'correcta': 'B'},
                {'pregunta': 'El morfema -triz para marcar el femenino '
                             'aparece en pares como actor/actriz y:',
                 'alternativas': ['Duque/duquesa',
                                  'Papa/papisa',
                                  'Héroe/heroína',
                                  'Emperador/emperatriz',
                                  'Alcalde/alcaldesa'],
                 'correcta': 'D'},
                {'pregunta': 'Los sustantivos que pueden ser masculinos o '
                             'femeninos sin que su forma cambie, como el/la '
                             'artista, se llaman:',
                 'alternativas': ['Comunes en cuanto al género',
                                  'Ambiguos',
                                  'Epicenos',
                                  'Heterónimos',
                                  'De terminación variable'],
                 'correcta': 'A'},
                {'pregunta': 'Muchos sustantivos de persona con masculino en '
                             '-o, que designan profesiones, presentan el '
                             'femenino terminado en:',
                 'alternativas': ['-a', '-e', '-isa', '-triz', '-ina'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos que designan grados de la '
                             'escala militar, como soldado o sargento, son '
                             'considerados:',
                 'alternativas': ['Comunes en cuanto al género',
                                  'Epicenos',
                                  'Ambiguos exclusivamente en plural',
                                  'De terminación variable exclusiva',
                                  'Heterónimos'],
                 'correcta': 'A'},
                {'pregunta': 'Los sustantivos de terminación invariable que '
                             'pueden usarse como masculino o femenino sin '
                             'cambiar de significado, como el/la mar, se '
                             'llaman sustantivos:',
                 'alternativas': ['Comunes obligatorios',
                                  'Heterónimos',
                                  'Ambiguos en cuanto al género',
                                  'Epicenos',
                                  'De terminación variable'],
                 'correcta': 'C'},
                {'pregunta': 'Los términos polisémicos que se diferencian en '
                             'significado y en género, como «el capital» y '
                             '«la capital», son sustantivos:',
                 'alternativas': ['Ambiguos',
                                  'Comunes',
                                  'Polisémicos con diferencia de género',
                                  'Epicenos',
                                  'Heterónimos'],
                 'correcta': 'C'},
                {'pregunta': 'Los sustantivos con un único género gramatical '
                             'para nombrar ambos sexos, distinguidos '
                             'agregando macho o hembra, se llaman '
                             'sustantivos:',
                 'alternativas': ['Comunes en cuanto al género',
                                  'Ambiguos',
                                  'Heterónimos',
                                  'Epicenos',
                                  'De terminación variable'],
                 'correcta': 'D'},
                {'pregunta': 'Es incorrecto concordar el adjetivo con el '
                             'sexo real de un sustantivo epiceno; por ello, '
                             'se dice correctamente «el tiburón hembra es '
                             'muy»:',
                 'alternativas': ['Peligroso',
                                  'Ninguna es correcta',
                                  'Peligrosos',
                                  'Peligrosas',
                                  'Peligrosa'],
                 'correcta': 'A'},
                {'pregunta': 'Los nombres terminados en vocal átona o '
                             'tónica, como casa o café, forman el plural '
                             'agregando:',
                 'alternativas': ['-es', 'Sin cambio', '-ces', '-res', '-s'],
                 'correcta': 'E'},
                {'pregunta': 'Los nombres acabados en las consonantes L, N, '
                             'R, D, Z, J, como cónsul o pared, forman el '
                             'plural agregando:',
                 'alternativas': ['-s', 'Sin cambio', '-es', '-ces', '-ses'],
                 'correcta': 'C'},
                {'pregunta': 'Palabras llanas o esdrújulas terminadas en -S '
                             'o -X, como «tesis» o «tórax», en plural:',
                 'alternativas': ['Agregan -es',
                                  'Agregan -s',
                                  'Se vuelven agudas',
                                  'Permanecen invariables',
                                  'Cambian la raíz'],
                 'correcta': 'D'},
                {'pregunta': 'Los nombres terminados en -Y, como rey o ley, '
                             'forman el plural agregando:',
                 'alternativas': ['-es', '-s', '-ces', '-ies', 'Sin cambio'],
                 'correcta': 'A'},
                {'pregunta': 'En los compuestos que forman una sola palabra, '
                             'como «bocacalle», el plural se marca en:',
                 'alternativas': ['Ambos elementos',
                                  'El segundo elemento',
                                  'El primer elemento',
                                  'Ningún elemento',
                                  'Un elemento intermedio'],
                 'correcta': 'B'},
                {'pregunta': 'En compuestos escritos por separado donde el '
                             'segundo elemento aporta información '
                             'determinativa, como «años luz», el plural se '
                             'marca en:',
                 'alternativas': ['El segundo elemento',
                                  'El primer elemento',
                                  'Ambos elementos',
                                  'Se pluraliza como una sola palabra',
                                  'Ningún elemento'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos macho y hembra no se '
                             'pluralizan cuando:',
                 'alternativas': ['Modifican a otro sustantivo',
                                  'Son sujeto de la oración',
                                  'Llevan artículo determinado',
                                  'Van en plural genérico',
                                  'Van al inicio de la oración'],
                 'correcta': 'A'},
                {'pregunta': 'La oración con dos sustantivos comunes en '
                             'cuanto al género es: (Banco UNSAAC)',
                 'alternativas': ['El ciclista atropelló con fuerza a una '
                                  'yegua',
                                  'El dentista prohibió el uso excesivo de '
                                  'azúcar',
                                  'El taxista llevó al turista a la estación',
                                  'El deportista obtuvo un pendiente de paga',
                                  'La auxiliar tiene una ardilla hermosa'],
                 'correcta': 'C'},
                {'pregunta': 'Los sustantivos ambiguos son: (Banco UNSAAC)',
                 'alternativas': ['Actor - yegua',
                                  'Alumno - poeta',
                                  'Artista - vodka',
                                  'Interrogante - dote',
                                  'Profesional - rehén'],
                 'correcta': 'D'},
                {'pregunta': 'El enunciado que presenta un sustantivo '
                             'epiceno con concordancia adecuada es: (Banco '
                             'UNSAAC)',
                 'alternativas': ['El ombú hembra es frondosa',
                                  'El rinoceronte hembra es hermoso',
                                  'El personaje de la comedia salió '
                                  'victorioso',
                                  'La víbora macho es muy venenoso',
                                  'La avispa macho es peligroso'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que solo presentan número '
                             'plural son: (Banco UNSAAC)',
                 'alternativas': ['Anales - noticias',
                                  'Peces - albricias',
                                  'Fauces - flores',
                                  'Nupcias - bruces',
                                  'Comicios - tenazas'],
                 'correcta': 'D'},
                {'pregunta': 'En cuanto al género, la oración con sustantivo '
                             'común es: (Banco UNSAAC)',
                 'alternativas': ['La tigresa es exhibida en el zoológico',
                                  'La doctora auscultó al paciente',
                                  'El adolescente concurrió al festival',
                                  'El internet es usado por multitudes',
                                  'El Papa visitará nuestro país'],
                 'correcta': 'C'},
                {'pregunta': 'El sustantivo ambiguo está presente en: (Banco '
                             'UNSAAC)',
                 'alternativas': ['La capital está muy lejos',
                                  'La tilde no se usa siempre',
                                  'El Sol irradia rayos nocivos',
                                  'El taxista nos llevó al aeropuerto',
                                  'El yerno es aceptado por la familia'],
                 'correcta': 'C'},
                {'pregunta': 'Son sustantivos epicenos: (Banco UNSAAC)',
                 'alternativas': ['El foco macho - la foca hembra',
                                  'El palto - la palta',
                                  'El león macho - el león hembra',
                                  'La jirafa macho - la jirafa hembra',
                                  'Toro - vaca'],
                 'correcta': 'D'},
                {'pregunta': 'El sustantivo que se usa únicamente en número '
                             'singular es: (Banco UNSAAC)',
                 'alternativas': ['Salud',
                                  'Bucle',
                                  'Alicate',
                                  'Pantalón',
                                  'Enfermedad'],
                 'correcta': 'A'},
                {'pregunta': 'En el proceso de feminización, el sustantivo '
                             'de terminación variable es: (Banco UNSAAC)',
                 'alternativas': ['Obstetra',
                                  'Periodista',
                                  'Mar',
                                  'Senador',
                                  'Cóndor'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras «yerno» y «nuera» constituyen '
                             'sustantivos: (Banco UNSAAC)',
                 'alternativas': ['Ambiguos',
                                  'Heterónimos',
                                  'Polisémicos',
                                  'Epicenos',
                                  'Homónimos'],
                 'correcta': 'B'},
                {'pregunta': 'El enunciado que presenta un sustantivo '
                             'polisémico es: (Banco UNSAAC)',
                 'alternativas': ['El calor es sofocante en verano',
                                  'Ese caballo de paso es de mi compadre',
                                  'La adolescente expuso su nuevo proyecto',
                                  'El guitarrista se presentó en el teatro',
                                  'La editorial Alfaguara es muy '
                                  'prestigiosa'],
                 'correcta': 'E'},
                {'pregunta': 'El sustantivo «jueves» se pluraliza a través '
                             'de: (Banco UNSAAC)',
                 'alternativas': ['El artículo «los»',
                                  'El morfema «-s»',
                                  'El artículo «las»',
                                  'El morfema «-es»',
                                  'El artículo «el»'],
                 'correcta': 'A'},
                {'pregunta': 'El nombre propio bien pluralizado es: (Banco '
                             'UNSAAC)',
                 'alternativas': ['Los Fernandos Belaúndes son políticos',
                                  'Los Albertos Fujimori deben estar '
                                  'encarcelados',
                                  'Los Sancho Panza son personas indeseables',
                                  'Marios Vargas Llosas es un gran escritor',
                                  'La María Cristina juegan en el parque'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CRITERIOS PARA DEFINIR EL SUSTANTIVO / '
                                'FUNCIONES DEL SUSTANTIVO',
                      'items': ['Según el criterio semántico, el sustantivo '
                                'designa a los seres y objetos de la '
                                'realidad, de existencia concreta o '
                                'abstracta.',
                                'Según el criterio morfológico, el '
                                'sustantivo es una palabra variable con '
                                'morfemas de género y número.',
                                'Según el criterio sintáctico, el sustantivo '
                                'forma grupos nominales capaces de cumplir '
                                'funciones como sujeto o complemento.',
                                'El sustantivo puede funcionar como núcleo '
                                'del sujeto, del complemento directo, '
                                'indirecto o circunstancial.',
                                'El sustantivo puede funcionar como núcleo '
                                'del vocativo, como en «Señorita, aquí tiene '
                                'su cuaderno».',
                                'El sustantivo puede funcionar como núcleo '
                                'de la aposición, como en «Ricardo Palma, el '
                                'bibliotecario mendigo».']},
                     {'titulo': 'SUSTANTIVOS PROPIOS Y COMUNES / OTRAS '
                                'CLASIFICACIONES DEL SUSTANTIVO',
                      'items': ['Los sustantivos propios nombran a los seres '
                                'diferenciándolos de los demás de su misma '
                                'especie, y se escriben con mayúscula '
                                'inicial.',
                                'Los sustantivos comunes nombran a todos los '
                                'seres de una clase, y se escriben con '
                                'minúscula inicial.',
                                'Los sustantivos contables designan '
                                'entidades que se pueden contar, como «tres '
                                'planetas».',
                                'Los sustantivos no contables denotan '
                                'magnitudes o sustancias, como «un poco de '
                                'café».',
                                'Los sustantivos concretos nombran seres '
                                'percibidos por los sentidos, con existencia '
                                'independiente.']},
                     {'titulo': 'TIPOS DE GÉNERO DEL SUSTANTIVO (I) / TIPOS '
                                'DE GÉNERO DEL SUSTANTIVO (II)',
                      'items': ['Los sustantivos heterónimos expresan la '
                                'diferencia masculino/femenino con términos '
                                'de raíz diferente: padre/madre, '
                                'caballo/yegua.',
                                'Los sustantivos de terminación variable '
                                'manifiestan el género con morfemas sobre la '
                                'misma raíz: niño/niña; la desinencia más '
                                'común del femenino es -a.',
                                'Otros morfemas de género en nombres de '
                                'personas son -esa (alcalde/alcaldesa), -isa '
                                '(profeta/profetisa), -triz (actor/actriz) y '
                                '-ina (héroe/heroína).',
                                'Muchos sustantivos de persona con masculino '
                                'en -o, que designan profesiones, presentan '
                                'el femenino en -a: abogado/abogada, '
                                'ingeniero/ingeniera.',
                                'Los sustantivos que designan grados de la '
                                'escala militar son comunes en cuanto al '
                                'género, cualquiera sea su terminación: '
                                'el/la soldado, el/la sargento.',
                                'Los sustantivos ambiguos en cuanto al '
                                'género son de terminación invariable y '
                                'pueden usarse como masculino o femenino sin '
                                'cambiar de significado: el/la mar, el/la '
                                'azúcar.']},
                     {'titulo': 'LOS SUSTANTIVOS EPICENOS / REGLAS GENERALES '
                                'DEL PLURAL',
                      'items': ['Los sustantivos epicenos tienen un único '
                                'género gramatical para nombrar ambos sexos, '
                                'distinguido agregando macho o hembra: la '
                                'avispa macho, el tiburón hembra.',
                                'Existen sustantivos epicenos de animales '
                                '(jirafa, hormiga, cebra), de plantas '
                                '(palmera, sauce) y de personas (víctima, '
                                'cónyuge, personaje, rehén).',
                                'Es incorrecto concordar el adjetivo con el '
                                'sexo real en sustantivos epicenos: decir '
                                '«el tiburón hembra es muy peligrosa» es '
                                'incorrecto; debe ser «peligroso».',
                                'Los nombres terminados en vocal átona o '
                                'tónica hacen el plural agregando -s: casas, '
                                'cafés, sofás.',
                                'Los nombres terminados en -í, -ú tónicas '
                                'admiten dos variantes de plural: bisturíes '
                                'o bisturís, tabúes o tabús.',
                                'Los nombres acabados en las consonantes L, '
                                'N, R, D, Z, J hacen el plural en -es: '
                                'cónsules, leones, paredes, peces.']},
                     {'titulo': 'EL PLURAL DE LOS COMPUESTOS',
                      'items': ['Los compuestos que forman una sola palabra '
                                'pluralizan solo el segundo elemento: '
                                'bocacalles, tiovivos, cortometrajes.',
                                'Cuando dos sustantivos se escriben '
                                'separados y el segundo aporta información '
                                'determinativa, el plural se marca solo en '
                                'el primero: años luz, coches bomba, hombres '
                                'rana.',
                                'Los sustantivos macho y hembra no se '
                                'pluralizan cuando modifican a otro '
                                'sustantivo: las panteras macho, las '
                                'avestruces hembra.']}]},
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
                {'titulo': '9.3 PRONOMBRES ÁTONOS O CLÍTICOS',
                 'items': ['Los pronombres {átonos} son: me, se, te, le, '
                           'les, la, las, lo, los, nos, os.',
                           'Al carecer de {acento} propio, los pronombres '
                           'átonos se apoyan fonéticamente en el verbo '
                           'contiguo, por lo que también se llaman '
                           'pronombres {clíticos}.',
                           'Ejemplos de pronombres átonos: «Te admitieron '
                           'para el ciclo», «La abrazó amablemente», '
                           '«{Cómpratelo}».']},
                {'titulo': '9.4 PRONOMBRES DEMOSTRATIVOS',
                 'items': ['Los pronombres demostrativos identifican algo o '
                           'alguien estableciendo la {distancia} con '
                           'relación al hablante.',
                           'Cerca del hablante (1ª persona): {este}, esta, '
                           'estos, estas, esto.',
                           'Cerca del oyente (2ª persona): {ese}, esa, esos, '
                           'esas, eso.',
                           'Lejos de ambos (3ª persona): {aquel}, aquella, '
                           'aquellos, aquellas, aquello.']},
                {'titulo': '9.5 PRONOMBRES POSESIVOS',
                 'items': ['Los pronombres posesivos indican {posesión} o '
                           'pertenencia, nombrando al objeto a través del '
                           '{poseedor}.',
                           'De 1ª persona: mío, mía, míos, mías, {nuestro}, '
                           'nuestra.',
                           'De 2ª persona: tuyo, tuya, tuyos, tuyas, '
                           '{vuestro}, vuestra.',
                           'De 3ª persona: {suyo}, suya, suyos, suyas.']},
                {'titulo': '9.6 PRONOMBRES INDEFINIDOS Y NUMERALES',
                 'items': ['Los pronombres {indefinidos} son cuantificadores '
                           'que dan una referencia vaga o imprecisa de los '
                           'seres: alguien, {nadie}, varios, muchos, '
                           'cualquiera.',
                           'Los pronombres {numerales} indican cantidad, '
                           'orden, repetición, división o distribución de '
                           'los seres.',
                           'Los numerales {cardinales} indican cantidad '
                           'exacta: «Entregó doce para la familia».',
                           'Los numerales {ordinales} expresan el lugar que '
                           'ocupa una unidad en una serie: «Los últimos '
                           'siempre ganan».',
                           'Los numerales {múltiplos} indican multiplicación '
                           'o repetición: «Ganarás el {doble}; mañana, el '
                           'triple».',
                           'Los numerales {partitivos} indican la parte o '
                           'fracción de un ser: «Comí solo la {mitad}».']},
                {'titulo': '9.7 PRONOMBRES RELATIVOS, INTERROGATIVOS Y '
                           'EXCLAMATIVOS',
                 'items': ['Los pronombres {relativos} encabezan una '
                           'proposición subordinada y hacen referencia a un '
                           'sustantivo {antecedente}: que, cual, quien, '
                           'cuyo.',
                           'Los pronombres {interrogativos} son los mismos '
                           'relativos, pero expresan {pregunta}; llevan '
                           'tilde y se usan entre signos de interrogación: '
                           '¿qué?, ¿cuál?, ¿quién?',
                           'Los pronombres {exclamativos} son los relativos '
                           'que expresan asombro, admiración o exclamación: '
                           '«¡Cuánto te quiere!», «¡{Quién} lo hubiera '
                           'creído!».']}],
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
                                  'Sin nombrarlos directamente',
                                  'Nombrándolos con precisión',
                                  'Solo en femenino',
                                  'Solo en plural'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre es descrito como una palabra:',
                 'alternativas': ['Invariable',
                                  'Siempre concreta',
                                  'Exclusivamente descriptiva',
                                  'No-connotativa',
                                  'Connotativa'],
                 'correcta': 'D'},
                {'pregunta': 'El pronombre es una palabra no descriptiva '
                             'porque:',
                 'alternativas': ['Señala al ser sin conceptuarlo',
                                  'Nombra directamente al ser',
                                  'Tiene significado fijo siempre',
                                  'Solo se usa en plural',
                                  'Señala cualidades del sustantivo'],
                 'correcta': 'A'},
                {'pregunta': 'Que el pronombre tenga significación ocasional '
                             'significa que:',
                 'alternativas': ['Solo funciona en singular',
                                  'Fuera de contexto carece de significado '
                                  'definido',
                                  'Es sinónimo de un sustantivo fijo',
                                  'Siempre tiene el mismo significado',
                                  'Nunca tiene significado'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el pronombre se carga de significado '
                             'dentro de un contexto, adquiere un valor:',
                 'alternativas': ['Ortográfico',
                                  'Descriptivo',
                                  'Referencial',
                                  'Morfológico exclusivo',
                                  'Fonológico'],
                 'correcta': 'C'},
                {'pregunta': 'Según el criterio morfológico, el pronombre es '
                             'una palabra:',
                 'alternativas': ['Variable, con accidentes de género, '
                                  'número y persona',
                                  'Exclusivamente masculina',
                                  'Sin flexión alguna',
                                  'Solo singular',
                                  'Invariable'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio sintáctico, el pronombre '
                             'puede funcionar como sustantivo, adjetivo o:',
                 'alternativas': ['Artículo',
                                  'Adverbio',
                                  'Interjección',
                                  'Preposición',
                                  'Conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre que funciona como sujeto '
                             'se llama caso:',
                 'alternativas': ['Nominativo o recto',
                                  'Vocativo',
                                  'Dativo',
                                  'Acusativo',
                                  'Preposicional'],
                 'correcta': 'A'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento directo se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Dativo',
                                  'Nominativo',
                                  'Preposicional',
                                  'Recto'],
                 'correcta': 'A'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento indirecto se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Vocativo',
                                  'Nominativo',
                                  'Dativo',
                                  'Preposicional'],
                 'correcta': 'D'},
                {'pregunta': 'El caso del pronombre usado después de una '
                             'preposición se llama caso:',
                 'alternativas': ['Preposicional',
                                  'Dativo',
                                  'Recto',
                                  'Nominativo',
                                  'Acusativo'],
                 'correcta': 'A'},
                {'pregunta': 'En «Yo no lo sabía», el pronombre «yo» está en '
                             'caso:',
                 'alternativas': ['Acusativo',
                                  'Preposicional',
                                  'Dativo',
                                  'Vocativo',
                                  'Nominativo'],
                 'correcta': 'E'},
                {'pregunta': 'En «No me entienden», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Nominativo',
                                  'Vocativo',
                                  'Recto',
                                  'Preposicional',
                                  'Acusativo'],
                 'correcta': 'E'},
                {'pregunta': 'En «Me duelen las muelas», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Recto',
                                  'Dativo',
                                  'Acusativo',
                                  'Nominativo',
                                  'Preposicional'],
                 'correcta': 'B'},
                {'pregunta': 'En «Confiaba en él», el pronombre «él» está en '
                             'caso:',
                 'alternativas': ['Acusativo',
                                  'Dativo',
                                  'Recto',
                                  'Nominativo',
                                  'Preposicional'],
                 'correcta': 'E'},
                {'pregunta': 'En «Ese se cayó anoche», el pronombre «ese» '
                             'ejemplifica que el pronombre es una palabra:',
                 'alternativas': ['Exclusivamente adjetiva',
                                  'Connotativa',
                                  'Fija en significado',
                                  'Descriptiva',
                                  'No descriptiva'],
                 'correcta': 'E'},
                {'pregunta': 'En «Esas niñas son más honestas que aquellas», '
                             'el primer pronombre «esas» funciona como:',
                 'alternativas': ['Adjetivo',
                                  'Conjunción',
                                  'Adverbio',
                                  'Sustantivo',
                                  'Preposición'],
                 'correcta': 'A'},
                {'pregunta': 'En «Todos estudiaban aquí», el pronombre '
                             '«todos» funciona como:',
                 'alternativas': ['Adjetivo',
                                  'Adverbio',
                                  'Sustantivo (núcleo del sujeto)',
                                  'Vocativo',
                                  'Preposición'],
                 'correcta': 'C'},
                {'pregunta': 'Los pronombres «ella», «tú», «ellos» aislados, '
                             'sin contexto, tienen significado:',
                 'alternativas': ['Siempre concreto',
                                  'Vacío o indefinido',
                                  'Descriptivo detallado',
                                  'Fijo y estable',
                                  'Exclusivamente plural'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre, a diferencia del sustantivo, se '
                             'caracteriza principalmente por:',
                 'alternativas': ['Señalar al ser sin nombrarlo con '
                                  'precisión',
                                  'Nombrar directamente al ser con sus '
                                  'cualidades',
                                  'Tener siempre género femenino',
                                  'No poder funcionar como sujeto',
                                  'Ser siempre invariable'],
                 'correcta': 'A'},
                {'pregunta': 'Los pronombres átonos como me, se, te, le, lo, '
                             'la también se llaman pronombres:',
                 'alternativas': ['Interrogativos',
                                  'Numerales',
                                  'Tónicos',
                                  'Clíticos',
                                  'Relativos'],
                 'correcta': 'D'},
                {'pregunta': 'Los pronombres átonos, al carecer de acento '
                             'propio, se apoyan fonéticamente en:',
                 'alternativas': ['El verbo contiguo',
                                  'El adverbio',
                                  'El sujeto',
                                  'El adjetivo',
                                  'El artículo'],
                 'correcta': 'A'},
                {'pregunta': 'Los pronombres demostrativos identifican algo '
                             'o alguien estableciendo la:',
                 'alternativas': ['Posesión',
                                  'Distancia con relación al hablante',
                                  'Repetición',
                                  'Cantidad',
                                  'Interrogación'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre demostrativo que indica cercanía '
                             'a la 2ª persona gramatical (el oyente) es:',
                 'alternativas': ['Este', 'Ese', 'Esto', 'Aquello', 'Aquel'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre demostrativo que indica lejanía '
                             'de ambos interlocutores (3ª persona) es:',
                 'alternativas': ['Eso', 'Aquel', 'Ese', 'Esto', 'Este'],
                 'correcta': 'C'},
                {'pregunta': 'Los pronombres posesivos indican posesión o '
                             'pertenencia, nombrando al objeto a través de:',
                 'alternativas': ['La distancia',
                                  'El lugar',
                                  'El tiempo',
                                  'El poseedor',
                                  'La cantidad'],
                 'correcta': 'D'},
                {'pregunta': 'Los cuantificadores que dan una referencia '
                             'vaga o imprecisa de los seres, como «alguien» '
                             'o «varios», se llaman pronombres:',
                 'alternativas': ['Indefinidos',
                                  'Relativos',
                                  'Demostrativos',
                                  'Numerales',
                                  'Posesivos'],
                 'correcta': 'A'},
                {'pregunta': 'Las palabras que indican cantidad, orden, '
                             'repetición o distribución de los seres se '
                             'llaman pronombres:',
                 'alternativas': ['Indefinidos',
                                  'Posesivos',
                                  'Relativos',
                                  'Interrogativos',
                                  'Numerales'],
                 'correcta': 'E'},
                {'pregunta': 'Los numerales que indican cantidad exacta, '
                             'como «doce», se llaman numerales:',
                 'alternativas': ['Partitivos',
                                  'Indefinidos',
                                  'Ordinales',
                                  'Cardinales',
                                  'Múltiplos'],
                 'correcta': 'D'},
                {'pregunta': 'Los numerales que expresan el lugar que ocupa '
                             'una unidad en una serie se llaman numerales:',
                 'alternativas': ['Partitivos',
                                  'Relativos',
                                  'Ordinales',
                                  'Cardinales',
                                  'Múltiplos'],
                 'correcta': 'C'},
                {'pregunta': 'Los numerales que indican multiplicación o '
                             'repetición, como «el doble», se llaman '
                             'numerales:',
                 'alternativas': ['Múltiplos',
                                  'Indefinidos',
                                  'Cardinales',
                                  'Ordinales',
                                  'Partitivos'],
                 'correcta': 'A'},
                {'pregunta': 'Los numerales que indican la parte o fracción '
                             'de un ser, como «la mitad», se llaman '
                             'numerales:',
                 'alternativas': ['Cardinales',
                                  'Múltiplos',
                                  'Relativos',
                                  'Ordinales',
                                  'Partitivos'],
                 'correcta': 'E'},
                {'pregunta': 'Los pronombres que encabezan una proposición '
                             'subordinada y hacen referencia a un sustantivo '
                             'antecedente se llaman pronombres:',
                 'alternativas': ['Numerales',
                                  'Exclamativos',
                                  'Relativos',
                                  'Indefinidos',
                                  'Interrogativos'],
                 'correcta': 'C'},
                {'pregunta': 'Los mismos pronombres relativos, cuando '
                             'expresan pregunta y llevan tilde, se llaman '
                             'pronombres:',
                 'alternativas': ['Interrogativos',
                                  'Posesivos',
                                  'Demostrativos',
                                  'Indefinidos',
                                  'Exclamativos'],
                 'correcta': 'A'},
                {'pregunta': 'Los pronombres relativos que expresan asombro '
                             'o admiración, como en «¡Cuánto te quiere!», se '
                             'llaman pronombres:',
                 'alternativas': ['Indefinidos',
                                  'Relativos simples',
                                  'Interrogativos',
                                  'Numerales',
                                  'Exclamativos'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CRITERIOS PARA DEFINIR EL PRONOMBRE',
                      'items': ['Según el criterio semántico, el pronombre '
                                'indica la existencia de seres sin '
                                'nombrarlos directamente.',
                                'El pronombre es una palabra no-connotativa, '
                                'porque no señala cualidades o '
                                'características del sustantivo.',
                                'El pronombre es una palabra no descriptiva, '
                                'porque señala al ser sin conceptuarlo.']},
                     {'titulo': 'CASOS DEL PRONOMBRE PERSONAL',
                      'items': ['El caso nominativo o recto corresponde a '
                                'pronombres como «yo», «tú», «él», que '
                                'funcionan como sujeto.',
                                'El caso acusativo, de complemento directo, '
                                'corresponde a pronombres como «me», «te», '
                                '«lo», «la».',
                                'El caso dativo, de complemento indirecto, '
                                'corresponde a pronombres como «me», «te», '
                                '«le», «les».']},
                     {'titulo': 'PRONOMBRES ÁTONOS O CLÍTICOS',
                      'items': ['Los pronombres átonos son: me, se, te, le, '
                                'les, la, las, lo, los, nos, os.',
                                'Al carecer de acento propio, los pronombres '
                                'átonos se apoyan fonéticamente en el verbo '
                                'contiguo, por lo que también se llaman '
                                'pronombres clíticos.',
                                'Ejemplos de pronombres átonos: «Te '
                                'admitieron para el ciclo», «La abrazó '
                                'amablemente», «Cómpratelo».']},
                     {'titulo': 'PRONOMBRES DEMOSTRATIVOS',
                      'items': ['Los pronombres demostrativos identifican '
                                'algo o alguien estableciendo la distancia '
                                'con relación al hablante.',
                                'Cerca del hablante (1ª persona): este, '
                                'esta, estos, estas, esto.',
                                'Cerca del oyente (2ª persona): ese, esa, '
                                'esos, esas, eso.']},
                     {'titulo': 'PRONOMBRES POSESIVOS',
                      'items': ['Los pronombres posesivos indican posesión o '
                                'pertenencia, nombrando al objeto a través '
                                'del poseedor.',
                                'De 1ª persona: mío, mía, míos, mías, '
                                'nuestro, nuestra.',
                                'De 2ª persona: tuyo, tuya, tuyos, tuyas, '
                                'vuestro, vuestra.']},
                     {'titulo': 'PRONOMBRES INDEFINIDOS Y NUMERALES',
                      'items': ['Los pronombres indefinidos son '
                                'cuantificadores que dan una referencia vaga '
                                'o imprecisa de los seres: alguien, nadie, '
                                'varios, muchos, cualquiera.',
                                'Los pronombres numerales indican cantidad, '
                                'orden, repetición, división o distribución '
                                'de los seres.',
                                'Los numerales cardinales indican cantidad '
                                'exacta: «Entregó doce para la familia».']},
                     {'titulo': 'PRONOMBRES RELATIVOS, INTERROGATIVOS Y '
                                'EXCLAMATIVOS',
                      'items': ['Los pronombres relativos encabezan una '
                                'proposición subordinada y hacen referencia '
                                'a un sustantivo antecedente: que, cual, '
                                'quien, cuyo.',
                                'Los pronombres interrogativos son los '
                                'mismos relativos, pero expresan pregunta; '
                                'llevan tilde y se usan entre signos de '
                                'interrogación: ¿qué?, ¿cuál?, ¿quién?',
                                'Los pronombres exclamativos son los '
                                'relativos que expresan asombro, admiración '
                                'o exclamación: «¡Cuánto te quiere!», '
                                '«¡Quién lo hubiera creído!».']}]},
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
                {'titulo': '10.4 TIPOS DE ADJETIVO CALIFICATIVO',
                 'items': ['El adjetivo calificativo {especificativo} o '
                           'restrictivo precisa de qué sustantivo se trata, '
                           'restringiendo su extensión: «gatos {negros}», '
                           '«alumno aplicado».',
                           'El adjetivo calificativo {explicativo} o no '
                           'restrictivo aparece entre pausas, va antepuesto '
                           'y no tiene carga excluyente: «El {misterioso} '
                           'gato sufrió una quemadura».',
                           'El adjetivo calificativo {epíteto} señala una '
                           'cualidad propia e inherente del sustantivo: '
                           '«{blanca} nieve», «roja sangre», «verde '
                           'hierba».']},
                {'titulo': '10.5 GRADO POSITIVO Y COMPARATIVO',
                 'items': ['El grado {positivo} expresa una cualidad '
                           'atribuida al sustantivo tal cual es, sin '
                           'comparación: «joven estudioso».',
                           'El grado {comparativo} nombra la cualidad '
                           'estableciendo una comparación; puede ser de '
                           '{superioridad} (más... que), igualdad (tan... '
                           'como) o inferioridad (menos... que).']},
                {'titulo': '10.6 SUPERLATIVO ABSOLUTO PERIFRÁSTICO Y '
                           'SINTÉTICO',
                 'items': ['El {superlativo absoluto} expresa la cualidad en '
                           'sumo grado, sin comparación.',
                           'El superlativo absoluto {perifrástico} modifica '
                           'el adjetivo con adverbios como muy, sumamente, '
                           'extremadamente: «Mi hermana es {muy} hermosa».',
                           'El superlativo absoluto {sintético} tiene dos '
                           'formas según la terminación del adjetivo.',
                           '1ª forma: si el adjetivo termina en -re o -ro, '
                           'se añade el sufijo {-érrimo(a)}: pobre → '
                           'paupérrimo, libre → libérrimo.',
                           '2ª forma: si el adjetivo tiene otra terminación, '
                           'se añade el sufijo {-ísimo(a)}: bueno → '
                           'bonísimo, fuerte → fortísimo, sabio → '
                           'sapientísimo.']},
                {'titulo': '10.7 SUPERLATIVO RELATIVO Y FORMAS IRREGULARES',
                 'items': ['El superlativo {relativo} maximiza o minimiza la '
                           'cualidad en relación a todos los de su misma '
                           'clase: «Aquella alumna es la {más} estudiosa del '
                           'salón».',
                           'Las formas {irregulares} o sincréticas del '
                           'adjetivo no siguen las reglas generales: '
                           'bueno→mejor→{óptimo}; malo→peor→pésimo; '
                           'grande→mayor→{máximo}; pequeño→menor→mínimo.']},
                {'titulo': '10.8 ADJETIVOS DETERMINATIVOS: DEMOSTRATIVOS Y '
                           'POSESIVOS',
                 'items': ['Los adjetivos {demostrativos} modifican al '
                           'sustantivo indicando la distancia de los seres '
                           'respecto al hablante: este/esta, {ese}/esa, '
                           'aquel/aquella.',
                           'Los adjetivos {posesivos} modifican al '
                           'sustantivo indicando posesión: mi(s), tu(s), '
                           'su(s), {nuestro}(s), vuestro(s).']},
                {'titulo': '10.9 ADJETIVOS NUMERALES',
                 'items': ['Los adjetivos {numerales} modifican al '
                           'sustantivo indicando cantidad y número exactos.',
                           'Los {cardinales} expresan cantidad exacta: cinco '
                           'delincuentes, tres soles.',
                           'Los {ordinales} expresan orden o sucesión: '
                           'segundo nivel, sexto grado.',
                           'Los {múltiplos} indican multiplicación o '
                           'repetición: doble baile, triple vacuna.',
                           'Los {partitivos} indican fracción de la unidad, '
                           'acompañados del sustantivo «parte» salvo medio, '
                           'mitad y tercio.']},
                {'titulo': '10.10 APÓCOPE DEL ADJETIVO',
                 'items': ['El {apócope} es la supresión de sonidos al final '
                           'de ciertas palabras.',
                           'Los adjetivos apócope pierden la {-o} final '
                           'cuando van delante de un sustantivo masculino '
                           'singular; en femenino quedan {intactos}.',
                           'Ejemplos de apócope: grande→{gran} chico; '
                           'bueno→un buen amigo; primero→el {primer} hijo; '
                           'alguno→algún consejo; ninguno→ningún alumno.']}],
  'cuadros': [{'titulo': '10.2 CLASES DE ADJETIVO CALIFICATIVO',
               'encabezados': ['Clase', 'Característica'],
               'filas': [['{Especificativo}', '{Precisa} y puede restringir'],
                         ['{Explicativo}',
                          'Entre pausas, sin carga {excluyente}'],
                         ['{Epíteto}', 'Cualidad {propia}, valor poético']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el adjetivo '
                             'agrega información o:',
                 'alternativas': ['Califica al sustantivo',
                                  'Actúa como preposición',
                                  'Sustituye al sustantivo',
                                  'Reemplaza al verbo',
                                  'Elimina el sustantivo'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio morfológico, el adjetivo es '
                             'una palabra:',
                 'alternativas': ['Variable, con género y número',
                                  'Solo singular',
                                  'Invariable',
                                  'Sin flexión alguna',
                                  'Solo masculina'],
                 'correcta': 'A'},
                {'pregunta': 'La función principal del adjetivo, según el '
                             'criterio sintáctico, es modificar '
                             'directamente:',
                 'alternativas': ['Al sustantivo',
                                  'A la conjunción',
                                  'Al adverbio',
                                  'A la preposición',
                                  'Al verbo'],
                 'correcta': 'A'},
                {'pregunta': 'Además de modificar al sustantivo, el adjetivo '
                             'puede funcionar como núcleo del:',
                 'alternativas': ['Vocativo',
                                  'Predicativo o atributo',
                                  'Complemento directo únicamente',
                                  'Complemento agente',
                                  'Sujeto exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos que expresan cualidades o '
                             'estados del sustantivo son los adjetivos:',
                 'alternativas': ['Numerales',
                                  'Posesivos',
                                  'Determinativos exclusivos',
                                  'Gentilicios',
                                  'Calificativos'],
                 'correcta': 'E'},
                {'pregunta': 'El adjetivo que precisa de qué sustantivo se '
                             'trata y puede restringir su extensión es el '
                             'adjetivo:',
                 'alternativas': ['Especificativo o restrictivo',
                                  'Gentilicio',
                                  'Posesivo',
                                  'Epíteto',
                                  'Explicativo'],
                 'correcta': 'A'},
                {'pregunta': 'El adjetivo que aparece entre pausas y no '
                             'tiene carga excluyente es el adjetivo:',
                 'alternativas': ['Especificativo',
                                  'Epíteto',
                                  'Numeral',
                                  'Explicativo o no restrictivo',
                                  'Gentilicio'],
                 'correcta': 'D'},
                {'pregunta': 'El adjetivo que señala una cualidad propia del '
                             'sustantivo, con valor poético cuando va '
                             'antepuesto, es el:',
                 'alternativas': ['Explicativo',
                                  'Gentilicio',
                                  'Especificativo',
                                  'Determinativo',
                                  'Epíteto'],
                 'correcta': 'A'},
                {'pregunta': 'En «blanca nieve», el adjetivo «blanca» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Gentilicio',
                                  'Numeral',
                                  'Especificativo',
                                  'Epíteto',
                                  'Explicativo'],
                 'correcta': 'D'},
                {'pregunta': 'En «Los jugadores, contentos con el resultado, '
                             'lo celebraron», el adjetivo «contentos» es:',
                 'alternativas': ['Posesivo',
                                  'Especificativo',
                                  'Gentilicio',
                                  'Explicativo',
                                  'Epíteto'],
                 'correcta': 'D'},
                {'pregunta': 'En «gatos negros», el adjetivo «negros» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Numeral',
                                  'Gentilicio',
                                  'Especificativo',
                                  'Explicativo',
                                  'Epíteto exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'Los adjetivos gentilicios califican al '
                             'sustantivo por su:',
                 'alternativas': ['Cantidad',
                                  'Color',
                                  'Forma',
                                  'Lugar de origen o procedencia',
                                  'Tamaño'],
                 'correcta': 'D'},
                {'pregunta': 'El sufijo «-eño/-eña» forma gentilicios como:',
                 'alternativas': ['Italiana',
                                  'Limeña',
                                  'Cordobés',
                                  'Chileno',
                                  'Bonaerense'],
                 'correcta': 'B'},
                {'pregunta': 'El sufijo «-ense» forma gentilicios como:',
                 'alternativas': ['Habanera',
                                  'Cordobés',
                                  'Limeña',
                                  'Italiana',
                                  'Bonaerense'],
                 'correcta': 'E'},
                {'pregunta': 'El sufijo «-és/-esa» forma gentilicios como:',
                 'alternativas': ['Europeo',
                                  'Chileno',
                                  'Bonaerense',
                                  'Cordobés',
                                  'Limeña'],
                 'correcta': 'D'},
                {'pregunta': 'En «El joven austriaco ganó un premio», el '
                             'adjetivo «austriaco» es un adjetivo:',
                 'alternativas': ['Explicativo',
                                  'Calificativo especificativo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Posesivo'],
                 'correcta': 'D'},
                {'pregunta': 'En «María llegó muy cansada», el adjetivo '
                             '«cansada» funciona como núcleo del:',
                 'alternativas': ['Sujeto',
                                  'Complemento directo',
                                  'Complemento indirecto',
                                  'Predicativo',
                                  'Vocativo'],
                 'correcta': 'D'},
                {'pregunta': 'En «La población está asustada», el adjetivo '
                             '«asustada» funciona como:',
                 'alternativas': ['Aposición',
                                  'Vocativo',
                                  'Complemento directo',
                                  'Sujeto',
                                  'Atributo'],
                 'correcta': 'E'},
                {'pregunta': 'El adjetivo epíteto, en posición pospuesta, '
                             'suele tener una intención:',
                 'alternativas': ['Coloquial',
                                  'Poética exclusiva',
                                  'Matemática',
                                  'Científica',
                                  'Legal'],
                 'correcta': 'A'},
                {'pregunta': 'En «lámpara portátil», el adjetivo «portátil» '
                             'cumple una función:',
                 'alternativas': ['Especificativa',
                                  'Numeral',
                                  'Explicativa',
                                  'Epíteto',
                                  'Gentilicia'],
                 'correcta': 'A'},
                {'pregunta': 'El adjetivo calificativo que precisa de qué '
                             'sustantivo se trata, restringiendo su '
                             'extensión, como en «gatos negros», se llama:',
                 'alternativas': ['Especificativo o restrictivo',
                                  'Numeral',
                                  'Determinativo',
                                  'Epíteto',
                                  'Explicativo'],
                 'correcta': 'A'},
                {'pregunta': 'El adjetivo calificativo que aparece entre '
                             'pausas, va antepuesto y no tiene carga '
                             'excluyente se llama:',
                 'alternativas': ['Epíteto',
                                  'Especificativo',
                                  'Explicativo o no restrictivo',
                                  'Numeral',
                                  'Posesivo'],
                 'correcta': 'C'},
                {'pregunta': 'El adjetivo calificativo que señala una '
                             'cualidad propia e inherente del sustantivo, '
                             'como en «blanca nieve», se llama:',
                 'alternativas': ['Epíteto',
                                  'Demostrativo',
                                  'Numeral',
                                  'Explicativo',
                                  'Especificativo'],
                 'correcta': 'A'},
                {'pregunta': 'El grado del adjetivo que expresa una cualidad '
                             'tal cual es, sin comparación, se llama grado:',
                 'alternativas': ['Comparativo',
                                  'Positivo',
                                  'Superlativo relativo',
                                  'Superlativo absoluto',
                                  'Epíteto'],
                 'correcta': 'B'},
                {'pregunta': 'El grado del adjetivo que establece una '
                             'comparación de superioridad, igualdad o '
                             'inferioridad se llama grado:',
                 'alternativas': ['Positivo',
                                  'Superlativo absoluto',
                                  'Comparativo',
                                  'Superlativo relativo',
                                  'Perifrástico exclusivo'],
                 'correcta': 'C'},
                {'pregunta': 'El grado superlativo absoluto que modifica el '
                             'adjetivo con adverbios como «muy» o '
                             '«sumamente» se llama superlativo absoluto:',
                 'alternativas': ['Sintético',
                                  'Comparativo',
                                  'Positivo',
                                  'Relativo',
                                  'Perifrástico'],
                 'correcta': 'E'},
                {'pregunta': 'El grado superlativo absoluto sintético de un '
                             'adjetivo terminado en -re o -ro se forma '
                             'añadiendo el sufijo:',
                 'alternativas': ['-mente',
                                  '-ísimo',
                                  '-perífrasis',
                                  '-érrimo',
                                  '-ando'],
                 'correcta': 'D'},
                {'pregunta': 'El superlativo absoluto sintético del adjetivo '
                             '«bueno» es:',
                 'alternativas': ['Bonísimo',
                                  'Buenísimo',
                                  'Optísimo',
                                  'Buenérrimo',
                                  'Mejorísimo'],
                 'correcta': 'A'},
                {'pregunta': 'El superlativo absoluto sintético del adjetivo '
                             '«libre» es:',
                 'alternativas': ['Libremente',
                                  'Librísimo',
                                  'Liberísimo',
                                  'Libertísimo',
                                  'Libérrimo'],
                 'correcta': 'E'},
                {'pregunta': 'El grado del adjetivo que maximiza o minimiza '
                             'la cualidad respecto a todos los de su misma '
                             'clase, como en «la más estudiosa del salón», '
                             'se llama superlativo:',
                 'alternativas': ['Absoluto sintético',
                                  'Absoluto perifrástico',
                                  'Positivo',
                                  'Relativo',
                                  'Comparativo'],
                 'correcta': 'D'},
                {'pregunta': 'La forma irregular o sincrética del '
                             'comparativo del adjetivo «bueno» es:',
                 'alternativas': ['Buenísimo',
                                  'Mejor',
                                  'Bonísimo',
                                  'Más bueno',
                                  'Óptimo'],
                 'correcta': 'B'},
                {'pregunta': 'La forma irregular o sincrética del '
                             'superlativo del adjetivo «grande» es:',
                 'alternativas': ['Mayor',
                                  'Magnísimo',
                                  'Máximo',
                                  'Más grande',
                                  'Grandísimo'],
                 'correcta': 'C'},
                {'pregunta': 'Los adjetivos que modifican al sustantivo '
                             'indicando la distancia de los seres respecto '
                             'al hablante (este, ese, aquel) se llaman '
                             'adjetivos:',
                 'alternativas': ['Calificativos',
                                  'Demostrativos',
                                  'Posesivos',
                                  'Numerales',
                                  'Gentilicios'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos numerales que expresan cantidad '
                             'exacta, como «cinco delincuentes», se llaman:',
                 'alternativas': ['Múltiplos',
                                  'Cardinales',
                                  'Indefinidos',
                                  'Ordinales',
                                  'Partitivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos numerales que indican fracción '
                             'de la unidad, como «media manzana», se llaman:',
                 'alternativas': ['Indefinidos',
                                  'Partitivos',
                                  'Ordinales',
                                  'Cardinales',
                                  'Múltiplos'],
                 'correcta': 'B'},
                {'pregunta': 'La supresión de sonidos al final de ciertas '
                             'palabras, como en «gran chico» en vez de '
                             '«grande chico», se llama:',
                 'alternativas': ['Sinalefa',
                                  'Apócope',
                                  'Sinéresis',
                                  'Elisión',
                                  'Diéresis'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos apócope pierden su vocal final '
                             'cuando van delante de un sustantivo masculino '
                             'singular; en su forma femenina:',
                 'alternativas': ['Quedan intactos',
                                  'Se duplican',
                                  'Cambian de raíz',
                                  'Se convierten en pronombres',
                                  'También se apocopan'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CRITERIOS PARA DEFINIR EL ADJETIVO / '
                                'ADJETIVOS CALIFICATIVOS',
                      'items': ['Según el criterio semántico, el adjetivo '
                                'agrega información o califica al '
                                'sustantivo, y también lo determina.',
                                'Según el criterio morfológico, el adjetivo '
                                'es una palabra variable con morfemas de '
                                'género y número.',
                                'Los adjetivos calificativos expresan '
                                'cualidades o estados del sustantivo al cual '
                                'modifican.',
                                'El adjetivo especificativo o restrictivo '
                                'precisa de qué sustantivo se trata y puede '
                                'restringir su extensión.']},
                     {'titulo': 'ADJETIVOS GENTILICIOS / TIPOS DE ADJETIVO '
                                'CALIFICATIVO',
                      'items': ['Los adjetivos gentilicios califican al '
                                'sustantivo por su lugar de origen o '
                                'procedencia.',
                                'El sufijo -eño/-eña forma gentilicios como '
                                '«limeña»; el sufijo -ense forma gentilicios '
                                'como «bonaerense».',
                                'El adjetivo calificativo especificativo o '
                                'restrictivo precisa de qué sustantivo se '
                                'trata, restringiendo su extensión: «gatos '
                                'negros», «alumno aplicado».',
                                'El adjetivo calificativo explicativo o no '
                                'restrictivo aparece entre pausas, va '
                                'antepuesto y no tiene carga excluyente: «El '
                                'misterioso gato sufrió una quemadura».']},
                     {'titulo': 'GRADO POSITIVO Y COMPARATIVO / SUPERLATIVO '
                                'ABSOLUTO PERIFRÁSTICO Y SINTÉTIC',
                      'items': ['El grado positivo expresa una cualidad '
                                'atribuida al sustantivo tal cual es, sin '
                                'comparación: «joven estudioso».',
                                'El grado comparativo nombra la cualidad '
                                'estableciendo una comparación; puede ser de '
                                'superioridad (más... que), igualdad (tan... '
                                'como) o inferioridad (menos... que).',
                                'El superlativo absoluto expresa la cualidad '
                                'en sumo grado, sin comparación.',
                                'El superlativo absoluto perifrástico '
                                'modifica el adjetivo con adverbios como '
                                'muy, sumamente, extremadamente: «Mi hermana '
                                'es muy hermosa».']},
                     {'titulo': 'SUPERLATIVO RELATIVO Y FORMAS IRREGULARES / '
                                'ADJETIVOS DETERMINATIVOS: DEMOS',
                      'items': ['El superlativo relativo maximiza o minimiza '
                                'la cualidad en relación a todos los de su '
                                'misma clase: «Aquella alumna es la más '
                                'estudiosa del salón».',
                                'Las formas irregulares o sincréticas del '
                                'adjetivo no siguen las reglas generales: '
                                'bueno→mejor→óptimo; malo→peor→pésimo; '
                                'grande→mayor→máximo; pequeño→menor→mínimo.',
                                'Los adjetivos demostrativos modifican al '
                                'sustantivo indicando la distancia de los '
                                'seres respecto al hablante: este/esta, '
                                'ese/esa, aquel/aquella.',
                                'Los adjetivos posesivos modifican al '
                                'sustantivo indicando posesión: mi(s), '
                                'tu(s), su(s), nuestro(s), vuestro(s).']},
                     {'titulo': 'ADJETIVOS NUMERALES / APÓCOPE DEL ADJETIVO',
                      'items': ['Los adjetivos numerales modifican al '
                                'sustantivo indicando cantidad y número '
                                'exactos.',
                                'Los cardinales expresan cantidad exacta: '
                                'cinco delincuentes, tres soles.',
                                'El apócope es la supresión de sonidos al '
                                'final de ciertas palabras.',
                                'Los adjetivos apócope pierden la -o final '
                                'cuando van delante de un sustantivo '
                                'masculino singular; en femenino quedan '
                                'intactos.']}]},
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
                {'titulo': '11.4 FUNCIONES Y VALORES DEL ARTÍCULO',
                 'items': ['El artículo {determinado} actúa como presentador '
                           'del sustantivo, dando mayor viveza a la '
                           'expresión: «La Historia del hombre...».',
                           'El artículo {indeterminado} «un» y sus variantes '
                           'dan mayor énfasis a la expresión: «Eres un '
                           'candidato del pueblo».',
                           'El artículo funciona como {desambiguador} de '
                           'género y número: el oyente/la oyente; la '
                           'caries/las caries.',
                           'Cuando dos adjetivos modifican a un sustantivo, '
                           'el artículo debe preceder solo al {primer} '
                           'adjetivo: «El débil y triste mendigo...».',
                           'El uso del artículo es {opcional} en algunos '
                           'países: Perú/El Perú; no acepta artículo '
                           'Bolivia, Chile, Colombia.',
                           'Por razones de {eufonía}, los sustantivos '
                           'femeninos que empiezan con «a» o «ha» tónicas se '
                           'anteponen del artículo «{el}» en singular: el '
                           'águila, el agua, el arma.',
                           'En plural, estos sustantivos vuelven a usar el '
                           'artículo femenino que corresponde: las águilas, '
                           'las {aguas}.',
                           'El artículo es {sustantivador} universal: al '
                           'anteponerse a una palabra de otra categoría, la '
                           'convierte en sustantivo: «El {inteligente} '
                           'superó a todos».']},
                {'titulo': '11.5 EL ADVERBIO',
                 'items': ['El adverbio es una palabra {invariable} que '
                           'modifica al verbo, al adjetivo o a otro '
                           'adverbio.',
                           'Los adverbios se clasifican según su significado '
                           'en adverbios de {lugar}, tiempo, modo, cantidad, '
                           'afirmación, negación y duda.']},
                {'titulo': '11.6 CLASES DE ADVERBIOS (I)',
                 'items': ['Los adverbios de {lugar} indican situación o '
                           'ubicación: aquí, allá, cerca, lejos, {delante}, '
                           'detrás.',
                           'Los adverbios de {tiempo} indican período o '
                           'suceso: hoy, ayer, siempre, {pronto}, todavía, '
                           'ahora.',
                           'Los adverbios de {modo} indican manera o '
                           'procedimiento: bien, mal, {despacio}, aprisa, '
                           'así.',
                           'Los adverbios de {cantidad} indican grado o '
                           'porción: poco, mucho, tanto, {demasiado}, casi, '
                           'bastante.',
                           'Los adverbios terminados en {-mente} son en su '
                           'mayoría adverbios de modo, formados por un '
                           'adjetivo más el sufijo -mente: rápidamente, '
                           '{felizmente}.']},
                {'titulo': '11.7 CLASES DE ADVERBIOS (II)',
                 'items': ['Los adverbios de {orden} indican sucesión: '
                           'primeramente, {seguidamente}, finalmente.',
                           'Los adverbios de {afirmación} indican certeza: '
                           'sí, ciertamente, {seguramente}, efectivamente.',
                           'Los adverbios de {negación} indican objeción o '
                           'contradicción: no, {nunca}, jamás, tampoco.',
                           'Los adverbios de {duda} indican incertidumbre: '
                           'quizás, {tal vez}, acaso, a lo mejor.']},
                {'titulo': '11.8 USOS CORRECTOS DEL ADVERBIO',
                 'items': ['Es {incorrecto} decir «Lo encontré abajo de la '
                           'mesa»; lo correcto es «Lo encontré {debajo} de '
                           'la mesa».',
                           'Es incorrecto decir «Íbamos adelante del '
                           'profesor»; lo correcto es «Íbamos {delante} del '
                           'profesor».',
                           'Es incorrecto decir «Se puso atrás de ti»; lo '
                           'correcto es «Se puso {detrás} de ti».']}],
  'cuadros': [{'titulo': '11.2 CLASES DE ARTÍCULO',
               'encabezados': ['Clase', 'Masculino singular', 'Referencia'],
               'filas': [['{Determinado}', 'El', 'Sustantivo {conocido}'],
                         ['{Indeterminado}', 'Un', 'Ser {no} conocido'],
                         ['{Neutro}', 'Lo', 'Sustantiva {adjetivos}']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, el artículo '
                             'carece de significado lexical pero posee '
                             'significado:',
                 'alternativas': ['Ninguno',
                                  'Gramatical',
                                  'Fonológico',
                                  'Morfológico exclusivo',
                                  'Pragmático'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo, en su posición dentro de la '
                             'oración, siempre:',
                 'alternativas': ['Aparece solo en plural',
                                  'Sigue al sustantivo',
                                  'Reemplaza al verbo',
                                  'Se ubica al final de la oración',
                                  'Precede al sustantivo'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio morfológico, el artículo '
                             'concuerda con el sustantivo en:',
                 'alternativas': ['Aspecto verbal',
                                  'Solo persona gramatical',
                                  'Género y número',
                                  'Solo tiempo verbal',
                                  'Modo verbal'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo que hace referencia a un '
                             'sustantivo conocido por el hablante se llama '
                             'artículo:',
                 'alternativas': ['Indeterminado',
                                  'Demostrativo',
                                  'Neutro',
                                  'Posesivo',
                                  'Determinado'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo que hace referencia a seres no '
                             'conocidos se llama artículo:',
                 'alternativas': ['Definido',
                                  'Indeterminado',
                                  'Neutro',
                                  'Determinado',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo neutro del español es:',
                 'alternativas': ['La', 'El', 'Lo', 'Un', 'Una'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo neutro «lo» sirve para '
                             'sustantivar:',
                 'alternativas': ['Preposiciones',
                                  'Artículos',
                                  'Verbos',
                                  'Conjunciones',
                                  'Adjetivos'],
                 'correcta': 'E'},
                {'pregunta': 'En «Lo bueno supervive a través del tiempo», '
                             '«lo bueno» funciona como un sustantivo:',
                 'alternativas': ['Propio',
                                  'Abstracto',
                                  'Concreto',
                                  'Contable',
                                  'Colectivo'],
                 'correcta': 'B'},
                {'pregunta': 'El único artículo que se puede contraer es:',
                 'alternativas': ['El', 'Los', 'Un', 'Las', 'La'],
                 'correcta': 'A'},
                {'pregunta': 'El artículo «el» se contrae con las '
                             'preposiciones «a» y:',
                 'alternativas': ['Sin', 'Para', 'De', 'Por', 'Con'],
                 'correcta': 'C'},
                {'pregunta': 'La contracción de «a» más «el» da como '
                             'resultado:',
                 'alternativas': ['A el siempre', 'Aal', 'Ael', 'Del', 'Al'],
                 'correcta': 'E'},
                {'pregunta': 'La contracción de «de» más «el» da como '
                             'resultado:',
                 'alternativas': ['Dell',
                                  'Del',
                                  'Al',
                                  'Dle',
                                  'De el siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Las contracciones del artículo se usan '
                             'solamente ante sustantivos:',
                 'alternativas': ['Colectivos exclusivos',
                                  'Contables únicamente',
                                  'Abstractos',
                                  'Comunes',
                                  'Propios siempre'],
                 'correcta': 'D'},
                {'pregunta': 'Si el artículo forma parte de un topónimo, '
                             'como «El Salvador», la contracción:',
                 'alternativas': ['No procede',
                                  'Es obligatoria',
                                  'Depende del contexto oral',
                                  'Se aplica solo por escrito',
                                  'Es opcional siempre'],
                 'correcta': 'A'},
                {'pregunta': 'En «Viajaremos a El Cairo», la ausencia de '
                             'contracción se debe a que:',
                 'alternativas': ['Es una excepción sin explicación',
                                  'El Cairo no es un lugar real',
                                  'Es un error ortográfico',
                                  'La preposición no lo permite nunca',
                                  'El artículo forma parte del topónimo'],
                 'correcta': 'E'},
                {'pregunta': 'El adverbio, en cuanto a su morfología, es una '
                             'palabra:',
                 'alternativas': ['Con flexión verbal',
                                  'Solo masculina',
                                  'Variable en género y número',
                                  'Solo plural',
                                  'Invariable'],
                 'correcta': 'E'},
                {'pregunta': 'El adverbio puede modificar al verbo, al '
                             'adjetivo o:',
                 'alternativas': ['A otro adverbio',
                                  'A la conjunción',
                                  'Al pronombre exclusivamente',
                                  'Al artículo',
                                  'Al sustantivo directamente'],
                 'correcta': 'A'},
                {'pregunta': 'Los adverbios se clasifican, entre otras '
                             'categorías, en adverbios de lugar, tiempo y:',
                 'alternativas': ['Caso',
                                  'Persona',
                                  'Género',
                                  'Número',
                                  'Modo'],
                 'correcta': 'E'},
                {'pregunta': 'En «El ayer quedó en olvido», el artículo «el» '
                             'sustantiva a:',
                 'alternativas': ['Un verbo',
                                  'Un adjetivo',
                                  'Un adverbio temporal',
                                  'Una preposición',
                                  'Una conjunción'],
                 'correcta': 'C'},
                {'pregunta': 'En «Un día te entregaré unos regalos», los '
                             'artículos usados son de tipo:',
                 'alternativas': ['Neutro',
                                  'Indeterminado',
                                  'Contraído',
                                  'Demostrativo',
                                  'Determinado'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo indeterminado «un» y sus variantes '
                             'sirven, entre otras cosas, para:',
                 'alternativas': ['Eliminar el sustantivo',
                                  'Convertir el sustantivo en verbo',
                                  'Pluralizar el sustantivo',
                                  'Restar énfasis a la expresión',
                                  'Dar mayor énfasis a la expresión'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo funciona como desambiguador de '
                             'género y número en casos como «el oyente» / '
                             '«la oyente», es decir, como:',
                 'alternativas': ['Sustantivador',
                                  'Diminutivo',
                                  'Intensificador',
                                  'Desambiguador',
                                  'Pluralizador'],
                 'correcta': 'D'},
                {'pregunta': 'Cuando dos adjetivos calificativos modifican a '
                             'un mismo sustantivo, el artículo debe '
                             'preceder:',
                 'alternativas': ['Al sustantivo dos veces',
                                  'A ambos adjetivos',
                                  'Solo al segundo adjetivo',
                                  'Solo al primer adjetivo',
                                  'A ninguno de los adjetivos'],
                 'correcta': 'D'},
                {'pregunta': 'Por razones de eufonía, los sustantivos '
                             'femeninos que empiezan con «a» o «ha» tónicas, '
                             'en singular, se anteponen del artículo:',
                 'alternativas': ['La', 'Los', 'Un', 'El', 'Las'],
                 'correcta': 'D'},
                {'pregunta': 'En «Las águilas», al pasar al plural, el '
                             'sustantivo femenino que empieza con «a» tónica '
                             'recupera el artículo:',
                 'alternativas': ['Un',
                                  'Uno',
                                  'Lo',
                                  'El',
                                  'La forma femenina «las»'],
                 'correcta': 'E'},
                {'pregunta': 'El artículo es considerado sustantivador '
                             'universal porque, al anteponerse a una palabra '
                             'de otra categoría gramatical, la convierte en:',
                 'alternativas': ['Pronombre',
                                  'Sustantivo',
                                  'Adjetivo',
                                  'Adverbio',
                                  'Verbo'],
                 'correcta': 'B'},
                {'pregunta': 'Los adverbios que indican situación o '
                             'ubicación, como «aquí» o «lejos», se llaman '
                             'adverbios de:',
                 'alternativas': ['Lugar',
                                  'Tiempo',
                                  'Orden',
                                  'Cantidad',
                                  'Modo'],
                 'correcta': 'A'},
                {'pregunta': 'Los adverbios que indican período o suceso, '
                             'como «ayer» o «pronto», se llaman adverbios '
                             'de:',
                 'alternativas': ['Lugar',
                                  'Tiempo',
                                  'Duda',
                                  'Modo',
                                  'Cantidad'],
                 'correcta': 'B'},
                {'pregunta': 'Los adverbios que indican manera o '
                             'procedimiento, como «despacio» o «bien», se '
                             'llaman adverbios de:',
                 'alternativas': ['Modo',
                                  'Afirmación',
                                  'Orden',
                                  'Lugar',
                                  'Cantidad'],
                 'correcta': 'A'},
                {'pregunta': 'Los adverbios que indican grado o porción, '
                             'como «demasiado» o «casi», se llaman adverbios '
                             'de:',
                 'alternativas': ['Modo',
                                  'Tiempo',
                                  'Cantidad',
                                  'Duda',
                                  'Orden'],
                 'correcta': 'C'},
                {'pregunta': 'La mayoría de los adverbios terminados en '
                             '«-mente», como «rápidamente», son adverbios '
                             'de:',
                 'alternativas': ['Lugar',
                                  'Cantidad',
                                  'Modo',
                                  'Tiempo',
                                  'Orden'],
                 'correcta': 'C'},
                {'pregunta': 'Los adverbios que indican sucesión, como '
                             '«primeramente» o «finalmente», se llaman '
                             'adverbios de:',
                 'alternativas': ['Modo',
                                  'Cantidad',
                                  'Lugar',
                                  'Duda',
                                  'Orden'],
                 'correcta': 'E'},
                {'pregunta': 'Los adverbios que indican incertidumbre o '
                             'vacilación, como «quizás» o «tal vez», se '
                             'llaman adverbios de:',
                 'alternativas': ['Duda',
                                  'Modo',
                                  'Afirmación',
                                  'Orden',
                                  'Negación'],
                 'correcta': 'A'},
                {'pregunta': 'Es incorrecto decir «Lo encontré abajo de la '
                             'mesa»; la forma correcta es:',
                 'alternativas': ['Lo encontré por abajo la mesa',
                                  'Lo encontré bajo de la mesa',
                                  'Lo encontré debajo de la mesa',
                                  'Todas son correctas',
                                  'Lo encontré abajo la mesa'],
                 'correcta': 'C'},
                {'pregunta': 'Es incorrecto decir «Íbamos adelante del '
                             'profesor»; la forma correcta es:',
                 'alternativas': ['Todas son correctas',
                                  'Íbamos por adelante el profesor',
                                  'Íbamos delante del profesor',
                                  'Íbamos en adelante el profesor',
                                  'Íbamos adelante al profesor'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'CRITERIOS DEL ARTÍCULO',
                      'items': ['Según el criterio semántico, el artículo '
                                'carece de significado lexical propio, pero '
                                'posee significado gramatical.',
                                'El artículo siempre precede al sustantivo.',
                                'Según el criterio morfológico, el artículo '
                                'es una palabra variable que concuerda en '
                                'género y número con el sustantivo.']},
                     {'titulo': 'CLASIFICACIÓN DEL ARTÍCULO',
                      'items': ['El artículo determinado, o definido, hace '
                                'referencia a un sustantivo conocido: el, '
                                'la, los, las.',
                                'El artículo indeterminado, o indefinido, '
                                'hace referencia a seres no conocidos: un, '
                                'una, unos, unas.',
                                'El artículo neutro «lo» sirve para '
                                'sustantivar a los adjetivos, '
                                'convirtiéndolos en sustantivos '
                                'abstractos.']},
                     {'titulo': 'LA CONTRACCIÓN DEL ARTÍCULO',
                      'items': ['El único artículo que puede contraerse es '
                                'el, cuando se une a las preposiciones a o '
                                'de.',
                                'La preposición «a» más «el» forma la '
                                'contracción al; la preposición «de» más '
                                '«el» forma la contracción del.',
                                'Las contracciones se usan solo ante '
                                'sustantivos comunes.']},
                     {'titulo': 'FUNCIONES Y VALORES DEL ARTÍCULO',
                      'items': ['El artículo determinado actúa como '
                                'presentador del sustantivo, dando mayor '
                                'viveza a la expresión: «La Historia del '
                                'hombre...».',
                                'El artículo indeterminado «un» y sus '
                                'variantes dan mayor énfasis a la expresión: '
                                '«Eres un candidato del pueblo».',
                                'El artículo funciona como desambiguador de '
                                'género y número: el oyente/la oyente; la '
                                'caries/las caries.']},
                     {'titulo': 'EL ADVERBIO',
                      'items': ['El adverbio es una palabra invariable que '
                                'modifica al verbo, al adjetivo o a otro '
                                'adverbio.',
                                'Los adverbios se clasifican según su '
                                'significado en adverbios de lugar, tiempo, '
                                'modo, cantidad, afirmación, negación y '
                                'duda.']},
                     {'titulo': 'CLASES DE ADVERBIOS (I)',
                      'items': ['Los adverbios de lugar indican situación o '
                                'ubicación: aquí, allá, cerca, lejos, '
                                'delante, detrás.',
                                'Los adverbios de tiempo indican período o '
                                'suceso: hoy, ayer, siempre, pronto, '
                                'todavía, ahora.',
                                'Los adverbios de modo indican manera o '
                                'procedimiento: bien, mal, despacio, aprisa, '
                                'así.']},
                     {'titulo': 'CLASES DE ADVERBIOS (II)',
                      'items': ['Los adverbios de orden indican sucesión: '
                                'primeramente, seguidamente, finalmente.',
                                'Los adverbios de afirmación indican '
                                'certeza: sí, ciertamente, seguramente, '
                                'efectivamente.',
                                'Los adverbios de negación indican objeción '
                                'o contradicción: no, nunca, jamás, '
                                'tampoco.']},
                     {'titulo': 'USOS CORRECTOS DEL ADVERBIO',
                      'items': ['Es incorrecto decir «Lo encontré abajo de '
                                'la mesa»; lo correcto es «Lo encontré '
                                'debajo de la mesa».',
                                'Es incorrecto decir «Íbamos adelante del '
                                'profesor»; lo correcto es «Íbamos delante '
                                'del profesor».',
                                'Es incorrecto decir «Se puso atrás de ti»; '
                                'lo correcto es «Se puso detrás de ti».']}]},
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
                {'titulo': '12.5 ACCIDENTES GRAMATICALES: PERSONA, NÚMERO Y '
                           'TIEMPO',
                 'items': ['El accidente {número} expresa la cantidad de '
                           'personas que realizan la acción: singular o '
                           '{plural}.',
                           'El accidente {persona} hace referencia a quién '
                           'realiza la acción: primera (yo), {segunda} (tú), '
                           'tercera (él).',
                           'El accidente {tiempo} indica la época en que se '
                           'realiza la acción: pasado, {presente} o futuro.',
                           'El {tiempo simple} expresa la acción con una '
                           'sola palabra; el tiempo {compuesto} usa el '
                           'auxiliar haber más el participio: «ha '
                           'viajado».']},
                {'titulo': '12.6 ACCIDENTES GRAMATICALES: ASPECTO Y MODO',
                 'items': ['El {aspecto} señala si la acción está concluida '
                           'o en proceso: {imperfectivo} (cantaba, no '
                           'concluida), perfectivo (he cantado, concluida) y '
                           'neutro (cantaré).',
                           'El {modo indicativo} afirma o niega la acción de '
                           'manera real y objetiva, con seguridad: «Manuel '
                           '{escribe} poemas».',
                           'El {modo subjuntivo} expresa la acción de manera '
                           'subjetiva, como deseo o duda: «Queremos que '
                           'Manuel {escriba} poemas».',
                           'El {modo imperativo} expresa la acción como '
                           'orden o ruego, dirigida a la segunda persona: '
                           '«{Estudien} con esmero, jóvenes».',
                           'La {voz} indica si el sujeto es activo (realiza '
                           'la acción) o {pasivo} (la recibe): «El profesor '
                           'asesora» (activa) / «Los alumnos son asesorados» '
                           '(pasiva).']},
                {'titulo': '12.7 VERBOS AUXILIARES',
                 'items': ['Los verbos {auxiliares} auxilian a los verboides '
                           'en su conjugación: ser, {haber} y estar.',
                           'El auxiliar {ser} sirve para formar la voz '
                           '{pasiva}: «Un tema nuevo fue interpretado por '
                           'Leo Dan».',
                           'El auxiliar {haber} sirve para formar los '
                           'tiempos {compuestos}: «Lilia ha bailado con '
                           'Fredy».',
                           'El auxiliar {estar} actúa como auxiliar de un '
                           '{gerundio}: «Estoy amando apasionadamente».']},
                {'titulo': '12.8 LOS VERBOIDES: INFINITIVO Y GERUNDIO',
                 'items': ['Los {verboides} son formas no personales del '
                           'verbo, porque no están conjugados en ninguna '
                           '{persona}.',
                           'El {infinitivo} es la forma sustantiva del '
                           'verbo, cumple función de núcleo del sujeto y '
                           'termina en -ar, -er, -ir.',
                           'El infinitivo {simple} carece de verbo auxiliar: '
                           '«El {amar} es maravilloso».',
                           'El infinitivo {compuesto} se forma con haber más '
                           'el participio: «El {haber} vivido contigo fue '
                           'fascinante».',
                           'El {gerundio} es la forma adverbial del verbo, '
                           'funciona como circunstancial.',
                           'El gerundio {simple} termina en -ando o -iendo: '
                           '«Ella vive {amando}».',
                           'El gerundio {compuesto} se forma con habiendo '
                           'más participio: «{Habiendo} sufrido, ahora vive '
                           'tranquilo».']},
                {'titulo': '12.9 LOS VERBOIDES: EL PARTICIPIO',
                 'items': ['El {participio} es la forma adjetiva y '
                           'sustantiva del verbo, expresa acción terminada '
                           '(valor {perfectivo}) y presenta flexiones de '
                           'género y número.',
                           'El participio pasivo {regular} termina en -ado, '
                           '-ido: niño {amado}, momento vivido.',
                           'El participio pasivo {irregular} termina en '
                           '-cho, -to, -so, -jo, -vo: cliente {satisfecho}, '
                           'documento escrito, libro impreso.',
                           'El participio {activo} termina en -ante, -iente, '
                           '-ente, -ador, -edor, -idor, y funciona como '
                           'sustantivo o adjetivo: el {oyente}, el '
                           'gobernador.']}],
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
                 'alternativas': ['Existencia',
                                  'Solo lugar',
                                  'Solo cantidad',
                                  'Solo posesión',
                                  'Solo cualidad'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio morfológico, el verbo '
                             'presenta accidentes de número, persona, '
                             'tiempo, modo y:',
                 'alternativas': ['Género',
                                  'Aspecto',
                                  'Grado',
                                  'Caso',
                                  'Especie'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio sintáctico, el verbo '
                             'funciona como núcleo:',
                 'alternativas': ['Del vocativo',
                                  'Del complemento agente exclusivo',
                                  'Del sujeto',
                                  'De la aposición',
                                  'Del predicado verbal'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos que sirven de nexo entre el sujeto '
                             'y su atributo se llaman verbos:',
                 'alternativas': ['Reflexivos',
                                  'Recíprocos',
                                  'Copulativos',
                                  'Transitivos',
                                  'Impersonales'],
                 'correcta': 'C'},
                {'pregunta': 'Un ejemplo de verbo copulativo es:',
                 'alternativas': ['Correr',
                                  'Ser',
                                  'Escribir',
                                  'Comer',
                                  'Saltar'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que expresan por sí solos una idea '
                             'con sentido pleno se llaman verbos:',
                 'alternativas': ['Auxiliares',
                                  'No copulativos o predicativos',
                                  'Semicopulativos únicamente',
                                  'Impersonales exclusivos',
                                  'Copulativos'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que tienen complemento directo se '
                             'llaman verbos:',
                 'alternativas': ['Recíprocos exclusivos',
                                  'Impersonales',
                                  'Intransitivos',
                                  'Copulativos',
                                  'Transitivos'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos que no tienen complemento directo '
                             'se llaman verbos:',
                 'alternativas': ['Reflexivos exclusivos',
                                  'Transitivos',
                                  'Intransitivos',
                                  'Copulativos',
                                  'Recíprocos'],
                 'correcta': 'C'},
                {'pregunta': 'Los verbos cuya acción recae sobre el mismo '
                             'sujeto que la realiza se llaman verbos:',
                 'alternativas': ['Recíprocos',
                                  'Copulativos',
                                  'Reflexivos',
                                  'Transitivos exclusivos',
                                  'Impersonales'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter reflexivo de un verbo se comprueba '
                             'añadiendo el refuerzo:',
                 'alternativas': ['«Mismo(a)»',
                                  '«Uno a otro»',
                                  '«Mutuamente»',
                                  '«Entre sí»',
                                  '«Recíprocamente»'],
                 'correcta': 'A'},
                {'pregunta': 'Los verbos que usan pronombres como énfasis '
                             'sin representar transitividad se llaman '
                             'verbos:',
                 'alternativas': ['Transitivos',
                                  'Recíprocos',
                                  'Copulativos',
                                  'Reflexivos',
                                  'Cuasireflexivos'],
                 'correcta': 'E'},
                {'pregunta': 'Los verbos cuasireflexivos, a diferencia de '
                             'los reflexivos, NO aceptan el refuerzo:',
                 'alternativas': ['Ninguno de los anteriores',
                                  '«Mutuamente»',
                                  '«Recíprocamente»',
                                  '«Mismo(a)»',
                                  '«Entre todos»'],
                 'correcta': 'D'},
                {'pregunta': 'Los verbos con sujeto plural que ejercen una '
                             'acción mutua entre ellos se llaman verbos:',
                 'alternativas': ['Transitivos',
                                  'Cuasireflexivos',
                                  'Impersonales',
                                  'Reflexivos',
                                  'Recíprocos'],
                 'correcta': 'E'},
                {'pregunta': 'El carácter recíproco de un verbo se comprueba '
                             'con el refuerzo:',
                 'alternativas': ['«Exclusivamente»',
                                  '«A sí mismo»',
                                  '«Solamente»',
                                  '«Mutuamente» o «recíprocamente»',
                                  '«Mismo(a)»'],
                 'correcta': 'D'},
                {'pregunta': 'Los verbos cuyo sujeto se desconoce o no se '
                             'precisa se llaman verbos:',
                 'alternativas': ['Reflexivos',
                                  'Transitivos',
                                  'Impersonales',
                                  'Recíprocos',
                                  'Copulativos'],
                 'correcta': 'C'},
                {'pregunta': '«Llovió en Cusco» es un ejemplo de verbo '
                             'impersonal referido a:',
                 'alternativas': ['Una acción transitiva',
                                  'Una acción recíproca',
                                  'Un fenómeno de la naturaleza',
                                  'Un fenómeno social',
                                  'Un verbo copulativo'],
                 'correcta': 'C'},
                {'pregunta': '«Se traspasa local comercial» ejemplifica un '
                             'verbo impersonal con el signo:',
                 'alternativas': ['De pasiva refleja exclusiva',
                                  'De reflexividad',
                                  'De copulación',
                                  'De impersonalidad pronominal «se»',
                                  'De reciprocidad'],
                 'correcta': 'D'},
                {'pregunta': '«Dicen que te vas a casar» ejemplifica un '
                             'verbo impersonal porque:',
                 'alternativas': ['Tiene complemento directo explícito',
                                  'Expresa un fenómeno natural',
                                  'No se conoce o no se quiere dar a conocer '
                                  'el sujeto',
                                  'Es un verbo copulativo',
                                  'El sujeto es plural y conocido'],
                 'correcta': 'C'},
                {'pregunta': 'En «Yo me caigo», a diferencia de «yo caigo», '
                             'el pronombre «me»:',
                 'alternativas': ['Da solo énfasis, sin representar '
                                  'transitividad',
                                  'Sustituye al sujeto',
                                  'Indica reciprocidad',
                                  'Es un artículo neutro',
                                  'Funciona como complemento directo'],
                 'correcta': 'A'},
                {'pregunta': 'Los verbos «ser», «estar» y «parecer» '
                             'pertenecen a la clase de verbos:',
                 'alternativas': ['Cuasireflexivos',
                                  'Copulativos',
                                  'Impersonales',
                                  'Recíprocos',
                                  'Transitivos'],
                 'correcta': 'B'},
                {'pregunta': 'El accidente gramatical del verbo que expresa '
                             'la cantidad de personas que realizan la acción '
                             'se llama:',
                 'alternativas': ['Persona',
                                  'Modo',
                                  'Tiempo',
                                  'Aspecto',
                                  'Número'],
                 'correcta': 'E'},
                {'pregunta': 'El accidente gramatical del verbo que hace '
                             'referencia al ser que realiza la acción (yo, '
                             'tú, él) se llama:',
                 'alternativas': ['Voz',
                                  'Número',
                                  'Aspecto',
                                  'Tiempo',
                                  'Persona'],
                 'correcta': 'E'},
                {'pregunta': 'El tiempo verbal formado por el auxiliar haber '
                             'más el participio, como «ha viajado», se llama '
                             'tiempo:',
                 'alternativas': ['Neutro',
                                  'Perfectivo exclusivo',
                                  'Imperfectivo exclusivo',
                                  'Compuesto',
                                  'Simple'],
                 'correcta': 'D'},
                {'pregunta': 'El aspecto verbal que señala que la acción '
                             'está concluida, sin posibilidad de repetirse, '
                             'como «he cantado», se llama aspecto:',
                 'alternativas': ['Compuesto exclusivo',
                                  'Neutro',
                                  'Simple',
                                  'Perfectivo',
                                  'Imperfectivo'],
                 'correcta': 'D'},
                {'pregunta': 'El modo verbal que afirma o niega la acción de '
                             'manera real y objetiva, con seguridad, se '
                             'llama modo:',
                 'alternativas': ['Imperativo',
                                  'Potencial',
                                  'Condicional',
                                  'Subjuntivo',
                                  'Indicativo'],
                 'correcta': 'E'},
                {'pregunta': 'El modo verbal que expresa la acción de manera '
                             'subjetiva, como deseo o duda, se llama modo:',
                 'alternativas': ['Imperativo',
                                  'Neutro',
                                  'Indicativo',
                                  'Subjuntivo',
                                  'Potencial'],
                 'correcta': 'D'},
                {'pregunta': 'El modo verbal que expresa la acción como '
                             'orden, mandato o ruego dirigido a la segunda '
                             'persona se llama modo:',
                 'alternativas': ['Indicativo',
                                  'Condicional',
                                  'Potencial',
                                  'Subjuntivo',
                                  'Imperativo'],
                 'correcta': 'E'},
                {'pregunta': 'En la construcción sintáctica «Los alumnos son '
                             'asesorados por el profesor», la voz empleada '
                             'es la voz:',
                 'alternativas': ['Pasiva',
                                  'Impersonal',
                                  'Media',
                                  'Refleja',
                                  'Activa'],
                 'correcta': 'A'},
                {'pregunta': 'El verbo auxiliar que sirve para formar la voz '
                             'pasiva es:',
                 'alternativas': ['Ir', 'Haber', 'Ser', 'Tener', 'Estar'],
                 'correcta': 'C'},
                {'pregunta': 'El verbo auxiliar que sirve para formar los '
                             'tiempos compuestos es:',
                 'alternativas': ['Estar', 'Haber', 'Ser', 'Tener', 'Ir'],
                 'correcta': 'B'},
                {'pregunta': 'El verbo auxiliar que actúa como auxiliar de '
                             'un gerundio, como en «Estoy amando», es:',
                 'alternativas': ['Ser', 'Haber', 'Andar', 'Estar', 'Ir'],
                 'correcta': 'B'},
                {'pregunta': 'Las formas no personales del verbo, porque no '
                             'están conjugadas en ninguna persona, se '
                             'llaman:',
                 'alternativas': ['Voces',
                                  'Aspectos',
                                  'Verboides',
                                  'Accidentes',
                                  'Modos'],
                 'correcta': 'C'},
                {'pregunta': 'La forma sustantiva del verbo, que cumple '
                             'función de núcleo del sujeto y termina en -ar, '
                             '-er, -ir, se llama:',
                 'alternativas': ['Infinitivo',
                                  'Gerundio',
                                  'Voz activa',
                                  'Participio',
                                  'Modo indicativo'],
                 'correcta': 'A'},
                {'pregunta': 'La forma adverbial del verbo, que '
                             'sintácticamente funciona como circunstancial y '
                             'termina en -ando o -iendo, se llama:',
                 'alternativas': ['Infinitivo',
                                  'Voz pasiva',
                                  'Modo subjuntivo',
                                  'Gerundio',
                                  'Participio'],
                 'correcta': 'D'},
                {'pregunta': 'La forma adjetiva y sustantiva del verbo, que '
                             'expresa acción terminada con valor perfectivo, '
                             'se llama:',
                 'alternativas': ['Aspecto neutro',
                                  'Gerundio',
                                  'Infinitivo',
                                  'Participio',
                                  'Modo imperativo'],
                 'correcta': 'D'},
                {'pregunta': 'El participio pasivo regular termina en -ado '
                             'o:',
                 'alternativas': ['-cho', '-jo', '-ido', '-so', '-to'],
                 'correcta': 'C'},
                {'pregunta': 'El participio pasivo irregular puede terminar '
                             'en -cho, -to, -so, -jo o:',
                 'alternativas': ['-ante', '-vo', '-iendo', '-ado', '-ido'],
                 'correcta': 'B'},
                {'pregunta': 'El participio activo, que funciona como '
                             'sustantivo o adjetivo, termina en -ante, '
                             '-iente, -ente, -ador, -edor o:',
                 'alternativas': ['-iendo', '-ando', '-ado', '-ido', '-idor'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'CRITERIOS PARA DEFINIR EL VERBO / VERBOS '
                                'COPULATIVOS Y NO COPULATIVOS',
                      'items': ['Según el criterio semántico, el verbo '
                                'expresa acción, inacción, pasión, estado, '
                                'existencia y transformación.',
                                'Según el criterio morfológico, el verbo es '
                                'una palabra variable con accidentes de '
                                'número, persona, tiempo, modo y aspecto.',
                                'Según el criterio sintáctico, el verbo '
                                'funciona como núcleo del predicado verbal.',
                                'Los verbos copulativos no manifiestan idea '
                                'con sentido pleno y sirven de nexo entre el '
                                'sujeto y su atributo: ser, estar, parecer.',
                                'Los verbos no copulativos, o predicativos, '
                                'expresan por sí solos idea con sentido '
                                'pleno.']},
                     {'titulo': 'CLASES DE VERBOS NO COPULATIVOS / VERBOS '
                                'IMPERSONALES',
                      'items': ['Los verbos transitivos expresan una acción '
                                'que transita del sujeto a un objeto, y '
                                'tienen complemento directo.',
                                'Los verbos intransitivos no tienen '
                                'complemento directo, sino circunstanciales '
                                'o de régimen.',
                                'Los verbos reflexivos tienen una acción que '
                                'se refleja sobre el mismo sujeto; se '
                                'comprueban con el refuerzo «mismo».',
                                'Los verbos impersonales son aquellos cuyo '
                                'sujeto se desconoce o no se precisa con '
                                'exactitud.',
                                'Los verbos que se refieren a fenómenos de '
                                'la naturaleza, como llover o nevar, son '
                                'impersonales.',
                                'Los verbos con el signo de impersonalidad '
                                'pronominal «se», como «se traspasa local», '
                                'también son impersonales.']},
                     {'titulo': 'ACCIDENTES GRAMATICALES: PERSONA, NÚMERO Y '
                                'TIEMPO / ACCIDENTES GRAMATICALES',
                      'items': ['El accidente número expresa la cantidad de '
                                'personas que realizan la acción: singular o '
                                'plural.',
                                'El accidente persona hace referencia a '
                                'quién realiza la acción: primera (yo), '
                                'segunda (tú), tercera (él).',
                                'El accidente tiempo indica la época en que '
                                'se realiza la acción: pasado, presente o '
                                'futuro.',
                                'El aspecto señala si la acción está '
                                'concluida o en proceso: imperfectivo '
                                '(cantaba, no concluida), perfectivo (he '
                                'cantado, concluida) y neutro (cantaré).',
                                'El modo indicativo afirma o niega la acción '
                                'de manera real y objetiva, con seguridad: '
                                '«Manuel escribe poemas».',
                                'El modo subjuntivo expresa la acción de '
                                'manera subjetiva, como deseo o duda: '
                                '«Queremos que Manuel escriba poemas».']},
                     {'titulo': 'VERBOS AUXILIARES / LOS VERBOIDES: '
                                'INFINITIVO Y GERUNDIO',
                      'items': ['Los verbos auxiliares auxilian a los '
                                'verboides en su conjugación: ser, haber y '
                                'estar.',
                                'El auxiliar ser sirve para formar la voz '
                                'pasiva: «Un tema nuevo fue interpretado por '
                                'Leo Dan».',
                                'El auxiliar haber sirve para formar los '
                                'tiempos compuestos: «Lilia ha bailado con '
                                'Fredy».',
                                'Los verboides son formas no personales del '
                                'verbo, porque no están conjugados en '
                                'ninguna persona.',
                                'El infinitivo es la forma sustantiva del '
                                'verbo, cumple función de núcleo del sujeto '
                                'y termina en -ar, -er, -ir.',
                                'El infinitivo simple carece de verbo '
                                'auxiliar: «El amar es maravilloso».']},
                     {'titulo': 'LOS VERBOIDES: EL PARTICIPIO',
                      'items': ['El participio es la forma adjetiva y '
                                'sustantiva del verbo, expresa acción '
                                'terminada (valor perfectivo) y presenta '
                                'flexiones de género y número.',
                                'El participio pasivo regular termina en '
                                '-ado, -ido: niño amado, momento vivido.',
                                'El participio pasivo irregular termina en '
                                '-cho, -to, -so, -jo, -vo: cliente '
                                'satisfecho, documento escrito, libro '
                                'impreso.']}]},
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
                {'titulo': '13.3 LOCUCIONES PREPOSITIVAS',
                 'items': ['Las {locuciones prepositivas} son agrupaciones '
                           'de palabras que adquieren en conjunto el sentido '
                           'y función de una {preposición}.',
                           'El modelo más común es preposición + sustantivo '
                           '+ preposición: a {pesar} de, en torno a, a '
                           'través de, con motivo de.']},
                {'titulo': '13.4 LA CONJUNCIÓN: CRITERIOS',
                 'items': ['Según el criterio {semántico}, la conjunción '
                           'carece de significado lexical; expresa unión, '
                           'oposición o {consecuencia}.',
                           'Según el criterio {morfológico}, la conjunción '
                           'carece de accidentes gramaticales, por lo que es '
                           '{invariable}.',
                           'Según el criterio {sintáctico}, la conjunción '
                           'funciona como nexo {coordinante} y subordinante, '
                           'enlazando elementos.']},
                {'titulo': '13.5 CONJUNCIONES COORDINANTES',
                 'items': ['Las conjunciones {coordinantes} unen elementos '
                           'del mismo nivel jerárquico: copulativas, '
                           '{disyuntivas} y adversativas.',
                           'Las conjunciones {copulativas} (y, e, ni) unen '
                           'dos o más elementos: «Juan y Pedro vinieron»; se '
                           'usa {e} antes de palabra que empieza con i.',
                           'Las conjunciones {disyuntivas} (o, u, o bien) '
                           'tienen valor de alternativa; se usa {u} antes de '
                           'palabra que empieza con o.',
                           'Las conjunciones {adversativas} (pero, sino, '
                           'aunque) señalan enunciados contrapuestos; {pero} '
                           'indica restricción y {sino} expresa '
                           'incompatibilidad.']},
                {'titulo': '13.6 CONJUNCIONES SUBORDINANTES (I)',
                 'items': ['Las conjunciones {subordinantes} enlazan dos '
                           'elementos de distinta jerarquía.',
                           'Las {causales} (porque, como, pues) establecen '
                           'relación causa-efecto: «Estudio {porque} quiero '
                           'aprobar».',
                           'Las {condicionales} (si, siempre que) establecen '
                           'que una proposición es condición de otra: «{Si} '
                           'no estudias, no aprobarás».',
                           'Las {concesivas} (aunque, si bien, a pesar de) '
                           'introducen un inconveniente que no impide la '
                           'acción: «{Aunque} estudie, no aprobaré».']},
                {'titulo': '13.7 CONJUNCIONES SUBORDINANTES (II)',
                 'items': ['Las {comparativas} (como, que) denotan '
                           'comparación: «No es tan listo {como} dicen».',
                           'Las {consecutivas} (tal... que, tan... que) '
                           'muestran la consecuencia de algo cuantificado: '
                           '«Hacía tanto frío {que} no se podía salir».',
                           'Las {finales} (para que, a fin de que) indican '
                           'finalidad o propósito: «Toca el piano {para que} '
                           'vean lo bien que lo haces».',
                           'Las {ilativas} (luego, conque, en consecuencia) '
                           'introducen una oración como consecuencia de la '
                           'anterior: «Pienso, {luego} existo».']}],
  'cuadros': [{'titulo': '13.2 LAS PREPOSICIONES DEL ESPAÑOL',
               'encabezados': ['Grupo', 'Preposiciones'],
               'filas': [['Básicas', 'a, ante, bajo, {con}, contra, de'],
                         ['Medias', 'desde, en, {entre}, hacia, hasta'],
                         ['Finales', '{para}, por, según, sin, sobre, tras'],
                         ['{Arcaicas}', 'so, cabe']]}],
  'preguntas': [{'pregunta': 'Según el criterio semántico, la preposición '
                             'tiene un significado de carácter:',
                 'alternativas': ['Contextual',
                                  'Morfológico puro',
                                  'Fonológico exclusivo',
                                  'Inexistente',
                                  'Fijo y absoluto'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio morfológico, la preposición '
                             'se caracteriza por:',
                 'alternativas': ['No sufrir variaciones formales',
                                  'Concordar en persona',
                                  'Presentar variaciones de género y número',
                                  'Tener flexión verbal',
                                  'Cambiar según el sujeto'],
                 'correcta': 'A'},
                {'pregunta': 'Según el criterio sintáctico, la preposición '
                             'funciona como:',
                 'alternativas': ['Núcleo del predicado',
                                  'Modificador indirecto exclusivo',
                                  'Sujeto de la oración',
                                  'Núcleo del sujeto',
                                  'Conectivo o nexo subordinante'],
                 'correcta': 'E'},
                {'pregunta': 'En «La casa de Patricia fue construida por los '
                             'albañiles», la preposición que encabeza al '
                             'agente es:',
                 'alternativas': ['Con', 'De', 'En', 'Para', 'Por'],
                 'correcta': 'E'},
                {'pregunta': 'Las preposiciones que encabezan al agente en '
                             'voz pasiva son:',
                 'alternativas': ['Con y sin',
                                  'Para y desde',
                                  'Entre y hacia',
                                  'A y ante',
                                  'Por y de'],
                 'correcta': 'E'},
                {'pregunta': 'La preposición «ante» significa:',
                 'alternativas': ['Delante de o en presencia de',
                                  'Junto a',
                                  'Después de',
                                  'Lejos de',
                                  'Debajo de'],
                 'correcta': 'A'},
                {'pregunta': 'La preposición «bajo» puede indicar situación '
                             'inferior o:',
                 'alternativas': ['Subordinación',
                                  'Compañía',
                                  'Finalidad',
                                  'Tiempo exclusivo',
                                  'Origen'],
                 'correcta': 'A'},
                {'pregunta': 'En «Con mucho estudio puedes conseguir la '
                             'beca», la preposición «con» indica:',
                 'alternativas': ['Tiempo',
                                  'Compañía',
                                  'Medio para conseguir algo',
                                  'Contenido',
                                  'Oposición'],
                 'correcta': 'C'},
                {'pregunta': 'La preposición «contra» indica principalmente:',
                 'alternativas': ['Posesión',
                                  'Compañía',
                                  'Finalidad',
                                  'Oposición o ubicación',
                                  'Procedencia'],
                 'correcta': 'D'},
                {'pregunta': 'En «El departamento de mi amiga», la '
                             'preposición «de» indica:',
                 'alternativas': ['Tiempo',
                                  'Material',
                                  'Tema',
                                  'Posesión o pertenencia',
                                  'Origen'],
                 'correcta': 'D'},
                {'pregunta': 'En «Yo soy de Apurímac», la preposición «de» '
                             'indica:',
                 'alternativas': ['Tema o asunto',
                                  'Tiempo',
                                  'Posesión',
                                  'Material',
                                  'Origen o procedencia'],
                 'correcta': 'E'},
                {'pregunta': 'La preposición «desde» indica principio de '
                             'tiempo o de:',
                 'alternativas': ['Modo',
                                  'Compañía',
                                  'Oposición',
                                  'Finalidad',
                                  'Lugar'],
                 'correcta': 'E'},
                {'pregunta': 'La preposición «hacia» indica dirección o:',
                 'alternativas': ['Compañía',
                                  'Una tendencia',
                                  'Material',
                                  'Oposición',
                                  'Posesión'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «hasta» puede indicar término '
                             'de lugar, acción o:',
                 'alternativas': ['Oposición',
                                  'Material',
                                  'Tiempo',
                                  'Compañía',
                                  'Posesión'],
                 'correcta': 'C'},
                {'pregunta': 'La preposición «para» puede indicar finalidad, '
                             'tiempo o:',
                 'alternativas': ['Oposición',
                                  'Dirección',
                                  'Posesión exclusiva',
                                  'Compañía',
                                  'Material'],
                 'correcta': 'B'},
                {'pregunta': 'En el sujeto, la preposición encabeza al:',
                 'alternativas': ['Vocativo',
                                  'Núcleo del sujeto',
                                  'Modificador indirecto',
                                  'Predicado nominal',
                                  'Complemento directo'],
                 'correcta': 'C'},
                {'pregunta': '«So» y «cabe» son ejemplos de preposiciones:',
                 'alternativas': ['Modernas de uso frecuente',
                                  'Extranjeras',
                                  'Arcaicas',
                                  'Neológicas',
                                  'Compuestas'],
                 'correcta': 'C'},
                {'pregunta': 'En «Estamos pasando bajo el puente», la '
                             'preposición «bajo» indica:',
                 'alternativas': ['Subordinación',
                                  'Compañía',
                                  'Situación inferior',
                                  'Finalidad',
                                  'Tiempo'],
                 'correcta': 'C'},
                {'pregunta': 'En «Dame un té con leche», la preposición '
                             '«con» indica:',
                 'alternativas': ['Contenido o unión de cosas',
                                  'Medio',
                                  'Tiempo',
                                  'Oposición',
                                  'Compañía de personas'],
                 'correcta': 'A'},
                {'pregunta': 'En «Este informe es para mi jefe», la '
                             'preposición «para» indica:',
                 'alternativas': ['Origen',
                                  'Finalidad',
                                  'Compañía',
                                  'Dirección',
                                  'Tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'Las agrupaciones de palabras que adquieren en '
                             'conjunto el sentido y función de una '
                             'preposición se llaman:',
                 'alternativas': ['Conectores lógicos',
                                  'Frases nominales',
                                  'Locuciones conjuntivas',
                                  'Locuciones adverbiales',
                                  'Locuciones prepositivas'],
                 'correcta': 'E'},
                {'pregunta': 'Según el criterio semántico, la conjunción se '
                             'caracteriza por:',
                 'alternativas': ['Indicar posesión',
                                  'Carecer de significado lexical',
                                  'Ser siempre variable',
                                  'Tener significado lexical propio',
                                  'Funcionar como sustantivo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, la conjunción '
                             'es una palabra:',
                 'alternativas': ['Con género gramatical',
                                  'Invariable',
                                  'Con flexión verbal',
                                  'Variable en género y número',
                                  'Con grados de comparación'],
                 'correcta': 'B'},
                {'pregunta': 'Las conjunciones que unen elementos del mismo '
                             'nivel jerárquico se llaman conjunciones:',
                 'alternativas': ['Coordinantes',
                                  'Subordinantes',
                                  'Enfáticas',
                                  'Interrogativas',
                                  'Correlativas'],
                 'correcta': 'A'},
                {'pregunta': 'Las conjunciones y, e, ni, que unen dos o más '
                             'elementos, se llaman conjunciones:',
                 'alternativas': ['Disyuntivas',
                                  'Adversativas',
                                  'Consecutivas',
                                  'Causales',
                                  'Copulativas'],
                 'correcta': 'E'},
                {'pregunta': 'La conjunción copulativa «y» se escribe «e» '
                             'cuando la siguiente palabra empieza con:',
                 'alternativas': ['La vocal i',
                                  'La letra u',
                                  'La letra o',
                                  'La letra a',
                                  'Cualquier consonante'],
                 'correcta': 'A'},
                {'pregunta': 'Las conjunciones o, u, o bien, que tienen '
                             'valor de alternativa, se llaman conjunciones:',
                 'alternativas': ['Finales',
                                  'Disyuntivas',
                                  'Concesivas',
                                  'Adversativas',
                                  'Copulativas'],
                 'correcta': 'B'},
                {'pregunta': 'Las conjunciones pero, sino, aunque, que '
                             'señalan enunciados contrapuestos, se llaman '
                             'conjunciones:',
                 'alternativas': ['Causales',
                                  'Comparativas',
                                  'Disyuntivas',
                                  'Copulativas',
                                  'Adversativas'],
                 'correcta': 'E'},
                {'pregunta': 'Las conjunciones porque, como, pues, que '
                             'establecen una relación de causa-efecto, se '
                             'llaman conjunciones:',
                 'alternativas': ['Condicionales',
                                  'Consecutivas',
                                  'Finales',
                                  'Concesivas',
                                  'Causales'],
                 'correcta': 'E'},
                {'pregunta': 'Las conjunciones si, siempre que, siempre y '
                             'cuando, que establecen que una proposición es '
                             'condición de otra, se llaman conjunciones:',
                 'alternativas': ['Condicionales',
                                  'Causales',
                                  'Concesivas',
                                  'Comparativas',
                                  'Ilativas'],
                 'correcta': 'A'},
                {'pregunta': 'Las conjunciones aunque, si bien, a pesar de, '
                             'que introducen un inconveniente que no impide '
                             'la acción, se llaman conjunciones:',
                 'alternativas': ['Causales',
                                  'Concesivas',
                                  'Condicionales',
                                  'Consecutivas',
                                  'Finales'],
                 'correcta': 'B'},
                {'pregunta': 'Las conjunciones que denotan comparación entre '
                             'dos o más frases, como «como» o «que», se '
                             'llaman conjunciones:',
                 'alternativas': ['Comparativas',
                                  'Consecutivas',
                                  'Finales',
                                  'Ilativas',
                                  'Concesivas'],
                 'correcta': 'A'},
                {'pregunta': 'Las conjunciones que introducen una '
                             'proposición mostrando la consecuencia de algo '
                             'cuantificado, como «tan... que», se llaman '
                             'conjunciones:',
                 'alternativas': ['Ilativas',
                                  'Finales',
                                  'Causales',
                                  'Comparativas',
                                  'Consecutivas'],
                 'correcta': 'E'},
                {'pregunta': 'Las conjunciones para que, a fin de que, que '
                             'indican finalidad o propósito, se llaman '
                             'conjunciones:',
                 'alternativas': ['Comparativas',
                                  'Consecutivas',
                                  'Causales',
                                  'Finales',
                                  'Concesivas'],
                 'correcta': 'D'},
                {'pregunta': 'Las conjunciones luego, conque, en '
                             'consecuencia, que introducen una oración como '
                             'consecuencia de la anterior, se llaman '
                             'conjunciones:',
                 'alternativas': ['Comparativas',
                                  'Ilativas',
                                  'Causales',
                                  'Concesivas',
                                  'Finales'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CRITERIOS DE LA PREPOSICIÓN',
                      'items': ['Según el criterio semántico, la preposición '
                                'no tiene significación por sí sola: su '
                                'sentido es de carácter contextual.',
                                'Según el criterio morfológico, la '
                                'preposición no sufre variaciones formales; '
                                'carece de morfemas.',
                                'Según el criterio sintáctico, la '
                                'preposición funciona como conectivo o nexo '
                                'subordinante.']},
                     {'titulo': 'USOS DE ALGUNAS PREPOSICIONES',
                      'items': ['La preposición «a» puede indicar dirección, '
                                'lugar, tiempo o modo.',
                                'La preposición «ante» significa «delante» o '
                                '«en presencia de».',
                                'La preposición «bajo» puede indicar '
                                'situación inferior o subordinación.']},
                     {'titulo': 'LOCUCIONES PREPOSITIVAS',
                      'items': ['Las locuciones prepositivas son '
                                'agrupaciones de palabras que adquieren en '
                                'conjunto el sentido y función de una '
                                'preposición.',
                                'El modelo más común es preposición + '
                                'sustantivo + preposición: a pesar de, en '
                                'torno a, a través de, con motivo de.']},
                     {'titulo': 'LA CONJUNCIÓN: CRITERIOS',
                      'items': ['Según el criterio semántico, la conjunción '
                                'carece de significado lexical; expresa '
                                'unión, oposición o consecuencia.',
                                'Según el criterio morfológico, la '
                                'conjunción carece de accidentes '
                                'gramaticales, por lo que es invariable.',
                                'Según el criterio sintáctico, la conjunción '
                                'funciona como nexo coordinante y '
                                'subordinante, enlazando elementos.']},
                     {'titulo': 'CONJUNCIONES COORDINANTES',
                      'items': ['Las conjunciones coordinantes unen '
                                'elementos del mismo nivel jerárquico: '
                                'copulativas, disyuntivas y adversativas.',
                                'Las conjunciones copulativas (y, e, ni) '
                                'unen dos o más elementos: «Juan y Pedro '
                                'vinieron»; se usa e antes de palabra que '
                                'empieza con i.',
                                'Las conjunciones disyuntivas (o, u, o bien) '
                                'tienen valor de alternativa; se usa u antes '
                                'de palabra que empieza con o.']},
                     {'titulo': 'CONJUNCIONES SUBORDINANTES (I)',
                      'items': ['Las conjunciones subordinantes enlazan dos '
                                'elementos de distinta jerarquía.',
                                'Las causales (porque, como, pues) '
                                'establecen relación causa-efecto: «Estudio '
                                'porque quiero aprobar».',
                                'Las condicionales (si, siempre que) '
                                'establecen que una proposición es condición '
                                'de otra: «Si no estudias, no aprobarás».']},
                     {'titulo': 'CONJUNCIONES SUBORDINANTES (II)',
                      'items': ['Las comparativas (como, que) denotan '
                                'comparación: «No es tan listo como dicen».',
                                'Las consecutivas (tal... que, tan... que) '
                                'muestran la consecuencia de algo '
                                'cuantificado: «Hacía tanto frío que no se '
                                'podía salir».',
                                'Las finales (para que, a fin de que) '
                                'indican finalidad o propósito: «Toca el '
                                'piano para que vean lo bien que lo '
                                'haces».']}]},
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
                {'titulo': '14.4 EL SINTAGMA VERBAL Y SU NÚCLEO',
                 'items': ['El {sintagma verbal} (SV), o predicado, tiene '
                           'como núcleo a un {verbo} que concuerda con el '
                           'núcleo del sujeto.',
                           'El {núcleo} del SV es el verbo que subordina a '
                           'las demás palabras del predicado.']},
                {'titulo': '14.5 COMPLEMENTOS MONOVALENTES DEL VERBO',
                 'items': ['El {complemento directo} (CD) es el ser sobre el '
                           'que recae la acción verbal; puede sustituirse '
                           'por lo, la, los, {las}: «El joven compró libros» '
                           '→ «El joven los compró».',
                           'El {complemento indirecto} (CI) es el ser que se '
                           'beneficia o perjudica con la acción; se encabeza '
                           'con «{a}» o «para»: «El docente le compró '
                           'libros».',
                           'El {complemento circunstancial} (CC) complementa '
                           'el verbo con matices de lugar, {tiempo}, modo, '
                           'causa, compañía o finalidad.',
                           'El {complemento agente} (CAg) se encabeza con la '
                           'preposición «{por}»; aparece en oraciones en voz '
                           'pasiva: «Los muros fueron intervenidos por un '
                           'equipo».',
                           'El {complemento de régimen} (C.REG) viene '
                           'introducido por una preposición exigida por el '
                           'propio {verbo}: «Se apoderó de la ciudad».']},
                {'titulo': '14.6 COMPLEMENTOS BIVALENTES: PREDICATIVO Y '
                           'ATRIBUTO',
                 'items': ['El {predicativo} (PVO) complementa a un verbo '
                           '{no copulativo}, expresando cualidad o estado '
                           'del sujeto o del CD: «El niño se despertó '
                           '{atemorizado}».',
                           'El {atributo} complementa a un verbo '
                           '{copulativo} o semicopulativo: «El mes de '
                           'febrero es {lluvioso}».',
                           'El atributo es sustituible por el pronombre '
                           'invariable «{lo}»; el predicativo no lo es.',
                           'El {predicado nominal} tiene como núcleo un '
                           'sustantivo, adjetivo o adverbio; el predicado '
                           '{verbal} tiene como núcleo un verbo conjugado.']},
                {'titulo': '14.7 CONCEPTO Y CARACTERÍSTICAS DE LA ORACIÓN',
                 'items': ['La {oración} es la unidad de predicación que '
                           'pone en relación un sujeto con un predicado '
                           'verbal; expresa un {juicio} completo.',
                           'La oración posee sentido {completo}, autonomía '
                           'sintáctica, entonación propia, y generalmente '
                           'está dotada de verbo {conjugado}.']},
                {'titulo': '14.8 ORACIONES UNIMEMBRES Y BIMEMBRES',
                 'items': ['Las oraciones {unimembres} no poseen sujeto ni '
                           'predicado, pero tienen sentido {completo}.',
                           'Las unimembres {sin verbo} o contextuales '
                           'adquieren valor oracional en un contexto: '
                           '«¡{Hola}!», «Buenos días».',
                           'Las unimembres con verbos {impersonales} carecen '
                           'de sujeto: «{Amaneció} nublado», «Hay muchos '
                           'alumnos».',
                           'Las oraciones {bimembres} poseen sujeto y '
                           'predicado, expreso o {tácito}.']},
                {'titulo': '14.9 ORACIONES SIMPLES Y COMPUESTAS',
                 'items': ['Las oraciones {simples} presentan un solo verbo '
                           '{principal} o conjugado, sin proposiciones.',
                           'Las oraciones {compuestas} constan de dos o más '
                           '{verbos} o proposiciones.']},
                {'titulo': '14.10 ORACIONES SEGÚN LA ACTITUD DEL HABLANTE '
                           '(I)',
                 'items': ['Las oraciones {enunciativas} o declarativas '
                           'afirman o niegan hechos de forma {objetiva}: '
                           '«Hoy hace frío».',
                           'Las oraciones {desiderativas} manifiestan un '
                           'deseo: «{Ojalá} lleguen pronto».',
                           'Las oraciones {dubitativas} expresan duda o '
                           'probabilidad: «{Tal vez} tengas razón».']},
                {'titulo': '14.11 ORACIONES SEGÚN LA ACTITUD DEL HABLANTE '
                           '(II)',
                 'items': ['Las oraciones {interrogativas} expresan una '
                           'pregunta, directa o {indirecta}: «¿Cuál es tu '
                           'nombre?»',
                           'Las oraciones {imperativas} o exhortativas '
                           'presentan un mandato u orden, con modo '
                           '{imperativo}: «Abre la ventana».',
                           'Las oraciones {exclamativas} expresan emociones, '
                           'con signos de {exclamación}: «¡Qué susto '
                           'pasamos!»']}],
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
                                  'Escritura',
                                  'Sonido'],
                 'correcta': 'B'},
                {'pregunta': 'La sintaxis, como disciplina lingüística, '
                             'estudia las relaciones entre los elementos de '
                             'una frase y:',
                 'alternativas': ['Solo su ortografía',
                                  'Solo su significado aislado',
                                  'Solo su pronunciación',
                                  'Las funciones que desempeña cada palabra',
                                  'Solo su origen etimológico'],
                 'correcta': 'D'},
                {'pregunta': 'La unidad básica de la sintaxis es:',
                 'alternativas': ['La sílaba',
                                  'El morfema',
                                  'El grafema',
                                  'El fonema',
                                  'El sintagma'],
                 'correcta': 'E'},
                {'pregunta': 'El sintagma se define como una unidad formada '
                             'por palabras dotadas de sentido y valor:',
                 'alternativas': ['Semántico aislado',
                                  'Morfológico exclusivo',
                                  'Fonológico',
                                  'Funcional',
                                  'Ortográfico'],
                 'correcta': 'D'},
                {'pregunta': 'El sintagma nominal también se conoce como:',
                 'alternativas': ['Vocativo',
                                  'Complemento circunstancial',
                                  'Frase nominal o grupo nominal',
                                  'Predicado nominal exclusivo',
                                  'Sintagma verbal'],
                 'correcta': 'C'},
                {'pregunta': 'El núcleo del sintagma nominal siempre es:',
                 'alternativas': ['Un adverbio',
                                  'Una conjunción',
                                  'Una preposición',
                                  'Un sustantivo o palabra sustantivada',
                                  'Un verbo'],
                 'correcta': 'D'},
                {'pregunta': 'Los modificadores del sintagma nominal '
                             'dependen de:',
                 'alternativas': ['El núcleo',
                                  'El complemento circunstancial',
                                  'El verbo principal',
                                  'El sujeto de otra oración',
                                  'El predicado verbal'],
                 'correcta': 'A'},
                {'pregunta': 'El modificador que se une al núcleo del SN sin '
                             'ningún enlace se llama:',
                 'alternativas': ['Modificador indirecto',
                                  'Aposición especificativa',
                                  'Aposición explicativa',
                                  'Modificador directo',
                                  'Complemento agente'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras que funcionan típicamente como '
                             'modificador directo son:',
                 'alternativas': ['Los adverbios',
                                  'Las conjunciones',
                                  'Los artículos y adjetivos',
                                  'Las preposiciones',
                                  'Los verbos'],
                 'correcta': 'C'},
                {'pregunta': 'El modificador que se une al núcleo mediante '
                             'preposiciones se llama:',
                 'alternativas': ['Modificador indirecto',
                                  'Vocativo',
                                  'Aposición',
                                  'Núcleo secundario',
                                  'Modificador directo'],
                 'correcta': 'A'},
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
                 'alternativas': ['Especificativa',
                                  'Indirecta',
                                  'Explicativa',
                                  'Directa',
                                  'Neutra'],
                 'correcta': 'C'},
                {'pregunta': 'En «Pachacútec, el constructor de Machu '
                             'Picchu, fue el noveno Inca», el segmento entre '
                             'comas es una aposición:',
                 'alternativas': ['Explicativa',
                                  'Neutra',
                                  'Indirecta',
                                  'Especificativa',
                                  'Directa'],
                 'correcta': 'A'},
                {'pregunta': 'La aposición que singulariza al nombre y no va '
                             'entre comas se llama aposición:',
                 'alternativas': ['Indirecta',
                                  'Neutra',
                                  'Explicativa',
                                  'Directa',
                                  'Especificativa'],
                 'correcta': 'E'},
                {'pregunta': 'En «El río Vilcanota recorre el Valle '
                             'Sagrado», «Vilcanota» funciona como una '
                             'aposición:',
                 'alternativas': ['Neutra',
                                  'Explicativa',
                                  'Directa',
                                  'Indirecta',
                                  'Especificativa'],
                 'correcta': 'E'},
                {'pregunta': 'En «El estudiante proactivo logró su '
                             'propósito», «proactivo» funciona como:',
                 'alternativas': ['Vocativo',
                                  'Modificador indirecto',
                                  'Núcleo del SN',
                                  'Modificador directo',
                                  'Aposición'],
                 'correcta': 'D'},
                {'pregunta': 'En «Los estudiantes con empeño logran todo», '
                             '«con empeño» funciona como:',
                 'alternativas': ['Modificador indirecto',
                                  'Aposición explicativa',
                                  'Núcleo',
                                  'Modificador directo',
                                  'Vocativo'],
                 'correcta': 'A'},
                {'pregunta': 'En «Cusco, capital histórica del Perú, es una '
                             'ciudad milenaria», «capital histórica del '
                             'Perú» es una aposición:',
                 'alternativas': ['Explicativa',
                                  'Indirecta',
                                  'Especificativa',
                                  'Neutra',
                                  'Directa'],
                 'correcta': 'A'},
                {'pregunta': 'Ortográficamente, la aposición explicativa '
                             'siempre aparece:',
                 'alternativas': ['Subrayada',
                                  'En mayúscula total',
                                  'Entre paréntesis obligatorios',
                                  'Sin ninguna puntuación',
                                  'Separada entre comas'],
                 'correcta': 'E'},
                {'pregunta': 'Semánticamente, los elementos de una aposición '
                             'explicativa son:',
                 'alternativas': ['Sinónimos',
                                  'Sin relación semántica',
                                  'Parónimos',
                                  'Homófonos',
                                  'Antónimos'],
                 'correcta': 'A'},
                {'pregunta': 'El núcleo del sintagma verbal es el verbo, que '
                             'subordina a las demás palabras del:',
                 'alternativas': ['Sujeto',
                                  'Vocativo',
                                  'Sintagma nominal',
                                  'Complemento agente',
                                  'Predicado'],
                 'correcta': 'E'},
                {'pregunta': 'El complemento sobre el que recae directamente '
                             'la acción verbal, sustituible por '
                             'lo/la/los/las, se llama:',
                 'alternativas': ['Complemento directo',
                                  'Complemento circunstancial',
                                  'Complemento de régimen',
                                  'Complemento indirecto',
                                  'Complemento agente'],
                 'correcta': 'A'},
                {'pregunta': 'El complemento que indica el ser que se '
                             'beneficia o perjudica con la acción verbal, '
                             'encabezado por «a» o «para», se llama:',
                 'alternativas': ['Complemento directo',
                                  'Predicativo',
                                  'Complemento indirecto',
                                  'Complemento circunstancial',
                                  'Atributo'],
                 'correcta': 'C'},
                {'pregunta': 'El complemento que se encabeza con la '
                             'preposición «por» y aparece en oraciones en '
                             'voz pasiva se llama complemento:',
                 'alternativas': ['Directo',
                                  'Indirecto',
                                  'Circunstancial',
                                  'Agente',
                                  'De régimen'],
                 'correcta': 'D'},
                {'pregunta': 'El complemento que complementa a un verbo no '
                             'copulativo, expresando cualidad o estado del '
                             'sujeto o del CD, se llama:',
                 'alternativas': ['Atributo',
                                  'Complemento directo',
                                  'Predicativo',
                                  'Complemento de régimen',
                                  'Complemento agente'],
                 'correcta': 'C'},
                {'pregunta': 'El complemento que acompaña a un verbo '
                             'copulativo o semicopulativo, sustituible por '
                             'el pronombre «lo», se llama:',
                 'alternativas': ['Predicativo',
                                  'Atributo',
                                  'Complemento de régimen',
                                  'Complemento circunstancial',
                                  'Complemento agente'],
                 'correcta': 'B'},
                {'pregunta': 'El predicado cuyo núcleo es un sustantivo, '
                             'adjetivo o adverbio, sin verbo conjugado, se '
                             'llama predicado:',
                 'alternativas': ['Nominal',
                                  'Verbal',
                                  'Simple',
                                  'Bimembre',
                                  'Compuesto'],
                 'correcta': 'A'},
                {'pregunta': 'La oración, definida como la unidad de '
                             'predicación, pone en relación un sujeto con '
                             'un:',
                 'alternativas': ['Complemento',
                                  'Adjunto',
                                  'Predicado verbal',
                                  'Vocativo',
                                  'Núcleo nominal'],
                 'correcta': 'C'},
                {'pregunta': 'Las oraciones que no poseen sujeto ni '
                             'predicado, pero sí tienen sentido completo, se '
                             'llaman oraciones:',
                 'alternativas': ['Subordinadas',
                                  'Unimembres',
                                  'Compuestas',
                                  'Coordinadas',
                                  'Bimembres'],
                 'correcta': 'B'},
                {'pregunta': 'Las oraciones unimembres que carecen de sujeto '
                             'por tener verbos impersonales, como «Amaneció '
                             'nublado», corresponden al tipo:',
                 'alternativas': ['Con verbos impersonales',
                                  'Coordinadas',
                                  'Sin verbo o contextuales',
                                  'Compuestas',
                                  'Bimembres con sujeto tácito'],
                 'correcta': 'A'},
                {'pregunta': 'Las oraciones que poseen sujeto y predicado, '
                             'expreso o tácito, se llaman oraciones:',
                 'alternativas': ['Unimembres',
                                  'Nominales exclusivas',
                                  'Contextuales',
                                  'Impersonales',
                                  'Bimembres'],
                 'correcta': 'E'},
                {'pregunta': 'Las oraciones que presentan un solo verbo '
                             'principal o conjugado, sin proposiciones, se '
                             'llaman oraciones:',
                 'alternativas': ['Unimembres',
                                  'Simples',
                                  'Compuestas',
                                  'Bimembres exclusivas',
                                  'Contextuales'],
                 'correcta': 'B'},
                {'pregunta': 'Las oraciones que constan de dos o más verbos '
                             'o proposiciones se llaman oraciones:',
                 'alternativas': ['Contextuales',
                                  'Simples',
                                  'Impersonales',
                                  'Compuestas',
                                  'Unimembres'],
                 'correcta': 'D'},
                {'pregunta': 'Las oraciones que afirman o niegan hechos de '
                             'manera objetiva, para transmitir información, '
                             'se llaman oraciones:',
                 'alternativas': ['Exclamativas',
                                  'Dubitativas',
                                  'Enunciativas o declarativas',
                                  'Desiderativas',
                                  'Interrogativas'],
                 'correcta': 'C'},
                {'pregunta': 'Las oraciones en las que el hablante '
                             'manifiesta un deseo, como «Ojalá lleguen '
                             'pronto», se llaman oraciones:',
                 'alternativas': ['Dubitativas',
                                  'Imperativas',
                                  'Desiderativas',
                                  'Interrogativas',
                                  'Enunciativas'],
                 'correcta': 'C'},
                {'pregunta': 'Las oraciones en las que el hablante expresa '
                             'duda o probabilidad, como «Tal vez tengas '
                             'razón», se llaman oraciones:',
                 'alternativas': ['Exhortativas',
                                  'Desiderativas',
                                  'Enunciativas',
                                  'Dubitativas',
                                  'Exclamativas'],
                 'correcta': 'D'},
                {'pregunta': 'Las oraciones que presentan lo que se dice '
                             'como un mandato, orden o ruego, generalmente '
                             'en modo imperativo, se llaman oraciones:',
                 'alternativas': ['Desiderativas',
                                  'Imperativas o exhortativas',
                                  'Dubitativas',
                                  'Interrogativas',
                                  'Enunciativas'],
                 'correcta': 'B'},
                {'pregunta': 'Las oraciones en las que el hablante expresa '
                             'emociones, con signos de exclamación, se '
                             'llaman oraciones:',
                 'alternativas': ['Desiderativas',
                                  'Imperativas',
                                  'Enunciativas',
                                  'Exclamativas',
                                  'Dubitativas'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DE SINTAXIS Y SINTAGMA / EL '
                                'SINTAGMA NOMINAL',
                      'items': ['«Sintaxis» es un término de origen griego '
                                'que significa «orden o disposición».',
                                'La sintaxis estudia las relaciones entre '
                                'los elementos de una frase y las funciones '
                                'que desempeña cada palabra.',
                                'El sintagma nominal (SN), o frase nominal, '
                                'está formado por un sustantivo u otra '
                                'categoría sustantivada que constituye su '
                                'núcleo.',
                                'El núcleo del sintagma nominal siempre es '
                                'un sustantivo o palabra sustantivada.']},
                     {'titulo': 'MODIFICADORES DEL SINTAGMA NOMINAL / EL '
                                'SINTAGMA VERBAL Y SU NÚCLEO',
                      'items': ['El modificador directo (MD) se une al '
                                'núcleo sin enlace; son artículos y '
                                'adjetivos.',
                                'El modificador indirecto (MI) se une al '
                                'núcleo mediante preposiciones o '
                                'conjunciones comparativas.',
                                'El sintagma verbal (SV), o predicado, tiene '
                                'como núcleo a un verbo que concuerda con el '
                                'núcleo del sujeto.',
                                'El núcleo del SV es el verbo que subordina '
                                'a las demás palabras del predicado.']},
                     {'titulo': 'COMPLEMENTOS MONOVALENTES DEL VERBO / '
                                'COMPLEMENTOS BIVALENTES: PREDICATIVO ',
                      'items': ['El complemento directo (CD) es el ser sobre '
                                'el que recae la acción verbal; puede '
                                'sustituirse por lo, la, los, las: «El joven '
                                'compró libros» → «El joven los compró».',
                                'El complemento indirecto (CI) es el ser que '
                                'se beneficia o perjudica con la acción; se '
                                'encabeza con «a» o «para»: «El docente le '
                                'compró libros».',
                                'El predicativo (PVO) complementa a un verbo '
                                'no copulativo, expresando cualidad o estado '
                                'del sujeto o del CD: «El niño se despertó '
                                'atemorizado».',
                                'El atributo complementa a un verbo '
                                'copulativo o semicopulativo: «El mes de '
                                'febrero es lluvioso».']},
                     {'titulo': 'CONCEPTO Y CARACTERÍSTICAS DE LA ORACIÓN / '
                                'ORACIONES UNIMEMBRES Y BIMEMBRES',
                      'items': ['La oración es la unidad de predicación que '
                                'pone en relación un sujeto con un predicado '
                                'verbal; expresa un juicio completo.',
                                'La oración posee sentido completo, '
                                'autonomía sintáctica, entonación propia, y '
                                'generalmente está dotada de verbo '
                                'conjugado.',
                                'Las oraciones unimembres no poseen sujeto '
                                'ni predicado, pero tienen sentido completo.',
                                'Las unimembres sin verbo o contextuales '
                                'adquieren valor oracional en un contexto: '
                                '«¡Hola!», «Buenos días».']},
                     {'titulo': 'ORACIONES SIMPLES Y COMPUESTAS / ORACIONES '
                                'SEGÚN LA ACTITUD DEL HABLANTE (I',
                      'items': ['Las oraciones simples presentan un solo '
                                'verbo principal o conjugado, sin '
                                'proposiciones.',
                                'Las oraciones compuestas constan de dos o '
                                'más verbos o proposiciones.',
                                'Las oraciones enunciativas o declarativas '
                                'afirman o niegan hechos de forma objetiva: '
                                '«Hoy hace frío».',
                                'Las oraciones desiderativas manifiestan un '
                                'deseo: «Ojalá lleguen pronto».']},
                     {'titulo': 'ORACIONES SEGÚN LA ACTITUD DEL HABLANTE '
                                '(II)',
                      'items': ['Las oraciones interrogativas expresan una '
                                'pregunta, directa o indirecta: «¿Cuál es tu '
                                'nombre?»',
                                'Las oraciones imperativas o exhortativas '
                                'presentan un mandato u orden, con modo '
                                'imperativo: «Abre la ventana».']}]},
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
                {'titulo': '15.4 CLASES DE TEXTO POR SU CONTENIDO',
                 'items': ['El texto {informativo} contiene noticias de '
                           'carácter real; su uso es propio del contexto '
                           '{periodístico}.',
                           'El texto {científico} contiene resultados de una '
                           'investigación, expuestos en monografías, tesis o '
                           '{artículos} científicos.',
                           'El texto {filosófico} contiene reflexiones sobre '
                           'las causas y fines primeros de la {existencia} '
                           'humana.',
                           'El texto {humanístico} contiene ideas sobre la '
                           'actividad humana, sin el rigor de la ciencia ni '
                           'la profundidad {filosófica}.',
                           'El texto {literario} constituye obras donde '
                           'prima la {belleza} del lenguaje: novelas, '
                           'cuentos, poemas.']},
                {'titulo': '15.5 CLASES DE TEXTO POR SU ESTRUCTURA',
                 'items': ['El texto {analizante} presenta la idea principal '
                           'al {inicio} del párrafo, explicada luego por las '
                           'ideas secundarias.',
                           'El texto {sintetizante} presenta la idea '
                           'principal al {final} del párrafo, como síntesis '
                           'de lo anterior.',
                           'El texto {centrado} presenta la idea principal '
                           'al {medio} del párrafo.',
                           'El texto {encuadrado} presenta la idea principal '
                           'al inicio y al {final} del párrafo.',
                           'El texto {paralelo} no presenta idea principal '
                           'ni secundarias; todas las ideas tienen {igual} '
                           'importancia.']},
                {'titulo': '15.6 CONCEPTO DE LECTURA Y NIVEL LITERAL',
                 'items': ['La {lectura} es la actividad mental de '
                           'percepción, comprensión y reacción que permite '
                           'informarse del contenido de un {texto}.',
                           'El nivel {literal}, textual o lineal, se somete '
                           'estrictamente a los contenidos {explícitos} del '
                           'texto, sin entrar en interpretación.']},
                {'titulo': '15.7 NIVEL INFERENCIAL',
                 'items': ['El nivel {inferencial}, deductivo o extralineal, '
                           'busca relaciones que van más allá de lo '
                           '{establecido} en el texto.',
                           'El nivel inferencial incluye: inferir {ideas} '
                           'principales no explícitas, inferir relaciones de '
                           '{causa} y efecto, y predecir acontecimientos.',
                           'La meta del nivel inferencial es la elaboración '
                           'de {conclusiones}.']},
                {'titulo': '15.8 NIVEL CRÍTICO',
                 'items': ['El nivel {crítico} emite juicios sobre el texto '
                           'leído, aceptándolo o rechazándolo con '
                           '{fundamentos}.',
                           'Los juicios del nivel crítico pueden ser de '
                           '{realidad} o fantasía, de adecuación y validez, '
                           'de apropiación, o de rechazo o {aceptación}.']}],
  'cuadros': [{'titulo': '15.3 CLASES DE TEXTO POR SU FORMA',
               'encabezados': ['Clase', 'Finalidad'],
               'filas': [['{Narrativo}', '{Contar} acontecimientos'],
                         ['{Descriptivo}', '{Representar} con palabras'],
                         ['{Argumentativo}', '{Persuadir} al lector']]}],
  'preguntas': [{'pregunta': 'El término «texto» proviene del latín '
                             '«textus», que significa:',
                 'alternativas': ['Idea',
                                  'Discurso',
                                  'Palabra',
                                  'Tejido',
                                  'Escrito'],
                 'correcta': 'D'},
                {'pregunta': 'El texto se define como una unidad de '
                             'contenido y forma que tiene como base:',
                 'alternativas': ['El morfema',
                                  'La oración simple',
                                  'El párrafo',
                                  'La sílaba',
                                  'El fonema'],
                 'correcta': 'C'},
                {'pregunta': 'El texto tiene un carácter comunicativo, un '
                             'carácter pragmático y un carácter:',
                 'alternativas': ['Improvisado',
                                  'Estructurado',
                                  'Fonológico exclusivo',
                                  'Aleatorio',
                                  'Musical'],
                 'correcta': 'B'},
                {'pregunta': 'El texto se define como la secuencia '
                             'lingüística con sentido:',
                 'alternativas': ['Nulo',
                                  'Pleno',
                                  'Exclusivamente literal',
                                  'Ambiguo',
                                  'Fragmentado'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis o planteamiento central que el autor '
                             'desarrolla en un texto se llama:',
                 'alternativas': ['Título',
                                  'Subtítulo',
                                  'Idea secundaria',
                                  'Tema general',
                                  'Idea principal'],
                 'correcta': 'E'},
                {'pregunta': 'Las ideas que sirven de argumento a la idea '
                             'principal se llaman:',
                 'alternativas': ['Temas',
                                  'Ideas secundarias',
                                  'Conclusiones exclusivas',
                                  'Ideas principales',
                                  'Títulos'],
                 'correcta': 'B'},
                {'pregunta': 'Todo aquello de lo que se habla en un texto, '
                             'el asunto general, se llama:',
                 'alternativas': ['Tema',
                                  'Argumento',
                                  'Idea principal',
                                  'Idea secundaria',
                                  'Título'],
                 'correcta': 'A'},
                {'pregunta': 'La frase breve que sintetiza la idea central '
                             'de un texto se llama:',
                 'alternativas': ['Tema',
                                  'Párrafo',
                                  'Título',
                                  'Argumento',
                                  'Idea secundaria'],
                 'correcta': 'C'},
                {'pregunta': 'El texto que presenta una sucesión de acciones '
                             'en el tiempo se llama texto:',
                 'alternativas': ['Descriptivo',
                                  'Instructivo',
                                  'Expositivo puro',
                                  'Narrativo',
                                  'Argumentativo'],
                 'correcta': 'D'},
                {'pregunta': 'La finalidad del texto narrativo es:',
                 'alternativas': ['Describir un objeto',
                                  'Dar instrucciones',
                                  'Definir conceptos',
                                  'Contar acontecimientos reales o ficticios',
                                  'Persuadir al lector'],
                 'correcta': 'D'},
                {'pregunta': 'El texto que representa con palabras un '
                             'objeto, paisaje o persona se llama texto:',
                 'alternativas': ['Argumentativo',
                                  'Descriptivo',
                                  'Narrativo',
                                  'Dialógico',
                                  'Expositivo'],
                 'correcta': 'B'},
                {'pregunta': 'El texto descriptivo es comparado en el texto '
                             'con:',
                 'alternativas': ['Una fórmula matemática',
                                  'Una pintura hecha con palabras',
                                  'Un poema exclusivamente',
                                  'Una noticia breve',
                                  'Un discurso político'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta una tesis con argumentos '
                             'para persuadir al lector se llama texto:',
                 'alternativas': ['Dialógico',
                                  'Narrativo',
                                  'Argumentativo',
                                  'Descriptivo',
                                  'Instructivo'],
                 'correcta': 'C'},
                {'pregunta': 'La finalidad principal del texto argumentativo '
                             'es:',
                 'alternativas': ['Narrar hechos',
                                  'Describir un paisaje',
                                  'Enumerar datos',
                                  'Dar una receta',
                                  'Persuadir al lector sobre un punto de '
                                  'vista'],
                 'correcta': 'E'},
                {'pregunta': 'El carácter comunicativo del texto se '
                             'relaciona con:',
                 'alternativas': ['Su color',
                                  'Su función social',
                                  'Su extensión física',
                                  'Su formato de impresión',
                                  'Su tipografía'],
                 'correcta': 'C'},
                {'pregunta': 'El carácter pragmático del texto implica que '
                             'se produce con:',
                 'alternativas': ['Total aleatoriedad',
                                  'Solo fines comerciales',
                                  'Ninguna intención',
                                  'Solo fines estéticos',
                                  'Una intención y en una situación '
                                  'concreta'],
                 'correcta': 'E'},
                {'pregunta': 'Descubrir la idea de mayor jerarquía en un '
                             'texto es fundamental para lograr:',
                 'alternativas': ['Solo memorizar el texto',
                                  'Ignorar las ideas secundarias',
                                  'Evitar el análisis',
                                  'Una comprensión cabal del texto',
                                  'Reducir el vocabulario'],
                 'correcta': 'D'},
                {'pregunta': 'Las ideas secundarias cumplen el papel de '
                             'fundamentar, explicar y:',
                 'alternativas': ['Reemplazar el tema',
                                  'Contradecir la idea principal',
                                  'Eliminar la idea principal',
                                  'Sustituir el título',
                                  'Presentar con diversos recursos la idea '
                                  'principal'],
                 'correcta': 'E'},
                {'pregunta': 'El tema de un texto puede ser un aspecto '
                             'general como:',
                 'alternativas': ['Solo un lugar geográfico',
                                  'Solo un nombre propio',
                                  'El cáncer, la violencia o la política',
                                  'Solo una fecha',
                                  'Solo un número'],
                 'correcta': 'C'},
                {'pregunta': 'El texto, según el concepto general, es un '
                             'acto de habla o una serie de actos '
                             'lingüísticos realizados en:',
                 'alternativas': ['Cualquier situación sin contexto',
                                  'Un vacío comunicativo',
                                  'Una situación comunicativa determinada',
                                  'Ausencia total de intención',
                                  'Un contexto irrelevante'],
                 'correcta': 'C'},
                {'pregunta': 'El texto que contiene noticias de carácter '
                             'real, propio del contexto periodístico, se '
                             'llama texto:',
                 'alternativas': ['Informativo',
                                  'Filosófico',
                                  'Científico',
                                  'Humanístico',
                                  'Literario'],
                 'correcta': 'A'},
                {'pregunta': 'El texto que contiene resultados de una '
                             'investigación, expuestos en monografías o '
                             'tesis, se llama texto:',
                 'alternativas': ['Filosófico',
                                  'Científico',
                                  'Humanístico',
                                  'Informativo',
                                  'Literario'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que contiene reflexiones sobre las '
                             'causas y fines primeros de la existencia '
                             'humana se llama texto:',
                 'alternativas': ['Humanístico',
                                  'Informativo',
                                  'Filosófico',
                                  'Literario',
                                  'Científico'],
                 'correcta': 'C'},
                {'pregunta': 'El texto que constituye obras donde prima la '
                             'belleza del lenguaje, como novelas o poemas, '
                             'se llama texto:',
                 'alternativas': ['Científico',
                                  'Literario',
                                  'Humanístico',
                                  'Informativo',
                                  'Filosófico'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta la idea principal al '
                             'inicio del párrafo, explicada por las ideas '
                             'secundarias, se llama texto:',
                 'alternativas': ['Paralelo',
                                  'Analizante',
                                  'Encuadrado',
                                  'Centrado',
                                  'Sintetizante'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta la idea principal al '
                             'final del párrafo, como síntesis de lo '
                             'anterior, se llama texto:',
                 'alternativas': ['Paralelo',
                                  'Sintetizante',
                                  'Centrado',
                                  'Encuadrado',
                                  'Analizante'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta la idea principal al '
                             'medio del párrafo se llama texto:',
                 'alternativas': ['Paralelo',
                                  'Encuadrado',
                                  'Sintetizante',
                                  'Centrado',
                                  'Analizante'],
                 'correcta': 'D'},
                {'pregunta': 'El texto que presenta la idea principal al '
                             'inicio y al final del párrafo se llama texto:',
                 'alternativas': ['Sintetizante',
                                  'Analizante',
                                  'Paralelo',
                                  'Centrado',
                                  'Encuadrado'],
                 'correcta': 'E'},
                {'pregunta': 'El texto que no presenta idea principal ni '
                             'ideas secundarias, donde todas las ideas '
                             'tienen igual importancia, se llama texto:',
                 'alternativas': ['Centrado',
                                  'Encuadrado',
                                  'Analizante',
                                  'Sintetizante',
                                  'Paralelo'],
                 'correcta': 'E'},
                {'pregunta': 'El nivel de comprensión lectora que se somete '
                             'estrictamente a los contenidos explícitos del '
                             'texto, sin interpretación, se llama nivel:',
                 'alternativas': ['Inferencial',
                                  'Deductivo',
                                  'Literal',
                                  'Valorativo',
                                  'Crítico'],
                 'correcta': 'C'},
                {'pregunta': 'El nivel de comprensión lectora que busca '
                             'relaciones más allá de lo establecido en el '
                             'texto, formulando hipótesis, se llama nivel:',
                 'alternativas': ['Textual',
                                  'Literal',
                                  'Crítico',
                                  'Lineal',
                                  'Inferencial'],
                 'correcta': 'E'},
                {'pregunta': 'La meta del nivel inferencial de comprensión '
                             'lectora es la elaboración de:',
                 'alternativas': ['Resúmenes',
                                  'Definiciones',
                                  'Glosarios',
                                  'Conclusiones',
                                  'Transcripciones'],
                 'correcta': 'D'},
                {'pregunta': 'El nivel de comprensión lectora que emite '
                             'juicios sobre el texto, aceptándolo o '
                             'rechazándolo con fundamentos, se llama nivel:',
                 'alternativas': ['Deductivo',
                                  'Literal',
                                  'Inferencial',
                                  'Crítico',
                                  'Textual'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONCEPTO DEL TEXTO',
                      'items': ['«Texto» proviene del latín «textus», que '
                                'significa «tejido».',
                                'El texto es una unidad '
                                'semántico-estructural, de contenido y '
                                'forma, que tiene como base al párrafo.',
                                'El texto tiene un carácter comunicativo, un '
                                'carácter pragmático y un carácter '
                                'estructurado.']},
                     {'titulo': 'ESTRUCTURA INTERNA DEL TEXTO',
                      'items': ['La idea principal es la tesis o '
                                'planteamiento central que el autor '
                                'desarrolla, el núcleo del discurso.',
                                'Las ideas secundarias sirven de argumento a '
                                'la idea principal, fundamentándola y '
                                'explicándola.',
                                'El tema es todo aquello de lo que se habla '
                                'en el texto, el asunto descrito y '
                                'desarrollado.']},
                     {'titulo': 'CLASES DE TEXTO POR SU FORMA',
                      'items': ['El texto narrativo presenta una sucesión de '
                                'acciones en el tiempo, para contar hechos '
                                'reales o ficticios.',
                                'El texto descriptivo representa por medio '
                                'de palabras un objeto, paisaje o persona, '
                                'como una pintura verbal.',
                                'El texto argumentativo presenta una tesis y '
                                'argumentos con el objetivo de persuadir al '
                                'lector.']},
                     {'titulo': 'CLASES DE TEXTO POR SU CONTENIDO',
                      'items': ['El texto informativo contiene noticias de '
                                'carácter real; su uso es propio del '
                                'contexto periodístico.',
                                'El texto científico contiene resultados de '
                                'una investigación, expuestos en '
                                'monografías, tesis o artículos científicos.',
                                'El texto filosófico contiene reflexiones '
                                'sobre las causas y fines primeros de la '
                                'existencia humana.']},
                     {'titulo': 'CLASES DE TEXTO POR SU ESTRUCTURA',
                      'items': ['El texto analizante presenta la idea '
                                'principal al inicio del párrafo, explicada '
                                'luego por las ideas secundarias.',
                                'El texto sintetizante presenta la idea '
                                'principal al final del párrafo, como '
                                'síntesis de lo anterior.',
                                'El texto centrado presenta la idea '
                                'principal al medio del párrafo.']},
                     {'titulo': 'CONCEPTO DE LECTURA Y NIVEL LITERAL',
                      'items': ['La lectura es la actividad mental de '
                                'percepción, comprensión y reacción que '
                                'permite informarse del contenido de un '
                                'texto.',
                                'El nivel literal, textual o lineal, se '
                                'somete estrictamente a los contenidos '
                                'explícitos del texto, sin entrar en '
                                'interpretación.']},
                     {'titulo': 'NIVEL INFERENCIAL',
                      'items': ['El nivel inferencial, deductivo o '
                                'extralineal, busca relaciones que van más '
                                'allá de lo establecido en el texto.',
                                'El nivel inferencial incluye: inferir ideas '
                                'principales no explícitas, inferir '
                                'relaciones de causa y efecto, y predecir '
                                'acontecimientos.',
                                'La meta del nivel inferencial es la '
                                'elaboración de conclusiones.']},
                     {'titulo': 'NIVEL CRÍTICO',
                      'items': ['El nivel crítico emite juicios sobre el '
                                'texto leído, aceptándolo o rechazándolo con '
                                'fundamentos.',
                                'Los juicios del nivel crítico pueden ser de '
                                'realidad o fantasía, de adecuación y '
                                'validez, de apropiación, o de rechazo o '
                                'aceptación.']}]},
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
                {'titulo': '16.4 LA HOMONIMIA',
                 'items': ['La {homofonía} se produce cuando las palabras '
                           'tienen igual sonido pero escritura y '
                           '{significado} distintos: rebelar/{revelar}, '
                           'bello/vello, ojear/hojear.',
                           'La {homografía} se produce cuando las palabras '
                           'tienen igual escritura y pronunciación, pero '
                           '{significados} distintos: lima '
                           '(fruta/herramienta), cura '
                           '(sacerdote/curación).']},
                {'titulo': '16.5 HIPERONIMIA, HIPONIMIA, HOLONIMIA Y '
                           'MERONIMIA',
                 'items': ['La {hiperonimia} establece la relación '
                           'genérico-específica: {flor} es hiperónimo de '
                           'rosa.',
                           'La {hiponimia} establece la relación '
                           'específico-genérico: {mesa} es hipónimo de '
                           'mueble.',
                           'La {cohiponimia} relaciona hipónimos de un mismo '
                           'hiperónimo: lechuga y zanahoria son cohipónimos '
                           'de {hortaliza}.',
                           'La {holonimia} establece la relación todo-parte: '
                           '{árbol} es holónimo de rama.',
                           'La {meronimia} establece la relación parte-todo: '
                           '{pedal} es merónimo de bicicleta.',
                           'La {comeronimia} relaciona merónimos de un mismo '
                           'holónimo: raíz, tallo y hojas son comerónimos de '
                           '{árbol}.']},
                {'titulo': '16.6 ANALOGÍAS: CONCEPTO Y SIMÉTRICAS',
                 'items': ['La {analogía} es la semejanza de relación que '
                           'existe entre dos pares de palabras: una '
                           '{premisa} o base, y cinco alternativas.',
                           'Las analogías {simétricas} permiten intercambiar '
                           'libremente el orden de los componentes, porque '
                           'son equivalentes entre sí.',
                           'Las analogías de {sinonimia} relacionan términos '
                           'de significado semejante: sereno : ecuánime.',
                           'Las analogías de {complementariedad} vinculan '
                           'objetos que se requieren mutuamente: violín : '
                           'arco.',
                           'Las analogías {cogenéricas} tienen como atributo '
                           'esencial la pertenencia a la misma clase o '
                           'categoría: oro : plata (metales).']},
                {'titulo': '16.7 ANALOGÍAS ASIMÉTRICAS Y '
                           'DENOTACIÓN/CONNOTACIÓN',
                 'items': ['Las analogías {asimétricas} exigen respetar el '
                           'mismo orden de la base en la respuesta, sin '
                           'poder intercambiarse.',
                           'Las analogías de {antonimia} relacionan términos '
                           'de significado opuesto, respetando el mismo '
                           'orden: empezar : concluir.',
                           'La {denotación} es la relación objetiva entre '
                           'significante y referente; es el significado '
                           '{universal} de una palabra, usado en textos '
                           'técnicos y científicos.',
                           'La {connotación} es el doble sentido o sentido '
                           'figurado atribuido a las palabras; es '
                           '{subjetiva} y propia del lenguaje literario: '
                           '«Esa señorita es un bombón».']}],
  'cuadros': [{'titulo': '16.1-16.3 LAS TRES RELACIONES SEMÁNTICAS',
               'encabezados': ['Relación', 'Característica'],
               'filas': [['{Sinonimia}', 'Significados {semejantes}'],
                         ['{Antonimia}', 'Significados {contrarios}'],
                         ['{Paronimia}',
                          'Sonido {semejante}, significado distinto']]}],
  'preguntas': [{'pregunta': 'Etimológicamente, «sinónimo» significa:',
                 'alternativas': ['Ausencia de significado',
                                  'Oposición de ideas',
                                  'Equivalencia o afinidad de significados',
                                  'Sonido contrario',
                                  'Escritura similar'],
                 'correcta': 'C'},
                {'pregunta': 'La sinonimia es la semejanza de significados '
                             'entre términos comprendidos en un mismo:',
                 'alternativas': ['Campo sintáctico exclusivo',
                                  'Campo fonológico',
                                  'Campo gráfico',
                                  'Campo morfológico exclusivo',
                                  'Campo semántico'],
                 'correcta': 'E'},
                {'pregunta': 'Los sinónimos, además de significados '
                             'parecidos, pertenecen a la misma:',
                 'alternativas': ['Categoría fonológica',
                                  'Familia léxica exclusiva',
                                  'Raíz etimológica exclusiva',
                                  'Categoría ortográfica',
                                  'Clase gramatical'],
                 'correcta': 'E'},
                {'pregunta': 'Los sinónimos que mantienen el mismo '
                             'significado sin importar el contexto se llaman '
                             'sinónimos:',
                 'alternativas': ['Absolutos',
                                  'Contextuales',
                                  'Parciales',
                                  'Indirectos',
                                  'Relativos'],
                 'correcta': 'A'},
                {'pregunta': '«Casa» y «vivienda» son un ejemplo de '
                             'sinónimos:',
                 'alternativas': ['Parciales',
                                  'Antónimos',
                                  'Absolutos',
                                  'Relativos',
                                  'Parónimos'],
                 'correcta': 'C'},
                {'pregunta': 'Los sinónimos que cambian de sentido según el '
                             'contexto se llaman sinónimos:',
                 'alternativas': ['Directos',
                                  'Relativos o indirectos',
                                  'Universales',
                                  'Absolutos',
                                  'Parciales fijos'],
                 'correcta': 'B'},
                {'pregunta': 'Los antónimos se definen como palabras de la '
                             'misma categoría gramatical que expresan '
                             'significados:',
                 'alternativas': ['Contrarios',
                                  'Semejantes',
                                  'Neutros',
                                  'Idénticos',
                                  'Ambiguos'],
                 'correcta': 'A'},
                {'pregunta': 'Los antónimos que expresan ideas total y '
                             'exactamente contrarias se llaman antónimos:',
                 'alternativas': ['Semánticos exclusivos',
                                  'Indirectos',
                                  'Relativos',
                                  'Parciales',
                                  'Absolutos'],
                 'correcta': 'E'},
                {'pregunta': '«Introvertido» y «extrovertido» son un ejemplo '
                             'de antónimos:',
                 'alternativas': ['Relativos',
                                  'Parciales',
                                  'Sinónimos',
                                  'Parónimos',
                                  'Absolutos'],
                 'correcta': 'E'},
                {'pregunta': 'Los antónimos que muestran ideas parcialmente '
                             'opuestas se llaman antónimos:',
                 'alternativas': ['Totales',
                                  'Puros',
                                  'Absolutos',
                                  'Directos',
                                  'Relativos'],
                 'correcta': 'E'},
                {'pregunta': '«Cima» y «planicie» son un ejemplo de '
                             'antónimos:',
                 'alternativas': ['Relativos',
                                  'Sinónimos',
                                  'Absolutos',
                                  'Homófonos',
                                  'Parónimos'],
                 'correcta': 'A'},
                {'pregunta': 'La paronimia ocurre cuando dos palabras se '
                             'asemejan en:',
                 'alternativas': ['Su significado',
                                  'Su origen etimológico exclusivamente',
                                  'Su extensión',
                                  'Su categoría gramatical exclusivamente',
                                  'Su sonido, pero se escriben diferente'],
                 'correcta': 'E'},
                {'pregunta': 'Los parónimos, a diferencia de los sinónimos, '
                             'tienen significados:',
                 'alternativas': ['Opuestos exactamente',
                                  'Ambiguos',
                                  'Idénticos siempre',
                                  'Distintos',
                                  'Iguales'],
                 'correcta': 'D'},
                {'pregunta': 'Los parónimos diferenciados por el acento, '
                             'como «ánimo», «animo» y «animó», son parónimos '
                             'por:',
                 'alternativas': ['El significado',
                                  'La escritura',
                                  'El acento',
                                  'El origen',
                                  'La categoría gramatical'],
                 'correcta': 'C'},
                {'pregunta': '«Actitud» (postura) y «aptitud» (idoneidad) '
                             'son un ejemplo de parónimos por:',
                 'alternativas': ['El sonido idéntico',
                                  'La escritura',
                                  'El acento',
                                  'El significado igual',
                                  'La sinonimia'],
                 'correcta': 'B'},
                {'pregunta': '«Absolver» (perdonar) y «absorber» (beber) son '
                             'un ejemplo de parónimos por:',
                 'alternativas': ['La antonimia',
                                  'La sinonimia',
                                  'El acento',
                                  'El campo semántico',
                                  'La escritura'],
                 'correcta': 'E'},
                {'pregunta': 'En «El sacerdote habló de la oración» y «El '
                             'alumno escribió una oración», la palabra '
                             '«oración» ejemplifica:',
                 'alternativas': ['Un antónimo absoluto',
                                  'Un antónimo relativo',
                                  'Un sinónimo absoluto',
                                  'Un sinónimo relativo',
                                  'Un parónimo por el acento'],
                 'correcta': 'D'},
                {'pregunta': '«Rapidez» y «lentitud» son un ejemplo de:',
                 'alternativas': ['Antónimos',
                                  'Homófonos',
                                  'Sinónimos relativos',
                                  'Parónimos por el acento',
                                  'Sinónimos absolutos'],
                 'correcta': 'A'},
                {'pregunta': 'Alcalde y alcaide son un ejemplo de:',
                 'alternativas': ['Sinónimos absolutos',
                                  'Parónimos por la escritura',
                                  'Antónimos relativos',
                                  'Sinónimos relativos',
                                  'Antónimos absolutos'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres relaciones semánticas estudiadas son '
                             'sinonimia, antonimia y:',
                 'alternativas': ['Ortografía',
                                  'Sintaxis',
                                  'Fonética',
                                  'Paronimia',
                                  'Morfología'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras que tienen igual sonido pero '
                             'escritura y significado distintos, como '
                             '«bello» y «vello», presentan:',
                 'alternativas': ['Homografía',
                                  'Paronimia',
                                  'Sinonimia',
                                  'Homofonía',
                                  'Hiperonimia'],
                 'correcta': 'D'},
                {'pregunta': 'Las palabras que tienen igual escritura y '
                             'pronunciación, pero significados distintos, '
                             'como «lima» (fruta/herramienta), presentan:',
                 'alternativas': ['Hiponimia',
                                  'Paronimia',
                                  'Homografía',
                                  'Homofonía',
                                  'Antonimia'],
                 'correcta': 'C'},
                {'pregunta': 'La relación semántica genérico-específica, '
                             'como en «flor es hiperónimo de rosa», se '
                             'llama:',
                 'alternativas': ['Meronimia',
                                  'Hiponimia',
                                  'Hiperonimia',
                                  'Holonimia',
                                  'Homonimia'],
                 'correcta': 'C'},
                {'pregunta': 'La relación semántica específico-genérico, '
                             'como en «mesa es hipónimo de mueble», se '
                             'llama:',
                 'alternativas': ['Hiperonimia',
                                  'Meronimia',
                                  'Hiponimia',
                                  'Holonimia',
                                  'Cohiponimia'],
                 'correcta': 'C'},
                {'pregunta': 'La relación semántica todo-parte, como en '
                             '«árbol es holónimo de rama», se llama:',
                 'alternativas': ['Holonimia',
                                  'Comeronimia',
                                  'Hiperonimia',
                                  'Hiponimia',
                                  'Meronimia'],
                 'correcta': 'A'},
                {'pregunta': 'La relación semántica parte-todo, como en '
                             '«pedal es merónimo de bicicleta», se llama:',
                 'alternativas': ['Holonimia',
                                  'Meronimia',
                                  'Hiperonimia',
                                  'Hiponimia',
                                  'Cohiponimia'],
                 'correcta': 'B'},
                {'pregunta': 'La semejanza de relación que existe entre dos '
                             'pares de palabras, estructurada en una premisa '
                             'y cinco alternativas, se llama:',
                 'alternativas': ['Sinonimia',
                                  'Antonimia',
                                  'Homonimia',
                                  'Analogía',
                                  'Paronimia'],
                 'correcta': 'D'},
                {'pregunta': 'Las analogías en las que el orden de los '
                             'componentes puede intercambiarse libremente, '
                             'por ser equivalentes, se llaman analogías:',
                 'alternativas': ['Cogenéricas exclusivas',
                                  'Simétricas',
                                  'De complementariedad exclusiva',
                                  'Asimétricas',
                                  'De antonimia'],
                 'correcta': 'B'},
                {'pregunta': 'Las analogías que relacionan términos de '
                             'significado semejante, como «sereno : '
                             'ecuánime», se llaman analogías de:',
                 'alternativas': ['Cogenericidad',
                                  'Sinonimia',
                                  'Homonimia',
                                  'Antonimia',
                                  'Complementariedad'],
                 'correcta': 'B'},
                {'pregunta': 'Las analogías que vinculan objetos que se '
                             'requieren mutuamente para cumplir su función, '
                             'como «violín : arco», se llaman analogías de:',
                 'alternativas': ['Antonimia',
                                  'Sinonimia',
                                  'Complementariedad',
                                  'Meronimia',
                                  'Cogenericidad'],
                 'correcta': 'C'},
                {'pregunta': 'Las analogías en las que debe respetarse el '
                             'mismo orden de la base en la respuesta, sin '
                             'poder intercambiarse, se llaman analogías:',
                 'alternativas': ['Asimétricas',
                                  'Cogenéricas exclusivas',
                                  'De complementariedad exclusiva',
                                  'Simétricas',
                                  'De sinonimia exclusiva'],
                 'correcta': 'A'},
                {'pregunta': 'La relación objetiva entre el significante y '
                             'el referente, con significado universal, '
                             'propia de textos técnicos, se llama:',
                 'alternativas': ['Connotación',
                                  'Sinonimia',
                                  'Denotación',
                                  'Polisemia',
                                  'Homonimia'],
                 'correcta': 'C'},
                {'pregunta': 'El doble sentido o sentido figurado que se '
                             'atribuye a las palabras, de carácter subjetivo '
                             'y propio del lenguaje literario, se llama:',
                 'alternativas': ['Sinonimia',
                                  'Antonimia',
                                  'Connotación',
                                  'Homonimia',
                                  'Denotación'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LA SINONIMIA',
                      'items': ['Etimológicamente, «sinónimo» proviene del '
                                'griego «sin» (con) y «onomas» (nombre), es '
                                'decir, equivalencia de significados.',
                                'La sinonimia es la semejanza de '
                                'significados entre términos comprendidos en '
                                'un mismo campo semántico.',
                                'Los sinónimos pertenecen a la misma clase '
                                'gramatical y poseen significados '
                                'parecidos.']},
                     {'titulo': 'LA ANTONIMIA',
                      'items': ['Los antónimos son palabras de la misma '
                                'categoría gramatical que expresan '
                                'significados contrarios.',
                                'Los antónimos absolutos expresan ideas '
                                'total y exactamente contrarias, como '
                                '«introvertido» y «extrovertido».',
                                'Los antónimos relativos muestran ideas '
                                'parcialmente opuestas, sin oposición '
                                'plena.']},
                     {'titulo': 'LA PARONIMIA',
                      'items': ['La paronimia ocurre cuando dos palabras se '
                                'asemejan en su sonido pero se escriben '
                                'distinto y tienen significados diferentes.',
                                'Los parónimos por el acento cambian de '
                                'significado según sean esdrújulas, llanas o '
                                'agudas, como «ánimo», «animo» y «animó».',
                                'Los parónimos por la escritura tienen '
                                'significados distintos, como «actitud» '
                                '(postura) y «aptitud» (idoneidad).']},
                     {'titulo': 'LA HOMONIMIA',
                      'items': ['La homofonía se produce cuando las palabras '
                                'tienen igual sonido pero escritura y '
                                'significado distintos: rebelar/revelar, '
                                'bello/vello, ojear/hojear.',
                                'La homografía se produce cuando las '
                                'palabras tienen igual escritura y '
                                'pronunciación, pero significados distintos: '
                                'lima (fruta/herramienta), cura '
                                '(sacerdote/curación).']},
                     {'titulo': 'HIPERONIMIA, HIPONIMIA, HOLONIMIA Y '
                                'MERONIMIA',
                      'items': ['La hiperonimia establece la relación '
                                'genérico-específica: flor es hiperónimo de '
                                'rosa.',
                                'La hiponimia establece la relación '
                                'específico-genérico: mesa es hipónimo de '
                                'mueble.',
                                'La cohiponimia relaciona hipónimos de un '
                                'mismo hiperónimo: lechuga y zanahoria son '
                                'cohipónimos de hortaliza.']},
                     {'titulo': 'ANALOGÍAS: CONCEPTO Y SIMÉTRICAS',
                      'items': ['La analogía es la semejanza de relación que '
                                'existe entre dos pares de palabras: una '
                                'premisa o base, y cinco alternativas.',
                                'Las analogías simétricas permiten '
                                'intercambiar libremente el orden de los '
                                'componentes, porque son equivalentes entre '
                                'sí.',
                                'Las analogías de sinonimia relacionan '
                                'términos de significado semejante: sereno : '
                                'ecuánime.']},
                     {'titulo': 'ANALOGÍAS ASIMÉTRICAS Y '
                                'DENOTACIÓN/CONNOTACIÓN',
                      'items': ['Las analogías asimétricas exigen respetar '
                                'el mismo orden de la base en la respuesta, '
                                'sin poder intercambiarse.',
                                'Las analogías de antonimia relacionan '
                                'términos de significado opuesto, respetando '
                                'el mismo orden: empezar : concluir.',
                                'La denotación es la relación objetiva entre '
                                'significante y referente; es el significado '
                                'universal de una palabra, usado en textos '
                                'técnicos y científicos.']}]}]
