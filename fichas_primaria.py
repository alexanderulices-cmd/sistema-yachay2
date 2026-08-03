# ================================================================
# FICHAS DE COMUNICACIÓN — PRIMARIA
# I.E.P. ALTERNATIVO YACHAY
# ================================================================
"""Genera fichas de comprensión lectora listas para imprimir.

Las 20 lecturas son fábulas de Esopo (dominio público) reescritas con
vocabulario de 1° y 2° de primaria: oraciones cortas, tiempo pasado
simple y no más de 130 palabras, para que un niño que recién consolida
la lectura pueda terminar el texto sin frustrarse.

Cada ficha trae tres preguntas que siguen los niveles de comprensión
del CNEB: literal (obtiene información), inferencial (infiere e
interpreta) y crítica (reflexiona y evalúa).

Integración en sistema_web.py:
    from fichas_primaria import tab_fichas_primaria
"""

import io
from datetime import datetime

import streamlit as st

ENCABEZADO_L1 = "I.E.P. YACHAY  ·  ACADEMIA YACHAY"
ENCABEZADO_L2 = "PIONEROS EN LA EDUCACIÓN DE CALIDAD"
PIE_LEGAL = ("Derechos reservados — I.E.P. ALTERNATIVO YACHAY · "
             "Documento generado por SISTEMA YACHAY PRO")


# ================================================================
# 1. LECTURAS
# ================================================================
# grado: 1 = apto desde 1°, 2 = mejor desde 2° (texto algo más largo)

