import pandas as pd
import streamlit as st
from scipy.spatial.distance import pdist, squareform

datos_originales_con_grupo = pd.read_csv("datos_originales_con_grupo.csv")
datos_scaled = pd.read_csv("datos_scaled.csv")
viviendas_maximas_recomendadas = 16
viviendas_iniciales = 16 
viviendas_por_incremento = 16

distancias = pdist(datos_scaled.values, metric='euclidean')
matriz_distancias = pd.DataFrame(squareform(distancias))

if "vivienda_seleccionada" not in st.session_state:
    st.session_state["vivienda_seleccionada"] = None

if "viviendas_a_mostrar" not in st.session_state:
    st.session_state["viviendas_a_mostrar"] = viviendas_iniciales

if st.session_state["vivienda_seleccionada"] is None:
    st.markdown("<h1 style='text-align: center;'>Selecciona una vivienda</h1>", unsafe_allow_html=True)

    viviendas_mostrar = datos_originales_con_grupo.head(st.session_state["viviendas_a_mostrar"])

    cols = st.columns(4) 
    for index, vivienda in viviendas_mostrar.iterrows():
        vivienda_info = (
            f"<b>Vivienda {index + 1}</b><br>"
            f"🛏️ Habitaciones: {vivienda['Habitaciones']}<br>"
            f"🛁 Baños: {vivienda['Baños']}<br>"
            f"📐 Metros: {vivienda['Metros cuadrados construidos']} m²<br>"
            f"💶 Precio: {vivienda['Precio']} €"
        )
        with cols[index % 4]:
            st.markdown(
                f"""
                <div style="text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-top: 5px;">
                    {vivienda_info}
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Seleccionar Vivienda", key=index):
                st.session_state["vivienda_seleccionada"] = (vivienda, index)

    if len(viviendas_mostrar) < len(datos_originales_con_grupo):
        if st.button("Mostrar más"):
            st.session_state["viviendas_a_mostrar"] += viviendas_por_incremento

else:
    vivienda, idx = st.session_state["vivienda_seleccionada"]

    st.markdown(f"<h2 style='font-weight: bold;'>{vivienda['Título']}</h2>", unsafe_allow_html=True)
    st.write(vivienda['Dirección'])
    st.markdown(f"<h4 style='font-weight: bold;'>{vivienda['Precio']} €</h4>", unsafe_allow_html=True)
    st.write(f"📐 {vivienda['Metros cuadrados construidos']} m², 🛏️ {vivienda['Habitaciones']} habitaciones, 🛁 {vivienda['Baños']} baños")
    st.write(vivienda['Descripción'])

    link_id = vivienda['Id del anuncio']
    link_url = f"https://www.idealista.com/inmueble/{link_id}"
    st.markdown(f"[Ver más detalles en Idealista]({link_url})")

    st.markdown("<h5>Características Adicionales:</h5>", unsafe_allow_html=True)
    st.write(f" - Ascensor: {vivienda['Ascensor (Sí/No)']}") 
    st.write(f" - Obra nueva: {vivienda['Obra nueva (Sí/No)']}")
    st.write(f" - Piscina: {vivienda['Piscina (Sí/No)']}")
    st.write(f" - Terraza: {vivienda['Terraza (Sí/No)']}")
    st.write(f" - Parking: {vivienda['Parking (Sí/No)']}")
    st.write(f" - Parking incluido en el precio: {vivienda['Parking incluido en el precio (Sí/No)']}")
    st.write(f" - Aire acondicionado: {vivienda['Aire acondicionado (Sí/No)']}")
    st.write(f" - Trastero: {vivienda['Trastero (Sí/No)']}")
    st.write(f" - Jardín: {vivienda['Jardín (Sí/No)']}")

    grupo_vivienda = vivienda['Grupo']

    indices_mismo_grupo = datos_originales_con_grupo[datos_originales_con_grupo['Grupo'] == grupo_vivienda].index
    indices_mismo_grupo = indices_mismo_grupo.drop(idx)
    indices_recomendaciones = matriz_distancias.iloc[idx, indices_mismo_grupo].sort_values().index[:viviendas_maximas_recomendadas]
    recomendaciones = datos_originales_con_grupo.iloc[indices_recomendaciones]

    st.markdown("<h5>Viviendas recomendadas:</h5>", unsafe_allow_html=True)

    rows = [recomendaciones.iloc[i:i+4] for i in range(0, len(recomendaciones), 4)]
    for row in rows:
        cols = st.columns(4)
        for col, (index, vivienda_recomendada) in zip(cols, row.iterrows()):
            vivienda_info = (
                f"<b>Vivienda {index+1}</b><br>"
                f"🛏️ Habitaciones: {vivienda_recomendada['Habitaciones']}<br>"
                f"🛁 Baños: {vivienda_recomendada['Baños']}<br>"
                f"📐 Metros: {vivienda_recomendada['Metros cuadrados construidos']} m²<br>"
                f"💶 Precio: {vivienda_recomendada['Precio']} €"
            )
            with col:
                st.markdown(
                    f"""
                    <div style="text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-top: 5px;">
                        {vivienda_info}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                if st.button("Seleccionar Vivienda", key=f"recomendada_{index}"):
                    st.session_state["vivienda_seleccionada"] = (vivienda_recomendada, index)

    if st.button("Volver a la selección de viviendas"):
        st.session_state["vivienda_seleccionada"] = None
