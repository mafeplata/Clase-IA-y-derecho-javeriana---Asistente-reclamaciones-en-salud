"""
ReclamaSalud — Asistente de Reclamaciones de Salud ante la EPS
Proyecto Final: Derecho e Inteligencia Artificial
Pontificia Universidad Javeriana · 2026-II
Docente: Pedro Ardila
Estudiante: Maria Fernanda Plata Silva

Aplicación interactiva en Streamlit con:
1. Calculadora de términos legales y semáforo de riesgo (Ley 1755/15 y Circular Supersalud)
2. Directorio oficial de canales de radicación de cada EPS y Supersalud
3. Exportación formal a PDF maquetado con membrete judicial (fpdf2) y .txt
4. Hoja de ruta interactiva post-reclamación (Escalamiento a Supersalud y Acción de Tutela)
5. Motor RAG sobre corpus normativo colombiano y salvaguarda de triage para urgencias médicas.
"""

import os
import sys
import re
import datetime
import requests
import urllib.parse
import streamlit as st

# Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# -----------------------------------------------------------------------------
# 1. MOTOR RAG (Importación con fallback autónomo para evitar caídas)
# -----------------------------------------------------------------------------
try:
    from src.rag_engine import CorpusRAG
except Exception:
    class CorpusRAG:
        """Fallback local autónomo de RAG si no se encuentra la carpeta src/."""
        def __init__(self, corpus_dir=None):
            self.corpus_dir = os.path.join(BASE_DIR, "corpus") if corpus_dir is None else corpus_dir
            self.documents = []
            self._load()

        def _load(self):
            if not os.path.exists(self.corpus_dir):
                return
            for fname in sorted(os.listdir(self.corpus_dir)):
                if not fname.endswith(".txt"):
                    continue
                fpath = os.path.join(self.corpus_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    lines = content.split("\n")
                    header = lines[0].replace("#", "").strip() if lines else fname
                    chunks = re.split(r"\n(?=(?:ARTÍCULO\s+\d+|[0-9]+\.\s+[A-ZÁÉÍÓÚÑ]))", content)
                    for idx, c in enumerate(chunks):
                        c_clean = c.strip()
                        if not c_clean or c_clean.startswith("#"):
                            continue
                        first_l = c_clean.split("\n")[0].replace("#", "").strip()
                        self.documents.append({
                            "id": f"{fname}_{idx}",
                            "source_title": header,
                            "section": first_l,
                            "text": c_clean
                        })
                except Exception:
                    pass

        def search(self, query, top_k=3):
            if not self.documents:
                return []
            q_terms = set(re.findall(r"\b\w{4,}\b", query.lower()))
            scored = []
            for d in self.documents:
                text_l = (d["text"] + " " + d["section"]).lower()
                score = sum(text_l.count(t) for t in q_terms)
                if score > 0:
                    scored.append((score, d))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [d for _, d in scored[:top_k]]

        def get_formatted_context(self, query, top_k=3):
            res = self.search(query, top_k=top_k)
            if not res:
                return "Corpus oficial colombiano consultado."
            parts = [f"[{d['source_title']} - {d['section']}]:\n{d['text']}" for d in res]
            return "\n\n".join(parts)

# -----------------------------------------------------------------------------
# 2. DIRECTORIO OFICIAL DE CANALES DE RADICACIÓN POR EPS
# -----------------------------------------------------------------------------
DIRECTORIO_EPS = {
    "EPS Sanitas": {
        "nombre_completo": "Entidad Promotora de Salud Sanitas S.A.S.",
        "portal_web": "https://www.epssanitas.com",
        "portal_pqrs": "https://www.epssanitas.com",
        "telefono_nacional": "01 8000 919 100",
        "telefono_bogota": "(601) 375 9000",
        "consejo_radicacion": "Ingresa al portal web oficial de EPS Sanitas con tu tipo y número de documento en la sección 'Oficina Virtual' para radicar en línea, o acude presencialmente a tu centro de atención exigiendo copia sellada con fecha y número de radicado."
    },
    "Nueva EPS": {
        "nombre_completo": "Nueva EPS S.A.",
        "portal_web": "https://www.nuevaeps.com.co",
        "portal_pqrs": "https://www.nuevaeps.com.co",
        "telefono_nacional": "01 8000 954 400 (Contributivo) / 01 8000 952 000 (Subsidiado)",
        "telefono_bogota": "(601) 307 7022",
        "consejo_radicacion": "Ingresa al portal web oficial de Nueva EPS e inicia sesión en 'Oficina Virtual' para tramitar tu solicitud, o radica por escrito en la Oficina de Atención al Afiliado más cercana."
    },
    "Sura EPS": {
        "nombre_completo": "EPS y Medicina Prepagada Suramericana S.A.",
        "portal_web": "https://www.epssura.com",
        "portal_pqrs": "https://www.epssura.com",
        "telefono_nacional": "01 8000 519 519",
        "telefono_bogota": "(601) 489 7941",
        "consejo_radicacion": "Accede a www.epssura.com e inicia sesión en 'Servicios en Línea' con tu usuario para radicar y hacer seguimiento a tu reclamo, o llama a su línea nacional de atención."
    },
    "Salud Total EPS": {
        "nombre_completo": "Salud Total EPS del Régimen Contributivo S.A.",
        "portal_web": "https://saludtotal.com.co",
        "portal_pqrs": "https://saludtotal.com.co",
        "telefono_nacional": "01 8000 1 14524",
        "telefono_bogota": "(601) 485 4555",
        "consejo_radicacion": "Ingresa a saludtotal.com.co e identifícate en el 'Punto de Atención al Usuario (PAU) Virtual' con tu cédula y contraseña para registrar tu PQRD con constancia inmediata."
    },
    "Famisanar EPS": {
        "nombre_completo": "EPS Famisanar SAS",
        "portal_web": "https://www.famisanar.com.co",
        "portal_pqrs": "https://www.famisanar.com.co",
        "telefono_nacional": "01 8000 116 662 (Contributivo) / 01 8000 914 202 (Subsidiado)",
        "telefono_bogota": "(601) 307 8069",
        "consejo_radicacion": "Ingresa al portal oficial de Famisanar en 'Oficina Virtual' para radicar en línea, o acude a los Centros de Atención al Usuario (CAU) con copia física del documento."
    },
    "Compensar EPS": {
        "nombre_completo": "Compensar Entidad Promotora de Salud",
        "portal_web": "https://www.compensar.com",
        "portal_pqrs": "https://www.compensar.com",
        "telefono_nacional": "01 8000 915 202",
        "telefono_bogota": "(601) 444 1234",
        "consejo_radicacion": "Ingresa a compensar.com en el módulo de Salud y accede con tus credenciales a 'Transacciones en Línea' para registrar tu queja o reclamo."
    },
    "Savia Salud EPS": {
        "nombre_completo": "Alianza Medellín Antioquia EPS S.A.S. - Savia Salud",
        "portal_web": "https://www.saviasaludeps.com",
        "portal_pqrs": "https://www.saviasaludeps.com",
        "telefono_nacional": "01 8000 423 683",
        "telefono_bogota": "Línea Medellín: (604) 448 1747",
        "consejo_radicacion": "Ingresa a saviasaludeps.com en la sección 'Atención al Ciudadano' o radica en la oficina de atención municipal más cercana."
    }
}

CANAL_SUPERSALUD = {
    "entidad": "Superintendencia Nacional de Salud (Supersalud)",
    "portal_web": "https://www.supersalud.gov.co",
    "portal_pqrs": "https://www.supersalud.gov.co",
    "linea_gratuita_nacional": "01 8000 513 700",
    "telefono_bogota": "(601) 744 2000"
}

def get_eps_info(nombre_eps: str) -> dict:
    for key, data in DIRECTORIO_EPS.items():
        if key.lower() in nombre_eps.lower():
            return data
    return {
        "nombre_completo": nombre_eps,
        "portal_web": "https://www.supersalud.gov.co",
        "portal_pqrs": "https://www.supersalud.gov.co",
        "telefono_nacional": "Línea de atención de la entidad",
        "telefono_bogota": "Consultar en la página oficial",
        "consejo_radicacion": "Radica por la página web de la EPS o en su sede de atención al usuario exigiendo copia con sello y radicado."
    }

# -----------------------------------------------------------------------------
# 3. GENERADOR DE PDF FORMAL (Con soporte de fpdf2)
# -----------------------------------------------------------------------------
try:
    from fpdf import FPDF
    FPDF_INSTALADO = True
except ImportError:
    FPDF_INSTALADO = False

def generar_pdf_derecho_peticion(texto_peticion: str) -> bytes:
    """Genera un archivo PDF con formato judicial elegante a partir del texto."""
    if not FPDF_INSTALADO:
        return b""

    class PDFDoc(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(100, 110, 120)
            self.cell(0, 5, "RECLAMASALUD — ASISTENTE ACADEMICO | PONTIFICIA UNIVERSIDAD JAVERIANA", 0, 1, "C")
            self.set_draw_color(180, 190, 200)
            self.line(20, 14, 190, 14)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(140, 140, 140)
            self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}} - Ejercicio del Derecho de Peticion (Ley 1755 de 2015)", 0, 0, "C")

    # Limpieza de caracteres para latin-1
    t = texto_peticion
    for k, v in {"—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...", "•": "*"}.items():
        t = t.replace(k, v)
    t = re.sub(r"[^\x00-\xFF]", "", t)

    pdf = PDFDoc(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.alias_nb_pages()
    pdf.add_page()

    for line in t.split("\n"):
        s = line.strip()
        if s.startswith("====") or s.startswith("----"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(3)
        elif re.match(r"^(I|II|III|IV|V)\.\s+[A-Z\s]+", s) or s.startswith("ASUNTO:"):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 30, 60)
            pdf.multi_cell(0, 5, s)
            pdf.ln(1)
        elif s.startswith("Señores:") or s.startswith("Senores:") or s.startswith("Peticionario") or s.startswith("Atentamente,"):
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(30, 40, 50)
            pdf.multi_cell(0, 5, s)
            pdf.ln(1)
        elif "ADVERTENCIA:" in s:
            pdf.ln(2)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(120, 30, 30)
            pdf.multi_cell(0, 4, s)
        else:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(20, 25, 30)
            if s:
                pdf.multi_cell(0, 5, s)
            else:
                pdf.ln(2)

    return bytes(pdf.output())

# -----------------------------------------------------------------------------
# 4. CALCULADORA DE TÉRMINOS LEGALES Y SEMÁFORO
# -----------------------------------------------------------------------------
def calcular_terminos_legales(fecha_solicitud, tipo_barrera):
    hoy = datetime.date.today()
    if fecha_solicitud > hoy:
        return 0, 0, "verde", "Fecha futura o del día de hoy."

    dias_calendario = (hoy - fecha_solicitud).days
    dias_habiles = 0
    cur = fecha_solicitud
    while cur < hoy:
        cur += datetime.timedelta(days=1)
        if cur.weekday() < 5:
            dias_habiles += 1

    es_medicamento = "medicamento" in tipo_barrera.lower()

    if es_medicamento:
        if dias_calendario <= 2:
            estado = "verde"
            mensaje = f"🟢 DENTRO DEL TÉRMINO LEGAL: Han transcurrido {dias_calendario} de 2 días máximos permitidos para entrega de fórmulas pendientes (Res. 229 de 2020)."
        elif dias_calendario <= 5:
            estado = "amarillo"
            mensaje = f"🟡 PLAZO DE ENTREGA VENCIDO: Han transcurrido {dias_calendario} días desde la orden. La farmacia/EPS está en mora. Debes radicar de inmediato la petición formal."
        else:
            estado = "rojo"
            mensaje = f"🔴 MORA GRAVE E INJUSTIFICADA: Han transcurrido {dias_calendario} días sin medicamentos. Hay vulneración de los principios de oportunidad y continuidad (Ley 1751/2015). Se habilita queja ante Supersalud y Acción de Tutela."
    else:
        if dias_habiles <= 10:
            estado = "verde"
            mensaje = f"🟢 DENTRO DEL TÉRMINO ORDINARIO: Han transcurrido {dias_habiles} de 15 días hábiles. La entidad aún dispone de plazo legal para gestionar la solicitud."
        elif dias_habiles <= 15:
            estado = "amarillo"
            mensaje = f"🟡 TÉRMINO PRÓXIMO A VENCER: Han transcurrido {dias_habiles} de 15 días hábiles. Si no recibes respuesta en los próximos días, se configurará silencio administrativo."
        else:
            estado = "rojo"
            mensaje = f"🔴 TÉRMINO LEGAL VENCIDO: Han transcurrido {dias_habiles} días hábiles (más de los 15 permitidos por la Ley 1755 de 2015). Se ha configurado una dilación administrativa injustificada."

    return dias_calendario, dias_habiles, estado, mensaje

# -----------------------------------------------------------------------------
# 5. SISTEMA DE ACCESIBILIDAD UNIVERSAL Y ASISTENCIA POR VOZ (WCAG 2.1)
# -----------------------------------------------------------------------------
def obtener_audio_es(texto: str) -> bytes:
    """Genera audio MP3 en español colombiano de forma robusta y rápida."""
    # 1. Intentar con gTTS si está disponible
    try:
        from gtts import gTTS
        import io
        texto_limpio = re.sub(r'[*_#=\-\[\]]', ' ', texto)
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        tts = gTTS(text=texto_limpio[:1200], lang='es', tld='com.co')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        pass

    # 2. Fallback inmediato con servicio TTS público de Google (sin librerías adicionales)
    try:
        import urllib.parse
        import requests
        texto_limpio = re.sub(r'[*_#=\-\[\]]', ' ', texto)
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        fragmento = texto_limpio[:350]
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=es&q={urllib.parse.quote(fragmento)}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
        if r.status_code == 200 and len(r.content) > 1000:
            return r.content
    except Exception:
        pass
    return b""


def render_lector_audio(texto: str, titulo: str = "Escuchar en voz alta", key: str = "audio_1"):
    """Muestra un botón de audio que al presionarse genera y reproduce voz en español nativa."""
    estado_key = f"reproducir_{key}"
    if st.button(f"🔊 {titulo}", key=f"btn_{key}", use_container_width=False):
        st.session_state[estado_key] = True

    if st.session_state.get(estado_key, False):
        with st.spinner("🎙️ Generando voz en español..."):
            audio_bytes = obtener_audio_es(texto)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                st.caption("ℹ️ *Usa los controles del reproductor para pausar, regular volumen o cambiar velocidad.*")
            else:
                st.info("ℹ️ No se pudo cargar el audio en este momento.")


def render_semaforo_accesible(est_semaforo, msg_semaforo, daltonismo_filtro):
    """Renderiza el semáforo con soporte daltónico (patrones, bordes, símbolos no cromáticos) y botón de audio."""
    if est_semaforo == "verde":
        badge_simbolo = "🟢 [ESTADO NORMAL: DENTRO DEL TÉRMINO LEGAL]"
        icono_dalt = "✔ CÍRCULO / PLAZO VIGENTE"
        if "Deuteranopía" in daltonismo_filtro or "Protanopía" in daltonismo_filtro:
            borde_estilo = "border: 2px solid #38BDF8; background-color: #0C4A6E; color: #FFFFFF;"
        else:
            borde_estilo = "border: 2px solid #22C55E; background-color: #064E3B; color: #FFFFFF;"
    elif est_semaforo == "amarillo":
        badge_simbolo = "🟡 [ALERTA PREVENTIVA: TÉRMINO PRÓXIMO A VENCER O EN MORA INICIAL]"
        icono_dalt = "▲ TRIÁNGULO / ADVERTENCIA"
        if "Deuteranopía" in daltonismo_filtro or "Protanopía" in daltonismo_filtro:
            borde_estilo = "border: 2px dashed #F59E0B; background-color: #78350F; color: #FFFFFF;"
        else:
            borde_estilo = "border: 2px dashed #EAB308; background-color: #713F12; color: #FFFFFF;"
    else:
        badge_simbolo = "🔴 [ALERTA LEGAL MÁXIMA: TÉRMINO VENCIDO / MORA INJUSTIFICADA]"
        icono_dalt = "✖ CUADRADO / MORA GRAVE"
        if "Deuteranopía" in daltonismo_filtro or "Protanopía" in daltonismo_filtro:
            borde_estilo = "border: 3px double #F87171; background-color: #7F1D1D; color: #FFFFFF;"
        else:
            borde_estilo = "border: 3px double #EF4444; background-color: #7F1D1D; color: #FFFFFF;"

    st.markdown(
        f"""
        <div style="{borde_estilo} padding: 14px 16px; border-radius: 8px; margin: 10px 0; font-family: sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="font-weight: 800; font-size: 14.5px; margin-bottom: 6px; color: #FFFFFF;">
                {badge_simbolo}
                <span style="font-size: 12.5px; font-weight: normal; margin-left: 8px; opacity: 0.95; color: #FFFFFF;">
                    (Guía visual accesible: {icono_dalt})
                </span>
            </div>
            <div style="font-size: 13.5px; line-height: 1.5; color: #FFFFFF;">
                {msg_semaforo}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    render_lector_audio(
        texto=f"Dictamen del semáforo legal. {msg_semaforo}",
        titulo="Escuchar dictamen del semáforo",
        key="tts_semaforo"
    )


def inyectar_css_accesibilidad(modo_apariencia, bg_col, text_col, card_col, btn_col, tam_fuente, interlineado, fuente_css, daltonismo_filtro="Sin filtro adicional"):
    """Inyecta reglas CSS dinámicas y elegantes sin romper la jerarquía visual de Streamlit."""
    
    # 1. Base tipográfica limpia para párrafos y lecturas
    css = f"""
    <style>
    /* Tipografía y lectura cómoda */
    .stApp, .stMarkdown p, .stMarkdown li, div[data-testid="stMarkdownContainer"] p {{
        font-family: {fuente_css} !important;
        font-size: {tam_fuente}px !important;
        line-height: {interlineado} !important;
    }}
    
    /* Jerarquía de encabezados protegida y proporcional */
    h1, [data-testid="stHeader"] h1 {{
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        color: #004B87 !important;
        line-height: 1.25 !important;
    }}
    h2 {{
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1E293B !important;
        line-height: 1.3 !important;
    }}
    h3 {{
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #1E293B !important;
        line-height: 1.35 !important;
    }}
    h4 {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }}

    /* ETIQUETAS DE CAMPOS: 100% VISIBLES, OSCURAS Y LEGIBLES */
    label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stMarkdown label {{
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
        display: block !important;
        margin-bottom: 5px !important;
    }}

    /* CAMPOS DE TEXTO E INPUTS: FONDO BLANCO, BORDES CLAROS Y TEXTO OSCURO */
    input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #94A3B8 !important;
        border-radius: 8px !important;
        font-size: {tam_fuente}px !important;
    }}

    /* Texto seleccionado y foco */
    input[type="text"]:focus, textarea:focus {{
        border-color: #004B87 !important;
        box-shadow: 0 0 0 3px rgba(0, 75, 135, 0.25) !important;
    }}

    /* Placeholders en cursiva suave pero visible */
    input::placeholder, textarea::placeholder {{
        color: #64748B !important;
        opacity: 0.9 !important;
    }}

    /* Desplegables de Streamlit */
    div[data-baseweb="popover"], div[data-baseweb="menu"] {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }}

    /* Expanders limpios */
    [data-testid="stExpander"] {{
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        background-color: #F8FAFC !important;
    }}
    [data-testid="stExpander"] summary {{
        font-weight: 700 !important;
        color: #004B87 !important;
    }}
    """

    # 2. Modos de contraste específicos
    if "Estándar Javeriana" in modo_apariencia:
        css += """
        /* TEMA INSTITUCIONAL JAVERIANA ALTO CONTRASTE (AZUL NOCHE Y ORO) */
        .stApp {
            background-color: #0A192F !important;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] {
            background-color: #071224 !important;
            border-right: 2px solid #1E3A5F !important;
        }
        h1, [data-testid="stHeader"] h1 {
            color: #FFC72C !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4) !important;
        }
        h2, h3 {
            color: #93C5FD !important;
        }
        h4, h5, h6 {
            color: #E2E8F0 !important;
        }
        .main p, .main li, div[data-testid="stMarkdownContainer"] p {
            color: #F8FAFC !important;
        }
        label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stMarkdown label {
            color: #FFD166 !important;
            font-weight: 700 !important;
            font-size: 0.98rem !important;
            letter-spacing: 0.3px !important;
        }
        input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {
            background-color: #112240 !important;
            color: #FFFFFF !important;
            border: 2px solid #38BDF8 !important;
            border-radius: 8px !important;
        }
        input[type="text"]:focus, textarea:focus {
            border-color: #FFC72C !important;
            box-shadow: 0 0 0 3px rgba(255, 199, 44, 0.35) !important;
        }
        input::placeholder, textarea::placeholder {
            color: #94A3B8 !important;
            opacity: 1 !important;
        }
        div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"], li[role="option"] {
            background-color: #112240 !important;
            color: #FFFFFF !important;
            border: 1.5px solid #38BDF8 !important;
        }
        li[role="option"] {
            color: #FFFFFF !important;
        }
        li[role="option"]:hover {
            background-color: #1E3A8A !important;
            color: #FFC72C !important;
        }
        [data-testid="stExpander"] {
            background-color: #112240 !important;
            border: 2px solid #1E3A8A !important;
            border-radius: 8px !important;
        }
        [data-testid="stExpander"] summary {
            color: #60A5FA !important;
            font-weight: 700 !important;
        }
        [data-testid="stAlert"] {
            background-color: #16243E !important;
            border: 2px solid #F59E0B !important;
            color: #FEF3C7 !important;
        }
        button[kind="primary"] {
            background-color: #0284C7 !important;
            border: 2px solid #38BDF8 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        div[data-baseweb="tab-list"] {
            background-color: transparent !important;
        }
        div[data-baseweb="tab"] {
            color: #CBD5E1 !important;
        }
        div[aria-selected="true"] {
            color: #FFC72C !important;
            border-bottom-color: #FFC72C !important;
        }
        """
    elif "Modo Claro" in modo_apariencia:
        css += """
        .stApp {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }
        h1 { color: #002B49 !important; }
        h2, h3 { color: #003366 !important; }
        label, [data-testid="stWidgetLabel"] p { color: #002B49 !important; font-weight: 700 !important; }
        input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
            border: 2px solid #004B87 !important;
        }
        [data-testid="stExpander"] {
            background-color: #F8FAFC !important;
            border: 2px solid #CBD5E1 !important;
        }
        """
    elif "Alto Contraste Oscuro" in modo_apariencia:
        css += """
        .stApp {
            background-color: #121212 !important;
            color: #FFFFFF !important;
        }
        h1, h2, h3, h4, label, [data-testid="stWidgetLabel"] p {
            color: #FFE600 !important;
        }
        input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {
            background-color: #000000 !important;
            color: #FFE600 !important;
            border: 2px solid #FFE600 !important;
        }
        [data-testid="stExpander"] {
            background-color: #1E1E1E !important;
            border: 2px solid #FFE600 !important;
        }
        [data-testid="stExpander"] summary {
            color: #FFE600 !important;
        }
        """
    elif "Modo Sepia" in modo_apariencia:
        css += """
        .stApp {
            background-color: #FBF0D9 !important;
            color: #2B2B2B !important;
        }
        h1 { color: #5C3A1E !important; }
        h2, h3 { color: #3B2613 !important; }
        label, [data-testid="stWidgetLabel"] p {
            color: #3B2613 !important;
        }
        input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {
            background-color: #FFFDF7 !important;
            color: #2B2B2B !important;
            border: 1.5px solid #C4B59D !important;
        }
        [data-testid="stExpander"] {
            background-color: #F4E7C5 !important;
            border: 1.5px solid #C4B59D !important;
        }
        """
    elif "100% Personalizado" in modo_apariencia:
        css += f"""
        .stApp {{
            background-color: {bg_col} !important;
            color: {text_col} !important;
        }}
        h1, h2, h3, h4, label, [data-testid="stWidgetLabel"] p {{
            color: {text_col} !important;
        }}
        input[type="text"], textarea, .stSelectbox [data-baseweb="select"] {{
            background-color: {card_col} !important;
            color: {text_col} !important;
            border: 2px solid {btn_col} !important;
        }}
        button[kind="primary"] {{
            background-color: {btn_col} !important;
        }}
        """

    if "Monocromático" in daltonismo_filtro:
        css += """
        .stApp {
            filter: grayscale(100%) contrast(115%) !important;
        }
        """

    css += "\n</style>"
    st.markdown(css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONFIGURACIÓN E INTERFAZ STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ReclamaSalud — Asistente de Reclamaciones",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_rag():
    return CorpusRAG()

rag = get_rag()

# Banner superior permanente
st.warning(
    "⚖️ **ADVERTENCIA OBLIGATORIA (EJERCICIO ACADÉMICO):**\n\n"
    "Esta herramienta es un ejercicio estrictamente académico desarrollado en el marco de la clase "
    "de Derecho e Inteligencia Artificial de la Pontificia Universidad Javeriana. "
    "**No constituye asesoría legal, no ofrece orientación médica y no sustituye la consulta con un abogado titulado, "
    "un profesional de la salud o las autoridades competentes.** En caso de una emergencia médica vital, comuníquese "
    "de inmediato con la línea 123 o acuda al centro asistencial de urgencias más cercano."
)

# Barra lateral
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
        ["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.3-70b-instruct:free", "mistralai/mistral-7b-instruct:free"],
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

    st.divider()
    st.markdown("### 🎨 Personalización y Accesibilidad")
    st.caption("Pautas WCAG 2.1 · Res. MinTIC 1519/2020 · Ley 1751/15")
    
    with st.expander("🛠️ Personalizar interfaz, colores y voz", expanded=False):
        modo_apariencia = st.selectbox(
            "Tema visual de la página:",
            [
                "🌟 Estándar Javeriana (Alto Contraste Azul y Oro)",
                "☀️ Javeriana Modo Claro (Contraste Reforzado)",
                "🌙 Alto Contraste Oscuro (Negro y Amarillo WCAG AAA)",
                "📜 Modo Sepia (Lectura Descansada)",
                "👁️ Modo Daltonismo Universal",
                "🎨 ¡100% Personalizado a mi gusto!"
            ],
            index=0,
            help="Selecciona el tema institucional Javeriana de alto contraste o personaliza tus propios colores."
        )

        es_alto_contraste = False
        if modo_apariencia == "🎨 ¡100% Personalizado a mi gusto!":
            st.markdown("**Personaliza tus propios colores:**")
            color_fondo = st.color_picker("Color de fondo de página:", value="#0A192F")
            color_texto = st.color_picker("Color de los textos:", value="#FFFFFF")
            color_tarjeta = st.color_picker("Color de recuadros y tarjetas:", value="#112240")
            color_primario = st.color_picker("Color de botones principales:", value="#0284C7")
        elif "🌙 Alto Contraste Oscuro" in modo_apariencia:
            color_fondo = "#121212"
            color_texto = "#FFE600"
            color_tarjeta = "#1E1E1E"
            color_primario = "#FFE600"
            es_alto_contraste = True
        elif "📜 Modo Sepia" in modo_apariencia:
            color_fondo = "#FBF0D9"
            color_texto = "#2B2B2B"
            color_tarjeta = "#F4E7C5"
            color_primario = "#7D4E24"
        elif "👁️ Modo Daltonismo" in modo_apariencia:
            color_fondo = "#0B192C"
            color_texto = "#FFFFFF"
            color_tarjeta = "#1E293B"
            color_primario = "#0055A5"
        elif "☀️ Javeriana Modo Claro" in modo_apariencia:
            color_fondo = "#FFFFFF"
            color_texto = "#0F172A"
            color_tarjeta = "#F8FAFC"
            color_primario = "#004B87"
        else: # "🌟 Estándar Javeriana (Alto Contraste Azul y Oro)"
            color_fondo = "#0A192F"
            color_texto = "#FFFFFF"
            color_tarjeta = "#112240"
            color_primario = "#0284C7"

        st.markdown("---")
        tam_fuente = st.slider(
            "Tamaño de letra (px):",
            min_value=14,
            max_value=26,
            value=16,
            step=1,
            help="14px compacto, 16px normal, 20px grande, 24px adulto mayor"
        )

        interlineado_opc = st.select_slider(
            "Interlineado de lectura:",
            options=["Compacto (1.3x)", "Estándar (1.6x)", "Amplio / Dislexia (1.9x)", "Máximo (2.2x)"],
            value="Estándar (1.6x)"
        )
        line_height_map = {
            "Compacto (1.3x)": "1.3",
            "Estándar (1.6x)": "1.6",
            "Amplio / Dislexia (1.9x)": "1.9",
            "Máximo (2.2x)": "2.2"
        }
        interlineado_css = line_height_map[interlineado_opc]

        fuente_opc = st.selectbox(
            "Tipo de letra (Tipografía):",
            [
                "Sans-Serif (Moderna y limpia)",
                "Serif (Clásica estilo código judicial)",
                "Lectura Fácil / Dislexia (Segoe UI / Comic)",
                "Monospace (Espacio fijo técnico)"
            ]
        )
        font_map = {
            "Sans-Serif (Moderna y limpia)": "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
            "Serif (Clásica estilo código judicial)": "Georgia, 'Times New Roman', Cambria, serif",
            "Lectura Fácil / Dislexia (Segoe UI / Comic)": "'Comic Sans MS', 'OpenDyslexic', 'Segoe UI', sans-serif",
            "Monospace (Espacio fijo técnico)": "'Courier New', Courier, monospace"
        }
        fuente_css = font_map[fuente_opc]

        daltonismo_filtro = st.selectbox(
            "Filtro visual para Daltonismo:",
            [
                "Sin filtro adicional",
                "Deuteranopía (Dificultad con verdes)",
                "Protanopía (Dificultad con rojos)",
                "Tritanopía (Dificultad con azules)",
                "Monocromático (Escala de grises)"
            ]
        )

        st.caption("🔊 *Los reproductores de voz cuentan con control de velocidad (0.75x, 1x, 1.25x) y volumen integrados.*")

    # Inyección de estilos de accesibilidad limpios y no destructivos
    inyectar_css_accesibilidad(
        modo_apariencia=modo_apariencia,
        bg_col=color_fondo,
        text_col=color_texto,
        card_col=color_tarjeta,
        btn_col=color_primario,
        tam_fuente=tam_fuente,
        interlineado=interlineado_css,
        fuente_css=fuente_css,
        daltonismo_filtro=daltonismo_filtro
    )

# Encabezado principal
col_logo, col_text = st.columns([1, 6])
with col_logo:
    st.markdown("# 🏥")
with col_text:
    st.title("ReclamaSalud — Asistente de Reclamaciones ante EPS")
    st.markdown("#### *Organiza tu caso, verifica plazos legales y crea una reclamación formal para tu EPS fundamentada en la ley colombiana.*")

st.divider()

# Entrevista guiada
st.subheader("📋 Entrevista Guiada de Reclamación")
st.write("Diligencia los siguientes campos para que el asistente organice los hechos, calcule los términos de vencimiento y fundamente la reclamación jurídica.")

with st.container():
    # Bloque 1: Datos de Afiliación
    st.markdown("### 1️⃣ Datos de Afiliación y Contacto")
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre_usuario = st.text_input("Nombre del paciente o peticionario (Usa nombre ficticio):", value="", placeholder="Ej. Juan Pérez (Simulado)")
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
            eps_nombre = st.text_input("Escribe el nombre de la EPS:", placeholder="Nombre de la EPS")
        regimen = st.selectbox("Régimen de Afiliación:", ["Contributivo (Cotizante)", "Contributivo (Beneficiario)", "Subsidiado"])
    with col3:
        ciudad = st.text_input("Ciudad / Municipio de residencia:", value="", placeholder="Ej. Bogotá D.C.")
        cedula_simulada = st.text_input("Número de documento ficticio:", value="", placeholder="Ej. 1.020.304.050")

    # Directorio de radicación de la EPS seleccionada
    info_eps = get_eps_info(eps_nombre)
    with st.expander(f"📮 Canales oficiales de radicación y contacto ({eps_nombre})", expanded=False):
        c_eps1, c_eps2 = st.columns([3, 2])
        with c_eps1:
            st.markdown(f"**Entidad:** {info_eps['nombre_completo']}")
            st.markdown(f"📞 **Línea gratuita nacional:** `{info_eps['telefono_nacional']}`  \n📍 **Línea Bogotá/Local:** `{info_eps['telefono_bogota']}`")
            st.caption(f"💡 **Consejo de radicación:** {info_eps['consejo_radicacion']}")
        with c_eps2:
            url_eps = info_eps.get("portal_web") or info_eps.get("portal_pqrs", "https://www.supersalud.gov.co")
            st.link_button(f"🌐 Portal Oficial de {eps_nombre}", url_eps, use_container_width=True)
            st.link_button("🏛️ Radicar en Supersalud", CANAL_SUPERSALUD["portal_pqrs"], use_container_width=True)
            st.caption("ℹ️ *Nota:* Para radicar por internet, la mayoría de EPS solicitan ingresar con tu usuario o cédula en su oficina virtual. Si la web de la EPS presenta errores, puedes radicar directamente en la Superintendencia de Salud.")

    st.divider()

    # Bloque 2: Tipo de Problema
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

    # Bloque 3: Triage, Cronología y Semáforo
    st.markdown("### 3️⃣ Cronología de los Hechos y Semáforo de Términos Legales")

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
        render_lector_audio(
            texto="Alerta de emergencia médica vital. Detenga el trámite de este documento. Los síntomas descritos corresponden a una posible urgencia vital. Comuníquese de inmediato a la línea de emergencias 123 en Colombia o traslade al paciente a la sala de urgencias más cercana. El artículo 14 de la Ley Estatutaria de Salud obliga a todas las clínicas y hospitales a prestar atención obligatoria e inmediata sin autorizaciones ni copagos.",
            titulo="Escuchar alerta de urgencia vital en voz alta",
            key="tts_urgencia"
        )
    else:
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            fecha_orden = st.date_input("Fecha de la orden o solicitud médica:", datetime.date.today())
            medico_tratante = st.text_input("Médico o especialidad que ordenó el servicio:", value="", placeholder="Ej. Dra. Martínez / Medicina Interna")
            servicio_solicitado = st.text_input("Nombre del medicamento, cita o examen solicitado:", value="", placeholder="Ej. Losartán 50mg / Cita con Neurología")
            
            # Semáforo de Término Legal Accesible (WCAG 2.1)
            d_cal, d_hab, est_semaforo, msg_semaforo = calcular_terminos_legales(fecha_orden, tipo_barrera)
            st.markdown("#### 🚦 Semáforo de Término Legal")
            render_semaforo_accesible(est_semaforo, msg_semaforo, daltonismo_filtro)

        with col_f2:
            st.markdown("#### 📝 Narración de los Hechos de tu Caso")
            relato_hechos = st.text_area(
                "✍️ Describe cronológicamente lo sucedido con la EPS:",
                value="",
                placeholder="Escribe aquí los hechos: fecha en que ordenaron el servicio, qué respuesta te dieron en la farmacia o EPS, cuánto tiempo llevas esperando y cómo ha afectado tu salud...",
                height=180
            )
            with st.expander("🎙️ ¿Cómo dictarle con tu voz a este cuadro?", expanded=False):
                st.markdown(
                    "Puedes narrar tu caso hablando directamente a tu micrófono sin escribir en el teclado:\n\n"
                    "- 💻 **En Windows (PC o Portátil):** Haz clic dentro del cuadro de texto superior y presiona la combinación de teclas **`Windows + H`**. Aparecerá el micrófono de Windows y transcribirá todo lo que hables en español directamente en la caja.\n"
                    "- 📱 **En celulares (Android o iPhone):** Toca dentro del cuadro de texto y presiona el ícono del **Micrófono 🎙️** en la esquina de tu teclado para dictar.\n"
                    "- 🍎 **En Mac:** Presiona dos veces la tecla `Fn` o activa el dictado por voz de macOS."
                )

    st.divider()

    # Bloque 4: Documentos de Soporte
    st.markdown("### 4️⃣ Documentos y Pruebas Disponibles")
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        tiene_formula = st.checkbox("Copia de orden médica o fórmula expedida por el médico tratante", value=False)
        tiene_pendiente = st.checkbox("Constancia de sello de 'pendiente' o comprobante de solicitud ante farmacia", value=False)
    with col_an2:
        tiene_radicado = st.checkbox("Número de radicado o reclamo previo ante la EPS", value=False)
        tiene_documento_id = st.checkbox("Copia de documento de identidad del paciente y peticionario", value=False)

# Procesamiento y generación
st.write("")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generar_btn = st.button("⚖️ Generar Borrador de Reclamación ante la EPS", type="primary", use_container_width=True, disabled=es_urgencia)

if generar_btn and not es_urgencia:
    nombre_final = nombre_usuario.strip() if nombre_usuario.strip() else "[NOMBRE DEL PETICIONARIO]"
    ciudad_final = ciudad.strip() if ciudad.strip() else "[CIUDAD O MUNICIPIO]"
    cedula_final = cedula_simulada.strip() if cedula_simulada.strip() else "[NÚMERO DE DOCUMENTO]"
    medico_final = medico_tratante.strip() if medico_tratante.strip() else "[MÉDICO TRATANTE]"
    servicio_final = servicio_solicitado.strip() if servicio_solicitado.strip() else "[MEDICAMENTO, CITA O EXAMEN SOLICITADO]"
    relato_final = relato_hechos.strip() if relato_hechos.strip() else "He acudido ante la entidad a solicitar el servicio prescrito sin que a la fecha se haya garantizado oportunamente."

    with st.spinner("Consultando el corpus normativo colombiano y estructurando la reclamación..."):
        consulta_rag = f"{tipo_barrera} {servicio_final} {relato_final}"
        documentos_recuperados = rag.search(consulta_rag, top_k=3)
        contexto_rag = rag.get_formatted_context(consulta_rag, top_k=3)

        borrador_texto = f"""Señores:
{eps_nombre.upper()}
Atención: Oficina de Peticiones, Quejas, Reclamos y Solicitudes (PQRS) / Gerencia de Servicio al Cliente
Ciudad: {ciudad_final}
Canal de radicación: [CORREO ELECTRÓNICO O PORTAL DE PQRD DE LA EPS]

ASUNTO: DERECHO DE PETICIÓN EN INTERÉS PARTICULAR (ARTÍCULO 23 DE LA CONSTITUCIÓN POLÍTICA Y LEY 1755 DE 2015) CON FUNDAMENTO EN EL DERECHO FUNDAMENTAL A LA SALUD (LEY ESTATUTARIA 1751 DE 2015).

Peticionario(a): {nombre_final}
Documento de Identidad: C.C. {cedula_final}
Calidad: Afiliado(a) en régimen {regimen}
Calidad de actuación: {rol_usuario}
Municipio de atención: {ciudad_final}

Yo, {nombre_final}, mayor de edad, identificado(a) como aparece al pie de mi firma, en ejercicio del derecho fundamental de petición consagrado en el artículo 23 de la Constitución Política y en la Ley 1755 de 2015, y en garantía del derecho fundamental autónomo e irrenunciable a la salud consagrado en la Ley Estatutaria 1751 de 2015, acudo respetuosamente ante su despacho con fundamento en los siguientes:

I. HECHOS
1. Me encuentro válidamente afiliado(a) a la entidad {eps_nombre} en calidad de {regimen} en el municipio de {ciudad_final}.
2. Con fecha {fecha_orden.strftime('%d de %B de %Y')}, el profesional adscrito a su red prestadora, {medico_final}, prescribió y ordenó formalmente el servicio consistente en: {servicio_final}.
3. Hechos y trámites surtidos: {relato_final}
4. A la fecha de radicación de la presente petición, han transcurrido términos desproporcionados sin que la entidad garantice de manera continua, efectiva y oportuna el servicio ordenado, incurriendo en una dilación administrativa injustificada.
5. Dicha conducta lesiona el principio de continuidad e integralidad del tratamiento, trasladando de manera indebida a la parte usuaria cargas burocráticas y deficiencias de inventario o contratación que corresponden exclusivamente a la gestión de la EPS.

II. PETICIONES
1. Se AUTORICE Y GARANTICE DE FORMA INMEDIATA, OPORTUNA Y EFECTIVA la entrega / asignación / realización de: {servicio_final}, prescrito por el médico tratante.
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
Ciudad: {ciudad_final}
Dirección física: [INDICAR DIRECCIÓN COMPLETA PARA NOTIFICACIÓN]
Teléfono de contacto: [INDICAR NÚMERO DE TELÉFONO O CELULAR]
Correo electrónico para notificaciones: [INDICAR CORREO ELECTRÓNICO]

Atentamente,

___________________________________________
FIRMA
Nombre: {nombre_final}
C.C. n.° {cedula_final}
{f'En calidad de: {rol_usuario}' if 'paciente directamente' not in rol_usuario.lower() else ''}

================================================================================
ADVERTENCIA: Este documento es un borrador académico generado por ReclamaSalud. 
Verifique los datos entre corchetes antes de radicar. No constituye asesoría legal formal.
================================================================================
"""

        st.session_state["borrador_generado"] = borrador_texto
        st.session_state["documentos_recuperados"] = documentos_recuperados
        st.session_state["contexto_rag"] = contexto_rag
        st.session_state["datos_caso"] = {
            "nombre": nombre_final,
            "eps": eps_nombre,
            "regimen": regimen,
            "ciudad": ciudad_final,
            "barrera": tipo_barrera,
            "servicio": servicio_final,
            "fecha": fecha_orden
        }

# Visualización de resultados
if "borrador_generado" in st.session_state and not es_urgencia:
    st.success("✅ Reclamación jurídica estructurada y fundamentada exitosamente.")
    
    tab_doc, tab_resumen, tab_fuentes, tab_hoja_ruta = st.tabs([
        "📄 Borrador de Derecho de Petición",
        "📊 Resumen del Caso",
        "🔍 Fuentes Jurídicas del Corpus (RAG)",
        "🗺️ ¿Qué hacer si no responden? (Ruta de Escalamiento)"
    ])

    with tab_doc:
        st.markdown("### Borrador Formal de Derecho de Petición ante la EPS")
        render_lector_audio(
            texto=st.session_state["borrador_generado"],
            titulo="Escuchar Derecho de Petición en voz alta",
            key="tts_peticion"
        )
        st.caption("Revisa el texto, completa los campos entre corchetes `[...]` y descarga tu documento en PDF o Texto.")
        st.text_area("Texto de la reclamación:", value=st.session_state["borrador_generado"], height=440)
        
        col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
        with col_d1:
            st.download_button(
                label="📥 Descargar Texto (.txt)",
                data=st.session_state["borrador_generado"],
                file_name=f"derecho_peticion_{eps_nombre.replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_d2:
            if FPDF_INSTALADO:
                try:
                    pdf_bytes = generar_pdf_derecho_peticion(st.session_state["borrador_generado"])
                    st.download_button(
                        label="📄 Descargar en PDF Formal",
                        data=pdf_bytes,
                        file_name=f"derecho_peticion_{eps_nombre.replace(' ', '_').lower()}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.caption(f"Error generando PDF: {e}")
            else:
                st.caption("ℹ️ PDF disponible cuando subas el archivo requirements.txt actualizado a GitHub.")

        with col_d3:
            st.info("💡 **Consejo de radicación:** Radica este documento a través del portal de PQRD de tu EPS o en ventanilla física, exigiendo copia sellada con fecha y número de radicado.")

    with tab_resumen:
        st.markdown("### 📊 Ficha Resumen del Caso")
        datos = st.session_state.get("datos_caso", {})
        st.write(f"**Peticionario(a):** {datos.get('nombre', '')}")
        st.write(f"**EPS Reclamada:** {datos.get('eps', '')}")
        st.write(f"**Régimen y Ciudad:** {datos.get('regimen', '')} · {datos.get('ciudad', '')}")
        st.write(f"**Barrera Identificada:** {datos.get('barrera', '')}")
        st.write(f"**Servicio Involucrado:** {datos.get('servicio', '')}")
        st.write(f"**Fecha de orden médica:** {datos.get('fecha', datetime.date.today()).strftime('%d/%m/%Y')}")

    with tab_fuentes:
        st.markdown("### 🔍 Artículos y Subreglas Recuperadas del Corpus (RAG)")
        st.write("El asistente recuperó los siguientes fragmentos de fuentes oficiales para sustentar la reclamación:")
        for idx, doc in enumerate(st.session_state.get("documentos_recuperados", []), 1):
            with st.expander(f"📌 [Fuente {idx}] {doc['source_title']} — {doc['section']}"):
                st.code(doc["text"], language="text")

    with tab_hoja_ruta:
        st.markdown("### 🗺️ Hoja de Ruta Post-Reclamación")
        render_lector_audio(
            texto="Hoja de ruta post reclamación. Paso 1: Radica el documento por el portal web oficial o en ventanilla física exigiendo sello de recibido con fecha, hora y número de radicado. Paso 2: Si la EPS responde favorablemente, acude por tu servicio. Paso 3A: Si la EPS no responde o niega el servicio, presenta queja formal ante la Superintendencia Nacional de Salud aportando copia de tu petición. Paso 3B: Si la falta de atención compromete tu salud o vida digna, puedes interponer una Acción de Tutela con apoyo gratuito de la Personería o la Defensoría del Pueblo.",
            titulo="Escuchar Hoja de Ruta en voz alta",
            key="tts_ruta"
        )
        st.write("¿Qué pasos debes seguir una vez tengas tu derecho de petición listo?")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### Paso 1: Radicación y Custodia de la Prueba")
            st.write(
                "1. Radica el documento por el portal web oficial de PQRS de tu EPS o en la sede física de atención.\n"
                "2. **Guarda el comprobante:** Exige sello de recibido con fecha, hora y número de radicado (o pantallazo si fue virtual).\n"
                "3. Revisa el semáforo de términos de ReclamaSalud para saber exactamente cuándo vence el plazo de ley."
            )

            st.markdown("#### Paso 2: Si la EPS responde favorablemente")
            st.write("Acude a reclamar el medicamento o asiste a la cita programada llevando tu número de autorización.")

        with col_p2:
            st.markdown("#### Paso 3A: Vía Administrativa — Queja en Supersalud")
            st.write(
                "Si la EPS **no responde en el término** o **niega el servicio injustificadamente**:\n"
                "- Presenta una denuncia formal ante la Superintendencia Nacional de Salud aportando copia de tu petición radicada.\n"
                "- La Supersalud puede ordenar medidas cautelares y conminar a la EPS a entregar el servicio en 48 a 72 horas."
            )
            st.link_button("🚨 Radicar Queja en la Superintendencia de Salud", CANAL_SUPERSALUD["portal_pqrs"], use_container_width=True)

            st.markdown("#### Paso 3B: Vía Judicial Constitucional — Acción de Tutela")
            st.write(
                "Si la falta de atención o medicamento compromete tu salud o tu vida digna:\n"
                "- Puedes interponer una **Acción de Tutela** ante cualquier juez de la República por vulneración al derecho fundamental a la salud (Ley 1751/2015).\n"
                "- **Apoyo gratuito:** Puedes acudir a la **Personería Municipal**, a la **Defensoría del Pueblo** o al Consultorio Jurídico de la Pontificia Universidad Javeriana para que te ayuden a redactarla sin costo."
            )

st.divider()
st.caption(
    "⚖️ **ReclamaSalud** · Pontificia Universidad Javeriana · Facultad de Ciencias Jurídicas · 2026-II · "
    "Construido con Streamlit, LangChain, fpdf2 y Python para la clase de Derecho e Inteligencia Artificial."
)
