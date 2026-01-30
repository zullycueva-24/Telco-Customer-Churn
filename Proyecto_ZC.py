import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
import io

if "df" not in st.session_state:
    st.session_state["df"] = None

class DataAnalyzer:
                def __init__(self, df:pd.DataFrame):
                    self.df = df

                def info_general(self):
                    buffer = io.StringIO()
                    self.df.info(buf=buffer)
                    return buffer.getvalue()

                def tipos_variables(self):
                    return self.df.dtypes

                def nulos(self):
                    return self.df.isnull().sum()

                def clasificar_variables(self):
                    numericas = self.df.select_dtypes(include="number").columns.tolist()
                    categoricas = self.df.select_dtypes(exclude="number").columns.tolist()
                    return numericas, categoricas

                def estadisticas(self):
                    return self.df.describe()

                def moda(self, col):
                    return self.df[col].mode().iloc[0]

                def histograma(self, col):
                    fig, ax = plt.subplots()
                    self.df[col].dropna().hist(ax=ax, bins=30)

                    ax.set_title(f"Distribución de {col}")
                    ax.set_xlabel(col)          
                    ax.set_ylabel("Frecuencia")    
                    return fig
                
st.sidebar.title("Módulos")

modulo = st.sidebar.selectbox("Seleccione un módulo",["Home", "Carga del Dataset", "Análisis Exploratorio de Datos (EDA)", "Conclusiones"])

if modulo == "Home":

# Configuración de página
    st.set_page_config(
    page_title="Proyecto de Análisis de Datos",
    page_icon="📱",
    layout="centered"
)

