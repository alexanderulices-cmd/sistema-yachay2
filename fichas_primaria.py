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

FABULAS_1_2 = [
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

# ================================================================
# LECTURAS 3° Y 4° — LEYENDAS ANDINAS Y MITOS DEL MUNDO
# ================================================================

LECTURAS_3_4 = [
    {"titulo": "Manco Cápac y Mama Ocllo", "tipo": "Leyenda andina", "grado": 3,
     "texto": (
        "Cuentan los antiguos que el dios Sol miró la tierra y la vio en "
        "desorden. Los hombres vivían en cuevas y no sabían cultivar.\n"
        "Entonces envió a sus hijos, Manco Cápac y Mama Ocllo, desde las "
        "aguas del lago Titicaca. Les entregó una vara de oro y les dijo:\n"
        "—Caminen hacia el norte. Donde la vara se hunda por completo, "
        "funden allí su pueblo.\n"
        "Los hermanos caminaron muchos días probando la tierra. En el cerro "
        "Huanacaure, la vara se hundió sin esfuerzo.\n"
        "Allí fundaron el Cusco. Manco Cápac enseñó a los hombres a cultivar "
        "y construir. Mama Ocllo enseñó a las mujeres a hilar y tejer."),
     "moraleja": "Todo pueblo se levanta con trabajo y conocimiento compartido.",
     "literal": "¿Qué les entregó el dios Sol a sus hijos?",
     "inferencial": "¿Por qué crees que la vara debía hundirse en la tierra?",
     "critica": "¿Qué enseñanzas de Manco Cápac y Mama Ocllo siguen siendo útiles hoy?"},

    {"titulo": "Los hermanos Ayar", "tipo": "Leyenda andina", "grado": 4,
     "texto": (
        "De la montaña de Pacaritambo salieron cuatro hermanos con sus "
        "esposas, buscando tierra fértil.\n"
        "Ayar Cachi era tan fuerte que con su honda derribaba cerros. Sus "
        "hermanos, temerosos de su poder, lo encerraron en una cueva.\n"
        "Ayar Uchu se convirtió en piedra en el cerro Huanacaure, para "
        "quedar como guardián del camino.\n"
        "Ayar Auca voló hasta el valle y se transformó en piedra para marcar "
        "el lugar exacto donde debía nacer la ciudad.\n"
        "Solo Ayar Manco llegó al final del viaje. Con su esposa Mama Ocllo "
        "fundó el Cusco y tomó el nombre de Manco Cápac.\n"
        "Cada hermano dejó algo de sí para que la ciudad existiera."),
     "moraleja": "Toda gran obra se sostiene sobre el aporte de muchos.",
     "literal": "¿Cuántos hermanos salieron de Pacaritambo?",
     "inferencial": "¿Por qué los hermanos encerraron a Ayar Cachi?",
     "critica": "¿Te parece justo lo que hicieron con Ayar Cachi? Explica."},

    {"titulo": "El Inkarrí", "tipo": "Mito andino", "grado": 4,
     "texto": (
        "Los abuelos de los Andes cuentan que hubo un rey llamado Inkarrí, "
        "sabio y justo, que ordenaba los cerros y los ríos con su palabra.\n"
        "Cuando llegaron los conquistadores, lo apresaron y separaron su "
        "cabeza de su cuerpo. Enterraron cada parte en un lugar distinto, "
        "muy lejos una de otra.\n"
        "Pero bajo la tierra, dicen, la cabeza sigue viva y el cuerpo crece "
        "lentamente hacia ella.\n"
        "Cuando el cuerpo esté completo, Inkarrí volverá a levantarse y el "
        "mundo andino recuperará su orden.\n"
        "Por eso los abuelos dicen que la esperanza nunca muere: solo "
        "espera bajo la tierra."),
     "moraleja": "Un pueblo que recuerda su historia mantiene viva su esperanza.",
     "literal": "¿Qué hicieron los conquistadores con Inkarrí?",
     "inferencial": "¿Qué representa que el cuerpo crezca bajo la tierra?",
     "critica": "¿Por qué crees que este relato se sigue contando hasta hoy?"},

    {"titulo": "La leyenda del Huascarán", "tipo": "Leyenda andina", "grado": 3,
     "texto": (
        "Huáscar y Huandy se amaban, pero sus familias eran enemigas y les "
        "prohibieron verse.\n"
        "Una noche escaparon juntos hacia las alturas. Caminaron por la "
        "nieve tomados de la mano, sin mirar atrás.\n"
        "El frío fue más fuerte que ellos. Cayeron abrazados sobre el "
        "hielo y no volvieron a levantarse.\n"
        "Al amanecer, en aquel lugar se alzaban dos nevados enormes, muy "
        "juntos, brillando bajo el sol.\n"
        "Los llamaron Huascarán y Huandoy. Y dicen que el agua que baja "
        "de sus cumbres son las lágrimas que aún derraman."),
     "moraleja": "Los rencores entre familias hacen daño a los inocentes.",
     "literal": "¿Por qué Huáscar y Huandy no podían verse?",
     "inferencial": "¿Qué representan los dos nevados en la leyenda?",
     "critica": "¿Qué habrías aconsejado a las familias de los jóvenes?"},

    {"titulo": "El puente del Apurímac", "tipo": "Leyenda andina", "grado": 4,
     "texto": (
        "El río Apurímac corría tan bravo que nadie podía cruzarlo. Su "
        "nombre significa «el que habla», por el ruido de sus aguas.\n"
        "Los pueblos de un lado y del otro no podían visitarse ni comerciar.\n"
        "Entonces los ancianos reunieron a todas las familias. Durante "
        "meses, cada una trenzó cuerdas de paja brava.\n"
        "Un día tendieron todas las cuerdas juntas de orilla a orilla y "
        "construyeron un puente colgante.\n"
        "Cada año lo rehacían entre todos. El puente duró siglos, porque "
        "no lo sostenía la paja, sino el trabajo comunitario."),
     "moraleja": "Lo que nadie puede solo, un pueblo unido sí lo logra.",
     "literal": "¿Con qué material hicieron el puente?",
     "inferencial": "¿Por qué el texto dice que al puente lo sostenía el trabajo comunitario?",
     "critica": "¿Qué problema de tu comunidad podría resolverse trabajando juntos?"},

    {"titulo": "Ícaro y las alas de cera", "tipo": "Mito griego", "grado": 4,
     "texto": (
        "Dédalo era un gran inventor, encerrado con su hijo Ícaro en una "
        "isla de la que no podían escapar.\n"
        "Con plumas de aves y cera, Dédalo construyó dos pares de alas.\n"
        "—Vuela a media altura —le advirtió a su hijo—. Si vas muy bajo, el "
        "mar mojará tus plumas. Si subes demasiado, el sol derretirá la "
        "cera.\n"
        "Al principio Ícaro obedeció. Pero volar lo llenó de alegría y "
        "quiso subir más y más, hasta acercarse al sol.\n"
        "La cera se derritió. Las plumas se soltaron una a una e Ícaro "
        "cayó al mar.\n"
        "Dédalo siguió volando solo, llorando a su hijo."),
     "moraleja": "El entusiasmo sin prudencia puede costar caro.",
     "literal": "¿Qué le advirtió Dédalo a su hijo?",
     "inferencial": "¿Por qué Ícaro desobedeció a su padre?",
     "critica": "¿Cuándo es bueno arriesgarse y cuándo hay que escuchar un consejo?"},

    {"titulo": "El caballo de Troya", "tipo": "Mito griego", "grado": 4,
     "texto": (
        "Los griegos llevaban diez años sitiando la ciudad de Troya sin "
        "poder entrar. Sus murallas eran altísimas.\n"
        "Entonces Ulises tuvo una idea. Construyeron un enorme caballo de "
        "madera y escondieron soldados dentro.\n"
        "Dejaron el caballo frente a las puertas y fingieron marcharse en "
        "sus barcos.\n"
        "Los troyanos creyeron que era un regalo de despedida y lo metieron "
        "a la ciudad para celebrarlo.\n"
        "Esa noche, mientras todos dormían, los soldados salieron del "
        "caballo y abrieron las puertas.\n"
        "Troya cayó no por la fuerza, sino por un engaño."),
     "moraleja": "La astucia puede lograr lo que la fuerza no consigue.",
     "literal": "¿Qué escondía el caballo de madera?",
     "inferencial": "¿Por qué los troyanos metieron el caballo a la ciudad?",
     "critica": "¿Está bien usar el engaño para ganar? Da tu opinión."},

    {"titulo": "La grulla agradecida", "tipo": "Cuento japonés", "grado": 3,
     "texto": (
        "Un anciano pobre encontró una grulla atrapada en una trampa. Con "
        "cuidado le soltó la pata y la dejó volar.\n"
        "Esa noche, una joven tocó la puerta de su casa pidiendo refugio. "
        "El anciano y su esposa la recibieron con cariño.\n"
        "La joven les dijo que sabía tejer, pero les pidió algo:\n"
        "—Nunca miren mientras trabajo.\n"
        "Cada día salía de su cuarto con telas hermosas que los ancianos "
        "vendían muy bien. Pero la joven adelgazaba.\n"
        "Un día, la curiosidad los venció y espiaron. Dentro había una "
        "grulla arrancándose sus propias plumas para tejer.\n"
        "Al ser descubierta, la grulla voló y no regresó jamás."),
     "moraleja": "La confianza que se rompe difícilmente se recupera.",
     "literal": "¿Qué le pidió la joven a los ancianos?",
     "inferencial": "¿Por qué la joven adelgazaba cada día?",
     "critica": "¿Por qué crees que es difícil respetar la privacidad de otros?"},

    {"titulo": "El dragón y la perla", "tipo": "Cuento chino", "grado": 4,
     "texto": (
        "Un niño pobre encontró en el campo una perla que brillaba como la "
        "luna. La guardó en el jarro de arroz de su casa.\n"
        "A la mañana siguiente, el jarro estaba lleno hasta el borde. La "
        "puso en la caja del dinero y ocurrió lo mismo.\n"
        "El niño y su madre compartieron el arroz con todos sus vecinos "
        "hambrientos.\n"
        "Unos hombres codiciosos supieron del secreto y fueron a robarla.\n"
        "El niño, para que no cayera en sus manos, se tragó la perla.\n"
        "Al instante sintió un calor enorme, corrió al río y se convirtió "
        "en dragón. Desde entonces cuida las aguas que dan de comer al "
        "pueblo."),
     "moraleja": "Lo que se comparte protege a muchos; lo que se acapara, a nadie.",
     "literal": "¿Qué pasaba con lo que el niño guardaba junto a la perla?",
     "inferencial": "¿Por qué el niño decidió tragarse la perla?",
     "critica": "¿Qué diferencia hay entre el niño y los hombres codiciosos?"},

    {"titulo": "Anansi y la sabiduría", "tipo": "Cuento africano", "grado": 3,
     "texto": (
        "Anansi, la araña, quiso guardar toda la sabiduría del mundo solo "
        "para él.\n"
        "Recorrió la tierra recogiéndola y la metió en una calabaza enorme. "
        "Después decidió esconderla en la copa del árbol más alto.\n"
        "Se ató la calabaza al frente del cuerpo e intentó trepar. Pero la "
        "calabaza le estorbaba y resbalaba una y otra vez.\n"
        "Su hijo, que lo miraba desde abajo, le dijo:\n"
        "—Padre, sería más fácil si te la atas a la espalda.\n"
        "Anansi comprendió que, por más sabiduría que hubiera juntado, "
        "aún le faltaba la de su hijo.\n"
        "Enojado, soltó la calabaza. Se rompió y la sabiduría se esparció "
        "por todo el mundo."),
     "moraleja": "Nadie posee todo el saber: siempre se aprende de otros.",
     "literal": "¿Qué guardó Anansi en la calabaza?",
     "inferencial": "¿Por qué Anansi se enojó con el consejo de su hijo?",
     "critica": "¿De quién has aprendido algo que no esperabas?"},

    {"titulo": "El origen del lago Titicaca", "tipo": "Leyenda andina", "grado": 4,
     "texto": (
        "Los apus permitieron a los hombres vivir en un valle fértil, con "
        "una sola condición: no debían subir a la cima del cerro sagrado, "
        "donde ardía el fuego prohibido.\n"
        "Durante años cumplieron. Pero unos hombres, tentados por la "
        "curiosidad y el orgullo, subieron una noche.\n"
        "Los apus, ofendidos, enviaron pumas del interior de la tierra.\n"
        "El dios Sol lloró tres días y tres noches al ver lo ocurrido. Sus "
        "lágrimas inundaron el valle entero.\n"
        "Cuando dejó de llorar, solo se veía un inmenso lago con pumas de "
        "piedra flotando.\n"
        "Por eso lo llamaron Titi-caca, que significa «puma de piedra»."),
     "moraleja": "Romper un acuerdo puede cambiar la vida de todos.",
     "literal": "¿Qué condición pusieron los apus a los hombres?",
     "inferencial": "¿Por qué el lago se llama Titicaca?",
     "critica": "¿Qué acuerdos existen en tu escuela y por qué importa cumplirlos?"},

    {"titulo": "El sembrador de dátiles", "tipo": "Cuento árabe", "grado": 4,
     "texto": (
        "Un rey vio a un anciano encorvado plantando una palmera datilera "
        "en el desierto.\n"
        "—Anciano, esa palmera tarda muchos años en dar fruto. Tú no vivirás "
        "para comer un solo dátil —le dijo.\n"
        "El anciano levantó la mirada y respondió:\n"
        "—Señor, toda mi vida he comido dátiles de palmeras que otros "
        "sembraron y que tampoco los probaron. Yo siembro para los que "
        "vienen después.\n"
        "El rey quedó en silencio. Comprendió que aquel hombre pobre le "
        "había enseñado más que todos sus consejeros."),
     "moraleja": "Sembramos también para quienes vendrán después de nosotros.",
     "literal": "¿Qué estaba plantando el anciano?",
     "inferencial": "¿Por qué el rey quedó en silencio?",
     "critica": "¿Qué podrías hacer hoy que beneficie a los niños del futuro?"},

    {"titulo": "La leyenda del maíz", "tipo": "Leyenda andina", "grado": 3,
     "texto": (
        "Cuentan que hubo un tiempo de hambre en los Andes. La tierra no "
        "daba nada y los niños lloraban.\n"
        "Una joven llamada Sara subió al cerro a pedir ayuda a los apus. "
        "Estuvo tres días sin bajar.\n"
        "Al tercer día se quedó dormida sobre la tierra seca y no despertó.\n"
        "Donde ella durmió creció una planta alta, de hojas largas, con "
        "granos dorados apretados unos contra otros.\n"
        "El pueblo comió y sobrevivió.\n"
        "Por eso al maíz se le llama «sara» en quechua, y por eso se le "
        "agradece antes de sembrarlo."),
     "moraleja": "Los alimentos que nos sostienen merecen respeto y gratitud.",
     "literal": "¿Cómo se llama el maíz en quechua?",
     "inferencial": "¿Qué representa la planta que creció donde durmió Sara?",
     "critica": "¿Qué alimento de tu casa merecería una leyenda? Escríbela en cinco líneas."},

    {"titulo": "El cóndor y la pastora", "tipo": "Leyenda andina", "grado": 4,
     "texto": (
        "Una pastora cuidaba ovejas sola en la puna. Un joven apuesto empezó "
        "a visitarla cada tarde.\n"
        "Un día le propuso llevarla a conocer su casa. Ella aceptó y él la "
        "cargó en su espalda.\n"
        "Subieron y subieron hasta un risco altísimo. Allí el joven se "
        "convirtió en cóndor.\n"
        "La pastora quedó atrapada, sin poder bajar.\n"
        "Un picaflor la escuchó llorar y avisó a su familia, que subió a "
        "rescatarla con sogas.\n"
        "Desde entonces se dice en los Andes: cuidado con quien te ofrece "
        "alturas sin decirte cómo bajarás."),
     "moraleja": "No todo el que promete llevarte lejos piensa en tu regreso.",
     "literal": "¿En qué se convirtió el joven?",
     "inferencial": "¿Por qué la pastora aceptó irse con él?",
     "critica": "¿Qué señales debemos observar antes de confiar en un desconocido?"},

    {"titulo": "El rey Midas", "tipo": "Mito griego", "grado": 4,
     "texto": (
        "El rey Midas pidió un deseo: que todo lo que tocara se convirtiera "
        "en oro.\n"
        "Al principio se llenó de alegría. Tocaba muebles, piedras, ramas, y "
        "todo brillaba.\n"
        "Pero al sentarse a comer, el pan se volvió oro en su boca. El agua "
        "se endureció en su copa.\n"
        "Cuando su hija corrió a abrazarlo, ella también quedó convertida en "
        "una estatua dorada.\n"
        "Midas suplicó que le quitaran el don.\n"
        "Comprendió, demasiado tarde, que había pedido lo que menos "
        "necesitaba."),
     "moraleja": "Desear sin pensar en las consecuencias puede costar lo que más queremos.",
     "literal": "¿Qué le pasó a la hija de Midas?",
     "inferencial": "¿Por qué el don se convirtió en un castigo?",
     "critica": "Si pudieras pedir un deseo, ¿qué consecuencias tendría? Piénsalo antes de responder."},

    {"titulo": "El ratón de la ciudad de Anansi", "tipo": "Cuento africano",
     "grado": 3,
     "texto": (
        "Un campesino tenía un campo lleno de maleza y no quería trabajarlo.\n"
        "Cada mañana decía: «mañana lo hago».\n"
        "Un vecino sembró el suyo, lo regó y lo cuidó.\n"
        "Cuando llegó la cosecha, el vecino llenó sus depósitos.\n"
        "El campesino miró su campo lleno de hierba mala y dijo:\n"
        "—Qué suerte tiene mi vecino.\n"
        "El vecino lo escuchó y respondió:\n"
        "—Es curioso: mientras más temprano me levanto, más suerte tengo."),
     "moraleja": "Lo que muchos llaman suerte suele llamarse constancia.",
     "literal": "¿Qué decía el campesino cada mañana?",
     "inferencial": "¿Qué quiso decir el vecino con su respuesta?",
     "critica": "¿Qué tarea vienes postergando? ¿Cuándo la harás?"},

    {"titulo": "El tigre y el sabio", "tipo": "Cuento hindú", "grado": 4,
     "texto": (
        "Un tigre cayó en una trampa y no podía salir. Pasó un sabio y el "
        "tigre le suplicó ayuda.\n"
        "—Si te libero, me comerás —dijo el sabio.\n"
        "—Jamás. Te lo juro.\n"
        "El sabio, compasivo, lo sacó. Apenas libre, el tigre se preparó "
        "para atacarlo.\n"
        "—¡Prometiste! —reclamó el sabio.\n"
        "—Prometí cuando tenía miedo —respondió el tigre.\n"
        "Pasó un zorro y ambos le contaron. El zorro dijo:\n"
        "—No entiendo. Muéstrenme cómo estaban.\n"
        "El tigre volvió a la trampa para explicarlo. El zorro cerró la "
        "puerta y siguió su camino."),
     "moraleja": "Una promesa hecha por conveniencia se rompe con la misma facilidad.",
     "literal": "¿Qué le prometió el tigre al sabio?",
     "inferencial": "¿Cómo resolvió el zorro la situación?",
     "critica": "¿Cuándo una promesa vale de verdad?"},

    {"titulo": "El origen del arcoíris", "tipo": "Leyenda andina", "grado": 3,
     "texto": (
        "Después de muchos días de lluvia, los ríos se desbordaron y la "
        "gente perdió sus chacras.\n"
        "Una niña subió al cerro y le habló al cielo:\n"
        "—Ya no llores más. Nosotros también tenemos sed de sol.\n"
        "El cielo escuchó. La lluvia paró y el sol asomó entre las nubes.\n"
        "Entonces apareció una franja de colores que iba de un cerro al "
        "otro, como un puente.\n"
        "Los abuelos dijeron que era la señal de que el cielo y la tierra "
        "habían vuelto a entenderse.\n"
        "En quechua lo llamaron k'uychi."),
     "moraleja": "Después de los días difíciles siempre llega el entendimiento.",
     "literal": "¿Cómo se llama el arcoíris en quechua?",
     "inferencial": "¿Qué representaba el arcoíris para los abuelos?",
     "critica": "¿Qué colores ves en la bandera del Cusco? ¿Con qué se relaciona?"},
]


# ================================================================
# LECTURAS 5° Y 6° — TEXTOS PARA PENSAR
# ================================================================

LECTURAS_5_6 = [
    {"titulo": "Los dos lobos", "tipo": "Relato cheroqui", "grado": 5,
     "texto": (
        "Un abuelo conversaba con su nieto sobre la vida.\n"
        "—Dentro de cada persona hay dos lobos que pelean —le dijo—. Uno es "
        "la rabia, la envidia, el orgullo y la mentira. El otro es la "
        "alegría, la humildad, la generosidad y la verdad.\n"
        "El niño lo pensó un momento y preguntó:\n"
        "—Abuelo, ¿cuál de los dos gana?\n"
        "El anciano respondió con calma:\n"
        "—Gana el que tú alimentas cada día."),
     "moraleja": "Nuestro carácter se forma con lo que decidimos alimentar.",
     "literal": "¿Qué representan los dos lobos?",
     "inferencial": "¿Qué significa «alimentar» a un lobo en este relato?",
     "critica": "¿Qué acciones concretas alimentan al lobo bueno en tu vida diaria?"},

    {"titulo": "El elefante encadenado", "tipo": "Reflexión", "grado": 6,
     "texto": (
        "En el circo, un elefante enorme permanecía atado a una pequeña "
        "estaca de madera clavada en el suelo.\n"
        "Un niño preguntó por qué no escapaba, si con su fuerza podía "
        "arrancar un árbol.\n"
        "Un anciano le explicó:\n"
        "—Ese elefante está atado a esa estaca desde que era muy pequeño. "
        "Entonces sí era débil. Tiró y tiró durante días, y no pudo "
        "soltarse.\n"
        "—¿Y ahora? —insistió el niño.\n"
        "—Ahora es gigante, pero cree que no puede. Nunca volvió a "
        "intentarlo desde que creció.\n"
        "El elefante no está atado por la estaca, sino por su recuerdo."),
     "moraleja": "A veces lo que nos detiene no es la realidad, sino una creencia vieja.",
     "literal": "¿Qué sujeta al elefante?",
     "inferencial": "¿Por qué el elefante ya no intenta escapar?",
     "critica": "¿Qué cosa crees que «no puedes» y quizá nunca has vuelto a intentar?"},

    {"titulo": "El violinista en el metro", "tipo": "Texto informativo", "grado": 6,
     "texto": (
        "En 2007, un violinista tocó durante 45 minutos en una estación del "
        "metro de Washington. Interpretó piezas muy difíciles con un violín "
        "de enorme valor.\n"
        "Pasaron más de mil personas. Solo siete se detuvieron a escuchar. "
        "Recaudó apenas 32 dólares.\n"
        "Ese músico era Joshua Bell, uno de los violinistas más reconocidos "
        "del mundo. Días antes había llenado un teatro donde las entradas "
        "costaban cien dólares.\n"
        "El experimento fue organizado por un periódico para estudiar la "
        "percepción de las personas.\n"
        "La pregunta que dejó fue simple: ¿cuánta belleza pasa a nuestro "
        "lado sin que la notemos, solo porque no esperábamos encontrarla "
        "allí?"),
     "moraleja": "El valor de algo no siempre depende del lugar donde aparece.",
     "literal": "¿Cuántas personas se detuvieron a escuchar?",
     "inferencial": "¿Por qué casi nadie se detuvo, si era un músico famoso?",
     "critica": "¿Qué talentos podría haber en tu salón que nadie ha notado?"},

    {"titulo": "La papa que salvó al mundo", "tipo": "Texto informativo", "grado": 5,
     "texto": (
        "La papa nació en los Andes, hace más de siete mil años. Los "
        "antiguos peruanos la domesticaron y desarrollaron miles de "
        "variedades, adaptadas a distintas alturas y climas.\n"
        "También inventaron el chuño: congelaban la papa en la noche "
        "helada y la secaban al sol, logrando que durara años sin "
        "malograrse.\n"
        "Cuando la papa llegó a Europa, al principio la miraron con "
        "desconfianza. Con el tiempo se volvió alimento básico y ayudó a "
        "que millones de personas dejaran de pasar hambre.\n"
        "Hoy el Perú conserva más de tres mil variedades de papa nativa.\n"
        "Ese conocimiento no vino de un laboratorio: vino de los "
        "agricultores andinos."),
     "moraleja": "El conocimiento de nuestros pueblos tiene valor mundial.",
     "literal": "¿Qué es el chuño y para qué servía?",
     "inferencial": "¿Por qué el texto dice que la papa «salvó al mundo»?",
     "critica": "¿Qué otros saberes de tu comunidad merecerían ser valorados?"},

    {"titulo": "El puente de los monos", "tipo": "Cuento hindú", "grado": 5,
     "texto": (
        "Un grupo de monos vivía en un árbol de frutos dulces junto al río. "
        "Un rey los quiso cazar y llegó con sus arqueros.\n"
        "El jefe de los monos vio que sus compañeros no alcanzaban a saltar "
        "hasta el árbol de la otra orilla.\n"
        "Entonces se estiró él mismo entre las dos ramas, sujetándose con "
        "manos y pies, y formó un puente con su propio cuerpo.\n"
        "Todos los monos pasaron sobre él y se salvaron.\n"
        "Cuando el último cruzó, el jefe cayó agotado.\n"
        "El rey, conmovido, ordenó atenderlo y dijo a sus soldados:\n"
        "—Este animal me ha enseñado lo que es gobernar."),
     "moraleja": "El verdadero líder es el que sostiene a los demás.",
     "literal": "¿Cómo salvó el jefe a los otros monos?",
     "inferencial": "¿Qué aprendió el rey sobre gobernar?",
     "critica": "¿Cómo debería comportarse el delegado o brigadier de tu aula?"},

    {"titulo": "El vaso de agua", "tipo": "Reflexión", "grado": 6,
     "texto": (
        "Una maestra levantó un vaso con agua frente a su clase.\n"
        "—¿Cuánto pesa? —preguntó.\n"
        "Los estudiantes respondieron con distintos números.\n"
        "—El peso exacto no importa —dijo ella—. Importa cuánto tiempo lo "
        "sostengo. Si lo sostengo un minuto, no pasa nada. Si lo sostengo "
        "una hora, me dolerá el brazo. Si lo sostengo todo el día, no podré "
        "moverlo.\n"
        "El vaso pesa lo mismo siempre, pero mientras más tiempo lo cargo, "
        "más pesado se vuelve.\n"
        "—Las preocupaciones son iguales —terminó—. Piénsenlas, resuélvanlas, "
        "y suéltenlas antes de dormir."),
     "moraleja": "Cargar una preocupación demasiado tiempo la vuelve más pesada.",
     "literal": "¿Qué sostenía la maestra?",
     "inferencial": "¿Por qué el vaso se vuelve más pesado con el tiempo?",
     "critica": "¿Qué haces tú cuando una preocupación no te deja dormir?"},

    {"titulo": "Los tres albañiles", "tipo": "Reflexión", "grado": 6,
     "texto": (
        "Un viajero encontró a tres hombres colocando ladrillos bajo el sol.\n"
        "Al primero le preguntó qué hacía.\n"
        "—¿No lo ves? Pego ladrillos. Es un trabajo pesado y mal pagado.\n"
        "El segundo respondió:\n"
        "—Levanto un muro. Cuando termine, cobraré y me iré a casa.\n"
        "El tercero, sonriendo, dijo:\n"
        "—Estoy construyendo una catedral. Dentro de cien años la gente "
        "vendrá aquí a encontrarse.\n"
        "Los tres hacían exactamente lo mismo. Pero solo uno sabía para qué."),
     "moraleja": "El sentido que le damos a nuestro trabajo cambia su valor.",
     "literal": "¿Qué respondió el tercer albañil?",
     "inferencial": "¿Por qué el mismo trabajo tenía tres significados distintos?",
     "critica": "¿Para qué estudias tú? Responde como el tercer albañil."},

    {"titulo": "María Reiche y las líneas de Nazca", "tipo": "Biografía", "grado": 5,
     "texto": (
        "María Reiche llegó al Perú desde Alemania siendo joven. En el "
        "desierto de Nazca encontró unas líneas enormes trazadas sobre la "
        "tierra hace más de mil quinientos años.\n"
        "Nadie les daba importancia. Los camiones pasaban por encima y las "
        "iban borrando.\n"
        "María decidió estudiarlas. Vivió sola en una casita del desierto, "
        "con muy poco dinero, midiendo y dibujando cada figura durante "
        "décadas.\n"
        "Barría las líneas con una escoba para que no desaparecieran bajo "
        "la arena.\n"
        "Gracias a su insistencia, las líneas de Nazca fueron protegidas y "
        "hoy son Patrimonio de la Humanidad.\n"
        "Murió en el Perú, el país que eligió como suyo."),
     "moraleja": "Una sola persona constante puede salvar el patrimonio de todos.",
     "literal": "¿Con qué barría María Reiche las líneas?",
     "inferencial": "¿Por qué era importante que alguien las estudiara?",
     "critica": "¿Qué lugar o tradición de tu región merecería ser protegido?"},

    {"titulo": "El experimento de los malvaviscos", "tipo": "Texto informativo",
     "grado": 6,
     "texto": (
        "En los años sesenta, un investigador puso a niños de cuatro años "
        "frente a un malvavisco.\n"
        "Les dijo: «puedes comerlo ahora, o esperar quince minutos y te doy "
        "dos».\n"
        "Luego salía del cuarto.\n"
        "Algunos comían de inmediato. Otros se tapaban los ojos, cantaban o "
        "se daban vuelta para resistir.\n"
        "Años después se observó que quienes habían esperado tendían a "
        "obtener mejores resultados escolares.\n"
        "Estudios recientes matizaron la conclusión: influye también el "
        "entorno del niño y si aprendió que las promesas se cumplen.\n"
        "Pero algo quedó claro: saber esperar se puede entrenar."),
     "moraleja": "La capacidad de esperar no es un don: se practica.",
     "literal": "¿Qué debían hacer los niños para ganar dos malvaviscos?",
     "inferencial": "¿Por qué algunos niños se tapaban los ojos?",
     "critica": "¿Qué haces tú cuando quieres algo de inmediato y conviene esperar?"},

    {"titulo": "Los quipus, la escritura que no era letra",
     "tipo": "Texto informativo · Perú", "grado": 5,
     "texto": (
        "Los incas no usaban letras, pero sí registraban información: lo "
        "hacían con quipus, cuerdas con nudos de distintos colores.\n"
        "Cada nudo indicaba una cantidad según su forma y su posición. El "
        "color señalaba de qué se hablaba: maíz, papas, personas, tributos.\n"
        "Los quipucamayocs eran los especialistas encargados de leerlos y "
        "guardarlos.\n"
        "Manejaban un sistema de numeración decimal, igual que el nuestro.\n"
        "Muchos quipus fueron destruidos durante la Colonia.\n"
        "Hoy los investigadores siguen estudiando si algunos también "
        "registraban palabras y no solo números."),
     "moraleja": "Escribir no es solo usar letras: es guardar información para otros.",
     "literal": "¿Quiénes leían los quipus?",
     "inferencial": "¿Por qué el color de la cuerda era importante?",
     "critica": "Inventa un sistema de nudos para registrar tus notas del mes."},

    {"titulo": "La carta de la niña que no podía estudiar",
     "tipo": "Derechos y ciudadanía", "grado": 6,
     "texto": (
        "En muchas partes del mundo hay niñas que no van a la escuela porque "
        "deben trabajar, cuidar hermanos o porque su comunidad no lo "
        "considera necesario.\n"
        "Malala Yousafzai fue una de ellas. En su país prohibieron que las "
        "niñas estudiaran.\n"
        "Ella escribió un diario contando lo que ocurría, con otro nombre "
        "para protegerse.\n"
        "Cuando se supo quién era, un grupo armado le disparó camino a "
        "casa. Tenía quince años.\n"
        "Sobrevivió. Siguió hablando.\n"
        "A los diecisiete recibió el Premio Nobel de la Paz, el más joven de "
        "la historia."),
     "moraleja": "La educación es un derecho, y hay quienes arriesgan la vida por él.",
     "literal": "¿Por qué Malala escribía con otro nombre?",
     "inferencial": "¿Por qué su diario resultaba peligroso para algunos?",
     "critica": "¿Conoces a alguien que dejó de estudiar? ¿Por qué crees que fue?"},

    {"titulo": "El puente de cuerdas de Q'eswachaka",
     "tipo": "Texto informativo · Perú", "grado": 5,
     "texto": (
        "Cada junio, cuatro comunidades del Cusco se reúnen sobre el río "
        "Apurímac para rehacer un puente inca de cuerdas.\n"
        "Cortan y trenzan la paja ichu, la retuercen en sogas cada vez más "
        "gruesas y tienden el puente en tres días.\n"
        "El puente viejo se corta y cae al río. El nuevo queda listo.\n"
        "Nadie usa maquinaria. El conocimiento pasa de padres a hijos "
        "trabajando, no leyendo.\n"
        "En 2013 la UNESCO lo declaró Patrimonio Cultural Inmaterial de la "
        "Humanidad.\n"
        "Es el último puente inca de cuerdas que sigue en uso."),
     "moraleja": "Una tradición viva se conserva practicándola, no guardándola.",
     "literal": "¿Con qué material hacen el puente?",
     "inferencial": "¿Por qué se dice que el conocimiento pasa «trabajando, no leyendo»?",
     "critica": "¿Qué tradición de Chinchero se aprende haciendo? Descríbela."},

    {"titulo": "Por qué olvidamos lo que estudiamos",
     "tipo": "Aprender a aprender", "grado": 6,
     "texto": (
        "Un investigador midió cuánto recordamos con el paso de los días. "
        "Descubrió que olvidamos rápido: en 24 horas se pierde buena parte "
        "de lo estudiado.\n"
        "Pero encontró algo más útil: cada vez que repasamos, la curva del "
        "olvido baja más lento.\n"
        "Repasar el mismo día, luego a los tres días y luego a la semana "
        "hace que el recuerdo dure meses.\n"
        "Leer muchas veces seguidas no funciona igual: da la sensación de "
        "saber, pero no fija.\n"
        "Lo que sí fija es intentar recordar sin mirar el cuaderno, aunque "
        "cueste."),
     "moraleja": "Repasar espaciado y recordar sin mirar funciona mejor que releer.",
     "literal": "¿Cuánto se olvida en las primeras 24 horas?",
     "inferencial": "¿Por qué releer muchas veces «da la sensación de saber»?",
     "critica": "Diseña tu propio plan de repaso para el próximo examen."},

    {"titulo": "El niño que dibujaba mapas", "tipo": "Reflexión", "grado": 5,
     "texto": (
        "Un niño de un pueblo alejado dibujaba mapas en el suelo con un "
        "palo. Mapas de su comunidad, de los caminos, de los cerros.\n"
        "Sus compañeros se burlaban: «eso no sirve para nada».\n"
        "Un día llegó una brigada de salud que no encontraba el camino a los "
        "caseríos altos.\n"
        "El niño dibujó la ruta en una hoja: dónde estaba el río, dónde el "
        "puente caído, por dónde rodear.\n"
        "La brigada llegó a tiempo.\n"
        "Nadie volvió a decirle que sus mapas no servían."),
     "moraleja": "Lo que hoy parece inútil puede ser lo que mañana haga falta.",
     "literal": "¿Qué dibujaba el niño?",
     "inferencial": "¿Por qué sus mapas resultaron valiosos?",
     "critica": "¿Qué habilidad tuya crees que aún nadie ha valorado?"},
]


# ================================================================
# LECTURAS SECUNDARIA — VOCACIÓN, METAS Y VALORES
# ================================================================

LECTURAS_SECUNDARIA = [
    {"titulo": "El bambú japonés", "tipo": "Reflexión sobre el esfuerzo", "grado": 7,
     "texto": (
        "Cuando se siembra una semilla de bambú japonés, durante el primer "
        "año no ocurre nada visible. Tampoco en el segundo, ni en el "
        "tercero. Ni en el cuarto.\n"
        "El agricultor riega y cuida un terreno que parece vacío. Muchos "
        "abandonan en ese punto, convencidos de que la semilla estaba "
        "muerta.\n"
        "Pero en el quinto año, el bambú brota y crece hasta treinta metros "
        "en apenas seis semanas.\n"
        "¿Creció en seis semanas o en cinco años?\n"
        "Creció en cinco años. Durante todo ese tiempo estuvo construyendo "
        "bajo tierra un sistema de raíces capaz de sostener semejante "
        "altura.\n"
        "Sin esas raíces invisibles, el tallo se habría quebrado."),
     "moraleja": "Los resultados que se ven rápido casi siempre tienen años invisibles detrás.",
     "literal": "¿Cuánto tiempo pasa antes de que el bambú brote?",
     "inferencial": "¿Por qué el texto dice que el bambú creció en cinco años y no en seis semanas?",
     "critica": "¿En qué área de tu vida estás en el «periodo de raíces»? ¿Qué te costaría abandonar ahora?"},

    {"titulo": "El zapatero que quería ser médico", "tipo": "Orientación vocacional", "grado": 7,
     "texto": (
        "Un joven de un pueblo andino quería estudiar Medicina. Su familia "
        "tenía un taller de calzado y necesitaba sus manos.\n"
        "Trabajó de día y estudió de noche durante tres años. Postuló dos "
        "veces y no ingresó.\n"
        "La tercera vez cambió su método: en lugar de repasar todo, "
        "identificó los cursos donde perdía más puntos y los atacó primero.\n"
        "Ingresó.\n"
        "Años después volvió a su pueblo como médico. En su consultorio "
        "colgó, enmarcada, una herramienta del taller de su padre.\n"
        "Cuando le preguntaban por qué, respondía: «Para no olvidar de "
        "dónde vengo ni cuánto costó»."),
     "moraleja": "No basta con esforzarse: hay que esforzarse donde realmente hace falta.",
     "literal": "¿Qué cambió el joven en su tercer intento?",
     "inferencial": "¿Por qué colgó una herramienta del taller en su consultorio?",
     "critica": "¿Cuáles son tus dos cursos más débiles? ¿Qué harás distinto esta semana?"},

    {"titulo": "¿Qué se te da bien y qué te importa?", "tipo": "Orientación vocacional", "grado": 7,
     "texto": (
        "Elegir una carrera no es adivinar el futuro. Es responder con "
        "honestidad a cuatro preguntas.\n"
        "Primera: ¿qué se me da bien sin esfuerzo extraordinario? Aquello "
        "que otros me piden ayuda para hacer.\n"
        "Segunda: ¿qué me interesa tanto que investigo por mi cuenta, sin "
        "que nadie me lo pida?\n"
        "Tercera: ¿qué problema de mi comunidad me molesta lo suficiente "
        "como para querer resolverlo?\n"
        "Cuarta: ¿de qué puedo vivir dignamente en el lugar donde quiero "
        "estar?\n"
        "Donde esas cuatro respuestas se cruzan, aparece una vocación. Casi "
        "nunca es un rayo de inspiración: es un cruce que se descubre "
        "preguntando y probando."),
     "moraleja": "La vocación se construye respondiendo preguntas honestas, no esperando una señal.",
     "literal": "¿Cuántas preguntas propone el texto para elegir una carrera?",
     "inferencial": "¿Por qué no basta con elegir solo lo que se nos da bien?",
     "critica": "Responde por escrito las cuatro preguntas. ¿Qué carreras aparecen en el cruce?"},

    {"titulo": "Las cien mil formas de no hacerlo", "tipo": "Reflexión sobre el fracaso", "grado": 7,
     "texto": (
        "A Thomas Edison le preguntaron cómo se sentía tras miles de "
        "intentos fallidos por crear la bombilla eléctrica.\n"
        "Respondió que no había fracasado: había encontrado miles de "
        "maneras que no funcionaban, y cada una lo acercaba a la que sí.\n"
        "El detalle importante no es la frase, sino el método: Edison "
        "anotaba cada intento, qué material había usado y por qué había "
        "fallado.\n"
        "No repetía errores. Los archivaba.\n"
        "Un fracaso del que no se aprende nada se repite. Un fracaso "
        "analizado es información.\n"
        "La diferencia entre ambos no está en el resultado, sino en el "
        "cuaderno de notas."),
     "moraleja": "Un error analizado deja de ser un fracaso y se vuelve información.",
     "literal": "¿Qué hacía Edison después de cada intento fallido?",
     "inferencial": "¿Cuál es la diferencia entre un fracaso que se repite y uno que enseña?",
     "critica": "Piensa en tu último examen desaprobado. ¿Qué anotarías en un cuaderno como el de Edison?"},

    {"titulo": "El costo de la comparación", "tipo": "Salud emocional", "grado": 7,
     "texto": (
        "En las redes sociales vemos los mejores momentos de la vida de los "
        "demás: viajes, logros, celebraciones.\n"
        "Casi nunca vemos sus horas de estudio aburridas, sus dudas ni sus "
        "fracasos, porque eso no se publica.\n"
        "Comparar nuestro día completo con el momento más brillante de otro "
        "es una comparación tramposa desde el inicio.\n"
        "El problema no es admirar a alguien: admirar motiva. El problema "
        "es medirse contra una imagen incompleta y concluir que uno vale "
        "menos.\n"
        "Una comparación útil es contigo mismo: ¿sé más hoy que hace un "
        "mes? ¿Cumplí lo que me propuse esta semana?\n"
        "Esa competencia sí se puede ganar."),
     "moraleja": "La única comparación justa es con la persona que fuiste ayer.",
     "literal": "¿Qué no solemos ver en las redes sociales?",
     "inferencial": "¿Por qué el texto llama «tramposa» a esa comparación?",
     "critica": "¿Con quién te comparas seguido? ¿Qué sabes realmente de su esfuerzo diario?"},

    {"titulo": "El pescador y el empresario", "tipo": "Reflexión sobre el éxito", "grado": 7,
     "texto": (
        "Un empresario vio a un pescador que regresaba temprano con pocos "
        "peces.\n"
        "—Deberías pescar más horas —le dijo—. Con eso comprarías otra "
        "barca, luego una flota, después una fábrica. En veinte años serías "
        "rico.\n"
        "—¿Y después? —preguntó el pescador.\n"
        "—Después podrías retirarte, dormir hasta tarde, pescar un rato, "
        "jugar con tus hijos y compartir con tus amigos al atardecer.\n"
        "El pescador sonrió:\n"
        "—Eso es exactamente lo que hago hoy.\n"
        "El empresario no supo qué responder."),
     "moraleja": "Vale la pena preguntarse hacia dónde corremos antes de empezar a correr.",
     "literal": "¿Qué le propuso el empresario al pescador?",
     "inferencial": "¿Por qué el empresario no supo qué responder?",
     "critica": "¿Este relato justifica no esforzarse? Argumenta a favor y en contra."},

    {"titulo": "Un lugar en la mesa", "tipo": "Valores y ciudadanía", "grado": 7,
     "texto": (
        "En un aula, un estudiante nuevo se sentaba siempre solo. Hablaba "
        "distinto y traía otra comida.\n"
        "Nadie lo maltrataba. Simplemente nadie lo invitaba.\n"
        "Un día, una compañera movió su silla y le hizo espacio en su mesa. "
        "No dijo un discurso. Solo corrió la silla.\n"
        "Al mes siguiente, esa mesa era la más ruidosa del salón.\n"
        "Años después, él contó que ese gesto le cambió el año escolar.\n"
        "La exclusión no siempre grita. A veces es solo un espacio que "
        "nadie ofrece."),
     "moraleja": "Incluir no siempre exige grandes actos: a veces basta con hacer espacio.",
     "literal": "¿Qué hizo la compañera por el estudiante nuevo?",
     "inferencial": "¿Por qué el texto dice que «la exclusión no siempre grita»?",
     "critica": "¿Hay alguien en tu salón que suele quedarse solo? ¿Qué podrías hacer esta semana?"},

    {"titulo": "La beca de Ana", "tipo": "Orientación vocacional", "grado": 7,
     "texto": (
        "Ana quería estudiar Ingeniería, pero en su casa no había dinero "
        "para una universidad privada.\n"
        "Su tutora le dijo algo que la marcó: «Si no puedes pagar, tienes "
        "que informarte el doble».\n"
        "Ana investigó becas del Estado, concursos escolares, programas de "
        "las universidades públicas y requisitos de cada uno. Armó un "
        "cuaderno con fechas límite.\n"
        "Descubrió que varias becas exigían un promedio alto desde tercero "
        "de secundaria, algo que nadie le había dicho antes.\n"
        "Empezó a cuidar sus notas desde ese momento.\n"
        "Hoy estudia Ingeniería con beca completa. No fue suerte: fue "
        "información buscada a tiempo."),
     "moraleja": "La información buscada a tiempo abre puertas que el dinero no abre.",
     "literal": "¿Qué armó Ana para organizarse?",
     "inferencial": "¿Por qué era importante que cuidara sus notas desde tercero?",
     "critica": "¿Qué becas o concursos existen para estudiantes de tu región? Investiga y anota tres."},
]


# ================================================================
# 1° GRADO — LECTOESCRITURA
# ================================================================
# En 1° todavía se está consolidando la decodificación: vocales,
# sílabas y palabras cortas. Ponerles una fábula de 130 palabras es
# adelantarse. Estos textos usan sílabas directas y repetición para
# que el niño LEA, no adivine.

LECTOESCRITURA_1 = [
    {"titulo": "Mi mamá me ama", "tipo": "Sílabas con M", "grado": 0,
     "texto": (
        "Mi mamá me ama.\n"
        "Mi mamá amasa la masa.\n"
        "Memo mima a mi mamá.\n"
        "Memo y mamá comen mote.\n"
        "¡Qué rico el mote!"),
     "moraleja": "Sílabas trabajadas: ma · me · mi · mo · mu",
     "literal": "¿Qué amasa mi mamá?",
     "inferencial": "¿Quién mima a mamá?",
     "critica": "Encierra todas las sílabas «ma» que encuentres en el texto."},

    {"titulo": "El puma de Pepe", "tipo": "Sílabas con P", "grado": 0,
     "texto": (
        "Pepe pisa la pampa.\n"
        "Pepe ve un puma.\n"
        "El puma pasa. No pisa a Pepe.\n"
        "Pepe pide papa a su papá.\n"
        "Papá pela la papa para Pepe."),
     "moraleja": "Sílabas trabajadas: pa · pe · pi · po · pu",
     "literal": "¿Qué ve Pepe en la pampa?",
     "inferencial": "¿Por qué Pepe le pide papa a su papá?",
     "critica": "Escribe tres palabras nuevas que empiecen con «pa»."},

    {"titulo": "La lana de la llama", "tipo": "Sílabas con L", "grado": 0,
     "texto": (
        "La llama da lana.\n"
        "Lola lava la lana.\n"
        "La lana es suave.\n"
        "Lola le da la lana a su abuela.\n"
        "La abuela teje un lindo chullo."),
     "moraleja": "Sílabas trabajadas: la · le · li · lo · lu",
     "literal": "¿Qué hace Lola con la lana?",
     "inferencial": "¿Para qué sirve la lana de la llama?",
     "critica": "Dibuja lo que teje la abuela y escribe su nombre."},

    {"titulo": "El sol sale", "tipo": "Sílabas con S", "grado": 0,
     "texto": (
        "El sol sale. Sale el sol.\n"
        "Susi se asoma.\n"
        "Susi saluda al sol.\n"
        "El sol sube y sube.\n"
        "¡Sale el sol sobre el cerro!"),
     "moraleja": "Sílabas trabajadas: sa · se · si · so · su",
     "literal": "¿Quién saluda al sol?",
     "inferencial": "¿En qué momento del día ocurre el texto?",
     "critica": "Cuenta cuántas veces aparece la palabra «sol»."},

    {"titulo": "Tito toma su tacita", "tipo": "Sílabas con T", "grado": 0,
     "texto": (
        "Tito tiene una tacita.\n"
        "Tita le da té.\n"
        "Tito toma su té.\n"
        "El té está tibio.\n"
        "Tito y Tita toman juntos."),
     "moraleja": "Sílabas trabajadas: ta · te · ti · to · tu",
     "literal": "¿Qué toma Tito?",
     "inferencial": "¿Por qué el texto dice que el té está tibio y no caliente?",
     "critica": "Une con una línea: ta-za, te-cho, ti-za."},

    {"titulo": "Las vocales de mi cara", "tipo": "Vocales", "grado": 0,
     "texto": (
        "A de araña.\n"
        "E de estrella.\n"
        "I de iglesia.\n"
        "O de oso.\n"
        "U de uva.\n"
        "¡Ya sé mis cinco vocales!"),
     "moraleja": "Vocales trabajadas: a · e · i · o · u",
     "literal": "¿Con qué vocal empieza «oso»?",
     "inferencial": "¿Cuántas vocales hay en total?",
     "critica": "Busca en tu salón un objeto que empiece con cada vocal."},

    {"titulo": "Nino y su nido", "tipo": "Sílabas con N", "grado": 0,
     "texto": (
        "Nino mira un nido.\n"
        "En el nido hay un ave.\n"
        "El ave no se mueve.\n"
        "Nino no toca el nido.\n"
        "Nino cuida a la naturaleza."),
     "moraleja": "Sílabas trabajadas: na · ne · ni · no · nu",
     "literal": "¿Qué hay en el nido?",
     "inferencial": "¿Por qué Nino no toca el nido?",
     "critica": "¿Qué harías tú si vieras un nido con crías?"},

    {"titulo": "El dedo de Dani", "tipo": "Sílabas con D", "grado": 0,
     "texto": (
        "Dani da su dedo a su hermanita.\n"
        "La bebé lo agarra.\n"
        "Dani se ríe.\n"
        "La bebé no lo suelta.\n"
        "¡Dani y su hermanita se dan la mano!"),
     "moraleja": "Sílabas trabajadas: da · de · di · do · du",
     "literal": "¿Qué le da Dani a su hermanita?",
     "inferencial": "¿Por qué Dani se ríe?",
     "critica": "Cuenta algo que haces con tu hermano o hermana."},

    {"titulo": "El casco de Camila", "tipo": "Sílabas con C", "grado": 0,
     "texto": ("Camila come camote.\n"
               "Camila cuida su casa.\n"
               "En la casa hay una cama.\n"
               "Camila canta con su mamá.\n"
               "¡Qué linda canta Camila!"),
     "moraleja": "Sílabas trabajadas: ca · co · cu",
     "literal": "¿Qué come Camila?",
     "inferencial": "¿Con quién canta Camila?",
     "critica": "Escribe dos palabras más que empiecen con «ca»."},

    {"titulo": "Fefa y su foco", "tipo": "Sílabas con F", "grado": 0,
     "texto": ("Fefa tiene un foco.\n"
               "El foco da luz.\n"
               "Fefa lee con su foco.\n"
               "Su familia la mira.\n"
               "Fefa lee muy fuerte."),
     "moraleja": "Sílabas trabajadas: fa · fe · fi · fo · fu",
     "literal": "¿Qué tiene Fefa?",
     "inferencial": "¿Para qué usa Fefa el foco?",
     "critica": "Dibuja algo de tu casa que empiece con «fo»."},

    {"titulo": "El burro de Beto", "tipo": "Sílabas con B", "grado": 0,
     "texto": ("Beto tiene un burro.\n"
               "El burro es bueno.\n"
               "Beto le da un balde de agua.\n"
               "El burro bebe.\n"
               "Beto y su burro bajan al río."),
     "moraleja": "Sílabas trabajadas: ba · be · bi · bo · bu",
     "literal": "¿Qué le da Beto a su burro?",
     "inferencial": "¿Por qué el burro bebe agua?",
     "critica": "Encierra todas las «b» del texto."},

    {"titulo": "La vaca de Vito", "tipo": "Sílabas con V", "grado": 0,
     "texto": ("Vito ve una vaca.\n"
               "La vaca vive en el valle.\n"
               "Vito le da avena.\n"
               "La vaca no se va.\n"
               "Vito vuelve con su vaca."),
     "moraleja": "Sílabas trabajadas: va · ve · vi · vo · vu",
     "literal": "¿Dónde vive la vaca?",
     "inferencial": "¿Por qué la vaca no se va?",
     "critica": "Lee en voz alta: va-ca, va-lle, a-ve-na."},

    {"titulo": "El perro corre", "tipo": "Sonido fuerte R · RR", "grado": 0,
     "texto": ("El perro corre.\n"
               "Corre por el cerro.\n"
               "Rita ríe.\n"
               "El perro regresa.\n"
               "Rita y el perro corren juntos."),
     "moraleja": "Sonido fuerte: «rr» entre vocales, «r» al inicio de palabra",
     "literal": "¿Por dónde corre el perro?",
     "inferencial": "¿Por qué Rita ríe?",
     "critica": "Marca las palabras con «rr»: perro, cerro, corre."},

    {"titulo": "El niño y la piña", "tipo": "Sílabas con Ñ", "grado": 0,
     "texto": ("El niño tiene una piña.\n"
               "La piña es dulce.\n"
               "Toña le pide un poco.\n"
               "El niño le da la mitad.\n"
               "Toña y el niño comen la piña."),
     "moraleja": "Sílabas trabajadas: ña · ñe · ñi · ño · ñu",
     "literal": "¿Qué fruta tiene el niño?",
     "inferencial": "¿Por qué el niño le da la mitad a Toña?",
     "critica": "Escribe tu nombre y busca si tiene «ñ»."},

    {"titulo": "Chela y su chompa", "tipo": "Sílabas con CH", "grado": 0,
     "texto": ("Chela tiene una chompa.\n"
               "La chompa es de lana.\n"
               "Hace mucho frío en Chinchero.\n"
               "Chela se pone su chompa.\n"
               "Ahora Chela no tiene frío."),
     "moraleja": "Sílabas trabajadas: cha · che · chi · cho · chu",
     "literal": "¿De qué es la chompa de Chela?",
     "inferencial": "¿Por qué Chela se pone la chompa?",
     "critica": "Nombra tres cosas de lana que uses en tu casa."},

    {"titulo": "La gota gorda", "tipo": "Sílabas con G", "grado": 0,
     "texto": ("Cae una gota gorda.\n"
               "Gabi mira el agua.\n"
               "El gato se guarda.\n"
               "Gabi guarda su gorro.\n"
               "Ya no cae agua."),
     "moraleja": "Sílabas trabajadas: ga · go · gu · gue · gui",
     "literal": "¿Qué guarda Gabi?",
     "inferencial": "¿Por qué el gato se guarda?",
     "critica": "Lee: guan-te, gui-so, gue-rra."},

    {"titulo": "El jarro de Juana", "tipo": "Sílabas con J", "grado": 0,
     "texto": ("Juana tiene un jarro.\n"
               "En el jarro hay jugo.\n"
               "Juana juega con José.\n"
               "José toma jugo.\n"
               "Juana y José juegan juntos."),
     "moraleja": "Sílabas trabajadas: ja · je · ji · jo · ju",
     "literal": "¿Qué hay en el jarro?",
     "inferencial": "¿Qué hacen Juana y José?",
     "critica": "Escribe dos nombres que empiecen con «J»."},

    {"titulo": "El queso de Quique", "tipo": "Sílabas con QUE · QUI", "grado": 0,
     "texto": ("Quique quiere queso.\n"
               "Su mamá le da un poquito.\n"
               "Quique come el queso.\n"
               "Le queda un pedacito.\n"
               "Quique lo comparte con Quena."),
     "moraleja": "Sílabas trabajadas: que · qui (la «u» no suena)",
     "literal": "¿Qué quiere Quique?",
     "inferencial": "¿Qué hace Quique con el último pedacito?",
     "critica": "Lee en voz alta y comprueba que la «u» no se pronuncia."},

    {"titulo": "La llave de la lluvia", "tipo": "Sílabas con LL", "grado": 0,
     "texto": ("Llegó la lluvia.\n"
               "Yeni llama a su llama.\n"
               "La llama llega.\n"
               "Yeni cierra con llave.\n"
               "Ya no llueve."),
     "moraleja": "Sílabas trabajadas: lla · lle · lli · llo · llu",
     "literal": "¿A quién llama Yeni?",
     "inferencial": "¿Por qué Yeni cierra con llave?",
     "critica": "Busca las palabras con «ll» y cuéntalas."},

    {"titulo": "El zapato de Zoila", "tipo": "Sílabas con Z", "grado": 0,
     "texto": ("Zoila tiene un zapato.\n"
               "El zapato es azul.\n"
               "Zoila lo limpia.\n"
               "Su zapato quedó lindo.\n"
               "Zoila sale a la plaza."),
     "moraleja": "Sílabas trabajadas: za · zo · zu",
     "literal": "¿De qué color es el zapato?",
     "inferencial": "¿Por qué el zapato quedó lindo?",
     "critica": "Separa en sílabas: za-pa-to, a-zul, pla-za."},

    {"titulo": "El tren de Tere", "tipo": "Sílabas trabadas TR · PR · BR", "grado": 0,
     "texto": ("Tere ve un tren.\n"
               "El tren trae trigo.\n"
               "Bruno abre la puerta.\n"
               "Prende la luz.\n"
               "Tere y Bruno prueban el pan."),
     "moraleja": "Sílabas trabadas: tra · tre · pre · pro · bru",
     "literal": "¿Qué trae el tren?",
     "inferencial": "¿Por qué Bruno prende la luz?",
     "critica": "Lee despacio: tren, trigo, Bruno, prende, prueban."},

    {"titulo": "El plato de Blanca", "tipo": "Sílabas trabadas PL · BL · FL · CL", "grado": 0,
     "texto": ("Blanca pone la mesa.\n"
               "Saca un plato blanco.\n"
               "Hay flores en la mesa.\n"
               "Clara llega con pan.\n"
               "Blanca y Clara comen juntas."),
     "moraleja": "Sílabas trabadas: pla · bla · flo · cla",
     "literal": "¿De qué color es el plato?",
     "inferencial": "¿Para qué Blanca pone la mesa?",
     "critica": "Escribe tres palabras con «pl» o «bl»."},
]


# ================================================================
# ORTOGRAFÍA — 2° A 6° DE PRIMARIA
# ================================================================
# Cada ficha presenta un texto donde la regla aparece muchas veces,
# luego enuncia la regla y termina con un ejercicio de aplicación.
# Se aprende ortografía leyendo la palabra correcta muchas veces, no
# memorizando reglas sueltas.

ORTOGRAFIA = [
    {"titulo": "Uso de la B", "tipo": "Ortografía · B", "grado": 3,
     "texto": (
        "Beatriz caminaba por el bosque buscando bayas. Llevaba una bolsa "
        "blanca y un sombrero.\n"
        "Mientras subía, observaba las nubes. Iba silbando una canción que "
        "cantaba su abuela.\n"
        "De pronto tropezó con una raíz y estuvo a punto de caer, pero se "
        "sostuvo del tronco.\n"
        "—Debo tener cuidado —pensó—. Es mejor bajar despacio.\n"
        "Cuando volvió a su casa, su abuela ya había preparado el desayuno."),
     "moraleja": ("Se escribe con B: las terminaciones -aba, -abas, -ábamos "
                  "del pasado (caminaba, observaba); después de M (sombrero, "
                  "también); las palabras que empiezan con bu-, bur-, bus- "
                  "(buscar, burro); y los verbos terminados en -bir salvo "
                  "hervir, servir y vivir."),
     "literal": "¿Qué buscaba Beatriz en el bosque?",
     "inferencial": "¿Por qué decidió bajar despacio?",
     "critica": "Subraya en el texto seis palabras con B y clasifícalas según la regla."},

    {"titulo": "Uso de la V", "tipo": "Ortografía · V", "grado": 3,
     "texto": (
        "Víctor volvió al pueblo el viernes. Venía en un viejo camión que "
        "avanzaba lento por la curva.\n"
        "Vio los nevados a lo lejos y sintió que revivía.\n"
        "En la puerta lo esperaba su vecina Vilma con un vaso de chicha.\n"
        "—Bienvenido —le dijo—. Te vimos venir desde temprano.\n"
        "Víctor sonrió. Volver siempre valía la pena."),
     "moraleja": ("Se escribe con V: después de N (envío, invierno); las "
                  "palabras que empiezan con vice-, villa-, viva- ; los "
                  "adjetivos terminados en -ave, -avo, -eve, -ivo (suave, "
                  "octavo, breve, activo); y el pasado de andar, estar y "
                  "tener (anduve, estuve, tuve)."),
     "literal": "¿Quién esperaba a Víctor en la puerta?",
     "inferencial": "¿Por qué Víctor sintió que revivía al ver los nevados?",
     "critica": "Escribe cinco palabras con V que no aparezcan en el texto."},

    {"titulo": "¿B o V? Palabras que suenan igual", "tipo": "Ortografía · B/V",
     "grado": 4,
     "texto": (
        "En español, la B y la V suenan igual. Por eso hay que fijarse en el "
        "significado.\n"
        "Un **tubo** es un caño; **tuvo** es del verbo tener.\n"
        "**Bello** significa hermoso; **vello** es el pelo suave del cuerpo.\n"
        "**Botar** es lanzar algo; **votar** es elegir en una elección.\n"
        "**Bienes** son propiedades; **vienes** es del verbo venir.\n"
        "**Cabo** es un grado militar; **cavo** viene de cavar.\n"
        "Confundirlas cambia por completo lo que quisimos decir."),
     "moraleja": ("Palabras homófonas: suenan igual pero se escriben distinto "
                  "y significan cosas diferentes. La única forma de acertar "
                  "es entender el significado en la oración."),
     "literal": "¿Qué diferencia hay entre «botar» y «votar»?",
     "inferencial": "¿Por qué el texto dice que confundirlas cambia el mensaje?",
     "critica": "Escribe una oración con «tubo» y otra con «tuvo»."},

    {"titulo": "Uso de la G y la J", "tipo": "Ortografía · G/J", "grado": 4,
     "texto": (
        "El ingeniero llegó al colegio con una caja de herramientas.\n"
        "Traía un mensaje urgente para el director sobre el arreglo del "
        "techo.\n"
        "Los alumnos lo miraban con curiosidad mientras él dirigía el "
        "trabajo.\n"
        "—Es un trabajo delicado —explicó—. Hay que proteger la viga "
        "principal.\n"
        "Al día siguiente, el techo ya no goteaba y todos festejaron."),
     "moraleja": ("Se escribe con G: -ger, -gir (proteger, dirigir) salvo "
                  "tejer y crujir; las palabras con gen- (urgente, "
                  "inteligente); y geo- (geografía).\n"
                  "Se escribe con J: -aje, -eje (mensaje, hereje); el pasado "
                  "de decir y traer (dije, traje); y -jero, -jería "
                  "(extranjero, relojería)."),
     "literal": "¿Qué traía el ingeniero?",
     "inferencial": "¿Por qué festejaron al día siguiente?",
     "critica": "Clasifica: mensaje, urgente, dirigía, caja, colegio."},

    {"titulo": "Uso de la H muda", "tipo": "Ortografía · H", "grado": 4,
     "texto": (
        "Hoy hace mucho frío. Hilda hierve agua para el mate.\n"
        "Su hermano Hugo ha llegado del huerto con hierbas y habas.\n"
        "—¿Hay hueco en la olla? —pregunta.\n"
        "Hilda sonríe. Hace horas que lo espera.\n"
        "Los dos hermanos toman su mate junto a la cocina, mientras afuera "
        "el hielo cubre los techos."),
     "moraleja": ("La H no suena, pero cambia el significado. Se escribe con "
                  "H: todas las formas del verbo haber (he, has, ha, hay, "
                  "había); las palabras que empiezan con hie-, hue-, hia-, "
                  "hui- (hielo, huevo, hueco); y hosp-, herm-, hist-, horm- "
                  "(hospital, hermano, historia, hormiga)."),
     "literal": "¿Qué trajo Hugo del huerto?",
     "inferencial": "¿Cómo sabemos que hace mucho frío?",
     "critica": "Diferencia: «ha» (verbo haber), «a» (preposición), «ah» "
                "(exclamación). Escribe una oración con cada una."},

    {"titulo": "Uso de C, S y Z", "tipo": "Ortografía · C/S/Z", "grado": 5,
     "texto": (
        "La profesora explicaba con paciencia la lección de ciencias.\n"
        "Hablaba de la formación de los cerros y de la presión del aire en "
        "la altura.\n"
        "Los estudiantes tomaban apuntes en silencio, con la esperanza de "
        "entender.\n"
        "—La observación es la base de toda investigación —dijo.\n"
        "Al terminar la clase, varios se acercaron a hacer preguntas. Ella "
        "los felicitó por su curiosidad."),
     "moraleja": ("Con C: las terminaciones -ción cuando viene de una palabra "
                  "con -to o -do (canción, atención); los diminutivos -cito, "
                  "-cita (pancito).\n"
                  "Con S: las terminaciones -sión de palabras con -so, -sor "
                  "(presión, expresión); los adjetivos -oso, -osa (curioso); "
                  "y -ísimo (grandísimo).\n"
                  "Con Z: las terminaciones -anza y -eza (esperanza, "
                  "belleza)."),
     "literal": "¿Qué explicaba la profesora?",
     "inferencial": "¿Por qué felicitó a los estudiantes?",
     "critica": "Completa: aten__ión, pre__ión, espe__anza, curio__o, bell__a."},

    {"titulo": "La tilde y el acento", "tipo": "Ortografía · Tildación",
     "grado": 5,
     "texto": (
        "El camión subía por la carretera hacia el Cusco.\n"
        "El chófer llevaba café, azúcar y algunos árboles pequeños para "
        "sembrar.\n"
        "—¿Cuándo llegaremos? —preguntó un pasajero.\n"
        "—Después del mediodía —respondió él.\n"
        "La música sonaba bajito. Nadie hablaba. Solo se escuchaba el motor "
        "y el viento entre los eucaliptos."),
     "moraleja": ("Agudas: acento en la última sílaba; llevan tilde si "
                  "terminan en vocal, N o S (camión, café).\n"
                  "Graves: acento en la penúltima; llevan tilde si NO "
                  "terminan en vocal, N o S (árbol, azúcar).\n"
                  "Esdrújulas: acento en la antepenúltima; SIEMPRE llevan "
                  "tilde (música, sábado)."),
     "literal": "¿Qué llevaba el chófer en el camión?",
     "inferencial": "¿Cómo era el ambiente dentro del camión?",
     "critica": "Clasifica y tilda si corresponde: camion, arbol, musica, cafe, "
                "sabado, carretera."},

    {"titulo": "Mayúsculas y punto", "tipo": "Ortografía · Puntuación",
     "grado": 3,
     "texto": (
        "Mi nombre es Rosa Quispe. Vivo en Chinchero, provincia de Urubamba, "
        "en la región Cusco.\n"
        "Estudio en la I.E.P. Alternativo Yachay.\n"
        "Mi mejor amiga se llama Ana. Los sábados vamos juntas a la feria.\n"
        "En julio celebramos las Fiestas Patrias. El Perú es mi país.\n"
        "Cuando sea grande quiero conocer el río Amazonas."),
     "moraleja": ("Se escribe con mayúscula: al inicio de un texto y después "
                  "de punto; los nombres de personas, lugares e "
                  "instituciones (Rosa, Chinchero, Yachay).\n"
                  "NO llevan mayúscula: los días, los meses ni las "
                  "estaciones (sábado, julio, invierno)."),
     "literal": "¿Dónde vive Rosa?",
     "inferencial": "¿Por qué «julio» va con minúscula y «Fiestas Patrias» con mayúscula?",
     "critica": "Reescribe correctamente: «mi amiga ana vive en cusco y viaja en Julio»."},

    {"titulo": "La coma que cambia todo", "tipo": "Ortografía · Puntuación",
     "grado": 6,
     "texto": (
        "Una coma puede cambiar por completo el sentido de una oración.\n"
        "«Vamos a comer, niños» es una invitación.\n"
        "«Vamos a comer niños» es una amenaza.\n"
        "«No, espere» pide que se detenga.\n"
        "«No espere» pide lo contrario.\n"
        "La coma se usa para separar elementos de una lista, para llamar a "
        "alguien por su nombre y para encerrar aclaraciones.\n"
        "Un texto sin comas obliga al lector a adivinar."),
     "moraleja": ("La coma separa elementos de una enumeración, aísla el "
                  "vocativo (el nombre de quien nos escucha) y encierra "
                  "aclaraciones dentro de la oración."),
     "literal": "¿Qué diferencia hay entre las dos frases sobre comer?",
     "inferencial": "¿Por qué el texto dice que sin comas el lector debe adivinar?",
     "critica": "Coloca las comas: «compré papas maíz habas y quinua»."},

    {"titulo": "Palabras que se separan y palabras que no",
     "tipo": "Ortografía · Escritura", "grado": 6,
     "texto": (
        "Muchos errores vienen de unir o separar mal las palabras.\n"
        "**Porque** responde una causa: «no fui porque llovía».\n"
        "**Por qué** pregunta: «¿por qué no viniste?».\n"
        "**Porqué** es un sustantivo: «no entiendo el porqué».\n"
        "**También** significa además; **tan bien** indica de buena manera.\n"
        "**A ver** es mirar; **haber** es del verbo haber.\n"
        "**Sino** es una oposición; **si no** plantea una condición."),
     "moraleja": ("Unir o separar cambia la función de la palabra. Si dudas, "
                  "reemplaza mentalmente: si puedes decir «por cuál motivo», "
                  "va separado y con tilde."),
     "literal": "¿Qué significa «también»?",
     "inferencial": "¿Cómo puedes darte cuenta si va «por qué» o «porque»?",
     "critica": "Completa: «¿___ no viniste?» — «___ estaba enfermo»."},
]


# ================================================================
# CIENTÍFICOS Y CIENTÍFICAS — 4° A 6° Y SECUNDARIA
# ================================================================

CIENTIFICOS = [
    {"titulo": "Marie Curie y el brillo peligroso", "tipo": "Ciencia · Mujeres",
     "grado": 5,
     "texto": (
        "Marie Curie nació en Polonia, donde a las mujeres no se les permitía "
        "entrar a la universidad. Estudió en secreto, en clases clandestinas.\n"
        "En París vivió en un cuarto helado, comiendo pan y té para poder "
        "pagar sus estudios.\n"
        "Junto a su esposo Pierre, procesó toneladas de mineral en un galpón "
        "sin calefacción hasta aislar dos elementos nuevos: el polonio y el "
        "radio.\n"
        "Fue la primera mujer en ganar un Premio Nobel, y la única persona en "
        "ganarlo en dos ciencias distintas.\n"
        "Nunca patentó su descubrimiento: quería que la ciencia fuera de "
        "todos. Murió por la radiación que ella misma estudió."),
     "moraleja": "El conocimiento avanza cuando se comparte, no cuando se guarda.",
     "literal": "¿Qué dos elementos descubrió Marie Curie?",
     "inferencial": "¿Por qué se dice que estudió «en secreto»?",
     "critica": "¿Qué obstáculos enfrentan hoy las mujeres que quieren estudiar ciencia?"},

    {"titulo": "Katherine Johnson y los números que llevaron a la Luna",
     "tipo": "Ciencia · Mujeres", "grado": 6,
     "texto": (
        "Katherine Johnson calculaba trayectorias espaciales en la NASA "
        "cuando las computadoras recién empezaban a existir.\n"
        "Era una mujer afroamericana en los años sesenta: debía usar baños "
        "separados y comer aparte de sus colegas.\n"
        "Sus cálculos eran tan precisos que, antes del primer vuelo orbital "
        "de John Glenn, el astronauta pidió que ella revisara a mano los "
        "resultados de la computadora.\n"
        "«Si ella dice que están bien, entonces despego», dijo.\n"
        "Sus números también ayudaron a llevar el Apolo 11 a la Luna.\n"
        "Recibió el máximo honor civil de su país a los 97 años."),
     "moraleja": "El talento no depende del color de piel ni del género.",
     "literal": "¿Qué le pidió John Glenn antes de despegar?",
     "inferencial": "¿Por qué era extraordinario que ella trabajara en la NASA?",
     "critica": "¿Qué injusticias como esas siguen ocurriendo hoy?"},

    {"titulo": "Alexander Fleming y el error afortunado", "tipo": "Ciencia",
     "grado": 5,
     "texto": (
        "En 1928, Fleming se fue de vacaciones y dejó sus placas de cultivo "
        "sin lavar en el laboratorio.\n"
        "Al volver encontró un hongo creciendo en una de ellas. Alrededor del "
        "hongo, las bacterias habían desaparecido.\n"
        "Cualquier otro habría botado la placa. Fleming se detuvo a observar "
        "qué había pasado.\n"
        "Ese hongo producía una sustancia que mataba bacterias: la "
        "penicilina.\n"
        "El primer antibiótico de la historia ha salvado cientos de millones "
        "de vidas.\n"
        "El descubrimiento fue casual. La observación no lo fue."),
     "moraleja": "El azar favorece a la mente preparada para observar.",
     "literal": "¿Qué encontró Fleming al volver de vacaciones?",
     "inferencial": "¿Por qué el texto dice que el descubrimiento fue casual pero la observación no?",
     "critica": "¿Alguna vez descubriste algo por accidente? Cuéntalo."},

    {"titulo": "Jane Goodall y los chimpancés que usaban herramientas",
     "tipo": "Ciencia · Mujeres", "grado": 5,
     "texto": (
        "Jane Goodall llegó a Tanzania a los 26 años, sin título "
        "universitario, solo con un cuaderno y muchísima paciencia.\n"
        "Durante meses los chimpancés huían de ella. Se sentaba a la misma "
        "hora, en el mismo lugar, hasta que dejaron de temerle.\n"
        "Un día vio algo que cambió la ciencia: un chimpancé quitó las hojas "
        "de una rama y la usó para sacar termitas de un hueco.\n"
        "Hasta ese momento se creía que solo los humanos fabricaban "
        "herramientas.\n"
        "Su descubrimiento obligó a redefinir qué significa ser humano.\n"
        "Hoy, con más de 90 años, sigue viajando por el mundo defendiendo "
        "la naturaleza."),
     "moraleja": "La paciencia y la observación valen tanto como un laboratorio.",
     "literal": "¿Qué vio hacer al chimpancé?",
     "inferencial": "¿Por qué ese descubrimiento fue tan importante?",
     "critica": "¿Qué podrías aprender observando con paciencia en tu comunidad?"},

    {"titulo": "Pedro Paulet, el peruano que soñó con cohetes",
     "tipo": "Ciencia · Perú", "grado": 6,
     "texto": (
        "Pedro Paulet nació en Arequipa en 1874. De niño observaba los "
        "volcanes y se preguntaba cómo llegar más alto.\n"
        "Estudió en Europa y, en 1895, construyó un motor a reacción que "
        "funcionaba con combustible líquido.\n"
        "También diseñó el «avión torpedo», una nave con forma parecida a "
        "las naves espaciales que vendrían décadas después.\n"
        "Publicó sus ideas recién en 1927, cuando otros ya avanzaban en lo "
        "mismo.\n"
        "Wernher von Braun, creador de los cohetes que llevaron al hombre a "
        "la Luna, lo reconoció como pionero de la propulsión moderna.\n"
        "Muchos peruanos aún no saben quién fue."),
     "moraleja": "Del Perú también han salido ideas que cambiaron el mundo.",
     "literal": "¿Qué construyó Pedro Paulet en 1895?",
     "inferencial": "¿Por qué su nombre no es tan conocido como el de otros científicos?",
     "critica": "¿Por qué crees que se conocen poco los aportes peruanos a la ciencia?"},

    {"titulo": "Fabiola León-Velarde y la vida en la altura",
     "tipo": "Ciencia · Perú · Mujeres", "grado": 6,
     "texto": (
        "Fabiola León-Velarde se preguntó algo que nadie de afuera podía "
        "responder mejor que un peruano: ¿cómo hace el cuerpo humano para "
        "vivir a más de 4000 metros de altura?\n"
        "Estudió durante décadas a los pobladores andinos y descubrió cómo "
        "su sangre y sus pulmones se adaptan al poco oxígeno.\n"
        "También investigó el mal de montaña crónico, que afecta a miles de "
        "personas en los Andes.\n"
        "Sus estudios se usan hoy en todo el mundo, desde el Himalaya hasta "
        "la medicina deportiva.\n"
        "Llegó a ser rectora de una universidad y presidenta de Concytec.\n"
        "Investigó su propio territorio y lo convirtió en ciencia mundial."),
     "moraleja": "Los mejores temas de investigación suelen estar en casa.",
     "literal": "¿Qué estudió Fabiola León-Velarde?",
     "inferencial": "¿Por qué un peruano estaba en mejor posición para investigar esto?",
     "critica": "¿Qué pregunta científica podrías investigar sobre Chinchero?"},

    {"titulo": "Ada Lovelace, la primera programadora",
     "tipo": "Ciencia · Mujeres", "grado": 6,
     "texto": (
        "Ada Lovelace vivió en el siglo XIX, cuando a las mujeres se les "
        "enseñaba música y bordado, no matemática.\n"
        "Su madre insistió en que estudiara números para alejarla de la "
        "poesía de su padre, el poeta Lord Byron.\n"
        "Conoció a Charles Babbage, que diseñaba una máquina de calcular "
        "gigante.\n"
        "Ada escribió instrucciones paso a paso para esa máquina: el primer "
        "programa de la historia, casi cien años antes de la primera "
        "computadora real.\n"
        "Y entendió algo que ni Babbage había visto: la máquina no solo "
        "podría calcular números, también podría manejar música y símbolos.\n"
        "Imaginó la informática antes de que existiera."),
     "moraleja": "Imaginar lo que aún no existe también es hacer ciencia.",
     "literal": "¿Para qué máquina escribió Ada sus instrucciones?",
     "inferencial": "¿Qué entendió Ada que Babbage no había visto?",
     "critica": "¿Qué tecnología te gustaría que existiera dentro de 50 años?"},

    {"titulo": "Barbara McClintock y los genes que saltan",
     "tipo": "Ciencia · Mujeres", "grado": 6,
     "texto": (
        "Barbara McClintock estudiaba el maíz. Se preguntaba por qué algunos "
        "granos salían de colores distintos dentro de la misma mazorca.\n"
        "Tras años observando al microscopio, propuso algo que nadie creía: "
        "hay genes que se mueven de lugar dentro del cromosoma.\n"
        "Sus colegas la ignoraron. Algunos dijeron que estaba equivocada. "
        "Ella dejó de publicar, pero no dejó de investigar.\n"
        "Treinta años después, nuevas técnicas confirmaron que tenía razón.\n"
        "Recibió el Premio Nobel a los 81 años.\n"
        "El maíz, planta domesticada en América, le dio la clave."),
     "moraleja": "Tener razón antes de tiempo exige paciencia y convicción.",
     "literal": "¿Qué planta estudiaba Barbara McClintock?",
     "inferencial": "¿Por qué dejó de publicar sus hallazgos?",
     "critica": "¿Qué harías si nadie te creyera algo de lo que estás seguro?"},

    {"titulo": "María Rostworowski y la historia que faltaba",
     "tipo": "Ciencia · Perú · Mujeres", "grado": 6,
     "texto": (
        "María Rostworowski no estudió Historia en la universidad. Aprendió "
        "leyendo documentos coloniales por su cuenta.\n"
        "Se dio cuenta de que la historia del Perú antiguo se contaba casi "
        "solo desde los cronistas españoles.\n"
        "Ella buscó otras fuentes: juicios, testamentos y padrones donde "
        "hablaban los propios pobladores andinos.\n"
        "Así demostró que existían señoríos costeños poderosos antes de los "
        "incas, y que las mujeres andinas tenían derechos sobre la tierra.\n"
        "Escribió más de veinte libros y fundó un instituto de "
        "investigación.\n"
        "Cambió la forma en que el Perú se entiende a sí mismo."),
     "moraleja": "Una historia completa necesita escuchar todas las voces.",
     "literal": "¿Qué fuentes usó María Rostworowski?",
     "inferencial": "¿Por qué era un problema contar la historia solo desde los cronistas españoles?",
     "critica": "¿Qué historias de tu comunidad no están escritas en ningún libro?"},

    {"titulo": "Modesto Montoya y la ciencia que se explica",
     "tipo": "Ciencia · Perú", "grado": 6,
     "texto": (
        "Modesto Montoya nació en una familia humilde y estudió Física "
        "nuclear en Francia.\n"
        "Pudo quedarse allá con un buen sueldo, pero volvió al Perú, donde "
        "casi no había laboratorios ni presupuesto.\n"
        "Investigó la fisión nuclear y publicó trabajos reconocidos "
        "internacionalmente.\n"
        "Pero hizo algo igual de importante: organizó encuentros de ciencia "
        "para escolares y explicó física en programas de televisión y "
        "radio, con palabras sencillas.\n"
        "Decía que un país no avanza solo con científicos, sino con una "
        "población que entienda de ciencia."),
     "moraleja": "La ciencia que no se comunica se queda encerrada.",
     "literal": "¿Qué estudió Modesto Montoya en Francia?",
     "inferencial": "¿Por qué es importante que un científico sepa explicar?",
     "critica": "Explica a un compañero menor algo que hayas aprendido esta semana."},
]


# ================================================================
# ORGANIZACIÓN POR NIVEL
# ================================================================
# Antes todo era una sola lista y el docente terminaba imprimiendo las
# 20 fábulas aunque solo quisiera las de su grado. Ahora cada nivel es
# un conjunto propio.

LECTURAS_POR_NIVEL = {
    "1° de Primaria — Lectoescritura (sílabas y vocales)": LECTOESCRITURA_1,
    "1° y 2° de Primaria — Fábulas": FABULAS_1_2,
    "Ortografía (2° a 6°) — B, V, G, J, H, tildes": ORTOGRAFIA,
    "3° y 4° de Primaria — Leyendas y mitos": LECTURAS_3_4,
    "5° y 6° de Primaria — Textos para pensar": LECTURAS_5_6,
    "Secundaria — Vocación, metas y valores": LECTURAS_SECUNDARIA,
    "Científicos y científicas (5°, 6° y Secundaria)": CIENTIFICOS,
}


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

        _tt = str(L.get("tipo", "")).lower()
        if "ortografía" in _tt:
            _cab = "FICHA DE ORTOGRAFÍA"
        elif "sílabas" in _tt or "vocales" in _tt or "sonido" in _tt:
            _cab = "FICHA DE LECTOESCRITURA"
        else:
            _cab = "FICHA DE COMPRENSIÓN LECTORA"
        story.append(Paragraph(_cab, nota))
        story.append(Paragraph(L["titulo"].upper(), titulo))

        for parrafo in L["texto"].split("\n"):
            if parrafo.strip():
                story.append(Paragraph(parrafo.strip(), cuerpo))

        story.append(Spacer(1, 6))
        # La etiqueta cambia con el tipo de texto: una ficha de sílabas no
        # tiene "moraleja", y una biografía tiene idea central, no moraleja.
        _t = str(L.get("tipo", "")).lower()
        _txt_mor = str(L["moraleja"])
        if _txt_mor.lower().startswith(("sílabas trabajadas",
                                        "vocales trabajadas")):
            _etq = ""
        elif "ortografía" in _t:
            _etq = "<b>Regla ortográfica:</b> "
        elif (not _t) or any(k in _t for k in ("fábula", "leyenda", "mito",
                                               "cuento", "relato")):
            # Las fábulas base no llevan campo "tipo": por defecto, moraleja.
            _etq = "<b>Moraleja:</b> "
        else:
            _etq = "<b>Idea central:</b> "
        mor = Table([[Paragraph(_etq + _txt_mor, preg)]],
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
    st.subheader("📖 Fichas de Comprensión Lectora")
    st.caption("Fábulas, leyendas andinas, mitos del mundo y textos de "
               "reflexión, con preguntas de los tres niveles de comprensión "
               "del CNEB.")

    nivel = st.selectbox("Nivel:", list(LECTURAS_POR_NIVEL.keys()),
                         key="fp_nivel")
    lecturas_nivel = LECTURAS_POR_NIVEL[nivel]

    c1, c2 = st.columns(2)
    with c1:
        grado_txt = st.text_input("Grado y sección (se imprime en la ficha):",
                                  placeholder="3° A", key="fp_grado")
    with c2:
        tipos = sorted({L.get("tipo", "Lectura") for L in lecturas_nivel})
        tipo_sel = st.selectbox("Tipo de texto:", ["Todos"] + tipos,
                                key="fp_tipo")

    disponibles = (lecturas_nivel if tipo_sel == "Todos"
                   else [L for L in lecturas_nivel
                         if L.get("tipo") == tipo_sel])

    trab = st.checkbox("Incluir trabalenguas al pie de cada ficha",
                       value=nivel.startswith("1°"), key="fp_trab")

    st.markdown("##### Elige las lecturas a imprimir")
    titulos_disp = [L["titulo"] for L in disponibles]

    # Streamlit no permite reasignar la clave de un widget ya creado. Por eso
    # los botones de marcar/quitar guardan la selección en otra variable y
    # cambian el número de versión: al cambiar la clave, el multiselect se
    # vuelve a crear tomando ese valor como predeterminado.
    _ver = st.session_state.get("fp_ver", 0)
    _forzado = st.session_state.get("fp_forzado")
    if _forzado is None:
        _predet = titulos_disp[:1]
    else:
        _predet = [t for t in _forzado if t in titulos_disp]

    ct1, ct2 = st.columns(2)
    with ct1:
        if st.button(f"Marcar las {len(disponibles)} de este nivel",
                     use_container_width=True, key="fp_todas"):
            st.session_state["fp_forzado"] = list(titulos_disp)
            st.session_state["fp_ver"] = _ver + 1
            st.rerun()
    with ct2:
        if st.button("Quitar todas", use_container_width=True, key="fp_nada"):
            st.session_state["fp_forzado"] = []
            st.session_state["fp_ver"] = _ver + 1
            st.rerun()

    elegidas = st.multiselect(
        "Lecturas:", titulos_disp, default=_predet,
        key=f"fp_sel_{nivel}_{tipo_sel}_{_ver}",
        help="Se imprime solo lo que marques aquí. Cada lectura ocupa una "
             "hoja completa.")

    seleccion = [L for L in disponibles if L["titulo"] in elegidas]

    if not seleccion:
        st.warning("No has marcado ninguna lectura. Elige al menos una "
                   "para poder generar el PDF.")
        return

    st.info(f"**{len(seleccion)} ficha(s) seleccionada(s)** — el PDF tendrá "
            f"{len(seleccion)} hoja(s).")

    with st.expander("Ver una lectura antes de imprimir"):
        v = st.selectbox("Lectura:", [L["titulo"] for L in seleccion],
                         key="fp_prev")
        L = next(x for x in seleccion if x["titulo"] == v)
        st.markdown(f"### {L['titulo']}")
        st.caption(L.get("tipo", ""))
        st.write(L["texto"])
        st.success(f"**Idea central:** {L['moraleja']}")
        st.markdown(f"**1.** {L['literal']}  \n"
                    f"**2.** {L['inferencial']}  \n"
                    f"**3.** {L['critica']}")

    if st.button("📄 GENERAR FICHAS EN PDF", type="primary",
                 use_container_width=True, key="fp_gen"):
        try:
            st.session_state["fp_pdf"] = generar_ficha_pdf(
                seleccion, trab, grado_txt)
            st.session_state["fp_pdf_n"] = len(seleccion)
        except Exception as e:
            st.error(f"No se pudo generar: {e}")

    # El PDF se guarda en sesión: si no, al pulsar descargar la página se
    # recarga, el botón de generar vuelve a False y el archivo se pierde.
    if st.session_state.get("fp_pdf"):
        st.download_button(
            f"⬇️ Descargar {st.session_state['fp_pdf_n']} ficha(s)",
            data=st.session_state["fp_pdf"],
            file_name=f"fichas_{st.session_state['fp_pdf_n']}.pdf",
            mime="application/pdf", use_container_width=True, key="fp_dl")
        st.success("Imprime a doble cara para ahorrar papel: cada ficha "
                   "ocupa una carilla completa.")
