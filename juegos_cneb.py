# ================================================================
# APRENDO JUGANDO — INICIAL Y PRIMARIA
# I.E.P. ALTERNATIVO YACHAY
# ================================================================
"""Juegos interactivos alineados al CNEB para Inicial y Primaria.

Por qué HTML embebido y no controles de Streamlit: Streamlit vuelve a
ejecutar todo el script en cada clic, lo que produce un parpadeo de medio
segundo por respuesta. Para un niño de cinco años eso rompe el juego. El
motor va en HTML/JS dentro de un componente, así que responde al instante
y permite animaciones y sonido.

Integración en sistema_web.py:
    from juegos_cneb import tab_aprendo_jugando
"""

import json

import streamlit as st
import streamlit.components.v1 as components


# ================================================================
# 1. BANCO DE ACTIVIDADES
# ================================================================
# Tipos de ejercicio:
#   opcion    -> enunciado + emoji grande + opciones (1 correcta)
#   emparejar -> pares que el niño une tocando
#   ordenar   -> secuencia que debe tocarse en orden correcto
#
# Campo "d" = dificultad: 1 básico, 2 intermedio, 3 avanzado.
# El juego arranca siempre por lo básico y sube: si la primera actividad
# es la más difícil, el niño se frustra antes de entrar en confianza.