LECTURAS = [
    {
        "titulo": "La liebre y la tortuga", "grado": 1,
        "texto": (
            "La liebre corría muy rápido y se burlaba de la tortuga.\n"
            "—Eres tan lenta que nunca ganarías una carrera —le dijo.\n"
            "La tortuga la miró con calma y respondió:\n"
            "—Corramos y veamos quién llega primero.\n"
            "Empezó la carrera. La liebre salió disparada y pronto dejó "
            "atrás a la tortuga. Como iba muy adelante, pensó que podía "
            "descansar bajo un árbol. Se quedó dormida.\n"
            "La tortuga caminó despacio, pero no se detuvo ni un momento. "
            "Pasó junto al árbol y siguió avanzando.\n"
            "Cuando la liebre despertó, corrió con todas sus fuerzas. Ya "
            "era tarde: la tortuga había cruzado la meta."),
        "moraleja": "Con constancia se llega más lejos que con apuro.",
        "literal": "¿Quién ganó la carrera?",
        "inferencial": "¿Por qué crees que la liebre se quedó dormida?",
        "critica": "¿Alguna vez dejaste algo a medias por confiarte? Cuenta qué pasó.",
    },
    {
        "titulo": "El león y el ratón", "grado": 1,
        "texto": (
            "Un león dormía en el bosque. Un ratoncito pasó corriendo y lo "
            "despertó sin querer.\n"
            "El león lo atrapó con su enorme pata.\n"
            "—¡Perdóname! —pidió el ratón—. Algún día podré ayudarte.\n"
            "El león se rió, pero lo dejó ir.\n"
            "Días después, unos cazadores atraparon al león con una red. El "
            "león rugía y no podía soltarse.\n"
            "El ratoncito escuchó los rugidos y llegó corriendo. Con sus "
            "dientes pequeños royó las cuerdas, una por una, hasta que el "
            "león quedó libre.\n"
            "—Gracias, amigo —dijo el león—. Ya no me reiré de los pequeños."),
        "moraleja": "Nadie es tan pequeño que no pueda ayudar.",
        "literal": "¿Cómo ayudó el ratón al león?",
        "inferencial": "¿Por qué el león dejó libre al ratón la primera vez?",
        "critica": "¿Te han ayudado alguna vez cuando nadie lo esperaba?",
    },
    {
        "titulo": "La zorra y las uvas", "grado": 1,
        "texto": (
            "Una zorra caminaba con mucha hambre. De pronto vio un racimo "
            "de uvas moradas colgando de una parra.\n"
            "Las uvas se veían jugosas y dulces.\n"
            "La zorra saltó una vez, pero no las alcanzó. Saltó otra vez, "
            "más alto, y tampoco. Saltó muchas veces más, hasta quedar "
            "cansada.\n"
            "Al final se dio por vencida. Se alejó caminando y dijo en voz "
            "alta:\n"
            "—No importa. Esas uvas están verdes."),
        "moraleja": "Es fácil despreciar lo que no logramos alcanzar.",
        "literal": "¿Qué quería alcanzar la zorra?",
        "inferencial": "¿Las uvas estaban verdes de verdad? ¿Por qué lo dijo?",
        "critica": "¿Qué podría haber hecho la zorra en lugar de rendirse?",
    },
    {
        "titulo": "El pastorcito mentiroso", "grado": 1,
        "texto": (
            "Un pastorcito cuidaba ovejas en el cerro. Se aburría mucho.\n"
            "Un día gritó:\n"
            "—¡El lobo! ¡Viene el lobo!\n"
            "Los vecinos subieron corriendo, pero no había ningún lobo. El "
            "pastorcito se rió.\n"
            "Al día siguiente hizo lo mismo. Los vecinos volvieron a subir "
            "y otra vez se rió de ellos.\n"
            "Pero una tarde el lobo llegó de verdad.\n"
            "—¡El lobo! ¡Ayúdenme! —gritó el pastorcito.\n"
            "Nadie subió. Todos pensaron que mentía otra vez."),
        "moraleja": "Quien miente muchas veces ya no es creído cuando dice la verdad.",
        "literal": "¿Qué gritaba el pastorcito?",
        "inferencial": "¿Por qué nadie lo ayudó la última vez?",
        "critica": "¿Qué le dirías al pastorcito si fueras su amigo?",
    },
    {
        "titulo": "La cigarra y la hormiga", "grado": 1,
        "texto": (
            "Todo el verano la cigarra cantó bajo el sol.\n"
            "La hormiga, en cambio, trabajó sin parar. Llevaba granos a su "
            "casa, uno tras otro.\n"
            "—¿Por qué trabajas tanto? Ven a cantar —le decía la cigarra.\n"
            "—Guardo comida para el invierno —respondía la hormiga.\n"
            "Llegó el invierno. Cayó la nieve y ya no había comida en el "
            "campo.\n"
            "La cigarra, con frío y hambre, tocó la puerta de la hormiga.\n"
            "La hormiga le abrió y compartió con ella. Pero le dijo:\n"
            "—El próximo verano, guarda tú también."),
        "moraleja": "Prepararse a tiempo evita sufrir después.",
        "literal": "¿Qué hizo la hormiga durante el verano?",
        "inferencial": "¿Por qué la cigarra pasó hambre en invierno?",
        "critica": "¿Estuvo bien que la hormiga compartiera? ¿Por qué?",
    },
    {
        "titulo": "El cuervo y la zorra", "grado": 2,
        "texto": (
            "Un cuervo encontró un pedazo de queso y se subió a una rama "
            "para comerlo tranquilo.\n"
            "Una zorra lo vio desde abajo y se le hizo agua la boca.\n"
            "—¡Qué hermoso eres, cuervo! —le dijo—. Tus plumas brillan. "
            "Seguro que tu voz es la más linda del bosque. ¡Canta un poco!\n"
            "El cuervo se sintió muy orgulloso. Abrió el pico para cantar y "
            "el queso cayó al suelo.\n"
            "La zorra lo atrapó al vuelo.\n"
            "—Gracias por el queso —dijo—. La próxima vez, desconfía de "
            "quien te alaba demasiado."),
        "moraleja": "Cuidado con quien te halaga: puede querer algo de ti.",
        "literal": "¿Qué tenía el cuervo en el pico?",
        "inferencial": "¿Por qué la zorra le dijo tantos elogios al cuervo?",
        "critica": "¿Cómo puedes darte cuenta de si alguien te halaga de verdad?",
    },
    {
        "titulo": "La gallina de los huevos de oro", "grado": 2,
        "texto": (
            "Un campesino tenía una gallina muy especial: cada mañana ponía "
            "un huevo de oro.\n"
            "El campesino vendía el huevo y poco a poco se hizo rico.\n"
            "Pero un día pensó:\n"
            "—Si adentro de la gallina hay tanto oro, lo sacaré todo de una "
            "vez y seré millonario.\n"
            "Tomó un cuchillo y abrió a la gallina.\n"
            "Adentro no había oro. La gallina murió y nunca más hubo huevos "
            "dorados.\n"
            "El campesino se quedó pobre y arrepentido."),
        "moraleja": "La ambición sin paciencia hace perder lo que ya se tiene.",
        "literal": "¿Qué ponía la gallina cada mañana?",
        "inferencial": "¿Qué error cometió el campesino?",
        "critica": "¿Qué habrías hecho tú en su lugar?",
    },
    {
        "titulo": "El perro y su reflejo", "grado": 1,
        "texto": (
            "Un perro caminaba con un hueso grande en el hocico.\n"
            "Al cruzar un puente, miró hacia el río y vio a otro perro que "
            "también llevaba un hueso.\n"
            "En realidad era su propio reflejo en el agua, pero él no lo "
            "sabía.\n"
            "—Ese hueso se ve más grande que el mío —pensó.\n"
            "Abrió la boca para ladrar y quitarle el hueso al otro perro.\n"
            "Su hueso cayó al río y se hundió.\n"
            "El perro se quedó sin nada."),
        "moraleja": "Por querer más, se pierde lo que ya se tiene.",
        "literal": "¿Qué llevaba el perro en el hocico?",
        "inferencial": "¿A quién vio realmente el perro en el agua?",
        "critica": "¿Qué consejo le darías al perro?",
    },
    {
        "titulo": "El viento y el sol", "grado": 2,
        "texto": (
            "El viento y el sol discutían sobre quién era más fuerte.\n"
            "Vieron pasar a un caminante con un abrigo.\n"
            "—Ganará quien logre quitarle el abrigo —dijo el sol.\n"
            "El viento sopló con toda su fuerza. Sopló y sopló. Pero "
            "mientras más soplaba, el caminante más se cerraba el abrigo "
            "para protegerse del frío.\n"
            "Cansado, el viento se rindió.\n"
            "Entonces el sol brilló suavemente. El caminante empezó a "
            "sentir calor. Poco después se quitó el abrigo y se sentó a "
            "descansar bajo un árbol."),
        "moraleja": "Se logra más con amabilidad que con fuerza.",
        "literal": "¿Quién logró que el caminante se quitara el abrigo?",
        "inferencial": "¿Por qué el caminante se cerraba más el abrigo con el viento?",
        "critica": "¿En qué situación de tu vida sirve más ser amable que insistir?",
    },
    {
        "titulo": "Los dos amigos y el oso", "grado": 2,
        "texto": (
            "Dos amigos caminaban por el bosque. De pronto apareció un oso.\n"
            "Uno de ellos corrió y se subió rápido a un árbol, sin avisarle "
            "al otro.\n"
            "El segundo amigo no pudo escapar. Se tiró al suelo y se quedó "
            "quieto, sin respirar fuerte.\n"
            "El oso se acercó, le olió la cara y se fue.\n"
            "El amigo del árbol bajó riendo:\n"
            "—¿Qué te dijo el oso al oído?\n"
            "—Me dijo que no viaje con amigos que me abandonan en el "
            "peligro —respondió."),
        "moraleja": "Los amigos de verdad se conocen en los momentos difíciles.",
        "literal": "¿Qué hizo el segundo amigo cuando llegó el oso?",
        "inferencial": "¿Por qué el oso se fue sin hacerle daño?",
        "critica": "¿Qué harías tú si un amigo estuviera en peligro?",
    },
    {
        "titulo": "El ratón de campo y el ratón de ciudad", "grado": 2,
        "texto": (
            "El ratón de ciudad visitó a su primo del campo. Cenaron "
            "granos y raíces.\n"
            "—¡Qué comida tan pobre! Ven a mi casa —dijo el de ciudad.\n"
            "Fueron a la ciudad. En la mesa había queso, pan y frutas. El "
            "ratón de campo estaba feliz.\n"
            "De pronto se escucharon pasos y ladridos. Los dos corrieron a "
            "esconderse en un hueco, con el corazón acelerado.\n"
            "Cuando todo pasó, el ratón de campo dijo:\n"
            "—Prefiero mis granos tranquilos que tu queso con miedo. Y "
            "regresó a casa."),
        "moraleja": "Vale más lo sencillo con tranquilidad que lo abundante con miedo.",
        "literal": "¿Qué comían en el campo?",
        "inferencial": "¿Por qué el ratón de campo decidió regresar?",
        "critica": "¿Tú qué preferirías? Explica por qué.",
    },
    {
        "titulo": "La lechera", "grado": 2,
        "texto": (
            "Una joven llevaba en la cabeza un balde lleno de leche para "
            "vender en el mercado.\n"
            "Mientras caminaba, empezó a soñar:\n"
            "—Con el dinero de la leche compraré huevos. De los huevos "
            "nacerán pollitos. Venderé los pollos y compraré un vestido "
            "nuevo. Con ese vestido todos me mirarán en la fiesta y yo "
            "saludaré así...\n"
            "Al mover la cabeza, el balde se cayó.\n"
            "La leche se derramó en el camino y con ella se fueron los "
            "huevos, los pollos y el vestido."),
        "moraleja": "Antes de soñar con lo que vendrá, cuida lo que tienes ahora.",
        "literal": "¿Qué llevaba la lechera en la cabeza?",
        "inferencial": "¿Por qué se le cayó el balde?",
        "critica": "¿Está mal soñar? ¿Qué le faltó hacer a la lechera?",
    },
    {
        "titulo": "El burro cargado de sal", "grado": 2,
        "texto": (
            "Un burro llevaba sacos de sal. Al cruzar un río, resbaló y "
            "cayó al agua.\n"
            "La sal se disolvió y la carga quedó mucho más liviana.\n"
            "El burro se puso feliz con su descubrimiento.\n"
            "Al día siguiente lo cargaron con esponjas. Al llegar al río, "
            "el burro se tiró al agua a propósito.\n"
            "Pero las esponjas absorbieron el agua y se volvieron pesadas.\n"
            "El burro apenas pudo salir del río, cargando el doble de "
            "peso."),
        "moraleja": "Lo que funciona una vez no siempre funciona otra.",
        "literal": "¿Qué llevaba el burro el primer día?",
        "inferencial": "¿Por qué las esponjas pesaron más al mojarse?",
        "critica": "¿Qué debió hacer el burro antes de tirarse al agua?",
    },
    {
        "titulo": "La paloma y la hormiga", "grado": 1,
        "texto": (
            "Una hormiga cayó a un arroyo y la corriente se la llevaba.\n"
            "Una paloma la vio desde una rama. Cortó una hoja y la dejó "
            "caer al agua.\n"
            "La hormiga se subió a la hoja y llegó a la orilla, salvada.\n"
            "Poco después, un cazador apuntó a la paloma con su honda.\n"
            "La hormiga lo vio. Corrió y le picó el pie con todas sus "
            "fuerzas.\n"
            "El cazador gritó de dolor y la paloma escuchó el ruido. Voló "
            "lejos, sana y salva."),
        "moraleja": "El favor que damos hoy puede volver mañana.",
        "literal": "¿Cómo salvó la paloma a la hormiga?",
        "inferencial": "¿Por qué la hormiga picó al cazador?",
        "critica": "Cuenta una vez en que ayudaste a alguien.",
    },
    {
        "titulo": "El lobo con piel de oveja", "grado": 2,
        "texto": (
            "Un lobo tenía hambre, pero el pastor cuidaba muy bien su "
            "rebaño.\n"
            "Entonces el lobo encontró una piel de oveja en el campo. Se la "
            "puso encima y se metió entre las ovejas.\n"
            "Nadie lo reconoció. Caminó tranquilo con el rebaño hasta el "
            "corral.\n"
            "Esa noche el pastor quiso preparar la cena. Entró al corral y "
            "eligió, sin mirar mucho, a la oveja más gorda.\n"
            "Era el lobo disfrazado.\n"
            "Su propio engaño lo llevó a su final."),
        "moraleja": "Quien engaña suele caer en su propia trampa.",
        "literal": "¿Cómo se disfrazó el lobo?",
        "inferencial": "¿Por qué el pastor no se dio cuenta del engaño?",
        "critica": "¿Por qué es peligroso fingir ser quien no eres?",
    },
    {
        "titulo": "Las ranas piden un rey", "grado": 2,
        "texto": (
            "Las ranas vivían libres en su laguna, pero no estaban "
            "contentas.\n"
            "—¡Queremos un rey! —pidieron a gritos.\n"
            "Les enviaron un tronco. Cayó al agua con un ruido enorme y las "
            "ranas se escondieron asustadas.\n"
            "Después vieron que no se movía y empezaron a saltar encima.\n"
            "—Este rey es aburrido. ¡Queremos otro! —reclamaron.\n"
            "Entonces les enviaron una cigüeña. La cigüeña caminó por la "
            "laguna y se comió a varias ranas.\n"
            "Las ranas extrañaron su vieja libertad."),
        "moraleja": "A veces se pierde lo bueno por no saber valorarlo.",
        "literal": "¿Qué pidieron las ranas?",
        "inferencial": "¿Por qué las ranas extrañaron su libertad al final?",
        "critica": "¿Qué cosas buenas tienes ahora que a veces no valoras?",
    },
    {
        "titulo": "El leñador honrado", "grado": 2,
        "texto": (
            "Un leñador cortaba árboles junto al río. Sin querer, su hacha "
            "cayó al agua.\n"
            "El leñador se sentó a llorar, porque era su única herramienta.\n"
            "Apareció un anciano y sacó del río un hacha de oro.\n"
            "—¿Es esta la tuya?\n"
            "—No, señor —respondió el leñador.\n"
            "El anciano sacó una de plata. El leñador volvió a decir que "
            "no.\n"
            "Por fin sacó una vieja hacha de hierro.\n"
            "—¡Esa sí es la mía! —dijo feliz.\n"
            "El anciano le regaló las tres, por su honradez."),
        "moraleja": "La honradez siempre tiene recompensa.",
        "literal": "¿Qué se le cayó al leñador?",
        "inferencial": "¿Por qué el anciano le regaló las tres hachas?",
        "critica": "¿Qué habrías dicho tú frente al hacha de oro?",
    },
    {
        "titulo": "El avaro y su oro", "grado": 2,
        "texto": (
            "Un hombre muy avaro vendió todo lo que tenía y compró una "
            "barra de oro.\n"
            "La enterró en un hueco detrás de su casa.\n"
            "Cada día iba a mirar el hueco, sin sacar nunca el oro.\n"
            "Un vecino lo espió, descubrió el escondite y se llevó la "
            "barra.\n"
            "Al día siguiente el avaro encontró el hueco vacío y lloró "
            "desesperado.\n"
            "El vecino le dijo:\n"
            "—No llores. Pon una piedra en el hueco y míralo igual. Como "
            "nunca usaste el oro, te servirá lo mismo."),
        "moraleja": "Lo que se guarda y nunca se usa es como si no existiera.",
        "literal": "¿Dónde escondió el avaro su oro?",
        "inferencial": "¿Por qué el vecino le dijo que pusiera una piedra?",
        "critica": "¿De qué sirve tener algo si nunca lo usas ni lo compartes?",
    },
    {
        "titulo": "La zorra y la cigüeña", "grado": 2,
        "texto": (
            "La zorra invitó a cenar a la cigüeña. Le sirvió la sopa en un "
            "plato ancho y plano.\n"
            "La zorra lamió toda su sopa rápido. La cigüeña, con su pico "
            "largo, no pudo tomar ni una gota.\n"
            "Días después, la cigüeña invitó a la zorra.\n"
            "Sirvió la comida en un jarrón alto y angosto.\n"
            "La cigüeña metió su pico y comió tranquila. La zorra solo "
            "pudo oler la comida.\n"
            "—Ahora sabes cómo me sentí —le dijo la cigüeña."),
        "moraleja": "No hagas a otros lo que no quieres que te hagan a ti.",
        "literal": "¿En qué le sirvió la zorra la sopa a la cigüeña?",
        "inferencial": "¿Por qué la cigüeña usó un jarrón alto?",
        "critica": "¿Cómo se siente alguien cuando lo dejan de lado en un juego?",
    },
    {
        "titulo": "El águila y el escarabajo", "grado": 2,
        "texto": (
            "Una liebre corría perseguida por un águila. Pidió ayuda a un "
            "escarabajo que estaba cerca.\n"
            "El escarabajo le rogó al águila que la dejara ir. El águila "
            "ni lo escuchó y se llevó a la liebre.\n"
            "El escarabajo no lo olvidó. Buscó el nido del águila y empujó "
            "sus huevos fuera, uno por uno.\n"
            "El águila cambió su nido de sitio muchas veces, pero el "
            "escarabajo siempre lo encontraba.\n"
            "Al final el águila entendió que hasta el más pequeño merece "
            "respeto."),
        "moraleja": "No desprecies a nadie por ser pequeño.",
        "literal": "¿A quién pidió ayuda la liebre?",
        "inferencial": "¿Por qué el escarabajo persiguió al águila?",
        "critica": "¿Por qué está mal burlarse de los más pequeños del salón?",
    },
]

