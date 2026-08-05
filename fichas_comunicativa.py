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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La comunicación se define como el proceso a '
                           'través del cual dos o más individuos '
                           '{Interactúan para intercambiar información}.',
                           'La fase de la comunicación constituida por la '
                           'codificación y decodificación mental es la fase '
                           '{Psíquica}.',
                           'La fase que se refiere al funcionamiento del '
                           'aparato fonador y la audición es la fase '
                           '{Fisiológica}.',
                           'El elemento de la comunicación que codifica y '
                           'transmite el mensaje es {El emisor}.',
                           'El elemento que percibe y decodifica el mensaje '
                           'es {El receptor}.',
                           'El medio físico a través del cual se transporta '
                           'el mensaje se llama {Canal}.',
                           'El sistema de signos convencionales que usan '
                           'emisor y receptor se llama {Código}.',
                           'El conjunto de objetos o fenómenos a los que se '
                           'hace mención en el acto comunicativo es {El '
                           'referente}.',
                           'El lugar y momento en que se desarrolla el acto '
                           'comunicativo se denomina {Circunstancia o '
                           'contexto}.',
                           'La comunicación que utiliza el idioma para '
                           'codificar el mensaje es la comunicación '
                           '{Lingüística}.',
                           'La comunicación oral se caracteriza por ser '
                           '{Sincrónica y momentánea}.',
                           'La comunicación escrita se caracteriza por ser '
                           '{Asincrónica y planificada}.',
                           'La disciplina que estudia los movimientos '
                           'corporales y gestos es la {Kinésica}.',
                           'La disciplina que estudia las relaciones de '
                           'proximidad entre interlocutores es la '
                           '{Proxémica}.',
                           'La disciplina que estudia el contacto ocular '
                           'durante la comunicación es la {Oculésica}.',
                           'La disciplina que estudia el uso del tiempo en '
                           'la comunicación es la {Cronémica}.',
                           'El monólogo interior y el soliloquio son '
                           'ejemplos de comunicación {Intrapersonal}.',
                           'La comunicación que se produce cuando '
                           'interactúan dos personas es la {Interpersonal}.',
                           'La interacción entre ciudadanos y medios de '
                           'comunicación masivos es la comunicación '
                           '{Pública}.',
                           'La comunicación grupal se orienta al '
                           'cumplimiento de {Objetivos comunes del '
                           'grupo}.']}],
  'cuadros': [{'titulo': '1.3 DISCIPLINAS DE LA COMUNICACIÓN NO LINGÜÍSTICA',
               'encabezados': ['Disciplina', 'Estudia'],
               'filas': [['{Kinésica}', 'Movimientos, posturas y {gestos}'],
                         ['{Proxémica}',
                          'Relaciones de {proximidad} o alejamiento'],
                         ['{Oculésica}', 'El {contacto} ocular'],
                         ['{Háptica}', 'El contacto físico y sus {efectos}'],
                         ['{Cronémica}', 'El uso del {tiempo}']]}],
  'preguntas': [{'pregunta': 'La comunicación se define como el proceso a '
                             'través del cual dos o más individuos:',
                 'alternativas': ['Compiten entre sí',
                                  'Interactúan para intercambiar información',
                                  'Se aíslan mutuamente',
                                  'Ejercen autoridad',
                                  'Compran bienes'],
                 'correcta': 'B'},
                {'pregunta': 'La fase de la comunicación constituida por la '
                             'codificación y decodificación mental es la '
                             'fase:',
                 'alternativas': ['Física',
                                  'Psíquica',
                                  'Fisiológica',
                                  'Social',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'La fase que se refiere al funcionamiento del '
                             'aparato fonador y la audición es la fase:',
                 'alternativas': ['Psíquica',
                                  'Fisiológica',
                                  'Física',
                                  'Social',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento de la comunicación que codifica y '
                             'transmite el mensaje es:',
                 'alternativas': ['El receptor',
                                  'El emisor',
                                  'El canal',
                                  'El código',
                                  'El referente'],
                 'correcta': 'B'},
                {'pregunta': 'El elemento que percibe y decodifica el '
                             'mensaje es:',
                 'alternativas': ['El emisor',
                                  'El receptor',
                                  'El canal',
                                  'El mensaje',
                                  'El código'],
                 'correcta': 'B'},
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
                 'alternativas': ['Canal',
                                  'Código',
                                  'Mensaje',
                                  'Referente',
                                  'Circunstancia'],
                 'correcta': 'B'},
                {'pregunta': 'El conjunto de objetos o fenómenos a los que '
                             'se hace mención en el acto comunicativo es:',
                 'alternativas': ['El código',
                                  'El referente',
                                  'El canal',
                                  'El emisor',
                                  'El receptor'],
                 'correcta': 'B'},
                {'pregunta': 'El lugar y momento en que se desarrolla el '
                             'acto comunicativo se denomina:',
                 'alternativas': ['Código',
                                  'Circunstancia o contexto',
                                  'Referente',
                                  'Canal',
                                  'Mensaje'],
                 'correcta': 'B'},
                {'pregunta': 'La comunicación que utiliza el idioma para '
                             'codificar el mensaje es la comunicación:',
                 'alternativas': ['No lingüística',
                                  'Lingüística',
                                  'Kinésica',
                                  'Proxémica',
                                  'Cromática'],
                 'correcta': 'B'},
                {'pregunta': 'La comunicación oral se caracteriza por ser:',
                 'alternativas': ['Duradera y planificada',
                                  'Sincrónica y momentánea',
                                  'Asincrónica',
                                  'Siempre escrita',
                                  'Sin recursos no verbales'],
                 'correcta': 'B'},
                {'pregunta': 'La comunicación escrita se caracteriza por '
                             'ser:',
                 'alternativas': ['Sincrónica',
                                  'Asincrónica y planificada',
                                  'Efímera',
                                  'Sin cohesión',
                                  'Sin puntuación'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia los movimientos '
                             'corporales y gestos es la:',
                 'alternativas': ['Proxémica',
                                  'Kinésica',
                                  'Cronémica',
                                  'Háptica',
                                  'Acústica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia las relaciones de '
                             'proximidad entre interlocutores es la:',
                 'alternativas': ['Kinésica',
                                  'Proxémica',
                                  'Oculésica',
                                  'Facial',
                                  'Cromática'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia el contacto ocular '
                             'durante la comunicación es la:',
                 'alternativas': ['Háptica',
                                  'Oculésica',
                                  'Cronémica',
                                  'Kinésica',
                                  'Acústica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia el uso del tiempo en '
                             'la comunicación es la:',
                 'alternativas': ['Proxémica',
                                  'Cronémica',
                                  'Háptica',
                                  'Facial',
                                  'Cromática'],
                 'correcta': 'B'},
                {'pregunta': 'El monólogo interior y el soliloquio son '
                             'ejemplos de comunicación:',
                 'alternativas': ['Interpersonal',
                                  'Intrapersonal',
                                  'Grupal',
                                  'Pública',
                                  'Masiva'],
                 'correcta': 'B'},
                {'pregunta': 'La comunicación que se produce cuando '
                             'interactúan dos personas es la:',
                 'alternativas': ['Intrapersonal',
                                  'Interpersonal',
                                  'Grupal',
                                  'Pública',
                                  'Social'],
                 'correcta': 'B'},
                {'pregunta': 'La interacción entre ciudadanos y medios de '
                             'comunicación masivos es la comunicación:',
                 'alternativas': ['Grupal',
                                  'Pública',
                                  'Intrapersonal',
                                  'Interpersonal',
                                  'Privada'],
                 'correcta': 'B'},
                {'pregunta': 'La comunicación grupal se orienta al '
                             'cumplimiento de:',
                 'alternativas': ['Objetivos individuales',
                                  'Objetivos comunes del grupo',
                                  'Ninguna finalidad',
                                  'Metas ajenas al grupo',
                                  'Reglas externas impuestas'],
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
                           '{biológico} moldeado por la evolución.']},
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según la RAE, el lenguaje es la facultad de '
                           'expresarse mediante el sonido articulado u otros '
                           '{Sistemas de signos}.',
                           'Según Sapir, el lenguaje es un método '
                           'exclusivamente humano y {No instintivo}.',
                           'Según Pinker, el lenguaje es una capacidad '
                           '{Innata del Homo sapiens}.',
                           'Que el lenguaje sea usado por todos los seres '
                           'humanos corresponde a la característica de ser '
                           '{Universal}.',
                           'Que el lenguaje se manifieste de forma oral, '
                           'escrita, gestual o musical corresponde a que es '
                           '{Multiforme}.',
                           'Que el lenguaje sea resultado de un acuerdo '
                           'comunitario corresponde a que es {Convencional}.',
                           'Que el lenguaje funcione de acuerdo a normas o '
                           'reglas corresponde a que es {Sistémico}.',
                           'Que una palabra represente algo concreto o '
                           'abstracto corresponde a que el lenguaje es '
                           '{Simbólico}.',
                           'La función del lenguaje centrada en el emisor, '
                           'que manifiesta emociones, es la función '
                           '{Expresiva}.',
                           'La función centrada en el receptor, que busca '
                           'que actúe mediante órdenes, es la función '
                           '{Apelativa}.',
                           'La función centrada en el contenido, propia de '
                           'textos informativos, es la función {Referencial '
                           'o representativa}.',
                           'La función que se usa cuando el código se '
                           'refiere al código mismo es la función '
                           '{Metalingüística}.',
                           'La función centrada en el canal, que mantiene el '
                           'contacto entre interlocutores, es la función '
                           '{Fática}.',
                           'La función centrada en el mensaje, propia de las '
                           'obras literarias, es la función {Poética}.',
                           'Según Saussure, el lenguaje tiene dos planos '
                           'interdependientes: lengua y {Habla}.',
                           'La lengua, según Saussure, es de carácter '
                           '{Social}.',
                           'El habla, según Saussure, es de carácter '
                           '{Individual}.',
                           'El habla se realiza físicamente por medio de '
                           '{Los órganos de fonación}.']}],
  'cuadros': [{'titulo': '2.3 LAS SEIS FUNCIONES DEL LENGUAJE',
               'encabezados': ['Función', 'Centrada en'],
               'filas': [['{Expresiva}', 'El {emisor}'],
                         ['{Apelativa}', 'El {receptor}'],
                         ['{Referencial}', 'El {contenido}'],
                         ['{Metalingüística}', 'El {código}'],
                         ['{Fática}', 'El {canal}'],
                         ['{Poética}', 'El {mensaje}']]}],
  'preguntas': [{'pregunta': 'Según la RAE, el lenguaje es la facultad de '
                             'expresarse mediante el sonido articulado u '
                             'otros:',
                 'alternativas': ['Instintos',
                                  'Sistemas de signos',
                                  'Ruidos naturales',
                                  'Reflejos biológicos',
                                  'Impulsos'],
                 'correcta': 'B'},
                {'pregunta': 'Según Sapir, el lenguaje es un método '
                             'exclusivamente humano y:',
                 'alternativas': ['Instintivo',
                                  'No instintivo',
                                  'Genético únicamente',
                                  'Animal',
                                  'Universal en todas las especies'],
                 'correcta': 'B'},
                {'pregunta': 'Según Pinker, el lenguaje es una capacidad:',
                 'alternativas': ['Aprendida exclusivamente',
                                  'Innata del Homo sapiens',
                                  'Exclusiva de algunas culturas',
                                  'Artificial',
                                  'Adquirida solo en la escuela'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje sea usado por todos los seres '
                             'humanos corresponde a la característica de '
                             'ser:',
                 'alternativas': ['Multiforme',
                                  'Universal',
                                  'Simbólico',
                                  'Sistémico',
                                  'Innato'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje se manifieste de forma oral, '
                             'escrita, gestual o musical corresponde a que '
                             'es:',
                 'alternativas': ['Universal',
                                  'Multiforme',
                                  'Convencional',
                                  'Racional',
                                  'Aprendido'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje sea resultado de un acuerdo '
                             'comunitario corresponde a que es:',
                 'alternativas': ['Simbólico',
                                  'Convencional',
                                  'Sistémico',
                                  'Innato',
                                  'Cultural exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Que el lenguaje funcione de acuerdo a normas o '
                             'reglas corresponde a que es:',
                 'alternativas': ['Simbólico',
                                  'Sistémico',
                                  'Racional',
                                  'Multiforme',
                                  'Innato'],
                 'correcta': 'B'},
                {'pregunta': 'Que una palabra represente algo concreto o '
                             'abstracto corresponde a que el lenguaje es:',
                 'alternativas': ['Sistémico',
                                  'Simbólico',
                                  'Convencional',
                                  'Universal',
                                  'Aprendido'],
                 'correcta': 'B'},
                {'pregunta': 'La función del lenguaje centrada en el emisor, '
                             'que manifiesta emociones, es la función:',
                 'alternativas': ['Apelativa',
                                  'Expresiva',
                                  'Referencial',
                                  'Fática',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el receptor, que busca '
                             'que actúe mediante órdenes, es la función:',
                 'alternativas': ['Expresiva',
                                  'Apelativa',
                                  'Metalingüística',
                                  'Poética',
                                  'Fática'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el contenido, propia de '
                             'textos informativos, es la función:',
                 'alternativas': ['Expresiva',
                                  'Referencial o representativa',
                                  'Fática',
                                  'Poética',
                                  'Apelativa'],
                 'correcta': 'B'},
                {'pregunta': 'La función que se usa cuando el código se '
                             'refiere al código mismo es la función:',
                 'alternativas': ['Referencial',
                                  'Metalingüística',
                                  'Fática',
                                  'Expresiva',
                                  'Poética'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el canal, que mantiene '
                             'el contacto entre interlocutores, es la '
                             'función:',
                 'alternativas': ['Poética',
                                  'Fática',
                                  'Referencial',
                                  'Apelativa',
                                  'Expresiva'],
                 'correcta': 'B'},
                {'pregunta': 'La función centrada en el mensaje, propia de '
                             'las obras literarias, es la función:',
                 'alternativas': ['Fática',
                                  'Poética',
                                  'Metalingüística',
                                  'Apelativa',
                                  'Referencial'],
                 'correcta': 'B'},
                {'pregunta': '«¡Cállate!» es un ejemplo de la función del '
                             'lenguaje:',
                 'alternativas': ['Expresiva',
                                  'Apelativa',
                                  'Poética',
                                  'Referencial',
                                  'Fática'],
                 'correcta': 'B'},
                {'pregunta': '«El precio del gas subió excesivamente» es un '
                             'ejemplo de la función:',
                 'alternativas': ['Expresiva',
                                  'Referencial',
                                  'Apelativa',
                                  'Poética',
                                  'Fática'],
                 'correcta': 'B'},
                {'pregunta': 'Según Saussure, el lenguaje tiene dos planos '
                             'interdependientes: lengua y:',
                 'alternativas': ['Habla',
                                  'Discurso',
                                  'Texto',
                                  'Gramática',
                                  'Sintaxis'],
                 'correcta': 'A'},
                {'pregunta': 'La lengua, según Saussure, es de carácter:',
                 'alternativas': ['Individual',
                                  'Social',
                                  'Biológico',
                                  'Instintivo',
                                  'Privado'],
                 'correcta': 'B'},
                {'pregunta': 'El habla, según Saussure, es de carácter:',
                 'alternativas': ['Social',
                                  'Individual',
                                  'Colectivo',
                                  'Universal',
                                  'Convencional exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El habla se realiza físicamente por medio de:',
                 'alternativas': ['Los signos escritos',
                                  'Los órganos de fonación',
                                  'La memoria colectiva',
                                  'Los diccionarios',
                                  'Las normas gramaticales'],
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
                {'titulo': '3.4 ELEMENTOS SEGMENTALES Y SUPRASEGMENTALES',
                 'items': ['Los elementos {segmentales} constituyen la '
                           'cadena hablada, definidos según criterios '
                           'articulatorios, acústicos y perceptivos.',
                           'Los elementos {suprasegmentales}, como la '
                           'entonación y el acento, se superponen a la '
                           'cadena de sonidos.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La disciplina que estudia los sonidos de la '
                           'lengua en su carácter distintivo de significados '
                           'es la {Fonología}.',
                           'La disciplina que estudia los mecanismos de '
                           'producción física de los sonidos del habla es la '
                           '{Fonética}.',
                           'El número de fonemas del español es {24}.',
                           'Los fonemas se representan entre {Barras / /}.',
                           'Los fonos se representan entre {Corchetes [ ]}.',
                           'Los fonemas son unidades de estudio de la '
                           '{Fonología}.',
                           'Los fonos son unidades de estudio de la '
                           '{Fonética}.',
                           'Un fonema se define como un segmento fonológico '
                           'que {No puede descomponerse en unidades '
                           'sucesivas menores}.',
                           'Los fonemas son sonidos {Ideales y mentales}.',
                           'Los fonos son la materialización de un fonema a '
                           'través {Del habla}.',
                           'Un par mínimo, como «beso» y «peso», sirve para '
                           'identificar {Fonemas distintos por el cambio de '
                           'significado}.',
                           'Los elementos constitutivos de un fonema, cuya '
                           'modificación causa contraste significativo, son '
                           'los {Rasgos distintivos}.',
                           'El fonema /p/ tiene, entre sus rasgos '
                           'distintivos, ser bilabial, oclusivo y {Sordo}.',
                           'El fonema /b/ tiene, entre sus rasgos '
                           'distintivos, ser bilabial, oclusivo y {Sonoro}.',
                           'Los elementos que constituyen la cadena hablada '
                           'y se estudian con criterios articulatorios son '
                           'los elementos {Segmentales}.',
                           'La entonación y el acento son ejemplos de '
                           'elementos {Suprasegmentales}.',
                           'El número de dígrafos en la escritura del '
                           'español es {5}.',
                           'En español, /b/ y /l/ son fonemas distintos '
                           'porque existen pares de palabras como {Bata y '
                           'lata}.',
                           'Los fonemas carecen de significación {Por sí '
                           'solos}.']}],
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
                 'alternativas': ['Fonética',
                                  'Fonología',
                                  'Morfología',
                                  'Sintaxis',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'La disciplina que estudia los mecanismos de '
                             'producción física de los sonidos del habla es '
                             'la:',
                 'alternativas': ['Fonología',
                                  'Fonética',
                                  'Semántica',
                                  'Morfología',
                                  'Pragmática'],
                 'correcta': 'B'},
                {'pregunta': 'El número de fonemas del español es:',
                 'alternativas': ['27', '24', '30', '20', '22'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas se representan entre:',
                 'alternativas': ['Corchetes [ ]',
                                  'Barras / /',
                                  'Comillas « »',
                                  'Paréntesis ( )',
                                  'Llaves { }'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonos se representan entre:',
                 'alternativas': ['Barras / /',
                                  'Corchetes [ ]',
                                  'Comillas « »',
                                  'Paréntesis ( )',
                                  'Llaves { }'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas son unidades de estudio de la:',
                 'alternativas': ['Fonética',
                                  'Fonología',
                                  'Sintaxis',
                                  'Morfología',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonos son unidades de estudio de la:',
                 'alternativas': ['Fonología',
                                  'Fonética',
                                  'Morfología',
                                  'Semántica',
                                  'Pragmática'],
                 'correcta': 'B'},
                {'pregunta': 'Un fonema se define como un segmento '
                             'fonológico que:',
                 'alternativas': ['Se puede descomponer en unidades menores',
                                  'No puede descomponerse en unidades '
                                  'sucesivas menores',
                                  'Carece de valor distintivo',
                                  'Es siempre visible por escrito',
                                  'No existe en la lengua oral'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas son sonidos:',
                 'alternativas': ['Reales y materializados',
                                  'Ideales y mentales',
                                  'Infinitos',
                                  'Sin valor distintivo',
                                  'Exclusivamente escritos'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonos son la materialización de un fonema '
                             'a través:',
                 'alternativas': ['De la escritura',
                                  'Del habla',
                                  'De la lectura silenciosa',
                                  'De la memoria',
                                  'De la gramática'],
                 'correcta': 'B'},
                {'pregunta': 'Un par mínimo, como «beso» y «peso», sirve '
                             'para identificar:',
                 'alternativas': ['Sinónimos',
                                  'Fonemas distintos por el cambio de '
                                  'significado',
                                  'Antónimos',
                                  'Homófonos idénticos',
                                  'Palabras sin relación'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos constitutivos de un fonema, cuya '
                             'modificación causa contraste significativo, '
                             'son los:',
                 'alternativas': ['Fonos',
                                  'Rasgos distintivos',
                                  'Grafemas',
                                  'Dígrafos',
                                  'Morfemas'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /p/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sonoro',
                                  'Sordo',
                                  'Nasal',
                                  'Vibrante',
                                  'Fricativo'],
                 'correcta': 'B'},
                {'pregunta': 'El fonema /b/ tiene, entre sus rasgos '
                             'distintivos, ser bilabial, oclusivo y:',
                 'alternativas': ['Sordo',
                                  'Sonoro',
                                  'Nasal',
                                  'Lateral',
                                  'Vibrante'],
                 'correcta': 'B'},
                {'pregunta': '«Peso» y «beso» se diferencian por el rasgo '
                             'distintivo de:',
                 'alternativas': ['El punto de articulación',
                                  'La sonoridad',
                                  'El modo nasal',
                                  'La vocal final',
                                  'La sílaba tónica'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos que constituyen la cadena '
                             'hablada y se estudian con criterios '
                             'articulatorios son los elementos:',
                 'alternativas': ['Suprasegmentales',
                                  'Segmentales',
                                  'Morfológicos',
                                  'Sintácticos',
                                  'Semánticos'],
                 'correcta': 'B'},
                {'pregunta': 'La entonación y el acento son ejemplos de '
                             'elementos:',
                 'alternativas': ['Segmentales',
                                  'Suprasegmentales',
                                  'Morfológicos',
                                  'Léxicos',
                                  'Sintácticos'],
                 'correcta': 'B'},
                {'pregunta': 'El número de dígrafos en la escritura del '
                             'español es:',
                 'alternativas': ['3', '5', '7', '2', '10'],
                 'correcta': 'B'},
                {'pregunta': 'En español, /b/ y /l/ son fonemas distintos '
                             'porque existen pares de palabras como:',
                 'alternativas': ['Casa y caza',
                                  'Bata y lata',
                                  'Vaca y baca',
                                  'Tubo y tuvo',
                                  'Ola y hola'],
                 'correcta': 'B'},
                {'pregunta': 'Los fonemas carecen de significación:',
                 'alternativas': ['Siempre en combinación',
                                  'Por sí solos',
                                  'En cualquier contexto',
                                  'Solo en el habla informal',
                                  'Solo en la escritura'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La sílaba se define como la unidad estructural '
                           'que actúa como principio {Organizador de la '
                           'lengua}.',
                           'La sílaba se agrupa en torno al segmento de '
                           'máxima {Sonoridad}.',
                           'En español, el núcleo silábico es siempre de '
                           'naturaleza {Vocálica}.',
                           'El constituyente silábico que es la cumbre o '
                           'centro de la sílaba es {El núcleo}.',
                           'El margen silábico anterior, de naturaleza '
                           'consonántica, se llama {Inicio o ataque}.',
                           'El margen silábico posterior, en posición '
                           'implosiva, se llama {Coda}.',
                           'La rima silábica está constituida por {El núcleo '
                           'y la coda}.',
                           'El silabeo consiste en {Pronunciar o escribir '
                           'separadas las sílabas de una palabra}.',
                           'Una consonante entre dos vocales siempre forma '
                           'sílaba con la vocal que {La sigue}.',
                           'En la palabra «pato», la separación silábica '
                           'correcta es {Pa-to}.',
                           'Los grupos tautosilábicos pr, br, tr, cr, pl, '
                           'bl, cl se caracterizan por ser {Inseparables}.',
                           'En la palabra «apretar», el grupo «pr» se '
                           'mantiene {Junto, formando sílaba con la vocal '
                           'siguiente}.',
                           'Cuando una sílaba termina en consonante y la '
                           'siguiente comienza en otra consonante, ambas se '
                           '{Separan entre ambas consonantes}.',
                           'En la palabra «asma», la separación silábica es '
                           '{As-ma}.',
                           'En la palabra «Cuba», la separación silábica '
                           'correcta es {Cu-ba}.',
                           'Un vocablo monosilábico, como «pan», tiene {Una '
                           'sola sílaba}.',
                           'La palabra «amor» se divide silábicamente como '
                           '{A-mor}.',
                           'El núcleo silábico, según el texto, resulta '
                           'determinante para asignar {El acento léxico}.',
                           'Un sonido o grupo de sonidos pronunciados en un '
                           'solo golpe de voz constituye {Una sílaba}.',
                           'Las vocales solas, por sí mismas, pueden '
                           'constituir {Sílabas}.']}],
  'cuadros': [{'titulo': '4.2 CONSTITUYENTES DE LA SÍLABA',
               'encabezados': ['Constituyente', 'Posición', 'Naturaleza'],
               'filas': [['{Núcleo}', 'Centro', '{Vocálica}'],
                         ['{Inicio}', 'Margen anterior', '{Consonántica}'],
                         ['{Coda}', 'Margen posterior', 'Consonántica']]}],
  'preguntas': [{'pregunta': 'La sílaba se define como la unidad estructural '
                             'que actúa como principio:',
                 'alternativas': ['Semántico',
                                  'Organizador de la lengua',
                                  'Morfológico exclusivo',
                                  'Sintáctico',
                                  'Pragmático'],
                 'correcta': 'B'},
                {'pregunta': 'La sílaba se agrupa en torno al segmento de '
                             'máxima:',
                 'alternativas': ['Consonancia',
                                  'Sonoridad',
                                  'Duración',
                                  'Intensidad tonal',
                                  'Frecuencia'],
                 'correcta': 'B'},
                {'pregunta': 'En español, el núcleo silábico es siempre de '
                             'naturaleza:',
                 'alternativas': ['Consonántica',
                                  'Vocálica',
                                  'Mixta obligatoria',
                                  'Nasal',
                                  'Fricativa'],
                 'correcta': 'B'},
                {'pregunta': 'El constituyente silábico que es la cumbre o '
                             'centro de la sílaba es:',
                 'alternativas': ['El inicio',
                                  'El núcleo',
                                  'La coda',
                                  'La rima',
                                  'El ataque'],
                 'correcta': 'B'},
                {'pregunta': 'El margen silábico anterior, de naturaleza '
                             'consonántica, se llama:',
                 'alternativas': ['Coda',
                                  'Inicio o ataque',
                                  'Núcleo',
                                  'Rima',
                                  'Centro'],
                 'correcta': 'B'},
                {'pregunta': 'El margen silábico posterior, en posición '
                             'implosiva, se llama:',
                 'alternativas': ['Inicio',
                                  'Coda',
                                  'Núcleo',
                                  'Ataque',
                                  'Centro'],
                 'correcta': 'B'},
                {'pregunta': 'La rima silábica está constituida por:',
                 'alternativas': ['Solo el inicio',
                                  'El núcleo y la coda',
                                  'Solo la coda',
                                  'El inicio y la coda',
                                  'Ningún elemento fijo'],
                 'correcta': 'B'},
                {'pregunta': 'El silabeo consiste en:',
                 'alternativas': ['Unir todas las sílabas',
                                  'Pronunciar o escribir separadas las '
                                  'sílabas de una palabra',
                                  'Eliminar las vocales',
                                  'Contar las consonantes',
                                  'Acentuar todas las palabras'],
                 'correcta': 'B'},
                {'pregunta': 'Una consonante entre dos vocales siempre forma '
                             'sílaba con la vocal que:',
                 'alternativas': ['La precede',
                                  'La sigue',
                                  'Es tónica',
                                  'Es átona',
                                  'Está más lejos'],
                 'correcta': 'B'},
                {'pregunta': 'En la palabra «pato», la separación silábica '
                             'correcta es:',
                 'alternativas': ['Pat-o',
                                  'Pa-to',
                                  'P-ato',
                                  'Pato completo',
                                  'Pa-t-o'],
                 'correcta': 'B'},
                {'pregunta': 'Los grupos tautosilábicos pr, br, tr, cr, pl, '
                             'bl, cl se caracterizan por ser:',
                 'alternativas': ['Separables siempre',
                                  'Inseparables',
                                  'Vocálicos',
                                  'Nulos en español',
                                  'Solo finales de palabra'],
                 'correcta': 'B'},
                {'pregunta': 'En la palabra «apretar», el grupo «pr» se '
                             'mantiene:',
                 'alternativas': ['Separado en dos sílabas',
                                  'Junto, formando sílaba con la vocal '
                                  'siguiente',
                                  'Eliminado',
                                  'Sustituido por otra letra',
                                  'Acentuado siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando una sílaba termina en consonante y la '
                             'siguiente comienza en otra consonante, ambas '
                             'se:',
                 'alternativas': ['Unen en una sola sílaba',
                                  'Separan entre ambas consonantes',
                                  'Eliminan',
                                  'Convierten en vocales',
                                  'Ignoran en el silabeo'],
                 'correcta': 'B'},
                {'pregunta': 'En la palabra «asma», la separación silábica '
                             'es:',
                 'alternativas': ['A-sma',
                                  'As-ma',
                                  'Asm-a',
                                  'A-s-ma',
                                  'Asma sin dividir'],
                 'correcta': 'B'},
                {'pregunta': 'En español NO existe frontera silábica en la '
                             'secuencia:',
                 'alternativas': ['Vocal-consonante',
                                  'Consonante-vocal',
                                  'Consonante-consonante',
                                  'Vocal-vocal',
                                  'Diptongo-consonante'],
                 'correcta': 'B'},
                {'pregunta': 'En la palabra «Cuba», la separación silábica '
                             'correcta es:',
                 'alternativas': ['Cub-a',
                                  'Cu-ba',
                                  'C-uba',
                                  'Cu-b-a',
                                  'Cuba sin dividir'],
                 'correcta': 'B'},
                {'pregunta': 'Un vocablo monosilábico, como «pan», tiene:',
                 'alternativas': ['Ninguna sílaba',
                                  'Una sola sílaba',
                                  'Dos sílabas',
                                  'Tres sílabas',
                                  'Cuatro sílabas o más'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «amor» se divide silábicamente '
                             'como:',
                 'alternativas': ['Am-or',
                                  'A-mor',
                                  'Amo-r',
                                  'A-m-or',
                                  'Amor sin dividir'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo silábico, según el texto, resulta '
                             'determinante para asignar:',
                 'alternativas': ['El género gramatical',
                                  'El acento léxico',
                                  'El número gramatical',
                                  'La categoría sintáctica',
                                  'El sujeto de la oración'],
                 'correcta': 'B'},
                {'pregunta': 'Un sonido o grupo de sonidos pronunciados en '
                             'un solo golpe de voz constituye:',
                 'alternativas': ['Un morfema',
                                  'Una sílaba',
                                  'Un fonema aislado',
                                  'Una oración',
                                  'Un sintagma'],
                 'correcta': 'B'},
                {'pregunta': 'Las vocales solas, por sí mismas, pueden '
                             'constituir:',
                 'alternativas': ['Solo consonantes',
                                  'Sílabas',
                                  'Solo diptongos',
                                  'Solo palabras compuestas',
                                  'Ningún elemento fónico'],
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
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El signo diacrítico que marca la acentuación de '
                           'una palabra por escrito se llama {Tilde}.',
                           'El acento que diferencia en la pronunciación una '
                           'sílaba, contrastándola con el resto, es el '
                           'acento {Prosódico}.',
                           'La función del acento que diferencia unidades '
                           'acentuadas de inacentuadas es la función '
                           '{Contrastiva}.',
                           'La función del acento que diferencia el '
                           'significado de palabras como «médico» y «medicó» '
                           'es la función {Distintiva}.',
                           'La función que permite percibir los grupos '
                           'acentuales del discurso es la función '
                           '{Culminativa}.',
                           'Las palabras monosilábicas, por regla general '
                           '{Nunca se acentúan gráficamente, salvo tilde '
                           'diacrítica}.',
                           'Las palabras agudas tienen la sílaba tónica en '
                           'la posición {Última}.',
                           'Las palabras agudas llevan tilde cuando terminan '
                           'en {N, s o vocal}.',
                           'Las palabras llanas o graves tienen la sílaba '
                           'tónica en la posición {Penúltima}.',
                           'Las palabras llanas llevan tilde cuando terminan '
                           'en {Consonante distinta de n, s o vocal}.',
                           'Las palabras esdrújulas tienen la sílaba tónica '
                           'en la posición {Antepenúltima}.',
                           'Las palabras esdrújulas, en cuanto a la tilde '
                           '{Todas llevan tilde}.',
                           'Las palabras sobresdrújulas tienen la sílaba '
                           'tónica {Anterior a la antepenúltima}.',
                           'Las palabras sobresdrújulas se caracterizan por '
                           'ser {Compuestas, y todas llevan tilde}.',
                           'La palabra «cuéntaselo» es un ejemplo de palabra '
                           '{Sobresdrújula}.',
                           'La palabra «césped» es un ejemplo de palabra '
                           '{Llana}.',
                           'La palabra «comité» lleva tilde porque es aguda '
                           'terminada en {Vocal}.',
                           'La palabra «botón» lleva tilde porque es aguda '
                           'terminada en {N}.',
                           'La palabra «jueves» no lleva tilde porque, '
                           'siendo llana, termina en {S}.',
                           'La palabra «música» es un ejemplo de palabra '
                           '{Esdrújula}.']}],
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
                          'Siempre lleva {tilde}']]}],
  'preguntas': [{'pregunta': 'El signo diacrítico que marca la acentuación '
                             'de una palabra por escrito se llama:',
                 'alternativas': ['Diéresis',
                                  'Tilde',
                                  'Cedilla',
                                  'Apóstrofo',
                                  'Guion'],
                 'correcta': 'B'},
                {'pregunta': 'El acento que diferencia en la pronunciación '
                             'una sílaba, contrastándola con el resto, es el '
                             'acento:',
                 'alternativas': ['Gráfico',
                                  'Prosódico',
                                  'Diacrítico',
                                  'Ortográfico exclusivo',
                                  'Fonológico puro'],
                 'correcta': 'B'},
                {'pregunta': 'La función del acento que diferencia unidades '
                             'acentuadas de inacentuadas es la función:',
                 'alternativas': ['Distintiva',
                                  'Contrastiva',
                                  'Culminativa',
                                  'Gráfica',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'La función del acento que diferencia el '
                             'significado de palabras como «médico» y '
                             '«medicó» es la función:',
                 'alternativas': ['Contrastiva',
                                  'Distintiva',
                                  'Culminativa',
                                  'Ortográfica',
                                  'Prosódica pura'],
                 'correcta': 'B'},
                {'pregunta': 'La función que permite percibir los grupos '
                             'acentuales del discurso es la función:',
                 'alternativas': ['Distintiva',
                                  'Culminativa',
                                  'Contrastiva',
                                  'Gráfica',
                                  'Semántica'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras monosilábicas, por regla general:',
                 'alternativas': ['Siempre llevan tilde',
                                  'Nunca se acentúan gráficamente, salvo '
                                  'tilde diacrítica',
                                  'Llevan tilde si son agudas',
                                  'Se acentúan según el contexto',
                                  'Llevan doble tilde'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras agudas tienen la sílaba tónica en '
                             'la posición:',
                 'alternativas': ['Primera',
                                  'Última',
                                  'Penúltima',
                                  'Antepenúltima',
                                  'Anterior a la antepenúltima'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras agudas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['Cualquier consonante',
                                  'N, s o vocal',
                                  'Solo consonantes dobles',
                                  'La letra y siempre',
                                  'Ninguna terminación específica'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras llanas o graves tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Última',
                                  'Penúltima',
                                  'Antepenúltima',
                                  'Primera',
                                  'Anterior a la antepenúltima'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras llanas llevan tilde cuando '
                             'terminan en:',
                 'alternativas': ['N, s o vocal',
                                  'Consonante distinta de n, s o vocal',
                                  'Solo vocal',
                                  'Solo la letra y',
                                  'Ninguna terminación'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras esdrújulas tienen la sílaba '
                             'tónica en la posición:',
                 'alternativas': ['Última',
                                  'Penúltima',
                                  'Antepenúltima',
                                  'Anterior a la antepenúltima',
                                  'Primera exclusivamente'],
                 'correcta': 'C'},
                {'pregunta': 'Las palabras esdrújulas, en cuanto a la tilde:',
                 'alternativas': ['Nunca llevan tilde',
                                  'Todas llevan tilde',
                                  'Solo algunas llevan tilde',
                                  'Llevan tilde solo si terminan en vocal',
                                  'Dependen del contexto'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras sobresdrújulas tienen la sílaba '
                             'tónica:',
                 'alternativas': ['En la última posición',
                                  'Anterior a la antepenúltima',
                                  'En la penúltima',
                                  'En la antepenúltima',
                                  'Sin posición fija'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras sobresdrújulas se caracterizan '
                             'por ser:',
                 'alternativas': ['Siempre simples',
                                  'Compuestas, y todas llevan tilde',
                                  'Monosilábicas',
                                  'Sin tilde nunca',
                                  'Solo verbos'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «cuéntaselo» es un ejemplo de '
                             'palabra:',
                 'alternativas': ['Aguda',
                                  'Llana',
                                  'Esdrújula',
                                  'Sobresdrújula',
                                  'Monosilábica'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «césped» es un ejemplo de palabra:',
                 'alternativas': ['Aguda',
                                  'Llana',
                                  'Esdrújula',
                                  'Sobresdrújula',
                                  'Monosilábica'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «comité» lleva tilde porque es '
                             'aguda terminada en:',
                 'alternativas': ['Consonante distinta de n o s',
                                  'N',
                                  'S',
                                  'Vocal',
                                  'Consonante doble'],
                 'correcta': 'D'},
                {'pregunta': 'La palabra «botón» lleva tilde porque es aguda '
                             'terminada en:',
                 'alternativas': ['Vocal',
                                  'N',
                                  'S',
                                  'Consonante doble',
                                  'La letra y'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «jueves» no lleva tilde porque, '
                             'siendo llana, termina en:',
                 'alternativas': ['Consonante distinta de n o s',
                                  'S',
                                  'Vocal abierta tónica',
                                  'Consonante doble',
                                  'La letra y'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «música» es un ejemplo de palabra:',
                 'alternativas': ['Aguda',
                                  'Llana',
                                  'Esdrújula',
                                  'Sobresdrújula',
                                  'Monosilábica'],
                 'correcta': 'C'}]},
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
                 'alternativas': ['Los verbos irregulares',
                                  'Los textos cortos informativos',
                                  'Los adjetivos calificativos',
                                  'Las preposiciones',
                                  'Los artículos'],
                 'correcta': 'B'},
                {'pregunta': 'El uso combinado de minúsculas y mayúsculas '
                             'dentro de una misma palabra debe:',
                 'alternativas': ['Fomentarse siempre',
                                  'Evitarse en la escritura normal',
                                  'Usarse en todo texto formal',
                                  'Aplicarse en cartas oficiales',
                                  'Prohibirse en las siglas'],
                 'correcta': 'B'},
                {'pregunta': 'Las siglas se escriben con mayúscula:',
                 'alternativas': ['Solo la primera letra',
                                  'Todas las letras que las componen',
                                  'Solo las vocales',
                                  'Solo las consonantes',
                                  'Ninguna letra en particular'],
                 'correcta': 'B'},
                {'pregunta': 'Las siglas, a diferencia de las abreviaturas, '
                             'se escriben:',
                 'alternativas': ['Con puntos',
                                  'Sin puntos',
                                  'Solo en cursiva',
                                  'Solo entre comillas',
                                  'Con guion final'],
                 'correcta': 'B'},
                {'pregunta': 'Las abreviaturas, a diferencia de las siglas, '
                             'se escriben:',
                 'alternativas': ['Sin puntos',
                                  'Con puntos',
                                  'Sin mayúsculas nunca',
                                  'Solo en números',
                                  'En cursiva obligatoria'],
                 'correcta': 'B'},
                {'pregunta': 'Los nombres latinos de especies, como «Homo '
                             'sapiens», se escriben con mayúscula inicial y:',
                 'alternativas': ['Entre comillas',
                                  'En cursiva',
                                  'Subrayados',
                                  'En negrita',
                                  'Entre paréntesis'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra «Dios» se escribe con mayúscula '
                             'cuando se usa:',
                 'alternativas': ['Con artículo, en sentido genérico',
                                  'Sin artículo, como nombre propio del ser '
                                  'supremo monoteísta',
                                  'Solo en textos religiosos católicos',
                                  'Nunca en español',
                                  'Solo en mayúscula total'],
                 'correcta': 'B'},
                {'pregunta': 'Si un dígrafo como «ch» o «ll» aparece al '
                             'inicio de una palabra con mayúscula, se '
                             'escribe en mayúscula:',
                 'alternativas': ['Ambas letras del dígrafo',
                                  'Solo la primera letra',
                                  'Ninguna letra',
                                  'Solo la segunda letra',
                                  'Todo en minúscula'],
                 'correcta': 'B'},
                {'pregunta': 'La mayúscula de las letras i y j, a diferencia '
                             'de su forma minúscula:',
                 'alternativas': ['Lleva doble punto',
                                  'Carece del punto sobrescrito',
                                  'Lleva tilde obligatoria',
                                  'Se escribe en cursiva siempre',
                                  'No existe en mayúscula'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno por el cual un nombre común '
                             'reemplaza completamente a un nombre propio se '
                             'llama:',
                 'alternativas': ['Personificación',
                                  'Antonomasia',
                                  'Metonimia',
                                  'Sinécdoque',
                                  'Hipérbole'],
                 'correcta': 'B'},
                {'pregunta': 'El fenómeno que atribuye rasgos humanos a '
                             'conceptos abstractos, como «la Muerte», se '
                             'llama:',
                 'alternativas': ['Antonomasia',
                                  'Personificación',
                                  'Metáfora exclusiva',
                                  'Comparación',
                                  'Ironía'],
                 'correcta': 'B'},
                {'pregunta': 'Se escribe con mayúscula la primera palabra de '
                             'un escrito y la que va después de:',
                 'alternativas': ['Una coma',
                                  'Un punto',
                                  'Un guion',
                                  'Unas comillas',
                                  'Un paréntesis'],
                 'correcta': 'B'},
                {'pregunta': 'La palabra que sigue a los puntos suspensivos, '
                             'cuando estos cierran un enunciado, se escribe '
                             'con:',
                 'alternativas': ['Minúscula siempre',
                                  'Mayúscula',
                                  'Cursiva obligatoria',
                                  'Comillas',
                                  'Negrita'],
                 'correcta': 'B'},
                {'pregunta': 'Si los puntos suspensivos NO cierran el '
                             'enunciado, la palabra siguiente se escribe '
                             'con:',
                 'alternativas': ['Mayúscula',
                                  'Minúscula',
                                  'Negrita obligatoria',
                                  'Cursiva',
                                  'Subrayado'],
                 'correcta': 'B'},
                {'pregunta': 'Después de dos puntos se escribe mayúscula '
                             'cuando anuncian el inicio de una unidad '
                             'independiente, como en:',
                 'alternativas': ['Una enumeración simple',
                                  'El saludo de una carta',
                                  'Una cita textual breve',
                                  'Un ejemplo cualquiera',
                                  'Una lista de compras'],
                 'correcta': 'B'},
                {'pregunta': 'Los documentos jurídicos que usan mayúscula '
                             'total suelen presentar palabras como:',
                 'alternativas': ['Considerando',
                                  'CERTIFICA',
                                  'Atentamente',
                                  'Estimado',
                                  'Saludos'],
                 'correcta': 'B'},
                {'pregunta': 'La mayúscula inicial marca y delimita, entre '
                             'otras cosas:',
                 'alternativas': ['Los verbos conjugados',
                                  'Los nombres propios',
                                  'Las preposiciones',
                                  'Los artículos indeterminados',
                                  'Las conjunciones'],
                 'correcta': 'B'},
                {'pregunta': '«El Salvador» usado para referirse a '
                             'Jesucristo es un ejemplo de:',
                 'alternativas': ['Personificación',
                                  'Antonomasia',
                                  'Metáfora pura',
                                  'Sinécdoque',
                                  'Ironía'],
                 'correcta': 'B'},
                {'pregunta': 'Las siglas «RAE» y «AVE» ejemplifican el uso '
                             'de mayúsculas para:',
                 'alternativas': ['Nombres propios de personas',
                                  'Formar e identificar siglas',
                                  'Números romanos',
                                  'Documentos jurídicos',
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
                                  'Comprensión',
                                  'Traducción',
                                  'Pronunciación exclusiva',
                                  'Eliminación'],
                 'correcta': 'B'},
                {'pregunta': 'Una función de los signos de puntuación es '
                             'indicar los límites de:',
                 'alternativas': ['Las palabras sueltas',
                                  'Las unidades discursivas',
                                  'Los fonemas',
                                  'Las sílabas',
                                  'Los morfemas'],
                 'correcta': 'B'},
                {'pregunta': 'La función que indica si un enunciado es '
                             'interrogativo o exclamativo es la función de:',
                 'alternativas': ['Límites discursivos',
                                  'Modalidad del enunciado',
                                  'Omisión',
                                  'Cohesión',
                                  'Referencia'],
                 'correcta': 'B'},
                {'pregunta': 'El punto se usa correctamente en:',
                 'alternativas': ['Los títulos de libros',
                                  'Las abreviaturas',
                                  'Las dedicatorias',
                                  'Los eslóganes',
                                  'Las direcciones electrónicas'],
                 'correcta': 'B'},
                {'pregunta': 'El punto se usa también en:',
                 'alternativas': ['Los títulos de obras de arte',
                                  'Fechas y horas',
                                  'Los nombres de autor en portadas',
                                  'Los eslóganes publicitarios',
                                  'Las direcciones web'],
                 'correcta': 'B'},
                {'pregunta': 'NO se escribe punto al final de:',
                 'alternativas': ['Una abreviatura',
                                  'Los títulos y subtítulos de libros',
                                  'Una fecha completa',
                                  'Una hora exacta',
                                  'Un párrafo normal'],
                 'correcta': 'B'},
                {'pregunta': 'Los nombres de autor en portadas, prólogos o '
                             'firmas de documentos se escriben:',
                 'alternativas': ['Con punto final',
                                  'Sin punto final',
                                  'Entre comillas obligatorias',
                                  'En mayúscula total',
                                  'Subrayados siempre'],
                 'correcta': 'B'},
                {'pregunta': 'Las dedicatorias, como «Para William», se '
                             'escriben:',
                 'alternativas': ['Con punto final',
                                  'Sin punto final',
                                  'Entre paréntesis',
                                  'En cursiva obligatoria',
                                  'Con doble punto'],
                 'correcta': 'B'},
                {'pregunta': 'Los eslóganes publicitarios, por regla '
                             'general, se escriben:',
                 'alternativas': ['Con punto final',
                                  'Sin punto final',
                                  'Solo en mayúsculas',
                                  'Entre comillas siempre',
                                  'Con coma final'],
                 'correcta': 'B'},
                {'pregunta': 'Las direcciones electrónicas, como '
                             'www.unsaac.edu.pe, se escriben:',
                 'alternativas': ['Con punto final obligatorio',
                                  'Sin punto final',
                                  'Entre corchetes',
                                  'Solo en mayúsculas',
                                  'Con guion final'],
                 'correcta': 'B'},
                {'pregunta': 'La coma que intercala información aclaratoria '
                             'dentro del enunciado es la coma:',
                 'alternativas': ['Vocativa',
                                  'Incidental',
                                  'Enumerativa',
                                  'Elíptica',
                                  'Hiperbática'],
                 'correcta': 'B'},
                {'pregunta': 'La coma que separa el nombre de la persona a '
                             'quien nos dirigimos es la coma:',
                 'alternativas': ['Incidental',
                                  'Vocativa',
                                  'Enumerativa',
                                  'Explicativa',
                                  'Distributiva'],
                 'correcta': 'B'},
                {'pregunta': 'En «Eduardo, no quiero que salgas tan tarde», '
                             'la coma usada es la coma:',
                 'alternativas': ['Incidental',
                                  'Vocativa',
                                  'Enumerativa',
                                  'Elíptica',
                                  'Hiperbática'],
                 'correcta': 'B'},
                {'pregunta': 'En «La mansión, abandonada, se convirtió en '
                             'refugio», la coma usada es la coma:',
                 'alternativas': ['Vocativa',
                                  'Incidental',
                                  'Enumerativa',
                                  'Distributiva',
                                  'Final'],
                 'correcta': 'B'},
                {'pregunta': 'El punto se usa en abreviaturas como:',
                 'alternativas': ['ONU', 'Sra.', 'DNI', 'AFP', 'RAE'],
                 'correcta': 'B'},
                {'pregunta': 'Las enumeraciones en forma de lista, como en '
                             'un examen de opción múltiple, se escriben:',
                 'alternativas': ['Con punto final en cada ítem '
                                  'obligatoriamente',
                                  'Sin punto final en cada ítem',
                                  'Solo con coma',
                                  'Solo con punto y coma',
                                  'En un solo párrafo continuo'],
                 'correcta': 'B'},
                {'pregunta': 'Los pies de imagen y cabeceras de cuadros, '
                             'cuando son breves, se escriben:',
                 'alternativas': ['Siempre con punto',
                                  'Generalmente sin punto',
                                  'Entre comillas obligatorias',
                                  'En mayúscula total',
                                  'Con dos puntos finales'],
                 'correcta': 'B'},
                {'pregunta': 'Los signos de puntuación señalan el carácter '
                             'especial de fragmentos como:',
                 'alternativas': ['Solo los títulos',
                                  'Citas e incisos',
                                  'Solo los números',
                                  'Solo las siglas',
                                  'Solo los nombres propios'],
                 'correcta': 'B'},
                {'pregunta': '«A quien madruga…» ejemplifica la función de '
                             'los signos de puntuación de indicar:',
                 'alternativas': ['Modalidad interrogativa',
                                  'La omisión de una parte del enunciado',
                                  'Límites discursivos',
                                  'Una cita textual',
                                  'Una fecha'],
                 'correcta': 'B'},
                {'pregunta': 'El punto se usa correctamente después de una '
                             'hora como:',
                 'alternativas': ['17.30',
                                  '17:30 con coma',
                                  'Diecisiete treinta escrito',
                                  '1730 sin separador',
                                  '17-30'],
                 'correcta': 'A'}]},
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
                 'alternativas': ['Solo acciones',
                                  'Seres y objetos de la realidad',
                                  'Solo cualidades',
                                  'Solo relaciones lógicas',
                                  'Solo cantidades'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el sustantivo '
                             'es una palabra:',
                 'alternativas': ['Invariable',
                                  'Variable, con morfemas de género y número',
                                  'Sin flexión',
                                  'Exclusivamente derivada',
                                  'Sin composición posible'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio sintáctico, el sustantivo '
                             'forma grupos nominales que pueden cumplir '
                             'función de:',
                 'alternativas': ['Solo adjetivo',
                                  'Sujeto, complemento directo, indirecto, '
                                  'entre otros',
                                  'Solo verbo',
                                  'Solo preposición',
                                  'Solo conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'En «El profesor viajará muy pronto», el '
                             'sustantivo «profesor» funciona como núcleo de:',
                 'alternativas': ['El complemento directo',
                                  'El sujeto',
                                  'El vocativo',
                                  'La aposición',
                                  'El complemento agente'],
                 'correcta': 'B'},
                {'pregunta': 'En «Señorita, aquí tiene su cuaderno», '
                             '«Señorita» funciona como núcleo del:',
                 'alternativas': ['Sujeto',
                                  'Vocativo',
                                  'Complemento directo',
                                  'Complemento indirecto',
                                  'Atributo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Ricardo Palma, el bibliotecario mendigo, '
                             'escribió Tradiciones peruanas», «el '
                             'bibliotecario mendigo» es núcleo de:',
                 'alternativas': ['El sujeto',
                                  'La aposición',
                                  'El vocativo',
                                  'El complemento circunstancial',
                                  'El atributo'],
                 'correcta': 'B'},
                {'pregunta': 'En «El cuento fue leído por el niño», «el '
                             'niño» funciona como núcleo del complemento:',
                 'alternativas': ['Directo',
                                  'Agente',
                                  'Indirecto',
                                  'Circunstancial',
                                  'De régimen'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que nombran a los seres '
                             'diferenciándolos de los demás de su especie '
                             'son los sustantivos:',
                 'alternativas': ['Comunes',
                                  'Propios',
                                  'Colectivos',
                                  'Abstractos',
                                  'Contables'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos propios, ortográficamente, se '
                             'escriben con:',
                 'alternativas': ['Minúscula inicial',
                                  'Mayúscula inicial',
                                  'Cursiva obligatoria',
                                  'Comillas siempre',
                                  'Guion inicial'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que nombran a todos los seres '
                             'de una clase son los sustantivos:',
                 'alternativas': ['Propios',
                                  'Comunes',
                                  'Colectivos exclusivos',
                                  'Contables',
                                  'Individuales exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que designan entidades que se '
                             'pueden contar son los sustantivos:',
                 'alternativas': ['No contables',
                                  'Contables',
                                  'Abstractos',
                                  'Colectivos',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que denotan magnitudes o '
                             'sustancias, como «un poco de café», son los '
                             'sustantivos:',
                 'alternativas': ['Contables',
                                  'No contables',
                                  'Individuales',
                                  'Colectivos',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que nombran seres percibidos '
                             'por los sentidos son los sustantivos:',
                 'alternativas': ['Abstractos',
                                  'Concretos',
                                  'Colectivos',
                                  'No contables',
                                  'Comunes exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que se conocen mediante un '
                             'proceso mental de abstracción son los '
                             'sustantivos:',
                 'alternativas': ['Concretos',
                                  'Abstractos',
                                  'Individuales',
                                  'Contables',
                                  'Propios exclusivos'],
                 'correcta': 'B'},
                {'pregunta': '«Hermosura», «paz» y «ambición» son ejemplos '
                             'de sustantivos:',
                 'alternativas': ['Concretos',
                                  'Abstractos',
                                  'Colectivos',
                                  'Contables',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': '«Cóndor», «árbol» y «lapicero» son ejemplos de '
                             'sustantivos:',
                 'alternativas': ['Abstractos',
                                  'Concretos',
                                  'Colectivos exclusivos',
                                  'No contables',
                                  'Propios'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos que nombran a un solo ser son '
                             'los sustantivos:',
                 'alternativas': ['Colectivos',
                                  'Individuales',
                                  'Abstractos',
                                  'No contables',
                                  'Propios exclusivos'],
                 'correcta': 'B'},
                {'pregunta': '«Arboleda», «enjambre» y «cardumen» son '
                             'ejemplos de sustantivos:',
                 'alternativas': ['Individuales',
                                  'Colectivos',
                                  'Abstractos',
                                  'Propios',
                                  'No contables exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los sustantivos colectivos, en número '
                             'singular, designan:',
                 'alternativas': ['Un solo ser',
                                  'Un conjunto de seres',
                                  'Una cualidad abstracta',
                                  'Una acción',
                                  'Una relación lógica'],
                 'correcta': 'B'},
                {'pregunta': 'En «Aquellos jóvenes parecen buenos '
                             'profesionales», «profesionales» funciona como '
                             'núcleo de:',
                 'alternativas': ['El sujeto',
                                  'El atributo',
                                  'El vocativo',
                                  'La aposición',
                                  'El complemento agente'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Nombrándolos con precisión',
                                  'Sin nombrarlos directamente',
                                  'Solo en plural',
                                  'Solo en femenino',
                                  'Con cualidades específicas'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre es descrito como una palabra:',
                 'alternativas': ['Connotativa',
                                  'No-connotativa',
                                  'Exclusivamente descriptiva',
                                  'Siempre concreta',
                                  'Invariable'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre es una palabra no descriptiva '
                             'porque:',
                 'alternativas': ['Señala cualidades del sustantivo',
                                  'Señala al ser sin conceptuarlo',
                                  'Nombra directamente al ser',
                                  'Tiene significado fijo siempre',
                                  'Solo se usa en plural'],
                 'correcta': 'B'},
                {'pregunta': 'Que el pronombre tenga significación ocasional '
                             'significa que:',
                 'alternativas': ['Siempre tiene el mismo significado',
                                  'Fuera de contexto carece de significado '
                                  'definido',
                                  'Nunca tiene significado',
                                  'Solo funciona en singular',
                                  'Es sinónimo de un sustantivo fijo'],
                 'correcta': 'B'},
                {'pregunta': 'Cuando el pronombre se carga de significado '
                             'dentro de un contexto, adquiere un valor:',
                 'alternativas': ['Descriptivo',
                                  'Referencial',
                                  'Morfológico exclusivo',
                                  'Fonológico',
                                  'Ortográfico'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el pronombre es '
                             'una palabra:',
                 'alternativas': ['Invariable',
                                  'Variable, con accidentes de género, '
                                  'número y persona',
                                  'Sin flexión alguna',
                                  'Exclusivamente masculina',
                                  'Solo singular'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio sintáctico, el pronombre '
                             'puede funcionar como sustantivo, adjetivo o:',
                 'alternativas': ['Preposición',
                                  'Adverbio',
                                  'Conjunción',
                                  'Interjección',
                                  'Artículo'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre que funciona como sujeto '
                             'se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Nominativo o recto',
                                  'Dativo',
                                  'Preposicional',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento directo se llama caso:',
                 'alternativas': ['Nominativo',
                                  'Acusativo',
                                  'Dativo',
                                  'Preposicional',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre que funciona como '
                             'complemento indirecto se llama caso:',
                 'alternativas': ['Acusativo',
                                  'Dativo',
                                  'Nominativo',
                                  'Preposicional',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'El caso del pronombre usado después de una '
                             'preposición se llama caso:',
                 'alternativas': ['Nominativo',
                                  'Preposicional',
                                  'Acusativo',
                                  'Dativo',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'En «Yo no lo sabía», el pronombre «yo» está en '
                             'caso:',
                 'alternativas': ['Acusativo',
                                  'Nominativo',
                                  'Dativo',
                                  'Preposicional',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «No me entienden», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Nominativo',
                                  'Acusativo',
                                  'Preposicional',
                                  'Vocativo',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'En «Me duelen las muelas», el pronombre «me» '
                             'funciona en caso:',
                 'alternativas': ['Acusativo',
                                  'Dativo',
                                  'Nominativo',
                                  'Preposicional',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'En «Confiaba en él», el pronombre «él» está en '
                             'caso:',
                 'alternativas': ['Nominativo',
                                  'Preposicional',
                                  'Acusativo',
                                  'Dativo',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'En «Ese se cayó anoche», el pronombre «ese» '
                             'ejemplifica que el pronombre es una palabra:',
                 'alternativas': ['Descriptiva',
                                  'No descriptiva',
                                  'Connotativa',
                                  'Fija en significado',
                                  'Exclusivamente adjetiva'],
                 'correcta': 'B'},
                {'pregunta': 'En «Esas niñas son más honestas que aquellas», '
                             'el primer pronombre «esas» funciona como:',
                 'alternativas': ['Sustantivo',
                                  'Adjetivo',
                                  'Adverbio',
                                  'Preposición',
                                  'Conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'En «Todos estudiaban aquí», el pronombre '
                             '«todos» funciona como:',
                 'alternativas': ['Adjetivo',
                                  'Sustantivo (núcleo del sujeto)',
                                  'Adverbio',
                                  'Preposición',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'Los pronombres «ella», «tú», «ellos» aislados, '
                             'sin contexto, tienen significado:',
                 'alternativas': ['Fijo y estable',
                                  'Vacío o indefinido',
                                  'Siempre concreto',
                                  'Exclusivamente plural',
                                  'Descriptivo detallado'],
                 'correcta': 'B'},
                {'pregunta': 'El pronombre, a diferencia del sustantivo, se '
                             'caracteriza principalmente por:',
                 'alternativas': ['Nombrar directamente al ser con sus '
                                  'cualidades',
                                  'Señalar al ser sin nombrarlo con '
                                  'precisión',
                                  'Tener siempre género femenino',
                                  'No poder funcionar como sujeto',
                                  'Ser siempre invariable'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Sustituye al sustantivo',
                                  'Califica al sustantivo',
                                  'Reemplaza al verbo',
                                  'Actúa como preposición',
                                  'Elimina el sustantivo'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el adjetivo es '
                             'una palabra:',
                 'alternativas': ['Invariable',
                                  'Variable, con género y número',
                                  'Sin flexión alguna',
                                  'Solo masculina',
                                  'Solo singular'],
                 'correcta': 'B'},
                {'pregunta': 'La función principal del adjetivo, según el '
                             'criterio sintáctico, es modificar '
                             'directamente:',
                 'alternativas': ['Al verbo',
                                  'Al sustantivo',
                                  'Al adverbio',
                                  'A la preposición',
                                  'A la conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'Además de modificar al sustantivo, el adjetivo '
                             'puede funcionar como núcleo del:',
                 'alternativas': ['Sujeto exclusivamente',
                                  'Predicativo o atributo',
                                  'Complemento directo únicamente',
                                  'Vocativo',
                                  'Complemento agente'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos que expresan cualidades o '
                             'estados del sustantivo son los adjetivos:',
                 'alternativas': ['Gentilicios',
                                  'Calificativos',
                                  'Determinativos exclusivos',
                                  'Posesivos',
                                  'Numerales'],
                 'correcta': 'B'},
                {'pregunta': 'El adjetivo que precisa de qué sustantivo se '
                             'trata y puede restringir su extensión es el '
                             'adjetivo:',
                 'alternativas': ['Explicativo',
                                  'Especificativo o restrictivo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Posesivo'],
                 'correcta': 'B'},
                {'pregunta': 'El adjetivo que aparece entre pausas y no '
                             'tiene carga excluyente es el adjetivo:',
                 'alternativas': ['Especificativo',
                                  'Explicativo o no restrictivo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Numeral'],
                 'correcta': 'B'},
                {'pregunta': 'El adjetivo que señala una cualidad propia del '
                             'sustantivo, con valor poético cuando va '
                             'antepuesto, es el:',
                 'alternativas': ['Especificativo',
                                  'Explicativo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Determinativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «blanca nieve», el adjetivo «blanca» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Especificativo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Explicativo',
                                  'Numeral'],
                 'correcta': 'B'},
                {'pregunta': 'En «Los jugadores, contentos con el resultado, '
                             'lo celebraron», el adjetivo «contentos» es:',
                 'alternativas': ['Especificativo',
                                  'Explicativo',
                                  'Epíteto',
                                  'Gentilicio',
                                  'Posesivo'],
                 'correcta': 'B'},
                {'pregunta': 'En «gatos negros», el adjetivo «negros» es un '
                             'ejemplo de adjetivo:',
                 'alternativas': ['Explicativo',
                                  'Especificativo',
                                  'Epíteto exclusivo',
                                  'Gentilicio',
                                  'Numeral'],
                 'correcta': 'B'},
                {'pregunta': 'Los adjetivos gentilicios califican al '
                             'sustantivo por su:',
                 'alternativas': ['Color',
                                  'Lugar de origen o procedencia',
                                  'Tamaño',
                                  'Forma',
                                  'Cantidad'],
                 'correcta': 'B'},
                {'pregunta': 'El sufijo «-eño/-eña» forma gentilicios como:',
                 'alternativas': ['Cordobés',
                                  'Limeña',
                                  'Italiana',
                                  'Bonaerense',
                                  'Chileno'],
                 'correcta': 'B'},
                {'pregunta': 'El sufijo «-ense» forma gentilicios como:',
                 'alternativas': ['Limeña',
                                  'Bonaerense',
                                  'Cordobés',
                                  'Italiana',
                                  'Habanera'],
                 'correcta': 'B'},
                {'pregunta': 'El sufijo «-és/-esa» forma gentilicios como:',
                 'alternativas': ['Limeña',
                                  'Cordobés',
                                  'Bonaerense',
                                  'Chileno',
                                  'Europeo'],
                 'correcta': 'B'},
                {'pregunta': 'En «El joven austriaco ganó un premio», el '
                             'adjetivo «austriaco» es un adjetivo:',
                 'alternativas': ['Calificativo especificativo',
                                  'Gentilicio',
                                  'Epíteto',
                                  'Explicativo',
                                  'Posesivo'],
                 'correcta': 'B'},
                {'pregunta': 'En «María llegó muy cansada», el adjetivo '
                             '«cansada» funciona como núcleo del:',
                 'alternativas': ['Sujeto',
                                  'Predicativo',
                                  'Complemento directo',
                                  'Vocativo',
                                  'Complemento indirecto'],
                 'correcta': 'B'},
                {'pregunta': 'En «La población está asustada», el adjetivo '
                             '«asustada» funciona como:',
                 'alternativas': ['Sujeto',
                                  'Atributo',
                                  'Complemento directo',
                                  'Vocativo',
                                  'Aposición'],
                 'correcta': 'B'},
                {'pregunta': 'El adjetivo epíteto, en posición pospuesta, '
                             'suele tener una intención:',
                 'alternativas': ['Poética exclusiva',
                                  'Coloquial',
                                  'Científica',
                                  'Legal',
                                  'Matemática'],
                 'correcta': 'B'},
                {'pregunta': 'En «lámpara portátil», el adjetivo «portátil» '
                             'cumple una función:',
                 'alternativas': ['Explicativa',
                                  'Especificativa',
                                  'Epíteto',
                                  'Gentilicia',
                                  'Numeral'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Fonológico',
                                  'Gramatical',
                                  'Morfológico exclusivo',
                                  'Pragmático',
                                  'Ninguno'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo, en su posición dentro de la '
                             'oración, siempre:',
                 'alternativas': ['Sigue al sustantivo',
                                  'Precede al sustantivo',
                                  'Se ubica al final de la oración',
                                  'Reemplaza al verbo',
                                  'Aparece solo en plural'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el artículo '
                             'concuerda con el sustantivo en:',
                 'alternativas': ['Solo tiempo verbal',
                                  'Género y número',
                                  'Solo persona gramatical',
                                  'Modo verbal',
                                  'Aspecto verbal'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo que hace referencia a un '
                             'sustantivo conocido por el hablante se llama '
                             'artículo:',
                 'alternativas': ['Indeterminado',
                                  'Determinado',
                                  'Neutro',
                                  'Posesivo',
                                  'Demostrativo'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo que hace referencia a seres no '
                             'conocidos se llama artículo:',
                 'alternativas': ['Determinado',
                                  'Indeterminado',
                                  'Neutro',
                                  'Definido',
                                  'Recto'],
                 'correcta': 'B'},
                {'pregunta': 'El artículo neutro del español es:',
                 'alternativas': ['El', 'La', 'Lo', 'Un', 'Una'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo neutro «lo» sirve para '
                             'sustantivar:',
                 'alternativas': ['Verbos',
                                  'Adjetivos',
                                  'Preposiciones',
                                  'Conjunciones',
                                  'Artículos'],
                 'correcta': 'B'},
                {'pregunta': 'En «Lo bueno supervive a través del tiempo», '
                             '«lo bueno» funciona como un sustantivo:',
                 'alternativas': ['Concreto',
                                  'Abstracto',
                                  'Propio',
                                  'Colectivo',
                                  'Contable'],
                 'correcta': 'B'},
                {'pregunta': 'El único artículo que se puede contraer es:',
                 'alternativas': ['La', 'Los', 'El', 'Las', 'Un'],
                 'correcta': 'C'},
                {'pregunta': 'El artículo «el» se contrae con las '
                             'preposiciones «a» y:',
                 'alternativas': ['Con', 'Para', 'De', 'Por', 'Sin'],
                 'correcta': 'C'},
                {'pregunta': 'La contracción de «a» más «el» da como '
                             'resultado:',
                 'alternativas': ['Del', 'Al', 'Ael', 'A el siempre', 'Aal'],
                 'correcta': 'B'},
                {'pregunta': 'La contracción de «de» más «el» da como '
                             'resultado:',
                 'alternativas': ['Al',
                                  'Del',
                                  'Dle',
                                  'De el siempre',
                                  'Dell'],
                 'correcta': 'B'},
                {'pregunta': 'Las contracciones del artículo se usan '
                             'solamente ante sustantivos:',
                 'alternativas': ['Propios siempre',
                                  'Comunes',
                                  'Colectivos exclusivos',
                                  'Abstractos',
                                  'Contables únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'Si el artículo forma parte de un topónimo, '
                             'como «El Salvador», la contracción:',
                 'alternativas': ['Es obligatoria',
                                  'No procede',
                                  'Es opcional siempre',
                                  'Depende del contexto oral',
                                  'Se aplica solo por escrito'],
                 'correcta': 'B'},
                {'pregunta': 'En «Viajaremos a El Cairo», la ausencia de '
                             'contracción se debe a que:',
                 'alternativas': ['Es un error ortográfico',
                                  'El artículo forma parte del topónimo',
                                  'El Cairo no es un lugar real',
                                  'La preposición no lo permite nunca',
                                  'Es una excepción sin explicación'],
                 'correcta': 'B'},
                {'pregunta': 'El adverbio, en cuanto a su morfología, es una '
                             'palabra:',
                 'alternativas': ['Variable en género y número',
                                  'Invariable',
                                  'Solo masculina',
                                  'Solo plural',
                                  'Con flexión verbal'],
                 'correcta': 'B'},
                {'pregunta': 'El adverbio puede modificar al verbo, al '
                             'adjetivo o:',
                 'alternativas': ['Al artículo',
                                  'A otro adverbio',
                                  'A la conjunción',
                                  'Al pronombre exclusivamente',
                                  'Al sustantivo directamente'],
                 'correcta': 'B'},
                {'pregunta': 'Los adverbios se clasifican, entre otras '
                             'categorías, en adverbios de lugar, tiempo y:',
                 'alternativas': ['Género',
                                  'Modo',
                                  'Número',
                                  'Persona',
                                  'Caso'],
                 'correcta': 'B'},
                {'pregunta': 'En «El ayer quedó en olvido», el artículo «el» '
                             'sustantiva a:',
                 'alternativas': ['Un verbo',
                                  'Un adverbio temporal',
                                  'Una preposición',
                                  'Un adjetivo',
                                  'Una conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'En «Un día te entregaré unos regalos», los '
                             'artículos usados son de tipo:',
                 'alternativas': ['Determinado',
                                  'Indeterminado',
                                  'Neutro',
                                  'Contraído',
                                  'Demostrativo'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Solo cantidad',
                                  'Existencia',
                                  'Solo lugar',
                                  'Solo posesión',
                                  'Solo cualidad'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, el verbo '
                             'presenta accidentes de número, persona, '
                             'tiempo, modo y:',
                 'alternativas': ['Género',
                                  'Aspecto',
                                  'Caso',
                                  'Grado',
                                  'Especie'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio sintáctico, el verbo '
                             'funciona como núcleo:',
                 'alternativas': ['Del sujeto',
                                  'Del predicado verbal',
                                  'Del vocativo',
                                  'De la aposición',
                                  'Del complemento agente exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que sirven de nexo entre el sujeto '
                             'y su atributo se llaman verbos:',
                 'alternativas': ['Transitivos',
                                  'Copulativos',
                                  'Reflexivos',
                                  'Recíprocos',
                                  'Impersonales'],
                 'correcta': 'B'},
                {'pregunta': 'Un ejemplo de verbo copulativo es:',
                 'alternativas': ['Correr',
                                  'Ser',
                                  'Escribir',
                                  'Saltar',
                                  'Comer'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que expresan por sí solos una idea '
                             'con sentido pleno se llaman verbos:',
                 'alternativas': ['Copulativos',
                                  'No copulativos o predicativos',
                                  'Impersonales exclusivos',
                                  'Semicopulativos únicamente',
                                  'Auxiliares'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que tienen complemento directo se '
                             'llaman verbos:',
                 'alternativas': ['Intransitivos',
                                  'Transitivos',
                                  'Impersonales',
                                  'Copulativos',
                                  'Recíprocos exclusivos'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que no tienen complemento directo '
                             'se llaman verbos:',
                 'alternativas': ['Transitivos',
                                  'Intransitivos',
                                  'Reflexivos exclusivos',
                                  'Copulativos',
                                  'Recíprocos'],
                 'correcta': 'B'},
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
                                  '«Mismo(a)»',
                                  '«Recíprocamente»',
                                  '«Entre sí»',
                                  '«Uno a otro»'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos que usan pronombres como énfasis '
                             'sin representar transitividad se llaman '
                             'verbos:',
                 'alternativas': ['Reflexivos',
                                  'Cuasireflexivos',
                                  'Recíprocos',
                                  'Transitivos',
                                  'Copulativos'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos cuasireflexivos, a diferencia de '
                             'los reflexivos, NO aceptan el refuerzo:',
                 'alternativas': ['«Mutuamente»',
                                  '«Mismo(a)»',
                                  '«Entre todos»',
                                  '«Recíprocamente»',
                                  'Ninguno de los anteriores'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos con sujeto plural que ejercen una '
                             'acción mutua entre ellos se llaman verbos:',
                 'alternativas': ['Reflexivos',
                                  'Recíprocos',
                                  'Cuasireflexivos',
                                  'Impersonales',
                                  'Transitivos'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter recíproco de un verbo se comprueba '
                             'con el refuerzo:',
                 'alternativas': ['«Mismo(a)»',
                                  '«Mutuamente» o «recíprocamente»',
                                  '«A sí mismo»',
                                  '«Solamente»',
                                  '«Exclusivamente»'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos cuyo sujeto se desconoce o no se '
                             'precisa se llaman verbos:',
                 'alternativas': ['Transitivos',
                                  'Impersonales',
                                  'Reflexivos',
                                  'Recíprocos',
                                  'Copulativos'],
                 'correcta': 'B'},
                {'pregunta': '«Llovió en Cusco» es un ejemplo de verbo '
                             'impersonal referido a:',
                 'alternativas': ['Un fenómeno social',
                                  'Un fenómeno de la naturaleza',
                                  'Una acción transitiva',
                                  'Un verbo copulativo',
                                  'Una acción recíproca'],
                 'correcta': 'B'},
                {'pregunta': '«Se traspasa local comercial» ejemplifica un '
                             'verbo impersonal con el signo:',
                 'alternativas': ['De pasiva refleja exclusiva',
                                  'De impersonalidad pronominal «se»',
                                  'De reciprocidad',
                                  'De reflexividad',
                                  'De copulación'],
                 'correcta': 'B'},
                {'pregunta': '«Dicen que te vas a casar» ejemplifica un '
                             'verbo impersonal porque:',
                 'alternativas': ['El sujeto es plural y conocido',
                                  'No se conoce o no se quiere dar a conocer '
                                  'el sujeto',
                                  'Es un verbo copulativo',
                                  'Expresa un fenómeno natural',
                                  'Tiene complemento directo explícito'],
                 'correcta': 'B'},
                {'pregunta': 'En «Yo me caigo», a diferencia de «yo caigo», '
                             'el pronombre «me»:',
                 'alternativas': ['Funciona como complemento directo',
                                  'Da solo énfasis, sin representar '
                                  'transitividad',
                                  'Indica reciprocidad',
                                  'Es un artículo neutro',
                                  'Sustituye al sujeto'],
                 'correcta': 'B'},
                {'pregunta': 'Los verbos «ser», «estar» y «parecer» '
                             'pertenecen a la clase de verbos:',
                 'alternativas': ['Transitivos',
                                  'Copulativos',
                                  'Recíprocos',
                                  'Impersonales',
                                  'Cuasireflexivos'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Fijo y absoluto',
                                  'Contextual',
                                  'Fonológico exclusivo',
                                  'Morfológico puro',
                                  'Inexistente'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio morfológico, la preposición '
                             'se caracteriza por:',
                 'alternativas': ['Presentar variaciones de género y número',
                                  'No sufrir variaciones formales',
                                  'Cambiar según el sujeto',
                                  'Tener flexión verbal',
                                  'Concordar en persona'],
                 'correcta': 'B'},
                {'pregunta': 'Según el criterio sintáctico, la preposición '
                             'funciona como:',
                 'alternativas': ['Núcleo del predicado',
                                  'Conectivo o nexo subordinante',
                                  'Sujeto de la oración',
                                  'Núcleo del sujeto',
                                  'Modificador indirecto exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'En «La casa de Patricia fue construida por los '
                             'albañiles», la preposición que encabeza al '
                             'agente es:',
                 'alternativas': ['De', 'Por', 'Para', 'Con', 'En'],
                 'correcta': 'B'},
                {'pregunta': 'Las preposiciones que encabezan al agente en '
                             'voz pasiva son:',
                 'alternativas': ['A y ante',
                                  'Por y de',
                                  'Con y sin',
                                  'Para y desde',
                                  'Entre y hacia'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «ante» significa:',
                 'alternativas': ['Después de',
                                  'Delante de o en presencia de',
                                  'Debajo de',
                                  'Junto a',
                                  'Lejos de'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «bajo» puede indicar situación '
                             'inferior o:',
                 'alternativas': ['Finalidad',
                                  'Subordinación',
                                  'Origen',
                                  'Compañía',
                                  'Tiempo exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Con mucho estudio puedes conseguir la '
                             'beca», la preposición «con» indica:',
                 'alternativas': ['Compañía',
                                  'Medio para conseguir algo',
                                  'Contenido',
                                  'Oposición',
                                  'Tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «contra» indica principalmente:',
                 'alternativas': ['Finalidad',
                                  'Oposición o ubicación',
                                  'Posesión',
                                  'Procedencia',
                                  'Compañía'],
                 'correcta': 'B'},
                {'pregunta': 'En «El departamento de mi amiga», la '
                             'preposición «de» indica:',
                 'alternativas': ['Origen',
                                  'Posesión o pertenencia',
                                  'Material',
                                  'Tema',
                                  'Tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Yo soy de Apurímac», la preposición «de» '
                             'indica:',
                 'alternativas': ['Posesión',
                                  'Origen o procedencia',
                                  'Material',
                                  'Tema o asunto',
                                  'Tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «desde» indica principio de '
                             'tiempo o de:',
                 'alternativas': ['Modo',
                                  'Lugar',
                                  'Finalidad',
                                  'Compañía',
                                  'Oposición'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «hacia» indica dirección o:',
                 'alternativas': ['Posesión',
                                  'Una tendencia',
                                  'Material',
                                  'Oposición',
                                  'Compañía'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «hasta» puede indicar término '
                             'de lugar, acción o:',
                 'alternativas': ['Posesión',
                                  'Tiempo',
                                  'Material',
                                  'Compañía',
                                  'Oposición'],
                 'correcta': 'B'},
                {'pregunta': 'La preposición «para» puede indicar finalidad, '
                             'tiempo o:',
                 'alternativas': ['Posesión exclusiva',
                                  'Dirección',
                                  'Material',
                                  'Oposición',
                                  'Compañía'],
                 'correcta': 'B'},
                {'pregunta': 'En el sujeto, la preposición encabeza al:',
                 'alternativas': ['Núcleo del sujeto',
                                  'Modificador indirecto',
                                  'Complemento directo',
                                  'Vocativo',
                                  'Predicado nominal'],
                 'correcta': 'B'},
                {'pregunta': '«So» y «cabe» son ejemplos de preposiciones:',
                 'alternativas': ['Modernas de uso frecuente',
                                  'Arcaicas',
                                  'Compuestas',
                                  'Neológicas',
                                  'Extranjeras'],
                 'correcta': 'B'},
                {'pregunta': 'En «Estamos pasando bajo el puente», la '
                             'preposición «bajo» indica:',
                 'alternativas': ['Subordinación',
                                  'Situación inferior',
                                  'Finalidad',
                                  'Tiempo',
                                  'Compañía'],
                 'correcta': 'B'},
                {'pregunta': 'En «Dame un té con leche», la preposición '
                             '«con» indica:',
                 'alternativas': ['Compañía de personas',
                                  'Contenido o unión de cosas',
                                  'Oposición',
                                  'Medio',
                                  'Tiempo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Este informe es para mi jefe», la '
                             'preposición «para» indica:',
                 'alternativas': ['Tiempo',
                                  'Finalidad',
                                  'Dirección',
                                  'Origen',
                                  'Compañía'],
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
                 'alternativas': ['Significado',
                                  'Orden o disposición',
                                  'Sonido',
                                  'Escritura',
                                  'Comunicación'],
                 'correcta': 'B'},
                {'pregunta': 'La sintaxis, como disciplina lingüística, '
                             'estudia las relaciones entre los elementos de '
                             'una frase y:',
                 'alternativas': ['Solo su pronunciación',
                                  'Las funciones que desempeña cada palabra',
                                  'Solo su ortografía',
                                  'Solo su significado aislado',
                                  'Solo su origen etimológico'],
                 'correcta': 'B'},
                {'pregunta': 'La unidad básica de la sintaxis es:',
                 'alternativas': ['El fonema',
                                  'El sintagma',
                                  'El morfema',
                                  'La sílaba',
                                  'El grafema'],
                 'correcta': 'B'},
                {'pregunta': 'El sintagma se define como una unidad formada '
                             'por palabras dotadas de sentido y valor:',
                 'alternativas': ['Fonológico',
                                  'Funcional',
                                  'Ortográfico',
                                  'Morfológico exclusivo',
                                  'Semántico aislado'],
                 'correcta': 'B'},
                {'pregunta': 'El sintagma nominal también se conoce como:',
                 'alternativas': ['Sintagma verbal',
                                  'Frase nominal o grupo nominal',
                                  'Predicado nominal exclusivo',
                                  'Complemento circunstancial',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'El núcleo del sintagma nominal siempre es:',
                 'alternativas': ['Un verbo',
                                  'Un sustantivo o palabra sustantivada',
                                  'Un adverbio',
                                  'Una preposición',
                                  'Una conjunción'],
                 'correcta': 'B'},
                {'pregunta': 'Los modificadores del sintagma nominal '
                             'dependen de:',
                 'alternativas': ['El verbo principal',
                                  'El núcleo',
                                  'El sujeto de otra oración',
                                  'El predicado verbal',
                                  'El complemento circunstancial'],
                 'correcta': 'B'},
                {'pregunta': 'El modificador que se une al núcleo del SN sin '
                             'ningún enlace se llama:',
                 'alternativas': ['Modificador indirecto',
                                  'Modificador directo',
                                  'Aposición explicativa',
                                  'Aposición especificativa',
                                  'Complemento agente'],
                 'correcta': 'B'},
                {'pregunta': 'Las palabras que funcionan típicamente como '
                             'modificador directo son:',
                 'alternativas': ['Los verbos',
                                  'Los artículos y adjetivos',
                                  'Las preposiciones',
                                  'Las conjunciones',
                                  'Los adverbios'],
                 'correcta': 'B'},
                {'pregunta': 'El modificador que se une al núcleo mediante '
                             'preposiciones se llama:',
                 'alternativas': ['Modificador directo',
                                  'Modificador indirecto',
                                  'Aposición',
                                  'Núcleo secundario',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'El modificador del SN que tiene el mismo valor '
                             'que el núcleo y puede conmutarse con él es:',
                 'alternativas': ['El modificador directo',
                                  'La aposición',
                                  'El modificador indirecto',
                                  'El artículo',
                                  'El adjetivo calificativo'],
                 'correcta': 'B'},
                {'pregunta': 'La aposición que se separa por comas y es '
                             'sinónima del núcleo se llama aposición:',
                 'alternativas': ['Especificativa',
                                  'Explicativa',
                                  'Directa',
                                  'Indirecta',
                                  'Neutra'],
                 'correcta': 'B'},
                {'pregunta': 'En «Pachacútec, el constructor de Machu '
                             'Picchu, fue el noveno Inca», el segmento entre '
                             'comas es una aposición:',
                 'alternativas': ['Especificativa',
                                  'Explicativa',
                                  'Indirecta',
                                  'Directa',
                                  'Neutra'],
                 'correcta': 'B'},
                {'pregunta': 'La aposición que singulariza al nombre y no va '
                             'entre comas se llama aposición:',
                 'alternativas': ['Explicativa',
                                  'Especificativa',
                                  'Directa',
                                  'Neutra',
                                  'Indirecta'],
                 'correcta': 'B'},
                {'pregunta': 'En «El río Vilcanota recorre el Valle '
                             'Sagrado», «Vilcanota» funciona como una '
                             'aposición:',
                 'alternativas': ['Explicativa',
                                  'Especificativa',
                                  'Indirecta',
                                  'Neutra',
                                  'Directa'],
                 'correcta': 'B'},
                {'pregunta': 'En «El estudiante proactivo logró su '
                             'propósito», «proactivo» funciona como:',
                 'alternativas': ['Modificador indirecto',
                                  'Modificador directo',
                                  'Aposición',
                                  'Núcleo del SN',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Los estudiantes con empeño logran todo», '
                             '«con empeño» funciona como:',
                 'alternativas': ['Modificador directo',
                                  'Modificador indirecto',
                                  'Aposición explicativa',
                                  'Núcleo',
                                  'Vocativo'],
                 'correcta': 'B'},
                {'pregunta': 'En «Cusco, capital histórica del Perú, es una '
                             'ciudad milenaria», «capital histórica del '
                             'Perú» es una aposición:',
                 'alternativas': ['Especificativa',
                                  'Explicativa',
                                  'Directa',
                                  'Indirecta',
                                  'Neutra'],
                 'correcta': 'B'},
                {'pregunta': 'Ortográficamente, la aposición explicativa '
                             'siempre aparece:',
                 'alternativas': ['Sin ninguna puntuación',
                                  'Separada entre comas',
                                  'Entre paréntesis obligatorios',
                                  'Subrayada',
                                  'En mayúscula total'],
                 'correcta': 'B'},
                {'pregunta': 'Semánticamente, los elementos de una aposición '
                             'explicativa son:',
                 'alternativas': ['Antónimos',
                                  'Sinónimos',
                                  'Homófonos',
                                  'Parónimos',
                                  'Sin relación semántica'],
                 'correcta': 'B'}]},
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
                                  'Palabra',
                                  'Discurso'],
                 'correcta': 'B'},
                {'pregunta': 'El texto se define como una unidad de '
                             'contenido y forma que tiene como base:',
                 'alternativas': ['La oración simple',
                                  'El párrafo',
                                  'La sílaba',
                                  'El fonema',
                                  'El morfema'],
                 'correcta': 'B'},
                {'pregunta': 'El texto tiene un carácter comunicativo, un '
                             'carácter pragmático y un carácter:',
                 'alternativas': ['Musical',
                                  'Estructurado',
                                  'Aleatorio',
                                  'Fonológico exclusivo',
                                  'Improvisado'],
                 'correcta': 'B'},
                {'pregunta': 'El texto se define como la secuencia '
                             'lingüística con sentido:',
                 'alternativas': ['Ambiguo',
                                  'Pleno',
                                  'Nulo',
                                  'Fragmentado',
                                  'Exclusivamente literal'],
                 'correcta': 'B'},
                {'pregunta': 'La tesis o planteamiento central que el autor '
                             'desarrolla en un texto se llama:',
                 'alternativas': ['Idea secundaria',
                                  'Idea principal',
                                  'Título',
                                  'Tema general',
                                  'Subtítulo'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas que sirven de argumento a la idea '
                             'principal se llaman:',
                 'alternativas': ['Ideas principales',
                                  'Ideas secundarias',
                                  'Títulos',
                                  'Temas',
                                  'Conclusiones exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Todo aquello de lo que se habla en un texto, '
                             'el asunto general, se llama:',
                 'alternativas': ['Idea principal',
                                  'Tema',
                                  'Título',
                                  'Idea secundaria',
                                  'Argumento'],
                 'correcta': 'B'},
                {'pregunta': 'La frase breve que sintetiza la idea central '
                             'de un texto se llama:',
                 'alternativas': ['Tema',
                                  'Título',
                                  'Idea secundaria',
                                  'Párrafo',
                                  'Argumento'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta una sucesión de acciones '
                             'en el tiempo se llama texto:',
                 'alternativas': ['Descriptivo',
                                  'Narrativo',
                                  'Argumentativo',
                                  'Expositivo puro',
                                  'Instructivo'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad del texto narrativo es:',
                 'alternativas': ['Persuadir al lector',
                                  'Contar acontecimientos reales o ficticios',
                                  'Describir un objeto',
                                  'Dar instrucciones',
                                  'Definir conceptos'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que representa con palabras un '
                             'objeto, paisaje o persona se llama texto:',
                 'alternativas': ['Narrativo',
                                  'Descriptivo',
                                  'Argumentativo',
                                  'Expositivo',
                                  'Dialógico'],
                 'correcta': 'B'},
                {'pregunta': 'El texto descriptivo es comparado en el texto '
                             'con:',
                 'alternativas': ['Una fórmula matemática',
                                  'Una pintura hecha con palabras',
                                  'Un discurso político',
                                  'Una noticia breve',
                                  'Un poema exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'El texto que presenta una tesis con argumentos '
                             'para persuadir al lector se llama texto:',
                 'alternativas': ['Narrativo',
                                  'Argumentativo',
                                  'Descriptivo',
                                  'Instructivo',
                                  'Dialógico'],
                 'correcta': 'B'},
                {'pregunta': 'La finalidad principal del texto argumentativo '
                             'es:',
                 'alternativas': ['Narrar hechos',
                                  'Persuadir al lector sobre un punto de '
                                  'vista',
                                  'Describir un paisaje',
                                  'Dar una receta',
                                  'Enumerar datos'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter comunicativo del texto se '
                             'relaciona con:',
                 'alternativas': ['Su función social',
                                  'Su extensión física',
                                  'Su tipografía',
                                  'Su color',
                                  'Su formato de impresión'],
                 'correcta': 'B'},
                {'pregunta': 'El carácter pragmático del texto implica que '
                             'se produce con:',
                 'alternativas': ['Ninguna intención',
                                  'Una intención y en una situación concreta',
                                  'Solo fines estéticos',
                                  'Solo fines comerciales',
                                  'Total aleatoriedad'],
                 'correcta': 'B'},
                {'pregunta': 'Descubrir la idea de mayor jerarquía en un '
                             'texto es fundamental para lograr:',
                 'alternativas': ['Solo memorizar el texto',
                                  'Una comprensión cabal del texto',
                                  'Ignorar las ideas secundarias',
                                  'Reducir el vocabulario',
                                  'Evitar el análisis'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas secundarias cumplen el papel de '
                             'fundamentar, explicar y:',
                 'alternativas': ['Contradecir la idea principal',
                                  'Presentar con diversos recursos la idea '
                                  'principal',
                                  'Eliminar la idea principal',
                                  'Sustituir el título',
                                  'Reemplazar el tema'],
                 'correcta': 'B'},
                {'pregunta': 'El tema de un texto puede ser un aspecto '
                             'general como:',
                 'alternativas': ['Solo un nombre propio',
                                  'El cáncer, la violencia o la política',
                                  'Solo una fecha',
                                  'Solo un número',
                                  'Solo un lugar geográfico'],
                 'correcta': 'B'},
                {'pregunta': 'El texto, según el concepto general, es un '
                             'acto de habla o una serie de actos '
                             'lingüísticos realizados en:',
                 'alternativas': ['Cualquier situación sin contexto',
                                  'Una situación comunicativa determinada',
                                  'Ausencia total de intención',
                                  'Un vacío comunicativo',
                                  'Un contexto irrelevante'],
                 'correcta': 'B'}]},
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
                 'alternativas': ['Sonido contrario',
                                  'Equivalencia o afinidad de significados',
                                  'Escritura similar',
                                  'Ausencia de significado',
                                  'Oposición de ideas'],
                 'correcta': 'B'},
                {'pregunta': 'La sinonimia es la semejanza de significados '
                             'entre términos comprendidos en un mismo:',
                 'alternativas': ['Campo fonológico',
                                  'Campo semántico',
                                  'Campo morfológico exclusivo',
                                  'Campo sintáctico exclusivo',
                                  'Campo gráfico'],
                 'correcta': 'B'},
                {'pregunta': 'Los sinónimos, además de significados '
                             'parecidos, pertenecen a la misma:',
                 'alternativas': ['Categoría fonológica',
                                  'Clase gramatical',
                                  'Categoría ortográfica',
                                  'Familia léxica exclusiva',
                                  'Raíz etimológica exclusiva'],
                 'correcta': 'B'},
                {'pregunta': 'Los sinónimos que mantienen el mismo '
                             'significado sin importar el contexto se llaman '
                             'sinónimos:',
                 'alternativas': ['Relativos',
                                  'Absolutos',
                                  'Parciales',
                                  'Contextuales',
                                  'Indirectos'],
                 'correcta': 'B'},
                {'pregunta': '«Casa» y «vivienda» son un ejemplo de '
                             'sinónimos:',
                 'alternativas': ['Relativos',
                                  'Absolutos',
                                  'Parciales',
                                  'Antónimos',
                                  'Parónimos'],
                 'correcta': 'B'},
                {'pregunta': 'Los sinónimos que cambian de sentido según el '
                             'contexto se llaman sinónimos:',
                 'alternativas': ['Absolutos',
                                  'Relativos o indirectos',
                                  'Directos',
                                  'Parciales fijos',
                                  'Universales'],
                 'correcta': 'B'},
                {'pregunta': 'Los antónimos se definen como palabras de la '
                             'misma categoría gramatical que expresan '
                             'significados:',
                 'alternativas': ['Semejantes',
                                  'Contrarios',
                                  'Idénticos',
                                  'Ambiguos',
                                  'Neutros'],
                 'correcta': 'B'},
                {'pregunta': 'Los antónimos que expresan ideas total y '
                             'exactamente contrarias se llaman antónimos:',
                 'alternativas': ['Relativos',
                                  'Absolutos',
                                  'Parciales',
                                  'Semánticos exclusivos',
                                  'Indirectos'],
                 'correcta': 'B'},
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
                                  'Directos',
                                  'Totales',
                                  'Puros'],
                 'correcta': 'B'},
                {'pregunta': '«Cima» y «planicie» son un ejemplo de '
                             'antónimos:',
                 'alternativas': ['Absolutos',
                                  'Relativos',
                                  'Sinónimos',
                                  'Parónimos',
                                  'Homófonos'],
                 'correcta': 'B'},
                {'pregunta': 'La paronimia ocurre cuando dos palabras se '
                             'asemejan en:',
                 'alternativas': ['Su significado',
                                  'Su sonido, pero se escriben diferente',
                                  'Su categoría gramatical exclusivamente',
                                  'Su origen etimológico exclusivamente',
                                  'Su extensión'],
                 'correcta': 'B'},
                {'pregunta': 'Los parónimos, a diferencia de los sinónimos, '
                             'tienen significados:',
                 'alternativas': ['Iguales',
                                  'Distintos',
                                  'Idénticos siempre',
                                  'Opuestos exactamente',
                                  'Ambiguos'],
                 'correcta': 'B'},
                {'pregunta': 'Los parónimos diferenciados por el acento, '
                             'como «ánimo», «animo» y «animó», son parónimos '
                             'por:',
                 'alternativas': ['La escritura',
                                  'El acento',
                                  'El significado',
                                  'La categoría gramatical',
                                  'El origen'],
                 'correcta': 'B'},
                {'pregunta': '«Actitud» (postura) y «aptitud» (idoneidad) '
                             'son un ejemplo de parónimos por:',
                 'alternativas': ['El acento',
                                  'La escritura',
                                  'El sonido idéntico',
                                  'El significado igual',
                                  'La sinonimia'],
                 'correcta': 'B'},
                {'pregunta': '«Absolver» (perdonar) y «absorber» (beber) son '
                             'un ejemplo de parónimos por:',
                 'alternativas': ['El acento',
                                  'La escritura',
                                  'La sinonimia',
                                  'La antonimia',
                                  'El campo semántico'],
                 'correcta': 'B'},
                {'pregunta': 'En «El sacerdote habló de la oración» y «El '
                             'alumno escribió una oración», la palabra '
                             '«oración» ejemplifica:',
                 'alternativas': ['Un antónimo absoluto',
                                  'Un sinónimo relativo',
                                  'Un parónimo por el acento',
                                  'Un antónimo relativo',
                                  'Un sinónimo absoluto'],
                 'correcta': 'B'},
                {'pregunta': '«Rapidez» y «lentitud» son un ejemplo de:',
                 'alternativas': ['Sinónimos absolutos',
                                  'Antónimos',
                                  'Parónimos por el acento',
                                  'Sinónimos relativos',
                                  'Homófonos'],
                 'correcta': 'B'},
                {'pregunta': 'Alcalde y alcaide son un ejemplo de:',
                 'alternativas': ['Sinónimos absolutos',
                                  'Parónimos por la escritura',
                                  'Antónimos absolutos',
                                  'Sinónimos relativos',
                                  'Antónimos relativos'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres relaciones semánticas estudiadas son '
                             'sinonimia, antonimia y:',
                 'alternativas': ['Morfología',
                                  'Paronimia',
                                  'Sintaxis',
                                  'Fonética',
                                  'Ortografía'],
                 'correcta': 'B'}]}]