BANCO = {
    "Inicial (3 a 5 años)": {
        "Matemática": [
            {"tipo": "opcion", "emoji": "🍎🍎🍎", "d": 1, "pregunta": "¿Cuántas manzanas hay?",
             "opciones": ["2", "3", "4"], "correcta": "3"},
            {"tipo": "opcion", "emoji": "🐤🐤🐤🐤🐤", "d": 1, "pregunta": "¿Cuántos pollitos hay?",
             "opciones": ["4", "5", "6"], "correcta": "5"},
            {"tipo": "opcion", "emoji": "🐘  🐁", "d": 1, "pregunta": "¿Cuál es más grande?",
             "opciones": ["El elefante", "El ratón"], "correcta": "El elefante"},
            {"tipo": "opcion", "emoji": "🔴🔺", "d": 1, "pregunta": "¿Cuál es el círculo?",
             "opciones": ["🔴", "🔺"], "correcta": "🔴"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Toca los números del 1 al 5",
             "items": ["1", "2", "3", "4", "5"]},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une cada número con su cantidad",
             "pares": [["1", "⭐"], ["2", "⭐⭐"], ["3", "⭐⭐⭐"]]},
            {"tipo": "opcion", "emoji": "🟦🟦🟥🟦🟦", "d": 2, "pregunta": "¿Cuál es diferente?",
             "opciones": ["🟦", "🟥"], "correcta": "🟥"},
        ],
        "Comunicación": [
            {"tipo": "opcion", "emoji": "🐘", "d": 1, "pregunta": "¿Con qué vocal empieza «elefante»?",
             "opciones": ["A", "E", "I"], "correcta": "E"},
            {"tipo": "opcion", "emoji": "🦆", "d": 1, "pregunta": "¿Con qué vocal empieza «oso»?",
             "opciones": ["O", "U", "A"], "correcta": "O"},
            {"tipo": "opcion", "emoji": "☀️", "d": 2, "pregunta": "¿Con qué vocal empieza «sol»?",
             "opciones": ["O", "E", "I"], "correcta": "O"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la vocal con su dibujo",
             "pares": [["A", "🐝 abeja"], ["I", "⛪ iglesia"], ["U", "🍇 uvas"]]},
            {"tipo": "opcion", "emoji": "🐈  🎩", "d": 3, "pregunta": "¿Cuáles riman?",
             "opciones": ["gato y zapato", "gato y perro"], "correcta": "gato y zapato"},
        ],
        "Personal Social": [
            {"tipo": "opcion", "emoji": "😊", "d": 1, "pregunta": "¿Qué emoción es?",
             "opciones": ["Alegría", "Tristeza", "Enojo"], "correcta": "Alegría"},
            {"tipo": "opcion", "emoji": "😢", "d": 1, "pregunta": "¿Qué emoción es?",
             "opciones": ["Alegría", "Tristeza", "Miedo"], "correcta": "Tristeza"},
            {"tipo": "opcion", "emoji": "🙋", "d": 2, "pregunta": "¿Qué hago si quiero hablar en clase?",
             "opciones": ["Levanto la mano", "Grito"], "correcta": "Levanto la mano"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une cada parte con su nombre",
             "pares": [["👁️", "Ojos"], ["👂", "Orejas"], ["✋", "Manos"]]},
            {"tipo": "opcion", "emoji": "🧼💧", "d": 2, "pregunta": "¿Cuándo me lavo las manos?",
             "opciones": ["Antes de comer", "Nunca"], "correcta": "Antes de comer"},
        ],
        "Inglés": [
            {"tipo": "opcion", "emoji": "🔵", "d": 1, "pregunta": "¿Qué color es «blue»?",
             "opciones": ["🔵", "🔴", "🟡"], "correcta": "🔵"},
            {"tipo": "opcion", "emoji": "🟡", "d": 1, "pregunta": "¿Qué color es «yellow»?",
             "opciones": ["🟡", "🟢", "🔵"], "correcta": "🟡"},
            {"tipo": "opcion", "emoji": "🐱", "d": 1, "pregunta": "«Cat» es…",
             "opciones": ["Gato", "Perro"], "correcta": "Gato"},
            {"tipo": "opcion", "emoji": "☀️", "d": 1, "pregunta": "«Sun» es…",
             "opciones": ["Sol", "Luna"], "correcta": "Sol"},
            {"tipo": "opcion", "emoji": "✋", "d": 1, "pregunta": "¿Cómo dices «hola»?",
             "opciones": ["Hello", "Bye"], "correcta": "Hello"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el color con su nombre",
             "pares": [["🔴", "Red"], ["🟢", "Green"], ["🟡", "Yellow"]]},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el animal con su nombre",
             "pares": [["🐶", "Dog"], ["🐱", "Cat"], ["🐦", "Bird"]]},
            {"tipo": "ordenar", "d": 2, "pregunta": "Toca del 1 al 3 en inglés",
             "items": ["One", "Two", "Three"]},
            {"tipo": "opcion", "emoji": "👋", "d": 2, "pregunta": "¿Cómo te despides?",
             "opciones": ["Bye bye", "Hello"], "correcta": "Bye bye"},
            {"tipo": "emparejar", "d": 3, "pregunta": "Une la parte del cuerpo",
             "pares": [["👁️", "Eyes"], ["✋", "Hands"], ["👣", "Feet"]]},
        ],
        "Ciencia y Ambiente": [
            {"tipo": "opcion", "emoji": "🦙", "d": 1, "pregunta": "¿Qué animal es?",
             "opciones": ["Llama", "Vaca", "Perro"], "correcta": "Llama"},
            {"tipo": "opcion", "emoji": "🌱", "d": 2, "pregunta": "¿Qué necesita una planta para crecer?",
             "opciones": ["Agua y sol", "Solo piedras"], "correcta": "Agua y sol"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el animal con su casa",
             "pares": [["🐦", "Nido"], ["🐝", "Colmena"], ["🐕", "Casita"]]},
            {"tipo": "opcion", "emoji": "🚰", "d": 2, "pregunta": "¿Qué hago para cuidar el agua?",
             "opciones": ["Cierro el caño", "Dejo el caño abierto"],
             "correcta": "Cierro el caño"},
        ],
    },

    "Primaria 1° a 3°": {
        "Matemática": [
            {"tipo": "opcion", "emoji": "➕", "d": 1, "pregunta": "7 + 5 =",
             "opciones": ["11", "12", "13"], "correcta": "12"},
            {"tipo": "opcion", "emoji": "➖", "d": 1, "pregunta": "15 − 8 =",
             "opciones": ["6", "7", "8"], "correcta": "7"},
            {"tipo": "opcion", "emoji": "🧮", "d": 2, "pregunta": "¿Cuántas decenas hay en 40?",
             "opciones": ["4", "40", "14"], "correcta": "4"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena de menor a mayor",
             "items": ["12", "25", "38", "41", "57"]},
            {"d": 2, "tipo": "opcion", "emoji": "🍬", "pregunta":
             "Ana tenía 20 caramelos y regaló 6. ¿Cuántos le quedan?",
             "opciones": ["14", "16", "26"], "correcta": "14"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la operación con su resultado",
             "pares": [["3 × 4", "12"], ["10 − 6", "4"], ["5 + 9", "14"]]},
            {"tipo": "opcion", "emoji": "📏", "d": 3, "pregunta": "¿Cuál es mayor?",
             "opciones": ["1 metro", "50 centímetros"], "correcta": "1 metro"},
        ],
        "Comunicación": [
            {"tipo": "opcion", "emoji": "🔤", "d": 1, "pregunta": "¿Cuántas sílabas tiene «ventana»?",
             "opciones": ["2", "3", "4"], "correcta": "3"},
            {"tipo": "opcion", "emoji": "✏️", "d": 1, "pregunta": "¿Cuál se escribe con mayúscula?",
             "opciones": ["cusco", "Cusco"], "correcta": "Cusco"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena la oración",
             "items": ["Mi", "mamá", "prepara", "el", "desayuno"]},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une cada palabra con su sinónimo",
             "pares": [["Bonito", "Hermoso"], ["Rápido", "Veloz"], ["Feliz", "Alegre"]]},
            {"tipo": "opcion", "emoji": "🔁", "d": 1, "pregunta": "¿Cuál es lo contrario de «alto»?",
             "opciones": ["Bajo", "Grande", "Ancho"], "correcta": "Bajo"},
            {"d": 2, "tipo": "opcion", "emoji": "❓", "pregunta":
             "¿Qué signo va al final de: Cómo te llamas",
             "opciones": ["?", ".", "!"], "correcta": "?"},
        ],
        "Personal Social": [
            {"tipo": "opcion", "emoji": "🇵🇪", "d": 1, "pregunta": "¿Cuáles son los colores de la bandera del Perú?",
             "opciones": ["Rojo y blanco", "Azul y blanco"], "correcta": "Rojo y blanco"},
            {"tipo": "opcion", "emoji": "🏔️", "d": 1, "pregunta": "¿En qué región está Chinchero?",
             "opciones": ["Cusco", "Lima", "Piura"], "correcta": "Cusco"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la región con su paisaje",
             "pares": [["Costa", "🏖️ Desierto y mar"], ["Sierra", "⛰️ Montañas"],
                       ["Selva", "🌳 Bosques y ríos"]]},
            {"tipo": "opcion", "emoji": "🤝", "d": 1, "pregunta": "¿Qué hago si un compañero se cae?",
             "opciones": ["Lo ayudo a levantarse", "Me río"],
             "correcta": "Lo ayudo a levantarse"},
            {"tipo": "opcion", "emoji": "📜", "d": 2, "pregunta": "Todos los niños tienen derecho a...",
             "opciones": ["Estudiar", "Trabajar todo el día"], "correcta": "Estudiar"},
        ],
        "Ciencia y Ambiente": [
            {"tipo": "opcion", "emoji": "💧", "d": 1, "pregunta": "¿En qué estado está el hielo?",
             "opciones": ["Sólido", "Líquido", "Gaseoso"], "correcta": "Sólido"},
            {"tipo": "opcion", "emoji": "👅", "d": 1, "pregunta": "¿Con qué sentido probamos la comida?",
             "opciones": ["Gusto", "Vista", "Oído"], "correcta": "Gusto"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el ser vivo con su grupo",
             "pares": [["🌻 Girasol", "Planta"], ["🐟 Pez", "Animal"], ["🍄 Hongo", "Hongo"]]},
            {"tipo": "opcion", "emoji": "🥦", "d": 1, "pregunta": "¿Cuál es un alimento saludable?",
             "opciones": ["Brócoli", "Gaseosa"], "correcta": "Brócoli"},
            {"tipo": "opcion", "emoji": "♻️", "d": 2, "pregunta": "¿Dónde va una botella de plástico?",
             "opciones": ["Tacho de reciclaje", "Al río"],
             "correcta": "Tacho de reciclaje"},
        ],
        "Inglés": [
            {"tipo": "opcion", "emoji": "🔴", "d": 1, "pregunta": "¿Cómo se dice «rojo»?",
             "opciones": ["Red", "Blue", "Green"], "correcta": "Red"},
            {"tipo": "opcion", "emoji": "🐕", "d": 1, "pregunta": "¿Cómo se dice «perro»?",
             "opciones": ["Dog", "Cat", "Bird"], "correcta": "Dog"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la palabra con su significado",
             "pares": [["Mother", "Mamá"], ["Father", "Papá"], ["Sister", "Hermana"]]},
            {"tipo": "ordenar", "d": 2, "pregunta": "Toca los números en inglés del 1 al 5",
             "items": ["One", "Two", "Three", "Four", "Five"]},
            {"tipo": "opcion", "emoji": "👋", "d": 2, "pregunta": "¿Cómo saludas en la mañana?",
             "opciones": ["Good morning", "Good night"], "correcta": "Good morning"},
            {"tipo": "opcion", "emoji": "🍎", "d": 1, "pregunta": "¿Cómo se dice «manzana»?",
             "opciones": ["Apple", "Banana", "Orange"], "correcta": "Apple"},
            {"tipo": "opcion", "emoji": "🏠", "d": 1, "pregunta": "«House» significa…",
             "opciones": ["Casa", "Escuela"], "correcta": "Casa"},
            {"tipo": "opcion", "emoji": "📕", "d": 1, "pregunta": "¿Cómo se dice «libro»?",
             "opciones": ["Book", "Pen", "Bag"], "correcta": "Book"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el útil escolar",
             "pares": [["Pencil", "Lápiz"], ["Notebook", "Cuaderno"],
                       ["Eraser", "Borrador"]]},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el animal de la granja",
             "pares": [["Cow", "Vaca"], ["Horse", "Caballo"], ["Duck", "Pato"]]},
            {"tipo": "opcion", "emoji": "🎂", "d": 2, "pregunta":
             "«How old are you?» pregunta por…",
             "opciones": ["Tu edad", "Tu nombre"], "correcta": "Tu edad"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Toca del 6 al 10 en inglés",
             "items": ["Six", "Seven", "Eight", "Nine", "Ten"]},
            {"tipo": "opcion", "emoji": "❓", "d": 3, "pregunta":
             "«My name is Ana» significa…",
             "opciones": ["Mi nombre es Ana", "Tengo un nombre"],
             "correcta": "Mi nombre es Ana"},
            {"tipo": "emparejar", "d": 3, "pregunta": "Une el color con el objeto",
             "pares": [["The sun is", "Yellow"], ["The grass is", "Green"],
                       ["The sky is", "Blue"]]},
        ],
    },

    "Primaria 4° a 6°": {
        "Matemática": [
            {"tipo": "opcion", "emoji": "✖️", "d": 1, "pregunta": "7 × 8 =",
             "opciones": ["54", "56", "64"], "correcta": "56"},
            {"tipo": "opcion", "emoji": "🍕", "d": 2, "pregunta": "¿Qué fracción es mayor?",
             "opciones": ["1/2", "1/4", "1/8"], "correcta": "1/2"},
            {"d": 2, "tipo": "opcion", "emoji": "⬛", "pregunta":
             "Perímetro de un cuadrado de lado 6 cm:",
             "opciones": ["24 cm", "36 cm", "12 cm"], "correcta": "24 cm"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena de menor a mayor",
             "items": ["1/8", "1/4", "1/2", "3/4", "1"]},
            {"tipo": "emparejar", "d": 3, "pregunta": "Une la fracción con su decimal",
             "pares": [["1/2", "0,5"], ["1/4", "0,25"], ["3/4", "0,75"]]},
            {"d": 2, "tipo": "opcion", "emoji": "💰", "pregunta":
             "Un cuaderno cuesta S/ 4,50. ¿Cuánto cuestan 3?",
             "opciones": ["S/ 13,50", "S/ 12,00", "S/ 14,50"], "correcta": "S/ 13,50"},
        ],
        "Comunicación": [
            {"d": 1, "tipo": "opcion", "emoji": "📝", "pregunta":
             "En «El perro corre rápido», ¿cuál es el verbo?",
             "opciones": ["Corre", "Perro", "Rápido"], "correcta": "Corre"},
            {"tipo": "opcion", "emoji": "🔠", "d": 1, "pregunta": "¿Cuál lleva tilde?",
             "opciones": ["Camión", "Camion"], "correcta": "Camión"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la palabra con su clase",
             "pares": [["Cusco", "Sustantivo propio"], ["Hermoso", "Adjetivo"],
                       ["Caminar", "Verbo"]]},
            {"d": 2, "tipo": "opcion", "emoji": "🔗", "pregunta":
             "Estudié mucho ______ aprobé el examen.",
             "opciones": ["por eso", "aunque"], "correcta": "por eso"},
            {"d": 2, "tipo": "opcion", "emoji": "📖", "pregunta":
             "¿Cómo se llama la idea más importante de un texto?",
             "opciones": ["Idea principal", "Título", "Párrafo"],
             "correcta": "Idea principal"},
        ],
        "Personal Social": [
            {"tipo": "opcion", "emoji": "🏛️", "d": 1, "pregunta": "¿Cuál fue la capital del Tahuantinsuyo?",
             "opciones": ["Cusco", "Lima", "Cajamarca"], "correcta": "Cusco"},
            {"d": 2, "tipo": "opcion", "emoji": "🗳️", "pregunta":
             "¿Quién elige al Presidente del Perú?",
             "opciones": ["Los ciudadanos", "El Congreso"], "correcta": "Los ciudadanos"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la cultura con su región",
             "pares": [["Inca", "Cusco"], ["Chavín", "Áncash"], ["Nazca", "Ica"]]},
            {"tipo": "ordenar", "d": 3, "pregunta": "Ordena las etapas de la historia del Perú",
             "items": ["Culturas preincas", "Imperio inca", "Conquista",
                       "Virreinato", "República"]},
            {"d": 2, "tipo": "opcion", "emoji": "⚖️", "pregunta":
             "¿Qué poder del Estado hace las leyes?",
             "opciones": ["Legislativo", "Ejecutivo", "Judicial"],
             "correcta": "Legislativo"},
        ],
        "Ciencia y Ambiente": [
            {"tipo": "opcion", "emoji": "🫁", "d": 1, "pregunta": "¿Qué órgano permite respirar?",
             "opciones": ["Pulmones", "Estómago", "Riñones"], "correcta": "Pulmones"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena la cadena alimenticia",
             "items": ["🌿 Pasto", "🐄 Vaca", "🐆 Puma"]},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el sistema con su función",
             "pares": [["Digestivo", "Procesa los alimentos"],
                       ["Circulatorio", "Transporta la sangre"],
                       ["Nervioso", "Controla el cuerpo"]]},
            {"d": 2, "tipo": "opcion", "emoji": "🌡️", "pregunta":
             "¿Cómo se llama el paso de líquido a gas?",
             "opciones": ["Evaporación", "Condensación", "Solidificación"],
             "correcta": "Evaporación"},
            {"d": 3, "tipo": "opcion", "emoji": "🌎", "pregunta":
             "¿Qué causa el calentamiento global?",
             "opciones": ["Gases de efecto invernadero", "La lluvia"],
             "correcta": "Gases de efecto invernadero"},
        ],
        "Inglés": [
            {"tipo": "opcion", "emoji": "🕐", "d": 1, "pregunta": "What time is it? (1:00)",
             "opciones": ["One o'clock", "Two o'clock"], "correcta": "One o'clock"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une el verbo con su significado",
             "pares": [["To eat", "Comer"], ["To run", "Correr"], ["To read", "Leer"]]},
            {"tipo": "opcion", "emoji": "🏫", "d": 1, "pregunta": "«I go to school» significa:",
             "opciones": ["Voy al colegio", "Vivo en el colegio"],
             "correcta": "Voy al colegio"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena los días de la semana",
             "items": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]},
            {"tipo": "opcion", "emoji": "🌦️", "d": 1, "pregunta": "How is the weather? ☀️",
             "opciones": ["It's sunny", "It's rainy"], "correcta": "It's sunny"},
            {"tipo": "opcion", "emoji": "👧", "d": 1, "pregunta":
             "«She is my sister» significa…",
             "opciones": ["Ella es mi hermana", "Él es mi hermano"],
             "correcta": "Ella es mi hermana"},
            {"tipo": "emparejar", "d": 2, "pregunta": "Une la profesión",
             "pares": [["Teacher", "Profesor"], ["Doctor", "Médico"],
                       ["Farmer", "Agricultor"]]},
            {"tipo": "opcion", "emoji": "🍽️", "d": 2, "pregunta":
             "«I have breakfast at 7» significa…",
             "opciones": ["Desayuno a las 7", "Ceno a las 7"],
             "correcta": "Desayuno a las 7"},
            {"tipo": "ordenar", "d": 2, "pregunta": "Ordena los meses del año",
             "items": ["January", "February", "March", "April", "May"]},
            {"tipo": "opcion", "emoji": "📍", "d": 2, "pregunta":
             "«Where do you live?» pregunta por…",
             "opciones": ["Dónde vives", "Qué haces"], "correcta": "Dónde vives"},
            {"tipo": "ordenar", "d": 3, "pregunta": "Ordena la oración en inglés",
             "items": ["I", "study", "English", "every", "day"]},
            {"tipo": "opcion", "emoji": "⏳", "d": 3, "pregunta": "¿Cuál está en pasado?",
             "opciones": ["I played football", "I play football"],
             "correcta": "I played football"},
            {"tipo": "emparejar", "d": 3, "pregunta": "Une el verbo con su pasado",
             "pares": [["Go", "Went"], ["Eat", "Ate"], ["See", "Saw"]]},
        ],
    },
}


