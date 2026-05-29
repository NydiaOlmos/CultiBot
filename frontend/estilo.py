import streamlit as st

def estilo_general():
    return st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
    *{
        font-family: Poppins;
    }

    .main-card {
        background-color: rgba(255, 255, 255, 0.08); /* Fondo muy sutilmente visible */
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6); /* Sombra intensa para que flote */
        margin-top: 20px;
        backdrop-filter: blur(8px); /* Efecto cristal */
        border: 1px solid rgba(255, 255, 255, 0.1); /* Borde sutil brillante */
        position: relative; /* Asegura que la tarjeta esté encima de las estrellas */
        z-index: 10;
    }
    """,
    unsafe_allow_html=True,
)

def estilo_metricas():
    return st.markdown(
    """
    <style>
    .metric-card {
        background-color: #111214;
        border: 1px solid #262730;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0px;
    }
    .metric-title {
        font-size: 14px;
        color: #808495;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        display: inline-block;
    }
    .metric-delta {
        font-size: 14px;
        color: ; /* Color verde para indicar subida/positivo */
        margin-left: 8px;
        display: inline-block;
        font-weight: 500;
    }
    /* Estilo para la sección NPK */
    .npk-section-title {
        font-size: 18px;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 15px;
        margin-top: 10px;
    }
    .npk-label-container {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 6px;
        font-weight: 500;
    }
    .npk-icon-text {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .npk-bar-bg {
        background-color: #1c1d21;
        border-radius: 4px;
        height: 8px;
        width: 100%;
        margin-bottom: 20px;
    }
    .npk-bar-fill {
        height: 100%;
        border-radius: 4px;
    }
    
    /* Texto de actualización */
    .footer-text {
        font-size: 13px;
        color: #64748b;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