# --- ESTILOS CSS ---
    st.markdown("""
    <style>
    .hero {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 3rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    }
    .card {
    background-color: #f5f5f5;
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    }
    .tech span {
    background-color: #e0e7ff;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    margin-right: 0.4rem;
    display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO ---
    st.markdown("""
    <div class="hero">
    <h1>📊 CASO DE ESTUDIO 2 - TelcoCustomerChurn</h1>
    <h3>Análisis de datos con enfoque estratégico</h3>
    <p>Explorando información, encontrando patrones y contando historias con datos 🚀</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # espacio

# --- OBJETIVO ---
    st.markdown("""
    <div class="card">
    <h2>🎯 Objetivo del análisis</h2>
    <p>
    Este proyecto tiene como objetivo analizar y comprender las causas asociadas a la fuga de los clientes,
    identificando patrones, tendencias y hallazgos relevantes que apoyen la toma de decisiones.
    </p>
    </div>
    """, unsafe_allow_html=True)

# --- AUTOR ---
    st.markdown("""
    <div class="card">
    <h2>👩‍💻 Datos del autor</h2>
    <ul>
        <li><b>Nombre:</b> Zully Beatriz Cueva Yerba</li>
        <li><b>Curso / Especialización:</b> Especialización en Python for Analytics</li>
        <li><b>Año:</b> 2026</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- DATASET ---
    st.markdown("""
    <div class="card">
    <h2>📁 Dataset</h2>
    <p>
    El Dataset utilizado contiene información sobre los clientes, sus servicios contratados, facturación mensual, tiempo de permanencia y estado actual en la empresa.
    Durante el último mes, debido a la coyuntura del COVID-19, la empresa incrementó su ratio de fuga de clientes en +0.5 puntos porcentuales, pasando de 2% en promedio a 2.5%. El costo de adquirir un nuevo cliente es entre 6 y 7 veces mayor que retener uno existente, por lo que es vital analizar los datos históricos para detectar patrones de comportamiento y mejorar la retención.
    </p>
    </div>
    """, unsafe_allow_html=True)

# --- TECNOLOGÍAS ---
    st.markdown("""
    <div class="card">
    <h2>🛠️ Tecnologías utilizadas</h2>
    <div class="tech">
        <span>🐍 Python</span>
        <span>📊 Pandas</span>
        <span>📈 NumPy</span>
        <span>🌐 Streamlit</span>
        <span>🎨 Matplotlib</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
    st.markdown("""
    <p style="text-align:center; color: gray;">
    Proyecto final académico • 2026 • Powered by Streamlit ⚡
    </p>
    """, unsafe_allow_html=True)

elif modulo == "Carga del Dataset":

    st.header("📂 Módulo 2: Carga del Dataset")

    archivo_cargado = st.file_uploader(
    "📤 Sube tu archivo CSV para comenzar el análisis",
    type=["csv"],
    key="uploader_csv"
)

# Validación: archivo cargado
    if archivo_cargado is not None and st.session_state["df"] is None:
        try:
        # Leer CSV
            st.session_state["df"]= pd.read_csv(archivo_cargado)

            st.success("✅ Archivo cargado correctamente")

        except Exception as e:
            st.error("❌ Error al leer el archivo. Verifica que sea un CSV válido.")
            st.exception(e)

    if st.session_state["df"] is not None:
        df = st.session_state["df"]
            
        # Dimensiones del dataset
        filas, columnas = df.shape
        st.info(f"📐 Dimensiones del dataset: **{filas} filas** y **{columnas} columnas**")

        # Vista previa
        st.subheader("👀 Vista previa del dataset")
        st.dataframe(df.head())      

    else:
        st.warning("⚠️ Aún no se ha cargado ningún archivo. El análisis está deshabilitado.")

elif modulo == "Análisis Exploratorio de Datos (EDA)":
    st.header("📊 Módulo 3: Análisis Exploratorio de Datos")

    if st.session_state["df"] is None:
        st.warning("⚠️ Primero debes cargar un dataset en el módulo 'Carga del Dataset'")
        st.stop()
    
    df = st.session_state.df
    analyzer = DataAnalyzer(df)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").astype(float)
    df["SeniorCitizen_flag"] = df["SeniorCitizen"].astype(bool)
    df["Churn_flag"] = df["Churn"].map({"Yes": 1, "No": 0})
    servicios = [
    "Partner", "Dependents", "PhoneService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "PaperlessBilling"
    ]

    for col in servicios:
        df[f"{col}_flag"] = df[col].map({"Yes": 1, "No": 0})
    
    df["MultipleLines_flag"] = df["MultipleLines"] == "Yes"

    cols_internet = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies"
    ]

    for col in cols_internet:
        df[f"{col}_flag"] = df[col] == "Yes"

    tab_eda1, tab_eda2 = st.tabs(["📊 EDA Básico", "📈 EDA Avanzado"])

    with tab_eda1:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "1️⃣ Info General",
            "2️⃣ Variables",
            "3️⃣ Estadísticas Descriptivas",
            "4️⃣ Valores faltantes",
            "5️⃣ Distribución de variables"])

    with tab_eda2:
        tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "6️⃣ Variables categóricas",
            "7️⃣ Análisis bivariado",
            "8️⃣ Categórico vs categórico",
            "9️⃣ Análisis dinámico",
            "🔟 Hallazgos clave"
            ])

    with tab1:
        st.subheader("📌 Información general del dataset")

        col1, col2 = st.columns(2)
    
        with col1:
            st.text("Información del DataFrame")
            st.text(analyzer.info_general())

        with col2:
            st.write("Tipos de datos")
            st.dataframe(analyzer.tipos_variables())

        st.markdown("---")

        st.write("Conteo de valores nulos")
        st.dataframe(analyzer.nulos())

    with tab2:
        st.subheader("📂 Clasificación de variables")

        numericas, categoricas = analyzer.clasificar_variables()

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"🔢 Variables numéricas ({len(numericas)})")
            st.write(numericas)

        with col2:
            st.write(f"🏷️ Variables categóricas ({len(categoricas)})")
            st.write(categoricas)

    with tab3:
        st.subheader("📈 Estadísticas descriptivas")
        st.dataframe(analyzer.estadisticas())
        st.markdown("""
        **Interpretación básica**:
        - La media indica el valor promedio.
        - La mediana muestra el valor central.
        - La desviación estándar refleja la dispersión de los datos.
        """)

    with tab4:
        st.subheader("🕳️ Análisis de valores faltantes")

        nulos = analyzer.nulos()
        st.dataframe(nulos[nulos > 0])

        st.markdown("""
        **Discusión**:  
        Las variables con valores faltantes pueden afectar el análisis y deben
        ser tratadas según su importancia y proporción de ausencia. 
        """)

    with tab5:
        st.subheader("📊 Distribución de variables numéricas")

        col = st.selectbox("Selecciona una variable numérica", numericas)
        fig = analyzer.histograma(col)
        st.pyplot(fig)

        st.markdown("**Interpretación visual**: Se observa la forma de la distribución y posibles sesgos.")
        
    with tab6:
        st.subheader("📊 Análisis de variables categóricas")

        cat_col = st.selectbox("Selecciona variable categórica", categoricas)

        conteo = df[cat_col].value_counts()
        st.bar_chart(conteo)

        st.write("Proporciones")
        st.dataframe((conteo / conteo.sum()) * 100)

    with tab7:
        st.subheader("🔁 Numérico vs Categórico")

        num = st.selectbox("Variable numérica", numericas)
        cat = st.selectbox("Variable categórica", categoricas)

        st.dataframe(df.groupby(cat)[num].mean())

    with tab8:
        st.subheader("🔁 Categórico vs Categórico")

        cat1 = st.selectbox("Primera variable", categoricas, key="cat1")
        cat2 = st.selectbox("Segunda variable", categoricas, key="cat2")

        tabla = pd.crosstab(
            df[cat1],
            df[cat2],
            normalize="index"
        ) * 100

        st.dataframe(tabla.round(2))

    with tab9:
        st.subheader("🎛️ Análisis dinámico")

        cols = st.multiselect("Selecciona columnas", df.columns.tolist())
        if cols:
            st.dataframe(df[cols].head())

    with tab10:
        st.header("🔑 Hallazgos claves")

        st.markdown("---")

        st.write("""🔑
                             
        1️⃣ Incremento de la fuga asociado a cambios en el contexto
        Se observa un aumento del ratio de churn del 2% al 2.5%, coincidiendo con el periodo de coyuntura COVID-19.
        Este incremento sugiere que factores externos (económicos y operativos) influyen directamente en el comportamiento de los clientes.

        2️⃣ Relación entre antigüedad del cliente y fuga
        Los clientes con menor tenure presentan una mayor tasa de cancelación.
        Esto indica una etapa temprana crítica, donde la experiencia inicial impacta fuertemente en la retención.

        3️⃣ Impacto de los cargos mensuales
        Los clientes con MonthlyCharges más altos muestran una mayor propensión a la fuga.
        En contextos de incertidumbre económica, el precio se convierte en un factor determinante.

        4️⃣ Diferencias claras por tipo de contrato
        Los contratos mensuales concentran una mayor proporción de churn frente a contratos de mayor plazo.
        Esto evidencia que la flexibilidad contractual también implica mayor riesgo de fuga.

        5️⃣ Servicios y tipo de conectividad
        Se identifican variaciones en la fuga según el tipo de servicio contratado.
        Algunos servicios presentan mayor cancelación, lo que sugiere posibles problemas de valor percibido o calidad.
        """)