# ================================================================
# 2. MOTOR DEL JUEGO
# ================================================================

_HTML = r"""
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">
<style>
:root{
  /* Paleta tomada de los tejidos de Chinchero */
  --tela:#FDFBF7; --indigo:#1B3A94; --carmesi:#C1272D; --maiz:#F2A900;
  --jade:#0E9F8E; --fucsia:#C13D8C; --tinta:#22252B; --humo:#6B7280;
  --exito:#16A34A; --error:#DC2626;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Nunito',system-ui,sans-serif;background:var(--tela);
  color:var(--tinta);padding:14px;-webkit-tap-highlight-color:transparent}
.marco{max-width:760px;margin:0 auto}

/* --- Faja andina: la barra de progreso se teje --- */
.faja{display:flex;gap:3px;height:22px;border-radius:11px;overflow:hidden;
  background:#E8E3DA;padding:3px}
.hilo{flex:1;border-radius:6px;background:#D6D0C6;transition:background .35s ease,transform .35s ease}
.hilo.on{transform:scaleY(1.0)}
.barra-top{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.vidas{font-size:1.35rem;letter-spacing:2px;white-space:nowrap}
.marcador{font-weight:900;color:var(--indigo);font-size:1rem;white-space:nowrap}

.tarjeta{background:#fff;border-radius:22px;padding:26px 22px;
  box-shadow:0 6px 0 #E4DED4,0 12px 30px rgba(0,0,0,.07);text-align:center}
.nivelchip{display:inline-block;background:#F3F0EA;color:var(--humo);
  border-radius:999px;padding:4px 14px;font-size:.8rem;font-weight:900;
  letter-spacing:.5px;margin-bottom:10px}
.subenivel{background:linear-gradient(90deg,var(--maiz),var(--carmesi));
  color:#fff;border-radius:14px;padding:12px;font-weight:900;
  margin-bottom:14px;animation:sube .3s ease}
.emoji{font-size:3.6rem;line-height:1.2;margin-bottom:10px}
.pregunta{font-size:1.35rem;font-weight:900;margin-bottom:20px;line-height:1.35}

.ops{display:grid;gap:12px}
.op{background:#fff;border:3px solid #E4DED4;border-radius:16px;
  padding:16px 18px;font-size:1.15rem;font-weight:700;cursor:pointer;
  font-family:inherit;transition:transform .12s,border-color .15s,background .15s;
  box-shadow:0 4px 0 #E4DED4}
.op:hover{border-color:var(--indigo);transform:translateY(-2px)}
.op:active{transform:translateY(2px);box-shadow:0 1px 0 #E4DED4}
.op.ok{border-color:var(--exito);background:#E9FBEF;box-shadow:0 4px 0 #A7E9BC}
.op.mal{border-color:var(--error);background:#FDECEC;box-shadow:0 4px 0 #F3B7B7}
.op.sel{border-color:var(--indigo);background:#EEF2FF}
.op:disabled{cursor:default}

.pares{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.orden-zona{min-height:56px;display:flex;flex-wrap:wrap;gap:8px;
  justify-content:center;padding:10px;border-radius:14px;background:#F3F0EA;
  margin-bottom:12px}
.pill{background:var(--indigo);color:#fff;border-radius:12px;padding:8px 14px;
  font-weight:700}

.aviso{margin-top:16px;border-radius:14px;padding:14px;font-weight:700;
  font-size:1.05rem;display:none}
.aviso.ver{display:block;animation:sube .25s ease}
.aviso.bien{background:#E9FBEF;color:#12703A}
.aviso.mal{background:#FDECEC;color:#9B1C1C}
@keyframes sube{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

.btn{margin-top:16px;width:100%;border:none;border-radius:16px;padding:15px;
  font-family:inherit;font-size:1.1rem;font-weight:900;color:#fff;
  background:var(--indigo);cursor:pointer;box-shadow:0 5px 0 #14286B}
.btn:active{transform:translateY(3px);box-shadow:0 2px 0 #14286B}
.btn.verde{background:var(--exito);box-shadow:0 5px 0 #0F7434}

.final{text-align:center;padding:30px 16px}
.final h2{font-size:2rem;color:var(--indigo);margin-bottom:6px}
.final .puntos{font-size:3.4rem;font-weight:900;color:var(--maiz);margin:8px 0}
.sello{font-size:4rem;margin-bottom:6px}
.chispa{position:fixed;font-size:1.6rem;pointer-events:none;animation:cae 1.1s linear forwards}
@keyframes cae{to{transform:translateY(90vh) rotate(360deg);opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media(max-width:520px){.pares{grid-template-columns:1fr}.emoji{font-size:2.8rem}}
</style></head><body>
<div class="marco">
  <div class="barra-top">
    <div class="vidas" id="vidas"></div>
    <div class="faja" id="faja" style="flex:1"></div>
    <div class="marcador" id="marcador">0</div>
  </div>
  <div id="zona"></div>
</div>
<script>
const EJ = __DATOS__;
const COLORES = ['#C1272D','#F2A900','#0E9F8E','#1B3A94','#C13D8C'];
let i=0, aciertos=0, vidas=3, bloqueado=false, seleccion=null, orden=[];

const $ = id => document.getElementById(id);

function pintarBarra(){
  $('faja').innerHTML = EJ.map((_,k)=>
    `<div class="hilo ${k<i?'on':''}" style="background:${k<i?COLORES[k%5]:'#D6D0C6'}"></div>`
  ).join('');
  $('vidas').textContent = '❤️'.repeat(vidas) + '🤍'.repeat(3-vidas);
  $('marcador').textContent = aciertos;
}

function chispas(){
  for(let k=0;k<18;k++){
    const s=document.createElement('div');
    s.className='chispa';
    s.textContent=['🎉','⭐','✨','🌟'][k%4];
    s.style.left=Math.random()*100+'vw';
    s.style.top='-40px';
    s.style.animationDelay=(Math.random()*.4)+'s';
    document.body.appendChild(s);
    setTimeout(()=>s.remove(),1600);
  }
}

function aviso(ok,txt){
  const a=document.createElement('div');
  a.className='aviso ver '+(ok?'bien':'mal');
  a.textContent=txt;
  $('zona').querySelector('.tarjeta').appendChild(a);
}

function siguiente(){
  i++; seleccion=null; orden=[]; bloqueado=false;
  if(vidas<=0 || i>=EJ.length){ final(); } else { render(); }
  pintarBarra();
}

function botonSeguir(){
  const b=document.createElement('button');
  b.className='btn verde'; b.textContent='Continuar';
  b.onclick=siguiente;
  $('zona').querySelector('.tarjeta').appendChild(b);
}

function acertar(){ aciertos++; pintarBarra(); chispas();
  aviso(true,'¡Muy bien! 🎉'); botonSeguir(); }
function fallar(msg){ vidas--; aviso(false,msg); pintarBarra(); botonSeguir(); }

const ETIQ = {1:'⭐ BÁSICO', 2:'⭐⭐ INTERMEDIO', 3:'⭐⭐⭐ AVANZADO'};

function render(){
  const e = EJ[i];
  const z = $('zona');
  z.innerHTML = '';
  const t = document.createElement('div'); t.className='tarjeta';

  // Aviso solo cuando la dificultad sube respecto a la anterior:
  // el niño necesita saber que el juego se puso más exigente.
  const dAct = e.d || 1;
  const dAnt = i>0 ? (EJ[i-1].d || 1) : 0;
  if(i>0 && dAct>dAnt){
    const s=document.createElement('div'); s.className='subenivel';
    s.textContent='¡Subiste de nivel! Ahora '+ETIQ[dAct];
    t.appendChild(s);
  }
  const chip=document.createElement('div'); chip.className='nivelchip';
  chip.textContent=ETIQ[dAct]; t.appendChild(chip);

  if(e.emoji){ const em=document.createElement('div'); em.className='emoji';
    em.textContent=e.emoji; t.appendChild(em); }
  const p=document.createElement('div'); p.className='pregunta';
  p.textContent=e.pregunta; t.appendChild(p);

  if(e.tipo==='opcion'){
    const c=document.createElement('div'); c.className='ops';
    const ops=[...e.opciones].sort(()=>Math.random()-.5);
    ops.forEach(o=>{
      const b=document.createElement('button'); b.className='op'; b.textContent=o;
      b.onclick=()=>{
        if(bloqueado) return; bloqueado=true;
        c.querySelectorAll('.op').forEach(x=>x.disabled=true);
        if(o===e.correcta){ b.classList.add('ok'); acertar(); }
        else{ b.classList.add('mal');
          c.querySelectorAll('.op').forEach(x=>{
            if(x.textContent===e.correcta) x.classList.add('ok'); });
          fallar('La respuesta correcta es: '+e.correcta); }
      };
      c.appendChild(b);
    });
    t.appendChild(c);
  }

  if(e.tipo==='emparejar'){
    const izq=e.pares.map(x=>x[0]);
    const der=[...e.pares.map(x=>x[1])].sort(()=>Math.random()-.5);
    let hechos=0;
    const g=document.createElement('div'); g.className='pares';
    const colI=document.createElement('div'); colI.className='ops';
    const colD=document.createElement('div'); colD.className='ops';
    izq.forEach(v=>{ const b=document.createElement('button');
      b.className='op'; b.textContent=v; b.dataset.v=v;
      b.onclick=()=>{ if(b.disabled) return;
        colI.querySelectorAll('.op').forEach(x=>x.classList.remove('sel'));
        b.classList.add('sel'); seleccion=v; };
      colI.appendChild(b); });
    der.forEach(v=>{ const b=document.createElement('button');
      b.className='op'; b.textContent=v;
      b.onclick=()=>{
        if(!seleccion || b.disabled) return;
        const par=e.pares.find(x=>x[0]===seleccion);
        if(par && par[1]===v){
          b.classList.add('ok'); b.disabled=true;
          const src=[...colI.querySelectorAll('.op')].find(x=>x.dataset.v===seleccion);
          src.classList.remove('sel'); src.classList.add('ok'); src.disabled=true;
          seleccion=null; hechos++;
          if(hechos===e.pares.length){ acertar(); }
        } else {
          b.classList.add('mal');
          setTimeout(()=>b.classList.remove('mal'),600);
          if(!bloqueado){ bloqueado=true; vidas--; pintarBarra();
            aviso(false,'Ese par no coincide. Inténtalo de nuevo.');
            setTimeout(()=>{ bloqueado=false;
              const a=t.querySelector('.aviso'); if(a) a.remove(); },1200); }
        }
      };
      colD.appendChild(b); });
    g.appendChild(colI); g.appendChild(colD); t.appendChild(g);
  }

  if(e.tipo==='ordenar'){
    const zona=document.createElement('div'); zona.className='orden-zona';
    zona.innerHTML='<span style="color:#9AA1AC;font-weight:700">Toca en orden…</span>';
    t.appendChild(zona);
    const c=document.createElement('div'); c.className='ops';
    const mezcla=[...e.items].sort(()=>Math.random()-.5);
    mezcla.forEach(v=>{ const b=document.createElement('button');
      b.className='op'; b.textContent=v;
      b.onclick=()=>{
        if(b.disabled||bloqueado) return;
        const esperado=e.items[orden.length];
        if(v===esperado){
          orden.push(v); b.disabled=true; b.classList.add('ok');
          if(orden.length===1) zona.innerHTML='';
          const pill=document.createElement('span');
          pill.className='pill'; pill.textContent=v; zona.appendChild(pill);
          if(orden.length===e.items.length){ bloqueado=true; acertar(); }
        } else {
          b.classList.add('mal'); bloqueado=true;
          c.querySelectorAll('.op').forEach(x=>x.disabled=true);
          fallar('El orden correcto era: '+e.items.join(' → '));
        }
      };
      c.appendChild(b); });
    t.appendChild(c);
  }

  z.appendChild(t);
}

function final(){
  const total=EJ.length;
  const pct=Math.round(100*aciertos/total);
  let sello='🌱', msg='¡Sigue practicando! Cada intento te hace mejor.';
  if(pct>=90){ sello='🏆'; msg='¡Excelente! Dominas este tema.'; }
  else if(pct>=70){ sello='🌟'; msg='¡Muy bien! Ya casi lo dominas.'; }
  else if(pct>=50){ sello='💪'; msg='¡Vas bien! Repasa y vuelve a intentar.'; }
  $('zona').innerHTML=
    `<div class="tarjeta final"><div class="sello">${sello}</div>
     <h2>${vidas<=0?'Se acabaron los corazones':'¡Terminaste!'}</h2>
     <div class="puntos">${aciertos} / ${total}</div>
     <p style="color:var(--humo);font-weight:700">${msg}</p>
     <button class="btn" onclick="reiniciar()">Jugar otra vez</button></div>`;
  if(pct>=70) chispas();
  pintarBarra();
}

function reiniciar(){ i=0; aciertos=0; vidas=3; bloqueado=false;
  seleccion=null; orden=[]; pintarBarra(); render(); }

pintarBarra(); render();
</script></body></html>
"""


