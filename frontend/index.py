import plotly.express as px
import streamlit as st
from estilo import estilo_general, estilo_metricas
import requests
import pandas as pd
import json

POSITIVO = "#24a148"
NEGATIVO = "#FF6C6C"
NPK = ["#4ade80", "#06b6d4", "#eab308"]
HOST = "http://127.0.0.1:8000/"

# Configuracion de la pagina
st.set_page_config(page_title="CultiBot", layout="wide", page_icon="🌱", initial_sidebar_state="collapsed")

# Estilos
estilo_general()
estilo_metricas()

def init_session():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = {}

# Función para las cards de temperatura, humedad, luminosidad
def draw_metric_card(column, icon, title, value, delta, color):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{icon} {title}</div>
                <div>
                    <span class="metric-value">{value}</span>
                    <span class="metric-delta" style="color:{color};">{delta}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Función para las barras del NPK
def draw_npk_bar(column, icon, name, percentage, color):
    """Función para dibujar de forma limpia cada barra NPK"""
    with column:
        st.markdown(
            f"""
            <div>
                <div class="npk-label-container">
                    <span class="npk-icon-text"><span>{icon}</span> {name}</span>
                    <span style="font-weight: bold;">{percentage}%</span>
                </div>
                <div class="npk-bar-bg">
                    <div class="npk-bar-fill" style="width: {percentage*20}%; background-color: {color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def titulo(nombre_boton:str, icono:str, planta:dict):
    col_atras, col_titulo, col_analisis = st.columns([1,8,1], vertical_alignment="center")

    with col_atras:
        if st.button("←"):
            # Limpiamos los parámetros para volver al inicio
            st.query_params.clear()
            st.rerun()
    
    col_titulo.title(planta["nombre"])
    col_titulo.markdown(f"**Planta:** {planta['tipo']}")
    col_titulo.markdown(f"**Suelo:** {planta['tipo_suelo'].capitalize()}")

    # col_analisis.button("CultiBot", type="primary", icon="🤖")
    with col_analisis:
        if st.button(nombre_boton, type="primary", icon=icono):
            # Limpiamos los parámetros para volver al inicio
            st.query_params["vista"] = nombre_boton
            st.rerun()

def estadisticas(df: pd.DataFrame, metrica: dict):
    # --- 1. SECCIÓN TEMPERATURA Y HUMEDAD
    col_t, col_h, col_l = st.columns(3)

    dif_temp = float(df.loc[1]['temperatura_ambiente']) - float(metrica['temperatura_ambiente'])
    dif_hum = float(df.loc[1]['humedad_suelo']) - float(metrica['humedad_suelo'])
    dif_lum = float(df.loc[1]['luminosidad']) - float(metrica['luminosidad'])

    draw_metric_card(col_t, "🌡️", "Temperatura", f"{metrica['temperatura_ambiente']}°C", f"{dif_temp:.2f}°C", POSITIVO if dif_temp >= 0 else NEGATIVO)
    draw_metric_card(col_h, "💧", "Humedad", f"{metrica['humedad_suelo']}%", f"{dif_hum:.2f}%", POSITIVO if dif_temp >= 0 else NEGATIVO)
    draw_metric_card(col_l, "⛅", "Luminosidad", f"{metrica['luminosidad']}lx", f"{dif_lum:.2f}lx", POSITIVO if dif_temp >= 0 else NEGATIVO)

    # --- 2. SECCIÓN NPK NUTRIENTS ---
    st.markdown('<div class="npk-section-title">NPK Nutrients</div>', unsafe_allow_html=True)

    # Creamos 3 columnas para Nitrogeno, Potasio y Fosforo
    col_n, col_k, col_p = st.columns(3)

    # Renderizar las barras con sus respectivos colores hex según la imagen
    draw_npk_bar(col_n, "⚛️", "N", metrica['nutrientes']['nitrogeno'], NPK[0])  # Nitrogeno
    draw_npk_bar(col_k, "🧪", "K", metrica['nutrientes']['potasio'], NPK[1])  # Potasio
    draw_npk_bar(col_p, "🍃", "P", metrica['nutrientes']['fosforo'], NPK[2])  # Fosforo

    # --- 3. FOOTER (Last updated) ---
    st.markdown(f'<div class="footer-text">Última actualización: {metrica["fecha"]}</div>', unsafe_allow_html=True)

    col_1, col_2= st.columns(2)

    # --- 4. Gráfico Temperatura ---
    fig_t = px.line(df, x='fecha', y="temperatura_ambiente", title='🌡️ Temperatura')
    fig_t.update_traces(line_color="#9C071B")
    col_1.plotly_chart(fig_t)

    # --- 5. Gráfico Humedad ---
    fig_h = px.line(df, x='fecha', y="humedad_suelo", title='💧 Humedad')
    fig_h.update_traces(line_color="#070F9C")
    col_2.plotly_chart(fig_h)
    
    # --- 6. Gráfico Luminosidad ---
    fig_l = px.line(df, x='fecha', y="luminosidad", title='⛅ Luminosidad')
    fig_l.update_traces(line_color="#F4D80B")
    col_1.plotly_chart(fig_l)

    # --- 7. Gráfico NPK ---
    fig_n = px.line(df, x='fecha', y=['nitrogeno', 'potasio', 'fosforo'], title='⚛️ Nutrients', color_discrete_sequence=NPK)
    col_2.plotly_chart(fig_n)

def cultiBot(prompt: str, respuesta_previa: str = "") -> list:
    data = {
        "model": "google/gemma-4-e4b",
        "input": f"{prompt}",
        "max_output_tokens": 3000,
        "reasoning": "on"
    }

    if respuesta_previa != "":
        data["previous_response_id"] = respuesta_previa

    response = requests.post(
        "http://localhost:1234/api/v1/chat",
        json= data
    )
    response = response.json()
    try:
        return [response['output'][1]['content'], response['response_id']]
    except:
        return [response, ""]

def formato_respuesta(respuesta_json):
    markdown_content = f"""
# Reporte de Estado

## Estado General

**{respuesta_json['estado_general']}**

## Diagnóstico

{respuesta_json['diagnostico_detallado']}

## Acciones Inmediatas

"""

    # Recorremos la lista de acciones para agregarlas como puntos de viñeta
    for accion in respuesta_json["acciones_inmediatas"]:
        markdown_content += f"- {accion}\n"

    markdown_content += f"""

## Sugerencias de fertilizante

{respuesta_json['sugerencia_fertilizante']}
    """
    # print(markdown_content)
    return markdown_content

def metricas_to_df(metricas: list) -> pd.DataFrame:
    metricas_dict = {
        "humedad_suelo" : [], 
        "temperatura_ambiente" : [],
        "luminosidad" : [],
        "nitrogeno" : [],
        "potasio" : [],
        "fosforo" : [],
        "fecha" : []
        }

    for m in metricas:
        metricas_dict['humedad_suelo'].append(m['humedad_suelo'])
        metricas_dict['temperatura_ambiente'].append(m['temperatura_ambiente'])
        metricas_dict['luminosidad'].append(m['luminosidad'])
        metricas_dict['nitrogeno'].append(m['nutrientes']['nitrogeno'])
        metricas_dict['potasio'].append(m['nutrientes']['potasio'])
        metricas_dict['fosforo'].append(m['nutrientes']['fosforo'])
        metricas_dict['fecha'].append(m['fecha'])

    return pd.DataFrame(metricas_dict)

def vista_inicio():
    st.title("🏠 Página de Inicio CultiBot 🍃")
    st.write("Bienvenido al panel principal.")

    # Extrae todas las plantas
    response = requests.get(HOST).json()

    # Transforma la respuesta en un data frame
    df = pd.DataFrame(response['plantas'])
    seleccion = st.dataframe(
        df, 
        hide_index=True,
        on_select="rerun",  # Vuelve a ejecutar el script inmediatamente al hacer clic
        selection_mode="single-row"
    )

    # Verifica si el usuario selecciono alguna planta
    fila_seleccionada = seleccion.get("selection", {}).get("rows", [])

    if fila_seleccionada:
        # Rescata el id de la planta
        indice_fila = fila_seleccionada[0]
        id_planta = df.iloc[indice_fila]["id"]

        # Agrega el id como parametro
        st.query_params["id"] = str(id_planta)
        st.query_params["vista"] = "Métricas"
        st.rerun()

def vista_metricas(planta_id):
    # Extrae todas las méticas de la planta
    response_all = requests.get(f"{HOST}metricas?id={planta_id}").json()
    metricas_planta = response_all['metricas']

    # Extrae las últimas métricas de la planta
    response_last = requests.get(f"{HOST}ultimaMetrica?id={planta_id}").json()
    ultimas_metricas = response_last['metrica']

    # Barra del titulo
    titulo('CultiBot', '🤖', ultimas_metricas['planta'])

    # Transformarmos las metricas en un data frame
    metricas_df = metricas_to_df(metricas_planta)

    # Baners con las estadisticas y graficas
    estadisticas(metricas_df, ultimas_metricas)

    st.dataframe(metricas_df)

    # st.write(ultimas_metricas)

def vista_cultibot(planta_id):
    # Extrae las últimas métricas de la planta
    response_last = requests.get(f"{HOST}ultimaMetrica?id={planta_id}").json()
    ultimas_metricas = response_last['metrica']

    # Barra del titulo
    titulo('Métricas', '📈', ultimas_metricas['planta'])

    # Inicializa el historial de mensjaes según la planta
    if planta_id not in st.session_state.messages:
        st.session_state.messages[planta_id] = []

    # Genera el reporte general (Primer mensaje)
    if not st.session_state.messages[planta_id] and ultimas_metricas:
        with st.spinner("Pensando..."):
            response = cultiBot(ultimas_metricas)
            response_json = response[0]
            if "```json" in response_json:
                texto_limpio = response_json.split("```json")[1].split("```")[0].strip()
                response_json = json.loads(texto_limpio)
            st.session_state.messages[planta_id].append({"id": response[1],"role": "assistant", "content": formato_respuesta(response_json)})

    # Renderizar los mensajes anteriores
    for message in st.session_state.messages[planta_id]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input():
        # Mostrar el mensaje del usuario inmediatamente en el contenedor
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages[planta_id].append({"role": "user", "content": prompt})

        # Extraemos el id de la ultima respuesta del bot
        id_previo = ""
        for msg in reversed(st.session_state.messages[planta_id]):
            if msg["role"] == "assistant" and "id" in msg and msg["id"]:
                id_previo = msg["id"]
                break # Ya no es necesario seguir en el for

        # Respuesta del bot
        with st.spinner("Pensando..."):
            if st.session_state.messages[planta_id]:
                response = cultiBot(prompt, id_previo)
        with st.chat_message("assistant"):
            st.markdown(response[0])
            
        st.session_state.messages[planta_id].append({"id": response[1], "role": "assistant", "content": response[0]})

if __name__ == "__main__":
    init_session()
    # Leemos los parámetros actuales de la URL
    parametros = st.query_params

    if "id" in parametros and "vista" in parametros:
        id_seleccionado = parametros["id"]
        if parametros["vista"] == "Métricas":
            vista_metricas(id_seleccionado)
        else:
            vista_cultibot(id_seleccionado)
    else:
        # Si no hay parámetros, mostramos el inicio por defecto
        vista_inicio()