elif modulo == "Conclusiones":

    st.markdown("""
        <style>
            .card {
                background-color: #f5f5f5;
                padding: 3rem;
                border-radius: 25px;
                margin: 2.5rem auto;
                max-width: 2000px;
                min-height: 420px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            }

            .card h2 {
                text-align: center;
                margin-bottom: 2rem;
            }

            .card p {
                font-size: 1.05rem;
                line-height: 1.7;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
        <h2>🧠 CONCLUSIONES FINALES</h2>

        <b>1️⃣ La retención es financieramente prioritaria</b><br>
        Dado que adquirir un nuevo cliente cuesta entre 6 y 7 veces más que retener uno existente,
        incluso un aumento de 0.5 pp en churn representa un impacto económico significativo.
        </p>

        <p>
        <b>2️⃣ La etapa inicial del cliente es clave</b><br>
        Los clientes nuevos presentan mayor riesgo de fuga, por lo que es fundamental reforzar estrategias
        de onboarding, acompañamiento y comunicación temprana.
        </p>

        <p>
        <b>3️⃣ El precio influye más en contextos de crisis</b><br>
        Los cargos mensuales elevados incrementan la probabilidad de churn, lo que sugiere evaluar planes flexibles,
        descuentos temporales o beneficios adicionales durante periodos de incertidumbre.
        </p>

        <p>
        <b>4️⃣ El tipo de contrato es un factor estratégico</b><br>
        Los contratos de corto plazo muestran mayor rotación, por lo que se recomienda incentivar contratos
        de mayor duración mediante beneficios claros para el cliente.
        </p>

        <p>
        <b>5️⃣ El análisis exploratorio permite accionar sin predecir</b><br>
        El EDA permite identificar patrones claros de comportamiento y priorizar acciones concretas de retención,
        sin necesidad de construir modelos predictivos en esta etapa.
        </p>
        </div>

        """, unsafe_allow_html=True)