def render_juego(ejercicios, alto=680):
    html = _HTML.replace("__DATOS__", json.dumps(ejercicios, ensure_ascii=False))
    components.html(html, height=alto, scrolling=True)


# ================================================================
# 3. INTERFAZ
# ================================================================

def tab_aprendo_jugando(config=None):
    st.subheader("🎮 Aprendo Jugando — Inicial y Primaria")
    st.caption("Actividades interactivas alineadas al CNEB. El estudiante "
               "responde tocando la pantalla: sirve en tablet, celular y "
               "pizarra digital.")

    c1, c2 = st.columns(2)
    with c1:
        nivel = st.selectbox("Nivel:", list(BANCO.keys()), key="jg_nivel")
    with c2:
        area = st.selectbox("Área curricular:", list(BANCO[nivel].keys()),
                            key="jg_area")

    ejercicios = BANCO[nivel][area]

    NIVELES = {
        "Progresivo — de fácil a difícil": None,
        "Solo básico ⭐": 1,
        "Solo intermedio ⭐⭐": 2,
        "Solo avanzado ⭐⭐⭐": 3,
    }
    c3, c4 = st.columns(2)
    with c3:
        modo = st.selectbox("Dificultad:", list(NIVELES.keys()), key="jg_dif",
                            help="En modo progresivo las actividades salen "
                                 "ordenadas de la más simple a la más "
                                 "exigente, como una escalera.")
    with c4:
        filtro_d = NIVELES[modo]
        disponibles = ([e for e in ejercicios if e.get("d", 1) == filtro_d]
                       if filtro_d else list(ejercicios))
        tope = max(len(disponibles), 3)
        cuantos = st.slider("Cantidad de actividades:", 3, tope,
                            min(6, tope), key="jg_n")

    if not disponibles:
        st.warning(f"No hay actividades de ese nivel en {area}. "
                   f"Elige otra dificultad o cambia de área.")
        return

    import random
    seed = st.session_state.get("jg_seed", 0)
    if filtro_d:
        lista = list(disponibles)
        random.Random(seed).shuffle(lista)
        lista = lista[:cuantos]
    else:
        # Progresivo: se mezcla dentro de cada nivel y luego se apilan
        # básico → intermedio → avanzado, para que la dificultad suba.
        lista = []
        for niv in (1, 2, 3):
            grupo = [e for e in disponibles if e.get("d", 1) == niv]
            random.Random(seed + niv).shuffle(grupo)
            lista.extend(grupo)
        lista = lista[:cuantos]

    b1, b2 = st.columns([1, 3])
    with b1:
        if st.button("🔄 Nuevas", use_container_width=True, key="jg_reroll"):
            st.session_state["jg_seed"] = st.session_state.get("jg_seed", 0) + 1
            st.rerun()
    with b2:
        _mapa = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}
        _ruta = " → ".join(_mapa[e.get("d", 1)] for e in lista)
        st.caption(f"{len(lista)} actividades · 3 corazones · "
                   f"faja andina que se teje con cada acierto")
        st.caption(f"Ruta de esta sesión: {_ruta}")

    render_juego(lista)

    with st.expander("💡 Cómo usarlo en clase"):
        st.markdown("""
- **En la pizarra digital:** proyecta y que los niños pasen por turnos a tocar
  la respuesta. Funciona bien como actividad de inicio o de cierre.
- **En tablets o celulares:** cada niño juega a su ritmo mientras tú
  acompañas a quienes lo necesitan.
- **Como evaluación formativa:** observa en qué actividad se traban. El error
  te dice qué desempeño hay que reforzar, no solo cuántos puntos sacaron.
- **Los corazones no castigan:** al perderlos el juego termina y ofrece volver
  a intentar. La idea es reintentar, no calificar.
""")
