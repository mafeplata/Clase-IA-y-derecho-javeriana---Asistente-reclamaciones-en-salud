"""
ReclamaSalud — Asistente de Reclamaciones de Salud ante la EPS
Proyecto Final: Derecho e Inteligencia Artificial
Pontificia Universidad Javeriana · 2026-II
Docente: Pedro Ardila
Estudiante: Maria Fernanda Plata Silva

Aplicación interactiva construida en Streamlit con motor RAG sobre corpus normativo colombiano.
"""

import os
import json
import datetime
import requests
import streamlit as st
from src.rag_engine import CorpusRAG

# Configuración de página
st.set_page_config(
    page_title="ReclamaSalud — Asistente de Reclamaciones",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar motor RAG
@st.cache_resource
def get_rag():
    return CorpusRAG()

rag = get_rag()

# -----------------------------------------------------------------------------
# ADVERTENCIA OBLIGATORIA (Banner superior permanente)
# -----------------------------------------------------------------------------
st.warning(
    "⚖️ **ADVERTENCIA OBLIGATORIA (EJERCICIO ACADÉMICO):**\n\n"
    "Esta herramienta es un ejercicio estrictamente académico desarrollado en el marco de la clase "
    "de Derecho e Inteligencia Artificial de la Pontificia Universidad Javeriana. "
    "**No constituye asesoría legal, no ofrece orientación médica y no sustituye la consulta con un abogado titulado, "
    "un profesional de la salud o las autoridades competentes.** En caso de una emergencia médica vital, comuníquese "
    "de inmediato con la línea 123 o acuda al centro asistencial de urgencias más cercano."
)

# -----------------------------------------------------------------------------
# BARRA LATERAL (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Logo_Pontificia_Universidad_Javeriana.svg/1200px-Logo_Pontificia_Universidad_Javeriana.svg.png", width=160)
    st.title("⚖️ ReclamaSalud")
    st.caption("**Pontificia Universidad Javeriana · 2026-II**")
    st.markdown("**Estudiante:** Maria Fernanda Plata Silva  \n**Docente:** Pedro Ardila")
    
    st.divider()
    
    st.markdown("### 🔒 Privacidad y Datos (Ley 1581/12)")
    st.info(
        "Esta versión académica **no almacena historias clínicas ni datos personales** en bases de datos. "
        "Para realizar las pruebas, utiliza **nombres y situaciones ficticias**."
    )
    
    st.divider()
    
    st.markdown("### ⚙️ Configuración del Modelo")
    api_key = st.text_input(
        "OpenRouter API Key (Opcional)",
        type="password",
        value=st.secrets.get("OPENROUTER_API_KEY", "") if hasattr(st, "secrets") else "",
        help="Si no ingresas una clave, el sistema utilizará el generador de plantilla jurídica autónomo con RAG."
    )
    
    selected_model = st.selectbox(
        "Modelo de Lenguaje (OpenRouter)",
        [
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
        ],
        index=0
    )
    
    st.divider()
    st.markdown("### 📚 Corpus Conectado")
    st.markdown(f"**Total de fragmentos jurídicos indexados:** `{len(rag.documents)}`")
    with st.expander("Ver fuentes normativas"):
        st.markdown(
            "- Constitución Política (Arts. 23, 48, 49)\n"
            "- Ley Estatutaria 1751 de 2015\n"
            "- Ley 1755 de 2015 (Petición)\n"
            "- Resolución 229 de 2020 (MinSalud)\n"
            "- Circular 2023151000000010-5 (Supersalud)\n"
            "- Sentencia T-760 de 2008 (Corte Const.)"
        )

# -----------------------------------------------------------------------------
# ENCABEZADO PRINCIPAL
# -----------------------------------------------------------------------------
col_logo, col_text = st.columns([1, 6])
with col_logo:
    st.markdown("# 🏥")
with col_text:
    st.title("ReclamaSalud — Asistente de Reclamaciones ante EPS")
    st.markdown("#### *Organiza tu caso y crea una reclamación clara para tu EPS fundamentada en la ley colombiana.*")

st.divider()

# -----------------------------------------------------------------------------
# ENTREVISTA GUIADA POR PASOS
# -----------------------------------------------------------------------------
st.subheader("📋 Entrevista Guiada de Reclamación")
st.write("Diligencia los siguientes campos para que el asistente organice los hechos y fundamente la reclamación jurídica.")

with st.container():
    # --- BLOQUE 1: DATOS DE AFILIACIÓN ---
    st.markdown("### 1️⃣ Datos de Afiliación y Contacto")
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre_usuario = st.text_input("Nombre del paciente o peticionario (Usa nombre ficticio):", value="Carmen Silva (Simulado)")
        rol_usuario = st.selectbox("¿Quién presenta la reclamación?", [
            "El paciente directamente",
            "Familiar / Cuidador autorizado del paciente",
            "Representante legal (menor o persona con discapacidad)"
        ])
    with col2:
        eps_nombre = st.selectbox("Entidad Promotora de Salud (EPS):", [
            "EPS Sanitas", "Nueva EPS", "Sura EPS", "Salud Total EPS",
            "Famisanar EPS", "Compensar EPS", "Savia Salud EPS", "Otra EPS"
        ])
        if eps_nombre == "Otra EPS":
            eps_nombre = st.text_input("Escribe el nombre de la EPS:")
        regimen = st.selectbox("Régimen de Afiliación:", ["Contributivo (Cotizante)", "Contributivo (Beneficiario)", "Subsidiado"])
    with col3:
        ciudad = st.text_input("Ciudad / Municipio de residencia:", value="Bogotá D.C.")
        cedula_simulada = st.text_input("Número de documento ficticio:", value="1.020.304.050")

    st.divider()

    # --- BLOQUE 2: TIPO DE PROBLEMA EN SALUD ---
    st.markdown("### 2️⃣ Tipo de Barrera o Problema con la EPS")
    tipo_barrera = st.selectbox(
        "Selecciona el problema principal que experimentas:",
        [
            "Negativa o demora injustificada en entrega de medicamentos (fórmulas pendientes)",
            "Falta de asignación o demora desproporcionada de cita médica (general o especialista)",
            "Falta de autorización o programación de exámenes diagnósticos o cirugías",
            "Interrupción injustificada de un tratamiento médico continuo",
            "Barrera administrativa o traslado indebido de trámites burocráticos al paciente"
        ]
    )

    st.divider()

    # --- BLOQUE 3: TRIAGE ÉTICO Y CRONOLOGÍA DE LOS HECHOS ---
    st.markdown("### 3️⃣ Cronología de los Hechos y Triage de Seguridad")

    # DETECTOR DE ALARMA MÉDICA (TRIAGE ÉTICO)
    es_urgencia = st.checkbox(
        "⚠️ **ALERTA MÉDICA:** Marque esta casilla si el paciente presenta actualmente dolor torácico agudo (pecho), dificultad respiratoria severa, pérdida de conocimiento o riesgo vital inminente.",
        value=False
    )

    if es_urgencia:
        st.error(
            "🚨 **ALERTA DE EMERGENCIA MÉDICA VITAL — ACCIÓN INMEDIATA REQUERIDA** 🚨\n\n"
            "**¡DETENGA EL TRÁMITE DE ESTE DOCUMENTO!**\n\n"
            "Los síntomas descritos corresponden a una posible urgencia médica vital que no admite esperas burocráticas ni cartas escritas.\n\n"
            "1. **Comuníquese de inmediato a la línea de emergencias 123** en Colombia o traslade al paciente a la sala de urgencias de la clínica u hospital más cercano.\n"
            "2. **Fundamento legal de protección inmediata:** Conforme al **artículo 14 de la Ley Estatutaria 1751 de 2015**, **TODAS** las clínicas y hospitales de Colombia (públicas y privadas) están obligadas a prestar atención inicial de urgencias de forma obligatoria e inmediata, **sin exigir autorizaciones de la EPS, sin cita previa y sin cobro de copagos ni pagos anticipados**.\n\n"
            "*La vida y la salud inmediata son la prioridad absoluta.*"
        )
    else:
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            fecha_orden = st.date_input("Fecha de la orden o fórmula médica:", datetime.date(2026, 1, 15))
            medico_tratante = st.text_input("Médico o especialidad que ordenó el servicio:", value="Dr. Médico Tratante / Medicina Interna")
            servicio_solicitado = st.text_input("Nombre del medicamento, cita o examen solicitado:", value="Losartán 50mg y Amlodipino")
        with col_f2:
            relato_hechos = st.text_area(
                "Describe cronológicamente lo sucedido (trámites realizados, respuestas de la EPS, tiempo de espera y consecuencias en la salud):",
                value="El 15 de enero de 2026 acudí al punto de dispensación de medicamentos asignado por la EPS con la fórmula médica n.° 88452. Me informaron que el medicamento se encontraba agotado y me sellaron la orden como pendiente. Han transcurrido más de seis semanas, he llamado reiteradamente a la línea telefónica donde solo me dicen que sigue agotado y a la fecha la paciente se encuentra sin dosis, lo que ha generado descompensación en su presión arterial.",
                height=140
            )

    st.divider()

    # --- BLOQUE 4: DOCUMENTOS DE SOPORTE ---
    st.markdown("### 4️⃣ Documentos y Pruebas Disponibles")
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        tiene_formula = st.checkbox("Copia de orden médica o fórmula expedida por el médico tratante", value=True)
        tiene_pendiente = st.checkbox("Constancia de sello de 'pendiente' o comprobante de solicitud ante farmacia", value=True)
    with col_an2:
        tiene_radicado = st.checkbox("Número de radicado o reclamo previo ante la EPS", value=False)
        tiene_documento_id = st.checkbox("Copia de documento de identidad del paciente y peticionario", value=True)

# -----------------------------------------------------------------------------
# PROCESAMIENTO Y GENERACIÓN DEL DOCUMENTO
# -----------------------------------------------------------------------------
st.write("")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar_btn = st.button("⚖️ Generar Borrador de Reclamación ante la EPS", type="primary", use_container_width=True, disabled=es_urgencia)

if generar_btn and not es_urgencia:
    with st.spinner("Consultando el corpus normativo colombiano y estructurando la reclamación..."):
        # 1. Búsqueda RAG sobre el corpus normativo
        consulta_rag = f"{tipo_barrera} {servicio_solicitado} {relato_hechos}"
        documentos_recuperados = rag.search(consulta_rag, top_k=3)
        contexto_rag = rag.get_formatted_context(consulta_rag, top_k=3)

        # 2. Generación del borrador formal
        borrador_texto = f"""Señores:
{eps_nombre.upper()}
Atención: Oficina de Peticiones, Quejas, Reclamos y Solicitudes (PQRS) / Gerencia de Servicio al Cliente
Ciudad: {ciudad}
Canal de radicación: [CORREO ELECTRÓNICO O PORTAL DE PQRD DE LA EPS]

ASUNTO: DERECHO DE PETICIÓN EN INTERÉS PARTICULAR (ARTÍCULO 23 DE LA CONSTITUCIÓN POLÍTICA Y LEY 1755 DE 2015) CON FUNDAMENTO EN EL DERECHO FUNDAMENTAL A LA SALUD (LEY ESTATUTARIA 1751 DE 2015).

Peticionario(a): {nombre_usuario}
Documento de Identidad: C.C. {cedula_simulada}
Calidad: Afiliado(a) en régimen {regimen}
Calidad de actuación: {rol_usuario}
Municipio de atención: {ciudad}

Yo, {nombre_usuario}, mayor de edad, identificado(a) como aparece al pie de mi firma, en ejercicio del derecho fundamental de petición consagrado en el artículo 23 de la Constitución Política y en la Ley 1755 de 2015, y en garantía del derecho fundamental autónomo e irrenunciable a la salud consagrado en la Ley Estatutaria 1751 de 2015, acudo respetuosamente ante su despacho con fundamento en los siguientes:

I. HECHOS
1. Me encuentro válidamente afiliado(a) a la entidad {eps_nombre} en calidad de {regimen} en el municipio de {ciudad}.
2. Con fecha {fecha_orden.strftime('%d de %B de %Y')}, el profesional adscrito a su red prestadora, {medico_tratante}, prescribió y ordenó formalmente el servicio consistente en: {servicio_solicitado}.
3. Hechos y trámites surtidos: {relato_hechos}
4. A la fecha de radicación de la presente petición, han transcurrido términos desproporcionados sin que la entidad garantice de manera continua, efectiva y oportuna el servicio ordenado, incurriendo en una dilación administrativa injustificada.
5. Dicha conducta lesiona el principio de continuidad e integralidad del tratamiento, trasladando de manera indebida a la parte usuaria cargas burocráticas y deficiencias de inventario o contratación que corresponden exclusivamente a la gestión de la EPS.

II. PETICIONES
1. Se AUTORICE Y GARANTICE DE FORMA INMEDIATA, OPORTUNA Y EFECTIVA la entrega / asignación / realización de: {servicio_solicitado}, prescrito por el médico tratante.
2. Se garantice la CONTINUIDAD E INTEGRALIDAD del tratamiento médico, disponiendo los ciclos, citas de control o entregas subsecuentes sin interrupciones, dilaciones ni exigencia de trámites administrativos no contemplados en la ley.
3. Se remita respuesta motivada, clara y de fondo a la presente petición en los términos perentorios fijados por la Ley 1755 de 2015 y la Circular Externa 2023151000000010-5 de la Superintendencia Nacional de Salud, informando las gestiones concretas adelantadas y la red de prestadores habilitada.

III. FUNDAMENTOS DE DERECHO
Sustento esta reclamación en las siguientes disposiciones del ordenamiento jurídico colombiano:
1. Constitución Política de Colombia: Artículo 23 (Derecho fundamental de petición) y Artículo 49 (Atención a la salud como servicio público esencial a cargo del Estado).
2. Ley Estatutaria 1751 de 2015:
   - Artículos 2 y 6: Consagran la salud como derecho fundamental y consagran los principios rectores de OPORTUNIDAD, CONTINUIDAD, ACCESIBILIDAD e INTEGRALIDAD.
   - Artículo 8: Principio de integralidad (prohibición expresa de fragmentar la atención o imponer barreras burocráticas).
   - Artículo 10: Derecho del paciente a recibir atención oportuna y a que no se le trasladen cargas administrativas de las entidades.
3. Ley 1755 de 2015: Artículos 13, 14, 16 y 32, que vinculan a las entidades prestadoras de servicios públicos esenciales como las EPS a resolver las peticiones dentro de los términos perentorios de ley mediante respuestas completas y de fondo.
4. Resolución 229 de 2020 del Ministerio de Salud: Carta de derechos y deberes del paciente, reconociendo el derecho a la entrega completa de medicamentos (con obligación de suministro en un plazo máximo de 48 horas cuando quedan pendientes) y la asignación oportuna de citas médicas.
5. Circular Externa 2023151000000010-5 de 2023 de la Superintendencia Nacional de Salud: Instrucciones sobre clasificación de riesgos y términos prioritarios en la resolución de quejas y reclamos en salud.
6. Jurisprudencia de la Corte Constitucional (Sentencia T-760 de 2008): Establece como subreglas vinculantes la prohibición de trasladar trámites burocráticos al paciente y la garantía estricta de continuidad en la provisión de servicios y medicamentos esenciales.

IV. PRUEBAS Y ANEXOS
Para que obren como prueba, anexo copia simple de:
{'- Copia de la orden médica o fórmula prescrita vigente.' if tiene_formula else ''}
{'- Copia de constancia de solicitud / sello de pendiente de farmacia.' if tiene_pendiente else ''}
{'- Copia del radicado de solicitud o reclamo anterior ante la EPS.' if tiene_radicado else ''}
{'- Copia de los documentos de identidad correspondientes.' if tiene_documento_id else ''}

V. NOTIFICACIONES
Recibiré respuesta a la presente solicitud en:
Ciudad: {ciudad}
Dirección física: [INDICAR DIRECCIÓN COMPLETA PARA NOTIFICACIÓN]
Teléfono de contacto: [INDICAR NÚMERO DE TELÉFONO O CELULAR]
Correo electrónico para notificaciones: [INDICAR CORREO ELECTRÓNICO]

Atentamente,

___________________________________________
FIRMA
Nombre: {nombre_usuario}
C.C. n.° {cedula_simulada}
{f'En calidad de: {rol_usuario}' if 'paciente directamente' not in rol_usuario.lower() else ''}

================================================================================
ADVERTENCIA: Este documento es un borrador académico generado por ReclamaSalud. 
Verifique los datos entre corchetes antes de radicar. No constituye asesoría legal formal.
================================================================================
"""

        # Guardar en estado de sesión
        st.session_state["borrador_generado"] = borrador_texto
        st.session_state["documentos_recuperados"] = documentos_recuperados
        st.session_state["contexto_rag"] = contexto_rag

# -----------------------------------------------------------------------------
# VISUALIZACIÓN DE RESULTADOS
# -----------------------------------------------------------------------------
if "borrador_generado" in st.session_state and not es_urgencia:
    st.success("✅ Reclamación jurídica estructurada y fundamentada exitosamente.")
    
    tab_doc, tab_resumen, tab_fuentes = st.tabs([
        "📄 Borrador de Derecho de Petición",
        "📊 Resumen del Caso",
        "🔍 Fuentes Jurídicas del Corpus (RAG)"
    ])

    with tab_doc:
        st.markdown("### Borrador Formal de Derecho de Petición ante la EPS")
        st.caption("Revisa el texto, completa los campos entre corchetes `[...]` y utiliza el botón inferior para descargarlo.")
        st.text_area("Texto de la reclamación:", value=st.session_state["borrador_generado"], height=480)
        
        col_d1, col_d2 = st.columns([1, 2])
        with col_d1:
            st.download_button(
                label="📥 Descargar Documento (.txt)",
                data=st.session_state["borrador_generado"],
                file_name=f"derecho_peticion_{eps_nombre.replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_d2:
            st.info("💡 **Cómo radicar:** Envía este documento por el portal de PQRS de tu EPS o radícalo en su oficina de atención al usuario, exigiendo siempre sello de recibido con fecha y número de radicado.")

    with tab_resumen:
        st.markdown("### 📊 Ficha Resumen del Caso")
        st.write(f"**Peticionario(a):** {nombre_usuario}")
        st.write(f"**EPS Reclamada:** {eps_nombre}")
        st.write(f"**Régimen y Ciudad:** {regimen} · {ciudad}")
        st.write(f"**Barrera Identificada:** {tipo_barrera}")
        st.write(f"**Servicio Involucrado:** {servicio_solicitado}")
        st.write(f"**Fecha de prescripción médica:** {fecha_orden.strftime('%d/%m/%Y')}")

    with tab_fuentes:
        st.markdown("### 🔍 Artículos y Subreglas Recuperadas del Corpus (RAG)")
        st.write("El asistente recuperó los siguientes fragmentos de fuentes oficiales para sustentar la reclamación:")
        for idx, doc in enumerate(st.session_state.get("documentos_recuperados", []), 1):
            with st.expander(f"📌 [Fuente {idx}] {doc['source_title']} — {doc['section']}"):
                st.code(doc["text"], language="text")

# -----------------------------------------------------------------------------
# PIE DE PÁGINA
# -----------------------------------------------------------------------------
st.divider()
st.caption(
    "⚖️ **ReclamaSalud** · Pontificia Universidad Javeriana · Facultad de Ciencias Jurídicas · 2026-II · "
    "Construido con Streamlit, LangChain y Python para la clase de Derecho e Inteligencia Artificial."
)