TRABALENGUAS = [
    "Tres tristes tigres tragaban trigo en un trigal.",
    "Pablito clavó un clavito en la calva de un calvito.",
    "El cielo está enladrillado, ¿quién lo desenladrillará? "
    "El desenladrillador que lo desenladrille, buen desenladrillador será.",
    "Como poco coco como, poco coco compro.",
    "Erre con erre cigarro, erre con erre barril; "
    "rápido corren los carros cargados de azúcar del ferrocarril.",
    "Pepe Pecas pica papas con un pico; "
    "con un pico pica papas Pepe Pecas.",
    "Mi mamá me mima mucho y yo mimo a mi mamá.",
    "El perro de San Roque no tiene rabo porque Ramón Ramírez "
    "se lo ha cortado.",
    "Paco Peco, chico rico, insultaba como un loco a su tío Federico.",
    "La bruja piruja prepara un brebaje con una hoja de brócoli verde.",
    "Juan tuvo un tubo, y el tubo que tuvo se le rompió.",
    "Si Sansón no sazona su salsa con sal, sosa le sale la salsa a Sansón.",
]


# ================================================================
# 2. GENERACIÓN DE FICHAS EN PDF
# ================================================================

def _pie_pagina(canvas, doc):
    from reportlab.lib.units import cm
    canvas.saveState()
    canvas.setFont("Helvetica", 6.5)
    canvas.setFillColorRGB(0.42, 0.45, 0.50)
    canvas.drawCentredString(doc.pagesize[0] / 2, 0.75 * cm, PIE_LEGAL)
    canvas.setStrokeColorRGB(0.80, 0.83, 0.87)
    canvas.setLineWidth(0.4)
    canvas.line(1.4 * cm, 1.05 * cm, doc.pagesize[0] - 1.4 * cm, 1.05 * cm)
    canvas.restoreState()


