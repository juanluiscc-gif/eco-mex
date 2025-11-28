import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

data_clean = pd.read_csv('data_clean.csv')

# Título de la aplicación
st.title("Estudio de la economía formal mexicana")

# Crear tres columnas para los botones
col1, col2, col3 = st.columns(3)

# Botón 1: Importancia del estudio
with col1:
    if st.button("Importancia del estudio"):
        st.write("El presente estudio se realiza con el objetivo de ilustrar los datos oficiales sobre las actividades económicas que se desarrollan en México. Siendo la primer parte de un estudio más extenso que permita contestar a las preguntas: ¿QUÉ DEBO HACER PARA HACER DINERO?, ¿DONDE DEBO INVERTIR MI TIEMPO Y DINERO?, ¿EN QUÉ DEBO TRABAJAR?, ¿QUÉ DEBO ESTUDIAR?")

# Botón 2: Qué es la economía formal
with col2:
    if st.button("¿Qué es la economía formal?"):
        st.write("Son todas las actividades económicas registradas, reguladas y vigiladas por el estado, incluyendo el pago de impuestos, el cumplimiento de leyes laborales y de seguridad social, y el registro legal de empresas y trabajadores.")

# Botón 3: Qué es la economía informal
with col3:
    if st.button("¿Qué es la economía informal?"):
        st.write("Se trata de la producción de bienes y servicios que no están registrados ni protegidos por el estado, incluyendo el trabajo y las empresas que operan fuera de los marcos legales y normativos.")

st.subheader("Metodología del estudio")
st.write("Para el presente estudio se obtuvieron los datos del “Sistema empresarial mexicano”, donde se hizo una limpieza de datos a fin de poder mostrar las actividades económicas registradas por el gobierno, y que se desarrollan en todo el pais. Una vez que se pudo identificar la cantidad de empresas registradas, se les asignó un sector económico, a fin de poder comparar diferentes localidades. Se logró cuantificar un 87 % de las actividades registradas por el gobierno mexicano. Los datos abiertos están aquí: https://datos.gob.mx/dataset/sistema_informacion_empresarial_mexicano ")

st.divider()  # Línea separadora

st.subheader("Limitaciones del estudio")
st.write("Es importante reconocer que las palabras ‘formal’ e ‘informal’, no necesariamente quiere decir que una actividad es mejor o peor que la otra, en el sentido social, legal o moral. Se refiere a las condiciones administrativas bajo las cuales se desarrollan algunas actividades. Es decir, que las actividades que registra el gobierno se pueden contar o medir, pero es probable que estos datos sean sólo un reflejo de una economía mucho más grande y que sostiene a la sociedad mexicana.")

st.subheader("Resultados del estudio")
st.write("Primeramente se muestran las actividades de las empresas que registró el gobierno mexicano. En la segunda parte, se podrán comparar el número de empresas o actividades registradas por Estado. Esta comparación se limita a dos estados por turno.")

st.subheader("Sectores económicos en México")
fig = go.Figure(data=[go.Histogram(x=data_clean['sector_economico'])])
# Opcional: añadir un título al gráfico 
fig.update_layout(title_text='Distribución de los sectores económicos en México')
# Mostrar el gráfico Plotly
st.plotly_chart(fig)
st.write("Los datos sin clasificar obedecen a errores en la toma de información por parte del gobierno mexicano.")

st.subheader("Actividades de los sectores económicos en México")
# Obtener sectores económicos únicos
sectores = data_clean[data_clean["sector_economico"]!= "sin clasificar"][data_clean["sector_economico"].unique() ]

# Crear una gráfica para cada sector
for sector in sectores:
    st.subheader(f"Sector: {sector}")

    # Filtrar actividades del sector actual
    df_sector = data_clean[data_clean["sector_economico"] == sector]

    # Contar actividades
    conteo_actividades = df_sector["actividad"].value_counts()

    # Crear gráfica circular
    fig, ax = plt.subplots()
    ax.pie(conteo_actividades, labels=conteo_actividades.index, autopct="%1.1f%%")
    ax.axis("equal")  # Para que sea circular

    # Mostrar gráfica
    st.pyplot(fig)

# Comparación de economías entre estados
st.title("Revisa las actividades economicas en los estados por sector.")

# 1️ SELECTBOX PARA ELEGIR EL ESTADO
estados = sorted(data_clean["estado"].unique())
estado_sel = st.selectbox("Selecciona un estado", estados)

# Filtrar por el estado seleccionado
df_estado = data_clean[data_clean["estado"] == estado_sel].copy()

# 2️ SELECTBOX PARA ELEGIR EL SECTOR ECONÓMICO DISPONIBLE EN ESE ESTADO
sectores_validos = ["primario", "secundario", "terciario"]

# Sectores válidos en el estado
sectores = sorted(
    df_estado[df_estado["sector_economico"].isin(sectores_validos)]["sector_economico"].unique())

if not sectores:
    st.warning("Este estado no contiene información de sectores permitidos.")
    st.stop()

sector_sel = st.selectbox("Selecciona un sector económico", sectores)

# Filtrar por sector elegido
df_sector = df_estado[df_estado["sector_economico"] == sector_sel]

# 3️ CONTAR ACTIVIDADES
conteo_actividades = df_sector["actividad"].value_counts()

st.subheader(f"Actividades económicas del sector **{sector_sel.capitalize()}** en **{estado_sel}**")

# 4️ GRÁFICA CIRCULAR
fig, ax = plt.subplots()
ax.pie(conteo_actividades, labels=conteo_actividades.index, autopct="%1.1f%%")
ax.axis("equal")
st.pyplot(fig)

# 5️ APARTADO EXTRA: EMPRESAS SIN CLASIFICAR
sin_clasificar = df_estado[df_estado["sector_economico"] == "sin clasificar"]

if not sin_clasificar.empty:
    total_sin_clasificar = len(sin_clasificar)
    st.info(f"En este estado no se pudieron clasificar **{total_sin_clasificar}** empresas.")
else:
    st.success("En este estado todas las empresas fueron clasificadas correctamente.")