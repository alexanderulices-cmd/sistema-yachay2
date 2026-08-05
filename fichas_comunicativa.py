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
                 'correcta': 'C'}]}]