def generar_ficha_pdf(lecturas, incluir_trabalenguas=True, grado_txt=""):
    """Una ficha por lectura, en hojas separadas y listas para fotocopiar."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, PageBreak)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    ss = getSampleStyleSheet()
    marca = ParagraphStyle("m", parent=ss["Title"], fontSize=15,
                           textColor=colors.HexColor("#001e7c"),
                           alignment=TA_CENTER, spaceAfter=0, leading=18)
    lema = ParagraphStyle("l", parent=ss["Normal"], fontSize=8,
                          textColor=colors.HexColor("#b45309"),
                          alignment=TA_CENTER, spaceAfter=8)
    titulo = ParagraphStyle("t", parent=ss["Title"], fontSize=16,
                            textColor=colors.HexColor("#001e7c"),
                            alignment=TA_CENTER, spaceAfter=8, spaceBefore=4)
    cuerpo = ParagraphStyle("c", parent=ss["Normal"], fontSize=13,
                            leading=22, alignment=TA_JUSTIFY,
                            spaceAfter=6)
    preg = ParagraphStyle("p", parent=ss["Normal"], fontSize=11.5,
                          leading=16, spaceAfter=2)
    nota = ParagraphStyle("n", parent=ss["Normal"], fontSize=9,
                          textColor=colors.HexColor("#475569"))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                            topMargin=1.3 * cm, bottomMargin=1.6 * cm)
    story = []

    for idx, L in enumerate(lecturas):
        story.append(Paragraph(ENCABEZADO_L1, marca))
        story.append(Paragraph(ENCABEZADO_L2, lema))

        datos = Table([[
            "Nombre: ______________________________________",
            f"Grado: {grado_txt or '______'}",
            "Fecha: ____/____/______",
        ]], colWidths=[9.4 * cm, 3.5 * cm, 4.5 * cm])
        datos.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, -1), 0.8, colors.HexColor("#001e7c")),
        ]))
        story.append(datos)
        story.append(Spacer(1, 8))

        story.append(Paragraph("FICHA DE COMPRENSIÓN LECTORA", nota))
        story.append(Paragraph(L["titulo"].upper(), titulo))

        for parrafo in L["texto"].split("\n"):
            if parrafo.strip():
                story.append(Paragraph(parrafo.strip(), cuerpo))

        story.append(Spacer(1, 6))
        mor = Table([[Paragraph(
            f"<b>Moraleja:</b> {L['moraleja']}", preg)]],
            colWidths=[17.4 * cm])
        mor.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef3c7")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#f59e0b")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(mor)
        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Responde:</b>", preg))
        etiquetas = [("1.", L["literal"], "¿Qué dice el texto?"),
                     ("2.", L["inferencial"], "¿Qué puedo deducir?"),
                     ("3.", L["critica"], "¿Qué opino yo?")]
        for num, pregunta, pista in etiquetas:
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                f"<b>{num}</b> {pregunta} "
                f"<font size=8 color='#94a3b8'>({pista})</font>", preg))
            for _ in range(2):
                story.append(Paragraph(
                    "<font color='#cbd5e1'>"
                    "________________________________________________"
                    "________________________________</font>", preg))

        if incluir_trabalenguas:
            tl = TRABALENGUAS[idx % len(TRABALENGUAS)]
            story.append(Spacer(1, 10))
            tt = Table([[Paragraph(
                f"<b>Trabalenguas del día:</b> {tl}", preg)]],
                colWidths=[17.4 * cm])
            tt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#2563eb")),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ]))
            story.append(tt)

        if idx < len(lecturas) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=_pie_pagina, onLaterPages=_pie_pagina)
    buf.seek(0)
    return buf.getvalue()


# ================================================================
# 3. INTERFAZ
# ================================================================

def tab_fichas_primaria(config=None):
    st.subheader("📖 Fichas de Comprensión Lectora — Primaria")
    st.caption("20 fábulas de Esopo adaptadas a 1° y 2° grado, con preguntas "
               "de los tres niveles de comprensión del CNEB y un "
               "trabalenguas en cada ficha.")

    c1, c2 = st.columns(2)
    with c1:
        filtro = st.selectbox(
            "Nivel de dificultad:",
            ["Todas las lecturas", "Solo 1° grado (textos más cortos)",
             "Desde 2° grado"], key="fp_filtro")
    with c2:
        grado_txt = st.text_input("Grado y sección (se imprime en la ficha):",
                                  placeholder="1° A", key="fp_grado")

    trab = st.checkbox("Incluir trabalenguas al pie de cada ficha",
                       value=True, key="fp_trab")

    if filtro.startswith("Solo 1"):
        disponibles = [L for L in LECTURAS if L["grado"] == 1]
    elif filtro.startswith("Desde 2"):
        disponibles = [L for L in LECTURAS if L["grado"] == 2]
    else:
        disponibles = list(LECTURAS)

    titulos = [L["titulo"] for L in disponibles]
    elegidas = st.multiselect(
        "Lecturas a incluir (vacío = todas):", titulos, key="fp_sel",
        help="Cada lectura se imprime en su propia hoja, lista para "
             "fotocopiar.")
    seleccion = ([L for L in disponibles if L["titulo"] in elegidas]
                 if elegidas else disponibles)

    st.info(f"**{len(seleccion)} ficha(s)** — se imprimirán en "
            f"{len(seleccion)} hoja(s).")

    with st.expander("Ver una lectura antes de imprimir"):
        if seleccion:
            v = st.selectbox("Lectura:", [L["titulo"] for L in seleccion],
                             key="fp_prev")
            L = next(x for x in seleccion if x["titulo"] == v)
            st.markdown(f"### {L['titulo']}")
            st.write(L["texto"])
            st.success(f"**Moraleja:** {L['moraleja']}")
            st.markdown(f"**1.** {L['literal']}  \n"
                        f"**2.** {L['inferencial']}  \n"
                        f"**3.** {L['critica']}")

    if seleccion and st.button("📄 GENERAR FICHAS EN PDF", type="primary",
                               use_container_width=True, key="fp_gen"):
        try:
            pdf = generar_ficha_pdf(seleccion, trab, grado_txt)
            st.download_button(
                "⬇️ Descargar fichas", data=pdf,
                file_name=f"fichas_comprension_{len(seleccion)}.pdf",
                mime="application/pdf", use_container_width=True,
                key="fp_dl")
            st.success("Listo. Imprime a doble cara para ahorrar papel: "
                       "cada ficha ocupa una carilla completa.")
        except Exception as e:
            st.error(f"No se pudo generar: {e}")
